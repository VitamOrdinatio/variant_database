#!/usr/bin/env python3
"""MARK reconnaissance for VDB Phase 4.3 Assertion Record planning.

This script inspects selected Registration Unit SQLite databases declared by the
Phase 4.2 downstream Assertion Record input manifest. It emits exploratory
receipts for resolver-policy and Layer 2 fixture planning.

It does not create Assertion Records.
It does not derive topology.
It opens SQLite databases read-only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import sqlite3
import tarfile
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

DEFAULT_INPUT_MANIFEST = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv"
)
DEFAULT_OUTPUT_ROOT = Path("/root/Desktop")
DEFAULT_CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"

CANDIDATE_TABLE_TERMS = ["assertion", "assertions", "claim", "claims", "relationship", "relationships"]
SUPPORT_TABLE_TERMS = ["source_identity", "source_identities", "artifact", "artifacts", "package", "packages", "metadata"]
CANDIDATE_COLUMN_TERMS = [
    "assertion", "claim", "relationship", "participant", "source_identity", "source_artifact",
    "artifact_id", "artifact", "package_id", "producer_family", "assertion_type", "source_record",
    "source_row", "record_ref", "row_ref",
]
ASSERTION_ID_COLUMN_TERMS = ["assertion_registration_id", "source_assertion_registration_id", "assertion_id", "claim_id"]
ASSERTION_TYPE_COLUMN_TERMS = ["assertion_type", "claim_type", "type", "relationship_type", "kind"]
SOURCE_ARTIFACT_COLUMN_TERMS = ["source_artifact", "artifact_id", "artifact_path", "source_file", "source_table"]
SOURCE_IDENTITY_COLUMN_TERMS = ["source_identity", "identity_id", "participant_id", "gene_id", "variant_id", "sample_id", "phenotype"]
SOURCE_RECORD_COLUMN_TERMS = ["source_record", "source_row", "record_ref", "row_ref", "row_id", "line_number"]
PARTICIPANT_COLUMN_TERMS = ["sample", "variant", "gene", "phenotype", "transcript", "source", "participant"]
RELATIONSHIP_COLUMN_TERMS = ["relationship", "predicate", "relation", "assertion_type", "claim_type"]
SIDECAR_SUFFIXES = ("-journal", "-wal", "-shm", ".sqlite-journal", ".db-journal")


def utc_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_bool(value: bool) -> str:
    return "true" if value else "false"


def safe_str(value: Any) -> str:
    if value is None:
        return "not_reported"
    text = str(value)
    if text == "":
        return "not_reported"
    return text.replace("\n", " ").replace("\r", " ")


def contains_any(value: str, terms: Sequence[str]) -> bool:
    lower = value.lower()
    return any(term in lower for term in terms)


def matching_terms(value: str, terms: Sequence[str]) -> List[str]:
    lower = value.lower()
    return [term for term in terms if term in lower]


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: List[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: safe_str(row.get(field)) for field in fieldnames})


def write_single_row_tsv(path: Path, row: Dict[str, Any]) -> None:
    write_tsv(path, [row], list(row.keys()))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def list_sidecars(registration_unit_path: Optional[Path], sqlite_path: Path) -> List[str]:
    roots: List[Path] = []
    if registration_unit_path and registration_unit_path.exists():
        roots.append(registration_unit_path)
    if sqlite_path.parent.exists() and sqlite_path.parent not in roots:
        roots.append(sqlite_path.parent)
    sidecars: List[str] = []
    for root in roots:
        try:
            for candidate in root.rglob("*"):
                if candidate.is_file() and candidate.name.endswith(SIDECAR_SUFFIXES):
                    sidecars.append(str(candidate))
        except Exception as exc:
            sidecars.append(f"INSPECTION_ERROR:{root}:{exc}")
    return sorted(set(sidecars))


def resolve_path(repo_root: Path, value: Optional[str]) -> Optional[Path]:
    if value is None:
        return None
    value = value.strip()
    if not value or value in {"not_reported", "not_available", "unresolved"}:
        return None
    path = Path(value)
    return path if path.is_absolute() else (repo_root / path).resolve()


def get_first(row: Dict[str, str], names: Sequence[str]) -> Optional[str]:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return None


def resolve_sqlite_path(repo_root: Path, row: Dict[str, str]) -> Tuple[Optional[Path], str]:
    direct = get_first(row, ["registration_unit_sqlite_path", "sqlite_path", "registration_sqlite_path", "vdb_sqlite_path"])
    if direct:
        resolved = resolve_path(repo_root, direct)
        if resolved:
            return resolved, "registration_unit_sqlite_path"
    unit_path_value = get_first(row, ["registration_unit_path", "registration_unit_reference", "registration_unit_dir"])
    unit_path = resolve_path(repo_root, unit_path_value)
    if unit_path:
        for name in ["vdb.sqlite", "registration_unit.sqlite", "registration.sqlite"]:
            candidate = unit_path / name
            if candidate.exists():
                return candidate, f"{unit_path_value}/{name}"
        return unit_path / "vdb.sqlite", "registration_unit_path/vdb.sqlite_assumed"
    return None, "unresolved"


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def connect_readonly(sqlite_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{sqlite_path.as_posix()}?mode=ro", uri=True)


def sqlite_tables(conn: sqlite3.Connection) -> List[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    return [row[0] for row in rows]


def table_columns(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    rows = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})").fetchall()
    return [
        {"cid": cid, "column_name": name, "column_type": col_type, "notnull": notnull, "default_value": default_value, "primary_key": pk}
        for cid, name, col_type, notnull, default_value, pk in rows
    ]


def table_count(conn: sqlite3.Connection, table_name: str) -> Tuple[Optional[int], str]:
    try:
        value = conn.execute(f"SELECT COUNT(*) FROM {quote_identifier(table_name)}").fetchone()[0]
        return int(value), "counted"
    except Exception as exc:
        return None, f"count_failed:{exc}"


def sample_values(conn: sqlite3.Connection, table_name: str, columns: Sequence[str], limit: int) -> List[Dict[str, Any]]:
    if not columns or limit <= 0:
        return []
    try:
        safe_columns = ", ".join(quote_identifier(col) for col in columns)
        rows = conn.execute(f"SELECT {safe_columns} FROM {quote_identifier(table_name)} LIMIT ?", (limit,)).fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as exc:
        return [{"sample_error": str(exc)}]


def group_values(conn: sqlite3.Connection, table_name: str, column_name: str, limit: int = 250) -> List[Tuple[str, int]]:
    try:
        rows = conn.execute(
            f"SELECT {quote_identifier(column_name)}, COUNT(*) AS n FROM {quote_identifier(table_name)} GROUP BY {quote_identifier(column_name)} ORDER BY n DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [(safe_str(value), int(count)) for value, count in rows]
    except Exception:
        return []


def semantic_role(column_name: str) -> str:
    if contains_any(column_name, ASSERTION_ID_COLUMN_TERMS):
        return "assertion_identity_candidate"
    if contains_any(column_name, ASSERTION_TYPE_COLUMN_TERMS):
        return "assertion_type_candidate"
    if contains_any(column_name, SOURCE_ARTIFACT_COLUMN_TERMS):
        return "source_artifact_reference_candidate"
    if contains_any(column_name, SOURCE_IDENTITY_COLUMN_TERMS):
        return "source_identity_or_participant_candidate"
    if contains_any(column_name, SOURCE_RECORD_COLUMN_TERMS):
        return "source_record_reference_candidate"
    if contains_any(column_name, PARTICIPANT_COLUMN_TERMS):
        return "participant_candidate"
    if contains_any(column_name, RELATIONSHIP_COLUMN_TERMS):
        return "relationship_candidate"
    return "not_classified"


def score_candidate_table(table_name: str, columns: Sequence[str]) -> Tuple[int, List[str]]:
    reasons: List[str] = []
    score = 0
    table_matches = matching_terms(table_name, CANDIDATE_TABLE_TERMS)
    support_matches = matching_terms(table_name, SUPPORT_TABLE_TERMS)
    if table_matches:
        score += 3
        reasons.append("table_name:" + ",".join(table_matches))
    if support_matches:
        score += 1
        reasons.append("support_table_name:" + ",".join(support_matches))
    for column in columns:
        matches = matching_terms(column, CANDIDATE_COLUMN_TERMS)
        if matches:
            score += min(2, len(matches))
            reasons.append(f"column:{column}:{','.join(matches)}")
    return score, reasons


def has_column(columns: Sequence[str], terms: Sequence[str]) -> bool:
    return any(contains_any(column, terms) for column in columns)


def matching_columns(columns: Sequence[str], terms: Sequence[str]) -> List[str]:
    return [column for column in columns if contains_any(column, terms)]


def recommendation_for(producer_family: str, table_name: str, assertion_type: str, candidate_score: int, fallback_required: bool) -> Tuple[str, str, str, str]:
    pf = producer_family.upper()
    lower_table = table_name.lower()
    lower_type = assertion_type.lower()
    notes: List[str] = []
    if candidate_score < 3:
        return "not_applicable", "not_applicable", "not_applicable", "low candidate score"
    action, assertion, relationship = "needs_review", (assertion_type if assertion_type not in {"not_reported", "None"} else "needs_review"), "needs_review"
    if pf == "VAP":
        if any(term in lower_type or term in lower_table for term in ["variant", "annotation", "observation"]):
            action = "index_with_note" if fallback_required else "index"
            assertion = "variant_observation_or_annotation"
            relationship = "variant claim preserved from VAP registration"
        elif any(term in lower_type or term in lower_table for term in ["validation", "quality"]):
            assertion = "validation_result_or_quality_status"
            relationship = "producer validation or quality claim"
        notes.append("VAP heuristic only; DEX review required")
    elif pf == "GSC":
        if any(term in lower_type or term in lower_table for term in ["semantic", "consensus", "gene", "source", "contribution"]):
            action = "index_with_note" if fallback_required else "index"
            assertion = "semantic_prior_or_source_contribution"
            relationship = "phenotype-gene or source-contribution claim preserved from GSC registration"
        elif "validation" in lower_type or "validation" in lower_table:
            assertion = "producer_validation_result"
            relationship = "producer validation claim"
        notes.append("GSC heuristic only; DEX review required")
    else:
        notes.append("unknown producer family; DEX review required")
    if fallback_required:
        notes.append("fallback key likely required")
    return action, assertion, relationship, "; ".join(notes)


def create_archive(output_dir: Path) -> Tuple[Path, Path, str]:
    archive_path = output_dir.with_suffix(".tgz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(output_dir, arcname=output_dir.name)
    checksum = sha256_file(archive_path)
    checksum_path = Path(str(archive_path) + ".sha256")
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n", encoding="utf-8")
    return archive_path, checksum_path, checksum


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 4.3 assertion registration reconnaissance on MARK.")
    parser.add_argument("--input-manifest", default=str(DEFAULT_INPUT_MANIFEST))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--corpus-generation-id", default=DEFAULT_CORPUS_GENERATION_ID)
    parser.add_argument("--max-sample-rows", type=int, default=5)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    input_manifest = resolve_path(repo_root, args.input_manifest) or Path(args.input_manifest).resolve()
    output_root = Path(args.output_root).resolve()
    timestamp = utc_timestamp()
    output_dir = output_root / f"assertion_registration_reconnaissance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "run_id": f"assertion_registration_reconnaissance_{timestamp}",
        "started_at": iso_now(),
        "completed_at": "not_completed",
        "repo_root": str(repo_root),
        "input_manifest": str(input_manifest),
        "output_dir": str(output_dir),
        "corpus_generation_id_expected": args.corpus_generation_id,
        "exploratory_status": "reconnaissance_only",
        "certification_status": "not_certification_evidence",
        "creates_assertion_records": False,
        "derives_topology": False,
        "characterizes_geometry": False,
        "constructs_surfaces": False,
        "emits_projections": False,
        "performs_rdgp_reasoning": False,
        "opens_sqlite_read_only": True,
        "mutates_registration_units": False,
        "status": "running",
        "errors": [],
    }

    table_rows: List[Dict[str, Any]] = []
    column_rows: List[Dict[str, Any]] = []
    candidate_rows: List[Dict[str, Any]] = []
    candidate_column_rows: List[Dict[str, Any]] = []
    type_rows: List[Dict[str, Any]] = []
    sample_rows: List[Dict[str, Any]] = []
    artifact_rows: List[Dict[str, Any]] = []
    identity_rows: List[Dict[str, Any]] = []
    producer_summary: Dict[str, Dict[str, Any]] = {}
    key_rows: List[Dict[str, Any]] = []
    recommendation_rows: List[Dict[str, Any]] = []
    sidecar_before_rows: List[Dict[str, Any]] = []
    sidecar_after_rows: List[Dict[str, Any]] = []
    sidecar_summary: Dict[str, Any] = {"units": [], "new_sidecars_total": 0, "new_sidecars": []}
    non_mutation_summary: Dict[str, Any] = {"opens_sqlite_read_only": True, "mutates_registration_units": False, "unit_checks": []}
    unresolved_questions: List[str] = []

    try:
        if not input_manifest.exists():
            raise FileNotFoundError(f"Input manifest not found: {input_manifest}")
        manifest_rows = read_tsv(input_manifest)
        if not manifest_rows:
            raise RuntimeError(f"Input manifest is empty: {input_manifest}")
        summary["manifest_row_count"] = len(manifest_rows)
        summary["selected_registration_unit_count"] = len(manifest_rows)

        for manifest_index, row in enumerate(manifest_rows, start=1):
            registration_unit_id = get_first(row, ["registration_unit_id", "registration_unit_label", "unit_id", "label"]) or f"manifest_row_{manifest_index}"
            producer_family = get_first(row, ["producer_family", "expected_producer_family"]) or "not_reported"
            source_package_id = get_first(row, ["source_package_id", "package_id"]) or "not_reported"
            corpus_generation_id = get_first(row, ["corpus_generation_id"]) or args.corpus_generation_id
            registration_unit_path = resolve_path(repo_root, get_first(row, ["registration_unit_path", "registration_unit_reference", "registration_unit_dir"]))
            sqlite_path, sqlite_resolution = resolve_sqlite_path(repo_root, row)

            producer_summary.setdefault(producer_family, {
                "producer_family": producer_family, "registration_unit_count": 0, "table_count": 0,
                "candidate_table_count": 0, "assertion_registration_type_count": 0,
                "rows_in_candidate_tables": 0, "fallback_likely_table_count": 0, "errors": [],
            })
            producer_summary[producer_family]["registration_unit_count"] += 1
            unit_summary = {"registration_unit_id": registration_unit_id, "producer_family": producer_family, "sqlite_path": str(sqlite_path) if sqlite_path else "unresolved", "sqlite_resolution": sqlite_resolution, "read_only_opened": False, "error": ""}

            if not sqlite_path or not sqlite_path.exists():
                message = f"SQLite path missing for {registration_unit_id}: {sqlite_path}"
                summary["errors"].append(message)
                producer_summary[producer_family]["errors"].append(message)
                unresolved_questions.append(message)
                non_mutation_summary["unit_checks"].append(unit_summary)
                continue

            before = list_sidecars(registration_unit_path, sqlite_path)
            sidecar_before_rows.extend({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "sidecar_path": s} for s in before)

            try:
                conn = connect_readonly(sqlite_path)
                unit_summary["read_only_opened"] = True
            except Exception as exc:
                message = f"Read-only SQLite open failed for {registration_unit_id}: {exc}"
                summary["errors"].append(message)
                producer_summary[producer_family]["errors"].append(message)
                unit_summary["error"] = message
                non_mutation_summary["unit_checks"].append(unit_summary)
                continue

            try:
                tables = sqlite_tables(conn)
                producer_summary[producer_family]["table_count"] += len(tables)
                for table_name in tables:
                    columns = table_columns(conn, table_name)
                    column_names = [c["column_name"] for c in columns]
                    row_count, row_count_status = table_count(conn, table_name)
                    candidate_score, candidate_reasons = score_candidate_table(table_name, column_names)
                    is_candidate = candidate_score >= 3 or table_name.lower() == "assertion_registrations"

                    table_rows.append({"corpus_generation_id": corpus_generation_id, "registration_unit_id": registration_unit_id, "producer_family": producer_family, "source_package_id": source_package_id, "sqlite_path": str(sqlite_path), "table_name": table_name, "row_count": row_count if row_count is not None else "not_available", "row_count_status": row_count_status, "candidate_assertion_table": normalize_bool(is_candidate), "candidate_score": candidate_score, "candidate_reason": ";".join(candidate_reasons) if candidate_reasons else "not_candidate"})

                    for col in columns:
                        base_col_row = {"corpus_generation_id": corpus_generation_id, "registration_unit_id": registration_unit_id, "producer_family": producer_family, "source_package_id": source_package_id, "table_name": table_name, "column_name": col["column_name"], "column_type": col["column_type"], "notnull": col["notnull"], "default_value": col["default_value"], "primary_key": col["primary_key"], "candidate_semantic_role": semantic_role(col["column_name"])}
                        column_rows.append(base_col_row)
                        if is_candidate:
                            candidate_column_rows.append(base_col_row)

                    if contains_any(table_name, SOURCE_ARTIFACT_COLUMN_TERMS) or has_column(column_names, SOURCE_ARTIFACT_COLUMN_TERMS):
                        artifact_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "table_name": table_name, "row_count": row_count if row_count is not None else "not_available", "artifact_reference_columns": ",".join(matching_columns(column_names, SOURCE_ARTIFACT_COLUMN_TERMS)) or "not_detected", "all_columns": ",".join(column_names)})
                    if contains_any(table_name, SOURCE_IDENTITY_COLUMN_TERMS) or has_column(column_names, SOURCE_IDENTITY_COLUMN_TERMS):
                        identity_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "table_name": table_name, "row_count": row_count if row_count is not None else "not_available", "source_identity_columns": ",".join(matching_columns(column_names, SOURCE_IDENTITY_COLUMN_TERMS)) or "not_detected", "all_columns": ",".join(column_names)})

                    if is_candidate:
                        producer_summary[producer_family]["candidate_table_count"] += 1
                        if row_count:
                            producer_summary[producer_family]["rows_in_candidate_tables"] += row_count
                        has_assertion_id = has_column(column_names, ASSERTION_ID_COLUMN_TERMS)
                        has_assertion_type = has_column(column_names, ASSERTION_TYPE_COLUMN_TERMS)
                        has_source_artifact = has_column(column_names, SOURCE_ARTIFACT_COLUMN_TERMS)
                        has_source_identity = has_column(column_names, SOURCE_IDENTITY_COLUMN_TERMS)
                        has_source_record = has_column(column_names, SOURCE_RECORD_COLUMN_TERMS)
                        has_participants = has_column(column_names, PARTICIPANT_COLUMN_TERMS)
                        has_relationships = has_column(column_names, RELATIONSHIP_COLUMN_TERMS)
                        fallback_required = not has_assertion_id
                        if fallback_required:
                            producer_summary[producer_family]["fallback_likely_table_count"] += 1
                        candidate_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "source_package_id": source_package_id, "table_name": table_name, "row_count": row_count if row_count is not None else "not_available", "candidate_score": candidate_score, "candidate_reasons": ";".join(candidate_reasons), "has_source_assertion_registration_id": normalize_bool(has_assertion_id), "has_assertion_type": normalize_bool(has_assertion_type), "has_source_artifact_reference": normalize_bool(has_source_artifact), "has_source_identity_reference": normalize_bool(has_source_identity), "has_source_record_reference": normalize_bool(has_source_record), "has_participant_fields": normalize_bool(has_participants), "has_relationship_fields": normalize_bool(has_relationships), "fallback_key_likely_required": normalize_bool(fallback_required)})
                        preferred_key_strategy = "source_assertion_registration_id" if has_assertion_id else "not_available"
                        fallback_key_strategy = "fallback_source_record_fingerprint" if fallback_required else "not_required"
                        risk_level = "low" if has_assertion_id else ("medium" if has_source_artifact and (has_source_record or has_participants) else "high")
                        key_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "candidate_table": table_name, "has_source_assertion_registration_id": normalize_bool(has_assertion_id), "has_assertion_type": normalize_bool(has_assertion_type), "has_source_artifact_id": normalize_bool(has_source_artifact), "has_source_record_reference": normalize_bool(has_source_record), "has_source_row_reference": normalize_bool(has_source_record), "has_participant_fields": normalize_bool(has_participants), "has_relationship_fields": normalize_bool(has_relationships), "preferred_key_strategy": preferred_key_strategy, "fallback_key_strategy": fallback_key_strategy, "fallback_required": normalize_bool(fallback_required), "key_risk_level": risk_level, "notes": "heuristic reconnaissance; DEX review required"})

                        type_columns = matching_columns(column_names, ASSERTION_TYPE_COLUMN_TERMS)
                        type_observations: List[Tuple[str, str, Any]] = []
                        if type_columns:
                            for type_column in type_columns:
                                grouped = group_values(conn, table_name, type_column)
                                if grouped:
                                    for observed_type, count in grouped:
                                        type_observations.append((type_column, observed_type, count))
                                else:
                                    type_observations.append((type_column, "not_resolved", "not_available"))
                        else:
                            type_observations.append(("not_detected", "not_reported", row_count if row_count is not None else "not_available"))
                        for type_column, observed_type, count in type_observations:
                            type_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "table_name": table_name, "type_column": type_column, "observed_assertion_registration_type": observed_type, "observed_row_count": count})
                            action, assertion, relationship, notes = recommendation_for(producer_family, table_name, observed_type, candidate_score, fallback_required)
                            recommendation_rows.append({"producer_family": producer_family, "registration_unit_id": registration_unit_id, "observed_table": table_name, "observed_assertion_registration_type": observed_type, "observed_row_count": count, "recommended_v1_action": action, "recommended_assertion_type": assertion, "recommended_relationship_class": relationship, "source_assertion_key_strategy": preferred_key_strategy if not fallback_required else fallback_key_strategy, "fallback_required": normalize_bool(fallback_required), "reason": "heuristic based on table/column/type names", "notes": notes})

                        interesting_cols: List[str] = []
                        for term_group in [ASSERTION_ID_COLUMN_TERMS, ASSERTION_TYPE_COLUMN_TERMS, SOURCE_ARTIFACT_COLUMN_TERMS, SOURCE_RECORD_COLUMN_TERMS, PARTICIPANT_COLUMN_TERMS, RELATIONSHIP_COLUMN_TERMS]:
                            for col in matching_columns(column_names, term_group):
                                if col not in interesting_cols:
                                    interesting_cols.append(col)
                        interesting_cols = (interesting_cols[:20] if interesting_cols else column_names[:10])
                        for i, sample in enumerate(sample_values(conn, table_name, interesting_cols, args.max_sample_rows), start=1):
                            sample_rows.append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "table_name": table_name, "sample_index": i, "sample_columns": ",".join(interesting_cols), "sample_json": json.dumps({k: safe_str(v) for k, v in sample.items()}, sort_keys=True)})
            except Exception as exc:
                message = f"Inspection failed for {registration_unit_id}: {exc}"
                summary["errors"].append(message)
                producer_summary[producer_family]["errors"].append(message)
                unit_summary["error"] = message
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

            after = list_sidecars(registration_unit_path, sqlite_path)
            sidecar_after_rows.extend({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "sidecar_path": s} for s in after)
            new_sidecars = sorted(set(after) - set(before))
            sidecar_summary["units"].append({"registration_unit_id": registration_unit_id, "producer_family": producer_family, "before_sidecar_count": len(before), "after_sidecar_count": len(after), "new_sidecar_count": len(new_sidecars), "new_sidecars": new_sidecars})
            if new_sidecars:
                sidecar_summary["new_sidecars_total"] += len(new_sidecars)
                sidecar_summary["new_sidecars"].extend(new_sidecars)
            non_mutation_summary["unit_checks"].append(unit_summary)

        producer_rows = []
        for producer_family, values in sorted(producer_summary.items()):
            row = dict(values)
            row["errors"] = "; ".join(values.get("errors", [])) if values.get("errors") else "none"
            producer_rows.append(row)
        if not candidate_rows:
            unresolved_questions.append("No assertion-registration candidate tables were detected by heuristic scan.")
        if not recommendation_rows:
            unresolved_questions.append("No resolver scope recommendations could be generated.")
        if any(row.get("fallback_required") == "true" for row in key_rows):
            unresolved_questions.append("At least one candidate table appears to require fallback source_assertion_key construction.")

        readme = f"""# Phase 4.3 Assertion Registration Reconnaissance Receipt

Run ID: `{summary['run_id']}`

Input manifest:

```text
{input_manifest}
```

This receipt is exploratory. It does not create Assertion Records, derive topology, characterize geometry, construct surfaces, emit projections, or perform RDGP reasoning.
"""
        (output_dir / "README.md").write_text(readme, encoding="utf-8")

        write_tsv(output_dir / "registration_unit_table_inventory.tsv", table_rows, ["corpus_generation_id", "registration_unit_id", "producer_family", "source_package_id", "sqlite_path", "table_name", "row_count", "row_count_status", "candidate_assertion_table", "candidate_score", "candidate_reason"])
        write_tsv(output_dir / "registration_unit_column_inventory.tsv", column_rows, ["corpus_generation_id", "registration_unit_id", "producer_family", "source_package_id", "table_name", "column_name", "column_type", "notnull", "default_value", "primary_key", "candidate_semantic_role"])
        write_tsv(output_dir / "assertion_registration_table_candidates.tsv", candidate_rows, ["registration_unit_id", "producer_family", "source_package_id", "table_name", "row_count", "candidate_score", "candidate_reasons", "has_source_assertion_registration_id", "has_assertion_type", "has_source_artifact_reference", "has_source_identity_reference", "has_source_record_reference", "has_participant_fields", "has_relationship_fields", "fallback_key_likely_required"])
        write_tsv(output_dir / "assertion_registration_column_inventory.tsv", candidate_column_rows, ["corpus_generation_id", "registration_unit_id", "producer_family", "source_package_id", "table_name", "column_name", "column_type", "notnull", "default_value", "primary_key", "candidate_semantic_role"])
        write_tsv(output_dir / "assertion_registration_type_inventory.tsv", type_rows, ["registration_unit_id", "producer_family", "table_name", "type_column", "observed_assertion_registration_type", "observed_row_count"])
        write_tsv(output_dir / "assertion_registration_sample_values.tsv", sample_rows, ["registration_unit_id", "producer_family", "table_name", "sample_index", "sample_columns", "sample_json"])
        write_tsv(output_dir / "source_artifact_reference_inventory.tsv", artifact_rows, ["registration_unit_id", "producer_family", "table_name", "row_count", "artifact_reference_columns", "all_columns"])
        write_tsv(output_dir / "source_identity_reference_inventory.tsv", identity_rows, ["registration_unit_id", "producer_family", "table_name", "row_count", "source_identity_columns", "all_columns"])
        write_tsv(output_dir / "producer_family_reconnaissance_summary.tsv", producer_rows, ["producer_family", "registration_unit_count", "table_count", "candidate_table_count", "assertion_registration_type_count", "rows_in_candidate_tables", "fallback_likely_table_count", "errors"])
        write_tsv(output_dir / "source_assertion_key_feasibility.tsv", key_rows, ["registration_unit_id", "producer_family", "candidate_table", "has_source_assertion_registration_id", "has_assertion_type", "has_source_artifact_id", "has_source_record_reference", "has_source_row_reference", "has_participant_fields", "has_relationship_fields", "preferred_key_strategy", "fallback_key_strategy", "fallback_required", "key_risk_level", "notes"])
        write_tsv(output_dir / "resolver_scope_recommendations.tsv", recommendation_rows, ["producer_family", "registration_unit_id", "observed_table", "observed_assertion_registration_type", "observed_row_count", "recommended_v1_action", "recommended_assertion_type", "recommended_relationship_class", "source_assertion_key_strategy", "fallback_required", "reason", "notes"])
        write_tsv(output_dir / "sidecar_before_inventory.tsv", sidecar_before_rows, ["registration_unit_id", "producer_family", "sidecar_path"])
        write_tsv(output_dir / "sidecar_after_inventory.tsv", sidecar_after_rows, ["registration_unit_id", "producer_family", "sidecar_path"])

        summary.update({"completed_at": iso_now(), "status": "completed_with_errors" if summary["errors"] else "completed", "table_inventory_count": len(table_rows), "column_inventory_count": len(column_rows), "assertion_registration_candidate_table_count": len(candidate_rows), "assertion_registration_type_inventory_count": len(type_rows), "source_artifact_reference_inventory_count": len(artifact_rows), "source_identity_reference_inventory_count": len(identity_rows), "source_assertion_key_feasibility_count": len(key_rows), "resolver_scope_recommendation_count": len(recommendation_rows), "new_sidecars_total": sidecar_summary["new_sidecars_total"]})
        non_mutation_summary["new_sidecars_total"] = sidecar_summary["new_sidecars_total"]
        non_mutation_summary["mutates_registration_units"] = sidecar_summary["new_sidecars_total"] > 0
        summary["mutates_registration_units"] = non_mutation_summary["mutates_registration_units"]
        write_json(output_dir / "non_mutation_summary.json", non_mutation_summary)
        write_json(output_dir / "sidecar_check_summary.json", sidecar_summary)
        (output_dir / "unresolved_questions.md").write_text("# Unresolved Questions\n\n" + ("\n".join(f"- {q}" for q in unresolved_questions) if unresolved_questions else "- None detected by reconnaissance heuristics.") + "\n", encoding="utf-8")
        write_json(output_dir / "reconnaissance_run_summary.json", summary)
        write_single_row_tsv(output_dir / "reconnaissance_run_summary.tsv", summary)
        archive_path, checksum_path, checksum = create_archive(output_dir)
        summary["archive_path"] = str(archive_path)
        summary["archive_sha256_path"] = str(checksum_path)
        summary["archive_sha256"] = checksum
        write_json(output_dir / "reconnaissance_run_summary.json", summary)
        write_single_row_tsv(output_dir / "reconnaissance_run_summary.tsv", summary)
        archive_path.unlink(missing_ok=True)
        checksum_path.unlink(missing_ok=True)
        archive_path, checksum_path, checksum = create_archive(output_dir)
        print("Reconnaissance complete")
        print(f"Receipt directory: {output_dir}")
        print(f"Archive: {archive_path}")
        print(f"SHA256: {checksum_path}")
        print(f"Status: {summary['status']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"  - {error}")
        return 0 if not summary["errors"] else 2
    except Exception as exc:
        summary["completed_at"] = iso_now()
        summary["status"] = "failed"
        summary["errors"].append(str(exc))
        write_json(output_dir / "reconnaissance_run_summary.json", summary)
        write_single_row_tsv(output_dir / "reconnaissance_run_summary.tsv", summary)
        try:
            archive_path, checksum_path, checksum = create_archive(output_dir)
            print(f"Failed reconnaissance archived: {archive_path}")
            print(f"SHA256: {checksum_path}")
        except Exception as archive_exc:
            print(f"Archive creation also failed: {archive_exc}")
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

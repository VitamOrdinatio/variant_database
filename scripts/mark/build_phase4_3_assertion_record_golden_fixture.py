#!/usr/bin/env python3
"""Build a Phase 4.3 Assertion Record golden fixture candidate on MARK.

This script is an acquisition/export tool. It is intended to be developed on
sys76, committed to git, pulled onto MARK, and run from the VDB repository root
on MARK. It writes a compressed real-world-derived Layer 2 fixture candidate to
/root/Desktop for manual retrieval and sys76 curation.

It does not create production Assertion Records, does not derive topology, does
not run Layer 2 validation, and does not run Layer 3 MARK validation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sqlite3
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

DEFAULT_INPUT_MANIFEST = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/"
    "downstream_assertion_record_input_manifest.tsv"
)
DEFAULT_OUTPUT_ROOT = Path("/root/Desktop")
DEFAULT_FIXTURE_PREFIX = "phase4_3_assertion_record_golden_fixture"
DEFAULT_FIXTURE_ID = "phase4_3_assertion_record_golden_fixture_v1"
DEFAULT_CONTRACT_ID = "phase4_3_assertion_record_golden_fixture_contract"
DEFAULT_CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"
BUILDER_NAME = "build_phase4_3_assertion_record_golden_fixture.py"
BUILDER_VERSION = "v0.1"
REQUIRED_UNITS = [
    "gsc_epilepsy",
    "gsc_mitochondrial_disease",
    "vap_hg002",
    "vap_median_ERR10619300",
    "vap_q1_ERR10619212",
    "vap_q3_ERR10619225",
]
TABLES_TO_SLICE = [
    "assertion_registrations",
    "source_identities",
    "artifacts",
    "tep_packages",
    "schema_metadata",
]
SIDECAR_SUFFIXES = (
    "-wal",
    "-shm",
    ".sqlite-journal",
    ".db-journal",
    "-journal",
)


def utc_timestamp_for_name() -> str:
    return datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise RuntimeError(f"TSV has no header: {path}")
        return [dict(row) for row in reader]


def collect_fieldnames(rows: Sequence[Dict[str, Any]]) -> List[str]:
    seen: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.append(key)
    return seen or ["status"]


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value).replace("\r", " ").replace("\n", " ")


def write_tsv(path: Path, rows: Sequence[Dict[str, Any]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = collect_fieldnames(rows)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: normalize_cell(row.get(k, "")) for k in fieldnames})


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_sidecars(paths: Iterable[Path]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for db_path in paths:
        if not db_path:
            continue
        parent = db_path.parent
        stem = db_path.name
        candidates: List[str] = []
        for entry in parent.iterdir():
            name = entry.name
            if name.startswith(stem) and any(name.endswith(suffix) for suffix in SIDECAR_SUFFIXES):
                candidates.append(str(entry))
            elif any(name.endswith(suffix) and db_path.stem in name for suffix in SIDECAR_SUFFIXES):
                candidates.append(str(entry))
        out[str(db_path)] = sorted(set(candidates))
    return out


def sqlite_connect_readonly(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (table,)
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table: str) -> List[str]:
    rows = conn.execute(f"PRAGMA table_info({quote_ident(table)})").fetchall()
    return [str(row[1]) for row in rows]


def count_rows(conn: sqlite3.Connection, table: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) AS n FROM {quote_ident(table)}").fetchone()["n"])


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def stable_order_clause(columns: Sequence[str]) -> str:
    preferred = [
        "assertion_registration_id",
        "source_identity_id",
        "artifact_id",
        "package_id",
        "source_record_ref",
        "source_value",
        "identity_kind",
        "participant_role",
        "source_namespace",
    ]
    order_cols = [quote_ident(c) for c in preferred if c in columns]
    return ", ".join(order_cols) if order_cols else "rowid"


def select_all_rows(conn: sqlite3.Connection, table: str) -> List[Dict[str, Any]]:
    columns = table_columns(conn, table)
    order_by = stable_order_clause(columns)
    query = f"SELECT * FROM {quote_ident(table)} ORDER BY {order_by}"
    return [row_to_dict(row) for row in conn.execute(query)]


def resolve_registration_unit_id(row: Dict[str, str], ordinal: int) -> str:
    candidates = [
        "registration_unit_id",
        "selected_registration_unit_id",
        "unit_id",
        "registration_id",
        "source_registration_unit_id",
    ]
    for key in candidates:
        if row.get(key):
            return str(row[key]).strip()
    for key, value in row.items():
        if "registration" in key.lower() and "unit" in key.lower() and "id" in key.lower() and value:
            return str(value).strip()
    return f"registration_unit_{ordinal:03d}"


def resolve_producer_family(row: Dict[str, str], registration_unit_id: str) -> str:
    for key in ("producer_family", "producer", "source_producer_family"):
        if row.get(key):
            return str(row[key]).strip()
    lowered = registration_unit_id.lower()
    if lowered.startswith("vap"):
        return "VAP"
    if lowered.startswith("gsc"):
        return "GSC"
    return "not_reported"


def path_candidates_from_row(row: Dict[str, str]) -> List[str]:
    priority_keys = [
        "registration_unit_sqlite_path",
        "registration_unit_db_path",
        "sqlite_path",
        "sqlite_db_path",
        "registration_unit_database_path",
        "registration_unit_reference",
        "registration_unit_path",
        "registration_unit_dir",
        "registration_unit_directory",
        "source_registration_unit_reference",
        "source_registration_unit_path",
        "package_path",
        "tep_package_path",
    ]
    values: List[str] = []
    for key in priority_keys:
        if row.get(key):
            values.append(str(row[key]).strip())
    for key, value in row.items():
        if not value:
            continue
        key_l = key.lower()
        value_s = str(value).strip()
        if any(token in key_l for token in ("path", "reference", "sqlite", "db", "database", "package")):
            if value_s not in values:
                values.append(value_s)
        elif any(ext in value_s.lower() for ext in (".sqlite", ".sqlite3", ".db")):
            if value_s not in values:
                values.append(value_s)
    return values


def resolve_existing_path(candidate: str, repo_root: Path) -> Optional[Path]:
    if not candidate:
        return None
    candidate = candidate.strip()
    if candidate.startswith("file://"):
        candidate = candidate[len("file://") :]
    path = Path(candidate)
    possibilities = [path]
    if not path.is_absolute():
        possibilities.append(repo_root / path)
    for possible in possibilities:
        try:
            if possible.exists():
                return possible.resolve()
        except OSError:
            continue
    return None


def find_sqlite_under(path: Path) -> Optional[Path]:
    if path.is_file() and path.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
        return path.resolve()
    if not path.is_dir():
        return None
    matches: List[Path] = []
    for pattern in ("*.sqlite", "*.sqlite3", "*.db"):
        matches.extend(path.rglob(pattern))
    matches = sorted(p.resolve() for p in matches if p.is_file())
    if len(matches) == 1:
        return matches[0]
    preferred = [p for p in matches if "registration" in p.name.lower() or "unit" in p.name.lower()]
    if len(preferred) == 1:
        return preferred[0]
    return None


@dataclass
class RegistrationUnitSelection:
    registration_unit_id: str
    producer_family: str
    manifest_row_index: int
    manifest_row: Dict[str, str]
    resolved_sqlite_path: Optional[Path]
    resolution_status: str
    resolution_message: str


def resolve_registration_units(manifest_rows: List[Dict[str, str]], repo_root: Path) -> List[RegistrationUnitSelection]:
    selections: List[RegistrationUnitSelection] = []
    for idx, row in enumerate(manifest_rows, start=1):
        reg_id = resolve_registration_unit_id(row, idx)
        producer = resolve_producer_family(row, reg_id)
        resolved: Optional[Path] = None
        messages: List[str] = []
        for candidate in path_candidates_from_row(row):
            existing = resolve_existing_path(candidate, repo_root)
            if existing is None:
                continue
            sqlite_path = find_sqlite_under(existing)
            if sqlite_path is not None:
                resolved = sqlite_path
                messages.append(f"resolved from manifest value: {candidate}")
                break
        if resolved is None:
            status = "unresolved"
            msg = "No unambiguous SQLite database path could be resolved from manifest row."
        else:
            status = "resolved"
            msg = "; ".join(messages) or "resolved"
        selections.append(
            RegistrationUnitSelection(
                registration_unit_id=reg_id,
                producer_family=producer,
                manifest_row_index=idx,
                manifest_row=row,
                resolved_sqlite_path=resolved,
                resolution_status=status,
                resolution_message=msg,
            )
        )
    return selections


def sqlite_condition_for_group(group: Dict[str, Any], columns: Sequence[str]) -> Tuple[str, List[Any]]:
    conditions: List[str] = []
    params: List[Any] = []
    for col in ("assertion_registration_id", "identity_kind", "participant_role", "source_namespace"):
        if col not in columns:
            continue
        val = group.get(col)
        if val is None or val == "":
            conditions.append(f"({quote_ident(col)} IS NULL OR {quote_ident(col)} = '')")
        else:
            conditions.append(f"{quote_ident(col)} = ?")
            params.append(val)
    return (" AND ".join(conditions) if conditions else "1 = 1"), params


def source_identity_summary(conn: sqlite3.Connection) -> Tuple[List[Dict[str, Any]], str]:
    table = "source_identities"
    if not table_exists(conn, table):
        return [], "source_identities table unavailable"
    columns = table_columns(conn, table)
    required = ["assertion_registration_id", "identity_kind", "participant_role", "source_namespace"]
    available = [c for c in required if c in columns]
    if not available:
        return [], "source_identities table lacks summary grouping columns"
    group_by = ", ".join(quote_ident(c) for c in available)
    select_expr = ", ".join(quote_ident(c) for c in available)
    query = (
        f"SELECT {select_expr}, COUNT(*) AS source_identity_count "
        f"FROM {quote_ident(table)} GROUP BY {group_by} ORDER BY {group_by}"
    )
    rows = [row_to_dict(row) for row in conn.execute(query)]
    for row in rows:
        for col in required:
            row.setdefault(col, "")
    return rows, "resolved"


def source_identity_slice(conn: sqlite3.Connection, summary_rows: Sequence[Dict[str, Any]], k: int) -> List[Dict[str, Any]]:
    table = "source_identities"
    if not table_exists(conn, table):
        return []
    columns = table_columns(conn, table)
    order_col = "source_identity_id" if "source_identity_id" in columns else "rowid"
    order_expr = quote_ident(order_col) if order_col != "rowid" else "rowid"
    selected: Dict[str, Dict[str, Any]] = {}
    for group in summary_rows:
        where, params = sqlite_condition_for_group(group, columns)
        for direction in ("ASC", "DESC"):
            query = (
                f"SELECT * FROM {quote_ident(table)} WHERE {where} "
                f"ORDER BY {order_expr} {direction} LIMIT ?"
            )
            for row in conn.execute(query, params + [k]):
                record = row_to_dict(row)
                key = json.dumps(record, sort_keys=True, default=str)
                selected[key] = record
    return list(selected.values())


def source_identity_set_candidates(summary_rows: Sequence[Dict[str, Any]], registration_unit_id: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for idx, row in enumerate(summary_rows, start=1):
        assertion_registration_id = row.get("assertion_registration_id", "")
        rows.append(
            {
                "source_identity_set_candidate_id": f"{registration_unit_id}|source_identity_set|{idx:06d}",
                "registration_unit_id": registration_unit_id,
                "source_assertion_registration_id": assertion_registration_id,
                "source_identity_table_reference": f"{registration_unit_id}:source_identities",
                "source_identity_filter": f"assertion_registration_id={assertion_registration_id}",
                "identity_kind": row.get("identity_kind", ""),
                "participant_role": row.get("participant_role", ""),
                "source_namespace": row.get("source_namespace", ""),
                "source_identity_count": row.get("source_identity_count", ""),
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "validation_status": "not_evaluated",
            }
        )
    return rows


def has_variant_signal(row: Dict[str, Any]) -> bool:
    haystack = " ".join(
        str(row.get(k, "")) for k in ("identity_kind", "participant_role", "source_namespace", "source_label")
    ).lower()
    return "variant" in haystack or "vcf" in haystack


def detect_noncoding_status(columns: Sequence[str], sample_rows: Sequence[Dict[str, Any]]) -> Tuple[str, str]:
    explicit_cols = [
        c for c in columns
        if any(token in c.lower() for token in ("coding", "noncoding", "consequence", "region", "feature", "biotype"))
    ]
    if not explicit_cols:
        return "not_detectable_from_source_identity_table", "no explicit noncoding/consequence/region columns detected"
    noncoding_tokens = ("noncoding", "non_coding", "intron", "intergenic", "utr", "promoter", "enhancer", "regulatory")
    for row in sample_rows:
        haystack = " ".join(str(row.get(c, "")) for c in explicit_cols).lower()
        if any(token in haystack for token in noncoding_tokens):
            return "explicitly_detected", f"token detected in columns: {','.join(explicit_cols)}"
    return "not_detectable_from_source_identity_table", f"explicit columns present but no noncoding token in sampled rows: {','.join(explicit_cols)}"


def add_registration_unit_id(rows: Sequence[Dict[str, Any]], registration_unit_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        record = {"registration_unit_id": registration_unit_id}
        record.update(row)
        out.append(record)
    return out


def extraction_readme(fixture_name: str, timestamp: str) -> str:
    return f"""# Phase 4.3 Assertion Record Golden Fixture Candidate

**Fixture candidate:** `{fixture_name}`

**Generated:** `{timestamp}`

This package is a MARK-derived candidate acquisition package for the Phase 4.3
Assertion Record Layer 2 golden fixture.

It is not a production Assertion Record Index.

It is not a Phase 4.3 certification receipt.

It is not Evidence Topology, Convergence Geometry, an Evidence Convergence
Surface, a Projection View, or RDGP reasoning.

The package should be retrieved to sys76, checksum-verified, inspected, curated,
and then staged strategically under a committed fixture target such as:

```text
tests/fixtures/phase4/assertion_records/{fixture_name}/
```

The purpose of this candidate package is to preserve compressed real-world
Registration Unit substrate sufficient to test compact Assertion Record claim
preservation and lossless source identity recoverability.
"""


def expected_placeholder_rows() -> List[Dict[str, str]]:
    return [
        {"expected_artifact": name, "status": "placeholder_pending_builder_review"}
        for name in [
            "expected_assertion_record_index.tsv",
            "expected_assertion_record_index.jsonl",
            "expected_assertion_record_source_identity_sets.tsv",
            "expected_assertion_record_source_identity_summary.tsv",
            "expected_assertion_record_participants.tsv",
            "expected_assertion_record_relationships.tsv",
            "expected_assertion_record_evidence_basis.tsv",
            "expected_assertion_record_context.tsv",
            "expected_assertion_record_lineage.tsv",
            "expected_assertion_record_payload_references.tsv",
            "expected_downstream_topology_input_manifest.tsv",
            "expected_validation_summary.json",
        ]
    ]


def build_file_manifest(root: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    checksum_file = root / "checksums" / "file_manifest.sha256"
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path == checksum_file:
            continue
        rel = path.relative_to(root)
        rows.append({"sha256": sha256_file(path), "relative_path": str(rel), "size_bytes": str(path.stat().st_size)})
    return rows


def write_file_manifest(root: Path) -> None:
    rows = build_file_manifest(root)
    checksum_dir = root / "checksums"
    checksum_dir.mkdir(parents=True, exist_ok=True)
    with (checksum_dir / "file_manifest.sha256").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(f"{row['sha256']}  {row['relative_path']}\n")


def tar_directory(source_dir: Path, archive_path: Path) -> None:
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(source_dir, arcname=source_dir.name)


def write_archive_checksum(archive_path: Path) -> Path:
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(f"{sha256_file(archive_path)}  {archive_path.name}\n", encoding="utf-8")
    return checksum_path


def copy_manifest_slice(input_manifest: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_manifest, output_path)


def process_registration_unit(
    selection: RegistrationUnitSelection,
    output_dir: Path,
    k: int,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    reg_id = selection.registration_unit_id
    unit_dir = output_dir / "registration_units" / reg_id
    unit_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "registration_unit_id": reg_id,
        "producer_family": selection.producer_family,
        "sqlite_path": str(selection.resolved_sqlite_path) if selection.resolved_sqlite_path else "",
        "resolution_status": selection.resolution_status,
        "resolution_message": selection.resolution_message,
        "opened_read_only": False,
        "mutation_status": "not_evaluated",
        "assertion_registration_count": 0,
        "source_identity_count_total": 0,
        "source_identity_summary_row_count": 0,
        "source_identity_slice_row_count": 0,
        "artifact_count": 0,
        "tep_package_count": 0,
        "schema_metadata_count": 0,
        "variant_identity_rows_detected": 0,
        "noncoding_detection_status": "not_evaluated",
        "noncoding_detection_message": "not_evaluated",
        "status": "not_evaluated",
    }
    recoverability_rows: List[Dict[str, Any]] = []
    anti_flattening_rows: List[Dict[str, Any]] = []
    contract_rows: List[Dict[str, Any]] = []

    def add_contract(check: str, status: str, message: str) -> None:
        contract_rows.append(
            {
                "registration_unit_id": reg_id,
                "producer_family": selection.producer_family,
                "check_name": check,
                "check_status": status,
                "message": message,
            }
        )

    if not selection.resolved_sqlite_path:
        summary["status"] = "failed_unresolved_sqlite"
        add_contract("sqlite_resolved", "failed", selection.resolution_message)
        for table in TABLES_TO_SLICE:
            write_tsv(unit_dir / f"{table}.slice.tsv", [], ["status"])
        return summary, recoverability_rows, anti_flattening_rows, contract_rows

    before_sidecars = snapshot_sidecars([selection.resolved_sqlite_path])
    try:
        conn = sqlite_connect_readonly(selection.resolved_sqlite_path)
        summary["opened_read_only"] = True
        add_contract("sqlite_opened_read_only", "passed", "SQLite opened with mode=ro and PRAGMA query_only=ON")
    except Exception as exc:
        summary["status"] = "failed_sqlite_open"
        add_contract("sqlite_opened_read_only", "failed", str(exc))
        return summary, recoverability_rows, anti_flattening_rows, contract_rows

    try:
        for table in ("assertion_registrations", "artifacts", "tep_packages", "schema_metadata"):
            if table_exists(conn, table):
                rows = select_all_rows(conn, table)
                write_tsv(unit_dir / f"{table}.slice.tsv", add_registration_unit_id(rows, reg_id))
                summary_key = {
                    "assertion_registrations": "assertion_registration_count",
                    "artifacts": "artifact_count",
                    "tep_packages": "tep_package_count",
                    "schema_metadata": "schema_metadata_count",
                }[table]
                summary[summary_key] = len(rows)
                add_contract(f"{table}_present", "passed", f"{len(rows)} rows extracted")
            else:
                write_tsv(unit_dir / f"{table}.slice.tsv", [], ["registration_unit_id", "status"])
                add_contract(f"{table}_present", "warning", "table unavailable")

        if table_exists(conn, "source_identities"):
            total_source_identities = count_rows(conn, "source_identities")
            summary["source_identity_count_total"] = total_source_identities
            sid_summary, _sid_status = source_identity_summary(conn)
            summary["source_identity_summary_row_count"] = len(sid_summary)
            sid_slice = source_identity_slice(conn, sid_summary, k=k)
            summary["source_identity_slice_row_count"] = len(sid_slice)
            sid_candidates = source_identity_set_candidates(sid_summary, reg_id)
            sid_cols = table_columns(conn, "source_identities")
            variant_rows = [r for r in sid_summary if has_variant_signal(r)]
            summary["variant_identity_rows_detected"] = len(variant_rows)
            nc_status, nc_message = detect_noncoding_status(sid_cols, sid_slice)
            summary["noncoding_detection_status"] = nc_status
            summary["noncoding_detection_message"] = nc_message

            write_tsv(unit_dir / "source_identity_summary.tsv", add_registration_unit_id(sid_summary, reg_id))
            write_tsv(unit_dir / "source_identity_set_candidates.tsv", sid_candidates)
            write_tsv(unit_dir / "source_identities.slice.tsv", add_registration_unit_id(sid_slice, reg_id))

            add_contract("source_identities_present", "passed", f"{total_source_identities} total source identities")
            add_contract("source_identity_summary_emitted", "passed", f"{len(sid_summary)} summary rows")
            add_contract("source_identity_set_candidates_emitted", "passed", f"{len(sid_candidates)} set candidate rows")
            add_contract("source_identity_slice_emitted", "passed", f"{len(sid_slice)} deterministic slice rows")

            for row in sid_summary:
                rec = {"registration_unit_id": reg_id, "producer_family": selection.producer_family}
                rec.update(row)
                rec["recoverability_status"] = "lossless_by_reference"
                rec["source_identity_filter"] = f"assertion_registration_id={row.get('assertion_registration_id', '')}"
                recoverability_rows.append(rec)

            anti_flattening_rows.append(
                {
                    "registration_unit_id": reg_id,
                    "producer_family": selection.producer_family,
                    "source_identity_total_count": total_source_identities,
                    "source_identity_summary_row_count": len(sid_summary),
                    "source_identity_slice_row_count": len(sid_slice),
                    "variant_identity_summary_rows": len(variant_rows),
                    "noncoding_detection_status": nc_status,
                    "noncoding_detection_message": nc_message,
                    "anti_flattening_status": "passed" if len(sid_candidates) > 0 else "warning",
                    "message": "source identity set candidates emitted; full source identity universe represented by reconstructable filters",
                }
            )
        else:
            write_tsv(unit_dir / "source_identities.slice.tsv", [], ["registration_unit_id", "status"])
            write_tsv(unit_dir / "source_identity_summary.tsv", [], ["registration_unit_id", "status"])
            write_tsv(unit_dir / "source_identity_set_candidates.tsv", [], ["registration_unit_id", "status"])
            add_contract("source_identities_present", "failed", "source_identities table unavailable")
            anti_flattening_rows.append(
                {
                    "registration_unit_id": reg_id,
                    "producer_family": selection.producer_family,
                    "anti_flattening_status": "failed",
                    "message": "source_identities table unavailable",
                }
            )

        after_sidecars = snapshot_sidecars([selection.resolved_sqlite_path])
        before_set = set(before_sidecars.get(str(selection.resolved_sqlite_path), []))
        after_set = set(after_sidecars.get(str(selection.resolved_sqlite_path), []))
        created = sorted(after_set - before_set)
        summary["mutation_status"] = "passed" if not created else "failed_sidecars_created"
        summary["sidecars_created"] = ";".join(created)
        add_contract("registration_unit_not_mutated", "passed" if not created else "failed", "no new SQLite sidecars" if not created else ";".join(created))
        summary["status"] = "passed" if summary["mutation_status"] == "passed" else "passed_with_note"
    finally:
        conn.close()

    return summary, recoverability_rows, anti_flattening_rows, contract_rows


def build_fixture(args: argparse.Namespace) -> int:
    repo_root = Path.cwd().resolve()
    input_manifest = Path(args.input_manifest)
    input_manifest = (repo_root / input_manifest).resolve() if not input_manifest.is_absolute() else input_manifest.resolve()
    if not input_manifest.exists():
        raise SystemExit(f"Missing input manifest: {input_manifest}")

    timestamp = utc_timestamp_for_name()
    fixture_name = f"{args.fixture_prefix}_{timestamp}"
    output_root = Path(args.output_root)
    candidate_dir = output_root / fixture_name
    if candidate_dir.exists():
        raise SystemExit(f"Output directory already exists: {candidate_dir}")
    candidate_dir.mkdir(parents=True, exist_ok=False)

    manifest_rows = read_tsv(input_manifest)
    selections = resolve_registration_units(manifest_rows, repo_root)

    copy_manifest_slice(input_manifest, candidate_dir / "input" / "downstream_assertion_record_input_manifest.slice.tsv")
    selected_rows = []
    for sel in selections:
        selected_rows.append(
            {
                "registration_unit_id": sel.registration_unit_id,
                "producer_family": sel.producer_family,
                "manifest_row_index": sel.manifest_row_index,
                "resolved_sqlite_path": str(sel.resolved_sqlite_path) if sel.resolved_sqlite_path else "",
                "resolution_status": sel.resolution_status,
                "resolution_message": sel.resolution_message,
            }
        )
    write_tsv(candidate_dir / "input" / "selected_registration_units.tsv", selected_rows)

    all_summaries: List[Dict[str, Any]] = []
    all_recoverability: List[Dict[str, Any]] = []
    all_anti_flattening: List[Dict[str, Any]] = []
    all_contract: List[Dict[str, Any]] = []

    selected_ids = {s.registration_unit_id for s in selections}
    for expected_unit in REQUIRED_UNITS:
        if expected_unit not in selected_ids:
            all_contract.append(
                {
                    "registration_unit_id": expected_unit,
                    "producer_family": "not_resolved",
                    "check_name": "required_registration_unit_present",
                    "check_status": "warning",
                    "message": "Required canonical Registration Unit was not present in input manifest or could not be resolved by ID.",
                }
            )

    for sel in selections:
        summary, recoverability, anti_flattening, contract = process_registration_unit(sel, candidate_dir, k=args.k)
        all_summaries.append(summary)
        all_recoverability.extend(recoverability)
        all_anti_flattening.extend(anti_flattening)
        all_contract.extend(contract)

    summary_obj = {
        "fixture_id": DEFAULT_FIXTURE_ID,
        "fixture_name": fixture_name,
        "contract_id": DEFAULT_CONTRACT_ID,
        "source_corpus_generation_id": DEFAULT_CORPUS_GENERATION_ID,
        "builder_name": BUILDER_NAME,
        "builder_version": BUILDER_VERSION,
        "generated_at_utc": utc_iso(),
        "repo_root": str(repo_root),
        "input_manifest": str(input_manifest),
        "candidate_dir": str(candidate_dir),
        "selected_registration_unit_count": len(selections),
        "registration_unit_summaries": all_summaries,
        "layer_role": "Layer 2 fixture acquisition package; extracted on MARK, curated and run on sys76",
        "creates_assertion_records": False,
        "runs_layer2_validation": False,
        "runs_layer3_validation": False,
        "derives_topology": False,
        "emits_projection_views": False,
        "performs_rdgp_reasoning": False,
    }
    write_json(candidate_dir / "extraction_summary.json", summary_obj)
    write_tsv(candidate_dir / "extraction_summary.tsv", all_summaries)

    manifest_obj = {
        "fixture_id": DEFAULT_FIXTURE_ID,
        "fixture_name": fixture_name,
        "contract_id": DEFAULT_CONTRACT_ID,
        "source_corpus_generation_id": DEFAULT_CORPUS_GENERATION_ID,
        "input_manifest": str(input_manifest),
        "generated_at_utc": utc_iso(),
        "output_policy": "MARK writes candidate package to /root/Desktop; sys76 curates and commits",
        "committed_fixture_target_recommended": f"tests/fixtures/phase4/assertion_records/{fixture_name}/",
    }
    write_json(candidate_dir / "extraction_manifest.json", manifest_obj)
    write_tsv(candidate_dir / "extraction_manifest.tsv", [{k: v for k, v in manifest_obj.items()}])

    write_tsv(candidate_dir / "validation" / "source_identity_recoverability_summary.tsv", all_recoverability)
    write_tsv(candidate_dir / "validation" / "anti_flattening_coverage_summary.tsv", all_anti_flattening)
    write_tsv(candidate_dir / "validation" / "contract_alignment_summary.tsv", all_contract)
    write_json(candidate_dir / "validation" / "contract_alignment_summary.json", all_contract)
    write_tsv(candidate_dir / "expected" / "expected_output_placeholder_manifest.tsv", expected_placeholder_rows())

    limitations = [
        "# Fixture Limitations",
        "",
        "This is a MARK-derived candidate package for a compressed Layer 2 golden fixture.",
        "It does not contain full production-scale source_identity tables.",
        "It preserves source identity recoverability through deterministic slices, summaries, and set candidate filters.",
        "Expected Assertion Record output snapshots are placeholders until the builder emits draft outputs and DEX review accepts them.",
        "The package does not create production Assertion Records, derive topology, emit projections, or perform RDGP reasoning.",
        "",
    ]
    unresolved = [s for s in all_summaries if str(s.get("status", "")).startswith("failed")]
    if unresolved:
        limitations.append("## Failed Or Unresolved Registration Units")
        limitations.append("")
        for row in unresolved:
            limitations.append(f"- `{row.get('registration_unit_id')}`: {row.get('resolution_message')}")
    (candidate_dir / "fixture_limitations.md").write_text("\n".join(limitations) + "\n", encoding="utf-8")
    (candidate_dir / "README.md").write_text(extraction_readme(fixture_name, timestamp), encoding="utf-8")

    write_file_manifest(candidate_dir)

    archive_path = output_root / f"{fixture_name}.tgz"
    tar_directory(candidate_dir, archive_path)
    checksum_path = write_archive_checksum(archive_path)

    print(f"Candidate fixture directory: {candidate_dir}")
    print(f"Candidate fixture archive:   {archive_path}")
    print(f"Archive checksum:            {checksum_path}")
    print("Retrieve the .tgz and .tgz.sha256 to sys76 for curation and git tracking.")
    return 0


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-manifest",
        default=str(DEFAULT_INPUT_MANIFEST),
        help="Path to downstream_assertion_record_input_manifest.tsv relative to repo root or absolute.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Directory where MARK candidate fixture package and TGZ are written.",
    )
    parser.add_argument(
        "--fixture-prefix",
        default=DEFAULT_FIXTURE_PREFIX,
        help="Prefix for timestamped candidate fixture directory name.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="Rows selected from the beginning and end of each source identity group.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.k < 1:
        raise SystemExit("--k must be >= 1")
    return build_fixture(args)


if __name__ == "__main__":
    raise SystemExit(main())

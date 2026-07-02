#!/usr/bin/env python3
"""Phase 4.3E MARK full-corpus Assertion Record smoketest.

Layer 3 validation script for the canonical six-unit MARK corpus.

Prime Directive
---------------
Do not mutate input folders or input files. This script treats the Phase 4.2
Corpus Generation output and all Registration Unit SQLite databases as
read-only input substrate. It writes only to the configured Phase 4.3 Assertion
Record output directory, the validation receipt directory, and the MARK Desktop
retrieval bundle.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tarfile
from datetime import datetime
from typing import Any, Iterable

REPO_ROOT = Path.cwd().resolve()
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from variant_database.phase4.assertion_records.builder import build_assertion_records  # noqa: E402

DEFAULT_CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"
DEFAULT_MANIFEST = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/"
    "downstream_assertion_record_input_manifest.tsv"
)
DEFAULT_BUILD_OUTPUT = Path("results/phase4/assertion_records/mark_phase4_corpus_6tep_v1")
DEFAULT_VALIDATION_ROOT = Path("results/validation/phase4_assertion_records")
DEFAULT_DESKTOP_ROOT = Path("/root/Desktop")

EXPECTED_REGISTRATION_UNITS = 6
EXPECTED_ASSERTIONS = 52
EXPECTED_VAP_ASSERTIONS = 40
EXPECTED_GSC_ASSERTIONS = 12
EXPECTED_SOURCE_IDENTITY_TOTAL = 147_941_196
EXPECTED_SOURCE_IDENTITY_SET_GROUPS = 204
EXPECTED_RESOLVER_STATUS_COUNTS = {
    "supported": 26,
    "indexed_with_note": 14,
    "deferred": 12,
}
EXPECTED_SOURCE_IDENTITY_SET_STATUS_COUNTS = {
    "required": 34,
    "optional": 16,
    "not_applicable": 2,
}

MANIFEST_PATH_COLUMNS = (
    "registration_unit_sqlite_path",
    "sqlite_path",
    "sqlite_db_path",
    "registration_unit_db_path",
    "registration_unit_path",
)
GOVERNED_OUTPUTS = [
    "assertion_record_index.tsv",
    "assertion_record_index.jsonl",
    "assertion_record_participants.tsv",
    "assertion_record_relationships.tsv",
    "assertion_record_evidence_basis.tsv",
    "assertion_record_context.tsv",
    "assertion_record_lineage.tsv",
    "assertion_record_payload_references.tsv",
    "assertion_record_source_identity_sets.tsv",
    "assertion_record_source_identity_summary.tsv",
    "assertion_record_validation_report.tsv",
    "assertion_record_validation_report.json",
    "downstream_topology_input_manifest.tsv",
]
PROHIBITED_OUTPUT_TOKENS = (
    "geometry",
    "surface",
    "projection",
    "rdgp",
    "clinical_actionability",
    "causality",
)
ALLOWED_TOPOLOGY_OUTPUT = "downstream_topology_input_manifest.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: to_cell(row.get(key, "")) for key in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def file_line_count(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def tsv_data_row_count(path: Path) -> int:
    lines = file_line_count(path)
    return max(0, lines - 1)


def int_cell(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return default


def dir_size_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    total = 0
    for file_path in path.rglob("*"):
        if file_path.is_file():
            total += file_path.stat().st_size
    return total


def require_repo_root() -> None:
    expected = REPO_ROOT / "src" / "variant_database" / "phase4" / "assertion_records"
    if not expected.exists():
        raise SystemExit(
            "This script must be run from the VDB repo root. "
            f"Expected to find {expected.relative_to(REPO_ROOT) if expected.is_absolute() else expected}."
        )


def resolve_existing_path(raw_value: str, *, manifest_path: Path) -> Path:
    value = (raw_value or "").strip()
    if not value:
        raise ValueError("empty path value")
    path = Path(value)
    candidates: list[Path]
    if path.is_absolute():
        candidates = [path]
    else:
        candidates = [REPO_ROOT / path, manifest_path.parent / path, path]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved
    return candidates[0].resolve()


def resolve_registration_unit_path(row: dict[str, str], *, manifest_path: Path) -> Path:
    for column in MANIFEST_PATH_COLUMNS:
        value = (row.get(column) or "").strip()
        if value:
            return resolve_existing_path(value, manifest_path=manifest_path)
    raise ValueError(
        "manifest row lacks a Registration Unit SQLite path. "
        f"Checked columns: {', '.join(MANIFEST_PATH_COLUMNS)}"
    )


def connect_read_only(sqlite_path: Path) -> sqlite3.Connection:
    if not sqlite_path.exists():
        raise FileNotFoundError(f"Registration Unit SQLite database not found: {sqlite_path}")
    conn = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def snapshot_input_tree(root: Path) -> dict[str, dict[str, Any]]:
    snapshot: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return snapshot
    for path in sorted(root.rglob("*")):
        if path.is_file():
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            rel = str(path.relative_to(root))
            snapshot[rel] = {
                "size_bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
    return snapshot


def compare_snapshots(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    before_keys = set(before)
    after_keys = set(after)
    for rel in sorted(before_keys - after_keys):
        rows.append({"relative_path": rel, "status": "deleted", "before": before[rel], "after": ""})
    for rel in sorted(after_keys - before_keys):
        rows.append({"relative_path": rel, "status": "created", "before": "", "after": after[rel]})
    for rel in sorted(before_keys & after_keys):
        if before[rel] != after[rel]:
            rows.append({"relative_path": rel, "status": "modified", "before": before[rel], "after": after[rel]})
    return rows


def snapshot_inputs(input_roots: list[Path]) -> dict[str, dict[str, dict[str, Any]]]:
    snapshots: dict[str, dict[str, dict[str, Any]]] = {}
    for root in input_roots:
        snapshots[str(root)] = snapshot_input_tree(root)
    return snapshots


def compare_input_snapshots(
    before: dict[str, dict[str, dict[str, Any]]],
    after: dict[str, dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in sorted(set(before) | set(after)):
        for diff in compare_snapshots(before.get(root, {}), after.get(root, {})):
            rows.append(
                {
                    "input_root": root,
                    "relative_path": diff["relative_path"],
                    "status": diff["status"],
                    "before": diff["before"],
                    "after": diff["after"],
                }
            )
    return rows


def parse_manifest(manifest_path: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    rows = read_tsv(manifest_path)
    resolved_rows: list[dict[str, Any]] = []
    for row in rows:
        registration_unit_id = (row.get("registration_unit_id") or "").strip()
        producer_family = (row.get("producer_family") or "").strip().upper()
        sqlite_path = resolve_registration_unit_path(row, manifest_path=manifest_path)
        if not registration_unit_id:
            raise ValueError("manifest row missing registration_unit_id")
        if not producer_family:
            raise ValueError(f"manifest row for {registration_unit_id} missing producer_family")
        if not sqlite_path.exists():
            raise FileNotFoundError(f"resolved Registration Unit path does not exist: {sqlite_path}")
        resolved_rows.append(
            {
                "registration_unit_id": registration_unit_id,
                "producer_family": producer_family,
                "sqlite_path": str(sqlite_path),
            }
        )
    return rows, resolved_rows


def inspect_registration_units(resolved_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    unit_reports: list[dict[str, Any]] = []
    assertion_type_rows: list[dict[str, Any]] = []
    for row in resolved_rows:
        registration_unit_id = row["registration_unit_id"]
        producer_family = row["producer_family"]
        sqlite_path = Path(row["sqlite_path"])
        with connect_read_only(sqlite_path) as conn:
            has_assertions = table_exists(conn, "assertion_registrations")
            has_source_identities = table_exists(conn, "source_identities")
            assertion_count = 0
            if has_assertions:
                assertion_count = int(conn.execute("SELECT COUNT(*) FROM assertion_registrations").fetchone()[0])
                for item in conn.execute(
                    """
                    SELECT producer_family, assertion_type, COUNT(*) AS assertion_count
                    FROM assertion_registrations
                    GROUP BY producer_family, assertion_type
                    ORDER BY producer_family, assertion_type
                    """
                ).fetchall():
                    assertion_type_rows.append(
                        {
                            "registration_unit_id": registration_unit_id,
                            "producer_family": str(item["producer_family"] or producer_family).upper(),
                            "assertion_type": item["assertion_type"],
                            "input_assertion_count": int(item["assertion_count"]),
                        }
                    )
        unit_reports.append(
            {
                "registration_unit_id": registration_unit_id,
                "producer_family": producer_family,
                "sqlite_path": str(sqlite_path),
                "sqlite_size_bytes": sqlite_path.stat().st_size,
                "has_assertion_registrations": has_assertions,
                "has_source_identities": has_source_identities,
                "assertion_count": assertion_count,
            }
        )
    return unit_reports, assertion_type_rows


def output_file_manifest(output_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(output_dir))
        row_count = ""
        if path.suffix == ".tsv":
            row_count = tsv_data_row_count(path)
        elif path.suffix == ".jsonl":
            row_count = file_line_count(path)
        rows.append(
            {
                "relative_path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "row_count": row_count,
            }
        )
    return rows


def validate_governed_outputs(output_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name in GOVERNED_OUTPUTS:
        path = output_dir / name
        rows.append(
            {
                "output_name": name,
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "status": "passed" if path.exists() else "failed",
            }
        )
    return rows


def load_output_tables(output_dir: Path) -> dict[str, list[dict[str, str]]]:
    tables: dict[str, list[dict[str, str]]] = {}
    for name in [
        "assertion_record_index.tsv",
        "assertion_record_participants.tsv",
        "assertion_record_source_identity_sets.tsv",
        "assertion_record_source_identity_summary.tsv",
        "assertion_record_validation_report.tsv",
        "assertion_record_lineage.tsv",
        "downstream_topology_input_manifest.tsv",
    ]:
        path = output_dir / name
        tables[name] = read_tsv(path) if path.exists() else []
    return tables


def count_by(rows: list[dict[str, str]], *fields: str) -> dict[tuple[str, ...], int]:
    counts: dict[tuple[str, ...], int] = {}
    for row in rows:
        key = tuple(row.get(field, "") for field in fields)
        counts[key] = counts.get(key, 0) + 1
    return counts


def reconcile_counts(
    *,
    unit_reports: list[dict[str, Any]],
    output_tables: dict[str, list[dict[str, str]]],
) -> list[dict[str, Any]]:
    index_rows = output_tables["assertion_record_index.tsv"]
    source_sets = output_tables["assertion_record_source_identity_sets.tsv"]
    source_summary = output_tables["assertion_record_source_identity_summary.tsv"]
    downstream = output_tables["downstream_topology_input_manifest.tsv"]

    input_assertions = sum(int(row["assertion_count"]) for row in unit_reports)
    input_vap = sum(int(row["assertion_count"]) for row in unit_reports if row["producer_family"] == "VAP")
    input_gsc = sum(int(row["assertion_count"]) for row in unit_reports if row["producer_family"] == "GSC")
    output_vap = sum(1 for row in index_rows if row.get("producer_family") == "VAP")
    output_gsc = sum(1 for row in index_rows if row.get("producer_family") == "GSC")
    source_total = sum(int_cell(row.get("source_identity_count")) for row in source_summary)

    checks = [
        ("registration_unit_count", EXPECTED_REGISTRATION_UNITS, len(unit_reports)),
        ("input_assertion_count", EXPECTED_ASSERTIONS, input_assertions),
        ("output_assertion_record_count", input_assertions, len(index_rows)),
        ("vap_assertion_count", EXPECTED_VAP_ASSERTIONS, output_vap),
        ("gsc_assertion_count", EXPECTED_GSC_ASSERTIONS, output_gsc),
        ("downstream_topology_manifest_count", len(index_rows), len(downstream)),
        ("source_identity_set_group_count", EXPECTED_SOURCE_IDENTITY_SET_GROUPS, len(source_sets)),
        ("source_identity_summary_group_count", EXPECTED_SOURCE_IDENTITY_SET_GROUPS, len(source_summary)),
        ("source_identity_total_count", EXPECTED_SOURCE_IDENTITY_TOTAL, source_total),
    ]
    rows: list[dict[str, Any]] = []
    for check_name, expected, observed in checks:
        rows.append(
            {
                "check_name": check_name,
                "expected": expected,
                "observed": observed,
                "status": "passed" if expected == observed else "failed",
            }
        )
    rows.append(
        {
            "check_name": "input_vap_assertion_count",
            "expected": EXPECTED_VAP_ASSERTIONS,
            "observed": input_vap,
            "status": "passed" if input_vap == EXPECTED_VAP_ASSERTIONS else "failed",
        }
    )
    rows.append(
        {
            "check_name": "input_gsc_assertion_count",
            "expected": EXPECTED_GSC_ASSERTIONS,
            "observed": input_gsc,
            "status": "passed" if input_gsc == EXPECTED_GSC_ASSERTIONS else "failed",
        }
    )
    return rows


def reconcile_assertion_types(
    input_assertion_types: list[dict[str, Any]],
    index_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    output_counts = count_by(index_rows, "registration_unit_id", "producer_family", "assertion_type")
    rows: list[dict[str, Any]] = []
    for input_row in input_assertion_types:
        key = (
            input_row["registration_unit_id"],
            input_row["producer_family"],
            input_row["assertion_type"],
        )
        observed = output_counts.get(key, 0)
        expected = int(input_row["input_assertion_count"])
        rows.append(
            {
                **input_row,
                "output_assertion_count": observed,
                "status": "passed" if expected == observed else "failed",
            }
        )
    return rows


def reconcile_source_identities(output_tables: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    set_rows = output_tables["assertion_record_source_identity_sets.tsv"]
    summary_rows = output_tables["assertion_record_source_identity_summary.tsv"]
    summary_counts = {
        (
            row.get("assertion_id", ""),
            row.get("source_assertion_registration_id", ""),
            row.get("identity_kind", ""),
            row.get("participant_role", ""),
            row.get("source_namespace", ""),
        ): int_cell(row.get("source_identity_count"))
        for row in summary_rows
    }
    rows: list[dict[str, Any]] = []
    for row in set_rows:
        key = (
            row.get("assertion_id", ""),
            row.get("source_assertion_registration_id", ""),
            row.get("identity_kind", ""),
            row.get("participant_role", ""),
            row.get("source_namespace", ""),
        )
        set_count = int_cell(row.get("source_identity_count"))
        summary_count = summary_counts.get(key)
        filter_value = row.get("source_identity_filter", "")
        required_parts = [
            "assertion_registration_id=",
            "identity_kind=",
            "participant_role=",
            "source_namespace=",
        ]
        filter_ok = all(part in filter_value for part in required_parts)
        rows.append(
            {
                "assertion_id": row.get("assertion_id", ""),
                "source_assertion_registration_id": row.get("source_assertion_registration_id", ""),
                "identity_kind": row.get("identity_kind", ""),
                "participant_role": row.get("participant_role", ""),
                "source_namespace": row.get("source_namespace", ""),
                "set_count": set_count,
                "summary_count": summary_count if summary_count is not None else "missing",
                "partition_specific_filter": filter_ok,
                "status": "passed" if summary_count == set_count and filter_ok else "failed",
            }
        )
    return rows


def _counter_text(counter: Counter[str]) -> str:
    return ";".join(f"{key}={counter[key]}" for key in sorted(counter))


def validate_preservation_hardening(output_tables: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    """Validate MARK-scale preservation hardening invariants.

    These checks encode the Phase 4.3E recon findings. They deliberately fail if
    Assertion Record output regresses to header-only participants, orphaned
    source identity references, ambiguous preservation/resolver status, or
    under-specified lineage.
    """
    index_rows = output_tables["assertion_record_index.tsv"]
    participant_rows = output_tables["assertion_record_participants.tsv"]
    set_rows = output_tables["assertion_record_source_identity_sets.tsv"]
    summary_rows = output_tables["assertion_record_source_identity_summary.tsv"]
    lineage_rows = output_tables["assertion_record_lineage.tsv"]

    rows: list[dict[str, Any]] = []

    set_ids = {row.get("source_identity_set_id", "") for row in set_rows if row.get("source_identity_set_id", "")}
    participant_set_ids = {
        row.get("source_identity_set_id", "") for row in participant_rows if row.get("source_identity_set_id", "")
    }
    summary_set_ids = {
        row.get("source_identity_set_id", "") for row in summary_rows if row.get("source_identity_set_id", "")
    }

    participant_sources = Counter(row.get("participant_source", "") for row in participant_rows)
    participant_failures = 0
    participant_failure_details: list[str] = []
    if len(participant_rows) != EXPECTED_SOURCE_IDENTITY_SET_GROUPS:
        participant_failures += 1
        participant_failure_details.append(f"participant_rows={len(participant_rows)}")
    if set_rows and not participant_rows:
        participant_failures += 1
        participant_failure_details.append("source identity sets exist but participants are empty")
    if participant_rows and len(participant_set_ids) != len(participant_rows):
        participant_failures += 1
        participant_failure_details.append("some participant rows lack source_identity_set_id")
    if participant_rows and set(participant_sources) != {"source_identity_set_reference"}:
        participant_failures += 1
        participant_failure_details.append(f"participant_sources={_counter_text(participant_sources)}")
    rows.append(
        {
            "check_name": "participant_bridge_populated_from_source_identity_sets",
            "expected": (
                f"{EXPECTED_SOURCE_IDENTITY_SET_GROUPS} participant rows; "
                "all participants use source_identity_set_reference and carry source_identity_set_id"
            ),
            "observed": (
                f"participants={len(participant_rows)}; source_identity_sets={len(set_rows)}; "
                f"participant_sources={_counter_text(participant_sources)}"
            ),
            "status": "passed" if participant_failures == 0 else "failed",
            "detail": "; ".join(participant_failure_details),
        }
    )

    participant_missing = sorted(participant_set_ids - set_ids)
    participant_unreferenced_sets = sorted(set_ids - participant_set_ids)
    summary_missing = sorted(summary_set_ids - set_ids)
    summary_unreferenced_sets = sorted(set_ids - summary_set_ids)
    join_failures = 0
    join_details: list[str] = []
    if len(set_ids) != len(set_rows):
        join_failures += 1
        join_details.append("source identity set IDs are missing or non-unique")
    if participant_missing:
        join_failures += 1
        join_details.append(f"participant_missing={len(participant_missing)}")
    if participant_unreferenced_sets:
        join_failures += 1
        join_details.append(f"participant_unreferenced_sets={len(participant_unreferenced_sets)}")
    if summary_missing:
        join_failures += 1
        join_details.append(f"summary_missing={len(summary_missing)}")
    if summary_unreferenced_sets:
        join_failures += 1
        join_details.append(f"summary_unreferenced_sets={len(summary_unreferenced_sets)}")
    rows.append(
        {
            "check_name": "source_identity_set_id_join_integrity",
            "expected": "source_identity_set_id values are unique and join across source sets, participants, and summaries",
            "observed": (
                f"set_ids={len(set_ids)}; participant_set_ids={len(participant_set_ids)}; "
                f"summary_set_ids={len(summary_set_ids)}"
            ),
            "status": "passed" if join_failures == 0 and bool(set_ids) else "failed",
            "detail": "; ".join(join_details[:8]),
        }
    )

    preservation_counts = Counter(row.get("preservation_status", "") for row in index_rows)
    resolver_counts = Counter(row.get("resolver_status", "") for row in index_rows)
    validation_counts = Counter(row.get("validation_status", "") for row in index_rows)
    status_failures = 0
    status_details: list[str] = []
    if len(index_rows) != EXPECTED_ASSERTIONS:
        status_failures += 1
        status_details.append(f"index_rows={len(index_rows)}")
    if preservation_counts != Counter({"preserved": EXPECTED_ASSERTIONS}):
        status_failures += 1
        status_details.append(f"preservation_counts={_counter_text(preservation_counts)}")
    if resolver_counts != Counter(EXPECTED_RESOLVER_STATUS_COUNTS):
        status_failures += 1
        status_details.append(f"resolver_counts={_counter_text(resolver_counts)}")
    if any(not value for value in validation_counts):
        status_failures += 1
        status_details.append(f"validation_counts={_counter_text(validation_counts)}")
    rows.append(
        {
            "check_name": "preservation_and_resolver_status_are_explicit",
            "expected": (
                f"preservation_status=preserved for {EXPECTED_ASSERTIONS}; "
                f"resolver counts={EXPECTED_RESOLVER_STATUS_COUNTS}"
            ),
            "observed": (
                f"preservation_counts={_counter_text(preservation_counts)}; "
                f"resolver_counts={_counter_text(resolver_counts)}"
            ),
            "status": "passed" if status_failures == 0 else "failed",
            "detail": "; ".join(status_details),
        }
    )

    required_lineage_columns = [
        "source_artifact_relative_path",
        "source_artifact_sha256",
        "source_artifact_size_bytes",
        "source_record_ref_status",
        "lineage_completeness_status",
    ]
    lineage_status_counts = Counter(row.get("lineage_completeness_status", "") for row in lineage_rows)
    row_ref_status_counts = Counter(row.get("source_record_ref_status", "") for row in lineage_rows)
    missing_lineage_columns: list[str] = []
    if lineage_rows:
        missing_lineage_columns = [column for column in required_lineage_columns if column not in lineage_rows[0]]
    else:
        missing_lineage_columns = required_lineage_columns.copy()
    lineage_failures = 0
    lineage_details: list[str] = []
    if len(lineage_rows) != EXPECTED_ASSERTIONS:
        lineage_failures += 1
        lineage_details.append(f"lineage_rows={len(lineage_rows)}")
    if missing_lineage_columns:
        lineage_failures += 1
        lineage_details.append(f"missing_columns={','.join(missing_lineage_columns)}")
    for column in required_lineage_columns:
        if any(not row.get(column, "") for row in lineage_rows):
            lineage_failures += 1
            lineage_details.append(f"blank_{column}")
            break
    if lineage_status_counts != Counter({"artifact_level_lineage_present_row_ref_absent": EXPECTED_ASSERTIONS}):
        lineage_failures += 1
        lineage_details.append(f"lineage_status_counts={_counter_text(lineage_status_counts)}")
    if row_ref_status_counts != Counter({"explicit_absence": EXPECTED_ASSERTIONS}):
        lineage_failures += 1
        lineage_details.append(f"row_ref_status_counts={_counter_text(row_ref_status_counts)}")
    rows.append(
        {
            "check_name": "artifact_level_lineage_is_explicit",
            "expected": (
                "artifact-level provenance fields present; "
                f"lineage_completeness_status=artifact_level_lineage_present_row_ref_absent for {EXPECTED_ASSERTIONS}; "
                f"source_record_ref_status=explicit_absence for {EXPECTED_ASSERTIONS}"
            ),
            "observed": (
                f"lineage_rows={len(lineage_rows)}; lineage_status_counts={_counter_text(lineage_status_counts)}; "
                f"row_ref_status_counts={_counter_text(row_ref_status_counts)}"
            ),
            "status": "passed" if lineage_failures == 0 else "failed",
            "detail": "; ".join(lineage_details),
        }
    )

    source_obligation_counts = Counter(row.get("source_identity_set_status", "") for row in index_rows)
    obligation_failures = 0
    obligation_details: list[str] = []
    if source_obligation_counts != Counter(EXPECTED_SOURCE_IDENTITY_SET_STATUS_COUNTS):
        obligation_failures += 1
        obligation_details.append(f"source_identity_set_status_counts={_counter_text(source_obligation_counts)}")
    not_applicable_assertions = sorted(
        {
            row.get("producer_family", "") + ":" + row.get("assertion_type", "")
            for row in index_rows
            if row.get("source_identity_set_status", "") == "not_applicable"
        }
    )
    if not_applicable_assertions != ["GSC:producer_contract_validation"]:
        obligation_failures += 1
        obligation_details.append(f"not_applicable_assertions={','.join(not_applicable_assertions)}")
    rows.append(
        {
            "check_name": "source_identity_obligation_status_is_explicit",
            "expected": f"source identity obligation counts={EXPECTED_SOURCE_IDENTITY_SET_STATUS_COUNTS}; not_applicable only GSC:producer_contract_validation",
            "observed": f"source_identity_set_status_counts={_counter_text(source_obligation_counts)}; not_applicable={','.join(not_applicable_assertions)}",
            "status": "passed" if obligation_failures == 0 else "failed",
            "detail": "; ".join(obligation_details),
        }
    )

    return rows


def bundle_report_payload(
    *,
    bundle_path: Path,
    sha_path: Path,
    retrieval_mode: str,
    include_build_output: bool,
) -> dict[str, Any]:
    """Return non-self-referential retrieval bundle metadata.

    The authoritative archive checksum is the external .tgz.sha256 sidecar. The
    receipt inside the archive must not claim a final checksum for the archive
    that contains it.
    """
    return {
        "bundle_path": str(bundle_path),
        "bundle_sha256_path": str(sha_path),
        "bundle_sha256_sidecar_name": sha_path.name,
        "bundle_checksum_authority": "external_sidecar",
        "internal_archive_sha256_claim": False,
        "retrieval_mode": retrieval_mode,
        "full_build_output_included_in_bundle": include_build_output,
    }


def bundle_report_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"key": key, "value": value} for key, value in sorted(payload.items())]


def non_goal_report(output_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(output_dir))
        lower = rel.lower()
        status = "passed"
        message = "no prohibited output token detected"
        if "topology" in lower and rel != ALLOWED_TOPOLOGY_OUTPUT:
            status = "failed"
            message = "unexpected topology-like output"
        for token in PROHIBITED_OUTPUT_TOKENS:
            if token in lower:
                status = "failed"
                message = f"unexpected prohibited output token: {token}"
        if lower.endswith("source_identities.tsv") or "raw_source_identit" in lower:
            status = "failed"
            message = "raw source identity output detected"
        rows.append({"relative_path": rel, "status": status, "message": message})

    validation_json = output_dir / "assertion_record_validation_report.json"
    if validation_json.exists():
        payload = json.loads(validation_json.read_text(encoding="utf-8"))
        non_goals = payload.get("non_goals", {})
        for key, value in sorted(non_goals.items()):
            rows.append(
                {
                    "relative_path": "assertion_record_validation_report.json",
                    "status": "passed" if value is False else "failed",
                    "message": f"non_goals.{key}={value}",
                }
            )
    return rows


def create_previews(output_dir: Path, preview_dir: Path, *, n: int = 25) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    preview_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(output_dir.rglob("*")):
        if not source.is_file():
            continue
        rel = source.relative_to(output_dir)
        target_base = preview_dir / rel
        target_base.parent.mkdir(parents=True, exist_ok=True)
        head_path = target_base.with_suffix(target_base.suffix + ".head.txt")
        tail_path = target_base.with_suffix(target_base.suffix + ".tail.txt")
        try:
            lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception as exc:  # pragma: no cover - defensive MARK path
            rows.append({"relative_path": str(rel), "status": "skipped", "message": str(exc)})
            continue
        head_path.write_text("\n".join(lines[:n]) + ("\n" if lines[:n] else ""), encoding="utf-8")
        tail_path.write_text("\n".join(lines[-n:]) + ("\n" if lines[-n:] else ""), encoding="utf-8")
        rows.append(
            {
                "relative_path": str(rel),
                "line_count": len(lines),
                "head_preview": str(head_path.relative_to(preview_dir)),
                "tail_preview": str(tail_path.relative_to(preview_dir)),
                "status": "created",
            }
        )
    return rows


def add_check(checks: list[dict[str, Any]], name: str, status: str, message: str, detail: Any = "") -> None:
    checks.append({"check_name": name, "status": status, "message": message, "detail": detail})


def summarize_checks(checks: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for check in checks:
        counts[check["status"]] = counts.get(check["status"], 0) + 1
    overall = "passed" if counts.get("failed", 0) == 0 else "failed"
    return {"overall_status": overall, "status_counts": counts, "checks": checks}


def make_bundle(
    *,
    timestamp: str,
    desktop_root: Path,
    receipt_dir: Path,
    build_output: Path,
    retrieval_mode: str,
    include_build_output: bool,
) -> tuple[Path, Path, str]:
    desktop_root.mkdir(parents=True, exist_ok=True)
    bundle_path = desktop_root / f"phase4_3_mark_full_corpus_assertion_record_smoketest_{timestamp}.tgz"
    sha_path = desktop_root / f"{bundle_path.name}.sha256"
    if bundle_path.exists():
        bundle_path.unlink()
    if sha_path.exists():
        sha_path.unlink()
    with tarfile.open(bundle_path, "w:gz") as tar:
        tar.add(receipt_dir, arcname=str(receipt_dir.relative_to(REPO_ROOT)))
        if include_build_output and build_output.exists():
            tar.add(build_output, arcname=str(build_output.relative_to(REPO_ROOT)))
    digest = sha256_file(bundle_path)
    sha_path.write_text(f"{digest}  {bundle_path.name}\n", encoding="utf-8")
    return bundle_path, sha_path, digest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Phase 4.3E MARK full-corpus Assertion Record smoketest.",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--corpus-generation-id", default=DEFAULT_CORPUS_GENERATION_ID)
    parser.add_argument("--build-output", type=Path, default=DEFAULT_BUILD_OUTPUT)
    parser.add_argument("--validation-root", type=Path, default=DEFAULT_VALIDATION_ROOT)
    parser.add_argument("--desktop-root", type=Path, default=DEFAULT_DESKTOP_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-bundle-mb", type=float, default=100.0)
    parser.add_argument("--overwrite-output", action="store_true")
    parser.add_argument("--repeat-build", action="store_true")
    parser.add_argument("--preview-lines", type=int, default=25)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_repo_root()

    timestamp = args.timestamp or datetime.now().strftime("%Y_%m_%d_%H%M%S")
    manifest_path = (REPO_ROOT / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest.resolve()
    build_output = (REPO_ROOT / args.build_output).resolve() if not args.build_output.is_absolute() else args.build_output.resolve()
    validation_root = (REPO_ROOT / args.validation_root).resolve() if not args.validation_root.is_absolute() else args.validation_root.resolve()
    receipt_dir = validation_root / f"mark_full_corpus_smoketest_{timestamp}"
    receipt_dir.mkdir(parents=True, exist_ok=False)

    checks: list[dict[str, Any]] = []
    exit_code = 0

    try:
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest not found: {manifest_path}")
        if build_output.exists():
            if args.overwrite_output:
                shutil.rmtree(build_output)
            else:
                raise FileExistsError(
                    f"build output already exists: {build_output}. "
                    "Use --overwrite-output only for an intentional rerun."
                )

        manifest_rows, resolved_rows = parse_manifest(manifest_path)
        unit_reports, input_assertion_type_rows = inspect_registration_units(resolved_rows)
        input_roots = sorted({manifest_path.parent.resolve(), *(Path(row["sqlite_path"]).parent.resolve() for row in resolved_rows)})
        input_snapshot_before = snapshot_inputs(input_roots)

        write_tsv(
            receipt_dir / "input_manifest_report.tsv",
            resolved_rows,
            ["registration_unit_id", "producer_family", "sqlite_path"],
        )
        write_tsv(
            receipt_dir / "registration_unit_input_report.tsv",
            unit_reports,
            [
                "registration_unit_id",
                "producer_family",
                "sqlite_path",
                "sqlite_size_bytes",
                "has_assertion_registrations",
                "has_source_identities",
                "assertion_count",
            ],
        )
        write_tsv(
            receipt_dir / "input_assertion_type_report.tsv",
            input_assertion_type_rows,
            ["registration_unit_id", "producer_family", "assertion_type", "input_assertion_count"],
        )

        add_check(checks, "manifest_exists", "passed", f"manifest found: {manifest_path}")
        add_check(
            checks,
            "six_registration_units_declared",
            "passed" if len(resolved_rows) == EXPECTED_REGISTRATION_UNITS else "failed",
            f"found {len(resolved_rows)} manifest rows",
        )
        missing_tables = [row for row in unit_reports if not row["has_assertion_registrations"] or not row["has_source_identities"]]
        add_check(
            checks,
            "required_registration_unit_tables_present",
            "passed" if not missing_tables else "failed",
            f"missing required table reports: {len(missing_tables)}",
            missing_tables,
        )

        build_result = build_assertion_records(
            manifest_path=manifest_path,
            output_dir=build_output,
            corpus_generation_id=args.corpus_generation_id,
        )
        add_check(checks, "builder_completed", "passed", f"builder emitted {build_result.assertion_count} Assertion Records")

        repeat_report: list[dict[str, Any]] = []
        if args.repeat_build:
            repeat_output = receipt_dir / "repeat_build_output"
            repeat_result = build_assertion_records(
                manifest_path=manifest_path,
                output_dir=repeat_output,
                corpus_generation_id=args.corpus_generation_id,
            )
            for name in GOVERNED_OUTPUTS:
                a = build_output / name
                b = repeat_output / name
                a_hash = sha256_file(a) if a.exists() else "missing"
                b_hash = sha256_file(b) if b.exists() else "missing"
                repeat_report.append(
                    {
                        "output_name": name,
                        "run_a_sha256": a_hash,
                        "run_b_sha256": b_hash,
                        "status": "passed" if a_hash == b_hash else "failed",
                    }
                )
            add_check(
                checks,
                "repeat_build_determinism",
                "passed" if all(row["status"] == "passed" for row in repeat_report) else "failed",
                f"compared {len(repeat_report)} governed outputs using --repeat-build",
            )
            add_check(checks, "repeat_build_completed", "passed", f"repeat build emitted {repeat_result.assertion_count} Assertion Records")
        else:
            add_check(
                checks,
                "governed_output_hash_manifest_created",
                "passed",
                "single full-corpus build completed; --repeat-build not requested",
            )

        governed_report = validate_governed_outputs(build_output)
        write_tsv(receipt_dir / "governed_output_presence.tsv", governed_report, ["output_name", "exists", "size_bytes", "status"])
        add_check(
            checks,
            "governed_outputs_present",
            "passed" if all(row["status"] == "passed" for row in governed_report) else "failed",
            f"checked {len(governed_report)} governed outputs",
        )

        output_manifest = output_file_manifest(build_output)
        write_tsv(receipt_dir / "output_file_manifest.tsv", output_manifest, ["relative_path", "size_bytes", "sha256", "row_count"])

        output_tables = load_output_tables(build_output)
        count_rows = reconcile_counts(unit_reports=unit_reports, output_tables=output_tables)
        write_tsv(receipt_dir / "count_reconciliation.tsv", count_rows, ["check_name", "expected", "observed", "status"])
        add_check(
            checks,
            "count_reconciliation",
            "passed" if all(row["status"] == "passed" for row in count_rows) else "failed",
            f"checked {len(count_rows)} count invariants",
        )

        assertion_type_rows = reconcile_assertion_types(input_assertion_type_rows, output_tables["assertion_record_index.tsv"])
        write_tsv(
            receipt_dir / "assertion_type_reconciliation.tsv",
            assertion_type_rows,
            ["registration_unit_id", "producer_family", "assertion_type", "input_assertion_count", "output_assertion_count", "status"],
        )
        add_check(
            checks,
            "assertion_type_reconciliation",
            "passed" if all(row["status"] == "passed" for row in assertion_type_rows) else "failed",
            f"checked {len(assertion_type_rows)} assertion type groups",
        )

        source_rows = reconcile_source_identities(output_tables)
        write_tsv(
            receipt_dir / "source_identity_reconciliation.tsv",
            source_rows,
            [
                "assertion_id",
                "source_assertion_registration_id",
                "identity_kind",
                "participant_role",
                "source_namespace",
                "set_count",
                "summary_count",
                "partition_specific_filter",
                "status",
            ],
        )
        add_check(
            checks,
            "source_identity_set_reconciliation",
            "passed" if source_rows and all(row["status"] == "passed" for row in source_rows) else "failed",
            f"checked {len(source_rows)} source identity set groups",
        )

        preservation_rows = validate_preservation_hardening(output_tables)
        write_tsv(
            receipt_dir / "preservation_hardening_report.tsv",
            preservation_rows,
            ["check_name", "expected", "observed", "status", "detail"],
        )
        for row in preservation_rows:
            add_check(
                checks,
                row["check_name"],
                row["status"],
                row["observed"],
                row.get("detail", ""),
            )

        validation_rows = output_tables["assertion_record_validation_report.tsv"]
        status_accounted = len(output_tables["assertion_record_index.tsv"])
        add_check(
            checks,
            "no_silent_assertion_drops",
            "passed" if status_accounted == EXPECTED_ASSERTIONS else "failed",
            f"Assertion Record index contains {status_accounted} rows",
        )
        add_check(
            checks,
            "validation_report_nonempty",
            "passed" if len(validation_rows) > 0 else "failed",
            f"validation rows: {len(validation_rows)}",
        )

        non_goal_rows = non_goal_report(build_output)
        write_tsv(receipt_dir / "non_goals_report.tsv", non_goal_rows, ["relative_path", "status", "message"])
        add_check(
            checks,
            "non_goal_boundary_preserved",
            "passed" if all(row["status"] == "passed" for row in non_goal_rows) else "failed",
            f"non-goal checks: {len(non_goal_rows)}",
        )

        input_snapshot_after = snapshot_inputs(input_roots)
        mutation_rows = compare_input_snapshots(input_snapshot_before, input_snapshot_after)
        write_tsv(receipt_dir / "input_mutation_report.tsv", mutation_rows, ["input_root", "relative_path", "status", "before", "after"])
        add_check(
            checks,
            "prime_directive_input_files_not_mutated",
            "passed" if not mutation_rows else "failed",
            "input folders unchanged" if not mutation_rows else f"input mutations detected: {len(mutation_rows)}",
        )

        build_size = dir_size_bytes(build_output)
        receipt_size = dir_size_bytes(receipt_dir)
        max_bundle_bytes = int(args.max_bundle_mb * 1024 * 1024)
        include_build_output = build_size <= max_bundle_bytes
        retrieval_mode = "plan_a_full_output_bundle" if include_build_output else "plan_b_summary_bundle"

        preview_rows: list[dict[str, Any]] = []
        if not include_build_output:
            preview_rows = create_previews(build_output, receipt_dir / "output_previews", n=args.preview_lines)
            write_tsv(
                receipt_dir / "output_preview_manifest.tsv",
                preview_rows,
                ["relative_path", "line_count", "head_preview", "tail_preview", "status"],
            )

        retrieval_rows = [
            {
                "key": "retrieval_mode",
                "value": retrieval_mode,
            },
            {
                "key": "build_output_path",
                "value": str(build_output),
            },
            {
                "key": "validation_receipt_path",
                "value": str(receipt_dir),
            },
            {
                "key": "build_output_size_bytes",
                "value": build_size,
            },
            {
                "key": "validation_receipt_size_bytes_before_bundle",
                "value": receipt_size,
            },
            {
                "key": "max_bundle_bytes_for_full_output",
                "value": max_bundle_bytes,
            },
            {
                "key": "full_build_output_included_in_bundle",
                "value": include_build_output,
            },
        ]
        write_tsv(receipt_dir / "retrieval_manifest.tsv", retrieval_rows, ["key", "value"])
        write_json(
            receipt_dir / "retrieval_manifest.json",
            {
                "retrieval_mode": retrieval_mode,
                "build_output_path": str(build_output),
                "validation_receipt_path": str(receipt_dir),
                "build_output_size_bytes": build_size,
                "validation_receipt_size_bytes_before_bundle": receipt_size,
                "max_bundle_bytes_for_full_output": max_bundle_bytes,
                "full_build_output_included_in_bundle": include_build_output,
                "preview_manifest_rows": len(preview_rows),
            },
        )

        summary = summarize_checks(checks)
        write_tsv(receipt_dir / "validation_summary.tsv", checks, ["check_name", "status", "message", "detail"])
        write_json(
            receipt_dir / "validation_summary.json",
            {
                **summary,
                "corpus_generation_id": args.corpus_generation_id,
                "manifest_path": str(manifest_path),
                "build_output_path": str(build_output),
                "receipt_path": str(receipt_dir),
                "timestamp": timestamp,
            },
        )
        write_json(
            receipt_dir / "run_manifest.json",
            {
                "phase": "4.3E",
                "layer": "Layer 3 MARK full-corpus validation",
                "prime_directive": "Do not mutate input folders or input files.",
                "corpus_generation_id": args.corpus_generation_id,
                "manifest_path": str(manifest_path),
                "build_output_path": str(build_output),
                "receipt_path": str(receipt_dir),
                "registration_unit_count": len(resolved_rows),
                "expected_assertion_count": EXPECTED_ASSERTIONS,
                "expected_source_identity_total": EXPECTED_SOURCE_IDENTITY_TOTAL,
                "repeat_build": args.repeat_build,
                "retrieval_mode": retrieval_mode,
            },
        )
        (receipt_dir / "README.md").write_text(
            "# Phase 4.3E MARK Full-Corpus Assertion Record Smoketest\n\n"
            f"Status: {summary['overall_status']}\n\n"
            "This receipt records the Layer 3 MARK full-corpus Assertion Record smoketest.\n"
            "The script enforces the Prime Directive: input folders and input files must not be mutated.\n\n"
            f"Corpus Generation: `{args.corpus_generation_id}`\n\n"
            f"Build output: `{build_output}`\n\n"
            f"Retrieval mode: `{retrieval_mode}`\n",
            encoding="utf-8",
        )

        bundle_path, sha_path, bundle_sha = make_bundle(
            timestamp=timestamp,
            desktop_root=args.desktop_root,
            receipt_dir=receipt_dir,
            build_output=build_output,
            retrieval_mode=retrieval_mode,
            include_build_output=include_build_output,
        )
        bundle_rows = [
            {"key": "bundle_path", "value": str(bundle_path)},
            {"key": "bundle_sha256_path", "value": str(sha_path)},
            {"key": "bundle_sha256", "value": bundle_sha},
        ]
        write_tsv(receipt_dir / "bundle_report.tsv", bundle_rows, ["key", "value"])
        write_json(
            receipt_dir / "bundle_report.json",
            {"bundle_path": str(bundle_path), "bundle_sha256_path": str(sha_path), "bundle_sha256": bundle_sha},
        )

        # Recreate bundle once so bundle_report is included in the receipt inside the archive.
        bundle_path, sha_path, bundle_sha = make_bundle(
            timestamp=timestamp,
            desktop_root=args.desktop_root,
            receipt_dir=receipt_dir,
            build_output=build_output,
            retrieval_mode=retrieval_mode,
            include_build_output=include_build_output,
        )

        if summary["overall_status"] == "passed":
            print("Phase 4.3E MARK full-corpus smoketest PASSED")
            exit_code = 0
        else:
            print(
                f"Phase 4.3E MARK full-corpus smoketest FAILED: "
                f"{summary['status_counts'].get('failed', 0)} failed checks"
            )
            exit_code = 1
        print(f"Receipt: {receipt_dir}")
        print(f"Retrieval bundle: {bundle_path}")
        print(f"Bundle checksum: {sha_path}")
        return exit_code
    except Exception as exc:
        write_json(
            receipt_dir / "operator_error.json",
            {
                "status": "operator_error",
                "error_type": type(exc).__name__,
                "message": str(exc),
                "receipt_path": str(receipt_dir),
            },
        )
        print(f"Phase 4.3E MARK full-corpus smoketest OPERATOR ERROR: {exc}", file=sys.stderr)
        print(f"Receipt: {receipt_dir}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Phase 4.3D Layer 2 Assertion Record golden fixture smoketest.

This script is sys76-local. It consumes the committed compressed real-world
Phase 4.3 Assertion Record golden fixture, materializes temporary SQLite
Registration Units, runs the Assertion Record builder twice, and emits a
validation receipt. It does not run on MARK, does not consume the uncompressed
full corpus, does not write production Assertion Record corpus outputs, and does
not derive topology, geometry, surfaces, projections, or RDGP reasoning.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

DEFAULT_FIXTURE = Path(
    "tests/fixtures/phase4/assertion_records/"
    "phase4_3_assertion_record_golden_fixture_2026_07_01_203720"
)
DEFAULT_OUTPUT_ROOT = Path("results/validation/phase4_assertion_records")
DEFAULT_CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"
SMOKETEST_PREFIX = "golden_fixture_smoketest"

REQUIRED_UNIT_FILES = [
    "assertion_registrations.slice.tsv",
    "source_identities.slice.tsv",
    "source_identity_summary.tsv",
    "source_identity_set_candidates.tsv",
    "artifacts.slice.tsv",
    "tep_packages.slice.tsv",
    "schema_metadata.slice.tsv",
]

GOVERNED_BUILD_OUTPUTS = [
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

PROHIBITED_OUTPUT_TOKENS = [
    "convergence_geometry",
    "evidence_topology",
    "evidence_convergence_surface",
    "projection_view",
    "rdgp",
    "gene_rank",
    "variant_rank",
    "clinical_actionability",
    "causality",
]

SOURCE_IDENTITY_COLUMNS = [
    "source_identity_id",
    "assertion_registration_id",
    "identity_kind",
    "participant_role",
    "source_value",
    "source_namespace",
    "source_label",
    "extraction_method",
    "source_record_ref",
    "payload_json",
    "source_identity_count",
]


@dataclass(frozen=True)
class Check:
    check_name: str
    status: str
    message: str
    detail: str = ""


def _repo_root() -> Path:
    return Path.cwd().resolve()


def _ensure_import_path(repo_root: Path) -> None:
    src = repo_root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def _timestamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _write_tsv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _to_cell(row.get(key, "")) for key in fieldnames})


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _first_present(row: dict[str, Any], columns: Iterable[str], default: str = "") -> str:
    """Return the first non-empty value from a row using allowed schema aliases."""
    for column in columns:
        value = row.get(column)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return default


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_files(paths: Iterable[Path], root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(paths):
        if path.is_file():
            hashes[str(path.relative_to(root))] = _sha256_file(path)
    return hashes


def _parse_sha256_manifest(path: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    if not path.exists():
        return entries
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, rel = parts
        rel = rel.strip()
        if rel.startswith("*"):
            rel = rel[1:]
        entries.append((digest, Path(rel)))
    return entries


def _validate_checksum_manifest(fixture: Path) -> tuple[list[dict[str, str]], list[Check]]:
    rows: list[dict[str, str]] = []
    checks: list[Check] = []
    manifest = fixture / "checksums" / "file_manifest.sha256"
    entries = _parse_sha256_manifest(manifest)
    if not manifest.exists():
        checks.append(Check("fixture_checksum_manifest_present", "failed", "checksums/file_manifest.sha256 missing"))
        return rows, checks
    if not entries:
        checks.append(Check("fixture_checksum_manifest_parseable", "failed", "checksum manifest has no parseable entries"))
        return rows, checks

    failed = 0
    for expected, rel in entries:
        path = fixture / rel
        if not path.exists():
            rows.append({"path": str(rel), "expected_sha256": expected, "actual_sha256": "", "status": "missing"})
            failed += 1
            continue
        actual = _sha256_file(path)
        status = "passed" if actual == expected else "failed"
        if status != "passed":
            failed += 1
        rows.append({"path": str(rel), "expected_sha256": expected, "actual_sha256": actual, "status": status})
    checks.append(
        Check(
            "fixture_checksum_manifest_validates",
            "passed" if failed == 0 else "failed",
            f"validated {len(entries)} checksum entries with {failed} failures",
        )
    )
    return rows, checks


def _discover_registration_units(fixture: Path) -> list[Path]:
    root = fixture / "registration_units"
    if not root.exists():
        return []
    return sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name)


def _producer_family_from_assertions(unit_dir: Path) -> str:
    rows = _read_tsv(unit_dir / "assertion_registrations.slice.tsv")
    for row in rows:
        producer = (row.get("producer_family") or "").strip().upper()
        if producer:
            return producer
    return "UNKNOWN"


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _create_table(conn: sqlite3.Connection, table_name: str, columns: list[str]) -> None:
    col_defs = ", ".join(f"{_quote_identifier(col)} TEXT" for col in columns)
    conn.execute(f"CREATE TABLE {_quote_identifier(table_name)} ({col_defs})")


def _insert_rows(conn: sqlite3.Connection, table_name: str, columns: list[str], rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    placeholders = ", ".join("?" for _ in columns)
    quoted_cols = ", ".join(_quote_identifier(col) for col in columns)
    sql = f"INSERT INTO {_quote_identifier(table_name)} ({quoted_cols}) VALUES ({placeholders})"
    values = [[_to_cell(row.get(col, "")) for col in columns] for row in rows]
    conn.executemany(sql, values)


def _materialize_tsv_table(conn: sqlite3.Connection, table_name: str, path: Path) -> int:
    rows = _read_tsv(path)
    if rows:
        columns = list(rows[0].keys())
    else:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            columns = next(reader, [])
    _create_table(conn, table_name, columns)
    _insert_rows(conn, table_name, columns, rows)
    return len(rows)


def _source_identity_row_from_candidate(candidate: dict[str, str]) -> dict[str, str]:
    payload = {
        "source_identity_filter": candidate.get("source_identity_filter", ""),
        "source_identity_table_reference": candidate.get("source_identity_table_reference", ""),
        "lossiness_status": candidate.get("lossiness_status", ""),
        "resolution_status": candidate.get("resolution_status", ""),
        "validation_status": candidate.get("validation_status", ""),
        "source_identity_set_candidate_id": candidate.get("source_identity_set_candidate_id", ""),
    }
    return {
        "source_identity_id": candidate.get("source_identity_set_candidate_id", ""),
        "assertion_registration_id": candidate.get("source_assertion_registration_id", ""),
        "identity_kind": candidate.get("identity_kind", ""),
        "participant_role": candidate.get("participant_role", ""),
        "source_value": "__compressed_source_identity_set__",
        "source_namespace": candidate.get("source_namespace", ""),
        "source_label": "compressed source identity set candidate",
        "extraction_method": "phase4_3_layer2_fixture_materialization",
        "source_record_ref": candidate.get("source_identity_filter", ""),
        "payload_json": json.dumps(payload, sort_keys=True, separators=(",", ":")),
        "source_identity_count": candidate.get("source_identity_count", ""),
    }


def _materialize_source_identities(conn: sqlite3.Connection, path: Path) -> tuple[int, int]:
    candidates = _read_tsv(path)
    rows = [_source_identity_row_from_candidate(candidate) for candidate in candidates]
    _create_table(conn, "source_identities", SOURCE_IDENTITY_COLUMNS)
    _insert_rows(conn, "source_identities", SOURCE_IDENTITY_COLUMNS, rows)
    represented = 0
    for candidate in candidates:
        try:
            represented += int(candidate.get("source_identity_count", "0") or 0)
        except ValueError:
            pass
    return len(rows), represented


def _materialize_registration_units(
    *, fixture: Path, work_dir: Path, receipt_dir: Path
) -> tuple[Path, list[dict[str, Any]], list[Check]]:
    checks: list[Check] = []
    materialization_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    materialized_root = work_dir / "materialized_registration_units"
    materialized_root.mkdir(parents=True, exist_ok=True)

    for unit_dir in _discover_registration_units(fixture):
        registration_unit_id = unit_dir.name
        producer_family = _producer_family_from_assertions(unit_dir)
        sqlite_dir = materialized_root / registration_unit_id
        sqlite_dir.mkdir(parents=True, exist_ok=True)
        db_path = sqlite_dir / "vdb.sqlite"
        if db_path.exists():
            db_path.unlink()
        conn = sqlite3.connect(db_path)
        try:
            table_specs = [
                ("assertion_registrations", unit_dir / "assertion_registrations.slice.tsv"),
                ("artifacts", unit_dir / "artifacts.slice.tsv"),
                ("tep_packages", unit_dir / "tep_packages.slice.tsv"),
                ("schema_metadata", unit_dir / "schema_metadata.slice.tsv"),
            ]
            for table_name, path in table_specs:
                row_count = _materialize_tsv_table(conn, table_name, path)
                materialization_rows.append(
                    {
                        "registration_unit_id": registration_unit_id,
                        "producer_family": producer_family,
                        "table_name": table_name,
                        "materialization_source": str(path.relative_to(fixture)),
                        "materialized_row_count": row_count,
                        "represented_source_identity_count": "",
                        "status": "materialized",
                    }
                )
            compressed_rows, represented_count = _materialize_source_identities(
                conn, unit_dir / "source_identity_set_candidates.tsv"
            )
            materialization_rows.append(
                {
                    "registration_unit_id": registration_unit_id,
                    "producer_family": producer_family,
                    "table_name": "source_identities",
                    "materialization_source": str((unit_dir / "source_identity_set_candidates.tsv").relative_to(fixture)),
                    "materialized_row_count": compressed_rows,
                    "represented_source_identity_count": represented_count,
                    "status": "materialized_from_compressed_set_candidates",
                }
            )
            conn.commit()
        finally:
            conn.close()

        manifest_rows.append(
            {
                "registration_unit_id": registration_unit_id,
                "producer_family": producer_family,
                "registration_unit_sqlite_path": str(db_path.resolve()),
            }
        )

    manifest_path = receipt_dir / "materialized_manifest.tsv"
    _write_tsv(
        manifest_path,
        manifest_rows,
        ["registration_unit_id", "producer_family", "registration_unit_sqlite_path"],
    )
    checks.append(
        Check(
            "temporary_registration_units_materialized",
            "passed" if manifest_rows else "failed",
            f"materialized {len(manifest_rows)} temporary Registration Units",
        )
    )
    return manifest_path, materialization_rows, checks


def _validate_fixture_structure(fixture: Path) -> tuple[list[dict[str, str]], list[Check]]:
    rows: list[dict[str, str]] = []
    checks: list[Check] = []
    required_paths = [
        "README.md",
        "input/downstream_assertion_record_input_manifest.slice.tsv",
        "input/selected_registration_units.tsv",
        "registration_units",
        "validation/contract_alignment_summary.tsv",
        "validation/source_identity_recoverability_summary.tsv",
        "validation/source_identity_not_applicable_assertions.tsv",
        "validation/anti_flattening_coverage_summary.tsv",
        "checksums/file_manifest.sha256",
    ]
    missing = 0
    for rel in required_paths:
        path = fixture / rel
        status = "present" if path.exists() else "missing"
        if status == "missing":
            missing += 1
        rows.append({"path": rel, "status": status, "kind": "fixture_required_path"})
    checks.append(
        Check(
            "fixture_required_paths_present",
            "passed" if missing == 0 else "failed",
            f"checked {len(required_paths)} required fixture paths with {missing} missing",
        )
    )

    unit_dirs = _discover_registration_units(fixture)
    checks.append(
        Check(
            "six_registration_units_present",
            "passed" if len(unit_dirs) == 6 else "failed",
            f"found {len(unit_dirs)} registration unit directories",
        )
    )
    for unit_dir in unit_dirs:
        for file_name in REQUIRED_UNIT_FILES:
            path = unit_dir / file_name
            status = "present" if path.exists() else "missing"
            rows.append({"path": str(path.relative_to(fixture)), "status": status, "kind": "registration_unit_required_file"})
    missing_unit_files = sum(1 for row in rows if row["kind"] == "registration_unit_required_file" and row["status"] != "present")
    checks.append(
        Check(
            "registration_unit_slice_files_present",
            "passed" if missing_unit_files == 0 else "failed",
            f"required unit file missing count: {missing_unit_files}",
        )
    )
    return rows, checks


def _validate_fixture_curation(fixture: Path) -> tuple[list[dict[str, str]], list[Check]]:
    rows: list[dict[str, str]] = []
    checks: list[Check] = []

    partition_failures = 0
    candidate_count = 0
    for unit_dir in _discover_registration_units(fixture):
        path = unit_dir / "source_identity_set_candidates.tsv"
        for row in _read_tsv(path):
            candidate_count += 1
            filter_value = row.get("source_identity_filter", "")
            required_tokens = [
                "assertion_registration_id=",
                "identity_kind=",
                "participant_role=",
                "source_namespace=",
            ]
            status = "passed" if all(token in filter_value for token in required_tokens) else "failed"
            if status != "passed":
                partition_failures += 1
            rows.append(
                {
                    "registration_unit_id": unit_dir.name,
                    "check_name": "partition_specific_source_identity_filter",
                    "status": status,
                    "source_assertion_registration_id": row.get("source_assertion_registration_id", ""),
                    "detail": filter_value,
                }
            )
    checks.append(
        Check(
            "partition_specific_source_identity_filters",
            "passed" if candidate_count > 0 and partition_failures == 0 else "failed",
            f"checked {candidate_count} source identity set candidates with {partition_failures} failures",
        )
    )

    contract_path = fixture / "validation" / "contract_alignment_summary.tsv"
    contract_rows = _read_tsv(contract_path) if contract_path.exists() else []
    required_passed = []
    for row in contract_rows:
        check_name = _first_present(
            row,
            [
                "check_name",
                "check",
                "validation_check",
                "contract_check",
                "requirement",
                "obligation",
            ],
        )
        status = _first_present(row, ["status", "validation_status", "check_status"])
        if check_name == "required_registration_unit_present" and status == "passed":
            required_passed.append(row)
    checks.append(
        Check(
            "required_registration_unit_alias_checks_passed",
            "passed" if len(required_passed) == 6 else "failed",
            f"found {len(required_passed)} passed required_registration_unit_present rows",
        )
    )

    na_path = fixture / "validation" / "source_identity_not_applicable_assertions.tsv"
    na_rows = _read_tsv(na_path) if na_path.exists() else []
    checks.append(
        Check(
            "source_identity_not_applicable_rows_present",
            "passed" if len(na_rows) >= 2 else "failed",
            f"found {len(na_rows)} source identity not_applicable rows",
        )
    )
    return rows, checks


def _count_input_assertions(fixture: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    counts: dict[str, Any] = {
        "registration_units": 0,
        "assertion_registrations": 0,
        "producer_counts": {},
        "assertion_type_counts": {},
    }
    producer_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for unit_dir in _discover_registration_units(fixture):
        counts["registration_units"] += 1
        assertion_rows = _read_tsv(unit_dir / "assertion_registrations.slice.tsv")
        for row in assertion_rows:
            producer = (row.get("producer_family") or "UNKNOWN").upper()
            assertion_type = row.get("assertion_type") or "UNKNOWN"
            producer_counts[producer] = producer_counts.get(producer, 0) + 1
            type_key = f"{producer}:{assertion_type}"
            type_counts[type_key] = type_counts.get(type_key, 0) + 1
            counts["assertion_registrations"] += 1
        rows.append(
            {
                "registration_unit_id": unit_dir.name,
                "producer_family": _producer_family_from_assertions(unit_dir),
                "input_assertion_registration_count": len(assertion_rows),
            }
        )
    counts["producer_counts"] = producer_counts
    counts["assertion_type_counts"] = type_counts
    return rows, counts


def _validate_count_reconciliation(
    *, fixture: Path, run_dir: Path, input_counts: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[Check]]:
    rows: list[dict[str, Any]] = []
    checks: list[Check] = []
    index_rows = _read_tsv(run_dir / "assertion_record_index.tsv")
    validation_rows = _read_tsv(run_dir / "assertion_record_validation_report.tsv")
    producer_counts: dict[str, int] = {}
    for row in index_rows:
        producer = row.get("producer_family", "UNKNOWN")
        producer_counts[producer] = producer_counts.get(producer, 0) + 1

    comparisons = [
        ("registration_units", input_counts["registration_units"], len(_discover_registration_units(fixture))),
        ("assertion_registrations", input_counts["assertion_registrations"], len(index_rows)),
        ("VAP_assertions", input_counts["producer_counts"].get("VAP", 0), producer_counts.get("VAP", 0)),
        ("GSC_assertions", input_counts["producer_counts"].get("GSC", 0), producer_counts.get("GSC", 0)),
    ]
    failures = 0
    for name, expected, observed in comparisons:
        status = "passed" if expected == observed else "failed"
        if status != "passed":
            failures += 1
        rows.append({"check_name": name, "expected_count": expected, "observed_count": observed, "status": status})
    checks.append(
        Check(
            "assertion_count_reconciliation",
            "passed" if failures == 0 else "failed",
            f"checked assertion count reconciliation with {failures} failures",
        )
    )

    accounted_statuses = {"supported", "indexed_with_note", "deferred", "unsupported"}
    index_status_count = sum(1 for row in index_rows if row.get("validation_status") in accounted_statuses)
    rows.append(
        {
            "check_name": "no_silent_assertion_drops",
            "expected_count": input_counts["assertion_registrations"],
            "observed_count": index_status_count,
            "status": "passed" if index_status_count == input_counts["assertion_registrations"] else "failed",
        }
    )
    checks.append(
        Check(
            "no_silent_assertion_drops",
            "passed" if index_status_count == input_counts["assertion_registrations"] else "failed",
            f"accounted statuses in index: {index_status_count} of {input_counts['assertion_registrations']}",
        )
    )

    if not validation_rows:
        checks.append(Check("validation_report_nonempty", "failed", "assertion_record_validation_report.tsv has no rows"))
    else:
        checks.append(Check("validation_report_nonempty", "passed", f"validation rows: {len(validation_rows)}"))
    return rows, checks


def _validate_assertion_types(input_counts: dict[str, Any], run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    index_rows = _read_tsv(run_dir / "assertion_record_index.tsv")
    observed: dict[str, int] = {}
    for row in index_rows:
        key = f"{row.get('producer_family', 'UNKNOWN')}:{row.get('assertion_type', 'UNKNOWN')}"
        observed[key] = observed.get(key, 0) + 1
    rows: list[dict[str, Any]] = []
    failures = 0
    for key, expected in sorted(input_counts["assertion_type_counts"].items()):
        obs = observed.get(key, 0)
        status = "passed" if expected == obs else "failed"
        if status != "passed":
            failures += 1
        producer, assertion_type = key.split(":", 1)
        rows.append(
            {
                "producer_family": producer,
                "assertion_type": assertion_type,
                "expected_count": expected,
                "observed_count": obs,
                "status": status,
            }
        )
    return rows, [
        Check(
            "assertion_type_reconciliation",
            "passed" if failures == 0 else "failed",
            f"checked {len(rows)} producer/assertion_type groups with {failures} failures",
        )
    ]


def _fixture_source_identity_candidates(fixture: Path) -> dict[tuple[str, str, str, str, str], int]:
    expected: dict[tuple[str, str, str, str, str], int] = {}
    for unit_dir in _discover_registration_units(fixture):
        for row in _read_tsv(unit_dir / "source_identity_set_candidates.tsv"):
            key = (
                unit_dir.name,
                row.get("source_assertion_registration_id", ""),
                row.get("identity_kind", ""),
                row.get("participant_role", ""),
                row.get("source_namespace", ""),
            )
            try:
                count = int(row.get("source_identity_count", "0") or 0)
            except ValueError:
                count = 0
            expected[key] = count
    return expected


def _validate_source_identity_sets(fixture: Path, run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    expected = _fixture_source_identity_candidates(fixture)
    summary_rows = _read_tsv(run_dir / "assertion_record_source_identity_summary.tsv")
    observed: dict[tuple[str, str, str, str, str], int] = {}
    for row in summary_rows:
        key = (
            row.get("registration_unit_id", ""),
            row.get("source_assertion_registration_id", ""),
            row.get("identity_kind", ""),
            row.get("participant_role", ""),
            row.get("source_namespace", ""),
        )
        try:
            count = int(row.get("source_identity_count", "0") or 0)
        except ValueError:
            count = 0
        observed[key] = count

    rows: list[dict[str, Any]] = []
    failures = 0
    for key, expected_count in sorted(expected.items()):
        observed_count = observed.get(key)
        status = "passed" if observed_count == expected_count else "failed"
        if status != "passed":
            failures += 1
        rows.append(
            {
                "registration_unit_id": key[0],
                "source_assertion_registration_id": key[1],
                "identity_kind": key[2],
                "participant_role": key[3],
                "source_namespace": key[4],
                "expected_source_identity_count": expected_count,
                "observed_source_identity_count": "" if observed_count is None else observed_count,
                "status": status,
            }
        )
    extra = sorted(set(observed) - set(expected))
    for key in extra:
        failures += 1
        rows.append(
            {
                "registration_unit_id": key[0],
                "source_assertion_registration_id": key[1],
                "identity_kind": key[2],
                "participant_role": key[3],
                "source_namespace": key[4],
                "expected_source_identity_count": "",
                "observed_source_identity_count": observed[key],
                "status": "unexpected_observed_group",
            }
        )

    set_rows = _read_tsv(run_dir / "assertion_record_source_identity_sets.tsv")
    checks = [
        Check(
            "source_identity_set_reconciliation",
            "passed" if expected and failures == 0 else "failed",
            f"reconciled {len(expected)} expected source identity set groups with {failures} failures",
        ),
        Check(
            "source_identity_set_outputs_present",
            "passed" if set_rows and summary_rows else "failed",
            f"source identity set rows: {len(set_rows)}; summary rows: {len(summary_rows)}",
        ),
    ]
    return rows, checks


def _validate_source_identity_not_applicable(fixture: Path, run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    expected_rows = _read_tsv(fixture / "validation" / "source_identity_not_applicable_assertions.tsv")
    validation_rows = _read_tsv(run_dir / "assertion_record_validation_report.tsv")
    observed = {
        _first_present(row, ["source_assertion_registration_id", "assertion_registration_id"]): row
        for row in validation_rows
        if _first_present(row, ["source_identity_set_status", "source_identity_status"]) == "not_applicable"
    }
    rows: list[dict[str, Any]] = []
    failures = 0
    for expected in expected_rows:
        sid = _first_present(
            expected,
            [
                "source_assertion_registration_id",
                "assertion_registration_id",
                "source_assertion_key",
                "assertion_id",
            ],
        )
        obs = observed.get(sid)
        status = "passed" if sid and obs else "failed"
        if status != "passed":
            failures += 1
        rows.append(
            {
                "registration_unit_id": _first_present(expected, ["registration_unit_id"]),
                "producer_family": _first_present(expected, ["producer_family"]),
                "source_assertion_registration_id": sid,
                "assertion_type": _first_present(expected, ["assertion_type"]),
                "expected_source_identity_set_status": "not_applicable",
                "observed_source_identity_set_status": "" if obs is None else _first_present(obs, ["source_identity_set_status", "source_identity_status"]),
                "status": status,
            }
        )
    return rows, [
        Check(
            "source_identity_not_applicable_reconciliation",
            "passed" if failures == 0 and len(expected_rows) >= 2 else "failed",
            f"checked {len(expected_rows)} not_applicable assertions with {failures} failures",
        )
    ]



def _validate_preservation_hardening(run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    """Validate Phase 4.3 preservation hardening invariants.

    These checks encode the MARK input-substrate recon findings. They ensure that
    Layer 2 fails if the builder regresses to header-only participants, orphaned
    source identity references, ambiguous preservation/resolver status, or
    under-specified lineage.
    """
    rows: list[dict[str, Any]] = []
    checks: list[Check] = []

    index_rows = _read_tsv(run_dir / "assertion_record_index.tsv")
    participant_rows = _read_tsv(run_dir / "assertion_record_participants.tsv")
    set_rows = _read_tsv(run_dir / "assertion_record_source_identity_sets.tsv")
    summary_rows = _read_tsv(run_dir / "assertion_record_source_identity_summary.tsv")
    lineage_rows = _read_tsv(run_dir / "assertion_record_lineage.tsv")

    set_ids = {row.get("source_identity_set_id", "") for row in set_rows if row.get("source_identity_set_id", "")}
    participant_set_ids = {
        row.get("source_identity_set_id", "") for row in participant_rows if row.get("source_identity_set_id", "")
    }
    summary_set_ids = {
        row.get("source_identity_set_id", "") for row in summary_rows if row.get("source_identity_set_id", "")
    }

    participant_failures = 0
    if set_rows and not participant_rows:
        participant_failures += 1
    if participant_rows and len(participant_set_ids) != len(participant_rows):
        participant_failures += 1
    participant_sources = {row.get("participant_source", "") for row in participant_rows}
    if participant_rows and participant_sources != {"source_identity_set_reference"}:
        participant_failures += 1
    rows.append(
        {
            "check_name": "participant_bridge_populated_from_source_identity_sets",
            "expected": "participant rows > 0 when source identity sets exist; all participants use source_identity_set_reference",
            "observed": (
                f"participants={len(participant_rows)}; source_identity_sets={len(set_rows)}; "
                f"participant_sources={','.join(sorted(participant_sources))}"
            ),
            "status": "passed" if participant_failures == 0 else "failed",
            "detail": "",
        }
    )
    checks.append(
        Check(
            "participant_bridge_populated_from_source_identity_sets",
            "passed" if participant_failures == 0 else "failed",
            f"participant rows: {len(participant_rows)}; source identity set rows: {len(set_rows)}",
        )
    )

    participant_missing = sorted(participant_set_ids - set_ids)
    summary_missing = sorted(summary_set_ids - set_ids)
    join_failures = len(participant_missing) + len(summary_missing)
    if set_rows and len(summary_set_ids) != len(summary_rows):
        join_failures += 1
    rows.append(
        {
            "check_name": "source_identity_set_id_join_integrity",
            "expected": "participant and summary source_identity_set_id values join to assertion_record_source_identity_sets.tsv",
            "observed": (
                f"participant_missing={len(participant_missing)}; summary_missing={len(summary_missing)}; "
                f"set_ids={len(set_ids)}; participant_set_ids={len(participant_set_ids)}; summary_set_ids={len(summary_set_ids)}"
            ),
            "status": "passed" if join_failures == 0 and set_ids else "failed",
            "detail": ";".join(participant_missing[:5] + summary_missing[:5]),
        }
    )
    checks.append(
        Check(
            "source_identity_set_id_join_integrity",
            "passed" if join_failures == 0 and set_ids else "failed",
            f"participant missing joins: {len(participant_missing)}; summary missing joins: {len(summary_missing)}",
        )
    )

    preservation_values = [row.get("preservation_status", "") for row in index_rows]
    resolver_values = [row.get("resolver_status", "") for row in index_rows]
    validation_values = [row.get("validation_status", "") for row in index_rows]
    expected_resolver_values = {"supported", "indexed_with_note", "deferred", "unsupported"}
    status_failures = 0
    if not index_rows:
        status_failures += 1
    if any(value != "preserved" for value in preservation_values):
        status_failures += 1
    if any(value not in expected_resolver_values for value in resolver_values):
        status_failures += 1
    if any(not value for value in validation_values):
        status_failures += 1
    rows.append(
        {
            "check_name": "preservation_and_resolver_status_are_explicit",
            "expected": "all indexed records preservation_status=preserved and resolver_status is explicit",
            "observed": (
                f"index_rows={len(index_rows)}; preserved={preservation_values.count('preserved')}; "
                f"resolver_values={','.join(sorted(set(resolver_values)))}"
            ),
            "status": "passed" if status_failures == 0 else "failed",
            "detail": "",
        }
    )
    checks.append(
        Check(
            "preservation_and_resolver_status_are_explicit",
            "passed" if status_failures == 0 else "failed",
            f"preserved {preservation_values.count('preserved')} of {len(index_rows)} records; resolver statuses: {sorted(set(resolver_values))}",
        )
    )

    required_lineage_columns = [
        "source_artifact_relative_path",
        "source_artifact_sha256",
        "source_artifact_size_bytes",
        "source_record_ref_status",
        "lineage_completeness_status",
    ]
    lineage_failures = 0
    missing_columns: list[str] = []
    if lineage_rows:
        missing_columns = [col for col in required_lineage_columns if col not in lineage_rows[0]]
    else:
        lineage_failures += 1
    if missing_columns:
        lineage_failures += len(missing_columns)
    for row in lineage_rows:
        for col in required_lineage_columns:
            if not row.get(col, ""):
                lineage_failures += 1
                break
    lineage_status_values = {row.get("lineage_completeness_status", "") for row in lineage_rows}
    row_ref_status_values = {row.get("source_record_ref_status", "") for row in lineage_rows}
    rows.append(
        {
            "check_name": "artifact_level_lineage_is_explicit",
            "expected": "artifact provenance fields and explicit source_record_ref/lineage statuses are present for every lineage row",
            "observed": (
                f"lineage_rows={len(lineage_rows)}; missing_columns={','.join(missing_columns)}; "
                f"lineage_statuses={','.join(sorted(lineage_status_values))}; "
                f"source_record_ref_statuses={','.join(sorted(row_ref_status_values))}"
            ),
            "status": "passed" if lineage_failures == 0 else "failed",
            "detail": "",
        }
    )
    checks.append(
        Check(
            "artifact_level_lineage_is_explicit",
            "passed" if lineage_failures == 0 else "failed",
            f"lineage rows: {len(lineage_rows)}; lineage failures: {lineage_failures}",
        )
    )

    return rows, checks


def _validate_anti_flattening(fixture: Path, run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    rows: list[dict[str, Any]] = []
    checks: list[Check] = []
    represented_count = sum(_fixture_source_identity_candidates(fixture).values())
    physical_slice_count = 0
    for unit_dir in _discover_registration_units(fixture):
        physical_slice_count += len(_read_tsv(unit_dir / "source_identities.slice.tsv"))
    summary_rows = _read_tsv(run_dir / "assertion_record_source_identity_summary.tsv")
    participant_rows = _read_tsv(run_dir / "assertion_record_participants.tsv")
    rows.append(
        {
            "check_name": "represented_source_identity_universe_exceeds_physical_slice",
            "represented_source_identity_count": represented_count,
            "physical_source_identity_slice_rows": physical_slice_count,
            "source_identity_summary_rows": "",
            "participant_rows": "",
            "status": "passed" if represented_count > physical_slice_count else "failed",
        }
    )
    rows.append(
        {
            "check_name": "source_identity_sets_not_replaced_by_participants_only",
            "represented_source_identity_count": "",
            "physical_source_identity_slice_rows": "",
            "source_identity_summary_rows": len(summary_rows),
            "participant_rows": len(participant_rows),
            "status": "passed" if summary_rows else "failed",
        }
    )
    failures = sum(1 for row in rows if row.get("status") != "passed")
    checks.append(
        Check(
            "anti_flattening_checks",
            "passed" if failures == 0 else "failed",
            f"anti-flattening failures: {failures}",
        )
    )
    return rows, checks


def _hash_governed_outputs(run_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in GOVERNED_BUILD_OUTPUTS:
        path = run_dir / name
        hashes[name] = _sha256_file(path) if path.exists() else "MISSING"
    return hashes


def _validate_determinism(run_a: Path, run_b: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    hashes_a = _hash_governed_outputs(run_a)
    hashes_b = _hash_governed_outputs(run_b)
    rows: list[dict[str, Any]] = []
    failures = 0
    for name in GOVERNED_BUILD_OUTPUTS:
        status = "passed" if hashes_a.get(name) == hashes_b.get(name) and hashes_a.get(name) != "MISSING" else "failed"
        if status != "passed":
            failures += 1
        rows.append(
            {
                "output_file": name,
                "run_a_sha256": hashes_a.get(name, ""),
                "run_b_sha256": hashes_b.get(name, ""),
                "status": status,
            }
        )
    return rows, [
        Check(
            "deterministic_build_outputs",
            "passed" if failures == 0 else "failed",
            f"compared {len(GOVERNED_BUILD_OUTPUTS)} governed outputs with {failures} failures",
        )
    ]


def _validate_non_goals(run_dir: Path) -> tuple[list[dict[str, Any]], list[Check]]:
    rows: list[dict[str, Any]] = []
    failures = 0
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(run_dir))
        if rel == "downstream_topology_input_manifest.tsv":
            rows.append({"path": rel, "status": "allowed_handoff_manifest", "matched_token": "topology"})
            continue
        rel_lower = rel.lower()
        matched = [token for token in PROHIBITED_OUTPUT_TOKENS if token in rel_lower]
        status = "failed" if matched else "passed"
        if status != "passed":
            failures += 1
        rows.append({"path": rel, "status": status, "matched_token": ",".join(matched)})

    validation_json = run_dir / "assertion_record_validation_report.json"
    if validation_json.exists():
        payload = json.loads(validation_json.read_text(encoding="utf-8"))
        non_goals = payload.get("non_goals", {})
        for key, value in sorted(non_goals.items()):
            status = "passed" if value is False else "failed"
            if status != "passed":
                failures += 1
            rows.append({"path": f"assertion_record_validation_report.json:{key}", "status": status, "matched_token": str(value)})
    else:
        failures += 1
        rows.append({"path": "assertion_record_validation_report.json", "status": "failed", "matched_token": "missing"})

    return rows, [
        Check(
            "non_goal_boundary_preserved",
            "passed" if failures == 0 else "failed",
            f"non-goal failures: {failures}",
        )
    ]


def _write_validation_summary(receipt_dir: Path, checks: list[Check]) -> None:
    rows = [check.__dict__ for check in checks]
    _write_tsv(receipt_dir / "validation_summary.tsv", rows, ["check_name", "status", "message", "detail"])
    status_counts: dict[str, int] = {}
    for check in checks:
        status_counts[check.status] = status_counts.get(check.status, 0) + 1
    _write_json(
        receipt_dir / "validation_summary.json",
        {
            "overall_status": "passed" if all(check.status == "passed" for check in checks) else "failed",
            "status_counts": status_counts,
            "checks": rows,
        },
    )


def _write_readme(receipt_dir: Path, *, fixture: Path, corpus_generation_id: str) -> None:
    text = f"""# Phase 4.3D Assertion Record Golden Fixture Smoketest Receipt

This receipt was generated by:

```text
scripts/validation/run_phase4_3_golden_fixture_assertion_record_smoketest.py
```

Layer: Phase 4.3D — Layer 2 compressed golden fixture validation.

Fixture:

```text
{fixture}
```

Corpus Generation ID:

```text
{corpus_generation_id}
```

This receipt keeps both builder runs:

```text
build_outputs/run_a/
build_outputs/run_b/
```

The script materializes temporary SQLite Registration Units from the committed
compressed fixture and feeds those temporary databases to the Assertion Record
builder. Source identity set candidates are materialized as compressed set rows
with declared `source_identity_count` values so Layer 2 validates the compressed
real-world identity universe rather than only bounded example rows.

This receipt is not Layer 3 validation, not a production Assertion Record corpus,
and not Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces,
Projection Views, or RDGP reasoning.
"""
    (receipt_dir / "README.md").write_text(text, encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    repo_root = _repo_root()
    _ensure_import_path(repo_root)
    from variant_database.phase4.assertion_records.builder import build_assertion_records

    fixture = Path(args.fixture).resolve()
    output_root = Path(args.output_root)
    timestamp = args.timestamp or _timestamp()
    receipt_dir = (output_root / f"{SMOKETEST_PREFIX}_{timestamp}").resolve()
    receipt_dir.mkdir(parents=True, exist_ok=False)

    checks: list[Check] = []
    _write_json(
        receipt_dir / "run_manifest.json",
        {
            "script": "scripts/validation/run_phase4_3_golden_fixture_assertion_record_smoketest.py",
            "phase": "Phase 4.3D",
            "layer": "Layer 2 compressed golden fixture validation",
            "fixture": str(fixture),
            "output_root": str(Path(args.output_root).resolve()),
            "receipt_dir": str(receipt_dir),
            "corpus_generation_id": args.corpus_generation_id,
            "timestamp": timestamp,
            "keep_workdir": bool(args.keep_workdir),
            "keeps_run_a_and_run_b": True,
        },
    )
    _write_readme(receipt_dir, fixture=fixture, corpus_generation_id=args.corpus_generation_id)

    if not fixture.exists():
        checks.append(Check("fixture_directory_exists", "failed", f"fixture not found: {fixture}"))
        _write_validation_summary(receipt_dir, checks)
        return 2
    checks.append(Check("fixture_directory_exists", "passed", f"fixture found: {fixture}"))

    before_hashes = _hash_files(fixture.rglob("*"), fixture)

    checksum_rows, checksum_checks = _validate_checksum_manifest(fixture)
    checks.extend(checksum_checks)
    _write_tsv(
        receipt_dir / "fixture_integrity_report.tsv",
        checksum_rows,
        ["path", "expected_sha256", "actual_sha256", "status"],
    )

    structure_rows, structure_checks = _validate_fixture_structure(fixture)
    checks.extend(structure_checks)
    _write_tsv(receipt_dir / "fixture_structure_report.tsv", structure_rows, ["path", "status", "kind"])

    curation_rows, curation_checks = _validate_fixture_curation(fixture)
    checks.extend(curation_checks)
    _write_tsv(
        receipt_dir / "fixture_curation_report.tsv",
        curation_rows,
        ["registration_unit_id", "check_name", "status", "source_assertion_registration_id", "detail"],
    )

    input_rows, input_counts = _count_input_assertions(fixture)
    _write_tsv(
        receipt_dir / "fixture_input_assertion_counts.tsv",
        input_rows,
        ["registration_unit_id", "producer_family", "input_assertion_registration_count"],
    )

    build_root = receipt_dir / "build_outputs"
    run_a = build_root / "run_a"
    run_b = build_root / "run_b"
    work_parent = receipt_dir / "work"

    if args.keep_workdir:
        work_dir = work_parent
        work_dir.mkdir(parents=True, exist_ok=True)
        manifest_path, materialization_rows, materialization_checks = _materialize_registration_units(
            fixture=fixture, work_dir=work_dir, receipt_dir=receipt_dir
        )
        checks.extend(materialization_checks)
        _write_tsv(
            receipt_dir / "materialization_report.tsv",
            materialization_rows,
            [
                "registration_unit_id",
                "producer_family",
                "table_name",
                "materialization_source",
                "materialized_row_count",
                "represented_source_identity_count",
                "status",
            ],
        )
        build_assertion_records(
            manifest_path=manifest_path,
            output_dir=run_a,
            corpus_generation_id=args.corpus_generation_id,
        )
        build_assertion_records(
            manifest_path=manifest_path,
            output_dir=run_b,
            corpus_generation_id=args.corpus_generation_id,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="phase4_3_layer2_materialization_") as tmp:
            work_dir = Path(tmp)
            manifest_path, materialization_rows, materialization_checks = _materialize_registration_units(
                fixture=fixture, work_dir=work_dir, receipt_dir=receipt_dir
            )
            checks.extend(materialization_checks)
            _write_tsv(
                receipt_dir / "materialization_report.tsv",
                materialization_rows,
                [
                    "registration_unit_id",
                    "producer_family",
                    "table_name",
                    "materialization_source",
                    "materialized_row_count",
                    "represented_source_identity_count",
                    "status",
                ],
            )
            build_assertion_records(
                manifest_path=manifest_path,
                output_dir=run_a,
                corpus_generation_id=args.corpus_generation_id,
            )
            build_assertion_records(
                manifest_path=manifest_path,
                output_dir=run_b,
                corpus_generation_id=args.corpus_generation_id,
            )

    count_rows, count_checks = _validate_count_reconciliation(fixture=fixture, run_dir=run_a, input_counts=input_counts)
    checks.extend(count_checks)
    _write_tsv(receipt_dir / "count_reconciliation.tsv", count_rows, ["check_name", "expected_count", "observed_count", "status"])

    type_rows, type_checks = _validate_assertion_types(input_counts, run_a)
    checks.extend(type_checks)
    _write_tsv(
        receipt_dir / "assertion_type_reconciliation.tsv",
        type_rows,
        ["producer_family", "assertion_type", "expected_count", "observed_count", "status"],
    )

    source_rows, source_checks = _validate_source_identity_sets(fixture, run_a)
    checks.extend(source_checks)
    _write_tsv(
        receipt_dir / "source_identity_set_reconciliation.tsv",
        source_rows,
        [
            "registration_unit_id",
            "source_assertion_registration_id",
            "identity_kind",
            "participant_role",
            "source_namespace",
            "expected_source_identity_count",
            "observed_source_identity_count",
            "status",
        ],
    )

    na_rows, na_checks = _validate_source_identity_not_applicable(fixture, run_a)
    checks.extend(na_checks)
    _write_tsv(
        receipt_dir / "source_identity_not_applicable_reconciliation.tsv",
        na_rows,
        [
            "registration_unit_id",
            "producer_family",
            "source_assertion_registration_id",
            "assertion_type",
            "expected_source_identity_set_status",
            "observed_source_identity_set_status",
            "status",
        ],
    )

    preservation_rows, preservation_checks = _validate_preservation_hardening(run_a)
    checks.extend(preservation_checks)
    _write_tsv(
        receipt_dir / "preservation_hardening_report.tsv",
        preservation_rows,
        ["check_name", "expected", "observed", "status", "detail"],
    )

    anti_rows, anti_checks = _validate_anti_flattening(fixture, run_a)
    checks.extend(anti_checks)
    _write_tsv(
        receipt_dir / "anti_flattening_report.tsv",
        anti_rows,
        ["check_name", "represented_source_identity_count", "physical_source_identity_slice_rows", "source_identity_summary_rows", "participant_rows", "status"],
    )

    det_rows, det_checks = _validate_determinism(run_a, run_b)
    checks.extend(det_checks)
    _write_tsv(receipt_dir / "determinism_report.tsv", det_rows, ["output_file", "run_a_sha256", "run_b_sha256", "status"])

    non_goal_rows, non_goal_checks = _validate_non_goals(run_a)
    checks.extend(non_goal_checks)
    _write_tsv(receipt_dir / "non_goals_report.tsv", non_goal_rows, ["path", "status", "matched_token"])

    after_hashes = _hash_files(fixture.rglob("*"), fixture)
    mutation_status = "passed" if before_hashes == after_hashes else "failed"
    checks.append(
        Check(
            "fixture_inputs_not_mutated",
            mutation_status,
            "fixture hashes unchanged" if mutation_status == "passed" else "fixture hashes changed during smoketest",
        )
    )

    _write_validation_summary(receipt_dir, checks)

    failed = [check for check in checks if check.status != "passed"]
    if failed:
        print(f"Phase 4.3D golden fixture smoketest FAILED: {len(failed)} failed checks")
        print(f"Receipt: {receipt_dir}")
        return 1
    print("Phase 4.3D golden fixture smoketest PASSED")
    print(f"Receipt: {receipt_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Phase 4.3D Layer 2 Assertion Record golden fixture smoketest."
    )
    parser.add_argument(
        "--fixture",
        default=str(DEFAULT_FIXTURE),
        help=f"Committed compressed Layer 2 fixture path. Default: {DEFAULT_FIXTURE}",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help=f"Validation receipt output root. Default: {DEFAULT_OUTPUT_ROOT}",
    )
    parser.add_argument(
        "--corpus-generation-id",
        default=DEFAULT_CORPUS_GENERATION_ID,
        help=f"Corpus Generation ID to pass to the builder. Default: {DEFAULT_CORPUS_GENERATION_ID}",
    )
    parser.add_argument("--timestamp", default=None, help="Optional timestamp override YYYY_MM_DD_HHMMSS.")
    parser.add_argument(
        "--keep-workdir",
        action="store_true",
        help="Keep materialized temporary SQLite Registration Units under the receipt work/ directory.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except FileExistsError as exc:
        print(f"Operator/config error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Phase 4.3D golden fixture smoketest error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

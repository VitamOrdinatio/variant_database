#!/usr/bin/env python3
"""Run the Phase 4.2 MARK full-corpus Corpus Generation smoketest.

This is Validation Layer 3 for Phase 4.2.

It operates on the real MARK Phase 3 canonical Registration Unit SQLite files,
regenerates Phase 4.1-compatible inventory/readiness receipts from those full
SQLite files, feeds those receipts into the real Phase 4.2 Corpus Generation
emitter, validates the emitted Corpus Generation artifact set, and archives the
Layer 3 receipt bundle.

It does not use tests/fixtures.

It does not use the compressed Layer 2 golden fixture.

It does not mutate Registration Units, certify Corpus Generations, create
Assertion Records, derive topology, or interpret evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sqlite3
import tarfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from variant_database.phase4.corpus_generation.artifacts import (
    emit_corpus_generation_artifacts,
)
from variant_database.phase4.corpus_generation.manifest import (
    CANONICAL_SELECTION_MANIFEST_COLUMNS,
)
from variant_database.phase4.corpus_generation.validation import (
    validate_corpus_generation_artifact_set,
)


SMOKETEST_ID = "phase4_2_mark_full_corpus_corpus_generation_smoketest"
CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"
SELECTION_POLICY_ID = "mark_phase4_6tep_certified_input_policy"

DEFAULT_SOURCE_ROOT = Path("results/registration/mark_phase3_canonical")
DEFAULT_OUTPUT_ROOT = Path("results/validation/phase4_corpus_generation")

EXPECTED_LABELS = (
    "gsc_epilepsy",
    "gsc_mitochondrial_disease",
    "vap_hg002",
    "vap_median_ERR10619300",
    "vap_q1_ERR10619212",
    "vap_q3_ERR10619225",
)

EXPECTED_PRODUCER_DISTRIBUTION = {
    "GSC": 2,
    "VAP": 4,
}

EXPECTED_SUMMARY = {
    "included_registration_unit_count": 6,
    "excluded_registration_unit_count": 0,
    "downstream_assertion_record_input_count": 6,
    "artifact_count_total": 82,
    "assertion_registration_count_total": 52,
    "source_identity_count_total": 147941196,
}

REQUIRED_TABLES = (
    "schema_metadata",
    "tep_packages",
    "artifacts",
    "assertion_registrations",
    "source_identities",
)

FORBIDDEN_DOWNSTREAM_DIRS = (
    "assertion_records",
    "topology",
    "geometry",
    "surfaces",
    "projections",
)


def main() -> int:
    args = _parse_args()

    source_root = args.source_root
    output_root = args.output_root
    build_timestamp = args.build_timestamp or _utc_timestamp()
    validation_timestamp = args.validation_timestamp or _utc_timestamp()
    receipt_suffix = _timestamp_suffix(validation_timestamp)

    _reject_fixture_path(source_root)

    receipt_dir = output_root / f"mark_full_corpus_smoketest_{receipt_suffix}"
    _safe_reset_dir(receipt_dir, output_root)

    inputs_dir = receipt_dir / "inputs"
    phase4_1_receipts_dir = receipt_dir / "phase4_1_receipts"
    scratch_dir = receipt_dir / "scratch_corpus_generation" / CORPUS_GENERATION_ID
    validation_receipts_dir = receipt_dir / "validation_receipts"
    logs_dir = receipt_dir / "logs"

    for directory in (
        inputs_dir,
        phase4_1_receipts_dir,
        scratch_dir,
        validation_receipts_dir,
        logs_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    inspected_records = _inspect_mark_registration_units(source_root)

    inventory_path = _write_inventory(phase4_1_receipts_dir, inspected_records)
    readiness_path = _write_readiness(phase4_1_receipts_dir, inspected_records)
    selection_manifest_path = _write_selection_manifest(inputs_dir, inspected_records)
    policy_path = _write_policy(inputs_dir, inspected_records)

    policy = json.loads(policy_path.read_text(encoding="utf-8"))

    build_artifacts = emit_corpus_generation_artifacts(
        selection_manifest_path,
        scratch_dir,
        corpus_generation_label=policy["corpus_generation_label"],
        corpus_generation_purpose=policy["corpus_generation_purpose"],
        corpus_generation_version=policy["corpus_generation_version"],
        selection_policy_id=policy["selection_policy_id"],
        selection_policy_version=policy["selection_policy_version"],
        selection_policy_description=policy["selection_policy_description"],
        registration_unit_inventory_path=inventory_path,
        registration_unit_readiness_path=readiness_path,
        repo_root=Path("."),
        build_timestamp=build_timestamp,
        validate_selection_manifest_filesystem=True,
    )

    validation_result = validate_corpus_generation_artifact_set(
        scratch_dir,
        selection_manifest_path,
        policy_path,
        inventory_path,
        readiness_path,
        validation_receipts_dir,
        validation_timestamp=validation_timestamp,
    )

    observed_summary = _read_observed_summary(
        corpus_generation_manifest_json=build_artifacts.corpus_generation_manifest_json_path,
        validation_summary_json=validation_result.validation_summary_json_path,
    )
    boundary_status = _evaluate_boundary(scratch_dir, inspected_records)
    summary_status = _evaluate_summary(observed_summary, boundary_status)

    smoketest_status = (
        "passed"
        if validation_result.validation_status == "passed"
        and summary_status == "passed"
        and boundary_status == "passed"
        else "failed"
    )

    summary_payload = _build_smoketest_summary(
        source_root=source_root,
        receipt_dir=receipt_dir,
        build_timestamp=build_timestamp,
        validation_timestamp=validation_timestamp,
        inspected_records=inspected_records,
        observed_summary=observed_summary,
        validation_result=validation_result,
        build_artifacts=build_artifacts,
        boundary_status=boundary_status,
        summary_status=summary_status,
        smoketest_status=smoketest_status,
    )

    summary_json = receipt_dir / "phase4_2_mark_full_corpus_smoketest_summary.json"
    summary_tsv = receipt_dir / "phase4_2_mark_full_corpus_smoketest_summary.tsv"
    log_path = logs_dir / "phase4_2_mark_full_corpus_smoketest.log"

    summary_json.write_text(
        json.dumps(summary_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    _write_tsv(
        summary_tsv,
        (
            "smoketest_id",
            "corpus_generation_id",
            "smoketest_status",
            "validation_status",
            "summary_status",
            "boundary_status",
            "build_timestamp",
            "validation_timestamp",
            "included_registration_unit_count",
            "excluded_registration_unit_count",
            "downstream_assertion_record_input_count",
            "artifact_count_total",
            "assertion_registration_count_total",
            "source_identity_count_total",
        ),
        [
            {
                **summary_payload["smoketest_identity"],
                **summary_payload["observed_summary"],
            }
        ],
    )

    log_path.write_text(
        "\n".join(
            [
                "Phase 4.2 MARK full-corpus Corpus Generation smoketest completed.",
                f"smoketest_status: {smoketest_status}",
                f"validation_status: {validation_result.validation_status}",
                f"summary_status: {summary_status}",
                f"boundary_status: {boundary_status}",
                f"source_root: {source_root}",
                f"receipt_dir: {receipt_dir}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    _copy_latest_receipts(receipt_dir, output_root)
    archive_path = _archive_receipt(receipt_dir, output_root)

    _print_summary(
        summary_payload=summary_payload,
        receipt_dir=receipt_dir,
        archive_path=archive_path,
    )

    return 0 if smoketest_status == "passed" else 1


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Phase 4.2 MARK full-corpus Corpus Generation smoketest."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=DEFAULT_SOURCE_ROOT,
        help="MARK Phase 3 canonical Registration Unit root.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Output root for Phase 4.2 Corpus Generation validation receipts.",
    )
    parser.add_argument(
        "--build-timestamp",
        default=None,
        help="Build timestamp to preserve in emitted Corpus Generation artifacts.",
    )
    parser.add_argument(
        "--validation-timestamp",
        default=None,
        help="Validation timestamp to preserve in emitted validation receipts.",
    )
    return parser.parse_args()


def _reject_fixture_path(source_root: Path) -> None:
    source_text = str(source_root)
    if "tests/fixtures" in source_text or "golden_fixture" in source_text:
        raise ValueError(
            "Layer 3 must not use compressed fixture paths. "
            f"Rejected source root: {source_root}"
        )


def _safe_reset_dir(path: Path, allowed_parent: Path) -> None:
    path_resolved = path.resolve()
    parent_resolved = allowed_parent.resolve()

    if path_resolved == parent_resolved:
        raise ValueError(f"Refusing to reset output root directly: {path}")

    if not str(path_resolved).startswith(str(parent_resolved) + "/"):
        raise ValueError(
            f"Refusing to reset directory outside output root: {path_resolved}"
        )

    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _inspect_mark_registration_units(source_root: Path) -> list[dict[str, Any]]:
    if not source_root.is_dir():
        raise FileNotFoundError(f"MARK Phase 3 canonical source root missing: {source_root}")

    inspected: list[dict[str, Any]] = []

    for label in EXPECTED_LABELS:
        registration_unit_path = source_root / label
        sqlite_path = registration_unit_path / "vdb.sqlite"

        print(f"Inspecting MARK Registration Unit: {label}")
        print(f"  sqlite: {sqlite_path}")

        before_state = _sqlite_file_state(sqlite_path)
        preexisting_sidecars = _sqlite_sidecars(sqlite_path)

        db_status = _inspect_sqlite(sqlite_path)

        after_state = _sqlite_file_state(sqlite_path)
        postflight_sidecars = _sqlite_sidecars(sqlite_path)

        non_mutation_status = (
            "passed"
            if before_state == after_state and preexisting_sidecars == postflight_sidecars
            else "failed"
        )

        producer_family = _producer_family_from_label_or_status(label, db_status)

        inspection_status = (
            "passed"
            if db_status["open_status"] == "passed"
            and db_status["query_only_status"] == "passed"
            and db_status["required_table_status"] == "passed"
            and db_status["integrity_check_status"] == "passed"
            and non_mutation_status == "passed"
            else "failed"
        )

        readiness_status = "ready" if inspection_status == "passed" else "not_ready"
        readiness_reasons = (
            "ready MARK full-corpus registration unit"
            if readiness_status == "ready"
            else "MARK full-corpus registration unit inspection failed"
        )

        inspected.append(
            {
                "registration_unit_id": f"mark_phase3_canonical::{label}",
                "registration_unit_label": label,
                "producer_family": producer_family,
                "validation_layer": "validation_layer_3_mark_full_corpus",
                "source_role": "mark_phase3_canonical_registration_unit",
                "registration_backend": "sqlite",
                "registration_unit_path_resolved": str(registration_unit_path),
                "sqlite_path_resolved": str(sqlite_path),
                "expected_read_mode": "read_only",
                "non_mutation_status": non_mutation_status,
                "preexisting_sidecars": ";".join(preexisting_sidecars),
                "postflight_sidecars": ";".join(postflight_sidecars),
                "inspection_status": inspection_status,
                "readiness_status": readiness_status,
                "readiness_reasons": readiness_reasons,
                **db_status,
            }
        )

    return inspected


def _inspect_sqlite(sqlite_path: Path) -> dict[str, Any]:
    status: dict[str, Any] = {
        "open_status": "failed",
        "query_only_status": "failed",
        "required_table_status": "failed",
        "integrity_check_status": "failed",
        "schema_metadata_row_count": 0,
        "tep_packages_row_count": 0,
        "artifacts_row_count": 0,
        "assertion_registrations_row_count": 0,
        "source_identities_row_count": 0,
        "observed_producer_families": "",
    }

    if not sqlite_path.is_file():
        return status

    uri = f"file:{sqlite_path.as_posix()}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row

    try:
        status["open_status"] = "passed"

        conn.execute("PRAGMA query_only=ON;")
        query_only = conn.execute("PRAGMA query_only;").fetchone()[0]
        status["query_only_status"] = "passed" if int(query_only) == 1 else "failed"

        existing_tables = set(_table_names(conn))
        missing_tables = sorted(set(REQUIRED_TABLES) - existing_tables)
        status["required_table_status"] = (
            "passed" if not missing_tables else "missing:" + ",".join(missing_tables)
        )

        if not missing_tables:
            for table in REQUIRED_TABLES:
                print(f"    counting {table}")
                status[f"{table}_row_count"] = _count_rows(conn, table)

        if "assertion_registrations" in existing_tables:
            status["observed_producer_families"] = ";".join(
                _observed_producer_families(conn)
            )

        print("    running integrity_check")
        integrity_value = str(conn.execute("PRAGMA integrity_check;").fetchone()[0])
        status["integrity_check_status"] = (
            "passed" if integrity_value == "ok" else integrity_value
        )

        return status

    finally:
        conn.close()


def _table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return [str(row["name"]) for row in rows]


def _count_rows(conn: sqlite3.Connection, table: str) -> int:
    quoted = '"' + table.replace('"', '""') + '"'
    row = conn.execute(f"SELECT COUNT(*) AS row_count FROM {quoted}").fetchone()
    return int(row["row_count"])


def _observed_producer_families(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        """
        SELECT producer_family
        FROM assertion_registrations
        GROUP BY producer_family
        ORDER BY producer_family
        """
    ).fetchall()
    return [str(row["producer_family"]) for row in rows if row["producer_family"]]


def _producer_family_from_label_or_status(label: str, status: dict[str, Any]) -> str:
    observed = [
        item for item in str(status.get("observed_producer_families", "")).split(";") if item
    ]

    if len(observed) == 1:
        return observed[0]

    if label.startswith("gsc_"):
        return "GSC"

    if label.startswith("vap_"):
        return "VAP"

    return "unknown"


def _sqlite_file_state(sqlite_path: Path) -> dict[str, int | str | None]:
    if not sqlite_path.exists():
        return {
            "exists": "false",
            "size_bytes": None,
            "mtime_ns": None,
        }

    stat = sqlite_path.stat()
    return {
        "exists": "true",
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def _sqlite_sidecars(sqlite_path: Path) -> list[str]:
    candidates = [
        sqlite_path.with_name(sqlite_path.name + suffix)
        for suffix in ("-wal", "-shm", "-journal")
    ]
    return sorted(str(path) for path in candidates if path.exists())


def _write_inventory(output_dir: Path, records: list[dict[str, Any]]) -> Path:
    path = output_dir / "registration_unit_inventory.tsv"
    columns = (
        "inventory_schema_version",
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "validation_layer",
        "source_role",
        "registration_backend",
        "registration_unit_path_resolved",
        "sqlite_path_resolved",
        "expected_read_mode",
        "open_status",
        "query_only_status",
        "required_table_status",
        "integrity_check_status",
        "inspection_status",
        "schema_metadata_row_count",
        "tep_packages_row_count",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
        "observed_producer_families",
        "non_mutation_status",
        "preexisting_sidecars",
        "postflight_sidecars",
    )
    rows = [
        {
            "inventory_schema_version": "phase4_2_mark_full_corpus_inventory_v1",
            **record,
        }
        for record in records
    ]
    _write_tsv(path, columns, rows)
    return path


def _write_readiness(output_dir: Path, records: list[dict[str, Any]]) -> Path:
    path = output_dir / "registration_unit_readiness.tsv"
    columns = (
        "readiness_schema_version",
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "validation_layer",
        "source_role",
        "registration_backend",
        "registration_unit_path_resolved",
        "sqlite_path_resolved",
        "expected_read_mode",
        "open_status",
        "query_only_status",
        "required_table_status",
        "integrity_check_status",
        "inspection_status",
        "schema_metadata_row_count",
        "tep_packages_row_count",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
        "readiness_status",
        "readiness_reasons",
    )
    rows = [
        {
            "readiness_schema_version": "phase4_2_mark_full_corpus_readiness_v1",
            **record,
        }
        for record in records
    ]
    _write_tsv(path, columns, rows)
    return path


def _write_selection_manifest(
    output_dir: Path,
    records: list[dict[str, Any]],
) -> Path:
    path = output_dir / "corpus_generation_selection_manifest.tsv"
    rows: list[dict[str, Any]] = []

    for record in records:
        row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
        row.update(
            {
                "corpus_generation_id": CORPUS_GENERATION_ID,
                "registration_unit_label": record["registration_unit_label"],
                "registration_unit_reference": record["registration_unit_id"],
                "registration_unit_path": record["registration_unit_path_resolved"],
                "registration_unit_sqlite_path": record["sqlite_path_resolved"],
                "expected_registration_unit_id": record["registration_unit_id"],
                "expected_producer_family": record["producer_family"],
                "expected_registration_unit_validation_status": "passed",
                "expected_registration_unit_certification_status": "certified",
                "expected_registration_unit_readiness_status": "ready",
                "expected_backend": "sqlite",
                "inclusion_status": "included",
                "inclusion_rationale": (
                    "included in Phase 4.2 MARK full-corpus Corpus Generation smoketest"
                ),
                "exclusion_status": "",
                "exclusion_rationale": "",
                "registration_unit_inventory_record_reference": (
                    "phase4_1_receipts/registration_unit_inventory.tsv"
                ),
                "registration_unit_readiness_record_reference": (
                    "phase4_1_receipts/registration_unit_readiness.tsv"
                ),
                "phase4_1_validation_receipt_reference": "phase4_1_receipts/",
                "notes": "MARK full-corpus real-world Registration Unit",
            }
        )
        rows.append(row)

    _write_tsv(path, tuple(CANONICAL_SELECTION_MANIFEST_COLUMNS), rows)
    return path


def _write_policy(output_dir: Path, records: list[dict[str, Any]]) -> Path:
    path = output_dir / "corpus_generation_selection_policy.json"
    producer_counts = dict(Counter(record["producer_family"] for record in records))

    payload = {
        "selection_policy_id": SELECTION_POLICY_ID,
        "selection_policy_version": "v1",
        "selection_policy_description": (
            "Select the six certified MARK Phase 3 canonical Registration Units "
            "for Phase 4.2 Corpus Generation Layer 3 full-corpus validation."
        ),
        "corpus_generation_id": CORPUS_GENERATION_ID,
        "corpus_generation_label": "MARK Phase 4 6-TEP Benchmark Corpus v1",
        "corpus_generation_purpose": (
            "Layer 3 MARK full-corpus validation for Phase 4.2 Corpus Generation "
            "artifact flow"
        ),
        "corpus_generation_version": "v1",
        "required_registration_unit_validation_status": "passed",
        "required_registration_unit_certification_status": "certified",
        "required_registration_unit_readiness_status": "ready",
        "required_backend": "sqlite",
        "producer_families_in_scope": sorted(producer_counts),
        "expected_registration_unit_count": len(records),
        "expected_producer_family_counts": EXPECTED_PRODUCER_DISTRIBUTION,
        "expected_registration_unit_labels": [record["registration_unit_label"] for record in records],
        "expected_summary": EXPECTED_SUMMARY,
        "registration_unit_inventory_reference": (
            "phase4_1_receipts/registration_unit_inventory.tsv"
        ),
        "registration_unit_readiness_reference": (
            "phase4_1_receipts/registration_unit_readiness.tsv"
        ),
        "authority_boundary": {
            "uses_mark_full_corpus_data": True,
            "uses_compressed_golden_fixture": False,
            "declares_scope": True,
            "opens_sqlite_read_only": True,
            "mutates_registration_units": False,
            "interprets_evidence": False,
            "creates_assertion_records": False,
            "derives_topology": False,
            "certifies_corpus_generation": False,
        },
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _read_observed_summary(
    *,
    corpus_generation_manifest_json: Path,
    validation_summary_json: Path,
) -> dict[str, Any]:
    corpus_payload = json.loads(corpus_generation_manifest_json.read_text(encoding="utf-8"))
    validation_payload = json.loads(validation_summary_json.read_text(encoding="utf-8"))

    summaries = corpus_payload["summaries"]

    return {
        "included_registration_unit_count": summaries["included_registration_unit_count"],
        "excluded_registration_unit_count": summaries["excluded_registration_unit_count"],
        "downstream_assertion_record_input_count": summaries[
            "downstream_assertion_record_input_count"
        ],
        "artifact_count_total": summaries["artifact_count_total"],
        "assertion_registration_count_total": summaries[
            "assertion_registration_count_total"
        ],
        "source_identity_count_total": summaries["source_identity_count_total"],
        "producer_family_distribution": summaries.get("producer_family_distribution", {}),
        "corpus_generation_validation_status": corpus_payload[
            "corpus_generation_identity"
        ]["corpus_generation_validation_status"],
        "corpus_generation_certification_status": corpus_payload[
            "corpus_generation_identity"
        ]["corpus_generation_certification_status"],
        "validation_status": validation_payload["validation_status"],
        "total_check_count": validation_payload["total_check_count"],
        "passed_check_count": validation_payload["passed_check_count"],
        "failed_check_count": validation_payload["failed_check_count"],
    }


def _evaluate_boundary(
    scratch_dir: Path,
    inspected_records: list[dict[str, Any]],
) -> str:
    for record in inspected_records:
        if "tests/fixtures" in record["sqlite_path_resolved"]:
            return "failed"

        if record["non_mutation_status"] != "passed":
            return "failed"

    for forbidden_name in FORBIDDEN_DOWNSTREAM_DIRS:
        if (scratch_dir / forbidden_name).exists():
            return "failed"

    return "passed"


def _evaluate_summary(
    observed_summary: dict[str, Any],
    boundary_status: str,
) -> str:
    for key, expected_value in EXPECTED_SUMMARY.items():
        if observed_summary.get(key) != expected_value:
            return "failed"

    if observed_summary["producer_family_distribution"] != EXPECTED_PRODUCER_DISTRIBUTION:
        return "failed"

    if observed_summary["validation_status"] != "passed":
        return "failed"

    if observed_summary["failed_check_count"] != 0:
        return "failed"

    if observed_summary["corpus_generation_validation_status"] != "not_evaluated":
        return "failed"

    if observed_summary["corpus_generation_certification_status"] != "not_available":
        return "failed"

    if boundary_status != "passed":
        return "failed"

    return "passed"


def _build_smoketest_summary(
    *,
    source_root: Path,
    receipt_dir: Path,
    build_timestamp: str,
    validation_timestamp: str,
    inspected_records: list[dict[str, Any]],
    observed_summary: dict[str, Any],
    validation_result,
    build_artifacts,
    boundary_status: str,
    summary_status: str,
    smoketest_status: str,
) -> dict[str, Any]:
    return {
        "smoketest_identity": {
            "smoketest_id": SMOKETEST_ID,
            "corpus_generation_id": CORPUS_GENERATION_ID,
            "smoketest_status": smoketest_status,
            "validation_status": validation_result.validation_status,
            "summary_status": summary_status,
            "boundary_status": boundary_status,
            "build_timestamp": build_timestamp,
            "validation_timestamp": validation_timestamp,
        },
        "validation_layer": {
            "layer": "Layer 3",
            "name": "MARK Real-World Full-Corpus Smoketest",
            "purpose": (
                "Validate Phase 4.2 Corpus Generation artifact flow against the "
                "real MARK Phase 3 canonical Registration Unit corpus."
            ),
        },
        "continuation_chain": {
            "source_root": str(source_root),
            "source_substrate": "real MARK Phase 3 canonical Registration Units",
            "phase4_1_receipts_regenerated": True,
            "phase4_2_build_executed": True,
            "phase4_2_artifact_set_validated": True,
        },
        "registration_units": {
            "registration_unit_count": len(inspected_records),
            "registration_unit_labels": [
                record["registration_unit_label"] for record in inspected_records
            ],
        },
        "expected_summary": EXPECTED_SUMMARY,
        "observed_summary": observed_summary,
        "artifacts": {
            "receipt_dir": str(receipt_dir),
            "scratch_corpus_generation_dir": str(build_artifacts.output_dir),
            "corpus_generation_manifest_json": str(
                build_artifacts.corpus_generation_manifest_json_path
            ),
            "corpus_generation_manifest_tsv": str(
                build_artifacts.corpus_generation_manifest_tsv_path
            ),
            "downstream_assertion_record_input_manifest": str(
                build_artifacts.downstream_assertion_record_input_manifest_path
            ),
            "validation_report_json": str(validation_result.validation_report_json_path),
            "validation_report_tsv": str(validation_result.validation_report_tsv_path),
            "validation_summary_json": str(validation_result.validation_summary_json_path),
            "validation_summary_tsv": str(validation_result.validation_summary_tsv_path),
        },
        "authority_boundary": {
            "uses_mark_full_corpus_data": True,
            "uses_compressed_golden_fixture": False,
            "opens_sqlite_read_only": True,
            "mutates_registration_units": False,
            "certifies_corpus_generation": False,
            "creates_assertion_records": False,
            "derives_topology": False,
            "interprets_evidence": False,
        },
    }


def _copy_latest_receipts(receipt_dir: Path, output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    for filename in (
        "phase4_2_mark_full_corpus_smoketest_summary.json",
        "phase4_2_mark_full_corpus_smoketest_summary.tsv",
    ):
        shutil.copyfile(receipt_dir / filename, output_root / filename)


def _archive_receipt(receipt_dir: Path, output_root: Path) -> Path:
    archive_root = output_root / "receipt_archives"
    archive_root.mkdir(parents=True, exist_ok=True)

    archive_path = archive_root / f"{receipt_dir.name}.tgz"
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(receipt_dir, arcname=receipt_dir.name)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {archive_path.name}\n", encoding="utf-8")

    return archive_path


def _print_summary(
    *,
    summary_payload: dict[str, Any],
    receipt_dir: Path,
    archive_path: Path,
) -> None:
    identity = summary_payload["smoketest_identity"]
    observed = summary_payload["observed_summary"]

    print()
    print("Phase 4.2 MARK full-corpus Corpus Generation smoketest complete.")
    print()
    print(f"smoketest_id: {identity['smoketest_id']}")
    print(f"corpus_generation_id: {identity['corpus_generation_id']}")
    print(f"smoketest_status: {identity['smoketest_status']}")
    print(f"validation_status: {identity['validation_status']}")
    print(f"summary_status: {identity['summary_status']}")
    print(f"boundary_status: {identity['boundary_status']}")
    print()
    print(f"receipt_dir: {receipt_dir}")
    print(f"receipt_archive: {archive_path}")
    print()
    print("observed_summary:")
    for key in (
        "included_registration_unit_count",
        "excluded_registration_unit_count",
        "downstream_assertion_record_input_count",
        "artifact_count_total",
        "assertion_registration_count_total",
        "source_identity_count_total",
        "producer_family_distribution",
        "total_check_count",
        "passed_check_count",
        "failed_check_count",
    ):
        print(f"  {key}: {observed[key]}")


def _write_tsv(
    path: Path,
    columns: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(columns),
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _timestamp_suffix(timestamp: str) -> str:
    return (
        timestamp.replace("-", "_")
        .replace(":", "")
        .replace("T", "_")
        .replace("Z", "")
    )


if __name__ == "__main__":
    raise SystemExit(main())

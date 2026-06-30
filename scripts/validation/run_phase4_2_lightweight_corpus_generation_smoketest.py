#!/usr/bin/env python3
"""Run the Phase 4.2 lightweight Corpus Generation smoketest.

This is Validation Layer 2 for Phase 4.2.

It creates a small golden fixture substrate, emits Corpus Generation build
artifacts through the real emitter, validates those artifacts through the real
validator, writes durable smoketest receipts, and archives the receipt bundle.

It does not use MARK data.

It does not open SQLite, mutate Registration Units, certify Corpus Generations,
create Assertion Records, derive topology, or interpret evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tarfile
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


SMOKETEST_ID = "phase4_2_lightweight_corpus_generation_smoketest"
CORPUS_GENERATION_ID = "lightweight_phase4_2_corpus_v1"
SELECTION_POLICY_ID = "lightweight_phase4_2_golden_fixture_policy"

DEFAULT_OUTPUT_ROOT = Path("results/validation/phase4_corpus_generation")

EXPECTED_SUMMARY = {
    "included_registration_unit_count": 2,
    "excluded_registration_unit_count": 1,
    "downstream_assertion_record_input_count": 2,
    "artifact_count_total": 25,
    "assertion_registration_count_total": 16,
    "source_identity_count_total": 300,
}


def main() -> int:
    args = _parse_args()

    output_root = args.output_root
    build_timestamp = args.build_timestamp or _utc_timestamp()
    validation_timestamp = args.validation_timestamp or _utc_timestamp()
    receipt_suffix = _timestamp_suffix(validation_timestamp)

    receipt_dir = output_root / f"lightweight_fixture_smoketest_{receipt_suffix}"
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

    selection_manifest = _write_selection_manifest(inputs_dir)
    policy_path = _write_policy(inputs_dir)
    inventory_path = _write_inventory(phase4_1_receipts_dir)
    readiness_path = _write_readiness(phase4_1_receipts_dir)

    policy = json.loads(policy_path.read_text(encoding="utf-8"))

    build_artifacts = emit_corpus_generation_artifacts(
        selection_manifest,
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
        validate_selection_manifest_filesystem=False,
    )

    validation_result = validate_corpus_generation_artifact_set(
        scratch_dir,
        selection_manifest,
        policy_path,
        inventory_path,
        readiness_path,
        validation_receipts_dir,
        validation_timestamp=validation_timestamp,
    )

    observed_summary = _read_observed_summary(
        build_artifacts.corpus_generation_manifest_json_path,
        validation_result.validation_summary_json_path,
    )
    summary_status = _evaluate_summary(observed_summary)

    smoketest_status = (
        "passed"
        if validation_result.validation_status == "passed"
        and summary_status == "passed"
        else "failed"
    )

    summary_payload = _build_smoketest_summary(
        receipt_dir=receipt_dir,
        build_timestamp=build_timestamp,
        validation_timestamp=validation_timestamp,
        build_artifacts=build_artifacts,
        validation_result=validation_result,
        observed_summary=observed_summary,
        summary_status=summary_status,
        smoketest_status=smoketest_status,
    )

    summary_json = receipt_dir / "phase4_2_lightweight_smoketest_summary.json"
    summary_tsv = receipt_dir / "phase4_2_lightweight_smoketest_summary.tsv"
    log_path = logs_dir / "phase4_2_lightweight_smoketest.log"

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
                "Phase 4.2 lightweight Corpus Generation smoketest completed.",
                f"smoketest_status: {smoketest_status}",
                f"validation_status: {validation_result.validation_status}",
                f"summary_status: {summary_status}",
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
        description="Run the Phase 4.2 lightweight Corpus Generation smoketest."
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


def _write_selection_manifest(inputs_dir: Path) -> Path:
    path = inputs_dir / "lightweight_phase4_2_selection_manifest.tsv"
    rows = [
        _selection_row(
            label="gsc_lightweight_fixture",
            producer_family="GSC",
            included=True,
        ),
        _selection_row(
            label="vap_lightweight_fixture",
            producer_family="VAP",
            included=True,
        ),
        _selection_row(
            label="vap_deferred_lightweight_fixture",
            producer_family="VAP",
            included=False,
        ),
    ]
    _write_tsv(path, CANONICAL_SELECTION_MANIFEST_COLUMNS, rows)
    return path


def _selection_row(
    *,
    label: str,
    producer_family: str,
    included: bool,
) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": CORPUS_GENERATION_ID,
            "registration_unit_label": label,
            "registration_unit_reference": label,
            "registration_unit_path": f"lightweight_fixture/registration/{label}",
            "registration_unit_sqlite_path": (
                f"lightweight_fixture/registration/{label}/vdb.sqlite"
            ),
            "expected_registration_unit_id": "",
            "expected_producer_family": producer_family,
            "expected_registration_unit_validation_status": "passed",
            "expected_registration_unit_certification_status": "certified",
            "expected_registration_unit_readiness_status": "ready",
            "expected_backend": "sqlite",
            "registration_unit_inventory_record_reference": (
                "phase4_1_receipts/registration_unit_inventory.tsv"
            ),
            "registration_unit_readiness_record_reference": (
                "phase4_1_receipts/registration_unit_readiness.tsv"
            ),
            "phase4_1_validation_receipt_reference": "phase4_1_receipts/",
            "notes": f"{label} lightweight fixture row",
        }
    )

    if included:
        row["inclusion_status"] = "included"
        row["inclusion_rationale"] = "lightweight golden fixture included input"
    else:
        row["exclusion_status"] = "deferred"
        row["exclusion_rationale"] = "lightweight golden fixture deferred control"

    return row


def _write_policy(inputs_dir: Path) -> Path:
    path = inputs_dir / "lightweight_phase4_2_selection_policy.json"
    payload = {
        "selection_policy_id": SELECTION_POLICY_ID,
        "selection_policy_version": "v1",
        "selection_policy_description": (
            "Select a two-unit lightweight golden Corpus Generation fixture "
            "with one deferred control row for Phase 4.2 smoketesting."
        ),
        "corpus_generation_id": CORPUS_GENERATION_ID,
        "corpus_generation_label": "Lightweight Phase 4.2 Corpus Generation Fixture v1",
        "corpus_generation_purpose": (
            "local golden fixture smoketest for Phase 4.2 Corpus Generation"
        ),
        "corpus_generation_version": "v1",
        "required_registration_unit_validation_status": "passed",
        "required_registration_unit_certification_status": "certified",
        "required_registration_unit_readiness_status": "ready",
        "required_backend": "sqlite",
        "producer_families_in_scope": ["GSC", "VAP"],
        "expected_registration_unit_count": 2,
        "expected_producer_family_counts": {"GSC": 1, "VAP": 1},
        "expected_registration_unit_labels": [
            "gsc_lightweight_fixture",
            "vap_lightweight_fixture",
        ],
        "registration_unit_inventory_reference": (
            "phase4_1_receipts/registration_unit_inventory.tsv"
        ),
        "registration_unit_readiness_reference": (
            "phase4_1_receipts/registration_unit_readiness.tsv"
        ),
        "authority_boundary": {
            "declares_scope": True,
            "interprets_evidence": False,
            "creates_assertion_records": False,
            "derives_topology": False,
            "certifies_corpus_generation": False,
        },
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_inventory(receipts_dir: Path) -> Path:
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
    )
    rows = [
        {
            "inventory_schema_version": "phase4_registration_unit_inventory_v1",
            "registration_unit_id": "ru_gsc_lightweight_fixture",
            "registration_unit_label": "gsc_lightweight_fixture",
            "producer_family": "GSC",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": (
                "lightweight_fixture/registration/gsc_lightweight_fixture"
            ),
            "sqlite_path_resolved": (
                "lightweight_fixture/registration/gsc_lightweight_fixture/vdb.sqlite"
            ),
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "9",
            "assertion_registrations_row_count": "6",
            "source_identities_row_count": "100",
        },
        {
            "inventory_schema_version": "phase4_registration_unit_inventory_v1",
            "registration_unit_id": "ru_vap_lightweight_fixture",
            "registration_unit_label": "vap_lightweight_fixture",
            "producer_family": "VAP",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": (
                "lightweight_fixture/registration/vap_lightweight_fixture"
            ),
            "sqlite_path_resolved": (
                "lightweight_fixture/registration/vap_lightweight_fixture/vdb.sqlite"
            ),
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "16",
            "assertion_registrations_row_count": "10",
            "source_identities_row_count": "200",
        },
    ]
    path = receipts_dir / "registration_unit_inventory.tsv"
    _write_tsv(path, columns, rows)
    return path


def _write_readiness(receipts_dir: Path) -> Path:
    columns = (
        "readiness_schema_version",
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "validation_layer",
        "source_role",
        "registration_backend",
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
            "readiness_schema_version": "phase4_registration_unit_readiness_v1",
            "registration_unit_id": "ru_gsc_lightweight_fixture",
            "registration_unit_label": "gsc_lightweight_fixture",
            "producer_family": "GSC",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "9",
            "assertion_registrations_row_count": "6",
            "source_identities_row_count": "100",
            "readiness_status": "ready",
            "readiness_reasons": "ready lightweight fixture",
        },
        {
            "readiness_schema_version": "phase4_registration_unit_readiness_v1",
            "registration_unit_id": "ru_vap_lightweight_fixture",
            "registration_unit_label": "vap_lightweight_fixture",
            "producer_family": "VAP",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "16",
            "assertion_registrations_row_count": "10",
            "source_identities_row_count": "200",
            "readiness_status": "ready",
            "readiness_reasons": "ready lightweight fixture",
        },
    ]
    path = receipts_dir / "registration_unit_readiness.tsv"
    _write_tsv(path, columns, rows)
    return path


def _read_observed_summary(
    corpus_generation_manifest_json: Path,
    validation_summary_json: Path,
) -> dict[str, Any]:
    corpus_payload = json.loads(corpus_generation_manifest_json.read_text(encoding="utf-8"))
    validation_payload = json.loads(validation_summary_json.read_text(encoding="utf-8"))

    return {
        "included_registration_unit_count": corpus_payload["summaries"][
            "included_registration_unit_count"
        ],
        "excluded_registration_unit_count": corpus_payload["summaries"][
            "excluded_registration_unit_count"
        ],
        "downstream_assertion_record_input_count": corpus_payload["summaries"][
            "downstream_assertion_record_input_count"
        ],
        "artifact_count_total": corpus_payload["summaries"]["artifact_count_total"],
        "assertion_registration_count_total": corpus_payload["summaries"][
            "assertion_registration_count_total"
        ],
        "source_identity_count_total": corpus_payload["summaries"][
            "source_identity_count_total"
        ],
        "validation_status": validation_payload["validation_status"],
        "total_check_count": validation_payload["total_check_count"],
        "passed_check_count": validation_payload["passed_check_count"],
        "failed_check_count": validation_payload["failed_check_count"],
    }


def _evaluate_summary(observed_summary: dict[str, Any]) -> str:
    for key, expected_value in EXPECTED_SUMMARY.items():
        if observed_summary.get(key) != expected_value:
            return "failed"
    if observed_summary["validation_status"] != "passed":
        return "failed"
    if observed_summary["failed_check_count"] != 0:
        return "failed"
    return "passed"


def _build_smoketest_summary(
    *,
    receipt_dir: Path,
    build_timestamp: str,
    validation_timestamp: str,
    build_artifacts,
    validation_result,
    observed_summary: dict[str, Any],
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
            "build_timestamp": build_timestamp,
            "validation_timestamp": validation_timestamp,
        },
        "validation_layer": {
            "layer": "Layer 2",
            "name": "Lightweight Golden Fixture Smoketest",
            "purpose": (
                "Prove that Phase 4.2 Corpus Generation artifact flow works on "
                "a small controlled substrate through the real emitter and validator."
            ),
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
            "uses_mark_data": False,
            "opens_sqlite": False,
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
        "phase4_2_lightweight_smoketest_summary.json",
        "phase4_2_lightweight_smoketest_summary.tsv",
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

    print("Phase 4.2 lightweight Corpus Generation smoketest complete.")
    print()
    print(f"smoketest_id: {identity['smoketest_id']}")
    print(f"corpus_generation_id: {identity['corpus_generation_id']}")
    print(f"smoketest_status: {identity['smoketest_status']}")
    print(f"validation_status: {identity['validation_status']}")
    print(f"summary_status: {identity['summary_status']}")
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

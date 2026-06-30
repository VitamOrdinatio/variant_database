"""Corpus Generation artifact-set validation.

This module validates Phase 4.2 Corpus Generation build artifacts against a
governed selection manifest, selection policy, and Phase 4.1 Registration Unit
inventory/readiness receipts.

It validates artifact-set coherence only.

It intentionally does not:
- open SQLite
- mutate Registration Units
- certify Corpus Generations
- create Assertion Records
- derive topology, geometry, surfaces, projections, or interpretation
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from variant_database.phase4.corpus_generation.artifacts import (
    CORPUS_GENERATION_MANIFEST_COLUMNS,
    DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS,
)
from variant_database.phase4.corpus_generation.manifest import (
    load_corpus_generation_selection_manifest,
)


VALIDATOR_NAME = "variant_database.phase4.corpus_generation.validation"
VALIDATOR_VERSION = "0.1.0"

VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class CorpusGenerationValidationCheck:
    """Single Corpus Generation validation check."""

    check_id: str
    validation_group: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class CorpusGenerationValidationResult:
    """Corpus Generation validation result and emitted receipt paths."""

    corpus_generation_id: str
    validation_status: str
    validation_output_dir: Path
    validation_report_json_path: Path
    validation_report_tsv_path: Path
    validation_summary_json_path: Path
    validation_summary_tsv_path: Path
    checks: tuple[CorpusGenerationValidationCheck, ...]


def validate_corpus_generation_artifact_set(
    corpus_generation_dir: str | Path,
    selection_manifest_path: str | Path,
    policy_path: str | Path,
    registration_unit_inventory_path: str | Path,
    registration_unit_readiness_path: str | Path,
    validation_output_dir: str | Path,
    *,
    validation_timestamp: str,
) -> CorpusGenerationValidationResult:
    """Validate a Corpus Generation artifact set and emit validation receipts."""

    if not validation_timestamp:
        raise ValueError("validation_timestamp is required.")

    corpus_dir = Path(corpus_generation_dir)
    selection_manifest_file = Path(selection_manifest_path)
    policy_file = Path(policy_path)
    inventory_file = Path(registration_unit_inventory_path)
    readiness_file = Path(registration_unit_readiness_path)
    receipt_dir = Path(validation_output_dir)

    policy = _read_json(policy_file)
    selection_manifest = load_corpus_generation_selection_manifest(
        selection_manifest_file,
        repo_root=Path("."),
        validate_filesystem=False,
    )

    corpus_generation_id = policy["corpus_generation_id"]
    checks: list[CorpusGenerationValidationCheck] = []

    def add_check(
        check_id: str,
        group: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
    ) -> None:
        checks.append(
            CorpusGenerationValidationCheck(
                check_id=check_id,
                validation_group=group,
                status=(
                    VALIDATION_STATUS_PASSED
                    if passed
                    else VALIDATION_STATUS_FAILED
                ),
                message=message,
                expected=_stringify(expected),
                observed=_stringify(observed),
            )
        )

    required_files = {
        "copied_selection_manifest": (
            corpus_dir / "inputs" / "corpus_generation_selection_manifest.tsv"
        ),
        "corpus_generation_manifest_tsv": (
            corpus_dir / "corpus_generation_manifest.tsv"
        ),
        "corpus_generation_manifest_json": (
            corpus_dir / "corpus_generation_manifest.json"
        ),
        "corpus_generation_report_md": corpus_dir / "corpus_generation_report.md",
        "downstream_assertion_record_input_manifest_tsv": (
            corpus_dir / "downstream_assertion_record_input_manifest.tsv"
        ),
    }

    for artifact_name, path in required_files.items():
        add_check(
            f"artifact_presence__{artifact_name}",
            "artifact_presence",
            path.is_file(),
            f"Required artifact exists: {artifact_name}",
            "file exists",
            path,
        )
        add_check(
            f"artifact_nonempty__{artifact_name}",
            "artifact_presence",
            path.is_file() and path.stat().st_size > 0,
            f"Required artifact is non-empty: {artifact_name}",
            "non-empty file",
            path.stat().st_size if path.is_file() else "missing",
        )

    if any(not path.is_file() for path in required_files.values()):
        return _emit_validation_result(
            corpus_generation_id=corpus_generation_id,
            validation_output_dir=receipt_dir,
            validation_timestamp=validation_timestamp,
            corpus_generation_dir=corpus_dir,
            selection_manifest_path=selection_manifest_file,
            policy_path=policy_file,
            registration_unit_inventory_path=inventory_file,
            registration_unit_readiness_path=readiness_file,
            checks=checks,
        )

    copied_selection_manifest = required_files["copied_selection_manifest"]
    corpus_manifest_tsv = required_files["corpus_generation_manifest_tsv"]
    corpus_manifest_json = required_files["corpus_generation_manifest_json"]
    downstream_manifest_tsv = required_files[
        "downstream_assertion_record_input_manifest_tsv"
    ]

    corpus_header, corpus_rows = _read_tsv(corpus_manifest_tsv)
    downstream_header, downstream_rows = _read_tsv(downstream_manifest_tsv)
    payload = _read_json(corpus_manifest_json)
    inventory_rows = _read_receipt_by_label(inventory_file)
    readiness_rows = _read_receipt_by_label(readiness_file)

    add_check(
        "corpus_manifest_header",
        "artifact_shape",
        tuple(corpus_header) == CORPUS_GENERATION_MANIFEST_COLUMNS,
        "Corpus Generation manifest TSV uses canonical columns.",
        CORPUS_GENERATION_MANIFEST_COLUMNS,
        tuple(corpus_header),
    )
    add_check(
        "downstream_manifest_header",
        "artifact_shape",
        tuple(downstream_header) == DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS,
        "Downstream Assertion Record input manifest TSV uses canonical columns.",
        DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS,
        tuple(downstream_header),
    )

    required_json_keys = {
        "artifacts",
        "build_metadata",
        "corpus_generation_identity",
        "included_registration_units",
        "excluded_registration_units",
        "selection_manifest",
        "selection_policy",
        "phase4_1_receipts",
        "summaries",
    }
    add_check(
        "manifest_json_top_level_keys",
        "artifact_shape",
        required_json_keys <= set(payload),
        "Corpus Generation manifest JSON contains required top-level keys.",
        sorted(required_json_keys),
        sorted(payload),
    )

    add_check(
        "copied_selection_manifest_matches_source",
        "artifact_shape",
        copied_selection_manifest.read_text(encoding="utf-8")
        == selection_manifest_file.read_text(encoding="utf-8"),
        "Copied input selection manifest matches governed source manifest.",
        "byte-equivalent text",
        "matched"
        if copied_selection_manifest.read_text(encoding="utf-8")
        == selection_manifest_file.read_text(encoding="utf-8")
        else "different",
    )

    tsv_ids = {row["corpus_generation_id"] for row in corpus_rows}
    downstream_ids = {row["corpus_generation_id"] for row in downstream_rows}
    json_id = payload["corpus_generation_identity"]["corpus_generation_id"]

    add_check(
        "identity_coherence",
        "identity",
        {
            policy["corpus_generation_id"],
            selection_manifest.corpus_generation_id,
            json_id,
            *tsv_ids,
            *downstream_ids,
        }
        == {corpus_generation_id},
        "Policy, selection manifest, emitted TSVs, downstream manifest, and JSON identity agree.",
        corpus_generation_id,
        sorted(
            {
                policy["corpus_generation_id"],
                selection_manifest.corpus_generation_id,
                json_id,
                *tsv_ids,
                *downstream_ids,
            }
        ),
    )
    add_check(
        "output_directory_identity",
        "identity",
        corpus_dir.name == corpus_generation_id,
        "Output directory name matches corpus_generation_id.",
        corpus_generation_id,
        corpus_dir.name,
    )

    selected_labels = [
        record.registration_unit_label
        for record in selection_manifest.included_records
    ]
    selected_all_labels = [
        record.registration_unit_label for record in selection_manifest.records
    ]
    emitted_all_labels = [row["registration_unit_label"] for row in corpus_rows]
    emitted_included_rows = [
        row
        for row in corpus_rows
        if row["membership_record_type"] == "included_registration_unit"
    ]
    emitted_included_labels = [
        row["registration_unit_label"] for row in emitted_included_rows
    ]
    downstream_labels = [row["registration_unit_label"] for row in downstream_rows]

    add_check(
        "scope_row_count",
        "scope_preservation",
        len(corpus_rows) == len(selection_manifest.records),
        "Emitted corpus manifest preserves selection-manifest row count.",
        len(selection_manifest.records),
        len(corpus_rows),
    )
    add_check(
        "scope_row_order",
        "scope_preservation",
        emitted_all_labels == selected_all_labels,
        "Emitted corpus manifest preserves selection-manifest row order.",
        selected_all_labels,
        emitted_all_labels,
    )
    add_check(
        "included_scope_labels",
        "scope_preservation",
        emitted_included_labels == selected_labels,
        "Emitted included Registration Unit labels match selected included labels.",
        selected_labels,
        emitted_included_labels,
    )
    add_check(
        "policy_expected_labels",
        "scope_preservation",
        policy["expected_registration_unit_labels"] == selected_labels,
        "Policy expected Registration Unit labels match selected included labels.",
        policy["expected_registration_unit_labels"],
        selected_labels,
    )
    add_check(
        "downstream_included_only",
        "downstream_boundary",
        downstream_labels == selected_labels,
        "Downstream Assertion Record input manifest contains included rows only.",
        selected_labels,
        downstream_labels,
    )

    producer_distribution = dict(
        sorted(Counter(row["producer_family"] for row in emitted_included_rows).items())
    )
    add_check(
        "producer_family_distribution",
        "scope_preservation",
        producer_distribution == policy["expected_producer_family_counts"],
        "Producer family distribution matches policy.",
        policy["expected_producer_family_counts"],
        producer_distribution,
    )

    _add_receipt_enrichment_checks(
        add_check=add_check,
        emitted_included_rows=emitted_included_rows,
        inventory_rows=inventory_rows,
        readiness_rows=readiness_rows,
    )

    _add_summary_checks(
        add_check=add_check,
        emitted_included_rows=emitted_included_rows,
        payload=payload,
    )

    corpus_rows_by_label = {
        row["registration_unit_label"]: row for row in emitted_included_rows
    }
    for downstream_row in downstream_rows:
        label = downstream_row["registration_unit_label"]
        source_row = corpus_rows_by_label.get(label)
        add_check(
            f"downstream_projection_source__{label}",
            "downstream_boundary",
            source_row is not None,
            f"Downstream row has included Corpus Generation source row: {label}",
            "included corpus row exists",
            "found" if source_row is not None else "missing",
        )
        if source_row is not None:
            for column in DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS:
                add_check(
                    f"downstream_projection__{label}__{column}",
                    "downstream_boundary",
                    downstream_row[column] == source_row[column],
                    f"Downstream field is projected from Corpus Generation row: {label}.{column}",
                    source_row[column],
                    downstream_row[column],
                )

    validation_statuses = {
        row["corpus_generation_validation_status"] for row in corpus_rows
    }
    certification_statuses = {
        row["corpus_generation_certification_status"] for row in corpus_rows
    }

    add_check(
        "anti_self_validation_tsv",
        "authority_boundary",
        validation_statuses == {"not_evaluated"},
        "Build artifacts do not self-validate.",
        {"not_evaluated"},
        validation_statuses,
    )
    add_check(
        "anti_self_certification_tsv",
        "authority_boundary",
        certification_statuses == {"not_available"},
        "Build artifacts do not self-certify.",
        {"not_available"},
        certification_statuses,
    )
    add_check(
        "anti_self_validation_json",
        "authority_boundary",
        payload["corpus_generation_identity"]["corpus_generation_validation_status"]
        == "not_evaluated",
        "Manifest JSON does not self-validate.",
        "not_evaluated",
        payload["corpus_generation_identity"]["corpus_generation_validation_status"],
    )
    add_check(
        "anti_self_certification_json",
        "authority_boundary",
        payload["corpus_generation_identity"]["corpus_generation_certification_status"]
        == "not_available",
        "Manifest JSON does not self-certify.",
        "not_available",
        payload["corpus_generation_identity"]["corpus_generation_certification_status"],
    )

    forbidden_children = {
        "assertion_records",
        "topology",
        "geometry",
        "surfaces",
        "projections",
        "validation",
        "validation_receipts",
    }
    observed_forbidden = [
        child.name for child in corpus_dir.iterdir() if child.name in forbidden_children
    ]
    add_check(
        "no_layer_leakage_directories",
        "authority_boundary",
        observed_forbidden == [],
        "Corpus Generation build directory does not contain downstream layer directories.",
        [],
        observed_forbidden,
    )

    return _emit_validation_result(
        corpus_generation_id=corpus_generation_id,
        validation_output_dir=receipt_dir,
        validation_timestamp=validation_timestamp,
        corpus_generation_dir=corpus_dir,
        selection_manifest_path=selection_manifest_file,
        policy_path=policy_file,
        registration_unit_inventory_path=inventory_file,
        registration_unit_readiness_path=readiness_file,
        checks=checks,
    )


def _add_receipt_enrichment_checks(
    *,
    add_check,
    emitted_included_rows: list[dict[str, str]],
    inventory_rows: dict[str, dict[str, str]],
    readiness_rows: dict[str, dict[str, str]],
) -> None:
    field_map = {
        "registration_unit_id": ("inventory", "registration_unit_id"),
        "producer_family": ("inventory", "producer_family"),
        "registration_backend": ("inventory", "registration_backend"),
        "artifact_count": ("inventory", "artifacts_row_count"),
        "assertion_registration_count": (
            "inventory",
            "assertion_registrations_row_count",
        ),
        "source_identity_count": ("inventory", "source_identities_row_count"),
        "registration_unit_validation_status": ("inventory", "inspection_status"),
        "registration_unit_readiness_status": ("readiness", "readiness_status"),
    }

    for row in emitted_included_rows:
        label = row["registration_unit_label"]
        inventory = inventory_rows.get(label)
        readiness = readiness_rows.get(label)

        add_check(
            f"receipt_inventory_row_exists__{label}",
            "phase4_1_enrichment",
            inventory is not None,
            f"Phase 4.1 inventory row exists for included Registration Unit: {label}",
            "inventory row exists",
            "found" if inventory is not None else "missing",
        )
        add_check(
            f"receipt_readiness_row_exists__{label}",
            "phase4_1_enrichment",
            readiness is not None,
            f"Phase 4.1 readiness row exists for included Registration Unit: {label}",
            "readiness row exists",
            "found" if readiness is not None else "missing",
        )

        if inventory is None or readiness is None:
            continue

        for emitted_field, (receipt_source, receipt_field) in field_map.items():
            receipt_row = inventory if receipt_source == "inventory" else readiness
            add_check(
                f"receipt_enrichment__{label}__{emitted_field}",
                "phase4_1_enrichment",
                row[emitted_field] == receipt_row[receipt_field],
                f"Emitted field matches Phase 4.1 receipt: {label}.{emitted_field}",
                receipt_row[receipt_field],
                row[emitted_field],
            )


def _add_summary_checks(
    *,
    add_check,
    emitted_included_rows: list[dict[str, str]],
    payload: dict[str, Any],
) -> None:
    summaries = payload["summaries"]

    aggregate_fields = {
        "artifact_count_total": "artifact_count",
        "assertion_registration_count_total": "assertion_registration_count",
        "source_identity_count_total": "source_identity_count",
    }

    for summary_field, row_field in aggregate_fields.items():
        computed = sum(int(row[row_field]) for row in emitted_included_rows)
        observed = summaries[summary_field]
        add_check(
            f"summary_{summary_field}",
            "phase4_1_enrichment",
            computed == observed,
            f"Manifest JSON summary matches emitted included-row total: {summary_field}",
            computed,
            observed,
        )


def _emit_validation_result(
    *,
    corpus_generation_id: str,
    validation_output_dir: Path,
    validation_timestamp: str,
    corpus_generation_dir: Path,
    selection_manifest_path: Path,
    policy_path: Path,
    registration_unit_inventory_path: Path,
    registration_unit_readiness_path: Path,
    checks: list[CorpusGenerationValidationCheck],
) -> CorpusGenerationValidationResult:
    validation_output_dir.mkdir(parents=True, exist_ok=True)

    validation_status = (
        VALIDATION_STATUS_PASSED
        if all(check.status == VALIDATION_STATUS_PASSED for check in checks)
        else VALIDATION_STATUS_FAILED
    )

    report_json_path = validation_output_dir / "corpus_generation_validation_report.json"
    report_tsv_path = validation_output_dir / "corpus_generation_validation_report.tsv"
    summary_json_path = validation_output_dir / "corpus_generation_validation_summary.json"
    summary_tsv_path = validation_output_dir / "corpus_generation_validation_summary.tsv"

    passed_count = sum(check.status == VALIDATION_STATUS_PASSED for check in checks)
    failed_count = sum(check.status == VALIDATION_STATUS_FAILED for check in checks)

    report_payload = {
        "validation_identity": {
            "corpus_generation_id": corpus_generation_id,
            "validation_status": validation_status,
            "validation_timestamp": validation_timestamp,
            "validator_name": VALIDATOR_NAME,
            "validator_version": VALIDATOR_VERSION,
        },
        "inputs": {
            "corpus_generation_dir": str(corpus_generation_dir),
            "selection_manifest_path": str(selection_manifest_path),
            "policy_path": str(policy_path),
            "registration_unit_inventory_path": str(registration_unit_inventory_path),
            "registration_unit_readiness_path": str(registration_unit_readiness_path),
        },
        "summary": {
            "total_check_count": len(checks),
            "passed_check_count": passed_count,
            "failed_check_count": failed_count,
        },
        "checks": [asdict(check) for check in checks],
    }

    summary_payload = {
        **report_payload["validation_identity"],
        **report_payload["summary"],
    }

    report_json_path.write_text(
        json.dumps(report_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary_json_path.write_text(
        json.dumps(summary_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    _write_tsv(
        report_tsv_path,
        (
            "check_id",
            "validation_group",
            "status",
            "message",
            "expected",
            "observed",
        ),
        [asdict(check) for check in checks],
    )
    _write_tsv(
        summary_tsv_path,
        (
            "corpus_generation_id",
            "validation_status",
            "validation_timestamp",
            "validator_name",
            "validator_version",
            "total_check_count",
            "passed_check_count",
            "failed_check_count",
        ),
        [summary_payload],
    )

    return CorpusGenerationValidationResult(
        corpus_generation_id=corpus_generation_id,
        validation_status=validation_status,
        validation_output_dir=validation_output_dir,
        validation_report_json_path=report_json_path,
        validation_report_tsv_path=report_tsv_path,
        validation_summary_json_path=summary_json_path,
        validation_summary_tsv_path=summary_tsv_path,
        checks=tuple(checks),
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _read_receipt_by_label(path: Path) -> dict[str, dict[str, str]]:
    _, rows = _read_tsv(path)
    return {row["registration_unit_label"]: row for row in rows}


def _write_tsv(
    path: Path,
    columns: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> None:
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
            writer.writerow({column: _stringify(row.get(column, "")) for column in columns})


def _stringify(value: object) -> str:
    if isinstance(value, set):
        return json.dumps(sorted(value))
    if isinstance(value, tuple):
        return json.dumps(list(value))
    if isinstance(value, list):
        return json.dumps(value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return str(value)

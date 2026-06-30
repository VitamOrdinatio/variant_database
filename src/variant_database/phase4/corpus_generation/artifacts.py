"""Corpus Generation artifact emission.

This module emits Phase 4.2 Corpus Generation build artifacts from an explicit
selection manifest and optional Phase 4.1 Registration Unit inventory/readiness
receipts.

It intentionally does not:
- open SQLite
- mutate Registration Units
- emit validation receipts
- certify Corpus Generations
- create Assertion Records
- derive topology, geometry, surfaces, projections, or interpretation
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from variant_database.phase4.corpus_generation.manifest import (
    CorpusGenerationSelectionManifest,
    CorpusGenerationSelectionManifestRecord,
    load_corpus_generation_selection_manifest,
)


class CorpusGenerationArtifactError(ValueError):
    """Raised when Corpus Generation artifact emission fails."""


NOT_REPORTED = "not_reported"
NOT_AVAILABLE = "not_available"
NOT_EVALUATED = "not_evaluated"

DEFAULT_BUILDER_NAME = "variant_database.phase4.corpus_generation.artifacts"
DEFAULT_BUILDER_VERSION = "0.1.0"
DEFAULT_MANIFEST_SCHEMA_VERSION = "corpus_generation_schema_v1"


CORPUS_GENERATION_MANIFEST_COLUMNS: tuple[str, ...] = (
    "corpus_generation_id",
    "corpus_generation_label",
    "corpus_generation_purpose",
    "corpus_generation_version",
    "selection_policy_id",
    "selection_policy_version",
    "membership_record_type",
    "registration_unit_id",
    "registration_unit_label",
    "registration_unit_reference",
    "registration_unit_path",
    "registration_unit_sqlite_path",
    "registration_unit_inventory_record_reference",
    "registration_unit_readiness_record_reference",
    "phase4_1_validation_receipt_reference",
    "producer_family",
    "source_package_id",
    "registration_backend",
    "registration_unit_validation_status",
    "registration_unit_certification_status",
    "registration_unit_readiness_status",
    "corpus_generation_validation_status",
    "corpus_generation_certification_status",
    "inclusion_status",
    "inclusion_rationale",
    "exclusion_status",
    "exclusion_rationale",
    "artifact_count",
    "assertion_registration_count",
    "source_identity_count",
    "namespace_count",
    "evidence_domain_count",
    "builder_name",
    "builder_version",
    "build_timestamp",
    "manifest_schema_version",
    "notes",
)

DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS: tuple[str, ...] = (
    "corpus_generation_id",
    "registration_unit_id",
    "registration_unit_label",
    "registration_unit_reference",
    "registration_unit_path",
    "registration_unit_sqlite_path",
    "registration_unit_inventory_record_reference",
    "registration_unit_readiness_record_reference",
    "phase4_1_validation_receipt_reference",
    "producer_family",
    "source_package_id",
    "registration_backend",
    "assertion_registration_count",
    "source_identity_count",
    "registration_unit_validation_status",
    "registration_unit_certification_status",
    "registration_unit_readiness_status",
    "inclusion_status",
    "inclusion_rationale",
)

REQUIRED_INVENTORY_COLUMNS: frozenset[str] = frozenset(
    {
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "registration_backend",
        "registration_unit_path_resolved",
        "sqlite_path_resolved",
        "inspection_status",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
    }
)

REQUIRED_READINESS_COLUMNS: frozenset[str] = frozenset(
    {
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "registration_backend",
        "inspection_status",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
        "readiness_status",
        "readiness_reasons",
    }
)


@dataclass(frozen=True)
class CorpusGenerationSelectionPolicy:
    """Selection policy metadata preserved in Corpus Generation artifacts."""

    selection_policy_id: str
    selection_policy_version: str
    selection_policy_description: str
    required_registration_unit_validation_status: str = "passed"
    required_registration_unit_certification_status: str = "certified"
    required_registration_unit_readiness_status: str = "ready"


@dataclass(frozen=True)
class CorpusGenerationArtifactSet:
    """Paths emitted by Corpus Generation artifact construction."""

    output_dir: Path
    copied_selection_manifest_path: Path
    corpus_generation_manifest_tsv_path: Path
    corpus_generation_manifest_json_path: Path
    corpus_generation_report_path: Path
    downstream_assertion_record_input_manifest_path: Path


def emit_corpus_generation_artifacts(
    selection_manifest_path: str | Path,
    output_dir: str | Path,
    *,
    corpus_generation_label: str,
    corpus_generation_purpose: str,
    selection_policy_id: str,
    selection_policy_version: str,
    selection_policy_description: str,
    registration_unit_inventory_path: str | Path | None = None,
    registration_unit_readiness_path: str | Path | None = None,
    repo_root: str | Path | None = None,
    build_timestamp: str,
    corpus_generation_version: str = "v1",
    builder_name: str = DEFAULT_BUILDER_NAME,
    builder_version: str = DEFAULT_BUILDER_VERSION,
    manifest_schema_version: str = DEFAULT_MANIFEST_SCHEMA_VERSION,
    validate_selection_manifest_filesystem: bool = False,
) -> CorpusGenerationArtifactSet:
    """Emit deterministic Corpus Generation build artifacts.

    Parameters
    ----------
    selection_manifest_path:
        Explicit Corpus Generation selection manifest TSV.
    output_dir:
        Directory where build artifacts will be written.
    corpus_generation_label:
        Human-readable Corpus Generation label.
    corpus_generation_purpose:
        Declared Corpus Generation purpose.
    selection_policy_id, selection_policy_version, selection_policy_description:
        Selection policy metadata to preserve in emitted artifacts.
    registration_unit_inventory_path:
        Optional Phase 4.1 inventory TSV used to enrich membership records.
    registration_unit_readiness_path:
        Optional Phase 4.1 readiness TSV used to enrich membership records.
    repo_root:
        Optional base path for resolving relative selection-manifest paths.
    build_timestamp:
        Build timestamp. Required explicitly so tests and reproducible builds can
        inject a deterministic timestamp.
    validate_selection_manifest_filesystem:
        If true, require included Registration Unit directories and SQLite files
        declared in the selection manifest to exist. This does not open SQLite.
    """

    if not build_timestamp:
        raise CorpusGenerationArtifactError("build_timestamp is required.")

    if not corpus_generation_label:
        raise CorpusGenerationArtifactError("corpus_generation_label is required.")

    if not corpus_generation_purpose:
        raise CorpusGenerationArtifactError("corpus_generation_purpose is required.")

    policy = CorpusGenerationSelectionPolicy(
        selection_policy_id=selection_policy_id,
        selection_policy_version=selection_policy_version,
        selection_policy_description=selection_policy_description,
    )
    _validate_policy(policy)

    selection_manifest = load_corpus_generation_selection_manifest(
        selection_manifest_path,
        repo_root=repo_root,
        validate_filesystem=validate_selection_manifest_filesystem,
    )

    inventory_by_label = _load_inventory_by_label(registration_unit_inventory_path)
    readiness_by_label = _load_readiness_by_label(registration_unit_readiness_path)

    manifest_rows = _build_manifest_rows(
        selection_manifest=selection_manifest,
        corpus_generation_label=corpus_generation_label,
        corpus_generation_purpose=corpus_generation_purpose,
        corpus_generation_version=corpus_generation_version,
        policy=policy,
        inventory_by_label=inventory_by_label,
        readiness_by_label=readiness_by_label,
        builder_name=builder_name,
        builder_version=builder_version,
        build_timestamp=build_timestamp,
        manifest_schema_version=manifest_schema_version,
        require_inventory=registration_unit_inventory_path is not None,
        require_readiness=registration_unit_readiness_path is not None,
    )

    destination_dir = Path(output_dir)
    inputs_dir = destination_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    copied_selection_manifest_path = inputs_dir / "corpus_generation_selection_manifest.tsv"
    source_selection_manifest_path = Path(selection_manifest_path)
    _copy_if_not_same(source_selection_manifest_path, copied_selection_manifest_path)

    selection_manifest_sha256 = _sha256_file(source_selection_manifest_path)

    corpus_manifest_tsv = destination_dir / "corpus_generation_manifest.tsv"
    corpus_manifest_json = destination_dir / "corpus_generation_manifest.json"
    corpus_report = destination_dir / "corpus_generation_report.md"
    downstream_manifest = destination_dir / "downstream_assertion_record_input_manifest.tsv"

    _write_tsv(corpus_manifest_tsv, CORPUS_GENERATION_MANIFEST_COLUMNS, manifest_rows)

    downstream_rows = [
        _to_downstream_row(row)
        for row in manifest_rows
        if row["membership_record_type"] == "included_registration_unit"
    ]
    _write_tsv(
        downstream_manifest,
        DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS,
        downstream_rows,
    )

    payload = _build_json_payload(
        selection_manifest=selection_manifest,
        copied_selection_manifest_path=copied_selection_manifest_path,
        selection_manifest_sha256=selection_manifest_sha256,
        corpus_generation_label=corpus_generation_label,
        corpus_generation_purpose=corpus_generation_purpose,
        corpus_generation_version=corpus_generation_version,
        policy=policy,
        manifest_rows=manifest_rows,
        downstream_rows=downstream_rows,
        corpus_manifest_tsv=corpus_manifest_tsv,
        corpus_manifest_json=corpus_manifest_json,
        corpus_report=corpus_report,
        downstream_manifest=downstream_manifest,
        registration_unit_inventory_path=registration_unit_inventory_path,
        registration_unit_readiness_path=registration_unit_readiness_path,
        builder_name=builder_name,
        builder_version=builder_version,
        build_timestamp=build_timestamp,
        manifest_schema_version=manifest_schema_version,
    )
    _write_json(corpus_manifest_json, payload)

    report = _build_markdown_report(
        payload=payload,
        manifest_rows=manifest_rows,
        downstream_rows=downstream_rows,
    )
    corpus_report.write_text(report, encoding="utf-8")

    return CorpusGenerationArtifactSet(
        output_dir=destination_dir,
        copied_selection_manifest_path=copied_selection_manifest_path,
        corpus_generation_manifest_tsv_path=corpus_manifest_tsv,
        corpus_generation_manifest_json_path=corpus_manifest_json,
        corpus_generation_report_path=corpus_report,
        downstream_assertion_record_input_manifest_path=downstream_manifest,
    )


def _validate_policy(policy: CorpusGenerationSelectionPolicy) -> None:
    if not policy.selection_policy_id:
        raise CorpusGenerationArtifactError("selection_policy_id is required.")

    if not policy.selection_policy_version:
        raise CorpusGenerationArtifactError("selection_policy_version is required.")

    if not policy.selection_policy_description:
        raise CorpusGenerationArtifactError(
            "selection_policy_description is required."
        )


def _build_manifest_rows(
    *,
    selection_manifest: CorpusGenerationSelectionManifest,
    corpus_generation_label: str,
    corpus_generation_purpose: str,
    corpus_generation_version: str,
    policy: CorpusGenerationSelectionPolicy,
    inventory_by_label: dict[str, dict[str, str]],
    readiness_by_label: dict[str, dict[str, str]],
    builder_name: str,
    builder_version: str,
    build_timestamp: str,
    manifest_schema_version: str,
    require_inventory: bool,
    require_readiness: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for record in selection_manifest.records:
        inventory = _lookup_optional_receipt_row(
            receipt_by_label=inventory_by_label,
            label=record.registration_unit_label,
            receipt_name="inventory",
            source_row_number=record.source_row_number,
            required=require_inventory and record.is_included,
        )
        readiness = _lookup_optional_receipt_row(
            receipt_by_label=readiness_by_label,
            label=record.registration_unit_label,
            receipt_name="readiness",
            source_row_number=record.source_row_number,
            required=require_readiness and record.is_included,
        )

        _check_expected_metadata(record, inventory, readiness)

        rows.append(
            _build_manifest_row(
                record=record,
                corpus_generation_label=corpus_generation_label,
                corpus_generation_purpose=corpus_generation_purpose,
                corpus_generation_version=corpus_generation_version,
                policy=policy,
                inventory=inventory,
                readiness=readiness,
                builder_name=builder_name,
                builder_version=builder_version,
                build_timestamp=build_timestamp,
                manifest_schema_version=manifest_schema_version,
            )
        )

    return rows


def _build_manifest_row(
    *,
    record: CorpusGenerationSelectionManifestRecord,
    corpus_generation_label: str,
    corpus_generation_purpose: str,
    corpus_generation_version: str,
    policy: CorpusGenerationSelectionPolicy,
    inventory: dict[str, str] | None,
    readiness: dict[str, str] | None,
    builder_name: str,
    builder_version: str,
    build_timestamp: str,
    manifest_schema_version: str,
) -> dict[str, str]:
    membership_record_type = (
        "included_registration_unit"
        if record.is_included
        else "excluded_registration_unit"
    )

    producer_family = _first_reported(
        _from_receipt(inventory, "producer_family"),
        _from_receipt(readiness, "producer_family"),
        record.expected_producer_family,
    )

    registration_backend = _first_reported(
        _from_receipt(inventory, "registration_backend"),
        _from_receipt(readiness, "registration_backend"),
        record.expected_backend,
    )

    registration_unit_validation_status = _first_reported(
        _from_receipt(readiness, "inspection_status"),
        _from_receipt(inventory, "inspection_status"),
        record.expected_registration_unit_validation_status,
    )

    registration_unit_certification_status = _first_reported(
        record.expected_registration_unit_certification_status,
        NOT_REPORTED,
    )

    registration_unit_readiness_status = _first_reported(
        _from_receipt(readiness, "readiness_status"),
        record.expected_registration_unit_readiness_status,
    )

    return {
        "corpus_generation_id": record.corpus_generation_id,
        "corpus_generation_label": corpus_generation_label,
        "corpus_generation_purpose": corpus_generation_purpose,
        "corpus_generation_version": corpus_generation_version,
        "selection_policy_id": policy.selection_policy_id,
        "selection_policy_version": policy.selection_policy_version,
        "membership_record_type": membership_record_type,
        "registration_unit_id": _first_reported(
            _from_receipt(inventory, "registration_unit_id"),
            _from_receipt(readiness, "registration_unit_id"),
            record.expected_registration_unit_id,
        ),
        "registration_unit_label": record.registration_unit_label,
        "registration_unit_reference": _first_reported(
            record.registration_unit_reference,
            record.registration_unit_label,
        ),
        "registration_unit_path": _first_reported(
            record.registration_unit_path,
            _from_receipt(inventory, "registration_unit_path_resolved"),
        ),
        "registration_unit_sqlite_path": _first_reported(
            record.registration_unit_sqlite_path,
            _from_receipt(inventory, "sqlite_path_resolved"),
        ),
        "registration_unit_inventory_record_reference": _first_reported(
            record.registration_unit_inventory_record_reference,
            NOT_REPORTED,
        ),
        "registration_unit_readiness_record_reference": _first_reported(
            record.registration_unit_readiness_record_reference,
            NOT_REPORTED,
        ),
        "phase4_1_validation_receipt_reference": _first_reported(
            record.phase4_1_validation_receipt_reference,
            NOT_REPORTED,
        ),
        "producer_family": producer_family,
        "source_package_id": NOT_REPORTED,
        "registration_backend": registration_backend,
        "registration_unit_validation_status": registration_unit_validation_status,
        "registration_unit_certification_status": registration_unit_certification_status,
        "registration_unit_readiness_status": registration_unit_readiness_status,
        "corpus_generation_validation_status": NOT_EVALUATED,
        "corpus_generation_certification_status": NOT_AVAILABLE,
        "inclusion_status": record.inclusion_status,
        "inclusion_rationale": record.inclusion_rationale,
        "exclusion_status": record.exclusion_status,
        "exclusion_rationale": record.exclusion_rationale,
        "artifact_count": _first_reported(
            _from_receipt(inventory, "artifacts_row_count"),
            _from_receipt(readiness, "artifacts_row_count"),
        ),
        "assertion_registration_count": _first_reported(
            _from_receipt(inventory, "assertion_registrations_row_count"),
            _from_receipt(readiness, "assertion_registrations_row_count"),
        ),
        "source_identity_count": _first_reported(
            _from_receipt(inventory, "source_identities_row_count"),
            _from_receipt(readiness, "source_identities_row_count"),
        ),
        "namespace_count": NOT_REPORTED,
        "evidence_domain_count": NOT_REPORTED,
        "builder_name": builder_name,
        "builder_version": builder_version,
        "build_timestamp": build_timestamp,
        "manifest_schema_version": manifest_schema_version,
        "notes": record.notes,
    }


def _lookup_optional_receipt_row(
    *,
    receipt_by_label: dict[str, dict[str, str]],
    label: str,
    receipt_name: str,
    source_row_number: int,
    required: bool,
) -> dict[str, str] | None:
    row = receipt_by_label.get(label)
    if row is None and required:
        raise CorpusGenerationArtifactError(
            f"Row {source_row_number} registration_unit_label {label!r} "
            f"was not found in the Phase 4.1 {receipt_name} receipt."
        )

    return row


def _check_expected_metadata(
    record: CorpusGenerationSelectionManifestRecord,
    inventory: dict[str, str] | None,
    readiness: dict[str, str] | None,
) -> None:
    """Compare selection-manifest expectations against observed receipt metadata.

    Missing receipt metadata is not a mismatch.

    This is especially important for excluded or deferred candidates, which may
    intentionally lack Phase 4.1 inventory/readiness receipt rows.
    """

    observed_producer = _first_observed(
        _from_receipt(inventory, "producer_family"),
        _from_receipt(readiness, "producer_family"),
    )
    if (
        record.expected_producer_family
        and observed_producer
        and observed_producer != record.expected_producer_family
    ):
        raise CorpusGenerationArtifactError(
            f"Row {record.source_row_number} expected producer family "
            f"{record.expected_producer_family!r} but observed {observed_producer!r}."
        )

    observed_backend = _first_observed(
        _from_receipt(inventory, "registration_backend"),
        _from_receipt(readiness, "registration_backend"),
    )
    if (
        record.expected_backend
        and observed_backend
        and observed_backend != record.expected_backend
    ):
        raise CorpusGenerationArtifactError(
            f"Row {record.source_row_number} expected backend "
            f"{record.expected_backend!r} but observed {observed_backend!r}."
        )


def _to_downstream_row(row: dict[str, str]) -> dict[str, str]:
    return {
        column: row[column]
        for column in DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS
    }


def _load_inventory_by_label(path: str | Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}

    return _load_receipt_by_label(
        path=path,
        required_columns=REQUIRED_INVENTORY_COLUMNS,
        receipt_name="inventory",
    )


def _load_readiness_by_label(path: str | Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}

    return _load_receipt_by_label(
        path=path,
        required_columns=REQUIRED_READINESS_COLUMNS,
        receipt_name="readiness",
    )


def _load_receipt_by_label(
    *,
    path: str | Path,
    required_columns: frozenset[str],
    receipt_name: str,
) -> dict[str, dict[str, str]]:
    receipt_path = Path(path)
    if not receipt_path.is_file():
        raise CorpusGenerationArtifactError(
            f"Phase 4.1 {receipt_name} receipt does not exist: {receipt_path}"
        )

    with receipt_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = reader.fieldnames or []
        observed_columns = set(fieldnames)
        missing = sorted(required_columns - observed_columns)
        if missing:
            raise CorpusGenerationArtifactError(
                f"Phase 4.1 {receipt_name} receipt is missing required columns: "
                + ", ".join(missing)
            )

        rows_by_label: dict[str, dict[str, str]] = {}
        for row_number, raw_row in enumerate(reader, start=2):
            row = {key: _clean(value) for key, value in raw_row.items()}
            label = row.get("registration_unit_label", "")
            if not label:
                raise CorpusGenerationArtifactError(
                    f"Phase 4.1 {receipt_name} receipt row {row_number} "
                    "is missing registration_unit_label."
                )
            if label in rows_by_label:
                raise CorpusGenerationArtifactError(
                    f"Phase 4.1 {receipt_name} receipt contains duplicate "
                    f"registration_unit_label: {label}"
                )
            rows_by_label[label] = row

    return rows_by_label


def _build_json_payload(
    *,
    selection_manifest: CorpusGenerationSelectionManifest,
    copied_selection_manifest_path: Path,
    selection_manifest_sha256: str,
    corpus_generation_label: str,
    corpus_generation_purpose: str,
    corpus_generation_version: str,
    policy: CorpusGenerationSelectionPolicy,
    manifest_rows: list[dict[str, str]],
    downstream_rows: list[dict[str, str]],
    corpus_manifest_tsv: Path,
    corpus_manifest_json: Path,
    corpus_report: Path,
    downstream_manifest: Path,
    registration_unit_inventory_path: str | Path | None,
    registration_unit_readiness_path: str | Path | None,
    builder_name: str,
    builder_version: str,
    build_timestamp: str,
    manifest_schema_version: str,
) -> dict[str, Any]:
    included_rows = [
        row
        for row in manifest_rows
        if row["membership_record_type"] == "included_registration_unit"
    ]
    excluded_rows = [
        row
        for row in manifest_rows
        if row["membership_record_type"] != "included_registration_unit"
    ]

    return {
        "artifacts": {
            "corpus_generation_manifest_json": str(corpus_manifest_json),
            "corpus_generation_manifest_tsv": str(corpus_manifest_tsv),
            "corpus_generation_report_md": str(corpus_report),
            "downstream_assertion_record_input_manifest_tsv": str(
                downstream_manifest
            ),
        },
        "build_metadata": {
            "builder_name": builder_name,
            "builder_version": builder_version,
            "build_timestamp": build_timestamp,
            "manifest_schema_version": manifest_schema_version,
        },
        "corpus_generation_identity": {
            "corpus_generation_id": selection_manifest.corpus_generation_id,
            "corpus_generation_label": corpus_generation_label,
            "corpus_generation_purpose": corpus_generation_purpose,
            "corpus_generation_version": corpus_generation_version,
            "corpus_generation_validation_status": NOT_EVALUATED,
            "corpus_generation_certification_status": NOT_AVAILABLE,
        },
        "excluded_registration_units": excluded_rows,
        "included_registration_units": included_rows,
        "selection_manifest": {
            "source_path": str(selection_manifest.manifest_path),
            "copied_path": str(copied_selection_manifest_path),
            "sha256": selection_manifest_sha256,
            "record_count": len(selection_manifest.records),
        },
        "selection_policy": {
            "selection_policy_id": policy.selection_policy_id,
            "selection_policy_version": policy.selection_policy_version,
            "selection_policy_description": policy.selection_policy_description,
            "required_registration_unit_validation_status": (
                policy.required_registration_unit_validation_status
            ),
            "required_registration_unit_certification_status": (
                policy.required_registration_unit_certification_status
            ),
            "required_registration_unit_readiness_status": (
                policy.required_registration_unit_readiness_status
            ),
        },
        "phase4_1_receipts": {
            "registration_unit_inventory_path": (
                str(registration_unit_inventory_path)
                if registration_unit_inventory_path is not None
                else NOT_REPORTED
            ),
            "registration_unit_readiness_path": (
                str(registration_unit_readiness_path)
                if registration_unit_readiness_path is not None
                else NOT_REPORTED
            ),
        },
        "summaries": _build_summaries(
            included_rows=included_rows,
            excluded_rows=excluded_rows,
            downstream_rows=downstream_rows,
        ),
    }


def _build_summaries(
    *,
    included_rows: list[dict[str, str]],
    excluded_rows: list[dict[str, str]],
    downstream_rows: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "included_registration_unit_count": len(included_rows),
        "excluded_registration_unit_count": len(excluded_rows),
        "downstream_assertion_record_input_count": len(downstream_rows),
        "producer_family_distribution": _counter_dict(
            row["producer_family"] for row in included_rows
        ),
        "registration_unit_readiness_status_distribution": _counter_dict(
            row["registration_unit_readiness_status"] for row in included_rows
        ),
        "registration_unit_validation_status_distribution": _counter_dict(
            row["registration_unit_validation_status"] for row in included_rows
        ),
        "registration_unit_certification_status_distribution": _counter_dict(
            row["registration_unit_certification_status"] for row in included_rows
        ),
        "artifact_count_total": _sum_reported_ints(
            row["artifact_count"] for row in included_rows
        ),
        "assertion_registration_count_total": _sum_reported_ints(
            row["assertion_registration_count"] for row in included_rows
        ),
        "source_identity_count_total": _sum_reported_ints(
            row["source_identity_count"] for row in included_rows
        ),
    }


def _build_markdown_report(
    *,
    payload: dict[str, Any],
    manifest_rows: list[dict[str, str]],
    downstream_rows: list[dict[str, str]],
) -> str:
    identity = payload["corpus_generation_identity"]
    policy = payload["selection_policy"]
    summaries = payload["summaries"]

    included_rows = [
        row
        for row in manifest_rows
        if row["membership_record_type"] == "included_registration_unit"
    ]
    excluded_rows = [
        row
        for row in manifest_rows
        if row["membership_record_type"] != "included_registration_unit"
    ]

    included_table = _markdown_table(
        headers=[
            "registration_unit_label",
            "producer_family",
            "readiness",
            "assertions",
            "source_identities",
        ],
        rows=[
            [
                row["registration_unit_label"],
                row["producer_family"],
                row["registration_unit_readiness_status"],
                row["assertion_registration_count"],
                row["source_identity_count"],
            ]
            for row in included_rows
        ],
    )

    excluded_table = _markdown_table(
        headers=[
            "registration_unit_label",
            "exclusion_status",
            "exclusion_rationale",
        ],
        rows=[
            [
                row["registration_unit_label"],
                row["exclusion_status"],
                row["exclusion_rationale"],
            ]
            for row in excluded_rows
        ],
    )

    return f"""# Corpus Generation Report

## Identity

```text
corpus_generation_id: {identity["corpus_generation_id"]}
corpus_generation_label: {identity["corpus_generation_label"]}
corpus_generation_purpose: {identity["corpus_generation_purpose"]}
corpus_generation_version: {identity["corpus_generation_version"]}
corpus_generation_validation_status: {identity["corpus_generation_validation_status"]}
corpus_generation_certification_status: {identity["corpus_generation_certification_status"]}
```

## Selection Policy

```text
selection_policy_id: {policy["selection_policy_id"]}
selection_policy_version: {policy["selection_policy_version"]}
selection_policy_description: {policy["selection_policy_description"]}
```

## Input Selection Manifest

```text
copied_path: {payload["selection_manifest"]["copied_path"]}
sha256: {payload["selection_manifest"]["sha256"]}
record_count: {payload["selection_manifest"]["record_count"]}
```

## Phase 4.1 Receipt Inputs

```text
registration_unit_inventory_path: {payload["phase4_1_receipts"]["registration_unit_inventory_path"]}
registration_unit_readiness_path: {payload["phase4_1_receipts"]["registration_unit_readiness_path"]}
```

## Summary

```text
included_registration_unit_count: {summaries["included_registration_unit_count"]}
excluded_registration_unit_count: {summaries["excluded_registration_unit_count"]}
downstream_assertion_record_input_count: {summaries["downstream_assertion_record_input_count"]}
artifact_count_total: {summaries["artifact_count_total"]}
assertion_registration_count_total: {summaries["assertion_registration_count_total"]}
source_identity_count_total: {summaries["source_identity_count_total"]}
```

## Included Registration Units

{included_table}

## Excluded Or Deferred Registration Units

{excluded_table}

## Boundary

This report is a Corpus Generation build artifact.

It is not source truth.

It is not a validation receipt.

It does not certify the Corpus Generation.

It does not create Assertion Records, topology, geometry, surfaces, projections, or biological interpretation.

## Downstream Handoff

```text
downstream_assertion_record_input_manifest_rows: {len(downstream_rows)}
```
"""


def _markdown_table(*, headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_None._"

    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def _write_tsv(
    path: Path,
    columns: tuple[str, ...],
    rows: list[dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(columns),
            delimiter="\t",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _copy_if_not_same(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        same_file = source.resolve(strict=True) == destination.resolve(strict=False)
    except FileNotFoundError:
        same_file = False

    if not same_file:
        shutil.copyfile(source, destination)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _counter_dict(values: Any) -> dict[str, int]:
    return dict(sorted(Counter(value for value in values if value).items()))


def _sum_reported_ints(values: Any) -> int | str:
    total = 0
    observed = False
    for value in values:
        if value in {"", NOT_REPORTED, NOT_AVAILABLE, NOT_EVALUATED}:
            continue
        try:
            total += int(value)
            observed = True
        except ValueError:
            return NOT_REPORTED
    return total if observed else NOT_REPORTED


def _from_receipt(row: dict[str, str] | None, field: str) -> str:
    if row is None:
        return ""
    return row.get(field, "")


def _first_reported(*values: str) -> str:
    for value in values:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
    return NOT_REPORTED


def _first_observed(*values: str) -> str:
    """Return the first truly observed value, excluding unresolved sentinels."""

    unresolved = {
        "",
        NOT_REPORTED,
        NOT_AVAILABLE,
        NOT_EVALUATED,
        "not_applicable",
        "unresolved",
        "ambiguous",
        "conflicted",
        "inspection_failed",
        "unknown",
    }
    for value in values:
        cleaned = _clean(value)
        if cleaned and cleaned not in unresolved:
            return cleaned
    return ""


def _clean(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()

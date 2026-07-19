"""Lossless source genotype observation preservation.

This module implements the row-preservation substrate required before VDB may
claim ``genotype_preservation_validated``. It preserves producer rows in source
order, retains every emitted column in an ordered JSON representation, and does
not register genotype-to-variant relationships or infer inheritance.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence

from variant_database.persistence.genotype_repositories import (
    genotype_preservation_scope_id_for_request,
    persist_genotype_preservation_scope,
    persist_source_genotype_observation_batch,
    source_genotype_observation_persistence_id,
    update_genotype_preservation_scope_completion,
)

GENOTYPE_OBSERVATIONS_ROLE = "genotype_observations"
PRESERVATION_SCOPE_KIND_BOUNDED = "bounded_first_n_source_rows"
PRESERVATION_SCOPE_KIND_FULL = "full_source_artifact"
ROW_SELECTION_POLICY_FIRST_N = "source_row_order_first_n"
ROW_SELECTION_POLICY_ALL = "all_source_rows"
PRESERVATION_STATUS_IN_PROGRESS = "preservation_in_progress"
PRESERVATION_STATUS_COMPLETE_PENDING_VALIDATION = (
    "preservation_complete_pending_validation"
)

REQUIRED_SOURCE_FIELDS = (
    "schema_version",
    "genotype_observation_id",
    "sample_id",
    "run_id",
    "source_record_hash",
    "reference_build",
    "chromosome",
    "position",
    "reference_allele",
    "alternate_alleles_raw",
    "variant_relationship_status",
)

TYPED_SOURCE_FIELDS = (
    "genotype_observation_id_version",
    "schema_version",
    "entity_type",
    "evidence_class",
    "sample_id",
    "sample_alias",
    "sra_accession",
    "run_id",
    "vcf_sample_column_name",
    "sample_selection_policy",
    "sample_identity_mapping_status",
    "source_pipeline",
    "assay_type",
    "source_vcf_path",
    "source_vcf_sha256",
    "source_vcf_header_hash",
    "source_record_ordinal",
    "source_line_number",
    "source_record_hash",
    "reference_build",
    "chromosome",
    "position",
    "reference_allele",
    "alternate_alleles_raw",
    "alternate_allele_count",
    "called_allele_indices",
    "variant_relationship_status",
    "relationship_reason",
    "relationship_resolution_target",
    "variant_id",
    "variant_observation_id",
    "format_raw",
    "sample_format_raw",
    "gt_raw",
    "ad_raw",
    "dp_raw",
    "gq_raw",
    "pl_raw",
    "ft_raw",
    "record_parse_status",
    "record_preservation_status",
)


@dataclass(frozen=True)
class GenotypePreservationRequest:
    """Declared preservation scope for one VAP package."""

    package_id: str
    scope_label: str
    source_tep_id: str
    row_limit: int | None
    batch_size: int = 500

    def validate(self) -> None:
        if not self.package_id:
            raise ValueError("package_id is required")
        if not self.scope_label:
            raise ValueError("scope_label is required")
        if not self.source_tep_id:
            raise ValueError("source_tep_id is required")
        if self.row_limit is not None and self.row_limit < 1:
            raise ValueError("row_limit must be positive when provided")
        if self.batch_size < 1:
            raise ValueError("batch_size must be positive")


@dataclass(frozen=True)
class GenotypePreservationSummary:
    """Summary of one preservation execution."""

    package_id: str
    preservation_scope_id: str
    scope_label: str
    preservation_scope_kind: str
    row_selection_policy: str
    requested_row_limit: int | None
    selected_row_count: int
    source_declared_row_count: int | None
    first_selected_source_row: int | None
    last_selected_source_row: int | None
    source_column_count: int
    source_artifact_path: str
    source_artifact_sha256: str
    preservation_status: str


def preserve_genotype_observations(
    connection: sqlite3.Connection,
    request: GenotypePreservationRequest,
) -> GenotypePreservationSummary:
    """Preserve producer genotype rows under one explicit bounded/full scope.

    The function is intentionally additive. It does not mutate producer values,
    create relationship rows, or advance package maturity.
    """

    request.validate()
    classification = _load_classification(connection, request.package_id)
    _require_preservation_eligible_classification(classification)

    package_path = _load_package_path(connection, request.package_id)
    artifact = _load_genotype_observation_artifact(connection, request.package_id)
    source_path = Path(package_path) / str(artifact["artifact_path"])
    if not source_path.is_file():
        raise FileNotFoundError(f"Genotype observation artifact not found: {source_path}")

    source_declared_row_count = _load_source_declared_row_count(
        connection, request.package_id
    )
    scope_kind = (
        PRESERVATION_SCOPE_KIND_BOUNDED
        if request.row_limit is not None
        else PRESERVATION_SCOPE_KIND_FULL
    )
    row_selection_policy = (
        ROW_SELECTION_POLICY_FIRST_N
        if request.row_limit is not None
        else ROW_SELECTION_POLICY_ALL
    )
    scope_id = genotype_preservation_scope_id_for_request(
        package_id=request.package_id,
        scope_label=request.scope_label,
        source_artifact_sha256=str(artifact["artifact_sha256"]),
        row_selection_policy=row_selection_policy,
        requested_row_limit=request.row_limit,
    )

    existing = connection.execute(
        """
        SELECT preservation_scope_id
        FROM source_genotype_preservation_scopes
        WHERE preservation_scope_id = ? OR (package_id = ? AND scope_label = ?)
        """,
        (scope_id, request.package_id, request.scope_label),
    ).fetchone()
    if existing is not None:
        raise ValueError(
            "Genotype preservation scope already exists; use a new database or "
            f"scope label: {request.scope_label}"
        )

    with source_path.open(
        "r", encoding="utf-8", errors="strict", newline=""
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = tuple(reader.fieldnames or ())
        _validate_header(fieldnames)

        scope_record = {
            "preservation_scope_id": scope_id,
            "package_id": request.package_id,
            "source_tep_id": request.source_tep_id,
            "source_artifact_id": artifact["artifact_id"],
            "source_artifact_path": artifact["artifact_path"],
            "source_artifact_sha256": artifact["artifact_sha256"],
            "preservation_scope_kind": scope_kind,
            "scope_label": request.scope_label,
            "row_selection_policy": row_selection_policy,
            "requested_row_limit": request.row_limit,
            "selected_row_count": 0,
            "source_declared_row_count": source_declared_row_count,
            "first_selected_source_row": None,
            "last_selected_source_row": None,
            "source_column_order_json": json.dumps(fieldnames),
            "preservation_status": PRESERVATION_STATUS_IN_PROGRESS,
            "payload_json": json.dumps(
                {
                    "batch_size": request.batch_size,
                    "requested_row_limit": request.row_limit,
                    "row_selection_policy": row_selection_policy,
                    "scope_label": request.scope_label,
                    "source_tep_id": request.source_tep_id,
                },
                sort_keys=True,
            ),
        }

        selected_count = 0
        first_row_number: int | None = None
        last_row_number: int | None = None
        batch: list[dict[str, object]] = []

        with connection:
            persist_genotype_preservation_scope(
                connection,
                scope_record,
                commit=False,
            )

            for source_row_number, row in _iter_selected_rows(
                reader,
                request.row_limit,
            ):
                selected_count += 1
                first_row_number = first_row_number or source_row_number
                last_row_number = source_row_number
                batch.append(
                    _build_observation_record(
                        package_id=request.package_id,
                        preservation_scope_id=scope_id,
                        source_row_number=source_row_number,
                        fieldnames=fieldnames,
                        row=row,
                    )
                )

                if len(batch) >= request.batch_size:
                    persist_source_genotype_observation_batch(
                        connection,
                        batch,
                        commit=False,
                    )
                    batch.clear()

            if batch:
                persist_source_genotype_observation_batch(
                    connection,
                    batch,
                    commit=False,
                )

            if request.row_limit is not None and selected_count != request.row_limit:
                raise ValueError(
                    "Requested bounded preservation row count was not available: "
                    f"requested={request.row_limit}, selected={selected_count}"
                )

            update_genotype_preservation_scope_completion(
                connection,
                preservation_scope_id=scope_id,
                selected_row_count=selected_count,
                first_selected_source_row=first_row_number,
                last_selected_source_row=last_row_number,
                preservation_status=(
                    PRESERVATION_STATUS_COMPLETE_PENDING_VALIDATION
                ),
                commit=False,
            )

    return GenotypePreservationSummary(
        package_id=request.package_id,
        preservation_scope_id=scope_id,
        scope_label=request.scope_label,
        preservation_scope_kind=scope_kind,
        row_selection_policy=row_selection_policy,
        requested_row_limit=request.row_limit,
        selected_row_count=selected_count,
        source_declared_row_count=source_declared_row_count,
        first_selected_source_row=first_row_number,
        last_selected_source_row=last_row_number,
        source_column_count=len(fieldnames),
        source_artifact_path=str(artifact["artifact_path"]),
        source_artifact_sha256=str(artifact["artifact_sha256"]),
        preservation_status=PRESERVATION_STATUS_COMPLETE_PENDING_VALIDATION,
    )


def ordered_source_values_json(
    fieldnames: Sequence[str],
    row: dict[str, str | None],
) -> str:
    """Serialize all source values with explicit producer column order."""
    return json.dumps(
        [row.get(field) if row.get(field) is not None else "" for field in fieldnames],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def raw_source_row_hash(raw_source_values_json: str) -> str:
    """Return a deterministic hash for the preserved ordered source values."""
    return hashlib.sha256(raw_source_values_json.encode("utf-8")).hexdigest()


def _iter_selected_rows(
    reader: csv.DictReader,
    row_limit: int | None,
) -> Iterator[tuple[int, dict[str, str | None]]]:
    for row_number, row in enumerate(reader, start=1):
        if row_limit is not None and row_number > row_limit:
            break
        yield row_number, dict(row)


def _validate_header(fieldnames: Sequence[str]) -> None:
    if not fieldnames:
        raise ValueError("Genotype observation artifact has no header")
    if len(set(fieldnames)) != len(fieldnames):
        raise ValueError("Genotype observation artifact contains duplicate columns")
    missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in fieldnames]
    if missing:
        raise ValueError(
            "Genotype observation artifact is missing required fields: "
            + ",".join(missing)
        )


def _build_observation_record(
    *,
    package_id: str,
    preservation_scope_id: str,
    source_row_number: int,
    fieldnames: Sequence[str],
    row: dict[str, str | None],
) -> dict[str, object]:
    genotype_observation_id = (row.get("genotype_observation_id") or "").strip()
    if not genotype_observation_id:
        raise ValueError(
            f"Missing genotype_observation_id at source row {source_row_number}"
        )

    raw_values = ordered_source_values_json(fieldnames, row)
    record: dict[str, object] = {
        "source_genotype_observation_persistence_id": (
            source_genotype_observation_persistence_id(
                package_id=package_id,
                preservation_scope_id=preservation_scope_id,
                genotype_observation_id=genotype_observation_id,
            )
        ),
        "package_id": package_id,
        "preservation_scope_id": preservation_scope_id,
        "source_row_number": source_row_number,
        "genotype_observation_id": genotype_observation_id,
        "raw_source_row_hash": raw_source_row_hash(raw_values),
        "raw_source_values_json": raw_values,
    }
    for field in TYPED_SOURCE_FIELDS:
        record[field] = row.get(field)
    return record


def _load_classification(
    connection: sqlite3.Connection,
    package_id: str,
) -> dict[str, object]:
    row = connection.execute(
        """
        SELECT *
        FROM source_genotype_package_classifications
        WHERE package_id = ?
        """,
        (package_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"No genotype package classification for {package_id}")
    return dict(row)


def _require_preservation_eligible_classification(
    classification: dict[str, object],
) -> None:
    expected = {
        "producer_family": "VAP",
        "producer_genotype_applicability_state": (
            "genotype_applicable_to_producer_type"
        ),
        "genotype_capability_state": "genotype_capability_available",
        "genotype_maturity_state": "genotype_discovered",
        "classification_status": "classified",
        "trusted_modern_ingestion_ready": 1,
    }
    mismatches = {
        key: (expected_value, classification.get(key))
        for key, expected_value in expected.items()
        if classification.get(key) != expected_value
    }
    if mismatches:
        raise ValueError(
            "Package is not eligible for trusted genotype preservation: "
            + json.dumps(mismatches, sort_keys=True)
        )


def _load_package_path(connection: sqlite3.Connection, package_id: str) -> str:
    row = connection.execute(
        "SELECT package_path FROM tep_packages WHERE package_id = ?",
        (package_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"No package inventory row for {package_id}")
    return str(row[0])


def _load_genotype_observation_artifact(
    connection: sqlite3.Connection,
    package_id: str,
) -> dict[str, object]:
    row = connection.execute(
        """
        SELECT
            genotype_index.artifact_id,
            genotype_index.artifact_path,
            genotype_index.artifact_sha256,
            genotype_index.artifact_present,
            genotype_index.schema_version,
            genotype_index.parse_status,
            inventory.relative_path AS inventory_relative_path,
            inventory.sha256 AS inventory_sha256
        FROM source_genotype_artifact_index AS genotype_index
        LEFT JOIN artifacts AS inventory
          ON inventory.artifact_id = genotype_index.artifact_id
        WHERE genotype_index.package_id = ?
          AND genotype_index.artifact_role = ?
        """,
        (package_id, GENOTYPE_OBSERVATIONS_ROLE),
    ).fetchone()
    if row is None:
        raise ValueError("Genotype observation artifact index row is missing")
    record = dict(row)
    if int(record["artifact_present"]) != 1:
        raise ValueError("Genotype observation artifact is not present")
    if record["artifact_path"] != record["inventory_relative_path"]:
        raise ValueError("Genotype observation artifact path does not reconcile")
    if record["artifact_sha256"] != record["inventory_sha256"]:
        raise ValueError("Genotype observation artifact checksum does not reconcile")
    if record["schema_version"] != "genotype_observation_v1":
        raise ValueError("Unsupported genotype observation schema version")
    if record["parse_status"] != "header_parsed":
        raise ValueError("Genotype observation artifact header did not parse")
    return record


def _load_source_declared_row_count(
    connection: sqlite3.Connection,
    package_id: str,
) -> int | None:
    row = connection.execute(
        """
        SELECT genotype_observation_row_count
        FROM source_genotype_context_index
        WHERE package_id = ?
          AND context_kind = 'genotype_projection_summary'
        """,
        (package_id,),
    ).fetchone()
    if row is None or row[0] is None:
        return None
    return int(row[0])

"""VAP coordinate declaration extraction.

Coordinate declarations make VAP variant coordinates topology-ready without
performing namespace resolution, variant normalization, or biological
interpretation.

This module is producer-scoped. Non-VAP producers should not call it, and the
registration orchestrator treats it as an optional VAP-only substrate.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Mapping

from variant_database.persistence.repositories import stable_hash
from variant_database.registration.participant_extractor import (
    ExtractedParticipant,
    extract_vap_variant_participants_from_row,
)
from variant_database.registration.source_identity import (
    source_identity_id_for_registration,
)


CHROM_COLUMNS = (
    "chrom",
    "chromosome",
    "#chrom",
    "#chromosome",
)

POSITION_COLUMNS = (
    "pos",
    "position",
    "start",
)

START_COLUMNS = (
    "start",
)

END_COLUMNS = (
    "end",
)

REF_COLUMNS = (
    "ref",
    "reference",
    "reference_allele",
)

ALT_COLUMNS = (
    "alt",
    "alternate",
    "alternative",
    "alternate_allele",
)

VARIANT_TYPE_COLUMNS = (
    "variant_type",
)

VARIANT_CLASS_COLUMNS = (
    "variant_class",
)

NULL_LIKE_VALUES = {
    "",
    ".",
    "-",
    "na",
    "n/a",
    "none",
    "null",
}


@dataclass(frozen=True)
class SourceCoordinateDeclaration:
    """Structured coordinate substrate attached to a VAP source row."""

    coordinate_declaration_id: str
    assertion_registration_id: str
    source_identity_id: str
    source_record_ref: str | None
    source_artifact_path: str
    variant_source_namespace: str
    variant_source_value: str
    variant_source_label: str | None
    reference_genome_build: str | None
    reference_context_source: str | None
    chromosome: str
    position: str
    start: str | None
    end: str | None
    reference_allele: str
    alternate_allele: str
    variant_type: str | None
    variant_class: str | None
    coordinate_system: str
    coordinate_system_status: str
    normalization_status: str
    normalization_status_source: str
    sample_id: str | None
    run_id: str | None
    producer_pipeline: str | None
    extraction_method: str
    payload_json: str


def _is_present(value: object) -> bool:
    if value is None:
        return False
    value_s = str(value).strip()
    return value_s.lower() not in NULL_LIKE_VALUES


def _first_nonempty_value(
    row: Mapping[str, object],
    columns: tuple[str, ...],
) -> tuple[str, str] | None:
    """Return the first nonempty value for any matching column."""
    normalized_lookup = {str(key).lower(): key for key in row.keys()}

    for column in columns:
        original_key = normalized_lookup.get(column.lower())
        if original_key is None:
            continue

        value = row.get(original_key)
        if not _is_present(value):
            continue

        return column, str(value).strip()

    return None


def _metadata_value(
    package_metadata: Mapping[str, object] | None,
    key: str,
) -> str | None:
    if package_metadata is None:
        return None

    value = package_metadata.get(key)
    if not _is_present(value):
        return None

    return str(value).strip()


def _normalization_status_for_artifact(source_artifact_path: str) -> tuple[str, str]:
    """Derive a conservative processing-state label from a VAP artifact path."""
    normalized = source_artifact_path.replace("\\", "/").lower()

    if "entities/observation/" in normalized:
        return "source_observed", "artifact_path"
    if normalized.endswith("stage_08_vdb_ready_variants.tsv"):
        return "vdb_ready", "artifact_path"
    if normalized.endswith("stage_08_selected_transcript_consequences.tsv"):
        return "selected_transcript_consequence", "artifact_path"
    if "entities/coding_interpretation/" in normalized:
        return "coding_interpreted", "artifact_path"
    if "entities/noncoding_interpretation/" in normalized:
        return "noncoding_interpreted", "artifact_path"
    if normalized.endswith("coding_candidates.tsv"):
        return "coding_candidate", "artifact_path"
    if normalized.endswith("noncoding_candidates.tsv"):
        return "noncoding_candidate", "artifact_path"
    if normalized.endswith("splice_region_candidates.tsv"):
        return "splice_region_candidate", "artifact_path"
    if "entities/prioritization/" in normalized:
        return "prioritized_variant", "artifact_path"
    if "entities/validation/" in normalized:
        return "validation_candidate", "artifact_path"

    return "unknown", "artifact_path"


def coordinate_declaration_id_for_registration(
    assertion_registration_id: str,
    source_record_ref: str | None,
    variant_source_namespace: str,
    variant_source_value: str,
    reference_genome_build: str | None,
    chromosome: str,
    position: str,
    reference_allele: str,
    alternate_allele: str,
) -> str:
    """Derive a deterministic coordinate declaration ID."""
    return stable_hash(
        [
            "source_coordinate_declaration",
            assertion_registration_id,
            source_record_ref or "",
            variant_source_namespace,
            variant_source_value,
            reference_genome_build or "",
            chromosome,
            position,
            reference_allele,
            alternate_allele,
        ]
    )


def _variant_identity_for_row(
    assertion_registration_id: str,
    row: Mapping[str, object],
    source_record_ref: str | None,
) -> ExtractedParticipant | None:
    """Return the VAP variant participant used as coordinate identity anchor."""
    variant_participants = extract_vap_variant_participants_from_row(
        row=row,
        source_record_ref=source_record_ref,
    )

    if not variant_participants:
        return None

    return variant_participants[0]


def build_vap_coordinate_declaration_from_row(
    assertion_registration_id: str,
    row: Mapping[str, object],
    source_record_ref: str | None,
    source_artifact_path: str,
    package_metadata: Mapping[str, object] | None = None,
) -> SourceCoordinateDeclaration | None:
    """Build a VAP coordinate declaration from one source row.

    A declaration is emitted only when the row carries a complete coordinate
    tuple and a VAP variant source identity can be derived. Partial coordinates
    are intentionally not emitted in v1.
    """
    variant = _variant_identity_for_row(
        assertion_registration_id=assertion_registration_id,
        row=row,
        source_record_ref=source_record_ref,
    )
    if variant is None:
        return None

    chrom = _first_nonempty_value(row, CHROM_COLUMNS)
    position = _first_nonempty_value(row, POSITION_COLUMNS)
    reference = _first_nonempty_value(row, REF_COLUMNS)
    alternate = _first_nonempty_value(row, ALT_COLUMNS)

    if chrom is None or position is None or reference is None or alternate is None:
        return None

    chrom_column, chromosome = chrom
    position_column, position_value = position
    ref_column, reference_allele = reference
    alt_column, alternate_allele = alternate

    start = _first_nonempty_value(row, START_COLUMNS)
    end = _first_nonempty_value(row, END_COLUMNS)
    variant_type = _first_nonempty_value(row, VARIANT_TYPE_COLUMNS)
    variant_class = _first_nonempty_value(row, VARIANT_CLASS_COLUMNS)

    reference_genome_build = _metadata_value(package_metadata, "reference_genome_build")
    reference_context_source = _metadata_value(package_metadata, "metadata_artifact_path")
    sample_id = _metadata_value(package_metadata, "sample_id")
    run_id = _metadata_value(package_metadata, "run_id")
    producer_pipeline = _metadata_value(package_metadata, "pipeline_name")

    source_identity_id = source_identity_id_for_registration(
        assertion_registration_id=assertion_registration_id,
        identity_kind=variant.participant_kind,
        participant_role=variant.participant_role,
        source_value=variant.source_value,
        source_namespace=variant.source_namespace,
        source_record_ref=source_record_ref,
    )

    normalization_status, normalization_status_source = _normalization_status_for_artifact(
        source_artifact_path
    )

    coordinate_declaration_id = coordinate_declaration_id_for_registration(
        assertion_registration_id=assertion_registration_id,
        source_record_ref=source_record_ref,
        variant_source_namespace=variant.source_namespace,
        variant_source_value=variant.source_value,
        reference_genome_build=reference_genome_build,
        chromosome=chromosome,
        position=position_value,
        reference_allele=reference_allele,
        alternate_allele=alternate_allele,
    )

    payload = {
        "source": "vap_coordinate_declaration",
        "coordinate_columns": {
            "chromosome": chrom_column,
            "position": position_column,
            "reference_allele": ref_column,
            "alternate_allele": alt_column,
        },
        "metadata_context_status": (
            "reference_context_attached"
            if reference_genome_build is not None
            else "reference_context_missing"
        ),
        "annotation_assembly": _metadata_value(package_metadata, "annotation_assembly"),
        "annotation_engine": _metadata_value(package_metadata, "annotation_engine"),
    }

    return SourceCoordinateDeclaration(
        coordinate_declaration_id=coordinate_declaration_id,
        assertion_registration_id=assertion_registration_id,
        source_identity_id=source_identity_id,
        source_record_ref=source_record_ref,
        source_artifact_path=source_artifact_path,
        variant_source_namespace=variant.source_namespace,
        variant_source_value=variant.source_value,
        variant_source_label=variant.source_label,
        reference_genome_build=reference_genome_build,
        reference_context_source=reference_context_source,
        chromosome=chromosome,
        position=position_value,
        start=start[1] if start is not None else None,
        end=end[1] if end is not None else None,
        reference_allele=reference_allele,
        alternate_allele=alternate_allele,
        variant_type=variant_type[1] if variant_type is not None else None,
        variant_class=variant_class[1] if variant_class is not None else None,
        coordinate_system="vcf_style",
        coordinate_system_status="inferred_from_vap_variant_fields",
        normalization_status=normalization_status,
        normalization_status_source=normalization_status_source,
        sample_id=sample_id,
        run_id=run_id,
        producer_pipeline=producer_pipeline,
        extraction_method="vap_row_coordinate_columns_with_package_metadata",
        payload_json=json.dumps(payload, sort_keys=True),
    )

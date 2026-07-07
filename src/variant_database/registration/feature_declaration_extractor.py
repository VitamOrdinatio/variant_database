"""VAP feature declaration extraction.

Feature declarations make VAP annotation and surveillance context
registration-visible without performing namespace mediation or biological
interpretation.

This module is producer-scoped. Non-VAP producers should not call it, and the
registration orchestrator treats it as an optional VAP-only substrate.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Mapping

from variant_database.persistence.repositories import stable_hash
from variant_database.registration.coordinate_extractor import SourceCoordinateDeclaration
from variant_database.registration.participant_extractor import (
    ExtractedParticipant,
    extract_vap_variant_participants_from_row,
)
from variant_database.registration.source_identity import (
    source_identity_id_for_registration,
)


TRANSCRIPT_ID_COLUMNS = (
    "transcript_id",
    "transcript",
    "feature_id",
)

CONSEQUENCE_COLUMNS = (
    "consequence",
    "variant_consequence",
    "most_severe_consequence",
)

IMPACT_CLASS_COLUMNS = (
    "impact_class",
    "impact",
)

FUNCTIONAL_IMPACT_COLUMNS = (
    "functional_impact",
)

VARIANT_CONTEXT_COLUMNS = (
    "variant_context",
    "coding_noncoding_context",
    "coding_status",
)

GENE_MAPPING_STATUS_COLUMNS = (
    "gene_mapping_status",
)

REGULATORY_CANDIDATE_COLUMNS = (
    "is_regulatory_candidate",
    "regulatory_candidate",
)

SPLICE_REGION_CANDIDATE_COLUMNS = (
    "is_splice_region_candidate",
    "splice_region_candidate",
)

GENE_ID_COLUMNS = (
    "gene_id",
    "ensembl_gene_id",
    "ensembl_id",
)

GENE_SYMBOL_COLUMNS = (
    "gene_symbol",
    "symbol",
    "gene",
)

ANNOTATION_SOURCE_COLUMNS = (
    "annotation_source",
)

ANNOTATION_VERSION_COLUMNS = (
    "annotation_version",
)

CLINICAL_ANNOTATION_COLUMNS = (
    "clinvar_significance",
    "clinvar_clinical_significance",
    "clinical_significance",
    "clinvar_id",
    "clinvar_variation_id",
)

NULL_LIKE_VALUES = {
    "",
    ".",
    "-",
    "na",
    "n/a",
    "none",
    "null",
    "unknown",
}

TRUE_LIKE_VALUES = {
    "1",
    "t",
    "true",
    "y",
    "yes",
}

NONCODING_TOKENS = (
    "noncoding",
    "non_coding",
    "intergenic",
    "intronic",
    "intron",
    "utr",
    "upstream",
    "downstream",
    "regulatory",
)


@dataclass(frozen=True)
class SourceFeatureDeclaration:
    """Feature or surveillance declaration attached to a VAP source row."""

    feature_declaration_id: str
    assertion_registration_id: str
    coordinate_declaration_id: str | None
    source_identity_id: str | None
    source_record_ref: str | None
    source_artifact_path: str
    variant_source_namespace: str | None
    variant_source_value: str | None
    feature_kind: str
    feature_namespace: str
    feature_value: str
    feature_label: str | None
    relationship_type: str
    relationship_status: str
    gene_id: str | None
    gene_symbol: str | None
    gene_mapping_status: str | None
    transcript_id: str | None
    consequence: str | None
    impact: str | None
    impact_class: str | None
    functional_impact: str | None
    variant_context: str | None
    is_regulatory_candidate: str | None
    is_splice_region_candidate: str | None
    annotation_source: str | None
    annotation_version: str | None
    annotation_assembly: str | None
    reference_genome_build: str | None
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


def _is_true_like(value: object) -> bool:
    if value is None:
        return False
    return str(value).strip().lower() in TRUE_LIKE_VALUES


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


def _has_any_column(row: Mapping[str, object], columns: tuple[str, ...]) -> bool:
    normalized = {str(key).lower() for key in row.keys()}
    return any(column.lower() in normalized for column in columns)


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


def _variant_identity_for_row(
    row: Mapping[str, object],
    source_record_ref: str | None,
) -> ExtractedParticipant | None:
    variant_participants = extract_vap_variant_participants_from_row(
        row=row,
        source_record_ref=source_record_ref,
    )

    if not variant_participants:
        return None

    return variant_participants[0]


def feature_declaration_id_for_registration(
    assertion_registration_id: str,
    source_record_ref: str | None,
    variant_source_namespace: str | None,
    variant_source_value: str | None,
    coordinate_declaration_id: str | None,
    feature_kind: str,
    feature_namespace: str,
    feature_value: str,
    relationship_type: str,
    annotation_source: str | None,
    annotation_version: str | None,
) -> str:
    """Derive a deterministic feature declaration ID."""
    return stable_hash(
        [
            "source_feature_declaration",
            assertion_registration_id,
            source_record_ref or "",
            variant_source_namespace or "",
            variant_source_value or "",
            coordinate_declaration_id or "",
            feature_kind,
            feature_namespace,
            feature_value,
            relationship_type,
            annotation_source or "",
            annotation_version or "",
        ]
    )


def _noncoding_context_observed(
    source_artifact_path: str,
    consequence: str | None,
    variant_context: str | None,
) -> bool:
    haystack = " ".join(
        value.lower()
        for value in (
            source_artifact_path.replace("\\", "/"),
            consequence or "",
            variant_context or "",
        )
    )
    return any(token in haystack for token in NONCODING_TOKENS)


def _intergenic_context_observed(
    consequence: str | None,
    variant_context: str | None,
) -> bool:
    haystack = " ".join((consequence or "", variant_context or "")).lower()
    return "intergenic" in haystack


def _make_declaration(
    *,
    assertion_registration_id: str,
    coordinate_declaration_id: str | None,
    source_identity_id: str | None,
    source_record_ref: str | None,
    source_artifact_path: str,
    variant_source_namespace: str | None,
    variant_source_value: str | None,
    feature_kind: str,
    feature_namespace: str,
    feature_value: str,
    relationship_type: str,
    relationship_status: str,
    source_column: str | None,
    row_context: Mapping[str, str | None],
    package_metadata: Mapping[str, object] | None,
) -> SourceFeatureDeclaration:
    annotation_source = row_context["annotation_source"]
    annotation_version = row_context["annotation_version"]
    annotation_assembly = _metadata_value(package_metadata, "annotation_assembly")
    reference_genome_build = _metadata_value(package_metadata, "reference_genome_build")

    feature_declaration_id = feature_declaration_id_for_registration(
        assertion_registration_id=assertion_registration_id,
        source_record_ref=source_record_ref,
        variant_source_namespace=variant_source_namespace,
        variant_source_value=variant_source_value,
        coordinate_declaration_id=coordinate_declaration_id,
        feature_kind=feature_kind,
        feature_namespace=feature_namespace,
        feature_value=feature_value,
        relationship_type=relationship_type,
        annotation_source=annotation_source,
        annotation_version=annotation_version,
    )

    payload = {
        "source": "vap_feature_declaration",
        "source_column": source_column,
        "source_artifact_path": source_artifact_path,
        "coordinate_linkage_status": (
            "linked_to_coordinate_declaration"
            if coordinate_declaration_id is not None
            else "coordinate_declaration_not_available"
        ),
    }

    return SourceFeatureDeclaration(
        feature_declaration_id=feature_declaration_id,
        assertion_registration_id=assertion_registration_id,
        coordinate_declaration_id=coordinate_declaration_id,
        source_identity_id=source_identity_id,
        source_record_ref=source_record_ref,
        source_artifact_path=source_artifact_path,
        variant_source_namespace=variant_source_namespace,
        variant_source_value=variant_source_value,
        feature_kind=feature_kind,
        feature_namespace=feature_namespace,
        feature_value=feature_value,
        feature_label=feature_value,
        relationship_type=relationship_type,
        relationship_status=relationship_status,
        gene_id=row_context["gene_id"],
        gene_symbol=row_context["gene_symbol"],
        gene_mapping_status=row_context["gene_mapping_status"],
        transcript_id=row_context["transcript_id"],
        consequence=row_context["consequence"],
        impact=row_context["impact"],
        impact_class=row_context["impact_class"],
        functional_impact=row_context["functional_impact"],
        variant_context=row_context["variant_context"],
        is_regulatory_candidate=row_context["is_regulatory_candidate"],
        is_splice_region_candidate=row_context["is_splice_region_candidate"],
        annotation_source=annotation_source,
        annotation_version=annotation_version,
        annotation_assembly=annotation_assembly,
        reference_genome_build=reference_genome_build,
        sample_id=_metadata_value(package_metadata, "sample_id"),
        run_id=_metadata_value(package_metadata, "run_id"),
        producer_pipeline=_metadata_value(package_metadata, "pipeline_name"),
        extraction_method="vap_row_feature_declaration_with_package_metadata",
        payload_json=json.dumps(payload, sort_keys=True),
    )


def build_vap_feature_declarations_from_row(
    assertion_registration_id: str,
    row: Mapping[str, object],
    source_record_ref: str | None,
    source_artifact_path: str,
    package_metadata: Mapping[str, object] | None = None,
    coordinate_declaration: SourceCoordinateDeclaration | None = None,
) -> list[SourceFeatureDeclaration]:
    """Build VAP feature/surveillance declarations from one source row.

    False-like candidate flags are intentionally skipped. Meaningful absence
    states for noncoding and unannotated coordinate-bearing surveillance are
    preserved as compact annotation-status declarations.
    """
    variant_namespace: str | None = None
    variant_value: str | None = None
    source_identity_id: str | None = None
    coordinate_declaration_id: str | None = None

    if coordinate_declaration is not None:
        variant_namespace = coordinate_declaration.variant_source_namespace
        variant_value = coordinate_declaration.variant_source_value
        source_identity_id = coordinate_declaration.source_identity_id
        coordinate_declaration_id = coordinate_declaration.coordinate_declaration_id
    else:
        variant = _variant_identity_for_row(row, source_record_ref)
        if variant is not None:
            variant_namespace = variant.source_namespace
            variant_value = variant.source_value
            source_identity_id = source_identity_id_for_registration(
                assertion_registration_id=assertion_registration_id,
                identity_kind=variant.participant_kind,
                participant_role=variant.participant_role,
                source_value=variant.source_value,
                source_namespace=variant.source_namespace,
                source_record_ref=source_record_ref,
            )

    transcript = _first_nonempty_value(row, TRANSCRIPT_ID_COLUMNS)
    consequence = _first_nonempty_value(row, CONSEQUENCE_COLUMNS)
    impact_class = _first_nonempty_value(row, IMPACT_CLASS_COLUMNS)
    functional_impact = _first_nonempty_value(row, FUNCTIONAL_IMPACT_COLUMNS)
    variant_context = _first_nonempty_value(row, VARIANT_CONTEXT_COLUMNS)
    gene_mapping_status = _first_nonempty_value(row, GENE_MAPPING_STATUS_COLUMNS)
    regulatory_candidate = _first_nonempty_value(row, REGULATORY_CANDIDATE_COLUMNS)
    splice_candidate = _first_nonempty_value(row, SPLICE_REGION_CANDIDATE_COLUMNS)
    gene_id = _first_nonempty_value(row, GENE_ID_COLUMNS)
    gene_symbol = _first_nonempty_value(row, GENE_SYMBOL_COLUMNS)
    annotation_source = _first_nonempty_value(row, ANNOTATION_SOURCE_COLUMNS)
    annotation_version = _first_nonempty_value(row, ANNOTATION_VERSION_COLUMNS)

    row_context: dict[str, str | None] = {
        "gene_id": gene_id[1] if gene_id is not None else None,
        "gene_symbol": gene_symbol[1] if gene_symbol is not None else None,
        "gene_mapping_status": (
            gene_mapping_status[1] if gene_mapping_status is not None else None
        ),
        "transcript_id": transcript[1] if transcript is not None else None,
        "consequence": consequence[1] if consequence is not None else None,
        "impact": impact_class[1] if impact_class is not None and impact_class[0] == "impact" else None,
        "impact_class": (
            impact_class[1]
            if impact_class is not None and impact_class[0] == "impact_class"
            else None
        ),
        "functional_impact": (
            functional_impact[1] if functional_impact is not None else None
        ),
        "variant_context": variant_context[1] if variant_context is not None else None,
        "is_regulatory_candidate": (
            regulatory_candidate[1] if regulatory_candidate is not None else None
        ),
        "is_splice_region_candidate": (
            splice_candidate[1] if splice_candidate is not None else None
        ),
        "annotation_source": (
            annotation_source[1] if annotation_source is not None else None
        ),
        "annotation_version": (
            annotation_version[1] if annotation_version is not None else None
        ),
    }

    declarations: list[SourceFeatureDeclaration] = []

    def add(
        *,
        feature_kind: str,
        feature_namespace: str,
        feature_value: str,
        relationship_type: str,
        relationship_status: str = "declared",
        source_column: str | None = None,
    ) -> None:
        declarations.append(
            _make_declaration(
                assertion_registration_id=assertion_registration_id,
                coordinate_declaration_id=coordinate_declaration_id,
                source_identity_id=source_identity_id,
                source_record_ref=source_record_ref,
                source_artifact_path=source_artifact_path,
                variant_source_namespace=variant_namespace,
                variant_source_value=variant_value,
                feature_kind=feature_kind,
                feature_namespace=feature_namespace,
                feature_value=feature_value,
                relationship_type=relationship_type,
                relationship_status=relationship_status,
                source_column=source_column,
                row_context=row_context,
                package_metadata=package_metadata,
            )
        )

    if transcript is not None:
        add(
            feature_kind="transcript_annotation",
            feature_namespace="vap_transcript_id",
            feature_value=transcript[1],
            relationship_type="assigned_to_transcript",
            source_column=transcript[0],
        )

    if consequence is not None:
        add(
            feature_kind="sequence_consequence",
            feature_namespace="vap_consequence",
            feature_value=consequence[1],
            relationship_type="has_consequence",
            source_column=consequence[0],
        )

    if impact_class is not None:
        namespace = "vap_impact_class" if impact_class[0] == "impact_class" else "vap_impact"
        add(
            feature_kind="impact_class",
            feature_namespace=namespace,
            feature_value=impact_class[1],
            relationship_type="has_impact_class",
            source_column=impact_class[0],
        )

    if functional_impact is not None:
        add(
            feature_kind="functional_impact",
            feature_namespace="vap_functional_impact",
            feature_value=functional_impact[1],
            relationship_type="has_functional_impact",
            source_column=functional_impact[0],
        )

    if variant_context is not None:
        add(
            feature_kind="variant_context",
            feature_namespace="vap_variant_context",
            feature_value=variant_context[1],
            relationship_type="has_variant_context",
            source_column=variant_context[0],
        )

    if gene_mapping_status is not None:
        add(
            feature_kind="gene_mapping_status",
            feature_namespace="vap_gene_mapping_status",
            feature_value=gene_mapping_status[1],
            relationship_type="has_gene_mapping_status",
            source_column=gene_mapping_status[0],
        )

    if regulatory_candidate is not None and _is_true_like(regulatory_candidate[1]):
        add(
            feature_kind="regulatory_candidate",
            feature_namespace="vap_regulatory_candidate",
            feature_value="true",
            relationship_type="flagged_as_regulatory_candidate",
            source_column=regulatory_candidate[0],
        )

    source_artifact_path_normalized = source_artifact_path.replace("\\", "/").lower()
    splice_artifact_context = source_artifact_path_normalized.endswith(
        "splice_region_candidates.tsv"
    )
    if (splice_candidate is not None and _is_true_like(splice_candidate[1])) or splice_artifact_context:
        add(
            feature_kind="splice_region_candidate",
            feature_namespace="vap_splice_region_candidate",
            feature_value="true",
            relationship_type="flagged_as_splice_region_candidate",
            source_column=splice_candidate[0] if splice_candidate is not None else "artifact_path",
        )

    consequence_value = row_context["consequence"]
    variant_context_value = row_context["variant_context"]

    if _noncoding_context_observed(
        source_artifact_path=source_artifact_path,
        consequence=consequence_value,
        variant_context=variant_context_value,
    ):
        add(
            feature_kind="annotation_status",
            feature_namespace="vap_annotation_status",
            feature_value="noncoding_coordinate_surveillance",
            relationship_type="has_annotation_status",
            relationship_status="surveillance_context",
            source_column="artifact_path_or_annotation_context",
        )

    if _intergenic_context_observed(consequence_value, variant_context_value):
        add(
            feature_kind="annotation_status",
            feature_namespace="vap_annotation_status",
            feature_value="intergenic_coordinate_surveillance",
            relationship_type="has_annotation_status",
            relationship_status="surveillance_context",
            source_column="consequence_or_variant_context",
        )

    positive_annotation_observed = any(
        value is not None
        for value in (
            transcript,
            consequence,
            impact_class,
            functional_impact,
            variant_context,
        )
    )
    if coordinate_declaration is not None and not positive_annotation_observed:
        add(
            feature_kind="annotation_status",
            feature_namespace="vap_annotation_status",
            feature_value="unannotated_coordinate_surveillance",
            relationship_type="has_annotation_status",
            relationship_status="surveillance_context",
            source_column="coordinate_without_positive_annotation",
        )

    gene_mapping_absent = gene_id is None and gene_symbol is None
    if (
        coordinate_declaration is not None
        and gene_mapping_absent
        and (
            _has_any_column(row, GENE_ID_COLUMNS + GENE_SYMBOL_COLUMNS)
            or _intergenic_context_observed(consequence_value, variant_context_value)
            or (gene_mapping_status is not None and "no" in gene_mapping_status[1].lower())
            or (gene_mapping_status is not None and "unmapped" in gene_mapping_status[1].lower())
        )
    ):
        add(
            feature_kind="annotation_status",
            feature_namespace="vap_annotation_status",
            feature_value="no_gene_mapping_observed",
            relationship_type="has_annotation_status",
            relationship_status="surveillance_context",
            source_column="gene_columns_or_mapping_status",
        )

    if (
        coordinate_declaration is not None
        and transcript is None
        and _has_any_column(row, TRANSCRIPT_ID_COLUMNS)
    ):
        add(
            feature_kind="annotation_status",
            feature_namespace="vap_annotation_status",
            feature_value="no_transcript_annotation_observed",
            relationship_type="has_annotation_status",
            relationship_status="surveillance_context",
            source_column="transcript_columns",
        )

    if (
        coordinate_declaration is not None
        and _has_any_column(row, CLINICAL_ANNOTATION_COLUMNS)
        and _first_nonempty_value(row, CLINICAL_ANNOTATION_COLUMNS) is None
    ):
        add(
            feature_kind="clinical_annotation_status",
            feature_namespace="vap_clinical_annotation_status",
            feature_value="no_clinical_annotation_observed",
            relationship_type="has_clinical_annotation_status",
            relationship_status="surveillance_context",
            source_column="clinical_annotation_columns",
        )

    # Remove exact duplicate declarations produced by overlapping rules.
    deduplicated: dict[str, SourceFeatureDeclaration] = {}
    for declaration in declarations:
        deduplicated[declaration.feature_declaration_id] = declaration

    return list(deduplicated.values())

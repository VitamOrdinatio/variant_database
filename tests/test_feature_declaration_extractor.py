from __future__ import annotations

import json

from variant_database.registration.coordinate_extractor import (
    build_vap_coordinate_declaration_from_row,
)
from variant_database.registration.feature_declaration_extractor import (
    build_vap_feature_declarations_from_row,
)


def _metadata() -> dict[str, object]:
    return {
        "metadata_artifact_path": "entities/metadata/config_snapshot.yaml",
        "reference_genome_build": "GRCh38",
        "annotation_engine": "vep",
        "annotation_assembly": "GRCh38",
        "sample_id": "HG002",
        "run_id": "run_2026_06_03_010030",
        "pipeline_name": "variant_annotation_pipeline",
    }


def _coordinate(row: dict[str, object]):
    return build_vap_coordinate_declaration_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
    )


def test_build_vap_feature_declarations_extracts_positive_annotation_features() -> None:
    row = {
        "variant_id": "15:89333596:T:TTGC",
        "chromosome": "15",
        "position": "89333596",
        "reference_allele": "T",
        "alternate_allele": "TTGC",
        "transcript_id": "ENST00000268124",
        "consequence": "frameshift_variant",
        "impact_class": "HIGH",
        "functional_impact": "loss_of_function_candidate",
        "variant_context": "coding",
        "gene_mapping_status": "mapped",
        "gene_id": "ENSG00000140521",
        "gene_symbol": "POLG",
        "annotation_source": "VEP",
        "annotation_version": "source_configured",
    }
    coordinate = _coordinate(row)
    assert coordinate is not None

    declarations = build_vap_feature_declarations_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
        coordinate_declaration=coordinate,
    )

    by_kind = {(d.feature_kind, d.feature_value): d for d in declarations}

    assert ("transcript_annotation", "ENST00000268124") in by_kind
    assert ("sequence_consequence", "frameshift_variant") in by_kind
    assert ("impact_class", "HIGH") in by_kind
    assert ("functional_impact", "loss_of_function_candidate") in by_kind
    assert ("variant_context", "coding") in by_kind
    assert ("gene_mapping_status", "mapped") in by_kind

    transcript = by_kind[("transcript_annotation", "ENST00000268124")]
    assert transcript.coordinate_declaration_id == coordinate.coordinate_declaration_id
    assert transcript.source_identity_id == coordinate.source_identity_id
    assert transcript.variant_source_value == "15:89333596:T:TTGC"
    assert transcript.reference_genome_build == "GRCh38"
    assert transcript.annotation_assembly == "GRCh38"
    assert transcript.sample_id == "HG002"
    assert transcript.run_id == "run_2026_06_03_010030"

    payload = json.loads(transcript.payload_json)
    assert payload["coordinate_linkage_status"] == "linked_to_coordinate_declaration"


def test_build_vap_feature_declarations_skips_false_candidate_flags() -> None:
    row = {
        "variant_id": "1:100:A:G",
        "chromosome": "1",
        "position": "100",
        "reference_allele": "A",
        "alternate_allele": "G",
        "is_regulatory_candidate": "false",
        "is_splice_region_candidate": "0",
    }
    coordinate = _coordinate(row)
    assert coordinate is not None

    declarations = build_vap_feature_declarations_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
        coordinate_declaration=coordinate,
    )

    assert not any(d.feature_kind == "regulatory_candidate" for d in declarations)
    assert not any(d.feature_kind == "splice_region_candidate" for d in declarations)


def test_build_vap_feature_declarations_preserves_true_candidate_flags() -> None:
    row = {
        "variant_id": "1:100:A:G",
        "chromosome": "1",
        "position": "100",
        "reference_allele": "A",
        "alternate_allele": "G",
        "is_regulatory_candidate": "true",
        "is_splice_region_candidate": "yes",
    }
    coordinate = _coordinate(row)
    assert coordinate is not None

    declarations = build_vap_feature_declarations_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/routing/splice_region_candidates.tsv",
        package_metadata=_metadata(),
        coordinate_declaration=coordinate,
    )

    assert any(d.feature_kind == "regulatory_candidate" for d in declarations)
    assert any(d.feature_kind == "splice_region_candidate" for d in declarations)


def test_build_vap_feature_declarations_preserves_noncoding_surveillance_context() -> None:
    row = {
        "variant_id": "1:895427:G:C",
        "chromosome": "1",
        "position": "895427",
        "reference_allele": "G",
        "alternate_allele": "C",
        "gene_id": "NA",
        "gene_symbol": "NA",
        "transcript_id": "NA",
        "consequence": "intergenic_variant",
        "impact_class": "MODIFIER",
        "clinvar_significance": "NA",
    }
    coordinate = _coordinate(row)
    assert coordinate is not None

    declarations = build_vap_feature_declarations_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv",
        package_metadata=_metadata(),
        coordinate_declaration=coordinate,
    )

    status_values = {
        d.feature_value
        for d in declarations
        if d.feature_namespace in {
            "vap_annotation_status",
            "vap_clinical_annotation_status",
        }
    }

    assert "noncoding_coordinate_surveillance" in status_values
    assert "intergenic_coordinate_surveillance" in status_values
    assert "no_gene_mapping_observed" in status_values
    assert "no_transcript_annotation_observed" in status_values
    assert "no_clinical_annotation_observed" in status_values


def test_build_vap_feature_declarations_preserves_unannotated_coordinate_surveillance() -> None:
    row = {
        "variant_id": "2:200:A:T",
        "chromosome": "2",
        "position": "200",
        "reference_allele": "A",
        "alternate_allele": "T",
        "transcript_id": "NA",
        "gene_id": "NA",
        "gene_symbol": "NA",
    }
    coordinate = _coordinate(row)
    assert coordinate is not None

    declarations = build_vap_feature_declarations_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
        coordinate_declaration=coordinate,
    )

    assert any(
        d.feature_kind == "annotation_status"
        and d.feature_value == "unannotated_coordinate_surveillance"
        for d in declarations
    )

from __future__ import annotations

import json

from variant_database.registration.coordinate_extractor import (
    build_vap_coordinate_declaration_from_row,
)
from variant_database.registration.source_identity import (
    source_identity_id_for_registration,
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


def test_build_vap_coordinate_declaration_from_direct_variant_row() -> None:
    row = {
        "variant_id": "15:89333596:T:TTGC",
        "chromosome": "15",
        "position": "89333596",
        "reference_allele": "T",
        "alternate_allele": "TTGC",
        "variant_type": "INDEL",
        "variant_class": "insertion",
    }

    declaration = build_vap_coordinate_declaration_from_row(
        assertion_registration_id="ar1",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
    )

    assert declaration is not None
    assert declaration.variant_source_namespace == "vap_variant_id"
    assert declaration.variant_source_value == "15:89333596:T:TTGC"
    assert declaration.reference_genome_build == "GRCh38"
    assert declaration.reference_context_source == "entities/metadata/config_snapshot.yaml"
    assert declaration.chromosome == "15"
    assert declaration.position == "89333596"
    assert declaration.reference_allele == "T"
    assert declaration.alternate_allele == "TTGC"
    assert declaration.variant_type == "INDEL"
    assert declaration.variant_class == "insertion"
    assert declaration.coordinate_system == "vcf_style"
    assert declaration.coordinate_system_status == "inferred_from_vap_variant_fields"
    assert declaration.normalization_status == "vdb_ready"
    assert declaration.sample_id == "HG002"
    assert declaration.run_id == "run_2026_06_03_010030"

    expected_source_identity_id = source_identity_id_for_registration(
        assertion_registration_id="ar1",
        identity_kind="variant",
        participant_role="variant",
        source_value="15:89333596:T:TTGC",
        source_namespace="vap_variant_id",
        source_record_ref="row:1",
    )
    assert declaration.source_identity_id == expected_source_identity_id

    payload = json.loads(declaration.payload_json)
    assert payload["metadata_context_status"] == "reference_context_attached"
    assert payload["annotation_assembly"] == "GRCh38"


def test_build_vap_coordinate_declaration_constructs_variant_key_when_needed() -> None:
    row = {
        "chromosome": "1",
        "position": "895427",
        "reference_allele": "G",
        "alternate_allele": "C",
    }

    declaration = build_vap_coordinate_declaration_from_row(
        assertion_registration_id="ar2",
        row=row,
        source_record_ref="row:7",
        source_artifact_path="entities/observation/HG002.annotated_variants.tsv",
        package_metadata=_metadata(),
    )

    assert declaration is not None
    assert declaration.variant_source_namespace == "vap_constructed_variant_key"
    assert declaration.variant_source_value == "1:895427:G:C"
    assert declaration.normalization_status == "source_observed"


def test_build_vap_coordinate_declaration_requires_complete_coordinate_tuple() -> None:
    row = {
        "variant_id": "1:895427:G:C",
        "chromosome": "1",
        "position": "895427",
        "reference_allele": "G",
    }

    declaration = build_vap_coordinate_declaration_from_row(
        assertion_registration_id="ar3",
        row=row,
        source_record_ref="row:9",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=_metadata(),
    )

    assert declaration is None


def test_build_vap_coordinate_declaration_allows_missing_metadata_context() -> None:
    row = {
        "variant_id": "1:895427:G:C",
        "chromosome": "1",
        "position": "895427",
        "reference_allele": "G",
        "alternate_allele": "C",
    }

    declaration = build_vap_coordinate_declaration_from_row(
        assertion_registration_id="ar4",
        row=row,
        source_record_ref="row:1",
        source_artifact_path="entities/normalization/stage_08_vdb_ready_variants.tsv",
        package_metadata=None,
    )

    assert declaration is not None
    assert declaration.reference_genome_build is None
    assert declaration.reference_context_source is None
    payload = json.loads(declaration.payload_json)
    assert payload["metadata_context_status"] == "reference_context_missing"

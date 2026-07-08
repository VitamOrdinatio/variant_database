"""Tests for coordinate/feature declaration-set topology handle preservation."""
from __future__ import annotations

import csv
from pathlib import Path

from variant_database.phase4.evidence_topology.outputs import write_topology_outputs
from variant_database.phase4.evidence_topology.policy import failed_checks, preflight_policy
from variant_database.phase4.evidence_topology.relationships import (
    COORDINATE_DECLARATION_SET_MEMBER_TYPE,
    FEATURE_DECLARATION_SET_MEMBER_TYPE,
    execute_relationship_families,
)


V2_POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v2.json"
)


def _policy() -> dict:
    return {
        "policy_identity": {
            "topology_build_id": "test_topology_build",
            "input_corpus_generation_id": "test_corpus",
        },
        "topology_build_defaults": {
            "topology_build_id": "test_topology_build",
            "input_corpus_generation_id": "test_corpus",
            "topology_derivation_policy_id": "test_policy",
            "topology_derivation_policy_version": "vtest",
            "output_dir": "unused",
        },
        "deterministic_identity_rules": {"relationship_id_prefix": "topology_rel_"},
        "relationship_strategy_profiles": {
            "coordinate_declaration_set_membership": {
                "relationship_scope": "coordinate_declaration_set",
                "member_strategy": "coordinate_declaration_sets_grouped_by_key",
                "basis_component_strategy": "coordinate_declaration_set_reference",
                "emit_singleton_groups": True,
                "source_identity_expansion_status": "not_applicable",
                "statistical_testing_status": "requires_declaration_expansion",
                "namespace_mediation_status": "not_applicable",
            },
            "feature_declaration_set_membership": {
                "relationship_scope": "feature_declaration_set",
                "member_strategy": "feature_declaration_sets_grouped_by_key",
                "basis_component_strategy": "feature_declaration_set_reference",
                "emit_singleton_groups": True,
                "source_identity_expansion_status": "not_applicable",
                "statistical_testing_status": "requires_declaration_expansion",
                "namespace_mediation_status": "not_applicable",
            },
        },
        "enabled_relationship_families": [
            {
                "relationship_family_id": "coordinate_declaration_reference_build_membership",
                "strategy_profile": "coordinate_declaration_set_membership",
                "topology_dimension": "coordinate",
                "relationship_kind": "coordinate_declaration_reference_build_membership",
                "derivation_basis": "shared_reference_genome_build",
                "source_table": "assertion_record_coordinate_declaration_sets",
                "grouping_keys": ["reference_genome_build"],
            },
            {
                "relationship_family_id": "feature_declaration_kind_namespace_membership",
                "strategy_profile": "feature_declaration_set_membership",
                "topology_dimension": "feature",
                "relationship_kind": "feature_declaration_kind_namespace_membership",
                "derivation_basis": "shared_feature_kind_namespace_relationship",
                "source_table": "assertion_record_feature_declaration_sets",
                "grouping_keys": ["feature_kind", "feature_namespace", "relationship_type"],
            },
        ],
    }


def _rows_by_input() -> dict[str, list[dict[str, str]]]:
    return {
        "assertion_record_coordinate_declaration_sets": [
            {
                "coordinate_declaration_set_id": "cds1",
                "assertion_id": "ar1",
                "source_assertion_registration_id": "sar1",
                "registration_unit_id": "ru_vap",
                "coordinate_declaration_table_reference": "ru_vap:source_coordinate_declarations",
                "coordinate_declaration_filter": "assertion_registration_id=sar1;reference_genome_build=GRCh38",
                "variant_source_namespace": "vap_variant_id",
                "reference_genome_build": "GRCh38",
                "reference_context_source": "entities/metadata/config_snapshot.yaml",
                "source_artifact_path": "entities/normalization/stage_08_vdb_ready_variants.tsv",
                "normalization_status": "vdb_ready",
                "coordinate_system": "vcf_style",
                "coordinate_system_status": "inferred",
                "coordinate_declaration_count": "2",
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "coordinate_declaration_set_status": "resolved",
            }
        ],
        "assertion_record_feature_declaration_sets": [
            {
                "feature_declaration_set_id": "fds1",
                "assertion_id": "ar1",
                "source_assertion_registration_id": "sar1",
                "registration_unit_id": "ru_vap",
                "feature_declaration_table_reference": "ru_vap:source_feature_declarations",
                "feature_declaration_filter": "assertion_registration_id=sar1;feature_kind=annotation_status",
                "feature_kind": "annotation_status",
                "feature_namespace": "vap_annotation_status",
                "relationship_type": "has_annotation_status",
                "relationship_status": "declared",
                "reference_genome_build": "GRCh38",
                "annotation_source": "VEP",
                "annotation_assembly": "GRCh38",
                "source_artifact_path": "entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv",
                "feature_declaration_count": "3",
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "feature_declaration_set_status": "resolved",
            }
        ],
    }


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_v2_policy_preflight_accepts_declaration_set_vocabulary() -> None:
    result = preflight_policy(V2_POLICY_PATH)

    assert result.validation_status == "passed", failed_checks(result.checks)


def test_declaration_sets_become_topology_members_without_row_expansion() -> None:
    result = execute_relationship_families(_policy(), _rows_by_input())

    assert {member.member_type for member in result.members} == {
        COORDINATE_DECLARATION_SET_MEMBER_TYPE,
        FEATURE_DECLARATION_SET_MEMBER_TYPE,
    }
    assert {member.declaration_set_id for member in result.members} == {"cds1", "fds1"}
    assert {member.declaration_expansion_status for member in result.members} == {
        "available_by_declaration_set_reference"
    }
    assert any(
        component.basis_component_type == "coordinate_declaration_set_reference"
        for component in result.basis_components
    )
    assert any(
        component.basis_component_type == "feature_declaration_set_reference"
        for component in result.basis_components
    )


def test_declaration_set_expansion_index_preserves_handles_without_values(tmp_path: Path) -> None:
    build_result = execute_relationship_families(_policy(), _rows_by_input())
    output = write_topology_outputs(
        build_result,
        policy=_policy(),
        output_dir=tmp_path / "topology",
        build_timestamp_utc="2026-07-07T00:00:00Z",
    )

    assert output.validation_status == "passed"
    rows = _read_tsv(output.output_dir / "topology_declaration_set_expansion_index.tsv")
    assert {row["declaration_set_type"] for row in rows} == {"coordinate", "feature"}
    assert {row["declaration_set_id"] for row in rows} == {"cds1", "fds1"}
    assert {row["declaration_expansion_status"] for row in rows} == {
        "available_by_declaration_set_reference"
    }
    assert "expanded_declaration_value" not in rows[0]


def test_declaration_set_output_is_listed_in_manifest(tmp_path: Path) -> None:
    build_result = execute_relationship_families(_policy(), _rows_by_input())
    output = write_topology_outputs(
        build_result,
        policy=_policy(),
        output_dir=tmp_path / "topology",
        build_timestamp_utc="2026-07-07T00:00:00Z",
    )
    manifest_rows = _read_tsv(output.output_dir / "topology_build_manifest.tsv")

    assert "topology_declaration_set_expansion_index.tsv" in {
        row["artifact_name"] for row in manifest_rows
    }
    summary = _read_tsv(output.output_dir / "topology_summary.tsv")
    assert any(
        row["summary_group"] == "artifact_counts"
        and row["summary_key"] == "declaration_set_expansion_index_count"
        and row["summary_value"] == "2"
        for row in summary
    )

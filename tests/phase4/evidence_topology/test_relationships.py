"""Tests for conservative Evidence Topology relationship-family execution."""
from __future__ import annotations

from pathlib import Path

from variant_database.phase4.evidence_topology.policy import load_topology_policy
from variant_database.phase4.evidence_topology.relationships import (
    ASSERTION_MEMBER_TYPE,
    SOURCE_IDENTITY_SET_MEMBER_TYPE,
    build_relationship_rows,
    execute_relationship_families,
)


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)


def _minimal_policy():
    return {
        "policy_identity": {
            "topology_build_id": "test_topology_build",
            "input_corpus_generation_id": "test_corpus",
        },
        "topology_build_defaults": {
            "topology_build_id": "test_topology_build",
            "input_corpus_generation_id": "test_corpus",
        },
        "deterministic_identity_rules": {
            "relationship_id_prefix": "topology_rel_",
        },
        "relationship_strategy_profiles": {
            "assertion_metadata_membership": {
                "relationship_scope": "metadata",
                "member_strategy": "assertion_records_grouped_by_key",
                "basis_component_strategy": "field_value",
                "emit_singleton_groups": True,
                "source_identity_expansion_status": "not_required",
                "statistical_testing_status": "not_statistical_input",
                "namespace_mediation_status": "not_applicable",
            },
            "source_identity_set_membership": {
                "relationship_scope": "source_identity_set",
                "member_strategy": "source_identity_sets_grouped_by_key",
                "basis_component_strategy": "source_identity_set_reference",
                "emit_singleton_groups": True,
                "source_identity_expansion_status": "available_by_source_identity_set_reference",
                "statistical_testing_status": "requires_source_identity_expansion",
                "namespace_mediation_status": "not_applicable",
            },
            "source_identity_set_role_namespace": {
                "relationship_scope": "source_identity_set",
                "member_strategy": "source_identity_sets_grouped_by_key",
                "basis_component_strategy": "source_identity_set_reference",
                "emit_singleton_groups": True,
                "source_identity_expansion_status": "available_by_source_identity_set_reference",
                "statistical_testing_status": "requires_source_identity_expansion",
                "namespace_mediation_status": "source_namespace_only",
            },
        },
        "enabled_relationship_families": [
            {
                "relationship_family_id": "producer_family_membership",
                "strategy_profile": "assertion_metadata_membership",
                "topology_dimension": "producer",
                "relationship_kind": "producer_family_membership",
                "derivation_basis": "shared_producer_family",
                "source_table": "downstream_topology_input_manifest",
                "grouping_keys": ["producer_family"],
            },
            {
                "relationship_family_id": "source_identity_set_role_namespace_membership",
                "strategy_profile": "source_identity_set_role_namespace",
                "topology_dimension": "participant",
                "relationship_kind": "source_identity_set_role_namespace_membership",
                "derivation_basis": "shared_source_identity_set_role_kind_namespace",
                "source_table": "assertion_record_source_identity_sets",
                "grouping_keys": ["identity_kind", "participant_role", "source_namespace"],
            },
        ],
    }


def test_metadata_membership_executor_emits_relationships_members_and_basis() -> None:
    rows_by_input = {
        "downstream_topology_input_manifest": [
            {
                "assertion_id": "ar1",
                "corpus_generation_id": "test_corpus",
                "registration_unit_id": "ru1",
                "producer_family": "VAP",
            },
            {
                "assertion_id": "ar2",
                "corpus_generation_id": "test_corpus",
                "registration_unit_id": "ru2",
                "producer_family": "VAP",
            },
            {
                "assertion_id": "ar3",
                "corpus_generation_id": "test_corpus",
                "registration_unit_id": "ru3",
                "producer_family": "GSC",
            },
        ],
        "assertion_record_source_identity_sets": [],
    }

    result = execute_relationship_families(_minimal_policy(), rows_by_input)
    producer_relationships = [
        row for row in result.relationships if row.relationship_family_id == "producer_family_membership"
    ]

    assert len(producer_relationships) == 2
    assert {row.grouping_key for row in producer_relationships} == {
        "producer_family=GSC",
        "producer_family=VAP",
    }
    assert sum(row.member_count for row in producer_relationships) == 3
    assert all(member.member_type == ASSERTION_MEMBER_TYPE for member in result.members if member.source_assertion_id)
    assert any(component.basis_component_type == "assertion_field_value" for component in result.basis_components)


def test_source_identity_set_executor_is_reference_only_and_namespace_honest() -> None:
    rows_by_input = {
        "downstream_topology_input_manifest": [],
        "assertion_record_source_identity_sets": [
            {
                "source_identity_set_id": "sis1",
                "assertion_id": "ar1",
                "source_assertion_registration_id": "sar1",
                "identity_kind": "gene",
                "participant_role": "subject",
                "source_namespace": "NCBI",
                "source_identity_count": "10",
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "source_identity_set_status": "required",
            },
            {
                "source_identity_set_id": "sis2",
                "assertion_id": "ar2",
                "source_assertion_registration_id": "sar2",
                "identity_kind": "gene",
                "participant_role": "subject",
                "source_namespace": "NCBI",
                "source_identity_count": "20",
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "source_identity_set_status": "required",
            },
        ],
        "assertion_record_source_identity_summary": [
            {"source_identity_set_id": "sis1", "registration_unit_id": "ru1"},
            {"source_identity_set_id": "sis2", "registration_unit_id": "ru2"},
        ],
    }

    result = execute_relationship_families(_minimal_policy(), rows_by_input)
    relationship = next(
        row
        for row in result.relationships
        if row.relationship_family_id == "source_identity_set_role_namespace_membership"
    )

    assert relationship.source_identity_expansion_status == "available_by_source_identity_set_reference"
    assert relationship.statistical_testing_status == "requires_source_identity_expansion"
    assert relationship.namespace_mediation_status == "source_namespace_only"
    assert relationship.member_count == 2
    assert all(
        member.member_type == SOURCE_IDENTITY_SET_MEMBER_TYPE
        for member in result.members
        if member.topology_relationship_id == relationship.topology_relationship_id
    )
    assert all(
        component.lossiness_status == "lossless_by_reference"
        for component in result.basis_components
        if component.basis_component_type == "source_identity_set_reference"
    )


def test_singleton_groups_are_emitted() -> None:
    rows_by_input = {
        "downstream_topology_input_manifest": [
            {
                "assertion_id": "ar1",
                "corpus_generation_id": "test_corpus",
                "registration_unit_id": "ru1",
                "producer_family": "VAP",
            }
        ],
        "assertion_record_source_identity_sets": [],
    }

    result = execute_relationship_families(_minimal_policy(), rows_by_input)

    assert any(row.member_count == 1 for row in result.relationships)


def test_relationship_ids_are_stable_under_row_reordering() -> None:
    policy = _minimal_policy()
    rows = [
        {
            "assertion_id": "ar1",
            "corpus_generation_id": "test_corpus",
            "registration_unit_id": "ru1",
            "producer_family": "VAP",
        },
        {
            "assertion_id": "ar2",
            "corpus_generation_id": "test_corpus",
            "registration_unit_id": "ru2",
            "producer_family": "VAP",
        },
    ]
    left = execute_relationship_families(
        policy,
        {"downstream_topology_input_manifest": rows, "assertion_record_source_identity_sets": []},
    )
    right = execute_relationship_families(
        policy,
        {"downstream_topology_input_manifest": list(reversed(rows)), "assertion_record_source_identity_sets": []},
    )

    assert [row.topology_relationship_id for row in left.relationships] == [
        row.topology_relationship_id for row in right.relationships
    ]
    assert [row.member_id for row in left.members] == [row.member_id for row in right.members]
    assert [row.basis_component_id for row in left.basis_components] == [
        row.basis_component_id for row in right.basis_components
    ]


def test_result_rows_are_sorted_by_stable_identifiers() -> None:
    rows_by_input = {
        "downstream_topology_input_manifest": [
            {"assertion_id": "ar2", "producer_family": "VAP"},
            {"assertion_id": "ar1", "producer_family": "VAP"},
            {"assertion_id": "ar3", "producer_family": "GSC"},
        ],
        "assertion_record_source_identity_sets": [],
    }

    result = execute_relationship_families(_minimal_policy(), rows_by_input)

    assert [row.topology_relationship_id for row in result.relationships] == sorted(
        row.topology_relationship_id for row in result.relationships
    )
    assert [(row.topology_relationship_id, row.member_id) for row in result.members] == sorted(
        (row.topology_relationship_id, row.member_id) for row in result.members
    )
    assert [
        (row.topology_relationship_id, row.basis_component_id)
        for row in result.basis_components
    ] == sorted(
        (row.topology_relationship_id, row.basis_component_id)
        for row in result.basis_components
    )


def test_canonical_policy_executes_all_enabled_families_on_repo_local_surface() -> None:
    policy = load_topology_policy(POLICY_PATH)
    result = build_relationship_rows(policy, repo_root=Path("."))

    assert len(result.family_execution_records) == 12
    assert {row.execution_status for row in result.family_execution_records} == {"passed"}
    assert {row.relationship_family_id for row in result.family_execution_records} == {
        family["relationship_family_id"] for family in policy["enabled_relationship_families"]
    }
    assert result.relationships
    assert result.members
    assert result.basis_components


def test_canonical_full_corpus_relationship_member_and_basis_ids_are_unique() -> None:
    policy = load_topology_policy(POLICY_PATH)
    result = build_relationship_rows(policy, repo_root=Path("."))

    relationship_ids = [row.topology_relationship_id for row in result.relationships]
    member_ids = [row.member_id for row in result.members]
    basis_ids = [row.basis_component_id for row in result.basis_components]

    assert len(relationship_ids) == len(set(relationship_ids))
    assert len(member_ids) == len(set(member_ids))
    assert len(basis_ids) == len(set(basis_ids))


def test_canonical_full_corpus_build_is_stable_across_repeated_runs() -> None:
    policy = load_topology_policy(POLICY_PATH)

    left = build_relationship_rows(policy, repo_root=Path("."))
    right = build_relationship_rows(policy, repo_root=Path("."))

    assert [row.topology_relationship_id for row in left.relationships] == [
        row.topology_relationship_id for row in right.relationships
    ]
    assert [row.member_id for row in left.members] == [row.member_id for row in right.members]
    assert [row.basis_component_id for row in left.basis_components] == [
        row.basis_component_id for row in right.basis_components
    ]

"""Tests for deterministic Evidence Topology identity generation."""
from __future__ import annotations

from variant_database.phase4.evidence_topology.identity import (
    make_normalized_grouping_key,
    make_topology_basis_component_id,
    make_topology_member_id,
    make_topology_relationship_id,
    normalize_identity_part,
    stable_hash_payload,
)


def test_normalize_identity_part_distinguishes_null_and_empty() -> None:
    assert normalize_identity_part(None) == "__NULL__"
    assert normalize_identity_part("") == "__EMPTY__"
    assert normalize_identity_part("  VAP  ") == "VAP"


def test_normalize_identity_part_sorts_pipe_delimited_values() -> None:
    assert normalize_identity_part("B|A") == "A|B"


def test_stable_hash_payload_uses_normalized_parts() -> None:
    assert stable_hash_payload(["  VAP  ", "", None]) == "VAP\x1f__EMPTY__\x1f__NULL__"


def test_make_normalized_grouping_key_is_stable() -> None:
    row = {"identity_kind": "gene", "participant_role": "subject", "source_namespace": "NCBI"}

    assert make_normalized_grouping_key(
        row,
        ["identity_kind", "participant_role", "source_namespace"],
    ) == "identity_kind=gene|participant_role=subject|source_namespace=NCBI"


def test_make_normalized_grouping_key_respects_policy_declared_order() -> None:
    row = {"a": "1", "b": "2"}

    assert make_normalized_grouping_key(row, ["a", "b"]) == "a=1|b=2"
    assert make_normalized_grouping_key(row, ["b", "a"]) == "b=2|a=1"


def test_topology_relationship_id_is_stable_under_member_reordering() -> None:
    left = make_topology_relationship_id(
        topology_build_id="build1",
        relationship_family_id="producer_family_membership",
        topology_dimension="producer",
        relationship_kind="producer_family_membership",
        derivation_basis="shared_producer_family",
        normalized_grouping_key="producer_family=VAP",
        member_identifiers=["a3", "a1", "a2"],
    )
    right = make_topology_relationship_id(
        topology_build_id="build1",
        relationship_family_id="producer_family_membership",
        topology_dimension="producer",
        relationship_kind="producer_family_membership",
        derivation_basis="shared_producer_family",
        normalized_grouping_key="producer_family=VAP",
        member_identifiers=["a2", "a3", "a1"],
    )

    assert left == right
    assert left.startswith("topology_rel_")


def test_topology_relationship_id_changes_when_grouping_value_changes() -> None:
    common = {
        "topology_build_id": "build1",
        "relationship_family_id": "producer_family_membership",
        "topology_dimension": "producer",
        "relationship_kind": "producer_family_membership",
        "derivation_basis": "shared_producer_family",
        "member_identifiers": ["a1", "a2"],
    }

    vap = make_topology_relationship_id(
        **common,
        normalized_grouping_key="producer_family=VAP",
    )
    gsc = make_topology_relationship_id(
        **common,
        normalized_grouping_key="producer_family=GSC",
    )

    assert vap != gsc


def test_topology_relationship_id_changes_when_family_changes() -> None:
    common = {
        "topology_build_id": "build1",
        "topology_dimension": "producer",
        "relationship_kind": "producer_family_membership",
        "derivation_basis": "shared_producer_family",
        "normalized_grouping_key": "producer_family=VAP",
        "member_identifiers": ["a1", "a2"],
    }

    left = make_topology_relationship_id(
        **common,
        relationship_family_id="producer_family_membership",
    )
    right = make_topology_relationship_id(
        **common,
        relationship_family_id="assertion_type_membership",
    )

    assert left != right


def test_member_id_is_semantic_and_stable() -> None:
    left = make_topology_member_id(
        topology_relationship_id="rel1",
        member_type="assertion_record",
        member_role="producer_family_membership_member",
        member_reference="ar1",
        source_assertion_id="ar1",
    )
    right = make_topology_member_id(
        topology_relationship_id="rel1",
        member_type="assertion_record",
        member_role="producer_family_membership_member",
        member_reference="ar1",
        source_assertion_id="ar1",
    )

    assert left == right
    assert left.startswith("topology_member_")


def test_basis_component_id_is_semantic_and_stable() -> None:
    left = make_topology_basis_component_id(
        topology_relationship_id="rel1",
        basis_component_type="assertion_field_value",
        basis_component_role="grouping_key",
        basis_component_value="producer_family=VAP",
        basis_component_reference="producer_family=VAP",
    )
    right = make_topology_basis_component_id(
        topology_relationship_id="rel1",
        basis_component_type="assertion_field_value",
        basis_component_role="grouping_key",
        basis_component_value="producer_family=VAP",
        basis_component_reference="producer_family=VAP",
    )

    assert left == right
    assert left.startswith("topology_basis_")

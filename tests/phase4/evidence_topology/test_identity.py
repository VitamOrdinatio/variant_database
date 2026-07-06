"""Tests for deterministic Evidence Topology identity generation."""
from __future__ import annotations

from variant_database.phase4.evidence_topology.identity import (
    make_normalized_grouping_key,
    make_topology_relationship_id,
    normalize_identity_part,
)


def test_normalize_identity_part_distinguishes_null_and_empty() -> None:
    assert normalize_identity_part(None) == "__NULL__"
    assert normalize_identity_part("") == "__EMPTY__"
    assert normalize_identity_part("  VAP  ") == "VAP"


def test_normalize_identity_part_sorts_pipe_delimited_values() -> None:
    assert normalize_identity_part("B|A") == "A|B"


def test_make_normalized_grouping_key_is_stable() -> None:
    row = {"identity_kind": "gene", "participant_role": "subject", "source_namespace": "NCBI"}

    assert make_normalized_grouping_key(
        row,
        ["identity_kind", "participant_role", "source_namespace"],
    ) == "identity_kind=gene|participant_role=subject|source_namespace=NCBI"


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

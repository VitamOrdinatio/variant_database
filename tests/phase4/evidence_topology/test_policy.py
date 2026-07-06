"""Tests for Evidence Topology policy loading and preflight."""
from __future__ import annotations

from pathlib import Path

from variant_database.phase4.evidence_topology.policy import (
    VALIDATION_STATUS_PASSED,
    iter_enabled_relationship_families,
    load_topology_policy,
    preflight_policy,
    validate_strategy_profile_references,
)


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)


def _failed(checks):
    return [check for check in checks if check.status != VALIDATION_STATUS_PASSED]


def test_active_policy_json_loads() -> None:
    policy = load_topology_policy(POLICY_PATH)

    assert policy["policy_identity"]["policy_id"] == (
        "mark_phase4_vap_gsc_topology_derivation_policy_v1"
    )
    assert policy["policy_identity"]["topology_build_id"] == (
        "mark_phase4_corpus_6tep_v1_topology_build_v1"
    )


def test_active_policy_preflight_passes() -> None:
    result = preflight_policy(POLICY_PATH)

    assert result.validation_status == VALIDATION_STATUS_PASSED, _failed(result.checks)


def test_enabled_relationship_families_reference_declared_strategy_profiles() -> None:
    policy = load_topology_policy(POLICY_PATH)
    checks = validate_strategy_profile_references(policy)

    assert checks
    assert not _failed(checks)


def test_active_policy_declares_expected_v1_relationship_family_count() -> None:
    policy = load_topology_policy(POLICY_PATH)
    families = iter_enabled_relationship_families(policy)

    assert len(families) == 12
    assert {family["relationship_family_id"] for family in families} == {
        "corpus_metadata_membership",
        "registration_unit_membership",
        "producer_family_membership",
        "assertion_type_membership",
        "relationship_class_membership",
        "preservation_status_membership",
        "resolver_status_membership",
        "validation_status_membership",
        "source_identity_set_status_membership",
        "source_identity_set_role_namespace_membership",
        "source_identity_resolution_status_membership",
        "source_identity_lossiness_status_membership",
    }

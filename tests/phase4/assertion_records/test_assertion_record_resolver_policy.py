"""Layer 1 tests for Phase 4.3 resolver policy declaration."""
from __future__ import annotations

import pytest

from tests.phase4.assertion_records.helpers.builder_imports import import_required

pytestmark = pytest.mark.phase4_3_layer1

ALLOWED_RESOLUTION_STATUSES = {
    "supported",
    "indexed_with_note",
    "deferred",
    "unsupported",
}

EXPECTED_ASSERTION_TYPES = {
    "VAP": {
        "variant_observation",
        "variant_normalization",
        "variant_interpretation",
        "variant_prioritization",
        "validation",
        "candidate_routing",
    },
    "GSC": {
        "phenotype_gene_semantic_prior",
        "phenotype_gene_provenance",
        "source_gene_relationship",
        "aggregation_support",
        "source_contribution_topology",
        "producer_contract_validation",
    },
}


def _policy_matrix(policy_module):
    matrix = getattr(policy_module, "RESOLVER_STATUS", None)
    if matrix is None:
        matrix = getattr(policy_module, "RESOLVER_POLICY", None)
    assert isinstance(matrix, dict), "resolver policy module must expose RESOLVER_STATUS or RESOLVER_POLICY"
    return matrix


def _entry_status(entry) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        return entry.get("resolution_status", entry.get("status", ""))
    return ""


def test_resolver_policy_declares_every_known_phase4_3_assertion_type() -> None:
    policy = import_required("resolver_policy")
    matrix = _policy_matrix(policy)

    missing: list[str] = []
    invalid_status: list[str] = []
    for producer_family, assertion_types in EXPECTED_ASSERTION_TYPES.items():
        producer_policy = matrix.get(producer_family, {})
        for assertion_type in assertion_types:
            if assertion_type not in producer_policy:
                missing.append(f"{producer_family}:{assertion_type}")
                continue
            status = _entry_status(producer_policy[assertion_type])
            if status not in ALLOWED_RESOLUTION_STATUSES:
                invalid_status.append(f"{producer_family}:{assertion_type} -> {status!r}")

    assert not missing, "missing resolver policies: " + ", ".join(sorted(missing))
    assert not invalid_status, "invalid resolver statuses: " + ", ".join(sorted(invalid_status))


def test_deferred_or_unsupported_assertions_are_not_silent_drops() -> None:
    policy = import_required("resolver_policy")
    matrix = _policy_matrix(policy)

    vap_candidate_routing = _entry_status(matrix["VAP"]["candidate_routing"])
    gsc_source_contribution_topology = _entry_status(matrix["GSC"]["source_contribution_topology"])

    assert vap_candidate_routing in {"deferred", "indexed_with_note", "unsupported"}
    assert gsc_source_contribution_topology in {"indexed_with_note", "deferred", "supported"}


def test_gsc_producer_contract_validation_declares_source_identity_not_applicable() -> None:
    policy = import_required("resolver_policy")
    matrix = _policy_matrix(policy)

    entry = matrix["GSC"]["producer_contract_validation"]
    source_identity_status = None

    if hasattr(policy, "source_identity_set_status"):
        source_identity_status = policy.source_identity_set_status("GSC", "producer_contract_validation")
    elif isinstance(entry, dict):
        source_identity_status = entry.get("source_identity_set_status")

    assert source_identity_status in {
        "not_applicable",
        "not_applicable_for_source_identity_sets",
    }

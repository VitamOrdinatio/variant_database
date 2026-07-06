"""Tests for Evidence Topology builder scaffold behavior."""
from __future__ import annotations

from pathlib import Path

from variant_database.phase4.evidence_topology.builder import (
    VALIDATION_STATUS_PASSED,
    failed_input_checks,
    failed_policy_checks,
    run_preflight,
)


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)


def test_builder_preflight_passes_without_emitting_topology_rows() -> None:
    result = run_preflight(POLICY_PATH, repo_root=Path("."))

    assert result.validation_status == VALIDATION_STATUS_PASSED
    assert not failed_policy_checks(result)
    assert not failed_input_checks(result)
    assert result.policy_result.topology_build_id == (
        "mark_phase4_corpus_6tep_v1_topology_build_v1"
    )

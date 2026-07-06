"""Tests for Evidence Topology governed input preflight."""
from __future__ import annotations

from pathlib import Path

from variant_database.phase4.evidence_topology.inputs import (
    VALIDATION_STATUS_PASSED,
    preflight_assertion_record_surface,
    read_tsv_header,
)
from variant_database.phase4.evidence_topology.policy import load_topology_policy


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)
ASSERTION_INDEX = Path(
    "results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/"
    "assertion_record_index.tsv"
)


def _failed(checks):
    return [check for check in checks if check.status != VALIDATION_STATUS_PASSED]


def test_read_tsv_header_preserves_assertion_index_columns() -> None:
    header = read_tsv_header(ASSERTION_INDEX)

    assert len(header) == 16
    assert header[4] == "producer_family"
    assert header[5] == "source_package_id"


def test_canonical_assertion_record_surface_preflight_passes() -> None:
    policy = load_topology_policy(POLICY_PATH)
    result = preflight_assertion_record_surface(policy, repo_root=Path("."))

    assert result.required_input_count >= 6
    assert result.validation_status == VALIDATION_STATUS_PASSED, _failed(result.checks)

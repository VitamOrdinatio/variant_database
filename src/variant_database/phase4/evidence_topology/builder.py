"""Policy-aware Evidence Topology builder orchestration.

The current Phase 4.4 implementation supports:
- policy and governed-input preflight
- conservative v1 relationship-family row construction in memory

It deliberately does not yet emit topology artifacts to disk, build Convergence
Geometry, perform namespace-mediated canonical matching, run statistical tests,
or perform RDGP reasoning.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .inputs import (
    AssertionRecordSurfacePreflightResult,
    TopologyInputCheck,
    preflight_assertion_record_surface,
)
from .policy import (
    TopologyPolicyCheck,
    TopologyPolicyPreflightResult,
    load_topology_policy,
    preflight_policy,
)
from .relationships import TopologyRelationshipBuildResult, build_relationship_rows


VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class EvidenceTopologyPreflightResult:
    """Combined Evidence Topology preflight result."""

    policy_path: Path
    repo_root: Path
    validation_status: str
    policy_result: TopologyPolicyPreflightResult
    input_result: AssertionRecordSurfacePreflightResult


def run_preflight(
    policy_path: str | Path,
    repo_root: str | Path = Path("."),
) -> EvidenceTopologyPreflightResult:
    """Run policy and governed-input preflight checks.

    This function is intentionally read-only and emits no topology artifacts.
    """

    resolved_policy_path = Path(policy_path)
    root = Path(repo_root)

    policy_result = preflight_policy(resolved_policy_path)
    policy = load_topology_policy(resolved_policy_path)
    input_result = preflight_assertion_record_surface(policy, root)

    return EvidenceTopologyPreflightResult(
        policy_path=resolved_policy_path,
        repo_root=root,
        validation_status=_combined_status(
            policy_result.validation_status,
            input_result.validation_status,
        ),
        policy_result=policy_result,
        input_result=input_result,
    )


def build_topology_rows(
    policy_path: str | Path,
    repo_root: str | Path = Path("."),
) -> TopologyRelationshipBuildResult:
    """Build conservative v1 topology rows in memory.

    The function runs preflight first and raises ValueError on failure. It does
    not write output artifacts to disk.
    """

    preflight = run_preflight(policy_path, repo_root)
    if preflight.validation_status != VALIDATION_STATUS_PASSED:
        failed = [check.check_id for check in all_checks(preflight) if check.status != VALIDATION_STATUS_PASSED]
        raise ValueError(
            "Evidence Topology preflight failed before row construction: "
            + ", ".join(failed)
        )

    policy = load_topology_policy(policy_path)
    return build_relationship_rows(policy, repo_root)


def failed_policy_checks(
    result: EvidenceTopologyPreflightResult,
) -> tuple[TopologyPolicyCheck, ...]:
    """Return failed policy checks from a combined preflight result."""

    return tuple(
        check
        for check in result.policy_result.checks
        if check.status == VALIDATION_STATUS_FAILED
    )


def failed_input_checks(
    result: EvidenceTopologyPreflightResult,
) -> tuple[TopologyInputCheck, ...]:
    """Return failed input checks from a combined preflight result."""

    return tuple(
        check
        for check in result.input_result.checks
        if check.status == VALIDATION_STATUS_FAILED
    )


def all_checks(
    result: EvidenceTopologyPreflightResult,
) -> tuple[TopologyPolicyCheck | TopologyInputCheck, ...]:
    """Return all checks from a combined preflight result."""

    return tuple(_chain(result.policy_result.checks, result.input_result.checks))


def _combined_status(*statuses: str) -> str:
    return (
        VALIDATION_STATUS_FAILED
        if any(status == VALIDATION_STATUS_FAILED for status in statuses)
        else VALIDATION_STATUS_PASSED
    )


def _chain(
    *groups: Iterable[TopologyPolicyCheck | TopologyInputCheck],
) -> Iterable[TopologyPolicyCheck | TopologyInputCheck]:
    for group in groups:
        yield from group

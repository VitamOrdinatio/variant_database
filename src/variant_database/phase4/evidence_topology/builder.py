"""Policy-aware Evidence Topology builder orchestration.

This scaffold currently implements preflight only. It validates that the active
topology policy and governed Assertion Record surface are coherent before any
topology relationships are emitted.

It deliberately does not yet emit topology rows, build Convergence Geometry,
perform namespace-mediated matching, run statistical tests, or perform RDGP
reasoning.
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

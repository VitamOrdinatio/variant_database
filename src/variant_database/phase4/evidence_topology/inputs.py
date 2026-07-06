"""Governed Assertion Record input loading for Evidence Topology.

This module validates that the Phase 4.4 topology builder can consume the
governed Assertion Record surface declared by the active topology derivation
policy. It does not parse raw producer artifacts, reconstruct Registration
Units, mutate inputs, or emit topology outputs.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Iterable


VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class TopologyInputCheck:
    """Single Assertion Record input preflight check."""

    check_id: str
    validation_group: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class AssertionRecordSurfacePreflightResult:
    """Assertion Record surface preflight result."""

    repo_root: Path
    required_input_count: int
    validation_status: str
    checks: tuple[TopologyInputCheck, ...]


def read_tsv_header(path: str | Path) -> tuple[str, ...]:
    """Read only the header from a TSV file."""

    tsv_path = Path(path)
    with tsv_path.open("r", encoding="utf-8", newline="") as handle:
        header = handle.readline().rstrip("\n\r")

    if not header:
        return tuple()
    return tuple(header.split("\t"))


def validate_required_input_files(
    policy: dict[str, Any],
    repo_root: str | Path = Path("."),
) -> tuple[TopologyInputCheck, ...]:
    """Validate policy-declared required input file presence."""

    root = Path(repo_root)
    checks: list[TopologyInputCheck] = []

    for input_name, declaration in _iter_required_inputs(policy):
        relative_path = str(declaration.get("path", ""))
        path = root / relative_path
        _add_check(
            checks,
            f"required_input_exists__{input_name}",
            "input_presence",
            path.is_file(),
            f"Required topology input exists: {input_name}",
            "file exists",
            path,
        )
        _add_check(
            checks,
            f"required_input_nonempty__{input_name}",
            "input_presence",
            path.is_file() and path.stat().st_size > 0,
            f"Required topology input is non-empty: {input_name}",
            "non-empty file",
            path.stat().st_size if path.is_file() else "missing",
        )

    return tuple(checks)


def validate_required_columns(
    policy: dict[str, Any],
    repo_root: str | Path = Path("."),
) -> tuple[TopologyInputCheck, ...]:
    """Validate policy-declared required TSV columns."""

    root = Path(repo_root)
    checks: list[TopologyInputCheck] = []

    for input_name, declaration in _iter_required_inputs(policy):
        relative_path = str(declaration.get("path", ""))
        path = root / relative_path
        required_columns = tuple(declaration.get("required_columns", ()))

        if not path.is_file():
            _add_check(
                checks,
                f"required_columns_skipped_missing_file__{input_name}",
                "input_columns",
                False,
                f"Cannot validate columns because required input is missing: {input_name}",
                list(required_columns),
                "missing file",
            )
            continue

        observed_columns = read_tsv_header(path)
        missing_columns = tuple(
            column for column in required_columns if column not in observed_columns
        )
        _add_check(
            checks,
            f"required_columns_present__{input_name}",
            "input_columns",
            not missing_columns,
            f"Required columns are present for topology input: {input_name}",
            list(required_columns),
            {
                "observed_columns": list(observed_columns),
                "missing_columns": list(missing_columns),
            },
        )

    return tuple(checks)


def preflight_assertion_record_surface(
    policy: dict[str, Any],
    repo_root: str | Path = Path("."),
) -> AssertionRecordSurfacePreflightResult:
    """Run input-boundary checks for the policy-declared Assertion Record surface."""

    checks = list(validate_required_input_files(policy, repo_root)) + list(
        validate_required_columns(policy, repo_root)
    )
    required_inputs = policy.get("required_inputs", {})
    return AssertionRecordSurfacePreflightResult(
        repo_root=Path(repo_root),
        required_input_count=len(required_inputs) if isinstance(required_inputs, dict) else 0,
        validation_status=_validation_status(checks),
        checks=tuple(checks),
    )


def failed_checks(
    checks: Iterable[TopologyInputCheck],
) -> tuple[TopologyInputCheck, ...]:
    """Return failed input preflight checks."""

    return tuple(check for check in checks if check.status == VALIDATION_STATUS_FAILED)


def _iter_required_inputs(
    policy: dict[str, Any],
) -> tuple[tuple[str, dict[str, Any]], ...]:
    required_inputs = policy.get("required_inputs", {})
    if not isinstance(required_inputs, dict):
        return tuple()

    result: list[tuple[str, dict[str, Any]]] = []
    for input_name, declaration in required_inputs.items():
        if isinstance(declaration, dict):
            result.append((str(input_name), declaration))
    return tuple(result)


def _add_check(
    checks: list[TopologyInputCheck],
    check_id: str,
    group: str,
    passed: bool,
    message: str,
    expected: object = "",
    observed: object = "",
) -> None:
    checks.append(
        TopologyInputCheck(
            check_id=check_id,
            validation_group=group,
            status=VALIDATION_STATUS_PASSED if passed else VALIDATION_STATUS_FAILED,
            message=message,
            expected=_stringify(expected),
            observed=_stringify(observed),
        )
    )


def _validation_status(checks: Iterable[TopologyInputCheck]) -> str:
    return (
        VALIDATION_STATUS_FAILED
        if any(check.status == VALIDATION_STATUS_FAILED for check in checks)
        else VALIDATION_STATUS_PASSED
    )


def _stringify(value: object) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except TypeError:
        return str(value)

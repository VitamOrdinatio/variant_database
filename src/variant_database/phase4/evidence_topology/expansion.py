"""Source Identity Set expansion-handle audit for Evidence Topology.

This module validates that Phase 4.4 Evidence Topology preserves addressable
Source Identity Set expansion handles without flattening individual source
identity values. It audits the durable topology output family against the
upstream Assertion Record Source Identity Set surface.

It deliberately does not open Registration Unit SQLite files, expand source
identities, compute Convergence Geometry, emit Projection Views, construct
TEP-VDB packages, or perform RDGP reasoning.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import csv
from typing import Any, Iterable, Mapping


VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"

EXPANSION_INDEX_FILENAME = "topology_source_identity_expansion_index.tsv"
TOPOLOGY_RELATIONSHIPS_FILENAME = "topology_relationships.tsv"
ASSERTION_SOURCE_IDENTITY_SETS_FILENAME = "assertion_record_source_identity_sets.tsv"
ASSERTION_SOURCE_IDENTITY_SUMMARY_FILENAME = "assertion_record_source_identity_summary.tsv"

EXPANSION_INDEX_REQUIRED_COLUMNS = (
    "topology_build_id",
    "topology_relationship_id",
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "registration_unit_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
    "lossiness_status",
    "resolution_status",
    "source_identity_set_status",
    "source_identity_expansion_status",
    "statistical_testing_status",
    "validation_status",
)

TOPOLOGY_RELATIONSHIP_REQUIRED_COLUMNS = (
    "topology_relationship_id",
    "source_identity_expansion_status",
    "statistical_testing_status",
    "namespace_mediation_status",
)

ASSERTION_SOURCE_IDENTITY_SET_REQUIRED_COLUMNS = (
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
    "lossiness_status",
    "resolution_status",
    "source_identity_set_status",
)

ASSERTION_SOURCE_IDENTITY_SUMMARY_REQUIRED_COLUMNS = (
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "registration_unit_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
)

FORBIDDEN_EXPANDED_SOURCE_IDENTITY_COLUMNS = (
    "source_identity_value",
    "expanded_source_identity_value",
    "individual_source_identity_value",
    "canonical_identity_value",
    "participant_value",
)

ALLOWED_EXPANSION_STATUS_V1 = frozenset({"available_by_source_identity_set_reference"})
ALLOWED_STATISTICAL_STATUS_V1 = frozenset({"requires_source_identity_expansion"})


@dataclass(frozen=True)
class ExpansionHandleAuditCheck:
    """Single Source Identity Set expansion-handle audit check."""

    check_id: str
    validation_group: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class ExpansionHandleAuditResult:
    """Audit result for Source Identity Set expansion-handle preservation."""

    topology_output_dir: Path
    assertion_record_dir: Path
    validation_status: str
    checks: tuple[ExpansionHandleAuditCheck, ...]
    summary: Mapping[str, Any]


@dataclass(frozen=True)
class TsvTable:
    """Simple TSV table representation used by the audit."""

    path: Path
    header: tuple[str, ...]
    rows: tuple[dict[str, str], ...]


def audit_source_identity_expansion_handles(
    topology_output_dir: str | Path,
    assertion_record_dir: str | Path,
) -> ExpansionHandleAuditResult:
    """Validate Source Identity Set expansion handles without expanding values."""

    topology_dir = Path(topology_output_dir)
    assertion_dir = Path(assertion_record_dir)
    checks: list[ExpansionHandleAuditCheck] = []

    def add_check(
        check_id: str,
        group: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
    ) -> None:
        checks.append(
            ExpansionHandleAuditCheck(
                check_id=check_id,
                validation_group=group,
                status=VALIDATION_STATUS_PASSED if passed else VALIDATION_STATUS_FAILED,
                message=message,
                expected=_stringify(expected),
                observed=_stringify(observed),
            )
        )

    expansion_path = topology_dir / EXPANSION_INDEX_FILENAME
    relationships_path = topology_dir / TOPOLOGY_RELATIONSHIPS_FILENAME
    source_sets_path = assertion_dir / ASSERTION_SOURCE_IDENTITY_SETS_FILENAME
    source_summary_path = assertion_dir / ASSERTION_SOURCE_IDENTITY_SUMMARY_FILENAME

    required_files = {
        EXPANSION_INDEX_FILENAME: expansion_path,
        TOPOLOGY_RELATIONSHIPS_FILENAME: relationships_path,
        ASSERTION_SOURCE_IDENTITY_SETS_FILENAME: source_sets_path,
        ASSERTION_SOURCE_IDENTITY_SUMMARY_FILENAME: source_summary_path,
    }

    for label, path in required_files.items():
        add_check(
            f"required_file_exists__{label}",
            "file_presence",
            path.is_file(),
            f"Required expansion-handle audit file exists: {label}",
            "file exists",
            path,
        )
        add_check(
            f"required_file_nonempty__{label}",
            "file_presence",
            path.is_file() and path.stat().st_size > 0,
            f"Required expansion-handle audit file is non-empty: {label}",
            "non-empty file",
            path.stat().st_size if path.is_file() else "missing",
        )

    if any(not path.is_file() for path in required_files.values()):
        return _result(topology_dir, assertion_dir, checks, {})

    expansion = _read_tsv(expansion_path)
    relationships = _read_tsv(relationships_path)
    source_sets = _read_tsv(source_sets_path)
    source_summary = _read_tsv(source_summary_path)

    _add_header_check(
        add_check,
        "expansion_index_header",
        "artifact_shape",
        expansion.header,
        EXPANSION_INDEX_REQUIRED_COLUMNS,
        "Expansion index preserves required Source Identity Set handle columns.",
    )
    _add_header_check(
        add_check,
        "topology_relationship_header",
        "artifact_shape",
        relationships.header,
        TOPOLOGY_RELATIONSHIP_REQUIRED_COLUMNS,
        "Topology relationship index exposes relationship/status columns needed for expansion-handle joins.",
    )
    _add_header_check(
        add_check,
        "assertion_source_identity_set_header",
        "artifact_shape",
        source_sets.header,
        ASSERTION_SOURCE_IDENTITY_SET_REQUIRED_COLUMNS,
        "Assertion Record Source Identity Set surface exposes required handle columns.",
    )
    _add_header_check(
        add_check,
        "assertion_source_identity_summary_header",
        "artifact_shape",
        source_summary.header,
        ASSERTION_SOURCE_IDENTITY_SUMMARY_REQUIRED_COLUMNS,
        "Assertion Record Source Identity Summary surface exposes registration-unit recovery columns.",
    )

    forbidden_present = sorted(
        column for column in FORBIDDEN_EXPANDED_SOURCE_IDENTITY_COLUMNS if column in expansion.header
    )
    add_check(
        "expanded_source_identity_value_columns_absent",
        "anti_flattening",
        not forbidden_present,
        "Expansion index does not contain individual source identity value columns.",
        "no expanded source identity value columns",
        forbidden_present or "absent",
    )

    if _has_missing_required_headers(
        expansion.header,
        EXPANSION_INDEX_REQUIRED_COLUMNS,
    ):
        return _result(topology_dir, assertion_dir, checks, {})

    relationship_ids = {row.get("topology_relationship_id", "") for row in relationships.rows}
    expansion_relationship_ids = {
        row.get("topology_relationship_id", "") for row in expansion.rows
    }
    missing_relationship_ids = sorted(expansion_relationship_ids - relationship_ids)
    add_check(
        "expansion_relationship_refs_join_to_topology_relationships",
        "join_integrity",
        not missing_relationship_ids,
        "Every expansion-index topology_relationship_id joins to topology_relationships.tsv.",
        "all expansion relationship refs valid",
        missing_relationship_ids or "all valid",
    )

    source_sets_by_id = _index_unique(source_sets.rows, "source_identity_set_id")
    source_summary_by_id = _index_unique(source_summary.rows, "source_identity_set_id")

    expansion_source_set_ids = {row.get("source_identity_set_id", "") for row in expansion.rows}
    missing_source_set_ids = sorted(expansion_source_set_ids - set(source_sets_by_id))
    add_check(
        "expansion_source_identity_set_ids_join_to_assertion_surface",
        "join_integrity",
        not missing_source_set_ids,
        "Every expansion-index source_identity_set_id joins to assertion_record_source_identity_sets.tsv.",
        "all source_identity_set_id refs valid",
        missing_source_set_ids or "all valid",
    )

    missing_summary_ids = sorted(expansion_source_set_ids - set(source_summary_by_id))
    add_check(
        "expansion_source_identity_set_ids_join_to_summary_surface",
        "join_integrity",
        not missing_summary_ids,
        "Every expansion-index source_identity_set_id joins to assertion_record_source_identity_summary.tsv.",
        "all source_identity_set_id refs valid",
        missing_summary_ids or "all valid",
    )

    required_value_columns = tuple(EXPANSION_INDEX_REQUIRED_COLUMNS)
    empty_required_cells = _empty_required_cells(expansion.rows, required_value_columns)
    add_check(
        "expansion_handle_required_fields_nonempty",
        "handle_completeness",
        not empty_required_cells,
        "Expansion-index rows preserve non-empty required handle fields.",
        "no empty required handle cells",
        empty_required_cells[:20] if empty_required_cells else "none",
    )

    count_mismatches = []
    for row in expansion.rows:
        sid = row.get("source_identity_set_id", "")
        source_row = source_sets_by_id.get(sid)
        if not source_row:
            continue
        if row.get("source_identity_count", "") != source_row.get("source_identity_count", ""):
            count_mismatches.append(sid)
    add_check(
        "source_identity_count_preserved_from_assertion_surface",
        "handle_completeness",
        not count_mismatches,
        "Expansion-index source_identity_count values match the Assertion Record Source Identity Set surface.",
        "counts match by source_identity_set_id",
        sorted(set(count_mismatches))[:20] if count_mismatches else "all matched",
    )

    registration_mismatches = []
    for row in expansion.rows:
        sid = row.get("source_identity_set_id", "")
        summary_row = source_summary_by_id.get(sid)
        if not summary_row:
            continue
        if row.get("registration_unit_id", "") != summary_row.get("registration_unit_id", ""):
            registration_mismatches.append(sid)
    add_check(
        "registration_unit_id_recovered_from_source_identity_summary",
        "handle_completeness",
        not registration_mismatches,
        "Expansion-index registration_unit_id values are recovered from assertion_record_source_identity_summary.tsv.",
        "registration_unit_id matches by source_identity_set_id",
        sorted(set(registration_mismatches))[:20] if registration_mismatches else "all matched",
    )

    expansion_statuses = {row.get("source_identity_expansion_status", "") for row in expansion.rows}
    disallowed_expansion_statuses = sorted(expansion_statuses - ALLOWED_EXPANSION_STATUS_V1)
    add_check(
        "expansion_statuses_are_reference_only_v1",
        "expansion_honesty",
        not disallowed_expansion_statuses,
        "v1 expansion-index rows remain available by Source Identity Set reference only.",
        sorted(ALLOWED_EXPANSION_STATUS_V1),
        sorted(expansion_statuses),
    )

    statistical_statuses = {row.get("statistical_testing_status", "") for row in expansion.rows}
    disallowed_statistical_statuses = sorted(statistical_statuses - ALLOWED_STATISTICAL_STATUS_V1)
    add_check(
        "statistical_testing_status_requires_source_identity_expansion",
        "expansion_honesty",
        not disallowed_statistical_statuses,
        "Expansion-index rows do not claim analysis readiness; they require source identity expansion.",
        sorted(ALLOWED_STATISTICAL_STATUS_V1),
        sorted(statistical_statuses),
    )

    lossiness_values = {row.get("lossiness_status", "") for row in expansion.rows}
    add_check(
        "lossiness_status_preserved",
        "handle_completeness",
        bool(lossiness_values) and "lossless_by_reference" in lossiness_values,
        "Expansion-index rows preserve Source Identity Set lossiness state, including lossless_by_reference.",
        "lossless_by_reference present",
        sorted(lossiness_values),
    )

    summary = summarize_expansion_handles(expansion.rows, source_sets_by_id)
    return _result(topology_dir, assertion_dir, checks, summary)


def summarize_expansion_handles(
    expansion_rows: Iterable[Mapping[str, str]],
    source_sets_by_id: Mapping[str, Mapping[str, str]] | None = None,
) -> dict[str, Any]:
    """Return non-interpretive summary counts for expansion handles."""

    rows = tuple(expansion_rows)
    source_sets_by_id = source_sets_by_id or {}
    distinct_source_identity_set_ids = sorted(
        {row.get("source_identity_set_id", "") for row in rows if row.get("source_identity_set_id", "")}
    )
    distinct_relationship_ids = sorted(
        {row.get("topology_relationship_id", "") for row in rows if row.get("topology_relationship_id", "")}
    )

    represented_source_identity_count = 0
    for sid in distinct_source_identity_set_ids:
        source_row = source_sets_by_id.get(sid, {})
        represented_source_identity_count += _to_int(source_row.get("source_identity_count", "0"))

    return {
        "expansion_index_row_count": len(rows),
        "distinct_source_identity_set_count": len(distinct_source_identity_set_ids),
        "distinct_topology_relationship_count": len(distinct_relationship_ids),
        "represented_source_identity_count_distinct_sets": represented_source_identity_count,
        "by_identity_kind": dict(sorted(Counter(row.get("identity_kind", "") for row in rows).items())),
        "by_participant_role": dict(sorted(Counter(row.get("participant_role", "") for row in rows).items())),
        "by_source_namespace": dict(sorted(Counter(row.get("source_namespace", "") for row in rows).items())),
        "by_expansion_status": dict(sorted(Counter(row.get("source_identity_expansion_status", "") for row in rows).items())),
        "by_statistical_testing_status": dict(sorted(Counter(row.get("statistical_testing_status", "") for row in rows).items())),
        "by_lossiness_status": dict(sorted(Counter(row.get("lossiness_status", "") for row in rows).items())),
    }


def failed_checks(result: ExpansionHandleAuditResult) -> tuple[ExpansionHandleAuditCheck, ...]:
    """Return failed expansion-handle audit checks."""

    return tuple(check for check in result.checks if check.status == VALIDATION_STATUS_FAILED)


def check_by_id(
    result: ExpansionHandleAuditResult,
    check_id: str,
) -> ExpansionHandleAuditCheck:
    """Return one audit check by check_id."""

    for check in result.checks:
        if check.check_id == check_id:
            return check
    raise KeyError(check_id)


def _read_tsv(path: Path) -> TsvTable:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return TsvTable(
            path=path,
            header=tuple(reader.fieldnames or ()),
            rows=tuple(dict(row) for row in reader),
        )


def _add_header_check(
    add_check: Any,
    check_id: str,
    group: str,
    observed_header: Iterable[str],
    required_columns: Iterable[str],
    message: str,
) -> None:
    observed = tuple(observed_header)
    missing = tuple(column for column in required_columns if column not in observed)
    add_check(
        check_id,
        group,
        not missing,
        message,
        tuple(required_columns),
        missing or observed,
    )


def _has_missing_required_headers(
    observed_header: Iterable[str],
    required_columns: Iterable[str],
) -> bool:
    observed = set(observed_header)
    return any(column not in observed for column in required_columns)


def _index_unique(
    rows: Iterable[Mapping[str, str]],
    key: str,
) -> dict[str, Mapping[str, str]]:
    indexed: dict[str, Mapping[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if value and value not in indexed:
            indexed[value] = row
    return indexed


def _empty_required_cells(
    rows: Iterable[Mapping[str, str]],
    required_columns: Iterable[str],
) -> list[str]:
    empty: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        for column in required_columns:
            if row.get(column, "") == "":
                empty.append(f"row={row_index}:{column}")
    return empty


def _result(
    topology_output_dir: Path,
    assertion_record_dir: Path,
    checks: Iterable[ExpansionHandleAuditCheck],
    summary: Mapping[str, Any],
) -> ExpansionHandleAuditResult:
    checks_tuple = tuple(checks)
    status = (
        VALIDATION_STATUS_FAILED
        if any(check.status == VALIDATION_STATUS_FAILED for check in checks_tuple)
        else VALIDATION_STATUS_PASSED
    )
    return ExpansionHandleAuditResult(
        topology_output_dir=topology_output_dir,
        assertion_record_dir=assertion_record_dir,
        validation_status=status,
        checks=checks_tuple,
        summary=dict(summary),
    )


def _stringify(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}={value[key]}" for key in sorted(value))
    return str(value)


def _to_int(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0

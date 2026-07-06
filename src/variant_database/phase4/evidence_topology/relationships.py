"""Relationship-family execution for Phase 4.4 Evidence Topology.

This module executes the conservative v1 topology derivation policy over the
governed Phase 4.3 Assertion Record surface and constructs topology rows in
memory. It deliberately does not write topology artifacts, expand Source
Identity Sets, parse raw producer artifacts, perform namespace-mediated
canonical matching, emit Convergence Geometry, run statistical tests, or perform
RDGP reasoning.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .identity import (
    make_normalized_grouping_key,
    make_topology_basis_component_id,
    make_topology_member_id,
    make_topology_relationship_id,
    normalize_identity_part,
)


VALIDATION_STATUS_PASSED = "passed"
RELATIONSHIP_CLASSIFICATION_METADATA = "metadata_level_topology"
RELATIONSHIP_CLASSIFICATION_IMMEDIATE = "immediately_derived_topology"

ASSERTION_MEMBER_TYPE = "assertion_record"
SOURCE_IDENTITY_SET_MEMBER_TYPE = "source_identity_set"


@dataclass(frozen=True)
class TopologyRelationshipRow:
    """In-memory topology_relationships row."""

    topology_relationship_id: str
    topology_build_id: str
    relationship_family_id: str
    topology_dimension: str
    relationship_kind: str
    derivation_basis: str
    relationship_scope: str
    relationship_classification: str
    grouping_key: str
    grouping_value: str
    source_table: str
    source_assertion_id_summary: str
    source_identity_set_id_summary: str
    member_count: int
    basis_component_count: int
    input_corpus_generation_id: str
    source_identity_expansion_status: str
    statistical_testing_status: str
    namespace_mediation_status: str
    validation_status: str


@dataclass(frozen=True)
class TopologyRelationshipMemberRow:
    """In-memory topology_relationship_members row."""

    topology_relationship_id: str
    member_id: str
    member_type: str
    member_role: str
    member_reference: str
    source_assertion_id: str
    source_identity_set_id: str
    source_registration_unit_id: str
    source_corpus_generation_id: str
    validation_status: str


@dataclass(frozen=True)
class TopologyBasisComponentRow:
    """In-memory topology_basis_components row."""

    topology_relationship_id: str
    basis_component_id: str
    basis_component_type: str
    basis_component_role: str
    basis_component_value: str
    basis_component_reference: str
    basis_component_namespace: str
    source_assertion_id: str
    source_identity_set_id: str
    source_registration_unit_id: str
    source_corpus_generation_id: str
    resolution_status: str
    ambiguity_status: str
    conflict_status: str
    lossiness_status: str
    validation_status: str


@dataclass(frozen=True)
class RelationshipFamilyExecutionRow:
    """Execution accounting for one enabled relationship family."""

    topology_build_id: str
    relationship_family_id: str
    strategy_profile: str
    source_table: str
    grouping_keys: str
    execution_status: str
    relationship_count: int
    member_count: int
    basis_component_count: int
    message: str


@dataclass(frozen=True)
class TopologyRelationshipBuildResult:
    """In-memory result of conservative relationship-family execution."""

    topology_build_id: str
    input_corpus_generation_id: str
    relationships: tuple[TopologyRelationshipRow, ...]
    members: tuple[TopologyRelationshipMemberRow, ...]
    basis_components: tuple[TopologyBasisComponentRow, ...]
    family_execution_records: tuple[RelationshipFamilyExecutionRow, ...]


def load_policy_input_rows(
    policy: dict[str, Any],
    repo_root: str | Path = Path("."),
) -> dict[str, tuple[dict[str, str], ...]]:
    """Load policy-declared required input TSV rows."""

    root = Path(repo_root)
    rows_by_input: dict[str, tuple[dict[str, str], ...]] = {}
    required_inputs = policy.get("required_inputs", {})
    if not isinstance(required_inputs, dict):
        return rows_by_input

    for input_name, declaration in required_inputs.items():
        if not isinstance(declaration, dict):
            continue
        relative_path = declaration.get("path")
        if not relative_path:
            continue
        rows_by_input[str(input_name)] = tuple(_read_tsv(root / str(relative_path)))

    return rows_by_input


def build_relationship_rows(
    policy: dict[str, Any],
    repo_root: str | Path = Path("."),
) -> TopologyRelationshipBuildResult:
    """Execute enabled relationship families over policy-declared inputs."""

    return execute_relationship_families(
        policy,
        load_policy_input_rows(policy, repo_root),
    )


def execute_relationship_families(
    policy: dict[str, Any],
    rows_by_input: dict[str, Iterable[dict[str, str]]],
) -> TopologyRelationshipBuildResult:
    """Construct topology relationship, member, and basis rows in memory."""

    build_defaults = policy.get("topology_build_defaults", {})
    policy_identity = policy.get("policy_identity", {})
    identity_rules = policy.get("deterministic_identity_rules", {})

    topology_build_id = str(
        build_defaults.get("topology_build_id")
        or policy_identity.get("topology_build_id")
        or ""
    )
    input_corpus_generation_id = str(
        build_defaults.get("input_corpus_generation_id")
        or policy_identity.get("input_corpus_generation_id")
        or ""
    )
    relationship_id_prefix = str(
        identity_rules.get("relationship_id_prefix", "topology_rel_")
    )

    profiles = policy.get("relationship_strategy_profiles", {})
    if not isinstance(profiles, dict):
        profiles = {}

    materialized_rows_by_input = {
        key: tuple(rows) for key, rows in rows_by_input.items()
    }
    source_identity_summary_by_set = _source_identity_summary_by_set(
        materialized_rows_by_input.get("assertion_record_source_identity_summary", ())
    )

    relationships: list[TopologyRelationshipRow] = []
    members: list[TopologyRelationshipMemberRow] = []
    basis_components: list[TopologyBasisComponentRow] = []
    family_execution_records: list[RelationshipFamilyExecutionRow] = []

    for family in _iter_enabled_families(policy):
        family_id = str(family.get("relationship_family_id", ""))
        profile_name = str(family.get("strategy_profile", ""))
        profile = profiles.get(profile_name, {})
        if not isinstance(profile, dict):
            profile = {}

        source_table = str(family.get("source_table", ""))
        source_rows = tuple(materialized_rows_by_input.get(source_table, ()))
        grouping_keys = tuple(str(key) for key in family.get("grouping_keys", ()))
        grouped_rows = _group_rows(source_rows, grouping_keys)

        before_relationships = len(relationships)
        before_members = len(members)
        before_basis = len(basis_components)

        for grouping_key in sorted(grouped_rows):
            group_rows = grouped_rows[grouping_key]
            if not group_rows and not profile.get("emit_singleton_groups", False):
                continue

            member_type = _member_type_for_profile(profile_name, profile)
            member_identifier_key = _member_identifier_key(member_type)
            sorted_group_rows = tuple(
                sorted(
                    group_rows,
                    key=lambda row: normalize_identity_part(
                        row.get(member_identifier_key)
                    ),
                )
            )
            member_identifiers = tuple(
                str(row.get(member_identifier_key, "")) for row in sorted_group_rows
            )
            relationship_id = make_topology_relationship_id(
                topology_build_id=topology_build_id,
                relationship_family_id=family_id,
                topology_dimension=str(family.get("topology_dimension", "")),
                relationship_kind=str(family.get("relationship_kind", "")),
                derivation_basis=str(family.get("derivation_basis", "")),
                normalized_grouping_key=grouping_key,
                member_identifiers=member_identifiers,
                prefix=relationship_id_prefix,
            )

            grouping_basis_components = _make_grouping_basis_components(
                topology_relationship_id=relationship_id,
                grouping_key=grouping_key,
                grouping_keys=grouping_keys,
                representative_row=sorted_group_rows[0] if sorted_group_rows else {},
                source_table=source_table,
                input_corpus_generation_id=input_corpus_generation_id,
            )
            member_rows = _make_member_rows(
                topology_relationship_id=relationship_id,
                relationship_family_id=family_id,
                rows=sorted_group_rows,
                member_type=member_type,
                input_corpus_generation_id=input_corpus_generation_id,
                source_identity_summary_by_set=source_identity_summary_by_set,
            )
            source_identity_basis_components = _make_source_identity_set_basis_components(
                topology_relationship_id=relationship_id,
                rows=sorted_group_rows,
                member_type=member_type,
                input_corpus_generation_id=input_corpus_generation_id,
                source_identity_summary_by_set=source_identity_summary_by_set,
            )

            all_basis_components = (
                *grouping_basis_components,
                *source_identity_basis_components,
            )
            relationships.append(
                TopologyRelationshipRow(
                    topology_relationship_id=relationship_id,
                    topology_build_id=topology_build_id,
                    relationship_family_id=family_id,
                    topology_dimension=str(family.get("topology_dimension", "")),
                    relationship_kind=str(family.get("relationship_kind", "")),
                    derivation_basis=str(family.get("derivation_basis", "")),
                    relationship_scope=str(profile.get("relationship_scope", "")),
                    relationship_classification=_relationship_classification(profile),
                    grouping_key=grouping_key,
                    grouping_value=_grouping_value(grouping_key),
                    source_table=source_table,
                    source_assertion_id_summary=_join_unique(
                        row.get("assertion_id", "") for row in sorted_group_rows
                    ),
                    source_identity_set_id_summary=_join_unique(
                        row.get("source_identity_set_id", "") for row in sorted_group_rows
                    ),
                    member_count=len(member_rows),
                    basis_component_count=len(all_basis_components),
                    input_corpus_generation_id=input_corpus_generation_id,
                    source_identity_expansion_status=str(
                        profile.get("source_identity_expansion_status", "not_applicable")
                    ),
                    statistical_testing_status=str(
                        profile.get("statistical_testing_status", "not_applicable")
                    ),
                    namespace_mediation_status=str(
                        profile.get("namespace_mediation_status", "not_applicable")
                    ),
                    validation_status=VALIDATION_STATUS_PASSED,
                )
            )
            members.extend(member_rows)
            basis_components.extend(all_basis_components)

        family_execution_records.append(
            RelationshipFamilyExecutionRow(
                topology_build_id=topology_build_id,
                relationship_family_id=family_id,
                strategy_profile=profile_name,
                source_table=source_table,
                grouping_keys="|".join(grouping_keys),
                execution_status=VALIDATION_STATUS_PASSED,
                relationship_count=len(relationships) - before_relationships,
                member_count=len(members) - before_members,
                basis_component_count=len(basis_components) - before_basis,
                message="Enabled relationship family executed over governed Assertion Record surface.",
            )
        )

    result = TopologyRelationshipBuildResult(
        topology_build_id=topology_build_id,
        input_corpus_generation_id=input_corpus_generation_id,
        relationships=tuple(
            sorted(relationships, key=lambda row: row.topology_relationship_id)
        ),
        members=tuple(
            sorted(members, key=lambda row: (row.topology_relationship_id, row.member_id))
        ),
        basis_components=tuple(
            sorted(
                basis_components,
                key=lambda row: (row.topology_relationship_id, row.basis_component_id),
            )
        ),
        family_execution_records=tuple(
            sorted(family_execution_records, key=lambda row: row.relationship_family_id)
        ),
    )
    _assert_unique_result_ids(result)
    return result


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _iter_enabled_families(policy: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    families = policy.get("enabled_relationship_families", ())
    if not isinstance(families, list):
        return tuple()
    return tuple(family for family in families if isinstance(family, dict))


def _group_rows(
    rows: Iterable[dict[str, str]],
    grouping_keys: tuple[str, ...],
) -> dict[str, tuple[dict[str, str], ...]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[make_normalized_grouping_key(row, grouping_keys)].append(row)
    return {key: tuple(value) for key, value in grouped.items()}


def _member_type_for_profile(profile_name: str, profile: dict[str, Any]) -> str:
    strategy = str(profile.get("member_strategy", ""))
    if profile_name.startswith("source_identity_set") or strategy.startswith("source_identity_sets"):
        return SOURCE_IDENTITY_SET_MEMBER_TYPE
    return ASSERTION_MEMBER_TYPE


def _member_identifier_key(member_type: str) -> str:
    if member_type == SOURCE_IDENTITY_SET_MEMBER_TYPE:
        return "source_identity_set_id"
    return "assertion_id"


def _relationship_classification(profile: dict[str, Any]) -> str:
    scope = str(profile.get("relationship_scope", ""))
    if scope == "metadata" or scope.endswith("metadata_membership"):
        return RELATIONSHIP_CLASSIFICATION_METADATA
    return RELATIONSHIP_CLASSIFICATION_IMMEDIATE


def _make_grouping_basis_components(
    *,
    topology_relationship_id: str,
    grouping_key: str,
    grouping_keys: tuple[str, ...],
    representative_row: dict[str, str],
    source_table: str,
    input_corpus_generation_id: str,
) -> tuple[TopologyBasisComponentRow, ...]:
    components: list[TopologyBasisComponentRow] = []
    for key in grouping_keys:
        value = normalize_identity_part(representative_row.get(key))
        basis_component_type = (
            "source_identity_set_field_value"
            if source_table == "assertion_record_source_identity_sets"
            else "assertion_field_value"
        )
        basis_component_role = "grouping_key"
        basis_component_value = f"{key}={value}"
        basis_component_reference = grouping_key
        basis_component_namespace = (
            value if key in {"source_namespace", "participant_source_namespace"} else ""
        )
        components.append(
            TopologyBasisComponentRow(
                topology_relationship_id=topology_relationship_id,
                basis_component_id=make_topology_basis_component_id(
                    topology_relationship_id=topology_relationship_id,
                    basis_component_type=basis_component_type,
                    basis_component_role=basis_component_role,
                    basis_component_value=basis_component_value,
                    basis_component_reference=basis_component_reference,
                    basis_component_namespace=basis_component_namespace,
                ),
                basis_component_type=basis_component_type,
                basis_component_role=basis_component_role,
                basis_component_value=basis_component_value,
                basis_component_reference=basis_component_reference,
                basis_component_namespace=basis_component_namespace,
                source_assertion_id="",
                source_identity_set_id="",
                source_registration_unit_id="",
                source_corpus_generation_id=input_corpus_generation_id,
                resolution_status="not_applicable",
                ambiguity_status="not_applicable",
                conflict_status="not_applicable",
                lossiness_status="not_applicable",
                validation_status=VALIDATION_STATUS_PASSED,
            )
        )
    return tuple(components)


def _make_member_rows(
    *,
    topology_relationship_id: str,
    relationship_family_id: str,
    rows: Iterable[dict[str, str]],
    member_type: str,
    input_corpus_generation_id: str,
    source_identity_summary_by_set: dict[str, dict[str, str]],
) -> tuple[TopologyRelationshipMemberRow, ...]:
    member_identifier_key = _member_identifier_key(member_type)
    members: list[TopologyRelationshipMemberRow] = []
    member_role = f"{relationship_family_id}_member"
    for row in rows:
        member_reference = str(row.get(member_identifier_key, ""))
        row_source_identity_set_id = str(row.get("source_identity_set_id", ""))
        source_identity_set_id = (
            member_reference
            if member_type == SOURCE_IDENTITY_SET_MEMBER_TYPE
            else row_source_identity_set_id
        )
        source_assertion_id = str(row.get("assertion_id", ""))
        summary = source_identity_summary_by_set.get(source_identity_set_id, {})
        registration_unit_id = str(
            row.get("registration_unit_id")
            or summary.get("registration_unit_id")
            or ""
        )
        source_corpus_generation_id = str(
            row.get("corpus_generation_id") or input_corpus_generation_id
        )
        members.append(
            TopologyRelationshipMemberRow(
                topology_relationship_id=topology_relationship_id,
                member_id=make_topology_member_id(
                    topology_relationship_id=topology_relationship_id,
                    member_type=member_type,
                    member_role=member_role,
                    member_reference=member_reference,
                    source_assertion_id=source_assertion_id,
                    source_identity_set_id=source_identity_set_id,
                ),
                member_type=member_type,
                member_role=member_role,
                member_reference=member_reference,
                source_assertion_id=source_assertion_id,
                source_identity_set_id=source_identity_set_id,
                source_registration_unit_id=registration_unit_id,
                source_corpus_generation_id=source_corpus_generation_id,
                validation_status=VALIDATION_STATUS_PASSED,
            )
        )
    return tuple(members)


def _make_source_identity_set_basis_components(
    *,
    topology_relationship_id: str,
    rows: Iterable[dict[str, str]],
    member_type: str,
    input_corpus_generation_id: str,
    source_identity_summary_by_set: dict[str, dict[str, str]],
) -> tuple[TopologyBasisComponentRow, ...]:
    if member_type != SOURCE_IDENTITY_SET_MEMBER_TYPE:
        return tuple()

    components: list[TopologyBasisComponentRow] = []
    for row in rows:
        source_identity_set_id = str(row.get("source_identity_set_id", ""))
        source_assertion_id = str(row.get("assertion_id", ""))
        source_namespace = str(row.get("source_namespace", ""))
        summary = source_identity_summary_by_set.get(source_identity_set_id, {})
        registration_unit_id = str(
            row.get("registration_unit_id")
            or summary.get("registration_unit_id")
            or ""
        )
        source_corpus_generation_id = str(
            row.get("corpus_generation_id") or input_corpus_generation_id
        )
        basis_component_type = "source_identity_set_reference"
        basis_component_role = "grouping_member"
        components.append(
            TopologyBasisComponentRow(
                topology_relationship_id=topology_relationship_id,
                basis_component_id=make_topology_basis_component_id(
                    topology_relationship_id=topology_relationship_id,
                    basis_component_type=basis_component_type,
                    basis_component_role=basis_component_role,
                    basis_component_reference=source_identity_set_id,
                    basis_component_namespace=source_namespace,
                    source_assertion_id=source_assertion_id,
                    source_identity_set_id=source_identity_set_id,
                ),
                basis_component_type=basis_component_type,
                basis_component_role=basis_component_role,
                basis_component_value="",
                basis_component_reference=source_identity_set_id,
                basis_component_namespace=source_namespace,
                source_assertion_id=source_assertion_id,
                source_identity_set_id=source_identity_set_id,
                source_registration_unit_id=registration_unit_id,
                source_corpus_generation_id=source_corpus_generation_id,
                resolution_status=str(row.get("resolution_status", "not_applicable")),
                ambiguity_status="not_applicable",
                conflict_status="not_applicable",
                lossiness_status=str(row.get("lossiness_status", "lossless_by_reference")),
                validation_status=VALIDATION_STATUS_PASSED,
            )
        )
    return tuple(components)


def _source_identity_summary_by_set(
    rows: Iterable[dict[str, str]],
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        source_identity_set_id = row.get("source_identity_set_id", "")
        if source_identity_set_id:
            result[source_identity_set_id] = dict(row)
    return result


def _grouping_value(grouping_key: str) -> str:
    if "|" not in grouping_key and "=" in grouping_key:
        return grouping_key.split("=", 1)[1]
    return grouping_key


def _join_unique(values: Iterable[str]) -> str:
    cleaned = sorted({str(value) for value in values if str(value)})
    return "|".join(cleaned)


def _assert_unique_result_ids(result: TopologyRelationshipBuildResult) -> None:
    _assert_unique(
        "topology_relationship_id",
        (row.topology_relationship_id for row in result.relationships),
    )
    _assert_unique("member_id", (row.member_id for row in result.members))
    _assert_unique(
        "basis_component_id",
        (row.basis_component_id for row in result.basis_components),
    )


def _assert_unique(label: str, values: Iterable[str]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f"Duplicate {label} values: {sorted(duplicates)}")


def rows_as_dicts(rows: Iterable[Any]) -> tuple[dict[str, Any], ...]:
    """Convert dataclass row objects into dictionaries for later writers/tests."""

    return tuple(row.__dict__.copy() for row in rows)

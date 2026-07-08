"""Policy loading and conformance checks for Evidence Topology.

This module validates the executable Phase 4.4 topology derivation policy.
It does not construct topology relationships, open producer artifacts, mutate
Assertion Records, perform namespace mediation, perform statistical testing, or
derive biological interpretation.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Iterable


VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"

REQUIRED_TOP_LEVEL_KEYS = {
    "policy_identity",
    "governing_references",
    "input_boundary",
    "required_inputs",
    "topology_build_defaults",
    "deterministic_identity_rules",
    "relationship_strategy_profiles",
    "enabled_relationship_families",
    "deferred_relationship_families",
    "prohibited_relationship_families",
    "source_identity_expansion_policy",
    "namespace_mediation_policy",
    "statistical_testing_policy",
    "output_requirements",
    "validation_behavior",
    "anti_collapse_rules",
}

REQUIRED_POLICY_IDENTITY_KEYS = {
    "policy_id",
    "policy_version",
    "phase",
    "layer",
    "input_corpus_generation_id",
    "topology_build_id",
    "policy_status",
}

REQUIRED_ENABLED_FAMILY_KEYS = {
    "relationship_family_id",
    "strategy_profile",
    "topology_dimension",
    "relationship_kind",
    "derivation_basis",
    "source_table",
    "grouping_keys",
}

# These sets intentionally mirror the Phase 4.4 schema/spec vocabulary used by
# the initial conservative topology derivation policy. They are builder-facing
# guardrails, not biological interpretation rules.
ALLOWED_TOPOLOGY_DIMENSIONS = {
    "participant",
    "relationship",
    "context",
    "provenance",
    "epistemic",
    "temporal",
    "independence",
    "producer",
    "evidence_domain",
    "namespace",
    "uncertainty_status",
    "generation",
    "registration_unit",
    "corpus_generation",
    "metadata",
    "source_identity_set",
    "coordinate",
    "feature",
    "declaration_set",
}

ALLOWED_RELATIONSHIP_KINDS = {
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
    # Policy-conditional or future relationship kinds.
    "shared_participant",
    "shared_context",
    "shared_relationship_class",
    "shared_producer_family",
    "shared_evidence_domain",
    "source_identity_obligation_status_membership",
    "namespace_mediated_participant_match",
    "cross_producer_participant_intersection",
    "cross_evidence_domain_participant_intersection",
    "exact_source_identity_value_intersection",
    "exact_variant_overlap",
    "exact_gene_overlap",
    "exact_sample_overlap",
    "uncertainty_contrast",
    "temporal_generation_match",
    "registration_metadata_membership",
    "coordinate_declaration_reference_build_membership",
    "coordinate_declaration_namespace_membership",
    "feature_declaration_kind_namespace_membership",
    "feature_declaration_annotation_context_membership",
}

ALLOWED_DERIVATION_BASES = {
    "shared_source_identity",
    "shared_source_identity_set_role_kind_namespace",
    "shared_source_identity_set_status",
    "shared_source_identity_resolution_status",
    "shared_source_identity_lossiness_status",
    "shared_participant_role",
    "shared_participant_value",
    "shared_assertion_type",
    "shared_relationship_class",
    "shared_relationship_type",
    "shared_preservation_status",
    "shared_validation_status",
    "shared_resolver_status",
    "shared_phenotype_context",
    "shared_sample_context",
    "shared_gene_participant",
    "shared_variant_participant",
    "shared_producer_family",
    "shared_evidence_domain",
    "shared_registration_unit",
    "shared_corpus_generation",
    "namespace_mediated_match",
    "metadata_membership",
    "shared_reference_genome_build",
    "shared_variant_source_namespace",
    "shared_feature_kind_namespace_relationship",
    "shared_annotation_context",
}

ALLOWED_RELATIONSHIP_SCOPES = {
    "metadata",
    "source_identity_set",
    "coordinate_declaration_set",
    "feature_declaration_set",
    "namespace",
    "participant",
    "relationship",
    "context",
    "provenance",
    "corpus_generation",
    "registration_unit",
    "producer_family",
    "evidence_domain",
    "not_applicable",
}

ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS = {
    "not_required",
    "available_by_source_identity_set_reference",
    "requires_controlled_expansion",
    "expanded_under_policy",
    "deferred_by_policy",
    "not_applicable",
    "unavailable",
    "header_only_not_policy_enabled",
}

ALLOWED_STATISTICAL_TESTING_STATUS = {
    "not_statistical_input",
    "analysis_ready",
    "requires_source_identity_expansion",
    "requires_declaration_expansion",
    "requires_external_annotation",
    "requires_case_control_design",
    "deferred_to_projection_layer",
    "not_applicable",
}

ALLOWED_NAMESPACE_MEDIATION_STATUS = {
    "not_applicable",
    "direct_source_identity",
    "source_namespace_only",
    "canonical_identity_attached",
    "namespace_mediated",
    "ambiguous",
    "conflicted",
    "unresolved",
    "deferred_by_policy",
}

ALLOWED_MATCH_TYPES = {
    "source_identity_match",
    "source_namespace_match",
    "canonical_identity_match",
    "namespace_mediated_match",
    "ambiguous_namespace_match",
    "conflicted_namespace_match",
    "unresolved_namespace_state",
    "not_applicable",
    "deferred",
}

ALLOWED_TOPOLOGY_VALIDATION_STATUS = {
    "passed",
    "passed_with_note",
    "failed",
    "not_applicable",
    "deferred_by_policy",
}

PROHIBITED_TOPOLOGY_VALIDATION_STATUS = {
    "preserved",
    "supported",
    "indexed_with_note",
}


@dataclass(frozen=True)
class TopologyPolicyCheck:
    """Single policy preflight check."""

    check_id: str
    validation_group: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class TopologyPolicyPreflightResult:
    """Policy preflight result."""

    policy_path: Path
    policy_id: str
    topology_build_id: str
    validation_status: str
    checks: tuple[TopologyPolicyCheck, ...]


def load_topology_policy(path: str | Path) -> dict[str, Any]:
    """Load a topology derivation policy JSON file."""

    policy_path = Path(path)
    if not policy_path.is_file():
        raise FileNotFoundError(f"Topology policy JSON does not exist: {policy_path}")

    try:
        payload = json.loads(policy_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid topology policy JSON: {policy_path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"Topology policy JSON must contain an object: {policy_path}")

    return payload


def iter_enabled_relationship_families(policy: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    """Return enabled relationship-family declarations."""

    families = policy.get("enabled_relationship_families", ())
    if not isinstance(families, list):
        raise ValueError("enabled_relationship_families must be a list.")
    return tuple(family for family in families if isinstance(family, dict))


def validate_policy_structure(policy: dict[str, Any]) -> tuple[TopologyPolicyCheck, ...]:
    """Validate required policy shape and top-level identity fields."""

    checks: list[TopologyPolicyCheck] = []

    _add_check(
        checks,
        "policy_top_level_keys",
        "policy_structure",
        REQUIRED_TOP_LEVEL_KEYS <= set(policy),
        "Policy contains all required top-level keys.",
        sorted(REQUIRED_TOP_LEVEL_KEYS),
        sorted(policy),
    )

    identity = policy.get("policy_identity", {})
    _add_check(
        checks,
        "policy_identity_is_object",
        "policy_structure",
        isinstance(identity, dict),
        "policy_identity is an object.",
        "dict",
        type(identity).__name__,
    )

    if isinstance(identity, dict):
        _add_check(
            checks,
            "policy_identity_required_keys",
            "policy_structure",
            REQUIRED_POLICY_IDENTITY_KEYS <= set(identity),
            "policy_identity contains all required keys.",
            sorted(REQUIRED_POLICY_IDENTITY_KEYS),
            sorted(identity),
        )

    required_inputs = policy.get("required_inputs", {})
    _add_check(
        checks,
        "required_inputs_is_object",
        "policy_structure",
        isinstance(required_inputs, dict) and bool(required_inputs),
        "required_inputs is a non-empty object.",
        "non-empty dict",
        _shape(required_inputs),
    )

    strategy_profiles = policy.get("relationship_strategy_profiles", {})
    _add_check(
        checks,
        "strategy_profiles_is_object",
        "policy_structure",
        isinstance(strategy_profiles, dict) and bool(strategy_profiles),
        "relationship_strategy_profiles is a non-empty object.",
        "non-empty dict",
        _shape(strategy_profiles),
    )

    families = policy.get("enabled_relationship_families", ())
    _add_check(
        checks,
        "enabled_families_is_list",
        "policy_structure",
        isinstance(families, list) and bool(families),
        "enabled_relationship_families is a non-empty list.",
        "non-empty list",
        _shape(families),
    )

    if isinstance(families, list):
        for idx, family in enumerate(families):
            family_id = (
                family.get("relationship_family_id", f"index_{idx}")
                if isinstance(family, dict)
                else f"index_{idx}"
            )
            _add_check(
                checks,
                f"enabled_family_shape__{family_id}",
                "policy_structure",
                isinstance(family, dict),
                "Enabled relationship family is an object.",
                "dict",
                type(family).__name__,
            )
            if isinstance(family, dict):
                _add_check(
                    checks,
                    f"enabled_family_required_keys__{family_id}",
                    "policy_structure",
                    REQUIRED_ENABLED_FAMILY_KEYS <= set(family),
                    "Enabled relationship family contains required keys.",
                    sorted(REQUIRED_ENABLED_FAMILY_KEYS),
                    sorted(family),
                )
                _add_check(
                    checks,
                    f"enabled_family_grouping_keys__{family_id}",
                    "policy_structure",
                    isinstance(family.get("grouping_keys"), list)
                    and bool(family.get("grouping_keys")),
                    "Enabled relationship family declares non-empty grouping_keys.",
                    "non-empty list",
                    family.get("grouping_keys"),
                )

    return tuple(checks)


def validate_strategy_profile_references(
    policy: dict[str, Any],
) -> tuple[TopologyPolicyCheck, ...]:
    """Validate enabled families reference declared strategy profiles."""

    checks: list[TopologyPolicyCheck] = []
    profiles = policy.get("relationship_strategy_profiles", {})
    profile_names = set(profiles) if isinstance(profiles, dict) else set()

    for family in iter_enabled_relationship_families(policy):
        family_id = str(family.get("relationship_family_id", ""))
        profile_name = str(family.get("strategy_profile", ""))
        _add_check(
            checks,
            f"strategy_profile_reference__{family_id}",
            "policy_strategy_profiles",
            profile_name in profile_names,
            "Enabled relationship family references a declared strategy profile.",
            sorted(profile_names),
            profile_name,
        )

    return tuple(checks)


def validate_policy_vocabulary(policy: dict[str, Any]) -> tuple[TopologyPolicyCheck, ...]:
    """Validate v1 policy vocabulary against schema-recognized values."""

    checks: list[TopologyPolicyCheck] = []
    prohibited = set(policy.get("prohibited_relationship_families", ()))

    for family in iter_enabled_relationship_families(policy):
        family_id = str(family.get("relationship_family_id", ""))
        _add_check(
            checks,
            f"enabled_family_not_prohibited__{family_id}",
            "policy_vocabulary",
            family_id not in prohibited,
            "Enabled relationship family is not prohibited.",
            "not in prohibited_relationship_families",
            family_id,
        )
        _add_check(
            checks,
            f"topology_dimension_vocab__{family_id}",
            "policy_vocabulary",
            family.get("topology_dimension") in ALLOWED_TOPOLOGY_DIMENSIONS,
            "topology_dimension is schema-recognized.",
            sorted(ALLOWED_TOPOLOGY_DIMENSIONS),
            family.get("topology_dimension"),
        )
        _add_check(
            checks,
            f"relationship_kind_vocab__{family_id}",
            "policy_vocabulary",
            family.get("relationship_kind") in ALLOWED_RELATIONSHIP_KINDS,
            "relationship_kind is schema-recognized.",
            sorted(ALLOWED_RELATIONSHIP_KINDS),
            family.get("relationship_kind"),
        )
        _add_check(
            checks,
            f"derivation_basis_vocab__{family_id}",
            "policy_vocabulary",
            family.get("derivation_basis") in ALLOWED_DERIVATION_BASES,
            "derivation_basis is schema-recognized.",
            sorted(ALLOWED_DERIVATION_BASES),
            family.get("derivation_basis"),
        )

    profiles = policy.get("relationship_strategy_profiles", {})
    if isinstance(profiles, dict):
        for profile_name, profile in profiles.items():
            if not isinstance(profile, dict):
                _add_check(
                    checks,
                    f"strategy_profile_vocab_shape__{profile_name}",
                    "policy_vocabulary",
                    False,
                    "Strategy profile is an object.",
                    "dict",
                    type(profile).__name__,
                )
                continue

            _add_check(
                checks,
                f"relationship_scope_vocab__{profile_name}",
                "policy_vocabulary",
                profile.get("relationship_scope") in ALLOWED_RELATIONSHIP_SCOPES,
                "relationship_scope is schema-recognized.",
                sorted(ALLOWED_RELATIONSHIP_SCOPES),
                profile.get("relationship_scope"),
            )
            _add_check(
                checks,
                f"source_identity_expansion_status_vocab__{profile_name}",
                "policy_vocabulary",
                profile.get("source_identity_expansion_status")
                in ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS,
                "source_identity_expansion_status is schema-recognized.",
                sorted(ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS),
                profile.get("source_identity_expansion_status"),
            )
            _add_check(
                checks,
                f"statistical_testing_status_vocab__{profile_name}",
                "policy_vocabulary",
                profile.get("statistical_testing_status")
                in ALLOWED_STATISTICAL_TESTING_STATUS,
                "statistical_testing_status is schema-recognized.",
                sorted(ALLOWED_STATISTICAL_TESTING_STATUS),
                profile.get("statistical_testing_status"),
            )
            _add_check(
                checks,
                f"namespace_mediation_status_vocab__{profile_name}",
                "policy_vocabulary",
                profile.get("namespace_mediation_status")
                in ALLOWED_NAMESPACE_MEDIATION_STATUS,
                "namespace_mediation_status is schema-recognized.",
                sorted(ALLOWED_NAMESPACE_MEDIATION_STATUS),
                profile.get("namespace_mediation_status"),
            )

    expansion_policy = policy.get("source_identity_expansion_policy", {})
    if isinstance(expansion_policy, dict):
        _add_check(
            checks,
            "expansion_status_for_v1_vocab",
            "policy_vocabulary",
            expansion_policy.get("expansion_status_for_v1")
            in ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS,
            "source_identity_expansion_policy.expansion_status_for_v1 is schema-recognized.",
            sorted(ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS),
            expansion_policy.get("expansion_status_for_v1"),
        )
        _add_check(
            checks,
            "controlled_expansion_status_vocab",
            "policy_vocabulary",
            expansion_policy.get("controlled_expansion_status")
            in ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS,
            "source_identity_expansion_policy.controlled_expansion_status is schema-recognized.",
            sorted(ALLOWED_SOURCE_IDENTITY_EXPANSION_STATUS),
            expansion_policy.get("controlled_expansion_status"),
        )

    namespace_policy = policy.get("namespace_mediation_policy", {})
    if isinstance(namespace_policy, dict):
        _add_check(
            checks,
            "namespace_mediation_mode_vocab",
            "policy_vocabulary",
            namespace_policy.get("namespace_mediation_mode")
            in ALLOWED_NAMESPACE_MEDIATION_STATUS,
            "namespace_mediation_policy.namespace_mediation_mode is schema-recognized.",
            sorted(ALLOWED_NAMESPACE_MEDIATION_STATUS),
            namespace_policy.get("namespace_mediation_mode"),
        )
        match_types = namespace_policy.get("allowed_match_types_v1", ())
        observed_match_types = tuple(match_types) if isinstance(match_types, list) else ()
        _add_check(
            checks,
            "allowed_match_types_v1_vocab",
            "policy_vocabulary",
            set(observed_match_types) <= ALLOWED_MATCH_TYPES,
            "namespace_mediation_policy.allowed_match_types_v1 values are schema-recognized.",
            sorted(ALLOWED_MATCH_TYPES),
            sorted(observed_match_types),
        )

    validation_status_policy = policy.get("validation_status_policy", {})
    if isinstance(validation_status_policy, dict):
        observed = set(validation_status_policy.get("topology_validation_status_values", ()))
        _add_check(
            checks,
            "topology_validation_status_values_vocab",
            "policy_vocabulary",
            observed <= ALLOWED_TOPOLOGY_VALIDATION_STATUS,
            "Topology-layer validation status values are schema-recognized.",
            sorted(ALLOWED_TOPOLOGY_VALIDATION_STATUS),
            sorted(observed),
        )

        prohibited_observed = set(
            validation_status_policy.get("prohibited_topology_validation_status_values", ())
        )
        _add_check(
            checks,
            "prohibited_topology_validation_status_values_declared",
            "policy_vocabulary",
            PROHIBITED_TOPOLOGY_VALIDATION_STATUS <= prohibited_observed,
            "Upstream assertion statuses are prohibited as topology-layer validation statuses.",
            sorted(PROHIBITED_TOPOLOGY_VALIDATION_STATUS),
            sorted(prohibited_observed),
        )

    return tuple(checks)


def preflight_policy(path: str | Path) -> TopologyPolicyPreflightResult:
    """Run all policy preflight checks."""

    policy_path = Path(path)
    policy = load_topology_policy(policy_path)

    checks = (
        list(validate_policy_structure(policy))
        + list(validate_strategy_profile_references(policy))
        + list(validate_policy_vocabulary(policy))
    )

    identity = policy.get("policy_identity", {})
    if not isinstance(identity, dict):
        identity = {}

    return TopologyPolicyPreflightResult(
        policy_path=policy_path,
        policy_id=str(identity.get("policy_id", "")),
        topology_build_id=str(identity.get("topology_build_id", "")),
        validation_status=_validation_status(checks),
        checks=tuple(checks),
    )


def failed_checks(
    checks: Iterable[TopologyPolicyCheck],
) -> tuple[TopologyPolicyCheck, ...]:
    """Return failed checks from a policy preflight check iterable."""

    return tuple(check for check in checks if check.status == VALIDATION_STATUS_FAILED)


def _add_check(
    checks: list[TopologyPolicyCheck],
    check_id: str,
    group: str,
    passed: bool,
    message: str,
    expected: object = "",
    observed: object = "",
) -> None:
    checks.append(
        TopologyPolicyCheck(
            check_id=check_id,
            validation_group=group,
            status=VALIDATION_STATUS_PASSED if passed else VALIDATION_STATUS_FAILED,
            message=message,
            expected=_stringify(expected),
            observed=_stringify(observed),
        )
    )


def _validation_status(checks: Iterable[TopologyPolicyCheck]) -> str:
    return (
        VALIDATION_STATUS_FAILED
        if any(check.status == VALIDATION_STATUS_FAILED for check in checks)
        else VALIDATION_STATUS_PASSED
    )


def _shape(value: object) -> str:
    if isinstance(value, dict):
        return f"dict[{len(value)}]"
    if isinstance(value, list):
        return f"list[{len(value)}]"
    return type(value).__name__


def _stringify(value: object) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except TypeError:
        return str(value)

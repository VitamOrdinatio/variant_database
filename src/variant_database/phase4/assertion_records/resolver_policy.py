"""Phase 4.3 Assertion Record resolver policy.

The resolver policy classifies producer assertion registration types. It does not
assign biological truth, clinical actionability, causality, topology, geometry,
surface, projection, or RDGP authority.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

SUPPORTED = "supported"
INDEXED_WITH_NOTE = "indexed_with_note"
DEFERRED = "deferred"
UNSUPPORTED = "unsupported"

SOURCE_IDENTITY_REQUIRED = "required"
SOURCE_IDENTITY_OPTIONAL = "optional"
SOURCE_IDENTITY_NOT_APPLICABLE = "not_applicable"

RESOLVER_POLICY: dict[str, dict[str, dict[str, str]]] = {
    "VAP": {
        "variant_observation": {
            "resolution_status": SUPPORTED,
            "relationship_class": "variant_observation",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve observed variant evidence without interpretation.",
        },
        "variant_normalization": {
            "resolution_status": SUPPORTED,
            "relationship_class": "variant_normalization",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve normalization claim and source-native identity linkage.",
        },
        "variant_interpretation": {
            "resolution_status": SUPPORTED,
            "relationship_class": "variant_interpretation",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve interpretation label/context without assigning truth.",
        },
        "variant_prioritization": {
            "resolution_status": INDEXED_WITH_NOTE,
            "relationship_class": "variant_prioritization",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Index producer priority/routing context without adopting ranking authority.",
        },
        "validation": {
            "resolution_status": INDEXED_WITH_NOTE,
            "relationship_class": "producer_validation",
            "source_identity_set_status": SOURCE_IDENTITY_OPTIONAL,
            "note": "Preserve producer validation assertion as evidence context.",
        },
        "candidate_routing": {
            "resolution_status": DEFERRED,
            "relationship_class": "candidate_routing",
            "source_identity_set_status": SOURCE_IDENTITY_OPTIONAL,
            "note": "Defer routing semantics while accounting for the producer assertion.",
        },
    },
    "GSC": {
        "phenotype_gene_semantic_prior": {
            "resolution_status": SUPPORTED,
            "relationship_class": "phenotype_gene_semantic_prior",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve phenotype-scoped gene prior, not general gene truth.",
        },
        "phenotype_gene_provenance": {
            "resolution_status": SUPPORTED,
            "relationship_class": "phenotype_gene_provenance",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve provenance attached to phenotype-gene evidence.",
        },
        "source_gene_relationship": {
            "resolution_status": SUPPORTED,
            "relationship_class": "source_gene_relationship",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve source-scoped gene relationship.",
        },
        "aggregation_support": {
            "resolution_status": INDEXED_WITH_NOTE,
            "relationship_class": "aggregation_support",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve producer aggregation support without deriving VDB topology.",
        },
        "source_contribution_topology": {
            "resolution_status": INDEXED_WITH_NOTE,
            "relationship_class": "producer_source_contribution_topology",
            "source_identity_set_status": SOURCE_IDENTITY_REQUIRED,
            "note": "Preserve GSC-emitted topology-like assertion; do not treat as VDB Evidence Topology.",
        },
        "producer_contract_validation": {
            "resolution_status": INDEXED_WITH_NOTE,
            "relationship_class": "producer_contract_validation",
            "source_identity_set_status": SOURCE_IDENTITY_NOT_APPLICABLE,
            "note": "Artifact-level validation assertion without source identity set obligation.",
        },
    },
}

# Tests may accept either RESOLVER_POLICY or RESOLVER_STATUS. Keep both names.
RESOLVER_STATUS = RESOLVER_POLICY


def _producer_key(producer_family: str) -> str:
    return (producer_family or "").strip().upper()


def resolve_assertion(producer_family: str, assertion_type: str) -> dict[str, str]:
    """Return the v1 resolver policy entry for a producer assertion type."""
    producer_key = _producer_key(producer_family)
    assertion_key = (assertion_type or "").strip()
    entry = RESOLVER_POLICY.get(producer_key, {}).get(assertion_key)
    if entry is None:
        return {
            "resolution_status": UNSUPPORTED,
            "relationship_class": assertion_key or "unsupported_assertion",
            "source_identity_set_status": SOURCE_IDENTITY_OPTIONAL,
            "note": "Unsupported assertion type is explicitly accounted for and not silently dropped.",
        }
    return deepcopy(entry)


def resolution_status(producer_family: str, assertion_type: str) -> str:
    """Return only the resolver status for convenience."""
    return resolve_assertion(producer_family, assertion_type)["resolution_status"]


def relationship_class(producer_family: str, assertion_type: str) -> str:
    """Return the declared relationship class for an assertion type."""
    return resolve_assertion(producer_family, assertion_type)["relationship_class"]


def source_identity_set_status(producer_family: str, assertion_type: str) -> str:
    """Return source identity set applicability for an assertion type."""
    return resolve_assertion(producer_family, assertion_type)["source_identity_set_status"]


def is_indexable_status(status: str) -> bool:
    """Return whether the status should still produce an accountable index row."""
    return status in {SUPPORTED, INDEXED_WITH_NOTE, DEFERRED, UNSUPPORTED}

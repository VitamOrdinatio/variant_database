"""Deterministic topology identity helpers.

Evidence Topology identities must be stable under fixed inputs and must not
incorporate row order, filesystem traversal order, timestamps, output position,
or expanded Source Identity Set values.
"""
from __future__ import annotations

from collections.abc import Iterable
import hashlib
from typing import Any


DEFAULT_RELATIONSHIP_ID_PREFIX = "topology_rel_"
DEFAULT_MEMBER_ID_PREFIX = "topology_member_"
DEFAULT_BASIS_COMPONENT_ID_PREFIX = "topology_basis_"
DEFAULT_ROW_ID_DIGEST_LENGTH = 24
EMPTY_STRING_TOKEN = "__EMPTY__"
NULL_TOKEN = "__NULL__"
MULTIVALUE_SEPARATOR = "|"
COMPONENT_SEPARATOR = "\x1f"


def normalize_identity_part(value: Any) -> str:
    """Normalize one deterministic identity component.

    The normalization intentionally mirrors the Phase 4.4 derivation policy:
    trim whitespace, distinguish null from empty string, and sort simple
    pipe-delimited multivalue cells.
    """

    if value is None:
        return NULL_TOKEN

    text = str(value).strip()
    if text == "":
        return EMPTY_STRING_TOKEN

    if MULTIVALUE_SEPARATOR in text:
        parts = sorted(
            part.strip() if part.strip() else EMPTY_STRING_TOKEN
            for part in text.split(MULTIVALUE_SEPARATOR)
        )
        return MULTIVALUE_SEPARATOR.join(parts)

    return text


def normalize_identity_parts(parts: Iterable[Any]) -> tuple[str, ...]:
    """Normalize an ordered sequence of identity components."""

    return tuple(normalize_identity_part(part) for part in parts)


def stable_hash_payload(parts: Iterable[Any]) -> str:
    """Return the canonical payload string used for deterministic hashing."""

    return COMPONENT_SEPARATOR.join(normalize_identity_parts(parts))


def stable_digest(
    parts: Iterable[Any],
    *,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a truncated SHA256 digest for normalized identity parts."""

    payload = stable_hash_payload(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:digest_length]


def make_normalized_grouping_key(
    row: dict[str, Any],
    grouping_keys: Iterable[str],
) -> str:
    """Return a stable grouping-key string for a row and grouping columns.

    The grouping key order is the policy-declared grouping key order. It does
    not depend on dictionary iteration order.
    """

    return MULTIVALUE_SEPARATOR.join(
        f"{key}={normalize_identity_part(row.get(key))}" for key in grouping_keys
    )


def make_topology_relationship_id(
    *,
    topology_build_id: str,
    relationship_family_id: str,
    topology_dimension: str,
    relationship_kind: str,
    derivation_basis: str,
    normalized_grouping_key: str,
    member_identifiers: Iterable[Any],
    prefix: str = DEFAULT_RELATIONSHIP_ID_PREFIX,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a deterministic topology relationship identifier."""

    members = sorted(normalize_identity_part(member) for member in member_identifiers)
    payload_parts = [
        topology_build_id,
        relationship_family_id,
        topology_dimension,
        relationship_kind,
        derivation_basis,
        normalized_grouping_key,
        *members,
    ]
    return f"{prefix}{stable_digest(payload_parts, digest_length=digest_length)}"


def make_topology_member_id(
    *,
    topology_relationship_id: str,
    member_type: str,
    member_role: str,
    member_reference: str,
    source_assertion_id: str = "",
    source_identity_set_id: str = "",
    prefix: str = DEFAULT_MEMBER_ID_PREFIX,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a deterministic topology relationship member identifier."""

    payload_parts = [
        topology_relationship_id,
        member_type,
        member_role,
        member_reference,
        source_assertion_id,
        source_identity_set_id,
    ]
    digest = stable_digest(payload_parts, digest_length=digest_length)
    return f"{prefix}{digest}"


def make_topology_basis_component_id(
    *,
    topology_relationship_id: str,
    basis_component_type: str,
    basis_component_role: str,
    basis_component_value: str = "",
    basis_component_reference: str = "",
    basis_component_namespace: str = "",
    source_assertion_id: str = "",
    source_identity_set_id: str = "",
    prefix: str = DEFAULT_BASIS_COMPONENT_ID_PREFIX,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a deterministic topology basis component identifier."""

    payload_parts = [
        topology_relationship_id,
        basis_component_type,
        basis_component_role,
        basis_component_value,
        basis_component_reference,
        basis_component_namespace,
        source_assertion_id,
        source_identity_set_id,
    ]
    digest = stable_digest(payload_parts, digest_length=digest_length)
    return f"{prefix}{digest}"


def make_topology_row_id(
    prefix: str,
    parts: Iterable[Any],
    *,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a deterministic helper row identifier.

    This generic helper remains for backwards compatibility in tests and future
    internal callers. New relationship member and basis component code should
    prefer the semantic helpers above.
    """

    return f"{prefix}{stable_digest(parts, digest_length=digest_length)}"

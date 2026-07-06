"""Deterministic topology identity helpers.

Evidence Topology identities must be stable under fixed inputs and must not
incorporate row order, filesystem traversal order, timestamps, or expanded
Source Identity Set values.
"""
from __future__ import annotations

from collections.abc import Iterable
import hashlib
from typing import Any


DEFAULT_RELATIONSHIP_ID_PREFIX = "topology_rel_"
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


def make_normalized_grouping_key(
    row: dict[str, Any],
    grouping_keys: Iterable[str],
) -> str:
    """Return a stable grouping-key string for a row and grouping columns."""

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
        normalize_identity_part(topology_build_id),
        normalize_identity_part(relationship_family_id),
        normalize_identity_part(topology_dimension),
        normalize_identity_part(relationship_kind),
        normalize_identity_part(derivation_basis),
        normalize_identity_part(normalized_grouping_key),
        *members,
    ]
    digest = hashlib.sha256(COMPONENT_SEPARATOR.join(payload_parts).encode("utf-8")).hexdigest()
    return f"{prefix}{digest[:digest_length]}"


def make_topology_row_id(
    prefix: str,
    parts: Iterable[Any],
    *,
    digest_length: int = DEFAULT_ROW_ID_DIGEST_LENGTH,
) -> str:
    """Return a deterministic helper row identifier for members or basis rows."""

    normalized_parts = [normalize_identity_part(part) for part in parts]
    digest = hashlib.sha256(
        COMPONENT_SEPARATOR.join(normalized_parts).encode("utf-8")
    ).hexdigest()
    return f"{prefix}{digest[:digest_length]}"

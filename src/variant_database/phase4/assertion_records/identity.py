"""Deterministic identity helpers for Phase 4.3 Assertion Records.

Identity doctrine:

* ``source_assertion_key`` preserves producer/source claim identity.
* ``assertion_id`` preserves corpus-indexed Assertion Record identity.

The corpus generation participates in ``assertion_id`` so the same producer claim
can be represented independently in different governed corpus scopes.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def _normalize(value: Any) -> str:
    """Return a deterministic string representation for identifier material."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def stable_hash(parts: dict[str, Any] | list[Any] | tuple[Any, ...] | str, *, prefix: str = "") -> str:
    """Return a stable SHA-256 based identifier for structured material."""
    payload = json.dumps(parts, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}{digest}" if prefix else digest


def _require(name: str, value: Any) -> str:
    normalized = _normalize(value)
    if not normalized:
        raise ValueError(f"{name} is required for Assertion Record identity generation")
    return normalized


def make_source_assertion_key(
    *,
    registration_unit_id: str,
    source_package_id: str,
    source_artifact_id: str,
    source_assertion_registration_id: str,
    assertion_type: str,
    producer_family: str,
) -> str:
    """Create a stable producer/source claim key.

    The key is source-scoped and excludes ``corpus_generation_id`` by design.
    """
    material = {
        "registration_unit_id": _require("registration_unit_id", registration_unit_id),
        "source_package_id": _require("source_package_id", source_package_id),
        "source_artifact_id": _require("source_artifact_id", source_artifact_id),
        "source_assertion_registration_id": _require(
            "source_assertion_registration_id", source_assertion_registration_id
        ),
        "assertion_type": _require("assertion_type", assertion_type),
        "producer_family": _require("producer_family", producer_family).upper(),
    }
    return stable_hash(material, prefix="sak_")


def make_assertion_id(
    *,
    corpus_generation_id: str,
    registration_unit_id: str,
    source_assertion_key: str,
    assertion_type: str,
    producer_family: str,
) -> str:
    """Create a stable corpus-indexed Assertion Record identifier."""
    material = {
        "corpus_generation_id": _require("corpus_generation_id", corpus_generation_id),
        "registration_unit_id": _require("registration_unit_id", registration_unit_id),
        "source_assertion_key": _require("source_assertion_key", source_assertion_key),
        "assertion_type": _require("assertion_type", assertion_type),
        "producer_family": _require("producer_family", producer_family).upper(),
    }
    return stable_hash(material, prefix="ar_")

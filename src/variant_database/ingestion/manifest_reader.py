"""Manifest readers for VDB ingestion.

This module reads producer-emitted package manifests and summarizes their
declared topology.

It does not mutate producer artifacts.
It does not interpret biological evidence.
It does not create Evidence Objects.
It does not persist records.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


ENTITY_INVENTORY_FILENAME = "entity_inventory.json"


@dataclass(frozen=True)
class EntityInventorySummary:
    """Summary of an entity_inventory.json manifest."""

    manifest_path: str
    manifest_exists: bool
    top_level_keys: list[str]
    declared_record_count: int
    declared_artifact_paths: list[str]
    declared_entity_domains: list[str]


def read_json_file(path: Path | str) -> Any:
    """Read a JSON file."""
    json_path = Path(path)

    with json_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _collect_strings_with_pathish_values(value: Any) -> list[str]:
    """Collect string values that look like artifact paths."""
    paths: list[str] = []

    if isinstance(value, dict):
        for item in value.values():
            paths.extend(_collect_strings_with_pathish_values(item))
    elif isinstance(value, list):
        for item in value:
            paths.extend(_collect_strings_with_pathish_values(item))
    elif isinstance(value, str):
        if "/" in value or value.endswith((".tsv", ".json", ".md", ".txt")):
            paths.append(value)

    return paths


def _collect_domain_like_keys(value: Any) -> list[str]:
    """Collect conservative domain-like dictionary keys."""
    domains: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            key_s = str(key)
            key_l = key_s.lower()

            if any(
                token in key_l
                for token in (
                    "coding",
                    "noncoding",
                    "normalization",
                    "observation",
                    "prioritization",
                    "routing",
                    "validation",
                    "context",
                    "semantic",
                    "variant",
                    "gene",
                    "phenotype",
                )
            ):
                domains.append(key_s)

            domains.extend(_collect_domain_like_keys(item))
    elif isinstance(value, list):
        for item in value:
            domains.extend(_collect_domain_like_keys(item))

    return domains


def _count_declared_records(value: Any) -> int:
    """Count conservative record-like declarations in a JSON object."""
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        for key in ("entities", "artifacts", "records", "inventory"):
            candidate = value.get(key)
            if isinstance(candidate, list):
                return len(candidate)
        return len(value)
    return 0


def summarize_entity_inventory(manifest_path: Path | str) -> EntityInventorySummary:
    """Read and summarize an entity_inventory.json manifest."""
    path = Path(manifest_path).expanduser().resolve()

    if not path.exists():
        return EntityInventorySummary(
            manifest_path=str(path),
            manifest_exists=False,
            top_level_keys=[],
            declared_record_count=0,
            declared_artifact_paths=[],
            declared_entity_domains=[],
        )

    if not path.is_file():
        raise IsADirectoryError(f"Manifest path is not a file: {path}")

    payload = read_json_file(path)

    top_level_keys = sorted(payload.keys()) if isinstance(payload, dict) else []
    declared_artifact_paths = sorted(set(_collect_strings_with_pathish_values(payload)))
    declared_entity_domains = sorted(set(_collect_domain_like_keys(payload)))
    declared_record_count = _count_declared_records(payload)

    return EntityInventorySummary(
        manifest_path=str(path),
        manifest_exists=True,
        top_level_keys=top_level_keys,
        declared_record_count=declared_record_count,
        declared_artifact_paths=declared_artifact_paths,
        declared_entity_domains=declared_entity_domains,
    )


def entity_inventory_path_for_package(package_path: Path | str) -> Path:
    """Return the conventional entity_inventory.json path for a package."""
    return Path(package_path).expanduser().resolve() / ENTITY_INVENTORY_FILENAME

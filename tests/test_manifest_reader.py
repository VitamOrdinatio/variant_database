from __future__ import annotations

import json
from pathlib import Path

import pytest

from variant_database.ingestion.manifest_reader import (
    entity_inventory_path_for_package,
    summarize_entity_inventory,
)


def test_missing_entity_inventory_summary(tmp_path: Path) -> None:
    missing = tmp_path / "entity_inventory.json"

    summary = summarize_entity_inventory(missing)

    assert summary.manifest_exists is False
    assert summary.top_level_keys == []
    assert summary.declared_record_count == 0
    assert summary.declared_artifact_paths == []
    assert summary.declared_entity_domains == []


def test_rejects_directory_manifest_path(tmp_path: Path) -> None:
    with pytest.raises(IsADirectoryError):
        summarize_entity_inventory(tmp_path)


def test_entity_inventory_path_for_package(tmp_path: Path) -> None:
    package = tmp_path / "tep"

    path = entity_inventory_path_for_package(package)

    assert path == package.resolve() / "entity_inventory.json"


def test_summarize_entity_inventory_extracts_declared_topology(tmp_path: Path) -> None:
    manifest = tmp_path / "entity_inventory.json"
    payload = {
        "producer": "VAP",
        "artifacts": [
            {
                "domain": "coding_interpretation",
                "path": "entities/coding_interpretation/stage_09_coding_interpreted.tsv",
            },
            {
                "domain": "validation",
                "path": "entities/validation/stage_12_validation_candidates.tsv",
            },
        ],
        "domains": {
            "coding_interpretation": {},
            "validation": {},
        },
    }
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    summary = summarize_entity_inventory(manifest)

    assert summary.manifest_exists is True
    assert summary.top_level_keys == ["artifacts", "domains", "producer"]
    assert summary.declared_record_count == 2
    assert summary.declared_artifact_paths == [
        "entities/coding_interpretation/stage_09_coding_interpreted.tsv",
        "entities/validation/stage_12_validation_candidates.tsv",
    ]
    assert "coding_interpretation" in summary.declared_entity_domains
    assert "validation" in summary.declared_entity_domains

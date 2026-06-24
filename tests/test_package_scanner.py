from __future__ import annotations

from pathlib import Path

import pytest

from variant_database.ingestion.package_scanner import scan_package


def test_scan_missing_package(tmp_path: Path) -> None:
    missing = tmp_path / "missing_tep"

    inventory = scan_package(missing)

    assert inventory.package_exists is False
    assert inventory.artifact_count == 0
    assert inventory.artifacts == []


def test_scan_rejects_file_path(tmp_path: Path) -> None:
    file_path = tmp_path / "not_a_package.txt"
    file_path.write_text("not a package", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        scan_package(file_path)


def test_scan_package_inventory_is_deterministic(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    (package / "data.tsv").write_text("a\tb\n1\t2\n", encoding="utf-8")

    first = scan_package(package)
    second = scan_package(package)

    assert first == second
    assert first.package_exists is True
    assert first.artifact_count == 2
    assert first.manifest_paths == ["entity_inventory.json"]
    assert [a.relative_path for a in first.artifacts] == [
        "data.tsv",
        "entity_inventory.json",
    ]
    assert all(a.sha256 for a in first.artifacts)


def test_scan_ignores_emulation_housekeeping_files(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "_emulation_manifest.json").write_text("{}", encoding="utf-8")
    (package / "_emulation_report.md").write_text("report", encoding="utf-8")
    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")

    inventory = scan_package(package)

    assert inventory.artifact_count == 1
    assert inventory.manifest_paths == ["entity_inventory.json"]
    assert [a.relative_path for a in inventory.artifacts] == ["entity_inventory.json"]
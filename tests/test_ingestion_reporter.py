from __future__ import annotations

import json
from pathlib import Path

from variant_database.ingestion.ingestion_reporter import (
    inventory_report_dict,
    inventory_report_markdown,
    write_inventory_reports,
)
from variant_database.ingestion.package_scanner import scan_package


def test_inventory_report_dict_is_deterministic(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    (package / "data.tsv").write_text("a\tb\n1\t2\n", encoding="utf-8")

    inventory = scan_package(package)

    first = inventory_report_dict(inventory)
    second = inventory_report_dict(inventory)

    assert first == second
    assert first["report_type"] == "vdb_ingestion_inventory"
    assert first["report_version"] == "1.0"
    assert first["artifact_count"] == 2
    assert first["manifest_count"] == 1


def test_inventory_report_markdown_contains_expected_sections(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    inventory = scan_package(package)

    markdown = inventory_report_markdown(inventory)

    assert "# VDB Ingestion Inventory Report" in markdown
    assert "## Package" in markdown
    assert "## Manifests" in markdown
    assert "## Artifacts" in markdown
    assert "entity_inventory.json" in markdown


def test_write_inventory_reports(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    output_dir = tmp_path / "reports"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    inventory = scan_package(package)

    json_path, markdown_path = write_inventory_reports(inventory, output_dir)

    assert json_path.exists()
    assert markdown_path.exists()

    report = json.loads(json_path.read_text(encoding="utf-8"))

    assert report["report_type"] == "vdb_ingestion_inventory"
    assert report["artifact_count"] == 1
    assert markdown_path.read_text(encoding="utf-8").startswith(
        "# VDB Ingestion Inventory Report"
    )


def test_write_inventory_reports_is_deterministic(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    output_a = tmp_path / "reports_a"
    output_b = tmp_path / "reports_b"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    (package / "lineage_manifest.json").write_text("{}", encoding="utf-8")
    inventory = scan_package(package)

    json_a, md_a = write_inventory_reports(inventory, output_a)
    json_b, md_b = write_inventory_reports(inventory, output_b)

    assert json_a.read_text(encoding="utf-8") == json_b.read_text(encoding="utf-8")
    assert md_a.read_text(encoding="utf-8") == md_b.read_text(encoding="utf-8")

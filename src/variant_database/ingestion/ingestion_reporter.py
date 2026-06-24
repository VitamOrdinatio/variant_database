"""Deterministic ingestion inventory reporting.

This module converts read-only package inventories into human- and
machine-readable reports.

It does not mutate producer artifacts.
It does not interpret biological evidence.
It does not persist records.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any
import json

from variant_database.ingestion.package_scanner import PackageInventory


def inventory_report_dict(inventory: PackageInventory) -> dict[str, Any]:
    """Return a deterministic machine-readable report dictionary."""
    return {
        "report_type": "vdb_ingestion_inventory",
        "report_version": "1.0",
        "package_path": inventory.package_path,
        "package_exists": inventory.package_exists,
        "artifact_count": inventory.artifact_count,
        "manifest_count": len(inventory.manifest_paths),
        "manifest_paths": list(inventory.manifest_paths),
        "artifacts": [asdict(artifact) for artifact in inventory.artifacts],
    }


def write_inventory_json(
    inventory: PackageInventory,
    output_path: Path | str,
) -> Path:
    """Write a deterministic JSON inventory report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report = inventory_report_dict(inventory)
    path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return path


def inventory_report_markdown(inventory: PackageInventory) -> str:
    """Return a deterministic human-readable Markdown inventory report."""
    lines: list[str] = [
        "# VDB Ingestion Inventory Report",
        "",
        "## Package",
        "",
        f"- Package path: `{inventory.package_path}`",
        f"- Package exists: `{inventory.package_exists}`",
        f"- Artifact count: `{inventory.artifact_count}`",
        f"- Manifest count: `{len(inventory.manifest_paths)}`",
        "",
        "## Manifests",
        "",
    ]

    if inventory.manifest_paths:
        for manifest_path in inventory.manifest_paths:
            lines.append(f"- `{manifest_path}`")
    else:
        lines.append("- None detected")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "| Relative path | Size bytes | SHA256 |",
            "|---|---:|---|",
        ]
    )

    for artifact in inventory.artifacts:
        lines.append(
            f"| `{artifact.relative_path}` | "
            f"{artifact.size_bytes} | "
            f"`{artifact.sha256}` |"
        )

    lines.append("")
    return "\n".join(lines)


def write_inventory_markdown(
    inventory: PackageInventory,
    output_path: Path | str,
) -> Path:
    """Write a deterministic Markdown inventory report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        inventory_report_markdown(inventory),
        encoding="utf-8",
    )

    return path


def write_inventory_reports(
    inventory: PackageInventory,
    output_dir: Path | str,
    json_name: str = "inventory_report.json",
    markdown_name: str = "inventory_report.md",
) -> tuple[Path, Path]:
    """Write both JSON and Markdown inventory reports."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    json_path = write_inventory_json(inventory, directory / json_name)
    markdown_path = write_inventory_markdown(inventory, directory / markdown_name)

    return json_path, markdown_path

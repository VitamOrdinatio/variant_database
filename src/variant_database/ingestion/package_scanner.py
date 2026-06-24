"""Read-only package scanner for VDB ingestion.

This module performs structural inventory of a TEP package path.

It does not mutate producer artifacts.
It does not interpret biological evidence.
It does not persist records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import hashlib


IGNORED_ARTIFACTS = {
    "_emulation_manifest.json",
    "_emulation_report.md",
}

MANIFEST_FILENAMES = {
    "entity_inventory.json",
    "lineage_manifest.json",
    "validation_report.md",
    "manifest.json",
}


@dataclass(frozen=True)
class ArtifactInventory:
    """Inventory record for one file artifact."""

    relative_path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class PackageInventory:
    """Read-only inventory of a package directory."""

    package_path: str
    package_exists: bool
    artifact_count: int
    manifest_paths: list[str]
    artifacts: list[ArtifactInventory]


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA256 for a file without modifying it."""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_package(package_path: Path | str) -> PackageInventory:
    """Scan a package directory read-only and return deterministic inventory."""
    root = Path(package_path).expanduser().resolve()

    if not root.exists():
        return PackageInventory(
            package_path=str(root),
            package_exists=False,
            artifact_count=0,
            manifest_paths=[],
            artifacts=[],
        )

    if not root.is_dir():
        raise NotADirectoryError(f"Package path is not a directory: {root}")

    artifacts: list[ArtifactInventory] = []
    manifest_paths: list[str] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        rel = path.relative_to(root).as_posix()

        if path.name in IGNORED_ARTIFACTS:
            continue

        if path.name in MANIFEST_FILENAMES:
            manifest_paths.append(rel)

        artifacts.append(
            ArtifactInventory(
                relative_path=rel,
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
            )
        )

    return PackageInventory(
        package_path=str(root),
        package_exists=True,
        artifact_count=len(artifacts),
        manifest_paths=manifest_paths,
        artifacts=artifacts,
    )


def inventory_to_dict(inventory: PackageInventory) -> dict[str, Any]:
    """Convert inventory dataclasses to plain dictionaries."""
    return asdict(inventory)

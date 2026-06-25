"""Persistence repositories for VDB logical records."""

from __future__ import annotations

import hashlib
import sqlite3

from variant_database.ingestion.package_scanner import PackageInventory


def stable_hash(parts: list[str]) -> str:
    """Create a deterministic SHA256 ID from string parts."""
    payload = "\x1f".join(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def package_id_for_inventory(inventory: PackageInventory) -> str:
    """Derive a deterministic package ID from inventory content."""
    return stable_hash(
        [
            "tep_package",
            inventory.package_path,
            str(inventory.package_exists),
        ]
    )


def artifact_id_for_record(
    package_id: str,
    relative_path: str,
    sha256: str,
) -> str:
    """Derive a deterministic artifact ID."""
    return stable_hash(
        [
            "artifact",
            package_id,
            relative_path,
            sha256,
        ]
    )


def persist_package_inventory(
    connection: sqlite3.Connection,
    inventory: PackageInventory,
) -> str:
    """Persist a scanned package inventory and return its package ID."""
    package_id = package_id_for_inventory(inventory)
    manifest_paths = set(inventory.manifest_paths)

    connection.execute(
        """
        INSERT INTO tep_packages (
            package_id,
            package_path,
            package_exists,
            artifact_count,
            manifest_count
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(package_id) DO UPDATE SET
            package_path = excluded.package_path,
            package_exists = excluded.package_exists,
            artifact_count = excluded.artifact_count,
            manifest_count = excluded.manifest_count
        """,
        (
            package_id,
            inventory.package_path,
            int(inventory.package_exists),
            inventory.artifact_count,
            len(inventory.manifest_paths),
        ),
    )

    for artifact in inventory.artifacts:
        artifact_id = artifact_id_for_record(
            package_id=package_id,
            relative_path=artifact.relative_path,
            sha256=artifact.sha256,
        )

        connection.execute(
            """
            INSERT INTO artifacts (
                artifact_id,
                package_id,
                relative_path,
                size_bytes,
                sha256,
                is_manifest
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
                package_id = excluded.package_id,
                relative_path = excluded.relative_path,
                size_bytes = excluded.size_bytes,
                sha256 = excluded.sha256,
                is_manifest = excluded.is_manifest
            """,
            (
                artifact_id,
                package_id,
                artifact.relative_path,
                artifact.size_bytes,
                artifact.sha256,
                int(artifact.relative_path in manifest_paths),
            ),
        )

    connection.commit()
    return package_id


def get_package_record(
    connection: sqlite3.Connection,
    package_id: str,
) -> dict[str, object] | None:
    """Retrieve a persisted package record."""
    row = connection.execute(
        """
        SELECT
            package_id,
            package_path,
            package_exists,
            artifact_count,
            manifest_count
        FROM tep_packages
        WHERE package_id = ?
        """,
        (package_id,),
    ).fetchone()

    return dict(row) if row is not None else None


def list_artifact_records(
    connection: sqlite3.Connection,
    package_id: str,
) -> list[dict[str, object]]:
    """Retrieve persisted artifact records for a package."""
    rows = connection.execute(
        """
        SELECT
            artifact_id,
            package_id,
            relative_path,
            size_bytes,
            sha256,
            is_manifest
        FROM artifacts
        WHERE package_id = ?
        ORDER BY relative_path
        """,
        (package_id,),
    ).fetchall()

    return [dict(row) for row in rows]

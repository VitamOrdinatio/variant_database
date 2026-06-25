"""Schema creation utilities for VDB persistence."""

from __future__ import annotations

import sqlite3


SCHEMA_VERSION = "0.1.0"


def initialize_schema(connection: sqlite3.Connection) -> None:
    """Create the initial VDB persistence schema."""
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tep_packages (
            package_id TEXT PRIMARY KEY,
            package_path TEXT NOT NULL,
            package_exists INTEGER NOT NULL,
            artifact_count INTEGER NOT NULL,
            manifest_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS artifacts (
            artifact_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            relative_path TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            is_manifest INTEGER NOT NULL,
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id)
        );
        """
    )

    connection.execute(
        """
        INSERT INTO schema_metadata (key, value)
        VALUES ('schema_version', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (SCHEMA_VERSION,),
    )
    connection.commit()

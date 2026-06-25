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

        CREATE TABLE IF NOT EXISTS assertion_registrations (
            assertion_registration_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            artifact_id TEXT NOT NULL,
            surface_role TEXT NOT NULL,
            evidence_domain TEXT NOT NULL,
            producer_family TEXT NOT NULL,
            source_record_ref TEXT,
            assertion_type TEXT NOT NULL,
            participant_summary_json TEXT NOT NULL,
            support_ref_json TEXT NOT NULL,
            authority_context TEXT NOT NULL,
            uncertainty_context TEXT NOT NULL,
            registration_status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
        );

        CREATE TABLE IF NOT EXISTS source_identities (
            source_identity_id TEXT PRIMARY KEY,
            assertion_registration_id TEXT NOT NULL,
            identity_kind TEXT NOT NULL,
            participant_role TEXT NOT NULL,
            source_value TEXT NOT NULL,
            source_namespace TEXT NOT NULL,
            source_label TEXT,
            extraction_method TEXT NOT NULL,
            source_record_ref TEXT,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(assertion_registration_id)
                REFERENCES assertion_registrations(assertion_registration_id)
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

"""Assertion registration.

Assertion Registration is the VDB-owned custody record for
producer-emitted assertions.

This module creates artifact-level assertion registrations from
evidence-bearing surfaces. It does not parse row-level biology.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import sqlite3

from variant_database.persistence.repositories import stable_hash
from variant_database.registration.evidence_surface_classifier import classify_surface


@dataclass(frozen=True)
class AssertionRegistration:
    assertion_registration_id: str
    package_id: str
    artifact_id: str
    surface_role: str
    evidence_domain: str
    producer_family: str
    source_record_ref: str | None
    assertion_type: str
    participant_summary_json: str
    support_ref_json: str
    authority_context: str
    uncertainty_context: str
    registration_status: str
    payload_json: str


def assertion_id_for_surface(
    package_id: str,
    artifact_id: str,
    surface_role: str,
    evidence_domain: str,
) -> str:
    return stable_hash(
        [
            "assertion_registration",
            package_id,
            artifact_id,
            surface_role,
            evidence_domain,
        ]
    )


def build_artifact_level_assertion_registration(
    package_id: str,
    artifact_record: dict[str, object],
    producer_family: str,
    uncertainty_context: str = "source_asserted",
) -> AssertionRegistration | None:
    """Build one artifact-level assertion registration if surface is evidence-bearing."""
    relative_path = str(artifact_record["relative_path"])
    artifact_id = str(artifact_record["artifact_id"])

    surface = classify_surface(relative_path)

    if not surface.evidence_bearing:
        return None

    assertion_registration_id = assertion_id_for_surface(
        package_id=package_id,
        artifact_id=artifact_id,
        surface_role=surface.surface_role,
        evidence_domain=surface.evidence_domain,
    )

    support_ref = {
        "package_id": package_id,
        "artifact_id": artifact_id,
        "relative_path": relative_path,
        "source_record_ref": None,
    }

    payload = {
        "registration_level": "artifact",
        "relative_path": relative_path,
        "size_bytes": artifact_record["size_bytes"],
        "sha256": artifact_record["sha256"],
    }

    return AssertionRegistration(
        assertion_registration_id=assertion_registration_id,
        package_id=package_id,
        artifact_id=artifact_id,
        surface_role=surface.surface_role,
        evidence_domain=surface.evidence_domain,
        producer_family=producer_family,
        source_record_ref=None,
        assertion_type=surface.evidence_domain,
        participant_summary_json=json.dumps({}, sort_keys=True),
        support_ref_json=json.dumps(support_ref, sort_keys=True),
        authority_context="producer_emitted",
        uncertainty_context=uncertainty_context,
        registration_status="registered",
        payload_json=json.dumps(payload, sort_keys=True),
    )


def persist_assertion_registration(
    connection: sqlite3.Connection,
    registration: AssertionRegistration,
) -> str:
    """Persist one assertion registration."""
    connection.execute(
        """
        INSERT INTO assertion_registrations (
            assertion_registration_id,
            package_id,
            artifact_id,
            surface_role,
            evidence_domain,
            producer_family,
            source_record_ref,
            assertion_type,
            participant_summary_json,
            support_ref_json,
            authority_context,
            uncertainty_context,
            registration_status,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(assertion_registration_id) DO UPDATE SET
            package_id = excluded.package_id,
            artifact_id = excluded.artifact_id,
            surface_role = excluded.surface_role,
            evidence_domain = excluded.evidence_domain,
            producer_family = excluded.producer_family,
            source_record_ref = excluded.source_record_ref,
            assertion_type = excluded.assertion_type,
            participant_summary_json = excluded.participant_summary_json,
            support_ref_json = excluded.support_ref_json,
            authority_context = excluded.authority_context,
            uncertainty_context = excluded.uncertainty_context,
            registration_status = excluded.registration_status,
            payload_json = excluded.payload_json
        """,
        (
            registration.assertion_registration_id,
            registration.package_id,
            registration.artifact_id,
            registration.surface_role,
            registration.evidence_domain,
            registration.producer_family,
            registration.source_record_ref,
            registration.assertion_type,
            registration.participant_summary_json,
            registration.support_ref_json,
            registration.authority_context,
            registration.uncertainty_context,
            registration.registration_status,
            registration.payload_json,
        ),
    )
    connection.commit()
    return registration.assertion_registration_id


def register_artifact_level_assertions_for_package(
    connection: sqlite3.Connection,
    package_id: str,
    artifact_records: list[dict[str, object]],
    producer_family: str,
    uncertainty_context: str = "source_asserted",
) -> list[str]:
    """Register artifact-level assertions for evidence-bearing artifacts."""
    assertion_ids: list[str] = []

    for artifact_record in artifact_records:
        registration = build_artifact_level_assertion_registration(
            package_id=package_id,
            artifact_record=artifact_record,
            producer_family=producer_family,
            uncertainty_context=uncertainty_context,
        )

        if registration is None:
            continue

        assertion_ids.append(
            persist_assertion_registration(connection, registration)
        )

    return assertion_ids


def list_assertion_registrations(
    connection: sqlite3.Connection,
    package_id: str,
) -> list[dict[str, object]]:
    rows = connection.execute(
        """
        SELECT
            assertion_registration_id,
            package_id,
            artifact_id,
            surface_role,
            evidence_domain,
            producer_family,
            source_record_ref,
            assertion_type,
            participant_summary_json,
            support_ref_json,
            authority_context,
            uncertainty_context,
            registration_status,
            payload_json
        FROM assertion_registrations
        WHERE package_id = ?
        ORDER BY surface_role, artifact_id
        """,
        (package_id,),
    ).fetchall()

    return [dict(row) for row in rows]

"""Source identity attachment.

Source identities are producer-emitted or producer-derived participant
identities attached to assertion registrations.

This module preserves source identity only.
It does not perform namespace resolution.
It does not attach canonical identities.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
import sqlite3

from variant_database.persistence.repositories import stable_hash
from variant_database.registration.participant_extractor import ExtractedParticipant

@dataclass(frozen=True)
class SourceIdentity:
    source_identity_id: str
    assertion_registration_id: str
    identity_kind: str
    participant_role: str
    source_value: str
    source_namespace: str
    source_label: str | None
    extraction_method: str
    source_record_ref: str | None
    payload_json: str


def extract_vap_sample_id_from_package_path(package_path: str) -> str | None:
    """Extract a VAP sample identifier from a TEP package path."""
    match = re.search(r"vap_tep_([^/]+?)_run_\d{4}_\d{2}_\d{2}_\d{6}", package_path)
    if match:
        return match.group(1)

    return None


def source_identity_id_for_registration(
    assertion_registration_id: str,
    identity_kind: str,
    participant_role: str,
    source_value: str,
    source_namespace: str,
    source_record_ref: str | None,
) -> str:
    """Derive a deterministic source identity ID.

    Source record reference is part of identity because row-level participants
    must remain reconstructable and must not collapse across distinct source
    records within the same assertion registration.
    """
    return stable_hash(
        [
            "source_identity",
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_value,
            source_namespace,
            source_record_ref or "",
        ]
    )


def build_source_identity(
    assertion_registration_id: str,
    identity_kind: str,
    participant_role: str,
    source_value: str,
    source_namespace: str,
    source_label: str | None,
    extraction_method: str,
    source_record_ref: str | None = None,
    payload: dict[str, object] | None = None,
) -> SourceIdentity:
    """Build a deterministic source identity attachment."""
    source_identity_id = source_identity_id_for_registration(
        assertion_registration_id=assertion_registration_id,
        identity_kind=identity_kind,
        participant_role=participant_role,
        source_value=source_value,
        source_namespace=source_namespace,
        source_record_ref=source_record_ref,
    )

    return SourceIdentity(
        source_identity_id=source_identity_id,
        assertion_registration_id=assertion_registration_id,
        identity_kind=identity_kind,
        participant_role=participant_role,
        source_value=source_value,
        source_namespace=source_namespace,
        source_label=source_label,
        extraction_method=extraction_method,
        source_record_ref=source_record_ref,
        payload_json=json.dumps(payload or {}, sort_keys=True),
    )


def build_vap_sample_identity_for_registration(
    assertion_registration_id: str,
    package_path: str,
) -> SourceIdentity | None:
    """Build a VAP sample source identity from package path context."""
    sample_id = extract_vap_sample_id_from_package_path(package_path)

    if sample_id is None:
        return None

    return build_source_identity(
        assertion_registration_id=assertion_registration_id,
        identity_kind="sample",
        participant_role="sample",
        source_value=sample_id,
        source_namespace="vap_sample_id",
        source_label=sample_id,
        extraction_method="vap_package_path",
        payload={
            "package_path": package_path,
        },
    )


def persist_source_identity(
    connection: sqlite3.Connection,
    source_identity: SourceIdentity,
    commit: bool = True,
) -> str:
    """Persist one source identity attachment."""
    connection.execute(
        """
        INSERT INTO source_identities (
            source_identity_id,
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_value,
            source_namespace,
            source_label,
            extraction_method,
            source_record_ref,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_identity_id) DO UPDATE SET
            assertion_registration_id = excluded.assertion_registration_id,
            identity_kind = excluded.identity_kind,
            participant_role = excluded.participant_role,
            source_value = excluded.source_value,
            source_namespace = excluded.source_namespace,
            source_label = excluded.source_label,
            extraction_method = excluded.extraction_method,
            source_record_ref = excluded.source_record_ref,
            payload_json = excluded.payload_json
        """,
        (
            source_identity.source_identity_id,
            source_identity.assertion_registration_id,
            source_identity.identity_kind,
            source_identity.participant_role,
            source_identity.source_value,
            source_identity.source_namespace,
            source_identity.source_label,
            source_identity.extraction_method,
            source_identity.source_record_ref,
            source_identity.payload_json,
        ),
    )

    if commit:
        connection.commit()

    return source_identity.source_identity_id


def attach_vap_sample_identity_to_assertions(
    connection: sqlite3.Connection,
    package_path: str,
    assertion_registrations: list[dict[str, object]],
) -> list[str]:
    """Attach VAP sample identity to assertion registrations."""
    source_identity_ids: list[str] = []

    for registration in assertion_registrations:
        source_identity = build_vap_sample_identity_for_registration(
            assertion_registration_id=str(registration["assertion_registration_id"]),
            package_path=package_path,
        )

        if source_identity is None:
            continue

        source_identity_ids.append(
            persist_source_identity(connection, source_identity)
        )

    return source_identity_ids


def list_source_identities(
    connection: sqlite3.Connection,
    assertion_registration_id: str | None = None,
) -> list[dict[str, object]]:
    """List source identity attachments."""
    if assertion_registration_id is None:
        rows = connection.execute(
            """
            SELECT
                source_identity_id,
                assertion_registration_id,
                identity_kind,
                participant_role,
                source_value,
                source_namespace,
                source_label,
                extraction_method,
                source_record_ref,
                payload_json
            FROM source_identities
            ORDER BY assertion_registration_id, identity_kind, source_value
            """
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT
                source_identity_id,
                assertion_registration_id,
                identity_kind,
                participant_role,
                source_value,
                source_namespace,
                source_label,
                extraction_method,
                source_record_ref,
                payload_json
            FROM source_identities
            WHERE assertion_registration_id = ?
            ORDER BY identity_kind, source_value
            """,
            (assertion_registration_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def build_source_identity_from_participant(
    assertion_registration_id: str,
    participant: ExtractedParticipant,
) -> SourceIdentity:
    """Build a SourceIdentity from an extracted participant."""
    return build_source_identity(
        assertion_registration_id=assertion_registration_id,
        identity_kind=participant.participant_kind,
        participant_role=participant.participant_role,
        source_value=participant.source_value,
        source_namespace=participant.source_namespace,
        source_label=participant.source_label,
        extraction_method=participant.extraction_method,
        source_record_ref=participant.source_record_ref,
        payload={
            "source": "extracted_participant",
        },
    )


def attach_participants_to_assertion(
    connection: sqlite3.Connection,
    assertion_registration_id: str,
    participants: list[ExtractedParticipant],
    commit: bool = True,
) -> list[str]:
    """Persist extracted participants as source identities."""
    source_identity_ids: list[str] = []

    for participant in participants:
        source_identity = build_source_identity_from_participant(
            assertion_registration_id=assertion_registration_id,
            participant=participant,
        )
        source_identity_ids.append(
            persist_source_identity(
                connection,
                source_identity,
                commit=commit,
            )
        )

    return source_identity_ids
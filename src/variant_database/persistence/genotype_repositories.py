"""Persistence helpers for VDB genotype discovery surfaces."""

from __future__ import annotations

import sqlite3

from variant_database.persistence.repositories import stable_hash


def _required_int(value: object, field_name: str) -> int:
    """Return a validated integer value for SQLite persistence."""
    if isinstance(value, bool):
        raise TypeError(f"{field_name} must not be boolean")

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f"{field_name} is not an integer string: {value!r}"
            ) from exc

    raise TypeError(
        f"{field_name} must be an integer or integer string; "
        f"received {type(value).__name__}"
    )

def genotype_classification_id_for_package(package_id: str) -> str:
    return stable_hash(["source_genotype_package_classification", package_id])


def genotype_artifact_index_id_for_role(
    package_id: str,
    artifact_role: str,
    artifact_path: str,
) -> str:
    return stable_hash(
        [
            "source_genotype_artifact_index",
            package_id,
            artifact_role,
            artifact_path,
        ]
    )


def genotype_context_index_id_for_kind(
    package_id: str,
    context_kind: str,
    context_artifact_path: str,
) -> str:
    return stable_hash(
        [
            "source_genotype_context_index",
            package_id,
            context_kind,
            context_artifact_path,
        ]
    )


def persist_genotype_package_classification(
    connection: sqlite3.Connection,
    classification: dict[str, object],
    commit: bool = True,
) -> str:
    """Persist one package-level genotype capability classification."""
    connection.execute(
        """
        INSERT INTO source_genotype_package_classifications (
            genotype_classification_id,
            package_id,
            producer_family,
            producer_genotype_applicability_state,
            genotype_capability_state,
            genotype_maturity_state,
            genotype_artifact_set_status,
            governance_artifact_set_status,
            execution_provenance_status,
            trusted_modern_ingestion_ready,
            classification_status,
            classification_reason,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(package_id) DO UPDATE SET
            producer_family = excluded.producer_family,
            producer_genotype_applicability_state = excluded.producer_genotype_applicability_state,
            genotype_capability_state = excluded.genotype_capability_state,
            genotype_maturity_state = excluded.genotype_maturity_state,
            genotype_artifact_set_status = excluded.genotype_artifact_set_status,
            governance_artifact_set_status = excluded.governance_artifact_set_status,
            execution_provenance_status = excluded.execution_provenance_status,
            trusted_modern_ingestion_ready = excluded.trusted_modern_ingestion_ready,
            classification_status = excluded.classification_status,
            classification_reason = excluded.classification_reason,
            payload_json = excluded.payload_json
        """,
        (
            classification["genotype_classification_id"],
            classification["package_id"],
            classification["producer_family"],
            classification["producer_genotype_applicability_state"],
            classification["genotype_capability_state"],
            classification["genotype_maturity_state"],
            classification["genotype_artifact_set_status"],
            classification["governance_artifact_set_status"],
            classification["execution_provenance_status"],
            _required_int(
                classification["trusted_modern_ingestion_ready"],
                "trusted_modern_ingestion_ready",
            ),
            classification["classification_status"],
            classification["classification_reason"],
            classification["payload_json"],
        ),
    )

    if commit:
        connection.commit()

    return str(classification["genotype_classification_id"])


def persist_genotype_artifact_index_records(
    connection: sqlite3.Connection,
    records: list[dict[str, object]],
    commit: bool = True,
) -> list[str]:
    """Persist genotype artifact index records."""
    ids: list[str] = []

    for record in records:
        connection.execute(
            """
            INSERT INTO source_genotype_artifact_index (
                genotype_artifact_index_id,
                package_id,
                artifact_id,
                artifact_role,
                artifact_path,
                artifact_sha256,
                size_bytes,
                artifact_present,
                required_for_trusted_modern_ingestion,
                schema_version,
                parse_status,
                payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(package_id, artifact_role) DO UPDATE SET
                artifact_id = excluded.artifact_id,
                artifact_path = excluded.artifact_path,
                artifact_sha256 = excluded.artifact_sha256,
                size_bytes = excluded.size_bytes,
                artifact_present = excluded.artifact_present,
                required_for_trusted_modern_ingestion = excluded.required_for_trusted_modern_ingestion,
                schema_version = excluded.schema_version,
                parse_status = excluded.parse_status,
                payload_json = excluded.payload_json
            """,
            (
                record["genotype_artifact_index_id"],
                record["package_id"],
                record["artifact_id"],
                record["artifact_role"],
                record["artifact_path"],
                record["artifact_sha256"],
                _required_int(record["size_bytes"], "size_bytes"),
                _required_int(record["artifact_present"], "artifact_present"),
                _required_int(
                    record["required_for_trusted_modern_ingestion"],
                    "required_for_trusted_modern_ingestion",
                ),
                record["schema_version"],
                record["parse_status"],
                record["payload_json"],
            ),
        )
        ids.append(str(record["genotype_artifact_index_id"]))

    if commit:
        connection.commit()

    return ids


def persist_genotype_context_index_records(
    connection: sqlite3.Connection,
    records: list[dict[str, object]],
    commit: bool = True,
) -> list[str]:
    """Persist genotype context index records."""
    ids: list[str] = []

    for record in records:
        connection.execute(
            """
            INSERT INTO source_genotype_context_index (
                genotype_context_index_id,
                package_id,
                artifact_id,
                context_kind,
                context_artifact_path,
                context_artifact_sha256,
                schema_version,
                parse_status,
                registered_as_context,
                registered_as_biological_evidence,
                contract_status,
                provenance_completeness,
                projection_status,
                genotype_observation_row_count,
                source_record_count,
                direct_relationship_count,
                complex_relationship_count,
                unresolved_relationship_count,
                projection_error_count,
                projection_warning_count,
                reference_build,
                sample_id,
                run_id,
                payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(package_id, context_kind) DO UPDATE SET
                artifact_id = excluded.artifact_id,
                context_artifact_path = excluded.context_artifact_path,
                context_artifact_sha256 = excluded.context_artifact_sha256,
                schema_version = excluded.schema_version,
                parse_status = excluded.parse_status,
                registered_as_context = excluded.registered_as_context,
                registered_as_biological_evidence = excluded.registered_as_biological_evidence,
                contract_status = excluded.contract_status,
                provenance_completeness = excluded.provenance_completeness,
                projection_status = excluded.projection_status,
                genotype_observation_row_count = excluded.genotype_observation_row_count,
                source_record_count = excluded.source_record_count,
                direct_relationship_count = excluded.direct_relationship_count,
                complex_relationship_count = excluded.complex_relationship_count,
                unresolved_relationship_count = excluded.unresolved_relationship_count,
                projection_error_count = excluded.projection_error_count,
                projection_warning_count = excluded.projection_warning_count,
                reference_build = excluded.reference_build,
                sample_id = excluded.sample_id,
                run_id = excluded.run_id,
                payload_json = excluded.payload_json
            """,
            (
                record["genotype_context_index_id"],
                record["package_id"],
                record["artifact_id"],
                record["context_kind"],
                record["context_artifact_path"],
                record["context_artifact_sha256"],
                record["schema_version"],
                record["parse_status"],
                _required_int(
                    record["registered_as_context"],
                    "registered_as_context",
                ),
                _required_int(
                    record["registered_as_biological_evidence"],
                    "registered_as_biological_evidence",
                ),
                record["contract_status"],
                record["provenance_completeness"],
                record["projection_status"],
                record["genotype_observation_row_count"],
                record["source_record_count"],
                record["direct_relationship_count"],
                record["complex_relationship_count"],
                record["unresolved_relationship_count"],
                record["projection_error_count"],
                record["projection_warning_count"],
                record["reference_build"],
                record["sample_id"],
                record["run_id"],
                record["payload_json"],
            ),
        )
        ids.append(str(record["genotype_context_index_id"]))

    if commit:
        connection.commit()

    return ids

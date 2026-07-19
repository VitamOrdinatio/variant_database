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


def genotype_preservation_scope_id_for_request(
    package_id: str,
    scope_label: str,
    source_artifact_sha256: str,
    row_selection_policy: str,
    requested_row_limit: int | None,
) -> str:
    """Return the stable identity for one declared preservation scope."""
    return stable_hash(
        [
            "source_genotype_preservation_scope",
            package_id,
            scope_label,
            source_artifact_sha256,
            row_selection_policy,
            "full" if requested_row_limit is None else str(requested_row_limit),
        ]
    )


def source_genotype_observation_persistence_id(
    package_id: str,
    preservation_scope_id: str,
    genotype_observation_id: str,
) -> str:
    """Return a VDB persistence identity without replacing producer identity."""
    return stable_hash(
        [
            "source_genotype_observation",
            package_id,
            preservation_scope_id,
            genotype_observation_id,
        ]
    )


def persist_genotype_preservation_scope(
    connection: sqlite3.Connection,
    record: dict[str, object],
    commit: bool = True,
) -> str:
    """Persist one explicit genotype preservation scope."""
    connection.execute(
        """
        INSERT INTO source_genotype_preservation_scopes (
            preservation_scope_id,
            package_id,
            source_tep_id,
            source_artifact_id,
            source_artifact_path,
            source_artifact_sha256,
            preservation_scope_kind,
            scope_label,
            row_selection_policy,
            requested_row_limit,
            selected_row_count,
            source_declared_row_count,
            first_selected_source_row,
            last_selected_source_row,
            source_column_order_json,
            preservation_status,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["preservation_scope_id"],
            record["package_id"],
            record["source_tep_id"],
            record["source_artifact_id"],
            record["source_artifact_path"],
            record["source_artifact_sha256"],
            record["preservation_scope_kind"],
            record["scope_label"],
            record["row_selection_policy"],
            record["requested_row_limit"],
            _required_int(record["selected_row_count"], "selected_row_count"),
            record["source_declared_row_count"],
            record["first_selected_source_row"],
            record["last_selected_source_row"],
            record["source_column_order_json"],
            record["preservation_status"],
            record["payload_json"],
        ),
    )
    if commit:
        connection.commit()
    return str(record["preservation_scope_id"])


def persist_source_genotype_observation_batch(
    connection: sqlite3.Connection,
    records: list[dict[str, object]],
    commit: bool = True,
) -> list[str]:
    """Persist a bounded batch of immutable producer genotype rows."""
    if not records:
        return []

    columns = (
        "source_genotype_observation_persistence_id",
        "package_id",
        "preservation_scope_id",
        "source_row_number",
        "genotype_observation_id",
        "genotype_observation_id_version",
        "schema_version",
        "entity_type",
        "evidence_class",
        "sample_id",
        "sample_alias",
        "sra_accession",
        "run_id",
        "vcf_sample_column_name",
        "sample_selection_policy",
        "sample_identity_mapping_status",
        "source_pipeline",
        "assay_type",
        "source_vcf_path",
        "source_vcf_sha256",
        "source_vcf_header_hash",
        "source_record_ordinal",
        "source_line_number",
        "source_record_hash",
        "reference_build",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_alleles_raw",
        "alternate_allele_count",
        "called_allele_indices",
        "variant_relationship_status",
        "relationship_reason",
        "relationship_resolution_target",
        "variant_id",
        "variant_observation_id",
        "format_raw",
        "sample_format_raw",
        "gt_raw",
        "ad_raw",
        "dp_raw",
        "gq_raw",
        "pl_raw",
        "ft_raw",
        "record_parse_status",
        "record_preservation_status",
        "raw_source_row_hash",
        "raw_source_values_json",
    )
    placeholders = ", ".join("?" for _ in columns)
    connection.executemany(
        f"""
        INSERT INTO source_genotype_observations (
            {", ".join(columns)}
        )
        VALUES ({placeholders})
        """,
        [tuple(record.get(column) for column in columns) for record in records],
    )
    if commit:
        connection.commit()
    return [
        str(record["source_genotype_observation_persistence_id"])
        for record in records
    ]


def update_genotype_preservation_scope_completion(
    connection: sqlite3.Connection,
    *,
    preservation_scope_id: str,
    selected_row_count: int,
    first_selected_source_row: int | None,
    last_selected_source_row: int | None,
    preservation_status: str,
    commit: bool = True,
) -> None:
    """Finalize one scope after all selected source rows persist."""
    connection.execute(
        """
        UPDATE source_genotype_preservation_scopes
        SET selected_row_count = ?,
            first_selected_source_row = ?,
            last_selected_source_row = ?,
            preservation_status = ?
        WHERE preservation_scope_id = ?
        """,
        (
            selected_row_count,
            first_selected_source_row,
            last_selected_source_row,
            preservation_status,
            preservation_scope_id,
        ),
    )
    if commit:
        connection.commit()

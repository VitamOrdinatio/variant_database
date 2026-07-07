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


def persist_package_metadata_record(
    connection: sqlite3.Connection,
    metadata_record: dict[str, object],
    commit: bool = True,
) -> str:
    """Persist one package metadata record and return its deterministic ID."""
    connection.execute(
        """
        INSERT INTO package_metadata (
            package_metadata_id,
            package_id,
            metadata_artifact_id,
            metadata_role,
            metadata_artifact_path,
            metadata_artifact_sha256,
            metadata_format,
            run_id,
            run_id_derivation_method,
            sample_id,
            sample_alias,
            sra_accession,
            assay_type,
            project_name,
            pipeline_name,
            pipeline_version,
            execution_profile_name,
            hardware_class,
            reference_genome_build,
            reference_fasta_path,
            reference_fasta_index_path,
            reference_sequence_dictionary_path,
            annotation_engine,
            annotation_assembly,
            annotation_cache_dir,
            deterministic_mode,
            record_tool_versions,
            metadata_parse_status,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(package_metadata_id) DO UPDATE SET
            package_id = excluded.package_id,
            metadata_artifact_id = excluded.metadata_artifact_id,
            metadata_role = excluded.metadata_role,
            metadata_artifact_path = excluded.metadata_artifact_path,
            metadata_artifact_sha256 = excluded.metadata_artifact_sha256,
            metadata_format = excluded.metadata_format,
            run_id = excluded.run_id,
            run_id_derivation_method = excluded.run_id_derivation_method,
            sample_id = excluded.sample_id,
            sample_alias = excluded.sample_alias,
            sra_accession = excluded.sra_accession,
            assay_type = excluded.assay_type,
            project_name = excluded.project_name,
            pipeline_name = excluded.pipeline_name,
            pipeline_version = excluded.pipeline_version,
            execution_profile_name = excluded.execution_profile_name,
            hardware_class = excluded.hardware_class,
            reference_genome_build = excluded.reference_genome_build,
            reference_fasta_path = excluded.reference_fasta_path,
            reference_fasta_index_path = excluded.reference_fasta_index_path,
            reference_sequence_dictionary_path = excluded.reference_sequence_dictionary_path,
            annotation_engine = excluded.annotation_engine,
            annotation_assembly = excluded.annotation_assembly,
            annotation_cache_dir = excluded.annotation_cache_dir,
            deterministic_mode = excluded.deterministic_mode,
            record_tool_versions = excluded.record_tool_versions,
            metadata_parse_status = excluded.metadata_parse_status,
            payload_json = excluded.payload_json
        """,
        (
            metadata_record["package_metadata_id"],
            metadata_record["package_id"],
            metadata_record["metadata_artifact_id"],
            metadata_record["metadata_role"],
            metadata_record["metadata_artifact_path"],
            metadata_record["metadata_artifact_sha256"],
            metadata_record["metadata_format"],
            metadata_record["run_id"],
            metadata_record["run_id_derivation_method"],
            metadata_record["sample_id"],
            metadata_record["sample_alias"],
            metadata_record["sra_accession"],
            metadata_record["assay_type"],
            metadata_record["project_name"],
            metadata_record["pipeline_name"],
            metadata_record["pipeline_version"],
            metadata_record["execution_profile_name"],
            metadata_record["hardware_class"],
            metadata_record["reference_genome_build"],
            metadata_record["reference_fasta_path"],
            metadata_record["reference_fasta_index_path"],
            metadata_record["reference_sequence_dictionary_path"],
            metadata_record["annotation_engine"],
            metadata_record["annotation_assembly"],
            metadata_record["annotation_cache_dir"],
            metadata_record["deterministic_mode"],
            metadata_record["record_tool_versions"],
            metadata_record["metadata_parse_status"],
            metadata_record["payload_json"],
        ),
    )

    if commit:
        connection.commit()

    return str(metadata_record["package_metadata_id"])


def list_package_metadata_records(
    connection: sqlite3.Connection,
    package_id: str | None = None,
) -> list[dict[str, object]]:
    """List registered package metadata records."""
    if package_id is None:
        rows = connection.execute(
            """
            SELECT
                package_metadata_id,
                package_id,
                metadata_artifact_id,
                metadata_role,
                metadata_artifact_path,
                metadata_artifact_sha256,
                metadata_format,
                run_id,
                run_id_derivation_method,
                sample_id,
                sample_alias,
                sra_accession,
                assay_type,
                project_name,
                pipeline_name,
                pipeline_version,
                execution_profile_name,
                hardware_class,
                reference_genome_build,
                reference_fasta_path,
                reference_fasta_index_path,
                reference_sequence_dictionary_path,
                annotation_engine,
                annotation_assembly,
                annotation_cache_dir,
                deterministic_mode,
                record_tool_versions,
                metadata_parse_status,
                payload_json
            FROM package_metadata
            ORDER BY package_id, metadata_artifact_path
            """
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT
                package_metadata_id,
                package_id,
                metadata_artifact_id,
                metadata_role,
                metadata_artifact_path,
                metadata_artifact_sha256,
                metadata_format,
                run_id,
                run_id_derivation_method,
                sample_id,
                sample_alias,
                sra_accession,
                assay_type,
                project_name,
                pipeline_name,
                pipeline_version,
                execution_profile_name,
                hardware_class,
                reference_genome_build,
                reference_fasta_path,
                reference_fasta_index_path,
                reference_sequence_dictionary_path,
                annotation_engine,
                annotation_assembly,
                annotation_cache_dir,
                deterministic_mode,
                record_tool_versions,
                metadata_parse_status,
                payload_json
            FROM package_metadata
            WHERE package_id = ?
            ORDER BY metadata_artifact_path
            """,
            (package_id,),
        ).fetchall()

    return [dict(row) for row in rows]




def persist_source_coordinate_declaration(
    connection: sqlite3.Connection,
    coordinate_declaration: object,
    commit: bool = True,
) -> str:
    """Persist one source coordinate declaration and return its ID."""
    record = (
        coordinate_declaration
        if isinstance(coordinate_declaration, dict)
        else coordinate_declaration.__dict__
    )

    connection.execute(
        """
        INSERT INTO source_coordinate_declarations (
            coordinate_declaration_id,
            assertion_registration_id,
            source_identity_id,
            source_record_ref,
            source_artifact_path,
            variant_source_namespace,
            variant_source_value,
            variant_source_label,
            reference_genome_build,
            reference_context_source,
            chromosome,
            position,
            start,
            end,
            reference_allele,
            alternate_allele,
            variant_type,
            variant_class,
            coordinate_system,
            coordinate_system_status,
            normalization_status,
            normalization_status_source,
            sample_id,
            run_id,
            producer_pipeline,
            extraction_method,
            payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(coordinate_declaration_id) DO UPDATE SET
            assertion_registration_id = excluded.assertion_registration_id,
            source_identity_id = excluded.source_identity_id,
            source_record_ref = excluded.source_record_ref,
            source_artifact_path = excluded.source_artifact_path,
            variant_source_namespace = excluded.variant_source_namespace,
            variant_source_value = excluded.variant_source_value,
            variant_source_label = excluded.variant_source_label,
            reference_genome_build = excluded.reference_genome_build,
            reference_context_source = excluded.reference_context_source,
            chromosome = excluded.chromosome,
            position = excluded.position,
            start = excluded.start,
            end = excluded.end,
            reference_allele = excluded.reference_allele,
            alternate_allele = excluded.alternate_allele,
            variant_type = excluded.variant_type,
            variant_class = excluded.variant_class,
            coordinate_system = excluded.coordinate_system,
            coordinate_system_status = excluded.coordinate_system_status,
            normalization_status = excluded.normalization_status,
            normalization_status_source = excluded.normalization_status_source,
            sample_id = excluded.sample_id,
            run_id = excluded.run_id,
            producer_pipeline = excluded.producer_pipeline,
            extraction_method = excluded.extraction_method,
            payload_json = excluded.payload_json
        """,
        (
            record["coordinate_declaration_id"],
            record["assertion_registration_id"],
            record["source_identity_id"],
            record["source_record_ref"],
            record["source_artifact_path"],
            record["variant_source_namespace"],
            record["variant_source_value"],
            record["variant_source_label"],
            record["reference_genome_build"],
            record["reference_context_source"],
            record["chromosome"],
            record["position"],
            record["start"],
            record["end"],
            record["reference_allele"],
            record["alternate_allele"],
            record["variant_type"],
            record["variant_class"],
            record["coordinate_system"],
            record["coordinate_system_status"],
            record["normalization_status"],
            record["normalization_status_source"],
            record["sample_id"],
            record["run_id"],
            record["producer_pipeline"],
            record["extraction_method"],
            record["payload_json"],
        ),
    )

    if commit:
        connection.commit()

    return str(record["coordinate_declaration_id"])


def list_source_coordinate_declarations(
    connection: sqlite3.Connection,
    assertion_registration_id: str | None = None,
) -> list[dict[str, object]]:
    """List registered source coordinate declarations."""
    columns = """
        coordinate_declaration_id,
        assertion_registration_id,
        source_identity_id,
        source_record_ref,
        source_artifact_path,
        variant_source_namespace,
        variant_source_value,
        variant_source_label,
        reference_genome_build,
        reference_context_source,
        chromosome,
        position,
        start,
        end,
        reference_allele,
        alternate_allele,
        variant_type,
        variant_class,
        coordinate_system,
        coordinate_system_status,
        normalization_status,
        normalization_status_source,
        sample_id,
        run_id,
        producer_pipeline,
        extraction_method,
        payload_json
    """

    if assertion_registration_id is None:
        rows = connection.execute(
            f"""
            SELECT {columns}
            FROM source_coordinate_declarations
            ORDER BY assertion_registration_id, source_record_ref, variant_source_value
            """
        ).fetchall()
    else:
        rows = connection.execute(
            f"""
            SELECT {columns}
            FROM source_coordinate_declarations
            WHERE assertion_registration_id = ?
            ORDER BY source_record_ref, variant_source_value
            """,
            (assertion_registration_id,),
        ).fetchall()

    return [dict(row) for row in rows]

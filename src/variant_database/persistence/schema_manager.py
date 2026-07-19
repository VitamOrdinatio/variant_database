"""Schema creation utilities for VDB persistence."""

from __future__ import annotations

import sqlite3


SCHEMA_VERSION = "0.1.3"


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

        CREATE TABLE IF NOT EXISTS package_metadata (
            package_metadata_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            metadata_artifact_id TEXT NOT NULL,
            metadata_role TEXT NOT NULL,
            metadata_artifact_path TEXT NOT NULL,
            metadata_artifact_sha256 TEXT NOT NULL,
            metadata_format TEXT NOT NULL,
            run_id TEXT,
            run_id_derivation_method TEXT NOT NULL,
            sample_id TEXT,
            sample_alias TEXT,
            sra_accession TEXT,
            assay_type TEXT,
            project_name TEXT,
            pipeline_name TEXT,
            pipeline_version TEXT,
            execution_profile_name TEXT,
            hardware_class TEXT,
            reference_genome_build TEXT,
            reference_fasta_path TEXT,
            reference_fasta_index_path TEXT,
            reference_sequence_dictionary_path TEXT,
            annotation_engine TEXT,
            annotation_assembly TEXT,
            annotation_cache_dir TEXT,
            deterministic_mode INTEGER,
            record_tool_versions INTEGER,
            metadata_parse_status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(metadata_artifact_id) REFERENCES artifacts(artifact_id)
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

        CREATE TABLE IF NOT EXISTS source_coordinate_declarations (
            coordinate_declaration_id TEXT PRIMARY KEY,
            assertion_registration_id TEXT NOT NULL,
            source_identity_id TEXT NOT NULL,
            source_record_ref TEXT,
            source_artifact_path TEXT NOT NULL,
            variant_source_namespace TEXT NOT NULL,
            variant_source_value TEXT NOT NULL,
            variant_source_label TEXT,
            reference_genome_build TEXT,
            reference_context_source TEXT,
            chromosome TEXT NOT NULL,
            position TEXT NOT NULL,
            start TEXT,
            end TEXT,
            reference_allele TEXT NOT NULL,
            alternate_allele TEXT NOT NULL,
            variant_type TEXT,
            variant_class TEXT,
            coordinate_system TEXT NOT NULL,
            coordinate_system_status TEXT NOT NULL,
            normalization_status TEXT NOT NULL,
            normalization_status_source TEXT NOT NULL,
            sample_id TEXT,
            run_id TEXT,
            producer_pipeline TEXT,
            extraction_method TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(assertion_registration_id)
                REFERENCES assertion_registrations(assertion_registration_id),
            FOREIGN KEY(source_identity_id)
                REFERENCES source_identities(source_identity_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_coordinate_declarations_assertion
            ON source_coordinate_declarations(assertion_registration_id);

        CREATE INDEX IF NOT EXISTS idx_source_coordinate_declarations_variant
            ON source_coordinate_declarations(variant_source_namespace, variant_source_value);

        CREATE INDEX IF NOT EXISTS idx_source_coordinate_declarations_reference
            ON source_coordinate_declarations(reference_genome_build, chromosome, position);


        CREATE TABLE IF NOT EXISTS source_feature_declarations (
            feature_declaration_id TEXT PRIMARY KEY,
            assertion_registration_id TEXT NOT NULL,
            coordinate_declaration_id TEXT,
            source_identity_id TEXT,
            source_record_ref TEXT,
            source_artifact_path TEXT NOT NULL,
            variant_source_namespace TEXT,
            variant_source_value TEXT,
            feature_kind TEXT NOT NULL,
            feature_namespace TEXT NOT NULL,
            feature_value TEXT NOT NULL,
            feature_label TEXT,
            relationship_type TEXT NOT NULL,
            relationship_status TEXT NOT NULL,
            gene_id TEXT,
            gene_symbol TEXT,
            gene_mapping_status TEXT,
            transcript_id TEXT,
            consequence TEXT,
            impact TEXT,
            impact_class TEXT,
            functional_impact TEXT,
            variant_context TEXT,
            is_regulatory_candidate TEXT,
            is_splice_region_candidate TEXT,
            annotation_source TEXT,
            annotation_version TEXT,
            annotation_assembly TEXT,
            reference_genome_build TEXT,
            sample_id TEXT,
            run_id TEXT,
            producer_pipeline TEXT,
            extraction_method TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(assertion_registration_id)
                REFERENCES assertion_registrations(assertion_registration_id),
            FOREIGN KEY(coordinate_declaration_id)
                REFERENCES source_coordinate_declarations(coordinate_declaration_id),
            FOREIGN KEY(source_identity_id)
                REFERENCES source_identities(source_identity_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_feature_declarations_assertion
            ON source_feature_declarations(assertion_registration_id);

        CREATE INDEX IF NOT EXISTS idx_source_feature_declarations_coordinate
            ON source_feature_declarations(coordinate_declaration_id);

        CREATE INDEX IF NOT EXISTS idx_source_feature_declarations_feature
            ON source_feature_declarations(feature_kind, feature_namespace, feature_value);

        CREATE INDEX IF NOT EXISTS idx_source_feature_declarations_variant
            ON source_feature_declarations(variant_source_namespace, variant_source_value);

        CREATE TABLE IF NOT EXISTS source_genotype_package_classifications (
            genotype_classification_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL UNIQUE,
            producer_family TEXT NOT NULL,
            producer_genotype_applicability_state TEXT NOT NULL,
            genotype_capability_state TEXT NOT NULL,
            genotype_maturity_state TEXT NOT NULL,
            genotype_artifact_set_status TEXT NOT NULL,
            governance_artifact_set_status TEXT NOT NULL,
            execution_provenance_status TEXT NOT NULL,
            trusted_modern_ingestion_ready INTEGER NOT NULL,
            classification_status TEXT NOT NULL,
            classification_reason TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_genotype_package_classifications_state
            ON source_genotype_package_classifications(genotype_capability_state, genotype_maturity_state);

        CREATE TABLE IF NOT EXISTS source_genotype_artifact_index (
            genotype_artifact_index_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            artifact_id TEXT,
            artifact_role TEXT NOT NULL,
            artifact_path TEXT NOT NULL,
            artifact_sha256 TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            artifact_present INTEGER NOT NULL,
            required_for_trusted_modern_ingestion INTEGER NOT NULL,
            schema_version TEXT,
            parse_status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            UNIQUE(package_id, artifact_role),
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_genotype_artifact_index_package
            ON source_genotype_artifact_index(package_id);

        CREATE INDEX IF NOT EXISTS idx_source_genotype_artifact_index_role
            ON source_genotype_artifact_index(artifact_role, parse_status);

        CREATE TABLE IF NOT EXISTS source_genotype_context_index (
            genotype_context_index_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            artifact_id TEXT,
            context_kind TEXT NOT NULL,
            context_artifact_path TEXT NOT NULL,
            context_artifact_sha256 TEXT NOT NULL,
            schema_version TEXT,
            parse_status TEXT NOT NULL,
            registered_as_context INTEGER NOT NULL,
            registered_as_biological_evidence INTEGER NOT NULL,
            contract_status TEXT,
            provenance_completeness TEXT,
            projection_status TEXT,
            genotype_observation_row_count INTEGER,
            source_record_count INTEGER,
            direct_relationship_count INTEGER,
            complex_relationship_count INTEGER,
            unresolved_relationship_count INTEGER,
            projection_error_count INTEGER,
            projection_warning_count INTEGER,
            reference_build TEXT,
            sample_id TEXT,
            run_id TEXT,
            payload_json TEXT NOT NULL,
            UNIQUE(package_id, context_kind),
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_genotype_context_index_package
            ON source_genotype_context_index(package_id);

        CREATE INDEX IF NOT EXISTS idx_source_genotype_context_index_kind
            ON source_genotype_context_index(context_kind, parse_status);
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

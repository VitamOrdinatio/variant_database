"""Schema creation utilities for VDB persistence."""

from __future__ import annotations

import sqlite3


SCHEMA_VERSION = "0.1.4"


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


        CREATE TABLE IF NOT EXISTS source_genotype_preservation_scopes (
            preservation_scope_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            source_tep_id TEXT NOT NULL,
            source_artifact_id TEXT NOT NULL,
            source_artifact_path TEXT NOT NULL,
            source_artifact_sha256 TEXT NOT NULL,
            preservation_scope_kind TEXT NOT NULL,
            scope_label TEXT NOT NULL,
            row_selection_policy TEXT NOT NULL,
            requested_row_limit INTEGER,
            selected_row_count INTEGER NOT NULL,
            source_declared_row_count INTEGER,
            first_selected_source_row INTEGER,
            last_selected_source_row INTEGER,
            source_column_order_json TEXT NOT NULL,
            preservation_status TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            UNIQUE(package_id, scope_label),
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(source_artifact_id) REFERENCES artifacts(artifact_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_genotype_preservation_scopes_package
            ON source_genotype_preservation_scopes(package_id, preservation_status);

        CREATE TABLE IF NOT EXISTS source_genotype_observations (
            source_genotype_observation_persistence_id TEXT PRIMARY KEY,
            package_id TEXT NOT NULL,
            preservation_scope_id TEXT NOT NULL,
            source_row_number INTEGER NOT NULL,
            genotype_observation_id TEXT NOT NULL,
            genotype_observation_id_version TEXT,
            schema_version TEXT,
            entity_type TEXT,
            evidence_class TEXT,
            sample_id TEXT,
            sample_alias TEXT,
            sra_accession TEXT,
            run_id TEXT,
            vcf_sample_column_name TEXT,
            sample_selection_policy TEXT,
            sample_identity_mapping_status TEXT,
            source_pipeline TEXT,
            assay_type TEXT,
            source_vcf_path TEXT,
            source_vcf_sha256 TEXT,
            source_vcf_header_hash TEXT,
            source_record_ordinal TEXT,
            source_line_number TEXT,
            source_record_hash TEXT,
            reference_build TEXT,
            chromosome TEXT,
            position TEXT,
            reference_allele TEXT,
            alternate_alleles_raw TEXT,
            alternate_allele_count TEXT,
            called_allele_indices TEXT,
            variant_relationship_status TEXT,
            relationship_reason TEXT,
            relationship_resolution_target TEXT,
            variant_id TEXT,
            variant_observation_id TEXT,
            format_raw TEXT,
            sample_format_raw TEXT,
            gt_raw TEXT,
            ad_raw TEXT,
            dp_raw TEXT,
            gq_raw TEXT,
            pl_raw TEXT,
            ft_raw TEXT,
            record_parse_status TEXT,
            record_preservation_status TEXT,
            raw_source_row_hash TEXT NOT NULL,
            raw_source_values_json TEXT NOT NULL,
            UNIQUE(preservation_scope_id, source_row_number),
            UNIQUE(preservation_scope_id, genotype_observation_id),
            FOREIGN KEY(package_id) REFERENCES tep_packages(package_id),
            FOREIGN KEY(preservation_scope_id)
                REFERENCES source_genotype_preservation_scopes(preservation_scope_id)
        );

        CREATE INDEX IF NOT EXISTS idx_source_genotype_observations_scope_row
            ON source_genotype_observations(preservation_scope_id, source_row_number);

        CREATE INDEX IF NOT EXISTS idx_source_genotype_observations_identity
            ON source_genotype_observations(package_id, genotype_observation_id);

        CREATE INDEX IF NOT EXISTS idx_source_genotype_observations_source_record
            ON source_genotype_observations(package_id, source_record_hash);
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

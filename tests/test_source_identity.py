from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.package_scanner import scan_package
from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.repositories import (
    list_artifact_records,
    persist_package_inventory,
)
from variant_database.persistence.schema_manager import initialize_schema
from variant_database.registration.assertion_registration import (
    list_assertion_registrations,
    register_artifact_level_assertions_for_package,
)
from variant_database.registration.source_identity import (
    attach_vap_sample_identity_to_assertions,
    build_vap_sample_identity_for_registration,
    extract_vap_sample_id_from_package_path,
    list_source_identities,
)

from variant_database.registration.participant_extractor import ExtractedParticipant


def test_extract_vap_sample_id_from_package_path() -> None:
    path = (
        "/tmp/vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
    )

    assert extract_vap_sample_id_from_package_path(path) == "HG002"


def test_extract_vap_sample_id_returns_none_for_non_vap_path() -> None:
    assert extract_vap_sample_id_from_package_path("/tmp/gsc_tep.json") is None


def test_build_vap_sample_identity_for_registration() -> None:
    path = (
        "/tmp/vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
    )

    identity = build_vap_sample_identity_for_registration(
        assertion_registration_id="assertion-1",
        package_path=path,
    )

    assert identity is not None
    assert identity.identity_kind == "sample"
    assert identity.participant_role == "sample"
    assert identity.source_value == "HG002"
    assert identity.source_namespace == "vap_sample_id"
    assert identity.extraction_method == "vap_package_path"


def test_attach_vap_sample_identity_to_assertions(tmp_path: Path) -> None:
    package = (
        tmp_path
        / "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
    )
    (package / "entities" / "routing").mkdir(parents=True)
    (
        package / "entities" / "routing" / "coding_candidates.tsv"
    ).write_text("a\tb\n1\t2\n", encoding="utf-8")

    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifacts = list_artifact_records(connection, package_id)

    register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifacts,
        producer_family="VAP",
    )

    registrations = list_assertion_registrations(connection, package_id)

    source_identity_ids = attach_vap_sample_identity_to_assertions(
        connection=connection,
        package_path=inventory.package_path,
        assertion_registrations=registrations,
    )

    source_identities = list_source_identities(connection)

    assert len(source_identity_ids) == 1
    assert len(source_identities) == 1
    assert source_identities[0]["source_value"] == "HG002"
    assert source_identities[0]["source_namespace"] == "vap_sample_id"


def test_attach_vap_sample_identity_is_idempotent(tmp_path: Path) -> None:
    package = (
        tmp_path
        / "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
    )
    (package / "entities" / "routing").mkdir(parents=True)
    (
        package / "entities" / "routing" / "coding_candidates.tsv"
    ).write_text("a\tb\n1\t2\n", encoding="utf-8")

    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifacts = list_artifact_records(connection, package_id)

    register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifacts,
        producer_family="VAP",
    )

    registrations = list_assertion_registrations(connection, package_id)

    first = attach_vap_sample_identity_to_assertions(
        connection=connection,
        package_path=inventory.package_path,
        assertion_registrations=registrations,
    )
    second = attach_vap_sample_identity_to_assertions(
        connection=connection,
        package_path=inventory.package_path,
        assertion_registrations=registrations,
    )

    count = connection.execute(
        "SELECT COUNT(*) AS count FROM source_identities"
    ).fetchone()["count"]

    assert first == second
    assert count == 1


def test_build_source_identity_from_participant() -> None:
    from variant_database.registration.source_identity import (
        build_source_identity_from_participant,
    )

    participant = ExtractedParticipant(
        participant_kind="gene",
        participant_role="gene",
        source_namespace="vap_gene_symbol",
        source_value="POLG",
        source_label="POLG",
        extraction_method="vap_row_column:gene_symbol",
        source_record_ref="row:1",
    )

    identity = build_source_identity_from_participant(
        assertion_registration_id="assertion-1",
        participant=participant,
    )

    assert identity.identity_kind == "gene"
    assert identity.participant_role == "gene"
    assert identity.source_namespace == "vap_gene_symbol"
    assert identity.source_value == "POLG"
    assert identity.source_record_ref == "row:1"


def test_attach_participants_to_assertion(tmp_path: Path) -> None:
    from variant_database.registration.source_identity import (
        attach_participants_to_assertion,
    )

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    # Create minimal parent package/artifact/assertion rows to satisfy FKs.
    connection.execute(
        """
        INSERT INTO tep_packages (
            package_id,
            package_path,
            package_exists,
            artifact_count,
            manifest_count
        )
        VALUES ('package-1', '/tmp/package', 1, 1, 0)
        """
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
        VALUES ('artifact-1', 'package-1', 'entities/routing/coding_candidates.tsv', 10, 'abc', 0)
        """
    )
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
        VALUES (
            'assertion-1',
            'package-1',
            'artifact-1',
            'routing_candidates',
            'candidate_routing',
            'VAP',
            NULL,
            'candidate_routing',
            '{}',
            '{}',
            'producer_emitted',
            'source_asserted',
            'registered',
            '{}'
        )
        """
    )
    connection.commit()

    participants = [
        ExtractedParticipant(
            participant_kind="gene",
            participant_role="gene",
            source_namespace="vap_gene_symbol",
            source_value="POLG",
            source_label="POLG",
            extraction_method="vap_row_column:gene_symbol",
            source_record_ref="row:1",
        ),
        ExtractedParticipant(
            participant_kind="gene",
            participant_role="gene",
            source_namespace="vap_ensembl_gene_id",
            source_value="ENSG00000140521",
            source_label="ENSG00000140521",
            extraction_method="vap_row_column:gene_id",
            source_record_ref="row:1",
        ),
    ]

    source_identity_ids = attach_participants_to_assertion(
        connection=connection,
        assertion_registration_id="assertion-1",
        participants=participants,
    )

    source_identities = list_source_identities(connection)

    assert len(source_identity_ids) == 2
    assert len(source_identities) == 2
    assert [identity["source_value"] for identity in source_identities] == [
        "ENSG00000140521",
        "POLG",
    ]


def test_source_identity_id_includes_source_record_ref() -> None:
    from variant_database.registration.source_identity import (
        build_source_identity,
    )

    row_1_identity = build_source_identity(
        assertion_registration_id="assertion-1",
        identity_kind="gene",
        participant_role="gene",
        source_value="POLG",
        source_namespace="vap_gene_symbol",
        source_label="POLG",
        extraction_method="vap_row_column:gene_symbol",
        source_record_ref="row:1",
    )

    row_2_identity = build_source_identity(
        assertion_registration_id="assertion-1",
        identity_kind="gene",
        participant_role="gene",
        source_value="POLG",
        source_namespace="vap_gene_symbol",
        source_label="POLG",
        extraction_method="vap_row_column:gene_symbol",
        source_record_ref="row:2",
    )

    assert row_1_identity.source_identity_id != row_2_identity.source_identity_id
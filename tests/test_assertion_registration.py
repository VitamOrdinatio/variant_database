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
    build_artifact_level_assertion_registration,
    list_assertion_registrations,
    register_artifact_level_assertions_for_package,
)


def test_build_artifact_level_assertion_for_evidence_bearing_surface() -> None:
    artifact_record = {
        "artifact_id": "artifact-1",
        "relative_path": "entities/coding_interpretation/stage_09_coding_interpreted.tsv",
        "size_bytes": 10,
        "sha256": "abc",
    }

    registration = build_artifact_level_assertion_registration(
        package_id="package-1",
        artifact_record=artifact_record,
        producer_family="VAP",
    )

    assert registration is not None
    assert registration.producer_family == "VAP"
    assert registration.surface_role == "coding_interpretation"
    assert registration.evidence_domain == "variant_interpretation"
    assert registration.authority_context == "producer_emitted"
    assert registration.registration_status == "registered"


def test_build_artifact_level_assertion_skips_context_surface() -> None:
    artifact_record = {
        "artifact_id": "artifact-1",
        "relative_path": "entities/context/stage_13_run_report.md",
        "size_bytes": 10,
        "sha256": "abc",
    }

    registration = build_artifact_level_assertion_registration(
        package_id="package-1",
        artifact_record=artifact_record,
        producer_family="VAP",
    )

    assert registration is None


def test_register_artifact_level_assertions_for_package(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    (package / "entities" / "coding_interpretation").mkdir(parents=True)
    (package / "entities" / "context").mkdir(parents=True)

    (
        package / "entities" / "coding_interpretation" / "stage_09_coding_interpreted.tsv"
    ).write_text("a\tb\n1\t2\n", encoding="utf-8")
    (
        package / "entities" / "context" / "stage_13_run_report.md"
    ).write_text("context", encoding="utf-8")
    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")

    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifacts = list_artifact_records(connection, package_id)

    assertion_ids = register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifacts,
        producer_family="VAP",
    )

    registrations = list_assertion_registrations(connection, package_id)

    assert len(assertion_ids) == 1
    assert len(registrations) == 1
    assert registrations[0]["surface_role"] == "coding_interpretation"
    assert registrations[0]["evidence_domain"] == "variant_interpretation"


def test_register_artifact_level_assertions_is_idempotent(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    (package / "entities" / "routing").mkdir(parents=True)

    (
        package / "entities" / "routing" / "coding_candidates.tsv"
    ).write_text("a\tb\n1\t2\n", encoding="utf-8")

    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifacts = list_artifact_records(connection, package_id)

    first = register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifacts,
        producer_family="VAP",
    )
    second = register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifacts,
        producer_family="VAP",
    )

    count = connection.execute(
        "SELECT COUNT(*) AS count FROM assertion_registrations"
    ).fetchone()["count"]

    assert first == second
    assert count == 1

from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.package_scanner import scan_package
from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.repositories import (
    get_package_record,
    list_artifact_records,
    persist_package_inventory,
)
from variant_database.persistence.schema_manager import (
    SCHEMA_VERSION,
    initialize_schema,
)


def test_initialize_schema_records_schema_version(tmp_path: Path) -> None:
    db_path = tmp_path / "vdb.sqlite"
    connection = connect_sqlite(db_path)
    initialize_schema(connection)

    row = connection.execute(
        "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
    ).fetchone()

    assert row["value"] == SCHEMA_VERSION


def test_persist_package_inventory_round_trip(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    (package / "data.tsv").write_text("a\tb\n1\t2\n", encoding="utf-8")

    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)

    package_record = get_package_record(connection, package_id)
    artifacts = list_artifact_records(connection, package_id)

    assert package_record is not None
    assert package_record["package_id"] == package_id
    assert package_record["artifact_count"] == 2
    assert package_record["manifest_count"] == 1

    assert [a["relative_path"] for a in artifacts] == [
        "data.tsv",
        "entity_inventory.json",
    ]

    manifest_records = [a for a in artifacts if a["is_manifest"] == 1]
    assert [a["relative_path"] for a in manifest_records] == ["entity_inventory.json"]


def test_persist_package_inventory_is_idempotent(tmp_path: Path) -> None:
    package = tmp_path / "tep"
    package.mkdir()

    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")
    (package / "lineage_manifest.json").write_text("{}", encoding="utf-8")
    inventory = scan_package(package)

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    first_package_id = persist_package_inventory(connection, inventory)
    second_package_id = persist_package_inventory(connection, inventory)

    package_count = connection.execute(
        "SELECT COUNT(*) AS count FROM tep_packages"
    ).fetchone()["count"]
    artifact_count = connection.execute(
        "SELECT COUNT(*) AS count FROM artifacts"
    ).fetchone()["count"]

    assert first_package_id == second_package_id
    assert package_count == 1
    assert artifact_count == 2

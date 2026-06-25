"""Persist the HG002 lightweight TEP inventory into a local SQLite store.

Development script only.

This script:
- scans the local HG002 lightweight TEP emulator
- initializes a local VDB SQLite database
- persists package/artifact inventory records
- prints summary counts

It does not mutate the VAP fixture.
"""

from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.package_scanner import scan_package
from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.repositories import (
    get_package_record,
    list_artifact_records,
    persist_package_inventory,
)
from variant_database.persistence.schema_manager import initialize_schema


TEP_PATH = Path(
    "/home/steelsparrow/dev/portfolio_projects/"
    "variant_annotation_pipeline/results/"
    "run_2026_06_03_010030/tep_emulation/"
    "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
)

DB_PATH = Path("results/persistence/hg002/vdb.sqlite")


def main() -> int:
    inventory = scan_package(TEP_PATH)

    connection = connect_sqlite(DB_PATH)
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)

    package_record = get_package_record(connection, package_id)
    artifact_records = list_artifact_records(connection, package_id)

    print("VDB persistence inventory run complete")
    print(f"TEP path: {TEP_PATH}")
    print(f"Database: {DB_PATH}")
    print(f"Package exists: {inventory.package_exists}")
    print(f"Package ID: {package_id}")
    print(f"Artifact count scanned: {inventory.artifact_count}")
    print(f"Artifact count persisted: {len(artifact_records)}")
    print(f"Manifest count scanned: {len(inventory.manifest_paths)}")

    if package_record is None:
        print("ERROR: package record was not persisted")
        return 1

    print(f"Manifest count persisted: {package_record['manifest_count']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build the bounded ERR10619300 first-1K preservation smoke substrate.

The script copies the certified discovery database, adds the preservation
schema, and streams the first 1,000 producer genotype rows into the copy. This
is an engineering smoke substrate, not the representative 3TEP_1K golden-fixture
candidate. The source discovery database and producer TEP remain unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path

from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.schema_manager import initialize_schema
from variant_database.registration.genotype_preservation import (
    GenotypePreservationRequest,
    preserve_genotype_observations,
)

SOURCE_DATABASE = Path(
    "results/registration/"
    "sys76_single_ERR10619300_genotype_discovery_1k/vdb.sqlite"
)
OUTPUT_DATABASE = Path(
    "results/registration/genotype_preservation_3tep_first1k_smoke/"
    "vap_ERR10619300_first1k_smoke/vdb.sqlite"
)
SOURCE_TEP_ID = "vap_tep_ERR10619300_run_2026_07_14_114546_v1"
SCOPE_LABEL = "genotype_3tep_first1k_smoke_v1"
ROW_LIMIT = 1000


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace only the dedicated "
            "genotype_preservation_3tep_first1k_smoke output database."
        ),
    )
    args = parser.parse_args()

    if (
        "first1k_smoke" not in str(OUTPUT_DATABASE).lower()
        or "first1k_smoke" not in SCOPE_LABEL.lower()
    ):
        raise RuntimeError(
            "The source-order bounded smoke path and scope label must retain "
            "the first1k_smoke classification"
        )
    if not SOURCE_DATABASE.is_file():
        raise FileNotFoundError(f"Source discovery database not found: {SOURCE_DATABASE}")

    OUTPUT_DATABASE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_DATABASE.exists():
        if not args.overwrite:
            raise FileExistsError(
                f"Output already exists: {OUTPUT_DATABASE}; pass --overwrite to replace it"
            )
        OUTPUT_DATABASE.unlink()
        for suffix in ("-journal", "-shm", "-wal"):
            Path(str(OUTPUT_DATABASE) + suffix).unlink(missing_ok=True)

    source_hash_before = _sha256(SOURCE_DATABASE)
    source_connection = sqlite3.connect(
        f"file:{SOURCE_DATABASE.resolve()}?mode=ro",
        uri=True,
    )
    destination_connection = sqlite3.connect(OUTPUT_DATABASE)
    try:
        source_connection.backup(destination_connection)
    finally:
        destination_connection.close()
        source_connection.close()

    connection = connect_sqlite(OUTPUT_DATABASE)
    try:
        initialize_schema(connection)
        rows = connection.execute(
            """
            SELECT package_id
            FROM source_genotype_package_classifications
            ORDER BY package_id
            """
        ).fetchall()
        if len(rows) != 1:
            raise ValueError(
                "Expected exactly one package classification in the copied discovery database"
            )
        package_id = str(rows[0][0])
        summary = preserve_genotype_observations(
            connection,
            GenotypePreservationRequest(
                package_id=package_id,
                scope_label=SCOPE_LABEL,
                source_tep_id=SOURCE_TEP_ID,
                row_limit=ROW_LIMIT,
                batch_size=500,
            ),
        )
    finally:
        connection.close()

    source_hash_after = _sha256(SOURCE_DATABASE)
    if source_hash_before != source_hash_after:
        raise RuntimeError("Source discovery database changed during preservation")

    print("=" * 80)
    print("3TEP first-1K smoke VAP genotype preservation substrate complete")
    print(f"Source discovery database: {SOURCE_DATABASE}")
    print(f"Source discovery SHA-256: {source_hash_after}")
    print(f"Output database: {OUTPUT_DATABASE}")
    print(f"Output database SHA-256: {_sha256(OUTPUT_DATABASE)}")
    print(f"Package ID: {summary.package_id}")
    print(f"Source TEP ID: {SOURCE_TEP_ID}")
    print(f"Preservation scope ID: {summary.preservation_scope_id}")
    print(f"Scope label: {summary.scope_label}")
    print(f"Scope kind: {summary.preservation_scope_kind}")
    print(f"Row selection policy: {summary.row_selection_policy}")
    print(f"Requested row limit: {summary.requested_row_limit}")
    print(f"Selected row count: {summary.selected_row_count}")
    print(f"Source declared row count: {summary.source_declared_row_count}")
    print(
        "Selected source row range: "
        f"{summary.first_selected_source_row}..{summary.last_selected_source_row}"
    )
    print(f"Source column count: {summary.source_column_count}")
    print(f"Preservation status: {summary.preservation_status}")
    print("Persisted package maturity remains: genotype_discovered")
    print("External preservation validation is required before maturity advancement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Registration orchestration.

The registration orchestrator composes previously validated VDB layers into
one executable registration path.

It does not define evidence rules.
It does not perform namespace resolution.
It does not attach canonical identities.
It does not interpret biology.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

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
from variant_database.registration.participant_extractor import (
    discover_participants_from_row,
)
from variant_database.registration.source_identity import (
    attach_participants_to_assertion,
    attach_vap_sample_identity_to_assertions,
    list_source_identities,
)


@dataclass(frozen=True)
class RegistrationPipelineSummary:
    """Summary of one registration pipeline execution."""

    package_id: str
    package_path: str
    db_path: str
    producer_family: str
    package_exists: bool
    artifact_count: int
    assertion_registration_count: int
    row_count_scanned: int
    participant_count_discovered: int
    source_identity_count: int


def _iter_tsv_rows(
    path: Path,
    max_rows: int | None = None,
) -> Iterator[tuple[str, dict[str, str]]]:
    """Iterate TSV rows with deterministic source record references."""
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")

        for row_index, row in enumerate(reader, start=1):
            if max_rows is not None and row_index > max_rows:
                break

            yield f"row:{row_index}", dict(row)


def _is_tsv_artifact(relative_path: str) -> bool:
    return relative_path.lower().endswith(".tsv")


def run_registration_pipeline(
    package_path: Path | str,
    db_path: Path | str,
    producer_family: str,
    max_rows_per_artifact: int | None = None,
) -> RegistrationPipelineSummary:
    """Run the VDB registration pipeline for one package."""
    package = Path(package_path).expanduser().resolve()
    database = Path(db_path)

    inventory = scan_package(package)

    connection = connect_sqlite(database)
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifact_records = list_artifact_records(connection, package_id)

    register_artifact_level_assertions_for_package(
        connection=connection,
        package_id=package_id,
        artifact_records=artifact_records,
        producer_family=producer_family,
    )

    assertion_registrations = list_assertion_registrations(
        connection=connection,
        package_id=package_id,
    )

    # Package-level identity attachment remains producer-specific for now.
    if producer_family.strip().upper() == "VAP":
        attach_vap_sample_identity_to_assertions(
            connection=connection,
            package_path=inventory.package_path,
            assertion_registrations=assertion_registrations,
        )

    artifact_by_id = {
        str(artifact["artifact_id"]): artifact
        for artifact in artifact_records
    }

    row_count_scanned = 0
    participant_count_discovered = 0

    for registration in assertion_registrations:
        artifact_id = str(registration["artifact_id"])
        artifact = artifact_by_id[artifact_id]
        relative_path = str(artifact["relative_path"])

        if not _is_tsv_artifact(relative_path):
            continue

        artifact_path = package / relative_path

        for source_record_ref, row in _iter_tsv_rows(
            artifact_path,
            max_rows=max_rows_per_artifact,
        ):
            row_count_scanned += 1

            participants = discover_participants_from_row(
                producer_family=producer_family,
                row=row,
                source_record_ref=source_record_ref,
            )

            participant_count_discovered += len(participants)

            attach_participants_to_assertion(
                connection=connection,
                assertion_registration_id=str(
                    registration["assertion_registration_id"]
                ),
                participants=participants,
            )

    source_identities = list_source_identities(connection)

    return RegistrationPipelineSummary(
        package_id=package_id,
        package_path=inventory.package_path,
        db_path=str(database),
        producer_family=producer_family,
        package_exists=inventory.package_exists,
        artifact_count=inventory.artifact_count,
        assertion_registration_count=len(assertion_registrations),
        row_count_scanned=row_count_scanned,
        participant_count_discovered=participant_count_discovered,
        source_identity_count=len(source_identities),
    )

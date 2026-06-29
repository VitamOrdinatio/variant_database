"""
Phase 4 Registration Unit deterministic inventory artifact emission.

This module converts read-only Registration Unit inspection results into stable
inventory artifacts.

It may:
    - flatten inspection results into deterministic inventory rows
    - emit TSV inventory artifacts
    - emit JSON inventory artifacts

It must not:
    - load manifests
    - open SQLite databases
    - inspect SQLite contents
    - mutate Registration Units
    - certify Registration Units

Operating rule:
    Inspect elsewhere. Emit deterministically here. Never mutate.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from variant_database.phase4.registration_units.inspection import (
    REQUIRED_TABLES,
    RegistrationUnitInspectionResult,
)


INVENTORY_SCHEMA_VERSION = "phase4_registration_unit_inventory_v1"

INVENTORY_TSV_FILENAME = "registration_unit_inventory.tsv"
INVENTORY_JSON_FILENAME = "registration_unit_inventory.json"

INVENTORY_COLUMNS = [
    "inventory_schema_version",
    "registration_unit_id",
    "registration_unit_label",
    "producer_family",
    "validation_layer",
    "source_role",
    "registration_backend",
    "registration_unit_path_resolved",
    "sqlite_path_resolved",
    "expected_read_mode",
    "open_status",
    "query_only_status",
    "required_table_status",
    "integrity_check_status",
    "inspection_status",
    "schema_metadata_row_count",
    "tep_packages_row_count",
    "artifacts_row_count",
    "assertion_registrations_row_count",
    "source_identities_row_count",
]


class RegistrationUnitInventoryError(ValueError):
    """Raised when inventory artifacts cannot be built or emitted."""


@dataclass(frozen=True)
class RegistrationUnitInventoryRow:
    """Flattened deterministic inventory row for one Registration Unit."""

    inventory_schema_version: str
    registration_unit_id: str
    registration_unit_label: str
    producer_family: str
    validation_layer: str
    source_role: str
    registration_backend: str
    registration_unit_path_resolved: str
    sqlite_path_resolved: str
    expected_read_mode: str
    open_status: str
    query_only_status: str
    required_table_status: str
    integrity_check_status: str
    inspection_status: str
    schema_metadata_row_count: int
    tep_packages_row_count: int
    artifacts_row_count: int
    assertion_registrations_row_count: int
    source_identities_row_count: int

    def as_dict(self) -> dict[str, str]:
        """Return a stable string dictionary for TSV/JSON emission."""
        return {
            "inventory_schema_version": self.inventory_schema_version,
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "producer_family": self.producer_family,
            "validation_layer": self.validation_layer,
            "source_role": self.source_role,
            "registration_backend": self.registration_backend,
            "registration_unit_path_resolved": self.registration_unit_path_resolved,
            "sqlite_path_resolved": self.sqlite_path_resolved,
            "expected_read_mode": self.expected_read_mode,
            "open_status": self.open_status,
            "query_only_status": self.query_only_status,
            "required_table_status": self.required_table_status,
            "integrity_check_status": self.integrity_check_status,
            "inspection_status": self.inspection_status,
            "schema_metadata_row_count": str(self.schema_metadata_row_count),
            "tep_packages_row_count": str(self.tep_packages_row_count),
            "artifacts_row_count": str(self.artifacts_row_count),
            "assertion_registrations_row_count": str(
                self.assertion_registrations_row_count
            ),
            "source_identities_row_count": str(self.source_identities_row_count),
        }


@dataclass(frozen=True)
class RegistrationUnitInventoryArtifactSet:
    """Paths and row count for emitted inventory artifacts."""

    output_dir: Path
    tsv_path: Path
    json_path: Path
    row_count: int
    artifact_status: str


def build_registration_unit_inventory_rows(
    inspection_results: list[RegistrationUnitInspectionResult],
) -> list[RegistrationUnitInventoryRow]:
    """
    Build deterministic Registration Unit inventory rows.

    Rows are sorted by registration_unit_id to keep artifact emission stable even
    if callers provide inspection results in a different order.
    """
    if not inspection_results:
        raise RegistrationUnitInventoryError(
            "Cannot build Registration Unit inventory from zero inspection results."
        )

    rows = [
        _inventory_row_from_inspection_result(result)
        for result in inspection_results
    ]

    return sorted(rows, key=lambda row: row.registration_unit_id)


def emit_registration_unit_inventory_artifacts(
    inspection_results: list[RegistrationUnitInspectionResult],
    output_dir: str | Path,
) -> RegistrationUnitInventoryArtifactSet:
    """
    Emit deterministic TSV and JSON Registration Unit inventory artifacts.

    This function writes only to the supplied output directory. It does not open
    or touch Registration Unit SQLite files.
    """
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    rows = build_registration_unit_inventory_rows(inspection_results)

    tsv_path = destination / INVENTORY_TSV_FILENAME
    json_path = destination / INVENTORY_JSON_FILENAME

    _write_inventory_tsv(tsv_path, rows)
    _write_inventory_json(json_path, rows)

    return RegistrationUnitInventoryArtifactSet(
        output_dir=destination,
        tsv_path=tsv_path,
        json_path=json_path,
        row_count=len(rows),
        artifact_status="passed",
    )


def _inventory_row_from_inspection_result(
    result: RegistrationUnitInspectionResult,
) -> RegistrationUnitInventoryRow:
    table_counts = _table_counts_by_name(result)

    return RegistrationUnitInventoryRow(
        inventory_schema_version=INVENTORY_SCHEMA_VERSION,
        registration_unit_id=result.registration_unit_id,
        registration_unit_label=result.registration_unit_label,
        producer_family=result.producer_family,
        validation_layer=result.validation_layer,
        source_role=result.source_role,
        registration_backend=result.registration_backend,
        registration_unit_path_resolved=str(result.registration_unit_path_resolved),
        sqlite_path_resolved=str(result.sqlite_path_resolved),
        expected_read_mode=result.expected_read_mode,
        open_status=result.open_status,
        query_only_status=result.query_only_status,
        required_table_status=result.required_table_status,
        integrity_check_status=result.integrity_check_status,
        inspection_status=result.inspection_status,
        schema_metadata_row_count=table_counts["schema_metadata"],
        tep_packages_row_count=table_counts["tep_packages"],
        artifacts_row_count=table_counts["artifacts"],
        assertion_registrations_row_count=table_counts["assertion_registrations"],
        source_identities_row_count=table_counts["source_identities"],
    )


def _table_counts_by_name(
    result: RegistrationUnitInspectionResult,
) -> dict[str, int]:
    observed = {table.table_name: table for table in result.table_results}
    counts: dict[str, int] = {}

    for table_name in REQUIRED_TABLES:
        if table_name not in observed:
            raise RegistrationUnitInventoryError(
                f"{result.registration_unit_id}: missing table inspection result: "
                f"{table_name}"
            )

        row_count = observed[table_name].row_count
        if row_count is None:
            raise RegistrationUnitInventoryError(
                f"{result.registration_unit_id}: table row count is unavailable: "
                f"{table_name}"
            )

        counts[table_name] = row_count

    return counts


def _write_inventory_tsv(
    path: Path,
    rows: list[RegistrationUnitInventoryRow],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=INVENTORY_COLUMNS,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.as_dict())


def _write_inventory_json(
    path: Path,
    rows: list[RegistrationUnitInventoryRow],
) -> None:
    payload = {
        "inventory_schema_version": INVENTORY_SCHEMA_VERSION,
        "row_count": len(rows),
        "registration_units": [row.as_dict() for row in rows],
    }

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

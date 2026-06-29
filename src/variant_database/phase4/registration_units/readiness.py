"""
Phase 4 Registration Unit readiness and validation artifact emission.

This module evaluates deterministic readiness from inventory rows.

It may:
    - evaluate inventory rows against Phase 4.1 readiness gates
    - emit readiness TSV artifacts
    - emit readiness JSON artifacts
    - emit validation summary JSON artifacts

It must not:
    - load manifests
    - open SQLite databases
    - inspect SQLite contents
    - mutate Registration Units
    - certify Registration Units

Operating rule:
    Inventory describes. Readiness evaluates. Validation summarizes. Never mutate.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from variant_database.phase4.registration_units.inventory import (
    RegistrationUnitInventoryRow,
)


READINESS_SCHEMA_VERSION = "phase4_registration_unit_readiness_v1"

READINESS_TSV_FILENAME = "registration_unit_readiness.tsv"
READINESS_JSON_FILENAME = "registration_unit_readiness.json"
VALIDATION_SUMMARY_JSON_FILENAME = "registration_unit_validation_summary.json"

READINESS_COLUMNS = [
    "readiness_schema_version",
    "registration_unit_id",
    "registration_unit_label",
    "producer_family",
    "validation_layer",
    "source_role",
    "registration_backend",
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
    "readiness_status",
    "readiness_reasons",
]


class RegistrationUnitReadinessError(ValueError):
    """Raised when readiness artifacts cannot be built or emitted."""


@dataclass(frozen=True)
class RegistrationUnitReadinessRow:
    """Deterministic readiness row for one Registration Unit."""

    readiness_schema_version: str
    registration_unit_id: str
    registration_unit_label: str
    producer_family: str
    validation_layer: str
    source_role: str
    registration_backend: str
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
    readiness_status: str
    readiness_reasons: str

    def as_dict(self) -> dict[str, str]:
        """Return a stable string dictionary for TSV/JSON emission."""
        return {
            "readiness_schema_version": self.readiness_schema_version,
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "producer_family": self.producer_family,
            "validation_layer": self.validation_layer,
            "source_role": self.source_role,
            "registration_backend": self.registration_backend,
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
            "readiness_status": self.readiness_status,
            "readiness_reasons": self.readiness_reasons,
        }


@dataclass(frozen=True)
class RegistrationUnitReadinessArtifactSet:
    """Paths and status for emitted readiness/validation artifacts."""

    output_dir: Path
    readiness_tsv_path: Path
    readiness_json_path: Path
    validation_summary_json_path: Path
    row_count: int
    ready_count: int
    not_ready_count: int
    artifact_status: str


def build_registration_unit_readiness_rows(
    inventory_rows: list[RegistrationUnitInventoryRow],
) -> list[RegistrationUnitReadinessRow]:
    """
    Build deterministic Registration Unit readiness rows.

    Rows are sorted by registration_unit_id so output is stable regardless of
    caller input order.
    """
    if not inventory_rows:
        raise RegistrationUnitReadinessError(
            "Cannot build Registration Unit readiness from zero inventory rows."
        )

    rows = [_readiness_row_from_inventory_row(row) for row in inventory_rows]

    return sorted(rows, key=lambda row: row.registration_unit_id)


def emit_registration_unit_readiness_artifacts(
    inventory_rows: list[RegistrationUnitInventoryRow],
    output_dir: str | Path,
) -> RegistrationUnitReadinessArtifactSet:
    """
    Emit deterministic readiness and validation artifacts.

    This function writes only to the supplied output directory. It does not open
    or touch Registration Unit SQLite files.
    """
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    rows = build_registration_unit_readiness_rows(inventory_rows)

    readiness_tsv_path = destination / READINESS_TSV_FILENAME
    readiness_json_path = destination / READINESS_JSON_FILENAME
    validation_summary_json_path = destination / VALIDATION_SUMMARY_JSON_FILENAME

    _write_readiness_tsv(readiness_tsv_path, rows)
    _write_readiness_json(readiness_json_path, rows)
    _write_validation_summary_json(validation_summary_json_path, rows)

    ready_count = sum(1 for row in rows if row.readiness_status == "ready")
    not_ready_count = sum(1 for row in rows if row.readiness_status != "ready")

    return RegistrationUnitReadinessArtifactSet(
        output_dir=destination,
        readiness_tsv_path=readiness_tsv_path,
        readiness_json_path=readiness_json_path,
        validation_summary_json_path=validation_summary_json_path,
        row_count=len(rows),
        ready_count=ready_count,
        not_ready_count=not_ready_count,
        artifact_status="passed" if not_ready_count == 0 else "failed",
    )


def _readiness_row_from_inventory_row(
    row: RegistrationUnitInventoryRow,
) -> RegistrationUnitReadinessRow:
    reasons = _readiness_failure_reasons(row)
    readiness_status = "ready" if not reasons else "not_ready"
    readiness_reasons = "passed" if not reasons else ";".join(reasons)

    return RegistrationUnitReadinessRow(
        readiness_schema_version=READINESS_SCHEMA_VERSION,
        registration_unit_id=row.registration_unit_id,
        registration_unit_label=row.registration_unit_label,
        producer_family=row.producer_family,
        validation_layer=row.validation_layer,
        source_role=row.source_role,
        registration_backend=row.registration_backend,
        expected_read_mode=row.expected_read_mode,
        open_status=row.open_status,
        query_only_status=row.query_only_status,
        required_table_status=row.required_table_status,
        integrity_check_status=row.integrity_check_status,
        inspection_status=row.inspection_status,
        schema_metadata_row_count=row.schema_metadata_row_count,
        tep_packages_row_count=row.tep_packages_row_count,
        artifacts_row_count=row.artifacts_row_count,
        assertion_registrations_row_count=row.assertion_registrations_row_count,
        source_identities_row_count=row.source_identities_row_count,
        readiness_status=readiness_status,
        readiness_reasons=readiness_reasons,
    )


def _readiness_failure_reasons(
    row: RegistrationUnitInventoryRow,
) -> list[str]:
    reasons: list[str] = []

    if row.registration_backend != "sqlite":
        reasons.append("registration_backend_not_sqlite")

    if row.expected_read_mode != "read_only":
        reasons.append("expected_read_mode_not_read_only")

    if row.open_status != "passed":
        reasons.append("open_status_not_passed")

    if row.query_only_status != "enabled":
        reasons.append("query_only_status_not_enabled")

    if row.required_table_status != "passed":
        reasons.append("required_table_status_not_passed")

    if row.integrity_check_status != "ok":
        reasons.append("integrity_check_status_not_ok")

    if row.inspection_status != "passed":
        reasons.append("inspection_status_not_passed")

    row_count_checks = {
        "schema_metadata": row.schema_metadata_row_count,
        "tep_packages": row.tep_packages_row_count,
        "artifacts": row.artifacts_row_count,
        "assertion_registrations": row.assertion_registrations_row_count,
        "source_identities": row.source_identities_row_count,
    }

    for table_name, row_count in row_count_checks.items():
        if row_count <= 0:
            reasons.append(f"{table_name}_row_count_not_positive")

    return reasons


def _write_readiness_tsv(
    path: Path,
    rows: list[RegistrationUnitReadinessRow],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=READINESS_COLUMNS,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.as_dict())


def _write_readiness_json(
    path: Path,
    rows: list[RegistrationUnitReadinessRow],
) -> None:
    payload = {
        "readiness_schema_version": READINESS_SCHEMA_VERSION,
        "row_count": len(rows),
        "ready_count": sum(1 for row in rows if row.readiness_status == "ready"),
        "not_ready_count": sum(
            1 for row in rows if row.readiness_status != "ready"
        ),
        "registration_units": [row.as_dict() for row in rows],
    }

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_validation_summary_json(
    path: Path,
    rows: list[RegistrationUnitReadinessRow],
) -> None:
    ready_count = sum(1 for row in rows if row.readiness_status == "ready")
    not_ready_count = len(rows) - ready_count

    payload = {
        "readiness_schema_version": READINESS_SCHEMA_VERSION,
        "validation_status": "passed" if not_ready_count == 0 else "failed",
        "row_count": len(rows),
        "ready_count": ready_count,
        "not_ready_count": not_ready_count,
        "validation_gates": {
            "registration_backend": "sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "enabled",
            "required_table_status": "passed",
            "integrity_check_status": "ok",
            "inspection_status": "passed",
            "required_row_counts": "positive",
        },
        "not_ready_registration_units": [
            {
                "registration_unit_id": row.registration_unit_id,
                "registration_unit_label": row.registration_unit_label,
                "readiness_reasons": row.readiness_reasons,
            }
            for row in rows
            if row.readiness_status != "ready"
        ],
    }

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

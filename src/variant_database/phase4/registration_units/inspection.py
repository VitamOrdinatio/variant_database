"""
Phase 4 Registration Unit read-only inspection.

This module implements the first SQLite-aware Phase 4.1 layer.

It may:
    - open declared Registration Unit SQLite files read-only
    - set SQLite query_only mode
    - inspect required table presence
    - inspect required column presence
    - count rows in required tables
    - run read-only integrity checks

It must not:
    - write SQLite databases
    - create tables, indexes, triggers, views, or sidecars
    - emit inventory/readiness artifacts
    - mutate fixture or MARK source artifacts

Operating rule:
    Inspect read-only. Emit artifacts later. Never mutate.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from variant_database.phase4.registration_units.manifest import RegistrationUnitManifestRecord


REQUIRED_TABLES = [
    "schema_metadata",
    "tep_packages",
    "artifacts",
    "assertion_registrations",
    "source_identities",
]

REQUIRED_TABLE_COLUMNS = {
    "schema_metadata": {
        "key",
        "value",
    },
    "tep_packages": {
        "package_id",
        "package_path",
        "package_exists",
        "artifact_count",
        "manifest_count",
    },
    "artifacts": {
        "artifact_id",
        "package_id",
        "relative_path",
        "size_bytes",
        "sha256",
        "is_manifest",
    },
    "assertion_registrations": {
        "assertion_registration_id",
        "package_id",
        "artifact_id",
        "surface_role",
        "evidence_domain",
        "producer_family",
        "source_record_ref",
        "assertion_type",
        "participant_summary_json",
        "support_ref_json",
        "authority_context",
        "uncertainty_context",
        "registration_status",
        "payload_json",
    },
    "source_identities": {
        "source_identity_id",
        "assertion_registration_id",
        "identity_kind",
        "participant_role",
        "source_value",
        "source_namespace",
        "source_label",
        "extraction_method",
        "source_record_ref",
        "payload_json",
    },
}


class RegistrationUnitInspectionError(RuntimeError):
    """Raised when a Registration Unit cannot be inspected read-only."""


@dataclass(frozen=True)
class TableInspectionResult:
    """Inspection result for a single required table."""

    table_name: str
    exists: bool
    required_columns: tuple[str, ...]
    present_columns: tuple[str, ...]
    missing_columns: tuple[str, ...]
    row_count: int | None
    table_status: str

    def as_dict(self) -> dict[str, str]:
        return {
            "table_name": self.table_name,
            "exists": str(self.exists),
            "required_columns": ",".join(self.required_columns),
            "present_columns": ",".join(self.present_columns),
            "missing_columns": ",".join(self.missing_columns),
            "row_count": "" if self.row_count is None else str(self.row_count),
            "table_status": self.table_status,
        }


@dataclass(frozen=True)
class RegistrationUnitInspectionResult:
    """Read-only inspection result for one declared Registration Unit."""

    manifest_path: Path
    manifest_row_number: int
    registration_unit_id: str
    registration_unit_label: str
    producer_family: str
    validation_layer: str
    source_role: str
    registration_backend: str
    registration_unit_path_resolved: Path
    sqlite_path_resolved: Path
    expected_read_mode: str

    open_status: str
    query_only_status: str
    required_table_status: str
    integrity_check_status: str
    inspection_status: str
    table_results: tuple[TableInspectionResult, ...]

    def as_dict(self) -> dict[str, str]:
        return {
            "manifest_path": str(self.manifest_path),
            "manifest_row_number": str(self.manifest_row_number),
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "producer_family": self.producer_family,
            "validation_layer": self.validation_layer,
            "source_role": self.source_role,
            "registration_backend": self.registration_backend,
            "registration_unit_path_resolved": str(self.registration_unit_path_resolved),
            "sqlite_path_resolved": str(self.sqlite_path_resolved),
            "expected_read_mode": self.expected_read_mode,
            "open_status": self.open_status,
            "query_only_status": self.query_only_status,
            "required_table_status": self.required_table_status,
            "integrity_check_status": self.integrity_check_status,
            "inspection_status": self.inspection_status,
        }


def inspect_registration_units(
    records: list[RegistrationUnitManifestRecord],
) -> list[RegistrationUnitInspectionResult]:
    """Inspect multiple declared Registration Units read-only."""
    return [inspect_registration_unit(record) for record in records]


def inspect_registration_unit(
    record: RegistrationUnitManifestRecord,
) -> RegistrationUnitInspectionResult:
    """
    Inspect one declared Registration Unit read-only.

    This function opens SQLite, but only with read-only/query-only intent.
    It does not write output artifacts.
    """
    _validate_record_for_inspection(record)

    conn = _open_read_only_connection(record.sqlite_path_resolved)

    try:
        query_only_status = _query_only_status(conn)
        table_results = tuple(_inspect_required_tables(conn))
        required_table_status = _required_table_status(table_results)
        integrity_check_status = _integrity_check_status(conn)

        inspection_status = (
            "passed"
            if (
                query_only_status == "enabled"
                and required_table_status == "passed"
                and integrity_check_status == "ok"
            )
            else "failed"
        )

        return RegistrationUnitInspectionResult(
            manifest_path=record.manifest_path,
            manifest_row_number=record.manifest_row_number,
            registration_unit_id=record.registration_unit_id,
            registration_unit_label=record.registration_unit_label,
            producer_family=record.producer_family,
            validation_layer=record.validation_layer,
            source_role=record.source_role,
            registration_backend=record.registration_backend,
            registration_unit_path_resolved=record.registration_unit_path_resolved,
            sqlite_path_resolved=record.sqlite_path_resolved,
            expected_read_mode=record.expected_read_mode,
            open_status="passed",
            query_only_status=query_only_status,
            required_table_status=required_table_status,
            integrity_check_status=integrity_check_status,
            inspection_status=inspection_status,
            table_results=table_results,
        )
    finally:
        conn.close()


def _validate_record_for_inspection(record: RegistrationUnitManifestRecord) -> None:
    if record.registration_backend != "sqlite":
        raise RegistrationUnitInspectionError(
            f"{record.registration_unit_id}: unsupported backend for inspection: "
            f"{record.registration_backend}"
        )

    if record.expected_read_mode != "read_only":
        raise RegistrationUnitInspectionError(
            f"{record.registration_unit_id}: inspection requires read_only mode; "
            f"observed {record.expected_read_mode}"
        )

    if not record.sqlite_path_resolved.exists():
        raise RegistrationUnitInspectionError(
            f"{record.registration_unit_id}: sqlite_path does not exist: "
            f"{record.sqlite_path_resolved}"
        )

    if not record.sqlite_path_resolved.is_file():
        raise RegistrationUnitInspectionError(
            f"{record.registration_unit_id}: sqlite_path is not a file: "
            f"{record.sqlite_path_resolved}"
        )


def _open_read_only_connection(sqlite_path: Path) -> sqlite3.Connection:
    uri = f"file:{sqlite_path.as_posix()}?mode=ro&immutable=1"

    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        raise RegistrationUnitInspectionError(
            f"Could not open SQLite read-only: {sqlite_path}: {exc}"
        ) from exc

    conn.row_factory = sqlite3.Row

    try:
        conn.execute("PRAGMA query_only=ON;")
    except sqlite3.Error as exc:
        conn.close()
        raise RegistrationUnitInspectionError(
            f"Could not set query_only mode for SQLite: {sqlite_path}: {exc}"
        ) from exc

    return conn


def _query_only_status(conn: sqlite3.Connection) -> str:
    row = conn.execute("PRAGMA query_only;").fetchone()
    if row is None:
        return "unknown"

    value = row[0]
    return "enabled" if int(value) == 1 else "disabled"


def _inspect_required_tables(
    conn: sqlite3.Connection,
) -> list[TableInspectionResult]:
    existing_tables = _table_names(conn)
    results: list[TableInspectionResult] = []

    for table_name in REQUIRED_TABLES:
        required_columns = tuple(sorted(REQUIRED_TABLE_COLUMNS[table_name]))

        if table_name not in existing_tables:
            results.append(
                TableInspectionResult(
                    table_name=table_name,
                    exists=False,
                    required_columns=required_columns,
                    present_columns=tuple(),
                    missing_columns=required_columns,
                    row_count=None,
                    table_status="missing_table",
                )
            )
            continue

        present_columns = tuple(sorted(_table_columns(conn, table_name)))
        missing_columns = tuple(sorted(set(required_columns) - set(present_columns)))
        row_count = _count_rows(conn, table_name)

        table_status = "passed" if not missing_columns else "missing_columns"

        results.append(
            TableInspectionResult(
                table_name=table_name,
                exists=True,
                required_columns=required_columns,
                present_columns=present_columns,
                missing_columns=missing_columns,
                row_count=row_count,
                table_status=table_status,
            )
        )

    return results


def _required_table_status(
    table_results: tuple[TableInspectionResult, ...],
) -> str:
    failed = [
        result.table_name
        for result in table_results
        if result.table_status != "passed"
    ]

    if failed:
        return "failed:" + ",".join(failed)

    return "passed"


def _integrity_check_status(conn: sqlite3.Connection) -> str:
    row = conn.execute("PRAGMA integrity_check;").fetchone()
    if row is None:
        return "unknown"
    return str(row[0])


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return {str(row["name"]) for row in rows}


def _table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({_quote_identifier(table_name)})").fetchall()
    return [str(row["name"]) for row in rows]


def _count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(
        f"SELECT COUNT(*) AS row_count FROM {_quote_identifier(table_name)}"
    ).fetchone()
    return int(row["row_count"])


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'
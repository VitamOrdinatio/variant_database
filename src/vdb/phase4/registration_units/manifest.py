"""
Phase 4 Registration Unit input manifest handling.

This module implements the declarative manifest layer only.

It may:
    - read a TSV manifest
    - validate declared fields
    - resolve Registration Unit paths
    - optionally verify declared filesystem paths exist

It must not:
    - open SQLite databases
    - inspect SQLite table surfaces
    - count database rows
    - emit inventory/readiness artifacts
    - mutate source artifacts

Operating rule:
    Declare first. Inspect later. Never mutate.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = [
    "manifest_schema_version",
    "registration_unit_id",
    "registration_unit_label",
    "producer_family",
    "validation_layer",
    "source_role",
    "registration_backend",
    "registration_unit_path",
    "sqlite_path",
    "expected_read_mode",
    "notes",
]

REQUIRED_NONEMPTY_COLUMNS = [
    column for column in REQUIRED_COLUMNS if column != "notes"
]

ALLOWED_MANIFEST_SCHEMA_VERSIONS = {"v1"}
ALLOWED_PRODUCER_FAMILIES = {"GSC", "VAP"}
ALLOWED_VALIDATION_LAYERS = {
    "validation_layer_2_lightweight_fixture",
    "validation_layer_3_mark_full_corpus",
}
ALLOWED_SOURCE_ROLES = {
    "phase4_golden_fixture",
    "mark_phase3_canonical_full_corpus",
}
ALLOWED_REGISTRATION_BACKENDS = {"sqlite"}
ALLOWED_READ_MODES = {"read_only"}


class RegistrationUnitManifestError(ValueError):
    """Raised when a Registration Unit input manifest is invalid."""


@dataclass(frozen=True)
class RegistrationUnitManifestRecord:
    """Normalized Registration Unit manifest record."""

    manifest_path: Path
    manifest_row_number: int

    manifest_schema_version: str
    registration_unit_id: str
    registration_unit_label: str
    producer_family: str
    validation_layer: str
    source_role: str
    registration_backend: str

    registration_unit_path_declared: str
    sqlite_path_declared: str
    registration_unit_path_resolved: Path
    sqlite_path_resolved: Path

    expected_read_mode: str
    notes: str

    path_resolution_status: str
    declaration_status: str

    def as_dict(self) -> dict[str, str]:
        """Return a stable string dictionary for reporting or TSV emission."""
        return {
            "manifest_path": str(self.manifest_path),
            "manifest_row_number": str(self.manifest_row_number),
            "manifest_schema_version": self.manifest_schema_version,
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "producer_family": self.producer_family,
            "validation_layer": self.validation_layer,
            "source_role": self.source_role,
            "registration_backend": self.registration_backend,
            "registration_unit_path_declared": self.registration_unit_path_declared,
            "sqlite_path_declared": self.sqlite_path_declared,
            "registration_unit_path_resolved": str(self.registration_unit_path_resolved),
            "sqlite_path_resolved": str(self.sqlite_path_resolved),
            "expected_read_mode": self.expected_read_mode,
            "notes": self.notes,
            "path_resolution_status": self.path_resolution_status,
            "declaration_status": self.declaration_status,
        }


def load_registration_unit_manifest(
    manifest_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    validate_filesystem: bool = False,
) -> list[RegistrationUnitManifestRecord]:
    """
    Load and validate a Registration Unit input manifest.

    Parameters
    ----------
    manifest_path:
        Path to the TSV manifest.

    repo_root:
        Repository root used to resolve relative Registration Unit paths.
        Defaults to the current working directory.

    validate_filesystem:
        When true, confirm that the resolved Registration Unit directories exist
        and that resolved SQLite paths exist as files. This still does not open
        SQLite databases.

    Returns
    -------
    list[RegistrationUnitManifestRecord]
        Normalized Registration Unit declarations.

    Raises
    ------
    RegistrationUnitManifestError
        If the manifest is invalid.
    """
    manifest = Path(manifest_path)
    root = Path.cwd() if repo_root is None else Path(repo_root)

    if not manifest.exists():
        raise RegistrationUnitManifestError(f"Manifest file does not exist: {manifest}")

    if not manifest.is_file():
        raise RegistrationUnitManifestError(f"Manifest path is not a file: {manifest}")

    rows = _read_manifest_rows(manifest)
    if not rows:
        raise RegistrationUnitManifestError(f"Manifest contains no records: {manifest}")

    records: list[RegistrationUnitManifestRecord] = []

    seen_ids: set[str] = set()
    seen_labels: set[str] = set()

    for row_number, row in rows:
        _validate_required_fields(manifest, row_number, row)
        _validate_allowed_values(manifest, row_number, row)

        registration_unit_id = row["registration_unit_id"].strip()
        registration_unit_label = row["registration_unit_label"].strip()

        if registration_unit_id in seen_ids:
            raise RegistrationUnitManifestError(
                f"{manifest}:{row_number}: duplicate registration_unit_id: "
                f"{registration_unit_id}"
            )
        seen_ids.add(registration_unit_id)

        if registration_unit_label in seen_labels:
            raise RegistrationUnitManifestError(
                f"{manifest}:{row_number}: duplicate registration_unit_label: "
                f"{registration_unit_label}"
            )
        seen_labels.add(registration_unit_label)

        registration_unit_path_declared = row["registration_unit_path"].strip()
        sqlite_path_declared = row["sqlite_path"].strip()

        registration_unit_path_resolved = _resolve_registration_unit_path(
            registration_unit_path_declared,
            repo_root=root,
        )
        sqlite_path_resolved = _resolve_sqlite_path(
            sqlite_path_declared,
            registration_unit_path_resolved=registration_unit_path_resolved,
        )

        if validate_filesystem:
            _validate_filesystem_paths(
                manifest=manifest,
                row_number=row_number,
                registration_unit_path=registration_unit_path_resolved,
                sqlite_path=sqlite_path_resolved,
            )

        records.append(
            RegistrationUnitManifestRecord(
                manifest_path=manifest,
                manifest_row_number=row_number,
                manifest_schema_version=row["manifest_schema_version"].strip(),
                registration_unit_id=registration_unit_id,
                registration_unit_label=registration_unit_label,
                producer_family=row["producer_family"].strip(),
                validation_layer=row["validation_layer"].strip(),
                source_role=row["source_role"].strip(),
                registration_backend=row["registration_backend"].strip(),
                registration_unit_path_declared=registration_unit_path_declared,
                sqlite_path_declared=sqlite_path_declared,
                registration_unit_path_resolved=registration_unit_path_resolved,
                sqlite_path_resolved=sqlite_path_resolved,
                expected_read_mode=row["expected_read_mode"].strip(),
                notes=row.get("notes", "").strip(),
                path_resolution_status="resolved",
                declaration_status="valid",
            )
        )

    return records


def _read_manifest_rows(manifest: Path) -> list[tuple[int, dict[str, str]]]:
    with manifest.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")

        if reader.fieldnames is None:
            raise RegistrationUnitManifestError(
                f"Manifest has no header row: {manifest}"
            )

        missing_columns = [
            column for column in REQUIRED_COLUMNS if column not in reader.fieldnames
        ]
        if missing_columns:
            raise RegistrationUnitManifestError(
                f"Manifest missing required columns: {missing_columns}"
            )

        unexpected_blank_headers = [
            header for header in reader.fieldnames if header is None or not header.strip()
        ]
        if unexpected_blank_headers:
            raise RegistrationUnitManifestError(
                f"Manifest contains blank header columns: {manifest}"
            )

        return [
            (row_number, _normalize_row(row))
            for row_number, row in enumerate(reader, start=2)
        ]


def _normalize_row(row: dict[str, str | None]) -> dict[str, str]:
    return {
        key: "" if value is None else str(value)
        for key, value in row.items()
        if key is not None
    }


def _validate_required_fields(
    manifest: Path,
    row_number: int,
    row: dict[str, str],
) -> None:
    for column in REQUIRED_NONEMPTY_COLUMNS:
        value = row.get(column, "")
        if not value.strip():
            raise RegistrationUnitManifestError(
                f"{manifest}:{row_number}: required field is blank: {column}"
            )


def _validate_allowed_values(
    manifest: Path,
    row_number: int,
    row: dict[str, str],
) -> None:
    _validate_allowed(
        manifest,
        row_number,
        "manifest_schema_version",
        row["manifest_schema_version"],
        ALLOWED_MANIFEST_SCHEMA_VERSIONS,
    )
    _validate_allowed(
        manifest,
        row_number,
        "producer_family",
        row["producer_family"],
        ALLOWED_PRODUCER_FAMILIES,
    )
    _validate_allowed(
        manifest,
        row_number,
        "validation_layer",
        row["validation_layer"],
        ALLOWED_VALIDATION_LAYERS,
    )
    _validate_allowed(
        manifest,
        row_number,
        "source_role",
        row["source_role"],
        ALLOWED_SOURCE_ROLES,
    )
    _validate_allowed(
        manifest,
        row_number,
        "registration_backend",
        row["registration_backend"],
        ALLOWED_REGISTRATION_BACKENDS,
    )
    _validate_allowed(
        manifest,
        row_number,
        "expected_read_mode",
        row["expected_read_mode"],
        ALLOWED_READ_MODES,
    )


def _validate_allowed(
    manifest: Path,
    row_number: int,
    field_name: str,
    value: str,
    allowed_values: Iterable[str],
) -> None:
    value_clean = value.strip()
    allowed = set(allowed_values)
    if value_clean not in allowed:
        raise RegistrationUnitManifestError(
            f"{manifest}:{row_number}: unsupported {field_name}: "
            f"{value_clean!r}; allowed={sorted(allowed)}"
        )


def _resolve_registration_unit_path(
    declared_path: str,
    *,
    repo_root: Path,
) -> Path:
    path = Path(declared_path)
    if path.is_absolute():
        return path.resolve(strict=False)
    return (repo_root / path).resolve(strict=False)


def _resolve_sqlite_path(
    declared_sqlite_path: str,
    *,
    registration_unit_path_resolved: Path,
) -> Path:
    path = Path(declared_sqlite_path)
    if path.is_absolute():
        return path.resolve(strict=False)
    return (registration_unit_path_resolved / path).resolve(strict=False)


def _validate_filesystem_paths(
    *,
    manifest: Path,
    row_number: int,
    registration_unit_path: Path,
    sqlite_path: Path,
) -> None:
    if not registration_unit_path.exists():
        raise RegistrationUnitManifestError(
            f"{manifest}:{row_number}: registration_unit_path does not exist: "
            f"{registration_unit_path}"
        )

    if not registration_unit_path.is_dir():
        raise RegistrationUnitManifestError(
            f"{manifest}:{row_number}: registration_unit_path is not a directory: "
            f"{registration_unit_path}"
        )

    if not sqlite_path.exists():
        raise RegistrationUnitManifestError(
            f"{manifest}:{row_number}: sqlite_path does not exist: {sqlite_path}"
        )

    if not sqlite_path.is_file():
        raise RegistrationUnitManifestError(
            f"{manifest}:{row_number}: sqlite_path is not a file: {sqlite_path}"
        )
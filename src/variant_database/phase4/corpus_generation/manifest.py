"""Corpus Generation selection manifest loading.

This module implements the Phase 4.2 selection-manifest loader.

The loader is intentionally narrow:
- read a declared selection manifest
- validate row-level declaration shape
- preserve row order
- resolve paths
- optionally check filesystem existence

It does not open SQLite, inspect Registration Units, emit Corpus Generation
artifacts, or derive downstream evidence structures.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class CorpusGenerationManifestError(ValueError):
    """Raised when a Corpus Generation selection manifest is invalid."""


CANONICAL_SELECTION_MANIFEST_COLUMNS: tuple[str, ...] = (
    "corpus_generation_id",
    "registration_unit_label",
    "registration_unit_reference",
    "registration_unit_path",
    "registration_unit_sqlite_path",
    "expected_registration_unit_id",
    "expected_producer_family",
    "expected_registration_unit_validation_status",
    "expected_registration_unit_certification_status",
    "expected_registration_unit_readiness_status",
    "expected_backend",
    "registration_unit_inventory_record_reference",
    "registration_unit_readiness_record_reference",
    "phase4_1_validation_receipt_reference",
    "inclusion_status",
    "inclusion_rationale",
    "exclusion_status",
    "exclusion_rationale",
    "notes",
)

REQUIRED_SELECTION_MANIFEST_COLUMNS: frozenset[str] = frozenset(
    {
        "corpus_generation_id",
        "registration_unit_label",
        "registration_unit_path",
        "registration_unit_sqlite_path",
        "expected_backend",
        "inclusion_status",
        "inclusion_rationale",
        "exclusion_status",
        "exclusion_rationale",
    }
)

ALLOWED_INCLUSION_STATUSES: frozenset[str] = frozenset(
    {
        "included",
        "included_with_note",
        "included_for_fixture",
        "included_for_failure_mode",
    }
)

ALLOWED_EXCLUSION_STATUSES: frozenset[str] = frozenset(
    {
        "excluded",
        "excluded_uncertified",
        "excluded_failed_validation",
        "excluded_out_of_scope",
        "excluded_duplicate",
        "excluded_superseded",
        "excluded_missing",
        "excluded_unreadable",
        "deferred",
        "not_evaluated",
    }
)


@dataclass(frozen=True)
class CorpusGenerationSelectionManifestRecord:
    """One row from a Corpus Generation selection manifest."""

    source_row_number: int
    corpus_generation_id: str
    registration_unit_label: str
    registration_unit_reference: str
    registration_unit_path: str
    registration_unit_sqlite_path: str
    expected_registration_unit_id: str
    expected_producer_family: str
    expected_registration_unit_validation_status: str
    expected_registration_unit_certification_status: str
    expected_registration_unit_readiness_status: str
    expected_backend: str
    registration_unit_inventory_record_reference: str
    registration_unit_readiness_record_reference: str
    phase4_1_validation_receipt_reference: str
    inclusion_status: str
    inclusion_rationale: str
    exclusion_status: str
    exclusion_rationale: str
    notes: str
    registration_unit_path_resolved: Path | None
    registration_unit_sqlite_path_resolved: Path | None

    @property
    def is_included(self) -> bool:
        """Whether this row declares an included Registration Unit."""

        return bool(self.inclusion_status)

    @property
    def is_excluded_or_deferred(self) -> bool:
        """Whether this row declares an excluded or deferred candidate."""

        return bool(self.exclusion_status)


@dataclass(frozen=True)
class CorpusGenerationSelectionManifest:
    """Loaded Corpus Generation selection manifest."""

    manifest_path: Path
    corpus_generation_id: str
    records: tuple[CorpusGenerationSelectionManifestRecord, ...]

    @property
    def included_records(self) -> tuple[CorpusGenerationSelectionManifestRecord, ...]:
        """Rows declaring included Registration Units."""

        return tuple(record for record in self.records if record.is_included)

    @property
    def excluded_records(self) -> tuple[CorpusGenerationSelectionManifestRecord, ...]:
        """Rows declaring excluded or deferred candidates."""

        return tuple(record for record in self.records if record.is_excluded_or_deferred)


def load_corpus_generation_selection_manifest(
    manifest_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    validate_filesystem: bool = False,
) -> CorpusGenerationSelectionManifest:
    """Load and validate a Corpus Generation selection manifest TSV.

    Parameters
    ----------
    manifest_path:
        Path to a TSV selection manifest.
    repo_root:
        Optional base directory for resolving relative Registration Unit paths.
    validate_filesystem:
        When true, require included Registration Unit directories and SQLite
        files to exist. This check does not open SQLite.
    """

    manifest = Path(manifest_path)
    if not manifest.is_file():
        raise CorpusGenerationManifestError(
            f"Selection manifest does not exist or is not a file: {manifest}"
        )

    if manifest.suffix.lower() != ".tsv":
        raise CorpusGenerationManifestError(
            f"Selection manifest must be a .tsv file: {manifest}"
        )

    root = Path(repo_root) if repo_root is not None else manifest.parent

    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _validate_header(reader.fieldnames)
        records = tuple(
            _record_from_row(
                row=row,
                source_row_number=index,
                repo_root=root,
                validate_filesystem=validate_filesystem,
            )
            for index, row in enumerate(reader, start=2)
            if _row_has_content(row)
        )

    if not records:
        raise CorpusGenerationManifestError(
            f"Selection manifest contains no records: {manifest}"
        )

    corpus_generation_ids = {record.corpus_generation_id for record in records}
    if len(corpus_generation_ids) != 1:
        observed = ", ".join(sorted(corpus_generation_ids))
        raise CorpusGenerationManifestError(
            "Selection manifest must contain exactly one corpus_generation_id; "
            f"observed: {observed}"
        )

    _validate_no_duplicate_included_labels(records)
    _validate_no_duplicate_included_sqlite_paths(records)

    return CorpusGenerationSelectionManifest(
        manifest_path=manifest,
        corpus_generation_id=records[0].corpus_generation_id,
        records=records,
    )


def _validate_header(fieldnames: list[str] | None) -> None:
    if not fieldnames:
        raise CorpusGenerationManifestError("Selection manifest is missing a header row.")

    raw = tuple(field for field in fieldnames if field is not None)
    normalized = tuple(field.strip() for field in raw)

    if raw != normalized:
        raise CorpusGenerationManifestError(
            "Selection manifest column names must not contain leading or trailing whitespace."
        )

    if any(not field for field in normalized):
        raise CorpusGenerationManifestError(
            "Selection manifest contains an empty column name."
        )

    duplicates = sorted(
        field for field in set(normalized) if normalized.count(field) > 1
    )
    if duplicates:
        raise CorpusGenerationManifestError(
            "Selection manifest contains duplicate columns: " + ", ".join(duplicates)
        )

    observed = set(normalized)
    allowed = set(CANONICAL_SELECTION_MANIFEST_COLUMNS)
    required = set(REQUIRED_SELECTION_MANIFEST_COLUMNS)

    unknown = sorted(observed - allowed)
    if unknown:
        raise CorpusGenerationManifestError(
            "Selection manifest contains unknown columns: " + ", ".join(unknown)
        )

    missing = sorted(required - observed)
    if missing:
        raise CorpusGenerationManifestError(
            "Selection manifest is missing required columns: " + ", ".join(missing)
        )


def _row_has_content(row: dict[str, str | None]) -> bool:
    return any(_clean(value) for value in row.values())


def _record_from_row(
    *,
    row: dict[str, str | None],
    source_row_number: int,
    repo_root: Path,
    validate_filesystem: bool,
) -> CorpusGenerationSelectionManifestRecord:
    values = {
        column: _clean(row.get(column))
        for column in CANONICAL_SELECTION_MANIFEST_COLUMNS
    }

    for field in ("corpus_generation_id", "registration_unit_label"):
        if not values[field]:
            raise CorpusGenerationManifestError(
                f"Row {source_row_number} is missing required value: {field}"
            )

    inclusion_status = values["inclusion_status"]
    exclusion_status = values["exclusion_status"]
    has_inclusion = bool(inclusion_status)
    has_exclusion = bool(exclusion_status)

    if has_inclusion == has_exclusion:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} must declare exactly one disposition family: "
            "included or excluded/deferred."
        )

    if has_inclusion:
        _validate_included_row(
            values=values,
            source_row_number=source_row_number,
            repo_root=repo_root,
            validate_filesystem=validate_filesystem,
        )
    else:
        _validate_excluded_row(
            values=values,
            source_row_number=source_row_number,
        )

    return CorpusGenerationSelectionManifestRecord(
        source_row_number=source_row_number,
        corpus_generation_id=values["corpus_generation_id"],
        registration_unit_label=values["registration_unit_label"],
        registration_unit_reference=values["registration_unit_reference"],
        registration_unit_path=values["registration_unit_path"],
        registration_unit_sqlite_path=values["registration_unit_sqlite_path"],
        expected_registration_unit_id=values["expected_registration_unit_id"],
        expected_producer_family=values["expected_producer_family"],
        expected_registration_unit_validation_status=values[
            "expected_registration_unit_validation_status"
        ],
        expected_registration_unit_certification_status=values[
            "expected_registration_unit_certification_status"
        ],
        expected_registration_unit_readiness_status=values[
            "expected_registration_unit_readiness_status"
        ],
        expected_backend=values["expected_backend"],
        registration_unit_inventory_record_reference=values[
            "registration_unit_inventory_record_reference"
        ],
        registration_unit_readiness_record_reference=values[
            "registration_unit_readiness_record_reference"
        ],
        phase4_1_validation_receipt_reference=values[
            "phase4_1_validation_receipt_reference"
        ],
        inclusion_status=inclusion_status,
        inclusion_rationale=values["inclusion_rationale"],
        exclusion_status=exclusion_status,
        exclusion_rationale=values["exclusion_rationale"],
        notes=values["notes"],
        registration_unit_path_resolved=_resolve_optional_path(
            values["registration_unit_path"], repo_root
        ),
        registration_unit_sqlite_path_resolved=_resolve_optional_path(
            values["registration_unit_sqlite_path"], repo_root
        ),
    )


def _validate_included_row(
    *,
    values: dict[str, str],
    source_row_number: int,
    repo_root: Path,
    validate_filesystem: bool,
) -> None:
    inclusion_status = values["inclusion_status"]
    if inclusion_status not in ALLOWED_INCLUSION_STATUSES:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} has invalid inclusion_status: {inclusion_status}"
        )

    if not values["inclusion_rationale"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} requires inclusion_rationale."
        )

    if values["exclusion_rationale"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} must not declare exclusion_rationale "
            "for an included row."
        )

    if not values["registration_unit_path"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} requires registration_unit_path for included rows."
        )

    if not values["expected_backend"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} requires expected_backend for included rows."
        )

    backend = values["expected_backend"].lower()
    has_sqlite_path = bool(values["registration_unit_sqlite_path"])

    if backend == "sqlite" or has_sqlite_path:
        if not values["registration_unit_sqlite_path"]:
            raise CorpusGenerationManifestError(
                f"Row {source_row_number} requires registration_unit_sqlite_path "
                "for sqlite-backed included rows."
            )

    if validate_filesystem:
        registration_unit_path = _resolve_optional_path(
            values["registration_unit_path"], repo_root
        )
        registration_unit_sqlite_path = _resolve_optional_path(
            values["registration_unit_sqlite_path"], repo_root
        )

        if registration_unit_path is None or not registration_unit_path.is_dir():
            raise CorpusGenerationManifestError(
                f"Row {source_row_number} registration_unit_path is not a directory: "
                f"{values['registration_unit_path']}"
            )

        if backend == "sqlite" or has_sqlite_path:
            if (
                registration_unit_sqlite_path is None
                or not registration_unit_sqlite_path.is_file()
            ):
                raise CorpusGenerationManifestError(
                    f"Row {source_row_number} registration_unit_sqlite_path is not a file: "
                    f"{values['registration_unit_sqlite_path']}"
                )


def _validate_excluded_row(
    *,
    values: dict[str, str],
    source_row_number: int,
) -> None:
    exclusion_status = values["exclusion_status"]
    if exclusion_status not in ALLOWED_EXCLUSION_STATUSES:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} has invalid exclusion_status: {exclusion_status}"
        )

    if not values["exclusion_rationale"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} requires exclusion_rationale."
        )

    if values["inclusion_rationale"]:
        raise CorpusGenerationManifestError(
            f"Row {source_row_number} must not declare inclusion_rationale "
            "for an excluded/deferred row."
        )


def _validate_no_duplicate_included_labels(
    records: Iterable[CorpusGenerationSelectionManifestRecord],
) -> None:
    seen: dict[str, int] = {}
    for record in records:
        if not record.is_included:
            continue

        label = record.registration_unit_label
        if label in seen:
            raise CorpusGenerationManifestError(
                "Duplicate included registration_unit_label: "
                f"{label} in rows {seen[label]} and {record.source_row_number}"
            )

        seen[label] = record.source_row_number


def _validate_no_duplicate_included_sqlite_paths(
    records: Iterable[CorpusGenerationSelectionManifestRecord],
) -> None:
    seen: dict[str, int] = {}
    for record in records:
        if not record.is_included or not record.registration_unit_sqlite_path:
            continue

        path_key = str(record.registration_unit_sqlite_path_resolved)
        if path_key in seen:
            raise CorpusGenerationManifestError(
                "Duplicate included registration_unit_sqlite_path: "
                f"{record.registration_unit_sqlite_path} in rows "
                f"{seen[path_key]} and {record.source_row_number}"
            )

        seen[path_key] = record.source_row_number


def _resolve_optional_path(raw_path: str, repo_root: Path) -> Path | None:
    if not raw_path:
        return None

    path = Path(raw_path)
    if not path.is_absolute():
        path = repo_root / path

    return path.resolve(strict=False)


def _clean(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip()

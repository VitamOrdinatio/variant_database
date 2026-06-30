"""
Phase 4 Registration Unit validation orchestration.

This module runs the Phase 4.1 Registration Unit validation chain:

    manifest -> inspection -> inventory -> readiness -> validation summary

It may:
    - load a Registration Unit input manifest
    - inspect declared Registration Units read-only
    - emit deterministic inventory artifacts
    - emit deterministic readiness artifacts
    - emit a validation run summary
    - verify source SQLite files were not mutated

It must not:
    - mutate Registration Units
    - create SQLite sidecars
    - certify biological evidence
    - replace MARK full-corpus smoketesting

Operating rule:
    Declare. Inspect read-only. Emit deterministic artifacts. Verify no mutation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from variant_database.phase4.registration_units.inventory import (
    RegistrationUnitInventoryArtifactSet,
    build_registration_unit_inventory_rows,
    emit_registration_unit_inventory_artifacts,
)
from variant_database.phase4.registration_units.inspection import (
    RegistrationUnitInspectionResult,
    inspect_registration_units,
)
from variant_database.phase4.registration_units.manifest import (
    RegistrationUnitManifestRecord,
    load_registration_unit_manifest,
)
from variant_database.phase4.registration_units.readiness import (
    RegistrationUnitReadinessArtifactSet,
    emit_registration_unit_readiness_artifacts,
)


VALIDATION_RUN_SCHEMA_VERSION = "phase4_registration_unit_validation_run_v1"
VALIDATION_RUN_SUMMARY_JSON_FILENAME = "registration_unit_validation_run_summary.json"


class RegistrationUnitValidationError(RuntimeError):
    """Raised when Phase 4 Registration Unit validation cannot complete."""


@dataclass(frozen=True)
class SQLiteFileFingerprint:
    """Filesystem fingerprint for non-mutation validation."""

    registration_unit_id: str
    registration_unit_label: str
    sqlite_path: str
    exists: bool
    size_bytes: int | None
    mtime_ns: int | None
    sidecars: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "sqlite_path": self.sqlite_path,
            "exists": self.exists,
            "size_bytes": self.size_bytes,
            "mtime_ns": self.mtime_ns,
            "sidecars": list(self.sidecars),
        }


@dataclass(frozen=True)
class RegistrationUnitValidationRunResult:
    """Summary of one Phase 4.1 Registration Unit validation run."""

    manifest_path: Path
    output_dir: Path
    validation_run_summary_json_path: Path

    record_count: int
    inspection_count: int
    inventory_row_count: int
    readiness_row_count: int
    ready_count: int
    not_ready_count: int

    inspection_status: str
    inventory_artifact_status: str
    readiness_artifact_status: str
    non_mutation_status: str
    sidecar_status: str
    validation_status: str

    inventory_artifacts: RegistrationUnitInventoryArtifactSet
    readiness_artifacts: RegistrationUnitReadinessArtifactSet


def validate_registration_units_from_manifest(
    manifest_path: str | Path,
    output_dir: str | Path,
    *,
    repo_root: str | Path | None = None,
) -> RegistrationUnitValidationRunResult:
    """
    Run the Phase 4.1 Registration Unit validation chain.

    The function writes deterministic artifacts only to output_dir. It validates
    that declared SQLite files are not modified during the validation run.
    """
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    records = load_registration_unit_manifest(
        manifest_path,
        repo_root=repo_root,
        validate_filesystem=True,
    )

    before = _fingerprints_by_registration_unit_id(records)

    inspection_results = inspect_registration_units(records)
    inspection_status = _aggregate_inspection_status(inspection_results)

    inventory_artifacts = emit_registration_unit_inventory_artifacts(
        inspection_results,
        destination,
    )
    inventory_rows = build_registration_unit_inventory_rows(inspection_results)

    readiness_artifacts = emit_registration_unit_readiness_artifacts(
        inventory_rows,
        destination,
    )

    after = _fingerprints_by_registration_unit_id(records)

    mutation_details = _mutation_details(before, after)
    sidecar_details = _sidecar_details(before, after)

    non_mutation_status = "passed" if not mutation_details else "failed"
    sidecar_status = "passed" if not sidecar_details else "failed"

    validation_status = (
        "passed"
        if (
            inspection_status == "passed"
            and inventory_artifacts.artifact_status == "passed"
            and readiness_artifacts.artifact_status == "passed"
            and non_mutation_status == "passed"
            and sidecar_status == "passed"
        )
        else "failed"
    )

    summary_path = destination / VALIDATION_RUN_SUMMARY_JSON_FILENAME

    result = RegistrationUnitValidationRunResult(
        manifest_path=Path(manifest_path),
        output_dir=destination,
        validation_run_summary_json_path=summary_path,
        record_count=len(records),
        inspection_count=len(inspection_results),
        inventory_row_count=inventory_artifacts.row_count,
        readiness_row_count=readiness_artifacts.row_count,
        ready_count=readiness_artifacts.ready_count,
        not_ready_count=readiness_artifacts.not_ready_count,
        inspection_status=inspection_status,
        inventory_artifact_status=inventory_artifacts.artifact_status,
        readiness_artifact_status=readiness_artifacts.artifact_status,
        non_mutation_status=non_mutation_status,
        sidecar_status=sidecar_status,
        validation_status=validation_status,
        inventory_artifacts=inventory_artifacts,
        readiness_artifacts=readiness_artifacts,
    )

    _write_validation_run_summary_json(
        path=summary_path,
        result=result,
        before=before,
        after=after,
        mutation_details=mutation_details,
        sidecar_details=sidecar_details,
    )

    return result


def _aggregate_inspection_status(
    inspection_results: list[RegistrationUnitInspectionResult],
) -> str:
    if not inspection_results:
        return "failed"

    if all(result.inspection_status == "passed" for result in inspection_results):
        return "passed"

    return "failed"


def _fingerprints_by_registration_unit_id(
    records: list[RegistrationUnitManifestRecord],
) -> dict[str, SQLiteFileFingerprint]:
    return {
        record.registration_unit_id: _fingerprint_for_record(record)
        for record in records
    }


def _fingerprint_for_record(
    record: RegistrationUnitManifestRecord,
) -> SQLiteFileFingerprint:
    sqlite_path = record.sqlite_path_resolved

    exists = sqlite_path.exists()
    size_bytes: int | None = None
    mtime_ns: int | None = None

    if exists:
        stat = sqlite_path.stat()
        size_bytes = stat.st_size
        mtime_ns = stat.st_mtime_ns

    return SQLiteFileFingerprint(
        registration_unit_id=record.registration_unit_id,
        registration_unit_label=record.registration_unit_label,
        sqlite_path=str(sqlite_path),
        exists=exists,
        size_bytes=size_bytes,
        mtime_ns=mtime_ns,
        sidecars=_sqlite_sidecars(sqlite_path),
    )


def _sqlite_sidecars(sqlite_path: Path) -> tuple[str, ...]:
    candidates = [
        sqlite_path.parent / f"{sqlite_path.name}-wal",
        sqlite_path.parent / f"{sqlite_path.name}-shm",
        sqlite_path.parent / f"{sqlite_path.name}-journal",
    ]

    return tuple(sorted(str(path) for path in candidates if path.exists()))


def _mutation_details(
    before: dict[str, SQLiteFileFingerprint],
    after: dict[str, SQLiteFileFingerprint],
) -> list[dict[str, object]]:
    details: list[dict[str, object]] = []

    for registration_unit_id in sorted(before):
        before_state = before[registration_unit_id]
        after_state = after.get(registration_unit_id)

        if after_state is None:
            details.append(
                {
                    "registration_unit_id": registration_unit_id,
                    "mutation_reason": "missing_after_state",
                }
            )
            continue

        reasons: list[str] = []

        if before_state.exists != after_state.exists:
            reasons.append("exists_changed")

        if before_state.size_bytes != after_state.size_bytes:
            reasons.append("size_bytes_changed")

        if before_state.mtime_ns != after_state.mtime_ns:
            reasons.append("mtime_ns_changed")

        if before_state.sidecars != after_state.sidecars:
            reasons.append("sidecars_changed")

        if reasons:
            details.append(
                {
                    "registration_unit_id": registration_unit_id,
                    "registration_unit_label": before_state.registration_unit_label,
                    "sqlite_path": before_state.sqlite_path,
                    "mutation_reason": ";".join(reasons),
                    "before": before_state.as_dict(),
                    "after": after_state.as_dict(),
                }
            )

    return details


def _sidecar_details(
    before: dict[str, SQLiteFileFingerprint],
    after: dict[str, SQLiteFileFingerprint],
) -> list[dict[str, object]]:
    details: list[dict[str, object]] = []

    for registration_unit_id in sorted(before):
        before_state = before[registration_unit_id]
        after_state = after.get(registration_unit_id)

        if after_state is None:
            continue

        if before_state.sidecars != after_state.sidecars:
            details.append(
                {
                    "registration_unit_id": registration_unit_id,
                    "registration_unit_label": before_state.registration_unit_label,
                    "sqlite_path": before_state.sqlite_path,
                    "before_sidecars": list(before_state.sidecars),
                    "after_sidecars": list(after_state.sidecars),
                }
            )

    return details


def _write_validation_run_summary_json(
    *,
    path: Path,
    result: RegistrationUnitValidationRunResult,
    before: dict[str, SQLiteFileFingerprint],
    after: dict[str, SQLiteFileFingerprint],
    mutation_details: list[dict[str, object]],
    sidecar_details: list[dict[str, object]],
) -> None:
    payload = {
        "validation_run_schema_version": VALIDATION_RUN_SCHEMA_VERSION,
        "validation_status": result.validation_status,
        "manifest_path": str(result.manifest_path),
        "output_dir": str(result.output_dir),
        "record_count": result.record_count,
        "inspection": {
            "inspection_count": result.inspection_count,
            "inspection_status": result.inspection_status,
        },
        "inventory": {
            "artifact_status": result.inventory_artifact_status,
            "row_count": result.inventory_row_count,
            "tsv_path": str(result.inventory_artifacts.tsv_path),
            "json_path": str(result.inventory_artifacts.json_path),
        },
        "readiness": {
            "artifact_status": result.readiness_artifact_status,
            "row_count": result.readiness_row_count,
            "ready_count": result.ready_count,
            "not_ready_count": result.not_ready_count,
            "readiness_tsv_path": str(result.readiness_artifacts.readiness_tsv_path),
            "readiness_json_path": str(result.readiness_artifacts.readiness_json_path),
            "validation_summary_json_path": str(
                result.readiness_artifacts.validation_summary_json_path
            ),
        },
        "non_mutation": {
            "non_mutation_status": result.non_mutation_status,
            "sidecar_status": result.sidecar_status,
            "mutation_details": mutation_details,
            "sidecar_details": sidecar_details,
            "before": {
                key: value.as_dict()
                for key, value in sorted(before.items())
            },
            "after": {
                key: value.as_dict()
                for key, value in sorted(after.items())
            },
        },
        "authority_boundary": (
            "This validation run proves Phase 4.1 Registration Unit declaration, "
            "read-only inspection, inventory emission, readiness evaluation, and "
            "non-mutation behavior against the declared input manifest. It does not "
            "certify biological evidence, does not construct Corpus Generations, and "
            "does not replace full Phase 4 certification."
        ),
    }

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

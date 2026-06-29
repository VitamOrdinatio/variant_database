from __future__ import annotations

import json
from pathlib import Path

from variant_database.phase4.registration_units.inventory import (
    INVENTORY_JSON_FILENAME,
    INVENTORY_TSV_FILENAME,
)
from variant_database.phase4.registration_units.manifest import (
    load_registration_unit_manifest,
)
from variant_database.phase4.registration_units.readiness import (
    READINESS_JSON_FILENAME,
    READINESS_TSV_FILENAME,
    VALIDATION_SUMMARY_JSON_FILENAME,
)
from variant_database.phase4.registration_units.validation import (
    VALIDATION_RUN_SCHEMA_VERSION,
    VALIDATION_RUN_SUMMARY_JSON_FILENAME,
    validate_registration_units_from_manifest,
)


FIXTURE_MANIFEST = Path(
    "tests/fixtures/phase4/"
    "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
    "phase4_registration_unit_golden_fixture/"
    "manifests/registration_unit_input_manifest.tsv"
)


def test_registration_unit_validation_run_passes_for_fixture_manifest(
    tmp_path: Path,
) -> None:
    result = validate_registration_units_from_manifest(
        FIXTURE_MANIFEST,
        tmp_path,
        repo_root=Path.cwd(),
    )

    assert result.validation_status == "passed"
    assert result.record_count == 6
    assert result.inspection_count == 6
    assert result.inventory_row_count == 6
    assert result.readiness_row_count == 6
    assert result.ready_count == 6
    assert result.not_ready_count == 0
    assert result.inspection_status == "passed"
    assert result.inventory_artifact_status == "passed"
    assert result.readiness_artifact_status == "passed"
    assert result.non_mutation_status == "passed"
    assert result.sidecar_status == "passed"


def test_registration_unit_validation_run_emits_expected_artifacts(
    tmp_path: Path,
) -> None:
    result = validate_registration_units_from_manifest(
        FIXTURE_MANIFEST,
        tmp_path,
        repo_root=Path.cwd(),
    )

    expected_paths = {
        tmp_path / INVENTORY_TSV_FILENAME,
        tmp_path / INVENTORY_JSON_FILENAME,
        tmp_path / READINESS_TSV_FILENAME,
        tmp_path / READINESS_JSON_FILENAME,
        tmp_path / VALIDATION_SUMMARY_JSON_FILENAME,
        tmp_path / VALIDATION_RUN_SUMMARY_JSON_FILENAME,
    }

    assert result.validation_run_summary_json_path == (
        tmp_path / VALIDATION_RUN_SUMMARY_JSON_FILENAME
    )

    for path in expected_paths:
        assert path.is_file(), path


def test_registration_unit_validation_run_summary_schema_is_stable(
    tmp_path: Path,
) -> None:
    result = validate_registration_units_from_manifest(
        FIXTURE_MANIFEST,
        tmp_path,
        repo_root=Path.cwd(),
    )

    payload = json.loads(
        result.validation_run_summary_json_path.read_text(encoding="utf-8")
    )

    assert payload["validation_run_schema_version"] == VALIDATION_RUN_SCHEMA_VERSION
    assert payload["validation_status"] == "passed"
    assert payload["record_count"] == 6

    assert payload["inspection"] == {
        "inspection_count": 6,
        "inspection_status": "passed",
    }

    assert payload["inventory"]["artifact_status"] == "passed"
    assert payload["inventory"]["row_count"] == 6

    assert payload["readiness"]["artifact_status"] == "passed"
    assert payload["readiness"]["row_count"] == 6
    assert payload["readiness"]["ready_count"] == 6
    assert payload["readiness"]["not_ready_count"] == 0

    assert payload["non_mutation"]["non_mutation_status"] == "passed"
    assert payload["non_mutation"]["sidecar_status"] == "passed"
    assert payload["non_mutation"]["mutation_details"] == []
    assert payload["non_mutation"]["sidecar_details"] == []


def test_registration_unit_validation_run_does_not_mutate_sqlite_files(
    tmp_path: Path,
) -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    before = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    validate_registration_units_from_manifest(
        FIXTURE_MANIFEST,
        tmp_path,
        repo_root=Path.cwd(),
    )

    after = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    assert before == after


def test_registration_unit_validation_run_does_not_create_sqlite_sidecars(
    tmp_path: Path,
) -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    before = _sqlite_sidecars(records)

    validate_registration_units_from_manifest(
        FIXTURE_MANIFEST,
        tmp_path,
        repo_root=Path.cwd(),
    )

    after = _sqlite_sidecars(records)

    assert before == after


def _sqlite_sidecars(records) -> set[Path]:
    sidecars: set[Path] = set()

    for record in records:
        sqlite_path = record.sqlite_path_resolved

        for suffix in ["-wal", "-shm", "-journal"]:
            candidate = sqlite_path.parent / f"{sqlite_path.name}{suffix}"
            if candidate.exists():
                sidecars.add(candidate)

    return sidecars

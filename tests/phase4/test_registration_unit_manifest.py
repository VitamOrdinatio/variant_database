from __future__ import annotations

import csv
from pathlib import Path

import pytest

from vdb.phase4.registration_units.manifest import (
    RegistrationUnitManifestError,
    load_registration_unit_manifest,
)


FIXTURE_MANIFEST = Path(
    "tests/fixtures/phase4/"
    "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
    "phase4_registration_unit_golden_fixture/"
    "manifests/registration_unit_input_manifest.tsv"
)

EXPECTED_LABELS = {
    "gsc_epilepsy",
    "gsc_mitochondrial_disease",
    "vap_hg002",
    "vap_median_ERR10619300",
    "vap_q1_ERR10619212",
    "vap_q3_ERR10619225",
}


def test_registration_unit_fixture_manifest_loads_six_records() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    assert len(records) == 6
    assert {record.registration_unit_label for record in records} == EXPECTED_LABELS
    assert {record.validation_layer for record in records} == {
        "validation_layer_2_lightweight_fixture"
    }
    assert {record.source_role for record in records} == {"phase4_golden_fixture"}


def test_registration_unit_fixture_manifest_resolves_sqlite_paths() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    for record in records:
        assert record.registration_backend == "sqlite"
        assert record.expected_read_mode == "read_only"
        assert record.registration_unit_path_resolved.is_dir()
        assert record.sqlite_path_resolved.is_file()
        assert record.sqlite_path_resolved.name == "vdb.sqlite"
        assert record.path_resolution_status == "resolved"
        assert record.declaration_status == "valid"


def test_registration_unit_manifest_loading_does_not_mutate_sqlite_files() -> None:
    before = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in load_registration_unit_manifest(
            FIXTURE_MANIFEST,
            repo_root=Path.cwd(),
            validate_filesystem=True,
        )
    }

    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    after = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    assert before == after


def test_registration_unit_manifest_rejects_duplicate_registration_unit_id(
    tmp_path: Path,
) -> None:
    duplicate_manifest = tmp_path / "duplicate_registration_unit_id.tsv"
    rows = _read_manifest_dicts(FIXTURE_MANIFEST)

    rows[1]["registration_unit_id"] = rows[0]["registration_unit_id"]
    _write_manifest(duplicate_manifest, rows)

    with pytest.raises(RegistrationUnitManifestError, match="duplicate registration_unit_id"):
        load_registration_unit_manifest(
            duplicate_manifest,
            repo_root=Path.cwd(),
            validate_filesystem=False,
        )


def test_registration_unit_manifest_rejects_invalid_read_mode(
    tmp_path: Path,
) -> None:
    invalid_manifest = tmp_path / "invalid_read_mode.tsv"
    rows = _read_manifest_dicts(FIXTURE_MANIFEST)

    rows[0]["expected_read_mode"] = "read_write"
    _write_manifest(invalid_manifest, rows)

    with pytest.raises(RegistrationUnitManifestError, match="unsupported expected_read_mode"):
        load_registration_unit_manifest(
            invalid_manifest,
            repo_root=Path.cwd(),
            validate_filesystem=False,
        )


def test_registration_unit_manifest_rejects_missing_sqlite_when_filesystem_validation_enabled(
    tmp_path: Path,
) -> None:
    invalid_manifest = tmp_path / "missing_sqlite.tsv"
    rows = _read_manifest_dicts(FIXTURE_MANIFEST)

    rows[0]["registration_unit_path"] = str(tmp_path)
    rows[0]["sqlite_path"] = "missing.sqlite"
    _write_manifest(invalid_manifest, rows)

    with pytest.raises(RegistrationUnitManifestError, match="sqlite_path does not exist"):
        load_registration_unit_manifest(
            invalid_manifest,
            repo_root=Path.cwd(),
            validate_filesystem=True,
        )


def _read_manifest_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [dict(row) for row in reader]


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    assert rows
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
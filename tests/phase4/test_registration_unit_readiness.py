from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path

import pytest

from variant_database.phase4.registration_units.inspection import (
    inspect_registration_units,
)
from variant_database.phase4.registration_units.inventory import (
    build_registration_unit_inventory_rows,
)
from variant_database.phase4.registration_units.manifest import (
    load_registration_unit_manifest,
)
from variant_database.phase4.registration_units.readiness import (
    READINESS_COLUMNS,
    READINESS_JSON_FILENAME,
    READINESS_SCHEMA_VERSION,
    READINESS_TSV_FILENAME,
    VALIDATION_SUMMARY_JSON_FILENAME,
    RegistrationUnitReadinessError,
    build_registration_unit_readiness_rows,
    emit_registration_unit_readiness_artifacts,
)


FIXTURE_MANIFEST = Path(
    "tests/fixtures/phase4/"
    "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
    "phase4_registration_unit_golden_fixture/"
    "manifests/registration_unit_input_manifest.tsv"
)


def test_registration_unit_readiness_rows_are_built_from_inventory_rows() -> None:
    readiness_rows = build_registration_unit_readiness_rows(_inventory_rows())

    assert len(readiness_rows) == 6
    assert {row.readiness_schema_version for row in readiness_rows} == {
        READINESS_SCHEMA_VERSION
    }
    assert {row.readiness_status for row in readiness_rows} == {"ready"}
    assert {row.readiness_reasons for row in readiness_rows} == {"passed"}


def test_registration_unit_readiness_rows_are_sorted_deterministically() -> None:
    readiness_rows = build_registration_unit_readiness_rows(
        list(reversed(_inventory_rows()))
    )

    observed_ids = [row.registration_unit_id for row in readiness_rows]

    assert observed_ids == sorted(observed_ids)


def test_registration_unit_readiness_preserves_expected_fixture_counts() -> None:
    readiness_rows = build_registration_unit_readiness_rows(_inventory_rows())
    by_label = {row.registration_unit_label: row for row in readiness_rows}

    assert by_label["gsc_epilepsy"].source_identities_row_count == 273
    assert by_label["gsc_mitochondrial_disease"].source_identities_row_count == 254

    for label in [
        "vap_hg002",
        "vap_median_ERR10619300",
        "vap_q1_ERR10619212",
        "vap_q3_ERR10619225",
    ]:
        assert by_label[label].source_identities_row_count == 281


def test_registration_unit_readiness_artifacts_are_emitted(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_readiness_artifacts(
        _inventory_rows(),
        tmp_path,
    )

    assert artifact_set.artifact_status == "passed"
    assert artifact_set.row_count == 6
    assert artifact_set.ready_count == 6
    assert artifact_set.not_ready_count == 0
    assert artifact_set.readiness_tsv_path == tmp_path / READINESS_TSV_FILENAME
    assert artifact_set.readiness_json_path == tmp_path / READINESS_JSON_FILENAME
    assert (
        artifact_set.validation_summary_json_path
        == tmp_path / VALIDATION_SUMMARY_JSON_FILENAME
    )
    assert artifact_set.readiness_tsv_path.is_file()
    assert artifact_set.readiness_json_path.is_file()
    assert artifact_set.validation_summary_json_path.is_file()


def test_registration_unit_readiness_tsv_schema_is_stable(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_readiness_artifacts(
        _inventory_rows(),
        tmp_path,
    )

    with artifact_set.readiness_tsv_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        assert reader.fieldnames == READINESS_COLUMNS
        rows = list(reader)

    assert len(rows) == 6
    assert {row["readiness_schema_version"] for row in rows} == {
        READINESS_SCHEMA_VERSION
    }
    assert {row["readiness_status"] for row in rows} == {"ready"}


def test_registration_unit_readiness_json_schema_is_stable(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_readiness_artifacts(
        _inventory_rows(),
        tmp_path,
    )

    payload = json.loads(
        artifact_set.readiness_json_path.read_text(encoding="utf-8")
    )

    assert payload["readiness_schema_version"] == READINESS_SCHEMA_VERSION
    assert payload["row_count"] == 6
    assert payload["ready_count"] == 6
    assert payload["not_ready_count"] == 0
    assert len(payload["registration_units"]) == 6

    observed_ids = [
        row["registration_unit_id"]
        for row in payload["registration_units"]
    ]
    assert observed_ids == sorted(observed_ids)


def test_registration_unit_validation_summary_json_schema_is_stable(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_readiness_artifacts(
        _inventory_rows(),
        tmp_path,
    )

    payload = json.loads(
        artifact_set.validation_summary_json_path.read_text(encoding="utf-8")
    )

    assert payload["readiness_schema_version"] == READINESS_SCHEMA_VERSION
    assert payload["validation_status"] == "passed"
    assert payload["row_count"] == 6
    assert payload["ready_count"] == 6
    assert payload["not_ready_count"] == 0
    assert payload["not_ready_registration_units"] == []

    assert payload["validation_gates"] == {
        "registration_backend": "sqlite",
        "expected_read_mode": "read_only",
        "open_status": "passed",
        "query_only_status": "enabled",
        "required_table_status": "passed",
        "integrity_check_status": "ok",
        "inspection_status": "passed",
        "required_row_counts": "positive",
    }


def test_registration_unit_readiness_artifact_emission_is_deterministic(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    first = emit_registration_unit_readiness_artifacts(
        _inventory_rows(),
        first_dir,
    )
    second = emit_registration_unit_readiness_artifacts(
        list(reversed(_inventory_rows())),
        second_dir,
    )

    assert first.readiness_tsv_path.read_bytes() == second.readiness_tsv_path.read_bytes()
    assert first.readiness_json_path.read_bytes() == second.readiness_json_path.read_bytes()
    assert (
        first.validation_summary_json_path.read_bytes()
        == second.validation_summary_json_path.read_bytes()
    )


def test_registration_unit_readiness_rejects_empty_inventory_rows() -> None:
    with pytest.raises(RegistrationUnitReadinessError, match="zero inventory rows"):
        build_registration_unit_readiness_rows([])


def test_registration_unit_readiness_marks_failed_inventory_row_not_ready() -> None:
    inventory_rows = _inventory_rows()
    broken = replace(
        inventory_rows[0],
        query_only_status="disabled",
        inspection_status="failed",
    )

    readiness_rows = build_registration_unit_readiness_rows(
        [broken] + inventory_rows[1:]
    )

    by_id = {row.registration_unit_id: row for row in readiness_rows}
    broken_row = by_id[broken.registration_unit_id]

    assert broken_row.readiness_status == "not_ready"
    assert "query_only_status_not_enabled" in broken_row.readiness_reasons
    assert "inspection_status_not_passed" in broken_row.readiness_reasons


def test_registration_unit_readiness_artifact_emission_reports_not_ready_units(
    tmp_path: Path,
) -> None:
    inventory_rows = _inventory_rows()
    broken = replace(
        inventory_rows[0],
        integrity_check_status="failed",
    )

    artifact_set = emit_registration_unit_readiness_artifacts(
        [broken] + inventory_rows[1:],
        tmp_path,
    )

    assert artifact_set.artifact_status == "failed"
    assert artifact_set.ready_count == 5
    assert artifact_set.not_ready_count == 1

    payload = json.loads(
        artifact_set.validation_summary_json_path.read_text(encoding="utf-8")
    )

    assert payload["validation_status"] == "failed"
    assert payload["not_ready_count"] == 1
    assert len(payload["not_ready_registration_units"]) == 1
    assert (
        "integrity_check_status_not_ok"
        in payload["not_ready_registration_units"][0]["readiness_reasons"]
    )


def test_registration_unit_readiness_emission_does_not_mutate_sqlite_files(
    tmp_path: Path,
) -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )
    inspection_results = inspect_registration_units(records)
    inventory_rows = build_registration_unit_inventory_rows(inspection_results)

    before = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    emit_registration_unit_readiness_artifacts(
        inventory_rows,
        tmp_path,
    )

    after = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    assert before == after


def _inventory_rows():
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )
    inspection_results = inspect_registration_units(records)
    return build_registration_unit_inventory_rows(inspection_results)

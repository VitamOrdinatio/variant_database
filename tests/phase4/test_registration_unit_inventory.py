from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from variant_database.phase4.registration_units.inspection import (
    inspect_registration_units,
)
from variant_database.phase4.registration_units.inventory import (
    INVENTORY_COLUMNS,
    INVENTORY_JSON_FILENAME,
    INVENTORY_SCHEMA_VERSION,
    INVENTORY_TSV_FILENAME,
    RegistrationUnitInventoryError,
    build_registration_unit_inventory_rows,
    emit_registration_unit_inventory_artifacts,
)
from variant_database.phase4.registration_units.manifest import (
    load_registration_unit_manifest,
)


FIXTURE_MANIFEST = Path(
    "tests/fixtures/phase4/"
    "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
    "phase4_registration_unit_golden_fixture/"
    "manifests/registration_unit_input_manifest.tsv"
)


def test_registration_unit_inventory_rows_are_built_from_inspection_results() -> None:
    inspection_results = _inspection_results()

    rows = build_registration_unit_inventory_rows(inspection_results)

    assert len(rows) == 6
    assert {row.inventory_schema_version for row in rows} == {
        INVENTORY_SCHEMA_VERSION
    }
    assert {row.inspection_status for row in rows} == {"passed"}
    assert {row.query_only_status for row in rows} == {"enabled"}
    assert {row.required_table_status for row in rows} == {"passed"}
    assert {row.integrity_check_status for row in rows} == {"ok"}


def test_registration_unit_inventory_rows_are_sorted_deterministically() -> None:
    inspection_results = list(reversed(_inspection_results()))

    rows = build_registration_unit_inventory_rows(inspection_results)

    observed_ids = [row.registration_unit_id for row in rows]
    assert observed_ids == sorted(observed_ids)


def test_registration_unit_inventory_preserves_expected_fixture_counts() -> None:
    rows = build_registration_unit_inventory_rows(_inspection_results())
    by_label = {row.registration_unit_label: row for row in rows}

    assert by_label["gsc_epilepsy"].artifacts_row_count == 9
    assert by_label["gsc_epilepsy"].assertion_registrations_row_count == 6
    assert by_label["gsc_epilepsy"].source_identities_row_count == 273

    assert by_label["gsc_mitochondrial_disease"].artifacts_row_count == 9
    assert by_label["gsc_mitochondrial_disease"].assertion_registrations_row_count == 6
    assert by_label["gsc_mitochondrial_disease"].source_identities_row_count == 254

    for label in [
        "vap_hg002",
        "vap_median_ERR10619300",
        "vap_q1_ERR10619212",
        "vap_q3_ERR10619225",
    ]:
        assert by_label[label].artifacts_row_count == 16
        assert by_label[label].assertion_registrations_row_count == 10
        assert by_label[label].source_identities_row_count == 281


def test_registration_unit_inventory_artifacts_are_emitted(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_inventory_artifacts(
        _inspection_results(),
        tmp_path,
    )

    assert artifact_set.artifact_status == "passed"
    assert artifact_set.row_count == 6
    assert artifact_set.tsv_path == tmp_path / INVENTORY_TSV_FILENAME
    assert artifact_set.json_path == tmp_path / INVENTORY_JSON_FILENAME
    assert artifact_set.tsv_path.is_file()
    assert artifact_set.json_path.is_file()


def test_registration_unit_inventory_tsv_schema_is_stable(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_inventory_artifacts(
        _inspection_results(),
        tmp_path,
    )

    with artifact_set.tsv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        assert reader.fieldnames == INVENTORY_COLUMNS
        rows = list(reader)

    assert len(rows) == 6
    assert {row["inventory_schema_version"] for row in rows} == {
        INVENTORY_SCHEMA_VERSION
    }


def test_registration_unit_inventory_json_schema_is_stable(
    tmp_path: Path,
) -> None:
    artifact_set = emit_registration_unit_inventory_artifacts(
        _inspection_results(),
        tmp_path,
    )

    payload = json.loads(artifact_set.json_path.read_text(encoding="utf-8"))

    assert payload["inventory_schema_version"] == INVENTORY_SCHEMA_VERSION
    assert payload["row_count"] == 6
    assert len(payload["registration_units"]) == 6

    observed_ids = [
        row["registration_unit_id"]
        for row in payload["registration_units"]
    ]
    assert observed_ids == sorted(observed_ids)


def test_registration_unit_inventory_artifact_emission_is_deterministic(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    first = emit_registration_unit_inventory_artifacts(
        _inspection_results(),
        first_dir,
    )
    second = emit_registration_unit_inventory_artifacts(
        list(reversed(_inspection_results())),
        second_dir,
    )

    assert first.tsv_path.read_bytes() == second.tsv_path.read_bytes()
    assert first.json_path.read_bytes() == second.json_path.read_bytes()


def test_registration_unit_inventory_rejects_empty_inspection_results() -> None:
    with pytest.raises(RegistrationUnitInventoryError, match="zero inspection results"):
        build_registration_unit_inventory_rows([])


def test_registration_unit_inventory_emission_does_not_mutate_sqlite_files(
    tmp_path: Path,
) -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )
    inspection_results = inspect_registration_units(records)

    before = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    emit_registration_unit_inventory_artifacts(
        inspection_results,
        tmp_path,
    )

    after = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    assert before == after


def _inspection_results():
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )
    return inspect_registration_units(records)

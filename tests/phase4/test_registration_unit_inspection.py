from __future__ import annotations

from pathlib import Path

from variant_database.phase4.registration_units.inspection import (
    REQUIRED_TABLES,
    inspect_registration_units,
)
from variant_database.phase4.registration_units.manifest import load_registration_unit_manifest


FIXTURE_MANIFEST = Path(
    "tests/fixtures/phase4/"
    "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
    "phase4_registration_unit_golden_fixture/"
    "manifests/registration_unit_input_manifest.tsv"
)


def test_registration_unit_inspection_passes_for_fixture_manifest() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    results = inspect_registration_units(records)

    assert len(results) == 6
    assert {result.inspection_status for result in results} == {"passed"}
    assert {result.open_status for result in results} == {"passed"}
    assert {result.query_only_status for result in results} == {"enabled"}
    assert {result.required_table_status for result in results} == {"passed"}
    assert {result.integrity_check_status for result in results} == {"ok"}


def test_registration_unit_inspection_finds_required_tables() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    results = inspect_registration_units(records)

    for result in results:
        observed_tables = {table.table_name for table in result.table_results}
        assert observed_tables == set(REQUIRED_TABLES)

        for table in result.table_results:
            assert table.exists is True
            assert table.table_status == "passed"
            assert table.missing_columns == tuple()
            assert table.row_count is not None
            assert table.row_count > 0


def test_registration_unit_inspection_preserves_expected_fixture_shape() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    results = inspect_registration_units(records)

    by_label = {result.registration_unit_label: result for result in results}

    assert _row_count(by_label["gsc_epilepsy"], "artifacts") == 9
    assert _row_count(by_label["gsc_epilepsy"], "assertion_registrations") == 6
    assert _row_count(by_label["gsc_epilepsy"], "source_identities") == 273

    assert _row_count(by_label["gsc_mitochondrial_disease"], "artifacts") == 9
    assert _row_count(by_label["gsc_mitochondrial_disease"], "assertion_registrations") == 6
    assert _row_count(by_label["gsc_mitochondrial_disease"], "source_identities") == 254

    for label in [
        "vap_hg002",
        "vap_median_ERR10619300",
        "vap_q1_ERR10619212",
        "vap_q3_ERR10619225",
    ]:
        assert _row_count(by_label[label], "artifacts") == 16
        assert _row_count(by_label[label], "assertion_registrations") == 10
        assert _row_count(by_label[label], "source_identities") == 281


def test_registration_unit_inspection_does_not_mutate_sqlite_files() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    before = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    inspect_registration_units(records)

    after = {
        record.sqlite_path_resolved: record.sqlite_path_resolved.stat().st_mtime_ns
        for record in records
    }

    assert before == after


def test_registration_unit_inspection_does_not_create_sqlite_sidecars() -> None:
    records = load_registration_unit_manifest(
        FIXTURE_MANIFEST,
        repo_root=Path.cwd(),
        validate_filesystem=True,
    )

    before = _sqlite_sidecars(records)

    inspect_registration_units(records)

    after = _sqlite_sidecars(records)

    assert before == after


def _row_count(result, table_name: str) -> int:
    for table in result.table_results:
        if table.table_name == table_name:
            assert table.row_count is not None
            return table.row_count
    raise AssertionError(f"Missing table inspection result: {table_name}")


def _sqlite_sidecars(records) -> set[Path]:
    sidecars: set[Path] = set()

    for record in records:
        sqlite_path = record.sqlite_path_resolved
        parent = sqlite_path.parent
        stem = sqlite_path.name

        for suffix in ["-wal", "-shm", "-journal"]:
            candidate = parent / f"{stem}{suffix}"
            if candidate.exists():
                sidecars.add(candidate)

    return sidecars
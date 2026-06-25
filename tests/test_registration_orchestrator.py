from __future__ import annotations

from pathlib import Path

from variant_database.persistence.backend import connect_sqlite
from variant_database.registration.registration_orchestrator import (
    run_registration_pipeline,
)


def test_registration_pipeline_handles_missing_package(tmp_path: Path) -> None:
    summary = run_registration_pipeline(
        package_path=tmp_path / "missing",
        db_path=tmp_path / "vdb.sqlite",
        producer_family="VAP",
    )

    assert summary.package_exists is False
    assert summary.artifact_count == 0
    assert summary.assertion_registration_count == 0
    assert summary.row_count_scanned == 0
    assert summary.participant_count_discovered == 0
    assert summary.source_identity_count == 0


def test_registration_pipeline_registers_vap_fixture(tmp_path: Path) -> None:
    package = tmp_path / "vap_tep_HG002_run_2026_06_03_010030_v1"
    (package / "entities" / "routing").mkdir(parents=True)
    (package / "entities" / "context").mkdir(parents=True)

    (
        package / "entities" / "routing" / "coding_candidates.tsv"
    ).write_text(
        "variant_id\tgene_symbol\tgene_id\n"
        "15:89333596:T:TTGC\tPOLG\tENSG00000140521\n"
        "1:100000:A:G\t\t\n",
        encoding="utf-8",
    )
    (
        package / "entities" / "context" / "stage_13_run_report.md"
    ).write_text("context", encoding="utf-8")
    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")

    summary = run_registration_pipeline(
        package_path=package,
        db_path=tmp_path / "vdb.sqlite",
        producer_family="VAP",
    )

    assert summary.package_exists is True
    assert summary.artifact_count == 3
    assert summary.assertion_registration_count == 1
    assert summary.row_count_scanned == 2
    assert summary.participant_count_discovered == 4
    assert summary.source_identity_count == 5

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    source_values = [
        row["source_value"]
        for row in connection.execute(
            """
            SELECT source_value
            FROM source_identities
            ORDER BY source_namespace, source_value, source_record_ref
            """
        ).fetchall()
    ]

    assert "HG002" in source_values
    assert "15:89333596:T:TTGC" in source_values
    assert "1:100000:A:G" in source_values
    assert "POLG" in source_values
    assert "ENSG00000140521" in source_values


def test_registration_pipeline_respects_max_rows_per_artifact(tmp_path: Path) -> None:
    package = tmp_path / "vap_tep_HG002_run_2026_06_03_010030_v1"
    (package / "entities" / "routing").mkdir(parents=True)

    (
        package / "entities" / "routing" / "coding_candidates.tsv"
    ).write_text(
        "variant_id\tgene_symbol\n"
        "15:89333596:T:TTGC\tPOLG\n"
        "1:100000:A:G\tGENE2\n",
        encoding="utf-8",
    )

    summary = run_registration_pipeline(
        package_path=package,
        db_path=tmp_path / "vdb.sqlite",
        producer_family="VAP",
        max_rows_per_artifact=1,
    )

    assert summary.row_count_scanned == 1
    assert summary.participant_count_discovered == 2

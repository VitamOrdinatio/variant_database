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


def test_registration_pipeline_registers_vap_package_metadata(tmp_path: Path) -> None:
    package = tmp_path / "vap_tep_HG002_run_2026_06_03_010030_v1"
    (package / "entities" / "metadata").mkdir(parents=True)

    (
        package / "entities" / "metadata" / "config_snapshot.yaml"
    ).write_text(
        "project:\n"
        "  name: variant_annotation_pipeline\n"
        "  pipeline_name: variant_annotation_pipeline\n"
        "  version: v1.0\n"
        "input:\n"
        "  sample_id: HG002\n"
        "  sample_alias: NA24385\n"
        "  sra_accession: SRR12898354\n"
        "  assay_type: WGS\n"
        "reference:\n"
        "  genome_build: GRCh38\n"
        "  fasta_path: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa\n"
        "  fasta_index: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa.fai\n"
        "  sequence_dictionary: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.dict\n"
        "tools:\n"
        "  vep:\n"
        "    assembly: GRCh38\n"
        "    cache_dir: /root/.vep\n"
        "runtime:\n"
        "  deterministic_mode: true\n"
        "  record_tool_versions: true\n",
        encoding="utf-8",
    )

    summary = run_registration_pipeline(
        package_path=package,
        db_path=tmp_path / "vdb.sqlite",
        producer_family="VAP",
    )

    assert summary.package_exists is True
    assert summary.package_metadata_count == 1
    assert summary.assertion_registration_count == 0
    assert summary.source_identity_count == 0

    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    row = connection.execute(
        """
        SELECT
            metadata_role,
            metadata_artifact_path,
            run_id,
            run_id_derivation_method,
            sample_id,
            sra_accession,
            reference_genome_build,
            annotation_engine,
            annotation_assembly,
            metadata_parse_status
        FROM package_metadata
        """
    ).fetchone()

    assert row is not None
    assert row["metadata_role"] == "package_metadata"
    assert row["metadata_artifact_path"] == "entities/metadata/config_snapshot.yaml"
    assert row["run_id"] == "run_2026_06_03_010030"
    assert row["run_id_derivation_method"] == "tep_package_path_regex"
    assert row["sample_id"] == "HG002"
    assert row["sra_accession"] == "SRR12898354"
    assert row["reference_genome_build"] == "GRCh38"
    assert row["annotation_engine"] == "vep"
    assert row["annotation_assembly"] == "GRCh38"
    assert row["metadata_parse_status"] == "parsed"


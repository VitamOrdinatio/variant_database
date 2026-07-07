from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.package_scanner import scan_package
from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.repositories import (
    list_artifact_records,
    list_package_metadata_records,
    persist_package_inventory,
    persist_package_metadata_record,
)
from variant_database.persistence.schema_manager import initialize_schema
from variant_database.registration.metadata_extractor import (
    VAP_CONFIG_SNAPSHOT_RELATIVE_PATH,
    build_vap_package_metadata_record,
    derive_run_id_from_tep_path,
)


CONFIG_TEXT = """
project:
  name: variant_annotation_pipeline
  pipeline_name: variant_annotation_pipeline
  version: v1.0
input:
  sample_id: HG002
  sample_alias: NA24385
  sra_accession: SRR12898354
  assay_type: WGS
execution_profile:
  name: mark_hg002_sidecar_metrics_auto_render_test
  hardware_class: MARK1
reference:
  genome_build: GRCh38
  fasta_path: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa
  fasta_index: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.fa.fai
  sequence_dictionary: /data/storage/reference/grch38/GRCh38.primary_assembly.genome.dict
tools:
  vep:
    executable: /root/tools/vep/vep
    cache_dir: /root/.vep
    assembly: GRCh38
runtime:
  deterministic_mode: true
  record_tool_versions: true
""".strip()


def test_derive_run_id_from_vap_tep_path() -> None:
    run_id, method = derive_run_id_from_tep_path(
        "/x/vap_tep_HG002_run_2026_06_03_010030_v1"
    )

    assert run_id == "run_2026_06_03_010030"
    assert method == "tep_package_path_regex"


def test_build_vap_package_metadata_record_extracts_reference_context(
    tmp_path: Path,
) -> None:
    package = tmp_path / "vap_tep_HG002_run_2026_06_03_010030_v1"
    metadata_path = package / VAP_CONFIG_SNAPSHOT_RELATIVE_PATH
    metadata_path.parent.mkdir(parents=True)
    metadata_path.write_text(CONFIG_TEXT, encoding="utf-8")

    inventory = scan_package(package)
    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    package_id = persist_package_inventory(connection, inventory)
    artifact_records = list_artifact_records(connection, package_id)

    metadata_record = build_vap_package_metadata_record(
        package_id=package_id,
        package_path=inventory.package_path,
        artifact_records=artifact_records,
    )

    assert metadata_record is not None
    assert metadata_record["metadata_artifact_path"] == VAP_CONFIG_SNAPSHOT_RELATIVE_PATH
    assert metadata_record["metadata_role"] == "package_metadata"
    assert metadata_record["metadata_parse_status"] == "parsed"
    assert metadata_record["run_id"] == "run_2026_06_03_010030"
    assert metadata_record["sample_id"] == "HG002"
    assert metadata_record["sample_alias"] == "NA24385"
    assert metadata_record["sra_accession"] == "SRR12898354"
    assert metadata_record["assay_type"] == "WGS"
    assert metadata_record["reference_genome_build"] == "GRCh38"
    assert metadata_record["annotation_engine"] == "vep"
    assert metadata_record["annotation_assembly"] == "GRCh38"
    assert metadata_record["deterministic_mode"] == 1
    assert metadata_record["record_tool_versions"] == 1

    persist_package_metadata_record(connection, metadata_record)
    persisted = list_package_metadata_records(connection, package_id=package_id)

    assert len(persisted) == 1
    assert persisted[0]["reference_genome_build"] == "GRCh38"
    assert persisted[0]["metadata_artifact_sha256"] == metadata_record["metadata_artifact_sha256"]


def test_build_vap_package_metadata_record_returns_none_when_snapshot_missing(
    tmp_path: Path,
) -> None:
    package = tmp_path / "vap_tep_HG002_run_2026_06_03_010030_v1"
    package.mkdir()
    (package / "entity_inventory.json").write_text("{}", encoding="utf-8")

    inventory = scan_package(package)
    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)
    package_id = persist_package_inventory(connection, inventory)
    artifact_records = list_artifact_records(connection, package_id)

    metadata_record = build_vap_package_metadata_record(
        package_id=package_id,
        package_path=inventory.package_path,
        artifact_records=artifact_records,
    )

    assert metadata_record is None

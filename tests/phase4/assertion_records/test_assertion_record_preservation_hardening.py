from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

import pytest

from variant_database.phase4.assertion_records.builder import build_assertion_records

pytestmark = pytest.mark.phase4_3_layer1


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _make_sqlite(path: Path) -> None:
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE assertion_registrations (
                assertion_registration_id TEXT,
                package_id TEXT,
                artifact_id TEXT,
                surface_role TEXT,
                evidence_domain TEXT,
                producer_family TEXT,
                source_record_ref TEXT,
                assertion_type TEXT,
                participant_summary_json TEXT,
                support_ref_json TEXT,
                authority_context TEXT,
                uncertainty_context TEXT,
                registration_status TEXT,
                payload_json TEXT
            );
            CREATE TABLE source_identities (
                source_identity_id TEXT,
                assertion_registration_id TEXT,
                identity_kind TEXT,
                participant_role TEXT,
                source_value TEXT,
                source_namespace TEXT,
                source_label TEXT,
                extraction_method TEXT,
                source_record_ref TEXT,
                payload_json TEXT,
                source_identity_count INTEGER
            );
            CREATE TABLE artifacts (
                artifact_id TEXT,
                package_id TEXT,
                relative_path TEXT,
                size_bytes INTEGER,
                sha256 TEXT,
                is_manifest INTEGER
            );
            CREATE TABLE tep_packages (
                package_id TEXT,
                producer_family TEXT
            );
            CREATE TABLE schema_metadata (
                schema_name TEXT,
                schema_version TEXT
            );
            """
        )
        conn.execute(
            """
            INSERT INTO assertion_registrations VALUES (
                'ar_variant_observation_001',
                'pkg_vap_001',
                'artifact_vap_001',
                'observation',
                'variant',
                'VAP',
                '',
                'variant_observation',
                '{}',
                '{"relative_path":"variants.tsv"}',
                'producer_emitted',
                'source_asserted',
                'registered',
                '{"row_count": 2}'
            )
            """
        )
        conn.executemany(
            """
            INSERT INTO source_identities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    'sis_candidate_variant',
                    'ar_variant_observation_001',
                    'variant',
                    'variant',
                    '__compressed_source_identity_set__',
                    'vap_variant_id',
                    'compressed source identity set candidate',
                    'phase4_3_layer2_fixture_materialization',
                    'assertion_registration_id=ar_variant_observation_001;identity_kind=variant;participant_role=variant;source_namespace=vap_variant_id',
                    json.dumps({'source_identity_filter': 'variant-filter'}, sort_keys=True),
                    11,
                ),
                (
                    'sis_candidate_gene',
                    'ar_variant_observation_001',
                    'gene',
                    'gene',
                    '__compressed_source_identity_set__',
                    'vap_ensembl_gene_id',
                    'compressed source identity set candidate',
                    'phase4_3_layer2_fixture_materialization',
                    'assertion_registration_id=ar_variant_observation_001;identity_kind=gene;participant_role=gene;source_namespace=vap_ensembl_gene_id',
                    json.dumps({'source_identity_filter': 'gene-filter'}, sort_keys=True),
                    7,
                ),
            ],
        )
        conn.execute(
            """
            INSERT INTO artifacts VALUES (
                'artifact_vap_001',
                'pkg_vap_001',
                'entities/observation/variants.tsv',
                12345,
                'abc123sha',
                0
            )
            """
        )
        conn.execute("INSERT INTO tep_packages VALUES ('pkg_vap_001', 'VAP')")
        conn.execute("INSERT INTO schema_metadata VALUES ('registration_unit', 'test')")
        conn.commit()
    finally:
        conn.close()


def test_phase4_3_builder_preserves_participants_lineage_status_and_source_identity_set_ids(tmp_path: Path) -> None:
    db_path = tmp_path / "synthetic_vap.sqlite"
    _make_sqlite(db_path)

    manifest_path = tmp_path / "downstream_manifest.tsv"
    manifest_path.write_text(
        "registration_unit_id\tproducer_family\tregistration_unit_sqlite_path\n"
        f"synthetic_vap\tVAP\t{db_path}\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "assertion_records"
    build_assertion_records(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id="synthetic_corpus_generation",
    )

    index_rows = _read_tsv(output_dir / "assertion_record_index.tsv")
    assert len(index_rows) == 1
    assert index_rows[0]["preservation_status"] == "preserved"
    assert index_rows[0]["resolver_status"] == "supported"
    assert index_rows[0]["validation_status"] == "supported"

    source_identity_sets = _read_tsv(output_dir / "assertion_record_source_identity_sets.tsv")
    assert len(source_identity_sets) == 2
    assert {row["source_identity_count"] for row in source_identity_sets} == {"7", "11"}
    assert all(row["source_identity_set_id"].startswith("sis_") for row in source_identity_sets)

    participants = _read_tsv(output_dir / "assertion_record_participants.tsv")
    assert len(participants) == 2
    assert {row["participant_role"] for row in participants} == {"gene", "variant"}
    assert all(row["participant_source"] == "source_identity_set_reference" for row in participants)
    assert all(row["participant_value"].startswith("source_identity_set:sis_") for row in participants)
    assert {row["participant_count"] for row in participants} == {"7", "11"}
    assert {row["participant_source_namespace"] for row in participants} == {"vap_ensembl_gene_id", "vap_variant_id"}

    lineage = _read_tsv(output_dir / "assertion_record_lineage.tsv")
    assert len(lineage) == 1
    assert lineage[0]["source_artifact_relative_path"] == "entities/observation/variants.tsv"
    assert lineage[0]["source_artifact_sha256"] == "abc123sha"
    assert lineage[0]["source_artifact_size_bytes"] == "12345"
    assert lineage[0]["source_record_ref"] == ""
    assert lineage[0]["source_record_ref_status"] == "explicit_absence"
    assert lineage[0]["lineage_completeness_status"] == "artifact_level_lineage_present_row_ref_absent"

    summary = json.loads((output_dir / "assertion_record_validation_report.json").read_text(encoding="utf-8"))
    assert summary["participant_count"] == 2
    assert summary["preservation_status_counts"] == {"preserved": 1}
    assert summary["resolver_status_counts"] == {"supported": 1}
    assert summary["lineage_completeness_status_counts"] == {
        "artifact_level_lineage_present_row_ref_absent": 1
    }

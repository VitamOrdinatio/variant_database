"""Layer 1 synthetic checks for compressed source identity count handling.

This test protects the Phase 4.3D bridge. Layer 2 materializes compressed
real-world source identity set candidates into temporary SQLite rows that carry
precomputed source_identity_count values. The builder must preserve those set
cardinalities rather than counting only the representative rows.
"""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

import pytest

from variant_database.phase4.assertion_records.builder import build_assertion_records

pytestmark = pytest.mark.phase4_3_layer1


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="	"))


def _create_registration_unit_with_compressed_counts(path: Path) -> None:
    conn = sqlite3.connect(path)
    try:
        conn.execute(
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
            )
            """
        )
        conn.execute(
            """
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
                source_identity_count TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE artifacts (
                artifact_id TEXT,
                package_id TEXT,
                relative_path TEXT,
                size_bytes INTEGER,
                sha256 TEXT,
                is_manifest INTEGER
            )
            """
        )
        conn.execute(
            """
            INSERT INTO assertion_registrations VALUES (
                'assertion-001',
                'package-001',
                'artifact-001',
                'observation',
                'variant',
                'VAP',
                'record-001',
                'variant_observation',
                '{"sample":"SYNTH_SAMPLE","variant":"1:100:A:T"}',
                '{"artifact_id":"artifact-001"}',
                'producer_emitted',
                'source_asserted',
                'registered',
                '{"fixture":"compressed-count"}'
            )
            """
        )
        conn.execute(
            """
            INSERT INTO artifacts VALUES (
                'artifact-001',
                'package-001',
                'synthetic/variant_observation.tsv',
                123,
                'sha256-placeholder',
                0
            )
            """
        )
        rows = [
            (
                'set-row-variant',
                'assertion-001',
                'variant',
                'variant',
                '__compressed_source_identity_set__',
                'vap_variant_id',
                'compressed variant set',
                'phase4_3_layer2_fixture_materialization',
                '',
                '{"source_identity_filter":"assertion_registration_id=assertion-001;identity_kind=variant;participant_role=variant;source_namespace=vap_variant_id"}',
                '42',
            ),
            (
                'set-row-gene-a',
                'assertion-001',
                'gene',
                'gene',
                '__compressed_source_identity_set__',
                'vap_ensembl_gene_id',
                'compressed gene set A',
                'phase4_3_layer2_fixture_materialization',
                '',
                '{}',
                '3',
            ),
            (
                'set-row-gene-b',
                'assertion-001',
                'gene',
                'gene',
                '__compressed_source_identity_set__',
                'vap_ensembl_gene_id',
                'compressed gene set B',
                'phase4_3_layer2_fixture_materialization',
                '',
                '{}',
                '4',
            ),
            (
                'physical-sample-row',
                'assertion-001',
                'sample',
                'sample',
                'SYNTH_SAMPLE',
                'vap_sample_id',
                'synthetic sample',
                'physical_row',
                'record-001',
                '{}',
                '',
            ),
        ]
        conn.executemany(
            """
            INSERT INTO source_identities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
    finally:
        conn.close()


def test_builder_honors_precomputed_source_identity_count_in_compressed_rows(tmp_path: Path) -> None:
    db_path = tmp_path / "synthetic_compressed_counts.sqlite"
    _create_registration_unit_with_compressed_counts(db_path)

    manifest_path = tmp_path / "downstream_assertion_record_input_manifest.tsv"
    manifest_path.write_text(
        "registration_unit_id\tproducer_family\tregistration_unit_sqlite_path\n"
        f"synthetic_vap_compressed_counts\tVAP\t{db_path}\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "assertion_records"
    build_assertion_records(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id="synthetic_corpus_generation_compressed_counts",
    )

    summary_rows = _read_tsv(output_dir / "assertion_record_source_identity_summary.tsv")
    count_by_group = {
        (row["identity_kind"], row["participant_role"], row["source_namespace"]): int(row["source_identity_count"])
        for row in summary_rows
    }

    assert count_by_group[("variant", "variant", "vap_variant_id")] == 42
    assert count_by_group[("gene", "gene", "vap_ensembl_gene_id")] == 7
    assert count_by_group[("sample", "sample", "vap_sample_id")] == 1

    set_rows = _read_tsv(output_dir / "assertion_record_source_identity_sets.tsv")
    variant_row = next(row for row in set_rows if row["identity_kind"] == "variant")
    assert variant_row["source_identity_count"] == "42"
    assert "assertion_registration_id=assertion-001" in variant_row["source_identity_filter"]
    assert "identity_kind=variant" in variant_row["source_identity_filter"]
    assert "participant_role=variant" in variant_row["source_identity_filter"]
    assert "source_namespace=vap_variant_id" in variant_row["source_identity_filter"]

"""SQLite-side source identity aggregation tests for Phase 4.3.

These tests harden the Assertion Record builder for Layer 3 MARK full-corpus
validation. The builder must not load the full source_identities table into
Python when a Registration Unit may contain production-scale source identity
rows.
"""
from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

import pytest

from variant_database.phase4.assertion_records import builder as builder_module
from variant_database.phase4.assertion_records.builder import build_assertion_records

pytestmark = pytest.mark.phase4_3_layer1


def _create_registration_unit_with_compressed_counts(path: Path) -> None:
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
            """
        )
        conn.execute(
            """
            INSERT INTO assertion_registrations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ar-sql-aggregation-001",
                "pkg-sql-aggregation",
                "artifact-sql-aggregation",
                "observation",
                "variant",
                "VAP",
                "synthetic-row-1",
                "variant_observation",
                json.dumps({"sample": "SYNTH", "variant": "1:100:A:T"}, sort_keys=True),
                json.dumps({"artifact_id": "artifact-sql-aggregation"}, sort_keys=True),
                "producer_emitted",
                "source_asserted",
                "registered",
                json.dumps({"registration_level": "record"}, sort_keys=True),
            ),
        )
        conn.execute(
            """
            INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "artifact-sql-aggregation",
                "pkg-sql-aggregation",
                "entities/observation/synthetic.tsv",
                123,
                "sha256-synthetic",
                0,
            ),
        )
        conn.executemany(
            """
            INSERT INTO source_identities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "compressed-set-001",
                    "ar-sql-aggregation-001",
                    "variant",
                    "variant",
                    "__compressed_source_identity_set__",
                    "vap_variant_id",
                    "compressed source identity set candidate",
                    "phase4_3_layer2_fixture_materialization",
                    "assertion_registration_id=ar-sql-aggregation-001;identity_kind=variant;participant_role=variant;source_namespace=vap_variant_id",
                    json.dumps({"source_identity_filter": "variant partition"}, sort_keys=True),
                    100,
                ),
                (
                    "compressed-set-002",
                    "ar-sql-aggregation-001",
                    "variant",
                    "variant",
                    "__compressed_source_identity_set__",
                    "vap_variant_id",
                    "compressed source identity set candidate",
                    "phase4_3_layer2_fixture_materialization",
                    "assertion_registration_id=ar-sql-aggregation-001;identity_kind=variant;participant_role=variant;source_namespace=vap_variant_id",
                    json.dumps({"source_identity_filter": "variant partition supplemental"}, sort_keys=True),
                    23,
                ),
                (
                    "compressed-set-003",
                    "ar-sql-aggregation-001",
                    "gene",
                    "gene",
                    "__compressed_source_identity_set__",
                    "vap_gene_symbol",
                    "compressed source identity set candidate",
                    "phase4_3_layer2_fixture_materialization",
                    "assertion_registration_id=ar-sql-aggregation-001;identity_kind=gene;participant_role=gene;source_namespace=vap_gene_symbol",
                    json.dumps({"source_identity_filter": "gene partition"}, sort_keys=True),
                    7,
                ),
            ],
        )
        conn.commit()
    finally:
        conn.close()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_source_identity_groups_are_aggregated_inside_sqlite(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """The builder must not Python-load source_identities for full-corpus runs."""
    db_path = tmp_path / "synthetic_compressed_counts.sqlite"
    _create_registration_unit_with_compressed_counts(db_path)

    manifest_path = tmp_path / "downstream_assertion_record_input_manifest.tsv"
    manifest_path.write_text(
        "registration_unit_id\tproducer_family\tregistration_unit_sqlite_path\n"
        f"synthetic_vap_sqlite_aggregation\tVAP\t{db_path}\n",
        encoding="utf-8",
    )

    original_select_all = builder_module._select_all

    def guarded_select_all(conn: sqlite3.Connection, table_name: str):
        if table_name == "source_identities":
            raise AssertionError("source_identities must be aggregated in SQLite, not loaded with _select_all")
        return original_select_all(conn, table_name)

    monkeypatch.setattr(builder_module, "_select_all", guarded_select_all)

    output_dir = tmp_path / "assertion_records"
    build_assertion_records(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id="synthetic_corpus_sqlite_aggregation",
    )

    summary_rows = _read_tsv(output_dir / "assertion_record_source_identity_summary.tsv")
    counts = {
        (row["identity_kind"], row["participant_role"], row["source_namespace"]): int(row["source_identity_count"])
        for row in summary_rows
    }

    assert counts[("variant", "variant", "vap_variant_id")] == 123
    assert counts[("gene", "gene", "vap_gene_symbol")] == 7

    set_rows = _read_tsv(output_dir / "assertion_record_source_identity_sets.tsv")
    variant_rows = [row for row in set_rows if row["identity_kind"] == "variant"]
    assert len(variant_rows) == 1
    assert variant_rows[0]["source_identity_count"] == "123"
    assert "assertion_registration_id=ar-sql-aggregation-001" in variant_rows[0]["source_identity_filter"]
    assert "identity_kind=variant" in variant_rows[0]["source_identity_filter"]

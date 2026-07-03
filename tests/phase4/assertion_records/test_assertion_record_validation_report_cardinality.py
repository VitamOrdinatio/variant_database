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


def _make_gsc_contract_validation_sqlite(path: Path) -> None:
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
                'ar_gsc_contract_validation_001',
                'pkg_gsc_001',
                'artifact_gsc_contract_validation_001',
                'producer_contract_validation',
                'contract_validation',
                'GSC',
                '',
                'producer_contract_validation',
                '{}',
                '{"relative_path":"validation/contract_validation.json"}',
                'producer_emitted',
                'source_asserted',
                'registered',
                '{"validation_status":"passed"}'
            )
            """
        )
        conn.execute(
            """
            INSERT INTO artifacts VALUES (
                'artifact_gsc_contract_validation_001',
                'pkg_gsc_001',
                'validation/contract_validation.json',
                456,
                'deadbeefsha',
                0
            )
            """
        )
        conn.execute("INSERT INTO tep_packages VALUES ('pkg_gsc_001', 'GSC')")
        conn.execute("INSERT INTO schema_metadata VALUES ('registration_unit', 'test')")
        conn.commit()
    finally:
        conn.close()


def test_not_applicable_source_identity_assertion_has_single_assertion_aligned_validation_row(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "synthetic_gsc_contract_validation.sqlite"
    _make_gsc_contract_validation_sqlite(db_path)

    manifest_path = tmp_path / "downstream_manifest.tsv"
    manifest_path.write_text(
        "registration_unit_id\tproducer_family\tregistration_unit_sqlite_path\n"
        f"synthetic_gsc\tGSC\t{db_path}\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "assertion_records"
    result = build_assertion_records(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id="synthetic_corpus_generation",
    )

    index_rows = _read_tsv(output_dir / "assertion_record_index.tsv")
    validation_rows = _read_tsv(output_dir / "assertion_record_validation_report.tsv")
    source_identity_sets = _read_tsv(output_dir / "assertion_record_source_identity_sets.tsv")
    participants = _read_tsv(output_dir / "assertion_record_participants.tsv")
    validation_json = json.loads((output_dir / "assertion_record_validation_report.json").read_text(encoding="utf-8"))

    assert result.assertion_count == 1
    assert result.validation_count == 1
    assert len(index_rows) == 1
    assert len(validation_rows) == 1
    assert validation_json["assertion_record_count"] == 1
    assert validation_json["validation_row_count"] == 1

    row = validation_rows[0]
    assert row["producer_family"] == "GSC"
    assert row["assertion_type"] == "producer_contract_validation"
    assert row["preservation_status"] == "preserved"
    assert row["resolver_status"] == "indexed_with_note"
    assert row["validation_status"] == "indexed_with_note"
    assert row["source_identity_set_status"] == "not_applicable"
    assert row["resolver_status"] != "not_applicable_for_source_identity_sets"

    assert index_rows[0]["source_identity_set_status"] == "not_applicable"
    assert source_identity_sets == []
    assert participants == []

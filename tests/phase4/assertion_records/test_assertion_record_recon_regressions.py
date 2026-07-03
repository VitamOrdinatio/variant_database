"""Layer 1 regression tests for Phase 4.3E reconnaissance findings.

These tests lock down the preservation invariants exposed by the MARK input
substrate reconnaissance. They deliberately use synthetic Registration Units;
Layer 2 owns compressed real-world fixture validation and Layer 3 owns MARK
full-corpus validation.
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
        return list(csv.DictReader(handle, delimiter="\t"))


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=[
                "registration_unit_id",
                "producer_family",
                "registration_unit_sqlite_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _create_registration_unit(
    db_path: Path,
    *,
    producer_family: str,
    assertion_rows: list[tuple[str, str, str, str, str]],
    source_identity_rows: list[tuple[str, str, str, str, str, str]],
) -> None:
    """Create a tiny Registration Unit SQLite database.

    assertion_rows tuple:
        assertion_registration_id, artifact_id, assertion_type, surface_role, evidence_domain

    source_identity_rows tuple:
        source_identity_id, assertion_registration_id, identity_kind,
        participant_role, source_value, source_namespace
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
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
                payload_json TEXT
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
        package_id = f"pkg_{producer_family.lower()}_recon"
        for assertion_registration_id, artifact_id, assertion_type, surface_role, evidence_domain in assertion_rows:
            conn.execute(
                """
                INSERT INTO assertion_registrations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assertion_registration_id,
                    package_id,
                    artifact_id,
                    surface_role,
                    evidence_domain,
                    producer_family,
                    "",  # source_record_ref intentionally absent in real-corpus-like substrate
                    assertion_type,
                    "{}",  # participant_summary_json intentionally empty
                    f'{{"artifact_id":"{artifact_id}","package_id":"{package_id}"}}',
                    "producer_emitted",
                    "source_asserted",
                    "registered",
                    f'{{"registration_level":"artifact","artifact_id":"{artifact_id}"}}',
                ),
            )
            conn.execute(
                "INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?)",
                (
                    artifact_id,
                    package_id,
                    f"reports/{assertion_type}.tsv",
                    123,
                    f"sha256_{artifact_id}",
                    0,
                ),
            )

        for source_identity_id, assertion_registration_id, identity_kind, participant_role, source_value, source_namespace in source_identity_rows:
            conn.execute(
                """
                INSERT INTO source_identities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_identity_id,
                    assertion_registration_id,
                    identity_kind,
                    participant_role,
                    source_value,
                    source_namespace,
                    source_value,
                    "synthetic_recon_regression_fixture",
                    "",
                    "{}",
                ),
            )

        conn.execute("INSERT INTO tep_packages VALUES (?, ?)", (package_id, producer_family))
        conn.execute("INSERT INTO schema_metadata VALUES (?, ?)", ("registration_unit", "synthetic_recon_v1"))
        conn.commit()
    finally:
        conn.close()


@pytest.fixture()
def recon_regression_output(tmp_path: Path) -> Path:
    vap_db = tmp_path / "synthetic_vap_recon" / "vdb.sqlite"
    gsc_db = tmp_path / "synthetic_gsc_recon" / "vdb.sqlite"

    _create_registration_unit(
        vap_db,
        producer_family="VAP",
        assertion_rows=[
            (
                "vap_candidate_routing_001",
                "artifact_vap_candidate_routing",
                "candidate_routing",
                "candidate_routing",
                "VAP",
            ),
        ],
        source_identity_rows=[
            (
                "si_vap_variant_001",
                "vap_candidate_routing_001",
                "variant",
                "variant",
                "15:89333596:T:TTGC",
                "vap_variant_id",
            ),
            (
                "si_vap_variant_002",
                "vap_candidate_routing_001",
                "variant",
                "variant",
                "15:89333610:A:G",
                "vap_variant_id",
            ),
            (
                "si_vap_gene_001",
                "vap_candidate_routing_001",
                "gene",
                "gene",
                "ENSG00000140521",
                "vap_ensembl_gene_id",
            ),
        ],
    )

    _create_registration_unit(
        gsc_db,
        producer_family="GSC",
        assertion_rows=[
            (
                "gsc_contract_validation_001",
                "artifact_gsc_contract_validation",
                "producer_contract_validation",
                "output_contract_validation",
                "GSC",
            ),
        ],
        source_identity_rows=[],
    )

    manifest = tmp_path / "downstream_assertion_record_input_manifest.tsv"
    _write_manifest(
        manifest,
        [
            {
                "registration_unit_id": "synthetic_vap_recon",
                "producer_family": "VAP",
                "registration_unit_sqlite_path": str(vap_db),
            },
            {
                "registration_unit_id": "synthetic_gsc_recon",
                "producer_family": "GSC",
                "registration_unit_sqlite_path": str(gsc_db),
            },
        ],
    )

    output_dir = tmp_path / "assertion_records"
    build_assertion_records(
        manifest_path=manifest,
        output_dir=output_dir,
        corpus_generation_id="synthetic_recon_regression_corpus",
    )
    return output_dir


def test_empty_participant_summary_uses_source_identity_sets(recon_regression_output: Path) -> None:
    participants = _read_tsv(recon_regression_output / "assertion_record_participants.tsv")

    assert participants, "source identity participants should populate participants when participant_summary_json is empty"
    assert {row["source_assertion_registration_id"] for row in participants} == {"vap_candidate_routing_001"}
    assert {row["participant_source"] for row in participants} == {"source_identity_set_reference"}
    assert {row["participant_role"] for row in participants} == {"gene", "variant"}
    assert all(row["source_identity_set_id"] for row in participants)
    assert all(row["participant_count"] for row in participants)
    assert all(row["participant_resolution_status"] for row in participants)


def test_participants_join_to_source_identity_sets(recon_regression_output: Path) -> None:
    participants = _read_tsv(recon_regression_output / "assertion_record_participants.tsv")
    sets = _read_tsv(recon_regression_output / "assertion_record_source_identity_sets.tsv")

    set_ids = {row["source_identity_set_id"] for row in sets}
    participant_set_ids = {row["source_identity_set_id"] for row in participants}

    assert participant_set_ids
    assert participant_set_ids <= set_ids


def test_source_identity_summary_joins_to_source_identity_sets(recon_regression_output: Path) -> None:
    summaries = _read_tsv(recon_regression_output / "assertion_record_source_identity_summary.tsv")
    sets = _read_tsv(recon_regression_output / "assertion_record_source_identity_sets.tsv")

    set_ids = {row["source_identity_set_id"] for row in sets}
    summary_set_ids = {row["source_identity_set_id"] for row in summaries}

    assert summary_set_ids
    assert summary_set_ids <= set_ids


def test_deferred_resolver_status_is_still_preserved(recon_regression_output: Path) -> None:
    index_rows = _read_tsv(recon_regression_output / "assertion_record_index.tsv")
    row = next(row for row in index_rows if row["source_assertion_registration_id"] == "vap_candidate_routing_001")

    assert row["assertion_type"] == "candidate_routing"
    assert row["preservation_status"] == "preserved"
    assert row["resolver_status"] == "deferred"


def test_lineage_explicitly_represents_artifact_level_provenance_when_row_ref_absent(
    recon_regression_output: Path,
) -> None:
    lineage_rows = _read_tsv(recon_regression_output / "assertion_record_lineage.tsv")
    row = next(row for row in lineage_rows if row["source_assertion_registration_id"] == "vap_candidate_routing_001")

    assert row["source_record_ref"] == ""
    assert row["source_record_ref_status"] == "explicit_absence"
    assert row["lineage_completeness_status"] == "artifact_level_lineage_present_row_ref_absent"
    assert row["source_artifact_relative_path"] == "reports/candidate_routing.tsv"
    assert row["source_artifact_sha256"] == "sha256_artifact_vap_candidate_routing"
    assert row["source_artifact_size_bytes"] == "123"


def test_artifact_level_validation_assertion_has_not_applicable_source_identity_status(
    recon_regression_output: Path,
) -> None:
    index_rows = _read_tsv(recon_regression_output / "assertion_record_index.tsv")
    participants = _read_tsv(recon_regression_output / "assertion_record_participants.tsv")
    validation_rows = _read_tsv(recon_regression_output / "assertion_record_validation_report.tsv")

    row = next(row for row in index_rows if row["source_assertion_registration_id"] == "gsc_contract_validation_001")
    assert row["assertion_type"] == "producer_contract_validation"
    assert row["preservation_status"] == "preserved"
    assert row["resolver_status"] == "indexed_with_note"
    assert row["source_identity_set_status"] == "not_applicable"

    assert not [
        participant
        for participant in participants
        if participant["source_assertion_registration_id"] == "gsc_contract_validation_001"
    ]
    matching_validation_rows = [
        validation
        for validation in validation_rows
        if validation["source_assertion_registration_id"] == "gsc_contract_validation_001"
    ]
    assert len(matching_validation_rows) == 1
    validation = matching_validation_rows[0]
    assert validation["preservation_status"] == "preserved"
    assert validation["resolver_status"] == "indexed_with_note"
    assert validation["validation_status"] == "indexed_with_note"
    assert validation["source_identity_set_status"] == "not_applicable"
    assert validation["resolver_status"] != "not_applicable_for_source_identity_sets"
    assert validation["validation_status"] != "not_applicable_for_source_identity_sets"

"""Layer 1 synthetic integration tests for the Assertion Record builder."""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.phase4.assertion_records.helpers.builder_imports import import_required
from tests.phase4.assertion_records.helpers.synthetic_registration_units import (
    build_layer1_synthetic_corpus,
    read_tsv,
)

pytestmark = pytest.mark.phase4_3_layer1

EXPECTED_OUTPUT_FILES = {
    "assertion_record_index.tsv",
    "assertion_record_index.jsonl",
    "assertion_record_participants.tsv",
    "assertion_record_relationships.tsv",
    "assertion_record_evidence_basis.tsv",
    "assertion_record_context.tsv",
    "assertion_record_lineage.tsv",
    "assertion_record_payload_references.tsv",
    "assertion_record_source_identity_sets.tsv",
    "assertion_record_source_identity_summary.tsv",
    "assertion_record_validation_report.tsv",
    "assertion_record_validation_report.json",
    "downstream_topology_input_manifest.tsv",
}


def _run_builder(builder_module, *, manifest_path: Path, output_dir: Path, corpus_generation_id: str):
    if hasattr(builder_module, "build_assertion_records_from_manifest"):
        return builder_module.build_assertion_records_from_manifest(
            manifest_path=manifest_path,
            output_dir=output_dir,
            corpus_generation_id=corpus_generation_id,
        )
    if hasattr(builder_module, "build_assertion_records"):
        return builder_module.build_assertion_records(
            manifest_path=manifest_path,
            output_dir=output_dir,
            corpus_generation_id=corpus_generation_id,
        )
    pytest.fail(
        "builder module must expose build_assertion_records_from_manifest(...) "
        "or build_assertion_records(...)"
    )


def test_builder_emits_required_layer1_output_family(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    observed = {path.name for path in corpus.output_dir.iterdir() if path.is_file()}
    missing = EXPECTED_OUTPUT_FILES - observed
    assert not missing, "missing Assertion Record output files: " + ", ".join(sorted(missing))


def test_builder_preserves_lineage_and_accounts_for_every_input_assertion(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    index_rows = read_tsv(corpus.output_dir / "assertion_record_index.tsv")
    validation_rows = read_tsv(corpus.output_dir / "assertion_record_validation_report.tsv")

    required_index_columns = {
        "assertion_id",
        "source_assertion_key",
        "corpus_generation_id",
        "registration_unit_id",
        "producer_family",
        "source_assertion_registration_id",
        "assertion_type",
        "validation_status",
    }
    assert required_index_columns <= set(index_rows[0]), "Assertion Record index lacks required columns"

    represented_assertions = {
        row.get("source_assertion_registration_id", "") for row in index_rows + validation_rows
    }
    missing = set(corpus.assertion_registration_ids) - represented_assertions
    assert not missing, "input assertion registrations were silently dropped: " + ", ".join(sorted(missing))

    for row in index_rows:
        assert row["corpus_generation_id"] == corpus.corpus_generation_id
        assert row["registration_unit_id"]
        assert row["producer_family"] in {"VAP", "GSC"}
        assert row["assertion_id"]
        assert row["source_assertion_key"]


def test_participants_are_role_bearing_and_relationships_are_explicit(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    participant_rows = read_tsv(corpus.output_dir / "assertion_record_participants.tsv")
    relationship_rows = read_tsv(corpus.output_dir / "assertion_record_relationships.tsv")

    assert participant_rows, "participants output must not be empty"
    assert relationship_rows, "relationships output must not be empty"

    assert {"assertion_id", "participant_role"} <= set(participant_rows[0])
    assert {"assertion_id", "relationship_class"} <= set(relationship_rows[0])

    roles = {row["participant_role"] for row in participant_rows}
    assert {"sample", "variant", "gene", "phenotype"} & roles
    assert all(row["participant_role"] for row in participant_rows)
    assert all(row["relationship_class"] for row in relationship_rows)


def test_source_identity_sets_are_partitioned_and_not_flattened(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    set_rows = read_tsv(corpus.output_dir / "assertion_record_source_identity_sets.tsv")
    summary_rows = read_tsv(corpus.output_dir / "assertion_record_source_identity_summary.tsv")

    assert set_rows, "source identity set output must not be empty"
    assert summary_rows, "source identity summary output must not be empty"

    required_set_columns = {
        "assertion_id",
        "source_assertion_registration_id",
        "source_identity_filter",
        "identity_kind",
        "participant_role",
        "source_namespace",
        "source_identity_count",
        "lossiness_status",
    }
    assert required_set_columns <= set(set_rows[0])

    filters = [row["source_identity_filter"] for row in set_rows]
    assert any("identity_kind=" in value for value in filters)
    assert any("participant_role=" in value for value in filters)
    assert any("source_namespace=" in value for value in filters)
    assert any(row["lossiness_status"] == "lossless_by_reference" for row in set_rows)


def test_artifact_level_contract_validation_has_not_applicable_source_identity_status(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    set_rows = read_tsv(corpus.output_dir / "assertion_record_source_identity_sets.tsv")
    validation_rows = read_tsv(corpus.output_dir / "assertion_record_validation_report.tsv")
    combined = set_rows + validation_rows

    matching = [
        row for row in combined
        if row.get("source_assertion_registration_id") == "gsc_producer_contract_validation_001"
    ]
    assert matching, "GSC producer_contract_validation assertion must be explicitly accounted for"
    assert any(
        row.get("source_identity_set_status") in {
            "not_applicable",
            "not_applicable_for_source_identity_sets",
        }
        or row.get("validation_status") in {
            "indexed_with_note",
            "not_applicable",
            "not_applicable_for_source_identity_sets",
        }
        for row in matching
    )

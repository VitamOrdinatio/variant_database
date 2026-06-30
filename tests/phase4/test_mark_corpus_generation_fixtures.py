import csv
import json
from collections import Counter
from pathlib import Path

from variant_database.phase4.corpus_generation.manifest import (
    CANONICAL_SELECTION_MANIFEST_COLUMNS,
    load_corpus_generation_selection_manifest,
)


SELECTION_MANIFEST_PATH = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_corpus_6tep_v1_selection_manifest.tsv"
)

POLICY_PATH = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_6tep_certified_input_policy.json"
)

EXPECTED_LABELS = [
    "gsc_epilepsy",
    "gsc_mitochondrial_disease",
    "vap_hg002",
    "vap_median_ERR10619300",
    "vap_q1_ERR10619212",
    "vap_q3_ERR10619225",
]

EXPECTED_PHASE4_1_RECEIPT_REFERENCE = (
    "results/validation/phase4_registration_units/"
    "mark_full_corpus_smoketest_2026_06_30_052739/"
)


def test_mark_phase4_corpus_selection_manifest_loads() -> None:
    manifest = load_corpus_generation_selection_manifest(
        SELECTION_MANIFEST_PATH,
        repo_root=Path("."),
        validate_filesystem=False,
    )

    assert manifest.corpus_generation_id == "mark_phase4_corpus_6tep_v1"
    assert len(manifest.records) == 6
    assert len(manifest.included_records) == 6
    assert len(manifest.excluded_records) == 0
    assert [record.registration_unit_label for record in manifest.records] == (
        EXPECTED_LABELS
    )


def test_mark_phase4_corpus_selection_manifest_uses_canonical_columns() -> None:
    with SELECTION_MANIFEST_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)

    assert tuple(header) == CANONICAL_SELECTION_MANIFEST_COLUMNS


def test_mark_phase4_corpus_selection_manifest_declares_expected_scope() -> None:
    manifest = load_corpus_generation_selection_manifest(
        SELECTION_MANIFEST_PATH,
        repo_root=Path("."),
        validate_filesystem=False,
    )

    producer_counts = Counter(
        record.expected_producer_family for record in manifest.included_records
    )

    assert producer_counts == {"GSC": 2, "VAP": 4}
    assert {
        record.expected_registration_unit_validation_status
        for record in manifest.included_records
    } == {"passed"}
    assert {
        record.expected_registration_unit_certification_status
        for record in manifest.included_records
    } == {"certified"}
    assert {
        record.expected_registration_unit_readiness_status
        for record in manifest.included_records
    } == {"ready"}
    assert {record.expected_backend for record in manifest.included_records} == {
        "sqlite"
    }


def test_mark_phase4_corpus_selection_manifest_preserves_phase4_1_receipt_provenance() -> None:
    manifest = load_corpus_generation_selection_manifest(
        SELECTION_MANIFEST_PATH,
        repo_root=Path("."),
        validate_filesystem=False,
    )

    assert {
        record.phase4_1_validation_receipt_reference
        for record in manifest.included_records
    } == {EXPECTED_PHASE4_1_RECEIPT_REFERENCE}

    assert {
        record.registration_unit_inventory_record_reference
        for record in manifest.included_records
    } == {
        EXPECTED_PHASE4_1_RECEIPT_REFERENCE + "registration_unit_inventory.tsv"
    }

    assert {
        record.registration_unit_readiness_record_reference
        for record in manifest.included_records
    } == {
        EXPECTED_PHASE4_1_RECEIPT_REFERENCE + "registration_unit_readiness.tsv"
    }


def test_mark_phase4_policy_fixture_is_coherent_with_selection_manifest() -> None:
    manifest = load_corpus_generation_selection_manifest(
        SELECTION_MANIFEST_PATH,
        repo_root=Path("."),
        validate_filesystem=False,
    )
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    assert policy["selection_policy_id"] == "mark_phase4_6tep_certified_input_policy"
    assert policy["selection_policy_version"] == "v1"
    assert policy["corpus_generation_id"] == manifest.corpus_generation_id
    assert policy["expected_registration_unit_count"] == len(
        manifest.included_records
    )
    assert policy["expected_registration_unit_labels"] == EXPECTED_LABELS
    assert policy["expected_producer_family_counts"] == {
        "GSC": 2,
        "VAP": 4,
    }


def test_mark_phase4_policy_fixture_preserves_authority_boundary() -> None:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    boundary = policy["authority_boundary"]

    assert boundary["declares_scope"] is True
    assert boundary["interprets_evidence"] is False
    assert boundary["creates_assertion_records"] is False
    assert boundary["derives_topology"] is False
    assert boundary["certifies_corpus_generation"] is False

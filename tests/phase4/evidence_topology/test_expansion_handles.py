"""Tests for Source Identity Set expansion-handle preservation."""
from __future__ import annotations

from pathlib import Path
import csv

from variant_database.phase4.evidence_topology.expansion import (
    EXPANSION_INDEX_FILENAME,
    FORBIDDEN_EXPANDED_SOURCE_IDENTITY_COLUMNS,
    VALIDATION_STATUS_PASSED,
    audit_source_identity_expansion_handles,
    check_by_id,
    failed_checks,
)


TOPOLOGY_OUTPUT_DIR = Path(
    "results/phase4/evidence_topology/"
    "mark_phase4_corpus_6tep_v1_topology_build_v1"
)
ASSERTION_RECORD_DIR = Path(
    "results/phase4/assertion_records/mark_phase4_corpus_6tep_v1"
)


def _audit():
    return audit_source_identity_expansion_handles(
        TOPOLOGY_OUTPUT_DIR,
        ASSERTION_RECORD_DIR,
    )


def _read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def test_canonical_expansion_handle_audit_passes() -> None:
    result = _audit()

    assert result.validation_status == VALIDATION_STATUS_PASSED
    assert failed_checks(result) == ()


def test_expansion_index_references_valid_topology_relationships() -> None:
    result = _audit()
    check = check_by_id(
        result,
        "expansion_relationship_refs_join_to_topology_relationships",
    )

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_source_identity_set_ids_join_to_assertion_surface() -> None:
    result = _audit()
    check = check_by_id(
        result,
        "expansion_source_identity_set_ids_join_to_assertion_surface",
    )

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_source_identity_set_ids_join_to_summary_surface() -> None:
    result = _audit()
    check = check_by_id(
        result,
        "expansion_source_identity_set_ids_join_to_summary_surface",
    )

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_preserves_required_handle_fields() -> None:
    result = _audit()
    check = check_by_id(result, "expansion_handle_required_fields_nonempty")

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_preserves_source_identity_counts() -> None:
    result = _audit()
    check = check_by_id(result, "source_identity_count_preserved_from_assertion_surface")

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_recovers_registration_unit_ids_from_summary() -> None:
    result = _audit()
    check = check_by_id(
        result,
        "registration_unit_id_recovered_from_source_identity_summary",
    )

    assert check.status == VALIDATION_STATUS_PASSED


def test_expansion_index_does_not_contain_expanded_source_identity_values() -> None:
    header, _rows = _read_tsv(TOPOLOGY_OUTPUT_DIR / EXPANSION_INDEX_FILENAME)

    assert not set(FORBIDDEN_EXPANDED_SOURCE_IDENTITY_COLUMNS) & set(header)


def test_expansion_statuses_are_reference_only_for_v1() -> None:
    result = _audit()
    check = check_by_id(result, "expansion_statuses_are_reference_only_v1")

    assert check.status == VALIDATION_STATUS_PASSED
    assert result.summary["by_expansion_status"] == {
        "available_by_source_identity_set_reference": 816,
    }


def test_statistical_testing_status_requires_expansion_for_handles() -> None:
    result = _audit()
    check = check_by_id(
        result,
        "statistical_testing_status_requires_source_identity_expansion",
    )

    assert check.status == VALIDATION_STATUS_PASSED
    assert result.summary["by_statistical_testing_status"] == {
        "requires_source_identity_expansion": 816,
    }


def test_canonical_expansion_handle_summary_matches_expected_counts() -> None:
    result = _audit()

    assert result.summary["expansion_index_row_count"] == 816
    assert result.summary["distinct_source_identity_set_count"] == 204
    assert result.summary["distinct_topology_relationship_count"] == 14
    assert result.summary["represented_source_identity_count_distinct_sets"] == 147941196
    assert result.summary["by_lossiness_status"] == {"lossless_by_reference": 816}


def test_canonical_expansion_handles_preserve_namespace_breakdown() -> None:
    result = _audit()

    namespaces = result.summary["by_source_namespace"]
    joined_namespaces = " ".join(namespaces)

    assert namespaces
    assert "" not in namespaces
    assert sum(namespaces.values()) == 816
    assert "vap_" in joined_namespaces
    assert "gsc_" in joined_namespaces

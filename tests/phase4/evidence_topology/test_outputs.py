"""Tests for deterministic Evidence Topology output artifact emission."""
from __future__ import annotations

import csv
import inspect
import json
from pathlib import Path

from variant_database.phase4.evidence_topology.builder import build_topology_rows
from variant_database.phase4.evidence_topology.outputs import (
    DOWNSTREAM_GEOMETRY_COLUMNS,
    FORBIDDEN_DOWNSTREAM_GEOMETRY_COLUMNS,
    REQUIRED_OUTPUTS,
    write_topology_outputs,
)


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)


def _build_rows():
    signature = inspect.signature(build_topology_rows)
    kwargs = {}
    if "policy_path" in signature.parameters:
        kwargs["policy_path"] = POLICY_PATH
    if "policy" in signature.parameters:
        kwargs["policy"] = POLICY_PATH
    if "repo_root" in signature.parameters:
        kwargs["repo_root"] = Path(".")
    if "assertion_record_dir" in signature.parameters:
        kwargs["assertion_record_dir"] = Path(
            "results/phase4/assertion_records/mark_phase4_corpus_6tep_v1"
        )
    if kwargs:
        return build_topology_rows(**kwargs)
    return build_topology_rows(POLICY_PATH)


def _write_outputs(tmp_path: Path):
    build_result = _build_rows()
    return write_topology_outputs(
        build_result,
        policy=POLICY_PATH,
        output_dir=tmp_path / "topology_outputs",
        repo_root=Path("."),
        build_timestamp_utc="2026-07-06T00:00:00Z",
    )


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_write_topology_outputs_creates_required_artifact_family(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)

    assert result.validation_status == "passed"
    for name in REQUIRED_OUTPUTS:
        path = result.output_dir / name
        assert path.is_file(), name
        assert path.stat().st_size > 0, name


def test_relationship_tsv_and_jsonl_row_counts_match(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    relationship_rows = _read_tsv(result.output_dir / "topology_relationships.tsv")
    jsonl_rows = [
        json.loads(line)
        for line in (result.output_dir / "topology_relationships.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert relationship_rows
    assert len(relationship_rows) == len(jsonl_rows)


def test_members_and_basis_reference_valid_relationship_ids(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    relationship_ids = {
        row["topology_relationship_id"]
        for row in _read_tsv(result.output_dir / "topology_relationships.tsv")
    }
    member_relationship_ids = {
        row["topology_relationship_id"]
        for row in _read_tsv(result.output_dir / "topology_relationship_members.tsv")
    }
    basis_relationship_ids = {
        row["topology_relationship_id"]
        for row in _read_tsv(result.output_dir / "topology_basis_components.tsv")
    }

    assert member_relationship_ids <= relationship_ids
    assert basis_relationship_ids <= relationship_ids
    assert relationship_ids <= member_relationship_ids
    assert relationship_ids <= basis_relationship_ids


def test_manifest_lists_all_required_outputs_with_checksums(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    manifest_rows = _read_tsv(result.output_dir / "topology_build_manifest.tsv")
    names = {row["artifact_name"] for row in manifest_rows}

    assert set(REQUIRED_OUTPUTS) <= names
    for row in manifest_rows:
        assert row["artifact_path"]
        assert row["size_bytes"]
        assert row["validation_status"] == "passed"
        if row["artifact_name"] not in {
            "topology_build_manifest.tsv",
            "topology_build_manifest.json",
        }:
            assert len(row["sha256"]) == 64


def test_expansion_index_contains_source_identity_set_references_without_expansion(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    rows = _read_tsv(result.output_dir / "topology_source_identity_expansion_index.tsv")

    assert rows
    assert all(row["source_identity_set_id"] for row in rows)
    assert "expanded_source_identity_value" not in rows[0]
    assert {
        row["source_identity_expansion_status"]
        for row in rows
    } <= {
        "available_by_source_identity_set_reference",
        "requires_controlled_expansion",
        "deferred_by_policy",
        "not_applicable",
        "not_required",
        "header_only_not_policy_enabled",
    }


def test_namespace_mediation_emits_source_namespace_only_without_canonical_match(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    rows = _read_tsv(result.output_dir / "topology_namespace_mediation.tsv")

    assert rows
    assert "canonical_identity_match" not in {row["match_type"] for row in rows}
    assert "namespace_mediated_match" not in {row["match_type"] for row in rows}
    assert all(not row["canonical_identity_id"] for row in rows)
    assert all(not row["namespace_bridge_id"] for row in rows)


def test_downstream_geometry_manifest_contains_no_geometry_features(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    rows = _read_tsv(result.output_dir / "downstream_geometry_input_manifest.tsv")

    assert rows
    assert not (FORBIDDEN_DOWNSTREAM_GEOMETRY_COLUMNS & set(DOWNSTREAM_GEOMETRY_COLUMNS))
    assert "surface_eligibility" not in rows[0]
    assert "statistical_significance" not in rows[0]
    assert "biological_significance" not in rows[0]


def test_output_order_is_deterministic_across_repeated_writes(tmp_path: Path) -> None:
    first = _write_outputs(tmp_path / "first")
    second = _write_outputs(tmp_path / "second")

    comparable = [
        "topology_relationships.tsv",
        "topology_relationships.jsonl",
        "topology_relationship_members.tsv",
        "topology_basis_components.tsv",
        "topology_source_identity_expansion_index.tsv",
        "topology_namespace_mediation.tsv",
        "topology_metadata_relationships.tsv",
        "topology_summary.tsv",
        "downstream_geometry_input_manifest.tsv",
    ]
    for name in comparable:
        assert (first.output_dir / name).read_text(encoding="utf-8") == (
            second.output_dir / name
        ).read_text(encoding="utf-8")


def test_build_local_validation_report_passes(tmp_path: Path) -> None:
    result = _write_outputs(tmp_path)
    payload = json.loads(
        (result.output_dir / "topology_validation_report.json").read_text(encoding="utf-8")
    )

    assert payload["validation_status"] == "passed"
    assert payload["failed_check_count"] == 0
    assert payload["check_count"] >= 1

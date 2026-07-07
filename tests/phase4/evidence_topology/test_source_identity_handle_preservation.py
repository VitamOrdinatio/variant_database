"""Regression tests for Source Identity Set handle propagation through Step 4."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path

from variant_database.phase4.evidence_topology.builder import build_topology_rows


POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)


def _build_members() -> list[dict[str, object]]:
    result = build_topology_rows(policy_path=POLICY_PATH, repo_root=Path("."))
    return [asdict(row) if is_dataclass(row) else dict(row) for row in result.members]


def test_step4_source_identity_set_members_preserve_handle_metadata() -> None:
    members = _build_members()
    sis_members = [row for row in members if row.get("source_identity_set_id")]

    assert len(sis_members) == 816
    for column in [
        "source_assertion_registration_id",
        "identity_kind",
        "participant_role",
        "source_namespace",
        "source_identity_count",
        "lossiness_status",
        "resolution_status",
        "source_identity_set_status",
    ]:
        assert all(row.get(column) for row in sis_members), column


def test_step4_source_identity_set_members_preserve_distinct_source_identity_sets() -> None:
    members = _build_members()
    sis_members = [row for row in members if row.get("source_identity_set_id")]
    distinct_source_identity_set_ids = {
        str(row["source_identity_set_id"]) for row in sis_members
    }

    assert len(distinct_source_identity_set_ids) == 204
    assert sum(
        int(row["source_identity_count"])
        for row in {row["source_identity_set_id"]: row for row in sis_members}.values()
    ) == 147941196

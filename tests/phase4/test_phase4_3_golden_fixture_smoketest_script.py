from __future__ import annotations

import csv
import json
import os
from pathlib import Path
import subprocess
import sys


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="	"))


def test_phase4_3_layer2_smoketest_enforces_preservation_hardening(tmp_path: Path) -> None:
    script = Path("scripts/validation/run_phase4_3_golden_fixture_assertion_record_smoketest.py")
    fixture = Path(
        "tests/fixtures/phase4/assertion_records/"
        "phase4_3_assertion_record_golden_fixture_2026_07_01_203720"
    )
    assert script.exists()
    assert fixture.exists()

    output_root = tmp_path / "phase4_3d_receipts"
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--fixture",
            str(fixture),
            "--output-root",
            str(output_root),
            "--timestamp",
            "2099_01_01_000000",
        ],
        cwd=Path.cwd(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    receipt = output_root / "golden_fixture_smoketest_2099_01_01_000000"
    assert receipt.exists()
    summary = json.loads((receipt / "validation_summary.json").read_text(encoding="utf-8"))
    assert summary["overall_status"] == "passed"

    check_names = {check["check_name"] for check in summary["checks"]}
    assert "participant_bridge_populated_from_source_identity_sets" in check_names
    assert "source_identity_set_id_join_integrity" in check_names
    assert "preservation_and_resolver_status_are_explicit" in check_names
    assert "artifact_level_lineage_is_explicit" in check_names

    preservation_rows = _read_tsv(receipt / "preservation_hardening_report.tsv")
    assert preservation_rows
    assert {row["status"] for row in preservation_rows} == {"passed"}

    run_a = receipt / "build_outputs" / "run_a"
    index_rows = _read_tsv(run_a / "assertion_record_index.tsv")
    participant_rows = _read_tsv(run_a / "assertion_record_participants.tsv")
    set_rows = _read_tsv(run_a / "assertion_record_source_identity_sets.tsv")
    summary_rows = _read_tsv(run_a / "assertion_record_source_identity_summary.tsv")
    lineage_rows = _read_tsv(run_a / "assertion_record_lineage.tsv")

    assert len(index_rows) == 52
    assert len(participant_rows) == 204
    assert len(set_rows) == 204
    assert len(summary_rows) == 204
    assert len(lineage_rows) == 52

    assert {row["preservation_status"] for row in index_rows} == {"preserved"}
    assert {row["participant_source"] for row in participant_rows} == {"source_identity_set_reference"}
    assert {row["lineage_completeness_status"] for row in lineage_rows} == {
        "artifact_level_lineage_present_row_ref_absent"
    }
    assert {row["source_record_ref_status"] for row in lineage_rows} == {"explicit_absence"}

    set_ids = {row["source_identity_set_id"] for row in set_rows}
    assert {row["source_identity_set_id"] for row in participant_rows} <= set_ids
    assert {row["source_identity_set_id"] for row in summary_rows} <= set_ids

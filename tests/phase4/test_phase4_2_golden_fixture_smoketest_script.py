import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def test_phase4_2_golden_fixture_smoketest_script_runs_in_temp_output(
    tmp_path: Path,
) -> None:
    fixture_root = Path(
        "tests/fixtures/phase4/"
        "phase4_registration_unit_golden_fixture_2026_06_29_155520/"
        "phase4_registration_unit_golden_fixture"
    )
    assert fixture_root.is_dir()

    output_root = tmp_path / "phase4_corpus_generation_validation"

    env = os.environ.copy()
    env["PYTHONPATH"] = "src" + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/validation/run_phase4_2_golden_fixture_corpus_generation_smoketest.py",
            "--fixture-root",
            str(fixture_root),
            "--output-root",
            str(output_root),
            "--build-timestamp",
            "2026-06-30T12:20:00Z",
            "--validation-timestamp",
            "2026-06-30T12:25:00Z",
        ],
        check=False,
        cwd=Path("."),
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr

    receipt_dir = output_root / "golden_fixture_smoketest_2026_06_30_122500"
    summary_path = receipt_dir / "phase4_2_golden_fixture_smoketest_summary.json"

    assert summary_path.is_file()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["smoketest_identity"]["smoketest_status"] == "passed"
    assert summary["smoketest_identity"]["validation_status"] == "passed"
    assert summary["smoketest_identity"]["summary_status"] == "passed"

    assert summary["fixture"]["registration_unit_count"] == 6
    assert summary["fixture"]["registration_unit_labels"] == [
        "gsc_epilepsy",
        "gsc_mitochondrial_disease",
        "vap_hg002",
        "vap_median_ERR10619300",
        "vap_q1_ERR10619212",
        "vap_q3_ERR10619225",
    ]

    assert summary["observed_summary"]["included_registration_unit_count"] == 6
    assert summary["observed_summary"]["excluded_registration_unit_count"] == 0
    assert summary["observed_summary"]["downstream_assertion_record_input_count"] == 6
    assert summary["observed_summary"]["artifact_count_total"] == 82
    assert summary["observed_summary"]["assertion_registration_count_total"] == 52
    assert summary["observed_summary"]["source_identity_count_total"] == 1651
    assert summary["observed_summary"]["producer_family_distribution"] == {
        "GSC": 2,
        "VAP": 4,
    }
    assert summary["observed_summary"]["failed_check_count"] == 0

    assert summary["authority_boundary"]["uses_mark_full_corpus_data"] is False
    assert summary["authority_boundary"]["uses_compressed_real_row_fixture"] is True
    assert summary["authority_boundary"]["opens_fixture_sqlite_read_only"] is True
    assert summary["authority_boundary"]["mutates_registration_units"] is False
    assert summary["authority_boundary"]["creates_assertion_records"] is False
    assert summary["authority_boundary"]["derives_topology"] is False

    archive_path = (
        output_root
        / "receipt_archives"
        / "golden_fixture_smoketest_2026_06_30_122500.tgz"
    )
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")

    assert archive_path.is_file()
    assert checksum_path.is_file()

    observed_digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_text = checksum_path.read_text(encoding="utf-8").strip()

    assert checksum_text == (
        f"{observed_digest}  golden_fixture_smoketest_2026_06_30_122500.tgz"
    )

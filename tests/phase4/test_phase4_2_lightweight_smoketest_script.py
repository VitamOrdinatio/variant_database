import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def test_phase4_2_lightweight_smoketest_script_runs_in_temp_output(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "phase4_corpus_generation_validation"

    env = os.environ.copy()
    env["PYTHONPATH"] = "src" + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/validation/run_phase4_2_lightweight_corpus_generation_smoketest.py",
            "--output-root",
            str(output_root),
            "--build-timestamp",
            "2026-06-30T12:10:00Z",
            "--validation-timestamp",
            "2026-06-30T12:15:00Z",
        ],
        check=False,
        cwd=Path("."),
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr

    receipt_dir = output_root / "lightweight_fixture_smoketest_2026_06_30_121500"
    summary_path = receipt_dir / "phase4_2_lightweight_smoketest_summary.json"

    assert summary_path.is_file()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["smoketest_identity"]["smoketest_status"] == "passed"
    assert summary["smoketest_identity"]["validation_status"] == "passed"
    assert summary["smoketest_identity"]["summary_status"] == "passed"

    assert summary["observed_summary"]["included_registration_unit_count"] == 2
    assert summary["observed_summary"]["excluded_registration_unit_count"] == 1
    assert summary["observed_summary"]["downstream_assertion_record_input_count"] == 2
    assert summary["observed_summary"]["artifact_count_total"] == 25
    assert summary["observed_summary"]["assertion_registration_count_total"] == 16
    assert summary["observed_summary"]["source_identity_count_total"] == 300
    assert summary["observed_summary"]["failed_check_count"] == 0

    assert summary["authority_boundary"]["uses_mark_data"] is False
    assert summary["authority_boundary"]["opens_sqlite"] is False
    assert summary["authority_boundary"]["creates_assertion_records"] is False
    assert summary["authority_boundary"]["derives_topology"] is False

    archive_path = (
        output_root
        / "receipt_archives"
        / "lightweight_fixture_smoketest_2026_06_30_121500.tgz"
    )
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")

    assert archive_path.is_file()
    assert checksum_path.is_file()

    observed_digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_text = checksum_path.read_text(encoding="utf-8").strip()

    assert checksum_text == (
        f"{observed_digest}  lightweight_fixture_smoketest_2026_06_30_121500.tgz"
    )

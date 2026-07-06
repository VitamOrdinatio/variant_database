"""Tests for the canonical Evidence Topology build script.

These tests exercise the operator script through temporary output directories.
They must not write to the canonical results/phase4/evidence_topology location.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from variant_database.phase4.evidence_topology.outputs import REQUIRED_OUTPUTS


SCRIPT_PATH = Path("scripts/dev/phase4/build_mark_phase4_evidence_topology.py")


def _load_script_module():
    spec = importlib.util.spec_from_file_location(
        "build_mark_phase4_evidence_topology", SCRIPT_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_canonical_build_script_exists_and_exposes_entry_points() -> None:
    module = _load_script_module()

    assert SCRIPT_PATH.is_file()
    assert callable(module.run_canonical_build)
    assert callable(module.main)
    assert module.DEFAULT_OUTPUT_DIR == Path(
        "results/phase4/evidence_topology/"
        "mark_phase4_corpus_6tep_v1_topology_build_v1"
    )


def test_run_canonical_build_writes_required_outputs_to_temp_dir(tmp_path: Path) -> None:
    module = _load_script_module()
    output_dir = tmp_path / "canonical_emit"

    result = module.run_canonical_build(
        repo_root=Path("."),
        output_dir=output_dir,
        build_timestamp_utc="2026-07-06T00:00:00Z",
    )

    assert result.validation_status == "passed"
    assert result.output_dir == output_dir.resolve()
    for name in REQUIRED_OUTPUTS:
        path = output_dir / name
        assert path.is_file(), name
        assert path.stat().st_size > 0, name

    manifest = _read_json(output_dir / "topology_build_manifest.json")
    assert manifest["validation_status"] == "passed"
    assert manifest["artifact_count"] == len(REQUIRED_OUTPUTS)


def test_run_canonical_build_refuses_nonempty_output_without_overwrite(tmp_path: Path) -> None:
    module = _load_script_module()
    output_dir = tmp_path / "canonical_emit"
    output_dir.mkdir()
    sentinel = output_dir / "sentinel.txt"
    sentinel.write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(FileExistsError):
        module.run_canonical_build(repo_root=Path("."), output_dir=output_dir)

    assert sentinel.read_text(encoding="utf-8") == "do not overwrite"


def test_run_canonical_build_overwrite_replaces_existing_output(tmp_path: Path) -> None:
    module = _load_script_module()
    output_dir = tmp_path / "canonical_emit"
    output_dir.mkdir()
    sentinel = output_dir / "sentinel.txt"
    sentinel.write_text("replace me", encoding="utf-8")

    result = module.run_canonical_build(
        repo_root=Path("."),
        output_dir=output_dir,
        overwrite=True,
        build_timestamp_utc="2026-07-06T00:00:00Z",
    )

    assert result.validation_status == "passed"
    assert not sentinel.exists()
    assert (output_dir / "topology_validation_report.tsv").is_file()


def test_cli_main_writes_temp_output_and_reports_success(tmp_path: Path, capsys) -> None:
    module = _load_script_module()
    output_dir = tmp_path / "cli_emit"

    exit_code = module.main(
        [
            "--repo-root",
            ".",
            "--output-dir",
            str(output_dir),
            "--build-timestamp-utc",
            "2026-07-06T00:00:00Z",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Evidence Topology canonical build complete" in captured.out
    assert "validation_status: passed" in captured.out
    assert (output_dir / "downstream_geometry_input_manifest.tsv").is_file()


def test_cli_json_summary_is_parseable(tmp_path: Path, capsys) -> None:
    module = _load_script_module()
    output_dir = tmp_path / "cli_json_emit"

    exit_code = module.main(
        [
            "--repo-root",
            ".",
            "--output-dir",
            str(output_dir),
            "--build-timestamp-utc",
            "2026-07-06T00:00:00Z",
            "--json",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["validation_status"] == "passed"
    assert payload["artifact_count"] == len(REQUIRED_OUTPUTS)
    assert Path(payload["output_dir"]) == output_dir.resolve()

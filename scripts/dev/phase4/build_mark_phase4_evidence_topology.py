#!/usr/bin/env python3
"""Build canonical Phase 4.4 Evidence Topology artifacts.

This script materializes the MARK Phase 4 VAP/GSC Evidence Topology build from
repo-local governed Assertion Record artifacts. It is an operator-facing wrapper
around the library implementation. It does not parse raw producer artifacts,
open Registration Unit SQLite files, expand Source Identity Sets, compute
Convergence Geometry, emit Projection Views, or perform RDGP reasoning.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Sequence

from variant_database.phase4.evidence_topology.outputs import REQUIRED_OUTPUTS


DEFAULT_POLICY_PATH = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v1.json"
)

DEFAULT_OUTPUT_DIR = Path(
    "results/phase4/evidence_topology/"
    "mark_phase4_corpus_6tep_v1_topology_build_v1"
)


def resolve_repo_root(repo_root: str | Path | None = None) -> Path:
    """Return the repository root used for canonical topology materialization."""

    if repo_root is not None:
        return Path(repo_root).expanduser().resolve()
    # scripts/dev/phase4/<this file>.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    """Resolve a path relative to repo root unless already absolute."""

    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def directory_is_nonempty(path: Path) -> bool:
    """Return whether ``path`` exists as a non-empty directory."""

    return path.is_dir() and any(path.iterdir())


def run_canonical_build(
    *,
    repo_root: str | Path | None = None,
    policy_path: str | Path = DEFAULT_POLICY_PATH,
    output_dir: str | Path | None = None,
    overwrite: bool = False,
    build_timestamp_utc: str | None = None,
) -> Any:
    """Materialize the canonical Phase 4.4 Evidence Topology output family.

    Parameters
    ----------
    repo_root:
        Repository root. Defaults to the root inferred from this script path.
    policy_path:
        Active Evidence Topology derivation policy path.
    output_dir:
        Output directory. Defaults to the canonical Phase 4.4 topology results
        directory declared by VDB governance.
    overwrite:
        If false, fail when the output directory already exists and is non-empty.
        If true, remove the existing output directory before writing.
    build_timestamp_utc:
        Optional deterministic timestamp for tests or reproducible local checks.
    """

    repo = resolve_repo_root(repo_root)
    policy_file = resolve_repo_path(repo, policy_path)
    destination = resolve_repo_path(repo, output_dir or DEFAULT_OUTPUT_DIR)

    if not policy_file.is_file():
        raise FileNotFoundError(f"Topology policy file not found: {policy_file}")

    if directory_is_nonempty(destination):
        if not overwrite:
            raise FileExistsError(
                "Evidence Topology output directory already exists and is non-empty: "
                f"{destination}. Re-run with --overwrite to replace it."
            )
        shutil.rmtree(destination)

    from variant_database.phase4.evidence_topology.builder import (
        write_topology_outputs_for_build,
    )

    result = write_topology_outputs_for_build(
        policy_path=policy_file,
        output_dir=destination,
        repo_root=repo,
        build_timestamp_utc=build_timestamp_utc,
    )

    missing = [name for name in REQUIRED_OUTPUTS if not (destination / name).is_file()]
    if missing:
        raise RuntimeError(
            "Canonical Evidence Topology build did not emit required outputs: "
            + ", ".join(missing)
        )

    if getattr(result, "validation_status", "") != "passed":
        raise RuntimeError(
            "Canonical Evidence Topology build emitted artifacts, but build-local "
            f"validation status was {getattr(result, 'validation_status', '<missing>')!r}."
        )

    return result


def result_summary(result: Any) -> dict[str, Any]:
    """Return a concise JSON-serializable operator summary."""

    output_dir = Path(getattr(result, "output_dir"))
    artifact_paths = getattr(result, "artifact_paths", {}) or {}
    return {
        "topology_build_id": getattr(result, "topology_build_id", ""),
        "validation_status": getattr(result, "validation_status", ""),
        "output_dir": str(output_dir),
        "artifact_count": len(artifact_paths),
        "required_output_count": len(REQUIRED_OUTPUTS),
        "topology_validation_report": str(output_dir / "topology_validation_report.tsv"),
        "topology_summary": str(output_dir / "topology_summary.tsv"),
        "downstream_geometry_input_manifest": str(
            output_dir / "downstream_geometry_input_manifest.tsv"
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Materialize canonical Phase 4.4 Evidence Topology artifacts."
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root. Defaults to the root inferred from this script path.",
    )
    parser.add_argument(
        "--policy-path",
        default=str(DEFAULT_POLICY_PATH),
        help="Evidence Topology derivation policy path, relative to repo root unless absolute.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory, relative to repo root unless absolute.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing non-empty output directory.",
    )
    parser.add_argument(
        "--build-timestamp-utc",
        default=None,
        help="Optional build timestamp override. Intended for tests/reproducible checks.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the operator summary as JSON.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = run_canonical_build(
            repo_root=args.repo_root,
            policy_path=args.policy_path,
            output_dir=args.output_dir,
            overwrite=args.overwrite,
            build_timestamp_utc=args.build_timestamp_utc,
        )
    except Exception as exc:  # pragma: no cover - exercised by operator failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    summary = result_summary(result)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("Evidence Topology canonical build complete")
        print(f"  topology_build_id: {summary['topology_build_id']}")
        print(f"  validation_status: {summary['validation_status']}")
        print(f"  output_dir: {summary['output_dir']}")
        print(f"  artifact_count: {summary['artifact_count']}")
        print(f"  topology_summary: {summary['topology_summary']}")
        print(
            "  downstream_geometry_input_manifest: "
            f"{summary['downstream_geometry_input_manifest']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

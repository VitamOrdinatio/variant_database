#!/usr/bin/env python3
"""Register the two canonical GSC TEPs into parallel local VDB databases.

Local operator script only.

This runner resolves the canonical epilepsy and mitochondrial-disease GSC TEPs,
registers each package independently, and writes new SQLite databases beneath a
dedicated output root.

The script:

- never overwrites an existing SQLite output unless --overwrite is supplied
- verifies required GSC artifacts before registration
- fingerprints each resolved source package before and after registration
- fails if registration mutates the source package
- keeps the historical results/registration/gsc baselines untouched
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from variant_database.ingestion.tep_package_resolver import (
    resolve_gsc_tep_package,
)
from variant_database.registration.registration_orchestrator import (
    run_registration_pipeline,
)


DEFAULT_GSC_REPO_ROOT = (
    Path.home()
    / "dev/portfolio_projects/gene_set_consensus"
)

DEFAULT_OUTPUT_ROOT = Path(
    "results/registration/genotype_discovery_3tep"
)

GSC_TEP_RELATIVE_PATHS = {
    "gsc_epilepsy": Path(
        "results/teps/gsc/epilepsy_semantic_gtr_experimental/"
        "run_2026_06_22_184534/gsc_tep.json"
    ),
    "gsc_mitochondrial_disease": Path(
        "results/teps/gsc/mitochondrial_semantic_gtr_experimental/"
        "run_2026_06_23_015533/gsc_tep.json"
    ),
}


def parse_args() -> argparse.Namespace:
    """Parse local operator arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Register the canonical epilepsy and mitochondrial-disease "
            "GSC TEPs into separate local VDB SQLite databases."
        )
    )
    parser.add_argument(
        "--gsc-repo-root",
        type=Path,
        default=DEFAULT_GSC_REPO_ROOT,
        help=(
            "Path to the gene_set_consensus repository. "
            f"Default: {DEFAULT_GSC_REPO_ROOT}"
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=(
            "Root beneath which the two registration databases are written. "
            f"Default: {DEFAULT_OUTPUT_ROOT}"
        ),
    )
    parser.add_argument(
        "--max-rows-per-artifact",
        type=int,
        default=None,
        help=(
            "Optional canary row limit passed to the registration pipeline. "
            "Omit for complete registration."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Delete an existing target SQLite database and its standard "
            "sidecars before registration."
        ),
    )
    return parser.parse_args()


def sqlite_family(db_path: Path) -> tuple[Path, ...]:
    """Return the target SQLite file and its standard sidecar paths."""
    return (
        db_path,
        Path(f"{db_path}-wal"),
        Path(f"{db_path}-shm"),
        Path(f"{db_path}-journal"),
    )


def prepare_output_database(
    db_path: Path,
    *,
    overwrite: bool,
) -> None:
    """Prepare one output path without touching unrelated files."""
    existing = [
        path
        for path in sqlite_family(db_path)
        if path.exists()
    ]

    if existing and not overwrite:
        rendered = ", ".join(str(path) for path in existing)
        raise FileExistsError(
            "Refusing to overwrite existing SQLite output. "
            "Use --overwrite only when replacement is intentional: "
            f"{rendered}"
        )

    if overwrite:
        for path in existing:
            path.unlink()

    db_path.parent.mkdir(parents=True, exist_ok=True)


def tree_fingerprint(
    root: Path,
) -> tuple[tuple[str, int, int], ...]:
    """Capture source-tree path, size, and modification-time state."""
    if not root.is_dir():
        raise NotADirectoryError(
            f"Resolved GSC registration root is not a directory: {root}"
        )

    return tuple(
        sorted(
            (
                str(path.relative_to(root)),
                path.stat().st_size,
                path.stat().st_mtime_ns,
            )
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def summary_value(
    summary: Any,
    field_name: str,
    default: object = "n/a",
) -> object:
    """Read a registration summary field defensively for operator output."""
    return getattr(summary, field_name, default)


def register_gsc_package(
    *,
    label: str,
    tep_json_path: Path,
    gsc_repo_root: Path,
    output_root: Path,
    max_rows_per_artifact: int | None,
    overwrite: bool,
) -> None:
    """Resolve, register, and report one canonical GSC package."""
    if not tep_json_path.is_file():
        raise FileNotFoundError(
            f"Missing canonical GSC TEP descriptor: {tep_json_path}"
        )

    resolved = resolve_gsc_tep_package(
        tep_json_path=tep_json_path,
        producer_repo_root=gsc_repo_root,
    )

    if resolved.missing_required_artifact_ids:
        raise RuntimeError(
            f"{label} is missing required artifacts: "
            f"{resolved.missing_required_artifact_ids}"
        )

    registration_root = (
        Path(resolved.registration_root)
        .expanduser()
        .resolve()
    )

    db_path = output_root / label / "vdb.sqlite"

    prepare_output_database(
        db_path,
        overwrite=overwrite,
    )

    source_before = tree_fingerprint(
        registration_root
    )

    summary = run_registration_pipeline(
        package_path=resolved.registration_root,
        db_path=db_path,
        producer_family="GSC",
        max_rows_per_artifact=max_rows_per_artifact,
    )

    source_after = tree_fingerprint(
        registration_root
    )

    if source_before != source_after:
        raise RuntimeError(
            "Source package mutation detected during registration: "
            f"{label}"
        )

    print("=" * 80)
    print(f"GSC registration complete: {label}")
    print(f"TEP descriptor: {tep_json_path}")
    print(f"TEP ID: {resolved.tep_id}")
    print(f"Phenotype: {resolved.phenotype}")
    print(f"Registration root: {summary.package_path}")
    print(f"Database: {summary.db_path}")
    print(f"Producer family: {summary.producer_family}")
    print(f"Package exists: {summary.package_exists}")
    print(f"Package ID: {summary.package_id}")
    print(f"Artifacts: {summary.artifact_count}")
    print(
        "Assertion registrations: "
        f"{summary.assertion_registration_count}"
    )
    print(
        "Package metadata records: "
        f"{summary_value(summary, 'package_metadata_count')}"
    )
    print(
        "Coordinate declarations: "
        f"{summary_value(summary, 'coordinate_declaration_count')}"
    )
    print(
        "Feature declarations: "
        f"{summary_value(summary, 'feature_declaration_count')}"
    )
    print(f"Rows scanned: {summary.row_count_scanned}")
    print(
        "Participants discovered: "
        f"{summary.participant_count_discovered}"
    )
    print(
        "Source identities: "
        f"{summary.source_identity_count}"
    )
    print(
        "Elapsed seconds: "
        f"{summary.elapsed_seconds:.2f}"
    )
    print(
        "Rows/sec: "
        f"{summary.rows_per_second:.2f}"
    )
    print(
        "Participants/sec: "
        f"{summary.participants_per_second:.2f}"
    )
    print("Source package mutated: False")


def main() -> int:
    """Register both canonical GSC TEPs."""
    args = parse_args()

    gsc_repo_root = (
        args.gsc_repo_root
        .expanduser()
        .resolve()
    )
    output_root = args.output_root.expanduser()

    if not gsc_repo_root.is_dir():
        raise NotADirectoryError(
            f"GSC repository root not found: {gsc_repo_root}"
        )

    for label, relative_path in GSC_TEP_RELATIVE_PATHS.items():
        register_gsc_package(
            label=label,
            tep_json_path=gsc_repo_root / relative_path,
            gsc_repo_root=gsc_repo_root,
            output_root=output_root,
            max_rows_per_artifact=args.max_rows_per_artifact,
            overwrite=args.overwrite,
        )

    print("=" * 80)
    print("Double-GSC registration complete")
    print(f"Output root: {output_root}")
    print(f"Package count: {len(GSC_TEP_RELATIVE_PATHS)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

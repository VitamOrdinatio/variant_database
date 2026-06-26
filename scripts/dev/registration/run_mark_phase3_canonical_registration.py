"""Run MARK Phase 3 canonical registration smoke test.

Targets:
- 4 canonical VAP TEPs: HG002, q1, median, q3
- 2 canonical GSC TEPs: epilepsy, mitochondrial disease

Development/MARK validation script only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from variant_database.ingestion.tep_package_resolver import resolve_gsc_tep_package
from variant_database.registration.registration_orchestrator import (
    RegistrationPipelineSummary,
    run_registration_pipeline,
)


VAP_REPO_ROOT = Path.home() / "dev/portfolio_projects/variant_annotation_pipeline"
GSC_REPO_ROOT = Path.home() / "dev/portfolio_projects/gene_set_consensus"

OUTPUT_ROOT = Path("results/registration/mark_phase3_canonical")


@dataclass(frozen=True)
class RegistrationTarget:
    label: str
    producer_family: str
    package_path: Path
    db_path: Path
    tep_id: str | None = None
    phenotype: str | None = None


VAP_RUNS = {
    "vap_hg002": {
        "sample_id": "HG002",
        "run_id": "run_2026_06_03_010030",
    },
    "vap_q1_ERR10619212": {
        "sample_id": "ERR10619212",
        "run_id": "run_2026_05_30_214724",
    },
    "vap_median_ERR10619300": {
        "sample_id": "ERR10619300",
        "run_id": "run_2026_05_27_172531",
    },
    "vap_q3_ERR10619225": {
        "sample_id": "ERR10619225",
        "run_id": "run_2026_05_31_091242",
    },
}

GSC_TEPS = {
    "gsc_epilepsy": GSC_REPO_ROOT
    / "results/teps/gsc/epilepsy_semantic_gtr_experimental"
    / "run_2026_06_22_184534/gsc_tep.json",
    "gsc_mitochondrial_disease": GSC_REPO_ROOT
    / "results/teps/gsc/mitochondrial_semantic_gtr_experimental"
    / "run_2026_06_23_015533/gsc_tep.json",
}


def _delete_existing_sqlite(db_path: Path) -> None:
    for path in db_path.parent.glob(f"{db_path.name}*"):
        path.unlink()


def _find_vap_tep_directory(sample_id: str, run_id: str) -> Path:
    """Find one canonical VAP TEP directory for sample/run ID."""
    run_dir = VAP_REPO_ROOT / "results" / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"VAP run directory not found: {run_dir}")

    candidates = [
        path
        for path in run_dir.rglob(f"*{sample_id}*{run_id}*")
        if path.is_dir() and path.name.startswith("vap_tep_")
    ]

    non_emulation_candidates = [
        path
        for path in candidates
        if "emulation" not in str(path).lower()
    ]

    selected = non_emulation_candidates or candidates

    if len(selected) != 1:
        raise RuntimeError(
            "Expected exactly one VAP TEP directory for "
            f"sample_id={sample_id!r}, run_id={run_id!r}; "
            f"found {len(selected)}: {[str(path) for path in selected]}"
        )

    return selected[0]


def _build_targets() -> list[RegistrationTarget]:
    targets: list[RegistrationTarget] = []

    for label, config in VAP_RUNS.items():
        package_path = _find_vap_tep_directory(
            sample_id=config["sample_id"],
            run_id=config["run_id"],
        )

        targets.append(
            RegistrationTarget(
                label=label,
                producer_family="VAP",
                package_path=package_path,
                db_path=OUTPUT_ROOT / label / "vdb.sqlite",
            )
        )

    for label, tep_json_path in GSC_TEPS.items():
        resolved = resolve_gsc_tep_package(
            tep_json_path=tep_json_path,
            producer_repo_root=GSC_REPO_ROOT,
        )

        if resolved.missing_required_artifact_ids:
            raise RuntimeError(
                f"{label} missing required artifacts: "
                f"{resolved.missing_required_artifact_ids}"
            )

        targets.append(
            RegistrationTarget(
                label=label,
                producer_family="GSC",
                package_path=Path(resolved.registration_root),
                db_path=OUTPUT_ROOT / label / "vdb.sqlite",
                tep_id=resolved.tep_id,
                phenotype=resolved.phenotype,
            )
        )

    return targets


def _print_summary_row(
    target: RegistrationTarget,
    summary: RegistrationPipelineSummary,
) -> None:
    print(
        "\t".join(
            [
                target.label,
                target.producer_family,
                str(summary.artifact_count),
                str(summary.assertion_registration_count),
                str(summary.row_count_scanned),
                str(summary.participant_count_discovered),
                str(summary.source_identity_count),
                f"{summary.elapsed_seconds:.2f}",
                f"{summary.rows_per_second:.2f}",
                f"{summary.participants_per_second:.2f}",
                str(summary.db_path),
            ]
        )
    )


def main() -> int:
    targets = _build_targets()

    print("MARK Phase 3 canonical registration targets")
    print("=" * 80)
    for target in targets:
        print(f"{target.label}: {target.package_path}")

    print("\nRunning registration")
    print("=" * 80)
    print(
        "\t".join(
            [
                "label",
                "producer",
                "artifacts",
                "assertions",
                "rows",
                "participants",
                "source_identities",
                "elapsed_sec",
                "rows_per_sec",
                "participants_per_sec",
                "db_path",
            ]
        )
    )

    for target in targets:
        target.db_path.parent.mkdir(parents=True, exist_ok=True)
        _delete_existing_sqlite(target.db_path)

        summary = run_registration_pipeline(
            package_path=target.package_path,
            db_path=target.db_path,
            producer_family=target.producer_family,
        )

        _print_summary_row(target, summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

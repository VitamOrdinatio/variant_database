"""Run VDB registration against local canonical GSC TEPs."""

from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.tep_package_resolver import resolve_gsc_tep_package
from variant_database.registration.registration_orchestrator import (
    run_registration_pipeline,
)


GSC_REPO_ROOT = Path.home() / "dev/portfolio_projects/gene_set_consensus"

GSC_TEPS = {
    "epilepsy": GSC_REPO_ROOT / "results/teps/gsc/epilepsy_semantic_gtr_experimental/run_2026_06_22_184534/gsc_tep.json",
    "mitochondrial_disease": GSC_REPO_ROOT / "results/teps/gsc/mitochondrial_semantic_gtr_experimental/run_2026_06_23_015533/gsc_tep.json",
}


def main() -> int:
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

        summary = run_registration_pipeline(
            package_path=resolved.registration_root,
            db_path=Path("results/registration/gsc") / label / "vdb.sqlite",
            producer_family="GSC",
            #max_rows_per_artifact=100,
        )

        print("=" * 80)
        print(f"GSC registration complete: {label}")
        print(f"TEP ID: {resolved.tep_id}")
        print(f"Phenotype: {resolved.phenotype}")
        print(f"Registration root: {summary.package_path}")
        print(f"Database: {summary.db_path}")
        print(f"Artifacts: {summary.artifact_count}")
        print(f"Assertion registrations: {summary.assertion_registration_count}")
        print(f"Rows scanned: {summary.row_count_scanned}")
        print(f"Participants discovered: {summary.participant_count_discovered}")
        print(f"Source identities: {summary.source_identity_count}")
        print(f"Elapsed seconds: {summary.elapsed_seconds:.2f}")
        print(f"Rows/sec: {summary.rows_per_second:.2f}")
        print(f"Participants/sec: {summary.participants_per_second:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

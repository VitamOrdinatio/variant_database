"""Resolve canonical local GSC TEPs.

Development script only.

This validates that VDB can resolve reference-based GSC TEP packages without
flattening the transport envelope or ignoring authoritative producer outputs.
"""

from __future__ import annotations

from pathlib import Path

from variant_database.ingestion.tep_package_resolver import (
    resolve_gsc_tep_package,
)


GSC_REPO_ROOT = Path.home() / "dev/portfolio_projects/gene_set_consensus"

GSC_TEPS = {
    "epilepsy": GSC_REPO_ROOT
    / "results/teps/gsc/epilepsy_semantic_gtr_experimental"
    / "run_2026_06_22_184534/gsc_tep.json",
    "mitochondrial_disease": GSC_REPO_ROOT
    / "results/teps/gsc/mitochondrial_semantic_gtr_experimental"
    / "run_2026_06_23_015533/gsc_tep.json",
}


def main() -> int:
    for label, tep_json_path in GSC_TEPS.items():
        resolved = resolve_gsc_tep_package(
            tep_json_path=tep_json_path,
            producer_repo_root=GSC_REPO_ROOT,
        )

        print("=" * 80)
        print(f"GSC TEP: {label}")
        print(f"TEP ID: {resolved.tep_id}")
        print(f"Package ID: {resolved.package_id}")
        print(f"Release ID: {resolved.release_id}")
        print(f"Run ID: {resolved.run_id}")
        print(f"Phenotype: {resolved.phenotype}")
        print(f"Transport envelope: {resolved.transport_envelope_path}")
        print(f"Authoritative root: {resolved.authoritative_root}")
        print(f"Registration root: {resolved.registration_root}")
        print(f"Resolved artifacts: {len(resolved.resolved_artifacts)}")
        print(f"Missing required: {resolved.missing_required_artifact_ids}")
        print(f"Missing recommended: {resolved.missing_recommended_artifact_ids}")

        print("\nArtifacts:")
        for artifact in resolved.resolved_artifacts:
            status = "OK" if artifact.exists else "MISSING"
            requirement = (
                "required"
                if artifact.required
                else "recommended"
                if artifact.recommended
                else "declared"
            )
            print(
                f"  [{status}] {artifact.artifact_id} "
                f"({requirement}, {artifact.semantic_role})"
            )
            print(f"       {artifact.resolved_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

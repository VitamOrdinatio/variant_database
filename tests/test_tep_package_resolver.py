from __future__ import annotations

import json
from pathlib import Path

from variant_database.ingestion.tep_package_resolver import (
    resolve_gsc_tep_package,
)


def _write_minimal_gsc_tep(
    repo_root: Path,
    run_id: str = "run_2026_06_23_015533",
    package_id: str = "mitochondrial_semantic_gtr_experimental",
) -> Path:
    run_dir = repo_root / "results" / "runs" / run_id
    tables_dir = run_dir / "tables" / package_id
    reports_dir = run_dir / "reports" / package_id

    tables_dir.mkdir(parents=True)
    reports_dir.mkdir(parents=True)

    for path in [
        tables_dir / "consensus_gene_set.tsv",
        tables_dir / "gene_provenance.tsv",
        tables_dir / "source_contributions.tsv",
        tables_dir / "gene_source_matrix.tsv",
        tables_dir / "gene_frequency_table.tsv",
        reports_dir / "final_run_manifest.yaml",
        reports_dir / "output_contract_validation.tsv",
        reports_dir / "validation_report.md",
    ]:
        path.write_text("x\n", encoding="utf-8")

    tep_path = (
        repo_root
        / "results"
        / "teps"
        / "gsc"
        / package_id
        / run_id
        / "gsc_tep.json"
    )
    tep_path.parent.mkdir(parents=True)

    artifact_specs = [
        ("consensus_gene_set", tables_dir / "consensus_gene_set.tsv", "primary_semantic_prior_table", "tsv"),
        ("gene_provenance", tables_dir / "gene_provenance.tsv", "source_provenance_table", "tsv"),
        ("source_contributions", tables_dir / "source_contributions.tsv", "source_contribution_topology", "tsv"),
        ("gene_source_matrix", tables_dir / "gene_source_matrix.tsv", "source_gene_relationship_table", "tsv"),
        ("gene_frequency_table", tables_dir / "gene_frequency_table.tsv", "aggregation_support_table", "tsv"),
        ("final_run_manifest", reports_dir / "final_run_manifest.yaml", "authoritative_finalized_run_context", "yaml"),
        ("output_contract_validation", reports_dir / "output_contract_validation.tsv", "output_contract_validation", "tsv"),
        ("validation_report", reports_dir / "validation_report.md", "human_readable_validation_report", "md"),
    ]

    payload = {
        "envelope": {
            "tep_type": "gsc_tep",
            "tep_id": "gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1",
            "source_package_id": package_id,
            "source_release_id": f"{package_id}_v0.1",
            "source_run_id": run_id,
            "source_phenotype": "mitochondrial_disease",
            "source_authoritative_run_directory": f"results/runs/{run_id}",
        },
        "manifest": {
            "authoritative_run_directory": f"results/runs/{run_id}",
            "release_id": f"{package_id}_v0.1",
            "run_id": run_id,
            "artifacts": [
                {
                    "artifact_id": artifact_id,
                    "artifact_path": str(path.relative_to(repo_root)),
                    "semantic_role": semantic_role,
                    "artifact_type": artifact_type,
                }
                for artifact_id, path, semantic_role, artifact_type in artifact_specs
            ],
        },
    }

    tep_path.write_text(json.dumps(payload), encoding="utf-8")
    return tep_path


def test_resolve_gsc_tep_package_preserves_transport_and_authoritative_roots(
    tmp_path: Path,
) -> None:
    tep_path = _write_minimal_gsc_tep(tmp_path)

    resolved = resolve_gsc_tep_package(
        tep_json_path=tep_path,
        producer_repo_root=tmp_path,
    )

    assert resolved.producer_family == "GSC"
    assert resolved.tep_type == "gsc_tep"
    assert resolved.package_id == "mitochondrial_semantic_gtr_experimental"
    assert resolved.release_id == "mitochondrial_semantic_gtr_experimental_v0.1"
    assert resolved.run_id == "run_2026_06_23_015533"
    assert resolved.phenotype == "mitochondrial_disease"
    assert resolved.transport_envelope_path == str(tep_path.resolve())
    assert resolved.authoritative_root.endswith("results/runs/run_2026_06_23_015533")
    assert resolved.registration_root == resolved.authoritative_root


def test_resolve_gsc_tep_package_resolves_artifacts(tmp_path: Path) -> None:
    tep_path = _write_minimal_gsc_tep(tmp_path)

    resolved = resolve_gsc_tep_package(
        tep_json_path=tep_path,
        producer_repo_root=tmp_path,
    )

    artifacts = {artifact.artifact_id: artifact for artifact in resolved.resolved_artifacts}

    assert artifacts["consensus_gene_set"].required is True
    assert artifacts["consensus_gene_set"].exists is True
    assert artifacts["source_contributions"].required is True
    assert artifacts["gene_source_matrix"].recommended is True
    assert artifacts["validation_report"].recommended is True
    assert resolved.missing_required_artifact_ids == []
    assert resolved.missing_recommended_artifact_ids == []


def test_resolve_gsc_tep_package_reports_missing_required_artifact(
    tmp_path: Path,
) -> None:
    tep_path = _write_minimal_gsc_tep(tmp_path)
    (
        tmp_path
        / "results"
        / "runs"
        / "run_2026_06_23_015533"
        / "tables"
        / "mitochondrial_semantic_gtr_experimental"
        / "source_contributions.tsv"
    ).unlink()

    resolved = resolve_gsc_tep_package(
        tep_json_path=tep_path,
        producer_repo_root=tmp_path,
    )

    assert resolved.missing_required_artifact_ids == ["source_contributions"]


def test_resolve_gsc_tep_package_reports_missing_recommended_artifact(
    tmp_path: Path,
) -> None:
    tep_path = _write_minimal_gsc_tep(tmp_path)
    (
        tmp_path
        / "results"
        / "runs"
        / "run_2026_06_23_015533"
        / "reports"
        / "mitochondrial_semantic_gtr_experimental"
        / "validation_report.md"
    ).unlink()

    resolved = resolve_gsc_tep_package(
        tep_json_path=tep_path,
        producer_repo_root=tmp_path,
    )

    assert resolved.missing_required_artifact_ids == []
    assert resolved.missing_recommended_artifact_ids == ["validation_report"]

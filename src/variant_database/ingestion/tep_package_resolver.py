"""TEP package resolution.

TEP package resolution normalizes producer TEP arrival shapes into explicit
registration package metadata.

This module does not scan artifacts.
This module does not register assertions.
This module does not perform participant discovery.
This module does not mutate producer outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


GSC_REQUIRED_ARTIFACT_IDS = frozenset(
    {
        "consensus_gene_set",
        "gene_provenance",
        "source_contributions",
        "final_run_manifest",
    }
)

GSC_RECOMMENDED_ARTIFACT_IDS = frozenset(
    {
        "gene_source_matrix",
        "gene_frequency_table",
        "output_contract_validation",
        "validation_report",
    }
)


@dataclass(frozen=True)
class ResolvedTepArtifact:
    """One artifact resolved from a producer TEP."""

    artifact_id: str
    semantic_role: str | None
    artifact_type: str | None
    declared_path: str
    resolved_path: str
    required: bool
    recommended: bool
    exists: bool


@dataclass(frozen=True)
class ResolvedTepPackage:
    """Resolved producer TEP package."""

    producer_family: str
    tep_type: str
    tep_id: str
    package_id: str
    release_id: str
    run_id: str
    phenotype: str | None
    transport_envelope_path: str
    authoritative_root: str
    registration_root: str
    resolved_artifacts: list[ResolvedTepArtifact]
    missing_required_artifact_ids: list[str]
    missing_recommended_artifact_ids: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")

    return payload


def _resolve_repo_relative_path(
    producer_repo_root: Path,
    declared_path: str,
) -> Path:
    path = Path(declared_path)

    if path.is_absolute():
        return path

    return producer_repo_root / path


def resolve_gsc_tep_package(
    tep_json_path: Path | str,
    producer_repo_root: Path | str,
) -> ResolvedTepPackage:
    """Resolve a reference-based GSC TEP package.

    GSC TEPs are transport envelopes that reference authoritative producer
    outputs under the producer repository results/ tree.
    """
    tep_path = Path(tep_json_path).expanduser().resolve()
    repo_root = Path(producer_repo_root).expanduser().resolve()
    tep = _read_json(tep_path)

    envelope = tep.get("envelope", {})
    manifest = tep.get("manifest", {})

    if not isinstance(envelope, dict):
        raise ValueError("GSC TEP envelope must be a JSON object")
    if not isinstance(manifest, dict):
        raise ValueError("GSC TEP manifest must be a JSON object")

    authoritative_run_directory = str(
        manifest.get("authoritative_run_directory")
        or envelope.get("source_authoritative_run_directory")
        or ""
    )
    if not authoritative_run_directory:
        raise ValueError("GSC TEP is missing authoritative run directory")

    authoritative_root = _resolve_repo_relative_path(
        producer_repo_root=repo_root,
        declared_path=authoritative_run_directory,
    )

    artifact_entries = manifest.get("artifacts", [])
    if not isinstance(artifact_entries, list):
        raise ValueError("GSC TEP manifest.artifacts must be a list")

    resolved_artifacts: list[ResolvedTepArtifact] = []
    observed_artifact_ids: set[str] = set()

    for entry in artifact_entries:
        if not isinstance(entry, dict):
            raise ValueError("GSC TEP artifact entries must be JSON objects")

        artifact_id = str(entry.get("artifact_id", ""))
        declared_path = str(entry.get("artifact_path", ""))
        if not artifact_id or not declared_path:
            raise ValueError("GSC TEP artifact entry missing artifact_id or artifact_path")

        observed_artifact_ids.add(artifact_id)

        resolved_path = _resolve_repo_relative_path(
            producer_repo_root=repo_root,
            declared_path=declared_path,
        )

        resolved_artifacts.append(
            ResolvedTepArtifact(
                artifact_id=artifact_id,
                semantic_role=(
                    str(entry["semantic_role"])
                    if entry.get("semantic_role") is not None
                    else None
                ),
                artifact_type=(
                    str(entry["artifact_type"])
                    if entry.get("artifact_type") is not None
                    else None
                ),
                declared_path=declared_path,
                resolved_path=str(resolved_path),
                required=artifact_id in GSC_REQUIRED_ARTIFACT_IDS,
                recommended=artifact_id in GSC_RECOMMENDED_ARTIFACT_IDS,
                exists=resolved_path.exists(),
            )
        )

    missing_required = sorted(
        artifact_id
        for artifact_id in GSC_REQUIRED_ARTIFACT_IDS
        if artifact_id not in observed_artifact_ids
        or not any(
            artifact.artifact_id == artifact_id and artifact.exists
            for artifact in resolved_artifacts
        )
    )

    missing_recommended = sorted(
        artifact_id
        for artifact_id in GSC_RECOMMENDED_ARTIFACT_IDS
        if artifact_id not in observed_artifact_ids
        or not any(
            artifact.artifact_id == artifact_id and artifact.exists
            for artifact in resolved_artifacts
        )
    )

    return ResolvedTepPackage(
        producer_family="GSC",
        tep_type=str(envelope.get("tep_type", "")),
        tep_id=str(envelope.get("tep_id", "")),
        package_id=str(envelope.get("source_package_id", "")),
        release_id=str(
            manifest.get("release_id")
            or envelope.get("source_release_id")
            or ""
        ),
        run_id=str(manifest.get("run_id") or envelope.get("source_run_id") or ""),
        phenotype=(
            str(envelope["source_phenotype"])
            if envelope.get("source_phenotype") is not None
            else None
        ),
        transport_envelope_path=str(tep_path),
        authoritative_root=str(authoritative_root),
        registration_root=str(authoritative_root),
        resolved_artifacts=resolved_artifacts,
        missing_required_artifact_ids=missing_required,
        missing_recommended_artifact_ids=missing_recommended,
    )

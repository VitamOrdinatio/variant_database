"""Evidence surface classification.

Evidence surface classification maps producer artifacts into
VDB-recognized evidence surfaces.

This module intentionally performs no biological interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class EvidenceSurface:
    """Classification of a producer artifact."""

    surface_role: str
    evidence_domain: str
    evidence_bearing: bool


type SurfaceRule = tuple[str, EvidenceSurface]

VAP_SURFACE_RULES: tuple[SurfaceRule, ...] = (
    (
        "entities/coding_interpretation/",
        EvidenceSurface(
            "coding_interpretation",
            "variant_interpretation",
            True,
        ),
    ),
    (
        "entities/noncoding_interpretation/",
        EvidenceSurface(
            "noncoding_interpretation",
            "variant_interpretation",
            True,
        ),
    ),
    (
        "entities/normalization/",
        EvidenceSurface(
            "normalized_variants",
            "variant_normalization",
            True,
        ),
    ),
    (
        "entities/observation/",
        EvidenceSurface(
            "observations",
            "variant_observation",
            True,
        ),
    ),
    (
        "entities/prioritization/",
        EvidenceSurface(
            "prioritized_variants",
            "variant_prioritization",
            True,
        ),
    ),
    (
        "entities/routing/",
        EvidenceSurface(
            "routing_candidates",
            "candidate_routing",
            True,
        ),
    ),
    (
        "entities/validation/",
        EvidenceSurface(
            "validation_candidates",
            "validation",
            True,
        ),
    ),
    (
        "entities/context/",
        EvidenceSurface(
            "context",
            "run_context",
            False,
        ),
    ),
)

GSC_SURFACE_RULES: tuple[SurfaceRule, ...] = (
    (
        "consensus_gene_set.tsv",
        EvidenceSurface(
            "semantic_prior_table",
            "phenotype_gene_semantic_prior",
            True,
        ),
    ),
    (
        "gene_provenance.tsv",
        EvidenceSurface(
            "gene_provenance",
            "phenotype_gene_provenance",
            True,
        ),
    ),
    (
        "source_contributions.tsv",
        EvidenceSurface(
            "source_contribution_topology",
            "source_contribution_topology",
            True,
        ),
    ),
    (
        "gene_source_matrix.tsv",
        EvidenceSurface(
            "gene_source_matrix",
            "source_gene_relationship",
            True,
        ),
    ),
    (
        "gene_frequency_table.tsv",
        EvidenceSurface(
            "gene_frequency_table",
            "aggregation_support",
            True,
        ),
    ),
    (
        "output_contract_validation.tsv",
        EvidenceSurface(
            "output_contract_validation",
            "producer_contract_validation",
            True,
        ),
    ),
)

NON_EVIDENCE_ARTIFACTS = {
    "entity_inventory.json": EvidenceSurface(
        "package_manifest",
        "manifest",
        False,
    ),
    "lineage_manifest.json": EvidenceSurface(
        "lineage_manifest",
        "provenance",
        False,
    ),
    "validation_report.md": EvidenceSurface(
        "validation_report",
        "validation",
        False,
    ),
}


def classify_surface(
    relative_path: str,
    producer_family: str = "VAP",
) -> EvidenceSurface:
    """Classify an artifact into a VDB evidence surface."""
    filename = PurePosixPath(relative_path).name

    if filename in NON_EVIDENCE_ARTIFACTS:
        return NON_EVIDENCE_ARTIFACTS[filename]

    normalized = relative_path.replace("\\", "/")
    producer = producer_family.strip().upper()

    if producer == "VAP":
        for prefix, surface in VAP_SURFACE_RULES:
            if normalized.startswith(prefix):
                return surface

    if producer == "GSC":
        for artifact_name, surface in GSC_SURFACE_RULES:
            if filename == artifact_name:
                return surface

    return EvidenceSurface(
        "unclassified",
        "unknown",
        False,
    )

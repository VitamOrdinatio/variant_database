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


SURFACE_RULES: tuple[tuple[str, EvidenceSurface], ...] = (
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

SPECIAL_ARTIFACTS = {
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


def classify_surface(relative_path: str) -> EvidenceSurface:
    """Classify an artifact into a VDB evidence surface."""
    filename = PurePosixPath(relative_path).name

    if filename in SPECIAL_ARTIFACTS:
        return SPECIAL_ARTIFACTS[filename]

    normalized = relative_path.replace("\\", "/")

    for prefix, surface in SURFACE_RULES:
        if normalized.startswith(prefix):
            return surface

    return EvidenceSurface(
        "unclassified",
        "unknown",
        False,
    )

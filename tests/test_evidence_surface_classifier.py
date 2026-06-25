from variant_database.registration.evidence_surface_classifier import (
    classify_surface,
)


def test_manifest_classification() -> None:
    surface = classify_surface("entity_inventory.json")

    assert surface.surface_role == "package_manifest"
    assert surface.evidence_domain == "manifest"
    assert surface.evidence_bearing is False


def test_coding_surface() -> None:
    surface = classify_surface(
        "entities/coding_interpretation/stage_09_coding_interpreted.tsv"
    )

    assert surface.surface_role == "coding_interpretation"
    assert surface.evidence_bearing is True


def test_context_surface() -> None:
    surface = classify_surface(
        "entities/context/stage_13_run_report.md"
    )

    assert surface.surface_role == "context"
    assert surface.evidence_domain == "run_context"
    assert surface.evidence_bearing is False


def test_unknown_surface() -> None:
    surface = classify_surface(
        "future/producer/something_we_have_never_seen.xyz"
    )

    assert surface.surface_role == "unclassified"
    assert surface.evidence_domain == "unknown"
    assert surface.evidence_bearing is False

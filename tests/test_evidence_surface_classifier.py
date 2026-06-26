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


def test_classifies_gsc_consensus_gene_set() -> None:
    classification = classify_surface(
        relative_path="tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv",
        producer_family="GSC",
    )

    assert classification.evidence_bearing is True
    assert classification.surface_role == "semantic_prior_table"
    assert classification.evidence_domain == "phenotype_gene_semantic_prior"


def test_classifies_gsc_source_contributions() -> None:
    classification = classify_surface(
        relative_path="tables/mitochondrial_semantic_gtr_experimental/source_contributions.tsv",
        producer_family="GSC",
    )

    assert classification.evidence_bearing is True
    assert classification.surface_role == "source_contribution_topology"
    assert classification.evidence_domain == "source_contribution_topology"


def test_classifies_gsc_gene_provenance() -> None:
    classification = classify_surface(
        relative_path="tables/epilepsy_semantic_gtr_experimental/gene_provenance.tsv",
        producer_family="GSC",
    )

    assert classification.evidence_bearing is True
    assert classification.surface_role == "gene_provenance"
    assert classification.evidence_domain == "phenotype_gene_provenance"


def test_does_not_classify_gsc_validation_report_as_row_evidence() -> None:
    classification = classify_surface(
        relative_path="reports/epilepsy_semantic_gtr_experimental/validation_report.md",
        producer_family="GSC",
    )

    assert classification.evidence_bearing is False
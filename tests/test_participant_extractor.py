from variant_database.registration.participant_extractor import (
    extract_vap_gene_participants_from_row,
)


def test_extract_vap_gene_symbol_and_ensembl_id() -> None:
    row = {
        "gene_symbol": "POLG",
        "gene_id": "ENSG00000140521",
    }

    participants = extract_vap_gene_participants_from_row(
        row,
        source_record_ref="row:1",
    )

    assert len(participants) == 2

    assert participants[0].participant_kind == "gene"
    assert participants[0].source_namespace == "vap_gene_symbol"
    assert participants[0].source_value == "POLG"
    assert participants[0].source_record_ref == "row:1"

    assert participants[1].source_namespace == "vap_ensembl_gene_id"
    assert participants[1].source_value == "ENSG00000140521"


def test_extract_vap_gene_participants_is_case_insensitive() -> None:
    row = {
        "Gene_Symbol": "POLG",
        "Ensembl_Gene_ID": "ENSG00000140521",
    }

    participants = extract_vap_gene_participants_from_row(row)

    assert [p.source_value for p in participants] == [
        "POLG",
        "ENSG00000140521",
    ]


def test_extract_vap_gene_participants_ignores_empty_values() -> None:
    row = {
        "gene_symbol": "",
        "gene_id": "   ",
    }

    participants = extract_vap_gene_participants_from_row(row)

    assert participants == []


def test_extract_vap_gene_participants_supports_alternate_symbol_column() -> None:
    row = {
        "gene": "POLG",
        "ensembl_id": "ENSG00000140521",
    }

    participants = extract_vap_gene_participants_from_row(row)

    assert [p.source_namespace for p in participants] == [
        "vap_gene_symbol",
        "vap_ensembl_gene_id",
    ]


def test_extract_vap_gene_participants_returns_empty_for_unrecognized_row() -> None:
    row = {
        "chrom": "15",
        "pos": "89333596",
    }

    participants = extract_vap_gene_participants_from_row(row)

    assert participants == []


from variant_database.registration.participant_extractor import (
    extract_vap_participants_from_row,
    extract_vap_variant_participants_from_row,
)


def test_extract_vap_direct_variant_id_without_gene() -> None:
    row = {
        "variant_id": "15:89333596:T:TTGC",
    }

    participants = extract_vap_variant_participants_from_row(
        row,
        source_record_ref="row:1",
    )

    assert len(participants) == 1
    assert participants[0].participant_kind == "variant"
    assert participants[0].source_namespace == "vap_variant_id"
    assert participants[0].source_value == "15:89333596:T:TTGC"
    assert participants[0].source_record_ref == "row:1"


def test_extract_vap_constructed_variant_key_without_gene() -> None:
    row = {
        "chrom": "15",
        "pos": "89333596",
        "ref": "T",
        "alt": "TTGC",
    }

    participants = extract_vap_variant_participants_from_row(row)

    assert len(participants) == 1
    assert participants[0].participant_kind == "variant"
    assert participants[0].source_namespace == "vap_constructed_variant_key"
    assert participants[0].source_value == "15:89333596:T:TTGC"


def test_extract_vap_participants_variant_primary_gene_optional() -> None:
    row = {
        "variant_id": "15:89333596:T:TTGC",
        "gene_symbol": "POLG",
        "gene_id": "ENSG00000140521",
    }

    participants = extract_vap_participants_from_row(row)

    assert [p.participant_kind for p in participants] == [
        "variant",
        "gene",
        "gene",
    ]


def test_extract_vap_participants_preserves_noncoding_variant_without_gene() -> None:
    row = {
        "chrom": "1",
        "pos": "100000",
        "ref": "A",
        "alt": "G",
        "gene_symbol": "",
        "gene_id": "",
    }

    participants = extract_vap_participants_from_row(row)

    assert len(participants) == 1
    assert participants[0].participant_kind == "variant"
    assert participants[0].source_value == "1:100000:A:G"


def test_discover_participants_dispatches_to_vap() -> None:
    from variant_database.registration.participant_extractor import (
        discover_participants_from_row,
    )

    row = {
        "variant_id": "15:89333596:T:TTGC",
        "gene_symbol": "POLG",
    }

    participants = discover_participants_from_row(
        producer_family="VAP",
        row=row,
        source_record_ref="row:1",
    )

    assert [p.participant_kind for p in participants] == [
        "variant",
        "gene",
    ]


def test_discover_participants_is_case_insensitive_for_producer_family() -> None:
    from variant_database.registration.participant_extractor import (
        discover_participants_from_row,
    )

    row = {
        "variant_id": "15:89333596:T:TTGC",
    }

    participants = discover_participants_from_row(
        producer_family="vap",
        row=row,
    )

    assert len(participants) == 1
    assert participants[0].participant_kind == "variant"


def test_discover_participants_rejects_unimplemented_producer() -> None:
    import pytest

    from variant_database.registration.participant_extractor import (
        discover_participants_from_row,
    )

    with pytest.raises(NotImplementedError):
        discover_participants_from_row(
            producer_family="RDGP",
            row={"gene_symbol": "POLG"},
        )


def test_extract_gsc_primary_phenotype_gene_identity() -> None:
    from variant_database.registration.participant_extractor import (
        extract_gsc_participants_from_row,
    )

    row = {
        "phenotype": "mitochondrial_disease",
        "gene_id": "ENSG00000140521",
        "gene_symbol": "POLG",
        "provenance_id": "abc123",
    }

    participants = extract_gsc_participants_from_row(row, source_record_ref="row:1")

    assert [p.source_namespace for p in participants] == [
        "gsc_phenotype",
        "gsc_ensembl_gene_id",
        "gsc_gene_symbol",
        "gsc_provenance_id",
    ]
    assert [p.source_value for p in participants] == [
        "mitochondrial_disease",
        "ENSG00000140521",
        "POLG",
        "abc123",
    ]


def test_extract_gsc_source_contribution_topology() -> None:
    from variant_database.registration.participant_extractor import (
        extract_gsc_participants_from_row,
    )

    row = {
        "gene_id": "ENSG00000140521",
        "gene_symbol": "POLG",
        "source_gene_id": "ENSG00000140521",
        "source_id": "mitocarta_human",
        "semantic_channel": "contextual_biology",
    }

    participants = extract_gsc_participants_from_row(row, source_record_ref="row:7")

    assert [p.source_namespace for p in participants] == [
        "gsc_ensembl_gene_id",
        "gsc_gene_symbol",
        "gsc_source_gene_id",
        "gsc_source_id",
        "gsc_semantic_channel",
    ]
    assert all(p.source_record_ref == "row:7" for p in participants)


def test_discover_participants_dispatches_to_gsc() -> None:
    from variant_database.registration.participant_extractor import (
        discover_participants_from_row,
    )

    row = {
        "phenotype": "epilepsy",
        "gene_id": "ENSG00000140521",
        "gene_symbol": "POLG",
    }

    participants = discover_participants_from_row(
        producer_family="GSC",
        row=row,
        source_record_ref="row:1",
    )

    assert [p.source_namespace for p in participants] == [
        "gsc_phenotype",
        "gsc_ensembl_gene_id",
        "gsc_gene_symbol",
    ]
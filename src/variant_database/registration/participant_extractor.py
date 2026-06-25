"""Assertion Participant Discovery.

Assertion Participant Discovery identifies producer-native participants present
in evidence records.

This module does not persist identities.
This module does not perform namespace resolution.
This module does not attach canonical identities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


VARIANT_ID_COLUMNS = (
    "variant_id",
    "variant_key",
    "variant",
)

CHROM_COLUMNS = (
    "chrom",
    "chromosome",
    "#chrom",
    "#chromosome",
)

POS_COLUMNS = (
    "pos",
    "position",
    "start",
)

REF_COLUMNS = (
    "ref",
    "reference",
)

ALT_COLUMNS = (
    "alt",
    "alternate",
    "alternative",
)

GENE_SYMBOL_COLUMNS = (
    "gene_symbol",
    "symbol",
    "gene",
)

ENSEMBL_GENE_ID_COLUMNS = (
    "gene_id",
    "ensembl_gene_id",
    "ensembl_id",
)


@dataclass(frozen=True)
class ExtractedParticipant:
    """A participant extracted from a source record."""

    participant_kind: str
    participant_role: str
    source_namespace: str
    source_value: str
    source_label: str | None
    extraction_method: str
    source_record_ref: str | None


def _first_nonempty_value(
    row: Mapping[str, object],
    columns: tuple[str, ...],
) -> tuple[str, str] | None:
    """Return the first nonempty value for any matching column."""
    normalized_lookup = {str(key).lower(): key for key in row.keys()}

    for column in columns:
        original_key = normalized_lookup.get(column.lower())
        if original_key is None:
            continue

        value = row.get(original_key)
        if value is None:
            continue

        value_s = str(value).strip()
        if value_s:
            return column, value_s

    return None


def extract_vap_variant_participants_from_row(
    row: Mapping[str, object],
    source_record_ref: str | None = None,
) -> list[ExtractedParticipant]:
    """Extract VAP variant participants from a source row.

    VAP is variant-centered. Variant participant extraction must not depend on
    gene identity being present.
    """
    direct_variant = _first_nonempty_value(row, VARIANT_ID_COLUMNS)
    if direct_variant is not None:
        column, value = direct_variant
        return [
            ExtractedParticipant(
                participant_kind="variant",
                participant_role="variant",
                source_namespace="vap_variant_id",
                source_value=value,
                source_label=value,
                extraction_method=f"vap_row_column:{column}",
                source_record_ref=source_record_ref,
            )
        ]

    chrom = _first_nonempty_value(row, CHROM_COLUMNS)
    pos = _first_nonempty_value(row, POS_COLUMNS)
    ref = _first_nonempty_value(row, REF_COLUMNS)
    alt = _first_nonempty_value(row, ALT_COLUMNS)

    if chrom is None or pos is None or ref is None or alt is None:
        return []

    _, chrom_value = chrom
    _, pos_value = pos
    _, ref_value = ref
    _, alt_value = alt

    variant_key = f"{chrom_value}:{pos_value}:{ref_value}:{alt_value}"

    return [
        ExtractedParticipant(
            participant_kind="variant",
            participant_role="variant",
            source_namespace="vap_constructed_variant_key",
            source_value=variant_key,
            source_label=variant_key,
            extraction_method="vap_row_columns:chrom,pos,ref,alt",
            source_record_ref=source_record_ref,
        )
    ]


def extract_vap_gene_participants_from_row(
    row: Mapping[str, object],
    source_record_ref: str | None = None,
) -> list[ExtractedParticipant]:
    """Extract optional VAP gene participants from a source row.

    Gene participants are optional for VAP. Absence of gene identity must not
    prevent variant-centered assertion participant discovery.
    """
    participants: list[ExtractedParticipant] = []

    symbol = _first_nonempty_value(row, GENE_SYMBOL_COLUMNS)
    if symbol is not None:
        column, value = symbol
        participants.append(
            ExtractedParticipant(
                participant_kind="gene",
                participant_role="gene",
                source_namespace="vap_gene_symbol",
                source_value=value,
                source_label=value,
                extraction_method=f"vap_row_column:{column}",
                source_record_ref=source_record_ref,
            )
        )

    ensembl = _first_nonempty_value(row, ENSEMBL_GENE_ID_COLUMNS)
    if ensembl is not None:
        column, value = ensembl
        participants.append(
            ExtractedParticipant(
                participant_kind="gene",
                participant_role="gene",
                source_namespace="vap_ensembl_gene_id",
                source_value=value,
                source_label=value,
                extraction_method=f"vap_row_column:{column}",
                source_record_ref=source_record_ref,
            )
        )

    return participants


def extract_vap_participants_from_row(
    row: Mapping[str, object],
    source_record_ref: str | None = None,
) -> list[ExtractedParticipant]:
    """Extract VAP row-level participants.

    VAP participant discovery prioritizes variant identity and attaches gene
    identity only when present.
    """
    return (
        extract_vap_variant_participants_from_row(row, source_record_ref)
        + extract_vap_gene_participants_from_row(row, source_record_ref)
    )


def discover_participants_from_row(
    producer_family: str,
    row: Mapping[str, object],
    source_record_ref: str | None = None,
) -> list[ExtractedParticipant]:
    """Discover assertion participants for a producer row.

    This is the producer-agnostic dispatch layer used by orchestration.
    Producer-specific extraction remains isolated behind this interface.
    """
    producer = producer_family.strip().upper()

    if producer == "VAP":
        return extract_vap_participants_from_row(
            row=row,
            source_record_ref=source_record_ref,
        )

    raise NotImplementedError(
        f"Participant discovery is not implemented for producer_family={producer_family!r}"
    )
# HG002 TEP-VAP Lightweight Emulation Report

## Purpose

Create a lightweight, structure-faithful emulation copy of the certified HG002 TEP-VAP.

## Source

`/root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_06_03_010030/tep/vap_tep_HG002_run_2026_06_03_010030_v1`

## Output

`/root/Desktop/vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION`

## Prime Directive

The canonical source TEP was treated as read-only. This script writes only to `/root/Desktop/`.

## Priority Targets

- Gene symbol: `POLG`
- Gene ID: `ENSG00000140521`
- Variant fragments: `15:89333596:T:TTGC`, `89333596`

## File Summary

| Relative path | Mode | Source rows scanned | Output rows | Priority rows | Notes |
|---|---:|---:|---:|---:|---|
| `entity_inventory.json` | copy_intact |  |  |  |  |
| `lineage_manifest.json` | copy_intact |  |  |  |  |
| `validation_report.md` | copy_intact |  |  |  |  |
| `entities/context/stage_13_artifact_manifest.json` | copy_intact |  |  |  |  |
| `entities/context/stage_13_final_summary.json` | copy_intact |  |  |  |  |
| `entities/context/stage_13_run_report.md` | copy_intact |  |  |  |  |
| `entities/coding_interpretation/stage_09_coding_interpreted.tsv` | tsv_header_priority_and_fallback_slice | 27486 | 21 | 1 | priority rows captured: 1; fallback rows captured: 20 |
| `entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv` | tsv_header_priority_and_fallback_slice | 4609098 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/normalization/stage_08_selected_transcript_consequences.tsv` | tsv_header_priority_and_fallback_slice | 4636584 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/normalization/stage_08_vdb_ready_variants.tsv` | tsv_header_priority_and_fallback_slice | 4636584 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/observation/HG002_run_2026_06_03_010030.annotated_variants.tsv` | tsv_header_priority_and_fallback_slice | 4636584 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/prioritization/stage_11_prioritized_variants.tsv` | tsv_header_priority_and_fallback_slice | 4636584 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/routing/coding_candidates.tsv` | tsv_header_priority_and_fallback_slice | 24278 | 21 | 1 | priority rows captured: 1; fallback rows captured: 20 |
| `entities/routing/noncoding_candidates.tsv` | tsv_header_priority_and_fallback_slice | 4609098 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |
| `entities/routing/splice_region_candidates.tsv` | tsv_header_priority_and_fallback_slice | 3733 | 20 | 0 | no POLG / ENSG00000140521 priority rows detected; fallback rows captured: 20 |
| `entities/validation/stage_12_validation_candidates.tsv` | tsv_header_priority_and_fallback_slice | 4636584 | 45 | 25 | priority rows captured: 25; fallback rows captured: 20 |

## Recommended sys76 Destination

Copy this output folder into VDB as a local-only fixture or developer fixture, for example:

```text
tests/fixtures/tep_vap_hg002_lightweight/
```

Do not treat this emulator as biological evidence. It is a topology-preserving development fixture.

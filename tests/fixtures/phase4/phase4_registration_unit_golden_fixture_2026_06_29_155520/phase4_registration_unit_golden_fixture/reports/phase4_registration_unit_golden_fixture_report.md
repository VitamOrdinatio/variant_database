# Phase 4 Registration Unit Golden Fixture Report

## Purpose

Create a lightweight, real-row-derived Phase 4 development fixture from the six certified Phase 3 VDB Registration Unit SQLite databases on MARK.

## Created

`2026-06-29T15:55:20.492122+00:00`

## Source Corpus

`/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical`

## Output

Output directory: `/root/Desktop/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture`

Archive: `/root/Desktop/phase4_registration_unit_golden_fixture_2026_06_29_155520.tgz`

## Prime Directive

The script reads MARK-resident source SQLite files and writes only to `/root/Desktop/`. It must not mutate source repositories or source SQLite files.

## Extraction Policy

The fixture copies `schema_metadata`, `tep_packages`, `artifacts`, and `assertion_registrations` completely. It compresses `source_identities` by deterministic real-row selection with lineage.

## Authority Boundary

This fixture is a compressed, real-row-derived development substrate. It is not biological truth, clinical truth, Phase 4 certification, or a substitute for MARK full-corpus smoketesting.

## Summary

- Registration Units: `6`
- Total source SQLite bytes: `53135409152`
- Total output SQLite bytes: `970752`
- Total source_identities rows scanned: `147941196`
- Total source_identities rows selected: `1651`
- Total selected priority-seed rows: `512`
- Total warnings: `14`

## Per-Unit Summary

| Unit | Source identity rows scanned | Selected source identities | Priority selected | Null selected | Non-null selected | Output bytes | Warnings |
|---|---:|---:|---:|---:|---:|---:|---|
| `gsc_epilepsy` | 89138 | 273 | 66 | 0 | 273 | 151552 | priority seed absent in gsc_epilepsy: 15:89333596:T:TTGC; priority seed absent in gsc_epilepsy: 89333596; no null source_record_ref rows observed in gsc_epilepsy |
| `gsc_mitochondrial_disease` | 85434 | 254 | 46 | 0 | 254 | 147456 | priority seed absent in gsc_mitochondrial_disease: ENSG00000144285; priority seed absent in gsc_mitochondrial_disease: ENSG00000100150; priority seed absent in gsc_mitochondrial_disease: 15:89333596:T:TTGC; priority seed absent in gsc_mitochondrial_disease: 89333596; no null source_record_ref rows observed in gsc_mitochondrial_disease |
| `vap_hg002` | 97369849 | 281 | 100 | 10 | 271 | 167936 |  |
| `vap_median_ERR10619300` | 15467317 | 281 | 100 | 10 | 271 | 167936 | priority seed absent in vap_median_ERR10619300: 15:89333596:T:TTGC; priority seed absent in vap_median_ERR10619300: 89333596 |
| `vap_q1_ERR10619212` | 19017490 | 281 | 100 | 10 | 271 | 167936 | priority seed absent in vap_q1_ERR10619212: 15:89333596:T:TTGC; priority seed absent in vap_q1_ERR10619212: 89333596 |
| `vap_q3_ERR10619225` | 15911968 | 281 | 100 | 10 | 271 | 167936 | priority seed absent in vap_q3_ERR10619225: 15:89333596:T:TTGC; priority seed absent in vap_q3_ERR10619225: 89333596 |

## Source Non-Mutation Audit

| Unit | Pre/post state | Audit status | Notes |
|---|---|---|---|
| `gsc_epilepsy` | `unchanged` | `passed` | priority seed absent in gsc_epilepsy: 15:89333596:T:TTGC; priority seed absent in gsc_epilepsy: 89333596; no null source_record_ref rows observed in gsc_epilepsy |
| `gsc_mitochondrial_disease` | `unchanged` | `passed` | priority seed absent in gsc_mitochondrial_disease: ENSG00000144285; priority seed absent in gsc_mitochondrial_disease: ENSG00000100150; priority seed absent in gsc_mitochondrial_disease: 15:89333596:T:TTGC; priority seed absent in gsc_mitochondrial_disease: 89333596; no null source_record_ref rows observed in gsc_mitochondrial_disease |
| `vap_hg002` | `unchanged` | `passed` |  |
| `vap_median_ERR10619300` | `unchanged` | `passed` | priority seed absent in vap_median_ERR10619300: 15:89333596:T:TTGC; priority seed absent in vap_median_ERR10619300: 89333596 |
| `vap_q1_ERR10619212` | `unchanged` | `passed` | priority seed absent in vap_q1_ERR10619212: 15:89333596:T:TTGC; priority seed absent in vap_q1_ERR10619212: 89333596 |
| `vap_q3_ERR10619225` | `unchanged` | `passed` | priority seed absent in vap_q3_ERR10619225: 15:89333596:T:TTGC; priority seed absent in vap_q3_ERR10619225: 89333596 |

## sys76 Placement Recommendation

After manual retrieval, place the extracted fixture contents under:

```text
tests/fixtures/phase4/
```

The local fixture Registration Unit root should then be:

```text
tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

## Known Limitations

This fixture does not preserve all source rows or MARK-scale row volume. It is intended for rapid local Phase 4 development and must not replace MARK full-corpus smoketesting.

# Phase 4 Golden Fixture Synthesis Summary Report

## Purpose

This document summarizes Phase 4 golden fixture synthesis events for the Variant Database (VDB).

The primary purpose is to record whether each Phase 4 fixture was successfully created, where it was placed, what substrate it represents, what warnings were emitted, and whether the fixture is acceptable for local development.

This document is intended to grow append-only as additional Phase 4 fixtures are created for topology, geometry, evidence surface, projection, stress, or negative-case development.

---

# Fixture Registry

| Fixture ID                                                  | Fixture Type                     | Source Class                      | Status   | Primary Use                       |
| ----------------------------------------------------------- | -------------------------------- | --------------------------------- | -------- | --------------------------------- |
| `phase4_registration_unit_golden_fixture_2026_06_29_155520` | Registration Unit golden fixture | MARK-derived compressed real rows | Accepted | Phase 4.1 / 4.2 local development |

---

# Fixture 1: MARK-Derived Registration Unit Golden Fixture

## Fixture Identity

```text
fixture_id: phase4_registration_unit_golden_fixture_2026_06_29_155520
fixture_family: phase4_registration_unit_golden_fixture
fixture_role: Phase 4 Validation Layer 2
fixture_type: MARK-derived compressed real-row fixture
source_substrate: six certified Phase 3 VDB Registration Unit SQLite databases
creation_environment: MARK
local_development_environment: sys76
```

## Local Placement

The fixture was unpacked on sys76 under:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/
```

The active Registration Unit fixture root is:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

The unpacked fixture contains:

```text
15 directories
16 files
```

Primary fixture components:

```text
expected/
lineage/
manifests/
registration_units/
reports/
```

Compressed SQLite outputs:

```text
gsc_epilepsy/vdb.sqlite                         148K
gsc_mitochondrial_disease/vdb.sqlite            144K
vap_hg002/vdb.sqlite                            164K
vap_median_ERR10619300/vdb.sqlite               164K
vap_q1_ERR10619212/vdb.sqlite                   164K
vap_q3_ERR10619225/vdb.sqlite                   164K
```

## Source Coverage

The fixture was synthesized from all six certified Phase 3 Registration Unit SQLite files:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

The synthesis process scanned all source `source_identities` rows across the six source databases:

```text
total source_identities scanned: 147,941,196
total source_identities selected: 1,651
```

Per-unit selected rows:

| Registration Unit           | Source Rows Scanned | Source Rows Selected |
| --------------------------- | ------------------: | -------------------: |
| `gsc_epilepsy`              |              89,138 |                  273 |
| `gsc_mitochondrial_disease` |              85,434 |                  254 |
| `vap_hg002`                 |          97,369,849 |                  281 |
| `vap_median_ERR10619300`    |          15,467,317 |                  281 |
| `vap_q1_ERR10619212`        |          19,017,490 |                  281 |
| `vap_q3_ERR10619225`        |          15,911,968 |                  281 |

## Preserved Structure

The fixture preserved the expected Registration Unit table surface:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
source_identities
```

The following small structural tables were copied completely:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
```

The large table below was compressed by deterministic real-row selection:

```text
source_identities
```

No synthetic biological rows were created.

No synthetic source identity rows were created.

## Generated Support Artifacts

The fixture includes expected-output files:

```text
expected/registration_unit_category_summary_expected.tsv
expected/registration_unit_fixture_inventory_expected.tsv
expected/registration_unit_table_counts_expected.tsv
```

The fixture includes lineage artifacts:

```text
lineage/copied_table_lineage.tsv
lineage/selected_source_identity_lineage.tsv
```

The fixture includes manifest and report artifacts:

```text
manifests/phase4_registration_unit_golden_fixture_manifest.json
reports/phase4_registration_unit_golden_fixture_report.md
reports/source_database_audit.tsv
reports/fixture_database_audit.tsv
reports/fixture_checksums.tsv
```

## Synthesis Warnings

The synthesis completed with 14 warnings.

The warnings were interpreted as expected absence or coverage warnings, not fixture failures.

Warning distribution:

| Registration Unit           | Warning Count | Interpretation                                                                                    |
| --------------------------- | ------------: | ------------------------------------------------------------------------------------------------- |
| `gsc_epilepsy`              |             3 | VAP/HG002 variant fragments absent; no null `source_record_ref` rows                              |
| `gsc_mitochondrial_disease` |             5 | Epilepsy Ensembl IDs absent; VAP/HG002 variant fragments absent; no null `source_record_ref` rows |
| `vap_hg002`                 |             0 | Priority checks represented                                                                       |
| `vap_median_ERR10619300`    |             2 | HG002 POLG variant fragments absent                                                               |
| `vap_q1_ERR10619212`        |             2 | HG002 POLG variant fragments absent                                                               |
| `vap_q3_ERR10619225`        |             2 | HG002 POLG variant fragments absent                                                               |

Total:

```text
3 + 5 + 0 + 2 + 2 + 2 = 14
```

These warnings do not indicate corruption, failed extraction, missing required tables, failed SQLite integrity, or failed fixture generation.

The warnings record real biological and producer-specific absence patterns.

GSC Registration Units are phenotype-gene semantic evidence products, not variant-call products. Therefore, absence of VAP/HG002 variant fragments in GSC units is expected.

Non-HG002 VAP WES units are not expected to contain the exact HG002 POLG variant fragment.

The absence of null `source_record_ref` rows in GSC units appears to reflect a real producer-specific difference: GSC source identity rows are fully source-referenced in the selected corpus, whereas VAP units include null source-record-reference examples.

## Validation Interpretation

The generated fixture satisfies the intended Phase 4 Validation Layer 2 role.

Accepted properties:

```text
six Registration Unit directories present
six compressed vdb.sqlite files present
required SQLite table surface preserved
small structural tables copied completely
source_identities compressed by real-row selection
lineage artifacts emitted
source and fixture audit artifacts emitted
manifest and report artifacts emitted
checksums emitted
fixture is lightweight enough for rapid local development
```

The fixture is suitable for:

```text
Phase 4.1 Registration Unit inspection development
Phase 4.1 inventory/readiness validation
Phase 4.2 Corpus Generation development
early Phase 4.3 assertion-record indexing exploration
namespace/category grouping checks
producer-family and evidence-domain inspection
```

The fixture is not sufficient for:

```text
Phase 4 certification
release certification
full MARK-scale performance testing
full biological breadth validation
replacement of MARK full-corpus smoketesting
```

## Verdict

```text
ACCEPTED AS PHASE 4 VALIDATION LAYER 2 GOLDEN FIXTURE
```

The fixture is accepted as the primary local Phase 4 golden fixture for Registration Unit and early Corpus Generation development.

The 14 warnings should remain preserved in the fixture report because they document real absence patterns and producer-specific behavior.

No rerun is required for the current Phase 4.1 / Phase 4.2 development scope.

---

# Future Fixture Append Section Template

Additional Phase 4 fixtures should be appended below using this structure.

## Fixture N: <Fixture Name>

### Fixture Identity

```text
fixture_id:
fixture_family:
fixture_role:
fixture_type:
source_substrate:
creation_environment:
local_development_environment:
```

### Local Placement

```text
tests/fixtures/phase4/<fixture_path>/
```

### Source Coverage

Describe source inputs, source row counts, selected row counts, and any producer/domain coverage.

### Preserved Structure

Describe table surfaces, copied tables, compressed tables, and any deliberately omitted structures.

### Generated Support Artifacts

List manifests, reports, lineage files, expected outputs, and checksums.

### Synthesis Warnings

Summarize warnings and classify them as:

```text
expected_absence
coverage_note
non_blocking_warning
blocking_failure
```

### Validation Interpretation

Describe what the fixture supports and what it does not support.

### Verdict

```text
ACCEPTED
ACCEPTED_WITH_NOTES
REJECTED
SUPERSEDED
```

---

# Summary

The first Phase 4 golden fixture was successfully synthesized from the six certified Phase 3 MARK VDB Registration Unit SQLite databases.

It is a compressed real-row fixture, not a synthetic emulator.

It preserves the Registration Unit inspection surface, selected real source identity rows, source/output lineage, audits, manifests, checksums, and expected-output scaffolds.

It is accepted for Phase 4 Validation Layer 2 local development on sys76.

Future Phase 4 fixtures may be appended to this document as needs arise for topology, convergence geometry, evidence surfaces, projection, stress testing, or negative-case validation.

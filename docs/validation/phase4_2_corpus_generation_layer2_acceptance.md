# Phase 4.2 Corpus Generation Layer 2 Acceptance

## Status

Accepted.

Phase 4.2 Corpus Generation has cleared Validation Layer 2 using the MARK-derived compressed real-row Phase 4 Registration Unit golden fixture.

## Validation Layer

```text
Layer 2 — Lightweight Golden Fixture Smoketest
```

For Phase 4.2, Layer 2 means:

```text
Can the Phase 4.2 Corpus Generation artifact workflow operate correctly on a
small, sys76-local, real-row-derived golden fixture substrate before MARK
full-corpus smoketesting?
```

## Acceptance Verdict

```text
PHASE 4.2 LAYER 2 ACCEPTED
```

The acceptance-bearing Layer 2 receipt is the golden-fixture smoketest:

```text
results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
```

The synthetic lightweight smoketest is retained as a supplemental operator-path check, but it is not the primary Layer 2 acceptance receipt.

## Test Suite State At Acceptance

```text
140 passed
```

## Layer 2 Receipt Family

```text
results/validation/phase4_corpus_generation/
├── golden_fixture_smoketest_2026_06_30_122500/
├── lightweight_fixture_smoketest_2026_06_30_121500/
├── phase4_2_golden_fixture_smoketest_summary.json
├── phase4_2_golden_fixture_smoketest_summary.tsv
├── phase4_2_lightweight_smoketest_summary.json
├── phase4_2_lightweight_smoketest_summary.tsv
└── receipt_archives/
```

## Acceptance-Bearing Golden Fixture Receipt

The acceptance-bearing receipt is:

```text
results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
```

Expected durable artifacts include:

```text
inputs/
phase4_1_receipts/
scratch_corpus_generation/
validation_receipts/
logs/
phase4_2_golden_fixture_smoketest_summary.json
phase4_2_golden_fixture_smoketest_summary.tsv
```

The checksum-backed archive is:

```text
results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz
results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz.sha256
```

## Golden Fixture Substrate

The smoketest used the sys76-local MARK-derived compressed Phase 4 Registration Unit golden fixture:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/
```

Inner fixture root:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/
```

Registration Unit root:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

The fixture is compressed but real-row-derived. It is not synthetic and is not a substitute for MARK full-corpus smoketesting.

## Included Registration Units

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Producer distribution:

```text
GSC: 2
VAP: 4
```

## Acceptance Summary

The golden-fixture smoketest produced the expected Phase 4.2 Layer 2 summary:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed

included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 1651
producer_family_distribution: {'GSC': 2, 'VAP': 4}
failed_check_count: 0
```

## Scope Of Validation

This Layer 2 validation proves that Phase 4.2 can:

```text
consume the compressed real-row golden fixture
inspect local fixture SQLite files read-only
verify fixture checksums
verify non-mutation behavior
emit Phase 4.1-compatible inventory receipts
emit Phase 4.1-compatible readiness receipts
generate a Phase 4.2 Corpus Generation selection manifest
emit Corpus Generation build artifacts
emit downstream Assertion Record input manifest
validate the emitted Corpus Generation artifact set
preserve included-only downstream handoff behavior
preserve anti-certification boundaries
```

## Authority Boundaries

This Layer 2 validation does not:

```text
use MARK full-corpus data
certify biological correctness
certify Corpus Generation for release
create Assertion Records
derive Evidence Topology
derive Convergence Geometry
emit Evidence Convergence Surfaces
emit Projection Layer outputs
perform RDGP reasoning
interpret evidence
```

## Supplemental Synthetic Smoketest

A supplemental synthetic operator-path smoketest was also run:

```text
results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/
```

This receipt proves that the public/operator smoketest path can execute on a tiny hermetic fixture.

It is useful as a fast regression check, but the acceptance-bearing Layer 2 receipt is the compressed real-world golden fixture smoketest.

## Relationship To Layer 3

Layer 2 acceptance authorizes progression to Layer 3.

Layer 3 remains required before Phase 4.2 is architecturally closed.

Layer 3 will run against the MARK full-corpus substrate and should validate that the same Phase 4.2 Corpus Generation artifact workflow operates against the real full-scale Registration Unit corpus.

## Closing Statement

Phase 4.2 has now cleared local unit/integration testing and compressed real-world golden fixture smoketesting.

The next validation step is:

```text
Validation Layer 3 — MARK real-world Corpus Generation smoketest
```

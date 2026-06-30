# Phase 4.2 Corpus Generation Layer 3 Acceptance

## Status

Accepted.

Phase 4.2 Corpus Generation has cleared Validation Layer 3 using the real MARK full-corpus Phase 3 canonical Registration Unit substrate.

## Validation Layer

```text
Layer 3 — MARK Real-World Data Smoketest
```

For Phase 4.2, Layer 3 means:

```text
Can the Phase 4.2 Corpus Generation artifact workflow operate correctly on the
real MARK full-corpus continuation chain from Phase 3 Registration Units through
regenerated Phase 4.1 receipts and Phase 4.2 Corpus Generation validation?
```

## Acceptance Verdict

```text
PHASE 4.2 LAYER 3 ACCEPTED
```

The acceptance-bearing Layer 3 receipt is:

```text
results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/
```

The checksum-backed receipt archive is:

```text
results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz
results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
```

## Test Suite State After sys76 Import

```text
140 passed
```

## Layer 3 Continuation Chain

This Layer 3 smoketest used the real MARK Phase 3 canonical Registration Unit corpus:

```text
results/registration/mark_phase3_canonical/
```

The smoketest executed the following continuation chain:

```text
real MARK Phase 3 canonical Registration Units
    ↓
fresh Phase 4.1-compatible inventory/readiness receipts
    ↓
Phase 4.2 Corpus Generation selection manifest
    ↓
Phase 4.2 Corpus Generation build artifacts
    ↓
Phase 4.2 Corpus Generation artifact-set validation receipts
```

The smoketest did not use the compressed Layer 2 golden fixture.

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

## Layer 3 Summary

The MARK full-corpus smoketest produced the expected Phase 4.2 Layer 3 summary:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed
boundary_status: passed

included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 147941196
producer_family_distribution: {'GSC': 2, 'VAP': 4}
total_check_count: 210
passed_check_count: 210
failed_check_count: 0
```

## Per-Unit Full-Corpus Counts

```text
gsc_epilepsy:
    artifacts: 9
    assertion_registrations: 6
    source_identities: 89138

gsc_mitochondrial_disease:
    artifacts: 9
    assertion_registrations: 6
    source_identities: 85434

vap_hg002:
    artifacts: 16
    assertion_registrations: 10
    source_identities: 97369849

vap_median_ERR10619300:
    artifacts: 16
    assertion_registrations: 10
    source_identities: 15467317

vap_q1_ERR10619212:
    artifacts: 16
    assertion_registrations: 10
    source_identities: 19017490

vap_q3_ERR10619225:
    artifacts: 16
    assertion_registrations: 10
    source_identities: 15911968
```

## Scope Of Validation

This Layer 3 validation proves that Phase 4.2 can:

```text
operate against the real MARK Phase 3 canonical Registration Unit substrate
inspect all six real SQLite Registration Units read-only
regenerate Phase 4.1-compatible inventory receipts
regenerate Phase 4.1-compatible readiness receipts
declare a real six-unit Corpus Generation scope
emit Corpus Generation build artifacts
emit a downstream Assertion Record input manifest
validate the emitted Corpus Generation artifact set
preserve included-only downstream handoff behavior
preserve expected GSC/VAP producer distribution
preserve expected full-corpus artifact, assertion, and source-identity counts
preserve anti-certification and anti-derivation boundaries
```

## Authority Boundaries

This Layer 3 validation does not:

```text
use the compressed Layer 2 golden fixture
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

## Boundary Status

The smoketest authority boundary was preserved:

```text
uses_mark_full_corpus_data: true
uses_compressed_golden_fixture: false
opens_sqlite_read_only: true
mutates_registration_units: false
certifies_corpus_generation: false
creates_assertion_records: false
derives_topology: false
interprets_evidence: false
```

The emitted Corpus Generation artifact set retained:

```text
corpus_generation_validation_status: not_evaluated
corpus_generation_certification_status: not_available
```

The validation receipt externally judged the emitted artifact set as valid:

```text
validation_status: passed
```

This preserves the distinction between immutable build artifacts and external validation receipts.

## Relationship To Layer 2

Layer 2 validated Phase 4.2 against the sys76-local compressed real-row golden fixture.

Layer 3 validated Phase 4.2 against the full real MARK corpus.

The expected source identity totals differ intentionally:

```text
Layer 2 compressed golden fixture:
    source_identity_count_total: 1651

Layer 3 MARK full corpus:
    source_identity_count_total: 147941196
```

This confirms that Layer 3 used full MARK-scale source identity volume rather than the compressed fixture substrate.

## Closure Implication

With Layer 1, Layer 2, and Layer 3 complete, Phase 4.2 Corpus Generation is architecturally ready for closure.

The next implementation phase is:

```text
Phase 4.3 — Assertion Records
```

Phase 4.3 must consume the governed downstream input manifest emitted by Phase 4.2 rather than crawling Registration Unit folders opportunistically.

## Closing Statement

Phase 4.2 Corpus Generation has now demonstrated correct artifact behavior across:

```text
Layer 1 — pytest unit/integration validation
Layer 2 — sys76 compressed real-row golden fixture validation
Layer 3 — MARK full-corpus real-world validation
```

Phase 4.2 is ready to be recorded as cleared after final documentation and repository status updates.

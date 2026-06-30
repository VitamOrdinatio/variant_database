# Phase 4.2 Corpus Generation Certification

## Status

Certified for Phase 4.2 architectural closure.

## Certification Scope

This document records the final validation judgment for Phase 4.2 Corpus Generation.

Certification here means:

```text
VDB Phase 4.2 has demonstrated correct governed-scope declaration,
artifact emission, downstream included-only handoff behavior, and external
artifact-set validation across the required validation layers.
```

This is an architectural certification of the Phase 4.2 layer.

It is not:

```text
biological truth certification
clinical truth certification
release certification
RDGP reasoning certification
Assertion Record certification
Evidence Topology certification
Convergence Geometry certification
Evidence Surface certification
Projection Layer certification
```

## Phase 4.2 Responsibility

The Phase 4.2 responsibility is Corpus Generation.

The governing invariant is:

```text
A Corpus Generation declares the exact Registration Units selected for a
derived evidence run.
```

The boundary rule is:

```text
A folder of Registration Units is not a Corpus Generation.
```

Phase 4.2 must declare governed scope before downstream evidence structures are derived.

Phase 4.2 must not opportunistically crawl Registration Unit folders.

Phase 4.2 must not create Assertion Records, derive Evidence Topology, compute Convergence Geometry, emit Evidence Convergence Surfaces, emit Projection Layer outputs, or perform biological interpretation.

## Certified Corpus Generation

Canonical Corpus Generation:

```text
corpus_generation_id: mark_phase4_corpus_6tep_v1
```

Corpus Generation label:

```text
MARK Phase 4 6-TEP Benchmark Corpus v1
```

Included Registration Units:

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

Certified scope summary:

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
```

## Certified Build Artifact Family

Canonical Phase 4.2 build artifacts:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
├── inputs/corpus_generation_selection_manifest.tsv
├── corpus_generation_manifest.tsv
├── corpus_generation_manifest.json
├── corpus_generation_report.md
└── downstream_assertion_record_input_manifest.tsv
```

The critical downstream handoff artifact is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

This file is the governed Phase 4.3 input substrate.

Phase 4.3 must consume this governed downstream input manifest.

Phase 4.3 must not crawl Registration Unit folders opportunistically.

## Validation Strategy

Phase 4.2 was evaluated using VDB's three-layer validation strategy:

```text
Layer 1 — unit and integration tests
Layer 2 — lightweight golden fixture smoketest
Layer 3 — MARK real-world full-corpus smoketest
```

Phase 4.2 passed all three validation layers.

## Layer 1 Evidence

Layer 1 validated local implementation behavior through the pytest suite.

Layer 1 status:

```text
passed
```

Test suite state at closure:

```text
140 passed
```

Layer 1 covered the Phase 4.2 implementation stack, including:

```text
selection manifest loading
selection manifest validation
Corpus Generation artifact emission
receipt enrichment
downstream included-only handoff behavior
artifact-set validation
operator-facing smoketest scripts
authority boundary enforcement
```

## Layer 2 Evidence

Layer 2 validated Phase 4.2 against the sys76-local compressed real-row Phase 4 Registration Unit golden fixture.

Acceptance document:

```text
docs/validation/phase4_2_corpus_generation_layer2_acceptance.md
```

Acceptance-bearing receipt:

```text
results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
```

Checksum-backed receipt archive:

```text
results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz
results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz.sha256
```

Layer 2 substrate:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/
```

Layer 2 status:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed
failed_check_count: 0
```

Layer 2 summary:

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 1651
producer_family_distribution: {'GSC': 2, 'VAP': 4}
```

Layer 2 proved that Phase 4.2 could operate against a compressed but real-row-derived local substrate before MARK full-corpus validation.

## Supplemental Layer 2 Operator-Path Check

A supplemental synthetic operator-path smoketest was also executed.

Receipt:

```text
results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/
```

This receipt is useful as a minimal hermetic regression check.

It is not the primary Layer 2 acceptance-bearing receipt.

The acceptance-bearing Layer 2 receipt is the compressed real-row golden fixture smoketest.

## Layer 3 Evidence

Layer 3 validated Phase 4.2 against the real MARK full-corpus Phase 3 canonical Registration Unit substrate.

Acceptance document:

```text
docs/validation/phase4_2_corpus_generation_layer3_acceptance.md
```

Acceptance-bearing receipt:

```text
results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/
```

Checksum-backed receipt archive:

```text
results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz
results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
```

Layer 3 substrate:

```text
results/registration/mark_phase3_canonical/
```

Layer 3 continuation chain:

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

Layer 3 status:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed
boundary_status: passed
```

Layer 3 validation checks:

```text
total_check_count: 210
passed_check_count: 210
failed_check_count: 0
```

Layer 3 summary:

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 147941196
producer_family_distribution: {'GSC': 2, 'VAP': 4}
```

Layer 3 proved that Phase 4.2 could operate against the full real MARK corpus without using the compressed Layer 2 golden fixture.

## Layer 2 And Layer 3 Contrast

The expected source identity totals differ intentionally:

```text
Layer 2 compressed golden fixture:
    source_identity_count_total: 1651

Layer 3 MARK full corpus:
    source_identity_count_total: 147941196
```

This confirms that:

```text
Layer 2 used the compressed real-row sys76 golden fixture.

Layer 3 used the full real MARK corpus.
```

Layer 2 provided local compressed real-world fidelity.

Layer 3 provided full real-world corpus-scale validation.

## Boundary Preservation

Phase 4.2 preserved its authority boundaries across all validation layers.

The emitted Corpus Generation build artifact retained:

```text
corpus_generation_validation_status: not_evaluated
corpus_generation_certification_status: not_available
```

External validation receipts judged the artifact set:

```text
validation_status: passed
```

This distinction is required.

The Corpus Generation build artifact must not self-certify.

The validation receipt may externally judge the emitted artifact set.

The final repository-level certification may then certify Phase 4.2 for architectural closure.

## Non-Authority Claims

This certification does not claim:

```text
the biological interpretation is correct
the corpus is biologically complete
the assertions are clinically true
the topology is valid
the geometry is meaningful
the evidence surfaces are ready
the projection layer is ready
RDGP can reason over the corpus directly
all future producer corpora are automatically valid
```

Future corpora require their own explicit Corpus Generation declarations and validation receipts.

## Residual Scope Notes

The certified corpus is the canonical six-unit MARK Phase 4 benchmark corpus.

It contains:

```text
2 GSC Registration Units
4 VAP Registration Units
```

It does not include every possible VAP SRA-derived TEP.

It does not include future RSP Registration Units.

It does not include future expanded producer corpora.

Additional or expanded corpora must be declared through new Corpus Generations rather than by reusing this certification.

## Certification Decision

Phase 4.2 Corpus Generation is certified for architectural closure.

The certification basis is:

```text
Layer 1 passed.
Layer 2 accepted.
Layer 3 accepted.
Canonical six-unit Corpus Generation emitted.
Downstream included-only handoff emitted.
Artifact-set validation passed.
Authority boundaries preserved.
```

The closure decision is:

```text
PHASE 4.2 CORPUS GENERATION CERTIFIED FOR ARCHITECTURAL CLOSURE
```

## Authorized Next Phase

The next implementation phase is:

```text
Phase 4.3 — Assertion Records
```

Phase 4.3 is authorized to begin from:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Phase 4.3 must preserve the Phase 4 ordering doctrine:

```text
Registration Units preserve custody.
Corpus Generations declare scope.
Assertion Records preserve scientific claims.
Evidence Topology derives organization.
Convergence Geometry characterizes organization.
Evidence Convergence Surfaces govern exposure.
Projection Views represent governed evidence.
RDGP reasons.
```

## Closing Statement

Phase 4.2 Corpus Generation has fulfilled VDB's three-layer validation strategy.

It has demonstrated correct artifact behavior across local implementation tests, compressed real-row golden fixture validation, and full MARK real-world corpus validation.

Phase 4.2 is now architecturally closed.

Phase 4.3 Assertion Records may proceed from the governed downstream Corpus Generation handoff.

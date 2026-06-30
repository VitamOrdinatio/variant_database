# Phase 4.2 Corpus Generation Validation Receipts

## Purpose

This directory contains git-tracked validation receipts for VDB Phase 4.2 Corpus Generation.

These receipts preserve evidence from Corpus Generation build-artifact validation, supplemental operator-path smoketesting, compressed real-row golden fixture validation, and MARK full-corpus validation.

This directory is certification-reviewable evidence.

This directory is not disposable runtime scratch output.

---

## Supporting Documentation

Validation governance and certification documentation:

```text
docs/validation/corpus_generation_validation.md
docs/validation/phase4_2_corpus_generation_layer2_acceptance.md
docs/validation/phase4_2_corpus_generation_layer3_acceptance.md
docs/validation/phase4_2_corpus_generation_certification.md
docs/status/phase4_validation_backlog.md
```

Canonical Phase 4.2 build artifact family:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

Critical downstream Phase 4.3 handoff artifact:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

---

## Receipt Family Overview

This receipt family contains four distinct evidence classes.

```text
mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500/
    Timestamped validation receipt for the canonical emitted build artifact set.

lightweight_fixture_smoketest_2026_06_30_121500/
    Supplemental synthetic operator-path smoketest.

golden_fixture_smoketest_2026_06_30_122500/
    Layer 2 compressed real-row golden fixture smoketest.

mark_full_corpus_smoketest_2026_06_30_123500/
    Layer 3 MARK full-corpus smoketest.
```

These evidence classes must not be collapsed.

The synthetic lightweight smoketest is useful as a hermetic operator-path regression check.

The golden fixture smoketest is acceptance-bearing Layer 2 evidence.

The MARK full-corpus smoketest is acceptance-bearing Layer 3 evidence.

---

## Canonical Build-Artifact Validation Receipt

The canonical emitted Phase 4.2 build artifact family is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

The timestamped validation receipt for that emitted build artifact set is:

```text
results/validation/phase4_corpus_generation/mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500/
```

Retained receipt files:

```text
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
corpus_generation_validation_summary.json
corpus_generation_validation_summary.tsv
```

Latest convenience copies are also retained at the root of this directory:

```text
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
corpus_generation_validation_summary.json
corpus_generation_validation_summary.tsv
```

This receipt validates the emitted canonical Corpus Generation artifact set.

It is not a Layer 2 or Layer 3 smoketest receipt.

---

## Supplemental Lightweight Operator-Path Smoketest

Receipt directory:

```text
results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/
```

Purpose:

```text
supplemental synthetic operator-path validation
```

This smoketest exercises the Phase 4.2 operator path against a small synthetic fixture.

It is retained as a hermetic regression check.

It is not the acceptance-bearing Layer 2 receipt.

Retained receipt structure:

```text
inputs/
logs/
phase4_1_receipts/
scratch_corpus_generation/
validation_receipts/
phase4_2_lightweight_smoketest_summary.json
phase4_2_lightweight_smoketest_summary.tsv
```

Observed summary:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed

included_registration_unit_count: 2
excluded_registration_unit_count: 1
downstream_assertion_record_input_count: 2
artifact_count_total: 25
assertion_registration_count_total: 16
source_identity_count_total: 300
```

---

## Layer 2 Golden Fixture Smoketest

Receipt directory:

```text
results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
```

Purpose:

```text
Layer 2 compressed real-row golden fixture validation
```

This smoketest exercises Phase 4.2 against the sys76-local compressed real-row Phase 4 Registration Unit golden fixture.

It is the acceptance-bearing Layer 2 receipt for Phase 4.2 Corpus Generation.

Retained receipt structure:

```text
inputs/
logs/
phase4_1_receipts/
scratch_corpus_generation/
validation_receipts/
phase4_2_golden_fixture_smoketest_summary.json
phase4_2_golden_fixture_smoketest_summary.tsv
```

Acceptance summary:

```text
smoketest_status: passed
validation_status: passed
summary_status: passed
failed_check_count: 0

included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 1651
producer_family_distribution: {'GSC': 2, 'VAP': 4}
```

Boundary:

```text
uses_compressed_golden_fixture: true
uses_mark_full_corpus_data: false
```

Layer 2 proves that Phase 4.2 Corpus Generation operates correctly against a compressed real-row validation substrate before MARK full-corpus execution.

---

## Layer 3 MARK Full-Corpus Smoketest

Receipt directory:

```text
results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/
```

Purpose:

```text
Layer 3 real MARK full-corpus validation
```

This smoketest exercises Phase 4.2 against the real MARK Phase 3 canonical Registration Unit corpus.

It is the acceptance-bearing Layer 3 receipt for Phase 4.2 Corpus Generation.

Retained receipt structure:

```text
inputs/
logs/
phase4_1_receipts/
scratch_corpus_generation/
validation_receipts/
phase4_2_mark_full_corpus_smoketest_summary.json
phase4_2_mark_full_corpus_smoketest_summary.tsv
```

Acceptance summary:

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

Authority boundary:

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

Layer 3 proves that Phase 4.2 Corpus Generation operates correctly on the full real-world MARK corpus without using the compressed Layer 2 golden fixture.

---

## Latest Convenience Summary Files

Latest convenience summary files are retained at the root of this directory:

```text
phase4_2_lightweight_smoketest_summary.json
phase4_2_lightweight_smoketest_summary.tsv
phase4_2_golden_fixture_smoketest_summary.json
phase4_2_golden_fixture_smoketest_summary.tsv
phase4_2_mark_full_corpus_smoketest_summary.json
phase4_2_mark_full_corpus_smoketest_summary.tsv
```

These files support quick inspection.

They do not replace timestamped receipt directories.

The timestamped receipt directories remain the acceptance-bearing evidence.

---

## Receipt Archives

Portable receipt archives are retained under:

```text
results/validation/phase4_corpus_generation/receipt_archives/
```

Current archives:

```text
mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz
mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz.sha256

lightweight_fixture_smoketest_2026_06_30_121500.tgz
lightweight_fixture_smoketest_2026_06_30_121500.tgz.sha256

golden_fixture_smoketest_2026_06_30_122500.tgz
golden_fixture_smoketest_2026_06_30_122500.tgz.sha256

mark_full_corpus_smoketest_2026_06_30_123500.tgz
mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
```

Archives are retained when they allow review, transfer, or reconstruction of validation evidence generated on MARK or other non-primary execution machines.

Each archive should have a sibling `.sha256` checksum file.

---

## Archive Verification

Verify all retained Phase 4.2 Corpus Generation archives from the archive directory:

```bash
(
  cd results/validation/phase4_corpus_generation/receipt_archives
  sha256sum -c mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz.sha256
  sha256sum -c lightweight_fixture_smoketest_2026_06_30_121500.tgz.sha256
  sha256sum -c golden_fixture_smoketest_2026_06_30_122500.tgz.sha256
  sha256sum -c mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
)
```

Expected result:

```text
mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz: OK
lightweight_fixture_smoketest_2026_06_30_121500.tgz: OK
golden_fixture_smoketest_2026_06_30_122500.tgz: OK
mark_full_corpus_smoketest_2026_06_30_123500.tgz: OK
```

---

## Current Accepted Scope

Canonical Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Accepted Registration Unit scope:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Accepted producer distribution:

```text
GSC: 2
VAP: 4
```

Accepted shared summary:

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
```

Layer-specific source identity totals differ intentionally:

```text
Layer 2 compressed golden fixture:
    source_identity_count_total: 1651

Layer 3 MARK full corpus:
    source_identity_count_total: 147941196
```

---

## Validation Evidence Summary

Phase 4.2 Corpus Generation validation evidence includes:

```text
explicit scope declaration
selection manifest handling
selection policy preservation
receipt-backed Registration Unit readiness use
deterministic Corpus Generation artifact emission
downstream included-only handoff behavior
external artifact-set validation
non-mutation behavior
authority-boundary preservation
anti-certification safeguards
```

The critical downstream Phase 4.3 handoff artifact is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Phase 4.3 must consume the governed downstream input manifest.

Phase 4.3 must not crawl Registration Unit folders opportunistically.

---

## Authority Boundaries

These receipts may prove:

```text
Corpus Generation artifact-set validity
deterministic build artifact emission
selection policy preservation
selection manifest preservation
included-only downstream handoff behavior
receipt-backed Registration Unit readiness use
read-only SQLite handling in smoketest contexts
non-mutation behavior
benchmark-scale execution
authority-boundary preservation
```

These receipts do not prove:

```text
biological correctness
clinical interpretation
Assertion Record correctness
Evidence Topology correctness
Convergence Geometry correctness
Evidence Convergence Surface correctness
Projection Layer correctness
RDGP reasoning correctness
TEP-VDB emission correctness
full Phase 4.8 certification
```

Phase 4.2 receipts do not create Assertion Records.

Phase 4.2 receipts do not derive topology.

Phase 4.2 receipts do not compute geometry.

Phase 4.2 receipts do not emit surfaces.

Phase 4.2 receipts do not emit projections.

Phase 4.2 receipts do not interpret evidence.

---

## Scratch Versus Canonical Build Artifacts

Some timestamped receipt directories contain `scratch_corpus_generation/`.

Those directories preserve validation-local Corpus Generation artifacts generated during smoketest execution.

They should not be confused with the canonical Phase 4.2 build artifact family:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

The canonical downstream handoff artifact remains:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

---

## MARK Export Workflow

MARK may generate validation receipts.

MARK must not push to the canonical repository.

The intended workflow is:

```text
MARK generates receipts.
MARK bundles receipts.
sys76 imports receipts.
sys76 inspects receipts.
sys76 stages receipts.
sys76 commits receipts.
sys76 pushes receipts.
```

This protects the canonical sys76 repository state while preserving MARK-generated validation evidence.

---

## Maintenance Rules

When a new Phase 4.2 Corpus Generation validation run is retained, add it here.

Do not add arbitrary runtime outputs to this directory.

Do not remove acceptance-bearing receipts unless they are superseded by a documented replacement.

Do not remove receipt archives that support validation or certification documents.

Do not treat latest convenience summaries as replacements for timestamped receipt directories.

Do not treat validation-local `scratch_corpus_generation/` directories as canonical build artifact families.

Keep receipt directories stable, timestamped, and checksum-verifiable when archived.

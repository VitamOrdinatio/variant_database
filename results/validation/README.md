# Validation Results

This directory contains git-tracked validation receipts for VDB.

Validation receipts are generated evidence from validation, certification, smoketest, or benchmark runs. They are retained when they support governance, reproducibility, benchmark evidence, certification evidence, or historical validation review.

This directory is not for disposable runtime scratch output.

---

## Purpose

`results/validation/` is the repository's certification-reviewable validation receipt index.

It records what was actually proven during validation execution.

It complements, but does not replace, validation governance documents under:

```text
docs/validation/
```

The governing distinction is:

```text
docs/validation/
    Defines what must be proven.

results/validation/
    Preserves what was proven.
```

---

## Tracking Policy

The repository does not track arbitrary `results/` output.

The repository intentionally tracks selected result families that function as validation evidence or Phase 4 governed build artifacts.

Tracked result families currently include:

```text
results/validation/
results/phase4/
```

Within `results/validation/`, receipt directories may be tracked when they support one or more of the following:

```text
certification evidence
benchmark evidence
reproducibility evidence
governance-supporting validation evidence
historical validation evidence
```

Receipt files do not define validation doctrine.

Validation doctrine, validation specifications, acceptance documents, and certification documents live under:

```text
docs/validation/
```

---

## Current Receipt Families

```text
phase3_registration_certification/
    Phase 3 registration certification receipts supporting Registration Unit
    input trust for Phase 4.

phase4_registration_units/
    Phase 4.1 Registration Unit validation receipts, including both local
    lightweight-fixture receipts and MARK real-corpus six-unit benchmark
    smoketest receipts.

phase4_corpus_generation/
    Phase 4.2 Corpus Generation validation receipts, including synthetic
    operator-path receipts, Layer 2 compressed real-row golden fixture
    acceptance receipts, Layer 3 MARK full-corpus acceptance receipts, and
    portable receipt archives.
```

---

## Relationship To Validation Governance

The receipt families in this directory support these governance documents:

```text
docs/validation/phase3_registration_certification.md

docs/validation/registration_unit_validation.md
docs/validation/phase4_1_registration_unit_certification.md

docs/validation/corpus_generation_validation.md
docs/validation/phase4_2_corpus_generation_layer2_acceptance.md
docs/validation/phase4_2_corpus_generation_layer3_acceptance.md
docs/validation/phase4_2_corpus_generation_certification.md
```

Validation receipts should be interpreted through their corresponding governance documents.

A receipt proves only what its validation scope declares.

---

## Phase 3 Registration Certification Receipts

Receipt directory:

```text
results/validation/phase3_registration_certification/
```

Supporting documentation:

```text
docs/validation/phase3_registration_certification.md
```

Current retained receipt files:

```text
README.md
vdb_phase3_registration_efficacy_2026_06_27_124320_db_summary.tsv
vdb_phase3_registration_efficacy_2026_06_27_124320_identity_summary.tsv
vdb_phase3_registration_efficacy_2026_06_27_124320.json
vdb_phase3_registration_efficacy_2026_06_27_124320.md
```

Purpose:

```text
Certifies that heterogeneous VAP and GSC TEPs were registered into the
VDB Phase 3 registration substrate while preserving package, artifact,
assertion, source identity, namespace, and referential-integrity structure.
```

Current Phase 3 verdict:

```text
passed
```

---

## Phase 4.1 Registration Unit Receipts

Receipt directory:

```text
results/validation/phase4_registration_units/
```

Supporting documentation:

```text
docs/validation/registration_unit_validation.md
docs/validation/phase4_1_registration_unit_certification.md
```

### Local Lightweight-Fixture Receipts

Root-level files under `phase4_registration_units/` preserve the local lightweight-fixture Phase 4.1 validation receipts:

```text
registration_unit_inventory.json
registration_unit_inventory.tsv
registration_unit_readiness.json
registration_unit_readiness.tsv
registration_unit_validation_run_summary.json
registration_unit_validation_summary.json
```

Current local lightweight-fixture verdict:

```text
validation_status: passed
record_count: 6
inspection_count: 6
inventory_row_count: 6
readiness_row_count: 6
ready_count: 6
not_ready_count: 0
non_mutation_status: passed
sidecar_status: passed
```

### MARK Real-Corpus Six-Unit Benchmark Receipts

Timestamped MARK receipt directory:

```text
results/validation/phase4_registration_units/mark_full_corpus_smoketest_2026_06_30_052739/
```

Current retained MARK receipt files:

```text
inputs/registration_unit_input_manifest.tsv
logs/mark_phase4_1_smoketest.log
registration_unit_inventory.json
registration_unit_inventory.tsv
registration_unit_readiness.json
registration_unit_readiness.tsv
registration_unit_validation_run_summary.json
registration_unit_validation_summary.json
```

Portable MARK archive receipts:

```text
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz.sha256
```

Archive SHA256:

```text
e1183821d1c0d0fe7219bdd323a76ed79eb4820bb94ba39b6f15d61c5a639957
```

Current MARK full-corpus verdict:

```text
validation_status: passed
record_count: 6
inspection_count: 6
inventory_row_count: 6
readiness_row_count: 6
ready_count: 6
not_ready_count: 0
inspection_status: passed
inventory_artifact_status: passed
readiness_artifact_status: passed
non_mutation_status: passed
sidecar_status: passed
elapsed_seconds: 888.55
```

The MARK full-corpus run validates the six-unit canonical benchmark corpus:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Phase 4.1 Registration Unit validation status:

```text
passed
```

Phase 4.1 architectural closure status:

```text
certified for the six-unit canonical benchmark corpus
```

---

## Phase 4.2 Corpus Generation Receipts

Receipt directory:

```text
results/validation/phase4_corpus_generation/
```

Supporting documentation:

```text
docs/validation/corpus_generation_validation.md
docs/validation/phase4_2_corpus_generation_layer2_acceptance.md
docs/validation/phase4_2_corpus_generation_layer3_acceptance.md
docs/validation/phase4_2_corpus_generation_certification.md
```

Canonical Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Canonical build artifact family:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

Critical downstream Phase 4.3 handoff artifact:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

### Canonical Artifact-Set Validation Receipts

Timestamped validation receipt directory:

```text
results/validation/phase4_corpus_generation/mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500/
```

Latest convenience copies:

```text
results/validation/phase4_corpus_generation/corpus_generation_validation_report.json
results/validation/phase4_corpus_generation/corpus_generation_validation_report.tsv
results/validation/phase4_corpus_generation/corpus_generation_validation_summary.json
results/validation/phase4_corpus_generation/corpus_generation_validation_summary.tsv
```

Purpose:

```text
Validates the emitted canonical Corpus Generation artifact set for
mark_phase4_corpus_6tep_v1 against its declared selection manifest, policy,
Phase 4.1 inventory, Phase 4.1 readiness receipt, and anti-certification
boundaries.
```

### Supplemental Synthetic Operator-Path Receipts

Timestamped receipt directory:

```text
results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/
```

Latest convenience summary files:

```text
results/validation/phase4_corpus_generation/phase4_2_lightweight_smoketest_summary.json
results/validation/phase4_corpus_generation/phase4_2_lightweight_smoketest_summary.tsv
```

Purpose:

```text
Provides a minimal hermetic operator-path regression check for Phase 4.2
Corpus Generation.
```

This receipt is useful for local workflow regression.

It is not the primary Layer 2 acceptance-bearing receipt.

### Layer 2 Golden Fixture Acceptance Receipts

Timestamped receipt directory:

```text
results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
```

Latest convenience summary files:

```text
results/validation/phase4_corpus_generation/phase4_2_golden_fixture_smoketest_summary.json
results/validation/phase4_corpus_generation/phase4_2_golden_fixture_smoketest_summary.tsv
```

Purpose:

```text
Validates Phase 4.2 Corpus Generation against the sys76-local compressed
real-row Phase 4 Registration Unit golden fixture.
```

Layer 2 acceptance summary:

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

Layer 2 acceptance status:

```text
accepted
```

### Layer 3 MARK Full-Corpus Acceptance Receipts

Timestamped receipt directory:

```text
results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/
```

Latest convenience summary files:

```text
results/validation/phase4_corpus_generation/phase4_2_mark_full_corpus_smoketest_summary.json
results/validation/phase4_corpus_generation/phase4_2_mark_full_corpus_smoketest_summary.tsv
```

Purpose:

```text
Validates Phase 4.2 Corpus Generation against the real MARK full-corpus
Phase 3 canonical Registration Unit substrate.
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

Layer 3 acceptance summary:

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

Layer 3 authority boundary:

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

Layer 3 acceptance status:

```text
accepted
```

### Phase 4.2 Accepted Corpus Scope

The accepted canonical Phase 4.2 Corpus Generation includes:

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

Shared Phase 4.2 summary:

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
```

Source identity totals differ intentionally by validation layer:

```text
Layer 2 compressed golden fixture:
    source_identity_count_total: 1651

Layer 3 MARK full corpus:
    source_identity_count_total: 147941196
```

Phase 4.2 Corpus Generation validation status:

```text
passed
```

Phase 4.2 architectural closure status:

```text
certified for the six-unit canonical benchmark corpus
```

---

## Receipt Archives

Portable receipt archives are stored under each receipt family's `receipt_archives/` directory.

Receipt archives should be retained when they support:

```text
review
transfer
reconstruction
certification evidence
MARK-to-sys76 validation handoff
historical validation evidence
```

Each portable archive should have a sibling `.sha256` checksum file.

Current Phase 4.1 archive receipts:

```text
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz.sha256
```

Current Phase 4.2 archive receipts:

```text
results/validation/phase4_corpus_generation/receipt_archives/lightweight_fixture_smoketest_2026_06_30_121500.tgz
results/validation/phase4_corpus_generation/receipt_archives/lightweight_fixture_smoketest_2026_06_30_121500.tgz.sha256

results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz
results/validation/phase4_corpus_generation/receipt_archives/golden_fixture_smoketest_2026_06_30_122500.tgz.sha256

results/validation/phase4_corpus_generation/receipt_archives/mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz
results/validation/phase4_corpus_generation/receipt_archives/mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz.sha256

results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz
results/validation/phase4_corpus_generation/receipt_archives/mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
```

### Archive Verification

The checksum files use archive basenames.

Verify archives from inside the relevant archive directory.

Phase 4.1 MARK archive:

```bash
(
  cd results/validation/phase4_registration_units/receipt_archives
  sha256sum -c mark_full_corpus_smoketest_2026_06_30_052739.tgz.sha256
)
```

Expected result:

```text
mark_full_corpus_smoketest_2026_06_30_052739.tgz: OK
```

Phase 4.2 Corpus Generation archives:

```bash
(
  cd results/validation/phase4_corpus_generation/receipt_archives
  sha256sum -c lightweight_fixture_smoketest_2026_06_30_121500.tgz.sha256
  sha256sum -c golden_fixture_smoketest_2026_06_30_122500.tgz.sha256
  sha256sum -c mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz.sha256
  sha256sum -c mark_full_corpus_smoketest_2026_06_30_123500.tgz.sha256
)
```

Expected results:

```text
lightweight_fixture_smoketest_2026_06_30_121500.tgz: OK
golden_fixture_smoketest_2026_06_30_122500.tgz: OK
mark_phase4_corpus_6tep_v1_validation_2026_06_30_120500.tgz: OK
mark_full_corpus_smoketest_2026_06_30_123500.tgz: OK
```

---

## MARK Receipt Handoff Policy

MARK may generate validation receipts.

MARK should not push to the canonical remote.

The preferred workflow is:

```text
MARK:
    pull code
    execute heavy validation
    bundle receipts
    export archives to /root/Desktop

sys76:
    retrieve receipt bundles
    verify archive checksums
    inspect receipts
    run local tests
    stage, commit, and push
```

This protects the sys76 repository state while preserving MARK-generated validation evidence.

---

## Scope Boundaries

The retained receipts prove validation behavior within their declared scope.

They may prove:

```text
registration integrity
read-only inspection behavior
deterministic artifact emission
readiness evaluation
Corpus Generation scope declaration
policy-backed selection
receipt-backed validation
downstream included-only handoff behavior
non-mutation behavior
SQLite sidecar absence
authority-boundary preservation
anti-collapse safeguard preservation
benchmark-scale execution
certification evidence preservation
```

They do not prove:

```text
biological correctness
clinical interpretation
evidence scoring correctness
RDGP reasoning correctness
future corpus validity
Assertion Record correctness
Evidence Topology correctness
Convergence Geometry correctness
Evidence Convergence Surface correctness
Projection Layer correctness
TEP-VDB emission correctness
full Phase 4.8 certification
```

Phase 4.2 Corpus Generation receipts specifically do not:

```text
create Assertion Records
derive Evidence Topology
compute Convergence Geometry
emit Evidence Convergence Surfaces
emit Projection Layer outputs
perform RDGP reasoning
certify biological correctness
```

---

## Current Validation Milestones

```text
Phase 3 registration certification:
    passed

Phase 4.1 local lightweight-fixture validation:
    passed

Phase 4.1 MARK real-corpus six-unit benchmark smoketest:
    passed

Phase 4.1 Registration Unit architectural closure:
    certified

Phase 4.2 Corpus Generation Layer 1 validation:
    passed

Phase 4.2 Corpus Generation Layer 2 golden fixture validation:
    accepted

Phase 4.2 Corpus Generation Layer 3 MARK full-corpus validation:
    accepted

Phase 4.2 Corpus Generation architectural closure:
    certified
```

Current operational implication:

```text
The canonical six-unit Corpus Generation substrate is ready for Phase 4.3
Assertion Records.
```

Required Phase 4.3 input:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Phase 4.3 must consume the governed downstream input manifest.

Phase 4.3 must not crawl Registration Unit folders opportunistically.

---

## Future Receipt Families

Future Phase 4 receipt directories should be added only after the corresponding builder, validator, smoketest, or certification process executes.

Expected future receipt families include:

```text
phase4_assertion_records/
phase4_evidence_topology/
phase4_convergence_geometry/
phase4_evidence_convergence_surfaces/
phase4_projection_layer/
phase4_smoketest_certification/
```

Empty future receipt directories should not be created merely to satisfy planning expectations.

---

## Maintenance Rules

When new validation receipt families are added, update this README.

When new validation governance or certification documents are added, update:

```text
docs/validation/README.md
docs/validation/NAMESPACE.md
docs/status/phase4_validation_backlog.md
```

Do not add arbitrary runtime outputs to `results/validation/`.

Do not commit receipts without corresponding validation governance unless the receipt is explicitly transitional and documented.

Do not remove receipt archives that support certification documents.

Keep receipt directories stable and timestamped.

Keep latest convenience summary files synchronized with the accepted timestamped receipt directories.

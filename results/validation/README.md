# Validation Results

This directory contains git-tracked validation receipts for VDB.

Validation receipts are generated evidence from validation, certification, smoketest, or benchmark runs. They are retained when they support governance, reproducibility, benchmark evidence, certification evidence, or historical validation review.

This directory is not for disposable runtime scratch output.

---

## Receipt Directory Rule

A receipt directory may be tracked when it supports one or more of the following:

```text
certification evidence
benchmark evidence
reproducibility evidence
governance-supporting validation evidence
historical validation evidence
```

Receipt files do not define validation doctrine.

Validation doctrine and certification seed documents live under:

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
```

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

---

## Archive Verification

The MARK archive checksum uses the archive basename. Verify it from inside the archive directory:

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

---

## Scope Boundaries

The retained receipts prove validation behavior within their declared scope.

They may prove:

```text
registration integrity
read-only inspection behavior
deterministic artifact emission
readiness evaluation
non-mutation behavior
SQLite sidecar absence
benchmark-scale execution
certification evidence preservation
```

They do not prove:

```text
biological correctness
clinical interpretation
RDGP reasoning correctness
Corpus Generation correctness
Assertion Record correctness
Evidence Topology correctness
Convergence Geometry correctness
Evidence Convergence Surface correctness
Projection Layer correctness
TEP-VDB emission correctness
full Phase 4 certification
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
```

Current operational implication:

```text
The six-unit canonical Registration Unit substrate is ready for Phase 4.2
Corpus Generation development.
```

---

## Future Receipt Families

Future Phase 4 receipt directories should be added only after the corresponding builder, validator, smoketest, or certification process executes.

Expected future receipt families include:

```text
phase4_corpus_generation/
phase4_assertion_records/
phase4_evidence_topology/
phase4_convergence_geometry/
phase4_evidence_convergence_surfaces/
phase4_projection_layer/
phase4_smoketest_certification/
```

Empty future receipt directories should not be created merely to satisfy planning expectations.

---

## Maintenance Rule

When new validation receipt families are added, update this README.

When new validation governance or certification documents are added, update:

```text
docs/validation/README.md
docs/validation/NAMESPACE.md
```

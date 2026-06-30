# Phase 4.1 Registration Unit Validation Receipts

This directory contains Phase 4.1 Registration Unit validation receipts for VDB.

These receipts support validation governance for:

```text
docs/validation/registration_unit_validation.md
docs/validation/phase4_1_registration_unit_certification.md
```

They record evidence for Registration Unit declaration, read-only inspection, deterministic inventory emission, readiness evaluation, validation summary emission, non-mutation verification, and SQLite sidecar absence.

---

## Receipt Layout

```text
registration_unit_inventory.json
registration_unit_inventory.tsv
registration_unit_readiness.json
registration_unit_readiness.tsv
registration_unit_validation_run_summary.json
registration_unit_validation_summary.json
    Local lightweight-fixture Phase 4.1 validation receipts.

mark_full_corpus_smoketest_2026_06_30_052739/
    Extracted MARK real-corpus six-unit canonical benchmark smoketest receipts.

receipt_archives/
    Portable MARK smoketest archive and SHA256 checksum.
```

---

## Local Lightweight-Fixture Receipts

The root-level receipt files in this directory preserve the local Phase 4.1 lightweight-fixture validation run.

Current local verdict:

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

Purpose:

```text
Validate Phase 4.1 Registration Unit mechanics against a small deterministic
fixture with realistic Registration Unit structure.
```

---

## MARK Real-Corpus Six-Unit Benchmark Receipts

Timestamped receipt directory:

```text
mark_full_corpus_smoketest_2026_06_30_052739/
```

Contained files:

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

Current MARK verdict:

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

The MARK smoketest validated the six-unit canonical benchmark corpus:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Purpose:

```text
Validate that the same Phase 4.1 Registration Unit mechanics operate against
real canonical Phase 3 Registration Units at MARK scale without mutating the
source SQLite substrates.
```

---

## Portable Archive

Archive files:

```text
receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz
receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz.sha256
```

Archive SHA256:

```text
e1183821d1c0d0fe7219bdd323a76ed79eb4820bb94ba39b6f15d61c5a639957
```

Verify from the VDB repo root:

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

## Scope Boundary

These receipts prove Phase 4.1 Registration Unit validation behavior.

They support the claim that declared Registration Units can be:

```text
loaded from manifest
resolved deterministically
opened read-only
inspected structurally
summarized into deterministic inventory artifacts
evaluated for readiness
validated without SQLite mutation
validated without SQLite sidecar creation
```

They do not prove:

```text
biological correctness
clinical correctness
Corpus Generation correctness
Assertion Record correctness
Evidence Topology correctness
Convergence Geometry correctness
Evidence Convergence Surface correctness
Projection Layer correctness
TEP-VDB emission correctness
RDGP reasoning correctness
full Phase 4 certification
```

---

## Current Interpretation

Phase 4.1 Registration Unit validation is complete for the six-unit canonical benchmark corpus.

The six-unit canonical Registration Unit substrate is ready for Phase 4.2 Corpus Generation development.


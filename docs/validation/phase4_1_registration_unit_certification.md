# Phase 4.1 Registration Unit Certification Seed

**Status:** CERTIFIED

**Phase:** IV.1 — Registration Unit Declaration, Inspection, Inventory, Readiness, and Non-Mutation Validation

**Date:** 2026-06-30

---

## Purpose

This document records the Phase 4.1 MARK full-corpus Registration Unit smoketest for the Variant Database (VDB).

The objective of Phase 4.1 was to demonstrate that declared Phase 3 Registration Units can be loaded from a manifest, inspected read-only, summarized into deterministic inventory artifacts, evaluated for readiness, and verified as unmodified after validation.

This is a seed certification note intended to support later assembly of the full Phase 4 certification document.

---

## Certification Evidence

Primary evidence is preserved under:

```text
results/validation/phase4_registration_units/mark_full_corpus_smoketest_2026_06_30_052739/
```

Recommended archive preservation path:

```text
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz
results/validation/phase4_registration_units/receipt_archives/mark_full_corpus_smoketest_2026_06_30_052739.tgz.sha256
```

Archive SHA256:

```text
e1183821d1c0d0fe7219bdd323a76ed79eb4820bb94ba39b6f15d61c5a639957
```

The generated receipt set contains:

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

---

## Validation Corpus

The MARK smoketest evaluated six real canonical Phase 3 Registration Units:

| Registration Unit | Producer | Artifacts | Assertions | Source Identities | Readiness |
|---|---:|---:|---:|---:|---|
| `gsc_epilepsy` | GSC | 9 | 6 | 89,138 | ready |
| `gsc_mitochondrial_disease` | GSC | 9 | 6 | 85,434 | ready |
| `vap_hg002` | VAP | 16 | 10 | 97,369,849 | ready |
| `vap_median_ERR10619300` | VAP | 16 | 10 | 15,467,317 | ready |
| `vap_q1_ERR10619212` | VAP | 16 | 10 | 19,017,490 | ready |
| `vap_q3_ERR10619225` | VAP | 16 | 10 | 15,911,968 | ready |

---

## Validation Objectives

The Phase 4.1 validator evaluated the following invariants:

* Registration Unit manifest load succeeds.
* Six declared Registration Units are resolved from the manifest.
* SQLite files open successfully in read-only mode.
* SQLite query-only mode is enabled.
* Required registration tables are present.
* SQLite integrity checks pass.
* Inventory artifacts are emitted deterministically.
* Readiness artifacts are emitted deterministically.
* All Registration Units are marked ready.
* No source SQLite file is mutated during validation.
* No SQLite sidecar files are created during validation.

---

## Certification Results

Summary:

* `validation_status`: `passed`
* `record_count`: `6`
* `inspection_count`: `6`
* `inventory_row_count`: `6`
* `readiness_row_count`: `6`
* `ready_count`: `6`
* `not_ready_count`: `0`
* `inspection_status`: `passed`
* `inventory_artifact_status`: `passed`
* `readiness_artifact_status`: `passed`
* `non_mutation_status`: `passed`
* `sidecar_status`: `passed`
* `elapsed_seconds`: `888.55`

Certification Result:

**PASS**

---

## Architectural Findings

### 1. Real-Corpus Registration Unit Readiness Confirmed

All six canonical Phase 3 Registration Units were declared, inspected, inventoried, and marked ready for Phase 4.2 Corpus Generation.

### 2. Full-Scale Read-Only Inspection Confirmed

The smoketest operated against real MARK canonical Registration Units, including large VAP Registration Units with tens of millions of source identities.

### 3. Non-Mutation Boundary Confirmed

The validator did not mutate the source SQLite Registration Units. No file-size changes, modification-time changes, or SQLite sidecar creation events were detected.

---

## Scope of Certification

This certification applies specifically to Phase 4.1 Registration Unit validation.

It confirms successful:

* Registration Unit manifest declaration
* read-only inspection
* inventory emission
* readiness evaluation
* non-mutation verification
* SQLite sidecar absence

This certification does not evaluate biological correctness, construct Corpus Generations, derive Assertion Records, build Evidence Topology, compute Convergence Geometry, expose Evidence Convergence Surfaces, create Projection Views, or complete full Phase 4 certification.

---

## Conclusion

Phase 4.1 successfully demonstrates that the VDB can validate real canonical Phase 3 Registration Units as read-only, ready, non-mutated inputs for subsequent Phase 4 derived evidence layers.

**Certification Status:** PASS

**Recommendation:** Phase 4.1 may be considered complete for the six-unit canonical benchmark corpus and ready for progression into Phase 4.2 Corpus Generation.

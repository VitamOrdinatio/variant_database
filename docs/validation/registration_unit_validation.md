# Registration Unit Validation

## Purpose

This document defines validation requirements for Phase 4.1 Registration Units in the Variant Database (VDB).

Registration Unit validation verifies that declared Phase 4 Registration Units can be loaded, resolved, inspected read-only, inventoried deterministically, evaluated for readiness, and validated without mutating source SQLite files.

This document is a validation governance document.

This document is not a biological certification report.

This document is not a MARK full-corpus smoketest report.

This document is not a Corpus Generation validation document.

This document governs the Phase 4.1 Registration Unit validation layer.

---

# Scope

Registration Unit validation covers the following Phase 4.1 chain:

```text
Registration Unit input manifest
        ↓
manifest loading and validation
        ↓
filesystem path resolution
        ↓
read-only SQLite inspection
        ↓
deterministic Registration Unit inventory artifact emission
        ↓
Registration Unit readiness artifact emission
        ↓
validation run summary emission
        ↓
SQLite non-mutation verification
```

The implemented validation chain is represented by:

```text
src/variant_database/phase4/registration_units/manifest.py
src/variant_database/phase4/registration_units/inspection.py
src/variant_database/phase4/registration_units/inventory.py
src/variant_database/phase4/registration_units/readiness.py
src/variant_database/phase4/registration_units/validation.py
```

The corresponding test coverage is represented by:

```text
tests/phase4/test_registration_unit_manifest.py
tests/phase4/test_registration_unit_inspection.py
tests/phase4/test_registration_unit_inventory.py
tests/phase4/test_registration_unit_readiness.py
tests/phase4/test_registration_unit_validation.py
```

Current local implementation evidence:

```text
96 pytest tests passing
```

This local evidence supports Phase 4.1 Registration Unit validation readiness for the lightweight golden-fixture path.

Formal validation receipt generation remains required before Phase 4.1 local validation closure.

---

# Validation Authority Boundary

Registration Unit validation verifies preservation, structure, determinism, readiness, and non-mutation.

It does not verify biological correctness.

It does not perform evidence scoring.

It does not construct Corpus Generations.

It does not construct Assertion Records.

It does not derive Evidence Topology.

It does not construct Convergence Geometry.

It does not expose Evidence Convergence Surfaces.

It does not emit Projection Views.

It does not perform RDGP reasoning.

The Registration Unit layer preserves custody and exposes enough structural metadata for later Corpus Generation selection.

---

# Validation Inputs

## Required Input Manifest

The validator consumes a Registration Unit input manifest.

The manifest must conform to:

```text
docs/implementation/specifications/registration_unit_input_manifest_spec.md
```

The manifest declares Registration Units.

The manifest does not inspect SQLite files.

The manifest does not certify Registration Units.

The manifest does not mutate source files.

## Required Registration Unit SQLite Files

Each manifest row must resolve to a declared SQLite Registration Unit.

Each declared SQLite file must exist before inspection.

Each declared SQLite file must be inspected read-only.

Each declared SQLite file must remain unmodified after validation.

## Local Golden Fixture Input

The local lightweight validation path uses the Phase 4 Registration Unit golden fixture under:

```text
tests/fixtures/phase4/
```

The fixture contains representative lightweight Registration Units for:

```text
GSC epilepsy
GSC mitochondrial disease
VAP HG002
VAP median ERR10619300
VAP q1 ERR10619212
VAP q3 ERR10619225
```

The local fixture is suitable for validating deterministic behavior, structural inspection, readiness gates, artifact emission, and non-mutation behavior.

The local fixture does not replace MARK full-corpus smoketesting.

---

# Validation Outputs

A formal Phase 4.1 Registration Unit validation run should emit receipts under:

```text
results/validation/phase4_registration_units/
```

Expected receipt artifacts include:

```text
registration_unit_inventory.tsv
registration_unit_inventory.json
registration_unit_readiness.tsv
registration_unit_readiness.json
registration_unit_validation_summary.json
registration_unit_validation_run_summary.json
```

Additional README or Markdown summary files may be added if useful for human review.

Receipt artifacts should be git-tracked when they support governance, reproducibility, certification readiness, or historical validation evidence.

---

# Validation Gates

A Registration Unit validation run passes only if all required gates pass.

## Manifest Gates

The manifest validation layer must verify:

```text
manifest file exists
manifest is UTF-8 readable
manifest is tab-delimited
manifest header matches the required schema
manifest_schema_version is allowed
registration_unit_id values are non-empty
registration_unit_id values are unique
registration_unit_label values are non-empty
producer_family values are allowed
validation_layer values are allowed
source_role values are allowed
registration_backend values are allowed
expected_read_mode values are allowed
registration_unit_path values are non-empty
sqlite_path values are non-empty
declared paths resolve when filesystem validation is enabled
```

Failure of any required manifest gate fails the Registration Unit validation run.

## Read-Only Inspection Gates

The inspection layer must verify:

```text
declared SQLite files open successfully
SQLite files are opened in read-only mode
SQLite query_only mode is enabled
required Registration Unit tables are present
required columns are present in each required table
required table row counts are available
SQLite integrity_check returns ok
```

Required Registration Unit tables are:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
source_identities
```

Failure of any required read-only inspection gate fails the Registration Unit validation run.

## Inventory Artifact Gates

The inventory layer must verify:

```text
inventory rows are built from inspection results
one inventory row exists per declared Registration Unit
inventory rows sort deterministically by registration_unit_id
inventory TSV emits with stable columns
inventory JSON emits with stable schema
inventory row counts match inspection results
inventory artifact emission does not open or mutate SQLite files
```

Failure of any required inventory gate fails the Registration Unit validation run.

## Readiness Gates

The readiness layer must verify:

```text
registration_backend is sqlite
expected_read_mode is read_only
open_status is passed
query_only_status is enabled
required_table_status is passed
integrity_check_status is ok
inspection_status is passed
required table row counts are positive
```

A Registration Unit that fails any readiness gate must be marked:

```text
not_ready
```

A validation run containing one or more not-ready Registration Units must not be treated as passed.

## Validation Run Gates

The orchestration layer must verify:

```text
manifest loading succeeds
read-only inspection succeeds
inventory artifact emission succeeds
readiness artifact emission succeeds
validation run summary emits
all declared Registration Units are ready
SQLite source file mtimes are unchanged
SQLite source file sizes are unchanged
SQLite sidecar files are not created
```

Failure of any required validation run gate fails the Registration Unit validation run.

---

# Non-Mutation Requirements

Registration Unit validation must not mutate source Registration Unit SQLite files.

The validator must compare source SQLite file fingerprints before and after validation.

At minimum, non-mutation validation must check:

```text
SQLite file existence is unchanged
SQLite file size is unchanged
SQLite file mtime_ns is unchanged
SQLite sidecar state is unchanged
```

SQLite sidecars include:

```text
vdb.sqlite-wal
vdb.sqlite-shm
vdb.sqlite-journal
```

Creation of new SQLite sidecars during validation is a validation failure.

Modification of declared SQLite files during validation is a validation failure.

---

# Determinism Requirements

Registration Unit validation artifacts must be deterministic for the same input manifest and same source Registration Units.

Determinism requirements include:

```text
stable inventory row ordering
stable readiness row ordering
stable TSV headers
stable JSON keys
stable schema version labels
stable row counts
stable validation status fields
stable non-mutation report structure
```

Validation artifact determinism supports reproducibility, diff review, and governance traceability.

---

# Receipt Requirements

Formal Phase 4.1 validation receipts should preserve enough information to reconstruct:

```text
input manifest path
output receipt directory
declared Registration Unit count
inspection result count
inventory row count
readiness row count
ready Registration Unit count
not-ready Registration Unit count
inspection status
inventory artifact status
readiness artifact status
non-mutation status
sidecar status
overall validation status
before/after SQLite fingerprints
mutation details if present
sidecar details if present
authority boundary statement
```

The validation receipt must distinguish:

```text
passed validation run
failed validation run
ready Registration Unit
not-ready Registration Unit
local lightweight-fixture validation
future MARK full-corpus smoketest validation
```

Receipts must not claim biological correctness.

Receipts must not claim Phase 4 certification unless the corresponding certification document exists and the certification run has executed.

---

# Expected Local Validation Verdict

For the current lightweight golden-fixture path, the expected local validation verdict is:

```text
passed
```

Expected local validation properties:

```text
six Registration Units declared
six Registration Units inspected
six inventory rows emitted
six readiness rows emitted
six Registration Units marked ready
zero Registration Units marked not_ready
SQLite non-mutation status passed
SQLite sidecar status passed
overall validation status passed
```

This expected verdict is local to the lightweight golden fixture.

It does not replace MARK full-corpus smoketesting.

---

# MARK Full-Corpus Smoketest Boundary

MARK full-corpus smoketesting remains a later certification-strength validation target.

The local lightweight fixture validates implementation mechanics.

The MARK full-corpus smoketest should validate that the same Phase 4.1 Registration Unit validation chain can execute against the canonical Phase 3 Registration Unit corpus at production scale.

MARK full-corpus smoketesting should verify:

```text
canonical Phase 3 Registration Unit paths resolve
large SQLite Registration Units open read-only
inspection completes without mutation
inventory artifacts emit deterministically
readiness artifacts emit deterministically
validation summary emits
SQLite source files remain unmodified
SQLite sidecars are not created
```

MARK full-corpus smoketesting should be documented separately as a validation receipt or certification-strength report.

---

# Failure Semantics

A Registration Unit validation run must fail if:

```text
the manifest cannot be loaded
the manifest schema is invalid
a required manifest value is invalid
a declared filesystem path does not resolve
a declared SQLite file cannot be opened read-only
SQLite query_only mode is not enabled
a required table is missing
a required column is missing
SQLite integrity_check does not return ok
required row counts are unavailable
required row counts are not positive
inventory artifacts cannot be emitted
readiness artifacts cannot be emitted
one or more Registration Units are not ready
the validation run summary cannot be emitted
a source SQLite file is mutated
a SQLite sidecar is created or changed
```

Failure must be explicit.

Failure must not be silently downgraded to a warning.

Warnings may be used for non-blocking informational findings, but warnings must not obscure failed validation gates.

---

# Anti-Collapse Safeguards

Registration Unit validation must not collapse:

```text
manifest declaration into SQLite inspection
SQLite inspection into biological validation
inventory artifact into readiness verdict
readiness verdict into certification
local fixture validation into MARK full-corpus validation
Phase 3 registration certification into Phase 4 validation
Registration Unit validation into Corpus Generation validation
source SQLite file into disposable runtime output
validation receipt into validation doctrine
validation doctrine into validation receipt
```

The Registration Unit validator proves that declared Registration Units are structurally inspectable and operationally ready for Phase 4.2 Corpus Generation handoff.

It does not prove that downstream layers are implemented.

It does not prove that source producer evidence is biologically correct.

---

# Phase 4.1 Completion Criteria

Phase 4.1 Registration Unit validation can be considered locally complete when:

```text
docs/validation/registration_unit_validation.md exists
Registration Unit manifest handling is implemented
read-only Registration Unit inspection is implemented
deterministic inventory artifact emission is implemented
readiness artifact emission is implemented
validation orchestration is implemented
full test suite passes
formal validation receipts exist under results/validation/phase4_registration_units/
validation receipts show overall validation_status passed
validation receipts show all declared local fixture Registration Units ready
validation receipts show SQLite non-mutation status passed
validation receipts show SQLite sidecar status passed
```

Phase 4.1 local validation completion does not require:

```text
Corpus Generation implementation
Assertion Record implementation
Evidence Topology implementation
Convergence Geometry implementation
Evidence Convergence Surface implementation
Projection Layer implementation
RDGP-facing projection implementation
MARK full-corpus smoketest certification
full Phase 4 certification
```

---

# Summary

Registration Unit validation governs the first executable Phase 4 layer.

The validator must prove that declared Registration Units can be loaded, resolved, inspected read-only, inventoried deterministically, evaluated for readiness, summarized, and checked for non-mutation.

The current local implementation evidence is positive:

```text
96 pytest tests passing
```

The next required step is to generate and preserve formal Phase 4.1 validation receipts under:

```text
results/validation/phase4_registration_units/
```

Only after those receipts exist and pass should Phase 4.1 local Registration Unit validation be marked complete.

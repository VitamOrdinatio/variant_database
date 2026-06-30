# Corpus Generation Validation

**Status:** PLANNED REQUIRED

**Phase:** IV.2 — Corpus Generation Scope Declaration Validation

**Required Before:** Phase 4.2 Corpus Generation completion

---

## Purpose

This document defines validation requirements for VDB Phase 4.2 Corpus Generation.

A Corpus Generation is a deterministic, named, reconstructable declaration of Registration Unit membership for a downstream derived-evidence build.

The purpose of Corpus Generation validation is to prove that VDB can declare an explicit evidence scope before constructing Assertion Records, Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, or TEP-VDB outputs.

Core invariant:

```text
Corpus Generation freezes scope before VDB derives evidence.
```

A folder of Registration Units is not a Corpus Generation.

A Corpus Generation must be declared, policy-backed, receipt-backed, and reconstructable.

---

## Scope

This validation applies to the Phase 4.2 Corpus Generation layer.

It validates:

```text
Corpus Generation identity
selection policy declaration
selection manifest declaration
Registration Unit inclusion
Registration Unit exclusion when relevant
Registration Unit readiness visibility
deterministic corpus manifest emission
deterministic downstream Assertion Record input manifest emission
non-mutation behavior
anti-collapse safeguards
```

It does not validate:

```text
Registration Unit creation
Registration Unit repair
Registration Unit recertification
Assertion Record construction
Evidence Topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
Projection View generation
TEP-VDB emission
RDGP reasoning
biological interpretation
clinical interpretation
```

---

## Authority Boundary

Corpus Generation declares evidence scope.

It does not create source authority.

It does not reinterpret producer assertions.

It does not merge Registration Units into a single opaque evidence source.

It does not convert inclusion into confidence.

It does not convert exclusion into biological irrelevance.

It does not derive topology.

It does not reason.

Required authority boundary:

```text
Registration Units preserve custody.
Registration Unit readiness verifies safe consumption.
Corpus Generations declare scope.
Assertion Records preserve scientific claims.
```

---

## Required Inputs

Corpus Generation validation expects an implementation to consume explicit, declared inputs.

Required inputs include:

```text
Registration Unit readiness inventory
Corpus Generation selection manifest
Corpus Generation selection policy
Corpus Generation validation policy
Corpus Generation schema or contract version
builder name
builder version when available
build timestamp or deterministic timestamp policy
```

The selection manifest declares intended scope.

The selection policy explains why those Registration Units are selected.

The readiness inventory or equivalent Phase 4.1 receipt-backed input establishes that selected Registration Units are safe to consume.

Filesystem traversal may support discovery.

Filesystem traversal must not define corpus scope.

---

## Required Corpus Generation Identity

Every Corpus Generation must have stable identity.

Validation must confirm presence of:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version when applicable
selection_policy_id
selection_policy_version when applicable
builder_name
builder_version when available
build_timestamp or deterministic timestamp policy
validation_status
certification_status when available
```

For the initial MARK benchmark corpus, the expected identity is:

```text
corpus_generation_id: mark_phase4_corpus_6tep_v1
corpus_generation_label: MARK Phase 4 6-TEP Benchmark Corpus v1
corpus_generation_purpose: initial certified multi-producer Phase 4 benchmark corpus
corpus_generation_version: v1
selection_policy_id: mark_phase4_6tep_certified_input_policy
selection_policy_version: v1
```

If a different identifier is selected during implementation, the identifier must be explicit, stable, and documented.

---

## Required Selection Policy Validation

Every Corpus Generation must declare a selection policy.

Validation must confirm that the selection policy defines:

```text
eligible Registration Units
selected Registration Units
excluded Registration Units when relevant
required validation status
required certification status when applicable
producer families in scope
evidence domains in scope when applicable
temporal or generation constraints when applicable
inclusion rationale requirements
exclusion rationale requirements
failure behavior
```

For the initial MARK benchmark corpus, the selection policy should state:

```text
Select the six certified Phase 3 MARK Registration Units representing
two GSC semantic evidence packages and four VAP variant evidence packages
for initial Phase 4 multi-producer benchmark derivation.
```

The selection policy must not be replaced by an informal file list.

---

## Required Inclusion Validation

A Corpus Generation must explicitly declare every included Registration Unit.

For each included Registration Unit, validation must confirm:

```text
registration_unit_id
registration_unit_label
registration_unit_path or resolvable reference
producer_family
source_package_id when available
registration_backend
validation_status
certification_status when available
inclusion_status
inclusion_rationale
```

Validation must also confirm:

```text
at least one Registration Unit is included
each included Registration Unit is unique
each included Registration Unit resolves successfully
each included Registration Unit is readable
each included Registration Unit is ready
Registration Unit boundaries are preserved
producer_family labels are preserved
included Registration Units remain individually identifiable
```

Allowed inclusion statuses may include:

```text
included
included_with_note
included_for_fixture
included_for_failure_mode
```

Allowed inclusion rationales may include:

```text
certified Phase 3 benchmark input
producer-family representation
evidence-domain representation
cohort representation
heavy smoketest coverage
consumer projection readiness testing
release-corpus inclusion
failure-mode testing
synthetic fixture inclusion
```

---

## Required Exclusion Validation

A Corpus Generation should explicitly declare excluded Registration Units when exclusion affects interpretation of corpus scope.

For each relevant excluded Registration Unit or candidate, validation should confirm:

```text
registration_unit_id or candidate reference
registration_unit_label when available
registration_unit_path or resolvable reference when available
observed_producer_family when available
observed_validation_status when available
observed_certification_status when available
exclusion_status
exclusion_rationale
observed_failure_reason when applicable
```

Allowed exclusion statuses may include:

```text
excluded
excluded_uncertified
excluded_failed_validation
excluded_out_of_scope
excluded_duplicate
excluded_superseded
excluded_missing
excluded_unreadable
deferred
not_evaluated
```

Allowed exclusion rationales may include:

```text
uncertified Registration Unit
failed validation
out-of-scope producer family
out-of-scope cohort
out-of-scope evidence domain
duplicate or superseded Registration Unit
missing path
unreadable backend
explicitly deferred input
reserved for expanded corpus
outside declared benchmark scope
```

A Corpus Generation must not silently omit Registration Units when omission affects scope interpretation.

---

## Required Output Artifacts

A valid Corpus Generation implementation must emit deterministic sidecar artifacts outside the selected Registration Units.

Expected Phase 4.2 build outputs include:

```text
corpus_generation_manifest.tsv
corpus_generation_manifest.json
corpus_generation_report.md
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
downstream_assertion_record_input_manifest.tsv
```

Recommended initial build output directory:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

Corpus Generation output paths must not be confused with Registration Unit source paths.

Corpus Generation artifacts do not replace Registration Units.

Corpus Generation artifacts do not create Assertion Records.

Corpus Generation artifacts do not define topology, geometry, surfaces, projections, or biological interpretation.

---

## Required Corpus Manifest Validation

The Corpus Generation manifest must preserve enough information to reconstruct the selected evidence scope.

Validation must confirm that the manifest preserves:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version when applicable
selection_policy_id
selection_policy_version when applicable
included_registration_units
excluded_registration_units when applicable
producer_family_summary
package_summary
artifact_count_summary
assertion_registration_count_summary
source_identity_count_summary
namespace_count_summary when available
validation_status_summary
certification_status_summary
build_timestamp
builder_name
builder_version when available
manifest_schema_version when available
```

The manifest must be deterministic under fixed inputs.

The manifest must reconstruct the exact selected Registration Unit set.

The manifest must not become source truth.

---

## Required Downstream Handoff Validation

Corpus Generation provides the declared input scope for Phase 4.3 Assertion Record indexing.

A valid Corpus Generation must emit or support a downstream Assertion Record input manifest containing:

```text
corpus_generation_id
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id when available
registration_backend
assertion_registration_count when available
source_identity_count when available
validation_status
certification_status when available
```

Validation must confirm that this downstream manifest is:

```text
deterministic
complete for included Registration Units
traceable to the Corpus Generation manifest
sufficient for Assertion Record indexing
free of Assertion Record payloads
```

The downstream Assertion Record input manifest is not an Assertion Record index.

---

## Required Non-Mutation Validation

Corpus Generation construction may inspect Registration Units and readiness inventories.

It must not mutate Registration Unit SQLite files.

Validation must confirm:

```text
selected SQLite files exist before validation
selected SQLite files exist after validation
selected SQLite file sizes are unchanged
selected SQLite modification times are unchanged
no vdb.sqlite-wal files are created
no vdb.sqlite-shm files are created
no vdb.sqlite-journal files are created
```

If sidecars are present before execution, validation must report them explicitly.

If new sidecars are created during execution, validation must fail unless an explicit failure-mode test declares that behavior expected.

---

## Determinism Requirements

Corpus Generation outputs must be deterministic under fixed inputs.

Given the same:

```text
Registration Unit readiness inventory
Corpus Generation selection manifest
selection policy
validation policy
contract version
builder version
Registration Unit contents
```

the builder should produce equivalent:

```text
included Registration Unit list
excluded Registration Unit list when applicable
inclusion rationale records
exclusion rationale records when applicable
summary counts
validation status summaries
certification status summaries
manifest records
validation outcomes
report sections
downstream Assertion Record input manifest
```

Filesystem traversal order must not define Corpus Generation scope.

Output order must be stable.

Recommended ordering:

```text
explicit selection manifest order
```

If sorted output is used, the sorting policy must be declared.

---

## Required Validation Receipts

Corpus Generation validation receipts should be written under:

```text
results/validation/phase4_corpus_generation/
```

Expected receipt files may include:

```text
corpus_generation_validation_run_summary.json
corpus_generation_validation_summary.json
corpus_generation_manifest_validation.tsv
corpus_generation_membership_validation.tsv
corpus_generation_exclusion_validation.tsv
corpus_generation_non_mutation_summary.json
corpus_generation_determinism_summary.json
```

Receipt names may evolve during implementation.

Receipts must preserve enough information to reconstruct:

```text
input selection manifest
input readiness inventory
selection policy
validation policy
builder identity
validator identity
build output location
validation output location
included Registration Units
excluded Registration Units when relevant
validation findings
validation limitations
determinism evidence
non-mutation evidence
anti-collapse evidence
```

Empty future receipt directories should not be created before validation execution.

---

## Initial Local Validation Target

The initial local validation target should use small synthetic or fixture Registration Unit inputs.

Local validation must prove:

```text
selection manifest is required
selection policy is required
missing Registration Units are rejected
duplicate Registration Units are rejected
unready Registration Units are rejected
included Registration Units are explicit
inclusion rationale is preserved
exclusion rationale is preserved when applicable
Corpus Generation identity is stable
manifest outputs are deterministic
downstream Assertion Record input manifest is deterministic
Registration Units are not mutated
SQLite sidecars are not created
Assertion Records are not created
Topology is not derived
```

Local validation may use lightweight fixtures.

Local validation does not replace MARK benchmark validation.

---

## Initial MARK Benchmark Validation Target

The initial MARK benchmark validation target is the six-unit canonical benchmark corpus.

Expected Corpus Generation identity:

```text
mark_phase4_corpus_6tep_v1
```

Expected included Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Validation must confirm:

```text
expected six Registration Units are present
expected four VAP Registration Units are present
expected two GSC Registration Units are present
all expected Registration Units are readable
all expected Registration Units are ready
all expected Registration Units preserve producer_family
corpus_generation_id is stable
selection_policy_id is stable
corpus manifest is deterministic
downstream Assertion Record input manifest is deterministic
Registration Units are not mutated
SQLite sidecars are not created
```

This benchmark Corpus Generation is not a claim that all available VAP SRA-derived TEPs have been registered or included.

It is the initial six-unit benchmark corpus for Phase 4 derived-evidence layer development.

---

## Failure Modes

Corpus Generation validation must fail when:

```text
selection manifest is missing
selection policy is missing
corpus_generation_id is missing
included Registration Unit list is empty
included Registration Unit is duplicated
included Registration Unit cannot be resolved
included Registration Unit is unreadable
included Registration Unit is not ready
required producer_family does not match
required backend does not match
manifest output is nondeterministic
downstream Assertion Record input manifest is missing
Registration Unit SQLite file is mutated
SQLite sidecar is created unexpectedly
Assertion Records are created inside Corpus Generation
Evidence Topology is derived inside Corpus Generation
biological interpretation appears in Corpus Generation output
```

Validation may report warnings when:

```text
certification status is unavailable
namespace summaries are unavailable
exclusion records are not applicable
builder version is unavailable
storage-footprint summaries are unavailable
```

Warnings must not silently become pass conditions when required evidence is absent.

---

## Anti-Collapse Safeguards

Corpus Generation validation must prevent:

```text
folder listing treated as Corpus Generation
Corpus Generation treated as source truth
Corpus Generation treated as evidence confidence
Corpus inclusion treated as biological support
Corpus exclusion treated as biological irrelevance
Registration Unit boundaries collapsed
producer-family labels collapsed
package identity collapsed
artifact identity collapsed
assertion registration identity collapsed
source identity identity collapsed
validation status collapsed
certification status collapsed
inclusion rationale collapsed
exclusion rationale collapsed
Assertion Records created before corpus scope is declared
Topology derived before corpus scope is declared
Geometry created inside Corpus Generation
Surface eligibility declared inside Corpus Generation
Projection output replacing Corpus Generation
RDGP reasoning performed inside Corpus Generation
destructive modification of Registration Units during Corpus Generation
```

Any implementation that performs one of these actions violates Phase 4.2 validation expectations.

---

## Completion Criteria

Phase 4.2 Corpus Generation may be considered validation-complete when:

```text
docs/validation/corpus_generation_validation.md exists
explicit selection manifest format exists
selection policy is declared
Corpus Generation identity is stable
included Registration Units are explicit
included Registration Units are resolvable
included Registration Units are readable
included Registration Units are ready
Registration Unit boundaries are preserved
producer-family context is preserved
inclusion rationale is documented
exclusion rationale is documented when applicable
machine-readable Corpus Generation manifest is emitted
human-readable Corpus Generation report is emitted
Corpus Generation validation report is emitted
downstream Assertion Record input manifest is emitted
outputs are deterministic under fixed inputs
Corpus Generation does not mutate Registration Units
Corpus Generation does not create SQLite sidecars
Corpus Generation does not become source truth
Corpus Generation does not create Assertion Records
Corpus Generation does not derive topology
anti-collapse safeguards pass
local validation receipts exist
MARK benchmark validation receipts exist
```

Phase 4.2 is not complete merely because a file list exists.

Phase 4.2 is complete only when the declared Corpus Generation satisfies the Corpus Generation contract and can safely define the evidence universe for downstream Phase 4 derivation.

---

## Summary

Corpus Generation validation proves that VDB declares scope before deriving evidence.

The guiding rule is:

```text
Declare the scope.
Apply policy.
Preserve Registration Unit boundaries.
Document inclusion.
Document exclusion.
Emit deterministic manifests.
Do not mutate.
Do not derive.
Do not interpret.
```

Phase 4.2 validation must ensure that every downstream derived evidence layer begins from a declared, reconstructable, receipt-backed Corpus Generation.

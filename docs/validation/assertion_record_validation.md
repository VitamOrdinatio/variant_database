# Assertion Record Validation

**Status:** ACTIVE PHASE 4.3 VALIDATION GOVERNANCE

**Phase:** IV.3 — Assertion Records

**Primary Contract:** `docs/contracts/assertion_records/assertion_record_contract.md`

**Primary Schema:** `docs/implementation/schemas/assertion_record_schema.md`

**Primary Specification:** `docs/implementation/specifications/assertion_record_spec.md`

**Implementation Plan:** `docs/implementation/plans/assertion_record_plan.md`

**Primary Build Output Family:** `results/phase4/assertion_records/`

**Primary Validation Receipt Family:** `results/validation/phase4_assertion_records/`

---

## Purpose

This document defines the validation governance for VDB Phase 4.3 Assertion Record preservation.

Assertion Record validation proves that VDB can consume a declared Corpus Generation, inspect selected Registration Units read-only, preserve producer scientific claims as corpus-indexed Assertion Records, reconcile indexing coverage, emit deterministic claim-layer artifacts, and preserve authority boundaries.

Assertion Record validation confirms preservation, reconstructability, reconciliation, determinism, non-mutation, and anti-collapse behavior.

Assertion Record validation does not prove biological correctness.

Assertion Record validation does not derive Evidence Topology.

Assertion Record validation does not characterize Convergence Geometry.

Assertion Record validation does not construct Evidence Convergence Surfaces.

Assertion Record validation does not emit Projection Views.

Assertion Record validation does not perform RDGP reasoning.

---

# Validation Role

The governing Phase 4.3 transition is:

```text
Registration Units
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
```

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.
```

Assertion Record validation proves that the Assertion Record layer obeys this boundary.

It validates the transition from governed scope into preserved claim records.

It must not validate topology, geometry, surfaces, projections, biological reasoning, clinical interpretation, or causality.

---

# Scope

This validation document applies to Assertion Record artifacts derived from:

```text
VAP Registration Units
GSC Registration Units
future RSP Registration Units
future RDGP-returned Registration Units
future TEP-VDB products
future TEP-RDGP products
future external evidence capsules
future producer evidence packages
future reasoning producer outputs
```

The initial Phase 4.3 validation target is:

```text
mark_phase4_corpus_6tep_v1_assertion_record_index
```

Input Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Required upstream Phase 4.2 handoff artifact:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Expected Assertion Record build output family:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

Expected validation receipt family:

```text
results/validation/phase4_assertion_records/
```

---

# Non-Goals

Assertion Record validation does not validate:

```text
Registration Unit creation
Registration Unit repair
Registration Unit migration
Registration Unit recertification
Corpus Generation selection
Corpus Generation certification
Evidence Topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
Projection View generation
cross-producer confidence aggregation
clinical interpretation
causal interpretation
RDGP reasoning
biological truth assignment
```

Assertion Record validation is preservation validation.

It is not topology validation.

It is not reasoning validation.

It is not biological certification.

---

# Required Inputs

Assertion Record validation requires explicit inputs.

The validator must not discover scope opportunistically.

Required inputs include:

```text
Corpus Generation manifest
downstream Assertion Record input manifest
Assertion Record Index manifest
Assertion Record index
Assertion Record participant table
Assertion Record relationship table
Assertion Record evidence basis table
Assertion Record context table
Assertion Record lineage table
Assertion Record payload reference table
downstream topology input manifest
selected Registration Unit references
Assertion Record schema version
Assertion Record contract version
Assertion Record indexing policy
producer resolver policy
validation policy
builder name
builder version
validator name
validator version when available
```

For the initial MARK target, the required upstream handoff is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Assertion Record validation must fail or explicitly report unresolved state if the declared Corpus Generation input is unavailable.

Assertion Record validation must fail or explicitly report unresolved state if the downstream Assertion Record input manifest is unavailable.

Assertion Record validation must not substitute filesystem traversal for declared Corpus Generation scope.

---

# Required Build Artifacts

Phase 4.3 build artifacts should be emitted outside selected Registration Units.

Expected build artifacts include:

```text
assertion_record_index_manifest.tsv
assertion_record_index_manifest.json
assertion_record_index.tsv
assertion_record_index.jsonl
assertion_record_participants.tsv
assertion_record_relationships.tsv
assertion_record_evidence_basis.tsv
assertion_record_context.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
assertion_record_index_report.md
downstream_topology_input_manifest.tsv
```

These artifacts are Assertion Record artifacts.

They do not replace Registration Units.

They do not replace Corpus Generations.

They do not create Evidence Topology.

They do not create Convergence Geometry.

They do not create Evidence Convergence Surfaces.

They do not create Projection Views.

They do not perform biological reasoning.

---

# Required Validation Receipts

Assertion Record validation receipts must be emitted separately from Assertion Record build artifacts.

Validation receipt family:

```text
results/validation/phase4_assertion_records/
```

Expected validation receipt artifacts include:

```text
assertion_record_validation_report.json
assertion_record_validation_report.tsv
assertion_record_validation_summary.json
assertion_record_validation_summary.tsv
```

Expected timestamped validation receipt directories may include:

```text
lightweight_fixture_smoketest_<timestamp>/
golden_fixture_smoketest_<timestamp>/
mark_full_corpus_smoketest_<timestamp>/
receipt_archives/
```

Validation receipts record what was proven during validation execution.

They do not replace Assertion Record build artifacts.

They do not replace Registration Units.

They do not replace Corpus Generations.

---

# Validation Report Shape

The validation report should include:

```text
validation_report_id
validation_report_label
assertion_record_index_id
corpus_generation_id
assertion_record_index_manifest_reference
assertion_record_index_reference
participant_table_reference
relationship_table_reference
evidence_basis_table_reference
context_table_reference
lineage_table_reference
payload_reference_table_reference
downstream_topology_input_manifest_reference
validation_policy_id
validation_policy_version
validator_name
validator_version when available
validation_timestamp
overall_validation_status
selected_registration_unit_count
source_assertion_registration_count
indexed_assertion_record_count
indexed_with_note_count
unsupported_assertion_registration_count
deferred_assertion_registration_count
failed_assertion_registration_count
not_applicable_assertion_registration_count
not_evaluated_assertion_registration_count
producer_resolver_coverage_summary
duplicate_source_assertion_key_count
unresolved_source_assertion_key_count
determinism_status
non_mutation_status
anti_collapse_status
validation_findings
validation_limitations
```

The TSV validation report may represent one validation finding per row.

The JSON validation report may include nested findings grouped by validation tier, artifact, Registration Unit, producer family, assertion type, or validation finding class.

---

# Validation Finding Fields

Recommended validation finding fields:

| Field | Description |
| ----- | ----------- |
| `finding_id` | Stable finding identifier when available. |
| `assertion_record_index_id` | Assertion Record Index identity. |
| `corpus_generation_id` | Corpus Generation identity. |
| `registration_unit_id` | Registration Unit identity when applicable. |
| `assertion_id` | Assertion Record identity when applicable. |
| `source_assertion_key` | Source assertion key when applicable. |
| `producer_family` | Producer family when applicable. |
| `assertion_type` | Assertion type when applicable. |
| `finding_tier` | Validation tier. |
| `finding_type` | Type of validation finding. |
| `finding_severity` | Severity of finding. |
| `finding_status` | Status of finding. |
| `field_name` | Field affected when applicable. |
| `observed_value` | Observed value when useful. |
| `expected_value` | Expected value when useful. |
| `finding_message` | Human-readable finding message. |

Allowed finding tiers:

```text
input_validation
record_validation
participant_validation
relationship_validation
evidence_basis_validation
context_validation
lineage_validation
payload_reference_validation
reconciliation_validation
determinism_validation
non_mutation_validation
downstream_handoff_validation
anti_collapse_validation
mark_benchmark_validation
```

Allowed finding severities:

```text
info
note
warning
error
critical
```

---

# Three-Layer Validation Strategy

Phase 4.3 should use the same three-layer validation pattern established for Phase 4.2.

```text
Layer 1:
    local synthetic tests and implementation unit/integration tests

Layer 2:
    compressed real-row golden fixture derived from the canonical six-unit corpus

Layer 3:
    MARK full-corpus validation against mark_phase4_corpus_6tep_v1
```

The three layers validate the same architectural commitments at different scales.

Layer 1 proves local mechanics.

Layer 2 proves real-world-derived resolver behavior on a compressed fixture.

Layer 3 proves full-corpus execution against the canonical MARK benchmark corpus.

---

# Layer 1: Local Synthetic Validation

Layer 1 should use synthetic controlled fixtures and local tests.

Layer 1 validates:

```text
builder requires Corpus Generation input
builder requires downstream Assertion Record input manifest
builder rejects opportunistic Registration Unit discovery
builder preserves corpus_generation_id
builder preserves registration_unit_id
builder preserves producer_family
builder preserves source_package_id
builder preserves source_artifact_reference
builder generates stable assertion_id values
builder generates stable source_assertion_key values
builder preserves role-bearing participants
builder preserves relationship or relationship class
builder preserves evidence basis or explicit absence
builder preserves context or explicit absence
builder preserves lineage
builder preserves authority context
builder preserves uncertainty context
builder preserves payload reconstruction limitations
builder reports unsupported assertion types
builder reports deferred assertions
builder reports failed assertions
builder emits downstream_topology_input_manifest.tsv
builder does not mutate Registration Units
builder does not create topology
builder does not characterize geometry
builder does not construct surfaces
builder does not emit projections
builder does not perform biological reasoning
```

Layer 1 should include tests for deterministic ordering, duplicate source assertion key handling, unresolved state representation, and anti-collapse safeguards.

Layer 1 may use synthetic Registration Unit fixtures.

Layer 1 must not be treated as sufficient for Phase 4.3 closure.

---

# Layer 2: Compressed Real-Row Golden Fixture Validation

Phase 4.3 requires a new Layer 2 fixture.

The Layer 2 fixture should be derived from the canonical six-unit Corpus Generation but compressed around assertion-bearing structures.

Recommended fixture identity:

```text
phase4_3_assertion_record_golden_fixture_v1
```

Recommended fixture scope:

```text
2 GSC Registration Unit slices
4 VAP Registration Unit slices
assertion registration rows
source artifact rows
source identity rows needed for participant and evidence reconstruction
minimal package and registration metadata
expected resolver output snapshots
expected validation summary snapshots
```

Recommended fixture location:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
```

Layer 2 validation should prove:

```text
VAP resolver works against compressed real VAP assertion registrations
GSC resolver works against compressed real GSC assertion registrations
assertion counts reconcile to fixture Registration Units
unsupported assertion registrations are counted
deferred assertion registrations are counted
failed assertion registrations are counted
participants are role-bearing
relationships are explicit
evidence basis is reconstructable or explicitly absent
context is reconstructable or explicitly absent
lineage points back to Corpus Generation and Registration Units
payload references resolve or expose reconstruction limitations
outputs are deterministic
anti-collapse checks pass
```

Expected Layer 2 validation receipt family:

```text
results/validation/phase4_assertion_records/golden_fixture_smoketest_<timestamp>/
```

Layer 2 fixture records are validation fixtures.

They are not canonical build artifacts.

They are not substitutes for MARK full-corpus validation.

---

# Layer 3: MARK Full-Corpus Validation

Layer 3 validates Assertion Record indexing against the canonical six-unit MARK Corpus Generation.

Layer 3 must consume:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Layer 3 expected build output:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

Layer 3 expected validation receipt family:

```text
results/validation/phase4_assertion_records/mark_full_corpus_smoketest_<timestamp>/
```

Layer 3 validation should prove:

```text
all six selected Registration Units are consumed from the governed manifest
all selected Registration Units are inspected read-only
VAP assertion registrations are resolved or explicitly reported
GSC assertion registrations are resolved or explicitly reported
Assertion Record identities are stable
source assertion keys are stable or explicitly unresolved
assertion counts reconcile to Registration Unit inputs when applicable
unsupported assertion registrations are reported
deferred assertion registrations are reported
failed assertion registrations are reported
producer resolver coverage is reported
validation report is deterministic
downstream_topology_input_manifest.tsv is emitted
Registration Units are not mutated
no topology authority is embedded
no geometry authority is embedded
no surface authority is embedded
no projection authority is embedded
no RDGP reasoning authority is embedded
no biological truth authority is embedded
```

Layer 3 validates MARK execution behavior.

Layer 3 does not certify full Phase 4.

---

# Required Input Validation

Input validation confirms that the declared Corpus Generation and selected Registration Units are available.

Validation must check:

```text
input Corpus Generation exists
corpus_generation_id is declared
Corpus Generation manifest is readable
downstream Assertion Record input manifest exists
selected Registration Units are explicit
selected Registration Units are resolvable
selected Registration Units are readable
selected Registration Units expose assertion registrations or explicit absence
Registration Unit boundaries are preserved
producer families are declared
source package references are declared or explicitly unresolved
Registration Unit validation status is visible
Registration Unit certification status is visible when available
Registration Unit readiness status is visible when available
```

Assertion Record indexing must not silently select inputs.

Assertion Record validation must not silently expand Corpus Generation scope.

---

# Required Assertion Record Validation

Record validation confirms that each Assertion Record satisfies preservation obligations.

Validation must check:

```text
assertion_record_index_id exists
assertion_id exists
source_assertion_key exists or is explicitly unresolved
assertion_type exists
producer identity exists
producer_family exists
registration_unit_id is traceable
corpus_generation_id is traceable
source_package reference is traceable or explicitly unresolved
source_artifact reference is traceable or explicitly unresolved
source assertion registration reference is traceable or explicitly unresolved
relationship or relationship class is present
participant resolution status is present
evidence basis resolution status is present
context resolution status is present
authority context is visible or explicitly unresolved
uncertainty context is visible or explicitly unresolved
payload reference status is visible
indexing_status is present
validation_status is present
builder_name is present
indexed_at is present or explicitly unresolved during fixture generation
```

Assertion Records must preserve producer claims.

They must not represent VDB belief.

---

# Required Participant Validation

Participant validation confirms that participants are preserved as role-bearing components.

Validation must check:

```text
participant table exists
participant records reference valid assertion_id values
participant_role is explicit
participant_kind is visible or explicitly unresolved
participant_namespace is visible or explicitly unresolved
participant_value is visible or explicitly unresolved
source_identity_reference is visible or explicitly unresolved when applicable
source_artifact_reference is visible or explicitly unresolved
source_record_reference is visible or explicitly unresolved when applicable
producer_family is preserved
participant resolution status is present
participant validation status is present
```

Participants must not be silently collapsed into canonical identities.

Producer-native participant identities must remain visible.

Canonical identifiers may be attached separately through namespace governance.

---

# Required Relationship Validation

Relationship validation confirms that relationships are explicit and claim-preserving.

Validation must check:

```text
relationship table exists
relationship records reference valid assertion_id values
relationship_type exists
relationship_label is visible or explicitly unresolved when applicable
relationship_directionality is visible or explicitly not_applicable when applicable
relationship_arity is visible or explicitly unresolved when applicable
relationship_class is visible or explicitly unresolved when applicable
relationship_context is visible or explicitly unresolved when applicable
producer_family is preserved
assertion_type is preserved
relationship validation status is present
```

Relationships may be unary, binary, or higher-order.

Validation must not require all assertions to collapse into subject-predicate-object triples.

Relationship preservation does not imply biological correctness.

---

# Required Evidence Basis Validation

Evidence basis validation confirms that the evidence carrying or supporting the producer claim is reconstructable or explicitly absent.

Validation must check:

```text
evidence basis table exists
evidence basis records reference valid assertion_id values
evidence_basis_type exists
evidence_basis_reference is visible or explicitly unresolved
source_artifact_reference is visible or explicitly unresolved
source row, record, table, or file references are visible when available
source method, score, count, threshold, or validation result are preserved when available
producer payload reference is preserved when applicable
external snapshot reference is preserved when applicable
evidence basis resolution status is present
evidence basis validation status is present
```

Evidence basis must not be replaced by opaque summaries.

A missing evidence basis must be represented explicitly.

---

# Required Context Validation

Context validation confirms that the bounded context of the producer claim is preserved or explicitly absent.

Validation must check:

```text
context table exists
context records reference valid assertion_id values
context_type exists
context_value or explicit unresolved state is present
context_reference is preserved when available
context_namespace is preserved when applicable
producer_family is preserved
source_artifact_reference is preserved when applicable
context resolution status is present
context validation status is present
```

Context must remain distinct from biological interpretation.

Context explains claim boundaries.

Context does not determine claim truth.

---

# Required Lineage Validation

Lineage validation confirms reconstructability from Assertion Records back to Corpus Generation, Registration Units, source packages, source artifacts, assertion registrations, and source identities.

Validation must check:

```text
lineage table exists
lineage records reference valid assertion_id values
assertion_record_index_id is preserved
corpus_generation_id is preserved
corpus_generation_manifest_reference is visible
downstream_assertion_record_input_manifest_reference is preserved
registration_unit_id is preserved
registration_unit_reference is visible
source_package_id is visible or explicitly unresolved
source_package_reference is visible or explicitly unresolved
source_artifact_id is visible or explicitly unresolved
source_artifact_reference is visible or explicitly unresolved
source_assertion_registration_id is visible or explicitly unresolved
source_identity_references are visible or explicitly unresolved when applicable
producer_family is preserved
producer_reference is visible or explicitly unresolved
indexing_process is preserved
schema_version or contract_version is visible when available
validation_report_reference is visible when available
reconstruction_status is present
```

An Assertion Record without reconstructable lineage is not VDB-compliant.

---

# Required Payload Reference Validation

Payload reference validation confirms that producer-specific or large payloads are reconstructable by reference or expose reconstruction limitations.

Validation must check:

```text
payload reference table exists
payload reference records reference valid assertion_id values
payload_reference_type exists
payload_reference is present or explicitly unresolved
source_artifact_reference is visible or explicitly unresolved
source row, record, table, or file references are preserved when available
producer_payload_path is preserved when applicable
checksum_reference is preserved when available
payload_resolution_status is present
payload_lossiness_status is present
payload validation status is present
```

Required semantic fields must not exist only inside an opaque payload.

Payload lossiness must be explicit.

---

# Required Reconciliation Validation

Reconciliation validation confirms that indexing behavior is complete, deterministic, and explainable.

Validation must check:

```text
source assertion registrations are counted
indexed assertion registrations are counted
indexed-with-note assertion registrations are counted
unsupported assertion registrations are counted
deferred assertion registrations are counted
failed assertion registrations are counted
not-applicable assertion registrations are counted
not-evaluated assertion registrations are counted
assertion counts reconcile to selected Registration Units when applicable
producer resolver coverage is reported
unsupported assertion types are reported
duplicate source assertion keys are handled deterministically
unresolved source assertion keys are reported
skipped assertion registrations are explicitly justified
```

Phase 4.3 validation must not require every source assertion registration to become an indexed Assertion Record.

It must require every source assertion registration to be accounted for.

Silent disappearance is prohibited.

---

# Required Determinism Validation

Determinism validation confirms stable outputs under fixed inputs.

Given the same:

```text
Corpus Generation manifest
downstream Assertion Record input manifest
selected Registration Units
producer assertion resolver policies
indexing policy
validation policy
contract version
schema version
builder version
Registration Unit contents
```

the builder should produce equivalent:

```text
Assertion Record identities
source assertion keys
participant records
relationship records
evidence basis records
context records
lineage records
payload reference records
indexing statuses
validation statuses
failure reports
summary counts
downstream topology input manifest
```

Validation must check:

```text
stable assertion_id generation
stable source_assertion_key generation
stable resolver behavior
stable unresolved-state vocabulary
stable indexing status vocabulary
stable validation status vocabulary
stable report ordering
stable count semantics
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define Assertion Record order.

Filesystem traversal order must not define assertion indexing order.

Extraction queries should sort by stable keys.

---

# Required Non-Mutation Validation

Assertion Record indexing must be read-only with respect to selected Registration Units.

Validation must check:

```text
selected Registration Unit files are not modified
selected Registration Unit SQLite databases are opened read-only
no SQLite sidecars are created
no journal or WAL sidecars are created in Registration Unit directories
Registration Unit manifests are not rewritten
Registration Unit metadata is not rewritten
Registration Unit assertion registrations are not rewritten
source artifacts are not rewritten
```

Assertion Record build artifacts must be emitted outside selected Registration Units.

Validation receipts must be emitted under `results/validation/`.

---

# Required Downstream Topology Handoff Validation

The downstream topology input manifest makes Evidence Topology derivation deterministic.

Canonical artifact:

```text
downstream_topology_input_manifest.tsv
```

Validation must check:

```text
downstream topology input manifest exists
assertion_record_index_id is preserved
corpus_generation_id is preserved
assertion_id is preserved
assertion_type is preserved
producer_family is preserved
relationship_or_relationship_class is preserved
participant_reference_summary is visible or explicitly unresolved
source_identity_reference_summary is visible or explicitly unresolved when applicable
registration_unit_id is preserved
uncertainty_context is visible or explicitly unresolved
independence_context is visible or explicitly unresolved when applicable
temporal_or_generation_context is visible or explicitly unresolved
validation_status is present
```

The downstream topology input manifest is not Evidence Topology.

It must not contain topology relationships unless produced by the Evidence Topology implementation.

---

# Required Anti-Collapse Validation

Anti-collapse validation confirms that Assertion Record indexing did not exceed its authority.

Validation must check that the implementation does not perform:

```text
producer identity collapse
assertion type collapse
relationship collapse
participant collapse
participant role collapse
evidence basis collapse
context collapse
provenance collapse
authority collapse
uncertainty collapse
confidence context collapse
independence context collapse
temporal context collapse
Registration Unit lineage collapse
Corpus Generation lineage collapse
source artifact lineage collapse
source identity collapse
payload reference collapse
assertion registration collapse
Assertion Record replacement by source identity
Assertion Record replacement by artifact row
Assertion Record replacement by Evidence Object
Assertion Record replacement by Evidence State
Assertion Record replacement by topology relationship
Assertion Record replacement by geometry feature
Assertion Record replacement by surface membership
Assertion Record replacement by projection row
opaque score replacing assertion basis
cross-producer confidence score creation at Assertion Record layer
biological truth assertion by VDB
clinical actionability assertion by VDB
causality assertion by VDB
RDGP reasoning embedded in Assertion Record unless returned as a producer assertion
```

Any violation must fail validation unless explicitly isolated to a negative/failure-mode test fixture.

---

# Status Vocabularies

## Indexing Status Vocabulary

Allowed values:

```text
indexed
indexed_with_note
deferred
unsupported_assertion_type
missing_required_component
failed_validation
not_applicable
not_evaluated
```

## Validation Status Vocabulary

Allowed values:

```text
passed
passed_with_note
failed
not_available
not_reported
not_evaluated
unresolved
inspection_failed
```

## Resolution Status Vocabulary

Allowed values:

```text
resolved
resolved_with_note
not_available
not_applicable
not_reported
unresolved
ambiguous
conflicted
inspection_failed
unsupported
deferred
```

## Reconstruction Status Vocabulary

Allowed values:

```text
reconstructable
reconstructable_with_note
partially_reconstructable
not_reconstructable
not_available
not_applicable
unresolved
inspection_failed
```

## Payload Lossiness Status Vocabulary

Allowed values:

```text
lossless
lossless_by_reference
lossy_with_note
lossy
not_applicable
not_reported
unresolved
```

Unresolved values must not be collapsed into blank strings.

Missing values must not silently masquerade as zero, negative evidence, absence, or not relevant.

---

# Certification Boundary

Assertion Record validation may support Phase 4.3 certification review.

It does not itself certify:

```text
biological correctness
clinical correctness
causal interpretation
RDGP prioritization correctness
Evidence Topology correctness
Convergence Geometry correctness
Evidence Convergence Surface correctness
Projection View correctness
full Phase 4.8 completion
```

A passing Assertion Record validation result means:

```text
VDB preserved producer scientific claims from the declared Corpus Generation
as deterministic, reconstructable, corpus-indexed Assertion Records under the
declared validation policy.
```

A passing Assertion Record validation result does not mean:

```text
the claims are true
the claims are clinically actionable
the claims explain phenotype
the claims establish causality
the downstream topology is valid
the downstream geometry is valid
the downstream projections are valid
RDGP should prioritize a gene
```

---

# Completion Criteria

Assertion Record validation is complete when the implementation can prove:

```text
Corpus Generation input is explicit
downstream Assertion Record input manifest is explicit
selected Registration Units are explicit
selected Registration Units are read-only
producer assertion resolver policy is declared
Assertion Record Index identity is stable
Assertion Record identity is stable
source assertion key strategy is declared and validated
producer identity is preserved
assertion type is preserved
relationship or relationship class is preserved
participants are preserved when applicable
participant roles are explicit when participants are present
evidence basis is preserved or explicitly absent
context is preserved or explicitly absent
provenance is reconstructable
authority context is visible
uncertainty context is visible
confidence or support context is preserved when available
independence context is preserved when available
temporal or generation context is preserved when available
Registration Unit lineage is preserved
Corpus Generation lineage is preserved
source artifact lineage is preserved
source identity lineage is preserved when applicable
payload references resolve or expose reconstruction limitations
unsupported assertion registrations are reported
deferred assertion registrations are reported
failed assertion registrations are reported
validation report is emitted
validation summary is emitted
machine-readable Assertion Record artifacts are emitted
human-readable Assertion Record report is emitted
downstream topology input manifest is emitted
outputs are deterministic under fixed inputs
Assertion Records can serve as input to Evidence Topology
Assertion Records do not derive topology
Assertion Records do not perform biological reasoning
anti-collapse safeguards pass
Layer 1 local validation passes
Layer 2 compressed real-row golden fixture validation passes
Layer 3 MARK full-corpus validation passes
```

The implementation is not complete merely because rows, records, files, or indexes exist.

It is complete only when those records satisfy the Assertion Record contract, schema, and validation requirements.

---

# Summary

Assertion Record validation governs VDB Phase 4.3 preserved scientific claim validation.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.
```

The guiding validation rule is:

```text
Consume declared corpus scope.

Read selected Registration Units safely.

Preserve producer claims.

Preserve participants.

Preserve relationships.

Preserve evidence basis.

Preserve context.

Preserve uncertainty.

Preserve lineage.

Account for every source assertion registration.

Emit deterministic artifacts.

Emit deterministic validation receipts.

Do not mutate.

Do not derive.

Do not interpret.
```

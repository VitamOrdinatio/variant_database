# Assertion Record Resolver Policy Model

**Status:** ACTIVE PHASE 4.3 DESIGN MODEL

**Phase:** IV.3 — Assertion Records

**Primary Contract:** `docs/contracts/assertion_records/assertion_record_contract.md`

**Primary Schema:** `docs/implementation/schemas/assertion_record_schema.md`

**Primary Validation Governance:** `docs/validation/assertion_record_validation.md`

**Implementation Plan:** `docs/implementation/plans/assertion_record_plan.md`

**Companion Design Model:** `docs/design/assertion_record_identity_preservation_model.md`

---

## Purpose

This document defines the VDB Phase 4.3 resolver policy model for Assertion Record preservation.

A producer assertion resolver maps producer-specific assertion registrations into the common Assertion Record schema while preserving producer identity, claim semantics, relationship structure, participants, evidence basis, context, authority, uncertainty, confidence/support context when available, independence context when available, temporal context when available, lineage, and payload reconstruction references.

Resolver policy exists because VDB must support heterogeneous producer families without pretending that all producer claims have the same biological shape.

A resolver is producer-neutralizing.

It is not producer-erasing.

A resolver preserves producer claims.

It does not create biological meaning.

It does not aggregate across producers.

It does not rank evidence.

It does not derive topology.

It does not characterize geometry.

It does not construct surfaces.

It does not emit projections.

It does not perform RDGP reasoning.

---

# Resolver Policy Role

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

The resolver policy governs how Assertion Record indexing moves from selected Registration Unit assertion registrations into preserved corpus-indexed Assertion Records.

The resolver policy answers:

```text
Given a selected Registration Unit and its assertion-bearing material,
how does VDB preserve producer-specific claims as common Assertion Record
artifacts without changing producer authority or biological meaning?
```

The resolver policy does not answer:

```text
Which claims are biologically correct?
Which claims should be believed?
Which claims converge?
Which topology should be derived?
Which geometry should be characterized?
Which evidence surfaces should be exposed?
Which projections should consumers receive?
Which gene should RDGP prioritize?
```

Those questions belong downstream.

---

# Core Invariant

The core invariant is:

```text
A resolver maps producer-specific assertion registrations into the common
Assertion Record schema.

A resolver must preserve claim identity, producer identity, participant roles,
relationship semantics, evidence basis, context, authority, uncertainty,
and lineage.

A resolver must not infer biological truth.
```

Resolvers operate at the preservation layer.

They do not perform downstream reasoning.

---

# Resolver Responsibilities

A producer assertion resolver is responsible for declaring and implementing:

```text
producer_family
supported assertion registration types
unsupported assertion registration behavior
deferred assertion behavior
source assertion key strategy
assertion_id input tuple participation
assertion_type mapping
relationship mapping
participant role mapping
evidence basis mapping
context mapping
authority context mapping
uncertainty context mapping
confidence or support mapping when available
independence context mapping when available
temporal or generation mapping when available
lineage mapping
payload reference policy
validation behavior
failure behavior
```

A resolver must emit or support all fields required by:

```text
docs/implementation/schemas/assertion_record_schema.md
```

A resolver must satisfy preservation obligations defined by:

```text
docs/contracts/assertion_records/assertion_record_contract.md
```

A resolver must support validation obligations defined by:

```text
docs/validation/assertion_record_validation.md
```

---

# Resolver Non-Responsibilities

Resolvers must not perform:

```text
biological truth assignment
clinical interpretation
causal interpretation
cross-producer confidence aggregation
cross-assertion topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
Projection View generation
RDGP reasoning
source data repair without explicit status
silent source data normalization
silent namespace replacement
silent assertion registration exclusion
```

Resolvers may normalize records into VDB schema fields.

They must not normalize away producer-native identities, uncertainty, authority labels, or reconstruction paths.

---

# Resolver Policy Identity

Every resolver policy set should have a stable identity.

Recommended fields:

```text
producer_resolver_policy_id
producer_resolver_policy_version
supported_producer_families
supported_assertion_registration_types
unsupported_behavior
fallback_key_behavior
resolver_author
resolver_timestamp
schema_reference
contract_reference
validation_reference
```

Initial recommended policy identity:

```text
producer_resolver_policy_id: mark_phase4_vap_gsc_assertion_resolver_policy
producer_resolver_policy_version: v1
supported_producer_families: VAP, GSC
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
assertion_record_index_id: mark_phase4_corpus_6tep_v1_assertion_record_index
```

Policy identity must be visible in Assertion Record Index metadata and validation receipts.

---

# Generic Resolver Contract

Each producer resolver must declare the following logical contract.

## Input Contract

The resolver consumes assertion-bearing material from selected Registration Units declared by a Corpus Generation.

Required input context:

```text
corpus_generation_id
assertion_record_index_id
registration_unit_id
producer_family
source_package_id
source artifact references
assertion registration references when available
source identity references when applicable
Registration Unit metadata
Corpus Generation selection metadata
resolver policy identity
indexing policy identity
```

The resolver must not inspect Registration Units outside the declared Corpus Generation.

The resolver must not select inputs through filesystem traversal.

## Output Contract

The resolver must emit or support:

```text
Assertion Record core records
relationship records
participant records
evidence basis records
context records
lineage records
payload reference records
indexing status records
validation status records
downstream topology input manifest rows
```

Output records must preserve Registration Unit lineage and Corpus Generation lineage.

## Accounting Contract

Every source assertion registration encountered under the declared policy must be accounted for as one of:

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

Not every source assertion registration must become an indexed Assertion Record in v1.

Every source assertion registration must be accounted for.

Silent disappearance is prohibited.

---

# Producer Resolver Policy Shape

Each producer-specific resolver section should define:

```text
producer_family
initial_v1_scope
supported_assertion_registration_types
provisional_assertion_registration_types_pending_reconnaissance
unsupported_assertion_registration_behavior
deferred_assertion_registration_behavior
assertion_type_mapping
relationship_mapping
participant_role_mapping
evidence_basis_mapping
context_mapping
authority_context_mapping
uncertainty_context_mapping
confidence_support_mapping
independence_mapping
temporal_generation_mapping
lineage_mapping
payload_reference_mapping
source_assertion_key_strategy
fallback_source_assertion_key_strategy
validation_behavior
failure_behavior
Layer 2 fixture obligations
MARK Layer 3 obligations
```

Producer-specific sections in this design document are initial policy models.

They must be revisited after Registration Unit reconnaissance confirms the actual assertion registration shapes present in the six canonical Registration Units.

---

# VAP Resolver Policy Model

## Initial Status

The VAP resolver policy is provisional until Registration Unit reconnaissance confirms the actual VAP assertion registration shapes available in the canonical four VAP Registration Units.

Initial VAP target Registration Units:

```text
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Initial VAP producer family:

```text
VAP
```

## Initial VAP Assertion Scope

Initial VAP resolver scope may include:

```text
variant_observation
variant_annotation
variant_gene_association
interpretation_label_assignment
validation_result
quality_status
routing_or_priority_tier_assignment
```

The resolver must not assume all possible VAP output rows are assertion-bearing.

The resolver must distinguish assertion-bearing rows from supporting metadata, source identities, artifact metadata, and validation receipts.

## VAP Relationship Mapping

Initial VAP relationship classes may include:

```text
variant observed in sample
variant associated with gene
variant assigned annotation
variant assigned interpretation label
variant assigned consequence
variant assigned clinical significance
variant assigned priority tier
variant passed validation or quality criterion
```

These relationship classes preserve VAP-emitted claims.

They do not assert VDB biological belief.

## VAP Participant Role Mapping

Initial VAP participant roles may include:

```text
sample
variant
gene
transcript
annotation_source
clinical_label
consequence
priority_tier
pipeline_stage
validation_method
```

Participant identity must remain source-native.

Canonical gene or variant identity may be attached separately through namespace governance, but it must not replace source-native participant identity inside Assertion Records.

## VAP Evidence Basis Mapping

Initial VAP evidence basis references may include:

```text
source artifact
source row
variant call row
annotation row
quality field
clinical significance field
consequence field
pipeline stage artifact
validation artifact
priority tier artifact
```

Evidence basis may be represented directly or by reconstructable reference.

Large payloads should be preserved by reference where possible.

## VAP Context Mapping

Initial VAP context may include:

```text
sample context
run context
assay context
genome build context
pipeline stage context
annotation context
clinical annotation context
validation context
quality context
```

Context must remain bounded.

A VAP variant observation in one sample must not become a general claim about a gene, disease, or population unless VAP explicitly emitted such a claim.

## VAP Authority And Uncertainty Mapping

Initial VAP authority contexts may include:

```text
producer_observation
producer_annotation
producer_validation_result
producer_quality_status
corpus_indexed_preservation
```

Initial VAP uncertainty contexts may include:

```text
not_reported
uncertain
ambiguous
conflicting
not_applicable
unresolved
```

VAP quality flags, validation labels, and clinical annotation labels may be preserved as confidence/support or context.

They must not be converted into cross-producer VDB confidence.

## VAP Source Assertion Key Strategy

Preferred VAP source assertion key components:

```text
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id
assertion_type
```

Fallback VAP source assertion key components may include:

```text
registration_unit_id
source_package_id
source_artifact_id
source_record_reference
sample_id
variant identifier
gene identifier when applicable
relationship_or_relationship_class
assertion_type
producer_family
```

Fallback key use must be explicitly marked:

```text
source_assertion_key_strategy: fallback_source_record_fingerprint
source_assertion_key_resolution_status: resolved_with_note
```

## VAP Deferred Or Unsupported Behavior

The VAP resolver may defer assertion registration types when:

```text
the assertion registration type is not yet mapped
required source fields are unavailable
participant structure is ambiguous
relationship class is ambiguous
evidence basis cannot be reconstructed
source assertion key cannot be generated deterministically
```

Deferred VAP registrations must be counted and reported.

Unsupported VAP registrations must be counted and reported.

---

# GSC Resolver Policy Model

## Initial Status

The GSC resolver policy is provisional until Registration Unit reconnaissance confirms the actual GSC assertion registration shapes available in the canonical two GSC Registration Units.

Initial GSC target Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
```

Initial GSC producer family:

```text
GSC
```

## Initial GSC Assertion Scope

Initial GSC resolver scope may include:

```text
semantic_prior
phenotype_gene_relationship
source_contribution
consensus_membership
producer_validation_result
contract_validation_result
```

The resolver must distinguish GSC scientific assertion rows from metadata, source identity records, package metadata, artifact metadata, and validation receipts.

## GSC Relationship Mapping

Initial GSC relationship classes may include:

```text
phenotype has semantic prior for gene
gene belongs to phenotype-scoped consensus set
source contributes evidence for gene
source supports phenotype-gene relationship
producer output validates against declared contract
```

These relationship classes preserve GSC-emitted claims.

They do not assert VDB biological belief.

## GSC Participant Role Mapping

Initial GSC participant roles may include:

```text
phenotype
gene
source
semantic channel
evidence source
method
release
```

Source-native GSC identifiers must remain visible.

Canonical gene identifiers may be attached through namespace governance, but they must not erase source-native participant values or source label provenance.

## GSC Evidence Basis Mapping

Initial GSC evidence basis references may include:

```text
consensus gene set row
source contribution row
semantic score
source count
source list
source channel
source adapter
release metadata
run metadata
validation artifact
```

GSC semantic scores may be preserved as confidence/support context.

They must not be converted into a universal VDB confidence score.

## GSC Context Mapping

Initial GSC context may include:

```text
phenotype context
release context
run context
semantic scoring context
source adapter context
evidence channel context
contract validation context
```

A GSC phenotype-scoped semantic prior must remain phenotype-scoped.

It must not become a general gene truth claim.

## GSC Authority And Uncertainty Mapping

Initial GSC authority contexts may include:

```text
producer_semantic_prior
producer_source_contribution
producer_validation_result
corpus_indexed_preservation
```

Initial GSC uncertainty contexts may include:

```text
positive
not_reported
uncertain
ambiguous
conflicting
not_applicable
unresolved
```

GSC score, source count, source list, and semantic evidence channel may be preserved as confidence/support context.

They must not become VDB biological truth authority.

## GSC Source Assertion Key Strategy

Preferred GSC source assertion key components:

```text
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id
assertion_type
```

Fallback GSC source assertion key components may include:

```text
registration_unit_id
source_package_id
source_artifact_id
source_record_reference
phenotype
gene identifier
relationship_or_relationship_class
assertion_type
producer_family
```

Fallback key use must be explicitly marked:

```text
source_assertion_key_strategy: fallback_source_record_fingerprint
source_assertion_key_resolution_status: resolved_with_note
```

## GSC Deferred Or Unsupported Behavior

The GSC resolver may defer assertion registration types when:

```text
the assertion registration type is not yet mapped
required source fields are unavailable
phenotype or gene participant structure is ambiguous
relationship class is ambiguous
evidence basis cannot be reconstructed
source assertion key cannot be generated deterministically
```

Deferred GSC registrations must be counted and reported.

Unsupported GSC registrations must be counted and reported.

---

# Unsupported And Deferred Assertion Behavior

Unsupported or deferred assertion registrations are not automatically validation failures.

They become validation failures only when the declared indexing policy requires them to be indexed.

Allowed indexing statuses are:

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

Policy rule:

```text
Every source assertion registration must be accounted for.

Not every source assertion registration must become an indexed Assertion Record in v1.
```

Unsupported behavior must preserve:

```text
registration_unit_id
producer_family
source_package_id
source_artifact_id when available
source_assertion_registration_id when available
assertion registration type when available
unsupported reason
resolver policy identity
validation status
```

Deferred behavior must preserve:

```text
deferred reason
future eligibility when known
required missing components when applicable
resolver limitation when applicable
```

Silent exclusion is prohibited.

---

# Source Assertion Key And Fallback Policy

Resolver policies must use deterministic source assertion key generation.

Preferred source assertion key inputs:

```text
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id
assertion_type
producer_family
```

Fallback source assertion key inputs may include:

```text
registration_unit_id
source_package_id
source_artifact_id
source_record_reference
relationship_or_relationship_class
participant_reference_fingerprint
evidence_basis_reference
assertion_type
producer_family
```

Fallback key policy must declare:

```text
source_assertion_key_strategy
source_assertion_key_resolution_status
fallback_components_used
fallback_limitations
```

Fallback keys must be deterministic.

Fallback keys must not depend on:

```text
SQLite row-return order
filesystem traversal order
wall-clock time
non-deterministic dictionary ordering
runtime-specific object identity
temporary file path
```

If stable source assertion key generation fails, the source assertion registration must be reported as:

```text
missing_required_component
```

or another explicitly declared failure status under the validation policy.

---

# Participant Mapping Policy

Participants must remain role-bearing.

Resolver policies must map producer-specific fields to participant roles without replacing source-native identities.

Required participant mapping decisions:

```text
which source fields define participant_value
which source fields define participant_namespace
which source fields define participant_label
which source records define source_record_reference
which source identities attach as source_identity_reference
which participant roles are required by assertion type
which participant roles are optional
which unresolved participant states are allowed
```

Participant mapping must not:

```text
replace source-native identity with canonical identity
silently drop participant roles
silently merge participants
infer missing participants from downstream biological expectation
```

---

# Relationship Mapping Policy

Resolver policies must map producer-specific claim semantics to explicit relationship or relationship classes.

Required relationship mapping decisions:

```text
relationship_type
relationship_label
relationship_class
relationship_directionality when applicable
relationship_arity when applicable
relationship_context when applicable
assertion_type compatibility
producer_family compatibility
```

Relationship mapping must not:

```text
force all claims into binary subject-predicate-object form
derive cross-assertion topology
infer biological causality
promote producer claims to VDB belief
```

---

# Evidence Basis Mapping Policy

Resolver policies must preserve the evidence basis carrying or supporting the producer claim.

Required evidence basis mapping decisions:

```text
evidence_basis_type
evidence_basis_reference
source_artifact_reference
source_row_reference when available
source_record_reference when available
source_table_reference when available
source_file_reference when available
source method, score, count, threshold, or validation result when available
producer payload reference when applicable
external snapshot reference when applicable
resolution status
validation status
```

Evidence basis mapping must not replace reconstructable evidence with opaque summary fields.

If evidence basis is unavailable, the unavailable state must be explicit.

---

# Context Mapping Policy

Resolver policies must preserve the bounded context in which the producer emitted the claim.

Required context mapping decisions:

```text
context_type
context_value
context_reference
context_namespace
producer_family
source_artifact_reference
resolution status
validation status
```

Context may include:

```text
sample context
phenotype context
cohort context
condition context
contrast context
genome build context
annotation context
release context
run context
method context
pipeline stage context
evidence generation context
reasoning generation context when applicable
```

Context mapping must not generalize a bounded claim beyond its source context.

---

# Authority And Uncertainty Mapping Policy

Resolver policies must preserve authority context and uncertainty context.

Authority context answers:

```text
What kind of authority does the preserved assertion have?
```

Uncertainty context answers:

```text
What epistemic or uncertainty state accompanied the producer claim?
```

Allowed authority contexts may include:

```text
producer_assertion
producer_observation
producer_annotation
producer_semantic_prior
producer_validation_result
registration_preservation
corpus_indexed_preservation
not_reported
not_applicable
unresolved
```

Allowed uncertainty contexts may include:

```text
positive
negative
null
uncertain
conflicting
unsupported
provisional
deprecated
withdrawn
not_applicable
not_reported
ambiguous
unresolved
```

Resolver policies must not collapse:

```text
absence of evidence into negative evidence
uncertainty into falsehood
conflict into consensus
deprecated evidence into deleted evidence
provisional evidence into certified evidence
```

---

# Confidence, Independence, And Temporal Mapping Policy

Resolvers may preserve producer-provided confidence or support context when available.

Confidence/support examples:

```text
producer score
semantic score
quality flag
support count
frequency count
validation status
confidence label
evidence channel
threshold status
method-derived confidence
```

Confidence/support values must remain producer-contextual.

Resolvers must not convert heterogeneous producer values into a cross-producer VDB confidence score.

Independence context may include:

```text
producer run
producer release
source artifact
source table
source database
source publication
source cohort
source method
source evidence channel
source adapter
derivation group
replicate group
```

Temporal or generation context may include:

```text
producer run timestamp
producer release version
TEP generation timestamp
Registration Unit creation timestamp
Corpus Generation build timestamp
Assertion Record indexing timestamp
evidence generation identifier
reasoning generation identifier when applicable
```

Resolvers must preserve available independence and temporal context.

Resolvers must not infer independence beyond declared or reconstructable evidence.

---

# Lineage And Payload Reference Policy

Resolvers must preserve reconstruction lineage from Assertion Record back to source.

Lineage mapping must preserve:

```text
assertion_id
assertion_record_index_id
corpus_generation_id
corpus_generation_manifest_reference
downstream_assertion_record_input_manifest_reference
registration_unit_id
registration_unit_reference
source_package_id
source_package_reference
source_artifact_id
source_artifact_reference
source_assertion_registration_id when available
source_identity_references when applicable
producer_family
producer_reference
indexing_process
indexing_process_version
contract_version when available
schema_version when available
validation_report_reference when available
reconstruction_status
```

Payload references may include:

```text
source artifact reference
source row reference
source record reference
source table reference
source file reference
producer payload path
checksum reference
external snapshot reference
object-store reference
```

Required semantic fields must not exist only inside opaque payload.

Payload lossiness must be explicit.

---

# Validation Behavior

Resolver validation must support:

```text
input validation
record validation
participant validation
relationship validation
evidence basis validation
context validation
lineage validation
payload reference validation
reconciliation validation
determinism validation
non-mutation validation
downstream handoff validation
anti-collapse validation
```

Resolver validation must report:

```text
source assertion registration count
indexed count
indexed_with_note count
unsupported count
deferred count
failed count
not_applicable count
not_evaluated count
producer resolver coverage
duplicate source assertion key count
unresolved source assertion key count
validation limitations
```

Validation must confirm preservation and reconstructability.

Validation must not claim biological correctness.

---

# Relationship To Layer 2 Golden Fixture

The Phase 4.3 Layer 2 fixture must exercise resolver behavior against compressed real-world-derived data.

Recommended fixture identity:

```text
phase4_3_assertion_record_golden_fixture_v1
```

The fixture should include enough VAP and GSC evidence to validate:

```text
VAP resolver maps compressed real VAP assertion-bearing rows correctly
GSC resolver maps compressed real GSC assertion-bearing rows correctly
source_assertion_key behavior is stable
fallback key behavior is visible when used
unsupported registrations are counted
deferred registrations are counted
participants are role-bearing
relationships are explicit
evidence basis is reconstructable or explicitly absent
context is reconstructable or explicitly absent
lineage points back to Registration Units and Corpus Generation
payload references resolve or expose reconstruction limitations
anti-collapse checks pass
```

Layer 2 must not require all possible VAP or GSC assertion types to be supported.

Layer 2 must require every encountered source assertion registration to be accounted for.

---

# Relationship To Registration Unit Reconnaissance

Producer-specific resolver policy must be grounded in observed Registration Unit structures.

Before coding resolvers, VDB should inspect the six canonical Registration Units and document:

```text
which tables contain assertion registrations
which columns exist in assertion registration tables
which source artifact references are present
which source identity references are present
which producer assertion IDs are available
which assertion registration types are present
which assertion registration types are assertion-bearing
which assertion registration types are metadata-only
which fields can support participant mapping
which fields can support relationship mapping
which fields can support evidence basis mapping
which fields can support context mapping
which fields can support lineage mapping
which fields require fallback key generation
which records should be deferred or unsupported in v1
```

This reconnaissance should inform:

```text
VAP resolver v1 scope
GSC resolver v1 scope
Layer 2 fixture construction
Layer 3 MARK validation expectations
unsupported/deferred assertion policy
```

If reconnaissance contradicts this design model, the resolver policy model should be patched before implementation.

---

# Anti-Collapse Rules

Resolver implementations must not perform:

```text
producer identity collapse
producer family collapse
assertion type collapse
relationship collapse
participant collapse
participant role collapse
source-native identity collapse
evidence basis collapse
context collapse
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
source_assertion_key replaced by assertion_id
assertion_id replaced by source identity
assertion_id replaced by artifact identity
Assertion Record replaced by topology relationship
Assertion Record replaced by geometry feature
Assertion Record replaced by surface membership
Assertion Record replaced by projection row
opaque score replacing assertion basis
cross-producer confidence score created at resolver layer
biological truth asserted by resolver
clinical actionability asserted by resolver
causality asserted by resolver
RDGP reasoning embedded by resolver
```

Any implementation that performs one of these actions violates resolver policy.

---

# Completion Criteria

The resolver policy model is satisfied when Phase 4.3 implementation can demonstrate that:

```text
producer resolver policy identity is declared
VAP resolver scope is declared
GSC resolver scope is declared
unsupported behavior is declared
deferred behavior is declared
source assertion key strategy is declared
fallback source assertion key policy is declared
assertion type mapping is declared
relationship mapping is declared
participant role mapping is declared
evidence basis mapping is declared
context mapping is declared
authority context mapping is declared
uncertainty context mapping is declared
confidence/support mapping is declared when available
independence mapping is declared when available
temporal/generation mapping is declared when available
lineage mapping is declared
payload reference policy is declared
validation behavior is declared
failure behavior is declared
source assertion registrations are accounted for
Layer 2 fixture proves resolver behavior on compressed real-row data
Layer 3 MARK validation proves resolver behavior on the canonical corpus
anti-collapse safeguards pass
```

This model is not satisfied merely because resolver code exists.

It is satisfied only when resolver behavior is declared, deterministic, validation-visible, producer-aware, and preservation-safe.

---

# Summary

The Assertion Record resolver policy model defines how producer-specific assertion registrations become common VDB Assertion Records.

The guiding rule is:

```text
Map producer claims.

Preserve producer semantics.

Preserve participants.

Preserve relationships.

Preserve evidence basis.

Preserve context.

Preserve authority.

Preserve uncertainty.

Preserve lineage.

Account for every source assertion registration.

Do not derive.

Do not interpret.
```

Resolvers make heterogeneous producer claims indexable.

They must not make heterogeneous producer claims artificially identical.

# Assertion Record Implementation Plan

## Purpose

This document defines the implementation plan for Assertion Record construction in VDB Phase 4.

An Assertion Record is the primary preserved scientific claim object in VDB.

This plan describes how VDB will consume a declared Corpus Generation, inspect selected Registration Units, resolve producer assertion registrations, construct a corpus-indexed Assertion Record layer, preserve producer identity and evidence lineage, validate reconstructability, and provide downstream input to Evidence Topology.

The Phase 4 Assertion Record implementation goal is:

```text
Deterministically construct a corpus-indexed, producer-neutral
Assertion Record index from selected Registration Units while preserving
producer claims, participants, relationships, evidence basis, context,
uncertainty, authority, and lineage.
```

Assertion Record indexing preserves producer claims.

Assertion Record indexing does not interpret producer claims.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/assertion_records/assertion_record_contract.md
```

The governing contract states that Assertion Records must remain:

```text
producer-aware
claim-preserving
context-bounded
provenance-bound
participant-explicit
relationship-explicit
evidence-basis-preserving
authority-aware
uncertainty-aware
lineage-preserving
corpus-indexable
reconstructable
```

This plan is subordinate to the Assertion Record contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Assertion Record implementation role is to transform selected Registration Unit assertion registrations into preserved, corpus-indexable scientific claim objects.

An Assertion Record implementation answers:

```text
What did a producer claim,
about which participants,
under what relationship or relationship class,
with what evidence basis,
in what context,
with what provenance,
authority,
and uncertainty,
inside this declared Corpus Generation?
```

It does not answer:

```text
What is connected across assertions?

What topology emerges from the corpus?

What convergence geometry exists?

Which convergence regions are surface-eligible?

What projections should consumers receive?

What biological meaning should downstream systems infer?

Whether the producer claim is biologically correct?
```

Those questions belong to downstream implementation plans or downstream reasoning systems.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Registration Unit repair
Registration Unit migration
Registration Unit recertification
Corpus Generation selection
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

Assertion Record indexing is preservation work.

It is not topology work.

It is not reasoning work.

---

# Initial Implementation Target

The initial implementation target is the Assertion Record index for the first MARK Phase 4 Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

The expected upstream input is the downstream Assertion Record input manifest emitted by the Corpus Generation implementation, such as:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
    downstream_assertion_record_input_manifest.tsv
```

The initial Assertion Record implementation should consume the selected Registration Units declared by this Corpus Generation and emit a deterministic Assertion Record index for downstream Evidence Topology derivation.

The initial implementation target may be referred to as:

```text
mark_phase4_corpus_6tep_v1_assertion_record_index
```

This Assertion Record index is not Evidence Topology.

It is the preserved claim substrate from which Evidence Topology may later derive organization.

---

# Inputs

The Assertion Record implementation consumes:

```text
Corpus Generation manifest
downstream Assertion Record input manifest
selected Registration Unit references
Registration Unit contract version
Corpus Generation contract version
Assertion Record contract version
system contract version
producer assertion resolver policies
Assertion Record indexing policy
Assertion Record validation policy
builder name
builder version
indexing timestamp
```

Input Registration Units must be selected through a declared Corpus Generation.

Assertion Record indexing must not silently select Registration Units.

Assertion Record indexing must not parse raw producer artifacts when Registration Unit assertion registrations are available and sufficient.

---

# Outputs

The Assertion Record implementation should emit deterministic artifacts outside the selected Registration Units.

Expected outputs may include:

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
assertion_record_validation_report.json
assertion_record_validation_report.tsv
assertion_record_index_report.md
downstream_topology_input_manifest.tsv
```

These outputs are Assertion Record artifacts.

They do not replace Registration Units.

They do not replace the Corpus Generation.

They do not create topology relationships.

They do not create geometry features.

They do not create surface memberships.

They do not create projections.

They do not perform biological reasoning.

---

# Recommended Output Location

Initial Phase 4 Assertion Record outputs may be written under:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

A recommended initial layout is:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
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
    assertion_record_validation_report.json
    assertion_record_validation_report.tsv
    assertion_record_index_report.md
    downstream_topology_input_manifest.tsv
```

The output location should be configurable.

Assertion Record output paths must not be confused with Registration Unit source paths or Corpus Generation manifest paths.

---

# Required Assertion Record Index Identity

Every Assertion Record index must have a stable identity.

An Assertion Record index identity must preserve:

```text
assertion_record_index_id
assertion_record_index_label when available
input_corpus_generation_id
input_registration_unit_ids
assertion_record_indexing_policy_id
assertion_record_indexing_policy_version when available
producer_resolver_policy_ids when applicable
builder_name
builder_version when available
indexing_timestamp
validation_status
certification_status when available
```

For the initial MARK Assertion Record index, a recommended identity shape is:

```text
assertion_record_index_id: mark_phase4_corpus_6tep_v1_assertion_record_index
assertion_record_index_label: MARK Phase 4 6-TEP Assertion Record Index
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
assertion_record_indexing_policy_id: mark_phase4_vap_gsc_assertion_record_indexing_policy
assertion_record_indexing_policy_version: v1
```

Assertion Record index identity must remain stable across:

- Evidence Topology derivation
- Convergence Geometry derivation
- Evidence Convergence Surface construction
- Projection View generation
- validation
- certification
- reconstruction

The Assertion Record index identity is distinct from individual Assertion Record identity.

The Assertion Record index identifies the corpus-indexed claim layer.

Individual Assertion Records identify preserved claims within that layer.

Human-readable labels may support inspection.

Labels must not replace stable Assertion Record index identity.

---

# Required Assertion Record Identity

Every Assertion Record must have a stable identity.

An Assertion Record identity must preserve:

```text
assertion_id
assertion_label when available
assertion_type
producer_family
producer_id or producer reference
registration_unit_id
corpus_generation_id
source_package_id
source_artifact_id or source artifact reference
source_assertion_registration_id when available
created_at or indexed_at timestamp
indexing_process or builder name
indexing_process_version when available
validation_status
```

Assertion identity must remain stable across:

```text
Evidence Topology derivation
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
validation
certification
reconstruction
```

Human-readable labels may support inspection.

Labels must not replace stable Assertion Record identity.

---

# Source Assertion Key Strategy

The implementation should distinguish source assertion identity from corpus-indexed Assertion Record identity.

Recommended distinction:

```text
source_assertion_key
    stable identity for the producer assertion registration source,
    independent of a specific Corpus Generation when possible

assertion_id
    stable corpus-indexed Assertion Record identity used within a specific
    Corpus Generation
```

The same underlying producer assertion may participate in more than one Corpus Generation.

When this occurs, the implementation must preserve which Corpus Generation selected the assertion.

A deterministic `assertion_id` should be derived from stable source components when available, such as:

```text
corpus_generation_id
registration_unit_id
source_assertion_registration_id
assertion_type
producer_family
```

When `source_assertion_registration_id` is unavailable, the builder may use a declared fallback key derived from reconstructable source components.

Fallback components may include:

```text
source_package_id
source_artifact_id
source row or source record reference
assertion type
relationship or relationship class
participant references
evidence basis reference
```

Fallback key behavior must be explicit.

Fallback keys must not hide reconstruction limitations.

If stable Assertion Record identity cannot be produced, the record must fail validation or be emitted with an explicit unresolved identity status according to the declared validation policy.

---

# Producer Assertion Resolver Requirements

The Assertion Record implementation may use producer assertion resolvers.

A producer assertion resolver translates Registration Unit assertion registrations into the common Assertion Record logical model.

Initial resolvers may include:

```text
VAP assertion resolver
GSC assertion resolver
```

Future resolvers may include:

```text
RSP assertion resolver
RDGP-returned assertion resolver
external evidence capsule resolver
future producer assertion resolver
```

Each producer assertion resolver must declare:

```text
producer_family
supported assertion registration types
unsupported assertion registration behavior
relationship or relationship class mapping
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
```

Producer assertion resolvers must not create biological meaning.

Producer assertion resolvers must not perform cross-producer aggregation.

Producer assertion resolvers must not convert producer-specific confidence into a universal VDB confidence score.

Producer assertion resolvers must preserve producer heterogeneity while emitting a common corpus-indexable claim layer.

---

# Required Assertion Components

Each Assertion Record must preserve or explicitly declare absence for:

```text
producer identity
assertion type
relationship or relationship class
participants
evidence basis
context
provenance
authority context
uncertainty context
confidence or support context when available
independence context when available
temporal or generation context
source artifact references
source identity references
registration unit references
corpus generation references
payload references when applicable
validation status
```

If a component is unavailable, not applicable, not reported, unresolved, ambiguous, conflicted, intentionally absent, or inspection-failed, that state must be explicit when relevant.

Required components must not be collapsed into an opaque score, summary, projection row, or topology relationship.

---

# Participant Extraction Requirements

Assertion Records must preserve participants as role-bearing components.

Participant records should preserve:

```text
assertion_id
participant_id or participant reference
participant_role
participant_namespace when available
participant_value or resolvable reference
source_identity_reference when available
source_artifact_reference when available
producer_family
participant_context when available
validation_status
```

Participant roles may include:

```text
sample
variant
gene
transcript
phenotype
condition
contrast
source
semantic channel
pathway
regulatory_region
enhancer
promoter
chromatin_domain
noncoding_interval
regulatory_feature
cohort
publication
method
environment
reasoning output
external authority
```

Participant identity must remain distinguishable from canonical identity.

Source participants must not be overwritten by namespace-resolved participants.

Canonical identifiers may be attached separately through namespace governance.

If a participant is unavailable, unresolved, ambiguous, conflicted, or not applicable, that state must be explicit.

---

# Relationship Extraction Requirements

Assertion Records must preserve the relationship asserted by the producer.

Relationship records should preserve:

```text
assertion_id
relationship_id or relationship reference when available
relationship_type
relationship_label when available
relationship_directionality when applicable
relationship_arity
relationship_context when available
relationship_class when applicable
producer_family
assertion_type
validation_status
```

Relationships may be unary, binary, or higher-order.

VDB must not force all assertions into a subject-predicate-object model when the producer claim requires a richer participant structure.

Relationship preservation does not imply biological correctness.

A relationship inside an Assertion Record represents what the producer claimed.

It does not represent VDB endorsement.

---

# Evidence Basis Extraction Requirements

Assertion Records must preserve evidence basis when available.

Evidence basis records should preserve:

```text
assertion_id
evidence_basis_id or reference
evidence_basis_type
source_artifact_reference
source_row_reference when available
source_record_reference when available
source_table_reference when available
source_file_reference when available
source_database_snapshot when available
source_method when available
source_score when available
source_count when available
source_threshold when available
source_validation_result when available
source_provenance_channel when available
source_contribution_channel when available
producer_payload_reference when applicable
external_snapshot_reference when applicable
validation_status
```

Evidence basis may be represented directly or by reconstructable reference.

Large payloads do not need to be duplicated inside the Assertion Record if reconstruction is guaranteed.

Evidence basis must not be replaced by opaque summaries that prevent reconstruction of the producer claim.

---

# Context Extraction Requirements

Assertion Records must preserve context sufficient to interpret the producer claim as emitted.

Context records may preserve:

```text
assertion_id
context_type
context_value or context_reference
context_namespace when applicable
producer_family
source_artifact_reference when applicable
validation_status
```

Context may include:

```text
phenotype context
sample context
cohort context
condition context
contrast context
genome build context
transcript context
annotation context
regulatory context
regulatory domain context
chromatin context
noncoding burden context
regulatory feature annotation context
disease model context
method context
release context
run context
producer version context
schema version context
temporal context
evidence generation context
reasoning generation context when applicable
```

Context must remain distinct from biological interpretation.

Context explains the boundaries under which the producer emitted the claim.

Context does not determine whether the claim is biologically correct.

---

# Provenance And Lineage Requirements

Assertion Records must preserve provenance sufficient for reconstruction.

Lineage records should preserve:

```text
assertion_id
producer reference
producer_family
source_package_id
source_package_reference
source_artifact_id or reference
registration_unit_id
corpus_generation_id
source_assertion_registration_id when available
source_identity_references when applicable
indexing_process
indexing_process_version when available
schema or contract version when available
validation_report_reference when available
```

Provenance must allow reconstruction of:

```text
which producer emitted the claim
which producer family emitted the claim
which run or release generated the claim when available
which TEP transported the claim
which Registration Unit preserved the claim-bearing package
which Corpus Generation selected the Registration Unit
which artifact contained the claim-bearing material
which assertion registration carried the claim-bearing material when applicable
which source identities participated in the claim
which indexing process constructed or resolved the Assertion Record
which validation checks were applied
```

An Assertion Record without reconstructable provenance is not VDB-compliant.

---

# Authority, Uncertainty, Confidence, And Support Requirements

Assertion Records have preservation authority.

They do not have biological truth authority.

Assertion Records must preserve authority context and uncertainty context when available.

Authority context may include:

```text
producer authority class
source authority class
registration authority class
validation authority class
certification authority class when available
assertion preservation authority
```

Uncertainty or epistemic states may include:

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

The implementation must not collapse:

```text
absence of evidence into negative evidence
uncertainty into falsehood
conflict into consensus
deprecated evidence into deleted evidence
provisional evidence into certified evidence
```

Confidence or support context may be preserved when producer data provides it.

Confidence or support context may include:

```text
producer score
semantic score
support count
frequency count
validation status
quality flag
confidence label
evidence channel
threshold status
method-derived confidence
producer-specific confidence class
```

Confidence or support values must preserve producer context.

The Assertion Record layer must not convert heterogeneous producer confidence values into a single opaque cross-producer confidence score.

---

# Independence And Temporal Requirements

Assertion Records should preserve independence context when available.

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
source derivation group
replicate group
reasoning generation
evidence generation
```

Independence context helps downstream layers avoid false convergence.

The Assertion Record implementation must preserve available independence metadata.

It must not infer independence beyond declared or reconstructable evidence.

Assertion Records must also preserve temporal or generation context when available, including:

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

Temporal context must not be collapsed across generations.

---

# Payload And Reconstruction Requirements

Assertion Records may preserve large or producer-specific payloads by reference rather than duplication.

Payload references may include:

```text
assertion_id
source artifact reference
source row reference
source record reference
source table reference
source file reference
registration unit record reference
producer payload path
external snapshot reference
object-store reference
checksum reference when available
payload_resolution_status
payload_lossiness_status
```

Payload references must be resolvable or explicitly marked as unavailable.

If a payload reference cannot be resolved, the Assertion Record must expose that reconstruction limitation.

Payload lossiness must be explicit.

An Assertion Record must not be considered complete if the preserved core fields and payload references are insufficient to reconstruct the producer claim.

---

# Assertion Indexing Status

Each source assertion registration should receive an indexing status.

Indexing status may include:

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

Suggested semantics:

```text
indexed
    The source assertion registration was resolved into a compliant Assertion Record.

indexed_with_note
    The source assertion registration was resolved into an Assertion Record with
    documented caveats or limitations.

deferred
    The source assertion registration was not indexed in this implementation pass
    but remains eligible for future indexing.

unsupported_assertion_type
    The source assertion registration type is not supported by the current
    producer assertion resolver.

missing_required_component
    Required preservation components could not be resolved or explicitly
    represented.

failed_validation
    The attempted Assertion Record failed declared validation checks.

not_applicable
    The source registration was not assertion-bearing under the declared policy.

not_evaluated
    The source registration was not evaluated.
```

Unsupported or deferred assertion registrations must not silently disappear.

They should be counted and reported.

---

# Validation Strategy

Assertion Record validation should operate in four tiers.

## Tier 1: Input Validation

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
selected Registration Units expose assertion registrations
Registration Unit boundaries are preserved
```

## Tier 2: Record Validation

Record validation confirms that each Assertion Record satisfies preservation obligations.

Validation must check:

```text
assertion_id exists
assertion_type exists
producer identity exists
registration_unit_id is traceable
corpus_generation_id is traceable
source package reference is traceable
source artifact reference is traceable when applicable
source assertion registration reference is traceable when applicable
relationship or relationship class is present
participants are declared when applicable
participant roles are explicit when participants are present
evidence basis is declared or explicitly absent
context is declared or explicitly absent
provenance is reconstructable
authority context is visible
uncertainty context is visible
source identity references resolve when applicable
payload references resolve or expose reconstruction limitations
```

## Tier 3: Reconciliation Validation

Reconciliation validation confirms that indexing behavior is complete, deterministic, and explainable.

Validation must check:

```text
indexing is deterministic
assertion counts reconcile to selected Registration Units when applicable
source assertion registrations are counted
indexed assertion registrations are counted
unsupported assertion registrations are counted
deferred assertion registrations are counted
failed assertion registrations are counted
skipped assertion registrations are explicitly justified
duplicate source assertion keys are handled deterministically
unresolved source assertion keys are reported
producer resolver coverage is reported
```

## Tier 4: Anti-Collapse Validation

Anti-collapse validation confirms that Assertion Record indexing did not exceed its layer authority.

Validation must check:

```text
no assertion collapse occurs
no producer identity collapse occurs
no assertion type collapse occurs
no relationship collapse occurs
no participant collapse occurs
no evidence basis collapse occurs
no context collapse occurs
no provenance collapse occurs
no authority collapse occurs
no uncertainty collapse occurs
no Registration Unit lineage collapse occurs
no Corpus Generation lineage collapse occurs
no topology, geometry, surface, projection, or reasoning authority is embedded
Assertion Records do not derive topology
Assertion Records do not characterize geometry
Assertion Records do not create surface memberships
Assertion Records do not emit replacement projections
Assertion Records do not perform biological reasoning
```

Validation must confirm preservation and reconstructability.

Validation must not claim biological correctness.

---

# Determinism Requirements

Assertion Record indexing outputs must be deterministic under fixed inputs.

Given the same:

```text
Corpus Generation manifest
downstream Assertion Record input manifest
selected Registration Units
producer assertion resolver policies
indexing policy
validation policy
contract version
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

Determinism requirements include:

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

Extraction queries should sort by stable keys.

Filesystem traversal order must not define assertion indexing order.

---

# Reconstruction Requirements

Assertion Record artifacts must support reconstruction of:

```text
which Corpus Generation was used
which Registration Units were selected
which assertion registrations were inspected
which producer resolver policy was applied
which source assertion registration produced each Assertion Record
which producer emitted each claim
which package and artifact carried each claim
which participants were preserved
which relationship or relationship class was preserved
which evidence basis was preserved
which context bounded the claim
which authority context applied
which uncertainty context applied
which confidence or support context was preserved when available
which independence context was preserved when available
which temporal or generation context applied
which payload references were used
which reconstruction limitations were observed
which validation checks were applied
```

Assertion Record reconstruction must preserve enough information for downstream Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, RDGP-facing projections, and future reinterpretation.

---

# Relationship To Corpus Generation

Corpus Generations provide the evidence scope for Assertion Record indexing.

The responsibility boundary is:

```text
Corpus Generation
    declares selected Registration Units

Assertion Record indexing
    resolves producer claims from selected Registration Units into
    corpus-indexable Assertion Records
```

Assertion Records must preserve Corpus Generation lineage.

Each corpus-indexed Assertion Record must preserve:

```text
corpus_generation_id
corpus_generation_label when available
corpus_generation_version when available
selection policy reference when available
```

Assertion Record indexing must not expand Corpus Generation scope silently.

Assertion Record indexing must not include assertion registrations outside the declared Corpus Generation unless a new Corpus Generation or explicitly versioned input scope is declared.

---

# Relationship To Registration Units

Registration Units preserve assertion registrations.

Assertion Records are constructed, resolved, or indexed from assertion registrations within selected Registration Units.

Assertion Records must preserve traceability to their source Registration Units.

Each Assertion Record must preserve:

```text
registration_unit_id
source_package_id
source_artifact_id or source artifact reference
assertion registration reference when applicable
source identity references when applicable
```

Assertion Record indexing must not erase the Registration Unit boundary from which a claim was constructed.

Assertion Record indexing must not mutate Registration Units.

---

# Relationship To Evidence Topology

Assertion Records are the direct input to Evidence Topology.

The responsibility boundary is:

```text
Assertion Record
    preserves what a producer claimed among participants

Evidence Topology
    derives how preserved claims are connected across a corpus
```

Assertion Records may preserve internal producer relationships among their participants.

Assertion Records must not derive cross-assertion topology.

The Assertion Record implementation should emit or support a downstream topology input manifest containing:

```text
assertion_record_index_id
corpus_generation_id
assertion_id
assertion_type
producer_family
relationship or relationship class
participant references
source identity references when applicable
registration_unit_id
uncertainty context when applicable
independence context when available
temporal or generation context when available
validation_status
```

The downstream topology input manifest is not Evidence Topology.

It is a deterministic handoff artifact for topology derivation.

---

# Relationship To Downstream Derived Layers

Assertion Records provide the preserved claim substrate for:

```text
Evidence Topology
Convergence Geometry
Evidence Convergence Surfaces
Projection Views
RDGP-facing consumer projections
future downstream reasoning
```

Downstream derived layers must preserve Assertion Record lineage.

The following must not occur inside Assertion Record implementation:

```text
cross-assertion topology derivation
Convergence Geometry feature construction
Evidence Convergence Surface eligibility declaration
Evidence Convergence Surface disclosure decision
Projection View generation that replaces Assertion Records
RDGP reasoning
biological interpretation
cross-producer confidence aggregation
clinical actionability assignment
causality assignment
```

---

# Anti-Collapse Safeguards

Implementation must prevent:

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
Assertion Record replaced by source identity
Assertion Record replaced by artifact row
Assertion Record replaced by Evidence Object
Assertion Record replaced by Evidence State
Assertion Record replaced by topology relationship
Assertion Record replaced by geometry feature
Assertion Record replaced by surface membership
Assertion Record replaced by projection row
opaque score replacing assertion basis
cross-producer confidence score created at Assertion Record layer
biological truth asserted by VDB
clinical actionability asserted by VDB
causality asserted by VDB
RDGP reasoning embedded in Assertion Record unless returned as a producer assertion
```

Any implementation that performs one of these actions violates this plan and the Assertion Record contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Registration Units before running against the MARK corpus.

Recommended tests include:

```text
test_assertion_record_index_requires_corpus_generation
test_assertion_record_index_requires_downstream_input_manifest
test_assertion_record_index_preserves_corpus_generation_id
test_assertion_record_index_preserves_registration_unit_id
test_assertion_record_index_preserves_producer_family
test_assertion_record_index_preserves_source_package_id
test_assertion_record_index_preserves_source_artifact_reference
test_assertion_record_index_preserves_source_assertion_registration_id_when_available
test_assertion_record_index_requires_assertion_type
test_assertion_record_index_requires_relationship_or_relationship_class
test_assertion_record_index_preserves_role_bearing_participants
test_assertion_record_index_preserves_evidence_basis_or_explicit_absence
test_assertion_record_index_preserves_context_or_explicit_absence
test_assertion_record_index_preserves_uncertainty_context
test_assertion_record_index_preserves_authority_context
test_assertion_record_index_preserves_payload_reconstruction_limitations
test_assertion_record_index_reports_unsupported_assertion_types
test_assertion_record_index_reports_deferred_assertions
test_assertion_record_index_reports_failed_assertions
test_assertion_record_index_is_deterministic
test_assertion_record_index_does_not_mutate_registration_units
test_assertion_record_index_does_not_create_topology
test_assertion_record_index_does_not_perform_biological_reasoning
test_downstream_topology_input_manifest_is_emitted
```

MARK integration tests should confirm:

```text
mark_phase4_corpus_6tep_v1 is accepted as input
all selected Registration Units are inspected read-only
VAP assertion registrations are resolved or explicitly reported
GSC assertion registrations are resolved or explicitly reported
Assertion Record identities are stable
Assertion Record counts reconcile to Registration Unit inputs when applicable
unsupported assertion registrations are reported
producer resolver coverage is reported
downstream topology input manifest is deterministic
validation report is deterministic
```

Tests must not require biological correctness.

Tests validate preservation, reconstructability, determinism, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define Assertion Record indexing policy.

2. Define producer assertion resolver policy interface.

3. Define VAP assertion resolver behavior.

4. Define GSC assertion resolver behavior.

5. Load Corpus Generation manifest.

6. Load downstream Assertion Record input manifest.

7. Open selected Registration Units read-only.

8. Inventory assertion registrations by producer family and assertion type.

9. Generate source assertion keys.

10. Resolve Assertion Record identity.

11. Extract required Assertion Record components.

12. Extract role-bearing participants.

13. Extract relationship or relationship class.

14. Extract evidence basis references.

15. Extract context references.

16. Extract authority, uncertainty, confidence, support, independence,
    and temporal context when available.

17. Extract lineage and payload references.

18. Assign indexing status.

19. Validate Assertion Records.

20. Emit Assertion Record artifacts.

21. Emit Assertion Record validation report.

22. Emit downstream topology input manifest.

23. Add synthetic tests.

24. Add MARK corpus smoke test.

25. Hand off Assertion Record index to Evidence Topology implementation.
```

Each step must preserve Corpus Generation and Registration Unit lineage.

Each step must remain read-only with respect to selected Registration Units.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_assertion_record_index.py \
  --corpus-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/corpus_generation_manifest.tsv \
  --assertion-input-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv \
  --output-dir results/phase4/assertion_records/mark_phase4_corpus_6tep_v1 \
  --assertion-record-index-id mark_phase4_corpus_6tep_v1_assertion_record_index \
  --resolver-policy-id mark_phase4_vap_gsc_assertion_resolver_policy
```

or:

```bash
python scripts/phase4/validate_assertion_record_index.py \
  --assertion-record-index results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_index.tsv \
  --output-dir results/phase4/assertion_records/mark_phase4_corpus_6tep_v1
```

The exact script names are not contractually fixed.

The CLI must make Corpus Generation identity, input scope, resolver policy, and output location explicit.

---

# Expected Input Manifest Shape

A downstream Assertion Record input manifest may include:

```text
corpus_generation_id
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id
registration_backend
assertion_registration_count
source_identity_count
validation_status
certification_status
```

This manifest is produced by Corpus Generation implementation.

It is not an Assertion Record index.

It must be validated against selected Registration Units before indexing begins.

---

# Expected Assertion Record Index Shape

An Assertion Record index may include:

```text
assertion_record_index_id
assertion_id
source_assertion_key
assertion_label
assertion_type
producer_family
producer_id
registration_unit_id
corpus_generation_id
source_package_id
source_artifact_id
source_assertion_registration_id
relationship_or_relationship_class
authority_context
uncertainty_context
confidence_or_support_context
independence_context
temporal_or_generation_context
payload_reference_status
indexing_status
validation_status
builder_name
builder_version
indexed_at
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Expected Participant Table Shape

An Assertion Record participant table may include:

```text
assertion_id
participant_id
participant_role
participant_namespace
participant_value
source_identity_reference
source_artifact_reference
participant_context
producer_family
validation_status
```

Participants may be one-to-many relative to Assertion Records.

Participant records must remain role-bearing.

---

# Expected Evidence Basis Table Shape

An Assertion Record evidence basis table may include:

```text
assertion_id
evidence_basis_id
evidence_basis_type
source_artifact_reference
source_row_reference
source_record_reference
source_table_reference
source_file_reference
source_method
source_score
source_count
source_threshold
producer_payload_reference
external_snapshot_reference
validation_status
```

Evidence basis records may be one-to-many relative to Assertion Records.

Evidence basis must remain reconstructable.

---

# Expected Context Table Shape

An Assertion Record context table may include:

```text
assertion_id
context_type
context_value
context_reference
context_namespace
producer_family
source_artifact_reference
validation_status
```

Context records may be one-to-many relative to Assertion Records.

Context must not become biological interpretation.

---

# Expected Lineage Table Shape

An Assertion Record lineage table may include:

```text
assertion_id
corpus_generation_id
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id
source_identity_references
producer_family
producer_reference
indexing_process
indexing_process_version
contract_version
schema_version
validation_report_reference
```

Lineage records must support reconstruction from Assertion Record back to Registration Unit, source artifact, producer package, and Corpus Generation.

---

# Expected Downstream Topology Input Manifest Shape

A downstream topology input manifest may include:

```text
assertion_record_index_id
corpus_generation_id
assertion_id
assertion_type
producer_family
relationship_or_relationship_class
participant_reference_summary
source_identity_reference_summary
registration_unit_id
uncertainty_context
independence_context
temporal_or_generation_context
validation_status
```

This manifest exists to make Evidence Topology derivation deterministic.

It must not define topology relationships.

---

# Exit Criteria

The Assertion Record implementation plan is complete when:

```text
Corpus Generation input is explicit
selected Registration Units are explicit
producer assertion resolver policy is declared
Assertion Record identity is stable
source assertion key strategy is declared
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
validation report is emitted
machine-readable Assertion Record artifacts are emitted
human-readable Assertion Record index report is emitted
downstream topology input manifest is emitted
outputs are deterministic under fixed inputs
Assertion Records can serve as input to Evidence Topology
Assertion Records do not derive topology
Assertion Records do not perform biological reasoning
anti-collapse safeguards pass
```

This implementation is not complete merely because rows, records, files, or indexes exist.

It is complete only when those records satisfy the Assertion Record contract and can safely serve as the preserved claim substrate for downstream Phase 4 derivation.

---

# Summary

The Assertion Record implementation plan establishes the primary preserved scientific claim layer for VDB Phase 4.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.
```

The guiding rule is:

```text
Consume declared corpus scope.

Read Registration Units safely.

Preserve producer claims.

Preserve participants.

Preserve relationships.

Preserve evidence basis.

Preserve context.

Preserve uncertainty.

Preserve lineage.

Do not derive.

Do not interpret.
```

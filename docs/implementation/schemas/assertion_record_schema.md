# Assertion Record Schema

**Status:** ACTIVE PHASE 4.3 IMPLEMENTATION SCHEMA

**Phase:** IV.3 — Assertion Records

**Primary Contract:** `docs/contracts/assertion_records/assertion_record_contract.md`

**Primary Specification:** `docs/implementation/specifications/assertion_record_spec.md`

**Implementation Plan:** `docs/implementation/plans/assertion_record_plan.md`

**Conceptual Design Model:** `docs/design/assertion_record_and_projection_model.md`

**Upstream Input Family:** `results/phase4/corpus_generations/`

**Primary Build Output Family:** `results/phase4/assertion_records/`

**Primary Validation Receipt Family:** `results/validation/phase4_assertion_records/`

---

## Purpose

This document defines the Phase 4.3 schema for VDB Assertion Records.

An Assertion Record is the primary preserved scientific claim object in VDB.

The purpose of this schema is to define the emitted artifact family, logical record shapes, field names, cardinality, status vocabularies, validation receipt shape, and downstream topology handoff required for deterministic Assertion Record preservation.

Assertion Records preserve what producers claimed.

They do not represent VDB belief.

They do not determine biological correctness.

They do not derive topology.

They do not characterize convergence geometry.

They do not construct evidence convergence surfaces.

They do not emit projections.

They do not perform RDGP reasoning.

---

# Relationship To Contract, Specification, And Plan

This schema defines object and artifact shape.

Semantic obligations and preservation requirements are defined by:

```text
docs/contracts/assertion_records/assertion_record_contract.md
docs/implementation/specifications/assertion_record_spec.md
```

Implementation sequencing is defined by:

```text
docs/implementation/plans/assertion_record_plan.md
```

If this schema conflicts with the Assertion Record contract or the VDB system contract, the contracts take precedence.

This schema should be treated as the DEX implementation target for Phase 4.3.

---

# Phase 4.3 Schema Role

The Assertion Record schema governs the transition from declared Corpus Generation scope into preserved, corpus-indexed scientific claim records.

The governing chain is:

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

An Assertion Record answers:

```text
What did a producer claim,
about which participants,
under what relationship or relationship class,
with what evidence basis,
in what context,
with what provenance,
with what authority and uncertainty context,
inside which Corpus Generation?
```

An Assertion Record does not answer:

```text
What is connected across assertions?
What topology emerges from the corpus?
What convergence geometry exists?
Which convergence regions are surface-eligible?
What projections should consumers receive?
What biological meaning should downstream systems infer?
Whether the producer claim is biologically correct?
```

---

# Initial Canonical Target

The initial Phase 4.3 implementation target is:

```text
mark_phase4_corpus_6tep_v1_assertion_record_index
```

Input Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Required upstream handoff artifact:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Expected output family:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

Expected validation receipt family:

```text
results/validation/phase4_assertion_records/
```

Phase 4.3 must consume the governed downstream Assertion Record input manifest.

Phase 4.3 must not crawl Registration Unit folders opportunistically.

---

# Governed Output Artifact Family

Assertion Record build artifacts are emitted outside selected Registration Units.

Recommended canonical output layout:

```text
results/phase4/assertion_records/<corpus_generation_id>/
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

For the initial MARK Phase 4.3 target:

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
    assertion_record_index_report.md
    downstream_topology_input_manifest.tsv
```

Validation receipts must be emitted separately under:

```text
results/validation/phase4_assertion_records/
```

Build artifacts and validation receipts must not be collapsed.

---

# Core Logical Objects

The Phase 4.3 Assertion Record artifact family contains the following logical objects:

```text
assertion_record_index_identity
assertion_record_index_manifest_record
assertion_record
assertion_record_participant
assertion_record_relationship
assertion_record_evidence_basis
assertion_record_context
assertion_record_lineage
assertion_record_payload_reference
downstream_topology_input_manifest_record
assertion_record_validation_report
assertion_record_validation_summary
```

Together, these records answer:

```text
Which Corpus Generation was indexed,
which selected Registration Units were consumed,
which producer assertion registrations were inspected,
which producer claims were preserved,
which participants were preserved,
which relationships were preserved,
which evidence basis and context were preserved,
which lineage and reconstruction references were preserved,
which records were indexed, deferred, unsupported, or failed,
and which records are safe to hand off to Evidence Topology?
```

---

# Assertion Record Index Identity Schema

Every Assertion Record Index must have a stable identity.

## Required Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_record_index_id` | yes | Stable identity for the Assertion Record Index. |
| `assertion_record_index_label` | recommended | Human-readable label. |
| `input_corpus_generation_id` | yes | Corpus Generation indexed by this Assertion Record Index. |
| `input_corpus_generation_manifest_reference` | yes | Reference to the input Corpus Generation manifest. |
| `input_downstream_assertion_record_manifest_reference` | yes | Reference to the Phase 4.2 downstream Assertion Record input manifest. |
| `assertion_record_indexing_policy_id` | yes | Assertion Record indexing policy identifier. |
| `assertion_record_indexing_policy_version` | recommended | Indexing policy version. |
| `producer_resolver_policy_id` | recommended | Resolver policy set identifier. |
| `producer_resolver_policy_version` | recommended | Resolver policy version. |
| `builder_name` | yes | Builder process or script name. |
| `builder_version` | recommended | Builder version. |
| `indexing_timestamp` | yes | Timestamp of Assertion Record indexing. |
| `schema_version` | recommended | Assertion Record schema version. |
| `contract_version` | recommended | Assertion Record contract version. |
| `validation_status` | yes | Assertion Record Index validation status. |
| `certification_status` | recommended | Certification status when available. |

## Initial MARK Identity

Recommended initial identity:

```text
assertion_record_index_id: mark_phase4_corpus_6tep_v1_assertion_record_index
assertion_record_index_label: MARK Phase 4 6-TEP Assertion Record Index
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
assertion_record_indexing_policy_id: mark_phase4_vap_gsc_assertion_record_indexing_policy
assertion_record_indexing_policy_version: v1
producer_resolver_policy_id: mark_phase4_vap_gsc_assertion_resolver_policy
producer_resolver_policy_version: v1
```

The Assertion Record Index identity is distinct from individual Assertion Record identity.

---

# Source Assertion Key Strategy

The schema distinguishes source assertion identity from corpus-indexed Assertion Record identity.

```text
source_assertion_key
    Stable identity for the producer assertion registration source,
    independent of a specific Corpus Generation when possible.

assertion_id
    Stable corpus-indexed Assertion Record identity used within a specific
    Corpus Generation.
```

The same underlying producer assertion may participate in more than one Corpus Generation.

When this occurs, each corpus-indexed Assertion Record must preserve which Corpus Generation selected the source assertion.

A deterministic `assertion_id` should be derived from stable source components when available.

Recommended source components:

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

If stable Assertion Record identity cannot be produced, the record must fail validation or be emitted with explicit unresolved identity status according to the declared validation policy.

---

# Assertion Record Core Schema

An `AssertionRecord` represents one preserved producer claim inside a declared Corpus Generation.

```text
AssertionRecord
├── assertion_record_index_id
├── assertion_id
├── source_assertion_key
├── producer_identity
├── assertion_type
├── relationship_summary
├── participant_resolution_status
├── evidence_basis_resolution_status
├── context_resolution_status
├── provenance
├── authority_context
├── uncertainty_context
├── confidence_or_support_summary
├── independence_context_summary
├── temporal_or_generation_context
├── derivation
├── payload_reference_status
├── indexing_status
└── validation_status
```

## Required Core Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_record_index_id` | yes | Identity of the Assertion Record Index containing this record. |
| `assertion_id` | yes | Stable corpus-indexed Assertion Record identity. |
| `source_assertion_key` | yes | Stable source assertion key or explicit unresolved state. |
| `assertion_label` | recommended | Human-readable assertion label. |
| `assertion_type` | yes | Assertion type. |
| `producer_family` | yes | Producer family, such as `VAP` or `GSC`. |
| `producer_id` | recommended | Producer identifier or reference. |
| `registration_unit_id` | yes | Source Registration Unit identity. |
| `corpus_generation_id` | yes | Corpus Generation identity. |
| `source_package_id` | recommended | Source package identity. |
| `source_artifact_id` | recommended | Source artifact identity or explicit unresolved state. |
| `source_assertion_registration_id` | recommended | Source assertion registration identity when available. |
| `relationship_or_relationship_class` | yes | Preserved relationship or relationship class. |
| `participant_resolution_status` | yes | Participant preservation status. |
| `evidence_basis_resolution_status` | yes | Evidence basis preservation status. |
| `context_resolution_status` | yes | Context preservation status. |
| `authority_context` | recommended | Authority context or explicit unresolved state. |
| `uncertainty_context` | recommended | Uncertainty or epistemic context. |
| `confidence_or_support_context` | optional | Producer confidence or support context summary. |
| `independence_context` | optional | Independence context summary. |
| `temporal_or_generation_context` | recommended | Temporal or generation context summary. |
| `payload_reference_status` | recommended | Payload reference status. |
| `indexing_status` | yes | Indexing status. |
| `validation_status` | yes | Validation status. |
| `builder_name` | yes | Builder process or script name. |
| `builder_version` | recommended | Builder version. |
| `indexed_at` | yes | Indexing timestamp. |

## Producer Identity Substructure

Recommended producer identity fields:

```text
producer_family
producer_repository
producer_version
run_id
release_id
package_id
tep_id
producer_reference
```

Producer identity must not be removed, replaced, or silently rewritten.

---

# Relationship Table Schema

Relationships may be unary, binary, or higher-order.

VDB must not force all assertions into a pairwise subject-predicate-object model when the producer claim requires a richer participant structure.

Canonical relationship table:

```text
assertion_record_relationships.tsv
```

## Required Relationship Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `relationship_id` | recommended | Relationship record identity. |
| `relationship_type` | yes | Relationship type. |
| `relationship_label` | recommended | Human-readable relationship label. |
| `relationship_directionality` | conditional | Directionality when applicable. |
| `relationship_arity` | recommended | Unary, binary, ternary, or higher-order arity. |
| `relationship_class` | recommended | Broader relationship class. |
| `relationship_context` | optional | Relationship-specific context. |
| `producer_family` | yes | Producer family. |
| `assertion_type` | yes | Assertion type. |
| `validation_status` | yes | Relationship validation status. |

Initial relationship examples:

```text
variant observed in sample
variant assigned interpretation label
variant associated with gene
phenotype has semantic prior for gene
source contributes evidence for gene
producer contract validation result
gene differentially expressed under condition
sample-gene prioritization output
inheritance compatibility assertion
```

Relationship preservation does not imply biological correctness.

A relationship inside an Assertion Record represents what the producer claimed.

It does not represent VDB endorsement.

---

# Participant Table Schema

Participants are scientific or contextual entities participating in an assertion.

Participants must be role-bearing.

Canonical participant table:

```text
assertion_record_participants.tsv
```

## Required Participant Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `participant_id` | recommended | Participant record identity. |
| `participant_role` | yes | Role played by the participant. |
| `participant_kind` | recommended | Participant kind or category. |
| `participant_namespace` | recommended | Source namespace. |
| `participant_value` | conditional | Source-native participant value or explicit unresolved state. |
| `participant_label` | optional | Human-readable participant label. |
| `source_identity_reference` | recommended | Source identity reference when available. |
| `source_artifact_reference` | recommended | Source artifact reference when available. |
| `source_record_reference` | recommended | Source row or record reference when available. |
| `producer_family` | yes | Producer family. |
| `participant_context` | optional | Participant-specific context. |
| `resolution_status` | yes | Participant resolution status. |
| `validation_status` | yes | Participant validation status. |

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

---

# Evidence Basis Table Schema

Evidence basis records preserve the evidence supporting or carrying the producer claim.

Canonical evidence basis table:

```text
assertion_record_evidence_basis.tsv
```

## Required Evidence Basis Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `evidence_basis_id` | recommended | Evidence basis record identity. |
| `evidence_basis_type` | yes | Evidence basis type. |
| `evidence_basis_reference` | recommended | Stable basis reference when available. |
| `source_artifact_reference` | recommended | Source artifact reference. |
| `source_row_reference` | optional | Source row reference when available. |
| `source_record_reference` | optional | Source record reference when available. |
| `source_table_reference` | optional | Source table reference when available. |
| `source_file_reference` | optional | Source file reference when available. |
| `source_database_snapshot` | optional | Source database snapshot when available. |
| `source_method` | optional | Source method when available. |
| `source_score` | optional | Source score when available. |
| `source_count` | optional | Source count when available. |
| `source_threshold` | optional | Source threshold when available. |
| `source_validation_result` | optional | Source validation result when available. |
| `source_provenance_channel` | optional | Source provenance channel when available. |
| `source_contribution_channel` | optional | Source contribution channel when available. |
| `producer_payload_reference` | optional | Producer payload reference when applicable. |
| `external_snapshot_reference` | optional | External evidence snapshot reference when applicable. |
| `resolution_status` | yes | Evidence basis resolution status. |
| `validation_status` | yes | Evidence basis validation status. |

Evidence basis may be represented directly or by reconstructable reference.

Large payloads do not need to be duplicated inside the Assertion Record if reconstruction is guaranteed.

Evidence basis must not be replaced by opaque summaries that prevent reconstruction.

---

# Context Table Schema

Context records preserve boundaries under which the producer emitted the claim.

Canonical context table:

```text
assertion_record_context.tsv
```

## Required Context Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `context_id` | recommended | Context record identity. |
| `context_type` | yes | Context type. |
| `context_value` | conditional | Context value or explicit unresolved state. |
| `context_reference` | optional | Context reference when available. |
| `context_namespace` | optional | Context namespace when applicable. |
| `producer_family` | yes | Producer family. |
| `source_artifact_reference` | recommended | Source artifact reference when applicable. |
| `resolution_status` | yes | Context resolution status. |
| `validation_status` | yes | Context validation status. |

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

---

# Lineage Table Schema

Lineage records preserve reconstruction paths from Assertion Records back to Corpus Generation, Registration Units, source packages, source artifacts, assertion registrations, and source identities.

Canonical lineage table:

```text
assertion_record_lineage.tsv
```

## Required Lineage Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `assertion_record_index_id` | yes | Assertion Record Index identity. |
| `corpus_generation_id` | yes | Corpus Generation identity. |
| `corpus_generation_manifest_reference` | recommended | Corpus Generation manifest reference. |
| `downstream_assertion_record_input_manifest_reference` | yes | Phase 4.2 handoff manifest reference. |
| `registration_unit_id` | yes | Registration Unit identity. |
| `registration_unit_reference` | recommended | Registration Unit reference. |
| `source_package_id` | recommended | Source package identity. |
| `source_package_reference` | recommended | Source package reference. |
| `source_artifact_id` | recommended | Source artifact identity. |
| `source_artifact_reference` | recommended | Source artifact reference. |
| `source_assertion_registration_id` | recommended | Source assertion registration identity. |
| `source_identity_references` | recommended | Source identity references when applicable. |
| `producer_family` | yes | Producer family. |
| `producer_reference` | recommended | Producer reference. |
| `indexing_process` | yes | Indexing process or builder. |
| `indexing_process_version` | recommended | Builder version. |
| `contract_version` | recommended | Contract version. |
| `schema_version` | recommended | Schema version. |
| `validation_report_reference` | recommended | Validation report reference when available. |
| `reconstruction_status` | yes | Reconstruction status. |

An Assertion Record without reconstructable lineage is not VDB-compliant.

---

# Payload Reference Table Schema

Producer-specific or large payloads may be preserved by reference.

Canonical payload reference table:

```text
assertion_record_payload_references.tsv
```

## Required Payload Reference Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_id` | yes | Assertion Record identity. |
| `payload_reference_id` | recommended | Payload reference identity. |
| `payload_reference_type` | yes | Payload reference type. |
| `payload_reference` | conditional | Payload reference or explicit unresolved state. |
| `source_artifact_reference` | recommended | Source artifact reference. |
| `source_row_reference` | optional | Source row reference when available. |
| `source_record_reference` | optional | Source record reference when available. |
| `source_table_reference` | optional | Source table reference when available. |
| `producer_payload_path` | optional | Producer payload path when applicable. |
| `checksum_reference` | optional | Checksum reference when available. |
| `payload_resolution_status` | yes | Payload resolution status. |
| `payload_lossiness_status` | yes | Payload lossiness status. |
| `validation_status` | yes | Payload reference validation status. |

Required semantic fields must not exist only inside an opaque payload.

Payload references must be resolvable or explicitly marked as unavailable.

If payload references cannot be resolved, reconstruction limitations must be visible.

---

# Downstream Topology Input Manifest Schema

The downstream topology input manifest makes Evidence Topology derivation deterministic.

Canonical artifact:

```text
downstream_topology_input_manifest.tsv
```

This manifest is not Evidence Topology.

It must not contain topology relationships unless explicitly produced by the Evidence Topology implementation.

## Required Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `assertion_record_index_id` | yes | Assertion Record Index identity. |
| `corpus_generation_id` | yes | Corpus Generation identity. |
| `assertion_id` | yes | Assertion Record identity. |
| `assertion_type` | yes | Assertion type. |
| `producer_family` | yes | Producer family. |
| `relationship_or_relationship_class` | yes | Relationship or relationship class. |
| `participant_reference_summary` | recommended | Participant references or summary. |
| `source_identity_reference_summary` | recommended | Source identity reference summary when applicable. |
| `registration_unit_id` | yes | Source Registration Unit identity. |
| `uncertainty_context` | recommended | Uncertainty context. |
| `independence_context` | optional | Independence context. |
| `temporal_or_generation_context` | recommended | Temporal or generation context. |
| `validation_status` | yes | Assertion Record validation status. |

The downstream topology input manifest enables Evidence Topology derivation.

It does not perform Evidence Topology derivation.

---

# Validation Receipt Schema

Assertion Record validation receipts must live under:

```text
results/validation/phase4_assertion_records/
```

Implemented validation receipt artifacts should include:

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

The JSON validation report may include nested findings grouped by input validation, record validation, reconciliation validation, and anti-collapse validation.

---

# Validation Tiers

Assertion Record validation should operate in four tiers.

```text
Tier 1: Input Validation
Tier 2: Record Validation
Tier 3: Reconciliation Validation
Tier 4: Anti-Collapse Validation
```

## Tier 1: Input Validation

Confirms that the declared Corpus Generation and selected Registration Units are available.

## Tier 2: Record Validation

Confirms that each Assertion Record satisfies preservation obligations.

## Tier 3: Reconciliation Validation

Confirms that indexing behavior is complete, deterministic, and explainable.

## Tier 4: Anti-Collapse Validation

Confirms that Assertion Record indexing did not exceed its layer authority.

Validation must confirm preservation and reconstructability.

Validation must not claim biological correctness.

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

## Authority Context Vocabulary

Allowed values or phrases may include:

```text
producer_assertion
producer_observation
producer_annotation
producer_semantic_prior
registration_preservation
corpus_indexed_preservation
validation_result
not_reported
not_applicable
unresolved
```

## Uncertainty Context Vocabulary

Allowed values or phrases may include:

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

## Derivation Vocabulary

Allowed values:

```text
direct_producer_assertion
artifact_level_registration
row_level_projection
namespace_brokerage
semantic_projection
topological_projection
statistical_projection
manual_review
```

For Phase 4.3 direct producer-claim preservation, the preferred value is:

```text
direct_producer_assertion
```

Derived topology, geometry, surface, or projection values must not be produced by the Assertion Record layer.

---

# Layer 2 Golden Fixture Expectation

Phase 4.3 should use a compressed real-row Layer 2 golden fixture derived from the canonical six-unit Corpus Generation.

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

Layer 2 should prove:

```text
VAP resolver works against compressed real VAP assertion registrations
GSC resolver works against compressed real GSC assertion registrations
assertion counts reconcile to fixture Registration Units
unsupported or deferred assertion registrations are counted
participants are role-bearing
relationships are explicit
lineage points back to Registration Units and Corpus Generation
outputs are deterministic
anti-collapse checks pass
```

Layer 2 fixture records are validation fixtures.

They are not canonical build artifacts.

---

# VAP AssertionRecord Example

```yaml
assertion_record_index_id: mark_phase4_corpus_6tep_v1_assertion_record_index
assertion_id: assertion_vap_example_001
source_assertion_key: mark_phase4_corpus_6tep_v1|vap_hg002|vap_variant_observation|15:89333596:T:TTGC
assertion_label: HG002 variant observation 15:89333596:T:TTGC
assertion_type: variant_observation
producer_family: VAP
producer_id: variant_annotation_pipeline
registration_unit_id: vap_hg002
corpus_generation_id: mark_phase4_corpus_6tep_v1
source_package_id: vap_tep_HG002_run_2026_06_03_010030
source_artifact_id: annotated_variants
source_assertion_registration_id: not_reported
relationship_or_relationship_class: variant observed in sample
participant_resolution_status: resolved
evidence_basis_resolution_status: resolved
context_resolution_status: resolved
authority_context: producer_observation
uncertainty_context: not_reported
confidence_or_support_context: quality_flag:PASS
independence_context: pipeline_run:run_2026_06_03_010030
temporal_or_generation_context: run_2026_06_03_010030
payload_reference_status: lossless_by_reference
indexing_status: indexed_with_note
validation_status: passed_with_note
builder_name: build_assertion_record_index
builder_version: not_reported
indexed_at: null
```

Associated participant records:

```yaml
- assertion_id: assertion_vap_example_001
  participant_role: sample
  participant_kind: sample
  participant_namespace: vap_sample_id
  participant_value: HG002
  participant_label: HG002
  source_identity_reference: not_reported
  source_artifact_reference: annotated_variants
  source_record_reference: row:1
  producer_family: VAP
  resolution_status: resolved
  validation_status: passed

- assertion_id: assertion_vap_example_001
  participant_role: variant
  participant_kind: variant
  participant_namespace: vap_variant_id
  participant_value: 15:89333596:T:TTGC
  participant_label: 15:89333596:T:TTGC
  source_identity_reference: not_reported
  source_artifact_reference: annotated_variants
  source_record_reference: row:1
  producer_family: VAP
  resolution_status: resolved
  validation_status: passed
```

---

# GSC AssertionRecord Example

```yaml
assertion_record_index_id: mark_phase4_corpus_6tep_v1_assertion_record_index
assertion_id: assertion_gsc_example_001
source_assertion_key: mark_phase4_corpus_6tep_v1|gsc_mitochondrial_disease|gsc_semantic_prior|mitochondrial_disease|ENSG00000140521
assertion_label: mitochondrial_disease semantic prior for POLG
assertion_type: semantic_prior
producer_family: GSC
producer_id: gene_set_consensus
registration_unit_id: gsc_mitochondrial_disease
corpus_generation_id: mark_phase4_corpus_6tep_v1
source_package_id: mitochondrial_semantic_gtr_experimental
source_artifact_id: consensus_gene_set
source_assertion_registration_id: not_reported
relationship_or_relationship_class: phenotype has semantic prior for gene
participant_resolution_status: resolved
evidence_basis_resolution_status: resolved
context_resolution_status: resolved
authority_context: producer_semantic_prior
uncertainty_context: positive
confidence_or_support_context: semantic_score:0.94
independence_context: pipeline_run:run_2026_06_23_015533
temporal_or_generation_context: run_2026_06_23_015533
payload_reference_status: lossless_by_reference
indexing_status: indexed_with_note
validation_status: passed_with_note
builder_name: build_assertion_record_index
builder_version: not_reported
indexed_at: null
```

Associated participant records:

```yaml
- assertion_id: assertion_gsc_example_001
  participant_role: phenotype
  participant_kind: phenotype
  participant_namespace: gsc_phenotype
  participant_value: mitochondrial_disease
  participant_label: mitochondrial_disease
  source_identity_reference: not_reported
  source_artifact_reference: consensus_gene_set
  source_record_reference: row:1
  producer_family: GSC
  resolution_status: resolved
  validation_status: passed

- assertion_id: assertion_gsc_example_001
  participant_role: gene
  participant_kind: gene
  participant_namespace: gsc_ensembl_gene_id
  participant_value: ENSG00000140521
  participant_label: POLG
  source_identity_reference: not_reported
  source_artifact_reference: consensus_gene_set
  source_record_reference: row:1
  producer_family: GSC
  resolution_status: resolved
  validation_status: passed
```

---

# File Format Conventions

## TSV

TSV files provide compact, operator-readable tabular records.

The primary TSV build artifacts are:

```text
assertion_record_index_manifest.tsv
assertion_record_index.tsv
assertion_record_participants.tsv
assertion_record_relationships.tsv
assertion_record_evidence_basis.tsv
assertion_record_context.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
downstream_topology_input_manifest.tsv
```

The primary TSV validation receipt artifacts are:

```text
assertion_record_validation_report.tsv
assertion_record_validation_summary.tsv
```

## JSON

JSON files provide richer machine-readable metadata and summaries.

The primary JSON build artifact is:

```text
assertion_record_index_manifest.json
```

The primary JSON validation receipt artifacts are:

```text
assertion_record_validation_report.json
assertion_record_validation_summary.json
```

## JSONL

JSONL may represent one Assertion Record per line.

Canonical JSONL build artifact:

```text
assertion_record_index.jsonl
```

JSONL records must preserve the same semantics as the TSV family.

## Markdown

Markdown reports provide human-readable inspection summaries.

Canonical Markdown build artifact:

```text
assertion_record_index_report.md
```

Markdown reports are not substitutes for machine-readable Assertion Record artifacts or validation receipts.

---

# Anti-Collapse Safeguards

This schema prohibits:

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

Any implementation that performs one of these actions violates this schema.

---

# Schema Completion Criteria

The Assertion Record schema is satisfied when Phase 4.3 implementation can emit artifacts that:

```text
consume a declared Corpus Generation explicitly
consume the downstream Assertion Record input manifest explicitly
preserve Assertion Record Index identity
preserve stable Assertion Record identities
preserve source assertion keys or explicit unresolved identity states
preserve producer identity
preserve assertion type
preserve relationships or relationship classes
preserve role-bearing participants
preserve evidence basis or explicit absence
preserve context or explicit absence
preserve provenance and lineage
preserve authority context
preserve uncertainty context
preserve confidence or support context when available
preserve independence context when available
preserve temporal or generation context when available
preserve Registration Unit lineage
preserve Corpus Generation lineage
preserve source artifact lineage
preserve source identity lineage when applicable
preserve payload references or expose reconstruction limitations
report indexed assertion registrations
report indexed-with-note assertion registrations
report unsupported assertion registrations
report deferred assertion registrations
report failed assertion registrations
emit deterministic machine-readable Assertion Record artifacts
emit deterministic human-readable Assertion Record report
emit deterministic validation receipts
emit deterministic downstream topology input manifest
avoid mutating Registration Units
avoid expanding Corpus Generation scope
avoid deriving topology
avoid characterizing geometry
avoid constructing surfaces
avoid emitting projections
avoid biological interpretation
preserve anti-collapse safeguards
```

This schema is not satisfied merely because rows, records, files, or indexes exist.

It is satisfied only when those artifacts preserve producer scientific claims, remain reconstructable, preserve lineage, expose unresolved states, and can safely serve as the claim substrate for Evidence Topology derivation.

---

# Summary

The Assertion Record schema defines the Phase 4.3 preserved scientific claim layer.

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

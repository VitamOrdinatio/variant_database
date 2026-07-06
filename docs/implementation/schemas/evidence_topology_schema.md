# Evidence Topology Schema

## Epoch II: Evidence Geometry

| Epoch | Epoch Identity        | Epoch Purpose                                                                                       |
| ----- | --------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer           | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | **Evidence Geometry** | **Once assertions exist, how are preserved claims organized without becoming biological conclusions?** |
| III   | Discovery Layer       | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer      | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer       | Why do we do this?                                                                                  |

---

## Relationship To Design, Specification, And Contract

This schema implements the structural representation required by:

```text
docs/design/evidence_topology_model.md
docs/implementation/specifications/evidence_topology_spec.md
docs/contracts/evidence_topology/evidence_topology_contract.md
```

The design document defines the conceptual model.

The specification defines implementation requirements.

The contract defines non-negotiable Evidence Topology obligations.

This schema defines the logical objects, normalized artifacts, controlled vocabularies, and invariants that a Phase 4.4 Evidence Topology implementation must emit and validate.

If this schema conflicts with the Evidence Topology contract or VDB system contract, the contracts take precedence.

---

# Purpose

Evidence Topology objects represent deterministic organizational relationships derived from preserved Assertion Records inside a declared Corpus Generation.

Topology records are:

```text
derived
reconstructable
traceable
non-authoritative
corpus-bounded
relationship-explicit
dimension-explicit
basis-explicit
expansion-aware
representation-neutral
```

They organize preserved scientific evidence.

They are not themselves scientific evidence.

They do not perform biological reasoning, statistical inference, burden testing, Convergence Geometry, Evidence Convergence Surface construction, Projection View generation, or RDGP reasoning.

---

# Schema Role

This schema has two roles.

First, it defines the logical Evidence Topology object model:

```text
EvidenceTopologyBuild
        │
        └── EvidenceTopologyRelationship
                ├── RelationshipMember[]
                ├── BasisComponent[]
                ├── SourceIdentityExpansionHandle[]
                └── NamespaceMediationRecord[]
```

Second, it defines the normalized artifact family expected for Phase 4.4 implementation:

```text
topology_build_manifest.tsv
topology_build_manifest.json
topology_relationships.tsv
topology_relationships.jsonl
topology_relationship_members.tsv
topology_basis_components.tsv
topology_source_identity_expansion_index.tsv
topology_namespace_mediation.tsv
topology_metadata_relationships.tsv
topology_summary.tsv
topology_validation_report.tsv
topology_validation_report.json
topology_build_report.md
downstream_geometry_input_manifest.tsv
```

TSV artifacts are the normalized validation and reconstruction surface.

JSON and JSONL artifacts may preserve nested or machine-friendly forms.

Markdown reports are inspection aids.

No artifact in this schema may replace Assertion Records or acquire source authority.

---

# Initial Phase 4.4 Output Family

The initial canonical Phase 4.4 topology build is expected to write under:

```text
results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
```

The initial upstream Assertion Record surface is expected at:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

The initial handoff manifest is expected at:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/downstream_topology_input_manifest.tsv
```

The schema is not restricted to this corpus, but the first implementation target must satisfy this schema for `mark_phase4_corpus_6tep_v1_topology_build_v1`.

---

# Upstream Assertion Record Input Boundary

Evidence Topology consumes the validated Assertion Record surface.

A compliant Phase 4.4 builder may consume:

```text
assertion_record_index.tsv
assertion_record_index.jsonl
assertion_record_participants.tsv
assertion_record_source_identity_sets.tsv
assertion_record_source_identity_summary.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
assertion_record_validation_report.tsv
downstream_topology_input_manifest.tsv
```

Evidence Topology must not directly parse raw producer artifacts when Assertion Records are available.

Evidence Topology must not re-run ingestion.

Evidence Topology must not reconstruct Registration Units as an alternative source of topology truth.

Evidence Topology must not bypass Assertion Record primacy.

If a future topology builder performs controlled source-identity expansion, that expansion must be declared by policy, must preserve Assertion Record lineage, and must not mutate upstream Registration Units or Assertion Records.

---

# Artifact Family Overview

| Artifact | Required | Purpose |
| -------- | -------- | ------- |
| `topology_build_manifest.tsv` | Yes | Normalized manifest for the topology build identity, input surface, policy, builder, timestamps, and validation status. |
| `topology_build_manifest.json` | Yes | Machine-readable topology build manifest. |
| `topology_relationships.tsv` | Yes | Normalized topology relationship index. |
| `topology_relationships.jsonl` | Yes | JSONL topology relationship records. |
| `topology_relationship_members.tsv` | Yes | Explicit relationship membership records. |
| `topology_basis_components.tsv` | Yes | Explicit basis components explaining why each relationship exists. |
| `topology_source_identity_expansion_index.tsv` | Yes | Addressable Source Identity Set expansion handles for downstream controlled expansion without flattening identities into topology. |
| `topology_namespace_mediation.tsv` | Yes | Namespace mediation, unresolved-state, ambiguity, conflict, and direct-match status records. May be header-only or explicitly deferred when namespace mediation is not policy-enabled. |
| `topology_metadata_relationships.tsv` | Yes | Metadata-level topology subset for inspection and validation. Metadata relationships must also be represented in `topology_relationships.tsv`. |
| `topology_summary.tsv` | Yes | Build-level counts and relationship summaries. |
| `topology_validation_report.tsv` | Yes | Normalized validation check results. |
| `topology_validation_report.json` | Yes | Machine-readable validation summary. |
| `topology_build_report.md` | Yes | Human-readable topology build report. |
| `downstream_geometry_input_manifest.tsv` | Yes | Deterministic handoff manifest for Convergence Geometry. Must not contain geometry features. |

---

# Object: EvidenceTopologyBuild

Represents a deterministic topology construction event over a declared Assertion Record surface.

A topology build is derived organization.

It is not source evidence.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Stable topology construction identifier. |
| `topology_build_label` | string | Recommended | Human-readable label. Labels must not replace stable identity. |
| `input_corpus_generation_id` | string | Yes | Corpus Generation identity that bounds the topology. |
| `input_assertion_record_index_id` | string | Yes | Identifier for the Assertion Record index or equivalent source surface. |
| `input_downstream_topology_manifest_id` | string | Yes | Identifier for the downstream topology input manifest consumed by the build. |
| `input_assertion_record_surface_path` | path/string | Yes | Path to the governed Assertion Record output family. |
| `topology_derivation_policy_id` | string | Yes | Stable derivation policy identity. |
| `topology_derivation_policy_version` | string | Yes | Derivation policy version. |
| `builder_name` | string | Yes | Builder implementation name. |
| `builder_version` | string | Yes | Builder implementation version. |
| `build_timestamp_utc` | datetime | Yes | UTC build timestamp. |
| `contract_version` | string | Recommended | Evidence Topology contract version when available. |
| `schema_version` | string | Recommended | Evidence Topology schema version when available. |
| `validation_status` | enum | Yes | Build validation status. |
| `certification_status` | enum | Recommended | Certification status when available. |

## Input Path Fields

The normalized build manifest should also preserve the governed input paths or resolvable references used by the build:

```text
input_assertion_record_index_path
input_assertion_record_jsonl_path
input_assertion_record_participants_path
input_assertion_record_source_identity_sets_path
input_assertion_record_source_identity_summary_path
input_assertion_record_lineage_path
input_assertion_record_validation_report_path
input_downstream_topology_manifest_path
```

These paths preserve reconstruction handles.

They do not transfer source authority to topology.

---

# Object/Table: EvidenceTopologyRelationship

Represents one deterministic organizational relationship derived from the governed Assertion Record surface.

A topology relationship may organize Assertion Records, participants, source identity set references, metadata classes, producer families, evidence domains, contexts, namespace states, or other policy-enabled organizational axes.

A topology relationship is not a biological conclusion.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_relationship_id` | string | Yes | Stable deterministic relationship identifier. |
| `topology_build_id` | string | Yes | Parent topology build. |
| `input_corpus_generation_id` | string | Yes | Corpus Generation identity. |
| `topology_dimension` | enum | Yes | Organizational dimension. |
| `relationship_kind` | enum/string | Yes | Specific relationship type emitted by policy. |
| `derivation_basis` | enum/string | Yes | Reconstructable reason the relationship exists. |
| `relationship_scope` | enum/string | Yes | Scope class such as assertion, source_identity_set, metadata, namespace, or corpus. |
| `relationship_classification` | enum | Yes | Immediate, expansion-required, or deferred-statistical-analysis classification. |
| `source_assertion_id_summary` | string/list | Yes | Stable sorted source Assertion Record identifiers. May be delimited in TSV. |
| `source_assertion_count` | integer | Yes | Count of source Assertion Records contributing to the relationship. |
| `registration_unit_id_summary` | string/list | Required when applicable | Stable sorted source Registration Unit identifiers. |
| `source_identity_set_id_summary` | string/list | Required when applicable | Stable sorted Source Identity Set identifiers. |
| `relationship_member_summary` | string | Yes | Inspection summary of relationship members. Full members live in `topology_relationship_members.tsv`. |
| `basis_component_summary` | string | Yes | Inspection summary of basis components. Full components live in `topology_basis_components.tsv`. |
| `namespace_mediation_status` | enum | Yes | Namespace mediation status. |
| `source_identity_expansion_status` | enum | Yes | Whether granular source identity expansion is not applicable, available, required, deferred, or unavailable. |
| `statistical_testing_status` | enum | Yes | Whether the relationship is analysis-ready, requires expansion, or is not statistical input. |
| `validation_status` | enum | Yes | Relationship-level validation status. |

## Recommended Fields

```text
relationship_label
relationship_cardinality
relationship_summary
producer_family_summary
evidence_domain_summary
uncertainty_status_summary
temporal_context_summary
provenance_summary
lossiness_status
```

The relationship index may include summaries for inspection.

Summaries must not replace relationship members, basis components, source Assertion Record lineage, or expansion handles.

---

# Object/Table: RelationshipMember

Represents one explicit member of a topology relationship.

Relationship membership must be explicit.

Relationship membership must not imply biological importance.

Relationship membership must not replace Assertion Record lineage.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Parent topology build. |
| `topology_relationship_id` | string | Yes | Parent topology relationship. |
| `member_id` | string | Yes | Stable member identifier within the topology build. |
| `member_type` | enum/string | Yes | Kind of member. |
| `member_role` | string | Yes | Role within the organizational relationship. |
| `member_reference` | string | Yes | Source or topology reference for the member. |
| `member_namespace` | string | Required when applicable | Namespace for member value or reference. |
| `member_value` | string | Required when applicable | Member value. Must not imply canonical resolution without corresponding status. |
| `member_label` | string | Optional | Human-readable label. |
| `source_assertion_id` | string | Required when applicable | Source Assertion Record reference. |
| `source_assertion_registration_id` | string | Required when available | Source assertion registration reference. |
| `source_registration_unit_id` | string | Required when applicable | Source Registration Unit reference. |
| `source_corpus_generation_id` | string | Yes | Source Corpus Generation reference. |
| `source_identity_set_id` | string | Required when applicable | Source Identity Set reference. |
| `basis_component_id` | string | Required when applicable | Basis component supporting this member. |
| `validation_status` | enum | Yes | Member validation status. |

## Allowed Member Types

Initial member types include:

```text
assertion_record
participant
source_identity_set
source_artifact
registration_unit
corpus_generation
producer_family
evidence_domain
assertion_type
context
validation_status
resolver_status
namespace_state
metadata_value
```

---

# Object/Table: BasisComponent

Represents one reconstructable component used to derive a topology relationship.

Basis components explain why the topology relationship exists.

A topology relationship without explicit basis components is invalid unless the relationship is explicitly declared as a deferred or not-applicable validation record rather than an emitted topology relationship.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Parent topology build. |
| `topology_relationship_id` | string | Yes | Parent topology relationship. |
| `basis_component_id` | string | Yes | Stable basis component identifier. |
| `basis_component_type` | enum/string | Yes | Kind of basis component. |
| `basis_component_role` | string | Yes | Role of the component in derivation. |
| `basis_component_value` | string | Required when applicable | Value used as basis. |
| `basis_component_reference` | string | Required when applicable | Reference used as basis. |
| `basis_component_namespace` | string | Required when applicable | Namespace for value or reference. |
| `source_assertion_id` | string | Required when applicable | Source Assertion Record reference. |
| `source_assertion_registration_id` | string | Required when available | Source assertion registration reference. |
| `source_registration_unit_id` | string | Required when applicable | Source Registration Unit reference. |
| `source_corpus_generation_id` | string | Yes | Source Corpus Generation reference. |
| `source_identity_set_id` | string | Required when applicable | Source Identity Set reference. |
| `resolution_status` | enum | Yes | Resolution status for the basis component. |
| `ambiguity_status` | enum | Yes | Ambiguity status for the basis component. |
| `conflict_status` | enum | Yes | Conflict status for the basis component. |
| `lossiness_status` | enum | Yes | Lossiness status for the basis component. |
| `validation_status` | enum | Yes | Basis component validation status. |

---

# Object/Table: SourceIdentityExpansionIndex

The Source Identity Expansion Index preserves addressable links from topology relationships to Source Identity Sets without flattening large source identity universes into topology records.

This table is required for Phase 4.4 because the canonical Assertion Record surface is compact while source identity participation may be large.

It makes the identity universe:

```text
discoverable
countable
lineage-preserved
expansion-addressable
honestly classified for statistical testing
```

It does not itself perform source identity expansion.

It does not itself perform burden testing.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Parent topology build. |
| `topology_relationship_id` | string | Yes | Topology relationship requiring or exposing expansion handles. |
| `source_identity_set_id` | string | Yes | Source Identity Set reference from the Assertion Record layer. |
| `source_assertion_id` | string | Required when applicable | Source Assertion Record reference. |
| `source_assertion_registration_id` | string | Required when available | Source assertion registration reference. |
| `source_registration_unit_id` | string | Required when applicable | Source Registration Unit reference. |
| `input_corpus_generation_id` | string | Yes | Source Corpus Generation identity. |
| `source_identity_count` | integer | Yes | Count of source identities represented by the set. |
| `identity_kind` | string | Required when available | Identity kind represented by the set. |
| `participant_role` | string | Required when available | Participant role associated with the identity set. |
| `source_namespace` | string | Required when available | Source namespace associated with the identity set. |
| `expansion_status` | enum | Yes | Expansion availability or requirement status. |
| `expansion_policy_id` | string | Required when expansion is policy-governed | Policy governing expansion. |
| `expansion_required_for_statistical_testing` | boolean | Yes | Whether statistical testing requires controlled expansion beyond compact topology. |
| `statistical_testing_status` | enum | Yes | Statistical readiness status. |
| `recommended_downstream_use` | string | Recommended | Suggested downstream use such as geometry, surface, projection, RDGP-facing burden projection, or inspection. |
| `validation_status` | enum | Yes | Expansion index validation status. |

## Expansion Rule

Source identity counts are not independent evidence counts.

Source identity counts are not burden statistics.

Source identity counts do not imply biological convergence.

A source identity set count is an addressable preservation and reconstruction fact.

---

# Object/Table: NamespaceMediation

Namespace mediation records preserve whether a topology relationship is based on direct source identity, source namespace alignment, canonical identity attachment, namespace mediation, unresolved namespace state, ambiguity, conflict, or explicit deferral.

Namespace mediation must never masquerade as direct source identity matching.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Parent topology build. |
| `topology_relationship_id` | string | Yes | Parent topology relationship. |
| `source_identity_set_id` | string | Required when applicable | Source Identity Set reference. |
| `source_identity_reference` | string | Required when applicable | Source identity reference. |
| `source_namespace` | string | Required when applicable | Source namespace. |
| `canonical_identity_reference` | string | Required when applicable | Canonical identity reference, if available. |
| `namespace_event_reference` | string | Required when applicable | Namespace event reference, if available. |
| `identity_bridge_reference` | string | Required when applicable | Identity bridge reference, if available. |
| `match_type` | enum | Yes | Match type. |
| `resolution_status` | enum | Yes | Resolution status. |
| `ambiguity_status` | enum | Yes | Ambiguity status. |
| `conflict_status` | enum | Yes | Conflict status. |
| `resolution_provenance` | string | Required when applicable | Resolution provenance. |
| `validation_status` | enum | Yes | Namespace mediation validation status. |

---

# Object/Table: MetadataRelationship

Metadata-level topology relationships are allowed when explicitly enabled by derivation policy.

Metadata-level relationships may organize Assertion Records by corpus membership, registration unit membership, producer family, evidence domain, assertion type, validation status, resolver status, source identity obligation status, or other declared metadata basis.

Metadata-level topology must not imply biological relatedness.

Metadata-level topology must not become source evidence.

## Representation Rule

Metadata-level relationships must appear in:

```text
topology_relationships.tsv
```

They may also be copied into:

```text
topology_metadata_relationships.tsv
```

as an inspection and validation subset.

## Required Fields

`topology_metadata_relationships.tsv` should include the same core fields as `topology_relationships.tsv`, plus:

```text
metadata_basis_field
metadata_basis_value
metadata_policy_enabled
metadata_relationship_scope
```

---

# Object/Table: TopologySummary

Topology summaries are inspection and validation aids.

They must remain traceable to topology relationships.

They must not replace topology relationship records.

They must not replace Assertion Records.

They must not imply biological importance.

## Recommended Summary Metrics

```text
topology_build_id
input_corpus_generation_id
topology_relationship_count
topology_dimension_count
relationship_kind_count
assertion_record_participation_count
registration_unit_count
producer_family_count
evidence_domain_count
source_identity_set_reference_count
source_identity_count_represented
namespace_mediated_relationship_count
unresolved_namespace_relationship_count
ambiguous_namespace_relationship_count
conflicted_namespace_relationship_count
expansion_required_relationship_count
statistical_analysis_ready_relationship_count
metadata_relationship_count
validation_pass_count
validation_fail_count
```

Summary metrics are not source evidence.

---

# Object/Table: TopologyValidationReport

The topology validation report records validation checks over build identity, input boundary, relationship structure, lineage, source identity expansion handles, namespace mediation, metadata relationship policy enablement, determinism, and anti-collapse behavior.

## Required Fields

```text
topology_build_id
validation_check_id
validation_check_name
validation_check_category
validation_status
severity
observed_value
expected_value
message
source_artifact
```

Validation categories should include:

```text
input_boundary
build_identity
derivation_policy
relationship_structure
relationship_membership
basis_components
assertion_lineage
corpus_lineage
registration_unit_lineage
source_identity_expansion
namespace_mediation
metadata_relationships
downstream_geometry_handoff
determinism
non_mutation
authority_boundary
anti_collapse
```

Validation confirms organization and reconstructability.

Validation does not confirm biological correctness.

---

# Object/Table: DownstreamGeometryInputManifest

The downstream geometry input manifest makes Convergence Geometry derivation deterministic.

It identifies validated topology relationships that may be characterized by Convergence Geometry.

It must not contain geometry features.

It must not contain convergence regions.

It must not contain density, breadth, depth, producer diversity, evidence-domain diversity, modality diversity, structural motif, surface eligibility, disclosure, statistical significance, burden score, or biological interpretation fields.

## Required Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `topology_build_id` | string | Yes | Source topology build. |
| `input_corpus_generation_id` | string | Yes | Source Corpus Generation. |
| `input_assertion_record_index_id` | string | Yes | Source Assertion Record index. |
| `topology_relationship_id` | string | Yes | Source topology relationship. |
| `topology_dimension` | enum | Yes | Relationship dimension. |
| `relationship_kind` | enum/string | Yes | Relationship kind. |
| `derivation_basis` | enum/string | Yes | Relationship derivation basis. |
| `source_assertion_id_summary` | string/list | Yes | Source Assertion Record summary. |
| `relationship_member_summary` | string | Yes | Relationship member summary. |
| `basis_component_summary` | string | Yes | Basis component summary. |
| `namespace_mediation_status` | enum | Yes | Namespace mediation status. |
| `source_identity_expansion_status` | enum | Yes | Source identity expansion status. |
| `statistical_testing_status` | enum | Yes | Statistical testing status. |
| `validation_status` | enum | Yes | Validation status. |

---

# Controlled Vocabularies

Controlled vocabularies may be extended by future policy versions.

Existing values must not be silently redefined.

## Policy Alignment Rule

For a declared topology derivation policy, every policy-enabled value emitted by that policy must be recognized by this schema or explicitly declared as a policy-local extension.

This applies to:

```text
topology_dimension
relationship_kind
derivation_basis
relationship_scope
relationship_classification
source_identity_expansion_status
statistical_testing_status
namespace_mediation_status
match_type
resolution_status
ambiguity_status
conflict_status
lossiness_status
validation_status
certification_status
```

Policy-local extensions must not contradict the Evidence Topology contract, the VDB system contract, or existing schema vocabulary.

The initial Phase 4.4 policy:

```text
mark_phase4_vap_gsc_topology_derivation_policy_v1
```

must emit only schema-recognized values unless a policy-local extension is explicitly documented.

## topology_dimension

Initial controlled values:

```text
participant
relationship
context
provenance
producer
evidence_domain
namespace
epistemic_status
uncertainty_status
temporal
generation
registration_unit
corpus_generation
metadata
```


## relationship_kind

Initial controlled values are grouped by policy status.

### Phase 4.4 v1 Policy-Enabled Values

These values are enabled by the initial MARK Phase 4 VAP/GSC topology derivation policy.

```text
corpus_metadata_membership
registration_unit_membership
producer_family_membership
assertion_type_membership
relationship_class_membership
preservation_status_membership
resolver_status_membership
validation_status_membership
source_identity_set_status_membership
source_identity_set_role_namespace_membership
source_identity_resolution_status_membership
source_identity_lossiness_status_membership
```

### Policy-Conditional Or Future Values

These values may be enabled by future derivation policies, controlled source-identity expansion policies, namespace mediation policies, or downstream layers.

```text
shared_participant
shared_context
shared_relationship_class
shared_producer_family
shared_evidence_domain
source_identity_obligation_status_membership
namespace_mediated_participant_match
cross_producer_participant_intersection
cross_evidence_domain_participant_intersection
exact_source_identity_value_intersection
exact_variant_overlap
exact_gene_overlap
exact_sample_overlap
uncertainty_contrast
temporal_generation_match
registration_metadata_membership
```


## derivation_basis

Initial controlled values:

```text
shared_source_identity
shared_source_identity_set_role_kind_namespace
shared_source_identity_set_status
shared_source_identity_resolution_status
shared_source_identity_lossiness_status
shared_participant_role
shared_participant_value
shared_assertion_type
shared_relationship_class
shared_relationship_type
shared_preservation_status
shared_validation_status
shared_resolver_status
shared_phenotype_context
shared_sample_context
shared_gene_participant
shared_variant_participant
shared_producer_family
shared_evidence_domain
shared_registration_unit
shared_corpus_generation
namespace_mediated_match
metadata_membership
```

## relationship_scope

Initial controlled values:

```text
assertion
participant
source_identity_set
namespace
metadata
registration_unit
corpus_generation
producer_family
evidence_domain
context
```

## relationship_classification

Initial controlled values:

```text
immediately_derived_topology
expansion_required_topology
deferred_statistical_analysis
metadata_level_topology
```


## source_identity_expansion_status

Initial controlled values:

```text
not_required
available_by_source_identity_set_reference
requires_controlled_expansion
expanded_under_policy
deferred_by_policy
not_applicable
unavailable
header_only_not_policy_enabled
```

`available_by_source_identity_set_reference` means that granular source identities are not flattened into topology, but Source Identity Set references preserve an addressable expansion handle.

`requires_controlled_expansion` means that exact identity-value analysis or statistical testing requires a future declared expansion policy.

## statistical_testing_status

Initial controlled values:

```text
not_statistical_input
analysis_ready
requires_source_identity_expansion
requires_external_annotation
requires_case_control_design
deferred_to_projection_layer
not_applicable
```


## namespace_mediation_status

Initial controlled values:

```text
not_applicable
direct_source_identity
source_namespace_only
canonical_identity_attached
namespace_mediated
ambiguous
conflicted
unresolved
deferred_by_policy
```

`source_namespace_only` means that source namespace grouping or preservation is available, but canonical identity resolution has not been performed.

A `source_namespace_only` relationship must not be interpreted as a canonical identity match or namespace-mediated identity match.

## match_type

Initial controlled values:

```text
source_identity_match
source_namespace_match
canonical_identity_match
namespace_mediated_match
ambiguous_namespace_match
conflicted_namespace_match
unresolved_namespace_state
not_applicable
deferred
```

## resolution_status

Initial controlled values:

```text
resolved
unresolved
ambiguous
conflicted
deferred
not_applicable
```

## ambiguity_status

Initial controlled values:

```text
not_ambiguous
ambiguous
not_applicable
unknown
```

## conflict_status

Initial controlled values:

```text
not_conflicted
conflicted
not_applicable
unknown
```


## lossiness_status

Initial controlled values:

```text
lossless
lossless_by_reference
summary_only
reference_only
lossy
not_applicable
unknown
```

`lossless_by_reference` means that granular identities are not enumerated in the topology artifact, but a governed reference preserves reconstructability without evidence loss.


## validation_status

Initial controlled values:

```text
passed
passed_with_note
failed
not_applicable
deferred_by_policy
```

## Validation Status Scope Rule

Within Evidence Topology output artifacts, `validation_status` means topology-layer validation status unless the field name explicitly indicates an upstream source status.

When preserving upstream Assertion Record statuses, topology artifacts should use explicit summary field names such as:

```text
source_assertion_validation_status_summary
source_assertion_resolver_status_summary
source_assertion_preservation_status_summary
```

Topology-layer validation status values must not be confused with Assertion Record preservation or resolver states such as:

```text
preserved
supported
indexed_with_note
deferred
```

## certification_status

Initial controlled values:

```text
not_certified
certification_candidate
certified
not_applicable
```

---

# Phase 4.4 v1 Policy-Enabled Relationship Families

The initial MARK Phase 4 VAP/GSC topology derivation policy enables only conservative relationship families derived from Assertion Record metadata and Source Identity Set metadata.

The initial v1 policy-enabled families are:

```text
corpus_metadata_membership
registration_unit_membership
producer_family_membership
assertion_type_membership
relationship_class_membership
preservation_status_membership
resolver_status_membership
validation_status_membership
source_identity_set_status_membership
source_identity_set_role_namespace_membership
source_identity_resolution_status_membership
source_identity_lossiness_status_membership
```

These families are valid for conservative Phase 4.4 topology because they can be derived from the compact Assertion Record surface without flattening Source Identity Sets or asserting exact participant-value overlap.

The v1 policy does not enable:

```text
exact_source_identity_value_intersection
exact_variant_overlap
exact_gene_overlap
exact_sample_overlap
cross_producer_exact_participant_intersection
namespace_mediated_participant_value_match
biological_convergence
burden_score
case_control_enrichment
statistical_significance
rdgp_priority_signal
```

Those relationship families require future controlled expansion policies, namespace mediation policies, downstream geometry, projection-layer substrates, statistical analysis workflows, or downstream reasoning systems.

---

# Cardinality

```text
EvidenceTopologyBuild
    1
    ↓
EvidenceTopologyRelationship
    1..N
    ↓
RelationshipMember
    1..N
    ↓
BasisComponent
    1..N
```

Additional cardinalities:

```text
EvidenceTopologyRelationship
    0..N SourceIdentityExpansionIndex rows
    0..N NamespaceMediation rows

Metadata-level EvidenceTopologyRelationship
    1 optional MetadataRelationship subset row

EvidenceTopologyBuild
    1 TopologySummary
    1 TopologyValidationReport
    1 DownstreamGeometryInputManifest
```

A relationship may be pairwise, one-to-many, many-to-many, or higher-order.

Pairwise graph semantics are not required.

---

# Schema Invariants

Every valid `EvidenceTopologyBuild` must satisfy:

```text
topology_build_id is stable
input_corpus_generation_id is declared
input_assertion_record_index_id is declared
input Assertion Record surface path is declared
topology derivation policy is declared
builder identity is declared
build timestamp is declared
validation_status is declared
```

Every valid `EvidenceTopologyRelationship` must satisfy:

```text
derived from governed Assertion Record surface unless explicitly metadata-level
declares topology_dimension
declares relationship_kind
declares derivation_basis
declares relationship_scope
declares relationship_classification
has explicit members
has explicit basis components
traces to source Assertion Records unless explicitly metadata-level or corpus-level
traces to source Corpus Generation
traces to Registration Units when applicable
declares namespace_mediation_status
declares source_identity_expansion_status
declares statistical_testing_status
has validation_status
```

Every expansion-required relationship must satisfy:

```text
has at least one source_identity_set_id reference
has at least one SourceIdentityExpansionIndex row
states expansion_required_for_statistical_testing explicitly
states statistical_testing_status explicitly
```

Every namespace-mediated relationship must satisfy:

```text
has NamespaceMediation rows
states match_type explicitly
distinguishes direct source identity match from namespace-mediated match
preserves ambiguity, conflict, unresolved, or deferred status when applicable
```

Every metadata-level relationship must satisfy:

```text
is policy-enabled
states metadata_basis_field
states metadata_basis_value
states metadata_relationship_scope
preserves source Assertion Record lineage when derived from Assertion Records
preserves Corpus Generation lineage
preserves Registration Unit lineage when applicable
does not imply biological relatedness
does not become source evidence
```

No topology artifact may contain:

```text
Convergence Geometry features
convergence regions
surface eligibility
surface disclosure
Projection View replacement records
RDGP reasoning
biological causality
clinical actionability
statistical significance
burden scores
opaque connectedness scores replacing derivation basis
```

No topology artifact may treat:

```text
source identity count as independent evidence count
namespace-mediated identity as direct source identity
metadata membership as biological relatedness
topology relationship as source evidence
```

---

# Conservative Phase 4.4 v1 Example

The initial Phase 4.4 implementation should prefer conservative topology that is valid from the compact Assertion Record surface.

The following example illustrates `source_identity_set_role_namespace_membership` rather than an exact gene-value match.

```yaml
topology_build_id: mark_phase4_corpus_6tep_v1_topology_build_v1
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
topology_derivation_policy_id: mark_phase4_vap_gsc_topology_derivation_policy_v1

topology_relationship_id: topology_rel_source_identity_set_gene_ensembl_000001
topology_dimension: participant
relationship_kind: source_identity_set_role_namespace_membership
derivation_basis: shared_source_identity_set_role_kind_namespace
relationship_scope: source_identity_set
relationship_classification: expansion_required_topology
source_assertion_id_summary:
  - assertion_vap_example_001
  - assertion_gsc_example_001
source_identity_set_id_summary:
  - sis_vap_example_gene_ensembl
  - sis_gsc_example_gene_ensembl
namespace_mediation_status: deferred_by_policy
source_identity_expansion_status: requires_controlled_expansion
statistical_testing_status: requires_source_identity_expansion
validation_status: passed

relationship_members:
  - member_type: assertion_record
    member_role: source_assertion
    member_reference: assertion_vap_example_001
  - member_type: assertion_record
    member_role: source_assertion
    member_reference: assertion_gsc_example_001
  - member_type: source_identity_set
    member_role: shared_participant_identity_set
    member_reference: sis_vap_example_gene_ensembl
    member_namespace: ensembl_gene_id
  - member_type: source_identity_set
    member_role: shared_participant_identity_set
    member_reference: sis_gsc_example_gene_ensembl
    member_namespace: ensembl_gene_id

basis_components:
  - basis_component_type: source_identity_set_reference
    basis_component_role: shared_role_kind_namespace
    basis_component_value: gene|gene|ensembl_gene_id
    resolution_status: deferred
    ambiguity_status: not_applicable
    conflict_status: not_applicable
    lossiness_status: lossless_by_reference

source_identity_expansion_index:
  - source_identity_set_id: sis_vap_example_gene_ensembl
    source_identity_count: 49255528
    identity_kind: gene
    participant_role: gene
    source_namespace: ensembl_gene_id
    expansion_status: requires_controlled_expansion
    expansion_required_for_statistical_testing: true
    statistical_testing_status: requires_source_identity_expansion
```

This example does not assert that the two source identity sets share an exact gene value.

It asserts that the topology build has found a policy-valid relationship over source identity set role, kind, and namespace, and that exact participant-value analysis requires controlled expansion.

---

# Representation Independence

This schema intentionally avoids defining graph nodes or graph edges as governing primitives.

Evidence Topology is represented as organizational relationships rather than graph primitives.

The same topology may later be projected into:

```text
relational tables
SQLite tables
property graphs
hypergraphs
simplicial complexes
matrices
tensors
network views
dashboard views
future mathematical representations
```

without changing the preserved scientific meaning.

A graph projection is a Projection View over topology.

A graph projection is not topology itself.

---

# Summary

The Evidence Topology Schema provides the structural representation of deterministic organizational relationships derived from preserved Assertion Records.

It captures:

```text
topology construction identity
upstream Assertion Record surface identity
topology derivation policy
organizational relationships
relationship dimensions
relationship kinds
derivation bases
relationship members
basis components
Source Identity Set expansion handles
namespace mediation state
metadata-level topology
validation status
downstream Convergence Geometry handoff
```

The governing invariant is:

```text
Evidence Topology is compact and claim-derived, but not identity-blind.

It organizes preserved Assertion Records while preserving explicit,
validated handles to source identity sets for downstream controlled expansion,
geometry characterization, surface construction, projection, and future
RDGP-facing statistical workflows.
```

Evidence Topology is derived organization over preserved scientific assertions.

It is never itself preserved scientific evidence.

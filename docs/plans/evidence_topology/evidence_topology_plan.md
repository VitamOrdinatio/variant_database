# Evidence Topology Implementation Plan

## Purpose

This document defines the implementation plan for Evidence Topology construction in VDB Phase 4.

Evidence Topology is the deterministic, reconstructable organization of preserved Assertion Records within a declared Corpus Generation.

This plan describes how VDB will consume a governed Assertion Record index, apply an explicit topology derivation policy, derive topology relationships, preserve relationship members and basis components, validate reconstructability, preserve namespace state, and provide downstream input to Convergence Geometry.

The Phase 4 Evidence Topology implementation goal is:

```text
Deterministically derive reconstructable topology relationships over
preserved Assertion Records inside a declared Corpus Generation while
preserving derivation basis, relationship members, source lineage,
namespace state, and Assertion Record primacy.
```

Evidence Topology connects preserved claims.

Evidence Topology does not interpret preserved claims.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/evidence_topology/evidence_topology_contract.md
```

The governing contract states that Evidence Topology must remain:

```text
assertion-derived
corpus-bounded
deterministic
relationship-explicit
dimension-explicit
basis-explicit
traceable
representation-neutral
projection-neutral
non-interpretive
reconstructable
```

This plan is subordinate to the Evidence Topology contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Evidence Topology implementation role is to derive explicit organizational relationships over preserved Assertion Records within a declared Corpus Generation.

An Evidence Topology implementation answers:

```text
What is connected within the declared corpus?
```

It does not answer:

```text
What structural properties emerge from those connections?

Which convergence regions are important?

Which surfaces are eligible for disclosure?

What projections should consumers receive?

What biological meaning should downstream systems infer?

Whether a connection is causal?

Whether a connection is clinically actionable?

Whether a connected participant should be prioritized?
```

Those questions belong to downstream implementation plans or downstream reasoning systems.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Registration Unit repair
Corpus Generation selection
Assertion Record indexing
raw producer artifact parsing
producer TEP parsing
Convergence Geometry characterization
Evidence Convergence Surface construction
Projection View generation
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
priority assignment
```

Evidence Topology construction is derived organization work.

It is not preservation-authority work.

It is not geometry work.

It is not surface-governance work.

It is not projection work.

It is not reasoning work.

---

# Initial Implementation Target

The initial implementation target is the Evidence Topology build for the first MARK Phase 4 Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

The initial topology build may be identified as:

```text
mark_phase4_corpus_6tep_v1_topology_build_v1
```

The expected upstream input is the downstream topology input manifest emitted by the Assertion Record implementation, such as:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
    downstream_topology_input_manifest.tsv
```

The initial Evidence Topology implementation should consume the Assertion Record index for the declared Corpus Generation and emit deterministic topology relationship artifacts for downstream Convergence Geometry derivation.

This topology build is not Convergence Geometry.

It is the organized relationship substrate from which Convergence Geometry may later characterize structure.

---

# Inputs

The Evidence Topology implementation consumes:

```text
Corpus Generation manifest
Assertion Record index
downstream topology input manifest
Assertion Record validation report when available
topology derivation policy
namespace mediation policy when applicable
Evidence Topology contract version
Assertion Record contract version
Corpus Generation contract version
system contract version
builder name
builder version
build timestamp
```

Evidence Topology must consume governed VDB sources.

The normal Phase 4 input chain is:

```text
Corpus Generation
        ↓
Assertion Record index
        ↓
Evidence Topology Build
```

Evidence Topology must not directly parse raw producer artifacts when Assertion Records are available.

Evidence Topology must not re-run ingestion.

Evidence Topology must not reconstruct Registration Units.

Evidence Topology must not bypass Assertion Record primacy.

---

# Outputs

The Evidence Topology implementation should emit deterministic artifacts outside the Assertion Record index and selected Registration Units.

Expected outputs may include:

```text
topology_build_manifest.tsv
topology_build_manifest.json
topology_relationships.tsv
topology_relationships.jsonl
topology_relationship_members.tsv
topology_basis_components.tsv
topology_namespace_mediation.tsv
topology_metadata_relationships.tsv
topology_summary.tsv
topology_validation_report.json
topology_validation_report.tsv
topology_build_report.md
downstream_geometry_input_manifest.tsv
```

These outputs are Evidence Topology artifacts.

They do not replace Assertion Records.

They do not replace Corpus Generations.

They do not replace Registration Units.

They do not create geometry features.

They do not declare surface eligibility.

They do not create projections.

They do not perform biological reasoning.

---

# Recommended Output Location

Initial Phase 4 Evidence Topology outputs may be written under:

```text
results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
```

A recommended initial layout is:

```text
results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
    topology_build_manifest.tsv
    topology_build_manifest.json
    topology_relationships.tsv
    topology_relationships.jsonl
    topology_relationship_members.tsv
    topology_basis_components.tsv
    topology_namespace_mediation.tsv
    topology_metadata_relationships.tsv
    topology_summary.tsv
    topology_validation_report.json
    topology_validation_report.tsv
    topology_build_report.md
    downstream_geometry_input_manifest.tsv
```

The output location should be configurable.

Evidence Topology output paths must not be confused with Assertion Record source paths, Corpus Generation manifest paths, or Registration Unit source paths.

---

# Required Topology Build Identity

Every Evidence Topology Build must have a stable identity.

A Topology Build identity must preserve:

```text
topology_build_id
topology_build_label when available
input_corpus_generation_id
input_assertion_record_index_id when available
topology_derivation_policy_id
topology_derivation_policy_version when available
builder_name
builder_version when available
build_timestamp
validation_status
certification_status when available
```

For the initial MARK topology build, a recommended identity shape is:

```text
topology_build_id: mark_phase4_corpus_6tep_v1_topology_build_v1
topology_build_label: MARK Phase 4 6-TEP Evidence Topology Build v1
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
topology_derivation_policy_id: mark_phase4_vap_gsc_topology_derivation_policy
topology_derivation_policy_version: v1
```

Topology Build identity must remain stable across:

```text
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
validation
certification
reconstruction
```

Human-readable labels may support inspection.

Labels must not replace stable Topology Build identity.

---

# Topology Derivation Policy Requirements

Every Evidence Topology Build must declare a topology derivation policy.

The topology derivation policy must define:

```text
input Assertion Record source
eligible Assertion Record types
eligible participant roles
eligible relationship classes
eligible context fields
eligible source identity fields
enabled topology dimensions
enabled relationship kinds
enabled derivation bases
namespace mediation rules
metadata-level topology rules
discovery and overlay rules when applicable
unsupported relationship behavior
unresolved-state behavior
lossiness behavior
validation behavior
```

For the initial MARK topology build, the policy may be identified as:

```text
mark_phase4_vap_gsc_topology_derivation_policy_v1
```

The initial policy should focus on conservative topology derivation over VAP and GSC Assertion Records.

The policy must not define biological meaning.

The policy must not define geometry features.

The policy must not define surface eligibility.

The policy must not define RDGP reasoning behavior.

---

# Initial Topology Dimensions

The initial implementation should enable a conservative set of topology dimensions.

Recommended initial dimensions include:

```text
participant
relationship
context
producer
evidence_domain
namespace
uncertainty_status
temporal
generation
registration_unit
corpus_generation
```

Future or conditional dimensions may include:

```text
provenance
independence
overlay
discovery
external_authority
```

Topology dimensions are organizational axes.

They are not biological conclusions.

A topology dimension must not silently combine multiple dimensions unless the derivation policy explicitly declares a composite basis.

Composite topology relationships must preserve each contributing dimension.

---

# Relationship Kind Requirements

Every topology relationship must declare a relationship kind.

Recommended initial relationship kinds include:

```text
shared_participant
shared_context
shared_relationship_class
shared_producer_family
shared_evidence_domain
namespace_mediated_participant_match
cross_producer_participant_intersection
cross_evidence_domain_participant_intersection
cross_modality_participant_intersection_when_available
uncertainty_contrast
temporal_generation_match
registration_metadata_membership
corpus_metadata_membership
```

Relationship kinds must describe organization.

Relationship kinds must not assert biological meaning.

The following kinds are prohibited at the Evidence Topology layer:

```text
biological_convergence
candidate_gene_support
causal_link
pathogenicity_support
phenotype_explanation
confidence_relationship
surface_eligible_region
high_value_region
clinically_actionable_connection
```

Those concepts belong to downstream geometry, surface governance, projection shaping, reasoning systems, or returned producer assertions.

---

# Topology Relationship Identity Strategy

Every topology relationship must have a stable identity.

A deterministic `topology_relationship_id` should be derived from stable components when available, such as:

```text
topology_build_id
topology_dimension
relationship_kind
derivation_basis
relationship member references
basis component references
source Assertion Record identifiers
```

For example, a participant-based relationship identity may be derived from:

```text
topology_build_id
topology_dimension = participant
relationship_kind = shared_participant
derivation_basis = shared gene participant
participant_role
participant_value
participant_namespace
sorted source assertion_ids
```

Relationship identity must be deterministic under fixed inputs and policy.

Relationship identity must not depend on:

```text
filesystem traversal order
database incidental row-return order
Python object iteration order
non-stable temporary row numbers
report rendering order
```

If a stable topology relationship identity cannot be produced, the relationship must fail validation or be emitted with an explicit unresolved identity status according to the declared validation policy.

---

# Required Topology Relationship Components

Every topology relationship must preserve:

```text
topology_relationship_id
topology_build_id
topology_dimension
relationship_kind
derivation_basis
source_assertion_ids
relationship_members
basis_components
input_corpus_generation_id
registration_unit_ids when applicable
validation_status
```

A topology relationship may also preserve:

```text
relationship_label
relationship_scope
relationship_cardinality
relationship_summary
source_identity_references
namespace_event_references
overlay_attachment_references
discovery_event_references
provenance_references
temporal_context
independence_context
```

A topology relationship without a declared derivation basis is not compliant.

A topology relationship without reconstructable source Assertion Record lineage is not compliant unless it is explicitly declared as a corpus-level or registration-metadata topology relationship.

---

# Relationship Member Requirements

Topology relationships may include one or more relationship members.

Relationship members may represent:

```text
Assertion Records
participants
source identities
source artifacts
registration units
producer families
evidence domains
contexts
provenance sources
namespace events
overlay attachments
discovery events
external authorities
```

Relationship member records should preserve:

```text
topology_relationship_id
member_id or member reference
member_type
member_role
source_assertion_id when applicable
source_registration_unit_id when applicable
source_corpus_generation_id
basis_component_reference when applicable
validation_status
```

Relationship membership must be explicit.

Relationship membership must not imply biological importance.

Relationship membership must not replace Assertion Record lineage.

---

# Basis Component Requirements

Basis components explain why a topology relationship exists.

Basis components may include:

```text
participant role/value pairs
source identity references
namespace bridge references
artifact references
assertion field references
context references
provenance references
overlay attachment references
discovery event references
external evidence capsule references
temporal references
independence references
```

Basis component records should preserve:

```text
topology_relationship_id
basis_component_id
basis_component_type
basis_component_value or reference
basis_component_namespace when applicable
source_assertion_id when applicable
source_registration_unit_id when applicable
source_corpus_generation_id
resolution_status when applicable
ambiguity_status when applicable
conflict_status when applicable
lossiness_status when applicable
validation_status
```

Basis components must be sufficient to reconstruct the derivation of the topology relationship.

If a basis component is unavailable, unresolved, ambiguous, conflicted, or lossy, that state must be explicit.

A topology relationship with hidden or non-reconstructable basis components is not compliant.

---

# Derivation Basis Requirements

Every topology relationship must declare why it exists.

Allowed derivation bases may include:

```text
shared source identity
shared participant role
shared participant value
shared canonical identity through namespace bridge
shared assertion type
shared relationship type
shared phenotype context
shared sample context
shared gene participant
shared variant participant
shared transcript participant
shared condition context
shared producer family
shared evidence domain
cross-producer participant intersection
cross-modality participant intersection
shared provenance source
shared independence group
shared temporal generation
epistemic contrast
uncertainty contrast
registered overlay attachment
registered discovery event
external authority attachment
```

The derivation basis must be reconstructable from governed VDB records.

The derivation basis must distinguish source identity matches from namespace-mediated matches.

The derivation basis must distinguish direct producer evidence from derived VDB organization.

The derivation basis must not be replaced by an opaque connectedness score.

---

# Namespace-Mediated Topology Requirements

Evidence Topology may derive relationships through namespace governance.

Namespace-mediated topology must preserve:

```text
source identity references
source namespaces
canonical identity references when available
namespace event references
identity bridge references when available
resolution status
ambiguity status when available
conflict status when available
resolution provenance
```

Topology must distinguish:

```text
source identity match
source namespace match
canonical identity match
namespace-mediated match
ambiguous namespace match
conflicted namespace match
unresolved namespace state
```

A namespace-mediated relationship must not silently masquerade as a direct source identity match.

Canonical identity attachment must not replace source identity lineage.

Namespace uncertainty must remain visible to downstream topology, geometry, surface, and projection layers.

For the initial MARK topology build, namespace-mediated relationships should be conservative.

When namespace metadata is insufficient to support a mediated relationship, the topology record should either:

```text
preserve the unresolved namespace state
```

or:

```text
defer the relationship under the declared policy
```

The builder must not invent namespace resolution.

---

# Metadata-Level Topology Relationship Requirements

Evidence Topology may construct metadata-level topology relationships when explicitly declared by policy.

Metadata-level topology relationships may include:

```text
registration_metadata_membership
corpus_metadata_membership
producer_family_membership
evidence_domain_membership
validation_status_membership
certification_status_membership
```

Metadata-level relationships are allowed only when:

```text
the topology derivation policy explicitly enables them
their metadata basis is declared
their relationship members are explicit
their basis components are reconstructable
they preserve Corpus Generation lineage
they preserve Registration Unit lineage when applicable
they do not masquerade as biological evidence relationships
```

A metadata-level topology relationship without source Assertion Record lineage must be explicitly declared as corpus-level or registration-metadata topology.

Metadata-level topology must not imply biological relatedness.

Metadata-level topology must not become source evidence.

---

# Discovery And Overlay Topology Requirements

Evidence Topology may consume registered Discovery Events or Overlay Attachments only when those records are governed VDB records and preserve derivation provenance.

For the initial MARK topology build, discovery-derived and overlay-derived topology should be considered:

```text
contract-supported
implementation-deferred unless governed Discovery Events or Overlay Attachments exist
```

If discovery or overlay records are used, topology must preserve:

```text
discovery event references when applicable
overlay attachment references when applicable
attachment basis
attachment policy
attachment provenance
attachment uncertainty
source Assertion Record references
source Registration Unit references
source Corpus Generation reference
```

Discovery Events and Overlay Attachments must not silently enrich producer evidence.

Topology derived from discovery or overlay records must not fuse evidence strata.

Topology derived from discovery or overlay records must not create biological conclusions.

---

# Summary And Inventory Requirements

Evidence Topology may emit summaries and inventories.

Allowed topology summaries include:

```text
number of topology relationships
number of topology dimensions represented
number of Assertion Records participating
number of Registration Units represented
number of producer families represented
number of evidence domains represented
number of namespace-mediated relationships
number of unresolved or ambiguous relationships
number of relationships by derivation basis
```

Topology summaries must remain traceable to topology relationships and source Assertion Records.

Summaries must not replace topology relationship records.

Summaries must not replace Assertion Records.

Summaries must not imply biological importance unless explicitly produced by a downstream reasoning system and re-entered as a new preserved assertion.

The implementation should emit summary records only as inspection aids and validation aids.

---

# Validation Strategy

Evidence Topology validation should operate in four tiers.

## Tier 1: Input Validation

Input validation confirms that governed upstream sources are available.

Validation must check:

```text
input Corpus Generation exists
input_corpus_generation_id is declared
input Assertion Record source exists
input_assertion_record_index_id is declared when available
downstream topology input manifest exists
topology derivation policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
```

Validation must also confirm:

```text
Evidence Topology does not directly parse raw producer artifacts
Evidence Topology does not re-run ingestion
Evidence Topology does not reconstruct Registration Units
Evidence Topology does not bypass Assertion Record primacy
```

## Tier 2: Relationship Validation

Relationship validation confirms that each topology relationship satisfies required topology obligations.

Validation must check:

```text
topology_relationship_id exists
topology_build_id exists
topology_dimension is declared
relationship_kind is declared
derivation_basis is declared
relationship members are explicit
basis components are explicit
source Assertion Record lineage is reconstructable
source Corpus Generation lineage is reconstructable
source Registration Unit lineage is reconstructable when applicable
relationship identity is deterministic
relationship member ordering is deterministic
basis component ordering is deterministic
```

## Tier 3: Namespace, Metadata, Discovery, And Overlay Validation

Namespace validation must check:

```text
namespace-mediated relationships preserve namespace provenance
source identity matches are distinguishable from namespace-mediated matches
ambiguous namespace relationships are marked ambiguous
conflicted namespace relationships are marked conflicted
unresolved namespace states remain visible
canonical identity attachment does not replace source identity lineage
```

Metadata-level topology validation must check:

```text
metadata-level relationships are explicitly policy-enabled
metadata-level relationships preserve their metadata basis
metadata-level relationships do not masquerade as biological evidence relationships
metadata-level relationships preserve Corpus Generation lineage
metadata-level relationships preserve Registration Unit lineage when applicable
```

Discovery and overlay validation must check, when applicable:

```text
discovery-derived relationships preserve discovery provenance
overlay-derived relationships preserve overlay provenance
attachment basis is declared
attachment policy is declared
attachment uncertainty is visible
source Assertion Record references are preserved when applicable
```

## Tier 4: Anti-Collapse Validation

Anti-collapse validation confirms that Evidence Topology construction did not exceed its layer authority.

Validation must check:

```text
topology does not modify Assertion Records
topology does not mutate Registration Units
topology does not expand Corpus Generation scope silently
topology does not become source evidence
topology does not replace Assertion Records
topology does not embed Convergence Geometry features
topology does not declare surface eligibility
topology does not determine surface disclosure
topology does not emit replacement projections
topology does not perform biological reasoning
graph representation is not treated as topology itself
network representation is not treated as topology itself
opaque connectedness scores do not replace derivation basis
```

Validation must confirm organization and reconstructability.

Validation must not claim biological correctness.

---

# Determinism Requirements

Evidence Topology outputs must be deterministic under fixed inputs.

Given the same:

```text
Corpus Generation manifest
Assertion Record index
downstream topology input manifest
topology derivation policy
namespace mediation policy when applicable
contract version
builder version
Assertion Record contents
```

the builder should produce equivalent:

```text
topology_build_id
topology_relationship_ids
relationship member records
basis component records
namespace mediation records
metadata-level relationship records when applicable
summary records
validation outcomes
report sections
downstream geometry input manifest
```

Determinism requirements include:

```text
stable topology_build_id generation
stable topology_relationship_id generation
stable derivation policy behavior
stable namespace mediation behavior
stable unresolved-state vocabulary
stable relationship kind vocabulary
stable validation status vocabulary
stable relationship member ordering
stable basis component ordering
stable source Assertion Record ordering
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define topology relationship order.

Filesystem traversal order must not define topology derivation order.

All source Assertion Record lists used in relationship identity generation should be sorted by stable `assertion_id`.

---

# Reconstruction Requirements

Evidence Topology artifacts must support reconstruction of:

```text
which Corpus Generation bounded the topology
which Assertion Record index was used
which Assertion Records were connected
which topology derivation policy was applied
which topology dimensions were enabled
which relationship kinds were produced
which derivation basis supported each relationship
which relationship members participated
which basis components justified each relationship
which namespace states applied
which Registration Units contributed lineage when applicable
which producer families were represented
which evidence domains were represented
which unresolved or ambiguous states were preserved
which validation checks were applied
which builder produced the topology
which downstream geometry input manifest was emitted
```

Topology reconstruction must preserve enough information for downstream Convergence Geometry, Evidence Convergence Surfaces, Projection Views, RDGP-facing projections, and future reinterpretation.

---

# Relationship To Assertion Records

Assertion Records are the primary inputs to Evidence Topology.

The responsibility boundary is:

```text
Assertion Record
    preserves what a producer claimed among participants

Evidence Topology
    derives how preserved claims are connected within a corpus
```

Evidence Topology must preserve traceability to source Assertion Records.

Evidence Topology must not modify Assertion Records.

Evidence Topology must not replace Assertion Records.

Evidence Topology must not treat topological connectedness as producer evidence.

---

# Relationship To Corpus Generation

Corpus Generations provide the declared evidence scope for Evidence Topology derivation.

Every Evidence Topology Build must preserve:

```text
input_corpus_generation_id
input_corpus_generation_label when available
corpus selection policy reference when available
input Registration Unit references when applicable
```

Evidence Topology must not expand Corpus Generation scope silently.

Evidence Topology must not include Assertion Records outside the declared Corpus Generation unless a new Corpus Generation or explicitly versioned input scope is declared.

Evidence Topology must preserve Corpus Generation lineage for downstream geometry, surface, projection, and reconstruction.

---

# Relationship To Registration Units

Evidence Topology must preserve Registration Unit lineage through source Assertion Records.

Topology relationships should preserve Registration Unit references when relevant to reconstruction, validation, or downstream lineage.

Evidence Topology must not mutate Registration Units.

Evidence Topology must not merge Registration Unit boundaries.

Evidence Topology must not treat a Registration Unit as a topology relationship unless explicitly constructing a metadata-level relationship with declared basis.

---

# Relationship To Convergence Geometry

Evidence Topology is the direct input to Convergence Geometry.

The responsibility boundary is:

```text
Evidence Topology
    answers what is connected

Convergence Geometry
    answers what structural properties emerge from those connections
```

Evidence Topology may define relationships, neighborhoods, intersections, and organizational structures.

Convergence Geometry may characterize those structures.

Evidence Topology must not characterize the following as topology records:

```text
convergence density
convergence breadth
convergence depth
producer diversity
modality diversity
evidence-domain diversity
epistemic diversity
temporal persistence
structural motifs
region richness
surface eligibility
```

If an implementation computes such structural characterizations, those outputs are governed by the Convergence Geometry contract.

Topology relationships must remain distinguishable from geometry features.

---

# Relationship To Evidence Convergence Surfaces

Evidence Topology does not expose Evidence Convergence Surfaces.

Evidence Convergence Surfaces are governed exposure objects over Convergence Geometry.

Surface construction must preserve topology lineage.

A surface may expose topology-derived structure through geometry.

A surface must not replace topology relationships.

A surface must not acquire topology authority.

Evidence Topology must not declare:

```text
surface eligibility
surface disclosure
surface withholding
consumer-facing exposure
RDGP-facing projection readiness
```

Those responsibilities belong downstream.

---

# Relationship To Projection Views

Evidence Topology may be inspected, summarized, exported, or rendered through Projection Views.

Graph, network, matrix, table, report, dashboard, hypergraph, or future mathematical outputs are Projection Views when emitted from Evidence Topology.

A Projection View over Evidence Topology must declare:

```text
projection purpose
projection source layer
source topology_build_id
source topology_relationship_ids when applicable
source Assertion Record identities
source Corpus Generation identity
source Registration Unit identities when applicable
materialization status
lossiness status when applicable
reconstruction path
```

A Projection View over Evidence Topology does not replace Evidence Topology.

A Projection View does not acquire topology authority.

A graph projection must not be treated as the topology itself.

---

# Relationship To RDGP Consumer Projections

RDGP-facing consumer projections may include topology-derived structure directly or indirectly through Convergence Geometry and Evidence Convergence Surfaces.

Evidence Topology must preserve enough lineage so downstream projections can later expose:

```text
which Assertion Records were connected
which Corpus Generation bounded the topology
which Registration Units contributed evidence
which topology dimensions were used
which derivation bases supported relationships
which namespace bridges or unresolved namespace states were involved
which producer families, modalities, and evidence domains were represented when available
which evidence strata were connected or absent
```

Evidence Topology does not perform RDGP reasoning.

Evidence Topology does not determine whether connected evidence explains phenotype.

Evidence Topology only organizes preserved claims for downstream derivation and projection.

---

# Relationship To Downstream Derived Layers

Evidence Topology provides the organizational substrate for:

```text
Convergence Geometry
Evidence Convergence Surfaces
Projection Views
RDGP-facing consumer projections
future downstream reasoning
```

Downstream derived layers must preserve topology lineage.

The following must not occur inside Evidence Topology implementation:

```text
Convergence Geometry feature construction
Evidence Convergence Surface eligibility declaration
Evidence Convergence Surface disclosure decision
Projection View generation that replaces Evidence Topology
RDGP reasoning
biological interpretation
cross-producer convergence interpretation
clinical actionability assignment
causality assignment
```

---

# Anti-Collapse Safeguards

Implementation must prevent:

```text
Assertion Record replaced by topology relationship
source identity collapse
source namespace collapse
producer identity collapse
producer-family collapse
evidence-domain collapse
participant collapse
relationship basis collapse
derivation basis collapse
basis component collapse
namespace-mediated relationship treated as direct source identity match
ambiguous namespace relationship treated as resolved
conflicted namespace relationship treated as resolved
Corpus Generation scope collapse
Registration Unit boundary collapse
topology relationship without derivation basis
topology relationship without reconstructable lineage
topology treated as source evidence
topology treated as biological truth
topology treated as clinical evidence
topology deriving geometry features prematurely
topology declaring surface eligibility
topology performing biological reasoning
graph representation treated as topology itself
network representation treated as topology itself
projection row replacing topology relationship
opaque connectedness score replacing topology basis
cross-producer convergence interpreted as biological meaning
```

Any implementation that performs one of these actions violates this plan and the Evidence Topology contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Assertion Record indexes before running against the MARK corpus.

Recommended tests include:

```text
test_evidence_topology_requires_corpus_generation
test_evidence_topology_requires_assertion_record_source
test_evidence_topology_requires_derivation_policy
test_evidence_topology_preserves_topology_build_id
test_evidence_topology_preserves_input_corpus_generation_id
test_evidence_topology_preserves_input_assertion_record_index_id
test_evidence_topology_relationship_requires_dimension
test_evidence_topology_relationship_requires_kind
test_evidence_topology_relationship_requires_derivation_basis
test_evidence_topology_relationship_requires_members
test_evidence_topology_relationship_requires_basis_components
test_evidence_topology_relationship_traces_to_assertion_records
test_evidence_topology_relationship_traces_to_corpus_generation
test_evidence_topology_relationship_traces_to_registration_units_when_applicable
test_evidence_topology_distinguishes_direct_identity_match_from_namespace_mediated_match
test_evidence_topology_preserves_ambiguous_namespace_status
test_evidence_topology_preserves_conflicted_namespace_status
test_evidence_topology_preserves_unresolved_namespace_status
test_evidence_topology_metadata_relationships_are_policy_enabled
test_evidence_topology_does_not_modify_assertion_records
test_evidence_topology_does_not_mutate_registration_units
test_evidence_topology_does_not_expand_corpus_scope
test_evidence_topology_does_not_create_geometry_features
test_evidence_topology_does_not_declare_surface_eligibility
test_evidence_topology_does_not_perform_biological_reasoning
test_evidence_topology_outputs_are_deterministic
test_downstream_geometry_input_manifest_is_emitted
```

MARK integration tests should confirm:

```text
mark_phase4_corpus_6tep_v1 Assertion Record index is accepted as input
topology build identity is stable
participant relationships are derived when policy-enabled
context relationships are derived when policy-enabled
relationship-class relationships are derived when policy-enabled
producer-family relationships are derived when policy-enabled
evidence-domain relationships are derived when policy-enabled
namespace-mediated relationships are preserved or deferred under policy
metadata-level relationships are emitted only when policy-enabled
all topology relationships preserve source Assertion Record lineage
topology validation report is deterministic
downstream geometry input manifest is deterministic
```

Tests must not require biological correctness.

Tests validate organization, reconstructability, determinism, namespace-state preservation, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define Evidence Topology derivation policy.

2. Define enabled initial topology dimensions.

3. Define enabled initial relationship kinds.

4. Define namespace mediation behavior.

5. Define metadata-level topology behavior.

6. Load Corpus Generation manifest.

7. Load Assertion Record index.

8. Load downstream topology input manifest.

9. Validate governed input boundary.

10. Generate Topology Build identity.

11. Derive policy-enabled participant relationships.

12. Derive policy-enabled context relationships.

13. Derive policy-enabled relationship-class relationships.

14. Derive policy-enabled producer-family relationships.

15. Derive policy-enabled evidence-domain relationships.

16. Derive policy-enabled namespace-mediated relationships when supported.

17. Derive policy-enabled metadata-level relationships when supported.

18. Construct relationship member records.

19. Construct basis component records.

20. Construct namespace mediation records.

21. Validate topology relationships.

22. Emit topology build manifest.

23. Emit topology relationship artifacts.

24. Emit topology validation report.

25. Emit topology build report.

26. Emit downstream geometry input manifest.

27. Add synthetic tests.

28. Add MARK corpus smoke test.

29. Hand off topology build to Convergence Geometry implementation.
```

Each step must preserve Assertion Record lineage.

Each step must preserve Corpus Generation lineage.

Each step must remain non-mutating with respect to Registration Units and Assertion Records.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_evidence_topology.py \
  --assertion-record-index results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_index.tsv \
  --topology-input-manifest results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/downstream_topology_input_manifest.tsv \
  --corpus-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/corpus_generation_manifest.tsv \
  --output-dir results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1 \
  --topology-build-id mark_phase4_corpus_6tep_v1_topology_build_v1 \
  --topology-derivation-policy-id mark_phase4_vap_gsc_topology_derivation_policy_v1
```

or:

```bash
python scripts/phase4/validate_evidence_topology.py \
  --topology-build-manifest results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_build_manifest.tsv \
  --topology-relationships results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_relationships.tsv \
  --output-dir results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1
```

The exact script names are not contractually fixed.

The CLI must make Corpus Generation identity, Assertion Record input, topology derivation policy, and output location explicit.

---

# Expected Input Manifest Shape

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

This manifest is produced by Assertion Record implementation.

It is not Evidence Topology.

It must be validated against the Assertion Record index before topology derivation begins.

---

# Expected Topology Build Manifest Shape

A topology build manifest may include:

```text
topology_build_id
topology_build_label
input_corpus_generation_id
input_assertion_record_index_id
topology_derivation_policy_id
topology_derivation_policy_version
builder_name
builder_version
build_timestamp
validation_status
certification_status
contract_version
schema_version
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Expected Topology Relationship Shape

A topology relationship table may include:

```text
topology_relationship_id
topology_build_id
topology_dimension
relationship_kind
derivation_basis
source_assertion_id_summary
relationship_member_summary
basis_component_summary
input_corpus_generation_id
registration_unit_id_summary
namespace_mediation_status
validation_status
```

This table is a topology relationship index.

It is not a graph projection.

It is not geometry.

It is not source evidence.

---

# Expected Relationship Member Shape

A relationship member table may include:

```text
topology_relationship_id
member_id
member_type
member_role
member_reference
source_assertion_id
source_registration_unit_id
source_corpus_generation_id
basis_component_reference
validation_status
```

Relationship members may be one-to-many relative to topology relationships.

Relationship members must remain explicit and reconstructable.

---

# Expected Basis Component Shape

A basis component table may include:

```text
topology_relationship_id
basis_component_id
basis_component_type
basis_component_value
basis_component_reference
basis_component_namespace
source_assertion_id
source_registration_unit_id
source_corpus_generation_id
resolution_status
ambiguity_status
conflict_status
lossiness_status
validation_status
```

Basis components may be one-to-many relative to topology relationships.

Basis components must explain why the topology relationship exists.

---

# Expected Namespace Mediation Shape

A namespace mediation table may include:

```text
topology_relationship_id
source_identity_reference
source_namespace
canonical_identity_reference
namespace_event_reference
identity_bridge_reference
match_type
resolution_status
ambiguity_status
conflict_status
resolution_provenance
validation_status
```

The `match_type` field should distinguish:

```text
source_identity_match
source_namespace_match
canonical_identity_match
namespace_mediated_match
ambiguous_namespace_match
conflicted_namespace_match
unresolved_namespace_state
```

Namespace mediation records must preserve source identity lineage.

---

# Expected Downstream Geometry Input Manifest Shape

A downstream geometry input manifest may include:

```text
topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
topology_relationship_id
topology_dimension
relationship_kind
derivation_basis
source_assertion_id_summary
relationship_member_summary
basis_component_summary
namespace_mediation_status when applicable
validation_status
```

This manifest exists to make Convergence Geometry derivation deterministic.

It must not contain geometry features.

It must not characterize structural properties.

---

# Exit Criteria

The Evidence Topology implementation plan is complete when:

```text
Topology Build identity is stable
input Corpus Generation is declared
input Assertion Record source is declared
topology derivation policy is declared
builder identity is declared
topology relationships are created deterministically
topology relationships declare dimensions
topology relationships declare relationship kinds
topology relationships declare derivation basis
topology relationships preserve relationship members
topology relationships preserve basis components
topology relationships trace to Assertion Records
topology relationships trace to Corpus Generation
topology relationships trace to Registration Units when applicable
namespace-mediated relationships preserve namespace provenance
metadata-level topology relationships are policy-enabled when emitted
discovery-derived relationships preserve discovery provenance when applicable
overlay-derived relationships preserve overlay provenance when applicable
topology summaries remain traceable to topology relationships
machine-readable topology artifacts are emitted
human-readable topology build report is emitted
topology validation report is emitted
downstream geometry input manifest is emitted
outputs are deterministic under fixed inputs
topology can serve as input to Convergence Geometry
topology does not become source evidence
topology does not perform biological reasoning
topology remains representation-neutral
anti-collapse safeguards pass
```

This implementation is not complete merely because a graph, table, matrix, index, or file exists.

It is complete only when those records satisfy the Evidence Topology contract and can safely serve as the organized substrate for Convergence Geometry.

---

# Summary

The Evidence Topology implementation plan establishes the first derived organization layer in VDB Phase 4.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.
```

The guiding rule is:

```text
Consume preserved Assertion Records.

Declare the topology policy.

Derive relationships.

Declare dimensions.

Declare basis.

Preserve members.

Preserve lineage.

Preserve namespace state.

Avoid representation lock-in.

Do not characterize.

Do not expose.

Do not project.

Do not interpret.
```

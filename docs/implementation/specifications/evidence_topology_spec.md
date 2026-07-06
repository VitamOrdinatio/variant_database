# Evidence Topology Specification

## Epoch II: Evidence Geometry

| Epoch | Epoch Identity        | Epoch Purpose                                                                                       |
| ----- | --------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer           | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | **Evidence Geometry** | **Once assertions exist, how do preserved claims organize into derived evidence structure?**         |
| III   | Discovery Layer       | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer      | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer       | Why do we do this?                                                                                  |

---

## Relationship To Design, Contract, Plan, And Schema

This specification formalizes implementation requirements established by:

```text
docs/design/evidence_topology_model.md
docs/contracts/evidence_topology/evidence_topology_contract.md
docs/plans/evidence_topology/evidence_topology_plan.md
docs/implementation/schemas/evidence_topology_schema.md
```

The design document defines the conceptual model.

The contract defines the non-negotiable obligations.

The implementation plan defines the execution sequence.

The schema defines the structural representation.

This specification defines the requirements that every valid Evidence Topology implementation must satisfy.

If this specification conflicts with the Evidence Topology contract or the VDB System Contract, the contracts take precedence.

---

# Purpose

Evidence Topology provides the first deterministic organizational layer above preserved Assertion Records.

Its purpose is to organize preserved scientific claims without introducing biological interpretation, statistical inference, clinical interpretation, or source-authority transfer.

Evidence Topology is a derived implementation artifact.

Evidence Topology is never source evidence.

Evidence Topology is never a biological conclusion.

Evidence Topology is never an RDGP reasoning result.

For Phase 4.4, Evidence Topology must also preserve explicit handles to large Source Identity Set substrates when downstream discovery, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, TEP-VDB export, or RDGP-facing analysis may require controlled expansion.

The governing purpose is:

```text
Consume preserved Assertion Records.
Derive relationship organization.
Declare dimensions, kinds, and basis.
Preserve relationship members.
Preserve basis components.
Preserve lineage.
Make source identity expansion addressable.
Do not flatten evidence.
Do not hide evidence.
Do not interpret evidence.
```

---

# Governing Requirement

A valid Evidence Topology implementation must produce deterministic, reconstructable, traceable, non-authoritative organizational relationships derived from governed Assertion Record surfaces.

A valid Evidence Topology implementation must also distinguish:

```text
claim-level topology
source-identity expansion handles
namespace-mediated topology
deferred statistical analysis
```

This distinction is required because a compact Assertion Record surface may preserve a small number of claim records while retaining references to a much larger source-identity universe.

For the canonical Phase 4.3 substrate:

```text
52 Assertion Records preserve the claim-level spine.
147,941,196 source identities remain represented through governed Source Identity Set references.
```

Evidence Topology may organize the 52 Assertion Records.

Evidence Topology must not pretend that the 52 Assertion Records alone are an analysis-ready statistical burden matrix.

Evidence Topology must preserve reconstructable handles to the Source Identity Set universe when downstream work requires granular expansion.

---

# Scope

This specification governs:

```text
topology construction
topology build identity
topology derivation policy
topology relationships
topology relationship members
topology basis components
topology namespace mediation
topology metadata relationships
source identity expansion handles
topology summaries
topology reconstruction
topology validation
downstream Convergence Geometry input manifests
```

This specification does not govern:

```text
Registration Unit construction
Corpus Generation selection
Assertion Record construction
raw producer artifact parsing
producer TEP parsing
Convergence Geometry feature derivation
Evidence Convergence Surface construction
Projection View generation
TEP-VDB package emission
RDGP reasoning
biological interpretation
statistical inference
case-control enrichment testing
poly-noncoding burden testing
clinical interpretation
causal interpretation
mechanistic explanation
candidate prioritization
```

Those responsibilities belong to upstream preservation layers, downstream derived layers, projection layers, external analysis workflows, or downstream reasoning systems.

---

# Required Input Boundary

Evidence Topology must consume governed VDB sources.

The normal Phase 4 input chain is:

```text
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology Build
```

Evidence Topology must not directly parse raw producer artifacts when Assertion Records are available.

Evidence Topology must not re-run ingestion.

Evidence Topology must not reconstruct Registration Units.

Evidence Topology must not bypass Assertion Record primacy.

For the initial Phase 4.4 build, the governed upstream Assertion Record surface is:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

The canonical topology handoff artifact is:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/downstream_topology_input_manifest.tsv
```

A valid Phase 4.4 implementation may consume the following Assertion Record artifacts when present:

```text
assertion_record_index.tsv
assertion_record_index.jsonl
assertion_record_participants.tsv
assertion_record_source_identity_sets.tsv
assertion_record_source_identity_summary.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
assertion_record_relationships.tsv
assertion_record_evidence_basis.tsv
assertion_record_context.tsv
assertion_record_validation_report.tsv
assertion_record_validation_report.json
downstream_topology_input_manifest.tsv
```

These artifacts are the governed Assertion Record surface.

They are not raw producer artifacts.

They are not Registration Units.

They are not Evidence Topology.

Evidence Topology may preserve and expose Source Identity Set references emitted by the Assertion Record layer.

Evidence Topology must not flatten large Source Identity Sets into topology relationship records.

Evidence Topology must not hide Source Identity Sets behind opaque claim-level summaries.

If a topology implementation requires granular source identity values, it must use a declared controlled expansion policy and preserve Assertion Record primacy.

---

# Initial Phase 4.4 Corpus Target

The initial canonical topology build targets the corpus generation:

```text
mark_phase4_corpus_6tep_v1
```

The recommended initial topology build identifier is:

```text
mark_phase4_corpus_6tep_v1_topology_build_v1
```

The recommended initial topology derivation policy identifier is:

```text
mark_phase4_vap_gsc_topology_derivation_policy_v1
```

The recommended output location is:

```text
results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
```

This initial topology build is not Convergence Geometry.

This initial topology build is not an Evidence Convergence Surface.

This initial topology build is not a Projection View.

This initial topology build is not a TEP-VDB export.

This initial topology build is not RDGP reasoning.

---

# Topology Build Identity Requirements

Every Evidence Topology Build must have stable build identity.

A Topology Build must preserve:

```text
topology_build_id
topology_build_label when available
input_corpus_generation_id
input_assertion_record_index_id or equivalent governed Assertion Record source identifier
input_topology_manifest_path or equivalent handoff identifier
topology_derivation_policy_id
topology_derivation_policy_version when available
builder_name
builder_version when available
build_timestamp_utc
contract_version when available
schema_version when available
validation_status
certification_status when available
```

Topology Build identity must be stable across:

```text
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
TEP-VDB export
validation
certification
reconstruction
future reinterpretation
```

Human-readable labels may support inspection.

Labels must not replace stable Topology Build identity.

A topology build without stable identity is invalid.

---

# Topology Derivation Policy Requirements

Every Evidence Topology Build must declare a topology derivation policy.

The topology derivation policy must define:

```text
input Assertion Record source
input Corpus Generation identity
eligible Assertion Record types
eligible participant roles
eligible source identity set kinds
eligible source namespaces when applicable
eligible relationship classes
eligible context fields
enabled topology dimensions
enabled relationship kinds
enabled derivation bases
namespace mediation behavior
source identity expansion behavior
metadata-level topology behavior
discovery and overlay behavior when applicable
unsupported relationship behavior
unresolved-state behavior
ambiguity behavior
conflict behavior
lossiness behavior
statistical-testing readiness semantics
validation behavior
```

The policy must not define biological meaning.

The policy must not define statistical significance.

The policy must not define Convergence Geometry features.

The policy must not define Evidence Convergence Surface eligibility.

The policy must not define Projection View field selection.

The policy must not define RDGP reasoning behavior.

A topology relationship emitted without policy support is invalid.

## Schema And Policy Vocabulary Alignment

Every value emitted by an Evidence Topology implementation must be recognized by the Evidence Topology schema or explicitly declared as a policy-local extension.

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

Policy-local extensions must not contradict the Evidence Topology contract, the VDB System Contract, or existing schema vocabulary.

The initial Phase 4.4 policy:

```text
mark_phase4_vap_gsc_topology_derivation_policy_v1
```

must emit only schema-recognized values unless a policy-local extension is explicitly documented.

---

# Topology Relationship Requirements

Every Evidence Topology relationship must preserve:

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
namespace_mediation_status when applicable
source_identity_expansion_status when applicable
statistical_testing_status when applicable
validation_status
```

The following concepts are distinct and must not be collapsed:

```text
topology_dimension
relationship_kind
derivation_basis
```

`topology_dimension` identifies the organizational axis.

`relationship_kind` identifies the type of topology relationship.

`derivation_basis` identifies why the relationship exists.

Example:

```text
topology_dimension: producer
relationship_kind: producer_family_membership
derivation_basis: shared producer_family value
```

Example:

```text
topology_dimension: participant
relationship_kind: source_identity_set_role_namespace_membership
derivation_basis: shared source identity set role/kind/namespace
```

A topology relationship without a declared dimension is invalid.

A topology relationship without a declared relationship kind is invalid.

A topology relationship without a declared derivation basis is invalid.

A topology relationship without reconstructable source lineage is invalid unless it is explicitly declared as a corpus-level or metadata-level topology relationship under policy.

## Validation Status Scope

Within Evidence Topology outputs, `validation_status` means topology-layer validation status unless a field explicitly names an upstream source status.

When preserving upstream Assertion Record states, topology artifacts should use explicit summary fields such as:

```text
source_assertion_validation_status_summary
source_assertion_resolver_status_summary
source_assertion_preservation_status_summary
```

Topology-layer validation status values must not be confused with upstream Assertion Record preservation or resolver states such as:

```text
preserved
supported
indexed_with_note
deferred
```

---

# Topology Dimension Requirements

Every topology relationship must declare exactly one primary topology dimension.

Initial allowed dimensions include:

```text
participant
relationship
context
provenance
epistemic
temporal
independence
producer
evidence_domain
namespace
uncertainty_status
generation
registration_unit
corpus_generation
metadata
source_identity_set
```

Future dimensions may be added under a declared policy.

Topology dimensions are organizational axes.

They are not biological conclusions.

A topology dimension must not silently combine multiple axes unless the derivation policy explicitly declares a composite basis and preserves each contributing component.

---

# Relationship Kind Requirements

Every topology relationship must declare a relationship kind.

Initial Phase 4.4 v1 policy-enabled relationship kinds are:

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

Policy-conditional or future relationship kinds may include:

```text
evidence_domain_membership
shared_context_membership
temporal_generation_membership
independence_group_membership
source_identity_obligation_status_membership
certification_status_membership
```

Expansion-required relationship kinds may include:

```text
exact_source_identity_value_intersection
exact_variant_overlap
exact_gene_overlap
exact_sample_overlap
exact_sample_variant_burden
cross_producer_exact_participant_intersection
cross_evidence_domain_exact_participant_intersection
namespace_mediated_participant_value_match
```

These expansion-required relationship kinds must not be emitted as completed exact topology unless the implementation has a declared expansion policy and sufficient governed source identity substrate.

The following relationship kinds are prohibited at the Evidence Topology layer:

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
poly_noncoding_variant_burden_test
case_control_enrichment
regulatory_feature_burden
pathway_burden
network_level_disease_burden
statistical_significance
biological_risk_score
```

Those concepts belong to Convergence Geometry, Evidence Convergence Surfaces, Projection Views, external statistical analysis, downstream reasoning systems, or returned producer assertions.

---

# Derivation Basis Requirements

Every topology relationship must declare why it exists.

Allowed derivation bases may include schema-recognized values such as:

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

Human-readable descriptions may be used in reports, but machine-readable topology outputs must preserve schema-recognized derivation-basis values or explicitly declared policy-local extensions.

The derivation basis must be reconstructable from governed VDB records.

The derivation basis must distinguish:

```text
source identity set reference
source identity value
source namespace match
canonical identity match
namespace-mediated match
metadata-level relationship
statistical-analysis deferred relationship
```

The derivation basis must not be replaced by an opaque connectedness score.

The derivation basis must not imply biological importance.

---

# Relationship Classification Requirements

Every topology relationship or relationship candidate should be classified by derivation readiness.

Allowed relationship classification values are:

```text
immediately_derived_topology
expansion_required_topology
deferred_statistical_analysis
metadata_level_topology
not_applicable
```

## Immediately Derived Topology

Immediately derived topology may be emitted when the compact Assertion Record surface contains sufficient governed information to reconstruct the relationship.

Examples include:

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

## Expansion-Required Topology

Expansion-required topology must preserve expansion handles and must not claim completed exact-value relationships unless governed expansion has occurred.

Examples include:

```text
exact_source_identity_value_intersection
exact_variant_overlap
exact_gene_overlap
exact_sample_variant_burden
cross_producer_exact_participant_intersection
namespace_mediated_participant_value_match
```

## Deferred Statistical Analysis

Deferred statistical analysis is outside Evidence Topology.

Examples include:

```text
poly_noncoding_variant_burden_test
case_control_enrichment
regulatory_feature_burden
pathway_burden
network_level_disease_burden
statistical_significance
biological_risk_score
```

Evidence Topology may preserve the handles needed by downstream analysis.

Evidence Topology must not perform the analysis.

---

# Relationship Member Requirements

Topology relationships may include one or more relationship members.

Relationship members may represent:

```text
Assertion Records
participants
source identity sets
source identities when governed expansion is enabled
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

Relationship member records must preserve:

```text
topology_relationship_id
member_id or member reference
member_type
member_role
member_reference
source_assertion_id when applicable
source_registration_unit_id when applicable
source_corpus_generation_id
basis_component_reference when applicable
validation_status
```

Relationship membership must be explicit.

Relationship membership must not imply biological importance.

Relationship membership must not replace Assertion Record lineage.

Relationship membership must not flatten Source Identity Sets unless governed expansion is explicitly enabled.

---

# Basis Component Requirements

Basis components explain the evidence or metadata used to derive a topology relationship.

Basis components may include:

```text
participant role/value pairs
source identity set references
source identity references when governed expansion is enabled
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
validation-status references
resolver-status references
```

Basis component records must preserve:

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

If a basis component is unavailable, unresolved, ambiguous, conflicted, deferred, or lossy, that state must be explicit.

A topology relationship with hidden or non-reconstructable basis components is invalid.

---

# Source Identity Set And Expansion Requirements

Evidence Topology must preserve the distinction between:

```text
Assertion Record identity
Source Identity Set identity
individual source identity values
canonical identity values
namespace-mediated identity values
analysis-ready burden substrate
```

Evidence Topology must not flatten large Source Identity Sets into topology relationship records.

Evidence Topology must not hide Source Identity Sets behind opaque claim-level relationships.

Evidence Topology must preserve expansion handles when downstream discovery, geometry, surface construction, projection, TEP-VDB export, or statistical analysis may require granular source identities.

When Source Identity Set references are used, Evidence Topology should preserve:

```text
source_identity_set_id
source_identity_count
source_identity_kind when available
participant_role when available
source_namespace when available
source_assertion_id or source_assertion_registration_id
source_registration_unit_id
source_corpus_generation_id
expansion_status
expansion_policy_id when applicable
expansion_required_for_statistical_testing
recommended_downstream_use
validation_status
```

Allowed source identity expansion status values include:

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

A topology build that references Source Identity Sets must make their expansion status visible.

A topology build that cannot support source identity expansion must state that limitation explicitly.

---

# Namespace Mediation Requirements

Evidence Topology may derive relationships through namespace governance only when the derivation policy enables namespace-mediated topology.

Namespace-mediated topology must preserve:

```text
source identity set references when applicable
source identity references when governed expansion is enabled
source namespaces
canonical identity references when available
namespace event references when available
identity bridge references when available
match type
resolution status
ambiguity status when available
conflict status when available
resolution provenance
validation status
```

Allowed namespace mediation match type values include:

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

A namespace-mediated topology relationship must never masquerade as a direct source identity match.

`source_namespace_only` means that source namespace grouping or preservation is available, but canonical identity resolution has not been performed.

A `source_namespace_only` relationship must not be interpreted as a canonical identity match or namespace-mediated identity match.

Canonical identity attachment must never replace source identity lineage.

Namespace uncertainty must remain visible to downstream topology, geometry, surface, projection, and reasoning layers.

If namespace metadata is insufficient to support a mediated relationship, the implementation must either preserve the unresolved namespace state or defer the relationship under policy.

The builder must not invent namespace resolution.

---

# Metadata-Level Topology Requirements

Evidence Topology may construct metadata-level topology relationships when explicitly enabled by policy.

Metadata-level topology relationships may include v1 policy-enabled values such as:

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
source_identity_resolution_status_membership
source_identity_lossiness_status_membership
```

Policy-conditional or future metadata-level relationships may include:

```text
evidence_domain_membership
temporal_generation_membership
independence_group_membership
source_identity_obligation_status_membership
certification_status_membership
```

Metadata-level relationships are valid only when:

```text
the topology derivation policy explicitly enables them
their metadata basis is declared
their relationship members are explicit
their basis components are reconstructable
they preserve source Assertion Record lineage when derived from Assertion Records
they preserve Corpus Generation lineage
they preserve Registration Unit lineage when applicable
they do not masquerade as biological evidence relationships
they do not become source evidence
```

A metadata-level topology relationship without source Assertion Record lineage must be explicitly declared as corpus-level or registration-metadata topology.

Metadata-level topology must not imply biological relatedness.

Metadata-level topology must not become source evidence.

---

# Statistical Testing And Burden-Readiness Boundary

Evidence Topology is not statistical analysis.

Evidence Topology must not perform:

```text
case-control testing
cohort burden testing
poly-noncoding variant disease-burden testing
regulatory feature burden testing
pathway burden testing
network burden testing
statistical significance assignment
risk scoring
candidate prioritization
```

Evidence Topology may preserve expansion handles and readiness flags that downstream systems can use to determine whether a later projection or analysis workflow may construct an analysis-ready burden substrate.

Topology relationships should preserve `statistical_testing_status` or equivalent semantics when the relationship may be relevant to downstream statistical analysis.

Allowed statistical testing status values include:

```text
not_statistical_input
analysis_ready
requires_source_identity_expansion
requires_external_annotation
requires_case_control_design
deferred_to_projection_layer
not_applicable
```

A topology relationship may be `analysis_ready` only when the emitted topology or associated governed projection contains sufficient sample, variant, feature, cohort, denominator, annotation, missingness, and lineage information for the declared test.

For Phase 4.4 v1, poly-noncoding variant disease-burden testing is expected to require:

```text
source identity expansion
external or upstream regulatory annotation when not already present
case/control or cohort design declaration
missingness and denominator semantics
projection-layer or downstream analysis packaging
```

Evidence Topology may identify where burden-relevant evidence could be expanded.

Evidence Topology must not claim that compact claim-level topology is itself a burden-tested result.

---

# Output Requirements

A valid Evidence Topology implementation should emit machine-readable and human-readable artifacts sufficient for reconstruction, validation, and downstream Convergence Geometry input.

Expected output artifacts include:

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
topology_validation_report.json
topology_validation_report.tsv
topology_build_report.md
downstream_geometry_input_manifest.tsv
```

The `topology_source_identity_expansion_index.tsv` artifact is required when topology records reference Source Identity Sets that may require controlled downstream expansion.

The downstream geometry input manifest must identify topology relationships eligible for downstream Convergence Geometry characterization.

The downstream geometry input manifest must not contain Convergence Geometry features.

The downstream geometry input manifest must not characterize density, breadth, depth, producer diversity, modality diversity, evidence-domain diversity, structural motifs, convergence regions, surface eligibility, biological significance, or statistical significance.

---

# Downstream Geometry Boundary

Evidence Topology provides the organizational substrate consumed by Convergence Geometry.

Evidence Topology answers:

```text
What is connected?
```

Convergence Geometry answers:

```text
What structural properties emerge from those connections?
```

Evidence Topology must not emit:

```text
convergence density
convergence breadth
convergence depth
producer diversity as a geometry feature
modality diversity as a geometry feature
evidence-domain diversity as a geometry feature
epistemic diversity as a geometry feature
temporal persistence as a geometry feature
structural motifs
convergence regions
surface eligibility
surface disclosure
surface withholding
biological significance
statistical significance
```

If an implementation computes such structural characterizations, those outputs are governed by the Convergence Geometry contract, not this specification.

---

# Determinism Requirements

Topology construction must be deterministic under fixed inputs.

Given the same:

```text
Corpus Generation identity
Assertion Record index
Assertion Record participants
Assertion Record Source Identity Set references
Assertion Record lineage
Assertion Record validation report
downstream topology input manifest
topology derivation policy
namespace mediation policy when applicable
source identity expansion policy when applicable
contract version
schema version
builder version
```

VDB must produce equivalent:

```text
topology_build_id
topology_relationship_ids
relationship member records
basis component records
source identity expansion index records
namespace mediation records
metadata-level relationship records
summary records
validation outcomes
build report sections
downstream geometry input manifest records
```

Deterministic identity must not depend on:

```text
filesystem traversal order
SQLite incidental row-return order
Python object iteration order
non-stable temporary row numbers
report rendering order
```

Source Assertion Record lists, relationship members, basis components, and Source Identity Set references used in identity generation must be sorted by stable identifiers.

---

# Reconstruction Requirements

Evidence Topology artifacts must support reconstruction of:

```text
which Corpus Generation bounded the topology
which Assertion Record surface was used
which Assertion Records were connected
which topology derivation policy was applied
which topology dimensions were enabled
which relationship kinds were produced
which derivation basis supported each relationship
which relationship members participated
which basis components justified each relationship
which Source Identity Sets were referenced
which Source Identity Sets require controlled expansion
which namespace states applied
which Registration Units contributed lineage when applicable
which producer families were represented
which evidence domains were represented
which unresolved, ambiguous, conflicted, deferred, or lossy states were preserved
which validation checks were applied
which builder produced the topology
which downstream geometry input manifest was emitted
```

Topology reconstruction must preserve enough information for downstream Convergence Geometry, Evidence Convergence Surfaces, Projection Views, TEP-VDB exports, RDGP-facing projections, future statistical analysis, and future reinterpretation.

---

# Validation Requirements

Evidence Topology validation must confirm organization, reconstructability, determinism, lineage, expansion honesty, namespace-state preservation, and authority-boundary preservation.

Validation must not claim biological correctness.

Validation must not claim statistical significance.

Validation must check:

```text
input Corpus Generation exists or is declared
input_corpus_generation_id is declared
input Assertion Record source exists
input_assertion_record_index_id is declared when available
downstream topology input manifest exists
topology derivation policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
topology_build_id exists
every topology relationship has a stable identity
every topology relationship declares topology_dimension
every topology relationship declares relationship_kind
every topology relationship declares derivation_basis
every topology relationship has explicit relationship members
every topology relationship has explicit basis components
source Assertion Record lineage is reconstructable
source Corpus Generation lineage is reconstructable
source Registration Unit lineage is reconstructable when applicable
Source Identity Set references join to the Assertion Record surface
source identity expansion statuses are explicit when applicable
statistical testing statuses are explicit when applicable
namespace-mediated relationships preserve namespace provenance when applicable
metadata-level relationships are policy-enabled when emitted
downstream_geometry_input_manifest.tsv exists
outputs are deterministic under fixed inputs
Assertion Record inputs are not mutated
Registration Units are not mutated
Corpus Generation scope is not silently expanded
no topology relationship becomes source evidence
no Convergence Geometry features are emitted
no Evidence Convergence Surface eligibility is emitted
no Projection View replaces Evidence Topology
no biological reasoning is performed
```

Validation may be staged as:

```text
Layer 1: synthetic unit and regression tests
Layer 2: repo-local canonical full-corpus smoketest over the real Phase 4.3 Assertion Record surface
Layer 3: optional MARK parity or expansion-dependent validation when controlled source identity expansion requires MARK-local substrate
```

A compressed golden fixture is not required when the canonical Assertion Record output is small, local, and sufficient for the validation target.

Validation evidence must be adequate to support closure of the implementation layer.

---

# Forbidden Behaviors And Anti-Collapse Rules

Evidence Topology implementations must not:

```text
infer biological causality
assign statistical significance
determine clinical relevance
create mechanistic explanations
perform RDGP reasoning
perform poly-noncoding burden testing
modify preserved Assertion Records
rewrite producer evidence
mutate Registration Units
expand Corpus Generation scope silently
remove provenance
collapse Assertion Records into topology relationships
collapse source identities into canonical identities
collapse Source Identity Sets into opaque topology summaries
hide Source Identity Sets behind claim-level topology
collapse producer identity
collapse evidence-domain identity
collapse participant roles
collapse namespace uncertainty
collapse epistemic distinctions
collapse independence distinctions
fabricate organizational relationships lacking derivation basis
treat namespace-mediated matches as direct source identity matches
treat unresolved namespace states as resolved
treat ambiguous namespace states as resolved
treat conflicted namespace states as resolved
treat topology as source evidence
treat topology as biological truth
treat topology as clinical evidence
treat topology as statistical analysis
treat graph representation as topology itself
treat network representation as topology itself
treat projection output as replacement topology
emit Convergence Geometry features inside topology
emit Evidence Convergence Surface eligibility inside topology
emit consumer-facing Projection Views as topology authority
replace derivation basis with an opaque connectedness score
overclaim burden-readiness from compact claim-level topology
```

Any implementation that performs one of these actions violates this specification.

---

# Summary

A valid Evidence Topology implementation is:

```text
assertion-derived
corpus-bounded
policy-declared
deterministic
reconstructable
traceable
relationship-explicit
dimension-explicit
kind-explicit
basis-explicit
member-explicit
source-identity-expansion-aware
namespace-state-preserving
provenance-preserving
epistemically faithful
independence-preserving
higher-order capable
non-authoritative
non-interpretive
```

Evidence Topology exists to organize preserved Assertion Records.

Evidence Topology does not reinterpret them.

For the canonical Phase 4.4 implementation, Evidence Topology must be sufficient to organize the 52 preserved Assertion Records while preserving expansion-addressable handles to the 147,941,196 represented source identities.

This makes future discovery, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, TEP-VDB exports, and RDGP-facing analyses possible without flattening source identities, hiding evidence, or violating Assertion Record primacy.

The guiding rule is:

```text
Preserve the assertions.
Derive the relationships.
Declare the policy.
Declare the dimension.
Declare the kind.
Declare the basis.
Preserve the members.
Preserve the lineage.
Expose expansion handles.
Defer statistics to statistical layers.
Never let topology become evidence.
```

# Convergence Geometry Implementation Plan

## Purpose

This document defines the implementation plan for Convergence Geometry construction in VDB Phase 4.

Convergence Geometry is the deterministic, reconstructable structural characterization of Evidence Topology within a declared Corpus Generation.

This plan describes how VDB will consume a governed Evidence Topology Build, apply an explicit geometry derivation policy, construct bounded Convergence Regions, compute or record Geometry Features, optionally recognize Structural Motifs, preserve method provenance, validate reconstructability, and provide downstream input to Evidence Convergence Surface construction.

The Phase 4 Convergence Geometry implementation goal is:

```text
Deterministically characterize topology-derived evidence regions with
reconstructable structural features while preserving topology lineage,
Assertion Record lineage, Corpus Generation lineage, Registration Unit
lineage, method provenance, and non-interpretive geometry authority.
```

Convergence Geometry characterizes organization.

Convergence Geometry does not interpret organization.

Convergence Geometry builds the structurally rich haystack.

It does not identify the biological needle.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/convergence_geometry/convergence_geometry_contract.md
```

The governing contract states that Convergence Geometry must remain:

```text
topology-derived
corpus-bounded
deterministic
structural
region-explicit
feature-explicit
basis-explicit
method-neutral
representation-neutral
lineage-preserving
non-interpretive
reconstructable
```

This plan is subordinate to the Convergence Geometry contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Convergence Geometry implementation role is to characterize structural properties of topology-derived evidence organization within a declared Corpus Generation.

A Convergence Geometry implementation answers:

```text
What structural properties emerge from the connected evidence organization?
```

It does not answer:

```text
Which evidence is biologically explanatory?

Which gene is causal?

Which variant is pathogenic?

Which candidate should be prioritized?

Which convergence region is clinically actionable?

Which evidence structure represents biological truth?

Which region should be exposed to a downstream consumer?

Which RDGP conclusion should be drawn?
```

Those questions belong to downstream reasoning systems, downstream exposure policies, Projection Views, or returned producer assertions.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Corpus Generation selection
Assertion Record indexing
Evidence Topology derivation
raw producer artifact parsing
producer TEP parsing
Evidence Convergence Surface construction
surface eligibility declaration
surface disclosure decisions
Projection View generation
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
candidate prioritization
cross-producer confidence scoring
```

Convergence Geometry is structural characterization work.

It is not source-evidence work.

It is not topology derivation work.

It is not surface-governance work.

It is not projection work.

It is not biological reasoning work.

---

# Initial Implementation Target

The initial implementation target is the Convergence Geometry build for the first MARK Phase 4 Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

The initial geometry build may be identified as:

```text
mark_phase4_corpus_6tep_v1_geometry_build_v1
```

The expected upstream input is the downstream geometry input manifest emitted by the Evidence Topology implementation, such as:

```text
results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
    downstream_geometry_input_manifest.tsv
```

The initial Convergence Geometry implementation should consume the Evidence Topology Build for the declared Corpus Generation and emit deterministic region and feature artifacts for downstream Evidence Convergence Surface construction.

This Geometry Build is not an Evidence Convergence Surface.

It is the structural characterization substrate from which governed surfaces may later evaluate exposure.

---

# Inputs

The Convergence Geometry implementation consumes:

```text
Corpus Generation manifest
Assertion Record source reference when available
Evidence Topology Build manifest
Evidence Topology relationship artifacts
downstream geometry input manifest
Evidence Topology validation report when available
geometry derivation policy
geometry validation policy
method parameter configuration when applicable
Convergence Geometry contract version
Evidence Topology contract version
Assertion Record contract version
Corpus Generation contract version
system contract version
builder name
builder version
build timestamp
```

Convergence Geometry must consume governed VDB sources.

The normal Phase 4 input chain is:

```text
Corpus Generation
        ↓
Assertion Record index
        ↓
Evidence Topology Build
        ↓
Convergence Geometry Build
```

Convergence Geometry must not directly parse raw producer artifacts when topology-derived inputs are available.

Convergence Geometry must not re-run ingestion.

Convergence Geometry must not reconstruct Registration Units.

Convergence Geometry must not bypass Assertion Record primacy.

Convergence Geometry must not bypass Evidence Topology.

---

# Outputs

The Convergence Geometry implementation should emit deterministic artifacts outside the Evidence Topology Build, Assertion Record index, Corpus Generation manifest, and selected Registration Units.

Expected outputs may include:

```text
geometry_build_manifest.tsv
geometry_build_manifest.json
convergence_regions.tsv
convergence_regions.jsonl
geometry_features.tsv
geometry_features.jsonl
geometry_feature_basis.tsv
structural_motifs.tsv
structural_motifs.jsonl
geometry_method_parameters.tsv
geometry_lineage.tsv
geometry_summary.tsv
geometry_validation_report.json
geometry_validation_report.tsv
geometry_build_report.md
downstream_surface_input_manifest.tsv
```

Structural Motif outputs are optional in the initial implementation unless a declared motif policy exists.

These outputs are Convergence Geometry artifacts.

They do not replace Evidence Topology.

They do not replace Assertion Records.

They do not replace Corpus Generations.

They do not replace Registration Units.

They do not declare surface eligibility.

They do not determine surface disclosure.

They do not create projections.

They do not perform biological reasoning.

---

# Recommended Output Location

Initial Phase 4 Convergence Geometry outputs may be written under:

```text
results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/
```

A recommended initial layout is:

```text
results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/
    geometry_build_manifest.tsv
    geometry_build_manifest.json
    convergence_regions.tsv
    convergence_regions.jsonl
    geometry_features.tsv
    geometry_features.jsonl
    geometry_feature_basis.tsv
    structural_motifs.tsv
    structural_motifs.jsonl
    geometry_method_parameters.tsv
    geometry_lineage.tsv
    geometry_summary.tsv
    geometry_validation_report.json
    geometry_validation_report.tsv
    geometry_build_report.md
    downstream_surface_input_manifest.tsv
```

The output location should be configurable.

Convergence Geometry output paths must not be confused with Evidence Topology source paths, Assertion Record paths, Corpus Generation manifest paths, or Registration Unit source paths.

---

# Required Geometry Build Identity

Every Convergence Geometry Build must have a stable identity.

A Geometry Build identity must preserve:

```text
geometry_build_id
geometry_build_label when available
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id when available
geometry_derivation_policy_id
geometry_derivation_policy_version when available
builder_name
builder_version when available
build_timestamp
validation_status
certification_status when available
```

For the initial MARK geometry build, a recommended identity shape is:

```text
geometry_build_id: mark_phase4_corpus_6tep_v1_geometry_build_v1
geometry_build_label: MARK Phase 4 6-TEP Convergence Geometry Build v1
input_topology_build_id: mark_phase4_corpus_6tep_v1_topology_build_v1
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
geometry_derivation_policy_id: mark_phase4_vap_gsc_geometry_derivation_policy
geometry_derivation_policy_version: v1
```

Geometry Build identity must remain stable across:

```text
Evidence Convergence Surface construction
Projection View generation
validation
certification
reconstruction
```

Human-readable labels may support inspection.

Labels must not replace stable Geometry Build identity.

---

# Geometry Derivation Policy Requirements

Every Convergence Geometry Build must declare a geometry derivation policy.

The geometry derivation policy must define:

```text
input Evidence Topology Build
eligible topology dimensions
eligible topology relationship kinds
eligible derivation bases
enabled Convergence Region kinds
enabled region bounding bases
enabled Geometry Feature kinds
enabled feature derivation bases
Structural Motif policy when applicable
method-specific parameters when applicable
method provenance requirements
lossiness behavior
unsupported topology behavior
validation behavior
```

For the initial MARK geometry build, the policy may be identified as:

```text
mark_phase4_vap_gsc_geometry_derivation_policy_v1
```

The initial policy should focus on conservative structural characterization over the MARK VAP/GSC Evidence Topology Build.

The policy must not define biological meaning.

The policy must not define surface eligibility.

The policy must not define Projection View contents.

The policy must not define RDGP reasoning behavior.

---

# Convergence Region Requirements

A Convergence Region is a bounded topology-derived structure selected for structural characterization.

Every Convergence Region must preserve:

```text
convergence_region_id
geometry_build_id
input_topology_build_id
input_corpus_generation_id
region_label when available
region_kind
region_bounding_basis
source_topology_relationship_ids
source_assertion_ids
registration_unit_ids when applicable
validation_status
```

Convergence Region kinds may include:

```text
participant_centered
phenotype_centered
sample_centered
gene_centered
variant_centered
producer_crossing
modality_crossing
multi_component
temporal
provenance_centered
namespace_mediated
epistemic_contrast
uncertainty_contrast
external_authority_centered
```

Recommended initial region kinds include:

```text
gene_centered
phenotype_centered
sample_centered
variant_centered
producer_crossing
namespace_mediated
uncertainty_contrast
```

A Convergence Region is a structural region.

It is not a biological conclusion.

It is not a prioritization result.

It is not a clinical claim.

It is not a surface.

It is not a projection.

A Convergence Region without a declared bounding basis is not compliant.

---

# Region Bounding Basis Requirements

Every Convergence Region must declare the basis by which it was bounded.

Region bounding basis may include:

```text
participant_centered_neighborhood
phenotype_centered_neighborhood
sample_centered_neighborhood
gene_centered_neighborhood
variant_centered_neighborhood
producer_crossing_intersection
modality_crossing_intersection
multi_component_intersection
temporal_persistence_region
provenance_centered_region
namespace_mediated_region
epistemic_contrast_region
uncertainty_contrast_region
external_authority_region
```

Recommended initial bounding bases include:

```text
gene_centered_neighborhood
phenotype_centered_neighborhood
sample_centered_neighborhood
variant_centered_neighborhood
producer_crossing_intersection
namespace_mediated_region
uncertainty_contrast_region
```

The bounding basis must be reconstructable from Evidence Topology.

The bounding basis must preserve source topology relationship references.

The bounding basis must not be replaced by an opaque region label.

If a region is bounded by composite criteria, each contributing criterion must be declared.

A Convergence Region with hidden, implicit, or non-reconstructable bounds is not compliant.

---

# Convergence Region Identity Strategy

Every Convergence Region must have a stable identity.

A deterministic `convergence_region_id` should be derived from stable components when available, such as:

```text
geometry_build_id
region_kind
region_bounding_basis
source topology relationship identifiers
source Assertion Record identifiers when applicable
region anchor participant or context when applicable
```

For example, a gene-centered region identity may be derived from:

```text
geometry_build_id
region_kind = gene_centered
region_bounding_basis = gene_centered_neighborhood
gene participant namespace
gene participant value
sorted source topology_relationship_ids
sorted source assertion_ids
```

Region identity must be deterministic under fixed inputs and policy.

Region identity must not depend on:

```text
filesystem traversal order
database incidental row-return order
Python object iteration order
non-stable temporary row numbers
report rendering order
```

If a stable Convergence Region identity cannot be produced, the region must fail validation or be emitted with an explicit unresolved identity status according to the declared validation policy.

---

# Geometry Feature Requirements

A Geometry Feature is a structural property computed, recorded, or declared over a Convergence Region or topology-derived subset.

Every Geometry Feature must preserve:

```text
geometry_feature_id
geometry_build_id
convergence_region_id when applicable
input_topology_build_id
feature_kind
feature_value or feature_reference when applicable
feature_units or measurement context when applicable
feature_derivation_basis
source_topology_relationship_ids
source_assertion_ids
validation_status
```

Geometry Feature kinds may include:

```text
density
breadth
depth
intersection_complexity
producer_diversity
modality_diversity
evidence_domain_diversity
provenance_diversity
epistemic_diversity
uncertainty_breadth
independence_breadth
temporal_persistence
temporal_accumulation
namespace_mediation_burden
stratum_diversity
relationship_cardinality
participant_cardinality
region_size
```

Recommended initial feature kinds include:

```text
region_size
relationship_cardinality
participant_cardinality
producer_diversity
evidence_domain_diversity
modality_diversity when available
uncertainty_breadth
namespace_mediation_burden
temporal_accumulation when available
```

Deferred or method-sensitive feature kinds may include:

```text
density
depth
intersection_complexity
temporal_persistence
provenance_diversity
epistemic_diversity
independence_breadth
stratum_diversity
```

Deferred feature kinds are not architecturally prohibited.

They should be implemented only when the geometry derivation policy declares the method, parameters, feature basis, and validation behavior.

Geometry Features are structural descriptors.

They are not biological confidence scores.

They are not clinical actionability scores.

They are not causal claims.

They are not prioritization outputs.

A Geometry Feature without source topology lineage is not compliant.

---

# Feature Derivation Basis Requirements

Every Geometry Feature must declare how it was derived.

Feature derivation basis may include:

```text
topology_relationship_count
source_assertion_count
participant_count
producer_family_count
evidence_domain_count
modality_count
provenance_source_count
uncertainty_state_count
epistemic_state_count
independence_group_count
temporal_generation_count
namespace_mediation_count
relationship_cardinality
region_membership_summary
method_specific_computation
```

Feature derivation basis must preserve:

```text
input topology relationship references
input convergence region reference when applicable
input Assertion Record references when applicable
method or policy reference
builder version when available
parameter set when applicable
lossiness status when applicable
```

A Geometry Feature must not hide its computation behind an opaque convergence score.

If a feature is approximate, lossy, method-specific, or parameter-sensitive, that status must be explicit.

Feature values describe structure.

Feature values do not score truth.

---

# Geometry Feature Identity Strategy

Every Geometry Feature must have a stable identity.

A deterministic `geometry_feature_id` should be derived from stable components when available, such as:

```text
geometry_build_id
convergence_region_id when applicable
feature_kind
feature_derivation_basis
method or policy reference
parameter set reference when applicable
source topology relationship identifiers
```

For example, a producer-diversity feature identity may be derived from:

```text
geometry_build_id
convergence_region_id
feature_kind = producer_diversity
feature_derivation_basis = producer_family_count
geometry_derivation_policy_id
sorted source topology_relationship_ids
```

Feature identity must be deterministic under fixed inputs and policy.

Feature identity must not depend on incidental row order, filesystem traversal order, or non-stable temporary identifiers.

If a stable Geometry Feature identity cannot be produced, the feature must fail validation or be emitted with an explicit unresolved identity status according to the declared validation policy.

---

# Structural Motif Requirements

A Structural Motif is a recurring, declared, or method-recognized structural pattern over topology-derived evidence organization.

Structural Motifs are contract-supported.

For the initial MARK geometry build, Structural Motifs should be considered:

```text
contract-supported
implementation-deferred unless a declared motif policy exists
```

Structural Motifs may include:

```text
participant_intersection
cross_producer_pattern
cross_modality_pattern
multi_participant_pattern
shared_provenance_pattern
shared_epistemic_pattern
shared_uncertainty_pattern
temporal_recurrence_pattern
namespace_mediation_pattern
external_authority_pattern
```

Every emitted Structural Motif must preserve:

```text
structural_motif_id
geometry_build_id
motif_kind
motif_definition or motif_policy reference
source_convergence_region_ids when applicable
source_topology_relationship_ids
source_assertion_ids
feature_references when applicable
validation_status
```

Structural Motifs describe patterns.

They do not assign biological meaning to those patterns.

A Structural Motif without reconstructable source topology is not compliant.

A motif policy must be declared before motif outputs are treated as Convergence Geometry records.

---

# Method And Representation Neutrality Requirements

Convergence Geometry must remain method-neutral and representation-neutral.

A mathematical method may compute, summarize, or project Convergence Geometry.

A mathematical method must not become the VDB evidence model.

Valid current or future methods may include:

```text
relational summaries
matrix-based summaries
graph-derived summaries
hypergraph-derived summaries
simplicial summaries
persistent homology
network analysis
community or neighborhood analysis
motif analysis
tensor analysis
clustering
embedding analysis
manifold analysis
future mathematical methods
```

No method may acquire source authority.

No method may constrain the Convergence Geometry contract unless explicitly adopted by a future governing specification.

Geometry records must be defined in terms of:

```text
geometry build identity
input topology build identity
convergence region identity
region bounding basis
geometry feature identity
feature kind
feature derivation basis
source topology relationships
source Assertion Records
source Corpus Generation
source Registration Units
method provenance
validation status
```

not in terms of any single mathematical framework.

Feature tables, region inventories, geometry reports, dashboards, graph-derived metric tables, matrices, hypergraph summaries, visualizations, or future mathematical outputs are Projection Views when emitted for inspection or consumption.

Those representations do not replace Convergence Geometry.

---

# Method Parameter Requirements

When a geometry method uses parameters, thresholds, filters, distance functions, neighborhood rules, clustering settings, graph metrics, matrix transforms, or other method-specific configuration, those settings must be preserved.

Method parameter records should preserve:

```text
geometry_build_id
method_name or method_reference
method_version when available
parameter_set_id when applicable
parameter_name
parameter_value
parameter_units or context when applicable
parameter_source
default_or_explicit_status
validation_status
```

Parameter-sensitive outputs must expose parameter sensitivity when applicable.

If a Geometry Feature or Structural Motif depends on a parameter set, the feature or motif must reference that parameter set.

Hidden method parameters are not compliant.

---

# Summary And Profile Requirements

Convergence Geometry may emit summaries, inventories, or profiles.

Allowed summaries may include:

```text
number of Convergence Regions
number of Geometry Features
number of Structural Motifs
number of topology relationships characterized
number of Assertion Records represented
number of Registration Units represented
number of producer families represented
number of evidence domains represented
number of namespace-mediated regions
number of uncertainty-bearing regions
number of temporal regions
```

Allowed profiles may include structured summaries of:

```text
region feature sets
producer diversity profiles
modality diversity profiles
uncertainty profiles
epistemic profiles
temporal profiles
namespace mediation profiles
provenance diversity profiles
```

Summaries and profiles must remain traceable to regions, features, motifs, topology relationships, and source Assertion Records.

Summaries and profiles must not replace geometry records.

Summaries and profiles must not imply biological confidence unless explicitly produced by a downstream reasoning system and re-entered as a new preserved assertion.

The implementation should emit summary records only as inspection aids and validation aids.

---

# Validation Strategy

Convergence Geometry validation should operate in four tiers.

## Tier 1: Input Validation

Input validation confirms that governed upstream sources are available.

Validation must check:

```text
input Evidence Topology Build exists
input_topology_build_id is declared
input_corpus_generation_id exists
input Assertion Record source is traceable
downstream geometry input manifest exists
geometry derivation policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
```

Validation must also confirm:

```text
Convergence Geometry does not directly parse raw producer artifacts
Convergence Geometry does not re-run ingestion
Convergence Geometry does not reconstruct Registration Units
Convergence Geometry does not bypass Assertion Record primacy
Convergence Geometry does not bypass Evidence Topology
```

## Tier 2: Region Validation

Region validation confirms that each emitted Convergence Region satisfies region obligations.

Validation must check:

```text
each Convergence Region has a stable identity
each Convergence Region declares a region kind
each Convergence Region declares a region bounding basis
each Convergence Region traces to source topology relationships
each Convergence Region traces through topology to source Assertion Records
each Convergence Region preserves input Corpus Generation lineage
each Convergence Region preserves Registration Unit lineage when applicable
region identity is deterministic
region bounding basis is reconstructable
composite region bounds preserve each contributing criterion
```

## Tier 3: Feature And Motif Validation

Feature validation confirms that each emitted Geometry Feature satisfies feature obligations.

Validation must check:

```text
each Geometry Feature has a stable identity
each Geometry Feature declares a feature kind
each Geometry Feature declares a feature derivation basis
each Geometry Feature traces to source topology relationships
each Geometry Feature traces through topology to source Assertion Records
feature identity is deterministic
feature derivation basis is reconstructable
method-specific parameters are recorded when applicable
lossiness status is explicit when applicable
approximation status is explicit when applicable
parameter sensitivity is explicit when applicable
```

Motif validation must check, when motifs are emitted:

```text
each Structural Motif has a stable identity
each Structural Motif declares motif kind
each Structural Motif declares motif definition or motif policy
each Structural Motif traces to source topology relationships
each Structural Motif traces through topology to source Assertion Records
each Structural Motif references source Convergence Regions when applicable
each Structural Motif references source Geometry Features when applicable
```

## Tier 4: Anti-Collapse Validation

Anti-collapse validation confirms that Convergence Geometry construction did not exceed its layer authority.

Validation must check:

```text
geometry does not modify Evidence Topology
geometry does not mutate Registration Units
geometry does not expand Corpus Generation scope silently
geometry does not become source evidence
geometry does not replace topology relationships
geometry does not replace Assertion Records
geometry does not declare surface eligibility
geometry does not determine surface disclosure
geometry does not emit replacement projections
geometry does not perform biological reasoning
geometry does not embed RDGP reasoning
geometry does not convert structural richness into biological confidence
geometry does not treat density as confidence
geometry does not treat modality diversity as validation
geometry does not treat cross-producer breadth as causality
geometry does not treat temporal persistence as correctness
geometry does not treat namespace mediation as certainty
mathematical representation is not treated as geometry itself
opaque convergence scores do not replace feature basis
```

Validation must confirm structural characterization and reconstructability.

Validation must not claim biological correctness.

---

# Determinism Requirements

Convergence Geometry outputs must be deterministic under fixed inputs.

Given the same:

```text
Corpus Generation manifest
Assertion Record source
Evidence Topology Build
downstream geometry input manifest
geometry derivation policy
geometry validation policy
method parameter configuration
contract version
builder version
Evidence Topology contents
```

the builder should produce equivalent:

```text
geometry_build_id
convergence_region_ids
geometry_feature_ids
structural_motif_ids when emitted
region records
feature records
feature basis records
method parameter records
lineage records
summary records
validation outcomes
report sections
downstream surface input manifest
```

Determinism requirements include:

```text
stable geometry_build_id generation
stable convergence_region_id generation
stable geometry_feature_id generation
stable structural_motif_id generation when motifs are emitted
stable region bounding policy behavior
stable feature derivation policy behavior
stable method parameter handling
stable unresolved-state vocabulary
stable feature kind vocabulary
stable validation status vocabulary
stable source topology relationship ordering
stable source Assertion Record ordering
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define geometry record order.

Filesystem traversal order must not define geometry derivation order.

All source topology relationship lists used in region or feature identity generation should be sorted by stable `topology_relationship_id`.

All source Assertion Record lists used in lineage or reconstruction should be sorted by stable `assertion_id`.

---

# Reconstruction Requirements

Convergence Geometry artifacts must support reconstruction of:

```text
which Corpus Generation bounded the geometry
which Assertion Record source was used when available
which Evidence Topology Build was characterized
which topology relationships were characterized
which geometry derivation policy was applied
which Convergence Regions were bounded
which region kinds were produced
which region bounding bases were used
which Geometry Features were produced
which feature kinds were produced
which feature derivation bases were used
which Structural Motifs were emitted when applicable
which method or policy produced each record
which method parameters were used when applicable
which topology relationships supported each region, feature, or motif
which Assertion Records supported each region, feature, or motif
which Registration Units contributed lineage when applicable
which producer families were represented
which evidence domains were represented
which modalities were represented when available
which uncertainty states were present
which independence contexts were available when available
which temporal or generation context applied
which approximation, lossiness, or parameter-sensitive limitations were observed
which validation checks were applied
which builder produced the geometry
which downstream surface input manifest was emitted
```

Geometry reconstruction must preserve enough information for downstream Evidence Convergence Surfaces, Projection Views, RDGP-facing projections, future downstream reasoning, and future reinterpretation.

---

# Relationship To Evidence Topology

Evidence Topology is the direct input to Convergence Geometry.

The responsibility boundary is:

```text
Evidence Topology
    answers what is connected

Convergence Geometry
    answers what structural properties emerge from those connections
```

Convergence Geometry must preserve traceability to source topology relationships.

Convergence Geometry must not modify Evidence Topology.

Convergence Geometry must not replace Evidence Topology.

Convergence Geometry must not treat topological connectedness as biological meaning.

Topology relationships must remain distinguishable from geometry features.

---

# Relationship To Assertion Records

Assertion Records remain the primary preserved scientific claims.

Convergence Geometry derives structural features through Evidence Topology.

Geometry records must preserve lineage back to source Assertion Records.

Convergence Geometry must not modify Assertion Records.

Convergence Geometry must not replace Assertion Records.

Convergence Geometry must not treat structural richness as producer evidence.

Convergence Geometry must not treat structural richness as biological confidence.

---

# Relationship To Corpus Generations And Registration Units

Corpus Generations provide the declared evidence scope from which topology and geometry are derived.

Registration Units provide the custody boundary for the producer packages selected by the Corpus Generation.

Every Convergence Geometry Build must preserve:

```text
input_corpus_generation_id
input Registration Unit references when applicable
input Assertion Record source reference when available
input topology build reference
```

Convergence Geometry must not expand corpus scope silently.

Convergence Geometry must not include topology relationships outside the declared input Topology Build unless a new Topology Build or explicitly versioned input scope is declared.

Convergence Geometry must preserve Corpus Generation and Registration Unit lineage for downstream surfaces, projections, RDGP reasoning, and reconstruction.

---

# Relationship To Evidence Convergence Surfaces

Convergence Geometry is the direct input to Evidence Convergence Surfaces.

Convergence Geometry may characterize regions and features that surface construction later evaluates for governed exposure.

Convergence Geometry must not declare surface eligibility as geometry records.

If an implementation evaluates surface eligibility, those outputs are governed by the Evidence Convergence Surface contract.

Geometry records must remain distinguishable from surface eligibility records.

Convergence Geometry must not determine surface disclosure.

The responsibility boundary is:

```text
Convergence Geometry
    characterizes topology-derived structure

Evidence Convergence Surface
    exposes governed structurally eligible regions
```

A surface must preserve geometry lineage.

A surface must not replace geometry records.

A surface must not acquire geometry authority.

The downstream surface input manifest emitted by Convergence Geometry means:

```text
these geometry records are available as governed input to a future
Evidence Convergence Surface construction policy
```

It does not mean:

```text
these regions are surface eligible
```

---

# Relationship To Projection Views

Convergence Geometry may be inspected, summarized, exported, or rendered through Projection Views.

A projection over Convergence Geometry must declare:

```text
projection purpose
projection source layer
source geometry_build_id
source convergence_region_ids when applicable
source geometry_feature_ids when applicable
source structural_motif_ids when applicable
source topology_build_id
source Assertion Record identities
source Corpus Generation identity
source Registration Unit identities when applicable
materialization status
lossiness status when applicable
reconstruction path
```

Feature tables, region inventories, geometry reports, dashboards, graph-derived metric tables, matrices, hypergraph summaries, visualizations, or future mathematical outputs are Projection Views when emitted from Convergence Geometry.

A Projection View over Convergence Geometry does not replace Convergence Geometry.

A Projection View does not acquire geometry authority.

A mathematical representation must not be treated as the geometry itself.

---

# Relationship To RDGP Consumer Projections

RDGP-facing consumer projections may include geometry-derived structure directly or indirectly through Evidence Convergence Surfaces.

Convergence Geometry must preserve enough lineage so downstream projections can later expose:

```text
which Convergence Regions were characterized
which Geometry Features were available
which Structural Motifs were present when applicable
which topology relationships supported the geometry
which Assertion Records were involved
which Corpus Generation bounded the geometry
which Registration Units contributed evidence
which producer families, modalities, and evidence domains were represented when available
which uncertainty states were present
which independence contexts were available
which temporal or generation context applied
which structural features may support later biological confidence assessment
```

Convergence Geometry provides the convergence substrate for later reasoning modules.

Convergence Geometry may help RDGP locate biologically meaningful signals within structurally rich evidence regions.

Convergence Geometry does not decide which signal is biologically meaningful.

Convergence Geometry does not perform RDGP reasoning.

Convergence Geometry does not determine whether evidence explains phenotype.

---

# Relationship To Downstream Derived Layers

Convergence Geometry provides the structural characterization substrate for:

```text
Evidence Convergence Surfaces
Projection Views
RDGP-facing consumer projections
future downstream reasoning
```

Downstream derived layers must preserve geometry lineage.

The following must not occur inside Convergence Geometry implementation:

```text
Evidence Convergence Surface eligibility declaration
Evidence Convergence Surface disclosure decision
Projection View generation that replaces Convergence Geometry
RDGP reasoning
biological interpretation
cross-producer breadth interpreted as causality
modality diversity interpreted as validation
density interpreted as confidence
temporal persistence interpreted as correctness
namespace mediation interpreted as certainty
clinical actionability assignment
candidate prioritization
```

---

# Anti-Collapse Safeguards

Implementation must prevent:

```text
Evidence Topology replaced by Convergence Geometry
topology relationship replaced by geometry feature
Assertion Record replaced by geometry feature
Convergence Region replacing source topology lineage
Geometry Feature replacing source topology lineage
Structural Motif replacing source topology lineage
source identity collapse
producer identity collapse
producer-family collapse
evidence-domain collapse
modality collapse
uncertainty collapse
epistemic-status collapse
independence-context collapse
temporal-context collapse
Corpus Generation scope collapse
Registration Unit boundary collapse
region bounding basis collapse
feature derivation basis collapse
method provenance collapse
geometry feature treated as source evidence
geometry feature treated as biological truth
convergence region treated as biological conclusion
structural motif treated as biological mechanism
cross-producer breadth treated as causality
modality diversity treated as validation
density treated as confidence
temporal persistence treated as correctness
namespace mediation treated as certainty
surface eligibility declared inside geometry
projection output replacing geometry
RDGP reasoning embedded inside geometry
mathematical representation treated as geometry itself
opaque convergence score replacing feature basis
structural richness treated as biological confidence
```

Any implementation that performs one of these actions violates this plan and the Convergence Geometry contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Evidence Topology builds before running against the MARK corpus.

Recommended tests include:

```text
test_convergence_geometry_requires_topology_build
test_convergence_geometry_requires_corpus_generation
test_convergence_geometry_requires_derivation_policy
test_convergence_geometry_preserves_geometry_build_id
test_convergence_geometry_preserves_input_topology_build_id
test_convergence_geometry_preserves_input_corpus_generation_id
test_convergence_region_requires_stable_identity
test_convergence_region_requires_region_kind
test_convergence_region_requires_bounding_basis
test_convergence_region_traces_to_topology_relationships
test_convergence_region_traces_to_assertion_records
test_geometry_feature_requires_stable_identity
test_geometry_feature_requires_feature_kind
test_geometry_feature_requires_derivation_basis
test_geometry_feature_traces_to_topology_relationships
test_geometry_feature_does_not_replace_topology_relationship
test_geometry_feature_preserves_method_parameters_when_applicable
test_geometry_feature_preserves_lossiness_status_when_applicable
test_structural_motifs_are_deferred_without_motif_policy
test_structural_motif_requires_policy_when_emitted
test_convergence_geometry_does_not_modify_topology
test_convergence_geometry_does_not_mutate_registration_units
test_convergence_geometry_does_not_expand_corpus_scope
test_convergence_geometry_does_not_declare_surface_eligibility
test_convergence_geometry_does_not_perform_biological_reasoning
test_convergence_geometry_outputs_are_deterministic
test_downstream_surface_input_manifest_is_emitted
```

MARK integration tests should confirm:

```text
mark_phase4_corpus_6tep_v1 Evidence Topology Build is accepted as input
geometry build identity is stable
gene-centered regions are emitted when policy-enabled
phenotype-centered regions are emitted when policy-enabled
sample-centered regions are emitted when policy-enabled
variant-centered regions are emitted when policy-enabled
producer-crossing regions are emitted when policy-enabled
namespace-mediated regions are emitted or deferred under policy
uncertainty-contrast regions are emitted when policy-enabled
initial feature kinds are emitted when policy-enabled
deferred feature kinds are not emitted without policy support
Structural Motifs are not emitted without motif policy
all regions preserve source topology relationship lineage
all features preserve source topology relationship lineage
geometry validation report is deterministic
downstream surface input manifest is deterministic
```

Tests must not require biological correctness.

Tests validate structural characterization, reconstructability, determinism, method provenance, lineage preservation, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define Convergence Geometry derivation policy.

2. Define enabled initial Convergence Region kinds.

3. Define enabled initial region bounding bases.

4. Define enabled initial Geometry Feature kinds.

5. Define deferred feature kinds.

6. Define Structural Motif policy behavior.

7. Define method parameter recording behavior.

8. Load Corpus Generation manifest.

9. Load Evidence Topology Build manifest.

10. Load downstream geometry input manifest.

11. Validate governed input boundary.

12. Generate Geometry Build identity.

13. Construct policy-enabled Convergence Regions.

14. Construct region lineage records.

15. Compute or record policy-enabled Geometry Features.

16. Construct feature derivation basis records.

17. Record method parameters when applicable.

18. Defer Structural Motifs unless a motif policy is declared.

19. Validate regions, features, and motifs when emitted.

20. Emit geometry build manifest.

21. Emit Convergence Region artifacts.

22. Emit Geometry Feature artifacts.

23. Emit geometry lineage artifacts.

24. Emit geometry summary artifacts.

25. Emit geometry validation report.

26. Emit geometry build report.

27. Emit downstream surface input manifest.

28. Add synthetic tests.

29. Add MARK corpus smoke test.

30. Hand off Geometry Build to Evidence Convergence Surface implementation.
```

Each step must preserve topology lineage.

Each step must preserve Assertion Record lineage through topology.

Each step must preserve Corpus Generation lineage.

Each step must remain non-mutating with respect to Registration Units, Assertion Records, and Evidence Topology.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_convergence_geometry.py \
  --topology-build-manifest results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_build_manifest.tsv \
  --geometry-input-manifest results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/downstream_geometry_input_manifest.tsv \
  --corpus-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/corpus_generation_manifest.tsv \
  --output-dir results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1 \
  --geometry-build-id mark_phase4_corpus_6tep_v1_geometry_build_v1 \
  --geometry-derivation-policy-id mark_phase4_vap_gsc_geometry_derivation_policy_v1
```

or:

```bash
python scripts/phase4/validate_convergence_geometry.py \
  --geometry-build-manifest results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/geometry_build_manifest.tsv \
  --convergence-regions results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/convergence_regions.tsv \
  --geometry-features results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/geometry_features.tsv \
  --output-dir results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1
```

The exact script names are not contractually fixed.

The CLI must make Evidence Topology input, Corpus Generation identity, geometry derivation policy, and output location explicit.

---

# Expected Input Manifest Shape

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

This manifest is produced by Evidence Topology implementation.

It is not Convergence Geometry.

It must be validated against the Evidence Topology Build before geometry derivation begins.

---

# Expected Geometry Build Manifest Shape

A Geometry Build manifest may include:

```text
geometry_build_id
geometry_build_label
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
geometry_derivation_policy_id
geometry_derivation_policy_version
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

# Expected Convergence Region Shape

A Convergence Region table may include:

```text
convergence_region_id
geometry_build_id
input_topology_build_id
input_corpus_generation_id
region_label
region_kind
region_bounding_basis
source_topology_relationship_id_summary
source_assertion_id_summary
registration_unit_id_summary
validation_status
```

This table is a Convergence Region index.

It is not a surface.

It is not a projection.

It is not biological reasoning.

---

# Expected Geometry Feature Shape

A Geometry Feature table may include:

```text
geometry_feature_id
geometry_build_id
convergence_region_id
input_topology_build_id
feature_kind
feature_value
feature_reference
feature_units
measurement_context
feature_derivation_basis
source_topology_relationship_id_summary
source_assertion_id_summary
method_reference
parameter_set_id
lossiness_status
validation_status
```

This table records structural descriptors.

It does not record biological confidence.

---

# Expected Geometry Feature Basis Shape

A Geometry Feature basis table may include:

```text
geometry_feature_id
geometry_build_id
convergence_region_id
basis_component_id
basis_component_type
basis_component_value
source_topology_relationship_id
source_assertion_id
source_corpus_generation_id
source_registration_unit_id
method_reference
parameter_set_id
lossiness_status
validation_status
```

Feature basis records may be one-to-many relative to Geometry Features.

Feature basis records must explain how the feature was derived.

---

# Expected Structural Motif Shape

A Structural Motif table may include:

```text
structural_motif_id
geometry_build_id
motif_kind
motif_definition
motif_policy_reference
source_convergence_region_id_summary
source_topology_relationship_id_summary
source_assertion_id_summary
feature_reference_summary
validation_status
```

This table should be emitted only when a declared motif policy exists.

Structural Motifs describe patterns.

They do not assign biological meaning to those patterns.

---

# Expected Method Parameter Shape

A method parameter table may include:

```text
geometry_build_id
method_name
method_version
parameter_set_id
parameter_name
parameter_value
parameter_units
parameter_context
parameter_source
default_or_explicit_status
validation_status
```

Method parameters must be preserved when features, motifs, or summaries depend on them.

---

# Expected Downstream Surface Input Manifest Shape

A downstream surface input manifest may include:

```text
geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
convergence_region_id
region_kind
region_bounding_basis
geometry_feature_id_summary
feature_kind_summary
structural_motif_id_summary when applicable
source_topology_relationship_id_summary
source_assertion_id_summary
registration_unit_id_summary
validation_status
```

This manifest exists to make Evidence Convergence Surface construction deterministic.

It must not declare surface eligibility.

It must not declare disclosure status.

It must not determine consumer-facing exposure.

---

# Exit Criteria

The Convergence Geometry implementation plan is complete when:

```text
Geometry Build identity is stable
input Evidence Topology Build is declared
input Corpus Generation is declared
geometry derivation policy is declared
builder identity is declared
Convergence Regions are created deterministically when emitted
Convergence Regions declare region kind
Convergence Regions declare bounding basis
Convergence Regions trace to topology relationships
Convergence Regions trace through topology to Assertion Records
Geometry Features are created deterministically when emitted
Geometry Features declare feature kind
Geometry Features declare derivation basis
Geometry Features trace to topology relationships
Geometry Features trace through topology to Assertion Records
Structural Motifs trace to topology relationships when emitted
geometry records trace to Corpus Generation
geometry records trace to Registration Units when applicable
method-specific parameters are recorded when applicable
lossiness status is explicit when applicable
geometry summaries remain traceable to geometry records
machine-readable geometry artifacts are emitted
human-readable geometry build report is emitted
geometry validation report is emitted
downstream surface input manifest is emitted
outputs are deterministic under fixed inputs
geometry can serve as input to Evidence Convergence Surfaces
geometry does not become source evidence
geometry does not declare surface eligibility
geometry does not perform biological reasoning
geometry remains representation-neutral and method-neutral
anti-collapse safeguards pass
```

This implementation is not complete merely because a feature table, matrix, graph metric, report, visualization, or mathematical output exists.

It is complete only when those records satisfy the Convergence Geometry contract and can safely serve as the structural characterization substrate for Evidence Convergence Surface construction.

---

# Summary

The Convergence Geometry implementation plan establishes the structural characterization layer in VDB Phase 4.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces expose governed regions.
```

The guiding rule is:

```text
Consume topology.

Characterize structure.

Declare region bounds.

Declare feature basis.

Preserve method provenance.

Preserve lineage.

Remain method-neutral.

Remain representation-neutral.

Do not expose.

Do not project.

Do not reason.

Never convert structure into biological confidence.
```

Convergence Geometry builds the haystack.

Downstream reasoning may search for the needle.

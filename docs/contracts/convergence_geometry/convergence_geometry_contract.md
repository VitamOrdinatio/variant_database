# Convergence Geometry Contract

## Purpose

This document defines the VDB contract for Convergence Geometry.

Convergence Geometry is the deterministic, reconstructable structural characterization of Evidence Topology within a declared Corpus Generation.

Convergence Geometry characterizes structurally rich evidence regions so that downstream VDB layers can construct Evidence Convergence Surfaces, emit Projection Views, and support reasoning systems such as RDGP without allowing structural richness to become biological confidence inside VDB.

This contract ensures that Convergence Geometry remains:

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

Convergence Geometry characterizes organization.

It does not interpret biological meaning.

---

# Scope

This contract applies to all VDB Convergence Geometry builds and geometry-derived structural records, including:

```text
local synthetic geometry builds
small integration-test geometry builds
MARK corpus geometry builds
future multi-producer geometry builds
future multi-cohort geometry builds
future multi-modal geometry builds
future reasoning-informed geometry builds
future external-capsule geometry builds
future release geometry builds
future mathematical-method-specific geometry builds
```

This contract governs the logical requirements of Convergence Geometry.

It does not prescribe a single mathematical method, storage representation, or projection format.

Convergence Geometry may be represented or computed using:

```text
relational records
SQLite records
TSV records
JSON records
JSONL records
feature matrices
region inventories
graph-derived metrics
hypergraph-derived metrics
simplicial summaries
persistent homology outputs
network summaries
tensor summaries
clustering outputs
embedding summaries
manifold summaries
topological summaries
lakehouse partitions
object-store metadata records
future mathematical representations
future storage backends
```

The representation is not the architecture.

The deterministic, reconstructable structural characterization of Evidence Topology is the architecture.

---

# Parent System Contract Obligations

This contract is subordinate to:

```text
docs/contracts/system_contract.md
```

The System Contract establishes the governing VDB authority chain:

```text
Producer TEP
        ↓
registration unit
        ↓
corpus generation
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection Views
        ↓
Downstream Reasoning
```

This contract defines the obligations of the Convergence Geometry layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Convergence Geometry contract governs structural characterization over Evidence Topology.

Convergence Geometry answers:

```text
What structural properties emerge from the connected evidence organization?
```

Convergence Geometry does not answer:

```text
Which evidence is biologically explanatory?

Which gene is causal?

Which variant is pathogenic?

Which candidate should be prioritized?

Which convergence region is clinically actionable?

Which evidence structure represents biological truth?
```

Those responsibilities belong to downstream reasoning systems or returned producer assertions.

---

# Definition

Convergence Geometry is the deterministic structural characterization of Evidence Topology within a declared Corpus Generation.

Convergence Geometry may characterize topology-derived regions, features, motifs, profiles, or other structural summaries.

Convergence Geometry must preserve enough information to support:

```text
geometry build reconstruction
input topology reconstruction
input corpus reconstruction
input Assertion Record reconstruction
convergence region reconstruction
geometry feature reconstruction
structural motif reconstruction when applicable
region bounding basis reconstruction
feature derivation basis reconstruction
method reconstruction
provenance reconstruction
downstream surface construction
downstream projection lineage
downstream consumer reconstruction
```

Convergence Geometry is derived structural characterization.

It is not source evidence.

It is not an Assertion Record.

It is not Evidence Topology.

It is not an Evidence Convergence Surface.

It is not a Projection View.

It is not biological reasoning.

---

# Core Invariant

The architectural rule is:

```text
Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Convergence Geometry does not interpret organization.
```

The governing transition is:

```text
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
```

This means:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Surfaces expose governed regions.
```

Convergence Geometry may generate a structurally rich haystack for downstream reasoning.

It does not decide which element is the biological needle.

---

# Representation And Method Neutrality

Convergence Geometry must remain representation-neutral and method-neutral.

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

Geometry records must therefore be defined in terms of:

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

---

# Required Input Boundary

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

A geometry build must declare:

```text
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id when available
geometry_derivation_policy
builder_name
builder_version when available
build_timestamp
schema or contract version when available
```

If a geometry build uses a governed source other than a formal Evidence Topology Build, that source must be explicitly declared and must preserve traceability to Assertion Records, Corpus Generations, and Registration Units.

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

Geometry Build identity must remain stable across surface construction, projection generation, validation, certification, and reconstruction.

Human-readable labels may support inspection.

Labels must not replace stable Geometry Build identity.

---

# Convergence Region Obligations

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

A Convergence Region is a structural region.

It is not a biological conclusion.

It is not a prioritization result.

It is not a clinical claim.

It is not a surface.

It is not a projection.

A Convergence Region without a declared bounding basis is not VDB-compliant.

---

# Geometry Feature Obligations

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

Geometry Features are structural descriptors.

They are not biological confidence scores.

They are not clinical actionability scores.

They are not causal claims.

They are not prioritization outputs.

A Geometry Feature without source topology lineage is not VDB-compliant.

---

# Structural Motif Obligations

A Structural Motif is a recurring, declared, or method-recognized structural pattern over topology-derived evidence organization.

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

Every Structural Motif must preserve:

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

A Structural Motif without reconstructable source topology is not VDB-compliant.

---

# Region Bounding Basis Obligations

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

The bounding basis must be reconstructable from Evidence Topology.

The bounding basis must preserve source topology relationship references.

The bounding basis must not be replaced by an opaque region label.

If a region is bounded by composite criteria, each contributing criterion must be declared.

A Convergence Region with hidden, implicit, or non-reconstructable bounds is not VDB-compliant.

---

# Feature Derivation Basis Obligations

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

---

# Summary And Profile Obligations

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

---

# Relationship To Evidence Topology

Evidence Topology is the direct input to Convergence Geometry.

Evidence Topology answers:

```text
What is connected?
```

Convergence Geometry answers:

```text
What structural properties emerge from those connections?
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

The distinction is:

```text
Convergence Geometry
    characterizes topology-derived structure

Evidence Convergence Surface
    exposes governed structurally eligible regions
```

A surface must preserve geometry lineage.

A surface must not replace geometry records.

A surface must not acquire geometry authority.

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

RDGP-facing projections must preserve enough geometry lineage so that RDGP can evaluate:

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

# Validation Obligations

Convergence Geometry validation must confirm:

```text
geometry_build_id exists
input_topology_build_id exists
input_corpus_generation_id exists
input Assertion Record source is traceable
geometry derivation policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
each Convergence Region has a stable identity
each Convergence Region declares a region kind
each Convergence Region declares a region bounding basis
each Convergence Region traces to source topology relationships
each Geometry Feature has a stable identity
each Geometry Feature declares a feature kind
each Geometry Feature declares a feature derivation basis
each Geometry Feature traces to source topology relationships
each Structural Motif has a stable identity when motifs are emitted
each Structural Motif traces to source topology relationships
source Assertion Record lineage is reconstructable
source Corpus Generation lineage is reconstructable
source Registration Unit lineage is reconstructable when applicable
method-specific parameters are recorded when applicable
lossiness status is explicit when applicable
geometry derivation is deterministic under fixed inputs
geometry does not modify Evidence Topology
geometry does not mutate Registration Units
geometry does not expand Corpus Generation scope silently
geometry does not become source evidence
geometry does not declare surface eligibility
geometry does not embed projection or reasoning authority
geometry does not convert structural richness into biological confidence
```

Validation must confirm structural characterization and reconstructability.

Validation must not claim biological correctness.

---

# Anti-Collapse Rules

The following are prohibited:

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

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

A Convergence Geometry implementation is complete only when:

```text
Geometry Build identity is stable
input Evidence Topology Build is declared
input Corpus Generation is declared
geometry derivation policy is declared
builder identity is declared
Convergence Regions are created deterministically when emitted
Convergence Regions declare bounding basis
Convergence Regions trace to topology relationships
Geometry Features are created deterministically when emitted
Geometry Features declare feature kind
Geometry Features declare derivation basis
Geometry Features trace to topology relationships
Structural Motifs trace to topology relationships when emitted
geometry records trace through topology to Assertion Records
geometry records trace to Corpus Generation
geometry records trace to Registration Units when applicable
method-specific parameters are recorded when applicable
geometry summaries remain traceable to geometry records
geometry can serve as input to Evidence Convergence Surfaces
geometry does not become source evidence
geometry does not declare surface eligibility
geometry does not perform biological reasoning
geometry remains representation-neutral and method-neutral
anti-collapse validation passes
```

A Convergence Geometry implementation is not complete merely because a feature table, matrix, graph metric, report, visualization, or mathematical output exists.

A Convergence Geometry implementation is complete only when those records satisfy this contract.

---

# Summary

Convergence Geometry is the deterministic, reconstructable structural characterization of Evidence Topology within a declared Corpus Generation.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Surfaces expose governed regions.
```

Convergence Geometry creates the structurally rich convergence substrate that downstream reasoning modules may inspect.

It helps build the haystack.

It does not identify the biological needle.

The guiding rule is:

```text
Consume topology.

Characterize structure.

Declare region bounds.

Declare feature basis.

Preserve lineage.

Remain method-neutral.

Never convert structure into biological confidence.
```

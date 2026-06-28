# Evidence Topology Contract

## Purpose

This document defines the VDB contract for Evidence Topology.

Evidence Topology is the deterministic, reconstructable organization of preserved Assertion Records within a declared Corpus Generation.

Evidence Topology derives relationships, neighborhoods, intersections, and organizational structures over preserved claims so that downstream VDB layers can characterize Convergence Geometry, construct Evidence Convergence Surfaces, emit Projection Views, and support downstream reasoning without transferring source authority to derived structures.

This contract ensures that Evidence Topology remains:

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

Evidence Topology connects claims.

It does not interpret claims.

---

# Scope

This contract applies to all VDB Evidence Topology builds and topology-derived organizational records, including:

```text
local synthetic topology builds
small integration-test topology builds
MARK corpus topology builds
future multi-producer topology builds
future multi-cohort topology builds
future multi-modal topology builds
future reasoning-informed topology builds
future external-capsule topology builds
future release topology builds
```

This contract governs the logical requirements of Evidence Topology.

It does not prescribe a single mathematical representation, storage representation, or projection format.

Evidence Topology may be represented by:

```text
relational records
SQLite records
TSV records
JSON records
JSONL records
matrix representations
graph projections
hypergraph projections
simplicial projections
network projections
tensor projections
topological summaries
lakehouse partitions
object-store metadata records
future mathematical representations
future storage backends
```

The representation is not the architecture.

The deterministic, reconstructable organization of preserved Assertion Records is the architecture.

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

This contract defines the obligations of the Evidence Topology layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Evidence Topology contract governs the first derived organization layer over preserved Assertion Records.

Evidence Topology answers:

```text
What is connected within the declared corpus?
```

Evidence Topology does not answer:

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

Those responsibilities belong to downstream contracts or downstream reasoning systems.

---

# Definition

Evidence Topology is the deterministic organization of preserved Assertion Records within a declared Corpus Generation.

Evidence Topology may organize Assertion Records by shared participants, relationships, contexts, provenance, namespaces, evidence domains, producer families, uncertainty states, independence context, temporal context, or other declared topology dimensions.

Evidence Topology must preserve enough information to support:

```text
topology build reconstruction
input corpus reconstruction
input Assertion Record reconstruction
topology relationship reconstruction
derivation basis reconstruction
relationship member reconstruction
basis component reconstruction
namespace-mediated relationship reconstruction
provenance reconstruction
downstream geometry derivation
downstream surface lineage
downstream projection lineage
```

Evidence Topology is derived organization.

It is not source evidence.

It is not an Assertion Record.

It is not Convergence Geometry.

It is not an Evidence Convergence Surface.

It is not a Projection View.

It is not biological reasoning.

---

# Core Invariant

The architectural rule is:

```text
Assertion Records preserve producer scientific claims.

Evidence Topology derives organization among those claims.

Evidence Topology does not replace those claims.
```

The governing transition is:

```text
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
```

This means:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.
```

---

# Representation Neutrality

Evidence Topology must remain representation-neutral.

A graph may be a useful projection of Evidence Topology.

A graph must not be treated as Evidence Topology itself.

VDB must support current and future representational forms, including:

```text
tables
indices
matrices
graphs
hypergraphs
simplicial complexes
networks
tensors
topological summaries
future mathematical projections
```

No representation may acquire source authority.

No representation may constrain the underlying topology contract unless explicitly adopted by a future governing specification.

Topology relationships must therefore be defined in terms of:

```text
build identity
topology dimension
relationship kind
relationship members
derivation basis
basis components
source Assertion Records
source Corpus Generation
source Registration Units
provenance
validation status
```

not in terms of fixed graph-specific primitives such as nodes and edges.

Graph-specific language may appear in projections or implementation-specific reports.

It must not define the governing topology ontology.

---

# Required Input Boundary

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

A topology build must declare:

```text
input_corpus_generation_id
input_assertion_record_index_id or equivalent governed Assertion Record source
topology_derivation_policy
builder_name
builder_version when available
build_timestamp
schema or contract version when available
```

If a topology build uses a governed source other than a formal Assertion Record index, that source must be explicitly declared and must preserve traceability to Assertion Records or assertion-equivalent records.

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

Topology Build identity must remain stable across geometry derivation, surface construction, projection generation, validation, certification, and reconstruction.

Human-readable labels may support inspection.

Labels must not replace stable Topology Build identity.

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

A topology relationship without a declared derivation basis is not VDB-compliant.

A topology relationship without reconstructable source Assertion Record lineage is not VDB-compliant unless it is explicitly declared as a corpus-level or registration-metadata topology relationship.

---

# Topology Dimension Obligations

Evidence Topology must declare the dimension under which each topology relationship was derived.

Topology dimensions may include:

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
independence
temporal
generation
registration_unit
corpus_generation
overlay
discovery
external_authority
```

Topology dimensions are organizational axes.

They are not biological conclusions.

A topology dimension must not silently combine multiple dimensions unless the derivation policy explicitly declares a composite basis.

Composite topology relationships must preserve each contributing dimension.

---

# Derivation Basis Obligations

Every topology relationship must declare why it exists.

Derivation basis may include:

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

# Relationship Member Obligations

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

Relationship members must preserve:

```text
member_id or member reference
member_type
member_role
source Assertion Record reference when applicable
source Registration Unit reference when applicable
source Corpus Generation reference
basis component reference when applicable
```

Relationship membership must be explicit.

Relationship membership must not imply biological importance.

Relationship membership must not replace Assertion Record lineage.

---

# Basis Component Obligations

Basis components explain the evidence or metadata used to derive a topology relationship.

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

Basis components must be sufficient to reconstruct the derivation of the topology relationship.

If a basis component is unavailable, unresolved, ambiguous, conflicted, or lossy, that state must be explicit.

A topology relationship with hidden or non-reconstructable basis components is not VDB-compliant.

---

# Namespace-Mediated Topology Obligations

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

---

# Discovery And Overlay Obligations

Evidence Topology may consume registered Discovery Events or Overlay Attachments when those records are governed VDB records and preserve derivation provenance.

Topology may use such records to derive relationships only when the relationship basis is explicit.

Discovery or overlay-derived topology must preserve:

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

# Summary And Inventory Obligations

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

---

# Relationship To Assertion Records

Assertion Records are the primary inputs to Evidence Topology.

Evidence Topology derives organization over Assertion Records.

The distinction is:

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

# Relationship To Corpus Generations

Corpus Generations provide the declared evidence scope for Evidence Topology derivation.

Every Evidence Topology Build must preserve:

```text
input_corpus_generation_id
input_corpus_generation_label when available
corpus selection policy reference when available
input Registration Unit references when applicable
```

Evidence Topology must not expand corpus scope silently.

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

Evidence Topology answers:

```text
What is connected?
```

Convergence Geometry answers:

```text
What structural properties emerge from those connections?
```

Evidence Topology may define relationships, neighborhoods, intersections, and organizational structures.

Convergence Geometry may characterize those structures.

Evidence Topology must not characterize convergence density, breadth, depth, producer diversity, modality diversity, epistemic diversity, temporal persistence, or structural motifs as topology records.

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

---

# Relationship To Projection Views

Evidence Topology may be inspected, summarized, exported, or rendered through Projection Views.

A projection over Evidence Topology must declare:

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

Graph, network, matrix, table, report, dashboard, hypergraph, or future mathematical outputs are Projection Views when emitted from Evidence Topology.

A Projection View over Evidence Topology does not replace Evidence Topology.

A Projection View does not acquire topology authority.

A graph projection must not be treated as the topology itself.

---

# Relationship To RDGP Consumer Projections

RDGP-facing consumer projections may include topology-derived structure directly or indirectly through Convergence Geometry and Evidence Convergence Surfaces.

RDGP-facing projections must preserve enough topology lineage so that RDGP can evaluate:

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

# Validation Obligations

Evidence Topology validation must confirm:

```text
topology_build_id exists
input_corpus_generation_id exists
input Assertion Record source exists
topology derivation policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
every topology relationship has a stable identity
every topology relationship declares a topology dimension
every topology relationship declares a relationship kind
every topology relationship declares a derivation basis
every topology relationship has resolvable relationship members
basis components are resolvable or explicitly limited
source Assertion Record lineage is reconstructable
source Corpus Generation lineage is reconstructable
source Registration Unit lineage is reconstructable when applicable
namespace-mediated relationships preserve namespace provenance
discovery-derived relationships preserve discovery provenance when applicable
overlay-derived relationships preserve overlay provenance when applicable
topology derivation is deterministic under fixed inputs
topology does not modify Assertion Records
topology does not mutate Registration Units
topology does not expand Corpus Generation scope silently
topology does not become source evidence
topology does not embed geometry, surface, projection, or reasoning authority
```

Validation must confirm organization and reconstructability.

Validation must not claim biological correctness.

---

# Anti-Collapse Rules

The following are prohibited:

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

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

An Evidence Topology implementation is complete only when:

```text
Topology Build identity is stable
input Corpus Generation is declared
input Assertion Record source is declared
topology derivation policy is declared
builder identity is declared
topology relationships are created deterministically
topology relationships declare dimensions
topology relationships declare derivation basis
topology relationships preserve relationship members
topology relationships preserve basis components
topology relationships trace to Assertion Records
topology relationships trace to Corpus Generation
topology relationships trace to Registration Units when applicable
namespace-mediated relationships preserve namespace provenance
discovery-derived relationships preserve discovery provenance when applicable
overlay-derived relationships preserve overlay provenance when applicable
topology summaries remain traceable to topology relationships
topology can serve as input to Convergence Geometry
topology does not become source evidence
topology does not perform biological reasoning
topology remains representation-neutral
anti-collapse validation passes
```

An Evidence Topology implementation is not complete merely because a graph, table, matrix, index, or file exists.

An Evidence Topology implementation is complete only when those records satisfy this contract.

---

# Summary

Evidence Topology is the deterministic, reconstructable organization of preserved Assertion Records within a declared Corpus Generation.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.
```

Evidence Topology is the first derived layer in the Phase 4 architecture.

It connects preserved claims without interpreting them.

The guiding rule is:

```text
Declare the corpus.

Preserve the assertions.

Derive the relationships.

Declare the basis.

Preserve the lineage.

Avoid representation lock-in.

Never infer biological meaning.
```

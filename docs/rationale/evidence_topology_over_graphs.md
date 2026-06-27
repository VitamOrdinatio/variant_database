# Evidence Topology Over Graphs

## Epoch V: Rationale Layer

| Epoch | Epoch Identity      | Epoch Purpose                                                                                       |
| ----- | ------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer         | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry   | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | Discovery Layer     | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer    | How does one truth generate many useful views without duplication?                                  |
| V     | **Rationale Layer** | **Why is this important?**                                                                          |

---

## Purpose

This document explains why VDB uses Evidence Topology as the governing abstraction for evidence organization rather than treating graphs, graph databases, graph visualizations, or any other representational view as the evidence substrate.

Graphs are useful.

Graph views may be valuable.

Graph databases may be valid implementation backends.

Graph projections may support query, visualization, export, analysis, and downstream reasoning.

But graphs are not the VDB truth substrate.

The central claim is:

```text
Topology is the structure.

Graph is a view.
```

More generally:

```text
Evidence Topology is the governed abstraction.

Graphs, tables, matrices, hypergraphs, dashboards, exports, embeddings, and other projections are representational views over that abstraction.
```

---

# Central Rationale

VDB preserves Assertion Records as the primitive scientific truth objects.

Evidence Topology is derived from those assertions.

Topology describes how preserved assertions are connected, organized, grouped, related, or made adjacent by declared derivation bases.

A graph may display some of those relationships.

But a graph is not the same thing as the topology.

A graph is one possible representation of topology.

The governing distinction is:

```text
Assertions are preserved.

Topology is derived.

Graphs are projected.
```

This distinction prevents representational authority drift.

A view may be useful.

A view may be intuitive.

A view may be computationally powerful.

A view may be visually compelling.

But usefulness does not make a view authoritative.

---

# Assertions Come First

The rationale in `docs/rationale/why_assertions_are_primary.md` establishes that assertions are primary because they preserve scientific meaning before organization, geometry, discovery, projection, reasoning, or interpretation.

Evidence Topology follows from that principle.

Because assertions are primary, evidence relationships must be derived from assertions rather than imposed by a graph schema.

If VDB begins with graph edges, then every scientific statement must be forced into node-edge form.

If VDB begins with assertions, then graph views can be generated when useful, while the original assertion remains intact.

The difference is architectural:

```text
Graph-first architecture:
    evidence must fit the graph

Assertion-first architecture:
    graphs may be generated from evidence
```

VDB chooses assertion-first architecture.

---

# What Evidence Topology Means

Evidence Topology is the derived organization of preserved Assertion Records.

It asks:

```text
What is connected?

By what derivation basis?

From which assertions?

Under which organizational dimension?

With what traceability?
```

Evidence Topology may organize assertions by:

* shared participants
* shared variants
* shared genes
* shared samples
* shared phenotypes
* shared producers
* shared evidence origins
* shared provenance
* shared context
* shared epistemic status
* shared temporal scope
* shared independence groups
* cross-producer intersections
* cross-modality intersections
* multi-component evidence structures
* higher-order evidence neighborhoods

The topology layer does not ask:

```text
What are the graph nodes?

What are the graph edges?

What graph database should be used?

What visualization is most intuitive?
```

Those are representation questions.

Topology asks an architectural question.

Graphs answer a representation question.

Topology answers an architectural question.

---

# What Graphs Are

Graphs are representational structures.

They commonly organize information as:

* nodes
* edges
* labels
* weights
* paths
* neighborhoods
* connected components
* communities
* centrality measures

These structures can be extremely useful.

VDB may use graph representations to:

* visualize evidence neighborhoods
* support topology inspection
* generate query views
* export evidence structure
* compute graph-derived summaries
* communicate convergence
* support downstream reasoning
* render documentation figures

None of this is prohibited.

The architectural rule is simply:

```text
A graph may represent topology.

A graph must not become topology's authority.

A graph must not replace the assertions from which topology derives.
```

---

# Why Graphs Are Not Primary

Graphs are not primary because graph form is narrower than the scientific evidence VDB must preserve.

Graphs often privilege:

* two endpoints
* one edge
* one relationship label
* one edge direction
* one edge weight
* one graph schema
* one representation framework

VDB evidence may be:

* multi-participant
* higher-order
* context-bound
* evidence-bound
* temporally scoped
* provenance-rich
* epistemically qualified
* producer-specific
* modality-specific
* evidence-stratified
* independence-aware
* disclosure-governed
* reasoning-informed

A graph can encode many of these properties.

But it often does so through conventions:

* edge attributes
* auxiliary nodes
* reified statements
* hyperedge simulations
* bipartite expansions
* metadata tables
* embedded JSON payloads
* schema-specific rules
* visualization conventions

Those conventions may be valid implementation choices.

They are not the truth substrate.

The governing rationale is:

```text
When a representation requires conventions to preserve meaning, the convention is not the truth substrate.
```

The assertion remains the truth object.

The topology remains the derived organization.

The graph remains a representation.

---

# The Diamond Metaphor: Facets Are Views, Not the Lattice

The diamond provides a useful symbolic metaphor for VDB's topology and projection architecture.

A diamond is not defined by whichever facet faces the observer.

Its visible facets emerge from the underlying lattice.

Turning the diamond reveals a different face, but the new face does not invalidate or overwrite the previous one.

Multiple facets can be real at the same time because they arise from the same underlying structure.

The metaphor maps naturally to VDB.

In a diamond, visible facets emerge from strong three-dimensional covalent carbon-carbon bonding in a tetrahedral crystal lattice.

In VDB, projected views emerge from the connectivity structure that accrues when producer assertions are brokered, preserved, and organized.

The assertion-derived topology is the lattice-like substrate.

Graphs, tables, matrices, dashboards, exports, convergence surfaces, and other projections are facet-like views.

Each view may reveal something useful.

No single view exhausts the structure.

No single view replaces the substrate.

The metaphor is not a data model.

It is a way to understand why many valid views can coexist without any one view becoming source truth.

The core metaphorical doctrine is:

```text
Graphs are facets, not the lattice.
```

And more generally:

```text
Assertion connectivity creates topology.

Topology gives rise to many facets.

Facets reveal structure.

Facets do not replace structure.
```

A graph projection may reveal one relational face.

A tabular projection may reveal an audit face.

A matrix projection may reveal a computational face.

A surface projection may reveal a convergence face.

An export projection may reveal a downstream reasoning face.

A dashboard projection may reveal an operator-status face.

Each can be valid for its purpose.

None becomes the evidence substrate.

---

# Graph Lock-In

Graph lock-in is the architectural failure mode in which evidence meaning becomes dependent on a particular graph representation, graph schema, graph database, edge model, or visualization convention.

Graph lock-in may cause:

* pairwise flattening
* loss of participant roles
* loss of evidence strata
* loss of epistemic distinctions
* loss of context
* loss of provenance
* loss of temporal scope
* loss of independence metadata
* ambiguous edge semantics
* premature edge weighting
* representation-specific authority
* difficulty supporting future mathematical views
* difficulty representing higher-order evidence
* confusion between visualization and evidence

Graph lock-in does not require use of a literal graph database.

It can occur whenever a representational view becomes authoritative.

Therefore:

```text
Graph lock-in is one instance of projection lock-in.
```

Epoch IV prevents projection lock-in by requiring projections to preserve source identity, source layer, purpose, transform, lineage, and non-authoritative status.

Epoch II prevents graph lock-in by defining topology as a derived organizational abstraction rather than a graph-shaped substrate.

---

# Graphs as Projections

Graphs should be understood as topology projections.

They are one family of views over derived evidence organization.

Other topology projections may include:

* relational tables
* adjacency matrices
* incidence matrices
* hypergraphs
* bipartite views
* knowledge graph views
* RDF-style triples
* JSON neighborhood exports
* surface packages
* timeline views
* dashboard summaries
* embedding spaces
* tensor representations
* validation reports
* TEP-VDB packages
* future mathematical representations

Each projection may serve a different purpose.

A graph may be best for visualization.

A table may be best for audit.

A matrix may be best for computation.

A JSON export may be best for downstream transport.

A dashboard may be best for operator review.

An embedding may be best for exploratory analysis.

None of these projections is the topology itself.

The governing rule is:

```text
No projection over topology becomes topology.

No topology projection becomes assertion truth.
```

---

# Producer-Scoped Surface Notation

A projection facet may be understood as a view over a producer-scoped convergence surface.

The facet is not the source truth.

The facet is not the producer union itself.

The facet is a projected view of a surface derived from assertion records emitted by a declared producer support set.

---

## Producer Support Set

Let:

```text
𝓟 = the set of producer identities known to VDB
```

A producer-scoped view declares a producer support set:

```text
P ⊆ 𝓟
```

where `P` contains the producers whose preserved assertions participate in the scoped surface.

The producer support cardinality is:

```text
k(P) = |P|
```

In plain language:

```text
k = the number of producers contributing assertions to the scoped view
```

This value is not a biological score.

It is not a confidence score.

It is not evidence strength.

It is only the cardinality of the declared producer support set.

---

## Assertion Union

For a VDB generation `g`, let:

```text
A_g(p)
```

represent the set of Assertion Records preserved in generation `g` from producer `p`.

For a producer support set `P`, the scoped assertion corpus is:

```text
A_g(P) = ⋃ A_g(p), for all p ∈ P
```

In plain language:

```text
A_g(P) is the union of all preserved assertions from the producers in P at VDB generation g.
```

Example:

```text
P_A = {VAP, GSC, RSP}

k(P_A) = 3

A_g(P_A) = A_g(VAP) ∪ A_g(GSC) ∪ A_g(RSP)
```

A broader producer support set may be:

```text
P_B = {VAP, GSC, RSP, RDGP}

k(P_B) = 4

A_g(P_B) = A_g(VAP) ∪ A_g(GSC) ∪ A_g(RSP) ∪ A_g(RDGP)
```

If `P_A ⊂ P_B`, then the second scoped assertion corpus includes assertions from an additional producer.

This does not make `P_B` automatically more correct.

It only means the scoped surface is derived from a broader producer support set.

---

## Topology Derived from a Scoped Assertion Corpus

Evidence Topology is derived from Assertion Records.

For a producer support set `P` at generation `g`, the scoped topology may be written as:

```text
T_g(P) = Topology(A_g(P))
```

In plain language:

```text
T_g(P) is the evidence topology derived from the assertion union A_g(P).
```

This topology may organize assertions by shared participants, genes, variants, samples, phenotypes, producers, evidence origins, contexts, provenance, epistemic states, temporal scope, independence groups, or other declared topology dimensions.

The topology is derived.

It is not source truth.

---

## Geometry Derived from Scoped Topology

Convergence Geometry characterizes Evidence Topology.

For a scoped topology `T_g(P)`, the corresponding scoped convergence geometry may be written as:

```text
G_g(P) = Geometry(T_g(P))
```

In plain language:

```text
G_g(P) is the convergence geometry characterized from the scoped topology T_g(P).
```

Geometry may describe structural properties such as density, breadth, depth, producer diversity, modality diversity, provenance diversity, epistemic diversity, temporal persistence, or convergence motifs.

Geometry characterizes structure.

It does not interpret biological meaning.

---

## Surface Derived from Scoped Geometry

An Evidence Convergence Surface exposes structurally eligible convergence geometry under governed disclosure rules.

For a producer support set `P`, the scoped surface may be written as:

```text
S_g(P) = Surface(G_g(P))
```

In plain language:

```text
S_g(P) is the governed convergence surface exposed from geometry derived from assertions emitted by producers in P.
```

A surface is not merely the union of producer assertions.

It is a governed exposure object derived through the full chain:

```text
A_g(P) → T_g(P) → G_g(P) → S_g(P)
```

The surface exposes structurally eligible reasoning capacity.

It does not determine biological meaning.

---

## Projection of a Scoped Surface

A projection renders a governed surface into a view.

For a projection function `π`, a projected facet may be written as:

```text
F_g(P, π) = π(S_g(P))
```

In plain language:

```text
F_g(P, π) is a projected view of the producer-scoped surface S_g(P).
```

Examples of projection functions include:

```text
π_graph
π_table
π_matrix
π_dashboard
π_export
π_validation_report
π_TEP_VDB
```

A graph facet may therefore be written as:

```text
F_g(P, π_graph) = π_graph(S_g(P))
```

A table facet may be written as:

```text
F_g(P, π_table) = π_table(S_g(P))
```

A downstream export facet may be written as:

```text
F_g(P, π_TEP_VDB) = π_TEP_VDB(S_g(P))
```

The projection changes representation.

It does not change authority.

---

## Multiple Facets Can Coexist

Two projected facets may differ by producer support set, projection function, generation, or disclosure scope.

For example:

```text
P_A = {VAP, GSC, RSP}
k(P_A) = 3

F_g(P_A, π_graph)
```

and:

```text
P_B = {VAP, GSC, RSP, RDGP}
k(P_B) = 4

F_g(P_B, π_graph)
```

These are different projected views.

The first facet is derived from a three-producer assertion scope.

The second facet is derived from a four-producer assertion scope that includes RDGP reasoning assertions.

Both facets may be valid at the same time.

The broader facet does not erase the narrower facet.

The narrower facet does not contradict the broader facet.

They are different scoped projections over preserved assertion-derived structure.

The governing rule is:

```text
Different producer support sets may generate different valid surfaces.

Different projections may render those surfaces in different valid ways.

No scoped surface or projection becomes source truth.
```

---

## Generation-Aware Form

Producer-scoped notation is also generation-aware.

A surface derived before RDGP re-entry may be:

```text
S_1({VAP, GSC, RSP})
```

After RDGP consumes a VDB export and emits a TEP-RDGP that is ingested into VDB, a later generation may contain:

```text
S_2({VAP, GSC, RSP, RDGP})
```

The second surface does not overwrite the first.

Instead:

```text
VDB₁ → S_1({VAP, GSC, RSP})

VDB₂ → S_2({VAP, GSC, RSP, RDGP})
```

The difference reflects a later assertion corpus and a later derived topology.

The relationship is temporal, not corrective.

```text
VDB₂ is not VDB₁ corrected.

VDB₂ is VDB₁ expanded by later preserved assertions.
```

---

## Summary Notation

The full scoped derivation chain is:

```text
P ⊆ 𝓟

k(P) = |P|

A_g(P) = ⋃ A_g(p), for all p ∈ P

T_g(P) = Topology(A_g(P))

G_g(P) = Geometry(T_g(P))

S_g(P) = Surface(G_g(P))

F_g(P, π) = π(S_g(P))
```

In prose:

```text
Select a producer support set.

Collect the preserved assertions for that producer scope.

Derive evidence topology.

Characterize convergence geometry.

Expose a governed convergence surface.

Project that surface into a view.
```

The final doctrine is:

```text
Producer support defines scope.

Assertions define source truth.

Topology defines organization.

Geometry defines structural characterization.

Surfaces define governed exposure.

Projections define views.
```

No producer-scoped surface or projection replaces the preserved assertion substrate.


---

# Representation Is Not Authority

A graph view may be easier to understand than the underlying assertions.

A dashboard may be easier to inspect than the underlying topology.

A matrix may be easier to compute over than a lineage-rich assertion corpus.

An export package may be easier to transport than the internal VDB substrate.

These conveniences are valuable.

They are not authority.

VDB must preserve the distinction between:

```text
source truth
```

and:

```text
representational access
```

Representational access may change.

Source authority does not.

This is the same principle established in the Projection Layer:

```text
Projection changes representation, not authority.
```

Graphs follow that rule.

So do all other projections.

---

# Why Topology Is the Correct Abstraction

Topology is the correct governing abstraction because it describes organization without committing to a single representation.

Evidence Topology can describe:

* which assertions share participants
* which assertions share context
* which assertions share provenance
* which assertions share evidence origin
* which assertions cross producers
* which assertions cross modalities
* which assertions share epistemic status
* which assertions are temporally related
* which assertions are independent or correlated
* which assertions form higher-order neighborhoods
* which assertions contribute to convergence regions

A graph can represent some topology.

A table can represent some topology.

A hypergraph can represent some topology.

A matrix can represent some topology.

A future mathematical structure may represent topology in ways not yet anticipated.

Topology remains above those representations.

The key distinction is:

```text
Topology says what organizational relationships exist.

Projection says how those relationships are viewed.
```

---

# Higher-Order Evidence

VDB must support evidence relationships that are not naturally pairwise.

For example, a future convergence region may involve:

```text
VAP variant evidence

GSC semantic prior evidence

RSP transcriptomic evidence

PTN proteomic evidence

RDGP reasoning output

validation assertions

shared phenotype context

shared participant identity

shared temporal or provenance constraints
```

Representing this as pairwise graph edges may be useful.

But the underlying evidence structure is not merely a collection of independent pairwise edges.

It may be a higher-order convergence structure.

Evidence Topology must preserve that possibility.

This is why VDB defines topology relationships without requiring node-edge primitives.

Graphs may project higher-order evidence into readable form.

They must not flatten higher-order evidence into unlabeled pairwise relationships.

---

# Example: POLG Evidence Neighborhood

Consider a POLG-centered evidence neighborhood.

VAP may assert:

```text
sample HG002 contains variant 15:89333596:T:TTGC under a defined variant-calling workflow.
```

GSC may assert:

```text
POLG has a phenotype-scoped semantic prior for mitochondrial disease under a defined consensus run.
```

A future RSP pipeline may assert:

```text
POLG-associated transcriptomic context is differentially expressed under a defined contrast.
```

A future proteomics producer may assert:

```text
POLG-associated protein evidence is altered under a defined assay context.
```

RDGP may later assert:

```text
POLG is prioritized for a sample under a defined reasoning method.
```

Evidence Topology may organize these assertions through shared participant identity, phenotype context, producer family, modality, epistemic status, or temporal scope.

A graph projection may display POLG as a node connected to evidence sources.

That graph may be useful.

But the graph nodes and edges are not the evidence.

The assertions are the evidence records.

The topology relationship is the derived organization.

The graph is the view.

---

# Relationship to Convergence Geometry

Convergence Geometry characterizes Evidence Topology.

It asks:

```text
What structural properties emerge from the topology?
```

This may include:

* density
* breadth
* depth
* intersection complexity
* producer diversity
* modality diversity
* provenance diversity
* epistemic diversity
* independence breadth
* temporal persistence
* structural motifs
* convergence profiles

None of these require topology to be graph-shaped.

Graph algorithms may be used in some implementations.

But graph algorithms are optional methods.

They do not define VDB doctrine.

The relationship is:

```text
Assertions generate topology.

Topology may be characterized as geometry.

Geometry may be exposed as surfaces.

Surfaces and topology may be projected as graphs.

The graph remains a view.
```

---

# Relationship to Evidence Convergence Surfaces

Evidence Convergence Surfaces expose structurally eligible Convergence Geometry.

A surface may feel graph-like if visualized as a network.

But the surface is not a graph.

The surface is a governed exposure object over geometry.

A graph projection of a surface is a view over that exposure object.

The distinction is:

```text
Evidence Convergence Surface:
    governed exposure object

Graph projection:
    representational view of that object
```

A surface may be projected as a graph, table, matrix, dashboard, export package, or future view.

The surface remains the exposure object.

The projection remains the view.

---

# Relationship to Projection Layer

The Projection Layer generalizes the graph argument.

Graphs are one projection family.

They are not special in authority.

They are not privileged as truth.

The Projection Layer allows VDB to produce many useful views over one preserved truth substrate:

* graph views
* table views
* matrix views
* JSON package views
* validation report views
* operator dashboard views
* release views
* export views
* visualization views
* downstream reasoning input views

This supports the diamond metaphor.

Different facets may become visible depending on consumer, purpose, transform, and representation.

No facet replaces the lattice.

No projection replaces topology.

No topology replaces assertions.

---

# Implementation Flexibility

VDB does not prohibit graph implementations.

A valid implementation may use:

* graph databases
* relational tables
* JSON documents
* RDF-style triples
* property graphs
* hypergraph structures
* matrix stores
* document stores
* file-backed manifests
* hybrid representations
* future storage engines

The storage backend is an implementation decision.

The architecture requires that any implementation preserve:

* assertion identity
* topology derivation basis
* source traceability
* provenance
* context
* epistemic status
* evidence strata
* source generation
* reconstruction path
* projection non-authority

A graph database can be compliant.

A relational database can be compliant.

A file-backed manifest system can be compliant.

A graph database can also be non-compliant if it treats graph edges as source truth.

A relational database can also be non-compliant if it flattens evidence into untraceable rows.

Compliance depends on preserving the architecture, not on choosing a particular backend.

---

# What This Prevents

Choosing Evidence Topology over graphs prevents several failure modes.

## Pairwise Flattening

Higher-order evidence is reduced to unlabeled two-node relationships.

## Graph-Schema Authority

A graph schema becomes the de facto scientific model.

## Edge-Weight Overinterpretation

Numeric edge weights become treated as biological truth without preserved method or provenance.

## Provenance Loss

Graph edges obscure producer identity, source artifacts, or reconstruction path.

## Epistemic Collapse

Observed evidence, semantic priors, validation assertions, and reasoning outputs collapse into one relationship type.

## Context Loss

Phenotype scope, temporal scope, assay context, method context, or producer context disappears.

## Projection Lock-In

A useful graph view becomes treated as the underlying evidence substrate.

## Visualization Authority Drift

A network diagram becomes treated as evidence because it is visually persuasive.

## Future Method Blockage

Future hypergraph, tensor, temporal, or multi-modal projections become difficult because the graph was treated as doctrine.

Evidence Topology avoids these failures by remaining representation-independent.

---

# What This Allows

Choosing Evidence Topology over graphs also enables future capabilities.

VDB can support:

* graph projections for visualization
* relational projections for audit
* matrix projections for computation
* hypergraph projections for higher-order evidence
* temporal projections for evidence change over time
* JSON projections for transport
* dashboards for operator review
* TEP-VDB packages for downstream reasoning
* validation projections for system certification
* future mathematical representations not yet known

All of these can coexist.

Like facets of a diamond, each can reveal a different surface of the same underlying structure.

None needs to invalidate the others.

None needs to become truth.

---

# Relationship to Scientific Change

Scientific interpretation changes over time.

Therefore, VDB must preserve evidence organization in a form that can survive changes in representation.

A graph view that is useful today may be insufficient tomorrow.

A future method may require higher-order topology.

Another may require temporal topology.

Another may require tensorized evidence.

Another may require projection into an embedding space.

If VDB treats graphs as the primary substrate, future methods inherit graph assumptions.

If VDB treats topology as the governing abstraction, future methods can generate the representation they need while preserving traceability to assertions.

This is why Evidence Topology is the correct architectural layer.

It preserves organization without freezing representation.

---

# Summary

VDB uses Evidence Topology over graphs because topology is the governed organization of preserved assertions, while graphs are one possible representation of that organization.

Graphs are useful.

Graphs may be implemented.

Graphs may be visualized.

Graphs may be exported.

Graphs may support analysis.

But graphs are not the substrate.

The closing doctrine is:

```text
Assertions are preserved truth objects.

Topology is derived organization.

Graphs are representational projections.
```

Or, in the diamond metaphor:

```text
Graphs are facets, not the lattice.
```

The assertion-derived topology is the lattice-like structure.

Graphs and other projections are views.

Many views can be valid at once.

No view replaces the structure from which it emerged.

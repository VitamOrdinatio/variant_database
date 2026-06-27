# Why Assertions Are Primary

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

This document explains why Assertion Records are the primary preserved scientific objects in VDB.

VDB is designed to preserve evidence across changing scientific paradigms, methods, representations, reasoning systems, and interpretations.

To do that, VDB needs a preservation unit that is more durable than a graph edge, more meaningful than a raw row, more contextual than an entity, more auditable than a score, and less interpretive than a conclusion.

That unit is the assertion.

The central claim is:

```text
Assertions are primary because they preserve scientific meaning before organization, geometry, discovery, projection, reasoning, or interpretation.
```

Assertions are not primary because they are simple.

They are primary because they are the smallest objects that preserve scientific meaning without requiring VDB to decide scientific truth.

---

# Central Rationale

Scientific evidence must be preserved before it is organized.

It must be preserved before it is projected.

It must be preserved before it is interpreted.

It must be preserved before it is adjudicated.

An assertion records a producer-generated scientific statement in a form that can survive later changes in ontology, modeling strategy, reasoning framework, or biological interpretation.

A valid assertion preserves:

* who made the statement
* what relationship was asserted
* which participants were involved
* what evidence supported the statement
* what context bounded the statement
* what provenance supports reconstruction
* what epistemic status qualified the statement
* what temporal, independence, confidence, or derivation context applies

This is the minimum durable structure required for scientific preservation.

---

# What an Assertion Is

An Assertion Record is a provenance-bound, context-bounded evidence statement made by a producer about one or more participants, with an explicit relationship, evidence basis, and epistemic status.

In simplified form:

```text
producer
        asserted
relationship
        among participants
under context
        using evidence
with provenance
        and epistemic status
```

Examples:

```text
VAP asserts that sample HG002 contains a specific variant under a defined variant-calling workflow.
```

```text
GSC asserts that POLG has a phenotype-scoped semantic prior for mitochondrial disease under a defined consensus run.
```

```text
RDGP may assert that a gene is prioritized for a sample under a defined reasoning method.
```

In each case, VDB preserves the assertion as a scientific record.

VDB does not convert the assertion into VDB's own belief.

---

# Observation Is Not Assertion

Observations occur in the world.

Assertions are producer-generated scientific encodings of observations, analyses, classifications, or reasoning outputs.

VDB does not directly preserve biological reality.

It preserves what producers asserted about biological reality under declared methods, contexts, and evidence conditions.

This distinction matters.

A sequencer may produce reads.

A variant caller may produce candidate variants.

A pipeline may annotate those variants.

A producer may emit a structured evidence product.

VDB preserves the producer's assertion.

For example:

```text
The observation:
    sequencing reads align to a genomic region

The producer assertion:
    sample HG002 contains variant 15:89333596:T:TTGC under workflow W, reference R, caller C, and run context K

The VDB responsibility:
    preserve the assertion, provenance, context, and evidence basis
```

VDB preserves assertions because assertions are the scientific objects available for durable preservation.

---

# Why Not Raw Data?

Raw data is important.

But raw data is not the right primary object for VDB.

Raw data may include:

* FASTQ files
* BAM files
* CRAM files
* VCF files
* count matrices
* expression tables
* proteomics tables
* clinical forms
* source spreadsheets
* publication-derived tables

These artifacts may support assertions.

They may provide evidence basis or provenance.

But raw data alone does not express the scientific claim VDB needs to preserve.

A raw file does not by itself say:

```text
Producer X asserts relationship Y among participants Z under context C with evidence basis E.
```

That meaning emerges only through producer method, processing context, interpretation layer, and emitted evidence statement.

Therefore:

```text
Raw data supports assertions.
Raw data does not replace assertions.
```

VDB may reference raw data.

VDB may preserve provenance to raw data.

VDB may record source artifacts as evidence basis.

But the primary preserved scientific object remains the assertion.

---

# Why Not Entities?

Entities are necessary.

They are not sufficient.

A gene, variant, sample, phenotype, condition, pathway, publication, or producer is a participant or context object.

It is not itself evidence.

For example:

```text
POLG
```

alone does not tell VDB anything scientifically actionable.

It does not say whether POLG was observed, prioritized, associated, disputed, validated, expressed, mutated, annotated, or semantically implicated.

Scientific meaning appears when an entity participates in an assertion.

For example:

```text
GSC asserts POLG has a phenotype-scoped semantic prior for mitochondrial disease.
```

```text
VAP asserts sample HG002 contains a variant in a genomic region associated with POLG.
```

```text
RDGP asserts POLG is prioritized for a sample under a declared reasoning method.
```

Entities participate in assertions.

Entities are not the primary evidence object.

---

# Why Not Variant Records?

Variant records are central to many genomic systems.

But VDB is not only a variant store.

VDB must support evidence from multiple producers and modalities:

* variant observations
* semantic gene priors
* transcriptomic observations
* proteomic observations
* validation assertions
* literature-derived assertions
* downstream reasoning outputs
* future evidence modalities not yet defined

A variant record may be a participant in an assertion.

It may be the object of a VAP assertion.

It may appear in topology, geometry, surfaces, and projections.

But it cannot be the universal primary object because many valid VDB assertions do not reduce to variants.

For example:

```text
GSC may assert a phenotype-gene semantic prior without asserting a variant.
```

```text
RSP may assert differential expression without asserting a variant.
```

```text
RDGP may assert a sample-gene prioritization derived from multiple evidence strata.
```

Variant records are important participants.

They are not the universal preservation primitive.

---

# Why Not Graph Edges?

Graph edges are useful.

They are not primary.

Many scientific assertions can be represented as graph-like relationships:

```text
sample contains variant
gene associated with phenotype
variant affects gene
gene participates in pathway
producer emitted assertion
```

But a graph edge is too narrow to serve as VDB's preserved truth primitive.

Graph edges often imply:

* two endpoints
* one relationship
* one representation framework
* one edge type
* one graph-specific topology

VDB assertions may be:

* multi-participant
* context-bound
* evidence-bound
* temporally scoped
* provenance-rich
* epistemically qualified
* producer-specific
* higher-order
* modality-specific
* derived from complex evidence products

A graph edge may represent one projection of an assertion.

It must not replace the assertion.

The governing distinction is:

```text
Graph edges are possible projections of assertions.
They are not the preserved truth primitive.
```

This is why VDB derives topology from assertions instead of making graph edges primary.

Graphs may be useful later.

Assertions must survive even if the graph representation changes.

---

# Why Not Scores?

Scores are useful.

They are also dangerous when treated as primary truth.

A score may appear objective because it is numeric.

But scores usually depend on:

* input corpus
* method
* version
* evidence weights
* thresholds
* normalization
* calibration
* missingness
* training assumptions
* validation strategy
* producer context
* phenotype scope
* temporal scope

Without that context, a score can become an authority trap.

For example:

```text
semantic_prior_score = 0.82
```

is incomplete unless VDB also knows who computed it, using what method, over which source corpus, with what phenotype scope, and under what evidence model.

Therefore:

```text
Scores may be payloads within assertions.
Scores are not primary truth objects.
```

A score emitted by GSC, RDGP, or another producer can be preserved as part of an assertion.

But VDB must preserve the assertion context around the score.

---

# Why Not Conclusions?

Conclusions are downstream products.

They may be valuable.

They may be scientifically important.

They may be produced by expert review, statistical modeling, clinical interpretation, or downstream reasoning systems.

But conclusions depend on evidence, method, assumptions, thresholds, and interpretive context.

Examples of conclusions include:

```text
POLG is prioritized for this sample.
```

```text
Variant X is pathogenic.
```

```text
Gene Y is clinically actionable.
```

```text
Surface Z is biologically meaningful.
```

VDB may preserve such statements if a producer asserts them.

But VDB preserves them as assertions made by that producer.

VDB does not turn them into VDB's own final truth.

The rule is:

```text
A conclusion can be preserved as an assertion.
A conclusion must not replace the assertion model.
```

This allows downstream reasoning systems to contribute evidence while preserving VDB's epistemic boundary.

For example:

```text
RDGP conclusion
        ↓
RDGP assertion
        ↓
VDB preservation
```

RDGP may reason.

VDB preserves the reasoning output as a new assertion.

VDB does not become RDGP.

---

# Why Not Surfaces?

Evidence Convergence Surfaces are important.

They expose structurally eligible evidence geometry.

But surfaces are downstream of assertions.

A surface exists only because preserved assertions have already been organized into topology and characterized as geometry.

A surface is:

* derived
* generation-bound
* rule-dependent
* exposure-oriented
* consumer-relevant
* reconstructable from upstream layers

It is not the source evidence.

The correct relationship is:

```text
Assertions preserve evidence.

Topology organizes assertions.

Geometry characterizes topology.

Surfaces expose geometry.
```

A surface may reveal where evidence currently intersects.

It may support downstream reasoning.

It may be exported or projected.

But it cannot replace the assertions from which it ultimately derives.

---

# Why Not Projections?

Projections are necessary because different consumers need different views.

A projection may be a table, JSON package, dashboard, graph view, validation report, export bundle, release artifact, or visualization.

But projections are views.

They are purpose-bound, representation-specific, and consumer-dependent.

They exist because source evidence or governed derived structure already exists.

A projection may improve access.

It may improve usability.

It may improve transport.

It may improve visualization.

It must not become truth.

Therefore:

```text
Surfaces expose relationships among assertions.

Projections render views over assertions and derived layers.

Neither can replace the assertions from which they ultimately derive.
```

Projection changes representation.

It does not change authority.

---

# The Assertion as the Minimal Durable Scientific Object

The assertion is not minimal because it is small.

It is minimal because it carries the minimum scientific context required for durable preservation.

A valid Assertion Record can preserve:

* producer identity
* assertion type
* relationship
* participants
* evidence basis
* context
* provenance
* epistemic status
* confidence or support
* independence metadata
* temporal scope
* derivation
* payload

This structure allows VDB to preserve scientific meaning without deciding whether the assertion is correct.

That balance is the reason assertions are primary.

A smaller unit loses meaning.

A larger unit risks importing interpretation.

The assertion is the preservation boundary.

---

# Assertion Preservation Is Not Endorsement

Preserving an assertion does not mean VDB endorses it.

VDB preserving an assertion means:

```text
A producer made this evidence statement under this context with this provenance and epistemic status.
```

It does not mean:

```text
VDB believes this assertion is biologically true.
```

This distinction allows VDB to preserve:

* competing assertions
* uncertain assertions
* low-confidence assertions
* null assertions
* negative assertions
* deprecated assertions
* reasoning outputs later challenged by new evidence
* assertions from different scientific paradigms

If two producers emit conflicting assertions, VDB preserves both.

The conflict is part of the scientific record.

---

# Assertion Primacy Enables Multiplicity

Scientific evidence is often plural.

Different producers may assert different things about the same participant because they use different methods, datasets, contexts, thresholds, or assumptions.

VDB must preserve that multiplicity.

For example:

```text
One producer may assert a variant observation.

Another may assert a gene-level semantic prior.

Another may assert transcriptomic evidence.

Another may assert a downstream prioritization.

Another may assert a validation failure.
```

These are not interchangeable.

They should not be collapsed into one support value or one graph edge.

Assertion primacy allows them to coexist as distinct evidence states.

Derived layers may later organize their relationships.

Downstream reasoning may evaluate them.

But the assertions remain individually preserved.

---

# Assertion Primacy Enables Derived Layers

Every later VDB layer depends on assertions.

```text
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection
        ↓
Downstream reasoning
```

Topology is possible because assertions have participants, relationships, context, evidence basis, provenance, and epistemic status.

Geometry is possible because topology can be characterized structurally.

Surfaces are possible because geometry can be exposed in governed ways.

Projections are possible because assertions and derived layers can be viewed, packaged, or rendered for different purposes.

If assertions were not preserved first, later layers would either lose traceability or become the source of truth themselves.

That would invert the architecture.

VDB avoids that inversion.

---

# Assertion Primacy Enables Monotonic Knowledge Flow

Because assertions are primary, VDB can grow without rewriting history.

New evidence enters as new assertions.

Old assertions remain stable.

Derived layers can be recomputed.

Reasoning outputs can re-enter as new assertions.

Historical evidence remains auditable.

The monotonic model is:

```text
new observation or analysis
        ↓
producer assertion
        ↓
VDB preservation
        ↓
updated topology
        ↓
updated geometry
        ↓
updated surfaces
        ↓
updated projections
        ↓
downstream reasoning
        ↓
new producer assertion
```

Nothing in this flow requires rewriting prior assertions.

That is why assertion primacy is compatible with scientific change.

---

# Assertion Primacy Enables Future Paradigms

Future scientific methods may need evidence in forms not anticipated today.

Future VDB consumers may generate:

* graph projections
* hypergraph projections
* simplicial complexes
* tensor representations
* embedding spaces
* temporal topologies
* multi-modal matrices
* probabilistic models
* dashboard summaries
* reasoning input packages
* publication figures
* clinical review packets
* unknown future representations

Assertions can support these future uses because they preserve scientific meaning before any one representation is chosen.

A graph can be regenerated.

A surface can be recomputed.

A projection can be reformatted.

A reasoning model can be replaced.

But lost assertion context cannot be recovered if it was never preserved.

Therefore:

```text
Assertions are primary because they preserve scientific meaning before representation is chosen.
```

---

# Assertion Primacy and Evidence Independence

Assertions also allow VDB to preserve evidence independence.

Two statements may look similar but differ in source, method, evidence basis, producer, or context.

For example:

```text
Two producers may both mention POLG.

One may derive evidence from curated semantic consensus.

Another may derive evidence from sample-level variant observation.
```

These should not collapse simply because they share a participant.

Assertion Records allow VDB to preserve:

* independent evidence origins
* shared evidence origins
* producer-specific evidence
* method-specific evidence
* context-specific evidence
* correlated assertions
* duplicated assertions
* derived assertions

This is essential for downstream reasoning systems that must distinguish convergence from duplication.

---

# Assertion Primacy and Epistemic Status

Scientific evidence is not binary.

Assertions may represent:

* observed evidence
* inferred evidence
* semantic prior evidence
* validation evidence
* null evidence
* negative evidence
* uncertain evidence
* reasoning output
* deprecated evidence
* conflicting evidence

VDB must preserve these distinctions.

If the primary object were a score, graph edge, or conclusion, epistemic status would often be flattened.

Assertion Records preserve epistemic state as part of the evidence object itself.

That is why downstream topology, geometry, surfaces, and projections can remain epistemically safe.

---

# Relationship to Scientific Paradigms

The rationale in `scientific_paradigms_and_evidence_preservation.md` establishes that scientific interpretation changes over time.

This document explains the architectural consequence:

```text
If interpretation changes, VDB must preserve the unit that survives interpretive change.
```

That unit is the assertion.

A paradigm may change.

A disease model may change.

A reasoning method may change.

A representation may change.

A projection may change.

But a preserved assertion still records what a producer claimed, when, about what, under which context, using what evidence.

That is why assertions are primary.

---

# Relationship to Evidence Topology

Assertion primacy explains why Evidence Topology is derived.

Topology describes how preserved assertions relate.

It does not replace assertions.

This matters because topology can change as new assertions arrive.

For example:

```text
An earlier POLG assertion remains unchanged.

A new proteomic assertion involving POLG enters VDB.

The topology around POLG changes.

The old assertion is not rewritten.
```

If topology were primary, structural changes could become destructive.

Because assertions are primary, topology can be recomputed safely.

---

# Relationship to Projections

Assertion primacy also explains why projections are non-authoritative.

A projection may present assertions in useful form.

It may show a table, graph, dashboard, export package, validation report, or figure.

But projection identity is view identity.

Assertion identity remains truth identity.

Therefore:

```text
Projections may change access.
They may not change authority.
```

---

# What Assertion Primacy Prevents

Assertion primacy prevents several architectural failure modes.

## Entity-Centric Collapse

Treating genes, variants, samples, or phenotypes as evidence rather than participants.

## Graph Lock-In

Treating graph edges as primary truth rather than projections or topology-derived representations.

## Score Authority Drift

Treating numeric scores as self-explanatory truth without preserving method, context, and provenance.

## Conclusion Overwrite

Allowing downstream interpretation to overwrite upstream evidence.

## Surface Authority Drift

Treating convergence surfaces as evidence rather than governed exposure objects.

## Projection Authority Drift

Treating dashboards, tables, reports, or export packages as source truth.

## Historical Amnesia

Replacing old evidence states with updated interpretations.

## Evidence Collapse

Merging raw observations, semantic priors, validation assertions, and reasoning outputs into one undifferentiated support bucket.

Assertion primacy prevents these failures by preserving the evidence statement before derived organization or interpretation.

---

# Summary

Assertions are primary because they preserve the scientific statement before VDB organizes, characterizes, exposes, projects, or exports it.

Assertions are not VDB beliefs.

They are producer-attributed scientific evidence statements.

They preserve meaning, provenance, context, participants, evidence basis, epistemic status, and lineage.

Raw data supports assertions.

Entities participate in assertions.

Graph edges may project assertions.

Scores may appear inside assertions.

Conclusions may be preserved as assertions.

Surfaces expose relationships among assertions.

Projections render views over assertions and derived layers.

But assertions remain the preserved truth substrate.

The core doctrine is:

```text
Assertions preserve what was scientifically claimed.

Derived layers preserve how claims relate.

Reasoning systems evaluate what claims may mean.
```

That is why Assertion Records are the primary objects in VDB.

> Because assertions are primary,
> topology must be derived.
> 
> Because topology is derived,
> graphs and projections must be representational.
> 
> Because graphs and projections are representational,
> they cannot be the doctrine.
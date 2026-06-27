# Assertion Record Specification

## Purpose

This document defines the implementation obligations for VDB Assertion Records.

It specifies the semantic guarantees that any Assertion Record implementation must preserve, independent of storage backend, serialization format, database engine, or projection method.

This document is a specification, not a schema. The field-level schema is defined separately in:

```text
docs/implementation/schemas/assertion_record_schema.md
```

The conceptual design model is defined in:

```text
docs/design/assertion_record_and_projection_model.md
```

---

# Core Requirement

VDB implementations must preserve Assertion Records as immutable, provenance-bound, context-bounded evidence statements.

An Assertion Record must preserve what a producer asserted, under what context, using what evidence basis, with what provenance, and with what epistemic status.

VDB must not reinterpret an Assertion Record as biological truth.

---

# Assertion Record Invariant

The invariant of Phase 4 is:

```text
Assertions are primary.
Projections are derived.
```

An Assertion Record is the authoritative preserved object.

Edges, graphs, hypergraphs, RDF triples, simplicial complexes, topological summaries, convergence surfaces, and query surfaces are derived products.

No derived product may replace, mutate, or obscure the originating Assertion Record.

---

# Required Preservation Semantics

Every implementation of Assertion Records must preserve the following semantic classes:

```text
producer identity
assertion type
relationship
participants
evidence basis
context
provenance
epistemic status
```

These semantic classes must remain recoverable from the preserved record or from explicitly linked records.

Implementations may choose different physical representations, but they must not discard these semantics.

---

# Producer Identity Requirement

VDB must preserve the identity of the producer that made the assertion.

Producer identity may include:

```text
producer family
producer repository
producer version
pipeline run
release identifier
TEP identifier
package identifier
```

VDB must not remove, replace, or silently rewrite producer identity.

Producer identity must remain available to downstream projections and reasoning systems.

---

# Relationship Preservation Requirement

VDB must preserve the relationship asserted by the producer.

The relationship is part of the Assertion Record itself.

A graph edge, RDF predicate, hyperedge, or other projected relationship may be derived from the preserved relationship, but it is not the authoritative assertion.

VDB must not force all relationships into pairwise subject-predicate-object form when the assertion is naturally higher-order.

---

# Participant Preservation Requirement

VDB must preserve producer-native participants.

Participants may include:

```text
sample
variant
gene
phenotype
transcript
condition
contrast
publication
source
environmental factor
virus
pathway
cohort
```

Participants must retain:

```text
role
kind
source namespace
source value
source label when available
source record reference when available
```

VDB must not collapse producer-native participants into canonical identities during assertion preservation.

Canonical identity attachment and namespace brokerage are derived operations and must remain distinguishable from the original participant identities.

---

# Evidence Basis Requirement

VDB must preserve the evidence basis supporting the assertion.

Evidence basis may include:

```text
artifact
row
record
variant call
annotation source
semantic score
source contribution
literature source
differential expression result
validation output
pipeline-derived result
```

The evidence basis must remain linked to the Assertion Record when available.

VDB must not replace the evidence basis with downstream interpretation.

---

# Context Requirement

VDB must preserve the context in which the assertion is valid.

Context may include:

```text
sample context
phenotype context
disease context
experimental condition
contrast
tissue
run identifier
pipeline version
reference build
resource release
analysis stage
temporal scope
```

VDB must not generalize an assertion beyond its preserved context.

Context is required to prevent bounded evidence statements from silently becoming broader biological claims.

---

# Provenance Requirement

VDB must preserve chain-of-custody information for each Assertion Record.

Provenance may include:

```text
source repository
TEP identifier
artifact path
artifact hash
source row reference
pipeline run identifier
software version
resource version
timestamp
adapter identity
producer release
```

All projections derived from Assertion Records must retain linkage back to provenance.

No projection may sever the chain of custody from the preserved assertion.

---

# Epistemic Status Requirement

VDB must preserve the epistemic status of each Assertion Record.

Epistemic status describes the kind of knowledge represented.

Initial epistemic classes include:

```text
observed
annotated
asserted
derived
inferred
brokered
projected
hypothesized
```

VDB must not silently promote or demote epistemic status.

Observed, annotated, derived, inferred, brokered, projected, and hypothesized records must remain distinguishable.

---

# Derivation Requirement

Derived records and derived relationships must preserve how they came into existence.

Derivation classes may include:

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

A derived record must not appear indistinguishable from a direct producer assertion.

Derivation metadata must remain visible to downstream reasoning systems.

---

# Independence Requirement

VDB must preserve evidence independence information when available.

Multiple records are not necessarily independent merely because they are represented as multiple assertions.

Assertions may share an upstream evidence origin, such as:

```text
same publication
same database release
same pipeline run
same source adapter
same patient
same cohort
same annotation resource
```

VDB should preserve independence grouping where known.

Downstream reasoning systems must be able to distinguish repeated records from independent evidentiary origins when that information is available.

---

# Confidence and Support Requirement

VDB may preserve producer-provided confidence, score, support, quality, or evidence-strength values.

Examples include:

```text
semantic score
quality score
confidence score
support count
p-value
effect size
validation status
```

Confidence and support values must remain tied to their producer, method, and context.

VDB must not compare or normalize confidence values across producers unless an explicit downstream method defines the comparison.

---

# Temporal Requirement

VDB must preserve temporal and version context where available.

Temporal context may include:

```text
run timestamp
resource release date
publication date
clinical encounter date
analysis date
valid_from
valid_to
```

Time and version context must remain visible because scientific interpretation changes as evidence, resources, and methods evolve.

---

# Projection Requirement

Any projection derived from an Assertion Record must preserve linkage to the originating Assertion Record.

Projection types may include:

```text
participant projection
relationship projection
property graph projection
RDF projection
hypergraph projection
simplicial projection
topological projection
convergence surface
query surface
```

Each projection must preserve or reference:

```text
assertion_id
producer identity
provenance
epistemic status
derivation
```

Projection systems may simplify structure for mathematical or query purposes, but they must not obscure the preserved evidence statement.

---

# Non-Collapse Requirements

## Producer Non-Collapse

Assertions from different producers must not be merged merely because they share participants or relationships.

## Participant Non-Collapse

Producer-native participant identities must not be replaced by canonical identities during assertion preservation.

## Context Non-Collapse

Assertions must not be generalized beyond their preserved context.

## Evidence Non-Collapse

Multiple assertions derived from the same evidence origin must preserve independence information when available.

## Epistemic Non-Collapse

Assertions with different epistemic status must remain distinguishable.

## Projection Non-Collapse

Derived projections must not replace the Assertion Records from which they were generated.

---

# Compatibility with Phase 3

Current Phase 3 registration objects include:

```text
packages
artifacts
assertion_registrations
source_identities
```

These objects are compatible with the Assertion Record specification but do not yet fully implement explicit Assertion Records.

Phase 4 may introduce new objects or tables to represent Assertion Records directly while preserving compatibility with Phase 3 registration outputs.

---

# Relationship to Evidence Topology

Evidence topology is derived from Assertion Records.

VDB may project Assertion Records into topology, graph structures, hypergraphs, simplicial complexes, convergence surfaces, or other mathematical representations.

These representations are useful analytical views, but they are not the preserved scientific substrate.

The preserved scientific substrate is the Assertion Record corpus.

---

# Relationship to Downstream Reasoning

Downstream systems such as RDGP may consume Assertion Record projections for:

```text
statistical reasoning
evidence weighting
Bayesian integration
network propagation
enrichment analysis
hypothesis ranking
biological interpretation
```

Any downstream result must remain linked to the Assertion Records and projections from which it was derived.

VDB must preserve the distinction between evidence preservation and biological interpretation.

---

# Implementation Guidance

Implementations should favor explicitness over compactness.

If preserving a component requires additional linked records, payload fields, or projection tables, implementations should choose preservation over premature simplification.

The implementation must support future projection methods without requiring mutation of existing Assertion Records.

---

# Summary

This specification establishes the semantic obligations for VDB Assertion Record implementations.

The guiding rule is:

```text
A producer makes a bounded evidence statement.
VDB preserves that assertion.
All topology, convergence surfaces, and reasoning products are derived.
```

This specification protects the Truth Layer by ensuring that evidence remains distinguishable from interpretation, provenance remains recoverable, and future mathematical methods can operate over a stable preserved substrate.

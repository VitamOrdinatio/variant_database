# Assertion Record and Projection Model

## Purpose

This document defines the fundamental scientific object preserved by the Variant Database (VDB) and establishes the conceptual relationship between preserved assertions and their derived mathematical representations.

The purpose of this document is **not** to define an implementation schema. Instead, it establishes the conceptual invariant upon which Phase 4 of VDB is built.

---

# Design Principle

The immutable object preserved by VDB is the **Assertion Record**.

All mathematical representations—including relational tables, graphs, hypergraphs, RDF triples, simplicial complexes, topological representations, and future analytical structures—are derived projections of the preserved assertion record.

This distinction is foundational to the Truth Layer philosophy.

---

# Motivation

Scientific understanding changes.

Mathematical methods evolve.

Evidence interpretation improves.

What must remain stable is the faithful preservation of the scientific statements produced by authoritative evidence producers.

Accordingly, VDB does not preserve graphs.

VDB does not preserve edges.

VDB does not preserve biological conclusions.

VDB preserves **Assertion Records**.

Everything else is derived from those preserved records.

---

# Assertion Record

An Assertion Record is defined as:

> A provenance-bound, context-bounded evidence statement made by a producer about one or more participants, with an explicit relationship, evidence basis, and epistemic status.

An Assertion Record represents what a producer asserted.

It does **not** represent biological truth.

It does **not** represent a consensus interpretation.

It does **not** represent a canonical proposition.

Instead, it preserves the original scientific statement exactly as produced.

---

# Scientific Properties of an Assertion Record

Conceptually, every Assertion Record contains:

* producer identity
* relationship being asserted
* participating scientific entities
* evidence basis
* biological and technical context
* provenance
* epistemic status

These conceptual components define the scientific meaning of an assertion.

Their concrete implementation is intentionally deferred to the Assertion Record Schema.

---

# Assertions are Primary

Assertions are the primary preserved scientific object.

Graphs are not primary.

Edges are not primary.

Topological relationships are not primary.

Assertions exist independently of any mathematical representation.

This allows the same preserved assertion to participate in multiple analytical views without modifying the underlying scientific record.

---

# Projection Model

An Assertion Record may be projected into one or more mathematical representations.

Examples include:

* relational database projections
* participant projections
* relationship projections
* property graph projections
* RDF projections
* hypergraph projections
* simplicial projections
* topological projections
* future mathematical representations

These projections are derived products.

They are not authoritative evidence.

---

# Projection Invariants

Every projection generated from an Assertion Record shall preserve the scientific meaning of the original assertion.

Projection may reorganize information.

Projection may simplify information.

Projection may specialize information for a mathematical framework.

Projection shall never alter the underlying scientific statement.

If a mathematical framework cannot faithfully represent an Assertion Record, the limitation lies with the projection—not with the assertion.

---

# Assertion Immutability

Once registered, an Assertion Record is immutable.

Subsequent reasoning systems may derive:

* new relationships
* statistical observations
* convergence surfaces
* hypotheses
* biological interpretations

None of these modify the preserved Assertion Record.

Instead, they create additional derived products that retain explicit derivation and provenance.

---

# Separation of Scientific Responsibilities

Within the VDB ecosystem:

Producer repositories create assertions.

VDB preserves assertions.

VDB projects assertions into mathematical representations.

Downstream reasoning systems consume those projections.

This separation ensures that evidence preservation remains independent from statistical reasoning and biological interpretation.

---

# Relationship to the Truth Layer

The Truth Layer preserves scientific fidelity rather than scientific certainty.

An Assertion Record is considered "true" within VDB in the sense that it faithfully represents what a producer asserted.

Whether that assertion ultimately proves biologically correct is outside the responsibility of VDB.

VDB therefore preserves assertions without strengthening, weakening, or reinterpreting them.

---

# Relationship to Future Mathematical Methods

No single mathematical representation is privileged within VDB.

Graphs, hypergraphs, simplicial complexes, topological methods, and future analytical frameworks are all consumers of the same preserved assertion substrate.

This design intentionally decouples scientific preservation from mathematical representation.

As analytical methods evolve, new projection layers may be added without modifying previously preserved Assertion Records.

---

# Architectural Summary

The conceptual architecture established by this document is:

```text
Producer Assertion
        ↓
Assertion Record
        ↓
Projection Engine
        ↓
Mathematical Representation
        ↓
Downstream Reasoning
```

The Assertion Record is the invariant.

Projections are replaceable.

Reasoning is downstream.

This separation forms the conceptual foundation for Phase 4 of the Variant Database.

---

# Relationship to Future Evidence Organization

The Assertion Record is the primary preserved scientific object within VDB.

Future architectural structures—including evidence topology, convergence geometry, and evidence convergence surfaces—are deterministic projections derived from preserved assertions.

Accordingly, these downstream structures should emerge from preserved assertions rather than serving as alternative representations of truth.

Assertions remain primary.

Organizational structures remain derived.
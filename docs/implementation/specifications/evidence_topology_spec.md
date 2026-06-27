# Evidence Topology Specification

## Epoch II: Evidence Geometry

| Epoch | Epoch Identity        | Epoch Purpose                                                                                       |
| ----- | --------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer           | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | **Evidence Geometry** | **Once assertions exist, how do they organize into biological knowledge?**                          |
| III   | Discovery Layer       | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer      | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer       | Why do we do this?                                                                                  |

---

## Relationship to Design

This specification formalizes the implementation requirements established by:

```
docs/design/evidence_topology_model.md
```

The design document explains **what Evidence Topology is**.

This specification defines **the requirements that every valid Evidence Topology implementation must satisfy**.

---

# Purpose

Evidence Topology provides the first deterministic organizational layer above preserved Assertion Records.

Its purpose is to organize preserved scientific evidence without introducing biological interpretation or modifying producer assertions.

Evidence Topology is a derived implementation artifact.

It is never a source of scientific authority.

---

# Governing Requirement

A valid Evidence Topology implementation **must** produce deterministic, reconstructable, traceable, non-authoritative organizational relationships derived exclusively from preserved Assertion Records.

---

# Scope

This specification governs:

* topology construction
* topology records
* topology projections
* topology derivation
* topology reconstruction
* topology validation

It does not govern:

* biological reasoning
* statistical inference
* convergence analysis
* discovery surfaces

Those belong to later architectural layers.

---

# Input Requirements

Evidence Topology **must** be constructed exclusively from preserved Assertion Records.

Topology construction **must not** introduce information that is absent from the preserved assertion corpus.

Permitted assertion components include:

* participants
* relationships
* context
* provenance
* evidence basis
* producer identity
* epistemic status
* temporal scope
* independence metadata

---

# Derivation Requirements

Every topological relationship **must** be derived from one or more preserved Assertion Records.

Topology implementations **must not** generate relationships through biological inference.

Derived relationships represent organizational structure only.

---

# Derivation Basis

Every topological relationship **must** record its derivation basis.

The derivation basis explains why the organizational relationship exists.

Examples include:

* shared participant
* shared relationship
* shared context
* shared provenance
* shared producer
* shared temporal scope
* shared independence group
* shared evidence basis

The derivation basis is mandatory.

Topology relationships whose origin cannot be explained are invalid.

---

# Dimension Requirements

Every topological relationship **must** declare the organizational dimension through which it was derived.

Supported dimensions include:

* participant
* relationship
* context
* provenance
* epistemic
* temporal
* independence
* producer

Future dimensions may be introduced without altering existing topology.

---

# Traceability Requirements

Every topology record **must** remain traceable to the Assertion Records from which it was derived.

Traceability **must** permit reconstruction of:

* contributing assertions
* contributing assertion components
* derivation basis
* topology dimension

Topology records whose origin cannot be reconstructed are invalid.

---

# Reconstruction Requirements

Evidence Topology **must** be fully reconstructable.

Given an identical corpus of Assertion Records, topology construction **must** produce an equivalent organizational structure.

Evidence Topology therefore remains a derived artifact rather than a permanently authoritative scientific object.

---

# Determinism Requirements

Topology construction **must** be deterministic.

Identical preserved assertions **must** produce identical topology.

Implementation-specific optimizations must not alter topological meaning.

---

# Higher-Order Relationship Requirements

Evidence Topology implementations **must not** assume that all organizational relationships are pairwise.

The implementation **must** support organizational structures involving multiple assertions and multiple participants.

Future mathematical representations may encode these relationships differently without changing their preserved meaning.

---

# Epistemic Preservation Requirements

Topology construction **must** preserve the epistemic status associated with preserved assertions.

Observed evidence must remain distinguishable from:

* annotated evidence
* derived evidence
* brokered evidence
* inferred evidence
* hypothesized evidence

Topology **must not** collapse distinct epistemic classes into a single organizational relationship.

---

# Independence Requirements

Evidence Topology **must** preserve evidence independence.

Assertions originating from a common evidence source must remain distinguishable from assertions representing independent scientific observations.

Repeated references to the same evidence source **must not** be interpreted as independent corroboration.

---

# Provenance Requirements

Every topology relationship **must** preserve sufficient provenance to identify:

* originating producer
* originating assertion(s)
* evidence origin
* derivation pathway

Loss of provenance invalidates the topology relationship.

---

# Non-Authoritative Requirements

Evidence Topology **must not** be treated as scientific evidence.

Topology records:

* are not producer assertions
* are not biological conclusions
* are not scientific observations

They are deterministic organizational artifacts derived from preserved scientific evidence.

---

# Forbidden Behaviors

Evidence Topology implementations **must not**:

* infer biological causality
* assign statistical significance
* determine clinical relevance
* create mechanistic explanations
* modify preserved assertions
* rewrite producer evidence
* remove provenance
* collapse epistemic distinctions
* fabricate organizational relationships lacking derivation basis

---

# Implementation Metadata

Topology construction **should** preserve sufficient implementation metadata to support future auditing.

Recommended metadata includes:

* topology build identifier
* topology builder version
* input assertion corpus identifier
* build timestamp
* implementation version

Such metadata improves reproducibility but does not alter scientific meaning.

---

# Relationship to Convergence Geometry

Evidence Topology provides the organizational substrate consumed by Convergence Geometry.

Topology answers:

> What is connected?

Convergence Geometry answers:

> What structural properties emerge from those connections?

Topology construction therefore precedes all structural analysis.

---

# Validation Requirements

A valid Evidence Topology implementation should support validation of:

* deterministic reconstruction
* complete assertion traceability
* derivation basis completeness
* dimension validity
* provenance preservation
* epistemic preservation
* independence preservation

Validation failures indicate architectural defects rather than biological disagreement.

---

# Summary

A valid Evidence Topology implementation is:

* assertion-derived
* deterministic
* reconstructable
* traceable
* provenance-preserving
* epistemically faithful
* independence-preserving
* higher-order capable
* non-authoritative

Evidence Topology exists to organize preserved Assertion Records.

It does not reinterpret them.

Its purpose is to create a stable, deterministic organizational substrate upon which Convergence Geometry and future Discovery Layers may safely operate without compromising the integrity of the preserved scientific record.

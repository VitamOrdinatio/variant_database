# Convergence Geometry Specification

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

```text
docs/design/convergence_geometry_model.md
```

The design document defines the conceptual model.

This specification defines the implementation obligations that every valid Convergence Geometry implementation must satisfy.

---

# Purpose

Convergence Geometry provides deterministic structural characterization over Evidence Topology.

Its purpose is to identify and describe organizational structure without introducing biological interpretation.

Convergence Geometry is a derived implementation artifact.

It is never a source of scientific authority.

---

# Governing Requirement

A valid Convergence Geometry implementation **must** derive deterministic, reconstructable, traceable, topology-derived structural characterizations while preserving the authority of the underlying Assertion Records and Evidence Topology.

---

# Scope

This specification governs:

* geometry construction
* convergence regions
* geometry features
* structural motifs
* convergence profiles
* geometry validation

It does not govern:

* statistical inference
* biological interpretation
* hypothesis generation
* evidence ranking
* discovery surface exposure

These responsibilities belong to downstream architectural layers.

---

# Input Requirements

Convergence Geometry **must** derive exclusively from Evidence Topology.

Geometry implementations **must not** construct structural characterizations directly from preserved Assertion Records except through documented topology traceability.

This preserves the architectural dependency chain:

```text
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
```

---

# Geometry Build Requirements

Every Convergence Geometry build **must** identify:

* input topology build
* geometry builder
* builder version
* geometry method
* build parameters
* build timestamp

Geometry builds lacking reconstruction metadata are invalid.

---

# Convergence Region Requirements

Every Convergence Region **must** declare its region-bounding basis.

The region-bounding basis explains why a collection of topology relationships constitutes a single structural region.

Examples include:

* participant-centered neighborhood
* phenotype-centered neighborhood
* producer-crossing intersection
* multi-component intersection
* temporal persistence region
* provenance-centered region

Regions without explicit boundaries are invalid.

---

# Geometry Feature Requirements

Every Geometry Feature **must** declare the topology components from which it was derived.

Feature derivation must remain explicit and reconstructable.

Examples include:

* producer diversity derived from producer topology
* provenance diversity derived from provenance topology
* epistemic diversity derived from epistemic topology
* structural breadth derived from participant topology
* temporal persistence derived from temporal topology

Geometry Features whose derivation cannot be reconstructed are invalid.

---

# Structural Motif Requirements

Structural Motifs represent recurring organizational patterns.

Structural Motifs:

* must be deterministic
* must remain topology-derived
* must remain reconstructable

Structural Motifs **must not** imply:

* biological mechanism
* causal explanation
* statistical significance
* clinical importance

Recurring organization is not equivalent to biological interpretation.

---

# Convergence Profile Requirements

Every Convergence Profile **must** summarize the structural properties of a Convergence Region.

Profiles may summarize:

* participant composition
* producer diversity
* provenance diversity
* epistemic diversity
* independence characteristics
* temporal characteristics
* structural complexity

Profiles **must not** assign biological meaning to those summaries.

---

# Traceability Requirements

Every Convergence Geometry object **must** remain traceable to:

* originating topology build
* contributing topology relationships
* contributing Assertion Records

Geometry records whose lineage cannot be reconstructed are invalid.

---

# Determinism Requirements

Convergence Geometry **must** be deterministic.

Given:

* identical topology input
* identical geometry implementation
* identical build parameters

the resulting geometry **must** be equivalent.

Implementation optimizations must not alter structural meaning.

---

# Representation Independence

Convergence Geometry **must not** depend upon any specific mathematical representation.

Implementations may operate using:

* relational organization
* graph representations
* hypergraphs
* simplicial complexes
* topological data analysis
* tensor methods
* future mathematical frameworks

The representation may evolve.

The preserved structural meaning must remain invariant.

---

# Multiple Geometry Implementations

Multiple valid Convergence Geometry implementations may coexist over the same Evidence Topology.

Different implementations may characterize different structural properties provided that they remain:

* deterministic
* traceable
* reconstructable
* topology-derived

The existence of multiple geometry implementations does not alter preserved scientific evidence.

---

# Non-Authoritative Requirements

Convergence Geometry records:

* are not Assertion Records
* are not scientific observations
* are not producer assertions
* are not biological conclusions

They are deterministic structural characterizations derived from Evidence Topology.

---

# Forbidden Behaviors

Convergence Geometry implementations **must not**:

* infer biological causality
* assign statistical significance
* prioritize hypotheses
* determine clinical actionability
* rewrite topology
* modify preserved assertions
* fabricate convergence regions
* create Geometry Features lacking derivation basis

---

# Relationship to Discovery

Convergence Geometry prepares organizational structure for later discovery.

Conceptually:

```text
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
```

Geometry characterizes.

Discovery exposes.

These responsibilities must remain separate.

---

# Validation Requirements

A valid Convergence Geometry implementation should support validation of:

* deterministic reconstruction
* topology traceability
* assertion traceability
* complete region-bounding basis
* complete feature derivation basis
* representation independence
* preservation of producer authority

Validation failures indicate architectural defects rather than biological disagreement.

---

# Summary

A valid Convergence Geometry implementation is:

* topology-derived
* deterministic
* reconstructable
* traceable
* representation-independent
* structurally descriptive
* non-authoritative
* non-inferential

Convergence Geometry exists to characterize the structural organization established by Evidence Topology.

It does not interpret that organization.

Its purpose is to provide a stable structural substrate from which future Discovery Layers may expose regions of scientific interest while preserving the epistemic boundaries established throughout the Truth Layer.

# Ecosystem Layer Model

## Purpose

The repository ecosystem is intentionally organized into architectural layers rather than a collection of independent software projects.

Each repository occupies a specific responsibility domain, operates within a primary identity space, and contributes evidence to a larger discovery ecosystem.

The purpose of the ecosystem layer model is to explain:

* Why repositories remain responsibility-scoped
* Why identity spaces remain distinct
* How evidence moves between layers
* Why interoperability requires brokerage rather than identity collapse
* How VDB functions as the persistence nexus of the ecosystem

This model serves as the conceptual architecture governing repository interaction.

---

## Architectural Principle

The ecosystem is organized according to evidence responsibilities rather than implementation concerns.

Repositories are not separated because they use different technologies.

Repositories are separated because they answer different biological questions.

This distinction is critical.

A repository's primary identity model, evidence model, and responsibility model should remain aligned.

---

## Layer Overview

The ecosystem currently consists of four major layers:

```text
Knowledge Layer
        ↓
Evidence Layer
        ↓
Persistence Layer
        ↓
Reasoning Layer
```

Each layer possesses distinct responsibilities and identity models.

---

## Knowledge Layer

### Purpose

The knowledge layer contains repositories that curate and organize biological knowledge independent of any individual sample.

These repositories generate reusable semantic context.

### Current Repositories

```text
GSC
```

### Primary Identities

```text
Gene
Phenotype
Ontology
Evidence Source
Release
```

### Responsibilities

* Consensus construction
* Evidence-source integration
* Semantic scoring
* Phenotype-specific prioritization
* Release generation
* Knowledge curation

### Outputs

The knowledge layer produces semantic priors that can later be attached to sample-derived evidence.

These outputs remain knowledge-centric rather than sample-centric.

---

## Evidence Layer

### Purpose

The evidence layer generates observations directly from biological data.

These repositories produce evidence rather than interpretation.

### Current Repositories

```text
VAP
Future RSP
```

### Primary Identities

VAP:

```text
Variant
Transcript
Gene
Sample
Observation
```

Future RSP:

```text
Gene
Transcript
Expression Observation
Sample
```

### Responsibilities

* Data processing
* Observation generation
* Evidence annotation
* Provenance capture
* Execution tracking
* Semantic decomposition

### Outputs

The evidence layer produces observation-oriented evidence that remains directly linked to experimental or sequencing data.

---

## Persistence Layer

### Purpose

The persistence layer provides durable semantic storage and interoperability services.

Unlike the knowledge layer and evidence layer, the persistence layer does not own biological interpretation.

Its responsibility is preservation, organization, brokerage, and exposure.

### Current Repository

```text
VDB
```

### Primary Identities

```text
Canonical Identity
Brokered Identity
Persistence Entity
Overlay Entity
Provenance Entity
Query Entity
```

### Responsibilities

* Semantic persistence
* Identity brokerage
* Namespace governance
* Provenance preservation
* Query-surface generation
* Cross-domain interoperability

### Architectural Role

The persistence layer acts as the ecosystem nexus.

All major evidence domains converge here before downstream consumption.

---

## Reasoning Layer

### Purpose

The reasoning layer consumes persisted evidence and generates biological conclusions.

Unlike upstream layers, reasoning repositories focus on interpretation rather than evidence generation or persistence.

### Current Repository

```text
RDGP
```

### Primary Identities

```text
Sample
Gene
Candidate Gene
Reasoning State
Evidence Bundle
```

### Responsibilities

* Candidate prioritization
* Evidence aggregation
* Confidence modeling
* Hypothesis generation
* Explainable ranking

### Outputs

The reasoning layer produces decision-support artifacts rather than raw observations or semantic priors.

---

## Evidence Flow Architecture

Evidence moves vertically through the ecosystem.

```text
Knowledge Layer
        ↓

Evidence Layer
        ↓

Persistence Layer
        ↓

Reasoning Layer
```

This flow should not be interpreted as ownership transfer.

Each repository remains authoritative for the evidence it produces.

VDB persists evidence without assuming ownership of upstream semantics.

RDGP consumes evidence without altering upstream provenance.

---

## Identity-Space Architecture

Identity spaces are intentionally distributed.

Examples include:

```text
Variant identities
Gene identities
Phenotype identities
Sample identities
Transcript identities
Release identities
Execution identities
```

Identity spaces should not collapse into a single universal identity model.

Instead, interoperability is achieved through explicit identity brokerage.

This approach preserves provenance, multiplicity, ambiguity, and future interpretability.

---

## Identity Brokerage and Layer Boundaries

Identity brokerage exists because architectural layers utilize different primary identities.

Examples include:

```text
VAP
    Variant-centric

GSC
    Gene/phenotype-centric

RDGP
    Sample/gene-centric
```

These representations are not competing truths.

They are layer-specific perspectives.

The role of brokerage is to create governed relationships among these perspectives while preserving their independence.

---

## Overlay Architecture

Semantic overlays originate within the knowledge layer.

For example:

```text
GSC release
        ↓
Phenotype-scoped semantic prior
        ↓
VDB persistence
        ↓
RDGP attachment
```

Overlays therefore represent a distinct evidence class within the ecosystem.

They are not variant observations.

They are not reasoning outputs.

They are reusable knowledge-layer artifacts.

---

## Persistence Domains and Layer Independence

Persistence structure should not mirror repository structure.

Likewise, persistence structure should not mirror identity-space structure.

Instead, VDB organizes evidence according to semantic persistence domains.

This allows:

* Cross-repository interoperability
* Stable query surfaces
* Future reinterpretation
* Multi-modal integration
* Independent repository evolution

This principle prevents the ecosystem from becoming tightly coupled to current implementation choices.

---

## Future Expansion

The layer model intentionally anticipates future repositories.

Potential additions include:

```text
Additional evidence-generation systems

Additional knowledge repositories

Additional reasoning systems

Additional ontology services
```

The architectural model should accommodate new repositories through responsibility assignment and identity brokerage rather than structural redesign.

---

## Summary

The ecosystem is organized into four architectural layers:

```text
Knowledge Layer
Evidence Layer
Persistence Layer
Reasoning Layer
```

Each layer possesses distinct responsibilities, evidence models, and identity spaces.

Interoperability is achieved through preservation, brokerage, and persistence rather than identity collapse.

VDB occupies the persistence layer and functions as the interoperability nexus of the ecosystem, enabling independent repositories to cooperate while preserving semantic meaning, provenance, and future interpretability.

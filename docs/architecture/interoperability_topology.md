# Interoperability Topology

## Purpose

The repository ecosystem is designed around interoperability rather than consolidation.

Repositories are intentionally separated according to responsibility, evidence model, and identity model. Interoperability therefore cannot rely upon identity collapse, repository merging, or semantic reduction.

Instead, interoperability emerges through governed relationships among independently maintained evidence systems.

The purpose of this document is to define the architectural topology that enables repositories to cooperate while preserving provenance, semantic meaning, identity integrity, and future interpretability.

---

## Architectural Principle

Interoperability is achieved through preservation rather than simplification.

The ecosystem does not attempt to convert all evidence into a single universal representation.

Instead:

* repositories remain responsibility-scoped
* identity spaces remain distinct
* provenance remains attached
* semantics remain preserved
* interoperability is achieved through brokerage

This principle governs all cross-repository interaction.

---

## Topology Overview

The ecosystem currently consists of four primary repositories:

```text
VAP
GSC
VDB
RDGP
```

and one planned repository:

```text
RSP
```

Their interoperability topology can be represented as:

```text
            GSC
             │
             │
             ▼
VAP ───────► VDB ───────► RDGP
 │            ▲
 │            │
 └────────────┘

Future:

RSP ───────► VDB
```

Not all connections perform the same function.

Each edge within the topology represents a distinct interoperability operation.

---

## Interoperability Operations

The ecosystem currently recognizes several classes of interoperability.

### Variant Persistence

```text
VAP
    ↓
VDB
```

Purpose:

* Preserve variant observations
* Preserve transcript annotations
* Preserve provenance
* Preserve semantic partitions
* Enable future reinterpretation

This operation creates durable evidence persistence.

---

### Overlay Attachment

```text
VAP
    ↔
GSC
```

Purpose:

* Attach phenotype-scoped semantic context
* Enrich evidence
* Preserve source observations
* Preserve phenotype scope

Overlay attachment enriches evidence without modifying source evidence.

---

### Overlay Persistence

```text
GSC
    ↓
VDB
```

Purpose:

* Persist semantic priors
* Preserve phenotype context
* Preserve release identity
* Preserve semantic channels

Overlay persistence transforms semantic overlays into durable knowledge-layer artifacts.

---

### Aggregation

```text
VDB
    ↓
RDGP
```

Purpose:

* Assemble evidence
* Expose query surfaces
* Support candidate prioritization
* Enable explainable reasoning

Aggregation consumes persisted evidence while preserving upstream provenance.

---

### Identity-Space Bridging

```text
GSC
    ↔
RDGP
```

Purpose:

* Connect phenotype-scoped evidence
* Connect sample-scoped evidence
* Preserve independent identities
* Support explainable enrichment

Identity-space bridging does not collapse identity models. It establishes governed relationships between them.

---

## Identity-Space Topology

Interoperability exists because repositories operate within different primary identity spaces.

Examples include:

```text
VAP
    Variant-centric

GSC
    Gene / Phenotype-centric

VDB
    Persistence-centric

RDGP
    Sample / Gene-centric
```

These identities are not competing representations.

They are repository-specific perspectives on biological evidence.

The topology therefore depends upon identity brokerage rather than identity replacement.

---

## Identity Brokerage

Identity brokerage is the primary interoperability mechanism.

Its responsibilities include:

* identity reconciliation
* canonical identity assignment
* namespace resolution
* provenance preservation
* cross-space linkage

Identity brokerage does not create biological truth.

It creates governed relationships among identities.

Canonical identities therefore function as brokerage artifacts rather than semantic-truth artifacts.

---

## Semantic Overlay Topology

Semantic overlays represent a distinct interoperability class.

Unlike persistence operations, overlays enrich evidence without replacing it.

Example:

```text
GSC phenotype prior
        ↓
Overlay attachment
        ↓
Variant observation
```

The resulting evidence remains:

```text
Variant Evidence
+
Overlay Evidence
```

rather than:

```text
Modified Variant Evidence
```

This distinction is constitutionally important.

---

## Persistence-Centered Convergence

VDB functions as the convergence nexus of the ecosystem.

Evidence enters VDB through multiple interoperability pathways:

```text
Variant Persistence

Overlay Persistence

Future Functional Persistence
```

VDB then organizes evidence according to semantic persistence domains rather than repository ownership.

This enables interoperability among repositories that never directly exchange data.

---

## Discovery-Governed Interoperability

Interoperability is not implemented through direct repository coupling.

Instead, VDB employs discovery-governed persistence.

Incoming artifacts are:

```text
Transported
        ↓
Discovered
        ↓
Validated
        ↓
Brokered
        ↓
Persisted
```

This approach allows interoperability to evolve without destabilizing producer repositories.

---

## Repository Independence

Interoperability should not compromise repository autonomy.

Repositories retain authority over:

```text
Evidence generation

Semantic scoring

Execution products

Domain-specific logic
```

VDB provides persistence and brokerage.

RDGP provides reasoning.

GSC provides semantic priors.

VAP provides observations.

Each repository remains responsibility-scoped.

---

## Future Interoperability Expansion

The topology intentionally supports future repositories.

For example:

```text
RSP
```

will introduce functional evidence and transcriptomic evidence.

The ecosystem should accommodate new evidence classes through:

* persistence-domain extension
* identity brokerage
* semantic preservation
* query-surface expansion

rather than through architectural redesign.

---

## Preservation Doctrine

The ecosystem rejects interoperability approaches that require:

* identity collapse
* provenance removal
* semantic reduction
* irreversible normalization
* repository coupling

Instead, interoperability should preserve:

* source identity
* package identity
* provenance
* multiplicity
* semantic context
* historical reproducibility

This doctrine ensures that future biological questions remain answerable.

---

## Summary

The ecosystem employs a preservation-oriented interoperability topology.

Repositories remain responsibility-scoped and identity-scoped.

Interoperability is achieved through:

```text
Persistence

Overlay Attachment

Overlay Persistence

Identity Brokerage

Identity-Space Bridging

Aggregation
```

rather than through repository consolidation or identity collapse.

VDB functions as the convergence nexus of this topology, enabling evidence produced by independent repositories to participate in a shared discovery ecosystem while preserving provenance, semantic richness, and future interpretability.

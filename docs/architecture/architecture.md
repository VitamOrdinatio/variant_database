# VDB Architecture

## Purpose

The Variant Database (VDB) serves as the semantic persistence and interoperability nexus of the repository ecosystem.

Its purpose is not merely to store data, but to preserve, organize, broker, and expose biological evidence in a manner that remains traceable, reproducible, semantically rich, and useful for future discovery.

VDB occupies the architectural position between evidence-producing repositories and evidence-consuming repositories. It receives evidence from upstream systems, persists that evidence according to governed semantic models, and exposes stable query surfaces for downstream reasoning systems.

VDB therefore functions as the ecosystem's durable knowledge infrastructure.

---

## Ecosystem Position

Within the broader repository ecosystem, VDB occupies a central role.

Producer repositories generate evidence:

```text
VAP
    Variant-centric evidence

GSC
    Phenotype-scoped semantic priors

RSP
    Functional and expression evidence
```

Consumer repositories utilize persisted evidence:

```text
RDGP
    Rare disease reasoning
```

VDB sits between these layers.

```text
Producer Repositories
        ↓
Transport
        ↓
Discovery
        ↓
Namespace Brokerage
        ↓
Semantic Persistence
        ↓
Query Surfaces
        ↓
Consumer Repositories
```

This position establishes VDB as the interoperability nexus of the ecosystem.

---

## Architectural Principles

### Semantic Preservation

Evidence should remain semantically rich throughout its lifecycle.

VDB must preserve biological meaning rather than reduce evidence to flattened summaries or convenience-oriented abstractions.

Future biological questions should remain answerable from persisted evidence.

---

### Provenance Preservation

All persisted evidence must remain traceable to its originating source.

Source identities, package identities, execution identities, release identities, and artifact lineage must remain reconstructable.

Derived summaries must remain reproducible.

---

### Additive Normalization

Normalization is additive rather than destructive.

Source identifiers must remain preserved even when canonical identities are assigned.

VDB should create relationships between identities rather than replacing identities.

---

### Identity-Space Independence

Repositories possess distinct identity spaces.

Examples include:

```text
Variant identities
Gene identities
Phenotype identities
Sample identities
Evidence identities
```

Identity spaces must remain independent while still supporting interoperability.

---

### Future-Proofing

Persistence decisions should prioritize future utility.

Evidence should be stored in ways that support reinterpretation, reanalysis, and future scientific discovery.

Architectural simplifications that reduce future interpretability should be avoided.

---

## Core Architectural Components

### Discovery Engine

The discovery engine serves as the governance control plane responsible for evaluating incoming evidence.

Its responsibilities include:

* Artifact characterization
* Schema profiling
* Metadata profiling
* Contract matching
* Validation
* Governance mapping
* Routing decisions

The discovery engine determines what evidence appears to contain before persistence occurs.

---

### Namespace Brokerage Layer

The namespace brokerage layer governs identity relationships.

Its responsibilities include:

* Identity resolution
* Canonical identity assignment
* Namespace reconciliation
* Cross-space mapping
* Provenance-preserving normalization

Namespace brokerage does not alter source identities.

Instead, it creates governed relationships among identities.

---

### Semantic Persistence Layer

The semantic persistence layer organizes evidence according to semantic meaning rather than repository ownership.

Examples include:

```text
Variant evidence

Gene evidence

Phenotype evidence

Functional evidence

Overlay evidence

Provenance evidence
```

Persistence domains remain independent of producer repository structure.

---

### Query Surface Layer

Query surfaces expose persisted evidence to downstream consumers.

These surfaces provide stable access mechanisms for:

* RDGP
* Analytical workflows
* Discovery workflows
* Future repositories
* External consumers

Query surfaces should remain stable even as upstream repositories evolve.

---

## Evidence Lifecycle

Evidence entering VDB follows a governed lifecycle.

```text
Producer Repository
        ↓
Transport
        ↓
Discovery / Profiling
        ↓
Validation
        ↓
Namespace Brokerage
        ↓
Discovery Routing
        ↓
Semantic Persistence
        ↓
Query Surface Exposure
```

Each stage serves a distinct responsibility.

Responsibilities should remain separated to preserve architectural clarity and auditability.

---

## Identity Architecture

Identity is a foundational architectural concern.

VDB recognizes that biological evidence may be represented through multiple identity spaces simultaneously.

Examples include:

```text
Variant
Gene
Phenotype
Sample
Disease
Transcript
Ontology
Release
Execution
```

VDB therefore employs identity brokerage rather than identity replacement.

Canonical identities function as brokerage artifacts.

They enable interoperability while preserving source identity and provenance.

Identity authority resides within VDB, but source identities remain preserved and recoverable.

---

## Persistence Architecture

Persistence is governed by semantic meaning.

Repository ownership does not determine persistence structure.

Likewise, identity spaces do not determine persistence structure.

Instead, evidence is organized according to durable semantic domains.

This approach enables:

* Cross-repository interoperability
* Stable query surfaces
* Future reinterpretation
* Multi-modal evidence integration
* Longitudinal evidence accumulation

The persistence layer therefore functions as a durable knowledge substrate rather than a repository-oriented warehouse.

---

## Discovery and Governance Architecture

VDB operates as a governed system.

Discovery precedes ingestion.

Validation precedes persistence.

Governance precedes normalization.

This ordering ensures that evidence enters VDB through deterministic and auditable workflows.

The discovery engine therefore acts as a governance mechanism rather than merely an ingestion utility.

Its purpose is to preserve architectural consistency across the ecosystem.

---

## Interoperability Architecture

Interoperability is achieved through preservation rather than collapse.

Producer repositories maintain responsibility-scoped evidence models.

Examples include:

```text
VAP
    Variant observations

GSC
    Semantic priors

RSP
    Functional evidence

RDGP
    Reasoning outputs
```

VDB enables interoperability among these systems while preserving their distinct responsibilities.

The goal is evidence convergence rather than evidence homogenization.

---

## Operational Architecture

VDB inherits the ecosystem's operational principles:

* Deterministic execution
* Reproducibility
* Observability
* Structured provenance
* Operator-auditable workflows

Operational behavior should remain transparent and explainable.

Evidence movement, persistence decisions, namespace resolution events, and query-surface generation should remain reconstructable.

---

## Future Directions

The architecture intentionally anticipates future ecosystem expansion.

Planned areas include:

* Functional evidence integration through RSP
* Expanded ontology governance
* Multi-modal evidence convergence
* Advanced discovery workflows
* Cohort-scale evidence exploration
* Enhanced query-surface generation
* Cross-assay interoperability

These future capabilities should emerge through extension of existing architectural principles rather than replacement of foundational doctrine.

---

## Summary

VDB serves as the semantic persistence and interoperability nexus of the repository ecosystem.

Through governed discovery, additive namespace brokerage, semantic persistence domains, provenance preservation, and stable query surfaces, VDB enables independent repositories to interoperate while preserving biological meaning.

Its primary mission is not simply storage.

Its mission is durable, traceable, future-proof preservation and exposure of biological evidence for present and future scientific discovery.

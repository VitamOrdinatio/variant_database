# Transitional Evidence Product (TEP) Technical Justification

## Purpose

This document explains why Transitional Evidence Products (TEPs) exist from a systems architecture perspective.

The goal is not to justify a particular implementation, storage technology, serialization format, or database schema.

Rather, the goal is to justify the existence of a semantically governed transport architecture capable of preserving biological reasoning while repositories, software systems, and evidence ecosystems evolve over time.

This document complements the clinical justification for TEPs and focuses on technical, architectural, and future-proofing concerns.

---

# The Problem of Repository Evolution

Scientific repositories evolve.

New fields appear.

Old fields disappear.

Algorithms improve.

Evidence models mature.

Outputs that were sufficient in one release may become inadequate in future releases.

Examples include:

* VAP gaining new variant interpretation capabilities
* GSC gaining new consensus sources
* RSP gaining new transcriptomic analyses
* RDGP gaining new reasoning frameworks
* A currently unplanned repository being added to the repository ecosystem

Repository evolution is desirable.

Evidence ecosystems also evolve.

Entirely new evidence domains may emerge over time, including transcriptomic, proteomic, imaging, network, pathway, and future modalities not yet represented within the ecosystem.

A future-proof transport architecture must therefore accommodate not only repository evolution, but also evidence-domain evolution.

The transport layer must remain capable of preserving meaning even as new classes of biological evidence appear.

Repository evolution and evidence-domain evolution both present fundamental transport challenges.

A future-proof evidence ecosystem cannot assume that repositories remain static, nor can it assume that future evidence modalities are known in advance.

Evidence transport mechanisms must therefore remain compatible with evolving producer systems while remaining flexible enough to accommodate entirely new evidence domains.

---

# The Problem of Semantic Drift

Data often survives longer than the reasoning used to generate it.

Files remain.

Databases remain.

Reports remain.

However:

* assumptions disappear
* uncertainty disappears
* context disappears
* rationale disappears

Over time, this creates semantic drift.

Future users may possess the evidence but no longer understand what the evidence meant.

A future-proof system must preserve meaning alongside data.

---

# The Problem of Evidence Fragmentation

Modern bioinformatics systems generate evidence across many independent artifacts.

Examples include:

* TSV files
* JSON files
* reports
* metadata bundles
* provenance manifests
* validation outputs

Biological reasoning often spans multiple artifacts simultaneously.

The resulting evidence topology becomes fragmented across repositories and execution stages.

Without explicit transport governance, reconstruction becomes increasingly difficult as systems mature.

---

# Preservation as a First-Class Requirement

Many pipelines focus on evidence generation.

TEPs focus on evidence preservation.

Preservation includes:

* provenance
* traceability
* decomposition
* reproducibility
* explainability
* uncertainty visibility

These properties must survive transport.

A transport system that destroys these properties has failed its mission.

---

# The TEP Sleeve Principle

A TEP sleeve is a semantic projection layer.

The sleeve projects repository-local outputs into ecosystem-portable semantic structures.

Importantly:

```text
Output Contract
        ↓
TEP Sleeve
        ↓
TEP Payload
        ↓
TEP Envelope
```

The sleeve does not modify source artifacts.

The sleeve does not replace source artifacts.

The sleeve preserves source ownership while enabling ecosystem interoperability.

---

# One Producer Execution Generates Many TEPs

A producer execution is not equivalent to a TEP.

For example:

```text
One producer execution
        → many TEPs
```

A single VAP execution may generate many variant-centric evidence states.

A single GSC release may generate many phenotype-gene evidence states.

A single RDGP execution may generate many sample-gene reasoning states.

TEPs therefore represent atomic semantic evidence states rather than entire repository executions.

---

# One TEP May Derive From Many Source Artifacts

A biologically meaningful evidence state frequently spans multiple source artifacts.

For example:

```text
One TEP
        → many source artifacts
```

A single TEP may derive information from:

* annotation outputs
* candidate-review outputs
* validation outputs
* provenance artifacts
* metadata artifacts

Future TEP architectures should therefore support source artifact manifests rather than assuming a single source artifact.

---

# Source Topology Preservation

Evidence topology includes not only artifact lineage, but also the reasoning pathways through which evidence was transformed, filtered, prioritized, or contextualized during repository execution.

Preserving source artifact identity alone is insufficient.

A future-proof transport system must also preserve evidence topology.

Examples include:

* which artifacts contributed evidence
* which fields contributed evidence
* which semantic transformations occurred
* which provenance paths were traversed

> A TEP that cannot reconstruct its originating evidence topology has failed its transport mission.

---

# The Hotel Analogy

The TEP architecture may be understood through a transport analogy.

```text
Repository
    = evolving city

Output Contract
    = everything produced by the city

TEP Sleeve
    = dispatcher / translator

TEP Payload
    = passengers

TEP Envelope
    = travel documents

TEP
    = shuttle

VDB
    = hotel

Discovery Engine
    = concierge
```

Cities evolve.

Roads evolve.

Infrastructure evolves.

However, transport remains successful because the shuttle preserves passenger identity during transit.

The purpose of the shuttle is not to redefine passengers.

The purpose of the shuttle is to deliver them safely.

---

# Preservation Versus Compression

TEPs are not compression mechanisms.

Compression discards information.

TEPs preserve relationships.

The purpose of a TEP is not to reduce evidence.

The purpose of a TEP is to preserve semantically meaningful evidence structures while enabling transport.

TEPs therefore represent semantic synthesis rather than semantic reduction.

---

# Timeless Transport

A future-proof transport architecture must survive repository evolution.

Producer repositories may evolve independently.

Transport governance must remain stable.

This allows:

* historical evidence reconstruction
* longitudinal reinterpretation
* future repository compatibility
* institutional memory preservation

The objective is not to freeze repositories.

The objective is to preserve meaning while repositories evolve.

---

# Future-Proofing Through Projection

The sleeve architecture provides future-proofing through projection.

When repositories evolve:

* source artifacts remain unchanged
* provenance remains unchanged
* TEP projections may evolve

This separation allows transport semantics to improve without mutating historical evidence.

---

# Why Output Contracts Alone Are Insufficient

Output contracts define:

```text
everything produced
```

They do not define:

```text
what should be transported
```

Output contracts serve repository-local needs.

TEPs serve ecosystem-wide interoperability needs.

The two concepts are complementary rather than interchangeable.

---

# Why JSON Alone Is Insufficient

JSON is a serialization format.

JSON defines how information is represented.

JSON does not define:

* provenance requirements
* uncertainty requirements
* semantic transport requirements
* identity requirements
* interoperability requirements

A JSON document may contain a TEP.

A JSON document is not itself a TEP.

---

# Why SQL Alone Is Insufficient

SQL provides storage and retrieval capabilities.

SQL excels at:

* persistence
* indexing
* querying
* aggregation

SQL does not define:

* transport semantics
* evidence ownership
* semantic preservation requirements
* provenance preservation requirements

SQL may store TEPs.

SQL does not replace TEPs.

---

# Strategic Value for VDB

VDB functions as a brokerage and persistence layer.

As repositories evolve, VDB requires a transport architecture capable of preserving semantic integrity across repository boundaries.

TEPs provide that transport architecture.

TEPs allow VDB to persist:

* evidence identity
* provenance
* uncertainty
* explainability
* semantic context

without assuming static producer systems.

---

# Core Principle

```text
The purpose of a Transitional Evidence Product
is not merely to transport evidence.
```

> The purpose of a Transitional Evidence Product is to preserve semantically decomposed, traceable, provenance-aware biological reasoning while producer repositories evolve independently.

---

# Architectural Principle

```text
Source artifacts remain authoritative.

TEPs remain transportable.

Repositories remain evolvable.

Meaning remains preserved.
```

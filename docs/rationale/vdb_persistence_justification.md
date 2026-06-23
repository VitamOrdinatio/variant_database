# VDB Persistence Justification

## Purpose

This document explains why the Variant Database (VDB) exists as a persistence-oriented repository and why evidence persistence is a foundational architectural requirement of the VitamOrdinatio ecosystem.

The purpose of this document is not to define storage implementation details.

The purpose of this document is to explain why persistence is required and what capabilities persistence enables.

---

# Executive Summary

The Variant Database exists because valuable evidence should not become disposable after analysis completes.

Many bioinformatics pipelines produce reports, figures, tables, and candidate lists.

While useful, these outputs are often transient.

Once generated, the underlying evidence relationships become difficult to revisit, reinterpret, connect, or extend.

VDB was created to prevent this loss of evidentiary value.

---

# The Problem

Many traditional workflows resemble the following pattern:

```text
Raw Data
    ↓
Analysis Pipeline
    ↓
Report
```

The report becomes the primary artifact.

Over time:

```text
evidence relationships disappear

intermediate reasoning disappears

cross-study linkage disappears

future reinterpretation becomes difficult

discovery opportunities are lost
```

The result is a workflow optimized for reporting rather than knowledge retention.

---

# Evidence Is More Valuable Than Reports

Reports are snapshots.

Evidence is enduring.

A report answers a question that existed at a particular moment.

Evidence may answer questions that have not yet been asked.

This distinction is especially important in biology.

Scientific understanding changes continuously.

Evidence that appears unimportant today may become important tomorrow.

Therefore:

```text
reports are consumable

evidence is reusable
```

VDB prioritizes preservation of reusable evidence.

---

# The VAP Motivation

The need for VDB became apparent during development of the Variant Annotation Pipeline (VAP).

VAP produces rich evidence layers including:

```text
observed variants

annotations

interpretation overlays

prioritization outputs

validation outputs

lineage relationships
```

Traditional reporting captures only a small fraction of this structure.

Even highly informative case studies eventually become static documents.

Without persistence:

```text
cross-run comparison becomes difficult

variant rediscovery requires reprocessing

evidence lineage becomes fragmented

future reinterpretation becomes expensive
```

Persistence preserves the value of those outputs.

---

# The GSC Motivation

The Gene Set Consensus (GSC) repository revealed a second persistence challenge.

GSC produces:

```text
phenotype-scoped semantic priors

consensus evidence

source attribution

semantic channel relationships

uncertainty information
```

These outputs are not transient calculations.

They represent accumulated biological knowledge.

Without persistence:

```text
semantic priors remain isolated

cross-phenotype comparison becomes difficult

consensus evolution becomes difficult to track

future reuse becomes limited
```

Persistence transforms semantic outputs into reusable evidence assets.

---

# Preservation-First Architecture

VDB adopts a preservation-first philosophy.

This philosophy can be summarized as:

```text
Preserve first.

Interpret second.

Discover third.
```

The repository intentionally prioritizes retention of evidence before downstream reasoning.

This approach differs from systems that aggressively reduce evidence to final candidate lists or summary reports.

---

# Unknown Evidence Has Future Value

One of the central assumptions of VDB is that current scientific knowledge is incomplete.

Examples include:

```text
noncoding variants

poorly characterized genes

novel regulatory elements

unknown gene interactions

future phenotype relationships
```

Evidence that appears low-value today may become high-value later.

Therefore:

```text
absence of current interpretation
    ≠
absence of future importance
```

Persistence protects future discovery opportunities.

---

# Reinterpretation As A First-Class Capability

Most analysis systems are optimized for first-pass interpretation.

VDB is optimized for repeated interpretation.

Scientific understanding evolves through:

```text
new databases

new annotations

new biological mechanisms

new clinical observations

new computational methods
```

Persistence enables previously generated evidence to be revisited under new scientific frameworks.

This capability is essential for long-lived evidence ecosystems.

---

# Persistence Enables Discovery

Discovery requires evidence accumulation.

Discovery cannot occur if evidence is discarded after each analysis.

Persistence allows VDB to connect:

```text
variants

genes

phenotypes

samples

semantic priors

reasoning outputs
```

across repositories and time.

These accumulated relationships create opportunities for future discovery.

---

# Persistence Enables Interoperability

The repository ecosystem is intentionally distributed.

Each producer repository specializes in a distinct domain.

Examples include:

```text
VAP
    observed biological evidence

GSC
    semantic prior evidence

RSP
    transcriptomic evidence

RDGP
    prioritization and reasoning evidence
```

Persistence provides a stable substrate where these evidence classes can coexist.

Without persistence:

```text
interoperability becomes transient

cross-domain reasoning becomes difficult

knowledge becomes fragmented
```

---

# Persistence Enables Provenance Preservation

Evidence without provenance loses interpretability.

Persistence allows VDB to retain:

```text
producer provenance

run provenance

artifact provenance

lineage provenance

transport provenance
```

Preserved provenance enables future consumers to understand not only what evidence exists, but how that evidence was generated.

---

# Persistence Enables Identity Preservation

Evidence identities evolve.

Examples include:

```text
gene identifiers

variant identifiers

sample identifiers

phenotype identifiers
```

Persistence allows VDB to preserve both:

```text
historical identities

future identity mappings
```

This capability is essential for namespace brokerage and long-term interoperability.

---

# Persistence Enables Clinical Reuse

Clinical interpretation frequently occurs across long time horizons.

A variant that lacks interpretation today may become clinically relevant years later.

A semantic prior generated today may support future diagnostic reasoning.

Persistence allows evidence generated in one era to remain available to future clinicians and researchers.

This capability is one of the primary motivations behind the repository.

---

# Why VDB Is Not A Reporting Layer

A reporting layer answers:

```text
What happened?
```

A persistence layer answers:

```text
What should remain available?
```

These are different objectives.

VDB exists to preserve evidence.

Reports remain important, but reports are not the primary mission.

The primary mission is long-term evidence stewardship.

---

# Tradeoffs

Persistence introduces costs.

Examples include:

```text
storage requirements

indexing requirements

identity management complexity

provenance management complexity

ingestion complexity
```

These costs are accepted intentionally.

The repository prioritizes preservation value over short-term storage efficiency.

---

# Relationship To TEPs

Transitional Evidence Products (TEPs) exist because persistence requires transport.

Producer repositories generate evidence.

VDB persists evidence.

TEPs provide the interoperability mechanism that allows evidence to move between those systems without losing:

```text
identity

provenance

topology

authority

scientific meaning
```

Persistence and TEPs are therefore tightly coupled concepts.

---

# Success Criteria

The persistence mission succeeds when future users can:

```text
recover historical evidence

reinterpret evidence under new knowledge

connect evidence across repositories

audit evidence lineage

trace evidence provenance

perform discovery without re-running original analyses
```

while preserving producer intent and scientific context.

---

# Conclusion

The Variant Database exists because evidence should outlive the analyses that produced it.

Persistence transforms transient computational outputs into durable scientific assets.

By preserving evidence, provenance, identity, topology, and interoperability, VDB enables future reinterpretation, future discovery, and future clinical utility.

Persistence is therefore not merely a storage concern.

It is the foundational capability that allows the broader repository ecosystem to accumulate knowledge over time.

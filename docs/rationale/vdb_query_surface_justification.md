# vdb_query_surface_justification.md

## Purpose

This document explains why Query Surfaces exist within the Variant Database (VDB) architecture.

Query Surfaces are not implementation conveniences.

Query Surfaces are architectural boundaries that separate evidence preservation from evidence consumption.

This document describes the design rationale behind that separation.

---

# The Fundamental Problem

The Variant Database exists to preserve evidence.

Consumer systems exist to use evidence.

These goals are related, but they are not identical.

Examples:

```text
VDB
        →
preserve evidence

RDGP
        →
reason over evidence

future analytics systems
        →
analyze evidence

future discovery systems
        →
discover evidence

future clinical systems
        →
consume evidence
```

A preservation system and a reasoning system naturally require different representations of the same information.

---

# Early Repository Ecosystem Assumption

Early repository development naturally suggested a simpler architecture:

```text
VAP
        ↓

adapter

        ↓

RDGP
```

The adapter would transform VAP outputs into an RDGP-consumable representation.

This approach can work.

However, it introduces a hidden architectural risk.

---

# The Adapter Problem

When consumer systems directly drive data structure design, a subtle inversion occurs:

```text
consumer format
        ↓
becomes storage format
```

Over time:

```text
storage representation
        ↓
consumer representation
```

become indistinguishable.

The preservation layer begins to resemble the reasoning layer.

Eventually:

```text
evidence preservation
```

is constrained by:

```text
consumer requirements
```

This creates semantic pressure toward simplification.

---

# Preservation And Consumption Are Different Problems

Preservation systems naturally optimize for:

```text
identity

provenance

authority

artifacts

lineage

uncertainty

future reinterpretability
```

Consumer systems naturally optimize for:

```text
simplicity

speed

task-specific views

reasoning inputs

analysis-ready structures
```

Neither goal is incorrect.

However, neither goal should dictate the other.

---

# Architectural Separation

To prevent preservation and consumption concerns from collapsing into one another, VDB introduces a dedicated Query Surface Layer.

Conceptually:

```text
Persistence Layer
        ↓
Query Surface Layer
        ↓
Consumer Layer
```

Where:

```text
Persistence
        →
preserve evidence

Query Surface
        →
organize evidence

Consumer
        →
reason over evidence
```

This separation is intentional.

---

# Query Surfaces Are Not Database Queries

A Query Surface should not be understood as a SQL statement.

A Query Surface is a governed evidence retrieval contract.

Examples:

```text
sample-gene evidence retrieval

overlay retrieval

RDGP evidence preparation

evidence reconstruction
```

A Query Surface defines:

```text
what evidence is exposed

what evidence remains visible

what provenance remains visible

what uncertainty remains visible

what identity remains visible
```

Implementation technology is secondary.

---

# Why Consumers Should Not Query Persistence Directly

Without Query Surfaces:

```text
consumer systems
```

must understand:

```text
physical tables

artifact topology

namespace topology

overlay topology

provenance topology

discovery topology
```

This creates tight coupling between consumers and storage architecture.

Examples:

```text
RDGP coupled to VDB internals

future RSP coupled to VDB internals

future systems coupled to VDB internals
```

Such coupling reduces architectural flexibility.

---

# Query Surfaces Reduce Coupling

With Query Surfaces:

```text
consumer
        ↓

query surface
        ↓

preservation layer
```

Consumers request evidence.

Consumers do not need to understand how evidence is physically stored.

This allows:

```text
storage architecture

namespace architecture

overlay architecture

discovery architecture
```

to evolve independently from consumers.

---

# Query Surfaces As Anti-Collapse Architecture

One of the greatest long-term risks to preservation systems is semantic collapse.

Without architectural safeguards:

```text
preserved evidence
        ↓

flattened representation
        ↓

consumer workflow
```

gradually becomes:

```text
flattened representation
        ↓

authoritative representation
```

Eventually:

```text
preserved evidence
```

becomes secondary.

This is a preservation failure.

---

# Preserved Evidence Remains Authoritative

Within VDB:

```text
preserved evidence
```

remains authoritative.

Query Surfaces expose:

```text
derived representations
```

for specific consumers.

The distinction is critical.

Conceptually:

```text
preserved evidence
        →
authority

query surfaces
        →
views
```

Query Surfaces are consumers of preserved evidence.

They are not replacements for preserved evidence.

---

# Evidence States Rather Than Rows

Traditional databases expose rows.

VDB exposes evidence states.

Examples:

```text
sample-gene evidence state

variant observation state

semantic prior state

overlay attachment state

evidence reconstruction state
```

Query Surfaces therefore retrieve evidence states rather than isolated records.

This aligns query behavior with preservation objectives.

---

# Why Four Query Surfaces Exist

The VDB Query Surface architecture is intentionally organized around four core operations.

---

## Retrieve

```text
sample_gene_evidence_query.md
```

Answers:

```text
What evidence exists?
```

---

## Relate

```text
overlay_attachment_query.md
```

Answers:

```text
What evidence is connected?
```

---

## Prepare

```text
rdgp_surface_query.md
```

Answers:

```text
What evidence should be emitted?
```

---

## Reconstruct

```text
evidence_reconstruction_query.md
```

Answers:

```text
Why does this evidence exist?
```

---

# Query Surfaces And Discovery

VDB is not limited to producer-supplied evidence.

The Discovery Engine may identify additional contextual evidence.

Examples:

```text
BioSample metadata

BioProject metadata

external ontologies

future external resources
```

Discovered evidence must also become queryable.

Query Surfaces provide the mechanism through which discovered evidence enters the ecosystem.

---

# Query Surfaces And Future Reinterpretation

The repository ecosystem is explicitly designed to support future reinterpretation.

Examples include:

```text
future regulatory models

future noncoding interpretation

future transcriptomic integration

future network convergence analysis

future reasoning systems
```

The requirements of those future systems cannot be known today.

Therefore:

```text
VDB preserves broadly.

Query Surfaces expose narrowly.
```

This allows preservation requirements and consumer requirements to evolve independently.

---

# Query Surfaces And RDGP

RDGP is an important consumer of VDB.

However, RDGP is not the only consumer.

The Query Surface layer prevents RDGP requirements from becoming preservation requirements.

This allows:

```text
RDGP

future RSP

future discovery systems

future analytics systems

future clinical systems
```

to coexist without forcing all consumers into the same representation.

---

# Architectural Benefits

The Query Surface architecture provides:

```text
consumer decoupling

preservation protection

identity preservation

provenance preservation

uncertainty preservation

overlay preservation

future reinterpretability

future extensibility
```

while maintaining deterministic evidence access.

---

# Design Principle

The central design principle of Query Surfaces is:

```text
Preservation and consumption
are different architectural concerns.
```

Query Surfaces exist to ensure that those concerns remain separated.

---

# Conclusion

Query Surfaces are not merely a method of retrieving data.

They are a preservation boundary.

They allow evidence preservation architecture and evidence consumption architecture to evolve independently while remaining interoperable.

The purpose of Query Surfaces is not to simplify evidence.

The purpose of Query Surfaces is to expose preserved evidence safely.

The guiding principle is:

```text
Preserve broadly.

Expose narrowly.

Never collapse the evidence.
```

# Rationale

## Purpose

This namespace contains justification documents for major architectural, interoperability, persistence, discovery, and evidence-governance decisions within the Variant Database (VDB).

These documents explain why important design decisions were made and what capabilities those decisions were intended to preserve or enable.

Rationale documents serve as decision records for future maintainers, contributors, and downstream repositories.

---

## Relationship To Other Documentation

The VDB documentation hierarchy separates decisions from implementation.

```text
Architecture
    What exists?

Design
    How does it behave?

Implementation
    How is it realized?

Validation
    How is it verified?

Rationale
    Why was it chosen?
```

Rationale documents complement architectural and design documentation by preserving the reasoning behind major repository decisions.

---

## Current Documents

### TEP Justification

```text
vdb_tep_clinical_justification.md
vdb_tep_technical_justification.md
```

Explains why Transitional Evidence Products (TEPs) serve as the interoperability substrate of the repository ecosystem and how they support both present-day analysis and future reinterpretation.

### Persistence Justification

```text
vdb_persistence_justification.md
```

Explains why VDB functions as an evidence persistence layer rather than a transient reporting layer.

### Namespace Brokerage Justification

```text
vdb_namespace_brokerage_justification.md
```

Explains why VDB preserves and brokers identities rather than replacing producer-defined namespaces.

### Discovery Justification

```text
vdb_discovery_justification.md
```

Explains why evidence preservation, interoperability, and persistence are prerequisites for discovery-oriented reasoning.

### Query Surface Justification

```text
vdb_query_surface_justification.md
```

Explains why query surfaces are treated as discovery interfaces rather than simple database retrieval mechanisms.

---

## Intended Audience

This namespace is primarily intended for:

```text
ARCH

SAGE-VDB

DEX-VDB

future maintainers

future contributors

repository reviewers
```

These documents should be consulted when evaluating architectural changes, introducing new producer repositories, extending interoperability contracts, or revisiting foundational repository assumptions.

---

## Guiding Principle

VDB is built around a preservation-first philosophy.

Many repository decisions intentionally prioritize:

```text
evidence preservation

identity preservation

provenance preservation

future reinterpretation

cross-repository interoperability
```

over short-term convenience or aggressive evidence reduction.

The rationale namespace preserves the reasoning behind those decisions so that future development can distinguish deliberate doctrine from incidental implementation details.

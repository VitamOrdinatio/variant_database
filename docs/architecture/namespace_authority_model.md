# Namespace Authority Model

## Purpose

The purpose of this document is to define identity authority, namespace authority, canonical identity governance, and brokerage responsibilities within VDB.

The repository ecosystem contains multiple identity spaces, multiple namespace systems, and multiple evidence models.

Interoperability therefore requires a governed mechanism for relating identities without altering the meaning of upstream evidence.

This document establishes the authority boundaries that make such interoperability possible.

---

## Core Principle

Identity authority and semantic authority are not the same thing.

Producer repositories own semantic authority.

VDB owns namespace brokerage authority.

This distinction is foundational.

VDB exists to relate identities, not redefine biological meaning.

---

## Architectural Authority Chain

The ecosystem recognizes four distinct authority domains.

```text
Producer Truth
        ↓
TEP Transport
        ↓
Namespace Brokerage
        ↓
Discovery Consumption
```

Each domain possesses separate responsibilities.

---

## Producer Authority

Producer repositories remain authoritative for the evidence they generate.

Examples include:

```text
VAP
    Variant observations

GSC
    Semantic priors

Future RSP
    Functional observations

RDGP
    Reasoning outputs
```

Producer repositories determine:

* evidence meaning
* scoring logic
* evidence generation
* source-specific identifiers
* repository-specific semantics

Producer authority is never transferred to VDB.

---

## Transport Authority

Transport authority is provided through the Transitional Evidence Product (TEP) architecture.

TEPs preserve:

* payload semantics
* provenance
* topology
* transport identity

A TEP does not reinterpret evidence.

A TEP does not normalize evidence.

A TEP does not broker identities.

Its purpose is preservation and transport.

Transport authority therefore remains distinct from namespace authority.

---

## Namespace Brokerage Authority

VDB is the authoritative namespace broker of the ecosystem.

Its responsibilities include:

* identity reconciliation
* namespace resolution
* canonical identity assignment
* identity relationship management
* identity provenance preservation

Namespace brokerage exists because multiple repositories may legitimately describe the same biological entity using different identifiers.

Examples include:

```text
ENSG00000140521

HGNC:9175

NCBI:5424

POLG
```

These are not conflicting truths.

They are alternative identity representations.

VDB creates governed relationships among them.

---

## Discovery Authority

The discovery engine is not a namespace authority.

The discovery engine is a consumer of namespace authority.

Its responsibilities include:

* artifact profiling
* contract matching
* validation
* routing
* persistence-domain assignment

Discovery consumes canonical identity relationships after brokerage has occurred.

Discovery must not perform identity mutation.

Discovery must not redefine namespace relationships.

---

## Identity Spaces

The ecosystem contains multiple identity spaces.

Examples include:

```text
Variant Identity

Gene Identity

Transcript Identity

Phenotype Identity

Sample Identity

Disease Identity

Ontology Identity

Release Identity

Execution Identity

Transport Identity
```

These spaces are independent.

Interoperability should not require their collapse.

---

## Identity-Space Independence

Identity spaces are intentionally preserved.

Examples include:

```text
(sample_id, gene_id)

(phenotype, gene_id)

(variant_id)

(gsc_release_id, phenotype, gene_id)

(vap_run_id, sample_id)
```

These identities serve different purposes.

They should remain distinguishable throughout the ecosystem.

Identity brokerage creates relationships among identity spaces without erasing them.

---

## Canonical Identities

Canonical identities exist to support interoperability.

A canonical identity is a brokerage artifact.

A canonical identity is not biological truth.

For example:

```text
canonical_gene_id
```

does not replace:

```text
ENSG identifier
HGNC identifier
NCBI gene identifier
Gene symbol
```

Instead, it provides a stable reference point through which those identities may be related.

---

## Additive Normalization

All namespace normalization within VDB is additive.

Normalization must never erase source identities.

For every resolution event:

```text
Source Identity
        ↓
Canonical Relationship
        ↓
Canonical Identity
```

the original identifier must remain preserved and recoverable.

This requirement applies to all namespace systems.

---

## Resolution Events

Namespace resolution is treated as a first-class provenance activity.

Each resolution event should preserve:

```text
resolution_event_id

source_identifier

source_namespace

target_identifier

target_namespace

mapping_source

mapping_version

resolution_timestamp

mapping_status
```

Namespace resolution therefore becomes auditable and reproducible.

---

## Identity Relationship Graph

Namespace brokerage produces an identity relationship graph.

Examples include:

```text
Gene Symbol
        ↓

HGNC Identifier
        ↓

Ensembl Identifier
        ↓

NCBI Identifier
```

and

```text
Transcript
        ↓

Gene
        ↓

Variant
```

The graph captures relationships.

It does not replace participating identities.

---

## Namespace Uncertainty

Namespace uncertainty must remain visible.

Examples include:

```text
One-to-many mappings

Many-to-one mappings

Ambiguous mappings

Unresolved mappings

Version-dependent mappings
```

VDB must preserve uncertainty rather than conceal it.

Additive normalization enables ambiguity to remain detectable.

---

## Overlay Identity Governance

Semantic overlays introduce additional namespace requirements.

Examples include:

```text
(gsc_release_id,
 phenotype,
 canonical_gene_id)
```

Overlay identities remain distinct from:

```text
Variant identities

Sample identities

Observation identities
```

Overlay persistence therefore requires independent identity governance.

---

## Persistence and Namespace Authority

Persistence domains consume namespace authority.

Persistence domains do not create namespace authority.

This distinction is important.

Namespace brokerage determines identity relationships.

Persistence domains determine evidence organization.

The two systems cooperate but remain independent.

---

## Discovery and Namespace Authority

Discovery consumes namespace authority through canonical identities.

The workflow is:

```text
TEP Arrival
        ↓

Discovery / Profiling
        ↓

Namespace Brokerage
        ↓

Canonical Relationships
        ↓

Discovery Routing
        ↓

Persistence
```

Initial discovery determines what the artifact appears to contain.

Namespace brokerage determines how identities relate.

Discovery routing then uses brokered identity relationships to support deterministic persistence decisions.

This ordering ensures that discovery remains deterministic and identity-aware without becoming an identity-authority system.

---

## Future Namespace Expansion

The model intentionally supports future namespace systems.

Examples include:

```text
Future RSP identifiers

Ontology identifiers

Protein identifiers

Pathway identifiers

Cell-state identifiers

Functional module identifiers
```

New namespace systems should integrate through brokerage rather than architectural redesign.

---

## Authority Boundaries

The ecosystem therefore recognizes the following authority model:

```text
Producer Repositories
        Own Meaning

TEP
        Owns Transport

Namespace Brokerage
        Owns Relationships

Discovery
        Consumes Relationships

Persistence
        Organizes Evidence

RDGP
        Consumes Evidence
```

This separation prevents authority drift and preserves explainability.

---

## Summary

VDB functions as the namespace brokerage authority of the repository ecosystem.

Producer repositories remain authoritative for biological meaning.

TEPs remain authoritative for transport.

Discovery remains authoritative for governance-driven routing.

Namespace brokerage provides the additive identity relationships that allow these systems to interoperate.

Canonical identities are brokerage artifacts rather than biological-truth artifacts.

Through additive normalization, provenance-preserving resolution events, and identity-space independence, VDB enables interoperability without sacrificing semantic meaning, provenance integrity, or future interpretability.

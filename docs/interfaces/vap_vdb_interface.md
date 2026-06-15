# VAP ↔ VDB Interface

## Purpose

This document defines the interoperability contract governing evidence exchange between VAP (Variant Annotation Pipeline) and VDB (Variant Database).

The interface establishes:

* evidence ownership boundaries
* transport responsibilities
* persistence expectations
* provenance requirements
* identity-preservation requirements

The purpose of the interface is to ensure that VAP-produced evidence can enter VDB without loss of meaning, provenance, or future interpretability.

---

# Interface Overview

```text
     VAP
      ↓
TEP Transport
      ↓
     VDB
```

VAP produces evidence.

TEP transports evidence.

VDB persists evidence.

Each system owns distinct responsibilities.

---

# Ownership Boundaries

## VAP Responsibilities

VAP owns:

* execution
* annotation
* evidence generation
* run-scoped provenance
* source artifact creation
* source package identity

Examples include:

```text
vap_run_id

sample_id

variant observations

annotation outputs

pipeline metadata

stage outputs
```

VAP remains authoritative for the evidence it produces.

---

## TEP Responsibilities

TEP owns transport governance.

TEP preserves:

* evidence topology
* provenance topology
* reasoning topology
* source package identity
* transport identity

TEP does not reinterpret evidence.

---

## VDB Responsibilities

VDB owns:

* discovery
* identity brokerage
* semantic persistence
* query-surface generation

VDB does not become authoritative for VAP execution products.

VAP remains the source authority.

---

# Interface Inputs

The VAP → VDB interface consumes transported VAP evidence.

Transport should occur through:

```text
TEP
```

The TEP serves as the authoritative transport artifact.

Raw producer outputs should not be interpreted as direct persistence contracts.

---

# Evidence Classes

The interface supports transport of VAP-derived evidence classes.

Examples include:

```text
variant observations

variant annotations

transcript consequences

population-frequency annotations

clinical annotations

quality annotations

reviewability annotations

provenance artifacts
```

The interface should remain extensible.

Future evidence classes may be added without redesigning the interface.

---

# Identity Preservation Requirements

The interface must preserve source identities.

Examples include:

```text
sample_id

vap_run_id

source_package_id

variant identifiers

transcript identifiers

annotation identifiers
```

VDB may establish canonical relationships.

VDB must not erase source identities.

---

# Provenance Requirements

The interface must preserve provenance sufficient to reconstruct:

```text
source repository

source package

source artifact

execution lineage

transport lineage

ingestion lineage
```

Provenance should remain queryable after persistence.

---

# Variant Evidence Requirements

Variant evidence is a first-class persistence target.

The interface must preserve:

* variant observations
* variant multiplicity
* allele relationships
* annotation relationships
* transcript relationships

The interface must not collapse variant evidence into summary-only representations.

---

# Transcript Preservation Requirements

Transcript context must remain preserved.

Examples include:

```text
transcript consequence

transcript-specific annotation

transcript-specific interpretation
```

Transcript information should remain recoverable after persistence.

---

# Annotation Preservation Requirements

VAP annotations should remain preserved.

Examples include:

```text
functional annotation

clinical annotation

frequency annotation

quality annotation

reviewability annotation
```

Annotations should remain attributable to their originating evidence.

---

# Noncoding Evidence Requirements

Noncoding evidence is first-class evidence.

The interface must not assume:

```text
coding evidence > noncoding evidence
```

Noncoding observations should remain transportable, persistable, and queryable.

---

# Multiplicity Preservation Requirements

The interface must preserve evidence multiplicity.

Examples include:

```text
multiple annotations

multiple transcripts

multiple interpretations

multiple evidence relationships
```

Multiplicity should remain detectable.

---

# Semantic Preservation Requirements

VDB should preserve evidence meaning.

Persistence should not require premature reduction of:

* annotation richness
* transcript richness
* provenance richness
* uncertainty information

Future reinterpretability is a primary requirement.

---

# Discovery Expectations

Following ingestion, VDB discovery processes may characterize incoming evidence.

Examples include:

```text
artifact profiling

domain classification

identity detection

routing classification
```

Discovery does not alter source authority.

---

# Namespace Brokerage Expectations

Following discovery, VDB may establish canonical identity relationships.

Examples include:

```text
source transcript ↔ canonical transcript

source gene ↔ canonical gene
```

Namespace brokerage is additive.

Source identities remain preserved.

---

# Persistence Expectations

VDB should organize evidence according to semantic persistence doctrine.

Persistence organization should not be determined by repository ownership.

Evidence should remain queryable through stable query surfaces.

---

# Interface Guarantees

The interface guarantees:

* source identity preservation
* provenance preservation
* transcript preservation
* annotation preservation
* multiplicity preservation
* future reinterpretability
* additive namespace brokerage
* transport-safe evidence exchange

---

# Failure Conditions

The interface should reject workflows that require:

* source identity erasure
* provenance loss
* transcript loss
* annotation loss
* ambiguity concealment
* destructive normalization
* irreversible evidence compression

Such behaviors violate interface doctrine.

---

# Relationship to Constitutional Doctrine

This interface derives authority from:

* ecosystem identity governance
* TEP transport governance
* VDB semantic persistence governance

The interface expresses those principles specifically for VAP-produced evidence.

---

# Summary

The VAP ↔ VDB interface defines how VAP-produced evidence enters VDB while preserving identity, provenance, transcript context, annotation richness, multiplicity, and future interpretability.

VAP remains authoritative for evidence production.

TEP remains authoritative for transport.

VDB remains authoritative for discovery, identity brokerage, semantic persistence, and query-surface exposure.

The interface therefore enables durable evidence persistence without loss of biological meaning.

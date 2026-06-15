# GSC ↔ VDB Interface

## Purpose

This document defines the interoperability contract governing evidence exchange between GSC (Gene Set Consensus) and VDB (Variant Database).

The interface establishes:

* semantic-prior persistence responsibilities
* phenotype-scope preservation requirements
* release-preservation requirements
* provenance requirements
* identity-preservation requirements
* downstream attachability requirements

The purpose of the interface is to ensure that GSC-produced semantic evidence can enter VDB without loss of phenotype context, release identity, provenance, or future interpretability.

---

# Interface Overview

```text
     GSC
      ↓
TEP Transport
      ↓
     VDB
```

GSC produces semantic evidence.

TEP transports semantic evidence.

VDB persists semantic evidence.

Each system owns distinct responsibilities.

---

# Ownership Boundaries

## GSC Responsibilities

GSC owns:

* semantic scoring
* evidence-source integration
* consensus generation
* phenotype selection
* release construction
* release provenance

Examples include:

```text
gsc_release_id

phenotype

gene evidence

consensus scores

source evidence

semantic channels
```

GSC remains authoritative for semantic meaning.

---

## TEP Responsibilities

TEP owns transport governance.

TEP preserves:

* evidence topology
* provenance topology
* reasoning topology
* release identity
* transport identity

TEP does not reinterpret semantic evidence.

---

## VDB Responsibilities

VDB owns:

* discovery
* identity brokerage
* semantic persistence
* query-surface generation

VDB does not recompute GSC consensus.

GSC remains authoritative for semantic scoring.

---

# Interface Inputs

The GSC → VDB interface consumes transported GSC evidence.

Transport should occur through:

```text
TEP
```

The TEP serves as the authoritative transport artifact.

---

# Semantic Prior Evidence

The interface exists to persist semantic priors.

Examples include:

```text
phenotype-gene relationships

consensus evidence

curated evidence

knowledge-layer evidence

release-scoped semantic support
```

These artifacts represent semantic evidence rather than biological observations.

---

# Identity Model

The primary GSC identity model is:

```text
(phenotype, gene_id)
```

This identity space is distinct from:

```text
(sample_id, gene_id)

variant_id

transcript_id
```

Identity spaces must remain distinguishable after persistence.

---

# Release Identity Preservation

Release identity is first-class evidence.

Examples include:

```text
gsc_release_id

release provenance

release version

release construction context
```

Release identity must remain queryable.

Release identity must not be reduced to metadata-only status.

---

# Phenotype Scope Preservation

Phenotype context is a first-class component of GSC evidence.

Examples include:

```text
epilepsy

mitochondrial disease

future phenotype domains
```

Phenotype context must remain explicit.

Persistence must not collapse:

```text
(phenotype, gene_id)
```

into:

```text
(gene_id)
```

alone.

---

# Semantic Channel Preservation

The interface must preserve semantic channels.

Examples include:

```text
source support

consensus support

evidence classifications

future evidence channels
```

Semantic richness should remain queryable.

---

# Provenance Requirements

The interface must preserve provenance sufficient to reconstruct:

```text
source repository

source package

source release

source evidence

transport lineage

ingestion lineage
```

Provenance should remain recoverable after persistence.

---

# Ontology Resolution Expectations

GSC evidence may contain heterogeneous source identifiers.

Examples include:

```text
HGNC identifiers

NCBI identifiers

Ensembl identifiers

future ontology identifiers
```

VDB may establish canonical relationships.

Source identifiers must remain recoverable.

Namespace normalization must remain additive.

---

# Semantic Overlay Expectations

GSC evidence should remain attachable.

Persistence should support future overlay workflows.

Examples include:

```text
phenotype overlays

gene overlays

semantic enrichment workflows
```

Attachability is a primary persistence objective.

---

# Overlay Preservation Requirements

The interface must preserve:

* phenotype scope
* release identity
* semantic channels
* provenance lineage
* ontology relationships

Overlay meaning should remain intact after persistence.

---

# Discovery Expectations

Following ingestion, VDB discovery processes may characterize incoming semantic evidence.

Examples include:

```text
artifact profiling

release profiling

identity detection

routing classification
```

Discovery does not alter GSC authority.

---

# Namespace Brokerage Expectations

Following discovery, VDB may establish canonical identity relationships.

Examples include:

```text
NCBI Gene ID ↔ Canonical Gene ID

Ensembl Gene ID ↔ Canonical Gene ID
```

Brokerage relationships are additive.

Source identities remain authoritative.

---

# Persistence Expectations

VDB should persist GSC evidence according to semantic persistence doctrine.

Persistence should preserve:

* release identity
* phenotype identity
* semantic channels
* provenance
* ontology relationships

Repository ownership should not determine persistence structure.

---

# Attachability Expectations

Persisted GSC evidence should remain attachable to future consumers.

Examples include:

```text
RDGP

future RSP consumers

future query surfaces

future discovery workflows
```

Attachment methods should remain explainable and reproducible.

---

# Interface Guarantees

The interface guarantees:

* release preservation
* phenotype preservation
* provenance preservation
* semantic-channel preservation
* additive namespace brokerage
* transport-safe semantic persistence
* future attachability

---

# Failure Conditions

The interface should reject workflows that require:

* release identity loss
* phenotype identity loss
* semantic-channel loss
* provenance loss
* destructive normalization
* irreversible semantic compression
* recomputation of GSC consensus inside VDB

Such behaviors violate interface doctrine.

---

# Relationship to Constitutional Doctrine

This interface derives authority from:

* ecosystem identity governance
* semantic-overlay governance
* TEP transport governance
* VDB semantic persistence governance

The interface expresses those principles specifically for GSC-produced semantic evidence.

---

# Summary

The GSC ↔ VDB interface defines how phenotype-scoped semantic evidence enters VDB while preserving release identity, phenotype context, semantic richness, provenance, ontology relationships, and future attachability.

GSC remains authoritative for semantic meaning.

TEP remains authoritative for transport.

VDB remains authoritative for discovery, identity brokerage, semantic persistence, and query-surface exposure.

The interface therefore enables durable persistence of semantic priors without loss of biological context, release provenance, or future interoperability.

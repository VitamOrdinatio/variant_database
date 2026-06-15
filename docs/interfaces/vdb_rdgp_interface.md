# VDB ↔ RDGP Interface

## Purpose

This document defines the interoperability contract governing evidence exchange between VDB (Variant Database) and RDGP (Rare Disease Gene Prioritization).

The interface establishes:

* evidence-consumption responsibilities
* aggregation responsibilities
* query-surface expectations
* overlay-attachment expectations
* provenance requirements
* identity-preservation requirements

The purpose of the interface is to ensure that VDB-resident evidence can be consumed by RDGP without loss of provenance, uncertainty, identity context, or future interpretability.

---

# Interface Overview

```text
   VDB
    ↓
Query Surfaces
    ↓
   RDGP
```

VDB persists evidence.

RDGP consumes evidence.

VDB does not perform prioritization.

RDGP does not own evidence persistence.

Each system owns distinct responsibilities.

---

# Ownership Boundaries

## VDB Responsibilities

VDB owns:

* evidence persistence
* discovery
* namespace brokerage
* semantic persistence
* query-surface generation
* overlay persistence

Examples include:

```text
variant evidence

transcript evidence

gene evidence

phenotype overlays

provenance records

namespace relationships
```

VDB remains authoritative for persisted evidence.

---

## RDGP Responsibilities

RDGP owns:

* evidence interpretation
* candidate generation
* prioritization
* confidence modeling
* inheritance reasoning
* future reasoning frameworks

Examples include:

```text
candidate scores

candidate rankings

confidence assignments

inheritance assessments

prioritized_genes.tsv
```

RDGP remains authoritative for reasoning outputs.

---

# Architectural Separation

The interface preserves the following architectural boundary:

```text
 VDB = Evidence Persistence

RDGP = Evidence Reasoning
```

The interface exists to prevent reasoning logic from leaking into persistence and persistence concerns from leaking into reasoning.

---

# Interface Inputs

The VDB → RDGP interface exposes evidence through query surfaces.

RDGP should consume queryable evidence representations rather than direct persistence structures.

Query surfaces form the stability boundary between VDB and RDGP.

---

# Primary Identity Model

The primary RDGP identity model is:

```text
(sample_id, gene_id)
```

This identity space is distinct from:

```text
variant_id

transcript_id

(phenotype, gene_id)

gsc_release_id
```

Identity-space boundaries must remain visible.

---

# Aggregation Responsibilities

Aggregation is a required VDB responsibility.

RDGP consumes gene-level evidence.

VDB persists evidence across multiple identity spaces.

Therefore VDB must provide aggregation pathways that support RDGP consumption.

Examples include:

```text
variant → gene

transcript → gene

annotation → gene
```

Aggregation does not perform reasoning.

Aggregation prepares evidence for consumption.

---

# Variant Evidence Requirements

RDGP must be able to trace gene-level evidence back to underlying variants.

The interface should preserve:

* variant observations
* variant annotations
* transcript consequences
* provenance relationships
* uncertainty states

Gene-level representations must remain reproducible from underlying evidence.

---

# Sample-Gene Evidence Surfaces

The primary v1 consumption surface is:

```text
(sample_id, gene_id)
```

This surface may contain:

* variant-derived evidence
* annotation-derived evidence
* provenance summaries
* evidence-channel summaries
* uncertainty summaries

The surface should remain explainable.

---

# Overlay Attachment Expectations

VDB may expose semantic overlays derived from GSC.

Examples include:

```text
(phenotype, canonical_gene_id)
```

relationships.

RDGP may consume overlay-enriched evidence surfaces.

Overlay attachment must remain explicit and reproducible.

---

# Identity-Space Bridging

The interface supports identity-space bridging.

Examples include:

```text
(sample_id, gene_id)
        +
(phenotype, gene_id)
```

Bridging should remain traceable.

Identity spaces must not collapse into one another.

Phenotype-scoped evidence remains distinct from sample-scoped evidence.

---

# Overlay Governance

Overlay evidence is enrichment evidence.

Overlay evidence is not sample evidence.

Overlay absence is not negative evidence.

Overlay presence is not deterministic proof.

RDGP remains responsible for interpreting overlay significance.

---

# Provenance Requirements

The interface must preserve provenance sufficient to reconstruct:

```text
source repository

source package

source artifact

TEP lineage

ingestion lineage

namespace-resolution lineage

aggregation lineage

overlay-attachment lineage
```

Evidence should remain auditable.

---

# Uncertainty Preservation Requirements

The interface must preserve uncertainty.

Examples include:

```text
missing annotations

ambiguous mappings

unresolved identities

conflicting evidence

incomplete evidence
```

Uncertainty should remain visible.

RDGP should not be forced to infer uncertainty from absence.

---

# Evidence Channel Preservation

Evidence channels should remain separable.

Examples include:

```text
variant evidence

annotation evidence

semantic prior evidence

future functional evidence

future expression evidence
```

Channel separation supports explainable reasoning.

---

# Namespace Brokerage Expectations

RDGP consumes namespace-brokered evidence.

Canonical identities may support interoperability.

However:

* source identities remain recoverable
* brokerage remains additive
* normalization remains traceable

Identity authority remains external to RDGP.

---

# Query Surface Expectations

Query surfaces should provide:

* stable access paths
* reproducible aggregation
* provenance visibility
* overlay attachability
* uncertainty visibility

Consumers should not depend directly upon persistence layouts.

---

# Future Functional Evidence Support

The interface should support future evidence classes.

Examples include:

```text
RSP expression evidence

pathway evidence

functional evidence

cross-modal evidence
```

Future evidence classes should integrate through query-surface extension rather than interface redesign.

---

# Bidirectional Evidence Lifecycle

The VDB ↔ RDGP interface is bidirectional.

Initial evidence consumption typically follows:

```text
VDB → RDGP
```

through RDGP-oriented query surfaces.

However, RDGP may subsequently generate new evidence products.

Examples include:

* candidate rankings
* confidence assessments
* inheritance interpretations
* reasoning outputs
* future statistical analyses
* future functional interpretations

These outputs should be treated as evidence products rather than persistence-layer updates.

Recommended lifecycle:

```text
     VDB
      ↓
   VDB-TEP
      ↓
     RDGP
      ↓
RDGP Reasoning
      ↓
   RDGP-TEP
      ↓
     VDB
```

In this model, RDGP-derived outputs become a new evidence class persisted by VDB.

Reasoning products should remain attributable to:

* source RDGP release
* source RDGP methodology
* source evidence inputs
* reasoning provenance
* temporal context

RDGP outputs must not overwrite underlying evidence.

Instead, they should coexist alongside:

* observed evidence
* semantic prior evidence
* historical reasoning evidence

This architecture allows future consumers to evaluate both evidence and reasoning across time.

The interface therefore supports iterative refinement while preserving historical reproducibility and clinical interpretability.

---

# Interface Guarantees

The interface guarantees:

* evidence provenance preservation
* identity preservation
* uncertainty preservation
* overlay attachability
* aggregation reproducibility
* stable query surfaces
* additive namespace brokerage
* future extensibility

---

# Failure Conditions

The interface should reject workflows that require:

* provenance loss
* source identity erasure
* hidden aggregation
* hidden overlay attachment
* uncertainty concealment
* destructive normalization
* irreversible evidence compression

Such behaviors violate interface doctrine.

---

# Relationship to Constitutional Doctrine

This interface derives authority from:

* ecosystem identity governance
* TEP transport governance
* semantic persistence governance
* identity-space governance
* query-surface governance

The interface expresses those principles specifically for RDGP-facing evidence consumption.

---

# Summary

The VDB ↔ RDGP interface defines how persisted evidence becomes consumable by RDGP while preserving provenance, uncertainty, identity relationships, overlay context, and future interpretability.

VDB remains authoritative for evidence persistence.

RDGP remains authoritative for evidence reasoning.

Aggregation, overlay attachment, and query-surface generation provide the bridge between these responsibilities without collapsing identity spaces or obscuring evidence lineage.

The interface therefore enables explainable gene prioritization while preserving the integrity of the underlying evidence ecosystem.

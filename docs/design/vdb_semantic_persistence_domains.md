# VDB Semantic Persistence Domains

## Purpose

This document defines the semantic persistence philosophy underlying the Variant Database (VDB).

VDB is not intended to function as:

* a flat-file archive
* a monolithic variant table
* a simple TSV warehouse
* a passive storage layer

Instead, VDB serves as the governed evidence nexus for the broader repository ecosystem.

Its role is to persist, normalize, relate, and expose semantically distinct biological evidence domains originating from multiple upstream repositories.

---

# Core Principle

The foundational principle is:

```text
repo ownership != table granularity
```

Repositories emit semantically distinct evidence classes.

Therefore, VDB persistence structure should be driven by semantic evidence domains rather than repository boundaries alone.

Incorrect conceptual model:

```text
VAP → vap_table
GSC → gsc_table
RSP → rsp_table
RDGP → rdgp_table
```

Preferred conceptual model:

```text
VAP → multiple semantic evidence domains
GSC → multiple semantic evidence domains
RSP → multiple semantic evidence domains
RDGP → derived reasoning/result domains
```

This distinction is critical for preserving:

* provenance continuity
* relational flexibility
* interoperability
* auditability
* downstream query power
* future ecosystem expansion

---

# VDB Roles in the Ecosystem

VDB occupies four primary architectural roles.

| Role                   | Meaning                                        |
| ---------------------- | ---------------------------------------------- |
| persistence layer      | durable evidence storage                       |
| namespace authority    | identity normalization and arbitration         |
| interoperability nexus | ecosystem substrate exchange                   |
| query substrate        | stable analytical views for downstream systems |

---

# Persistence Layer

VDB persists biological evidence in normalized relational form.

Persistence responsibilities include:

* variant observations
* annotations
* semantic partitions
* metadata
* provenance
* telemetry
* overlay evidence
* expression evidence
* downstream reasoning artifacts

Persistence should preserve both:

* normalized canonical representations
* raw source lineage

The goal is durable evidence retention without silent semantic collapse.

---

# Namespace Authority

VDB acts as the ecosystem authority for identity normalization.

This includes:

* gene namespace normalization
* alias preservation
* identifier arbitration
* mapping provenance
* ambiguous identity tracking
* unresolved-state preservation

Likely namespace domains include:

| Domain              | Examples                           |
| ------------------- | ---------------------------------- |
| gene identifiers    | HGNC, Ensembl, Entrez              |
| variant identifiers | chromosome-position-ref-alt, dbSNP |
| sample identifiers  | sample_id, BioSample               |
| run identifiers     | VAP run_id, SRA run accession      |
| project identifiers | BioProject accession               |
| assay identifiers   | WES, WGS, RNAseq                   |

VDB should preserve both:

* canonical identities
* source-native identities

No silent namespace collapse should occur.

---

# Interoperability Nexus

VDB serves as the controlled evidence exchange layer for the broader ecosystem.

Example ecosystem flow:

```text
VAP
  ↓
VDB
  ↓
RDGP

GSC
  ↓
VDB
  ↓
overlay attachment

RSP
  ↓
VDB
  ↓
functional evidence integration
```

The database therefore becomes the shared semantic substrate layer connecting otherwise independent repositories.

---

# Query Substrate

VDB should expose stable query surfaces rather than forcing downstream systems to reconstruct complex joins repeatedly.

Examples:

* `(sample_id, gene_id)` RDGP evidence views
* validation-ready candidate views
* coding-only evidence views
* noncoding evidence views
* cohort-level summaries
* BioProject-stratified summaries
* GSC overlay attachment views
* expression-linked variant evidence views
* provenance-aware audit views

This allows downstream repositories to consume governed evidence surfaces without duplicating normalization logic.

---

# Semantic Persistence Domains

Each upstream repository naturally emits multiple semantic persistence domains.

These domains often deserve dedicated relational representation within VDB.

---

# VAP Persistence Domains

VAP naturally emits several distinct evidence domains.

Representative examples include:

1. variant observations
2. normalized variants
3. annotations
4. gene mappings
5. semantic partitions
6. coding interpretation substrates
7. noncoding interpretation substrates
8. prioritization outputs
9. validation candidate outputs
10. provenance artifacts
11. runtime telemetry
12. run metadata
13. stage summaries

These domains should not necessarily collapse into a single universal variant table.

Different downstream analytical questions require different evidence surfaces.

---

# GSC Persistence Domains

GSC naturally emits:

1. phenotype-gene priors
2. source provenance
3. evidence aggregation summaries
4. overlay-compatible gene evidence
5. source weighting metadata
6. confidence or tier structures

These are conceptually distinct from variant observations and should remain independently queryable.

---

# RSP Persistence Domains

RSP may eventually emit:

1. expression signals
2. DEG summaries
3. pathway enrichment evidence
4. network support evidence
5. transcript-level metadata
6. assay metadata
7. cohort-level expression summaries

These are functional evidence layers rather than variant-centric evidence layers.

---

# RDGP Persistence Domains

RDGP likely emits:

1. `(sample_id, gene_id)` ranking outputs
2. confidence summaries
3. explanation artifacts
4. scoring provenance
5. uncertainty states
6. inheritance reasoning outputs
7. evidence aggregation traces

These are derived reasoning domains rather than primary biological evidence domains.

---

# Persistence Domains vs Source Repositories

Persistence domains should not be interpreted as strict ownership silos.

Instead:

```text
repositories produce evidence
VDB organizes evidence semantically
```

This allows:

* cross-repository joins
* layered evidence integration
* future ecosystem expansion
* metadata harmonization
* ontology-aware querying

without collapsing biological meaning.

---

# Relationship to Discovery Engine

The VDB discovery engine determines which semantic persistence domain an incoming artifact belongs to.

Workflow:

```text
artifact
→ discovery/profile
→ governance mapping
→ semantic persistence domain
→ normalized ingestion
→ query exposure
```

This prevents arbitrary or accidental ingestion into incorrect relational structures.

The discovery engine therefore acts as the control-plane for persistence governance.

---

# Example Persistence Architecture

Illustrative example relational domains:

```text
samples
runs
source_artifacts
variant_observations
variant_annotations
gene_identity
gene_aliases
semantic_partitions
coding_interpretation
noncoding_interpretation
phenotype_gene_priors
expression_signals
rdgp_gene_rankings
runtime_metadata
stage_metrics
ingestion_events
```

Not all domains require fully separate tables in v1.

Some may initially exist as:

* staging tables
* normalized views
* intermediate representations
* controlled denormalized surfaces

The key principle is semantic separation, not maximal fragmentation.

---

# Persistence Granularity

Over-normalization can become as problematic as under-normalization.

VDB should therefore pursue:

```text
semantic normalization
```

rather than:

```text
maximal theoretical normalization
```

The goal is practical interoperability and auditability.

Not relational purity for its own sake.

---

# Provenance Preservation

Every persistence domain should preserve:

* source repository
* source artifact
* run identity
* schema version
* ingestion timestamp
* source-native identifiers
* normalization mappings
* transformation lineage

No evidence should become detached from its origin.

---

# Query-Oriented Design

Persistence domains should support downstream biological reasoning.

Example queries may include:

```text
Which coding variants survived prioritization in females from a specific BioProject?

Which variants map to genes with strong GSC epilepsy priors?

Which validation-ready candidates overlap expression-supported genes?

Which Stage 08 semantic partitions produced downstream RDGP Tier 1 genes?

Which variants repeatedly appear across heterogeneous runs?
```

The VDB schema should support such questions naturally.

---

# Avoiding Adapter Sprawl

A major design objective is preventing uncontrolled proliferation of custom one-off ingestion adapters.

Preferred architecture:

```text
thin adapter
→ standardized discovery profile
→ governance mapping
→ semantic persistence domain
→ deterministic ingestion
```

Adapters should perform only minimal source-specific extraction.

Semantic interpretation belongs within governed normalization layers.

---

# v1 Scope Recommendation

Recommended VDB v1 scope:

* VAP run-package ingestion
* semantic persistence domain mapping
* namespace normalization
* metadata normalization
* provenance preservation
* discovery-engine integration
* query-view generation
* RDGP-oriented evidence views
* GSC overlay attachment
* BioProject/SRA metadata support

Defer to later releases:

* large-scale ontology engines
* distributed query systems
* graph database layers
* advanced probabilistic schema inference
* ML-driven semantic discovery
* fully automated ontology reconciliation

---

# Summary

VDB should organize evidence according to semantic persistence domains rather than repository-level ownership alone.

This allows the ecosystem to preserve:

* provenance continuity
* semantic clarity
* interoperability
* downstream reasoning flexibility
* auditability
* normalization integrity

Repositories emit evidence.

VDB governs and persists evidence semantically.

That distinction is foundational to the architecture.

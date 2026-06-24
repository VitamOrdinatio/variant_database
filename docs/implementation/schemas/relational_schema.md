# relational_schema.md

## Purpose

The VDB Relational Schema defines the logical relational domains used to persist, organize, relate, and query evidence preserved within the Variant Database (VDB).

The Relational Schema is derived from:

```text
metadata_schema.md
provenance_schema.md
data_schema.md
```

The Relational Schema does not redefine metadata, provenance, or biological evidence.

Instead, it provides the relational architecture through which those concepts become persistable and queryable.

---

# Scope

The Relational Schema governs:

```text
logical relational domains
relational relationships
primary identities
foreign relationships
cross-domain associations
brokerage structures
query-surface foundations
```

The Relational Schema does not govern:

```text
specific SQL dialects
physical database engines
index implementations
query optimization strategies
```

These implementation details may evolve independently.

---

# Core Principle

## Relational Persistence Is Not Semantic Compression

The purpose of the Relational Schema is:

```text
preserve evidence meaning
```

not:

```text
flatten evidence into tables
```

The Relational Schema must preserve:

```text
metadata
provenance
evidence states
producer topology
```

without semantic collapse.

---

# Design Principles

## Logical Domains Before Physical Tables

The Relational Schema defines logical domains first.

Physical table implementations are secondary.

This ensures:

```text
DuckDB
PostgreSQL
future storage engines
```

can implement the architecture without changing its meaning.

---

## Preservation Before Convenience

Relational structures must preserve evidence.

Query convenience is secondary.

---

## Producer-Native Preservation

Producer-specific evidence models remain visible.

Examples:

```text
VAP evidence lifecycle

GSC semantic-prior topology
```

must not be collapsed into a common evidence table.

---

## Additive Integration

VDB may create relationships between evidence domains.

VDB must not replace producer-defined meaning.

---

# Layer 0 — Evidence Object Model

Layer 0 defines the conceptual evidence architecture underlying all producer repositories.

---

## Authority Classification Domain

Authority classification is a first-class relational concept.

Supported authority classes include:

```text
producer_authoritative
external_authority
vdb_discovered_external
vdb_inferred
user_supplied
derived_query_surface
unknown_authority
```

Authority classification may apply to:

```text
evidence objects
evidence states
external capsules
attachments
query surfaces
```

Authority classes supplement provenance.

Authority classes do not replace provenance.

---

## Evidence Object Domain

Represents a durable evidence-bearing object.

Examples:

```text
variant evidence object

semantic prior evidence object

future transcriptomic evidence object

future reasoning evidence object
```

Required identity:

```text
evidence_object_id
evidence_object_type
producer_id
```

Evidence Objects are the primary biological entities recognized by VDB.

---

## Evidence State Domain

Represents a specific state of an Evidence Object.

Examples:

```text
observation state

normalization state

coding interpretation state

prioritization state

semantic contribution state

consensus state
```

Required identity:

```text
evidence_state_id
evidence_object_id
state_type
```

Evidence States preserve evidence evolution.

---

## Evidence State Transition Domain

Represents movement between states.

Examples:

```text
observation
    →
normalization

normalization
    →
interpretation

contribution
    →
consensus
```

Required identity:

```text
transition_id
source_state_id
target_state_id
transition_type
```

Evidence State Transitions preserve evidence flow.

---

# Layer 1 — Preservation Registry

Layer 1 persists transport and preservation structures.

---

## Producer Domain

Represents producer repositories.

Logical objects:

```text
producer
producer_version
```

---

## Release Domain

Represents producer releases.

Logical objects:

```text
release
release_version
```

---

## Run Domain

Represents producer execution instances.

Logical objects:

```text
run
run_context
```

---

## TEP Package Domain

Represents transport packages.

Logical objects:

```text
tep_package
tep_family
tep_schema_version
```

---

## Artifact Domain

Represents package artifacts.

Logical objects:

```text
artifact
artifact_signature
artifact_checksum
```

---

## Entity Domain

Represents semantic package entities.

Examples:

```text
observation

normalization

semantic_prior

source_contribution
```

Logical objects:

```text
entity
entity_type
entity_role
```

---

## Manifest Domain

Represents package inventories.

Logical objects:

```text
manifest
manifest_entry
```

---

## Validation Domain

Represents validation metadata.

Logical objects:

```text
validation_state
validation_event
```

---

## Ingestion Domain

Represents VDB acquisition activities.

Logical objects:

```text
ingestion_event
schema_binding
```

---

# Layer 2 — Producer-Native Evidence Domains

Layer 2 preserves biological evidence in producer-native form.

---

# VAP Evidence Domains

## Variant Observation Domain

Logical object:

```text
vap_variant_observation
```

Represents observed variants.

---

## Variant Normalization Domain

Logical object:

```text
vap_variant_normalization
```

Represents normalized variant representations.

---

## Routing Domain

Logical object:

```text
vap_variant_routing
```

Represents evidence routing state.

---

## Coding Interpretation Domain

Logical object:

```text
vap_coding_interpretation
```

Represents coding-region interpretation overlays.

---

## Noncoding Interpretation Domain

Logical object:

```text
vap_noncoding_interpretation
```

Represents noncoding interpretation overlays.

---

## Prioritization Domain

Logical object:

```text
vap_prioritization_overlay
```

Represents prioritization states.

---

## Validation Domain

Logical object:

```text
vap_validation_overlay
```

Represents validation-oriented states.

---

## Context Domain

Logical object:

```text
vap_context_summary
```

Represents contextual summaries.

---

# GSC Evidence Domains

## Semantic Prior Domain

Logical object:

```text
gsc_semantic_prior
```

Represents phenotype-gene semantic priors.

---

## Gene Identity Domain

Logical object:

```text
gsc_gene_identity
```

Represents gene identity structures.

---

## Scoring Domain

Logical object:

```text
gsc_scoring_profile
```

Represents semantic scoring outputs.

---

## Semantic Channel Domain

Logical object:

```text
gsc_semantic_channel
```

Represents channel decomposition.

---

## Source Contribution Domain

Logical object:

```text
gsc_source_contribution
```

Represents source contribution topology.

---

## Gene Provenance Domain

Logical object:

```text
gsc_gene_provenance
```

Represents provenance-aware gene support structures.

---

## Uncertainty Domain

Logical object:

```text
gsc_uncertainty_state
```

Represents uncertainty structures.

---

# Future Producer Domains

The Relational Schema anticipates future repositories.

Examples:

```text
rsp_expression_observation

rsp_expression_interpretation

rdgp_reasoning_input

rdgp_reasoning_state

rdgp_prioritization_output
```

Future domains must be additive.

---

# Layer 3 — Namespace Brokerage

Layer 3 preserves identity resolution without replacing source identities.

---

## Source Identifier Domain

Logical object:

```text
source_identifier
```

Represents producer-defined identities.

Examples:

```text
gene symbols
Ensembl identifiers
HGNC identifiers
variant identifiers
phenotype identifiers
```

---

## Canonical Identifier Domain

Logical object:

```text
canonical_identifier
```

Represents VDB-resolved identities.

Canonical identities supplement source identities.

They do not replace them.

---

## Identifier Mapping Domain

Logical object:

```text
identifier_mapping
```

Represents source-to-canonical relationships.

---

## Namespace Resolution Domain

Logical object:

```text
namespace_resolution_event
```

Represents brokerage activities.

---

## Identity Bridge Domains

Logical objects:

```text
gene_identity_bridge

variant_identity_bridge

phenotype_identity_bridge

locus_identity_bridge
```

These structures enable cross-producer integration.

---

# Layer 4 — Query Surfaces

Layer 4 exposes stable consumer-facing access patterns.

Query surfaces are derived structures.

They do not replace preservation domains.

---

## Sample Variant Surface

Logical object:

```text
sample_variant_surface
```

---

## Sample Gene Surface

Logical object:

```text
sample_gene_surface
```

---

## Phenotype Gene Surface

Logical object:

```text
phenotype_gene_prior_surface
```

---

## Variant Gene Surface

Logical object:

```text
variant_gene_surface
```

---

## Noncoding Locus Surface

Logical object:

```text
noncoding_locus_surface
```

Supports future regulatory and enrichment workflows.

---

## Provenance Audit Surface

Logical object:

```text
provenance_audit_surface
```

Supports reconstruction and traceability.

---

## RDGP Input Surface

Logical object:

```text
rdgp_input_surface
```

Represents VDB evidence prepared for RDGP consumption.

---

# Row-Level Source Anchoring

Every persisted evidence record should remain traceable to its originating producer artifact.

Recommended relational attributes:

```text
source_artifact_id
source_row_number
source_row_hash
tep_id
entity_id
```

These structures preserve row-level traceability.

---

# Schema Binding Versioning

Relational persistence must preserve ingestion context.

Recommended relational attributes:

```text
schema_binding_version
parser_version
source_schema_signature
```

This ensures future reproducibility.

---

# Null-State Preservation

Relational persistence must distinguish:

```text
unknown

not_assessed

missing

negative

excluded
```

Null-state semantics must remain explicit.

---

# Required Relational Invariants

## Invariant 1

Evidence Objects remain reconstructable.

---

## Invariant 2

Evidence States remain reconstructable.

---

## Invariant 3

Evidence State Transitions remain reconstructable.

---

## Invariant 4

Producer-native evidence domains remain visible.

---

## Invariant 5

Namespace brokerage remains visible.

---

## Invariant 6

Query surfaces remain traceable.

---

## Invariant 7

Row-level source anchoring remains available.

---

## Invariant 8

Schema binding provenance remains available.

---

# Anti-Collapse Rules

## Evidence Object Collapse Prohibited

Evidence Objects must not be reduced to isolated rows.

---

## Evidence State Collapse Prohibited

Evidence States must remain distinguishable.

---

## Producer Collapse Prohibited

VAP, GSC, RDGP, and future repositories must not be merged into a common evidence model.

---

## Namespace Collapse Prohibited

Source identities must not be replaced by canonical identities.

---

## Query Surface Collapse Prohibited

Query surfaces must not become the sole preserved representation.

---

## Stage08 Convenience Collapse Prohibited

Persistence must not rely solely upon:

```text
stage_08_vdb_ready_variants.tsv
```

or any equivalent convenience surface.

The broader evidence topology must remain reconstructable.

---

# Relationship To Discovery Schema

The Relational Schema defines:

```text
what relational domains exist
```

The Discovery Schema defines:

```text
how those domains are discovered
navigated
indexed
explored
```

The Discovery Schema therefore builds directly upon the architecture established here.

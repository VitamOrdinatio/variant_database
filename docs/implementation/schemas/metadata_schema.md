# metadata_schema.md

## Purpose

The VDB Metadata Schema defines the descriptive and identity-bearing structures used to catalog evidence packages, artifacts, entities, runs, releases, producers, and ingestion events within the Variant Database (VDB).

The Metadata Schema does **not** define biological payload structures.

The Metadata Schema does **not** define lineage relationships.

The Metadata Schema does **not** define evidence interpretation.

Instead, the Metadata Schema defines the stable descriptive layer that allows VDB to identify, organize, discover, validate, and manage evidence products originating from heterogeneous producer repositories.

Metadata exists to answer:

```text
What is this?

Where did it come from?

When was it produced?

Who produced it?

What evidence package contains it?

What validation state does it possess?

How should it be located and referenced?
```

---

# Scope

The Metadata Schema governs:

```text
TEP packages
TEP families
Producer repositories
Producer runs
Producer releases
Artifacts
Entities
Manifests
Validation descriptors
Ingestion events
Schema versions
Discovery descriptors
```

The Metadata Schema intentionally excludes:

```text
Biological observations
Semantic consensus scores
Variant annotations
Phenotype reasoning
Gene prioritization
Lineage relationships
```

These belong to later schema layers.

---

# Design Principles

## Preservation Before Interpretation

Metadata must describe evidence without altering evidence meaning.

Metadata may identify an evidence object.

Metadata must not reinterpret an evidence object.

---

## Producer Authority Preservation

Metadata must preserve producer identity.

Producer-defined identifiers must remain visible.

VDB metadata must never overwrite source identifiers.

---

## Additive Normalization

VDB may add metadata.

VDB must not remove producer metadata.

Canonical identifiers may be attached.

Source identifiers must remain accessible.

---

## Evidence-Class Agnosticism

Metadata structures must support:

```text
VAP evidence

GSC evidence

RSP evidence

RDGP evidence

Future producer evidence
```

without requiring repository-specific metadata models.

---

## Discovery Enablement

Metadata should support discovery.

Metadata should not require payload inspection for basic catalog operations.

---

# Metadata Versus Provenance Versus Data

The VDB architecture separates metadata from provenance and data.

## Metadata

Answers:

```text
What is this object?
```

Examples:

```text
tep_id
artifact_id
producer_repository
run_id
release_id
entity_type
validation_status
```

---

## Provenance

Answers:

```text
How did this object come into existence?
```

Examples:

```text
lineage edges
derivation chains
transformation history
source attribution
```

Defined in:

```text
provenance_schema.md
```

---

## Data

Answers:

```text
What biological evidence does this object contain?
```

Examples:

```text
variants
genes
semantic priors
annotations
scores
```

Defined in:

```text
data_schema.md
```

---

# Core Metadata Entities

The Metadata Schema defines the following first-class entities:

```text
Producer
Release
Run
TEP Package
Artifact
Entity
Manifest
Validation State
Ingestion Event
Schema Version
Evidence Object
External Evidence Capsule
```

---

# Evidence Object Metadata

VDB recognizes Evidence Objects as first-class conceptual entities.

Evidence Objects represent durable evidence-bearing concepts that may persist through multiple Evidence States.

Examples:

```text
variant evidence object

semantic prior evidence object

transcriptomic evidence object

reasoning evidence object
```

Evidence Objects are described by metadata.

Evidence Objects are biologically defined by the Data Schema.

Evidence Objects are relationally represented by the Relational Schema.

Required fields:

```text
evidence_object_id
evidence_object_type
producer_id
```

Metadata does not define Evidence Object contents.

Metadata defines Evidence Object identity.


---

# Producer Metadata

Represents an evidence-producing repository.

Examples:

```text
variant_annotation_pipeline
gene_set_consensus
rnaseq_pipeline
rare_disease_gene_prioritization
```

Required fields:

```text
producer_id
producer_name
producer_version
repository_url
repository_type
```

---

# Release Metadata

Represents a producer-defined release.

Examples:

```text
epilepsy_gold_bronze_v0.1
mitocarta_only_v0.1
```

Required fields:

```text
release_id
producer_id
release_name
release_version
release_timestamp
```

---

# Run Metadata

Represents a producer execution instance.

Examples:

```text
run_2026_05_27_172531
run_2026_06_03_010030
```

Required fields:

```text
run_id
producer_id
release_id
generated_at
execution_context
```

---

# TEP Package Metadata

Represents a transport package entering VDB.

Examples:

```text
VAP-TEP
GSC-TEP
RDGP-TEP
```

Required fields:

```text
tep_id
tep_type
tep_schema_version
producer_id
release_id
run_id
generated_at
validation_state
```

A TEP Package is the primary transport unit recognized by VDB.

---

# Artifact Metadata

Represents a discrete file contained within a TEP package.

Examples:

```text
entity_inventory.json
lineage_manifest.json
annotated_variants.tsv
consensus_gene_set.tsv
validation_report.md
```

Required fields:

```text
artifact_id
tep_id
artifact_name
artifact_type
artifact_path
artifact_size
checksum
```

Artifact metadata must not assume biological meaning.

Artifacts are preserved as evidence-bearing containers.

---

# Entity Metadata

Represents a semantic evidence grouping defined by a producer.

Examples:

```text
observation
normalization
coding_interpretation
noncoding_interpretation
prioritization
validation

semantic_prior
source_contribution
gene_provenance
```

Required fields:

```text
entity_id
tep_id
entity_type
entity_name
semantic_role
producer_authority
```

Entity metadata exists to support discovery and preservation.

Entity metadata does not define biological payload structure.

---

# Manifest Metadata

Represents machine-readable package inventories.

Examples:

```text
entity_inventory.json
final_run_manifest.yaml
```

Required fields:

```text
manifest_id
tep_id
manifest_type
manifest_version
generated_at
```

---

# Validation-State Metadata

Represents producer-reported validation status.

Examples:

```text
certified
validated
experimental
provisional
```

Required fields:

```text
validation_state_id
validation_status
validation_timestamp
validation_report_reference
```

Validation metadata records status.

Validation metadata does not determine scientific truth.

---

# Authority Classification Metadata

Metadata may classify evidence authority.

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

Authority classification describes origin authority.

Authority classification does not determine correctness.

Authority classification must remain visible throughout the VDB lifecycle.

---

# Ingestion Event Metadata

Represents VDB acquisition activity.

Required fields:

```text
ingestion_event_id
tep_id
ingested_at
ingestion_version
ingestion_status
```

This metadata exists independently from producer metadata.

---

# Schema Version Metadata

Represents metadata schema evolution.

Required fields:

```text
schema_name
schema_version
effective_date
compatibility_notes
```

Schema evolution must never invalidate previously preserved evidence.

---

# External Evidence Capsule Metadata

External Evidence Capsules represent provenance-aware evidence objects synthesized by VDB from externally discovered sources.

Examples:

```text
BioSample metadata capsule

BioProject metadata capsule

external ontology capsule

external registry capsule
```

Required fields:

```text
external_capsule_id
authority_name
authority_record_id
retrieval_timestamp
authority_class
```

External Evidence Capsules supplement producer evidence.

External Evidence Capsules must never masquerade as producer evidence.

---

# Required Metadata Invariants

The following invariants are mandatory.

## Invariant 1

Every TEP Package must possess a stable TEP identifier.

---

## Invariant 2

Every artifact must reference exactly one TEP Package.

---

## Invariant 3

Every entity must reference exactly one TEP Package.

---

## Invariant 4

Producer identifiers must remain visible.

---

## Invariant 5

Run identifiers must remain visible.

---

## Invariant 6

Release identifiers must remain visible.

---

## Invariant 7

Validation state must be preserved.

---

## Invariant 8

Metadata may be extended.

Metadata may not destroy producer identity.

---

# Anti-Collapse Rules

The Metadata Schema explicitly prohibits:

## Repository Collapse

```text
VAP
GSC
RDGP
```

must not be merged into a single producer identity.

---

## Artifact Collapse

Distinct artifacts must not be reduced into a single package descriptor.

---

## Entity Collapse

Distinct entity domains must remain visible.

Examples:

```text
observation

normalization

coding_interpretation

semantic_prior

source_contribution
```

must remain distinguishable.

---

## Validation Collapse

Validation state must not be discarded during ingestion.

---

# Relationship To Later Schema Documents

The Metadata Schema provides the descriptive foundation for:

```text
provenance_schema.md
data_schema.md
relational_schema.md
discovery_schema.md
rdgp_query_surface_schema.md
```

The Metadata Schema establishes:

```text
what exists
```

Subsequent schema documents establish:

```text
how it is related

what it contains

how it is queried
```

Metadata therefore serves as the identity and catalog layer for the entire VDB architecture.

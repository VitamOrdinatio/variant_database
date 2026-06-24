# discovery_schema.md

## Purpose

The VDB Discovery Schema defines how the Variant Database (VDB) discovers, profiles, classifies, validates, attaches, ingests, and indexes evidence opportunities.

Discovery is the process by which VDB identifies evidence that may be relevant for preservation, query, enrichment, reinterpretation, or downstream reasoning.

The Discovery Schema answers:

```text
What evidence opportunity was found?

Where was it found?

What authority produced it?

What does it appear to contain?

How does it relate to existing VDB evidence?

Should it be attached, ingested, indexed, or deferred?
```

---

# Scope

The Discovery Schema governs:

```text
TEP discovery
artifact discovery
entity discovery
schema-signature discovery
field-availability discovery
missingness discovery
external evidence discovery
external metadata enrichment
discovery attachment
conflict detection
negative discovery results
refresh events
indexing readiness
```

The Discovery Schema does not define:

```text
biological payload structure
physical storage tables
clinical interpretation
prioritization logic
producer-side evidence generation
```

Those concerns belong to other schema layers.

---

# Core Principle

## Discovery Expands Evidence Horizons Without Overwriting Evidence

Discovery may identify new evidence, context, metadata, relationships, or enrichment opportunities.

Discovery must never silently replace producer evidence.

If discovered evidence conflicts with existing evidence, VDB must preserve both and mark the conflict.

---

# Relationship To Other Schema Documents

## Metadata Schema

The Metadata Schema defines what evidence objects, packages, artifacts, entities, producers, and ingestion events exist.

Discovery uses metadata to identify and classify evidence opportunities.

---

## Provenance Schema

The Provenance Schema defines how discovery results remain traceable to sources, retrieval events, transformations, and attachments.

Discovery without provenance is invalid.

---

## Data Schema

The Data Schema defines biological evidence domains.

Discovery identifies candidate evidence that may populate or extend those domains.

---

## Relational Schema

The Relational Schema defines logical relational domains.

Discovery supplies the profiling, attachment, conflict, and indexing structures that make relational persistence safe.

---

# Discovery Modes

VDB recognizes two primary discovery modes.

---

## Mode 1 — TEP Discovery

TEP Discovery operates on evidence products produced by VitamOrdinatio producer repositories.

Examples:

```text
TEP-VAP
TEP-GSC
future TEP-RSP
future TEP-RDGP
future TEP-VDB
```

TEP Discovery examines:

```text
TEP package identity
TEP family
TEP schema version
producer identity
run identity
release identity
artifact inventory
entity inventory
lineage manifest
validation state
payload signatures
schema signatures
field availability
```

Authority model:

```text
producer_authoritative
```

---

## Mode 2 — External Evidence Discovery

External Evidence Discovery operates on data not supplied directly through a VitamOrdinatio producer-side TEP.

Examples:

```text
NCBI BioProject metadata
NCBI BioSample metadata
SRA metadata
EBI / ENA metadata
ClinVar metadata
dbSNP metadata
HGNC metadata
Ensembl metadata
RefSeq metadata
external ontology records
```

External Discovery may identify missing, updated, or enrichable context.

Authority model:

```text
external_authority
```

External evidence must be preserved as externally sourced evidence, not silently merged into producer evidence.

---

# Discovery Lifecycle

The Discovery Schema separates discovery from ingestion.

The lifecycle is:

```text
discover
profile
classify authority
validate
attach or propose attachment
ingest
index
refresh when needed
```

Each step must be represented explicitly.

---

# Discovery Subject

A Discovery Subject is the object or opportunity being examined.

Examples:

```text
TEP package
TEP artifact
TEP entity
external accession
external record
missing metadata field
candidate identity relationship
candidate evidence relationship
```

Required fields:

```text
discovery_subject_id
subject_type
subject_reference
authority_class
discovery_scope
```

---

# Discovery Event

A Discovery Event records an act of discovery.

Examples:

```text
profiled TEP package
parsed entity inventory
inspected lineage manifest
detected missing BioSample field
queried NCBI BioSample
retrieved external metadata record
detected conflicting field value
refreshed external record snapshot
```

Required fields:

```text
discovery_event_id
discovery_subject_id
event_type
event_timestamp
discovery_method
discovery_tool
discovery_version
status
```

---

# Discovery Result

A Discovery Result records what was found.

Examples:

```text
artifact exists
schema signature detected
field present
field missing
external record retrieved
candidate attachment detected
conflict detected
no matching external record found
```

Required fields:

```text
discovery_result_id
discovery_event_id
result_type
result_status
result_summary
```

---

# Authority Classification

Every discovered object must have an authority class.

Supported classes include:

```text
producer_authoritative
external_authority
vdb_discovered_external
vdb_inferred
user_supplied
derived_query_surface
unknown_authority
```

Authority classification must remain visible.

Authority classes must not be silently promoted.

---

# Field-Level Discovery

Discovery must support field-level profiling.

Examples:

```text
age field present
sex field absent
BioSample accession present
library strategy present
organism field present
phenotype field missing
```

Required fields:

```text
field_discovery_id
discovery_result_id
field_name
field_status
field_value_preview
field_authority_class
field_source_reference
```

Field-level provenance is mandatory for externally discovered metadata.

---

# Missingness Discovery

Missingness is itself evidence.

Examples:

```text
BioSample field absent
age not provided
sex not provided
platform unknown
phenotype unavailable
```

Required fields:

```text
missingness_id
field_discovery_id
missingness_type
missingness_note
```

Missingness must not be collapsed into a null value without explanation.

---

# External Record Snapshot

External records may change over time.

VDB must preserve snapshots of externally retrieved records.

Examples:

```text
BioSample record snapshot
SRA run metadata snapshot
ENA record snapshot
HGNC gene record snapshot
```

Required fields:

```text
external_record_snapshot_id
authority_name
authority_record_id
retrieved_at
retrieval_method
record_hash
record_format
record_payload_reference
```

External snapshots preserve what VDB observed at retrieval time.

---

# Refresh Event

A Refresh Event records re-checking an external source.

Required fields:

```text
refresh_event_id
external_record_snapshot_id
refreshed_at
refresh_method
previous_record_hash
new_record_hash
change_detected
```

Refresh events preserve evidence evolution from external authorities.

---

# Discovery Attachment

A Discovery Attachment records how discovered evidence relates to existing VDB evidence.

Examples:

```text
BioSample metadata attached to VAP sample evidence object
SRA metadata attached to producer run
HGNC record attached to gene identity
external phenotype term attached to semantic prior
```

Required fields:

```text
discovery_attachment_id
discovery_result_id
target_evidence_object_id
target_evidence_state_id
attachment_type
attachment_status
```

Discovery attachments must be provenance-aware.

---

# Proposed Attachment State

Some discovered evidence should not be immediately treated as accepted.

Supported attachment states include:

```text
proposed
accepted
rejected
superseded
conflicted
deferred
```

This allows VDB to preserve candidate relationships without over-claiming.

---

# Conflict Record

A Conflict Record preserves disagreement between sources.

Examples:

```text
producer metadata differs from BioSample metadata
NCBI and ENA report different sample attributes
external authority updates a field value
identifier maps ambiguously
```

Required fields:

```text
conflict_id
conflict_type
existing_value_reference
discovered_value_reference
conflict_status
```

Conflicts must not be silently resolved.

---

# Negative Discovery Result

A Negative Discovery Result records that a discovery attempt found nothing.

Examples:

```text
no BioSample accession found
BioProject lookup failed
age field absent
external metadata unavailable
```

Required fields:

```text
negative_result_id
discovery_event_id
query_target
query_parameters
negative_result_type
```

Negative results prevent repeated blind querying and preserve meaningful absence.

---

# Schema Signature Discovery

Discovery must profile schema structure.

Examples:

```text
TSV header signature
JSON key signature
manifest signature
entity-domain signature
field-count signature
```

Required fields:

```text
schema_signature_id
discovery_result_id
artifact_id
signature_type
signature_hash
signature_summary
```

Schema signatures support future producer evolution.

---

# Field Availability Profile

A Field Availability Profile summarizes fields present or absent in an artifact, entity, package, or external record.

Required fields:

```text
field_profile_id
discovery_result_id
field_count
present_fields
missing_expected_fields
unexpected_fields
```

Field availability profiles support safe ingestion planning.

---

# Discovery Validation State

Discovery findings require validation state.

Supported states include:

```text
unvalidated
profiled
validated
partially_validated
conflicted
rejected
superseded
```

Discovery validation state must be independent from producer validation state.

---

# Indexing Readiness

Discovery may identify whether an object is ready for indexing.

Required fields:

```text
indexing_readiness_id
discovery_result_id
indexing_status
indexing_scope
blocking_reason
```

Indexing readiness does not imply biological interpretation.

---

# External Evidence Capsule

External evidence discovered by VDB should be organized into a provenance-aware capsule.

An External Evidence Capsule is not a producer-side TEP.

It is a VDB-synthesized preservation object for externally discovered context.

Required fields:

```text
external_capsule_id
authority_name
authority_record_id
discovery_event_id
snapshot_id
attachment_status
```

External Evidence Capsules preserve non-TEP evidence without pretending it came from a VitamOrdinatio producer repository.

---

## External Evidence Capsule Relationship To Metadata

External Evidence Capsules are metadata-bearing evidence objects.

External Evidence Capsules participate in:

```text
metadata classification

provenance tracking

authority classification

discovery attachment

query-surface exposure
```

External Evidence Capsules are not producer-side TEPs.

External Evidence Capsules are VDB-native preservation structures.

---

# Required Discovery Invariants

## Invariant 1

Discovery must be separate from ingestion.

---

## Invariant 2

Every discovery event must have provenance.

---

## Invariant 3

Every discovered object must have an authority class.

---

## Invariant 4

External evidence must not overwrite producer evidence.

---

## Invariant 5

Conflicts must remain visible.

---

## Invariant 6

Negative discovery results must be preservable.

---

## Invariant 7

External record snapshots must be versioned.

---

## Invariant 8

Field-level provenance must be available for externally discovered metadata.

---

## Invariant 9

Discovery attachments must preserve target evidence identity.

---

# Anti-Collapse Rules

## Producer Evidence Overwrite Prohibited

Externally discovered evidence must not replace producer evidence.

---

## Authority Collapse Prohibited

Producer, external, inferred, user-supplied, and derived evidence must remain distinguishable.

---

## Missingness Collapse Prohibited

Missing fields must not be collapsed into unexplained nulls.

---

## Conflict Collapse Prohibited

Conflicting evidence must not be silently resolved.

---

## Discovery-Ingestion Collapse Prohibited

Discovered evidence must not be treated as ingested evidence until ingestion is explicitly performed.

---

## Query Surface Collapse Prohibited

Discovery results must not become query surfaces unless explicitly indexed and validated.

---

# Relationship To RDGP

RDGP may consume VDB evidence surfaces that include discovered external context.

Examples:

```text
age-aware sample-gene evidence
BioSample-aware cohort stratification
platform-aware evidence filtering
phenotype-aware prioritization
```

However, RDGP-facing surfaces must preserve whether each context field was:

```text
producer supplied
externally discovered
VDB inferred
user supplied
```

This prevents hidden provenance contamination.

---

# Relationship To Future TEP Families

The Discovery Schema must support future TEP families.

Examples:

```text
TEP-RSP
TEP-RDGP
TEP-VDB
```

Discovery must be capable of identifying:

```text
known envelope
unknown payload
known producer
unknown entity domain
new schema signature
new evidence object type
```

Unknown evidence must be preserved as discoverable, not discarded.

---

# Summary

The Discovery Schema defines how VDB finds, profiles, classifies, attaches, validates, and indexes evidence opportunities.

Discovery is not interpretation.

Discovery is not ingestion.

Discovery is not overwrite.

Discovery is the governed process by which VDB expands its evidence horizon while preserving authority, provenance, conflict, missingness, and future reinterpretability.

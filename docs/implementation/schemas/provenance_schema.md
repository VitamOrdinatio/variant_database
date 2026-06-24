# provenance_schema.md

## Purpose

The VDB Provenance Schema defines how evidence origin, derivation, lineage, attribution, transformation, validation, and preservation history are represented within the Variant Database (VDB).

The Provenance Schema exists to ensure that evidence remains:

```text
traceable
auditable
reconstructable
reproducible
interpretable
```

across repository boundaries, TEP generations, schema evolution, and future biological reinterpretation.

The Provenance Schema answers:

```text
Where did this evidence originate?

What process produced it?

What artifacts contributed to it?

What transformations occurred?

What evidence entities does it depend upon?

Can the original context be reconstructed?
```

---

# Scope

The Provenance Schema governs:

```text
producer attribution
run attribution
release attribution
artifact lineage
entity lineage
TEP lineage
derivation relationships
transformation relationships
validation provenance
ingestion provenance
query-surface provenance
```

The Provenance Schema does not govern:

```text
biological payload structure
variant annotations
semantic scores
clinical interpretation
query execution logic
```

Those belong to later schema layers.

---

# Core Principle

## Evidence Must Remain Reconstructable

The primary purpose of provenance is not auditing.

The primary purpose of provenance is reconstruction.

VDB must preserve enough provenance to answer:

```text
How was this evidence state created?
```

at any future point.

This requirement applies equally to:

```text
VAP evidence
GSC evidence
RSP evidence
RDGP evidence
future producer evidence
```

---

# Design Principles

## Preservation Over Compression

Provenance must never be discarded solely because it appears redundant.

Future biological interpretation may depend on relationships that are not currently understood.

---

## Additive Provenance

VDB may add provenance.

VDB must not replace producer provenance.

Producer provenance remains authoritative.

---

## Field-Level Provenance

VDB must support provenance at the field level when attaching externally discovered evidence.

Examples:

```text
age
sex
BioSample accession
tissue type
collection metadata
```

Field-level provenance must preserve:

```text
field source
authority class
retrieval event
retrieval timestamp
```

Field-level provenance must remain distinguishable from producer-supplied values.

---

## Explicit Relationships

Lineage relationships must be represented explicitly.

Implicit lineage is prohibited.

---

## Multi-Hop Reconstruction

A provenance chain must support reconstruction across multiple transformations.

Example:

```text
Observation
    →
Normalization
    →
Interpretation
    →
Prioritization
    →
Validation
```

must remain traversable.

---

## Producer Neutrality

The provenance model must support:

```text
variant evidence

semantic prior evidence

transcriptomic evidence

reasoning evidence
```

without producer-specific assumptions.

---

# Provenance Entity Classes

The Provenance Schema defines the following first-class provenance entities:

```text
Source
Transformation
Lineage Edge
Attribution
Validation Event
Ingestion Event
Query Surface
```

---

# Source Provenance

Represents the origin of evidence.

Examples:

```text
VAP run
GSC run
RSP run
RDGP run
external reference dataset
```

Required fields:

```text
source_id
source_type
producer_id
run_id
release_id
generated_at
```

Source provenance identifies origin.

Source provenance does not describe biological content.

---

# Transformation Provenance

Represents a process that generated a new evidence state.

Examples:

```text
annotation
normalization
aggregation
semantic scoring
prioritization
validation
reasoning
```

Required fields:

```text
transformation_id
transformation_type
producer_id
run_id
timestamp
software_version
```

Transformations must be recorded as explicit provenance objects.

---

# Attribution Provenance

Represents evidence contribution.

Examples:

```text
GTR contribution
MitoCarta contribution
EPI25 contribution
ClinVar contribution
```

Required fields:

```text
attribution_id
source_id
evidence_entity_id
contribution_type
contribution_weight
```

Attribution provenance preserves contribution topology.

---

# Lineage Edge Model

The lineage edge is the fundamental provenance structure.

Lineage edges may connect:

```text
artifact
entity
evidence object
evidence state
```

Every derivation relationship is represented explicitly.

Examples:

```text
artifact
    →
artifact

entity
    →
entity

evidence state
    →
evidence state
```

Required fields:

```text
lineage_edge_id
source_object_id
source_object_type
target_object_id
target_object_type
relationship_type
transformation_id
```

Lineage relationships must remain reconstructable across all provenance-bearing object classes.

---

# Relationship Types

Supported lineage relationships include:

```text
derived_from
generated_from
aggregated_from
annotated_from
validated_from
reasoned_from
mapped_from
normalized_from
```

Additional relationship types may be added.

Relationship types must never be overloaded.

---

# Artifact Provenance

Artifacts must preserve their origin.

Required fields:

```text
artifact_id
source_artifact_id
source_run_id
source_release_id
```

Artifacts must remain traceable to producer outputs.

---

# Entity Provenance

Entities must preserve derivation relationships.

Examples:

```text
observation entity

normalization entity

semantic prior entity

source contribution entity
```

Required fields:

```text
entity_id
source_entity_id
entity_type
producer_id
```

---

# TEP Provenance

Every TEP entering VDB must retain transport provenance.

Required fields:

```text
tep_id
producer_id
run_id
release_id
tep_schema_version
generated_at
```

VDB must preserve transport provenance even after evidence is decomposed into persistence domains.

---

# VAP Provenance Obligations

VAP evidence requires preservation of:

```text
observation lineage
normalization lineage
coding interpretation lineage
noncoding interpretation lineage
prioritization lineage
validation lineage
context lineage
```

The Stage07 preservation anchor must remain reconstructable.

Later overlays must not obscure earlier evidence states.

---

# GSC Provenance Obligations

GSC evidence requires preservation of:

```text
phenotype context
source contribution topology
semantic channel attribution
consensus derivation
release identity
mapping status
uncertainty state
```

The source contribution network must remain reconstructable.

Gene + score collapse is prohibited.

---

# RDGP Provenance Obligations

Future RDGP evidence requires preservation of:

```text
input evidence references
reasoning framework references
prioritization rationale
reasoning lineage
uncertainty state
```

Reasoning outputs must remain traceable to supporting evidence.

---

# Validation Provenance

Validation must itself possess provenance.

Required fields:

```text
validation_event_id
validation_type
validation_timestamp
validation_status
validation_artifact
```

Validation provenance must never be discarded.

---

# Ingestion Provenance

VDB acquisition activities must be recorded.

Required fields:

```text
ingestion_event_id
tep_id
ingestion_timestamp
ingestion_version
ingestion_status
```

Producer provenance and ingestion provenance are separate concepts.

---

# Query Surface Provenance

Query surfaces must preserve evidence traceability.

Every queryable evidence object must support navigation back to:

```text
producer
release
run
tep
artifact
entity
```

A query surface must never become a provenance dead-end.

---

# Required Provenance Invariants

## Invariant 1

Every evidence object must have a provenance path.

---

## Invariant 2

Every lineage edge must be directional.

---

## Invariant 3

Every lineage edge must identify a relationship type.

---

## Invariant 4

Producer provenance must remain visible.

---

## Invariant 5

Run provenance must remain visible.

---

## Invariant 6

Release provenance must remain visible.

---

## Invariant 7

Validation provenance must remain visible.

---

## Invariant 8

TEP provenance must remain visible.

---

## Invariant 9

Lineage reconstruction must remain possible.

---

# Anti-Collapse Rules

## Provenance Removal Prohibited

Evidence may not be retained without provenance.

---

## Attribution Removal Prohibited

Source contribution information may not be discarded.

---

## Transformation Removal Prohibited

Transformations may not be hidden.

---

## Query-Surface Collapse Prohibited

Query surfaces must not sever links to underlying provenance.

---

## TEP Detachment Prohibited

Evidence persisted within VDB must remain traceable to its originating TEP.

---

# Relationship To Later Schema Documents

The Provenance Schema defines:

```text
where evidence came from
```

The Data Schema defines:

```text
what evidence contains
```

The Relational Schema defines:

```text
how evidence and provenance are physically stored
```

The Discovery Schema defines:

```text
how evidence and provenance are located
```

The RDGP Query Surface Schema defines:

```text
how provenance-aware evidence is consumed
```

The Provenance Schema therefore serves as the preservation and reconstruction layer of the VDB architecture.

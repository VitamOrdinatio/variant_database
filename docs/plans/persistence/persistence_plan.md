# persistence_plan.md

## Purpose

This document defines the implementation plan for the VDB persistence subsystem.

The persistence subsystem is responsible for durably preserving VDB logical domains after ingestion while maintaining identity, provenance, authority, uncertainty, evidence topology, and reconstructability.

This plan translates:

```text
docs/contracts/persistence/persistence_contract.md
```

into a concrete implementation sequence.

---

# Relationship To Master Plan

This plan services:

```text
docs/plans/implementation_plan.md
```

and implements:

```text
docs/contracts/persistence/persistence_contract.md
```

Persistence is the phase where VDB becomes a durable evidence preservation system rather than an inventory tool.

---

# Implementation Goal

The goal of the persistence subsystem is:

```text
Preserve VDB logical evidence domains
in a deterministic, reconstructable, storage-backed form
without collapsing evidence into convenience outputs.
```

Persistence must preserve evidence states and evidence history.

Persistence must not reduce evidence to consumer-ready tables.

---

# Backend Strategy

The initial backend should prioritize:

```text
determinism
inspectability
local development simplicity
testability
schema control
```

Recommended initial backend:

```text
SQLite
```

Supporting outputs may include:

```text
JSON reports
TSV exports
future DuckDB or Parquet analytics surfaces
```

SQLite should be treated as the canonical v1 persistence core unless implementation constraints require adjustment.

---

# Logical Domain Strategy

The persistence subsystem must preserve the following logical domains:

```text
TEP Package
Artifact
Entity
Metadata Record
Provenance Record
Evidence Object
Evidence State
Evidence State Transition
Namespace Event
Overlay Attachment
Discovery Event
External Evidence Capsule
Query Surface Derivation
Field Promotion Event
Promoted Index
```

Physical tables are implementation details.

Logical domains are contractual obligations.

---

# Core Table Versus Payload Field Strategy

Persistence must distinguish among three categories of stored information.

---

## Core Columns

Core columns are stable, governed, query-critical fields.

A field should become a core column when VDB must:

```text
join on it
validate it
version it
reconstruct from it
filter by it
control behavior with it
expose it on canonical query surfaces
```

Examples include:

```text
stable identifiers
producer identity
TEP identity
artifact identity
entity identity
Evidence Object identifiers
Evidence State identifiers
source namespace identifiers
canonical identifiers
resolution status
provenance handles
authority class
state type
timestamps
policy versions
schema versions
validation status
```

---

## Payload Fields

Payload fields preserve producer-specific or externally discovered details that are not yet required as core control fields.

Examples include:

```text
producer-specific row content
large annotation fields
VAP-specific interpretation labels
GSC scoring channel details
source-specific evidence labels
optional metadata
future or unknown fields
```

Payload is not discard space.

Payload is preservation space.

Payload fields must remain:

```text
stored
versioned
traceable
hashable
recoverable
```

---

## Promoted Indexes

Promoted indexes are derived, queryable structures created from payload fields when future use cases require direct filtering, joining, validation, or query-surface exposure.

A payload field may later become queryable through a governed field-promotion event.

Promoted indexes must preserve:

```text
original payload location
source authority
discovery event
promotion policy version
field semantics
null semantics
conflict status
```

Promotion must not rewrite the original payload.

---

# Field Promotion Strategy

Field promotion exists to support future discovery.

Example scenario:

```text
TEP-VAP initially lacks usable age metadata.

Later VDB discovers external BioSample metadata.

The external metadata is preserved as an External Evidence Capsule.

A field such as age_at_collection is promoted into a queryable index.

The original producer evidence remains unchanged.
```

Promotion enables future SQL-style queries without violating preservation doctrine.

Example future query:

```text
samples over age 30
with POLG evidence
and noncoding burden near candidate loci
```

Promotion is additive.

Promotion is provenance-aware.

Promotion is reversible by reconstruction.

---

# Stable Identifier Strategy

Persistence should use deterministic identifiers wherever practical.

Examples:

```text
tep_package_id
    derived from producer, run_id, tep_id, package identity

artifact_id
    derived from tep_package_id, relative path, checksum when available

entity_id
    derived from artifact_id and entity identity

evidence_object_id
    derived from artifact_id, entity_id, source row or evidence key

evidence_state_id
    derived from evidence_object_id, state type, payload hash, policy version

state_transition_id
    derived from source state, destination state, transition type, timestamp or deterministic event key
```

Stable IDs support:

```text
idempotent ingestion
deterministic testing
reconstruction
cross-run comparison
```

---

# Payload Strategy

Payloads should preserve producer-specific evidence without forcing premature normalization.

Payloads should be stored as structured data where possible.

Recommended forms:

```text
JSON payload columns

payload hashes

payload schema labels

payload source references
```

Payloads must remain reconstructable from persistence.

Payloads must not become opaque discard bins.

---

# Phase 1 — Backend Scaffold

## Purpose

Create the storage backend foundation.

## Expected Work

Implement:

```text
database initialization

schema version tracking

migration or schema creation utilities

connection management

transaction handling

basic repository interfaces
```

## Proposed Modules

```text
src/variant_database/persistence/

    backend.py

    schema_manager.py

    repositories.py

    models.py
```

## Expected Outputs

```text
empty VDB store

schema version table

initial schema creation function

backend smoke tests
```

## Exit Criteria

```text
store can be initialized

schema version is recorded

tests can create and destroy temporary stores

backend behavior is deterministic
```

---

# Phase 2 — Ingestion Output Persistence

## Purpose

Persist records generated by the ingestion subsystem.

## Expected Work

Persist:

```text
TEP Package Records

Artifact Records

Entity Records

Metadata Records

Provenance Records

Ingestion Events
```

## Expected Outputs

```text
package table or equivalent logical store

artifact table or equivalent logical store

entity table or equivalent logical store

metadata store

provenance store

ingestion event store
```

## Exit Criteria

```text
ingestion outputs persist successfully

metadata remains reconstructable

provenance remains reconstructable

artifact identity remains visible

source artifacts remain immutable
```

---

# Phase 3 — Evidence Object Persistence

## Purpose

Persist Evidence Objects as first-class logical objects.

## Expected Work

Implement storage for:

```text
Evidence Object identifiers

source references

producer references

artifact references

entity references

evidence family

evidence domain

authority class

payload references
```

## Expected Outputs

```text
Evidence Object store

Evidence Object insertion API

Evidence Object retrieval API

Evidence Object validation tests
```

## Exit Criteria

```text
Evidence Objects persist

Evidence Objects remain traceable to artifacts

Evidence Objects preserve source identity

Evidence Objects preserve authority
```

---

# Phase 4 — Evidence State Persistence

## Purpose

Persist Evidence States as additive, reconstructable states.

## Expected Work

Implement storage for:

```text
Evidence State identifiers

Evidence Object references

state type

state payload

state payload hash

generation context

authority context

uncertainty context

policy version
```

## Expected Outputs

```text
Evidence State store

Evidence State insertion API

Evidence State retrieval API

Evidence State validation tests
```

## Exit Criteria

```text
Evidence States persist

states are reconstructable

state payloads are preserved

states do not overwrite prior states
```

---

# Phase 5 — Evidence State Transition Persistence

## Purpose

Preserve evidence state history.

## Expected Work

Implement storage for:

```text
source state

destination state

transition type

transition rationale

triggering subsystem

transition timestamp

transition policy version
```

## Expected Outputs

```text
Evidence State Transition store

transition insertion API

transition retrieval API

state history traversal tests
```

## Exit Criteria

```text
state transitions persist

state history is reconstructable

transitions do not overwrite states
```

---

# Phase 6 — Future Domain Persistence Scaffolds

## Purpose

Create persistence capacity for downstream subsystems.

## Expected Work

Create logical stores for:

```text
Namespace Events

Identity Bridges

Overlay Attachments

Discovery Events

External Evidence Capsules

Query Surface Derivations

Field Promotion Events

Promoted Indexes
```

These may initially be minimally populated.

## Exit Criteria

```text
future domain stores exist

stores preserve logical separation

downstream subsystems can populate them later
```

---

# Phase 7 — Reconstruction Handles

## Purpose

Ensure all persisted domains support evidence reconstruction.

## Expected Work

Add or verify reconstruction handles for:

```text
source repository

source producer

source run

source TEP

source artifact

source entity

Evidence Object

Evidence State

Evidence State Transition

Namespace Event

Overlay Attachment

Discovery Event

Query Surface Derivation
```

## Expected Outputs

```text
reconstruction handle map

lineage traversal tests

reconstruction validation report
```

## Exit Criteria

```text
source lineage reconstructable

state lineage reconstructable

artifact lineage reconstructable

future overlay/discovery/query lineage supported
```

---

# Test Strategy

Persistence tests must verify:

```text
backend initialization

schema version tracking

record insertion

record retrieval

idempotent insertion where expected

stable ID generation

payload preservation

payload hashing

field promotion behavior

state immutability

state transition visibility

logical domain separation

reconstruction traversal
```

---

# Validation Gates

Persistence must satisfy:

```text
docs/validation/schema_validation.md
```

and must support:

```text
docs/validation/vdb_end_to_end_lifecycle_walkthrough.md
```

Required gates include:

```text
logical domain preservation

metadata reconstruction

provenance reconstruction

state reconstruction

namespace event readiness

overlay attachment readiness

query surface derivation readiness
```

---

# Anti-Collapse Checks

The persistence subsystem must verify that implementation does not:

```text
store only current state

overwrite source evidence

collapse Evidence Objects into Evidence States

collapse Evidence States into query outputs

collapse payload into discard space

collapse promoted indexes into source evidence

collapse provenance

collapse namespace history

collapse overlays into primary evidence

materialize query surfaces as authoritative evidence
```

These checks are mandatory.

---

# Future Benchmark Scenario

Persistence must support eventual execution of:

```text
docs/examples/vdb_evidence_lifecycle_example.md
```

Specifically, persistence must support preservation of:

```text
HG002 POLG VAP evidence

mitochondrial POLG GSC evidence

namespace bridge through ENSG00000140521

overlay attachment state

RDGP surface derivation

evidence reconstruction path
```

No persistence behavior may prevent this benchmark lifecycle.

---

# Definition Of Done

The persistence subsystem is complete when:

```text
backend initializes deterministically

logical domain records persist

Evidence Objects persist

Evidence States persist

Evidence State Transitions persist

payloads are preserved

payload fields can be promoted through governed events

metadata remains reconstructable

provenance remains reconstructable

state history remains reconstructable

validation passes

anti-collapse checks pass
```

The persistence subsystem is not complete merely because rows can be written.

---

# Summary

The persistence subsystem is the durable custody ledger of VDB.

Its purpose is to preserve evidence, preserve history, and preserve future query possibility.

The guiding implementation rule is:

```text
Store the control fields.

Preserve the payload.

Promote query fields only through governed events.

Never collapse the evidence state.
```

# persistence_contract.md

## Purpose

This contract defines the obligations, constraints, and expected behaviors of the VDB persistence subsystem.

The persistence subsystem is responsible for preserving evidence after successful ingestion while maintaining identity, provenance, authority, uncertainty, and reconstructability.

The persistence subsystem exists to ensure that evidence remains available for future discovery, reinterpretation, query construction, and downstream reasoning.

---

# Relationship To System Contract

This contract derives from:

```text
docs/contracts/system_contract.md
```

All persistence behavior must remain compliant with the VDB System Contract.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Core Principle

```text
Persistence stores evidence states.

Persistence does not store convenience outputs.
```

The persistence subsystem exists to preserve evidence and evidence history.

Convenience representations may be derived later.

Convenience representations must not replace preserved evidence.

---

# Scope

This contract governs:

```text
persistent evidence storage
logical evidence domains
Evidence Objects
Evidence States
Evidence State Transitions
metadata persistence
provenance persistence
namespace event persistence
overlay persistence
discovery event persistence
external evidence persistence
reconstruction support
```

This contract does not govern:

```text
TEP ingestion validation
namespace resolution execution
query surface generation
RDGP reasoning
consumer-specific projections
```

Those activities belong to separate subsystems.

---

# Persistence Boundary

The persistence subsystem operates at the boundary:

```text
Ingested Evidence
        ↓
Persistence
        ↓
Preserved Evidence
```

Persistence transforms transient ingestion outputs into durable evidence assets.

---

# Logical Domain Requirements

Persistence must preserve the following logical domains as first-class architectural concepts:

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

Logical domains are contractual obligations.

---

# Physical Tables Versus Logical Domains

Persistence implementations may utilize:

```text
SQLite
DuckDB
PostgreSQL
Parquet
future storage engines
```

Physical storage structures are implementation details.

Logical domains are architectural requirements.

Persistence implementations may change physical layouts.

Persistence implementations must preserve logical domains.

The following is prohibited:

```text
collapsing logical domains because of physical convenience
```

---

# Immutability Requirements

Persistence must preserve source evidence immutability.

Source evidence records must not be overwritten.

Source evidence records must not be destructively modified.

Derived evidence must be represented through:

```text
new Evidence States

new Evidence State Transitions

new attachment relationships
```

rather than mutation of existing evidence.

---

# Evidence Object Requirements

Persistence must preserve Evidence Objects.

Evidence Objects must retain:

```text
source identity
producer identity
artifact references
evidence family
authority class
provenance references
```

Evidence Objects represent the canonical preservation unit of evidence.

---

# Evidence State Requirements

Persistence must preserve Evidence States.

Evidence States must retain:

```text
state identity
state type
generation context
authority context
uncertainty context
producer context
```

Evidence States must remain independently reconstructable.

---

# Evidence State Transition Requirements

Persistence must preserve Evidence State Transitions.

Transitions must record:

```text
source state
destination state
transition type
transition timestamp
transition rationale
triggering subsystem
```

Examples include:

```text
ingestion registration

namespace resolution

overlay attachment

discovery enrichment

RDGP return path

future reinterpretation
```

Transitions must remain visible.

---

# Metadata Persistence Requirements

Persistence must preserve metadata sufficient to reconstruct:

```text
repository
producer
release
run
TEP package
artifact
entity
evidence object
evidence state
```

Metadata loss constitutes persistence failure.

---

# Provenance Persistence Requirements

Persistence must preserve provenance sufficient to reconstruct:

```text
evidence origin

producer lineage

artifact lineage

TEP lineage

state lineage

overlay lineage

query lineage
```

All preserved evidence must remain traceable.

---

# Namespace Event Persistence Requirements

Persistence must preserve namespace activity separately from source evidence.

Namespace events must preserve:

```text
source identifier

source namespace

canonical identifier

resolution authority

resolution status

resolution timestamp

resolution rationale
```

Source identities must remain visible after resolution.

---

# Overlay Attachment Persistence Requirements

Persistence must preserve overlay attachments as explicit relationships.

Overlay attachments must preserve:

```text
primary evidence

overlay evidence

attachment rationale

attachment authority

attachment uncertainty

attachment timestamp
```

Overlay attachments must not fuse evidence.

---

# Discovery Event Persistence Requirements

Persistence must preserve discovery events.

Discovery events must record:

```text
discovery identifier

trigger

discovery rationale

retrieved evidence

authority source

retrieval timestamp
```

Discovery must remain reconstructable.

---

# External Evidence Capsule Persistence Requirements

Persistence must preserve External Evidence Capsules separately from producer evidence.

External evidence must preserve:

```text
authority source

retrieval timestamp

snapshot identity

field provenance

conflict status

attachment status
```

External evidence must remain distinguishable from producer evidence.

---

# Query Surface Derivation Requirements

Persistence must preserve query-surface derivation history.

Persistence must retain:

```text
derivation identifier

derivation version

source evidence references

construction policy

timestamp
```

Query surfaces are derived products.

Query surfaces are not authoritative evidence.

---

# Field Promotion Requirements

Persistence may promote preserved payload fields into queryable indexes when future discovery, validation, query surfaces, or downstream consumers require direct filtering, joining, validation, or exposure.

Field promotion must preserve:

```text
original payload location

source authority

promotion event

promotion policy version

field semantics

null semantics

conflict status

source provenance

discovery provenance when applicable
```

Field promotion is additive.

Field promotion must not rewrite original payloads.

Field promotion must not convert derived indexes into authoritative evidence.

Promoted indexes are query-enabling structures.

Promoted indexes are not replacements for preserved payloads.

---

# Null Semantics Requirements

Persistence must preserve semantic distinctions among:

```text
unknown

missing

not evaluated

not applicable

ambiguous

conflicted

unresolved

measured zero
```

Null-state collapse is prohibited.

---

# Versioning Requirements

Persistence must preserve version visibility.

Examples include:

```text
schema versions

ingestion policy versions

namespace policy versions

query surface versions

overlay policy versions
```

Version history must remain visible.

---

# Determinism Requirements

Given identical:

```text
ingested evidence

schema versions

policies

resolution outcomes
```

the persistence subsystem must produce equivalent preserved structures.

Persistence behavior must be deterministic.

---

# Anti-Collapse Rules

The persistence subsystem must not:

```text
overwrite source evidence

store only current state

collapse state history

collapse provenance

collapse namespace history

collapse overlays into evidence

collapse evidence into scores

collapse artifacts into flattened rows

replace source identities with canonical identities

materialize query surfaces as authoritative evidence

collapse promoted indexes into source evidence

treat promoted indexes as authoritative evidence

rewrite payloads during field promotion
```

Preservation takes precedence over convenience.

---

# Reconstruction Requirements

Persistence must support reconstruction of:

```text
source repository

source producer

source release

source run

source TEP

source artifact

source entity

Evidence Object history

Evidence State history

namespace history

overlay history

discovery history

query-surface derivation history

field promotion history

promoted index derivation history
```

If reconstruction fails, persistence has failed.

---

# Compliance Criteria

The persistence subsystem is compliant only if:

```text
logical domains remain visible

source evidence remains immutable

Evidence Objects remain preserved

Evidence States remain preserved

Evidence State Transitions remain preserved

metadata remains reconstructable

provenance remains reconstructable

namespace history remains reconstructable

overlay history remains reconstructable

anti-collapse rules remain satisfied
```

Failure of any requirement constitutes contract noncompliance.

---

# Relationship To Other Contracts

This contract is serviced by:

```text
ingestion_contract.md
```

and supports:

```text
namespace_resolution_contract.md

discovery_overlay_contract.md

query_surface_contract.md
```

Persistence serves as the foundational layer upon which all downstream VDB functionality depends.

---

# Summary

The persistence subsystem exists to preserve evidence such that future systems can discover, relate, reinterpret, query, and reconstruct it.

The guiding principle is:

```text
Preserve the evidence.

Preserve the history.

Preserve the relationships.

Never collapse the state space.
```

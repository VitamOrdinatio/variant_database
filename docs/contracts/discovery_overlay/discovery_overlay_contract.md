# discovery_overlay_contract.md

## Purpose

This contract defines the obligations, constraints, and expected behaviors of the VDB discovery and overlay attachment subsystem.

The discovery and overlay subsystem is responsible for identifying evidence relationships and attaching evidence from one domain to evidence from another domain while preserving identity, provenance, authority, uncertainty, phenotype context, and reconstruction capability.

The purpose of discovery and overlay attachment is to relate evidence.
The purpose is not to fuse evidence.

---

# Relationship To System Contract

This contract derives from:
`docs/contracts/system_contract.md`

All discovery and overlay behavior must remain compliant with the VDB System Contract.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Core Principle

Discovery finds relationships.

Overlay attachment records relationships.

Neither discovery nor overlay attachment rewrites evidence.

Discovery and overlay attachment are additive.

They must not modify source evidence.

---

# Scope

This contract governs:

```text
internal evidence discovery

cross-producer evidence discovery

overlay candidate identification

overlay attachment creation

discovery event recording

overlay attachment provenance

attachment rationale preservation

phenotype context preservation

external evidence context attachment when applicable
```

This contract does not govern:

```text
producer TEP ingestion

persistent storage backend design

namespace resolution execution

query surface construction

RDGP reasoning
```

Those responsibilities belong to separate subsystems.

---

# Allowed Responsibilities

The discovery and overlay subsystem may:

```text
read preserved Evidence Objects

read preserved Evidence States

read Identity Bridges

identify candidate relationships

create Discovery Events

create Overlay Attachment records

create overlay-attached Evidence States when required

record attachment rationale

record attachment policy

record attachment provenance

record phenotype context

record uncertainty and conflict status
```

These are compliant discovery and overlay behaviors.

---

# Prohibited Responsibilities

The discovery and overlay subsystem must not:

```text
modify producer artifacts

overwrite source evidence

replace primary evidence

replace overlay evidence

fuse overlay evidence into primary evidence

hide attachment uncertainty

hide phenotype context

perform RDGP reasoning

declare biological causality

silently enrich evidence
```

Discovery and overlay attachment preserve relationships.

They do not rewrite evidence.

---

# Discovery Event Requirements

Every discovery operation that influences VDB state must produce a Discovery Event.

Discovery Events must preserve:

```text
discovery identifier

triggering subsystem

source evidence references

candidate evidence references

discovery rationale

discovery policy version

authority source when applicable

retrieval timestamp when applicable

conflict status

validation status
```

Discovery events must remain reconstructable.

---

# Overlay Attachment Requirements

Overlay attachments must preserve:

```text
primary evidence identity

overlay evidence identity

attachment basis

attachment rationale

attachment policy version

attachment authority

attachment uncertainty

phenotype context when applicable

namespace bridge references when applicable

discovery event references

provenance references
```

Overlay attachments must remain explicit relationships.

Overlay attachments must not fuse evidence.

---

# Cross-Producer Overlay Requirements

Cross-producer overlays must preserve both producer identities.
For example:

```text
VAP evidence
    remains VAP evidence

GSC evidence
    remains GSC evidence

Overlay Attachment
    records the relationship between them
```

The relationship may support downstream query surfaces.

The relationship must not convert GSC evidence into VAP evidence or VAP evidence into GSC evidence.

---

# Namespace Dependency Requirements

Overlay attachment may depend on Namespace Events and Identity Bridges.

When an overlay is attached through a namespace bridge, the attachment must preserve:

```text
source identifier

canonical identifier

identity bridge identifier

resolution status

resolution provenance
```

Overlay attachment must not bypass namespace uncertainty.

---

# Phenotype Context Requirements

Phenotype-scoped overlays must preserve phenotype context.

Examples include:

```text
mitochondrial phenotype context

epilepsy phenotype context

future disease or trait context
```

Phenotype context must not be hidden or treated as globally applicable unless explicitly justified.

---

# External Evidence Requirements

When externally discovered evidence participates in discovery or overlay attachment, it must remain distinguishable from producer evidence.

External evidence must preserve:

```text
external authority

retrieval event

retrieval timestamp

snapshot identity

field-level provenance

attachment status

conflict status
```

External evidence must not silently enrich producer evidence.

---

# Determinism Requirements

Given identical:

```text
preserved evidence

namespace events

identity bridges

discovery policies

overlay policies

schema versions
```

the discovery and overlay subsystem must produce equivalent outputs.

Discovery and overlay behavior must be deterministic.

---

# Anti-Collapse Rules

The discovery and overlay subsystem must not:

```text
collapse primary evidence and overlay evidence

collapse overlay relationship into evidence identity

collapse phenotype context

collapse attachment uncertainty

collapse discovery provenance

collapse producer identity

collapse namespace uncertainty

silently enrich evidence
```

Relationship preservation takes precedence over convenience.

---

# Compliance Criteria

The discovery and overlay subsystem is compliant only if:

```text
Discovery Events remain visible

Overlay Attachments remain visible

primary evidence remains distinguishable

overlay evidence remains distinguishable

attachment rationale remains visible

attachment provenance remains visible

phenotype context remains visible when applicable

namespace bridge provenance remains visible when applicable

uncertainty remains visible

anti-collapse rules are satisfied
```

Failure of any requirement constitutes contract noncompliance.

---

# Relationship To Other Contracts

This contract depends upon:

```text
ingestion_contract.md

persistence_contract.md

namespace_resolution_contract.md
```

and supports:

```text
query_surface_contract.md
```

Discovery and overlay attachment provide the relationship layer that query surfaces expose.

---

# Summary

The discovery and overlay subsystem exists to identify and preserve evidence relationships.

Its purpose is to make evidence interoperable without destroying its origin or meaning.

The guiding principle is:

```text
Discover relationships.

Attach explicitly.

Never fuse evidence.
```
# query_surface_contract.md

## Purpose

This contract defines the obligations, constraints, and expected behaviors of the VDB query surface subsystem.

The query surface subsystem is responsible for exposing preserved evidence to downstream consumers through governed access contracts.

The purpose of query surfaces is to provide structured access to evidence while preserving identity, provenance, authority, uncertainty, and reconstruction capability.

---

# Relationship To System Contract

This contract derives from:

```text
docs/contracts/system_contract.md
```

All query surface behavior must remain compliant with the VDB System Contract.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Core Principle

```text
Query surfaces are derived access contracts.

Query surfaces are not authoritative storage domains.
```

Query surfaces exist to expose evidence.

Query surfaces do not replace preserved evidence.

The authoritative representation of evidence remains persistence.

---

# Scope

This contract governs:

```text
sample-gene evidence retrieval

overlay attachment retrieval

RDGP surface generation

evidence reconstruction retrieval

future consumer-facing evidence surfaces

future export surfaces
```

This contract does not govern:

```text
evidence ingestion

evidence persistence

namespace resolution execution

overlay attachment execution

RDGP reasoning
```

Those responsibilities belong to separate subsystems.

---

# Query Surface Boundary

The query surface subsystem operates at the boundary:

```text
Preserved Evidence
        ↓
Query Surface
        ↓
Consumer
```

Query surfaces expose evidence.

Consumers reason over evidence.

---

# Allowed Responsibilities

The query surface subsystem may:

```text
retrieve Evidence Objects

retrieve Evidence States

retrieve Evidence State Transitions

assemble evidence channels

expose overlays

construct RDGP-ready surfaces

construct export surfaces

provide reconstruction handles

materialize derived views

emit structured outputs
```

These are compliant query surface behaviors.

---

# Prohibited Responsibilities

The query surface subsystem must not:

```text
modify preserved evidence

overwrite preserved evidence

replace preserved evidence

hide provenance

hide uncertainty

hide namespace status

perform biological reasoning

perform RDGP reasoning

fuse overlays into primary evidence

rewrite producer evidence
```

Query surfaces expose evidence.

They do not alter evidence.

---

# Canonical Query Surface Families

The query surface subsystem must support the following canonical query families:

```text
sample_gene_evidence_query

overlay_attachment_query

rdgp_surface_query

evidence_reconstruction_query
```

Future query families may be added without invalidating existing evidence.

---

# Evidence Object Retrieval Requirements

Query surfaces must support retrieval of Evidence Objects.

Retrieved Evidence Objects must preserve:

```text
source identity

producer identity

artifact references

authority class

provenance references
```

Evidence Objects must remain traceable to persistence.

---

# Evidence State Retrieval Requirements

Query surfaces must support retrieval of Evidence States.

Retrieved Evidence States must preserve:

```text
state identity

state type

authority context

uncertainty context

generation context

producer context
```

State history must remain visible.

---

# Evidence State Transition Requirements

Query surfaces must support retrieval of Evidence State Transitions.

Transition visibility must include:

```text
source state

destination state

transition type

transition rationale

transition timestamp
```

Evidence evolution must remain visible.

---

# Overlay Exposure Requirements

Query surfaces must expose overlays as explicit relationships.

Overlay exposure must preserve:

```text
primary evidence identity

overlay evidence identity

attachment rationale

attachment authority

attachment uncertainty
```

Overlays must remain distinguishable from primary evidence.

---

# Namespace Exposure Requirements

Query surfaces must expose namespace information.

Examples include:

```text
source identifier

source namespace

canonical identifier

resolution status

resolution authority

identity bridge identifier
```

Namespace uncertainty must remain visible.

---

# Provenance Exposure Requirements

Query surfaces must expose provenance sufficient to reconstruct:

```text
source repository

source producer

source run

source TEP

source artifact

source evidence object
```

Consumers must be able to evaluate evidence lineage.

---

# Null Semantics Requirements

Query surfaces must preserve semantic distinctions among:

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

# RDGP Surface Requirements

RDGP-facing surfaces must preserve:

```text
sample identifier

gene identifier

source identities

canonical identities

namespace status

evidence channels

overlay participation

uncertainty indicators

provenance references

query surface identifiers

return-path identifiers
```

RDGP surfaces must remain deterministic.

---

# Evidence Reconstruction Requirements

Every query surface must expose reconstruction handles.

Consumers must be able to transition from a query result to:

```text
Evidence Object

Evidence State

Evidence State Transition

source artifact

source TEP

source producer
```

No query surface may become a provenance dead end.

---

# Structured Output Requirements

Query surfaces may emit:

```text
JSON

TSV

CSV

materialized views

future structured formats
```

Output format does not determine authority.

Structured output remains a derived representation.

Persistence remains authoritative.

---

# Query Surface Versioning Requirements

Query surfaces must preserve:

```text
surface version

construction policy version

schema version

generation timestamp
```

Version history must remain visible.

---

# Determinism Requirements

Given identical:

```text
preserved evidence

namespace policies

overlay policies

query surface versions

schema versions
```

the query surface subsystem must produce equivalent outputs.

Query behavior must be deterministic.

---

# Consumer Boundary Requirements

Consumers may:

```text
retrieve evidence

analyze evidence

reason over evidence

export evidence
```

Consumers must not be treated as authoritative evidence sources solely because they consume a query surface.

Consumer outputs must remain distinguishable from VDB evidence.

---

# Anti-Collapse Rules

The query surface subsystem must not:

```text
invert authority between persistence and query surfaces

collapse evidence channels

collapse provenance

collapse namespace history

collapse uncertainty

collapse overlays into evidence

collapse state history

collapse source identity into canonical identity

discard reconstruction paths
```

Evidence fidelity takes precedence over convenience.

---

# Compliance Criteria

The query surface subsystem is compliant only if:

```text
Evidence Objects remain visible

Evidence States remain visible

Evidence State Transitions remain visible

provenance remains visible

namespace status remains visible

overlay relationships remain visible

uncertainty remains visible

reconstruction paths remain visible

determinism requirements are satisfied

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

discovery_overlay_contract.md
```

The query surface subsystem represents the final consumer-facing layer of VDB.

---

# Summary

The query surface subsystem exists to expose preserved evidence without replacing preserved evidence.

Query surfaces provide structured access while preserving identity, provenance, authority, uncertainty, and reconstruction capability.

The guiding principle is:

```text
Expose evidence.

Preserve authority.

Never let the view become the truth.
```

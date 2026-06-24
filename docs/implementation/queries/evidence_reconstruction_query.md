# evidence_reconstruction_query.md

## Purpose

This document defines the canonical evidence reconstruction query surface within the Variant Database (VDB).

The purpose of this query is to reconstruct the complete history, lineage, provenance, identity evolution, overlay relationships, discovery events, and state transitions associated with a preserved evidence object or evidence state.

This query exists to demonstrate that preservation succeeded.

---

# Scope

This query governs reconstruction of:

```text
evidence objects

evidence states

evidence state transitions

source artifacts

source entities

source TEPs

overlay attachments

namespace events

discovery events

query-surface derivations

RDGP round-trip lineage
```

This query defines:

```text
evidence reconstruction

lineage reconstruction

provenance reconstruction

identity reconstruction

overlay reconstruction

state reconstruction
```

This query does not perform:

```text
biological reasoning

gene prioritization

clinical interpretation

evidence scoring

diagnosis
```

---

# Core Question

The canonical question answered by this query is:

```text
Why does this evidence exist?
```

More precisely:

```text
Can this evidence be fully reconstructed?
```

And operationally:

```text
Show me everything that contributed
to this evidence object
or evidence state.
```

---

# Query Philosophy

This query verifies preservation.

Other query surfaces retrieve evidence.

This query reconstructs evidence.

Conceptually:

```text
sample_gene_evidence_query
        →
retrieve evidence

overlay_attachment_query
        →
relate evidence

rdgp_surface_query
        →
prepare evidence

evidence_reconstruction_query
        →
reconstruct evidence
```

---

# Core Principle

```text
Preserved evidence
must remain reconstructable.
```

The purpose of VDB preservation is not storage.

The purpose of VDB preservation is future reconstruction.

This query exists to demonstrate that reconstruction remains possible.

---

# Input Identity

## Required Inputs

Examples:

```text
evidence_object_id

OR

evidence_state_id
```

---

## Additional Supported Inputs

Examples:

```text
tep_id

artifact_id

entity_id

overlay_id

query_surface_id

surface_record_id

namespace_event_id

discovery_event_id
```

The reconstruction process should support multiple entry points.

---

# Reconstruction Model

Evidence reconstruction follows lineage relationships.

Conceptually:

```text
current evidence state
        ↑

state transition

        ↑

prior evidence state

        ↑

source artifact

        ↑

source TEP

        ↑

producer repository
```

The reconstruction model may continue through additional layers.

---

# Reconstruction Domains

Evidence reconstruction evaluates multiple domains.

---

## Evidence Reconstruction

Examples:

```text
evidence object identity

evidence state identity

state composition

state lineage
```

---

## Provenance Reconstruction

Examples:

```text
source repositories

source releases

source runs

source TEPs

source artifacts
```

---

## Identity Reconstruction

Examples:

```text
source identifiers

canonical identifiers

namespace mappings

resolution events
```

---

## Overlay Reconstruction

Examples:

```text
GSC overlays

future RSP overlays

external metadata overlays

future RDGP overlays
```

---

## Discovery Reconstruction

Examples:

```text
BioSample discovery

BioProject discovery

external ontology discovery

future discovery events
```

---

## Surface Reconstruction

Examples:

```text
sample-gene evidence surfaces

RDGP surfaces

future query surfaces
```

---

# Evidence-State Reconstruction

The query should reconstruct:

```text
current state

prior state

transition history

state lineage
```

where available.

---

## Required Outputs

Examples:

```text
state identifier

state type

state timestamp

state authority

state lineage
```

---

# State Transition Reconstruction

Evidence state transitions should remain visible.

Examples:

```text
observation state
        →
annotation state

annotation state
        →
prioritization state

prioritization state
        →
transport state
```

---

## Important Rule

State transitions must not be hidden.

State history must remain reconstructable.

---

# Provenance Reconstruction

The query should reconstruct provenance lineage.

Examples:

```text
repository

release

run

TEP

artifact

entity
```

---

## Provenance Chain

Conceptually:

```text
repository
        ↓

release
        ↓

run
        ↓

TEP
        ↓

artifact
        ↓

evidence state
```

---

## Success Criteria

The provenance chain remains reconstructable.

---

# Namespace Reconstruction

The query should reconstruct namespace activity.

Examples:

```text
source identity

canonical identity

resolution status

resolution authority

resolution event
```

---

## Required Outputs

Examples:

```text
namespace event id

authority source

authority version

resolution status

mapping rationale
```

---

# Overlay Reconstruction

The query should reconstruct overlay relationships.

Examples:

```text
overlay identity

attachment rationale

attachment status

attachment authority

attachment provenance
```

---

## Required Question

The query should answer:

```text
Why was this overlay attached?
```

---

# Discovery Reconstruction

Discovery activity must remain reconstructable.

Examples:

```text
external metadata retrieval

ontology retrieval

registry retrieval

future discovery events
```

---

## Required Outputs

Examples:

```text
discovery event id

retrieval source

retrieval timestamp

authority source

attachment outcome
```

---

# Query-Surface Reconstruction

The query should reconstruct query-surface derivation.

Examples:

```text
sample-gene surface

RDGP surface

future evidence surfaces
```

---

## Required Outputs

Examples:

```text
query_surface_id

query_surface_version

surface construction policy

surface derivation lineage
```

---

# RDGP Round-Trip Reconstruction

The query should support reconstruction across the complete VDB-RDGP lifecycle.

Examples:

```text
VAP-TEP
        →
VDB

VDB
        →
RDGP surface

RDGP surface
        →
RDGP

RDGP
        →
RDGP-TEP

RDGP-TEP
        →
VDB
```

---

## Required Question

The query should answer:

```text
How did this RDGP output come into existence?
```

---

# Human Reconstruction View

The query should support human-readable reconstruction.

Conceptually:

```text
Current Evidence State
        ↓

Source TEP
        ↓

Source Artifacts
        ↓

Producer Repository
```

Human reconstruction should prioritize interpretability.

---

# Machine Reconstruction View

The query should support machine-readable reconstruction.

Conceptually:

```text
nodes

edges

lineage graph

relationship graph
```

Machine reconstruction should prioritize completeness.

---

# Authority Requirements

Reconstruction must preserve authority.

Examples:

```text
producer authority

external authority

VDB-discovered authority

user-supplied authority
```

Authority must remain reconstructable.

---

# Uncertainty Requirements

The query should expose uncertainty history.

Examples:

```text
ambiguous identities

conflicting annotations

unresolved mappings

partial overlays
```

---

## Important Rule

Historical uncertainty must remain visible.

---

# Output Model

The query should expose:

```text
evidence lineage

state lineage

provenance lineage

identity lineage

overlay lineage

discovery lineage

surface lineage
```

The query should not expose only final states.

---

# Relationship To Sample-Gene Evidence Query

Sample-gene queries retrieve evidence.

Evidence reconstruction explains retrieved evidence.

---

# Relationship To Overlay Attachment Query

Overlay attachment queries identify relationships.

Evidence reconstruction explains those relationships.

---

# Relationship To RDGP Surface Query

RDGP surface queries construct reasoning surfaces.

Evidence reconstruction explains how those surfaces were constructed.

---

# Required Invariants

## Invariant 1

Evidence objects remain reconstructable.

---

## Invariant 2

Evidence states remain reconstructable.

---

## Invariant 3

State transitions remain reconstructable.

---

## Invariant 4

Source artifacts remain reconstructable.

---

## Invariant 5

Namespace activity remains reconstructable.

---

## Invariant 6

Overlay activity remains reconstructable.

---

## Invariant 7

Discovery activity remains reconstructable.

---

## Invariant 8

RDGP round-trip lineage remains reconstructable.

---

# Anti-Collapse Rules

## Provenance Collapse Prohibited

Source lineage must not be hidden.

---

## Identity Collapse Prohibited

Identity history must not be hidden.

---

## State Collapse Prohibited

State transitions must not be hidden.

---

## Overlay Collapse Prohibited

Attachment history must not be hidden.

---

## Discovery Collapse Prohibited

Discovery activity must not be hidden.

---

## Surface Collapse Prohibited

Query-surface derivation must not be hidden.

---

## RDGP Collapse Prohibited

Reasoning lineage must not be severed from source evidence.

---

# Success Criteria

The query succeeds when VDB can answer:

```text
Why does this evidence exist?
```

and can demonstrate:

```text
where it originated

how it evolved

what was attached

what was discovered

what identities were brokered

what surfaces were derived
```

without ambiguity.

---

# Summary

The evidence reconstruction query is the preservation verification surface of VDB.

Its purpose is not to retrieve evidence.

Its purpose is to prove that preserved evidence remains reconstructable.

The guiding principle is:

```text
If evidence cannot be reconstructed,

preservation has failed.
```

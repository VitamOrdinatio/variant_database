# Ingestion Orchestration Design

## Purpose

The purpose of the ingestion orchestration layer is to coordinate how evidence enters VDB.

This document does not define transport governance, discovery governance, namespace brokerage governance, or semantic persistence governance individually.

Those concerns are governed elsewhere.

Instead, this document defines how those systems cooperate to transform incoming evidence into persisted and queryable evidence assets.

The ingestion orchestration layer therefore functions as the operational coordinator of VDB evidence intake.

---

## Design Principles

### Understand Before Persist

Incoming evidence should be characterized before persistence decisions occur.

Discovery therefore precedes persistence.

---

### Preserve Before Transform

Evidence should arrive through governed transport mechanisms before any VDB-specific processing occurs.

Transport preservation therefore precedes discovery.

---

### Normalize Additively

Namespace normalization should create relationships rather than replace source identities.

Identity brokerage therefore remains additive.

---

### Route Semantically

Persistence destinations should be determined by semantic meaning rather than repository ownership.

---

### Preserve Provenance

Every orchestration decision should remain reconstructable.

Routing decisions, namespace-resolution events, discovery results, and persistence actions should remain traceable.

---

## Architectural Position

The ingestion orchestration layer occupies the operational space between transport and persistence.

```text
Producer Repository
        ↓

TEP Transport
        ↓

Discovery
        ↓

Validation
        ↓

Namespace Brokerage
        ↓

Persistence Routing
        ↓

Semantic Persistence Domains
        ↓

Query Surface Generation
```

The orchestration layer governs the transitions among these systems.

---

## Inputs

The orchestration layer accepts transported evidence packages.

Primary transport mechanism:

```text
TEP
```

TEPs provide:

* payload preservation
* topology preservation
* provenance preservation
* transport identity
* source artifact manifest preservation

The orchestration layer does not modify TEP semantics.

---

## Discovery Coordination

The first orchestration responsibility is discovery coordination.

Discovery performs:

```text
discover
→ profile
→ map
→ validate
```

The orchestration layer invokes discovery and consumes discovery outputs.

Discovery remains authoritative for artifact characterization.

The orchestration layer remains authoritative for workflow progression.

---

## Validation Coordination

Validation follows discovery.

Validation responsibilities include:

* schema validation
* contract validation
* required-field validation
* provenance validation
* transport validation

Validation outcomes should be deterministic.

Invalid evidence should not proceed to persistence routing.

---

## Namespace Brokerage Coordination

Following validation, orchestration invokes namespace brokerage.

Namespace brokerage remains responsible for:

* canonical identity assignment
* additive normalization
* identity relationship creation
* namespace-resolution events

The orchestration layer must not perform identity mutation.

Identity authority remains external to orchestration.

---

## Persistence Routing

Persistence routing determines where evidence should reside.

Routing decisions are based upon:

* evidence type
* semantic scope
* discovery classification
* namespace relationships
* persistence-domain rules

Routing must not depend upon repository ownership.

Examples:

```text
Variant Evidence
        →
Variant Domain

Semantic Overlay
        →
Overlay Domain

Provenance Event
        →
Provenance Domain
```

This principle preserves semantic persistence architecture.

---

## Overlay Ingestion

Semantic overlays require specialized routing.

Examples include:

```text
GSC phenotype-scoped priors
```

Overlay routing must preserve:

* release identity
* phenotype scope
* semantic channels
* overlay provenance

Overlays should remain attachable after persistence.

---

## Variant Ingestion

Variant-oriented evidence requires preservation of:

* observations
* transcript relationships
* annotation multiplicity
* provenance chains
* semantic partitions

Variant persistence should preserve future reinterpretability.

---

## Provenance Orchestration

The orchestration layer generates ingestion provenance.

Examples include:

```text
ingestion_event_id

discovery_report_id

namespace_resolution_event_id

routing_decision_id

persistence_event_id
```

These records provide reconstructability.

---

## Failure Handling

Orchestration should support deterministic failure states.

Examples include:

### Discovery Failure

Artifact cannot be characterized.

### Validation Failure

Artifact violates contract requirements.

### Namespace Failure

Required identity relationships cannot be established.

### Routing Failure

Persistence destination cannot be determined.

Each failure should produce auditable outcomes.

---

## Query-Surface Coordination

Persistence concludes the primary orchestration workflow.

Following persistence, VDB may generate:

* materialized query surfaces
* overlay attachment surfaces
* discovery-oriented views
* RDGP-facing evidence surfaces

Query generation remains downstream of persistence.

---

## Future Expansion

The orchestration architecture should support future evidence classes.

Examples include:

```text
RSP functional evidence

Future ontology artifacts

Future pathway artifacts

Future cohort artifacts
```

New evidence classes should integrate through routing extension rather than workflow redesign.

---

## Relationship to Discovery Engine

The discovery engine answers:

```text
What is this artifact?
```

The orchestration layer answers:

```text
What happens next?
```

The two systems are complementary rather than redundant.

---

## Relationship to Namespace Brokerage

Namespace brokerage answers:

```text
How do identities relate?
```

The orchestration layer answers:

```text
When should brokerage occur?
```

The two systems remain independent.

---

## Relationship to Semantic Persistence Domains

Semantic persistence domains answer:

```text
Where should evidence live?
```

The orchestration layer answers:

```text
How does evidence arrive there?
```

The two systems remain distinct architectural responsibilities.

---

## Summary

The ingestion orchestration layer serves as the operational coordinator of evidence intake within VDB.

It governs the movement of evidence through:

```text
Transport
        ↓
Discovery
        ↓
Validation
        ↓
Namespace Brokerage
        ↓
Persistence Routing
        ↓
Semantic Persistence
        ↓
Query Surface Exposure
```

while preserving transport integrity, identity authority boundaries, provenance reconstructability, semantic persistence doctrine, and future interpretability.

The orchestration layer therefore functions as the workflow conductor of the VDB evidence lifecycle.

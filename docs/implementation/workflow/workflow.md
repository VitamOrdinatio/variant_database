# VDB Workflow

## Purpose

This document defines the high-level evidence lifecycle workflow for the Variant Database (VDB).

The workflow describes the sequence by which evidence is produced, transported, discovered, validated, brokered, persisted, exposed, consumed, and potentially returned to VDB as new evidence.

This document is a lifecycle guide.

It does not define database schemas, exact field requirements, implementation code, or validation test suites. Those concerns belong to specifications, schemas, implementation plans, and validation documents.

The purpose of this document is to provide a shared operational map for VDB development.

---

## Scope

This workflow covers the full VDB evidence lifecycle:

```text
Producer Evidence Creation
        ↓
TEP Construction
        ↓
TEP Transport
        ↓
Discovery / Profiling
        ↓
Validation
        ↓
Namespace Resolution
        ↓
Persistence Routing
        ↓
Semantic Persistence
        ↓
Query Surface Construction
        ↓
Consumer Access
        ↓
Downstream Reasoning
        ↓
Reasoning TEP Construction
        ↓
Re-Ingestion
```

The workflow is intentionally staged.

Each stage serves a distinct responsibility.

---

## Workflow Principles

### Preserve Before Transform

Evidence should arrive through governed transport mechanisms before VDB-specific processing occurs.

TEP transport preserves source-owned evidence state.

---

### Understand Before Persist

VDB should characterize evidence before persistence decisions occur.

Discovery transforms incoming evidence from unknown artifacts into understood artifacts.

---

### Validate Before Route

Evidence should pass deterministic validation before persistence routing.

Validation prevents silent schema drift, provenance loss, and governance drift.

---

### Broker Additively

Namespace resolution must preserve source identities while creating canonical relationships.

Canonical identities support interoperability but do not replace source identities.

---

### Persist Semantically

Evidence should be organized according to semantic meaning rather than repository ownership.

Persistence domains should preserve future interpretability.

---

### Expose Through Surfaces

Consumers should interact with stable query surfaces rather than raw persistence internals.

Query surfaces provide the boundary between persistence and downstream reasoning.

---

### Reasoning Is Evidence

Downstream reasoning outputs may become new evidence products.

Reasoned outputs should return to VDB through governed transport rather than overwrite prior evidence.

---

## Lifecycle Overview

The VDB evidence lifecycle can be summarized as:

```text
Producer Repositories
          ↓
      Transport
          ↓
      Discovery
          ↓
      Brokerage
          ↓
     Persistence
          ↓
    Query Surfaces
          ↓
Consumer Repositories
          ↓
   Reasoned Evidence
          ↓
   Return Transport
          ↓
         VDB
```

This lifecycle supports both one-way evidence consumption and bidirectional evidence refinement.

---

## Stage 01 — Producer Evidence Creation

### Purpose

Producer repositories generate evidence within their own authority domains.

### Examples

```text
VAP
    observed variant evidence

GSC
    phenotype-scoped semantic priors

RSP
    functional and expression evidence

RDGP
    reasoned prioritization evidence
```

### Inputs

* Biological data
* Curated sources
* Pipeline outputs
* Repository-specific methods
* Repository-specific provenance

### Outputs

* Source artifacts
* Source package identities
* Repository-owned evidence states
* Repository-owned provenance

### Authority

Producer repositories own the meaning of the evidence they generate.

VDB does not replace producer authority.

---

## Stage 02 — TEP Construction

### Purpose

A Transitional Evidence Product packages producer-owned evidence for transport.

### Inputs

* Source artifacts
* Source package identity
* Source artifact manifest
* Evidence topology
* Provenance topology
* Reasoning topology, when applicable

### Outputs

* TEP envelope
* TEP payload
* TEP transport identity
* Source artifact manifest
* Topology-preserving evidence package

### Authority

TEP owns transport governance.

TEP does not reinterpret evidence.

TEP does not normalize identities.

TEP does not broker namespaces.

---

## Stage 03 — TEP Transport

### Purpose

TEP transport moves evidence from a producer repository toward VDB without loss of meaning, provenance, identity, or topology.

### Inputs

* Producer-created TEP

### Outputs

* Transported evidence package available for VDB intake

### Authority

Transport preserves evidence.

Transport does not determine persistence destinations.

Transport does not perform discovery.

Transport does not perform namespace brokerage.

---

## Stage 04 — Discovery / Profiling

### Purpose

Discovery determines what an incoming artifact appears to contain.

### Inputs

* Transported TEP
* TEP metadata
* Source artifact manifest
* Payload structure
* Declared source repository
* Declared artifact class, when available

### Outputs

* Artifact profile
* Column or field profile
* Value-domain profile
* Artifact classification
* Discovery warnings
* Candidate semantic roles

### Authority

Discovery owns evidence characterization.

Discovery does not mutate payloads.

Discovery does not own namespace authority.

Discovery does not persist evidence directly.

---

## Stage 05 — Validation

### Purpose

Validation determines whether discovered evidence is acceptable for progression through the VDB intake workflow.

### Inputs

* Discovery outputs
* Interface expectations
* TEP transport expectations
* Artifact manifest expectations
* Schema expectations, when available
* Provenance expectations

### Outputs

* Validation result
* Validation warnings
* Validation failures
* Acceptance or rejection decision
* Dry-run report, when applicable

### Authority

Validation gates workflow progression.

Invalid evidence should not proceed to persistence routing.

Validation failures should remain auditable.

---

## Stage 06 — Namespace Resolution

### Purpose

Namespace resolution establishes additive identity relationships between source identifiers and canonical identities.

### Inputs

* Validated identifier fields
* Source identifiers
* Source namespaces
* Source artifact context
* Mapping resources
* Mapping versions

### Outputs

* Source identity records
* Canonical identity relationships
* Resolution events
* Mapping status
* Ambiguity state
* Unresolved identity records

### Authority

Namespace resolution owns identity brokerage.

It does not redefine biological meaning.

It does not mutate source evidence.

It does not alter TEP payloads.

---

## Stage 07 — Persistence Routing

### Purpose

Persistence routing determines where evidence belongs within VDB.

### Inputs

* Discovery classifications
* Validation results
* Namespace-resolution outputs
* Evidence type
* Semantic scope
* Persistence-domain rules

### Outputs

* Routing decision
* Destination persistence domain
* Routing provenance
* Routing warnings or failures

### Authority

Routing connects characterized evidence to semantic persistence domains.

Routing should not depend on repository ownership alone.

Routing should not perform reasoning.

---

## Stage 08 — Semantic Persistence

### Purpose

Semantic persistence stores evidence according to durable evidence meaning.

### Inputs

* Validated evidence
* Routing decision
* Namespace relationships
* Provenance records
* Source identities
* Transport metadata

### Outputs

* Persisted evidence records
* Persisted provenance records
* Persisted namespace-resolution records
* Persisted source identity records
* Persisted semantic-domain records

### Authority

VDB owns durable semantic persistence.

VDB preserves evidence as a steward rather than replacing producer authority.

Persistence should preserve future interpretability.

---

## Stage 09 — Query Surface Construction

### Purpose

Query surfaces expose persisted evidence in stable, consumer-oriented forms.

### Inputs

* Persisted evidence
* Semantic persistence domains
* Namespace relationships
* Provenance records
* Overlay records
* Aggregation rules

### Outputs

* Evidence surfaces
* Overlay surfaces
* Aggregation surfaces
* Provenance surfaces
* Discovery surfaces
* RDGP-facing sample-gene surfaces
* Future consumer-facing surfaces

### Authority

Query surfaces organize access.

They do not replace persistence domains.

They do not perform downstream reasoning.

They provide stable consumption boundaries.

---

## Stage 10 — Consumer Access

### Purpose

Consumer repositories access VDB evidence through governed query surfaces.

### Inputs

* Query surfaces
* Consumer-specific evidence requirements
* Consumer identity model
* Consumer provenance requirements

### Outputs

* Consumer-ready evidence packages
* VDB-outbound TEPs, when transportable evidence packages are needed
* Query results
* Evidence bundles

### Authority

VDB exposes evidence.

Consumer repositories interpret evidence according to their own responsibility domains.

---

## Stage 11 — Downstream Reasoning

### Purpose

A consumer repository may perform reasoning over VDB-provided evidence.

### Example

```text
RDGP
    consumes sample-gene evidence
    performs candidate prioritization
    produces confidence assessments
    produces inheritance interpretations
```

### Inputs

* VDB query surfaces
* VDB-outbound TEPs, when applicable
* Consumer-specific configuration
* Consumer-specific reasoning models

### Outputs

* Reasoning outputs
* Candidate rankings
* Confidence assessments
* Interpretation artifacts
* Reasoning provenance

### Authority

Consumer repositories own reasoning.

VDB does not perform repository-specific downstream reasoning.

---

## Stage 12 — Reasoning TEP Construction

### Purpose

Reasoning outputs may be packaged as new evidence products for return to VDB.

### Inputs

* Downstream reasoning outputs
* Reasoning provenance
* Source evidence inputs
* Consumer methodology
* Temporal context

### Outputs

* RDGP-TEP or other consumer-generated TEP
* Reasoning payload
* Reasoning provenance
* Source evidence lineage
* Transport identity

### Authority

The consumer repository owns the reasoning product.

TEP owns transport preservation.

Reasoning products should be treated as new evidence rather than updates to prior evidence.

---

## Stage 13 — Re-Ingestion

### Purpose

VDB may ingest returned reasoning products as new persisted evidence classes.

### Inputs

* Consumer-generated TEP
* Reasoning payload
* Reasoning provenance
* Prior source evidence lineage
* Temporal context

### Outputs

* Persisted reasoning evidence
* Historical reasoning records
* Updated query surfaces, when appropriate
* Longitudinal evidence context

### Authority

VDB persists reasoning evidence without overwriting underlying evidence.

Returned reasoning products coexist alongside observed evidence and semantic prior evidence.

---

## Failure and Deferral States

The workflow should support deterministic failure and deferral states.

### Discovery Failure

The artifact cannot be characterized.

### Validation Failure

The artifact violates transport, schema, provenance, or interface requirements.

### Namespace Resolution Deferral

A source identity cannot yet be resolved but should remain preserved.

### Routing Failure

A valid artifact cannot be assigned to a semantic persistence domain.

### Persistence Failure

A routed artifact cannot be persisted safely.

### Query Surface Deferral

Evidence has been persisted but is not yet exposed through a stable consumer surface.

### Re-Ingestion Deferral

Returned reasoning evidence is preserved but not yet integrated into downstream query surfaces.

Failure and deferral states should produce auditable records rather than silent loss.

---

## Evidence Classes Across the Workflow

VDB should support multiple evidence classes across the workflow.

```text
Observed Evidence
    VAP variant observations
    future RSP expression observations

Aggregated Semantic Evidence
    GSC phenotype-gene priors
    release-scoped semantic overlays

Reasoned Evidence
    RDGP candidate rankings
    confidence assessments
    inheritance interpretations
```

These evidence classes should remain distinct while still supporting interoperability.

---

## Traceability to Implementation Artifacts

The workflow should remain traceable to later implementation documents.

Representative traceability:

```text
Stage 02 — TEP Construction
    implementation/specifications/tep_spec.md

Stage 04 — Discovery / Profiling
    implementation/specifications/discovery_report_spec.md
    implementation/schemas/discovery_schema.md

Stage 05 — Validation
    validation/schema_validation.md
    validation/ingestion_validation.md

Stage 06 — Namespace Resolution
    implementation/specifications/namespace_resolution_spec.md
    implementation/schemas/provenance_schema.md

Stage 07 — Persistence Routing
    implementation/specifications/ingestion_event_spec.md

Stage 08 — Semantic Persistence
    implementation/schemas/relational_schema.md
    implementation/schemas/data_schema.md

Stage 09 — Query Surface Construction
    implementation/schemas/rdgp_query_surface_schema.md

Stage 13 — Re-Ingestion
    implementation/specifications/provenance_spec.md
    implementation/specifications/ingestion_event_spec.md
```

This workflow provides the lifecycle backbone for later specifications and schemas.

---

## Non-Goals

This document does not define:

* exact database tables
* exact columns
* exact JSON structures
* exact TSV layouts
* exact validation tests
* exact SQL queries
* code-level implementation steps
* deployment procedures

Those concerns belong to other implementation, schema, query, validation, or plan documents.

---

## Summary

VDB operates as a staged evidence lifecycle system.

Evidence is produced by responsibility-scoped repositories, transported through TEPs, characterized by discovery, checked through validation, related through namespace brokerage, routed into semantic persistence domains, exposed through query surfaces, consumed by downstream systems, and potentially returned as new reasoning evidence.

The central workflow doctrine is:

```text
Preserve before transform.
Understand before persist.
Validate before route.
Broker additively.
Persist semantically.
Expose through surfaces.
Treat reasoning as evidence.
```

This lifecycle enables VDB to preserve biological meaning, provenance, identity, uncertainty, and future interpretability across repository boundaries and across time.

# query_surface_plan.md

## Purpose

This document defines the implementation plan for the VDB query surface subsystem.

The query surface subsystem is responsible for exposing preserved evidence through governed access contracts while preserving identity, provenance, authority, uncertainty, and reconstruction capability.

This plan translates:

```text
docs/contracts/query_surface/query_surface_contract.md
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
docs/contracts/query_surface/query_surface_contract.md
```

The query surface subsystem represents the primary consumer-facing layer of VDB.

---

# Implementation Goal

The goal of the query surface subsystem is:

```text
Provide deterministic access to preserved evidence
without converting query results into authoritative evidence.
```

Query surfaces exist to expose evidence.

Query surfaces do not replace evidence.

---

# Query Surface Philosophy

The query surface subsystem operates under the principle:

```text
Query surfaces are derived access contracts.

Query surfaces are not authoritative storage domains.
```

The following remain authoritative:

```text
Evidence Objects

Evidence States

Evidence State Transitions

Artifacts

TEP Packages

Metadata Records

Provenance Records
```

Query outputs are derived representations.

Persistence remains authoritative.

---

# Consumer Classes

The query surface subsystem must support multiple consumer classes.

---

## Human Consumers

Examples include:

```text
developers

scientists

curators

reviewers

validators
```

---

## Machine Consumers

Examples include:

```text
RDGP

future RSP integrations

future downstream repositories

future external systems
```

The same evidence may be exposed through multiple consumer-specific surfaces.

---

# Query Surface Record Strategy

Every query execution should produce a query surface record.

Minimum fields include:

```text
query_surface_id

query_surface_version

query_policy_version

generation_timestamp

source_domain_references
```

Query Surface Records support:

```text
reproducibility

reconstruction

auditability

validation
```

---

# Query Surface Construction Strategy

Query surfaces should retrieve evidence from persistence.

Query surfaces should not create authoritative evidence.

The preferred flow is:

```text
Persistence
        ↓
Evidence Retrieval
        ↓
Derived Query Surface
        ↓
Consumer
```

The query layer must remain thin.

Business logic should remain within upstream subsystems.

---

# Phase 1 — Sample Gene Evidence Query

## Purpose

Implement the canonical evidence retrieval surface.

## Query Specification

```text
docs/implementation/queries/sample_gene_evidence_query.md
```

## Purpose

Support retrieval of all preserved evidence associated with:

```text
sample_id

gene_id
```

or equivalent identifiers.

---

## Expected Work

Implement:

```text
Evidence Object retrieval

Evidence State retrieval

namespace status retrieval

overlay visibility

provenance visibility

uncertainty visibility
```

---

## Example Benchmark

```text
HG002

POLG
```

---

## Expected Outputs

```text
sample-gene evidence surface

structured JSON output

query surface record

validation output
```

---

## Exit Criteria

```text
all evidence channels visible

provenance visible

namespace status visible

uncertainty visible

reconstruction handles visible
```

---

# Phase 2 — Overlay Attachment Query

## Purpose

Implement cross-producer evidence exposure.

## Query Specification

```text
docs/implementation/queries/overlay_attachment_query.md
```

## Purpose

Expose relationships between:

```text
primary evidence

overlay evidence
```

without merging them.

---

## Expected Work

Implement:

```text
overlay retrieval

overlay attachment visibility

attachment rationale visibility

phenotype context visibility

overlay provenance visibility
```

---

## Example Benchmark

```text
HG002 POLG VAP evidence

+

Mitochondrial POLG GSC overlay
```

---

## Expected Outputs

```text
overlay attachment surface

attachment relationship records

query surface record
```

---

## Exit Criteria

```text
overlay remains distinguishable

primary evidence remains distinguishable

attachment rationale visible

attachment provenance visible
```

---

# Phase 3 — RDGP Surface Query

## Purpose

Implement the consumer contract for RDGP.

## Query Specification

```text
docs/implementation/queries/rdgp_surface_query.md
```

## Purpose

Prepare evidence for downstream RDGP consumption.

VDB prepares evidence.

RDGP performs reasoning.

---

## Expected Work

Implement:

```text
sample-gene evidence assembly

namespace visibility

overlay participation visibility

provenance visibility

uncertainty visibility

return-path visibility
```

---

## Expected Outputs

```text
RDGP-ready JSON surface

RDGP-ready TSV surface when appropriate

surface manifest

query surface record
```

---

## Exit Criteria

```text
RDGP requirements satisfied

surface deterministic

surface provenance-complete

surface namespace-aware

surface reconstruction-ready
```

---

# Phase 4 — Evidence Reconstruction Query

## Purpose

Implement reconstruction verification.

## Query Specification

```text
docs/implementation/queries/evidence_reconstruction_query.md
```

## Purpose

Demonstrate that preserved evidence remains reconstructable.

---

## Expected Work

Implement reconstruction of:

```text
TEP Package

Artifact

Entity

Evidence Object

Evidence State

Evidence State Transition

Namespace Event

Overlay Attachment

Query Surface Derivation
```

---

## Expected Outputs

```text
reconstruction report

reconstruction graph

lineage traversal output

query surface record
```

---

## Exit Criteria

```text
source lineage reconstructable

state lineage reconstructable

namespace lineage reconstructable

overlay lineage reconstructable

query lineage reconstructable
```

---

# Query Surface Versioning Strategy

Every query surface must preserve:

```text
surface version

query policy version

schema version

generation timestamp
```

Version history must remain visible.

---

# Query Surface Promotion Criteria

New query surfaces may be added only when supported by:

```text
contracts

schemas

validation doctrine

reconstruction capability
```

Ad hoc query surfaces are prohibited.

Every query surface must have:

```text
documented purpose

defined consumer

defined provenance behavior

defined reconstruction behavior
```

---

# Test Strategy

Query surface tests must verify:

```text
Evidence Object visibility

Evidence State visibility

Evidence State Transition visibility

namespace visibility

overlay visibility

provenance visibility

uncertainty visibility

determinism

reconstruction capability
```

---

# Validation Gates

The query surface subsystem must satisfy:

```text
docs/validation/schema_validation.md

docs/validation/vdb_end_to_end_lifecycle_walkthrough.md
```

Required gates include:

```text
evidence exposure

provenance exposure

namespace exposure

overlay exposure

reconstruction exposure

determinism
```

---

# Anti-Collapse Checks

The query surface subsystem must verify that implementation does not:

```text
replace persistence

hide provenance

hide uncertainty

hide namespace status

hide overlays

hide state history

hide reconstruction paths

promote query outputs to authoritative evidence

collapse evidence channels

collapse producer identity
```

These checks are mandatory.

---

# Benchmark Lifecycle Alignment

The query surface subsystem must support:

```text
docs/examples/vdb_evidence_lifecycle_example.md
```

Specifically:

```text
sample_gene_evidence_query

↓

overlay_attachment_query

↓

rdgp_surface_query

↓

evidence_reconstruction_query
```

This sequence represents the benchmark consumer path through VDB.

---

# Definition Of Done

The query surface subsystem is complete when:

```text
sample_gene_evidence_query implemented

overlay_attachment_query implemented

rdgp_surface_query implemented

evidence_reconstruction_query implemented

Query Surface Records exist

provenance remains visible

namespace status remains visible

overlay relationships remain visible

reconstruction paths remain visible

validation passes

anti-collapse checks pass
```

The query surface subsystem is not complete merely because query results can be generated.

---

# Summary

The query surface subsystem exists to expose preserved evidence while preserving authority boundaries.

Its purpose is to provide deterministic evidence access without compromising reconstruction capability.

The guiding implementation rule is:

```text
Expose evidence.

Preserve provenance.

Preserve identity.

Never let the view become the truth.
```

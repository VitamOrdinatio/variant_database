# implementation_plan.md

## Purpose

This document defines the master implementation plan for the Variant Database (VDB).

The purpose of this plan is to translate VDB contracts, schemas, validation doctrine, and query-surface specifications into an executable implementation sequence.

This plan governs implementation order, dependency structure, validation gates, and definitions of done.

---

# Governing Contracts

Implementation must comply with:

```text
docs/contracts/system_contract.md

docs/contracts/ingestion/ingestion_contract.md

docs/contracts/persistence/persistence_contract.md

docs/contracts/namespace_governance/namespace_resolution_contract.md

docs/contracts/discovery_overlay/discovery_overlay_contract.md

docs/contracts/query_surface/query_surface_contract.md
```

The System Contract governs all implementation work.

Subsystem contracts govern their corresponding implementation phases.

If any subsystem contract conflicts with the System Contract, the System Contract takes precedence.

---

# Governing Satellite Plans

Implementation is further guided by subsystem-specific satellite plans:

```text
docs/plans/ingestion/ingestion_plan.md

docs/plans/persistence/persistence_plan.md

docs/plans/namespace_governance/namespace_resolution_plan.md

docs/plans/discovery_overlay/discovery_overlay_plan.md

docs/plans/query_surface/query_surface_plan.md
```

Satellite plans translate subsystem contracts into executable implementation sequences.

The master implementation plan governs phase order.

Satellite plans govern phase execution details.

---

# Governing Schemas

Implementation must preserve the architecture defined by:

```text
docs/implementation/schemas/metadata_schema.md

docs/implementation/schemas/provenance_schema.md

docs/implementation/schemas/data_schema.md

docs/implementation/schemas/relational_schema.md

docs/implementation/schemas/discovery_schema.md

docs/implementation/schemas/rdgp_query_surface_schema.md
```

Schemas define the logical architecture.

Implementation may choose practical physical representations, but must preserve logical domains.

---

# Governing Validation Documents

Implementation must satisfy:

```text
docs/validation/validation_strategy.md

docs/validation/schema_validation.md

docs/validation/ingestion_validation.md

docs/validation/namespace_resolution_validation.md

docs/validation/vdb_end_to_end_lifecycle_walkthrough.md
```

Validation confirms preservation behavior.

Validation does not confirm biological correctness.

---

# Governing Query Specifications

Implementation must support the query behavior defined by:

```text
docs/implementation/queries/sample_gene_evidence_query.md

docs/implementation/queries/overlay_attachment_query.md

docs/implementation/queries/rdgp_surface_query.md

docs/implementation/queries/evidence_reconstruction_query.md
```

Query surfaces expose preserved evidence.

Query surfaces must not replace preserved evidence.

---

# Implementation Philosophy

VDB implementation must proceed preservation-first.

The initial implementation goal is not to build every consumer-facing query.

The initial implementation goal is to prove that certified producer evidence can enter VDB custody without loss of identity, provenance, authority, evidence topology, uncertainty, or reconstructability.

---

# Implementation Sequence

Implementation proceeds through the following phases:

```text
Phase 0
    Repository implementation skeleton

Phase 1
    Read-only TEP intake and ingestion registry

Phase 2
    Persistence layer and logical domain records

Phase 3
    Evidence Object and Evidence State construction

Phase 4
    Namespace governance

Phase 5
    Discovery and overlay attachment bridge

Phase 6
    Core query surface construction

Phase 7
    RDGP query surface emission

Phase 8
    Evidence reconstruction query surface

Phase 9
    End-to-end lifecycle validation
```

Each phase must satisfy its exit criteria before the next phase becomes authoritative.

Subsystem satellite plans provide detailed execution guidance for their corresponding phases.

---

# Phase 0 — Repository Implementation Skeleton

## Purpose

Create the minimum implementation scaffold for VDB code.

## Expected Work

```text
create src package structure

create tests structure

create CLI entry points

create configuration conventions

create fixture conventions

create report output conventions
```

## Expected Outputs

```text
src/variant_database/

tests/

scripts/

pyproject.toml or equivalent package configuration

initial CLI command

baseline test suite
```

## Exit Criteria

```text
package imports successfully

test suite runs

CLI smoke test passes

no producer artifacts are required yet
```

---

# Phase 1 — Read-Only TEP Intake And Ingestion Registry

## Purpose

Implement read-only inspection of certified producer TEPs.

## Expected Work

```text
read TEP-VAP package structure

read TEP-GSC package structure

identify package manifests

identify artifacts

identify entities

compute or read checksums where appropriate

create ingestion event records

emit ingestion report
```

## Initial Targets

```text
HG002 TEP-VAP

Epilepsy TEP-GSC

Mitochondrial TEP-GSC
```

## Required Safety Constraint

Producer artifacts must not be mutated.

## Expected Outputs

```text
ingestion report

TEP package registry

artifact registry

entity registry

validation status
```

## Exit Criteria

```text
certified TEPs can be inspected read-only

ingestion report is deterministic

producer artifact paths remain unchanged

artifact and entity inventories are reconstructable
```

---

# Phase 2 — Persistence Layer And Logical Domain Records

## Purpose

Create durable storage for VDB logical domains.

## Expected Work

```text
define persistence backend

create metadata records

create provenance records

create artifact records

create entity records

create TEP package records

create schema/version metadata
```

## Expected Outputs

```text
persistent VDB store

metadata domain records

provenance domain records

package/artifact/entity records

persistence validation report
```

## Exit Criteria

```text
logical domains remain distinguishable

source artifacts remain immutable

metadata is reconstructable

provenance is reconstructable

schema validation passes
```

---

# Phase 3 — Evidence Object And Evidence State Construction

## Purpose

Construct first-class Evidence Objects and initial Evidence States.

## Expected Work

```text
parse evidence-bearing entities

classify evidence domains

create Evidence Object records

create initial Evidence State records

create Evidence State Transition records for ingestion registration

preserve row/artifact traceability
```

## Initial Evidence Domains

```text
VAP variant evidence

VAP coding interpretation evidence

VAP noncoding interpretation evidence

VAP validation evidence

GSC phenotype-gene semantic prior evidence

GSC gene provenance evidence
```

## Expected Outputs

```text
Evidence Object registry

Evidence State registry

Evidence State Transition registry

source artifact references

source row references where practical
```

## Exit Criteria

```text
Evidence Objects exist

initial Evidence States exist

evidence states are traceable to artifacts

state creation is deterministic

no evidence channels are collapsed
```

---

# Phase 4 — Namespace Governance

## Purpose

Implement safe namespace resolution and identity bridging.

## Expected Work

```text
preserve source identifiers

classify source namespaces

attach canonical identifiers

create Namespace Events

create Identity Bridges

preserve resolution status

preserve resolution provenance
```

## Initial Target

```text
POLG
ENSG00000140521
```

## Required Safety Constraint

Canonical identifiers must not replace source identifiers.

## Expected Outputs

```text
Namespace Event records

Identity Bridge records

resolution status records

namespace validation report
```

## Exit Criteria

```text
source identity remains visible

canonical identity is additive

resolution provenance is visible

ambiguous/conflicted states can be represented

namespace validation passes
```

---

# Phase 5 — Discovery And Overlay Attachment Bridge

## Purpose

Implement the first cross-producer discovery and overlay relationship path.

This phase implements:

```text
docs/contracts/discovery_overlay/discovery_overlay_contract.md

docs/plans/discovery_overlay/discovery_overlay_plan.md
```

Discovery identifies candidate evidence relationships.

Overlay attachment records those relationships.

Neither discovery nor overlay attachment rewrites evidence.

## Prerequisites

This phase requires completion of:

```text
Phase 1
    Read-only TEP intake and ingestion registry

Phase 2
    Persistence layer and logical domain records

Phase 3
    Evidence Object and Evidence State construction

Phase 4
    Namespace governance
```

Discovery and overlay attachment must not become authoritative until preserved evidence, Evidence States, Namespace Events, and Identity Bridges are available.

## Expected Work

```text
discover VAP-GSC gene identity bridge

identify GSC overlays for VAP evidence

create Discovery Events

create Overlay Attachment records

preserve attachment rationale

preserve phenotype context

preserve attachment provenance

preserve namespace bridge references

create overlay-attached Evidence States when required

create Evidence State Transitions when required
```

## Initial Benchmark

```text
HG002 POLG VAP evidence

mitochondrial POLG GSC semantic evidence
```

## Expected Outputs

```text
Discovery Event records

Overlay Attachment records

overlay-attached Evidence State records when required

Evidence State Transition records when required

overlay attachment report

discovery and overlay validation report
```

## Exit Criteria

```text
overlay remains distinct from primary evidence

primary evidence remains reconstructable

overlay evidence remains reconstructable

attachment rationale is visible

phenotype context is preserved

namespace bridge provenance is visible

attachment provenance is visible

VAP evidence is not overwritten

GSC evidence is not merged into VAP evidence

discovery and overlay anti-collapse checks pass
```

---

# Phase 6 — Core Query Surface Construction

## Purpose

Implement governed core query surfaces.

This phase implements human- and system-facing evidence retrieval surfaces while preserving the authority boundary between persistence and query outputs.

Query surfaces expose preserved evidence.

Query surfaces do not replace preserved evidence.

## Expected Work

```text
sample-gene evidence retrieval

overlay attachment retrieval

structured output generation

query surface record creation

query surface validation
```

## Expected Outputs

```text
sample_gene_evidence output

overlay_attachment output

query surface records

query surface validation reports
```

## Exit Criteria

```text
query surfaces expose Evidence Objects

query surfaces expose Evidence States

query surfaces expose Evidence State Transitions

query surfaces expose provenance

query surfaces expose namespace status

query surfaces expose uncertainty

query surfaces expose overlay participation

query surfaces expose reconstruction handles

query surfaces remain derived access contracts
```

---

# Phase 7 — RDGP Query Surface Emission

## Purpose

Emit deterministic RDGP-ready evidence surfaces.

The RDGP-facing surface is a governed query surface.

VDB prepares evidence for RDGP.

RDGP reasons over evidence.

## Expected Work

```text
construct sample-gene RDGP records

include evidence channels

include overlay participation

include provenance handles

include namespace status

include uncertainty indicators

include return-path identifiers

create query surface derivation records
```

## Expected Outputs

```text
RDGP-ready JSON surface

RDGP-ready TSV surface when appropriate

surface manifest

query surface record

surface validation report
```

## Exit Criteria

```text
RDGP surface is deterministic

surface is sample-gene centered

surface is provenance-complete

surface is namespace-aware

surface is uncertainty-aware

surface is overlay-aware

surface is return-path-ready

surface remains reconstructable

VDB does not perform RDGP reasoning
```

---

# Phase 8 — Evidence Reconstruction Query Surface

## Purpose

Implement evidence reconstruction as the preservation verification query surface.

The reconstruction surface proves that query outputs remain connected to preserved evidence.

## Expected Work

```text
reconstruct from Evidence Object

reconstruct from Evidence State

reconstruct from Evidence State Transition

reconstruct from TEP package

reconstruct from artifact

reconstruct from namespace event

reconstruct from identity bridge

reconstruct from discovery event

reconstruct from overlay attachment

reconstruct from query surface record

reconstruct from promoted index when applicable
```

## Expected Outputs

```text
human-readable reconstruction report

machine-readable reconstruction graph

lineage validation report

query surface record
```

## Exit Criteria

```text
source repository reconstructable

source TEP reconstructable

source artifact reconstructable

source evidence object reconstructable

state history reconstructable

namespace history reconstructable

identity bridge history reconstructable

discovery history reconstructable

overlay history reconstructable

query-surface derivation reconstructable

field-promotion history reconstructable when applicable
```

---

# Phase 9 — End-To-End Lifecycle Validation

## Purpose

Execute the complete VDB lifecycle against the benchmark example.

## Benchmark Scenario

```text
HG002 POLG lifecycle

TEP-VAP
    →
VDB ingestion
    →
Evidence Object
    →
Evidence State
    →
Namespace Resolution
    →
GSC Overlay Attachment
    →
Sample-Gene Evidence Query
    →
RDGP Surface
    →
Evidence Reconstruction
```

## Expected Outputs

```text
end-to-end validation report

architecture compliance report

contract compliance report

benchmark comparison against docs/examples/vdb_evidence_lifecycle_example.md
```

## Exit Criteria

```text
system contract satisfied

mini-contracts satisfied

lifecycle walkthrough satisfied

benchmark exemplar matched or deviations explained

evidence remains reconstructable
```

---

# Implementation Stop Conditions

Implementation must stop and return to design if any of the following occur:

```text
producer artifacts require mutation

source identities would be overwritten

provenance cannot be reconstructed

Evidence Objects cannot be distinguished from Evidence States

namespace resolution requires source identity replacement

discovery requires silent enrichment

overlay attachment requires fusion with primary evidence

overlay attachment hides phenotype context

external evidence cannot remain distinguishable from producer evidence

query surfaces become authoritative storage

RDGP reasoning leaks into VDB

validation cannot explain evidence origin
```

Stop conditions indicate architectural or implementation design failure.

---

# Testing Strategy

Each phase must include tests for:

```text
positive path behavior

anti-collapse behavior

determinism

provenance preservation

identity preservation

schema conformance

contract compliance
```

Tests must prefer small fixtures when possible.

Large MARK-hosted producer artifacts may be inspected through read-only probes or controlled fixture extraction.

---

# Fixture Strategy

Implementation should use three fixture tiers:

```text
Tier 1
    synthetic minimal fixtures

Tier 2
    small real producer-derived fixtures

Tier 3
    MARK-hosted certified producer TEP probes
```

Tier 1 supports fast local unit tests.

Tier 2 supports realistic integration tests.

Tier 3 supports production realism without requiring multi-gigabyte artifacts in Git.

---

# Initial Benchmark Artifacts

Initial benchmark development is anchored by:

```text
HG002 TEP-VAP
    run_2026_06_03_010030

Epilepsy TEP-GSC
    run_2026_06_22_184534

Mitochondrial TEP-GSC
    run_2026_06_23_015533
```

These artifacts establish the initial real-world implementation target.

---

# Definitions Of Done

A phase is complete only when:

```text
implementation exists

tests exist

contract compliance is demonstrated

validation output is generated

documentation assumptions remain valid

anti-collapse checks pass
```

A phase is not complete merely because code runs.

---

# Implementation Priority

The first implementation priority is:

```text
read-only certified TEP intake
```

The first success condition is:

```text
VDB can inspect certified producer TEPs
without mutation
and emit deterministic ingestion reports.
```

Only after this succeeds should persistence and downstream evidence construction become authoritative.

---

# Summary

This implementation plan defines the master sequence for moving VDB from architecture into code.

The guiding implementation rule is:

```text
Build custody first.

Build persistence second.

Build evidence state preservation third.

Build interoperability fourth.

Build governed relationships fifth.

Build query surfaces last.

Validate everything.
```
# rdgp_surface_query.md

## Purpose

This document defines the canonical RDGP-facing query surface within the Variant Database (VDB).

The purpose of this query is to construct a governed, deterministic, provenance-complete evidence surface suitable for downstream Rare Disease Gene Prioritization (RDGP) reasoning.

This query prepares evidence for reasoning.

This query does not perform reasoning.

---

# Scope

This query governs construction of:

```text
RDGP-facing evidence surfaces

sample-gene evidence collections

overlay-enriched evidence collections

reasoning-ready evidence exports

TEP-VDB outbound reasoning substrates
```

This query defines:

```text
surface construction

evidence channel inclusion

overlay inclusion

aggregation behavior

namespace behavior

surface provenance

surface identity
```

This query does not perform:

```text
gene prioritization

inheritance reasoning

mechanistic reasoning

confidence assignment

clinical interpretation

causal inference
```

Those responsibilities belong to RDGP.

---

# Core Question

The canonical question answered by this query is:

```text
What governed evidence surface
should VDB emit for RDGP?
```

More precisely:

```text
What collection of sample-gene evidence states

should be exposed to RDGP

for deterministic downstream reasoning?
```

---

# Query Philosophy

This query constructs a reasoning-ready evidence surface.

The query does not determine biological meaning.

The query prepares preserved evidence for consumption by RDGP.

Conceptually:

```text
VDB
        →
evidence preparation

RDGP
        →
evidence reasoning
```

---

# Relationship To RDGP Query Surface Schema

This query implements the operational construction behavior described by:

```text
rdgp_query_surface_schema.md
```

The schema defines:

```text
what must exist
```

This query defines:

```text
how the surface is constructed
```

---

# Relationship To Sample-Gene Evidence Query

This query is built from sample-gene evidence states.

Conceptually:

```text
sample_gene_evidence_query
        ↓

sample-gene evidence state
        ↓

RDGP surface construction
        ↓

RDGP-facing evidence collection
```

This query does not redefine sample-gene retrieval behavior.

---

# Relationship To Overlay Attachment Query

This query consumes overlay attachment outputs.

Examples:

```text
GSC overlays

future RSP overlays

external metadata overlays

future RDGP overlays
```

Overlay attachment logic is governed by:

```text
overlay_attachment_query.md
```

---

# Core Construction Model

Conceptually:

```text
preserved evidence states
        ↓

overlay attachment
        ↓

surface construction
        ↓

RDGP-facing evidence surface
```

Evidence states remain authoritative.

The RDGP surface remains a derived representation.

---

# Input Scope

## Sample Scope

Examples:

```text
single sample

cohort

run

study

release
```

---

## Gene Scope

Examples:

```text
all genes

candidate genes

phenotype-associated genes

user-specified genes
```

---

## Phenotype Scope

Examples:

```text
epilepsy

mitochondrial disease

multiple phenotype contexts

unspecified phenotype
```

---

## Source Scope

Examples:

```text
specific TEPs

specific releases

specific repositories

specific producer families
```

---

# Surface Grain

The canonical surface grain is:

```text
sample_id
        ×
gene_id
```

Optionally:

```text
sample_id
        ×
gene_id
        ×
phenotype_context
```

when phenotype-scoped overlays participate.

---

# Deterministic Construction Requirements

Surface construction must be deterministic.

Equivalent inputs must produce equivalent outputs.

Examples:

```text
same evidence

same policies

same overlays

same schema versions

same scope
```

must yield:

```text
same surface
```

---

## Surface Identity

Every emitted surface must expose:

```text
query_surface_id

query_surface_version

surface_construction_timestamp

aggregation_policy_version

namespace_policy_version

overlay_policy_version

null_semantics_policy_version
```

---

# Evidence Channels

Evidence channels remain decomposed.

Examples:

```text
variant_evidence

gsc_overlay_evidence

transcriptomic_evidence

inheritance_evidence

mechanism_evidence

quality_evidence

identity_resolution_evidence

provenance_evidence

uncertainty_evidence
```

---

## Important Rule

Evidence channels must not be collapsed into a single support score.

---

# Overlay Inclusion

Overlay inclusion is policy-controlled.

Examples:

```text
include GSC overlays

exclude GSC overlays

include external context

include transcriptomic overlays

include pathway overlays
```

Overlay inclusion decisions must remain visible.

---

# Aggregation Policy

Aggregation policy must remain explicit.

Examples:

```text
variant burden policy

annotation precedence policy

overlay inclusion policy

surface eligibility policy
```

The surface must expose policy versions.

---

# Namespace Policy

Namespace behavior must remain explicit.

The surface must expose:

```text
namespace_policy_version

namespace_resolution_status

identity_bridge_summary
```

Identity uncertainty must remain visible.

---

# Null Semantics

The surface must preserve:

```text
unknown

missing

not_evaluated

ambiguous

conflicted

no_match

measured_zero
```

These states must not be collapsed.

---

# Phenotype Context

When phenotype-scoped overlays are attached, the surface must expose:

```text
phenotype identifier

phenotype authority

phenotype source

phenotype overlay status

phenotype match status
```

---

## Important Rule

Phenotype mismatch must remain visible.

Phenotype absence must remain distinguishable from phenotype conflict.

---

# Future Discovery Support

The surface should support future evidence domains.

Examples:

```text
transcriptomic evidence

network evidence

pathway evidence

regulatory evidence

noncoding evidence

future reasoning overlays
```

Unknown future evidence domains must not require redesign of the surface.

---

# Output Forms

## Authoritative Output

The authoritative representation is:

```text
structured evidence object

nested JSON
```

---

## Execution Output

Execution-oriented representations may include:

```text
TSV

tabular exports

materialized views
```

Execution outputs remain derived surfaces.

---

# Provenance Requirements

Every surface record must remain traceable.

Examples:

```text
source repositories

source TEPs

source artifacts

source evidence states

overlay attachments

namespace events
```

The surface must not become a provenance dead end.

---

# Return-Path Identifiers

The RDGP surface must support future RDGP re-ingestion.

Every surface should expose:

```text
tep_vdb_id

query_surface_id

query_surface_version

surface_record_id

surface_export_id
```

These identifiers support future:

```text
RDGP-TEP
        →
VDB
```

round trips.

---

# Non-Goals

This query does not:

```text
prioritize genes

rank candidates

infer inheritance

assign confidence

generate explanations

perform diagnosis
```

Those actions belong to RDGP.

---

# Required Invariants

## Invariant 1

Surface construction remains deterministic.

---

## Invariant 2

Evidence states remain reconstructable.

---

## Invariant 3

Evidence channels remain distinguishable.

---

## Invariant 4

Overlay participation remains visible.

---

## Invariant 5

Namespace uncertainty remains visible.

---

## Invariant 6

Phenotype context remains visible.

---

## Invariant 7

Provenance remains reconstructable.

---

## Invariant 8

The surface remains suitable for RDGP return-path integration.

---

# Anti-Collapse Rules

## Evidence-State Collapse Prohibited

Surface construction must not destroy evidence-state structure.

---

## Overlay Collapse Prohibited

Attached overlays must remain distinguishable.

---

## Identity Collapse Prohibited

Canonical identities must not replace source identities.

---

## Provenance Collapse Prohibited

Surface exports must preserve lineage references.

---

## Uncertainty Collapse Prohibited

Null-state distinctions must remain visible.

---

## Reasoning Collapse Prohibited

The surface must not substitute VDB interpretation for RDGP reasoning.

---

# Success Criteria

The query succeeds when VDB can construct a surface that:

```text
supports RDGP reasoning

preserves provenance

preserves identity

preserves uncertainty

preserves overlay structure

preserves future reinterpretability
```

without performing biological reasoning.

---

# Summary

The RDGP surface query defines how VDB constructs a deterministic, provenance-complete evidence surface suitable for downstream RDGP consumption.

The query prepares evidence.

The query does not reason about evidence.

The guiding principle is:

```text
VDB prepares evidence.

RDGP reasons over evidence.
```

# sample_gene_evidence_query.md

## Purpose

This document defines the canonical sample-gene evidence retrieval surface within the Variant Database (VDB).

The purpose of this query is to expose all evidence known to VDB for a specific:

```text
(sample_id, gene_id)
```

while preserving identity, provenance, uncertainty, overlay context, and evidence-state lineage.

This query represents the primary evidence retrieval surface for downstream consumers.

Examples include:

```text
RDGP

future analytics systems

future review systems

future discovery systems

future clinical research systems
```

---

# Scope

This query governs retrieval of:

```text
sample-gene evidence states

variant-derived evidence

overlay-attached evidence

external contextual evidence

provenance summaries

uncertainty summaries

identity summaries
```

This query does not perform:

```text
gene prioritization

clinical interpretation

diagnosis

causal inference

biological reasoning
```

Those responsibilities belong to downstream consumers.

---

# Core Question

The canonical question answered by this query is:

```text
What evidence exists for
(sample_id, gene_id)?
```

More precisely:

```text
What evidence states,
overlays,
provenance,
uncertainty,
identity mappings,
and contextual evidence

exist for this sample-gene pair?
```

---

# Query Philosophy

This query retrieves evidence.

This query does not perform reasoning.

The purpose of this query is to organize evidence for consumption.

Evidence retrieval and evidence interpretation remain distinct concerns.

---

# Evidence-State Retrieval

This query returns evidence states rather than isolated database rows.

Returned structures should represent preserved evidence states.

Examples:

```text
sample-gene evidence state

variant evidence state

semantic overlay evidence state

external context evidence state

provenance evidence state
```

The query surface may physically return:

```text
JSON

TSV

tabular structures

materialized views
```

but those structures represent evidence states rather than storage rows.

---

# Input Identity

## Required Inputs

```text
sample_id

gene_id
    OR
gene_symbol
```

---

## Optional Inputs

```text
phenotype_context

query_surface_version

namespace_policy_version

overlay_policy_version
```

---

# Namespace Requirements

Namespace brokerage must be applied prior to query-surface construction.

The query result must expose:

```text
source_gene_identifiers

canonical_gene_identifier

namespace_resolution_status

namespace_resolution_history
```

Supported resolution states include:

```text
exact

alias_resolved

deprecated_resolved

ambiguous

unresolved

conflicted

not_evaluated
```

Identity uncertainty must remain visible.

---

# Evidence-State Output Model

The returned object represents a sample-gene evidence state.

Conceptually:

```text
sample_id
        +
gene_id
        ↓

sample-gene evidence state
```

The evidence state may contain multiple evidence channels.

Channels remain distinguishable.

Channels must not be collapsed into a single support score.

---

# Evidence Channels

The query should expose decomposed evidence channels.

## Variant Observation Channel

Examples:

```text
observed variants

variant identities

variant counts

variant provenance
```

---

## Variant Interpretation Channel

Examples:

```text
clinical annotations

consequence annotations

pathogenicity annotations

interpretation provenance
```

---

## Coding Interpretation Channel

Examples:

```text
missense variants

frameshift variants

splice variants

coding burden summaries
```

---

## Noncoding Interpretation Channel

Examples:

```text
intronic variants

intergenic variants

regulatory annotations

future regulatory evidence
```

---

## Prioritization Channel

Examples:

```text
priority tiers

review categories

consumer-facing summaries
```

This channel preserves evidence.

It does not perform prioritization.

---

## Validation Channel

Examples:

```text
validation status

quality summaries

validation artifacts
```

---

## Overlay Channel

Examples:

```text
GSC overlays

future RSP overlays

future ontology overlays

future pathway overlays
```

---

## External Context Channel

Examples:

```text
BioSample context

BioProject context

external metadata context
```

---

## Provenance Channel

Examples:

```text
source TEPs

source artifacts

source repositories

lineage summaries
```

---

## Uncertainty Channel

Examples:

```text
missingness

ambiguity

conflicting annotations

unresolved mappings
```

---

# Variant Burden Surface

The query should expose variant burden summaries.

Examples:

```text
variant_count

rare_variant_count

high_impact_variant_count

pathogenic_variant_count

likely_pathogenic_variant_count

vus_variant_count
```

Variant burden summaries must remain traceable to contributing variants.

---

# Contributing Variant Visibility

The query must preserve contributing variant visibility.

Examples:

```text
variant identifiers

variant provenance

variant consequence summaries

variant source artifacts
```

Consumers must be able to reconstruct burden composition.

---

# GSC Overlay Behavior

When phenotype-scoped GSC evidence is available, the query may expose overlay context.

Examples:

```text
gsc_consensus_score

gsc_support_tier

gsc_source_count

gsc_release_identity

gsc_overlay_status
```

---

## Important Rule

Overlay absence does not imply negative evidence.

Supported states include:

```text
attached

not_attached

not_evaluated

unavailable

conflicted
```

---

# External Context Behavior

The query may expose externally discovered context.

Examples:

```text
age context

sex context

biosample context

platform context

cohort context
```

Externally discovered evidence must expose:

```text
authority class

retrieval timestamp

discovery provenance

attachment status
```

---

# Noncoding And Future Discovery Hooks

The query should preserve future-facing noncoding evidence.

Examples:

```text
noncoding_variant_count

noncoding_variant_ids

regulatory_annotation_status

nearest_locus_summary

future_model_status
```

---

## Important Rule

Lack of current annotations does not imply lack of future value.

---

# Phenotype Context

Phenotype context remains optional.

However, phenotype context becomes important when semantic overlays are attached.

The query should preserve:

```text
phenotype identity

phenotype authority

phenotype source

phenotype overlay scope
```

---

# Null Semantics

The query must preserve null-state distinctions.

Examples:

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

# Provenance Requirements

The query must expose sufficient provenance for reconstruction.

Examples:

```text
source repositories

source TEPs

source artifacts

namespace lineage

overlay lineage

discovery lineage

persistence lineage
```

The query must not become a provenance dead end.

---

# Output Forms

## Authoritative Output

The authoritative output form is a structured evidence object.

Examples:

```text
nested JSON

structured evidence bundle
```

---

## Convenience Output

Convenience representations may include:

```text
TSV

tabular views

materialized surfaces
```

Convenience outputs remain derived representations.

---

# Relationship To Overlay Attachment Query

Overlay attachment behavior is governed by:

```text
overlay_attachment_query.md
```

This query consumes overlay attachments.

It does not define overlay attachment rules.

---

# Relationship To RDGP Surface Query

This query represents a single sample-gene evidence retrieval operation.

The RDGP surface query operates across many sample-gene evidence states.

Conceptually:

```text
sample_gene_evidence_query
        ↓
individual evidence state

rdgp_surface_query
        ↓
reasoning-ready evidence collection
```

---

# Relationship To Provenance Audit Query

This query exposes provenance references.

Provenance audit queries reconstruct complete evidence lineage.

---

# Required Invariants

## Invariant 1

Sample identity remains visible.

---

## Invariant 2

Gene identity remains visible.

---

## Invariant 3

Namespace resolution status remains visible.

---

## Invariant 4

Evidence channels remain distinguishable.

---

## Invariant 5

Overlays remain distinguishable from primary evidence.

---

## Invariant 6

Provenance remains reconstructable.

---

## Invariant 7

Uncertainty remains visible.

---

## Invariant 8

Contributing variants remain traceable.

---

# Anti-Collapse Rules

## Evidence Channel Collapse Prohibited

Evidence channels must not be merged into a single support score.

---

## Overlay Collapse Prohibited

Overlay evidence must not overwrite primary evidence.

---

## Identity Collapse Prohibited

Canonical identities must not replace source identities.

---

## Provenance Collapse Prohibited

Query outputs must not sever lineage.

---

## Uncertainty Collapse Prohibited

Unknown, missing, unresolved, and conflicted states must remain distinguishable.

---

## Variant Collapse Prohibited

Variant burden summaries must remain reconstructable from contributing variants.

---

# Success Criteria

The query succeeds when VDB can answer:

```text
What evidence exists for this sample-gene pair?
```

while preserving:

```text
identity

provenance

authority

uncertainty

overlay context

future reinterpretability
```

without performing biological reasoning.

---

# Summary

The sample-gene evidence query is the canonical evidence retrieval surface within VDB.

It transforms preserved evidence into consumable evidence while preserving semantic richness, provenance, identity, uncertainty, overlay attachability, and future reinterpretability.

The query retrieves evidence.

The query does not decide what the evidence means.

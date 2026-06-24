# overlay_attachment_query.md

## Purpose

This document defines the canonical overlay attachment retrieval surface within the Variant Database (VDB).

The purpose of this query is to determine:

```text
What overlays are attached
to a given evidence object
or evidence state?
```

while preserving provenance, authority, identity, uncertainty, and attachment rationale.

---

# Scope

This query governs retrieval of:

```text
attached overlays

candidate overlays

overlay attachment rationale

attachment provenance

attachment uncertainty

attachment lineage
```

This query does not perform:

```text
evidence fusion

evidence replacement

biological reasoning

gene prioritization

clinical interpretation
```

---

# Core Question

The canonical question answered by this query is:

```text
What overlays are attached
to this evidence object
or evidence state?
```

More precisely:

```text
What additional evidence layers
have been attached,

why were they attached,

and how confident is VDB
in those attachments?
```

---

# Query Philosophy

Overlays are relationships.

Overlays are not replacements.

Overlays are not merges.

Overlays are not evidence fusion.

The purpose of overlay attachment is to create meaningful relationships between preserved evidence states.

---

# Core Principle

```text
Overlay attachment relates evidence.

Overlay attachment does not collapse evidence.
```

Examples:

```text
VAP evidence
        +
GSC overlay
```

does not become:

```text
single support score
```

Instead:

```text
VAP evidence state

with

attached GSC evidence state
```

Both evidence states remain independently recoverable.

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

## Optional Inputs

Examples:

```text
sample_id

gene_id

phenotype_context

overlay_type

authority_class

attachment_status
```

---

# Attachment Retrieval Model

Overlay attachment retrieval evaluates relationships between evidence states.

Conceptually:

```text
primary evidence state
        ↓
attachment evaluation
        ↓
overlay relationship
        ↓
attached overlay set
```

The primary evidence state remains authoritative for itself.

Attached overlays remain authoritative for themselves.

---

# Overlay Types

The query should support retrieval of multiple overlay classes.

---

## Gene Overlay

Examples:

```text
gene-level annotations

gene-level evidence

gene-level summaries
```

---

## Phenotype-Gene Overlay

Examples:

```text
GSC semantic priors

phenotype-scoped consensus evidence
```

---

## Sample Context Overlay

Examples:

```text
BioSample metadata

cohort metadata

demographic metadata
```

---

## Transcriptomic Overlay

Examples:

```text
future RSP evidence

expression evidence

differential expression evidence
```

---

## Pathway Overlay

Examples:

```text
pathway evidence

network evidence

functional context evidence
```

---

## Locus Proximity Overlay

Examples:

```text
regulatory proximity

noncoding burden context

future locus-based evidence
```

---

## Reasoning Overlay

Examples:

```text
future RDGP evidence

reasoning outputs

prioritization outputs
```

---

## External Metadata Overlay

Examples:

```text
BioProject metadata

registry metadata

external annotations
```

---

# Attachment Status

Attachment status must remain visible.

Supported states include:

```text
attached

candidate

not_attached

not_evaluated

ambiguous

conflicted

superseded
```

---

## Important Rule

The following must remain distinct:

```text
not_attached

not_evaluated

unknown

conflicted
```

Attachment absence does not imply negative evidence.

---

# Attachment Basis

Every attachment must expose why it exists.

Examples:

```text
canonical_gene_match

source_gene_match

alias_resolved_match

phenotype_match

phenotype_context_match

sample_accession_match

locus_overlap

locus_proximity

transcript_match

manual_attachment

policy_derived_attachment
```

---

## Required Principle

Attachments must be explainable.

Opaque attachment is prohibited.

---

# Attachment Provenance

Every attachment must expose provenance.

Examples:

```text
attachment_event_id

attachment_policy_version

attachment_timestamp

attachment_source

attachment_authority

attachment_method
```

---

## Success Criteria

Future systems must be able to reconstruct:

```text
why attachment occurred

when attachment occurred

how attachment occurred
```

---

# Namespace Requirements

Namespace brokerage may participate in attachment.

Examples:

```text
canonical gene resolution

alias resolution

ontology mapping

cross-domain identity resolution
```

The query should expose:

```text
namespace_resolution_status

identity_bridge_used

resolution_authority

resolution_version
```

---

# Phenotype Context Requirements

Phenotype-scoped overlays must preserve phenotype context.

Examples:

```text
phenotype identifier

phenotype source

phenotype authority

phenotype match status
```

---

## Important Rule

Phenotype mismatch should remain visible.

Phenotype mismatch must not be hidden.

---

# Authority Requirements

Attached overlays must expose authority.

Examples:

```text
producer_authoritative

external_authority

vdb_discovered_external

vdb_inferred

user_supplied
```

Authority must remain attached to overlays.

Authority must not be inherited implicitly.

---

# Uncertainty Requirements

Attachment uncertainty must remain visible.

Examples:

```text
ambiguous attachment

partial match

conflicting attachment

low-confidence attachment

deferred attachment
```

The query should expose:

```text
attachment_confidence

uncertainty_summary

conflict_summary
```

---

# External Context Attachments

Externally discovered evidence may be attached as overlays.

Examples:

```text
BioSample metadata

BioProject metadata

registry metadata

ontology metadata
```

External attachments must expose:

```text
retrieval timestamp

authority source

snapshot identity

discovery provenance
```

---

# Future Discovery Support

The overlay system should support future evidence domains.

Examples:

```text
future transcriptomic overlays

future pathway overlays

future network overlays

future noncoding evidence overlays

future reasoning overlays
```

Unknown overlay domains should remain attachable if preservation remains safe.

---

# Output Model

The query should return:

```text
primary evidence identity

overlay identities

attachment status

attachment basis

attachment provenance

attachment authority

attachment uncertainty
```

The query should not return a collapsed support score.

---

# Relationship To Sample-Gene Evidence Query

This query governs attachment relationships.

The sample-gene evidence query consumes attachment results.

Conceptually:

```text
overlay_attachment_query
        ↓
attachment relationships

sample_gene_evidence_query
        ↓
evidence state retrieval
```

---

# Relationship To RDGP Surface Query

RDGP surfaces depend heavily on overlay attachment.

Examples:

```text
GSC overlays

future RSP overlays

future contextual overlays
```

The RDGP surface should expose attachment results.

The RDGP surface should not redefine attachment logic.

---

# Relationship To Provenance Audit Query

Every attachment must remain auditable.

The provenance audit query should be able to reconstruct:

```text
attachment event

attachment rationale

attachment authority

attachment lineage
```

---

# Required Invariants

## Invariant 1

Primary evidence remains recoverable.

---

## Invariant 2

Overlay evidence remains recoverable.

---

## Invariant 3

Attachment rationale remains visible.

---

## Invariant 4

Attachment provenance remains visible.

---

## Invariant 5

Attachment authority remains visible.

---

## Invariant 6

Attachment uncertainty remains visible.

---

## Invariant 7

Phenotype context remains visible.

---

## Invariant 8

Namespace brokerage remains traceable.

---

# Anti-Collapse Rules

## Overlay Fusion Prohibited

Overlays must not replace primary evidence.

---

## Overlay Replacement Prohibited

Attached evidence must not overwrite source evidence.

---

## Identity Collapse Prohibited

Overlay identity must remain distinct from primary identity.

---

## Provenance Collapse Prohibited

Overlay lineage must remain reconstructable.

---

## Authority Collapse Prohibited

Overlay authority must remain visible.

---

## Attachment Ambiguity Collapse Prohibited

Attachment uncertainty must remain visible.

---

## Phenotype Collapse Prohibited

Phenotype-scoped overlays must preserve phenotype scope.

---

# Success Criteria

The query succeeds when VDB can answer:

```text
What overlays are attached
to this evidence state?
```

while preserving:

```text
identity

authority

provenance

uncertainty

attachment rationale

overlay independence
```

without performing evidence fusion.

---

# Summary

The overlay attachment query defines how VDB relates evidence across repositories, domains, and future evidence systems.

The purpose of overlay attachment is not to merge evidence.

The purpose of overlay attachment is to create traceable, explainable, provenance-aware relationships between independently preserved evidence states.

The guiding rule is:

```text
Overlay attachment relates evidence.

Overlay attachment does not collapse evidence.
```

# namespace_resolution_validation.md

## Purpose

This document defines how namespace resolution and identity brokerage are validated within the Variant Database (VDB).

Namespace validation evaluates whether identities remain preserved, traceable, authority-aware, and reconstructable throughout namespace resolution activities.

Namespace validation protects identity.

Namespace validation does not require all identities to resolve.

---

# Scope

This document governs validation of:

```text
identifier preservation

namespace preservation

identity brokerage

canonical identity attachment

identity mappings

identity lineage

resolution provenance

resolution ambiguity
```

This document defines:

```text
namespace validation objectives

identity-preservation requirements

resolution validation requirements

ambiguity handling

authority requirements

namespace validation severity
```

This document does not define:

```text
resolution algorithms

identity authority policies

database implementations

namespace brokerage code

mapping services
```

Those concerns belong to implementation or specification documents.

---

# Core Principle

```text
Resolution is optional.

Preservation is mandatory.
```

The purpose of namespace validation is not to determine whether every identity resolves.

The purpose of namespace validation is to determine whether identities survive brokerage safely.

The central question is:

```text
Can VDB relate identities
without destroying source identity?
```

---

# Relationship To Validation Strategy

The validation strategy defines validation philosophy.

This document applies that philosophy to identity spaces.

Conceptually:

```text
validation_strategy.md
        ↓

schema_validation.md
        ↓

namespace_resolution_validation.md
```

---

# Relationship To Ingestion Validation

Ingestion validation asks:

```text
Can identity enter VDB safely?
```

Namespace validation asks:

```text
Can identity brokerage occur safely?
```

Conceptually:

```text
identity preservation
        ↓
ingestion

identity brokerage
        ↓
namespace validation
```

---

# Namespace Validation Model

Namespace validation evaluates identity through multiple layers.

```text
Source Identity Preservation
        ↓

Canonical Identity Attachment
        ↓

Resolution Status Validation
        ↓

Resolution Provenance Validation
        ↓

Ambiguity Preservation
        ↓

Cross-Domain Consistency
        ↓

Query-Surface Safety
```

Each layer protects a different aspect of identity integrity.

---

# Layer 1 — Source Identity Preservation

## Purpose

Validate that source identities remain available after brokerage.

---

## Validation Targets

Examples:

```text
source_gene_id

source_gene_symbol

source_gene_namespace

source_variant_id

source_variant_namespace

source_phenotype_id

source_transcript_id

source_locus_id
```

---

## Required Checks

```text
source identifiers retained

source namespaces retained

source authority retained

source identity accessible
```

---

## Failure Condition

The following pattern is prohibited:

```text
source identity
        ↓
canonical identity only
```

without preserving source identity.

---

## Success Criteria

Source identities remain reconstructable.

---

# Layer 2 — Canonical Identity Attachment

## Purpose

Validate canonical identity integration.

---

## Examples

Canonical identifiers may include:

```text
HGNC

Ensembl

ClinVar

dbSNP

RefSeq

MANE

HPO

MONDO
```

---

## Required Checks

```text
canonical identity attached

canonical authority visible

source identity preserved

canonical identity traceable
```

---

## Important Rule

Canonical identities supplement source identities.

Canonical identities do not replace source identities.

---

## Success Criteria

Canonical identifiers enrich identity without destroying identity provenance.

---

# Layer 3 — Resolution Status Validation

## Purpose

Validate resolution state visibility.

---

## Supported Resolution States

Examples:

```text
exact

alias_resolved

deprecated_resolved

ambiguous

unresolved

conflicted

not_evaluated
```

---

## Required Checks

```text
resolution status present

resolution status reproducible

resolution state accessible
```

---

## Success Criteria

Resolution outcomes remain visible.

---

# Layer 4 — Resolution Provenance Validation

## Purpose

Validate traceability of resolution decisions.

---

## Required Resolution Provenance

Examples:

```text
resolution_event_id

authority_source

authority_version

mapping_method

resolved_at

resolution_status
```

---

## Required Checks

```text
mapping origin visible

authority visible

resolution history reconstructable
```

---

## Success Criteria

Future systems can explain why a mapping occurred.

---

# Layer 5 — Ambiguity Preservation

## Purpose

Protect unresolved and ambiguous identity states.

---

## Examples

Examples include:

```text
multiple candidate genes

multiple candidate transcripts

multiple candidate ontology mappings

historical aliases

conflicting authorities
```

---

## Required Checks

```text
ambiguity preserved

candidate mappings preserved

conflicts preserved

uncertainty visible
```

---

## Important Rule

Ambiguity is not identity failure.

Ambiguity becomes a validation concern only when ambiguity is hidden.

---

## Success Criteria

Ambiguous identities remain explicitly ambiguous.

---

# Layer 6 — Cross-Domain Consistency

## Purpose

Validate identity brokerage across evidence domains.

---

## Examples

Examples include:

```text
VAP variant evidence

GSC semantic priors

future RSP expression evidence

future RDGP reasoning evidence
```

---

## Required Checks

```text
cross-domain mappings traceable

source identities preserved

canonical identities stable

brokerage events visible
```

---

## Success Criteria

Evidence domains remain interoperable without identity collapse.

---

# Layer 7 — Query-Surface Safety

## Purpose

Validate safe exposure of identity through query surfaces.

---

## Examples

Examples include:

```text
sample × gene query surfaces

variant × gene query surfaces

phenotype × gene query surfaces

future cohort query surfaces
```

---

## Required Checks

```text
identity uncertainty visible

resolution status exposed

mapping provenance accessible

ambiguity preserved
```

---

## Important Rule

Query surfaces must not hide mapping uncertainty.

---

## Success Criteria

Consumers can evaluate identity confidence independently.

---

# Authority Validation

Namespace validation must preserve authority.

Examples:

```text
HGNC authority

Ensembl authority

ClinVar authority

HPO authority

MONDO authority

producer authority
```

---

## Required Checks

```text
authority source visible

authority version visible

authority lineage traceable
```

---

## Success Criteria

Identity authority remains reconstructable.

---

# Identity Lineage Validation

Namespace validation must preserve identity evolution.

Examples:

```text
deprecated symbols

historical aliases

merged identifiers

superseded identifiers
```

---

## Required Checks

```text
identity history available

identifier evolution traceable

supersession visible
```

---

## Success Criteria

Identity lineage remains reconstructable.

---

# Resolution Conflict Validation

Namespace validation must preserve conflicting identity claims.

Examples:

```text
multiple authorities disagree

multiple mappings exist

ontology disagreement

cross-reference disagreement
```

---

## Required Checks

```text
conflict visible

conflict source visible

conflict authority visible
```

---

## Important Rule

Conflicts must not be silently resolved.

---

## Success Criteria

Conflicting identity assertions remain reviewable.

---

# Namespace Validation Severity

Namespace validation uses the standard validation severity model.

---

## Informational

Examples:

```text
canonical identity unavailable

additional authority available
```

---

## Warning

Examples:

```text
unresolved identity

ambiguous identity

deprecated identifier
```

provided preservation remains intact.

---

## Error

Examples:

```text
missing resolution provenance

authority version unavailable

mapping history unavailable

identity conflict untracked
```

---

## Critical

Examples:

```text
source identity loss

namespace authority loss

canonical identity overwrites source identity

ambiguous mapping silently treated as exact

identity lineage destruction
```

Critical findings invalidate safe namespace brokerage.

---

# Anti-Collapse Validation

Namespace validation must detect identity collapse.

Validation should detect:

```text
source identity collapse

namespace collapse

authority collapse

lineage collapse

ambiguity collapse

query-surface identity collapse
```

---

# Required Invariants

## Invariant 1

Source identities remain preservable.

---

## Invariant 2

Source namespaces remain visible.

---

## Invariant 3

Canonical identities supplement source identities.

---

## Invariant 4

Resolution provenance remains available.

---

## Invariant 5

Ambiguity remains visible.

---

## Invariant 6

Authority remains visible.

---

## Invariant 7

Identity lineage remains reconstructable.

---

## Invariant 8

Query surfaces remain identity-aware.

---

# Relationship To Discovery

Discovery may identify new identities and relationships.

Namespace validation evaluates whether those relationships were attached safely.

Examples:

```text
external ontology attachment

external registry attachment

cross-domain identity bridge

discovered alias mapping
```

Namespace validation does not perform discovery.

Namespace validation evaluates discovery outcomes.

---

# Relationship To RDGP

RDGP consumes identity-brokered evidence surfaces.

Namespace validation must ensure that RDGP-facing surfaces preserve:

```text
resolution status

authority visibility

identity ambiguity

mapping provenance
```

This prevents reasoning over hidden identity assumptions.

---

# Success Criteria

Namespace validation succeeds when VDB can demonstrate that:

```text
identities survive brokerage

authorities remain visible

resolution history remains available

ambiguity remains visible

cross-domain interoperability remains possible

query surfaces remain identity-aware
```

without requiring destructive resolution.

---

# Conclusion

Namespace validation exists to protect identity throughout the VDB lifecycle.

The purpose of namespace brokerage is not to erase identity differences.

The purpose of namespace brokerage is to create relationships between identities while preserving their origins.

The central question of namespace validation is:

```text
Can VDB relate identities
without losing identity?
```

If the answer is yes, namespace validation has succeeded.

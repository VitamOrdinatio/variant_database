# namespace_resolution_contract.md

## Purpose

This contract defines the obligations, constraints, and expected behaviors of the VDB namespace resolution subsystem.

The namespace resolution subsystem is responsible for relating identities across producers, authorities, and evidence domains while preserving source identity and reconstruction capability.

The purpose of namespace resolution is to enable safe evidence interoperability without sacrificing identity provenance.

---

# Relationship To System Contract

This contract derives from:

```text
docs/contracts/system_contract.md
```

All namespace resolution behavior must remain compliant with the VDB System Contract.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Core Principle

```text
Namespace resolution attaches identity relationships.

Namespace resolution does not replace source identity.
```

The namespace resolution subsystem exists to create identity bridges.

It does not exist to erase, overwrite, or normalize away source identity.

---

# Scope

This contract governs:

```text
gene identity brokerage

transcript identity brokerage

variant identity brokerage

phenotype identity brokerage

sample and accession identity brokerage

external authority mappings

identity bridge creation

resolution event recording

resolution provenance preservation
```

This contract does not govern:

```text
evidence ingestion

evidence persistence

overlay attachment

query surface construction

RDGP reasoning
```

Those responsibilities belong to separate subsystems.

---

# Namespace Boundary

The namespace resolution subsystem operates at the boundary:

```text
Source Identity
        ↓
Namespace Resolution
        ↓
Identity Relationship
```

Namespace resolution relates identities.

It does not alter evidence.

---

# Allowed Responsibilities

The namespace resolution subsystem may:

```text
read source identifiers

classify namespace types

attach canonical identifiers

record alias relationships

record deprecated identifiers

create identity bridges

record resolution status

record resolution provenance

support cross-producer interoperability

support downstream query surfaces
```

These are compliant namespace resolution behaviors.

---

# Prohibited Responsibilities

The namespace resolution subsystem must not:

```text
overwrite source identifiers

erase source namespaces

replace source identity with canonical identity

silently resolve ambiguous mappings

silently resolve conflicting mappings

collapse independent producer identities

discard unresolved identities

perform biological interpretation
```

Identity preservation takes precedence over convenience.

---

# Supported Identity Spaces

The namespace resolution subsystem must support:

```text
genes

transcripts

variants

phenotypes

samples

runs

artifacts

TEP packages
```

Future identity spaces may be added without invalidating previously preserved evidence.

---

# Required Logical Outputs

Successful namespace resolution must produce:

```text
Namespace Event

Identity Assertion

Identity Bridge

Resolution Status

Resolution Provenance

Canonical Identity Attachment
```

These outputs form the minimum namespace preservation footprint.

---

# Source Identity Requirements

Source identity must remain visible after namespace resolution.

The following must remain reconstructable:

```text
source identifier

source namespace

source producer

source artifact

source evidence object
```

Source identity may never be replaced by canonical identity.

---

# Canonical Identity Attachment Requirements

Canonical identifiers may be attached when available.

Examples include:

```text
Ensembl Gene IDs

HGNC symbols

RefSeq identifiers

ontology identifiers

future authority identifiers
```

Canonical identities are additive.

Canonical identities are not replacements.

---

# Resolution Status Requirements

Namespace resolution must preserve resolution status.

Supported statuses include:

```text
exact

alias_resolved

deprecated_resolved

adapter_resolved

unresolved

ambiguous

conflicted

not_evaluated
```

Resolution status must remain visible to downstream consumers.

---

# Resolution Provenance Requirements

Every namespace resolution event must preserve:

```text
authority source

authority version

resolution policy version

mapping method

timestamp

resolution status
```

Namespace relationships without provenance are not compliant.

---

# Ambiguity Requirements

Ambiguous identities must remain visible.

Examples include:

```text
multiple possible mappings

insufficient mapping evidence

cross-authority disagreement
```

Ambiguous identities must not be silently converted into exact identities.

---

# Conflict Requirements

Conflicting identities must remain visible.

Examples include:

```text
authority disagreement

producer disagreement

namespace disagreement

historical identifier conflict
```

Conflicts must be preserved rather than hidden.

---

# Cross-Producer Identity Bridge Requirements

Namespace resolution must support cross-producer interoperability.

Example:

```text
VAP
    ↓
POLG

GSC
    ↓
POLG

Namespace Resolution
    ↓
ENSG00000140521
```

The resulting bridge enables interoperability.

The original producer identities remain preserved.

---

# Identity Bridge Requirements

Identity bridges must preserve:

```text
bridge identifier

source identity

destination identity

bridge authority

bridge rationale

bridge timestamp
```

Identity bridges must remain reconstructable.

---

# Query Surface Exposure Requirements

Namespace resolution information must be visible on query surfaces.

Examples include:

```text
source identifier

canonical identifier

resolution status

bridge identifier

mapping policy version
```

Consumers must be able to evaluate resolution quality.

---

# Evidence Reconstruction Requirements

Namespace history must remain reconstructable.

Given an evidence object, VDB must be able to reconstruct:

```text
source identity

source namespace

resolution events

identity bridges

authority sources

canonical attachments

resolution history
```

If namespace history cannot be reconstructed, namespace preservation has failed.

---

# Determinism Requirements

Given identical:

```text
source identifiers

authority datasets

resolution policies

schema versions
```

the namespace resolution subsystem must produce equivalent outputs.

Resolution behavior must be deterministic.

---

# Failure Classification

## Critical Failures

Critical failures violate identity preservation.

Examples:

```text
source identity overwritten

canonical identity replaces source identity

ambiguous mapping treated as exact

conflicting mapping hidden

resolution provenance lost
```

Critical failures block compliance.

---

## Errors

Errors prevent successful resolution.

Examples:

```text
invalid identifier structure

unsupported namespace format

authority mapping unavailable
```

Errors must remain visible.

---

## Warnings

Warnings preserve evidence while indicating uncertainty.

Examples:

```text
unresolved identity

ambiguous identity

adapter-derived mapping

partial authority coverage
```

Warnings must remain visible.

---

# POLG / POLG2 Identity Preservation Example

Namespace resolution must preserve identity specificity.

For example:

```text
POLG
```

and:

```text
POLG2
```

are distinct biological entities.

The presence of shared text fragments does not justify identity collapse.

The namespace resolution subsystem must require explicit evidence before creating identity bridges.

String similarity alone is insufficient.

---

# Anti-Collapse Rules

The namespace resolution subsystem must not:

```text
collapse source identity into canonical identity

collapse namespace history

collapse ambiguity into certainty

collapse conflicts into agreement

collapse producer-specific identities

discard unresolved identifiers

hide resolution uncertainty
```

Identity preservation takes precedence over normalization.

---

# Compliance Criteria

The namespace resolution subsystem is compliant only if:

```text
source identity remains visible

canonical identity remains additive

resolution provenance remains visible

identity bridges remain reconstructable

ambiguity remains visible

conflicts remain visible

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
```

and supports:

```text
query_surface_contract.md
```

Namespace governance serves as the interoperability layer of VDB.

---

# Summary

The namespace resolution subsystem exists to connect identities without destroying identities.

The subsystem must preserve source truth while enabling cross-producer discovery and interoperability.

The guiding principle is:

```text
Resolve carefully.

Preserve completely.

Never replace identity with convenience.
```

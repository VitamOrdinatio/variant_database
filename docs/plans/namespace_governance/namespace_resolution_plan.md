# namespace_resolution_plan.md

## Purpose

This document defines the implementation plan for the VDB namespace resolution subsystem.

The namespace resolution subsystem is responsible for creating identity relationships across evidence producers while preserving source identity, provenance, uncertainty, and reconstruction capability.

This plan translates:

```text
docs/contracts/namespace_governance/namespace_resolution_contract.md
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
docs/contracts/namespace_governance/namespace_resolution_contract.md
```

Namespace resolution is the interoperability layer of VDB.

It enables cross-producer evidence attachment without replacing producer identity.

---

# Implementation Goal

The goal of the namespace resolution subsystem is:

```text
Enable safe cross-producer identity bridges
while preserving source identity.
```

The purpose of namespace resolution is relationship creation.

The purpose of namespace resolution is not identity replacement.

---

# Initial Scope

Version 1 implementation focuses exclusively on:

```text
gene identity
```

The following identity domains are deferred:

```text
transcript identity

variant identity

phenotype identity

sample identity

accession identity

ontology identity
```

Future identity domains may be added without modifying prior namespace history.

---

# Initial Benchmark Scenario

The first namespace benchmark is:

```text
VAP
    POLG

GSC
    POLG

Canonical Identity
    ENSG00000140521
```

Successful namespace resolution must allow:

```text
HG002 POLG VAP evidence

+

Mitochondrial POLG GSC evidence
```

to participate in later overlay attachment.

---

# Identity Preservation Benchmark

The benchmark identity preservation case is:

```text
POLG
```

versus:

```text
POLG2
```

The namespace subsystem must preserve the distinction.

Shared text fragments do not justify identity bridges.

Substring matching is insufficient.

---

# Source Identifier Strategy

The namespace subsystem should prioritize identifiers already supplied by producers.

Examples include:

```text
gene_symbol

gene_id

mapping_status_summary

gene_mapping_status
```

Version 1 should rely primarily upon producer-emitted identity information.

Live external authority lookups are not required.

---

# Resolution Status Strategy

The namespace subsystem must preserve resolution status.

Initial implementation should support:

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

Only statuses exercised by benchmark data must be implemented immediately.

All statuses must remain representable.

---

# Namespace Event Strategy

Namespace resolution must produce:

```text
Namespace Event

Identity Assertion

Identity Bridge

Resolution Status

Resolution Provenance

Canonical Identity Attachment
```

These logical outputs become persistence records.

---

# Identity Bridge Strategy

Identity bridges must preserve:

```text
source identity

source namespace

canonical identity

bridge identifier

resolution authority

resolution status

policy version

timestamp
```

Identity bridges are additive.

Identity bridges are not replacements.

---

# Resolution Provenance Strategy

Every namespace event must preserve:

```text
authority source

authority version

resolution method

policy version

resolution status

timestamp
```

Namespace relationships without provenance are noncompliant.

---

# Proposed Module Structure

Initial implementation may utilize:

```text
src/variant_database/namespace_governance/

    identity_models.py

    namespace_classifier.py

    gene_resolver.py

    identity_bridge_builder.py

    namespace_event_writer.py

    namespace_validator.py
```

Module names may evolve.

Responsibilities must remain intact.

---

# Phase 1 — Identity Model Construction

## Purpose

Create the foundational identity structures used by namespace resolution.

## Expected Work

Implement:

```text
source identity models

canonical identity models

identity assertion models

resolution status models

bridge models
```

## Expected Outputs

```text
identity model definitions

identity validation tests
```

## Exit Criteria

```text
identity models exist

identity models support reconstruction

identity models support future identity domains
```

---

# Phase 2 — Namespace Classification

## Purpose

Classify source identities into recognized namespace categories.

## Expected Work

Implement:

```text
namespace detection

namespace labeling

namespace validation

source namespace preservation
```

Examples include:

```text
Ensembl

HGNC

producer-native identifiers

future namespaces
```

## Expected Outputs

```text
namespace classifications

classification validation tests
```

## Exit Criteria

```text
source namespace remains visible

namespace classification deterministic
```

---

# Phase 3 — Gene Resolution

## Purpose

Implement initial gene identity resolution.

## Expected Work

Implement:

```text
gene identity comparison

canonical identity attachment

resolution status assignment

resolution provenance assignment
```

## Initial Resolution Logic

Examples:

```text
identical stable gene identifiers
    → exact

known alias mapping
    → alias_resolved

known deprecated mapping
    → deprecated_resolved

multiple possible mappings
    → ambiguous

conflicting mappings
    → conflicted

no mapping
    → unresolved
```

## Expected Outputs

```text
resolved gene identities

resolution status records

resolution provenance records
```

## Exit Criteria

```text
POLG resolves correctly

POLG2 remains distinct

resolution status preserved
```

---

# Phase 4 — Identity Bridge Construction

## Purpose

Create cross-producer identity relationships.

## Expected Work

Implement:

```text
Identity Bridge creation

bridge persistence

bridge reconstruction support

bridge validation
```

## Expected Outputs

```text
Identity Bridge records

bridge retrieval APIs

bridge validation tests
```

## Exit Criteria

```text
cross-producer bridges exist

bridges remain reconstructable

source identities remain visible
```

---

# Phase 5 — Namespace Event Persistence

## Purpose

Persist namespace history.

## Expected Work

Implement:

```text
Namespace Event creation

Namespace Event persistence

event retrieval

event validation
```

## Expected Outputs

```text
Namespace Event records

event history APIs

event validation tests
```

## Exit Criteria

```text
namespace history reconstructable

resolution history reconstructable
```

---

# Phase 6 — Namespace Validation

## Purpose

Validate namespace preservation behavior.

## Expected Work

Execute:

```text
docs/validation/namespace_resolution_validation.md
```

against benchmark data.

## Validation Targets

```text
identity preservation

resolution provenance

bridge reconstruction

ambiguity handling

conflict handling

determinism
```

## Exit Criteria

```text
validation passes

anti-collapse checks pass
```

---

# Resolution Algorithm Rules

The following rules must be enforced.

---

## Exact Match Rule

If:

```text
stable identifiers match
```

then:

```text
exact bridge permitted
```

---

## Alias Rule

If:

```text
authority-supported alias exists
```

then:

```text
alias_resolved permitted
```

---

## Ambiguity Rule

If:

```text
multiple valid mappings exist
```

then:

```text
ambiguous
```

must be preserved.

---

## Conflict Rule

If:

```text
multiple incompatible mappings exist
```

then:

```text
conflicted
```

must be preserved.

---

## Substring Rule

The following is prohibited:

```text
substring-only identity resolution
```

Examples:

```text
POLG

POLG2
```

must remain distinct.

---

# Test Strategy

Namespace tests must verify:

```text
identity preservation

canonical identity attachment

resolution status preservation

bridge construction

bridge reconstruction

ambiguity preservation

conflict preservation

determinism
```

---

# Validation Gates

The namespace subsystem must satisfy:

```text
docs/validation/namespace_resolution_validation.md
```

Required gates include:

```text
source identity preservation

canonical identity visibility

bridge reconstruction

resolution provenance

ambiguity visibility

conflict visibility

determinism
```

---

# Anti-Collapse Checks

The namespace subsystem must verify that implementation does not:

```text
replace source identity

overwrite source identifiers

hide ambiguity

hide conflicts

discard unresolved identities

collapse namespace history

collapse producer-specific identities

collapse POLG into POLG2
```

These checks are mandatory.

---

# Future Benchmark Scenario

Namespace resolution must support eventual execution of:

```text
docs/examples/vdb_evidence_lifecycle_example.md
```

Specifically:

```text
HG002 POLG VAP evidence

↓

ENSG00000140521

↓

Mitochondrial POLG GSC evidence
```

must remain achievable.

No namespace behavior may prevent this benchmark lifecycle.

---

# Definition Of Done

The namespace subsystem is complete when:

```text
identity models exist

namespace classification exists

gene resolution exists

Identity Bridges exist

Namespace Events exist

resolution provenance exists

POLG benchmark succeeds

POLG2 benchmark succeeds

validation passes

anti-collapse checks pass
```

The namespace subsystem is not complete merely because identifiers can be matched.

---

# Summary

The namespace subsystem exists to create identity relationships without destroying identity history.

Its purpose is to enable interoperability while preserving source truth.

The guiding implementation rule is:

```text
Bridge identities.

Preserve origins.

Never replace identity with convenience.
```

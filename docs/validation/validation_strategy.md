# Validation Strategy

## Purpose

This document defines the validation philosophy and validation framework for the Variant Database (VDB).

The purpose of validation is to ensure that evidence entering, persisting within, and leaving VDB remains structurally sound, provenance-preserving, identity-preserving, and interoperable.

Validation exists to protect repository doctrine.

Validation does not exist to replace scientific interpretation.

---

# Scope

This document defines:

```text
validation objectives

validation layers

validation responsibilities

validation categories

validation philosophy
```

This document does not define:

```text
specific validation implementations

database constraints

test suites

validation code

validation schemas
```

Those concerns belong to implementation-level validation documentation.

---

# Core Principle

```text
Validation protects preservation.
```

VDB is fundamentally a preservation-oriented repository.

Therefore validation focuses on preserving:

```text
evidence

provenance

identity

topology

authority

interoperability
```

Validation should detect conditions that threaten those goals.

---

# Validation Philosophy

Validation is performed to answer a simple question:

```text
Can this evidence be trusted
to preserve its intended meaning?
```

Validation is not intended to determine whether biological conclusions are correct.

Biological interpretation remains the responsibility of evidence producers and downstream consumers.

VDB validates preservation readiness and interoperability readiness.

---

# Layered Validation Model

Validation within VDB occurs across multiple layers.

Conceptually:

```text
Producer Validation
        ↓
Transport Validation
        ↓
Ingestion Validation
        ↓
Namespace Validation
        ↓
Persistence Validation
        ↓
Discovery Validation
```

Each layer protects a different aspect of repository behavior.

---

# Producer Validation

Producer validation occurs before evidence reaches VDB.

Examples include:

```text
GSC-TEP validation

VAP-TEP validation

future RSP-TEP validation

future RDGP-TEP validation
```

Producer repositories remain responsible for validating:

```text
producer outputs

producer artifacts

producer evidence semantics
```

VDB should not duplicate producer validation unnecessarily.

---

# Transport Validation

Transport validation evaluates whether a TEP can be safely interpreted by VDB.

Examples include:

```text
required fields present

required artifacts declared

required provenance declared

artifact references valid

manifest integrity valid
```

Transport validation protects interoperability.

---

# Ingestion Validation

Ingestion validation evaluates whether a TEP satisfies VDB ingestion requirements.

Examples include:

```text
TEP compliance

artifact manifest compliance

provenance compliance

identity preservation requirements

authority declaration requirements
```

Ingestion validation determines whether evidence can enter VDB safely.

---

# Namespace Validation

Namespace validation evaluates identity integrity.

Examples include:

```text
identifier preservation

namespace authority preservation

resolution integrity

identity lineage preservation

mapping consistency
```

Namespace validation protects interoperability and future reinterpretation.

---

# Persistence Validation

Persistence validation evaluates whether evidence remains correctly represented after storage.

Examples include:

```text
artifact persistence

identity persistence

provenance persistence

topology persistence

relationship persistence
```

Persistence validation protects long-term evidence stewardship.

---

# Discovery Validation

Discovery validation evaluates whether persisted evidence remains discoverable.

Examples include:

```text
evidence retrieval

relationship traversal

cross-domain discovery

identity navigation

provenance accessibility
```

Discovery validation protects the repository's ability to generate future value from preserved evidence.

---

# Preservation-Critical Validation Targets

The following concepts are considered preservation-critical.

Validation should prioritize protecting:

```text
evidence payloads

artifact manifests

provenance

identity spaces

namespace authority

topology

lineage

validation records
```

Loss of any of these may compromise future reinterpretation.

---

# Authority Validation

VDB distinguishes authority preservation from evidence preservation.

Validation should verify:

```text
producer authority retained

source authority retained

namespace authority retained

validation authority retained
```

Authority loss is considered a validation concern.

---

# Provenance Validation

Validation should verify:

```text
producer provenance

run provenance

release provenance

package provenance

artifact provenance

lineage provenance
```

remain available after transport and ingestion.

Evidence without provenance should be considered incomplete.

---

# Identity Validation

Validation should verify:

```text
source identifiers preserved

canonical identifiers stable

identity mappings traceable

identity lineage preserved
```

Identity validation protects namespace brokerage.

---

# Topology Validation

Validation should verify that preservation-critical relationships remain intact.

Examples include:

```text
phenotype ↔ gene

gene ↔ variant

sample ↔ variant

observation ↔ interpretation

interpretation ↔ validation
```

Topology loss may reduce evidence interpretability.

---

# Unknowns And Nullability

Validation should preserve uncertainty.

The following states must remain distinguishable:

```text
unknown

missing

unresolved

ambiguous

deferred

not assessed
```

Validation must not silently convert these states into:

```text
negative

resolved

invalid
```

without supporting evidence.

---

# Validation Severity Levels

Validation outcomes may be categorized as:

## Informational

Conditions that do not threaten preservation.

Examples:

```text
optional metadata absent

non-critical summaries absent
```

---

## Warning

Conditions that may reduce utility but do not invalidate evidence.

Examples:

```text
partial namespace resolution

optional provenance unavailable
```

---

## Error

Conditions that threaten preservation or interoperability.

Examples:

```text
required provenance missing

required identities missing

artifact manifest corruption
```

---

## Critical

Conditions that invalidate safe ingestion or persistence.

Examples:

```text
authority loss

unrecoverable identity loss

artifact integrity failure

topology destruction
```

---

# Validation Responsibilities

Responsibility for validation is distributed.

Producer repositories validate:

```text
producer correctness

producer outputs

producer contracts
```

VDB validates:

```text
interoperability

preservation

identity

provenance

persistence readiness
```

This separation prevents duplication of responsibilities.

---

# Relationship To Specifications

Validation derives from repository specifications.

Examples include:

```text
tep_spec.md

artifact_manifest_spec.md

provenance_spec.md

ingestion_event_spec.md

namespace_resolution_spec.md
```

Validation exists to verify compliance with those specifications.

---

# Future Validation Documents

Implementation-level validation documentation should refine this strategy.

Examples include:

```text
schema_validation.md

ingestion_validation.md

namespace_resolution_validation.md
```

These documents define concrete validation procedures.

This document defines only the governing philosophy.

---

# Success Criteria

The validation strategy succeeds when VDB can confidently determine:

```text
evidence is preserved

identities are preserved

provenance is preserved

authority is preserved

topology is preserved

interoperability remains intact
```

without requiring repository-specific assumptions.

---

# Conclusion

Validation exists to protect the preservation mission of the Variant Database.

By validating evidence, provenance, identity, authority, topology, and interoperability across multiple layers, VDB ensures that transported evidence remains meaningful long after its original production.

Validation is therefore not merely a quality-control activity.

It is a preservation activity.

The central question of VDB validation is:

```text
Can future systems still understand,
trust,
and reuse this evidence?
```

If the answer is yes, validation has succeeded.

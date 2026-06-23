# Validation Strategy

## Purpose

This document defines the validation philosophy and validation framework for the Variant Database (VDB).

The purpose of validation is to ensure that evidence entering, persisting within, and leaving VDB remains structurally sound, provenance-preserving, identity-preserving, and interoperable.

Validation exists to protect repository doctrine.

Validation does not exist to replace scientific interpretation.

---

# Scope

This document defines:

```text id="vjlwm7"
validation objectives

validation layers

validation responsibilities

validation categories

validation philosophy
```

This document does not define:

```text id="m1q5kv"
specific validation implementations

database constraints

test suites

validation code

validation schemas
```

Those concerns belong to implementation-level validation documentation.

---

# Core Principle

```text id="zjlwm5"
Validation protects preservation.
```

VDB is fundamentally a preservation-oriented repository.

Therefore validation focuses on preserving:

```text id="y9cfmi"
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

```text id="1pq3w7"
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

```text id="4uz6lk"
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

```text id="rvpr6w"
GSC-TEP validation

VAP-TEP validation

future RSP-TEP validation

future RDGP-TEP validation
```

Producer repositories remain responsible for validating:

```text id="svzlsk"
producer outputs

producer artifacts

producer evidence semantics
```

VDB should not duplicate producer validation unnecessarily.

---

# Transport Validation

Transport validation evaluates whether a TEP can be safely interpreted by VDB.

Examples include:

```text id="2z3dbj"
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

```text id="wjmq8q"
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

```text id="9a3rdo"
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

```text id="ik7rwe"
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

```text id="x4kksy"
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

```text id="v7m5dq"
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

```text id="5b3f0u"
producer authority retained

source authority retained

namespace authority retained

validation authority retained
```

Authority loss is considered a validation concern.

---

# Provenance Validation

Validation should verify:

```text id="gyx27e"
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

```text id="ynv4np"
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

```text id="rv9lgj"
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

```text id="2z1eww"
unknown

missing

unresolved

ambiguous

deferred

not assessed
```

Validation must not silently convert these states into:

```text id="3v08cs"
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

```text id="6rt11w"
optional metadata absent

non-critical summaries absent
```

---

## Warning

Conditions that may reduce utility but do not invalidate evidence.

Examples:

```text id="njckb0"
partial namespace resolution

optional provenance unavailable
```

---

## Error

Conditions that threaten preservation or interoperability.

Examples:

```text id="9m6c0w"
required provenance missing

required identities missing

artifact manifest corruption
```

---

## Critical

Conditions that invalidate safe ingestion or persistence.

Examples:

```text id="yn0vjp"
authority loss

unrecoverable identity loss

artifact integrity failure

topology destruction
```

---

# Validation Responsibilities

Responsibility for validation is distributed.

Producer repositories validate:

```text id="8jylcu"
producer correctness

producer outputs

producer contracts
```

VDB validates:

```text id="fjn8kc"
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

```text id="0j50ae"
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

```text id="4e16sq"
schema_validation.md

ingestion_validation.md

namespace_resolution_validation.md
```

These documents define concrete validation procedures.

This document defines only the governing philosophy.

---

# Success Criteria

The validation strategy succeeds when VDB can confidently determine:

```text id="1l5cgc"
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

```text id="w0a0rh"
Can future systems still understand,
trust,
and reuse this evidence?
```

If the answer is yes, validation has succeeded.

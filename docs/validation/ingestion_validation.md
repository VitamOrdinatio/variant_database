# ingestion_validation.md

## Purpose

This document defines how evidence entering the Variant Database (VDB) is validated for safe preservation.

Ingestion validation determines whether evidence may enter VDB without introducing unrecoverable loss of identity, provenance, authority, topology, uncertainty, or evidence meaning.

Ingestion validation evaluates preservation readiness.

Ingestion validation does not evaluate biological correctness.

---

# Scope

This document governs validation of:

```text
TEP ingestion

producer evidence ingestion

external evidence capsule ingestion

artifact ingestion

entity ingestion

evidence object ingestion

evidence state ingestion
```

This document defines:

```text
ingestion validation gates

ingestion readiness requirements

severity classification

preservation protection requirements
```

This document does not define:

```text
ingestion implementation

database loaders

ETL logic

parser implementations

biological interpretation
```

---

# Core Principle

```text
Evidence must be preservable before it becomes ingestible.
```

The purpose of ingestion validation is to determine whether VDB can safely preserve incoming evidence.

The central question is:

```text
Can this evidence enter VDB
without threatening preservation?
```

---

# Relationship To Validation Strategy

The validation strategy defines repository-wide validation philosophy.

This document applies that philosophy to evidence entering VDB.

Conceptually:

```text
validation_strategy.md
        ↓

schema_validation.md
        ↓

ingestion_validation.md
```

---

# Relationship To Other Schemas

Ingestion validation exercises all constitutional schemas.

Examples:

```text
metadata_schema.md
        →
identity readiness

provenance_schema.md
        →
lineage readiness

data_schema.md
        →
evidence-domain readiness

relational_schema.md
        →
preservation readiness

discovery_schema.md
        →
external evidence readiness

rdgp_query_surface_schema.md
        →
future query readiness
```

---

# Validation Gate Model

Ingestion validation occurs through a series of validation gates.

An object must satisfy required gates before being considered ingestion-ready.

```text
Gate 1
    Intake Eligibility

Gate 2
    Package Integrity

Gate 3
    Metadata Completeness

Gate 4
    Provenance Completeness

Gate 5
    Evidence Domain Recognition

Gate 6
    Namespace Safety

Gate 7
    Null-State Safety

Gate 8
    Traceability

Gate 9
    Post-Ingestion Preservation

Gate 10
    Severity Assignment
```

---

# Gate 1 — Intake Eligibility

## Purpose

Determine whether VDB can recognize the incoming object.

---

## Validation Targets

Examples:

```text
TEP-VAP

TEP-GSC

future TEP-RSP

future TEP-RDGP

future TEP-VDB

External Evidence Capsule
```

---

## Required Checks

```text
object type identifiable

authority class declared

source origin identifiable

ingestion scope identifiable
```

---

## Success Criteria

The incoming object can be classified without ambiguity.

---

# Gate 2 — Package Integrity

## Purpose

Validate package-level structural integrity.

---

## TEP Validation Targets

Examples:

```text
TEP package

manifest

artifact inventory

entity inventory

validation reports
```

---

## Required Checks

```text
manifest present

required artifacts present

artifact inventory consistent

entity inventory consistent

declared package structure valid
```

---

## External Evidence Capsule Targets

Examples:

```text
BioSample capsule

BioProject capsule

external metadata capsule
```

---

## Required Checks

```text
authority declared

retrieval timestamp present

record snapshot available

source record identity available
```

---

## Success Criteria

Package structure is sufficiently complete for preservation.

---

# Gate 3 — Metadata Completeness

## Purpose

Validate metadata required for preservation.

---

## Required Metadata

Examples:

```text
producer identity

run identity

release identity

TEP identity

artifact identities

entity identities

schema version

authority class
```

---

## Success Criteria

Metadata supports future reconstruction.

---

# Gate 4 — Provenance Completeness

## Purpose

Validate reconstructability.

---

## Required Checks

Examples:

```text
source identifiable

lineage available

transformation context available

ingestion context available

authority source available
```

---

## External Evidence Requirements

Externally discovered evidence must expose:

```text
discovery event

retrieval source

retrieval timestamp

authority class
```

---

## Success Criteria

Evidence origins remain reconstructable.

---

# Gate 5 — Evidence Domain Recognition

## Purpose

Determine whether evidence can be classified safely.

---

## Known Evidence Domains

Examples:

```text
variant observation

variant interpretation

semantic prior

source contribution

uncertainty state

reasoning output
```

---

## Unknown Evidence Domains

Unknown evidence domains are not automatically invalid.

Unknown domains may be classified as:

```text
preservable

deferred

unsupported
```

depending on preservation risk.

---

## Success Criteria

Evidence domains can be preserved without forced semantic collapse.

---

# Gate 6 — Namespace Safety

## Purpose

Protect identity during ingestion.

---

## Required Checks

Examples:

```text
source identifiers preserved

source namespaces preserved

identity ambiguity detectable

identity conflicts preservable
```

---

## Important Rule

Namespace resolution is not required for ingestion.

Identity preservation is required for ingestion.

---

## Success Criteria

Identity can survive ingestion.

---

# Gate 7 — Null-State Safety

## Purpose

Protect uncertainty and missingness semantics.

---

## Required Checks

The following states must remain distinguishable:

```text
unknown

missing

not assessed

ambiguous

deferred

no match

measured zero
```

---

## Success Criteria

Null semantics remain reconstructable.

---

# Gate 8 — Traceability

## Purpose

Protect traceability back to source evidence.

---

## Artifact-Level Traceability

Examples:

```text
artifact identity

artifact role

artifact checksum

artifact source
```

---

## Row-Level Traceability

When parsed evidence is ingested:

```text
source artifact

source row number

source row hash

schema binding version
```

should remain available when practical.

---

## Success Criteria

Evidence remains traceable to source artifacts.

---

# Gate 9 — Post-Ingestion Preservation Validation

## Purpose

Verify that preservation objectives remain intact after ingestion.

---

## Validation Targets

Examples:

```text
TEP package discoverable

artifacts discoverable

entities discoverable

evidence objects discoverable

evidence states discoverable

lineage reconstructable

authority visible
```

---

## Success Criteria

The ingested object remains preservable within VDB.

---

# Gate 10 — Severity Assignment

## Purpose

Assign validation severity.

---

## Informational

Examples:

```text
optional metadata absent

future enhancement opportunity
```

---

## Warning

Examples:

```text
partial metadata completeness

unknown preservable domain

limited provenance detail
```

---

## Error

Examples:

```text
identity ambiguity

missing required metadata

missing required provenance

artifact inconsistency
```

---

## Critical

Examples:

```text
unrecoverable identity loss

unrecoverable provenance loss

authority ambiguity that cannot be preserved

topology destruction

artifact integrity failure
```

Critical findings block ingestion.

---

# Preservation Validation

Ingestion validation must evaluate preservation readiness.

The following must remain preservable:

```text
identity

provenance

authority

topology

uncertainty

evidence objects

evidence states

evidence transitions
```

---

# Authority Validation

Every ingestible object must expose authority.

Supported examples:

```text
producer_authoritative

external_authority

vdb_discovered_external

user_supplied

vdb_inferred
```

Authority classes must remain visible.

Authority classes must not be silently promoted.

---

# External Evidence Validation

External evidence must be evaluated separately from producer evidence.

Examples:

```text
BioSample metadata

BioProject metadata

external ontology records

registry metadata
```

External evidence must preserve:

```text
source authority

retrieval event

retrieval timestamp

snapshot identity

attachment status
```

---

# Anti-Collapse Validation

Ingestion validation must verify that ingestion does not force semantic collapse.

Validation should detect:

```text
identity collapse

provenance collapse

authority collapse

namespace collapse

topology collapse

evidence-state collapse

uncertainty collapse
```

---

# Required Invariants

## Invariant 1

Identity must remain preservable.

---

## Invariant 2

Provenance must remain reconstructable.

---

## Invariant 3

Authority must remain visible.

---

## Invariant 4

Evidence Objects must remain distinguishable.

---

## Invariant 5

Evidence States must remain distinguishable.

---

## Invariant 6

Null-state semantics must remain distinguishable.

---

## Invariant 7

Traceability must remain available.

---

## Invariant 8

Unknown evidence must not be discarded solely because it is unknown.

---

# Relationship To Lifecycle Validation

Ingestion validation evaluates whether evidence can enter VDB safely.

Lifecycle validation evaluates whether evidence survives the complete ecosystem lifecycle.

Conceptually:

```text
Can this evidence enter VDB safely?
        ↓
ingestion_validation.md

Can this evidence survive the ecosystem?
        ↓
vdb_end_to_end_lifecycle_walkthrough.md
```

---

# Success Criteria

Ingestion validation succeeds when VDB can demonstrate that:

```text
evidence is identifiable

evidence is traceable

evidence is preservable

evidence authority is visible

evidence uncertainty is preserved

evidence topology survives ingestion
```

without requiring biological interpretation.

---

# Conclusion

The purpose of ingestion validation is not to determine whether evidence is correct.

The purpose of ingestion validation is to determine whether evidence can be preserved safely.

The central question of ingestion validation is:

```text
If this evidence enters VDB today,

will future systems still be able to
identify,
trace,
reconstruct,
and reuse it?
```

If the answer is yes, ingestion validation has succeeded.

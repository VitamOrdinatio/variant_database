# schema_validation.md

## Purpose

This document defines how schema-level architecture within the Variant Database (VDB) is validated.

Schema validation evaluates whether VDB schemas remain internally coherent, mutually compatible, preservation-oriented, and capable of supporting the complete evidence lifecycle.

Schema validation exists to protect repository architecture.

Schema validation does not validate implementation correctness.

Schema validation does not validate biological conclusions.

---

# Scope

This document governs validation of:

```text
metadata_schema.md

provenance_schema.md

data_schema.md

relational_schema.md

discovery_schema.md

rdgp_query_surface_schema.md
```

This document defines:

```text
schema validation objectives

schema validation layers

cross-schema validation

preservation validation

lifecycle validation readiness

anti-collapse validation

future-discovery validation
```

This document does not define:

```text
database constraints

SQL implementations

test code

unit tests

integration tests

pipeline execution
```

Those concerns belong to implementation-level validation.

---

# Core Principle

```text
Schema validation protects architecture.
```

The purpose of schema validation is to determine whether repository doctrine remains coherent and enforceable.

Schema validation asks:

```text
Can the architecture preserve evidence meaning
across the complete repository lifecycle?
```

---

# Relationship To Validation Strategy

The validation strategy defines validation philosophy.

Schema validation operationalizes that philosophy for repository schemas.

Conceptually:

```text
validation_strategy.md
        ↓

schema_validation.md
        ↓

ingestion_validation.md

namespace_resolution_validation.md

future implementation validation
```

---

# Validation Philosophy

Schema validation evaluates architecture rather than implementation.

The central question is:

```text
If implementation were built exactly
according to these schemas,

would preservation goals succeed?
```

Schema validation should occur before implementation whenever possible.

---

# Validation Layers

Schema validation occurs across five layers.

```text
Intra-Schema Validation
        ↓

Cross-Schema Validation
        ↓

Lifecycle Validation
        ↓

Preservation Validation
        ↓

Future-Discovery Validation
```

Each layer protects a different architectural concern.

---

# Layer 1 — Intra-Schema Validation

## Purpose

Intra-schema validation evaluates whether an individual schema remains internally coherent.

Examples:

```text
metadata schema consistency

provenance schema consistency

data schema consistency
```

---

## Validation Targets

Validation should examine:

```text
purpose

scope

design principles

entities

domains

invariants

anti-collapse rules
```

---

## Success Criteria

A schema passes intra-schema validation when:

```text
no internal contradictions exist

all defined concepts remain reachable

invariants are enforceable

anti-collapse rules remain consistent
```

---

# Layer 2 — Cross-Schema Validation

## Purpose

Cross-schema validation evaluates whether schemas agree with one another.

---

## Validation Targets

Examples:

```text
metadata identities
        ↔
relational identities

provenance lineage
        ↔
evidence state transitions

authority classes
        ↔
discovery classifications

evidence domains
        ↔
query surfaces
```

---

## Success Criteria

A schema set passes cross-schema validation when:

```text
concepts are consistently defined

terminology is aligned

identities remain compatible

schema responsibilities remain distinct
```

---

# Layer 3 — Lifecycle Validation

## Purpose

Lifecycle validation evaluates whether evidence can survive the complete repository ecosystem.

---

## Validation Targets

Examples:

```text
Producer
    →
TEP

TEP
    →
VDB

VDB
    →
Discovery

Discovery
    →
Query Surface

Query Surface
    →
RDGP

RDGP
    →
RDGP-TEP

RDGP-TEP
    →
VDB
```

---

## Lifecycle Walkthrough Validation

Lifecycle validation may be executed using a representative evidence object.

Examples:

```text
HG002

ERR10619300

future certified specimens
```

Lifecycle validation should verify:

```text
identity preservation

provenance preservation

authority preservation

topology preservation

uncertainty preservation
```

through every stage.

---

## Success Criteria

Lifecycle validation succeeds when evidence remains reconstructable throughout the entire lifecycle.

---

# Layer 4 — Preservation Validation

## Purpose

Preservation validation evaluates whether schemas protect evidence meaning.

---

## Preservation-Critical Targets

Validation should verify preservation of:

```text
evidence objects

evidence states

evidence state transitions

provenance

identities

authority

topology

uncertainty

null-state semantics
```

---

## Reconstruction Requirement

Schema validation must verify that future systems can reconstruct:

```text
what evidence existed

where it originated

how it evolved

how it was interpreted

how it was transported
```

---

## Success Criteria

Preservation validation succeeds when semantic reconstruction remains possible.

---

# Layer 5 — Future-Discovery Validation

## Purpose

Future-discovery validation evaluates whether schemas remain useful beyond currently known analyses.

---

## Validation Targets

Examples include:

```text
future annotation systems

future regulatory models

future transcriptomic integration

future network analysis

future ontology systems

future reasoning systems
```

---

## Future Goalpost Evaluation

Schema validation should evaluate whether architecture remains compatible with future concepts such as:

```text
polygenic burden

poly-noncoding burden

network convergence

cross-modal convergence

similar-case discovery

hospital-scale evidence reuse

future AlphaGenome-style interpretation
```

Validation does not require implementation of these concepts.

Validation requires that architecture does not prevent them.

---

## Success Criteria

Future-discovery validation succeeds when future reinterpretation remains possible without architectural redesign.

---

# Preservation Invariant Validation

Schema validation should evaluate all preservation-critical invariants.

Examples:

```text
identity preservation

provenance preservation

authority preservation

topology preservation

uncertainty preservation
```

Any violation should be treated as a schema concern.

---

# Anti-Collapse Validation

A primary responsibility of schema validation is detection of semantic collapse.

Validation should verify that architecture prevents:

```text
evidence collapse

provenance collapse

authority collapse

identity collapse

topology collapse

query-surface collapse

namespace collapse
```

---

## Evidence Object Validation

Validation should verify:

```text
evidence objects remain distinguishable

evidence states remain distinguishable

evidence transitions remain distinguishable
```

---

## Query Surface Validation

Validation should verify that query surfaces remain derived structures.

Query surfaces must not become authoritative evidence stores.

---

# Authority Validation

Schema validation should verify that authority remains visible.

Examples:

```text
producer authority

external authority

VDB-discovered authority

user-supplied authority
```

Authority classes must remain distinguishable.

---

# Null-State Validation

Schema validation should verify that the following remain distinct:

```text
unknown

missing

unresolved

ambiguous

deferred

not assessed

no match

measured zero
```

Architectural collapse of null semantics is considered a validation concern.

---

# Validation Evidence

Schema validation should produce evidence supporting conclusions.

Examples:

```text
schema audits

cross-schema audits

lifecycle walkthroughs

consistency reviews

architectural trace analyses
```

Validation conclusions should be reproducible.

---

# Validation Outcomes

Schema validation outcomes may be classified using the validation strategy severity model.

Examples:

## Informational

```text
terminology refinement opportunity
```

---

## Warning

```text
cross-schema ambiguity

future-discovery concern
```

---

## Error

```text
schema contradiction

identity inconsistency

provenance inconsistency
```

---

## Critical

```text
architectural semantic collapse

preservation failure

unrecoverable lifecycle failure
```

---

# Relationship To Lifecycle Walkthroughs

Lifecycle walkthroughs are validation artifacts.

They execute the validation methodology defined here.

Examples:

```text
vdb_end_to_end_lifecycle_walkthrough.md
```

A lifecycle walkthrough does not define validation doctrine.

A lifecycle walkthrough applies validation doctrine.

---

# Relationship To Future Validation Documents

This document governs architectural validation.

Future validation documents may govern:

```text
ingestion validation

namespace validation

discovery validation

query-surface validation

implementation validation
```

Those documents should remain consistent with this schema validation framework.

---

# Success Criteria

Schema validation succeeds when VDB can demonstrate that:

```text
schema responsibilities are coherent

schemas agree with one another

evidence survives the lifecycle

preservation goals remain protected

future reinterpretation remains possible

semantic collapse is prevented
```

without requiring implementation-specific assumptions.

---

# Conclusion

Schema validation exists to determine whether VDB architecture remains capable of preserving evidence meaning across time.

The central question of schema validation is:

```text
If these schemas are implemented faithfully,

will future systems still be able to
understand,
reconstruct,
trust,
and reuse preserved evidence?
```

If the answer is yes, schema validation has succeeded.

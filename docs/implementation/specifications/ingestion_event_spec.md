# Ingestion Event Specification

## Purpose

This document defines the specification for ingestion events performed by the Variant Database (VDB).

An ingestion event occurs when VDB receives a Transitional Evidence Product (TEP) and evaluates that evidence for validation, namespace brokerage, persistence, discovery, and future reasoning.

The purpose of ingestion is to make evidence available to VDB.

The purpose of ingestion is not to alter producer truth.

---

# Scope

This specification applies to:

```text
GSC-TEP

VAP-TEP

future RSP-TEP

future RDGP-TEP

future VDB-TEP
```

This specification governs:

```text
TEP receipt

TEP validation

TEP acceptance

TEP rejection

TEP persistence

namespace preparation

discovery preparation

provenance preservation
```

This specification does not govern:

```text
database schemas

query implementation

namespace resolution algorithms

producer-side TEP construction

scientific scoring algorithms
```

---

# Core Principle

```text
Ingestion makes evidence available.

Ingestion does not redefine evidence.
```

Producer repositories remain authoritative for evidence they generate.

VDB becomes responsible for persistence, discovery, brokerage, and downstream interoperability.

Ingestion must preserve producer meaning.

---

# Ingestion Definition

An ingestion event is a bounded operation during which VDB receives a TEP and determines:

```text
what arrived

who produced it

whether it is valid

whether it can be persisted

which identities it contains

which provenance it preserves

which discovery surfaces it enables
```

An ingestion event may result in:

```text
acceptance

conditional acceptance

rejection

deferred processing
```

---

# Ingestion Lifecycle

Conceptually:

```text
Producer
    ↓
TEP Construction
    ↓
TEP Receipt
    ↓
Validation
    ↓
Acceptance Decision
    ↓
Persistence Preparation
    ↓
Namespace Preparation
    ↓
Discovery Preparation
```

Each stage should preserve producer authority and provenance.

---

# Ingestion Event Identity

Every ingestion event should possess an identity.

Examples:

```text
ingestion_event_id

ingestion_timestamp

ingestion_version

ingestion_status
```

Ingestion identity represents the consumer event.

It does not replace producer identity.

---

# Receipt Phase

The receipt phase establishes that a TEP has arrived.

Receipt should capture:

```text
TEP identity

producer identity

receipt timestamp

transport source

transport version
```

Receipt does not imply acceptance.

Receipt only confirms arrival.

---

# Validation Phase

Validation determines whether the received TEP satisfies consumer requirements.

Validation should evaluate:

```text
TEP structure

artifact manifest integrity

required provenance

required identities

required authority declarations

payload accessibility

lineage integrity, when applicable
```

Validation should not evaluate scientific correctness.

Scientific correctness remains the responsibility of the producer.

Validation evaluates transport readiness and structural compliance.

---

# Validation Outcomes

Validation outcomes may include:

```text
pass

fail

warning

deferred
```

Validation outcomes should be preserved as ingestion provenance.

Producer validation and consumer validation are distinct concepts.

---

# Acceptance Phase

Acceptance determines whether VDB will persist and broker the received evidence.

Acceptance decisions may include:

```text
accepted

conditionally_accepted

rejected

deferred
```

Acceptance should be based on:

```text
structural integrity

identity completeness

provenance completeness

artifact availability

authority declaration completeness
```

Acceptance must not depend upon biological interpretation.

---

# Rejection Phase

A rejected TEP should preserve rejection provenance.

Examples:

```text
rejection reason

rejection timestamp

validator identity

failed criteria
```

Rejection should remain traceable.

Rejected evidence should not silently disappear.

---

# Persistence Preparation

Accepted evidence enters persistence preparation.

Persistence preparation determines:

```text
what evidence will be persisted

what identities must be retained

what provenance must be retained

what topology must be retained
```

Persistence preparation must not alter producer evidence semantics.

---

# Namespace Preparation

Namespace preparation identifies candidate identity spaces.

Examples:

```text
gene identifiers

variant identifiers

sample identifiers

phenotype identifiers

package identifiers

run identifiers

artifact identifiers
```

Namespace preparation identifies identities.

Namespace resolution occurs later.

---

# Discovery Preparation

Discovery preparation identifies evidence surfaces that may be queried or explored.

Examples:

```text
semantic priors

variant observations

interpretation overlays

validation outputs

source attribution records
```

Discovery preparation should preserve producer-defined meaning.

Discovery preparation must not collapse evidence classes.

---

# Authority Preservation

Ingestion must preserve authority boundaries.

Examples:

```text
producer authority

run authority

artifact authority

validation authority
```

VDB may add authority records associated with ingestion.

VDB must not overwrite producer authority.

---

# Provenance Preservation

Ingestion must preserve all required provenance layers.

Examples:

```text
producer provenance

run provenance

release provenance

package provenance

artifact provenance

lineage provenance

transport provenance
```

Ingestion may add:

```text
ingestion provenance

namespace provenance

discovery provenance
```

Added provenance must be additive.

---

# Topology Preservation

Ingestion must preserve topology when topology contributes meaning.

Examples:

```text
phenotype-gene relationships

source attribution relationships

observation lineage

interpretation lineage

validation lineage
```

Topology preservation is required for future reinterpretation.

---

# Identity Preservation

Ingestion must preserve producer-declared identifiers.

Examples:

```text
gene identifiers

sample identifiers

variant identifiers

run identifiers

release identifiers

package identifiers
```

Identity preservation occurs before namespace brokerage.

Producer identifiers must remain recoverable.

---

# Observation Preservation

For observation-oriented producers:

```text
VAP

future RSP
```

ingestion must preserve:

```text
observed substrate

annotation context

interpretation context

validation context

lineage context
```

Final candidates alone are insufficient when earlier evidence remains preservation-critical.

---

# Semantic Preservation

For semantic-prior producers:

```text
GSC
```

ingestion must preserve:

```text
semantic priors

semantic channels

source attribution

consensus context

phenotype context
```

Binary membership preservation alone is insufficient.

---

# Unknowns And Nullability

Ingestion must preserve uncertainty.

The following states should remain distinguishable:

```text
unknown

missing

unresolved

not assessed

not applicable

negative
```

Consumer systems must not silently reinterpret unknown values.

---

# Reference-Based TEP Ingestion

Reference-based TEPs remain valid ingestion targets.

Reference-based ingestion should preserve:

```text
authoritative source location

artifact ownership

artifact provenance

artifact integrity metadata
```

VDB need not immediately copy producer artifacts to perform ingestion.

---

# Portable TEP Ingestion

Portable TEPs may be ingested through equivalent workflows.

Portable ingestion should additionally validate:

```text
bundle integrity

bundle completeness

artifact checksums

bundle manifest integrity
```

Portable and reference-based TEPs should converge to equivalent evidence states after successful ingestion.

---

# Ingestion Outputs

A successful ingestion event should produce:

```text
ingestion record

validation record

authority record

provenance record

namespace preparation record

discovery preparation record
```

These records become part of VDB provenance.

---

# Anti-Patterns

The following violate this specification:

```text
rewriting producer identifiers during ingestion

overwriting producer provenance

discarding lineage information

discarding topology information

candidate-only preservation for staged evidence producers

collapsing semantic priors into binary memberships

treating ingestion as ownership transfer

silently correcting producer evidence

converting unknown values into inferred values
```

---

# Compliance Expectations

A compliant ingestion implementation should allow consumers to answer:

```text
What arrived?

Who produced it?

Was it validated?

Was it accepted?

What evidence does it contain?

What provenance accompanies it?

What identities must be preserved?

What topology must be preserved?

What discovery surfaces become available?
```

without requiring direct inspection of the producer repository.

---

# Relationship To Other Specifications

This specification builds upon:

```text
tep_spec.md

artifact_manifest_spec.md

provenance_spec.md
```

Related specifications:

```text
namespace_resolution_spec.md
    identity brokerage behavior
```

Schema documents remain downstream of this specification.

---

# Summary

An ingestion event is the controlled process through which VDB receives and evaluates a TEP.

Ingestion preserves producer evidence, provenance, identity, topology, and authority while preparing evidence for persistence, namespace brokerage, discovery, and future reasoning.

Ingestion therefore functions as a stewardship process rather than a transformation process.

VDB receives evidence.

VDB does not redefine evidence.

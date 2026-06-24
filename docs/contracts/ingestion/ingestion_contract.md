# ingestion_contract.md

## Purpose

This contract defines the obligations, constraints, and expected behaviors of the VDB ingestion subsystem.

The ingestion subsystem serves as the custody-transfer boundary between producer evidence and VDB persistence.

The purpose of ingestion is to transfer evidence into VDB while preserving identity, provenance, authority, uncertainty, and reconstructability.

---

# Relationship To System Contract

This contract derives from:

```text
docs/contracts/system_contract.md
```

All ingestion behavior must remain compliant with the VDB System Contract.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Core Principle

```text
Ingestion transfers custody.

Ingestion does not transform meaning.
```

The ingestion subsystem may register, validate, and preserve evidence.

The ingestion subsystem must not reinterpret, collapse, overwrite, or replace evidence.

---

# Scope

This contract governs:

```text
producer TEP intake
artifact registration
entity registration
evidence-bearing entity registration
metadata registration
provenance registration
ingestion validation
ingestion reporting
ingestion event recording
downstream evidence-construction readiness
```

This contract does not govern:

```text
Evidence Object construction
Initial Evidence State construction
namespace resolution
discovery
overlay attachment
query surface construction
RDGP reasoning
consumer-specific projections
```

Evidence Object construction and Initial Evidence State construction occur after ingestion, during downstream persistence and evidence-construction phases.

Those responsibilities belong to downstream subsystems.

---

# Ingestion Boundary

The ingestion subsystem operates at the boundary:

```text
Producer Evidence
        ↓
Ingestion
        ↓
Persistent Evidence
```

The ingestion subsystem is responsible for ensuring that evidence crosses this boundary safely and reproducibly.

---

# Allowed Responsibilities

The ingestion subsystem may:

```text
read producer artifacts
validate producer artifacts
register TEP packages
register artifacts
register entities
register evidence-bearing source references
register metadata
register provenance
create ingestion reports
record ingestion events
emit downstream evidence-construction handoff records
```

These activities are considered compliant ingestion behaviors.

---

# Prohibited Responsibilities

The ingestion subsystem must not:

```text
modify producer artifacts
rewrite producer metadata
replace source identities
discard evidence because it appears low-value
perform biological interpretation
construct downstream reasoning states
attach semantic overlays
perform RDGP reasoning
emit consumer-specific evidence projections
```

Ingestion is a preservation and custody-transfer activity.

It is not a reasoning activity.

---

# Supported Inputs

The ingestion subsystem must support:

```text
TEP-VAP
TEP-GSC
future TEP-RSP
future TEP-RDGP
External Evidence Capsules
future producer TEPs
```

Support for new producer types must not require modification of previously ingested evidence.

---

# Producer Artifact Immutability

Producer artifacts are immutable.

Ingestion may:

```text
read
hash
validate
index
reference
```

producer artifacts.

Ingestion must not:

```text
rewrite
rename
move
modify
repackage
```

producer artifacts.

This requirement applies especially to certified producer TEPs.

---

# Required Logical Outputs

Successful ingestion must produce:

```text
Ingestion Event

TEP Package Record

Artifact Records

Entity Records

Metadata Records

Provenance Records

Evidence-Bearing Source Reference Map

Ingestion Report
```

These outputs form the minimum ingestion preservation footprint.

Evidence Objects and Initial Evidence States are constructed downstream after ingestion outputs have been persisted and validated.

---

# Ingestion Event Requirements

Every ingestion operation must generate an Ingestion Event.

The event must preserve:

```text
ingestion identifier
timestamp
source producer
source TEP
schema version
validation status
operator context when applicable
```

Ingestion events must remain reconstructable.

---

# Metadata Requirements

Ingestion must preserve metadata sufficient to reconstruct:

```text
producer
repository
run
release
TEP package
artifact
entity
evidence object
```

Metadata registration must occur before evidence registration.

---

# Provenance Requirements

Ingestion must preserve provenance sufficient to determine:

```text
where evidence originated

which producer emitted it

which run generated it

which TEP transported it

which artifact contained it
```

Evidence lacking reconstructable provenance must not be silently accepted.

---

# Evidence Construction Handoff Requirements

Ingestion must preserve enough information for downstream construction of Evidence Objects.

The ingestion subsystem must preserve:

```text
source identity
producer identity
artifact references
entity references
source row or record references when available
evidence family hints when available
evidence domain hints when available
authority context when available
provenance references
payload references
```

The ingestion subsystem must not collapse evidence-bearing content before downstream Evidence Object construction.

---

# Initial Evidence State Deferral Requirements

Initial Evidence States are not created during ingestion.

Ingestion must preserve enough information for downstream creation of Initial Evidence States.

The ingestion subsystem must preserve:

```text
producer context
generation context
authority context
uncertainty context
source payload references
source artifact references
source provenance references
```

Subsequent enrichment must create additional Evidence States rather than modifying producer-emitted evidence.

---

# Artifact Preservation Requirements

Artifacts must remain individually visible.

Ingestion must preserve:

```text
artifact identity
artifact type
artifact lineage
artifact location
artifact checksums when available
```

Artifact boundaries must remain visible.

---

# Evidence Domain Recognition

Ingestion must classify evidence into recognized domains.

Examples include:

```text
metadata

provenance

variant evidence

semantic evidence

validation evidence

contextual evidence
```

Unknown domains may be preserved.

Unknown domains must not be discarded solely because they are unrecognized.

---

# Namespace Safety Requirements

Ingestion must preserve source identity.

Ingestion may record namespace-related metadata.

Ingestion must not:

```text
replace source identifiers
overwrite source namespaces
attach canonical identities destructively
```

Namespace resolution occurs after ingestion.

---

# Null Semantics Requirements

Missing information must remain distinguishable from absent information.

Ingestion must preserve:

```text
null
unknown
unresolved
not applicable
missing
```

as distinct semantic states whenever available.

Ingestion must not silently collapse null semantics.

---

# External Evidence Capsule Requirements

External Evidence Capsules may be ingested if they preserve:

```text
authority source
retrieval event
retrieval timestamp
snapshot identity
field-level provenance
attachment status
```

External evidence must remain distinguishable from producer evidence.

---

# Validation Requirements

All ingestion operations must satisfy:

```text
docs/validation/ingestion_validation.md
```

Validation must evaluate:

```text
integrity

traceability

metadata completeness

provenance completeness

schema compliance

preservation safety
```

Validation determines whether evidence is eligible for custody transfer.

---

# Determinism Requirements

Given identical:

```text
producer artifacts

schema versions

ingestion policies

validation policies
```

the ingestion subsystem must produce equivalent outputs.

Deterministic behavior is required.

---

# Failure Classification

## Critical Failures

Critical failures block ingestion.

Examples:

```text
unreadable TEP

corrupted package

missing required provenance

unrecoverable identity loss

integrity failure
```

---

## Errors

Errors prevent successful registration but may permit diagnostic reporting.

Examples:

```text
malformed required metadata

invalid entity structure

required artifact missing
```

---

## Warnings

Warnings permit preservation.

Examples:

```text
unknown evidence domain

optional metadata missing

unresolved identity

future schema extension
```

Warnings must remain visible.

---

# Anti-Collapse Rules

The ingestion subsystem must not:

```text
reduce TEPs to convenience tables

discard low-priority evidence

collapse variants into gene summaries

collapse semantic evidence into scores

collapse source identity into canonical identity

collapse artifacts into flattened records
```

Preservation takes precedence over convenience.

---

# Compliance Criteria

The ingestion subsystem is compliant only if:

```text
producer artifacts remain immutable

metadata remains reconstructable

provenance remains reconstructable

evidence-bearing source references remain reconstructable

downstream Evidence Object construction remains possible

downstream Initial Evidence State construction remains possible

validation succeeds

anti-collapse rules are satisfied
```

Failure of any requirement constitutes contract noncompliance.

---

# Summary

The ingestion subsystem is responsible for transferring evidence into VDB custody without altering its meaning.

Ingestion must preserve evidence such that downstream systems can later discover, relate, query, reinterpret, and reconstruct it.

The guiding principle is:

```text
Accept broadly.

Preserve faithfully.

Never collapse the evidence.
```

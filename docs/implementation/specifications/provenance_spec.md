# Provenance Specification

## Purpose

This document defines provenance requirements for Transitional Evidence Products (TEPs) and for evidence persisted within the Variant Database (VDB).

The purpose of provenance is to preserve evidence origin, authority, lineage, reproducibility, accountability, and future reinterpretability.

Provenance allows consumers to determine:

```text
Where did this evidence originate?

Who produced it?

When was it produced?

What process generated it?

What artifacts support it?

What identities does it depend upon?

What evidence transformations occurred?

Can the evidence be reconstructed?
```

Provenance exists to preserve evidence trustworthiness without requiring direct access to the original execution environment.

---

# Scope

This specification applies to:

```text
GSC-TEP

VAP-TEP

future RSP-TEP

future RDGP-TEP

future VDB-TEP

VDB-ingested evidence
```

This specification governs:

```text
source provenance

producer provenance

run provenance

release provenance

artifact provenance

entity provenance

lineage provenance

transport provenance
```

This specification does not govern:

```text
database schemas

query implementations

namespace resolution algorithms

scientific scoring systems

payload schemas
```

---

# Core Principle

```text
Evidence without provenance
is evidence without context.
```

and

```text
Preserved evidence
must preserve preserved provenance.
```

Provenance is therefore preservation-critical.

A TEP that preserves evidence but loses provenance is incomplete.

---

# Provenance Definition

Provenance is the collection of information required to reconstruct:

```text
origin

authority

generation

transformation

transport

validation

interpretation context
```

of an evidence object.

Provenance may apply to:

```text
TEPs

artifacts

entities

records

lineage edges

source attributions

validation outputs
```

---

# Provenance Layers

Provenance is hierarchical.

The following layers are considered preservation-critical.

---

## Layer 1: Producer Provenance

Producer provenance identifies the repository responsible for generating evidence.

Examples:

```text
VAP

GSC

RSP

RDGP

VDB
```

Producer provenance should include:

```text
producer identity

producer version

repository identity

repository release, when applicable
```

Producer provenance must survive ingestion.

VDB must not replace producer provenance with VDB ownership.

---

## Layer 2: Run Provenance

Run provenance identifies the execution instance responsible for generating evidence.

Examples:

```text
run_2026_06_03_010030

run_2026_06_18_191312
```

Run provenance should include:

```text
run_id

run timestamp

run status

run validation state

run finalization state
```

For execution-oriented producers, run provenance is preservation-critical.

---

## Layer 3: Release Provenance

Release provenance identifies the logical release context associated with evidence.

Examples:

```text
epilepsy_semantic_gtr_experimental_v0.1

mitochondrial_semantic_gtr_experimental_v0.1
```

Release provenance should include:

```text
release identifier

release version

release timestamp

release scope
```

Release provenance complements run provenance.

Release provenance does not replace run provenance.

---

## Layer 4: Package Provenance

Package provenance identifies the package-level context transported by a TEP.

Examples:

```text
package_id

phenotype package

sample package

analysis package
```

Package provenance helps consumers understand intended evidence scope.

---

## Layer 5: Artifact Provenance

Artifact provenance identifies the source of a specific artifact.

Examples:

```text
source file

source directory

source stage

artifact role

artifact owner
```

Artifact provenance should allow consumers to determine:

```text
where the artifact came from

why the artifact exists

which evidence it supports
```

---

## Layer 6: Entity Provenance

Entity provenance identifies the origin of an evidence entity.

Examples:

```text
semantic_prior

observation_entity

routing_entity

validation_overlay
```

Entity provenance should preserve:

```text
entity role

entity origin

supporting artifacts

supporting authority context
```

---

## Layer 7: Lineage Provenance

Lineage provenance captures evidence evolution.

Examples:

```text
observation
    → normalization

normalization
    → routing

routing
    → interpretation

interpretation
    → prioritization

prioritization
    → validation
```

Lineage provenance is preservation-critical whenever evidence meaning depends upon transformation history.

---

## Layer 8: Transport Provenance

Transport provenance identifies how evidence moved between repositories.

Examples:

```text
source TEP

transport timestamp

transport version

transport package

transport validation state
```

Transport provenance enables evidence movement to remain visible after ingestion.

---

# Provenance Requirements

A compliant TEP must preserve sufficient provenance to reconstruct:

```text
producer

run

release

package

artifact

entity

lineage

transport
```

where applicable.

Not every producer requires every layer.

However, omission of a layer must not destroy evidence interpretability.

---

# Authority Preservation

Provenance must preserve authority boundaries.

Authority boundaries include:

```text
producer authority

run authority

artifact authority

validation authority
```

VDB may add provenance.

VDB must not overwrite producer provenance.

Producer provenance remains authoritative for producer-generated evidence.

---

# Source Attribution Provenance

Source attribution provenance identifies external evidence sources contributing to an evidence object.

Examples:

```text
EPI25

GTR

MitoCarta

ClinVar

VEP

gnomAD
```

Source attribution provenance should preserve:

```text
source identity

source role

source contribution context

source confidence context
```

Source attribution provenance is especially important for semantic-prior producers.

---

# Validation Provenance

Validation provenance captures validation state associated with evidence.

Validation provenance may include:

```text
validator identity

validation criteria

criteria version

validation timestamp

validation result
```

Validation provenance should remain visible after transport.

---

# Reproducibility Provenance

Provenance should support evidence reconstruction whenever possible.

Reproducibility provenance may include:

```text
producer version

configuration version

manifest version

artifact checksums

run identifiers

input references
```

A consumer should be able to determine whether evidence can be regenerated.

---

# Unknowns And Nullability

Provenance systems must preserve uncertainty.

The following states should remain distinguishable:

```text
unknown

missing

unresolved

not assessed

not applicable

negative
```

Missing provenance must not be silently converted into false provenance.

Unknown provenance must remain explicitly unknown.

---

# Additive Provenance

Consumers may add provenance.

For example:

```text
Producer
    ↓
TEP
    ↓
VDB Ingestion
```

creates new provenance.

The new provenance should be additive.

Examples:

```text
vdb_ingestion_timestamp

vdb_namespace_resolution_event

vdb_discovery_event
```

Additive provenance must not overwrite producer provenance.

---

# Provenance Preservation During Ingestion

VDB ingestion should:

```text
preserve producer provenance

preserve run provenance

preserve release provenance

preserve artifact provenance

preserve lineage provenance
```

Ingress processing must not discard provenance necessary for future reinterpretation.

---

# Provenance Preservation During Discovery

Discovery outputs should preserve provenance links back to source evidence.

Discovery systems should allow users to determine:

```text
what was discovered

why it was discovered

what evidence supports it

where the supporting evidence originated
```

without ambiguity.

---

# Anti-Patterns

The following violate this specification:

```text
overwriting producer provenance

collapsing run and release provenance

removing lineage provenance

removing source attribution

removing validation provenance

treating transport provenance as producer provenance

converting unknown provenance into assumed provenance

discarding provenance during ingestion

storing evidence without authority context
```

---

# Compliance Expectations

A provenance implementation should allow consumers to answer:

```text
Who produced this evidence?

What run produced it?

What release produced it?

What package transported it?

What artifacts support it?

What transformations occurred?

What validation was performed?

How did the evidence arrive here?

Can it be reconstructed?
```

without requiring access to undocumented external knowledge.

---

# Relationship To Other Specifications

This specification refines provenance obligations introduced by:

```text
tep_spec.md
```

Related specifications:

```text
artifact_manifest_spec.md
    artifact declaration

ingestion_event_spec.md
    ingestion behavior

namespace_resolution_spec.md
    identity brokerage behavior
```

Schema documents remain downstream of this specification.

---

# Summary

Provenance is the preserved history of evidence.

It captures origin, authority, transformation, validation, and transport.

Provenance exists at multiple layers including producer, run, release, package, artifact, entity, lineage, and transport levels.

A compliant provenance implementation preserves enough context to allow future systems to understand not only what evidence exists, but how that evidence came to exist.

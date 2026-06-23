# TEP Specification

## Purpose

This document defines the implementation-level specification for Transitional Evidence Products (TEPs) accepted by the Variant Database (VDB).

A TEP is a transportable evidence state produced by an upstream repository and prepared for discovery, validation, namespace brokerage, and persistence by VDB.

The purpose of a TEP is not merely to move files.

The purpose of a TEP is to preserve evidence, provenance, identity, topology, uncertainty, and scientific meaning across repository boundaries.

---

## Scope

This specification applies to all producer-side TEPs intended for VDB ingestion, including:

```text
GSC-TEP
    semantic prior evidence

VAP-TEP
    observed variant evidence and staged interpretation evidence

future RSP-TEP
    transcriptomic and functional evidence

future RDGP-TEP
    reasoned prioritization evidence

future VDB-TEP
    VDB-mediated evidence exports
```

This document defines required TEP concepts and obligations.

This document does not define:

```text
database schemas

SQL schemas

relational models

query surfaces

repository-specific scoring algorithms

producer implementation code

consumer implementation code
```

Those are governed separately by schema, implementation, and validation documentation.

---

## Core Definition

A Transitional Evidence Product is a producer-authored evidence package that contains or references:

```text
transport identity

producer identity

source authority context

payload or payload references

artifact manifest

provenance

validation state

evidence topology
```

A TEP may be:

```text
reference-based
    references authoritative producer artifacts

portable
    contains copied producer artifacts

hybrid
    contains selected artifacts and references others
```

Reference-based TEPs are valid when authoritative producer artifacts remain accessible and provenance remains reconstructable.

Portable TEPs may be introduced later for archival or machine-independent transfer.

---

## Core Principle

```text
A TEP preserves producer evidence.

A TEP does not replace producer evidence.
```

VDB may ingest, validate, index, broker, and persist TEP contents.

VDB must not treat TEP ingestion as ownership transfer of producer truth.

Producer repositories remain authoritative for the evidence they generate.

---

## Required Top-Level Concepts

A valid TEP must provide enough information for VDB to determine:

```text
What is this evidence product?

Who produced it?

What run or release generated it?

What evidence does it contain or reference?

Where are the authoritative artifacts?

What validation status does the producer assert?

What identities must be preserved?

What relationships give the evidence meaning?

What uncertainty or nullability must remain visible?
```

These questions may be answered through a single JSON file, a manifest, a directory package, or another declared package structure.

---

## TEP Identity

Every TEP must declare a stable TEP identity.

At minimum, TEP identity should include:

```text
tep_id

tep_type

tep_schema_version

producer repository

source run identity, when applicable

source release identity, when applicable

source package identity, when applicable

creation timestamp

validation state
```

TEP identity must not collapse producer identity.

For example:

```text
GSC-TEP identity
    must preserve release, phenotype, gene, package, and run context.

VAP-TEP identity
    must preserve sample, run, pipeline, package, and staged evidence context.
```

---

## Producer Authority

Every TEP must declare the producer repository responsible for the transported evidence.

Producer authority should include:

```text
producer name

producer version, when available

source repository identity

source run identity

source package identity

source validation status

source finalization status, when available
```

Producer authority must remain distinguishable from VDB authority.

VDB may broker identities.

VDB must not overwrite source authority.

---

## Source Authority Boundary

A TEP must identify the authoritative source boundary for the evidence it transports.

Examples include:

```text
finalized producer run directory

final run manifest

source package directory

TEP package root

copied artifact directory
```

For finalized-run producers, the finalized run should be treated as the strongest source authority boundary.

A release may identify a distribution concept.

A finalized run identifies an evidentiary execution state.

---

## TEP Payload

The payload is the evidence-bearing portion of a TEP.

Payloads may differ substantially across producer repositories.

A TEP payload may contain:

```text
semantic priors

observed variants

annotation records

interpretation overlays

validation overlays

source attribution records

stage lineage records

context sidecars

summary metadata
```

TEP payloads are not required to share a common biological schema.

Common transport governance does not imply common payload structure.

---

## Payload Authority

Payload contents remain producer-owned.

VDB may inspect payloads for discovery and ingestion.

VDB may construct additive namespace mappings.

VDB must not destructively normalize payload contents.

VDB must preserve enough source context to reconstruct producer meaning.

---

## Payload Summaries

A TEP may include package-level summaries.

Package-level summaries are optional convenience metadata.

Summaries must not replace passenger-level evidence.

If summaries are present, they must be clearly interpreted as non-authoritative unless explicitly stated otherwise.

A valid TEP may omit package-level summaries when summarization would risk semantic collapse.

---

## Artifact Manifest

A TEP must include or reference an artifact manifest.

The artifact manifest describes the evidence artifacts associated with the TEP.

Each artifact record should identify:

```text
artifact_id or source_artifact_role

artifact path or transport path

artifact type

producer ownership

semantic role

source stage, when applicable

row count, when applicable

column count, when applicable

variant or entity count, when applicable

hash or checksum, when available

source existence status, when applicable
```

Artifact manifests may describe referenced artifacts, copied artifacts, or both.

The manifest must allow VDB to determine what files belong to the TEP and what role each file plays.

---

## Evidence Entities

A TEP may organize artifacts into evidence entities.

An evidence entity is a conceptual evidence unit that may be represented by one or more artifacts.

Examples:

```text
semantic_prior

observation_entity

normalization_entity

routing_entity

coding_interpretation_overlay

noncoding_interpretation_overlay

prioritization_overlay

validation_overlay

context_sidecar

lineage_manifest
```

Entities are not database tables.

Entities are producer-declared evidence classes.

VDB may later map entities into database schemas, but schema mapping is outside this specification.

---

## Evidence Topology

A TEP must preserve topology when topology is required to understand evidence meaning.

Topology may include:

```text
source-to-gene relationships

phenotype-to-gene relationships

observation-to-annotation relationships

stage-to-stage lineage

routing relationships

interpretation relationships

prioritization relationships

validation relationships

contextualization relationships
```

Topology may be represented through lineage edges, source matrices, provenance tables, entity relationships, or other producer-declared structures.

A TEP that preserves only terminal outputs may be invalid if intermediate evidence states are required for reinterpretation.

Candidate-only preservation is insufficient for staged evidence producers when prior stages contain preservation-critical substrate.

---

## Provenance

A TEP must preserve provenance sufficient to reconstruct:

```text
where evidence originated

which repository generated it

which run generated it

which release or package it belongs to

which artifacts support it

which version of the producer generated it

which validation status applied at construction time
```

Provenance may appear at multiple levels:

```text
TEP-level provenance

artifact-level provenance

entity-level provenance

record-level provenance

source-attribution provenance
```

Producer-side provenance must remain visible after VDB ingestion.

---

## Validation State

A TEP must declare producer-side validation state.

At minimum, validation state should distinguish:

```text
candidate

pass

fail

unknown
```

Where available, validation metadata should include:

```text
validation status

validation timestamp

validator version

criteria version

criteria passed

criteria failed
```

VDB may perform additional consumer-side validation.

Producer-side validation and VDB-side validation are distinct.

---

## Reference-Based TEPs

A reference-based TEP points to authoritative producer artifacts rather than packaging all cargo directly.

Reference-based TEPs must provide:

```text
authoritative source boundary

artifact paths

artifact roles

producer ownership

validation status

provenance context

source artifact authority declaration
```

A reference-based TEP is valid only if consumers can determine where authoritative artifacts reside and what each referenced artifact means.

Reference-based TEPs are suitable for early producer-to-VDB interoperability when producer artifacts remain available.

---

## Portable TEPs

A portable TEP contains copied artifacts sufficient for transfer outside the producer repository or filesystem.

Portable TEPs may include:

```text
TEP metadata

artifact manifest

payload artifacts

source manifests

validation reports

bundle manifest

checksums
```

Portable TEPs are not required for initial VDB interoperability unless external transfer or archival independence is required.

Reference-based TEPs should be designed so portable bundles can be added later without changing producer evidence semantics.

---

## GSC-TEP Requirements

A GSC-TEP transports semantic prior evidence.

At minimum, a GSC-TEP should preserve:

```text
TEP identity

release identity

package identity

phenotype identity

semantic prior count

gene identity

semantic prior identity

consensus scores

scoring profile

semantic channels

source attribution

evidence tier summaries

mapping status

provenance

artifact manifest

finalized run context
```

A GSC-TEP must not collapse semantic priors into binary gene membership.

The combination of phenotype, release, and gene identity is preservation-critical.

---

## VAP-TEP Requirements

A VAP-TEP transports observed biological substrate and staged interpretation evidence.

At minimum, a VAP-TEP should preserve:

```text
TEP identity

sample identity

run identity

pipeline identity

observation entity

normalization entity

routing entity

coding interpretation overlay

noncoding interpretation overlay

prioritization overlay

validation overlay

context sidecar

lineage manifest

artifact checksums

stage relationships

validation report
```

A VAP-TEP must not preserve only final candidates when earlier stages contain observed substrate or interpretation context.

Observed variants, weakly filtered or unfiltered substrate, interpretation overlays, prioritization outputs, and validation outputs should remain distinguishable.

---

## Observation Versus Interpretation

TEPs should preserve the distinction between:

```text
observation

annotation

interpretation

prioritization

validation

summary
```

This distinction is especially important for VAP-like producers.

An observed variant is not equivalent to a prioritized variant.

A non-prioritized variant is not equivalent to an absent variant.

An unannotated variant is not equivalent to a biologically irrelevant variant.

---

## Semantic Prior Versus Observation

TEPs should preserve the distinction between semantic-prior evidence and observed biological evidence.

For example:

```text
GSC-TEP
    transports phenotype-scoped semantic priors.

VAP-TEP
    transports observed variants and staged interpretation overlays.
```

VDB must be able to ingest both without forcing them into the same payload model.

This is a core interoperability requirement.

---

## Nullability And Unknowns

TEPs must preserve uncertainty and nullability.

Missing data must not be silently converted into negative evidence.

Examples:

```text
no ClinVar annotation
    does not mean benign

no VEP consequence
    does not mean biologically irrelevant

no source support
    does not mean impossible future relevance

unresolved mapping
    does not mean invalid evidence
```

Where possible, TEPs should distinguish:

```text
unknown

not applicable

not assessed

unresolved

missing

negative
```

---

## Namespace Readiness

A TEP should preserve source identifiers in their producer-declared form.

VDB may create additive namespace mappings.

VDB must not erase source identifiers during namespace brokerage.

TEPs should expose enough identity context for VDB to broker relationships among:

```text
gene identifiers

variant identifiers

sample identifiers

run identifiers

release identifiers

package identifiers

phenotype identifiers

artifact identifiers
```

Namespace resolution is a downstream VDB process.

TEP construction must preserve the raw identity material required for that process.

---

## Ingestion Readiness

A TEP is ingestion-ready when VDB can determine:

```text
the producer

the evidence type

the source authority boundary

the payload or payload references

the artifact manifest

the validation state

the provenance context

the identity spaces involved

the topology required for meaning
```

Ingestion readiness does not require that VDB already has final storage schemas.

It requires that the TEP is sufficiently self-describing for consumer-side validation and routing.

---

## Anti-Patterns

The following violate this specification:

```text
candidate-only preservation for staged evidence producers

binary gene-list export without source attribution for semantic-prior producers

destructive namespace normalization

loss of producer identity

loss of run identity

loss of package identity

loss of phenotype identity where phenotype defines meaning

loss of stage lineage where stages define meaning

collapsing unknown into negative

treating package-level summaries as replacements for record-level evidence

mutating producer artifacts during TEP construction

declaring VDB-owned meaning for producer-owned evidence
```

---

## Compliance Expectations

A TEP implementation should be evaluated against the following questions:

```text
Does the TEP identify itself?

Does it identify its producer?

Does it identify its source authority boundary?

Does it preserve evidence payload or payload references?

Does it describe artifacts and their roles?

Does it preserve provenance?

Does it preserve identity spaces?

Does it preserve required topology?

Does it preserve uncertainty?

Does it distinguish observation from interpretation when needed?

Does it avoid candidate-only collapse?

Can VDB discover and validate it without guessing?
```

A TEP that cannot answer these questions should not be considered mature.

---

## Relationship To Other Specifications

This document is the root implementation specification for TEPs.

Related specifications should refine specific concerns:

```text
artifact_manifest_spec.md
    defines artifact declaration requirements

provenance_spec.md
    defines provenance requirements

ingestion_event_spec.md
    defines VDB ingestion events

namespace_resolution_spec.md
    defines VDB namespace brokerage behavior
```

Schema documents are downstream of this specification.

---

## Summary

A TEP is a transportable evidence state.

It preserves producer evidence across repository boundaries without transferring producer authority to VDB.

GSC-TEP demonstrates semantic-prior transport.

VAP-TEP demonstrates observed-substrate and evidence-lineage transport.

Together, these producer families establish the central VDB requirement:

```text
VDB must ingest heterogeneous evidence products
without collapsing their source authority,
payload meaning,
provenance,
identity,
topology,
or uncertainty.
```

TEPs are therefore not simple exports.

They are evidence preservation contracts between producer repositories and VDB.

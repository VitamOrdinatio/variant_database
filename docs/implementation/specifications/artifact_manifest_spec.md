# Artifact Manifest Specification

## Purpose

This document defines the specification for Artifact Manifests used within Transitional Evidence Products (TEPs).

An Artifact Manifest provides a structured inventory of evidence-bearing artifacts associated with a TEP.

Its purpose is to allow consumers to determine:

```text
What artifacts exist?

What role does each artifact play?

Where does each artifact reside?

Who owns each artifact?

How can artifact integrity be verified?

How does each artifact contribute to evidence interpretation?
```

Artifact manifests support:

```text
transport

validation

provenance

traceability

reconstruction

future reinterpretation
```

Artifact manifests do not define biological meaning.

Artifact manifests define artifact identity and artifact relationships.

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
artifact declaration

artifact identity

artifact integrity

artifact role description

artifact ownership

artifact transport metadata
```

This specification does not govern:

```text
payload schemas

database schemas

query surfaces

scientific scoring models

producer algorithms

consumer algorithms
```

---

# Core Definition

An artifact is a producer-generated object that contributes evidence, context, lineage, provenance, validation, or interpretation to a TEP.

Examples include:

```text
TSV

CSV

JSON

YAML

Parquet

VCF

manifest files

lineage records

validation reports

context sidecars
```

An Artifact Manifest is a structured declaration describing those artifacts.

---

# Core Principle

```text
Artifacts carry evidence.

Manifests describe artifacts.
```

The manifest must not replace artifact contents.

The manifest exists so consumers can understand what artifacts exist and how those artifacts should be interpreted.

---

# Manifest Requirements

Every TEP must include or reference an Artifact Manifest.

A manifest must allow a consumer to determine:

```text
artifact identity

artifact purpose

artifact location

artifact ownership

artifact integrity status

artifact relationship to evidence
```

A manifest must be sufficiently descriptive for ingestion, validation, and discovery routing.

---

# Artifact Identity

Every artifact must possess a stable identity within the scope of the TEP.

At minimum:

```text
artifact_id

artifact_role

artifact_type
```

should be declared.

Artifact identifiers must remain stable within a TEP package.

Artifact identifiers need not be globally unique.

---

# Artifact Role

Artifact role is mandatory.

Artifact role answers:

```text
Why does this artifact exist?
```

Examples:

```text
semantic_prior_table

source_contribution_table

observation_entity

normalization_entity

routing_entity

coding_interpretation_overlay

noncoding_interpretation_overlay

prioritization_overlay

validation_overlay

context_sidecar

lineage_manifest

validation_report
```

Artifact role is preservation-critical.

Consumers should interpret artifact role as authoritative producer intent.

---

# Artifact Type

Artifact type describes the technical representation.

Examples:

```text
tsv

csv

json

yaml

parquet

vcf

directory
```

Artifact type must not be confused with artifact role.

Example:

```text
artifact_role:
    validation_report

artifact_type:
    json
```

---

# Artifact Location

Every artifact must declare where it can be found.

Location may be represented as:

```text
source_path

transport_path

bundle_path

artifact_uri
```

Reference-based and portable TEPs may use different path strategies.

The manifest must make artifact retrieval unambiguous.

---

# Artifact Ownership

Every artifact must identify its producer authority.

Examples:

```text
GSC

VAP

RSP

RDGP

VDB
```

Ownership remains attached to artifacts after ingestion.

VDB ingestion must not overwrite producer ownership.

---

# Artifact Integrity

Artifact manifests should provide integrity metadata whenever available.

Recommended fields include:

```text
sha256

md5

size_bytes

creation_timestamp
```

Integrity metadata enables:

```text
validation

reconstruction

transport verification

bundle verification
```

Integrity metadata is strongly recommended for portable artifacts.

---

# Artifact Metrics

Artifacts may expose descriptive metrics.

Examples:

```text
row_count

column_count

entity_count

variant_count

gene_count

record_count
```

Metrics exist to aid validation and discovery.

Metrics must not be interpreted as evidence quality scores.

---

# Artifact Provenance

Artifacts should expose provenance metadata sufficient to determine:

```text
source repository

source run

source release

source package

producer version
```

Artifact provenance complements but does not replace TEP-level provenance.

---

# Artifact Validation Status

Artifacts may declare validation metadata.

Examples:

```text
validation_status

validation_timestamp

validator

criteria_version
```

Artifact validation state should be preserved when available.

---

# Artifact Categories

Artifacts generally fall into one or more categories:

## Evidence Artifacts

Contain primary evidence.

Examples:

```text
semantic priors

variant observations

annotation records

interpretation outputs
```

---

## Context Artifacts

Provide supporting interpretation context.

Examples:

```text
context sidecars

source attribution tables

metadata tables
```

---

## Provenance Artifacts

Describe evidence origin.

Examples:

```text
manifests

lineage records

run metadata
```

---

## Validation Artifacts

Describe validation state.

Examples:

```text
validation reports

acceptance reports

quality assessments
```

---

## Administrative Artifacts

Support transport and reconstruction.

Examples:

```text
bundle manifests

checksums

package inventories
```

---

# Relationship To Evidence Entities

Artifacts and entities are not synonymous.

An entity may be represented by:

```text
one artifact

many artifacts
```

An artifact may support:

```text
one entity

many entities
```

The manifest should preserve enough information to reconstruct these relationships.

---

# Reference-Based Artifact Manifests

Reference-based manifests describe artifacts that remain inside producer-controlled environments.

Reference manifests should declare:

```text
authoritative source location

artifact role

artifact ownership

artifact integrity metadata
```

Reference manifests must preserve sufficient information for later retrieval and validation.

---

# Portable Artifact Manifests

Portable manifests describe artifacts packaged inside transport bundles.

Portable manifests should additionally declare:

```text
bundle path

bundle checksum

transport integrity state
```

Portable manifests must support machine-independent reconstruction.

---

# Discovery Requirements

Artifact manifests should support discovery without requiring artifact inspection.

Consumers should be able to determine:

```text
what evidence classes exist

what artifact roles exist

what provenance exists

what validation artifacts exist
```

from the manifest alone.

The manifest should function as a catalog of evidence availability.

---

# Anti-Patterns

The following violate this specification:

```text
artifacts without declared roles

artifacts without ownership

artifacts without locations

artifact inventories that require payload inspection to understand purpose

artifact roles encoded solely in filenames

artifact manifests that mutate producer meaning

manifests that replace artifact contents

silent omission of validation artifacts

silent omission of provenance artifacts
```

---

# Compliance Expectations

A compliant Artifact Manifest allows a consumer to answer:

```text
What artifacts exist?

What role does each artifact serve?

Who produced each artifact?

Where does each artifact reside?

How can artifact integrity be verified?

How does each artifact relate to transported evidence?
```

without requiring prior knowledge of the producing repository.

---

# Relationship To Other Specifications

This specification refines artifact declaration requirements introduced by:

```text
tep_spec.md
```

Related specifications:

```text
provenance_spec.md
    provenance obligations

ingestion_event_spec.md
    ingestion behavior

namespace_resolution_spec.md
    identity brokerage behavior
```

Schema documents remain downstream of this specification.

---

# Summary

Artifact Manifests provide a structured declaration of evidence-bearing artifacts contained within or referenced by a TEP.

They preserve artifact identity, ownership, integrity, provenance, and purpose.

Artifact Manifests enable validation, reconstruction, interoperability, and discovery without altering producer authority or scientific meaning.

They are therefore the primary mechanism through which TEPs describe the evidence assets they transport.

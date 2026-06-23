# Namespace Resolution Specification

## Purpose

This document defines the specification for namespace resolution within the Variant Database (VDB).

Namespace resolution is the process through which VDB identifies, relates, brokers, and preserves identities originating from heterogeneous producer repositories and external evidence sources.

The purpose of namespace resolution is not to replace source identities.

The purpose of namespace resolution is to preserve source identities while enabling cross-domain interoperability.

---

# Scope

This specification applies to:

```text
GSC-TEP

VAP-TEP

future RSP-TEP

future RDGP-TEP

future VDB-TEP

external evidence sources
```

This specification governs:

```text
identity discovery

identity preservation

identity brokerage

cross-namespace relationships

canonical identity assignment

identity lineage

identity reconciliation
```

This specification does not govern:

```text
database schemas

query implementation

scientific scoring

payload interpretation

producer-side identity generation
```

---

# Core Principle

```text
Namespace resolution
preserves identity.

Namespace resolution
does not replace identity.
```

VDB exists to connect identities.

VDB does not exist to erase identities.

---

# Core Definition

A namespace is a bounded identity space.

Examples:

```text
Ensembl Gene

HGNC Symbol

NCBI Gene

ClinVar Variant

dbSNP Variant

Sample Identifier

Run Identifier

Package Identifier

TEP Identifier

Phenotype Identifier
```

Each namespace defines its own identity rules.

Namespace resolution is the process of creating relationships among identities originating from different namespaces.

---

# Identity Preservation Principle

The original identity emitted by a producer must remain recoverable.

Examples:

```text
SCN1A

ENSG00000144285

NCBIGene:6323

HG002

ERR10619300

run_2026_06_03_010030
```

Namespace brokerage must preserve these source identities.

Source identities must not be overwritten during resolution.

---

# Identity Brokerage Model

VDB acts as an identity broker.

Conceptually:

```text
Producer Identity
        ↓
Namespace Brokerage
        ↓
Canonical Identity
        ↓
Related Identities
```

Identity brokerage enables interoperability.

Identity brokerage does not invalidate source identities.

---

# Canonical Identity

VDB may assign canonical identities.

Canonical identities exist to provide stable reference points for discovery and persistence.

Examples:

```text
canonical_gene_id

canonical_variant_id

canonical_sample_id

canonical_phenotype_id
```

Canonical identities should be:

```text
stable

reproducible

internally consistent
```

Canonical identities must not replace source identities.

---

# Source Identity Preservation

Every namespace resolution event must preserve:

```text
source_identifier

source_namespace

source_authority

source_producer
```

Consumers must be able to reconstruct the original producer-declared identity.

---

# Namespace Authority

Every namespace possesses an authority.

Examples:

```text
HGNC
    gene symbol authority

Ensembl
    gene identifier authority

ClinVar
    clinical variant authority

Producer Repository
    run identifier authority

Producer Repository
    package identifier authority
```

Namespace resolution should respect authority boundaries.

VDB may broker identities.

VDB must not claim authority over external namespace definitions.

---

# Resolution Targets

Namespace resolution may operate on:

```text
genes

variants

samples

phenotypes

runs

releases

packages

artifacts

TEPs
```

Additional identity classes may be introduced in future versions.

---

# Resolution Outcomes

Resolution outcomes may include:

```text
resolved

partially_resolved

ambiguous

unresolved

deferred
```

These states must remain distinguishable.

---

# Resolved Identity

A resolved identity is one for which VDB can establish a confident mapping.

Example:

```text
SCN1A
    ↔ ENSG00000144285
```

Resolution should preserve both sides of the mapping.

---

# Partially Resolved Identity

A partially resolved identity possesses incomplete but useful mapping information.

Examples:

```text
gene symbol known

stable identifier unavailable
```

or

```text
variant coordinate known

canonical variant unresolved
```

Partial resolution remains valuable evidence.

---

# Ambiguous Identity

An ambiguous identity possesses multiple plausible mappings.

Examples:

```text
historical aliases

deprecated identifiers

multi-mapping records
```

Ambiguity must remain visible.

Ambiguity must not be silently collapsed.

---

# Unresolved Identity

An unresolved identity cannot currently be mapped.

Examples:

```text
novel identifier

unknown identifier

future namespace
```

Unresolved identities remain valid evidence.

Unresolved identities must remain queryable and recoverable.

---

# Deferred Resolution

Resolution may be deferred.

Examples:

```text
external service unavailable

authority unavailable

resolution algorithm unavailable
```

Deferred resolution is not equivalent to failure.

---

# Identity Lineage

Namespace resolution should preserve identity lineage.

Examples:

```text
old identifier
    →
new identifier

alias
    →
canonical identity

producer identifier
    →
brokered identity
```

Identity lineage enables historical reconstruction.

---

# Additive Resolution

Namespace resolution must be additive.

Resolution should create:

```text
relationships

mappings

cross-references
```

Resolution should not modify source evidence.

---

# Resolution Provenance

Every resolution event should produce provenance.

Examples:

```text
resolution_event_id

resolution_timestamp

resolution_method

resolution_version

resolution_outcome
```

Resolution provenance supports auditing and future reinterpretation.

---

# Producer-Specific Examples

## GSC

Examples:

```text
gene symbols

Ensembl identifiers

phenotype identifiers

semantic prior identifiers
```

Resolution must preserve phenotype-scoped context.

---

## VAP

Examples:

```text
sample identifiers

variant identifiers

gene identifiers

run identifiers

artifact identifiers
```

Resolution must preserve observation lineage context.

---

## Future RDGP

Examples:

```text
sample-gene relationships

candidate identifiers

reasoning identifiers
```

Resolution must preserve reasoning context.

---

# Discovery Requirements

Namespace resolution should support discovery across identity spaces.

Examples:

```text
gene
    ↔ variant

gene
    ↔ phenotype

sample
    ↔ variant

sample
    ↔ candidate

TEP
    ↔ evidence entity
```

Resolution enables these relationships.

Resolution does not create scientific meaning.

Scientific meaning remains producer-derived.

---

# Clinical Future-Proofing

Namespace resolution should preserve identities even when current biological interpretation is incomplete.

Examples:

```text
unannotated variants

high-frequency variants

novel genes

novel phenotypes

future evidence classes
```

Future discovery may create new mappings.

Therefore identity preservation is mandatory even when interpretation is unavailable.

---

# Unknowns And Nullability

Namespace resolution must preserve:

```text
unknown

missing

ambiguous

unresolved

deferred
```

These states must not be collapsed into:

```text
resolved

negative

invalid
```

without explicit evidence.

---

# Anti-Patterns

The following violate this specification:

```text
overwriting source identifiers

discarding unresolved identities

discarding ambiguous identities

silently selecting one mapping from multiple possibilities

removing namespace authority information

collapsing producer identities into canonical identities

treating unresolved as invalid

destroying identity lineage
```

---

# Compliance Expectations

A compliant namespace resolution implementation should allow consumers to answer:

```text
What identity was provided?

Which namespace owns it?

Was it resolved?

How was it resolved?

What canonical identity was assigned?

What alternate identities exist?

What authority supports the mapping?

Can the original identity be recovered?
```

without requiring external undocumented assumptions.

---

# Relationship To Other Specifications

This specification builds upon:

```text
tep_spec.md

artifact_manifest_spec.md

provenance_spec.md

ingestion_event_spec.md
```

Namespace resolution occurs after ingestion.

Namespace resolution creates identity relationships that later support persistence, discovery, and query surfaces.

Schema documents remain downstream of this specification.

---

# Summary

Namespace resolution is the process through which VDB brokers relationships among heterogeneous identity spaces.

It preserves source identities, authority boundaries, identity lineage, and resolution provenance while enabling interoperability across repositories and evidence domains.

Namespace resolution therefore functions as identity stewardship rather than identity replacement.

VDB connects identities.

VDB does not erase identities.

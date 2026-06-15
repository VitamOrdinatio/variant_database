# Namespace Resolution Engine Design

## Purpose

The namespace resolution engine defines how VDB should relate heterogeneous biological identifiers without mutating source evidence.

VDB receives evidence from repositories that use different identity systems.

Examples include:

* variant identifiers
* gene identifiers
* transcript identifiers
* phenotype identifiers
* sample identifiers
* release identifiers
* run identifiers
* transport identifiers

The namespace resolution engine exists to create additive, provenance-preserving identity relationships that allow evidence to interoperate across repositories.

It does not replace source identities.

It does not redefine biological meaning.

It does not mutate TEP payloads.

Its role is to broker identities.

---

## Design Principle

Namespace resolution is additive brokerage.

The engine should preserve:

```text
source identity
        +
canonical relationship
        +
resolution provenance
```

rather than replacing source identity with a canonical value.

Canonical identities are brokerage artifacts.

They support interoperability, but they do not replace source-native identifiers.

---

## Architectural Position

The namespace resolution engine operates after initial discovery and validation and before final persistence routing.

```text
TEP Transport
        ↓
Discovery / Profiling
        ↓
Validation
        ↓
Namespace Resolution
        ↓
Canonical Identity Relationships
        ↓
Discovery Routing
        ↓
Semantic Persistence Domains
        ↓
Query Surfaces
```

This ordering preserves the separation among transport, discovery, brokerage, persistence, and query exposure.

---

## Authority Boundaries

The engine must preserve the following authority boundaries:

```text
Producer Repositories
        own source meaning

TEPs
        preserve transport state

Namespace Resolution Engine
        brokers identity relationships

Discovery
        consumes identity relationships for routing

Persistence Domains
        organize evidence semantically

RDGP and other consumers
        consume queryable evidence surfaces
```

The namespace resolution engine should not become a hidden semantic interpretation layer.

---

## Input Identity Classes

The engine should support multiple identity classes.

Representative classes include:

```text
gene identifiers

variant identifiers

transcript identifiers

phenotype identifiers

sample identifiers

assay identifiers

run identifiers

release identifiers

source artifact identifiers

TEP identifiers
```

Each identity class may have multiple namespaces.

For example, gene identity may include:

```text
HGNC

Ensembl

NCBI Gene

gene symbol

source-specific aliases
```

Variant identity may include:

```text
chromosome-position-ref-alt

dbSNP

VEP-derived identifiers

source-local variant identifiers
```

Phenotype identity may include:

```text
HPO

OMIM

source-local phenotype labels

repository-defined phenotype scopes
```

---

## Source Identity Preservation

Every source identifier should remain preserved.

For each resolved identity, VDB should retain:

* source identifier
* source namespace
* source repository
* source artifact
* source package identity
* source field or column, when applicable
* source value
* resolution event

This allows future users to reconstruct how an identity entered VDB.

---

## Canonical Identity Assignment

Canonical identities provide stable routing anchors.

Examples include:

```text
canonical_gene_id

canonical_variant_id

canonical_transcript_id

canonical_phenotype_id

canonical_sample_id
```

Canonical identities should be assigned only through explicit resolution events.

The engine should not silently infer canonical identity without preserving mapping evidence.

---

## Resolution Events

Namespace resolution should be represented as an auditable event.

Each event should preserve:

```text
resolution_event_id

source_identifier

source_namespace

target_identifier

target_namespace

canonical_identifier

mapping_status

mapping_method

mapping_source

mapping_version

resolution_timestamp

confidence_or_quality_flag

ambiguity_state
```

Resolution events are provenance.

They should be persisted and queryable.

---

## Mapping Status

The engine should support explicit mapping status values.

Recommended statuses include:

```text
resolved

unresolved

ambiguous

deprecated

conflicting

not_applicable

pending_review
```

These states prevent silent collapse of uncertainty.

Unresolved identity is not failure by default.

Ambiguous identity is not failure by default.

Both are evidence states that should remain visible.

---

## Ambiguity Handling

Namespace ambiguity is expected.

Examples include:

* one source identifier maps to multiple canonical identifiers
* multiple source identifiers map to one canonical identifier
* gene symbols are reused or deprecated
* transcript identifiers map differently across annotation versions
* phenotype labels are underspecified
* source-local terms lack ontology equivalents

The engine should preserve ambiguity rather than conceal it.

Where ambiguity exists, downstream query surfaces should be able to filter or expose ambiguity state.

---

## Versioned Mapping Sources

Identity resolution depends on mapping resources.

Examples include:

```text
HGNC reference tables

Ensembl releases

NCBI Gene mappings

HPO releases

ClinVar releases

VEP annotation versions
```

The engine should preserve mapping-source version information.

A resolution that was valid under one mapping release may differ under a later mapping release.

Historical reproducibility requires versioned resolution provenance.

---

## Gene Namespace Resolution

Gene namespace resolution is a primary v1 concern.

VDB may receive gene evidence from:

* VAP
* GSC
* future RSP
* RDGP-facing query surfaces
* external metadata resources

These sources may use different identifiers.

The engine should support additive relationships among:

```text
HGNC ID

Ensembl gene ID

NCBI Gene ID

gene symbol

source-local gene identifier
```

The canonical gene identity should support interoperability while preserving every source-native identifier.

---

## Variant Namespace Resolution

Variant namespace resolution should preserve both variant entities and variant observations.

Variant evidence may arrive as:

```text
chromosome-position-ref-alt

VCF-style alleles

dbSNP identifiers

source-local variant identifiers

annotation-derived variant identifiers
```

The engine should distinguish:

```text
variant entity
```

from:

```text
variant observation
```

This distinction prevents sample-specific evidence from collapsing into universal variant identity.

---

## Phenotype Namespace Resolution

Phenotype evidence may arrive through:

* GSC phenotype scopes
* RDGP phenotype context
* source-local disease labels
* ontology identifiers
* cohort labels

The engine should preserve phenotype scope explicitly.

Phenotype labels should not be silently mapped to ontology terms unless the mapping is recorded.

Phenotype context is part of identity governance, especially for semantic overlays.

---

## Overlay Identity Resolution

Semantic overlays require special identity handling.

A GSC-derived semantic prior may be identified by:

```text
(gsc_release_id, phenotype, source_gene_id)
```

After brokerage, VDB may support:

```text
(gsc_release_id, phenotype, canonical_gene_id)
```

The source identity remains preserved.

The canonical identity enables attachment.

The release identity remains part of the overlay identity.

GSC release identity must not be treated as optional metadata.

---

## Identity-Space Bridging

Some VDB workflows require bridging distinct identity spaces.

Examples include:

```text
phenotype-gene evidence
        ↔
sample-gene evidence

variant evidence
        ↔
gene evidence

transcript evidence
        ↔
gene evidence
```

Identity-space bridging should remain explicit and explainable.

The engine should create relationships that support bridging while preserving the identity spaces involved.

---

## Relationship to RDGP Query Surfaces

RDGP consumes gene-level evidence surfaces.

VDB may need to aggregate variant-centric evidence into:

```text
(sample_id, gene_id)
```

records.

Namespace resolution supports this transformation by enabling variant-to-gene and source-gene-to-canonical-gene relationships.

However, namespace resolution does not perform RDGP reasoning.

It only provides identity relationships required for query-surface construction.

---

## Relationship to Discovery

Discovery answers:

```text
What does this artifact contain?
```

Namespace resolution answers:

```text
How do the artifact's identities relate to known identity systems?
```

The discovery engine may detect identifier-like fields.

The namespace resolution engine resolves those identifiers.

Discovery routing may then use resolved canonical identities to support deterministic persistence decisions.

---

## Relationship to TEPs

TEPs preserve producer-owned evidence states.

The namespace resolution engine must not mutate TEP payloads.

When resolving identities contained in a TEP, VDB should create additive resolution records outside the immutable payload.

The TEP remains unchanged.

The brokerage layer records how VDB interpreted identity relationships for persistence and query exposure.

---

## Relationship to Semantic Persistence Domains

Semantic persistence domains consume namespace-resolution outputs.

Examples:

```text
Variant evidence domain
        uses canonical_variant_id and source variant identities

Gene evidence domain
        uses canonical_gene_id and source gene identities

Overlay evidence domain
        uses release-scoped phenotype-gene identities

Provenance domain
        stores resolution events
```

Persistence domains should not create identity authority independently.

---

## Design Outputs

The namespace resolution engine should produce:

* canonical identity records
* source identity records
* identity relationship records
* resolution event records
* ambiguity reports
* unresolved identity reports
* mapping-source provenance records
* namespace validation warnings

These outputs should be persisted and queryable.

---

## Failure Modes

The engine should guard against:

* source identity erasure
* silent alias collapse
* unversioned mappings
* ambiguity concealment
* source-field loss
* payload mutation
* adapter-specific hidden normalization
* canonical identity overclaiming
* phenotype-context loss
* release-identity loss

These are architectural failures, not minor implementation issues.

---

## v1 Scope Recommendation

Recommended v1 scope:

* gene namespace resolution
* source identity preservation
* canonical gene identity assignment
* mapping status preservation
* mapping-source/version preservation
* unresolved and ambiguous state handling
* TEP-safe additive resolution records
* support for GSC overlay attachment
* support for VAP variant-to-gene query routing
* support for RDGP-facing sample-gene evidence surfaces

Defer to later releases:

* full ontology resolution lifecycle
* complex phenotype hierarchy reasoning
* graph-based identity reasoning
* transcript-version reconciliation at scale
* protein and pathway namespace brokerage
* automated conflict adjudication
* ML-driven identity inference

---

## Summary

The namespace resolution engine is VDB's design mechanism for additive identity brokerage.

It relates heterogeneous source identifiers to canonical identities while preserving source identity, provenance, ambiguity, mapping context, and historical reproducibility.

It does not own biological meaning.

It does not mutate TEP payloads.

It does not perform downstream reasoning.

It creates the identity relationships that allow discovery, semantic persistence, overlay attachment, and query surfaces to operate safely across repository boundaries.

# Namespace Authority Model

## Purpose

The purpose of this document is to define identity authority, namespace authority, canonical identity governance, and brokerage responsibilities within VDB.

The repository ecosystem contains multiple identity spaces, multiple namespace systems, multiple evidence models, and multiple biological coordinate systems.

Interoperability therefore requires a governed mechanism for relating identities without altering the meaning of upstream evidence.

This document establishes the authority boundaries that make such interoperability possible.

---

## Core Principle

Identity authority and semantic authority are not the same thing.

Producer repositories own semantic authority.

VDB owns namespace brokerage authority.

This distinction is foundational.

VDB exists to relate identities, not redefine biological meaning.

Namespace brokerage must preserve source identity, source namespace, coordinate context, feature context, producer context, and uncertainty.

---

## Coordinate-First Brokerage Principle

VDB's default namespace substrate for variant-derived evidence is genomic coordinate and reference-context identity.

Gene identity is essential, but it is not the root identity model for VDB.

Gene namespace brokerage is a routed specialization that applies when coordinate-centered evidence intersects, annotates to, or is otherwise related to named gene features.

This principle protects full-genome evidence preservation.

Variant-derived evidence must remain valid even when it falls outside named genes, outside current annotation models, or inside regions whose biological relevance is not yet understood.

The following pattern is therefore prohibited as a default VDB assumption:

```text
variant evidence
        ↓
required gene identity
        ↓
only gene-centered topology
```

The default VDB pattern is:

```text
coordinate / variant identity
        ↓
feature and interval relationships when available
        ↓
gene relationships when supported
        ↓
evidence topology and convergence geometry
```

This allows known gene annotations to participate in present-day convergence geometry while preserving noncoding and currently unannotated evidence for future discovery.

---

## Architectural Authority Chain

The ecosystem recognizes distinct authority domains.

```text
Producer Truth
        ↓
TEP Transport
        ↓
Source Identity Preservation
        ↓
Namespace Brokerage
        ↓
Discovery and Persistence Consumption
        ↓
Downstream Reasoning Consumption
```

Each domain possesses separate responsibilities.

Namespace brokerage begins before downstream persistence and query-surface construction.

Namespace brokerage must also be represented early enough that Assertion Records preserve namespace-aware identity state before they become immutable preservation artifacts.

---

## Producer Authority

Producer repositories remain authoritative for the evidence they generate.

Examples include:

```text
VAP
    Variant observations

GSC
    Semantic priors

Future RSP
    Functional observations

RDGP
    Reasoning outputs
```

Producer repositories determine:

* evidence meaning
* scoring logic
* evidence generation
* source-specific identifiers
* repository-specific semantics
* producer-native identity fields
* producer-native namespace declarations when emitted

Producer authority is never transferred to VDB.

VDB may broker identities emitted by producers.

VDB must not reinterpret producer evidence while doing so.

---

## Transport Authority

Transport authority is provided through the Transitional Evidence Product (TEP) architecture.

TEPs preserve:

* payload semantics
* provenance
* topology
* transport identity
* source-native identity fields when emitted
* producer-declared namespaces when emitted
* producer-supplied bridge artifacts when emitted

A TEP does not reinterpret evidence.

A TEP does not normalize evidence by default.

A TEP does not become VDB's namespace authority.

Its purpose is preservation and transport.

Transport authority therefore remains distinct from namespace authority.

---

## Namespace Brokerage Authority

VDB is the authoritative namespace broker of the ecosystem.

Its responsibilities include:

* identity reconciliation
* namespace resolution
* coordinate/reference-context identity brokerage
* interval and feature relationship brokerage
* canonical identity assignment
* identity relationship management
* identity provenance preservation
* ambiguity and unresolved-state preservation

Namespace brokerage exists because multiple repositories may legitimately describe related biological entities using different identifiers, coordinate systems, feature models, or producer-native identities.

Examples include:

```text
GRCh38 chr15:start-end ref/alt

ENSG00000140521

HGNC:9175

NCBIGene:5424

POLG

VAP run/sample/variant identity

GSC release/phenotype/gene identity
```

These are not conflicting truths.

They are alternative identity representations or related identity contexts.

VDB creates governed relationships among them.

VDB does not erase the participating identities.

---

## Brokerage Classes

VDB recognizes four primary brokerage classes.

```text
Default Coordinate Brokerage
        Root brokerage substrate for variant-derived evidence.

Feature Brokerage
        Brokerage between coordinates and biological intervals or annotation features.

Gene Brokerage
        Brokerage among gene identifiers, symbols, aliases, and gene-associated feature intervals.

Producer Brokerage
        Brokerage of source-native repository identities, releases, runs, artifacts, and source-local IDs.
```

These classes cooperate but must remain distinguishable.

Gene brokerage must not absorb coordinate brokerage.

Feature brokerage must not erase coordinate identity.

Producer brokerage must not be collapsed into external biological authority systems.

---

## Default Coordinate Brokerage

Default coordinate brokerage governs genomic coordinate and reference-context identity.

It is the default identity substrate for variant-derived evidence.

Representative fields include:

```text
reference_build

contig or chromosome

start coordinate

end coordinate

reference allele

alternate allele

variant type

coordinate convention

normalization status

source representation
```

Coordinate brokerage supports identities such as:

```text
single-nucleotide variant

small insertion or deletion

multi-base substitution

copy-number interval

structural variant interval

noncoding variant

intergenic variant

currently unannotated locus
```

A coordinate identity may later be related to gene, transcript, regulatory, or other feature identities.

That relationship is additive.

It does not replace the coordinate identity.

---

## Coordinate and Interval Authority

Coordinate and interval brokerage require explicit authority context.

Coordinate authority includes:

```text
reference genome build

contig naming convention

coordinate system

allele representation

normalization method

normalization version
```

Interval authority includes:

```text
reference genome build

contig

start coordinate

end coordinate

strand when applicable

feature source

feature source version

annotation release
```

Coordinate and interval identities are version-dependent.

For this reason, VDB must not treat a coordinate, interval, gene locus, or feature interval as complete without preserving the reference and annotation context required to reconstruct it.

---

## Feature Brokerage

Feature brokerage relates coordinate identities to biological intervals or annotation features.

Examples include:

```text
gene locus

transcript interval

exon

intron

UTR

splice region

promoter

enhancer

regulatory feature

conserved element

repeat element

burden window

future feature class
```

Feature brokerage supports relationships such as:

```text
variant overlaps feature

variant is contained by feature

variant contains feature

variant is near feature

variant annotates to feature

interval overlaps interval

burden window contains variants
```

Feature relationships are brokerage artifacts.

They must preserve the coordinate identity, the feature identity, the feature source, and the relationship type.

---

## Gene Brokerage

Gene brokerage relates gene identifiers and gene-associated identities.

Examples include:

```text
Ensembl gene identifier

NCBI Gene identifier

HGNC identifier

gene symbol

gene alias

source-local gene identifier
```

Gene brokerage remains essential for VDB because multiple evidence producers emit gene-centered evidence.

Examples include:

```text
GSC phenotype-gene semantic priors

future RSP gene or transcript evidence

RDGP-facing sample-gene surfaces

VAP-derived gene annotations from variant effects
```

However, gene brokerage is not the default substrate for variant-derived evidence.

A variant does not require a named gene to be preserved, organized, or exposed.

Gene brokerage applies when a variant coordinate, interval, transcript, or feature can be governedly related to a gene identity.

---

## Gene Identity and Gene Locus Are Distinct

A gene identity and a gene locus are not the same authority object.

Gene identity brokerage relates identifiers such as:

```text
POLG

HGNC:9175

ENSG-style gene identifiers

NCBI Gene identifiers
```

Gene locus brokerage relates genomic intervals associated with gene models, such as:

```text
reference_build

contig

start

end

strand

annotation_source

annotation_version
```

A semantic prior from GSC may be gene-identity-centered.

A variant observation from VAP may be coordinate-centered.

VDB can relate them only when a governed relationship exists between the coordinate identity, the gene locus or feature interval, and the gene identity.

For example:

```text
VAP variant coordinate
        ↓ overlaps / annotates_to
POLG gene locus interval
        ↓ represents / is_locus_for
POLG gene identity
        ↓ participates_in
GSC phenotype-gene semantic prior
```

This relationship enables evidence convergence without making gene identity the primary key for all variant evidence.

---

## Producer Brokerage

Producer brokerage governs repository-native identity spaces.

Examples include:

```text
VAP run identity

VAP sample identity

VAP source-local variant identity

GSC release identity

GSC phenotype scope

GSC source evidence identity

RSP experiment or contrast identity

RDGP reasoning output identity

TEP package identity

artifact identity
```

Producer identities remain authoritative within their producer-defined context.

VDB may relate producer identities to coordinate, feature, gene, phenotype, or sample identities.

VDB must not collapse producer identity into external biological identity.

---

## Discovery Authority

The discovery engine is not a namespace authority.

The discovery engine is a consumer of namespace authority.

Its responsibilities include:

* artifact profiling
* contract matching
* validation
* routing
* persistence-domain assignment

Discovery may detect namespace-bearing fields.

Discovery may route artifacts based on brokered identity relationships.

Discovery must not perform identity mutation.

Discovery must not redefine namespace relationships.

---

## Identity Spaces

The ecosystem contains multiple identity spaces.

Examples include:

```text
Coordinate Identity

Variant Identity

Allele Identity

Interval Identity

Feature Identity

Gene Identity

Gene Locus Identity

Transcript Identity

Regulatory Feature Identity

Phenotype Identity

Sample Identity

Disease Identity

Ontology Identity

Release Identity

Execution Identity

Transport Identity

Producer-Native Identity
```

These spaces are independent.

Interoperability should not require their collapse.

---

## Identity-Space Independence

Identity spaces are intentionally preserved.

Examples include:

```text
(sample_id, coordinate_variant_id)

(sample_id, gene_id)

(phenotype, gene_id)

(variant_id)

(coordinate_interval_id)

(gsc_release_id, phenotype, gene_id)

(vap_run_id, sample_id)
```

These identities serve different purposes.

They should remain distinguishable throughout the ecosystem.

Identity brokerage creates relationships among identity spaces without erasing them.

---

## Canonical Identities

Canonical identities exist to support interoperability.

A canonical identity is a brokerage artifact.

A canonical identity is not biological truth.

Examples include:

```text
canonical_coordinate_id

canonical_variant_id

canonical_interval_id

canonical_feature_id

canonical_gene_id

canonical_transcript_id

canonical_phenotype_id

canonical_sample_id

canonical_producer_identity_id
```

For example:

```text
canonical_gene_id
```

does not replace:

```text
ENSG identifier
HGNC identifier
NCBI gene identifier
Gene symbol
```

Instead, it provides a stable reference point through which those identities may be related.

Similarly:

```text
canonical_variant_id
```

does not replace source VCF representation, sample observation context, or producer-local variant identity.

Canonical coordinate or variant identities do not replace gene, transcript, feature, or producer identities.

Canonical identities are routing and interoperability aids, not evidence replacement mechanisms.

---

## Additive Normalization

All namespace normalization within VDB is additive.

Normalization must never erase source identities.

For every resolution event:

```text
Source Identity
        ↓
Canonical Relationship
        ↓
Canonical Identity
```

the original identifier must remain preserved and recoverable.

This requirement applies to all namespace systems, including coordinate, feature, gene, phenotype, sample, ontology, and producer-native namespaces.

---

## Resolution Events

Namespace resolution is treated as a first-class provenance activity.

Each resolution event should preserve:

```text
resolution_event_id

source_identifier

source_namespace

target_identifier

target_namespace

mapping_source

mapping_version

resolution_timestamp

mapping_status

identity_domain

relationship_type

lossiness_status

ambiguity_status
```

Coordinate-to-feature resolution events should also preserve:

```text
reference_build

coordinate_convention

feature_source

feature_source_version

annotation_release

overlap_or_relationship_method
```

Namespace resolution therefore becomes auditable and reproducible.

---

## Identity Relationship Graph

Namespace brokerage produces an identity relationship graph.

Examples include:

```text
Gene Symbol
        ↓
HGNC Identifier
        ↓
Ensembl Identifier
        ↓
NCBI Identifier
```

and

```text
Variant Coordinate
        ↓
Feature Interval
        ↓
Gene Locus
        ↓
Gene Identity
```

and

```text
Producer Assertion Identity
        ↓
Source Identity Set
        ↓
Coordinate / Feature / Gene Identity
```

The graph captures relationships.

It does not replace participating identities.

---

## Cross-Space Brokerage

VDB must support brokerage across identity spaces.

Examples include:

```text
variant coordinate
        ↔
gene locus interval

variant coordinate
        ↔
transcript interval

variant coordinate
        ↔
regulatory feature interval

gene identity
        ↔
gene locus interval

phenotype-gene evidence
        ↔
sample-variant evidence

producer assertion identity
        ↔
source identity set
```

Cross-space brokerage enables topology and convergence geometry without collapsing evidence into a single identity type.

This is essential for relating VAP coordinate-centered variant observations to GSC gene-centered semantic priors while preserving both evidence models.

---

## Namespace Uncertainty

Namespace uncertainty must remain visible.

Examples include:

```text
One-to-many mappings

Many-to-one mappings

Ambiguous mappings

Unresolved mappings

Version-dependent mappings

Reference-build-dependent mappings

Annotation-release-dependent mappings

Feature-overlap ambiguity
```

VDB must preserve uncertainty rather than conceal it.

Additive normalization enables ambiguity to remain detectable.

Unresolved coordinate, feature, or gene relationships are not evidence failure by default.

They are brokerage states.

---

## Noncoding and Unannotated Evidence Preservation

VDB must not require named gene membership for evidence preservation.

Noncoding, intergenic, regulatory, structural, and currently unannotated variants remain first-class coordinate identities.

A coordinate identity that lacks a present-day gene or feature relationship may still support future convergence geometry.

Preserving such identities protects future discovery, including poly-noncoding variant burden analysis and future annotation reinterpretation.

The absence of a gene mapping is therefore not a reason to discard, collapse, or downgrade the source coordinate identity.

---

## Overlay Identity Governance

Semantic overlays introduce additional namespace requirements.

Examples include:

```text
(gsc_release_id,
 phenotype,
 canonical_gene_id)
```

Overlay identities remain distinct from:

```text
Variant identities

Coordinate identities

Sample identities

Observation identities

Producer identities
```

Overlay persistence therefore requires independent identity governance.

When overlays are related to coordinate-centered evidence, VDB must preserve the cross-space brokerage path that connects the overlay identity to coordinate, feature, or gene identities.

---

## Persistence and Namespace Authority

Persistence domains consume namespace authority.

Persistence domains do not create namespace authority.

This distinction is important.

Namespace brokerage determines identity relationships.

Persistence domains determine evidence organization.

The two systems cooperate but remain independent.

---

## Discovery and Namespace Authority

Discovery consumes namespace authority through brokered identities and identity relationships.

The workflow is:

```text
TEP Arrival
        ↓
Discovery / Profiling
        ↓
Namespace-Bearing Identity Detection
        ↓
Namespace Brokerage
        ↓
Canonical and Source Identity Relationships
        ↓
Discovery Routing
        ↓
Persistence
```

Initial discovery determines what the artifact appears to contain.

Namespace brokerage determines how identities relate.

Discovery routing then uses brokered identity relationships to support deterministic persistence decisions.

This ordering ensures that discovery remains deterministic and identity-aware without becoming an identity-authority system.

---

## Relationship To Assertion Records

Assertion Records preserve producer assertions.

They should not require completed canonical identity resolution.

They must, however, preserve enough namespace-aware identity state to make later topology and geometry possible.

For namespace-bearing participants, Assertion Records should preserve:

```text
source identity

source namespace

identity kind

participant role

source identity set reference

resolution status

lossiness status

brokerage or bridge-readiness state when available
```

For coordinate-centered variant evidence, Assertion Records should preserve coordinate/reference-context identity or preserve references that make that identity recoverable.

For gene-centered evidence, Assertion Records should preserve gene identity, gene namespace, producer context, and bridge-readiness state.

If this substrate is absent from Assertion Records, later topology layers must not silently invent it.

---

## Relationship To Evidence Topology and Convergence Geometry

Evidence Topology organizes preserved assertions.

Convergence Geometry characterizes relationships that emerge from organized evidence.

Neither layer can safely recover identities that were not preserved.

Namespace brokerage must therefore provide topology with identity relationships such as:

```text
coordinate identity
        ↔
feature interval

feature interval
        ↔
gene identity

producer assertion identity
        ↔
source identity set

source identity
        ↔
canonical identity when governed
```

This enables convergence geometries such as:

```text
gene convergence

coordinate convergence

interval convergence

regulatory convergence

burden-window convergence

cross-producer convergence

noncoding convergence
```

Gene convergence is one valid geometry.

It is not the only valid geometry.

---

## Future Namespace Expansion

The model intentionally supports future namespace systems.

Examples include:

```text
Future RSP identifiers

Ontology identifiers

Protein identifiers

Pathway identifiers

Cell-state identifiers

Functional module identifiers

Regulatory annotation identifiers

Chromatin-domain identifiers

Burden-window identifiers

Future genome annotation systems
```

New namespace systems should integrate through brokerage rather than architectural redesign.

---

## Authority Boundaries

The ecosystem therefore recognizes the following authority model:

```text
Producer Repositories
        Own Meaning

TEP
        Owns Transport

Namespace Brokerage
        Owns Relationships

Discovery
        Consumes Relationships

Persistence
        Organizes Evidence

RDGP
        Consumes Evidence
```

This separation prevents authority drift and preserves explainability.

---

## Summary

VDB functions as the namespace brokerage authority of the repository ecosystem.

Producer repositories remain authoritative for biological meaning.

TEPs remain authoritative for transport.

Discovery remains authoritative for governance-driven routing.

Namespace brokerage provides the additive identity relationships that allow these systems to interoperate.

Canonical identities are brokerage artifacts rather than biological-truth artifacts.

The default namespace substrate for variant-derived evidence is coordinate/reference-context identity.

Gene namespace brokerage remains essential, but it is a routed specialization rather than the root identity model.

Feature and interval brokerage connect coordinate-centered evidence to genes, transcripts, regulatory elements, and future biological feature systems.

Producer brokerage preserves source-native repository identity spaces.

Through additive normalization, provenance-preserving resolution events, identity-space independence, and coordinate-first preservation, VDB enables interoperability without sacrificing semantic meaning, provenance integrity, noncoding evidence, or future interpretability.

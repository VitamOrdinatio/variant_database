# Namespace Resolution Engine Design

## Purpose

The namespace resolution engine defines how VDB relates heterogeneous biological identifiers without mutating source evidence.

VDB receives evidence from repositories that use different identity systems.

Examples include:

* coordinate and allele identifiers
* variant identifiers
* interval identifiers
* feature identifiers
* gene identifiers
* transcript identifiers
* phenotype identifiers
* sample identifiers
* release identifiers
* run identifiers
* artifact identifiers
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

The default namespace substrate for variant-derived evidence is coordinate/reference-context identity.

Gene identity is an essential routed specialization, but it is not the root brokerage model for VDB.

---

## Coordinate-First Brokerage Principle

VDB must preserve evidence across the full genome.

Therefore the namespace resolution engine must not require a named gene to preserve, broker, organize, or expose variant-derived evidence.

A variant may be biologically valid evidence even when it is:

```text
noncoding

intergenic

intronic

regulatory-adjacent

annotation-dependent

currently uninterpretable

not cleanly assigned to a named gene
```

The default brokerage route for variant-derived evidence is therefore:

```text
reference build
        +
contig / chromosome
        +
start / end
        +
reference allele
        +
alternate allele
        +
normalization state
        +
observation context
```

Gene brokerage is applied when evidence is gene-centered or when coordinate evidence can be related to governed gene or feature intervals.

Unmapped-to-gene does not mean unmapped-to-genome.

---

## Lifecycle Architectural Position

The namespace resolution engine is a governed brokerage function that may operate at multiple VDB lifecycle points.

Conceptually:

```text
TEP Transport
        ↓
Discovery / Profiling
        ↓
Validation
        ↓
Registration Substrate Construction
        ↓
Namespace Brokerage
        ↓
Assertion Record Construction
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Semantic Persistence Domains
        ↓
Query / Projection Surfaces
```

The engine may participate in:

```text
ingestion preflight

registration substrate construction

Assertion Record construction

Evidence Topology construction

projection and query-surface packaging
```

At every lifecycle point, the engine remains additive.

It must never mutate TEP payloads.

It must never overwrite source identities.

It must never silently collapse unresolved or ambiguous identities into exact canonical identities.

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

Resolution route selection is not interpretation.

For example, assigning a variant observation to coordinate brokerage means:

```text
this evidence carries coordinate-like identity
```

It does not mean:

```text
this variant is clinically meaningful
```

Likewise, relating a coordinate to a gene interval means:

```text
this coordinate overlaps or annotates to a governed feature interval
```

It does not mean:

```text
this variant explains disease through that gene
```

---

## Brokerage Route Model

The engine should route identity observations before applying route-specific brokerage.

Conceptually:

```text
incoming identity observation
        ↓
identity class detection
        ↓
brokerage route assignment
        ↓
route-specific preservation / resolution
        ↓
additive identity relationship records
```

Recommended v1 brokerage routes include:

```text
coordinate_brokerage

variant_brokerage

interval_brokerage

feature_brokerage

gene_brokerage

phenotype_brokerage

producer_brokerage

overlay_brokerage

transport_brokerage
```

Routing determines which identity-governance rules apply.

Routing does not discard identities assigned to other routes.

A single evidence object may participate in multiple routes.

For example, a VAP variant observation may participate in:

```text
coordinate_brokerage

variant_brokerage

observation_brokerage

feature_brokerage when annotation features are available

gene_brokerage when a governed gene relationship exists

producer_brokerage through VAP run and sample identities
```

---

## Input Identity Classes

The engine should support multiple identity classes.

Representative classes include:

```text
coordinate identifiers

allele identifiers

variant identifiers

variant observation identifiers

interval identifiers

feature identifiers

gene identifiers

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

For example, coordinate and variant identity may include:

```text
reference-build-qualified chromosome-position-ref-alt

VCF-style alleles

normalized allele representations

dbSNP identifiers

source-local variant identifiers

annotation-derived variant identifiers
```

Gene identity may include:

```text
HGNC ID

Ensembl Gene ID

NCBI Gene ID

gene symbol

source-specific aliases
```

Phenotype identity may include:

```text
HPO

OMIM

MONDO

source-local phenotype labels

repository-defined phenotype scopes
```

Producer identity may include:

```text
VAP run identifiers

VAP sample identifiers

GSC release identifiers

GSC phenotype scopes

GSC source identifiers

RSP run or contrast identifiers

TEP package identifiers

registration unit identifiers

corpus generation identifiers
```

---

## Source Identity Preservation

Every source identifier should remain preserved.

For each resolved or brokered identity, VDB should retain:

* source identifier
* source namespace
* source repository
* source artifact
* source package identity
* source field or column, when applicable
* source value
* source identity kind
* source participant role
* registration unit identity
* corpus generation identity, when applicable
* resolution or brokerage event

This allows future users to reconstruct how an identity entered VDB.

Source identity preservation applies even when no canonical identity is attached.

---

## Canonical Identity Assignment

Canonical identities provide stable routing anchors.

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

Canonical identities should be assigned only through explicit resolution events.

The engine should not silently infer canonical identity without preserving mapping evidence.

A canonical gene identity must not replace a coordinate identity.

A canonical feature identity must not replace a source variant observation.

Canonical identities are additive references, not destructive replacements.

---

## Resolution Events

Namespace resolution should be represented as an auditable event.

Each event should preserve:

```text
resolution_event_id

source_identifier

source_namespace

source_identity_kind

source_participant_role

target_identifier

target_namespace

canonical_identifier

brokerage_route

mapping_status

mapping_method

mapping_source

mapping_version

resolution_timestamp

confidence_or_quality_flag

ambiguity_state

lossiness_status
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

not_evaluated

bridge_available

bridge_required

bridge_missing

deferred_by_policy

source_identity_preserved
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
* coordinate systems differ across reference builds
* contig naming conventions differ across sources
* feature intervals differ across annotation releases
* source-local terms lack ontology equivalents

The engine should preserve ambiguity rather than conceal it.

Where ambiguity exists, downstream query surfaces should be able to filter or expose ambiguity state.

---

## Versioned Mapping Sources

Identity resolution depends on mapping resources.

Examples include:

```text
reference genome builds

contig naming conventions

variant normalization tools

annotation releases

HGNC reference tables

Ensembl releases

NCBI Gene mappings

HPO releases

ClinVar releases

VEP annotation versions

producer-supplied identifier maps
```

The engine should preserve mapping-source version information.

A resolution that was valid under one mapping release may differ under a later mapping release.

Historical reproducibility requires versioned resolution provenance.

---

## Coordinate And Variant Brokerage

Coordinate and variant brokerage is the default route for variant-derived evidence.

The engine should preserve coordinate identity using reference-context-qualified fields such as:

```text
reference_build

contig

start

end

reference_allele

alternate_allele

variant_type

coordinate_system

normalization_status

allele_representation

source_variant_identifier
```

The engine should distinguish:

```text
coordinate identity

variant entity

variant observation
```

A coordinate identity describes a reference-context location or allele representation.

A variant entity describes a normalized biological or representational variant entity.

A variant observation describes a sample-specific or run-specific observation of a variant.

For example:

```text
coordinate identity
        GRCh38 chromosome/start/end/ref/alt

variant entity
        normalized allele-level entity

variant observation
        sample-specific observation from VAP run X in sample Y
```

These identities are related, but they must not collapse into one another.

Coordinate brokerage allows noncoding and currently unannotated variants to remain first-class evidence even when no gene relationship is currently known.

---

## Interval And Feature Brokerage

Interval and feature brokerage relates coordinates to governed biological or annotation-derived regions.

Examples include:

```text
gene locus intervals

transcript intervals

exon intervals

intron intervals

UTR intervals

splice-region intervals

regulatory intervals

promoter intervals

enhancer intervals

conserved elements

repeat regions

burden windows

future feature classes
```

Feature brokerage should preserve:

```text
feature_identifier

feature_namespace

feature_type

reference_build

contig

start

end

strand, when applicable

annotation_source

annotation_version

feature_relationship_type
```

Feature brokerage relates coordinates to annotated biological regions without making those regions the primary identity substrate for variant-derived evidence.

Example:

```text
VAP coordinate-level variant observation
        ↓ overlaps / annotates_to
POLG gene locus interval
        ↓ attaches_to
POLG gene identity
        ↓ connects_to
GSC phenotype-gene semantic prior
```

This chain enables cross-space convergence while preserving the difference between coordinate identity, feature interval identity, gene identity, and semantic-prior identity.

---

## Gene Namespace Brokerage

Gene brokerage is a primary routed specialization.

It is not the default route for all VDB evidence.

VDB may receive gene evidence from:

* GSC
* VAP annotations
* future RSP
* RDGP-facing query surfaces
* external metadata resources

These sources may use different identifiers.

The engine should support additive relationships among:

```text
HGNC ID

Ensembl Gene ID

NCBI Gene ID

gene symbol

source-local gene identifier

alias symbol
```

Gene brokerage should preserve the distinction between:

```text
gene identity
```

and

```text
gene locus / feature interval
```

A gene identifier such as an HGNC ID, Ensembl Gene ID, NCBI Gene ID, or gene symbol is not the same object as a reference-build-specific genomic interval for that gene model.

Gene brokerage may use governed producer-supplied identifier maps or adapter-resolved identity fields.

For example, GSC may provide build-time identifier maps derived from MyGene.info or adapter-resolved identities emitted by producer-specific adapters.

VDB should consume those preserved identity products and their provenance.

VDB should not require runtime external service calls to broker identities during deterministic ingestion.

---

## Phenotype Namespace Brokerage

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

## Producer Identity Brokerage

Producer identity brokerage preserves source-native identity spaces that participate in evidence meaning.

Examples include:

```text
VAP run IDs

VAP sample IDs

VAP source-local variant IDs

GSC release IDs

GSC phenotype scopes

GSC source IDs

GSC semantic channels

GSC evidence-source identifiers

RSP run or contrast identifiers

TEP IDs

artifact IDs

registration unit IDs

corpus generation IDs
```

Producer identities are not optional metadata.

They may be part of the identity of the evidence object itself.

For example:

```text
(gsc_release_id, phenotype, gene_id)
```

must not be collapsed into:

```text
gene_id
```

Producer brokerage ensures that source-native evidence identity remains reconstructable after cross-repository relationship building.

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

coordinate evidence
        ↔
feature interval evidence

transcript evidence
        ↔
gene evidence

producer-local evidence
        ↔
canonical reference evidence
```

Identity-space bridging should remain explicit and explainable.

The engine should create relationships that support bridging while preserving the identity spaces involved.

Cross-space bridging should record bridge status, bridge source, bridge method, and lossiness state.

---

## Relationship To Evidence Topology And Convergence Geometry

Evidence Topology consumes brokered identity relationships.

Convergence Geometry characterizes structures that emerge from the topology.

If namespace brokerage collapses coordinate evidence into gene identity too early, VDB risks losing noncoding and currently unannotated evidence.

If namespace brokerage fails to relate coordinate evidence to governed feature or gene intervals when available, VDB risks missing true cross-producer convergence.

The namespace resolution engine therefore supports topology and geometry by preserving multiple brokerable axes:

```text
coordinate-centered evidence

variant-centered evidence

interval-centered evidence

feature-centered evidence

gene-centered evidence

phenotype-centered evidence

producer-centered evidence
```

Gene convergence is one possible geometry.

It is not the only geometry.

---

## Relationship To RDGP Query Surfaces

RDGP may consume gene-level evidence surfaces.

VDB may need to aggregate variant-centric evidence into:

```text
(sample_id, gene_id)
```

or related RDGP-facing records.

Namespace resolution supports this transformation by enabling coordinate-to-feature, feature-to-gene, and source-gene-to-canonical-gene relationships.

However, namespace resolution does not perform RDGP reasoning.

It only provides identity relationships required for query-surface construction.

RDGP-facing surfaces should expose source identity lineage, bridge status, mapping provenance, and ambiguity state rather than hiding them.

---

## Relationship To Discovery

Discovery answers:

```text
What does this artifact contain?
```

Namespace resolution answers:

```text
How do the artifact's identities relate to known identity systems?
```

The discovery engine may detect identifier-like fields.

The namespace resolution engine resolves or brokers those identifiers.

Discovery routing may then use brokered identity relationships to support deterministic persistence decisions.

Discovery must not become a hidden identity authority.

---

## Relationship To TEPs

TEPs preserve producer-owned evidence states.

The namespace resolution engine must not mutate TEP payloads.

When resolving identities contained in a TEP, VDB should create additive resolution records outside the immutable payload.

The TEP remains unchanged.

The brokerage layer records how VDB interpreted identity relationships for persistence, topology, geometry, and query exposure.

---

## Relationship To Semantic Persistence Domains

Semantic persistence domains consume namespace-resolution outputs.

Examples:

```text
Variant evidence domain
        uses coordinate / variant identity and source variant identities

Feature evidence domain
        uses interval / feature identity and source feature identities

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

* source identity records
* coordinate identity records
* variant identity records
* variant observation identity records
* interval identity records
* feature identity records
* gene identity records
* producer identity records
* canonical identity records
* identity relationship records
* coordinate-to-feature relationship records
* feature-to-gene relationship records
* resolution event records
* brokerage route records
* bridge-readiness records
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
* gene-centric collapse of coordinate evidence
* noncoding evidence loss
* unannotated variant discard
* coordinate-build ambiguity
* contig naming ambiguity
* variant observation collapse into variant entity
* feature interval treated as gene identity
* gene identity treated as gene locus without interval provenance
* gene symbol treated as exact identity without bridge evidence
* coordinate-to-gene relationship asserted without annotation provenance

These are architectural failures, not minor implementation issues.

---

## v1 Scope Recommendation

Recommended v1 scope:

* coordinate/reference-context brokerage for variant-derived evidence
* variant entity versus variant observation preservation
* source identity preservation
* producer identity preservation
* gene brokerage as a routed specialization
* interval and feature relationship readiness
* explicit bridge-readiness status
* mapping-source/version preservation
* unresolved and ambiguous state handling
* TEP-safe additive resolution records
* support for GSC overlay attachment without collapsing release identity
* support for VAP coordinate-to-gene routing when governed feature intervals exist
* support for RDGP-facing surfaces that expose bridge status and identity lineage

Defer to later releases:

* full external regulatory-feature atlas lifecycle
* automated coordinate liftover
* large-scale transcript-version reconciliation
* full ontology resolution lifecycle
* complex phenotype hierarchy reasoning
* graph-based identity reasoning
* protein and pathway namespace brokerage
* automated conflict adjudication
* ML-driven identity inference
* full value-level expansion from every source identity set

---

## Summary

The namespace resolution engine is VDB's design mechanism for additive identity brokerage.

It relates heterogeneous source identifiers to canonical or brokered identities while preserving source identity, provenance, ambiguity, mapping context, and historical reproducibility.

Its default route for variant-derived evidence is coordinate/reference-context brokerage.

Gene brokerage remains essential, but it is a routed specialization rather than the root brokerage model.

The engine does not own biological meaning.

It does not mutate TEP payloads.

It does not perform downstream reasoning.

It creates the identity relationships that allow discovery, semantic persistence, Evidence Topology, Convergence Geometry, overlay attachment, and query surfaces to operate safely across repository boundaries.

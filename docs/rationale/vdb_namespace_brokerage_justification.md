# VDB Namespace Brokerage Justification

## Purpose

This document explains why the Variant Database (VDB) implements namespace brokerage rather than namespace replacement.

The purpose of this document is to justify the identity management philosophy of the repository and explain why identity preservation is treated as a first-class architectural requirement.

This document does not define namespace resolution algorithms.

This document explains why namespace brokerage exists.

---

# Executive Summary

Modern biological evidence originates from many independent systems.

Each system introduces its own identifiers, naming conventions, authority structures, coordinate systems, feature definitions, and identity assumptions.

Examples include:

```text
Ensembl

HGNC

NCBI

ClinVar

dbSNP

VAP

GSC

RSP

RDGP
```

These systems are not incorrect.

They are optimized for different purposes.

The purpose of VDB is therefore not to eliminate those identities.

The purpose of VDB is to preserve and relate them.

VDB must support gene-level interoperability, but gene identity is not the root identity substrate for VDB.

For variant-derived evidence, the default identity substrate is genomic coordinate and reference-context identity.

Gene brokerage is essential, but it is a routed specialization applied when evidence is gene-centered or when coordinate evidence can be related to gene, transcript, regulatory, or other feature intervals.

This distinction protects full-genome evidence preservation, noncoding discovery, future reinterpretation, and valid convergence geometry.

---

# The Traditional Approach

Many systems attempt to solve identity complexity through normalization.

Conceptually:

```text
Source Identity
        ↓
Normalization
        ↓
Canonical Identity
        ↓
Discard Original Identity
```

This approach simplifies implementation.

However, it introduces important risks.

Examples include:

```text
loss of provenance

loss of historical context

loss of authority information

loss of ambiguity

loss of future reinterpretation capability

loss of currently unnamed or poorly annotated biology
```

VDB intentionally rejects this approach.

---

# Identity Is Evidence

One of the central assumptions of VDB is:

```text
Identity is evidence.
```

Identifiers are not merely implementation details.

Identifiers encode:

```text
authority

historical context

producer intent

biological context

semantic meaning
```

Discarding identities therefore discards information.

This principle applies not only to named biological identifiers, such as gene symbols or ontology terms, but also to coordinate identities, interval identities, source-local identifiers, observation identities, and producer-scoped identities.

A genomic coordinate can be an evidence-bearing identity even when no current biological name is attached to it.

---

# Producer Repositories Are Authorities

Each producer repository owns identities within its own domain.

Examples:

```text
VAP
    run identifiers

VAP
    sample-level evidence identities

VAP
    variant observations and coordinate-level evidence

GSC
    semantic prior identities

GSC
    release identities

RDGP
    reasoning identities

RSP
    transcriptomic evidence identities
```

Producer-generated identities are authoritative within producer-defined contexts.

VDB should not overwrite those identities.

---

# Authority Is Distributed

The ecosystem intentionally embraces distributed authority.

Examples:

```text
HGNC
    symbol authority

Ensembl
    gene and transcript identifier authority

Reference genome resources
    coordinate and assembly context authority

Annotation resources
    feature interval and transcript model authority

ClinVar
    clinical interpretation authority

VAP
    observational evidence authority

GSC
    semantic prior authority
```

No single system owns all biological identities.

VDB therefore acts as a broker among authorities rather than attempting to become the authority itself.

---

# Why Brokerage Exists

Namespace brokerage exists because interoperability requires relationships.

Interoperability does not require identity replacement.

Consider:

```text
SCN1A

ENSG00000144285

NCBIGene:6323
```

These identifiers are related.

They are not identical.

Likewise, a genomic coordinate and a gene identifier may be related without belonging to the same identity class.

For example:

```text
GRCh38 chromosome/start/end/ref/alt
        ↓
variant or interval identity
        ↓
feature overlap relationship
        ↓
gene locus or transcript feature
        ↓
gene identity
```

The goal is therefore:

```text
connect identities

without erasing identities
```

Namespace brokerage achieves this objective.

---

# Why Gene-Centric Brokerage Is Insufficient

Gene namespace brokerage is necessary but insufficient for VDB.

A gene-centric brokerage model protects known gene-level interoperability, but it cannot serve as the default identity model for a variant database.

Variant-derived evidence exists across the full genome.

Many variant observations are:

```text
coding

intronic

intergenic

regulatory-adjacent

splice-region-associated

UTR-associated

annotation-dependent

currently uninterpretable

not cleanly assigned to a known gene
```

If VDB treats named genes as the primary identity substrate, then evidence topology and convergence geometry become biased toward already named and currently annotated biology.

That would undermine VAP's preservation mission and VDB's discovery mission.

VDB must not collapse full-genome evidence into the subset of evidence that current gene annotation can name.

The critical principle is:

```text
Unmapped-to-gene does not mean unmapped-to-genome.
```

A noncoding or currently unannotated variant can still be preserved as a valid coordinate identity.

That coordinate identity may become important later when new regulatory annotations, burden models, chromatin maps, disease mechanisms, or feature definitions become available.

---

# Coordinate Identity Protects Future Discovery

Coordinate and reference-context identity provide the default full-genome substrate for variant-derived evidence.

A coordinate identity may include:

```text
reference build

contig or chromosome

start coordinate

end coordinate

reference allele

alternate allele

variant type

normalization status

source representation

observation context
```

This substrate does not require present-day biological naming to preserve evidence.

A variant can remain evidence even when no current gene, transcript, regulatory feature, ontology term, or disease mechanism is known.

Coordinate-first brokerage protects future discovery opportunities such as:

```text
poly-noncoding variant burden

regulatory-region convergence

variant-cluster convergence

burden windows

chromatin-domain relationships

future enhancer or promoter annotations

future conserved-element annotations

future noncoding disease mechanisms
```

If coordinate identity is lost or subordinated to gene identity too early, those future discoveries may become impossible to reconstruct.

---

# Gene Brokerage Remains Essential But Not Primary

Gene brokerage remains essential for cross-repository interoperability.

Examples include:

```text
Ensembl gene identifiers

NCBI Gene identifiers

HGNC identifiers

gene symbols

aliases

producer-specific gene identifiers
```

GSC is often gene-centered because it produces phenotype-scoped semantic priors over genes.

RSP may produce gene, transcript, or module-centered expression evidence.

RDGP-facing surfaces may often require sample-gene or phenotype-gene views.

VDB must therefore broker gene namespaces carefully.

However, gene brokerage is a routed specialization rather than the root brokerage model.

For VAP-derived variant evidence, the default identity substrate is coordinate or variant identity.

Gene identity becomes relevant when coordinate evidence can be related to a gene locus, transcript model, regulatory neighborhood, or other feature relationship.

This prevents VDB from treating gene names as mandatory for evidence preservation.

---

# Feature And Interval Brokerage Enable Cross-Space Convergence

Evidence convergence often requires relationships across identity spaces.

For example, VAP may preserve a coordinate-level variant observation while GSC preserves a phenotype-gene semantic prior.

A valid convergence path may require:

```text
coordinate identity
        ↓
variant or interval identity
        ↓
gene locus, transcript, or feature interval
        ↓
gene identity
        ↓
phenotype-gene semantic prior identity
```

This path is not a simple identifier replacement.

It is a governed chain of relationships among coordinate, interval, feature, gene, phenotype, and producer identities.

Feature and interval brokerage allow VDB to support both:

```text
gene-aware convergence
```

and

```text
noncoding or feature-centered convergence
```

without collapsing one into the other.

This protects VDB from two failure modes:

```text
false negative
    missing convergence because one producer is coordinate-centered and another is gene-centered

false positive
    overclaiming convergence through weak, ambiguous, or unsupported identity matches
```

---

# The VDB Brokerage Model

Conceptually:

```text
Source Identity
        ↓
Namespace Brokerage
        ↓
Relationship Layer
        ↓
Canonical Reference Layer
        ↓
Discovery / Topology / Persistence Consumers
```

The brokerage layer creates relationships.

The brokerage layer does not destroy source identity.

VDB brokerage includes multiple routed classes:

```text
Default Coordinate Brokerage
    genomic coordinate, allele, interval, and reference-context identity

Feature Brokerage
    gene loci, transcript loci, exons, introns, regulatory features,
    conserved elements, burden windows, and future feature classes

Gene Brokerage
    Ensembl, NCBI Gene, HGNC, gene symbols, aliases, and source gene IDs

Producer Brokerage
    source-native producer identities, release identities, run identities,
    artifact identities, package identities, and source-local identifiers
```

These brokerage classes cooperate.

They should not be collapsed into a single identity class.

---

# Why Canonical Identity Still Exists

VDB may assign canonical identities.

Canonical identities provide:

```text
stable references

cross-repository linkage

query simplification

persistence stability
```

However:

```text
canonical identity
    ≠
source identity
```

Canonical identities exist to facilitate interoperability.

They do not invalidate original identities.

VDB may need multiple canonical brokerage anchors, including:

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

No single canonical identity class should be treated as sufficient for all evidence.

In particular:

```text
canonical_gene_id is not the default canonical identity for variant-derived evidence.
```

---

# Unresolved Identities Are Valuable

Many systems treat unresolved identifiers as failures.

VDB intentionally rejects this assumption.

Examples include:

```text
novel variants

unannotated noncoding variants

novel genes

future evidence classes

emerging ontologies

repository-specific identifiers
```

An unresolved identity may still represent valid evidence.

Therefore:

```text
unresolved
    ≠
invalid
```

Preservation of unresolved identities is essential for future-proofing.

A variant may be unresolved with respect to gene or feature annotation while remaining fully preserved with respect to coordinate identity.

---

# Ambiguity Is Information

Ambiguous mappings are often treated as implementation problems.

VDB treats ambiguity as evidence.

Examples include:

```text
historical aliases

deprecated identifiers

multiple plausible mappings

ontology transitions

version-dependent coordinate or feature mappings
```

These conditions communicate uncertainty.

Removing ambiguity destroys information.

Therefore:

```text
ambiguity should be preserved

not hidden
```

whenever possible.

---

# Future Discovery Depends Upon Identity Preservation

Many future discoveries will emerge from relationships that are not obvious today.

Examples may include:

```text
new phenotype relationships

new gene relationships

new regulatory relationships

new noncoding burden relationships

new coordinate-cluster relationships

new feature classes

new evidence classes
```

If identities are discarded during ingestion, those future relationships may become impossible to reconstruct.

Identity preservation therefore protects future discovery opportunities.

Full-genome identity preservation requires that noncoding, intergenic, regulatory, and currently unannotated coordinate identities remain first-class evidence objects.

---

# Future Reinterpretation Depends Upon Identity Preservation

Scientific understanding evolves continuously.

New resources may eventually resolve identities that are currently:

```text
unknown

ambiguous

partially resolved

deferred

unannotated

not yet feature-linked
```

Preserving original identities allows future systems to revisit those questions.

Replacing identities prematurely may prevent reinterpretation.

Coordinate-first brokerage ensures that future reinterpretation can revisit both named and unnamed genomic evidence.

---

# Clinical Motivation

Clinical interpretation often occurs over long time horizons.

A future clinician may need to understand:

```text
what identifier was originally observed

what coordinate context was originally observed

what authority assigned it

what mappings existed at the time

what mappings exist now

what feature annotations were available at the time

what feature annotations emerged later
```

Namespace brokerage preserves this history.

Identity replacement destroys it.

---

# Relationship To TEPs

Transitional Evidence Products (TEPs) preserve source identities during transport.

Examples include:

```text
sample identifiers

gene identifiers

variant identifiers

coordinate identifiers

feature identifiers

run identifiers

release identifiers

package identifiers
```

Namespace brokerage continues that preservation philosophy after ingestion.

TEPs preserve identities during transport.

VDB preserves identities during persistence, topology construction, convergence geometry, and query-surface exposure.

These are complementary responsibilities.

---

# Relationship To Persistence

Persistence without identity preservation is incomplete.

Evidence that cannot be related back to its source identity loses context.

Namespace brokerage therefore serves as a critical component of the persistence mission.

Persistence preserves evidence.

Brokerage preserves relationships among evidence identities.

Coordinate-first brokerage ensures that persistence can preserve evidence across the full genome rather than only across currently named genes.

---

# Relationship To Evidence Topology And Convergence Geometry

Evidence Topology organizes preserved evidence relationships.

Convergence Geometry characterizes the structures that emerge from those relationships.

Both depend on preserved identity substrate.

If VDB collapses coordinate evidence into gene-only identity too early, convergence geometry may lose noncoding, interval, regulatory, or currently unannotated signals.

If VDB fails to broker gene and feature relationships when they are available, convergence geometry may miss valid cross-producer convergence.

The correct balance is:

```text
preserve coordinate identity by default

broker feature and gene relationships when governed evidence supports them

preserve ambiguity and unresolved states when brokerage is incomplete
```

This enables present-day gene-aware convergence while protecting future noncoding and feature-centered discovery.

---

# Tradeoffs

Namespace brokerage introduces complexity.

Examples include:

```text
identity lineage tracking

authority tracking

mapping maintenance

coordinate normalization governance

feature interval provenance

ambiguity management

resolution provenance
```

These costs are accepted intentionally.

The repository prioritizes long-term interpretability over short-term simplification.

---

# Why VDB Is Not A Namespace Authority

VDB stores and relates evidence.

VDB does not define biological nomenclature.

VDB does not define external authority systems.

VDB does not own reference genome assemblies, gene nomenclature, transcript models, or feature annotation authorities.

Instead:

```text
VDB preserves

VDB relates

VDB brokers
```

Authority remains with authoritative sources.

---

# Success Criteria

The namespace brokerage mission succeeds when future users can:

```text
recover original identifiers

recover coordinate and reference context

recover authority context

understand identity lineage

trace mappings through time

preserve unresolved identities

preserve ambiguous identities

preserve noncoding and currently unannotated evidence

perform cross-repository discovery

perform coordinate-aware, feature-aware, gene-aware, and producer-aware convergence analysis
```

without losing source meaning.

---

# Conclusion

Namespace brokerage exists because biological evidence emerges from many independent identity systems.

Rather than replacing those systems, VDB preserves and relates them.

This approach protects provenance, authority, ambiguity, future reinterpretation, and future discovery.

VDB therefore treats identities as evidence-bearing objects rather than disposable implementation details.

Coordinate-first brokerage is necessary because VDB must preserve evidence across the full genome, not only across the subset of biology that is currently gene-named or annotation-resolved.

Gene brokerage remains essential, but it is a routed specialization rather than the root model.

Feature and interval brokerage allow coordinate evidence to connect to named biological structures when governed relationships exist.

Producer brokerage preserves source-native evidence context.

The mission of namespace brokerage is simple:

```text
Preserve identities.

Relate identities.

Never erase identities.
```

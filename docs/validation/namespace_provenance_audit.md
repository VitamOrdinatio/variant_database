# Namespace Provenance Audit

## Purpose

This document defines the operational audit protocol for tracing namespace-bearing identity substrate through the VDB lifecycle.

It exists to answer a specific question:

```text
For each identity-bearing substrate required by VDB, what is the earliest stage
where it should appear, and does it survive through later phases without being
collapsed, dropped, or misclassified?
```

The namespace provenance audit is not a namespace-resolution algorithm.

The namespace provenance audit is not a mapping service.

The namespace provenance audit is not a value-expansion procedure.

The audit is a validation runbook for locating provenance breaks before downstream namespace hardening, Evidence Topology mediation, Convergence Geometry construction, or consumer-surface projection proceeds.

---

## Relationship To Namespace Validation

This document complements:

```text
docs/validation/namespace_resolution_validation.md
```

The validation document defines doctrine:

```text
Resolution is optional.

Preservation is mandatory.
```

This audit document defines how VDB proves that doctrine across the actual lifecycle.

Conceptually:

```text
namespace_resolution_validation.md
        ↓
Defines valid preservation and anti-collapse rules

namespace_provenance_audit.md
        ↓
Defines how to inspect the pipeline and locate earliest provenance breaks
```

The audit should therefore be treated as an operational validation contract.

It is a runbook for determining whether VDB has preserved enough identity substrate for future brokerage, topology, geometry, projection, and reinterpretation.

---

## Relationship To Namespace Governance

This document is governed by the following namespace documents:

```text
docs/architecture/namespace_authority_model.md

docs/rationale/vdb_namespace_brokerage_justification.md

docs/design/namespace_resolution_engine_design.md

docs/validation/namespace_resolution_validation.md
```

The authority model establishes that VDB owns namespace brokerage authority while producers retain semantic authority.

The rationale document explains why coordinate-first brokerage is necessary for full-genome preservation and future noncoding discovery.

The design document defines coordinate-first routed brokerage.

The validation document defines preservation, anti-collapse, and severity doctrine.

This document converts those principles into a stage-by-stage audit protocol.

---

## Core Audit Principle

Late-stage namespace failures must be traced to the earliest provenance break before any patch is applied.

A failure observed in Evidence Topology, Convergence Geometry, query surfaces, or RDGP-facing projections does not automatically mean that the current layer is the correct patch site.

The audit must ask:

```text
Where did the required identity substrate originate?

Where should it first have been preserved?

Where was it transformed, summarized, indexed, or projected?

Where did the provenance chain break?
```

Only after the earliest break is located should VDB patch the implementation, contract, schema, or validation layer.

This principle protects VDB's emergent-property architecture.

Convergence Geometry and downstream reasoning can only emerge safely when the lower-level identity constituents are correctly placed, preserved, and propagated.

---

## Audit Scope

The namespace provenance audit covers identity-bearing substrate from TEP arrival through Phase 4.4 Evidence Topology Step 7.

The audit stages are:

```text
TEP arrival

Phase 0
    intake / contract preflight

Phase 1
    artifact registration

Phase 2
    registration substrate

Phase 3
    ingestion finalization

Phase 4.1
    registration units

Phase 4.2
    corpus generation

Phase 4.3
    assertion records

Phase 4.4 through Step 7
    Evidence Topology construction and expansion-handle preservation
```

The audit does not require full canonical resolution at every stage.

The audit requires preservation, traceability, route classification, and explicit uncertainty.

---

## Audit Objectives

The audit must determine whether VDB can demonstrate that:

```text
source identities are preserved

source namespaces are preserved

identity route class is explicit or inferable

coordinate/reference-context identities remain first-class for VAP-derived evidence

gene identities remain first-class for GSC-derived evidence

feature relationships remain distinct from identity replacement

producer-scoped identities remain scoped

source identity handles survive compact representation

lossiness status remains visible

resolution status remains visible

future namespace brokerage remains possible
```

The audit must not treat unresolved identity as failure when source identity and provenance are preserved.

The audit must treat missing source identity, missing namespace, hidden collapse, or irrecoverable provenance loss as validation failures.

---

## Audit Lanes

The audit is organized into four identity brokerage lanes.

Each lane protects a different substrate required for future topology, geometry, projection, and interpretation.

---

## Lane 1 — Default Coordinate Brokerage

Default Coordinate Brokerage is the primary substrate for variant-derived evidence.

This lane protects full-genome preservation.

VDB must not require a named gene, transcript, regulatory feature, or ontology term for a variant-derived evidence element to remain valid.

Minimum expected substrate includes:

```text
reference_build

contig or chromosome

position or start/end

reference allele when applicable

alternate allele when applicable

variant representation

variant type when available

coordinate normalization status when available

sample or observation context

run or execution context

source-local variant identifier when available

source artifact reference

producer identity
```

This lane protects evidence such as:

```text
coding variants

intronic variants

intergenic variants

regulatory-adjacent variants

currently unannotated variants

burden-window candidates

future noncoding discovery substrate
```

Validation concern:

```text
Unmapped-to-gene does not mean unmapped-to-genome.
```

Critical failures include:

```text
coordinate identity lost

variant evidence preserved only as a gene name

noncoding variant discarded because no gene mapping exists

reference build missing for coordinate identity

variant observation collapsed into global variant entity without provenance
```

---

## Lane 2 — Feature Brokerage

Feature Brokerage relates coordinate identities to annotated biological regions without replacing coordinate identity.

Feature relationships may include:

```text
gene locus overlap

transcript overlap

exon / intron / UTR context

splice-region context

regulatory feature overlap

conserved element overlap

burden interval membership

future feature class membership
```

Minimum expected substrate includes:

```text
feature identifier when available

feature namespace

feature interval or feature reference

annotation source

annotation version or release when available

relationship type

relationship provenance

lossiness status

ambiguity status
```

Feature Brokerage supports relationships such as:

```text
coordinate identity
        overlaps
feature interval

feature interval
        attaches_to
gene identity
```

Feature Brokerage must not collapse feature relationships into identity replacement.

For example:

```text
variant coordinate overlaps POLG gene locus
```

is not the same as:

```text
variant identity equals POLG
```

Critical failures include:

```text
feature interval treated as gene identity

coordinate-to-gene relationship asserted without annotation provenance

feature annotation used to replace coordinate identity

nearest-gene or overlap relationship treated as exact causal interpretation

feature provenance lost
```

---

## Lane 3 — Gene Brokerage

Gene Brokerage is a routed specialization for gene-centered or gene-related evidence.

Gene Brokerage remains essential for GSC, future RSP, RDGP-facing gene surfaces, and coordinate-to-gene bridging.

Gene Brokerage is not the root identity model for all VDB evidence.

Minimum expected substrate includes:

```text
source_gene_id

source_gene_namespace

gene_symbol when available

Ensembl gene identifier when available

NCBI / Entrez gene identifier when available

HGNC identifier when available

alias or historical symbol when available

identifier map or adapter-resolution provenance when available

phenotype scope for GSC evidence

release identity for GSC evidence

source evidence provenance
```

Examples of gene-related producer substrates include:

```text
GSC phenotype-gene semantic priors

GSC source-specific gene identities

GSC identifier-map-resolved identities

adapter-resolved MitoCarta identities

future RSP gene or transcript identities

RDGP-facing gene-level surfaces
```

Gene Brokerage should support governed relationships among:

```text
Ensembl Gene

NCBI Gene

HGNC ID

gene symbol

alias

source-local gene identifier
```

Critical failures include:

```text
gene symbol treated as exact canonical identity without provenance

NCBI-to-Ensembl equivalence asserted without bridge evidence

GSC release identity lost from phenotype-gene overlay identity

phenotype context lost from semantic prior identity

gene namespace missing when gene identity is present
```

---

## Lane 4 — Producer Brokerage

Producer Brokerage preserves identities that are meaningful within producer-defined contexts.

These identities are not optional metadata.

They participate in evidence identity.

Minimum expected substrate includes:

```text
TEP identifier

producer identifier

source package identifier

artifact identifier

run identifier

sample identifier

release identifier

phenotype scope

source ID

semantic channel

registration unit identifier

corpus generation identifier

source assertion identifier

source identity set identifier

source table reference

source field or column reference
```

Examples include:

```text
VAP run/sample/variant identities

GSC release/phenotype/gene identities

GSC source-specific evidence identities

future RSP expression/module identities

RDGP reasoning identities
```

Producer-scoped identities must remain scoped unless an explicit brokerage event creates a governed relationship.

Critical failures include:

```text
producer scope lost

release identity treated as optional metadata

sample identity detached from variant observation

source assertion detached from source table reference

producer-local identifier treated as globally canonical without brokerage
```

---

## Stage Audit Model

Each audit stage should answer three questions:

```text
What identity-bearing substrate should exist at this stage?

What identity-bearing substrate is observed at this stage?

Can later-stage identity handles be traced back to this stage?
```

The audit should record whether identity substrate is:

```text
present

absent

deferred

not_applicable

inferable_but_not_explicit

present_with_lossiness

present_with_ambiguity

present_but_unresolved
```

---

## Stage A — TEP Arrival

TEP arrival establishes the incoming evidence substrate.

Audit questions:

```text
Does the TEP declare producer identity?

Does the TEP declare payload artifacts?

Does the TEP expose identity-bearing fields or tables?

Does the TEP preserve source-native identifiers?

Does the TEP declare source namespaces when available?

Does the TEP expose coordinate, variant, gene, feature, phenotype, sample,
release, run, and artifact identity lanes when applicable?

Does the TEP reference identifier maps, annotation products, or bridge artifacts
when applicable?
```

Expected VAP-oriented checks:

```text
variant coordinate fields

sample identifiers

run identifiers

source variant identifiers

gene annotation fields when available

transcript or consequence fields when available

reference build or annotation metadata when available
```

Expected GSC-oriented checks:

```text
gene_id

gene_namespace

gene_symbol when available

Ensembl / NCBI / HGNC-related identifiers when available

phenotype scope

release identity

source evidence provenance

identifier-map or adapter-resolution provenance when available
```

Failure at this stage may indicate a producer TEP contract gap.

---

## Stage B — Phase 0 Intake / Contract Preflight

Phase 0 determines whether VDB can ingest the TEP safely.

Audit questions:

```text
Can VDB identify which artifacts contain identities?

Can VDB classify identity-bearing artifacts by brokerage route?

Can missing namespace declarations be flagged?

Can unresolved-but-preserved states pass preflight?

Are source identity absence and namespace absence distinguished?
```

Expected audit outcome:

```text
identity-bearing artifacts detected

missing source identity flagged as error or critical

missing canonical identity not treated as failure by default

unresolved state allowed when source identity survives
```

---

## Stage C — Phase 1 Artifact Registration

Phase 1 registers evidence artifacts as VDB-addressable units.

Audit questions:

```text
Are identity-bearing artifacts registered?

Are identifier-map or bridge artifacts registered?

Are source artifact IDs preserved?

Are artifact roles preserved?

Are checksums, paths, and source package relationships preserved?

Can downstream identity records trace back to registered artifacts?
```

Expected audit outcome:

```text
source artifact provenance preserved

identity-bearing artifact roles visible

bridge or identifier-map artifacts preserved when present
```

---

## Stage D — Phase 2 Registration Substrate

Phase 2 preserves source evidence in registration substrate.

Audit questions:

```text
Are source identity tables present?

Are source identity sets declared?

Are coordinate fields preserved where applicable?

Are feature fields or annotation references preserved where applicable?

Are gene fields preserved where applicable?

Are producer IDs preserved?

Are source table references preserved?

Are source identity counts preserved?

Are lossiness and resolution states visible?
```

Expected audit outcome:

```text
source identity substrate available by reference

identity-bearing source tables reconstructable

coordinate, feature, gene, and producer lanes preserved or explicitly deferred
```

This stage is a major provenance checkpoint.

If Phase 2 loses identity substrate, later phases cannot safely reconstruct it.

---

## Stage E — Phase 3 Ingestion Finalization

Phase 3 finalizes registration outputs and prepares later Phase 4 operations.

Audit questions:

```text
Do registration outputs preserve identity_kind?

Do registration outputs preserve participant_role?

Do registration outputs preserve source_namespace?

Do registration outputs preserve source_identity_count?

Do registration outputs preserve source identity table references?

Do registration outputs preserve resolution status?

Do registration outputs preserve lossiness status?

Do registration outputs preserve producer and registration-unit context?
```

Expected audit outcome:

```text
identity handles finalized

namespace state visible

lossiness explicit

resolution state explicit

registration context preserved
```

This stage should prevent silent identity loss before Assertion Records.

---

## Stage F — Phase 4.1 Registration Units

Registration Units define bounded units of registered evidence.

Audit questions:

```text
Does each Registration Unit preserve producer identity?

Does each Registration Unit preserve input TEP or artifact linkage?

Does each Registration Unit expose whether coordinate, feature, gene, or
producer identity substrate exists?

Does each Registration Unit preserve source references to identity-bearing
artifacts?

Does each Registration Unit preserve bridge-readiness or unresolved states when
available?
```

Expected audit outcome:

```text
registration unit identity preserved

identity-bearing substrate membership preserved

unit-level namespace readiness visible or reconstructable
```

A Registration Unit may summarize identity substrate, but it must not sever traceability to the underlying source identity material.

---

## Stage G — Phase 4.2 Corpus Generation

Corpus Generation selects a bounded evidence corpus.

Audit questions:

```text
Does corpus selection preserve namespace-bearing unit membership?

Does corpus selection preserve identity route summaries?

Does corpus selection preserve bridge artifact references when present?

Does corpus selection preserve source identity set references?

Does corpus selection include evidence while accidentally excluding identity
substrate needed for brokerage?
```

Expected audit outcome:

```text
selected corpus remains identity-complete by reference

identity-bearing artifacts remain traceable

bridge or identifier-map references survive when present

corpus membership does not sever namespace provenance
```

This stage protects against selecting evidence without selecting the identity substrate needed to interpret that evidence later.

---

## Stage H — Phase 4.3 Assertion Records

Assertion Records preserve producer assertions.

This is the most important lifecycle checkpoint for namespace provenance.

Assertion Records do not need full canonical identity resolution.

Assertion Records must preserve namespace-aware participant identity state.

Audit questions:

```text
Does each Assertion Record preserve source assertion identity?

Does each Assertion Record preserve participant role?

Does each Assertion Record preserve identity kind?

Does each Assertion Record preserve source namespace?

Does each Assertion Record preserve Source Identity Set references when values
are compacted?

Does each Assertion Record preserve source assertion registration ID?

Does each Assertion Record preserve registration unit ID?

Does each Assertion Record preserve source identity count?

Does each Assertion Record preserve source identity table reference?

Does each Assertion Record preserve source identity filter?

Does each Assertion Record preserve lossiness status?

Does each Assertion Record preserve resolution status?

Does each Assertion Record preserve producer context?

Is the brokerage route explicit or inferable from participant_role,
identity_kind, and source_namespace?
```

Expected audit outcome:

```text
source assertion identity preserved

participant identity state preserved

source identity handles preserved

coordinate/gene/feature/producer routes preserved or inferable

canonical resolution may remain deferred

source identity reconstruction remains possible
```

Critical failures include:

```text
Assertion Record cannot reconstruct source identity

participant role lost

source namespace lost

source identity set reference lost

source identity table reference lost

coordinate-derived assertion reduced to gene-only identity

gene-centered assertion reduced to bare symbol without namespace or scope
```

---

## Stage I — Phase 4.4 Evidence Topology Through Step 7

Evidence Topology organizes preserved assertions.

Topology may remain compact.

Topology may defer full namespace mediation.

Topology must not lose identity handles required for later brokerage or geometry.

Audit questions:

```text
Do topology relationships preserve source assertion references?

Do topology members preserve Source Identity Set references where applicable?

Do topology basis components preserve identity-bearing references?

Does the topology expansion index preserve source assertion registration ID?

Does the topology expansion index preserve identity kind?

Does the topology expansion index preserve participant role?

Does the topology expansion index preserve source namespace?

Does the topology expansion index preserve source identity count?

Does the topology expansion index preserve lossiness status?

Does the topology expansion index preserve resolution status?

Does the topology expansion index preserve Source Identity Set status?

Does namespace mediation remain explicit when deferred?

Does downstream geometry input preserve enough identity state for safe future
Convergence Geometry?
```

Expected audit outcome:

```text
topology artifacts are compact but handle-preserving

Source Identity Sets remain addressable

source identity counts remain preserved by reference

namespace state remains visible

canonical mediation is deferred explicitly when not performed

Convergence Geometry claims are not emitted prematurely
```

Critical failures include:

```text
topology cannot trace to Assertion Records

Source Identity Set handles lost

source namespace lost between Assertion Records and topology

source identity count lost

topology emits geometry-level convergence claims without brokered identity basis

coordinate or gene route becomes unreconstructable
```

---

## Required Audit Outputs

A namespace provenance audit should produce machine-readable and human-readable outputs.

Recommended machine-readable fields:

```text
identity_route

producer

identity_class

source_namespace

earliest_expected_stage

first_observed_stage

last_confirmed_stage

required_fields_present

handle_preserved

value_expansion_required

bridge_required

bridge_available

lossiness_status

resolution_status

audit_status

earliest_gap_stage

recommended_fix_layer

notes
```

Recommended outputs:

```text
namespace_provenance_audit.tsv

namespace_provenance_summary.tsv

namespace_provenance_report.md
```

Recommended output location for corpus-specific audits:

```text
results/phase4/namespace_audit/<corpus_generation_id>/
```

Corpus-specific audit results should not be embedded in this governance document.

---

## Audit Status Values

Recommended audit statuses:

```text
passed

passed_with_deferred_resolution

warning

error

critical

not_applicable

not_evaluated
```

### Passed

Use when:

```text
source identity exists

source namespace exists

producer context exists

handle survives

lossiness is explicit

resolution status is explicit
```

### Passed With Deferred Resolution

Use when:

```text
source identity and namespace are preserved

canonical mediation is not yet performed

deferred status is explicit

future brokerage remains possible
```

### Warning

Use when:

```text
identity route is inferable but not explicit

bridge is required but not registered

feature relationship is present but annotation provenance is incomplete

canonical identity is unavailable but source identity remains preserved
```

### Error

Use when:

```text
required namespace field is missing

coordinate build is missing

coordinate normalization status is unavailable where required

source identity count is missing

source identity table reference is missing

bridge-readiness status is missing

feature interval provenance is unavailable where required
```

### Critical

Use when:

```text
source identity is lost

coordinate identity is lost

noncoding evidence is discarded due to absent gene mapping

canonical identity overwrites source identity

gene identity overwrites coordinate identity

variant observation collapses into variant entity without provenance

gene symbol is treated as exact canonical identity without mapping provenance

producer scope is lost

Assertion Records cannot reconstruct source identity

Evidence Topology cannot trace back to Source Identity Sets
```

---

## Audit Passes

The audit should be performed in at least two passes.

---

## Pass 1 — Artifact And Field Inventory

Pass 1 asks:

```text
What files exist?

What columns exist?

Which columns are empty or nonempty?

Which source namespaces exist?

Which participant roles exist?

Which identity kinds exist?

Which producer identities exist?

Which source identity handles exist?
```

This pass may be performed using TSV, JSON, and manifest inspection.

Pass 1 is necessary but not sufficient.

A field can exist and still fail provenance preservation if it cannot be joined back to its source substrate.

---

## Pass 2 — Lifecycle Join And Provenance Audit

Pass 2 asks:

```text
Can each identity-bearing object be traced from later artifacts back to the
earliest preserved substrate?
```

Examples:

```text
topology expansion row
        ↓
source_identity_set_id
        ↓
assertion_record_source_identity_sets.tsv
        ↓
source_identity_table_reference
        ↓
registration substrate / source artifact

assertion participant
        ↓
assertion_id
        ↓
registration_unit_id
        ↓
corpus_generation_id
        ↓
input TEP / artifact

GSC gene identity
        ↓
source_namespace
        ↓
source_identity_set
        ↓
source table
        ↓
identifier map / adapter-resolved substrate when present

VAP coordinate identity
        ↓
source variant or coordinate field
        ↓
source table
        ↓
VAP TEP artifact
        ↓
run / sample / reference-build context
```

Pass 2 is the provenance-localizing audit.

It determines where patching should occur if preservation fails.

---

## Prohibited Shortcuts

The namespace provenance audit must not use shortcuts that mask provenance defects.

Prohibited shortcuts include:

```text
patching late-stage outputs before locating the earliest provenance break

querying external services during deterministic lifecycle audit

re-querying MyGene.info as a substitute for preserved producer substrate

performing value-level expansion unless explicitly required by the audit scope

expanding all Source Identity Set values when compact handles are sufficient

creating canonical_gene_id values without governed bridge evidence

creating canonical_variant_id values without governed coordinate policy

treating gene symbols as exact canonical identities

treating feature overlaps as causal interpretation

treating absence of gene mapping as variant invalidity

treating unresolved identity as failure when preservation remains intact
```

The audit may identify the need for future value-level mediation.

It must not silently perform that mediation as part of provenance validation.

---

## Relationship To Evidence Topology

Evidence Topology organizes Assertion Records.

Evidence Topology must therefore inherit and preserve namespace-aware identity handles.

Topology artifacts may be compact.

Compactness is acceptable only when it is handle-preserving.

Evidence Topology should not emit full Convergence Geometry claims.

Evidence Topology should preserve enough namespace state for future geometry to determine whether convergence is:

```text
coordinate-centered

feature-mediated

gene-centered

producer-scoped

unresolved

ambiguous

deferred
```

A topology artifact that looks structurally complete but has lost Source Identity Set handle metadata fails namespace provenance audit.

---

## Relationship To Convergence Geometry

Convergence Geometry characterizes organized evidence.

It depends on valid namespace substrate.

If coordinate, feature, gene, or producer identities are collapsed before geometry, VDB may produce:

```text
false-negative convergence
```

or:

```text
false-positive convergence
```

Examples:

```text
false negative
    VAP coordinate evidence and GSC gene evidence cannot converge because
    coordinate-to-gene feature brokerage substrate was lost

false positive
    gene-symbol similarity is treated as exact identity without bridge evidence
```

The namespace provenance audit prevents Convergence Geometry from operating over hidden identity assumptions.

---

## Relationship To Evidence Convergence Surfaces

Evidence Convergence Surfaces expose characterized evidence.

Surfaces must be able to disclose:

```text
source identity

source namespace

brokerage route

bridge status

resolution status

ambiguity status

lossiness status

producer context
```

A surface that hides whether evidence was direct-gene, coordinate-to-feature, unresolved-coordinate, or ambiguous is not safe for downstream reasoning.

---

## Relationship To RDGP

RDGP consumes evidence surfaces.

RDGP-facing surfaces may be gene-centered today, but VDB validation must not assume that all future useful evidence projects cleanly to genes.

Namespace provenance audit must support:

```text
sample-gene evidence surfaces

sample-variant evidence surfaces

coordinate-to-gene mediated surfaces

noncoding burden surfaces

future regulatory or interval-based surfaces
```

RDGP-facing gene surfaces must expose whether evidence arrived through:

```text
direct gene identity

coordinate-to-gene feature brokerage

producer-specific identity

unresolved coordinate evidence

ambiguous bridge state
```

This prevents RDGP from reasoning over hidden identity assumptions.

---

## Recommended First Audit Sequence

For a Phase 4 namespace audit, begin with read-only inspection.

Recommended sequence:

```text
1. Inventory phase4 artifact paths.

2. Inventory columns and empty/nonempty counts across registration,
   Assertion Record, and Evidence Topology outputs.

3. Inventory source_namespace, identity_kind, participant_role, and producer
   context values.

4. Join Evidence Topology expansion rows back to Assertion Record Source Identity
   Sets.

5. Join Assertion Record participants and Source Identity Sets back to
   registration units and source table references.

6. Determine whether coordinate, feature, gene, and producer brokerage lanes are
   explicit, inferable, deferred, or absent.

7. Classify any failures by earliest_gap_stage.

8. Patch only the earliest correct layer.
```

The first audit should not attempt full value-level namespace mediation.

The first audit should determine whether VDB has preserved the substrate needed for later mediation.

---

## Summary

Namespace provenance audit protects VDB's ability to build valid emergent evidence structures.

The audit does not require all identities to resolve.

The audit requires that identities remain preserved, scoped, traceable, and honest about uncertainty.

The audit is successful when VDB can show, stage by stage, that coordinate, feature, gene, and producer identity substrates survive from TEP arrival through Evidence Topology without destructive collapse.

The guiding rule is:

```text
Find the earliest provenance break before patching the downstream symptom.
```

This rule protects Assertion Records, Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, RDGP interfaces, and future noncoding discovery.

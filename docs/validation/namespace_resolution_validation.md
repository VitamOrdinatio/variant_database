# namespace_resolution_validation.md

## Purpose

This document defines how namespace resolution and identity brokerage are validated within the Variant Database (VDB).

Namespace validation evaluates whether identities remain preserved, traceable, authority-aware, and reconstructable throughout namespace resolution and brokerage activities.

Namespace validation protects identity.

Namespace validation does not require all identities to resolve.

This document also defines the full-lifecycle audit expectations required to prove that namespace-bearing substrate survives from TEP arrival through Assertion Records and Evidence Topology.

---

# Scope

This document governs validation of:

```text
identifier preservation

namespace preservation

coordinate/reference-context preservation

feature and interval preservation

gene namespace brokerage

producer namespace preservation

canonical identity attachment

identity mappings

identity lineage

resolution provenance

resolution ambiguity

bridge-readiness state

query-surface identity safety
```

This document defines:

```text
namespace validation objectives

identity-preservation requirements

coordinate-first validation requirements

resolution validation requirements

lifecycle audit requirements

ambiguity handling

authority requirements

namespace validation severity
```

This document does not define:

```text
resolution algorithms

identity authority policies

database implementations

namespace brokerage code

mapping services

coordinate-normalization algorithms

interval-overlap algorithms
```

Those concerns belong to implementation, schema, or specification documents.

---

# Core Principle

```text
Resolution is optional.

Preservation is mandatory.
```

The purpose of namespace validation is not to determine whether every identity resolves.

The purpose of namespace validation is to determine whether identities survive brokerage safely.

The central question is:

```text
Can VDB relate identities
without destroying source identity?
```

For coordinate-first brokerage, the related question is:

```text
Can VDB preserve coordinate, feature, gene, and producer identity substrate
without prematurely collapsing one identity class into another?
```

---

# Lifecycle Principle

Namespace validation is a lifecycle concern rather than a late-stage output check.

A downstream namespace validation failure must not be patched only at the downstream output layer until the earliest provenance break has been located.

The required diagnostic sequence is:

```text
identify the missing datum, invariant, or behavior
        ↓
locate the earliest stage where it should have appeared
        ↓
inspect each propagation boundary
        ↓
patch the earliest incorrect component
        ↓
regenerate downstream derived artifacts
        ↓
rerun validation
```

This rule prevents downstream outputs from masking upstream identity loss.

---

# Relationship To Validation Strategy

The validation strategy defines validation philosophy.

This document applies that philosophy to identity spaces and namespace brokerage.

Conceptually:

```text
validation_strategy.md
        ↓

schema_validation.md
        ↓

namespace_resolution_validation.md
```

---

# Relationship To Ingestion Validation

Ingestion validation asks:

```text
Can identity enter VDB safely?
```

Namespace validation asks:

```text
Can identity brokerage occur safely?
```

Lifecycle namespace validation asks:

```text
Did identity substrate survive every phase needed for future brokerage,
topology, geometry, projection, and reinterpretation?
```

Conceptually:

```text
identity preservation
        ↓
ingestion
        ↓
registration substrate
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
namespace validation
```

---

# Namespace Validation Model

Namespace validation evaluates identity through multiple layers.

```text
Source Identity Preservation
        ↓

Coordinate / Reference-Context Preservation
        ↓

Brokerage Route Validation
        ↓

Canonical Identity Attachment
        ↓

Resolution Status Validation
        ↓

Resolution Provenance Validation
        ↓

Ambiguity Preservation
        ↓

Cross-Domain Consistency
        ↓

Query-Surface Safety
```

Each layer protects a different aspect of identity integrity.

---

# Brokerage Classes Under Validation

VDB validates namespace brokerage across four primary classes.

```text
Default coordinate brokerage

Feature brokerage

Gene brokerage

Producer brokerage
```

These classes are related but must not be collapsed.

---

## Default Coordinate Brokerage

Default coordinate brokerage protects genomic coordinate and reference-context identity.

For variant-derived evidence, coordinate/reference-context identity is the default preservation substrate.

Examples include:

```text
reference_build

contig

start

end

ref

alt

variant_type

normalization_status

coordinate_system

source_variant_id

variant_observation_id
```

A coordinate identity may remain valid even when no gene, transcript, regulatory feature, or ontology relationship is currently available.

---

## Feature Brokerage

Feature brokerage protects relationships between coordinate identities and biological intervals or annotations.

Examples include:

```text
gene locus interval

transcript interval

exon interval

intron interval

UTR interval

regulatory feature interval

conserved element interval

burden window

future feature class
```

Feature relationships supplement coordinate identity.

Feature relationships do not replace coordinate identity.

---

## Gene Brokerage

Gene brokerage protects relationships among gene identifiers and gene-related authority systems.

Examples include:

```text
Ensembl gene ID

NCBI Gene ID

HGNC ID

gene symbol

gene alias

source-local gene ID
```

Gene brokerage remains essential for VDB interoperability, GSC overlays, RSP-style evidence, and RDGP-facing surfaces.

Gene brokerage is a routed specialization rather than the required root identity model for all VDB evidence.

---

## Producer Brokerage

Producer brokerage protects source-native producer identities.

Examples include:

```text
TEP ID

artifact ID

registration unit ID

corpus generation ID

VAP run ID

VAP sample ID

VAP source-local variant ID

GSC release ID

GSC phenotype scope

GSC source ID

GSC semantic channel
```

Producer-scoped identity must remain scoped unless an explicit brokerage event relates it to another identity space.

---

# Layer 1 — Source Identity Preservation

## Purpose

Validate that source identities remain available after brokerage.

---

## Validation Targets

Examples:

```text
source_gene_id

source_gene_symbol

source_gene_namespace

source_variant_id

source_variant_namespace

source_coordinate_identity

source_feature_identity

source_phenotype_id

source_transcript_id

source_locus_id

source_producer_identity
```

---

## Required Checks

```text
source identifiers retained

source namespaces retained

source authority retained

source identity accessible

source identity scope preserved
```

---

## Failure Condition

The following pattern is prohibited:

```text
source identity
        ↓
canonical identity only
```

without preserving source identity.

---

## Success Criteria

Source identities remain reconstructable.

---

# Layer 2 — Coordinate / Reference-Context Preservation

## Purpose

Validate that variant-derived evidence remains preserveable as coordinate/reference-context evidence even when no gene or feature mapping is currently available.

---

## Validation Targets

Examples:

```text
reference_build

contig

start

end

ref

alt

variant_type

coordinate_system

normalization_status

variant entity identity

variant observation identity

sample/run observation context
```

---

## Required Checks

```text
coordinate identity retained when applicable

reference build retained when applicable

contig naming retained when applicable

allele representation retained when applicable

variant entity and variant observation remain distinguishable

noncoding and unannotated coordinate evidence remains valid when preserved
```

---

## Important Rule

Unmapped-to-gene does not mean unmapped-to-genome.

A preserved coordinate identity remains valid evidence even when gene, transcript, feature, or canonical annotation relationships are unresolved or absent.

---

## Success Criteria

Coordinate/reference-context identities remain first-class evidence substrate for variant-derived evidence.

---

# Layer 3 — Brokerage Route Validation

## Purpose

Validate that identities are routed to appropriate brokerage classes without semantic overreach.

---

## Supported Routes

Examples:

```text
coordinate_brokerage

feature_brokerage

gene_brokerage

phenotype_brokerage

producer_brokerage

overlay_brokerage

not_applicable

not_evaluated
```

---

## Required Checks

```text
brokerage route present when evaluated

route basis traceable

route does not mutate source identity

route does not imply biological interpretation

route-specific unresolved state allowed when preservation is intact
```

---

## Important Rule

Resolution route selection is not interpretation.

A route may declare that an identity is coordinate-like, gene-like, producer-scoped, or feature-related.

A route must not claim biological causality, clinical relevance, statistical burden, or mechanistic explanation.

---

## Success Criteria

Brokerage routes are explicit, traceable, and authority-preserving.

---

# Layer 4 — Canonical Identity Attachment

## Purpose

Validate canonical identity integration.

---

## Examples

Canonical identifiers may include:

```text
canonical_coordinate_id

canonical_variant_id

canonical_interval_id

canonical_feature_id

canonical_gene_id

canonical_transcript_id

canonical_phenotype_id

canonical_sample_id

HGNC

Ensembl

ClinVar

dbSNP

RefSeq

MANE

HPO

MONDO
```

---

## Required Checks

```text
canonical identity attached only when supported

canonical authority visible

source identity preserved

canonical identity traceable

canonical identity does not replace source identity
```

---

## Important Rule

Canonical identities supplement source identities.

Canonical identities do not replace source identities.

Canonical gene identities do not replace coordinate identities for variant-derived evidence.

---

## Success Criteria

Canonical identifiers enrich identity without destroying identity provenance.

---

# Layer 5 — Resolution Status Validation

## Purpose

Validate resolution state visibility.

---

## Supported Resolution States

Examples:

```text
exact

alias_resolved

deprecated_resolved

ambiguous

unresolved

conflicted

not_evaluated

not_applicable

source_identity_preserved

coordinate_preserved

bridge_required

bridge_available

bridge_deferred

feature_relationship_deferred
```

---

## Required Checks

```text
resolution status present

resolution status reproducible

resolution state accessible

unresolved state preserved rather than hidden

bridge-readiness state preserved when applicable
```

---

## Success Criteria

Resolution outcomes remain visible.

---

# Layer 6 — Resolution Provenance Validation

## Purpose

Validate traceability of resolution decisions.

---

## Required Resolution Provenance

Examples:

```text
resolution_event_id

authority_source

authority_version

mapping_method

resolved_at

resolution_status

bridge_source

annotation_source

annotation_version
```

---

## Required Checks

```text
mapping origin visible

authority visible

resolution history reconstructable

feature interval provenance visible when coordinate-to-feature relationships are asserted
```

---

## Success Criteria

Future systems can explain why a mapping or relationship occurred.

---

# Layer 7 — Ambiguity Preservation

## Purpose

Protect unresolved and ambiguous identity states.

---

## Examples

Examples include:

```text
multiple candidate genes

multiple candidate transcripts

multiple candidate ontology mappings

historical aliases

conflicting authorities

reference-build ambiguity

contig naming ambiguity

feature-overlap ambiguity

symbol-to-gene ambiguity
```

---

## Required Checks

```text
ambiguity preserved

candidate mappings preserved

conflicts preserved

uncertainty visible
```

---

## Important Rule

Ambiguity is not identity failure.

Ambiguity becomes a validation concern only when ambiguity is hidden.

---

## Success Criteria

Ambiguous identities remain explicitly ambiguous.

---

# Layer 8 — Cross-Domain Consistency

## Purpose

Validate identity brokerage across evidence domains.

---

## Examples

Examples include:

```text
VAP variant evidence

GSC semantic priors

future RSP expression evidence

future RDGP reasoning evidence
```

---

## Required Checks

```text
cross-domain mappings traceable

source identities preserved

canonical identities stable when assigned

brokerage events visible

coordinate-to-feature-to-gene relationships explicit when used

producer identity scope preserved
```

---

## Success Criteria

Evidence domains remain interoperable without identity collapse.

---

# Layer 9 — Query-Surface Safety

## Purpose

Validate safe exposure of identity through query surfaces.

---

## Examples

Examples include:

```text
sample × gene query surfaces

variant × gene query surfaces

coordinate × feature query surfaces

phenotype × gene query surfaces

noncoding burden query surfaces

future cohort query surfaces
```

---

## Required Checks

```text
identity uncertainty visible

resolution status exposed

mapping provenance accessible

ambiguity preserved

coordinate-derived evidence remains distinguishable from direct gene evidence

unresolved coordinate evidence remains exposeable when appropriate
```

---

## Important Rule

Query surfaces must not hide mapping uncertainty.

Query surfaces must not make gene projection appear source-native when it was derived through coordinate-to-feature brokerage.

---

## Success Criteria

Consumers can evaluate identity confidence independently.

---

# Full-Lifecycle Namespace Preservation Audit

## Purpose

The full-lifecycle namespace preservation audit identifies the earliest stage at which each namespace-bearing substrate must appear and verifies that it remains preserved through later VDB phases.

The audit exists to prevent late-stage artifacts from hiding earlier identity loss.

---

## Audit Range

The lifecycle audit covers:

```text
TEP arrival

Phase 0 intake / contract preflight

Phase 1 artifact registration

Phase 2 registration substrate

Phase 3 ingestion finalization

Phase 4.1 registration units

Phase 4.2 corpus generation

Phase 4.3 assertion records

Phase 4.4 Evidence Topology through Step 7
```

---

## Audit Questions

For each stage, validation must ask:

```text
What namespace-bearing substrate should exist at this stage?

Which artifact, table, field, or handle preserves it?

Which brokerage class does it support?

Is the source identity still reconstructable?

Is the namespace still visible?

Is the identity scope still visible?

Is the resolution or bridge-readiness status visible?

Was any identity class collapsed into another identity class?

If loss is detected downstream, what is the earliest stage where the loss occurred?
```

---

## TEP Arrival Audit

TEP arrival validation must confirm that incoming TEPs expose identity-bearing substrate or explicitly declare that such substrate is unavailable.

Required checks include:

```text
TEP identity declared

producer identity declared

payload artifacts declared

identity-bearing artifacts identifiable

source-native identifiers preserved by the producer

coordinate/variant/gene/feature/producer identity lanes detectable when applicable

identifier-map or bridge artifacts declared when provided
```

A missing canonical identity is not a failure by itself.

A missing source identity required to reconstruct producer evidence is a failure.

---

## Phase 0 Intake / Contract Preflight Audit

Phase 0 validation must confirm that VDB detects namespace-bearing substrate before accepting or processing a TEP.

Required checks include:

```text
identity-bearing artifacts classified

brokerage routes preliminarily detectable

missing namespace declarations flagged

unresolved-but-preserved identities allowed

source identity absence escalated

TEP payloads not mutated
```

---

## Phase 1 Artifact Registration Audit

Phase 1 validation must confirm that artifacts containing identities are registered as identity-bearing artifacts.

Required checks include:

```text
artifact identity preserved

artifact role preserved

identity-bearing artifact status preserved

identifier-map artifacts registered when present

bridge artifacts registered when present

artifact checksum and path preserved
```

This phase protects bridge substrate from being dropped before later brokerage.

---

## Phase 2 Registration Substrate Audit

Phase 2 validation must confirm that source identity substrate is preserved at row, table, or handle level.

Required checks include:

```text
source identity tables present when required

Source Identity Sets declared when compact preservation is required

coordinate fields preserved when applicable

gene fields preserved when applicable

feature fields preserved when applicable

producer-scoped identifiers preserved

source table references preserved

source identity counts preserved when expansion is deferred
```

Compact preservation is allowed.

Opaque preservation is not allowed.

---

## Phase 3 Ingestion Finalization Audit

Phase 3 validation must confirm that registration outputs carry brokerage-readiness state.

Required checks include:

```text
identity_kind preserved

participant_role preserved

source_namespace preserved

source_identity_count preserved

source identity table reference preserved

resolution_status preserved

lossiness_status preserved

source identity scope preserved

bridge-readiness state preserved when available
```

---

## Phase 4.1 Registration Unit Audit

Phase 4.1 validation must confirm that Registration Units preserve namespace substrate summaries and source references.

Required checks include:

```text
Registration Unit identity preserved

identity-bearing substrate summarized

coordinate identity presence declared when applicable

gene identity presence declared when applicable

producer identity presence declared when applicable

source artifact references preserved

bridge artifact references preserved when available

unresolved states preserved
```

---

## Phase 4.2 Corpus Generation Audit

Phase 4.2 validation must confirm that corpus selection does not drop namespace substrate required for later Assertion Records, topology, geometry, or projection.

Required checks include:

```text
corpus generation identity preserved

included Registration Units preserved

namespace-bearing unit membership preserved

identity route summaries preserved when available

Source Identity Set references preserved when available

bridge artifact references preserved when available

corpus scope not expanded silently

corpus scope not narrowed in a way that loses required identity substrate
```

---

## Phase 4.3 Assertion Record Audit

Phase 4.3 validation must confirm that Assertion Records preserve namespace-aware participant identity state.

Assertion Records do not need full canonical resolution.

Assertion Records must preserve enough identity substrate for future brokerage, Evidence Topology, Convergence Geometry, projection, and reinterpretation.

Required checks include:

```text
source assertion identity preserved

participant role preserved

identity kind preserved

source namespace preserved

source identity set reference preserved when applicable

source identity count preserved when applicable

source table reference preserved when applicable

resolution status preserved

lossiness status preserved

producer identity preserved

coordinate/variant/gene/feature route detectable when applicable
```

A producer claim may remain valid when canonical identity is unresolved.

A producer claim is not safely preserved if its source identity, namespace, participant role, or identity kind has been lost.

---

## Phase 4.4 Evidence Topology Through Step 7 Audit

Phase 4.4 validation must confirm that Evidence Topology organizes preserved Assertion Records without losing namespace-bearing handles.

Topology artifacts may remain compact, but compactness must be handle-preserving.

Required checks include:

```text
source Assertion Record lineage reconstructable

Source Identity Set references join back to Assertion Record source surfaces

source identity expansion statuses explicit

statistical testing statuses explicit

namespace states explicit

source identity counts preserved by reference when expansion is deferred

coordinate/gene/feature/producer brokerage state not collapsed

no Convergence Geometry claims emitted

no Evidence Convergence Surface eligibility emitted

no RDGP reasoning performed
```

For topology expansion handles, validation must confirm preservation of:

```text
source_assertion_registration_id

identity_kind

participant_role

source_namespace

source_identity_count

lossiness_status

resolution_status

source_identity_set_status
```

Evidence Topology must preserve enough namespace state for Convergence Geometry to operate safely later.

Evidence Topology must not perform biological interpretation.

---

# Authority Validation

Namespace validation must preserve authority.

Examples:

```text
reference build authority

contig naming authority

annotation release authority

HGNC authority

Ensembl authority

ClinVar authority

HPO authority

MONDO authority

producer authority
```

---

## Required Checks

```text
authority source visible

authority version visible

authority lineage traceable

producer authority not overwritten

coordinate authority not hidden behind gene authority
```

---

## Success Criteria

Identity authority remains reconstructable.

---

# Identity Lineage Validation

Namespace validation must preserve identity evolution.

Examples:

```text
deprecated symbols

historical aliases

merged identifiers

superseded identifiers

reference build transitions

annotation release transitions

producer-local identifier evolution
```

---

## Required Checks

```text
identity history available

identifier evolution traceable

supersession visible

mapping release visible when applicable
```

---

## Success Criteria

Identity lineage remains reconstructable.

---

# Resolution Conflict Validation

Namespace validation must preserve conflicting identity claims.

Examples:

```text
multiple authorities disagree

multiple mappings exist

ontology disagreement

cross-reference disagreement

coordinate build disagreement

annotation-source disagreement

feature-overlap disagreement
```

---

## Required Checks

```text
conflict visible

conflict source visible

conflict authority visible

conflict scope visible
```

---

## Important Rule

Conflicts must not be silently resolved.

---

## Success Criteria

Conflicting identity assertions remain reviewable.

---

# Namespace Validation Severity

Namespace validation uses the standard validation severity model.

---

## Informational

Examples:

```text
canonical identity unavailable

canonical gene identity unavailable for a preserved coordinate variant

feature annotation unavailable for a preserved coordinate variant

additional authority available
```

---

## Warning

Examples:

```text
unresolved identity

ambiguous identity

deprecated identifier

coordinate identity preserved but feature relationship deferred

gene bridge unavailable but source gene identity preserved
```

provided preservation remains intact.

---

## Error

Examples:

```text
missing resolution provenance

authority version unavailable

mapping history unavailable

identity conflict untracked

coordinate build missing

coordinate normalization status unavailable

feature interval provenance unavailable

bridge-readiness status missing
```

Errors may prevent safe brokerage until corrected or explicitly waived by policy.

---

## Critical

Examples:

```text
source identity loss

namespace authority loss

coordinate identity loss

canonical identity overwrites source identity

canonical gene identity overwrites coordinate identity

variant observation collapsed into global variant entity without provenance

noncoding variant discarded due to absent gene mapping

ambiguous mapping silently treated as exact

gene symbol treated as exact canonical identity without mapping provenance

identity lineage destruction
```

Critical findings invalidate safe namespace brokerage.

---

# Anti-Collapse Validation

Namespace validation must detect identity collapse.

Validation should detect:

```text
source identity collapse

namespace collapse

authority collapse

lineage collapse

ambiguity collapse

query-surface identity collapse

coordinate identity collapsed into gene identity

variant observation collapsed into variant entity

noncoding variant discarded because no gene mapping exists

unannotated variant treated as invalid

gene symbol treated as exact canonical identity

feature interval treated as equivalent to gene identity

coordinate-to-gene relationship asserted without annotation provenance

producer-scoped identity collapsed into global identity
```

---

# Required Invariants

## Invariant 1

Source identities remain preservable.

---

## Invariant 2

Source namespaces remain visible.

---

## Invariant 3

Coordinate/reference-context identities remain first-class for variant-derived evidence.

---

## Invariant 4

Noncoding and unannotated evidence remains valid when source coordinate identity is preserved.

---

## Invariant 5

Canonical identities supplement source identities.

---

## Invariant 6

Gene identities do not replace coordinate identities.

---

## Invariant 7

Feature relationships remain distinct from identity replacement.

---

## Invariant 8

Resolution provenance remains available.

---

## Invariant 9

Ambiguity remains visible.

---

## Invariant 10

Authority remains visible.

---

## Invariant 11

Identity lineage remains reconstructable.

---

## Invariant 12

Producer-scoped identities remain scoped unless explicitly brokered.

---

## Invariant 13

Query surfaces remain identity-aware.

---

## Invariant 14

Lifecycle audits locate the earliest provenance break before late-stage symptoms are patched.

---

# Relationship To Discovery

Discovery may identify new identities and relationships.

Namespace validation evaluates whether those relationships were attached safely.

Examples:

```text
external ontology attachment

external registry attachment

cross-domain identity bridge

discovered alias mapping

coordinate-to-feature relationship

producer identity relationship
```

Namespace validation does not perform discovery.

Namespace validation evaluates discovery outcomes.

---

# Relationship To Evidence Topology And Convergence Geometry

Evidence Topology organizes preserved evidence relationships.

Convergence Geometry characterizes organized topology.

Namespace validation must ensure that Evidence Topology receives and preserves enough namespace substrate for Convergence Geometry to operate safely.

Validation must prevent these failures:

```text
true convergence missed because source identities were under-preserved

false convergence created because gene symbols were treated as exact identity

noncoding convergence impossible because coordinate evidence was discarded

variant observations collapsed into global variant entities

coordinate-to-feature relationships emitted without provenance
```

Evidence Topology may preserve namespace and expansion handles.

Evidence Topology must not perform Convergence Geometry, burden testing, RDGP reasoning, or biological interpretation.

---

# Relationship To RDGP

RDGP consumes identity-brokered evidence surfaces.

Namespace validation must ensure that RDGP-facing surfaces preserve:

```text
resolution status

authority visibility

identity ambiguity

mapping provenance

bridge status

source identity lineage
```

RDGP-facing gene surfaces must expose whether evidence arrived through:

```text
direct gene identity

coordinate-to-gene feature brokerage

producer-scoped overlay identity

unresolved coordinate evidence
```

This prevents reasoning over hidden identity assumptions.

Future RDGP or RDGP-adjacent consumers may consume noncoding burden surfaces.

Validation must not assume that all useful evidence projects to genes.

---

# Success Criteria

Namespace validation succeeds when VDB can demonstrate that:

```text
identities survive brokerage

coordinate identities remain first-class

noncoding and unannotated evidence remains preserveable

authorities remain visible

resolution history remains available

ambiguity remains visible

cross-domain interoperability remains possible

query surfaces remain identity-aware

lifecycle provenance breaks can be localized
```

without requiring destructive resolution.

---

# Conclusion

Namespace validation exists to protect identity throughout the VDB lifecycle.

The purpose of namespace brokerage is not to erase identity differences.

The purpose of namespace brokerage is to create relationships between identities while preserving their origins.

The purpose of lifecycle validation is to prove that VDB did not lose the identity substrate needed for future brokerage, topology, geometry, projection, RDGP-facing evaluation, and reinterpretation.

The central question of namespace validation is:

```text
Can VDB relate identities
without losing identity?
```

The coordinate-first extension of that question is:

```text
Can VDB preserve full-genome coordinate evidence
without forcing it through present-day gene naming?
```

If the answer is yes, namespace validation has succeeded.

# TEP-VDB Architecture

**Status:** SAGE-VDB architecture draft  
**Intended path:** `docs/architecture/tep_vdb_architecture.md`  
**Layer:** VDB architecture / TEP-VDB export architecture  
**Downstream design family:** `docs/design/projection_surfaces/`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## Purpose

This document defines the architecture of **TEP-VDB**, the VDB-emitted
Transitional Evidence Product intended for downstream consumption by RDGP and
future reasoning systems.

TEP-VDB is not a raw dump of VDB contents.

TEP-VDB is a governed, projection-rich, provenance-preserving reasoning
transport package. It carries VDB-brokered evidence substrates, projection
surfaces, opportunity/context surfaces, policy manifests, and validation
receipts so that downstream systems can reason without re-integrating raw VAP,
GSC, or future producer packages.

The purpose of this architecture is to define what TEP-VDB must carry in order
to support two broad RDGP reasoning activities:

```text
1. Diagnostic support for what is known today.

2. Diagnostic discovery support for what is unknown today but may become known tomorrow.
```

Both activities require traceable evidence, source-preserved identities,
projection policies, genotype context, opportunity context, uncertainty state,
conflict state, and reconstruction paths.

This document is an architecture document. It is not a final implementation
schema, not a file-format specification, not a builder contract, and not an RDGP
reasoning model.

---

## Architectural Position

TEP-VDB sits at the boundary between VDB and downstream reasoning systems.

Conceptually:

```text
Producer TEPs
    ↓
VDB Registration Units
    ↓
Corpus Generation
    ↓
Assertion Records
    ↓
Evidence Topology
    ↓
Convergence Geometry
    ↓
Evidence Convergence Surfaces
    ↓
Projection Surfaces
    ↓
TEP-VDB
    ↓
RDGP / downstream reasoning
    ↓
TEP-RDGP or future reasoning outputs
    ↓
VDB re-ingestion as new assertions
```

TEP-VDB is therefore a transport and exposure product derived from VDB-governed
evidence layers. It does not replace Assertion Records, Evidence Topology,
Convergence Geometry, or Evidence Convergence Surfaces.

TEP-VDB is best understood as an **export projection family** over VDB evidence
state.

---

## Relationship to the Mathematical Foundation

TEP-VDB should conform to the mathematical foundation defined in:

```text
docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md
```

That formalism describes the general chain:

```text
A_C
    → T_C
    → (M_θ, Ω_θ)
    → G_θ
    → S_θ
    → TEP-VDB
    → RDGP
```

Where:

```text
A_C = corpus-indexed Assertion Record set
T_C = typed evidence topology
M_θ = projection membership / incidence operator
Ω_θ = opportunity space for projection policy θ
G_θ = convergence geometry
S_θ = emitted surface under policy θ
```

TEP-VDB is the transport package containing selected surfaces `S_θ`, shared
substrates, and the receipts necessary to reconstruct their derivation.

The governing traceability rule is:

```text
For every emitted surface element c:

tr_θ(c) ≠ ∅
```

That is, every emitted cell, row, count, membership, result, label, or summary
must trace to a finite typed evidence substructure and declared construction
policy.

---

## What TEP-VDB Is

TEP-VDB is a VDB-emitted package containing:

```text
shared evidence substrates
projection surfaces
opportunity and context surfaces
policy manifests
namespace brokerage receipts
surface-cell traceability receipts
validation receipts
anti-overclaim labels
surface currency metadata
```

TEP-VDB is designed to be:

```text
source-traceable
projection-rich
policy-declared
opportunity-aware
identity-preserving
surface-oriented
RDGP-ready
reconstructable
non-authoritative
non-interpretive
```

TEP-VDB defines the evidence room in which RDGP may reason.

It does not perform RDGP reasoning.

---

## What TEP-VDB Is Not

TEP-VDB is not:

```text
a raw VDB database dump

a merged VAP/GSC flat table

a single sample-gene matrix

a pathogenicity adjudication

a diagnostic report

a disease-association test result

a clinical-actionability statement

a replacement for Assertion Records

a replacement for Evidence Topology

a replacement for Convergence Geometry

a replacement for RDGP reasoning
```

TEP-VDB may carry known pathogenicity evidence, burden statistics, recurrence
statistics, prior-locus contrasts, coordinate-window scans, opportunity states,
uncertainty states, and feature projections.

It must not convert those surfaces into biological truth claims.

---

## Relationship to RDGP

RDGP consumes TEP-VDB surfaces.

VDB owns:

```text
evidence preservation
identity brokerage
topology construction
opportunity modeling
projection policy declaration
surface construction
traceability receipts
reason-ready transport
```

RDGP owns:

```text
statistical reasoning
candidate prioritization
model-based evaluation
inheritance reasoning when supported
explanation synthesis
reasoning-output emission
```

The boundary is:

```text
VDB exposes.
RDGP evaluates.
```

RDGP outputs must not mutate the input TEP-VDB, input surfaces, source
assertions, or topology. If RDGP outputs should persist in VDB, they must
return as new producer assertions in a future TEP-RDGP or equivalent reasoning
transport package.

---

## Two RDGP Reasoning Activities

TEP-VDB should support two broad classes of downstream reasoning.

---

### 1. Diagnostic Support for What Is Known Today

This activity asks:

```text
Given current preserved evidence, does this patient carry variants, genes,
prior loci, genotype states, or evidence contexts that are already supported by
known pathogenicity, clinical-significance, phenotype-prior, or curated evidence?
```

This is not discovery-first. It is evidence reconciliation against current
knowledge.

Examples include:

```text
known pathogenic / likely pathogenic variant evidence
known VUS or conflicting variant evidence
phenotype-scoped GSC prior context
genotype support for observed variants
sample-gene evidence rollups
quality / frequency context
conflict and uncertainty state
opportunity-aware absence context
```

The core VDB role is to surface current known evidence without making the final
diagnostic interpretation.

---

### 2. Diagnostic Discovery Support for What Is Unknown Today

This activity asks:

```text
Do patient genomes contain coordinate, locus, feature, recurrence, burden, or
cross-evidence convergence patterns that may nominate candidate variants,
regions, genes, or mechanisms for future interpretation?
```

This is discovery-oriented. It does not depend only on currently known
pathogenic variants.

Examples include:

```text
coordinate-first burden clusters
matched prior-locus burden contrasts
exact recurrent variants across patients
noncoding feature projections
regulatory or conserved-region overlap
patient recurrence
burden excess
opportunity-adjusted coordinate windows
matched background nulls
```

The core VDB role is to expose statistically reason-ready exploratory surfaces
without claiming causality, pathogenicity, disease association, or clinical
truth.

---

## Cross-Cutting Requirement

Both reasoning activities require the same safety substrate:

```text
source provenance
identity brokerage
genotype context
opportunity context
projection policy
uncertainty state
conflict state
surface currency
traceability receipts
anti-overclaim labels
```

Known-evidence support and discovery-oriented support should therefore be
packaged inside one coherent TEP-VDB architecture rather than emitted as
unrelated files.

---

## Three-Layer TEP-VDB Package Model

A TEP-VDB package should have three conceptual layers.

```text
TEP-VDB
    ├── shared substrates
    ├── projection surfaces
    └── policy / validation / traceability receipts
```

---

### Layer 1 — Shared Substrates

Shared substrates are the evidence and identity bases from which multiple
surfaces derive.

Representative shared substrates include:

```text
source corpus manifest
source TEP index
registration unit index
assertion record index
coordinate observations
sample-specific variant observations
genotype observations
source identity records
namespace brokerage records
coordinate / feature / gene / phenotype identity bridges
opportunity space
variant filter partitions
projection policy registry
source traceability receipts
```

Shared substrates are not themselves RDGP conclusions.

They define the evidence universe and reconstruction basis for all downstream
projection surfaces.

---

### Layer 2 — Projection Surfaces

Projection surfaces are VDB-constructed, policy-declared reasoning substrates.

They are emitted so RDGP can reason without re-integrating VAP, GSC, namespace
brokerage, opportunity modeling, projection memberships, or source lineage.

Projection surfaces should be grouped into three families:

```text
known-today diagnostic support surfaces
unknown-tomorrow discovery support surfaces
cross-cutting safety and governance surfaces
```

A surface may belong to more than one family.

---

### Layer 3 — Policy, Validation, and Traceability Receipts

Every TEP-VDB surface must carry receipts sufficient for reconstruction.

Required receipt categories include:

```text
source corpus identity
surface identity
surface generation
projection policy identity
projection policy version
namespace brokerage policy
opportunity policy
filter policy
counting policy
null model policy when applicable
lineage references
surface-cell traceability
validation status
limitations
anti-overclaim labels
reasoning currency state
```

A projection surface without reconstruction receipts is not TEP-VDB compliant.

---

## TEP-VDB v1 Surface Catalog

TEP-VDB v1 should declare the following surface families as first-class
architecture components.

Individual v1 surfaces may begin with minimal payloads, but they should not be
treated as optional conceptual afterthoughts.

```text
KVPS  — Known Variant Pathogenicity Surface
PGERS — Patient Gene Evidence Rollup Surface
GIRS  — Genotype / Inheritance Readiness Surface
OACS  — Opportunity / Absence / Callability Surface
CUES  — Conflict / Uncertainty Evidence-State Surface
CFBS  — Coordinate-First Burden Scan
MPLC  — Matched Prior-Locus Contrast
EVRS  — Exact Variant / Allele Recurrence Surface
RFPS  — Regulatory / Feature Projection Surface
PAPS  — Phenotype Alignment / Prior Surface
RMCS  — Reasoning / Method Currency Surface
```

The architecture-level commitment is that these surface families are part of
TEP-VDB v1's reasoning architecture.

Implementation-specific payload depth may vary by surface maturity.

---

# Known-Today Diagnostic Support Surfaces

These surfaces support RDGP reasoning over currently preserved known evidence.

They help answer:

```text
What does today's evidence already suggest, preserve, contradict, or qualify
for this patient?
```

---

## KVPS — Known Variant Pathogenicity Surface

### Purpose

KVPS exposes known pathogenicity or clinical-significance evidence attached to
sample-specific observed variants under governed identity, quality, genotype,
frequency, phenotype, and provenance policies.

### Core Question

```text
For each sample-specific observed variant, what preserved known pathogenicity,
clinical-significance, uncertainty, conflict, and source-version evidence is
attached to the same governed variant identity or identity neighborhood?
```

### Source Substrate

```text
sample-specific variant observations
coordinate / allele identity
known variant assertion records or clinical-significance overlays
genotype observations
quality context
frequency context
gene / phenotype overlays
source provenance
```

### Minimum v1 Output Concepts

```text
sample_id
run_id
sample_variant_observation_id
coordinate_variant_handle
variant_match_policy_id
variant_match_status
known_assertion_source
known_assertion_id
known_assertion_version
clinical_significance_label
assertion_conflict_state
genotype_observation_id
quality_state
frequency_status
phenotype_scope when available
gene context when available
known_pathogenicity_evidence_label
anti_overclaim_label
source_traceability
```

### Allowed Claims

KVPS may say:

```text
This patient has an observed variant whose governed identity matches preserved
known pathogenicity or clinical-significance evidence under declared policy.
```

KVPS must not say:

```text
This variant caused the patient's disease.
This patient is diagnosed.
This variant is clinically actionable.
```

---

## PGERS — Patient Gene Evidence Rollup Surface

### Purpose

PGERS provides a traceable patient-gene or patient-locus evidence rollup for
RDGP without making gene identity the root evidence substrate.

### Core Question

```text
For each patient and gene or locus, what observed evidence projects here, under
which policy, and with what provenance?
```

### Source Substrate

```text
sample-specific variant observations
coordinate-to-feature memberships
feature-to-gene relationships
genotype context
known pathogenicity memberships
GSC phenotype-scoped prior overlays
opportunity context
source traceability
```

### Minimum v1 Output Concepts

```text
sample_id
gene_id
gene_symbol
gene_namespace
phenotype_scope
projected_variant_count
rare_variant_count
coding_variant_count
noncoding_variant_count
splice_proximal_count
known_pathogenicity_evidence_count
gsc_prior_overlap
gsc_prior_tier
strongest_variant_evidence_label
genotype_context_available
opportunity_context_available
source_variant_observation_ids
projection_policy_id
bridge_status
traceability
```

### Boundary

PGERS may summarize projected evidence.

It must not become a gene-level diagnosis, causal statement, or RDGP ranking.

---

## GIRS — Genotype / Inheritance Readiness Surface

### Purpose

GIRS exposes genotype evidence and structural readiness for downstream
inheritance, dosage, zygosity, or family-aware reasoning.

GIRS does not perform inheritance reasoning.

### Core Question

```text
For each sample-specific variant observation, what genotype evidence is
available, and is it structurally usable for downstream inheritance or dosage
reasoning?
```

### Source Substrate

```text
genotype observations
sample-specific variant observations
FORMAT/sample VCF evidence
genotype call structure
read depth / quality support
sample filter context
source VCF/header context
```

### Minimum v1 Output Concepts

```text
sample_id
variant_observation_id
genotype_observation_id
gt_raw
genotype_call_state
gt_arity
phase_state
is_no_call
is_partial_no_call
depth_context
quality_context
sample_filter_context
inheritance_readiness_label
limitations
source_traceability
```

### Prohibited Claims

GIRS must not infer:

```text
de novo status
compound heterozygosity
recessive model
dominant model
carrier status
biological ploidy
sample sex
hemizygosity
parental origin
```

Those are downstream reasoning responsibilities.

---

## PAPS — Phenotype Alignment / Prior Surface

### Purpose

PAPS exposes phenotype-scoped prior context and phenotype alignment structure
without converting phenotype priors into generic gene truth.

### Core Question

```text
Which patient, gene, locus, variant, or surface evidence aligns with declared
phenotype scopes and preserved phenotype-gene priors?
```

### Source Substrate

```text
GSC phenotype-scoped priors
phenotype identities
sample phenotype context when available
gene identity brokerage
gene / locus evidence surfaces
source GSC traceability
```

### Minimum v1 Output Concepts

```text
sample_id when available
phenotype_scope
phenotype_source
phenotype_mapping_status
gene_id
gene_symbol
gsc_release_id
semantic_prior_id
gsc_prior_score_or_tier when available
source_gsc_trace
alignment_status
phenotype_scope_warning
anti_overclaim_label
```

### Boundary

PAPS may expose phenotype-prior alignment.

It must not conclude phenotype causality, diagnostic fit, or disease mechanism.

---

# Unknown-Tomorrow Discovery Support Surfaces

These surfaces support exploratory diagnostic discovery.

They help ask:

```text
What evidence patterns may become meaningful in the future, even if current
knowledge cannot yet fully interpret them?
```

---

## CFBS — Coordinate-First Burden Scan

### Purpose

CFBS scans coordinate space first, nominates burden or hotspot-like regions,
and only afterward attaches biological annotations.

### Core Question

```text
Across the patient corpus, are there genomic coordinate intervals where
qualifying variants cluster more than expected under a declared genomic
opportunity model?
```

### Architectural Role

CFBS is the coordinate-first discovery surface.

It protects noncoding, intergenic, intronic, regulatory, or currently
unannotated variation from being discarded by gene-first reasoning.

### Boundary

CFBS may nominate exploratory coordinate hotspot candidates.

It must not claim disease association, pathogenicity, causality, or biological
mechanism.

---

## MPLC — Matched Prior-Locus Contrast

### Purpose

MPLC compares burden near phenotype-scoped GSC-prior loci against matched
non-prior background loci.

### Core Question

```text
Within these patient genomes, do GSC-prior loci carry more local rare-variant
burden than comparable non-prior loci under the same technical and patient
background?
```

### Architectural Role

MPLC is the prior-informed locus burden surface.

It is not unbiased genome-wide discovery. It is a controlled test of whether
prior loci show excess local burden relative to matched background loci.

### Boundary

MPLC may report exploratory empirical-null evidence.

It must not claim formal disease association or causality.

---

## EVRS — Exact Variant / Allele Recurrence Surface

### Purpose

EVRS exposes exact or governed-equivalent recurrent variant observations across
patients.

### Core Question

```text
Which exact variants, alleles, or governed-equivalent variant identities recur
across multiple samples or patients?
```

### Source Substrate

```text
coordinate-normalized variant identities
sample-specific variant observations
variant observation identity
quality context
frequency context
genotype context
source traceability
```

### Minimum v1 Output Concepts

```text
coordinate_variant_handle
variant_identity_policy_id
sample_count
patient_count
observation_count
samples_with_variant
genotype_context_summary
quality_context_summary
frequency_context_summary
known_pathogenicity_overlap
artifact_warning_state
source_observation_ids
traceability
```

### Boundary

EVRS may expose recurrence.

It must not decide whether recurrence reflects disease biology, shared ancestry,
technical artifact, batch effect, or chance.

---

## RFPS — Regulatory / Feature Projection Surface

### Purpose

RFPS exposes governed relationships between coordinate evidence and biological
or annotation-derived features such as regulatory intervals, splice regions,
conserved elements, UTRs, promoters, enhancers, or cCRE-like elements.

### Core Question

```text
Which observed variants project to governed noncoding, regulatory,
splice-proximal, conserved, transcript, or feature intervals under declared
feature projection policies?
```

### Source Substrate

```text
coordinate observations
feature interval declarations
coordinate-to-feature memberships
feature-to-gene relationships when governed
annotation source/version provenance
quality and opportunity context
```

### Minimum v1 Output Concepts

```text
sample_id
variant_observation_id
coordinate_variant_handle
feature_id
feature_type
feature_namespace
feature_source
feature_version
overlap_policy_id
overlap_status
distance_to_feature_anchor when applicable
linked_gene_id when governed
feature_opportunity_context
source_traceability
```

### Boundary

RFPS may expose feature membership.

It must not assert that the feature is causal, functional in the patient,
regulatory for a particular gene, or disease-relevant unless such a claim is
preserved as source evidence.

---

# Cross-Cutting Safety and Governance Surfaces

These surfaces support both known-evidence reasoning and discovery-oriented
reasoning.

They prevent missingness, conflict, ambiguity, stale methods, or hidden
projection assumptions from masquerading as clean evidence.

---

## OACS — Opportunity / Absence / Callability Surface

### Purpose

OACS exposes where evidence could have been observed, where absence is
interpretable, and where absence is not interpretable because opportunity is
not available.

### Core Question

```text
For a given sample, region, gene, locus, feature, or window, what was the
opportunity to observe qualifying evidence?
```

### Source Substrate

```text
assay scope
callability estimates
coverage / confidence context
not-assayed regions
filtered regions
unknown opportunity states
projection target definitions
```

### Minimum v1 Output Concepts

```text
sample_id
region_id / gene_id / window_id / feature_id
assay_type
callable_bases
not_callable_bases
not_assayed_bases
low_confidence_bases
filtered_bases
unknown_opportunity_bases
opportunity_state
opportunity_policy_id
negative_evidence_allowed
absence_interpretation_label
limitations
traceability
```

### Boundary

OACS may allow downstream systems to distinguish absence from lack of
opportunity.

It must not itself conclude that a gene, region, or variant class is irrelevant.

---

## CUES — Conflict / Uncertainty Evidence-State Surface

### Purpose

CUES exposes conflict, ambiguity, unresolved state, deprecated evidence,
phenotype mismatch, source disagreement, and other epistemic safety conditions.

### Core Question

```text
Where do preserved assertions disagree, remain unresolved, carry ambiguous
identity state, or require caution before downstream reasoning?
```

### Source Substrate

```text
Assertion Records
clinical-significance labels
namespace brokerage statuses
phenotype-scope mappings
frequency states
quality states
evidence source versions
surface validation warnings
```

### Minimum v1 Output Concepts

```text
evidence_object_id
surface_id when applicable
conflict_type
conflicting_source_assertions
uncertainty_state
ambiguity_state
resolution_status
review_required
source_versions
anti_overclaim_label
traceability
```

### Boundary

CUES may warn or expose epistemic conflict.

It must not adjudicate which conflicting assertion is correct unless a separate
source assertion or downstream reasoning output owns that claim.

---

## RMCS — Reasoning / Method Currency Surface

### Purpose

RMCS tracks whether surfaces and returned reasoning outputs are current relative
to the relevant evidence corpus, projection policies, and reasoning methods.

RMCS applies to:

```text
VDB-emitted surfaces
RDGP-returned reasoning products
RDGP-informed re-emissions
```

which makes RMCS critical for this future loop:

```text
TEP-VDB → RDGP → TEP-RDGP → VDB → updated TEP-VDB
```

### Core Question

```text
Is this surface or reasoning-informed evidence current with respect to the
current corpus and declared method versions?
```

### Source Substrate

```text
surface generation records
corpus generation identity
projection policy versions
reasoning method versions
RDGP returned assertion lineage
new-evidence events
method-change events
refresh status
```

### Minimum v1 Output Concepts

```text
surface_id
surface_generation
source_corpus_id
projection_policy_id
projection_policy_version
reasoning_method_id when applicable
reasoning_method_version when applicable
reasoning_output_id when applicable
currency_state
staleness_reason
refresh_required
refresh_trigger
last_evaluated_generation
current_generation
traceability
```

### Boundary

RMCS may expose stale/current/unknown reasoning currency.

It must not decide whether a newer method is scientifically superior. It only
tracks declared method and corpus relationships.

---

# Surface Family Grouping

TEP-VDB surfaces should be grouped by RDGP reasoning activity.

---

## Known-Today Diagnostic Support Group

```text
KVPS
PGERS
GIRS
PAPS
CUES
OACS
RMCS when reasoning-informed evidence is present
```

These surfaces help RDGP reason from current known evidence.

---

## Unknown-Tomorrow Discovery Support Group

```text
CFBS
MPLC
EVRS
RFPS
PGERS
OACS
CUES
RMCS
```

These surfaces help RDGP reason over emerging, exploratory, uncertain, or
future-interpretable evidence.

---

## Shared Governance Group

```text
source corpus manifest
assertion/topology/geometry lineage
namespace brokerage receipts
projection policy registry
surface validation receipts
surface-cell traceability receipts
anti-overclaim labels
currency and refresh state
```

These records support all surfaces.

---

## Suggested TEP-VDB Package Layout

The exact layout should be derived later in implementation specifications and
schemas. Conceptually, a TEP-VDB package may resemble:

```text
tep_vdb/
    envelope/
    manifest/

    source_corpus/
        source_tep_index
        registration_unit_index
        assertion_record_index
        corpus_generation_manifest

    shared_substrates/
        coordinate_observations
        sample_variant_observations
        genotype_observations
        source_identities
        namespace_brokerage
        identity_bridges
        opportunity_space
        variant_filter_partitions
        projection_policy_registry
        source_traceability

    projection_surfaces/
        known_today/
            kvps_known_variant_pathogenicity_surface
            pgers_patient_gene_evidence_rollup_surface
            girs_genotype_inheritance_readiness_surface
            paps_phenotype_alignment_prior_surface

        discovery_tomorrow/
            cfbs_coordinate_first_burden_scan
            mplc_matched_prior_locus_contrast
            evrs_exact_variant_recurrence_surface
            rfps_regulatory_feature_projection_surface

        governance/
            oacs_opportunity_absence_callability_surface
            cues_conflict_uncertainty_evidence_state_surface
            rmcs_reasoning_method_currency_surface

    receipts/
        validation_receipts
        surface_traceability_receipts
        namespace_receipts
        opportunity_receipts
        projection_policy_receipts
        anti_overclaim_receipts
        currency_receipts
```

This layout is illustrative.

The architecture requirement is not a specific directory tree. The requirement
is that TEP-VDB preserve shared substrates, projection surfaces, and receipts as
separate, traceable, reconstructable package components.

---

## Projection-Specific Daughter Documents

This architecture should serve as the umbrella for projection-specific design
documents under:

```text
docs/design/projection_surfaces/
```

Current projection-surface design documents:

```text
docs/design/projection_surfaces/oacs_opportunity_absence_callability_surface.md
docs/design/projection_surfaces/cues_conflict_uncertainty_evidence_state_surface.md
docs/design/projection_surfaces/rmcs_reasoning_method_currency_surface.md

docs/design/projection_surfaces/kvps_known_variant_pathogenicity_surface.md
docs/design/projection_surfaces/girs_genotype_inheritance_readiness_surface.md
docs/design/projection_surfaces/paps_phenotype_alignment_prior_surface.md
docs/design/projection_surfaces/pgers_patient_gene_evidence_rollup_surface.md

docs/design/projection_surfaces/cfbs_coordinate_first_burden_scan.md
docs/design/projection_surfaces/mplc_matched_prior_locus_contrast.md
docs/design/projection_surfaces/evrs_exact_variant_recurrence_surface.md
docs/design/projection_surfaces/rfps_regulatory_feature_projection_surface.md
```

These daughter documents should remain specialized derivations of this
architecture and of the mathematical formalism.

Each daughter design should define:

```text
purpose
source substrate
projection policy
membership rule
opportunity model if applicable
minimum emitted objects
traceability requirements
validation requirements
allowed claims
prohibited claims
v1 scope
limitations
```

The daughter documents may mature at different rates, but they should not drift
from the shared TEP-VDB architecture, traceability doctrine, opportunity
doctrine, anti-collapse doctrine, or RDGP boundary.

---

## Required Receipts for Every Surface

Every TEP-VDB projection surface should preserve:

```text
surface_id
surface_type
surface_version
surface_generation
source_corpus_id
source_tep_count
source_registration_unit_count
assertion_record_index_id
topology_build_id when applicable
geometry_build_id when applicable
projection_policy_id
projection_policy_version
namespace_policy_id when applicable
opportunity_policy_id when applicable
filter_policy_id when applicable
counting_policy_id when applicable
null_model_id when applicable
random_seed when applicable
surface_validation_status
traceability_receipt_reference
anti_overclaim_label
limitations
```

Surface-specific schemas may add fields, but they must not remove the common
receipt obligations.

---

## Anti-Collapse Rules

TEP-VDB must preserve the following non-collapse rules.

```text
source identity must not collapse into canonical identity

coordinate identity must not collapse into gene identity

variant entity must not collapse into sample-specific variant observation

genotype observation must not collapse into inheritance conclusion

known pathogenicity evidence must not collapse into diagnosis

burden surface must not collapse into disease association

feature membership must not collapse into mechanism

phenotype prior must not collapse into patient diagnosis

projection surface must not collapse into source truth

TEP-VDB must not collapse into RDGP reasoning output

RDGP reasoning output must not mutate TEP-VDB input surfaces
```

Any implementation or document that violates these rules is architecturally
unsafe.

---

## Anti-Overclaim Labels

Every projection surface should carry explicit anti-overclaim labeling.

Representative labels include:

```text
known_evidence_surface_not_diagnosis

exploratory_burden_surface_not_association

feature_projection_not_mechanism

phenotype_prior_not_patient_phenotype_match

recurrence_surface_not_causality

genotype_readiness_not_inheritance_call

opportunity_context_not_negative_conclusion

conflict_surface_not_adjudication

currency_surface_not_method_quality_claim
```

The label set should be refined in future specifications.

The architecture requirement is that overclaim boundaries remain visible to
RDGP and human reviewers.

---

## v1 Architecture Commitments

```text
TEP-VDB v1 should commit to these surface families at the architecture and
manifest level. A given v1 implementation may emit a mature payload, a minimal
payload, a declared-not-yet-populated placeholder, or a validation-not-applicable
receipt for each surface, depending on corpus readiness and producer substrate
availability.
```

TEP-VDB v1 should commit to the following architecture:

```text
1. TEP-VDB is projection-rich, not a raw evidence dump.

2. TEP-VDB carries shared substrates plus projection surfaces.

3. TEP-VDB supports both known-today diagnostic support and unknown-tomorrow
   discovery support.

4. TEP-VDB includes first-class surface families for KVPS, PGERS, GIRS, OACS,
   CUES, CFBS, MPLC, EVRS, RFPS, PAPS, and RMCS.

5. Each surface preserves source traceability, projection policy, limitations,
   and anti-overclaim labels.

6. Opportunity context is required wherever burden, absence, or negative
   evidence interpretation may occur.

7. Genotype context is surfaced for downstream reasoning but does not become
   inheritance reasoning inside VDB.

8. Known pathogenicity evidence is surfaced but not adjudicated as diagnosis.

9. Discovery surfaces are exploratory unless a downstream validated reasoning
   system owns stronger claims.

10. RDGP outputs re-enter VDB only as new assertions, never as mutations of
    source surfaces.
```

### Architecture Commitment vs Implementation Maturity

```text
A surface family may be architecturally first-class before it is implementation
complete. TEP-VDB v1 may declare the family, emit a minimal surface, or emit a
not-populated receipt when required source substrate is unavailable.
```

---

## Non-Goals

This document does not define:

```text
final TEP-VDB physical package layout
SQLite schemas
JSON schemas
TSV schemas
builder implementation details
complete projection-surface specifications
RDGP scoring logic
clinical interpretation rules
formal pathogenicity adjudication
formal disease-association testing
human-reporting templates
```

Those should be derived in later design, specification, schema, validation, and
implementation documents.

---

## Future Derivation Path

Recommended derivation order:

```text
1. docs/architecture/tep_vdb_architecture.md

2. docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md

3. docs/design/tep_vdb_design.md                  # optional architecture-to-design bridge

4. docs/design/projection_surfaces/*.md

5. docs/implementation/specifications/tep_vdb_package_spec.md

6. docs/implementation/schemas/tep_vdb_package_schema.md

7. docs/implementation/specifications/*_projection_surface_spec.md

8. docs/implementation/schemas/*_projection_surface_schema.md

9. docs/validation/tep_vdb_validation.md

10. DEX-VDB builders and tests
```

Projection-specific design documents may be drafted before a full
`tep_vdb_design.md` exists, provided they remain consistent with this
architecture and the mathematical formalism.

---

## Summary

TEP-VDB is the VDB-to-RDGP reasoning transport architecture.

Its core role is to package VDB-preserved and VDB-brokered evidence into
traceable, policy-declared, projection-rich surfaces that RDGP can evaluate.

TEP-VDB must support two complementary RDGP activities:

```text
known-today diagnostic support

unknown-tomorrow diagnostic discovery support
```

To support those activities safely, TEP-VDB v1 should include:

```text
KVPS  — known variant pathogenicity evidence
PGERS — patient-gene evidence rollup
GIRS  — genotype / inheritance-readiness substrate
OACS  — opportunity / absence / callability context
CUES  — conflict / uncertainty evidence state
CFBS  — coordinate-first burden scan
MPLC  — matched prior-locus contrast
EVRS  — exact variant / allele recurrence
RFPS  — regulatory / feature projection
PAPS  — phenotype alignment / prior context
RMCS  — reasoning / method currency
```

Together, these surfaces make TEP-VDB more than a transport envelope.

They make it a governed reasoning platform:

```text
shared substrates
    +
known-evidence surfaces
    +
discovery surfaces
    +
context / denominator / conflict surfaces
    +
policy, lineage, validation, and currency receipts
```

The guiding doctrine is:

```text
VDB constructs the room.
RDGP reasons inside it.
Scientists interpret the evaluated evidence.
```

TEP-VDB therefore preserves the VDB boundary while enabling the central promise
of the repository ecosystem:

```text
intersecting lines of preserved evidence become statistically reason-ready
without losing provenance, identity, uncertainty, or future reinterpretability.
```

# Appendix A: VDB Developmental Phases

```text
Phase 4.4 Evidence Topology:
    produces topology substrate

Phase 4.5 Convergence Geometry:
    computes structural/geometric features

Phase 4.6 Evidence Convergence Surfaces:
    determines which structures are coherent enough to expose

Phase 4.7 Projection / Consumer Surfaces:
    packages selected surfaces into TEP-VDB for RDGP
```

# Appendix B: Corpus Applicability

The TEP-VDB disease-oriented v1 proof should prefer:

```text
5TEP core corpus
14TEP disease/prior exemplar corpus
```

which are each traced to source epilepsy WES SRAs and do not include non-disease HG002.

See `docs/architecture/hg002_wgs_stress_test_retirement_policy.md` for more information.
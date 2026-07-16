# RFPS — Regulatory Feature Projection Surface

**Status:** SAGE-VDB projection-surface design draft  
**Intended path:** `docs/design/projection_surfaces/rfps_regulatory_feature_projection_surface.md`  
**Layer:** TEP-VDB projection surface design  
**Surface family:** TEP-VDB unknown-tomorrow diagnostic discovery support surface; regulatory / feature projection substrate  
**Primary consumer:** RDGP and future downstream reasoning systems  
**Parent architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## 1. Purpose

The Regulatory Feature Projection Surface (RFPS) is the TEP-VDB projection surface that exposes governed relationships between sample-specific coordinate or variant observations and regulatory, transcriptomic, structural, conserved, or functional genomic features.

RFPS exists to prevent VDB and RDGP from collapsing variant-derived evidence into coding-gene-only representations.

RFPS provides RDGP with a traceable substrate for noncoding and regulatory evidence while preserving projection route, feature catalog identity, linkage policy, uncertainty, opportunity context, and anti-overclaim boundaries.

RFPS answers the question:

```text
For this sample-specific coordinate or variant observation, what regulatory,
transcriptomic, structural, conserved, or functional genomic features does it
project to under declared VDB policies, and what optional feature-linked targets
are exposed without inferring regulatory mechanism?
```

RFPS does not answer:

```text
Does this variant regulate this gene?
Does this variant disrupt this feature?
Does this variant explain the patient's phenotype?
Is this variant mechanistically causal?
```

---

## 2. Core Doctrine

```text
RFPS does not infer regulatory mechanism.

RFPS exposes traceable coordinate-to-feature and feature-to-target projection
memberships under declared feature catalogs, linkage policies, confidence
states, opportunity context, and anti-overclaim boundaries so RDGP can reason
over noncoding and regulatory evidence downstream.
```

The governing boundary is:

```text
RFPS exposes feature projection.
RDGP reasons over feature projection.
Scientists and clinicians interpret evaluated evidence.
```

---

## 3. Relationship to TEP-VDB Architecture

TEP-VDB is a projection-rich, provenance-preserving reasoning transport package emitted by VDB for downstream RDGP consumption.

RFPS is one of the projection surfaces in that package. Its role is to expose coordinate-derived feature context without forcing every observation through a gene-centric representation.

RFPS supports both major TEP-VDB reasoning activities:

```text
Known-today diagnostic support:
    expose whether observed variants intersect or project to regulatory or
    functional features relevant to known genes, transcripts, loci, or priors.

Unknown-tomorrow discovery support:
    preserve noncoding, regulatory, conserved, structural, or feature-mediated
    evidence that may become relevant only after downstream recurrence, burden,
    phenotype, or mechanistic reasoning.
```

RFPS is therefore a critical anti-collapse surface. It allows VDB to maintain the coordinate-first doctrine while still creating RDGP-usable feature and target context.

---

## 4. Relationship to Mathematical Formalism

Under the evidence topology / projection / geometry formalism, RFPS is a projection surface defined by a feature-projection policy.

```text
θ_RFPS:
    source objects =
        sample-specific coordinate observations,
        sample-specific variant observations,
        coordinate identity records,
        feature catalog records,
        feature interval records,
        feature-to-target linkage records,
        optional phenotype-prior, recurrence, opportunity, and uncertainty refs

    target objects =
        regulatory, transcriptomic, structural, conserved, or functional
        genomic features, and optional linked gene, transcript, locus, pathway,
        or phenotype-prior targets

    membership =
        coordinate or variant observation belongs to feature target if it
        satisfies declared overlap, distance, linkage, or feature-projection
        policy

    opportunity =
        required when interpreting absence of feature projection or feature
        catalog coverage

    geometry =
        feature membership strata, feature-target linkage strata, projection
        route summaries, context summaries, uncertainty summaries

    surface =
        regulatory feature projection substrate for RDGP
```

Compactly:

```text
S_RFPS = F_RFPS(T_C, M_RFPS, Ω_RFPS, P_RFPS)
```

Where:

```text
T_C = evidence topology

M_RFPS = membership operator from coordinate/variant observations to features
         and optional feature-linked targets

Ω_RFPS = feature/catalog/opportunity context for interpreting absence or
         projection coverage

P_RFPS = feature catalog, overlap, distance, linkage, target projection,
         lossiness, filtering, and labeling policy
```

Required traceability invariant:

```text
Every RFPS feature projection and feature-target link must trace to the source
coordinate observation, feature catalog record, linkage evidence, projection
policy, and explicit uncertainty or missingness state.
```

---

## 5. What RFPS Is

RFPS is a governed projection surface over coordinate-derived evidence.

It may expose:

```text
coordinate-to-feature memberships
variant-to-feature memberships
feature-to-target linkages
feature catalog identity
feature catalog version
feature type
feature context
tissue or cell-type context when declared
assay context when declared
reference genome context
projection route
linkage policy
linkage confidence state
lossiness state
opportunity state
conflict and uncertainty state
traceability receipts
```

RFPS provides a first-class substrate for evidence such as:

```text
promoter overlap
enhancer overlap
splice-regulatory context
UTR overlap
conserved noncoding element overlap
open chromatin overlap
transcription factor binding region overlap
chromatin-contact anchor overlap
topological domain or boundary membership
eQTL or regulatory-link context
nearest-gene fallback context when explicitly labeled as weak context
```

---

## 6. What RFPS Is Not

RFPS is not:

```text
a regulatory mechanism engine

a gene-expression inference engine

a functional validation surface

a pathogenicity classifier

a noncoding diagnostic engine

a gene prioritization score

a phenotype-matching engine

a causal-variant detector

a disease-association test

a replacement for PGERS, EVRS, CFBS, MPLC, PAPS, OACS, CUES, or RDGP
```

RFPS must not emit VDB-generated claims such as:

```text
this variant regulates this gene
this variant disrupts this enhancer
this variant causes loss of expression
this variant explains the phenotype
this is a functional disease variant
this is a causal noncoding variant
```

unless those claims exist as explicit source assertions from a producer and are preserved as such, not inferred by RFPS.

---

## 7. Coordinate-First Design

RFPS starts from sample-specific coordinate or variant observations.

The source object is not a gene.

The source object is:

```text
sample-specific coordinate observation
```

or:

```text
sample-specific variant observation
```

The first projection is:

```text
coordinate / variant observation
    →
regulatory or functional feature
```

Only after that may RFPS expose an optional second projection:

```text
feature
    →
linked gene / transcript / locus / pathway / phenotype-prior target
```

This ordering is mandatory.

A valid RFPS record may have no linked gene:

```text
sample variant overlaps enhancer-like feature;
linked gene unresolved.
```

That record remains useful. It must not be discarded merely because gene projection failed.

---

## 7A. Core Surface Units and Identity Boundary

RFPS has three primary unit types.

The coordinate-to-feature membership unit is:

```text
sample_variant_observation_id × feature_id × coordinate_to_feature_policy_id
```

or, when the source object is not variant-specific:

```text
coordinate_observation_id × feature_id × coordinate_to_feature_policy_id
```

The feature-to-target linkage unit is:

```text
feature_projection_membership_id × projected_target_id × target_link_policy_id
```

The summary unit is policy-dependent, but common summaries include:

```text
sample_id × feature_id × rfps_projection_policy_id

sample_id × projected_target_id × rfps_projection_policy_id
```

RFPS must preserve the distinction among:

```text
coordinate observation
sample-specific variant observation
feature projection membership
feature target link
projected gene / transcript / locus / pathway target
patient-gene rollup
downstream mechanistic reasoning
```

A feature projection without a linked gene is not a failed projection. It is a
valid feature-only evidence state.

A feature-to-gene projection is not a direct gene annotation unless the declared
policy and projection route support that interpretation.

---

## 8. Projection Layers

RFPS has two separable projection layers.

### 8.1 Coordinate-to-Feature Projection

This layer asks:

```text
Does this coordinate or variant observation intersect, neighbor, or otherwise
project to a declared feature under the coordinate-to-feature policy?
```

Examples:

```text
variant overlaps promoter interval
variant overlaps enhancer-like feature
variant falls within splice-proximal window
variant overlaps conserved noncoding element
variant lies within open chromatin region
variant overlaps transcription factor binding region
variant lies within topological domain boundary
```

### 8.2 Feature-to-Target Projection

This layer asks:

```text
Does this feature have a declared target under a feature-to-target policy?
```

Examples:

```text
promoter feature linked to nearby transcript

enhancer feature linked to gene by catalog evidence

eQTL region linked to expression target

chromatin-contact feature linked to locus target

feature linked only by nearest-gene fallback

feature has no declared target
```

The two layers must not be collapsed.

A direct promoter overlap and a distal enhancer-to-gene linkage are different projection routes and must remain distinguishable.

### 8.3 Feature-to-Target Link Status

RFPS should distinguish feature membership from target linkage.

Recommended `target_link_status` values include:

```text
target_link_declared_by_catalog
target_link_experimentally_supported
target_link_computationally_predicted
target_link_nearest_gene_fallback
target_link_contextual_only
target_link_ambiguous
target_link_unresolved
target_link_not_available
target_link_not_evaluated
target_link_not_applicable
```

Recommended `target_link_confidence_label` values include:

```text
high_confidence
moderate_confidence
limited_confidence
weak_context_only
unknown_confidence
not_evaluated
```

Recommended `lossiness_status` values include:

```text
not_lossy
lossy_contextual_bridge
high_lossiness
ambiguous_lossiness
lossiness_unknown
not_evaluated
```

These labels describe projection and linkage state. They are not mechanism,
causality, pathogenicity, or phenotype-fit labels.

---

## 9. Feature Target Vocabulary

RFPS should support feature targets that are not genes.

Valid feature-oriented target types may include:

```text
regulatory_feature
promoter_region
enhancer_region
silencer_or_repressor_region
insulator_or_boundary_region
splice_regulatory_region
utr_region
conserved_noncoding_element
open_chromatin_region
transcription_factor_binding_region
chromatin_contact_anchor
topological_domain_or_boundary
expression_qtl_region
unresolved_feature_target
```

Optional linked targets may include:

```text
linked_gene
linked_transcript
linked_locus
linked_pathway_context
linked_phenotype_prior_context
```

RFPS must support feature-only evidence. A missing gene target is not a reason to discard the feature membership.

---

## 10. Projection Routes

Projection route is a first-class RFPS field.

Possible routes include:

```text
gene_body_overlap
promoter_window_overlap
splice_proximal_window_overlap
UTR_overlap
enhancer_overlap
enhancer_gene_linkage
eQTL_gene_linkage
chromatin_contact_linkage
nearest_gene_fallback
topological_domain_membership
conserved_noncoding_element_overlap
open_chromatin_overlap
transcription_factor_binding_region_overlap
feature_only_projection
unresolved_projection_route
```

These routes must not be flattened into a single field such as:

```text
gene = POLG
```

A safe RFPS projection looks like:

```text
projection_route = distal_enhancer_feature_to_gene_link
target_gene = POLG
target_link_confidence_label = limited
lossiness_status = lossy_contextual_bridge
```

A gene target reached through RFPS is always accompanied by its projection route and linkage policy.

---

## 11. Nearest-Gene Fallback

Nearest-gene projection may be useful, but it is weak context.

RFPS may support nearest-gene mapping only if it is explicitly labeled as fallback context.

Required labels for nearest-gene fallback include:

```text
projection_route = nearest_gene_fallback
target_link_status = weak_context_only
lossiness_status = high_lossiness
anti_overclaim_label = feature_projection_not_mechanism
```

Nearest-gene fallback must not be treated as regulatory linkage.

Nearest gene is not equivalent to target gene.

---

## 12. Feature Catalog Context

RFPS combines sample-specific observations with reference or contextual feature catalogs.

Feature catalogs may be:

```text
general reference catalogs
tissue-specific catalogs
cell-type-specific catalogs
developmental-context catalogs
assay-specific catalogs
disease-context catalogs
source-specific catalogs
```

RFPS must preserve feature-catalog identity and context.

Recommended fields:

```text
feature_catalog_id
feature_catalog_version
feature_context
tissue_context
cell_type_context
developmental_context
assay_context
species_context
reference_genome
source_dataset
source_release
```

When context is unavailable, RFPS should emit explicit missingness labels:

```text
feature_context_not_declared
tissue_context_unknown
cell_type_context_unknown
assay_context_unknown
source_release_unknown
```

Generic feature context must not be silently treated as patient-specific or tissue-specific evidence.

## 12A. Feature Catalog Coverage and Feature Opportunity

RFPS should distinguish genomic opportunity from feature-catalog opportunity.

OACS may describe whether a coordinate region was callable, assayed, filtered,
or observable. RFPS must additionally describe whether a feature class or feature
catalog was available and evaluated for that region.

Recommended feature-catalog opportunity fields include:

```text
feature_catalog_coverage_state
feature_class_evaluated
feature_class_supported_status
feature_catalog_interval_overlap_state
feature_catalog_reference_build_match_status
feature_catalog_context_match_status
feature_opportunity_policy_id
```

Recommended `feature_catalog_coverage_state` values include:

```text
feature_catalog_coverage_available
feature_catalog_coverage_partial
feature_catalog_coverage_not_available
feature_catalog_coverage_not_evaluated
feature_catalog_coverage_unknown
```

Recommended `feature_class_supported_status` values include:

```text
feature_class_supported
feature_class_unmodeled
feature_class_not_available
feature_class_not_evaluated
feature_class_unknown
```

A lack of RFPS projection may reflect no feature membership, but it may also
reflect missing catalog coverage, unsupported feature class, reference-build
mismatch, unmodeled tissue context, or unavailable feature opportunity.

Therefore:

```text
no RFPS feature projection
    ≠ no regulatory relevance
```

unless feature-catalog opportunity and OACS-compatible genomic opportunity are
declared sufficient under policy.

---

## 13. Source Substrates

RFPS may consume the following VDB substrates:

```text
sample-specific coordinate observations
sample-specific variant observations
genotype-to-variant relationship records when feature projection depends on allele-specific VDB-brokered variant relationships
coordinate identity records
variant identity records
feature catalog records
feature interval records
feature-to-target linkage records
reference genome metadata
variant class records
sample/run identity records
producer registration units
assertion record index
namespace brokerage records
projection policy registry
OACS opportunity states
CUES conflict/uncertainty states
EVRS recurrence references
PAPS phenotype-prior references
PGERS patient-gene target references
```

RFPS must remain reconstructable from preserved assertions, feature catalogs, projection policies, and topology elements.

---

## 13A. RFPS Projection Policy

RFPS requires an explicit projection policy.

Recommended policy fields:

```text
rfps_projection_policy_id
rfps_projection_policy_version
source_corpus_generation_id
coordinate_to_feature_policy_id
feature_catalog_policy_id
feature_catalog_coverage_policy_id
feature_class_support_policy_id
target_link_policy_id
target_identity_bridge_policy_id
nearest_gene_fallback_policy_id
feature_context_policy_id
tissue_context_policy_id when applicable
cell_type_context_policy_id when applicable
assay_context_policy_id when applicable
oacs_reference_policy_id
cues_reference_policy_id
rmcs_reference_policy_id
paps_reference_policy_id
pgers_reference_policy_id
evrs_reference_policy_id
kvps_reference_policy_id
girs_reference_policy_id
traceability_policy_id
anti_overclaim_policy_id
```

The RFPS projection policy must declare:

```text
which coordinate or variant observations are eligible

which feature catalogs are eligible

which feature classes are modeled

which reference build is used

how coordinate-to-feature overlap, distance, or membership is determined

how feature-to-target linkage is determined

whether nearest-gene fallback is allowed

how feature-only projections are preserved

how unresolved or ambiguous target links are represented

how feature catalog coverage and feature opportunity are represented

how context such as tissue, cell type, assay, developmental stage, or source
dataset is preserved

which daughter-surface references may be attached

which claims are prohibited
```

Silent feature-class omission, silent nearest-gene fallback, silent target-link
selection, silent feature-context loss, and silent feature-only evidence
discard are prohibited.

---

## 14. Core Evidence Objects

RFPS should define at least the following core objects.

### 14.1 Feature Projection Membership

A `feature_projection_membership` records that a sample-specific coordinate or
variant observation projects to a feature under a declared policy.

```text
feature_projection_membership_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

sample_id
run_id
sample_variant_observation_id when applicable
coordinate_observation_id when applicable
coordinate_variant_handle when applicable

feature_id
feature_type
feature_label
feature_catalog_id
feature_catalog_version
feature_catalog_reference_build
coordinate_to_feature_policy_id
feature_catalog_coverage_state
feature_class_supported_status
projection_route
feature_projection_status
feature_overlap_type
distance_to_feature

oacs_surface_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable
traceability_refs
anti_overclaim_label
```

### 14.2 Feature Target Link

A `feature_target_link` records that a feature projection has an optional target
under a declared linkage policy.

```text
feature_target_link_id
feature_projection_membership_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

projected_target_id
target_type
target_namespace
target_label
target_identity_bridge_id
target_identity_bridge_status
target_identity_bridge_lossiness
target_identity_bridge_policy_id

target_link_policy_id
target_link_status
target_link_evidence_type
target_link_confidence_label
projection_route
lossiness_status

paps_prior_context_ref when applicable
pgers_target_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable
traceability_refs
anti_overclaim_label
```

A feature target link must not replace the underlying feature projection
membership. Target links are optional, policy-declared, and may be ambiguous,
lossy, unresolved, or unavailable.

### 14.3 Feature Projection Summary

A `feature_projection_summary` summarizes RFPS evidence by sample and target,
sample and feature, or sample and projected gene/locus target.

```text
rfps_summary_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

sample_id
summary_target_id
summary_target_type
summary_target_namespace
summary_policy_id

feature_projected_variant_count
feature_type_counts
projection_route_counts
feature_only_projection_count
feature_to_target_link_count
nearest_gene_fallback_count
unresolved_feature_projection_count

feature_catalog_coverage_state
feature_context_state
target_link_conflict_state
conflict_uncertainty_state
oacs_feature_opportunity_state
cues_event_refs when applicable
rmcs_currency_refs when applicable

membership_refs
feature_target_link_refs
traceability_refs
anti_overclaim_label
```

Summary rows must remain reconstructable from feature projection membership rows,
feature target link rows, and declared policy receipts.

---

## 15. Surface Outputs

RFPS should emit three related outputs.

### 15.1 Feature Projection Membership Table

One row per:

```text
sample_variant_observation_id × feature_id × feature_projection_policy_id
```

Recommended fields:

```text
feature_projection_membership_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

sample_id
run_id
sample_variant_observation_id
genotype_observation_id when applicable
genotype_variant_relationship_id when applicable
genotype_variant_relationship_state when applicable
relationship_derivation_policy_id when applicable
coordinate_observation_id
coordinate_variant_handle when applicable

reference_genome
contig
position_or_interval
variant_class

feature_id
feature_type
feature_label
feature_catalog_id
feature_catalog_version
feature_catalog_reference_build
feature_coordinates
feature_context
assay_context
tissue_context
cell_type_context
developmental_context when available

coordinate_to_feature_policy_id
feature_catalog_coverage_policy_id
feature_catalog_coverage_state
feature_class_supported_status
feature_overlap_type
distance_to_feature
projection_route
feature_projection_status

oacs_feature_opportunity_state
oacs_surface_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable

traceability_refs
anti_overclaim_label
```

### 15.2 Feature-to-Target Linkage Table

One row per:

```text
feature_projection_membership_id × projected_target_id × target_link_policy_id
```

Recommended fields:

```text
feature_target_link_id
feature_projection_membership_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

projected_target_id
target_type
target_namespace
target_label
target_identity_bridge_id
target_identity_bridge_status
target_identity_bridge_lossiness
target_identity_bridge_policy_id

target_link_policy_id
target_link_evidence_type
target_link_confidence_label
target_link_status
projection_route
lossiness_status

paps_prior_context_ref when applicable
paps_surface_ref when applicable
pgers_target_ref when applicable
evrs_surface_ref when applicable
kvps_known_evidence_ref when applicable
girs_genotype_context_ref when applicable

cues_event_refs when applicable
rmcs_currency_refs when applicable
traceability_refs
anti_overclaim_label
```

### 15.3 RFPS Summary Table

One row per:

```text
sample_id × projected_target_id
```

or, where useful:

```text
sample_id × feature_id
```

Recommended fields:

```text
rfps_summary_id
rfps_surface_id
rfps_surface_generation_id
source_corpus_generation_id
rfps_projection_policy_id

sample_id
summary_target_id
summary_target_type
summary_target_namespace
summary_policy_id

feature_projected_variant_count
regulatory_feature_projected_variant_count
promoter_projected_variant_count
enhancer_projected_variant_count
splice_regulatory_projected_variant_count
utr_projected_variant_count
conserved_noncoding_projected_variant_count
open_chromatin_projected_variant_count
tf_binding_region_projected_variant_count
chromatin_contact_projected_variant_count
nearest_gene_fallback_count
feature_only_projection_count
unresolved_feature_projection_count

strongest_feature_projection_label
target_link_conflict_state
feature_context_state
feature_catalog_coverage_state
oacs_feature_opportunity_state
cues_conflict_uncertainty_state
rmcs_currency_state when applicable

membership_refs
feature_target_link_refs
traceability_refs
anti_overclaim_label
```

Membership and linkage outputs preserve auditability. Summary outputs support
PGERS and RDGP consumption without replacing feature-level traceability.

---

## 16. RFPS Evidence-State Labels

RFPS labels should describe projection state, not mechanism.

Safe labels include:

```text
feature_projection_present
regulatory_feature_projection_present
feature_to_gene_link_present
feature_to_gene_link_ambiguous
feature_projection_context_limited
nearest_gene_context_only
feature_projection_unresolved
feature_projection_unmodeled
feature_projection_not_evaluated
feature_projection_with_conflict_or_uncertainty
feature_projection_present_without_target_link
feature_projection_present_with_lossy_target_link
feature_projection_present_with_nearest_gene_fallback
feature_projection_present_with_context_limitation
feature_catalog_coverage_limited
feature_class_not_modeled
feature_target_link_not_available
```

Unsafe VDB-generated labels include:

```text
functional_variant
regulatory_pathogenic_variant
enhancer_disruption
gene_regulation_disrupted
mechanistic_support_confirmed
causal_noncoding_variant
target_gene_confirmed
regulatory_target_confirmed
phenotype_relevant_regulatory_variant
disease_regulatory_mechanism
```

RFPS should not emit unsafe labels unless they are preserved source assertions from another producer, and even then they must remain source-attributed and non-adjudicated by VDB.

---

## 17. Relationship to OACS

RFPS depends on OACS when interpreting feature absence or catalog coverage.

No feature projection can mean many things:

```text
no feature catalog coverage
feature type not modeled
assay context not represented
region not callable
feature annotation unavailable for this reference build
projection policy did not evaluate this feature class
unknown feature opportunity
```

Therefore:

```text
No feature projection is not evidence of no regulatory relevance unless feature
opportunity and catalog coverage are declared sufficient.
```

Safe RFPS absence labels include:

```text
feature_projection_present
feature_projection_not_evaluated
feature_projection_unmodeled
feature_projection_absent_with_catalog_opportunity
feature_projection_absence_not_interpretable
```

RFPS should carry OACS references where opportunity context is needed.

---

## 18. Relationship to CUES

RFPS should coordinate aggressively with CUES because feature projection is often uncertain.

CUES should index RFPS events such as:

```text
feature_identity_ambiguous
feature_catalog_stale
feature_target_link_ambiguous
feature_target_link_low_confidence
nearest_gene_fallback_used
feature_context_mismatch
reference_build_mismatch
tissue_context_unknown
cell_type_context_unknown
feature_projection_unmodeled
feature_projection_policy_missing
```

RFPS may expose these states locally, but CUES owns package-level epistemic indexing and summary.

---

## 19. Relationship to PGERS

RFPS feeds PGERS, but PGERS must not erase RFPS projection route.

Example:

```text
RFPS:
    sample variant overlaps distal enhancer feature;
    feature linked to POLG under policy X;
    link confidence = limited.

PGERS:
    POLG patient-gene target has one regulatory-feature-projected
    noncoding observation, with RFPS reference retained.
```

Recommended PGERS fields consuming RFPS:

```text
rfps_feature_projection_refs
regulatory_feature_projected_variant_count
nearest_gene_fallback_count
unresolved_feature_projection_count
```

PGERS must not flatten RFPS evidence into ordinary gene-body variant evidence.

---

## 20. Relationship to EVRS

EVRS exposes exact allele recurrence. RFPS exposes feature projection.

Together they can provide RDGP with a powerful but still non-causal substrate:

```text
same noncoding allele recurs across samples
    +
overlaps enhancer-like feature
    +
feature has phenotype-relevant target context
```

EVRS owns recurrence.

RFPS owns feature projection.

RDGP evaluates biological or diagnostic relevance.

---

## 21. Relationship to CFBS and MPLC

RFPS does not own burden statistics or null models.

CFBS may identify coordinate windows with excess variant concentration. RFPS may annotate which feature classes occur in those windows.

MPLC may evaluate burden in prior-informed loci. RFPS may expose whether variants in those loci are coding, splice-proximal, promoter, enhancer, conserved noncoding, or unresolved.

RFPS must not emit enrichment or burden significance claims unless such claims are preserved source assertions or emitted by a dedicated statistical reasoning surface.

---

## 22. Relationship to PAPS

PAPS owns phenotype-prior alignment.

RFPS may expose whether a feature projects to a target that has phenotype-scoped prior context.

Recommended field:

```text
paps_prior_context_ref
```

RFPS must not infer phenotype fit.

Unsafe RFPS conclusion:

```text
regulatory feature explains epilepsy phenotype
```

Safe RFPS context:

```text
feature-linked target has phenotype-prior context available via PAPS
```

---

## 23. Relationship to KVPS and GIRS

KVPS owns known pathogenicity evidence attached to observed variants.

GIRS owns genotype and inheritance-readiness context.

RFPS may reference both when useful:

```text
kvps_known_evidence_ref
girs_genotype_context_ref
```

However, RFPS should not re-adjudicate pathogenicity or inheritance.

A safe combined context is:

```text
observed noncoding variant has genotype context via GIRS and feature projection
via RFPS; known evidence context is available via KVPS if present.
```

An unsafe conclusion is:

```text
this regulatory variant is pathogenic in this patient.
```

---

## 23A. Relationship to RMCS

RMCS owns method, dependency, currency, validation, refresh, and comparability
state.

RFPS should expose RMCS references when feature projection depends on:

```text
feature catalog version
feature catalog release
feature-to-target linkage source
coordinate-to-feature projection policy
nearest-gene fallback policy
target identity bridge policy
reference build
tissue or cell-type context source
assay-context catalog
surface validation state
```

An RFPS surface generated under a different feature catalog, reference build,
feature-to-target linkage policy, nearest-gene fallback policy, tissue/cell-type
context, or projection policy should not be compared to another RFPS surface
without RMCS comparability state.

Recommended field:

```text
rmcs_currency_refs
```

RMCS should not replace RFPS traceability. It only declares whether the RFPS
surface or feature projection result remains current, stale, superseded,
incomparable, or refresh-required under declared dependencies.

---

## 24. Required Receipts

Every RFPS surface generation should include receipts for:

```text
rfps_surface_id
surface_type
surface_version
rfps_surface_generation_id
source_corpus_id
source_corpus_generation_id
assertion_record_index_id
topology_build_id when applicable
rfps_projection_policy_id
coordinate_to_feature_policy_id
feature_catalog_policy_id
feature_catalog_id
feature_catalog_version
feature_catalog_reference_build
feature_catalog_coverage_policy_id
target_link_policy_id when applicable
target_identity_bridge_policy_id when applicable
nearest_gene_fallback_policy_id when applicable
namespace_policy_id
opportunity_policy_id when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable
traceability_receipt_reference
validation_receipt_reference
anti_overclaim_label
limitations
```

---

## 25. Validation Requirements

RFPS validation should ensure:

```text
every feature projection traces to a source coordinate/variant observation

every feature projection declares a feature catalog and catalog version

every feature-to-target link declares a target-link policy

nearest-gene fallback is labeled as weak context only

feature-only evidence is not discarded when target linkage is unresolved

reference genome context is declared

projection route is present for every feature projection

lossiness status is present for every target linkage

feature context missingness is explicit

OACS references are present for absence/callability-sensitive claims

CUES references are present for ambiguity, missingness, stale catalog, or
low-confidence feature-link states

RFPS does not emit mechanism, causality, pathogenicity, or diagnosis labels

summary rows trace to membership/linkage rows

RFPS surface IDs, surface generation IDs, and projection policy IDs are present

feature catalog coverage state is explicit

feature class support status is explicit

feature-only projections are preserved and not treated as failed gene projections

feature-to-target links preserve target identity bridge status and lossiness

nearest-gene fallback is never treated as regulatory linkage

feature catalog reference build matches or mismatch is surfaced through CUES

tissue, cell-type, assay, and developmental contexts are preserved or explicitly
unknown / not declared

summary rows reconcile to feature projection membership and feature target link
rows

RMCS references are present when feature catalog, linkage, projection policy, or
context currency is exposed

RFPS summary labels are not RDGP prioritization labels
```

---

## 26. v1 Minimum Viable Surface

RFPS v1 should preserve noncoding and feature evidence without overbuilding functional inference.

Minimum v1 inputs:

```text
sample-specific coordinate observations
sample-specific variant observations
reference genome / coordinate identity
variant class
basic gene/transcript annotation if available
feature catalogs if available
feature intervals if available
feature-to-target links if available
OACS opportunity state where available
CUES uncertainty state where available
```

Minimum v1 outputs:

```text
feature projection membership table
feature-to-target linkage table when target links exist
RFPS summary table
```

Required v1 context:

```text
feature_catalog_id
feature_catalog_version
coordinate_to_feature_policy_id
target_link_policy_id when applicable
projection_route
target_link_status
lossiness_status
feature_context_state
traceability_refs
anti_overclaim_label
```

Acceptable v1 limitation labels:

```text
feature_projection_unmodeled
feature_to_target_link_not_available
feature_context_not_declared
tissue_context_unknown
cell_type_context_unknown
```

Explicit unmodeled states are preferable to silently dropping noncoding evidence.

---

## 27. Anti-Overclaim Rules

RFPS must prohibit the following collapses:

```text
feature overlap treated as regulatory mechanism

feature-to-gene link treated as causal regulation

nearest gene treated as regulatory target

noncoding variant discarded because no gene link exists

feature-only evidence forced into a gene row

feature catalog context ignored

tissue/cell-type mismatch hidden

reference-build mismatch ignored

feature projection absence treated as no regulatory relevance without OACS

feature-to-target ambiguity hidden from RDGP

RFPS summary replacing membership-level traceability

RFPS projection state treated as RDGP score

RFPS projection state treated as pathogenicity evidence without KVPS or
explicit source assertion context
```

Required anti-overclaim label:

```text
feature_projection_not_mechanism
```

Additional labels may include:

```text
nearest_gene_context_not_regulatory_linkage
feature_target_link_not_causality
feature_projection_absence_not_negative_evidence
feature_context_not_patient_specific
feature_only_projection_not_failed_projection
target_link_not_gene_truth
nearest_gene_fallback_not_target_gene
feature_catalog_absence_not_no_function
feature_context_not_patient_tissue_context
feature_overlap_not_functional_disruption
rfps_projection_not_rdgp_priority
```

---

## 28. Invalid RFPS Patterns

Invalid RFPS designs include:

```text
collapsing all noncoding variants to nearest gene

requiring every feature projection to resolve to a gene

omitting feature catalog version

omitting projection route

omitting linkage policy

mixing direct gene annotation with distal feature-to-gene linkage

hiding unresolved feature targets

turning enhancer overlap into enhancer disruption

turning feature membership into mechanism

turning feature projection into RDGP priority score

turning no feature projection into no functional relevance

feature-only projection is discarded because no gene target is available

nearest-gene fallback is represented as target-gene linkage

feature catalog absence is interpreted as no regulatory feature

feature class not modeled is represented as no feature overlap

generic feature catalog context is represented as patient-specific tissue context

feature-to-target link is emitted without target identity bridge status

RFPS summary count is treated as a prioritization feature without preserving
membership and linkage references

RFPS surface generated under stale or incompatible feature catalog policy is
consumed without RMCS warning
```

These patterns would violate the coordinate-first and projection-safe architecture.

---

## 29. Strategic Value

RFPS is what makes VDB genuinely coordinate-first rather than coding-gene-first.

Without RFPS:

```text
noncoding evidence either disappears,
gets forced into nearest-gene heuristics,
or gets flattened into unsafe gene annotations.
```

With RFPS:

```text
noncoding evidence remains first-class,
feature memberships are traceable,
gene links are optional and policy-declared,
feature context is explicit,
uncertainty is visible,
and RDGP can reason over regulatory context without VDB inventing mechanism.
```

RFPS therefore protects both known-today diagnostic support and unknown-tomorrow discovery support.

---

## 30. Summary Doctrine

```text
RFPS is the TEP-VDB projection surface that projects sample-specific coordinate
and variant observations onto regulatory, transcriptomic, structural,
conserved, and functional genomic features, and optionally onto feature-linked
gene, transcript, locus, or phenotype-prior targets, while preserving feature
catalog identity, projection route, linkage policy, context, uncertainty,
opportunity state, traceability, and anti-overclaim boundaries so RDGP can
reason over noncoding and regulatory evidence without VDB inferring regulatory
mechanism or causality.
```


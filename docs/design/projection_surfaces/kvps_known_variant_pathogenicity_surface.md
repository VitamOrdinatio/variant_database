# KVPS Known Variant Pathogenicity Surface

**Proposed path:** `docs/design/projection_surfaces/kvps_known_variant_pathogenicity_surface.md`  
**Surface family:** TEP-VDB known-today diagnostic support surface
**Surface abbreviation:** KVPS  
**Status:** SAGE-VDB design draft  
**Primary architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## Purpose

The Known Variant Pathogenicity Surface (KVPS) defines the VDB projection surface that exposes known pathogenicity evidence attached to sample-specific observed variants.

KVPS exists to support RDGP diagnostic reasoning over what is known today.

Its role is to make preserved known-pathogenicity evidence:

```text
patient-observation-aware
identity-brokered
genotype-aware
quality-aware
frequency-aware
phenotype-context-aware
conflict-visible
provenance-preserving
RDGP-ready
```

KVPS does not decide pathogenicity.

KVPS does not diagnose a patient.

KVPS does not perform ACMG classification.

KVPS does not infer inheritance.

KVPS exposes traceable, source-preserved known pathogenicity evidence attached to sample-specific observed variants under governed identity, genotype, quality, frequency, phenotype, and provenance policies.

---

## Relationship to TEP-VDB Architecture

TEP-VDB is a projection-rich, provenance-preserving reasoning transport package emitted by VDB for RDGP consumption.

Within the TEP-VDB architecture, KVPS is a known-today diagnostic support surface.

Conceptually:

```text
TEP-VDB
    ├── shared evidence substrates
    ├── known-today diagnostic support surfaces
    │       └── KVPS
    ├── discovery-tomorrow support surfaces
    └── policy / validation / traceability receipts
```

KVPS complements, but does not replace, other TEP-VDB surfaces:

```text
KVPS
    known pathogenicity evidence attached to observed variants

PGERS
    patient-gene evidence rollup

GIRS
    genotype / inheritance-readiness substrate

OACS
    opportunity / absence / callability context

CUES
    conflict and uncertainty evidence-state surface

PAPS
    phenotype alignment and phenotype-scoped prior context

RMCS
    reasoning and method currency state

CFBS / MPLC / EVRS / RFPS
    discovery-oriented projection surfaces
```

KVPS should therefore remain narrow in authority while rich in traceable context.

---

## Relationship to the Mathematical Formalism

KVPS is a specialization of the VDB evidence topology and projection geometry formalism.

The general VDB formal chain is:

```text
A_C
    → T_C
    → (M_θ, Ω_θ)
    → G_θ
    → S_θ
    → TEP-VDB
    → RDGP
```

KVPS defines a projection policy:

```text
θ_KVPS
```

with the following specialization:

```text
source observations:
    sample-specific variant observations

target objects:
    preserved known-pathogenicity assertion records or assertion groups

membership rule:
    governed variant identity match

opportunity role:
    optional for positive known-evidence attachment;
    required before absence or negative-evidence claims are allowed

surface geometry:
    evidence-state stratification and assertion attachment,
    not burden scanning

surface:
    sample-variant known pathogenicity evidence attachment surface
```

A known assertion group is a governed VDB grouping of preserved source
assertions. It does not replace the individual source assertions and must remain
reconstructable from them.

A compact formal expression is:

```text
S_KVPS = F_KVPS(T_C, M_KVPS, B_C, P_KVPS)
```

where:

```text
T_C
    evidence topology for corpus generation C

M_KVPS
    known-assertion membership operator

B_C
    VDB identity brokerage relation set

P_KVPS
    KVPS projection policy, including identity-match, filter,
    conflict, summarization, and labeling rules
```

The surface-cell traceability invariant applies:

```text
For every emitted KVPS surface element c:

tr_KVPS(c) ≠ ∅
```

Every KVPS row, membership, evidence-state label, or summary must trace back to preserved Assertion Records, source identities, projection policy, and identity brokerage receipts.

---

## Scientific Question

KVPS answers:

```text
For each sample-specific observed variant, what known pathogenicity evidence
is attached to that observation through governed VDB identity brokerage,
and what genotype, quality, frequency, phenotype, conflict, and provenance
context should RDGP see before reasoning over it?
```

KVPS does not answer:

```text
Does this variant cause the patient's disease?

Is this patient diagnosed?

Is this variant clinically actionable?

Which inheritance model is satisfied?

What ACMG classification should be assigned?
```

Those questions belong downstream of KVPS.

---

## Core Doctrine

The core KVPS doctrine is:

```text
KVPS surfaces known pathogenicity evidence.

RDGP reasons over that evidence.

Scientists and clinicians interpret evaluated evidence.
```

KVPS may expose:

```text
known pathogenicity evidence present
known likely pathogenicity evidence present
known conflicting pathogenicity evidence present
known VUS or uncertain evidence present
known benign or likely benign evidence present
identity match ambiguity
phenotype-scope mismatch
frequency or quality limitations
source provenance
```

KVPS must not assert:

```text
pathogenicity as VDB truth
causality
diagnosis
clinical actionability
inheritance satisfaction
ACMG classification
therapeutic relevance
```

---

## Observation-Centered Surface Identity

KVPS is observation-centered.

Its primary unit is:

```text
sample_variant_observation_id
```

not:

```text
variant_id alone
canonical variant entity alone
ClinVar variant record alone
gene_id alone
```

This distinction is required because known pathogenicity evidence becomes patient-relevant only when a governed variant identity is observed in a specific sample context.

Conceptually:

```text
sample-specific observed variant
        ↔ governed variant identity match
        ↔ known pathogenicity assertion
```

KVPS therefore represents:

```text
This sample has this observed variant, and that observation matches these
known pathogenicity assertions under this declared policy.
```

It does not represent:

```text
This variant is pathogenic in this patient.
```

---

## Source Substrates

KVPS may consume the following VDB substrates.

### Required Substrates

```text
sample-specific variant observations
coordinate / reference-context variant identities
variant observation identities
Assertion Records for known pathogenicity or clinical-significance evidence
source identity records
identity brokerage records
projection policy registry
source provenance and lineage records
```

### Recommended Context Substrates

```text
genotype observations
variant quality context
frequency context
gene identity bridges
feature or transcript context
phenotype-scoped GSC prior context
conflict / uncertainty records
surface validation receipts
```

### Optional Future Substrates

```text
external curated pathogenicity assertion streams
expert panel review states
versioned clinical assertion histories
variant normalization equivalence classes
transcript-specific assertion context
condition-specific pathogenicity context
population-stratified frequency context
```

KVPS may reference other TEP-VDB surfaces for context, but it should not duplicate their full responsibilities.

---

## Known Pathogenicity Evidence Scope

KVPS should expose the full known evidence state, not only positive pathogenicity hits.

Recommended v1 known-evidence classes include:

```text
pathogenic
likely_pathogenic
pathogenic_or_likely_pathogenic
vus_or_uncertain
conflicting
benign
likely_benign
benign_or_likely_benign
deprecated
withdrawn
not_reported
unresolved
not_evaluated
```

These labels describe preserved source assertion state.

They are not VDB conclusions.

KVPS should retain source labels, source authority, source version, and source provenance whenever available.

---

## Variant Match Policy

KVPS must make variant matching policy explicit.

Known-variant pathogenicity evidence requires governed variant-level identity membership.

Gene-level overlap, phenotype-level overlap, or prior-gene support may provide context, but must not masquerade as exact known-variant evidence.

Recommended v1 variant match states:

```text
exact_coordinate_allele_match
normalized_allele_equivalence_match
source_asserted_variant_id_match
external_variant_id_match
transcript_context_specific_match
ambiguous_variant_identity_match
unresolved_variant_identity
gene_only_context_match_not_variant_equivalent
phenotype_only_context_match_not_variant_equivalent
no_known_variant_identity_match
```

Only variant-level match states should support strong known-variant evidence attachment.

Context-only matches must remain labeled as context.

---

## Projection Policy

A KVPS projection policy should declare:

```text
projection_policy_id
projection_policy_version
source_observation_scope
known_assertion_scope
variant_match_policy_id
identity_brokerage_policy_id
clinical_significance_label_policy_id
conflict_state_policy_id
frequency_policy_id
quality_policy_id
genotype_context_policy_id
phenotype_context_policy_id
summarization_policy_id
anti_overclaim_policy_id
```

The projection policy must answer:

```text
Which observed variants are eligible?

Which known assertion records are eligible?

How is variant identity equivalence determined?

How are ambiguous matches represented?

How are conflicting known assertions represented?

How are benign/VUS/pathogenic states preserved?

How are genotype, quality, frequency, and phenotype contexts attached?

What evidence-state labels may be emitted?

What claims are prohibited?
```

---

## Membership Operator

KVPS induces a membership relation between sample-specific observed variants and known pathogenicity assertions.

Conceptually:

```text
M_KVPS : O_variant → P(K_known)
```

where:

```text
O_variant
    eligible sample-specific variant observations

K_known
    known pathogenicity / clinical-significance assertion records
    or governed assertion groups

M_KVPS(o)
    known assertion memberships attached to observation o
    under the declared variant match policy
```

Membership does not create new evidence.

Membership exposes governed relationships among preserved evidence objects.

A single observed variant may attach to multiple known assertion records.

Multiple known assertion memberships do not multiply the source observation.

---

## Genotype Context

KVPS should attach genotype context when available.

Recommended genotype context fields include:

```text
genotype_observation_id
gt_raw
genotype_call_state
genotype_quality_state
depth_context
allelic_balance_context when available
phase_state when available
no_call_state
partial_no_call_state
genotype_context_available
genotype_context_limitation
```

When VDB emits genotype-to-variant relationship context, KVPS should preserve
whether the observed variant relationship was direct, brokered, ambiguous, or
unresolved.

Recommended relationship context fields include:

```text
genotype_variant_relationship_id
relationship_state
relationship_derivation_policy_id
relationship_type
allele_index when applicable
source_alt_allele when applicable
normalization_state when applicable
ambiguity_state when applicable
lossiness_state when applicable
identity_registration_state when applicable
```

This is especially important for known evidence attached to variants whose
genotype relationship was resolved from a multiallelic source record.

Safe KVPS statement:

```text
Known pathogenicity evidence is attached to an observed allele whose
genotype-to-variant relationship was resolved from a multiallelic source record
under VDB brokerage policy.
```

Unsafe KVPS statement:

```text
The producer emitted this as an independent biallelic genotype call.
```

KVPS may emit structural genotype labels such as:

```text
observed_heterozygous_like
observed_homozygous_alt_like
observed_reference_like
observed_no_call_or_uncertain
genotype_not_reported
```

These labels must remain genotype-context descriptors.

They must not become inheritance interpretations.

KVPS must not infer:

```text
dominant compatibility
recessive compatibility
compound heterozygosity
de novo status
carrier status
biallelic model satisfaction
segregation support
```

GIRS owns genotype-readiness context.

RDGP owns inheritance reasoning.

KVPS may reference genotype context from GIRS, but KVPS must not infer
inheritance model satisfaction, compound heterozygosity, de novo status, carrier
state, biallelic model satisfaction, or segregation support.

---

## Quality and Frequency Context

KVPS should preserve quality and frequency context so RDGP can reason safely.

Recommended quality context includes:

```text
variant_quality_state
call_filter_state
read_depth_state
genotype_quality_state
low_confidence_flag
quality_limitation
```

Recommended frequency context includes:

```text
frequency_source
allele_frequency
frequency_bin
frequency_policy_id
rare_under_policy
common_under_policy
frequency_missing
frequency_conflicting
frequency_limitation
```

KVPS should not silently discard common, low-quality, or frequency-missing variants unless the projection policy explicitly declares a filtered surface.

Where filtering occurs, the filter policy and excluded-count receipts should be visible.

---

## Phenotype and GSC Prior Context

KVPS may attach phenotype-scoped prior context when available.

Recommended fields include:

```text
phenotype_scope
gsc_prior_present
gsc_prior_strength_label
gsc_prior_source
gsc_release_id
phenotype_scope_match_status
phenotype_scope_not_declared
phenotype_scope_mismatch
phenotype_context_limitation
known_assertion_condition
known_assertion_condition_id
known_assertion_condition_namespace
known_assertion_condition_match_status
```

Phenotype and GSC prior context may strengthen RDGP reasoning, but KVPS must not use such context to upgrade a variant into a pathogenicity conclusion.

A valid KVPS statement is:

```text
This observed variant matches known pathogenicity evidence, and its gene
also has phenotype-scoped GSC prior context.
```

An invalid KVPS statement is:

```text
This variant explains the phenotype because its gene has a GSC prior.
```

PAPS should own broader phenotype alignment and phenotype-prior modeling.

KVPS may reference PAPS-like context without replacing PAPS.

---

## Conflict and Uncertainty Context

KVPS must expose conflict and uncertainty as first-class evidence states.

Recommended conflict dimensions include:

```text
clinical_significance_conflict_state
assertion_source_conflict_state
identity_conflict_state
phenotype_scope_conflict_state
frequency_conflict_state
quality_conflict_state
version_conflict_state
```

Recommended uncertainty states include:

```text
resolved
resolved_with_note
ambiguous
conflicted
unresolved
not_available
not_applicable
not_evaluated
not_reported
deprecated
withdrawn
```

KVPS may expose conflict.

KVPS should not resolve conflict unless the resolution itself is preserved as a source assertion or governed external adjudication assertion.

A valid KVPS label is:

```text
known_pathogenicity_conflict_visible
```

An invalid KVPS label is:

```text
known_pathogenicity_conflict_resolved
```

unless a preserved assertion supports that resolution.

CUES should own broader conflict and uncertainty integration across TEP-VDB surfaces.

KVPS should preserve enough local conflict context for RDGP to reason safely.

---

## Surface Outputs

KVPS should emit both membership-level and summary-level outputs when feasible.

### Membership-Level Output

The membership-level output is audit-oriented.

It may contain one row per:

```text
sample_variant_observation_id × known_assertion_membership
```

Recommended conceptual fields:

```text
known_assertion_membership_id
kvps_surface_id
kvps_surface_generation_id
projection_policy_id
corpus_generation_id
sample_id
run_id
sample_variant_observation_id
coordinate_variant_handle
reference_build
contig
position_or_interval
reference_allele
alternate_allele
variant_match_policy_id
variant_match_status
known_assertion_id
known_assertion_source
known_assertion_version
known_assertion_label
known_assertion_label_normalized
known_assertion_authority_context
known_assertion_uncertainty_context
known_assertion_review_context
known_assertion_provenance
clinical_significance_conflict_state
genotype_observation_id
genotype_context_label
quality_context_label
frequency_context_label
gene_identity_context
phenotype_scope_context
gsc_prior_context
anti_overclaim_label
traceability_reference
validation_status
identity_brokerage_event_refs
```

### Summary-Level Output

The summary-level output is RDGP-oriented.

It may contain one row per:

```text
sample_variant_observation_id
```

with summarized attached known-evidence state.

Recommended conceptual fields:

```text
kvps_surface_id
kvps_surface_generation_id
projection_policy_id
corpus_generation_id
sample_id
run_id
sample_variant_observation_id
coordinate_variant_handle
variant_match_summary_state
known_pathogenicity_evidence_state
known_pathogenicity_evidence_count
strongest_known_assertion_label
benign_evidence_present
conflicting_evidence_present
vus_or_uncertain_evidence_present
identity_ambiguity_state
genotype_context_available
quality_context_state
frequency_context_state
phenotype_prior_context_state
gene_context_state
rdgp_known_evidence_readiness_label
anti_overclaim_label
traceability_reference
validation_status
```

The summary-level table must remain reconstructable from the membership-level table and policy receipts.

---

## Recommended Evidence-State Labels

KVPS v1 should prefer deterministic categorical evidence labels over numeric pathogenicity scores.

Recommended labels include:

```text
known_pathogenicity_evidence_present
known_likely_pathogenicity_evidence_present
known_pathogenic_or_likely_pathogenic_evidence_present
known_conflicting_pathogenicity_evidence_present
known_vus_or_uncertain_evidence_present
known_benign_or_likely_benign_evidence_present
known_assertion_present_but_identity_match_ambiguous
known_assertion_present_but_phenotype_scope_mismatch
known_assertion_present_but_quality_limited
known_assertion_present_but_frequency_limited
no_known_pathogenicity_assertion_attached
known_pathogenicity_evidence_not_evaluated
```

These labels describe evidence attachment state.

They are not clinical conclusions.

---

## RDGP Consumption Role

RDGP consumes KVPS as a known-evidence reasoning substrate.

KVPS helps RDGP answer downstream questions such as:

```text
How should known pathogenicity evidence contribute to gene or variant
prioritization?

How should genotype context affect interpretation of a known pathogenicity
match?

How should conflicting or benign evidence modulate ranking?

How should phenotype-scoped prior context interact with known variant evidence?

How should low-quality, high-frequency, ambiguous, or unresolved evidence
be handled?
```

RDGP may use KVPS to support:

```text
candidate prioritization
known-evidence feature extraction
explanation generation
conflict-aware ranking
review queue construction
```

RDGP must not treat KVPS as a VDB diagnosis.

---

## Relationship to Other TEP-VDB Surfaces

KVPS should have clear boundaries relative to other surfaces.

```text
KVPS
    attaches known pathogenicity evidence to observed variants

PGERS
    rolls evidence up to patient-gene or patient-locus candidate space

GIRS
    exposes genotype and inheritance-readiness context

OACS
    exposes opportunity, callability, and absence interpretability

CUES
    integrates conflict and uncertainty across surfaces

PAPS
    exposes phenotype alignment and phenotype-scoped prior context

RMCS
    tracks corpus, surface, and method currency

EVRS
    exposes exact variant recurrence across samples

RFPS
    projects coordinate evidence to regulatory and feature intervals

CFBS
    scans coordinate windows for burden or clustering

MPLC
    contrasts prior loci against matched background loci
```

KVPS may reference these surfaces.

KVPS should not duplicate or absorb their full responsibilities.

---

## Opportunity and Absence Boundary

KVPS is primarily a positive known-evidence attachment surface.

A positive KVPS row says that an observed variant has attached known evidence under a declared policy.

KVPS should be cautious with absence claims.

The statement:

```text
No known pathogenic variant was observed in gene X.
```

requires opportunity and callability context.

Without OACS support, KVPS may emit:

```text
no_known_pathogenicity_assertion_attached
```

for an observed variant, but it should not make broader regional or gene-level absence claims.

Negative evidence belongs to an opportunity-aware surface.

---

## Traceability Requirements

Every KVPS output must preserve traceability.

Required traceability references include:

```text
sample_variant_observation_id
source Assertion Record identifiers
known assertion identifiers
registration_unit_id
corpus_generation_id
source_package_id
source_artifact_id
source identity references
identity brokerage event identifiers
projection_policy_id
variant_match_policy_id
surface_generation_id
validation receipt references
```

KVPS must allow reconstruction of:

```text
which observed variant was used
which known assertion was attached
which identity match policy connected them
which source labels and versions were preserved
which genotype, quality, frequency, and phenotype context was attached
which conflicts or uncertainties were visible
which anti-overclaim label applied
```

A KVPS surface row without traceability is invalid.

---

## Validation Requirements

KVPS validation should check:

```text
projection_policy_id is present
surface_generation_id is present
corpus_generation_id is present
sample_variant_observation_id is present
known assertion membership rows preserve source assertion identity
variant_match_policy_id is present
variant_match_status is present
identity ambiguity is explicit
clinical significance labels preserve source labels
normalized evidence labels are policy-declared
conflicting assertions are not silently hidden
benign/VUS/conflicting evidence is preserved when present
genotype context is attached or explicitly unavailable
quality context is attached or explicitly unavailable
frequency context is attached or explicitly unavailable
phenotype prior context is attached or explicitly unavailable
traceability references are present
anti-overclaim labels are present
summary rows reconstruct from membership rows
no projection row replaces an Assertion Record
no VDB pathogenicity conclusion is emitted
```

Validation should produce receipts suitable for TEP-VDB inclusion.

---

## Anti-Overclaim Rules

KVPS implementations must not perform the following actions:

```text
gene-level prior treated as exact known variant pathogenicity

phenotype overlap treated as variant pathogenicity

ClinVar or other source label treated as VDB clinical conclusion

known pathogenicity evidence treated as patient diagnosis

known pathogenicity evidence treated as causality

known pathogenicity evidence treated as clinical actionability

variant observation without genotype/quality context treated as high-confidence
patient evidence

ambiguous variant identity treated as exact match

benign, VUS, or conflicting evidence hidden because pathogenic evidence exists

frequency or quality filters applied silently

source version omitted

projection row treated as Assertion Record

RDGP output written back into KVPS instead of re-entering VDB as new assertions
```

Any implementation that performs one of these actions violates KVPS design.

---

## v1 Minimum Viable Surface

KVPS v1 should be conservative but useful.

Minimum v1 inputs:

```text
sample-specific variant observations
coordinate/reference-context variant identity
known pathogenicity or clinical-significance Assertion Records
identity brokerage records
projection policy registry
source provenance
```

Minimum v1 context:

```text
genotype observation reference when available
quality context when available
frequency context when available
gene identity bridge when available
phenotype/GSC prior context when available
```

Minimum v1 outputs:

```text
membership-level known assertion attachment table
summary-level observed variant known-evidence table
variant match status
known evidence-state label
conflict state
traceability reference
anti-overclaim label
validation status
```

Minimum v1 evidence-state labels:

```text
known_pathogenic_or_likely_pathogenic_evidence_present
known_conflicting_pathogenicity_evidence_present
known_vus_or_uncertain_evidence_present
known_benign_or_likely_benign_evidence_present
known_assertion_present_but_identity_match_ambiguous
no_known_pathogenicity_assertion_attached
known_pathogenicity_evidence_not_evaluated
```

KVPS v1 should not emit numeric pathogenicity scores.

KVPS v1 should not emit ACMG classifications.

KVPS v1 should not perform inheritance reasoning.

---

## Future Extensions

Future KVPS versions may support:

```text
richer variant normalization equivalence
transcript-specific pathogenicity assertion context
condition-specific known assertion context
expert-panel assertion stratification
version-to-version clinical assertion history
source-specific review-status weighting exposed as context
population-stratified frequency context
somatic/germline assertion separation
pharmacogenomic assertion context
risk/protective allele assertion context
links to CUES-wide conflict integration
links to PGERS candidate rollups
links to PAPS phenotype alignment summaries
```

Future extensions must preserve KVPS authority boundaries.

Numerical scoring, formal pathogenicity adjudication, ACMG classification, or diagnostic conclusion generation should remain outside KVPS unless VDB later ingests those as explicit producer assertions from an appropriate reasoning or clinical-review source.

---

## Non-Goals

KVPS does not define:

```text
SQLite schemas
JSON schemas
implementation code
full TEP-VDB export schema
RDGP scoring model
ACMG classification model
inheritance reasoning
clinical diagnosis
clinical actionability
causal inference
therapeutic recommendation
```

KVPS is a design model for a VDB projection surface.

Implementation specifications, schemas, validators, and builders should be derived later.

---

## Summary

KVPS is the known-today diagnostic support surface for TEP-VDB.

It exposes, for each sample-specific observed variant, the governed known pathogenicity evidence attached to that observation through VDB-brokered variant identity.

It preserves:

```text
sample-specific observation identity
known assertion identity
variant match policy
genotype context
quality context
frequency context
phenotype-prior context
conflict and uncertainty state
source provenance
surface traceability
anti-overclaim labels
```

It does not decide pathogenicity.

It does not diagnose.

It does not perform inheritance reasoning.

It does not replace RDGP.

The central KVPS doctrine is:

```text
KVPS surfaces known pathogenicity evidence.
RDGP reasons over that evidence.
Scientists and clinicians interpret evaluated evidence.
```

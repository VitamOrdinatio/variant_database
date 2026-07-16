# PGERS — Patient Gene Evidence Rollup Surface

**Status:** SAGE-VDB design draft  
**Intended path:** `docs/design/projection_surfaces/pgers_patient_gene_evidence_rollup_surface.md`  
**Surface family:** TEP-VDB known-today diagnostic-support surface; shared RDGP patient-gene/locus consumption plane  
**TEP-VDB role:** Rollup surface over preserved VDB substrates and daughter projection surfaces  
**Parent architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## Purpose

The Patient Gene Evidence Rollup Surface (PGERS) defines the VDB projection surface that rolls patient-specific evidence onto governed gene, locus, or gene-adjacent targets for downstream RDGP consumption.

PGERS exists because RDGP commonly reasons over a patient-gene evidence state, while VDB must preserve coordinate-first, assertion-first, provenance-preserving evidence rather than collapsing the system into a gene-centered database.

PGERS therefore provides a traceable bridge between:

```text
VDB's preservation substrate:
    assertions
    coordinate observations
    sample-specific variant observations
    genotype observations
    identity brokerage records
    feature/gene memberships
    phenotype-scoped priors
    opportunity state
    conflict state

and RDGP's common reasoning substrate:
    sample × gene/locus evidence state
```

PGERS is a rollup surface.

It is not a prioritization engine.

It is not a causal-gene detector.

It is not an inheritance model.

It is not a diagnosis.

---

## Relationship to TEP-VDB Architecture

PGERS is one of the v1 TEP-VDB projection surfaces defined by the TEP-VDB architecture.

Within the TEP-VDB package family, PGERS serves as the primary patient-gene or patient-locus consumption plane for RDGP.

Conceptually:

```text
TEP-VDB
    ├── shared substrates
    │       ├── assertion records
    │       ├── coordinate observations
    │       ├── sample-specific variant observations
    │       ├── genotype observations
    │       ├── namespace brokerage records
    │       ├── opportunity state
    │       └── projection policy registry
    │
    ├── daughter / contributing projection surfaces
    │       ├── KVPS
    │       ├── GIRS
    │       ├── OACS
    │       ├── CUES
    │       ├── PAPS
    │       ├── RFPS
    │       ├── CFBS
    │       ├── MPLC
    │       └── EVRS
    │
    └── PGERS
            └── patient-gene / patient-locus rollup surface for RDGP
```

PGERS may reference daughter or contributing TEP-VDB surfaces, but it does not
replace them, absorb their authority, or erase their membership-level
traceability.

For example:

```text
KVPS owns known-variant pathogenicity evidence attachment.
GIRS owns genotype / inheritance-readiness substrate.
OACS owns opportunity, absence, and callability state.
CUES owns conflict and uncertainty state.
PAPS owns phenotype alignment and phenotype-scoped prior context.
RFPS owns regulatory / feature projection memberships.
CFBS owns coordinate-first burden scan signals.
MPLC owns matched prior-locus contrast signals.
EVRS owns exact variant / allele recurrence signals.

PGERS rolls selected signals and references into a patient-gene/locus evidence state.
```

---

## Relationship to Mathematical Formalism

PGERS is a specialization of the VDB evidence topology and projection geometry formalism.

Using the formal chain:

```text
A_C
    → T_C
    → (M_θ, Ω_θ)
    → G_θ
    → S_θ
    → TEP-VDB
    → RDGP
```

PGERS is the surface:

```text
S_PGERS = F_PGERS(T_C, M_PGERS, Ω_PGERS, P_PGERS)
```

Where:

```text
T_C
    corpus-indexed evidence topology derived from preserved Assertion Records

M_PGERS
    membership operator assigning evidence objects to patient-gene,
    patient-locus, or patient-gene-adjacent targets

Ω_PGERS
    opportunity and callability context required for safe absence,
    denominator, and zero-evidence interpretation

P_PGERS
    projection, grouping, counting, filtering, labeling, and traceability policy

S_PGERS
    emitted Patient Gene Evidence Rollup Surface
```

PGERS is not a new truth layer.

PGERS is a policy-declared projection over preserved evidence, derived topology, opportunity context, and daughter projection surfaces.

---

## Scientific Question

PGERS answers:

```text
For this patient, what traceable evidence currently projects to this gene,
locus, or governed gene-adjacent target under declared VDB policies?
```

PGERS does not answer:

```text
Is this gene causal?
Is this the patient's diagnosis?
Should this gene be clinically reported?
What inheritance model is satisfied?
What is the final prioritization rank?
```

Those questions belong downstream to RDGP, clinical review, or other governed reasoning systems.

---

## Governing Doctrine

The governing doctrine of PGERS is:

```text
PGERS does not decide which gene is causal.

PGERS provides a traceable, policy-declared rollup of patient-specific evidence
projected onto gene, locus, or gene-adjacent target units for downstream RDGP
reasoning.
```

The key architectural tension PGERS resolves is:

```text
RDGP commonly needs sample × gene evidence states.

VDB must not collapse coordinate-first evidence preservation into a
simple gene-centered database.
```

Therefore PGERS must provide gene-oriented usability while preserving:

```text
coordinate evidence
sample-specific observation identity
variant identity
projection route
identity bridge status
feature/locus context
phenotype scope
opportunity state
provenance
uncertainty
surface traceability
```

---

## What PGERS Is

PGERS is:

```text
a patient-gene / patient-locus evidence rollup surface

a VDB-brokered projection over sample-specific evidence

a traceable RDGP input surface

a policy-declared aggregation view

a bridge from coordinate-first evidence to gene/locus reasoning units

a surface that preserves projection route and evidence strata
```

PGERS may expose:

```text
projected variant counts
rare variant counts
coding and noncoding evidence strata
known pathogenicity evidence summaries
variant recurrence context
genotype context summaries
opportunity and absence context
phenotype-scoped prior context
regulatory / feature-mediated projection context
CFBS / MPLC / EVRS surface references
conflict and uncertainty labels
traceability to source evidence
```

---

## What PGERS Is Not

PGERS is not:

```text
a gene prioritization score

a causal gene detector

a diagnostic conclusion

an inheritance model

an ACMG classifier

a clinical actionability surface

a phenotype-matching engine

a statistical association test

a replacement for coordinate evidence

a replacement for daughter projection surfaces

a replacement for RDGP reasoning
```

PGERS may expose evidence in a patient-gene form.

It must not claim that the gene is causal, diagnostic, prioritized, clinically actionable, or biologically proven.

---

## Core Unit

The core PGERS summary unit is:

```text
sample_id × projected_gene_target_id × projection_policy_id
```

It is intentionally not:

```text
sample_id × gene_symbol
```

because apparent gene-level evidence may arise through different projection routes, including:

```text
variant directly annotated to gene
coordinate overlaps gene body
coordinate overlaps promoter window
coordinate overlaps splice-proximal region
coordinate overlaps regulatory feature linked to gene
variant belongs to known pathogenicity assertion for gene
gene appears in phenotype-scoped GSC prior
gene appears through ambiguous identity bridge
gene appears through source-native label only
```

Those routes are not equivalent.

PGERS must preserve the route by which evidence reached a gene, locus, or gene-adjacent target.

---

## Patient, Sample, and Subject Identity Boundary

PGERS may use `sample_id` as the practical v1 row anchor, but it must not
silently collapse sample identity into patient identity.

When patient or subject identity is available, PGERS should preserve:

```text
patient_id when available
subject_id when available
sample_id
sample_patient_link_id when available
sample_patient_link_status
sample_role when available
```

Recommended `sample_patient_link_status` values include:

```text
same_subject_declared
same_subject_inferred_by_source
sample_patient_link_unavailable
sample_patient_link_ambiguous
sample_patient_link_not_evaluated
```

This distinction matters because future RDGP reasoning may involve:

```text
multiple samples from one patient
family or trio samples
tumor/normal or tissue-specific samples
technical replicates
longitudinal samples
re-ingested reasoning products
```

PGERS may provide a patient-gene/locus consumption plane, but its evidence rows
must remain traceable to the sample-specific observations that generated them.

---

## Projected Gene Targets

PGERS should support multiple target types.

Recommended `projected_gene_target_type` values include:

```text
canonical_gene
source_gene
gene_locus_interval
gene_body_window
splice_proximal_gene_window
promoter_gene_window
regulatory_linked_gene
feature_linked_gene
phenotype_prior_gene
candidate_locus_gene
ambiguous_gene_target
unresolved_gene_target
```

A projected target should preserve:

```text
projected_gene_target_id
projected_gene_target_version when applicable
target_type
target_namespace
target_label
canonical_gene_id when available
source_gene_id when applicable
source_gene_label when applicable
reference_build when interval-based
feature_or_locus_reference when applicable
target_identity_bridge_id
target_identity_bridge_policy_id
target_identity_bridge_status
target_identity_bridge_lossiness
target_identity_bridge_traceability_refs
projection_policy_id
projection_route
bridge_status
lossiness_status
```

`bridge_status` and `lossiness_status` may be retained as compact summary
fields, but PGERS should preserve the more explicit target-identity bridge
fields when available. A lossy, ambiguous, or unresolved bridge must not be
represented as exact gene support.

A gene target may be useful to RDGP even when it is not fully canonicalized.

However, unresolved, ambiguous, or lossy target state must remain visible.

---

## Projection Routes

PGERS must preserve projection route.

Recommended `projection_route` values include:

```text
direct_source_gene_annotation
coordinate_to_gene_body
coordinate_to_transcript
coordinate_to_splice_proximal_region
coordinate_to_promoter_window
coordinate_to_regulatory_feature_to_gene
coordinate_to_feature_to_gene
known_variant_assertion_to_gene
phenotype_prior_to_gene
mplc_locus_to_gene
cfbs_interval_to_gene
exact_variant_recurrence_to_gene
ambiguous_identity_bridge
unresolved_gene_projection
```

Projection route is not decorative metadata.

It is part of the meaning of the row.

For example:

```text
coding variant directly annotated to POLG
```

is not equivalent to:

```text
noncoding variant projected to POLG through a regulatory feature policy
```

Both may be RDGP-relevant.

They must remain distinguishable.

---

## Projection Route Multiplicity

A single patient-gene/locus target may receive evidence through multiple
projection routes.

PGERS should therefore distinguish:

```text
primary_projection_route when declared
contributing_projection_routes
projection_route_count
route_summary_policy_id
route_lossiness_summary
```

`primary_projection_route` is optional and must be policy-declared. PGERS must
not silently select a primary route merely because one route is easier to display.

When multiple routes contribute to a summary row, the summary must remain
reconstructable from membership-level rows that preserve each route separately.

Example:

```text
POLG patient-gene target receives:
    direct coding variant evidence
    known pathogenicity evidence via KVPS
    phenotype-prior context via PAPS
    genotype-readiness context via GIRS
```

These routes may support RDGP reasoning differently. PGERS may summarize them,
but it must not homogenize them into one unlabeled evidence class.

---

## Source Substrates

PGERS may consume or reference the following source substrates.

### Core VDB Substrates

```text
Assertion Records
Evidence Topology
coordinate observations
sample-specific variant observations
source identity records
namespace brokerage records
projection policy registry
opportunity / callability records
provenance records
validation receipts
```

### Projection Surface Substrates

```text
KVPS
    known variant pathogenicity evidence memberships

GIRS
    genotype / inheritance-readiness context

OACS
    opportunity, callability, and absence context

CUES
    conflict and uncertainty state

PAPS
    phenotype alignment and phenotype-scoped prior context

RFPS
    regulatory and feature projection memberships

CFBS
    coordinate-first burden scan intervals and signals

MPLC
    matched prior-locus contrast context

EVRS
    exact variant / allele recurrence context

RMCS
    surface and method currency state
```

PGERS should not require all daughter surfaces to be present before it can exist.

However, PGERS must distinguish:

```text
surface_not_available
surface_not_evaluated
surface_evaluated_no_membership
surface_evaluated_with_membership
surface_evaluated_with_conflict
surface_evaluated_with_limitation
```

---

## Daughter Surface Dependency Status

Because PGERS rolls up or references multiple daughter surfaces, each daughter
surface dependency should carry an explicit dependency status.

Recommended `daughter_surface_dependency_status` values include:

```text
surface_required_and_available
surface_optional_and_available
surface_not_available
surface_not_evaluated
surface_evaluated_no_membership
surface_evaluated_with_membership
surface_evaluated_with_conflict
surface_evaluated_with_limitation
surface_blocked_by_validation
surface_blocked_by_policy
surface_currency_unknown
surface_stale_under_rmcs
```

PGERS should preserve a dependency record for each daughter surface whose
absence, presence, limitation, or currency affects a rollup field.

Recommended dependency fields include:

```text
daughter_surface_id
daughter_surface_type
daughter_surface_generation_id
daughter_surface_dependency_status
dependency_required_by_policy
dependency_effect_on_pgers
cues_event_refs when applicable
rmcs_currency_refs when applicable
```

A PGERS summary field must not imply that a contributing surface was evaluated
when the contributing surface was unavailable, stale, not evaluated, or blocked

---

## Relationship to KVPS

KVPS operates at:

```text
sample_variant_observation × known pathogenicity assertion
```

PGERS operates at:

```text
sample × projected gene/locus target
```

Therefore KVPS contributes to PGERS, but PGERS does not replace KVPS.

Example:

```text
KVPS:
    this observed variant matches a known pathogenic assertion

PGERS:
    this patient-gene target has one observed variant with known
    pathogenicity evidence attached
```

PGERS may include KVPS-derived summary fields such as:

```text
kvps_known_pathogenicity_evidence_count
kvps_likely_pathogenicity_evidence_count
kvps_conflicting_pathogenicity_evidence_count
kvps_vus_or_uncertain_evidence_count
kvps_benign_or_likely_benign_evidence_count
kvps_strongest_known_evidence_label
kvps_conflict_state
kvps_membership_refs
kvps_surface_ref
```

KVPS remains the authoritative projection surface for known variant pathogenicity evidence attachment.

---

## Relationship to GIRS

GIRS owns genotype and inheritance-readiness substrate.

PGERS may summarize genotype context.

PGERS must not perform inheritance reasoning.

Allowed PGERS genotype summaries include:

```text
genotype_context_available_count
genotype_context_missing_count
heterozygous_like_variant_count
homozygous_alt_like_variant_count
hemizygous_like_variant_count when declared by producer/policy
no_call_or_uncertain_genotype_count
phase_information_available_count
phase_information_missing_count
girs_surface_ref
```

When GIRS exposes VDB-brokered genotype-to-variant relationship context, PGERS
may summarize relationship-readiness state without performing inheritance
reasoning.

Allowed PGERS genotype-relationship summaries include:

```text
genotype_variant_relationship_ready_count
genotype_variant_relationship_unresolved_count
genotype_variant_relationship_ambiguous_count
direct_source_biallelic_relationship_count
resolved_from_multiallelic_record_count
brokered_with_normalization_relationship_count
multiallelic_relationship_resolved_count
multiallelic_relationship_unresolved_count
multiallelic_relationship_not_evaluated_count
```

PGERS must not treat these relationship summaries as inheritance conclusions.

PGERS must not emit:

```text
dominant_model_satisfied
recessive_model_satisfied
compound_heterozygous
de_novo_candidate
carrier_status
biallelic_disease_model_satisfied
inheritance_mode_supported
```

Those belong to RDGP or a governed inheritance reasoning surface.

---

## Relationship to OACS

OACS is required for safe interpretation of zero or absent evidence.

PGERS must not treat lack of projected variants as negative evidence unless opportunity state supports that interpretation.

Core rule:

```text
No observed projected variants for a gene target is not negative evidence
unless OACS declares opportunity sufficient under the relevant policy.
```

PGERS may include OACS-derived fields such as:

```text
opportunity_state
callable_bases
not_callable_bases
not_assayed_bases
low_confidence_bases
filtered_bases
unknown_opportunity_bases
absence_interpretation_label
negative_evidence_allowed
oacs_surface_ref
```

Recommended absence labels:

```text
observed_evidence_present
no_observed_evidence_with_opportunity
no_observed_evidence_without_opportunity
no_observed_evidence_not_callable
no_observed_evidence_not_assayed
no_observed_evidence_unknown_opportunity
absence_not_evaluated
```

---

## Relationship to CUES

CUES owns conflict and uncertainty state.

PGERS may summarize conflict and uncertainty so RDGP can avoid treating ambiguous evidence as clean support.

PGERS may include:

```text
conflict_state
uncertainty_state
identity_ambiguity_present
pathogenicity_conflict_present
phenotype_scope_conflict_present
projection_route_conflict_present
opportunity_conflict_present
review_required
cues_surface_ref
```

PGERS must not resolve conflicts unless a preserved source assertion or governed policy explicitly provides a resolution state.

---

## Relationship to PAPS

PAPS owns phenotype alignment and phenotype-scoped prior context.

PGERS may include compact PAPS-derived fields such as:

```text
phenotype_scope
paps_prior_present
paps_prior_strength_label
paps_alignment_status
paps_prior_source_refs
paps_surface_ref
```

PGERS must not flatten phenotype-scoped GSC priors into generic gene truth.

A GSC prior is not simply:

```text
gene support
```

It is:

```text
phenotype-scoped evidence about a phenotype-gene relationship
```

PGERS may expose that context.

RDGP reasons over it.

---

## Relationship to RFPS

RFPS owns regulatory and feature projection memberships.

PGERS may roll RFPS memberships into gene-adjacent target rows.

For example:

```text
noncoding variant
    → regulatory feature
    → linked gene
    → PGERS patient-gene target
```

PGERS must preserve that route.

RFPS-derived evidence should be represented distinctly from direct coding or direct gene annotation evidence.

Recommended RFPS-derived fields include:

```text
regulatory_feature_variant_count
feature_linked_gene_variant_count
promoter_variant_count
enhancer_variant_count
utr_variant_count
splice_region_variant_count
conserved_element_variant_count
rfps_projection_route_summary
rfps_surface_ref
```

PGERS must not treat regulatory feature projection as equivalent to direct coding-gene annotation.

---

## Relationship to CFBS

CFBS owns coordinate-first burden scan signals.

PGERS may reference CFBS results when a patient-gene or patient-locus target overlaps a CFBS candidate interval or window.

PGERS may include:

```text
cfbs_candidate_interval_overlap
cfbs_window_overlap_count
cfbs_burden_signal_present
cfbs_recurrence_signal_present
cfbs_surface_ref
```

PGERS must not recreate CFBS null models, empirical tail probabilities, or scan statistics.

It should reference CFBS outputs.

---

## Relationship to MPLC

MPLC owns matched prior-locus contrast signals.

PGERS may reference MPLC target locus membership or burden context when the patient-gene target belongs to an MPLC target locus or background locus.

PGERS may include:

```text
mplc_target_locus_membership
mplc_background_locus_membership
mplc_burden_context_present
mplc_recurrence_context_present
mplc_surface_ref
```

PGERS must not perform matched prior-locus contrast testing.

It should reference MPLC outputs.

---

## Relationship to EVRS

EVRS owns exact variant / allele recurrence context.

PGERS may summarize EVRS-derived recurrence evidence for variants projected to a patient-gene target.

PGERS may include:

```text
evrs_exact_variant_recurrence_present
evrs_recurrent_variant_count
evrs_recurrent_observation_count
evrs_recurrence_context_label
evrs_surface_ref
```

PGERS must distinguish exact variant recurrence from coordinate-window burden or gene-level burden.

---

## Relationship to RMCS

RMCS owns reasoning and method currency state.

PGERS may include RMCS-derived state fields such as:

```text
surface_generation_id
source_corpus_generation_id
projection_policy_version
input_surface_currency_state
rdgp_reasoning_currency_state
refresh_required
rmcs_surface_ref
```

PGERS should not silently mix current raw evidence with stale downstream reasoning outputs.

---

## Projection Policy

PGERS requires an explicit projection policy.

Recommended policy fields:

```text
pgers_projection_policy_id
pgers_projection_policy_version
source_corpus_generation_id
source_surface_requirements
daughter_surface_dependency_policy
accepted_projection_routes
route_summary_policy
target_gene_identity_policy
target_identity_bridge_policy
coordinate_to_gene_policy
feature_to_gene_policy
known_assertion_rollup_policy
genotype_summary_policy
opportunity_summary_policy
phenotype_prior_summary_policy
conflict_summary_policy
currency_summary_policy
evidence_stratification_policy
counting_policy
filtering_policy
lossiness_policy
summarization_policy
traceability_policy
anti_overclaim_policy
```

Projection policy must declare whether a PGERS row includes:

```text
all evidence projected to a target
only qualifying evidence
only rare evidence
only coding evidence
only RDGP-eligible evidence
only evidence with sufficient identity confidence
```

Silent filtering is prohibited.

Projection policy must also declare whether PGERS is emitting:

```text
a broad evidence rollup
a filtered RDGP-eligible rollup
a known-evidence-focused rollup
a discovery-context rollup
a minimal v1 rollup with unavailable daughter surfaces
```

The rollup mode must be explicit because the same patient-gene target may have
different counts, labels, and limitations under different rollup policies.

---

## Counting Policy

PGERS must distinguish counting units.

Allowed counting units may include:

```text
source_observation
sample_variant_observation
unique_coordinate_variant
unique_variant_entity
variant_gene_membership
feature_gene_membership
known_assertion_membership
sample_gene_target
source_assertion
```

PGERS must not count membership rows as observations unless the counting policy explicitly declares membership-counting behavior.

Example distinction:

```text
One variant observation may map to two transcripts and one gene.

That does not automatically mean three variant observations.
```

The default observation-counting unit for variant-derived PGERS fields should be:

```text
sample_variant_observation
```

unless the counting policy explicitly declares another unit.

```text
PGERS should distinguish at least:

observation_count
    count of sample-specific variant observations

membership_count
    count of projection memberships

unique_coordinate_variant_count
    count of unique coordinate/reference-context variants

unique_variant_entity_count
    count of brokered variant entities

source_assertion_count
    count of preserved source assertions

known_assertion_membership_count
    count of KVPS known-assertion memberships
```

Membership counts may be useful, but they must not be represented as observed
variant counts.

Recommended fields:

```text
counting_policy_id
observation_count
membership_count
unique_variant_count
unique_coordinate_variant_count
source_assertion_count
known_assertion_membership_count
```

---

## Evidence Strata

PGERS should preserve evidence strata.

Recommended strata include:

```text
coding_variant_evidence
noncoding_variant_evidence
splice_region_evidence
regulatory_feature_evidence
known_pathogenicity_evidence
known_benignity_evidence
known_uncertain_or_vus_evidence
phenotype_prior_evidence
genotype_context_evidence
opportunity_context_evidence
conflict_uncertainty_context
target_bridge_context
recurrence_evidence
burden_scan_context
prior_locus_context
```

PGERS may summarize strata, but it must not homogenize them into one unlabeled support class.

---

## Surface Outputs

PGERS should emit two complementary output levels.

### Membership-Level Output

Membership-level output preserves auditability.

Recommended row unit:

```text
sample_id × projected_gene_target_id × contributing_evidence_membership_id
```

Representative fields:

```text
pgers_membership_id
pgers_surface_id
pgers_surface_generation_id
source_corpus_generation_id
pgers_projection_policy_id

patient_id when available
subject_id when available
sample_id
sample_patient_link_status

projected_gene_target_id
projected_gene_target_type
target_namespace
target_label
target_identity_bridge_id
target_identity_bridge_status
target_identity_bridge_lossiness

projection_route
primary_projection_route when declared
contributing_evidence_type
contributing_evidence_id
contributing_surface_id
contributing_surface_type
contributing_surface_generation_id
daughter_surface_dependency_status

source_assertion_id
source_observation_id
sample_variant_observation_id
variant_identity_id
coordinate_identity_id
feature_identity_id
gene_identity_id
known_assertion_membership_id
genotype_observation_id
opportunity_region_id
phenotype_prior_id
conflict_state_id
currency_state_id

bridge_status
lossiness_status
counting_unit
evidence_stratum
traceability_refs
validation_status
anti_overclaim_label
```

### Summary-Level Output

Summary-level output supports efficient RDGP consumption.

Recommended row unit:

```text
sample_id × projected_gene_target_id × projection_policy_id
```

Representative fields:

```text
pgers_summary_id
pgers_surface_id
pgers_surface_generation_id
source_corpus_generation_id
pgers_projection_policy_id

patient_id when available
subject_id when available
sample_id
sample_patient_link_status

projected_gene_target_id
projected_gene_target_type
target_namespace
target_label
canonical_gene_id
source_gene_id
target_identity_bridge_id
target_identity_bridge_status
target_identity_bridge_lossiness

projection_route_summary
primary_projection_route when declared
contributing_projection_routes
route_lossiness_summary

counting_policy_id
observation_count
membership_count
unique_variant_count
unique_coordinate_variant_count
source_assertion_count
known_assertion_membership_count

projected_variant_count
rare_variant_count
coding_variant_count
noncoding_variant_count
splice_region_variant_count
regulatory_feature_variant_count
known_pathogenicity_evidence_count
known_likely_pathogenicity_evidence_count
known_conflicting_pathogenicity_evidence_count
known_vus_or_uncertain_evidence_count
known_benign_or_likely_benign_evidence_count

kvps_strongest_known_evidence_label
genotype_context_available_count
genotype_context_missing_count
heterozygous_like_variant_count
homozygous_alt_like_variant_count
no_call_or_uncertain_genotype_count
genotype_variant_relationship_ready_count
genotype_variant_relationship_unresolved_count
genotype_variant_relationship_ambiguous_count
direct_source_biallelic_relationship_count
resolved_from_multiallelic_record_count
brokered_with_normalization_relationship_count
multiallelic_relationship_resolved_count
multiallelic_relationship_unresolved_count
multiallelic_relationship_not_evaluated_count

paps_prior_present
paps_prior_strength_label
paps_alignment_status
phenotype_scope

opportunity_state
negative_evidence_allowed
absence_interpretation_label

cfbs_context_present
mplc_context_present
evrs_context_present
rfps_context_present

daughter_surface_dependency_summary
input_surface_currency_state
conflict_state
uncertainty_state
review_required
strongest_evidence_state_label
pgers_evidence_label

membership_refs
cues_event_refs
rmcs_currency_refs
anti_overclaim_label
traceability_refs
validation_status
```

The summary-level table is an RDGP consumption surface. It must remain
reconstructable from membership-level PGERS rows and referenced daughter-surface
records. Summary-level fields must not replace daughter-surface authority.

---

## Evidence-State Labels

PGERS should emit evidence-state labels, not prioritization labels.

Recommended labels include:

```text
patient_gene_evidence_present
patient_gene_known_pathogenicity_evidence_present
patient_gene_known_conflicting_evidence_present
patient_gene_known_vus_or_uncertain_evidence_present
patient_gene_known_benign_evidence_present
patient_gene_variant_evidence_present
patient_gene_coding_variant_evidence_present
patient_gene_noncoding_variant_evidence_present
patient_gene_regulatory_feature_evidence_present
patient_gene_only_prior_evidence_present
patient_gene_prior_and_observation_evidence_present
patient_gene_no_observed_variant_with_opportunity
patient_gene_no_observed_variant_without_opportunity
patient_gene_projection_ambiguous
patient_gene_projection_unresolved
patient_gene_conflict_or_uncertainty_present
patient_gene_evidence_not_evaluated
patient_gene_evidence_present_with_limited_traceability
patient_gene_evidence_present_with_lossy_bridge
patient_gene_evidence_present_with_ambiguous_bridge
patient_gene_daughter_surface_unavailable
patient_gene_daughter_surface_not_evaluated
patient_gene_surface_currency_limited
patient_gene_rollup_policy_limited
```

PGERS should not emit labels such as:

```text
high_priority_gene
likely_disease_gene
causal_candidate
diagnostic_candidate
confirmed_gene
solved_case
```

Those belong downstream to RDGP or clinical interpretation.

---

## RDGP Consumption Role

PGERS provides RDGP with a structured patient-gene/locus evidence state.

RDGP may use PGERS to:

```text
identify genes/loci with patient-specific evidence
combine known pathogenicity evidence with genotype context
combine phenotype-scoped priors with observed variant evidence
separate coding and noncoding evidence
recognize regulatory or feature-mediated evidence
inspect evidence conflicts and uncertainty
avoid interpreting absence without opportunity
trace candidate evidence back to source assertions
prepare explanations over patient-gene evidence state
```

RDGP may reason over PGERS.

PGERS itself does not reason.

---

## PGERS Consumption Boundary

PGERS is a consumption plane, not a reasoning layer.

RDGP may use PGERS to organize evidence features, candidate explanations,
ranking inputs, and review queues. PGERS itself must not emit:

```text
rank
priority_score
candidate_status
diagnostic_status
model_fit_status
inheritance_model_result
causal_gene_label
```

If such values appear in VDB later, they must come from RDGP or another
governed reasoning producer and re-enter VDB as new assertions, not as mutations
of PGERS.

---

## Traceability Requirements

Every PGERS row must preserve traceability.

Membership-level rows must trace to:

```text
source Assertion Records
source observations
source identities
projection policies
identity brokerage records
source surfaces where applicable
validation receipts
```

Summary-level rows must trace to the membership-level rows that produced them.

Required invariant:

```text
Every PGERS summary cell must be reconstructable from membership-level
records, source surfaces, and declared policy.
```

A PGERS summary row without reconstructable membership lineage is invalid.

---

## Validation Requirements

PGERS validation should confirm:

```text
pgers_surface_id exists

source_corpus_generation_id exists

projection_policy_id exists

sample_id is present

projected_gene_target_id is present

projection route is declared

bridge status is declared

lossiness status is declared

counting policy is declared

membership-level traceability exists

summary-level rows reconcile to membership-level rows

zero evidence states are supported by OACS or explicitly marked unmodeled

known pathogenicity summaries reconcile to KVPS where available

genotype summaries reconcile to GIRS where available

phenotype-prior summaries reconcile to PAPS where available

conflict summaries reconcile to CUES where available

regulatory-feature summaries reconcile to RFPS where available

CFBS/MPLC/EVRS references are explicit when used

anti-overclaim labels are present

surface limitations are declared

sample identity is not silently collapsed into patient identity

sample_patient_link_status is explicit when patient/subject identity is used

target identity bridge IDs, statuses, and lossiness states are declared

daughter surface dependency status is explicit for each referenced surface

summary rows do not imply evaluation of unavailable or not-evaluated daughter surfaces

membership counts are not represented as observation counts unless explicitly declared

projection route multiplicity is preserved when multiple routes contribute

PAPS-derived phenotype priors retain phenotype scope

RFPS-derived feature context remains distinct from direct gene annotation

RMCS currency state is referenced when current/stale/comparability state is exposed

PGERS evidence labels are not RDGP prioritization labels
```

Validation must not certify biological correctness.

Validation certifies structural integrity, lineage, reconstruction, and policy compliance.

---

## Anti-Overclaim Rules

PGERS must not perform or imply the following unsafe transformations:

```text
gene row treated as causal gene

projected variant evidence treated as gene-level truth

gene-level prior treated as patient observation

sample-gene rollup treated as RDGP score

noncoding variant discarded because gene projection is absent

ambiguous gene bridge treated as exact gene identity

regulatory feature projection treated as direct coding-gene annotation

zero projected variants treated as absence without OACS opportunity state

KVPS known pathogenicity evidence flattened into generic support count

GSC phenotype-scoped prior flattened into generic gene support

genotype state converted into inheritance conclusion

resolved multiallelic genotype-to-variant relationships treated as independent
producer genotype rows

multiple genotype_variant_relationship rows from one genotype observation
treated as multiple source genotype observations

CFBS or MPLC signal converted into disease association

EVRS recurrence converted into causal recurrence

surface summary replacing membership-level traceability

projection row replacing Assertion Record

RDGP result written back into PGERS instead of re-entering VDB as new assertions

sample identity treated as patient identity without declared link

multiple projection routes collapsed into one unlabeled gene support class

lossy target bridge treated as exact gene identity

daughter surface unavailable treated as evaluated no evidence

surface_not_evaluated treated as surface_evaluated_no_membership

membership_count treated as observed variant count

PGERS evidence label treated as RDGP priority label

summary-level rollup treated as replacement for daughter-surface evidence
```

Any implementation that performs these transformations violates PGERS design doctrine.

---

## v1 Minimum Viable Surface

PGERS v1 should be architecture-complete but implementation-realistic.

Minimum v1 inputs:

```text
VAP sample-specific variant observations
VAP gene annotations where available
VDB coordinate/variant/gene brokerage records
GSC phenotype-gene priors where available
KVPS memberships where available
GIRS genotype context where available
OACS opportunity state where available
CUES conflict/uncertainty state where available
source_corpus_generation_id
pgers_surface_generation_id
patient_id when available
sample_patient_link_status when patient/subject identity is used
target_identity_bridge_status
target_identity_bridge_lossiness
daughter_surface_dependency_status
counting_policy_id
membership references
RMCS currency references when available
```

Minimum v1 outputs:

```text
membership-level patient-gene evidence rows
summary-level patient-gene evidence rows
```

Minimum v1 context:

```text
sample_id
projected_gene_target_id
projected_gene_target_type
projection_policy_id
projection_route
source observation references
source assertion references
known evidence references when available
genotype references when available
opportunity references when available
phenotype-prior references when available
conflict references when available
traceability references
anti-overclaim label
validation status
```

Optional but v1-compatible references:

```text
RFPS regulatory/feature projection memberships
CFBS candidate interval or window context
MPLC target/background locus context
EVRS exact variant recurrence context
RMCS currency state
```

PGERS v1 should not require all optional surfaces to be fully implemented before PGERS can emit basic patient-gene rollups.

However, the surface must preserve explicit `not_available`, `not_evaluated`, or `not_applicable` states for absent daughter surfaces.

---

## Future Extensions

Future PGERS versions may add:

```text
richer transcript-specific rollups
locus-level and regulatory domain rollups
protein-domain evidence rollups
pathway-level aggregation references
tissue-context evidence summaries
multi-omics evidence summaries
cohort-aware recurrence summaries
inheritance-model readiness hooks
family-based evidence references
longitudinal evidence state
reasoning-informed returned RDGP evidence references
```

Any future extension must preserve the PGERS boundary:

```text
PGERS rolls up evidence state.
RDGP reasons over evidence state.
```

---

## Non-Goals

PGERS does not define:

```text
RDGP ranking logic
inheritance reasoning
compound heterozygosity detection
de novo detection
ACMG classification
clinical actionability
final candidate-gene prioritization
phenotype matching algorithms
statistical association testing
CFBS implementation
MPLC implementation
KVPS implementation
RFPS implementation
OACS implementation
```

Those belong to daughter surfaces, downstream RDGP, or later implementation specifications.

---

## Summary

PGERS is the TEP-VDB projection surface that rolls patient-specific evidence onto governed gene, locus, or gene-adjacent targets for RDGP consumption while preserving coordinate-derived provenance, projection route, identity-bridge status, genotype context, opportunity context, phenotype-prior context, conflict state, daughter-surface references, and anti-overclaim boundaries.

The core PGERS responsibility is:

```text
Give RDGP a usable patient-gene/locus evidence state
without collapsing VDB into a gene-centered truth store.
```

The core PGERS boundary is:

```text
PGERS exposes patient-gene evidence state.
RDGP evaluates patient-gene evidence state.
Scientists and clinicians interpret evaluated evidence.
```


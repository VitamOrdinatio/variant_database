# EVRS — Exact Variant Recurrence Surface

**Status:** SAGE-VDB projection-surface design draft  
**Intended path:** `docs/design/projection_surfaces/evrs_exact_variant_recurrence_surface.md`  
**Layer:** TEP-VDB projection surface design  
**Surface family:** TEP-VDB unknown-tomorrow diagnostic discovery support surface; exact-variant recurrence substrate  
**Primary consumer:** RDGP and future downstream reasoning systems  
**Parent architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## 1. Purpose

The Exact Variant Recurrence Surface (EVRS) is a TEP-VDB projection surface that exposes recurrence of the same governed variant or allele identity across declared samples, runs, cohorts, phenotype scopes, assay scopes, producer corpora, or TEP-VDB package scopes.

EVRS answers the question:

```text
Does the same governed variant/allele identity recur across samples,
runs, cohorts, phenotypic strata, or evidence contexts under a declared
identity, deduplication, and recurrence policy?
```

EVRS is intentionally narrower than burden, locus, or gene-level projection surfaces. It does not ask whether a gene is enriched for variants, whether a locus has excess burden, or whether a recurrent variant is disease-associated. It exposes exact-variant recurrence as a traceable, policy-declared evidence state for downstream RDGP reasoning.

---

## 2. Core Doctrine

```text
EVRS does not infer disease association from recurrence.

EVRS exposes traceable exact-variant recurrence under declared identity,
deduplication, cohort, assay, and opportunity policies so RDGP can reason
over recurrence without confusing repeated observation with causality.
```

EVRS is a recurrence substrate, not an association test, founder-variant detector, diagnostic claim, pathogenicity classifier, or RDGP score.

---

## 3. Relationship to TEP-VDB Architecture

Within TEP-VDB, EVRS belongs to the discovery-tomorrow projection family while also supporting known-today diagnostic reasoning when recurrent exact variants overlap known pathogenicity evidence.

Conceptual position:

```text
source variant observations
    + governed coordinate / allele identity
    + recurrence scope
    + deduplication policy
    + genotype / quality context
    + opportunity / denominator context
    + conflict / uncertainty state
        ↓
EVRS exact variant recurrence surface
        ↓
RDGP recurrence-aware reasoning
```

EVRS keeps recurrence visible without forcing RDGP to reconstruct exact allele equivalence, sample deduplication, recurrence scopes, or recurrence traceability from raw observations.

---

## 4. Relationship to Mathematical Formalism

Under the VDB mathematical formalism, EVRS is a projection policy over sample-specific variant observations and governed allele identity objects.

```text
θ_EVRS:
    source objects =
        sample-specific variant observations,
        coordinate / allele identity records,
        genotype context,
        genotype-to-variant relationship records,
        multiallelic relationship brokerage state,
        allele-index mapping state when applicable,        
        quality / filter context,
        sample / run / producer identity,
        optional KVPS / PGERS / RFPS / OACS / CUES references

    target objects =
        normalized exact variant identities within declared recurrence scopes

    membership =
        a sample-specific variant observation belongs to a recurrence event if
        it matches the normalized variant identity under declared identity and
        deduplication policy

    opportunity =
        required when interpreting singleton, non-recurrence, recurrence
        denominator completeness, or cross-sample recurrence scope

    geometry =
        exact-allele recurrence counts, recurrence strata, deduplicated
        observation sets, genotype / quality / assay summaries

    surface =
        exact variant recurrence substrate for RDGP
```

Compactly:

```text
S_EVRS = F_EVRS(T_C, M_EVRS, Ω_EVRS, P_EVRS)
```

Where:

```text
T_C      = evidence topology
M_EVRS  = membership operator from sample-specific variant observations
          to normalized variant recurrence events
Ω_EVRS  = opportunity / denominator context for interpreting recurrence scope
P_EVRS  = identity, normalization, deduplication, cohort / scope, counting,
          and labeling policy
```

Required traceability invariant:

```text
Every EVRS recurrence count must trace to the exact sample-specific variant
observations and source assertion records that contributed to it.
```

---

## 5. Scientific Question

EVRS asks:

```text
For a declared recurrence scope, which exact governed variant or allele
identities recur, how many independent observations support each recurrence
state, and what identity, deduplication, genotype, quality, opportunity,
known-evidence, and uncertainty context constrains that recurrence?
```

EVRS does not ask:

```text
Is this recurrent allele pathogenic?
Is this recurrent allele disease-associated?
Is this a founder variant?
Does this recurrence explain the patient phenotype?
Does this recurrence satisfy an inheritance model?
```

Those are downstream reasoning or interpretation questions.

---

## 6. What EVRS Is

EVRS is:

```text
an exact-variant recurrence projection surface

a governed allele-identity recurrence table

a recurrence-scope-aware evidence state

a deduplication-aware observation summary

a recurrence traceability surface

a recurrence context substrate for RDGP
```

EVRS exposes recurrence of the same governed variant identity across declared scopes while preserving source observation references, identity policy, deduplication state, genotype context, quality context, opportunity context, and conflict / uncertainty state.

---

## 7. What EVRS Is Not

EVRS is not:

```text
a disease-association test

a burden scan

a gene-prior surface

a locus-enrichment model

a founder-variant classifier

a pathogenicity classifier

an ACMG interpreter

an inheritance model

a diagnostic report

a population-frequency database

a replacement for KVPS, PGERS, GIRS, OACS, CUES, RFPS, CFBS, MPLC, PAPS,
or RMCS
```

EVRS may reference those surfaces, but it does not absorb their responsibilities.

---

## 8. Core Unit

The core EVRS recurrence unit is:

```text
normalized_variant_identity_id × recurrence_scope_id × recurrence_policy_id
```

The membership-level unit is:

```text
normalized_variant_identity_id × sample_variant_observation_id × recurrence_scope_id
```

A recurrence unit must preserve the allele identity basis, recurrence scope, and recurrence policy. A count without these three pieces is not a governed EVRS recurrence count.

---

## 8A. Sample, Patient, Subject, and Recurrence Unit Boundary

EVRS may use `sample_id` as the practical v1 observation anchor, but recurrence
claims must declare the recurrence unit.

Recommended recurrence units include:

```text
observation
run
sample
patient
subject
family
producer
registration_unit
unknown
not_evaluated
```

For a simple demonstration corpus, `sample` and `patient` may be one-to-one
under source declarations. Generic EVRS schemas must not assume that
relationship silently.

When patient or subject identity is available, EVRS should preserve:

```text
patient_id when available
subject_id when available
sample_id
sample_patient_link_id when available
sample_patient_link_status
recurrence_unit_policy_id
recurrence_unit
```

Recommended `sample_patient_link_status` values include:

```text
same_subject_declared
same_subject_inferred_by_source
sample_patient_link_unavailable
sample_patient_link_ambiguous
sample_patient_link_not_evaluated
```

This prevents EVRS from overstating independent recurrence when the available
substrate only supports run-level, sample-level, or registration-level
recurrence.

A count such as:

```text
unique_sample_count = 3
```

must not be presented as:

```text
unique_biological_subject_count = 3
```

unless biological-subject identity is available and deduplicated under declared
policy.

---

## 9. Exact-Variant-Centered Design

EVRS is exact-variant-centered, not gene-centered.

The central identity should be equivalent to:

```text
reference_genome × contig × position × normalized_ref × normalized_alt
```

plus a VDB-governed variant identity handle.

This distinction is critical:

```text
same exact SNV observed in four samples
    ≠
four different rare variants observed in the same gene
```

The first is EVRS territory. The second is more naturally PGERS, MPLC, CFBS, or downstream RDGP reasoning territory.

---

## 10. Recurrence Scope

A recurrence event is only meaningful inside a declared comparison scope.

EVRS must declare a `recurrence_scope_id` and `recurrence_scope_type`.

Supported conceptual scope types include:

```text
tep_vdb_package_scope
whole_corpus
producer_corpus
sample_cohort
phenotype_scoped_cohort
assay_type_scope
wes_scope
wgs_scope
family_scope
run_batch_scope
case_only_scope
case_control_scope_if_available
registration_generation_scope
```

For v1, the recommended scope types are:

```text
tep_vdb_package_scope
phenotype_scoped_cohort
assay_type_scope
producer_corpus
registration_generation_scope
```

Example distinctions:

```text
variant observed in 3 of 12 epilepsy WES samples
    ≠
variant observed in 3 of 13 mixed WES / WGS samples

variant observed in 3 samples after sample-level deduplication
    ≠
variant observed in 3 runs where two runs may be reprocessings of the same
biological sample
```

EVRS recurrence scope should also declare the denominator universe:

```text
eligible_observation_count
eligible_sample_count
eligible_patient_count when available
eligible_subject_count when available
assay_scope
opportunity_scope
denominator_policy_id
```

The recurrence numerator and denominator must be scoped together. For example,
a recurrence numerator computed across WES samples must not be interpreted
against a mixed WES/WGS or broader package denominator unless the recurrence
policy explicitly declares that comparison.

---

## 11. Deduplication Policy

EVRS recurrence counts are fragile. A recurrence count can be inflated by:

```text
duplicate runs from the same biological sample
technical replicates
same sample processed by multiple pipelines
related individuals
reused public control or sample artifacts
multi-allelic representation differences
left-normalization differences
liftover or reference-build differences
producer-level duplicate assertions
source package re-ingestion
```

EVRS therefore requires:

```text
recurrence_deduplication_policy_id
```

EVRS should emit multiple count classes rather than a single ambiguous count:

```text
observation_count
unique_sample_count
unique_run_count
unique_registration_unit_count
unique_producer_count
unique_assertion_record_count
unique_biological_subject_count_if_available
```

EVRS should distinguish count classes from independence claims.

Recommended additional fields:

```text
recurrence_count_unit
independence_assumption
independence_status
relatedness_status when available
deduplication_limitation
```

Recommended `independence_status` values include:

```text
independent_subjects_declared
independent_samples_declared
independence_unknown
relatedness_possible
relatedness_not_evaluated
```

EVRS may expose recurrence counts under declared deduplication policy, but it
must not imply statistical independence unless independence is supported by the
available substrate.

If biological-subject identity is unavailable, EVRS must say so explicitly:

```text
biological_subject_deduplication_status = unavailable
```

Sample-level deduplication must not masquerade as biological-subject deduplication.

---

## 12. Variant Identity and Match Classes

Strong EVRS recurrence requires strict allele identity.

Recommended eligible exact recurrence identity requirements:

```text
same reference build
same contig
same normalized coordinate
same normalized reference allele
same normalized alternate allele
same variant class under policy
```

EVRS should emit an `identity_match_class` such as:

```text
exact_normalized_allele_match
exact_coordinate_allele_match
equivalent_normalized_representation
ambiguous_normalization_match
build_lifted_match
source_identifier_match_only
gene_only_match_not_allowed
unresolved_variant_identity
```

For v1, recurrence counts should be considered strong only for:

```text
exact_normalized_allele_match
exact_coordinate_allele_match
equivalent_normalized_representation
```

Other identity classes may be surfaced as limitations or CUES events, but they should not be silently counted as exact recurrence.

Core anti-collapse rule:

```text
A gene-level match is not exact variant recurrence.
```

---

## 13. Variant-Class Scope

Exact recurrence is most straightforward for SNVs and small indels. Other variant classes require specialized identity models.

EVRS must emit:

```text
variant_class
identity_model
normalization_model
variant_class_support_status
```

Recommended v1 support posture:

```text
SNV and small-indel recurrence are supported when normalized coordinate /
allele identity is available.

CNV, SV, STR, repeat-expansion, mobile-element, and complex-event recurrence
are out of scope or separately labeled as not modeled unless explicit identity
policies exist.
```

Required unsupported-state examples:

```text
cnv_exact_recurrence_not_modeled
sv_exact_recurrence_not_modeled
str_exact_recurrence_not_modeled
repeat_expansion_recurrence_not_modeled
complex_event_recurrence_not_modeled
```

Silent not-modeled behavior is not allowed.

---

## 13A. EVRS Projection Policy

EVRS requires an explicit projection policy.

Recommended policy fields:

```text
evrs_projection_policy_id
evrs_projection_policy_version
source_corpus_generation_id
recurrence_scope_policy_id
recurrence_unit_policy_id
identity_policy_id
allele_normalization_policy_id
variant_class_support_policy_id
deduplication_policy_id
counting_policy_id
genotype_summary_policy_id
genotype_variant_relationship_policy_id
multiallelic_relationship_policy_id
allele_index_mapping_policy_id
genotype_relationship_state_policy_id
quality_summary_policy_id
frequency_context_policy_id
oacs_reference_policy_id
denominator_readiness_policy_id
kvps_reference_policy_id
girs_reference_policy_id
paps_reference_policy_id
rfps_reference_policy_id
pgers_reference_policy_id
cues_reference_policy_id
rmcs_reference_policy_id
traceability_policy_id
anti_overclaim_policy_id
```

The EVRS projection policy must declare:

```text
which variant classes are eligible for exact recurrence

which identity model defines exact recurrence

which normalization model is used

which recurrence scopes are evaluated

which recurrence unit is counted

how duplicate runs, samples, registration units, producer records, related
subjects, and unavailable subject identity are handled

which genotype, quality, frequency, opportunity, and known-evidence contexts
are summarized

when singleton or non-recurrence labels may be emitted

which denominator readiness state is required for non-recurrence interpretation

which claims are prohibited
```

Silent identity broadening, silent deduplication, silent recurrence-unit changes,
silent unsupported-variant-class omission, and silent denominator substitution
are prohibited.

---

## 14. Relationship to KVPS

KVPS owns known variant pathogenicity evidence attachment.

EVRS may overlay KVPS context, such as:

```text
kvps_evidence_present
kvps_strongest_known_evidence_label
kvps_conflict_state
kvps_membership_refs
```

But EVRS must not re-adjudicate pathogenicity.

Safe statement:

```text
This recurrent exact allele overlaps known pathogenicity evidence exposed by
KVPS.
```

Unsafe statement:

```text
This recurrence confirms pathogenicity.
```

---

## 15. Relationship to PGERS

PGERS may consume EVRS as a gene or locus rollup feature.

Example PGERS-compatible summary:

```text
this patient-gene target contains a variant observed recurrently in the
corpus under EVRS policy
```

PGERS should preserve EVRS references rather than flattening exact recurrence into generic gene support.

Recommended PGERS fields:

```text
evrs_exact_variant_recurrence_refs
exact_recurrent_variant_count
exact_recurrence_strongest_label
```

with source EVRS traceability retained.

---

## 16. Relationship to GIRS

GIRS owns genotype and inheritance-readiness context.

EVRS may summarize genotype states across recurrent observations:

```text
heterozygous_like_observation_count
homozygous_alt_like_observation_count
hemizygous_like_observation_count
multi_alt_like_observation_count
genotype_missing_count
low_quality_genotype_count
```

EVRS must not infer:

```text
dominant recurrence
recessive recurrence
compound heterozygous recurrence
segregating recurrence
carrier frequency
```

Genotype recurrence summaries remain structural context. RDGP evaluates inheritance models.

---

## 17. Relationship to OACS

OACS provides opportunity and denominator context.

EVRS must coordinate with OACS when interpreting singleton status, non-recurrence, or recurrence denominator completeness.

Example risk:

```text
variant observed in only one sample
```

may mean:

```text
true singleton in a well-observed scope
not assayed in other samples
not callable in other samples
different assay scope
low opportunity in relevant regions
unknown opportunity
```

EVRS should therefore emit:

```text
recurrence_denominator_readiness
oacs_surface_ref
```

Recommended denominator readiness states:

```text
recurrence_denominator_available
recurrence_denominator_limited
recurrence_denominator_not_available
recurrence_denominator_unknown
```

EVRS must not treat singleton or non-recurrence as meaningful without OACS-compatible denominator context.

EVRS should distinguish recurrence from non-recurrence readiness.

Recommended fields:

```text
recurrence_denominator_readiness
non_recurrence_interpretation_label
singleton_interpretation_label
eligible_denominator_count
denominator_limitation
```

Recommended `non_recurrence_interpretation_label` values include:

```text
non_recurrence_interpretable_under_policy
non_recurrence_not_interpretable_limited_opportunity
non_recurrence_not_interpretable_mixed_assay_scope
non_recurrence_not_interpretable_unknown_denominator
non_recurrence_not_evaluated
```

Singleton or non-recurrence labels must not be interpreted as absence of disease
evidence without OACS-compatible denominator context.


---

## 18. Relationship to CUES

CUES indexes conflict, uncertainty, ambiguity, missingness, staleness, and limitations.

EVRS should emit or reference CUES events for:

```text
ambiguous variant identity
normalization conflict
reference build mismatch
duplicate sample suspected
batch-specific recurrence
low-quality recurrent observations
known artifact region
opportunity denominator unknown
frequency unexpectedly common
source assertion duplication
sample identity unresolved
```

EVRS may expose local conflict summaries, but CUES owns package-level epistemic event indexing.

---

## 19. Relationship to CFBS and MPLC

EVRS is not a burden scan.

```text
EVRS:
    same exact allele recurs

CFBS:
    coordinate windows show excess variant concentration

MPLC:
    prior-informed loci show excess burden relative to matched loci
```

A recurrent exact allele may contribute to a CFBS or MPLC burden signal, but EVRS does not test enrichment. Conversely, CFBS and MPLC may detect burden from multiple different variants without exact allele recurrence.

---

## 20. Relationship to RFPS

RFPS provides feature projection context.

EVRS may include RFPS references showing where recurrent variants project:

```text
coding exon
splice region
UTR
promoter
enhancer
conserved noncoding element
regulatory-linked feature
```

Recommended EVRS field:

```text
rfps_feature_projection_refs
```

EVRS must not infer molecular mechanism from feature membership. RFPS supplies feature projection; RDGP reasons over biological implication.

---

## 20A. Relationship to PAPS

PAPS owns phenotype alignment and phenotype-scoped prior context.

EVRS may reference PAPS when a recurrent exact variant projects to a target
with phenotype-scoped prior context.

EVRS may include PAPS-derived context such as:

```text
paps_surface_ref
paps_prior_refs
phenotype_scope
phenotype_scope_alignment_status
phenotype_prior_context_label
```

PAPS context must not convert exact recurrence into phenotype fit, disease
association, causality, or diagnosis.

Safe statement:

```text
This recurrent exact allele projects to a target with phenotype-scoped prior
context exposed by PAPS.
```

Unsafe statement:

```text
This recurrent exact allele is phenotype-matched disease evidence.
```

---

## 20B. Relationship to RMCS

RMCS owns method, dependency, currency, validation, refresh, and comparability
state.

EVRS should expose RMCS references when recurrence state depends on:

```text
recurrence policy
identity policy
normalization policy
deduplication policy
recurrence scope
source corpus generation
assay scope
opportunity denominator policy
supported variant-class policy
surface validation state
```

An EVRS surface generated under a different identity, normalization,
deduplication, recurrence-scope, source-corpus, assay-scope, or denominator
policy should not be compared to another EVRS surface without RMCS comparability
state.

Recommended field:

```text
rmcs_currency_refs
```

RMCS should not replace EVRS recurrence traceability. It only declares whether
the recurrence surface or prior recurrence result remains current, stale,
superseded, incomparable, or refresh-required under declared dependencies.

---

## 21. Relationship to External Population Frequency

EVRS recurrence is internal and scope-bound. It is not the same as external population allele frequency.

EVRS may include frequency context:

```text
external_frequency_source
external_allele_frequency
frequency_bin
rare_under_policy
common_under_policy
frequency_missing
frequency_conflict_state
```

But the conceptual separation must remain:

```text
EVRS recurrence_count = recurrence within declared VDB scope.

External allele frequency = population/resource context from outside the
declared VDB recurrence scope.
```

A common variant can recur. Recurrence alone does not imply pathogenicity.

---

## 22. Output 1 — Recurrence Membership Table

The EVRS recurrence membership table emits one row per:

```text
normalized_variant_identity_id × sample_variant_observation_id × recurrence_scope_id
```

The membership table should use a stable membership-row identifier, distinct
from the recurrence-event identifier:

```text
evrs_membership_id
```

The recurrence event itself should be represented by:

```text
evrs_recurrence_event_id
```

A recurrence event may have many membership rows.

Recommended fields:

```text
evrs_membership_id
evrs_recurrence_event_id
evrs_surface_id
evrs_surface_generation_id
source_corpus_generation_id
evrs_projection_policy_id

normalized_variant_identity_id
coordinate_variant_handle
sample_variant_observation_id
genotype_observation_id when available
genotype_variant_relationship_id when applicable
genotype_variant_relationship_state when applicable
relationship_derivation_policy_id when applicable
allele_index when applicable
source_alt_allele when applicable
relationship_ambiguity_state when applicable
relationship_lossiness_state when applicable
identity_registration_state when applicable

sample_id
patient_id when available
subject_id when available
sample_patient_link_status when applicable
run_id
registration_unit_id
assertion_id
source_assertion_key
producer_family

reference_genome
contig
position
normalized_ref
normalized_alt
variant_class
identity_match_class
identity_policy_id
normalization_model
normalization_policy_id
variant_class_support_status

normalized_genotype_state
quality_state
filter_state
assay_type

recurrence_scope_id
recurrence_scope_type
recurrence_scope_label
recurrence_policy_id
recurrence_unit
recurrence_unit_policy_id
deduplication_policy_id
deduplication_status
biological_subject_deduplication_status
independence_status

oacs_surface_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable
traceability_refs
anti_overclaim_label
```

This table preserves auditability of every observation contributing to recurrence.

---

## 23. Output 2 — Recurrence Summary Table

The EVRS recurrence summary table emits one row per:

```text
normalized_variant_identity_id × recurrence_scope_id × recurrence_policy_id
```

The summary table should use:

```text
evrs_recurrence_event_id
```

as the stable event identifier. This identifier must be reconstructable from
the normalized variant identity, recurrence scope, recurrence policy,
deduplication policy, and surface generation.


Recommended fields:

```text
evrs_recurrence_event_id
evrs_surface_id
evrs_surface_generation_id
source_corpus_generation_id
evrs_projection_policy_id

normalized_variant_identity_id
coordinate_variant_handle
variant_label
reference_genome
contig
position
normalized_ref
normalized_alt
variant_class
identity_match_class
identity_policy_id
normalization_policy_id
variant_class_support_status

recurrence_scope_id
recurrence_scope_type
recurrence_scope_label
recurrence_policy_id
recurrence_unit
recurrence_unit_policy_id
deduplication_policy_id

observation_count
unique_sample_count
unique_run_count
unique_registration_unit_count
unique_producer_count
unique_assertion_record_count
unique_patient_count_if_available
unique_biological_subject_count_if_available
biological_subject_deduplication_status
independence_status
deduplication_limitation

eligible_sample_count
eligible_patient_count_if_available
eligible_subject_count_if_available
denominator_policy_id
recurrence_denominator_readiness
oacs_denominator_readiness
oacs_surface_refs

genotype_state_summary
genotype_variant_relationship_state_summary
direct_source_biallelic_observation_count
resolved_from_multiallelic_record_observation_count
brokered_with_normalization_observation_count
ambiguous_genotype_variant_relationship_count
unresolved_genotype_variant_relationship_count
relationship_not_evaluated_observation_count
quality_state_summary
filter_state_summary
assay_type_summary
frequency_context

kvps_evidence_summary
kvps_membership_refs
girs_membership_refs
paps_context_refs when applicable
pgers_target_refs
rfps_feature_projection_refs
cfbs_context_refs when applicable
mplc_context_refs when applicable

cues_conflict_uncertainty_state
cues_event_refs
rmcs_currency_refs

recurrence_evidence_label
anti_overclaim_label
membership_refs
traceability_refs
limitations
```

This table is the primary RDGP consumption view and must remain reconstructable
from membership-level rows.

---

## 24. Output 3 — Package-Level Recurrence Summary

The EVRS package-level summary emits one row per EVRS surface generation.

Recommended fields:

```text
evrs_surface_id
surface_type
surface_version
surface_generation_id
source_corpus_id
source_corpus_generation_id
evrs_projection_policy_id
recurrence_policy_id
recurrence_unit_policy_id
deduplication_policy_id
identity_policy_id
normalization_policy_id
denominator_policy_id
supported_variant_classes
unsupported_variant_classes
recurrence_scope_count
recurrent_variant_count
singleton_variant_count
identity_ambiguous_variant_count
quality_limited_recurrence_count
denominator_limited_recurrence_count
deduplication_limited_recurrence_count
independence_unknown_recurrence_count
unsupported_variant_class_count
cues_event_count
rmcs_currency_state
validation_status
limitations
anti_overclaim_label
traceability_refs
```

This table supports surface QA, package inspection, and RDGP preflight checks
without replacing membership-level recurrence traceability.

---

## 25. EVRS Evidence Labels

EVRS labels must be descriptive, not inferential.

Allowed evidence-state labels:

```text
exact_variant_recurrence_observed
exact_variant_singleton_observed
exact_variant_recurrence_denominator_limited
exact_variant_recurrence_identity_ambiguous
exact_variant_recurrence_quality_limited
exact_variant_recurrence_batch_limited
exact_variant_recurrence_not_evaluated
exact_variant_recurrence_with_known_pathogenicity_evidence
exact_variant_recurrence_with_conflict_or_uncertainty
exact_variant_recurrence_observed_with_limited_deduplication
exact_variant_recurrence_observed_with_unknown_independence
exact_variant_recurrence_observed_with_mixed_assay_scope
exact_variant_singleton_denominator_limited
exact_variant_recurrence_variant_class_not_modeled
exact_variant_recurrence_scope_not_evaluated
```

Disallowed generated labels:

```text
disease_associated_recurrent_variant
causal_recurrent_variant
founder_variant
diagnostic_recurrence
pathogenic_recurrence_confirmed
recurrent_epilepsy_variant
```

Such interpretive labels may only appear if preserved as source assertions from an upstream producer, and even then EVRS must expose them as source claims, not EVRS conclusions.

---

## 26. RDGP Consumption Role

RDGP may consume EVRS as:

```text
exact recurrence feature substrate
recurrent-variant explanation substrate
known-evidence recurrence overlay substrate
phenotype-scoped recurrence context
quality-aware recurrence context
denominator-aware recurrence context
conflict-aware recurrence context
```

RDGP may reason over recurrence in combination with:

```text
KVPS known pathogenicity evidence
PGERS patient-gene rollups
GIRS genotype readiness
OACS opportunity context
CUES uncertainty state
RFPS feature projection context
PAPS phenotype-prior context
CFBS / MPLC burden surfaces
```

EVRS itself does not generate RDGP priorities.

---

## 27. Traceability Requirements

Every EVRS recurrence count must preserve traceability to contributing observations.

Minimum traceability:

```text
sample_variant_observation_id
sample_id
run_id
registration_unit_id
assertion_id
source_assertion_key
producer_family
source coordinate / allele representation
normalized coordinate / allele representation
identity policy
normalization policy
recurrence policy
deduplication policy
recurrence scope
surface generation
```

Summary rows must trace back to membership rows. Membership rows must trace back to source Assertion Records or explicit source observation records.

---

## 28. Validation Requirements

EVRS validation should confirm:

```text
every recurrence summary count equals the set of traceable membership rows

identity_match_class is declared for every membership row

reference genome / contig / position / ref / alt are present or explicitly
unresolved

deduplication policy is declared

recurrence scope is declared

sample-level counts do not masquerade as biological-subject counts

unsupported variant classes are explicitly labeled

singleton and non-recurrence labels carry denominator readiness state

low-quality or ambiguous identity rows are not silently counted as strong exact
recurrence

CUES events are emitted for identity ambiguity, deduplication limitation,
quality limitation, and denominator limitation where applicable

summary rows preserve traceability to membership rows

membership rows use `evrs_membership_id` and summary rows use
`evrs_recurrence_event_id`

recurrence unit is declared for every recurrence count

sample, patient, subject, run, producer, and registration-unit counts are not
silently conflated

sample_patient_link_status is explicit when patient or subject identity is used

independence_status is explicit when recurrence is interpreted across samples,
patients, or subjects

denominator readiness is present for singleton or non-recurrence labels

OACS references are present when recurrence denominator or non-recurrence
interpretation is exposed

RMCS references are present when currency, comparability, or refresh state is
exposed

PAPS references preserve phenotype scope when phenotype-prior context is exposed

EVRS summary rows remain reconstructable from EVRS membership rows and do not
replace KVPS, GIRS, PAPS, RFPS, PGERS, CFBS, or MPLC authority
```

---

## 29. v1 Minimum Viable EVRS

Supported in v1:

```text
SNV and small indel exact recurrence
reference-build-aware coordinate / ref / alt identity
normalized allele identity where available
sample-level deduplication
run / registration-unit traceability
genotype / quality summary from GIRS where available
known-evidence overlay from KVPS where available
opportunity denominator readiness from OACS where available
conflict / uncertainty state from CUES where available
membership-level recurrence output
summary-level recurrence output
package-level recurrence summary
```

Not required in v1:

```text
SV / CNV / STR exact recurrence
repeat-expansion recurrence
complex-event recurrence
founder inference
case-control association
ancestry-aware recurrence
family segregation recurrence
biological-subject deduplication when unavailable
cross-reference-build equivalence unless policy exists
```

Unavailable features must be explicitly labeled, not silently omitted.

---

## 30. Anti-Overclaim Rules

EVRS must enforce the following rules:

```text
recurrence is not disease association

same gene is not same exact variant recurrence

same amino-acid consequence is not exact allele recurrence

source identifier match is not coordinate / allele identity unless governed by
policy

build-lifted approximate match is not exact recurrence unless declared by
policy and labeled accordingly

duplicate runs must not be counted as independent samples without declared
deduplication status

family-related samples must not be treated as independent biological subjects
without disclosure

batch-specific recurrence must not be hidden

low-quality recurrent observations must not be counted without quality state

common population variants must not be treated as disease recurrence solely
because they recur

singleton status must not be treated as non-recurrence evidence without OACS
denominator context

EVRS recurrence count is not an RDGP score

EVRS summary rows must not replace membership-level traceability

sample recurrence treated as patient recurrence without declared linkage

patient recurrence treated as independent-subject recurrence without declared
deduplication and independence status

singleton treated as meaningful non-recurrence without denominator readiness

mixed WES/WGS recurrence scope interpreted without assay-scope policy

phenotype-scoped recurrence context treated as phenotype fit

PAPS prior context treated as recurrence causality

EVRS recurrence label treated as RDGP priority label

EVRS recurrence count compared across surfaces without RMCS comparability state

multiple genotype_variant_relationship rows from one genotype_observation_id
treated as multiple independent source genotype observations

resolved_from_multiallelic_record treated as direct_source_biallelic

multiallelic-derived exact allele recurrence treated as producer-emitted
biallelic recurrence without relationship-state disclosure

unresolved genotype-to-variant relationship treated as exact recurrence absence
```

---

## 31. Invalid EVRS Patterns

Invalid patterns include:

```text
gene-level recurrence table labeled as exact variant recurrence

variant recurrence counted without reference genome

variant recurrence counted without ref / alt identity

multi-allelic records collapsed without normalization policy

biological-subject uniqueness assumed from sample identifiers

run count reported as sample count

exact recurrence inferred from gene symbol, transcript, protein effect, or
clinical label alone

ambiguous variant identity counted as exact recurrence

external population frequency treated as VDB recurrence count

VDB recurrence count treated as population allele frequency

known pathogenicity overlap treated as recurrence pathogenicity confirmation

EVRS output written back as source assertion instead of preserved as a
projection surface

recurrence_event_id reused as membership-row identifier

recurrence count emitted without recurrence unit

sample identifiers treated as biological-subject identifiers

recurrent exact allele promoted to CFBS/MPLC burden signal without preserving
EVRS membership traceability

PAPS phenotype-prior context used to label recurrence as phenotype-matched
disease recurrence

RMCS stale or incomparable EVRS surface consumed as current

unsupported variant class omitted without explicit unsupported-state label
```

---

## 32. Strategic Value

EVRS gives TEP-VDB a precise recurrence primitive.

Without EVRS, RDGP must reconstruct recurrence by scanning raw variant observations and deciding allele equivalence, normalization, recurrence scope, deduplication, and traceability itself.

With EVRS, VDB exposes:

```text
Here is the exact allele.

Here are all sample-specific observations of it.

Here is the declared recurrence scope.

Here is the deduplication policy.

Here are genotype, quality, known-evidence, opportunity, and conflict contexts.

Now RDGP may reason.
```

That division of labor preserves VDB as an evidence integration and projection engine while keeping disease association, prioritization, and interpretation downstream.

---

## 33. Summary Doctrine

```text
EVRS is the TEP-VDB projection surface that exposes exact normalized
variant / allele recurrence across declared sample, corpus, phenotype, assay,
and producer scopes while preserving identity policy, deduplication state,
sample / run provenance, genotype and quality context, known-evidence overlays,
opportunity denominator readiness, conflict state, and anti-overclaim
boundaries so RDGP can reason over recurrence without treating repeated
observation as causality or disease association.
```


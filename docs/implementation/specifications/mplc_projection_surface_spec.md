# MPLC Projection Surface Specification

> Status: DEX-VDB implementation specification.
> This document derives from the SAGE-VDB MPLC method design, the
> opportunity-space specification, the projection-policy registry
> specification, and the shared TEP-VDB projection-surface schema.
> It defines the required logical artifacts, fields, policies, validation
> checks, and anti-overclaim boundaries for a VDB-emitted MPLC projection
> surface. It is not an implementation plan, builder contract, or RDGP scoring
> specification.

---

## 1. Purpose

The Matched Prior-Locus Contrast (MPLC) projection surface is a
method-specific reasoning room inside a VDB-emitted TEP-VDB package.

Its purpose is to let RDGP reason over a traceable, VDB-integrated surface that
asks:

```text
Do phenotype-scoped GSC-prior loci carry more local qualifying variant burden
than matched non-prior background loci under the same patient, assay,
opportunity, and filtering context?
```

MPLC is prior-informed. GSC defines the target-locus substrate. VAP-derived
coordinate observations provide patient variant evidence. VDB integrates,
normalizes, projects, and emits the reason-ready surface. RDGP consumes the
surface without independently re-ingesting VAP or GSC producer packages.

> MPLC may emit `exploratory_empirical_p_value` as an empirical tail probability
> under the declared matched-background locus null. This value is useful for
> ranking and hypothesis generation, but it must not be interpreted as a
> control-matched disease-association p-value.

---

## 2. Scope

This specification defines:

```text
MPLC method-surface boundaries
required MPLC policy stack
required MPLC logical artifacts
required and optional fields by artifact
controlled vocabularies
counting and identity rules
target-locus rules
background-matching rules
null-model rules
result-labeling rules
validation rules
failure modes
```

This specification applies to MPLC surfaces emitted inside:

```text
docs/implementation/schemas/tep_vdb_projection_surface_schema.md
```

---

## 3. Non-Goals

This specification does not define:

```text
generic TEP-VDB package layout
generic opportunity-space semantics
generic projection-policy registry semantics
RDGP scoring logic
RDGP diagnosis logic
MPLC builder implementation order
Python module names
database migrations
fixture construction plans
system contracts
implementation plans
```

Those concerns belong to their own schemas, specifications, contracts, or plans.

---

## 4. Method Invariant

MPLC preserves the following invariant:

```text
GSC-prior locus status selects the target set.
Matched non-prior loci define the empirical background.
VAP-derived sample-specific coordinate observations define countable evidence.
Opportunity space defines denominator support.
Projection policies define how observations enter locus windows.
Null models define exploratory empirical comparison.
RDGP receives a reason-ready surface, not raw producer packages.
```

MPLC must not collapse this chain into:

```text
variant → gene → score
```

MPLC is a projection and contrast surface. It is not causal inference, diagnosis,
or formal disease association testing.

---

## 5. Relationship to the Shared TEP-VDB Schema

The MPLC surface is a method room inside the shared TEP-VDB projection-surface
schema.

The shared schema owns:

```text
TEP-VDB envelope
source corpus index
shared substrate index
projection surface index
method-surface manifest shape
validation receipt containers
source traceability containers
demonstration-profile boundaries
```

This MPLC specification owns only the MPLC method room:

```text
projection_surfaces/
    mplc/
        mplc_analysis_scope
        target_locus_set
        background_locus_pool
        matched_locus_sets
        sample_locus_burden_matrix
        patient_locus_hit_matrix
        variant_locus_memberships
        null_draw_manifest
        mplc_results
        mplc_validation_receipts
```

The shared schema must remain generic. The first epilepsy demonstration may use
a 14-source profile, but this MPLC specification must not hard-code that source
count as a universal requirement.

---

## 6. Relationship to Opportunity Space

MPLC requires denominator support for any burden, burden-rate, recurrence-rate,
or observed-versus-background comparison.

MPLC references, but does not redefine:

```text
opportunity_model_id
opportunity_model_version
opportunity_basis_kind
opportunity_state
burden_readiness_status
```

Those are defined by:

```text
docs/implementation/specifications/opportunity_space_spec.md
```

MPLC may emit exploratory surfaces with approximate denominator support only if
the approximation is explicit.

MPLC must not declare a burden-ready surface when:

```text
opportunity_model_id is missing
opportunity_state is unknown and unqualified
opportunity_basis_kind is observed_variants_only
burden_readiness_status is not_burden_ready
burden_readiness_status is denominator_unavailable
```

If opportunity accounting is unavailable, MPLC may preserve the surface as
evidence, but it must label the surface as not burden-ready or exploratory-only.

---

## 7. Relationship to the Projection Policy Registry

MPLC requires declared policies for target selection, locus-window construction,
background matching, variant filtering, opportunity use, null generation, and
emission.

MPLC references, but does not redefine, registered policy semantics from:

```text
docs/implementation/specifications/projection_policy_registry_spec.md
```

Every policy-generated MPLC object must preserve:

```text
policy_id
policy_version
policy_class
source_substrate
target_substrate
lossiness_state
reversibility_state
traceability_requirement
```

MPLC must not use unversioned or implicit projection rules.

---

## 8. Required MPLC Policy Stack

Each MPLC surface must declare the following policy identifiers in
`mplc_analysis_scope`:

```text
target_locus_policy_id
background_matching_policy_id
window_policy_id
variant_filter_policy_id
opportunity_model_id
null_model_id
emission_policy_id
```

Recommended additional policy identifiers:

```text
phenotype_scope_policy_id
frequency_filter_policy_id
variant_class_partition_policy_id
anti_overclaim_policy_id
```

Minimum v1 policy examples may include:

```text
gene_body_plus_10kb_v1
matched_non_prior_background_loci_v1
rare_variant_filter_v1
ultra_rare_variant_filter_v1
sample_specific_locus_opportunity_v1
matched_background_empirical_null_v1
mplc_surface_emission_v1
```

These names are examples of policy registry entries. They are not executable
builder names.

---

## 9. Required Logical Artifacts

An MPLC projection surface must include the following logical artifacts.

```text
mplc_analysis_scope
target_locus_set
background_locus_pool
matched_locus_sets
sample_locus_burden_matrix
patient_locus_hit_matrix
variant_locus_memberships
null_draw_manifest
mplc_results
mplc_validation_receipts
```

A TEP-VDB implementation may serialize these artifacts as TSV, JSON, Parquet, or
another declared format, but the logical content and validation semantics must
be preserved.

---

## 10. `mplc_analysis_scope`

### Purpose

Defines the identity, corpus, policy stack, opportunity basis, and null basis of
the MPLC surface.

### Required Fields

```text
mplc_surface_id
tep_vdb_id
source_corpus_id
method_id
method_version
surface_schema_id
surface_schema_version
genome_build
target_locus_policy_id
background_matching_policy_id
window_policy_id
variant_filter_policy_id
opportunity_model_id
null_model_id
emission_policy_id
number_of_null_draws
random_seed
burden_readiness_status
interpretation_scope
anti_overclaim_label_set
created_at_utc
```

### Recommended Optional Fields

```text
phenotype_scope_policy_id
frequency_filter_policy_id
variant_class_partition_policy_id
opportunity_model_version
projection_policy_registry_id
assertion_record_build_id
topology_build_id
geometry_build_id
demonstration_profile_id
notes
```

### Controlled Values

`method_id` should be:

```text
mplc
```

`interpretation_scope` should be one of:

```text
exploratory_prior_locus_contrast
hypothesis_generating_prior_locus_burden
method_validation_surface
diagnostic_or_association_claim_prohibited
```

---

## 11. `target_locus_set`

### Purpose

Defines phenotype-scoped GSC-prior loci selected as MPLC targets.

### Required Fields

```text
target_set_id
target_locus_id
phenotype_scope
target_locus_policy_id
gsc_release_id
semantic_prior_id
gsc_prior_source
gsc_prior_score
gsc_prior_rank
gsc_prior_tier
gene_namespace
gene_id
gene_symbol
gene_biotype
chromosome
window_start
window_end
window_policy_id
genome_build
source_gsc_trace
included_status
exclusion_reason
```

### Recommended Optional Fields

```text
gsc_contribution_trace
gsc_evidence_class
gsc_confidence_label
canonical_transcript_id
locus_length_bases
target_window_length_bases
target_window_anchor
notes
```

### Rules

Target loci must be phenotype-scope aware.

Epilepsy and mitochondrial-disease GSC priors may coexist in the same TEP-VDB,
but MPLC must not silently merge them into one target set unless an explicit
projection policy declares that combined view.

GSC prior status is not causal truth. It is a phenotype-scoped prior substrate.

---

## 12. `background_locus_pool`

### Purpose

Defines eligible non-prior candidate loci for matched empirical background
construction.

### Required Fields

```text
background_pool_policy_id
background_locus_id
gene_namespace
gene_id
gene_symbol
gene_biotype
chromosome
window_start
window_end
window_policy_id
genome_build
matching_feature_values
eligibility_status
matching_eligible
excluded_from_target_set
excluded_due_to_gsc_prior
excluded_due_to_overlap_with_target_window
exclusion_reason_if_any
```

### Recommended Optional Fields

```text
locus_length_bases
window_length_bases
callable_bases_summary
gc_bin
cpg_bin
mappability_bin
repeat_fraction_bin
gnomad_density_bin
wes_capture_overlap_bin
constraint_bin
matching_feature_version
notes
```

### Rules

Background loci must be matched non-prior loci.

They must not be described as:

```text
non-disease genes
negative-control disease genes
benign loci
```

If a background locus overlaps a target locus window, belongs to the same
phenotype-scoped GSC prior set, or fails matching eligibility, it must be
excluded or explicitly flagged.

---

## 13. `matched_locus_sets`

### Purpose

Records the matched background locus selected for each target locus in each null
draw.

### Required Fields

```text
draw_id
target_locus_id
matched_background_locus_id
replacement_status
matching_rank
matching_distance
matching_features_used
matching_feature_summary
random_seed
background_matching_policy_id
```

### Recommended Optional Fields

```text
matching_failure_reason
fallback_matching_status
matched_with_replacement
stratum_id
chromosome_matching_status
opportunity_matching_status
notes
```

### Rules

Every null draw must preserve the target-set cardinality unless explicitly
declared otherwise.

If the real target set has `N` target loci, each complete background draw should
select `N` matched non-prior loci, subject to declared replacement rules.

Matching failures must be explicit. Silent replacement with arbitrary loci is
not allowed.

---

## 14. `sample_locus_burden_matrix`

### Purpose

Defines sample-specific qualifying variant burden and opportunity support for
each locus window.

### Required Fields

```text
sample_id
locus_id
locus_role
burden_count
rare_burden_count
ultra_rare_burden_count
noncoding_burden_count
coding_burden_count
splice_burden_count
callable_bases
burden_per_callable_base
no_call_bases
not_assayed_bases
opportunity_model_id
opportunity_state
burden_readiness_status
variant_filter_policy_id
window_policy_id
```

### Recommended Optional Fields

```text
genotype_available_count
heterozygous_count
homozygous_count
hemizygous_count
compound_heterozygous_candidate_count
dosage_weighted_burden
low_confidence_bases
unknown_opportunity_bases
filtered_bases
quality_partition_summary
frequency_partition_summary
notes
```

### Controlled Values

`locus_role` should be one of:

```text
target
background
matched_background
excluded
```

### Rules

Burden counts must operate over sample-specific coordinate observations.

Burden counts must not count duplicated transcript rows, feature mappings,
annotation overlays, or GSC overlap rows as separate observed variants.

`burden_per_callable_base` must not be computed when `callable_bases` is zero,
missing, unknown, or declared unavailable.

---

## 15. `patient_locus_hit_matrix`

### Purpose

Defines recurrence of qualifying hits across patients and loci without allowing
one high-burden sample to dominate the entire surface.

### Required Fields

```text
sample_id
locus_id
locus_role
has_qualifying_variant
qualifying_variant_count
strongest_variant_class
strongest_variant_handle
hit_partition_label
variant_filter_policy_id
window_policy_id
```

### Recommended Optional Fields

```text
strongest_sample_variant_observation_id
strongest_projection_membership_id
strongest_quality_state
strongest_frequency_bin
zygosity_state
genotype_state
notes
```

### Rules

`has_qualifying_variant` is a recurrence indicator, not a burden count.

A patient-locus hit means:

```text
sample s has at least one qualifying sample-specific coordinate observation
inside locus window g under the declared policy stack.
```

---

## 16. `variant_locus_memberships`

### Purpose

Defines how sample-specific coordinate observations enter target or background
locus windows under the declared projection policy.

### Required Fields

```text
projection_membership_id
coordinate_variant_handle
sample_variant_observation_id
sample_id
locus_id
locus_role
source_coordinate
chromosome
position
reference_allele
alternate_allele
distance_to_gene_or_window_anchor
variant_class
consequence_partition
frequency_bin
quality_state
frequency_source
frequency_version
frequency_status
source_vap_trace
window_policy_id
variant_filter_policy_id
projection_policy_id
projection_policy_version
```

### Recommended Optional Fields

```text
genotype_state
zygosity_state
allelic_balance
read_depth
genotype_quality
consequence_source
nearest_transcript_id
nearest_gene_distance_rank
membership_confidence
lossiness_state
notes
```

### Identity Rules

The canonical countable burden unit is:

```text
sample_variant_observation_id
```

The normalized variant identity is:

```text
coordinate_variant_handle
```

The projection record is:

```text
projection_membership_id
```

Multiple transcripts, features, gene-window memberships, or annotation overlays
may create multiple projection memberships. They must not create multiple
observed variants unless they refer to distinct sample-specific coordinate
observations.

---

## 17. `null_draw_manifest`

### Purpose

Records reproducible empirical background draws for MPLC.

### Required Fields

```text
draw_id
target_locus_id
selected_background_locus_id
replacement_status
random_seed
background_matching_policy_id
null_model_id
draw_status
```

### Recommended Optional Fields

```text
matching_rank
matching_distance
matching_features_used
draw_group_id
draw_failure_reason
fallback_status
notes
```

### Rules

The null draw manifest must be sufficient to reproduce, audit, or explain the
matched-background contrast.

MPLC empirical-tail values must not be reported without a declared
`number_of_null_draws`, `random_seed`, and `null_model_id`.

---

## 18. `mplc_results`

### Purpose

Reports exploratory MPLC contrast statistics and labels.

### Required Fields

```text
statistic_name
observed_target_value
null_mean
null_percentile
exploratory_empirical_p_value
interpretation_label
result_scope
burden_readiness_status
anti_overclaim_label
```

### Recommended Optional Fields

```text
null_median
null_standard_deviation
null_min
null_max
observed_background_summary
top_contributing_loci
top_contributing_samples
top_contributing_variants
patient_dominance_flag
matching_quality_flag
opportunity_quality_flag
notes
```

### Controlled `statistic_name` Values

```text
burden_excess
recurrence_excess
burden_per_callable_base_excess
patient_locus_hit_excess
compactness_excess
```

### Controlled `interpretation_label` Values

```text
exploratory_prior_locus_burden_excess
exploratory_prior_locus_recurrence_excess
matched_background_consistent
insufficient_opportunity_support
insufficient_matching_support
patient_dominated_signal
hypothesis_generating_only
```

### Prohibited Labels

MPLC results must not use:

```text
disease_associated
pathogenic_region
causal_locus
diagnostic_result
confirmed_epilepsy_locus
confirmed_mitochondrial_locus
```

### Empirical-Tail Rule

`exploratory_empirical_p_value` means an empirical tail probability under the
declared matched-background null. It is not a formal association p-value.

---

## 19. `mplc_validation_receipts`

### Purpose

Records whether the MPLC surface satisfies required structural, scientific, and
anti-overclaim checks.

### Required Fields

```text
validation_receipt_id
mplc_surface_id
validation_check
validation_status
severity
message
source_artifact_ref
created_at_utc
```

### Required Checks

```text
source_corpus_integrity
phenotype_scope_integrity
target_locus_gsc_traceability
coordinate_vap_traceability
sample_observation_counting_audit
opportunity_accounting
background_matching_diagnostics
target_background_overlap_audit
variant_filter_audit
patient_dominance_audit
null_reproducibility_audit
anti_overclaim_audit
```

### Controlled `validation_status` Values

```text
pass
warn
fail
not_applicable
not_evaluated
```

### Controlled `severity` Values

```text
info
warning
error
critical
```

---

## 20. Counting and Identity Rules

MPLC must count observations using sample-specific coordinate evidence.

The following are not countable burden units:

```text
transcript consequence rows
gene annotation rows
GSC prior rows
projection membership rows
post hoc annotation rows
```

The following may be used for grouping, filtering, or interpretation only when
declared by policy:

```text
gene symbols
transcript IDs
consequence terms
GSC prior tiers
phenotype scopes
frequency bins
quality states
```

If a single sample-specific observation maps to multiple genes or transcript
consequences, VDB must preserve those memberships but avoid double-counting the
same observation in aggregate burden counts unless a declared policy explicitly
uses membership-weighted counting and labels the result as such.

---

## 21. Target Locus Rules

Target loci must be selected by a declared `target_locus_policy_id`.

For MPLC v1, an acceptable starting target policy is:

```text
phenotype-scoped GSC prior genes, projected to gene body ±10 kb windows
```

The exact implementation must be registry-declared, for example:

```text
target_locus_policy_id: gsc_epilepsy_high_prior_genes_v1
window_policy_id: gene_body_plus_10kb_v1
```

MPLC may define separate target sets for:

```text
epilepsy high-confidence
epilepsy broad-prior
mitochondrial high-confidence
mitochondrial broad-prior
combined declared phenotype policy
```

Combined target sets are allowed only when an explicit phenotype-scope or
projection policy declares how combined priors are formed.

---

## 22. Background Matching Rules

Background loci must be selected by a declared `background_matching_policy_id`.

The background pool must exclude or flag loci that:

```text
belong to the relevant phenotype-scoped GSC prior target set
overlap target windows under the declared window policy
lack required coordinate or genome-build support
lack sufficient opportunity information when burden-ready output is claimed
fail declared matching criteria
```

Matching features should include, when available:

```text
callable length
locus or window length
chromosome or chromosome class
GC/CpG content
mappability
repeat fraction
local population variant density
WES capture overlap
constraint or gene-feature class
```

If matching quality is poor, MPLC may still emit a surface, but it must mark the
surface as exploratory-only or matching-limited.

---

## 23. Null Model Rules

MPLC uses a matched-background empirical null.

The null model must declare:

```text
null_model_id
number_of_null_draws
random_seed
background_matching_policy_id
replacement rules
matching features
target/background cardinality rules
```

MPLC should preserve target-set cardinality in each background draw unless a
declared null policy states otherwise.

For n=12 case-only demonstrations, null-derived quantities are exploratory
empirical-null evidence, not formal association evidence.

---

## 24. Opportunity and Burden-Readiness Rules

A result may be labeled `burden_ready` only if:

```text
opportunity_model_id is present
opportunity basis is declared
callable_bases or equivalent denominator support is available
opportunity_state is not unknown without qualification
burden_readiness_status from the opportunity layer permits burden use
```

A result must be labeled `exploratory_only`, `not_burden_ready`, or
`denominator_unavailable` if:

```text
opportunity is approximated but incomplete
opportunity is unavailable
opportunity is explicitly unmodeled
callable_bases are missing
sample-specific denominator support is absent
```

Observed variant locations must never be used as the denominator.

---

## 25. Anti-Overclaim Rules

MPLC outputs may support statements such as:

```text
exploratory prior-locus burden excess
matched-background contrast signal
hypothesis-generating recurrence signal
target-locus burden higher than matched non-prior background under declared model
```

MPLC outputs must not support statements such as:

```text
this locus is disease-associated
this locus is causal
this region is pathogenic
this sample has a diagnosis
GSC-prior genes are confirmed by MPLC
```

Anti-overclaim labels are required in `mplc_results` and must be included in
validation receipts.

---

## 26. Validation Rules

MPLC validation must include at least:

```text
1. Source corpus integrity
   Confirm all referenced source TEPs are declared in the TEP-VDB source corpus.

2. Phenotype-scope integrity
   Confirm target loci preserve GSC phenotype scope and are not silently merged.

3. GSC traceability
   Confirm every target locus traces to GSC release, semantic prior, and source
   prior evidence where available.

4. VAP coordinate traceability
   Confirm every burden-contributing observation traces to a VAP coordinate
   observation or sample-specific coordinate observation.

5. Sample-observation counting audit
   Confirm burden counts are not inflated by transcript, annotation, feature, or
   projection-membership duplication.

6. Opportunity accounting
   Confirm burden-ready claims have valid opportunity support.

7. Background matching diagnostics
   Confirm matching features, distances, ranks, and eligibility states are
   declared.

8. Target/background overlap audit
   Confirm background loci do not overlap target windows unless explicitly
   allowed and labeled.

9. Variant-filter audit
   Confirm variant filters and partitions are policy-declared.

10. Patient dominance audit
    Flag results driven primarily by one sample.

11. Null reproducibility audit
    Confirm null model, random seed, draw count, and draw manifest are present.

12. Anti-overclaim audit
    Confirm result labels remain exploratory and non-diagnostic.
```

---

## 27. Failure Modes

The following are MPLC failure modes:

```text
target loci lack GSC traceability
phenotype scopes are silently combined
background loci are treated as non-disease genes
background pool overlaps target set without declaration
matching features are missing or poor quality
opportunity denominators are missing but burden-ready claims are made
observed variant locations are used as denominator opportunity
sample observations are double-counted through transcript or annotation expansion
one patient dominates the apparent signal
null model is not reproducible
exploratory empirical p-values are treated as formal association p-values
RDGP is forced to re-ingest VAP or GSC to reconstruct the surface
```

Any critical failure should prevent the MPLC surface from being labeled
`burden_ready`.

---

## 28. Future Extensions

Future MPLC versions may add:

```text
dosage-weighted burden
inheritance-aware sample partitions
compound-heterozygosity-aware locus summaries
constraint-aware matching
tissue-context matching
developmental-stage context
regulatory target-linking policies
ancestry-aware background matching
external control cohorts
formal association testing
```

These extensions must remain policy-declared, coordinate-traceable,
opportunity-aware, and anti-overclaim bounded.

---

## 29. Summary

MPLC is a prior-informed VDB projection surface.

Its minimum safe implementation requires:

```text
phenotype-scoped GSC target loci
matched non-prior background loci
VAP-derived sample-specific coordinate observations
declared locus-window policy
declared variant-filter policy
declared opportunity model
declared matched-background null model
traceable burden and recurrence matrices
sample-observation counting discipline
validation receipts
anti-overclaim labels
```

The correct MPLC claim is:

```text
Under a declared matched-background null and opportunity model,
phenotype-scoped GSC-prior loci show or do not show exploratory local burden
or recurrence excess relative to matched non-prior loci.
```

The incorrect MPLC claim is:

```text
MPLC proves disease association, pathogenicity, diagnosis, or causality.
```

MPLC gives RDGP a scientifically bounded room to reason inside. It does not
replace RDGP, and it does not collapse VDB evidence integration into a single
variant-to-gene score.

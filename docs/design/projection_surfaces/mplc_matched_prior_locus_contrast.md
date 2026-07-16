# Matched Prior-Locus Contrast (MPLC)

> Status: SAGE-VDB projection-surface design draft.
>
> Intended path:
>
> `docs/design/projection_surfaces/mplc_matched_prior_locus_contrast.md`
>
> Parent architecture:
>
> `docs/architecture/tep_vdb_architecture.md`
>
> Mathematical parent:
>
> `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`
>
> Projection family:
>
> TEP-VDB unknown-tomorrow diagnostic discovery support surface.
>
> Primary consumer:
>
> RDGP and future downstream reasoning systems.
>
> This document defines the biological, mathematical, and evidentiary constraints
> for a VDB-emitted TEP-VDB projection surface. It is not a final implementation
> schema. DEX-VDB should derive implementation schemas, validators, and emission
> contracts from this design.

The Matched Prior-Locus Contrast (MPLC) surface is a prior-informed TEP-VDB
projection surface that compares burden near phenotype-scoped prior loci against
matched non-prior background loci using VAP-derived sample-specific coordinate
observations and GSC-derived prior provenance preserved through VDB.

For the planned first demonstration profile, the disease context is epilepsy.
The method design, however, should remain corpus- and phenotype-scope-general.

The Matched Prior-Locus Contrast (MPLC) method can be summarized in plain-English as:

```text
MPLC asks whether epilepsy patients carry more rare variant burden near
GSC-prior disease loci than near matched non-prior background loci
from the same genomes.
```

> MPLC thus defines a VDB-emitted projection surface that can support RDGP reasoning without requiring RDGP to re-integrate VAP and GSC source packages.

---

# Shared TEP-VDB Corpus Constraint

This method operates on a single uniform TEP-VDB emitted by VDB.

The source corpus for the planned first demonstration is:

```text
12 epilepsy TEP-VAPs
2 TEP-GSCs:
    epilepsy semantic priors
    mitochondrial disease semantic priors
```

RDGP does not re-ingest VAP or GSC producer packages directly for this method.
RDGP consumes VDB-emitted projection surfaces, burden matrices, null manifests,
annotation overlays, and source-traceability receipts from the TEP-VDB.

This constraint is not only a storage convenience. It is part of the system
boundary:

```text
VDB performs the 14-source-TEP integration once.
TEP-VDB carries the unified reason-ready projection substrate.
RDGP reasons over TEP-VDB surfaces without independently overlaying VAP and GSC.
```

Both MPLC and CFBS should therefore be treated as method-specific projection
surfaces inside the same TEP-VDB emission, not as separate ingestion modes.


> Demonstration profile note: the 14-source corpus described here is the
> planned first epilepsy demonstration profile, not a universal TEP-VDB schema
> requirement. Generic schemas should allow other source-corpus sizes and should
> enforce `source_tep_count == 14` only through an explicit demonstration
> validation profile.

> DEX derivation note: object lists in this MPLC design are schema seeds, not
> final field contracts. DEX-VDB must normalize required/optional fields, data
> types, controlled vocabularies, validation profiles, and file names in derived
> implementation specifications before any builder is implemented.

---

# Projection-Surface Alignment Addendum

MPLC is a TEP-VDB prior-informed discovery projection surface.

It belongs to the unknown-tomorrow diagnostic discovery family in the TEP-VDB
architecture, with strong dependency on phenotype-scoped prior evidence from
GSC.

Its role is to expose matched prior-locus burden, recurrence, background-null,
opportunity, and traceability substrates so RDGP can reason over whether
phenotype-scoped prior loci show burden excess relative to matched non-prior
loci.

The core doctrine is:

```text
MPLC does not prove disease association.

MPLC exposes exploratory, opportunity-aware burden and recurrence contrast
between phenotype-scoped prior loci and matched non-prior background loci under
declared target-locus, background-matching, window, variant-filter, null-model,
and opportunity policies.
```

MPLC is:

```text
prior-informed
phenotype-scope aware
matched-background based
opportunity-aware
locus/window based
null-model declared
traceable to sample-specific variant observations
traceable to GSC prior sources
exploratory
RDGP-facing
```

MPLC is not:

```text
a formal disease-association test
a diagnostic result
a causal-gene classifier
a pathogenicity adjudication
a proof that GSC-prior loci are disease-causing
a proof that background loci are non-disease loci
a replacement for RDGP reasoning
```

The safe boundary is:

```text
MPLC exposes matched prior-locus burden contrast.
RDGP reasons over that contrast.
Scientists and clinicians interpret evaluated evidence.
```

---

# Relationship to TEP-VDB Architecture

MPLC should conform to the TEP-VDB architecture and the mathematical foundation
for evidence topology, opportunity-aware geometry, and projection surfaces.

In the TEP-VDB v1 surface family, MPLC complements:

```text
CFBS:
    coordinate-first burden scan

PAPS:
    phenotype-prior alignment and prior provenance

PGERS:
    patient-gene / patient-locus evidence rollup

OACS:
    opportunity, absence, and callability context

CUES:
    conflict and uncertainty state

EVRS:
    exact variant recurrence

RFPS:
    regulatory / feature projection

RMCS:
    method, dependency, and currency state
```

MPLC should remain distinct from these sibling surfaces. It may reference or
consume their outputs, but it should not absorb their responsibilities.

---

# Relationship to Mathematical Formalism

Under the mathematical foundation, MPLC is a specialization of an
opportunity-aware prior-locus contrast surface.

```text
θ_MPLC:
    source objects =
        sample-specific coordinate / variant observations,
        phenotype-scoped GSC prior records,
        target locus definitions,
        matched background locus definitions,
        opportunity states,
        variant filter partitions,
        null-model receipts,
        matching diagnostics

    target objects =
        phenotype-scoped prior loci and matched non-prior background loci

    membership =
        a sample-specific variant observation belongs to a target or background
        locus if its coordinate satisfies the declared locus-window,
        variant-filter, opportunity, and membership policy

    opportunity =
        callable / assay-visible / quality-supported coordinate territory used
        as denominator context for target and background burden comparison

    geometry =
        target burden, background burden, burden excess, patient recurrence,
        exploratory empirical-null position, and matching diagnostics

    surface =
        matched prior-locus contrast substrate for RDGP
```

Compact form:

```text
S_MPLC = F_MPLC(T_C, M_MPLC, Ω_MPLC, P_MPLC)
```

Where:

```text
T_C = evidence topology

M_MPLC = membership operator from sample-specific coordinate observations
         to target and matched background loci

Ω_MPLC = opportunity space for locus-window burden comparison

P_MPLC = target-locus, background-matching, window, variant-filter,
         counting, null-model, and labeling policy
```

Traceability rule:

```text
Every MPLC burden count, recurrence count, target/background assignment,
matched background draw, empirical-null summary, and result label must trace to
contributing sample-specific variant observations, GSC prior records, matching
policy, opportunity records, projection policies, and source assertion records.
```

---

# 1. What MPLC is trying to test

We have two locus groups:

```text
Target loci:
    GSC-prior epilepsy / mitochondrial disease loci

Background loci:
    matched non-prior loci
    not in the GSC-prior target set
```

For each group, RDGP asks:

```text
Across the declared case/sample corpus,
how much rare coding / noncoding / regulatory / splice-proximal burden
appears near these loci?
```

For the planned first epilepsy demonstration profile, the declared case/sample
corpus is expected to contain 12 epilepsy TEP-VAPs. Generic MPLC schemas should
not hard-code this sample count.


The scientific question is not:

```text
Are these variants disease-causing?
```

The proper question is:

```text
Within these epilepsy genomes,
do GSC-prior loci carry more local rare-variant burden than comparable
non-prior loci under the same technical and patient background?
```

---

# 2. The proper null hypothesis

The null hypothesis is the “nothing special is happening here” model.

For MPLC, the null should be:

```text
After accounting for genomic opportunity, phenotype-scoped prior loci do not
carry more rare variant burden than matched non-prior background loci in the
same declared case/sample corpus.
```

For the planned first epilepsy demonstration profile, those prior loci may be
GSC-derived epilepsy or mitochondrial-disease prior loci, analyzed under explicit
phenotype-scope policy.

Or even simpler:

```text
If GSC-prior loci are not unusually burdened, then their observed variant
burden should look like the burden seen in matched background loci.
```

This is the key phrase:

```text
matched background loci
```

Not random loci. Not “non-disease” loci. Not arbitrary genes.

Matched background loci should look similar to the GSC-prior loci in ways that affect how many variants we expect to observe.

---

# 3. Why matching matters

Imagine two buckets.

One bucket is huge and easy to see into.
Another bucket is tiny and hidden in the dark.

If we find more pebbles in the huge visible bucket, that does not mean the huge bucket is biologically special. It may just have more space and better visibility.

Gene windows are like buckets.

Some gene windows are:

```text
longer
more callable
more GC-rich
more repetitive
more covered by WES
more mappable
more variant-dense in the general population
```

So we cannot compare disease-prior loci against just any random genes.

We need to compare them against background genes with similar “bucket properties.”

---

# 4. The objects MPLC needs

For every locus window `g`, VDB/TEP-VDB should provide RDGP with:

```text
locus_id
gene_id
gene_symbol
is_gsc_prior_locus
gsc_prior_tier
chromosome
window_start
window_end
window_policy_id
callable_bases
observed_variants
qualifying_variant_count
patient_recurrence_count
source VAP coordinate traces
source GSC prior traces
matching features
```

For every patient `s` and locus `g`, RDGP needs a small table like:

```text
sample_id
locus_id
qualifying_variant_count
rare_variant_count
noncoding_variant_count
coding_variant_count
splice_proximal_variant_count
callable_bases
burden_per_callable_base
patients_with_hit
```

This is the reason-ready substrate.


Implementation guardrail:

```text
coordinate_variant_handle:
    normalized coordinate/reference-context variant identity

sample_variant_observation_id:
    sample-specific observation of that variant

projection_membership_id:
    membership of that observation in a locus, window, feature, or annotation
```

Burden counts should operate over sample-specific coordinate observations, not
over duplicated annotation rows. Multiple transcript, feature, or gene-window
mappings should create multiple memberships, not multiple observed variants.

## Sample, Patient, and Recurrence Unit Boundary

MPLC may use `sample_id` as the practical v1 row anchor, but recurrence claims
must declare the recurrence unit.

Recommended recurrence units include:

```text
sample
patient
subject
family
unknown
not_evaluated
```

For the planned first epilepsy WES demonstration, `sample` and `patient` may be
one-to-one under the source corpus. Generic MPLC schemas should not assume that
relationship silently.

When patient or subject identity is available, MPLC should preserve:

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

---

# 5. The simplest math

Let:

```text
s = patient
g = gene/locus window
```

For each patient and locus, count the qualifying variants:

```text
B[s,g] = number of qualifying variants in patient s near locus g
```

Example:

```text
B[ERR10619300, SCN1A] = 2
```

means that patient `ERR10619300` has two qualifying variants in the `SCN1A` gene window.

But raw counts are not enough, because some windows are larger or more callable.

So define:

```text
C[s,g] = callable bases for patient s near locus g
```

Then a basic rate is:

```text
R[s,g] = B[s,g] / C[s,g]
```

In plain English:

```text
rate = variants observed / bases where variants could have been observed
```

That prevents a 200 kb callable region from unfairly beating a 10 kb callable region, acting as a form of normalization against varying gene sizes.

---

# 6. Cohort-level burden

For all GSC-prior target loci, sum the burden:

```text
Observed target burden:

O_target = sum of B[s,g]
           across all patients s
           and all GSC-prior loci g
```

In words:

```text
How many qualifying variants did we observe near all disease-prior loci
across all 12 patients?
```

But again, we should account for opportunity:

```text
Observed target opportunity:

C_target = sum of C[s,g]
           across all patients s
           and all GSC-prior loci g
```

Then:

```text
Target burden rate:

R_target = O_target / C_target
```

That is the burden rate near disease-prior loci.

---

# 7. Building the background null

For each GSC-prior target locus, choose matched background loci.

Example:

```text
Target:
    SCN1A

Matched background candidates:
    BG_001
    BG_002
    BG_003
    ...
    BG_100
```

Those background loci should be similar to SCN1A’s window in features such as:

```text
callable length
chromosome or chromosome class
GC/CpG content
mappability
repeat fraction
gene length
local population variant density
WES capture overlap, if WES
```

Then create many fake “target sets.”

For each fake set:

```text
replace every real GSC-prior locus with one matched background locus
```

So if the real target set has 500 GSC-prior loci, every fake set also has 500 loci.

That gives us:

```text
fake target set 1
fake target set 2
fake target set 3
...
fake target set 10,000
```

For each fake set, compute the same burden rate:

```text
R_background_1
R_background_2
R_background_3
...
R_background_10000
```

This collection is the null distribution.

Plain English:

```text
What burden would we expect if we looked at similar non-prior loci
instead of GSC-prior loci?
```

---

# 8. Exploratory empirical-null evidence

Now compare the real GSC-prior burden rate to the fake background burden rates.

If the real target rate is higher than nearly all fake background rates, that is interesting.

MPLC may report an exploratory empirical tail probability:

```text
exploratory_empirical_p_value =
    (1 + number of fake background rates >= real target rate)
    /
    (1 + number of fake background draws)
```

Example:

```text
10,000 fake background draws

real GSC-prior burden is higher than 9,875 of them

125 fake draws are equal or higher

exploratory_empirical_p_value = (1 + 125) / (1 + 10000)
exploratory_empirical_p_value ≈ 0.0126
```

Interpretation:

```text
Under the matched-background null,
a burden this high appears in about 1.3% of fake matched-background scans.
```

For n=12, this is exploratory empirical-null evidence, not formal disease association evidence.

---

# 9. Better than total burden: patient recurrence

Total burden can be misleading.

Suppose we find 20 variants near a disease-prior locus.

That could mean:

```text
20 variants in 1 patient
```

or:

```text
1 variant each in 8 different patients, plus extras
```

The second is usually more interesting for disease-cohort convergence.

So compute:

```text
K[g] = number of patients with at least one qualifying variant near locus g
```

Example:

```text
K[SCN1A] = 4
```

means 4 of the 12 patients have at least one qualifying variant in the `SCN1A` gene window.

Then compare recurrence in GSC-prior loci to recurrence in matched background loci.

A useful cohort statistic:

```text
O_recurrence_target =
    total number of patient-locus hits among GSC-prior loci
```

Where a patient-locus hit means:

```text
patient s has ≥1 qualifying variant near locus g
```

This prevents one high-burden patient from dominating everything.

---

# 10. Best first MPLC statistics

For the first implementation, I would define three MPLC scores.

## Score 1: burden excess

```text
Do GSC-prior loci have more qualifying variants
than matched background loci?
```

Use:

```text
burden per callable base
```

---

## Score 2: recurrence excess

```text
Do GSC-prior loci show hits across more patients
than matched background loci?
```

Use:

```text
number of patient-locus hits
```

---

## Score 3: compactness excess

```text
When variants appear near GSC-prior loci,
are they more spatially clustered than matched background variants?
```

Use something simple at first, like:

```text
minimum interval containing the variants
```

or:

```text
average distance among variants within the locus window
```

For n=12, burden and recurrence should be the first priority. Compactness can be v2.

---

# 11. Proper MPLC null, formal version

Here is the clean scientific version:

```text
MPLC null hypothesis:

Conditional on callable opportunity, locus-window structure, phenotype-scope
policy, and matching features, phenotype-scoped prior target loci are
exchangeable with matched non-prior background loci with respect to rare variant
burden in the declared case/sample corpus.
```

For the planned first epilepsy demonstration profile, the declared corpus is
expected to be the 12-sample epilepsy WES cohort. The null model should
nevertheless be defined over the declared corpus and policy, not over a
hard-coded sample count.

Freshman biology translation:

```text
If the disease-prior loci are not special, then they should look like
similar non-prior loci when we count rare variants in the same patients.
```

That is the null RDGP tests against.

---

# 12. What “exchangeable” means

This word is useful.

Exchangeable means:

```text
Under the null, swapping a GSC-prior locus with a matched background locus
should not change the expected variant burden.
```

So if `SCN1A` and a matched background locus have similar size, callability, GC, mappability, and variant-density opportunity, then under the null they should behave similarly.

If `SCN1A`-like target loci repeatedly show more burden than their matched substitutes, that is evidence of a target-locus burden excess.

Not proof of causality. But evidence of nonrandom case-internal convergence.

---

# 13. How GSC influences MPLC

For MPLC, GSC is used at the front:

```text
GSC defines the target loci.
```

That means MPLC is not unbiased genome-wide discovery. It is prior-informed.

That is fine.

The claim becomes:

```text
Given GSC-prior disease loci, do epilepsy patients show excess local burden
relative to matched non-prior loci?
```

This is exactly the kind of reason-ready question RDGP should ask.


Phenotype-scope guardrail:

Epilepsy and mitochondrial-disease GSC priors may both be present in the
TEP-VDB. MPLC should support separate phenotype-scoped prior surfaces and should
not silently combine them into one disease-prior target set unless an explicit
projection policy declares that combined view.

# 13A. MPLC Projection Policy

MPLC requires an explicit projection policy.

Recommended policy fields:

```text
mplc_projection_policy_id
mplc_projection_policy_version
source_corpus_generation_id
target_locus_policy_id
target_prior_scope_policy_id
paps_reference_policy_id
background_pool_policy_id
background_matching_policy_id
window_policy_id
variant_filter_policy_id
variant_class_partition_policy_id
counting_policy_id
recurrence_unit_policy_id
opportunity_model_id
oacs_reference_policy_id
null_model_policy_id
matching_diagnostics_policy_id
patient_dominance_policy_id
artifact_warning_policy_id
cues_reference_policy_id
rmcs_reference_policy_id
traceability_policy_id
anti_overclaim_policy_id
```

The MPLC projection policy must declare:

```text
which phenotype-scoped prior loci are eligible as targets

which prior source and phenotype scope are being tested

whether epilepsy, mitochondrial, broad, narrow, or combined prior scopes are
analyzed separately or together

which loci are eligible for the matched background pool

how background loci are excluded from target/prior sets

which matching features are required

which coordinate window policy is used

which samples or patients are included

which variant classes and filters are included

which opportunity denominator is used

which counting unit is used

which recurrence unit is used

which null model is used

which statistic ranks or summarizes the contrast

which warnings block, limit, or qualify MPLC consumption

which claims are prohibited
```

Silent filtering, silent prior-scope combination, silent denominator
substitution, silent recurrence-unit changes, and silent background-pool changes
are prohibited.


---

# 14. What TEP-VDB should emit for MPLC

TEP-VDB should not just emit final scores.

It should emit the room RDGP reasons inside. For MPLC, that room is a
method-specific projection surface inside one uniform TEP-VDB. In the planned
first epilepsy demonstration, that TEP-VDB uses the 14-source profile described
above. Generic TEP-VDB schemas should not hard-code that source count.

For MPLC, TEP-VDB should contain:

```text
tep_vdb_analysis_scope:
    tep_vdb_id
    source_corpus_id
    source_tep_count
    vap_tep_count
    gsc_tep_count
    vap_package_ids
    gsc_release_ids
    genome_build
    corpus_generation_id
    assertion_record_build_id
    topology_build_id
    geometry_build_id
    projection_policy_id
    emission_policy_id

mplc_analysis_scope:
    mplc_surface_id
    mplc_surface_generation_id
    method_id
    method_version
    mplc_projection_policy_id
    target_locus_policy_id
    target_prior_scope_policy_id
    paps_surface_ref when available
    background_pool_policy_id
    background_matching_policy_id
    window_policy_id
    variant_filter_policy_id
    variant_class_partition_policy_id
    counting_policy_id
    recurrence_unit_policy_id
    opportunity_model_id
    oacs_surface_ref
    null_model_id
    null_model_policy_id
    matching_diagnostics_policy_id
    cues_surface_ref when applicable
    rmcs_surface_ref when applicable
    number_of_null_draws
    random_seed
    anti_overclaim_policy_id

target_locus_set:
    target_locus_membership_id
    mplc_surface_id
    mplc_surface_generation_id
    target_set_id
    target_set_policy_id
    target_prior_scope_policy_id
    locus_id
    projected_target_id
    target_type
    phenotype_scope
    phenotype_scope_namespace
    phenotype_scope_alignment_status when available
    paps_surface_ref when available
    paps_prior_refs when available
    gsc_tep_id
    gsc_tep_version
    gsc_release_id
    gsc_prior_record_id when available
    semantic_prior_id
    gsc_prior_source
    gsc_prior_score
    gsc_prior_rank
    gsc_prior_tier
    gene_namespace
    gene_id
    gene_symbol
    gene_biotype
    target_identity_bridge_id
    target_identity_bridge_status
    target_identity_bridge_lossiness
    chromosome
    window_start
    window_end
    window_policy_id
    source_gsc_trace
    traceability_refs
    anti_overclaim_label

background_locus_pool:
    background_locus_id
    background_pool_policy_id
    mplc_surface_id
    mplc_surface_generation_id
    locus_id
    projected_target_id when applicable
    background_gene_namespace
    background_gene_id
    background_gene_symbol
    target_identity_bridge_status
    target_identity_bridge_lossiness
    chromosome
    window_start
    window_end
    window_policy_id
    matching_feature_values
    eligibility_status
    matching_eligible: true/false
    excluded_from_target_set: true/false
    excluded_due_to_prior_under_policy: true/false
    excluded_due_to_overlap_with_target_window: true/false
    excluded_due_to_opportunity_limitation: true/false
    exclusion_reason_if_any
    background_locus_not_non_disease_label
    oacs_surface_ref when applicable
    traceability_refs
    anti_overclaim_label

matched_locus_sets:
    matched_locus_membership_id
    mplc_surface_id
    mplc_surface_generation_id
    draw_id
    target_locus_id
    matched_background_locus_id
    replacement_status
    matching_rank
    matching_distance
    matching_features_used
    matching_feature_summary
    matching_quality_label
    matching_limitation_label
    random_seed
    background_matching_policy_id
    matching_diagnostics_ref
    traceability_refs
    anti_overclaim_label

matching_diagnostics:
    matching_diagnostics_id
    mplc_surface_id
    mplc_surface_generation_id
    background_matching_policy_id
    target_set_id
    background_pool_policy_id
    matching_feature_name
    target_distribution_summary
    matched_background_distribution_summary
    imbalance_metric
    imbalance_label
    matching_pass_status
    matching_limitation_label
    cues_event_refs when applicable
    traceability_refs

sample_locus_burden_matrix:
    mplc_sample_locus_row_id
    mplc_surface_id
    mplc_surface_generation_id
    sample_id
    patient_id when available
    subject_id when available
    sample_patient_link_status when applicable
    locus_id
    locus_role
    counting_policy_id
    recurrence_unit_policy_id
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
    low_confidence_bases
    filtered_bases
    unknown_opportunity_bases
    oacs_surface_ref
    traceability_refs
    anti_overclaim_label

patient_locus_hit_matrix:
    mplc_hit_row_id
    mplc_surface_id
    mplc_surface_generation_id
    sample_id
    patient_id when available
    subject_id when available
    sample_patient_link_status when applicable
    locus_id
    locus_role
    recurrence_unit
    recurrence_unit_policy_id
    has_qualifying_variant
    qualifying_variant_count
    strongest_variant_class
    strongest_variant_handle
    hit_partition_label
    genotype_context_summary when applicable
    genotype_variant_relationship_state_summary when applicable
    direct_source_biallelic_relationship_count when applicable
    resolved_from_multiallelic_record_count when applicable
    brokered_with_normalization_relationship_count when applicable
    ambiguous_genotype_variant_relationship_count when applicable
    unresolved_genotype_variant_relationship_count when applicable    
    quality_context_summary
    traceability_refs
    anti_overclaim_label

variant_locus_memberships:
    mplc_locus_membership_id
    mplc_surface_id
    mplc_surface_generation_id
    projection_membership_id
    coordinate_variant_handle
    sample_variant_observation_id
    genotype_observation_id when applicable
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
    locus_id
    locus_role
    source_coordinate
    chrom
    pos
    ref
    alt
    distance_to_gene_or_window_anchor
    variant_class
    consequence_partition
    frequency_bin
    quality_state
    frequency_source
    frequency_version
    frequency_status
    variant_filter_partition
    counting_unit
    source_vap_trace
    source_assertion_refs
    traceability_refs
    anti_overclaim_label

null_draw_manifest:
    null_draw_membership_id
    mplc_surface_id
    mplc_surface_generation_id
    draw_id
    target_locus_id
    selected_background_locus_id
    replacement_status
    random_seed
    background_matching_policy_id
    null_model_id
    null_model_policy_id
    matching_distance
    matching_quality_label
    traceability_refs
    anti_overclaim_label

mplc_results:
    mplc_result_id
    mplc_surface_id
    mplc_surface_generation_id
    statistic_name
    statistic_scope
    observed_target_value
    observed_background_summary
    null_mean
    null_percentile
    exploratory_empirical_p_value
    empirical_tail_probability_scope
    null_model_id
    null_model_policy_id
    target_locus_count
    background_locus_count
    sample_recurrence_count
    patient_recurrence_count when patient identity is available
    recurrence_unit
    max_single_sample_burden_fraction
    patient_dominance_warning
    matching_quality_summary
    opportunity_limitation_label
    candidate_label
    interpretation_label
    cues_event_refs when applicable
    rmcs_currency_refs when applicable
    traceability_refs
    anti_overclaim_label

validation_receipts:
    source_corpus_integrity_pass
    coordinate_traceability_pass
    gsc_traceability_pass
    matching_diagnostics_pass
    opportunity_accounting_pass
    patient_dominance_audit_pass
    anti_overclaim_pass
```

Recommended `locus_role` values:

```text
target_prior_locus
matched_background_locus
excluded_background_candidate
not_evaluated
```

`interpretation_label` must remain an anti-overclaim-safe label such as
`exploratory_prior_locus_burden_contrast`. It must not encode disease
association, pathogenicity, causality, diagnostic status, or RDGP ranking.

Background loci are matched non-prior loci under the declared MPLC policy. They
must not be described as proven nondisease loci, unaffected controls, benign
genes, or negative biological controls.

## Suggested shared TEP-VDB layout

```text
tep_vdb/
    envelope
    manifest
    source_corpus/
        source_tep_index
        vap_source_packages
        gsc_source_packages

    shared_substrates/
        coordinate_observations
        feature_declarations
        gene_annotations
        gsc_prior_overlays
        opportunity_space
        variant_filter_partitions
        source_traceability

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

        cfbs/
            cfbs_analysis_scope
            scan_space
            window_set
            sample_window_burden_matrix
            patient_window_hit_matrix
            variant_window_memberships
            null_model
            null_draw_summary
            candidate_interval_set
            posthoc_annotations
            cfbs_results
            cfbs_validation_receipts
```

This keeps the source corpus unified while letting MPLC and CFBS remain
distinct reasoning rooms. In the planned first epilepsy demonstration, that
unified corpus uses the 14-source profile described above.

---

# 15. Minimum viable MPLC v1

For a first version, keep it simple.

## Inputs

```text
Input:
    one uniform TEP-VDB emitted by VDB

TEP-VDB source corpus:
    12 epilepsy TEP-VAPs
    2 TEP-GSCs:
        epilepsy semantic priors
        mitochondrial disease semantic priors

TEP-VDB shared substrates:
    coordinate-normalized variant observations
    sample-specific observation handles
    genotype / zygosity / dosage fields where available
    GSC prior overlays
    gene annotation overlays
    genome build
    callable/opportunity approximation
    population-frequency overlay, if available
    explicit unknown-frequency / unresolved-frequency states
    source traceability receipts
```

---

## Target loci

```text
GSC epilepsy high-prior genes
GSC mitochondrial high-prior genes
```

Maybe do tiers separately:

```text
epilepsy high-confidence
epilepsy broad-prior
mitochondrial high-confidence
mitochondrial broad-prior
combined
```

---

## Window

Start with:

```text
gene body ±10 kb
```

Use this exact policy label:

```text
gene_body_plus_10kb_v1
```

---

## Variant filters

For MPLC v1:

```text
PASS or acceptable VAP quality
rare / absent in external population resources, if available
partition coding and noncoding separately
exclude low-mappability regions where possible
preserve unresolved states
```

---

## Null

```text
matched non-prior background loci
10,000 background draws
burden and recurrence exploratory empirical tail probabilities
```

---

## Outputs

```text
burden excess
recurrence excess
top contributing loci
top contributing patients
top contributing variants
traceable source coordinates
validation warnings
```

---

# MPLC Relationship to Sibling Projection Surfaces

MPLC should interoperate with sibling TEP-VDB projection surfaces without
collapsing into them.

## Relationship to KVPS

KVPS exposes known pathogenicity evidence attached to sample-specific observed
variants.

MPLC may reference KVPS when a variant contributing to a target or background
locus has known pathogenicity or clinical-significance context.

MPLC may include KVPS-derived context such as:

```text
known_pathogenicity_overlap
known_conflicting_pathogenicity_overlap
known_vus_or_uncertain_overlap
kvps_surface_ref
kvps_membership_refs
```

KVPS context must remain contribution-level context. It must not be used to
define target loci, define background loci, select matched backgrounds, or
convert target-locus burden into disease association.

---

## Relationship to GIRS

GIRS exposes genotype observation structure and inheritance-readiness context.

MPLC may reference GIRS for genotype-aware variant partitions or contribution
context, such as:

```text
genotype_context_available
heterozygous_like_contributor_count
homozygous_alt_like_contributor_count
no_call_or_uncertain_genotype_count
genotype_quality_limited_count
girs_surface_ref
girs_membership_refs
```

MPLC must not perform inheritance reasoning. Genotype context may help RDGP
evaluate target-locus evidence later, but MPLC itself remains a matched
prior-locus burden and recurrence contrast surface.

---

## Relationship to PAPS

PAPS provides phenotype-prior alignment and GSC prior provenance.

MPLC should consume phenotype-scoped prior targets through PAPS-compatible prior
context whenever available. MPLC must preserve phenotype scope and must not
flatten epilepsy, mitochondrial, broad, narrow, stale, or mismatched priors into
generic disease-gene labels.

PAPS owns phenotype-prior provenance and alignment state. MPLC owns matched
prior-locus burden contrast.

---

## Relationship to OACS

OACS provides the denominator and absence-readiness context MPLC requires.

MPLC should reference OACS for:

```text
target-locus opportunity
background-locus opportunity
callable bases
not-callable territory
not-assayed territory
low-confidence territory
filtered territory
unknown opportunity
negative-evidence readiness
```

MPLC must not compare target and background burden without declared opportunity
or explicit unmodeled-opportunity state.

---

## Relationship to OACS/PAPS Boundary Note

PAPS-derived prior scope may define MPLC target loci only through the declared
MPLC target-locus policy. OACS-derived opportunity context defines whether
target and background loci are comparable as burden denominators. These are
different roles:

```text
PAPS:
    Which phenotype-scoped prior targets are eligible?

OACS:
    Was the target/background locus observable enough for burden comparison?

MPLC:
    Does the prior target set show exploratory burden contrast relative to
    matched background loci?
```

---

## Relationship to CUES

CUES should index MPLC uncertainty and limitation events.

Examples include:

```text
target_background_matching_limited
matching_feature_imbalance
opportunity_unmodeled
patient_dominance_detected
phenotype_scope_mismatch
gsc_prior_stale
background_pool_limited
null_model_limited
exploratory_empirical_p_value_overread_risk
```

MPLC may carry these warning fields, but CUES owns the package-level epistemic
event surface.

---

## Relationship to PGERS

PGERS may summarize MPLC target-locus memberships inside patient-gene or
patient-locus evidence rollups.

MPLC should expose target-locus, background-locus, and contributing variant
references so PGERS can include prior-locus burden context without flattening
MPLC into a generic gene score.

---

## Relationship to RFPS

RFPS can provide feature and regulatory context for variants contributing to
MPLC target or background loci.

MPLC may include RFPS-derived partitions such as:

```text
regulatory_feature_variant_count
promoter_projected_variant_count
enhancer_projected_variant_count
splice_regulatory_variant_count
conserved_noncoding_variant_count
```

But MPLC must not infer regulatory mechanism.

---

## Relationship to EVRS

EVRS exposes exact allele recurrence.

MPLC exposes locus-level burden and recurrence relative to matched background
loci.

An exact recurrent allele may contribute to an MPLC locus signal, but MPLC
should not treat exact recurrence as equivalent to locus burden excess. MPLC
should preserve EVRS references when exact recurrent variants contribute to
target or background loci.

---

## Relationship to CFBS

CFBS is coordinate-first. MPLC is prior-informed.

MPLC may be compared narratively with CFBS, but the two surfaces answer
different questions and use different candidate-generation policies.

```text
CFBS:
    coordinates → burden scan → candidate intervals → post hoc biology

MPLC:
    phenotype-scoped priors → matched loci → burden contrast
```

A locus supported by both surfaces may be interesting to RDGP, but VDB must not
convert cross-surface convergence into causality.

---

## Relationship to RMCS

RMCS should track MPLC dependency and method currency, including:

```text
target_locus_policy_id
background_matching_policy_id
window_policy_id
variant_filter_policy_id
opportunity_model_id
null_model_id
gsc_release_id
phenotype_scope_policy_id
number_of_null_draws
random_seed
source_corpus_id
surface_generation_id
```

An MPLC surface generated under a different GSC release, target policy,
background-matching policy, source corpus, opportunity policy, null model, or
random seed should not be compared to another MPLC surface without an RMCS
comparability state.

---

## Required Anti-Overclaim Labels

MPLC rows, target/background summaries, result objects, and package-level
summaries should carry anti-overclaim labels.

Recommended default label:

```text
exploratory_prior_locus_contrast_not_association
```

Additional labels may include:

```text
prior_locus_burden_not_disease_association
matched_background_not_control_cohort
empirical_tail_probability_not_formal_association_p_value
gsc_prior_not_causality
target_burden_excess_not_diagnosis
opportunity_limited_burden_surface
mplc_candidate_not_rdgp_priority
mplc_result_not_genetic_diagnosis
patient_recurrence_not_case_control_association
background_locus_not_non_disease_control
genotype_context_not_inheritance_evidence_by_mplc
known_pathogenicity_overlap_not_locus_causality
paps_prior_scope_not_target_causality
```

---

## Invalid MPLC Patterns

Invalid MPLC designs include:

```text
GSC-prior loci are treated as causal loci.

Matched background loci are described as non-disease genes.

Target and background loci are compared without opportunity accounting.

Phenotype-scoped GSC priors are flattened into generic gene support.

Epilepsy and mitochondrial priors are silently combined without a projection
policy.

Exploratory empirical tail probabilities are described as formal
disease-association p-values.

Target-locus burden is labeled disease-associated, pathogenic, causal, or
diagnostic.

Background matching diagnostics are omitted.

One high-burden patient can dominate the target burden without a detectable
patient-dominance warning.

Multiple genotype_variant_relationship rows from one genotype_observation_id are
counted as multiple source genotype observations.

Resolved multiallelic genotype-to-variant relationships are treated as
direct_source_biallelic producer calls.

Unresolved, ambiguous, or not-evaluated genotype-to-variant relationships are
treated as absence or clean noncontribution without CUES/OACS-compatible
limitation state.

MPLC outputs are encoded as RDGP rankings.

MPLC summary rows replace membership-level coordinate and GSC-prior
traceability.

MPLC surfaces generated under different target/background/null policies are
compared without RMCS comparability state.

Sample recurrence is reported as patient recurrence without declared
sample-patient linkage.

Background loci are treated as nondisease controls.

A phenotype-scoped prior is treated as target-locus causality.

KVPS known pathogenicity context is used to define MPLC target loci.

GIRS genotype context is used to infer inheritance inside MPLC.

PAPS phenotype-prior context is silently combined across phenotype scopes.

RFPS feature context is treated as mechanism rather than contribution context.

A target or background locus with stale or incomparable MPLC policy state is
consumed without RMCS warning.
```

---

# 16. What not to do

Do not compare D (disease) loci to arbitrary random N (non-disease) loci.

Do not call N loci “non-disease genes.”

Do not treat missing annotation as benign.

Do not let one high-burden sample dominate.

Do not use one window size as biological truth.

Do not claim disease association.

Do not let RDGP see only final scores without coordinate traceability.

Do not treat exploratory empirical tail probabilities as formal association
p-values.

---

# 17. Assumptions

For MPLC, I am assuming:

```text
1. The 12 samples are comparable VAP-processed epilepsy cases.
2. GSC provides phenotype-scoped prior loci, not causal truth.
3. Background loci are non-prior, not proven nondisease.
4. VDB can emit coordinate-preserved sample-locus projections.
5. The first goal is exploratory prioritization, not formal association.
```

---

# 18. Limitations

MPLC has real limits:

```text
1. It does not include unaffected human controls.
2. It cannot prove epilepsy association.
3. It depends heavily on the matching policy.
4. It is sensitive to WES/WGS callability differences.
5. It may miss biology outside gene-proximal windows.
6. It may overfocus on known or GSC-prior biology.
7. n=12 limits recurrence power.
```

These are acceptable for a first RDGP demonstration if the claims are careful.

---

# 19. Edge cases

The main edge cases:

```text
1. Target loci are more callable than background loci.
2. Target loci are longer than background loci.
3. Target loci are more GC-rich or CpG-rich.
4. Target loci have more WES capture overlap.
5. Target loci are more constrained and therefore show fewer variants.
6. One patient drives the entire target burden.
7. Background pool accidentally includes poorly characterized disease loci.
8. A true signal lies outside the ±10 kb policy.
9. Rare variants are ancestry-specific rather than disease-relevant.
10. Noncoding variants project ambiguously to multiple genes.
```

---

# 20. Validation strategy

For MPLC, validation should include:

```text
1. Matching diagnostics
   Show target and background distributions for:
       callable bases
       gene length
       GC/CpG content
       mappability
       repeat fraction
       chromosome distribution
       gnomAD density, if available
       capture overlap, if WES

2. Burden diagnostics
   Show per-patient total burden.
   Flag if one patient dominates.

3. Null diagnostics
   Show the background null distribution.
   Show where the observed target statistic falls.

4. Window sensitivity
   Repeat with ±5 kb, ±10 kb, ±20 kb.

5. Variant-filter sensitivity
   Repeat with rare and ultra-rare filters.

6. Projection traceability
   Every burden count must trace back to source coordinates.

7. Anti-overclaim validation
   Results must be labeled hypothesis-generating.

8. Recurrence-unit audit
   Confirm sample recurrence, patient recurrence, and subject recurrence are
   not silently conflated.

9. Counting-unit audit
   Confirm burden counts use sample-specific variant observations unless a
   different counting unit is explicitly declared.

10. Phenotype-scope audit
    Confirm epilepsy, mitochondrial, broad, narrow, and combined prior scopes
    are analyzed under explicit target-locus policy and not silently merged.

11. Background-label audit
    Confirm matched background loci are described as non-prior matched loci,
    not nondisease genes or biological controls.

12. Daughter-surface boundary audit
    Confirm KVPS, GIRS, PAPS, RFPS, EVRS, PGERS, CUES, OACS, and RMCS
    references do not replace MPLC locus-membership traceability.

13. RMCS comparability audit
    Confirm MPLC surfaces generated under different target, background,
    window, variant-filter, opportunity, null-model, matching, GSC-release, or
    random-seed policies are not compared without explicit comparability state.

14. Interpretation-label audit
    Confirm MPLC labels remain exploratory and do not encode RDGP ranking,
    disease association, pathogenicity, causality, diagnosis, or clinical
    actionability.
```

---

# 21. Implementation relevance

For DEX-VDB, the “room boundaries” for MPLC are:

```text
VDB should emit:
    target locus sets
    matched background locus sets
    sample-locus burden matrices
    variant-locus memberships
    opportunity denominators
    null draw manifests
    matching diagnostics
    source-coordinate traceability

RDGP should consume:
    burden matrices
    recurrence matrices
    null distributions
    GSC prior labels
    validation receipts

RDGP should produce:
    prioritized candidate loci / regions
    not diagnostic conclusions
```

---

# Summary for MPLC Method Design

The proper design is:

```text
Matched Prior-Locus Contrast (MPLC)
```

The proper null is:

```text
GSC-prior loci are not more burdened than matched non-prior loci
after accounting for callable opportunity and genomic context.
```

The proper first implementation is:

```text
Use GSC to define target loci.
Use matched background loci to build an empirical null.
Use VAP-derived coordinate projections to count burden.
Use callable/opportunity denominators to normalize.
Use recurrence across patients to avoid one-sample artifacts.
Package everything in TEP-VDB so RDGP can reason transparently.
```

This gives RDGP a scientifically honest room to reason inside.

---

# 22. Daughter-Surface Summary Doctrine

MPLC is the TEP-VDB projection surface that compares phenotype-scoped GSC-prior
target loci against matched non-prior background loci using VAP-derived
sample-specific coordinate observations, opportunity-aware denominator context,
declared target/background/window/filter/null policies, recurrence summaries,
matching diagnostics, source traceability, uncertainty state, method currency,
and anti-overclaim boundaries so RDGP can reason over prior-informed burden
contrast without VDB claiming disease association, causality, pathogenicity, or
diagnosis.

In short:

```text
MPLC exposes matched prior-locus burden contrast.
RDGP reasons over that contrast.
Scientists and clinicians interpret evaluated evidence.
```
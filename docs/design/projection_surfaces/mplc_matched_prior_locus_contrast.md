# Matched Prior-Locus Contrast (MPLC)

> Status: SAGE-VDB scientific method design.
> This document defines the biological, mathematical, and evidentiary constraints
> for a VDB-emitted TEP-VDB projection surface. It is not a final implementation
> schema. DEX-VDB should derive implementation schemas, validators, and emission
> contracts from this design.

The Matched Prior-Locus Contrast (MPLC) method is a way for a priori evidence emanating from the Gene Set Consensus (GSC) repository to interface with patient variant information emanating from the Variant Annotation Pipeline (VAP) repository so that reasoning can be performed by the Rare Disease Gene Prioritization (RDGP) repository.

For our trial run, let's consider epilepsy manifestations in the clinical setting.

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
Across the 12 epilepsy patients,
how much rare coding / noncoding / regulatory / splice-proximal burden
appears near these loci?
```

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
After accounting for genomic opportunity, GSC-prior loci do not carry
more rare variant burden than matched non-prior background loci
in the same 12 epilepsy patients.
```

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

Conditional on callable opportunity, locus-window structure, and matching
features, GSC-prior target loci are exchangeable with matched non-prior
background loci with respect to rare variant burden in the 12 epilepsy patients.
```

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
    method_id
    method_version
    target_locus_policy_id
    background_matching_policy_id
    window_policy_id
    variant_filter_policy_id
    opportunity_model_id
    null_model_id
    number_of_null_draws
    random_seed

target_locus_set:
    target_set_id
    target_set_policy_id
    locus_id
    phenotype_scope
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
    source_gsc_trace

background_locus_pool:
    background_pool_policy_id
    locus_id
    background_gene_namespace
    background_gene_id
    background_gene_symbol
    chromosome
    window_start
    window_end
    matching_feature_values
    eligibility_status
    matching_eligible: true/false
    excluded_from_target_set: true/false
    excluded_due_to_gsc_prior: true/false
    excluded_due_to_overlap_with_target_window: true/false
    exclusion_reason_if_any

matched_locus_sets:
    draw_id
    target_locus_id
    matched_background_locus_id
    replacement_status
    matching_rank
    matching_distance
    matching_features_used
    matching_feature_summary
    random_seed
    matching_policy_id

sample_locus_burden_matrix:
    sample_id
    locus_id
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

patient_locus_hit_matrix:
    sample_id
    locus_id
    has_qualifying_variant
    qualifying_variant_count
    strongest_variant_class
    strongest_variant_handle
    hit_partition_label

variant_locus_memberships:
    variant_handle
    sample_id
    locus_id
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
    source_vap_trace

null_draw_manifest:
    draw_id
    target_locus_id
    selected_background_locus_id
    replacement_status
    random_seed
    matching_policy_id

mplc_results:
    statistic_name
    observed_target_value
    null_mean
    null_percentile
    exploratory_empirical_p_value
    interpretation_label

validation_receipts:
    source_corpus_integrity_pass
    coordinate_traceability_pass
    gsc_traceability_pass
    matching_diagnostics_pass
    opportunity_accounting_pass
    patient_dominance_audit_pass
    anti_overclaim_pass
```

That is enough substrate for RDGP to reason without needing to rediscover
VAP/GSC source evidence or independently overlay producer outputs.

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
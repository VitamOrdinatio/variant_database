# Coordinate-First Burden Scan (CFBS)

> Status: SAGE-VDB scientific method design.
> This document defines the biological, mathematical, and evidentiary constraints
> for a VDB-emitted TEP-VDB projection surface. It is not a final implementation
> schema. DEX-VDB should derive implementation schemas, validators, and emission
> contracts from this design.

The Coordinate-First Burden Scan (CFBS) utilizes genomic coordinates before invoking gene identifiers.

Plain-English version:

```text
CFBS asks where variants cluster in genome coordinate space first,
then asks afterward whether those regions overlap genes, regulatory elements,
or GSC-prior epilepsy / mitochondrial loci.
```

This is the discovery-preserving mode.

The MPLC method says:

```text
Start with GSC-prior loci, then compare against matched background loci.
```

CFBS says:

```text
Start with coordinates, nominate burden clusters, then annotate biology.
```

Both are valid. CFBS is broader and more discovery-oriented, but it pays a larger statistical penalty.

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

> DEX derivation note: object lists in this CFBS design are schema seeds, not
> final field contracts. DEX-VDB must normalize required/optional fields, data
> types, controlled vocabularies, validation profiles, and file names in derived
> implementation specifications before any builder is implemented.

---

# 1. What CFBS is trying to test

The scientific question is:

```text
Across the 12 epilepsy patients, are there genomic coordinate intervals
where qualifying variants cluster more than expected under a declared
genomic opportunity model?
```

Then, after those intervals are nominated:

```text
Are any nominated intervals near GSC-supported epilepsy or mitochondrial loci,
known disease genes, regulatory elements, conserved regions, or other plausible
biological features?
```

The order matters.

Correct CFBS order:

```text
coordinates → burden scan → candidate intervals → biological annotation
```

Incorrect order:

```text
GSC genes → only scan nearby regions → call it coordinate-first
```

GSC can still appear in the TEP-VDB as an annotation/projection layer, but for CFBS it should not define the scan windows.

---

# 2. Proper null hypothesis

For CFBS, the null is:

```text
After accounting for genomic opportunity, observed variants are not unusually
clustered in any coordinate interval.
```

Freshman biology version:

```text
If there are no special hotspot regions, then the variants should be spread
across the parts of the genome where VAP could have detected them, in a way
consistent with local background opportunity.
```

Important correction:

```text
The null is not uniform randomness across the whole genome.
```

The human genome is not a perfectly even playing field. Some regions are easier to sequence, easier to map, more mutation-prone, more repetitive, more constrained, or more polymorphic than others. So CFBS should use an opportunity-adjusted null, not a naïve “3 billion base pairs divided by total variants” model.

---

# 3. Better name for the null

I would call the CFBS null:

```text
Matched Genomic Opportunity Null
```

Abbreviation:

```text
MGO null
```

Plain-English version:

```text
A candidate hotspot is interesting only if it has more variant burden than
expected for a region with similar genomic and technical opportunity.
```

That phrase is important:

```text
similar genomic and technical opportunity
```

because variants do not appear equally everywhere.

---

# 4. Why uniform randomness is only a toy baseline

Your first mental model was:

```text
haploid genome ≈ 3 billion bp
T = total variants
expected spacing ≈ 3 billion / T
```

This is useful for intuition, but it is not biologically realistic.

A better mental model is:

```text
The genome is a landscape with uneven terrain.
Variants are more likely to be observed in some terrain than others.
```

Regions differ by:

```text
chromosome size
callable bases
coverage
mappability
repeat content
GC / CpG content
local mutation rate
population variant density
WES capture overlap
variant-calling reliability
selection / constraint
```

Scan-statistic methods exist because cluster detection generally requires comparing observed event counts to expected counts inside moving windows or regions, not simply looking at raw piles of events. Rare-variant scan methods such as SCANG and WGScan similarly use moving or sliding windows to detect association regions and their sizes, while STAARpipeline includes non-gene-centric sliding-window and dynamic-window analysis for large WGS/WES studies.

For our n=12 epilepsy case-only use, we borrow the scan geometry idea, not the full association-testing claim.

---

# 5. The core objects CFBS needs

For every genomic window `w`, TEP-VDB should give RDGP:

```text
window_id
chromosome
start
end
window_size
window_policy_id
callable_bases
observed_variant_count
rare_variant_count
noncoding_variant_count
patient_recurrence_count
expected_variant_count
observed_expected_ratio
empirical_null_percentile
source VAP coordinate traces
post hoc nearest gene annotations
post hoc GSC overlap annotations
```

For every patient `s` and window `w`:

```text
sample_id
window_id
variant_count
rare_variant_count
noncoding_variant_count
coding_variant_count
splice_proximal_count
callable_bases
burden_per_callable_base
```

For every variant-to-window membership:

```text
variant_handle
sample_id
chrom
pos
ref
alt
window_id
variant_class
frequency_bin
quality_state
source_vap_trace
```

That gives RDGP enough substrate to reason without flattening away provenance.


Implementation guardrail:

```text
coordinate_variant_handle:
    normalized coordinate/reference-context variant identity

sample_variant_observation_id:
    sample-specific observation of that variant

projection_membership_id:
    membership of that observation in a window, locus, feature, or annotation
```

Burden counts should operate over sample-specific coordinate observations, not
over duplicated annotation rows. Multiple transcript, feature, or post hoc GSC
mappings should create multiple memberships, not multiple observed variants.

---

# 6. The simplest math

Let:

```text
w = a genomic window
s = a patient
```

For a given window:

```text
N[w] = number of qualifying variants observed in window w
```

Example:

```text
N[chr2:1000000-1020000] = 7
```

That means seven qualifying variants were observed across the 12 patients in that 20 kb interval.

But raw count is not enough. You need the amount of genome where variants could have been detected:

```text
C[w] = callable opportunity in window w
```

Then:

```text
R[w] = N[w] / C[w]
```

Plain-English version:

```text
burden rate = variants observed / bases where variants could reasonably
have been observed
```

---

# 7. Expected burden

Under the MGO null, every window gets an expected count:

```text
E[w] = expected number of variants in window w
```

The simplest opportunity-adjusted version:

```text
E[w] = genome-wide variant rate × callable bases in w
```

Where:

```text
genome-wide variant rate =
    total qualifying variants / total callable bases
```

So:

```text
E[w] = (T / C_total) × C[w]
```

Freshman biology translation:

```text
If this window is 0.001% of the callable genome,
we expect about 0.001% of the variants to fall there,
unless something unusual is happening.
```

That is a better start than total genome size, because it uses callable genome rather than raw genome size.

---

# 8. Better expected burden

Eventually, expected burden should also consider matched context.

Instead of saying:

```text
all callable bases are equal
```

say:

```text
this window should be compared to other windows with similar properties
```

So each observed window is compared to matched background windows with similar:

```text
chromosome or chromosome class
callable length
GC / CpG content
mappability
repeat fraction
local gnomAD variant density
distance to TSS
variant class
WES capture overlap, if applicable
```

This gives us the Matched Genomic Opportunity Null (MGO Null).

---

# 9. How to build the null distribution

For each real scan, create many fake scans.

A fake scan should preserve the patient and variant structure that could
otherwise create false hotspot signals:

```text
same number of variants
same patient-level variant counts
same variant-class partitions where possible
same chromosome distribution, if desired
same callable territory
matched GC/mappability/repeat opportunity
```

The patient-level constraint should be treated as required for CFBS v1:

```text
For each sample s:
    preserve the number of qualifying variants from sample s
    preserve variant class partitions where possible
    randomize only within matched genomic opportunity space
```

Freshman biology translation:

```text
Given each patient's observed burden load, do variants cluster into the same
coordinate windows more than expected by matched random placement?
```

Then randomly place variants into matched allowable positions/windows.

Repeat this many times:

```text
fake scan 1
fake scan 2
fake scan 3
...
fake scan 10,000
```

For each fake scan, record both per-window scores and the strongest
genome-wide hotspot score.

```text
null_scope:
    per_window
    genomewide_max_statistic
```

Interpretation:

```text
per_window:
    asks whether this specific window is unusual

genomewide_max_statistic:
    asks whether this window is unusual after accounting for the fact
    that we searched many windows
```

The genomewide max-statistic null is safer for CFBS because CFBS searches many
windows. Per-window scores can still be reported as exploratory local evidence.

That gives RDGP a background distribution:

```text
How strong can a hotspot look just by chance
under matched genomic opportunity?
```

---

# 10. Exploratory empirical-null evidence

Suppose the real window has a hotspot score:

```text
S_real[w]
```

For 10,000 fake scans, calculate:

```text
S_fake_1
S_fake_2
...
S_fake_10000
```

Then CFBS may report an exploratory empirical tail probability:

```text
exploratory_empirical_p_value =
    (1 + number of fake scores >= real score)
    /
    (1 + number of fake scans)
```

Example:

```text
10,000 fake scans

real window is stronger than 9,950 fake maxima

50 fake scans had a hotspot as strong or stronger

exploratory_empirical_p_value = (1 + 50) / (1 + 10000)
exploratory_empirical_p_value ≈ 0.0051
```

Interpretation:

```text
Under the matched genomic opportunity null,
a hotspot this strong appears in about 0.5% of fake scans.
```

For n=12, this should be labeled exploratory empirical-null evidence, not formal disease association evidence.

---

# 11. What should the hotspot score be?

For CFBS v1, do not overcomplicate.

I would use three scores.

## Score 1: burden excess

```text
burden_excess[w] = observed variants / expected variants
```

In math:

```text
burden_excess[w] = N[w] / E[w]
```

Plain English:

```text
Did this window have more variants than expected?
```

---

## Score 2: patient recurrence

```text
K[w] = number of patients with ≥1 qualifying variant in window w
```

Plain English:

```text
Is this signal shared across multiple epilepsy patients,
or is it driven by one patient?
```

This is extremely important.

A window with 10 variants from one patient is less compelling than a window with 5 variants from 5 different patients.

---

## Score 3: cluster compactness

Within a larger window, are variants tightly grouped?

Simple version:

```text
compactness[w] =
    length of smallest sub-interval containing the variants
```

Plain English:

```text
Are the variants scattered across the full window,
or do they pile into a smaller local neighborhood?
```

For v1, I would prioritize burden and recurrence. Compactness can be added after the basics are stable.

---

# 12. Fixed windows versus sliding windows

You have two natural approaches.

## Fixed windows

Example:

```text
chr1:1-20000
chr1:20001-40000
chr1:40001-60000
...
```

Pros:

```text
simple
easy to explain
easy to validate
easy to reproduce
```

Cons:

```text
a real hotspot can be split across two adjacent windows
```

---

## Sliding windows

Example:

```text
20 kb window, sliding every 5 kb
```

Pros:

```text
less likely to miss boundary-crossing clusters
```

Cons:

```text
many more tests
more overlapping results
harder correction
```

For CFBS v1, I would start with fixed windows plus a simple merge rule:

```text
If adjacent high-scoring windows touch or overlap,
merge them into a candidate interval.
```

Then v2 can support sliding or dynamic windows. This long-term direction is aligned with established rare-variant scan practice, including scan-statistic and non-gene-centric windowing approaches. If any external method or software becomes normative for implementation, DEX-VDB should cite a specific versioned reference in the derived implementation specification rather than embedding an informal raw URL in this design document.

```text
candidate_interval_assembly_policy:
    merge_adjacent_significant_windows: true
    merge_distance_bp: 0
    max_gap_bp: optional
    ranking_statistic: burden_excess | recurrence | composite
    minimum_recurrence_count
    minimum_callable_bases
```

---

# 13. Proper CFBS null, formal version

```text
CFBS null hypothesis:

Conditional on callable opportunity, matched genomic context, patient-level
variant burden, and variant-class partition, qualifying variants from the
12 epilepsy patients are not more clustered in any coordinate interval than
expected under random placement within comparable genomic opportunity space.
```

Freshman biology translation:

```text
If there are no true hotspot-like regions, then the strongest clusters we see
in the real data should look like the strongest clusters we get after randomly
reshuffling each patient's variants into similar genomic neighborhoods.
```

That is the right null.

---

# 14. What “coordinate-first” really means

Coordinate-first does not mean biology is absent.

> Coordinate-first means biology is not allowed to choose the candidate windows before the scan.

The sequence is:

```text
1. Define genome-wide or callable-genome scan space.
2. Count variant burden by coordinate.
3. Rank candidate windows.
4. Only then annotate:
   nearest gene
   overlapping gene
   GSC epilepsy prior
   GSC mitochondrial prior
   promoter / enhancer / cCRE
   conservation
   known disease locus
```

This preserves discovery.

---

# 15. How GSC enters CFBS

For CFBS, GSC should enter after candidate intervals are detected.

TEP-VDB can still include GSC projections, but RDGP should treat them as post hoc annotations:

```text
coordinate-nominated interval
    → nearest gene
    → GSC overlap?
    → GSC prior tier?
    → phenotype scope?
```

Then RDGP can say:

```text
This interval was nominated without using GSC.
After nomination, it was found to lie near a GSC-prior epilepsy gene.
```

That is much stronger than:

```text
We looked near GSC genes and found a cluster.
```

Both are useful, but they answer different questions.


Post hoc GSC annotations must remain phenotype-scope aware. Epilepsy and
mitochondrial-disease GSC priors may both be present in the TEP-VDB, but CFBS
should not silently combine them into one disease-prior label unless an explicit
annotation policy declares that combined view.

---

# 16. Minimum viable CFBS v1

## Inputs

```text
one uniform TEP-VDB

TEP-VDB source corpus:
    12 epilepsy TEP-VAPs
    2 TEP-GSCs:
        epilepsy semantic priors
        mitochondrial disease semantic priors

TEP-VDB shared substrates:
    coordinate-normalized variant observations
    sample-specific observation handles
    genotype / zygosity / dosage fields where available
    variant quality states
    callable/opportunity approximation
    gene annotation overlays
    GSC prior overlays for post hoc interpretation
```

---

## Scan space

For v1:

```text
callable autosomal genome
```

or, if VAP/WES callability is limited:

```text
callable regions represented by the VAP cohort
```

Do not scan uncallable territory as if a zero means absence.

---

## Window policy

Start with:

```text
fixed_20kb_windows_v1
```

Also run sensitivity checks:

```text
fixed_5kb_windows_v1
fixed_10kb_windows_v1
fixed_50kb_windows_v1
```

Do not make 20 kb sacred.

---

## Variant filters

Use partitions:

```text
all qualifying variants
rare variants
ultra-rare variants
noncoding variants
coding/splice variants
SNVs only
indels separately
```

Noncoding should be one partition, not the only partition.

---

## Null

Start with two layers:

```text
Null 0:
    callable-length-adjusted uniform null

Null 1:
    matched genomic opportunity permutation null
```

Null 0 is for transparency/debugging. Null 1 is the real exploratory model.

---

## Outputs

```text
top candidate coordinate intervals
observed burden
expected burden
burden excess
patient recurrence
empirical null percentile
exploratory empirical tail probability
contributing variants
contributing patients
post hoc gene/GSC annotations
traceability receipts
artifact warnings
```

---

# 17. What TEP-VDB should emit for CFBS

TEP-VDB should define the room RDGP reasons inside.

For CFBS, that room is a coordinate-first projection surface inside one uniform
TEP-VDB. In the planned first epilepsy demonstration, that TEP-VDB uses the
14-source profile described above. Generic TEP-VDB schemas should not hard-code
that source count. GSC-derived fields are present as post hoc annotations, not
as scan-window selection rules.

For CFBS, emit:

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

cfbs_analysis_scope:
    method_id
    method_version
    scan_space_policy_id
    window_policy_id
    variant_filter_policy_id
    opportunity_model_id
    null_model_id
    posthoc_annotation_policy_id
    number_of_null_draws
    random_seed

scan_space:
    chromosome
    scan_start
    scan_end
    callable_bases
    included_status
    exclusion_reason

window_set:
    window_id
    chromosome
    start
    end
    window_size
    window_policy_id
    callable_bases
    gc_bin
    mappability_bin
    repeat_fraction_bin
    optional_gnomad_density_bin
    included_status
    exclusion_reason

sample_window_burden_matrix:
    sample_id
    window_id
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

patient_window_hit_matrix:
    sample_id
    window_id
    has_qualifying_variant
    qualifying_variant_count
    strongest_variant_class
    strongest_variant_handle
    hit_partition_label

variant_window_memberships:
    variant_handle
    sample_id
    window_id
    chrom
    pos
    ref
    alt
    variant_class
    consequence_partition
    frequency_bin
    quality_state
    frequency_source
    frequency_version
    frequency_status
    source_vap_trace

null_model:
    null_model_id
    null_model_type
    null_scope
    random_seed
    matching_features
    number_of_draws
    scan_space_policy_id
    preserve_patient_level_burden: true
    preserve_variant_class_partitions: true/false

null_draw_summary:
    draw_id
    max_burden_excess
    max_recurrence
    max_compactness
    selected_window_summary

candidate_interval_set:
    candidate_interval_id
    source_window_ids
    chromosome
    start
    end
    assembly_policy_id
    merge_rule
    ranking_statistic
    minimum_recurrence_count
    minimum_callable_bases

cfbs_results:
    window_id
    candidate_interval_id
    observed_count
    expected_count
    burden_excess
    patient_recurrence_count
    exploratory_empirical_p_value
    null_percentile
    candidate_label
    interpretation_label

posthoc_annotations:
    window_id
    candidate_interval_id
    nearest_gene
    overlapping_gene
    distance_to_gene
    gene_namespace
    gene_id
    gene_symbol
    gsc_epilepsy_overlap
    gsc_mitochondrial_overlap
    gsc_release_id
    gsc_phenotype_scope
    semantic_prior_id
    regulatory_feature_overlap
    annotation_policy_id

validation_receipts:
    source_corpus_integrity_pass
    coordinate_traceability_pass
    opportunity_accounting_pass
    null_model_pass
    patient_dominance_audit_pass
    posthoc_annotation_boundary_pass
    anti_overclaim_pass
```

This is enough for RDGP to reason without inventing its own substrate.

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

# 18. What not to do

Do not use raw genome length if callable territory is available.

Do not assume variants should be uniformly distributed.

Do not scan uncallable regions.

Do not let GSC define the coordinate-first windows.

Do not combine SNVs and indels without at least preserving partition labels.

Do not call candidate windows disease-associated.

Do not ignore patient recurrence.

Do not let one patient dominate the signal.

Do not annotate first and discover second.

Do not treat exploratory empirical tail probabilities as formal association
p-values.

---

# 19. Assumptions

For CFBS, I am assuming:

```text
1. The 12 samples are germline VAP outputs.
2. VDB has coordinate-normalized variant observations.
3. Callability is available or can be approximated.
4. The first goal is exploratory hotspot nomination.
5. GSC is used after coordinate nomination for interpretation.
6. RDGP consumes TEP-VDB projections, not raw VAP files.
```

---

# 20. Limitations

CFBS has real limits:

```text
1. n=12 gives limited recurrence power.
2. Case-only scans cannot prove disease association.
3. Uniform genome null is weak.
4. Matched opportunity null depends on matching quality.
5. WES-based noncoding scans are incomplete and capture-biased.
6. Multiple testing is severe for genome-wide windows.
7. Hotspots can reflect mapping or repeat artifacts.
8. Post hoc GSC overlap is supportive, not proof.
```

---

# 21. Edge cases

Watch for:

```text
1. A candidate interval is driven by one high-burden patient.
2. A candidate interval falls in a low-mappability region.
3. A candidate interval overlaps repeats or segmental duplications.
4. A candidate interval appears only because it is unusually callable.
5. A candidate interval is a common ancestry haplotype.
6. A real cluster is split across adjacent fixed windows.
7. A real signal is diluted by too-large windows.
8. A nearby GSC gene is not the true regulatory target.
9. GSC post hoc annotation creates narrative bias.
10. Indel artifacts inflate apparent clustering.
```

---

# 22. Validation strategy

For CFBS, validation should include:

```text
1. Coordinate survival
   Every candidate interval traces back to source VAP coordinates.

2. Scan-space audit
   Every scanned window has callable/opportunity status.

3. Null audit
   Null model is declared, versioned, and reproducible from random seed.

4. Patient dominance audit
   Flag windows where one sample contributes most of the burden.

5. Variant-class audit
   Report SNV, indel, coding, noncoding, and splice partitions separately.

6. Window sensitivity
   Repeat with 5 kb, 10 kb, 20 kb, and 50 kb windows.

7. Artifact audit
   Flag low-mappability, repetitive, segmental-duplication, or poor-callability windows.

8. Post hoc annotation boundary
   Confirm GSC/gene annotations were applied after coordinate ranking.

9. Empirical null audit
   Show where observed scores fall relative to fake scans.

10. Anti-overclaim validation
   Output must say exploratory coordinate hotspot candidate,
   not disease-associated or pathogenic region.
```

---

# 23. Implementation relevance

For DEX-VDB, CFBS means VDB needs to emit:

```text
scan window sets
scan-space inclusion/exclusion state
variant-window memberships
sample-window burden matrices
callable/opportunity denominators
null-model manifests
per-window observed/expected statistics
patient recurrence statistics
post hoc biological annotations
source-coordinate traceability
validation receipts
```

RDGP then consumes:

```text
ranked coordinate intervals
burden/recurrence/compactness scores
null distributions
GSC post hoc overlays
traceable contributing variants
```

RDGP produces:

```text
prioritized candidate regions and candidate nearby genes
```

not disease-causal claims.

---

# 24. Summary for the CFBS Method Design

The proper design is:

```text
Coordinate-First Burden Scan
```

The proper null is:

```text
Qualifying variants are not more clustered in any coordinate interval
than expected under a matched genomic opportunity model.
```

The proper first implementation is:

```text
Use VAP to define coordinate observations.
Use callable genome space to define where variants could have been seen.
Scan fixed coordinate windows.
Compare observed burden to expected burden under matched opportunity.
Rank windows by burden excess and patient recurrence.
Only after ranking, annotate genes, regulatory features, and GSC priors.
Package all windows, counts, null draws, annotations, and traceability into TEP-VDB.
```

The key scientific identity is:

```text
CFBS lets VDB ask where the genome itself points first.
RDGP asks what the biology might mean afterward.
```
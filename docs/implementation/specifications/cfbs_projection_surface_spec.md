# CFBS Projection Surface Specification

> Status: DEX-VDB implementation specification.  
> Derived from: `docs/design/opportunity_space_and_projection_policy_model.md` and
> `docs/design/projection_surfaces/cfbs_coordinate_first_burden_scan.md`.  
> Depends on:
> `docs/implementation/specifications/opportunity_space_spec.md`,
> `docs/implementation/specifications/projection_policy_registry_spec.md`, and
> `docs/implementation/schemas/tep_vdb_projection_surface_schema.md`.

## 1. Purpose

This document specifies the implementation-facing shape of the Coordinate-First
Burden Scan (CFBS) projection surface emitted by VDB inside TEP-VDB.

CFBS is a coordinate-first discovery surface. It asks whether qualifying
sample-specific variant observations cluster in genomic coordinate intervals
more than expected under a declared genomic opportunity model.

The core CFBS order is:

```text
coordinate observations
    → scan-space declaration
        → windowed burden counting
            → candidate interval nomination
                → post hoc biological annotation
                    → RDGP reasoning
```

CFBS must not allow gene, GSC, disease-prior, or RDGP labels to select candidate
windows before the coordinate scan. Those biological overlays may be applied only
after candidate intervals are nominated from coordinate-space burden evidence.

> CFBS may emit `exploratory_empirical_p_value` as an empirical tail probability
> under the declared matched genomic opportunity null. This value is useful for
> ranking and hypothesis generation, but it must not be interpreted as a
> control-matched disease-association p-value.

## 2. Scope

This specification defines the CFBS method room inside a TEP-VDB projection
surface package. It defines required logical artifacts, required fields,
controlled vocabularies, counting rules, scan-space rules, null-model rules,
post hoc annotation rules, result labels, validation checks, and failure modes.

This specification applies to CFBS surfaces emitted by VDB for RDGP consumption.
It is intended to be strict enough for validators and future builders while
remaining independent of concrete Python module names, database table names, or
execution plans.

## 3. Non-Goals

This document does not define the generic TEP-VDB package schema.

This document does not define opportunity-state semantics. Those are owned by
`docs/implementation/specifications/opportunity_space_spec.md`.

This document does not define the projection policy registry. Policy identity,
policy versioning, policy dependencies, lossiness, and reversibility are owned by
`docs/implementation/specifications/projection_policy_registry_spec.md`.

This document does not define MPLC.

This document does not define RDGP scoring, diagnosis, or prioritization logic.

This document does not define executable builders, validators, or implementation
plans.

## 4. Method Invariant

CFBS preserves the following invariant:

```text
CFBS candidate intervals are nominated from coordinate-space burden patterns
before gene, GSC, disease-prior, or RDGP labels are used for interpretation.
```

The following sequence is valid:

```text
coordinates → burden scan → candidate intervals → biological annotation
```

The following sequence is invalid for CFBS:

```text
GSC genes → restricted scan windows → coordinate-labeled result
```

A CFBS surface may contain GSC and gene annotations, but those annotations must
be post hoc overlays on coordinate-nominated candidate intervals. They must not
be scan-window selection inputs unless the method is explicitly reclassified as a
prior-informed method rather than CFBS.

## 5. Relationship to the Shared TEP-VDB Schema

CFBS is a method-specific projection surface inside the shared TEP-VDB package
schema:

```text
tep_vdb/
    shared_substrates/
        coordinate_observations
        sample_variant_observations
        opportunity_space
        projection_policy_registry
        source_traceability

    projection_surfaces/
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

The shared TEP-VDB schema owns package identity, source-corpus identity, shared
substrate indexes, projection-surface indexes, method manifests, and package-wide
validation receipts. This specification owns only the CFBS method room.

CFBS must consume the shared source corpus and shared substrates emitted by VDB.
RDGP must not re-ingest VAP or GSC producer packages to reconstruct CFBS.

## 6. Relationship to Opportunity Space

CFBS is burden-based and therefore denominator-dependent.

Every CFBS burden, rate, observed/expected statistic, null distribution, or
candidate interval result must declare an `opportunity_model_id` or explicitly
mark opportunity as unmodeled. A CFBS surface must not declare burden readiness
when opportunity is unavailable, ambiguous, or inferred only from observed
variant positions.

CFBS may support multiple denominator strengths:

```text
true sample-specific callable intervals
region-level callable approximation
assay-scope approximation
opportunity_unmodeled
```

Approximate opportunity is allowed only when its approximation status is explicit
and the emitted surface is labeled appropriately, for example
`exploratory_only` or `not_burden_ready`.

Observed variants are numerator evidence. They must never be treated as the
opportunity denominator.

## 7. Relationship to the Projection Policy Registry

CFBS must reference registered policy identifiers rather than redefining mapping,
windowing, filtering, null, annotation, and emission rules inline.

At minimum, a CFBS surface must reference:

```text
scan_space_policy_id
window_policy_id
variant_filter_policy_id
variant_class_partition_policy_id
opportunity_model_id
null_model_id
candidate_interval_assembly_policy_id
posthoc_annotation_policy_id
emission_policy_id
```

Optional CFBS policy references include:

```text
quality_policy_id
frequency_filter_policy_id
mappability_annotation_policy_id
repeat_annotation_policy_id
window_sensitivity_policy_id
anti_overclaim_policy_id
```

A CFBS scan-window policy may depend on coordinate and technical substrates such
as genome build, scan-space policy, opportunity model, variant filter policy,
variant-class partition policy, and quality policy.

A CFBS scan-window policy must not depend on:

```text
GSC prior labels
nearest-gene annotations
known disease gene labels
RDGP rankings
post hoc annotation outputs
candidate gene narratives
```

## 8. Required Logical Artifacts

A CFBS projection surface must contain, or explicitly declare the absence of, the
following logical artifacts:

```text
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

Artifacts may be represented as TSV, JSON, Parquet, SQLite tables, or another
future controlled representation. This specification defines logical schema
requirements, not physical storage format.

## 9. Required Fields by Artifact

### 9.1 `cfbs_analysis_scope`

Required fields:

```text
tep_vdb_id
projection_surface_id
method_id
method_version
source_corpus_id
genome_build
scan_space_policy_id
window_policy_id
variant_filter_policy_id
variant_class_partition_policy_id
opportunity_model_id
null_model_id
candidate_interval_assembly_policy_id
posthoc_annotation_policy_id
number_of_null_draws
random_seed
burden_readiness_status
anti_overclaim_label_set
```

`method_id` should be `cfbs` unless a future controlled vocabulary defines a more
specific CFBS subtype.

### 9.2 `scan_space`

Required fields:

```text
scan_space_id
scan_space_policy_id
genome_build
chromosome
scan_start
scan_end
region_type
included_status
exclusion_reason
opportunity_model_id
total_bases
assayed_bases
callable_bases
not_callable_bases
not_assayed_bases
low_confidence_bases
unknown_opportunity_bases
source_traceability_id
```

`scan_space` defines the coordinate universe eligible for windowing. It must not
silently include uncallable or not-assayed territory as if zero observed variants
represented biological absence.

### 9.3 `window_set`

Required fields:

```text
window_id
scan_space_id
window_policy_id
genome_build
chromosome
start
end
window_size_bp
stride_bp
window_type
included_status
exclusion_reason
total_bases
assayed_bases
callable_bases
not_callable_bases
not_assayed_bases
unknown_opportunity_bases
gc_bin
mappability_bin
repeat_fraction_bin
optional_gnomad_density_bin
source_traceability_id
```

`window_set` defines coordinate windows, not candidate biological conclusions.

### 9.4 `sample_window_burden_matrix`

Required fields:

```text
sample_id
source_tep_id
window_id
variant_filter_policy_id
variant_class_partition
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
unknown_opportunity_bases
burden_readiness_status
source_traceability_id
```

Rows should be interpreted as sample-by-window burden summaries under declared
variant filters and opportunity model.

### 9.5 `patient_window_hit_matrix`

Required fields:

```text
sample_id
source_tep_id
window_id
has_qualifying_variant
qualifying_variant_count
strongest_variant_class
strongest_variant_handle
hit_partition_label
patient_dominance_flag
source_traceability_id
```

This matrix supports recurrence and patient-dominance auditing. It must not be
reconstructed from final result labels alone.

### 9.6 `variant_window_memberships`

Required fields:

```text
projection_membership_id
coordinate_variant_handle
sample_variant_observation_id
sample_id
source_tep_id
window_id
genome_build
chromosome
position_start
position_end
ref
alt
variant_class
consequence_partition
frequency_bin
frequency_source
frequency_version
frequency_status
quality_state
membership_policy_id
source_vap_trace
source_traceability_id
```

Each row represents membership of one sample-specific coordinate observation in
one window. It does not represent a new variant if the same observation has other
memberships.

### 9.7 `null_model`

Required fields:

```text
null_model_id
null_model_type
null_scope
scan_space_policy_id
window_policy_id
opportunity_model_id
variant_filter_policy_id
matching_features
number_of_draws
random_seed
preserve_patient_level_burden
preserve_variant_class_partitions
preserve_chromosome_distribution
source_traceability_id
```

CFBS null models must be opportunity-aware. A uniform whole-genome null may be
included only as a transparent diagnostic baseline, not as the primary CFBS
exploratory model when opportunity-aware alternatives are available.

### 9.8 `null_draw_summary`

Required fields:

```text
draw_id
null_model_id
random_seed
max_burden_excess
max_recurrence
max_compactness
selected_window_summary
null_scope
source_traceability_id
```

The null draw summary should support both local and genomewide interpretation.
The genomewide max-statistic null is the preferred primary correction context for
CFBS because CFBS scans many windows.

### 9.9 `candidate_interval_set`

Required fields:

```text
candidate_interval_id
candidate_interval_assembly_policy_id
source_window_ids
genome_build
chromosome
start
end
merge_rule
ranking_statistic
minimum_recurrence_count
minimum_callable_bases
candidate_interval_label
burden_readiness_status
source_traceability_id
```

Candidate intervals are assembled from coordinate-nominated windows. They must
not be created from gene or GSC labels before the coordinate scan.

### 9.10 `posthoc_annotations`

Required fields:

```text
annotation_id
candidate_interval_id
window_id
posthoc_annotation_policy_id
annotation_type
gene_namespace
gene_id
gene_symbol
distance_to_gene
gsc_release_id
gsc_phenotype_scope
semantic_prior_id
regulatory_feature_id
annotation_timing
source_traceability_id
```

Required value:

```text
annotation_timing = post_candidate_nomination
```

Post hoc annotations may support RDGP interpretation, but they must not be used
to define CFBS scan windows or nominate candidate intervals.

### 9.11 `cfbs_results`

Required fields:

```text
window_id
candidate_interval_id
observed_count
expected_count
burden_excess
patient_recurrence_count
exploratory_empirical_p_value
null_percentile
null_scope
candidate_label
interpretation_label
burden_readiness_status
anti_overclaim_label
source_traceability_id
```

`exploratory_empirical_p_value` is an exploratory empirical-tail probability
under the declared null model. It must not be emitted or interpreted as a formal
association p-value.

### 9.12 `cfbs_validation_receipts`

Required fields:

```text
validation_check
validation_status
severity
message
artifact_id
policy_id
source_traceability_id
```

Validation receipts should be machine-readable enough for future validators and
human-readable enough for audit.

## 10. Controlled Vocabularies

### 10.1 `included_status`

Allowed values:

```text
included
excluded
partially_included
opportunity_unmodeled
unknown
```

### 10.2 `window_type`

Allowed values:

```text
fixed
sliding
dynamic
merged_candidate_interval_source
```

### 10.3 `variant_class_partition`

Allowed values should include:

```text
all_qualifying
snv
indel
coding
noncoding
splice_proximal
rare
ultra_rare
other_declared_partition
```

The partition policy must be declared in the projection policy registry.

### 10.4 `null_model_type`

Allowed values:

```text
callable_length_adjusted_uniform_null
matched_genomic_opportunity_null
matched_genomic_opportunity_permutation_null
diagnostic_uniform_null
opportunity_unmodeled_null
```

The matched genomic opportunity null is the primary CFBS v1 null family. Uniform
nulls are diagnostic baselines unless explicitly justified otherwise.

### 10.5 `null_scope`

Allowed values:

```text
per_window
genomewide_max_statistic
both
```

### 10.6 `burden_readiness_status`

Allowed values:

```text
burden_ready
exploratory_only
not_burden_ready
denominator_unavailable
```

### 10.7 `candidate_label`

Allowed values:

```text
exploratory_coordinate_hotspot_candidate
burden_excess_signal
recurrence_signal
opportunity_limited_signal
artifact_warning
insufficient_opportunity_support
```

### 10.8 Forbidden interpretation labels

The following labels must not be emitted by CFBS:

```text
disease_associated_region
pathogenic_region
causal_locus
diagnostic_result
validated_association
```

## 11. Counting and Identity Rules

CFBS burden counts must operate over sample-specific coordinate observations.

The required identity hierarchy is:

```text
coordinate_variant_handle:
    normalized coordinate/reference-context variant identity

sample_variant_observation_id:
    sample-specific observation of that coordinate variant

projection_membership_id:
    membership of that sample-specific observation in a window, candidate
    interval, feature, or post hoc annotation
```

The countable unit for burden is `sample_variant_observation_id` after applying
declared variant filters.

The following must not be treated as separate countable variant observations:

```text
multiple transcript consequence rows
multiple gene-overlap rows
multiple regulatory-feature memberships
multiple GSC post hoc overlaps
multiple candidate-interval annotation rows
```

Those are projection or annotation memberships, not additional variants.

## 12. Scan-Space Rules

A CFBS scan space must be declared before windowing.

For v1, acceptable scan-space policies include:

```text
callable_autosomal_genome_v1
cohort_represented_callable_regions_v1
assay_scope_approximate_regions_v1
```

If true callability is unavailable, the scan space must not be silently treated
as fully callable. It must declare an approximation or unmodeled opportunity
state.

Scan space must preserve genome build and coordinate system. A CFBS surface must
not mix genome builds inside one scan space.

WES-derived CFBS scan spaces must preserve capture or assay-scope limitations.
Noncoding CFBS over WES-derived samples must be labeled opportunity-limited or
exploratory unless a stronger opportunity basis is available.

## 13. Window-Set Rules

For CFBS v1, the preferred primary window policy is:

```text
fixed_20kb_windows_v1
```

Recommended sensitivity policies include:

```text
fixed_5kb_windows_v1
fixed_10kb_windows_v1
fixed_50kb_windows_v1
```

The window policy must declare:

```text
window_size_bp
stride_bp
coordinate inclusivity convention
chromosome boundary handling
minimum_callable_bases
exclusion rules
```

Adjacent windows may be assembled into candidate intervals only through a
registered candidate interval assembly policy.

## 14. Null Model Rules

CFBS must use an opportunity-aware null model when reporting burden or hotspot
signals.

The primary CFBS v1 null should preserve:

```text
patient-level qualifying variant counts
variant-class partitions where possible
scan-space eligibility
callable or assayed opportunity
matching features such as GC, mappability, repeat fraction, and population
variant density when available
```

CFBS may report both:

```text
per_window exploratory evidence
genomewide_max_statistic exploratory evidence
```

The genomewide max-statistic context should be preferred for primary candidate
ranking because CFBS searches many windows.

All null draws must declare a random seed, null model ID, number of draws, and
matching features. Null results that cannot be reproduced from declared policy
and seed must fail validation or be labeled non-reproducible.

## 15. Candidate Interval Assembly Rules

Candidate intervals are derived from high-scoring coordinate windows under a
registered assembly policy.

A v1 assembly policy may use:

```text
merge_adjacent_significant_windows: true
merge_distance_bp: 0
max_gap_bp: optional
ranking_statistic: burden_excess | recurrence | composite
minimum_recurrence_count
minimum_callable_bases
```

Candidate interval assembly must preserve the source window IDs that led to the
interval. Candidate intervals must not hide the window-level evidence used to
create them.

Candidate intervals are exploratory coordinate hotspot candidates, not biological
loci, disease regions, pathogenic intervals, or RDGP conclusions.

## 16. Post Hoc Annotation Rules

CFBS post hoc annotations may include:

```text
nearest gene
overlapping gene
distance to gene
GSC epilepsy prior overlap
GSC mitochondrial prior overlap
GSC phenotype scope
semantic prior ID
regulatory feature overlap
conservation annotation
known disease locus annotation
artifact annotation
```

All post hoc annotations must declare an annotation policy ID and must include
`annotation_timing = post_candidate_nomination`.

Epilepsy and mitochondrial-disease GSC priors must remain phenotype-scope aware.
They must not be silently combined into a single disease-prior label unless a
registered annotation or projection policy explicitly declares that combined
view.

A CFBS validation receipt must confirm that post hoc annotations were applied
after coordinate ranking and candidate interval nomination.

## 17. Result Labeling and Anti-Overclaim Rules

CFBS may emit labels such as:

```text
exploratory_coordinate_hotspot_candidate
exploratory_empirical_null_evidence
burden_excess_signal
recurrence_signal
opportunity_limited_signal
artifact_warning
insufficient_opportunity_support
```

CFBS must not emit labels such as:

```text
disease_associated_region
pathogenic_region
causal_locus
diagnostic_result
validated_association
```

The field `exploratory_empirical_p_value` must be described as an exploratory
empirical-tail probability under the declared null model. It must not be treated
as a formal disease-association p-value.

## 18. Validation Rules

A CFBS projection surface must support the following validation checks:

```text
source_corpus_integrity_validation
coordinate_survival_validation
scan_space_opportunity_validation
window_policy_validation
sample_observation_counting_validation
variant_class_partition_validation
patient_dominance_validation
null_model_reproducibility_validation
genomewide_multiple_scan_audit
candidate_interval_assembly_validation
posthoc_annotation_boundary_validation
gsc_phenotype_scope_validation
artifact_region_warning_validation
anti_overclaim_validation
```

### 18.1 Source corpus integrity validation

The surface must trace to one TEP-VDB source corpus and must not require RDGP to
re-ingest VAP or GSC packages.

### 18.2 Coordinate survival validation

Every burden count, window membership, candidate interval, and CFBS result must
trace to source coordinate observations.

### 18.3 Scan-space opportunity validation

Every scanned region and window must declare opportunity status. Unknown or
unmodeled opportunity must not be coerced to zero.

### 18.4 Sample-observation counting validation

Burden counts must count sample-specific coordinate observations, not annotation
rows or duplicated projection memberships.

### 18.5 Patient dominance validation

Candidate windows and intervals should be flagged when one sample contributes a
large fraction of the burden. The threshold should be declared in policy.

### 18.6 Null model reproducibility validation

Null results must declare model ID, random seed, matching features, and number of
draws.

### 18.7 Post hoc annotation boundary validation

The validator must confirm that GSC, gene, disease-prior, and RDGP-derived labels
were not used to select scan windows or nominate candidate intervals.

### 18.8 Anti-overclaim validation

CFBS outputs must use exploratory labels and must not claim causality,
pathogenicity, diagnostic status, or validated disease association.

## 19. Failure Modes

CFBS surfaces should fail validation or emit hard warnings for the following
conditions:

```text
scan windows selected using GSC or disease-prior labels before coordinate scan
missing opportunity_model_id for burden-ready outputs
observed variants used as denominator opportunity
uncallable or not-assayed regions treated as zero-burden absence
sample-observation IDs absent from burden-relevant membership tables
annotation rows counted as independent variants
no random seed or null model ID for empirical null results
per-window p-values presented as genomewide-corrected results
post hoc annotation timing missing or upstream of candidate nomination
GSC phenotype scopes silently combined
forbidden interpretation labels emitted
```

## 20. Future Extensions

Future CFBS versions may add:

```text
sliding-window policies
dynamic-window policies
multi-scale scan statistics
variant-class-specific nulls
sample-specific callable interval masks
population-stratified opportunity models
ancestry-aware artifact audits
regulatory-domain-aware post hoc annotations
long-read or structural-variant CFBS extensions
formal external-control association models
```

These extensions must preserve the CFBS invariant: candidate intervals are
nominated from coordinate-space burden evidence before biological annotations are
used for interpretation.

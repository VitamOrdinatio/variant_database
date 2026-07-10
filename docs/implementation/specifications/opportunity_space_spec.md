# Opportunity Space Specification

> Status: DEX-VDB implementation specification.
> This document derives implementation-facing opportunity-space requirements
> from `docs/design/opportunity_space_and_projection_policy_model.md` and its
> MPLC / CFBS daughter method designs. It defines denominator substrate
> semantics, logical artifacts, controlled vocabularies, validation rules, and
> burden-readiness boundaries for future VDB-emitted TEP-VDB projection surfaces.

## 1. Purpose

This specification defines how VDB represents **opportunity space**: the
coordinate, region, feature, or sample-specific territory in which evidence
could have been observed given assay scope, callability, quality, filtering,
variant-class eligibility, and declared model constraints.

Opportunity space is the denominator substrate for burden, recurrence,
convergence, and projection-surface reasoning.

The governing rule is:

```text
Coordinate evidence tells VDB what was observed.
Opportunity space tells VDB what could have been observed.
```

A VDB burden surface must not treat missing technical opportunity as biological
absence.

## 2. Scope

This specification defines:

```text
opportunity model levels
opportunity logical artifacts
required and optional fields
controlled vocabularies
WES / WGS denominator semantics
burden-readiness rules
validation requirements
failure modes
```

This specification applies to future TEP-VDB projection surfaces, including but
not limited to:

```text
Matched Prior-Locus Contrast (MPLC)
Coordinate-First Burden Scan (CFBS)
future burden, recurrence, or convergence surfaces
```

## 3. Non-Goals

This specification does not define final MPLC or CFBS schemas.

This specification does not define a complete Convergence Geometry schema.

This specification does not define a final TEP-VDB package layout.

This specification does not require perfect per-base callability before VDB can
preserve opportunity states.

This specification does not allow burden-ready claims without a declared
opportunity basis.

This specification does not allow observed variant locations to be used as the
opportunity denominator.

## 4. Core Invariant

VDB must preserve the distinction:

```text
observation ≠ opportunity ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

Observed variants are numerator evidence. They are not denominator opportunity.

Opportunity space may be precise, approximate, unavailable, or explicitly
unmodeled. The absence of perfect opportunity data is acceptable only if the
state is explicit and propagated into downstream validation receipts.

## 5. Relationship to Current VDB Phases

Current VDB Phase 3 / Phase 4 work preserves evidence and topology substrate:

```text
package metadata
coordinate declarations
feature declarations
coordinate declaration sets
feature declaration sets
evidence topology handles
```

Opportunity space is a downstream denominator layer. It should be declared before
VDB emits burden-ready Convergence Geometry or TEP-VDB projection surfaces.

The intended ordering is:

```text
Phase 3 / 4.3 / 4.4 evidence preservation
    → opportunity-space declaration
        → projection-policy registry
            → projection memberships
                → opportunity-aware geometry
                    → TEP-VDB projection surfaces
                        → RDGP reasoning
```

## 6. Opportunity Model Levels

VDB should support staged opportunity modeling. Higher levels are more
interpretable, but lower levels remain useful if they are explicitly labeled.

```text
Level 0: opportunity_unmodeled
    No denominator is available or safely inferred.
    Burden-ready claims are prohibited.

Level 1: assay_scope_approximation
    Opportunity is approximated from assay type, capture scope, known source
    package metadata, or declared producer configuration.
    Burden surfaces may be exploratory-only.

Level 2: region_level_approximation
    Opportunity is estimated at region/window/locus level from coarse coverage,
    capture overlap, or declared inclusion/exclusion status.
    Burden surfaces may be exploratory-only or limited burden-ready if validators
    pass and limitations are emitted.

Level 3: sample_region_callable_approximation
    Opportunity is estimated per sample and region/window/locus using callable
    intervals, coverage masks, or equivalent sample-specific denominator inputs.
    This is the first strong denominator level for sample-aware burden surfaces.

Level 4: variant_class_specific_callable_opportunity
    Opportunity is sample-specific, region-specific, and variant-class-specific.
    This is the strongest denominator level for burden, recurrence, and matched
    genomic opportunity models.
```

The implementation must never silently upgrade a lower level into a stronger
level.

## 7. Required Logical Artifacts

The opportunity-space layer should be represented by five logical artifacts.
The physical format may be TSV, JSON, Parquet, SQLite, or another declared
TEP-VDB serialization format in later schema documents.

```text
opportunity_model_manifest
opportunity_region_set
sample_region_opportunity_matrix
opportunity_source_index
opportunity_validation_receipts
```

### 7.1 `opportunity_model_manifest`

The manifest defines the opportunity model, its version, corpus scope, source
basis, readiness state, and limitations.

Minimum fields:

```text
opportunity_model_id
opportunity_model_version
opportunity_model_type
opportunity_basis_kind
opportunity_model_level
source_corpus_id
source_tep_count
vap_tep_count
gsc_tep_count
genome_build
assay_scope_policy_id
callability_policy_id
variant_class_policy_id
projection_policy_dependencies
callability_source_status
assay_scope_source_status
burden_readiness_status
limitations
created_by
created_at_utc
```

### 7.2 `opportunity_region_set`

The region set defines the coordinate or feature regions whose opportunity is
being evaluated.

Minimum fields:

```text
region_id
region_namespace
region_type
genome_build
chromosome
start
end
region_length_bp
region_policy_id
region_source
included_status
exclusion_reason
payload_json
```

Examples of `region_type`:

```text
genomic_window
gene_locus_window
capture_interval
callable_interval
scan_space_segment
candidate_interval
feature_region
```

### 7.3 `sample_region_opportunity_matrix`

The sample-region matrix is the core denominator artifact. It declares how much
of each region was assayed, callable, not callable, not assayed, filtered,
low-confidence, or unknown for each sample and variant-class partition.

Minimum fields:

```text
sample_id
run_id
source_package_id
assay_type
genome_build
region_id
variant_class_partition
opportunity_model_id
opportunity_basis_kind
opportunity_state
assay_scope_status
callability_status
quality_scope_status
total_region_bases
assayed_bases
callable_bases
not_callable_bases
not_assayed_bases
low_confidence_bases
filtered_bases
unknown_opportunity_bases
burden_readiness_status
source_trace
payload_json
```

Numeric base-count fields must be non-negative integers. Unknown counts should
be represented explicitly rather than coerced to zero.

### 7.4 `opportunity_source_index`

The source index records where denominator claims came from.

Minimum fields:

```text
source_artifact_id
source_artifact_kind
source_artifact_path
producer_family
source_package_id
run_id
checksum_if_available
derivation_role
source_status
notes
```

Examples of `source_artifact_kind`:

```text
callable_bed
capture_bed
coverage_summary
alignment_metric
variant_calling_mask
reference_genome_metadata
producer_config
manual_policy_declaration
unavailable
```

### 7.5 `opportunity_validation_receipts`

Validation receipts record whether opportunity-space artifacts are internally
coherent and safe for burden-aware downstream surfaces.

Minimum fields:

```text
validation_id
opportunity_model_id
validation_check
validation_status
severity
observed_value
expected_value
message
source_artifact_id
created_at_utc
```

## 8. Controlled Vocabularies

### 8.1 `opportunity_basis_kind`

Allowed values:

```text
callable_interval_mask
capture_interval_mask
coverage_threshold_model
assay_scope_approximation
region_level_approximation
sample_region_callable_approximation
variant_class_specific_callable_opportunity
opportunity_unmodeled
```

Disallowed as a denominator:

```text
observed_variants_only
```

`observed_variants_only` may appear only as a diagnostic warning or failure
condition. It must not support burden-ready surfaces.

### 8.2 `opportunity_state`

Allowed values:

```text
callable
partially_callable
not_callable
not_assayed
low_confidence
filtered
unknown
opportunity_unmodeled
```

### 8.3 `assay_scope_status`

Allowed values:

```text
genome_wide
capture_limited
targeted_panel_limited
region_limited
not_assayed
unknown_assay_scope
```

### 8.4 `callability_status`

Allowed values:

```text
callable
partially_callable
not_callable
callability_unknown
callability_unmodeled
```

### 8.5 `quality_scope_status`

Allowed values:

```text
quality_supported
low_confidence
filtered
quality_unknown
quality_unmodeled
```

### 8.6 `burden_readiness_status`

Allowed values:

```text
burden_ready
exploratory_only
not_burden_ready
denominator_unavailable
```

### 8.7 `included_status`

Allowed values:

```text
included
excluded
partially_included
unknown
```

### 8.8 `validation_status`

Allowed values:

```text
pass
warn
fail
not_applicable
```

### 8.9 `severity`

Allowed values:

```text
info
warning
error
critical
```

## 9. Base-Count Semantics

For a given sample, region, and variant-class partition:

```text
total_region_bases >= 0
assayed_bases >= 0
callable_bases >= 0
not_callable_bases >= 0
not_assayed_bases >= 0
low_confidence_bases >= 0
filtered_bases >= 0
unknown_opportunity_bases >= 0
```

Required inequalities:

```text
callable_bases <= assayed_bases
assayed_bases <= total_region_bases
not_assayed_bases <= total_region_bases
```

Recommended partition check:

```text
assayed_bases + not_assayed_bases + unknown_opportunity_bases
    should not exceed total_region_bases
```

If the implementation cannot guarantee exact additive partitioning, it must emit
a warning receipt and describe the approximation in `payload_json`.

## 10. WES and WGS Semantics

WES and WGS opportunity spaces must not be silently merged.

For WES:

```text
assay_scope_status = capture_limited or region_limited
absence outside captured / callable territory is not biological absence
noncoding observations may exist but must remain opportunity-limited
noncoding burden surfaces require explicit capture/opportunity limitations
```

For WGS:

```text
assay_scope_status = genome_wide
callability is still shaped by coverage, mappability, repeats, GC content,
alignment ambiguity, variant class, and quality filtering
```

Any cross-assay opportunity harmonization must declare a policy ID and emit a
validation receipt.

## 11. Variant-Class Semantics

Opportunity may differ by variant class. A region callable for SNVs may not be
equivalently callable for indels, structural variants, splice-proximal variants,
or noncoding/regulatory partitions.

Allowed initial `variant_class_partition` values:

```text
all_qualifying
snv
indel
coding
noncoding
splice_proximal
regulatory_candidate
ultra_rare
rare
unknown_partition
```

Derived specs may refine this vocabulary. Unknown or unresolved partitions must
not be coerced into rare, coding, noncoding, or callable categories.

## 12. Burden-Readiness Rules

A projection surface may declare `burden_ready` only if all of the following hold:

```text
1. opportunity_model_id is present.
2. opportunity_basis_kind is not opportunity_unmodeled.
3. observed_variants_only is not used as a denominator.
4. region_id values are traceable to genome_build-specific coordinates.
5. sample_id / run_id / source_package_id traceability is present.
6. callable_bases or equivalent denominator fields are present for the method.
7. zero-burden states distinguish absent_with_opportunity, not_callable,
   not_assayed, filtered, low_confidence, and unknown where applicable.
8. validation receipts contain no critical failures.
```

A projection surface may declare `exploratory_only` if denominator support is
approximate but explicit.

A projection surface must declare `not_burden_ready` or
`denominator_unavailable` if opportunity is unmodeled or denominator fields are
missing.

## 13. Relationship to MPLC

MPLC requires sample-locus opportunity denominators.

At minimum, the opportunity layer must support:

```text
sample_id
locus or gene-window region_id
callable_bases
not_assayed_bases
not_callable_bases
opportunity_model_id
burden_readiness_status
```

MPLC matching policies may use opportunity-related features such as:

```text
callable length
assayed length
capture overlap
GC / CpG bin
mappability bin
repeat fraction bin
local population variant density bin
```

If those features are not available, MPLC must emit matching-diagnostic warnings
and must not overstate burden excess.

## 14. Relationship to CFBS

CFBS requires sample-window and scan-space opportunity denominators.

At minimum, the opportunity layer must support:

```text
scan-space inclusion / exclusion
window region_id
sample-window callable_bases
sample-window not_assayed_bases
sample-window not_callable_bases
opportunity_model_id
burden_readiness_status
```

CFBS must not scan uncallable or not-assayed territory as if zero observations
mean absence. GSC and gene annotations remain post hoc for CFBS and must not
select scan windows.

## 15. Validation Rules

VDB validators should implement at least the following checks before a
burden-aware projection surface is emitted.

```text
1. model_manifest_present
   opportunity_model_manifest exists and contains required fields.

2. region_coordinates_valid
   region coordinates are valid for the declared genome_build.

3. source_trace_present
   each opportunity claim traces to a source artifact, policy declaration, or
   explicit unavailable state.

4. observed_variants_not_denominator
   observed variants are not used as opportunity denominator.

5. base_count_nonnegative
   all base-count fields are non-negative integers.

6. base_count_ordering_valid
   callable_bases <= assayed_bases <= total_region_bases where known.

7. unknown_not_coerced
   unknown opportunity is preserved and not silently converted to zero.

8. wes_wgs_not_silently_merged
   WES and WGS denominator models are distinct unless a harmonization policy is
   declared.

9. burden_ready_supported
   burden_ready is declared only when denominator support is adequate.

10. exploratory_labeled
    approximate denominator models are labeled exploratory_only where required.

11. variant_class_declared
    variant-class-specific opportunity is declared when variant-class partitions
    are used in burden surfaces.

12. validation_receipts_complete
    validation receipts summarize pass/warn/fail status for the opportunity
    model and downstream burden-readiness state.
```

## 16. Failure Modes

The following conditions should produce validation warnings or failures:

```text
opportunity model missing
opportunity model unversioned
opportunity basis unknown
observed variants used as denominator
burden-ready label without callable/opportunity denominator
WES absence treated as genome-wide absence
unknown opportunity coerced to zero
sample traceability missing
region genome_build missing
coordinate range invalid
negative base counts
callable_bases greater than assayed_bases
GSC or gene annotations used as opportunity substrate
```

Critical failures should prevent `burden_ready` status.

## 17. Emission Requirements

A TEP-VDB package that contains burden-aware projection surfaces should include
or reference:

```text
opportunity_model_manifest
opportunity_region_set
sample_region_opportunity_matrix
opportunity_source_index
opportunity_validation_receipts
```

If opportunity is unavailable, the package should still emit an explicit
`opportunity_unmodeled` manifest and validation receipt so downstream consumers
know that denominator-aware burden reasoning is not supported.

## 18. Future Extensions

Future versions may add:

```text
per-base callable interval storage
sample-specific coverage distributions
variant-class-specific callability masks
mappability / repeat / GC derived opportunity features
population-frequency-aware opportunity partitions
sex-chromosome and mitochondrial opportunity models
multi-assay harmonization policies
structural-variant opportunity models
confidence intervals around approximate denominators
```

These extensions must preserve the core invariant that opportunity space is a
declared denominator substrate, not inferred from observed variant locations.

## 19. Summary

This specification establishes opportunity space as the denominator substrate for
VDB projection surfaces.

The minimum safe doctrine is:

```text
Preserve observed coordinate evidence as numerator substrate.
Declare opportunity space as denominator substrate.
Allow approximate or unmodeled opportunity only when explicit.
Prohibit burden-ready claims without denominator support.
Keep WES and WGS opportunity distinct unless harmonized by policy.
Require validation receipts before RDGP consumes burden-aware surfaces.
```

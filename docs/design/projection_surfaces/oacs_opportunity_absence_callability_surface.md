# OACS: Opportunity / Absence / Callability Surface

> Status: SAGE-VDB projection-surface design draft.
>
> Intended path:
>
> `docs/design/projection_surfaces/oacs_opportunity_absence_callability_surface.md`
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
> TEP-VDB cross-cutting denominator and absence-safety surface.
>
> Primary consumer:
>
> RDGP, CFBS, MPLC, PGERS, KVPS, GIRS, EVRS, RFPS, PAPS, and future downstream reasoning systems.

---

## 1. Purpose

The Opportunity / Absence / Callability Surface, abbreviated **OACS**, defines the TEP-VDB projection surface that exposes whether evidence could have been observed in a declared sample, region, locus, feature, gene target, coordinate window, or projection target under a declared assay, callability, quality, filtering, and opportunity policy.

OACS exists because downstream reasoning systems must distinguish:

```text
observed evidence
absence with sufficient opportunity
absence without sufficient opportunity
not callable territory
not assayed territory
low-confidence territory
filtered territory
unknown opportunity
unmodeled opportunity
```

These states are not equivalent.

The central purpose of OACS is:

```text
Expose assay, callability, quality, filtering, and opportunity context for
sample-specific targets so RDGP and other projection surfaces can distinguish
observed evidence, interpretable absence, technical non-observability,
non-assay, low-confidence territory, filtered territory, and unknown
opportunity without converting technical missingness into biological absence.
```

OACS is the denominator and absence-safety surface for TEP-VDB.

It makes burden, recurrence, known-pathogenicity absence, genotype missingness, patient-gene rollups, and discovery-oriented surfaces safer by ensuring that zero-like states are not overinterpreted.

---

## 2. Relationship to TEP-VDB Architecture

TEP-VDB is a VDB-emitted, projection-rich reasoning transport package.

Within TEP-VDB, OACS belongs to the cross-cutting governance and safety surface family. It supports both major RDGP reasoning activities:

```text
known-today diagnostic support
unknown-tomorrow diagnostic discovery support
```

OACS supports nearly every other TEP-VDB projection surface:

```text
KVPS
    uses OACS to avoid treating no known pathogenicity hit as interpretable
    absence when the relevant observation or region was not callable or not
    assayed.

PGERS
    uses OACS to distinguish zero projected variants from absence that is
    interpretable under a declared gene/locus opportunity policy.

GIRS
    uses OACS to distinguish missing genotype, no-call, filtered territory,
    and technical non-observability from true absence.

CFBS
    uses OACS-compatible coordinate-window opportunity denominators.

MPLC
    uses OACS-compatible sample-locus opportunity denominators.

EVRS
    uses OACS to determine whether exact-variant non-recurrence is informative
    or simply unobservable.

RFPS
    uses OACS to determine whether regulatory and feature targets were
    observable enough for absence or burden claims.

PAPS
    uses OACS to prevent phenotype-prior contexts from being interpreted as
    unsupported merely because variant evidence was technically unavailable.

CUES
    exposes conflicts, ambiguity, and uncertainty involving opportunity state.

RMCS
    tracks whether OACS was emitted under current corpus and method policy.
```

OACS should be included in TEP-VDB v1 because all burden, recurrence, absence, and negative-evidence reasoning depends on declared opportunity context.

---

## 3. Relationship to Mathematical Formalism

Under the VDB mathematical formalism, OACS is the projection surface that materializes the opportunity object for downstream surfaces.

Let:

```text
C
    declared VDB corpus generation

A_C
    corpus-indexed Assertion Record set

T_C
    typed evidence topology derived from A_C

M_OACS
    opportunity membership operator assigning coordinate bases, intervals,
    regions, loci, features, windows, or other targets to opportunity states

Ω_OACS
    opportunity object

P_OACS
    opportunity projection policy, including assay scope, callability,
    filtering, quality, variant class, target definition, and absence-labeling
    rules
```

Then:

```text
S_OACS = F_OACS(T_C, M_OACS, Ω_OACS, P_OACS)
```

Where:

```text
Ω_OACS = (U_OACS, μ_OACS, q_OACS)
```

and:

```text
U_OACS
    eligible target universe, such as windows, loci, gene targets, features,
    regulatory targets, or variant neighborhoods

μ_OACS
    opportunity measure, such as callable bases, callable intervals,
    callable sample-target territory, or declared evaluable territory

q_OACS
    opportunity-state function assigning states such as callable,
    not_callable, not_assayed, low_confidence, filtered, unknown, or
    unmodeled
```

The required traceability invariant is:

```text
Every OACS opportunity state must trace to a declared assay scope,
callability source, quality/filter policy, or explicit unknown/unmodeled state.
```

Unknown opportunity may be valid only when it is explicit.

Unmodeled opportunity may be valid only when it disables absence interpretation.

---

## 4. Core Doctrine

OACS is governed by the following doctrine:

```text
OACS does not prove absence of disease evidence.

OACS exposes whether evidence could have been observed in a declared sample,
region, feature, gene, locus, window, or projection target under a declared
assay, callability, quality, filtering, and opportunity policy.
```

Therefore:

```text
zero observed variants
    ≠ biological absence

no known pathogenicity hit
    ≠ no pathogenic variant exists

no projected gene evidence
    ≠ gene excluded

missing genotype
    ≠ homozygous reference

not callable
    ≠ absent

not assayed
    ≠ absent

unknown opportunity
    ≠ negative evidence
```

OACS is intentionally conservative.

It does not make diagnostic conclusions, disease-exclusion claims, negative association claims, enrichment claims, or biological interpretations.

It provides the opportunity and absence-readiness context required for downstream systems to reason safely.

---

## 5. Scientific Question

OACS answers the following VDB-level question:

```text
For this sample and target, what territory was observable, not observable,
not assayed, low confidence, filtered, unknown, or unmodeled under the declared
assay and opportunity policy, and is absence of observed evidence interpretable
for downstream reasoning?
```

OACS does not answer:

```text
Is this gene ruled out?
Is this locus disease-free?
Is this patient negative for pathogenic variants?
Is this burden statistically significant?
Is this region biologically depleted?
Is this target clinically cleared?
```

Those questions belong downstream and require additional reasoning, model context, and interpretation.

---

## 6. What OACS Is

OACS is:

```text
a denominator surface
an absence-safety surface
a callability surface
a sample-target opportunity surface
a projection-policy-aware observability surface
a cross-surface support substrate
an RDGP safety substrate
```

OACS is the TEP-VDB surface that enables other surfaces to distinguish:

```text
observed evidence
interpretable non-observation
technical non-observation
unknown observability
unmodeled observability
```

OACS may expose observed-evidence presence for context, but it does not own biological evidence rollups.

OACS may expose zero counts, but it does not interpret zero counts biologically.

OACS may expose absence-readiness labels, but it does not conclude absence of disease evidence.

---

## 7. What OACS Is Not

OACS is not:

```text
a burden test
an enrichment test
a depletion test
a pathogenicity surface
a genotype-readiness surface
a patient-gene evidence rollup
a disease-exclusion model
a diagnostic negative report
a clinical clearance surface
a replacement for CFBS or MPLC denominators
a replacement for source callability evidence
a downstream reasoning result
```

OACS defines shared opportunity context and absence-readiness. CFBS and MPLC
may derive method-specific denominators from OACS-compatible opportunity
policies, but their method-specific denominator choices remain declared in
their own projection policies.

OACS does not perform CFBS.

OACS does not perform MPLC.

OACS does not perform RDGP reasoning.

OACS does not determine that a gene, locus, or region lacks disease relevance.

OACS only declares opportunity and absence-readiness context under governed policies.

---

## 8. Core Surface Unit

The primary OACS unit should be:

```text
sample_id × opportunity_target_id × opportunity_policy_id × variant_class
```

This is intentionally more specific than:

```text
sample_id × gene_symbol
```

or:

```text
sample_id × region_name
```

because opportunity depends on:

```text
assay type
sample/run context
target definition
variant class
callability model
quality/filter policy
projection policy
reference build
coordinate representation
```

The same biological label may correspond to different opportunity targets.

Example:

```text
POLG gene body
POLG ±10 kb locus window
POLG splice-proximal window
POLG promoter interval
POLG regulatory-linked enhancer set
POLG MPLC locus window
POLG PGERS projected gene target
```

These are not interchangeable.

OACS must preserve the target definition and policy that generated each opportunity state.

---

## 9. Opportunity Targets

OACS should support opportunity targets such as:

```text
single coordinate
coordinate interval
fixed genomic window
candidate interval
gene locus
gene body window
splice-proximal window
promoter interval
enhancer interval
regulatory feature
linked regulatory target
MPLC target locus
MPLC background locus
CFBS scan window
PGERS projected gene target
RFPS feature target
KVPS variant neighborhood
EVRS exact variant identity neighborhood
```

The target type must remain explicit.

A gene body window must not silently become a regulatory feature target.

A regulatory feature target must not silently become a direct gene annotation.

A coordinate window must not silently become a disease locus.

---

## 10. Opportunity State Vocabulary

OACS opportunity states are surface-facing absence-readiness states derived
from lower-level opportunity states such as callable, not_callable,
not_assayed, low_confidence, filtered, unknown, and opportunity_unmodeled.

OACS should distinguish at least the following states:

```text
observed_evidence_present
absence_evaluable_with_opportunity
absence_not_evaluable_not_callable
absence_not_evaluable_not_assayed
absence_not_evaluable_low_confidence
absence_not_evaluable_filtered
absence_not_evaluable_unknown_opportunity
absence_not_evaluable_unmodeled_opportunity
mixed_opportunity
opportunity_not_evaluated
```

`observed_evidence_present` is a contextual observability state, not an OACS-owned biological evidence rollup.

The key positive absence-readiness state is:

```text
absence_evaluable_with_opportunity
```

This state does not mean absence of disease evidence.

It means only:

```text
under the declared assay and opportunity policy, non-observation of qualifying
evidence in this target may be treated as interpretable by downstream reasoning.
```

All other absence-like states must preserve why absence is not safely interpretable.

---

## 11. Negative-Evidence Readiness

OACS should emit a field such as:

```text
negative_evidence_readiness
```

Recommended values:

```text
negative_evidence_allowed
negative_evidence_limited
negative_evidence_not_allowed
negative_evidence_unknown
negative_evidence_not_requested
```

OACS should also emit:

```text
absence_interpretation_label
```

Recommended values:

```text
absence_interpretable_under_policy
absence_not_interpretable_not_callable
absence_not_interpretable_not_assayed
absence_not_interpretable_low_confidence
absence_not_interpretable_filtered
absence_not_interpretable_unknown_opportunity
absence_not_interpretable_unmodeled_opportunity
absence_interpretation_not_requested
```

Downstream systems may use these labels to decide whether a zero, missing hit, or non-observation can contribute to negative evidence.

OACS itself does not decide what downstream weight such states should receive.

---

## 12. Variant-Class Awareness

Opportunity is variant-class dependent.

OACS should therefore include:

```text
variant_class
opportunity_variant_class
callability_model
filter_model
assay_scope_policy_id
```

Representative variant/opportunity classes include:

```text
SNV
small_indel
MNV
CNV
SV
STR
repeat_expansion
mitochondrial_variant
splice_region_variant
regulatory_variant
unknown_variant_class
```

VDB v1 may not model all variant classes.

That is acceptable only if unsupported classes are explicit:

```text
cnv_opportunity_not_modeled
sv_opportunity_not_modeled
str_opportunity_not_modeled
repeat_expansion_opportunity_not_modeled
mitochondrial_opportunity_not_modeled
```

Unsupported opportunity classes must not be silently treated as callable or absent.

---

## 13. WES and WGS Opportunity Boundaries

OACS must preserve assay-type-specific opportunity boundaries.

For WES:

```text
opportunity is capture/callability constrained
absence outside captured or callable territory is usually not interpretable
noncoding evidence may exist but does not imply genomewide noncoding opportunity
```

For WGS:

```text
opportunity is broader than WES but still constrained by coverage, mappability,
repeats, GC bias, alignment ambiguity, filters, sample quality, and variant
class
```

Therefore, OACS should require:

```text
assay_type
assay_scope_policy_id
callability_policy_id
opportunity_model_version
reference_build
```

OACS must not merge WES and WGS denominator models unless an explicit harmonization policy declares and justifies the equivalence.

---

## 14. Opportunity Evidence Grades

OACS should not require perfect base-level callability to be useful.

OACS may support graded opportunity evidence states:

```text
measured_base_level_opportunity
measured_interval_level_opportunity
estimated_opportunity
source_declared_opportunity
coarse_assay_scope_opportunity
opportunity_unmodeled
unknown_opportunity
```

When opportunity is unknown or unmodeled, OACS should still emit a row if the target is relevant, but it must disable absence interpretation unless policy explicitly allows a limited statement.

Example:

```text
opportunity_evidence_grade: opportunity_unmodeled
negative_evidence_readiness: negative_evidence_not_allowed
absence_interpretation_label: absence_not_interpretable_unmodeled_opportunity
```

This is safer than omitting the target or coercing unknown opportunity to zero.

---

## 15. Source Substrates

OACS may consume source substrates including:

```text
sample identity
run identity
assay type
reference build
coordinate target definitions
projection target definitions
capture interval records when available
callability records when available
coverage summaries when available
quality/filter records when available
variant observation records when needed for observed-context labels
CFBS window definitions
MPLC locus definitions
PGERS projected gene targets
RFPS feature targets
KVPS variant neighborhoods
EVRS exact variant neighborhoods
```

OACS should not require all substrates to exist in v1.

When a required substrate is unavailable, the emitted opportunity state should preserve the limitation explicitly.

---

## 16. Projection Policy

An OACS projection policy should declare:

```text
opportunity_policy_id
opportunity_policy_version
assay_scope_policy_id
callability_policy_id
quality_filter_policy_id
variant_class_policy_id
target_definition_policy_id
reference_build
coordinate_system
required source substrates
opportunity evidence grade rules
absence interpretation rules
negative evidence readiness rules
unknown/unmodeled behavior
lossiness policy
validation policy
```

The projection policy must define how OACS converts source opportunity evidence into target-level opportunity states.

It must also declare when opportunity is not modeled.

---

## 17. Surface Outputs

OACS should emit two primary output families.

### 17.1 Opportunity Target Table

The opportunity target table should emit one row per:

```text
sample_id × opportunity_target_id × opportunity_policy_id × variant_class
```

Representative fields:

```text
oacs_surface_id
corpus_generation_id
surface_generation_id
sample_id
run_id
assay_type
reference_build
opportunity_target_id
target_type
target_label
target_namespace
target_coordinates_or_reference
variant_class
opportunity_policy_id
callability_policy_id
assay_scope_policy_id
quality_filter_policy_id
opportunity_evidence_grade
callable_bases
not_callable_bases
not_assayed_bases
low_confidence_bases
filtered_bases
unknown_opportunity_bases
total_target_bases
callable_fraction
opportunity_state
negative_evidence_readiness
absence_interpretation_label
observed_qualifying_evidence_count
observed_evidence_refs
limitations
traceability_refs
anti_overclaim_label
rmcs_surface_ref
```

### 17.2 Opportunity Summary Table

The opportunity summary table should emit one row per higher-level target such as:

```text
sample × gene target
sample × locus target
sample × CFBS scan-window group
sample × MPLC target/background group
sample × RFPS feature group
```

Representative fields:

```text
oacs_summary_id
corpus_generation_id
surface_generation_id
sample_id
summary_target_id
summary_target_type
summary_target_label
variant_class
opportunity_policy_id
total_callable_bases
total_not_callable_bases
total_not_assayed_bases
total_low_confidence_bases
total_filtered_bases
total_unknown_opportunity_bases
mean_callable_fraction
minimum_callable_fraction
maximum_callable_fraction
opportunity_completeness_label
negative_evidence_readiness
absence_interpretation_label
target_row_count
surface_refs
limitations
traceability_refs
anti_overclaim_label
```

The target table supports auditability.

The summary table supports RDGP consumption.

Both must remain reconstructable from declared source substrates and policies.

---

## 18. Observed-Evidence Context

OACS may expose observed-evidence presence to distinguish:

```text
observed_evidence_present
absence_evaluable_with_opportunity
absence_not_evaluable
```

However, OACS does not own biological evidence rollup.

Observed evidence counts in OACS should be contextual and traceable.

Primary biological evidence states remain owned by surfaces such as:

```text
KVPS
PGERS
GIRS
CFBS
MPLC
EVRS
RFPS
PAPS
```

OACS may reference their evidence objects where needed, but it must not replace them.

---

## 19. Relationship to KVPS

KVPS exposes known pathogenicity evidence attached to sample-specific observed variants.

OACS supports KVPS by clarifying whether no known pathogenicity hit or non-observation can be interpreted.

For example:

```text
KVPS label:
    no_known_pathogenicity_assertion_attached

OACS label:
    absence_not_interpretable_unknown_opportunity
```

Together, these mean:

```text
No known pathogenicity assertion was attached, but this should not be treated
as interpretable absence because opportunity is unknown.
```

KVPS should not make negative known-pathogenicity claims without OACS-compatible absence context.

---

## 20. Relationship to PGERS

PGERS rolls patient-specific evidence onto governed gene, locus, or gene-adjacent targets.

OACS supports PGERS by determining whether zero projected variants can be interpreted.

For example:

```text
PGERS:
    projected_variant_count = 0

OACS:
    absence_evaluable_with_opportunity
```

This differs from:

```text
PGERS:
    projected_variant_count = 0

OACS:
    absence_not_evaluable_not_assayed
```

PGERS must not treat an empty patient-gene row as negative evidence without OACS support.

---

## 21. Relationship to GIRS

GIRS exposes genotype observation structure and inheritance-readiness context.

OACS supports GIRS by clarifying whether missing genotype, no-call states, or absent observations reflect technical non-observability.

GIRS must not convert:

```text
missing genotype
no-call
filtered call
not emitted genotype
```

into absence without OACS-compatible opportunity context.

OACS should also preserve a boundary between technical opportunity and
genotype-to-variant relationship readiness.

An unresolved, ambiguous, missing, or not-evaluated genotype-to-variant
relationship is not automatically an opportunity state.

For example:

```text
genotype_variant_relationship_unresolved
multiallelic_relationship_ambiguous
called_allele_index_out_of_range
missing_variant_identity
```

should primarily be surfaced through GIRS and CUES, with RMCS tracking any
policy or builder currency dependencies.

OACS may indicate whether the relevant region, target, or variant class was
observable, but OACS must not convert relationship-brokerage failure into
biological absence or technical non-opportunity unless the declared opportunity
policy supports that interpretation.

---

## 22. Relationship to CFBS

CFBS performs coordinate-first burden scanning.

OACS provides the denominator substrate for CFBS scan windows.

For a CFBS window `w`, the CFBS opportunity term should be OACS-compatible:

```text
C[w] = callable opportunity for window w under declared OACS/CFBS policy
```

CFBS should not treat raw window length as opportunity unless the policy explicitly declares that raw length is being used as a coarse or fallback approximation.

CFBS candidate intervals should retain OACS references so RDGP can inspect whether observed burden reflects biological signal or technical opportunity structure.

---

## 23. Relationship to MPLC

MPLC compares GSC-prior target loci against matched non-prior background loci.

OACS provides the sample-locus opportunity substrate for MPLC.

For MPLC target or background locus `g` in sample `s`, the MPLC opportunity term should be OACS-compatible:

```text
C[s,g] = callable opportunity for sample s and locus g under declared
OACS/MPLC policy
```

MPLC must not compare target and background loci without opportunity states sufficient to support the declared contrast.

Locus size, callability, assay scope, variant class, and quality/filter behavior must be governed.

---

## 24. Relationship to EVRS

EVRS exposes exact variant or allele recurrence across samples.

OACS supports EVRS by distinguishing:

```text
variant not recurrent because not present
variant not recurrent because not observable
variant recurrence unknown because opportunity is missing or unmodeled
```

Exact non-recurrence should not be interpreted without opportunity and assay context.

---

## 25. Relationship to RFPS

RFPS projects coordinate evidence onto regulatory, feature, splice, promoter, enhancer, conserved, or other governed noncoding/feature targets.

OACS supports RFPS by exposing whether those feature targets were observable.

This is essential because noncoding feature absence is often assay- and callability-dependent.

OACS should preserve feature-level opportunity states when RFPS emits feature projection memberships.

---

## 26. Relationship to PAPS

PAPS exposes phenotype alignment and phenotype-scoped prior context.

OACS supports PAPS by preventing phenotype-prior absence or patient-gene absence from being overread when opportunity was limited.

For example, a phenotype-prior gene with no observed variant evidence may still be relevant if the locus was poorly covered, not assayed, or opportunity-unmodeled.

---

## 27. Relationship to CUES

CUES exposes conflict, uncertainty, ambiguity, and evidence-state warnings.

OACS feeds CUES when opportunity states are conflicting or uncertain.

Examples:

```text
callability source conflict
assay-scope ambiguity
mixed opportunity
unknown opportunity
variant-class opportunity unavailable
WES/WGS denominator mismatch
callable fraction below policy threshold
```

CUES may surface OACS-derived warnings for RDGP and human reviewers.

---

## 28. Relationship to RMCS

RMCS tracks reasoning, method, corpus, and surface currency.

OACS outputs may become stale when:

```text
new callability evidence arrives
assay-scope policy changes
quality/filter policy changes
reference build changes
projection target definitions change
variant-class opportunity models change
source corpus changes
```

RMCS should track OACS surface generation and freshness so downstream surfaces know whether their denominator context remains current.

---

## 29. v1 Minimum Viable Surface

OACS v1 should be practical but explicit.

Minimum v1 inputs:

```text
sample identity
run identity
assay type
reference build
projection target definitions
coordinate intervals where available
quality/filter context where available
callability or coverage-like context where available
explicit unknown/unmodeled states where unavailable
```

Minimum v1 outputs:

```text
opportunity target table
opportunity summary table
```

Minimum v1 required fields:

```text
oacs_surface_id
corpus_generation_id
surface_generation_id
sample_id
run_id
assay_type
reference_build
opportunity_target_id
target_type
target_coordinates_or_reference
variant_class
opportunity_policy_id
opportunity_evidence_grade
opportunity_state
callable_bases when available
callable_fraction when available
not_callable / not_assayed / low_confidence / filtered / unknown states
negative_evidence_readiness
absence_interpretation_label
traceability_refs
anti_overclaim_label
```

If measured base-level callability is unavailable, v1 may emit:

```text
opportunity_evidence_grade: opportunity_unmodeled
opportunity_state: absence_not_evaluable_unmodeled_opportunity
negative_evidence_readiness: negative_evidence_not_allowed
```

This is valid and preferable to silent absence.

---

## 30. Validation Requirements

OACS validation should confirm:

```text
all OACS rows declare sample_id and run_id
all OACS rows declare assay_type
all OACS rows declare opportunity_target_id
all OACS rows declare target_type
all OACS rows declare variant_class
all OACS rows declare opportunity_policy_id
all OACS rows declare opportunity_state
all absence-like rows declare negative_evidence_readiness
unknown opportunity is not coerced to zero
unmodeled opportunity is explicit
not_assayed is not collapsed into absent
not_callable is not collapsed into absent
low_confidence is not collapsed into absent
filtered territory is not collapsed into absent
WES/WGS denominator policies are not silently merged
variant-class opportunity is not reused across incompatible classes
callable_bases and total_target_bases are internally consistent when present
callable_fraction is internally consistent when present
summary rows trace to target-level rows
traceability_refs are present or explicit unavailable-state refs exist
anti_overclaim_label is present
```

Validation should also confirm that downstream surfaces referencing OACS use matching opportunity policies or explicitly declare policy mismatch.

---

## 31. Anti-Overclaim Labels

Every OACS row should carry an anti-overclaim label.

Recommended labels include:

```text
oacs_opportunity_context_only
oacs_absence_readiness_context_only
oacs_not_negative_diagnosis
oacs_not_gene_exclusion
oacs_not_pathogenicity_absence
oacs_not_burden_result
oacs_not_statistical_result
oacs_unmodeled_opportunity_no_absence_claim
oacs_unknown_opportunity_no_absence_claim
```

These labels protect OACS from being interpreted as a negative diagnostic or biological-exclusion surface.

---

## 32. Anti-Collapse Rules

OACS prohibits the following patterns:

```text
zero observed variants treated as biological absence without opportunity

missing callability treated as callable

not_assayed treated as absent

not_callable treated as absent

filtered treated as absent

low-confidence territory treated as absent

unknown opportunity coerced to zero

unmodeled opportunity hidden from downstream consumers

WES and WGS denominators merged without policy

gene-level absence inferred from partial gene coverage

variant-class opportunity reused across incompatible variant classes

off-target WES evidence treated as genomewide WES opportunity

raw target length treated as callable bases without declared fallback policy

observed-evidence count treated as OACS-owned biological rollup

OACS opportunity state treated as diagnostic conclusion

OACS summary replacing target-level traceability
```

Any implementation that performs one of these actions violates OACS design doctrine.

---

## 33. Non-Goals

OACS does not define:

```text
complete callability file format
complete base-level coverage schema
complete CFBS implementation
complete MPLC implementation
complete PGERS implementation
complete RDGP negative-evidence model
clinical disease exclusion logic
gene-level diagnostic absence logic
burden significance testing
pathogenicity interpretation
ACMG interpretation
```

OACS defines the opportunity and absence-readiness surface that downstream systems may consume.

---

## 34. Future Extensions

Future OACS versions may support:

```text
base-level callable masks
sample-specific callable interval catalogs
variant-class-specific opportunity models
CNV/SV/STR opportunity models
mitochondrial opportunity models
mappability-aware opportunity models
GC-bias-aware opportunity models
repeat-aware opportunity models
sex-chromosome/ploidy-aware opportunity models
regulatory-feature-specific opportunity models
cross-assay opportunity harmonization
cohort-level opportunity summaries
release-level opportunity snapshots
large-scale WES/WGS denominator comparisons
```

These extensions should preserve the same anti-collapse doctrine.

More detailed opportunity models may refine absence interpretation, but they must not erase earlier opportunity uncertainty.

---

## 35. Summary

OACS is the TEP-VDB projection surface that exposes opportunity, callability, assay scope, quality, filtering, and absence-readiness context for sample-specific projection targets.

It exists because downstream reasoning must distinguish:

```text
observed evidence
interpretable non-observation
technical non-observability
non-assay
low-confidence territory
filtered territory
unknown opportunity
unmodeled opportunity
```

OACS is not a burden test, diagnostic negative result, or gene-exclusion surface.

It is the denominator and absence-safety substrate for TEP-VDB.

The governing boundary is:

```text
OACS exposes opportunity and absence-readiness.

Other VDB surfaces consume OACS to remain denominator-aware.

RDGP evaluates evidence using OACS context.

Scientists and clinicians interpret evaluated evidence.
```

In this way, OACS prevents TEP-VDB from converting technical missingness into biological absence and protects both known-today diagnostic support and unknown-tomorrow discovery reasoning.

# RMCS — Reasoning / Method Currency Surface

**Status:** SAGE-VDB projection-surface design draft  
**Intended path:** `docs/design/projection_surfaces/rmcs_reasoning_method_currency_surface.md`  
**Surface family:** TEP-VDB cross-cutting governance / currency / comparability surface  
**TEP-VDB role:** Capstone dependency, currency, validation, refresh, and comparability surface for all projection surfaces  
**Primary downstream consumer:** RDGP and future downstream reasoning systems  
**Related architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## 1. Purpose

The Reasoning / Method Currency Surface (RMCS) is the TEP-VDB projection surface that exposes dependency, currency, validation, refresh, and comparability state for VDB surfaces, source releases, projection policies, corpus generations, and downstream reasoning outputs.

RMCS exists because evidence surfaces are not timeless. A projection surface is generated from a particular corpus, assertion index, topology build, geometry build, namespace policy, opportunity policy, projection policy, source release set, validation state, and downstream reasoning method. When any of those dependencies change, prior surfaces and reasoning outputs may remain useful, but they are no longer automatically current or comparable.

The central doctrine is:

```text
RMCS does not decide whether evidence is true, false, stronger, weaker, or
clinically actionable.

RMCS exposes corpus, method, policy, surface, source-release, and reasoning
currency states so RDGP and downstream consumers can distinguish current,
stale, superseded, incomparable, unvalidated, or refresh-required reasoning
substrates.
```

RMCS is therefore a governance surface, not a biological interpretation surface.

---

## 2. Relationship to TEP-VDB Architecture

TEP-VDB is a projection-rich, provenance-preserving reasoning transport package emitted by VDB for RDGP. Within that package, RMCS is the surface responsible for declaring whether the package, surfaces, policies, dependencies, and returned reasoning outputs remain current under their declared dependency set.

Most TEP-VDB projection surfaces expose biological, statistical, epistemic, or contextual evidence:

```text
KVPS: known pathogenicity evidence
PGERS: patient-gene/locus rollup
GIRS: genotype-readiness context
OACS: opportunity and absence-readiness
CUES: conflict and uncertainty state
EVRS: exact variant recurrence
RFPS: regulatory/feature projection
PAPS: phenotype-prior alignment
CFBS: coordinate-first burden scan
MPLC: matched prior-locus contrast
```

RMCS answers a different architectural question:

```text
Is this evidence surface, projection policy, corpus generation, external source,
or downstream reasoning result still current relative to the dependency set
under which it was generated?
```

RMCS is the capstone governance layer for the projection-surface family. It allows VDB and RDGP to reason over evidence across time without silently treating stale, superseded, unvalidated, or incomparable artifacts as current.

---

## 3. Relationship to Mathematical Formalism

Under the VDB projection formalism:

```text
A_C
    → T_C
    → (M_θ, Ω_θ)
    → G_θ
    → S_θ
    → TEP-VDB
    → RDGP
```

RMCS is the specialization:

```text
θ_RMCS:
    source objects =
        TEP-VDB package manifests,
        corpus generation manifests,
        assertion record index versions,
        topology and geometry build receipts,
        projection policy receipts,
        namespace/opportunity/filter/counting policy receipts,
        surface validation receipts,
        external source version manifests,
        RDGP reasoning method manifests,
        prior reasoning outputs

    target objects =
        artifact currency states,
        dependency memberships,
        refresh states,
        validation and comparability summaries

    membership =
        artifact belongs to a currency state if its declared dependency set
        satisfies or fails declared currency, validation, refresh, and
        comparability policies

    opportunity =
        not genomic opportunity; dependency availability and evaluation
        availability may be represented as explicit unavailable or
        not-evaluated states

    geometry =
        dependency graph summaries,
        currency-state stratification,
        refresh-readiness summaries,
        comparability classes

    surface =
        reasoning and method currency substrate for RDGP and VDB governance
```

Compactly:

```text
S_RMCS = F_RMCS(T_C, D_RMCS, P_RMCS)
```

Where:

```text
D_RMCS = dependency relation among packages, surfaces, policies, sources,
         validation receipts, and reasoning outputs

P_RMCS = currency, refresh, validation, and comparability policy
```

Equivalently, to remain aligned with the membership notation used by the other projection-surface designs:

```text
M_RMCS = membership operator from artifacts to dependency/currency states
```

Every RMCS currency, refresh, validation, or comparability label must trace to the dependency manifest, policy receipt, validation receipt, source release, surface generation, reasoning method manifest, or explicit unavailable/not-evaluated state that produced the label.

---

## 4. Governance Question

RMCS answers:

```text
For this TEP-VDB package, surface, policy, dependency, or downstream reasoning
output, what dependency set was used, is that dependency set still current, did
validation pass, is refresh required, and can the artifact be compared to other
artifacts under declared policies?
```

RMCS does not answer:

```text
Is this gene causal?
Is this variant pathogenic?
Is this result clinically actionable?
Is this newer method better?
Did evidence strength increase?
```

Those are reasoning, validation, or interpretation questions outside RMCS authority unless preserved as explicit external assertions.

---

## 5. What RMCS Is

RMCS is:

```text
a dependency-state surface

a method/version currency surface

a refresh-readiness surface

a validation-state summary surface

a comparability governance surface

a package and surface provenance index

a downstream reasoning-output currency tracker
```

RMCS exposes the dependency and currency context required for RDGP to decide whether prior surfaces or reasoning outputs can be consumed, compared, refreshed, or re-evaluated.

---

## 6. What RMCS Is Not

RMCS is not:

```text
a biological evidence surface in the ordinary sense

a pathogenicity classifier

a gene prioritization model

a surface-quality score

a truth-maintenance system

a claim that newer evidence is better evidence

a claim that stale evidence is false evidence

a replacement for validation receipts

a replacement for CUES

a replacement for RDGP re-reasoning
```

RMCS labels currency. It does not adjudicate biological truth.

Validation state and currency state may affect downstream consumption, but
they are not scalar surface-quality scores.

---

## 7. Freshness, Currency, Validity, and Comparability

RMCS must distinguish four related but different states.

### 7.1 Freshness

Freshness describes when an artifact was generated, evaluated, or updated.

```text
freshness:
    generated_at
    evaluated_at
    source_release_date
    package_generation_time
```

An artifact may be fresh but invalid:

```text
generated today, but failed validation
```

### 7.2 Currency

Currency describes whether an artifact is current relative to its declared dependencies.

```text
currency:
    current relative to dependency set
    stale relative to dependency set
    superseded by newer artifact
    currency unknown
```

An artifact may be valid but stale:

```text
validated last month, but generated before a newer GSC prior package
```

### 7.3 Validity

Validity describes whether an artifact passed validation under its declared policy.

```text
validity:
    validation passed
    validation passed with warnings
    validation failed
    validation not evaluated
```

Validity is policy-relative. It is not truth.

### 7.4 Comparability

Comparability describes whether two artifacts can be compared under compatible corpus, policy, source-version, and method assumptions.

```text
comparability:
    comparable under same dependency set
    comparable with declared limitations
    not comparable because policy changed
    not comparable because corpus changed
    not comparable because method changed
    comparability unknown
```

A surface can be current but not comparable to another surface if the two were generated under incompatible policies.

---

## 8. Core RMCS Unit

The primary RMCS unit is:

```text
artifact_id × dependency_set_id × currency_policy_id
```

An `artifact_id` may refer to:

```text
TEP-VDB package
source corpus generation
assertion record index
topology build
geometry build
projection surface
projection surface cell
projection policy
namespace brokerage policy
opportunity policy
filter policy
counting policy
null-model policy
external source release
feature catalog
GSC prior package
known pathogenicity assertion source
RDGP reasoning output
RDGP method version
```

The dependency set is a governed relation:

```text
artifact
    depends_on →
        corpus generation
        assertion index
        topology build
        geometry build
        projection policy
        namespace policy
        opportunity policy
        external source release
        validation receipt
        downstream reasoning method
```

RMCS is therefore naturally a projection over a dependency graph.

---

## 8A. Dependency Set Identity and Comparability Scope

RMCS should track both individual dependencies and whole dependency sets.

The dependency set identity should include:

```text
dependency_set_id
dependency_set_fingerprint
dependency_set_role
dependency_set_generation_id
dependency_set_policy_id
```

Recommended dependency_set_role values include:

```text
surface_generation_dependencies
surface_validation_dependencies
surface_comparability_dependencies
surface_refresh_dependencies
reasoning_output_dependencies
package_generation_dependencies
```

RMCS should also support:

```text
comparability_scope_id
comparability_policy_id
```

because two artifacts may share some dependencies while still being
incomparable under a specific comparison policy.

For example:

```text
same source corpus
different CFBS window policy
    → not comparable for CFBS burden rank

same variant identity
different EVRS deduplication policy
    → not comparable for recurrence count

same RFPS feature catalog
different nearest-gene fallback policy
    → comparable only with declared limitations
```

A dependency fingerprint alone is not sufficient. RMCS must preserve which
dependencies matter for validity, refresh, and comparability under declared
policy.

---

## 9. Source Substrates

RMCS may consume the following source substrates:

```text
TEP-VDB package manifest
source corpus generation manifest
registration unit index
assertion record index
topology build receipt
geometry build receipt
projection surface manifest
projection policy registry
namespace brokerage policy receipts
opportunity policy receipts
filter/counting/null-model policy receipts
surface validation receipts
surface traceability receipts
source release manifests
known-variant assertion source versions
GSC TEP and prior-package versions
feature catalog versions
phenotype mapping source versions
RDGP reasoning method manifests
RDGP output manifests
prior RDGP reasoning assertions re-ingested into VDB
target identity bridge policy receipts
feature catalog coverage policy receipts
feature class support policy receipts
feature-to-target linkage policy receipts
nearest-gene fallback policy receipts
genotype FORMAT schema/parser receipts
recurrence scope and recurrence unit policy receipts
deduplication and independence policy receipts
scan-space and window policy receipts
candidate-interval assembly policy receipts
background-pool and background-matching policy receipts
matching diagnostics receipts
post hoc annotation policy receipts
prior evaluation universe receipts
daughter-surface dependency manifests
surface comparability manifests
surface-specific anti-overclaim policy receipts
```

After all TEP-VDB projection surfaces are considered, RMCS should treat
surface-specific policies as first-class dependencies. Policies such as
feature-to-target linkage, recurrence-unit selection, background matching,
window definition, prior-scope selection, genotype FORMAT parsing, target
identity bridging, and daughter-surface dependency requirements can materially
change whether a surface is current, valid, refresh-required, or comparable.

RMCS does not need to inspect biological content to determine most currency states. It needs dependency identity, version, fingerprint, policy, validation, and update context.

---

## 10. Currency State Vocabulary

RMCS should emit deterministic governance labels rather than continuous evidence scores.

Recommended `currency_state` values:

```text
current
current_with_note
stale
stale_source_release
stale_corpus_generation
stale_assertion_index
stale_topology_build
stale_geometry_build
stale_projection_policy
stale_namespace_policy
stale_opportunity_policy
stale_filter_policy
stale_counting_policy
stale_null_model_policy
stale_feature_catalog
stale_prior_source
stale_known_assertion_source
stale_reasoning_method
superseded
withdrawn
unvalidated
validation_failed
not_comparable
currency_unknown
currency_not_evaluated
stale_target_identity_bridge_policy
stale_genotype_format_schema
stale_recurrence_scope_policy
stale_recurrence_unit_policy
stale_deduplication_policy
stale_feature_catalog_coverage_policy
stale_feature_linkage_policy
stale_background_matching_policy
stale_scan_space_policy
stale_window_policy
stale_candidate_interval_assembly_policy
stale_posthoc_annotation_policy
stale_prior_evaluation_universe
stale_daughter_surface_dependency_policy
stale_surface_validation_profile
```

The generic state `stale` may be used only as a compact summary when the
specific stale dependency class is unavailable, mixed, or intentionally
summarized at package level.

When the changed dependency is known, RMCS should prefer the most specific
available state, such as:

```text
stale_projection_policy
stale_opportunity_policy
stale_feature_catalog
stale_genotype_format_schema
stale_recurrence_unit_policy
stale_background_matching_policy
```

Surface-specific stale states should be emitted when the changed dependency is
known. Generic `stale_projection_policy` remains useful as a compact summary,
but RMCS should preserve the more specific stale dependency class whenever it
can be determined.

Recommended `refresh_readiness_label` values:

```text
refresh_not_required
refresh_recommended
refresh_required
refresh_blocked_missing_dependency
refresh_blocked_validation_failure
refresh_blocked_policy_incompatibility
refresh_not_evaluated
```

These labels describe governance state. They do not describe biological truth or evidence strength.

---

## 11. Comparability State Vocabulary

RMCS should make comparability explicit, especially for repeated VDB/RDGP runs.

Recommended `comparability_state` values:

```text
comparable_same_policy_and_method
comparable_same_policy_different_package_generation
comparable_with_declared_limitations
not_comparable_policy_changed
not_comparable_corpus_changed
not_comparable_assertion_index_changed
not_comparable_namespace_policy_changed
not_comparable_opportunity_policy_changed
not_comparable_projection_policy_changed
not_comparable_null_model_changed
not_comparable_method_changed
not_comparable_source_release_changed
not_comparable_validation_failed
comparability_unknown
comparability_not_evaluated
not_comparable_target_identity_bridge_policy_changed
not_comparable_genotype_format_schema_changed
not_comparable_recurrence_scope_changed
not_comparable_recurrence_unit_changed
not_comparable_deduplication_policy_changed
not_comparable_feature_catalog_changed
not_comparable_feature_linkage_policy_changed
not_comparable_background_matching_policy_changed
not_comparable_scan_space_policy_changed
not_comparable_window_policy_changed
not_comparable_candidate_interval_policy_changed
not_comparable_posthoc_annotation_policy_changed
not_comparable_prior_scope_policy_changed
not_comparable_prior_evaluation_universe_changed
not_comparable_random_seed_changed_under_policy
not_comparable_daughter_surface_dependency_changed
```

For exploratory surfaces such as CFBS and MPLC, random seed, number of null
draws, null model, matching policy, and window policy may be comparability
dependencies. RMCS should not assume that two exploratory surfaces are comparable
merely because they share the same source corpus.

This prevents invalid longitudinal interpretation such as:

```text
old RDGP score = 0.73
new RDGP score = 0.81
therefore evidence improved
```

Such a comparison is only meaningful if the corpus, surfaces, policies, source releases, and RDGP method versions are comparable under declared policy.

---

## 12. Validation State Vocabulary

RMCS should summarize validation state without replacing validation receipts.

Recommended `validation_state` values:

```text
validation_passed
validation_passed_with_warnings
validation_failed
validation_blocked
validation_not_required_under_policy
validation_not_evaluated
validation_unknown
```

Validation state should always reference the validation receipt that produced it.

---

## 13. Refresh Semantics

RMCS should not automatically invalidate older evidence. It should identify whether refresh or re-reasoning is required.

Safe RMCS statements:

```text
surface generated under superseded source release

surface generated under superseded projection policy

RDGP output generated against older TEP-VDB package

refresh recommended

refresh required before comparison
```

Unsafe RMCS statements:

```text
old evidence is false

new evidence is stronger

old RDGP output is clinically invalid

new method is better
```

Currency is not truth. Staleness is not falsity. Recency is not superiority.

---

## 14. Artifact Levels

RMCS should track currency at multiple levels.

### 14.1 Package-Level Currency

```text
Is this TEP-VDB package current as a whole?
```

### 14.2 Surface-Level Currency

```text
Is this specific projection surface current relative to its dependencies?
```

### 14.3 Cell/Object-Level Currency

```text
Is this specific surface cell, evidence row, projected target, or dependency
object current relative to its direct dependencies?
```

### 14.4 Reasoning-Output Currency

```text
Is this downstream RDGP result current relative to the TEP-VDB package,
RDGP method version, and newer available evidence?
```

Reasoning-output currency is especially important because RDGP outputs may re-enter VDB as new assertions. RMCS can mark whether those returned reasoning assertions are current relative to later VDB evidence generations without mutating the original reasoning output.

---

## 15. Source Update, Policy Update, and Method Update

Currency can change for different reasons. RMCS should preserve the update category.

### 15.1 Source Update

A source update occurs when an external or producer source changes:

```text
known pathogenicity assertion source updated
GSC prior package regenerated
feature catalog updated
phenotype mapping source changed
external allele frequency source updated
```

### 15.2 Policy Update

A policy update occurs when VDB construction policy changes:

```text
projection policy changed
namespace brokerage policy changed
deduplication policy changed
callability/opportunity policy changed
surface schema changed
validation policy changed
null model changed
```

### 15.3 Method Update

A method update occurs when downstream reasoning changes:

```text
RDGP reasoning method version changed
model configuration changed
scoring weights changed
explanation template changed
inheritance reasoning policy changed
```

RMCS should expose the category because each one implies a different downstream response. A source update may require evidence refresh. A policy update may require surface regeneration. A method update may require RDGP re-evaluation.

---

## 15A. Surface-Specific Dependency Families

RMCS should preserve a surface-specific dependency family for each TEP-VDB
projection surface.

### KVPS Dependencies

For KVPS, RMCS should track:

```text
known assertion source version
known assertion condition / disease-context source version
variant identity policy
variant match policy
identity brokerage policy
clinical significance label policy
known assertion grouping policy
KVPS projection policy
KVPS validation receipt
```

### GIRS Dependencies

For GIRS, RMCS should track:

```text
source genotype field policy
source FORMAT schema policy
genotype parser version
genotype normalization policy
quality / depth / phase / ploidy policy
multiallelic-context policy
multiallelic relationship policy
allele index mapping policy
genotype-to-variant relationship policy
genotype-to-variant relationship builder version
genotype relationship surface schema version
variant normalization policy where genotype relationships depend on it
identity registration policy where genotype relationships depend on it
genotype projection policy
GIRS projection policy
GIRS validation receipt
```

GIRS currency may change when genotype parsing, FORMAT interpretation,
multiallelic relationship policy, allele-index mapping, genotype-to-variant
relationship construction, variant normalization, identity registration, or
readiness labeling changes.

RMCS should not treat a GIRS surface as comparable across packages if the
underlying genotype relationship policy or allele-index mapping policy changed
without an explicit comparability policy.

### OACS Dependencies

For OACS, RMCS should track:

```text
assay scope policy
callability model
opportunity policy
target opportunity policy
variant-class opportunity policy
absence-readiness policy
reference interval / capture territory version
OACS validation receipt
```

### CUES Dependencies

For CUES, RMCS should track:

```text
CUES event vocabulary version
normalized uncertainty-state policy
reasoning-effect label policy
severity / consumption-status policy
event aggregation policy
CUES validation receipt
```

### PAPS Dependencies

For PAPS, RMCS should track:

```text
GSC TEP version
GSC prior package version
phenotype namespace mapping policy
phenotype-scope alignment policy
target identity bridge policy
prior evaluation universe policy
prior absence policy
prior strength label policy
PAPS projection policy
PAPS validation receipt
```

### PGERS Dependencies

For PGERS, RMCS should track:

```text
daughter surface dependency policy
projection route policy
route summary policy
target identity bridge policy
gene / locus target policy
rollup counting policy
evidence stratification policy
filtering policy
summarization policy
PGERS projection policy
PGERS validation receipt
```

### CFBS Dependencies

For CFBS, RMCS should track:

```text
scan-space policy
window policy
variant filter policy
variant-class partition policy
counting policy
recurrence-unit policy
opportunity model
null model
candidate-interval assembly policy
post hoc annotation policy
patient-dominance policy
random seed
number of null draws
CFBS projection policy
CFBS validation receipt
```

### MPLC Dependencies

For MPLC, RMCS should track:

```text
target locus policy
target prior-scope policy
PAPS prior reference policy
background pool policy
background matching policy
matching diagnostics policy
window policy
variant filter policy
variant-class partition policy
counting policy
recurrence-unit policy
opportunity model
null model
random seed
number of null draws
MPLC projection policy
MPLC validation receipt
```

### EVRS Dependencies

For EVRS, RMCS should track:

```text
recurrence scope policy
recurrence unit policy
identity policy
allele normalization policy
variant-class support policy
deduplication policy
independence policy
denominator readiness policy
genotype summary policy
frequency context policy
EVRS projection policy
EVRS validation receipt
```

### RFPS Dependencies

For RFPS, RMCS should track:

```text
feature catalog version
feature catalog coverage policy
feature class support policy
coordinate-to-feature policy
feature-to-target linkage policy
target identity bridge policy
nearest-gene fallback policy
feature context policy
tissue / cell-type / assay context source
reference build
RFPS projection policy
RFPS validation receipt
```

RMCS should not collapse these surface-specific dependencies into a generic
`projection_policy_id` alone. A generic projection policy reference is useful,
but it is not sufficient for refresh, validation, or comparability decisions.

---

## 16. Relationship to CUES

RMCS and CUES are closely related but distinct.

```text
RMCS owns currency state.

CUES indexes currency-related epistemic events.
```

Example:

```text
RMCS:
    paps_surface_id = stale_prior_source

CUES:
    event_class = staleness
    event_type = gsc_prior_stale
    reasoning_effect_label = triggers_refresh
```

CUES gives RDGP the epistemic warning state. RMCS gives the detailed dependency and currency provenance.

RMCS should emit or reference CUES events for:

```text
stale_source_release
stale_projection_policy
stale_reasoning_method
validation_failed
not_comparable
currency_unknown
refresh_required
```

But CUES should not replace the RMCS dependency manifest.

---

## 17. Relationship to KVPS

For KVPS, RMCS should track:

```text
known assertion source version
variant identity policy
clinical significance label mapping policy
pathogenicity assertion source release
variant normalization policy
KVPS projection policy version
KVPS validation receipt
```

A KVPS surface or row may become stale if a known-variant assertion source changes, a variant identity policy changes, or the KVPS projection policy is superseded.

RMCS should not say the old KVPS evidence is false. It should say the KVPS surface was generated under an older dependency set and may require refresh.

---

## 18. Relationship to PGERS

For PGERS, RMCS should track:

```text
dependent surface set
daughter surface dependency policy
daughter surface dependency status
projection route policy
route summary policy
target identity bridge policy
gene / locus target policy
rollup counting policy
evidence stratification policy
filtering policy
summarization policy
PGERS schema version
PGERS projection policy
PGERS validation receipt
```

PGERS is highly dependency-rich because it may summarize KVPS, GIRS, OACS, CUES,
EVRS, RFPS, PAPS, CFBS, MPLC, and RMCS context.

A PGERS surface may become stale or incomparable when any of the following
changes:

```text
a contributing daughter surface changes
a daughter-surface dependency status changes
a target identity bridge policy changes
a counting policy changes
a projection route policy changes
a summarization policy changes
a rollup mode changes
```

RMCS should therefore preserve both:

```text
PGERS direct dependency currency

contributing-surface currency summary

daughter-surface dependency summary
```

PGERS currency must not imply that all daughter surfaces are current unless
their dependency states support that conclusion.

---

## 19. Relationship to GIRS

For GIRS, RMCS should track:

```text
genotype field parser version
genotype normalization policy
quality threshold policy
phase/ploidy context policy
GIRS projection policy version
GIRS validation receipt
```

A GIRS surface may become stale if genotype parsing, normalization, quality-state labeling, or phase/ploidy policy changes.

RMCS should not convert method change into inheritance reinterpretation. It only marks currency and refresh state.

---

## 20. Relationship to OACS

For OACS, RMCS should track:

```text
callability model version
assay scope policy
capture kit/reference interval version
opportunity policy
variant-class opportunity policy
OACS validation receipt
```

OACS is denominator-critical. Any change to opportunity policy, callability inputs, assay scope, or target definitions can make prior absence interpretations stale or incomparable.

RMCS should make denominator comparability explicit before RDGP compares absence or burden across runs.

---

## 21. Relationship to EVRS

For EVRS, RMCS should track:

```text
variant identity policy
allele normalization policy
recurrence scope policy
recurrence unit policy
cohort / package membership
assay scope
sample identity policy
sample-patient linkage policy
deduplication policy
independence policy
denominator readiness policy
variant-class support policy
EVRS projection policy
EVRS validation receipt
```

EVRS can become stale or incomparable when:

```text
the recurrence scope changes

the recurrence unit changes

sample-level recurrence is replaced by patient-level recurrence

deduplication policy changes

biological-subject identity becomes available

identity or normalization policy changes

assay scope changes

denominator readiness policy changes

variant-class support policy changes
```

RMCS should distinguish:

```text
same allele, different recurrence scope

same scope, different recurrence unit

same recurrence unit, different deduplication policy

same policy, expanded corpus

same recurrence count, different denominator readiness
```

Those are different comparability states.

---

## 22. Relationship to RFPS

For RFPS, RMCS should track:

```text
feature catalog version
feature catalog coverage policy
feature class support policy
coordinate-to-feature projection policy
feature-to-target linkage source
target identity bridge policy
nearest-gene fallback policy
reference build
context / tissue / cell-type / assay catalog release
RFPS projection policy version
RFPS validation receipt
```

Regulatory and feature annotations are highly source-version and context
sensitive. RFPS currency should identify whether a feature projection was
generated under:

```text
a stale feature catalog

a changed feature catalog coverage policy

a changed feature-to-target linkage source

a changed reference build

a changed tissue or cell-type context

a changed nearest-gene fallback policy

a changed target-link policy

a changed target identity bridge policy
```

A feature projection can remain traceable while no longer being comparable to
another RFPS surface generated under different catalog, context, linkage, or
fallback policies.

---

## 23. Relationship to PAPS

For PAPS, RMCS should track:

```text
GSC TEP version
GSC prior package version
phenotype namespace mapping policy
phenotype-prior source version
prior scoring policy
PAPS alignment policy
PAPS validation receipt
```

PAPS may become stale if GSC priors are regenerated, phenotype mapping policy changes, or target identity bridges change.

RMCS should avoid saying the old prior was wrong. It should declare the old prior package, alignment policy, or phenotype namespace mapping as stale or superseded.

---

## 24. Relationship to CFBS and MPLC

For CFBS and MPLC, RMCS is especially important because statistical discovery
surfaces are sensitive to corpus, opportunity, null model, matching, scan/window
policy, prior-scope policy, recurrence unit, and randomization settings.

For CFBS, RMCS should track:

```text
scan-space policy
window policy
variant filter policy
variant-class partition policy
counting policy
recurrence-unit policy
opportunity model
OACS reference policy
null model
candidate-interval assembly policy
post hoc annotation policy
patient-dominance policy
random seed
number of null draws
surface validation receipt
```

For MPLC, RMCS should track:

```text
target-locus policy
target prior-scope policy
PAPS reference policy
background-pool policy
background-matching policy
matching diagnostics policy
window policy
variant filter policy
variant-class partition policy
counting policy
recurrence-unit policy
opportunity model
OACS reference policy
null model
GSC release
random seed
number of null draws
surface validation receipt
```

A CFBS or MPLC result generated under one corpus, opportunity model, window
policy, null model, matching policy, prior-scope policy, recurrence unit, random
seed, or post hoc annotation policy should not be compared directly to another
without explicit RMCS comparability state.

RMCS should distinguish:

```text
same source corpus, different window policy

same target priors, different background matching policy

same null model, different random seed

same random seed, different number of null draws

same candidate interval, different post hoc annotation policy

same burden statistic, different recurrence unit

same prior set, different phenotype-scope policy
```

---

## 25. Relationship to RDGP Outputs

RDGP outputs may re-enter VDB as new assertions. RMCS should track the currency of those reasoning outputs relative to the TEP-VDB package and RDGP method version that produced them.

Example:

```text
RDGP prioritized POLG under TEP-VDB package v1.
Later, VDB package v2 adds new genotype, PAPS, KVPS, or OACS evidence.
```

RMCS can emit:

```text
rdgp_result_current_against_package_v1

rdgp_result_stale_against_package_v2

refresh_required_for_rdgp_result
```

RMCS does not recompute RDGP. It only states that the prior reasoning output was generated against an older evidence substrate or method version.

---

## 26. Output 1 — Dependency Manifest Table

The dependency manifest table should contain one row per:

```text
artifact_id × dependency_id
```

Conceptual fields:

```text
artifact_id
artifact_type
artifact_version
artifact_generation_id
surface_family when applicable
surface_type when applicable
dependency_set_id
dependency_set_fingerprint
dependency_set_role
dependency_set_generation_id
dependency_set_policy_id
comparability_scope_id when applicable
comparability_policy_id when applicable

dependency_id
dependency_type
dependency_name
dependency_version
dependency_fingerprint
dependency_role
dependency_required_for_generation
dependency_required_for_validity
dependency_required_for_refresh
dependency_required_for_comparability
dependency_currency_state
currency_basis_type

source_release_date
source_evaluated_at
policy_receipt_id
validation_receipt_id
cues_event_refs when applicable
traceability_refs
```

This table is the audit backbone of RMCS.

---

## 27. Output 2 — Surface Currency Table

The surface currency table should contain one row per:

```text
surface_id × currency_policy_id
```

Conceptual fields:

```text
surface_id
surface_type
surface_family
surface_subtype when applicable
surface_version
surface_generation_id
source_corpus_id
source_corpus_generation_id

dependency_set_id
dependency_set_fingerprint
comparability_scope_id
comparability_policy_id

assertion_record_index_id
topology_build_id
geometry_build_id
projection_policy_id
namespace_policy_id
opportunity_policy_id
filter_policy_id
counting_policy_id
null_model_policy_id
surface_specific_policy_refs
external_source_versions
daughter_surface_dependency_summary when applicable

validation_receipt_id
validation_profile_id
generated_at
evaluated_at
currency_policy_id
currency_basis_type
surface_currency_state
validation_state
refresh_readiness_label
comparability_state
superseded_by_surface_id
limitations
cues_event_refs
traceability_refs
```

This table allows RDGP to determine whether a specific surface is current,
stale, superseded, unvalidated, refresh-required, or incomparable.

`currency_basis_type` may have values like:

```text
source_release_update
corpus_generation_update
policy_update
validation_update
method_update
dependency_missing
manual_declaration
not_evaluated
```

---

## 28. Output 3 — Reasoning Method Currency Table

The reasoning method currency table should contain one row per:

```text
reasoning_output_id × method_currency_policy_id
```

Conceptual fields:

```text
reasoning_output_id
reasoning_system
reasoning_method_id
reasoning_method_version
reasoning_method_family when applicable

input_tep_vdb_package_id
input_surface_set_id
input_surface_versions
input_dependency_set_id
input_dependency_set_fingerprint
input_policy_set_id
input_policy_set_fingerprint

generated_at
evaluated_at
method_currency_policy_id
current_against_package_id
current_against_method_version
current_against_dependency_set_id
reasoning_currency_state
refresh_readiness_label
comparability_state
superseded_by_reasoning_output_id
cues_event_refs
traceability_refs
```

This table is optional when no downstream reasoning outputs are present, but it
should be part of the RMCS model so RDGP outputs can safely re-enter VDB later.

---

## 29. Output 4 — Package-Level RMCS Summary

The package-level RMCS summary should contain one row per:

```text
tep_vdb_package_id
```

Conceptual fields:

```text
tep_vdb_package_id
package_generation_id
source_corpus_id
surface_count
current_surface_count
current_with_note_surface_count
stale_surface_count
superseded_surface_count
unvalidated_surface_count
validation_failed_surface_count
not_comparable_surface_count
refresh_required_count
refresh_recommended_count
currency_unknown_count
highest_currency_severity_label
package_currency_state
package_validation_state
package_comparability_state
rmcs_summary_label
anti_overclaim_label
traceability_refs
source_corpus_generation_id
dependency_set_id
dependency_set_fingerprint
surface_family_summary
daughter_surface_dependency_summary
comparability_scope_summary
refresh_blocked_count
stale_policy_count
stale_source_count
stale_method_count
stale_surface_specific_dependency_count
```

The package-level summary should be an intake aid only. It must not imply that
all included surfaces are equally current, equally comparable, or equally valid.
RDGP should be able to inspect surface-level and dependency-level RMCS rows when
a package-level summary reports stale, blocked, unknown, or incomparable state.

This table gives RDGP a compact governance summary without replacing detailed dependency-level traceability.

---

## 30. RMCS Evidence Labels

RMCS labels should be governance labels, not evidence-strength labels.

Safe labels:

```text
current_against_declared_dependencies

current_with_declared_limitations

stale_against_source_release

stale_against_projection_policy

stale_against_corpus_generation

stale_against_reasoning_method

superseded_by_newer_surface

refresh_required

refresh_recommended

not_comparable_under_policy

currency_unknown

currency_not_evaluated
```

Unsafe labels:

```text
better_method

worse_method

more_true

less_true

clinically_invalid

diagnostically_updated

evidence_strength_increased

evidence_strength_decreased
```

A method can be newer without being better. A stale surface can remain useful. A current surface can still be invalid if validation fails.

---

## 31. Required Traceability

Every RMCS row should preserve traceability to:

```text
artifact manifest
surface manifest
source corpus generation manifest
assertion record index
topology build receipt
geometry build receipt
projection policy receipt
namespace policy receipt
opportunity policy receipt
validation receipt
external source release manifest
RDGP method manifest when applicable
explicit unavailable/not-evaluated state when no dependency data exist
```

The traceability rule is:

```text
No RMCS currency, refresh, validation, or comparability label may be emitted
without a dependency, policy, validation, source-release, method-manifest, or
explicit unavailable/not-evaluated basis.
```

---

## 32. Required Validation

RMCS validation should verify:

```text
every artifact has a stable artifact_id

every dependency relation has dependency_id and dependency_type

every currency label has a currency_policy_id

every validation state references a validation receipt or explicit not-evaluated state

every comparability label references a comparability policy or explicit not-evaluated state

every refresh label references a refresh policy or explicit not-evaluated state

surface-level summaries agree with dependency-level rows

package-level summaries agree with surface-level rows

reasoning-output currency rows reference the input TEP-VDB package and method version

currency_unknown is not silently treated as current

validation_failed is not silently treated as stale only

superseded artifacts retain traceability to the artifact that superseded them when known

dependency_set_fingerprint is present for surface-level currency rows

surface-specific policy dependencies are preserved when applicable

surface currency summaries do not hide stale daughter-surface dependencies

comparability state is emitted when scan, window, null-model, recurrence-unit,
deduplication, target-bridge, feature-catalog, prior-scope, or matching policy
differs across artifacts

random seed and number of null draws are tracked for exploratory empirical-null
surfaces when required by policy

RMCS rows distinguish current, valid, and comparable

package-level summaries do not imply surface-level comparability

RDGP reasoning-output currency rows include input dependency-set identity

surface-specific stale states are not collapsed to generic stale state when the
specific dependency class is known
```

RMCS validation should also ensure that package-level summaries never replace detailed dependency traceability.

---

## 33. Anti-Overclaim Rules

RMCS must explicitly prohibit:

```text
fresh artifact treated as valid artifact

valid artifact treated as current artifact

current artifact treated as true evidence

stale artifact treated as false evidence

newer method treated as better method

method-version change treated as evidence-strength change

surface generated under different policies compared without comparability state

RDGP output silently reused after input package changes

external source update ignored

policy update hidden from downstream consumers

currency_unknown treated as current

validation_not_evaluated treated as validation_passed

RMCS label treated as RDGP prioritization score

package-level summary replacing dependency-level traceability

same source corpus treated as same dependency set

same surface type treated as comparable without policy comparison

same recurrence count treated as comparable after recurrence-unit or
deduplication policy changes

same burden statistic treated as comparable after null-model, window, matching,
or randomization-policy changes

same feature projection treated as comparable after feature catalog or linkage
policy changes

same phenotype prior treated as comparable after phenotype-scope or prior
evaluation-universe changes

current package treated as all surfaces current

current surface treated as all surface rows current

RMCS package summary treated as replacement for dependency manifest
```

Recommended anti-overclaim label:

```text
currency_surface_not_evidence_strength_claim
stale_not_false
newer_not_better
```

---

## 34. v1 Minimum Viable Surface

RMCS v1 should support the following artifacts:

```text
TEP-VDB package
source corpus generation
registration unit index
assertion record index
projection surface
projection policy
namespace policy
opportunity policy
validation receipt
GSC prior package if present
known assertion source version if present
feature catalog version if present
RDGP reasoning output if re-ingested
surface-specific projection policies
surface-specific validation profiles
daughter-surface dependency manifests where applicable
dependency set fingerprints
comparability scope identifiers
```

Minimum v1 outputs:

```text
RMCS dependency manifest table

RMCS surface currency table

RMCS reasoning method currency table when RDGP outputs are present

RMCS package-level summary

surface-specific dependency summary fields

dependency-set fingerprint fields

comparability-scope fields
```

Minimum v1 states:

```text
current
current_with_note
stale
superseded
unvalidated
validation_failed
not_comparable
refresh_recommended
refresh_required
currency_unknown
currency_not_evaluated
```

RMCS v1 does not need to solve automated semantic policy-diffing. It does need
to preserve enough dependency identity for VDB, RDGP, and future validators to
know when two surfaces or reasoning outputs were generated under different
corpus, policy, source, validation, or method conditions.

This is sufficient for VDB and RDGP to avoid silent reuse of stale or incomparable evidence substrates.

---

## 35. Future Extensions

Future RMCS versions may support:

```text
fine-grained cell-level currency for individual surface rows

source-specific currency policies

automated dependency-difference reports

surface-to-surface comparability matrices

RDGP model-family compatibility matrices

schema migration compatibility state

longitudinal package lineage visualization

reasoning-output invalidation policies when explicit validation supports them

external source deprecation and withdrawal propagation

policy-diff summaries for changed projection rules
```

These extensions should remain governance-layer features. They should not turn RMCS into an evidence-strength or truth-adjudication model.

---

## 36. Strategic Value

RMCS is the surface that lets VDB and RDGP remain honest over time.

Without RMCS:

```text
old surfaces look current,
new surfaces look automatically better,
RDGP outputs can be reused after evidence changed,
CFBS/MPLC runs can be compared across incompatible policies,
and source updates can silently desynchronize TEP-VDB packages.
```

With RMCS:

```text
every surface knows what it depended on,
every reasoning result knows what it consumed,
every package knows whether it is current, stale, superseded, unvalidated,
or incomparable,
and RDGP can decide when refresh or re-reasoning is required.
```

RMCS completes the projection-surface family by providing time-aware, policy-aware, dependency-aware governance for all TEP-VDB surfaces.

---

## 37. Summary Doctrine

```text
RMCS exposes dependency, currency, validation, refresh, and comparability state.

RMCS does not convert currency state into truth, evidence strength, clinical
interpretation, or method superiority.

RDGP uses RMCS to determine whether evidence substrates and prior reasoning
remain current, stale, superseded, unvalidated, incomparable, or
refresh-required.
```

A compact summary:

```text
RMCS is the TEP-VDB projection surface that exposes dependency, currency,
validation, refresh, and comparability state for VDB surfaces, source releases,
projection policies, corpus generations, and downstream reasoning outputs so
RDGP can determine whether evidence substrates and prior reasoning remain
current, stale, superseded, unvalidated, incomparable, or refresh-required
without VDB converting currency state into truth, evidence strength, or
clinical interpretation.
```

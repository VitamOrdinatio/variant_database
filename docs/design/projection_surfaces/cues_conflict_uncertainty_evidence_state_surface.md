# CUES: Conflict / Uncertainty Evidence-State Surface

**Status:** SAGE-VDB design draft  
**Intended path:** `docs/design/projection_surfaces/cues_conflict_uncertainty_evidence_state_surface.md`  
**Layer:** TEP-VDB projection surface design  
**Surface family:** Epistemic safety / conflict and uncertainty state  
**Parent architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## 1. Purpose

The Conflict / Uncertainty Evidence-State Surface (CUES) is the TEP-VDB projection surface that exposes conflict, uncertainty, ambiguity, missingness, limitation, staleness, scope mismatch, and related epistemic states across VDB-derived evidence objects and projection surfaces.

CUES exists so RDGP and other downstream reasoning systems do not consume VDB projection surfaces as falsely clean support.

CUES answers the question:

```text
Where is the evidence conflicted, ambiguous, unresolved, stale, incomplete,
scope-mismatched, or otherwise unsafe to treat as clean support?
```

CUES does not resolve these states. It makes them explicit, typed, traceable, and consumable.

---

## 2. Core Doctrine

```text
CUES does not resolve conflict.

CUES exposes conflict, uncertainty, ambiguity, missingness, incompleteness,
staleness, limitation, and epistemic state so RDGP can reason with caution
rather than consuming falsely clean evidence surfaces.
```

CUES is the epistemic safety layer of TEP-VDB.

It does not answer:

```text
Which source is correct?
Which variant is causal?
Which gene should be prioritized?
Which uncertainty should be ignored?
Which conclusion is clinically valid?
```

It answers:

```text
What uncertainty or conflict exists?
Where does it attach?
Which object or surface does it affect?
What source state produced it?
What reasoning effect should downstream systems consider?
Can the event be traced back to source assertions, policies, surfaces, or receipts?
```

---

## 3. Relationship to TEP-VDB Architecture

TEP-VDB is a projection-rich transport package emitted by VDB for RDGP and related downstream consumers.

Within that architecture:

```text
Producer TEPs
    → Assertion Records
    → Evidence Topology
    → Convergence Geometry
    → Projection Surfaces
    → TEP-VDB
    → RDGP
```

CUES is a cross-cutting projection surface over the projected evidence state.

It indexes epistemic concerns arising from:

```text
source assertions
identity brokerage
projection memberships
surface cells
policy receipts
validation receipts
surface generation state
source version state
opportunity/callability state
phenotype scope state
genotype/call quality state
```

CUES allows RDGP to consume evidence surfaces with explicit caution and limitation context.

---

## 4. Relationship to Mathematical Formalism

Under the VDB mathematical formalism, CUES is a projection over epistemic-state annotations in the evidence topology and emitted surfaces.

```text
S_CUES = F_CUES(T_C, M_CUES, P_CUES)
```

Where:

```text
T_C      = evidence topology for corpus generation C
M_CUES   = membership operator from evidence/surface objects to CUES events
P_CUES   = event detection, classification, severity, reasoning-effect,
           and summary policy
S_CUES   = conflict / uncertainty evidence-state surface
```

When opportunity uncertainty is involved, OACS-derived opportunity context may enter as part of the source substrate:

```text
S_CUES = F_CUES(T_C, M_CUES, Ω_related, P_CUES)
```

CUES is not a probabilistic confidence model unless a future version explicitly declares one. In v1, CUES is a deterministic event and summary surface.

---

## 5. Scientific Question

CUES asks:

```text
For each evidence object, projection membership, surface cell, or emitted
TEP-VDB object, what conflict, uncertainty, ambiguity, missingness, limitation,
staleness, or scope mismatch should be visible to downstream reasoning?
```

It does not ask:

```text
Is the evidence ultimately true?
Is this gene causal?
Is this variant pathogenic?
Is this reasoning result clinically valid?
```

---

## 6. What This Surface Is

CUES is:

```text
an epistemic-state surface

a cross-surface warning and limitation index

a conflict and uncertainty event registry

a package-level caution substrate

a traceability-preserving evidence-state projection

a downstream reasoning safety surface
```

CUES exposes structured events such as:

```text
clinical-significance conflict
variant identity ambiguity
gene bridge ambiguity
genotype uncertainty
phase missingness
ploidy unknown
opportunity unmodeled
callability unknown
phenotype scope mismatch
projection policy missing
traceability incomplete
source assertion deprecated
surface validation warning
surface currency stale
```

---

## 7. What This Surface Is Not

CUES is not:

```text
a conflict resolver
an adjudication engine
a majority-vote system
a pathogenicity classifier
a diagnostic report
a gene-prioritization model
an ACMG interpreter
an inheritance model
a confidence score unless explicitly governed by a later policy
a replacement for source assertions
a replacement for source-specific uncertainty labels
a replacement for event-level traceability
```

CUES should never convert uncertainty into certainty.

---

## 8. Core Unit

The event-level core unit of CUES is:

```text
evidence_object_id × cues_event_id
```

`evidence_object_id` may refer to any object that can carry epistemic state:

```text
sample_variant_observation_id
genotype_observation_id
known_pathogenicity_assertion_membership_id
projected_gene_target_id
opportunity_target_id
feature_projection_membership_id
phenotype_prior_membership_id
surface_cell_id
surface_id
TEP-VDB package id
```

This design is intentionally object-agnostic. Conflict and uncertainty can occur at variant, genotype, gene, feature, surface-cell, policy, receipt, or package level.

---

## 9. Event Classes

CUES should distinguish different epistemic event classes. These are not interchangeable.

Recommended v1 `cues_event_class` values:

```text
conflict
uncertainty
ambiguity
missingness
limitation
staleness
scope_mismatch
quality_concern
provenance_gap
identity_resolution_issue
opportunity_issue
method_currency_issue
validation_issue
not_evaluated
```

These classes allow RDGP to handle epistemic states differently.

For example:

```text
conflict
    may require caution, review, or downstream adjudication

missingness
    may block a reasoning feature

ambiguity
    may require branch-aware reasoning

staleness
    may trigger refresh or currency review

scope_mismatch
    may prevent evidence reuse in a declared context
```

---

## 10. Event Types

Recommended v1 `cues_event_type` values include:

```text
clinical_significance_conflict
pathogenic_vs_benign_conflict
known_assertion_vus_or_uncertain
source_assertion_deprecated
source_assertion_withdrawn
source_version_stale
variant_identity_ambiguous
variant_identity_unresolved
gene_bridge_ambiguous
gene_bridge_unresolved
regulatory_feature_link_ambiguous
phenotype_scope_mismatch
phenotype_scope_not_declared
gsc_prior_scope_uncertain
genotype_low_quality
genotype_no_call
genotype_partial_no_call
genotype_missing
phase_missing
phase_conflicting
ploidy_unknown
mitochondrial_context_uncertain
callability_unknown
opportunity_unmodeled
opportunity_not_assayed
opportunity_not_callable
negative_evidence_not_allowed
projection_policy_missing
projection_policy_unknown
surface_validation_warning
surface_validation_failed
traceability_incomplete
traceability_missing
surface_currency_unknown
surface_currency_stale
method_version_mismatch
```

This list is intentionally extensible.

Additional genotype-relationship and multiallelic brokerage event types:

```text
multiallelic_relationship_deferred
multiallelic_relationship_ambiguous
multiallelic_relationship_unresolved
genotype_variant_relationship_missing
genotype_variant_relationship_not_evaluated
genotype_variant_relationship_policy_unavailable
called_allele_index_out_of_range
allele_index_mapping_ambiguous
allele_index_mapping_unresolved
normalization_ambiguous
normalization_policy_unavailable
symbolic_alt_unresolved
spanning_deletion_context_required
missing_variant_identity
allele_depth_vector_mismatch
allele_depth_unavailable
relationship_traceability_incomplete
```

---

## 11. Source Labels and Normalized CUES Labels

CUES must preserve source-specific labels while mapping them into a common event vocabulary.

A CUES event should include both:

```text
source_uncertainty_label
normalized_uncertainty_state
```

Example:

```text
source_uncertainty_label = "conflicting interpretations of pathogenicity"
normalized_uncertainty_state = clinical_significance_conflict
```

Another example:

```text
source_uncertainty_label = "GQ below policy threshold"
normalized_uncertainty_state = genotype_low_quality
```

The normalized state is additive. It must not replace or destroy the source label.

---

## 12. Severity Labels

CUES may emit severity-like fields, but v1 severity should be categorical, policy-declared, and non-probabilistic. Severity labels are surface-consumption labels, not biological severity,
clinical severity, or evidence strength.

Recommended `cues_severity_label` values:

```text
informational
caution
limitation
blocking
review_required
unknown
not_evaluated
```

Severity is not an RDGP score.

Severity indicates how the event should be treated as a surface-consumption concern.

---

## 13. Reasoning-Effect Labels

CUES may declare a `reasoning_effect_label` to help RDGP consume the event safely.

Recommended values:

```text
no_effect_declared
use_with_caution
requires_surface_context
requires_manual_review
limits_negative_evidence
limits_positive_evidence
blocks_specific_reasoning_feature
blocks_surface_consumption
triggers_refresh
not_evaluated
```

Examples:

```text
opportunity_unmodeled
    → limits_negative_evidence

variant_identity_ambiguous
    → limits_positive_evidence

surface_currency_stale
    → triggers_refresh

missing_traceability
    → blocks_surface_consumption
```

The reasoning-effect label does not prioritize genes or variants. It only describes safe downstream handling of the evidence object.

---

## 14. Relationship to KVPS

KVPS exposes known pathogenicity evidence attached to sample-specific observed variants.

CUES indexes epistemic concerns affecting KVPS evidence, such as:

```text
clinical-significance conflict
pathogenic vs benign disagreement
VUS / uncertain state
source assertion deprecated
source version stale
ambiguous variant identity match
phenotype-scope mismatch
traceability incomplete
```

KVPS may say:

```text
known pathogenicity evidence attached
```

CUES may say:

```text
that known evidence is conflicting, stale, identity-ambiguous, or scope-limited
```

CUES does not override KVPS. It annotates the epistemic state that RDGP must consider.

---

## 15. Relationship to PGERS

PGERS rolls patient-specific evidence onto governed gene, locus, or gene-adjacent targets.

CUES indexes epistemic concerns affecting PGERS, such as:

```text
ambiguous gene bridge
lossy projection route
regulatory link ambiguity
conflicting evidence strata
patient-gene rollup includes unresolved memberships
source evidence present only through uncertain projection
PGERS summary derived from incomplete membership traceability
```

PGERS may say:

```text
patient-gene evidence present
```

CUES may say:

```text
the evidence is projected through an ambiguous bridge or lossy route
```

---

## 16. Relationship to GIRS

GIRS exposes genotype observation structure and inheritance-readiness context.

CUES indexes epistemic concerns affecting GIRS, such as:

```text
genotype low quality
genotype no-call
genotype partial no-call
genotype missing
phase missing
phase conflicting
ploidy unknown
mitochondrial context uncertain
raw genotype field unavailable
```

GIRS may say:

```text
genotype context available but inheritance-readiness limited
```

CUES may say:

```text
low genotype quality limits positive evidence or missing phase blocks a specific
inheritance feature
```

CUES does not infer inheritance models.

---

## 17. Relationship to OACS

OACS exposes opportunity, callability, and absence-readiness state.

CUES indexes epistemic concerns affecting OACS, such as:

```text
opportunity unmodeled
callability unknown
region not assayed
region not callable
low-confidence territory
unknown opportunity bases
negative evidence not allowed
assay scope unknown
variant class opportunity not modeled
```

OACS may say:

```text
absence is not interpretable because opportunity is unknown
```

CUES may summarize this as:

```text
opportunity_issue with reasoning effect limits_negative_evidence
```

---

## 18. Relationship to PAPS

PAPS owns phenotype alignment and phenotype-scoped prior context.

CUES indexes PAPS-related epistemic concerns such as:

```text
phenotype scope mismatch
phenotype scope not declared
phenotype mapping ambiguous
GSC prior scope uncertain
prior source stale
phenotype-prior bridge unresolved
```

CUES prevents phenotype prior evidence from being consumed as clean support when its scope is mismatched or ambiguous.

---

## 19. Relationship to RFPS

RFPS owns regulatory and feature projection evidence.

CUES indexes RFPS-related epistemic concerns such as:

```text
regulatory feature link ambiguous
feature-to-gene bridge uncertain
feature source stale
feature membership low confidence
coordinate-to-feature overlap ambiguous
noncoding projection route lossy
```

CUES prevents feature overlap from being silently converted into mechanism or direct gene evidence.

---

## 20. Relationship to CFBS, MPLC, and EVRS

CUES applies to discovery-oriented surfaces as well.

For CFBS, CUES may index:

```text
window opportunity incomplete
scan denominator uncertain
candidate interval low callability
high-scoring window driven by low-confidence territory
```

For MPLC, CUES may index:

```text
target/background matching limitation
locus opportunity mismatch
prior locus scope mismatch
background sampling warning
```

For EVRS, CUES may index:

```text
recurrence count may include duplicate source observations
allele identity ambiguity
sample independence uncertain
cohort membership uncertain
```

CUES prevents discovery surfaces from being overread as clean statistical or biological conclusions.

---

## 21. Relationship to RMCS

RMCS owns reasoning and method currency state.

CUES may index RMCS-generated concerns such as:

```text
surface currency stale
method version mismatch
reasoning output no longer current
source corpus updated after surface generation
refresh required
```

The boundary is:

```text
RMCS declares currency and refresh state.
CUES exposes the epistemic effect of that state for downstream consumption.
```

CUES should not absorb RMCS.

---

## 22. Event-Level Output

CUES should emit an event-level output with one row per CUES event.

Conceptual primary key:

```text
cues_event_id
```

Recommended fields:

```text
cues_event_id
tep_vdb_id
surface_id
surface_cell_id
evidence_object_id
evidence_object_type
sample_id
gene_id
variant_observation_id
genotype_observation_id
assertion_id
source_assertion_key
producer_family
source_surface_ref
cues_event_class
cues_event_type
source_uncertainty_label
normalized_uncertainty_state
conflict_participant_refs
conflicting_assertion_refs
scope_context
severity_label
reasoning_effect_label
review_recommendation_label
traceability_refs
anti_overclaim_label
```

The event-level output is the audit surface.

---

## 23. Summary-Level Output

CUES should also emit summary-level outputs for RDGP consumption.

Recommended summary units:

```text
sample_variant_observation_id
sample_id × projected_gene_target_id
surface_cell_id
surface_id
TEP-VDB package id
```

Recommended fields:

```text
object_id
object_type
has_conflict
has_uncertainty
has_ambiguity
has_missingness
has_limitation
has_staleness
has_scope_mismatch
has_blocking_issue
highest_severity_label
reasoning_effect_summary
review_recommended
event_count
blocking_event_count
review_required_event_count
event_refs
traceability_refs
anti_overclaim_label
```

The summary-level output is the RDGP-friendly surface.

CUES summaries must remain reconstructable from event-level rows and must not
replace event-level traceability.

---

## 24. Package-Level CUES Summary

CUES should emit a TEP-VDB package-level summary.

Recommended fields:

```text
tep_vdb_id
source_corpus_id
surface_generation_id
cues_surface_id
total_cues_event_count
conflict_event_count
uncertainty_event_count
ambiguity_event_count
missingness_event_count
limitation_event_count
staleness_event_count
scope_mismatch_event_count
blocking_event_count
review_required_event_count
surfaces_with_warnings
surfaces_with_blocking_events
package_highest_severity_label
package_reasoning_effect_summary
package_consumption_status
```

This allows RDGP and validation systems to rapidly determine whether the package has epistemic concerns that affect consumption.


`package_consumption_status` might have values such as:

```text
consumable_with_no_blocking_cues
consumable_with_cautions
consumable_with_blocking_events
consumption_not_evaluated
```

---

## 25. Traceability Requirements

Every CUES event must trace to at least one of:

```text
source assertion
source assertion key
Assertion Record
Registration Unit
Corpus Generation
identity brokerage receipt
projection policy receipt
projection membership
surface cell
surface validation receipt
opportunity receipt
currency receipt
explicit unknown/unavailable state
```

Required rule:

```text
Every CUES event must trace to the source assertion, surface cell,
policy receipt, validation receipt, or explicit missing/unavailable state
that generated the event.
```

A CUES event without traceability is itself a CUES event:

```text
traceability_missing
```

---

## 26. Validation Requirements

CUES validation should confirm:

```text
every event has a stable cues_event_id

every event has an object_id and object_type

every event declares event_class and event_type

every event has source label or explicit source-unavailable state

every event has normalized_uncertainty_state

every event has severity_label

every event has reasoning_effect_label

every event has traceability_refs or explicit traceability_missing event

summary-level counts match event-level rows

package-level counts match lower-level summaries

blocking events are not silently omitted

surface validation failures produce CUES events

unknown/unmodeled states are explicit, not coerced to clean states
```

---

## 27. v1 Minimum Viable Surface

CUES v1 should support the following minimum event families:

```text
variant identity ambiguity
variant identity unresolved
gene bridge ambiguity
gene bridge unresolved
known pathogenicity conflict
known benign/pathogenic conflict
VUS or uncertain known assertion state
genotype uncertainty / no-call / low-quality call
phase missing
ploidy unknown
multiallelic relationship deferred / ambiguous / unresolved
genotype-to-variant relationship missing or not evaluated
called allele index out of range
allele index mapping ambiguous or unresolved
normalization ambiguous or unavailable
symbolic ALT unresolved
spanning deletion context required
missing allele-specific variant identity
allele depth vector mismatch or unavailable
opportunity unknown / unmodeled / not callable / not assayed
negative evidence not allowed
phenotype scope mismatch or not declared
projection policy missing or unknown
traceability incomplete or missing
surface validation warning or failure
surface currency unknown or stale when RMCS is available
```

Minimum v1 outputs:

```text
CUES event table
CUES object summary table
TEP-VDB package-level CUES summary
```

Minimum required fields:

```text
cues_event_id
object_id
object_type
surface_id
event_class
event_type
source_uncertainty_label
normalized_uncertainty_state
severity_label
reasoning_effect_label
traceability_refs
anti_overclaim_label
```

---

## 28. Allowed Claims

CUES may claim:

```text
this evidence object has a declared conflict event

this surface cell has a declared uncertainty event

this patient-gene summary has ambiguity or limitation present

this source assertion is deprecated, withdrawn, stale, or conflicting according
to preserved source state

this genotype context is low quality, missing, no-call, partial no-call, or
phase-limited under declared policy

this opportunity state limits negative evidence

this phenotype-prior context has scope mismatch or missing scope declaration

this surface has validation or currency warnings

this evidence should be used with caution, reviewed, refreshed, or blocked
under declared policy
```

---

## 29. Prohibited Claims

CUES must not claim:

```text
the conflict is resolved

the majority source is correct

the most recent source is automatically correct

the pathogenic interpretation is correct despite benign conflict

the VUS should be treated as pathogenic

the unknown state should be treated as negative

the missing state should be treated as absence

the gene is causal

the variant is diagnostic

the evidence is clinically actionable

the RDGP priority should be reduced or increased by a CUES score unless RDGP
owns that scoring policy
```

---

## 30. Anti-Overclaim Labels

Recommended CUES anti-overclaim labels:

```text
conflict_surface_not_adjudication
uncertainty_surface_not_confidence_score
cues_event_not_rdgp_score
vus_not_pathogenic_or_benign_by_vdb
unknown_not_negative_evidence
missingness_not_absence
ambiguity_not_exact_identity
staleness_not_source_invalidity
severity_not_clinical_conclusion
review_required_not_diagnostic_result
```

Every emitted CUES row should carry an appropriate anti-overclaim label.

---

## 31. Anti-Collapse Rules

CUES should explicitly prohibit:

```text
conflict resolved by majority vote inside VDB

VUS treated as pathogenic or benign by VDB

unknown treated as negative

missingness treated as absence

ambiguity hidden from RDGP

low-quality genotype treated as high-confidence observation

phenotype-scope mismatch ignored

deprecated source assertion treated as current without warning

unresolved identity treated as exact

surface validation warning omitted from TEP-VDB

stale reasoning treated as current

CUES severity treated as RDGP score

CUES summary replacing event-level traceability
```

---

## 32. Implementation Notes

CUES should be built from:

```text
source uncertainty labels
source assertion states
identity brokerage statuses
projection policy receipts
surface validation receipts
surface currency receipts
surface-specific uncertainty fields
explicit unknown/unavailable states
```

CUES should not require every daughter surface to use identical field names internally, but every daughter surface should expose enough structured warning/limitation state for CUES to index.

A practical v1 approach:

```text
1. Define common CUES event vocabulary.
2. Require every daughter surface to emit uncertainty/conflict/limitation fields.
3. Build CUES event rows from these fields.
4. Build object-level summaries from event rows.
5. Build package-level summary from object summaries.
```

---

## 33. Relationship to RDGP

RDGP consumes CUES as a reasoning-safety surface.

RDGP may use CUES to:

```text
downweight or block specific reasoning features
flag evidence for manual review
avoid using negative evidence when opportunity is unknown
avoid treating ambiguous identity as exact
avoid treating stale surfaces as current
explain limitations in downstream outputs
trigger refresh or re-ingestion workflows
```

But RDGP, not CUES, owns reasoning outcomes.

The boundary is:

```text
CUES exposes epistemic state.
RDGP decides how epistemic state affects reasoning.
Scientists and clinicians interpret evaluated evidence.
```

---

## 34. Future Extensions

Future versions of CUES may support:

```text
formal uncertainty ontologies
probabilistic confidence models declared outside VDB preservation layer
source reliability calibration
branch-aware ambiguity propagation
manual review state integration
expert adjudication assertions as new source assertions
longitudinal conflict tracking across corpus generations
surface-level uncertainty propagation graphs
machine-readable reasoning-effect contracts for RDGP
```

Any future confidence or probability model must be explicitly declared and must not replace source traceability.

---

## 35. Summary Doctrine

```text
CUES is the TEP-VDB projection surface that exposes conflict, uncertainty,
ambiguity, missingness, limitation, staleness, scope mismatch, and epistemic
state across VDB-derived projection surfaces so RDGP can consume evidence with
explicit caution, review, and reasoning-effect context rather than treating
all projected evidence as clean support.
```

In short:

```text
CUES exposes epistemic state.
RDGP reasons with epistemic state.
Scientists and clinicians interpret evaluated evidence.
```

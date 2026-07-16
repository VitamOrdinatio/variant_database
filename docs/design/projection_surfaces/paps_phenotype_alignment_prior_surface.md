# PAPS — Phenotype Alignment / Prior Surface

**Status:** SAGE-VDB design draft  
**Intended path:** `docs/design/projection_surfaces/paps_phenotype_alignment_prior_surface.md`  
**Surface family:** TEP-VDB known-today diagnostic-support surface; cross-supporting phenotype-prior context surface
**Primary downstream consumer:** RDGP  
**Related architecture:** `docs/architecture/tep_vdb_architecture.md`  
**Mathematical foundation:** `docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md`

---

## 1. Purpose

The Phenotype Alignment / Prior Surface (PAPS) is the TEP-VDB projection surface that exposes declared phenotype context, phenotype namespace mapping state, phenotype-gene prior evidence, GSC-derived prior provenance, target identity bridge status, phenotype-scope alignment labels, uncertainty/currency context, and anti-overclaim boundaries for downstream RDGP reasoning.

PAPS exists because phenotype priors are powerful but dangerous if flattened into generic gene support. A phenotype-scoped prior for an epilepsy gene, mitochondrial disease gene, or other disease-contextual gene set is not a diagnosis, not a patient-specific phenotype fit, and not a causal-gene conclusion. PAPS preserves the scope, source, policy, and limitations of phenotype-prior evidence so RDGP can reason over it safely.

The central doctrine is:

```text
PAPS does not diagnose phenotype fit.

PAPS exposes declared phenotype context, phenotype-gene prior evidence,
phenotype-scope alignment state, and prior provenance so RDGP can reason over
phenotype relevance without VDB converting priors into causal or diagnostic
claims.
```

---

## 2. Relationship to TEP-VDB Architecture

TEP-VDB is a projection-rich, provenance-preserving reasoning transport package emitted by VDB for RDGP. Within that package, PAPS is the surface responsible for phenotype-context and phenotype-prior alignment.

PAPS contributes to both major RDGP reasoning activities:

```text
Known-today diagnostic support:
    contextualize known variant, genotype, and gene/locus evidence using
    declared phenotype-scoped priors.

Unknown-tomorrow discovery support:
    contextualize recurrence, burden, regulatory projection, and locus-level
    signals using phenotype-scoped prior evidence without treating those priors
    as proof of disease association.
```

PAPS is the clean bridge between GSC and RDGP through VDB. It preserves phenotype scope and prior provenance while leaving prioritization and phenotype-fit reasoning to RDGP.

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

PAPS is the specialization:

```text
θ_PAPS:
    source objects =
        phenotype context assertions,
        phenotype namespace mappings,
        phenotype-gene prior records,
        GSC TEP outputs,
        projected gene/locus/feature targets,
        optional KVPS/PGERS/RFPS/EVRS context

    target objects =
        phenotype-context × target prior memberships and summaries

    membership =
        target belongs to a phenotype-prior surface if it matches a
        phenotype-scoped prior under declared target identity and
        phenotype-mapping policy

    opportunity =
        not primary, except for declaring whether phenotype context or prior
        sources were available/evaluated

    geometry =
        phenotype-prior stratification, alignment-state summaries,
        prior-source and prior-strength summaries

    surface =
        phenotype alignment and prior substrate for RDGP
```

Compactly:

```text
S_PAPS = F_PAPS(T_C, M_PAPS, P_PAPS)
```

Where needed, an availability/evaluation opportunity term may be included:

```text
S_PAPS = F_PAPS(T_C, M_PAPS, Ω_PAPS, P_PAPS)
```

Here `Ω_PAPS` describes phenotype-context and prior-source availability. It is not genomic callability; genomic opportunity remains OACS responsibility.

Every PAPS prior or alignment-state label must trace to a phenotype context record, prior source record, target identity bridge, mapping policy, or explicit unavailable/not-evaluated state.

---

## 4. Scientific Question

PAPS answers:

```text
What phenotype-scoped prior context is attached to this gene, locus, feature,
variant, sample, or cohort — and how safely does that context align with the
declared phenotype context?
```

PAPS does not answer:

```text
Does this gene explain the patient?
Does this patient have the disease?
Does this variant explain the phenotype?
Is this a clinically diagnostic match?
```

Those are RDGP or clinical interpretation questions.

---

## 5. What PAPS Is

PAPS is a governed phenotype-prior projection surface. It exposes:

```text
declared phenotype context
phenotype namespace mapping state
phenotype-gene prior memberships
GSC-derived prior evidence
prior source provenance
prior strength labels as emitted by source systems
phenotype-scope alignment labels
target identity bridge state
prior currency / uncertainty context
traceability receipts
anti-overclaim labels
```

PAPS may attach phenotype-prior context to:

```text
genes
gene loci
transcripts
feature-linked gene targets
regulatory features
variant-associated gene targets
pathways or modules if later supported
```

For v1, the dominant target type is expected to be phenotype-scoped gene priors, especially from GSC.

---

## 6. What PAPS Is Not

PAPS is not:

```text
a diagnostic engine
a phenotype-fit model
a causal-gene classifier
a patient phenotype similarity engine
a gene prioritization score
a replacement for GSC
a replacement for RDGP
a clinical interpretation report
a generic gene-support flattener
```

PAPS must not convert phenotype-scoped priors into disease causality, diagnosis, or patient-specific phenotype fit.

---

## 7. Core Doctrine

PAPS should preserve four concepts separately:

```text
declared_corpus_phenotype_scope

declared_sample_phenotype_context

phenotype_prior_scope_alignment

computed_or_downstream_patient_phenotype_fit
```

VDB/PAPS may expose the first two when they are present in the evidence substrate.

VDB/PAPS may also expose `phenotype_prior_scope_alignment` when the alignment is
a policy-declared comparison between a preserved prior scope and a declared
phenotype context.

RDGP owns `computed_or_downstream_patient_phenotype_fit` unless a producer
explicitly emits phenotype-fit reasoning as a preserved assertion.

The distinction is:

```text
phenotype_prior_scope_alignment
    Does this prior's declared phenotype scope match, broadly relate to,
    mismatch, or remain unevaluated relative to a declared phenotype context?

computed_or_downstream_patient_phenotype_fit
    Does this patient's phenotype profile fit this gene, disease, mechanism,
    or diagnosis?
```

The architectural boundary is:

```text
PAPS exposes phenotype-prior scope and alignment substrate.
RDGP evaluates phenotype relevance, prioritization, and patient phenotype fit.
Scientists and clinicians interpret evaluated evidence.
```

---

## 8. Core Surface Unit

The core PAPS unit is:

```text
phenotype_context_id × projected_target_id × prior_policy_id
```

When sample-specific phenotype context is available, the preferred unit is:

```text
sample_id × phenotype_context_id × projected_target_id × prior_policy_id
```

The target should not be limited to a gene symbol. PAPS should preserve:

```text
projected_target_id
target_type
target_namespace
target_label
target_identity_bridge_status
prior_policy_id
phenotype_mapping_policy_id
alignment_policy_id
```

PAPS target identity should remain bridge-aware. A projected target may be a
gene, locus, feature-linked gene target, regulatory target, variant-associated
target, pathway, or future module. PAPS must preserve the bridge route and
lossiness state that connected the prior to the projected target.

Recommended additional identity fields:

```text
target_identity_bridge_id
target_identity_bridge_policy_id
target_identity_bridge_lossiness
target_identity_bridge_traceability_refs
```

A phenotype prior attached through a lossy or ambiguous target bridge must not be
represented as exact target support.


This prevents phenotype-prior evidence from being flattened into unqualified gene support.

---

## 9. Phenotype Context Levels

PAPS must distinguish phenotype context levels:

```text
corpus_level_phenotype_scope
cohort_level_phenotype_scope
sample_level_phenotype_context
family_level_phenotype_context if later supported
query_level_phenotype_context
producer_declared_phenotype_context
not_declared
not_evaluated
unknown
```

A cohort label such as `epilepsy` is not equivalent to a patient-level HPO-coded phenotype profile. PAPS must preserve the granularity of the phenotype context.

---

## 10. Phenotype Namespace and Mapping State

PAPS should preserve raw phenotype labels and normalized phenotype identifiers separately.

Conceptual phenotype fields include:

```text
raw_phenotype_label
normalized_phenotype_id
phenotype_namespace
phenotype_mapping_policy_id
phenotype_mapping_status
phenotype_scope_granularity
phenotype_context_source
phenotype_context_version
```

Supported or future phenotype namespaces may include:

```text
HPO
MONDO
OMIM
Orphanet
MeSH
GSC internal phenotype scope
free-text phenotype label
cohort label
study label
unknown
```

Mapping states may include:

```text
exact_phenotype_match
ancestor_descendant_match
sibling_or_related_term_match
broad_scope_match
narrow_scope_match
free_text_unmapped
ambiguous_mapping
mapping_not_attempted
mapping_unavailable
not_declared
```

Phenotype namespace mapping and phenotype-scope alignment are related but not
identical.

```text
phenotype_mapping_status
    describes how a raw phenotype label maps to a normalized phenotype identity
    or namespace.

phenotype_scope_alignment_status
    describes how a prior's declared phenotype scope relates to a declared
    corpus, cohort, sample, query, or producer phenotype context.
```

A phenotype may be successfully mapped but still mismatched to the prior scope.
Conversely, a broad cohort scope may be related to a prior scope without being a
precise patient-level phenotype match.

A broad cohort label must not be represented as a precise patient-level phenotype profile unless the source evidence supports that representation.

---

## 11. Prior Evidence Sources

PAPS is designed to preserve phenotype-scoped priors from VDB-ingested producers. In v1, the most important prior source is GSC.

For GSC-derived priors, PAPS should preserve:

```text
gsc_tep_id
gsc_tep_version
gsc_run_id
gsc_surface_or_record_id if available
gsc_prior_record_id when available
gsc_phenotype_scope_id when available
phenotype_scope
phenotype_scope_namespace
prior_strength_label
prior_score_if_source_emitted
source_contribution_refs
semantic_scoring_policy
source_evidence_families
gsc_source_identity_refs
prior_currency_state
prior_traceability_refs
```

PAPS should preserve GSC prior labels and scores as source-emitted or
policy-derived context. It must not recalibrate GSC priors into universal
patient-level probabilities or RDGP scores.

Safe PAPS statements:

```text
POLG has a mitochondrial-disease-scoped GSC prior.

SCN1A has epilepsy-scoped prior evidence from GSC under source policy X.
```

Unsafe PAPS statements:

```text
POLG is the patient's causal gene.

SCN1A explains this patient's epilepsy.
```

---

## 12. Prior Presence vs Phenotype Alignment

PAPS must distinguish two questions:

```text
Does this target have phenotype-scoped prior evidence?

Does that prior scope align with this declared phenotype context?
```

The first is prior presence. The second is phenotype-scope alignment. Neither is diagnosis.

Conceptual fields:

```text
prior_present
prior_scope
prior_strength_label
declared_phenotype_context
phenotype_scope_alignment_status
alignment_basis
alignment_policy_id
alignment_limitation
```

Safe phenotype-scope alignment labels include:

```text
prior_scope_matches_declared_context
prior_scope_broader_than_declared_context
prior_scope_narrower_than_declared_context
prior_scope_related_to_declared_context
prior_scope_mismatch
prior_scope_not_declared
sample_phenotype_not_available
alignment_not_evaluated
```

Unsafe labels include:

```text
phenotype_fit_good
phenotype_fit_bad
diagnostic_match
clinical_match_confirmed
```

PAPS alignment labels describe prior-scope relationship, not patient-level
phenotype fit.

For example:

```text
prior_scope_matches_declared_context
```

means that the prior's declared scope is compatible with the declared context
under the alignment policy. It does not mean:

```text
the patient's phenotype fits the gene
the gene explains the phenotype
the diagnosis is confirmed
the prior should increase RDGP rank by a fixed amount
```

---

## 12A. Projection Policy

A PAPS projection policy should declare:

```text
paps_projection_policy_id
paps_projection_policy_version
prior_policy_id
phenotype_mapping_policy_id
alignment_policy_id
target_identity_bridge_policy_id
prior_presence_policy_id
prior_absence_policy_id when prior absence is emitted
source_prior_scope_policy_id
prior_strength_label_policy_id
currency_reference_policy_id
CUES reference policy
RMCS reference policy
anti_overclaim_policy_id
traceability_policy_id
```

The policy must answer:

```text
Which phenotype contexts are eligible?

Which prior records are eligible?

How are raw phenotype labels mapped to phenotype identities?

How are prior scopes compared to declared phenotype contexts?

How are broad, narrow, related, mismatched, missing, and unevaluated states
represented?

How are target identities bridged?

How is target-bridge ambiguity or lossiness exposed?

When may prior absence be emitted?

What source prior labels or scores may be preserved?

What claims are prohibited?
```

PAPS projection policy must preserve source phenotype scope and target identity
bridge state. It must not silently convert phenotype-scoped prior evidence into
generic gene support.

---

## 13. Relationship to GSC

PAPS does not replace GSC. GSC produces phenotype-scoped semantic priors for phenotype-gene relationships. PAPS projects those priors into the TEP-VDB package while preserving their provenance, phenotype scope, source contribution context, and limitations.

PAPS must not detach GSC priors from their phenotype scope. A GSC prior is not generic gene support unless a declared policy explicitly exposes it as broad context with appropriate lossiness labeling.

Required GSC preservation principles:

```text
GSC phenotype scope remains explicit.
GSC prior source remains traceable.
GSC prior strength remains source-emitted or policy-derived, not silently altered.
GSC prior evidence families remain available through references.
GSC prior currency remains visible.
GSC prior is not converted into diagnosis or causality by VDB.
```

---

## 14. Relationship to KVPS

KVPS exposes known variant pathogenicity evidence attached to sample-specific observed variants. PAPS provides phenotype-prior context for the associated target.

Example:

```text
KVPS:
    observed variant matches known pathogenic assertion.

PAPS:
    associated gene has phenotype-scoped prior matching the declared context.

RDGP:
    may reason over the combination.
```

PAPS does not upgrade KVPS evidence. It only supplies phenotype-prior context.

---

## 15. Relationship to PGERS

PGERS rolls patient-specific evidence to gene, locus, or gene-adjacent targets. PAPS attaches phenotype prior context to those targets.

```text
PGERS:
    patient-specific evidence projected to a gene/locus target

PAPS:
    phenotype-context and phenotype-prior evidence attached to a target
```

PGERS may include PAPS-derived fields such as:

```text
paps_prior_present
paps_prior_strength_label
paps_alignment_status
paps_surface_ref
```

PAPS remains the authority for prior provenance and phenotype-scope alignment logic.

---

## 16. Relationship to RFPS

RFPS may project a noncoding variant to a regulatory feature or feature-linked gene target. PAPS may then attach phenotype-scoped prior context to that target.

Example:

```text
RFPS:
    noncoding variant projects to enhancer linked to gene X.

PAPS:
    gene X has epilepsy-scoped GSC prior evidence.

RDGP:
    may reason over the combined regulatory, phenotype-prior, and patient
    evidence context.
```

RFPS owns feature projection. PAPS owns phenotype prior context. RDGP owns interpretation.

---

## 17. Relationship to EVRS

EVRS exposes exact variant recurrence. PAPS may provide phenotype-prior context for the recurrent variant's projected gene/locus/feature target.

Safe combination:

```text
same exact allele recurs in declared scope
    +
projected target has phenotype-scoped prior evidence
```

Unsafe conclusion by PAPS:

```text
recurrent phenotype-matched disease allele
```

EVRS owns recurrence. PAPS owns phenotype prior context. RDGP evaluates the combined evidence.

---

## 18. Relationship to CFBS and MPLC

CFBS and MPLC are discovery-oriented burden/contrast surfaces. PAPS supplies phenotype-prior context for loci or targets involved in those surfaces.

For CFBS:

```text
candidate interval overlaps or projects to a target with phenotype-scoped prior
```

For MPLC:

```text
prior-informed target/background locus carries declared phenotype-prior context
```

PAPS does not own null models, burden enrichment, or disease association testing.

---

## 19. Relationship to CUES

PAPS should emit or reference CUES events for phenotype-prior uncertainty.

Examples:

```text
phenotype_scope_mismatch
phenotype_mapping_ambiguous
sample_phenotype_missing
prior_scope_not_declared
GSC prior stale
source contribution conflict
phenotype_namespace_mismatch
free_text_phenotype_unmapped
prior_source_unavailable
alignment_not_evaluated
```

PAPS should expose these locally, while CUES provides package-level epistemic event indexing.

---

## 20. Relationship to RMCS

RMCS owns method/corpus/surface currency. PAPS should expose RMCS references when prior currency matters.

Potential currency states:

```text
prior_current_under_policy
prior_stale_under_policy
prior_currency_unknown
prior_source_version_missing
prior_refresh_available
prior_currency_not_evaluated
```

PAPS does not decide that a stale prior is invalid. It exposes the currency state so RDGP can reason accordingly.

---

## 21. Surface Outputs

PAPS should emit at least two levels of output:

```text
phenotype-prior membership table
phenotype-prior summary table
```

A package-level phenotype-prior summary may also be useful for TEP-VDB audit and RDGP intake.

---

## 22. Phenotype-Prior Membership Table

One row per:

```text
phenotype_context_id × projected_target_id × prior_assertion_or_prior_record_id
```

Conceptual fields:

```text
paps_membership_id
paps_surface_id
paps_surface_generation_id
corpus_generation_id
source_corpus_id when distinct

sample_id when available
cohort_id when available
phenotype_context_id
phenotype_context_level
phenotype_context_source
raw_phenotype_label
normalized_phenotype_id
phenotype_namespace
phenotype_mapping_policy_id
phenotype_mapping_status
phenotype_scope_granularity

projected_target_id
target_type
target_namespace
target_label
target_identity_bridge_id
target_identity_bridge_status
target_identity_bridge_policy_id
target_identity_bridge_lossiness

prior_source
prior_record_id
gsc_tep_id
gsc_tep_version
gsc_run_id
gsc_prior_record_id when available
gsc_phenotype_scope_id when available
prior_scope
prior_scope_namespace
prior_strength_label
prior_score_if_emitted
prior_evidence_family
source_contribution_refs

paps_projection_policy_id
prior_policy_id
alignment_policy_id
phenotype_scope_alignment_status
alignment_basis
alignment_limitation

prior_currency_state
cues_event_refs
rmcs_currency_refs
traceability_refs
anti_overclaim_label
```

This table preserves auditability, prior provenance, target bridge state, and
source-level phenotype scope.

---

## 23. Phenotype-Prior Summary Table

One row per:

```text
sample_id × projected_target_id × phenotype_context_id × prior_policy_id
```

If sample phenotype is unavailable, a corpus-level summary may use:

```text
corpus_id × projected_target_id × phenotype_context_id × prior_policy_id
```

Conceptual fields:

```text
paps_summary_id
paps_surface_id
paps_surface_generation_id
corpus_generation_id
source_corpus_id when distinct

sample_id when available
cohort_id when available
phenotype_context_id
phenotype_context_level
projected_target_id
target_type
target_namespace

prior_present
prior_absence_state when emitted
prior_evaluation_universe_id when prior absence is emitted
strongest_prior_strength_label
prior_source_count
gsc_prior_present
gsc_prior_strength_label
phenotype_scope_alignment_status
phenotype_mapping_status
target_identity_bridge_status
target_identity_bridge_lossiness

prior_currency_state
cues_conflict_uncertainty_state
paps_evidence_label
membership_refs
anti_overclaim_label
traceability_refs
```
This table supports RDGP consumption without replacing membership-level
traceability or erasing phenotype scope.

---

## 24. Package-Level PAPS Summary

A TEP-VDB package may also include a compact PAPS summary:

```text
package_phenotype_contexts
package_prior_sources
package_gsc_prior_count
package_prior_target_count
package_phenotype_mapping_status_summary
package_alignment_status_summary
package_prior_currency_summary
package_cues_summary
```

This is an intake aid only. It must not replace the membership or summary tables.

---

## 25. PAPS Evidence Labels

Safe PAPS labels are prior-state or alignment-state labels:

```text
phenotype_scoped_prior_present
phenotype_scoped_prior_absent_within_declared_evaluation_universe
phenotype_scoped_prior_not_evaluated
phenotype_scope_matches_declared_context
phenotype_scope_related_to_declared_context
phenotype_scope_mismatch
phenotype_context_missing
phenotype_mapping_ambiguous
phenotype_prior_with_conflict_or_uncertainty
phenotype_prior_stale_or_currency_limited
```

Unsafe PAPS labels include:

```text
phenotype_fit_confirmed
diagnostic_match
causal_gene_supported
gene_explains_phenotype
clinical_relevance_confirmed
patient_has_gene_disease_match
```

These unsafe labels belong to downstream reasoning or clinical interpretation, if anywhere.

---

## 26. Alignment Basis

When PAPS emits an alignment state, it should declare the basis:

```text
corpus_scope_match
cohort_scope_match
sample_declared_phenotype_match
phenotype_namespace_mapping
ancestor_descendant_mapping
broad_related_scope
manual_or_source_declared_mapping
not_evaluated
unknown
```

Alignment labels without an alignment basis are unsafe because they hide how phenotype context was connected to prior scope.

---

## 27. Prior Strength Handling

PAPS may preserve source-emitted prior scores or labels, such as GSC strength labels or scores. It should not invent new cross-source probabilistic priors unless a declared policy exists.

Allowed:

```text
prior_strength_label as emitted by source
prior_score_if_source_emitted
source_contribution_summary_ref
policy-derived categorical label with policy ID
```

Disallowed in v1 unless a separate governed method is defined:

```text
universal phenotype-prior probability
cross-source calibrated gene score
patient-level phenotype-fit score
RDGP prioritization score
```

---

## 28. Phenotype Prior Absence

Absence of a phenotype prior is not evidence against a target.

PAPS may emit:

```text
phenotype_scoped_prior_absent_within_declared_evaluation_universe
```

only under a declared prior evaluation policy that defines the evaluated prior
universe.

When prior absence is emitted, PAPS should preserve:

```text
prior_absence_state
prior_evaluation_universe_id
prior_evaluation_policy_id
prior_source_scope
prior_source_version
prior_absence_limitation
```

The anti-overclaim boundary is:

```text
No PAPS prior attached does not mean the gene, locus, feature, or variant lacks
biological or diagnostic relevance.
```

This is especially important for novel disease genes, noncoding loci, weakly
curated phenotypes, emerging evidence, phenotype scopes not represented in GSC,
and targets outside the evaluated prior universe.

---

## 29. Traceability Requirements

Every PAPS row must trace to one or more of:

```text
phenotype context record
raw phenotype label
normalized phenotype identifier
phenotype mapping policy
phenotype-prior source record
GSC TEP record
GSC run record
source contribution reference
projected target identity bridge
alignment policy
currency receipt
CUES event
explicit unavailable/not-evaluated state
```

A PAPS row without traceability must be invalid or explicitly marked as traceability-limited.

---

## 30. Validation Requirements

PAPS validation should check:

```text
every membership row has a phenotype_context_id

raw phenotype labels are preserved when available

normalized phenotype IDs include namespace and mapping policy

prior source IDs are preserved

GSC priors retain phenotype scope

projected targets retain identity bridge status

alignment labels have alignment policy and basis

source-emitted scores are not silently transformed

missing sample phenotype is not treated as mismatch

absence of prior is not treated as negative evidence

CUES events are emitted for ambiguity, mismatch, missingness, and stale priors

traceability references resolve

anti-overclaim labels are present

phenotype_mapping_status and phenotype_scope_alignment_status are not collapsed

target identity bridge status and bridge lossiness are explicit

PAPS prior labels preserve source phenotype scope

prior absence is emitted only with a declared prior evaluation universe and policy

broad cohort phenotype scope is not promoted to sample-level phenotype profile

PAPS alignment labels are not phenotype-fit conclusions

membership-level rows support summary-level reconstruction

CUES and RMCS references are present when conflict, uncertainty, mismatch, or currency state is exposed
```

---

## 31. v1 Minimum Viable Surface

PAPS v1 should support:

```text
corpus-level phenotype scope
sample-level phenotype context if present
GSC phenotype-gene priors
gene target attachment
target identity bridge status
prior strength labels as emitted by GSC
broad alignment state between declared phenotype context and prior scope
CUES events for mismatch, ambiguity, missingness, or stale priors
```

PAPS v1 is not required to support:

```text
full patient HPO similarity scoring
gene-disease phenotype profile matching
quantitative phenotype-fit score
phenotype-driven diagnosis
causal-gene prioritization
```

Minimum outputs:

```text
PAPS phenotype-prior membership table
PAPS phenotype-prior summary table
PAPS package-level phenotype-prior summary
```

---

## 32. Anti-Overclaim Rules

PAPS must explicitly prohibit:

```text
cohort phenotype label treated as patient phenotype

GSC phenotype-gene prior treated as diagnosis

phenotype prior treated as patient-specific evidence by itself

broad phenotype scope treated as exact phenotype match

free-text phenotype treated as normalized phenotype without mapping status

phenotype namespace mappings treated as lossless

prior strength treated as RDGP score

phenotype-scope mismatch hidden

missing phenotype context treated as no phenotype relevance

absence of GSC prior treated as evidence against a gene

PAPS summary replacing prior/source traceability
```

The default anti-overclaim label is:

```text
phenotype_prior_not_patient_phenotype_match
```

Additional labels may include:

```text
phenotype_scope_not_diagnosis
phenotype_prior_not_causality
cohort_scope_not_patient_profile
prior_absence_not_negative_evidence
prior_scope_alignment_not_patient_phenotype_fit
phenotype_mapping_not_lossless_identity
target_bridge_not_exact_unless_declared
prior_absence_outside_universe_not_negative_evidence
```

---

## 33. Invalid PAPS Patterns

Invalid PAPS patterns include:

```text
A GSC prior is copied into PGERS as generic gene support without phenotype scope.

A cohort label is treated as a patient-level phenotype profile.

A broad phenotype namespace mapping is represented as an exact match.

A missing patient phenotype is represented as phenotype mismatch.

A PAPS prior-strength label is consumed as a gene-prioritization score.

A PAPS summary table is emitted without membership-level traceability.

A target with no GSC prior is marked as unsupported.

A phenotype-prior source is included without source version or policy context.

Phenotype namespace mapping is treated as phenotype-scope alignment.

Phenotype-scope alignment is treated as patient phenotype fit.

A lossy target bridge is represented as exact prior support.

Prior absence is emitted without a declared prior evaluation universe.

Corpus-level phenotype scope is silently reused as sample-level phenotype evidence.

GSC prior score is recalibrated into a patient-level probability without a declared downstream method.
```

These patterns should be caught by validation or surfaced through CUES.

---

## 34. RDGP Consumption Role

PAPS gives RDGP a safe phenotype-prior substrate.

RDGP may use PAPS to reason over:

```text
whether a candidate gene has phenotype-scoped prior evidence
whether the prior scope matches, broadly relates to, or mismatches the declared context
whether a known variant hit occurs in a phenotype-prior gene
whether a burden or recurrence signal occurs in a phenotype-prior target
whether regulatory feature projection reaches a phenotype-prior target
whether phenotype-prior context is stale, missing, ambiguous, or limited
```

PAPS itself does not perform these prioritization steps. It exposes the context.

---

## 35. Strategic Value

PAPS is the surface that lets VDB use GSC correctly.

Without PAPS:

```text
GSC priors may be flattened into generic gene support,
phenotype scope may be erased,
and RDGP may receive gene evidence without knowing whether the prior is
epilepsy-scoped, mitochondrial-scoped, broad, narrow, stale, or mismatched.
```

With PAPS:

```text
phenotype scope remains explicit,
prior provenance remains traceable,
alignment state is visible,
and RDGP can decide how to use phenotype-prior context.
```

This preserves the architecture:

```text
GSC emits phenotype-scoped priors.
VDB preserves and projects those priors through PAPS.
RDGP reasons over patient/corpus evidence using PAPS context.
Scientists and clinicians interpret evaluated evidence.
```

---

## 36. Summary Doctrine

```text
PAPS is the TEP-VDB projection surface that exposes declared phenotype
context, phenotype namespace mapping state, phenotype-gene prior evidence,
GSC-derived prior provenance, target identity bridge status, phenotype-scope
alignment labels, uncertainty/currency context, and anti-overclaim boundaries
so RDGP can reason over phenotype relevance without VDB converting
phenotype-scoped priors into diagnosis, causality, or patient-specific
phenotype fit.
```

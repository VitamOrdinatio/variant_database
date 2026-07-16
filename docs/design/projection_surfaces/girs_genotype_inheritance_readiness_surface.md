# GIRS: Genotype / Inheritance Readiness Surface

> Status: SAGE-VDB projection-surface design draft.
>
> Intended path:
>
> `docs/design/projection_surfaces/girs_genotype_inheritance_readiness_surface.md`
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
>     TEP-VDB known-today diagnostic-support surface;
>     cross-supporting genotype-readiness substrate for 
>     downstream reasoning.
>
> Primary consumer:
>
> RDGP and future downstream reasoning systems.

---

## 1. Purpose

The Genotype / Inheritance Readiness Surface, abbreviated **GIRS**, defines a TEP-VDB projection surface that exposes genotype observation structure for downstream reasoning.

GIRS exists because RDGP and future reasoning systems need genotype context in order to evaluate inheritance models, dosage hypotheses, zygosity-sensitive evidence, biallelic candidate structure, and sample-specific variant support.

However, VDB must not perform inheritance reasoning inside the projection layer.

GIRS therefore exposes genotype evidence state and readiness context. It does not conclude inheritance.

The central purpose of GIRS is:

```text
Expose genotype observation structure and inheritance-readiness context
for sample-specific variant observations while preserving raw genotype fields,
normalized structural call states, quality/depth/phase/ploidy limitations,
source traceability, and anti-overclaim boundaries.
```

GIRS makes TEP-VDB more useful to RDGP by allowing RDGP to reason over genotype-aware evidence without forcing RDGP to reconstruct VAP genotype fields, source records, identity mappings, or quality limitations from raw producer artifacts.

---

## 2. Relationship to TEP-VDB Architecture

TEP-VDB is a VDB-emitted, projection-rich reasoning transport package.

Within TEP-VDB, GIRS belongs to the known-today diagnostic-support surface family and also supports unknown-tomorrow discovery reasoning.

Conceptually:

```text
VDB
    preserves assertions
    brokers identities
    constructs topology
    projects genotype evidence state
    emits GIRS

RDGP
    consumes GIRS
    evaluates inheritance models downstream
```

GIRS supports several TEP-VDB projection surfaces:

```text
KVPS
    uses genotype context when known pathogenicity evidence attaches to
    an observed variant.

PGERS
    summarizes genotype-aware patient-gene evidence rollups without
    performing inheritance reasoning.

CUES
    exposes genotype-related conflict, ambiguity, missingness, and uncertainty.

OACS
    determines whether absence or no-call states are interpretable.

PAPS
    may combine phenotype-prior context with genotype-readiness context
    downstream through RDGP.

RMCS
    tracks whether GIRS was emitted under current corpus and method policy.
```

GIRS should be included in TEP-VDB v1 because known pathogenicity evidence and patient-gene rollups are much less useful to RDGP when genotype context is absent, hidden, or uninterpretable.

---

## 3. Relationship to Mathematical Formalism

Under the VDB mathematical formalism, GIRS is a projection surface over sample-specific variant observations and associated genotype-bearing evidence.

Let:

```text
C
    declared VDB corpus generation

A_C
    corpus-indexed Assertion Record set

T_C
    typed evidence topology derived from A_C

M_GIRS
    genotype membership operator attaching genotype-bearing source evidence
    to sample-specific variant observations

P_GIRS
    genotype projection policy, including source-field, normalization,
    quality, phase, ploidy, readiness, and labeling rules

Ω_GIRS
    optional opportunity/callability structure used when absence, no-call,
    or non-observation states are interpreted
```

Then:

```text
S_GIRS = F_GIRS(T_C, M_GIRS, P_GIRS)
```

When absence, no-call, callability, or opportunity context is required:

```text
S_GIRS = F_GIRS(T_C, M_GIRS, Ω_GIRS, P_GIRS)
```

The required traceability invariant is:

```text
Every GIRS genotype state must trace to a source genotype field, source
record, source Assertion Record, or explicit missing/unavailable state.
```

GIRS is not a score. It is not an inheritance inference. It is a traceable projection surface that makes genotype evidence state available for downstream reasoning.

---

## 4. Core Doctrine

GIRS is governed by the following doctrine:

```text
GIRS does not perform inheritance reasoning.

GIRS exposes genotype observation structure, quality context, phasing context,
ploidy context, and readiness/limitation states so RDGP can reason about
inheritance models downstream.
```

Therefore:

```text
genotype readiness
    ≠ inheritance conclusion

heterozygous-like state
    ≠ dominant model satisfied

two heterozygous-like variants
    ≠ compound heterozygosity

homozygous-alt-like state
    ≠ recessive diagnosis

no-call
    ≠ absence

missing genotype field
    ≠ homozygous reference
```

GIRS is intentionally conservative. It creates a safer substrate for RDGP by separating raw genotype evidence, normalized call-state structure, and inheritance-readiness state.

---

## 5. Scientific Question

GIRS answers the following VDB-level question:

```text
For each sample-specific variant observation, what genotype/call evidence is
available, what structural state does it support under declared policy, and
what limitations must downstream inheritance reasoning know?
```

GIRS does not answer:

```text
Is this variant causal?
Is this disease dominant?
Is this disease recessive?
Is this variant de novo?
Are these variants in trans?
Is this patient compound heterozygous?
Is this variant clinically actionable?
Is this genotype diagnostic?
```

Those questions belong downstream, primarily to RDGP or future inheritance-specific reasoning systems.

---

## 6. What GIRS Is

GIRS is:

```text
a genotype observation projection surface

a genotype-readiness context surface

a source-traceable representation of genotype-bearing fields

a normalized structural call-state surface

a quality/depth/phase/ploidy limitation surface

an RDGP input surface

a TEP-VDB daughter projection surface
```

GIRS may expose:

```text
raw genotype fields

normalized genotype-like structural states

genotype quality context

read depth context

allelic depth or balance context

filter state

phase state

phase-set availability

multi-allelic state

no-call or partial-no-call state

declared ploidy context

sex chromosome or mitochondrial context when available

inheritance-readiness labels

readiness limitations

traceability references
```

---

## 7. What GIRS Is Not

GIRS is not:

```text
an inheritance model

an inheritance result

a causal variant classifier

a disease-model evaluator

a compound-heterozygosity caller

a de novo caller

a segregation analysis

a carrier-status surface

a mitochondrial diagnosis surface

an ACMG/AMP interpretation module

a clinical actionability surface

an RDGP score

a replacement for raw genotype traceability
```

GIRS must not emit downstream reasoning conclusions.

---

## 8. Core Surface Unit

The primary GIRS unit is:

```text
sample_variant_observation_id × genotype_observation_id
```

When genotype observations are not yet represented as first-class objects, the fallback conceptual unit is:

```text
sample_variant_observation_id × genotype_context
```

The core object is not a gene, disease, inheritance model, ClinVar assertion, or patient-gene score.

It is:

```text
a specific variant observation in a specific sample with a specific genotype
or genotype-like call state.
```

This protects VDB's distinction among:

```text
coordinate identity
variant entity
sample-specific variant observation
genotype observation
gene projection
patient-gene rollup
downstream inheritance reasoning
```

These identities must remain distinct.

## Identifier Naming Convention

Within GIRS, the primary VDB identity for a sample-specific observed variant is:

```text
sample_variant_observation_id
```

This identifier should be used consistently in GIRS outputs, validation rules,
traceability references, and downstream surface references.

Source-native or producer-side variant rows should be referenced using explicit
source fields such as:

```text
source_variant_record_ref
source_genotype_record_ref
source_assertion_refs
source_artifact_id
```

GIRS should not use an ambiguous `variant_observation_id` field when the intended
object is the VDB sample-specific observation. This prevents collapse among:

```text
source variant record
coordinate variant identity
sample-specific variant observation
genotype observation
projection membership
downstream inheritance reasoning object
```

---

## 9. Source Substrates

GIRS may consume the following source substrates from VDB topology and TEP-VDB shared substrates.

### 9.1 Sample-Specific Variant Observations

Required when available:

```text
sample_id
run_id
assay_type
sample_variant_observation_id
coordinate_variant_handle
reference_build
contig
position or interval
reference allele
alternate allele
source_variant_record_ref
source Assertion Record references
```

The `sample_variant_observation_id` is the primary VDB identity for the observed
variant in a specific sample. Producer-native records remain recoverable through
source references and must not replace the VDB observation identity.

### 9.2 Genotype Fields

Producer-emitted genotype fields may include:

```text
GT
AD
DP
GQ
PL
PS
PGT
PID
FT
filter
call status
allelic balance if emitted
heteroplasmy fraction if emitted
source genotype field references
```

GIRS should preserve raw fields by reference or value when feasible.

### 9.2.1 Source FORMAT Schema Context

Because genotype FORMAT fields vary by caller, producer, and pipeline stage,
GIRS should preserve source FORMAT schema context when available.

Recommended fields include:

```text
source_format_schema_ref
source_format_field_set
source_format_field_presence_state
source_format_field_missingness_state
source_format_parser_version
```

These fields allow GIRS, CUES, RMCS, and validation systems to distinguish:

```text
field absent because unsupported by source
field absent because not emitted
field present but value missing
field present but no-call
field present but filtered
field present and usable under declared policy
```

FORMAT schema context must remain traceable to producer records, source artifacts,
or explicit unavailable/not-evaluated states.

### 9.3 Quality and Filter Context

Potential fields:

```text
variant quality
genotype quality
read depth
allelic depth
filter status
call confidence
low-confidence flag
source QC state
pipeline-stage quality label
```

### 9.4 Phase Context

Potential fields:

```text
phased / unphased GT representation
phase set
phase-set identifier
physical or statistical phase metadata when emitted
phase confidence when emitted
phase missingness
```

GIRS exposes phasing availability and limitations. It does not infer cis/trans.

### 9.5 Ploidy and Chromosome Context

Potential fields:

```text
declared ploidy
ploidy source
contig class
autosomal context
sex chromosome context
mitochondrial context
haploid-like context
unknown ploidy context
```

GIRS may expose declared context. It must not silently infer sex-specific inheritance implications.

### 9.6 Opportunity / Callability Context

GIRS may reference OACS when no-call, missingness, absence, or negative evidence could be interpreted.

Potential fields:

```text
callable state
not-callable state
not-assayed state
low-confidence state
filtered state
unknown opportunity state
opportunity policy ID
OACS surface reference
```

### 9.7 Genotype-to-Variant Relationship Context

When VDB has constructed first-class genotype-to-variant relationships, GIRS
should consume or reference those relationships rather than requiring downstream
systems to reconstruct allele-index logic from raw genotype fields.

Recommended relationship context fields include:

```text
genotype_variant_relationship_id
genotype_observation_id
sample_variant_observation_id
relationship_type
relationship_state
relationship_derivation_policy_id
allele_index when applicable
source_alt_allele when applicable
variant_identity_id when available
sample_variant_observation_id when resolved
normalization_state
ambiguity_state
lossiness_state
identity_registration_state
allele_depth when available
allele_depth_state when available
relationship_traceability_refs
```

Recommended relationship states include:

```text
direct_source_biallelic
resolved_from_multiallelic_record
brokered_with_normalization
resolved_from_split_normalized_record
ambiguous_requires_review
unresolved_missing_variant_identity
unresolved_symbolic_alt
unresolved_spanning_deletion
spanning_deletion_context_required
unresolved_malformed_gt
unresolved_allele_index_out_of_range
unresolved_normalization_ambiguous
unresolved_policy_not_available
not_evaluated
```

GIRS may expose these relationship states as inheritance-readiness context.

GIRS must not convert relationship readiness into inheritance interpretation.

For example:

```text
resolved_from_multiallelic_record
```

may indicate that the allele-specific genotype-to-variant relationship is usable
under VDB brokerage policy, but it does not mean:

```text
direct_source_biallelic
compound heterozygosity
biallelic model satisfied
inheritance mode supported
diagnosis
```

CUES should index ambiguous, unresolved, unsupported, or traceability-limited
relationship states. RMCS should track the currency of genotype relationship
policies, allele-index mapping policies, relationship builders, and associated
validation receipts.

---

## 10. Three-Level Genotype Representation

GIRS should distinguish three layers of genotype representation.

### 10.1 Raw Genotype Context

Raw genotype context preserves producer-emitted or producer-derived genotype fields.

Examples:

```text
GT_raw
AD_raw
DP_raw
GQ_raw
PL_raw
PS_raw
PGT_raw
PID_raw
FT_raw
source_genotype_field_reference
source_record_reference
```

Raw genotype context must remain reconstructable.

### 10.2 Normalized Structural Call State

Normalized structural call state provides conservative, implementation-stable labels for genotype shape.

Recommended v1 values:

```text
heterozygous_like
homozygous_alt_like
homozygous_ref_like
hemizygous_like
multi_alt_like
reference_like
alternate_present_like
no_call
partial_no_call
uncertain_call
not_reported
not_applicable
unsupported
```

These labels describe genotype-call structure.

They are not inheritance claims.

### 10.3 Inheritance-Readiness State

Inheritance-readiness state describes whether RDGP can safely use the genotype context for downstream inheritance reasoning.

Recommended v1 values:

```text
inheritance_ready
inheritance_ready_with_note
inheritance_limited_low_quality
inheritance_limited_no_call
inheritance_limited_partial_no_call
inheritance_limited_missing_depth
inheritance_limited_missing_quality
inheritance_limited_missing_phase
inheritance_limited_unknown_ploidy
inheritance_limited_multiallelic
inheritance_limited_ambiguous_identity
inheritance_limited_missing_genotype_context
inheritance_not_evaluated
inheritance_not_applicable
unsupported
```

A readiness state is not an inheritance result.

---

## 11. Projection Policy

GIRS must declare a genotype projection policy.

A minimal `P_GIRS` should include:

```text
girs_projection_policy_id
girs_projection_policy_version
genotype_projection_policy_id when distinct from girs_projection_policy_id
genotype_projection_policy_version when distinct from girs_projection_policy_version
source genotype field policy
source FORMAT schema policy
raw field preservation policy
normalized genotype-state policy
quality-state policy
depth-state policy
phase-state policy
ploidy-context policy
mitochondrial-context policy when applicable
multiallelic-context policy
no-call and missingness policy
OACS reference policy
CUES reference policy
RMCS reference policy
readiness-label policy
anti-overclaim policy
traceability policy
```

The projection policy must specify how raw fields are interpreted into structural labels.

The policy must also specify which fields are required for each readiness label.

If `girs_projection_policy_id` and `genotype_projection_policy_id` are the same
identifier in a given implementation, the policy receipt should state that GIRS
is the governing genotype projection policy. If they are distinct, the
relationship between the surface-level GIRS policy and the genotype-specific
normalization policy must be explicit and traceable.

---

## 12. Recommended v1 Label Sets

### 12.1 Genotype Context Availability

```text
genotype_context_available
genotype_context_available_with_note
genotype_context_missing
genotype_context_not_reported
genotype_context_not_applicable
genotype_context_unsupported
genotype_context_not_evaluated
```

### 12.2 Depth Context State

```text
depth_context_available
depth_context_missing
depth_context_low
depth_context_sufficient_under_policy
depth_context_not_reported
depth_context_not_applicable
depth_context_not_evaluated
```

### 12.3 Quality Context State

```text
quality_context_available
quality_context_low_confidence
quality_context_pass_under_policy
quality_context_filtered
quality_context_missing
quality_context_not_reported
quality_context_not_applicable
quality_context_not_evaluated
```

### 12.4 Phase Context State

```text
phase_context_available
phase_context_missing
phase_context_unphased
phase_context_not_reported
phase_context_not_applicable
phase_context_conflicting
phase_context_not_evaluated
```

### 12.5 Ploidy Context State

```text
ploidy_context_declared
ploidy_context_missing
ploidy_context_inferred_by_source
ploidy_context_unknown
ploidy_context_not_applicable
ploidy_context_conflicting
ploidy_context_not_evaluated
```

### 12.6 Genotype Conflict State

```text
no_genotype_conflict_detected
genotype_conflict_visible
genotype_quality_conflict_visible
phase_conflict_visible
ploidy_conflict_visible
source_field_conflict_visible
genotype_conflict_not_evaluated
```

### 12.7 Multiallelic Context State

```text
multiallelic_context_absent
multiallelic_context_present
multiallelic_context_simplified_under_policy
multiallelic_context_unsupported
multiallelic_context_not_evaluated
```

Multiallelic context should remain explicit because genotype structure,
allelic depth, genotype likelihoods, and normalized call states may be ambiguous
or lossy at multiallelic sites.

GIRS must not silently simplify multiallelic genotype context into clean
biallelic heterozygous-like or homozygous-like states unless the declared
projection policy permits that simplification and records the associated
lossiness.

---

## 13. Surface Outputs

GIRS should emit two logical output surfaces.

### 13.1 Genotype Observation Membership Surface

One row per:

```text
sample_variant_observation_id × genotype_observation_id
```

Recommended conceptual fields:

```text
girs_membership_id
girs_surface_id
girs_surface_generation_id
corpus_generation_id
girs_projection_policy_id
genotype_projection_policy_id

sample_id
run_id
assay_type
sample_variant_observation_id
genotype_observation_id
coordinate_variant_handle
reference_build
genotype_variant_relationship_id when applicable
relationship_type when applicable
relationship_state when applicable
relationship_derivation_policy_id when applicable
allele_index when applicable
source_alt_allele when applicable
normalization_state when applicable
ambiguity_state when applicable
lossiness_state when applicable
identity_registration_state when applicable
allele_depth when applicable
allele_depth_state when applicable
contig
position_or_interval
reference_allele
alternate_allele

source_genotype_record_ref
source_variant_record_ref
source_assertion_refs
registration_unit_id
source_package_id
source_artifact_id

source_format_schema_ref
source_format_field_set
source_format_field_presence_state
source_format_parser_version

GT_raw
AD_raw
DP_raw
GQ_raw
PL_raw
PS_raw
PGT_raw
PID_raw
FT_raw

filter_state
quality_context_state
depth_context_state
phase_context_state
ploidy_context_state
multiallelic_context_state

normalized_genotype_state
genotype_context_availability
genotype_conflict_state

oacs_surface_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable

traceability_refs
validation_status
anti_overclaim_label
```

This output preserves auditability, source reconstruction, genotype FORMAT
context, and governance-surface references.

### 13.2 Genotype Readiness Summary Surface

One row per:

```text
sample_variant_observation_id
```

Optional derived rollups may also be emitted for:

```text
sample_id × projected_gene_target_id
```

when PGERS requires genotype-summary context.

Recommended conceptual fields:

```text
girs_summary_id
girs_surface_id
girs_surface_generation_id
corpus_generation_id
girs_projection_policy_id
genotype_projection_policy_id

sample_id
run_id
sample_variant_observation_id
coordinate_variant_handle

genotype_context_available
normalized_genotype_state
inheritance_readiness_label
readiness_limitation
genotype_variant_relationship_state_summary
genotype_variant_relationship_ready_count
genotype_variant_relationship_unresolved_count
genotype_variant_relationship_ambiguous_count
multiallelic_relationship_resolved_count
multiallelic_relationship_unresolved_count
multiallelic_relationship_not_evaluated_count

depth_context_state
quality_context_state
phase_context_state
ploidy_context_state
multiallelic_context_state
no_call_state
mitochondrial_context_state when applicable

genotype_observation_refs
source_assertion_refs
oacs_surface_ref when applicable
cues_event_refs when applicable
rmcs_currency_refs when applicable

traceability_refs
validation_status
anti_overclaim_label
```

The readiness summary must remain reconstructable from the genotype observation
membership surface and declared projection-policy receipts.

---

## 14. Relationship to KVPS

KVPS exposes known pathogenicity evidence attached to sample-specific observed variants.

GIRS provides the genotype context that makes those variant observations usable for downstream RDGP reasoning.

KVPS may reference GIRS fields such as:

```text
genotype_observation_id
normalized_genotype_state
inheritance_readiness_label
quality_context_state
depth_context_state
phase_context_state
ploidy_context_state
```

But KVPS must not perform inheritance reasoning.

Example boundary:

```text
KVPS may expose:
    known pathogenicity evidence attaches to an observed variant.

GIRS may expose:
    the variant observation is heterozygous-like with sufficient depth
    under declared policy.

RDGP may reason:
    this evidence contributes to a dominant-model hypothesis.
```

---

## 15. Relationship to PGERS

PGERS rolls patient evidence onto gene, locus, or gene-adjacent targets.

PGERS may consume GIRS summaries to expose genotype-aware counts:

```text
heterozygous_like_variant_count
homozygous_alt_like_variant_count
genotype_context_available_count
genotype_context_limited_count
phase_context_available_count
quality_limited_genotype_count
```

PGERS must not convert these into inheritance conclusions.

GIRS owns genotype-readiness context.

PGERS owns patient-gene rollup context.

RDGP owns inheritance reasoning.

---

## 16. Relationship to OACS

GIRS and OACS are complementary.

```text
GIRS:
    What genotype/call state was emitted for this sample-specific variant
    observation?

OACS:
    Was the corresponding coordinate, region, feature, or locus observable
    enough for absence or no-call interpretation?
```

GIRS must not treat missing genotype evidence as absence unless OACS declares the opportunity basis required for that interpretation.

Examples:

```text
missing genotype field
    ≠ variant absent

no-call
    ≠ reference genotype

filtered call
    ≠ no biological variant

not assayed
    ≠ negative evidence
```

---

## 17. Relationship to CUES

CUES may expose genotype-related conflict and uncertainty across surfaces.

GIRS should preserve enough state for CUES to report:

```text
genotype conflict
quality conflict
phase conflict
ploidy conflict
source-field conflict
identity/genotype mismatch
low-confidence genotype used by downstream surfaces
```

GIRS may include local conflict labels, but CUES should own package-level conflict/uncertainty synthesis.

---

## 18. Relationship to RMCS

RMCS tracks whether TEP-VDB surfaces are current relative to evidence corpus, projection policies, and downstream reasoning methods.

GIRS should expose:

```text
girs_surface_generation_id
corpus_generation_id
projection_policy_id
projection_policy_version
source genotype extraction version
validation receipt reference
```

RMCS can then determine whether genotype-readiness surfaces are stale, current, or unknown relative to the active TEP-VDB generation.

---

## 19. Relationship to Mitochondrial Evidence

GIRS should be compatible with mitochondrial genotype contexts.

If available, GIRS may expose:

```text
mitochondrial_contig_context
mt_depth_context
heteroplasmy_fraction
heteroplasmy_fraction_source
heteroplasmy_state_label if producer-safe
mt_call_quality
mt_readiness_limitation
```

But GIRS must not conclude:

```text
maternal inheritance supported
pathogenic heteroplasmy threshold exceeded
mitochondrial disease diagnosed
```

Those remain RDGP or future specialized reasoning responsibilities.

---

## 20. Relationship to Sex Chromosome Evidence

GIRS may preserve sex chromosome and ploidy context when declared.

Potential states:

```text
autosomal_context
x_chromosome_context
y_chromosome_context
pseudoautosomal_context
sex_chromosome_context_unknown
declared_ploidy_context_available
declared_ploidy_context_missing
```

GIRS must not silently infer:

```text
X-linked model satisfied
Y-linked model satisfied
hemizygous pathogenic diagnosis
```

When sex, ploidy, or pseudoautosomal context is absent or uncertain, GIRS should expose limitation states rather than inferred inheritance claims.

---

## 21. RDGP Consumption Role

RDGP may use GIRS to evaluate:

```text
dominant compatibility
recessive compatibility
biallelic candidate structure
compound heterozygosity
de novo evidence if family data eventually exist
X-linked or sex-chromosome models
mitochondrial models
carrier-state implications
genotype confidence
variant support strength
```

GIRS does not perform these evaluations.

The boundary is:

```text
GIRS exposes genotype readiness.
RDGP evaluates inheritance models.
```

GIRS helps RDGP avoid unsafe assumptions about missing genotype data, low-quality calls, phasing limitations, ploidy limitations, multi-allelic complexity, and no-call states.

---

## 22. Validation Requirements

GIRS validation should confirm:

```text
every emitted genotype state has traceability
raw genotype fields are preserved by value or reconstructable reference
normalized genotype states are declared under policy
normalized genotype states are consistent with raw GT under declared policy
unsupported or ambiguous raw genotype patterns are not coerced into clean
heterozygous-like or homozygous-like states
multiallelic genotype context is explicit when present or not evaluated
source FORMAT schema context is preserved or explicitly unavailable
readiness labels are declared under policy
missing genotype fields are represented explicitly
no-call and partial-no-call states are distinguishable
quality context is visible when available
depth context is visible when available
phase context is visible when available
ploidy context is visible when available
ambiguous or unsupported states are explicit
OACS references exist when absence/no-call interpretation is exposed
GIRS does not emit inheritance-model conclusions
membership-level rows support summary-level reconstruction
surface IDs, GIRS projection policy IDs, and genotype projection policy IDs are present or explicitly declared equivalent
anti-overclaim labels are present
```

Validation should also check that deterministic reruns over fixed inputs produce stable GIRS outputs.

---

## 23. Anti-Overclaim Labels

Recommended GIRS anti-overclaim labels:

```text
genotype_structure_only

inheritance_not_evaluated

inheritance_readiness_only

not_diagnostic

not_causal

not_clinical_actionability

not_compound_heterozygosity_call

not_de_novo_call

not_segregation_analysis

absence_not_inferred_without_opportunity

ploidy_not_inferred_without_declared_context

phase_not_interpreted
```

Every GIRS row should carry an appropriate anti-overclaim label or reference to surface-level anti-overclaim policy.

---

## 24. Invalid GIRS Patterns

The following patterns are prohibited.

```text
raw GT treated as an inheritance conclusion

heterozygous-like state treated as dominant-model evidence by VDB

two heterozygous-like variants treated as compound heterozygosity by VDB

homozygous-alt-like state treated as recessive diagnosis by VDB

hemizygous-like state treated as X-linked diagnosis by VDB

no-call treated as absence

missing genotype field treated as homozygous reference

multiallelic genotype context silently simplified into biallelic genotype state
without declared policy and lossiness

low-quality genotype hidden from RDGP

phase missingness ignored

ploidy context inferred silently

mitochondrial heteroplasmy interpreted as pathogenic threshold

genotype-readiness label treated as RDGP score

GIRS summary replacing source genotype traceability

RDGP reasoning output written back into GIRS instead of re-entering VDB
as new Assertion Records
```

Any implementation that performs one of these actions violates the GIRS design.

---

## 25. v1 Minimum Viable Surface

A minimum viable GIRS v1 should include:

```text
Input substrates:
    VAP sample-specific variant observations
    genotype fields if present
    source record references
    quality/filter/depth fields if present
    coordinate identity
    sample/run identity

Required outputs:
    genotype observation membership surface
    genotype readiness summary surface

Required identifiers:
    girs_surface_id
    girs_membership_id
    girs_summary_id
    corpus_generation_id
    projection_policy_id
    sample_id
    run_id
    sample_variant_observation_id
    genotype_observation_id when available
    genotype_variant_relationship_id when applicable

Required states:
    genotype_context_availability
    normalized_genotype_state
    depth_context_state
    quality_context_state
    phase_context_state
    ploidy_context_state
    inheritance_readiness_label
    readiness_limitation
    genotype_conflict_state

Required governance:
    source traceability
    policy traceability
    validation status
    anti-overclaim label
```

GIRS v1 does not require family data, trio support, segregation support, inheritance modeling, or clinical interpretation.

---

## 26. Future Extensions

Future GIRS or GIRS-adjacent surfaces may support:

```text
family-aware genotype readiness

trio availability context

parent-child genotype comparison substrate

segregation-readiness substrate

copy-number genotype state

structural-variant genotype context

phased haplotype block context

compound-heterozygosity candidate substrate

mitochondrial heteroplasmy-specific readiness

sex-chromosome-specific readiness

mosaicism-aware genotype context

long-read phase/read-support context
```

These extensions should remain readiness or substrate surfaces unless and until a downstream reasoning engine emits explicit reasoning assertions.

---

## 27. Non-Goals

GIRS does not define:

```text
RDGP inheritance scoring

dominant/recessive model logic

compound heterozygosity inference

de novo inference

segregation analysis

clinical genotype interpretation

ACMG/AMP classification

variant pathogenicity interpretation

disease diagnosis

clinical actionability

full genotype schema implementation

database DDL

builder code

validator code
```

Those belong to downstream design, implementation, or reasoning documents.

---

## 28. Summary

GIRS is the TEP-VDB projection surface that exposes genotype observation structure and inheritance-readiness context for sample-specific variant observations.

It preserves raw genotype fields, normalized structural call states, depth/quality/phase/ploidy context, missingness states, readiness limitations, traceability, and anti-overclaim boundaries.

GIRS enables RDGP to reason over inheritance models without forcing RDGP to reconstruct genotype evidence from raw producer artifacts and without allowing VDB to become an inheritance reasoning engine.

The governing boundary is:

```text
GIRS exposes genotype readiness.

RDGP evaluates inheritance models.

Scientists and clinicians interpret evaluated evidence.
```

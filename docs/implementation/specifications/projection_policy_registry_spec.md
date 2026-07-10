# Projection Policy Registry Specification

> Status: DEX-VDB implementation specification.
> This document derives from `docs/design/opportunity_space_and_projection_policy_model.md`
> and governs how VDB declares, versions, validates, and references projection
> policies used to emit future TEP-VDB projection surfaces.

## 1. Purpose

This specification defines the VDB Projection Policy Registry.

The registry is the canonical implementation-facing catalog of declared rules
used to transform, group, window, annotate, filter, match, or otherwise relate
one evidence substrate to another during projection-surface construction.

The registry prevents downstream surfaces from silently applying ad hoc joins,
implicit biological assumptions, unversioned window definitions, hidden variant
filters, or undocumented annotation overlays.

In VDB, a projection policy is not biological truth. It is a versioned,
auditable rule that produces projection memberships, annotation memberships,
filter partitions, locus/window definitions, matching sets, null-model inputs,
or emission constraints.

## 2. Scope

This specification applies to policy declarations required for VDB-emitted
TEP-VDB projection surfaces, including but not limited to:

```text
coordinate projection policies
feature projection policies
gene projection policies
phenotype-prior projection policies
region definition policies
window policies
locus-window policies
variant filter policies
annotation overlay policies
background matching policies
candidate interval assembly policies
null model policies
emission policies
```

The registry governs policy declarations and dependencies. It does not define
final projection-surface outputs, burden matrices, or RDGP prioritization logic.

## 3. Non-Goals

This specification does not define:

```text
opportunity-space file formats
projection result schemas
burden matrix schemas
MPLC result schemas
CFBS result schemas
candidate rankings
RDGP scoring logic
builder execution order
formal statistical association claims
```

Opportunity semantics are defined in:

```text
docs/implementation/specifications/opportunity_space_spec.md
```

MPLC and CFBS method-specific output structures should be defined in later
method specifications.

## 4. Core Invariant

The registry preserves this invariant:

```text
policy ≠ projection membership ≠ geometry ≠ interpretation ≠ reasoning
```

A policy is a declared rule.

A projection membership is the application of that rule to a source object.

Geometry is a numerical structure derived from evidence, memberships, and
opportunity-aware denominators.

Interpretation assigns biological or clinical meaning.

Reasoning ranks, prioritizes, or concludes.

VDB may declare and apply policies, but it must not collapse those policies into
biological truth or RDGP conclusions.

## 5. Relationship to Opportunity Space

The Projection Policy Registry references opportunity models, but it does not
redefine opportunity states or denominator semantics.

Any policy that produces or supports burden rates, expected burden,
observed/expected ratios, empirical-null statistics, or burden-ready projection
surfaces must declare one of the following:

```text
opportunity_model_id
opportunity_unmodeled with burden_readiness_status != burden_ready
```

A policy must not imply burden readiness unless an admissible opportunity basis
exists under `opportunity_space_spec.md`.

Examples:

```text
valid:
    policy_id: fixed_20kb_windows_v1
    opportunity_requirement: required_for_burden_surface
    opportunity_model_id: opportunity_model_assay_scope_approximation_v1
    burden_readiness_status: exploratory_only

valid:
    policy_id: coordinate_preservation_only_v1
    opportunity_requirement: not_required
    burden_readiness_status: not_applicable

invalid:
    policy_id: burden_rate_surface_v1
    opportunity_requirement: required_for_burden_surface
    opportunity_model_id: null
    burden_readiness_status: burden_ready
```

Observed variant locations must never be used as a denominator policy.

## 6. Relationship to Evidence Topology and Convergence Geometry

Evidence Topology organizes typed relationships among preserved evidence handles.
Projection policies declare how evidence can be mapped, grouped, annotated, or
partitioned for later geometry and projection-surface emission.

The conceptual chain is:

```text
coordinate evidence
    → topology
        → declared projection policies
            → projection memberships
                → opportunity-aware geometry
                    → reason-ready TEP-VDB
                        → RDGP
```

Implementation may materialize projection memberships before numerical geometry,
because burden matrices, locus/window memberships, and post hoc annotations
depend on declared policies. The required invariant is that every policy-driven
membership is versioned, traceable, and bounded by declared lossiness and
anti-overclaim constraints.

## 7. Required Logical Artifacts

The registry consists of the following logical artifacts:

```text
projection_policy_registry_manifest
projection_policy_index
projection_policy_definition
projection_policy_dependency_index
projection_policy_validation_receipts
```

Physical file names may be finalized by later TEP-VDB schema documents, but the
logical artifacts and required semantics defined here are normative.

## 8. Artifact: projection_policy_registry_manifest

The manifest identifies the registry build.

Required fields:

```text
projection_policy_registry_id
registry_version
registry_build_id
registry_created_at
governing_spec_version
source_corpus_id
genome_build
status
description
```

Recommended fields:

```text
created_by
repository_name
repository_commit
input_policy_sources
validation_summary_status
payload_json
```

Controlled `status` values:

```text
draft
active
deprecated
superseded
invalid
```

## 9. Artifact: projection_policy_index

The policy index is a compact list of registered policies.

Required fields:

```text
policy_id
policy_version
policy_name
policy_class
policy_family
policy_status
source_substrate
target_substrate
is_lossy
requires_opportunity_model
requires_random_seed
implementation_status
```

Recommended fields:

```text
registry_build_id
genome_build
method_scope
applicability_scope
short_description
replacement_policy_id
payload_json
```

Controlled `policy_status` values:

```text
draft
active
deprecated
superseded
invalid
```

Controlled `implementation_status` values:

```text
design_only
spec_declared
implemented
validated
deprecated
```

## 10. Artifact: projection_policy_definition

The policy definition records the rule itself.

Required fields:

```text
policy_id
policy_version
policy_class
policy_family
source_substrate
target_substrate
rule_summary
rule_parameters_json
controlled_vocabulary_id
genome_build
coordinate_system
reference_context_requirement
applicability_scope
exclusion_rules_json
lossiness_state
reversibility_state
traceability_requirement
opportunity_requirement
anti_overclaim_requirement
```

Recommended fields:

```text
method_scope
random_seed_requirement
external_reference_id
external_reference_version
source_artifact_requirement
output_membership_kind
validation_profile_id
payload_json
```

### Rule parameters

`rule_parameters_json` should capture all parameters required to reproduce the
policy behavior. Examples include:

```text
window_size_bp
window_stride_bp
locus_padding_bp
included_chromosomes
excluded_chromosomes
variant_classes
frequency_threshold
matching_features
minimum_callable_bases
merge_distance_bp
random_seed
number_of_null_draws
```

### External references

If a policy depends on an external method, ontology, annotation release,
software package, or resource, the policy definition must use versioned
reference fields rather than informal raw URLs embedded in design prose.

Required when applicable:

```text
external_reference_id
external_reference_version
external_reference_role
```

## 11. Artifact: projection_policy_dependency_index

Projection surfaces often depend on policy stacks rather than single policies.
The dependency index records these relationships.

Required fields:

```text
policy_id
policy_version
dependency_policy_id
dependency_policy_version
dependency_kind
required_status
```

Recommended fields:

```text
dependency_order
dependency_reason
validation_rule_id
payload_json
```

Controlled `dependency_kind` values:

```text
requires_opportunity_model
requires_scan_space_policy
requires_window_policy
requires_locus_window_policy
requires_variant_filter_policy
requires_annotation_policy
requires_background_matching_policy
requires_null_model_policy
requires_emission_policy
requires_reference_context
requires_external_resource
```

Controlled `required_status` values:

```text
required
optional
forbidden
conditional
```

## 12. Artifact: projection_policy_validation_receipts

Validation receipts record whether registry policies satisfy the requirements of
this specification.

Required fields:

```text
policy_id
policy_version
validation_check
validation_status
severity
message
```

Recommended fields:

```text
validation_profile_id
validator_version
checked_at
source_artifact
remediation_hint
payload_json
```

Controlled `validation_status` values:

```text
pass
warn
fail
not_applicable
not_tested
```

Controlled `severity` values:

```text
info
warning
error
fatal
```

## 13. Controlled Vocabularies

### policy_class

Allowed values:

```text
coordinate_projection_policy
feature_projection_policy
gene_projection_policy
phenotype_prior_projection_policy
region_definition_policy
window_policy
locus_window_policy
variant_filter_policy
annotation_overlay_policy
background_matching_policy
candidate_interval_assembly_policy
null_model_policy
emission_policy
```

### source_substrate and target_substrate

Allowed values include:

```text
coordinate_observation
sample_variant_observation
feature_declaration
gene_annotation
phenotype_prior
opportunity_region
scan_window
locus_window
candidate_interval
variant_filter_partition
annotation_overlay
burden_matrix
null_draw_manifest
projection_surface
tep_vdb_manifest
```

Derived schemas may extend this vocabulary if the extension is documented,
versioned, and validated.

### lossiness_state

Allowed values:

```text
lossless
bounded_lossy
lossy
unknown_lossiness
not_applicable
```

### reversibility_state

Allowed values:

```text
fully_reversible
coordinate_traceable
partially_reversible
not_reversible
unknown
```

`coordinate_traceable` means the projection result may not be fully reversible to
all source fields, but it retains enough traceability to recover the underlying
coordinate evidence used to produce the membership.

### traceability_requirement

Allowed values:

```text
coordinate_trace_required
source_identity_trace_required
annotation_trace_required
gsc_prior_trace_required
not_required
```

### opportunity_requirement

Allowed values:

```text
required_for_burden_surface
required_for_null_model
recommended
not_required
forbidden
```

### anti_overclaim_requirement

Allowed values:

```text
exploratory_label_required
posthoc_annotation_label_required
burden_readiness_label_required
not_required
```

## 14. Policy Dependency Rules

Policies must declare dependencies when their behavior depends on other policy
rules or external resources.

Examples:

```text
fixed_20kb_windows_v1
    requires_scan_space_policy
    requires_reference_context

matched_background_locus_policy_v1
    requires_locus_window_policy
    requires_opportunity_model
    requires_variant_filter_policy

matched_genomic_opportunity_null_v1
    requires_window_policy
    requires_opportunity_model
    requires_variant_filter_policy
    requires_random_seed

nearest_gene_posthoc_annotation_v1
    requires_annotation_policy
    requires_reference_context
```

A policy stack must fail validation if a required dependency is absent,
invalid, deprecated without override, or version-incompatible.

## 15. Lossiness and Reversibility Rules

Every policy must declare both `lossiness_state` and `reversibility_state`.

Rules:

```text
1. A lossy policy must declare what information is lost.
2. A partially reversible policy must declare the minimum reversible handle.
3. A burden-relevant projection must be at least coordinate_traceable.
4. A projection used by RDGP must retain source-coordinate traceability unless
   explicitly labeled as annotation-only and not burden-relevant.
5. Unknown lossiness is allowed only for draft policies and must not be used in
   burden-ready surfaces.
```

Examples:

```text
coordinate → fixed window:
    lossiness_state: bounded_lossy
    reversibility_state: coordinate_traceable

coordinate → exact coordinate identity:
    lossiness_state: lossless
    reversibility_state: fully_reversible

gene → phenotype-scoped GSC prior:
    lossiness_state: bounded_lossy
    reversibility_state: partially_reversible
```

## 16. Method-Specific Guardrails

### 16.1 MPLC guardrails

MPLC is prior-informed. It may use GSC priors to define target loci, but that use
must be policy-declared and phenotype-scope aware.

MPLC policy stacks should declare:

```text
target_locus_policy_id
background_matching_policy_id
window_policy_id
variant_filter_policy_id
opportunity_model_id
null_model_id
```

MPLC validation must check:

```text
1. GSC target-locus policy includes phenotype_scope.
2. GSC target-locus policy includes gsc_release_id or equivalent source trace.
3. GSC target-locus policy includes semantic_prior_id where available.
4. Background loci are matched non-prior loci, not asserted non-disease loci.
5. Background loci overlapping target windows are excluded or explicitly marked.
6. Matching features are declared and versioned.
7. Burden and recurrence statistics use sample-specific coordinate observations,
   not duplicated annotation rows.
8. Results are labeled exploratory and not disease-associated, causal, or
   diagnostic.
```

### 16.2 CFBS guardrails

CFBS is coordinate-first. Biology must not choose candidate windows before the
coordinate scan.

CFBS scan-window policies may depend on:

```text
genome_build
reference_context
scan_space_policy_id
window_policy_id
opportunity_model_id
variant_filter_policy_id
variant_class_partition
```

CFBS scan-window policies must not depend on:

```text
gsc_prior_overlay
nearest_gene_annotation
known_disease_gene_annotation
posthoc_annotation_policy
RDGP ranking
```

CFBS validation must check:

```text
1. Scan windows are defined before post hoc GSC/gene annotation.
2. GSC priors are used only as post hoc annotations, not as scan-space selectors.
3. Candidate interval assembly policy is declared and versioned.
4. Null model policy preserves patient-level burden where required.
5. Variant-class partitions are preserved where possible.
6. Results are labeled exploratory coordinate hotspot candidates, not
   disease-associated or pathogenic regions.
```

## 17. Example Policy IDs

The following examples are schema seeds and design anchors, not required final
field contracts or implemented builders:

```text
gene_body_plus_10kb_v1
fixed_5kb_windows_v1
fixed_10kb_windows_v1
fixed_20kb_windows_v1
fixed_50kb_windows_v1
splice_proximal_interval_v1
nearest_gene_posthoc_annotation_v1
gsc_epilepsy_prior_overlay_v1
gsc_mitochondrial_prior_overlay_v1
rare_variant_filter_v1
ultra_rare_variant_filter_v1
matched_background_locus_policy_v1
candidate_interval_merge_adjacent_v1
matched_genomic_opportunity_null_v1
matched_prior_locus_null_v1
```

Final policy IDs should be stabilized in implementation specs and validation
profiles before builder code depends on them.

## 18. Validation Rules

Registry validators should check:

```text
1. policy_id and policy_version are present.
2. policy_id + policy_version is unique within the registry.
3. policy_class is in the controlled vocabulary.
4. source_substrate and target_substrate are declared.
5. rule_summary is present.
6. rule_parameters_json is valid JSON when required.
7. lossiness_state is declared.
8. reversibility_state is declared.
9. traceability_requirement is declared.
10. opportunity_requirement is declared.
11. burden-relevant policies declare opportunity_model_id or an explicit
    opportunity_unmodeled state with non-burden-ready status.
12. required dependencies are present and version-compatible.
13. deprecated policies are not used without explicit override.
14. external references are versioned when present.
15. CFBS scan-window policies do not depend on GSC/gene-prior labels.
16. MPLC target policies are phenotype-scope aware.
17. anti-overclaim requirements are present for exploratory surfaces.
18. unknown lossiness is not used in burden-ready surfaces.
```

## 19. Failure Modes

The registry should prevent or flag the following failure modes:

```text
unversioned projection rule
implicit coordinate-to-gene shortcut
hidden variant filter
untracked window size
untracked locus padding
GSC prior used in CFBS scan-window selection
MPLC background loci treated as non-disease truth
burden surface emitted without opportunity model
lossy projection emitted without lossiness declaration
projection result lacking source-coordinate traceability
external method or annotation release used without version
policy stack uses deprecated dependency silently
exploratory empirical statistic labeled as formal association evidence
```

## 20. Future Extensions

Future registry versions may support:

```text
policy checksums
machine-readable JSON Schema definitions
policy inheritance
policy compatibility matrices
policy packs for demonstration profiles
formal semantic versioning rules
runtime registry loading
policy-driven builder orchestration
```

These extensions should preserve the current invariant: policies declare rules;
projection memberships apply rules; geometry derives numerical structure;
RDGP performs downstream reasoning.

# Projection Surface Validation Plan

> Status: DEX-VDB validation derivation.
> This document defines validation expectations for VDB-emitted TEP-VDB
> projection surfaces intended for RDGP consumption.
> It is not a validator implementation contract, pytest plan, CLI specification,
> or final artifact filename contract.

## 1. Purpose

This document defines the validation plan for VDB projection surfaces emitted as
TEP-VDB products.

Projection surfaces are reason-ready evidence products that carry coordinated
substrates, projection memberships, opportunity context, policy declarations,
method-specific result objects, validation receipts, and traceability sufficient
for RDGP consumption.

The validation goal is not to prove biological truth.

The validation goal is to determine whether a VDB-emitted projection surface is
structurally complete, traceable, opportunity-aware, policy-declared,
anti-overclaim bounded, and safe for RDGP to consume without reconstructing the
underlying VAP/GSC integration.

---

## 2. Scope

This plan applies to VDB-emitted TEP-VDB projection surfaces, including:

```text
MPLC = Matched Prior-Locus Contrast
CFBS = Coordinate-First Burden Scan
future projection-surface methods
```

It covers validation of:

```text
TEP-VDB package structure
source corpus integrity
shared substrate integrity
coordinate and sample-observation identity
opportunity-space declarations
projection-policy declarations
method-surface manifests
method-specific outputs
validation receipts
anti-overclaim labels
RDGP consumption boundaries
```

---

## 3. Non-Goals

This document does not define:

```text
exact validator module names
exact CLI commands
exact pytest module paths
exact output filenames for every artifact
exact TSV or JSON column order
exact builder execution order
exact RDGP importer implementation
RDGP scoring logic
RDGP-TEP return-leg implementation schema
```

Those belong to later implementation plans, system contracts, mini-contracts,
validator specifications, and builder documentation.

---

## 4. Validation Invariant

A projection surface is valid only if RDGP can consume it as a reason-ready
surface without losing:

```text
source traceability
identity boundaries
sample-specific observation identity
opportunity context
projection-policy context
uncertainty state
method-surface provenance
validation receipts
anti-overclaim labels
```

The governing architectural invariant is:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

Validation must reject or block projection surfaces that collapse these layers
into opaque gene, locus, window, or candidate scores.

---

## 5. Validation Levels

Projection-surface validation is organized into four levels.

### Level 1 — Package Validity

Determine whether the TEP-VDB package is structurally complete.

This level asks:

```text
Does the product contain or reference the expected top-level containers?
Are required manifests present?
Are projection surfaces enumerated?
Are validation receipt containers present?
```

### Level 2 — Substrate Validity

Determine whether source corpus, shared substrates, policies, opportunity
objects, and traceability objects are usable.

This level asks:

```text
Are source packages identifiable?
Are coordinate and sample-observation identities preserved?
Are opportunity states declared?
Are projection policies declared?
Can evidence be traced back to source artifacts?
```

### Level 3 — Method-Surface Validity

Determine whether each method room is internally coherent.

This level asks:

```text
Is the MPLC surface coherent as prior-informed matched locus contrast evidence?
Is the CFBS surface coherent as coordinate-first burden scan evidence?
Are method-specific nulls, memberships, matrices, annotations, and results valid?
```

### Level 4 — Interface Safety

Determine whether RDGP can safely consume the projection surface.

This level asks:

```text
Can RDGP consume the product without re-integrating VAP/GSC packages?
Are exploratory results labeled conservatively?
Are burden claims opportunity-supported?
Are method outputs distinguishable from RDGP reasoning outputs?
```

---

## 6. Required Validation Inputs

A validation run should receive or discover the following logical inputs.

```text
tep_vdb_envelope
tep_vdb_manifest
source_tep_index
shared_substrate_index
projection_surface_index
method_surface_manifests
source_traceability_index
validation_receipt_index, if validating an existing emitted package
method-specific projection surface artifacts
```

Validation may also consume repo-local policy/spec references, including:

```text
docs/implementation/specifications/opportunity_space_spec.md
docs/implementation/specifications/projection_policy_registry_spec.md
docs/implementation/schemas/tep_vdb_projection_surface_schema.md
docs/implementation/specifications/mplc_projection_surface_spec.md
docs/implementation/specifications/cfbs_projection_surface_spec.md
docs/interfaces/vdb_rdgp_interface.md
```

Validation should treat these documents as rule sources until executable schemas
or validators supersede them.

---

## 7. Required Validation Outputs

A validation run should emit a validation receipt set.

At minimum, each receipt should include:

```text
validation_receipt_id
tep_vdb_id
projection_surface_id
method_id
validator_id
validator_version
validation_timestamp_utc
input_artifacts
check_id
check_name
check_group
severity
status
message
affected_artifact
affected_record_count
recommendation
```

Receipt output should support both human review and machine filtering.

---

## 8. Package-Level Validation

Package-level validation confirms that the TEP-VDB projection-surface product is
present and internally navigable.

### 8.1 Required Containers

A valid projection-surface TEP-VDB package must contain or reference:

```text
tep_vdb_envelope
tep_vdb_manifest
source_tep_index
shared_substrate_index
projection_surface_index
method_surface_manifests
validation_receipt_index
source_traceability_index
```

### 8.2 Package Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `pkg.envelope.present` | TEP-VDB envelope is present. | BLOCK |
| `pkg.manifest.present` | TEP-VDB manifest is present. | BLOCK |
| `pkg.source_index.present` | Source TEP index is present. | BLOCK |
| `pkg.substrate_index.present` | Shared substrate index is present. | BLOCK |
| `pkg.surface_index.present` | Projection surface index is present. | BLOCK |
| `pkg.method_manifest.present` | Every surface has a method-surface manifest. | BLOCK |
| `pkg.validation_index.present` | Validation receipt index is present or planned for emission. | FAIL |
| `pkg.traceability_index.present` | Source traceability index is present. | BLOCK |

### 8.3 Package-Level Failure Examples

Package-level failures include:

```text
missing envelope
missing source corpus index
missing projection surface index
surface listed without manifest
method surface present but not indexed
traceability index absent
```

Any package-level `BLOCK` failure makes the product unsafe for RDGP consumption.

---

## 9. Source Corpus Validation

Source corpus validation confirms that all contributing producer packages remain
separable, traceable, and internally consistent.

### 9.1 Required Source Corpus Properties

The source corpus must preserve:

```text
source_corpus_id
source_tep_id
producer_family
producer_package_id
producer_run_id or release identity
source_tep_type
sample_id, where applicable
assay_type, where applicable
phenotype_scope, where applicable
genome_build, where applicable
included_status
exclusion_reason, where applicable
source_traceability_id
```

### 9.2 Source Corpus Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `source.corpus_id.present` | Source corpus identity is declared. | BLOCK |
| `source.counts.consistent` | Source counts are internally consistent with indexed source rows. | FAIL |
| `source.producer_family.present` | Every source row declares producer family. | BLOCK |
| `source.package_identity.present` | Every included source preserves package identity. | BLOCK |
| `source.identity_not_collapsed` | VAP, GSC, RSP, and RDGP identities are not collapsed into generic `run_id`. | BLOCK |
| `source.exclusion_reason.present` | Excluded sources declare exclusion reasons. | FAIL |
| `source.genome_build.coherent` | Genome build declarations are coherent for coordinate-bearing sources. | FAIL |
| `source.phenotype_scope.coherent` | Phenotype scopes are declared for GSC prior sources. | FAIL |

### 9.3 Demonstration Profile Checks

When validating a named demonstration profile, profile-specific expectations may
be enforced.

For example, a first epilepsy projection-surface profile may require:

```text
source_tep_count == 14
vap_tep_count == 12
gsc_tep_count == 2
epilepsy GSC source present
mitochondrial GSC source present
expected VAP epilepsy packages present
```

These counts belong to the demonstration profile, not to the generic TEP-VDB
schema.

---

## 10. Shared Substrate Validation

Shared substrate validation confirms that projection surfaces can reference the
same stable evidence substrate without duplicating or corrupting evidence.

### 10.1 Expected Shared Substrate Classes

A TEP-VDB projection product may contain or reference:

```text
coordinate_observations
sample_variant_observations
feature_declarations
gene_annotations
gsc_prior_overlays
opportunity_space
variant_filter_partitions
projection_policy_registry
source_traceability
```

### 10.2 Shared Substrate Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `substrate.index.present` | Shared substrate index is present. | BLOCK |
| `substrate.classes.declared` | Each substrate declares substrate class. | FAIL |
| `substrate.path_or_reference.present` | Each required substrate has path or reference. | FAIL |
| `substrate.row_count.present` | Row counts are declared when available. | WARN |
| `substrate.validation_status.present` | Each substrate declares validation status. | FAIL |
| `substrate.traceability.present` | Each substrate has source traceability. | BLOCK |

### 10.3 Required Substrate Classes for Burden Surfaces

Any burden-relevant projection surface must have access to:

```text
sample_variant_observations
opportunity_space or explicit opportunity_unmodeled declaration
projection_policy_registry
source_traceability
```

Missing `sample_variant_observations` is a `BLOCK` failure for burden-counting
surfaces.

---

## 11. Opportunity-Space Validation

Opportunity-space validation confirms that burden, recurrence, observed/expected,
and empirical-null claims are denominator-aware.

### 11.1 Required Opportunity Properties

Burden-relevant surfaces must declare:

```text
opportunity_model_id
opportunity_model_version
opportunity_basis_kind
opportunity_state
burden_readiness_status
assay_scope_status
callability_status, where available
callable_bases, where applicable
not_callable_bases, where applicable
not_assayed_bases, where applicable
unknown_opportunity_bases, where applicable
```

### 11.2 Opportunity Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `opp.model.present` | Opportunity model ID is present for burden-relevant surfaces. | BLOCK |
| `opp.basis.present` | Opportunity basis kind is declared. | BLOCK |
| `opp.state.present` | Opportunity state is declared. | FAIL |
| `opp.burden_readiness.present` | Burden-readiness status is declared. | BLOCK |
| `opp.unmodeled_not_burden_ready` | `opportunity_unmodeled` is not marked burden-ready. | BLOCK |
| `opp.unknown_not_zero` | Unknown opportunity is not treated as zero burden opportunity. | BLOCK |
| `opp.wes_wgs_not_silently_merged` | WES and WGS opportunity spaces are not silently merged. | FAIL |
| `opp.observed_variants_not_denominator` | Observed variants alone are not used as denominator. | BLOCK |
| `opp.counts.nonnegative` | Opportunity base counts are non-negative. | FAIL |
| `opp.counts.coherent` | Callable/not-callable/not-assayed/unknown counts are internally coherent. | FAIL |

### 11.3 Opportunity Failure Examples

Blocking opportunity failures include:

```text
burden_ready without opportunity_model_id
burden_ready with opportunity_unmodeled
unknown opportunity encoded as zero opportunity
observed variant rows used as denominator
WES capture-limited regions treated as genomewide absence
```

---

## 12. Projection-Policy Validation

Projection-policy validation confirms that derived surfaces declare the rules by
which they were produced.

### 12.1 Required Policy References

Depending on method, a projection surface may require:

```text
projection_policy_registry_id
region_definition_policy_id
window_policy_id
locus_window_policy_id
variant_filter_policy_id
background_matching_policy_id
candidate_interval_assembly_policy_id
null_model_id
posthoc_annotation_policy_id
emission_policy_id
```

### 12.2 Projection-Policy Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `policy.registry.present` | Projection policy registry ID is present. | BLOCK |
| `policy.ids.present` | Required policy IDs are present for each surface. | BLOCK |
| `policy.versions.present` | Policy versions are present. | BLOCK |
| `policy.deprecated.flagged` | Deprecated policies are flagged. | WARN |
| `policy.lossiness.declared` | Lossiness state is declared where projection is lossy. | FAIL |
| `policy.reversibility.declared` | Reversibility/traceability state is declared. | FAIL |
| `policy.surface_dependencies.valid` | Method-specific dependencies are allowed. | BLOCK |
| `policy.unversioned_external_reference` | External references are versioned or frozen. | FAIL |

### 12.3 Policy Failure Examples

Blocking policy failures include:

```text
projection surface without policy registry
window memberships without window policy
MPLC matched background set without matching policy
CFBS candidate interval without assembly policy
null outputs without null model identity
```

---

## 13. Traceability Validation

Traceability validation confirms that every emitted projection object can be
traced back to source evidence, source packages, policy decisions, and method
surface membership.

### 13.1 Required Traceability Objects

Traceability should connect:

```text
source package → source artifact → VDB substrate → projection membership → method result
```

For burden surfaces, traceability should also connect:

```text
sample_variant_observation_id → projection_membership_id → locus/window/result row
```

### 13.2 Traceability Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `trace.source.present` | Source traceability exists for each substrate. | BLOCK |
| `trace.membership.present` | Projection memberships trace to source observations. | BLOCK |
| `trace.policy.present` | Derived rows trace to policy IDs. | BLOCK |
| `trace.opportunity.present` | Burden rows trace to opportunity model. | BLOCK |
| `trace.method.present` | Result rows trace to method surface ID. | FAIL |
| `trace.validation.present` | Results trace to validation receipts. | FAIL |
| `trace.roundtrip.inspectable` | Evidence trail is reconstructable for sampled records. | FAIL |

### 13.3 Traceability Failure Examples

Blocking traceability failures include:

```text
burden row without sample_variant_observation_id lineage
result row without projection_surface_id
membership row without policy ID
GSC overlay without GSC release or phenotype-scope traceability
```

---

## 14. Identity and Counting Validation

Identity and counting validation prevents annotation expansion, transcript
multiplicity, feature overlap, or projection membership expansion from inflating
observed evidence.

### 14.1 Required Identity Triplet

Projection surfaces that count variants must distinguish:

```text
coordinate_variant_handle       = normalized coordinate/reference-context identity
sample_variant_observation_id   = sample-specific observation of that variant
projection_membership_id        = membership of an observation in a locus/window/feature/annotation
```

### 14.2 Counting Rule

The countable burden unit is:

```text
sample_variant_observation_id
```

The countable burden unit is not:

```text
annotation row
transcript consequence row
gene mapping row
GSC overlay row
projection membership row
candidate interval row
```

### 14.3 Identity and Counting Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `identity.coordinate_handle.present` | Coordinate variant handle is present where coordinate identity is required. | BLOCK |
| `identity.sample_observation.present` | Sample-specific observation identity is present for burden surfaces. | BLOCK |
| `identity.membership.present` | Projection membership identity is present. | BLOCK |
| `count.unit.sample_observation` | Burden counts are computed over sample-specific observations. | BLOCK |
| `count.no_annotation_inflation` | Annotation rows do not inflate burden counts. | BLOCK |
| `count.no_transcript_inflation` | Transcript consequence rows do not inflate burden counts. | BLOCK |
| `count.no_overlay_inflation` | GSC or post hoc overlay rows do not inflate burden counts. | BLOCK |
| `count.duplicate_memberships_audited` | Multiple memberships for one observation are detectable. | FAIL |

---

## 15. MPLC Validation

MPLC validation confirms that the Matched Prior-Locus Contrast surface is a
prior-informed, phenotype-scoped, opportunity-aware contrast rather than an
uncontrolled gene-prior assertion.

### 15.1 Required MPLC Artifacts

An MPLC surface should contain or reference:

```text
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
```

### 15.2 MPLC Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `mplc.scope.present` | MPLC analysis scope is present. | BLOCK |
| `mplc.target.traceable_to_gsc` | Target loci trace to phenotype-scoped GSC priors. | BLOCK |
| `mplc.phenotype_scope.declared` | Phenotype scope is declared and not silently combined. | BLOCK |
| `mplc.background.pool.present` | Background locus pool is present. | BLOCK |
| `mplc.background.non_prior_declared` | Background loci are matched non-prior loci, not declared non-disease genes. | FAIL |
| `mplc.matching.policy.present` | Background matching policy is declared. | BLOCK |
| `mplc.target_background_overlap.audited` | Target/background overlap is excluded, declared, or flagged. | BLOCK |
| `mplc.memberships.traceable` | Variant/locus memberships trace to sample observations. | BLOCK |
| `mplc.burden.counting.valid` | Locus burden counts use sample-specific observations. | BLOCK |
| `mplc.patient_dominance.detectable` | Patient dominance is detectable in hit matrices. | FAIL |
| `mplc.null.reproducible` | Null draw manifest includes reproducibility information. | FAIL |
| `mplc.results.labelled_exploratory` | MPLC results are labeled exploratory/hypothesis-generating. | BLOCK |
| `mplc.pvalue.not_association` | `exploratory_empirical_p_value` is not described as a control-matched disease-association p-value. | BLOCK |

### 15.3 MPLC Blocking Failures

MPLC is unsafe for RDGP consumption if:

```text
target loci do not trace to phenotype-scoped GSC priors
background loci cannot be distinguished from target loci
matching policy is absent
opportunity model is absent for burden-ready claims
burden counts cannot be traced to sample_variant_observation_id
exploratory p-values are labeled as association evidence
```

---

## 16. CFBS Validation

CFBS validation confirms that the Coordinate-First Burden Scan surface nominates
candidate intervals from coordinate-space burden patterns before biological
annotation is used for interpretation.

### 16.1 Required CFBS Artifacts

A CFBS surface should contain or reference:

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

### 16.2 CFBS Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `cfbs.scope.present` | CFBS analysis scope is present. | BLOCK |
| `cfbs.scan_space.present` | Scan space is declared. | BLOCK |
| `cfbs.scan_space.opportunity_declared` | Scan space declares opportunity model or unmodeled status. | BLOCK |
| `cfbs.window_policy.present` | Window policy is declared. | BLOCK |
| `cfbs.windows.not_gsc_selected` | Scan windows are not selected by GSC prior labels. | BLOCK |
| `cfbs.memberships.traceable` | Variant/window memberships trace to sample observations. | BLOCK |
| `cfbs.burden.counting.valid` | Window burden counts use sample-specific observations. | BLOCK |
| `cfbs.patient_dominance.detectable` | Patient dominance is detectable in hit matrices. | FAIL |
| `cfbs.null.model.present` | Matched genomic opportunity null is declared. | BLOCK |
| `cfbs.null.scope.declared` | Null scope is declared, such as per-window or genomewide max statistic. | FAIL |
| `cfbs.candidate_interval.policy.present` | Candidate interval assembly policy is declared. | BLOCK |
| `cfbs.candidate_before_annotation` | Candidate intervals are nominated before post hoc annotation. | BLOCK |
| `cfbs.annotation_timing.posthoc` | Post hoc annotations declare `annotation_timing = post_candidate_nomination`. | BLOCK |
| `cfbs.gsc_annotations.posthoc` | GSC/gene/regulatory annotations are marked post hoc. | BLOCK |
| `cfbs.results.labelled_exploratory` | CFBS results are labeled exploratory/hypothesis-generating. | BLOCK |
| `cfbs.pvalue.not_association` | `exploratory_empirical_p_value` is not described as a control-matched disease-association p-value. | BLOCK |

### 16.3 CFBS Blocking Failures

CFBS is unsafe for RDGP consumption if:

```text
scan windows are selected by GSC prior labels
candidate intervals are created after biological annotation filtering
post hoc annotations are not marked post_candidate_nomination
matched genomic opportunity null is absent
burden-ready claims lack opportunity support
burden counts cannot be traced to sample_variant_observation_id
exploratory p-values are labeled as association evidence
```

---

## 17. RDGP Consumption Boundary Validation

RDGP consumption boundary validation confirms that VDB is emitting a
reason-ready surface rather than requiring RDGP to rebuild VDB integration logic.

### 17.1 Consumption Boundary Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `rdgp.consume.no_reintegration_required` | RDGP can consume the surface without re-ingesting VAP/GSC packages. | BLOCK |
| `rdgp.consume.receipts_present` | Required validation receipts are present or emitted. | FAIL |
| `rdgp.consume.traceability_present` | Source traceability is sufficient for RDGP explanations. | BLOCK |
| `rdgp.consume.method_not_reasoning` | Projection-surface outputs are not encoded as final RDGP rankings. | BLOCK |
| `rdgp.consume.surface_identity_present` | Projection surface identity is declared. | BLOCK |
| `rdgp.consume.method_version_present` | Method version is declared. | FAIL |

### 17.2 Consumption Boundary Failure Examples

Blocking failures include:

```text
RDGP must load VAP packages to understand VAP-derived observations
RDGP must load GSC packages to determine phenotype-prior target loci
projection result rows lack provenance to VDB-emitted substrates
projection surface result is already labeled as RDGP rank or diagnosis
```

---

## 18. Anti-Overclaim Validation

Anti-overclaim validation confirms that exploratory projection surfaces are not
represented as disease association, pathogenicity, diagnosis, or final RDGP
reasoning outputs.

### 18.1 Required Anti-Overclaim Labels

Projection surfaces should declare an anti-overclaim label set.

Allowed labels may include:

```text
descriptive_only
exploratory_hypothesis_generating
not_association_evidence
not_control_matched_association
not_diagnostic
not_pathogenicity_claim
opportunity_limited
```

### 18.2 Forbidden Interpretive Claims

Projection surfaces must not label exploratory outputs as:

```text
disease_associated_region
pathogenic_region
causal_locus
diagnostic_result
validated_association
clinical_finding
```

### 18.3 Anti-Overclaim Checks

| Check ID | Description | Severity |
| --- | --- | --- |
| `claim.labels.present` | Anti-overclaim labels are present. | BLOCK |
| `claim.exploratory_declared` | Exploratory result posture is declared. | BLOCK |
| `claim.pvalue.exploratory` | Exploratory empirical p-values are labeled correctly. | BLOCK |
| `claim.no_association_language` | Association/diagnostic/pathogenicity language is absent unless separately justified. | BLOCK |
| `claim.method_not_rdgp_reasoning` | Method results are not encoded as final RDGP reasoning outputs. | BLOCK |

---

## 19. Failure Severity Model

Validation checks should use a small severity vocabulary.

```text
PASS            = check succeeded
WARN            = non-blocking concern; product remains inspectable
FAIL            = invalid or incomplete condition; product may be inspectable but not clean
BLOCK           = unsafe for RDGP consumption
NOT_APPLICABLE  = check not relevant to this surface or profile
```

### 19.1 Failure Classes

Validation failures should be grouped into classes:

```text
schema_failure
package_failure
source_corpus_failure
shared_substrate_failure
traceability_failure
identity_failure
counting_failure
opportunity_failure
policy_failure
method_surface_failure
anti_overclaim_failure
rdgp_consumption_failure
```

### 19.2 BLOCK Conditions

A projection surface should be blocked from normal RDGP consumption if any of
the following occur:

```text
missing source traceability
missing sample_variant_observation_id for burden counts
burden_ready without opportunity basis
opportunity_unmodeled treated as burden_ready
projection results without policy identity
MPLC target and background loci not distinguishable
CFBS windows selected by GSC prior labels
CFBS post hoc annotations not marked post hoc
exploratory empirical p-values interpreted as control-matched association p-values
projection results encoded as RDGP rankings or diagnosis
```

---

## 20. Validation Receipt Requirements

Validation receipts are part of the projection-surface product, not optional
side commentary.

Each validation check should be represented in a receipt or receipt summary that
supports audit and downstream filtering.

### 20.1 Receipt Fields

Recommended fields:

```text
validation_receipt_id
tep_vdb_id
source_corpus_id
projection_surface_id
method_id
method_version
validator_id
validator_version
validation_timestamp_utc
check_id
check_group
check_name
severity
status
failure_class
affected_artifact
affected_field
affected_record_count
message
recommendation
```

### 20.2 Receipt Aggregation

A validation run should also emit surface-level summary values:

```text
total_checks
pass_count
warn_count
fail_count
block_count
not_applicable_count
overall_validation_status
rdgp_consumption_status
```

Recommended `rdgp_consumption_status` values:

```text
rdgp_consumable
rdgp_consumable_with_warnings
rdgp_not_consumable
validation_incomplete
```

---

## 21. Demonstration Profile Validation

Generic validation should not hard-code the first demonstration corpus.

However, named demonstration profiles may add strict profile expectations.

### 21.1 Example Demonstration Profile

A future profile may be named:

```text
epilepsy_12vap_2gsc_projection_surface_v1
```

It may require:

```text
12 VAP source TEPs
2 GSC source TEPs
epilepsy phenotype-scoped GSC source
mitochondrial phenotype-scoped GSC source
expected source corpus IDs
expected genome build declarations
expected projection surface methods, such as MPLC and CFBS
```

### 21.2 Profile Validation Rule

Profile-specific failures must be labeled as profile failures rather than generic
schema failures.

Example:

```text
profile.expected_source_missing
```

This prevents the generic TEP-VDB schema from becoming accidentally tied to one
corpus demonstration.

---

## 22. Future Extensions

Future validation extensions may cover:

```text
RSP functional projection surfaces
cross-modal convergence surfaces
RDGP-TEP return-leg validation
structural-variant projection surfaces
mitochondrial heteroplasmy-aware projection surfaces
sample-specific callability models
control-matched association extensions, if true controls are later introduced
```

Future extensions should preserve the same principles:

```text
source traceability
identity separation
opportunity awareness
policy declaration
uncertainty preservation
anti-overclaim labeling
RDGP consumption safety
```

---

## 23. Summary

Projection-surface validation ensures that VDB-emitted TEP-VDB products are safe
for RDGP consumption.

A valid projection surface must be:

```text
structurally complete
source-traceable
identity-preserving
sample-observation countable
opportunity-aware
policy-declared
method-coherent
anti-overclaim bounded
RDGP-consumable without source re-integration
```

The validation plan intentionally precedes implementation. It defines what must
be true before future validators, builders, fixtures, and system contracts encode
those checks in executable form.

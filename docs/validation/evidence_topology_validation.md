# Evidence Topology Validation

## Purpose

This document defines validation requirements for Phase 4.4 Evidence Topology in the Variant Database (VDB).

Evidence Topology validation proves that VDB can deterministically derive reconstructable, non-interpretive topology relationships from a validated Assertion Record surface while preserving lineage, authority boundaries, source identity expansion handles, namespace state, and downstream Convergence Geometry readiness.

Validation also confirms that emitted topology artifacts use schema-recognized controlled vocabularies and comply with the declared topology derivation policy.

This document is a validation governance document.

This document is not the Evidence Topology contract.

This document is not the Evidence Topology specification.

This document is not the Evidence Topology schema.

This document is not a validation receipt.

---

# Validation Scope

This document governs validation for Evidence Topology builds, including the initial canonical Phase 4.4 build:

```text
topology_build_id:
    mark_phase4_corpus_6tep_v1_topology_build_v1

input_corpus_generation_id:
    mark_phase4_corpus_6tep_v1

input Assertion Record surface:
    results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/

expected topology output:
    results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/
```

Validation must confirm that Evidence Topology answers:

```text
What is connected within the declared corpus?
```

Validation must not claim that Evidence Topology answers:

```text
What structural properties emerge from those connections?
Which convergence regions are important?
Which surfaces are eligible for disclosure?
Which projections should consumers receive?
Whether a relationship is biologically meaningful?
Whether a relationship is statistically significant?
Whether evidence explains disease?
```

Those responsibilities belong to downstream Convergence Geometry, Evidence Convergence Surface, Projection View, consumer projection, or reasoning layers.

---

# Non-Goals

Evidence Topology validation does not validate:

```text
biological correctness
clinical correctness
statistical significance
poly-noncoding variant burden
case-control enrichment
regulatory feature burden
pathway burden
network-level disease burden
convergence geometry features
surface eligibility
surface disclosure
Projection View correctness
RDGP reasoning
```

Evidence Topology validation may confirm that future statistical or burden-oriented workflows have explicit expansion handles.

It must not claim that those workflows have already been performed.

---

# Required Governed Inputs

A Phase 4.4 validation run must consume a governed Assertion Record surface and the declared topology derivation policy.

For the initial canonical build, required Assertion Record inputs are:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_index.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_index.jsonl
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_participants.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_source_identity_sets.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_source_identity_summary.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_lineage.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_payload_references.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_validation_report.tsv
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/downstream_topology_input_manifest.tsv
```

The initial canonical derivation policy input is:

```text
docs/implementation/policies/evidence_topology/mark_phase4_vap_gsc_topology_derivation_policy_v1.json
```

A validation run must verify that the topology builder consumes the Assertion Record surface and declared derivation policy rather than opportunistically crawling Registration Units, parsing raw producer artifacts, or re-running ingestion.

Evidence Topology may preserve references to Registration Units through Assertion Record lineage.

Evidence Topology must not reconstruct Registration Units as its primary input path.

---

# Required Topology Outputs

A valid Evidence Topology build should emit the following artifact family:

```text
topology_build_manifest.tsv
topology_build_manifest.json
topology_relationships.tsv
topology_relationships.jsonl
topology_relationship_members.tsv
topology_basis_components.tsv
topology_source_identity_expansion_index.tsv
topology_namespace_mediation.tsv
topology_metadata_relationships.tsv
topology_summary.tsv
topology_validation_report.json
topology_validation_report.tsv
topology_build_report.md
downstream_geometry_input_manifest.tsv
```

The output family must remain distinct from:

```text
Assertion Record outputs
Corpus Generation outputs
Registration Unit outputs
Convergence Geometry outputs
Evidence Convergence Surface outputs
Projection View outputs
```

Output completeness validation must confirm:

```text
all required topology outputs exist
all required topology outputs have expected headers
header-only outputs are allowed only when policy explicitly disables that behavior
header-only outputs must preserve validation status or deferral semantics
topology_namespace_mediation.tsv may be header-only or explicitly deferred for Phase 4.4 v1 when namespace mediation is not policy-enabled
topology_source_identity_expansion_index.tsv must not be missing when topology relationships reference Source Identity Sets
```

---

# Validation Layers

Evidence Topology validation uses staged validation.

## Layer 1: Unit And Regression Validation

Layer 1 uses synthetic or minimal fixtures to validate builder behavior, identity stability, relationship construction, basis construction, source lineage, source identity expansion handling, namespace status handling, determinism, non-mutation, and anti-collapse behavior.

Layer 1 must be fast enough to run as part of normal local test execution.

## Layer 2: Repo-Local Canonical Full-Corpus Smoketest

Layer 2 uses the real, git-tracked canonical Phase 4.3 Assertion Record surface:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

Layer 2 is the default closure-grade smoketest for Phase 4.4 v1 when the topology builder consumes only the compact Assertion Record surface.

Layer 2 replaces the need for a separate compressed golden fixture when the real canonical input is small, local, deterministic, and practical to validate directly.

## Layer 3: Optional MARK Parity Or Expansion-Dependent Validation

Layer 3 is required only when a Phase 4.4 implementation begins dereferencing large Source Identity Sets, depends on MARK-local Registration Unit access, or requires operational parity with MARK.

Layer 3 is optional for a conservative v1 topology builder that consumes only the repo-local Assertion Record surface and does not perform controlled source identity expansion.

---

# Input-Boundary Validation

Input-boundary validation must confirm:

```text
input Assertion Record index exists
downstream topology input manifest exists
input_corpus_generation_id is declared
input Assertion Record source identity is declared
topology derivation policy is declared
topology derivation policy exists
topology derivation policy is readable
schema-recognized controlled vocabulary expectations are declared
builder name is declared
builder version is declared when available
build timestamp is declared
raw producer artifacts are not parsed
ingestion is not re-run
Registration Units are not crawled opportunistically
Assertion Record inputs are not mutated
Corpus Generation scope is not expanded silently
```

Validation must fail if topology derivation bypasses Assertion Record primacy.

---

# Topology Build Identity Validation

Topology Build validation must confirm:

```text
topology_build_id exists
topology_build_id is stable under fixed inputs
topology_build_label is present when emitted
input_corpus_generation_id is present
input_assertion_record_index_id is present
input_downstream_topology_manifest_id or path is present
topology_derivation_policy_id is present
topology_derivation_policy_version is present when available
builder_name is present
builder_version is present when available
build_timestamp_utc is present
validation_status is present
certification_status is present when available or explicitly not_applicable
```

The initial canonical build identity is expected to be:

```text
mark_phase4_corpus_6tep_v1_topology_build_v1
```

---

# Topology Relationship Validation

Relationship validation must confirm every topology relationship has:

```text
topology_relationship_id
topology_build_id
topology_dimension
relationship_kind
derivation_basis
input_corpus_generation_id
source_assertion_id_summary or explicit metadata-level exception
relationship_member_summary
basis_component_summary
validation_status
```

Validation must confirm:

```text
topology_relationship_id values are unique
topology_relationship_id values are deterministic
topology_dimension is not empty
relationship_kind is not empty
derivation_basis is not empty
dimension, kind, and basis are not collapsed into one ambiguous field
source Assertion Record lineage is reconstructable
metadata-level relationships are explicitly marked as metadata-level
non-metadata relationships trace to one or more Assertion Records
```

A topology relationship without a declared derivation basis is invalid.

A non-metadata topology relationship without reconstructable Assertion Record lineage is invalid.

---

# Policy Execution Validation

Policy execution validation must confirm:

```text
topology derivation policy exists
topology derivation policy identity matches the topology build manifest
every emitted relationship kind is policy-enabled or explicitly policy-local
every enabled relationship family is executed or explicitly failed
no enabled relationship family is silently skipped
deferred relationship families are not emitted as completed topology
prohibited relationship families are not emitted
relationship family execution report exists
relationship family execution report preserves enabled, deferred, prohibited, skipped, failed, and emitted states
```

For Phase 4.4 v1, validation must fail if Evidence Topology emits exact participant-value overlap, namespace-mediated participant-value matches, biological convergence, burden scores, case-control enrichment, statistical significance, surface eligibility, or RDGP priority signals.

---

# Controlled Vocabulary Validation

Controlled vocabulary validation must confirm that emitted topology values are recognized by the Evidence Topology schema or explicitly declared as policy-local extensions.

Validation must confirm schema-recognized values for:

```text
topology_dimension
relationship_kind
derivation_basis
relationship_scope
relationship_classification
source_identity_expansion_status
statistical_testing_status
namespace_mediation_status
match_type when emitted
resolution_status when emitted
ambiguity_status when emitted
conflict_status when emitted
lossiness_status when emitted
validation_status
certification_status when emitted
```

Validation must fail if an output artifact silently emits uncontrolled values for these fields.

Validation must also confirm that topology-layer `validation_status` values are not confused with upstream Assertion Record preservation or resolver states.

---

# Validation Status Scope Validation

Within Evidence Topology outputs, `validation_status` means topology-layer validation status unless the field name explicitly indicates an upstream source status.

Topology-layer validation status values are:

```text
passed
passed_with_note
failed
not_applicable
deferred_by_policy
```

When upstream Assertion Record states are preserved, topology outputs should use explicit source-status summary fields such as:

```text
source_assertion_validation_status_summary
source_assertion_resolver_status_summary
source_assertion_preservation_status_summary
```

Validation must fail if upstream source states such as `preserved`, `supported`, `indexed_with_note`, or `deferred` are used as topology-layer validation statuses.

---

# Relationship Member Validation

Relationship member validation must confirm:

```text
topology_relationship_members.tsv exists
every member references a valid topology_relationship_id
member_id or equivalent member reference is present
member_type is present
member_role is present
member_reference or member_value is present
source_assertion_id is present when applicable
source_registration_unit_id is present when applicable
source_corpus_generation_id is present
source_identity_set_id is present when applicable
validation_status is present
```

Relationship members must be explicit.

Relationship members must not imply biological importance.

Relationship members must not replace Assertion Record lineage.

---

# Basis Component Validation

Basis component validation must confirm:

```text
topology_basis_components.tsv exists
every basis component references a valid topology_relationship_id
basis_component_id is present
basis_component_type is present
basis_component_role is present when applicable
basis_component_value or basis_component_reference is present
source_assertion_id is present when applicable
source_registration_unit_id is present when applicable
source_corpus_generation_id is present
source_identity_set_id is present when applicable
resolution_status is explicit when applicable
ambiguity_status is explicit when applicable
conflict_status is explicit when applicable
lossiness_status is explicit when applicable
validation_status is present
```

Basis components must explain why the topology relationship exists.

A topology relationship whose basis cannot be reconstructed is invalid.

---

# Source Identity Expansion Validation

Source identity expansion validation protects the boundary between compact topology and the larger source identity universe.

Validation must confirm:

```text
topology_source_identity_expansion_index.tsv exists
source_identity_set_id values join to assertion_record_source_identity_sets.tsv
source_identity_count is preserved when available
source identity kind is preserved when available
participant role is preserved when available
source namespace is preserved when available
source Assertion Record lineage is preserved
source Registration Unit lineage is preserved when available
source_identity_expansion_status is explicit
statistical_testing_status is explicit
lossiness_status is preserved when available, including lossless_by_reference
source_identity_count is preserved as a reconstruction count, not interpreted as an independent evidence count
available_by_source_identity_set_reference does not imply expanded source identities
requires_controlled_expansion records do not claim analysis_ready
expanded_under_policy is not emitted without a declared controlled expansion policy
large Source Identity Sets are not flattened into topology relationships
large Source Identity Sets are not hidden from downstream reconstruction
```

Allowed `source_identity_expansion_status` values include:

```text
not_required
available_by_source_identity_set_reference
requires_controlled_expansion
expanded_under_policy
deferred_by_policy
not_applicable
unavailable
header_only_not_policy_enabled
```

For Phase 4.4 v1, `available_by_source_identity_set_reference` means that Source Identity Set references preserve addressable expansion handles, not that granular source identities have been expanded.

For Phase 4.4 v1, `expanded_under_policy` must not be emitted unless a controlled source identity expansion policy is declared and validated.

Allowed `statistical_testing_status` values include:

```text
not_statistical_input
analysis_ready
requires_source_identity_expansion
requires_external_annotation
requires_case_control_design
deferred_to_projection_layer
not_applicable
```

For Phase 4.4 v1, Evidence Topology may identify burden-relevant expansion handles.

It must not claim that poly-noncoding burden testing, case-control enrichment, regulatory feature burden, pathway burden, or network-level disease burden has been performed.

---

# Namespace Mediation Validation

Namespace mediation validation must confirm:

```text
topology_namespace_mediation.tsv exists or namespace mediation is explicitly not_applicable
namespace_mediation_status is explicit
match_type is explicit when namespace mediation is used
source identity matches are distinguishable from namespace-mediated matches
ambiguous namespace states remain ambiguous
conflicted namespace states remain conflicted
unresolved namespace states remain unresolved
canonical identity attachment does not replace source identity lineage
validation_status is present
```

Allowed `match_type` values include:

```text
source_identity_match
source_namespace_match
canonical_identity_match
namespace_mediated_match
ambiguous_namespace_match
conflicted_namespace_match
unresolved_namespace_state
not_applicable
deferred
```

A namespace-mediated relationship must not masquerade as a direct source identity match.

`source_namespace_only` means that source namespace grouping or preservation is available, but canonical identity resolution has not been performed.

Validation must fail if `source_namespace_only` relationships are treated as direct source identity matches, canonical identity matches, or namespace-mediated identity matches.

For Phase 4.4 v1, validation must fail if `canonical_identity_match` or `namespace_mediated_match` is emitted without an explicit namespace mediation policy that enables it.

Deferred namespace states must remain explicit as `deferred_by_policy` or equivalent policy-declared deferral states.

---

# Metadata-Level Topology Validation

Metadata-level topology validation must confirm:

```text
metadata-level relationships are explicitly policy-enabled
metadata-level relationships declare relationship_scope or equivalent metadata marker
metadata-level relationships declare derivation basis
metadata-level relationships preserve Corpus Generation lineage
metadata-level relationships preserve Registration Unit lineage when applicable
metadata-level relationships do not imply biological relatedness
metadata-level relationships do not become source evidence
```

Valid Phase 4.4 v1 metadata-level or metadata-derived relationship kinds include:

```text
corpus_metadata_membership
registration_unit_membership
producer_family_membership
assertion_type_membership
relationship_class_membership
preservation_status_membership
resolver_status_membership
validation_status_membership
source_identity_set_status_membership
source_identity_resolution_status_membership
source_identity_lossiness_status_membership
```

Policy-conditional or future metadata-level relationship kinds may include:

```text
evidence_domain_membership
temporal_generation_membership
independence_group_membership
certification_status_membership
source_identity_obligation_status_membership
```

Policy-conditional or future relationship kinds must not be required for Phase 4.4 v1 unless the active derivation policy enables them.

---

# Downstream Geometry Boundary Validation

Evidence Topology is the input to Convergence Geometry.

Validation must confirm:

```text
downstream_geometry_input_manifest.tsv exists
downstream_geometry_input_manifest.tsv references valid topology_relationship_id values
downstream_geometry_input_manifest.tsv preserves input_corpus_generation_id
downstream_geometry_input_manifest.tsv preserves input_assertion_record_index_id
downstream_geometry_input_manifest.tsv preserves source assertion summaries
downstream_geometry_input_manifest.tsv preserves relationship kind and derivation basis
downstream_geometry_input_manifest.tsv preserves namespace mediation status when applicable
downstream_geometry_input_manifest.tsv preserves source identity expansion status when applicable
```

Validation must fail if Evidence Topology emits:

```text
convergence density
convergence breadth
convergence depth
producer diversity metric
modality diversity metric
evidence-domain diversity metric
structural motif
convergence region
surface eligibility
surface disclosure
surface withholding
biological significance
statistical significance
burden score
surface eligibility
projection readiness
RDGP readiness
biological interpretation
```

Those are downstream responsibilities.

---

# Determinism Validation

Determinism validation must confirm that fixed inputs and fixed policy produce equivalent outputs.

Validation must check stability of:

```text
topology_build_id
topology_relationship_id values
relationship ordering
relationship member ordering
basis component ordering
namespace mediation ordering
source identity expansion index ordering
topology summary values
validation report values
downstream geometry input manifest
```

Topology identity must not depend on:

```text
filesystem traversal order
incidental SQLite row-return order
Python object iteration order
temporary row numbers
wall-clock timestamp except in build metadata
```

Build timestamps may differ across runs.

Topology meaning must not differ under fixed input and policy.

---

# Non-Mutation Validation

Non-mutation validation must confirm that topology construction does not modify:

```text
Assertion Record input files
Corpus Generation input files
Registration Unit files
producer artifacts
validation receipt inputs
```

Recommended checks include:

```text
input file SHA256 before build
input file SHA256 after build
input file size before build
input file size after build
mtime inspection when appropriate
```

Validation fails if governed upstream inputs are mutated.

---

# Anti-Collapse Validation

Anti-collapse validation must fail if Evidence Topology:

```text
replaces Assertion Records
modifies Assertion Records
mutates Registration Units
expands Corpus Generation scope silently
treats topology as source evidence
treats topology as biological truth
performs biological reasoning
performs statistical inference
declares surface eligibility
declares surface disclosure
emits Convergence Geometry features
emits Projection Views that replace topology
collapses topology_dimension, relationship_kind, and derivation_basis
hides Source Identity Set expansion requirements
flattens large Source Identity Sets into topology relationships
claims burden-readiness without analyzable substrate
treats source identity count as independent evidence count
treats namespace-mediated identity as direct source identity
```

Anti-collapse validation protects the boundary:

```text
Assertion Records preserve claims.
Evidence Topology derives organization.
Convergence Geometry characterizes organization.
```

---

# Validation Receipt Requirements

Evidence Topology validation receipts live under:

```text
results/validation/phase4_evidence_topology/
```

The initial canonical receipt family should use a path such as:

```text
results/validation/phase4_evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1_validation_<timestamp>/
```

Expected receipt contents include:

```text
README.md
validation_summary.json
validation_summary.tsv
topology_validation_report.json
topology_validation_report.tsv
count_reconciliation.tsv
input_boundary_report.tsv
relationship_integrity_report.tsv
source_identity_expansion_report.tsv
namespace_mediation_report.tsv
downstream_geometry_boundary_report.tsv
anti_collapse_report.tsv
input_mutation_report.tsv
output_file_manifest.tsv
runtime_metadata.json
runtime_metadata.tsv
```

If a portable archive is emitted, the checksum authority should be an external sidecar:

```text
retrieval/phase4_4_evidence_topology_smoketest_<timestamp>.tgz
retrieval/phase4_4_evidence_topology_smoketest_<timestamp>.tgz.sha256
```

A receipt proves that a validation run occurred and what it found.

A receipt does not replace this validation document.

---

# Phase 4.4 Closure Criteria

Phase 4.4 Evidence Topology validation may be considered complete for a declared topology build only when:

```text
Evidence Topology validation document exists
topology implementation exists
topology build output exists
validation receipt exists
all required validation checks pass
topology build identity is stable
topology derivation policy is declared
topology derivation policy is validated
schema-recognized controlled vocabularies are used
enabled relationship families are executed or explicitly failed
deferred relationship families remain deferred unless a future policy enables them
prohibited relationship families are absent
relationships are deterministic and reconstructable
every relationship declares dimension, kind, and basis
relationship members are explicit
basis components are explicit
source Assertion Record lineage is preserved
Corpus Generation lineage is preserved
Registration Unit lineage is preserved when applicable
Source Identity Set expansion handles are explicit
statistical_testing_status values are honest
namespace mediation is explicit or not_applicable
downstream geometry input manifest exists
no geometry features are emitted
no surface eligibility is emitted
no Projection View replaces topology
no biological reasoning is performed
input files are not mutated
```

Closure for the initial topology build should be stated as:

```text
Phase 4.4 Evidence Topology validation is complete for
mark_phase4_corpus_6tep_v1_topology_build_v1.
```

Closure must not be stated as:

```text
all future Evidence Topology validation is complete
all possible topology derivation policies are validated
poly-noncoding burden testing is validated
RDGP readiness is validated
Phase 4.8 certification is complete
```

---

# Summary

Evidence Topology validation proves that VDB can derive organization over preserved Assertion Records without violating source authority, lineage, namespace, or downstream layer boundaries.

The validation target is not biological truth.

The validation target is:

```text
topology derived from the validated Assertion Record surface
relationships that are reconstructable and non-interpretive
schema-recognized controlled vocabularies
policy-enabled relationship families
source identity sets that remain expansion-addressable
namespace mediation that remains honest
outputs that are deterministic and non-mutating
a downstream geometry manifest that is safe for Phase 4.5
```

Phase 4.4 should close only when topology is compact, claim-derived, expansion-aware, lineage-preserving, deterministic, and safe for Convergence Geometry.


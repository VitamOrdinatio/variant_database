# Corpus Generation Implementation Plan

## Purpose

This document defines the implementation plan for Corpus Generation construction in VDB Phase 4.

A Corpus Generation is the declared evidence scope from which Phase 4 derived evidence structures are built.

This plan describes how VDB will select Registration Units under an explicit policy, preserve inclusion and exclusion rationale, emit deterministic corpus manifests, validate corpus scope, and provide downstream input material for Assertion Record indexing.

The Phase 4 Corpus Generation implementation goal is:

```text
Declare a deterministic, reconstructable evidence scope that preserves
Registration Unit boundaries and can serve as the input basis for
Assertion Record indexing and downstream derived evidence construction.
```

A Corpus Generation declares scope.

It does not interpret evidence.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/corpus_generation/corpus_generation_contract.md
```

The governing contract states that a Corpus Generation must remain:

```text
declared
traceable
deterministic
registration-unit-preserving
producer-aware
scope-explicit
policy-explicit
validation-aware
certification-aware
reconstructable
```

This plan is subordinate to the Corpus Generation contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Corpus Generation implementation role is to declare which Registration Units are selected together as a bounded evidence universe for downstream Phase 4 derivation.

A Corpus Generation implementation answers:

```text
Which Registration Units are selected together as the evidence basis
for this derived VDB build?
```

It does not answer:

```text
What scientific claims are represented as Assertion Records?

What relationships exist among assertions?

What topology emerges from the selected corpus?

What convergence geometry exists?

Which convergence regions are surface-eligible?

What projections should consumers receive?

What biological meaning should downstream systems infer?
```

Those questions belong to downstream implementation plans.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Registration Unit repair
Registration Unit migration
Registration Unit recertification
producer TEP parsing
raw producer artifact parsing
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
RDGP reasoning
biological interpretation
```

Corpus Generation construction may inspect selected Registration Units or Registration Unit readiness inventories.

It must not mutate Registration Units.

It must not create source authority.

It must not become source truth.

---

# Initial Implementation Target

The initial implementation target is the certified Phase 3 MARK Registration Unit set.

The initial benchmark Corpus Generation should be identified as:

```text
mark_phase4_corpus_6tep_v1
```

or another explicitly declared Corpus Generation identifier.

The initial benchmark Corpus Generation is expected to include:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

This initial Corpus Generation is useful because it includes:

```text
multiple producer families
heterogeneous evidence domains
small GSC semantic evidence packages
large VAP source-identity-heavy evidence packages
certified Phase 3 registration outputs
realistic MARK-scale storage behavior
```

This benchmark Corpus Generation is not the only valid Corpus Generation pattern.

Future Corpus Generations may include different Registration Units, producer families, cohorts, evidence modalities, evidence domains, external evidence capsules, or reasoning-returned assertion packages.

---

# Inputs

The Corpus Generation implementation consumes:

```text
Registration Unit readiness inventory
explicit Corpus Generation selection manifest
Corpus Generation selection policy
Corpus Generation validation policy
Corpus Generation contract version
system contract version
builder name
builder version
build timestamp
```

The Registration Unit readiness inventory should be produced by the Registration Unit implementation plan.

The selection manifest declares candidate Registration Units and their intended inclusion or exclusion status.

The selection policy determines which Registration Units become part of the Corpus Generation.

A folder listing is not sufficient to define a Corpus Generation.

Implicit filesystem discovery must not silently define corpus scope.

---

# Outputs

The Corpus Generation implementation should emit deterministic sidecar artifacts outside the selected Registration Units.

Expected outputs may include:

```text
corpus_generation_manifest.tsv
corpus_generation_manifest.json
corpus_generation_report.md
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
downstream_assertion_record_input_manifest.tsv
```

These outputs are Corpus Generation artifacts.

They do not replace Registration Units.

They do not create Assertion Records.

They do not define topology, geometry, surfaces, projections, or biological interpretation.

---

# Recommended Output Location

Initial Phase 4 Corpus Generation outputs may be written under:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
```

A recommended initial layout is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
    corpus_generation_manifest.tsv
    corpus_generation_manifest.json
    corpus_generation_report.md
    corpus_generation_validation_report.json
    corpus_generation_validation_report.tsv
    downstream_assertion_record_input_manifest.tsv
```

The output location should be configurable.

Corpus Generation output paths must not be confused with Registration Unit source paths.

---

# Required Corpus Generation Identity

Every Corpus Generation must have a stable identity.

A Corpus Generation identity must preserve:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version when applicable
selection_policy_id
selection_policy_version when applicable
builder_name
builder_version when available
build_timestamp
validation_status
certification_status when available
```

For the initial MARK benchmark corpus, a recommended identity shape is:

```text
corpus_generation_id: mark_phase4_corpus_6tep_v1
corpus_generation_label: MARK Phase 4 6-TEP Benchmark Corpus v1
corpus_generation_purpose: initial certified multi-producer Phase 4 heavy smoketest corpus
corpus_generation_version: v1
selection_policy_id: mark_phase4_6tep_certified_input_policy
selection_policy_version: v1
```

Human-readable labels may support inspection.

Labels must not replace stable Corpus Generation identity.

---

# Selection Policy Requirements

Every Corpus Generation must declare a selection policy.

The selection policy must define:

```text
eligible Registration Units
selected Registration Units
excluded Registration Units when exclusion is relevant
required validation status
required certification status when applicable
producer families in scope
evidence domains in scope
temporal or generation constraints when applicable
inclusion rationale requirements
exclusion rationale requirements
failure behavior
```

For the initial MARK benchmark corpus, the selection policy should state:

```text
Select the six certified Phase 3 MARK Registration Units representing
two GSC semantic evidence packages and four VAP variant evidence packages
for initial Phase 4 multi-producer heavy smoketest derivation.
```

The selection policy must be versioned when policy evolution would affect Corpus Generation reconstruction.

Selection policy must not be replaced by an informal file list.

---

# Registration Unit Inclusion Requirements

A Corpus Generation must explicitly declare every included Registration Unit.

For each included Registration Unit, the Corpus Generation manifest must preserve:

```text
registration_unit_id
registration_unit_label
registration_unit_path or resolvable reference
producer_family
source_package_id
registration_backend
validation_status
certification_status when available
inclusion_status
inclusion_rationale
```

Inclusion status may include:

```text
included
included_with_note
included_for_fixture
included_for_failure_mode
```

Inclusion rationale may include:

```text
certified Phase 3 benchmark input
producer-family representation
evidence-domain representation
cohort representation
heavy smoketest coverage
consumer projection readiness testing
release-corpus inclusion
failure-mode testing
synthetic fixture inclusion
```

Included Registration Units must remain individually identifiable.

A Corpus Generation must not merge selected Registration Units into a single opaque evidence source.

---

# Registration Unit Exclusion Requirements

A Corpus Generation should explicitly declare excluded Registration Units when exclusion affects interpretation of corpus scope.

For each relevant excluded Registration Unit or candidate, the Corpus Generation manifest should preserve:

```text
registration_unit_id or candidate reference
registration_unit_label when available
registration_unit_path or resolvable reference when available
observed_producer_family when available
observed_validation_status when available
observed_certification_status when available
exclusion_status
exclusion_rationale
observed_failure_reason when applicable
```

Exclusion status may include:

```text
excluded
excluded_uncertified
excluded_failed_validation
excluded_out_of_scope
excluded_duplicate
excluded_superseded
excluded_missing
excluded_unreadable
deferred
not_evaluated
```

Exclusion rationale may include:

```text
uncertified Registration Unit
failed validation
out-of-scope producer family
out-of-scope cohort
out-of-scope evidence domain
duplicate or superseded Registration Unit
missing path
unreadable backend
explicitly deferred input
```

A Corpus Generation must not silently exclude Registration Units when the exclusion affects scope interpretation.

---

# Corpus Manifest Requirements

A Corpus Generation must emit or resolve to a corpus manifest.

The corpus manifest must preserve:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version when applicable
selection_policy_id
selection_policy_version when applicable
included_registration_units
excluded_registration_units when applicable
producer_family_summary
package_summary
artifact_count_summary
assertion_registration_count_summary
source_identity_count_summary
namespace_count_summary when available
validation_status_summary
certification_status_summary
build_timestamp
builder_name
builder_version when available
manifest_schema_version when available
```

The manifest must be deterministic under fixed inputs.

The manifest must be sufficient to reconstruct the exact selected Registration Unit set.

The manifest must not replace selected Registration Units.

The manifest must not become source truth.

---

# Count And Inventory Requirements

A Corpus Generation may summarize selected Registration Units.

Allowed count and inventory summaries include:

```text
number of Registration Units
producer-family distribution
package count
artifact count
assertion registration count
source identity count
namespace distribution
evidence-domain distribution
validation status distribution
certification status distribution
storage footprint summary when available
```

Count and inventory summaries must remain traceable to selected Registration Units.

Summaries must not replace Registration Unit records.

Summaries must not collapse:

```text
source identity
producer identity
artifact identity
assertion registration identity
validation status
certification status
Registration Unit boundaries
```

If counts are unavailable, incomplete, approximate, or not applicable, that status must be explicit.

---

# Certification-Aware Behavior

Corpus Generation construction must preserve both Registration Unit status and Corpus Generation status.

A Corpus Generation built entirely from certified Registration Units is not automatically certified.

Certified Registration Units support Corpus Generation certification.

They do not replace Corpus Generation validation.

Supported Corpus Generation status values include:

```text
planned
provisional
validated
certified
rejected
deprecated
```

For the initial implementation:

```text
Input Registration Units may be certified.

The initial Corpus Generation may be validated after manifest and scope checks pass.

The Corpus Generation becomes certified only after declared certification checks pass.
```

A Corpus Generation must not silently masquerade as certified.

A Corpus Generation builder must not promote Registration Unit certification status.

---

# Read-Only Input Requirements

Corpus Generation construction may inspect Registration Units and Registration Unit readiness inventories.

Allowed actions include:

```text
read Registration Unit metadata
read Registration Unit validation status
read Registration Unit certification status
read package registrations
read artifact registrations
read assertion registration counts
read source identity counts
read producer-family metadata
read Registration Unit readiness inventories
emit corpus manifests
emit corpus inventories
emit corpus validation reports
emit sidecar indexes
emit downstream input manifests
```

Prohibited actions include:

```text
rewriting certified Registration Units
deleting Registration Unit records
mutating producer package references
mutating artifact references
mutating assertion registrations
mutating source identities
replacing source identities with canonical identities
changing Registration Unit certification status without evidence
copying all source identities into a materialized corpus without explicit need
treating materialized corpus output as source truth
```

If Corpus Generation construction requires Registration Unit repair, migration, regeneration, or recertification, that work must occur outside the Corpus Generation operation and must produce new or explicitly versioned Registration Unit artifacts.

---

# Validation Strategy

Corpus Generation validation should operate in three tiers.

## Tier 1: Input Validation

Input validation confirms that selected Registration Units are explicit, resolvable, readable, and status-visible.

Validation must check:

```text
Registration Unit readiness inventory exists when required
selection manifest exists
selection policy exists
selected Registration Units are explicit
selected Registration Units are resolvable
selected Registration Units are readable
selected Registration Units expose validation status
selected Registration Units expose certification status when available
selected Registration Units preserve boundaries
```

## Tier 2: Manifest Validation

Manifest validation confirms that Corpus Generation scope is declared and reconstructable.

Validation must check:

```text
corpus_generation_id exists
corpus_generation_label exists when required
corpus_generation_purpose is declared
selection_policy_id is declared
selection_policy_version is declared when available
builder_name is declared
builder_version is declared when available
build_timestamp is declared
included Registration Units are explicit
inclusion rationale is documented
exclusion rationale is documented when applicable
producer-family summary is deterministic
package summary is deterministic
artifact count summary is deterministic
assertion registration count summary is deterministic
source identity count summary is deterministic
validation status summary is deterministic
certification status summary is deterministic
manifest is deterministic
manifest reconstructs exact selected Registration Unit set
```

## Tier 3: Anti-Collapse Validation

Anti-collapse validation confirms that Corpus Generation construction did not exceed its layer authority.

Validation must check:

```text
Registration Unit boundaries are preserved
Corpus Generation does not mutate Registration Units
Corpus Generation does not become source truth
Corpus Generation does not create Assertion Records
Corpus Generation does not derive Evidence Topology
Corpus Generation does not characterize Convergence Geometry
Corpus Generation does not declare surface eligibility
Corpus Generation does not determine surface disclosure
Corpus Generation does not emit replacement projections
Corpus Generation does not perform biological reasoning
```

---

# MARK Benchmark Validation

For the initial MARK Phase 4 benchmark corpus, validation should additionally confirm:

```text
expected six Registration Units are present
expected four VAP Registration Units are present
expected two GSC Registration Units are present
all expected Registration Units are readable
all expected Registration Units expose validation status
all expected Registration Units expose certification status
all expected Registration Units are certified
corpus_generation_id is stable
selection policy is stable
corpus manifest is deterministic
downstream Assertion Record input manifest is deterministic
```

The initial benchmark Corpus Generation should fail validation if expected Registration Units are missing unless the validation policy explicitly declares failure-mode testing.

---

# Determinism Requirements

Corpus Generation outputs must be deterministic under fixed inputs.

Given the same:

```text
Registration Unit readiness inventory
Corpus Generation selection manifest
selection policy
validation policy
contract version
builder version
Registration Unit contents
```

the builder should produce equivalent:

```text
included Registration Unit list
excluded Registration Unit list when applicable
inclusion rationale records
exclusion rationale records when applicable
summary counts
validation status summaries
certification status summaries
manifest records
validation outcomes
report sections
downstream Assertion Record input manifest
```

Filesystem traversal order must not define Corpus Generation scope.

Output order should be stable.

Recommended ordering:

```text
explicit selection manifest order
```

with stable identity verification for each included Registration Unit.

If alternate sorted output is needed, it should sort by:

```text
producer_family
registration_unit_label
registration_unit_id
```

and the sorting policy must be declared.

---

# Reconstruction Requirements

A Corpus Generation artifact must support reconstruction of:

```text
which Registration Units were selected
which Registration Units were excluded when relevant
which paths or references were used
which selection policy was applied
which validation policy was applied
which inclusion rationale was used
which exclusion rationale was used when applicable
which producer families were represented
which evidence domains were represented
which packages were represented
which artifact counts were observed
which assertion registration counts were observed
which source identity counts were observed
which validation statuses were observed
which certification statuses were observed
which builder produced the manifest
which build timestamp was used
which manifest schema version was used when available
which downstream input manifest was emitted
```

A Corpus Generation artifact must preserve enough information for downstream Assertion Record indexing, topology derivation, geometry derivation, surface construction, projection generation, and reconstruction.

---

# Relationship To Registration Units

Registration Units are inputs to Corpus Generations.

The responsibility boundary is:

```text
Registration Unit implementation
    verifies that individual Registration Units are readable, traceable,
    status-visible, non-mutated, and safe to consume

Corpus Generation implementation
    declares which Registration Units are selected together as a build scope
```

A Corpus Generation may include multiple Registration Units.

A Registration Unit may participate in multiple Corpus Generations.

Corpus Generations must preserve Registration Unit identities.

Corpus Generations must not erase Registration Unit boundaries.

---

# Relationship To Assertion Record Indexing

Corpus Generations provide the evidence scope for Assertion Record indexing.

A Corpus Generation should emit or support a downstream Assertion Record input manifest containing:

```text
corpus_generation_id
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id
registration_backend
assertion_registration_count when available
source_identity_count when available
validation_status
certification_status when available
```

The responsibility boundary is:

```text
Corpus Generation
    declares selected Registration Units

Assertion Record indexing
    resolves producer claims from selected Registration Units into
    corpus-indexable Assertion Records
```

Corpus Generation construction must not create Assertion Records.

The downstream input manifest is not an Assertion Record index.

---

# Relationship To Downstream Derived Layers

Corpus Generations provide the declared input scope for:

```text
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
RDGP-facing consumer projections
```

Downstream derived layers must preserve Corpus Generation lineage.

Corpus Generation construction must not perform downstream derivation.

The following must not occur inside Corpus Generation implementation:

```text
Assertion Record construction
Evidence Topology relationship derivation
Convergence Geometry feature construction
Evidence Convergence Surface eligibility declaration
Evidence Convergence Surface disclosure decision
Projection View generation that replaces Corpus Generation
RDGP reasoning
biological interpretation
```

---

# Anti-Collapse Safeguards

Implementation must prevent:

```text
corpus scope collapse
Registration Unit boundary collapse
producer-family collapse
package identity collapse
artifact identity collapse
assertion registration collapse
source identity collapse
namespace collapse
validation status collapse
certification status collapse
inclusion rationale collapse
exclusion rationale collapse
Corpus Generation treated as source truth
materialized corpus treated as source truth
uncertified Registration Units silently included in a certified corpus
Registration Units merged without preserved boundaries
topology derived before corpus scope is declared
topology relationships created inside Corpus Generation
geometry created inside Corpus Generation
surface eligibility declared inside Corpus Generation
projection output replacing Corpus Generation
biological reasoning performed inside Corpus Generation
destructive modification of Registration Units during Corpus Generation construction
```

Any implementation that performs one of these actions violates this plan and the Corpus Generation contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Registration Unit inventories before running against the MARK set.

Recommended tests include:

```text
test_corpus_generation_requires_explicit_selection_manifest
test_corpus_generation_requires_selection_policy
test_corpus_generation_rejects_missing_registration_unit
test_corpus_generation_rejects_unreadable_registration_unit
test_corpus_generation_preserves_registration_unit_boundaries
test_corpus_generation_preserves_inclusion_rationale
test_corpus_generation_preserves_exclusion_rationale_when_applicable
test_corpus_generation_does_not_promote_certification_status
test_corpus_generation_built_from_certified_units_is_not_auto_certified
test_corpus_generation_manifest_is_deterministic
test_corpus_generation_summary_counts_are_deterministic
test_corpus_generation_emits_downstream_assertion_record_input_manifest
test_corpus_generation_does_not_mutate_registration_units
test_corpus_generation_does_not_create_assertion_records
test_corpus_generation_does_not_create_topology
```

MARK integration tests should confirm:

```text
expected six Registration Unit paths are selected
expected four VAP Registration Units are selected
expected two GSC Registration Units are selected
all expected Registration Units are readable
all expected Registration Units are certified
corpus_generation_id is stable
selection policy identity is stable
corpus manifest is deterministic
validation report is deterministic
downstream Assertion Record input manifest is deterministic
```

Tests must not require biological correctness.

Tests validate declared scope, Registration Unit preservation, determinism, traceability, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define explicit Corpus Generation selection manifest format.

2. Define initial MARK six-Registration Unit selection policy.

3. Load Registration Unit readiness inventory.

4. Validate candidate Registration Unit readiness states.

5. Apply selection policy.

6. Resolve selected Registration Unit identities.

7. Record inclusion rationale for each selected Registration Unit.

8. Record relevant exclusion rationale when applicable.

9. Build deterministic Corpus Generation manifest.

10. Build producer-family and evidence-domain summaries.

11. Build package, artifact, assertion-registration, and source-identity summaries.

12. Emit machine-readable Corpus Generation manifest.

13. Emit human-readable Corpus Generation report.

14. Emit Corpus Generation validation report.

15. Emit downstream Assertion Record input manifest.

16. Add synthetic tests.

17. Add MARK six-Registration Unit smoke test.

18. Hand off manifest to Assertion Record implementation.
```

Each step must preserve Registration Unit boundaries.

Each step must remain read-only with respect to selected Registration Units.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_corpus_generation.py \
  --selection-manifest docs/manifests/mark_phase4_corpus_6tep_v1.tsv \
  --registration-unit-inventory results/phase4/registration_units/registration_unit_inventory.tsv \
  --output-dir results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1 \
  --corpus-generation-id mark_phase4_corpus_6tep_v1 \
  --selection-policy-id mark_phase4_6tep_certified_input_policy
```

or:

```bash
python scripts/phase4/validate_corpus_generation.py \
  --corpus-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/corpus_generation_manifest.tsv \
  --output-dir results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1
```

The exact script names are not contractually fixed.

The CLI must make input scope and selection policy explicit.

---

# Expected Selection Manifest Shape

A Corpus Generation selection manifest may include:

```text
corpus_generation_id
registration_unit_label
registration_unit_path
expected_registration_unit_id when available
expected_producer_family
expected_certification_status
expected_backend
inclusion_status
inclusion_rationale
notes
```

The selection manifest declares intended Corpus Generation scope.

It is not source truth.

It does not replace Registration Unit metadata.

It must be validated against Registration Unit metadata or readiness inventory records.

---

# Expected Corpus Manifest Shape

A Corpus Generation manifest may include:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version
selection_policy_id
selection_policy_version
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id
registration_backend
validation_status
certification_status
inclusion_status
inclusion_rationale
artifact_count
assertion_registration_count
source_identity_count
namespace_count
builder_name
builder_version
build_timestamp
manifest_schema_version
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Expected Downstream Assertion Record Input Manifest Shape

A downstream Assertion Record input manifest may include:

```text
corpus_generation_id
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id
registration_backend
assertion_registration_count
source_identity_count
validation_status
certification_status
```

This manifest exists to make downstream Assertion Record indexing deterministic.

It must not contain Assertion Records unless explicitly produced by the Assertion Record implementation.

---

# Exit Criteria

The Corpus Generation implementation plan is complete when:

```text
explicit Corpus Generation selection manifest can be declared
selection policy is declared
Corpus Generation identity is stable
included Registration Units are explicit
included Registration Units are resolvable
included Registration Units are readable
Registration Unit boundaries are preserved
producer-family context is preserved
package identity is preserved
artifact counts are recorded when available
assertion registration counts are recorded when available
source identity counts are recorded when available
validation status is visible
certification status is visible when available
inclusion rationale is documented
exclusion rationale is documented when applicable
machine-readable Corpus Generation manifest is emitted
human-readable Corpus Generation report is emitted
Corpus Generation validation report is emitted
downstream Assertion Record input manifest is emitted
outputs are deterministic under fixed inputs
Corpus Generation does not mutate Registration Units
Corpus Generation does not become source truth
Corpus Generation can serve as input to Assertion Record indexing
anti-collapse safeguards pass
```

This implementation is not complete merely because a file list exists.

It is complete only when the declared Corpus Generation satisfies the Corpus Generation contract and can safely define the evidence universe for downstream Phase 4 derivation.

---

# Summary

The Corpus Generation implementation plan establishes the Phase 4 evidence-scope declaration layer.

The governing distinction is:

```text
Registration Units preserve custody.

Registration Unit readiness verifies safe consumption.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.
```

The guiding rule is:

```text
Declare the scope.

Apply policy.

Preserve Registration Unit boundaries.

Document inclusion.

Document exclusion.

Emit deterministic manifests.

Do not mutate.

Do not derive.

Do not interpret.
```

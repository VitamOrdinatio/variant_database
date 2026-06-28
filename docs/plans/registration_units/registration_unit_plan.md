# Registration Unit Implementation Plan

## Purpose

This document defines the implementation plan for Phase 4 Registration Unit consumption in VDB.

Registration Units are the durable custody boundary between producer TEP ingestion and Phase 4 derived evidence architecture.

This plan describes how Phase 4 builders will discover, inspect, validate, inventory, and consume existing Registration Units as read-only checkpoint inputs for downstream Corpus Generation construction and Assertion Record indexing.

This plan does not define how producer TEPs are ingested or registered.

That responsibility belongs to earlier ingestion, persistence, and registration implementation work.

The Phase 4 Registration Unit implementation goal is:

```text
Safely consume certified Registration Units as traceable, readable,
non-mutated inputs for downstream Phase 4 derivation.
```

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/registration_units/registration_unit_contract.md
```

The governing contract states that a Registration Unit must remain:

```text
traceable
readable
non-destructive
storage-neutral
producer-aware
namespace-preserving
assertion-preserving
source-identity-preserving
certification-aware
reconstructable
```

This plan is subordinate to the contract.

If this plan conflicts with the Registration Unit contract or the VDB system contract, the contracts take precedence.

---

# Implementation Role

The Registration Unit implementation role in Phase 4 is to provide a read-only readiness and inventory layer over existing registered producer evidence packages.

A Phase 4 Registration Unit implementation answers:

```text
Can this accepted producer evidence package be safely consumed as a
traceable, readable, non-mutated, status-visible input for downstream
Phase 4 work?
```

It does not answer:

```text
Which Registration Units belong in a Corpus Generation?

What scientific claims should be indexed as Assertion Records?

What topology emerges from the corpus?

What convergence geometry exists?

Which surfaces should be exposed?

What projections should consumers receive?

What biological meaning should downstream systems infer?
```

Those questions belong to downstream implementation plans.

---

# Non-Goals

This plan does not implement:

```text
producer TEP ingestion
Registration Unit creation from raw producer packages
Registration Unit repair
Registration Unit migration
Registration Unit recertification
Corpus Generation selection
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View generation
RDGP reasoning
biological interpretation
```

This plan must not reopen Phase 3.

Phase 4 may inspect Registration Units.

Phase 4 must not mutate Registration Units.

---

# Initial Implementation Target

The initial implementation target is the certified Phase 3 MARK Registration Unit set.

Current MARK Registration Units are represented as SQLite databases at paths such as:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

These Registration Units are checkpointed Phase 4 inputs.

The initial implementation should produce a deterministic readiness inventory over these inputs without modifying them.

The initial target artifact class may be referred to as:

```text
registration_unit_readiness_index
```

This readiness index is not a Corpus Generation.

It is an implementation-supporting inventory that makes Corpus Generation construction safer and more deterministic.

---

# Inputs

The initial Registration Unit implementation consumes:

```text
Registration Unit path list
Registration Unit contract version
system contract version
Registration Unit inspection policy
Registration Unit validation policy
builder name
builder version
execution timestamp
```

For SQLite-backed Registration Units, each input path should point to a `vdb.sqlite` Registration Unit.

Input paths may come from:

```text
explicit manifest
configured path list
repository-local fixture
MARK Phase 3 canonical path list
future discovery mechanism
```

Implicit filesystem discovery must not silently define authoritative Registration Unit scope.

If discovery is used, the discovered candidate set must be emitted and reviewed as an inventory input.

---

# Outputs

The Registration Unit implementation should emit sidecar artifacts outside the certified Registration Units.

Expected outputs may include:

```text
registration_unit_inventory.tsv
registration_unit_inventory.json
registration_unit_readiness_report.md
registration_unit_validation_report.json
registration_unit_validation_report.tsv
```

These outputs are implementation-supporting sidecars.

They do not replace Registration Units.

They do not create source authority.

They do not define Corpus Generation scope.

They do not become Assertion Records.

They do not derive topology, geometry, surfaces, or projections.

---

# Recommended Output Location

Initial Phase 4 outputs may be written under a path such as:

```text
results/phase4/registration_units/
```

or another explicitly declared VDB results path.

The output location should be configurable.

Output paths must not be confused with Registration Unit source paths.

A recommended initial layout is:

```text
results/phase4/registration_units/
    registration_unit_inventory.tsv
    registration_unit_inventory.json
    registration_unit_readiness_report.md
    registration_unit_validation_report.json
    registration_unit_validation_report.tsv
```

---

# Required Builder Behavior

A Registration Unit readiness builder must:

```text
accept an explicit Registration Unit input list
open each Registration Unit in read-only mode when supported
inspect required Registration Unit metadata
inspect required preserved domains
record backend representation
record validation status
record certification status when available
record package identity
record artifact inventory summary
record assertion registration inventory summary
record source identity inventory summary
record namespace inventory summary
record provenance availability
emit deterministic inventories
emit deterministic validation reports
emit human-readable readiness reports
```

The builder must not:

```text
modify Registration Unit files
rewrite Registration Unit metadata
repair Registration Unit records in place
migrate Registration Unit schemas in place
delete records
insert records
change validation status
change certification status
replace source identities with canonical identities
create Assertion Records inside the Registration Unit
derive topology inside the Registration Unit
derive geometry inside the Registration Unit
create surface memberships inside the Registration Unit
emit projections that replace Registration Units
```

If a Registration Unit fails readiness inspection, the builder should report the failure and continue or halt according to the declared validation policy.

Failure handling must be deterministic.

---

# Read-Only Consumption Requirements

Phase 4 Registration Unit inspection must be read-only.

For SQLite-backed Registration Units, implementation should use read-only database access where supported.

A builder should avoid access modes that can:

```text
create journal files
mutate database metadata
modify schema
modify rows
update indexes
vacuum or optimize the database
write temporary state into the Registration Unit directory
```

If a read-only mode is unavailable in a local environment, the builder must still avoid intentional writes and must document the limitation.

Any derived sidecar artifact must be emitted outside the certified Registration Unit.

Registration Unit inspection must not change file contents.

When feasible, validation may compare pre-inspection and post-inspection file metadata or checksums to confirm non-mutation.

---

# Required Inspection Domains

The Registration Unit builder should inspect the following domains when available:

```text
Registration Unit identity
source package identity
producer family
producer repository
producer run or release
TEP package metadata
artifact registrations
assertion registrations
source identities
source namespaces
evidence domains
assertion types
authority context
uncertainty context
surface-relevant roles when declared
provenance records
validation status
certification status
schema metadata
backend metadata
```

The builder should also inspect implementation-supporting records when present:

```text
metadata records
entity records
Evidence Object records
Evidence State records
Evidence State Transition records
registration reports
validation reports
certification reports
```

Inspection of implementation-supporting records must not allow those records to supersede Assertion Record primacy.

---

# Required Inventory Fields

A machine-readable Registration Unit inventory should preserve, when available:

```text
registration_unit_id
registration_unit_label
registration_unit_path
registration_backend
registration_backend_version
producer_family
source_package_id
source_package_path
source_package_checksum
producer_repository
producer_run_id
producer_release_id
registration_created_at
registration_created_by
validation_status
certification_status
contract_version
schema_version
artifact_count
assertion_registration_count
source_identity_count
namespace_count
evidence_domain_count
assertion_type_count
provenance_record_count
validation_report_reference
certification_report_reference
readiness_status
readiness_failure_reason
inspection_timestamp
builder_name
builder_version
```

If a field cannot be resolved, the inventory should explicitly indicate the state.

Allowed unresolved states may include:

```text
not_available
not_applicable
not_reported
unresolved
ambiguous
conflicted
inspection_failed
```

Missing values must not silently masquerade as negative evidence.

---

# Required Readiness Status

Registration Unit readiness status may include:

```text
ready
ready_with_note
provisional
failed
rejected
not_evaluated
```

Suggested semantics:

```text
ready
    The Registration Unit passed required readiness checks and may be used as a
    candidate input for Corpus Generation.

ready_with_note
    The Registration Unit passed required readiness checks but has documented
    caveats that downstream builders should preserve.

provisional
    The Registration Unit is usable for fixture or development work but is not
    appropriate for certified Phase 4 derivation.

failed
    The Registration Unit failed required inspection or validation checks.

rejected
    The Registration Unit is explicitly unsuitable for downstream use under the
    declared policy.

not_evaluated
    The Registration Unit was listed but not inspected.
```

Readiness status is not the same as certification status.

A readiness report must not silently promote a Registration Unit to certified.

---

# Validation Strategy

Registration Unit validation should operate in two tiers.

## Tier 1: Representation-Level Validation

Representation-level validation confirms the backend can be inspected.

For SQLite-backed Registration Units, validation may check:

```text
file exists
file is readable
SQLite connection succeeds
read-only access succeeds when supported
required tables exist
required indexes exist when applicable
schema metadata is available when applicable
referential integrity holds when applicable
row counts are internally consistent when applicable
```

SQLite-specific checks are implementation validation checks.

They do not redefine the Registration Unit architecture.

## Tier 2: Contract-Level Validation

Contract-level validation confirms the Registration Unit satisfies architectural obligations.

Validation must check:

```text
Registration Unit identity exists
Registration Unit identity is stable
producer family is declared
source package identity is preserved
source package reference resolves when applicable
artifact registrations exist
assertion registrations exist
source identities exist where expected
source namespaces are preserved
artifact references resolve when applicable
assertion registration references resolve when applicable
source identity references resolve when applicable
provenance is reconstructable
validation status is visible
certification status is visible when available
Registration Unit representation is declared
inspection does not mutate the Registration Unit
```

Validation must also confirm that no prohibited derived-layer behavior occurred inside the Registration Unit.

---

# Certification-Aware Behavior

Current MARK heavy Phase 4 work should prefer Registration Units with status:

```text
certified
```

Development fixtures may use provisional or validated Registration Units if their status is explicit.

The readiness builder must preserve Registration Unit certification status exactly as reported.

The readiness builder must not infer certification from readability alone.

The readiness builder must not promote:

```text
validated → certified
provisional → certified
uncertified → certified
```

If certification evidence is missing, the inventory must expose that limitation.

---

# Determinism Requirements

Registration Unit readiness outputs must be deterministic under fixed inputs.

Given the same:

```text
Registration Unit input list
Registration Unit contents
inspection policy
validation policy
contract version
builder version
execution environment assumptions
```

the builder should produce equivalent:

```text
inventory records
readiness statuses
validation summaries
report contents
```

Determinism requirements include:

```text
stable sorting by Registration Unit identity or input order
stable unresolved-state vocabulary
stable validation status vocabulary
stable report section ordering
stable count semantics
stable error handling under declared policy
```

Filesystem traversal order must not define output order.

If filesystem metadata such as modification time is recorded, it must be labeled as an environmental observation rather than Registration Unit identity.

---

# Reconstruction Requirements

A Registration Unit readiness artifact must support reconstruction of:

```text
which Registration Units were inspected
which paths or references were used
which backend representation was declared
which producer family each unit represented
which source package each unit preserved
which artifacts were registered
which assertion registrations were available
which source identities were available
which namespaces were preserved
which validation status was reported
which certification status was reported
which inspection policy was used
which validation policy was used
which builder produced the inventory
which readiness status was assigned
which limitations were observed
```

The readiness artifact must preserve enough information for the Corpus Generation layer to select Registration Units without re-discovering or mutating them.

---

# Relationship To Corpus Generation

The Registration Unit implementation prepares candidate inputs for Corpus Generation.

The responsibility boundary is:

```text
Registration Unit implementation
    verifies that individual Registration Units are readable, traceable,
    status-visible, and safe to consume

Corpus Generation implementation
    declares which Registration Units are selected together as a build scope
```

The Registration Unit readiness inventory may indicate eligibility or readiness.

It must not silently declare Corpus Generation scope.

A Registration Unit may appear in multiple Corpus Generations.

A Corpus Generation must preserve the identity of each selected Registration Unit.

---

# Relationship To Assertion Record Indexing

Registration Units preserve assertion registrations.

Assertion Record indexing constructs or resolves corpus-indexable Assertion Records from selected Registration Units.

The Registration Unit implementation must verify that assertion-registration material is present and traceable.

It must not construct the final Assertion Record index.

It may emit counts and references that help downstream Assertion Record indexing validate completeness.

Any assertion-registration summary emitted by this plan must remain traceable to the Registration Unit and must not replace Assertion Records.

---

# Relationship To Downstream Derived Layers

Registration Units do not derive downstream evidence structure.

The following must not occur inside Registration Unit implementation:

```text
Evidence Topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
Projection View generation that replaces Registration Units
RDGP reasoning
biological interpretation
cross-producer convergence inference
cross-modality convergence inference
```

Downstream derived layers must preserve Registration Unit lineage through Assertion Records, topology, geometry, surfaces, and projections.

---

# Anti-Collapse Safeguards

Implementation must prevent:

```text
Registration Unit boundary collapse
producer identity collapse
source package identity collapse
artifact identity collapse
assertion registration collapse
source identity collapse
source namespace collapse
authority collapse
uncertainty collapse
validation status collapse
certification status collapse
canonical identity replacing source identity
sidecar inventory treated as source truth
readiness status treated as certification status
Registration Unit inventory treated as Corpus Generation scope
Registration Unit summary treated as Assertion Record index
topology created inside Registration Unit inspection
geometry created inside Registration Unit inspection
surface membership created inside Registration Unit inspection
projection output replacing a Registration Unit
biological reasoning performed during Registration Unit inspection
```

Any implementation that performs one of these actions violates this plan and the Registration Unit contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Registration Units before running against the MARK set.

Recommended tests include:

```text
test_registration_unit_inventory_accepts_explicit_input_list
test_registration_unit_inventory_is_deterministic
test_registration_unit_readiness_preserves_input_order_or_stable_sort
test_registration_unit_readiness_reports_missing_file
test_registration_unit_readiness_reports_unreadable_backend
test_registration_unit_readiness_detects_missing_required_tables_when_sqlite
test_registration_unit_readiness_reports_missing_identity
test_registration_unit_readiness_reports_missing_package_identity
test_registration_unit_readiness_reports_missing_assertion_registrations
test_registration_unit_readiness_reports_missing_source_identities_when_expected
test_registration_unit_readiness_preserves_certification_status
test_registration_unit_readiness_does_not_promote_certification_status
test_registration_unit_readiness_emits_machine_readable_inventory
test_registration_unit_readiness_emits_human_readable_report
test_registration_unit_inspection_does_not_mutate_sqlite_file_when_checkable
```

MARK integration tests should confirm:

```text
expected six Registration Unit paths are inspected
all expected Registration Units are readable
all expected Registration Units expose producer family
all expected Registration Units expose package identity
all expected Registration Units expose assertion registrations
all expected Registration Units expose source identities where expected
all expected Registration Units expose certification status
inventory output is deterministic
readiness report is deterministic
```

Tests must not require biological correctness.

Tests validate custody, readability, traceability, status visibility, and non-mutation.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define explicit Registration Unit input manifest format.

2. Implement read-only Registration Unit opener.

3. Implement backend representation inspection.

4. Implement identity and package metadata extraction.

5. Implement artifact registration inventory extraction.

6. Implement assertion registration inventory extraction.

7. Implement source identity and namespace inventory extraction.

8. Implement validation and certification status extraction.

9. Implement deterministic inventory writer.

10. Implement readiness report writer.

11. Implement validation report writer.

12. Add synthetic tests.

13. Add MARK six-Registration Unit smoke test.

14. Hand off readiness inventory to Corpus Generation implementation.
```

Each step should remain read-only with respect to Registration Units.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_registration_unit_inventory.py \
  --input-manifest docs/manifests/mark_phase3_registration_units.tsv \
  --output-dir results/phase4/registration_units \
  --contract-version <version>
```

or:

```bash
python scripts/phase4/validate_registration_units.py \
  --input-manifest docs/manifests/mark_phase3_registration_units.tsv \
  --output-dir results/phase4/registration_units
```

The exact script names are not contractually fixed.

The CLI must make input scope explicit.

---

# Expected Input Manifest Shape

A Registration Unit input manifest may include:

```text
registration_unit_label
registration_unit_path
expected_producer_family
expected_certification_status
expected_backend
notes
```

The input manifest is an operator declaration of candidate Registration Unit paths.

It is not a Corpus Generation.

It is not source truth.

It does not replace Registration Unit metadata.

---

# Expected Inventory Shape

A Registration Unit inventory may include:

```text
registration_unit_id
registration_unit_label
registration_unit_path
producer_family
source_package_id
registration_backend
validation_status
certification_status
artifact_count
assertion_registration_count
source_identity_count
namespace_count
readiness_status
readiness_failure_reason
builder_name
builder_version
inspection_timestamp
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Exit Criteria

The Registration Unit implementation plan is complete when:

```text
explicit Registration Unit inputs can be declared
Registration Units can be opened read-only when supported
Registration Unit representation is recorded
Registration Unit identity is extracted or unresolved state is explicit
source package identity is extracted or unresolved state is explicit
producer family is extracted or unresolved state is explicit
artifact registrations are inventoried
assertion registrations are inventoried
source identities are inventoried where expected
source namespaces are inventoried where expected
validation status is visible
certification status is visible when available
readiness status is assigned under declared policy
machine-readable inventory is emitted
human-readable readiness report is emitted
validation report is emitted
outputs are deterministic under fixed inputs
inspection does not mutate Registration Units
sidecar outputs do not replace Registration Units
Registration Units are selectable by Corpus Generation
anti-collapse safeguards pass
```

This implementation is not complete merely because a file path list exists.

It is complete only when the inspected Registration Units satisfy the Registration Unit contract well enough to serve as safe Phase 4 checkpoint inputs.

---

# Summary

The Registration Unit implementation plan establishes the read-only Phase 4 consumption posture for registered producer evidence packages.

The governing distinction is:

```text
Registration Units preserve custody.

Registration Unit readiness verifies safe consumption.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.
```

The guiding rule is:

```text
Inspect read-only.

Record readiness.

Preserve custody.

Emit sidecars.

Do not mutate.

Do not derive.

Do not interpret.
```

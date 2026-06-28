# Registration Unit Schema

## Purpose

This document defines the Phase 4 Registration Unit schema for the Variant Database (VDB).

The purpose of this schema is to define how Phase 4 declares, inspects, inventories, validates, and references existing Registration Units as read-only checkpoint inputs for downstream Corpus Generation construction and Assertion Record indexing.

A Registration Unit is the durable custody boundary between producer TEP ingestion and Phase 4 derived evidence architecture.

This schema governs the Phase 4 consumption-facing representation of Registration Units.

It does not define producer TEP ingestion.

It does not define the physical storage schema of Phase 3 registration databases.

It does not define Corpus Generation scope.

It does not create Assertion Records.

It does not derive Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, or Projection Views.

---

# Schema Role

The Registration Unit schema defines the logical records emitted by Phase 4 Registration Unit inspection.

The central schema object is:

```text
registration_unit_inventory_record
```

A Registration Unit inventory record answers:

```text
Was this declared Registration Unit inspected under a declared policy,
using a declared builder, in a declared execution context, and is it safe
to consume as a traceable, readable, non-mutated, status-visible Phase 4 input?
```

A Registration Unit inventory record is an inspection-sidecar record.

It is not the Registration Unit itself.

It is not source truth.

It is not certification evidence by itself.

It is not Corpus Generation scope.

It is not an Assertion Record index.

---

# Non-Goals

This schema does not define:

```text
producer TEP payload schemas
producer package schemas
raw VAP artifact schemas
raw GSC artifact schemas
Phase 3 ingestion tables
Phase 3 registration database DDL
SQLite table definitions for registered package storage
Registration Unit repair
Registration Unit migration
Registration Unit recertification
Corpus Generation manifests
Assertion Record index records
Evidence Topology records
Convergence Geometry records
Evidence Convergence Surface records
Projection View records
RDGP reasoning outputs
biological interpretation
```

This schema must not reopen Phase 3.

Phase 4 may inspect Registration Units.

Phase 4 must not mutate Registration Units.

---

# Governed Artifacts

This schema governs the following Phase 4 Registration Unit artifacts:

```text
registration_unit_input_manifest.tsv
registration_unit_input_manifest.json when policy-enabled
registration_unit_inventory.tsv
registration_unit_inventory.json
registration_unit_readiness_report.md
registration_unit_validation_report.json
registration_unit_validation_report.tsv
```

Recommended output location:

```text
results/phase4/registration_units/
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

---

# File Format Conventions

## TSV

TSV files provide compact, operator-readable tabular records.

The canonical TSV artifact for this schema is:

```text
registration_unit_inventory.tsv
```

The TSV should include the Corpus Generation handoff minimum fields defined below.

Additional columns may be added when implementation matures, provided they do not collapse unresolved states or remove reconstruction capacity.

## JSON

JSON files provide richer machine-readable records.

The canonical JSON artifact for this schema is:

```text
registration_unit_inventory.json
```

The JSON representation may include nested domain summaries, validation metadata, inspection metadata, and non-mutation evidence.

## Markdown

Markdown reports provide human-readable inspection summaries.

The canonical Markdown artifact for this schema is:

```text
registration_unit_readiness_report.md
```

## JSONL

This schema does not require JSONL for the initial Registration Unit layer.

Registration Unit inventory is expected to be represented as TSV plus JSON.

JSONL may be added later if implementation emits row-oriented per-domain inspection streams.

---

# Registration Unit Input Manifest Schema

The Registration Unit input manifest declares candidate Registration Unit paths or references for inspection.

The input manifest is an operator declaration.

It is not Corpus Generation scope.

It is not source truth.

It does not replace Registration Unit metadata.

It does not certify Registration Units.

## Required Input Manifest Fields

| Field                           |    Required | Description                                                                 |
| ------------------------------- | ----------: | --------------------------------------------------------------------------- |
| `registration_unit_label`       |         yes | Human-readable label for the candidate Registration Unit.                   |
| `registration_unit_reference`   | recommended | Backend-neutral reference to the candidate Registration Unit.               |
| `registration_unit_path`        | conditional | Filesystem path when the Registration Unit is path-backed.                  |
| `expected_registration_unit_id` |    optional | Expected stable Registration Unit identifier, when known before inspection. |
| `expected_producer_family`      | recommended | Expected producer family, such as `VAP` or `GSC`.                           |
| `expected_certification_status` | recommended | Expected certification status, when known.                                  |
| `expected_backend`              | recommended | Expected backend representation, such as `sqlite`.                          |
| `fixture_class`                 |         yes | Fixture class for the candidate Registration Unit.                          |
| `execution_context`             |         yes | Expected execution context for inspection.                                  |
| `notes`                         |    optional | Operator notes.                                                             |

## Input Manifest Example

```text
registration_unit_label	registration_unit_path	expected_producer_family	expected_certification_status	expected_backend	fixture_class	execution_context	notes
gsc_epilepsy	results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite	GSC	certified	sqlite	MARK_certified_registration_unit	MARK	Phase 3 certified MARK input
vap_hg002	results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite	VAP	certified	sqlite	MARK_certified_registration_unit	MARK	HG002 reference specimen
local_fixture	tests/fixtures/phase4/registration_units/local_golden/vdb.sqlite	VAP	provisional	sqlite	local_golden_fixture	local	Local development fixture
```

## Input Manifest Rules

The input manifest must make inspection scope explicit.

Implicit filesystem discovery must not silently define authoritative Registration Unit scope.

If filesystem discovery is used, the discovered candidate set must be emitted as a reviewable input manifest before downstream inspection becomes authoritative.

Fields prefixed with `expected_` are validation expectations.

They must not override inspected Registration Unit metadata.

---

# Registration Unit Inventory Record Schema

A Registration Unit inventory record is the canonical Phase 4 inspection record for one declared Registration Unit.

The record must preserve:

```text
Registration Unit identity
backend representation
producer identity
source package identity
inspection context
readiness status
validation status
certification status
domain summaries
non-mutation evidence
builder identity
reconstruction handles
```

## Required Inventory Fields

| Field                            |    Required | Description                                                                           |
| -------------------------------- | ----------: | ------------------------------------------------------------------------------------- |
| `registration_unit_id`           |         yes | Stable Registration Unit identifier, or explicit unresolved state.                    |
| `registration_unit_label`        |         yes | Human-readable Registration Unit label.                                               |
| `registration_unit_reference`    | recommended | Backend-neutral reference to the Registration Unit.                                   |
| `registration_unit_path`         | conditional | Filesystem path when path-backed.                                                     |
| `registration_backend`           |         yes | Backend representation, such as `sqlite`, `relational`, `object_store`, or `unknown`. |
| `registration_backend_version`   | recommended | Backend version when available.                                                       |
| `registration_backend_detail`    |    optional | Backend-specific detail, without making backend the architecture.                     |
| `producer_family`                |         yes | Producer family, such as `VAP`, `GSC`, `RSP`, `RDGP`, or explicit unresolved state.   |
| `source_package_id`              |         yes | Source package identifier, or explicit unresolved state.                              |
| `source_package_path`            | recommended | Source package path or resolvable package reference when available.                   |
| `source_package_checksum`        |    optional | Source package checksum when available.                                               |
| `producer_repository`            | recommended | Producer repository identifier or unresolved state.                                   |
| `producer_run_id`                | recommended | Producer run identifier when available.                                               |
| `producer_release_id`            | recommended | Producer release identifier when available.                                           |
| `registration_created_at`        | recommended | Timestamp for Registration Unit creation when available.                              |
| `registration_created_by`        | recommended | Process or tool that created the Registration Unit when available.                    |
| `contract_version`               | recommended | Registration Unit contract version when available.                                    |
| `schema_version`                 | recommended | Registration Unit schema version when available.                                      |
| `validation_status`              |         yes | Validation status exposed by the Registration Unit or inspection.                     |
| `certification_status`           |         yes | Certification status exposed by the Registration Unit or explicit unresolved state.   |
| `artifact_count`                 |         yes | Count of registered artifacts, or explicit unresolved state.                          |
| `assertion_registration_count`   |         yes | Count of assertion registrations, or explicit unresolved state.                       |
| `source_identity_count`          |         yes | Count of source identities, or explicit unresolved state.                             |
| `namespace_count`                | recommended | Count of source namespaces, or explicit unresolved state.                             |
| `evidence_domain_count`          | recommended | Count of evidence domains, or explicit unresolved state.                              |
| `assertion_type_count`           | recommended | Count of assertion types, or explicit unresolved state.                               |
| `provenance_record_count`        | recommended | Count of provenance records, or explicit unresolved state.                            |
| `validation_report_reference`    | recommended | Reference to validation evidence when available.                                      |
| `certification_report_reference` | recommended | Reference to certification evidence when available.                                   |
| `fixture_class`                  |         yes | Fixture class of the inspected Registration Unit.                                     |
| `execution_context`              |         yes | Execution context of inspection.                                                      |
| `readiness_status`               |         yes | Phase 4 readiness status assigned by inspection.                                      |
| `readiness_failure_reason`       | conditional | Required when readiness is not `ready` or `ready_with_note`.                          |
| `readiness_note`                 |    optional | Human-readable readiness note.                                                        |
| `inspection_timestamp`           |         yes | Timestamp for Phase 4 inspection.                                                     |
| `inspection_policy_id`           | recommended | Inspection policy identifier.                                                         |
| `inspection_policy_version`      | recommended | Inspection policy version.                                                            |
| `validation_policy_id`           | recommended | Validation policy identifier.                                                         |
| `validation_policy_version`      | recommended | Validation policy version.                                                            |
| `builder_name`                   |         yes | Name of builder that emitted the record.                                              |
| `builder_version`                | recommended | Builder version when available.                                                       |

## Corpus Generation Handoff Minimum

The following fields are the minimum recommended handoff fields for downstream Corpus Generation construction:

```text
registration_unit_id
registration_unit_label
registration_unit_reference
registration_unit_path
registration_backend
producer_family
source_package_id
validation_status
certification_status
artifact_count
assertion_registration_count
source_identity_count
namespace_count
readiness_status
readiness_failure_reason
fixture_class
execution_context
inspection_timestamp
builder_name
builder_version
```

Corpus Generation may require additional fields under its own schema.

The Registration Unit inventory enables Corpus Generation selection.

It does not select a Corpus Generation.

---

# Optional Domain Summary Schemas

Domain summaries support readiness assessment and downstream selection.

They do not duplicate full Registration Unit payloads.

They do not replace Registration Unit records.

They do not replace Assertion Records.

## Artifact Summary

| Field                                  | Description                                               |
| -------------------------------------- | --------------------------------------------------------- |
| `artifact_count`                       | Total registered artifact count.                          |
| `artifact_roles_present`               | Declared artifact roles when available.                   |
| `artifact_domains_present`             | Evidence domains represented by artifacts when available. |
| `artifact_reference_resolution_status` | Whether artifact references resolve under inspection.     |
| `artifact_summary_note`                | Optional note.                                            |

## Assertion Registration Summary

| Field                                 | Description                                                     |
| ------------------------------------- | --------------------------------------------------------------- |
| `assertion_registration_count`        | Total assertion registration count.                             |
| `assertion_types_present`             | Assertion types represented when available.                     |
| `relationship_classes_present`        | Registered relationship classes when available.                 |
| `participant_reference_status`        | Whether participant references are available and resolvable.    |
| `evidence_basis_reference_status`     | Whether evidence-basis references are available and resolvable. |
| `assertion_registration_summary_note` | Optional note.                                                  |

## Source Identity Summary

| Field                                  | Description                                                          |
| -------------------------------------- | -------------------------------------------------------------------- |
| `source_identity_count`                | Total source identity count.                                         |
| `source_namespaces_present`            | Namespaces represented by source identities.                         |
| `canonical_identity_attachment_status` | Whether canonical identities are separately attached when available. |
| `source_identity_resolution_status`    | Resolution status summary.                                           |
| `source_identity_ambiguity_status`     | Ambiguity status summary.                                            |
| `source_identity_conflict_status`      | Conflict status summary.                                             |
| `source_identity_summary_note`         | Optional note.                                                       |

## Namespace Summary

| Field                         | Description                               |
| ----------------------------- | ----------------------------------------- |
| `namespace_count`             | Total namespace count.                    |
| `namespace_labels_present`    | Namespace labels represented.             |
| `namespace_types_present`     | Namespace types when available.           |
| `namespace_resolution_status` | Resolution status summary when available. |
| `namespace_summary_note`      | Optional note.                            |

## Provenance Summary

| Field                             | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `provenance_record_count`         | Total provenance record count.               |
| `registration_process`            | Registration process or tool when available. |
| `registration_process_version`    | Registration process version when available. |
| `registration_timestamp`          | Registration timestamp when available.       |
| `input_package_reference_status`  | Whether input package reference resolves.    |
| `input_artifact_reference_status` | Whether input artifact references resolve.   |
| `provenance_summary_note`         | Optional note.                               |

---

# Readiness Status Vocabulary

Registration Unit readiness status is assigned by Phase 4 inspection.

Readiness status is not certification status.

Allowed values:

```text
ready
ready_with_note
provisional
failed
rejected
not_evaluated
```

## Status Semantics

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

Readiness status must not silently promote a Registration Unit to certified.

---

# Validation Status And Certification Status

Registration Unit inspection must preserve validation and certification status exactly as observed.

The readiness builder must not infer certification from readability.

The readiness builder must not promote:

```text
validated → certified
provisional → certified
uncertified → certified
not_reported → certified
```

## Certification Status Vocabulary

Allowed certification status values include:

```text
certified
validated
provisional
uncertified
rejected
not_available
not_reported
unresolved
inspection_failed
```

## Validation Status Vocabulary

Allowed validation status values include:

```text
passed
passed_with_note
failed
not_available
not_reported
not_evaluated
unresolved
inspection_failed
```

If existing Registration Units expose a different status vocabulary, the inventory must either:

```text
preserve the source status verbatim
```

or:

```text
map the source status to this schema and preserve the original value in a source-status field
```

Recommended fields:

```text
validation_status
validation_status_source_value
certification_status
certification_status_source_value
```

---

# Unresolved-State Vocabulary

Missing or unresolved values must be explicit.

Allowed unresolved states include:

```text
not_available
not_applicable
not_reported
unresolved
ambiguous
conflicted
inspection_failed
unknown
```


These values must not be collapsed into blank strings.

Missing values must not silently masquerade as:

```text
absence
negative evidence
zero count
not relevant
validation failure
certification failure
```

When a count cannot be resolved, the field should use an explicit unresolved value rather than `0`.

A value of `0` means the inspected Registration Unit reported zero records for that domain.

A value of `not_reported` means the domain count was not reported.

---

# Read-Only And Non-Mutation Schema Fields

Phase 4 inspection must not mutate Registration Units.

The schema therefore includes non-mutation evidence fields.

| Field                        |    Required | Description                                                                                     |
| ---------------------------- | ----------: | ----------------------------------------------------------------------------------------------- |
| `inspection_access_mode`     | recommended | Access mode used for inspection, such as `read_only`, `best_effort_non_mutating`, or `unknown`. |
| `read_only_open_status`      | recommended | Whether read-only open succeeded when supported.                                                |
| `sidecar_output_status`      | recommended | Whether all emitted artifacts were written outside the Registration Unit path.                  |
| `pre_inspection_size_bytes`  |    optional | File size before inspection when path-backed and available.                                     |
| `post_inspection_size_bytes` |    optional | File size after inspection when path-backed and available.                                      |
| `pre_inspection_mtime`       |    optional | Modification time before inspection when available.                                             |
| `post_inspection_mtime`      |    optional | Modification time after inspection when available.                                              |
| `checksum_method`            |    optional | Method used for checksum or non-mutation evidence.                                              |
| `pre_inspection_checksum`    |    optional | Pre-inspection checksum when computed.                                                          |
| `post_inspection_checksum`   |    optional | Post-inspection checksum when computed.                                                         |
| `non_mutation_check_status`  | recommended | Result of non-mutation check.                                                                   |
| `non_mutation_check_note`    |    optional | Explanation of limitation or observation.                                                       |

## Inspection Access Mode Vocabulary

Allowed values:

```text
read_only
best_effort_non_mutating
read_only_unavailable
not_applicable
unknown
inspection_failed
```

## Checksum Method Vocabulary

Allowed values:

```text
not_performed
stat_only
checksum_compare
backend_read_only_guarantee
unavailable
not_applicable
```

## Non-Mutation Check Status Vocabulary

Allowed values:

```text
passed
passed_with_note
not_performed
failed
unavailable
not_applicable
inspection_failed
```

For large MARK SQLite files, full checksum comparison may be expensive.

A schema-compliant inspection may therefore use `stat_only` or `backend_read_only_guarantee` when declared by policy.

The chosen method must be explicit.

---

# Fixture And Execution Context Fields

Registration Unit inspection must distinguish local development fixtures from certified MARK Registration Units.

## Fixture Class Vocabulary

Allowed values:

```text
synthetic_fixture
local_golden_fixture
MARK_certified_registration_unit
MARK_development_registration_unit
future_fixture
unknown
```

## Execution Context Vocabulary

Allowed values:

```text
local
MARK
CI
manual
unknown
```

## Recommended Execution Fields

| Field                       | Description                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| `fixture_class`             | Declares fixture or certified-input class.                                                  |
| `execution_context`         | Declares execution context.                                                                 |
| `host_context`              | Optional host or environment label.                                                         |
| `expected_storage_location` | Optional storage-location expectation, such as local repo fixture or MARK result path.      |
| `is_heavy_smoketest_input`  | Boolean-like field indicating whether this record is intended for heavy MARK smoketest use. |

Local golden fixtures may be provisional.

MARK heavy Phase 4 smoketests should use Registration Units with explicit certified status.

A local fixture must not masquerade as a certified MARK Registration Unit.

---

# Validation Report Shape

The Registration Unit validation report records whether declared Registration Units satisfy inspection and contract-level readiness requirements.

The validation report should include:

```text
validation_report_id
validation_report_label
input_manifest_reference
inventory_reference
validation_policy_id
validation_policy_version
inspection_policy_id
inspection_policy_version
builder_name
builder_version
validation_timestamp
overall_validation_status
record_count
ready_count
ready_with_note_count
provisional_count
failed_count
rejected_count
not_evaluated_count
mutation_check_pass_count
mutation_check_failed_count
certified_count
uncertified_count
validation_findings
validation_limitations
```

The TSV validation report may represent one validation finding per row.

The JSON validation report may include nested findings grouped by Registration Unit.

## Validation Finding Fields

| Field                     | Description                                     |
| ------------------------- | ----------------------------------------------- |
| `finding_id`              | Stable finding identifier when available.       |
| `registration_unit_id`    | Registration Unit identity or unresolved state. |
| `registration_unit_label` | Human-readable label.                           |
| `finding_type`            | Type of validation finding.                     |
| `finding_severity`        | Severity of the finding.                        |
| `finding_status`          | Status of the finding.                          |
| `field_name`              | Field affected when applicable.                 |
| `observed_value`          | Observed value when useful.                     |
| `expected_value`          | Expected value when useful.                     |
| `finding_message`         | Human-readable message.                         |

## Finding Severity Vocabulary

Allowed values:

```text
info
note
warning
error
critical
```

---

# Readiness Report Shape

The readiness report is a human-readable summary of Registration Unit inspection.

The readiness report should include:

```text
inspection summary
input manifest reference
output inventory reference
validation report reference
execution context
builder identity
inspection policy
validation policy
overall readiness summary
per-Registration Unit readiness summary
non-mutation summary
certification visibility summary
unresolved-state summary
limitations
recommended next action
```

The readiness report is not certification evidence by itself.

The readiness report must not promote Registration Units to certified.

---

# Reconstruction Requirements

Registration Unit inventory and validation artifacts must support reconstruction of:

```text
which Registration Units were declared
which Registration Units were inspected
which paths or references were used
which backend representation was declared
which producer family each unit represented
which source package each unit preserved
which artifact registrations were visible
which assertion registrations were visible
which source identities were visible
which namespaces were preserved
which validation status was reported
which certification status was reported
which inspection policy was used
which validation policy was used
which builder produced the inventory
which readiness status was assigned
which non-mutation evidence was recorded
which limitations were observed
```

The readiness inventory must preserve enough information for Corpus Generation to select Registration Units without rediscovering or mutating them.

---

# Relationship To Corpus Generation Schema

The Registration Unit schema prepares candidate inputs for Corpus Generation.

The responsibility boundary is:

```text
Registration Unit schema
    defines how individual Registration Units are declared, inspected,
    inventoried, validated, and handed off as candidate inputs

Corpus Generation schema
    defines how selected Registration Units are grouped under a declared
    corpus-generation identity and selection policy
```

The Registration Unit inventory may indicate readiness.

It must not silently declare Corpus Generation scope.

A Registration Unit may appear in multiple Corpus Generations.

A Corpus Generation must preserve the identity of each selected Registration Unit.

---

# Relationship To Assertion Record Schema

Registration Units preserve assertion registrations.

Assertion Record indexing constructs or resolves corpus-indexable Assertion Records from selected Registration Units.

The Registration Unit schema may summarize assertion-registration availability.

It must not define the final corpus-level Assertion Record index.

It must not collapse distinct assertion registrations into opaque counts that prevent reconstruction.

Any assertion-registration summary emitted under this schema must remain traceable to the Registration Unit.

---

# Relationship To Downstream Derived Schemas

Registration Unit schema artifacts must not define or emit:

```text
Evidence Topology records
Convergence Geometry records
Evidence Convergence Surface memberships
Projection View materializations
RDGP reasoning outputs
biological interpretation records
```

Downstream derived schemas must preserve Registration Unit lineage through Assertion Records, topology, geometry, surfaces, and projections.

---

# Anti-Collapse Safeguards

This schema prohibits:

```text
Registration Unit input manifest treated as Corpus Generation scope
Registration Unit inventory treated as source truth
Registration Unit readiness treated as certification
Registration Unit summary treated as Assertion Record index
Registration Unit inspection treated as topology derivation
Registration Unit inspection treated as geometry characterization
Registration Unit inspection treated as surface construction
Registration Unit inspection treated as projection generation
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
sidecar inventory replacing Registration Unit records
biological reasoning during Registration Unit inspection
destructive modification of certified Registration Units
```

Any implementation that performs one of these actions violates this schema.

---

# Minimal Local Golden Fixture Requirements

A local golden fixture used for Phase 4.1 development should include enough structure to exercise this schema without requiring MARK-resident heavy SQLite files.

A minimal local golden fixture should support inspection of:

```text
Registration Unit identity
backend representation
producer family
source package identity
artifact registration count
assertion registration count
source identity count
namespace count
validation status
certification status or explicit provisional status
readiness status assignment
non-mutation check behavior
unresolved-state handling
```

The local golden fixture may be provisional.

It must not masquerade as certified MARK output.

The fixture should be small enough for local unit tests and CI.

---

# MARK Smoketest Requirements

MARK heavy Phase 4 Registration Unit smoketests should inspect the certified Phase 3 Registration Unit set.

Expected MARK Registration Unit paths may include:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

MARK-facing builder and validator scripts may use MARK-explicit paths such as:

```text
scripts/mark/phase4/build_registration_unit_inventory.py
scripts/mark/phase4/validate_registration_units.py
```

The exact script names are not schema-level requirements.

The schema-level requirement is that MARK inspection must remain explicit, read-only, deterministic, status-visible, and non-mutating.

---

# Schema Completion Criteria

The Registration Unit schema is satisfied when Phase 4 Registration Unit implementation can emit artifacts that:

```text
declare candidate Registration Unit inputs explicitly
preserve Registration Unit identity or explicit unresolved state
preserve backend representation
preserve producer family or explicit unresolved state
preserve source package identity or explicit unresolved state
summarize artifact registrations
summarize assertion registrations
summarize source identities
summarize namespaces
expose validation status
expose certification status when available
assign readiness status under declared policy
record inspection context
record builder identity
record fixture class
record execution context
record non-mutation evidence or limitation
emit machine-readable inventory
emit human-readable readiness report
emit machine-readable validation report
support Corpus Generation handoff
remain deterministic under fixed inputs
avoid mutating Registration Units
preserve anti-collapse safeguards
```

This schema is not satisfied merely because a path list exists.

It is satisfied only when inspected Registration Units are represented as safe, traceable, non-mutated Phase 4 checkpoint inputs.

---

# Summary

The Registration Unit schema defines the Phase 4 consumption-facing schema for registered producer evidence packages.

The governing distinction is:

```text
Registration Units preserve custody.

Registration Unit readiness verifies safe consumption.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.
```

The guiding rule is:

```text
Declare inputs.

Inspect read-only.

Record readiness.

Expose status.

Preserve custody.

Emit sidecars.

Do not mutate.

Do not derive.

Do not interpret.
```

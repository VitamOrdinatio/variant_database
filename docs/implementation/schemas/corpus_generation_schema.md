# Corpus Generation Schema

## Purpose

This document defines the Phase 4 Corpus Generation schema for the Variant Database (VDB).

The purpose of this schema is to define how VDB declares, validates, summarizes, and hands off a selected set of Registration Units as a deterministic evidence scope for downstream Phase 4 derivation.

A Corpus Generation is the declared evidence scope from which Assertion Record indexing, Evidence Topology derivation, Convergence Geometry derivation, Evidence Convergence Surface construction, Projection View generation, and downstream consumer projections may proceed.

A Corpus Generation declares scope.

It does not interpret evidence.

It does not create Assertion Records.

It does not derive Evidence Topology.

It does not characterize Convergence Geometry.

It does not construct Evidence Convergence Surfaces.

It does not emit Projection Views that replace the Corpus Generation.

It does not perform downstream reasoning.

---

# Schema Role

The Corpus Generation schema defines the logical records emitted by Phase 4 Corpus Generation construction.

The central schema objects are:

```text
corpus_generation_identity
corpus_generation_selection_manifest_record
corpus_generation_manifest_record
corpus_generation_registration_unit_membership_record
corpus_generation_exclusion_record
downstream_assertion_record_input_manifest_record
```

Together, these records answer:

```text
Which Registration Units were selected together,
under which selection policy,
for which Corpus Generation identity,
with which inclusion and exclusion rationale,
with which validation and certification visibility,
and with which downstream handoff records?
```

Corpus Generation records are scope-declaration records.

They are not source evidence.

They are not Registration Units.

They are not Assertion Records.

They are not topology, geometry, surfaces, projections, or biological interpretations.

---

# Non-Goals

This schema does not define:

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
physical storage DDL
SQLite implementation internals
```

Corpus Generation construction may inspect Registration Unit readiness inventories and selected Registration Units.

Corpus Generation construction must not mutate Registration Units.

Corpus Generation construction must not create source authority.

Corpus Generation construction must not become source truth.

---

# Governed Artifacts

This schema governs the following Phase 4 Corpus Generation artifacts:

```text
corpus_generation_selection_manifest.tsv
corpus_generation_selection_manifest.json when policy-enabled
corpus_generation_manifest.tsv
corpus_generation_manifest.json
corpus_generation_report.md
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
downstream_assertion_record_input_manifest.tsv
```

Recommended output location:

```text
results/phase4/corpus_generations/<corpus_generation_id>/
    corpus_generation_manifest.tsv
    corpus_generation_manifest.json
    corpus_generation_report.md
    corpus_generation_validation_report.json
    corpus_generation_validation_report.tsv
    downstream_assertion_record_input_manifest.tsv
```

For the initial MARK benchmark Corpus Generation:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
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

# File Format Conventions

## TSV

TSV files provide compact, operator-readable tabular records.

The canonical TSV artifacts for this schema are:

```text
corpus_generation_manifest.tsv
corpus_generation_validation_report.tsv
downstream_assertion_record_input_manifest.tsv
```

`corpus_generation_manifest.tsv` should be row-oriented by Registration Unit membership or exclusion record.

Each row may repeat Corpus Generation identity fields to preserve standalone row interpretability.

## JSON

JSON files provide richer machine-readable records.

The canonical JSON artifacts for this schema are:

```text
corpus_generation_manifest.json
corpus_generation_validation_report.json
```

The JSON representation may include nested Corpus Generation identity, selection policy, included Registration Units, excluded Registration Units, summaries, validation metadata, downstream handoff references, and reconstruction metadata.

## Markdown

Markdown reports provide human-readable inspection summaries.

The canonical Markdown artifact for this schema is:

```text
corpus_generation_report.md
```

## JSONL

This schema does not require JSONL for the initial Corpus Generation layer.

Corpus Generation is manifest-oriented rather than record-stream-oriented.

JSONL may be added later if implementation emits row-oriented per-membership or per-validation finding streams.

---

# Selection Manifest Schema

A Corpus Generation selection manifest declares intended Corpus Generation scope before final validation.

The selection manifest is an operator or builder declaration.

It is not source truth.

It is not sufficient by itself to define a validated Corpus Generation.

It does not replace Registration Unit metadata.

It must be validated against Registration Unit readiness inventory records or Registration Unit metadata before Corpus Generation construction becomes authoritative.

## Required Selection Manifest Fields

| Field                           |    Required | Description                                                     |
| ------------------------------- | ----------: | --------------------------------------------------------------- |
| `corpus_generation_id`          |         yes | Stable identifier for the intended Corpus Generation.           |
| `registration_unit_label`       |         yes | Human-readable label for the candidate Registration Unit.       |
| `registration_unit_reference`   | recommended | Backend-neutral reference to the candidate Registration Unit.   |
| `registration_unit_path`        | conditional | Filesystem path when the Registration Unit is path-backed.      |
| `expected_registration_unit_id` |    optional | Expected stable Registration Unit identifier when known.        |
| `expected_producer_family`      | recommended | Expected producer family.                                       |
| `expected_certification_status` | recommended | Expected Registration Unit certification status.                |
| `expected_readiness_status`     | recommended | Expected Registration Unit readiness status when available.     |
| `expected_backend`              | recommended | Expected Registration Unit backend representation.              |
| `inclusion_status`              |         yes | Intended inclusion status under the selection policy.           |
| `inclusion_rationale`           | conditional | Required when the candidate is intended for inclusion.          |
| `exclusion_status`              | conditional | Required when the candidate is explicitly excluded or deferred. |
| `exclusion_rationale`           | conditional | Required when exclusion affects scope interpretation.           |
| `notes`                         |    optional | Operator or builder notes.                                      |

## Selection Manifest Example

```text
corpus_generation_id	registration_unit_label	registration_unit_path	expected_producer_family	expected_certification_status	expected_backend	inclusion_status	inclusion_rationale	notes
mark_phase4_corpus_6tep_v1	gsc_epilepsy	results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite	GSC	certified	sqlite	included	certified Phase 3 benchmark input	GSC epilepsy semantic evidence
mark_phase4_corpus_6tep_v1	gsc_mitochondrial_disease	results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite	GSC	certified	sqlite	included	certified Phase 3 benchmark input	GSC mitochondrial semantic evidence
mark_phase4_corpus_6tep_v1	vap_hg002	results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite	VAP	certified	sqlite	included	certified Phase 3 benchmark input	HG002 reference specimen
```

## Selection Manifest Rules

A selection manifest must make intended Corpus Generation scope explicit.

Implicit filesystem discovery must not silently define Corpus Generation scope.

A folder listing is not a Corpus Generation.

Fields prefixed with `expected_` are validation expectations.

They must not override inspected Registration Unit metadata.

---

# Corpus Generation Identity Schema

Every Corpus Generation must have a stable identity.

## Required Identity Fields

| Field                       |    Required | Description                                            |
| --------------------------- | ----------: | ------------------------------------------------------ |
| `corpus_generation_id`      |         yes | Stable Corpus Generation identifier.                   |
| `corpus_generation_label`   | recommended | Human-readable label.                                  |
| `corpus_generation_purpose` |         yes | Declared purpose of the Corpus Generation.             |
| `corpus_generation_version` | recommended | Corpus Generation version when applicable.             |
| `selection_policy_id`       |         yes | Selection policy identifier.                           |
| `selection_policy_version`  | recommended | Selection policy version when applicable.              |
| `builder_name`              |         yes | Name of builder that emitted the Corpus Generation.    |
| `builder_version`           | recommended | Builder version when available.                        |
| `build_timestamp`           |         yes | Timestamp of Corpus Generation construction.           |
| `manifest_schema_version`   | recommended | Corpus Generation schema version.                      |
| `validation_status`         |         yes | Corpus Generation validation status.                   |
| `certification_status`      | recommended | Corpus Generation certification status when available. |

## Initial MARK Benchmark Identity

Recommended initial identity:

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

# Selection Policy Schema

Every Corpus Generation must declare a selection policy.

The selection policy defines which Registration Units are eligible, selected, excluded, or deferred.

## Required Selection Policy Fields

| Field                              |    Required | Description                                                              |
| ---------------------------------- | ----------: | ------------------------------------------------------------------------ |
| `selection_policy_id`              |         yes | Stable selection policy identifier.                                      |
| `selection_policy_version`         | recommended | Selection policy version when applicable.                                |
| `selection_policy_description`     |         yes | Human-readable selection rule.                                           |
| `required_validation_status`       | recommended | Required Registration Unit validation status when applicable.            |
| `required_certification_status`    | recommended | Required Registration Unit certification status when applicable.         |
| `producer_families_in_scope`       | recommended | Producer families eligible under this policy.                            |
| `evidence_domains_in_scope`        |    optional | Evidence domains eligible under this policy when applicable.             |
| `temporal_constraints`             |    optional | Temporal or generation constraints when applicable.                      |
| `inclusion_rationale_requirements` | recommended | Required rationale semantics for inclusion.                              |
| `exclusion_rationale_requirements` | recommended | Required rationale semantics for exclusion.                              |
| `failure_behavior`                 | recommended | Whether missing, unreadable, or uncertified inputs fail, warn, or defer. |

## Initial MARK Benchmark Selection Policy

Recommended initial policy statement:

```text
Select the six certified Phase 3 MARK Registration Units representing
two GSC semantic evidence packages and four VAP variant evidence packages
for initial Phase 4 multi-producer heavy smoketest derivation.
```

Selection policy must not be replaced by an informal file list.

Policy evolution that changes Corpus Generation reconstruction must be versioned.

---

# Corpus Generation Manifest Schema

The Corpus Generation manifest is the validated declared evidence scope.

It must preserve the exact selected Registration Unit set, relevant exclusions, selection policy, summary counts, validation visibility, certification visibility, and downstream handoff references.

## Required Manifest Fields

| Field                          |    Required | Description                                                                           |
| ------------------------------ | ----------: | ------------------------------------------------------------------------------------- |
| `corpus_generation_id`         |         yes | Stable Corpus Generation identifier.                                                  |
| `corpus_generation_label`      | recommended | Human-readable label.                                                                 |
| `corpus_generation_purpose`    |         yes | Declared Corpus Generation purpose.                                                   |
| `corpus_generation_version`    | recommended | Corpus Generation version.                                                            |
| `selection_policy_id`          |         yes | Selection policy identifier.                                                          |
| `selection_policy_version`     | recommended | Selection policy version.                                                             |
| `membership_record_type`       |         yes | Record type, such as `included_registration_unit` or `excluded_registration_unit`.    |
| `registration_unit_id`         | conditional | Required for included units; explicit unresolved state allowed for failed candidates. |
| `registration_unit_label`      |         yes | Human-readable Registration Unit label or candidate label.                            |
| `registration_unit_reference`  | recommended | Backend-neutral Registration Unit reference.                                          |
| `registration_unit_inventory_record_reference` | recommended | Reference to the Registration Unit inventory record used during Corpus Generation construction. |
| `registration_unit_path`       | conditional | Filesystem path when path-backed.                                                     |
| `producer_family`              | recommended | Producer family or explicit unresolved state.                                         |
| `source_package_id`            | recommended | Source package identifier or explicit unresolved state.                               |
| `registration_backend`         | recommended | Registration Unit backend representation.                                             |
| `validation_status`            | recommended | Registration Unit validation status.                                                  |
| `certification_status`         | recommended | Registration Unit certification status.                                               |
| `readiness_status`             | recommended | Registration Unit readiness status from Phase 4.1 when available.                     |
| `inclusion_status`             | conditional | Inclusion status for included units.                                                  |
| `inclusion_rationale`          | conditional | Inclusion rationale for included units.                                               |
| `exclusion_status`             | conditional | Exclusion status for excluded or deferred candidates.                                 |
| `exclusion_rationale`          | conditional | Exclusion rationale when applicable.                                                  |
| `artifact_count`               | recommended | Registered artifact count or explicit unresolved state.                               |
| `assertion_registration_count` | recommended | Assertion registration count or explicit unresolved state.                            |
| `source_identity_count`        | recommended | Source identity count or explicit unresolved state.                                   |
| `namespace_count`              | recommended | Namespace count or explicit unresolved state.                                         |
| `evidence_domain_count`        |    optional | Evidence domain count or explicit unresolved state.                                   |
| `builder_name`                 |         yes | Builder name.                                                                         |
| `builder_version`              | recommended | Builder version.                                                                      |
| `build_timestamp`              |         yes | Build timestamp.                                                                      |
| `manifest_schema_version`      | recommended | Corpus Generation schema version.                                                     |

## Manifest Rules

The manifest must be deterministic under fixed inputs.

The manifest must be sufficient to reconstruct the exact selected Registration Unit set.

The manifest must preserve Registration Unit boundaries.

The manifest must not replace Registration Units.

The manifest must not become source truth.

## Flattened Status Field Disambiguation

When Corpus Generation-level status fields and Registration Unit-level status fields appear in the same flattened table, implementations should use explicit field prefixes.

Recommended flattened status fields include:

```text
corpus_generation_validation_status
corpus_generation_certification_status
registration_unit_validation_status
registration_unit_certification_status
registration_unit_readiness_status
```

Unprefixed fields may be used only when the record context makes the authority unambiguous.

Flattened records must not allow Corpus Generation validation status, Corpus Generation certification status, Registration Unit validation status, Registration Unit certification status, or Registration Unit readiness status to collapse into a single ambiguous status field.

---

# Included Registration Unit Membership Schema

Each included Registration Unit must be represented by a membership record.

## Required Included Membership Fields

```text
corpus_generation_id
selection_policy_id
registration_unit_id
registration_unit_label
registration_unit_reference
registration_unit_inventory_record_reference
registration_unit_path
producer_family
source_package_id
registration_backend
validation_status
certification_status
readiness_status
inclusion_status
inclusion_rationale
artifact_count
assertion_registration_count
source_identity_count
namespace_count
```

For included Registration Units, the following fields are required or must be represented by an explicit unresolved state:

```text
source_package_id
registration_backend
validation_status
certification_status
readiness_status
```

These fields must not silently disappear from included membership records.

## Inclusion Status Vocabulary

Allowed values:

```text
included
included_with_note
included_for_fixture
included_for_failure_mode
```

## Inclusion Rationale Vocabulary

Allowed rationale values or phrases may include:

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

Additional rationales may be used when documented by selection policy.

Included Registration Units must remain individually identifiable.

A Corpus Generation must not merge selected Registration Units into a single opaque evidence source.

---

# Excluded Registration Unit Record Schema

A Corpus Generation should explicitly declare excluded Registration Units or candidates when exclusion affects interpretation of corpus scope.

## Required Exclusion Fields

| Field                                   |    Required | Description                                                          |
| --------------------------------------- | ----------: | -------------------------------------------------------------------- |
| `corpus_generation_id`                  |         yes | Corpus Generation identifier.                                        |
| `selection_policy_id`                   |         yes | Selection policy identifier.                                         |
| `candidate_registration_unit_id`        | recommended | Candidate Registration Unit identifier or explicit unresolved state. |
| `candidate_registration_unit_label`     | recommended | Human-readable candidate label.                                      |
| `candidate_registration_unit_reference` | recommended | Backend-neutral candidate reference.                                 |
| `candidate_registration_unit_path`      | conditional | Candidate path when path-backed.                                     |
| `observed_producer_family`              |    optional | Observed producer family when available.                             |
| `observed_validation_status`            |    optional | Observed validation status when available.                           |
| `observed_certification_status`         |    optional | Observed certification status when available.                        |
| `observed_readiness_status`             |    optional | Observed readiness status when available.                            |
| `exclusion_status`                      |         yes | Exclusion status.                                                    |
| `exclusion_rationale`                   |         yes | Exclusion rationale.                                                 |
| `observed_failure_reason`               | conditional | Required when exclusion is failure-related.                          |

## Exclusion Status Vocabulary

Allowed values:

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

## Exclusion Rationale Vocabulary

Allowed rationale values or phrases may include:

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

# Corpus Summary Schemas

A Corpus Generation may summarize selected Registration Units.

Summaries support inspection, validation, and downstream planning.

Summaries do not replace Registration Unit records.

Summaries do not become Assertion Records.

Summaries do not create topology, geometry, surfaces, projections, or biological interpretations.

## Allowed Summary Domains

Allowed count and inventory summaries include:

```text
registration_unit_count
producer_family_distribution
package_count
artifact_count_summary
assertion_registration_count_summary
source_identity_count_summary
namespace_count_summary
evidence_domain_distribution
validation_status_distribution
certification_status_distribution
readiness_status_distribution
storage_footprint_summary when available
```

## Summary Rules

Count and inventory summaries must remain traceable to selected Registration Units.

Summaries must not collapse:

```text
Registration Unit boundaries
producer identity
source package identity
artifact identity
assertion registration identity
source identity
namespace identity
validation status
certification status
readiness status
```

If counts are unavailable, incomplete, approximate, or not applicable, that state must be explicit.

---

# Downstream Assertion Record Input Manifest Schema

The downstream Assertion Record input manifest makes Assertion Record indexing deterministic.

Canonical artifact:

```text
downstream_assertion_record_input_manifest.tsv
```

This manifest is not an Assertion Record index.

It must not contain derived Assertion Records unless explicitly produced by the Assertion Record implementation.

## Required Fields

| Field                          |    Required | Description                                                |
| ------------------------------ | ----------: | ---------------------------------------------------------- |
| `corpus_generation_id`         |         yes | Corpus Generation identifier.                              |
| `registration_unit_id`         |         yes | Selected Registration Unit identifier.                     |
| `registration_unit_label`      |         yes | Human-readable Registration Unit label.                    |
| `registration_unit_reference`  | recommended | Backend-neutral Registration Unit reference.               |
| `registration_unit_inventory_record_reference` | recommended | Reference to the Registration Unit inventory record used to validate this selected Registration Unit. |
| `registration_unit_path`       | conditional | Registration Unit path when path-backed.                   |
| `producer_family`              |         yes | Producer family.                                           |
| `source_package_id`            | recommended | Source package identifier.                                 |
| `registration_backend`         | recommended | Backend representation.                                    |
| `assertion_registration_count` | recommended | Assertion registration count or explicit unresolved state. |
| `source_identity_count`        | recommended | Source identity count or explicit unresolved state.        |
| `validation_status`            | recommended | Registration Unit validation status.                       |
| `certification_status`         | recommended | Registration Unit certification status.                    |
| `readiness_status`             | recommended | Registration Unit readiness status.                        |
| `inclusion_status`             |         yes | Inclusion status from Corpus Generation manifest.          |
| `inclusion_rationale`          | recommended | Inclusion rationale.                                       |

## Handoff Rules

The downstream Assertion Record input manifest must preserve:

```text
Corpus Generation identity
selected Registration Unit identities
Registration Unit references
producer-family context
source package context
assertion registration availability
source identity availability
validation status
certification status
readiness status
```

The downstream Assertion Record input manifest enables Assertion Record indexing.

It does not perform Assertion Record indexing.

---

# Status Vocabularies

## Corpus Generation Status Vocabulary

Allowed Corpus Generation status values:

```text
planned
provisional
validated
certified
rejected
deprecated
```

Status semantics:

```text
planned
    The Corpus Generation has been declared but not yet constructed.

provisional
    The Corpus Generation is usable for development or fixture testing but is not
    authoritative for certification.

validated
    The Corpus Generation passed declared validation checks but has not been
    formally certified.

certified
    The Corpus Generation passed declared certification checks and may serve as
    a canonical Phase 4 derivation input.

rejected
    The Corpus Generation failed required validation or certification checks and
    must not be used as a Phase 4 input unless explicitly testing failure behavior.

deprecated
    The Corpus Generation remains historically reconstructable but should not be
    used for new derivation work unless explicitly requested.
```

## Validation Status Vocabulary

Allowed validation status values:

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

## Certification Status Vocabulary

Allowed certification status values:

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

## Important Certification Rule

A Corpus Generation built entirely from certified Registration Units is not automatically certified.

Certified Registration Units support Corpus Generation certification.

They do not replace Corpus Generation validation.

A Corpus Generation must not silently masquerade as certified.

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

A value of `0` means the selected Registration Unit reported zero records for that domain.

A value of `not_reported` means the domain count was not reported.

---

# Validation Report Shape

The Corpus Generation validation report records whether the declared Corpus Generation satisfies input, manifest, and anti-collapse requirements.

The validation report should include:

```text
validation_report_id
validation_report_label
corpus_generation_id
corpus_generation_manifest_reference
selection_manifest_reference
registration_unit_readiness_inventory_reference
selection_policy_id
selection_policy_version
validation_policy_id
validation_policy_version
builder_name
builder_version
validation_timestamp
overall_validation_status
included_registration_unit_count
excluded_registration_unit_count
deferred_registration_unit_count
producer_family_summary
certification_status_summary
readiness_status_summary
validation_findings
validation_limitations
```

The TSV validation report may represent one validation finding per row.

The JSON validation report may include nested findings grouped by Corpus Generation, Registration Unit membership, exclusion record, or validation tier.

## Validation Finding Fields

| Field                     | Description                                 |
| ------------------------- | ------------------------------------------- |
| `finding_id`              | Stable finding identifier when available.   |
| `corpus_generation_id`    | Corpus Generation identity.                 |
| `registration_unit_id`    | Registration Unit identity when applicable. |
| `registration_unit_label` | Registration Unit label when applicable.    |
| `finding_tier`            | Validation tier.                            |
| `finding_type`            | Type of validation finding.                 |
| `finding_severity`        | Severity of the finding.                    |
| `finding_status`          | Status of the finding.                      |
| `field_name`              | Field affected when applicable.             |
| `observed_value`          | Observed value when useful.                 |
| `expected_value`          | Expected value when useful.                 |
| `finding_message`         | Human-readable message.                     |

## Finding Tier Vocabulary

Allowed values:

```text
input_validation
manifest_validation
anti_collapse_validation
mark_benchmark_validation
```

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

# Corpus Generation Report Shape

The Corpus Generation report is a human-readable summary of declared evidence scope.

The report should include:

```text
Corpus Generation identity
selection policy summary
input selection manifest reference
Registration Unit readiness inventory reference
output manifest reference
validation report reference
included Registration Unit summary
excluded Registration Unit summary when applicable
producer-family summary
evidence-domain summary when available
artifact-count summary
assertion-registration-count summary
source-identity-count summary
validation status summary
certification status summary
readiness status summary
limitations
recommended next action
```

The Corpus Generation report is not source truth.

The Corpus Generation report is not certification evidence by itself.

The Corpus Generation report must not promote a Corpus Generation to certified.

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

Corpus Generation artifacts must support reconstruction of:

```text
which Registration Units were selected
which Registration Units were excluded when relevant
which paths or references were used
which selection policy was applied
which validation policy was applied
which inclusion rationale was used
which exclusion rationale was used when applicable
which producer families were represented
which evidence domains were represented when available
which packages were represented
which artifact counts were observed
which assertion registration counts were observed
which source identity counts were observed
which validation statuses were observed
which certification statuses were observed
which readiness statuses were observed
which builder produced the manifest
which build timestamp was used
which manifest schema version was used when available
which downstream input manifest was emitted
```

A Corpus Generation artifact must preserve enough information for downstream Assertion Record indexing, topology derivation, geometry derivation, surface construction, projection generation, and reconstruction.

---

# Relationship To Registration Unit Schema

Registration Units are inputs to Corpus Generations.

The responsibility boundary is:

```text
Registration Unit schema
    defines how individual Registration Units are declared, inspected,
    inventoried, validated, and handed off as candidate inputs

Corpus Generation schema
    defines how selected Registration Units are grouped under a declared
    Corpus Generation identity and selection policy
```

A Corpus Generation may include multiple Registration Units.

A Registration Unit may participate in multiple Corpus Generations.

Corpus Generations must preserve Registration Unit identities.

Corpus Generations must not erase Registration Unit boundaries.

---

# Relationship To Assertion Record Schema

Corpus Generations provide the evidence scope for Assertion Record indexing.

A Corpus Generation should emit or support a downstream Assertion Record input manifest containing selected Registration Unit identities, source package references, assertion-registration availability, source-identity availability, and status visibility.

The responsibility boundary is:

```text
Corpus Generation
    declares selected Registration Units

Assertion Record indexing
    resolves producer claims from selected Registration Units into
    corpus-indexable Assertion Records
```

Corpus Generation construction must not create Assertion Records.

The downstream Assertion Record input manifest is not an Assertion Record index.

Assertion Record indexing must preserve:

```text
corpus_generation_id
registration_unit_id
```

---

# Relationship To Downstream Derived Schemas

Corpus Generation schema artifacts may support downstream derivation by declaring evidence scope.

They must not define or emit:

```text
Assertion Record objects
Evidence Topology relationships
Convergence Geometry regions or features
Evidence Convergence Surface memberships
Projection View materializations
RDGP reasoning outputs
biological interpretation records
```

Downstream derived schemas must preserve Corpus Generation lineage.

Corpus Generation construction must not perform downstream derivation.

---

# Initial MARK Benchmark Requirements

The initial MARK Phase 4 benchmark Corpus Generation is expected to include six certified Phase 3 Registration Units:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

MARK benchmark validation should confirm:

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

# Anti-Collapse Safeguards

This schema prohibits:

```text
selection manifest treated as validated Corpus Generation
folder listing treated as Corpus Generation scope
Corpus Generation manifest treated as source truth
Corpus Generation treated as merged replacement for Registration Units
Registration Unit boundary collapse
producer-family collapse
source package identity collapse
artifact identity collapse
assertion registration collapse
source identity collapse
namespace collapse
validation status collapse
certification status collapse
readiness status collapse
inclusion rationale collapse
exclusion rationale collapse
certified Registration Units automatically promoting Corpus Generation to certified
uncertified Registration Units silently included in a certified Corpus Generation
topology derived before corpus scope is declared
topology relationships created inside a Corpus Generation
geometry created inside a Corpus Generation
surface eligibility declared inside a Corpus Generation
surface disclosure determined inside a Corpus Generation
projection output replacing Corpus Generation
biological reasoning performed inside Corpus Generation
destructive modification of Registration Units during Corpus Generation construction
```

Any implementation that performs one of these actions violates this schema.

---

# Schema Completion Criteria

The Corpus Generation schema is satisfied when Phase 4 Corpus Generation implementation can emit artifacts that:

```text
declare Corpus Generation identity
declare selection policy
declare intended selection scope explicitly
validate selected Registration Units against readiness inventory or Registration Unit metadata
preserve selected Registration Unit identities
preserve Registration Unit boundaries
preserve producer-family context
preserve source package identity
preserve artifact counts when available
preserve assertion-registration counts when available
preserve source-identity counts when available
preserve namespace counts when available
preserve validation status
preserve certification status when available
preserve readiness status when available
document inclusion rationale
document exclusion rationale when applicable
emit deterministic machine-readable Corpus Generation manifest
emit deterministic human-readable Corpus Generation report
emit deterministic validation report
emit deterministic downstream Assertion Record input manifest
support downstream Assertion Record indexing
avoid mutating Registration Units
avoid creating Assertion Records
avoid downstream derivation
avoid biological interpretation
preserve anti-collapse safeguards
```

This schema is not satisfied merely because a file list exists.

It is satisfied only when the declared Corpus Generation is reconstructable, deterministic, policy-explicit, Registration Unit-preserving, validation-aware, and safe to use as the evidence universe for downstream Phase 4 derivation.

---

# Summary

The Corpus Generation schema defines the Phase 4 scope-declaration schema for selected Registration Units.

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

Expose status.

Emit deterministic manifests.

Do not mutate.

Do not derive.

Do not interpret.
```

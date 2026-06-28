# Projection Layer Schema

## Purpose

This document defines the Phase 4 Projection Layer schema for the Variant Database (VDB).

The purpose of this schema is to define how VDB represents governed source records as deterministic, purpose-bound Projection Views while preserving source authority, lineage, field transformations, omissions, lossiness, generation context, currency context, materialization context, and reconstruction paths.

A Projection View is a purpose-bound representation over preserved assertions or governed VDB-derived layers.

Projection changes representation.

Projection does not change authority.

Projection makes governed VDB evidence inspectable, transmissible, reportable, exportable, queryable, and consumable.

Projection must never make evidence more true.

---

# Schema Role

The Projection Layer schema defines the logical records emitted by Phase 4 Projection Layer construction.

The central schema objects are:

```text
projection_build_manifest_record
projection_view_record
projection_source_record
projection_field_map_record
projection_transformation_record
projection_lossiness_record
projection_omission_record
projection_authority_label_record
projection_generation_currency_record
projection_reconstruction_path_record
projection_validation_finding_record
materialized_projection_record
```

Together, these records answer:

```text
What was projected?

From which governed source layer?

From which source records?

For what purpose?

Under which projection policy?

With which field selections, omissions, transformations, and materializations?

With which lossiness?

With which authority labels?

With which generation and currency context?

With which reconstruction path?
```

Projection Layer schema artifacts are representation-governance records.

They are not source evidence.

They are not Registration Units.

They are not Corpus Generations.

They are not Assertion Records.

They are not Evidence Topology.

They are not Convergence Geometry.

They are not Evidence Convergence Surfaces.

They are not downstream reasoning.

---

# Non-Goals

This schema does not define:

```text
Registration Unit creation
Corpus Generation selection
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
surface eligibility declaration
surface disclosure decisions
raw producer artifact parsing
producer TEP parsing
Query Surface governance
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
candidate prioritization
projection-derived biological confidence scoring
final RDGP payload semantics
dashboard visualization design
API endpoint behavior
physical storage DDL
```

Projection Layer schema artifacts represent governed VDB records.

They must not mutate source records.

They must not overwrite source records.

They must not replace source records.

They must not convert representation into source authority.

---

# Governed Artifacts

This schema governs the following Phase 4 Projection Layer artifacts:

```text
projection_build_manifest.tsv
projection_build_manifest.json
projection_views.tsv
projection_views.jsonl
projection_source_records.tsv
projection_field_map.tsv
projection_transformations.tsv
projection_lossiness.tsv
projection_omissions.tsv
projection_authority_labels.tsv
projection_generation_currency.tsv
projection_reconstruction_paths.tsv
projection_validation_report.json
projection_validation_report.tsv
projection_build_report.md
```

Depending on declared projection purpose and materialization policy, materialized outputs may include:

```text
materialized/developer_inspection_projection.tsv
materialized/validation_projection.md
materialized/surface_membership_projection.tsv
materialized/assertion_record_projection.tsv
materialized/topology_inspection_projection.tsv
materialized/geometry_feature_projection.tsv
materialized/surface_export_projection.json
materialized/rdgp_facing_projection_manifest.tsv
materialized/rdgp_facing_projection.json
future materialized projection outputs
```

Recommended output location:

```text
results/phase4/projection_layer/<projection_build_id>/
    projection_build_manifest.tsv
    projection_build_manifest.json
    projection_views.tsv
    projection_views.jsonl
    projection_source_records.tsv
    projection_field_map.tsv
    projection_transformations.tsv
    projection_lossiness.tsv
    projection_omissions.tsv
    projection_authority_labels.tsv
    projection_generation_currency.tsv
    projection_reconstruction_paths.tsv
    projection_validation_report.json
    projection_validation_report.tsv
    projection_build_report.md
    materialized/
        developer_inspection_projection.tsv
        validation_projection.md
        surface_membership_projection.tsv
```

For the initial MARK Phase 4 projection build:

```text
results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1/
```

Projection outputs must not overwrite governed source records.

Projection output paths must not be confused with source layer paths.

---

# File Format Conventions

## TSV

TSV files provide compact, operator-readable tabular records.

Canonical TSV artifacts include:

```text
projection_build_manifest.tsv
projection_views.tsv
projection_source_records.tsv
projection_field_map.tsv
projection_transformations.tsv
projection_lossiness.tsv
projection_omissions.tsv
projection_authority_labels.tsv
projection_generation_currency.tsv
projection_reconstruction_paths.tsv
projection_validation_report.tsv
```

## JSON

JSON files provide richer machine-readable structured records.

Canonical JSON artifacts include:

```text
projection_build_manifest.json
projection_validation_report.json
```

JSON may include nested build metadata, source declarations, field maps, lossiness records, authority labels, materialization records, validation findings, and reconstruction paths.

## JSONL

JSONL files represent row-oriented record streams where each line is an independent JSON object.

Canonical JSONL artifact:

```text
projection_views.jsonl
```

JSONL is appropriate when Projection Views contain many projected records or when downstream consumers benefit from line-delimited streaming.

`projection_views.jsonl` contains line-delimited Projection View metadata records unless a projection policy explicitly declares a materialized projected-record stream.

Materialized projected records should be emitted under:

```text
materialized/
```

or another projection-policy-declared materialization path.

Projection View metadata streams and materialized projected-record streams must not be silently conflated.

## Markdown

Markdown reports provide human-readable projection build summaries.

Canonical Markdown artifact:

```text
projection_build_report.md
```

## Materialized Formats

Materialized Projection Views may use TSV, CSV, JSON, JSONL, Markdown, HTML, PDF, SQLite export, Parquet, dashboard payloads, API responses, or future consumer formats.

Materialization format does not define authority.

The declared source layer, source records, projection policy, authority labels, lossiness records, and reconstruction paths define authority.

---

# Projection Build Manifest Schema

A Projection Build is the execution-level object that emits one or more Projection Views.

A Projection Build manifest declares build identity, source layer, source manifest, projection policy, builder identity, validation status, certification status, and schema/contract context.

## Required Fields

| Field                             |    Required | Description                                                          |
| --------------------------------- | ----------: | -------------------------------------------------------------------- |
| `projection_build_id`             |         yes | Stable Projection Build identifier.                                  |
| `projection_build_label`          | recommended | Human-readable Projection Build label.                               |
| `input_source_layer`              |         yes | Declared governed source layer.                                      |
| `input_source_manifest_id`        | recommended | Source manifest identifier when available.                           |
| `input_source_manifest_path`      | recommended | Source manifest path or resolvable reference.                        |
| `input_corpus_generation_id`      | conditional | Required when source lineage includes a Corpus Generation.           |
| `input_assertion_record_index_id` | conditional | Required when source lineage includes an Assertion Record index.     |
| `input_topology_build_id`         | conditional | Required when source lineage includes Evidence Topology.             |
| `input_geometry_build_id`         | conditional | Required when source lineage includes Convergence Geometry.          |
| `input_surface_build_id`          | conditional | Required when source lineage includes Evidence Convergence Surfaces. |
| `projection_policy_id`            |         yes | Projection policy identifier.                                        |
| `projection_policy_version`       | recommended | Projection policy version.                                           |
| `field_mapping_policy_id`         | recommended | Field mapping policy identifier when separate.                       |
| `transformation_policy_id`        | recommended | Transformation policy identifier when separate.                      |
| `lossiness_policy_id`             | recommended | Lossiness policy identifier when separate.                           |
| `authority_labeling_policy_id`    | recommended | Authority labeling policy identifier when separate.                  |
| `generation_currency_policy_id`   | recommended | Generation/currency policy identifier when applicable.               |
| `builder_name`                    |         yes | Projection builder name.                                             |
| `builder_version`                 | recommended | Projection builder version.                                          |
| `projection_timestamp`            |         yes | Projection build timestamp.                                          |
| `contract_version`                | recommended | Projection Layer contract version.                                   |
| `schema_version`                  | recommended | Projection Layer schema version.                                     |
| `validation_status`               |         yes | Projection Build validation status.                                  |
| `certification_status`            | recommended | Projection Build certification status when available.                |

## Initial MARK Projection Build Identity

Recommended initial identity:

```text
projection_build_id: mark_phase4_corpus_6tep_v1_projection_build_v1
projection_build_label: MARK Phase 4 6-TEP Projection Build v1
input_source_layer: evidence_convergence_surface
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
projection_policy_id: mark_phase4_general_projection_policy
projection_policy_version: v1
```

A Projection Build may emit multiple Projection Views.

Projection Build identity must remain stable across validation, certification, reconstruction, consumer delivery, and returned reasoning linkage when applicable.

---

# Projection View Record Schema

A Projection View is a purpose-bound representation emitted by a Projection Build.

## Required Fields

| Field                        |    Required | Description                                                                |
| ---------------------------- | ----------: | -------------------------------------------------------------------------- |
| `projection_id`              |         yes | Stable Projection View identifier.                                         |
| `projection_build_id`        |         yes | Parent Projection Build identifier.                                        |
| `projection_label`           | recommended | Human-readable Projection View label.                                      |
| `projection_type`            |         yes | Type of Projection View.                                                   |
| `projection_purpose`         |         yes | Declared purpose of the Projection View.                                   |
| `projection_source_layer`    |         yes | Governed source layer represented by the projection.                       |
| `projection_policy_id`       |         yes | Projection policy identifier.                                              |
| `projection_policy_version`  | recommended | Projection policy version.                                                 |
| `target_consumer_class`      | conditional | Required for consumer-specific projections.                                |
| `projection_builder_name`    |         yes | Builder name.                                                              |
| `projection_builder_version` | recommended | Builder version.                                                           |
| `projection_timestamp`       |         yes | Projection timestamp.                                                      |
| `materialization_format`     |         yes | Materialized format, such as `tsv`, `json`, `markdown`, or `api_response`. |
| `materialization_path`       | conditional | Required when materialized as a file or package.                           |
| `materialization_status`     |         yes | Materialization status.                                                    |
| `lossiness_status`           |         yes | Declared lossiness status.                                                 |
| `validation_status`          |         yes | Projection View validation status.                                         |
| `certification_status`       | recommended | Certification status when available.                                       |
| `reconstruction_path_id`     | recommended | Reconstruction path identifier.                                            |

## Projection Type Vocabulary

Allowed projection types include:

```text
registration_unit_inventory_projection
corpus_generation_manifest_projection
assertion_record_table_projection
evidence_topology_inspection_projection
convergence_geometry_feature_projection
evidence_convergence_surface_projection
validation_report_projection
certification_report_projection
query_response_projection
developer_inspection_projection
dashboard_projection
TEP_VDB_export_projection
RDGP_facing_consumer_projection
future_consumer_projection
```

Additional projection types may be added when they preserve the schema invariants.

## Projection Purpose Rules

Projection purpose must be explicit.

Projection purpose may include:

```text
inspection
validation
certification
reporting
export
query_response
developer_debugging
consumer_delivery
downstream_reasoning_substrate
release_packaging
dashboard_display
future_consumer_support
```

Projection purpose must not be inferred solely from file name, directory path, dashboard title, report title, or output format.

---

# Projection Source Record Schema

Projection source records identify the governed records represented by a Projection View.

A Projection View generated without declared source records is not compliant.

## Required Fields

| Field                            |    Required | Description                                         |
| -------------------------------- | ----------: | --------------------------------------------------- |
| `projection_id`                  |         yes | Projection View identifier.                         |
| `projection_build_id`            |         yes | Projection Build identifier.                        |
| `projection_source_layer`        |         yes | Declared source layer.                              |
| `source_record_id`               |         yes | Source record identifier.                           |
| `source_record_type`             | recommended | Source record type or class.                        |
| `source_record_generation`       | recommended | Source record generation or version when available. |
| `source_authority_class`         |         yes | Authority class of the source record.               |
| `source_validation_status`       | recommended | Source validation status when available.            |
| `source_certification_status`    | recommended | Source certification status when available.         |
| `source_lineage_reference`       | recommended | Lineage reference when available.                   |
| `source_reconstruction_handle`   | recommended | Reconstruction handle.                              |
| `source_record_selection_policy` | recommended | Source selection policy or rule.                    |
| `validation_status`              |         yes | Validation status for this source record linkage.   |

## Source Layer Vocabulary

Allowed source layer values include:

```text
registration_unit
corpus_generation
assertion_record
evidence_topology
convergence_geometry
evidence_convergence_surface
validation_report
certification_report
query_surface
external_evidence_capsule
returned_reasoning_assertion
other_governed_vdb_source
```

## Source Record Reference Examples

Source record references may include:

```text
registration_unit_id
corpus_generation_id
assertion_id
topology_build_id
topology_relationship_id
geometry_build_id
convergence_region_id
geometry_feature_id
structural_motif_id
surface_id
surface_build_id
surface_membership_id
validation_report_id
certification_report_id
query_surface_id
external_capsule_id
returned_assertion_id
```

Source records must remain reconstructable.

Projection Views must not mutate, overwrite, or replace source records.

---

# Projection Field Map Schema

Projection field maps make field selection, field omission, renaming, transformation, flattening, denormalization, aggregation, and summary generation auditable.

Consumers must not be required to infer field provenance from column names alone.

## Required Fields

| Field                   |    Required | Description                                                                        |
| ----------------------- | ----------: | ---------------------------------------------------------------------------------- |
| `projection_id`         |         yes | Projection View identifier.                                                        |
| `projection_build_id`   |         yes | Projection Build identifier.                                                       |
| `source_layer`          |         yes | Source layer.                                                                      |
| `source_record_class`   | recommended | Source record class.                                                               |
| `source_field`          | conditional | Required when action references a source field.                                    |
| `target_field`          | conditional | Required when a target field is emitted.                                           |
| `field_action`          |         yes | Field action.                                                                      |
| `transformation_rule`   | conditional | Required when field is transformed, flattened, aggregated, summarized, or renamed. |
| `field_authority_class` | recommended | Authority class of the field.                                                      |
| `lossiness_status`      |         yes | Field-level lossiness status.                                                      |
| `omission_reason`       | conditional | Required when field is omitted or redacted.                                        |
| `reconstruction_path`   | recommended | Field-level reconstruction path.                                                   |
| `validation_status`     |         yes | Validation status for the field mapping.                                           |

## Field Action Vocabulary

Allowed values:

```text
selected
renamed
transformed
flattened
denormalized
aggregated
summarized
omitted
redacted
not_applicable
```

## Field Map Rules

Field renaming must not obscure source authority.

Field flattening must not collapse evidence strata.

Aggregation must not hide independent evidence strata unless explicitly declared as lossy.

Summary generation must not replace source records.

Omitted fields must be declared when omission affects interpretation, reconstruction, consumer use, authority, uncertainty, null semantics, lossiness, or downstream reasoning affordance.

---

# Projection Transformation Schema

Projection transformation records describe transformations applied to source records or fields.

## Required Fields

| Field                    |    Required | Description                                             |
| ------------------------ | ----------: | ------------------------------------------------------- |
| `projection_id`          |         yes | Projection View identifier.                             |
| `projection_build_id`    |         yes | Projection Build identifier.                            |
| `transformation_id`      |         yes | Stable transformation identifier.                       |
| `source_layer`           |         yes | Source layer.                                           |
| `source_record_class`    | recommended | Source record class.                                    |
| `source_field_reference` | conditional | Required when transformation applies to a source field. |
| `target_field`           | conditional | Required when transformation emits a target field.      |
| `transformation_type`    |         yes | Transformation type.                                    |
| `transformation_rule`    |         yes | Declared transformation rule.                           |
| `aggregation_rule`       | conditional | Required when aggregation is performed.                 |
| `sorting_rule`           | conditional | Required when sort order affects output semantics.      |
| `lossiness_status`       |         yes | Transformation lossiness status.                        |
| `reconstruction_path`    | recommended | Reconstruction path for transformed material.           |
| `validation_status`      |         yes | Transformation validation status.                       |

## Transformation Type Vocabulary

Allowed values:

```text
field_selection
field_rename
field_transform
field_flatten
record_denormalization
record_filter
record_aggregation
summary_generation
format_serialization
consumer_specific_packaging
report_rendering
dashboard_rendering
query_response_shaping
other_declared_transformation
```

## Transformation Rules

Transformations must not create biological meaning.

Transformations must not alter source authority.

Transformations must not collapse uncertainty, null semantics, producer strata, evidence-domain strata, namespace states, or independent evidence strata unless lossiness is explicitly declared.

---

# Projection Lossiness Schema

Projection lossiness records declare whether a Projection View is complete, partial, filtered, summarized, redacted, or otherwise lossy.

Lossiness is allowed.

Hidden lossiness is not allowed.

## Required Fields

| Field                                     |    Required | Description                                                                               |
| ----------------------------------------- | ----------: | ----------------------------------------------------------------------------------------- |
| `projection_id`                           |         yes | Projection View identifier.                                                               |
| `projection_build_id`                     |         yes | Projection Build identifier.                                                              |
| `lossiness_status`                        |         yes | Overall lossiness status.                                                                 |
| `lossiness_type`                          | recommended | Type of lossiness.                                                                        |
| `lossiness_reason`                        | conditional | Required when projection is lossy, partial, filtered, redacted, summary-only, or unknown. |
| `affected_source_layer`                   | conditional | Source layer affected by lossiness when applicable.                                       |
| `affected_source_record`                  | conditional | Source record affected by lossiness when applicable.                                      |
| `affected_field`                          | conditional | Field affected by lossiness when applicable.                                              |
| `filtering_policy`                        | conditional | Filtering policy when projection is filtered.                                             |
| `redaction_policy`                        | conditional | Redaction policy when projection is redacted.                                             |
| `summary_policy`                          | conditional | Summary policy when projection is summary-only.                                           |
| `reconstruction_path_to_omitted_material` | recommended | Reconstruction path to omitted material when available.                                   |
| `validation_status`                       |         yes | Validation status for lossiness declaration.                                              |

## Lossiness Status Vocabulary

Allowed values:

```text
lossless
field_lossy
record_lossy
summary_only
consumer_filtered
policy_filtered
format_limited
redacted
partial
unknown
not_applicable
```

## Lossiness Rules

Omitted evidence must not be interpreted as absent evidence.

Filtered evidence must not be interpreted as negative evidence.

Summary-only projections must not be treated as complete evidence representations.

If lossiness is unknown, that status must be explicit.

---

# Projection Omission Schema

Projection omission records declare omitted source layers, records, fields, or intermediate derivation components.

## Required Fields

| Field                                     |    Required | Description                                             |
| ----------------------------------------- | ----------: | ------------------------------------------------------- |
| `projection_id`                           |         yes | Projection View identifier.                             |
| `projection_build_id`                     |         yes | Projection Build identifier.                            |
| `omission_id`                             |         yes | Stable omission identifier.                             |
| `omitted_source_layer`                    | conditional | Source layer omitted when applicable.                   |
| `omitted_source_record`                   | conditional | Source record omitted when applicable.                  |
| `omitted_field`                           | conditional | Field omitted when applicable.                          |
| `omission_reason`                         |         yes | Reason for omission.                                    |
| `omission_policy_id`                      | recommended | Policy responsible for omission.                        |
| `lossiness_status`                        |         yes | Lossiness status caused by or associated with omission. |
| `reconstruction_path_to_omitted_material` | recommended | Reconstruction path to omitted material when available. |
| `validation_status`                       |         yes | Omission validation status.                             |

## Omission Reason Vocabulary

Allowed values include:

```text
not_applicable_to_projection_purpose
not_available_in_source
not_selected_by_policy
consumer_filtered
policy_filtered
format_limited
redacted
summary_only_projection
source_layer_not_in_chain
partial_chain_projection
withheld_upstream
unknown
other_declared_reason
```

Omission records must distinguish:

```text
not available
not applicable
withheld
filtered
redacted
not selected
unknown
```

These states must not collapse into a blank value.

---

# Projection Authority Label Schema

Authority labels make the projected record’s status explicit to consumers.

Consumers must not be required to infer authority from projection layout, folder location, table name, report title, dashboard panel, or package format.

## Required Fields

| Field                           |    Required | Description                                      |
| ------------------------------- | ----------: | ------------------------------------------------ |
| `projection_id`                 |         yes | Projection View identifier.                      |
| `projection_build_id`           |         yes | Projection Build identifier.                     |
| `projected_record_id`           | conditional | Projected record identifier when applicable.     |
| `projection_source_layer`       |         yes | Source layer represented.                        |
| `source_record_id`              | recommended | Source record identifier.                        |
| `source_authority_class`        |         yes | Authority class of the source record.            |
| `projection_authority_class`    |         yes | Authority class of the projected representation. |
| `producer_identity`             | conditional | Producer identity when applicable.               |
| `assertion_id`                  | conditional | Assertion Record identity when applicable.       |
| `derived_layer_identity`        | conditional | Derived-layer identity when applicable.          |
| `surface_eligibility_status`    | conditional | Surface eligibility status when applicable.      |
| `surface_disclosure_status`     | conditional | Surface disclosure status when applicable.       |
| `uncertainty_status`            | conditional | Uncertainty status when applicable.              |
| `null_state`                    | conditional | Null state when applicable.                      |
| `generation_or_currency_status` | conditional | Generation or currency status when applicable.   |
| `lossiness_status`              |         yes | Lossiness status.                                |
| `reconstruction_handle`         | recommended | Reconstruction handle.                           |
| `validation_status`             |         yes | Authority-label validation status.               |

## Source Authority Class Vocabulary

Allowed values include:

```text
producer_source_evidence
registration_unit_custody_metadata
corpus_scope_metadata
preserved_assertion
derived_organization
derived_structural_characterization
governed_exposure
projection_representation
validation_output
certification_output
query_response
returned_reasoning_assertion
external_evidence_capsule
unknown
```

## Projection Authority Class Vocabulary

Allowed values include:

```text
projection_representation
materialized_projection_output
inspection_representation
validation_representation
certification_representation
consumer_delivery_representation
query_response_representation
dashboard_representation
report_representation
export_representation
unknown
```

Projection authority is narrow.

It governs representation.

It does not create source authority.

---

# Projection Generation And Currency Schema

Projection generation and currency records preserve temporal, versioning, refresh, staleness, and supersession context.

## Required Fields

| Field                         |    Required | Description                                                       |
| ----------------------------- | ----------: | ----------------------------------------------------------------- |
| `projection_id`               |         yes | Projection View identifier.                                       |
| `projection_build_id`         |         yes | Projection Build identifier.                                      |
| `projection_generation_id`    | recommended | Projection generation identifier.                                 |
| `source_generation_id`        | recommended | Source generation identifier when available.                      |
| `source_build_identifier`     | recommended | Source build identifier when available.                           |
| `source_policy_version`       | recommended | Source policy version when available.                             |
| `projection_policy_version`   | recommended | Projection policy version.                                        |
| `projection_timestamp`        |         yes | Projection timestamp.                                             |
| `consumer_delivery_timestamp` | conditional | Required when delivered to a consumer and available.              |
| `refresh_status`              | recommended | Refresh status.                                                   |
| `staleness_status`            | recommended | Staleness status.                                                 |
| `supersession_status`         | recommended | Supersession status.                                              |
| `supersedes_projection_id`    | conditional | Prior projection superseded by this projection when applicable.   |
| `superseded_by_projection_id` | conditional | Later projection that supersedes this projection when applicable. |
| `validation_status`           |         yes | Generation/currency validation status.                            |

## Generation And Currency Status Vocabulary

Allowed values:

```text
current
stale
superseded
partial
provisional
deprecated
unknown
not_applicable
```

## Generation And Currency Rules

Projection generation must not overwrite earlier projection generations.

A newer projection must not erase reconstructability of an older projection.

A stale projection must not silently masquerade as current.

A superseded projection must remain historically reconstructable when retained.

---

# Projection Reconstruction Path Schema

Projection reconstruction paths allow source lineage and projection construction to be recovered.

A Projection View without a reconstruction path is not compliant.

## Required Fields

| Field                           |    Required | Description                                                        |
| ------------------------------- | ----------: | ------------------------------------------------------------------ |
| `projection_id`                 |         yes | Projection View identifier.                                        |
| `projection_build_id`           |         yes | Projection Build identifier.                                       |
| `reconstruction_path_id`        |         yes | Stable reconstruction path identifier.                             |
| `projection_source_layer`       |         yes | Source layer represented.                                          |
| `source_record_reference`       | recommended | Source record reference or source manifest reference.              |
| `source_manifest_reference`     | recommended | Source manifest reference when available.                          |
| `source_authority_reference`    | recommended | Source authority record or label reference.                        |
| `field_map_reference`           | recommended | Field map reference.                                               |
| `transformation_reference`      | recommended | Transformation reference.                                          |
| `lossiness_reference`           | recommended | Lossiness record reference.                                        |
| `omission_reference`            | recommended | Omission record reference.                                         |
| `authority_label_reference`     | recommended | Authority label reference.                                         |
| `generation_currency_reference` | recommended | Generation/currency reference.                                     |
| `materialization_reference`     | conditional | Materialized output reference when applicable.                     |
| `full_chain_status`             |         yes | Whether projection has full-chain or partial-chain reconstruction. |
| `omitted_intermediate_layers`   | conditional | Required for partial-chain projections when relevant.              |
| `omitted_layer_rationale`       | conditional | Required when intermediate layers are omitted.                     |
| `validation_status`             |         yes | Reconstruction-path validation status.                             |

## Full Chain Reconstruction

When a Projection View is derived from a full Phase 4 chain, reconstruction should support traceability to:

```text
Evidence Convergence Surface
Convergence Geometry
Evidence Topology
Assertion Records
Corpus Generation
Registration Units
producer artifacts
producer TEPs
```

## Partial Chain Reconstruction

When a Projection View is derived from a partial chain, reconstruction must support traceability to the declared source layer and its governed upstream lineage.

Partial-chain projections must declare:

```text
projection source layer
projection source records
omitted intermediate layers when relevant
reason omitted layers are not applicable
traceability path to preserved assertions, Registration Units, or another governed VDB source when applicable
```

---

# Materialized Projection Output Schema

Materialized projection outputs are concrete rendered files, packages, reports, tables, dashboards, or query responses emitted from Projection Views.

Projection metadata artifacts declare how projection was performed.

Materialized projection outputs are concrete rendered forms.

A materialized projection output is not source truth.

A materialized projection output does not replace its Projection View metadata.

A materialized projection output does not replace its governed source layer.

## Required Materialization Fields

| Field                       |    Required | Description                                        |
| --------------------------- | ----------: | -------------------------------------------------- |
| `projection_id`             |         yes | Projection View identifier.                        |
| `projection_build_id`       |         yes | Projection Build identifier.                       |
| `materialization_id`        | recommended | Stable materialization identifier.                 |
| `materialization_format`    |         yes | Output format.                                     |
| `materialization_path`      | conditional | File path or resolvable reference when applicable. |
| `materialization_role`      |         yes | Role of the materialized output.                   |
| `target_consumer_class`     | conditional | Consumer class when applicable.                    |
| `record_count`              | recommended | Projected record count when applicable.            |
| `field_count`               | recommended | Projected field count when applicable.             |
| `lossiness_status`          |         yes | Lossiness status.                                  |
| `authority_label_reference` | recommended | Authority label reference.                         |
| `reconstruction_path_id`    | recommended | Reconstruction path identifier.                    |
| `validation_status`         |         yes | Materialization validation status.                 |

## Materialization Format Vocabulary

Allowed values include:

```text
tsv
csv
json
jsonl
markdown
html
pdf
sqlite_export
parquet
dashboard_view
query_response
api_response
package
future_format
```

## Materialization Role Vocabulary

Allowed values include:

```text
developer_inspection
validation
certification
surface_membership
assertion_record_export
topology_inspection
geometry_feature_export
surface_export
RDGP_facing_consumer_payload
query_response
dashboard
report
future_consumer_payload
```

## Materialization Rules

Materialized outputs should be emitted under:

```text
materialized/
```

unless a projection policy explicitly declares another output location.

Materialized outputs may be regenerated from declared source records, projection policy, field maps, transformations, lossiness records, authority labels, generation/currency records, and reconstruction paths.

---

# RDGP-Facing Projection Profile Requirements

RDGP-facing Projection Views prepare governed VDB evidence for RDGP reasoning.

RDGP-facing projections expose reasoning affordances.

They do not perform RDGP reasoning.

They do not determine whether evidence explains phenotype.

They do not prioritize candidate genes.

They do not create biological confidence.

They do not generate RDGP conclusions.

## Required RDGP-Facing Preservation Categories

When an RDGP-facing projection profile is enabled, it should preserve or explicitly declare omission for:

```text
projection purpose
target consumer class
source layer
source surface identity when applicable
source geometry identity when applicable
source topology identity when applicable
source Assertion Record identities when applicable
source Corpus Generation identity
source Registration Unit identities when applicable
producer strata
evidence-domain strata
modality strata when available
modality or evidence-domain identity mapping when vocabularies differ across producers
sample context when applicable
gene context when applicable
phenotype context when applicable
variant context when applicable
regulatory context when applicable
regulatory domain association when applicable
phenotype-linked regulatory region when applicable
regulatory feature context when applicable
future regulatory evidence class when applicable
uncertainty states
null semantics
negative evidence distinction when available
evidence completeness status when available
completeness scope when available
absence basis when evidence absence is asserted
omission basis when evidence is not projected
withholding basis when evidence is withheld upstream
sample recurrence when available
cohort recurrence when available
producer recurrence when available
evidence uniqueness when available
assertion reuse when available
prior observation history when available
namespace mediation status
generation context
currency context
lossiness status
reconstruction handles
return-path identifiers
```

## RDGP Return-Path Requirements

RDGP-facing projections should preserve return-path identifiers sufficient to reconstruct:

```text
source Projection View
source projection generation
source surface when applicable
source geometry when applicable
source topology when applicable
source Assertion Records when applicable
source Corpus Generation
source Registration Units when applicable
downstream reasoning producer
reasoning generation
reasoning output identity
```

Returned RDGP reasoning outputs may re-enter VDB only as new preserved producer assertions or another declared governed source layer.

Returned RDGP assertions must not overwrite the Projection View or the VDB evidence generation from which they were derived.

---

# Validation Report Shape

Projection validation confirms representation, source declaration, field audibility, authority preservation, lossiness disclosure, reconstruction, determinism, and anti-collapse behavior.

## Validation Report Fields

The Projection validation report should include:

```text
validation_report_id
validation_report_label
projection_build_id
projection_build_manifest_reference
projection_views_reference
source_records_reference
field_map_reference
transformation_reference
lossiness_reference
omission_reference
authority_label_reference
generation_currency_reference
reconstruction_path_reference
materialized_output_reference when applicable
projection_policy_id
projection_policy_version
validation_policy_id
validation_policy_version
builder_name
builder_version
validator_name
validator_version
validation_timestamp
overall_validation_status
projection_view_count
source_record_count
field_map_record_count
transformation_record_count
lossiness_record_count
omission_record_count
authority_label_record_count
reconstruction_path_count
materialized_output_count
validation_findings
validation_limitations
```

The TSV validation report may represent one validation finding per row.

The JSON validation report may include nested findings grouped by Projection Build, Projection View, validation tier, source layer, field map, lossiness record, authority label, reconstruction path, or materialized output.

## Validation Finding Fields

| Field                 | Description                                 |
| --------------------- | ------------------------------------------- |
| `finding_id`          | Stable finding identifier when available.   |
| `projection_build_id` | Projection Build identifier.                |
| `projection_id`       | Projection View identifier when applicable. |
| `source_layer`        | Source layer when applicable.               |
| `source_record_id`    | Source record identifier when applicable.   |
| `finding_tier`        | Validation tier.                            |
| `finding_type`        | Type of validation finding.                 |
| `finding_severity`    | Severity of the finding.                    |
| `finding_status`      | Status of the finding.                      |
| `field_name`          | Field affected when applicable.             |
| `observed_value`      | Observed value when useful.                 |
| `expected_value`      | Expected value when useful.                 |
| `finding_message`     | Human-readable message.                     |

## Validation Tier Vocabulary

Allowed values:

```text
identity_and_source_validation
field_and_transformation_validation
authority_lossiness_and_omission_validation
reconstruction_validation
anti_collapse_validation
RDGP_facing_projection_validation
mark_projection_smoketest_validation
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

Validation must not claim biological correctness.

Validation must not certify RDGP reasoning correctness.

---

# Status And Vocabulary Definitions

## Validation Status Vocabulary

Allowed values:

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

Allowed values:

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

## Materialization Status Vocabulary

Allowed values:

```text
materialized
materialized_with_note
not_materialized
deferred
failed
not_applicable
```

## Refresh Status Vocabulary

Allowed values:

```text
current
refresh_needed
refresh_in_progress
stale
unknown
not_applicable
```

## Supersession Status Vocabulary

Allowed values:

```text
active
superseded
supersedes_prior
deprecated
unknown
not_applicable
```

## Unresolved-State Vocabulary

Allowed unresolved-state values:

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

Missing values must not collapse into blank strings.

A blank value must not silently masquerade as absence, negative evidence, zero count, non-applicability, validation failure, or certification failure.

---

# Determinism Requirements

Projection Layer outputs must be deterministic under fixed inputs.

Given the same:

```text
declared source layer
source records
source record generation
projection policy
field mapping policy
transformation policy
lossiness policy
authority labeling policy
materialization format
contract version
schema version
builder version
```

the builder should produce equivalent:

```text
projection_build_id
projection_id
projection source declarations
projection source record references
field map records
transformation records
lossiness records
omission records
authority label records
generation and currency records
materialized projection outputs
validation outcomes
report sections
reconstruction paths
```

Determinism requirements include:

```text
stable projection_id generation
stable source record ordering
stable field ordering
stable transformation behavior
stable omission behavior
stable lossiness behavior
stable authority label behavior
stable generation behavior
stable currency behavior
stable materialization behavior
stable validation status vocabulary
stable unresolved-state vocabulary
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define projection order.

Filesystem traversal order must not define projection order.

Source record lists used in projection identity generation should be sorted by stable source identifiers unless projection policy explicitly declares another stable ordering rule.

All output rows should be ordered by declared projection policy.

---

# Reconstruction Requirements

Projection Layer artifacts must support reconstruction of:

```text
projection identity
projection purpose
projection policy
projection source layer
projection source records
projection materialization format
projection lossiness status
field selection rules
field omission rules
field renaming rules
field transformation rules
filtering rules
aggregation rules when applicable
sorting rules when applicable
source authority labels
source validation status when available
source certification status when available
source lineage
generation context
currency context
consumer-specific shaping rules when applicable
materialization path
consumer delivery path when applicable
return-path identifiers when applicable
```

When a Projection View is derived from a full Phase 4 chain, reconstruction must support traceability to:

```text
Evidence Convergence Surface
Convergence Geometry
Evidence Topology
Assertion Records
Corpus Generation
Registration Units
producer artifacts
producer TEPs
```

When a Projection View is derived from a partial chain, reconstruction must support traceability to the declared source layer and its governed upstream lineage.

A Projection View without a reconstruction path is not schema-compliant.

---

# Relationship To Evidence Convergence Surface Schema

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed exposed evidence or another declared governed source for a purpose.

The responsibility boundary is:

```text
Evidence Convergence Surface schema
    defines governed exposure records, memberships, eligibility basis,
    disclosure basis, withholding, evidence strata, generation, and currency

Projection Layer schema
    defines purpose-bound representation over governed source records,
    including materialization, field mapping, lossiness, authority labels,
    generation, currency, and reconstruction paths
```

A Projection View over an Evidence Convergence Surface must preserve source surface identity when applicable.

A Projection View must not replace an Evidence Convergence Surface.

A Projection View must not acquire surface authority.

A Projection View must not treat surface eligibility as biological confidence.

A Projection View must not treat surface disclosure as biological endorsement.

---

# Relationship To Query Surface Specifications

A Query Surface is a governed access mechanism.

A Projection View is a purpose-bound representation emitted from governed VDB records.

The responsibility boundary is:

```text
Query Surface
    governed access pathway or interface over VDB records

Projection View
    purpose-bound representation emitted from governed VDB records
```

A Query Surface may emit Projection Views.

A query response may be a Projection View.

A Query Surface must not obscure projection source layer, authority status, lineage, lossiness, generation context, or reconstruction path.

A Projection View emitted through a Query Surface must satisfy this schema and the Projection Layer contract.

A Query Surface must not replace Projection Views.

A Projection View must not replace Query Surface governance.

---

# Relationship To Assertion Projection Taxonomy Schema

The Assertion Projection Taxonomy schema and the Projection Layer schema have distinct responsibilities.

```text
assertion_projection_taxonomy_schema.md
    defines conceptual projection classes and assertion/projection taxonomy

projection_layer_schema.md
    defines concrete Projection Layer build artifacts, Projection View records,
    source records, field maps, transformations, lossiness, omissions, authority
    labels, generation/currency records, reconstruction paths, validation records,
    and materialized outputs
```

The taxonomy may inform projection type classification.

The Projection Layer schema governs projection artifact representation and validation.

The taxonomy does not replace Projection Layer build metadata.

Projection Layer metadata does not replace conceptual projection taxonomy.

---

# Initial MARK Projection Build Requirements

The initial MARK Phase 4 Projection Build is expected to consume the downstream projection input manifest emitted by the Evidence Convergence Surface implementation.

Expected source manifest shape may include:

```text
surface_build_id
surface_id
surface_type
surface_purpose
input_geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
surface_membership_id
convergence_region_id
geometry_feature_id_summary
structural_motif_id_summary when applicable
eligibility_status
disclosure_status
withholding_reason when applicable
lossiness_status when applicable
generation_status when applicable
currency_status when applicable
validation_status
```

The initial projection build should prove general projection mechanics before RDGP-facing specialization.

Recommended initial projection types:

```text
developer_inspection_projection
validation_projection
surface_membership_projection
```

MARK projection validation should confirm:

```text
mark_phase4_corpus_6tep_v1 downstream projection input manifest is accepted
projection build identity is stable
source layer is declared
source records are declared
projection policy is declared
field map is emitted
lossiness records are emitted
omission records are emitted when relevant
authority labels are emitted
generation and currency records are emitted
reconstruction paths are emitted
developer inspection projection is emitted when policy-enabled
validation projection is emitted when policy-enabled
surface membership projection is emitted when policy-enabled
projection validation report is deterministic
materialized projection outputs are deterministic
```

RDGP-facing projection tests should be added when an RDGP projection profile is implemented.

---

# Anti-Collapse Safeguards

This schema prohibits:

```text
Projection View treated as source truth
Projection View treated as source evidence
Projection View treated as biological truth
Projection View treated as clinical evidence
projection row replacing Assertion Record
projection row replacing topology relationship
projection row replacing geometry feature
projection row replacing surface membership
projection package replacing Evidence Convergence Surface
projection format defining architecture
dashboard treated as evidence
query response treated as source evidence
report treated as source evidence
consumer package treated as reasoning conclusion
lossiness hidden
omitted evidence treated as absent evidence
filtered evidence treated as negative evidence
summary-only projection treated as complete evidence
field rename obscuring authority
materialized export overwriting upstream records
projection policy collapse
projection source layer collapse
projection lineage collapse
projection generation collapse
authority label collapse
uncertainty collapse
null-state collapse
producer-family collapse
evidence-domain collapse
namespace-state collapse
opaque composite score hiding independent evidence strata
RDGP-facing projection performing RDGP reasoning
pretty output treated as biological truth
```

Any implementation that performs one of these actions violates this schema.

---

# Schema Completion Criteria

The Projection Layer schema is satisfied when Phase 4 Projection Layer implementation can emit artifacts that:

```text
declare Projection Build identity
declare Projection View identity
declare projection purpose
declare projection source layer
declare source records
declare projection policy
declare materialization format
declare materialization path when applicable
declare field selection
declare field omission when relevant
declare field renaming when relevant
declare transformation rules when relevant
declare aggregation rules when relevant
declare lossiness status
declare omission reason when relevant
preserve authority labels
preserve source lineage
preserve generation context
preserve currency context when applicable
emit field map records when relevant
emit transformation records when relevant
emit lossiness records
emit omission records when relevant
emit authority label records
emit generation and currency records
emit reconstruction path records
emit materialized Projection Views when policy-enabled
emit human-readable Projection Build report
emit Projection Layer validation report
support full-chain reconstruction when source is a surface
support partial-chain reconstruction when source is another governed VDB layer
remain deterministic under fixed inputs
avoid mutating source records
avoid replacing source records
avoid becoming source evidence
avoid biological interpretation
preserve anti-collapse safeguards
```

This schema is not satisfied merely because a file, table, export, dashboard, API response, report, or package exists.

It is satisfied only when those records are purpose-bound, source-declared, authority-labeled, lineage-preserving, lossiness-explicit, materialization-neutral, generation-aware, currency-aware, reconstructable, non-interpretive, and non-authority-transferring.

---

# Summary

The Projection Layer schema defines the Phase 4 representation-governance schema for purpose-bound Projection Views.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed evidence for a purpose.

Downstream systems reason over projections.
```

The guiding rule is:

```text
Declare the source.

Declare the purpose.

Represent the evidence.

Expose lossiness.

Preserve authority.

Preserve lineage.

Preserve generation.

Preserve currency.

Remain materialization-neutral.

Do not mutate.

Do not overwrite.

Do not reason.

Never let representation become truth.
```

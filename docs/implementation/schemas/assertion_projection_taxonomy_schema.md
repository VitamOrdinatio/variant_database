# Assertion Projection Taxonomy Schema

## Epoch IV: Projection Layer

| Epoch | Epoch Identity       | Epoch Purpose                                                                                       |
| ----- | -------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer          | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry    | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | Discovery Layer      | How do preserved evidence topologies become discoverable?                                           |
| IV    | **Projection Layer** | **How does one truth generate many useful views without duplication?**                              |
| V     | Rationale Layer      | Why do we do this?                                                                                  |

---

## Schema Status

This document defines the schema structure for assertion projection taxonomy.

It is downstream of:

* `docs/design/assertion_projection_taxonomy.md`
* `docs/implementation/specifications/assertion_projection_taxonomy_spec.md`
* `docs/design/assertion_record_and_projection_model.md`
* `docs/implementation/schemas/assertion_record_schema.md`
* `docs/design/evidence_topology_model.md`
* `docs/implementation/schemas/evidence_topology_schema.md`
* `docs/design/convergence_geometry_model.md`
* `docs/implementation/schemas/convergence_geometry_schema.md`
* `docs/design/evidence_convergence_surface_model.md`
* `docs/implementation/schemas/evidence_convergence_surface_schema.md`

This schema is not a database-backend requirement.

It defines semantic object structure, required fields, optional extensions, controlled vocabularies, examples, invalid structures, and implementation invariants.

---

# Purpose

VDB preserves one scientific truth substrate and generates many useful views over it.

Those views are projections.

This schema defines the object family required to represent projections safely.

A valid projection schema must preserve:

* projection identity
* source identity
* source layer
* source generation
* projection purpose
* projection transform
* projection representation
* projection materialization state
* source lineage
* reconstructability
* semantic distinctions
* authority boundaries

The central schema invariant is:

```text
Projection identity is view identity.
Source identity remains truth identity.
```

---

# Schema Design Principle

Projection objects must be modular.

A projection should not be represented as a single flattened record that hides source identity, transform lineage, materialization state, aggregation behavior, redaction behavior, or currency state.

The schema separates the following concerns:

* projection build context
* projection root identity
* source references
* transform metadata
* lineage references
* materialization state
* consumer context
* aggregation behavior
* redaction behavior
* currency state
* export references
* validation records

This prevents useful views from becoming duplicate truth.

---

# Schema Tiering

The projection schema is organized into three tiers.

| Tier   | Name                                 | Purpose                                                                                    |
| ------ | ------------------------------------ | ------------------------------------------------------------------------------------------ |
| Tier 1 | Core Projection Identity and Lineage | Required for all persistent projections                                                    |
| Tier 2 | Materialization and Export Support   | Required for cached, materialized, archived, or exported projections                       |
| Tier 3 | Safety and Lifecycle Extensions      | Required when projections aggregate, redact, track currency, or require validation records |

Tier 1 is the operational core.

Tier 2 is conditional.

Tier 3 is conditional and forward-compatible.

Tier 3 support should not block initial implementation of basic projection generation.

---

# Object Overview

```text
AssertionProjectionBuild
        ↓
AssertionProjection
        ↓
        ├── ProjectionSourceReference[]
        ├── ProjectionTransform[]
        ├── ProjectionLineageReference[]
        ├── ProjectionMaterialization?      # Tier 2
        ├── ProjectionConsumerContext?      # Tier 2
        ├── ProjectionExportReference[]?    # Tier 2
        ├── ProjectionAggregation[]?        # Tier 3
        ├── ProjectionRedaction[]?          # Tier 3
        ├── ProjectionCurrencyState?        # Tier 3
        └── ProjectionValidationRecord[]?   # Tier 3
```

The root object is `AssertionProjection`.

`AssertionProjectionBuild` records the construction context.

`ProjectionSourceReference` and `ProjectionLineageReference` preserve source identity and reconstruction paths.

`ProjectionTransform` records how the view was generated.

Tier 2 objects describe persistence, consumers, and export artifacts.

Tier 3 objects describe aggregation, redaction, currency, and validation state.

---

# Tier 1: Core Projection Identity and Lineage

Tier 1 is required for every persistent projection.

Tier 1 objects:

* `AssertionProjectionBuild`
* `AssertionProjection`
* `ProjectionSourceReference`
* `ProjectionTransform`
* `ProjectionLineageReference`

Tier 1 answers:

* What projection exists?
* What source layer does it represent?
* What source objects does it represent?
* Why does it exist?
* How was it generated?
* How can it be traced back to source truth?

---

# AssertionProjectionBuild

## Purpose

`AssertionProjectionBuild` records the build context used to generate one or more projections.

It identifies the projection implementation, rule set, source VDB generation, source corpus, source builds, and build parameters.

## Object Shape

```yaml
AssertionProjectionBuild:
  projection_build_id: string
  projection_builder_name: string
  projection_builder_version: string
  projection_rule_set_id: string
  projection_rule_set_version: string
  source_vdb_generation_id: string
  source_assertion_corpus_id: string
  source_build_ids: array[string]
  build_scope: string
  build_parameters: object
  built_at: datetime
```

## Field Requirements

| Field                         | Required    | Description                                                           |
| ----------------------------- | ----------- | --------------------------------------------------------------------- |
| `projection_build_id`         | Yes         | Stable identifier for this projection build                           |
| `projection_builder_name`     | Yes         | Name of the projection builder implementation                         |
| `projection_builder_version`  | Yes         | Version of the projection builder implementation                      |
| `projection_rule_set_id`      | Yes         | Projection rule set used                                              |
| `projection_rule_set_version` | Yes         | Version of projection rule set                                        |
| `source_vdb_generation_id`    | Yes         | VDB generation used as source context                                 |
| `source_assertion_corpus_id`  | Recommended | Assertion corpus associated with the source generation                |
| `source_build_ids`            | Recommended | Source topology, geometry, surface, validation, or export builds used |
| `build_scope`                 | Yes         | Scope of the projection build                                         |
| `build_parameters`            | Recommended | Parameters sufficient to reconstruct build behavior                   |
| `built_at`                    | Yes         | Build timestamp or equivalent version marker                          |

## Controlled Vocabulary: `build_scope`

Recommended values:

* `corpus_wide`
* `participant_scoped`
* `phenotype_scoped`
* `surface_scoped`
* `producer_scoped`
* `lineage_scoped`
* `validation_scoped`
* `export_scoped`
* `release_scoped`
* `operator_scoped`

## Invariant

A projection build identifies the implementation context used to generate projections.

It does not identify source truth.

---

# AssertionProjection

## Purpose

`AssertionProjection` is the root projection object.

It identifies a purpose-bound view over preserved assertions or governed derived layers.

## Object Shape

```yaml
AssertionProjection:
  projection_id: string
  projection_build_id: string
  projection_kind: string
  projection_purpose: string
  projection_label: string
  projection_description: string
  primary_source_layer: string
  projection_representation: string
  materialization_mode: string
  projection_status: string
  source_generation_id: string
  created_at: datetime
```

## Field Requirements

| Field                       | Required    | Description                                      |
| --------------------------- | ----------- | ------------------------------------------------ |
| `projection_id`             | Yes         | Stable identifier for the projection view        |
| `projection_build_id`       | Recommended | Build that produced the projection               |
| `projection_kind`           | Yes         | Projection class or family                       |
| `projection_purpose`        | Yes         | Declared reason the projection exists            |
| `projection_label`          | Recommended | Human-readable label                             |
| `projection_description`    | Optional    | Non-interpretive projection description          |
| `primary_source_layer`      | Yes         | Governed VDB layer directly projected            |
| `projection_representation` | Yes         | Representation form                              |
| `materialization_mode`      | Yes         | Persistence / lifecycle mode                     |
| `projection_status`         | Yes         | Current projection lifecycle status              |
| `source_generation_id`      | Yes         | Source VDB generation or source-layer generation |
| `created_at`                | Yes         | Projection creation timestamp or version marker  |

## Controlled Vocabulary: `projection_kind`

Recommended values:

* `assertion_centered_projection`
* `participant_centered_projection`
* `provenance_projection`
* `epistemic_projection`
* `stratum_projection`
* `topology_projection`
* `geometry_projection`
* `surface_projection`
* `export_projection`
* `visualization_projection`
* `validation_projection`
* `release_projection`

## Controlled Vocabulary: `projection_purpose`

Recommended values:

* `audit`
* `query`
* `visualization`
* `export`
* `reasoning_input`
* `validation`
* `review`
* `operator_status`
* `interoperability`
* `release`
* `documentation`
* `debugging`

## Controlled Vocabulary: `primary_source_layer`

Recommended values:

* `assertion`
* `topology`
* `geometry`
* `surface`
* `corpus`
* `generation`
* `lineage`
* `validation`
* `export_package`

## Controlled Vocabulary: `projection_representation`

Recommended values:

* `table`
* `json`
* `yaml`
* `graph`
* `hypergraph`
* `matrix`
* `network`
* `timeline`
* `summary`
* `index`
* `report`
* `dashboard`
* `figure`
* `package`
* `manifest`
* `validation_report`

## Controlled Vocabulary: `materialization_mode`

Recommended values:

* `ephemeral`
* `cached`
* `materialized`
* `exported`
* `archived`

## Controlled Vocabulary: `projection_status`

Recommended values:

* `active`
* `historical`
* `stale`
* `superseded`
* `invalid`
* `archived`
* `not_evaluated`

## Invariants

An `AssertionProjection` must:

* have projection identity
* declare projection kind
* declare projection purpose
* declare primary source layer
* declare representation
* declare materialization mode
* preserve source generation
* avoid biological, clinical, statistical, causal, or mechanistic interpretation

Projection identity must not replace source identity.

---

# ProjectionSourceReference

## Purpose

`ProjectionSourceReference` records the direct source objects, corpora, builds, or reconstruction queries represented by a projection.

It answers:

> What source content does this projection represent?

## Object Shape

```yaml
ProjectionSourceReference:
  projection_source_reference_id: string
  projection_id: string
  source_layer: string
  source_role: string
  source_object_id: string
  source_object_type: string
  source_namespace: string
  source_generation_id: string
  source_build_id: string
  source_corpus_id: string
  reconstruction_query_id: string
  reconstruction_query: string
```

## Field Requirements

| Field                            | Required    | Description                                        |
| -------------------------------- | ----------- | -------------------------------------------------- |
| `projection_source_reference_id` | Yes         | Stable identifier for this source reference        |
| `projection_id`                  | Yes         | Projection to which source applies                 |
| `source_layer`                   | Yes         | Source layer represented                           |
| `source_role`                    | Yes         | Role of source in projection                       |
| `source_object_id`               | Conditional | Required when source object is enumerated          |
| `source_object_type`             | Recommended | Type of source object                              |
| `source_namespace`               | Recommended | Namespace for source object identity               |
| `source_generation_id`           | Yes         | Source generation represented                      |
| `source_build_id`                | Conditional | Required when source derives from a build          |
| `source_corpus_id`               | Conditional | Required when source is corpus-scoped              |
| `reconstruction_query_id`        | Conditional | Required when source set is represented by query   |
| `reconstruction_query`           | Conditional | Query or rule sufficient to reconstruct source set |

At least one of the following must be present:

* `source_object_id`
* `source_corpus_id`
* `source_build_id`
* `reconstruction_query_id`
* `reconstruction_query`

## Controlled Vocabulary: `source_layer`

Recommended values:

* `assertion`
* `topology`
* `geometry`
* `surface`
* `corpus`
* `generation`
* `lineage`
* `validation`
* `export_package`

## Controlled Vocabulary: `source_role`

Recommended values:

* `primary_source`
* `secondary_source`
* `lineage_source`
* `aggregation_source`
* `display_source`
* `export_source`
* `validation_source`

## Invariants

Every projection must have at least one `ProjectionSourceReference`.

If source objects are not enumerated, a reconstruction query, corpus reference, build reference, or manifest-equivalent source reference must exist.

---

# ProjectionTransform

## Purpose

`ProjectionTransform` records how source content was converted into a projection.

It answers:

> How was the source represented as this view?

## Object Shape

```yaml
ProjectionTransform:
  projection_transform_id: string
  projection_id: string
  transform_kind: string
  transform_basis: string
  transform_name: string
  transform_version: string
  transform_parameters: object
  transform_lossiness: string
  omitted_content_classes: array[string]
  reconstruction_supported: boolean
```

## Field Requirements

| Field                      | Required    | Description                                        |
| -------------------------- | ----------- | -------------------------------------------------- |
| `projection_transform_id`  | Yes         | Stable identifier for transform record             |
| `projection_id`            | Yes         | Projection to which transform applies              |
| `transform_kind`           | Yes         | Transform class                                    |
| `transform_basis`          | Recommended | Reason this transform is appropriate for purpose   |
| `transform_name`           | Recommended | Human-readable transform name                      |
| `transform_version`        | Recommended | Transform version                                  |
| `transform_parameters`     | Recommended | Parameters used by transform                       |
| `transform_lossiness`      | Yes         | Declared lossiness state                           |
| `omitted_content_classes`  | Conditional | Required for lossy or redacted projections         |
| `reconstruction_supported` | Yes         | Whether reconstruction of source view is supported |

## Controlled Vocabulary: `transform_kind`

Recommended values:

* `filter`
* `group`
* `sort`
* `summarize`
* `aggregate`
* `reshape`
* `serialize`
* `index`
* `redact`
* `label`
* `visualize`
* `package`

## Controlled Vocabulary: `transform_basis`

Recommended values:

* `query_filter`
* `audit_grouping`
* `validation_summary`
* `export_serialization`
* `visualization_layout`
* `reasoning_input_packaging`
* `operator_status_summary`
* `release_snapshot`
* `interoperability_conversion`

## Controlled Vocabulary: `transform_lossiness`

Recommended values:

* `lossless`
* `controlled_lossy`
* `redacted`
* `summary_only`
* `unknown`

## Invariants

Every projection must declare at least one `ProjectionTransform`.

Lossy transforms must declare lossiness.

Redacted transforms must declare omitted content classes.

A projection transform must not silently alter scientific meaning.

---

# ProjectionLineageReference

## Purpose

`ProjectionLineageReference` records the reconstruction chain from a projection back through governed VDB layers.

It answers:

> How can this projection be traced back to source truth?

## Object Shape

```yaml
ProjectionLineageReference:
  projection_lineage_reference_id: string
  projection_id: string
  lineage_kind: string
  lineage_role: string
  source_id: string
  source_type: string
  source_layer: string
  source_namespace: string
  source_build_id: string
  source_generation_id: string
```

## Field Requirements

| Field                             | Required    | Description                                    |
| --------------------------------- | ----------- | ---------------------------------------------- |
| `projection_lineage_reference_id` | Yes         | Stable identifier for lineage reference        |
| `projection_id`                   | Yes         | Projection to which lineage applies            |
| `lineage_kind`                    | Yes         | Kind of lineage object                         |
| `lineage_role`                    | Yes         | Role in reconstruction chain                   |
| `source_id`                       | Yes         | Identifier of source lineage object            |
| `source_type`                     | Recommended | Type of source lineage object                  |
| `source_layer`                    | Yes         | VDB layer associated with source               |
| `source_namespace`                | Recommended | Namespace for source object                    |
| `source_build_id`                 | Conditional | Build associated with source, where applicable |
| `source_generation_id`            | Recommended | Generation associated with source              |

## Controlled Vocabulary: `lineage_kind`

Recommended values:

* `assertion_record`
* `topology_relationship`
* `convergence_region`
* `geometry_feature`
* `structural_motif`
* `convergence_profile`
* `evidence_convergence_surface`
* `surface_export_package`
* `producer_tep`
* `producer_artifact`
* `assertion_corpus`
* `vdb_generation`

## Controlled Vocabulary: `lineage_role`

Recommended values:

* `direct_source`
* `upstream_source`
* `reconstruction_source`
* `audit_source`
* `display_source`
* `export_source`
* `aggregation_basis`
* `validation_basis`

## Invariants

Every persistent projection must preserve lineage sufficient to reach its source layer.

A projection over a derived layer must preserve lineage sufficient to reach Assertion Records through governed upstream layers.

Lineage may be explicit or resolvable through build IDs, manifests, or lineage records.

---

# Tier 2: Materialization and Export Support

Tier 2 applies when projections are cached, materialized, archived, exported, or generated for a declared consumer.

Tier 2 objects:

* `ProjectionMaterialization`
* `ProjectionConsumerContext`
* `ProjectionExportReference`

Tier 2 should be implemented when projection outputs persist beyond ephemeral query execution or leave VDB as transport artifacts.

---

# ProjectionMaterialization

## Purpose

`ProjectionMaterialization` records persistence and lifecycle information for a projection.

It answers:

> Is this projection persisted, where is it, and under what lifecycle conditions?

## Object Shape

```yaml
ProjectionMaterialization:
  projection_materialization_id: string
  projection_id: string
  materialization_mode: string
  materialization_status: string
  materialized_at: datetime
  materialized_artifact_uri: string
  cache_policy_id: string
  invalidation_basis: string
  source_currency_at_materialization: string
```

## Field Requirements

| Field                                | Required    | Description                                  |
| ------------------------------------ | ----------- | -------------------------------------------- |
| `projection_materialization_id`      | Yes         | Stable identifier for materialization record |
| `projection_id`                      | Yes         | Projection being materialized                |
| `materialization_mode`               | Yes         | Materialization mode                         |
| `materialization_status`             | Yes         | Current materialization lifecycle state      |
| `materialized_at`                    | Conditional | Required for persisted projections           |
| `materialized_artifact_uri`          | Optional    | Path or URI to artifact                      |
| `cache_policy_id`                    | Optional    | Cache policy used                            |
| `invalidation_basis`                 | Recommended | Basis for invalidation or staleness          |
| `source_currency_at_materialization` | Recommended | Currency state when materialized             |

## Controlled Vocabulary: `materialization_status`

Recommended values:

* `active`
* `expired`
* `invalidated`
* `archived`
* `superseded`
* `failed`

## Controlled Vocabulary: `invalidation_basis`

Recommended values:

* `source_generation_change`
* `transform_version_change`
* `policy_change`
* `operator_invalidated`
* `not_applicable`
* `not_evaluated`

## Invariant

Materialization must not confer authority.

A materialized projection remains derived.

---

# ProjectionConsumerContext

## Purpose

`ProjectionConsumerContext` records the intended consumer or workflow for a projection.

It answers:

> Who or what is this projection generated to serve?

## Object Shape

```yaml
ProjectionConsumerContext:
  projection_consumer_context_id: string
  projection_id: string
  consumer_class: string
  consumer_name: string
  consumer_contract_id: string
  disclosure_policy_id: string
  required_lineage_depth: string
  required_representation: string
```

## Field Requirements

| Field                            | Required    | Description                            |
| -------------------------------- | ----------- | -------------------------------------- |
| `projection_consumer_context_id` | Yes         | Stable identifier for consumer context |
| `projection_id`                  | Yes         | Projection to which context applies    |
| `consumer_class`                 | Yes         | Consumer class                         |
| `consumer_name`                  | Optional    | Specific consumer name                 |
| `consumer_contract_id`           | Optional    | Consumer contract governing projection |
| `disclosure_policy_id`           | Optional    | Disclosure policy applied              |
| `required_lineage_depth`         | Recommended | Required lineage depth                 |
| `required_representation`        | Recommended | Required representation format         |

## Controlled Vocabulary: `consumer_class`

Recommended values:

* `vdb_operator`
* `rdgp`
* `sage`
* `validation_workflow`
* `visualization_layer`
* `external_export_consumer`
* `human_reviewer`
* `future_reasoning_engine`
* `release_workflow`
* `audit_workflow`

## Controlled Vocabulary: `required_lineage_depth`

Recommended values:

* `projection_only`
* `source_layer`
* `derived_layer`
* `assertion_record`
* `producer_tep`
* `producer_artifact`

## Invariant

Consumer context may affect projection format or disclosure.

It must not alter source truth.

---

# ProjectionExportReference

## Purpose

`ProjectionExportReference` records outbound transport artifacts emitted from projections.

It answers:

> What artifact was emitted from this projection?

## Object Shape

```yaml
ProjectionExportReference:
  projection_export_reference_id: string
  projection_id: string
  export_package_id: string
  export_artifact_uri: string
  export_format: string
  export_reason: string
  consumer_name: string
  exported_at: datetime
  export_status: string
```

## Field Requirements

| Field                            | Required    | Description                                   |
| -------------------------------- | ----------- | --------------------------------------------- |
| `projection_export_reference_id` | Yes         | Stable identifier for export reference        |
| `projection_id`                  | Yes         | Projection that produced the export           |
| `export_package_id`              | Yes         | Export package identifier                     |
| `export_artifact_uri`            | Optional    | Path or URI to exported artifact              |
| `export_format`                  | Yes         | Export serialization or package format        |
| `export_reason`                  | Yes         | Reason export was generated                   |
| `consumer_name`                  | Recommended | Intended consumer                             |
| `exported_at`                    | Yes         | Export timestamp or equivalent version marker |
| `export_status`                  | Yes         | Export lifecycle status                       |

## Controlled Vocabulary: `export_reason`

Recommended values:

* `initial_reasoning_package`
* `refresh_package`
* `audit_export`
* `validation_export`
* `release_export`
* `operator_requested_export`
* `external_interoperability_export`

## Controlled Vocabulary: `export_status`

Recommended values:

* `planned`
* `emitted`
* `consumed`
* `superseded`
* `failed`
* `archived`

## Invariant

Export packages are projection artifacts.

They are not source truth.

---

# Tier 3: Safety and Lifecycle Extensions

Tier 3 applies when projections aggregate, redact, track source currency, or carry validation results.

Tier 3 objects:

* `ProjectionAggregation`
* `ProjectionRedaction`
* `ProjectionCurrencyState`
* `ProjectionValidationRecord`

Tier 3 support is architecturally reserved but should not block initial projection implementation.

---

# ProjectionAggregation

## Purpose

`ProjectionAggregation` records counts, summaries, groupings, or aggregate values represented in a projection.

It answers:

> What was counted, grouped, summarized, or aggregated?

## Object Shape

```yaml
ProjectionAggregation:
  projection_aggregation_id: string
  projection_id: string
  aggregation_kind: string
  aggregation_basis: string
  source_object_set_reference: string
  source_object_count: integer
  aggregation_scope: string
  aggregation_complete: boolean
  aggregation_value_name: string
  aggregation_value: string
```

## Field Requirements

| Field                         | Required    | Description                                        |
| ----------------------------- | ----------- | -------------------------------------------------- |
| `projection_aggregation_id`   | Yes         | Stable identifier for aggregation record           |
| `projection_id`               | Yes         | Projection containing aggregation                  |
| `aggregation_kind`            | Yes         | Aggregation class                                  |
| `aggregation_basis`           | Yes         | Basis for aggregation                              |
| `source_object_set_reference` | Yes         | Source set or reconstruction query used            |
| `source_object_count`         | Recommended | Number of source objects represented               |
| `aggregation_scope`           | Yes         | Scope over which aggregation was computed          |
| `aggregation_complete`        | Yes         | Whether aggregation covers complete declared scope |
| `aggregation_value_name`      | Yes         | Name of aggregate value                            |
| `aggregation_value`           | Yes         | Aggregate value                                    |

## Controlled Vocabulary: `aggregation_kind`

Recommended values:

* `count`
* `group_count`
* `summary_statistic`
* `presence_absence`
* `feature_summary`
* `stratum_summary`
* `producer_summary`
* `participant_summary`
* `lineage_summary`

## Controlled Vocabulary: `aggregation_basis`

Recommended values:

* `count_assertions_by_participant`
* `count_assertions_by_producer`
* `count_strata_by_surface`
* `count_surfaces_by_currency_state`
* `summarize_geometry_features`
* `summarize_lineage_completeness`
* `summarize_validation_status`

## Invariant

Aggregations must preserve source set reference or reconstruction query.

Aggregations must not become unlabeled support scores.

---

# ProjectionRedaction

## Purpose

`ProjectionRedaction` records withheld content, redaction policy, and source reconstruction references.

It answers:

> What was withheld, under what policy, and can the full source still be resolved?

## Object Shape

```yaml
ProjectionRedaction:
  projection_redaction_id: string
  projection_id: string
  redaction_policy_id: string
  redaction_basis: string
  redacted_element_classes: array[string]
  redaction_scope: string
  unredacted_source_reference: string
  redaction_reason: string
```

## Field Requirements

| Field                         | Required    | Description                                                  |
| ----------------------------- | ----------- | ------------------------------------------------------------ |
| `projection_redaction_id`     | Yes         | Stable identifier for redaction record                       |
| `projection_id`               | Yes         | Projection containing redaction                              |
| `redaction_policy_id`         | Yes         | Redaction policy applied                                     |
| `redaction_basis`             | Yes         | Basis for redaction                                          |
| `redacted_element_classes`    | Yes         | Classes of elements redacted                                 |
| `redaction_scope`             | Yes         | Scope of redaction                                           |
| `unredacted_source_reference` | Recommended | Reference to upstream unredacted source or privileged source |
| `redaction_reason`            | Recommended | Non-interpretive reason for redaction                        |

## Controlled Vocabulary: `redaction_basis`

Recommended values:

* `consumer_contract`
* `privacy_policy`
* `external_export_policy`
* `summary_only_policy`
* `operator_policy`
* `not_applicable`

## Invariant

A redacted projection must not present itself as complete source truth.

Redaction must not alter source identity.

---

# ProjectionCurrencyState

## Purpose

`ProjectionCurrencyState` records whether a projection is current relative to its declared source layer, transform, and policy.

Projection currency is metadata-derived.

It is not meaning-derived.

## Object Shape

```yaml
ProjectionCurrencyState:
  projection_currency_state_id: string
  projection_id: string
  currency_state: string
  source_generation_at_projection: string
  current_source_generation: string
  transform_version_at_projection: string
  current_transform_version: string
  policy_version_at_projection: string
  current_policy_version: string
  currency_basis: string
  currency_evaluated_at: datetime
```

## Field Requirements

| Field                             | Required    | Description                                      |
| --------------------------------- | ----------- | ------------------------------------------------ |
| `projection_currency_state_id`    | Yes         | Stable identifier for currency state record      |
| `projection_id`                   | Yes         | Projection whose currency is represented         |
| `currency_state`                  | Yes         | Current currency state                           |
| `source_generation_at_projection` | Recommended | Source generation used when projection was built |
| `current_source_generation`       | Recommended | Current source generation when evaluated         |
| `transform_version_at_projection` | Recommended | Transform version used when projection was built |
| `current_transform_version`       | Recommended | Current transform version when evaluated         |
| `policy_version_at_projection`    | Optional    | Policy version used when projection was built    |
| `current_policy_version`          | Optional    | Current policy version when evaluated            |
| `currency_basis`                  | Yes         | Metadata comparison used                         |
| `currency_evaluated_at`           | Yes         | Timestamp or version marker for evaluation       |

## Controlled Vocabulary: `currency_state`

Recommended values:

* `current`
* `historical`
* `stale_due_to_source_change`
* `stale_due_to_transform_change`
* `stale_due_to_policy_change`
* `stale_due_to_multiple_changes`
* `not_evaluated`

## Controlled Vocabulary: `currency_basis`

Recommended values:

* `source_generation_match`
* `source_generation_mismatch`
* `transform_version_match`
* `transform_version_mismatch`
* `policy_version_match`
* `policy_version_mismatch`
* `historical_projection`
* `not_evaluated`

## Invariant

Projection currency must be metadata-derived.

Projection currency must not be determined from biological meaning.

---

# ProjectionValidationRecord

## Purpose

`ProjectionValidationRecord` records projection safety, completeness, and conformance checks.

It answers:

> Was the projection valid, incomplete, stale, or unsafe?

## Object Shape

```yaml
ProjectionValidationRecord:
  projection_validation_record_id: string
  projection_id: string
  validation_status: string
  validation_check_id: string
  validation_check_version: string
  validation_issue_kind: string
  validation_message: string
  validated_at: datetime
```

## Field Requirements

| Field                             | Required    | Description                                |
| --------------------------------- | ----------- | ------------------------------------------ |
| `projection_validation_record_id` | Yes         | Stable identifier for validation record    |
| `projection_id`                   | Yes         | Projection being validated                 |
| `validation_status`               | Yes         | Validation outcome                         |
| `validation_check_id`             | Yes         | Validation check identifier                |
| `validation_check_version`        | Recommended | Version of validation check                |
| `validation_issue_kind`           | Conditional | Required when status is warning or invalid |
| `validation_message`              | Recommended | Human-readable non-interpretive message    |
| `validated_at`                    | Yes         | Validation timestamp or version marker     |

## Controlled Vocabulary: `validation_status`

Recommended values:

* `valid`
* `warning`
* `invalid`
* `not_evaluated`

## Controlled Vocabulary: `validation_issue_kind`

Recommended values:

* `missing_source_layer`
* `missing_source_identity`
* `missing_purpose`
* `missing_transform`
* `missing_lineage`
* `unreconstructable_projection`
* `semantic_collapse`
* `authority_transfer_risk`
* `stale_projection_state`
* `forbidden_interpretation`
* `incomplete_disclosure`
* `invalid_export`
* `lossiness_not_declared`
* `aggregation_basis_missing`
* `redaction_basis_missing`

## Invariant

Validation records may classify projection safety.

They must not classify biological meaning.

---

# Controlled Vocabulary Summary

## Projection Kinds

* `assertion_centered_projection`
* `participant_centered_projection`
* `provenance_projection`
* `epistemic_projection`
* `stratum_projection`
* `topology_projection`
* `geometry_projection`
* `surface_projection`
* `export_projection`
* `visualization_projection`
* `validation_projection`
* `release_projection`

## Projection Purposes

* `audit`
* `query`
* `visualization`
* `export`
* `reasoning_input`
* `validation`
* `review`
* `operator_status`
* `interoperability`
* `release`
* `documentation`
* `debugging`

## Source Layers

* `assertion`
* `topology`
* `geometry`
* `surface`
* `corpus`
* `generation`
* `lineage`
* `validation`
* `export_package`

## Transform Kinds

* `filter`
* `group`
* `sort`
* `summarize`
* `aggregate`
* `reshape`
* `serialize`
* `index`
* `redact`
* `label`
* `visualize`
* `package`

## Materialization Modes

* `ephemeral`
* `cached`
* `materialized`
* `exported`
* `archived`

## Projection Currency States

* `current`
* `historical`
* `stale_due_to_source_change`
* `stale_due_to_transform_change`
* `stale_due_to_policy_change`
* `stale_due_to_multiple_changes`
* `not_evaluated`

---

# Example 1: POLG Assertion Query Projection

This example represents an assertion-centered query projection over POLG-associated Assertion Records.

```yaml
AssertionProjection:
  projection_id: "projection_POLG_assertion_query_0001"
  projection_build_id: "projection_build_2026_06_26_001"
  projection_kind: "assertion_centered_projection"
  projection_purpose: "query"
  projection_label: "POLG assertion query projection"
  projection_description: "Query projection listing Assertion Records involving POLG."
  primary_source_layer: "assertion"
  projection_representation: "table"
  materialization_mode: "ephemeral"
  projection_status: "active"
  source_generation_id: "vdb_generation_001"
  created_at: "2026-06-26T00:00:00Z"

ProjectionSourceReference:
  projection_source_reference_id: "source_POLG_assertions_0001"
  projection_id: "projection_POLG_assertion_query_0001"
  source_layer: "assertion"
  source_role: "primary_source"
  source_corpus_id: "assertion_corpus_001"
  reconstruction_query_id: "query_assertions_by_participant_POLG_v1"
  reconstruction_query: "participant_namespace = 'HGNC_SYMBOL' AND participant_value = 'POLG'"
  source_generation_id: "vdb_generation_001"

ProjectionTransform:
  projection_transform_id: "transform_POLG_assertion_filter_0001"
  projection_id: "projection_POLG_assertion_query_0001"
  transform_kind: "filter"
  transform_basis: "query_filter"
  transform_name: "filter_assertions_by_participant"
  transform_version: "v1"
  transform_parameters:
    participant_namespace: "HGNC_SYMBOL"
    participant_value: "POLG"
  transform_lossiness: "lossless"
  omitted_content_classes: []
  reconstruction_supported: true
```

This projection is a view over assertions.

It does not replace the Assertion Records.

---

# Example 2: RDGP TEP-VDB Export Projection

This example represents an export projection generated from an Evidence Convergence Surface for RDGP.

```yaml
AssertionProjection:
  projection_id: "projection_POLG_surface_rdgp_export_0001"
  projection_build_id: "projection_build_2026_06_27_001"
  projection_kind: "export_projection"
  projection_purpose: "reasoning_input"
  projection_label: "POLG RDGP export projection"
  projection_description: "Surface-derived export projection for RDGP reasoning input."
  primary_source_layer: "surface"
  projection_representation: "package"
  materialization_mode: "exported"
  projection_status: "active"
  source_generation_id: "vdb_generation_002"
  created_at: "2026-06-27T00:00:00Z"

ProjectionSourceReference:
  projection_source_reference_id: "source_POLG_surface_export_0001"
  projection_id: "projection_POLG_surface_rdgp_export_0001"
  source_layer: "surface"
  source_role: "primary_source"
  source_object_id: "surface_POLG_primary_0001"
  source_object_type: "EvidenceConvergenceSurface"
  source_generation_id: "surface_generation_001"
  source_build_id: "surface_build_2026_06_26_001"
  source_corpus_id: "assertion_corpus_001"

ProjectionTransform:
  projection_transform_id: "transform_POLG_surface_package_0001"
  projection_id: "projection_POLG_surface_rdgp_export_0001"
  transform_kind: "package"
  transform_basis: "reasoning_input_packaging"
  transform_name: "package_surface_for_rdgp"
  transform_version: "v1"
  transform_parameters:
    consumer: "RDGP"
    lineage_depth: "assertion_record"
    include_evidence_strata: true
  transform_lossiness: "controlled_lossy"
  omitted_content_classes:
    - "internal_vdb_cache_metadata"
  reconstruction_supported: true

ProjectionConsumerContext:
  projection_consumer_context_id: "consumer_POLG_rdgp_0001"
  projection_id: "projection_POLG_surface_rdgp_export_0001"
  consumer_class: "rdgp"
  consumer_name: "RDGP"
  consumer_contract_id: "consumer_contract_rdgp_v1"
  disclosure_policy_id: "disclosure_policy_rdgp_v1"
  required_lineage_depth: "assertion_record"
  required_representation: "package"

ProjectionExportReference:
  projection_export_reference_id: "export_POLG_rdgp_0001"
  projection_id: "projection_POLG_surface_rdgp_export_0001"
  export_package_id: "tep_vdb_POLG_rdgp_0001"
  export_artifact_uri: "results/teps/vdb/polg/tep_vdb_POLG_rdgp_0001.json"
  export_format: "json"
  export_reason: "initial_reasoning_package"
  consumer_name: "RDGP"
  exported_at: "2026-06-27T00:05:00Z"
  export_status: "emitted"
```

The TEP-VDB export is a transport artifact.

It is not the source surface.

---

# Example 3: Operator Dashboard Projection

This example represents a cached dashboard projection summarizing surface refresh states.

```yaml
AssertionProjection:
  projection_id: "projection_surface_refresh_dashboard_0001"
  projection_build_id: "projection_build_2026_07_01_001"
  projection_kind: "visualization_projection"
  projection_purpose: "operator_status"
  projection_label: "Surface refresh dashboard projection"
  projection_description: "Dashboard view summarizing reasoning currency and refresh trigger state."
  primary_source_layer: "surface"
  projection_representation: "dashboard"
  materialization_mode: "cached"
  projection_status: "active"
  source_generation_id: "vdb_generation_003"
  created_at: "2026-07-01T00:00:00Z"

ProjectionTransform:
  projection_transform_id: "transform_refresh_dashboard_0001"
  projection_id: "projection_surface_refresh_dashboard_0001"
  transform_kind: "summarize"
  transform_basis: "operator_status_summary"
  transform_name: "summarize_surface_refresh_states"
  transform_version: "v1"
  transform_parameters:
    group_by:
      - "currency_state"
      - "refresh_trigger_kind"
  transform_lossiness: "summary_only"
  omitted_content_classes:
    - "full_assertion_payload"
    - "full_geometry_payload"
  reconstruction_supported: true

ProjectionMaterialization:
  projection_materialization_id: "materialization_refresh_dashboard_0001"
  projection_id: "projection_surface_refresh_dashboard_0001"
  materialization_mode: "cached"
  materialization_status: "active"
  materialized_at: "2026-07-01T00:00:00Z"
  materialized_artifact_uri: "cache/projections/surface_refresh_dashboard.json"
  cache_policy_id: "cache_policy_operator_dashboard_v1"
  invalidation_basis: "source_generation_change"
  source_currency_at_materialization: "current"
```

This projection supports operator review.

It is not an authoritative evidence object.

---

# Example 4: Validation Projection

This example represents a validation projection identifying surfaces missing eligibility records.

```yaml
AssertionProjection:
  projection_id: "projection_missing_surface_eligibility_0001"
  projection_build_id: "projection_build_validation_2026_06_27_001"
  projection_kind: "validation_projection"
  projection_purpose: "validation"
  projection_label: "Missing surface eligibility validation projection"
  projection_description: "Validation projection listing surfaces lacking SurfaceEligibility records."
  primary_source_layer: "surface"
  projection_representation: "validation_report"
  materialization_mode: "materialized"
  projection_status: "active"
  source_generation_id: "vdb_generation_002"
  created_at: "2026-06-27T00:00:00Z"

ProjectionTransform:
  projection_transform_id: "transform_missing_surface_eligibility_0001"
  projection_id: "projection_missing_surface_eligibility_0001"
  transform_kind: "filter"
  transform_basis: "validation_summary"
  transform_name: "find_surfaces_missing_eligibility"
  transform_version: "v1"
  transform_parameters:
    condition: "surface has no SurfaceEligibility record"
  transform_lossiness: "lossless"
  omitted_content_classes: []
  reconstruction_supported: true

ProjectionValidationRecord:
  projection_validation_record_id: "validation_missing_surface_eligibility_0001"
  projection_id: "projection_missing_surface_eligibility_0001"
  validation_status: "valid"
  validation_check_id: "check_surface_eligibility_presence"
  validation_check_version: "v1"
  validation_issue_kind: "missing_source_identity"
  validation_message: "Projection successfully identifies surfaces missing SurfaceEligibility records."
  validated_at: "2026-06-27T00:05:00Z"
```

This projection reports a system conformance issue.

It does not make biological claims.

---

# Example 5: Aggregated Projection

This example represents an aggregate participant-centered projection counting assertions by producer for POLG.

```yaml
AssertionProjection:
  projection_id: "projection_POLG_assertion_count_by_producer_0001"
  projection_build_id: "projection_build_2026_06_26_002"
  projection_kind: "participant_centered_projection"
  projection_purpose: "review"
  projection_label: "POLG assertion count by producer"
  projection_description: "Aggregate projection counting POLG-associated assertions by producer."
  primary_source_layer: "assertion"
  projection_representation: "table"
  materialization_mode: "materialized"
  projection_status: "active"
  source_generation_id: "vdb_generation_001"
  created_at: "2026-06-26T00:00:00Z"

ProjectionAggregation:
  projection_aggregation_id: "aggregation_POLG_by_producer_0001"
  projection_id: "projection_POLG_assertion_count_by_producer_0001"
  aggregation_kind: "group_count"
  aggregation_basis: "count_assertions_by_producer"
  source_object_set_reference: "query_assertions_by_participant_POLG_v1"
  source_object_count: 13
  aggregation_scope: "POLG-associated Assertion Records in assertion_corpus_001"
  aggregation_complete: true
  aggregation_value_name: "assertion_count_by_producer"
  aggregation_value: "VAP=4;GSC=7;RDGP=2"
```

This aggregate is a review view.

It is not a support score.

---

# Example 6: Redacted Export Projection

This example represents a redacted export projection for an external consumer.

```yaml
AssertionProjection:
  projection_id: "projection_external_redacted_surface_export_0001"
  projection_build_id: "projection_build_2026_07_15_001"
  projection_kind: "export_projection"
  projection_purpose: "interoperability"
  projection_label: "External redacted surface export projection"
  projection_description: "Redacted export projection for external interoperability review."
  primary_source_layer: "surface"
  projection_representation: "json"
  materialization_mode: "exported"
  projection_status: "active"
  source_generation_id: "vdb_generation_004"
  created_at: "2026-07-15T00:00:00Z"

ProjectionRedaction:
  projection_redaction_id: "redaction_external_surface_0001"
  projection_id: "projection_external_redacted_surface_export_0001"
  redaction_policy_id: "external_export_policy_v1"
  redaction_basis: "external_export_policy"
  redacted_element_classes:
    - "internal_build_paths"
    - "operator_notes"
  redaction_scope: "external interoperability export"
  unredacted_source_reference: "surface_POLG_primary_0001"
  redaction_reason: "Remove internal operational fields for external export."

ProjectionTransform:
  projection_transform_id: "transform_external_redacted_surface_0001"
  projection_id: "projection_external_redacted_surface_export_0001"
  transform_kind: "redact"
  transform_basis: "interoperability_conversion"
  transform_name: "redact_surface_for_external_export"
  transform_version: "v1"
  transform_parameters:
    redaction_policy_id: "external_export_policy_v1"
  transform_lossiness: "redacted"
  omitted_content_classes:
    - "internal_build_paths"
    - "operator_notes"
  reconstruction_supported: true
```

This projection is intentionally redacted.

It must not present itself as complete source truth.

---

# Schema Maturity Requirements

## Tier 1 Required

All persistent projections must support Tier 1.

Tier 1 enables:

* projection identity
* source layer declaration
* source identity or reconstruction path
* projection purpose
* projection transform
* lineage reference
* reconstructability

## Tier 2 Conditional

Tier 2 is required when projections are cached, materialized, archived, exported, or consumer-specific.

Tier 2 enables:

* materialization lifecycle
* consumer contract tracking
* export artifact tracking

## Tier 3 Conditional / Forward-Compatible

Tier 3 is required when projections aggregate, redact, track source currency, or carry validation records.

Tier 3 enables:

* aggregation safety
* redaction safety
* projection currency tracking
* projection validation

Tier 3 support is architecturally reserved but should not block first operational projection implementation.

---

# Schema Invariants

A valid assertion projection schema must satisfy the following invariants.

## Projection Identity

Every persistent projection must have stable projection identity.

## Source Identity

Every projection must preserve source identity or source reconstruction path.

## Source Layer

Every projection must declare a primary source layer.

## Projection Purpose

Every projection must declare why it exists.

## Projection Transform

Every projection must declare how it was generated.

## Projection Lineage

Every projection must preserve reconstructable lineage to its source.

## Identity Separation

Projection identity must never replace source identity.

## Authority Separation

Projection representation must never confer authority.

## Generation Awareness

Every projection must preserve source generation.

## Controlled Lossiness

Lossy projections must declare lossiness and preserve reconstruction.

## Aggregation Safety

Aggregations must preserve source set reference or reconstruction query.

## Redaction Safety

Redactions must declare policy and must not create replacement truth.

## Currency Safety

Projection currency must be metadata-derived, not meaning-derived.

## Non-Interpretation

No projection field may express biological meaning unless that meaning is itself a preserved source assertion and clearly attributed.

---

# Invalid Structures

The following structures are invalid.

## Projection Without Source Layer

```yaml
AssertionProjection:
  projection_id: "projection_invalid_001"
  primary_source_layer: null
```

A projection must declare its source layer.

---

## Projection Without Source Identity

```yaml
ProjectionSourceReference:
  projection_id: "projection_invalid_002"
  source_object_id: null
  source_corpus_id: null
  source_build_id: null
  reconstruction_query_id: null
  reconstruction_query: null
```

A projection must preserve source identity or reconstruction path.

---

## Projection Without Purpose

```yaml
AssertionProjection:
  projection_id: "projection_invalid_003"
  projection_purpose: null
```

A projection must declare why it exists.

---

## Projection Without Transform

```yaml
AssertionProjection:
  projection_id: "projection_invalid_004"

ProjectionTransform: []
```

A projection must declare how it was generated.

---

## Projection Identity Replacing Source Identity

```yaml
AssertionProjection:
  projection_id: "assertion_gsc_000041"
```

Projection identifiers must not masquerade as source assertion identifiers.

---

## Flattened Evidence Projection

```yaml
AssertionProjection:
  projection_id: "projection_invalid_flat_support_001"
  projection_kind: "participant_centered_projection"

ProjectionAggregation:
  aggregation_value_name: "support_score"
  aggregation_value: "12"
  aggregation_basis: null
```

Aggregated support without source basis risks semantic collapse.

---

## Lossy Projection Without Declared Lossiness

```yaml
ProjectionTransform:
  transform_kind: "summarize"
  transform_lossiness: "lossless"
  omitted_content_classes:
    - "full_assertion_payload"
```

A projection that omits content must declare controlled lossiness.

---

## Redacted Projection Without Policy

```yaml
ProjectionRedaction:
  redaction_policy_id: null
  redacted_element_classes:
    - "internal_build_paths"
```

Redaction must be policy-governed.

---

## Export Projection Without Source Generation

```yaml
AssertionProjection:
  projection_kind: "export_projection"
  projection_purpose: "reasoning_input"
  source_generation_id: null
```

Export projections must preserve source generation.

---

## Visualization Projection Treated as Evidence

```yaml
AssertionProjection:
  projection_kind: "visualization_projection"
  projection_label: "POLG disease-causing evidence"
```

Visualization labels must not encode biological conclusions unless the claim is source-attributed.

---

# Implementation Notes

This schema does not prescribe a database backend.

Objects may be represented as:

* relational tables
* JSON documents
* YAML documents
* graph metadata
* manifest records
* validation reports
* export package metadata
* cached view metadata
* hybrid structures

Storage choices may vary.

Schema obligations do not.

Implementations should preserve identity, source references, transform metadata, lineage, materialization state, and non-authoritative status regardless of storage format.

---

# Summary

The Assertion Projection Taxonomy Schema represents the Projection Layer as a tiered object system.

Tier 1 supports core projection identity, source declaration, transform declaration, and lineage.

Tier 2 supports materialized, cached, archived, exported, and consumer-specific projections.

Tier 3 supports aggregation safety, redaction safety, projection currency, and validation records.

Together, these tiers allow VDB to generate many useful views over one preserved truth substrate.

The central boundary is:

```text
Projection changes representation.
Projection does not change authority.
```

A projection may improve access.

It may improve usability.

It may improve transport.

It may improve visualization.

It must not become truth.

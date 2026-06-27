# Evidence Convergence Surface Schema

## Epoch III: Discovery Layer

| Epoch | Epoch Identity      | Epoch Purpose                                                                                       |
| ----- | ------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer         | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry   | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | **Discovery Layer** | **How do preserved evidence topologies become discoverable?**                                       |
| IV    | Projection Layer    | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer     | Why do we do this?                                                                                  |

---

## Schema Status

This document defines the schema structure for Evidence Convergence Surfaces.

It is downstream of:

* `docs/design/evidence_convergence_surface_model.md`
* `docs/implementation/specifications/evidence_convergence_surface_spec.md`
* `docs/design/convergence_geometry_model.md`
* `docs/implementation/schemas/convergence_geometry_schema.md`
* `docs/design/evidence_topology_model.md`
* `docs/implementation/schemas/evidence_topology_schema.md`
* `docs/design/assertion_record_and_projection_model.md`
* `docs/implementation/schemas/assertion_record_schema.md`

This schema is not a storage-backend requirement.

It defines semantic object structure, required fields, optional extensions, controlled vocabularies, examples, and invalid structures.

---

# Purpose

Evidence Convergence Surfaces are governed exposure objects over Convergence Geometry.

They expose deterministic reasoning capacity for downstream systems while preserving:

* geometry lineage
* topology lineage
* assertion lineage
* surface eligibility
* surface disclosure basis
* evidence strata
* surface generation
* reasoning provenance
* reasoning currency
* refresh state

This schema defines the objects required to represent those obligations.

---

# Schema Design Principle

The Evidence Convergence Surface schema uses a tiered structure.

This allows VDB to support current operational needs without losing the architectural path required for future reasoning re-entry, method upgrades, and refresh tracking.

The schema is organized into three tiers.

| Tier   | Name                                   | Purpose                                                                            |
| ------ | -------------------------------------- | ---------------------------------------------------------------------------------- |
| Tier 1 | Core Surface Exposure                  | Required for primary geometry-derived surface exposure                             |
| Tier 2 | Reasoning-Informed Surface Support     | Required when downstream reasoning assertions re-enter VDB                         |
| Tier 3 | Reasoning Currency and Refresh Support | Required when surfaces track stale reasoning, refresh triggers, or method upgrades |

Tier 1 is required for all Evidence Convergence Surfaces.

Tier 2 is required only for reasoning-informed surfaces.

Tier 3 is required only when reasoning currency, refresh state, or outbound refresh packages are represented.

---

# Object Overview

```text
EvidenceConvergenceSurfaceBuild
        ↓
EvidenceConvergenceSurface
        ↓
        ├── SurfaceRegionReference[]
        ├── SurfaceEligibility[]
        ├── SurfaceDisclosure[]
        ├── SurfaceEvidenceStratum[]
        ├── SurfaceLineageReference[]
        ├── ReasoningSurfaceContext?          # Tier 2
        ├── ReasoningCurrencyState?          # Tier 3
        ├── SurfaceRefreshTrigger[]?         # Tier 3
        └── SurfaceExportPackageReference[]? # Tier 3
```

The root object is `EvidenceConvergenceSurface`.

The build object records how surfaces were generated.

Region, eligibility, disclosure, strata, and lineage objects preserve the surface's structural and epistemic context.

Reasoning and refresh objects are conditional extensions.

---

# Tier 1: Core Surface Exposure

Tier 1 supports primary Evidence Convergence Surfaces derived from Convergence Geometry.

Tier 1 is required for all valid surfaces.

Tier 1 objects:

* `EvidenceConvergenceSurfaceBuild`
* `EvidenceConvergenceSurface`
* `SurfaceRegionReference`
* `SurfaceEligibility`
* `SurfaceDisclosure`
* `SurfaceEvidenceStratum`
* `SurfaceLineageReference`

---

# EvidenceConvergenceSurfaceBuild

## Purpose

`EvidenceConvergenceSurfaceBuild` records the construction context for a set of Evidence Convergence Surfaces.

It supports reproducibility by identifying the upstream geometry build, rule sets, disclosure policy, implementation version, and VDB evidence generation used to produce surfaces.

## Object Shape

```yaml
EvidenceConvergenceSurfaceBuild:
  surface_build_id: string
  input_geometry_build_id: string
  input_topology_build_id: string
  input_assertion_corpus_id: string
  vdb_generation_id: string
  surface_builder_name: string
  surface_builder_version: string
  surface_rule_set_id: string
  surface_rule_set_version: string
  disclosure_policy_id: string
  disclosure_policy_version: string
  build_scope: string
  build_parameters: object
  built_at: datetime
```

## Field Requirements

| Field                       | Required    | Description                                                                                    |
| --------------------------- | ----------- | ---------------------------------------------------------------------------------------------- |
| `surface_build_id`          | Yes         | Stable identifier for this surface build                                                       |
| `input_geometry_build_id`   | Yes         | Convergence Geometry build used as direct input                                                |
| `input_topology_build_id`   | Yes         | Upstream topology build represented by the geometry                                            |
| `input_assertion_corpus_id` | Yes         | Assertion corpus used by the upstream topology and geometry                                    |
| `vdb_generation_id`         | Yes         | VDB evidence generation at surface construction time                                           |
| `surface_builder_name`      | Yes         | Name of the surface construction implementation                                                |
| `surface_builder_version`   | Yes         | Version of the surface construction implementation                                             |
| `surface_rule_set_id`       | Yes         | Identifier for eligibility and construction rules                                              |
| `surface_rule_set_version`  | Yes         | Version of the surface rule set                                                                |
| `disclosure_policy_id`      | Yes         | Identifier for disclosure policy                                                               |
| `disclosure_policy_version` | Yes         | Version of disclosure policy                                                                   |
| `build_scope`               | Yes         | Scope of the build, such as corpus-wide, phenotype-scoped, participant-scoped, or audit-scoped |
| `build_parameters`          | Recommended | Parameter object sufficient to reconstruct the build                                           |
| `built_at`                  | Yes         | Time or version marker for the build                                                           |

## Invariant

A surface build must identify the exact geometry build and rule context used to generate its surfaces.

---

# EvidenceConvergenceSurface

## Purpose

`EvidenceConvergenceSurface` is the core surface object.

It represents a governed, queryable exposure object over one or more Convergence Regions.

## Object Shape

```yaml
EvidenceConvergenceSurface:
  surface_id: string
  surface_build_id: string
  surface_generation_id: string
  vdb_generation_id: string
  surface_kind: string
  surface_label: string
  surface_description: string
  surface_status: string
  surface_eligibility_summary: string
  surface_disclosure_summary: string
  source_convergence_region_ids: array[string]
  surface_evidence_strata_ids: array[string]
  created_at: datetime
```

## Field Requirements

| Field                           | Required    | Description                                                   |
| ------------------------------- | ----------- | ------------------------------------------------------------- |
| `surface_id`                    | Yes         | Stable identifier for the surface                             |
| `surface_build_id`              | Yes         | Build that produced the surface                               |
| `surface_generation_id`         | Yes         | Surface generation identifier                                 |
| `vdb_generation_id`             | Yes         | VDB evidence generation from which the surface was produced   |
| `surface_kind`                  | Yes         | Conceptual class of surface                                   |
| `surface_label`                 | Recommended | Human-readable surface label                                  |
| `surface_description`           | Optional    | Non-interpretive description of the surface                   |
| `surface_status`                | Yes         | Lifecycle state of the surface                                |
| `surface_eligibility_summary`   | Yes         | Short summary of why the surface is eligible                  |
| `surface_disclosure_summary`    | Yes         | Short summary of why disclosed content is exposed             |
| `source_convergence_region_ids` | Yes         | One or more source Convergence Regions exposed by the surface |
| `surface_evidence_strata_ids`   | Yes         | Evidence strata represented in the surface                    |
| `created_at`                    | Yes         | Surface creation timestamp or version marker                  |

## Controlled Vocabulary: `surface_kind`

Recommended values:

* `primary_convergence_surface`
* `mixed_modality_surface`
* `reasoning_informed_surface`
* `reentry_surface`
* `audit_surface`
* `refresh_candidate_surface`

## Controlled Vocabulary: `surface_status`

Recommended values:

* `active`
* `historical`
* `superseded`
* `audit_only`
* `refresh_candidate`
* `retired`

## Invariants

An Evidence Convergence Surface must:

* reference at least one source Convergence Region
* belong to a surface build
* belong to a VDB generation
* declare eligibility summary
* declare disclosure summary
* declare evidence strata
* avoid biological or statistical interpretation

---

# SurfaceRegionReference

## Purpose

`SurfaceRegionReference` links a surface to the Convergence Geometry it exposes.

It preserves the rule that surfaces are geometry-derived.

## Object Shape

```yaml
SurfaceRegionReference:
  surface_region_reference_id: string
  surface_id: string
  convergence_region_id: string
  geometry_build_id: string
  region_role: string
  region_bounding_basis: string
  included_geometry_feature_ids: array[string]
  included_structural_motif_ids: array[string]
  included_convergence_profile_ids: array[string]
```

## Field Requirements

| Field                              | Required    | Description                                        |
| ---------------------------------- | ----------- | -------------------------------------------------- |
| `surface_region_reference_id`      | Yes         | Stable identifier for this region reference        |
| `surface_id`                       | Yes         | Surface containing the region                      |
| `convergence_region_id`            | Yes         | Source Convergence Region                          |
| `geometry_build_id`                | Yes         | Geometry build containing the region               |
| `region_role`                      | Yes         | Role of the region within the surface              |
| `region_bounding_basis`            | Yes         | Bounding basis inherited from Convergence Geometry |
| `included_geometry_feature_ids`    | Recommended | Geometry Features exposed through the surface      |
| `included_structural_motif_ids`    | Optional    | Structural Motifs exposed through the surface      |
| `included_convergence_profile_ids` | Optional    | Convergence Profiles exposed through the surface   |

## Controlled Vocabulary: `region_role`

Recommended values:

* `primary_region`
* `supporting_region`
* `comparison_region`
* `audit_region`
* `refresh_region`

## Invariant

Every surface must have at least one `SurfaceRegionReference`.

A surface without a source Convergence Region is invalid.

---

# SurfaceEligibility

## Purpose

`SurfaceEligibility` records why a Convergence Region may become an exposed surface.

Eligibility is structural.

Eligibility is not biological importance.

## Object Shape

```yaml
SurfaceEligibility:
  surface_eligibility_id: string
  surface_id: string
  eligibility_basis: string
  eligibility_rule_id: string
  eligibility_rule_version: string
  eligibility_scope: string
  eligibility_source_geometry_ids: array[string]
  eligibility_source_feature_ids: array[string]
  eligibility_explanation: string
```

## Field Requirements

| Field                             | Required    | Description                                     |
| --------------------------------- | ----------- | ----------------------------------------------- |
| `surface_eligibility_id`          | Yes         | Stable identifier for this eligibility record   |
| `surface_id`                      | Yes         | Surface to which eligibility applies            |
| `eligibility_basis`               | Yes         | Structural reason the surface may exist         |
| `eligibility_rule_id`             | Yes         | Rule that determined eligibility                |
| `eligibility_rule_version`        | Yes         | Version of eligibility rule                     |
| `eligibility_scope`               | Yes         | Scope over which eligibility was evaluated      |
| `eligibility_source_geometry_ids` | Yes         | Geometry objects used to determine eligibility  |
| `eligibility_source_feature_ids`  | Recommended | Geometry Features used to determine eligibility |
| `eligibility_explanation`         | Recommended | Non-interpretive explanation of eligibility     |

## Controlled Vocabulary: `eligibility_basis`

Recommended values:

* `cross_producer_geometry`
* `multi_modal_geometry`
* `independent_evidence_geometry`
* `epistemic_diversity_geometry`
* `temporal_persistence_geometry`
* `multi_component_geometry`
* `reasoning_reentry_geometry`
* `audit_requested_geometry`
* `refresh_required_geometry`

## Forbidden Eligibility Values

The following concepts must not be used as eligibility bases:

* `important`
* `interesting`
* `significant`
* `promising`
* `causal`
* `pathogenic`
* `actionable`
* `clinically_relevant`
* `biologically_meaningful`

## Invariant

Every surface must have at least one `SurfaceEligibility` record.

---

# SurfaceDisclosure

## Purpose

`SurfaceDisclosure` records why specific information is exposed through a surface.

Disclosure is distinct from eligibility.

Eligibility answers why the surface may exist.

Disclosure answers why the surface contains what it contains.

## Object Shape

```yaml
SurfaceDisclosure:
  surface_disclosure_id: string
  surface_id: string
  disclosure_basis: string
  disclosure_policy_id: string
  disclosure_policy_version: string
  consumer_class: string
  consumer_name: string
  disclosed_element_kind: string
  disclosed_element_scope: string
  lineage_depth: string
  redaction_state: string
```

## Field Requirements

| Field                       | Required    | Description                                                  |
| --------------------------- | ----------- | ------------------------------------------------------------ |
| `surface_disclosure_id`     | Yes         | Stable identifier for this disclosure record                 |
| `surface_id`                | Yes         | Surface to which disclosure applies                          |
| `disclosure_basis`          | Yes         | Reason this information is exposed                           |
| `disclosure_policy_id`      | Yes         | Disclosure policy used                                       |
| `disclosure_policy_version` | Yes         | Version of disclosure policy                                 |
| `consumer_class`            | Recommended | Intended class of consumer                                   |
| `consumer_name`             | Optional    | Specific consumer name, such as RDGP                         |
| `disclosed_element_kind`    | Yes         | Kind of element disclosed                                    |
| `disclosed_element_scope`   | Yes         | Scope of disclosed content                                   |
| `lineage_depth`             | Yes         | Depth of lineage exposed                                     |
| `redaction_state`           | Yes         | Whether content is full, summarized, redacted, or referenced |

## Controlled Vocabulary: `disclosure_basis`

Recommended values:

* `minimum_reasoning_context`
* `assertion_lineage_required`
* `topology_lineage_required`
* `geometry_feature_required`
* `provenance_audit_required`
* `epistemic_status_required`
* `independence_context_required`
* `temporal_context_required`
* `reasoning_currency_required`
* `refresh_context_required`
* `consumer_contract_required`

## Controlled Vocabulary: `consumer_class`

Recommended values:

* `downstream_reasoning_engine`
* `human_audit`
* `visualization_layer`
* `validation_workflow`
* `operator_review`
* `future_consumer`

## Controlled Vocabulary: `lineage_depth`

Recommended values:

* `surface_only`
* `geometry_region`
* `topology_relationship`
* `assertion_record`
* `producer_tep`
* `producer_artifact`

## Controlled Vocabulary: `redaction_state`

Recommended values:

* `full`
* `summary`
* `reference_only`
* `redacted`
* `not_applicable`

## Invariant

Every surface must have at least one `SurfaceDisclosure` record.

A surface must not expose arbitrary VDB internal state without disclosure basis.

---

# SurfaceEvidenceStratum

## Purpose

`SurfaceEvidenceStratum` records the evidence classes represented in a surface.

This prevents raw observations, semantic priors, and reasoning outputs from being collapsed into a single undifferentiated support class.

## Object Shape

```yaml
SurfaceEvidenceStratum:
  surface_evidence_stratum_id: string
  surface_id: string
  stratum_kind: string
  producer_family: string
  producer_id: string
  modality: string
  epistemic_status: string
  derivation_class: string
  source_assertion_ids: array[string]
  source_assertion_count: integer
  source_participant_scope: array[string]
  source_context_scope: array[string]
```

## Field Requirements

| Field                         | Required    | Description                                                                             |
| ----------------------------- | ----------- | --------------------------------------------------------------------------------------- |
| `surface_evidence_stratum_id` | Yes         | Stable identifier for this stratum                                                      |
| `surface_id`                  | Yes         | Surface containing this stratum                                                         |
| `stratum_kind`                | Yes         | Evidence class represented by this stratum                                              |
| `producer_family`             | Yes         | Producer family, such as VAP, GSC, RSP, PTN, RDGP                                       |
| `producer_id`                 | Yes         | Specific producer identifier                                                            |
| `modality`                    | Yes         | Evidence modality                                                                       |
| `epistemic_status`            | Yes         | Epistemic status inherited from assertions or producer                                  |
| `derivation_class`            | Yes         | Whether evidence is raw, derived, semantic, reasoning-derived, validation-derived, etc. |
| `source_assertion_ids`        | Recommended | Assertion Records represented by this stratum                                           |
| `source_assertion_count`      | Yes         | Number of source assertions represented                                                 |
| `source_participant_scope`    | Recommended | Participants covered by the stratum                                                     |
| `source_context_scope`        | Recommended | Contexts covered by the stratum                                                         |

## Controlled Vocabulary: `stratum_kind`

Recommended values:

* `raw_variant_observation`
* `semantic_prior`
* `transcriptomic_observation`
* `proteomic_observation`
* `clinical_observation`
* `environmental_observation`
* `imaging_observation`
* `literature_derived_assertion`
* `reasoning_output`
* `validation_assertion`

## Controlled Vocabulary: `modality`

Recommended values:

* `variant`
* `gene_set`
* `transcriptomic`
* `proteomic`
* `clinical`
* `environmental`
* `imaging`
* `literature`
* `reasoning`
* `validation`
* `unknown`

## Controlled Vocabulary: `derivation_class`

Recommended values:

* `raw_producer_assertion`
* `semantic_prior_assertion`
* `derived_producer_assertion`
* `downstream_reasoning_assertion`
* `validation_assertion`
* `audit_assertion`

## Invariants

A surface must preserve evidence stratum identity.

A composite surface must contain at least two strata.

A reasoning-informed surface must contain at least one `reasoning_output` stratum.

Distinct evidence strata must not be homogenized.

---

# SurfaceLineageReference

## Purpose

`SurfaceLineageReference` provides a generic reconstruction path from a surface back to source geometry, topology, assertions, and producer artifacts.

## Object Shape

```yaml
SurfaceLineageReference:
  surface_lineage_reference_id: string
  surface_id: string
  lineage_kind: string
  lineage_role: string
  source_id: string
  source_type: string
  source_namespace: string
  source_build_id: string
  source_producer_id: string
```

## Field Requirements

| Field                          | Required    | Description                                     |
| ------------------------------ | ----------- | ----------------------------------------------- |
| `surface_lineage_reference_id` | Yes         | Stable identifier for lineage reference         |
| `surface_id`                   | Yes         | Surface to which lineage applies                |
| `lineage_kind`                 | Yes         | Kind of upstream lineage                        |
| `lineage_role`                 | Yes         | Role of the source object in the surface        |
| `source_id`                    | Yes         | Identifier of the source object                 |
| `source_type`                  | Yes         | Type of source object                           |
| `source_namespace`             | Recommended | Namespace in which the source object is defined |
| `source_build_id`              | Optional    | Build identifier associated with the source     |
| `source_producer_id`           | Optional    | Producer associated with the source             |

## Controlled Vocabulary: `lineage_kind`

Recommended values:

* `geometry_build`
* `convergence_region`
* `geometry_feature`
* `structural_motif`
* `convergence_profile`
* `topology_relationship`
* `assertion_record`
* `producer_tep`
* `producer_artifact`

## Controlled Vocabulary: `lineage_role`

Recommended values:

* `source`
* `supporting`
* `exposed`
* `audit`
* `refresh_basis`
* `reasoning_input`
* `reasoning_output`

## Invariant

A surface must preserve lineage to:

* Convergence Geometry
* Evidence Topology
* Assertion Records

Producer TEP or producer artifact lineage is strongly recommended where available.

---

# Tier 2: Reasoning-Informed Surface Support

Tier 2 is required when downstream reasoning outputs re-enter VDB and participate in future surface exposure.

Tier 2 objects:

* `ReasoningSurfaceContext`
* `ReasoningAssertionReference`

---

# ReasoningSurfaceContext

## Purpose

`ReasoningSurfaceContext` records the downstream reasoning context associated with a reasoning-informed surface.

It preserves the fact that reasoning outputs were generated outside VDB and later re-entered as assertions.

## Object Shape

```yaml
ReasoningSurfaceContext:
  reasoning_surface_context_id: string
  surface_id: string
  reasoning_producer_id: string
  reasoning_producer_name: string
  reasoning_producer_version: string
  reasoning_method_id: string
  reasoning_method_name: string
  reasoning_method_version: string
  reasoning_run_id: string
  reasoning_input_surface_id: string
  reasoning_input_surface_generation_id: string
  reasoning_input_assertion_corpus_id: string
  reasoning_input_vdb_generation_id: string
  reasoning_output_tep_id: string
  reasoning_output_ingestion_id: string
```

## Field Requirements

| Field                                   | Required    | Description                                        |
| --------------------------------------- | ----------- | -------------------------------------------------- |
| `reasoning_surface_context_id`          | Yes         | Stable identifier for reasoning context            |
| `surface_id`                            | Yes         | Reasoning-informed surface                         |
| `reasoning_producer_id`                 | Yes         | Producer identity of reasoning system              |
| `reasoning_producer_name`               | Recommended | Human-readable producer name                       |
| `reasoning_producer_version`            | Recommended | Producer version                                   |
| `reasoning_method_id`                   | Yes         | Reasoning method identifier                        |
| `reasoning_method_name`                 | Recommended | Human-readable method name                         |
| `reasoning_method_version`              | Yes         | Reasoning method version                           |
| `reasoning_run_id`                      | Yes         | Downstream reasoning run identifier                |
| `reasoning_input_surface_id`            | Yes         | Surface consumed by reasoning system               |
| `reasoning_input_surface_generation_id` | Yes         | Generation of consumed input surface               |
| `reasoning_input_assertion_corpus_id`   | Yes         | Assertion corpus used by reasoning system          |
| `reasoning_input_vdb_generation_id`     | Yes         | VDB generation used by reasoning system            |
| `reasoning_output_tep_id`               | Recommended | TEP identifier for returned reasoning product      |
| `reasoning_output_ingestion_id`         | Recommended | VDB ingestion event for returned reasoning product |

## Invariants

A reasoning-informed surface must include `ReasoningSurfaceContext`.

Reasoning context must identify both the reasoning method and the input surface/corpus used by the reasoning system.

---

# ReasoningAssertionReference

## Purpose

`ReasoningAssertionReference` links a reasoning-informed surface to preserved downstream reasoning assertions.

## Object Shape

```yaml
ReasoningAssertionReference:
  reasoning_assertion_reference_id: string
  surface_id: string
  reasoning_surface_context_id: string
  assertion_id: string
  assertion_role: string
  confidence_or_support_reference: string
  epistemic_status: string
  provenance_reference: string
```

## Field Requirements

| Field                              | Required    | Description                                                |
| ---------------------------------- | ----------- | ---------------------------------------------------------- |
| `reasoning_assertion_reference_id` | Yes         | Stable identifier for reasoning assertion reference        |
| `surface_id`                       | Yes         | Reasoning-informed surface                                 |
| `reasoning_surface_context_id`     | Yes         | Reasoning context associated with the assertion            |
| `assertion_id`                     | Yes         | Preserved Assertion Record emitted by downstream reasoning |
| `assertion_role`                   | Yes         | Role of assertion in the surface                           |
| `confidence_or_support_reference`  | Optional    | Reference to confidence/support metadata if present        |
| `epistemic_status`                 | Yes         | Epistemic status of reasoning assertion                    |
| `provenance_reference`             | Recommended | Provenance reference for reasoning assertion               |

## Controlled Vocabulary: `assertion_role`

Recommended values:

* `primary_reasoning_output`
* `supporting_reasoning_output`
* `confidence_assertion`
* `prioritization_assertion`
* `negative_or_null_assertion`
* `method_metadata_assertion`
* `validation_assertion`

## Invariant

Reasoning outputs must be represented as preserved assertions, not as VDB conclusions.

---

# Tier 3: Reasoning Currency and Refresh Support

Tier 3 supports future-proofing.

It is required when VDB tracks whether reasoning-informed surfaces are current relative to evidence corpus state and reasoning method state.

Tier 3 objects:

* `ReasoningCurrencyState`
* `SurfaceRefreshTrigger`
* `SurfaceExportPackageReference`

---

# ReasoningCurrencyState

## Purpose

`ReasoningCurrencyState` records whether the reasoning associated with a surface is current relative to the relevant evidence corpus and declared reasoning method.

Currency is metadata-derived.

It is not meaning-derived.

## Object Shape

```yaml
ReasoningCurrencyState:
  reasoning_currency_state_id: string
  surface_id: string
  currency_state: string
  reasoning_producer_id: string
  reasoning_method_id: string
  reasoning_method_version: string
  current_declared_reasoning_method_version: string
  reasoning_input_assertion_corpus_id: string
  current_relevant_assertion_corpus_id: string
  reasoning_input_vdb_generation_id: string
  current_vdb_generation_id: string
  relevance_basis: string
  currency_basis: string
  currency_evaluated_at: datetime
```

## Field Requirements

| Field                                       | Required    | Description                                            |
| ------------------------------------------- | ----------- | ------------------------------------------------------ |
| `reasoning_currency_state_id`               | Yes         | Stable identifier for currency state record            |
| `surface_id`                                | Yes         | Surface whose currency is represented                  |
| `currency_state`                            | Yes         | Current reasoning currency state                       |
| `reasoning_producer_id`                     | Conditional | Required for reasoning-informed surfaces               |
| `reasoning_method_id`                       | Conditional | Required for reasoning-informed surfaces               |
| `reasoning_method_version`                  | Conditional | Method version used by existing reasoning              |
| `current_declared_reasoning_method_version` | Conditional | Current declared method version for this surface class |
| `reasoning_input_assertion_corpus_id`       | Conditional | Corpus used by reasoning system                        |
| `current_relevant_assertion_corpus_id`      | Conditional | Current relevant corpus for this surface               |
| `reasoning_input_vdb_generation_id`         | Conditional | VDB generation used by reasoning system                |
| `current_vdb_generation_id`                 | Yes         | Current VDB generation when currency was evaluated     |
| `relevance_basis`                           | Conditional | Basis for deciding which corpus is relevant            |
| `currency_basis`                            | Yes         | Metadata comparison used to determine currency         |
| `currency_evaluated_at`                     | Yes         | Timestamp or version marker for currency evaluation    |

## Controlled Vocabulary: `currency_state`

Recommended values:

* `raw_only`
* `reasoning_current`
* `reasoning_stale_due_to_new_evidence`
* `reasoning_stale_due_to_method_update`
* `reasoning_stale_due_to_both`
* `refresh_candidate`
* `refresh_completed`
* `not_evaluated`

## Controlled Vocabulary: `relevance_basis`

Recommended values:

* `shared_participant`
* `shared_context`
* `shared_phenotype`
* `shared_region`
* `shared_surface_anchor`
* `consumer_contract_scope`
* `operator_declared_scope`
* `not_applicable`

## Controlled Vocabulary: `currency_basis`

Recommended values:

* `raw_surface_no_reasoning`
* `corpus_generation_match`
* `corpus_generation_mismatch`
* `reasoning_method_match`
* `reasoning_method_mismatch`
* `corpus_and_method_match`
* `corpus_and_method_mismatch`
* `operator_declared`
* `not_evaluated`

## Invariants

Reasoning currency must be determined from metadata.

A surface must not present stale reasoning as current.

A raw-only surface may use `currency_state: raw_only`.

---

# SurfaceRefreshTrigger

## Purpose

`SurfaceRefreshTrigger` records why refresh is warranted for a surface.

A surface may have multiple refresh triggers.

## Object Shape

```yaml
SurfaceRefreshTrigger:
  refresh_trigger_id: string
  surface_id: string
  trigger_kind: string
  trigger_detected_at: datetime
  trigger_source: string
  previous_value: string
  current_value: string
  affected_scope: string
  recommended_action: string
  operator_visibility: string
```

## Field Requirements

| Field                 | Required    | Description                                             |
| --------------------- | ----------- | ------------------------------------------------------- |
| `refresh_trigger_id`  | Yes         | Stable identifier for refresh trigger                   |
| `surface_id`          | Yes         | Surface affected by trigger                             |
| `trigger_kind`        | Yes         | Reason refresh is warranted                             |
| `trigger_detected_at` | Yes         | Time or version marker of detection                     |
| `trigger_source`      | Yes         | Source of trigger                                       |
| `previous_value`      | Recommended | Prior metadata value                                    |
| `current_value`       | Recommended | Current metadata value                                  |
| `affected_scope`      | Yes         | Scope affected by trigger                               |
| `recommended_action`  | Recommended | Non-interpretive recommended action                     |
| `operator_visibility` | Yes         | Whether and how the trigger should be shown to operator |

## Controlled Vocabulary: `trigger_kind`

Recommended values:

* `new_relevant_raw_evidence`
* `reasoning_method_update`
* `reasoning_producer_version_update`
* `disclosure_contract_update`
* `eligibility_rule_update`
* `operator_requested_audit`
* `evidence_and_method_update`

## Controlled Vocabulary: `trigger_source`

Recommended values:

* `producer_tep_ingestion`
* `reasoning_method_registry`
* `surface_currency_check`
* `operator_action`
* `policy_update`
* `validation_check`

## Controlled Vocabulary: `recommended_action`

Recommended values:

* `emit_refresh_package`
* `operator_review`
* `no_action`
* `audit_lineage`
* `update_disclosure_contract`
* `update_eligibility_rules`

## Controlled Vocabulary: `operator_visibility`

Recommended values:

* `visible`
* `hidden`
* `audit_only`
* `warning`
* `error`

## Invariant

Refresh triggers must be metadata-derived, not meaning-derived.

---

# SurfaceExportPackageReference

## Purpose

`SurfaceExportPackageReference` records outbound packages emitted from surfaces for downstream reasoning systems.

The surface is the persistent exposure object.

The export package is a transport artifact.

## Object Shape

```yaml
SurfaceExportPackageReference:
  export_package_reference_id: string
  export_package_id: string
  surface_id: string
  surface_generation_id: string
  consumer_contract_id: string
  consumer_class: string
  consumer_name: string
  export_reason: string
  refresh_trigger_ids: array[string]
  exported_at: datetime
  export_status: string
  export_artifact_uri: string
```

## Field Requirements

| Field                         | Required    | Description                                    |
| ----------------------------- | ----------- | ---------------------------------------------- |
| `export_package_reference_id` | Yes         | Stable identifier for export package reference |
| `export_package_id`           | Yes         | Identifier for outbound package                |
| `surface_id`                  | Yes         | Surface exported                               |
| `surface_generation_id`       | Yes         | Surface generation exported                    |
| `consumer_contract_id`        | Recommended | Disclosure/consumer contract used for export   |
| `consumer_class`              | Yes         | Class of consumer                              |
| `consumer_name`               | Recommended | Specific consumer name                         |
| `export_reason`               | Yes         | Reason package was emitted                     |
| `refresh_trigger_ids`         | Conditional | Required for refresh exports                   |
| `exported_at`                 | Yes         | Export timestamp or version marker             |
| `export_status`               | Yes         | Export lifecycle status                        |
| `export_artifact_uri`         | Optional    | URI or path to outbound artifact               |

## Controlled Vocabulary: `export_reason`

Recommended values:

* `initial_reasoning_package`
* `refresh_due_to_new_evidence`
* `refresh_due_to_method_update`
* `refresh_due_to_both`
* `audit_export`
* `operator_requested_export`
* `validation_export`

## Controlled Vocabulary: `export_status`

Recommended values:

* `planned`
* `emitted`
* `consumed`
* `superseded`
* `failed`
* `archived`

## Invariant

Outbound packages must preserve surface identity and generation.

A TEP-VDB package must not be treated as equivalent to the persistent Evidence Convergence Surface.

---

# Controlled Vocabulary Summary

## Surface Kinds

* `primary_convergence_surface`
* `mixed_modality_surface`
* `reasoning_informed_surface`
* `reentry_surface`
* `audit_surface`
* `refresh_candidate_surface`

## Surface Status

* `active`
* `historical`
* `superseded`
* `audit_only`
* `refresh_candidate`
* `retired`

## Eligibility Basis

* `cross_producer_geometry`
* `multi_modal_geometry`
* `independent_evidence_geometry`
* `epistemic_diversity_geometry`
* `temporal_persistence_geometry`
* `multi_component_geometry`
* `reasoning_reentry_geometry`
* `audit_requested_geometry`
* `refresh_required_geometry`

## Disclosure Basis

* `minimum_reasoning_context`
* `assertion_lineage_required`
* `topology_lineage_required`
* `geometry_feature_required`
* `provenance_audit_required`
* `epistemic_status_required`
* `independence_context_required`
* `temporal_context_required`
* `reasoning_currency_required`
* `refresh_context_required`
* `consumer_contract_required`

## Stratum Kinds

* `raw_variant_observation`
* `semantic_prior`
* `transcriptomic_observation`
* `proteomic_observation`
* `clinical_observation`
* `environmental_observation`
* `imaging_observation`
* `literature_derived_assertion`
* `reasoning_output`
* `validation_assertion`

## Currency States

* `raw_only`
* `reasoning_current`
* `reasoning_stale_due_to_new_evidence`
* `reasoning_stale_due_to_method_update`
* `reasoning_stale_due_to_both`
* `refresh_candidate`
* `refresh_completed`
* `not_evaluated`

## Refresh Trigger Kinds

* `new_relevant_raw_evidence`
* `reasoning_method_update`
* `reasoning_producer_version_update`
* `disclosure_contract_update`
* `eligibility_rule_update`
* `operator_requested_audit`
* `evidence_and_method_update`

---

# Example 1: Primary Raw Surface

This example represents a primary surface exposing convergence between VAP and GSC assertions.

```yaml
EvidenceConvergenceSurface:
  surface_id: "surface_POLG_primary_0001"
  surface_build_id: "surface_build_2026_06_26_001"
  surface_generation_id: "surface_generation_001"
  vdb_generation_id: "vdb_generation_001"
  surface_kind: "primary_convergence_surface"
  surface_label: "POLG primary convergence surface"
  surface_description: "Geometry-derived exposure over POLG-associated VAP and GSC assertion convergence."
  surface_status: "active"
  surface_eligibility_summary: "cross_producer_geometry"
  surface_disclosure_summary: "minimum_reasoning_context"
  source_convergence_region_ids:
    - "convergence_region_POLG_0001"
  surface_evidence_strata_ids:
    - "stratum_POLG_vap_variant_0001"
    - "stratum_POLG_gsc_prior_0001"
  created_at: "2026-06-26T00:00:00Z"

SurfaceEvidenceStratum:
  - surface_evidence_stratum_id: "stratum_POLG_vap_variant_0001"
    surface_id: "surface_POLG_primary_0001"
    stratum_kind: "raw_variant_observation"
    producer_family: "VAP"
    producer_id: "VAP"
    modality: "variant"
    epistemic_status: "observed"
    derivation_class: "raw_producer_assertion"
    source_assertion_ids:
      - "assertion_vap_000317"
    source_assertion_count: 1

  - surface_evidence_stratum_id: "stratum_POLG_gsc_prior_0001"
    surface_id: "surface_POLG_primary_0001"
    stratum_kind: "semantic_prior"
    producer_family: "GSC"
    producer_id: "GSC"
    modality: "gene_set"
    epistemic_status: "semantic_prior"
    derivation_class: "semantic_prior_assertion"
    source_assertion_ids:
      - "assertion_gsc_000041"
    source_assertion_count: 1

ReasoningCurrencyState:
  reasoning_currency_state_id: "currency_POLG_primary_0001"
  surface_id: "surface_POLG_primary_0001"
  currency_state: "raw_only"
  current_vdb_generation_id: "vdb_generation_001"
  relevance_basis: "not_applicable"
  currency_basis: "raw_surface_no_reasoning"
  currency_evaluated_at: "2026-06-26T00:00:00Z"
```

This surface exposes reasoning capacity but does not contain downstream reasoning output.

---

# Example 2: Reasoning-Informed Surface

This example represents a surface after RDGP consumes the primary surface and returns TEP-RDGP assertions.

```yaml
EvidenceConvergenceSurface:
  surface_id: "surface_POLG_rdgp_informed_0001"
  surface_build_id: "surface_build_2026_06_27_001"
  surface_generation_id: "surface_generation_002"
  vdb_generation_id: "vdb_generation_002"
  surface_kind: "reasoning_informed_surface"
  surface_label: "POLG RDGP-informed convergence surface"
  surface_description: "Geometry-derived exposure including preserved RDGP reasoning assertions over prior POLG convergence surface."
  surface_status: "active"
  surface_eligibility_summary: "reasoning_reentry_geometry"
  surface_disclosure_summary: "minimum_reasoning_context"
  source_convergence_region_ids:
    - "convergence_region_POLG_0002"
  surface_evidence_strata_ids:
    - "stratum_POLG_vap_variant_0001"
    - "stratum_POLG_gsc_prior_0001"
    - "stratum_POLG_rdgp_reasoning_0001"
  created_at: "2026-06-27T00:00:00Z"

ReasoningSurfaceContext:
  reasoning_surface_context_id: "reasoning_context_POLG_rdgp_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  reasoning_producer_id: "RDGP"
  reasoning_producer_name: "Rare Disease Gene Prioritization"
  reasoning_producer_version: "v1"
  reasoning_method_id: "rdgp_prioritization_model"
  reasoning_method_name: "RDGP prioritization model"
  reasoning_method_version: "v1"
  reasoning_run_id: "rdgp_run_0001"
  reasoning_input_surface_id: "surface_POLG_primary_0001"
  reasoning_input_surface_generation_id: "surface_generation_001"
  reasoning_input_assertion_corpus_id: "assertion_corpus_001"
  reasoning_input_vdb_generation_id: "vdb_generation_001"
  reasoning_output_tep_id: "tep_rdgp_0001"
  reasoning_output_ingestion_id: "vdb_ingestion_rdgp_0001"

SurfaceEvidenceStratum:
  surface_evidence_stratum_id: "stratum_POLG_rdgp_reasoning_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  stratum_kind: "reasoning_output"
  producer_family: "RDGP"
  producer_id: "RDGP"
  modality: "reasoning"
  epistemic_status: "statistically_derived"
  derivation_class: "downstream_reasoning_assertion"
  source_assertion_ids:
    - "assertion_rdgp_000091"
  source_assertion_count: 1

ReasoningCurrencyState:
  reasoning_currency_state_id: "currency_POLG_rdgp_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  currency_state: "reasoning_current"
  reasoning_producer_id: "RDGP"
  reasoning_method_id: "rdgp_prioritization_model"
  reasoning_method_version: "v1"
  current_declared_reasoning_method_version: "v1"
  reasoning_input_assertion_corpus_id: "assertion_corpus_001"
  current_relevant_assertion_corpus_id: "assertion_corpus_001"
  reasoning_input_vdb_generation_id: "vdb_generation_001"
  current_vdb_generation_id: "vdb_generation_002"
  relevance_basis: "shared_participant"
  currency_basis: "corpus_and_method_match"
  currency_evaluated_at: "2026-06-27T00:00:00Z"
```

This surface exposes preserved RDGP reasoning assertions.

It does not convert those assertions into VDB conclusions.

---

# Example 3: New Producer Refresh

This example represents a future case where a proteomics producer TEP enters VDB after RDGP reasoning.

The prior RDGP-informed surface remains historically valid, but reasoning currency becomes stale because RDGP did not reason over the new PTN assertions.

```yaml
ReasoningCurrencyState:
  reasoning_currency_state_id: "currency_POLG_rdgp_0002"
  surface_id: "surface_POLG_rdgp_informed_0001"
  currency_state: "reasoning_stale_due_to_new_evidence"
  reasoning_producer_id: "RDGP"
  reasoning_method_id: "rdgp_prioritization_model"
  reasoning_method_version: "v1"
  current_declared_reasoning_method_version: "v1"
  reasoning_input_assertion_corpus_id: "assertion_corpus_001"
  current_relevant_assertion_corpus_id: "assertion_corpus_002"
  reasoning_input_vdb_generation_id: "vdb_generation_001"
  current_vdb_generation_id: "vdb_generation_003"
  relevance_basis: "shared_participant"
  currency_basis: "corpus_generation_mismatch"
  currency_evaluated_at: "2026-07-01T00:00:00Z"

SurfaceRefreshTrigger:
  refresh_trigger_id: "refresh_POLG_ptn_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  trigger_kind: "new_relevant_raw_evidence"
  trigger_detected_at: "2026-07-01T00:00:00Z"
  trigger_source: "producer_tep_ingestion"
  previous_value: "assertion_corpus_001"
  current_value: "assertion_corpus_002"
  affected_scope: "POLG shared participant surface"
  recommended_action: "emit_refresh_package"
  operator_visibility: "warning"
```

This does not mean the PTN evidence changed RDGP's conclusion.

It means RDGP has not yet reasoned over the updated relevant raw evidence corpus.

---

# Example 4: Reasoning Method Refresh

This example represents a future case where RDGP changes its declared reasoning method version.

```yaml
ReasoningCurrencyState:
  reasoning_currency_state_id: "currency_POLG_rdgp_0003"
  surface_id: "surface_POLG_rdgp_informed_0001"
  currency_state: "reasoning_stale_due_to_method_update"
  reasoning_producer_id: "RDGP"
  reasoning_method_id: "rdgp_prioritization_model"
  reasoning_method_version: "v1"
  current_declared_reasoning_method_version: "v2"
  reasoning_input_assertion_corpus_id: "assertion_corpus_001"
  current_relevant_assertion_corpus_id: "assertion_corpus_001"
  reasoning_input_vdb_generation_id: "vdb_generation_001"
  current_vdb_generation_id: "vdb_generation_002"
  relevance_basis: "shared_participant"
  currency_basis: "reasoning_method_mismatch"
  currency_evaluated_at: "2027-01-01T00:00:00Z"

SurfaceRefreshTrigger:
  refresh_trigger_id: "refresh_POLG_method_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  trigger_kind: "reasoning_method_update"
  trigger_detected_at: "2027-01-01T00:00:00Z"
  trigger_source: "reasoning_method_registry"
  previous_value: "rdgp_prioritization_model:v1"
  current_value: "rdgp_prioritization_model:v2"
  affected_scope: "RDGP-informed POLG surface"
  recommended_action: "emit_refresh_package"
  operator_visibility: "warning"
```

This does not mean RDGP v2 is biologically superior.

It means the surface reasoning currency no longer matches the declared current reasoning method.

---

# Example 5: Refresh Export Package

This example represents VDB emitting a refreshed TEP-VDB package for downstream reasoning after a refresh trigger.

```yaml
SurfaceExportPackageReference:
  export_package_reference_id: "export_POLG_refresh_0001"
  export_package_id: "tep_vdb_POLG_refresh_0001"
  surface_id: "surface_POLG_rdgp_informed_0001"
  surface_generation_id: "surface_generation_002"
  consumer_contract_id: "consumer_contract_rdgp_v1"
  consumer_class: "downstream_reasoning_engine"
  consumer_name: "RDGP"
  export_reason: "refresh_due_to_new_evidence"
  refresh_trigger_ids:
    - "refresh_POLG_ptn_0001"
  exported_at: "2026-07-01T01:00:00Z"
  export_status: "emitted"
  export_artifact_uri: "results/teps/vdb/polg_refresh/tep_vdb_POLG_refresh_0001.json"
```

The export package is not the surface itself.

It is a transport artifact generated from a surface for downstream reasoning.

---

# Schema Maturity Requirements

## Tier 1 Required

All valid Evidence Convergence Surfaces must support Tier 1 fields and objects.

Tier 1 enables:

* primary surface exposure
* geometry lineage
* topology lineage
* assertion lineage
* eligibility basis
* disclosure basis
* evidence strata

## Tier 2 Conditional

Tier 2 is required for reasoning-informed surfaces.

Tier 2 enables:

* RDGP re-entry
* future reasoning-engine re-entry
* reasoning assertion references
* reasoning method provenance
* reasoning input lineage

## Tier 3 Conditional / Forward-Compatible

Tier 3 support is architecturally reserved but must not be treated as a prerequisite for the first operational Discovery Layer implementation.

Tier 3 is required when VDB tracks reasoning currency, refresh state, or outbound refresh packages.

Tier 3 enables:

* stale reasoning detection
* new evidence refresh detection
* reasoning method refresh detection
* operator warnings
* refresh package references
* future-proof reasoning currency audits

---

# Schema Invariants

A valid Evidence Convergence Surface schema must satisfy the following invariants.

## Surface Identity

Every surface must have stable identity, generation identity, and build identity.

## Geometry Dependency

Every surface must reference source Convergence Geometry.

## Eligibility

Every surface must declare why it is structurally eligible for exposure.

## Disclosure

Every surface must declare why its contents are disclosed.

## Traceability

Every surface must preserve lineage to geometry, topology, and Assertion Records.

## Evidence Strata

Every surface must preserve evidence stratum identity.

## Generation Awareness

Every surface must preserve the VDB generation from which it was produced.

## Reasoning Provenance

Every reasoning-informed surface must preserve reasoning producer, method, input surface, input corpus, and output assertion provenance.

## Reasoning Currency

Every reasoning-informed surface with currency tracking must distinguish current reasoning from stale reasoning.

## Refresh Safety

Refresh triggers must be metadata-derived, not meaning-derived.

## Non-Interpretation

No schema field may express biological meaning unless that meaning is itself a preserved Assertion Record.

---

# Invalid Structures

The following structures are invalid.

## Surface Without Geometry

```yaml
EvidenceConvergenceSurface:
  surface_id: "surface_invalid_001"
  source_convergence_region_ids: []
```

A surface without source Convergence Geometry violates the dependency chain.

## Surface Without Eligibility

```yaml
EvidenceConvergenceSurface:
  surface_id: "surface_invalid_002"
  surface_eligibility_summary: null
```

A surface must declare why it is eligible for exposure.

## Surface With Interpretive Eligibility

```yaml
SurfaceEligibility:
  eligibility_basis: "biologically_meaningful"
```

Surface eligibility must be structural, not interpretive.

## Surface Without Disclosure Basis

```yaml
SurfaceDisclosure:
  disclosure_basis: null
```

A surface must declare why information is exposed.

## Homogenized Composite Surface

```yaml
SurfaceEvidenceStratum:
  stratum_kind: "combined_support"
```

Distinct evidence types must not be collapsed into a single undifferentiated support class.

## Reasoning-Informed Surface Without Reasoning Context

```yaml
EvidenceConvergenceSurface:
  surface_kind: "reasoning_informed_surface"
  reasoning_context: null
```

A reasoning-informed surface must preserve downstream reasoning provenance.

## Stale Reasoning Presented as Current

```yaml
ReasoningCurrencyState:
  reasoning_input_assertion_corpus_id: "assertion_corpus_001"
  current_relevant_assertion_corpus_id: "assertion_corpus_002"
  currency_state: "reasoning_current"
```

A corpus mismatch must not be represented as current reasoning.

## Biological Conclusion Embedded in Surface

```yaml
EvidenceConvergenceSurface:
  surface_label: "POLG disease-causing surface"
```

Surface labels and descriptions must not encode biological conclusions unless they refer to preserved source assertions.

---

# Implementation Notes

This schema does not require a specific database representation.

Objects may be represented as:

* relational tables
* JSON documents
* YAML documents
* graph projections
* object records
* versioned files
* hybrid storage structures

Storage choices may vary.

Schema obligations do not.

Implementations should preserve object identity, linkage, traceability, and controlled vocabulary semantics regardless of backend.

---

# Summary

The Evidence Convergence Surface schema represents the Discovery Layer as a tiered object system.

Tier 1 supports core geometry-derived surface exposure.

Tier 2 supports reasoning-informed surfaces after downstream reasoning outputs re-enter VDB as preserved assertions.

Tier 3 supports reasoning currency, refresh triggers, and outbound refresh package references.

Together, these tiers allow VDB to expose deterministic reasoning capacity without becoming a reasoning engine.

The schema preserves the central boundary:

```text
VDB exposes surfaces.
Downstream systems reason.
Returned reasoning becomes new assertions.
Future surfaces expand.
```

Evidence Convergence Surfaces therefore remain governed, traceable, generation-aware, and non-interpretive discovery objects.

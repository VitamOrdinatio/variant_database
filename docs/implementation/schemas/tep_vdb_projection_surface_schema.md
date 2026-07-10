# TEP-VDB Projection Surface Schema

> Status: DEX-VDB implementation schema draft.
> This document defines the shared TEP-VDB projection-surface package shape.
> It is derived from the opportunity-space doctrine, the opportunity-space
> specification, the projection-policy registry specification, and the MPLC/CFBS
> scientific method-design documents. It is not a method-specific MPLC or CFBS
> implementation specification.

## 1. Purpose

This schema defines the shared container structure for VDB-emitted TEP-VDB
projection surfaces.

A TEP-VDB projection-surface package binds together:

```text
source corpus identity
shared evidence substrates
opportunity-space declarations
projection-policy registry references
method-specific projection surfaces
validation receipts
source traceability
anti-overclaim labels
```

The purpose of this schema is to let VDB emit one unified reason-ready transport
product that downstream RDGP can consume without re-ingesting producer TEPs or
reconstructing VAP/GSC integration independently.

## 2. Scope

This schema applies to VDB-emitted TEP-VDB projection-surface packages. It
defines the common package layout, required top-level containers, shared
substrate indices, method-surface containers, traceability rules, and
schema-level validation requirements.

This schema is intentionally method-neutral. MPLC and CFBS are represented here
as method-specific projection-surface rooms inside the same TEP-VDB package, but
the exact field contracts for those rooms are defined in later method-specific
specifications.

## 3. Non-Goals

This schema does not define MPLC matching logic.

This schema does not define CFBS scan-window logic.

This schema does not define opportunity-state semantics; those belong to:

```text
docs/implementation/specifications/opportunity_space_spec.md
```

This schema does not define projection-policy semantics; those belong to:

```text
docs/implementation/specifications/projection_policy_registry_spec.md
```

This schema does not define RDGP scoring, diagnosis, prioritization, or final
biological interpretation.

This schema does not define builder execution order, implementation plans,
contracts, fixtures, or executable validators.

## 4. Schema Invariant

TEP-VDB must carry one unified source corpus and shared substrates. Method
surfaces such as MPLC and CFBS must be projection surfaces inside that same
product, not separate ingestion modes.

```text
VDB integrates source TEPs once.
TEP-VDB carries the unified reason-ready projection substrate.
MPLC and CFBS are method-specific rooms inside TEP-VDB.
RDGP reasons over VDB-emitted surfaces.
RDGP does not independently overlay VAP and GSC.
```

The schema must preserve the scientific separation:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

## 5. Logical Package Layout

A TEP-VDB projection-surface package should follow this logical layout:

```text
tep_vdb/
    envelope
    manifest

    source_corpus/
        source_tep_index
        vap_source_packages
        gsc_source_packages

    shared_substrates/
        coordinate_observations
        sample_variant_observations
        feature_declarations
        gene_annotations
        gsc_prior_overlays
        opportunity_space
        variant_filter_partitions
        projection_policy_registry
        source_traceability

    projection_surfaces/
        projection_surface_index

        mplc/
            method_surface_manifest
            ...

        cfbs/
            method_surface_manifest
            ...

    validation_receipts/
        schema_validation_receipts
        source_corpus_validation_receipts
        shared_substrate_validation_receipts
        projection_surface_validation_receipts
```

This layout is logical rather than a final archive-format mandate. Derived
implementation contracts may choose TSV, JSON, JSONL, SQLite, or packaged
archive forms, but they must preserve these containers and relationships.

## 6. Required Top-Level Containers

A TEP-VDB projection-surface package must contain or reference the following
logical containers:

```text
tep_vdb_envelope
tep_vdb_manifest
source_tep_index
shared_substrate_index
projection_surface_index
method_surface_manifest for each projection surface
validation_receipt_index
source_traceability_index
```

A package may include additional method-specific tables, but those tables must
be registered through the relevant method-surface manifest.

## 7. TEP-VDB Envelope Schema

The envelope identifies the TEP-VDB package and binds it to upstream VDB build
state.

Required fields:

```text
tep_vdb_id
tep_vdb_schema_id
tep_vdb_schema_version
tep_vdb_build_id
created_at_utc
vdb_repository_version
source_corpus_id
genome_build
assertion_record_build_id
topology_build_id
opportunity_model_id
projection_policy_registry_id
emission_policy_id
status
```

Conditionally required fields:

```text
geometry_build_id
```

`geometry_build_id` is required when the package contains numerical burden,
recurrence, contrast, expected-burden, null-distribution, or candidate-ranking
outputs. It may be absent or explicitly marked `not_applicable` for packages
that only carry preserved substrates and projection-policy declarations.

Controlled values for `status`:

```text
draft
validated
validated_with_warnings
failed_validation
deprecated
```

## 8. Manifest Schema

The package manifest lists all package members and their semantic roles.

Required fields:

```text
manifest_record_id
tep_vdb_id
relative_path
container_name
object_name
object_class
schema_id
schema_version
required_status
row_count
checksum_if_available
validation_status
```

Controlled values for `object_class`:

```text
envelope
manifest
source_corpus
shared_substrate
projection_surface
method_surface_manifest
method_table
validation_receipt
source_traceability
policy_registry
opportunity_space
```

Controlled values for `required_status`:

```text
required
conditional
optional
not_applicable
```

## 9. Source Corpus Schema

The source corpus records the producer TEP packages integrated into the TEP-VDB.
The generic schema must not hard-code the first epilepsy demonstration source
count.

Required fields for `source_tep_index`:

```text
source_tep_id
source_corpus_id
producer_family
producer_package_id
producer_run_id
producer_release_id
source_tep_type
sample_id
assay_type
phenotype_scope
genome_build
source_artifact_path
source_traceability_id
included_status
exclusion_reason
```

Controlled values for `producer_family`:

```text
VAP
GSC
RSP
RDGP
other
```

Controlled values for `included_status`:

```text
included
excluded
excluded_with_receipt
missing_expected_source
not_applicable
```

Source-corpus count fields belong in the package envelope or analysis scope as
generic integers:

```text
source_tep_count
vap_tep_count
gsc_tep_count
rsp_tep_count
other_tep_count
```

The planned first epilepsy demonstration may validate these as:

```text
source_tep_count == 14
vap_tep_count == 12
gsc_tep_count == 2
```

but that constraint belongs to a demonstration validation profile, not the
generic schema.

## 10. Shared Substrates Schema

Shared substrates are evidence or governance layers that may be consumed by one
or more projection surfaces.

Required fields for `shared_substrate_index`:

```text
substrate_id
tep_vdb_id
substrate_name
substrate_class
substrate_path
schema_id
schema_version
row_count
checksum_if_available
required_status
source_traceability_id
validation_status
```

Controlled values for `substrate_class`:

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
other
```

### 10.1 Coordinate Observations

Coordinate observations describe reference-context variant evidence independent
of whether a variant is later projected to a gene, region, feature, or prior.
They are numerator substrate, not denominator substrate.

Required identity concepts:

```text
coordinate_variant_handle
genome_build
chromosome
position_or_interval
reference_allele
alternate_allele
normalization_status
source_traceability_id
```

### 10.2 Sample Variant Observations

Sample variant observations represent sample-specific observations of coordinate
variants. Burden counts must operate over sample-specific observations, not over
duplicated annotation rows.

Required identity concepts:

```text
sample_variant_observation_id
coordinate_variant_handle
sample_id
run_id
assay_type
quality_state
genotype_state
zygosity_state
dosage_state
source_traceability_id
```

Genotype, zygosity, and dosage fields may be unavailable in early surfaces, but
their availability state must be explicit.

### 10.3 Feature Declarations

Feature declarations preserve annotations, consequences, transcript mappings,
gene mappings, surveillance labels, and other feature-level declarations. They
must not be counted as independent observed variants unless linked back to a
sample-specific coordinate observation.

### 10.4 Opportunity Space

Opportunity-space substrates declare denominator evidence: what could have been
observed under assay, callability, quality, and model constraints. Opportunity
semantics are governed by `opportunity_space_spec.md`.

### 10.5 Projection Policy Registry

The projection-policy registry declares the policies used to create projection
memberships, windows, locus sets, filters, matching rules, null models,
annotation overlays, and emission surfaces. Policy semantics are governed by
`projection_policy_registry_spec.md`.

## 11. Projection Surface Index Schema

The projection surface index declares the method-specific rooms included in the
TEP-VDB package.

Required fields:

```text
projection_surface_id
tep_vdb_id
method_id
method_version
surface_class
surface_path
surface_schema_id
surface_schema_version
opportunity_model_id
projection_policy_registry_id
primary_policy_ids
source_corpus_id
status
validation_status
```

Controlled values for `surface_class`:

```text
mplc
cfbs
future_method
other
```

Controlled values for `status`:

```text
draft
emitted
validated
validated_with_warnings
failed_validation
deprecated
```

## 12. Method Surface Container Schema

Each method surface must include a method-surface manifest.

Required fields for `method_surface_manifest`:

```text
projection_surface_id
method_id
method_version
surface_schema_id
surface_schema_version
required_shared_substrates
required_policy_ids
required_opportunity_model_ids
primary_result_tables
membership_tables
null_model_tables
annotation_tables
validation_receipts
anti_overclaim_label_set
burden_readiness_status
```

Controlled values for `burden_readiness_status`:

```text
burden_ready
exploratory_only
not_burden_ready
denominator_unavailable
opportunity_unmodeled
not_applicable
```

A method surface that emits burden counts, burden rates, expected burden,
observed/expected ratios, empirical tail probabilities, recurrence surfaces, or
candidate intervals must reference an `opportunity_model_id` or explicitly mark
opportunity as unmodeled and set `burden_readiness_status` to a non-ready value.

## 13. Method Room Placeholders

This schema reserves containers for method-specific surfaces but does not define
their final field contracts.

### 13.1 MPLC Room

The MPLC room may contain:

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

The exact MPLC field contract belongs to:

```text
docs/implementation/specifications/mplc_projection_surface_spec.md
```

### 13.2 CFBS Room

The CFBS room may contain:

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

The exact CFBS field contract belongs to:

```text
docs/implementation/specifications/cfbs_projection_surface_spec.md
```

## 14. Validation Receipt Schema

Validation receipts record schema-level and surface-level checks.

Required fields:

```text
validation_receipt_id
tep_vdb_id
projection_surface_id
validation_scope
validation_check
validation_status
severity
message
source_object_id
validator_id
validator_version
created_at_utc
```

Controlled values for `validation_scope`:

```text
schema
source_corpus
shared_substrate
opportunity_space
projection_policy
projection_surface
method_surface
traceability
anti_overclaim
```

Controlled values for `validation_status`:

```text
pass
warn
fail
not_applicable
not_evaluated
```

Controlled values for `severity`:

```text
info
warning
error
critical
```

## 15. Source Traceability Requirements

Traceability is structural, not optional.

A TEP-VDB projection-surface package must support the following traceability
rules:

```text
1. Every projection surface traces to source_corpus_id.
2. Every source TEP traces to a producer package, run, release, or artifact.
3. Every burden-relevant table traces to sample_variant_observation_id or an equivalent source-coordinate observation handle.
4. Every GSC-prior label traces to GSC release, phenotype scope, and semantic-prior identity where available.
5. Every opportunity-dependent result declares opportunity_model_id.
6. Every policy-generated membership declares policy_id and policy_version.
7. Every method result carries an interpretation or anti-overclaim label.
```

A projection surface that cannot satisfy source-coordinate traceability may be
preserved as an incomplete artifact, but it must not be marked reason-ready.

## 16. Demonstration Profile Rules

The generic schema must allow arbitrary source-corpus sizes.

The first epilepsy demonstration profile may define additional validation rules:

```text
source_tep_count == 14
vap_tep_count == 12
gsc_tep_count == 2
expected epilepsy GSC source present
expected mitochondrial disease GSC source present
expected 12 epilepsy VAP source packages present
RDGP does not re-ingest VAP or GSC producer packages
```

These profile rules should be implemented as validation-profile checks, not as
generic schema invariants.

## 17. Schema-Level Validation Rules

Schema-level validation should check:

```text
1. TEP-VDB envelope is present.
2. TEP-VDB manifest is present.
3. Source corpus index is present.
4. Source counts are internally consistent.
5. All source TEPs have producer_family and source traceability.
6. Shared substrate index is present.
7. Projection policy registry is referenced.
8. Opportunity model is referenced or explicitly unmodeled.
9. Every projection surface has a method-surface manifest.
10. Every method-surface manifest references required shared substrates.
11. Every method-surface manifest references required policy IDs.
12. No method surface declares burden_ready without opportunity support.
13. No method surface lacks anti-overclaim labels.
14. No projection surface requires RDGP-side re-ingestion of VAP/GSC.
15. Every burden-relevant result traces to sample-specific coordinate observations.
```

## 18. Failure Modes

The following states should fail validation or produce explicit warnings:

```text
missing envelope
missing manifest
missing source corpus index
missing shared substrate index
missing projection surface index
method surface without method manifest
burden-ready surface without opportunity model
burden counts based on annotation rows rather than sample observations
GSC-prior label without GSC traceability
policy-generated membership without policy ID/version
hard-coded demonstration source count in generic schema
RDGP-side re-ingestion requirement
missing anti-overclaim label
unknown opportunity coerced to zero
```

Critical failures should block reason-ready TEP-VDB emission. Warnings may allow
artifact preservation but must prevent unsupported burden-ready or RDGP-ready
claims.

## 19. Future Extensions

Future schema revisions may add:

```text
additional producer families
additional projection-surface methods
multiple genome-build support
liftover or cross-build mapping receipts
sample-family or inheritance-aware observation layers
long-read or structural-variant opportunity models
external annotation bundle manifests
compact binary matrix packaging
formal JSON Schema or frictionless table schema emission
```

Future extensions must preserve the core invariant that TEP-VDB binds source
traceability, opportunity accounting, projection-policy declaration, method
surfaces, validation receipts, and anti-overclaim labels into one VDB-emitted
transport product.

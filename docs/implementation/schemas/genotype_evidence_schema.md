# Genotype Evidence Schema

**Status:** schema draft  
**Intended path:** `docs/implementation/schemas/genotype_evidence_schema.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** Logical VDB schemas for genotype evidence preservation, brokerage, receipts, declarations, and topology-ready substrates  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Design parent:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Specification parent:** `docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md`  
**Primary brokerage policy:** `docs/design/multiallelic_relationships_vdb_brokerage_policy.md`  

---

## 1. Purpose

This document defines the logical schema surfaces VDB should use to represent
first-class genotype evidence from genotype-capable TEP-VAP packages.

The ingestion specification defines required behavior.

This schema defines the VDB-side representational layers needed to preserve
producer genotype observations, route relationship handling, register direct
relationships, construct VDB-derived brokerage relationships, emit brokerage
receipts, prepare Assertion Records, and expose topology-ready genotype
substrates.

The central schema doctrine is:

```text
VDB schema separates source genotype observations from VDB-derived
genotype-to-variant relationships.
```

The schema must make it structurally impossible to mistake a VDB-derived
genotype-to-variant relationship for a producer-emitted genotype observation.

---

## 2. Scope

This schema defines logical VDB surfaces for:

```text
source genotype observation preservation

genotype artifact and package indexing

execution provenance context indexing

relationship input routing

direct producer-declared genotype-to-variant relationships

VDB-derived genotype-to-variant relationships

genotype brokerage receipts

genotype declaration sets for Assertion Records

genotype topology members and relationship basis

enumerations and missing-value semantics
```

This document does not define:

```text
SQL DDL

SQLite migrations

ORM models

physical indexes

API schemas

CLI behavior

test names

TEP-VDB projection surface schemas

RDGP reasoning schemas
```

Those belong to implementation and downstream projection documents.

---

## 3. Schema Principles

### 3.1 Preserve Producer Truth First

VDB must preserve every producer genotype observation row before deriving
relationships from it.

Schema implication:

```text
source_genotype_observations
    precedes
relationship input routing
    precedes
direct / derived relationship representation
    precedes
Assertion Records and topology surfaces
```

### 3.2 Separate Source Evidence from Derived Topology

A producer genotype observation is source evidence.

A VDB-derived genotype-to-variant relationship is topology.

The schema must preserve this distinction using explicit surfaces and explicit
fields such as:

```text
relationship_origin

relationship_state

relationship_derivation_policy_id

genotype_observation_id

genotype_variant_relationship_id
```

### 3.3 Preserve All Producer Columns

VDB may parse and index selected columns, but it must preserve all
producer-emitted genotype observation columns.

Known producer columns should be retained as typed/indexed fields where useful.

Unknown future columns should be retained in a source-preserved extension
representation rather than dropped.

### 3.4 Canonical Identities Are Additive

VDB may create canonical identities and persistence identities.

Those identities must not replace producer identities.

### 3.5 Receipts Are First-Class Schema Surfaces

Relationship brokerage and genotype preservation require receipts.

A derived relationship without a traceable policy and basis record is not
trusted topology.

---

## 4. Logical Surface Overview

The logical genotype schema consists of the following surfaces:

```text
source_genotype_package_classifications

source_genotype_observations

genotype_artifact_index

genotype_projection_summary_index

genotype_source_header_context_index

execution_provenance_context_index

genotype_relationship_input_index

direct_genotype_variant_relationships

derived_genotype_variant_relationships

genotype_brokerage_receipts

genotype_declaration_sets

genotype_topology_members

genotype_topology_relationship_basis
```

A future implementation may materialize these as SQL tables, TSV files,
dataclasses, or hybrid structures.

The logical boundaries must remain intact.

---

## 5. Identity Ownership

### 5.1 Producer-Owned Identities

Producer-owned identities originate in VAP and must remain recoverable exactly
as emitted.

Examples:

```text
genotype_observation_id

genotype_observation_id_version

sample_id

sample_alias

sra_accession

run_id

vcf_sample_column_name

source_vcf_path

source_vcf_sha256

source_vcf_header_hash

source_record_ordinal

source_line_number

source_record_hash

variant_id when producer-direct

variant_observation_id when emitted
```

### 5.2 TEP-Owned Identities

TEP-owned identities describe transport.

Examples:

```text
tep_id

entity_id

lineage_entity_id

artifact_id

artifact_path

artifact_sha256
```

### 5.3 VDB-Owned Identities

VDB-owned identities support persistence, brokerage, topology, and discovery.

Examples:

```text
source_package_id

registration_unit_id

genotype_relationship_input_id

genotype_variant_relationship_id

brokerage_receipt_id

declaration_set_id

topology_member_id

topology_relationship_id

canonical_variant_id

variant_identity_id

sample_variant_observation_id
```

VDB-owned identities are additive.

They must never replace producer-owned identities.

---

## 6. Common Fields

The following fields may appear across multiple genotype schema surfaces.

| Field | Requirement | Description |
|---|---:|---|
| `source_package_id` | required | VDB package identity for the ingested producer package. |
| `tep_id` | recommended | Transport package identity when available. |
| `producer_type` | required | Producer package type, for example `TEP-VAP` or `TEP-GSC`. |
| `producer_genotype_applicability_state` | required where package-scoped | Whether genotype applies to the declared producer package type. |
| `genotype_capability_state` | required where package-scoped | Canonical genotype capability state assigned by VDB. |
| `genotype_maturity_state` | required where package-scoped genotype classification is recorded | Highest validated genotype maturity tier for a genotype-applicable package, or `genotype_maturity_not_applicable` when genotype is outside the producer package's evidence domain. |
| `sample_id` | required where sample-scoped | Producer sample identity. |
| `run_id` | required where run-scoped | Producer run identity. |
| `genotype_observation_id` | required for genotype evidence | Producer genotype observation identity. |
| `source_record_hash` | required for row traceability | Producer source VCF record hash. |
| `source_vcf_sha256` | recommended / required for trusted ingestion when emitted | Source VCF identity. |
| `source_vcf_header_hash` | recommended / required for trusted ingestion when emitted | Source VCF header/context identity. |
| `reference_build` | required where coordinate-scoped | Reference build declared by producer. |
| `chromosome` | required where coordinate-scoped | Source chromosome/contig. |
| `position` | required where coordinate-scoped | Source 1-based position as emitted by producer. |
| `reference_allele` | required where allele-scoped | Source reference allele. |
| `alternate_alleles_raw` | required for multiallelic brokerage | Source ALT list preserving order. |
| `called_allele_indices` | required for allele-index brokerage when emitted | Called allele indices parsed from GT. |
| `traceability_refs` | recommended | Structured references to source artifacts, rows, policies, and receipts. |

---

## 6A. `source_genotype_package_classifications`

### 6A.1 Purpose

`source_genotype_package_classifications` records the package-level genotype
scope classification produced during VDB discovery.

This surface distinguishes three independent questions:

```text
Does genotype apply to the producer package type?

What genotype capability did the package provide?

What validated genotype maturity state applies to the package?
```

Package classification must be completed before genotype-specific artifact or
row-level evidence is trusted.

### 6A.2 Cardinality

```text
exactly one row per registered source package
```

A package must not receive multiple competing genotype classifications.

### 6A.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `package_id` | required | Registered VDB package identity and foreign-key basis for the package classification. |
| `tep_id` | recommended | Transport package identity when available. |
| `producer_family` | required | Explicit classifier-dispatch family, currently `VAP` or `GSC`. |
| `producer_type` | optional | Transport-facing producer type, for example `TEP-VAP` or `TEP-GSC`, when retained separately from the classifier family. |
| `producer_genotype_applicability_state` | required | Whether genotype belongs to the producer package type's evidence domain. |
| `genotype_capability_state` | required | Package-level genotype capability classification. |
| `genotype_maturity_state` | required | Validated genotype maturity tier or explicit not-applicable state. |
| `genotype_artifact_set_status` | required | State of the canonical genotype artifact set for this package. |
| `execution_provenance_status` | required | Package execution-provenance requirement and registration state. |
| `classification_status` | required | Whether package genotype classification completed successfully. |
| `classification_reason` | required | Governed reason for the assigned classification. |
| `trusted_modern_ingestion_ready` | required | Whether the package is eligible for trusted modern genotype ingestion. |
| `traceability_refs` | recommended | References to package governance artifacts and validation receipts. |

### 6A.4 Classifier Naming Boundary

The implemented package-classification surface uses:

```text
package_id

producer_family
```

`producer_family` is the explicit dispatch key used to select producer-specific
genotype classification rules.

Current governed values are:

```text
VAP

GSC
```

`producer_type`, when retained, is transport metadata and may use values such as:

```text
TEP-VAP

TEP-GSC
```

`producer_type` must not silently replace `producer_family` as the classifier
dispatch key.

Likewise, `source_package_id` may remain the logical package-reference field on
other downstream genotype surfaces, but the implemented
`source_genotype_package_classifications` surface uses `package_id`.

These names must not be treated as interchangeable without an explicit mapping.

### 6A.5 Required Classification Pairings

Canonical package-level pairings include:

```text
modern genotype-capable TEP-VAP:
    producer_family =
        VAP

    producer_genotype_applicability_state =
        genotype_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_available

    genotype_maturity_state =
        genotype_discovered

legacy variant-only TEP-VAP:
    producer_family =
        VAP

    producer_genotype_applicability_state =
        genotype_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_unavailable_legacy

    genotype_maturity_state =
        genotype_discovered

TEP-GSC:
    producer_family =
        GSC

    producer_genotype_applicability_state =
        genotype_not_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_not_applicable

    genotype_maturity_state =
        genotype_maturity_not_applicable
```

`classification_status` communicates whether VDB successfully evaluated and
recorded the package classification.

It must not be replaced by misuse of `genotype_maturity_state`.

### 6A.6 Required Invariants

```text
genotype_capability_not_applicable
    requires
genotype_not_applicable_to_producer_type
    and
genotype_maturity_not_applicable

genotype_maturity_not_applicable
    must not be assigned to a genotype-applicable producer package

genotype_discovered
    must not be assigned to a genotype-not-applicable producer package

genotype_capability_unavailable_legacy
    requires a genotype-applicable producer package

one package_id
    has exactly one package-level genotype classification

one package classification
    has exactly one explicit producer_family dispatch value
```

Future producer families must receive explicit producer-specific classification
rules.

They must not silently inherit TEP-VAP or TEP-GSC classification semantics.

---

## 7. `source_genotype_observations`

### 7.1 Purpose

`source_genotype_observations` preserves genotype observations emitted by
TEP-VAP.

This is the immutable producer-truth surface.

Every trusted genotype-aware VDB ingestion must preserve this surface before
relationship registration or brokerage.

### 7.2 Cardinality

```text
one row per producer-emitted genotype observation
```

A source genotype observation may later map to:

```text
zero, one, or multiple VDB relationship rows
```

That later relationship cardinality must not alter the source observation
cardinality.

### 7.3 Required Preservation Behavior

The surface must preserve:

```text
all columns emitted in entities/genotype/genotype_observations.tsv

source row order or source record ordinal

source row identity

source row content hash or equivalent reconstructability proof
```

Known `genotype_observation_v1` fields should be typed and indexed where useful.

Unknown future fields must be retained in a source-preserved extension field or
equivalent raw row representation.

The combination of typed/indexed fields plus source-preserved extension fields
must be sufficient to reconstruct the producer-emitted genotype observation row.

VDB-normalized convenience fields must not replace raw producer values.

### 7.4 Required Index / Integrity Fields

| Field | Requirement | Description |
|---|---:|---|
| `source_package_id` | required | VDB package identity. |
| `tep_id` | recommended | TEP transport identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `genotype_observation_id_version` | required when emitted | Producer identity version. |
| `schema_version` | required | Producer genotype schema version. |
| `entity_type` | required when emitted | Expected producer entity type. |
| `evidence_class` | required when emitted | Producer evidence class. |
| `sample_id` | required | Producer sample identity. |
| `run_id` | required | Producer run identity. |
| `source_vcf_sha256` | required for trusted ingestion when emitted | Source VCF checksum. |
| `source_vcf_header_hash` | required for trusted ingestion when emitted | Source VCF header checksum/hash. |
| `source_record_ordinal` | required when emitted | Source VCF record order. |
| `source_line_number` | recommended when emitted | Source line number. |
| `source_record_hash` | required | Source VCF record hash. |
| `reference_build` | required | Reference build. |
| `chromosome` | required | Source chromosome/contig. |
| `position` | required | Source position. |
| `reference_allele` | required | Source REF allele. |
| `alternate_alleles_raw` | required | Raw ordered ALT list. |
| `variant_relationship_status` | required | Producer relationship status. |
| `relationship_reason` | required when emitted | Producer relationship reason. |
| `relationship_resolution_target` | required when emitted | Producer relationship resolution target. |
| `raw_source_row_hash` | recommended | Hash of preserved source row serialization. |
| `raw_source_row_repr` | optional | Raw row or JSON-preserved row when physical design requires it. |

### 7.5 Anti-Collapse Rule

This surface must not contain VDB-derived relationship rows.

A VDB-derived relationship must be represented in relationship surfaces, not as
a new row in `source_genotype_observations`.

---

## 8. `genotype_artifact_index`

### 8.1 Purpose

`genotype_artifact_index` records discovered genotype-related artifacts and
their package governance status.

It supports package classification and genotype artifact-set validation.

### 8.2 Cardinality

```text
one row per genotype-related artifact per source package
```

### 8.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `source_package_id` | required | VDB package identity. |
| `tep_id` | recommended | TEP transport identity. |
| `run_id` | recommended | Producer run identity when discoverable. |
| `sample_id` | recommended | Producer sample identity when discoverable. |
| `artifact_role` | required | Role of artifact. |
| `artifact_path` | required | Path within TEP package. |
| `artifact_sha256` | required for trusted modern genotype ingestion for canonical genotype artifacts | Artifact checksum. |
| `schema_version` | recommended | Artifact schema version. |
| `row_count` | recommended where tabular | Row count. |
| `column_count` | recommended where tabular | Column count. |
| `entity_inventory_status` | required | Inventory registration status. |
| `lineage_status` | required | Lineage registration status. |
| `validation_status` | required | Validation state. |
| `artifact_set_status` | required | Complete/incomplete/invalid status. |

For trusted modern genotype-capable TEP-VAP ingestion, checksum absence for a
canonical genotype artifact is not a normal trusted-ingestion state.

Legacy, compatibility, quarantine, or unsupported-version paths may explicitly
represent checksum absence.

### 8.4 Allowed `artifact_role` Values

```text
genotype_observations

genotype_projection_summary

genotype_source_header_context

execution_provenance_context
```

---

## 9. `genotype_projection_summary_index`

### 9.1 Purpose

`genotype_projection_summary_index` records parsed package-level genotype
projection summary values from:

```text
entities/genotype/genotype_projection_summary.json
```

This surface supports package classification, count reconciliation, relationship
partition validation, and validation receipt generation.

### 9.2 Cardinality

```text
zero or one row per genotype-capable source package
```

Legacy non-genotype packages should not synthesize this row.

### 9.3 Fields

| Field                                    |                           Requirement | Description                                                     |
| ---------------------------------------- | ------------------------------------: | --------------------------------------------------------------- |
| `source_package_id`                      |                              required | VDB package identity.                                           |
| `tep_id`                                 |                           recommended | TEP transport identity.                                         |
| `producer_type`                          |                              required | Producer package type.                                          |
| `sample_id`                              |                           recommended | Producer sample identity when applicable.                       |
| `run_id`                                 |                           recommended | Producer run identity when applicable.                          |
| `artifact_path`                          |                              required | Path to genotype projection summary artifact.                   |
| `artifact_sha256`                        | required for trusted modern ingestion | Artifact checksum.                                              |
| `schema_version`                         |                              required | Summary schema version.                                         |
| `genotype_observation_row_count`         |                              required | Producer-declared genotype observation row count.               |
| `source_record_count`                    |                           recommended | Producer-declared source record count when emitted.             |
| `direct_relationship_count`              |                           recommended | Producer-declared direct relationship count.                    |
| `complex_relationship_count`             |                           recommended | Producer-declared complex relationship count.                   |
| `unresolved_relationship_count`          |                           recommended | Producer-declared unresolved relationship count when emitted.   |
| `not_applicable_relationship_count`      |                           recommended | Producer-declared not-applicable count when emitted.            |
| `projection_status`                      |                 required when emitted | Producer genotype projection status.                            |
| `projection_error_count`                 |                           recommended | Producer projection error count.                                |
| `projection_warning_count`               |                           recommended | Producer projection warning count.                              |
| `unresolved_relationship_count_reported` |                           recommended | Whether unresolved count was producer-reported or VDB-computed. |
| `summary_reconciliation_state`           |                              required | VDB reconciliation state.                                       |
| `traceability_refs`                      |                           recommended | Source artifact and validation references.                      |

### 9.4 Anti-Collapse Rule

This surface summarizes producer genotype projection.

It must not be treated as genotype observation evidence or VDB brokerage output.

---

## 10. `genotype_source_header_context_index`

### 10.1 Purpose

`genotype_source_header_context_index` records parsed source-header context from:

```text
entities/genotype/genotype_source_header_context.json
```

This surface preserves source VCF/header context needed for source identity,
sample-column identity, FORMAT definition awareness, reference-build context,
and future auditability.

### 10.2 Cardinality

```text
zero or one row per genotype-capable source package
```

Legacy non-genotype packages should not synthesize this row.

### 10.3 Fields

| Field                     |                           Requirement | Description                                             |
| ------------------------- | ------------------------------------: | ------------------------------------------------------- |
| `source_package_id`       |                              required | VDB package identity.                                   |
| `tep_id`                  |                           recommended | TEP transport identity.                                 |
| `producer_type`           |                              required | Producer package type.                                  |
| `sample_id`               |                           recommended | Producer selected sample identity.                      |
| `run_id`                  |                           recommended | Producer run identity.                                  |
| `artifact_path`           |                              required | Path to genotype source-header context artifact.        |
| `artifact_sha256`         | required for trusted modern ingestion | Artifact checksum.                                      |
| `schema_version`          |                              required | Header-context schema version.                          |
| `source_vcf_sha256`       | required for trusted modern ingestion | Source VCF identity.                                    |
| `source_vcf_header_hash`  | required for trusted modern ingestion | Source VCF header identity.                             |
| `reference_build`         |                required where emitted | Reference build declared by producer context.           |
| `contig_count`            |                           recommended | Number of contigs represented in source-header context. |
| `format_definition_count` |                           recommended | Number of FORMAT definitions represented.               |
| `sample_column_count`     |                           recommended | Number of sample columns represented in source context. |
| `selected_sample_column`  |                           recommended | Selected VCF sample column name.                        |
| `header_context_state`    |                              required | VDB header-context validation state.                    |
| `traceability_refs`       |                           recommended | Source artifact and validation references.              |

### 10.4 Anti-Collapse Rule

This surface is source context.

It must not be treated as genotype observation evidence, variant evidence, or
relationship brokerage output.

---

## 11. `execution_provenance_context_index`

### 11.1 Purpose

`execution_provenance_context_index` registers execution provenance as package
and run context.

It must not be mixed into biological evidence surfaces.

### 11.2 Cardinality

```text
zero or one execution provenance context row per source package
```

Trusted modern genotype-capable TEP-VAP ingestion requires one execution
provenance context row.

Legacy, compatibility, quarantine, or unsupported-version paths may explicitly
represent absence.

### 11.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `source_package_id` | required | VDB package identity. |
| `tep_id` | recommended | TEP identity. |
| `run_id` | recommended | Producer run identity. |
| `artifact_path` | required for trusted modern genotype ingestion | Execution provenance artifact path. |
| `artifact_sha256` | required for trusted modern genotype ingestion | Artifact checksum. |
| `contract_status` | recommended | Execution provenance contract state. |
| `provenance_completeness` | recommended | Completeness state. |
| `resolution_mode` | recommended | How provenance was resolved. |
| `toolchain_status` | recommended | Toolchain context status. |
| `annotation_environment_status` | recommended | Annotation environment status. |
| `resource_environment_status` | recommended | Resource environment status. |
| `registered_as_context` | required | Must be true for this surface. |
| `context_role` | required | Expected value: `execution_provenance`. |

### 11.4 Anti-Collapse Rule

Rows in this surface must not be interpreted as variant evidence, genotype
evidence, pathogenicity evidence, phenotype evidence, or reasoning evidence.

---

## 12. `genotype_relationship_input_index`

### 12.1 Purpose

`genotype_relationship_input_index` routes preserved genotype observations into
relationship handling paths.

It is a routing/index surface, not a relationship-output surface.

### 12.2 Cardinality

```text
one row per source genotype observation requiring relationship classification
```

In practice, trusted genotype-aware ingestion should create one row for each
source genotype observation.

### 12.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `genotype_relationship_input_id` | required | VDB-owned input routing identity. |
| `source_package_id` | required | VDB package identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `sample_id` | required | Producer sample identity. |
| `run_id` | required | Producer run identity. |
| `source_record_hash` | required | Source record hash. |
| `variant_relationship_status` | required | Producer relationship status. |
| `relationship_reason` | recommended | Producer relationship reason. |
| `relationship_resolution_target` | recommended | Producer relationship target. |
| `variant_id` | optional | Producer variant ID when emitted. |
| `variant_observation_id` | optional | Producer variant observation ID when emitted. |
| `alternate_alleles_raw` | recommended | Raw ALT list. |
| `alternate_allele_count` | recommended | ALT count. |
| `called_allele_indices` | recommended | Called allele indices. |
| `relationship_input_class` | required | VDB routing class. |
| `brokerage_required` | required | Boolean-like state. |
| `brokerage_reason` | recommended | Reason brokerage is required. |
| `input_validation_state` | required | Valid/invalid/not evaluated. |

### 12.4 Allowed `relationship_input_class` Values

```text
direct_relationship_input

complex_relationship_input

unresolved_relationship_input

not_applicable_relationship_input

unsupported_relationship_input
```

---

## 13. `direct_genotype_variant_relationships`

### 13.1 Purpose

`direct_genotype_variant_relationships` registers producer-declared direct
genotype-to-variant relationships.

These are source-direct relationships, not VDB-derived brokerage relationships.

### 13.2 Cardinality

```text
zero or one direct relationship row per eligible direct genotype observation
```

A direct relationship is eligible only when producer fields support direct
registration under the ingestion specification.

### 13.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `genotype_variant_relationship_id` | required | VDB-owned relationship identity. |
| `relationship_origin` | required | Expected value: `producer_declared`. |
| `relationship_state` | required | Expected value: `direct_source_biallelic`. |
| `source_package_id` | required | VDB package identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `variant_id` | required | Producer variant ID. |
| `variant_observation_id` | recommended | Producer variant observation ID when emitted. |
| `sample_id` | required | Producer sample identity. |
| `run_id` | required | Producer run identity. |
| `source_record_hash` | required | Source record hash. |
| `producer_relationship_status` | required | Producer relationship status. |
| `producer_relationship_reason` | recommended | Producer relationship reason. |
| `producer_relationship_resolution_target` | recommended | Producer relationship target. |
| `traceability_state` | required | Traceability completeness state. |
| `traceability_refs` | recommended | Source artifact/row references. |

### 13.4 Anti-Collapse Rule

Rows in this surface must never be used to represent multiallelic-derived or
normalization-brokered relationships.

---

## 14. `derived_genotype_variant_relationships`

### 14.1 Purpose

`derived_genotype_variant_relationships` represents VDB-derived
genotype-to-variant relationships.

These rows are topology.

They are not producer genotype observations.

### 14.2 Cardinality

```text
zero, one, or multiple rows per source genotype observation
```

### 14.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `genotype_variant_relationship_id` | required | VDB-owned derived relationship identity. |
| `relationship_origin` | required | Expected value: `vdb_derived`. |
| `relationship_type` | required | Type of relationship edge. |
| `relationship_state` | required | Specific VDB relationship state. |
| `source_package_id` | required | VDB package identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `sample_id` | required | Producer sample identity. |
| `run_id` | required | Producer run identity. |
| `source_record_hash` | required | Source record hash. |
| `reference_build` | required where resolved | Reference build. |
| `chromosome` | required where resolved | Chromosome/contig. |
| `position` | required where resolved | Position. |
| `reference_allele` | required where resolved | Source REF allele. |
| `source_record_alt` | recommended | Source ALT list. |
| `allele_index` | required where allele-index derived | Called allele index. |
| `source_alt_allele` | required where allele-index derived | Source ALT allele at index. |
| `variant_identity_id` | optional | VDB or canonical variant identity when resolved. |
| `sample_variant_observation_id` | optional | Sample-specific variant observation identity when resolved. |
| `variant_normalization_policy_id` | recommended where normalization participates | Normalization policy. |
| `normalization_state` | required | Normalization state. |
| `ambiguity_state` | required | Ambiguity state. |
| `lossiness_state` | required | Lossiness state. |
| `identity_registration_state` | required | Identity registration state. |
| `traceability_state` | required | Source traceability state. |
| `relationship_derivation_policy_id` | required | VDB brokerage policy identity. |
| `anti_overclaim_label` | required | Anti-overclaim label. |
| `traceability_refs` | recommended | Source and policy references. |

### 14.4 Allowed `relationship_type` Values

```text
genotype_observation_resolved_to_alt_allele

genotype_observation_brokered_to_variant_identity

genotype_observation_brokered_to_sample_variant_observation

genotype_observation_relationship_unresolved

genotype_observation_relationship_ambiguous
```

### 14.5 Anti-Collapse Rule

Rows in this surface must not be counted as producer genotype observations.

---

## 15. `genotype_brokerage_receipts`

### 15.1 Purpose

`genotype_brokerage_receipts` records the outcome of VDB brokerage evaluation
for brokerage-required genotype observations.

Receipts make complex-row handling auditable.

### 15.2 Cardinality

```text
zero or one receipt per brokerage-required genotype observation per brokerage
policy evaluation
```

### 15.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `brokerage_receipt_id` | required | VDB-owned receipt identity. |
| `source_package_id` | required | VDB package identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `source_record_hash` | required | Source record hash. |
| `brokerage_policy_id` | required | Primary VDB brokerage policy. |
| `allele_index_mapping_policy_id` | recommended | Allele-index policy. |
| `variant_normalization_policy_id` | recommended | Variant normalization policy. |
| `symbolic_alt_policy_id` | recommended | Symbolic ALT policy. |
| `spanning_deletion_policy_id` | recommended | Spanning deletion policy. |
| `brokerage_input_state` | required | Input readiness state. |
| `brokerage_outcome` | required | Outcome state. |
| `derived_relationship_count` | required | Total derived relationship rows. |
| `resolved_relationship_count` | required | Resolved relationship count. |
| `ambiguous_relationship_count` | required | Ambiguous relationship count. |
| `unresolved_relationship_count` | required | Unresolved relationship count. |
| `not_evaluated_relationship_count` | required | Not-evaluated relationship count. |
| `failure_reason` | optional | Failure reason if applicable. |
| `warning_codes` | optional | Brokerage warning codes. |
| `traceability_refs` | recommended | Source and derived relationship refs. |

### 15.4 Required Invariant

For a brokerage-required genotype observation:

```text
derived_relationship_count
    ==
resolved_relationship_count
+ ambiguous_relationship_count
+ unresolved_relationship_count
+ not_evaluated_relationship_count
```

---

## 16. `genotype_declaration_sets`

### 16.1 Purpose

`genotype_declaration_sets` prepares genotype evidence for Phase 4.3 Assertion
Records.

This is a non-interpretive declaration substrate.

### 16.2 Cardinality

```text
zero or more declaration rows per genotype observation
```

### 16.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `declaration_set_id` | required | VDB-owned declaration identity. |
| `declaration_set_type` | required | Type of genotype declaration. |
| `source_package_id` | required | VDB package identity. |
| `sample_id` | recommended | Producer sample identity. |
| `run_id` | recommended | Producer run identity. |
| `genotype_observation_id` | required | Producer genotype observation ID. |
| `source_record_hash` | required | Source record hash. |
| `declaration_key` | required | Declared property key. |
| `declaration_value` | optional | Declared property value. |
| `declaration_state` | required | State of declaration. |
| `source_field` | recommended | Source producer field. |
| `source_artifact` | recommended | Source artifact path. |
| `source_artifact_sha256` | recommended | Source artifact checksum. |
| `traceability_refs` | recommended | Source trace references. |

### 16.4 Allowed `declaration_set_type` Values

```text
genotype_observation_declaration_set

genotype_source_record_declaration_set

genotype_relationship_status_declaration_set

genotype_called_allele_index_declaration_set

genotype_format_field_declaration_set

genotype_missingness_declaration_set

genotype_quality_context_declaration_set

genotype_brokerage_requirement_declaration_set
```

### 16.5 Prohibited Declaration Meaning

Declaration sets must not encode:

```text
dominant-compatible

recessive-compatible

compound-heterozygous

de-novo

carrier-diagnosis

biallelic-disease-model-satisfied

pathogenic-genotype

diagnostic-genotype
```

---

## 17. `genotype_topology_members`

### 17.1 Purpose

`genotype_topology_members` exposes genotype entities and relationship objects
as Phase 4.4 topology members.

### 17.2 Cardinality

```text
one row per genotype-related topology member
```

### 17.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `topology_member_id` | required | VDB-owned topology member identity. |
| `topology_member_type` | required | Type of topology member. |
| `source_package_id` | required | VDB package identity. |
| `entity_ref` | required | Referenced entity or relationship ID. |
| `entity_ref_type` | required | Type of referenced entity. |
| `genotype_observation_id` | optional | Producer genotype observation ID. |
| `genotype_variant_relationship_id` | optional | Relationship ID when member is relationship-scoped. |
| `source_record_hash` | recommended | Source record hash. |
| `member_state` | required | Topology member state. |
| `traceability_refs` | recommended | Source traceability references. |

### 17.4 Allowed `topology_member_type` Values

```text
genotype_observation

direct_genotype_variant_relationship

derived_genotype_variant_relationship

genotype_relationship_unresolved_state

genotype_brokerage_receipt

genotype_declaration_set
```

---

## 18. `genotype_topology_relationship_basis`

### 18.1 Purpose

`genotype_topology_relationship_basis` records why genotype topology
relationships exist.

This prevents topology edges from becoming receipt-free assertions.

### 18.2 Cardinality

```text
one or more basis rows per genotype topology relationship
```

### 18.3 Fields

| Field | Requirement | Description |
|---|---:|---|
| `topology_relationship_id` | required | VDB topology relationship identity. |
| `basis_id` | required | Basis identity. |
| `basis_type` | required | Basis type. |
| `source_artifact` | required | Source artifact path. |
| `source_artifact_sha256` | recommended | Source artifact checksum. |
| `genotype_observation_id` | required where genotype-scoped | Producer genotype observation ID. |
| `source_record_hash` | recommended | Source record hash. |
| `relationship_derivation_policy_id` | recommended | Derivation policy. |
| `normalization_policy_id` | recommended | Normalization policy. |
| `evidence_basis_state` | required | Basis state. |
| `lossiness_state` | recommended | Lossiness state. |
| `ambiguity_state` | recommended | Ambiguity state. |
| `traceability_refs` | recommended | Source and policy references. |

### 18.4 Allowed `basis_type` Values

```text
source_genotype_observation

direct_producer_relationship

vdb_brokerage_receipt

allele_index_mapping

normalization_policy

identity_registration

unresolved_relationship_state

ambiguity_state

lossiness_state
```

---

## 19. Enumerations

### 19.1 `genotype_capability_state`

```text
genotype_capability_available

genotype_capability_unavailable_legacy

genotype_capability_not_applicable

genotype_capability_incomplete

genotype_capability_invalid

genotype_capability_unsupported_version
```

Required semantic distinctions:

```text
genotype_capability_unavailable_legacy
    genotype applies to the producer package type, but the legacy package did
    not emit first-class genotype evidence

genotype_capability_not_applicable
    genotype is outside the declared producer package type's evidence domain
```

These values must not be treated as interchangeable.

### 19.2 `genotype_maturity_state`

For genotype-applicable producer packages, the cumulative maturity progression
is:

```text
genotype_discovered

genotype_preservation_validated

genotype_direct_relationships_registered

genotype_complex_relationships_preserved

genotype_brokerage_evaluated

genotype_assertion_ready

genotype_topology_ready

genotype_projection_ready
```

For producer package types whose evidence domains exclude genotype, the required
state is:

```text
genotype_maturity_not_applicable
```

`genotype_maturity_not_applicable` is not part of the cumulative genotype
maturity progression.

It means that genotype maturity does not apply to the producer package's
evidence grammar.

Package classification completion must be represented through
`classification_status` and validation receipts, not by assigning
`genotype_discovered` to a genotype-not-applicable producer package.

### 19.3 `relationship_origin`

```text
producer_declared

vdb_derived

not_applicable

not_evaluated
```

### 19.4 `relationship_state`

```text
direct_source_biallelic

resolved_from_multiallelic_record

brokered_with_normalization

resolved_from_split_normalized_record

ambiguous_requires_review

unresolved_missing_variant_identity

unresolved_symbolic_alt

unresolved_spanning_deletion

spanning_deletion_context_required

unresolved_malformed_gt

unresolved_allele_index_out_of_range

unresolved_normalization_ambiguous

unresolved_policy_not_available

not_evaluated
```

### 19.5 `brokerage_outcome`

```text
brokerage_not_evaluated

brokerage_resolved

brokerage_ambiguous

brokerage_unresolved

brokerage_policy_unavailable
```

### 19.6 `ambiguity_state`

```text
unambiguous

ambiguous

ambiguous_normalized_mapping

ambiguous_symbolic_mapping

ambiguous_source_context

not_applicable

not_evaluated
```

### 19.7 `lossiness_state`

```text
lossless

lossless_allele_index_mapping

lossless_normalized_mapping

potentially_lossy

lossy

not_applicable

not_evaluated
```

### 19.8 `normalization_state`

```text
no_normalization_required

normalized_losslessly

normalized_with_left_alignment

normalized_with_trimming

normalization_ambiguous

normalization_policy_unavailable

normalization_failed

not_applicable

not_evaluated
```

### 19.9 `identity_registration_state`

```text
variant_identity_registered

sample_variant_observation_registered

missing

unresolved

ambiguous

not_applicable

not_evaluated
```

### 19.10 `traceability_state`

```text
source_trace_complete

source_trace_partial

source_trace_missing

not_applicable
```

### 19.11 `depth_availability_state`

```text
allele_depth_available

allele_depth_missing

allele_depth_vector_length_mismatch

allele_depth_not_applicable

allele_depth_unparseable
```

### 19.12 `anti_overclaim_label`

```text
genotype_relationship_not_inheritance_interpretation

multiallelic_relationship_not_independent_producer_row

allele_depth_annotation_not_independent_ad_vector

resolved_relationship_not_direct_source_biallelic

genotype_state_not_disease_model

genotype_missingness_not_absence
```

---

## 20. Null and Missing-Value Semantics

The schema must preserve distinct missingness states.

### 20.1 Required Distinctions

VDB must distinguish:

```text
NULL / missing / unavailable

not_applicable

not_evaluated

unknown

unresolved

ambiguous

measured zero

empty producer field

producer sentinel value
```

### 20.2 Genotype-Specific Distinctions

VDB must not collapse:

```text
missing genotype artifact
    into no-call

no-call
    into absence

partial no-call
    into direct allele-specific certainty

missing variant identity
    into missing genotype observation

unresolved relationship
    into evidence absence

legacy genotype unavailable
    into homozygous reference

zero allele depth
    into missing allele depth
```

### 20.3 Raw Producer Sentinels

When producer TSV fields use sentinel values such as:

```text
NA
none
blank
not_applicable
not_evaluated
```

VDB must preserve the raw producer value and may additionally map it to a
normalized VDB nullability state.

Raw value preservation and normalized nullability state are distinct.

---

## 20A. Genotype-Not-Applicable Producer Representation

For producer package types whose evidence domain excludes genotype, VDB must
represent genotype scope explicitly without inventing legacy status.

Recommended package-scoped fields:

```text
package_id

tep_id

producer_family

producer_type

producer_genotype_applicability_state

genotype_capability_state

genotype_maturity_state

genotype_artifact_set_status

execution_provenance_status

classification_reason

traceability_refs
```

Recommended TEP-GSC values:

```text
producer_family = GSC

producer_type = TEP-GSC

producer_genotype_applicability_state =
    genotype_not_applicable_to_producer_type

genotype_capability_state =
    genotype_capability_not_applicable

genotype_maturity_state =
    genotype_maturity_not_applicable

genotype_artifact_set_status =
    genotype_artifact_set_not_applicable

execution_provenance_status =
    execution_provenance_not_applicable

classification_reason =
    genotype_not_applicable_to_producer_type
```

This representation means that genotype is outside the declared TEP-GSC
evidence grammar.

The fact that VDB evaluated and recorded this classification is represented by:

```text
classification_status = classified
```

and by the associated validation receipts.

It must not be represented by assigning:

```text
genotype_maturity_state = genotype_discovered
```

TEP-GSC contains phenotype-scoped gene evidence.

It does not contain sample-specific genotype evidence.

A genotype-not-applicable producer package must not synthesize:

```text
source_genotype_observations

genotype_relationship_input_index rows

direct genotype-to-variant relationships

derived genotype-to-variant relationships

genotype brokerage receipts
```

A genotype-not-applicable producer package must not be represented as:

```text
genotype_capability_unavailable_legacy
```

because legacy unavailability applies only when genotype belongs to the
producer's evidence domain but was not emitted by the legacy package.

---

## 21. Legacy Compatibility Representation

For older genotype-applicable TEP-VAP packages without genotype artifacts, VDB
may materialize explicit legacy states.

This representation does not apply to producer package types whose evidence
domain excludes genotype.

Recommended fields for legacy-compatible package records:

```text
package_id

tep_id

producer_family

producer_type

producer_genotype_applicability_state

genotype_capability_state

genotype_maturity_state

legacy_compatibility_mode

genotype_context_state

genotype_projection_state

legacy_reason

traceability_refs
```

Recommended values:

```text
producer_family = VAP

producer_type = TEP-VAP

producer_genotype_applicability_state =
    genotype_applicable_to_producer_type

genotype_capability_state =
    genotype_capability_unavailable_legacy

genotype_maturity_state =
    genotype_discovered

legacy_compatibility_mode = variant_only_legacy_compatibility_mode

genotype_context_state = genotype_context_unavailable

genotype_projection_state = genotype_projection_not_evaluated
```

For a legacy TEP-VAP package, `genotype_discovered` means that genotype
applicability and capability classification completed.

It does not mean that the package emitted genotype observations.

Legacy records must not advance beyond `genotype_discovered` without the
producer genotype substrate and the validation receipts required by the higher
maturity state.

Legacy records must not synthesize `source_genotype_observations`.

---

## 22. Direct and Derived Relationship Union View

Implementations may eventually expose a union view:

```text
genotype_variant_relationships
```

This union view may combine:

```text
direct_genotype_variant_relationships

derived_genotype_variant_relationships
```

The union view is permitted only if it preserves:

```text
relationship_origin

relationship_state

genotype_observation_id

genotype_variant_relationship_id

source_record_hash

relationship_derivation_policy_id when derived

producer relationship status when producer-declared
```

The union view must not erase the distinction between:

```text
producer_declared direct_source_biallelic

and

vdb_derived resolved_from_multiallelic_record
```

---

## 23. Non-Goals

This schema does not define:

```text
physical SQL DDL

SQLite indexes

ORM class names

exact file names emitted by code

final TEP-VDB relationship surface schema

RDGP consumption schema

clinical interpretation schema

projection surface schemas for GIRS / PGERS / EVRS / OACS / CUES / RMCS
```

This schema also does not replace the VDB multiallelic brokerage policy.

---

## 24. Success Criteria

This schema is successful when VDB can represent:

```text
1. every producer genotype observation as immutable source evidence

2. every genotype artifact and context artifact with inventory, lineage, and
   validation status

3. execution provenance as context, not biological evidence

4. every genotype observation's relationship input routing state

5. every direct producer relationship as producer-declared

6. every VDB-derived relationship as derived topology

7. every brokerage-required genotype observation with an auditable brokerage
   receipt or explicit not-evaluated state

8. genotype declaration sets suitable for Phase 4.3 Assertion Records

9. genotype topology members and relationship basis suitable for Phase 4.4
   Evidence Topology

10. direct and derived relationships without semantic collapse

11. unresolved, ambiguous, spanning-deletion, symbolic, missing-identity, and
    not-evaluated states without treating them as absence

12. legacy variant-only TEP-VAP packages without inferred genotype

13. genotype-not-applicable producer packages using the coherent classification:

    ```text
    genotype_not_applicable_to_producer_type

    genotype_capability_not_applicable

    genotype_maturity_not_applicable
    ```

    without legacy misclassification or synthesized genotype evidence

14. legacy genotype-applicable TEP-VAP packages using
    `genotype_capability_unavailable_legacy` and `genotype_discovered` without
    implying that genotype observations exist

15. mixed-producer package classifications that preserve distinct evidence
    grammars for TEP-VAP and TEP-GSC

16. completed package classification without conflating classification status
    with genotype evidence maturity
```

The schema fails if it permits a VDB-derived relationship to masquerade as a
producer genotype observation.

---

## 25. Relationship to Validation, Contract, and Plan

The validation document should define how to prove that each schema surface is
complete, coherent, and non-collapsing.

The contract should define what downstream systems can rely on after VDB
successfully populates these schema surfaces.

The implementation plan should define the sequence for building these surfaces
in code.

---

## 26. Final Doctrine

The genotype evidence schema is layered:

```text
source_genotype_package_classifications
    package-level applicability, capability, and maturity classification

source_genotype_observations
    immutable producer truth

genotype_relationship_input_index
    routing and brokerage eligibility

direct_genotype_variant_relationships
    producer-declared direct links

derived_genotype_variant_relationships
    VDB-derived topology links

genotype_brokerage_receipts
    proof of relationship evaluation

genotype_declaration_sets
    Phase 4.3 substrate

genotype_topology_members / genotype_topology_relationship_basis
    Phase 4.4 substrate
```

The schema must preserve source truth, expose brokerage state, and prevent
derived topology from being confused with producer evidence.

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.
```

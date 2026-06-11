# VDB Tri-Layer Discovery Engine Architecture

## Purpose

This document defines the design philosophy and architecture for a tri-layer discovery engine within the Variant Database (VDB).

The discovery engine is intended to support deterministic, auditable, and schema-governed ingestion of heterogeneous biological evidence artifacts from:

* VAP
* GSC
* future RSP outputs
* external metadata resources
* BioProject / BioSample / SRA metadata
* annotation resources such as VEP, ClinVar, or related structured exports

The central goal is to prevent VDB ingestion from devolving into a large collection of brittle one-off adapters.

Instead, VDB should ingest evidence through a governed process:

```text
discover → profile → map → validate → ingest
```

The discovery engine functions as a control-plane layer for determining what an artifact contains, how it relates to known ecosystem contracts, and whether it can safely enter VDB.

---

# Core Concept

A human reviewing an unfamiliar table often performs a sequence of reasoning steps:

1. inspect the file name and source
2. inspect the column headers
3. inspect several example rows
4. identify obvious semantic fields
5. count unique values in categorical columns
6. distinguish missing values from true zeros
7. infer whether fields represent identifiers, annotations, metadata, or evidence states
8. compare the table against expected schemas
9. decide whether the file is valid, incomplete, novel, or incompatible

The VDB discovery engine formalizes this reasoning into deterministic software.

It does not replace explicit contracts.

Instead, it acts as a second validation and characterization layer that checks whether incoming artifacts conform to known contracts or require governance review.

---

# Architectural Position

VDB is the authoritative evidence nexus for the broader repository ecosystem.

Its responsibilities include:

* evidence persistence
* metadata normalization
* gene namespace normalization
* source artifact tracking
* cross-run query support
* downstream RDGP evidence generation
* GSC overlay attachment
* future RSP functional evidence integration

The discovery engine sits at the boundary between incoming artifacts and normalized VDB tables.

```text
VAP / GSC / RSP / external metadata
        ↓
artifact discovery
        ↓
governance mapping
        ↓
deterministic ingestion
        ↓
normalized VDB evidence store
        ↓
query surfaces / RDGP / downstream systems
```

---

# Design Principle

The discovery engine must never silently mutate, collapse, or reinterpret evidence.

Discovery may observe.

Discovery may profile.

Discovery may propose mappings.

Discovery may flag risks.

Discovery must not silently rewrite biological meaning.

All transformations must be explicit, logged, and reproducible.

---

# Three-Layer Architecture

The VDB discovery engine is organized into three layers:

1. Artifact Discovery Layer
2. Governance Mapping Layer
3. Deterministic Ingestion Layer

Each layer has a distinct role.

---

# Layer 1 — Artifact Discovery Layer

## Purpose

The discovery layer answers:

```text
What is this artifact?
```

It performs deterministic profiling of incoming files before any database ingestion occurs.

This layer should work for both internal ecosystem outputs and external metadata sources.

Examples include:

* VAP stage outputs
* VAP run metadata
* VAP stage summaries
* GSC consensus gene evidence tables
* RSP DEG tables
* BioSample metadata tables
* BioProject/SRA run manifests
* ClinVar-derived exports
* VEP-derived annotation tables

---

## Discovery Tasks

The discovery layer should inspect:

* file path
* file name
* source repository
* declared artifact type, if available
* run_id, if available
* sample_id, if available
* stage identity, if available
* delimiter
* column names
* row count
* column count
* data types
* missing-value patterns
* categorical value domains
* numeric ranges
* identifier-like columns
* gene-like columns
* variant-like columns
* metadata-like columns
* provenance-like columns
* duplicated rows
* duplicated key candidates
* file hash
* file size
* modification timestamp

---

## Column-Level Profiling

For each column, the discovery engine should generate a structured profile.

Suggested fields:

| Field                   | Meaning                                                         |
| ----------------------- | --------------------------------------------------------------- |
| column_name             | original column name                                            |
| inferred_type           | string, integer, float, boolean, categorical, identifier, mixed |
| null_count              | number of missing values                                        |
| null_fraction           | fraction of missing values                                      |
| unique_count            | number of unique values                                         |
| example_values          | bounded list of representative values                           |
| value_domain            | full domain for low-cardinality fields                          |
| min_value               | numeric minimum, if applicable                                  |
| max_value               | numeric maximum, if applicable                                  |
| candidate_semantic_role | inferred semantic role                                          |
| confidence              | mapping confidence                                              |
| warnings                | possible ambiguity or incompatibility                           |

---

## Value-Domain Profiling

Value-domain profiling is especially important for biological interpretation fields.

For example:

```text
column_name = clinvar_significance
unique_values = Benign, Likely_benign, VUS, Likely_pathogenic, Pathogenic, Conflicting_interpretations
```

This permits VDB to recognize that the column likely represents a clinical-significance classification domain.

Similarly:

```text
column_name = priority_tier
unique_values = Tier_1, Tier_2, Tier_3
```

suggests prioritization-state semantics.

The discovery engine should therefore generate value-count summaries similar to the exploratory pivot-table behavior a human analyst would perform manually.

---

## Discovery Outputs

The discovery layer should emit auditable sidecar artifacts such as:

```text
artifact_discovery_report.json
column_profile.tsv
value_domain_summary.tsv
artifact_fingerprint.json
discovery_warnings.tsv
```

These outputs should be preserved for validation and debugging.

---

# Layer 2 — Governance Mapping Layer

## Purpose

The governance mapping layer answers:

```text
What does this artifact mean within the VDB ecosystem?
```

This layer compares discovered artifact structure against known contracts, schemas, and interface specifications.

It determines whether the artifact:

* conforms to an existing contract
* partially conforms to a known contract
* introduces a new schema version
* contains unexpected columns
* lacks required fields
* contains unexpected value domains
* requires manual governance review
* should be rejected

---

## Relationship to VAP Contracts

VAP remains authoritative for the meaning of its outputs.

Therefore:

* VAP should define output contracts
* VAP should define stage semantics
* VAP should define expected columns and allowed values
* VAP should define null semantics where possible
* VAP should define stage-specific artifact identities

VDB should not reverse-engineer VAP biology from raw columns.

Instead, VDB discovery should recapitulate and validate VAP contracts.

This makes VDB a second-layer validator.

The relationship is:

```text
VAP output contract = source-of-truth semantic declaration
VDB discovery engine = independent compliance and ingestion validation
```

---

## Relationship to VDB Ingestion Contracts

VDB is authoritative for ingestion behavior.

Therefore, VDB should define:

* accepted artifact classes
* required fields for ingestion
* canonical table destinations
* namespace normalization rules
* metadata normalization rules
* allowed null-state representations
* artifact lineage requirements
* ingestion rejection rules
* provenance capture requirements

Together, VAP and VDB form a dual-sided interface:

```text
VAP promises what it emits.
VDB verifies and governs what it accepts.
```

---

# Contract Matching

The governance layer should compare incoming artifacts against known schema specifications.

Possible contract match outcomes:

| Outcome              | Meaning                                                  |
| -------------------- | -------------------------------------------------------- |
| exact_match          | artifact matches expected schema and value domains       |
| compatible_extension | artifact has expected fields plus tolerated extra fields |
| partial_match        | artifact resembles known schema but is missing fields    |
| schema_drift         | artifact differs from known schema version               |
| unknown_artifact     | artifact does not match known artifact class             |
| rejected             | artifact violates required contract                      |

This allows controlled evolution without silent breakage.

---

# Allowed Value Validation

Column values should be checked against declared allowed domains where available.

Examples:

| Column                | Example Expected Domain                                                |
| --------------------- | ---------------------------------------------------------------------- |
| clinical_significance | Benign, Likely_benign, VUS, Likely_pathogenic, Pathogenic, Conflicting |
| assay_type            | WES, WGS, RNAseq, unknown                                              |
| quality_flag          | PASS, FAIL, LOW_QUALITY, unknown                                       |
| gene_mapping_status   | resolved, unresolved, ambiguous                                        |
| priority_tier         | Tier_1, Tier_2, Tier_3, unassigned                                     |
| validation_required   | true, false, unknown                                                   |

Unexpected values should not be silently coerced.

They should be reported as governance warnings or ingestion-blocking errors depending on severity.

---

# Null Semantics

The governance layer must distinguish:

```text
missing
```

from:

```text
zero
```

and from:

```text
not applicable
```

This is essential for downstream biological reasoning.

Examples:

| State     | Meaning                     |
| --------- | --------------------------- |
| NULL      | unavailable or not provided |
| 0         | measured value of zero      |
| NA        | not applicable              |
| unknown   | explicitly unresolved       |
| ambiguous | multiple possible mappings  |

VDB should preserve these distinctions wherever possible.

---

# Metadata Mapping

The governance layer should also map metadata fields.

For BioProject/BioSample/SRA-derived inputs, this may include:

* BioProject accession
* BioSample accession
* SRA accession
* organism
* sex
* tissue
* disease
* phenotype
* sequencing strategy
* assay type
* platform
* library layout
* run accession
* experiment accession
* sample title
* source name
* collection attributes

Because public metadata are often inconsistent, VDB should preserve both:

* canonical normalized metadata fields
* raw source metadata key/value pairs

This prevents information loss.

---

# Layer 3 — Deterministic Ingestion Layer

## Purpose

The deterministic ingestion layer answers:

```text
How does this validated artifact enter VDB?
```

Only artifacts that pass governance mapping should enter normalized VDB tables.

Ingestion must preserve:

* run identity
* source artifact identity
* source repository
* artifact hash
* schema version
* mapping version
* ingestion timestamp
* stage identity
* provenance lineage
* raw-to-normalized field mapping
* rejected-row reports, if applicable

---

# Ingestion Modes

VDB may support multiple ingestion modes.

| Mode           | Meaning                                                            |
| -------------- | ------------------------------------------------------------------ |
| strict         | reject artifacts that deviate from expected contract               |
| permissive     | ingest recognized fields and preserve unexpected fields separately |
| discovery_only | profile artifact without ingesting                                 |
| dry_run        | simulate ingestion and emit validation report                      |
| reingest       | replay ingestion with existing manifest and mapping version        |

For v1, strict and discovery_only modes may be sufficient.

---

# VAP Run-Package Ingestion

A VAP run directory should be treated as an atomic source artifact package.

A run package may include:

* processed stage outputs
* metadata sidecars
* metrics
* runtime profiles
* stage summaries
* figure source tables
* logs
* validation outputs
* artifact manifests

VDB should ingest VAP runs through a manifest-mediated process.

The manifest should define:

* run_id
* sample_id
* assay_type
* source_pipeline
* source_repository
* artifact_path
* artifact_type
* stage
* required status
* expected_schema
* destination_table
* schema_version

This prevents VDB from guessing which files matter.

---

# Example VAP Run-Package Manifest

```text
run_id	sample_id	assay_type	stage	artifact_type	artifact_path	required	destination_table	schema_version
run_2026_05_27_172531	ERR10619300	WES	stage08	vdb_ready_variants	results/run_2026_05_27_172531/processed/stage_08_vdb_ready_variants.tsv	true	stage08_vdb_ready_variants	v1
run_2026_05_27_172531	ERR10619300	WES	stage08	rdgp_gene_seed	results/run_2026_05_27_172531/processed/stage_08_rdgp_gene_evidence_seed.tsv	true	stage08_rdgp_gene_evidence_seed	v1
run_2026_05_27_172531	ERR10619300	WES	stage11	prioritized_variants	results/run_2026_05_27_172531/processed/stage_11_prioritized_variants.tsv	true	stage11_prioritized_variants	v1
run_2026_05_27_172531	ERR10619300	WES	stage12	validation_candidates	results/run_2026_05_27_172531/processed/stage_12_validation_candidates.tsv	true	stage12_validation_candidates	v1
```

---

# Recommended VDB Tables Supporting Discovery

The discovery engine should likely preserve its own metadata in dedicated tables.

Suggested tables:

```text
source_artifacts
artifact_discovery_reports
artifact_column_profiles
artifact_value_domains
artifact_schema_matches
artifact_mapping_decisions
artifact_ingestion_events
artifact_ingestion_warnings
artifact_ingestion_errors
```

These tables make discovery itself queryable.

That is important because VDB should be able to answer:

```text
Which artifacts matched their expected contracts?
Which columns drifted between VAP versions?
Which value domains changed?
Which artifacts were ingested under which schema versions?
Which fields were preserved but not normalized?
```

---

# Contract Compliance as Hotel Check-In

The discovery engine functions like a controlled check-in process.

Incoming artifacts are not allowed directly into the database.

They must present:

* identity
* source
* expected role
* schema
* provenance
* allowed values
* metadata context

The engine verifies:

* passport: artifact identity
* reservation: expected manifest entry
* room type: destination table
* credentials: schema and value-domain compliance
* baggage: raw metadata and provenance sidecars

Only then is the artifact admitted into VDB.

This protects VDB from silent contamination.

---

# Internal and External Input Symmetry

A major design principle is that VDB should apply the same discovery process to both:

* internal ecosystem artifacts
* external public metadata or annotation resources

Internal examples:

* VAP stage outputs
* GSC consensus outputs
* RSP functional evidence outputs

External examples:

* BioSample metadata
* BioProject metadata
* SRA run metadata
* ClinVar-derived tables
* HGNC reference tables
* VEP-derived annotations

This symmetry prevents the system from becoming fragmented into isolated adapter logic.

The same discovery engine should profile, summarize, and validate all incoming structured evidence.

---

# Adapter Strategy

The discovery engine does not eliminate all adapters.

Some source-specific adapters will still be necessary.

However, adapters should be thin.

Preferred architecture:

```text
thin adapter → standardized artifact profile → governance mapping → deterministic ingestion
```

Adapters should perform only minimal source-specific access or extraction.

They should not contain hidden biological normalization logic.

All semantic normalization should occur in the governance mapping and deterministic ingestion layers.

---

# Validation Strategy

VDB discovery validation should include:

* known VAP artifact recognition
* schema drift detection
* unexpected column detection
* missing required column detection
* unexpected categorical value detection
* null vs zero preservation
* deterministic report generation
* repeated discovery reproducibility
* artifact hash preservation
* dry-run ingestion validation
* rejected artifact reporting

Validation should prove that identical artifacts produce identical discovery reports and ingestion decisions.

---

# Example Validation Cases

## VAP Stage 08 Artifact

Input:

```text
stage_08_vdb_ready_variants.tsv
```

Expected:

* artifact recognized as VAP Stage 08 VDB-ready variant substrate
* required variant identity columns detected
* gene identity fields detected
* clinical significance fields detected
* value domains profiled
* destination table identified
* ingestion approved if schema matches contract

---

## VAP Stage 12 Artifact

Input:

```text
stage_12_validation_candidates.tsv
```

Expected:

* artifact recognized as validation candidate substrate
* validation-related columns detected
* priority and QC domains profiled
* validation status values checked
* destination table identified
* ingestion approved if schema matches contract

---

## BioSample Metadata Artifact

Input:

```text
biosample_metadata.tsv
```

Expected:

* artifact recognized as external metadata source
* source accession fields detected
* available attributes profiled
* raw metadata key/value pairs preserved
* canonical metadata fields mapped where possible
* ambiguous fields flagged rather than discarded

---

# Failure Modes

The discovery engine should explicitly guard against:

* silent schema drift
* silent value-domain drift
* column-name collision
* alias collapse
* null/zero confusion
* undocumented metadata loss
* source artifact ambiguity
* duplicate ingestion
* stage misclassification
* adapter-specific hidden transformations

These are infrastructure threats, not minor implementation details.

---

# v1 Scope Recommendation

For VDB v1, the discovery engine should remain focused and achievable.

Recommended v1 scope:

* TSV artifact profiling
* VAP run-package manifest ingestion
* column profile generation
* value-domain summary generation
* schema matching against VAP artifact contracts
* dry-run mode
* strict ingestion mode
* source artifact tracking
* ingestion event logging
* basic BioProject/SRA metadata profiling
* deterministic output validation

Defer to post-v1:

* automatic ontology mapping
* complex semantic inference
* machine-learning-based schema matching
* web-scale metadata ingestion
* fully generalized external source adapters
* dynamic schema migration

---

# Summary

The VDB tri-layer discovery engine is a deterministic control-plane system for governed evidence ingestion.

It formalizes the human process of inspecting, profiling, interpreting, and validating incoming tables before allowing them into the database.

Its three layers are:

1. artifact discovery
2. governance mapping
3. deterministic ingestion

This architecture allows VDB to serve as the authoritative evidence nexus for the repository ecosystem while preserving auditability, provenance continuity, namespace integrity, and downstream interoperability.

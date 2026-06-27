# Assertion Record Schema

## Purpose

This document defines the semantic field structure for VDB Assertion Records.

This is a schema document. It defines object shape, field names, cardinality, and representative examples. Semantic obligations and preservation requirements are defined separately in:

```text
docs/implementation/specifications/assertion_record_spec.md
```

The conceptual design model is defined in:

```text
docs/design/assertion_record_and_projection_model.md
```

---

# AssertionRecord

An `AssertionRecord` represents one preserved producer assertion.

```text
AssertionRecord
├── assertion_id
├── producer_identity
├── assertion_type
├── relationship
├── participants[]
├── evidence_basis[]
├── context
├── provenance
├── epistemic_status
├── confidence_or_support[]
├── independence_group[]
├── temporal_scope
├── derivation
└── payload
```

---

# Required Fields

## assertion_id

Stable identifier for the assertion record.

```text
Type: string
Cardinality: required, exactly one
Example: assertion_4fcc9c71...
```

---

## producer_identity

Identity of the producer that emitted the assertion.

```text
Type: object
Cardinality: required, exactly one
```

Recommended structure:

```text
producer_family: string
producer_repository: string | null
producer_version: string | null
run_id: string | null
release_id: string | null
package_id: string | null
tep_id: string | null
```

Example:

```yaml
producer_family: GSC
producer_repository: gene_set_consensus
producer_version: null
run_id: run_2026_06_23_015533
release_id: mitochondrial_semantic_gtr_experimental_v0.1
package_id: mitochondrial_semantic_gtr_experimental
tep_id: gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1
```

---

## assertion_type

High-level type of assertion.

```text
Type: string
Cardinality: required, exactly one
```

Initial examples:

```text
variant_observation
variant_annotation
semantic_prior
source_contribution
differential_expression
gene_prioritization
validation_result
```

---

## relationship

Producer-asserted relationship.

```text
Type: string
Cardinality: required, exactly one
```

Initial examples:

```text
contains
annotates
supports
prioritizes
differentially_expressed
contributes_to
validates
observes
```

---

## participants

Scientific entities participating in the assertion.

```text
Type: array[Participant]
Cardinality: required, one or more
```

Participant structure:

```text
participant_role: string
participant_kind: string
source_namespace: string
source_value: string
source_label: string | null
source_record_ref: string | null
```

Example:

```yaml
- participant_role: gene
  participant_kind: gene
  source_namespace: gsc_ensembl_gene_id
  source_value: ENSG00000140521
  source_label: POLG
  source_record_ref: row:42
```

---

## evidence_basis

Evidence source supporting the assertion.

```text
Type: array[EvidenceBasis]
Cardinality: required, one or more
```

EvidenceBasis structure:

```text
basis_type: string
basis_ref: string
artifact_id: string | null
artifact_path: string | null
source_record_ref: string | null
description: string | null
```

Initial `basis_type` examples:

```text
artifact
row
record
variant_call
annotation_record
semantic_score
source_contribution
literature_record
validation_output
```

Example:

```yaml
- basis_type: row
  basis_ref: source_contributions.tsv::row:42
  artifact_id: artifact_a1b2c3
  artifact_path: tables/mitochondrial_semantic_gtr_experimental/source_contributions.tsv
  source_record_ref: row:42
  description: GSC source contribution row
```

---

## context

Biological, technical, phenotypic, or experimental context.

```text
Type: object
Cardinality: required, exactly one
```

Recommended flexible structure:

```text
sample_id: string | null
phenotype: string | null
condition: string | null
contrast: string | null
tissue: string | null
run_id: string | null
pipeline_stage: string | null
reference_build: string | null
resource_release: string | null
additional_context: object
```

Example:

```yaml
sample_id: null
phenotype: mitochondrial_disease
condition: null
contrast: null
tissue: null
run_id: run_2026_06_23_015533
pipeline_stage: consensus_generation
reference_build: null
resource_release: mitochondrial_semantic_gtr_experimental_v0.1
additional_context: {}
```

---

## provenance

Chain-of-custody information.

```text
Type: object
Cardinality: required, exactly one
```

Recommended structure:

```text
source_repository: string | null
tep_id: string | null
package_id: string | null
artifact_id: string | null
artifact_path: string | null
artifact_sha256: string | null
source_record_ref: string | null
software_version: string | null
resource_version: string | null
created_at: string | null
```

Example:

```yaml
source_repository: gene_set_consensus
tep_id: gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1
package_id: mitochondrial_semantic_gtr_experimental
artifact_id: source_contributions
artifact_path: tables/mitochondrial_semantic_gtr_experimental/source_contributions.tsv
artifact_sha256: null
source_record_ref: row:42
software_version: null
resource_version: mitochondrial_semantic_gtr_experimental_v0.1
created_at: null
```

---

## epistemic_status

Class of knowledge represented by the assertion.

```text
Type: string
Cardinality: required, exactly one
```

Initial controlled vocabulary:

```text
observed
annotated
asserted
derived
inferred
brokered
projected
hypothesized
```

Example:

```yaml
epistemic_status: asserted
```

---

# Optional Fields

## confidence_or_support

Producer-provided score, confidence, support, or quality information.

```text
Type: array[ConfidenceOrSupport]
Cardinality: optional, zero or more
```

ConfidenceOrSupport structure:

```text
support_type: string
support_value: string | number | boolean
support_unit: string | null
method: string | null
description: string | null
```

Example:

```yaml
- support_type: semantic_score
  support_value: 0.94
  support_unit: null
  method: GSC semantic scoring
  description: phenotype-scoped semantic prior score
```

---

## independence_group

Evidence-origin grouping used to distinguish repeated records from independent evidence origins.

```text
Type: array[IndependenceGroup]
Cardinality: optional, zero or more
```

IndependenceGroup structure:

```text
group_type: string
group_id: string
description: string | null
```

Initial `group_type` examples:

```text
publication
database_release
pipeline_run
source_adapter
patient
cohort
annotation_resource
```

Example:

```yaml
- group_type: pipeline_run
  group_id: run_2026_06_23_015533
  description: GSC mitochondrial semantic consensus run
```

---

## temporal_scope

Time or version window associated with the assertion.

```text
Type: object
Cardinality: optional, zero or one
```

Recommended structure:

```text
observed_at: string | null
asserted_at: string | null
valid_from: string | null
valid_to: string | null
resource_release_date: string | null
publication_date: string | null
```

Example:

```yaml
observed_at: null
asserted_at: null
valid_from: null
valid_to: null
resource_release_date: null
publication_date: null
```

---

## derivation

Process by which the assertion record or derived record came into existence.

```text
Type: string
Cardinality: optional for direct producer assertions; required for derived records
```

Initial controlled vocabulary:

```text
direct_producer_assertion
artifact_level_registration
row_level_projection
namespace_brokerage
semantic_projection
topological_projection
statistical_projection
manual_review
```

Example:

```yaml
derivation: direct_producer_assertion
```

---

## payload

Producer-specific extension payload.

```text
Type: object
Cardinality: optional, zero or one
```

The payload may preserve additional producer-specific information.

Required semantic fields must not exist only inside `payload`.

Example:

```yaml
payload:
  source_name: MitoCarta
  source_weight: 1.0
  scoring_rule_id: mitocarta_contextual_biology
```

---

# Example: VAP AssertionRecord

```yaml
assertion_id: assertion_vap_example_001
producer_identity:
  producer_family: VAP
  producer_repository: variant_annotation_pipeline
  producer_version: null
  run_id: run_2026_06_03_010030
  release_id: null
  package_id: vap_tep_HG002_run_2026_06_03_010030
  tep_id: null

assertion_type: variant_observation
relationship: contains

participants:
  - participant_role: sample
    participant_kind: sample
    source_namespace: vap_sample_id
    source_value: HG002
    source_label: HG002
    source_record_ref: null
  - participant_role: variant
    participant_kind: variant
    source_namespace: vap_variant_id
    source_value: 15:89333596:T:TTGC
    source_label: 15:89333596:T:TTGC
    source_record_ref: row:1

evidence_basis:
  - basis_type: row
    basis_ref: annotated_variants.tsv::row:1
    artifact_id: null
    artifact_path: entities/observation/HG002_run_2026_06_03_010030.annotated_variants.tsv
    source_record_ref: row:1
    description: VAP variant observation row

context:
  sample_id: HG002
  phenotype: null
  condition: null
  contrast: null
  tissue: null
  run_id: run_2026_06_03_010030
  pipeline_stage: observation
  reference_build: null
  resource_release: null
  additional_context: {}

provenance:
  source_repository: variant_annotation_pipeline
  tep_id: null
  package_id: vap_tep_HG002_run_2026_06_03_010030
  artifact_id: null
  artifact_path: entities/observation/HG002_run_2026_06_03_010030.annotated_variants.tsv
  artifact_sha256: null
  source_record_ref: row:1
  software_version: null
  resource_version: null
  created_at: null

epistemic_status: observed
confidence_or_support: []
independence_group:
  - group_type: pipeline_run
    group_id: run_2026_06_03_010030
    description: VAP HG002 run
temporal_scope: null
derivation: direct_producer_assertion
payload: {}
```

---

# Example: GSC AssertionRecord

```yaml
assertion_id: assertion_gsc_example_001
producer_identity:
  producer_family: GSC
  producer_repository: gene_set_consensus
  producer_version: null
  run_id: run_2026_06_23_015533
  release_id: mitochondrial_semantic_gtr_experimental_v0.1
  package_id: mitochondrial_semantic_gtr_experimental
  tep_id: gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1

assertion_type: semantic_prior
relationship: supports

participants:
  - participant_role: phenotype
    participant_kind: phenotype
    source_namespace: gsc_phenotype
    source_value: mitochondrial_disease
    source_label: mitochondrial_disease
    source_record_ref: row:1
  - participant_role: gene
    participant_kind: gene
    source_namespace: gsc_ensembl_gene_id
    source_value: ENSG00000140521
    source_label: POLG
    source_record_ref: row:1

evidence_basis:
  - basis_type: row
    basis_ref: consensus_gene_set.tsv::row:1
    artifact_id: consensus_gene_set
    artifact_path: tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv
    source_record_ref: row:1
    description: GSC phenotype-scoped semantic prior row

context:
  sample_id: null
  phenotype: mitochondrial_disease
  condition: null
  contrast: null
  tissue: null
  run_id: run_2026_06_23_015533
  pipeline_stage: consensus_gene_set
  reference_build: null
  resource_release: mitochondrial_semantic_gtr_experimental_v0.1
  additional_context: {}

provenance:
  source_repository: gene_set_consensus
  tep_id: gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1
  package_id: mitochondrial_semantic_gtr_experimental
  artifact_id: consensus_gene_set
  artifact_path: tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv
  artifact_sha256: null
  source_record_ref: row:1
  software_version: null
  resource_version: mitochondrial_semantic_gtr_experimental_v0.1
  created_at: null

epistemic_status: asserted
confidence_or_support:
  - support_type: semantic_score
    support_value: 0.94
    support_unit: null
    method: GSC semantic scoring
    description: phenotype-scoped semantic prior score

independence_group:
  - group_type: pipeline_run
    group_id: run_2026_06_23_015533
    description: GSC mitochondrial semantic consensus run

temporal_scope: null
derivation: direct_producer_assertion
payload: {}
```

---

# Schema Notes

This schema is intentionally semantic rather than storage-specific.

SQLite tables, JSON documents, RDF exports, property graphs, and future storage systems may represent this structure differently.

Any representation is valid only if it preserves the semantic fields required by the Assertion Record specification.

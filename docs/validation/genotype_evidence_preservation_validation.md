# Genotype Evidence Preservation Validation

**Status:** validation draft  
**Intended path:** `docs/validation/genotype_evidence_preservation_validation.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** Validation gates and receipt expectations for genotype-aware VDB ingestion, preservation, brokerage, declaration, and topology preparation  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Design parent:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Specification parent:** `docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md`  
**Schema parent:** `docs/implementation/schemas/genotype_evidence_schema.md`  

---

## 1. Purpose

This document defines how VDB validates preservation of first-class genotype
evidence from genotype-capable TEP-VAP packages.

The architecture document defines what must remain true.

The design document defines how genotype evidence should move through VDB.

The specification defines required ingestion behavior.

The schema defines the logical representational surfaces.

This validation document defines how VDB proves that implementation satisfied
those requirements without source-truth loss, semantic collapse, or reasoning
overreach.

The central validation doctrine is:

```text
Genotype evidence validation succeeds only when VDB proves that producer
genotype observations remain losslessly preserved and that all VDB-created
relationship objects are traceable, policy-declared, non-interpretive, and
structurally distinguishable from producer evidence.
```

---

## 2. Scope

This document covers validation for:

```text
package genotype capability classification

genotype artifact-set completeness

execution provenance context registration

source genotype observation preservation

producer identity preservation

count reconciliation

relationship partitioning

direct relationship registration

complex relationship preservation

brokerage receipts

derived genotype-to-variant relationships

spanning-deletion conservative handling

genotype declaration sets

genotype topology substrates

anti-collapse and anti-overclaim constraints

legacy compatibility mode

mixed-corpus behavior
```

This document does not define:

```text
pytest function names

CLI commands

SQL queries

physical table names

exact receipt file paths

projection-surface validation

RDGP reasoning validation

clinical validity checks
```

Those details belong to implementation and test planning.

---

## 3. Validation Philosophy

Genotype evidence validation is not merely a code test.

It is an evidence-boundary audit.

The validation must prove that:

```text
producer genotype observations remain producer evidence

VDB-derived relationships remain derived topology

direct producer relationships remain distinguishable from VDB-derived
relationships

complex and unresolved states remain visible

execution provenance is registered as context

legacy genotype absence is not converted into inferred genotype

no VDB ingestion layer emits inheritance interpretation
```

Validation should emphasize traceability and non-collapse over convenience.

---

## 4. Validation Status Vocabulary

Validation receipts should use a controlled status vocabulary.

Recommended statuses:

```text
pass

pass_with_advisory

pass_with_legacy_limitation

pass_with_unresolved_brokerage

fail

quarantine

not_evaluated
```

### 4.1 `pass`

All required validation conditions are satisfied.

### 4.2 `pass_with_advisory`

Core preservation and trust requirements are satisfied, but expected governed
complexity exists.

Examples:

```text
complex multiallelic brokerage-required rows exist

spanning-deletion contexts are preserved conservatively

brokerage not yet evaluated by design stage
```

### 4.3 `pass_with_legacy_limitation`

A package is valid for variant-only legacy compatibility but has no first-class
genotype substrate.

No genotype inference is permitted.

### 4.4 `pass_with_unresolved_brokerage`

Source genotype observations are preserved, but one or more genotype-to-variant
relationships remain explicitly unresolved under available VDB policy.

Unresolved brokerage is not evidence loss.

### 4.5 `fail`

A required validation condition failed and trusted ingestion must not proceed.

### 4.6 `quarantine`

The package or row may be preserved for diagnostic inspection, but must not
enter trusted Assertion Records, Evidence Topology, projection surfaces, or
RDGP-facing exports.

### 4.7 `not_evaluated`

The validation gate was not evaluated.

This state must remain explicit.

---

## 4A. Genotype Maturity Validation Vocabulary

Genotype validation is maturity-tiered.

A package, corpus, or VDB build must not claim a higher genotype maturity state
than its validation receipts support.

Recommended maturity states are:

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

Validation must prove the prerequisite receipts for each claimed maturity state.

For example:

```text
genotype_preservation_validated
    requires source genotype observation preservation validation

genotype_direct_relationships_registered
    requires direct relationship registration validation

genotype_complex_relationships_preserved
    requires complex relationship preservation validation

genotype_brokerage_evaluated
    requires brokerage receipt validation and derived relationship validation

genotype_assertion_ready
    requires declaration-set validation

genotype_topology_ready
    requires topology substrate and topology basis validation

genotype_projection_ready
    requires later projection-surface validation outside this document
```

A build may pass lower-tier genotype validation without passing higher-tier
validation.

---

## 5. Failure Class Vocabulary

Validation receipts should record specific failure classes.

Recommended failure classes:

```text
missing_required_artifact

partial_genotype_artifact_set

checksum_mismatch

lineage_missing

schema_version_unsupported

row_count_mismatch

column_preservation_failure

identity_preservation_failure

source_vcf_identity_missing

source_header_identity_missing

source_record_identity_missing

direct_complex_partition_mismatch

complex_relationship_silent_promotion

producer_observation_split_detected

derived_relationship_origin_missing

relationship_traceability_missing

brokerage_receipt_missing

spanning_deletion_silent_resolution

inheritance_overclaim_detected

execution_provenance_misclassified

legacy_genotype_inference_detected

unexpected_genotype_for_producer_type

mixed_corpus_genotype_scope_error
```

Failure classes should be stable enough to support downstream review.

---

## 6. Package Classification Validation

Every ingested package must receive exactly one genotype capability state.

Allowed states:

```text
genotype_capability_available

genotype_capability_unavailable_legacy

genotype_capability_incomplete

genotype_capability_invalid

genotype_capability_unsupported_version
```

Validation must prove:

```text
one and only one state was assigned

state assignment follows specification rules

partial genotype artifact sets are not classified as legacy

unsupported versions are not silently coerced

invalid genotype-capable packages do not enter trusted genotype ingestion
```

Expected receipt family:

```text
genotype_package_classification_receipt
```

Required receipt fields should include:

```text
source_package_id
producer_type
genotype_capability_state
classification_basis
artifact_presence_summary
schema_version_summary
validation_status
failure_classes
```

---

## 7. Genotype Artifact-Set Validation

For genotype-capable TEP-VAP packages, validation must verify the canonical
genotype artifact set:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

Validation must prove:

```text
all three artifacts are present

all three artifacts are parseable

all three artifacts are registered in entity inventory or equivalent governance

all three artifacts are represented in lineage when required

artifact checksums are present where package metadata provides checksums

artifact schema versions are supported

genotype projection summary is coherent

source-header context is coherent

genotype_observations.tsv header is readable
```

For trusted modern genotype-capable TEP-VAP ingestion, canonical genotype
artifact checksum reconciliation is required.

Checksum absence or checksum non-reconciliation must produce failure or
quarantine unless the package is explicitly handled under a legacy,
compatibility, quarantine, or unsupported-version state.

A partial artifact set must fail or quarantine.

Expected receipt family:

```text
genotype_artifact_set_validation_receipt
```

---

## 8. Execution Provenance Context Validation

For packages that provide execution provenance at:

```text
entities/context/execution_provenance.json
```

validation must prove that VDB registers it as context.

For trusted modern genotype-capable TEP-VAP ingestion, this artifact is required.

For legacy, compatibility, quarantine, or unsupported-version paths, absence may
be represented explicitly.

It must not be registered as:

```text
variant evidence

genotype evidence

pathogenicity evidence

phenotype evidence

reasoning evidence
```

Validation must verify:

```text
artifact path captured

artifact checksum captured and reconciled for trusted modern genotype-capable
TEP-VAP ingestion

contract status captured when available

provenance completeness captured when available

toolchain context captured when available

annotation environment context captured when available

resource environment context captured when available

registered_as_context = true
```

Expected receipt family:

```text
execution_provenance_context_validation_receipt
```

Misclassifying execution provenance as biological evidence must fail validation.

---

## 9. Source Genotype Observation Preservation Validation

This gate validates the immutable producer-truth surface:

```text
source_genotype_observations
```

Validation must prove:

```text
producer row count equals VDB preserved row count

all producer-emitted columns are preserved

genotype_observation_id values are unchanged

genotype_observation_id values are unique within the package

source row order or source_record_ordinal remains recoverable

source row identity remains recoverable

raw source row hash or equivalent reconstructability proof exists

raw FORMAT/sample fields are preserved where emitted

GT / AD / DP / GQ / PL / FT fields are preserved where emitted

unknown FORMAT fields are preserved where emitted

projection advisory and warning codes are preserved
```

Validation must fail if VDB:

```text
drops genotype rows

drops producer columns

rewrites producer genotype_observation_id

silently rewrites raw FORMAT/sample values

fails to preserve row-level source traceability
```

Expected receipt family:

```text
source_genotype_observation_preservation_receipt
```

---

## 10. Identity Preservation Validation

Validation must prove that producer identity remains recoverable.

Required identity classes include:

```text
genotype_observation_id

sample_id

run_id

source VCF identity

source VCF header identity

source record identity

reference build

source coordinate identity

producer relationship state
```

Validation must verify preservation of emitted fields such as:

```text
source_vcf_path

source_vcf_sha256

source_vcf_header_hash

source_record_ordinal

source_line_number

source_record_hash

reference_build

chromosome

position

reference_allele

alternate_alleles_raw

called_allele_indices
```

VDB-owned identities may be added.

They must not replace producer identities.

Expected receipt family:

```text
genotype_identity_preservation_receipt
```

---

## 11. Count Reconciliation Validation

Validation must reconcile producer summary counts, observed source table counts,
and VDB-preserved counts.

Required reconciliations include:

```text
genotype_projection_summary genotype_observation_row_count
    ==
observed genotype_observations.tsv data rows
    ==
VDB source_genotype_observations rows
```

If source-record count is provided:

```text
source_record_count
    ==
genotype_observation_row_count
```

Relationship partition counts must reconcile:

```text
direct_relationship_count
+ complex_relationship_count
+ unresolved_relationship_count
+ not_applicable_relationship_count
    ==
genotype_observation_row_count
```

If producer summary omits a partition count, VDB may compute it from source
rows, but the receipt must distinguish:

```text
producer_summarized_count

VDB_computed_count
```

Expected receipt family:

```text
genotype_count_reconciliation_receipt
```

---

## 12. Relationship Partition Validation

Relationship partition validation verifies producer relationship states and VDB
routing.

Validation must prove:

```text
each genotype observation receives one relationship input class

direct rows are routed to direct registration

complex rows are routed to complex preservation / brokerage input

unresolved rows remain unresolved unless a governed policy evaluates them

not_applicable rows remain explicit

unrecognized statuses are preserved and not silently trusted
```

For direct rows, expected producer pattern is:

```text
variant_relationship_status = direct

relationship_resolution_target = none

variant_id populated
```

For complex rows, expected producer pattern may include:

```text
variant_relationship_status = complex

relationship_resolution_target = vdb_brokerage

variant_id blank or unavailable by design
```

A blank `variant_id` in a complex row must not be classified as genotype
evidence failure when the row is explicitly delegated to VDB brokerage.

Expected receipt family:

```text
relationship_partition_validation_receipt
```

---

## 13. Direct Relationship Registration Validation

For direct relationships, validation must prove:

```text
relationship_origin = producer_declared

relationship_state = direct_source_biallelic

genotype_observation_id preserved

variant_id preserved

variant_observation_id preserved when emitted

sample_id preserved

run_id preserved

source_record_hash preserved

producer relationship status preserved

producer relationship reason preserved when emitted

producer relationship resolution target preserved

traceability refs present
```

Validation must also prove that direct relationships do not emit:

```text
inheritance mode

carrier status

compound heterozygosity

de novo status

disease causality

diagnosis
```

Expected receipt family:

```text
direct_relationship_registration_receipt
```

---

## 14. Complex Relationship Preservation Validation

Complex relationship preservation validation verifies that complex rows remain
visible before brokerage.

Validation must prove:

```text
complex source genotype observations are preserved in source_genotype_observations

complex rows appear in genotype_relationship_input_index

complex rows are not dropped

complex rows are not silently promoted to direct

complex rows are not represented as missing genotype evidence

complex rows preserve relationship_reason

complex rows preserve relationship_resolution_target

complex rows preserve source ALT order

complex rows preserve called allele indices

complex rows preserve raw GT / AD / DP / GQ / PL / FORMAT evidence where emitted
```

Expected receipt family:

```text
complex_relationship_preservation_receipt
```

Validation must fail if complex rows disappear or become direct source-biallelic
relationships without explicit VDB-derived relationship records and brokerage
receipts.

---

## 15. Brokerage Receipt Validation

Every brokerage-required genotype observation must have either:

```text
a brokerage receipt
```

or:

```text
an explicit not_evaluated / policy_unavailable state
```

Validation must reconcile:

```text
brokerage input count
    ==
brokerage resolved count
+ brokerage ambiguous count
+ brokerage unresolved count
+ brokerage not_evaluated count
+ brokerage policy_unavailable count
```

Brokerage receipts must preserve:

```text
genotype_observation_id

source_record_hash

brokerage policy id

allele-index mapping policy id when applicable

variant normalization policy id when applicable

spanning-deletion policy id when applicable

brokerage outcome

derived relationship count

traceability refs
```

Expected receipt family:

```text
brokerage_receipt_validation_receipt
```

A brokerage-required row without a receipt or explicit not-evaluated state must
fail validation.

---

## 16. Derived Relationship Validation

Derived relationship validation applies to VDB-created genotype-to-variant
relationships.

Validation must prove:

```text
relationship_origin = vdb_derived

genotype_observation_id preserved

source_record_hash preserved

allele_index preserved where applicable

source_alt_allele preserved where applicable

relationship_derivation_policy_id present

normalization policy present when normalization participates

relationship_state present

ambiguity_state present

lossiness_state present

identity_registration_state present

traceability_state present

anti_overclaim_label present
```

For multiallelic-derived relationships, validation must prove:

```text
relationship_state != direct_source_biallelic
```

Even a resolved multiallelic-derived relationship must remain distinguishable
from a direct producer relationship.

Validation must also prove:

```text
multiple VDB-derived relationships from one genotype_observation_id do not imply
multiple producer genotype observations
```

Expected receipt family:

```text
derived_relationship_validation_receipt
```

---

## 17. Spanning-Deletion Validation

Spanning-deletion validation applies to source records involving alleles such as:

```text
ALT = *
```

Unless a declared spanning-deletion resolution policy exists, validation must
prove that VDB uses conservative states such as:

```text
spanning_deletion_context_required

unresolved_spanning_deletion
```

Validation must fail if VDB silently treats `*` as an ordinary SNV or small-indel
alternate allele.

Validation must also prove that unresolved spanning-deletion state is not
treated as:

```text
missing genotype evidence

variant absence

evidence loss

direct biallelic linkage
```

Expected receipt family:

```text
spanning_deletion_validation_receipt
```

---

## 18. Declaration-Set Validation

Declaration-set validation applies to genotype declaration substrates used for
Phase 4.3 Assertion Records.

Validation must prove declaration sets are:

```text
source-traceable

non-interpretive

typed

basis-linked

policy-compatible when relevant
```

Allowed declaration meanings include:

```text
genotype_observation_preserved

genotype_observation_has_source_record

genotype_observation_has_raw_gt

genotype_observation_has_raw_ad_vector

genotype_observation_has_called_allele_index

genotype_observation_has_call_state

genotype_observation_has_missingness_state

genotype_observation_has_phase_context

genotype_observation_requires_vdb_brokerage

genotype_observation_has_complex_relationship
```

Forbidden declaration meanings include:

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

Expected receipt family:

```text
declaration_set_validation_receipt
```

---

## 19. Topology Substrate Validation

Topology substrate validation applies to genotype members and relationship basis
surfaces prepared for Phase 4.4 Evidence Topology.

Validation must prove genotype topology members and basis rows are:

```text
typed

traceable

policy-declared where derived

non-interpretive

basis-backed

source-preserving
```

Every genotype topology relationship must have a basis.

A topology edge without a source basis, policy basis, or receipt basis must fail
validation.

Genotype topology must not encode inheritance conclusions.

Expected receipt families:

```text
topology_substrate_validation_receipt

topology_relationship_basis_validation_receipt
```

---

## 20. Anti-Collapse Validation

Anti-collapse validation is a required global gate.

Validation must prove VDB does not collapse:

```text
genotype observation
    into variant identity

sample-specific variant observation
    into genotype observation

source genotype observation
    into allele-specific relationship

VDB-derived relationship
    into producer genotype observation

resolved_from_multiallelic_record
    into direct_source_biallelic

unresolved relationship
    into evidence absence

missing genotype artifact
    into homozygous reference

no-call
    into absence

execution provenance
    into biological evidence

genotype state
    into inheritance interpretation
```

Expected receipt family:

```text
anti_collapse_validation_receipt
```

Any detected collapse must fail trusted genotype validation.

---

## 21. Anti-Overclaim Validation

Anti-overclaim validation ensures VDB does not emit biological interpretations
during genotype ingestion, declaration, or topology preparation.

Validation must prove VDB does not emit:

```text
dominant-compatible

recessive-compatible

compound-heterozygous

de-novo

carrier status

biallelic disease model satisfied

pathogenic genotype

diagnostic genotype

disease causality

clinical diagnosis
```

Validation should verify that relevant relationship and topology rows carry
anti-overclaim labels such as:

```text
genotype_relationship_not_inheritance_interpretation

multiallelic_relationship_not_independent_producer_row

allele_depth_annotation_not_independent_ad_vector

resolved_relationship_not_direct_source_biallelic

genotype_state_not_disease_model

genotype_missingness_not_absence
```

Expected receipt family:

```text
anti_overclaim_validation_receipt
```

---

## 22. Legacy Compatibility Validation

Legacy compatibility validation applies to older TEP-VAP packages without
first-class genotype artifacts.

Validation must prove:

```text
legacy package has no genotype artifact set

package is otherwise valid for variant-only ingestion

genotype capability is labeled genotype_capability_unavailable_legacy

legacy compatibility mode is explicit

no synthetic genotype observations are created

no genotype relationship inputs are fabricated

no homozygous-reference or no-call state is inferred

no genotype opportunity or negative evidence is inferred
```

Recommended explicit states:

```text
variant_only_legacy_compatibility_mode

genotype_context_unavailable

genotype_not_emitted_by_source

genotype_projection_not_evaluated
```

Expected receipt family:

```text
legacy_compatibility_validation_receipt
```

---

## 23. Mixed-Corpus Validation

VDB corpora may contain multiple producer types.

In the near-term 5-TEP local corpus, genotype validation applies to:

```text
TEP-VAP packages:
    genotype evidence validation applies when genotype artifacts are present
```

For TEP-GSC packages, genotype validation should record:

```text
genotype_not_applicable_to_producer_type
```

and must not fail the corpus merely because GSC does not emit genotype evidence.

Mixed-corpus validation must prove:

```text
producer_type is recorded for every package

producer type is respected

TEP-VAP genotype packages are validated under genotype rules

TEP-GSC packages are not misclassified as failed genotype packages

corpus-level summaries distinguish genotype-applicable and genotype-not-applicable
packages
```

Expected receipt family:

```text
mixed_corpus_genotype_scope_receipt
```

---

## 24. Required Validation Receipt Families

The following receipt families are recommended for genotype-aware validation:

```text
genotype_package_classification_receipt

genotype_artifact_set_validation_receipt

execution_provenance_context_validation_receipt

source_genotype_observation_preservation_receipt

genotype_identity_preservation_receipt

genotype_count_reconciliation_receipt

relationship_partition_validation_receipt

direct_relationship_registration_receipt

complex_relationship_preservation_receipt

brokerage_receipt_validation_receipt

derived_relationship_validation_receipt

spanning_deletion_validation_receipt

declaration_set_validation_receipt

topology_substrate_validation_receipt

topology_relationship_basis_validation_receipt

anti_collapse_validation_receipt

anti_overclaim_validation_receipt

legacy_compatibility_validation_receipt

mixed_corpus_genotype_scope_receipt

genotype_evidence_validation_summary
```

Receipt physical formats may be JSON, TSV, Markdown, or another governed VDB
format.

This document defines receipt responsibilities, not physical file formats.

---

## 25. Required Summary Metrics

A genotype validation summary should include at minimum:

```text
source_package_id

producer_type

genotype_capability_state

genotype_maturity_state

genotype_artifact_set_status

execution_provenance_context_status

execution_provenance_required_for_trusted_modern_ingestion

source_genotype_observation_count

preserved_genotype_observation_count

producer_column_count

preserved_column_count

genotype_observation_id_unique_count

duplicate_genotype_observation_id_count

source_vcf_identity_status

source_header_identity_status

source_record_identity_status

sample_run_reference_coherence_status

direct_relationship_count

complex_relationship_count

unresolved_relationship_count

not_applicable_relationship_count

direct_relationship_registered_count

complex_relationship_preserved_count

brokerage_input_count

brokerage_resolved_count

brokerage_ambiguous_count

brokerage_unresolved_count

brokerage_not_evaluated_count

brokerage_policy_unavailable_count

derived_relationship_count

spanning_deletion_context_required_count

producer_observation_split_count

inheritance_assertion_count

execution_provenance_misclassified_count

validation_status

failure_classes
```

Expected invariant values:

```text
producer_observation_split_count = 0

inheritance_assertion_count = 0

execution_provenance_misclassified_count = 0
```

Any nonzero value for these three metrics must fail trusted genotype validation.

---

## 26. Non-Goals

This validation document does not define:

```text
unit test function names

pytest fixtures

CLI command syntax

SQL query text

final output file paths

final JSON schema for receipts

projection-surface validation

RDGP reasoning validation

clinical validity

diagnostic validity

pathogenicity correctness
```

This validation document also does not prove that VAP producer output is correct.

It validates VDB preservation and handling of the producer substrate.

---

## 27. Success Criteria

Genotype evidence preservation validation succeeds when VDB can prove:

```text
1. genotype-capable TEP-VAP packages are correctly classified

2. genotype artifact sets are complete and coherent

3. execution provenance is registered as context

4. every source genotype observation row is preserved

5. all producer columns are preserved

6. producer identities remain recoverable

7. row counts and relationship partition counts reconcile

8. direct relationships are registered as producer-declared direct links

9. complex relationships are preserved and routed to brokerage or explicit
   not-evaluated states

10. VDB-derived relationships remain topology and not producer evidence

11. brokerage receipts reconcile with brokerage-required inputs

12. spanning deletions are preserved conservatively unless a declared policy
    resolves them

13. declaration sets are non-interpretive

14. topology substrates are typed, traceable, basis-backed, and policy-declared

15. legacy packages remain usable without inferred genotype

16. mixed corpora distinguish genotype-applicable and genotype-not-applicable
    producer packages

17. no VDB layer emits inheritance conclusions during genotype ingestion,
    declaration, or topology preparation
```

---

## 28. Relationship to Contract, Plan, and Code

The contract document should state what downstream VDB consumers can rely on
after these validation gates pass.

The implementation plan should sequence code work so that each validation gate
can be implemented and exercised incrementally.

Code should not claim genotype-aware VDB status until the relevant validation
receipts exist and pass.

---

## 29. Final Doctrine

Genotype evidence validation is the certification bridge between producer truth
and VDB implementation.

A VDB build is not genotype-aware merely because it can read genotype columns.

It is genotype-aware only when it proves:

```text
producer genotype observations are preserved

producer identities remain recoverable

direct and derived relationships remain distinguishable

complex and unresolved states remain visible

brokerage is receipt-backed

declaration and topology layers remain non-interpretive

legacy genotype absence is not backfilled

RDGP reasoning is not performed inside VDB
```

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.
```

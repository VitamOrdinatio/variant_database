# Genotype Evidence Contract

**Status:** contract draft  
**Intended path:** `docs/contracts/genotype_evidence/genotype_evidence_contract.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, RDGP consumers, TEP-VDB emitters, future VDB maintainers  
**Scope:** Contractual guarantees and non-guarantees for VDB genotype evidence after validated ingestion, preservation, brokerage, declaration, and topology preparation  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Design parent:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Specification parent:** `docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md`  
**Schema parent:** `docs/implementation/schemas/genotype_evidence_schema.md`  
**Validation parent:** `docs/validation/genotype_evidence_preservation_validation.md`  

---

## 1. Purpose

This document defines what VDB guarantees to downstream consumers after
genotype-aware VDB ingestion and validation.

The architecture document defines what must remain true. The design document
defines how genotype evidence moves through VDB. The specification defines
required VDB behavior. The schema defines the logical VDB representation. The
validation document defines how VDB proves preservation and non-collapse.

This contract defines what downstream systems may rely on after validation
receipts pass.

The central contract doctrine is:

```text
VDB guarantees only the genotype evidence maturity tier whose required
validation receipts have passed.
```

VDB does not make a single undifferentiated `genotype-aware` guarantee.

A corpus may be genotype-preserving without being genotype-brokered. A corpus
may be genotype-brokered without being projection-ready. A corpus may be
topology-ready without containing RDGP inheritance reasoning.

---

## 2. Scope

This contract applies to VDB handling of genotype-capable TEP-VAP packages and
mixed VDB corpora that may contain genotype-applicable and genotype-not-applicable
producer packages.

This contract covers:

```text
genotype capability classification
genotype maturity state guarantees
modern TEP-VAP genotype artifact guarantees
execution provenance context guarantees
source genotype observation preservation guarantees
identity preservation guarantees
direct relationship guarantees
complex relationship preservation guarantees
brokerage guarantees
derived relationship guarantees
declaration-set guarantees
topology substrate guarantees
legacy compatibility guarantees
mixed-corpus guarantees
anti-collapse guarantees
anti-overclaim guarantees
validation receipt guarantees
consumer responsibilities
non-guarantees
contract violation conditions
```

This contract does not define:

```text
SQL tables
field ordering
physical file formats
CLI commands
pytest names
brokerage algorithms
projection surface schemas
RDGP reasoning logic
clinical interpretation logic
```

---

## 3. Authority Stack

This contract is subordinate to the established VDB genotype foundation:

```text
docs/architecture/genotype_first_class_vdb_evidence_model.md
docs/design/genotype_evidence_ingestion_and_brokerage_design.md
docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md
docs/implementation/schemas/genotype_evidence_schema.md
docs/validation/genotype_evidence_preservation_validation.md
```

If a future implementation conflicts with this contract, the implementation is
not contract-compliant.

If this contract conflicts with the architecture-level anti-collapse doctrine,
the architecture-level doctrine governs.

---

## 4. Contract Vocabulary

### 4.1 Guarantee

A guarantee is a VDB property that downstream consumers may rely on after the
required validation receipts pass.

### 4.2 Non-Guarantee

A non-guarantee is a property downstream consumers must not infer from VDB
genotype surfaces.

### 4.3 Consumer

A consumer is any downstream VDB phase, TEP-VDB emitter, RDGP process, analyst,
or future system that reads VDB genotype evidence surfaces.

### 4.4 Trusted Modern Genotype Ingestion

Trusted modern genotype ingestion applies to genotype-capable TEP-VAP packages
that satisfy the required artifact, version, checksum, lineage, validation,
execution provenance, and row-count reconciliation requirements.

### 4.5 Contract-Compliant Surface

A contract-compliant surface is a VDB output or persistence surface that has
passed the validation receipts required for its claimed maturity tier.

---

## 5. Genotype Capability Contract

VDB guarantees that every package receives exactly one genotype capability
state before genotype evidence is trusted.

Allowed genotype capability states are:

```text
genotype_capability_available
genotype_capability_unavailable_legacy
genotype_capability_incomplete
genotype_capability_invalid
genotype_capability_unsupported_version
```

### 5.1 Consumer Guarantee

Consumers may rely on:

```text
genotype-capable packages being explicitly classified before genotype evidence
is trusted
partial genotype artifact sets not being classified as legacy
unsupported genotype schema versions not being silently coerced
invalid genotype-capable packages not entering trusted genotype ingestion
```

### 5.2 Consumer Non-Guarantee

Consumers must not interpret:

```text
genotype_capability_unavailable_legacy
```

as evidence of:

```text
homozygous reference
variant absence
no-call
callability
opportunity evidence
negative disease evidence
inheritance-readiness support
```

Legacy unavailability means genotype was not emitted by the producer substrate.

It is not a biological observation.

---

## 6. Genotype Maturity Contract

VDB genotype guarantees are maturity-tiered.

Allowed genotype maturity states are:

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

VDB must not claim a higher genotype maturity state than its validation receipts
support.

### 6.1 `genotype_discovered`

VDB guarantees that genotype applicability and package-level genotype capability
state have been evaluated.

This state does not guarantee row-level genotype preservation.

### 6.2 `genotype_preservation_validated`

VDB guarantees that producer genotype observations have been preserved and
validated according to the genotype preservation validation gates.

For trusted modern genotype-capable TEP-VAP packages, this maturity state also
requires execution provenance context validation to have passed.

This state does not guarantee direct relationship registration, complex
brokerage, topology readiness, projection readiness, or RDGP reasoning.

### 6.3 `genotype_direct_relationships_registered`

VDB guarantees that eligible direct producer-declared genotype-to-variant
relationships have been registered as direct producer relationships.

This state does not guarantee that complex genotype relationships have been
brokered.

### 6.4 `genotype_complex_relationships_preserved`

VDB guarantees that complex genotype relationships are preserved as governed
source states and routed to brokerage input or explicit not-evaluated states.

This state does not guarantee that all complex relationships are resolved.

### 6.5 `genotype_brokerage_evaluated`

VDB guarantees that brokerage-required genotype observations have either
brokerage receipts or explicit not-evaluated / policy-unavailable states.

This state does not guarantee projection readiness or RDGP reasoning.

### 6.6 `genotype_assertion_ready`

VDB guarantees that genotype declaration sets and genotype-informed Assertion
Record substrates are available and non-interpretive.

This state does not guarantee topology readiness unless topology validation has
also passed.

### 6.7 `genotype_topology_ready`

VDB guarantees that genotype topology members and topology relationship basis
surfaces are typed, traceable, source-preserving, policy-declared where derived,
and non-interpretive.

This state does not guarantee projection readiness or RDGP reasoning.

### 6.8 `genotype_projection_ready`

VDB guarantees that later genotype-aware projection surfaces have passed their
own projection-specific validation.

Projection-readiness validation is outside the scope of the current
preservation-validation document and must be governed separately.

---

## 7. Modern TEP-VAP Input Contract

For trusted modern genotype-capable TEP-VAP ingestion, VDB guarantees that the
canonical genotype artifact set has been discovered, validated, and reconciled:

```text
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
```

VDB also guarantees that the required package governance artifacts have been
used before row-level genotype trust is established:

```text
entity_inventory.json
lineage_manifest.json
validation_report.md
```

### 7.1 Atomic Artifact-Set Guarantee

Consumers may rely on trusted modern genotype-capable packages having a complete
canonical genotype artifact set.

### 7.2 Partial Artifact Non-Guarantee

Consumers must not treat a partial genotype artifact set as trusted genotype
evidence.

A partial genotype artifact set is incomplete, invalid, quarantined, or otherwise
non-trusted until resolved under governed policy.

---

## 8. Execution Provenance Context Contract

For trusted modern genotype-capable TEP-VAP ingestion, VDB guarantees that:

```text
entities/context/execution_provenance.json
```

has been discovered and registered as execution provenance context.

VDB guarantees that execution provenance is registered as context, not as
biological evidence.

### 8.1 Consumer Guarantee

Consumers may rely on execution provenance context being available for trusted
modern genotype-capable ingestion.

Execution provenance may support:

```text
auditability
reproducibility
toolchain dependency tracking
reference-resource tracking
annotation environment comparison
method-currency reasoning in later governed surfaces
```

### 8.2 Consumer Non-Guarantee

Consumers must not treat execution provenance as:

```text
variant evidence
genotype evidence
pathogenicity evidence
phenotype evidence
reasoning evidence
diagnostic evidence
```

Execution provenance describes how evidence was generated.

It does not itself assert biological state.

---

## 9. Source Genotype Observation Preservation Contract

At maturity state:

```text
genotype_preservation_validated
```

VDB guarantees that producer genotype observations have been preserved as
immutable source evidence.

### 9.1 Preservation Guarantee

Consumers may rely on VDB-preserved genotype observations retaining:

```text
genotype_observation_id
genotype_observation_id_version when emitted
sample identity
run identity
source VCF identity
source VCF header identity
source record identity
reference build
coordinate and allele context
raw FORMAT and sample FORMAT evidence
GT / AD / DP / GQ / PL / FT fields where emitted
called allele indices
missingness and no-call state
relationship status
relationship reason
relationship resolution target
record parse and preservation state
projection advisory and warning state
```

### 9.2 Full-Row Reconstructability Guarantee

VDB guarantees that producer-emitted genotype columns are preserved either as
typed/indexed columns or as a raw source-row extension representation sufficient
to reconstruct the producer-emitted genotype observation row.

### 9.3 Raw Value Non-Replacement Guarantee

VDB-normalized convenience fields do not replace raw producer values.

Consumers must treat raw producer values and VDB-normalized convenience values
as distinct.

### 9.4 Non-Guarantee

Source genotype observation preservation does not guarantee:

```text
inheritance mode
carrier status
compound heterozygosity
de novo status
disease causality
diagnosis
variant pathogenicity
clinical validity
```

---

## 10. Identity Preservation Contract

VDB guarantees that producer identities remain recoverable after trusted
genotype preservation.

Producer identities include:

```text
genotype_observation_id
sample_id
run_id
source_vcf_path
source_vcf_sha256
source_vcf_header_hash
source_record_ordinal
source_line_number when emitted
source_record_hash
reference_build
chromosome
position
reference_allele
alternate_alleles_raw
called_allele_indices
```

VDB may add canonical or internal identities.

VDB-owned identities are additive.

They do not replace producer-owned identities.

---

## 11. Direct Relationship Contract

At maturity state:

```text
genotype_direct_relationships_registered
```

VDB guarantees that eligible direct genotype-to-variant relationships are
registered as producer-declared direct links.

### 11.1 Direct Relationship Guarantee

Consumers may rely on direct relationship rows preserving:

```text
relationship_origin = producer_declared
relationship_state = direct_source_biallelic
genotype_observation_id
variant_id
variant_observation_id when emitted
sample_id
run_id
source_record_hash
producer relationship status
producer relationship reason when emitted
producer relationship resolution target
traceability references
```

### 11.2 Direct Relationship Non-Guarantee

A direct genotype-to-variant relationship is not an inheritance assertion.

Consumers must not infer:

```text
dominant-compatible
recessive-compatible
compound-heterozygous
de-novo
carrier status
disease causality
diagnosis
```

from a direct VDB relationship.

---

## 12. Complex Relationship Contract

At maturity state:

```text
genotype_complex_relationships_preserved
```

VDB guarantees that complex genotype relationships are preserved as governed
source states.

### 12.1 Complex Relationship Guarantee

Consumers may rely on complex rows being:

```text
preserved in source_genotype_observations
represented in genotype_relationship_input_index
routed to brokerage input or explicit not-evaluated state
traceable to source record identity
traceable to raw GT / AD / DP / GQ / PL / FORMAT fields where emitted
traceable to relationship status, reason, and resolution target
```

### 12.2 Complex Relationship Non-Guarantee

A complex relationship does not mean:

```text
missing genotype evidence
evidence loss
projection failure
direct biallelic source linkage
inheritance limitation by itself
invalid genotype observation
```

A blank, missing, or sentinel `variant_id` on a complex row is not a genotype
preservation failure when the row is explicitly delegated to VDB brokerage.

---

## 13. Brokerage Contract

At maturity state:

```text
genotype_brokerage_evaluated
```

VDB guarantees that each brokerage-required genotype observation has either:

```text
a brokerage receipt
```

or:

```text
an explicit not_evaluated / policy_unavailable state
```

### 13.1 Brokerage Receipt Guarantee

Consumers may rely on brokerage receipts preserving:

```text
genotype_observation_id
source_record_hash
brokerage policy identity
allele-index mapping policy identity when applicable
variant normalization policy identity when applicable
symbolic ALT policy identity when applicable
spanning-deletion policy identity when applicable
brokerage outcome
derived relationship count
traceability references
```

### 13.2 Brokerage Non-Guarantee

Brokerage evaluation does not guarantee that every brokerage-required
relationship is resolved.

A brokerage outcome may be:

```text
brokerage_resolved
brokerage_ambiguous
brokerage_unresolved
brokerage_not_evaluated
brokerage_policy_unavailable
```

Unresolved brokerage is not evidence absence.

Policy-unavailable brokerage is not evidence absence.

---

## 14. Derived Relationship Contract

When VDB emits derived genotype-to-variant relationships, VDB guarantees that
they remain distinguishable from producer genotype observations and direct
producer relationships.

### 14.1 Derived Relationship Guarantee

Consumers may rely on derived relationships carrying:

```text
relationship_origin = vdb_derived
genotype_observation_id
source_record_hash
allele_index when applicable
source_alt_allele when applicable
relationship_state
relationship_derivation_policy_id
normalization state
ambiguity state
lossiness state
identity registration state
traceability state
anti-overclaim label
```

### 14.2 Multiallelic Cardinality Guarantee

A single `genotype_observation_id` may map to zero, one, or multiple VDB-derived
relationship identifiers.

Multiple VDB-derived relationships from one `genotype_observation_id` do not
imply multiple producer genotype observations.

### 14.3 Derived Relationship Non-Guarantee

A VDB-derived relationship is not:

```text
a producer genotype observation
a direct source-biallelic relationship unless explicitly producer-declared
an inheritance assertion
a disease assertion
a diagnosis
```

---

## 15. Spanning-Deletion Contract

For genotype observations involving spanning-deletion alleles such as:

```text
ALT = *
```

VDB guarantees conservative handling unless a declared spanning-deletion
resolution policy exists.

Allowed conservative relationship states include:

```text
spanning_deletion_context_required
unresolved_spanning_deletion
```

Consumers must not treat unresolved spanning-deletion state as:

```text
missing genotype evidence
variant absence
evidence loss
direct biallelic linkage
```

---

## 16. Declaration-Set Contract

At maturity state:

```text
genotype_assertion_ready
```

VDB guarantees that genotype declaration sets are available and non-interpretive.

Permitted declaration meanings include:

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

## 17. Topology Contract

At maturity state:

```text
genotype_topology_ready
```

VDB guarantees that genotype topology members and relationship basis surfaces
are:

```text
typed
traceable
source-preserving
basis-backed
policy-declared where derived
non-interpretive
```

VDB topology may include genotype observations, direct relationships, derived
relationships, unresolved relationship states, brokerage receipts, and genotype
declaration sets.

Topology readiness does not imply projection readiness.

Topology readiness does not imply RDGP reasoning.

Topology readiness does not imply clinical interpretation.

---

## 18. Legacy Compatibility Contract

For packages classified as:

```text
genotype_capability_unavailable_legacy
```

VDB may provide variant-only legacy compatibility.

### 18.1 Legacy Guarantee

Consumers may rely on explicit legacy states such as:

```text
variant_only_legacy_compatibility_mode
genotype_context_unavailable
genotype_not_emitted_by_source
genotype_projection_not_evaluated
```

### 18.2 Legacy Non-Guarantee

Consumers must not infer genotype from legacy variant-only packages.

Legacy genotype absence must not be interpreted as:

```text
homozygous reference
variant absence
no-call
callability
negative disease evidence
opportunity evidence
inheritance-readiness support
```

---

## 19. Mixed-Corpus Contract

VDB corpora may contain multiple producer types.

For mixed corpora, VDB guarantees producer-type-aware genotype applicability.

### 19.1 TEP-VAP

For `TEP-VAP` packages, genotype validation applies when genotype artifacts are
present or expected under modern genotype-capable ingestion.

### 19.2 TEP-GSC

For `TEP-GSC` packages, VDB may record:

```text
genotype_not_applicable_to_producer_type
```

This state must not fail the corpus merely because GSC does not emit genotype
evidence.

### 19.3 Mixed-Corpus Guarantee

Consumers may rely on mixed-corpus summaries distinguishing:

```text
genotype-applicable producer packages
genotype-not-applicable producer packages
legacy genotype-unavailable packages
invalid or quarantined genotype packages
```

---

## 20. Anti-Collapse Contract

VDB guarantees that validated genotype evidence surfaces preserve the following
non-equivalences:

```text
variant identity
    ≠ sample-specific variant observation

sample-specific variant observation
    ≠ genotype observation

genotype observation
    ≠ genotype-to-variant relationship

source genotype observation
    ≠ allele-specific relationship

VDB-derived relationship
    ≠ producer genotype observation

resolved_from_multiallelic_record
    ≠ direct_source_biallelic

genotype-to-variant relationship
    ≠ inheritance interpretation

execution provenance
    ≠ biological evidence
```

Any surface that collapses these distinctions is not contract-compliant.

---

## 21. Anti-Overclaim Contract

VDB genotype ingestion, preservation, declaration, brokerage, and topology
surfaces must not emit biological reasoning conclusions.

Consumers must not treat VDB genotype evidence surfaces as:

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

unless such claims are emitted by a separate governed reasoning producer.

VDB genotype surfaces may include anti-overclaim labels such as:

```text
genotype_relationship_not_inheritance_interpretation
multiallelic_relationship_not_independent_producer_row
allele_depth_annotation_not_independent_ad_vector
resolved_relationship_not_direct_source_biallelic
genotype_state_not_disease_model
genotype_missingness_not_absence
```

---

## 22. Validation Receipt Contract

VDB guarantees are valid only when the corresponding validation receipts pass.

Required receipt families may include:

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

If a receipt is absent, failed, or not evaluated, VDB must not claim the maturity
tier depending on that receipt.

---

## 23. Consumer Responsibilities

Consumers are responsible for respecting VDB state labels, relationship states,
maturity states, and anti-overclaim labels.

Consumers must not:

```text
interpret genotype missingness as homozygous reference
interpret no-call as absence
interpret unresolved relationship as evidence absence
interpret complex relationship as invalid genotype evidence
interpret derived relationship as producer genotype observation
interpret resolved_from_multiallelic_record as direct_source_biallelic
interpret execution provenance as biological evidence
interpret VDB topology as RDGP reasoning
interpret genotype-aware burden as disease association
```

Consumers that need inheritance, diagnosis, pathogenicity, or disease-model
claims must obtain them from a governed downstream reasoning producer.

---

## 24. Non-Guarantees

This contract does not guarantee:

```text
clinical diagnosis
pathogenicity correctness
inheritance-model satisfaction
compound heterozygosity
de novo status
carrier status
biallelic disease-model compatibility
variant causality
disease association
full symbolic ALT resolution
full spanning-deletion resolution
projection-surface availability unless genotype_projection_ready is validated
RDGP prioritization
```

This contract also does not guarantee that VAP producer output is scientifically
correct.

It guarantees VDB preservation, registration, brokerage-state exposure,
non-collapse, and non-overclaim behavior for the producer substrate.

---

## 25. Contract Violation Conditions

A VDB run, package, corpus, or surface violates this contract if it:

```text
claims a maturity tier without required passing validation receipts
classifies a partial genotype artifact set as legacy
accepts trusted modern genotype ingestion without required execution provenance
drops producer genotype rows
drops producer genotype columns without reconstructability
rewrites genotype_observation_id
replaces raw producer values with normalized convenience values
silently promotes complex relationships to direct relationships
creates synthetic producer genotype observations
hides unresolved relationships
treats spanning-deletion `*` as an ordinary ALT allele without policy
misclassifies execution provenance as biological evidence
interprets genotype missingness as homozygous reference
emits inheritance interpretation inside VDB genotype ingestion, declaration, or
topology layers
fails to distinguish TEP-GSC genotype-not-applicable status from TEP-VAP
genotype validation failure
```

Contract-violating outputs must not be treated as trusted genotype-aware VDB
surfaces.

---

## 26. Relationship to Implementation Plan

The implementation plan should sequence code work so that this contract becomes
true incrementally.

The implementation plan should not claim a maturity state before the
corresponding validation receipts exist and pass.

The recommended implementation order is:

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

Projection readiness may require later projection-specific documents and
validation beyond this contract's preservation scope.

---

## 27. Success Criteria

This contract is satisfied when downstream consumers can safely rely on VDB to:

```text
1. classify genotype capability explicitly for each package

2. report genotype maturity tier without overclaiming

3. require the complete genotype artifact set for trusted modern genotype
   ingestion

4. require execution provenance context for trusted modern genotype ingestion

5. preserve producer genotype observations without mutating producer truth

6. preserve producer identities and source traceability

7. distinguish direct producer relationships from VDB-derived relationships

8. preserve complex relationships as governed source states

9. represent brokerage outcomes using receipts or explicit unresolved /
   not-evaluated states

10. keep derived relationships structurally distinct from producer genotype
    observations

11. expose declaration and topology substrates without inheritance reasoning

12. support legacy variant-only packages without inferred genotype

13. support mixed corpora without treating genotype-not-applicable producers as
    genotype failures

14. enforce anti-collapse and anti-overclaim boundaries
```

---

## 28. Final Doctrine

VDB's genotype evidence contract is preservation-first, brokerage-aware,
validation-gated, and maturity-tiered.

VDB guarantees only what its validation receipts prove.

VDB preserves producer genotype observations as source evidence.

VDB registers direct producer relationships as producer-declared relationships.

VDB preserves complex relationships as governed source states.

VDB derives relationship topology only under declared policy.

VDB does not create producer genotype observations.

VDB does not infer inheritance.

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.

Scientists and clinicians interpret evaluated evidence.
```

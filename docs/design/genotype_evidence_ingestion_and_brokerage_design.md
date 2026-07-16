# Genotype Evidence Ingestion and Brokerage Design

**Status:** design draft  
**Intended path:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** VDB design for ingesting genotype-capable TEP-VAP packages and brokering genotype-to-variant relationships  
**Upstream authority:** VAP genotype-capable TEP-VAP producer substrate  
**Primary VDB policy authority:** `docs/design/multiallelic_relationships_vdb_brokerage_policy.md`  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  

---

## 1. Purpose

This document defines the VDB design for ingesting modern genotype-capable
TEP-VAP packages and constructing genotype-to-variant relationship substrates
without losing producer truth.

The architecture document establishes that genotype is first-class VDB evidence.

This design document describes how genotype evidence should move through VDB:

```text
TEP-VAP discovery
    → genotype artifact-set validation
        → execution provenance context registration
            → lossless genotype observation registration
                → direct relationship registration
                    → complex relationship preservation
                        → VDB brokerage
                            → genotype-informed Assertion Records
                                → genotype-informed Evidence Topology
```

The core design doctrine is:

```text
VDB first preserves the producer genotype observation, then separately evaluates
whether one or more genotype-to-variant relationships can be registered or
derived under VDB policy.
```

---

## 2. Scope

This document governs VDB behavior for:

```text
modern TEP-VAP genotype artifact discovery
execution provenance context registration
lossless genotype observation registration
direct genotype-to-variant relationship registration
complex genotype relationship preservation
multiallelic relationship brokerage
spanning-deletion conservative handling
genotype declaration set preparation
genotype-aware Assertion Record preparation
genotype-aware Evidence Topology preparation
validation receipt design
legacy compatibility behavior
```

This document does not define:

```text
final table schemas
SQL DDL
column-level schema contracts
CLI behavior
builder module names
RDGP scoring logic
inheritance reasoning
TEP-VDB projection surface schemas
```

Those concerns belong to later specification, schema, validation, contract,
implementation-plan, and code documents.

---

## 3. Authority Boundaries

### 3.1 VAP Producer Boundary

VAP owns source-faithful genotype preservation.

VAP emits:

```text
one authoritative genotype observation per selected sample per readable
source VCF record

raw FORMAT/sample evidence

source VCF identity

source VCF header identity

source record identity

sample and run identity

direct relationship state when safe

complex or unresolved relationship state when VDB brokerage is required
```

VDB must not reimplement VAP producer behavior.

VDB consumes the producer substrate.

---

### 3.2 VDB Brokerage Boundary

VDB owns ingestion, preservation, identity registration, relationship
registration, relationship brokerage, and non-interpretive topology.

VDB may:

```text
register producer genotype observations

register direct producer-declared relationships

preserve complex producer-declared relationship state

derive additive allele-specific relationship topology

record ambiguity, lossiness, normalization, policy, and traceability state

emit consumer-safe relationship substrates for downstream systems
```

VDB must not:

```text
create synthetic producer genotype observations

mutate producer genotype observations

silently promote complex relationships to direct relationships

collapse genotype observation into variant identity

infer inheritance

infer compound heterozygosity

infer disease causality

emit diagnosis
```

---

### 3.3 RDGP Reasoning Boundary

RDGP owns downstream biological reasoning.

RDGP may reason over VDB-emitted relationship surfaces.

VDB must expose genotype relationship state safely enough that RDGP does not
need to reconstruct VCF allele-index logic from raw FORMAT fields.

VDB must not implement RDGP reasoning behavior.

---

## 4. Design Goals

This design must support the following goals:

```text
1. Discover modern genotype-capable TEP-VAP packages.

2. Treat genotype artifacts as an atomic producer artifact set.

3. Register execution provenance as context, not biological evidence.

4. Preserve producer genotype observations without loss or mutation.

5. Keep variant identity, sample-specific variant observation, and genotype
   observation separately typed.

6. Register direct producer-declared genotype-to-variant relationships.

7. Preserve complex relationships as governed VDB-brokerage inputs.

8. Broker multiallelic relationships as additive derived topology.

9. Preserve spanning-deletion relationships conservatively until a specific
   resolution policy exists.

10. Prepare genotype declaration sets for Phase 4.3 Assertion Records.

11. Prepare typed genotype topology relationships for Phase 4.4 Evidence
    Topology.

12. Emit validation receipts proving no producer-truth collapse occurred.
```

---

## 5. Modern TEP-VAP Inputs

A modern genotype-capable TEP-VAP is expected to expose:

```text
entity_inventory.json

lineage_manifest.json

validation_report.md

entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json

entities/context/execution_provenance.json
```

VDB should inspect the small package-governance artifacts before touching the
large genotype observation table.

Recommended discovery order:

```text
1. validation_report.md
2. entity_inventory.json
3. lineage_manifest.json
4. genotype_projection_summary.json
5. genotype_source_header_context.json
6. execution_provenance.json
7. bounded probes or streaming reads of genotype_observations.tsv
```

The genotype observation table may be large.

The package contract should be established from inventory, lineage, validation,
summary, header context, and provenance before VDB streams row-level genotype
evidence.

---

## 6. Genotype Artifact-Set Discovery

The genotype artifact set is atomic.

The required genotype artifacts are:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

VDB must not classify a TEP-VAP package as genotype-enabled if only part of this
artifact set is present.

Discovery outcomes should use the canonical VDB genotype capability vocabulary:

```text
genotype_capability_available

genotype_capability_unavailable_legacy

genotype_capability_incomplete

genotype_capability_invalid

genotype_capability_unsupported_version
```

A partial genotype artifact set must never be classified as legacy.

Legacy means no genotype artifact set is present.

Incomplete means one or more genotype artifacts are present but the canonical
genotype artifact set is not complete.

Trusted genotype-aware ingestion requires:

```text
all three genotype artifacts present

transport paths registered in entity inventory

checksums present

lineage branch present

TEP validation status discoverable

projection summary coherent

source/header context preserved
```

Incomplete genotype artifact sets should be rejected or quarantined, not treated
as normal genotype-enabled evidence.

---

## 7. Execution Provenance Context Registration

Modern TEP-VAP packages transport execution provenance at:

```text
entities/context/execution_provenance.json
```

VDB should register this artifact as run/package context.

It should support:

```text
auditability
reproducibility
toolchain dependency tracking
reference-resource tracking
method-currency comparison
future RMCS integration
```

Execution provenance must not be treated as:

```text
variant evidence
genotype evidence
pathogenicity evidence
phenotype evidence
reasoning evidence
```

Design rule:

```text
execution_provenance describes how evidence was generated;
it does not assert biological state.
```

For trusted modern genotype-capable TEP-VAP ingestion, execution provenance is a
required context artifact.

VDB may explicitly represent absent execution provenance only for legacy,
compatibility, quarantine, or unsupported-version paths.

Trusted modern genotype ingestion should not proceed if execution provenance is
missing, malformed, or misclassified.

---

## 8. Lossless Genotype Observation Registration

VDB must register genotype observations as immutable producer evidence.

Registration must preserve the complete producer row and every emitted field.

Important preserved field classes include:

```text
schema and identity fields

sample and run fields

source VCF and header identity fields

source record ordinal, line, and hash fields

reference build and coordinate fields

reference and alternate allele fields

relationship status, reason, and target fields

raw FORMAT and sample FORMAT fields

GT / AD / DP / GQ / PL / FT fields where emitted

GT parsing and call-state fields

called allele indices

missingness and no-call fields

depth and quality convenience fields

site and sample filter fields

record parse and preservation status fields

projection advisory and warning fields
```

VDB may create persistence identifiers.

VDB may create canonical identifiers.

VDB may create relationship identifiers.

None of those identifiers may replace `genotype_observation_id`.

---

## 9. Relationship Partitioning Model

After preserving genotype observations, VDB should partition relationship
handling by producer-declared relationship fields.

Relevant producer fields include:

```text
variant_relationship_status

relationship_reason

relationship_resolution_target

variant_id

variant_observation_id

alternate_alleles_raw

alternate_allele_count

called_allele_indices

source_record_hash
```

Minimum relationship partitions:

```text
direct

complex

unresolved

not_applicable
```

The design rule is:

```text
relationship partitioning is not relationship brokerage.
```

Partitioning decides how VDB should route the row.

Brokerage decides whether and how VDB can construct derived relationship
topology.

---

## 10. Direct Relationship Registration

For rows where:

```text
variant_relationship_status = direct
relationship_resolution_target = none
variant_id is populated
```

VDB may register the direct producer-declared genotype-to-variant relationship.

The direct relationship must remain distinguishable from VDB-derived
relationships.

Recommended direct relationship state:

```text
direct_source_biallelic
```

Direct registration should preserve:

```text
genotype_observation_id

variant_id

variant_observation_id when emitted

sample_id

run_id

source package identity

source_record_hash

reference build

coordinate and allele context

producer relationship status

producer relationship reason

producer relationship resolution target
```

A direct relationship is a producer-declared link.

It is not an inheritance assertion.

---

## 11. Complex Relationship Preservation

For rows where:

```text
variant_relationship_status = complex
relationship_resolution_target = vdb_brokerage
```

VDB must preserve the source genotype observation and producer relationship
state.

Complex relationship preservation should record:

```text
genotype_observation_id

relationship_reason

relationship_resolution_target

source_record_hash

alternate_alleles_raw

alternate_allele_count

called_allele_indices

gt_raw

ad_raw

dp_raw

gq_raw

pl_raw

format_raw

sample_format_raw

record_parse_status

record_preservation_status

projection_advisory_codes

projection_warning_codes
```

A complex relationship is not:

```text
missing genotype evidence

evidence loss

projection failure

direct biallelic source linkage

inheritance limitation by itself
```

It is a governed source state that may require VDB relationship brokerage.

---

## 12. Multiallelic Brokerage Design

Multiallelic brokerage should be performed under a declared VDB policy.

Canonical example:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

VAP emits one genotype observation.

VDB preserves that genotype observation.

VDB may then derive two relationship edges:

```text
genotype_observation G
    → allele index 1 / source ALT C

genotype_observation G
    → allele index 2 / source ALT G
```

Both derived relationships must preserve:

```text
same genotype_observation_id

same source_record_hash

same source record context

allele index

source ALT allele

relationship derivation policy

normalization policy if used

ambiguity state

lossiness state

traceability references
```

Neither derived relationship is a new producer genotype observation.

Recommended brokerage sequence:

```text
1. Read the preserved source genotype observation.

2. Confirm source record identity and preservation state.

3. Parse called allele indices from the preserved genotype state.

4. Confirm called non-reference allele indices are within the source ALT list.

5. Map each called non-reference allele index to a source ALT allele.

6. Construct an allele-specific source allele candidate:
       reference_build, chromosome, position, reference_allele, source_alt_allele

7. Apply declared variant normalization policy if required.

8. Match or register allele-specific variant identity.

9. Construct a derived relationship if mapping is unambiguous.

10. Emit ambiguous or unresolved relationship state if mapping is not safe.

11. Preserve policy, ambiguity, lossiness, and traceability metadata.
```

Required policy concepts include:

```text
multiallelic_relationship_policy_id

allele_index_mapping_policy_id

variant_normalization_policy_id

identity_registration_policy_id

lossiness_policy_id
```

No splitting, trimming, left-alignment, normalization, symbolic handling, or
relationship resolution may occur silently.

---

## 13. Spanning-Deletion Conservative Handling

Spanning-deletion alleles such as:

```text
ALT = *
```

require conservative handling.

VDB must not treat `*` as an ordinary SNV or small-indel alternate allele unless
a specific spanning-deletion policy exists.

Initial conservative states should include:

```text
spanning_deletion_context_required

unresolved_spanning_deletion
```

For spanning-deletion rows, VDB should preserve:

```text
genotype_observation_id

source_record_hash

alternate_alleles_raw

called_allele_indices

gt_raw

ad_raw

record_preservation_status

producer relationship status

producer relationship reason

producer relationship resolution target
```

A spanning-deletion context can remain preserved and explicitly unresolved.

Unresolved is not absence.

Unresolved is not evidence loss.

---

## 14. Relationship State Axes

VDB should not overload one field with all relationship semantics.

Design should support separate axes:

```text
relationship_state

ambiguity_state

lossiness_state

normalization_state

identity_registration_state

traceability_state

depth_availability_state
```

Example resolved multiallelic relationship:

```text
relationship_state = resolved_from_multiallelic_record
ambiguity_state = unambiguous
lossiness_state = lossless_allele_index_mapping
normalization_state = no_normalization_required
identity_registration_state = variant_identity_registered
traceability_state = source_trace_complete
```

Example unresolved relationship:

```text
relationship_state = unresolved_normalization_ambiguous
ambiguity_state = ambiguous_normalized_mapping
lossiness_state = potentially_lossy
normalization_state = nontrivial_normalization
identity_registration_state = unresolved
traceability_state = source_trace_complete
```

These axes make later CUES, RMCS, OACS, GIRS, EVRS, and PGERS integration
possible without hiding uncertainty.

---

## 15. FORMAT and Depth Semantics

VDB must preserve record-level FORMAT semantics.

For a multiallelic record:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

The source AD vector is record-scoped:

```text
AD = 2,4,9
```

VDB may derive relationship-level annotations:

```text
allele index 1 / ALT C / allele_depth = 4

allele index 2 / ALT G / allele_depth = 9
```

VDB must not claim:

```text
A>C has independent producer AD = 2,4

A>G has independent producer AD = 2,9
```

Relationship-level allele depth is a VDB-derived annotation from source
allele-index mapping.

It is not an independent producer AD vector.

Fields such as `PL` may encode genotype-combination likelihoods rather than
independent allele-level quantities. VDB should preserve them as source record
evidence unless a specific policy governs derived use.

---

## 16. Genotype Declaration Sets for Phase 4.3

Before genotype-informed Assertion Records are created, VDB should define
declaration-set inputs that expose genotype evidence without interpretation.

Candidate declaration sets include:

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

These declaration sets should preserve source handles and policy context.

They should not perform inheritance reasoning.

---

## 17. Genotype-Informed Assertion Records

After lossless registration and declaration-set construction, VDB may create
genotype-informed Assertion Records.

Permitted assertion examples:

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

Brokerage-completed assertions may be added only after VDB relationship
brokerage succeeds under declared policy.

Invalid assertion examples:

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

## 18. Genotype Evidence Topology for Phase 4.4

Evidence Topology is the primary place where VDB-brokered relationships become
typed non-interpretive topology.

Candidate topology relations include:

```text
sample_variant_observation
    has_genotype_observation

genotype_observation
    has_raw_genotype_field

genotype_observation
    has_called_allele_index

genotype_observation
    has_normalized_call_state

genotype_observation
    has_quality_state

genotype_observation
    has_phase_context

genotype_observation
    has_missingness_state

genotype_observation
    brokered_to_variant_identity

genotype_observation
    brokered_to_sample_variant_observation

genotype_observation
    relationship_unresolved

genotype_observation
    relationship_ambiguous
```

Every topology relation should carry:

```text
participant roles

source genotype observation reference

source record reference

relationship type

relationship state

policy references

normalization state

ambiguity state

lossiness state

traceability references
```

Topology must remain non-interpretive.

---

## 19. Validation Receipt Design

VDB should emit validation receipts proving genotype evidence preservation and
safe brokerage.

Minimum validation receipt topics:

```text
genotype artifact-set completeness

canonical genotype artifact checksum reconciliation for trusted modern genotype
ingestion

entity inventory reconciliation

lineage branch reconciliation

validation-report status capture

genotype projection summary reconciliation

source-header context registration

execution provenance context registration

execution provenance checksum reconciliation for trusted modern genotype
ingestion

row-count preservation

column preservation

genotype_observation_id preservation

genotype_observation_id uniqueness

sample / run / reference-build coherence

source VCF identity preservation

source VCF header identity preservation

source record identity preservation

relationship partition reconciliation

direct relationship registration count

complex relationship preservation count

brokerage input count

brokerage attempted count

brokerage resolved count

brokerage ambiguous count

brokerage unresolved count

brokerage not-evaluated count

spanning-deletion conservative state count

no producer observation splitting

no inheritance interpretation emitted
```

Validation should fail if VDB:

```text
drops genotype rows

changes producer genotype_observation_id

silently rewrites raw FORMAT/sample values

promotes complex relationships to direct source relationships

creates synthetic producer genotype observations

hides unresolved relationships

emits inheritance conclusions
```

---

## 20. Legacy Compatibility Mode

Older TEP-VAP packages may lack genotype artifacts.

VDB may support them under explicit compatibility states:

```text
variant_only_legacy_compatibility_mode

genotype_context_unavailable

genotype_not_emitted_by_source

genotype_projection_not_evaluated
```

Legacy compatibility mode must not infer genotype.

VDB must not treat absent genotype artifacts as:

```text
homozygous reference

variant absence

no-call

callability

negative disease evidence

opportunity evidence
```

Legacy mode should remain usable for historical artifacts but must not be treated
as the target architecture for modern genotype-capable TEP-VAPs.

---

## 21. Candidate Implementation Surfaces

This design anticipates, but does not finalize, the following possible VDB
implementation surfaces:

```text
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

genotype_evidence_validation_summary
```

These names align with the logical schema document.

Final physical storage choices still belong to implementation.

A later union surface such as `genotype_variant_relationships` may be exposed
only if it preserves `relationship_origin`, `relationship_state`, source
traceability, and derivation-policy fields strongly enough to prevent collapse
between producer-declared direct relationships and VDB-derived relationships.

---

## 22. Non-Goals

This design does not:

```text
define final SQL tables

define final TSV schemas

define final field ordering

define API behavior

define CLI behavior

define RDGP reasoning rules

define inheritance models

define clinical interpretation

define GIRS / PGERS / EVRS / OACS / CUES / RMCS schemas

resolve every symbolic ALT class

resolve spanning deletion semantics beyond conservative preservation

replace the VDB multiallelic brokerage policy
```

---

## 23. Success Criteria

This design is successful when it gives DEX-VDB a clear path to implement:

```text
1. genotype-capable TEP-VAP discovery

2. complete genotype artifact-set validation

3. execution provenance context registration

4. lossless genotype observation registration

5. direct producer relationship registration

6. complex relationship preservation

7. governed multiallelic relationship brokerage

8. conservative spanning-deletion handling

9. genotype declaration sets

10. genotype-informed Assertion Records

11. genotype-informed Evidence Topology

12. validation receipts proving no loss, collapse, or reasoning overreach
```

The design is not successful if implementation would:

```text
hide genotype inside variant identity

treat genotype as a late projection overlay

create synthetic producer genotype observations

force RDGP to reconstruct VCF allele-index logic

emit inheritance conclusions inside VDB
```

---

## 24. Relationship to Later Documents

This design should be followed by:

```text
docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md

docs/implementation/schemas/genotype_evidence_schema.md

docs/validation/genotype_evidence_preservation_validation.md

docs/contracts/genotype_evidence/genotype_evidence_contract.md

docs/plans/genotype_evidence/genotype_evidence_plan.md
```

The architecture document defines:

```text
what must remain true
```

This design document defines:

```text
how evidence should move through VDB while those truths remain intact
```

The specification will define:

```text
required VDB behavior
```

The schema will define:

```text
physical and logical representation
```

The validation document will define:

```text
how preservation and brokerage correctness are proven
```

The contract will define:

```text
what VDB guarantees to downstream consumers after successful ingestion
```

The implementation plan will define:

```text
the code and test sequence
```

---

## 25. Final Doctrine

VDB ingests genotype observations as immutable producer evidence.

VDB registers direct producer-declared relationships separately from
VDB-derived brokerage relationships.

VDB preserves complex genotype relationships as governed source states before
deriving relationship topology.

VDB performs multiallelic and related brokerage as additive, typed,
policy-declared topology.

VDB does not create new producer genotype observations.

VDB does not infer inheritance.

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.
```

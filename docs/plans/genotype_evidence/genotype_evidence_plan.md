# Genotype Evidence Implementation Plan

**Status:** implementation plan draft  
**Intended path:** `docs/plans/genotype_evidence/genotype_evidence_plan.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** Maturity-tiered implementation roadmap for genotype evidence discovery, preservation, relationship registration, brokerage, declaration, topology preparation, and validation receipts  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Design parent:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Specification parent:** `docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md`  
**Schema parent:** `docs/implementation/schemas/genotype_evidence_schema.md`  
**Validation parent:** `docs/validation/genotype_evidence_preservation_validation.md`  
**Contract parent:** `docs/contracts/genotype_evidence/genotype_evidence_contract.md`  

---

## 1. Purpose

This document defines the implementation plan for adding first-class genotype
evidence support to VDB.

The plan translates the genotype evidence architecture, design, specification,
schema, validation, and contract into an ordered implementation sequence.

The core implementation doctrine is:

```text
No genotype-applicable package may claim a genotype maturity tier until the
validation receipts for that tier exist and pass.

No genotype-not-applicable package may be placed on the cumulative genotype
maturity ladder.
```

For a producer package whose evidence domain excludes genotype, the correct
package state is:

```text
genotype_maturity_not_applicable
```

This state requires passing package-classification validation but is not itself
a genotype evidence maturity tier.

This plan is maturity-tiered.

It does not attempt to jump directly to genotype topology or projection
readiness.

---

## 2. Scope

This plan covers implementation of:

```text
genotype package discovery

genotype capability classification

genotype artifact indexing

genotype projection summary indexing

genotype source-header context indexing

execution provenance context indexing

source genotype observation preservation

relationship input routing

direct producer relationship registration

complex relationship preservation

brokerage receipts

derived genotype-to-variant relationship scaffolding

genotype declaration sets for Phase 4.3

genotype topology members and basis for Phase 4.4

validation receipt generation

single-package and mixed-corpus validation
```

This plan does not cover:

```text
projection-surface schemas

TEP-VDB emission format

RDGP reasoning implementation

clinical interpretation

full symbolic ALT resolution

full spanning-deletion resolution

final performance optimization

database migration finalization
```

Projection readiness requires later projection-specific design and validation.

---

## 3. Authority Stack

Implementation must follow the genotype evidence foundation:

```text
docs/architecture/genotype_first_class_vdb_evidence_model.md

docs/design/genotype_evidence_ingestion_and_brokerage_design.md

docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md

docs/implementation/schemas/genotype_evidence_schema.md

docs/validation/genotype_evidence_preservation_validation.md

docs/contracts/genotype_evidence/genotype_evidence_contract.md
```

The VDB multiallelic brokerage policy remains the primary VDB relationship
governance authority for multiallelic and related brokerage behavior.

Implementation must not import VAP producer behavior into VDB.

Implementation must not import RDGP reasoning behavior into VDB.

---

## 4. Implementation Doctrine

The implementation order is:

```text
preserve first

classify second

route third

register direct fourth

preserve complex fifth

broker sixth

assert seventh

topologize eighth

project later
```

The implementation must preserve the following non-equivalences:

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

The implementation must treat maturity states as validated claims, not labels of
intent.

---

## 5. Producer-Aware Maturity Roadmap

Implementation must distinguish:

```text
the cumulative genotype maturity progression for genotype-applicable producer
packages

and

the terminal genotype-not-applicable state for producer package types whose
evidence domains exclude genotype
```

### 5.1 Genotype-Applicable Progression

For genotype-applicable producer packages, the implementation plan follows:

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

This plan targets the first seven genotype-applicable maturity states.

`genotype_projection_ready` is explicitly deferred.

### 5.2 Genotype-Not-Applicable State

For a producer package type whose evidence domain excludes genotype, the
required state is:

```text
genotype_maturity_not_applicable
```

This state is not an entry point into the cumulative maturity progression.

It means that genotype maturity does not apply to the producer package's
evidence grammar.

Package classification completion is represented separately by:

```text
classification_status = classified
```

and by passing package-classification validation receipts.

### 5.3 Current Required Pairings

```text
modern genotype-capable TEP-VAP:
    producer_genotype_applicability_state =
        genotype_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_available

    genotype_maturity_state =
        genotype_discovered

legacy variant-only TEP-VAP:
    producer_genotype_applicability_state =
        genotype_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_unavailable_legacy

    genotype_maturity_state =
        genotype_discovered

TEP-GSC:
    producer_genotype_applicability_state =
        genotype_not_applicable_to_producer_type

    genotype_capability_state =
        genotype_capability_not_applicable

    genotype_maturity_state =
        genotype_maturity_not_applicable
```

Future producer families must receive explicit applicability, capability, and
maturity rules.

They must not silently inherit VAP or GSC behavior.

---

## 6. Stage 0 — Foundation Read-In and Guardrails

### 6.1 Target Maturity

```text
none
```

This is a preparation stage.

### 6.2 Purpose

Establish implementation guardrails before code changes.

### 6.3 Work Items

```text
commit the genotype foundation document stack

confirm intended paths for architecture, design, specification, schema,
validation, contract, and plan

verify current VDB Phase 4.1–4.4 implementation surfaces

identify existing package, assertion-record, and topology builder entry points

define implementation branch or commit scope
```

### 6.4 Required Receipts

```text
none
```

### 6.5 Tests

```text
no new runtime tests required
```

### 6.6 Exit Criteria

```text
foundation docs are present

implementation scope is producer-aware package classification first

genotype-applicable packages may first achieve genotype_discovered

genotype-not-applicable packages must use genotype_maturity_not_applicable

projection and RDGP reasoning are explicitly deferred
```

---

## 7. Stage 1 — Package Discovery and Producer-Aware Classification

### 7.1 Target Package States

For genotype-applicable producer packages:

```text
genotype_discovered
```

For producer package types whose evidence domains exclude genotype:

```text
genotype_maturity_not_applicable
```

These outcomes are mutually exclusive.

### 7.2 Purpose

Discover producer genotype applicability and classify package genotype
capability and maturity before trusted genotype ingestion.

### 7.3 Work Items

Implement package-level discovery for:

```text
entity_inventory.json

lineage_manifest.json

validation_report.md

entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json

entities/context/execution_provenance.json
```

Persist exactly one package-level classification in:

```text
source_genotype_package_classifications
```

Implement canonical genotype applicability states:

```text
genotype_applicable_to_producer_type

genotype_not_applicable_to_producer_type
```

Implement canonical genotype capability states:

```text
genotype_capability_available

genotype_capability_unavailable_legacy

genotype_capability_not_applicable

genotype_capability_incomplete

genotype_capability_invalid

genotype_capability_unsupported_version
```

Implement producer-aware applicability, capability, and maturity pairing:

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

Record classification completion separately:

```text
classification_status = classified
```

Future producer families must receive explicit producer-specific classification
rules.

They must not silently inherit TEP-GSC behavior merely because they are not
TEP-VAP.

### 7.4 Required Package-Level Receipts

```text
genotype_package_classification_receipt

genotype_artifact_set_validation_receipt when genotype applies
```

The mixed-corpus receipt is not required to establish one package's Stage 1
classification.

It is generated later during corpus-level validation.

### 7.5 Tests

Test cases must cover:

```text
complete modern genotype-capable TEP-VAP

legacy variant-only TEP-VAP

partial genotype artifact set

invalid genotype artifact set

unsupported genotype schema version

TEP-GSC using:

    genotype_not_applicable_to_producer_type

    genotype_capability_not_applicable

    genotype_maturity_not_applicable

invalid capability/applicability pairings, including:

    TEP-GSC with genotype_capability_unavailable_legacy

    TEP-VAP with genotype_capability_not_applicable

invalid maturity/applicability pairings, including:

    TEP-GSC with genotype_discovered

    TEP-VAP with genotype_maturity_not_applicable

undeclared producer family without an explicit classification rule
```

### 7.6 Exit Criteria

```text
every registered package receives exactly one package-level genotype
classification

every classification records producer_family

every classification records applicability, capability, and maturity

classification_status = classified

partial genotype artifact sets are not classified as legacy

TEP-GSC is not treated as failed or missing genotype evidence

TEP-GSC uses genotype_maturity_not_applicable rather than
genotype_discovered

legacy TEP-VAP uses genotype_discovered only as classification-level maturity
and does not imply genotype observations exist

capability and applicability form a coherent producer-aware pair

maturity and applicability form a coherent producer-aware pair

no large genotype table is trusted before governance artifacts are inspected
```

---

## 8. Stage 2 — Artifact Index and Context Surface Registration

### 8.1 Target Maturity

```text
no new package maturity state
```

For genotype-applicable packages, this stage extends the
`genotype_discovered` substrate with indexed artifact and context surfaces.

For genotype-not-applicable packages, the package remains:

```text
genotype_maturity_not_applicable
```

and must not synthesize genotype artifact or context surfaces.

### 8.2 Purpose

Materialize package-level genotype artifact and context surfaces before
row-level genotype observation preservation.

### 8.3 Work Items

Implement or prepare logical surfaces for:

```text
genotype_artifact_index

genotype_projection_summary_index

genotype_source_header_context_index

execution_provenance_context_index
```

For `genotype_projection_summary_index`, capture:

```text
genotype observation row count

source record count when emitted

direct relationship count

complex relationship count

unresolved relationship count when emitted

not-applicable relationship count when emitted

projection status

projection error and warning counts

summary reconciliation state
```

For `genotype_source_header_context_index`, capture:

```text
source VCF identity

source VCF header identity

reference build

contig context

FORMAT definition context

sample-column context

selected sample column
```

For `execution_provenance_context_index`, capture:

```text
execution provenance artifact path

execution provenance artifact checksum

contract status

toolchain context

annotation environment context

resource environment context

registered_as_context = true
```

### 8.4 Required Receipts

```text
execution_provenance_context_validation_receipt

genotype_count_reconciliation_receipt
```

### 8.5 Tests

Test cases should cover:

```text
execution provenance present and registered as context

execution provenance missing in trusted modern genotype-capable package

execution provenance misclassified as evidence

projection summary parse failure

source-header context parse failure

checksum missing or mismatch in trusted modern genotype-capable package
```

### 8.6 Exit Criteria

```text
trusted modern genotype-capable ingestion fails or quarantines when execution
provenance is absent, malformed, or misclassified

projection summary values are available for count reconciliation

source-header context values are available for identity preservation

execution provenance is never registered as biological evidence
```

---

## 9. Stage 3 — Source Genotype Observation Preservation

### 9.1 Target Maturity

```text
genotype_preservation_validated
```

### 9.2 Purpose

Preserve every producer genotype observation row as immutable source evidence.

### 9.3 Work Items

Implement source genotype observation preservation for:

```text
source_genotype_observations
```

Required behavior:

```text
stream or load genotype_observations.tsv without mutating producer values

preserve all producer-emitted columns

preserve genotype_observation_id exactly

preserve source VCF identity

preserve source VCF header identity

preserve source record identity

preserve sample identity

preserve run identity

preserve reference build

preserve raw FORMAT and sample FORMAT fields

preserve GT / AD / DP / GQ / PL / FT fields where emitted

preserve called allele indices

preserve missingness and no-call states

preserve relationship status, reason, and resolution target

preserve projection advisory and warning codes
```

Implement full-row reconstructability by either:

```text
typed/indexed column preservation

or

typed/indexed fields plus raw source-row extension representation
```

### 9.4 Required Receipts

```text
source_genotype_observation_preservation_receipt

genotype_identity_preservation_receipt

genotype_count_reconciliation_receipt
```

### 9.5 Tests

Test cases should cover:

```text
row count reconciliation

all producer columns preserved or reconstructable

genotype_observation_id unchanged

genotype_observation_id uniqueness

sample/run/reference-build coherence

source VCF identity preservation

source VCF header identity preservation

source record identity preservation

raw FORMAT/sample values not replaced by normalized convenience values

producer_observation_split_count = 0

inheritance_assertion_count = 0
```

### 9.6 Exit Criteria

```text
VDB preserved genotype row count equals producer genotype_observations.tsv row
count

all producer columns are preserved or reconstructable

producer genotype identities remain recoverable

no producer genotype observation is split

no inheritance assertion is emitted
```

---

## 10. Stage 4 — Relationship Input Routing

### 10.1 Target Maturity

```text
no new maturity state
```

Relationship input routing is a required prerequisite for:

```text
genotype_direct_relationships_registered

genotype_complex_relationships_preserved
```

This stage extends the `genotype_preservation_validated` substrate with
relationship-routing readiness, but it does not by itself unlock a new genotype
maturity state.

### 10.2 Purpose

Route preserved genotype observations into relationship handling classes without
performing relationship brokerage.

### 10.3 Work Items

Implement:

```text
genotype_relationship_input_index
```

Assign one relationship input class per genotype observation:

```text
direct_relationship_input

complex_relationship_input

unresolved_relationship_input

not_applicable_relationship_input

unsupported_relationship_input
```

Use producer fields:

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

### 10.4 Required Receipts

```text
relationship_partition_validation_receipt
```

### 10.5 Tests

Test cases should cover:

```text
direct rows routed to direct_relationship_input

complex rows routed to complex_relationship_input

unresolved rows remain unresolved

not-applicable rows remain explicit

unsupported status values are preserved and not silently trusted

blank variant_id on complex row is not evidence failure
```

### 10.6 Exit Criteria

```text
every genotype observation receives one relationship input class

direct + complex + unresolved + not-applicable counts reconcile to total
genotype rows

relationship partitioning does not mutate source genotype observations

relationship partitioning is not represented as brokerage
```

---

## 11. Stage 5 — Direct Producer Relationship Registration

### 11.1 Target Maturity

```text
genotype_direct_relationships_registered
```

### 11.2 Purpose

Register eligible direct producer-declared genotype-to-variant relationships.

### 11.3 Work Items

Implement:

```text
direct_genotype_variant_relationships
```

A row is eligible when:

```text
variant_relationship_status = direct

relationship_resolution_target = none

variant_id is populated

genotype_observation_id is populated

source_record_hash is populated
```

Register direct relationship rows with:

```text
relationship_origin = producer_declared

relationship_state = direct_source_biallelic
```

Preserve:

```text
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

### 11.4 Required Receipts

```text
relationship_partition_validation_receipt

direct_relationship_registration_receipt
```

### 11.5 Tests

Test cases should cover:

```text
eligible direct rows registered

ineligible direct rows rejected or routed to explicit non-direct state

direct rows retain producer-declared origin

direct rows retain direct_source_biallelic state

direct rows remain distinguishable from derived relationships

direct rows emit no inheritance claims
```

### 11.6 Exit Criteria

```text
eligible direct relationships are registered

relationship_origin = producer_declared

relationship_state = direct_source_biallelic

no direct relationship implies inheritance, disease causality, or diagnosis
```

---

## 12. Stage 6 — Complex Relationship Preservation

### 12.1 Target Maturity

```text
genotype_complex_relationships_preserved
```

### 12.2 Purpose

Preserve complex genotype relationships as governed source states before
attempting brokerage.

### 12.3 Work Items

Ensure complex rows are:

```text
preserved in source_genotype_observations

represented in genotype_relationship_input_index

not dropped

not silently promoted to direct

not represented as missing genotype evidence

routed to brokerage input or explicit not-evaluated state
```

Preserve complex row evidence:

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

### 12.4 Required Receipts

```text
complex_relationship_preservation_receipt
```

### 12.5 Tests

Test cases should cover:

```text
complex rows preserved as source genotype observations

complex rows routed to brokerage input or explicit not-evaluated state

blank variant_id on complex rows preserved as meaningful producer state

complex rows not treated as evidence loss

complex rows not promoted to direct_source_biallelic

complex rows emit no inheritance claims
```

### 12.6 Exit Criteria

```text
all complex rows remain visible

complex row count reconciles

complex rows are preserved before brokerage

complex relationships are governed source states, not failures
```

---

## 13. Stage 7 — Brokerage Receipts and Derived Relationship Scaffolding

### 13.1 Target Maturity

```text
genotype_brokerage_evaluated
```

### 13.2 Purpose

Create the brokerage receipt and derived relationship infrastructure needed to
evaluate brokerage-required genotype observations.

This stage may begin conservatively.

Full multiallelic resolution is not required on the first implementation pass.

### 13.3 Work Items

Implement:

```text
genotype_brokerage_receipts

derived_genotype_variant_relationships
```

Every brokerage-required genotype observation must receive either:

```text
a brokerage receipt
```

or:

```text
an explicit not_evaluated / policy_unavailable state
```

Initial brokerage outcomes may include:

```text
brokerage_not_evaluated

brokerage_policy_unavailable

brokerage_unresolved

brokerage_ambiguous

brokerage_resolved
```

Derived relationships must preserve:

```text
relationship_origin = vdb_derived

genotype_observation_id

source_record_hash

allele_index when applicable

source_alt_allele when applicable

relationship_derivation_policy_id

normalization state

ambiguity state

lossiness state

identity registration state

traceability state

anti-overclaim label
```

### 13.4 Required Receipts

```text
brokerage_receipt_validation_receipt

derived_relationship_validation_receipt

spanning_deletion_validation_receipt
```

### 13.5 Tests

Test cases should cover:

```text
brokerage-required row receives receipt or explicit not-evaluated state

derived relationship uses relationship_origin = vdb_derived

multiallelic-derived relationship is not direct_source_biallelic

multiple derived relationships from one genotype_observation_id do not create
multiple source genotype observations

spanning-deletion alleles use conservative states unless policy exists

unresolved brokerage is not evidence absence

policy-unavailable brokerage is not evidence absence
```

### 13.6 Exit Criteria

```text
brokerage input count reconciles with brokerage receipts and explicit outcomes

derived relationships are structurally distinct from producer genotype
observations

spanning-deletion rows are conservative unless declared policy resolves them

no derived relationship emits inheritance, disease causality, or diagnosis
```

---

## 14. Stage 8 — Genotype Declaration Sets for Phase 4.3

### 14.1 Target Maturity

```text
genotype_assertion_ready
```

### 14.2 Purpose

Prepare genotype declaration sets for Phase 4.3 Assertion Records.

### 14.3 Work Items

Implement:

```text
genotype_declaration_sets
```

Allowed declaration set types include:

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

### 14.4 Required Receipts

```text
declaration_set_validation_receipt

anti_overclaim_validation_receipt
```

### 14.5 Tests

Test cases should prove declaration sets do not encode:

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

### 14.6 Exit Criteria

```text
genotype declaration sets are source-traceable

genotype declaration sets are typed

genotype declaration sets are basis-linked

genotype declaration sets are non-interpretive

genotype assertion readiness is receipt-backed
```

---

## 15. Stage 9 — Genotype Topology Substrates for Phase 4.4

### 15.1 Target Maturity

```text
genotype_topology_ready
```

### 15.2 Purpose

Integrate genotype evidence and relationships into Phase 4.4 Evidence Topology
without introducing interpretation.

### 15.3 Work Items

Implement:

```text
genotype_topology_members

genotype_topology_relationship_basis
```

Integrate these surfaces with the existing Phase 4.4 topology builder rather
than replacing the topology builder.

Topology members may include:

```text
genotype_observation

direct_genotype_variant_relationship

derived_genotype_variant_relationship

genotype_relationship_unresolved_state

genotype_brokerage_receipt

genotype_declaration_set
```

Topology relationship basis rows may include:

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

### 15.4 Required Receipts

```text
topology_substrate_validation_receipt

topology_relationship_basis_validation_receipt

anti_collapse_validation_receipt

anti_overclaim_validation_receipt
```

### 15.5 Tests

Test cases should prove:

```text
every genotype topology relationship has basis

genotype topology members are typed

genotype topology basis rows are traceable

derived topology relationships preserve policy references

direct and derived relationships remain distinct

topology edges emit no inheritance claims
```

### 15.6 Exit Criteria

```text
genotype topology surfaces are typed, traceable, source-preserving,
basis-backed, policy-declared where derived, and non-interpretive

genotype_topology_ready is claimed only after topology validation receipts pass
```

---

## 16. Stage 10 — Corpus-Scale Validation

### 16.1 Target Maturity

```text
tier-dependent
```

### 16.2 Purpose

Validate implementation behavior over single-package and mixed-corpus cases.

### 16.3 Corpus Targets

Run staged validation over:

```text
single modern genotype-capable TEP-VAP smoke package

near-term three-TEP mixed-producer proof corpus:
    ERR10619300 median TEP-VAP
    epilepsy TEP-GSC
    mitochondrial TEP-GSC

later five-TEP mixed-corpus expansion:
    ERR10619212 q1 TEP-VAP
    ERR10619300 median TEP-VAP
    ERR10619225 q3 TEP-VAP
    epilepsy TEP-GSC
    mitochondrial TEP-GSC
```

The three-TEP proof corpus is the first required mixed-producer closure target.

The five-TEP corpus remains a later breadth and depth expansion after the
three-TEP producer-neutral behavior is validated.

### 16.4 Required Receipts

```text
genotype_evidence_validation_summary

mixed_corpus_genotype_scope_receipt
```

Plus all maturity-specific receipts required by the tier being claimed.

### 16.5 Tests

Corpus-scale tests should prove:

```text
TEP-VAP packages are genotype-applicable

modern genotype-capable TEP-VAP packages pass or fail under genotype rules

TEP-GSC packages are genotype_not_applicable_to_producer_type

TEP-GSC packages use genotype_capability_not_applicable

TEP-GSC packages use genotype_maturity_not_applicable

TEP-GSC packages are not assigned genotype_discovered

genotype-applicable TEP-VAP packages are not assigned
    genotype_maturity_not_applicable

TEP-GSC packages are not classified as
    genotype_capability_unavailable_legacy

GSC absence of genotype evidence does not fail the mixed corpus

mixed-corpus summaries preserve distinct producer evidence grammars:

    TEP-VAP:
        sample_id × variant_id
        sample_id × genotype_observation_id

    TEP-GSC:
        phenotype_id × gene_id

one corpus-level evaluation consumes all three declared package classifications

three-TEP aggregate values equal:

    package_count = 3

    genotype_applicable_count = 1

    genotype_not_applicable_count = 2

    legacy_genotype_unavailable_count = 0

    invalid_or_incomplete_count = 0

    genotype_applicable_package_maturity_floor =
        genotype_discovered

    mixed_corpus_exercised = true

corpus-level genotype maturity floor is computed only across
genotype-applicable packages

genotype_maturity_not_applicable is excluded from ordered maturity comparison

package classification status remains distinct from genotype maturity

three independent package validations do not establish
mixed_corpus_exercised = true
```

### 16.6 Exit Criteria

```text
single-package smoke validates

all three package classifications validate independently

one corpus-level evaluation consumes the declared three-package set

three-TEP mixed-producer proof corpus validates at the claimed applicable-package
maturity floor

TEP-GSC packages pass genotype scope classification using
genotype_maturity_not_applicable rather than legacy, failed, or
genotype_discovered status

mixed-corpus summaries calculate an ordered maturity floor only across
genotype-applicable packages

mixed_corpus_exercised = true is supported by a corpus-level receipt

later five-TEP mixed-corpus expansion remains compatible with the same
producer-neutral classification model

summary receipts state package-level and corpus-level maturity honestly
```

---

## 17. Validation Receipt Matrix

### 17.1 Package-Level Genotype Maturity Receipts

| Package State | Required Receipt Families |
|---|---|
| `genotype_discovered` | `genotype_package_classification_receipt`; `genotype_artifact_set_validation_receipt` for every genotype-applicable package, including validation of complete modern availability or complete legacy absence |
| `genotype_maturity_not_applicable` | `genotype_package_classification_receipt` proving the required not-applicable applicability, capability, and maturity pairing |
| `genotype_preservation_validated` | `source_genotype_observation_preservation_receipt`; `genotype_identity_preservation_receipt`; `genotype_count_reconciliation_receipt`; lower-tier applicable-package receipts |
| `genotype_direct_relationships_registered` | `relationship_partition_validation_receipt`; `direct_relationship_registration_receipt`; lower-tier applicable-package receipts |
| `genotype_complex_relationships_preserved` | `relationship_partition_validation_receipt`; `complex_relationship_preservation_receipt`; lower-tier applicable-package receipts |
| `genotype_brokerage_evaluated` | `brokerage_receipt_validation_receipt`; `derived_relationship_validation_receipt`; `spanning_deletion_validation_receipt`; lower-tier applicable-package receipts |
| `genotype_assertion_ready` | `declaration_set_validation_receipt`; `anti_overclaim_validation_receipt`; lower-tier applicable-package receipts |
| `genotype_topology_ready` | `topology_substrate_validation_receipt`; `topology_relationship_basis_validation_receipt`; `anti_collapse_validation_receipt`; `anti_overclaim_validation_receipt`; lower-tier applicable-package receipts |
| `genotype_projection_ready` | deferred to projection-specific validation |

For a modern genotype-capable TEP-VAP package, the artifact-set receipt must
validate complete and coherent genotype artifact availability.

For a legacy variant-only TEP-VAP package, the artifact-set receipt must validate
complete genotype artifact-set absence and must prove that no partial genotype
artifact set was misclassified as legacy.

A genotype-not-applicable producer package does not require a genotype
artifact-set validation receipt merely to establish
`genotype_maturity_not_applicable`; its package-classification receipt must
instead validate the explicit not-applicable artifact-set state.

`genotype_maturity_not_applicable` is not a lower-tier prerequisite for any
genotype-applicable maturity state.

For trusted modern genotype-capable TEP-VAP ingestion, execution provenance
context validation is required before row-level trusted genotype preservation
may be claimed.

`execution_provenance_context_validation_receipt` is therefore required before
advancing from `genotype_discovered` into
`genotype_preservation_validated`.

No package-level maturity state may be claimed without its corresponding
receipt families passing.

### 17.2 Corpus-Level Receipt

The corpus-level receipt is:

```text
mixed_corpus_genotype_scope_receipt
```

It is not a prerequisite for assigning one package's Stage 1 maturity state.

It is required to claim:

```text
mixed_corpus_exercised = true
```

The receipt must calculate an ordered maturity floor only across
genotype-applicable packages.

It must report genotype-not-applicable packages separately.

---

## 18. Testing Strategy

Testing should be layered.

### 18.1 Unit Tests

Unit tests should cover:

```text
artifact discovery

capability classification

producer type classification

projection summary parsing

source-header context parsing

execution provenance context registration

genotype observation row preservation

relationship input routing

direct relationship registration

complex relationship preservation

brokerage receipt generation

derived relationship state validation

declaration-set generation

topology member and basis generation
```

### 18.2 Fixture Tests

Fixture tests should include:

```text
complete modern genotype-capable TEP-VAP fixture

partial genotype artifact set fixture

legacy variant-only fixture

TEP-GSC genotype-not-applicable fixture using:

    genotype_capability_not_applicable

    genotype_maturity_not_applicable

invalid capability/applicability pairing fixtures

invalid maturity/applicability pairing fixtures

undeclared producer-family fixture

direct relationship fixture

complex multiallelic relationship fixture

spanning-deletion fixture

unsupported genotype version fixture
```

### 18.3 Corpus Tests

Corpus tests should include:

```text
single modern TEP-VAP smoke

three-TEP mixed-producer proof corpus:
    one modern genotype-capable TEP-VAP
    two phenotype-scoped TEP-GSCs

later five-TEP mixed-corpus expansion
```

### 18.4 Negative Tests

Negative tests should prove VDB fails or quarantines when:

```text
genotype artifacts are partial

execution provenance is missing in trusted modern genotype ingestion

checksums fail

row counts fail

source identity is unrecoverable

genotype_observation_id is rewritten

producer rows are split

complex rows are silently promoted to direct

execution provenance is misclassified as biological evidence

TEP-GSC is assigned genotype_discovered

TEP-VAP is assigned genotype_maturity_not_applicable

an undeclared producer family silently inherits VAP or GSC classification rules

inheritance claims are emitted inside VDB
```

---

## 19. Non-Goals

This plan does not implement or plan:

```text
RDGP reasoning

inheritance model evaluation

compound heterozygosity calling

de novo inference

clinical diagnosis

pathogenicity classification

final symbolic ALT resolution

final spanning-deletion biological interpretation

projection-surface schemas

TEP-VDB emission format

performance optimization for the 144 WES corpus

public API design
```

These may be addressed by later documents after genotype preservation,
brokerage, declaration, and topology readiness are validated.

---

## 20. Exit Criteria for This Plan

This implementation plan is complete when VDB can demonstrate:

```text
1. genotype capability classification is implemented

2. genotype artifact and context indexes are implemented

3. trusted modern execution provenance context is required and registered

4. source genotype observations are preserved without loss or mutation

5. direct producer relationships are registered

6. complex relationships are preserved and routed safely

7. brokerage-required rows have receipts or explicit not-evaluated /
   policy-unavailable states

8. derived relationships remain topology and not producer evidence

9. genotype declaration sets are non-interpretive

10. genotype topology members and basis rows are typed, traceable,
    source-preserving, policy-declared where derived, and non-interpretive

11. mixed-corpus validation distinguishes TEP-VAP genotype applicability from
    TEP-GSC genotype-not-applicable status

12. TEP-GSC packages use `genotype_maturity_not_applicable` and are not assigned
    `genotype_discovered`

13. genotype-applicable packages do not use
    `genotype_maturity_not_applicable`

14. package classification completion remains distinct from genotype maturity

15. corpus maturity floors are calculated only across genotype-applicable
    packages

16. `mixed_corpus_exercised = true` requires a corpus-level validation receipt

17. no VDB layer emits inheritance reasoning
```

---

## 21. Relationship to Future Projection Work

This plan intentionally defers:

```text
genotype_projection_ready
```

Projection readiness should be governed by later projection-surface documents.

Future projection work may define:

```text
variant-only surfaces

genotype-aware surfaces

genotype-stratified surfaces

inheritance-readiness-aware surfaces

RDGP-facing TEP-VDB surfaces
```

Projection work must preserve the genotype evidence contract.

Projection work must not erase the distinction between producer genotype
observations and VDB-derived relationship topology.

---

## 22. Final Doctrine

The genotype evidence implementation plan is staged, receipt-gated, and
maturity-tiered.

VDB must not claim a genotype-applicable maturity tier before its validation
receipts pass.

VDB must represent genotype-not-applicable producer packages with
`genotype_maturity_not_applicable`, not `genotype_discovered`.

VDB must keep package classification completion distinct from genotype maturity.

VDB must preserve before it brokers.

VDB must route before it resolves.

VDB must register direct producer relationships separately from VDB-derived
relationships.

VDB must preserve complex source states before brokerage.

VDB must create receipts for brokerage outcomes.

VDB must keep declarations and topology non-interpretive.

VDB must defer RDGP reasoning.

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.

Scientists and clinicians interpret evaluated evidence.
```

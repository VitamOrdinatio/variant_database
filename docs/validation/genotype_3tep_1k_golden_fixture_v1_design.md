# Genotype 3TEP 1K Golden Fixture v1 Design

**Status:** design draft  
**Intended path:** `docs/validation/genotype_3tep_1k_golden_fixture_v1_design.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** Design and promotion criteria for a representative, deterministic, real-substrate three-package integration fixture containing one 1,000-row TEP-VAP derivative and two complete TEP-GSC packages  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Validation parent:** `docs/validation/genotype_evidence_preservation_validation.md`  
**Implementation-plan parent:** `docs/plans/genotype_evidence/genotype_evidence_plan.md`  

---

## 1. Purpose

This document defines how VDB should construct, validate, promote, version, and
use the first genotype-aware mixed-producer golden integration fixture.

The fixture is intended to carry a bounded but representative real producer
substrate through the complete VDB pathway:

```text
package discovery
    ↓
source observation preservation
    ↓
relationship routing and registration
    ↓
relationship brokerage
    ↓
Assertion Records
    ↓
Evidence Topology
    ↓
projection implementation and validation
```

The fixture contains three producer packages:

```text
one ERR10619300-derived TEP-VAP validation fixture
    containing exactly 1,000 deterministically selected genotype observations

two complete phenotype-scoped TEP-GSC packages
    epilepsy
    mitochondrial disease
```

The central design doctrine is:

```text
A source-order first-1,000-row smoke test proves bounded persistence mechanics.
It does not constitute the representative 3TEP_1K golden fixture.
```

---

## 2. Terminology

VDB must distinguish four substrates.

### 2.1 First-1K smoke substrate

```text
genotype_3tep_first1k_smoke_v1
```

The first-1K smoke substrate uses the first 1,000 genotype-observation rows in
producer source order.

Its purpose is to prove:

```text
schema creation
bounded streaming
batch persistence
ordered raw-value reconstruction
source identity retention
count reconciliation
read-only validation behavior
```

It is not selected for biological or structural representativeness.

It must never be called a candidate fixture, golden fixture, or production
proof.

### 2.2 Representative candidate fixture

```text
genotype_3tep_1k_candidate_v1
```

The candidate fixture contains exactly 1,000 unique ERR10619300 genotype
observations selected from the complete certified producer artifact by a
versioned, deterministic, coverage-balanced selection policy.

Candidate membership is frozen while the candidate is exercised through the
intended end-to-end pathway.

A candidate may be revised before golden promotion when a documented fixture
coverage defect is discovered.

### 2.3 Golden fixture

```text
genotype_3tep_1k_golden_v1
```

The golden fixture is the exact candidate membership that has passed all
required fixture-level validation gates.

Golden promotion changes fixture status. It does not change row membership,
producer identities, source hashes, or package bytes.

A promoted golden version is immutable.

### 2.4 Full three-TEP proof

```text
genotype_3tep_full_v1
```

The full proof contains:

```text
all 736,508 ERR10619300 genotype observations
complete epilepsy TEP-GSC
complete mitochondrial-disease TEP-GSC
```

The full proof is executed only after the golden 1K fixture clears the intended
end-to-end pathway.

---

## 3. Current First-1K Smoke Classification

The current bounded preservation run selected source rows `1..1000` from:

```text
source_tep_id:
    vap_tep_ERR10619300_run_2026_07_14_114546_v1

source_declared_genotype_row_count:
    736508

row_selection_policy:
    source_row_order_first_n
```

That run is valid evidence for preservation mechanics.

It must be retained or cited only under explicit first-1K smoke terminology:

```text
first-1K source-order smoke
bounded preservation engineering proof
non-representative smoke substrate
```

It must not be used as the basis for:

```text
golden-fixture coverage claims
relationship-class coverage claims
brokerage representativeness claims
Assertion Record representativeness claims
Evidence Topology representativeness claims
projection representativeness claims
```

---

## 4. Fixture Composition

The candidate and golden corpus each contain exactly three package members.

### 4.1 TEP-VAP fixture derivative

The VAP member is derived from the certified ERR10619300 producer package.

It contains exactly 1,000 selected genotype observations plus the minimum
complete producer context required for VDB ingestion, validation, lineage
reconstruction, and downstream processing.

The materialized fixture must be explicitly identified as a validation fixture
derivative.

It must not reuse the production package identity as though its bytes were the
original complete producer package.

Required identity layering:

```text
fixture_corpus_id
fixture_package_id
fixture_tep_id
source_package_id
source_tep_id
source_genotype_artifact_sha256
selection_manifest_sha256
```

Original producer observation identities must remain unchanged:

```text
genotype_observation_id
source_record_hash
source_record_ordinal
source_line_number
variant_id
variant_observation_id
sample_id
run_id
```

### 4.2 TEP-GSC members

The epilepsy and mitochondrial-disease TEP-GSC packages remain complete.

The `1K` qualifier applies only to the VAP genotype-observation membership. It
does not imply truncation of either GSC package.

The GSC members retain:

```text
genotype applicability:
    genotype_not_applicable_to_producer_type

genotype capability:
    genotype_capability_not_applicable

genotype maturity:
    genotype_maturity_not_applicable
```

They remain first-class mixed-corpus members and rejoin the common VDB pathway
at Assertion Records, Evidence Topology, and projection surfaces.

---

## 5. Selection Objectives

The candidate must balance five objectives.

### 5.1 Real producer fidelity

All selected rows must originate unchanged from the certified ERR10619300
producer genotype artifact.

No synthetic row may enter the real candidate membership.

### 5.2 Determinism

The same source artifact, selection policy version, and selection seed must
produce the same 1,000-row membership and manifest.

### 5.3 Coverage balance

The candidate should expose common paths and architecturally important rare
paths that exist in the source substrate.

It should not be a purely proportional sample that omits rare structural
classes, and it should not be a hand-picked collection that loses a defensible
selection model.

### 5.4 Bounded runtime and storage

The materialized fixture must remain small enough for repeated local execution,
CI-grade validation where practical, manual inspection, and durable retention.

### 5.5 End-to-end stability

Candidate membership should remain stable while downstream implementation is
built. Failures should normally trigger code, schema, policy, or provenance
repairs—not silent row reselection.

---

## 6. Full-Artifact Profiling Gate

VDB must profile the complete 736,508-row genotype artifact before defining
selection quotas.

The profiler must be read-only and streaming.

The profile should measure dimensions supported by the producer columns,
including:

```text
variant_relationship_status
relationship_reason
relationship_resolution_target

called genotype state
    heterozygous
    homozygous alternate
    homozygous reference where represented
    partial call
    no-call
    missing

alternate-allele cardinality
    biallelic
    multiallelic

variant class where derivable without interpretation
    SNV
    insertion
    deletion
    mixed or complex
    symbolic ALT
    spanning deletion

variant identity state
    variant_id present
    variant_id absent
    variant_observation_id present
    brokerage required

record_parse_status
record_preservation_status
filter state where available
chromosome distribution
depth and genotype-quality bins where available
```

The profile must also report joint strata needed by downstream relationship
routing, particularly:

```text
variant_relationship_status
    × called genotype state
    × alternate-allele cardinality
```

No fixed quota should be declared before the source profile is reviewed.

---

## 7. Selection Method

The v1 candidate should use deterministic coverage-balanced stratified
selection.

### 7.1 Selection sequence

```text
1. Verify the certified source TEP and genotype artifact hashes.

2. Stream-profile the complete genotype artifact.

3. Define observed primary strata and rare coverage obligations.

4. Reserve minimum rows for architecturally important observed classes.

5. Allocate remaining capacity across common primary strata using declared
   proportional or capped-proportional rules.

6. Rank rows within each stratum by a stable hash over immutable producer
   identity and the declared selection seed.

7. Resolve overlapping coverage obligations deterministically.

8. Fill any remaining capacity using the same stable ranking policy.

9. Emit exactly 1,000 unique selected genotype_observation_id values.

10. Emit and validate the complete selection manifest.
```

### 7.2 Stable ranking key

The ranking key should be derived from immutable producer identity, for example:

```text
sha256(
    selection_policy_version
    + selection_seed
    + source_genotype_artifact_sha256
    + genotype_observation_id
    + source_record_hash
)
```

The policy must specify exact delimiter and encoding behavior.

### 7.3 Rare-class handling

Minimum coverage may be reserved for observed classes such as:

```text
complex relationships
unresolved relationships
multiallelic records
missing direct variant identity
no-call and partial-call states
filtered or conservatively preserved states
symbolic alleles
spanning-deletion contexts
normalization or brokerage ambiguity
```

A class absent from the certified source artifact must be recorded as absent.
It must not be synthesized into the real fixture.

Synthetic fixtures remain responsible for exhaustive branch and failure-state
coverage.

---

## 8. Selection Manifest

The candidate must be manifest-driven.

The manifest is the authority for row membership.

Required corpus-level fields:

```text
schema_version
fixture_corpus_id
fixture_status
selection_policy_version
selection_seed
created_utc
source_tep_id
source_package_id
source_genotype_artifact_path
source_genotype_artifact_sha256
source_declared_row_count
selected_row_count
selection_manifest_sha256
```

Required row-level fields:

```text
selection_ordinal
source_row_number
genotype_observation_id
source_record_hash
source_record_ordinal
source_line_number
primary_selection_stratum
coverage_tags
selection_reason
stable_rank_hash
```

The manifest must prove:

```text
exactly 1000 rows
1000 unique genotype_observation_id values
1000 unique selection ordinals
all selected rows exist in the certified source artifact
all recorded source hashes reconcile
no row falls outside the declared selection policy
```

The selection manifest must be versioned and checksummed before fixture
materialization.

---

## 9. Materialized Fixture Requirements

The materialized VAP fixture derivative must preserve a complete, internally
coherent validation package shape.

At minimum it should include or deterministically regenerate:

```text
entity inventory
lineage manifest
validation report
1,000-row genotype observation artifact
genotype projection summary
genotype source-header context
execution provenance
selection manifest
fixture derivation manifest
```

All package counts and checksums must describe the fixture derivative rather
than falsely retaining full-package counts.

The fixture must retain explicit lineage to the production source:

```text
production TEP-VAP
    ↓ deterministic selection manifest
fixture TEP-VAP derivative
```

The fixture must never be represented as a clinical or production patient
result.

---

## 10. Candidate Validation Gates

Before end-to-end use, the candidate must pass:

```text
source identity validation
selection-policy validation
selection-manifest validation
fixture-package integrity validation
count reconciliation
checksum reconciliation
column reconstruction validation
producer observation identity preservation
relationship-status coverage audit
called-genotype coverage audit
allele-cardinality coverage audit
rare-class obligation audit
no-synthetic-row validation
```

Candidate preservation validation must additionally prove:

```text
selected rows = 1000
persisted rows = 1000
unique producer observation IDs = 1000
all producer columns reconstructable
source-order identity retained independently of fixture selection order
no producer observation split
no inheritance interpretation emitted
```

---

## 11. End-to-End Candidate Use

The exact candidate membership should be carried through each implementation
layer.

```text
discovery
preservation
relationship routing
direct relationship registration
complex relationship preservation
brokerage evaluation
Assertion Records
Evidence Topology
projection implementation
```

A downstream failure must be classified before fixture membership changes.

Preferred response order:

```text
1. investigate source provenance
2. investigate fixture materialization
3. investigate schema or implementation
4. investigate validation policy
5. revise candidate membership only when a documented coverage defect exists
```

Candidate reselection is not an acceptable substitute for repairing a pipeline
defect.

---

## 12. Golden Promotion Gate

The candidate may be promoted to `genotype_3tep_1k_golden_v1` only when:

```text
candidate membership is frozen
all three package identities are bound by one corpus manifest
all required preservation receipts pass
all implemented relationship and brokerage receipts pass
Assertion Records are reconstructable and validated
Evidence Topology is reconstructable and validated
implemented projection surfaces pass their governing validation
fixture bytes and manifest hashes are recorded
no unresolved fixture-construction defect remains
```

Promotion must emit a signed or checksummed promotion receipt containing:

```text
candidate fixture ID
golden fixture ID
candidate manifest SHA-256
golden corpus manifest SHA-256
package identities
required receipt identities
promotion timestamp
promotion status
```

Golden promotion does not rerun selection.

---

## 13. Golden Immutability and Versioning

`genotype_3tep_1k_golden_v1` is immutable after promotion.

The following changes require a new golden version:

```text
row membership change
selection-policy change
source producer package change
source artifact hash change
fixture package schema incompatibility
required package member change
semantic correction that changes expected end-to-end outputs
```

A new version should use:

```text
genotype_3tep_1k_candidate_v2
    ↓ promotion
genotype_3tep_1k_golden_v2
```

Golden v1 remains available for historical reproducibility unless retention
policy explicitly retires it.

---

## 14. Relationship to Synthetic Fixtures

The real 3TEP 1K golden fixture is an integration fixture.

It is not expected to exhaust every malformed, impossible, or biologically
absent state.

Testing responsibilities are divided as follows:

```text
real representative 3TEP 1K fixture
    heterogeneous end-to-end integration
    realistic producer distributions
    durable regression outputs

small synthetic fixtures
    exhaustive branch coverage
    malformed inputs
    impossible pairings
    rare failure states
    deterministic negative controls
```

Synthetic rows must never be mixed into the real fixture without explicit
fixture-family separation.

---

## 15. Storage and Runtime Doctrine

Fixture construction should avoid unnecessary duplication of the full source
artifact.

The profiler and selector should stream the source once where practical.

The fixture should retain:

```text
selected source rows
required package context
selection and derivation manifests
checksums
validation receipts
```

It should not retain redundant full-source copies inside the fixture tree.

Before materialization, operators should record:

```text
df -h .
du -sh results/registration results/validation tests/fixtures
```

Runtime and storage telemetry should be emitted for:

```text
full-source profiling
candidate selection
fixture materialization
fixture registration
fixture validation
```

---

## 16. Recommended Path and Naming Model

Provisional paths:

```text
results/fixtures/genotype_3tep_1k_candidate_v1/
results/fixtures/genotype_3tep_1k_golden_v1/

results/registration/genotype_3tep_1k_candidate_v1/
results/validation/genotype_3tep_1k_candidate_v1/
```

Candidate materialization and validation should stabilize before a repository
retention location is finalized.

No generic `3tep_1k` path should be used without a lifecycle qualifier:

```text
first1k_smoke
candidate_v1
golden_v1
full_v1
```

---

## 17. Near-Term Implementation Sequence

```text
1. Reclassify the current first-1K code and outputs as first1k_smoke.

2. Retain the first-1K preservation receipt only as an engineering smoke proof.

3. Implement the read-only full-artifact profiler.

4. Review the observed ERR10619300 distribution.

5. Lock the v1 selection policy and rare-class obligations.

6. Emit genotype_3tep_1k_candidate_v1 selection manifest.

7. Materialize the fixture-specific TEP-VAP derivative.

8. Bind the VAP derivative and two complete TEP-GSC packages in one candidate
   corpus manifest.

9. Validate candidate discovery and preservation.

10. Carry the exact candidate through relationship, Assertion Record, topology,
    and projection implementation.

11. Promote the unchanged candidate to genotype_3tep_1k_golden_v1.

12. Replay the same implementation against genotype_3tep_full_v1.
```

---

## 18. Acceptance Criteria

This design is satisfied when VDB can demonstrate:

```text
the first-1K source-order smoke is unambiguously labeled and isolated

the representative candidate is selected deterministically from the complete
certified source artifact

the candidate contains exactly 1,000 unique real producer observations

the two GSC packages remain complete and genotype-not-applicable

candidate membership is manifest-bound and reproducible

fixture package identity is distinct from production package identity

all producer observation identities and raw values remain losslessly preserved

golden promotion changes status without changing membership

golden v1 is immutable and versioned

the full three-TEP proof is executed only after golden closure
```

---

## 19. Closing Principle

```text
The first-1K smoke proves that VDB can preserve a bounded source-order slice.

The 3TEP 1K candidate proves that VDB can carry a representative real mixed
corpus through its architecture.

The golden fixture proves that the exact bounded corpus has become a stable,
reproducible end-to-end regression authority.
```

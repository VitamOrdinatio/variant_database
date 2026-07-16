# Genotype as First-Class VDB Evidence Model

**Status:** architecture draft  
**Intended path:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** VDB evidence architecture for modern genotype-capable TEP-VAP ingestion  
**Primary upstream substrate:** genotype-aware TEP-VAP  
**Primary downstream consumer:** TEP-VDB / RDGP  

---

## 1. Purpose

This document defines the VDB architecture for treating genotype observations as
first-class evidence.

Modern TEP-VAP packages now emit genotype observations as a dedicated producer
evidence domain. VDB must therefore ingest, preserve, register, broker, assert,
and topologize genotype evidence from the beginning of the consumer path.

The purpose of this document is to establish the evidence model and authority
boundaries that downstream design, specification, schema, validation, contract,
implementation-plan, and code work must preserve.

This document is architectural.

It does not define:

```text
database schemas
SQL DDL
builder implementations
projection-surface schemas
RDGP reasoning rules
TEP-VDB emission formats
```

Those concerns belong to later documents.

---

## 2. Scope

This document applies to VDB ingestion and downstream handling of modern
genotype-capable TEP-VAP packages.

It governs how VDB should understand:

```text
variant identity
sample-specific variant observation
genotype observation
genotype-to-variant relationship
execution provenance context
```

It also defines how genotype evidence should enter:

```text
producer evidence intake
registration / preservation
source identity substrate
declaration substrates
Assertion Records
Evidence Topology
later geometry and projection surfaces
```

This document does not govern VAP producer implementation or RDGP reasoning
implementation.

---

## 3. Governing Doctrine

The ecosystem doctrine is:

```text
VAP preserves.

VDB brokers.

RDGP reasons.

Scientists and clinicians interpret evaluated evidence.
```

For genotype evidence, this becomes:

```text
VAP preserves authoritative genotype observations.

VDB registers genotype identities, preserves producer truth, brokers
genotype-to-variant relationships, and constructs non-interpretive topology.

RDGP reasons over VDB-emitted genotype-aware surfaces in combination with
additional governed evidence.
```

VDB must not collapse these responsibilities.

---

## 4. Architectural Thesis

Genotype is first-class VDB evidence.

Genotype is not:

```text
variant identity
sample-specific variant observation
annotation
prioritization
validation status
inheritance interpretation
diagnosis
```

The target VDB architecture is:

```text
variant identity
    +
sample-specific variant observation
    +
genotype observation
    +
genotype-to-variant relationship topology
    +
execution provenance context
```

These objects are related.

They are not interchangeable.

---

## 5. Evidence Object Model

### 5.1 Variant Identity

A `variant_identity` represents a coordinate / allele / normalization-aware
variant identity.

It answers:

```text
Which variant or allele is being referenced?
```

Variant identity is generally reusable across samples, runs, packages, and
corpora when identity brokerage supports such reuse.

VDB may create canonical variant identities.

Canonical identities are additive.

They must not replace producer identities.

---

### 5.2 Sample-Specific Variant Observation

A `sample_variant_observation` represents the observation that a variant was
observed in a particular sample, run, package, and source context.

It answers:

```text
Was this variant observed in this sample, run, and package?
```

This object is source- and sample-contextual.

It must remain distinct from reusable variant identity.

---

### 5.3 Genotype Observation

A `genotype_observation` represents caller-emitted, sample-specific genotype
evidence preserved by VAP.

It answers:

```text
What genotype or genotype-like call state did the caller emit for this
source VCF record and selected sample?
```

A genotype observation may preserve:

```text
GT
AD
DP
GQ
PL
FT
FORMAT
sample FORMAT value
phase notation
called allele indices
missingness state
no-call state
source record identity
source VCF identity
source VCF header identity
sample identity
run identity
reference build
relationship status
relationship reason
relationship resolution target
```

A genotype observation is producer evidence.

It must remain immutable with respect to producer-emitted values.

---

### 5.4 Genotype-to-Variant Relationship

A `genotype_to_variant_relationship` connects genotype evidence to variant or
allele identity.

Relationships may be:

```text
direct producer-declared relationships
VDB-derived allele-specific brokerage relationships
ambiguous relationships
unresolved relationships
not-evaluated relationships
```

A relationship is not the same object as the genotype observation.

For complex records, VDB may derive zero, one, or multiple relationship rows
from one genotype observation.

Those derived rows are topology.

They are not new producer genotype observations.

---

### 5.5 Execution Provenance Context

`execution_provenance_context` describes the computational substrate that
generated the producer evidence.

It may include:

```text
toolchain versions
annotation environment
reference resources
resource checksums
execution platform
provenance validation status
```

Execution provenance is first-class context.

It is not biological evidence.

It should support auditability, reproducibility, dependency tracking, and later
method-currency reasoning.

---

## 6. Core Non-Equivalences

VDB must preserve these distinctions:

```text
variant identity
    ≠ sample-specific variant observation

sample-specific variant observation
    ≠ genotype observation

genotype observation
    ≠ genotype-to-variant relationship

genotype-to-variant relationship
    ≠ inheritance interpretation

execution provenance
    ≠ biological evidence

source identity
    ≠ canonical identity

VDB-derived relationship topology
    ≠ producer genotype observation
```

These are scientific invariants, not implementation preferences.

---

## 7. Authority Boundaries

### 7.1 VAP Authority

VAP owns the producer truth for genotype observations.

VAP is authoritative for:

```text
genotype_observation_id
sample_id
run_id
source VCF identity
source VCF header identity
source record identity
raw FORMAT/sample evidence
called allele indices
direct versus complex relationship declaration
record preservation state
genotype projection summary
TEP-VAP transport
```

VAP may provide direct genotype-to-variant linkage when the relationship is
unambiguous under VAP policy.

VAP must not be assumed to have performed VDB identity brokerage.

---

### 7.2 VDB Authority

VDB owns consumer-side registration, persistence, identity brokerage,
relationship brokerage, topology construction, and consumer-safe projection.

VDB may:

```text
preserve genotype observations
register direct producer relationships
construct derived allele-specific relationships
assign canonical identities
record relationship states
record ambiguity and lossiness states
record normalization policy
record brokerage policy
emit genotype-aware topology
emit genotype-aware TEP-VDB surfaces
```

VDB must not:

```text
overwrite raw producer genotype values
replace genotype_observation_id
silently alter producer relationship status
represent one source genotype observation as multiple producer observations
collapse genotype into variant identity
infer inheritance mode
infer compound heterozygosity
infer de novo status
infer carrier status
infer disease causality
emit diagnosis
```

---

### 7.3 RDGP Authority

RDGP owns downstream biological reasoning over VDB-emitted surfaces.

RDGP may reason about:

```text
inheritance readiness
inheritance models
candidate gene prioritization
compound-heterozygosity candidates
biallelic-model compatibility
genotype-aware burden interpretation
```

RDGP reasoning results are downstream assertions.

They must not mutate VAP source truth or VDB brokerage topology.

---

## 8. Rejected Architecture: Variant / Genotype Collapse

VDB must not collapse variant identity and genotype state into one identity
object.

Unsafe examples include:

```text
chr15:89333596:T:TTGC:heterozygous

variant_identity_plus_gt_state

canonical_variant_id_with_zygosity_embedded
```

This collapse is unsafe because:

```text
the same variant may occur in different genotype states across samples

variant recurrence and genotype recurrence answer different questions

genotype quality and missingness should not contaminate allele identity

sample-specific call state is not reusable variant identity

RDGP needs typed evidence, not pre-entangled identifiers
```

Correct architecture:

```text
variant identity is separate

sample-specific variant observation is separate

genotype observation is separate

relationships connect them under policy
```

---

## 9. Rejected Architecture: Late Genotype Overlay

VDB must not treat genotype as a late decoration added only after
variant-centric Assertion Records, Evidence Topology, Convergence Geometry, and
projection surfaces have already been built.

The rejected model is:

```text
variant-centric ingestion
    → variant-centric Assertion Records
        → variant-centric Evidence Topology
            → variant-centric Convergence Geometry
                → genotype fields attached during final projection
```

This is insufficient because genotype cannot shape topology or geometry if it
enters only after those layers are constructed.

Late overlay prevents faithful representation of:

```text
genotype-informed Assertion Records
genotype relationship topology
genotype-stratified recurrence
genotype-readiness states
genotype missingness topology
multiallelic brokerage topology
phase / ploidy limitation states
```

Late overlay may be acceptable only as an explicitly labeled legacy
compatibility behavior for older variant-only TEP-VAP packages.

It is not the target architecture.

---

## 10. Target Architecture: Typed First-Class Genotype Evidence

The target architecture is a typed first-class genotype model.

In this architecture:

```text
variant identity is first-class

sample-specific variant observation is first-class

genotype observation is first-class

genotype-to-variant relationship topology is first-class

execution provenance context is first-class
```

These objects are equally important for preservation, but they do not share the
same semantic role.

VDB should preserve and relate them as distinct evidence objects.

Projection policies may later choose whether a surface is:

```text
variant-only
genotype-aware
genotype-stratified
inheritance-readiness-aware
```

No projection policy may erase the source distinction between producer
genotype observation and VDB-derived relationship topology.

---

## 10A. Genotype Maturity Boundaries

Genotype support in VDB is maturity-tiered.

VDB must not use `genotype-aware` as an undifferentiated claim.

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

These states are not equivalent.

A VDB build may preserve genotype observations before it can broker all complex
relationships.

A VDB build may broker genotype relationships before it can emit
projection-ready genotype surfaces.

A VDB build may be genotype-topology-ready before RDGP performs inheritance
reasoning.

The contract and implementation plan must state which maturity tier has been
achieved and validated.

---

## 11. Multiallelic Relationship Doctrine

Multiallelic genotype records demonstrate why genotype must be first-class but
separately typed.

A single source record may contain multiple alternate alleles:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

VAP preserves one source genotype observation for this source record.

VDB may derive relationships such as:

```text
genotype observation G
    → allele index 1 / source ALT C

genotype observation G
    → allele index 2 / source ALT G
```

Both derived relationships trace to the same authoritative source genotype
observation.

VDB must not create:

```text
synthetic producer genotype row for A>C
synthetic producer genotype row for A>G
```

The architectural invariant is:

```text
one genotype_observation_id
    may map to
zero or more VDB-derived genotype-to-variant relationships

but

multiple VDB-derived relationships
    must not imply
multiple producer genotype observations
```

---

## 12. Relationship State Doctrine

VDB must distinguish producer-direct relationships from VDB-derived
relationships.

Recommended architectural categories include:

```text
direct_source_biallelic
resolved_from_multiallelic_record
brokered_with_normalization
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

A relationship derived from a multiallelic source record may be resolved and
usable while still not being a direct source-biallelic relationship.

The distinction must survive ingestion, topology, projection, and RDGP-facing
surfaces.

---

## 13. Execution Provenance Boundary

Execution provenance is first-class VDB context.

It must be registered, preserved, and made available for auditability and later
method-currency reasoning.

Execution provenance may inform future surfaces such as:

```text
method currency
resource compatibility
reference-resource comparability
annotation environment comparison
pipeline reproducibility
```

But execution provenance must not be treated as:

```text
variant evidence
genotype evidence
pathogenicity evidence
phenotype evidence
reasoning evidence
```

The boundary is:

```text
execution provenance describes how evidence was generated

it does not itself assert biological state
```

---

## 14. VDB Phase Implications

### Phase 1 — Producer Evidence Intake

VDB must discover modern genotype-capable TEP-VAP packages.

Required discovery targets include:

```text
entity_inventory.json
lineage_manifest.json
validation_report.md
entities/genotype/genotype_observations.tsv
entities/genotype/genotype_projection_summary.json
entities/genotype/genotype_source_header_context.json
entities/context/execution_provenance.json
```

Phase 1 should determine whether genotype capability is available, absent, or
legacy-unavailable before any large-table ingestion begins.

---

### Phase 2 — Registration / Preservation

VDB must register genotype observations as source evidence.

Registration must preserve:

```text
row count
column names
schema version
genotype_observation_id
source VCF identity
source VCF header identity
source record identity
sample identity
run identity
reference build
raw FORMAT/sample evidence
called allele indices
relationship status
relationship reason
relationship resolution target
projection advisory codes
projection warning codes
```

No VDB-derived relationship may alter the registered producer object.

---

### Phase 4.1 — Source Identity / Package Substrate

VDB must preserve identity for:

```text
producer package
registration unit
sample
run
source VCF
source VCF header
source record
sample-specific variant observation
genotype observation
```

This identity substrate is required before genotype relationship brokerage can
be trustworthy.

---

### Phase 4.2 — Declaration Substrate

VDB must extend the declaration substrate to include genotype declarations
beside coordinate, feature, and metadata declarations.

The declaration substrate should support handles for:

```text
genotype observation set
genotype source record set
genotype relationship status set
genotype called allele index set
genotype FORMAT/sample field set
genotype provenance/context set
```

The exact schema belongs to later implementation documents.

---

### Phase 4.3 — Assertion Records

VDB Assertion Records should become genotype-informed.

Permitted non-interpretive assertion families include:

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

Invalid Assertion Record families include:

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

Those are downstream reasoning assertions, not VDB preservation assertions.

---

### Phase 4.4 — Evidence Topology

Evidence Topology should include genotype nodes and typed genotype
relationships.

Permitted topology relations include:

```text
sample_variant_observation has_genotype_observation

genotype_observation has_raw_genotype_field

genotype_observation has_called_allele_index

genotype_observation has_normalized_call_state

genotype_observation has_quality_state

genotype_observation has_phase_context

genotype_observation has_missingness_state

genotype_observation brokered_to_variant_identity

genotype_observation brokered_to_sample_variant_observation

genotype_observation relationship_unresolved

genotype_observation relationship_ambiguous
```

All topology edges must be:

```text
typed
non-interpretive
policy-declared
traceable
source-preserving
```

---

### Phase 4.5 and Later — Geometry and Projection Surfaces

After genotype-aware topology is stable, geometry and projection surfaces may
consume genotype evidence under declared policy.

Possible surface modes include:

```text
variant-only
genotype-aware
genotype-stratified
inheritance-readiness-aware
```

Examples of later genotype-aware geometry include:

```text
exact variant recurrence stratified by genotype state

patient-gene heterozygous-like count

patient-gene homozygous-alt-like count

genotype-missingness count

phase-availability count

relationship-state burden count

low-quality genotype burden partition
```

These are structural evidence features.

They are not inheritance conclusions.

Projection-surface details are deferred until genotype ingestion, relationship
brokerage, Assertion Records, and Evidence Topology are stable.

---

## 15. Legacy Compatibility Mode

Older TEP-VAP packages may not emit first-class genotype artifacts.

VDB may support them under explicit compatibility labels such as:

```text
variant_only_legacy_compatibility_mode

genotype_context_unavailable

genotype_not_emitted_by_source

genotype_projection_not_evaluated
```

VDB must not infer genotype for older packages.

VDB must not convert missing genotype artifacts into:

```text
homozygous reference
variant absence
callability
no-call
negative disease evidence
opportunity evidence
```

Legacy compatibility is acceptable for historical packages.

It is not the target architecture for modern genotype-capable TEP-VAPs.

---

## 16. Anti-Collapse Rules

VDB must enforce the following anti-collapse rules:

```text
variant identity ≠ sample-specific variant observation

sample-specific variant observation ≠ genotype observation

genotype observation ≠ genotype-to-variant relationship

source genotype observation ≠ allele-specific relationship

derived relationship ≠ producer genotype row

direct_source_biallelic ≠ resolved_from_multiallelic_record

genotype-to-variant relationship ≠ inheritance interpretation

heterozygous-like ≠ dominant-compatible

homozygous-alt-like ≠ recessive diagnosis

two heterozygous-like variants in one gene ≠ compound heterozygosity

phase missing ≠ phase in trans

ploidy unknown ≠ hemizygosity

genotype missing ≠ homozygous reference

no call ≠ absence

unresolved relationship ≠ evidence absence

missing variant identity ≠ missing genotype observation

allele depth annotation ≠ independent allele-specific AD vector

genotype-aware burden ≠ disease association

execution provenance ≠ biological evidence
```

These rules are required architecture constraints.

---

## 17. Success Criteria

This architecture is successful when VDB can demonstrate that:

```text
1. Modern TEP-VAP genotype artifacts are discovered as a complete artifact set.

2. Genotype observations are registered as first-class source evidence.

3. Raw genotype fields and source-record provenance remain recoverable.

4. Variant identity, sample-specific variant observation, and genotype
   observation remain separately typed.

5. Direct producer relationships remain distinguishable from VDB-derived
   brokerage relationships.

6. Complex multiallelic and spanning-deletion relationship states remain explicit.

7. VDB-derived relationship topology does not create producer genotype rows.

8. Genotype-informed Assertion Records are non-interpretive.

9. Genotype-informed Evidence Topology is typed, traceable, and policy-declared.

10. Execution provenance is registered as context, not biological evidence.

11. Legacy variant-only TEP-VAPs remain usable without inferred genotype.

12. No VDB layer emits inheritance conclusions unless they are preserved from an
    explicit external reasoning producer.
```

---

## 18. Relationship to Downstream Documents

This architecture should govern the following VDB-side documents:

```text
docs/design/genotype_evidence_ingestion_and_brokerage_design.md

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

The downstream documents define:

```text
how VDB will implement, validate, contract, and execute those truths
```

---

## 19. Final Doctrine

VDB must preserve genotype observations as first-class producer evidence and
construct genotype-to-variant relationships as additive, typed, traceable
topology.

VDB must not collapse genotype into variant identity.

VDB must not represent VDB-derived relationships as producer observations.

VDB must not infer inheritance.

The final boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.

Scientists and clinicians interpret evaluated evidence.
```

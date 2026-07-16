# Multiallelic Relationships: VDB Brokerage Policy

> Status: SAGE-VDB design policy draft.  
> Intended path: `docs/design/multiallelic_relationships_vdb_brokerage_policy.md`  
> Parent Truth Layer: `AI_Workspace/shared/repo_strategy/repo_ecosystem_multiallelic_relationships.md`  
> Upstream VAP derivative: `docs/design/multiallelic_relationships_vap_handling_policy.md`  
> Target audience: DEX-VDB  
> Repository: `variant_database`  
> Scope: VDB handling of multiallelic genotype-to-variant brokerage after TEP-VAP ingestion.  

---

# 1. Purpose

This document defines how VDB should consume source-preserved multiallelic genotype observations from TEP-VAP and construct allele-specific genotype-to-variant relationships without mutating producer truth or forcing RDGP to reconstruct VCF allele-index logic.

The core question is:

```text
How should VDB broker allele-specific relationships from source-record-scoped
multiallelic genotype observations while preserving the original genotype
observation as authoritative producer evidence?
```

This is a VDB brokerage policy, not a VAP producer policy and not an RDGP reasoning policy.

The governing ecosystem doctrine is:

```text
VAP preserves.
VDB brokers.
RDGP reasons.
```

---

# 2. Executive Doctrine

VDB should treat multiallelic genotype relationships as a first-class brokerage and topology problem.

The doctrine is:

```text
VDB preserves the original VAP genotype observation as source-faithful evidence.

VDB constructs allele-specific genotype-to-variant relationships as additive,
typed, policy-declared derived topology.

VDB does not create new producer genotype observations.

VDB does not collapse genotype observation into variant identity.

VDB does not perform inheritance interpretation.

VDB exposes registered relationships, ambiguity states, traceability, and
policy metadata so RDGP can reason without reparsing raw VCF FORMAT fields.
```

This policy exists because multiallelic genotype records are not producer errors. They are legitimate source-record structures that require downstream relationship brokerage.

For example:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

This source record contains one genotype observation that references two alternate allele indices.

VDB may derive relationships from that one genotype observation to the allele-specific identities for `A>C` and `A>G`.

VDB must not convert that one source genotype observation into two independent producer genotype observations.

---

# 3. Definition: Multiallelic Genotype Relationship

A multiallelic genotype relationship is the relationship between:

```text
one source-record-scoped genotype observation
```

and:

```text
one or more allele-specific variant identities or sample-specific variant
observations
```

when a single source variant record contains multiple alternate alleles and the genotype field references one or more of those allele indices.

Example:

```text
CHROM = chr1
POS   = 100
REF   = A
ALT   = C,G
GT    = 1/2
AD    = 2,4,9
```

In this record:

```text
allele index 0 = REF allele A
allele index 1 = first ALT allele C
allele index 2 = second ALT allele G
```

The genotype observation references allele indices `1` and `2`.

Therefore, VDB may derive:

```text
genotype observation G
    -> source ALT allele C / allele index 1
    -> source ALT allele G / allele index 2
```

But VDB must preserve that these relationships originate from the same source-record-scoped genotype observation.

---

# 4. VDB Responsibility Boundary

VDB owns identity brokerage, source preservation, derived relationship construction, topology exposure, and consumer-safe projection.

VDB may:

```text
register source genotype observations
preserve source record identity
preserve raw genotype / FORMAT evidence
map called allele indices to source ALT alleles
broker source ALT alleles to allele-specific variant identities
construct typed genotype-to-variant topology relationships
record relationship state, ambiguity, lossiness, and policy metadata
emit RDGP-facing relationship surfaces
```

VDB must not:

```text
create independent producer genotype rows from one multiallelic source record
mutate the original VAP genotype observation
collapse genotype observation into variant identity
collapse multiallelic-derived relationships into direct biallelic links
infer inheritance mode
infer compound heterozygosity
infer de novo status
infer diagnosis or disease causality
force RDGP to reconstruct VCF allele-index logic from raw FORMAT fields
```

The VDB boundary is:

```text
VDB brokers relationships.
RDGP interprets biological meaning.
```

---

# 5. Source Truth vs Derived Topology

VDB must preserve a strict distinction between source evidence and derived topology.

## Source truth

The source-truth object is the genotype observation emitted by VAP from the original source record.

It includes:

```text
genotype_observation_id
sample_id
run_id
source_package_id
source_record_hash
source_record_ref
source_record_alt
gt_raw
ad_raw
dp_raw
gq_raw
pl_raw
format_raw
sample_format_raw
called_allele_indices
relationship status emitted by VAP
```

This object remains authoritative for what the producer emitted.

## Derived topology

The derived topology objects are VDB-constructed allele-specific relationships.

They may include:

```text
genotype_variant_relationship_id
genotype_observation_id
allele_index
source_alt_allele
variant_identity_id
sample_variant_observation_id
relationship_state
relationship_derivation_policy_id
normalization_state
ambiguity_state
lossiness_state
traceability_refs
```

These objects are valid VDB topology artifacts, but they are not new producer genotype observations.

The core invariant is:

```text
source genotype observation ≠ derived allele-specific relationship
```

---

# 6. VDB Workflow Placement

Multiallelic relationship brokerage should be distributed across the VDB workflow, but relationship construction primarily belongs in Evidence Topology.

## Phase 1 — Producer Evidence Intake

VDB detects that TEP-VAP contains genotype observations and relationship-status fields.

Relevant incoming fields include:

```text
variant_relationship_status
relationship_reason
relationship_resolution_target
alternate_alleles_raw
alternate_allele_count
called_allele_indices
gt_raw
ad_raw
source_record_hash
```

Phase 1 should not resolve allele-specific relationships. It should recognize that genotype evidence exists and that some records require VDB brokerage.

## Phase 2 — Registration / Preservation

VDB registers the source genotype observation as preserved producer evidence.

Preserve:

```text
genotype_observation_id
sample_id
run_id
source_package_id
source_record_hash
source_record_ref
source_record_alt
raw GT / AD / DP / GQ / PL / FORMAT fields
called allele indices
relationship status from VAP
```

Phase 2 may record direct biallelic relationships emitted by VAP, but it should not perform complex multiallelic resolution.

## Phase 4.1 — Source Identity / Package Substrate

VDB preserves identity for:

```text
producer package
registration unit
sample
run
source VCF / header
source record
genotype observation
sample-specific variant observation
```

This substrate ensures multiallelic brokerage remains traceable to source packages and source records.

## Phase 4.2 — Coordinate / Feature / Metadata Declaration Substrate

VDB preserves coordinate, allele, genotype, and normalization declaration handles.

For multiallelic records, this includes:

```text
source allele list
allele index map
reference allele
alternate allele strings
normalization candidate state
variant identity registration state
```

## Phase 4.3 — Assertion Records

VDB creates non-interpretive genotype assertion records.

Examples:

```text
genotype_observation_preserved
genotype_observation_has_called_allele_index
genotype_observation_has_raw_ad_vector
genotype_observation_requires_vdb_brokerage
genotype_observation_has_complex_multiallelic_relationship
```

Phase 4.3 may assert:

```text
genotype observation G references called allele indices 1,2
```

But it should not assert:

```text
genotype observation G has fully resolved allele-specific relationships
```

unless VDB identity mapping and relationship brokerage have actually completed under policy.

## Phase 4.4 — Evidence Topology

Phase 4.4 is the primary resolution layer.

VDB constructs typed topology edges such as:

```text
genotype_observation_resolved_to_alt_allele
genotype_observation_brokered_to_variant_identity
genotype_observation_brokered_to_sample_variant_observation
genotype_observation_relationship_unresolved
genotype_observation_relationship_ambiguous
```

Every edge must carry:

```text
relation_type
participant_roles
source genotype observation reference
source record reference
allele index
source ALT allele
construction policy
normalization policy
ambiguity state
lossiness state
traceability references
```

## Phase 4.5+ — Geometry and Surfaces

Once topology exists, VDB surfaces may consume it.

Examples:

```text
GIRS:
    genotype relationship readiness

EVRS:
    exact variant recurrence stratified by relationship state

PGERS:
    patient-gene genotype-state summaries

KVPS:
    known pathogenicity evidence with genotype relationship context

OACS:
    no-call / missing / unavailable relationship context

CUES:
    ambiguous or unresolved genotype relationship events

RMCS:
    multiallelic relationship policy version and currency
```

---

# 7. Required VAP Inputs

VDB depends on VAP preserving enough information to perform deterministic brokerage.

Minimum expected VAP inputs include:

```text
genotype_observation_id
sample_id
run_id
source_package_id
reference_build
chromosome
position
reference_allele
alternate_alleles_raw
alternate_allele_count
is_multiallelic
called_allele_indices
variant_relationship_status
relationship_reason
relationship_resolution_target
source_vcf_sha256
source_vcf_header_hash
source_record_ordinal
source_record_hash
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

For multiallelic records, VDB expects VAP to preserve the source record and indicate that relationship construction is delegated to VDB.

Preferred VAP handoff state:

```text
relationship_resolution_target = vdb_brokerage
```

Preferred VAP relationship reason:

```text
relationship_reason = multiallelic_source_record
```

---

# 8. Brokerage Policy

For each source genotype observation requiring brokerage, VDB should follow a declared multiallelic relationship policy.

Recommended policy sequence:

```text
1. Read the source genotype observation.
2. Confirm source record identity and preservation state.
3. Parse called allele indices from the preserved genotype state.
4. Confirm allele indices are within the source allele list.
5. Map each called non-reference allele index to a source ALT allele.
6. Construct an allele-specific source allele candidate:
       chromosome, position, reference, source_alt_i, reference_build
7. Apply declared variant normalization policy if required.
8. Match or register allele-specific variant identity.
9. Link the genotype observation to the allele-specific variant identity or
   sample-specific variant observation if mapping is unambiguous.
10. Emit ambiguous or unresolved relationship state if mapping is not safe.
11. Preserve relationship derivation policy, ambiguity, lossiness, and traceability.
```

Required policy identifiers:

```text
multiallelic_relationship_policy_id
variant_normalization_policy_id
allele_index_mapping_policy_id
symbolic_alt_policy_id
spanning_deletion_policy_id
lossiness_policy_id
identity_registration_policy_id
```

No normalization, splitting, trimming, left-alignment, symbolic handling, or spanning-deletion handling should occur silently.

---

# 9. Canonical Example

Input source record:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

VAP emits one genotype observation:

```text
genotype_observation_id = G1
source_record_ref = A
source_record_alt = C,G
gt_raw = 1/2
ad_raw = 2,4,9
called_allele_indices = 1,2
variant_relationship_status = complex
relationship_reason = multiallelic_source_record
relationship_resolution_target = vdb_brokerage
```

VDB preserves `G1` as the authoritative source genotype observation.

VDB may construct two derived relationships:

```text
relationship R1:
    genotype_observation_id = G1
    allele_index = 1
    source_alt_allele = C
    allele_depth = 4
    relationship_state = resolved_from_multiallelic_record

relationship R2:
    genotype_observation_id = G1
    allele_index = 2
    source_alt_allele = G
    allele_depth = 9
    relationship_state = resolved_from_multiallelic_record
```

Both relationships point back to the same source genotype observation and source record.

VDB must not emit:

```text
synthetic producer genotype row for A>C
synthetic producer genotype row for A>G
```

The authoritative source AD vector remains:

```text
AD = 2,4,9
```

The per-allele depth values are relationship annotations derived from allele-index mapping, not independent producer AD vectors.

---

# 10. Relationship State Model

VDB should use relationship states that distinguish source-direct, resolved-derived, brokered, ambiguous, unresolved, and not-evaluated cases.

Recommended VDB relationship states:

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

Core rule:

```text
resolved_from_multiallelic_record must not collapse to direct_source_biallelic.
```

A relationship derived from a multiallelic record can be resolved and unambiguous while still not being source-direct.

The distinction matters because downstream consumers must know whether an allele-specific relationship was emitted directly by the producer or brokered by VDB.

---

# 11. Relationship Confidence, Ambiguity, and Lossiness Axes

VDB should not overload a single relationship state field with all confidence semantics.

Use separate axes where possible:

```text
relationship_state
ambiguity_state
lossiness_state
normalization_state
identity_registration_state
traceability_state
```

Example resolved lossless relationship:

```text
relationship_state = resolved_from_multiallelic_record
ambiguity_state = unambiguous
lossiness_state = lossless_allele_index_mapping
normalization_state = no_normalization_required
identity_registration_state = variant_identity_registered
traceability_state = source_trace_complete
```

Example normalization-mediated relationship:

```text
relationship_state = brokered_with_normalization
ambiguity_state = unambiguous
lossiness_state = lossless_normalized_mapping
normalization_state = nontrivial_normalization
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

---

# 12. Depth and FORMAT Semantics

VDB must preserve record-level FORMAT semantics while exposing safe relationship-level annotations.

For:

```text
REF = A
ALT = C,G
GT  = 1/2
AD  = 2,4,9
```

VDB should preserve:

```text
source_ad_raw = 2,4,9
ref_depth = 2
```

VDB may derive:

```text
relationship_to_C:
    allele_index = 1
    source_alt_allele = C
    allele_depth = 4

relationship_to_G:
    allele_index = 2
    source_alt_allele = G
    allele_depth = 9
```

VDB must not claim:

```text
A>C has independent producer AD = 2,4
A>G has independent producer AD = 2,9
```

Pairwise depth annotations may be useful, but the source AD vector remains authoritative.

This caution is especially important for fields like `PL`, which may encode genotype-combination likelihoods rather than independent allele-level quantities.

Required FORMAT handling rules:

```text
raw FORMAT/sample values remain preserved
record-level vectors remain record-level evidence
allele-index-derived annotations must cite source index and vector position
missing AD or malformed AD must not block preservation of genotype observation
relationship-level depth must carry availability / validity state
```

Recommended depth availability states:

```text
allele_depth_available
allele_depth_missing
allele_depth_vector_length_mismatch
allele_depth_not_applicable
allele_depth_unparseable
```

---

# 13. Normalization and Identity Brokerage

VDB owns variant identity brokerage for allele-specific relationships.

For each called allele index, VDB should:

```text
1. Resolve the source ALT allele by index.
2. Construct source allele candidate:
       chromosome, position, reference, alt_i, reference_build
3. Apply declared variant normalization policy if required.
4. Attempt to match or register allele-specific variant identity.
5. Construct derived relationship if mapping is unambiguous.
6. Emit unresolved or ambiguous relationship state otherwise.
```

VDB should record:

```text
source_allele_candidate_id
normalized_variant_identity_id
variant_normalization_policy_id
normalization_state
normalization_lossiness_state
identity_registration_state
```

Recommended normalization states:

```text
no_normalization_required
normalized_losslessly
normalized_with_left_alignment
normalized_with_trimming
normalization_ambiguous
normalization_policy_unavailable
normalization_failed
not_evaluated
```

VDB must not silently convert a complex source allele into a normalized variant identity without retaining source coordinates, source alleles, policy, and traceability.

---

# 14. Ambiguity and Failure Policy

VDB should preserve source observations even when relationship brokerage fails.

A failed or unresolved relationship is not equivalent to missing genotype evidence.

## Called allele index exceeds ALT count

Example:

```text
ALT = C,G
GT = 1/3
```

VDB should not construct an allele-specific edge for index `3`.

Recommended state:

```text
relationship_state = unresolved_allele_index_out_of_range
cues_event = genotype_relationship_invalid_allele_index
```

## Symbolic ALT

Example:

```text
ALT = <DEL>
```

Resolve only if a declared symbolic-variant brokerage policy exists.

Otherwise:

```text
relationship_state = unresolved_symbolic_alt
```

## Spanning deletion

Example:

```text
ALT = *
```

Do not treat as an ordinary SNV/indel allele.

Recommended state:

```text
relationship_state = unresolved_spanning_deletion
```

or:

```text
relationship_state = spanning_deletion_context_required
```

## Mixed or malformed GT

If VAP classified the GT as malformed, VDB should preserve the genotype observation and avoid relationship resolution unless a declared recovery policy exists.

Recommended state:

```text
relationship_state = unresolved_malformed_gt
```

## Normalization ambiguity

If a source ALT allele cannot be mapped safely to one allele-specific identity:

```text
relationship_state = unresolved_normalization_ambiguous
```

If normalization succeeds but requires explicit caveats:

```text
relationship_state = brokered_with_normalization
ambiguity_state = unambiguous
lossiness_state = lossless_normalized_mapping
```

## Missing allele-specific variant identity

If the source allele is valid but the corresponding allele-specific variant identity is not yet registered:

```text
relationship_state = unresolved_missing_variant_identity
identity_registration_state = missing
```

The source genotype observation remains preserved and may become resolvable after identity registration improves.

---

# 15. RDGP-Facing Minimum Relationship Surface

RDGP should not be forced to reconstruct VCF allele-index logic from raw FORMAT fields.

VDB should emit a consumer-safe relationship surface or equivalent TEP-VDB component.

Suggested name:

```text
genotype_variant_relationship_surface
```

Minimum fields:

```text
genotype_variant_relationship_id
genotype_observation_id
sample_id
run_id
source_package_id
source_record_hash
reference_build
chromosome
position
source_record_ref
source_record_alt
allele_index
source_alt_allele
variant_identity_id
sample_variant_observation_id
called_in_gt
gt_raw
gt_separator
phase_state
genotype_call_state
ad_raw
ref_depth
allele_depth
allele_depth_state
dp_raw
gq_raw
pl_raw
relationship_type
relationship_state
relationship_derivation_policy_id
variant_normalization_policy_id
normalization_state
ambiguity_state
lossiness_state
identity_registration_state
traceability_refs
cues_event_refs
rmcs_policy_refs
anti_overclaim_label
```

## Cardinality Invariant

A single source genotype observation may produce zero, one, or multiple
VDB-derived genotype-to-variant relationship rows.

This cardinality reflects relationship topology, not producer row count.

Required invariant:

```text
one genotype_observation_id
    may map to
zero or more genotype_variant_relationship_id values
```

But: 

```text
multiple genotype_variant_relationship_id values
    must not imply
multiple producer genotype observations
```

Every relationship row derived from the same source record must preserve the
same `genotype_observation_id` and `source_record_hash`.

## Anti-Overclaim Label

Required anti-overclaim label:

```text
genotype_relationship_not_inheritance_interpretation
```

## Optional Additional Labels

Optional additional labels:

```text
multiallelic_relationship_not_independent_producer_row
allele_depth_annotation_not_independent_ad_vector
resolved_relationship_not_direct_source_biallelic
```

This surface allows RDGP to reason over registered relationships without reparsing raw VCF FORMAT fields or duplicating VDB identity brokerage logic.

---

# 16. Projection Surface Integration

Multiallelic brokerage relationships should integrate with the broader TEP-VDB projection surface family.

## GIRS

GIRS is the primary consumer of genotype relationship topology.

It should expose:

```text
relationship_ready
relationship_complex_resolved
relationship_complex_unresolved
relationship_ambiguous
relationship_not_evaluated
```

GIRS may summarize genotype-readiness, but it must not infer inheritance mode.

## EVRS

EVRS may stratify exact recurrence by relationship state:

```text
direct_source_biallelic
resolved_from_multiallelic_record
brokered_with_normalization
ambiguous
unresolved
```

EVRS must not treat relationship resolution as causality.

## PGERS

PGERS may include patient-gene or patient-locus summaries of resolved, ambiguous, and unresolved genotype-to-variant relationships.

PGERS must preserve relationship-state counts and not flatten unresolved multiallelic relationships into absence.

## KVPS

KVPS may attach known pathogenicity evidence to allele-specific variant identities while preserving that the genotype relationship may have been derived from a multiallelic source record.

Safe label:

```text
known variant evidence attached to brokered genotype relationship
```

Unsafe label:

```text
multiallelic genotype proves disease model
```

## OACS

OACS must distinguish:

```text
no genotype relationship
unresolved genotype relationship
not callable
not assayed
missing genotype
no call
partial no call
```

Unresolved relationship is not absence.

## CUES

CUES should capture genotype relationship uncertainty events such as:

```text
multiallelic_relationship_ambiguous
allele_index_out_of_range
normalization_ambiguous
symbolic_alt_unresolved
spanning_deletion_context_required
missing_variant_identity
allele_depth_vector_mismatch
```

## RMCS

RMCS should track:

```text
multiallelic_relationship_policy_id
variant_normalization_policy_id
allele_index_mapping_policy_id
genotype_parser_policy_id
relationship_builder_version
```

This makes brokerage auditable and comparable across VDB builds.

---

# 17. Validation Requirements

DEX-VDB should validate the following before treating multiallelic brokerage as implementation-complete.

```text
1. Every VDB-derived relationship traces to exactly one source genotype
   observation.

2. No VDB-derived relationship creates a new producer genotype observation.

3. Every resolved multiallelic relationship carries allele_index and source_alt.

4. Every resolved relationship preserves source_record_hash and
   genotype_observation_id.

5. AD mapping is allele-index consistent when AD is present.

6. Relationship state is not collapsed to direct_source_biallelic for
   multiallelic-derived links.

7. Ambiguous, unresolved, symbolic, spanning-deletion, malformed, and missing
   identity states remain distinct.

8. Normalization policy is recorded whenever normalization participates.

9. RDGP-facing surfaces include traceability, ambiguity, lossiness, and policy
   metadata.

10. No inheritance interpretation is emitted.
```

Validation should fail if VDB:

```text
silently treats multiallelic-derived links as direct biallelic source links

drops unresolved relationships without status

creates independent producer genotype rows

forces RDGP to reconstruct allele-index logic

emits inheritance conclusions
```

---

# 18. Anti-Collapse Rules

VDB must enforce the following anti-collapse rules:

```text
source genotype observation ≠ allele-specific relationship

derived relationship ≠ producer genotype row

variant identity ≠ genotype observation

genotype-to-variant relationship ≠ inheritance interpretation

resolved_from_multiallelic_record ≠ direct_source_biallelic

allele depth annotation ≠ independent allele-specific AD vector

normalization success ≠ biological interpretation

unresolved relationship ≠ evidence absence

missing variant identity ≠ missing genotype observation

two resolved alternate-allele relationships from one genotype observation ≠
two independent source genotype calls

two heterozygous-like variants in a gene ≠ compound heterozygosity
```

These are scientific invariants, not implementation preferences.

---

# 19. Implementation Notes for DEX-VDB

This design policy is not a final schema. DEX-VDB should derive implementation specifications, validators, and table/file contracts from this document.

Likely implementation targets include:

```text
genotype observation registration model
multiallelic relationship policy registry
genotype-to-variant relationship builder
topology relation vocabulary
relationship validation receipts
GIRS relationship-readiness fields
EVRS genotype-relationship stratification fields
PGERS relationship-state rollup fields
CUES genotype relationship events
RMCS relationship policy currency fields
TEP-VDB relationship surface emission
```

A minimal first implementation may support only:

```text
simple SNV/small-indel multiallelic records
lossless allele-index mapping
no symbolic ALT resolution
no spanning-deletion resolution
explicit unresolved states for unsupported cases
```

That is acceptable if unsupported cases remain preserved, typed, and visible.

---

# 20. Summary Doctrine

```text
VDB preserves the original VAP genotype observation as source-faithful evidence.

VDB constructs allele-specific genotype-to-variant relationships as additive,
typed, policy-declared derived topology.

VDB records allele index, source ALT, depth mapping, normalization state,
ambiguity state, lossiness state, relationship policy, and traceability.

VDB does not create independent producer genotype observations.

VDB does not collapse multiallelic-derived relationships into direct biallelic
source links.

VDB exposes consumer-safe relationship surfaces so RDGP can reason without
reparsing raw VCF FORMAT fields.

VDB brokers.
RDGP reasons.
```

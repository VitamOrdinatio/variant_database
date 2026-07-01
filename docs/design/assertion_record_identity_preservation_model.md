# Assertion Record Identity Preservation Model

**Status:** ACTIVE PHASE 4.3 DESIGN MODEL

**Phase:** IV.3 — Assertion Records

**Primary Contract:** `docs/contracts/assertion_records/assertion_record_contract.md`

**Primary Schema:** `docs/implementation/schemas/assertion_record_schema.md`

**Primary Validation Document:** `docs/validation/assertion_record_validation.md`

**Implementation Plan:** `docs/implementation/plans/assertion_record_plan.md`

**Primary Build Output Family:** `results/phase4/assertion_records/`

**Primary Validation Receipt Family:** `results/validation/phase4_assertion_records/`

---

## Purpose

This document defines the identity preservation model for VDB Phase 4.3 Assertion Records.

The purpose of this model is to ensure that Assertion Record identity preserves both source-side producer claim identity and VDB corpus-indexed membership identity without collapsing producer authority, Registration Unit custody, Corpus Generation scope, source artifact identity, participant identity, or downstream derived-layer identity.

Assertion Record identity must support:

```text
producer claim reconstruction
source assertion reconstruction
Registration Unit reconstruction
Corpus Generation reconstruction
Assertion Record Index reconstruction
future Evidence Topology lineage
future Convergence Geometry lineage
future Evidence Convergence Surface lineage
future Projection View lineage
future RDGP-facing reconstruction
```

This model is design doctrine.

It is not a physical storage schema.

It is not a validation report.

It is not an implementation script.

---

# Identity Preservation Role

Assertion Records are the first Phase 4 layer where selected Registration Unit assertion registrations become corpus-indexed preserved scientific claims.

The governing chain is:

```text
Registration Units
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
```

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.
```

The identity preservation model governs the transition from declared scope to preserved claim records.

It prevents the following identity mistake:

```text
A row, artifact, participant, source identity, topology edge, or projection row
is treated as if it were the Assertion Record itself.
```

---

# Core Invariant

The core identity invariant is:

```text
Assertion identity must preserve both source claim identity and corpus-indexed membership identity.
```

The model therefore separates:

```text
source_assertion_key
    identity for the source-side or registration-side claim-bearing unit

assertion_id
    identity for the VDB corpus-indexed Assertion Record

assertion_record_index_id
    identity for the Assertion Record layer built for a declared Corpus Generation
```

These identities must not collapse.

A source assertion can participate in more than one Corpus Generation.

A corpus-indexed Assertion Record must preserve which Corpus Generation selected it.

---

# Identity Stack

Assertion Record identity sits within a layered identity stack.

```text
1. Producer package identity
2. Registration Unit identity
3. Corpus Generation identity
4. Assertion Record Index identity
5. Source assertion key
6. Corpus-indexed assertion_id
7. Downstream topology handoff identity
```

Each layer has a different authority.

## Producer Package Identity

Producer package identity indicates where the evidence package came from.

Examples:

```text
VAP TEP package
GSC TEP package
future RSP package
future RDGP-returned package
external evidence capsule
```

Producer package identity must not be replaced by VDB identity.

## Registration Unit Identity

Registration Unit identity indicates where VDB preserved custody over an accepted producer evidence package.

Registration Unit identity must not be replaced by producer package identity, Corpus Generation identity, or Assertion Record identity.

## Corpus Generation Identity

Corpus Generation identity indicates which governed evidence universe selected the Registration Unit.

Corpus Generation identity freezes scope before Assertion Record indexing.

## Assertion Record Index Identity

Assertion Record Index identity indicates which Phase 4.3 claim-layer build indexed a declared Corpus Generation.

The initial recommended identity is:

```text
mark_phase4_corpus_6tep_v1_assertion_record_index
```

## Source Assertion Key

Source assertion key identifies the source-side or registration-side claim-bearing unit.

It should remain stable across Corpus Generations when the same underlying source assertion is selected again.

## Corpus-Indexed Assertion ID

The corpus-indexed `assertion_id` identifies the VDB Assertion Record emitted within a specific Corpus Generation.

It may differ across Corpus Generations even when the same source assertion participates in more than one Corpus Generation.

## Downstream Topology Handoff Identity

Downstream topology handoff identity preserves which Assertion Records were handed to Evidence Topology.

It must not become Evidence Topology itself.

---

# Identity Objects

## assertion_record_index_id

`assertion_record_index_id` identifies a complete Assertion Record Index build.

Recommended components:

```text
input_corpus_generation_id
phase identifier
claim-layer label
version when applicable
```

Recommended initial value:

```text
mark_phase4_corpus_6tep_v1_assertion_record_index
```

This identity is stable for the claim-layer build.

It is not the identity of an individual producer claim.

## source_assertion_key

`source_assertion_key` identifies the source claim-bearing unit before corpus-indexed Assertion Record membership is applied.

It should be derived from source-side or registration-side identity when available.

It may be native, registration-derived, or fallback-derived.

## assertion_id

`assertion_id` identifies one corpus-indexed VDB Assertion Record.

It must be deterministic under fixed inputs.

It must preserve Corpus Generation lineage.

It must not be inferred from row order, filesystem traversal order, SQLite row-return order, or non-deterministic timestamps.

---

# Source Assertion Key Model

The source assertion key preserves the identity of the source claim-bearing material.

Preferred source assertion key tuple:

```text
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id
assertion_type
producer_family
```

When `source_assertion_registration_id` is available, it should be used.

When `source_assertion_registration_id` is unavailable, a fallback key may be constructed from reconstructable source components.

Recommended fallback tuple:

```text
registration_unit_id
source_package_id
source_artifact_id
source_record_reference
relationship_or_relationship_class
participant_reference_fingerprint
evidence_basis_reference
assertion_type
producer_family
```

Fallback key behavior must be explicit.

Fallback-derived keys must not masquerade as native producer assertion identifiers.

Recommended key metadata fields:

```text
source_assertion_key
source_assertion_key_strategy
source_assertion_key_resolution_status
source_assertion_key_components
source_assertion_key_fingerprint_version
source_assertion_key_limitation
```

Recommended `source_assertion_key_strategy` values:

```text
native_source_assertion_registration_id
registration_assertion_id
source_record_fingerprint
source_artifact_record_fingerprint
participant_relationship_fingerprint
manual_fixture_key
unresolved
```

Recommended `source_assertion_key_resolution_status` values:

```text
resolved
resolved_with_note
fallback_resolved
unresolved
ambiguous
conflicted
inspection_failed
not_available
not_applicable
```

---

# Corpus-Indexed Assertion ID Model

The corpus-indexed `assertion_id` identifies the VDB Assertion Record emitted within a declared Corpus Generation.

Recommended deterministic assertion ID tuple:

```text
corpus_generation_id
registration_unit_id
source_assertion_key
assertion_type
producer_family
```

Conceptual derivation:

```text
assertion_id = stable_id(
    corpus_generation_id,
    registration_unit_id,
    source_assertion_key,
    assertion_type,
    producer_family
)
```

The implementation should use a deterministic, ordered, versioned identity tuple.

The exact hash or ID-rendering method must be declared in the indexing policy.

Recommended assertion ID metadata fields:

```text
assertion_id
assertion_id_strategy
assertion_id_components
assertion_id_fingerprint_version
assertion_id_resolution_status
```

Recommended `assertion_id_strategy` values:

```text
corpus_indexed_source_assertion_key
corpus_indexed_fallback_source_fingerprint
fixture_declared_assertion_id
unresolved
```

An `assertion_id` must remain stable under fixed inputs.

If the same source assertion participates in two different Corpus Generations, the `source_assertion_key` should remain stable while the corpus-indexed `assertion_id` may differ.

---

# Cross-Corpus Participation

The same underlying producer assertion may participate in more than one Corpus Generation.

When this occurs:

```text
source_assertion_key should remain the same
assertion_id should preserve the Corpus Generation that selected the assertion
lineage must expose all relevant Registration Unit and Corpus Generation identity
```

Example:

```text
source_assertion_key:
    vap_hg002|annotated_variants|row:42|variant_observation

assertion_id in corpus A:
    assertion_<stable_id(corpus_A, source_assertion_key)>

assertion_id in corpus B:
    assertion_<stable_id(corpus_B, source_assertion_key)>
```

This preserves both source continuity and corpus-specific membership.

Cross-corpus reuse must not cause Assertion Records from separate Corpus Generations to collapse into one undifferentiated object.

---

# Producer-Specific Identity Considerations

Producer-specific resolver behavior belongs in the resolver policy model.

This document defines only identity preservation expectations.

## VAP

VAP assertion identity may require fallback source assertion keys when native assertion registration identifiers are not available.

Likely VAP identity components include:

```text
registration_unit_id
source_package_id
source_artifact_id
sample_id
variant identifier
source row reference
assertion_type
relationship_or_relationship_class
producer_family
```

Representative VAP assertion identity examples:

```text
variant observation in sample
variant annotation claim
variant associated with gene
variant interpretation label
validation result
routing or prioritization output
```

VAP variant identifiers must remain source-native unless canonical identity attachment is explicitly represented separately.

## GSC

GSC assertion identity may require fallback source assertion keys when native assertion registration identifiers are not available.

Likely GSC identity components include:

```text
registration_unit_id
source_package_id
source_artifact_id
phenotype identifier or label
gene identifier
source row reference
assertion_type
relationship_or_relationship_class
producer_family
```

Representative GSC assertion identity examples:

```text
phenotype has semantic prior for gene
source contributes evidence for gene
source supports phenotype-gene relationship
producer contract validation result
```

GSC gene identifiers and phenotype labels must preserve source-native identity.

Canonical namespace brokerage may be attached separately but must not replace source participants.

---

# Collision And Duplicate Handling

Assertion Record identity generation must explicitly handle collisions and duplicates.

Validation must detect:

```text
duplicate source_assertion_key within the same Registration Unit
duplicate source_assertion_key across selected Registration Units
ambiguous fallback source assertion keys
duplicate assertion_id values within one Assertion Record Index
conflicting records with the same assertion_id
same source assertion appearing in multiple Corpus Generations
```

Duplicate source assertions are not always errors.

They may represent:

```text
repeated evidence rows
duplicate producer output
same claim carried by multiple artifacts
same claim selected into multiple Corpus Generations
fixture duplication for negative testing
```

The indexing policy must declare duplicate behavior.

Allowed duplicate handling outcomes may include:

```text
indexed
indexed_with_note
deferred
duplicate_reported
failed_validation
```

Silent duplicate collapse is prohibited.

---

# Unresolved Identity Handling

Unresolved identity must be explicit.

Missing or unstable identity must not become a blank string.

Allowed unresolved identity states include:

```text
not_available
not_applicable
not_reported
unresolved
ambiguous
conflicted
inspection_failed
unsupported
deferred
```

If `source_assertion_key` cannot be resolved, the implementation must either:

```text
fail the record under the declared validation policy
emit the record with explicit unresolved identity status
or defer the source assertion registration with a counted indexing status
```

If `assertion_id` cannot be generated deterministically, the record must not silently enter the valid Assertion Record Index.

Unresolved identity must be represented in validation receipts.

---

# Lineage Preservation Requirements

Every Assertion Record must preserve lineage sufficient to reconstruct:

```text
which producer emitted the claim
which producer family emitted the claim
which source package carried the claim
which source artifact carried the claim
which assertion registration carried the claim when available
which source identities participated when applicable
which Registration Unit preserved custody
which Corpus Generation selected the Registration Unit
which Assertion Record Index emitted the claim record
which builder and policy generated the identity
which validation report checked the identity
```

Minimum lineage identity fields:

```text
assertion_record_index_id
assertion_id
source_assertion_key
corpus_generation_id
registration_unit_id
source_package_id
source_artifact_id
source_assertion_registration_id when available
producer_family
producer_reference
indexing_process
indexing_policy_id
source_assertion_key_strategy
assertion_id_strategy
validation_report_reference when available
```

An Assertion Record without reconstructable lineage is not VDB-compliant.

---

# Relationship To Validation

Assertion Record validation must check identity preservation.

Validation must confirm:

```text
assertion_record_index_id exists
assertion_id exists and is deterministic
source_assertion_key exists or is explicitly unresolved
source_assertion_key_strategy is declared
assertion_id_strategy is declared
corpus_generation_id is preserved
registration_unit_id is preserved
producer_family is preserved
source package identity is preserved or explicitly unresolved
source artifact identity is preserved or explicitly unresolved
source assertion registration identity is preserved or explicitly unresolved
fallback key usage is visible
duplicate source assertion keys are reported
unresolved source assertion keys are reported
Assertion Record identity does not collapse into participant identity
Assertion Record identity does not collapse into source identity
Assertion Record identity does not collapse into topology identity
```

Identity validation is required at all three validation layers.

---

# Relationship To Layer 2 Fixture

The Phase 4.3 Layer 2 golden fixture must exercise identity preservation against compressed real-row data.

Layer 2 identity tests should confirm:

```text
stable source_assertion_key generation for compressed VAP slices
stable source_assertion_key generation for compressed GSC slices
stable assertion_id generation across repeated fixture runs
fallback source assertion key strategy is visible when used
unresolved source assertion keys are reported when present
duplicate source assertion keys are detected when present
source_assertion_key remains distinguishable from assertion_id
assertion_id remains distinguishable from participant IDs
assertion_id remains distinguishable from source identity IDs
assertion_id remains distinguishable from topology handoff records
```

Optional Layer 2 negative tests may include:

```text
missing source artifact reference
missing source assertion registration ID
ambiguous participant fingerprint
duplicate source row reference
changed corpus_generation_id
```

If `corpus_generation_id` changes while source material remains fixed, a corpus-indexed `assertion_id` should change or the indexing policy must explicitly justify why it does not.

---

# Relationship To Downstream Layers

Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, and RDGP-facing consumer surfaces must preserve Assertion Record lineage.

They may derive new identities.

They must not replace Assertion Record identity.

Downstream identities may include:

```text
topology_node_id
topology_edge_id
geometry_feature_id
surface_id
projection_view_id
projection_record_id
rdgp_input_record_id
```

None of these downstream identities may become the Assertion Record identity.

Assertion Records are preservation-layer claim identities.

Downstream layers are derived organization, characterization, exposure, projection, or reasoning identities.

---

# Anti-Collapse Rules

The following identity collapses are prohibited:

```text
source_assertion_key treated as identical to assertion_id
assertion_id treated as identical to source_identity_id
assertion_id treated as identical to artifact_id
assertion_id treated as identical to source_record_reference
assertion_id treated as identical to registration_unit_id
assertion_id treated as identical to corpus_generation_id
assertion_id treated as identical to participant identity
assertion_id treated as identical to relationship identity
assertion_id treated as identical to evidence basis identity
assertion_id treated as identical to topology node identity
assertion_id treated as identical to topology edge identity
assertion_id treated as identical to geometry feature identity
assertion_id treated as identical to surface identity
assertion_id treated as identical to projection row identity
Assertion Record identity inferred from row order
Assertion Record identity inferred from filesystem traversal order
Assertion Record identity inferred from SQLite row-return order
fallback keys represented as native source assertion IDs
unresolved identity represented as blank string
source participant identity overwritten by canonical identity
cross-corpus assertion reuse collapsed without Corpus Generation lineage
```

Any implementation that performs one of these actions violates this design model.

---

# Completion Criteria

This identity preservation model is satisfied when Phase 4.3 implementation can prove:

```text
Assertion Record Index identity is stable
source_assertion_key strategy is declared
assertion_id strategy is declared
source_assertion_key and assertion_id remain distinct
source assertion identity is preserved when available
fallback source assertion keys are explicit when used
fallback source assertion keys expose reconstruction limitations
corpus_generation_id participates in corpus-indexed Assertion Record identity
registration_unit_id is preserved
producer_family is preserved
source_package_id is preserved or explicitly unresolved
source_artifact_id is preserved or explicitly unresolved
source_assertion_registration_id is preserved or explicitly unresolved
source identity references are preserved when applicable
duplicate source assertion keys are reported
unresolved source assertion keys are reported
Assertion Record IDs are deterministic under fixed inputs
Assertion Record IDs are not derived from non-deterministic row order
cross-corpus participation preserves source continuity and corpus membership
Layer 2 fixture validates identity behavior on compressed real-row data
Layer 3 MARK validation confirms identity behavior on the canonical corpus
anti-collapse identity safeguards pass
```

This model is not satisfied merely because IDs exist.

It is satisfied only when identities preserve source claim identity, corpus-indexed membership identity, lineage, reconstruction, and downstream derivation boundaries.

---

# Summary

Assertion Record identity preservation protects the Phase 4.3 claim layer.

The guiding identity rule is:

```text
Preserve the source claim.

Preserve the corpus membership.

Preserve the Registration Unit.

Preserve the Corpus Generation.

Preserve the Assertion Record Index.

Keep source_assertion_key and assertion_id distinct.

Never let downstream derived identities replace preserved claim identity.
```

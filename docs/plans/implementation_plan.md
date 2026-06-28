# implementation_plan.md

## Purpose

This document defines the master implementation plan for the Variant Database (VDB).

The purpose of this plan is to translate VDB contracts, schemas, validation doctrine, and query-surface specifications into an executable implementation sequence.

This plan governs implementation order, dependency structure, validation gates, and definitions of done.

---

# Governing Contracts

Implementation must comply with:

```text
docs/contracts/system_contract.md
```

The System Contract governs all implementation work.

If any subsystem contract conflicts with the System Contract, the System Contract takes precedence.

## Existing Operational Contracts

Implementation must continue to respect existing operational contracts:

```text
docs/contracts/ingestion/ingestion_contract.md
docs/contracts/persistence/persistence_contract.md
docs/contracts/namespace_governance/namespace_resolution_contract.md
docs/contracts/discovery_overlay/discovery_overlay_contract.md
docs/contracts/query_surface/query_surface_contract.md
```

These contracts govern custody transfer, persistence, namespace preservation, relationship attachment, and query exposure.

## Required Phase 4 Architectural Contracts

The following Phase 4 architectural contracts must be added before implementation of their corresponding layers is considered complete:

```text
docs/contracts/registration_units/registration_unit_contract.md
docs/contracts/corpus_generation/corpus_generation_contract.md
docs/contracts/assertion_records/assertion_record_contract.md
docs/contracts/evidence_topology/evidence_topology_contract.md
docs/contracts/convergence_geometry/convergence_geometry_contract.md
docs/contracts/evidence_convergence_surfaces/evidence_convergence_surface_contract.md
docs/contracts/projection_layer/projection_layer_contract.md
```

These contracts govern the assertion-derived Phase 4 architecture.

---

# Governing Satellite Plans

Implementation is further guided by subsystem-specific satellite plans.

## Existing Operational Satellite Plans

```text
docs/plans/ingestion/ingestion_plan.md
docs/plans/persistence/persistence_plan.md
docs/plans/namespace_governance/namespace_resolution_plan.md
docs/plans/discovery_overlay/discovery_overlay_plan.md
docs/plans/query_surface/query_surface_plan.md
```

These plans remain valid for operational custody, persistence, namespace, overlay, and query-surface concerns.

## Required Phase 4 Architectural Satellite Plans

The following Phase 4 plans must be added before implementation of their corresponding layers is considered complete:

```text
docs/plans/registration_units/registration_unit_plan.md
docs/plans/corpus_generation/corpus_generation_plan.md
docs/plans/assertion_records/assertion_record_plan.md
docs/plans/evidence_topology/evidence_topology_plan.md
docs/plans/convergence_geometry/convergence_geometry_plan.md
docs/plans/evidence_convergence_surfaces/evidence_convergence_surface_plan.md
docs/plans/projection_layer/projection_layer_plan.md
```

The master implementation plan governs phase order.

Satellite plans govern execution details for their corresponding implementation layers.

---

# Governing Architecture And Design Documents

Implementation must preserve the architecture defined by the Phase 4 architecture, design, specification, schema, and rationale documents.

## Truth Layer

```text
docs/architecture/truth_layer_philosophy.md
docs/architecture/scientific_evidence_preservation_principles.md
docs/architecture/evidence_persistence_philosophy.md
docs/architecture/epistemic_boundaries.md
docs/architecture/knowledge_flow_philosophy.md
```

## Assertion And Derived-Layer Models

```text
docs/design/assertion_record_and_projection_model.md
docs/design/evidence_topology_model.md
docs/design/convergence_geometry_model.md
docs/design/evidence_convergence_surface_model.md
docs/design/assertion_projection_taxonomy.md
docs/design/registration_unit_and_corpus_generation_model.md
```

## Consumer-Side Requirements

```text
docs/design/rdgp_consumer_surface_requirements.md
```

This document provides consumer-side reasoning affordance requirements for RDGP-facing VDB projections.

It constrains what VDB must expose without transferring biological reasoning into VDB.

---

# Governing Specifications And Schemas

Implementation must preserve the logical architecture defined by existing schemas and Phase 4 schemas.

## Existing Foundation Schemas

```text
docs/implementation/schemas/metadata_schema.md
docs/implementation/schemas/provenance_schema.md
docs/implementation/schemas/data_schema.md
docs/implementation/schemas/relational_schema.md
docs/implementation/schemas/discovery_schema.md
docs/implementation/schemas/rdgp_query_surface_schema.md
```

## Phase 4 Specifications

```text
docs/implementation/specifications/assertion_record_spec.md
docs/implementation/specifications/evidence_topology_spec.md
docs/implementation/specifications/convergence_geometry_spec.md
docs/implementation/specifications/evidence_convergence_surface_spec.md
docs/implementation/specifications/assertion_projection_taxonomy_spec.md
```

## Phase 4 Schemas

```text
docs/implementation/schemas/assertion_record_schema.md
docs/implementation/schemas/evidence_topology_schema.md
docs/implementation/schemas/convergence_geometry_schema.md
docs/implementation/schemas/evidence_convergence_surface_schema.md
docs/implementation/schemas/assertion_projection_taxonomy_schema.md
```

## Required New Phase 4 Schemas

The following schemas must be added before their corresponding implementations are considered complete, unless they are explicitly deferred with documented rationale:

```text
docs/implementation/schemas/registration_unit_schema.md
docs/implementation/schemas/corpus_generation_schema.md
```

Implementation may choose practical physical representations, but must preserve the logical domains required by the governing contracts and schemas.

---

# Governing Validation Documents

Implementation must satisfy existing validation doctrine and Phase 4 validation requirements.

## Existing Validation Documents

```text
docs/validation/validation_strategy.md
docs/validation/schema_validation.md
docs/validation/ingestion_validation.md
docs/validation/namespace_resolution_validation.md
docs/validation/vdb_end_to_end_lifecycle_walkthrough.md
docs/validation/phase3_registration_certification.md
```

## Required Phase 4 Validation Documents

The following validation documents must be added before Phase 4 implementation is considered complete, unless they are explicitly deferred with documented rationale:

```text
docs/validation/registration_unit_validation.md
docs/validation/corpus_generation_validation.md
docs/validation/assertion_record_validation.md
docs/validation/evidence_topology_validation.md
docs/validation/convergence_geometry_validation.md
docs/validation/evidence_convergence_surface_validation.md
docs/validation/projection_layer_validation.md
docs/validation/phase4_satellite_plan_system_coherence_review.md
docs/validation/phase4_architecture_compliance_walkthrough.md
docs/validation/phase4_smoketest_certification.md
```

The satellite plan system coherence review is the Phase 4 planning-level counterpart to Phase 3 registration certification. It validates that Phase 4 contracts, plans, handoff artifacts, identity propagation, authority boundaries, status vocabularies, and validation expectations form a coherent implementation system before Phase 4 code becomes authoritative.

Validation confirms preservation, derivation traceability, authority boundaries, and consumer-readiness.

Validation does not confirm biological correctness.

---

# Governing Query And Projection Specifications

Existing query specifications remain valid where they expose preserved evidence or reconstruction handles:

```text
docs/implementation/queries/sample_gene_evidence_query.md
docs/implementation/queries/overlay_attachment_query.md
docs/implementation/queries/rdgp_surface_query.md
docs/implementation/queries/evidence_reconstruction_query.md
```

After Phase 4 architecture freeze, query outputs should be treated as projection views or consumer-facing access surfaces over governed VDB layers.

The following projection specifications must be added before Phase 4 projection implementation is considered complete, unless they are explicitly deferred with documented rationale:

```text
docs/implementation/queries/corpus_generation_manifest_query.md
docs/implementation/queries/assertion_record_index_query.md
docs/implementation/queries/evidence_topology_query.md
docs/implementation/queries/convergence_geometry_query.md
docs/implementation/queries/evidence_convergence_surface_query.md
docs/implementation/queries/projection_manifest_query.md
docs/implementation/queries/rdgp_consumer_projection_query.md
```

Query surfaces and projection views expose preserved or derived evidence structure.

They must not replace preserved evidence.

---

# Implementation Philosophy

VDB implementation must proceed preservation-first and derivation-safe.

The initial implementation goal was to prove that certified producer evidence could enter VDB custody without loss of identity, provenance, authority, namespace structure, uncertainty, or reconstructability.

That foundation has now been certified through Phase 3 registration validation on real VAP and GSC producer TEPs.

The next implementation goal is to prove that certified registration units can be used as checkpointed inputs for Phase 4 derived evidence structure.

Phase 4 implementation must not re-solve ingestion.

Phase 4 implementation must consume certified registration units, declare corpus generations, derive topology, characterize geometry, expose governed surfaces, emit projections, and validate reconstruction across the full derivation chain.

The guiding implementation rule for Phase 4 is:

```text
Consume certified registration units.

Declare corpus generations.

Preserve Assertion Record primacy.

Derive organization.

Characterize structure.

Expose surfaces.

Project views.

Validate authority boundaries.
```

---

# Implementation Status

The previous implementation sequence established the VDB custody foundation.

The following implementation domains are now considered foundational and certified or historically established for current Phase 4 planning purposes:

```text
repository implementation skeleton
read-only TEP intake
package and artifact registration
source identity registration
producer-family registration
persistence foundation
registration database construction
Phase 3 MARK canonical registration
Phase 3 registration certification
```

The certified Phase 3 registration outputs are checkpointed inputs for Phase 4 implementation.

Phase 4 should not rebuild them de novo unless they are unavailable, invalid, uncertified, or explicitly being regenerated.

---

# Active Implementation Sequence

Implementation now proceeds through the following Phase 4 sequence:

```text
Phase 4.0
    Contract, plan, and satellite alignment

Phase 4.1
    Registration unit input fixture declaration

Phase 4.2
    Corpus generation manifest construction

Phase 4.3
    Assertion Record corpus indexing

Phase 4.4
    Evidence Topology derivation

Phase 4.5
    Convergence Geometry derivation

Phase 4.6
    Evidence Convergence Surface construction

Phase 4.7
    Projection layer and consumer projection readiness

Phase 4.8
    Reconstruction, validation, and Phase 4 certification
```

Each phase must satisfy its exit criteria before the next phase becomes authoritative.

Subsystem satellite plans provide detailed execution guidance for their corresponding phases.

---

# Phase 4.0 — Contract, Plan, And Satellite Alignment

## Purpose

Align implementation governance with the frozen Phase 4 architecture.

## Expected Work

```text
update system contract
update master implementation plan
create Phase 4 architectural mini-contracts
create Phase 4 architectural satellite plans
verify satellite plan handoff coherence
verify identity propagation across Phase 4 layers
verify authority-boundary coherence across Phase 4 layers
verify status vocabulary coherence across Phase 4 layers
identify required schema additions
identify required validation additions
identify required query/projection specifications
emit Phase 4 satellite plan system coherence review
```

## Expected Outputs

```text
updated docs/contracts/system_contract.md
updated docs/plans/implementation_plan.md
Phase 4 mini-contracts
Phase 4 satellite plans
docs/validation/phase4_satellite_plan_system_coherence_review.md
docs/status/phase4_schema_backlog.md
docs/status/phase4_validation_backlog.md
docs/status/phase4_query_projection_backlog.md
```

The schema backlog should track missing or deferred schemas, such as `registration_unit_schema.md`, `corpus_generation_schema.md`, and a decision on whether `projection_layer_schema.md` is needed or whether `assertion_projection_taxonomy_schema.md` covers enough.

The validation backlog should track missing validation docs, probes, smoke tests, and certification reports.

The query/projection backlog should track query specs and projection profiles, including RDGP-facing projections.

The Phase 4 backlog files are controlled gap registers.

They identify required schemas, validation artifacts, query specifications, projection profiles, and implementation-supporting documents that are known but not yet complete.

Backlog entries should declare:

```text
artifact path
owning Phase 4 layer
required or optional status
blocking or non-blocking status
current resolution status
deferral rationale when applicable
```

Backlogs do not replace contracts, plans, schemas, validation documents, or implementation work.

They make remaining work explicit so Phase 4.0 can close cleanly before authoritative Phase 4 code begins.



## Exit Criteria

```text
system contract reflects Phase 4 architecture

implementation plan reflects Phase 4 sequence

required satellite contracts are created or explicitly deferred with rationale

required satellite plans are created or explicitly deferred with rationale

satellite plans consume and emit coherent handoff artifacts

identity propagation is coherent from Registration Units through Projection Views

authority boundaries are coherent across all Phase 4 layers

status vocabularies are compatible or explicitly layer-scoped

required schema additions are identified

required validation additions are identified

required query/projection specifications are identified

phase4_satellite_plan_system_coherence_review.md is emitted

no Phase 4 code implementation proceeds without governing contract and plan coverage
```

---

# Phase 4.1 — Registration Unit Input Fixture Declaration

## Purpose

Declare certified Phase 3 registration databases as checkpointed Phase 4 input fixtures.

## Expected Work

```text
identify certified registration units

record registration unit paths

record producer family

record package identifiers

record artifact counts

record assertion counts

record source identity counts

record certification status

verify registration units are readable

verify registration units are not modified
```

## Initial MARK Input Corpus

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite

results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite

results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite

results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite

results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite

results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

## Expected Outputs
```text
registration_unit_inventory.tsv
registration_unit_inventory.json
registration_unit_readiness_report.md
registration_unit_validation_report.json
registration_unit_validation_report.tsv
```

## Exit Criteria

```text
all declared registration units exist

all declared registration units are readable

all declared registration units have certification status

all declared registration units preserve package identity

all declared registration units preserve assertion registrations

all declared registration units preserve source identities

no registration unit is mutated

registration unit validation passes
```

---

# Phase 4.2 — Corpus Generation Manifest Construction

## Purpose

Construct a declared corpus generation over certified registration units.

## Expected Work
```text
create corpus generation identifier
select registration units under explicit selection policy
record inclusion rationale
record exclusion rationale when applicable
record package identifiers
record producer families
record artifact counts
record assertion-registration counts
record source-identity counts
record certification status
record build timestamp
record selection policy version
emit corpus generation manifest
emit downstream Assertion Record input manifest
```

## Expected Outputs

```text
corpus_generation_manifest.tsv
corpus_generation_manifest.json
corpus_generation_report.md
corpus_generation_validation_report.json
corpus_generation_validation_report.tsv
downstream_assertion_record_input_manifest.tsv
```

## Exit Criteria

```text
corpus generation identity exists

included registration units are explicit

excluded registration units are explicit when applicable

corpus scope is reconstructable

registration unit lineage is preserved

corpus generation does not become source truth

corpus generation validation passes
```

---

# Phase 4.3 — Assertion Record Corpus Indexing

## Purpose

Build a corpus-level Assertion Record index from certified registration units.

## Expected Work

```text
read assertion registrations from registration units

preserve registration unit identity

preserve package and artifact lineage

preserve producer family

preserve assertion type

preserve relationship

preserve participants when available

preserve evidence basis when available

preserve context

preserve provenance

preserve authority context

preserve uncertainty context

preserve source identity references

avoid unnecessary duplication of large source identity tables
```

## Expected Outputs

```text
assertion_record_index_manifest.tsv
assertion_record_index_manifest.json
assertion_record_index.tsv
assertion_record_index.jsonl
assertion_record_participants.tsv
assertion_record_relationships.tsv
assertion_record_evidence_basis.tsv
assertion_record_context.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
assertion_record_validation_report.json
assertion_record_validation_report.tsv
assertion_record_index_report.md
downstream_topology_input_manifest.tsv
```

## Exit Criteria

```text
Assertion Records are indexed

Assertion Records remain traceable to registration units

source identities remain traceable

producer identity remains visible

assertion type remains visible

provenance remains reconstructable

indexing is deterministic

no assertion collapse occurs

assertion record validation passes

Assertion Record index identity is stable
```

---

# Phase 4.4 — Evidence Topology Derivation

## Purpose

Derive deterministic Evidence Topology over indexed Assertion Records.

## Expected Work

```text
define topology build identifier

read Assertion Record index

derive topology relationships

preserve derivation basis

preserve source assertion references

preserve participant references

preserve registration unit references

preserve corpus generation reference

emit topology build metadata

emit topology relationship records
```

## Expected Outputs

```text
topology_build_manifest.tsv
topology_build_manifest.json
topology_relationships.tsv
topology_relationships.jsonl
topology_relationship_members.tsv
topology_basis_components.tsv
topology_namespace_mediation.tsv
topology_metadata_relationships.tsv
topology_summary.tsv
topology_validation_report.json
topology_validation_report.tsv
topology_build_report.md
downstream_geometry_input_manifest.tsv
```

## Exit Criteria

```text
topology is derived from Assertion Records

topology relationships declare derivation basis

topology relationships trace to source assertions

topology relationships trace to registration units

topology does not become source evidence

topology derivation is deterministic

topology validation passes
```

---

# Phase 4.5 — Convergence Geometry Derivation

## Purpose

Characterize structural properties over Evidence Topology.

## Expected Work

```text
define geometry build identifier

read topology build outputs

derive convergence regions

derive geometry features

derive structural motifs when applicable

preserve region bounding basis

preserve source topology references

preserve source assertion references

preserve corpus generation reference

emit geometry build metadata
```

## Expected Outputs

```text
geometry_build_manifest.tsv
geometry_build_manifest.json
convergence_regions.tsv
convergence_regions.jsonl
geometry_features.tsv
geometry_features.jsonl
geometry_feature_basis.tsv
structural_motifs.tsv when policy-enabled
structural_motifs.jsonl when policy-enabled
geometry_method_parameters.tsv
geometry_lineage.tsv
geometry_summary.tsv
geometry_validation_report.json
geometry_validation_report.tsv
geometry_build_report.md
downstream_surface_input_manifest.tsv
```

## Exit Criteria

```text
geometry is derived from topology

convergence regions declare bounding basis

geometry features declare source topology components

geometry remains traceable to assertions

geometry does not perform biological reasoning

geometry does not become source evidence

geometry derivation is deterministic

geometry validation passes
```

---

# Phase 4.6 — Evidence Convergence Surface Construction

## Purpose

Construct governed Evidence Convergence Surfaces over Convergence Geometry.

## Expected Work

```text
define surface build identifier
read Convergence Geometry build outputs
evaluate policy-enabled geometry-derived records for eligibility
evaluate policy-enabled geometry-derived records for disclosure
preserve eligibility basis
preserve disclosure basis
preserve withholding reason when applicable
preserve lossiness status when applicable
preserve evidence strata
preserve producer identity
preserve modality identity when available
preserve uncertainty and null semantics when available
preserve generation and currency context
preserve corpus generation reference
emit surface build metadata
emit downstream Projection View input manifest
```

## Expected Outputs

```text
surface_build_manifest.tsv
surface_build_manifest.json
evidence_convergence_surfaces.tsv
evidence_convergence_surfaces.jsonl
surface_memberships.tsv
surface_memberships.jsonl
surface_eligibility_basis.tsv
surface_disclosure_basis.tsv
surface_withholding.tsv
surface_lineage.tsv
surface_evidence_strata.tsv
surface_generation_currency.tsv
surface_validation_report.json
surface_validation_report.tsv
surface_build_report.md
downstream_projection_input_manifest.tsv
```

## Exit Criteria

```text
surfaces are derived from geometry

surface eligibility basis is explicit

surface disclosure basis is explicit

evidence strata remain distinguishable

surface lineage is reconstructable

surfaces expose reasoning capacity without reasoning

surfaces do not become source evidence

surface validation passes

surface eligibility and disclosure are exposure states, not biological interpretations
```

---

# Phase 4.7 — Projection Layer And Consumer Projection Readiness

## Purpose

Implement governed Projection Views over declared VDB source layers, prove general projection mechanics, and prepare for RDGP-facing consumer projection profiles without allowing projection representation to become source authority or downstream reasoning.

## Materialized Projection Outputs

Projection metadata artifacts and materialized projection outputs are distinct.

Projection metadata artifacts declare:

```text
projection identity
projection source layer
projection source records
projection policy
field selection
field transformation
field omission
lossiness
authority labels
generation and currency context
reconstruction paths
```

Materialized projection outputs are concrete rendered files emitted from a Projection View for inspection, validation, export, reporting, or downstream consumption.

Examples include:

```text
developer inspection tables
validation reports
surface membership tables
RDGP-facing JSON packages
RDGP-facing TSV manifests
future dashboard or query-response payloads
```

Materialized projection outputs must be emitted under:

```text
materialized/
```

unless a projection policy explicitly declares another output location.

A materialized projection output is not source truth.

A materialized projection output does not replace its Projection View metadata.

A materialized projection output does not replace its governed source layer.

A materialized projection output may be regenerated from declared source records, projection policy, field maps, transformations, authority labels, lossiness records, generation/currency records, and reconstruction paths.

## Expected Work

```text
define projection build identifier

define projection purpose

define projection source layer

define projection policy

read governed source records

preserve source record references

preserve projection lineage

preserve authority labels

preserve field selection and transformation rules

preserve projection materialization status

preserve projection lossiness status when applicable

preserve generation and currency context

emit projection manifest

emit developer or validation projection first when policy-enabled

construct RDGP-facing consumer projection only after general projection mechanics pass or under an explicitly declared RDGP projection profile

preserve reasoning affordances required by RDGP when RDGP-facing projection is implemented

preserve return-path identifiers when downstream reasoning return is possible
```

## RDGP Projection Must Preserve

When an RDGP-facing projection profile is enabled, it must preserve:

```text
projection purpose
target consumer class
projection source layer
source surface identity when applicable
source geometry identity when applicable
source topology identity when applicable
source Assertion Record identities when applicable
source Corpus Generation identity
source Registration Unit identities when applicable
producer strata
evidence-domain strata
modality strata when available
sample context when applicable
gene context when applicable
phenotype context when applicable
variant context when applicable
regulatory context when applicable
uncertainty states
null semantics
negative evidence distinction when available
evidence completeness status when available
completeness scope when available
absence basis when evidence absence is asserted
omission basis when evidence is not projected
withholding basis when evidence is withheld upstream
namespace mediation status
generation context
currency context
lossiness status
reconstruction handles
return-path identifiers
```

RDGP-facing projections expose reasoning affordances.

They do not perform RDGP reasoning.

They do not determine whether evidence explains phenotype.

They do not prioritize candidate genes.

They do not create biological confidence.

## Expected Outputs

```text
projection_build_manifest.tsv
projection_build_manifest.json
projection_views.tsv
projection_views.jsonl
projection_source_records.tsv
projection_field_map.tsv
projection_transformations.tsv
projection_lossiness.tsv
projection_omissions.tsv
projection_authority_labels.tsv
projection_generation_currency.tsv
projection_reconstruction_paths.tsv
projection_validation_report.json
projection_validation_report.tsv
projection_build_report.md
materialized/developer_inspection_projection.tsv when policy-enabled
materialized/validation_projection.md when policy-enabled
materialized/surface_membership_projection.tsv when policy-enabled
materialized/rdgp_facing_projection_manifest.tsv when RDGP profile is policy-enabled
materialized/rdgp_facing_projection.json when RDGP profile is policy-enabled
rdgp_consumer_projection_validation_report.md when RDGP profile is policy-enabled
```

## Exit Criteria

```text
projection identity is stable

projection purpose is explicit

projection source layer is explicit

projection source records are explicit

projection policy is declared

projection lineage is reconstructable

projection authority labels are preserved

projection lossiness is declared

projection does not become source truth

projection does not mutate source records

projection does not replace source records

projection does not perform biological reasoning

general projection mechanics pass before RDGP-facing projection becomes authoritative

RDGP projection exposes reasoning affordances when implemented

RDGP projection does not perform RDGP reasoning when implemented

RDGP projection is deterministic when implemented

RDGP projection is return-path-ready when implemented

projection validation passes
```

---

# Phase 4.8 — Reconstruction, Validation, And Phase 4 Certification

## Purpose

Validate that the full Phase 4 derivation chain is reconstructable, deterministic, authority-safe, and consumer-ready.

## Expected Work

```text
reconstruct from projection to surface

reconstruct from surface to geometry

reconstruct from geometry to topology

reconstruct from topology to Assertion Records

reconstruct from Assertion Records to registration units

reconstruct from registration units to producer TEPs

validate authority boundaries

validate anti-collapse rules

validate deterministic rebuild behavior

validate RDGP consumer-readiness

emit Phase 4 certification report
```

## Expected Outputs

```text
phase4_reconstruction_report.md
phase4_authority_boundary_report.md
phase4_anti_collapse_report.md
phase4_consumer_readiness_report.md
phase4_satellite_plan_system_coherence_review.md when refreshed during certification
phase4_smoketest_certification.md
```

## Exit Criteria

```text
system contract satisfied

relevant mini-contracts satisfied

registration units remain unmodified

corpus generation is reconstructable

Assertion Records are reconstructable

topology derivation is reconstructable

geometry derivation is reconstructable

surface derivation is reconstructable

projection derivation is reconstructable

RDGP-facing projection is consumer-ready

VDB does not perform biological reasoning

Phase 4 certification passes

Phase 4 satellite plan coherence remains valid or deviations are documented 

full handoff chain is reconstructable from Projection Views back to Registration Units

all downstream manifests resolve to declared upstream artifacts
```

---

# Implementation Stop Conditions

Implementation must stop and return to design if any of the following occur:

```text
producer artifacts require mutation

certified registration units require destructive modification

Phase 4 requires parsing raw producer artifacts when certified registration units are available

source identities would be overwritten

registration unit identity would be lost

corpus generation scope cannot be reconstructed

Assertion Records cannot be reconstructed

provenance cannot be reconstructed

Evidence Objects or Evidence States supersede Assertion Records

namespace resolution requires source identity replacement

topology derivation creates source authority

geometry derivation performs biological reasoning

surface construction determines biological meaning

projection output becomes authoritative storage

projection lossiness is not declared

evidence strata are collapsed into opaque composite scores

uncertainty or null states are collapsed

external evidence cannot remain distinguishable from producer evidence

RDGP reasoning leaks into VDB

returned RDGP assertions overwrite prior evidence generations

validation cannot explain evidence origin or derivation path
```

Stop conditions indicate architectural or implementation design failure.

---

# Testing Strategy

Each phase must include tests for:

```text
positive path behavior
anti-collapse behavior
determinism
provenance preservation
identity preservation
registration unit preservation
corpus generation reconstruction
assertion traceability
derived-layer traceability
schema conformance
contract compliance
authority boundary preservation
```

Tests must prefer small fixtures when possible.

Large MARK-hosted registration units should be inspected through read-only probes, checkpointed smoketests, or controlled derived-index builds.

Testing must distinguish:

```text
local unit tests
small integration tests
MARK checkpointed registration-unit tests
MARK heavy Phase 4 smoketests
certification probes
```

---

# Fixture Strategy

Implementation should use four fixture tiers:

```text
Tier 1
    synthetic minimal fixtures

Tier 2
    small real producer-derived fixtures

Tier 3
    certified registration-unit fixtures

Tier 4
    MARK-hosted heavy Phase 4 corpus-generation smoketests
```

Tier 1 supports fast local unit tests.

Tier 2 supports realistic integration tests.

Tier 3 supports development against certified registration units without rebuilding raw TEP ingestion.

Tier 4 supports production-realistic topology, geometry, surface, and projection validation on MARK.

Large registration units must not be stored in Git.

Generated certification summaries, manifests, validation reports, and compact derived summaries may be committed when appropriate.

---

# Initial Phase 4 Benchmark Corpus

Initial Phase 4 development is anchored by the certified MARK Phase 3 registration corpus:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite

results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite

results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite

results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite

results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite

results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

These registration units establish the first real-world Phase 4 input corpus.

The initial corpus generation should be named:

```text
mark_phase4_corpus_6tep_v1
```

or another declared corpus-generation identifier.

This corpus should be used to test:

```text
registration unit indexing
corpus generation manifest construction
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry derivation
Evidence Convergence Surface construction
Projection View construction
RDGP consumer projection readiness
full derivation reconstruction
```

---

# Definitions Of Done

A phase is complete only when:

```text
implementation exists

tests exist

contract compliance is demonstrated

validation output is generated

documentation assumptions remain valid

anti-collapse checks pass

authority boundaries are preserved

traceability to registration units is preserved

traceability to Assertion Records is preserved when applicable

derived-layer reconstruction passes when applicable

consumer-readiness is demonstrated when applicable
```

A phase is not complete merely because code runs.

A phase is not complete if derived output cannot be traced back to governed VDB sources.

A Phase 4 phase is not complete if it requires unnecessary re-registration of certified input fixtures.

---

# Implementation Priority

The current implementation priority is:

```text
Phase 4.0
    Contract, plan, and satellite alignment
```

The first Phase 4 code success condition is:

```text
VDB can read certified registration units
without mutation
and emit a deterministic corpus generation manifest.
```

Only after this succeeds should topology, geometry, surfaces, or projections become authoritative implementation targets.

---

# Summary

This implementation plan defines the master sequence for moving VDB from certified registration custody into Phase 4 derived evidence architecture.

The guiding implementation rule is:

```text
Do not rebuild custody when certified registration units exist.

Do not derive topology before declaring corpus scope.

Do not derive geometry before topology exists.

Do not expose surfaces before geometry is traceable.

Do not project views without declaring purpose and lineage.

Do not let derived layers acquire authority.

Validate everything.
```

Or more compactly:

```text
Build from certified custody.

Declare the corpus.

Index assertions.

Derive topology.

Characterize geometry.

Expose surfaces.

Project safely.

Certify reconstruction.
```
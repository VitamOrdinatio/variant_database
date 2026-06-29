# Phase 4 Query And Projection Backlog

## Purpose

This document records the Phase 4 query and projection backlog for the Variant Database (VDB).

The purpose of this backlog is to track query-surface modernization, Projection View integration, consumer-facing query needs, reconstruction query needs, RDGP-facing query/projection decisions, and query directory index maintenance during Phase 4.

This document is not itself a query specification.

This document is not a Projection Layer schema.

This document is not a Query Surface contract.

This document is a query/projection governance control register.

---

# Current Verdict

The current query directory contains valuable pre-Phase 4 conceptual query-surface documents.

These documents define important retrieval, overlay, RDGP-facing, and reconstruction intentions, but they predate the now-formalized Phase 4 derived-evidence chain.

Current verdict:

```text
PASS FOR PHASE 4.0 QUERY/PROJECTION BACKLOG GOVERNANCE,
WITH QUERY SURFACE MODERNIZATION DEFERRED UNTIL UPSTREAM PHASE 4
DERIVED LAYERS AND PROJECTION MECHANICS EXIST.
```

This is not a claim that Phase 4 query implementation is complete.

This is not a claim that RDGP-facing projection payloads are finalized.

This is not a claim that existing query documents are obsolete.

The correct interpretation is:

```text
Current query documents are retained as conceptual anchors.

Projection Layer schema now provides future projection metadata and
materialization governance.

Phase 4 query specifications should be modernized in layer order as upstream
Phase 4 structures become real.
```

---

# Query Surfaces Versus Projection Views

VDB distinguishes Query Surfaces from Projection Views.

```text
Query Surface
    governed access pathway or interface over VDB records

Projection View
    purpose-bound representation emitted from governed VDB records
```

A Query Surface may emit a Projection View.

A query response may be represented as a Projection View.

A Projection View may be used as a query response, export, report, dashboard payload, validation output, or consumer package.

However:

```text
Query Surface governance is not the same thing as Projection Layer metadata.

Projection View materialization is not the same thing as Query Surface policy.

A query response must not silently become source evidence.

A Projection View must not silently replace Query Surface governance.
```

This backlog tracks both query-surface modernization and projection-facing query needs without collapsing the two layers.

---

# Phase 4 Query/Projection Context

The current Phase 4 architecture establishes the following authority chain:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed evidence for a purpose.

Downstream systems reason over projections.
```

Query and projection specifications should be modernized against this chain.

Existing query documents should be reconciled with the following newer Phase 4 terms:

```text
Registration Unit
Corpus Generation
Assertion Record
Evidence Topology
Convergence Geometry
Evidence Convergence Surface
Projection View
Query Surface
```

The older concepts of:

```text
evidence object
evidence state
overlay
query surface
RDGP surface
surface construction
reconstruction
```

remain useful, but they must be mapped carefully onto the Phase 4 preservation and derived-layer model.

---

# Status Vocabulary

## Query Document Status

Allowed values:

```text
completed
completed_pre_phase4_review_required
planned_required
planned_future
review_required
harmonization_required
deferred
superseded
```

## Projection Decision Status

Allowed values:

```text
not_applicable
projection_schema_present
projection_profile_pending
projection_materialization_pending
future_consumer_decision
deferred_until_layer_exists
```

## Requirement Class

Allowed values:

```text
required
conditional
optional
deferred
future
```

## Blocking Status

Allowed values:

```text
non_blocking_for_phase4_0
required_before_phase4_0_closure
required_before_phase4_2_completion
required_before_phase4_3_completion
required_before_phase4_4_completion
required_before_phase4_5_completion
required_before_phase4_6_completion
required_before_phase4_7_completion
required_before_phase4_8_certification
deferred_non_blocking
```

---

# Existing Query Surface Documents

The following query documents are currently present.

They are retained as conceptual anchors and should be reviewed before being treated as implementation-ready Phase 4 query specifications.

| Document                                                       | Requirement Class | Query Document Status                | Projection Decision Status         | Blocking Status                        | Notes                                                                                                                                                                                 |
| -------------------------------------------------------------- | ----------------- | ------------------------------------ | ---------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/queries/sample_gene_evidence_query.md`    | conditional       | completed_pre_phase4_review_required | projection_materialization_pending | required_before_phase4_8_certification | Defines the canonical sample-gene evidence retrieval intent. Must be reconciled with Assertion Records, Evidence Convergence Surfaces, and Projection Views before RDGP-facing use.   |
| `docs/implementation/queries/overlay_attachment_query.md`      | conditional       | completed_pre_phase4_review_required | deferred_until_layer_exists        | required_before_phase4_6_completion    | Defines overlay attachment retrieval intent. Must be reconciled with Evidence Topology, Convergence Geometry, Evidence Convergence Surface membership, and future overlay governance. |
| `docs/implementation/queries/rdgp_surface_query.md`            | conditional       | completed_pre_phase4_review_required | projection_profile_pending         | required_before_phase4_8_certification | Defines RDGP-facing surface construction intent. Should be modernized after Projection Layer mechanics and RDGP-facing projection profile requirements stabilize.                     |
| `docs/implementation/queries/evidence_reconstruction_query.md` | required          | completed_pre_phase4_review_required | projection_materialization_pending | required_before_phase4_8_certification | Defines preservation-verification and reconstruction intent. Must be reconciled with full Phase 4 lineage from Projection View back to producer TEPs.                                 |

## Existing Query Document Interpretation

The existing query documents are not obsolete.

They should not be deleted.

They should not be treated as complete Phase 4 implementation specifications without modernization.

They should be treated as:

```text
conceptual anchors
consumer-intent documents
pre-Phase 4 query-surface doctrine
modernization inputs
```

---

# Existing Projection Governance

Projection governance is now represented by:

```text
docs/implementation/schemas/projection_layer_schema.md
```

The Projection Layer schema defines:

```text
Projection Build records
Projection View records
source record records
field map records
transformation records
lossiness records
omission records
authority label records
generation/currency records
reconstruction path records
validation records
materialized output records
```

This schema provides the metadata and materialization model needed for future query response projections, RDGP-facing consumer projections, validation projections, inspection projections, and export projections.

However, the existence of the Projection Layer schema does not mean query/projection implementation is complete.

Projection mechanics remain staged for Phase 4.7.

RDGP-facing projection specialization remains staged after general Projection Layer mechanics are validated.

---

# Required Future Phase 4 Query Documents

The following future query documents are expected as Phase 4 implementation proceeds.

They are not all required before Phase 4.0 closure.

| Planned Document                                                    | Requirement Class | Query Document Status | Projection Decision Status  | Blocking Status                        | Purpose                                                                                                                                                                            |
| ------------------------------------------------------------------- | ----------------- | --------------------- | --------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/queries/corpus_generation_manifest_query.md`   | conditional       | planned_required      | deferred_until_layer_exists | required_before_phase4_2_completion    | Defines how Corpus Generation manifests, selected Registration Units, inclusion/exclusion rationale, and scope summaries are queried.                                              |
| `docs/implementation/queries/assertion_record_index_query.md`       | required          | planned_required      | deferred_until_layer_exists | required_before_phase4_3_completion    | Defines how corpus-indexed Assertion Records are queried while preserving producer claim identity, corpus identity, Registration Unit lineage, and authority status.               |
| `docs/implementation/queries/evidence_topology_query.md`            | required          | planned_required      | deferred_until_layer_exists | required_before_phase4_4_completion    | Defines how Evidence Topology relationships are queried without treating topology as biological truth.                                                                             |
| `docs/implementation/queries/convergence_geometry_query.md`         | required          | planned_required      | deferred_until_layer_exists | required_before_phase4_5_completion    | Defines how Convergence Geometry regions, features, and structural motifs are queried without treating geometry as confidence.                                                     |
| `docs/implementation/queries/evidence_convergence_surface_query.md` | required          | planned_required      | deferred_until_layer_exists | required_before_phase4_6_completion    | Defines how Evidence Convergence Surface records, memberships, eligibility basis, disclosure basis, withholding, generation, and currency are queried.                             |
| `docs/implementation/queries/projection_manifest_query.md`          | required          | planned_required      | projection_schema_present   | required_before_phase4_7_completion    | Defines how Projection Builds, Projection Views, source records, field maps, transformations, lossiness, authority labels, materializations, and reconstruction paths are queried. |
| `docs/implementation/queries/rdgp_consumer_projection_query.md`     | conditional       | planned_required      | projection_profile_pending  | required_before_phase4_8_certification | Defines how RDGP-facing consumer projections are queried or emitted after Projection Layer mechanics stabilize.                                                                    |

## Future Query Document Rule

Future query documents should be authored in layer order.

A query document should not claim implementation readiness until its upstream source layer exists and its authority boundary has been validated.

---

# RDGP-Facing Query And Projection Decisions

RDGP-facing query and projection work should remain staged.

The current RDGP-facing query document defines the intent to construct deterministic, provenance-complete evidence surfaces for downstream RDGP reasoning.

The Projection Layer schema now adds the representation-governance model required for RDGP-facing Projection Views.

The RDGP-facing backlog items are:

```text
modernize rdgp_surface_query.md against Phase 4 terminology
define rdgp_consumer_projection_query.md
decide whether RDGP-facing output is primarily a query response, Projection View,
TEP-VDB export, or consumer package
preserve return-path identifiers
preserve source Projection View identifiers
preserve source surface, geometry, topology, Assertion Record, Corpus Generation,
and Registration Unit lineage when applicable
preserve lossiness, omissions, authority labels, generation, and currency
avoid RDGP reasoning inside VDB
```

## RDGP-Facing Decision Rule

RDGP-facing query/projection specifications should not be finalized before:

```text
Evidence Convergence Surface mechanics exist
Projection Layer mechanics exist
RDGP consumer requirements are stable
return-path requirements are defined
lossiness and omission behavior are validated
```

RDGP-facing projections prepare evidence for reasoning.

They do not reason.

---

# Reconstruction Query Modernization

The evidence reconstruction query remains essential.

It should eventually be modernized to reconstruct through the complete Phase 4 chain:

```text
Projection View
        ↓
Evidence Convergence Surface
        ↓
Convergence Geometry
        ↓
Evidence Topology
        ↓
Assertion Record
        ↓
Corpus Generation
        ↓
Registration Unit
        ↓
producer artifact
        ↓
producer TEP
```

The modernization should preserve older reconstruction domains where still relevant:

```text
evidence reconstruction
state reconstruction
provenance reconstruction
identity reconstruction
overlay reconstruction
discovery reconstruction
surface reconstruction
RDGP round-trip reconstruction
```

The reconstruction query should not become a biological interpretation query.

It exists to verify preservation.

---

# Overlay Query Modernization

The overlay attachment query should be reconciled with Phase 4 derived evidence layers.

Modernization should clarify whether an overlay relationship is represented through:

```text
Assertion Record relationships
Evidence Topology relationships
Convergence Geometry structure
Evidence Convergence Surface membership
Projection View representation
future external evidence capsule linkage
future returned reasoning assertion linkage
```

The overlay query should continue to preserve:

```text
attachment status
attachment basis
attachment provenance
attachment authority
attachment uncertainty
phenotype context
namespace brokerage
overlay independence
```

Overlay attachment must not become evidence fusion.

---

# Sample-Gene Query Modernization

The sample-gene evidence query should be reconciled with Assertion Records, Evidence Convergence Surfaces, and Projection Views.

Modernization should clarify whether sample-gene evidence retrieval is implemented as:

```text
direct Assertion Record query
Evidence Topology-derived query
Evidence Convergence Surface query
Projection View query response
RDGP-facing consumer projection input
```

The query should continue to preserve:

```text
sample identity
gene identity
namespace resolution status
evidence channels
overlays
provenance
uncertainty
contributing variant visibility
future reinterpretability
```

The query must not perform prioritization or biological reasoning.

---

# Query Directory Index Refresh

The following query directory index files require review.

| File                                       | Requirement Class | Query Document Status | Blocking Status                  | Required Action                                                                                                                                        |
| ------------------------------------------ | ----------------- | --------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `docs/implementation/queries/README.md`    | required          | review_required       | required_before_phase4_0_closure | Refresh to state that existing query docs are conceptual anchors and that Phase 4 query/projection modernization is staged by layer.                   |
| `docs/implementation/queries/NAMESPACE.md` | required          | review_required       | required_before_phase4_0_closure | Refresh to include `phase4_query_projection_backlog.md` if status docs are referenced, and to preserve namespace entries for existing query documents. |

At minimum, the query README and NAMESPACE should include the existing query documents:

```text
sample_gene_evidence_query.md
overlay_attachment_query.md
rdgp_surface_query.md
evidence_reconstruction_query.md
```

As future query documents are authored, the README and NAMESPACE should be updated to include:

```text
corpus_generation_manifest_query.md
assertion_record_index_query.md
evidence_topology_query.md
convergence_geometry_query.md
evidence_convergence_surface_query.md
projection_manifest_query.md
rdgp_consumer_projection_query.md
```

Index files do not define query authority.

They support query document discovery.

---

# Phase 4.0 Query/Projection Closure Criteria

Phase 4.0 query/projection backlog closure is satisfied when:

```text
phase4_query_projection_backlog.md exists
existing query documents are inventoried
existing query documents are marked completed_pre_phase4_review_required
Projection Layer schema is acknowledged as present
future Phase 4 query documents are tracked by implementation phase
RDGP-facing projection decisions are explicitly staged
reconstruction query modernization is tracked
overlay query modernization is tracked
sample-gene query modernization is tracked
docs/implementation/queries/README.md is refreshed
docs/implementation/queries/NAMESPACE.md is refreshed
no known query/projection obligation remains untracked
```

Phase 4.0 query/projection backlog closure does not require:

```text
Phase 4 query implementation
Projection Layer implementation
final RDGP-facing projection payload
completed projection materialization
query response API
dashboard implementation
completed layer-specific query documents for all layers
completed RDGP return-path integration
```

---

# Phase 4 Layer Query/Projection Gates

The following gates describe when future query/projection documents become required.

## Phase 4.2 Corpus Generation

Required before completion when Corpus Generation queryability is part of the layer deliverable:

```text
docs/implementation/queries/corpus_generation_manifest_query.md
```

## Phase 4.3 Assertion Records

Required before completion:

```text
docs/implementation/queries/assertion_record_index_query.md
```

## Phase 4.4 Evidence Topology

Required before completion:

```text
docs/implementation/queries/evidence_topology_query.md
```

## Phase 4.5 Convergence Geometry

Required before completion:

```text
docs/implementation/queries/convergence_geometry_query.md
```

## Phase 4.6 Evidence Convergence Surfaces

Required before completion:

```text
docs/implementation/queries/evidence_convergence_surface_query.md
```

## Phase 4.7 Projection Layer

Required before completion:

```text
docs/implementation/queries/projection_manifest_query.md
```

## Phase 4.8 RDGP-Facing Certification

Required before RDGP-facing certification:

```text
docs/implementation/queries/rdgp_consumer_projection_query.md
```

The existing `rdgp_surface_query.md` should be reviewed and reconciled before Phase 4.8 certification.

---

# Anti-Collapse Safeguards

This backlog must not collapse:

```text
query backlog into query specification
query surface into Projection View
Projection View into Query Surface
query response into source evidence
query response into biological reasoning
Projection Layer schema into RDGP payload schema
RDGP-facing projection into RDGP reasoning
sample-gene evidence retrieval into candidate prioritization
overlay attachment into evidence fusion
evidence reconstruction into evidence scoring
materialized output into source truth
dashboard display into evidence authority
query directory index into query authority
conceptual anchor document into implementation-ready specification
future query document into Phase 4.0 blocker
```

A query document may be useful without being implementation-ready.

A Projection View may be emitted through a Query Surface without replacing Query Surface governance.

A query response may be materialized as a Projection View without becoming source truth.

RDGP-facing query/projection outputs must prepare evidence, not reason over evidence.

---

# Recommended Next Actions

Recommended immediate actions:

```text
1. Create docs/status/phase4_query_projection_backlog.md.

2. Refresh docs/implementation/queries/README.md.

3. Refresh docs/implementation/queries/NAMESPACE.md.

4. Keep existing query documents as completed_pre_phase4_review_required.

5. Do not attempt to finalize RDGP-facing Projection View payloads until
   Evidence Convergence Surface and Projection Layer mechanics exist.

6. Draft corpus_generation_manifest_query.md only if Phase 4.2 implementation
   requires queryability as part of layer completion.

7. Draft assertion_record_index_query.md before completing Phase 4.3.

8. Draft evidence_topology_query.md before completing Phase 4.4.

9. Draft convergence_geometry_query.md before completing Phase 4.5.

10. Draft evidence_convergence_surface_query.md before completing Phase 4.6.

11. Draft projection_manifest_query.md before completing Phase 4.7.

12. Draft rdgp_consumer_projection_query.md before Phase 4.8 RDGP-facing
    certification.
```

These actions support orderly Phase 4 execution.

They do not imply that Phase 4 query/projection implementation is complete.

---

# Summary

The Phase 4 query/projection backlog records the current query-surface and projection-governance state.

Existing query documents are present and valuable, but they require Phase 4 modernization before implementation use.

Projection Layer schema is now present and provides the metadata/materialization model for future Projection View work.

Future query documents should be drafted in layer order as upstream Phase 4 structures become real.

Current query/projection backlog verdict:

```text
PASS FOR PHASE 4.0 QUERY/PROJECTION BACKLOG GOVERNANCE
```

with the following closure condition:

```text
Refresh docs/implementation/queries/README.md and
docs/implementation/queries/NAMESPACE.md before declaring Phase 4.0
query/projection governance fully closed.
```

# Phase 4 Schema Backlog

## Purpose

This document records the Phase 4 schema backlog for the Variant Database (VDB).

The purpose of this backlog is to track schema coverage, schema review status, schema harmonization needs, index maintenance, deferred schema abstractions, and future schema profile decisions for Phase 4.

This document is not itself a schema.

This document is not a substitute for missing required schemas.

This document is a schema governance status register.

---

# Current Verdict

As of this review, the required Phase 4 logical schema suite is present.

No known required Phase 4 logical schema is missing for Phase 4.0 closure.

The remaining schema backlog consists of:

```text
schema review
schema harmonization monitoring
README and NAMESPACE refresh
future profile decisions
deferred optional abstractions
```

The three previously missing Phase 4 logical schema gaps have been closed:

```text
docs/implementation/schemas/registration_unit_schema.md
docs/implementation/schemas/corpus_generation_schema.md
docs/implementation/schemas/projection_layer_schema.md
```

These schemas are marked:

```text
completed
```

---

# Phase 4 Schema Coverage Chain

Phase 4 schema coverage now spans the full required logical chain:

```text
Registration Unit
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection Layer
```

The governing schema chain is:

```text
docs/implementation/schemas/registration_unit_schema.md
docs/implementation/schemas/corpus_generation_schema.md
docs/implementation/schemas/assertion_record_schema.md
docs/implementation/schemas/evidence_topology_schema.md
docs/implementation/schemas/convergence_geometry_schema.md
docs/implementation/schemas/evidence_convergence_surface_schema.md
docs/implementation/schemas/projection_layer_schema.md
```

This chain supports the Phase 4 authority sequence:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed evidence.
```

---

# Status Vocabulary

## Schema Status

Allowed schema status values:

```text
completed
completed_pending_review
review_required
harmonization_required
deferred_optional_abstraction
future_profile_decision
superseded
```

## Requirement Class

Allowed requirement classes:

```text
required
optional
conditional
deferred
future
```

## Blocking Status

Allowed blocking status values:

```text
non_blocking_for_phase4_0
required_before_phase4_0_closure
required_before_layer_completion
required_before_phase4_8_certification
deferred_non_blocking
```

---

# Required Phase 4 Schemas

The following schemas provide required Phase 4 logical schema coverage.

| Schema                                                               | Requirement Class | Schema Status | Blocking Status                  | Notes                                                                                                                                                                                                            |
| -------------------------------------------------------------------- | ----------------- | ------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/schemas/registration_unit_schema.md`            | required          | completed     | non_blocking_for_phase4_0        | Defines Phase 4 read-only Registration Unit declaration, inspection, inventory, readiness, validation, and Corpus Generation handoff schema.                                                                     |
| `docs/implementation/schemas/corpus_generation_schema.md`            | required          | completed     | non_blocking_for_phase4_0        | Defines policy-declared Corpus Generation scope, Registration Unit membership, inclusion/exclusion rationale, deterministic manifests, validation reports, and Assertion Record handoff schema.                  |
| `docs/implementation/schemas/assertion_record_schema.md`             | required          | completed     | required_before_layer_completion | Existing Assertion Record schema. Review before Phase 4.3 implementation to confirm compatibility with Registration Unit and Corpus Generation handoff artifacts.                                                |
| `docs/implementation/schemas/evidence_topology_schema.md`            | required          | completed     | required_before_layer_completion | Existing Evidence Topology schema. Review before Phase 4.4 implementation to confirm compatibility with Assertion Record outputs.                                                                                |
| `docs/implementation/schemas/convergence_geometry_schema.md`         | required          | completed     | required_before_layer_completion | Existing Convergence Geometry schema. Review before Phase 4.5 implementation to confirm compatibility with Evidence Topology outputs.                                                                            |
| `docs/implementation/schemas/evidence_convergence_surface_schema.md` | required          | completed     | required_before_layer_completion | Existing Evidence Convergence Surface schema. Review before Phase 4.6 implementation to confirm compatibility with Convergence Geometry outputs and downstream projection input manifests.                       |
| `docs/implementation/schemas/projection_layer_schema.md`             | required          | completed     | non_blocking_for_phase4_0        | Defines Projection Build, Projection View, source record, field map, transformation, lossiness, omission, authority label, generation/currency, reconstruction path, validation, and materialized-output schema. |

## Required Schema Summary

The required Phase 4 logical schema suite is complete.

No additional required Phase 4 schema is currently known to be missing for Phase 4.0 closure.

Layer-specific schema reviews should still occur before each corresponding implementation phase begins.

---

# Cross-Cutting, Taxonomy, And Consumer-Facing Schemas

The following schemas support classification, projection taxonomy, discovery, and consumer-facing access.

| Schema                                                                | Requirement Class | Schema Status | Blocking Status                        | Notes                                                                                                                                                                     |
| --------------------------------------------------------------------- | ----------------- | ------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/schemas/assertion_projection_taxonomy_schema.md` | conditional       | completed     | required_before_layer_completion       | Existing taxonomy schema. Review before Projection Layer implementation and consumer-facing profile work to confirm it remains aligned with `projection_layer_schema.md`. |
| `docs/implementation/schemas/rdgp_query_surface_schema.md`            | conditional       | completed     | required_before_phase4_8_certification | Existing RDGP-facing query surface schema. Review after Projection Layer mechanics stabilize and before RDGP-facing consumer projection certification.                    |
| `docs/implementation/schemas/discovery_schema.md`                     | conditional       | completed     | required_before_phase4_8_certification | Existing discovery schema. Review when Phase 4 derived artifacts become discoverable through VDB Discovery or Query Surface workflows.                                    |

---

# Foundation Schemas

The following schemas provide foundational metadata, provenance, data, relational, and discovery support.

| Schema                                             | Requirement Class | Schema Status | Blocking Status           | Notes                                                                                                                                     |
| -------------------------------------------------- | ----------------- | ------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/schemas/metadata_schema.md`   | required          | completed     | non_blocking_for_phase4_0 | Existing foundation schema. May require review if Phase 4 builders add new metadata fields.                                               |
| `docs/implementation/schemas/provenance_schema.md` | required          | completed     | non_blocking_for_phase4_0 | Existing foundation schema. May require review as Registration Unit, Corpus Generation, and Projection Layer reconstruction paths mature. |
| `docs/implementation/schemas/data_schema.md`       | required          | completed     | non_blocking_for_phase4_0 | Existing foundation schema. No immediate Phase 4.0 schema gap identified.                                                                 |
| `docs/implementation/schemas/relational_schema.md` | required          | completed     | non_blocking_for_phase4_0 | Existing foundation schema. No immediate Phase 4.0 schema gap identified.                                                                 |

Foundation schemas do not need to be rewritten for Phase 4.0 closure unless implementation reveals a concrete mismatch.

---

# Schema Index And Namespace Files

The following directory-level index files require refresh because new Phase 4 schema files have been added.

| File                                       | Requirement Class | Schema Status   | Blocking Status                  | Required Action                                                                                         |
| ------------------------------------------ | ----------------- | --------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `docs/implementation/schemas/README.md`    | required          | review_required | required_before_phase4_0_closure | Refresh to mention Registration Unit, Corpus Generation, and Projection Layer schemas.                  |
| `docs/implementation/schemas/NAMESPACE.md` | required          | review_required | required_before_phase4_0_closure | Refresh to include Registration Unit, Corpus Generation, and Projection Layer schema namespace entries. |

## Index Refresh Requirements

The schema README and NAMESPACE should reflect the current schema directory.

At minimum, they should include:

```text
registration_unit_schema.md
corpus_generation_schema.md
projection_layer_schema.md
```

They should also preserve existing entries for:

```text
assertion_record_schema.md
evidence_topology_schema.md
convergence_geometry_schema.md
evidence_convergence_surface_schema.md
assertion_projection_taxonomy_schema.md
rdgp_query_surface_schema.md
metadata_schema.md
provenance_schema.md
data_schema.md
relational_schema.md
discovery_schema.md
```

The index files should not redefine schema authority.

They should make schema discovery easier.

---

# Deferred Optional Schema Abstractions

The following possible schemas are not currently required for Phase 4.0 closure.

They may become useful later if repeated patterns across layer-specific artifacts justify shared abstraction.

| Candidate Schema                                                 | Requirement Class | Schema Status                 | Blocking Status       | Rationale                                                                                                                                                                                         |
| ---------------------------------------------------------------- | ----------------- | ----------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/implementation/schemas/phase4_handoff_manifest_schema.md`  | deferred          | deferred_optional_abstraction | deferred_non_blocking | Each Phase 4 layer currently declares its own handoff manifest shape. A shared handoff schema may be useful later, but premature centralization could create unnecessary abstraction churn.       |
| `docs/implementation/schemas/phase4_validation_report_schema.md` | deferred          | deferred_optional_abstraction | deferred_non_blocking | Each Phase 4 layer currently declares its own validation report shape. A shared validation-report schema may be useful after Phase 4.1 through Phase 4.4 builders reveal stable common structure. |

## Deferred Abstraction Rule

Deferred optional abstractions must not be treated as missing required schemas.

A deferred optional abstraction becomes required only if implementation reveals repeated cross-layer structure that should be governed centrally.

Until then, layer-specific schema definitions remain authoritative.

---

# Future Profile Decisions

The following future schema decisions are expected but not required for Phase 4.0 closure.

| Candidate Profile                                  | Requirement Class | Schema Status           | Blocking Status                        | Rationale                                                                                                                                                                                                               |
| -------------------------------------------------- | ----------------- | ----------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RDGP-facing projection payload profile             | future            | future_profile_decision | required_before_phase4_8_certification | `projection_layer_schema.md` defines RDGP-facing projection preservation categories, but a final RDGP-specific payload profile should wait until general projection mechanics and RDGP consumer requirements stabilize. |
| Future external evidence capsule schema profile    | future            | future_profile_decision | deferred_non_blocking                  | External evidence capsules are supported conceptually but are not required for the initial MARK Phase 4 benchmark corpus.                                                                                               |
| Future returned reasoning assertion schema profile | future            | future_profile_decision | deferred_non_blocking                  | Returned reasoning outputs may re-enter VDB as governed producer assertions, but this is downstream of initial Projection Layer mechanics and RDGP-facing workflow stabilization.                                       |

Future profile decisions should not block Phase 4.0 closure.

They should be revisited when their corresponding implementation or consumer workflow becomes active.

---

# Current Schema Directory Snapshot

Current schema directory coverage includes:

```text
docs/implementation/schemas/assertion_projection_taxonomy_schema.md
docs/implementation/schemas/assertion_record_schema.md
docs/implementation/schemas/convergence_geometry_schema.md
docs/implementation/schemas/corpus_generation_schema.md
docs/implementation/schemas/data_schema.md
docs/implementation/schemas/discovery_schema.md
docs/implementation/schemas/evidence_convergence_surface_schema.md
docs/implementation/schemas/evidence_topology_schema.md
docs/implementation/schemas/metadata_schema.md
docs/implementation/schemas/NAMESPACE.md
docs/implementation/schemas/projection_layer_schema.md
docs/implementation/schemas/provenance_schema.md
docs/implementation/schemas/rdgp_query_surface_schema.md
docs/implementation/schemas/README.md
docs/implementation/schemas/registration_unit_schema.md
docs/implementation/schemas/relational_schema.md
```

The directory contains the required schemas for Phase 4.0 closure.

The directory index files require refresh to reflect the expanded schema set.

---

# Phase 4.0 Schema Closure Criteria

Phase 4.0 schema closure is satisfied when:

```text
required Phase 4 logical schemas are present
Registration Unit schema is present
Corpus Generation schema is present
Assertion Record schema is present
Evidence Topology schema is present
Convergence Geometry schema is present
Evidence Convergence Surface schema is present
Projection Layer schema is present
schema status register is present
schema README is refreshed
schema NAMESPACE is refreshed
deferred optional abstractions are explicitly marked non-blocking
future profile decisions are explicitly marked future/non-blocking
no known required Phase 4 schema gap remains untracked
```

Phase 4.0 schema closure does not require:

```text
implementation code
physical SQLite DDL finalization
performance indexes
final RDGP-facing payload profile
shared handoff manifest schema
shared validation report schema
future external capsule profile
future returned reasoning assertion profile
```

---

# Anti-Collapse Safeguards

This backlog must not collapse:

```text
schema backlog into schema specification
completed schema into implemented code
logical schema into physical DDL
directory index into schema authority
deferred optional abstraction into required missing schema
future profile decision into Phase 4.0 blocker
Projection Layer schema into RDGP-specific payload schema
Corpus Generation schema into Assertion Record schema
Registration Unit schema into Corpus Generation scope
```

A schema may be complete while implementation remains pending.

A schema may require future review without being a Phase 4.0 blocker.

A deferred optional abstraction is not a missing required schema.

---

# Recommended Next Actions

Recommended immediate actions:

```text
1. Refresh docs/implementation/schemas/README.md.

2. Refresh docs/implementation/schemas/NAMESPACE.md.

3. Keep docs/implementation/schemas/registration_unit_schema.md marked completed.

4. Keep docs/implementation/schemas/corpus_generation_schema.md marked completed.

5. Keep docs/implementation/schemas/projection_layer_schema.md marked completed.

6. Revisit assertion_record_schema.md before Phase 4.3 implementation.

7. Revisit evidence_topology_schema.md before Phase 4.4 implementation.

8. Revisit convergence_geometry_schema.md before Phase 4.5 implementation.

9. Revisit evidence_convergence_surface_schema.md before Phase 4.6 implementation.

10. Revisit projection_layer_schema.md before Phase 4.7 implementation, especially for materialized-output policy and RDGP-facing specialization.
```

These actions support orderly Phase 4 execution.

They do not indicate a missing required Phase 4.0 schema.

---

# Summary

The Phase 4 schema backlog has transitioned from a missing-schema concern to a schema governance status register.

The required Phase 4 logical schema suite is present.

The major Phase 4 schema gaps have been closed:

```text
Registration Unit schema
Corpus Generation schema
Projection Layer schema
```

Remaining schema work consists of index refresh, layer-specific pre-implementation review, deferred optional abstraction decisions, and future consumer profile decisions.

Current schema verdict:

```text
PASS FOR PHASE 4.0 SCHEMA COVERAGE
```

with the following closure condition:

```text
Refresh schema README and NAMESPACE before declaring Phase 4.0 schema governance fully closed.
```

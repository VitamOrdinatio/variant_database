# Three-Layer Validation Strategy

## Status

Active architectural guardrail.

## Purpose

VDB is designed as an emergent-property-driven system.

Each Phase 4 layer receives artifacts from the previous layer and derives a more expressive structure from them. This architecture is powerful because downstream capabilities become consequences of upstream artifact design rather than ad hoc feature implementation.

The corresponding risk is that malformed upstream artifacts become malformed downstream premises.

This document defines the three-layer validation strategy used to prevent artifact errors from propagating through the Phase 4 stack.

## Architectural Context

VDB Phase 4 follows this layer sequence:

```text
Producer TEPs
    ↓
Phase 3 Registration
    ↓
Phase 4.1 Registration Units
    ↓
Phase 4.2 Corpus Generation
    ↓
Phase 4.3 Assertion Records
    ↓
Phase 4.4 Evidence Topology
    ↓
Phase 4.5 Convergence Geometry
    ↓
Phase 4.6 Evidence Convergence Surfaces
    ↓
Phase 4.7 Projection Layer
    ↓
Phase 4.8 Certification / RDGP-facing confidence
```

The core preservation doctrine is:

```text
VDB preserves assertions before it organizes evidence.
VDB organizes evidence before it exposes evidence.
VDB exposes evidence before it projects evidence.
VDB projects evidence before downstream systems reason over evidence.
```

Because later layers depend on earlier artifacts, validation must prove not only that code behaves correctly, but that the correct artifact substrate is being pushed through the system.

## The Achilles Heel of Emergent-Property Architecture

In an emergent-property architecture, downstream capabilities are intentionally not hand-designed first. They are expected to become inevitable consequences of well-formed upstream structure.

This creates a specific failure mode:

```text
incorrect upstream artifact
    ↓
plausible but incorrect downstream emergent property
```

The dangerous case is not simply a failing test.

The dangerous case is a passing implementation operating on the wrong first principles.

For example:

```text
bad Registration Unit
    ↓
bad Corpus Generation
    ↓
bad Assertion Records
    ↓
bad Evidence Topology
    ↓
bad Convergence Geometry
    ↓
bad Evidence Surfaces
    ↓
bad Projection / RDGP substrate
```

The three-layer validation strategy exists to prevent this failure mode.

## Validation Layers

### Layer 1 — Unit and Integration Tests

Layer 1 validates the code contract.

It answers:

```text
Does the implementation behave according to its local specification?
Do loaders reject malformed inputs?
Do emitters write canonical fields?
Do validators detect known failure modes?
Are layer boundaries enforced in code?
```

Layer 1 typically runs through `pytest`.

Layer 1 should be fast, deterministic, and local.

Layer 1 does not prove that an operator can push a complete artifact substrate through a real workflow.

### Layer 2 — Lightweight Golden Fixture Smoketest

Layer 2 validates artifact flow through a small, controlled substrate.

It answers:

```text
Can an operator push a lightweight golden artifact set through the layer?
Are real files emitted in the expected result families?
Are validation receipts emitted in the expected validation families?
Does the layer preserve intended artifact semantics outside isolated unit tests?
```

Layer 2 is not merely “more unit tests.”

Layer 2 is an operator-facing rehearsal of the artifact pathway using a small known-good fixture.

The fixture should be small enough to run locally on the sys76 workstation, but expressive enough to exercise the semantic substrate required by the layer under test.

### Layer 3 — MARK Real-World Data Smoketest

Layer 3 validates artifact flow against the real MARK-scale substrate.

It answers:

```text
Can the same layer operate against real VDB artifacts?
Do real producer-derived Registration Units and Corpus Generations behave as expected?
Do real artifact counts, assertion counts, source-identity counts, and provenance references remain coherent?
Does the layer preserve boundaries under real data scale?
```

Layer 3 should not overclaim biological correctness unless the layer itself is responsible for biological correctness.

For most Phase 4 layers, MARK smoketesting validates real-corpus artifact behavior, not final scientific interpretation.

## Validation Layer Summary

| Layer | Name | Primary Question | Substrate | Typical Output |
|---|---|---|---|---|
| 1 | Unit / integration tests | Does the code contract hold? | synthetic in-test fixtures | pytest result |
| 2 | Lightweight golden fixture smoketest | Does the artifact workflow work on a controlled substrate? | small local golden fixture | smoketest receipts |
| 3 | MARK real-world smoketest | Does the artifact workflow work on the real corpus substrate? | MARK real producer-derived artifacts | MARK smoketest receipts |

## Fixture Validity Horizon

A lightweight fixture remains valid only while it expresses the minimum semantic substrate required by the phase under test.

Fixtures should evolve as Phase 4 layers become more semantically demanding.

A fixture that is sufficient for Registration Unit custody may be insufficient for Assertion Record construction. A fixture that is sufficient for Assertion Record construction may be insufficient for topology, geometry, surface exposure, or projection validation.

The fixture should not be discarded automatically.

It should be extended or versioned when the next layer requires richer semantics.

## Phase-Specific Fixture Requirements

### Phase 4.1 — Registration Units

The fixture must express minimal Registration Unit custody.

Required substrate:

```text
Registration Unit manifest declaration
SQLite-backed Registration Unit
expected Registration Unit path
expected SQLite path
minimal required schema tables
query-only/read-only inspection behavior
inventory emission
readiness emission
non-mutation behavior
sidecar absence
```

Purpose:

```text
Prove that VDB can inspect Registration Units without mutating them.
```

### Phase 4.2 — Corpus Generation

The fixture must express minimal governed corpus membership.

Required substrate:

```text
selection manifest
selection policy
included Registration Units
optional excluded/deferred candidates
Phase 4.1 inventory receipt
Phase 4.1 readiness receipt
Corpus Generation artifact emission
downstream included-only handoff
artifact-set validation
anti-self-validation and anti-self-certification boundaries
```

Purpose:

```text
Prove that VDB can declare, emit, and validate governed corpus scope without creating downstream evidence.
```

### Phase 4.3 — Assertion Records

The fixture must express minimal multi-producer assertion substrate.

Required substrate:

```text
GSC-style assertion examples
VAP-style assertion examples
producer-native claim identity
source package identity
artifact identity
source identity references
namespace references
assertion provenance
assertion subject / predicate / object or equivalent claim structure
enough heterogeneity to prove producer-native claims become common Assertion Records
```

Purpose:

```text
Prove that VDB can preserve producer-native scientific claims as common Assertion Records without erasing provenance or adding interpretation.
```

### Phase 4.4 — Evidence Topology

The fixture must express minimal relationships among Assertion Records.

Required substrate:

```text
multiple Assertion Records sharing at least one entity
multiple Assertion Records with distinct producers
at least one sample-linked assertion
at least one gene-linked assertion
at least one variant-linked assertion where applicable
known expected topology nodes
known expected topology edges
known isolated or non-convergent control case
```

Purpose:

```text
Prove that VDB can organize preserved Assertion Records into evidence topology without converting topology into belief or confidence.
```

### Phase 4.5 — Convergence Geometry

The fixture must express measurable convergence patterns over topology.

Required substrate:

```text
topology with known convergence cases
topology with known non-convergence cases
multi-producer convergence example
single-producer non-convergence example
expected convergence counts
expected geometric summaries
known edge/node participation patterns
```

Purpose:

```text
Prove that VDB can characterize evidence organization geometrically without claiming biological confidence.
```

### Phase 4.6 — Evidence Convergence Surfaces

The fixture must express governed exposure cases.

Required substrate:

```text
convergence geometry inputs
surface eligibility rules
included surface examples
excluded surface examples
surface boundary cases
provenance-preserving surface records
known exposure constraints
```

Purpose:

```text
Prove that VDB can expose governed evidence surfaces without exposing unauthorized or under-supported structures.
```

### Phase 4.7 — Projection Layer

The fixture must express projection-view cases.

Required substrate:

```text
validated evidence surfaces
projection definitions
included projection examples
excluded projection examples
consumer-facing field mappings
lossless provenance references
known projection row counts
known projection identity references
```

Purpose:

```text
Prove that VDB can emit governed projection views without changing source authority or performing downstream reasoning.
```

### Phase 4.8 — Certification / RDGP-Facing Confidence

The fixture must express minimal certification and downstream confidence cases.

Required substrate:

```text
projection inputs
certification rules
passing certification example
failing certification example
ambiguous or incomplete example
RDGP-facing handoff fields
confidence boundary fields
traceable validation provenance
```

Purpose:

```text
Prove that VDB can certify projection readiness and expose RDGP-facing confidence substrates without becoming RDGP.
```

## Validation Provenance

Each validation layer should leave durable provenance.

Recommended receipt families:

```text
results/validation/phase4_registration_units/
results/validation/phase4_corpus_generation/
results/validation/phase4_assertion_records/
results/validation/phase4_evidence_topology/
results/validation/phase4_convergence_geometry/
results/validation/phase4_evidence_surfaces/
results/validation/phase4_projection_layer/
results/validation/phase4_certification/
```

Each receipt family should distinguish:

```text
unit/integration test results
lightweight golden fixture smoketest receipts
MARK real-world smoketest receipts
latest convenience copies
timestamped durable receipt directories
checksum-backed receipt archives where appropriate
```

## Boundary Rules

Validation must preserve phase authority.

A validation layer may say:

```text
this artifact set is valid for the layer contract
```

It must not say, unless the layer explicitly owns that authority:

```text
the biological interpretation is correct
the corpus is scientifically certified
the assertions are clinically true
the topology is confidence
the geometry is belief
the surface is reasoning
the projection is RDGP output
```

## Required Guardrail

Before a Phase 4 layer is considered cleared, it should pass:

```text
Layer 1 — unit/integration tests
Layer 2 — lightweight golden fixture smoketest
Layer 3 — MARK real-world smoketest
```

Exceptions must be documented explicitly.

A layer may proceed experimentally before all three validation layers are complete, but it should not be treated as architecturally closed until all required validation layers pass.

## Closing Principle

Correct emergent behavior depends on correct artifact premises.

Therefore, VDB validates not only code, but the artifact substrates that carry meaning from one layer to the next.

# Validation Namespace

Namespace: `docs/validation/`

**Validation = Proof and verification**

> Core question:
> How do we prove VDB behavior is correct, reproducible, deterministic, and authority-preserving?

Validation documents answer:

```text
What behavior must be proven?
What validation checks are required?
What evidence demonstrates correctness?
What failure modes must be detected?
What receipts should be preserved?
What authority boundaries must not collapse?
```

Validation is:

```text
evidence-oriented
reproducibility-focused
contract-aware
implementation-verifying
lineage-preserving
authority-boundary-preserving
anti-collapse-aware
```

Principle:

```text
Validation proves that implementation satisfies contractual expectations.
```

Anti-pattern:

```text
Validation documents should not become implementation specifications,
future implementation plans, biological interpretation reports, or
certification claims without receipt evidence.
```

---

# Namespace Entries

## Global Validation Doctrine

```text
validation_strategy.md
    Master validation doctrine.

schema_validation.md
    Schema validation doctrine and schema-coherence procedures.

ingestion_validation.md
    Ingestion validation doctrine.

namespace_resolution_validation.md
    Namespace-resolution validation doctrine.

vdb_end_to_end_lifecycle_walkthrough.md
    End-to-end lifecycle validation walkthrough.
```

## Phase 3 Validation

```text
phase3_registration_certification.md
    Phase 3 registration certification governance and receipt interpretation.
```

## Phase 4 Validation Governance

```text
phase4_validation_backlog.md
    Phase 4 validation governance control register.

phase4_satellite_plan_system_coherence_review.md
    Phase 4 satellite-plan system coherence review.

registration_unit_validation.md
    Phase 4.1 Registration Unit validation governance.

phase4_1_registration_unit_certification.md
    Phase 4.1 Registration Unit certification seed for the MARK real-corpus
    six-unit canonical benchmark smoketest.
```

## Planned Phase 4 Layer Validation Documents

```text
corpus_generation_validation.md
    Planned Phase 4.2 Corpus Generation validation governance.

assertion_record_validation.md
    Planned Phase 4.3 Assertion Record validation governance.

evidence_topology_validation.md
    Planned Phase 4.4 Evidence Topology validation governance.

convergence_geometry_validation.md
    Planned Phase 4.5 Convergence Geometry validation governance.

evidence_convergence_surface_validation.md
    Planned Phase 4.6 Evidence Convergence Surface validation governance.

projection_layer_validation.md
    Planned Phase 4.7 Projection Layer validation governance.
```

## Planned Phase 4 Certification Documents

```text
phase4_architecture_compliance_walkthrough.md
    Planned Phase 4 architecture-compliance walkthrough.

phase4_smoketest_certification.md
    Planned Phase 4 smoketest certification governance.
```

---

# Current Phase 4.1 Validation State

Phase 4.1 Registration Unit validation is complete for the six-unit canonical benchmark corpus.

Governance document:

```text
registration_unit_validation.md
```

Certification seed document:

```text
phase4_1_registration_unit_certification.md
```

Receipt directory:

```text
results/validation/phase4_registration_units/
```

Current validation evidence includes:

```text
local lightweight-fixture validation_status passed
MARK real-corpus validation_status passed
six Registration Units declared
six Registration Units inspected
six Registration Units marked ready
zero Registration Units marked not_ready
non_mutation_status passed
sidecar_status passed
MARK full-corpus receipt archive SHA256 verified
```

The MARK real-corpus smoketest validated the following six canonical Phase 3 Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

This confirms Registration Unit declaration, read-only inspection, deterministic inventory emission, readiness evaluation, validation summary emission, and non-mutation behavior for both the lightweight fixture path and the MARK six-unit canonical benchmark path.

This does not complete Phase 4.8 certification.

This does not imply that all available VAP SRA-derived TEPs have been registered into VDB Phase 3 or included in Phase 4.1 validation.

---

# Validation Receipts

Validation receipts live under:

```text
results/validation/
```

Current tracked validation receipt families include:

```text
results/validation/phase3_registration_certification/
    Phase 3 registration certification receipts.

results/validation/phase4_registration_units/
    Phase 4.1 Registration Unit validation receipts, including local
    lightweight-fixture receipts, MARK real-corpus six-unit benchmark receipts,
    and portable MARK receipt archives.
```

Receipt files record what was proven during validation execution.

Receipt files do not define validation doctrine.

---

# Validation Boundary

Validation proves implementation behavior.

Validation does not silently become:

```text
source evidence
biological truth
clinical interpretation
RDGP reasoning
query policy
projection payload authority
certification without receipts
```

Validation receipts support evidence-based governance.

Validation documents define what those receipts must prove.

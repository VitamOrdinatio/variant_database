# README.md for `docs/validation/`

## Scope

Validation documentation describes how VDB proves compliance with its contracts, schemas, preservation rules, lineage requirements, reproducibility expectations, and authority boundaries.

Validation documents define what must be proven.

Validation receipts record what was actually proven during a validation, certification, smoketest, or benchmark run.

---

# Validation Philosophy

Validation answers four core questions:

```text
What behavior must be proven?

What validation checks are required?

What evidence demonstrates correctness?

What failure modes must be detected?
```

Validation is:

```text
evidence-oriented
reproducibility-focused
contract-aware
implementation-verifying
authority-boundary-preserving
anti-collapse-aware
```

Core principle:

```text
Validation proves that implementation satisfies contractual expectations.
```

Anti-pattern:

```text
Validation documents should not become implementation specifications,
future implementation plans, or biological interpretation reports.
```

---

# Validation Governance Documents

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
    Lifecycle validation walkthrough.
```

## Phase 3 Validation

```text
phase3_registration_certification.md
    Documents Phase 3 registration certification and associated validation
    receipt evidence.
```

## Phase 4 Validation Governance

```text
phase4_validation_backlog.md
    Phase 4 validation governance control register.

phase4_satellite_plan_system_coherence_review.md
    Phase 4 satellite-plan coherence review.

registration_unit_validation.md
    Phase 4.1 Registration Unit validation governance.

phase4_1_registration_unit_certification.md
    Phase 4.1 Registration Unit certification seed for the MARK real-corpus
    six-unit canonical benchmark smoketest.

corpus_generation_validation.md
    Phase 4.2 Corpus Generation validation governance.

phase4_2_corpus_generation_layer2_acceptance.md
    Phase 4.2 Layer 2 compressed real-row golden fixture acceptance evidence.

phase4_2_corpus_generation_layer3_acceptance.md
    Phase 4.2 Layer 3 MARK full-corpus acceptance evidence.

phase4_2_corpus_generation_certification.md
    Phase 4.2 Corpus Generation architectural closure certification.
```

---

# Phase 4 Layer Validation Documents

Phase 4 validation documents are authored by implementation layer.

Current status:

```text
registration_unit_validation.md
    completed

phase4_1_registration_unit_certification.md
    completed certification for Phase 4.1 six-unit canonical benchmark

corpus_generation_validation.md
    implemented and accepted

phase4_2_corpus_generation_layer2_acceptance.md
    accepted Layer 2 golden fixture validation for Phase 4.2

phase4_2_corpus_generation_layer3_acceptance.md
    accepted Layer 3 MARK full-corpus validation for Phase 4.2

phase4_2_corpus_generation_certification.md
    certified Phase 4.2 architectural closure

assertion_record_validation.md
    planned_required before Phase 4.3 completion

evidence_topology_validation.md
    planned_required before Phase 4.4 completion

convergence_geometry_validation.md
    planned_required before Phase 4.5 completion

evidence_convergence_surface_validation.md
    planned_required before Phase 4.6 completion

projection_layer_validation.md
    planned_required before Phase 4.7 completion
```

Expected future certification and walkthrough documents:

```text
phase4_architecture_compliance_walkthrough.md
    required before Phase 4.8 certification

phase4_smoketest_certification.md
    required before Phase 4.8 certification
```

---

# Phase 4.1 Registration Unit Validation Status

Phase 4.1 Registration Unit validation is complete for the six-unit canonical benchmark corpus.

Validation governance document:

```text
registration_unit_validation.md
```

Certification document:

```text
phase4_1_registration_unit_certification.md
```

Validation receipt directory:

```text
results/validation/phase4_registration_units/
```

Phase 4.1 validation evidence includes:

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

The MARK full-corpus smoketest validated the following six canonical Phase 3 Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

This closes Phase 4.1 Registration Unit validation for the six-unit canonical benchmark corpus.

This does not complete Phase 4.8 certification.

This does not imply that all available VAP SRA-derived TEPs have been registered into VDB Phase 3 or included in Phase 4.1 validation.

---

# Phase 4.2 Corpus Generation Validation Status

Phase 4.2 Corpus Generation validation is complete for the canonical six-unit MARK benchmark corpus.

Validation governance document:

```text
corpus_generation_validation.md
```

Layer 2 acceptance document:

```text
phase4_2_corpus_generation_layer2_acceptance.md
```

Layer 3 acceptance document:

```text
phase4_2_corpus_generation_layer3_acceptance.md
```

Certification document:

```text
phase4_2_corpus_generation_certification.md
```

Validation receipt directory:

```text
results/validation/phase4_corpus_generation/
```

Canonical Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Phase 4.2 validation evidence includes:

```text
140 pytest tests passing
Layer 2 golden fixture smoketest passed
Layer 3 MARK full-corpus smoketest passed
six Registration Units included
zero Registration Units excluded
82 artifacts represented
52 assertion registrations represented
147941196 MARK full-corpus source identities represented
210 MARK full-corpus validation checks passed
0 MARK full-corpus validation checks failed
```

The canonical Phase 4.2 Corpus Generation includes:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

The accepted downstream Phase 4.3 handoff artifact is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

This closes Phase 4.2 Corpus Generation validation for the six-unit canonical benchmark corpus.

This does not complete Phase 4.8 certification.

This does not certify biological correctness.

This does not create Assertion Records, derive Evidence Topology, compute Convergence Geometry, emit Evidence Convergence Surfaces, emit Projection Layer outputs, or perform RDGP reasoning.

This does not imply that all available VAP SRA-derived TEPs have been registered into VDB Phase 3 or included in the canonical Phase 4.2 Corpus Generation.

---

# Validation Receipts

Validation receipts live under:

```text
results/validation/
```

Tracked validation receipts are retained when they support:

```text
certification evidence
benchmark evidence
reproducibility evidence
governance-supporting validation evidence
historical validation evidence
```

Current tracked validation receipt families include:

```text
results/validation/phase3_registration_certification/
results/validation/phase4_registration_units/
results/validation/phase4_corpus_generation/
```

Current Phase 4.1 Registration Unit receipt evidence includes:

```text
results/validation/phase4_registration_units/
    Local lightweight-fixture Phase 4.1 validation receipts.

results/validation/phase4_registration_units/mark_full_corpus_smoketest_2026_06_30_052739/
    MARK real-corpus six-unit benchmark Phase 4.1 validation receipts.

results/validation/phase4_registration_units/receipt_archives/
    Portable MARK receipt archive and SHA256 checksum.
```

Current Phase 4.2 Corpus Generation receipt evidence includes:

```text
results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/
    Supplemental synthetic operator-path Phase 4.2 validation receipts.

results/validation/phase4_corpus_generation/golden_fixture_smoketest_2026_06_30_122500/
    Layer 2 compressed real-row golden fixture acceptance receipts.

results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/
    Layer 3 MARK full-corpus Phase 4.2 acceptance receipts.

results/validation/phase4_corpus_generation/receipt_archives/
    Portable Phase 4.2 receipt archives and SHA256 checksums.
```

Runtime scratch output should not be confused with governance-supporting validation receipts.

---

# Test Taxonomy

```text
                MARK Canonical Corpus
               (production-scale evidence)
                         ▲
                         │
              Lightweight Golden Fixtures
             (real structure, tiny data)
                         ▲
                         │
          Integration / Developer Scripts
                         ▲
                         │
               Synthetic Unit Tests
```

Each layer serves a different purpose.

```text
Synthetic Unit Tests
    Does this one function work?

Integration / Developer Scripts
    Does this workflow execute as expected?

Lightweight Golden Fixtures
    Does the VDB architecture work against realistic structure with small data?

MARK Canonical Corpus
    Does the same implementation work on production-scale evidence?
```

---

# Authority Boundary

Validation may prove:

```text
structural correctness
deterministic behavior
lineage preservation
receipt generation
non-mutation behavior
authority-boundary preservation
anti-collapse safeguards
benchmark-scale execution
```

Validation must not silently claim:

```text
biological correctness
clinical interpretation
evidence scoring correctness
RDGP reasoning correctness
Phase 4 certification
producer evidence truth
TEP-VDB emission correctness
```

Certification-strength claims require the corresponding certification document and validation receipts.

---

# Current Validation Milestones

```text
Phase 3 registration certification:
    passed

Phase 4.1 local lightweight-fixture validation:
    passed

Phase 4.1 MARK real-corpus six-unit benchmark smoketest:
    passed

Phase 4.1 Registration Unit architectural closure:
    certified

Phase 4.2 Corpus Generation Layer 1 validation:
    passed

Phase 4.2 Corpus Generation Layer 2 golden fixture validation:
    accepted

Phase 4.2 Corpus Generation Layer 3 MARK full-corpus validation:
    accepted

Phase 4.2 Corpus Generation architectural closure:
    certified
```

Current operational implication:

```text
The canonical six-unit Corpus Generation substrate is ready for Phase 4.3
Assertion Records.
```

Required Phase 4.3 input:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Phase 4.3 must consume the governed downstream input manifest.

Phase 4.3 must not crawl Registration Unit folders opportunistically.

---

# Index Maintenance

When new validation documents are added, update:

```text
docs/validation/README.md
docs/validation/NAMESPACE.md
```

When new validation receipt families are added, update:

```text
results/validation/README.md
```

Directory index files support discovery.

They do not define validation authority.

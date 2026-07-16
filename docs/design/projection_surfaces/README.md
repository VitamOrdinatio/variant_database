# Projection Surfaces

This folder contains the projection-surface design documents for **TEP-VDB**:
VDB-emitted, policy-declared, traceable reasoning substrates for RDGP and future
downstream reasoning systems.

These documents are daughter designs of:

```text
docs/architecture/tep_vdb_architecture.md
docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md
```

The architecture document explains what TEP-VDB is. The mathematical foundation
explains how VDB moves from preserved producer assertions into evidence topology,
opportunity-aware projection geometry, emitted surfaces, and downstream reasoning
transport.

---

## Abbreviations

### Repositories / Systems

```text
VAP      Variant Annotation Pipeline
GSC      Gene Set Consensus
VDB      Variant Database
RDGP     Rare Disease Gene Prioritization
RSP      RNA-seq Pipeline

TEP      Transitional Evidence Product
TEP-VAP  VAP-emitted Transitional Evidence Product
TEP-GSC  GSC-emitted Transitional Evidence Product
TEP-VDB  VDB-emitted Transitional Evidence Product for downstream reasoning
TEP-RDGP RDGP-emitted Transitional Evidence Product for brokerage into VDB
```

### Projection Surfaces

```text
OACS   Opportunity / Absence / Callability Surface
CUES   Conflict / Uncertainty Evidence-State Surface
RMCS   Reasoning / Method Currency Surface
KVPS   Known Variant Pathogenicity Surface
GIRS   Genotype / Inheritance Readiness Surface
PAPS   Phenotype Alignment / Prior Surface
PGERS  Patient Gene Evidence Rollup Surface
CFBS   Coordinate-First Burden Scan
MPLC   Matched Prior-Locus Contrast
EVRS   Exact Variant / Allele Recurrence Surface
RFPS   Regulatory / Feature Projection Surface
```

---

## Why Eleven Surfaces?

TEP-VDB is not a raw VDB dump and not a single merged evidence table.

Projection surfaces exist because downstream reasoning needs different evidence
shapes for different questions. A known pathogenicity hit, a genotype-readiness
state, a phenotype-scoped prior, a coordinate burden signal, an exact recurrent
allele, and a regulatory feature projection are related, but they are not the
same kind of object.

The core separation is:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

Projection surfaces are **reason-ready substrates**. They are not biological
truth, diagnosis, causality, pathogenicity adjudication, regulatory mechanism,
or RDGP ranking.

---

## The Three Buckets

### 1. Cross-Cutting Safety / Governance

These surfaces make every other surface safer to consume.

| Surface | Executive Summary |
| --- | --- |
| OACS | What could have been observed? Defines opportunity, callability, absence-readiness, and denominator context. |
| CUES | What is conflicted, ambiguous, missing, stale, limited, or unsafe to treat as clean support? |
| RMCS | Is this package, surface, policy, dependency, method, or comparison current, validated, refresh-ready, and comparable? |

### 2. Known-Today Diagnostic Support

These surfaces help RDGP reason over evidence that is already known, observed,
or currently contextualized.

| Surface | Executive Summary |
| --- | --- |
| KVPS | Known pathogenicity or clinical-significance evidence attached to sample-specific observed variants. |
| GIRS | Genotype observation structure and inheritance-readiness context, without inheritance reasoning. |
| PAPS | Phenotype context, GSC-derived phenotype-scoped priors, phenotype-scope alignment, and prior provenance. |
| PGERS | Patient-gene/locus rollup plane for RDGP consumption, without ranking or causal-gene selection. |

### 3. Unknown-Tomorrow Discovery Support

These surfaces expose exploratory patterns that may support future allele,
locus, feature, recurrence, or functional-role discovery. They do not claim
disease association, mechanism, pathogenicity, or causality.

| Surface | Executive Summary |
| --- | --- |
| CFBS | Coordinate-first burden/hotspot candidate intervals, annotated biologically only after coordinate nomination. |
| MPLC | Phenotype-prior locus burden contrast against matched non-prior background loci. |
| EVRS | Exact governed variant or allele recurrence across declared scopes. |
| RFPS | Coordinate-to-feature and feature-to-target projection for regulatory, conserved, structural, transcriptomic, or functional features. |

---

## How the Buckets Relate

```text
OACS / CUES / RMCS
    govern safe consumption of all surfaces.

KVPS / GIRS / PAPS
    provide known variant, genotype, and phenotype-prior context.

PGERS
    rolls selected evidence into a patient-gene/locus view for RDGP.

CFBS / MPLC / EVRS / RFPS
    expose discovery-oriented coordinate, locus, recurrence, and feature
    substrates.
```

A downstream reasoning engine may combine surfaces, but each surface keeps its
own authority boundary. For example:

```text
KVPS may show that an observed variant has known pathogenicity evidence.
GIRS may show that genotype context is usable or limited.
PAPS may show that the target has phenotype-scoped prior context.
PGERS may summarize those signals at the patient-gene/locus level.
RDGP may reason over the combination.
```

VDB must not collapse that chain into a diagnosis, causal-gene call,
pathogenicity conclusion, regulatory mechanism, disease association, or RDGP
priority.

---

## Design Rule of Thumb

Each projection surface should preserve:

```text
source evidence identity
projection policy
membership rule
opportunity or limitation context when relevant
traceability references
validation state
anti-overclaim boundary
```

If a surface cannot be traced back to preserved evidence, declared topology,
projection policy, and validation receipts, it is not TEP-VDB compliant.

---

## Minimal Reading Order

1. [TEP-VDB Architecture](../../architecture/tep_vdb_architecture.md)
2. [Mathematical Foundation](../../design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md)
3. Safe Consumption: [OACS](./oacs_opportunity_absence_callability_surface.md), [CUES](./cues_conflict_uncertainty_evidence_state_surface.md), [RMCS](./rmcs_reasoning_method_currency_surface.md)
4. Known-Today Diagnostic Support: [KVPS](./kvps_known_variant_pathogenicity_surface.md), [GIRS](./girs_genotype_inheritance_readiness_surface.md), [PAPS](./paps_phenotype_alignment_prior_surface.md), [PGERS](./pgers_patient_gene_evidence_rollup_surface.md)
5. Unknown-Tomorrow Discovery Support: [CFBS](./cfbs_coordinate_first_burden_scan.md), [MPLC](./mplc_matched_prior_locus_contrast.md), [EVRS](./evrs_exact_variant_recurrence_surface.md), [RFPS](./rfps_regulatory_feature_projection_surface.md)


That order moves from architecture, to math, to safety, to known-today evidence,
to unknown-tomorrow discovery.

---

## Summary Doctrine

```text
VDB preserves evidence.
VDB constructs topology.
VDB emits projection surfaces.
TEP-VDB transports those surfaces.
RDGP reasons.
Scientists and clinicians interpret evaluated evidence.
```

# Opportunity Space and Projection Policy Model

> Status: SAGE-VDB scientific design doctrine.
> This document defines the biological, mathematical, and evidentiary constraints
> for opportunity-space preservation and projection-policy governance in VDB.
> It is not a final implementation schema. DEX-VDB should derive implementation
> schemas, validators, and emission contracts from this design.

## Core Vocabulary

**Coordinate evidence**  
Observed variant-derived evidence anchored to reference-context genomic coordinates.

**Opportunity space**  
The coordinate or feature territory in which evidence could have been observed, given assay scope, callability, quality, and model eligibility.

**Opportunity state**  
The declared observability status for a coordinate, region, feature, or sample context. Examples include `callable`, `not_callable`, `not_assayed`, `low_confidence`, `filtered`, and `unknown`.

**Projection policy**  
A versioned rule for mapping one evidence substrate to another, such as coordinate → feature, feature → gene, or gene → phenotype.

**Projection result**  
The emitted mapping, burden matrix, region membership, gene assignment, or annotation surface produced by applying a projection policy.

**Evidence Topology**  
Typed relationships among preserved evidence handles. Topology organizes what evidence objects are related without converting those relationships into numerical conclusions.

**Convergence Geometry**  
Quantitative matrices, burden surfaces, recurrence surfaces, or distance/cluster structures derived over Evidence Topology and opportunity-aware projection substrates.

**Reason-ready surface**  
A VDB-emitted, traceable, policy-declared substrate that RDGP can consume without re-ingesting raw producer TEPs or independently reconstructing VAP/GSC integration.

## Governing Sentence

Coordinate evidence tells VDB what was observed; opportunity space tells VDB what could have been observed.


## Parent Doctrine Note

This document is the parent doctrine for downstream VDB projection-surface
method designs, including MPLC and CFBS. It defines shared numerator,
denominator, and projection-policy constraints. Method-specific documents may
specialize these constraints, but they should not weaken coordinate traceability,
opportunity accounting, projection-policy declaration, or anti-overclaim
boundaries.

## Required DEX Derivations

Successor DEX-VDB sessions should not treat this doctrine or its method-design
daughter documents as executable schemas. Before implementing projection-surface
builders, DEX-VDB should derive and stabilize, in order:

```text
docs/implementation/specifications/opportunity_space_spec.md
docs/implementation/specifications/projection_policy_registry_spec.md
docs/implementation/schemas/tep_vdb_projection_surface_schema.md
docs/implementation/specifications/mplc_projection_surface_spec.md
docs/implementation/specifications/cfbs_projection_surface_spec.md
```

After those specifications are stable, DEX-VDB should update the canonical VDB
→ RDGP interface document rather than creating a parallel interface surface:

```text
docs/interfaces/vdb_rdgp_interface.md
```

Contracts, implementation plans, and executable builders should follow these
specifications, not precede them.

## 1. Purpose

This document defines the scientific doctrine for opportunity-space preservation and projection-policy governance in VDB. Its purpose is to prevent downstream burden, convergence, and prioritization surfaces from treating missing technical opportunity as biological absence.

VDB should preserve observed coordinate evidence as numerator substrate, preserve opportunity space as denominator substrate, and preserve projection policy as the reversible mapping substrate that governs how coordinate evidence is related to genes, features, phenotypes, and downstream reasoning surfaces.

## 2. Scientific Motivation

VDB has moved toward coordinate-first evidence preservation because gene identity alone is not a sufficient convergence substrate for genomic evidence. Many variants are noncoding, intronic, intergenic, regulatory, splice-proximal, or otherwise not safely reducible to a single gene symbol.

A coordinate-first model protects the full observed evidence space. However, observed evidence alone is not enough for burden reasoning. A region with zero observed variants may represent true absence, poor callability, lack of assay coverage, filtering, low confidence, or unknown opportunity.

Therefore, any burden surface that counts observed variants must also declare the opportunity space over which those variants could have been observed.

## 3. Core Invariant

VDB should preserve the following invariant:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

An observation is evidence anchored to source and coordinate context. An annotation is an overlay. A projection is a governed mapping from one substrate to another. An interpretation assigns biological or clinical meaning. Reasoning ranks, prioritizes, or concludes.

VDB may organize and project evidence, but it must not collapse these layers into a single `variant → gene → score` shortcut.

## 4. Coordinate Evidence as Numerator Substrate

Coordinate evidence defines what was observed. For VAP-derived evidence, this includes reference-context variant observations such as genome build, chromosome, position or interval, reference allele, alternate allele, sample identity, quality state, normalization state, and source traceability.

This evidence is the numerator substrate for downstream burden reasoning:

```text
observed burden = count or weight of observed qualifying evidence
```

But numerator evidence is not interpretable alone. A count of zero is only meaningful if VDB also knows whether the corresponding region was observable.

## 5. Opportunity Space as Denominator Substrate

Opportunity space defines what could have been observed under the assay, callability, quality, and model constraints of the corpus.

For a region, locus, feature, or window, opportunity space may include:

```text
assayed territory
callable bases
low-confidence territory
not-assayed territory
filtered territory
unknown opportunity territory
variant-class-specific opportunity
sample-specific opportunity
```

Opportunity space is the denominator substrate for burden reasoning:

```text
burden rate = observed qualifying evidence / observable opportunity
```

A burden surface without opportunity accounting risks treating technical absence as biological absence. VDB must not make that mistake.

## 6. Null, Absence, Missingness, and Callability States

VDB should distinguish at least the following states:

```text
observed
absent_with_opportunity
not_callable
not_assayed
low_confidence
filtered
unknown
```

These states are not interchangeable.

`absent_with_opportunity` means evidence could reasonably have been observed but was not observed. `not_callable` means the region was assayed but cannot support a confident absence claim. `not_assayed` means the region was outside the observable assay scope. `unknown` means VDB cannot safely classify the opportunity state.

Future implementations may refine these states, but they must not collapse them into a single missing or zero state.

## 7. Relationship to WES and WGS

WES and WGS have different opportunity spaces.

For WES, opportunity is concentrated around captured or otherwise observable regions. Noncoding observations may exist, but absence outside captured or callable territory is usually not interpretable as biological absence.

For WGS, opportunity is broader but still not uniform. Coverage, mappability, repeats, GC content, alignment ambiguity, variant class, and quality filters still shape what could have been observed.

Therefore, VDB should not treat WES and WGS as sharing the same denominator model unless that equivalence is explicitly declared and justified by a policy.

## 8. Projection Policy as Reversible Mapping Substrate

A projection policy is a versioned rule that maps evidence from one substrate to another. Examples include:

```text
coordinate → gene body ±10 kb
coordinate → TSS ±10 kb
coordinate → splice-proximal interval
coordinate → regulatory feature
regulatory feature → linked gene
gene → phenotype-scoped GSC prior
```

Projection policies are not biological truth. They are declared mapping rules that produce projection results.

Every projection result should preserve:

```text
projection_policy_id
projection_policy_version
source substrate
target substrate
mapping confidence
lossiness state
source coordinate traceability
```

Where possible, projections should be reversible back to coordinate evidence. When reversibility is incomplete, the lossiness must be explicit.

## 9. Relationship to Evidence Topology

Evidence Topology organizes preserved evidence handles into typed relationships. It should precede Convergence Geometry because geometry should be derived from declared relationships, not from ad hoc joins over raw producer artifacts.

Topology answers:

```text
What evidence objects are connected, under what relationship type, policy, and provenance?
```

Topology does not answer:

```text
Is this locus causal?
Is this region disease-associated?
Which gene should be prioritized?
```

Those questions require downstream geometry and reasoning layers.

## 10. Relationship to Convergence Geometry

Convergence Geometry derives numerical structures over topology and opportunity-aware projections. These may include burden matrices, recurrence surfaces, distance structures, cluster scores, or observed-versus-expected summaries.

Geometry should be opportunity-aware. A matrix of observed counts without denominator context is not sufficient for responsible reasoning.

Geometry must not overclaim. It may describe convergence, burden, recurrence, clustering, or candidate signals. It must not claim causality, diagnosis, pathogenicity, or association-level proof unless a downstream validated reasoning layer explicitly owns that claim.

## 11. Relationship to TEP-VDB and RDGP

TEP-VDB is the intended reason-ready transport product emitted by VDB after the relevant topology, opportunity, projection-policy, and geometry layers are declared. It should carry coordinate evidence, opportunity states, projection policies, projection results, topology/geometry identifiers, validation receipts, and source traceability.

RDGP consumes TEP-VDB surfaces. RDGP should not independently reconstruct VAP/GSC integration, infer hidden opportunity states, or treat projection results as source truth.

The intended conceptual architecture is:

```text
coordinate evidence
    → topology
        → declared projection policies
            → projection memberships
                → opportunity-aware geometry
                    → reason-ready TEP-VDB
                        → RDGP
```

Implementation may materialize some projection memberships before numerical
geometry, because burden matrices, locus/window memberships, and post hoc
annotations depend on declared projection policies. The invariant is not that
every projection waits until after geometry; the invariant is that every
projection is policy-declared, traceable to coordinate evidence, opportunity
aware when used for burden reasoning, and bounded by anti-overclaim labels.

## 12. Relationship to MPLC and CFBS

MPLC and CFBS are downstream projection-surface designs that depend on this doctrine.

MPLC uses opportunity space to compare GSC-prior loci against matched non-prior background loci. Without opportunity accounting, MPLC could mistake larger, more callable, or more assay-visible target loci for true burden excess.

CFBS uses opportunity space to scan coordinate windows before post hoc biological annotation. Without opportunity accounting, CFBS could mistake technical visibility, mappability artifacts, or assay structure for biological clustering.

This document is therefore a parent doctrine for MPLC and CFBS. Those method designs define specific reasoning rooms; this document defines the shared numerator, denominator, and projection-policy rules those rooms must obey.

## 13. Non-Goals

This document does not define a final implementation schema.

This document does not define a complete opportunity-space file format.

This document does not define a complete Convergence Geometry specification.

This document does not define a complete TEP-VDB export specification.

This document does not define MPLC or CFBS implementation schemas.

This document does not define RDGP scoring, diagnosis, or prioritization logic.

DEX-VDB should derive implementation specifications, schemas, validators, and tests from this doctrine in later documents.

## 14. DEX-VDB Implementation Guardrails

Future DEX-VDB implementation should preserve these guardrails:

```text
1. Every burden surface declares its opportunity basis.
2. Every zero-burden state distinguishes absence from not-callable, not-assayed, filtered, and unknown.
3. Every projection declares a projection policy ID and version.
4. Every projection result remains traceable to coordinate evidence.
5. Every lossy projection declares its lossiness.
6. WES and WGS opportunity models remain distinct unless explicitly harmonized.
7. Topology precedes geometry.
8. Geometry remains descriptive or exploratory unless downstream validation supports stronger claims.
9. TEP-VDB transports reason-ready surfaces without forcing RDGP to re-ingest producer TEPs.
10. RDGP performs downstream reasoning, ranking, and prioritization.
11. Burden-readiness must not be declared unless opportunity-space state is present or explicitly marked as unmodeled.
```

## 15. Validation Implications

Later validators should check that:

```text
burden outputs include opportunity declarations
zero states are not ambiguous
projection policies are declared and versioned
projection results trace back to source coordinates
unknown opportunity is preserved rather than coerced to zero
method surfaces inherit the correct opportunity model
MPLC and CFBS outputs declare their projection policies and opportunity bases
anti-overclaim labels are present where applicable
opportunity-unmodeled states are explicit when true opportunity accounting is unavailable
```

A TEP-VDB surface that lacks opportunity accounting may still be preserved as evidence, but it should not be treated as fully reason-ready for burden-based RDGP interpretation.

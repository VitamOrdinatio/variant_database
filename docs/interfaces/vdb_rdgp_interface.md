# VDB ↔ RDGP Interface

> Status: VDB-local interface derivation.
> This document derives from the ecosystem VDB ↔ RDGP Truth Layer and expresses
> the interface from the VDB repository perspective. It is public-facing VDB
> documentation, not the private ecosystem authority document, not a full
> TEP-VDB payload schema, and not an RDGP scoring specification.

## Purpose

This document defines how VDB exposes, emits, and later accepts evidence across
its interface with RDGP.

The interface exists to ensure that VDB-resident and VDB-emitted evidence can be
consumed by RDGP without loss of:

```text
provenance
source identity
coordinate identity
sample-observation identity
namespace context
uncertainty state
opportunity context
projection-policy context
validation receipts
future interpretability
```

VDB persists, brokers, projects, and transports evidence.

RDGP consumes VDB-exposed evidence surfaces, reasons over them, and may later
return RDGP-derived reasoning products to VDB as additive evidence.

---

# 1. Derivation Note

This file is the VDB-local derivation of the ecosystem VDB ↔ RDGP interface
Truth Layer.

The Truth Layer defines cross-repository doctrine. This VDB-local document
translates that doctrine into VDB-facing expectations:

```text
what VDB must expose
what VDB must emit
what VDB must preserve
what VDB must not collapse
what RDGP may expect from VDB-produced surfaces
what VDB may later accept back from RDGP as returned evidence products
```

This file should not weaken the upstream doctrine around provenance,
identity-space boundaries, uncertainty preservation, query surfaces,
TEP transport, opportunity state, projection policies, anti-overclaim labels, or
bidirectional evidence lifecycle.

---

# 2. Interface Overview

The VDB ↔ RDGP interface has three routes.

```text
Route A:
    VDB query surfaces → RDGP

Route B:
    VDB → TEP-VDB projection surfaces → RDGP

Route C:
    RDGP → RDGP-TEP reasoning products → VDB
```

Current VDB development is primarily focused on Route B:

```text
VDB → TEP-VDB → RDGP
```

However, the interface remains bidirectional. RDGP-derived outputs should be able
to return to VDB later as additive reasoning evidence without overwriting source
evidence.

---

# 3. Architectural Boundary

The interface preserves the following system boundary:

```text
VDB  = evidence persistence, brokerage, projection, transport
RDGP = evidence reasoning, prioritization, confidence, interpretation
```

The core invariant is:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

VDB may expose observations, annotations, overlays, opportunity declarations,
projection-policy declarations, projection memberships, method surfaces, and
validation receipts.

RDGP may reason over those surfaces.

VDB must not silently become RDGP.

RDGP must not silently become VDB.

---

# 4. VDB Responsibilities

VDB owns:

```text
evidence persistence
producer package registration
TEP ingestion and lineage preservation
coordinate evidence preservation
feature evidence preservation
namespace brokerage
semantic persistence
query-surface generation
overlay persistence
opportunity-space declaration
projection-policy declaration
projection-surface emission
TEP-VDB packaging
validation receipt preservation
returned RDGP evidence-product persistence
```

Examples of VDB-resident or VDB-emitted evidence include:

```text
variant evidence
sample-specific coordinate observations
transcript evidence
feature evidence
gene evidence
phenotype overlays
GSC semantic prior overlays
opportunity-space declarations
projection-policy declarations
projection memberships
MPLC projection surfaces
CFBS projection surfaces
validation receipts
provenance records
namespace relationships
```

VDB does not perform RDGP prioritization, diagnosis, causal inference, or
candidate ranking unless such outputs are explicitly persisted as returned
RDGP-derived evidence products.

---

# 5. RDGP Responsibilities

RDGP owns:

```text
evidence consumption
evidence interpretation
candidate generation
prioritization
confidence modeling
inheritance reasoning
reasoning-output generation
future reasoning frameworks
```

Examples of RDGP outputs include:

```text
candidate scores
candidate rankings
confidence assignments
inheritance assessments
prioritized_genes.tsv
prioritized regions or candidate loci
reasoning explanations
```

RDGP must not own source evidence persistence.

RDGP must not silently alter source evidence identities.

RDGP may return reasoning outputs to VDB as additive evidence products through a
future RDGP-TEP return route.

---

# 6. Interface Routes

## 6.1 Route A: VDB Query Surfaces → RDGP

VDB may expose RDGP-facing query surfaces over VDB-resident evidence.

Examples include:

```text
sample-gene evidence surfaces
variant-gene aggregation surfaces
provenance-rich evidence summaries
overlay-enriched gene surfaces
future functional evidence surfaces
```

RDGP should consume stable query surfaces rather than depending directly on VDB
persistence layouts.

Query surfaces are stability boundaries.

## 6.2 Route B: VDB → TEP-VDB Projection Surfaces → RDGP

VDB may emit TEP-VDB as a reason-ready transport product for RDGP.

TEP-VDB is the preferred vehicle for projection-surface workflows.

A TEP-VDB projection-surface product carries the source corpus, shared
substrates, opportunity context, projection-policy identity, method-specific
surfaces, validation receipts, traceability, and anti-overclaim labels needed for
RDGP to reason without reconstructing producer integration.

Normal RDGP consumption of TEP-VDB should not require RDGP to re-ingest VAP or
GSC packages to recreate the same surface. Such re-integration should only occur
in explicit audit or debug workflows.

## 6.3 Route C: RDGP → RDGP-TEP → VDB

RDGP may later emit reasoning products back to VDB as additive evidence products.

Examples include:

```text
candidate rankings
confidence assessments
inheritance interpretations
prioritization explanations
future statistical analyses
future functional interpretations
```

Recommended lifecycle:

```text
     VDB
      ↓
   TEP-VDB
      ↓
     RDGP
      ↓
RDGP Reasoning
      ↓
   RDGP-TEP
      ↓
     VDB
```

Returned RDGP products must not overwrite observed evidence, semantic priors,
source assertions, historical reasoning products, or producer-derived evidence.

They should persist as additive reasoning evidence with explicit methodology,
release, input, and temporal provenance.

---

# 7. TEP-VDB as Interface Vehicle

For projection-surface workflows, TEP-VDB is the VDB → RDGP vehicle.

TEP-VDB is not merely a file bundle. It is the reason-ready transport product
that carries enough declared evidence context for RDGP to consume VDB-produced
projection surfaces safely.

## 7.1 Minimum Interface Payload

The following content classes form the minimum TEP-VDB interface payload for
projection-surface consumption.

```text
TEP-VDB envelope
TEP-VDB manifest
source corpus index
source TEP index
shared substrate index
coordinate observations
sample-specific variant observations
feature/gene/overlay declarations
opportunity-space reference or explicit unmodeled state
projection policy registry reference
projection surface index
method surface manifests
method-specific projection rooms, such as MPLC and CFBS
validation receipt index
source traceability index
anti-overclaim label set
```

RDGP may rely on these content classes existing or being referenced when it
consumes a VDB-emitted TEP-VDB projection-surface product.

## 7.2 What This Interface Does Not Freeze

This interface does not freeze:

```text
exact table filenames
exact column order
exact serialization format
exact package directory layout
exact validator command-line interface
exact builder module names
exact RDGP import API
exact RDGP-TEP return schema
```

Those details belong to VDB implementation schemas, method-specific projection
surface specifications, validation plans, system contracts, implementation
plans, and future RDGP-TEP documents.

## 7.3 TEP-VDB Consumption Rule

When RDGP consumes a VDB-emitted TEP-VDB projection surface, RDGP consumes the
surface that VDB emitted and the validation receipts attached to it.

RDGP must not silently reconstruct the same VAP/GSC integration independently.

RDGP may perform independent reconstruction only under an explicit audit/debug
mode that is separately labeled and does not replace the VDB-emitted surface.

---

# 8. Identity Spaces

The interface must preserve identity-space boundaries.

Important identity spaces include:

```text
sample_id
coordinate_variant_handle
sample_variant_observation_id
variant_id / variant_handle
transcript_id
gene_id
(sample_id, gene_id)
(phenotype_scope, gene_id)
gsc_release_id
projection_surface_id
projection_membership_id
rdgp_run_id
rdgp_tep_id
```

The v1 RDGP compatibility identity is usually:

```text
(sample_id, gene_id)
```

That identity is distinct from:

```text
coordinate_variant_handle
sample_variant_observation_id
(phenotype_scope, gene_id)
gsc_release_id
projection_surface_id
projection_membership_id
```

Phenotype-scoped evidence remains distinct from sample-scoped evidence.

Source identity remains distinct from canonical identity.

Projection membership remains distinct from observed variant identity.

---

# 9. Sample-Gene v1 Compatibility Surface

The v1 compatibility surface remains:

```text
(sample_id, gene_id)
```

This surface supports gene-centric RDGP reasoning and may contain:

```text
variant-derived evidence
annotation-derived evidence
semantic prior evidence
future functional evidence
provenance summaries
uncertainty summaries
evidence-channel summaries
```

This surface remains important, but it is not the entire VDB ↔ RDGP interface.

## 9.1 Required v1 Evidence Components

For v1 sample-gene consumption, VDB should support evidence components such as:

```text
sample_id
sample_label or external sample name
source_pipeline
ingest_timestamp
variant_id or variant_handle
coordinate_variant_handle
sample_variant_observation_id
chrom
pos
ref
alt
variant_type
quality_flag or filter/pass status
gene_id and/or gene_symbol, if mapped
zygosity, if available
mitochondrial flag, if applicable
annotation_id
consequence
impact_class
population_frequency
clinical_significance
transcript_id
annotation_source
annotation_version
gene_mapping_status
```

Missing fields must remain explicit. RDGP must not silently interpret missing
frequency as rare, missing clinical significance as benign, or missing overlay
support as negative evidence.

## 9.2 Sample-Gene Aggregation

Each v1 sample-gene aggregation record should represent a unique:

```text
(sample_id, gene_id)
```

The record may include:

```text
variant_count
rare_variant_count
high_impact_variant_count
pathogenic_variant_count
likely_pathogenic_variant_count
vus_variant_count
likely_benign_variant_count
benign_variant_count
max_variant_severity
has_low_quality_evidence
phenotype-scoped semantic prior summary
future expression or functional evidence summary
provenance_summary
uncertainty_summary
```

Per-class counts must be computed after a declared annotation precedence or
partitioning policy, not by naïvely counting all annotation rows.

---

# 10. TEP-VDB Projection Surface Expectations

Projection surfaces are method-specific reasoning rooms emitted by VDB inside
TEP-VDB.

Examples include:

```text
MPLC = Matched Prior-Locus Contrast
CFBS = Coordinate-First Burden Scan
future projection-surface methods
```

Projection surfaces may include:

```text
method-specific manifests
membership tables
burden matrices
recurrence matrices
matched background sets
null manifests
candidate interval sets
post hoc annotation overlays
validation receipts
source traceability
anti-overclaim labels
```

Projection surfaces are not RDGP reasoning outputs. They are VDB-emitted,
policy-declared, opportunity-aware evidence surfaces that RDGP can reason over.

---

# 11. Opportunity and Projection Policy Requirements

## 11.1 Opportunity Requirement

Any RDGP-facing burden, recurrence, observed/expected, or empirical-null surface
must declare an opportunity basis or explicitly declare opportunity as unmodeled.

A surface must not be labeled burden-ready unless its opportunity-space state is
present and acceptable under the relevant VDB opportunity specification.

Zeros are meaningful only under an appropriate observable opportunity model.

Unknown, not assayed, not callable, filtered, and opportunity-unmodeled states
must remain distinguishable.

## 11.2 Projection Policy Requirement

Any VDB-emitted projection surface must declare the policy rules used to create
its:

```text
regions
windows
loci
memberships
filters
annotations
background sets
null models
emission package
```

Relevant references may include:

```text
opportunity_model_id
projection_policy_registry_id
projection_policy_id
variant_filter_policy_id
window_policy_id
background_matching_policy_id
candidate_interval_assembly_policy_id
null_model_id
posthoc_annotation_policy_id
emission_policy_id
```

Projection policies must remain versioned, traceable, and inspectable.

---

# 12. Countable Observation and Membership Rules

Burden counts must operate over sample-specific observations rather than
duplicated annotation rows.

The interface distinguishes:

```text
coordinate_variant_handle       = normalized coordinate/reference-context identity
sample_variant_observation_id   = sample-specific observation of that variant
projection_membership_id        = membership of an observation in a window/locus/feature/annotation
```

Multiple transcript, feature, gene, regulatory, GSC-prior, or annotation
memberships may exist for one observed variant.

Those memberships must not create additional observed variants.

This rule applies to both v1 sample-gene surfaces and TEP-VDB projection
surfaces.

---

# 13. MPLC and CFBS Consumption Expectations

This interface names method-specific consumption expectations. Detailed
field-level contracts live in the method-specific VDB implementation
specifications.

## 13.1 MPLC

MPLC is a prior-informed projection surface.

VDB emits MPLC to support RDGP reasoning over whether phenotype-scoped GSC-prior
loci carry more local qualifying variant burden than matched non-prior
background loci under a declared patient, assay, opportunity, filtering, and
matching context.

MPLC consumption expectations:

```text
GSC target loci remain phenotype-scope aware.
Background loci are matched non-prior loci, not proven non-disease genes.
Target/background overlap is declared, excluded, or flagged.
Matching policies are declared.
Opportunity basis is declared for burden-ready claims.
exploratory_empirical_p_value is not a control-matched disease-association p-value.
```

## 13.2 CFBS

CFBS is a coordinate-first projection surface.

VDB emits CFBS to support RDGP reasoning over coordinate intervals nominated from
coordinate-space burden patterns before gene, GSC, regulatory, disease-prior, or
RDGP labels are used for interpretation.

CFBS consumption expectations:

```text
Scan windows are not selected by GSC prior labels.
Candidate intervals are nominated before post hoc biological annotation.
Post hoc GSC/gene/regulatory annotations remain marked as post hoc.
Phenotype-scoped GSC annotations are not silently combined.
Opportunity basis is declared for burden-ready claims.
exploratory_empirical_p_value is not a control-matched disease-association p-value.
```

RDGP must not reinterpret CFBS candidates as disease-associated regions,
pathogenic regions, causal loci, or diagnostic results unless a separate,
validated downstream reasoning layer explicitly owns and supports that claim.

---

# 14. Overlay Governance

Overlay evidence is enrichment evidence.

Overlay evidence is not sample evidence.

Overlay absence is not negative evidence.

Overlay presence is not deterministic proof.

RDGP remains responsible for interpreting overlay significance.

## 14.1 GSC Overlays

GSC may provide phenotype-scoped semantic prior evidence such as:

```text
curated disease membership
semantic prior score
consensus support score
source list and provenance
phenotype-gene relationship support
```

GSC-derived support must be interpreted as an evidence-model output with
provenance, not as binary gene set membership.

GSC-derived priors must remain phenotype-scope aware.

RDGP may consume GSC overlays through VDB query surfaces or TEP-VDB projection
surfaces, but phenotype scopes must not be silently combined.

## 14.2 RSP and Future Functional Evidence

Future RSP or functional evidence may include:

```text
differential expression status
effect size / fold change
network convergence score
tissue/context metadata
provenance to dataset/run/contrast
```

Functional evidence should be interpreted as dataset-linked and
contrast-specific evidence, not sample-specific or phenotype-defining truth.

Future evidence should integrate through query-surface or TEP-style extension
rather than interface redesign.

---

# 15. Provenance Requirements

For RDGP-facing evidence records and projection surfaces, VDB should preserve
provenance sufficient to reconstruct:

```text
source repository
source package
source artifact
TEP lineage
ingestion lineage
namespace-resolution lineage
aggregation lineage
overlay-attachment lineage
projection-policy lineage
opportunity-model lineage
validation lineage
RDGP reasoning lineage, for returned products
```

Every RDGP prioritization output should be explainable in terms of:

```text
which source evidence contributed
which producer packages contributed
which projection or aggregation policies were used
which annotations and overlays were used
which opportunity model was used, if burden reasoning was involved
which RDGP method and release generated the reasoning output
```

If RDGP cannot explain this, the VDB ↔ RDGP interface is insufficient.

---

# 16. Uncertainty and Null Handling

The interface must preserve uncertainty.

Examples include:

```text
missing annotations
ambiguous mappings
unresolved identities
conflicting evidence
incomplete evidence
unknown opportunity
not assayed regions
not callable regions
opportunity unmodeled states
```

RDGP should not be forced to infer uncertainty from absence.

## 16.1 Null Handling Contract

Missing values must be represented as NULL or explicit placeholders.

Downstream systems must not infer biological meaning from missing values.

Aggregation and projection metrics must distinguish:

```text
zero       = observed absence under an appropriate observable opportunity model
null       = unknown, not measured, unresolved, or unavailable
unmodeled  = no safe opportunity/denominator model is available
```

---

# 17. Namespace Brokerage Expectations

RDGP consumes namespace-brokered evidence.

Canonical identities may support interoperability. However:

```text
source identities remain recoverable
brokerage remains additive
normalization remains traceable
identity authority remains external to RDGP
```

VDB should not erase source namespace context while providing canonical
RDGP-facing surfaces.

---

# 18. Quality and Edge-Case Handling

## 18.1 Low-Quality Variants

Low-quality or filtered variants should not be silently discarded from all
contexts unless explicitly configured.

RDGP should be able to:

```text
exclude them from scoring
include them with penalty or warning
report them separately
```

## 18.2 Multi-Allelic Variants

VDB should normalize multi-allelic events in a way RDGP can consume
consistently. If not fully supported initially, the limitation must be explicit.

## 18.3 Structural Variants

Structural variants may not fit the same schema as SNVs/indels. The interface
should preserve placeholders and compatibility strategy where possible.

## 18.4 Mitochondrial Variants and Heteroplasmy

For mitochondrial variants:

```text
VDB should allow explicit mitochondrial labeling.
Heteroplasmy fields may be absent in early versions but should be anticipated.
RDGP must not assume diploid nuclear-style interpretation always applies.
```

## 18.5 Noncoding and Unmapped Evidence

Noncoding, intronic, intergenic, regulatory, splice-proximal, and unmapped
coordinate evidence should remain first-class evidence in VDB and TEP-VDB.

Such evidence may be outside the v1 sample-gene surface, but it is not outside
the full VDB ↔ RDGP interface.

---

# 19. RDGP-TEP Return-Leg Expectations

RDGP-derived outputs returning to VDB should be treated as evidence products,
not persistence-layer updates.

Returned RDGP products should preserve:

```text
rdgp_tep_id
rdgp_run_id
rdgp_release_id
rdgp_method_id
rdgp_method_version
source_tep_vdb_id or source_query_surface_id
source_evidence_inputs
reasoning_parameters
reasoning_outputs
confidence assignments
candidate rankings
temporal context
validation receipts
```

Returned products must not overwrite:

```text
observed variant evidence
source annotations
GSC semantic priors
RSP functional evidence
historical RDGP reasoning outputs
```

Instead, returned products coexist as additive reasoning evidence.

---

# 20. Interface Guarantees

The VDB ↔ RDGP interface guarantees:

```text
evidence provenance preservation
source identity preservation
coordinate identity preservation
sample-observation identity preservation
uncertainty preservation
overlay attachability
aggregation reproducibility
stable query surfaces
TEP-VDB projection-surface portability
additive namespace brokerage
opportunity-state visibility for burden reasoning
projection-policy visibility for derived surfaces
validation receipt preservation
anti-overclaim label preservation
bidirectional evidence lifecycle support
future extensibility
```

---

# 21. Failure Conditions

The interface should reject workflows that require:

```text
provenance loss
source identity erasure
hidden aggregation
hidden overlay attachment
uncertainty concealment
destructive normalization
irreversible evidence compression
unversioned projection policies
unmodeled opportunity treated as burden-ready
RDGP-side re-integration of VAP/GSC in normal TEP-VDB consumption
sample evidence and phenotype prior evidence collapse
exploratory empirical p-values interpreted as control-matched association p-values
RDGP reasoning outputs overwriting source evidence
```

Such behaviors violate VDB ↔ RDGP interface doctrine.

---

# 22. Relationship to VDB Implementation Documents

This interface document defines VDB-local interoperability doctrine. Detailed
implementation behavior is derived in VDB-local implementation documents.

Relevant implementation documents include:

```text
docs/implementation/specifications/opportunity_space_spec.md
docs/implementation/specifications/projection_policy_registry_spec.md
docs/implementation/schemas/tep_vdb_projection_surface_schema.md
docs/implementation/specifications/mplc_projection_surface_spec.md
docs/implementation/specifications/cfbs_projection_surface_spec.md
```

This interface does not replace those documents.

Those documents make the interface executable through schemas, method-specific
surface specifications, validation plans, system contracts, implementation
plans, builders, and validators.

---

# 23. Non-Goals

This document does not define:

```text
exact SQL schemas
exact Python classes
exact file names for generated projection tables
RDGP scoring implementation details
MPLC or CFBS field-level implementation contracts
complete TEP-VDB package implementation details
RDGP-TEP implementation schema
builder execution order
validator command-line interfaces
```

Those belong in implementation specs, schemas, validation plans, contracts,
implementation plans, and future RDGP-return documentation.

---

# 24. Summary

VDB persists, brokers, projects, and transports genomic evidence.

RDGP consumes VDB-exposed evidence surfaces, reasons over them, and may emit
reasoning products back to VDB as additive evidence.

The VDB ↔ RDGP interface supports:

```text
VDB query surfaces → RDGP
VDB-emitted TEP-VDB projection surfaces → RDGP
RDGP-emitted RDGP-TEP reasoning products → VDB
```

The v1 sample-gene surface remains a valid compatibility route, but the modern
interface also supports coordinate-first, opportunity-aware, policy-declared
projection surfaces such as MPLC and CFBS.

TEP-VDB is the preferred vehicle for projection-surface workflows. Its minimum
interface payload includes source corpus identity, shared substrates,
coordinate/sample-observation identity, opportunity context, projection-policy
identity, method surfaces, validation receipts, traceability, and
overclaim-prevention labels.

The interface exists to ensure that evidence can move between persistence and
reasoning layers without losing provenance, uncertainty, identity context,
namespace context, opportunity context, projection-policy context, validation
context, or future interpretability.

# rdgp_query_surface_schema.md

## Purpose

The RDGP Query Surface Schema defines the governed VDB-authored evidence surface intended for downstream Rare Disease Gene Prioritization (RDGP) reasoning.

The purpose of this schema is to expose a stable, provenance-complete, namespace-resolved, uncertainty-aware `(sample_id, gene_id)` evidence state that RDGP can reason over without re-solving upstream persistence, identity, aggregation, or evidence-union problems.

RDGP consumes evidence.

VDB prepares governed evidence surfaces.

---

# Scope

This schema governs:

```text
TEP-VDB outbound surfaces
RDGP-facing query surfaces
sample-gene evidence states
variant burden aggregation
GSC overlay attachment
phenotype context
inheritance-ready fields
mechanism/context hooks
confidence and uncertainty decomposition
provenance summaries
query-surface versioning
RDGP return-path requirements
```

This schema does not govern:

```text
RDGP scoring logic
RDGP prioritization logic
RDGP confidence assignment
RDGP explanation generation
clinical interpretation
diagnosis
```

---

# Core Principle

## Flattened But Not Collapsed

The RDGP query surface may be flattened for execution.

It must not be semantically collapsed.

A TSV surface may exist for RDGP convenience.

A nested JSON object must remain the authoritative representation.

Recommended export pattern:

```text
TEP-VDB full object
    nested JSON
    provenance-rich
    semantically complete
    authoritative

RDGP query surface
    flattened TSV
    stable
    sample_id × gene_id
    execution-friendly
    non-authoritative convenience surface
```

---

# VDB / RDGP Boundary

VDB owns:

```text
persistence policy
namespace arbitration
query-surface construction
aggregation policy
evidence-union governance
TEP-VDB export
```

RDGP owns:

```text
biological reasoning
gene prioritization
confidence modeling
inheritance reasoning
explanation generation
RDGP-TEP emission
```

RDGP must not be required to reconstruct upstream VAP, GSC, RSP, or VDB evidence topology.

---

# Bidirectional Evidence Flow

The VDB/RDGP relationship is sequentially bidirectional.

```text
VDB
    →
RDGP
    governed evidence surface

RDGP
    →
VDB
    RDGP-TEP reasoning evidence
```

RDGP outputs must return to VDB as new reasoning evidence.

RDGP outputs must not overwrite VAP, GSC, RSP, or VDB-preserved evidence.

---

# Required Reasoning Identity

Every RDGP-facing record must expose a stable reasoning identity:

```text
sample_id
gene_id
gene_symbol
canonical_gene_id
source_gene_ids
source_gene_symbols
namespace_resolution_status
ontology_resolution_events
```

The primary reasoning grain is:

```text
sample_id × gene_id
```

Namespace resolution status must remain explicit.

Supported namespace states include:

```text
exact
alias_resolved
deprecated_resolved
ambiguous
unresolved
not_evaluated
```

---

# Query Surface Metadata

Every RDGP-facing surface must expose query-surface identity.

Required fields:

```text
query_surface_id
query_surface_name
query_surface_version
query_surface_type
tep_vdb_id
tep_vdb_version
vdb_release_id
vdb_export_timestamp
aggregation_policy_version
namespace_policy_version
annotation_precedence_policy_version
null_semantics_policy_version
```

This allows RDGP to distinguish the same evidence under different VDB policies.

---

# Variant Evidence Burden

VDB owns aggregation from variant-level observations into gene-level burden fields.

Recommended fields:

```text
variant_count
rare_variant_count
high_impact_variant_count
pathogenic_variant_count
likely_pathogenic_variant_count
vus_variant_count
benign_variant_count
likely_benign_variant_count
max_variant_severity
has_low_quality_evidence
contributing_variant_ids
variant_provenance_summary
```

Aggregation policy must be versioned.

RDGP must not infer aggregation rules from raw counts.

---

# Evidence Channels

Evidence channels must remain decomposed.

Recommended channels:

```text
variant_evidence
phenotype_prior_evidence
gsc_overlay_evidence
transcriptomic_evidence
network_or_pathway_evidence
mechanism_evidence
quality_evidence
provenance_evidence
inheritance_evidence
identity_resolution_evidence
```

RDGP must not receive a single collapsed support score.

---

# Phenotype Context

GSC-derived evidence is meaningful only within phenotype context.

Recommended fields:

```text
selected_phenotype
phenotype_id
phenotype_label
phenotype_source
phenotype_match_status
phenotype_overlay_version
```

Phenotype missingness must remain explicit.

---

# GSC Overlay Fields

For each `(sample_id, gene_id)` surface record, VDB should expose GSC overlay context when available.

Recommended fields:

```text
gsc_consensus_score
gsc_support_tier
gsc_source_count
gsc_source_list
gsc_weight_tier_summary
gsc_release_id
gsc_tep_id
gsc_provenance_summary
gsc_overlay_status
```

Required semantic rule:

```text
no_gsc_match ≠ negative evidence
```

---

# Inheritance-Ready Fields

The RDGP surface should expose inheritance-ready fields even if incomplete.

Recommended fields:

```text
zygosity_state
inheritance_mode
inheritance_support
inheritance_conflict
inheritance_uncertainty
segregation_available
family_structure_available
mitochondrial_relevance
heteroplasmy_relevance
```

Unavailable genotype or family information must be represented explicitly.

---

# Mechanism And Context Hooks

The RDGP surface should preserve future-facing biological hooks.

Recommended fields:

```text
mechanism_context
mechanism_support
mechanism_conflict
mechanism_explanation
pathway_context
tissue_context
developmental_context
temporal_context
transcript_context
interaction_context
dosage_context
oligogenic_context
constraint_context
functional_consequence_context
```

These fields may be sparse in early VDB releases.

Sparse does not mean irrelevant.

---

# Confidence And Uncertainty Decomposition

The RDGP surface must expose uncertainty explicitly.

Recommended fields:

```text
evidence_confidence
provenance_confidence
identity_confidence
phenotype_confidence
inheritance_confidence
transcriptomic_confidence
uncertainty_present
uncertainty_sources
missingness_present
conflicting_annotations_present
sparse_evidence_present
unresolved_mechanism_present
```

RDGP should never need to infer uncertainty from absence.

---

# Cohort And Stratification Context

The RDGP surface should support future cohort-aware and context-aware reasoning.

Recommended optional fields:

```text
sample_context_fields
external_metadata_context
age_context
sex_context
biosample_context
platform_context
cohort_context
```

Each contextual field must preserve:

```text
authority_class
source_reference
retrieval_or_ingestion_timestamp
null_status
conflict_status
```

This supports future questions such as age-stratified vulnerability among carriers of specific evidence architectures.

---

# Noncoding Burden And Locus-Proximity Hooks

The RDGP surface should anticipate future noncoding interpretation and enrichment workflows.

Recommended fields:

```text
noncoding_variant_count
noncoding_high_concern_count
near_gsc_locus_count
nearest_gsc_locus_summary
noncoding_locus_proximity_status
regulatory_model_support
matched_background_available
enrichment_context_available
```

Noncoding fields may be empty in early releases.

Noncoding absence must not imply biological irrelevance.

---

# Evidence Architecture Summaries

VDB may expose evidence architecture summaries to support reviewability and similarity discovery.

Recommended fields:

```text
evidence_architecture_summary
candidate_architecture_class
reviewability_state
evidence_density_summary
channel_presence_vector
```

These summaries are not RDGP conclusions.

They are VDB-prepared descriptions of evidence composition.

---

# Similar-Case Discovery Hooks

The RDGP surface may expose features useful for future similar-case discovery.

Recommended fields:

```text
similar_case_signature
evidence_similarity_features
case_comparison_ready
```

These fields support future hospital-scale discovery workflows.

They must remain provenance-aware.

---

# Provenance Requirements

Every RDGP-facing record must trace back to upstream evidence.

Required fields:

```text
source_tep_ids
source_tep_types
source_repositories
source_runs
source_artifacts
source_artifact_checksums
producer_versions
vdb_ingest_run_id
vdb_query_surface_version
vdb_export_timestamp
tep_vdb_version
vdb_release_id
```

RDGP explanations must be able to identify where evidence came from.

---

# Explainability-Ready Summaries

VDB may prepare structured summaries for RDGP explainability.

Recommended fields:

```text
evidence_summary
variant_burden_summary
gsc_overlay_summary
transcriptomic_summary
uncertainty_summary
provenance_summary
identity_resolution_summary
```

These summaries support RDGP reasoning.

They are not final interpretation.

---

# Annotation Multiplicity Preservation

The RDGP surface may flatten evidence.

It must preserve multiplicity indicators.

Required multiplicity concepts:

```text
multiple_transcript_interpretations_present
multiple_pathogenicity_assertions_present
multiple_source_annotations_present
multiple_supporting_evidence_streams_present
annotation_multiplicity_summary
```

RDGP should not be required to reconstruct multiplicity from raw upstream payloads, but it must know when multiplicity existed.

---

# Explicit Null Semantics

Major fields must distinguish:

```text
unknown
not_evaluated
not_applicable
no_match
measured_zero
present
conflicted
resolved
ambiguous
```

This applies especially to:

```text
GSC overlay status
transcriptomic support
genotype support
phenotype match
clinical annotation
gene mapping
mechanism context
external metadata context
```

---

# Surface Stability And Versioning

RDGP benefits from stable surfaces across VDB releases.

When structure changes, VDB must expose:

```text
schema version identity
aggregation policy identity
namespace policy identity
null semantics policy identity
backward compatibility notes
```

The goal is not static schemas.

The goal is deterministic interpretation across time.

---

# RDGP Return Path Requirements

RDGP outputs must be suitable for re-entry into VDB as RDGP-TEPs.

Required return-path fields:

```text
rdgp_run_id
source_tep_vdb_id
source_query_surface_id
source_surface_version
reasoning_framework_version
rdgp_output_tep_id
rdgp_output_timestamp
```

RDGP-TEPs should preserve:

```text
input evidence references
reasoning state
prioritization output
confidence decomposition
explanation artifacts
uncertainty state
```

RDGP output must be treated as reasoning evidence, not as replacement evidence.

---

# Required Invariants

## Invariant 1

The RDGP surface must preserve `(sample_id, gene_id)` reasoning identity.

---

## Invariant 2

The RDGP surface must preserve provenance back to upstream TEPs.

---

## Invariant 3

The RDGP surface must preserve namespace resolution status.

---

## Invariant 4

The RDGP surface must preserve uncertainty explicitly.

---

## Invariant 5

The RDGP surface must preserve phenotype context when GSC overlays are attached.

---

## Invariant 6

The RDGP surface must distinguish no-match from negative evidence.

---

## Invariant 7

The RDGP surface must remain stable and versioned.

---

## Invariant 8

RDGP return evidence must be re-ingestable as a distinct evidence family.

---

# Anti-Collapse Rules

## Support Score Collapse Prohibited

VDB must not provide RDGP only a single support score.

---

## GSC Overlay Collapse Prohibited

GSC evidence must not be reduced to gene plus score.

---

## Variant Burden Collapse Prohibited

Variant burden counts must remain tied to contributing variant provenance.

---

## Null Collapse Prohibited

Missing, unavailable, no-match, not-evaluated, and measured-zero states must remain distinct.

---

## Provenance Collapse Prohibited

RDGP-facing surfaces must not sever upstream TEP, artifact, run, or repository lineage.

---

## Return-Path Collapse Prohibited

RDGP outputs must not overwrite VDB source evidence.

RDGP outputs must return as new reasoning evidence.

---

# Summary

The RDGP Query Surface Schema defines a governed VDB-authored reasoning surface for RDGP.

The surface is:

```text
sample_id × gene_id centered
flattened enough for execution
provenance-complete
namespace-aware
uncertainty-aware
phenotype-aware
future-context aware
bidirectionally reusable
```

The guiding rule is:

```text
RDGP receives a reasoning-ready evidence state.

RDGP does not receive collapsed evidence.
```

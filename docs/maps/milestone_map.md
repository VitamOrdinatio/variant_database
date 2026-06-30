# Milestone Map: variant_database (VDB)

---

## Purpose

Provide a structured, persistent, queryable database for storing and integrating:

- variant calls (from VAP) 
- annotations (functional, clinical, population) 
- gene-level context (from GSC) 
- future expression evidence (from RSP) 

VDB serves as the authoritative source of genomic evidence that enables downstream systems (e.g., RDGP) to perform reproducible, interpretable analysis.

VDB also preserves producer TEP-derived evidence packages and constructs governed Phase 4 evidence structures for downstream derivation, exposure, and consumer-facing projection.

---

## Current Architecture Status

This milestone map began as a v1 relational evidence-store roadmap.

VDB has since matured into a TEP-preserving evidence architecture.

The current architecture preserves producer evidence through:

```text
Registration Units
Corpus Generations
Assertion Records
Evidence Topology
Convergence Geometry
Evidence Convergence Surfaces
Projection Views
```

The original normalized relational model remains a foundational substrate, especially for VAP-derived variant evidence, but it is no longer the complete architectural description of VDB.

This update is a lightweight LANE-respecting refresh. It preserves the original map while making the current Phase 3/Phase 4 architecture visible.

---

## Layer Ecosystem

1. producer evidence providers: VAP, GSC, future RSP
2. TEP transport and Registration Unit preservation
3. Corpus Generation scope declaration
4. Assertion Record preservation
5. Evidence Topology, Convergence Geometry, and Evidence Convergence Surface governance
6. Projection View and consumer interface layer
7. downstream reasoning layer: RDGP

---

## Terminology

- "variant-level evidence": structured observations and annotations associated with a specific variant in a specific sample
- "gene-level evidence": aggregated variant and contextual information associated with a gene for a given sample
- "authoritative evidence layer": the system of record from which downstream analytical systems retrieve genomic evidence

---

## Modern Phase 4 Doctrine

Current VDB Phase 4 doctrine:

```text
Registration Units preserve custody.
Corpus Generations declare scope.
Assertion Records preserve scientific claims.
Evidence Topology derives organization.
Convergence Geometry characterizes organization.
Evidence Convergence Surfaces govern exposure.
Projection Views represent governed evidence.
RDGP reasons.
```

This doctrine extends the original relational-data model without discarding it.

The older v1 relational model remains important for normalized evidence storage, inspection, provenance, namespace brokerage, and consumer queries.

The modern Phase 4 architecture adds governed evidence preservation, scope declaration, derivation boundaries, and projection governance.

---

## Core Data Model (v1)

The following v1 data model is foundational.

It describes the original normalized relational evidence substrate, especially for VAP-derived variant evidence.

It should be interpreted as a substrate layer, not as the complete modern VDB architecture.

VDB implements a normalized relational schema centered on variant-level evidence.

Core entities:

### Samples
- sample_id
- sample_label
- run_id
- source_pipeline
- ingest_timestamp
- assay_type

### Variants
- variant_id
- sample_id
- chrom
- pos
- ref
- alt
- variant_type
- quality_flag
- gene_id
- gene_symbol
- zygosity (if available)
- mitochondrial_flag (if applicable)

### Annotations
- annotation_id
- variant_id
- consequence
- impact_class
- population_frequency
- clinical_significance
- transcript_id
- annotation_source
- annotation_version

### Genes
- gene_id
- gene_symbol
- ensembl_gene_id (if available)
- gene_biotype (optional)

---

### Gene Identity Resolution (v1)

VDB is the authoritative namespace-resolution layer for the ecosystem.

VDB must support deterministic normalization and preservation of:

- Ensembl gene identifiers
- Entrez identifiers (if available)
- HGNC-approved gene symbols
- historical/deprecated symbols
- source-specific aliases
- unresolved or ambiguous mappings

Gene identity normalization must preserve provenance and must never silently collapse ambiguous mappings.

Namespace resolution decisions must be:

- reproducible
- traceable
- source-aware
- deterministic

VDB acts as the canonical identity broker between:

- VAP variant evidence
- GSC phenotype overlays
- future RSP convergence overlays
- RDGP reasoning inputs

---

### Gene Namespace Aliases

- alias_id
- canonical_gene_id
- alias_symbol
- alias_source
- alias_type
- resolution_status
- mapping_confidence
- provenance_note

Goal:
Preserve namespace provenance without silently discarding source-specific identity information.

---

### Example Records (v1)

Sample:
- sample_id: SAMPLE_001
- sample_label: proband_001
- run_id: RUN_2026_001
- source_pipeline: VAP_v1
- ingest_timestamp: 2026-04-19T10:32:00

Variant:
- variant_id: VAR_001
- sample_id: SAMPLE_001
- chrom: chr15
- pos: 89875948
- ref: A
- alt: G
- variant_type: SNV
- quality_flag: PASS
- gene_id: ENSG00000140521
- gene_symbol: POLG
- zygosity: heterozygous
- mitochondrial_flag: false

Annotation:
- annotation_id: ANN_001
- variant_id: VAR_001
- consequence: missense_variant
- impact_class: moderate
- population_frequency: 0.0001
- clinical_significance: VUS
- transcript_id: ENST00000268124
- annotation_source: ClinVar
- annotation_version: 2026-04

---

## Metadata Normalization Layer

VDB must normalize metadata associated with samples, runs, projects, assays, and source repositories.

VAP-derived evidence should not enter VDB as isolated variant rows. Each ingested record must remain linked to contextual metadata sufficient to support downstream stratified queries.

Metadata entities may include:

* sample_id
* run_id
* source_pipeline
* source_repository
* BioProject accession
* SRA accession
* assay_type
* sequencing_strategy
* cohort_label
* case_study_context
* organism
* sex / gender, if available
* tissue / source material, if available
* disease or phenotype label, if available
* ingest_timestamp
* metadata_source
* metadata_resolution_status

VDB should preserve missing, partial, ambiguous, or unavailable metadata explicitly.

Goal:
VDB supports biologically meaningful cross-sample and cross-cohort queries without forcing upstream repositories to flatten or over-normalize their metadata before ingestion.

---

## VAP Multi-Artifact Ingestion Strategy

VDB should ingest VAP outputs as a structured multi-artifact evidence package rather than as a single flat file.

VAP produces stage-specific TSV outputs with different downstream utilities. VDB should preserve this structure by mapping distinct VAP artifacts into appropriate relational tables or staging tables.

Representative VAP-derived artifact classes include:

* normalized variant substrates
* annotated variant substrates
* Stage 08 coding candidate substrates
* Stage 08 noncoding candidate substrates
* RDGP-oriented gene evidence substrates
* variant summary substrates
* prioritization outputs
* validation candidate outputs
* telemetry and provenance summaries
* run-level metadata artifacts

VDB ingestion should therefore support:

* artifact manifest ingestion
* source artifact identity
* artifact type classification
* stage provenance
* schema validation per artifact type
* deterministic replay of ingestion
* preservation of artifact-to-table lineage

Goal:
VDB functions as a normalized evidence warehouse for VAP-derived semantic substrates rather than a simple TSV loader.

---

## Query and View Layer

VDB must expose stable query surfaces for downstream repositories.

The core relational schema should remain normalized, but downstream systems should not be forced to reconstruct complex joins manually.

VDB should provide documented SQL queries, materialized views, or Python accessors for:

* sample-linked variant evidence
* annotation-linked variant evidence
* gene-linked variant aggregation
* `(sample_id, gene_id)` RDGP evidence records
* GSC overlay attachment
* cohort-level variant summaries
* BioProject / SRA stratified summaries
* metadata-aware filtering
* provenance-aware audit trails

The RDGP-facing query surface should produce one unique evidence record per `(sample_id, gene_id)` pair while preserving traceability to contributing variants, annotations, overlays, and source artifacts.

Goal:
VDB becomes both the authoritative evidence store and the stable query interface for downstream reasoning systems.

---

## Run-Package Ingestion and Discovery Governance

VDB v1.0 adopts a manifest-mediated run-package ingestion architecture.  Within VDB, this architecture is referred to as the VDB Discovery Engine.

Rather than ingesting isolated flat files, VDB ingests governed evidence packages originating from upstream repositories such as VAP.

Each run package may contain:

* stage-specific semantic substrates
* annotation outputs
* prioritization outputs
* validation outputs
* telemetry artifacts
* provenance artifacts
* metadata sidecars
* execution summaries
* interoperability-oriented substrates

VDB ingestion therefore operates through three coordinated layers:

### 1. Discovery Layer

Artifact discovery performs deterministic profiling of incoming artifacts including:

* column discovery
* datatype inference
* categorical value profiling
* null-state profiling
* namespace candidate detection
* metadata candidate detection
* provenance field discovery

Discovery layers do not silently mutate schemas.

They generate auditable discovery reports used for governance validation.

### 2. Governance Mapping Layer

Governance mapping aligns discovered artifacts to canonical ecosystem semantics including:

* namespace normalization
* ontology alignment
* provenance semantics
* null semantics
* stage identity
* artifact identity
* allowed value domains

### 3. Deterministic Ingestion Layer

Validated artifacts are ingested into normalized VDB relational structures while preserving:

* provenance continuity
* artifact lineage
* source identities
* run identities
* stage identities
* replayability

Goal:
VDB functions as the authoritative governed evidence nexus for the broader repository ecosystem.

---

## Interface Contract (RDGP Alignment)

VDB must support the VDB ↔ RDGP interface contract.

Specifically, VDB must guarantee that:

- all fields required by RDGP are retrievable
- variant records can be aggregated to the (sample_id, gene_id) level
- field naming aligns with the interface specification
- missing values are explicitly represented (not inferred)
- provenance is preserved for all records

Failure to meet this contract will break downstream prioritization.

---

## Strategic Value (High Signal)

This repo demonstrates:
  - SQL / relational data modeling 
  - genomic data normalization 
  - cross-sample reasoning 
  - integration across pipelines 
  - clinical data thinking (auditability, provenance) 

This is what separates:
`“pipeline user” → “bioinformatics analyst”`

---

## Standard Access Pattern (v1)

Downstream systems must be able to retrieve from VDB:

- sample-linked variant records
- annotation-linked variant records
- normalized gene identifiers
- provenance metadata
- gene-level aggregation metrics as defined in the VDB ↔ RDGP interface contract
    - variant_count
    - rare_variant_count
    - high_impact_variant_count
    - pathogenic_variant_count
    - likely_pathogenic_variant_count
    - vus_variant_count
    - likely_benign_variant_count
    - benign_variant_count
    - max_variant_severity


## Milestones

The original M1–M8 milestones describe the foundational relational, namespace, ingestion, query, provenance, edge-case, and integration substrate.

They remain useful as historical and foundational milestones.

They are now extended by the modern Phase 3/Phase 4 TEP preservation and evidence-derivation architecture.

Current active frontier:

```text
Phase 3:
    TEP package registration and Registration Unit substrate preparation

Phase 4.1:
    Registration Unit preservation and readiness validation

Phase 4.2:
    Corpus Generation scope declaration and validation

Phase 4.3+:
    Assertion Records, Evidence Topology, Convergence Geometry,
    Evidence Convergence Surfaces, and Projection Views
```



### M1 — Core Schema (Data Model Exists)

Define and implement core tables:
  - samples 
  - variants 
  - genes 
  - annotations 
Relationships:
  - variant ↔ sample 
  - variant ↔ gene 
  - variant ↔ annotation 
Basic fields:
  - genomic position (chr, pos, ref, alt) 
  - gene symbol 
  - variant type 
  - sample ID 

Ensure:
  - primary keys defined for all tables
  - foreign key relationships enforced
  - gene mapping is normalized (no free-text duplication)
  - canonical namespace-resolution strategy defined
  - alias preservation behavior defined
  - ambiguous mapping behavior explicitly documented

Goal:
A normalized schema capable of preserving genomic evidence identity and namespace provenance deterministically.

---

### M2 — Namespace Resolution Layer

Implement deterministic namespace handling for:

- Ensembl IDs
- HGNC symbols
- historical aliases
- source-specific gene identifiers

Requirements:

- canonical identity preservation
- alias traceability
- provenance-aware mapping
- unresolved-state preservation
- no silent namespace collapse

Validation should include:

- deterministic normalization behavior
- reproducible alias resolution
- ambiguous mapping detection
- source-aware namespace provenance

Goal:
VDB becomes the authoritative identity-resolution layer for downstream ecosystem integration.

---

### M3 — Ingestion from VAP (Data Enters System)
  - Parse VAP output (VCF or derived table) 
  - Insert into database 
  - Ensure: 
      - no duplication issues 
      - consistent formatting 
      - reproducible ingestion 

Goal:
You can run VAP → load results into VDB reliably

---

### M4 — Annotation Linkage (Meaningful Data Layer)
Extend schema to support:
  - functional consequence 
  - population frequency (even mock initially) 
  - clinical significance (placeholder or real) 
Separate annotation table (important):
  - don’t overload variant table 

Ensure:
  - multiple annotation rows per variant are supported
  - annotation_source and annotation_version are preserved
  - conflicting annotations remain detectable

Goal:
Variants are no longer raw—they are interpretable

---

### M5 — Query Layer

VDB must expose all aggregation metrics required for deterministic downstream computation of variant_score.

Implement queries such as:
  - rare + high-impact variants 
  - variants grouped by gene 
  - variants across samples 
  - gene-level aggregation 
Expose:
  - SQL queries 
  - or Python interface (SQLAlchemy) 

Support queries that enable gene-level aggregation required by RDGP:

- variant_count per (sample_id, gene_id)
- rare_variant_count
- high_impact_variant_count
- pathogenic_variant_count
- likely_pathogenic_variant_count
- vus_variant_count
- likely_benign_variant_count
- benign_variant_count
- max_variant_severity

Gene-level aggregation must produce one unique evidence record per (sample_id, gene_id) pair for downstream RDGP consumption.

Goal:
Database supports deterministic construction of the gene-level evidence records required by the VDB ↔ RDGP interface contract.


---

### M6 — Provenance + Auditability
Track:
  - which pipeline generated data 
  - when data was ingested 
  - source files (VCF names, run IDs) 
  - versioning of annotations 
Add fields like:
  - source_pipeline 
  - run_id 
  - timestamp 

Provenance must allow:

- tracing each gene-level evidence record back to:
    - contributing variants
    - annotation sources
    - pipeline run

This is required for RDGP interpretability.

Goal:
Every stored evidence record can be traced back to its origin.

---

### M7 — Edge Cases + Data Integrity

VDB must mediate cross-repository identity reconciliation without requiring upstream repositories to share identical namespace conventions.

All cross-system overlays must preserve:
- source identity
- namespace provenance
- normalization traceability

Address:
  - multi-allelic variants 
  - missing annotations 
  - conflicting annotations 
  - low-quality entries (flagging, not necessarily filtering) 
  - mitochondrial variants (even if minimal) 
Define:
  - assumptions 
  - limitations 

Null Handling:
- missing values must be stored explicitly (NULL)
- zero and NULL must be distinguishable
- no downstream system should infer biological meaning from missing data

Validation should include:
- schema integrity checks
- foreign key consistency
- duplicate-ingestion prevention
- annotation-row preservation
- reproducible aggregation metrics for selected (`sample_id`, `gene_id`) pairs
- null vs zero behavior checks

Goal:
System handles real-world genomic data without silent failure.

---

### M8 — Integration Hooks (Prepare for Ecosystem)
Prepare for:
- GSC: 
    - gene-level joins 
- RSP: 
    - gene expression linkage 
- RDGP: 
    - scoring inputs 

For GSC integration, VDB should be able to attach:
  - consensus_score
  - source_list
  - source_count
to gene-linked records without altering core variant tables.

GSC overlays are attached at the gene-linked evidence layer and may be propagated to (sample_id, gene_id) records during RDGP aggregation.

For RSP integration, VDB should ensure:
  - schema remains extensible for future RSP-linked gene expression overlays without requiring redesign of core variant tables
  - variant-to-gene aggregation is possible without schema redesign
  - GSC_support and rare disease gene prioritization can be attached without altering core tables

For RDGP integration, VDB should ensure: 
  - schema supports all fields required by RDGP Core Data Model
  - variant-to-gene aggregation is possible without schema redesign
  - GSC_support and expression_support can be attached without altering core tables

Goal:
VDB acts as the stable, central evidence layer for downstream systems such as GSC, RSP, and RDGP.

---

## Modern Phase 3 / Phase 4 Milestones

The following milestones extend the original M1–M8 roadmap.

They reflect the current architecture in which VDB preserves producer TEP-derived evidence and derives governed internal evidence structures.

### M9 — TEP Package Registration

Register producer TEP-derived evidence packages into the VDB Phase 3 registration substrate.

Requirements:

- preserve package identity
- preserve artifact identity
- preserve assertion registration identity
- preserve source identity
- preserve namespace identity
- preserve producer-family identity
- preserve referential integrity
- emit certification-reviewable registration receipts

Current status:

```text
implemented and certified for the canonical Phase 3 benchmark substrate
```

Goal:
Producer evidence can enter VDB as preserved, queryable, provenance-retaining registration substrate rather than as flattened rows.

---

### M10 — Registration Unit Preservation

Declare and validate Registration Units as Phase 4.1 candidate evidence-custody units.

Requirements:

- inspect registered evidence stores read-only
- preserve Registration Unit identity
- emit deterministic inventory artifacts
- emit readiness artifacts
- verify non-mutation behavior
- verify SQLite sidecar absence
- preserve Phase 3 certification visibility

Current status:

```text
implemented and validated for the six-unit canonical benchmark corpus
```

Supporting evidence:

```text
docs/validation/registration_unit_validation.md
docs/validation/phase4_1_registration_unit_certification.md
results/validation/phase4_registration_units/
```

Goal:
VDB can safely identify which registered evidence units are ready to participate in downstream Phase 4 derivation.

---

### M11 — Corpus Generation Scope Declaration

Declare a deterministic Corpus Generation over selected Registration Units.

Requirements:

- declare Corpus Generation identity
- declare selection policy
- preserve included Registration Unit boundaries
- preserve excluded/deferred scope when relevant
- emit deterministic Corpus Generation manifests
- emit deterministic downstream Assertion Record input manifest
- validate artifact set externally
- preserve authority boundaries

Current status:

```text
implemented and validated for mark_phase4_corpus_6tep_v1
```

Supporting evidence:

```text
docs/implementation/schemas/corpus_generation_schema.md
docs/validation/corpus_generation_validation.md
docs/validation/phase4_2_corpus_generation_certification.md
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
results/validation/phase4_corpus_generation/
```

Critical Phase 4.3 handoff:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Goal:
VDB can freeze a governed evidence universe before deriving Assertion Records, topology, geometry, surfaces, or projections.

---

### M12 — Assertion Record Indexing

Index scientific claims from the selected Corpus Generation without interpreting them.

Requirements:

- consume the governed downstream Assertion Record input manifest
- preserve Corpus Generation identity
- preserve Registration Unit identity
- preserve producer claim identity
- preserve source lineage
- preserve assertion semantics
- avoid biological confidence scoring
- avoid topology derivation inside the Assertion Record layer

Current status:

```text
next active implementation frontier
```

Goal:
VDB can preserve scientific claims as corpus-indexed Assertion Records without collapsing them into downstream biological interpretation.

---

### M13 — Evidence Topology Derivation

Derive organization over Assertion Records.

Requirements:

- consume Assertion Records
- derive relationships without transferring source authority
- preserve lineage to Corpus Generation and Registration Units
- distinguish topology from confidence, interpretation, and reasoning
- avoid geometry or surface exposure decisions inside the topology layer

Current status:

```text
planned
```

Goal:
VDB can organize preserved claims into evidence topology while keeping source authority and biological interpretation separate.

---

### M14 — Convergence Geometry Characterization

Characterize organization over topology.

Requirements:

- consume Evidence Topology
- characterize convergence structure
- preserve derivation lineage
- avoid treating geometry as biological truth
- avoid consumer exposure decisions inside geometry construction

Current status:

```text
planned
```

Goal:
VDB can characterize convergence patterns without collapsing structural characterization into confidence or reasoning.

---

### M15 — Evidence Convergence Surface Governance

Govern which topology/geometry-derived structures are eligible for consumer exposure.

Requirements:

- declare surface identity
- preserve eligibility basis
- preserve disclosure basis
- preserve withholding rationale
- preserve generation and currency
- emit downstream projection input manifests

Current status:

```text
planned
```

Goal:
VDB can control evidence exposure through governed surfaces rather than exposing internal structures opportunistically.

---

### M16 — Projection View / Consumer Surface Materialization

Materialize governed consumer-facing projections.

Requirements:

- declare Projection Build identity
- declare Projection View identity
- declare source surfaces
- preserve field maps
- preserve transformations and omissions
- preserve lossiness
- preserve authority labels
- preserve reconstruction path
- support RDGP-facing and future consumer-facing query surfaces

Current status:

```text
planned
```

Goal:
VDB can expose governed evidence to downstream consumers without making consumers reconstruct internal storage, topology, or geometry directly.

---

## Transport And Projection Clarification

Producer TEPs transport upstream evidence into VDB.

VDB preserves producer evidence and may later emit governed downstream projection artifacts.

A VDB Projection View is not the same thing as a producer TEP.

A VDB projection package may become a transport artifact in the future, but it should be treated as a governed consumer projection, not as raw producer evidence.

Convergence Geometry is an internal derived characterization layer unless and until a governed projection explicitly exposes it.

This corrects the older informal idea that VDB should simply emit TEPs containing convergence geometries.

Modern VDB doctrine is stricter:

```text
Producer TEPs enter VDB.

VDB preserves custody, declares scope, preserves claims, derives organization,
characterizes convergence, governs exposure, and materializes projections.

RDGP reasons.
```


---

## Release Gate (Public v1.0)
VDB is portfolio-ready when:
  - schema is clearly defined and documented 
  - data from VAP can be ingested reproducibly 
  - annotated variants exist in structured form 
  - queries demonstrate real analytical use 
  - provenance is tracked 
  - documentation includes: 
      - assumptions 
      - limitations 
      - edge cases 
      - validation strategy 
      - implementation details 
  - namespace normalization behavior documented
  - alias handling behavior documented
  - unresolved mapping behavior validated
  - provenance-preserving normalization demonstrated

---

## Future Upgrades (Post v1.0)
  - GSC integration (gene sets + enrichment) 
  - RSP integration (expression-aware filtering) 
  - performance scaling (PostgreSQL if needed) 
  - advanced indexing 
  - API layer (optional) 
  - clinical-style reporting outputs


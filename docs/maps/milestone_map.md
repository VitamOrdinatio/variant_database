# Milestone Map: variant_database (VDB)

---

## Purpose

Provide a structured, persistent, queryable database for storing and integrating:

- variant calls (from VAP) 
- annotations (functional, clinical, population) 
- gene-level context (from GSC) 
- future expression evidence (from RSP) 

VDB serves as the authoritative source of genomic evidence that enables downstream systems (e.g., RDGP) to perform reproducible, interpretable analysis.

---

## Layer Ecosystem
1. evidence providers (VAP, GSC, future RSP)
2. authoritative evidence layer (VDB)
3. interface contract layer (vdb_rdgp_interface)
4. reasoning layer (RDGP)

---

## Terminology

- "variant-level evidence": structured observations and annotations associated with a specific variant in a specific sample
- "gene-level evidence": aggregated variant and contextual information associated with a gene for a given sample
- "authoritative evidence layer": the system of record from which downstream analytical systems retrieve genomic evidence

## Core Data Model (v1)

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


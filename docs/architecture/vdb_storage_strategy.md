# VDB Storage Strategy and Artifact Lifecycle

## 1. Purpose

VDB is the normalized relational integration layer for the computational genomics ecosystem.

Producer repositories such as VAP and RSP generate biological and computational artifacts within defined workflow boundaries. VDB provides the persistent relational space where those outputs can be normalized, linked, queried, intersected, and reinterpreted across semantic domains.

For example, VDB alone permits:

- variant ∩ gene set
- variant ∩ phenotype
- variant ∩ expression contrast
- variant ∩ physiology
- variant ∩ infection history

VDB is therefore not designed to duplicate raw producer-repository storage. It is designed to preserve relational meaning across producer outputs.

---

## 2. Quick Terminology

| Term      | Meaning                                                                        |
| --------- | ------------------------------------------------------------------------------ |
| VDB       | Variant Database                                                               |
| VAP       | Variant Annotation Pipeline                                                    |
| RSP       | RNA Sequencing Pipeline                                                        |
| GSC       | Gene Set Consensus                                                             |
| RDGP      | Rare Disease Gene Prioritization                                               |
| SeroStrat | Cohort engineering and physiological/infectious disease stratification         |
| MARK      | Primary 40-core Linux HPC execution node used for empirical pipeline telemetry |

---

## 3. VDB Storage Identity

VDB owns normalized relational derivatives and semantic integration products.

It does not own:

* raw FASTQ files,
* BAM files,
* raw alignments,
* full producer execution directories,
* or bulky intermediate artifacts.

Those artifacts remain the responsibility of producer repositories such as VAP and RSP.

VDB instead stores the durable relational products needed to ask questions across repositories, samples, variants, genes, contrasts, phenotypes, and biological overlays.

---

## 4. Producer vs Consumer Ownership

The ecosystem follows a simple ownership boundary:

```text
Producer repos own raw execution artifacts.
VDB owns normalized relational derivatives.
```

Producer repositories generate domain-specific outputs:

| Producer  | Primary responsibility                                                          |
| --------- | ------------------------------------------------------------------------------- |
| VAP       | variant discovery, annotation, prioritization, and genomic execution provenance |
| RSP       | RNA-seq execution, expression contrasts, and transcriptomic convergence outputs |
| GSC       | curated gene-set overlays and consensus gene knowledge                          |
| RDGP      | gene prioritization outputs and evidence scoring                                |
| SeroStrat | clinical, physiological, and infectious disease stratification outputs          |

VDB consumes these outputs and transforms them into persistent relational entities.

---

### TEP and Brokerage Boundary

When producer outputs arrive as Transitional Evidence Products (TEPs), VDB should treat the TEP payload as producer-owned source truth.

VDB may ingest, validate, route, persist, and derive relational entities from TEPs, but it should not mutate producer-owned TEP payload semantics.

Namespace normalization performed by VDB is additive brokerage, not payload mutation.

Thus:

```text
Producer repositories own source truth.
TEPs transport source truth.
VDB brokers and persists source truth.
Discovery exposes source truth through governed query surfaces.
```

---

## 5. Semantic Domain Integration

VDB is designed to integrate multiple semantic domains, including:

* variants,
* genes,
* samples,
* sequencing runs,
* expression contrasts,
* gene sets,
* disease-associated loci,
* prioritization outputs,
* physiological overlays,
* infectious disease context,
* and provenance metadata.

Each producer repository draws a boundary around what it can generate.

VDB draws the larger relational circle around those boundaries.

This allows questions that no single producer repository can answer alone.

---

## 6. What VDB Should Not Store

VDB should avoid becoming a second raw-data archive.

In general, VDB should not store:

| Artifact                     | Reason                                                      |
| ---------------------------- | ----------------------------------------------------------- |
| FASTQ.gz files               | retained by producer-side acquisition/storage systems       |
| BAM files                    | too large; reproducible from retained substrate when needed |
| raw alignments               | producer-owned execution artifacts                          |
| full VAP/RSP run directories | bulky and workflow-specific                                 |
| temporary intermediate files | not durable relational products                             |

Avoiding duplication keeps VDB focused, queryable, and storage-efficient.

---

## 7. What VDB Should Store

VDB should store normalized relational derivatives and provenance pointers.

Examples include:

| VDB-owned object                     | Purpose                                       |
| ------------------------------------ | --------------------------------------------- |
| normalized variant records           | stable variant-level interrogation            |
| sample–variant relationships         | cohort and sample-level querying              |
| gene–variant relationships           | gene-centered analysis                        |
| gene-set membership overlays         | biological context from GSC or other sources  |
| expression contrast summaries        | RSP-derived transcriptomic integration        |
| prioritization outputs               | RDGP and VAP-derived evidence layers          |
| physiological or infectious overlays | SeroStrat-linked clinical context             |
| source file paths and checksums      | provenance linkage back to producer artifacts |
| SQL indexes/materialized views       | performant query and integration layers       |
| database backups/dumps               | operational database resilience               |
| TEP envelopes, payload references, and source artifact manifests | governed transport, provenance, and topology preservation |

VDB may reference producer-owned files by path and checksum, but should not mutate producer-owned artifacts.

---

## 8. Variant Lifecycle: From Static Output to Queryable Entity

Without VDB, variants may remain stranded inside run-specific files, reports, or case-study artifacts.

With VDB, variants become persistent queryable entities.

This transition matters because biological significance often emerges through relationships:

* variant ↔ gene,
* variant ↔ sample,
* variant ↔ cohort,
* variant ↔ phenotype,
* variant ↔ gene set,
* variant ↔ expression contrast,
* variant ↔ physiological context,
* variant ↔ future annotation framework.

VDB therefore transforms static producer outputs into an active relational interrogation layer.

---

## 9. Storage Implications

VDB’s storage footprint is expected to come from:

* normalized SQL tables,
* relational indexes,
* materialized views,
* provenance metadata,
* ingestion logs,
* database backups,
* and semantic overlays.

This storage footprint is smaller than duplicating raw sequencing artifacts, but it is still real infrastructure.

PostgreSQL storage amplification is expected as tables, indexes, views, and backups mature.

VDB storage planning should therefore account for relational overhead while explicitly avoiding raw FASTQ/BAM duplication.

---

## 10. Future-Facing Reinterpretation

VDB is designed for future reinterpretability.

As biological annotation frameworks mature, previously unresolved variant patterns may become newly interpretable.

This is especially important for:

* noncoding variants,
* regulatory regions,
* gene-set proximity patterns,
* enhancer/promoter hypotheses,
* chromatin organization hypotheses,
* and genotype–environment interaction models.

VDB preserves the relational substrate needed to revisit these patterns without requiring producer repositories to indefinitely retain every bulky execution artifact.

This is particularly important because biologically meaningful patterns may only emerge statistically across cohorts, semantic overlays, or future annotation frameworks that do not yet exist at the time of original variant acquisition.

---

## 11. Summary

VDB is the ecosystem’s semantic interrogation layer.

It does not replace VAP, RSP, GSC, RDGP, or SeroStrat.

Instead, it gives their outputs a durable relational home.

VDB’s storage strategy is therefore guided by one central principle:

```text
Do not duplicate raw producer artifacts.
Do not mutate producer-owned transport payloads.
Preserve normalized relational meaning through additive brokerage.
```

> VDB is where variants stop being files, and become entities.

---
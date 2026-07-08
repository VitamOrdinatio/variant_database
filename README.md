# Variant Database (VDB)

**VDB is a preservation-first genomic evidence database for registering, preserving, and organizing heterogeneous evidence products from bioinformatics pipelines.**

The project is designed around a simple principle: genomic evidence should remain reproducible, provenance-aware, and queryable without collapsing away the producer context that made the evidence meaningful. VDB registers transportable evidence products from upstream systems, preserves producer assertions and source identities, stores metadata/coordinate/feature declarations, and derives topology-ready evidence substrates for downstream biological reasoning.

<p align="center">
  <img src="docs/design/figures/convergence_geometry_model.png" alt="VDB convergence geometry model" width="850">
</p>

## Why VDB Exists

Modern genomics workflows produce evidence in many shapes: sample-level variant observations, annotation lifecycles, phenotype-gene priors, transcriptomic signals, validation reports, run manifests, and provenance records. A conventional flat table can store pieces of that output, but it often loses the relationships that make the evidence scientifically auditable.

VDB is being built as an evidence infrastructure layer that keeps those relationships intact. It emphasizes:

- **Producer-aware ingestion** of structured evidence packages rather than ad hoc table loading.
- **Provenance preservation** across source artifacts, run context, validation receipts, and lineage metadata.
- **Namespace discipline** for genes, variants, samples, coordinates, and producer-specific identifiers.
- **Coordinate and feature preservation** so noncoding, intergenic, unannotated, and currently ambiguous variants remain available for future reinterpretation.
- **Topology-ready evidence organization** without prematurely claiming biological causality, clinical interpretation, or diagnostic actionability.

## Evidence Products in Scope

VDB currently focuses on two upstream evidence producers from the surrounding repository ecosystem:

| Producer | Evidence shape | VDB role |
| --- | --- | --- |
| **VAP** | Sample/run-specific variant evidence lifecycles, including observation, normalization, coding and noncoding interpretation, prioritization, validation, and run context | Preserve variant-derived evidence, source identities, reference-context coordinates, feature declarations, and lifecycle provenance |
| **GSC** | Phenotype-scoped semantic priors for phenotype-gene relationships | Preserve semantic-prior evidence, gene namespace, phenotype scope, source attribution, scoring context, and provenance |

These evidence products are intentionally different. VDB does not force them into a single flat model. Instead, it registers each producer's evidence while preserving the authority boundaries that make the evidence interpretable.

<p align="center">
  <img src="docs/architecture/figures/vdb_semantic_persistence_and_interoperability_nexus.png" alt="VDB semantic persistence and interoperability nexus" width="850">
</p>

## Current Implementation Status

VDB is in active pre-v1.0 development. The repository has moved beyond initial ingestion into late Phase 4 work focused on converting producer TEPs into durable, topology-ready evidence substrates.

Implemented and validated layers include:

- **TEP-aware registration** for producer evidence packages.
- **SQLite-backed registration units** for preserving package artifacts, assertions, identities, metadata, coordinates, and feature declarations.
- **Registration Unit validation** with read-only source handling and non-mutation checks.
- **Corpus Generation** from governed input policies and selection manifests.
- **Assertion Record generation** that preserves producer scientific claims and references large identity/declaration sets through deterministic handles.
- **Conservative Evidence Topology** that derives organization over preserved evidence without overclaiming downstream interpretation.
- **A layered test strategy** spanning unit tests, golden fixtures, and MARK-executed smoke tests.

The current test suite contains **253 passing pytest tests** across the implemented VDB codebase and fixture/documentation context.

## Benchmark Corpus

VDB's near-term v1.0 benchmark centers on a six-TEP multi-producer corpus:

- **4 VAP TEPs**: HG002 WGS plus representative epilepsy WES packages at q1, median, and q3 depth tiers.
- **2 GSC TEPs**: epilepsy and mitochondrial disease semantic-prior packages.

This benchmark is intentionally modest but heterogeneous. It demonstrates that VDB can preserve both production-scale variant evidence and compact phenotype-gene semantic priors under a shared registration and assertion-record architecture.

Longer-term corpus expansion may include all 13 currently completed VAP TEPs, and eventually a much larger 144-sample VAP corpus. That broader expansion is future roadmap work, not a requirement for the first public VDB release.

## Reproducibility Philosophy

VDB is built around the idea that scientific software claims need receipts. Assertions about ingestion, corpus scope, validation state, topology readiness, and producer evidence boundaries should be backed by concrete artifacts.

Examples include:

- input policies and selection manifests for benchmark corpora,
- validation reports and readiness tables,
- deterministic artifact inventories,
- source identity and declaration-set handles,
- golden fixtures,
- pytest coverage across implementation layers,
- MARK smoke-test outputs on real producer evidence.

The goal is not only to make evidence queryable, but to make the path from producer output to downstream substrate inspectable and reproducible.

<p align="center">
  <img src="docs/architecture/figures/vdb_evidence_lifecycle_architecture.png" alt="VDB evidence lifecycle architecture" width="850">
</p>

## Repository Layout

The most important repository areas are:

| Path | Purpose |
| --- | --- |
| `src/variant_database/` | Core Python implementation for registration, persistence, corpus generation, assertion records, and topology derivation |
| `scripts/` | Operational scripts, validation utilities, MARK smoke-test drivers, and development helpers |
| `tests/` | Unit tests, integration tests, and golden-fixture tests |
| `tests/fixtures/` | Synthetic and golden evidence fixtures used for reproducible validation |
| `docs/architecture/` | System architecture and authority models |
| `docs/contracts/` | System contracts and boundary definitions |
| `docs/design/` | Design rationale and conceptual models |
| `docs/implementation/` | Implementation specifications and schema-facing documentation |
| `docs/validation/` | Validation receipts and certification summaries |
| `docs/manifests/` | Governed corpus policies and selection manifests |
| `results/` | Generated validation and Phase 4 development outputs |

## Documentation Starting Points

For a quick orientation, start with:

- [`docs/NAMESPACE.md`](docs/NAMESPACE.md) — documentation namespace overview.
- [`docs/maps/milestone_map.md`](docs/maps/milestone_map.md) — development phases and repository roadmap.
- [`docs/contracts/system_contract.md`](docs/contracts/system_contract.md) — system responsibilities and boundaries.
- [`docs/architecture/namespace_authority_model.md`](docs/architecture/namespace_authority_model.md) — namespace and authority model.
- [`docs/implementation/specifications/vap_coordinate_feature_registration_spec.md`](docs/implementation/specifications/vap_coordinate_feature_registration_spec.md) — VAP metadata, coordinate, and feature declaration registration.
- [`docs/validation/`](docs/validation/) — validation summaries and receipts.

The root README is intentionally lightweight. The detailed architecture lives in the documentation tree.

## Roadmap

Near-term work is focused on completing the transition from preserved evidence topology toward downstream evidence surfaces:

- resume namespace mediation after full modern six-TEP receipts are available,
- complete convergence geometry over topology-derived relationships,
- define projection views for downstream consumers,
- expose RDGP-facing query surfaces,
- continue hardening noncoding-aware evidence preservation,
- expand benchmark coverage after v1.0 stabilization.

## Non-Goals

VDB is not a clinical decision-support system, diagnostic classifier, or pathogenicity caller. It does not claim that a variant causes disease, that a gene is clinically actionable, or that a downstream prioritization is medically valid.

Its role is narrower and more foundational: preserve genomic evidence, identity, provenance, reference context, and topology-ready structure so that downstream reasoning systems can operate on auditable substrates.

## Project Status

VDB is under active development as part of a broader computational biology repository ecosystem. The current implementation is best understood as a pre-v1.0 genomic evidence infrastructure project with validated registration, assertion-record, and conservative topology layers.

# Registration Unit and Corpus Generation Model

## Purpose

This document defines how VDB should treat Phase 3 registration outputs as checkpointed inputs for Phase 4 topology, geometry, surface, and projection development.

The key distinction is:

```text
A registration unit is an architectural object.

A SQLite database is the current implementation representation of that object.
```

This distinction allows VDB to use the certified Phase 3 MARK registration databases immediately while avoiding permanent coupling of VDB architecture to one physical storage layout.

---

# Core Claim

Phase 3 produces certified registration units.

Phase 4 consumes certified registration units.

The registration unit is the durable boundary between raw producer TEP ingestion and derived VDB evidence topology.

```text
Producer TEP
        ↓
Phase 3 registration
        ↓
Certified registration unit
        ↓
Phase 4 corpus generation
        ↓
Evidence topology
        ↓
Convergence geometry
        ↓
Evidence convergence surfaces
        ↓
Projection views / exports
```

Phase 4 should not re-read raw producer artifacts when certified registration units already exist.

---

# Registration Unit

A registration unit is the canonical registered representation of one accepted producer evidence package.

A registration unit must preserve:

* TEP package identity
* artifact identity
* assertion registrations
* source identities
* producer family
* evidence domains
* assertion types
* surface roles
* authority context
* uncertainty context
* source namespaces
* extraction methods
* package/artifact/source referential integrity
* certification or validation status

In the current implementation, one registration unit is represented as:

```text
results/registration/mark_phase3_canonical/<label>/vdb.sqlite
```

The Phase 3 certified corpus currently includes:

```text
results/registration/mark_phase3_canonical/
├── gsc_epilepsy/vdb.sqlite
├── gsc_mitochondrial_disease/vdb.sqlite
├── vap_hg002/vdb.sqlite
├── vap_median_ERR10619300/vdb.sqlite
├── vap_q1_ERR10619212/vdb.sqlite
└── vap_q3_ERR10619225/vdb.sqlite
```

These files are registration capsules: independently auditable, independently rerunnable, and independently certifiable.

---

# Current MARK Scale

The current certified MARK registration corpus is approximately 50 GB:

```text
gsc_epilepsy/vdb.sqlite                  31M
gsc_mitochondrial_disease/vdb.sqlite     30M
vap_hg002/vdb.sqlite                     33G
vap_median_ERR10619300/vdb.sqlite       5.2G
vap_q1_ERR10619212/vdb.sqlite           6.4G
vap_q3_ERR10619225/vdb.sqlite           5.3G
```

This scale is expected.

The VAP databases are large because they preserve row-level source identities at high cardinality. For example, HG002 contains more than 97 million source identities.

This is not random bloat.

It is the storage cost of preserving source identity, provenance, and namespace structure at scale.

---

# One TEP to One Registration Unit

For Phase 3 and early Phase 4, the recommended operational rule is:

```text
1 accepted producer TEP → 1 certified registration unit
```

This provides:

* isolated failure domains
* easy audit
* easy re-run
* path-stable checkpointing
* producer-specific debugging
* certification evidence per producer package
* protection against cross-TEP contamination
* stable input fixtures for Phase 4 smoketests

However, this is an implementation strategy, not a permanent architectural law.

The architectural invariant is:

```text
Each accepted TEP must produce or resolve to a traceable registration unit.
```

The invariant is not:

```text
Each accepted TEP must forever be represented by exactly one SQLite file.
```

---

# Corpus Generation

A corpus generation is a declared collection of certified registration units used as the input basis for derived VDB layers.

A corpus generation should declare:

* corpus generation identifier
* included registration units
* registration unit paths
* package IDs
* producer families
* artifact counts
* assertion counts
* source identity counts
* certification status
* build timestamp
* derivation rules
* excluded registration units, if any
* reason for inclusion or exclusion

The first Phase 4 heavy smoketest corpus should use the existing six certified Phase 3 registration units.

Possible name:

```text
mark_phase4_corpus_6tep_v1
```

or:

```text
phase4_smoketest_corpus_001
```

The corpus generation should not blindly copy all source identities into a new database unless materialization is explicitly required.

Instead, it should first construct indexes and derived artifacts over certified registration units.

---

# Phase 4 Input Rule

Phase 4 topology and geometry builders should consume certified registration units through declared schema and manifest interfaces.

They should not bypass Phase 3 by parsing raw producer artifacts directly.

Incorrect Phase 4 pattern:

```text
Open VAP TSV files.
Open GSC TSV files.
Join producer-specific rows directly.
Derive topology from raw artifacts.
```

Correct Phase 4 pattern:

```text
Open certified registration units.
Read assertion registrations.
Read source identities.
Build corpus-level indexes.
Derive topology.
Characterize geometry.
Expose surfaces.
Render projections.
```

This protects the architectural boundary between registration and topology.

---

# Storage Model Options

VDB should remain storage-layout agnostic.

Several physical layouts may be valid if they preserve the registration unit invariant and corpus generation traceability.

## Option 1: One Database Per TEP

Each accepted TEP produces one SQLite database.

Example:

```text
vap_hg002/vdb.sqlite
gsc_epilepsy/vdb.sqlite
```

Advantages:

* simple audit
* simple rerun
* easy checkpointing
* strong isolation
* good failure boundaries
* ideal for Phase 3 certification and early Phase 4 smoketests

Risks:

* many files at large scale
* cross-TEP queries require orchestration
* repeated scanning may become expensive
* integrated topology requires a corpus-level index

Recommended use:

```text
Current MARK Phase 3 and early Phase 4.
```

## Option 2: One Database Per Producer Run

Multiple TEPs emitted from one producer run are grouped into a single registration database.

Advantages:

* fewer files
* preserves run-level context
* useful when one producer emits several related TEPs
* may reduce duplicated package/run metadata

Risks:

* larger failure domains
* less isolated per-TEP certification
* requires clear internal registration unit boundaries

Recommended use:

```text
Future producer workflows that emit multiple tightly coupled TEPs from one run.
```

## Option 3: One Database Per Corpus Generation

All registration units selected for a corpus generation are materialized into one integrated database.

Advantages:

* fast corpus-level querying
* easier global indexing
* easier topology construction
* useful for stable release snapshots

Risks:

* duplicates large registration content
* expensive to rebuild
* may blur registration-unit boundaries if poorly designed
* can encourage treating corpus materialization as source truth

Recommended use:

```text
Later Phase 4 or Phase 5 release builds where performance requires materialized integration.
```

Required safeguard:

```text
The corpus database must remain reconstructable from source registration units.
```

## Option 4: One Central Relational Database

All accepted registration units are loaded into a central relational database.

Advantages:

* strong query performance
* centralized indexing
* easier multi-producer joins
* easier operational API development

Risks:

* operational complexity
* migration burden
* possible authority drift from source registration units to central tables
* harder lightweight portability

Recommended use:

```text
Mature VDB service deployment, not initial Phase 4 smoketest.
```

Required safeguard:

```text
Central tables must preserve registration_unit_id and source package identity for every derived record.
```

## Option 5: Lakehouse-Style Layout

Registration and derived artifacts are stored as partitioned files, such as Parquet, Arrow, DuckDB-compatible files, or similar columnar formats.

Advantages:

* strong scalability
* efficient analytical scans
* partitioning by producer, generation, namespace, or assertion type
* good fit for large multi-SRA corpora

Risks:

* added tooling complexity
* requires strict metadata discipline
* easier to lose referential clarity if partitions are not governed
* may be premature before schema stabilizes

Recommended use:

```text
Future large-scale VDB deployments, especially 144-SRA or multi-cohort builds.
```

Required safeguard:

```text
Partitions must preserve registration unit lineage and corpus generation identity.
```

## Option 6: Object Store Plus Indexed Metadata

Large artifacts are stored as immutable objects, while lightweight metadata indexes record package, artifact, assertion, source identity, topology, and projection references.

Advantages:

* scalable
* cloud/HPC compatible
* avoids unnecessary duplication
* supports immutable artifact storage
* can pair well with metadata catalogs

Risks:

* higher implementation complexity
* requires careful index synchronization
* object identity and metadata identity must remain aligned
* may be excessive for current local MARK development

Recommended use:

```text
Future distributed or institutional VDB deployment.
```

Required safeguard:

```text
Object identity, checksum, registration unit identity, and corpus generation identity must remain inseparable.
```

---

# Recommended Current Strategy

For current MARK development, the best strategy is:

```text
1 TEP → 1 SQLite registration unit
many certified registration units → 1 declared corpus generation
corpus generation → derived topology/geometry/surfaces/projections
```

The current Phase 3 certified registration units should be reused as checkpointed Phase 4 inputs.

This avoids repeatedly paying the heavy extraction cost and ensures Phase 4 development proceeds from validated registration substrate rather than raw producer artifacts.

---

# Avoiding Unnecessary Duplication

Phase 4 should not immediately build a giant merged SQLite database that copies all source identities from every registration unit.

The current six-unit corpus is already approximately 50 GB.

A naive integrated copy could double storage before topology and geometry artifacts are produced.

Instead, Phase 4 should initially build lightweight corpus-level indexes such as:

```text
corpus_generation_manifest.tsv
registration_unit_index.tsv
package_index.tsv
assertion_index.tsv
namespace_summary.tsv
participant_key_index.tsv
topology_relationships.sqlite
geometry_features.sqlite
surface_inventory.tsv
projection_inventory.tsv
```

Only later, if performance requires it, should VDB materialize a full integrated corpus database.

---

# Corpus-Level Derived Artifacts

A Phase 4 corpus generation may produce derived artifacts such as:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/
├── corpus_generation_manifest.tsv
├── registration_unit_index.tsv
├── package_index.tsv
├── assertion_index.tsv
├── namespace_summary.tsv
├── topology/
│   ├── topology_relationships.sqlite
│   └── topology_summary.tsv
├── geometry/
│   ├── geometry_features.sqlite
│   └── geometry_summary.tsv
├── surfaces/
│   ├── surface_inventory.tsv
│   └── surface_summary.tsv
└── projections/
    ├── projection_inventory.tsv
    └── export_summary.tsv
```

These artifacts derive from certified registration units.

They do not replace them.

---

# Authority Boundary

Registration units preserve source assertions.

Corpus generations declare which registration units participate in a build.

Topology derives organization.

Geometry characterizes topology.

Surfaces expose structurally eligible regions.

Projections render views.

No corpus generation, derived topology, geometry artifact, surface, projection, or materialized database becomes source truth.

The governing authority chain is:

```text
Producer TEP
        ↓
registration unit
        ↓
corpus generation
        ↓
derived layers
```

The source authority remains with preserved producer assertions inside registration units.

---

# Phase 4 Smoketest Implication

The existing certified Phase 3 MARK corpus should be treated as the canonical heavy Phase 4 smoketest fixture.

Input:

```text
results/registration/mark_phase3_canonical/
```

Expected Phase 4 workflow:

```text
certified registration units
        ↓
corpus generation manifest
        ↓
assertion/source identity indexing
        ↓
topology derivation
        ↓
geometry derivation
        ↓
surface inventory
        ↓
projection/export test
```

This allows Phase 4 to test the new derived architecture without repeatedly rebuilding Phase 3 registration.

---

# Documentation and Contract Implications

The Phase 4 system contract should include the following rule:

```text
Phase 4 consumes certified registration units, not raw producer TEPs.
```

The implementation plan should include:

```text
Build a corpus generation manifest over the certified Phase 3 MARK registration units.
```

Satellite contracts should define:

* registration unit input requirements
* corpus generation manifest requirements
* topology derivation requirements
* geometry derivation requirements
* surface exposure requirements
* projection requirements

Validation should certify:

* registration unit discoverability
* corpus generation integrity
* no missing registration units
* no uncertified inputs unless explicitly marked
* no destructive modification of registration units
* no unnecessary duplication of source identities
* derived topology traceability back to registration units

---

# Summary

The certified Phase 3 registration SQLite databases should be treated as checkpointed registration units.

They are durable, auditable, and reusable Phase 4 inputs.

The current operational rule is:

```text
1 TEP → 1 certified SQLite registration unit
```

The architectural rule is:

```text
1 accepted TEP → 1 traceable registration unit
```

The Phase 4 rule is:

```text
many certified registration units → 1 corpus generation → derived topology, geometry, surfaces, and projections
```

This allows VDB to proceed efficiently on MARK while preserving implementation flexibility for future storage models, including per-producer-run databases, corpus-generation databases, central relational stores, lakehouse layouts, and object-store-backed metadata indexes.

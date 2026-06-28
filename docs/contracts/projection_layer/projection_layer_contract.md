# Projection Layer Contract

## Purpose

This document defines the VDB contract for the Projection Layer.

A Projection View is a purpose-bound representation over preserved assertions or governed VDB-derived layers.

Projection Views represent governed VDB evidence for a defined purpose, consumer, validation task, export, report, query response, dashboard, package, or downstream reasoning substrate without changing the authority of the source records they represent.

This contract ensures that Projection Views remain:

```text
purpose-bound
source-declared
authority-labeled
lineage-preserving
lossiness-explicit
materialization-neutral
consumer-aware when applicable
generation-aware
currency-aware
reconstructable
non-interpretive
non-authority-transferring
```

Projection changes representation.

Projection does not change authority.

---

# Scope

This contract applies to all VDB Projection Views, including:

```text
registration unit inventory projections
corpus generation manifest projections
Assertion Record table projections
Evidence Topology inspection projections
Convergence Geometry feature projections
Evidence Convergence Surface projections
validation report projections
certification report projections
query response projections
developer inspection projections
dashboard projections
TEP-VDB export projections
RDGP-facing consumer projections
future consumer-specific projections
future report projections
future API projections
future release projections
```

This contract governs the logical requirements of Projection Views.

It does not prescribe a single storage representation, export format, report format, query interface, visualization style, or consumer package structure.

Projection Views may be represented by:

```text
TSV
CSV
JSON
JSONL
SQLite export
Parquet
Markdown report
HTML report
PDF report
dashboard view
query response
API response
TEP-VDB package
RDGP-facing package
validation report
certification report
manifest file
future consumer format
future storage backend
```

The representation is not the architecture.

The purpose-bound, lineage-preserving representation of governed VDB records is the architecture.

---

# Parent System Contract Obligations

This contract is subordinate to:

```text
docs/contracts/system_contract.md
```

The System Contract establishes the governing VDB authority chain:

```text
Producer TEP
        ↓
registration unit
        ↓
corpus generation
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection Views
        ↓
Downstream Reasoning
```

This contract defines the obligations of the Projection Layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Projection Layer contract governs purpose-bound representation over preserved or derived VDB records.

A Projection View answers:

```text
How is governed VDB evidence represented for this purpose?
```

A Projection View does not answer:

```text
What is biologically true?

What is causal?

What is clinically actionable?

Which evidence should be exposed?

Which evidence exists outside the declared source layer?

Which downstream reasoning conclusion is correct?

Which candidate should be prioritized?
```

Those responsibilities belong to upstream source layers, governed surface policies, downstream reasoning systems, or returned producer assertions.

---

# Definition

A Projection View is a purpose-bound representation over one or more governed VDB source layers.

A Projection View may select, filter, summarize, flatten, denormalize, rename, serialize, package, render, or materialize source records for a declared purpose.

A Projection View must preserve enough information to support:

```text
projection reconstruction
source layer reconstruction
source record reconstruction
source authority reconstruction
field selection reconstruction
field omission reconstruction
transformation reconstruction
lossiness reconstruction
materialization reconstruction
generation reconstruction
currency reconstruction
consumer-use reconstruction when applicable
downstream return-path reconstruction when applicable
```

A Projection View is representation.

It is not source evidence.

It is not a Registration Unit.

It is not a Corpus Generation.

It is not an Assertion Record.

It is not Evidence Topology.

It is not Convergence Geometry.

It is not an Evidence Convergence Surface.

It is not downstream reasoning.

---

# Core Invariant

The architectural rule is:

```text
Projection changes representation.

Projection does not change authority.
```

The governing transition is:

```text
Evidence Convergence Surfaces
        ↓
Projection Views
        ↓
Downstream Reasoning
```

However, Projection Views may also be emitted from other governed VDB source layers when the projection purpose does not require the full Phase 4 derived chain.

This means:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed evidence for a purpose.

Downstream systems reason over projections.
```

Projection Views may make VDB evidence easier to inspect, validate, transmit, query, export, or consume.

They must not make VDB evidence more authoritative than its source layer.

---

# Projection Authority

Projection Views have representation authority.

A Projection View is authoritative for:

```text
which source layer it represented
which source records it included
which source records it omitted when omission is relevant
which fields it rendered
which fields it omitted when omission is relevant
which transformations it applied
which projection policy it used
which materialization format it emitted
which lossiness status applies
which consumer or purpose it served
which generation and currency context applied
which reconstruction path is available
```

A Projection View is not authoritative for:

```text
producer source evidence
producer scientific claims
Assertion Record correctness
topology relationship correctness
geometry feature correctness
surface eligibility correctness
biological confidence
clinical interpretation
causality
pathogenicity
candidate prioritization
RDGP reasoning
```

Projection authority is narrow.

It governs representation.

It does not create source authority.

---

# Representation And Materialization Neutrality

Projection Views must remain representation-neutral and materialization-neutral.

Valid projection materializations may include:

```text
tables
files
packages
reports
dashboards
query responses
API responses
database exports
validation outputs
certification outputs
consumer-specific payloads
future projection formats
```

A materialized projection is not source truth.

A dashboard is not source truth.

A query response is not source truth.

A report is not source truth.

A consumer package is not source truth.

The materialized format must not define the authority of the projection.

The declared source layer and source records define the projection's authority boundary.

---

# Required Source Declaration

Every Projection View must declare its source layer.

Supported source layers may include:

```text
registration_unit
corpus_generation
assertion_record
evidence_topology
convergence_geometry
evidence_convergence_surface
validation_report
certification_report
query_surface
external_evidence_capsule
returned_reasoning_assertion
other_governed_vdb_source
```

A Projection View must declare source records sufficient for reconstruction.

Source record references may include:

```text
registration_unit_ids
corpus_generation_ids
assertion_ids
topology_build_ids
topology_relationship_ids
geometry_build_ids
convergence_region_ids
geometry_feature_ids
structural_motif_ids
surface_ids
surface_build_ids
surface_membership_ids
validation_report_ids
certification_report_ids
query_surface_ids
external_capsule_ids
returned_assertion_ids
```

A Projection View generated without a declared source layer is not VDB-compliant.

A Projection View generated without reconstructable source records is not VDB-compliant.

---

# Full-Chain And Partial-Chain Projection Obligations

The canonical full Phase 4 derivation chain is:

```text
Projection View
        ↓
Evidence Convergence Surface
        ↓
Convergence Geometry
        ↓
Evidence Topology
        ↓
Assertion Record
        ↓
registration unit
        ↓
producer artifact
        ↓
producer TEP
```

Not every Projection View is required to include every intermediate derived layer.

Valid partial-chain projections may include:

```text
Registration Unit inventory projection
    source layer = registration_unit

Corpus Generation manifest projection
    source layer = corpus_generation

Assertion Record table projection
    source layer = assertion_record

Evidence Topology inspection projection
    source layer = evidence_topology

Convergence Geometry feature report
    source layer = convergence_geometry

Evidence Convergence Surface export
    source layer = evidence_convergence_surface

Validation report projection
    source layer = validation_report

RDGP-facing consumer projection
    source layer = evidence_convergence_surface or another declared governed source
```

When a Projection View does not include the full Phase 4 chain, it must explicitly declare:

```text
projection source layer
projection source records
omitted intermediate layers when relevant
reason omitted layers are not applicable
traceability path to preserved assertions, registration units, or another governed VDB source
```

A partial-chain projection is valid only when its source layer and reconstruction path are explicit.

---

# Required Projection Identity

Every Projection View must have a stable identity.

A Projection View identity must preserve:

```text
projection_id
projection_label when available
projection_type
projection_purpose
projection_source_layer
projection_policy_id
projection_policy_version when available
projection_builder_name
projection_builder_version when available
projection_timestamp
materialization_format
lossiness_status
validation_status
certification_status when available
```

Projection identity must remain stable across validation, certification, reconstruction, consumer delivery, and returned reasoning linkage when applicable.

Human-readable labels may support inspection.

Labels must not replace stable Projection View identity.

---

# Projection Policy Obligations

Every Projection View must declare a projection policy.

Projection policy must define or reference:

```text
source layer
source record selection criteria
field inclusion rules
field omission rules
field renaming rules
field transformation rules
filtering rules
aggregation rules when applicable
sorting or ordering rules when applicable
materialization format rules
lossiness rules
consumer purpose when applicable
consumer-specific shaping rules when applicable
reconstruction requirements
validation requirements
```

Projection policy must be reconstructable.

Projection policy must not silently change source authority.

Projection policy must not silently hide evidence strata, uncertainty, lineage, generation context, or lossiness.

A Projection View without a declared projection policy is not VDB-compliant.

---

# Source Record Obligations

A Projection View must preserve source record references sufficient for reconstruction.

Source record obligations include:

```text
source layer declaration
source record identifiers
source record version or generation context when available
source authority class
source validation status when available
source certification status when available
source lineage references when applicable
source reconstruction handles
```

Projection Views must not mutate source records.

Projection Views must not replace source records.

Projection Views must not overwrite source records.

Projection Views must not silently materialize a new source evidence layer.

---

# Field Selection And Transformation Obligations

Projection Views may select, rename, transform, flatten, denormalize, summarize, aggregate, or package fields.

Allowed projection transformations include:

```text
field selection
field omission
field renaming
field ordering
field grouping
field flattening
record denormalization
record filtering
record aggregation
summary generation
format serialization
consumer-specific packaging
report rendering
dashboard rendering
query response shaping
```

Every transformation must preserve or declare:

```text
source field reference when applicable
target field name when applicable
transformation rule
lossiness status
source authority class
reconstruction path
```

Field renaming must not obscure source authority.

Field flattening must not collapse evidence strata.

Aggregation must not hide independent evidence strata unless explicitly declared as lossy.

Summary generation must not replace source records.

Projection transformations must not create biological meaning.

---

# Lossiness And Omission Obligations

Projection Views may be lossy.

Lossiness is allowed.

Hidden lossiness is not allowed.

Projection lossiness status may include:

```text
lossless
field_lossy
record_lossy
summary_only
consumer_filtered
policy_filtered
format_limited
redacted
partial
unknown
not_applicable
```

A Projection View must declare lossiness status.

When relevant, a Projection View must preserve:

```text
omitted source layers
omitted source records
omitted fields
omission reason
lossiness reason
filtering policy
redaction policy
summary policy
reconstruction path to omitted material when available
```

Omitted evidence must not be interpreted as absent evidence.

Filtered evidence must not be interpreted as negative evidence.

Summary-only projections must not be treated as complete evidence representations.

If lossiness is unknown, that status must be explicit.

---

# Authority Labeling Obligations

Projection Views must preserve authority labeling.

A Projection View should preserve or expose:

```text
projection source layer
source authority class
source record identifiers
producer identity when applicable
Assertion Record identity when applicable
derived-layer identity when applicable
surface eligibility status when applicable
surface disclosure status when applicable
uncertainty status when applicable
null state when applicable
generation or currency status when applicable
lossiness status
reconstruction handles
```

Projected records must remain distinguishable as:

```text
preserved evidence
custody metadata
corpus scope metadata
derived organization
derived structural characterization
governed exposure
projection representation
validation output
certification output
returned reasoning assertion
```

Consumers must not be required to infer authority from projection layout.

Authority must be explicit.

---

# Generation And Currency Obligations

Projection Views must preserve generation and currency context.

Projection records should preserve:

```text
projection_generation_id when available
source_generation_id when available
source build identifiers when applicable
source policy versions when applicable
projection_policy_version
projection_timestamp
refresh_status when available
staleness_status when applicable
supersession_status when applicable
consumer_delivery_timestamp when applicable
```

Generation and currency status may include:

```text
current
stale
superseded
partial
provisional
deprecated
unknown
not_applicable
```

Projection generation must not overwrite earlier projection generations.

A newer projection must not erase reconstructability of an older projection.

A stale projection must not silently masquerade as current.

A superseded projection must remain historically reconstructable when retained.

---

# Reconstruction Obligations

A Projection View must preserve reconstruction paths.

A Projection View must allow reconstruction of:

```text
projection identity
projection purpose
projection policy
projection source layer
projection source records
projection materialization format
projection lossiness status
field selection rules
field omission rules
transformation rules
source authority labels
source lineage
generation context
currency context
consumer-specific shaping rules when applicable
```

When a Projection View is derived from a full Phase 4 chain, reconstruction must support traceability to:

```text
Evidence Convergence Surface
Convergence Geometry
Evidence Topology
Assertion Records
Corpus Generation
Registration Units
producer artifacts
producer TEPs
```

When a Projection View is derived from a partial chain, reconstruction must support traceability to the declared source layer and its governed upstream lineage.

A Projection View without a reconstruction path is not VDB-compliant.

---

# Relationship To Evidence Convergence Surfaces

Evidence Convergence Surfaces provide governed exposure substrate for many Projection Views.

The distinction is:

```text
Evidence Convergence Surface
    governs exposure of structurally eligible convergence substrate

Projection View
    represents governed evidence or exposed substrate for a purpose
```

A Projection View may render an Evidence Convergence Surface as:

```text
table
manifest
JSON package
TSV package
SQLite export
dashboard
validation report
query response
TEP-VDB export
RDGP-facing consumer projection
future consumer-specific package
```

A Projection View must preserve source surface identity when its source layer is an Evidence Convergence Surface.

A Projection View must not replace an Evidence Convergence Surface.

A Projection View must not acquire surface authority.

A Projection View must not treat surface eligibility as biological confidence.

A Projection View must not treat surface disclosure as biological endorsement.

---

# Relationship To Convergence Geometry

Projection Views may represent Convergence Geometry directly when the projection purpose is geometry inspection, validation, reporting, export, or downstream analysis.

A Projection View over Convergence Geometry must preserve:

```text
source geometry_build_id
source convergence_region_ids when applicable
source geometry_feature_ids when applicable
source structural_motif_ids when applicable
source topology_build_id when applicable
source Assertion Record lineage when applicable
lossiness status
reconstruction path
```

A Projection View over Convergence Geometry must not replace Convergence Geometry.

A Projection View must not treat geometry features as biological confidence.

A Projection View must not treat structural richness as biological meaning.

---

# Relationship To Evidence Topology

Projection Views may represent Evidence Topology directly when the projection purpose is topology inspection, validation, reporting, export, or downstream analysis.

A Projection View over Evidence Topology must preserve:

```text
source topology_build_id
source topology_relationship_ids when applicable
topology dimensions when applicable
derivation bases when applicable
source Assertion Record lineage when applicable
lossiness status
reconstruction path
```

A Projection View over Evidence Topology must not replace Evidence Topology.

A Projection View must not treat topological connectedness as biological meaning.

A graph, network, matrix, hypergraph, table, dashboard, or future mathematical output is a projection when emitted as a representation over topology.

Such a projection must not be treated as topology itself.

---

# Relationship To Assertion Records

Projection Views may represent Assertion Records directly when the projection purpose is assertion inspection, validation, export, reporting, or downstream consumer preparation.

A Projection View over Assertion Records must preserve:

```text
source Assertion Record identities
producer identity when applicable
assertion type when applicable
relationship or relationship class when applicable
participants when applicable
evidence basis when applicable
authority context when applicable
uncertainty context when applicable
source Registration Unit identity when applicable
source Corpus Generation identity when applicable
lossiness status
reconstruction path
```

A Projection View over Assertion Records must not replace Assertion Records.

A Projection View must not treat projected rows as source assertions.

A Projection View must not create biological truth.

A flattened assertion table must preserve or declare lossiness over assertion components.

---

# Relationship To Corpus Generations And Registration Units

Projection Views may represent Corpus Generations or Registration Units directly when the projection purpose is inventory, validation, certification, reporting, inspection, or implementation support.

A Projection View over Corpus Generations must preserve:

```text
source corpus_generation_id
included Registration Unit references when applicable
selection policy reference when applicable
inclusion and exclusion rationale when applicable
validation status
certification status when available
lossiness status
reconstruction path
```

A Projection View over Registration Units must preserve:

```text
source registration_unit_id
source package identity when applicable
producer family when applicable
artifact references when applicable
assertion registration references when applicable
source identity references when applicable
validation status
certification status when available
lossiness status
reconstruction path
```

A Projection View must not replace a Corpus Generation.

A Projection View must not replace a Registration Unit.

A Projection View must not treat a materialized manifest, report, or export as source truth.

---

# Relationship To Query Surfaces

A Query Surface is a governed access mechanism.

A Projection View is a purpose-bound representation emitted from governed VDB records.

The distinction is:

```text
Query Surface
    governed access pathway or interface over VDB records

Projection View
    purpose-bound representation emitted from governed VDB records
```

A Query Surface may emit Projection Views.

A query response may be a Projection View.

A Query Surface must not obscure projection source layer, authority status, lineage, lossiness, generation context, or reconstruction path.

A Projection View emitted through a Query Surface must satisfy this contract.

A Query Surface must not replace Projection Views.

A Projection View must not replace Query Surface governance.

---

# Relationship To RDGP Consumer Projections

RDGP-facing Projection Views prepare governed VDB evidence for RDGP reasoning.

RDGP-facing projections may be generated from Evidence Convergence Surfaces or another declared governed VDB source layer when appropriate.

An RDGP-facing Projection View should preserve:

```text
projection purpose
target consumer class
source layer
source surface identity when applicable
source geometry identity when applicable
source topology identity when applicable
source Assertion Record identities when applicable
source Corpus Generation identity
source Registration Unit identities when applicable
producer strata
evidence-domain strata
modality strata when available
modality or evidence-domain identity mapping when vocabularies differ across producers
sample context when applicable
gene context when applicable
phenotype context when applicable
variant context when applicable
regulatory context when applicable
regulatory domain association when applicable
phenotype-linked regulatory region when applicable
regulatory feature context when applicable
future regulatory evidence class when applicable
uncertainty states
null semantics
negative evidence distinction when available
evidence completeness status when available
completeness scope when available
absence basis when evidence absence is asserted
omission basis when evidence is not projected
withholding basis when evidence is withheld upstream
sample recurrence when available
cohort recurrence when available
producer recurrence when available
evidence uniqueness when available
assertion reuse when available
prior observation history when available
namespace mediation status
generation context
currency context
lossiness status
reconstruction handles
return-path identifiers
```

RDGP-facing projections expose reasoning affordances.

They do not perform RDGP reasoning.

They do not determine whether evidence explains phenotype.

They do not prioritize candidate genes.

They do not create biological confidence.

They do not generate RDGP conclusions.

Returned RDGP reasoning outputs may re-enter VDB only as new preserved producer assertions.

Returned RDGP assertions must not overwrite the Projection View or the VDB evidence generation from which they were derived.

---

# Relationship To Validation And Certification Reports

Validation and certification reports may be Projection Views when they represent governed VDB records for validation, audit, or certification purposes.

A validation or certification Projection View must preserve:

```text
source layer
source records
validation or certification policy
validation or certification results
builder or validator identity
validation timestamp
certification timestamp when applicable
authority status
lossiness status when applicable
reconstruction path
```

Validation and certification projections may certify preservation, derivation, projection, consumer-readiness, or reconstruction success.

They must not certify biological correctness.

A validation report must not replace source records.

A certification report must not become source evidence.

---

# Validation Obligations

Projection View validation must confirm:

```text
projection_id exists
projection purpose is declared
projection source layer is declared
projection source records are resolvable
projection policy is declared
projection builder identity is declared
projection builder version is declared when available
projection timestamp is declared
materialization format is declared
lossiness status is declared
omitted fields or omitted layers are declared when relevant
authority status is visible
uncertainty is preserved or omission is declared when relevant
null semantics are preserved or omission is declared when relevant
generation context is visible
currency context is visible when applicable
source lineage is reconstructable
projection reconstruction path exists
projection is deterministic under fixed inputs
projection does not mutate source records
projection does not replace source records
projection does not become source evidence
projection does not perform biological reasoning
projection does not convert representation into authority
```

RDGP-facing projection validation should additionally confirm:

```text
target consumer class is declared
producer strata are preserved
evidence-domain strata are preserved
uncertainty states are preserved
null semantics are preserved when available
namespace mediation status is preserved
generation and currency metadata are preserved
return-path identifiers are preserved
lossiness is visible
consumer-specific omissions are declared when relevant
evidence completeness status is preserved when available
completeness scope is preserved when available
absence basis is declared when evidence absence is asserted
omission basis is declared when evidence is not projected
withholding basis is preserved when evidence was withheld upstream
sample recurrence is preserved or omission is declared when relevant
cohort recurrence is preserved or omission is declared when relevant
producer recurrence is preserved or omission is declared when relevant
evidence uniqueness is preserved or omission is declared when relevant
assertion reuse is preserved or omission is declared when relevant
prior observation history is preserved or omission is declared when relevant
modality or evidence-domain identity mapping is preserved when vocabularies differ across producers
regulatory context is preserved or omission is declared when relevant
regulatory domain association is preserved or omission is declared when relevant
phenotype-linked regulatory region is preserved or omission is declared when relevant
regulatory feature context is preserved or omission is declared when relevant
future regulatory evidence class is preserved or omission is declared when relevant
```

Validation must confirm representation, lineage, lossiness disclosure, and authority boundaries.

Validation must not claim biological correctness.

---

# Anti-Collapse Rules

The following are prohibited:

```text
Projection View treated as source truth
Projection View treated as source evidence
Projection View treated as biological truth
Projection View treated as clinical evidence
projection row replacing Assertion Record
projection row replacing topology relationship
projection row replacing geometry feature
projection row replacing surface membership
projection package replacing Evidence Convergence Surface
projection format defining architecture
dashboard treated as evidence
query response treated as source evidence
report treated as source evidence
consumer package treated as reasoning conclusion
lossiness hidden
omitted evidence treated as absent evidence
filtered evidence treated as negative evidence
summary-only projection treated as complete evidence
field rename obscuring authority
materialized export overwriting upstream records
projection policy collapse
projection source layer collapse
projection lineage collapse
projection generation collapse
authority label collapse
uncertainty collapse
null-state collapse
producer-family collapse
evidence-domain collapse
namespace-state collapse
opaque composite score hiding independent evidence strata
RDGP-facing projection performing RDGP reasoning
pretty output treated as biological truth
```

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

A Projection Layer implementation is complete only when:

```text
Projection View identity is stable
projection purpose is declared
projection source layer is declared
projection source records are declared
projection policy is declared
projection builder identity is declared
materialization format is declared
lossiness status is declared
omitted fields or layers are declared when relevant
authority labels are preserved
source lineage is reconstructable
generation context is preserved
currency context is preserved when applicable
projection reconstruction path exists
projection is deterministic under fixed inputs
Projection Views can serve their declared purpose
Projection Views do not mutate source records
Projection Views do not replace source records
Projection Views do not become source evidence
Projection Views do not perform biological reasoning
Projection Views remain materialization-neutral
anti-collapse validation passes
```

A Projection Layer implementation is not complete merely because a file, table, export, dashboard, API response, report, or package exists.

A Projection Layer implementation is complete only when those records satisfy this contract.

---

# Summary

A Projection View is a purpose-bound representation over preserved assertions or governed VDB-derived layers.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent governed evidence for a purpose.

Downstream systems reason over projections.
```

Projection Views make governed VDB evidence inspectable, transmissible, reportable, exportable, queryable, and consumable.

They do not change authority.

They do not identify biological truth.

They do not confer biological confidence.

The guiding rule is:

```text
Declare the source.

Declare the purpose.

Represent the evidence.

Expose lossiness.

Preserve authority.

Preserve lineage.

Never let representation become truth.
```

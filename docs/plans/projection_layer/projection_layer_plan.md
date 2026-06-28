# Projection Layer Implementation Plan

## Purpose

This document defines the implementation plan for the VDB Projection Layer.

A Projection View is a purpose-bound representation over preserved assertions or governed VDB-derived layers.

This plan describes how VDB will consume declared governed source layers, apply explicit projection policies, select and transform fields, preserve authority labels, preserve lineage, expose lossiness and omissions, preserve generation and currency context, validate reconstructability, and emit deterministic projection artifacts for inspection, reporting, export, query response, validation, certification, or downstream reasoning.

The Phase 4 Projection Layer implementation goal is:

```text
Deterministically emit purpose-bound Projection Views over declared
governed source layers while preserving source authority, source records,
lineage, field transformations, omissions, lossiness, generation, currency,
materialization format, and reconstruction paths without converting
representation into source evidence or biological interpretation.
```

Projection changes representation.

Projection does not change authority.

Projection makes evidence usable.

Projection must never make evidence more true.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/projection_layer/projection_layer_contract.md
```

The governing contract states that Projection Views must remain:

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

This plan is subordinate to the Projection Layer contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Projection Layer implementation role is to represent governed VDB records for declared purposes without changing the authority of those records.

A Projection View implementation answers:

```text
How is governed VDB evidence represented for this purpose?
```

It does not answer:

```text
What is biologically true?

What is causal?

What is clinically actionable?

Which evidence should be exposed?

Which evidence exists outside the declared source layer?

Which downstream reasoning conclusion is correct?

Which candidate should be prioritized?
```

Those questions belong to upstream source layers, governed surface policies, downstream reasoning systems, or returned producer assertions.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Corpus Generation selection
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry characterization
Evidence Convergence Surface construction
surface eligibility declaration
surface disclosure decisions
raw producer artifact parsing
producer TEP parsing
Query Surface governance
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
candidate prioritization
projection-derived biological confidence scoring
```

Projection Layer implementation is representation work.

It is not source-evidence work.

It is not exposure-governance work.

It is not topology work.

It is not geometry work.

It is not biological reasoning work.

---

# Initial Implementation Target

The initial implementation target is the Projection Layer build for the first MARK Phase 4 Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

The initial projection build may be identified as:

```text
mark_phase4_corpus_6tep_v1_projection_build_v1
```

The expected upstream input is the downstream projection input manifest emitted by the Evidence Convergence Surface implementation, such as:

```text
results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/
    downstream_projection_input_manifest.tsv
```

The first implementation should prove the general projection mechanics before overfitting to one downstream consumer.

Recommended initial projection types include:

```text
developer_inspection_projection
validation_projection
surface_membership_projection
```

RDGP-facing projections are supported by this plan, but should be implemented as specialized projection profiles after general projection mechanics are validated.

---

# Inputs

The Projection Layer implementation consumes:

```text
declared governed source layer
source record manifest
downstream projection input manifest when applicable
Projection Layer contract version
source layer contract version
system contract version
projection policy
field mapping policy
transformation policy when applicable
lossiness policy
authority labeling policy
generation and currency policy when applicable
consumer shaping policy when applicable
builder name
builder version
projection timestamp
```

When projecting from Evidence Convergence Surfaces, the implementation may consume:

```text
Evidence Convergence Surface Build manifest
Evidence Convergence Surface records
Surface Membership records
surface eligibility basis records
surface disclosure basis records
surface withholding records
surface lineage records
surface generation and currency records
downstream projection input manifest
```

When projecting from other governed layers, the implementation must declare the source layer and source records explicitly.

A projection without a declared source layer is not a VDB Projection View.

It is only a file, table, report, dashboard, or package.

---

# Outputs

The Projection Layer implementation should emit deterministic projection artifacts outside the governed source records it represents.

Expected outputs may include:

```text
projection_build_manifest.tsv
projection_build_manifest.json
projection_views.tsv
projection_views.jsonl
projection_source_records.tsv
projection_field_map.tsv
projection_transformations.tsv
projection_lossiness.tsv
projection_omissions.tsv
projection_authority_labels.tsv
projection_generation_currency.tsv
projection_reconstruction_paths.tsv
projection_validation_report.json
projection_validation_report.tsv
projection_build_report.md
```

Depending on the declared projection purpose and materialization format, additional materialized outputs may include:

```text
developer_inspection_projection.tsv
validation_projection.md
surface_membership_projection.tsv
assertion_record_projection.tsv
topology_inspection_projection.tsv
geometry_feature_projection.tsv
surface_export_projection.json
rdgp_facing_projection_manifest.tsv
rdgp_facing_projection.json
```

Materialized projection outputs are Projection Views.

They do not replace their governed source layer.

They do not become source evidence.

They do not become biological truth.

They do not perform downstream reasoning.

---

# Recommended Output Location

Initial Phase 4 Projection Layer outputs may be written under:

```text
results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1/
```

A recommended initial layout is:

```text
results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1/
    projection_build_manifest.tsv
    projection_build_manifest.json
    projection_views.tsv
    projection_views.jsonl
    projection_source_records.tsv
    projection_field_map.tsv
    projection_transformations.tsv
    projection_lossiness.tsv
    projection_omissions.tsv
    projection_authority_labels.tsv
    projection_generation_currency.tsv
    projection_reconstruction_paths.tsv
    projection_validation_report.json
    projection_validation_report.tsv
    projection_build_report.md
    materialized/
        developer_inspection_projection.tsv
        validation_projection.md
        surface_membership_projection.tsv
```

The output location should be configurable.

Projection output paths must not be confused with source layer paths.

Projection outputs must not overwrite source records.

---

# Required Projection Build Identity

Every Projection Layer build must have a stable identity.

A Projection Build identity should preserve:

```text
projection_build_id
projection_build_label when available
input_source_layer
input_source_manifest_id when available
input_corpus_generation_id when applicable
projection_policy_id
projection_policy_version when available
builder_name
builder_version when available
projection_timestamp
validation_status
certification_status when available
```

For the initial MARK projection build, a recommended identity shape is:

```text
projection_build_id: mark_phase4_corpus_6tep_v1_projection_build_v1
projection_build_label: MARK Phase 4 6-TEP Projection Build v1
input_source_layer: evidence_convergence_surface
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
projection_policy_id: mark_phase4_general_projection_policy
projection_policy_version: v1
```

Projection Build identity must remain stable across:

```text
validation
certification
reconstruction
consumer delivery
returned reasoning linkage when applicable
```

Human-readable labels may support inspection.

Labels must not replace stable Projection Build identity.

---

# Required Projection View Identity

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

Projection types may include:

```text
registration_unit_inventory_projection
corpus_generation_manifest_projection
assertion_record_table_projection
evidence_topology_inspection_projection
convergence_geometry_feature_projection
evidence_convergence_surface_projection
validation_report_projection
certification_report_projection
query_response_projection
developer_inspection_projection
dashboard_projection
TEP_VDB_export_projection
RDGP_facing_consumer_projection
future_consumer_projection
```

A Projection View identity must remain stable across validation, certification, reconstruction, consumer delivery, and returned reasoning linkage when applicable.

A projection label must not replace stable projection identity.

---

# Projection Policy Requirements

Every Projection View must declare a projection policy.

A projection policy must define or reference:

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
authority labeling rules
generation and currency rules
reconstruction requirements
validation requirements
```

For the initial MARK projection build, a policy may be identified as:

```text
mark_phase4_general_projection_policy_v1
```

A projection policy must be reconstructable.

A projection policy must not silently change source authority.

A projection policy must not silently hide evidence strata, uncertainty, lineage, generation context, or lossiness.

A Projection View without a declared projection policy is not compliant.

---

# Source Declaration Requirements

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

A Projection View generated without a declared source layer is not compliant.

A Projection View generated without reconstructable source records is not compliant.

Source declaration is the first validation gate for every projection.

---

# Full-Chain And Partial-Chain Projection Requirements

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

# Source Record Requirements

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

# Field Selection And Transformation Requirements

Projection Views may select, rename, transform, flatten, denormalize, summarize, aggregate, serialize, package, render, or materialize source records for a declared purpose.

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
projection_id
source layer
source record reference when applicable
source field reference when applicable
target field name when applicable
transformation rule
lossiness status
source authority class
reconstruction path
validation status
```

Field renaming must not obscure source authority.

Field flattening must not collapse evidence strata.

Aggregation must not hide independent evidence strata unless explicitly declared as lossy.

Summary generation must not replace source records.

Projection transformations must not create biological meaning.

---

# Field Map Requirements

Projection Views should emit or preserve a field map when fields are selected, renamed, transformed, omitted, flattened, or aggregated.

A field map may include:

```text
projection_id
source_layer
source_record_class
source_field
target_field
field_action
transformation_rule
field_authority_class
lossiness_status
omission_reason when applicable
reconstruction_path
validation_status
```

`field_action` values may include:

```text
selected
renamed
transformed
flattened
denormalized
aggregated
summarized
omitted
redacted
not_applicable
```

The field map should make projected output auditable.

Consumers must not be required to infer field provenance from column names alone.

---

# Lossiness And Omission Requirements

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

# Authority Labeling Requirements

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

Consumers must not be required to infer authority from projection layout, folder location, table name, report title, dashboard panel, or package format.

Authority must be explicit.

---

# Generation And Currency Requirements

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

# Materialization Neutrality Requirements

Projection Views must remain materialization-neutral.

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

The declared source layer and source records define the projection authority boundary.

---

# RDGP-Facing Projection Requirements

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

# Validation And Certification Projection Requirements

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

# Query Surface Boundary Requirements

A Query Surface is a governed access mechanism.

A Projection View is a purpose-bound representation emitted from governed VDB records.

The responsibility boundary is:

```text
Query Surface
    governed access pathway or interface over VDB records

Projection View
    purpose-bound representation emitted from governed VDB records
```

A Query Surface may emit Projection Views.

A query response may be a Projection View.

A Query Surface must not obscure projection source layer, authority status, lineage, lossiness, generation context, or reconstruction path.

A Projection View emitted through a Query Surface must satisfy this plan and the Projection Layer contract.

A Query Surface must not replace Projection Views.

A Projection View must not replace Query Surface governance.

---

# Validation Strategy

Projection View validation should operate in five tiers.

## Tier 1: Identity And Source Validation

Identity and source validation confirms that the projection has a declared purpose and governed source.

Validation must check:

```text
projection_id exists
projection identity is stable
projection purpose is declared
projection source layer is declared
projection source records are resolvable
projection policy is declared
projection builder identity is declared
projection builder version is declared when available
projection timestamp is declared
materialization format is declared
source authority class is declared
source validation status is preserved when available
source certification status is preserved when available
```

## Tier 2: Field And Transformation Validation

Field and transformation validation confirms that represented fields are auditable.

Validation must check:

```text
included fields are declared
omitted fields are declared when relevant
renamed fields preserve source references
transformation rules are declared
aggregation rules are declared when applicable
sorting rules are deterministic
field flattening does not collapse evidence strata silently
record denormalization preserves reconstruction path
summary generation does not replace source records
field authority labels are visible when applicable
```

## Tier 3: Authority, Lossiness, And Omission Validation

Authority and lossiness validation confirms that representation does not become source authority.

Validation must check:

```text
authority status is visible
source authority class is visible
lossiness status is declared
omission reason is declared when relevant
lossiness reason is declared when relevant
filtering policy is declared when relevant
redaction policy is declared when relevant
uncertainty is preserved or omission is declared when relevant
null semantics are preserved or omission is declared when relevant
generation context is visible
currency context is visible when applicable
omitted evidence is not represented as absent evidence
filtered evidence is not represented as negative evidence
summary-only projection is not represented as complete evidence
```

## Tier 4: Reconstruction Validation

Reconstruction validation confirms that source lineage can be recovered.

Validation must check:

```text
source lineage is reconstructable
projection reconstruction path exists
source records can be traced from projection records
source layer reconstruction is possible
source authority reconstruction is possible
field selection reconstruction is possible
field omission reconstruction is possible
transformation reconstruction is possible
lossiness reconstruction is possible
generation reconstruction is possible
currency reconstruction is possible
partial-chain omissions are declared when relevant
full-chain lineage is preserved when source is a surface
```

## Tier 5: Anti-Collapse Validation

Anti-collapse validation confirms that Projection View construction did not exceed its layer authority.

Validation must check:

```text
projection does not mutate source records
projection does not replace source records
projection does not overwrite source records
projection does not become source evidence
projection does not become biological truth
projection does not become clinical evidence
projection does not perform biological reasoning
projection does not embed RDGP reasoning
projection does not convert representation into authority
projection row does not replace Assertion Record
projection row does not replace topology relationship
projection row does not replace geometry feature
projection row does not replace surface membership
projection package does not replace Evidence Convergence Surface
dashboard is not treated as source truth
query response is not treated as source evidence
report is not treated as source evidence
consumer package is not treated as reasoning conclusion
pretty output is not treated as biological truth
```

Validation must confirm representation, lineage, lossiness disclosure, and authority boundaries.

Validation must not claim biological correctness.

---

# RDGP-Facing Projection Validation

RDGP-facing projection validation should additionally confirm:

```text
target consumer class is declared
producer strata are preserved
evidence-domain strata are preserved
modality strata are preserved when available
uncertainty states are preserved
null semantics are preserved when available
namespace mediation status is preserved
generation metadata are preserved
currency metadata are preserved
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

RDGP-facing projection validation must confirm reasoning affordance preservation.

It must not claim RDGP reasoning correctness.

It must not claim biological correctness.

---

# Determinism Requirements

Projection Layer outputs must be deterministic under fixed inputs.

Given the same:

```text
declared source layer
source records
source record generation
projection policy
field mapping policy
transformation policy
lossiness policy
authority labeling policy
materialization format
contract version
builder version
```

the builder should produce equivalent:

```text
projection_id
projection source declarations
projection source record references
field map records
transformation records
lossiness records
omission records
authority label records
generation and currency records
materialized projection outputs
validation outcomes
report sections
reconstruction paths
```

Determinism requirements include:

```text
stable projection_id generation
stable source record ordering
stable field ordering
stable transformation behavior
stable omission behavior
stable lossiness behavior
stable authority label behavior
stable generation behavior
stable currency behavior
stable materialization behavior
stable validation status vocabulary
stable unresolved-state vocabulary
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define projection order.

Filesystem traversal order must not define projection order.

All source record lists used in projection identity generation should be sorted by stable source identifiers.

All output rows should be sorted by declared projection policy.

---

# Reconstruction Requirements

Projection View artifacts must support reconstruction of:

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
field renaming rules
field transformation rules
filtering rules
aggregation rules when applicable
sorting rules when applicable
source authority labels
source validation status when available
source certification status when available
source lineage
generation context
currency context
consumer-specific shaping rules when applicable
materialization path
consumer delivery path when applicable
return-path identifiers when applicable
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

A Projection View without a reconstruction path is not compliant.

---

# Relationship To Evidence Convergence Surfaces

Evidence Convergence Surfaces provide governed exposure substrate for many Projection Views.

The responsibility boundary is:

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

The responsibility boundary is:

```text
Query Surface
    governed access pathway or interface over VDB records

Projection View
    purpose-bound representation emitted from governed VDB records
```

A Query Surface may emit Projection Views.

A query response may be a Projection View.

A Query Surface must not obscure projection source layer, authority status, lineage, lossiness, generation context, or reconstruction path.

A Projection View emitted through a Query Surface must satisfy this plan and the Projection Layer contract.

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

# Relationship To Downstream Reasoning

Downstream systems may reason over Projection Views.

Projection Views may expose reasoning affordances.

Projection Views do not perform downstream reasoning.

Projection Views must not determine:

```text
biological explanation
causality
pathogenicity
clinical actionability
candidate prioritization
RDGP confidence
downstream reasoning correctness
```

Returned downstream reasoning outputs may re-enter VDB only as governed producer assertions or another declared governed source layer.

Returned reasoning outputs must preserve return-path identifiers sufficient to reconstruct:

```text
source Projection View
source projection generation
source surface when applicable
source geometry when applicable
source topology when applicable
source Assertion Records when applicable
source Corpus Generation
source Registration Units when applicable
downstream reasoning producer
reasoning generation
reasoning output identity
```

Returned reasoning outputs must not overwrite the Projection View or its source evidence generation.

---

# Anti-Collapse Safeguards

Implementation must prevent:

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

Any implementation that performs one of these actions violates this plan and the Projection Layer contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture governed source records before running against the MARK corpus.

Recommended tests include:

```text
test_projection_requires_projection_id
test_projection_requires_projection_purpose
test_projection_requires_source_layer
test_projection_requires_source_records
test_projection_requires_projection_policy
test_projection_requires_materialization_format
test_projection_requires_lossiness_status
test_projection_preserves_source_authority_class
test_projection_preserves_source_record_references
test_projection_preserves_source_generation_context
test_projection_preserves_currency_context_when_available
test_projection_field_map_preserves_source_fields
test_projection_field_rename_preserves_source_reference
test_projection_field_omission_declares_omission_reason
test_projection_transformation_declares_rule
test_projection_aggregation_declares_lossiness
test_projection_flattening_does_not_collapse_strata_silently
test_projection_preserves_authority_labels
test_projection_preserves_uncertainty_or_declares_omission
test_projection_preserves_null_semantics_or_declares_omission
test_projection_reconstruction_path_exists
test_projection_partial_chain_declares_omitted_layers_when_relevant
test_projection_does_not_mutate_source_records
test_projection_does_not_replace_source_records
test_projection_does_not_become_source_evidence
test_projection_does_not_perform_biological_reasoning
test_projection_outputs_are_deterministic
```

MARK integration tests should confirm:

```text
mark_phase4_corpus_6tep_v1 downstream projection input manifest is accepted
projection build identity is stable
developer inspection projection is emitted when policy-enabled
validation projection is emitted when policy-enabled
surface membership projection is emitted when policy-enabled
projection source layer is declared
projection source records are declared
projection policy is declared
field map is emitted
lossiness records are emitted
authority labels are emitted
generation and currency records are emitted
projection validation report is deterministic
materialized projection outputs are deterministic
```

RDGP-facing projection tests should be added when an RDGP projection profile is implemented.

Tests must not require biological correctness.

Tests validate representation, reconstructability, determinism, lineage preservation, authority labeling, lossiness disclosure, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define Projection Layer build identity.

2. Define initial projection policy.

3. Define supported initial projection types.

4. Define source declaration behavior.

5. Define field inclusion and omission behavior.

6. Define field renaming and transformation behavior.

7. Define lossiness and omission vocabulary.

8. Define authority labeling behavior.

9. Define generation and currency behavior.

10. Define materialization behavior.

11. Load declared source layer manifest.

12. Load downstream projection input manifest when applicable.

13. Validate governed source boundary.

14. Generate Projection View identity.

15. Select source records according to projection policy.

16. Select and map fields according to projection policy.

17. Apply declared transformations.

18. Record omissions and lossiness.

19. Record authority labels.

20. Record source lineage.

21. Record generation and currency context.

22. Materialize Projection View outputs.

23. Validate Projection View artifacts.

24. Emit projection build manifest.

25. Emit projection metadata artifacts.

26. Emit materialized projection outputs.

27. Emit projection validation report.

28. Emit projection build report.

29. Add synthetic tests.

30. Add MARK corpus smoke test.

31. Add RDGP-facing projection profile only after general projection mechanics pass.
```

Each step must preserve source authority.

Each step must preserve reconstruction paths.

Each step must remain non-mutating with respect to all governed source layers.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_projection_view.py \
  --source-layer evidence_convergence_surface \
  --source-manifest results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/downstream_projection_input_manifest.tsv \
  --output-dir results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1 \
  --projection-build-id mark_phase4_corpus_6tep_v1_projection_build_v1 \
  --projection-policy-id mark_phase4_general_projection_policy_v1 \
  --projection-type developer_inspection_projection \
  --materialization-format tsv
```

or:

```bash
python scripts/phase4/validate_projection_view.py \
  --projection-build-manifest results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1/projection_build_manifest.tsv \
  --projection-views results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1/projection_views.tsv \
  --output-dir results/phase4/projection_layer/mark_phase4_corpus_6tep_v1_projection_build_v1
```

The exact script names are not contractually fixed.

The CLI must make source layer, source records, projection policy, projection type, materialization format, and output location explicit.

---

# Expected Input Manifest Shape

A downstream projection input manifest from Evidence Convergence Surfaces may include:

```text
surface_build_id
surface_id
surface_type
surface_purpose
input_geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
surface_membership_id
convergence_region_id
geometry_feature_id_summary
structural_motif_id_summary when applicable
eligibility_status
disclosure_status
withholding_reason when applicable
lossiness_status when applicable
generation_status when applicable
currency_status when applicable
validation_status
```

This manifest is produced by Evidence Convergence Surface implementation.

It is not a Projection View.

It must be validated against the declared source layer before projection begins.

---

# Expected Projection Build Manifest Shape

A Projection Build manifest may include:

```text
projection_build_id
projection_build_label
input_source_layer
input_source_manifest_id
input_corpus_generation_id
projection_policy_id
projection_policy_version
builder_name
builder_version
projection_timestamp
validation_status
certification_status
contract_version
schema_version
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Expected Projection View Shape

A Projection View table may include:

```text
projection_id
projection_label
projection_type
projection_purpose
projection_source_layer
projection_policy_id
projection_policy_version
projection_builder_name
projection_builder_version
projection_timestamp
materialization_format
materialization_path
lossiness_status
validation_status
certification_status
```

This table declares Projection Views.

It is not a source evidence table.

It is not biological reasoning.

---

# Expected Source Record Shape

A projection source record table may include:

```text
projection_id
projection_source_layer
source_record_id
source_record_type
source_record_generation
source_authority_class
source_validation_status
source_certification_status
source_lineage_reference
source_reconstruction_handle
validation_status
```

Source record tables must support reconstruction from projected output back to governed source records.

---

# Expected Field Map Shape

A projection field map may include:

```text
projection_id
source_layer
source_record_class
source_field
target_field
field_action
transformation_rule
field_authority_class
lossiness_status
omission_reason
reconstruction_path
validation_status
```

The field map must make field selection, renaming, transformation, omission, and flattening auditable.

---

# Expected Transformation Shape

A projection transformation table may include:

```text
projection_id
transformation_id
source_layer
source_record_class
source_field_reference
target_field
transformation_type
transformation_rule
aggregation_rule when applicable
sorting_rule when applicable
lossiness_status
reconstruction_path
validation_status
```

Transformation records must not create biological meaning.

---

# Expected Lossiness And Omission Shape

A projection lossiness table may include:

```text
projection_id
lossiness_status
lossiness_type
lossiness_reason
omitted_source_layer
omitted_source_record
omitted_field
omission_reason
filtering_policy
redaction_policy
summary_policy
reconstruction_path_to_omitted_material
validation_status
```

Lossiness and omission records must prevent hidden evidence omission.

---

# Expected Authority Label Shape

A projection authority label table may include:

```text
projection_id
projected_record_id
projection_source_layer
source_record_id
source_authority_class
projection_authority_class
producer_identity when applicable
assertion_id when applicable
derived_layer_identity when applicable
surface_eligibility_status when applicable
surface_disclosure_status when applicable
uncertainty_status when applicable
null_state when applicable
generation_or_currency_status when applicable
lossiness_status
reconstruction_handle
validation_status
```

Authority labels must make the projected record’s status explicit to consumers.

---

# Expected Generation And Currency Shape

A projection generation and currency table may include:

```text
projection_id
projection_generation_id
source_generation_id
source_build_identifier
source_policy_version
projection_policy_version
projection_timestamp
consumer_delivery_timestamp
refresh_status
staleness_status
supersession_status
supersedes_projection_id
superseded_by_projection_id
validation_status
```

Generation and currency records must prevent stale or superseded projections from masquerading as current.

---

# Expected Materialized Projection Shape

Materialized projection outputs may vary by projection type and format.

A materialized developer inspection projection may include:

```text
projection_id
projected_record_id
projection_source_layer
source_record_id
source_authority_class
projection_authority_class
display_label
source_summary
lineage_summary
lossiness_status
generation_or_currency_status
validation_status
```

A materialized surface membership projection may include:

```text
projection_id
surface_id
surface_membership_id
convergence_region_id
geometry_feature_id_summary
eligibility_status
disclosure_status
withholding_reason
source_authority_class
lossiness_status
reconstruction_handle
validation_status
```

An RDGP-facing projection profile should be specified separately when implemented.

---

# Exit Criteria

The Projection Layer implementation plan is complete when:

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
field map is emitted when relevant
transformation records are emitted when relevant
omission records are emitted when relevant
projection reconstruction path exists
projection is deterministic under fixed inputs
machine-readable projection artifacts are emitted
materialized Projection Views are emitted when policy-enabled
human-readable projection build report is emitted
projection validation report is emitted
Projection Views can serve their declared purpose
Projection Views do not mutate source records
Projection Views do not replace source records
Projection Views do not become source evidence
Projection Views do not perform biological reasoning
Projection Views remain materialization-neutral
anti-collapse safeguards pass
```

This implementation is not complete merely because a file, table, export, dashboard, API response, report, or package exists.

It is complete only when those records satisfy the Projection Layer contract and can safely serve as purpose-bound representations over governed VDB source layers.

---

# Summary

The Projection Layer implementation plan establishes the purpose-bound representation layer in VDB Phase 4.

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

The guiding rule is:

```text
Declare the source.

Declare the purpose.

Represent the evidence.

Expose lossiness.

Preserve authority.

Preserve lineage.

Preserve generation.

Preserve currency.

Remain materialization-neutral.

Do not mutate.

Do not overwrite.

Do not reason.

Never let representation become truth.
```

Projection Views make governed VDB evidence inspectable, transmissible, reportable, exportable, queryable, and consumable.

They do not change authority.

They do not identify biological truth.

They do not confer biological confidence.

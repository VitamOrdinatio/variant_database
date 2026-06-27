# Assertion Projection Taxonomy Specification

## Epoch IV: Projection Layer

| Epoch | Epoch Identity       | Epoch Purpose                                                                                       |
| ----- | -------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer          | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry    | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | Discovery Layer      | How do preserved evidence topologies become discoverable?                                           |
| IV    | **Projection Layer** | **How does one truth generate many useful views without duplication?**                              |
| V     | Rationale Layer      | Why do we do this?                                                                                  |

---

## Specification Status

This document defines implementation requirements for assertion projection taxonomy.

It is downstream of:

* `docs/design/assertion_projection_taxonomy.md`
* `docs/design/assertion_record_and_projection_model.md`
* `docs/implementation/specifications/assertion_record_spec.md`
* `docs/design/evidence_topology_model.md`
* `docs/implementation/specifications/evidence_topology_spec.md`
* `docs/design/convergence_geometry_model.md`
* `docs/implementation/specifications/convergence_geometry_spec.md`
* `docs/design/evidence_convergence_surface_model.md`
* `docs/implementation/specifications/evidence_convergence_surface_spec.md`

It is upstream of:

* `docs/implementation/schemas/assertion_projection_taxonomy_schema.md`

---

# Purpose

VDB preserves one scientific truth substrate and generates many useful views over that substrate.

Those views are projections.

This specification defines the requirements that any valid projection implementation must satisfy.

A valid projection implementation must allow VDB to generate useful views for audit, query, visualization, export, validation, review, interoperability, and downstream reasoning without creating duplicate truth.

---

# Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used normatively.

* **MUST** indicates a required implementation obligation.
* **MUST NOT** indicates a prohibited behavior.
* **SHOULD** indicates a strongly recommended behavior.
* **SHOULD NOT** indicates a discouraged behavior.
* **MAY** indicates an allowed but optional behavior.

---

# Governing Requirement

A valid assertion projection implementation **MUST** generate purpose-bound, source-traceable, reconstructable views from preserved assertions or governed derived layers.

A projection implementation **MUST NOT** create duplicate truth, transfer source authority, collapse evidence semantics, or perform interpretation.

The governing implementation invariant is:

```text
Projection changes representation, not authority.
```

A second governing rule is:

```text
Projection represents.
It does not replace.
```

---

# Scope

This specification governs:

* projection construction
* projection identity
* source layer declaration
* source object lineage
* projection purpose
* projection class
* projection transform
* projection representation
* projection materialization
* projection lineage
* controlled lossiness
* aggregation behavior
* redaction behavior
* export projections
* visualization projections
* projection currency
* projection validation
* prohibited projection patterns

---

# Out of Scope

This specification does not govern:

* creation of Assertion Records
* mutation of Assertion Records
* biological interpretation
* clinical interpretation
* statistical reasoning
* causal inference
* hypothesis confirmation
* downstream reasoning model behavior
* RDGP internal reasoning logic
* visual design style
* database-specific physical storage implementation

A projection may support downstream reasoning.

A projection must not perform downstream reasoning.

---

# Layer Relationship

All valid projections ultimately trace back to Assertion Records.

However, a projection does not need to be directly sourced from Assertion Records.

A valid projection **MAY** be directly sourced from any governed VDB layer, provided that the source layer itself preserves lineage back to Assertion Records.

Allowed source layers include:

* Assertion Records
* Evidence Topology
* Convergence Geometry
* Evidence Convergence Surfaces
* assertion corpora
* VDB generations
* lineage records
* validation records
* export packages

The valid dependency model is:

```text
Assertion Records
        ↓
Governed Derived Layers
        ↓
Purpose-Bound Projections
```

The invalid dependency model is:

```text
Projection
        ↓
New Source Truth
```

---

# Projection Identity Requirements

Every persistent projection **MUST** have projection identity.

Projection identity identifies the view.

Projection identity **MUST NOT** replace source evidence identity.

A valid projection implementation **MUST** preserve separation between:

```text
source identity
```

and:

```text
projection identity
```

Examples of source identity include:

* `assertion_id`
* `topology_relationship_id`
* `convergence_region_id`
* `surface_id`
* `assertion_corpus_id`
* `vdb_generation_id`

Examples of projection identity include:

* `projection_id`
* `projection_row_id`
* `projection_export_id`
* `projection_manifest_id`

A projection **MAY** contain projection-specific row identifiers, display identifiers, or export identifiers.

Those identifiers **MUST NOT** be treated as Assertion Record identifiers or source object identifiers.

---

# Source Layer Requirements

Every projection **MUST** declare a primary source layer.

Recommended source layer values include:

* `assertion`
* `topology`
* `geometry`
* `surface`
* `corpus`
* `generation`
* `lineage`
* `validation`
* `export_package`

A projection **MAY** declare secondary source layers.

For example, a surface projection may declare:

```text
primary_source_layer: surface
secondary_source_layers: geometry, topology, assertion
```

The primary source layer identifies the governed object class from which the projection is directly generated.

The secondary source layers identify upstream lineage or supporting context.

A projection **MUST NOT** present mixed source content without declaring its primary source layer.

---

# Source Object Requirements

Every projection **MUST** preserve source object identity or a resolvable source reconstruction path.

A projection **SHOULD** include explicit source object identifiers when the source set is small enough to represent directly.

For large source sets, a projection **MAY** preserve a reconstruction query, source corpus identifier, source build identifier, or manifest reference instead of enumerating every source object.

A projection source declaration **MUST** be sufficient to reconstruct the source set.

At minimum, a projection **MUST** preserve:

* source layer
* source object identifiers or reconstruction query
* source generation
* source build identity, where applicable
* source corpus identity, where applicable

A projection lacking source identity or reconstruction path is invalid.

---

# Projection Purpose Requirements

Every projection **MUST** declare its purpose.

Projection purpose answers:

> Why does this view exist?

Recommended projection purpose values include:

* `audit`
* `query`
* `visualization`
* `export`
* `reasoning_input`
* `validation`
* `review`
* `operator_status`
* `interoperability`
* `release`
* `documentation`
* `debugging`

Projection purpose **MUST** be operational, representational, transport-oriented, validation-oriented, or review-oriented.

Projection purpose **MUST NOT** be biological significance, clinical priority, pathogenicity, causality, therapeutic relevance, or hypothesis confirmation.

Invalid projection purposes include:

* `identify_disease_genes`
* `rank_biological_importance`
* `determine_pathogenicity`
* `infer_causality`
* `recommend_clinical_action`

Those activities belong to downstream reasoning or human interpretation, not VDB projection.

---

# Projection Class Requirements

Every projection **SHOULD** declare a projection class.

Recommended projection classes include:

* `assertion_centered_projection`
* `participant_centered_projection`
* `provenance_projection`
* `epistemic_projection`
* `stratum_projection`
* `topology_projection`
* `geometry_projection`
* `surface_projection`
* `export_projection`
* `visualization_projection`
* `validation_projection`
* `release_projection`

A projection implementation **MAY** introduce additional projection classes.

Any additional projection class **MUST** still satisfy source identity, purpose, transform, lineage, reconstructability, and non-authority requirements.

Projection class describes the view family.

It **MUST NOT** imply biological meaning.

---

# Projection Transform Requirements

Every projection **MUST** declare its transform.

Projection transform answers:

> How was the source represented as this view?

Recommended transform classes include:

* `filter`
* `group`
* `sort`
* `summarize`
* `aggregate`
* `reshape`
* `serialize`
* `index`
* `redact`
* `label`
* `visualize`
* `package`

A projection transform **MUST** be:

* source-traceable
* reconstructable
* purpose-bound
* non-authoritative
* semantically safe

A projection transform **MUST NOT** silently alter scientific meaning.

A projection transform **MUST NOT** remove source identity required for reconstruction.

A projection transform **MUST NOT** collapse evidence strata, epistemic status, participant roles, producer identity, or provenance unless the lossiness is explicitly declared and source reconstruction remains possible.

---

# Projection Transform Basis

Every projection **SHOULD** declare a transform basis.

Transform basis explains why the transform is appropriate for the projection purpose.

Examples include:

* `query_filter`
* `audit_grouping`
* `validation_summary`
* `export_serialization`
* `visualization_layout`
* `reasoning_input_packaging`
* `operator_status_summary`
* `release_snapshot`
* `interoperability_conversion`

Transform basis **MUST** remain non-interpretive.

Invalid transform bases include:

* `biological_importance`
* `clinical_priority`
* `pathogenic_relevance`
* `causal_strength`
* `mechanistic_likelihood`

---

# Projection Representation Requirements

Every projection **SHOULD** declare its representation.

Recommended representation values include:

* `table`
* `json`
* `yaml`
* `graph`
* `hypergraph`
* `matrix`
* `network`
* `timeline`
* `summary`
* `index`
* `report`
* `dashboard`
* `figure`
* `package`
* `manifest`
* `validation_report`

Representation format **MUST NOT** determine authority.

A graph projection is not more authoritative than a table projection.

A dashboard projection is not a conclusion.

A figure projection is not evidence.

A package projection is not source truth.

Representation changes usability.

It does not change scientific authority.

---

# Projection Materialization Requirements

A projection **MAY** be generated in different materialization modes.

Recommended materialization modes include:

* `ephemeral`
* `cached`
* `materialized`
* `exported`
* `archived`

## Ephemeral Projection

An ephemeral projection is generated on demand and not persisted.

Ephemeral projections **SHOULD** still preserve source identity during their lifetime.

## Cached Projection

A cached projection is temporarily persisted for performance.

Cached projections **MUST NOT** be treated as source truth.

Cached projections **SHOULD** preserve cache creation time, source generation, and invalidation basis.

## Materialized Projection

A materialized projection is persistently stored as a reusable view.

Materialized projections **MUST** preserve source generation, transform identity, transform version, and reconstruction path.

Materialized projections **MUST NOT** become canonical evidence stores.

## Exported Projection

An exported projection is serialized or packaged for downstream or external consumption.

Exported projections **MUST** preserve source identity, source generation, projection purpose, consumer, and lineage depth.

## Archived Projection

An archived projection preserves a historical view of a specific source generation.

Archived projections **MUST** declare the source generation they represent.

Archived projections **MUST NOT** be presented as current unless they are current relative to their declared source state.

The governing rule is:

```text
Materialization does not confer authority.
```

---

# Projection Currency Requirements

Projection implementations **SHOULD** support source currency metadata for cached, materialized, exported, and archived projections.

Projection currency answers:

> Is this projection current relative to its declared source layer and source generation?

Recommended projection currency states include:

* `current`
* `historical`
* `stale_due_to_source_change`
* `stale_due_to_transform_change`
* `stale_due_to_policy_change`
* `not_evaluated`

Projection currency **MUST** be metadata-derived.

Projection currency **MUST NOT** be meaning-derived.

A projection may become stale because its source layer changed, its transform changed, or its disclosure policy changed.

A projection must not be called stale because VDB believes its biological conclusion changed.

Projections do not contain VDB biological conclusions.

---

# Projection Lineage Requirements

Every projection **MUST** preserve lineage to its source.

At minimum, a projection lineage record **MUST** support:

* projection identity
* source layer
* source object identifiers or reconstruction query
* source generation
* source build identity, where applicable
* source corpus identity, where applicable
* projection purpose
* projection class
* projection transform
* transform version, where applicable
* projection parameters
* projection representation
* projection materialization mode
* projection consumer, where applicable
* created_at or equivalent version marker

A projection over a derived layer **MUST** preserve enough source references to reach the upstream Assertion Records through governed lineage.

For example:

```text
surface projection
        ↓
surface_id
        ↓
convergence_region_id
        ↓
topology_relationship_id
        ↓
assertion_id
```

A projection **MAY** reference lineage indirectly through build identifiers, manifests, or resolvable lineage records.

A projection without reconstructable lineage is invalid.

---

# Reconstructability Requirements

A projection **MUST** be reconstructable from its declared source, transform, parameters, implementation version, and policy context.

Given the same:

* source layer
* source objects
* source generation
* source build
* projection transform
* transform parameters
* projection implementation version
* disclosure policy, where applicable

the implementation **MUST** produce an equivalent projection.

Equivalent projections do not need to be byte-identical across storage backends.

They must preserve the same source semantics, projection purpose, lineage, transform basis, and non-authoritative status.

---

# Controlled Lossiness Requirements

Some projections may intentionally omit detail.

Examples include:

* dashboards
* summary tables
* public figures
* validation reports
* redacted exports
* compact transport packages

Controlled lossiness is permitted only when:

* projection purpose is declared
* transform basis is declared
* omitted content class is declared or inferable from policy
* source reconstruction remains possible
* the projection does not claim to be complete source truth

A lossy projection **MUST NOT** pretend to be lossless.

A lossy projection **MUST NOT** remove the ability to reconstruct or resolve source evidence.

A lossy projection **MUST NOT** remove provenance, epistemic status, or evidence strata required for its declared purpose.

The central rule is:

```text
Lossy projection is allowed.
Unlabeled semantic loss is not.
```

---

# Aggregation Requirements

Projection implementations **MAY** aggregate source content.

Aggregation includes counts, grouped summaries, feature summaries, participant summaries, producer summaries, and stratum summaries.

Aggregated projections **MUST** declare:

* aggregation basis
* source object set or reconstruction query
* aggregation transform
* source scope
* whether the aggregation is complete or scoped

An aggregation **MUST NOT** be represented as source truth.

An aggregation **MUST NOT** erase source identity.

An aggregation **MUST NOT** merge distinct evidence strata, epistemic states, producer families, or modalities into an unlabeled support class.

Acceptable:

```text
assertion_count = 7
aggregation_basis = count_assertions_by_participant
source_assertion_ids = [...]
```

Acceptable for large source sets:

```text
assertion_count = 12831
aggregation_basis = count_assertions_by_producer
source_corpus_id = assertion_corpus_004
reconstruction_query_id = query_assertions_by_producer_v1
```

Invalid:

```text
support_score = 7
```

with no source set, aggregation basis, or explanation.

---

# Redaction Requirements

Projection implementations **MAY** support redacted projections.

Redaction must be governed.

A redacted projection **MUST** declare:

* redaction policy identity
* redaction basis
* redacted element classes
* source reconstruction path or privileged source reference
* consumer or disclosure context

A redacted projection **MUST NOT** present itself as complete source truth.

A redacted projection **MUST NOT** alter source identity.

A redacted projection **MUST NOT** create a new evidence object to replace the redacted source.

---

# Labeling Requirements

Projection implementations **MAY** attach human-readable labels.

Labels may include:

* gene symbols
* sample labels
* producer labels
* phenotype labels
* surface labels
* display names
* report headings

Labels **MUST NOT** replace canonical identifiers.

Labels **MUST** remain distinguishable from source identity.

For example:

```text
gene_symbol: POLG
gene_id: ENSG00000140521
```

is valid.

But:

```text
participant_id: POLG
```

without namespace or canonical identifier may be insufficient when canonical identity is required.

Labels **MUST NOT** encode biological conclusions unless those conclusions are preserved source assertions and clearly attributed.

---

# Export Projection Requirements

Export projections are transport-oriented views generated for downstream or external consumers.

Export projections **MUST** declare:

* projection identity
* source layer
* source object identity
* source generation
* projection purpose
* consumer
* disclosure basis or disclosure policy
* transform identity
* representation format
* lineage depth
* export package identity, where applicable
* export timestamp or equivalent version marker

An export projection **MUST NOT** be treated as the source object.

For example:

```text
Evidence Convergence Surface
        persistent governed exposure object

TEP-VDB export projection
        transport view generated from that surface
```

The TEP-VDB package is not the surface itself.

It is a projection generated for downstream consumption.

Export projections for downstream reasoning **SHOULD** preserve enough lineage and evidence strata for the downstream reasoning engine to understand what it is reasoning over.

---

# Visualization Projection Requirements

Visualization projections are human-readable or graphical views.

Visualization projections may include:

* figures
* dashboards
* diagrams
* network renderings
* timelines
* summary panels
* operator charts

Visualization projections **MUST NOT** be treated as evidence objects.

Visualization projections used for audit, review, or release **SHOULD** preserve source references or links to source lineage.

Visualization projections **SHOULD** declare simplifications, omitted content, grouping rules, or display transforms where those choices affect interpretation.

Visualization projections **MUST NOT** encode biological conclusions unless those conclusions are preserved source assertions and clearly attributed.

The central visualization rule is:

```text
A visualization may explain a view.
It must not become the evidence.
```

---

# Validation Projection Requirements

Validation projections are views generated to inspect conformance, completeness, consistency, or implementation behavior.

Validation projections **MAY** report:

* missing source identity
* missing lineage
* missing projection purpose
* missing transform
* stale materialized projections
* invalid eligibility or disclosure references
* missing evidence strata
* unreconstructable exports
* forbidden interpretive labels

Validation projections **MUST NOT** make biological claims.

Validation projections **MAY** classify projection validity.

Projection validity is a system property.

It is not a biological claim.

---

# Release Projection Requirements

Release projections are generated for milestone, version, archive, certification, or public release contexts.

Release projections **MUST** declare:

* source VDB generation
* source corpus or object set
* projection transform
* projection purpose
* release identifier, where applicable
* created_at or equivalent version marker

Release projections preserve historical state.

They **MUST NOT** replace the source VDB generation.

They **MUST NOT** imply that later VDB generations contain the same evidence state.

---

# Projection Ordering and Ranking Requirements

Projection implementations **MAY** order projection outputs for retrieval, display, auditing, pagination, or review.

Allowed ordering bases include:

* deterministic identifier
* source generation
* build time
* producer
* participant
* modality
* evidence stratum
* projection class
* surface status
* refresh state
* validation status
* assertion count
* feature count

Projection ordering **MUST NOT** be represented as biological priority, clinical priority, pathogenicity likelihood, causal strength, or mechanistic importance unless such ranking is itself a preserved source assertion from an external reasoning producer and clearly attributed.

Projection sorting is allowed.

Projection-derived biological ranking is not.

---

# Projection Consumer Requirements

A projection **MAY** declare an intended consumer.

Recommended consumer classes include:

* `vdb_operator`
* `rdgp`
* `sage`
* `validation_workflow`
* `visualization_layer`
* `external_export_consumer`
* `human_reviewer`
* `future_reasoning_engine`
* `release_workflow`
* `audit_workflow`

Consumer declaration may affect disclosure depth, representation format, export format, and lineage requirements.

Consumer declaration **MUST NOT** alter source truth.

Consumer declaration **MUST NOT** justify semantic collapse.

---

# Projection Safety Requirements

A valid projection implementation **MUST** preserve source identity.

A valid projection implementation **MUST** preserve source layer.

A valid projection implementation **MUST** preserve projection purpose.

A valid projection implementation **MUST** preserve transform identity.

A valid projection implementation **MUST** preserve reconstructability.

A valid projection implementation **MUST** preserve provenance required for the projection purpose.

A valid projection implementation **MUST** preserve epistemic distinctions required for the projection purpose.

A valid projection implementation **MUST** preserve evidence strata required for the projection purpose.

A valid projection implementation **MUST** preserve participant roles and namespaces when projecting participant-centered evidence.

A valid projection implementation **MUST NOT** transfer authority from source objects to projection objects.

A valid projection implementation **MUST NOT** create duplicate scientific truth.

---

# Non-Interpretation Requirements

A projection **MUST NOT** claim:

* biological causality
* disease mechanism
* pathogenicity
* clinical actionability
* therapeutic relevance
* statistical significance generated by VDB
* hypothesis confirmation
* biological correctness
* clinical priority
* mechanistic explanation
* diagnostic relevance

A projection **MAY** represent such claims only when they exist as preserved source assertions from an authorized producer or downstream reasoning system.

When representing such claims, the projection **MUST** preserve attribution to the source assertion.

A projection **MUST NOT** convert a source-attributed claim into a VDB claim.

---

# Invalid Projection Conditions

A projection is invalid if it:

* lacks projection identity when persisted
* lacks source layer
* lacks source identity or reconstruction path
* lacks projection purpose
* lacks projection transform
* lacks reconstructability
* replaces source identity with projection identity
* copies assertion content without preserving assertion identity
* collapses evidence strata into unlabeled support
* collapses epistemic states into unlabeled support
* removes provenance required for its declared purpose
* performs biological interpretation
* performs clinical interpretation
* claims statistical significance generated by VDB
* ranks by biological importance without source attribution
* treats cached or materialized projection as canonical truth
* exports untraceable summaries
* presents stale projection as current
* presents lossy projection as complete
* aggregates without aggregation basis
* redacts without redaction basis
* visualizes without preserving audit path when used for audit or review

---

# Validation Requirements

A valid implementation **SHOULD** provide validation checks for projection safety.

Validation checks **SHOULD** include:

* projection identity presence
* source layer presence
* source object identity or reconstruction path presence
* source generation presence
* projection purpose presence
* projection transform presence
* transform parameter presence where required
* lineage completeness
* representation declaration
* materialization mode declaration
* controlled lossiness declaration where applicable
* aggregation basis declaration where applicable
* redaction basis declaration where applicable
* absence of forbidden interpretive claims
* preservation of evidence strata where applicable
* preservation of epistemic distinctions where applicable
* preservation of provenance required by purpose
* reconstruction feasibility

Validation failures **SHOULD** distinguish between:

* missing identity
* missing source declaration
* missing purpose
* missing transform
* missing lineage
* unreconstructable projection
* semantic collapse
* authority transfer risk
* stale projection state
* forbidden interpretation
* incomplete disclosure
* invalid export

A projection may be valid but historical.

A projection may be valid but stale.

A projection may be lossy but valid if lossiness is declared and reconstruction remains possible.

---

# Relationship to Evidence Convergence Surfaces

Evidence Convergence Surfaces are governed exposure objects.

Projection may generate views over those surfaces.

For example:

```text
Evidence Convergence Surface
        ↓
Surface Projection
        ↓
TEP-VDB Export Projection
        ↓
RDGP
```

The surface remains the source exposure object.

The projection is the purpose-bound representation.

The export package is the transport artifact.

Projection implementations **MUST** preserve these distinctions.

---

# Relationship to Downstream Reasoning

A projection may serve as input to downstream reasoning.

For example, a reasoning input projection may package surface evidence strata, lineage, provenance, and generation metadata for RDGP.

Such a projection **MUST NOT** perform RDGP reasoning.

The valid route is:

```text
Projection
        ↓
Downstream reasoning
        ↓
Reasoning assertions
        ↓
VDB preservation
```

Downstream reasoning outputs **MUST** re-enter VDB as Assertion Records if they are to become part of the preserved evidence substrate.

They **MUST NOT** modify the projection that served as input.

They **MUST NOT** modify source assertions, topology, geometry, or surfaces.

---

# Implementation Independence

This specification does not require a particular storage backend, projection engine, query language, serialization format, graph representation, or visualization library.

Valid implementations may use:

* relational views
* materialized tables
* JSON documents
* YAML documents
* graph projections
* hypergraph projections
* matrix exports
* manifests
* dashboards
* static reports
* package artifacts
* future representation systems

Representation may vary.

Projection obligations do not.

---

# Summary

A valid assertion projection implementation allows VDB to generate many useful views from one preserved truth substrate.

It must preserve:

* projection identity
* source identity
* source layer
* source generation
* projection purpose
* projection transform
* projection representation
* projection materialization state
* projection lineage
* reconstruction path
* semantic distinctions
* authority boundaries

It must not create:

* duplicate truth
* untraceable summaries
* semantic collapse
* authority transfer
* biological interpretation
* clinical interpretation
* VDB-generated statistical conclusions

The central invariant of the Projection Layer is:

```text
Projection is view generation, not evidence generation.
```

A projection may make evidence easier to use.

It must never become the evidence.

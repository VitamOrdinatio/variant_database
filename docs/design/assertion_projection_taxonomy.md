# Assertion Projection Taxonomy

## Epoch IV: Projection Layer

| Epoch | Epoch Identity       | Epoch Purpose                                                                                       |
| ----- | -------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer          | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry    | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | Discovery Layer      | How do preserved evidence topologies become discoverable?                                           |
| IV    | **Projection Layer** | **How does one truth generate many useful views without duplication?**                              |
| V     | Rationale Layer      | Why do we do this?                                                                                  |

---

## Epoch IV: Projection Layer

```text
Assertion Projection Taxonomy <- THIS DOCUMENT
        ↓
Assertion Projection Taxonomy Specification
        ↓
Assertion Projection Taxonomy Schema
```

See also:

* `docs/design/assertion_record_and_projection_model.md`
* `docs/implementation/specifications/assertion_record_spec.md`
* `docs/implementation/schemas/assertion_record_schema.md`
* `docs/design/evidence_topology_model.md`
* `docs/design/convergence_geometry_model.md`
* `docs/design/evidence_convergence_surface_model.md`

---

# Purpose

VDB preserves one scientific truth substrate and generates many controlled views over it.

Those views are projections.

A projection may make preserved evidence easier to query, audit, validate, visualize, export, compare, package, or hand to downstream reasoning systems.

A projection must never become a second source of truth.

This document defines a taxonomy for assertion projections: purpose-bound, reconstructable views derived from Assertion Records or from governed layers that themselves derive from Assertion Records.

Although the filename refers to assertion projection, projections may be generated from multiple VDB layers. This is because every valid VDB layer ultimately traces back to preserved Assertion Records.

Assertion Records remain the primitive truth substrate.

Projections are useful views over that substrate.

---

# Governing Principle

Projection is view generation, not evidence generation.

Projection changes access.

It does not change authority.

```text
Projection
    ≠
Truth
```

A projection may duplicate representation for convenience.

It must not duplicate scientific authority.

---

# Relationship to Prior Epochs

Epoch IV inherits the layer discipline established by Epochs I through III.

| Layer                         | Responsibility                        |
| ----------------------------- | ------------------------------------- |
| Assertion Records             | Preserve                              |
| Evidence Topology             | Organize                              |
| Convergence Geometry          | Characterize                          |
| Evidence Convergence Surfaces | Expose                                |
| Projections                   | Render, package, summarize, or format |
| Downstream reasoning          | Evaluate                              |
| Scientists / clinicians       | Interpret                             |

Projections may operate over several source layers:

```text
Assertion Records ───────────────→ assertion projections
Evidence Topology ───────────────→ topology projections
Convergence Geometry ────────────→ geometry projections
Evidence Convergence Surfaces ───→ surface projections
Lineage / corpus state ──────────→ audit and validation projections
```

Projection does not create a new truth layer above surfaces.

Projection is a controlled view-generation discipline across the VDB substrate.

Projection is best understood as a lateral representation capability rather than a new vertical scientific layer.

Assertion Records preserve truth.

Topology, geometry, and surfaces build governed structure and exposure over that truth.

Projection operates across those governed layers to produce purpose-bound views for query, audit, visualization, validation, export, review, interoperability, or downstream reasoning.

A projection exists because source evidence or governed derived structure already exists.

It does not create a new scientific layer above surfaces.

---

# Definition

An assertion projection is a purpose-bound, reconstructable view derived from preserved assertions or governed derived layers, created to support a declared use case without duplicating or replacing source truth.

A valid projection must answer:

* What source layer did it come from?
* What source objects does it represent?
* Why does it exist?
* How was it generated?
* What transform was applied?
* What purpose does it serve?
* Can it be reconstructed?
* What claims is it forbidden from making?

If a projection cannot answer these questions, it is not safe for VDB use.

---

# Projection Is Not Truth

A projection is not the scientific evidence itself.

The source Assertion Records remain authoritative.

Derived layers retain their own governed identity.

A projection may represent those layers, but it must not replace them.

```text
assertion_id
        identifies preserved scientific evidence

projection_id
        identifies a view over preserved evidence or derived structure
```

Projection identity identifies the view.

It does not identify the scientific truth represented by the view.

---

# Why Projection Is Needed

VDB must support many legitimate access patterns without duplicating truth.

Different consumers need different views:

* operators need status views
* validators need completeness views
* reasoning systems need structured input packages
* auditors need provenance and lineage views
* scientists need query and review views
* visualization layers need simplified renderable views
* export workflows need portable transport views
* future systems may need mathematical or semantic projections not currently anticipated

These views should be generated from preserved truth and governed derived layers.

They should not become parallel evidence stores.

---

# Projection as Controlled Representation

Projection is representation control.

It may involve:

* filtering
* grouping
* sorting
* summarizing
* aggregating
* reshaping
* serializing
* indexing
* formatting
* labeling
* redacting
* packaging
* visualizing

These operations are allowed only when they remain:

* source-traceable
* reconstructable
* non-authoritative
* purpose-bound
* epistemically safe

Projection convenience must not justify semantic collapse.

---

# Projection Source Layers

Every projection must declare its source layer.

A source layer identifies the governed VDB layer from which the projection is derived.

Recommended source layer categories include:

## Assertion Source

A projection derived directly from Assertion Records.

Example:

```text
All Assertion Records involving POLG.
```

## Topology Source

A projection derived from Evidence Topology.

Example:

```text
All topology relationships connecting POLG to mitochondrial disease context.
```

## Geometry Source

A projection derived from Convergence Geometry.

Example:

```text
Geometry feature summary for POLG-centered convergence regions.
```

## Surface Source

A projection derived from Evidence Convergence Surfaces.

Example:

```text
RDGP-compatible package projection for an active evidence convergence surface.
```

## Corpus Source

A projection derived from a declared assertion corpus or VDB generation.

Example:

```text
All producer assertion counts for VDB generation 3.
```

## Lineage Source

A projection derived from provenance and reconstruction paths.

Example:

```text
All producer TEPs contributing to a given surface.
```

A projection may reference multiple source layers, but it must declare a primary source layer.

---

# Projection Purpose Taxonomy

Every projection must declare its purpose.

Projection purpose answers:

> Why does this view exist?

Recommended projection purposes include:

## Audit

Used to inspect provenance, lineage, completeness, source identity, or reconstruction paths.

Example:

```text
Show all Assertion Records lacking producer artifact lineage.
```

## Query

Used to answer a structured retrieval question.

Example:

```text
Return all preserved assertions involving POLG and mitochondrial disease context.
```

## Visualization

Used to render evidence or derived structure for human inspection.

Example:

```text
Render a participant-centered topology neighborhood as a network diagram.
```

## Export

Used to package VDB content for external or downstream systems.

Example:

```text
Generate a TEP-VDB package for RDGP.
```

## Reasoning Input

Used to provide structured input to downstream reasoning systems.

Example:

```text
Generate a surface-derived projection containing evidence strata and lineage for RDGP evaluation.
```

## Validation

Used to check schema conformance, lineage completeness, generation consistency, or implementation correctness.

Example:

```text
List all surfaces without source Convergence Region references.
```

## Review

Used for human inspection of evidence state.

Example:

```text
Produce an operator review table of stale reasoning-informed surfaces.
```

## Operator Status

Used to communicate system state without interpretation.

Example:

```text
Show all surfaces with refresh-triggered currency warnings.
```

## Interoperability

Used to support format conversion or exchange between systems.

Example:

```text
Serialize assertion lineage as JSON for external consumer compatibility.
```

Projection purpose must remain distinct from biological importance.

---

# Projection Representation Taxonomy

A projection may use many representational forms.

Recommended projection representation categories include:

* table
* JSON
* YAML
* graph
* hypergraph
* matrix
* network
* timeline
* summary
* index
* report
* dashboard
* figure
* package
* manifest
* validation report

Representation format does not determine authority.

A graph projection is not more truthful than a table projection.

A dashboard is not a conclusion.

A figure is not evidence.

A package is not the source truth.

Each representation is a view.

---

# Projection Materialization Taxonomy

A projection may be generated in different materialization modes.

## Ephemeral Projection

Generated on demand and not persisted.

Example:

```text
Interactive query result.
```

## Cached Projection

Persisted temporarily for performance.

Example:

```text
Cached surface summary for repeated operator queries.
```

## Materialized Projection

Persisted as a reusable view.

Example:

```text
Materialized assertion summary table for validation workflows.
```

## Exported Projection

Serialized for downstream or external consumption.

Example:

```text
TEP-VDB export projection for RDGP.
```

## Archived Projection

Preserved as a historical view of a specific VDB generation or release state.

Example:

```text
Release-time projection of all certified surfaces.
```

Materialization does not confer authority.

A materialized projection remains derived.

An archived projection remains a historical view.

---

# Projection Consumer Taxonomy

A projection may be generated for different consumers.

Recommended consumer categories include:

* VDB operator
* RDGP
* SAGE
* validation workflow
* visualization layer
* external export consumer
* human reviewer
* future reasoning engine
* release workflow
* audit workflow

The consumer helps determine disclosure depth, representation format, and lineage requirements.

The consumer does not change source truth.

---

# Core Projection Classes

Projection classes describe common families of views.

These classes may overlap.

A projection should declare its class, source layer, purpose, representation, and consumer.

---

## Assertion-Centered Projection

A view over Assertion Records.

Used for:

* audit
* query
* export
* validation
* review

Examples:

```text
All Assertion Records involving POLG.
All GSC assertions with epistemic_status = semantic_prior.
All VAP assertions emitted for HG002.
```

Assertion-centered projections are close to the truth substrate and must preserve assertion identity.

They must not merge distinct assertions into unlabeled summaries without traceability.

---

## Participant-Centered Projection

A view grouped around one or more participants.

Participants may include:

* gene
* variant
* sample
* phenotype
* condition
* producer
* publication
* pathway
* surface anchor

Examples:

```text
All assertions where POLG appears as a participant.
All topology relationships involving HG002.
All surfaces anchored on mitochondrial disease phenotype context.
```

Participant-centered projections are useful for query and review.

They must preserve participant roles and namespaces.

---

## Provenance Projection

A view over source lineage, producer identity, and artifact history.

Used for:

* audit
* certification
* traceback
* reproducibility
* release review

Examples:

```text
Show all producer TEPs contributing to a surface.
Show the source artifact lineage for a GSC assertion.
Show every build involved in producing an outbound TEP-VDB package.
```

Provenance projections must preserve producer identity and artifact references.

They must not flatten lineage.

---

## Epistemic Projection

A view grouped by epistemic status or evidence state.

Used for:

* uncertainty review
* null evidence inspection
* conflict inspection
* reasoning input
* evidence quality review

Examples:

```text
Separate observed, semantic-prior, inferred, validation, and reasoning-output assertions.
Show all null or negative assertions for a participant.
Show all reasoning-output assertions separately from raw producer assertions.
```

Epistemic projections must not collapse epistemic states.

They must preserve the distinction between observed, inferred, semantic, validation, and reasoning-derived evidence.

---

## Stratum Projection

A view organized by evidence stratum.

Used for:

* multi-modal review
* reasoning input
* refresh inspection
* composite surface analysis

Examples:

```text
Show VAP variant evidence, GSC semantic prior evidence, PTN proteomic evidence, and RDGP reasoning output as separate strata.
```

Stratum projections prevent apples-and-oranges collapse.

They may show structural intersection among strata.

They must not claim equivalence among strata.

---

## Topology Projection

A view over Evidence Topology.

Used for:

* relationship inspection
* neighborhood review
* query expansion
* network visualization
* topology validation

Examples:

```text
Show topology relationships connecting POLG, mitochondrial phenotype context, and contributing producers.
Show all topology relationships derived from shared participant basis.
```

Topology projections must preserve topology derivation basis.

They must not become replacement topology.

---

## Geometry Projection

A view over Convergence Geometry.

Used for:

* convergence region review
* structural motif inspection
* feature summary
* geometry validation
* downstream surface preparation

Examples:

```text
Show geometry features for POLG-centered convergence regions.
Show all convergence regions with multi-modal geometry.
```

Geometry projections must preserve region-bounding basis and geometry build identity.

They must not claim biological significance.

---

## Surface Projection

A view over Evidence Convergence Surfaces.

Used for:

* operator review
* RDGP handoff
* refresh audit
* surface comparison
* disclosure inspection

Examples:

```text
Show all active surfaces.
Show all reasoning-informed surfaces stale due to new evidence.
Show all surfaces eligible for RDGP export.
```

Surface projections must preserve surface identity, generation, eligibility basis, disclosure basis, evidence strata, and reasoning currency where applicable.

They must not become the surface itself.

---

## Export Projection

A transport-oriented projection used to generate outbound artifacts.

Used for:

* TEP-VDB packaging
* downstream reasoning input
* external interoperability
* archival handoff

Examples:

```text
Generate RDGP-compatible export projection for surface generation 3.
Generate a JSON package containing surface lineage and evidence strata.
```

Export projections must declare:

* source surface or source layer
* export purpose
* consumer
* disclosure basis
* source generation
* included lineage depth

An export projection is not the persistent source object.

It is a transport view.

---

## Visualization Projection

A human-readable or graphical projection.

Used for:

* dashboards
* figures
* diagrams
* operator inspection
* public documentation
* exploratory review

Examples:

```text
Render a topology neighborhood as a network.
Render evidence strata as separate lanes.
Render refresh state as operator dashboard rows.
```

Visualization projections are explanatory aids.

They are not evidence objects.

They must preserve access to source identity and lineage if used for audit or review.

---

## Validation Projection

A projection built to support testing or validation.

Used for:

* schema validation
* lineage completeness checks
* smoke testing
* certification
* release review

Examples:

```text
List all surfaces missing SurfaceEligibility records.
List all Assertion Records lacking producer identity.
List all reasoning-informed surfaces missing reasoning method version.
```

Validation projections may report invalidity or incompleteness.

They must not make biological claims.

---

## Release Projection

A projection generated for a release, milestone, or certification bundle.

Used for:

* release notes
* certification reports
* archived release state
* reproducibility snapshots

Examples:

```text
Projection of all certified surfaces in VDB Phase 4 release.
Projection of all producer corpora included in a release bundle.
```

Release projections preserve historical state.

They must not replace the source VDB generation or source objects.

---

# Projection Transform Semantics

Projection transforms describe how source content is represented in the view.

Common transform classes include:

## Filter

Select a subset of source objects.

Example:

```text
Assertions involving POLG.
```

## Group

Organize source objects by a shared property.

Example:

```text
Assertions grouped by producer.
```

## Sort

Order source objects deterministically.

Example:

```text
Surfaces sorted by generation and refresh state.
```

## Summarize

Represent source objects using non-authoritative summary fields.

Example:

```text
Counts of assertions per producer.
```

## Aggregate

Compute derived counts or summaries.

Example:

```text
Number of evidence strata represented in a surface.
```

## Reshape

Change structural form without changing meaning.

Example:

```text
Assertion records reshaped into a table for review.
```

## Serialize

Convert source objects to a transport or storage format.

Example:

```text
Surface projection serialized as JSON.
```

## Index

Generate lookup structures.

Example:

```text
Participant-to-assertion index.
```

## Redact

Limit disclosed information according to policy.

Example:

```text
Reference-only projection for external review.
```

## Label

Attach human-readable labels without altering identity.

Example:

```text
Display gene symbol alongside Ensembl gene identifier.
```

## Visualize

Convert source structure into graphical form.

Example:

```text
Topology neighborhood rendered as a graph diagram.
```

Every transform must preserve source traceability.

---

# Projection Identity

Every projection should have projection identity.

Projection identity allows VDB to refer to the view, reconstruct the view, audit the view, and distinguish one view from another.

Projection identity must remain separate from source identity.

```text
Source identity:
    assertion_id
    topology_relationship_id
    convergence_region_id
    surface_id

Projection identity:
    projection_id
```

Projection identity identifies the representation.

It does not replace the source.

---

# Projection Lineage

Every projection must preserve lineage to its source.

At minimum, a projection should declare:

* projection identity
* source layer
* source object identifiers
* source generation
* source build identity, where applicable
* projection purpose
* projection transform
* projection parameters
* projection consumer
* projection representation
* created_at or equivalent version marker

Projection lineage enables reconstruction.

A projection without source lineage is unsafe.

---

# Projection and Duplication

Projection requires a careful distinction between representational duplication and truth duplication.

## Representational Duplication

Representational duplication may be allowed.

A projection may copy labels, counts, summaries, serialized fields, or display-ready values for convenience.

Example:

```text
A dashboard projection displays gene symbol POLG and assertion count 7.
```

This is acceptable if the projection remains traceable to source assertions.

## Truth Duplication

Truth duplication is prohibited.

A projection must not become a second authoritative location for scientific evidence.

Invalid:

```text
A projection stores copied assertion content without preserving assertion_id or source lineage.
```

Invalid:

```text
A projection-derived summary becomes treated as the canonical evidence state.
```

The source truth remains upstream.

---

# Projection Safety Rules

Valid projections must follow these rules.

## Preserve Source Identity

A projection must preserve references to source objects.

## Preserve Source Layer

A projection must declare whether it derives from assertion, topology, geometry, surface, corpus, lineage, or another governed layer.

## Preserve Purpose

A projection must declare why it exists.

## Preserve Transform

A projection must declare how the view was generated.

## Preserve Reconstructability

A projection must be reconstructable from its declared sources and parameters.

## Preserve Epistemic Distinctions

A projection must not collapse observed, inferred, semantic-prior, validation, and reasoning-output evidence into one undifferentiated class.

## Preserve Evidence Strata

A projection must not homogenize evidence modalities or producer families.

## Preserve Provenance

A projection must not remove producer identity or source artifact lineage needed for audit.

## Preserve Authority Boundary

A projection must not become canonical truth.

## Preserve Non-Interpretation

A projection must not make biological, clinical, statistical, causal, or mechanistic claims unless those claims are themselves preserved source assertions and clearly attributed.

---

# Invalid Projection Patterns

The following projection patterns are unsafe.

## Duplicate Truth Projection

A projection copies assertion content but loses or omits source assertion identity.

This creates a second truth location.

## Flattened Evidence Projection

A projection merges raw variants, semantic priors, proteomics evidence, validation assertions, and reasoning outputs into a single unlabeled support class.

This collapses evidence strata.

## Interpretive Projection

A projection labels a participant, surface, region, or assertion as causal, pathogenic, clinically actionable, significant, or biologically meaningful without that claim being a preserved source assertion.

This violates VDB's epistemic boundary.

## Untraceable Export Projection

An exported projection lacks source layer, surface generation, assertion corpus identity, or lineage references.

This prevents downstream audit and reconstruction.

## Visualization Authority Drift

A figure, dashboard, or rendered network becomes treated as the authoritative source.

Visual projections are aids.

They are not truth.

## Materialized Authority Drift

A cached or materialized projection becomes treated as canonical because it is easier to access than the source layer.

Performance convenience must not create authority transfer.

## Unlabeled Aggregation

A projection aggregates counts, scores, or summaries without preserving how the aggregation was generated.

Unlabeled aggregation risks semantic collapse.

---

# Projection and Downstream Reasoning

Projections may serve downstream reasoning systems.

For example, VDB may generate an export projection from an Evidence Convergence Surface for RDGP.

This projection may be packaged as a TEP-VDB transport artifact.

The projection may support reasoning.

It must not perform reasoning.

```text
Projection
        ↓
Downstream reasoning
        ↓
Reasoning assertions
        ↓
VDB preservation
```

If a downstream reasoning system returns outputs, those outputs must re-enter VDB as new Assertion Records.

They must not modify the projection that served as input.

They must not modify the source surface.

They must not modify the original assertions.

---

# Projection and Evidence Convergence Surfaces

Evidence Convergence Surfaces and projections are related but distinct.

An Evidence Convergence Surface is a governed exposure object over Convergence Geometry.

A surface projection is a view over that surface.

```text
Evidence Convergence Surface
        persistent governed exposure object

Surface Projection
        purpose-bound representation of that surface
```

For example:

```text
surface_POLG_primary_0001
        persistent surface

projection_POLG_primary_rdgp_export_0001
        RDGP export projection derived from the surface
```

The projection may be serialized, filtered, summarized, or packaged.

The source surface remains the governed exposure object.

---

# Projection and TEP-VDB

TEP-VDB packages may be understood as export projections.

A TEP-VDB package is a transport artifact generated for downstream consumption.

It may include:

* source surface identity
* surface generation
* assertion corpus identity
* evidence strata
* topology lineage
* geometry lineage
* assertion lineage
* disclosure context
* refresh context

But the TEP-VDB package is not the source truth.

It is a projection of VDB evidence state for a declared consumer and purpose.

---

# Projection and Historical Reproducibility

Projections should be generation-aware.

A projection generated from a specific VDB generation remains historically valid for that generation.

Later VDB generations may produce different projections because the evidence corpus, topology, geometry, surfaces, rules, or disclosure policies have changed.

This does not invalidate the earlier projection.

It records that the earlier projection belongs to an earlier state.

Projections should therefore preserve:

* source generation
* projection generation
* source build identity
* transform identity
* transform parameters
* projection creation time or version marker

Historical reproducibility allows future users to reconstruct what VDB exposed, exported, or visualized at a given time.

---

# Projection and Controlled Lossiness

Some projections may intentionally omit detail.

For example:

* a dashboard may show counts rather than full Assertion Records
* an export may disclose reference-only lineage
* a figure may show simplified labels
* a validation report may summarize missing fields

Controlled lossiness is allowed only when:

* the projection declares its purpose
* the projection declares its disclosure or transform basis
* omitted information remains reconstructable from source objects
* the projection does not pretend to be complete source truth

Lossy projection is acceptable.

Unlabeled semantic loss is not.

---

# Relationship to Future Mathematical Views

VDB must remain open to future mathematical projection forms.

Future projections may include:

* graph projections
* hypergraph projections
* simplicial complex projections
* tensor projections
* topological summaries
* manifold representations
* embedding spaces
* probabilistic views
* temporal evolution views
* unknown future mathematical representations

These representations may be powerful.

They do not become truth.

A future mathematical projection must still declare:

* source layer
* source objects
* transform
* purpose
* parameters
* generation
* lineage
* limitations

Mathematical sophistication does not confer authority.

---

# Projection Doctrine

Epoch IV can be summarized by the following principles.

## One Truth, Many Views

VDB preserves one evidence substrate.

It may generate many views over that substrate.

## Views Are Derived

Every projection is derived from preserved assertions or governed derived layers.

## Views Are Purpose-Bound

Every projection exists for a declared use case.

## Views Are Reconstructable

Every projection must be reproducible from its source.

## Views Are Non-Authoritative

A projection does not become source truth.

## Views Preserve Identity

Projection identity is separate from evidence identity.

## Views Preserve Semantics

Projection convenience must not collapse provenance, epistemic status, evidence strata, participant roles, or source identity.

## Views Do Not Interpret

Projection does not create biological, clinical, statistical, causal, or mechanistic conclusions.

---

# Summary

The Projection Layer allows VDB to generate many useful views from one preserved truth substrate.

Assertions remain the primitive scientific evidence.

Topology, geometry, and surfaces remain governed derived layers.

Projections are purpose-bound representations over those sources.

They may support query, audit, export, visualization, validation, review, interoperability, and downstream reasoning.

They must not create duplicate truth.

The central invariant of Epoch IV is:

```text
Projection is view generation, not evidence generation.
```

A projection may change representation.

It may change accessibility.

It may change format.

It may change consumer usability.

It must not change authority.

In this way, one preserved truth can generate many useful views without duplication.

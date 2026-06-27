# Evidence Convergence Surface Specification

## Epoch III: Discovery Layer

| Epoch | Epoch Identity      | Epoch Purpose                                                                                       |
| ----- | ------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer         | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry   | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | **Discovery Layer** | **How do preserved evidence topologies become discoverable?**                                       |
| IV    | Projection Layer    | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer     | Why do we do this?                                                                                  |

---

## Specification Status

This document defines implementation requirements for Evidence Convergence Surfaces.

It is downstream of:

* `docs/design/evidence_convergence_surface_model.md`
* `docs/design/convergence_geometry_model.md`
* `docs/implementation/specifications/convergence_geometry_spec.md`
* `docs/design/evidence_topology_model.md`
* `docs/implementation/specifications/evidence_topology_spec.md`
* `docs/design/assertion_record_and_projection_model.md`
* `docs/implementation/specifications/assertion_record_spec.md`

It is upstream of:

* `docs/implementation/schemas/evidence_convergence_surface_schema.md`

---

# Purpose

The Evidence Convergence Surface model defines surfaces as governed exposure layers over Convergence Geometry.

This specification defines the obligations that any valid Evidence Convergence Surface implementation must satisfy.

A valid implementation must expose geometry-derived reasoning capacity while preserving:

* traceability
* provenance
* evidence strata
* generation history
* reasoning currency
* refresh state
* epistemic boundaries

Evidence Convergence Surfaces must not perform reasoning, interpretation, prioritization, or biological conclusion formation.

---

# Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used normatively.

* **MUST** indicates a required implementation obligation.
* **MUST NOT** indicates a prohibited behavior.
* **SHOULD** indicates a strongly recommended behavior.
* **MAY** indicates an allowed but optional behavior.

---

# Governing Requirement

A valid Evidence Convergence Surface implementation **MUST** expose only geometry-derived, structurally eligible, disclosure-governed, traceable, generation-aware reasoning capacity.

It **MUST NOT** perform biological, statistical, clinical, causal, or mechanistic interpretation.

The governing implementation invariant is:

```text
Evidence Convergence Surfaces expose.
They do not reason.
```

---

# Dependency Chain

Evidence Convergence Surfaces **MUST** respect the established VDB dependency chain.

```text
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Downstream Statistical Reasoning
```

A surface **MUST** be derived from Convergence Geometry.

A surface **MUST NOT** bypass Convergence Geometry by being constructed directly from Assertion Records or Evidence Topology.

A surface **MAY** expose lineage to Assertion Records and Evidence Topology, but that lineage exposure does not make Assertion Records or Evidence Topology direct construction inputs for the surface layer.

---

# Scope

This specification governs:

* Evidence Convergence Surface construction
* surface eligibility
* surface disclosure
* surface identity
* surface traceability
* evidence strata preservation
* composite surface behavior
* surface generation tracking
* reasoning-informed surface behavior
* reasoning currency
* refresh triggers
* outbound TEP-VDB surface packaging
* validation requirements
* prohibited interpretive behavior

---

# Out of Scope

This specification does not govern:

* RDGP internal reasoning methods
* downstream statistical models
* downstream biological interpretation
* downstream clinical interpretation
* hypothesis ranking
* pathogenicity assessment
* causal inference
* therapeutic recommendation
* publication claims
* human expert review procedures

Downstream systems may reason over surfaces.

VDB surfaces themselves must not reason.

---

# Required Inputs

A valid Evidence Convergence Surface implementation **MUST** derive surfaces from one or more Convergence Geometry objects.

Required upstream inputs include:

* Convergence Geometry build identity
* Convergence Region identity
* region bounding basis
* Geometry Features, where applicable
* Structural Motifs, where applicable
* Convergence Profiles, where applicable
* source topology relationship lineage
* source assertion lineage
* upstream build metadata

A surface implementation **MUST** preserve enough upstream identity to reconstruct the path:

```text
Surface
    ↓
Convergence Geometry
    ↓
Evidence Topology
    ↓
Assertion Records
    ↓
Producer TEPs / source artifacts
```

---

# Surface Construction Requirements

## Geometry-Derived Construction

Every Evidence Convergence Surface **MUST** be constructed from Convergence Geometry.

A surface implementation **MUST** identify the Convergence Region or regions from which the surface is exposed.

A surface implementation **MUST** identify the geometry build from which the surface is derived.

A surface implementation **MUST NOT** create surfaces from uncharacterized topology alone.

A surface implementation **MUST NOT** create surfaces directly from raw producer assertions.

## Deterministic Construction

Surface construction **MUST** be deterministic.

Given the same:

* input Convergence Geometry
* surface eligibility rules
* surface disclosure rules
* build parameters
* implementation version

the implementation **MUST** produce equivalent surfaces.

Equivalent surfaces do not need to be byte-identical across storage backends, but they must preserve the same semantic content, lineage, eligibility basis, disclosure basis, and reasoning currency state.

## Reconstructability

Every generated surface **MUST** be reconstructable from its declared inputs, build metadata, eligibility basis, and disclosure basis.

A surface that cannot be reconstructed or traced to upstream geometry is invalid.

---

# Surface Eligibility Requirements

Every Evidence Convergence Surface **MUST** declare a surface eligibility basis.

The surface eligibility basis answers:

> Why may this Convergence Geometry become an exposed surface?

Eligibility **MUST** be structural.

Eligibility **MUST NOT** be biological, clinical, statistical, or interpretive.

Allowed classes of surface eligibility include, but are not limited to:

* cross-producer geometry
* multi-modal geometry
* independent-evidence geometry
* epistemic-diversity geometry
* temporal-persistence geometry
* multi-component geometry
* reasoning-reentry geometry
* audit-requested geometry
* refresh-required geometry

Forbidden eligibility concepts include:

* important
* interesting
* significant
* promising
* causal
* pathogenic
* actionable
* clinically relevant
* biologically meaningful

A surface **MUST NOT** be generated because VDB considers a region biologically important.

A surface **MAY** be generated because a region satisfies a deterministic structural exposure rule.

---

# Surface Disclosure Requirements

Every Evidence Convergence Surface **MUST** declare a surface disclosure basis.

The surface disclosure basis answers:

> Why are these specific evidence elements exposed to the downstream consumer?

Disclosure basis **MUST** be distinct from eligibility basis.

Eligibility governs whether a surface may exist.

Disclosure governs what the surface exposes.

Allowed classes of disclosure basis include, but are not limited to:

* minimum reasoning context
* assertion lineage required
* topology lineage required
* geometry feature required
* provenance audit required
* epistemic status required
* independence context required
* temporal context required
* reasoning currency required
* refresh context required
* consumer contract required

A surface implementation **MUST NOT** expose arbitrary VDB internal state without a declared disclosure basis.

A surface implementation **MUST NOT** omit lineage, provenance, or epistemic context required for downstream audit.

---

# Governed Disclosure Requirements

An Evidence Convergence Surface functions as a governed disclosure contract.

A valid surface implementation **MUST** expose enough information for downstream reasoning systems to understand what they are reasoning over.

A valid surface implementation **MUST** expose enough lineage for audit and reconstruction.

A valid surface implementation **MUST NOT** expose VDB internals merely because they are available.

A valid surface implementation **MUST NOT** flatten provenance for convenience.

A valid surface implementation **MUST NOT** editorialize disclosed content.

---

# Traceability Requirements

Every Evidence Convergence Surface **MUST** be traceable to its upstream derivation chain.

A valid implementation **MUST** preserve references to:

* source Convergence Geometry build
* source Convergence Region or regions
* contributing Geometry Features, where applicable
* contributing Structural Motifs, where applicable
* contributing Convergence Profiles, where applicable
* source Evidence Topology relationships
* source Assertion Records
* source producer identities
* source TEPs or producer artifacts, where available

A surface **MUST NOT** expose summarized evidence without preserving a reconstruction path to the underlying assertions.

Traceability may be exposed directly or through resolvable lineage references, but it **MUST** remain available.

---

# Evidence Strata Requirements

Evidence Convergence Surfaces **MUST** preserve evidence stratum identity.

An evidence stratum is a preserved class of evidence distinguished by producer, modality, epistemic status, and derivation class.

Examples of evidence strata include:

* raw variant observation stratum
* semantic prior stratum
* transcriptomic observation stratum
* proteomic observation stratum
* clinical observation stratum
* reasoning-output stratum
* validation stratum

A surface **MAY** expose multiple evidence strata.

A surface **MUST NOT** homogenize distinct evidence strata into a single undifferentiated evidence class.

A composite surface **MUST** preserve the distinction between raw observations, semantic priors, downstream reasoning outputs, validation assertions, and other evidence classes.

A surface **MAY** expose that multiple evidence strata intersect structurally.

A surface **MUST NOT** claim that one stratum confirms, validates, outweighs, or biologically explains another stratum.

---

# Composite Surface Requirements

A composite surface exposes more than one evidence stratum.

Composite surfaces **MUST** declare their contributing strata.

Composite surfaces **MUST** preserve stratum-specific provenance.

Composite surfaces **MUST** preserve stratum-specific epistemic status.

Composite surfaces **MUST** preserve stratum-specific derivation class.

Composite surfaces **MUST NOT** collapse raw and reasoning-informed evidence into equivalent support.

Composite surfaces **MAY** expose cross-modal or reasoning-informed convergence as structural organization.

Composite surfaces **MUST NOT** interpret that convergence.

---

# Surface Generation Requirements

Every Evidence Convergence Surface **MUST** be generation-aware.

A surface generation identifies the VDB evidentiary state from which a surface was produced.

A valid implementation **MUST** preserve:

* surface generation identity
* input VDB evidence state
* input assertion corpus identity
* input topology build identity
* input geometry build identity
* surface build metadata
* surface build timestamp or equivalent temporal marker

Earlier surface generations **MUST** remain historically valid relative to the evidence state from which they were generated.

Later surface generations **MUST NOT** rewrite earlier surface generations.

A surface implementation **MUST** support append-only surface history.

---

# Historical Validity

A surface generated from a prior evidence state is not invalid merely because VDB later ingests new evidence.

It remains valid for its original generation.

However, its reasoning currency may change relative to the current evidence state.

Implementations **MUST** distinguish historical validity from current reasoning currency.

A historically valid surface may be reasoning-stale.

---

# Reasoning-Informed Surface Requirements

A reasoning-informed surface is a surface whose exposed geometry includes preserved downstream reasoning assertions.

A reasoning-informed surface **MUST** preserve:

* reasoning producer identity
* reasoning producer version, where available
* reasoning method identity
* reasoning method version
* reasoning run identity
* reasoning input surface identity
* reasoning input surface generation
* reasoning input assertion corpus identity
* reasoning input VDB generation
* reasoning output assertion identity
* reasoning output provenance
* reasoning epistemic status
* reasoning confidence or support metadata, where available

A reasoning-informed surface **MUST NOT** adopt downstream reasoning conclusions as VDB conclusions.

VDB may expose:

```text
RDGP assertion A exists with confidence metadata C under method M.
```

VDB must not claim:

```text
RDGP assertion A is biologically true.
```

---

# Reasoning Re-Entry Requirements

Downstream reasoning outputs may re-enter VDB as producer assertions.

When this occurs, they **MUST** be preserved as new Assertion Records.

They **MUST NOT** modify the surfaces, topology relationships, geometry regions, or Assertion Records that served as their inputs.

They **MAY** participate in future topology construction, geometry characterization, and surface exposure.

Reasoning re-entry **MUST** be monotonic.

The valid flow is:

```text
Surface
        ↓
Downstream reasoning
        ↓
New reasoning assertion
        ↓
VDB preservation
        ↓
Future topology / geometry / surface
```

The invalid flow is:

```text
Surface
        ↓
Downstream reasoning
        ↓
Modify prior VDB evidence
```

---

# Reasoning Currency Requirements

Reasoning-informed surfaces **MUST** preserve reasoning currency.

Reasoning currency answers:

> Is the reasoning associated with this surface current relative to the relevant evidence corpus and declared reasoning method?

A valid implementation **MUST** determine reasoning currency from metadata.

Reasoning currency **MUST NOT** be determined from biological interpretation.

Reasoning currency **MUST** consider at least:

* current relevant raw assertion corpus
* assertion corpus used as reasoning input
* current declared reasoning method
* reasoning method used to generate existing reasoning assertions
* current declared reasoning producer version, where applicable
* reasoning producer version used to generate existing reasoning assertions, where applicable

A reasoning-informed surface **MUST** expose or preserve its reasoning currency state.

---

# Reasoning Currency States

A valid implementation **SHOULD** support reasoning currency states sufficient to distinguish:

* raw-only surface
* reasoning-current surface
* reasoning-stale due to new evidence
* reasoning-stale due to method update
* reasoning-stale due to both new evidence and method update
* refresh candidate
* refresh completed

Exact state names may vary by implementation, but the semantic distinctions **MUST** be preserved.

A surface **MUST NOT** present stale reasoning as current.

---

# Evidence-Triggered Refresh Requirements

An evidence-triggered refresh occurs when new relevant raw producer assertions enter VDB after a reasoning-informed surface was generated.

Examples include:

* new proteomics assertions
* new transcriptomics assertions
* new clinical assertions
* new imaging assertions
* new environmental assertions
* new literature-derived assertions
* new variant assertions
* new semantic prior assertions

When new relevant raw evidence enters VDB, an implementation **MUST** be able to determine whether existing reasoning-informed surfaces were generated against an earlier raw assertion corpus.

If prior reasoning did not include the newly ingested relevant evidence, the implementation **MUST** mark reasoning currency as stale or refresh-warranted.

The implementation **MUST NOT** infer that the new evidence changes the biological conclusion.

It may only infer that the reasoning input corpus is no longer current.

---

# Reasoning-Method-Triggered Refresh Requirements

A reasoning-method-triggered refresh occurs when the declared downstream reasoning method changes after reasoning-informed surfaces were generated.

Examples include changes to:

* model version
* statistical method
* inference framework
* calibration scheme
* null model
* evidence weighting strategy
* validation regime
* reasoning producer version

An implementation **MUST** be able to determine whether existing reasoning-informed surfaces were generated under an earlier declared reasoning method.

If the current declared reasoning method differs from the method used to generate existing reasoning assertions, the implementation **SHOULD** mark affected surfaces as refresh-warranted.

The implementation **MUST NOT** claim that the newer method is biologically superior unless such a claim itself enters VDB as a preserved assertion from an authorized producer.

---

# Refresh Trigger Requirements

A valid implementation **SHOULD** preserve the reason a refresh is warranted.

Refresh trigger classes include:

* new relevant raw evidence
* reasoning method update
* reasoning producer version update
* disclosure contract update
* eligibility rule update
* operator-requested audit
* both evidence and method update

Refresh triggers **MUST** be metadata-derived.

Refresh triggers **MUST NOT** be meaning-derived.

The central rule is:

```text
Surface currency is metadata-derived, not meaning-derived.
```

---

# Refresh Workflow Requirements

A refresh is the process by which VDB emits an updated reasoning-capacity package to a downstream reasoning system and later ingests refreshed reasoning assertions.

The expected refresh flow is:

```text
Current VDB evidence state
        ↓
TEP-VDB refresh package
        ↓
Downstream reasoning system
        ↓
TEP-reasoning output
        ↓
VDB ingestion
        ↓
Updated reasoning-informed surfaces
```

VDB **MAY** identify refresh as warranted.

VDB **MAY** generate a refresh candidate package.

VDB **MAY** expose refresh status to an operator.

VDB **MAY** ingest refreshed reasoning outputs.

VDB **MUST NOT** perform the downstream reasoning itself.

VDB **MUST NOT** overwrite earlier reasoning-informed surfaces during refresh.

---

# Operator Visibility Requirements

Refresh state **SHOULD** be operator-visible.

An implementation **SHOULD** be able to report:

* affected surfaces
* current reasoning currency state
* refresh trigger
* prior reasoning input corpus
* current relevant evidence corpus
* prior reasoning method
* current declared reasoning method
* recommended outbound refresh package, where applicable

Operator warnings **MUST** be phrased as refresh or currency notices.

They **MUST NOT** be phrased as biological conclusions.

Acceptable:

```text
Refresh warranted: new relevant raw assertions entered after prior reasoning.
```

Not acceptable:

```text
New evidence changes the biological conclusion.
```

---

# Outbound TEP-VDB Package Requirements

When VDB emits an outbound package for downstream reasoning, the package **SHOULD** preserve surface identity and context.

An outbound TEP-VDB package **SHOULD** include:

* surface identity
* surface generation
* surface eligibility basis
* surface disclosure basis
* surface evidence strata
* input assertion corpus identity
* source geometry lineage
* source topology lineage
* source assertion lineage
* provenance context
* epistemic context
* independence context
* temporal context
* reasoning currency state, where applicable
* refresh trigger, where applicable
* consumer contract identity, where applicable

A refresh package **SHOULD** identify why it was generated.

A refresh package **MUST NOT** imply that VDB has interpreted the exposed evidence.

---

# Surface Ordering and Ranking Requirements

Surface ordering **MAY** be implemented for deterministic retrieval, auditing, pagination, or operator review.

Allowed ordering concepts include:

* build time
* surface generation
* surface class
* deterministic identifier
* region size
* feature count
* refresh state
* audit state

Surface ordering **MUST NOT** be represented as biological priority, clinical priority, statistical significance, pathogenicity likelihood, or mechanistic importance.

A valid implementation **MUST NOT** rank surfaces by inferred biological relevance unless such ranking is produced by an external reasoning system and re-enters VDB as a preserved assertion.

---

# Surface Classes

A valid implementation **MAY** distinguish surface classes.

Recommended conceptual classes include:

* primary convergence surface
* mixed-modality surface
* reasoning-informed surface
* re-entry surface
* audit surface
* refresh candidate surface

Surface class **MUST** describe exposure type.

Surface class **MUST NOT** imply biological significance.

---

# Disclosure Contract Requirements

A surface implementation **SHOULD** support consumer-specific disclosure contracts.

A disclosure contract may determine:

* which strata are included
* which lineage depth is exposed
* which provenance summaries are included
* whether full assertion references or summaries are exposed
* whether reasoning currency is exposed
* whether refresh metadata is exposed

Disclosure contracts **MUST NOT** alter underlying evidence identity.

Disclosure contracts **MUST NOT** rewrite lineage.

Disclosure contracts **MUST NOT** change epistemic status.

Disclosure contracts **MUST** preserve reconstructability.

---

# Reproducibility Requirements

A valid implementation **MUST** support reproducible investigation.

Given the same:

* VDB evidence generation
* input assertion corpus
* topology build
* geometry build
* surface eligibility rules
* surface disclosure rules
* surface build parameters
* implementation version

the same Evidence Convergence Surfaces **MUST** be reconstructable.

A surface generated in one VDB generation **MUST** remain reproducible even after later evidence generations are added.

---

# Non-Interpretation Requirements

Evidence Convergence Surfaces **MUST NOT** claim:

* biological causality
* disease mechanism
* pathogenicity
* statistical significance
* clinical actionability
* therapeutic relevance
* hypothesis confirmation
* biological correctness
* clinical priority
* mechanistic explanation
* diagnostic relevance

Evidence Convergence Surfaces **MAY** claim:

* geometry-derived exposure
* structural eligibility
* disclosure basis
* traceability
* evidence strata composition
* surface generation
* reasoning currency state
* refresh status
* deterministic reasoning capacity

---

# Invalid Surface Conditions

A surface is invalid if it:

* lacks source Convergence Geometry
* bypasses Convergence Geometry
* lacks surface eligibility basis
* lacks surface disclosure basis
* lacks traceability to upstream geometry
* lacks lineage to topology and assertions
* collapses distinct evidence strata
* presents stale reasoning as current
* modifies prior assertions
* modifies prior surfaces during refresh
* claims biological meaning
* claims statistical support generated by VDB
* omits reasoning provenance for reasoning-informed content
* omits input corpus identity for reasoning-informed content
* omits method identity for reasoning-informed content
* cannot be reconstructed from declared inputs

---

# Validation Requirements

A valid implementation **SHOULD** provide validation checks for:

* geometry lineage presence
* topology lineage presence
* assertion lineage presence
* surface eligibility basis presence
* surface disclosure basis presence
* evidence strata preservation
* surface generation consistency
* reasoning currency consistency
* refresh trigger consistency
* disclosure contract consistency
* absence of forbidden interpretive claims

Validation failures **SHOULD** distinguish between:

* structural invalidity
* missing lineage
* stale reasoning
* incomplete disclosure
* forbidden interpretation
* unreconstructable surface

Stale reasoning is not necessarily structural invalidity.

It is a currency state that must be explicitly represented.

---

# Relationship to RDGP

RDGP is the initial downstream reasoning system expected to consume Evidence Convergence Surfaces.

VDB provides RDGP with:

* structurally eligible surfaces
* governed disclosure context
* evidence strata
* geometry lineage
* topology lineage
* assertion lineage
* provenance context
* epistemic context
* reasoning currency metadata
* refresh context

RDGP may return:

* statistical reasoning assertions
* prioritization assertions
* confidence or support metadata
* model-specific outputs
* reasoning provenance

When RDGP outputs re-enter VDB, they **MUST** be preserved as new Assertion Records.

VDB **MUST NOT** treat RDGP outputs as VDB conclusions.

---

# Relationship to Future Reasoning Systems

This specification is not RDGP-specific.

Any future reasoning system that consumes Evidence Convergence Surfaces and returns outputs to VDB **MUST** re-enter through preserved assertions.

Future reasoning systems may include:

* Bayesian reasoning engines
* enrichment engines
* causal reasoning engines
* graph reasoning engines
* topological reasoning engines
* machine learning systems
* clinical decision-support systems
* future mathematical frameworks

VDB **MUST** preserve reasoning system identity, method identity, method version, input surface lineage, and output assertion provenance for any such system.

---

# Implementation Independence

This specification does not require a particular storage backend, query system, graph engine, mathematical representation, or serialization format.

Valid implementations may use:

* relational storage
* document storage
* graph projections
* hypergraph projections
* columnar stores
* object stores
* versioned files
* future storage or projection systems

The representation may vary.

The preservation obligations do not.

---

# Summary

A valid Evidence Convergence Surface implementation exposes structurally eligible Convergence Geometry as governed, traceable, generation-aware reasoning capacity.

It must preserve:

* eligibility basis
* disclosure basis
* geometry lineage
* topology lineage
* assertion lineage
* evidence strata
* surface generation
* reasoning provenance
* reasoning currency
* refresh state

It must not perform:

* biological interpretation
* statistical reasoning
* clinical reasoning
* causal inference
* prioritization
* hypothesis confirmation

Evidence Convergence Surfaces are the Discovery Layer of VDB only in the sense that they make preserved evidence geometry discoverable.

They expose opportunity.

They do not determine meaning.

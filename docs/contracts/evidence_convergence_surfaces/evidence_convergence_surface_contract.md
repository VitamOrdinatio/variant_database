# Evidence Convergence Surface Contract

## Purpose

This document defines the VDB contract for Evidence Convergence Surfaces.

An Evidence Convergence Surface is a governed exposure object over Convergence Geometry.

Evidence Convergence Surfaces expose structurally eligible, lineage-preserved, policy-governed regions of Convergence Geometry so that Projection Views and downstream reasoning systems can consume evidence structure without converting exposure, eligibility, or structural richness into biological confidence.

This contract ensures that Evidence Convergence Surfaces remain:

```text
geometry-derived
policy-governed
surface-explicit
membership-explicit
eligibility-explicit
disclosure-explicit
lineage-preserving
generation-aware
currency-aware
consumer-aware when applicable
projection-neutral
non-interpretive
reconstructable
```

Evidence Convergence Surfaces govern exposure.

They do not interpret biological meaning.

---

# Scope

This contract applies to all VDB Evidence Convergence Surface builds, surfaces, and surface membership records, including:

```text
local synthetic surfaces
small integration-test surfaces
MARK corpus surfaces
future multi-producer surfaces
future multi-cohort surfaces
future multi-modal surfaces
future RDGP-facing surfaces
future validation-facing surfaces
future query-facing surfaces
future release surfaces
future external-capsule surfaces
future reasoning-informed surfaces
future consumer-specific exposure surfaces
```

This contract governs the logical requirements of Evidence Convergence Surfaces.

It does not prescribe a single physical storage representation, projection format, consumer format, or query interface.

Evidence Convergence Surfaces may be represented by:

```text
relational records
SQLite records
TSV records
JSON records
JSONL records
surface manifests
surface membership tables
surface eligibility reports
surface disclosure reports
surface lineage reports
lakehouse partitions
object-store metadata records
future storage backends
```

The representation is not the architecture.

The governed, reconstructable exposure of structurally eligible Convergence Geometry is the architecture.

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

This contract defines the obligations of the Evidence Convergence Surface layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Evidence Convergence Surface contract governs the transition from structurally characterized convergence geometry into governed evidence exposure.

An Evidence Convergence Surface answers:

```text
Which structurally characterized evidence regions are eligible for governed exposure,
under which policy,
for which purpose,
with which lineage,
at which generation?
```

An Evidence Convergence Surface does not answer:

```text
Which evidence is biologically explanatory?

Which gene is causal?

Which variant is pathogenic?

Which candidate should be prioritized?

Which exposed region is clinically actionable?

Which projection format should be emitted?

Which downstream reasoning conclusion should be accepted?
```

Those responsibilities belong to downstream reasoning systems, returned producer assertions, or the Projection View layer.

---

# Definition

An Evidence Convergence Surface is a governed exposure object over Convergence Geometry.

An Evidence Convergence Surface may expose selected Convergence Regions, Geometry Features, Structural Motifs, geometry profiles, or other geometry-derived records according to explicit eligibility and disclosure policies.

An Evidence Convergence Surface must preserve enough information to support:

```text
surface build reconstruction
input geometry reconstruction
input topology reconstruction
input Assertion Record reconstruction
input corpus reconstruction
surface identity reconstruction
surface membership reconstruction
eligibility basis reconstruction
disclosure basis reconstruction
withholding basis reconstruction when applicable
generation reconstruction
currency reconstruction
projection lineage
downstream consumer reconstruction
```

An Evidence Convergence Surface is governed exposure.

It is not source evidence.

It is not an Assertion Record.

It is not Evidence Topology.

It is not Convergence Geometry.

It is not a Projection View.

It is not a Query Surface.

It is not biological reasoning.

---

# Core Invariant

The architectural rule is:

```text
Convergence Geometry characterizes structure.

Evidence Convergence Surfaces govern exposure.

Evidence Convergence Surfaces do not interpret meaning.
```

The governing transition is:

```text
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection Views
```

This means:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent exposed or governed evidence for a purpose.
```

Convergence Geometry may generate the structurally rich haystack.

Evidence Convergence Surfaces expose governed regions of that haystack.

Projection Views package those regions.

Downstream reasoning systems may search for the biological needle.

---

# Surface Authority

Evidence Convergence Surfaces have exposure authority.

A surface is authoritative for:

```text
which geometry-derived regions were evaluated
which geometry-derived regions were eligible
which geometry-derived regions were exposed
which geometry-derived regions were withheld
which eligibility policy was used
which disclosure policy was used
which purpose governed the surface
which input geometry build was used
which generation context applied
which lineage was preserved
```

A surface is not authoritative for:

```text
producer source evidence
producer scientific claims
Assertion Record correctness
topology correctness beyond declared lineage
geometry correctness beyond declared input geometry
biological confidence
clinical interpretation
causality
pathogenicity
candidate prioritization
RDGP reasoning
```

Surface authority is narrow.

It governs exposure.

It does not create source authority.

---

# Representation And Consumer Neutrality

Evidence Convergence Surfaces must remain representation-neutral and consumer-neutral unless explicitly declared otherwise.

A surface may support many projection types, including:

```text
RDGP-facing projections
validation reports
developer inspection tables
query responses
dashboards
TEP-VDB exports
consumer-specific packages
future projection formats
```

A surface must not be defined by any one projection format.

A surface may be consumer-aware when its purpose requires consumer-specific exposure rules.

Consumer-aware surfaces must declare:

```text
target_consumer_class when applicable
consumer purpose
consumer readiness basis
consumer-specific eligibility policy when applicable
consumer-specific disclosure policy when applicable
```

Consumer awareness must not become biological interpretation.

Consumer readiness must not become biological correctness.

---

# Required Input Boundary

Evidence Convergence Surfaces must consume governed VDB sources.

The normal Phase 4 input chain is:

```text
Corpus Generation
        ↓
Assertion Record index
        ↓
Evidence Topology Build
        ↓
Convergence Geometry Build
        ↓
Evidence Convergence Surface Build
```

Evidence Convergence Surfaces must not directly parse raw producer artifacts when geometry-derived inputs are available.

Evidence Convergence Surfaces must not re-run ingestion.

Evidence Convergence Surfaces must not reconstruct Registration Units.

Evidence Convergence Surfaces must not bypass Assertion Record primacy.

Evidence Convergence Surfaces must not bypass Evidence Topology.

Evidence Convergence Surfaces must not bypass Convergence Geometry.

A surface build must declare:

```text
input_geometry_build_id
input_topology_build_id when available
input_corpus_generation_id
input_assertion_record_index_id when available
surface_policy_id
eligibility_policy_id
disclosure_policy_id
builder_name
builder_version when available
build_timestamp
schema or contract version when available
```

If a surface build uses a governed source other than a formal Convergence Geometry Build, that source must be explicitly declared and must preserve traceability to Assertion Records, Corpus Generations, Registration Units, topology, and geometry-equivalent records.

---

# Required Surface Build Identity

Every Evidence Convergence Surface Build must have a stable identity.

A Surface Build identity must preserve:

```text
surface_build_id
surface_build_label when available
input_geometry_build_id
input_topology_build_id when available
input_corpus_generation_id
input_assertion_record_index_id when available
surface_policy_id
surface_policy_version when available
eligibility_policy_id
eligibility_policy_version when available
disclosure_policy_id
disclosure_policy_version when available
builder_name
builder_version when available
build_timestamp
validation_status
certification_status when available
```

Surface Build identity must remain stable across projection generation, validation, certification, reconstruction, and downstream consumer use.

Human-readable labels may support inspection.

Labels must not replace stable Surface Build identity.

---

# Required Evidence Convergence Surface Identity

Every Evidence Convergence Surface must have a stable identity.

An Evidence Convergence Surface identity must preserve:

```text
surface_id
surface_label when available
surface_type
surface_purpose
surface_build_id
input_geometry_build_id
input_topology_build_id when available
input_corpus_generation_id
surface_generation_id when available
target_consumer_class when applicable
validation_status
certification_status when available
```

Surface types may include:

```text
general_convergence_surface
RDGP_facing_surface
validation_surface
developer_inspection_surface
release_surface
query_backed_surface
external_capsule_surface
future_consumer_surface
```

A surface identity must remain stable across projection generation, validation, certification, reconstruction, and downstream consumer use.

A surface label must not replace stable surface identity.

---

# Surface Membership Obligations

Surface Membership records declare whether geometry-derived records participate in a surface.

Surface Membership may evaluate or include:

```text
Convergence Regions
Geometry Features
Structural Motifs
geometry profiles
geometry summaries
topology-derived supporting structure
```

Every Surface Membership record must preserve:

```text
surface_membership_id
surface_id
surface_build_id
input_geometry_build_id
convergence_region_id when applicable
geometry_feature_ids when applicable
structural_motif_ids when applicable
source_topology_relationship_ids when applicable
source_assertion_ids when applicable
eligibility_status
disclosure_status
eligibility_basis
disclosure_basis
withholding_reason when applicable
validation_status
```

Surface Membership status may include:

`eligibility_status` with values of:

```text
eligible
ineligible
deferred
not_applicable
not_evaluated
```

and `disclosure_status` with values of:

```text
exposed
withheld
deferred
deprecated
superseded
not_applicable
not_evaluated
```

Membership must be explicit.

Surface Membership must not imply biological importance.

Surface Membership must not replace Convergence Regions, Geometry Features, Structural Motifs, topology relationships, or Assertion Records.

---

# Eligibility Basis Obligations

Every eligible or ineligible surface membership must declare an eligibility basis.

Eligibility basis may include:

```text
lineage completeness
geometry validation status
topology validation status
Assertion Record traceability
Corpus Generation traceability
Registration Unit traceability
producer-family visibility
evidence-domain visibility
uncertainty visibility
null-semantics visibility
namespace status visibility
generation context availability
currency metadata availability
surface purpose compatibility
consumer-readiness criteria
policy-declared structural criteria
reconstruction handle availability
```

Eligibility basis must be reconstructable from governed VDB records.

Eligibility basis must preserve the policy used to evaluate eligibility.

Eligibility basis must not be replaced by an opaque exposure score.

Eligibility means structurally and procedurally suitable for governed exposure.

Eligibility does not mean biologically correct.

Eligibility does not mean clinically actionable.

Eligibility does not mean explanatory.

---

# Disclosure Basis Obligations

Every exposed or withheld surface membership must declare a disclosure basis.

Disclosure basis may include:

```text
included by surface policy
withheld by surface policy
insufficient lineage
insufficient uncertainty visibility
insufficient namespace status visibility
unsupported consumer purpose
stale generation
superseded generation
incomplete reconstruction path
incomplete evidence strata
deferred for future review
not applicable to surface purpose
```

Disclosure basis must be reconstructable from governed VDB records or explicit surface policy.

Disclosure basis must not be replaced by an opaque disclosure flag.

Disclosure means a geometry-derived record is included in a governed surface.

Disclosure does not mean VDB endorses biological meaning.

Withholding does not mean the evidence is absent.

Withholding does not mean the evidence is negative.

---

# Evidence Strata And Lineage Obligations

Evidence Convergence Surfaces must preserve evidence strata and lineage sufficient for downstream projections and consumers to evaluate exposed structure.

A surface must preserve or expose references to:

```text
source Convergence Regions
source Geometry Features
source Structural Motifs when applicable
source Evidence Topology Build
source topology relationships
source Assertion Records
source Corpus Generation
source Registration Units
source producer families
source evidence domains
source namespaces
source uncertainty states
source null states when available
source evidence completeness status when available
source completeness scope when available
source absence basis when evidence absence is asserted
source omission basis when evidence is not exposed
source provenance records
```

A surface must preserve enough completeness context for downstream consumers to distinguish:

```text
evidence absent from the declared corpus
evidence present but withheld
evidence not evaluated
evidence unresolved
evidence conflicting
producer-declared negative evidence
```

Evidence completeness must remain scoped.

A completeness statement must declare what corpus, surface, evidence domain, modality, producer family, participant set, or projection purpose it applies to when that scope is relevant.

A surface must not collapse independent evidence strata.

A surface must not collapse producer identity.

A surface must not collapse modality or evidence-domain identity.

A surface must not collapse uncertainty or null semantics.

A surface must not hide namespace mediation, ambiguity, conflict, or unresolved identity states.

---

# Generation And Currency Obligations

Evidence Convergence Surfaces must preserve generation and currency context.

Surface records should preserve:

```text
surface_generation_id when available
input_geometry_generation when available
input_topology_generation when available
input_corpus_generation_id
input_assertion_generation when available
build_timestamp
surface_policy_version
eligibility_policy_version when available
disclosure_policy_version when available
refresh_status when available
staleness_status when applicable
supersession_status when applicable
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

Surface generation must not overwrite earlier surface generations.

A newer surface must not erase reconstructability of an older surface.

A stale surface must not silently masquerade as current.

A superseded surface must remain historically reconstructable when retained.

---

# Withholding And Lossiness Obligations

Evidence Convergence Surfaces may withhold or omit geometry-derived records according to policy.

When a region, feature, motif, or profile is withheld, the surface must preserve:

```text
withholding status
withholding reason
withholding policy reference when applicable
source geometry reference
source topology reference when applicable
source Assertion Record lineage when applicable
```

Withheld evidence must not be interpreted as absent evidence.

Ineligible evidence must not be interpreted as negative evidence.

Deferred evidence must not be interpreted as unsupported evidence.

If a surface is lossy, partial, filtered, consumer-specific, or policy-limited, that status must be explicit.

Surface lossiness must be preserved for downstream Projection Views.

---

# Relationship To Convergence Geometry

Convergence Geometry is the direct input to Evidence Convergence Surfaces.

Convergence Geometry answers:

```text
What structural properties emerge from connected evidence organization?
```

Evidence Convergence Surfaces answer:

```text
Which structurally characterized regions are eligible for governed exposure?
```

Evidence Convergence Surfaces must preserve traceability to source geometry records.

Evidence Convergence Surfaces must not modify Convergence Geometry.

Evidence Convergence Surfaces must not replace Convergence Geometry.

Evidence Convergence Surfaces must not treat geometry features as source evidence.

Evidence Convergence Surfaces must not treat structural richness as biological confidence.

---

# Relationship To Evidence Topology

Evidence Convergence Surfaces must preserve topology lineage through Convergence Geometry.

Surface records should preserve topology build references and topology relationship references when relevant to reconstruction, validation, projection, or downstream consumer use.

Evidence Convergence Surfaces must not modify Evidence Topology.

Evidence Convergence Surfaces must not replace Evidence Topology.

Evidence Convergence Surfaces must not treat topological connectedness as biological meaning.

---

# Relationship To Assertion Records

Assertion Records remain the primary preserved scientific claims.

Evidence Convergence Surfaces expose geometry-derived structure that remains traceable through topology to Assertion Records.

Surface records must preserve or expose Assertion Record lineage when relevant to reconstruction, validation, projection, or downstream consumer use.

Evidence Convergence Surfaces must not modify Assertion Records.

Evidence Convergence Surfaces must not replace Assertion Records.

Evidence Convergence Surfaces must not treat surface eligibility as producer evidence.

Evidence Convergence Surfaces must not treat surface disclosure as biological endorsement.

---

# Relationship To Corpus Generations And Registration Units

Corpus Generations provide the declared evidence scope from which topology, geometry, and surfaces are derived.

Registration Units provide the custody boundary for the producer packages selected by the Corpus Generation.

Every Evidence Convergence Surface Build must preserve:

```text
input_corpus_generation_id
input Registration Unit references when applicable
input Assertion Record source reference when available
input topology build reference when available
input geometry build reference
```

Evidence Convergence Surfaces must not expand corpus scope silently.

Evidence Convergence Surfaces must not include geometry records outside the declared input Geometry Build unless a new Geometry Build or explicitly versioned input scope is declared.

Evidence Convergence Surfaces must preserve Corpus Generation and Registration Unit lineage for downstream Projection Views, RDGP reasoning, and reconstruction.

---

# Relationship To Projection Views

Projection Views represent, render, package, export, summarize, or query governed VDB records for a purpose.

Evidence Convergence Surfaces provide governed exposure substrate for Projection Views.

The distinction is:

```text
Evidence Convergence Surface
    governs exposure of structurally eligible convergence substrate

Projection View
    represents governed evidence or exposed substrate for a purpose
```

One Evidence Convergence Surface may support multiple Projection Views.

A Projection View may render a surface as:

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

A Projection View over an Evidence Convergence Surface must declare:

```text
projection purpose
projection source layer
source surface_id
source surface_build_id
source surface_membership_ids when applicable
source geometry records
source topology records
source Assertion Record identities
source Corpus Generation identity
source Registration Unit identities when applicable
materialization status
lossiness status when applicable
reconstruction path
```

A Projection View does not replace an Evidence Convergence Surface.

A Projection View does not acquire surface authority.

An Evidence Convergence Surface must not be treated as a projection format.

---

# Relationship To Query Surfaces

An Evidence Convergence Surface is an architectural exposure object.

A Query Surface is an access interface or consumer-facing access surface over governed VDB records.

The distinction is:

```text
Evidence Convergence Surface
    governed exposed convergence substrate

Query Surface
    access pathway or interface over governed VDB layers
```

A Query Surface may expose an Evidence Convergence Surface.

A Query Surface may project, filter, or materialize surface content according to query and projection policy.

A Query Surface must not replace an Evidence Convergence Surface.

A Query Surface must not acquire surface authority.

A Query Surface must not obscure source authority, surface eligibility basis, disclosure basis, lineage, lossiness, or generation context.

---

# Relationship To RDGP Consumer Projections

RDGP-facing projections may consume Evidence Convergence Surfaces.

RDGP-facing surfaces and projections must preserve enough lineage for RDGP to evaluate:

```text
which convergence regions were exposed
which geometry features were available
which structural motifs were present when applicable
which topology relationships supported them
which Assertion Records participated
which Corpus Generation bounded the surface
which Registration Units contributed evidence
which producer families, modalities, and evidence domains were represented when available
which uncertainty states were present
which null states were present
which evidence completeness status applied when available
which completeness scope applied when available
which absence basis was used when evidence absence was asserted
which omission or withholding basis was used when evidence was not exposed
which namespace states were direct, mediated, ambiguous, conflicted, or unresolved
which generation or currency context applied
which reconstruction handles are available
which regions were withheld or omitted when relevant
```

An Evidence Convergence Surface may expose reasoning affordances.

It does not perform reasoning.

An Evidence Convergence Surface may help RDGP inspect a governed convergence substrate.

It does not decide which signal is biologically meaningful.

It does not determine whether evidence explains phenotype.

It does not generate RDGP prioritization.

---

# Validation Obligations

Evidence Convergence Surface validation must confirm:

```text
surface_build_id exists
input_geometry_build_id exists
input_topology_build_id is traceable when applicable
input_corpus_generation_id is traceable
input Assertion Record source is traceable
surface policy is declared
eligibility policy is declared
disclosure policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
surface identity is stable
surface purpose is declared
surface memberships are explicit
surface memberships trace to source geometry records
eligibility status is declared for evaluated memberships
disclosure status is declared for evaluated memberships
eligibility basis is declared
disclosure basis is declared
withholding reason is declared when applicable
source geometry lineage is reconstructable
source topology lineage is reconstructable
source Assertion Record lineage is reconstructable
source Corpus Generation lineage is reconstructable
source Registration Unit lineage is reconstructable when applicable
generation context is visible
currency context is visible when applicable
lossiness status is explicit when applicable
surface construction is deterministic under fixed inputs
surface does not modify Convergence Geometry
surface does not mutate Registration Units
surface does not expand Corpus Generation scope silently
surface does not become source evidence
surface does not become a projection
surface does not perform biological reasoning
surface does not convert structural eligibility into biological confidence
```

RDGP-facing surface validation should additionally confirm:

```text
producer-family strata are preserved
evidence-domain strata are preserved
uncertainty states are preserved
null semantics are preserved when available
namespace mediation status is preserved
generation and currency metadata are preserved
reconstruction handles are available
withholding and lossiness states are explicit when relevant
evidence completeness status is preserved when available
completeness scope is preserved when available
absence basis is explicit when evidence absence is asserted
omission or withholding basis is explicit when evidence is not exposed
```

Validation must confirm governed exposure and reconstructability.

Validation must not claim biological correctness.

---

# Anti-Collapse Rules

The following are prohibited:

```text
Convergence Geometry replaced by Evidence Convergence Surface
Geometry Feature replaced by surface membership
Convergence Region replaced by surface membership
Structural Motif replaced by surface membership
topology relationship replaced by surface membership
Assertion Record replaced by surface membership
surface eligibility treated as biological confidence
surface disclosure treated as biological endorsement
surface membership treated as source evidence
surface treated as source evidence
surface treated as biological truth
surface treated as clinical evidence
surface treated as Projection View
Projection View treated as Evidence Convergence Surface
Query Surface treated as Evidence Convergence Surface
withheld evidence treated as absent evidence
ineligible region treated as negative evidence
deferred evidence treated as unsupported evidence
consumer readiness treated as biological correctness
structural eligibility treated as clinical actionability
surface generation collapse
surface policy collapse
eligibility basis collapse
disclosure basis collapse
withholding basis collapse
lossiness collapse
producer-family collapse
evidence-domain collapse
modality collapse
uncertainty collapse
null-state collapse
namespace-state collapse
Corpus Generation scope collapse
Registration Unit boundary collapse
RDGP reasoning embedded inside surface
opaque surface score replacing eligibility basis
```

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

An Evidence Convergence Surface implementation is complete only when:

```text
Surface Build identity is stable
input Convergence Geometry Build is declared
input Corpus Generation is declared
surface policy is declared
eligibility policy is declared
disclosure policy is declared
builder identity is declared
surface identity is stable
surface purpose is declared
surface memberships are explicit when emitted
surface memberships trace to geometry records
eligibility status is declared for evaluated memberships
disclosure status is declared for evaluated memberships
eligibility basis is reconstructable
disclosure basis is reconstructable
withholding reason is declared when applicable
surface records trace to Convergence Geometry
surface records trace through geometry to Evidence Topology
surface records trace through topology to Assertion Records
surface records trace to Corpus Generation
surface records trace to Registration Units when applicable
generation context is preserved
currency context is preserved when applicable
lossiness status is explicit when applicable
surface can serve as input to Projection Views
surface does not become source evidence
surface does not become a projection
surface does not perform biological reasoning
surface remains representation-neutral
anti-collapse validation passes
```

An Evidence Convergence Surface implementation is not complete merely because a table, manifest, export, dashboard, query response, report, or package exists.

An Evidence Convergence Surface implementation is complete only when those records satisfy this contract.

---

# Summary

An Evidence Convergence Surface is a governed exposure object over Convergence Geometry.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.

Convergence Geometry characterizes organization.

Evidence Convergence Surfaces govern exposure.

Projection Views represent exposed or governed evidence for a purpose.
```

Evidence Convergence Surfaces expose governed structure without interpreting meaning.

They make structurally eligible convergence substrate available for projections and downstream reasoning.

They do not identify biological truth.

They do not confer biological confidence.

The guiding rule is:

```text
Consume geometry.

Evaluate eligibility.

Declare disclosure.

Preserve lineage.

Expose governed structure.

Remain projection-neutral.

Never convert exposure into interpretation.
```

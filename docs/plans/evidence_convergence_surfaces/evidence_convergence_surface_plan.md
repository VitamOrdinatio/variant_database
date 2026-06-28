# Evidence Convergence Surface Implementation Plan

## Purpose

This document defines the implementation plan for Evidence Convergence Surface construction in VDB Phase 4.

An Evidence Convergence Surface is a governed exposure object over Convergence Geometry.

This plan describes how VDB will consume a governed Convergence Geometry Build, apply explicit surface, eligibility, and disclosure policies, evaluate geometry-derived records for governed exposure, preserve membership state, preserve withholding and lossiness semantics, preserve generation and currency context, validate reconstructability, and provide downstream input to Projection Views.

The Phase 4 Evidence Convergence Surface implementation goal is:

```text
Deterministically construct governed exposure surfaces over Convergence
Geometry while preserving eligibility basis, disclosure basis, withholding
semantics, lineage, generation, currency, lossiness, and consumer-awareness
boundaries without converting exposure into biological interpretation.
```

Evidence Convergence Surfaces govern exposure.

Evidence Convergence Surfaces do not interpret biological meaning.

Convergence Geometry builds the structurally rich haystack.

Evidence Convergence Surfaces decide which parts of the haystack are governed for exposure.

Projection Views package exposed substrate.

Downstream reasoning systems may search for the biological needle.

---

# Contract Reference

This plan implements the obligations defined in:

```text
docs/contracts/evidence_convergence_surfaces/evidence_convergence_surface_contract.md
```

The governing contract states that Evidence Convergence Surfaces must remain:

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

This plan is subordinate to the Evidence Convergence Surface contract and the VDB system contract.

If this plan conflicts with either contract, the contracts take precedence.

---

# Implementation Role

The Evidence Convergence Surface implementation role is to govern exposure of structurally characterized Convergence Geometry records.

An Evidence Convergence Surface implementation answers:

```text
Which structurally characterized evidence regions are eligible for governed exposure,
under which policy,
for which purpose,
with which lineage,
at which generation?
```

It does not answer:

```text
Which evidence is biologically explanatory?

Which gene is causal?

Which variant is pathogenic?

Which candidate should be prioritized?

Which exposed region is clinically actionable?

Which projection format should be emitted?

Which downstream reasoning conclusion should be accepted?
```

Those questions belong to downstream reasoning systems, returned producer assertions, or the Projection View layer.

---

# Non-Goals

This plan does not implement:

```text
Registration Unit creation
Corpus Generation selection
Assertion Record indexing
Evidence Topology derivation
Convergence Geometry characterization
raw producer artifact parsing
producer TEP parsing
Projection View generation
Query Surface implementation
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
candidate prioritization
surface-derived biological confidence scoring
```

Evidence Convergence Surface construction is exposure governance work.

It is not source-evidence work.

It is not topology work.

It is not geometry work.

It is not projection work.

It is not biological reasoning work.

---

# Initial Implementation Target

The initial implementation target is the Evidence Convergence Surface build for the first MARK Phase 4 Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

The initial surface build may be identified as:

```text
mark_phase4_corpus_6tep_v1_surface_build_v1
```

The expected upstream input is the downstream surface input manifest emitted by the Convergence Geometry implementation, such as:

```text
results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/
    downstream_surface_input_manifest.tsv
```

The initial Evidence Convergence Surface implementation should consume the Convergence Geometry Build for the declared Corpus Generation and emit deterministic surface, membership, eligibility, disclosure, lineage, generation, and validation artifacts for downstream Projection View construction.

This Surface Build is not a Projection View.

It is the governed exposure substrate from which Projection Views may later render, package, export, summarize, or query exposed evidence structure.

---

# Inputs

The Evidence Convergence Surface implementation consumes:

```text
Corpus Generation manifest
Assertion Record source reference when available
Evidence Topology Build reference when available
Convergence Geometry Build manifest
Convergence Region artifacts
Geometry Feature artifacts
Structural Motif artifacts when available
downstream surface input manifest
Convergence Geometry validation report when available
surface policy
eligibility policy
disclosure policy
surface validation policy
generation and currency policy when applicable
consumer-awareness policy when applicable
Evidence Convergence Surface contract version
Convergence Geometry contract version
Evidence Topology contract version
Assertion Record contract version
Corpus Generation contract version
system contract version
builder name
builder version
build timestamp
```

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

---

# Outputs

The Evidence Convergence Surface implementation should emit deterministic artifacts outside the Convergence Geometry Build, Evidence Topology Build, Assertion Record index, Corpus Generation manifest, and selected Registration Units.

Expected outputs may include:

```text
surface_build_manifest.tsv
surface_build_manifest.json
evidence_convergence_surfaces.tsv
evidence_convergence_surfaces.jsonl
surface_memberships.tsv
surface_memberships.jsonl
surface_eligibility_basis.tsv
surface_disclosure_basis.tsv
surface_withholding.tsv
surface_lineage.tsv
surface_evidence_strata.tsv
surface_generation_currency.tsv
surface_validation_report.json
surface_validation_report.tsv
surface_build_report.md
downstream_projection_input_manifest.tsv
```

These outputs are Evidence Convergence Surface artifacts.

They do not replace Convergence Geometry.

They do not replace Evidence Topology.

They do not replace Assertion Records.

They do not replace Corpus Generations.

They do not replace Registration Units.

They do not become Projection Views.

They do not become Query Surfaces.

They do not perform biological reasoning.

---

# Recommended Output Location

Initial Phase 4 Evidence Convergence Surface outputs may be written under:

```text
results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/
```

A recommended initial layout is:

```text
results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/
    surface_build_manifest.tsv
    surface_build_manifest.json
    evidence_convergence_surfaces.tsv
    evidence_convergence_surfaces.jsonl
    surface_memberships.tsv
    surface_memberships.jsonl
    surface_eligibility_basis.tsv
    surface_disclosure_basis.tsv
    surface_withholding.tsv
    surface_lineage.tsv
    surface_evidence_strata.tsv
    surface_generation_currency.tsv
    surface_validation_report.json
    surface_validation_report.tsv
    surface_build_report.md
    downstream_projection_input_manifest.tsv
```

The output location should be configurable.

Evidence Convergence Surface output paths must not be confused with Convergence Geometry source paths, Evidence Topology paths, Assertion Record paths, Corpus Generation manifest paths, or Registration Unit source paths.

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

For the initial MARK surface build, a recommended identity shape is:

```text
surface_build_id: mark_phase4_corpus_6tep_v1_surface_build_v1
surface_build_label: MARK Phase 4 6-TEP Evidence Convergence Surface Build v1
input_geometry_build_id: mark_phase4_corpus_6tep_v1_geometry_build_v1
input_topology_build_id: mark_phase4_corpus_6tep_v1_topology_build_v1
input_corpus_generation_id: mark_phase4_corpus_6tep_v1
surface_policy_id: mark_phase4_general_surface_policy
surface_policy_version: v1
eligibility_policy_id: mark_phase4_general_surface_eligibility_policy
eligibility_policy_version: v1
disclosure_policy_id: mark_phase4_general_surface_disclosure_policy
disclosure_policy_version: v1
```

Surface Build identity must remain stable across:

```text
Projection View generation
validation
certification
reconstruction
downstream consumer use
```

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

Recommended initial surface types are:

```text
developer_inspection_surface
validation_surface
general_convergence_surface
```

The first implementation should prove governed exposure mechanics before overfitting to one downstream consumer.

RDGP-facing surfaces are supported by the contract but may be implemented after the general surface mechanics are validated.

A surface identity must remain stable across projection generation, validation, certification, reconstruction, and downstream consumer use.

A surface label must not replace stable surface identity.

---

# Surface Policy Requirements

Every Evidence Convergence Surface Build must declare a surface policy.

The surface policy defines the surface purpose, surface type, construction scope, consumer-awareness behavior, generation behavior, and high-level exposure intent.

A surface policy should declare:

```text
surface_policy_id
surface_policy_version when available
surface_type
surface_purpose
input_geometry_build_id
eligible geometry-derived record classes
surface construction scope
target_consumer_class when applicable
consumer purpose when applicable
generation behavior
currency behavior
lossiness behavior
validation behavior
```

For the initial MARK build, a policy may be identified as:

```text
mark_phase4_general_surface_policy_v1
```

A surface policy must not define biological meaning.

A surface policy must not define Projection View format.

A surface policy must not define RDGP reasoning behavior.

A surface policy governs exposure substrate construction.

It does not package the exposed substrate.

---

# Eligibility Policy Requirements

Every Evidence Convergence Surface Build must declare an eligibility policy.

The eligibility policy defines which geometry-derived records are procedurally suitable for governed exposure.

An eligibility policy should declare:

```text
eligibility_policy_id
eligibility_policy_version when available
eligible geometry record classes
required lineage conditions
required validation conditions
required uncertainty visibility
required namespace-state visibility
required completeness visibility when applicable
required generation metadata
required currency metadata when applicable
required reconstruction handles
consumer-readiness criteria when applicable
policy-declared structural criteria when applicable
unsupported record behavior
deferred record behavior
validation behavior
```

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

Eligibility means structurally and procedurally suitable for governed exposure.

Eligibility does not mean biologically correct.

Eligibility does not mean clinically actionable.

Eligibility does not mean explanatory.

Eligibility does not mean prioritized.

Structural criteria may determine procedural exposure suitability.

Structural criteria must not assert biological importance.

---

# Disclosure Policy Requirements

Every Evidence Convergence Surface Build must declare a disclosure policy.

The disclosure policy defines which eligible or evaluated geometry-derived records are exposed, withheld, deferred, deprecated, superseded, not applicable, or not evaluated.

A disclosure policy should declare:

```text
disclosure_policy_id
disclosure_policy_version when available
disclosure statuses
withholding statuses
withholding reason vocabulary
deferred behavior
deprecated behavior
superseded behavior
consumer-specific disclosure behavior when applicable
lossiness behavior
omission behavior
validation behavior
```

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

Disclosure means a geometry-derived record is included in a governed surface.

Disclosure does not mean VDB endorses biological meaning.

Withholding does not mean the evidence is absent.

Withholding does not mean the evidence is negative.

Deferral does not mean the evidence is unsupported.

Disclosure is an exposure state.

It is not an evidence interpretation.

---

# Surface Membership Requirements

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

Eligibility status values may include:

```text
eligible
ineligible
deferred
not_applicable
not_evaluated
```

Disclosure status values may include:

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

Surface Membership must not replace Convergence Regions.

Surface Membership must not replace Geometry Features.

Surface Membership must not replace Structural Motifs.

Surface Membership must not replace topology relationships.

Surface Membership must not replace Assertion Records.

---

# Surface Membership Identity Strategy

Every Surface Membership record must have a stable identity.

A deterministic `surface_membership_id` should be derived from stable components when available, such as:

```text
surface_id
surface_build_id
input_geometry_build_id
convergence_region_id when applicable
geometry_feature_ids when applicable
structural_motif_ids when applicable
eligibility_policy_id
disclosure_policy_id
```

For example, a region membership identity may be derived from:

```text
surface_id
surface_build_id
input_geometry_build_id
convergence_region_id
eligibility_policy_id
disclosure_policy_id
```

Membership identity must be deterministic under fixed inputs and policy.

Membership identity must not depend on:

```text
filesystem traversal order
database incidental row-return order
Python object iteration order
non-stable temporary row numbers
report rendering order
```

If a stable Surface Membership identity cannot be produced, the membership must fail validation or be emitted with an explicit unresolved identity status according to the declared validation policy.

---

# Eligibility Basis Requirements

Every eligible or ineligible surface membership must declare an eligibility basis.

Eligibility basis records should preserve:

```text
surface_membership_id
surface_id
eligibility_status
eligibility_basis_type
eligibility_basis_value or reference
eligibility_policy_id
eligibility_policy_version when available
source_geometry_reference
source_topology_reference when applicable
source_assertion_reference when applicable
source_corpus_generation_id
source_registration_unit_reference when applicable
validation_status
```

Eligibility basis must be reconstructable from governed VDB records.

Eligibility basis must preserve the policy used to evaluate eligibility.

Eligibility basis must not be replaced by an opaque exposure score.

Eligibility basis must not imply biological correctness.

---

# Disclosure Basis Requirements

Every exposed or withheld surface membership must declare a disclosure basis.

Disclosure basis records should preserve:

```text
surface_membership_id
surface_id
disclosure_status
disclosure_basis_type
disclosure_basis_value or reference
disclosure_policy_id
disclosure_policy_version when available
withholding_reason when applicable
source_geometry_reference
source_topology_reference when applicable
source_assertion_reference when applicable
source_corpus_generation_id
source_registration_unit_reference when applicable
validation_status
```

Disclosure basis must be reconstructable from governed VDB records or explicit surface policy.

Disclosure basis must not be replaced by an opaque disclosure flag.

Disclosure basis must not imply biological endorsement.

---

# Withholding And Lossiness Requirements

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

Lossiness records should preserve:

```text
surface_id
surface_build_id
surface_membership_id when applicable
lossiness_status
lossiness_type
lossiness_basis
omitted_record_reference when applicable
withheld_record_reference when applicable
policy_reference
validation_status
```

---

# Evidence Strata And Lineage Requirements

Evidence Convergence Surfaces must preserve evidence strata and lineage sufficient for downstream Projection Views and consumers to evaluate exposed structure.

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

# Generation And Currency Requirements

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

Generation and currency records should preserve:

```text
surface_id
surface_build_id
surface_generation_id when available
input_geometry_build_id
input_topology_build_id when available
input_corpus_generation_id
input_assertion_record_index_id when available
build_timestamp
refresh_status
staleness_status
supersession_status
supersedes_surface_id when applicable
superseded_by_surface_id when applicable
validation_status
```

---

# Consumer Awareness Requirements

Evidence Convergence Surfaces must remain representation-neutral and consumer-neutral unless explicitly declared otherwise.

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

For the initial implementation, consumer-aware surfaces should be optional unless the selected surface type requires consumer-specific behavior.

Recommended initial posture:

```text
Implement general, validation, or developer-inspection surfaces first.

Add RDGP-facing or other consumer-aware surfaces after general exposure
governance mechanics are validated.
```

---

# RDGP-Facing Surface Requirements

RDGP-facing surfaces are supported by the Evidence Convergence Surface contract.

When implemented, RDGP-facing surfaces and downstream projections must preserve enough lineage for RDGP to evaluate:

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

# Validation Strategy

Evidence Convergence Surface validation should operate in five tiers.

## Tier 1: Input Validation

Input validation confirms that governed upstream sources are available.

Validation must check:

```text
input_geometry_build_id exists
input Convergence Geometry Build is readable
input_topology_build_id is traceable when applicable
input_corpus_generation_id is traceable
input Assertion Record source is traceable
downstream surface input manifest exists
surface policy is declared
eligibility policy is declared
disclosure policy is declared
builder name is declared
builder version is declared when available
build timestamp is declared
```

Validation must also confirm:

```text
Evidence Convergence Surface construction does not directly parse raw producer artifacts
Evidence Convergence Surface construction does not re-run ingestion
Evidence Convergence Surface construction does not reconstruct Registration Units
Evidence Convergence Surface construction does not bypass Assertion Record primacy
Evidence Convergence Surface construction does not bypass Evidence Topology
Evidence Convergence Surface construction does not bypass Convergence Geometry
```

## Tier 2: Surface Identity Validation

Surface identity validation confirms that the Surface Build and surfaces are stable and purpose-declared.

Validation must check:

```text
surface_build_id exists
surface_build_id is stable
surface_id exists
surface_id is stable
surface_type is declared
surface_purpose is declared
surface_build_id is linked to input_geometry_build_id
surface_build_id is linked to input_corpus_generation_id
target_consumer_class is declared when applicable
generation context is visible
currency context is visible when applicable
validation_status is declared
certification_status is declared when available
```

## Tier 3: Membership Validation

Membership validation confirms that exposure evaluation records are explicit and reconstructable.

Validation must check:

```text
surface memberships are explicit
surface_membership_id exists
surface_membership_id is stable
memberships trace to source geometry records
memberships trace to source topology records when applicable
memberships trace to source Assertion Records when applicable
eligibility status is declared for evaluated memberships
disclosure status is declared for evaluated memberships
eligibility basis is declared
disclosure basis is declared
withholding reason is declared when applicable
lineage is reconstructable
lossiness status is explicit when applicable
```

## Tier 4: Evidence Strata, Completeness, And Consumer Validation

Evidence strata validation must check:

```text
producer-family strata are preserved
evidence-domain strata are preserved
modality strata are preserved when available
uncertainty states are preserved
null semantics are preserved when available
namespace mediation status is preserved
generation metadata are preserved
currency metadata are preserved when applicable
reconstruction handles are available
withholding and lossiness states are explicit when relevant
```

Completeness validation must check, when applicable:

```text
evidence completeness status is preserved when available
completeness scope is preserved when available
absence basis is explicit when evidence absence is asserted
omission basis is explicit when evidence is not exposed
withholding basis is explicit when evidence is withheld
evidence present but withheld is distinguishable from evidence absent
evidence not evaluated is distinguishable from evidence negative
```

Consumer-aware validation must check, when applicable:

```text
target_consumer_class is declared
consumer purpose is declared
consumer readiness basis is declared
consumer-specific eligibility policy is declared when required
consumer-specific disclosure policy is declared when required
consumer readiness is not treated as biological correctness
```

## Tier 5: Anti-Collapse Validation

Anti-collapse validation confirms that Evidence Convergence Surface construction did not exceed its layer authority.

Validation must check:

```text
surface does not modify Convergence Geometry
surface does not mutate Registration Units
surface does not expand Corpus Generation scope silently
surface does not become source evidence
surface does not replace Convergence Geometry
surface does not replace Geometry Features
surface does not replace Convergence Regions
surface does not replace Structural Motifs
surface does not become a Projection View
surface does not become a Query Surface
surface does not perform biological reasoning
surface does not embed RDGP reasoning
surface does not convert structural eligibility into biological confidence
surface disclosure is not treated as biological endorsement
surface membership is not treated as source evidence
withheld evidence is not treated as absent evidence
ineligible evidence is not treated as negative evidence
deferred evidence is not treated as unsupported evidence
opaque surface scores do not replace eligibility basis
```

Validation must confirm governed exposure and reconstructability.

Validation must not claim biological correctness.

---

# Determinism Requirements

Evidence Convergence Surface outputs must be deterministic under fixed inputs.

Given the same:

```text
Corpus Generation manifest
Assertion Record source
Evidence Topology Build reference
Convergence Geometry Build
downstream surface input manifest
surface policy
eligibility policy
disclosure policy
generation and currency policy
contract version
builder version
Convergence Geometry contents
```

the builder should produce equivalent:

```text
surface_build_id
surface_ids
surface_membership_ids
eligibility statuses
disclosure statuses
eligibility basis records
disclosure basis records
withholding records
lossiness records
lineage records
generation and currency records
summary records
validation outcomes
report sections
downstream projection input manifest
```

Determinism requirements include:

```text
stable surface_build_id generation
stable surface_id generation
stable surface_membership_id generation
stable eligibility policy behavior
stable disclosure policy behavior
stable withholding behavior
stable generation behavior
stable currency behavior
stable unresolved-state vocabulary
stable eligibility status vocabulary
stable disclosure status vocabulary
stable lossiness vocabulary
stable validation status vocabulary
stable source geometry record ordering
stable source topology relationship ordering when applicable
stable source Assertion Record ordering when applicable
stable duplicate handling
stable failure handling under declared policy
```

SQLite row-return order must not define surface record order.

Filesystem traversal order must not define surface derivation order.

All source geometry record lists used in surface or membership identity generation should be sorted by stable geometry record identifiers.

All source topology relationship lists used in lineage should be sorted by stable `topology_relationship_id`.

All source Assertion Record lists used in lineage should be sorted by stable `assertion_id`.

---

# Reconstruction Requirements

Evidence Convergence Surface artifacts must support reconstruction of:

```text
which Corpus Generation bounded the surface
which Assertion Record source was used when available
which Evidence Topology Build supported the input geometry
which Convergence Geometry Build was used
which Convergence Regions were evaluated
which Geometry Features were evaluated
which Structural Motifs were evaluated when applicable
which surface policy was applied
which eligibility policy was applied
which disclosure policy was applied
which surface type was emitted
which surface purpose was declared
which target consumer class applied when applicable
which memberships were emitted
which eligibility status was assigned to each evaluated membership
which disclosure status was assigned to each evaluated membership
which eligibility basis justified each eligibility status
which disclosure basis justified each disclosure status
which withholding reasons applied when applicable
which lossiness states applied when applicable
which geometry records supported each membership
which topology relationships supported each membership when applicable
which Assertion Records supported each membership when applicable
which Registration Units contributed lineage when applicable
which producer families were represented
which evidence domains were represented
which modalities were represented when available
which uncertainty states were present
which null states were present when available
which namespace states were direct, mediated, ambiguous, conflicted, or unresolved
which evidence completeness status applied when available
which completeness scope applied when available
which absence basis was used when evidence absence was asserted
which omission basis was used when evidence was not exposed
which generation context applied
which currency context applied
which builder produced the surface
which downstream projection input manifest was emitted
```

Surface reconstruction must preserve enough information for downstream Projection Views, Query Surfaces, RDGP-facing projections, future downstream reasoning, and future reinterpretation.

---

# Relationship To Convergence Geometry

Convergence Geometry is the direct input to Evidence Convergence Surfaces.

The responsibility boundary is:

```text
Convergence Geometry
    characterizes topology-derived structure

Evidence Convergence Surface
    governs exposure of structurally eligible convergence substrate
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

Evidence Convergence Surfaces must not expand Corpus Generation scope silently.

Evidence Convergence Surfaces must not include geometry records outside the declared input Geometry Build unless a new Geometry Build or explicitly versioned input scope is declared.

Evidence Convergence Surfaces must preserve Corpus Generation and Registration Unit lineage for downstream Projection Views, RDGP reasoning, and reconstruction.

---

# Relationship To Projection Views

Projection Views represent, render, package, export, summarize, or query governed VDB records for a purpose.

Evidence Convergence Surfaces provide governed exposure substrate for Projection Views.

The responsibility boundary is:

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

The responsibility boundary is:

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

# Relationship To Downstream Derived Layers

Evidence Convergence Surfaces provide the governed exposure substrate for:

```text
Projection Views
Query Surfaces
RDGP-facing consumer projections
future consumer-specific projections
future downstream reasoning
```

Downstream derived layers must preserve surface lineage.

The following must not occur inside Evidence Convergence Surface implementation:

```text
Projection View materialization that replaces surface authority
Query Surface implementation that replaces surface authority
RDGP reasoning
biological interpretation
clinical actionability assignment
causality assignment
candidate prioritization
surface eligibility interpreted as biological confidence
surface disclosure interpreted as biological endorsement
withholding interpreted as absence
ineligibility interpreted as negative evidence
consumer readiness interpreted as biological correctness
```

---

# Anti-Collapse Safeguards

Implementation must prevent:

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

Any implementation that performs one of these actions violates this plan and the Evidence Convergence Surface contract.

---

# Initial Test Strategy

Initial tests should use small synthetic or fixture Convergence Geometry builds before running against the MARK corpus.

Recommended tests include:

```text
test_surface_requires_geometry_build
test_surface_requires_corpus_generation
test_surface_requires_surface_policy
test_surface_requires_eligibility_policy
test_surface_requires_disclosure_policy
test_surface_build_preserves_surface_build_id
test_surface_build_preserves_input_geometry_build_id
test_surface_build_preserves_input_corpus_generation_id
test_surface_identity_requires_surface_type
test_surface_identity_requires_surface_purpose
test_surface_membership_requires_stable_identity
test_surface_membership_traces_to_geometry_records
test_surface_membership_preserves_eligibility_status
test_surface_membership_preserves_disclosure_status
test_surface_membership_preserves_eligibility_basis
test_surface_membership_preserves_disclosure_basis
test_surface_membership_preserves_withholding_reason_when_applicable
test_surface_preserves_geometry_lineage
test_surface_preserves_topology_lineage_when_applicable
test_surface_preserves_assertion_record_lineage_when_applicable
test_surface_preserves_corpus_generation_lineage
test_surface_preserves_registration_unit_lineage_when_applicable
test_surface_preserves_generation_context
test_surface_preserves_currency_context_when_applicable
test_surface_preserves_lossiness_status_when_applicable
test_surface_preserves_namespace_state
test_surface_preserves_uncertainty_state
test_surface_preserves_null_semantics_when_available
test_surface_does_not_modify_geometry
test_surface_does_not_mutate_registration_units
test_surface_does_not_expand_corpus_scope
test_surface_does_not_become_projection
test_surface_does_not_perform_biological_reasoning
test_surface_outputs_are_deterministic
test_downstream_projection_input_manifest_is_emitted
```

MARK integration tests should confirm:

```text
mark_phase4_corpus_6tep_v1 Convergence Geometry Build is accepted as input
surface build identity is stable
general convergence surface is emitted when policy-enabled
developer inspection surface is emitted when policy-enabled
validation surface is emitted when policy-enabled
surface memberships are emitted deterministically
eligibility statuses are emitted deterministically
disclosure statuses are emitted deterministically
withholding reasons are emitted when applicable
geometry lineage is preserved
topology lineage is preserved when applicable
Assertion Record lineage is preserved when applicable
generation and currency records are emitted
surface validation report is deterministic
downstream projection input manifest is deterministic
```

Tests must not require biological correctness.

Tests validate governed exposure, reconstructability, determinism, lineage preservation, generation and currency preservation, withholding semantics, and anti-collapse behavior.

---

# Initial Implementation Sequence

The initial implementation should proceed in the following order:

```text
1. Define Evidence Convergence Surface policy.

2. Define eligibility policy.

3. Define disclosure policy.

4. Define generation and currency behavior.

5. Define withholding and lossiness behavior.

6. Define initial surface types.

7. Define consumer-awareness behavior.

8. Load Corpus Generation manifest.

9. Load Convergence Geometry Build manifest.

10. Load downstream surface input manifest.

11. Validate governed input boundary.

12. Generate Surface Build identity.

13. Generate Evidence Convergence Surface identity.

14. Evaluate policy-enabled geometry-derived records for eligibility.

15. Evaluate policy-enabled geometry-derived records for disclosure.

16. Construct Surface Membership records.

17. Construct eligibility basis records.

18. Construct disclosure basis records.

19. Construct withholding and lossiness records when applicable.

20. Construct evidence strata and lineage records.

21. Construct generation and currency records.

22. Validate surfaces and memberships.

23. Emit surface build manifest.

24. Emit Evidence Convergence Surface artifacts.

25. Emit Surface Membership artifacts.

26. Emit surface validation report.

27. Emit surface build report.

28. Emit downstream projection input manifest.

29. Add synthetic tests.

30. Add MARK corpus smoke test.

31. Hand off Surface Build to Projection View implementation.
```

Each step must preserve geometry lineage.

Each step must preserve topology lineage through geometry when available.

Each step must preserve Assertion Record lineage through topology when available.

Each step must preserve Corpus Generation lineage.

Each step must remain non-mutating with respect to Registration Units, Assertion Records, Evidence Topology, and Convergence Geometry.

---

# Expected CLI Shape

A future command-line interface may use a pattern such as:

```bash
python scripts/phase4/build_evidence_convergence_surface.py \
  --geometry-build-manifest results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/geometry_build_manifest.tsv \
  --surface-input-manifest results/phase4/convergence_geometry/mark_phase4_corpus_6tep_v1_geometry_build_v1/downstream_surface_input_manifest.tsv \
  --corpus-manifest results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/corpus_generation_manifest.tsv \
  --output-dir results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1 \
  --surface-build-id mark_phase4_corpus_6tep_v1_surface_build_v1 \
  --surface-policy-id mark_phase4_general_surface_policy_v1 \
  --eligibility-policy-id mark_phase4_general_surface_eligibility_policy_v1 \
  --disclosure-policy-id mark_phase4_general_surface_disclosure_policy_v1
```

or:

```bash
python scripts/phase4/validate_evidence_convergence_surface.py \
  --surface-build-manifest results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/surface_build_manifest.tsv \
  --surfaces results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/evidence_convergence_surfaces.tsv \
  --memberships results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1/surface_memberships.tsv \
  --output-dir results/phase4/evidence_convergence_surfaces/mark_phase4_corpus_6tep_v1_surface_build_v1
```

The exact script names are not contractually fixed.

The CLI must make Convergence Geometry input, Corpus Generation identity, surface policy, eligibility policy, disclosure policy, and output location explicit.

---

# Expected Input Manifest Shape

A downstream surface input manifest may include:

```text
geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
convergence_region_id
region_kind
region_bounding_basis
geometry_feature_id_summary
feature_kind_summary
structural_motif_id_summary when applicable
source_topology_relationship_id_summary
source_assertion_id_summary
registration_unit_id_summary
validation_status
```

This manifest is produced by Convergence Geometry implementation.

It is not an Evidence Convergence Surface.

It must be validated against the Convergence Geometry Build before surface construction begins.

---

# Expected Surface Build Manifest Shape

A Surface Build manifest may include:

```text
surface_build_id
surface_build_label
input_geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
surface_policy_id
surface_policy_version
eligibility_policy_id
eligibility_policy_version
disclosure_policy_id
disclosure_policy_version
builder_name
builder_version
build_timestamp
validation_status
certification_status
contract_version
schema_version
```

Additional columns may be added as implementation matures.

Column additions must preserve backward-compatible reconstruction where possible.

---

# Expected Evidence Convergence Surface Shape

An Evidence Convergence Surface table may include:

```text
surface_id
surface_label
surface_type
surface_purpose
surface_build_id
input_geometry_build_id
input_topology_build_id
input_corpus_generation_id
surface_generation_id
target_consumer_class
validation_status
certification_status
```

This table declares governed exposure objects.

It is not a Projection View.

It is not a Query Surface.

It is not biological reasoning.

---

# Expected Surface Membership Shape

A Surface Membership table may include:

```text
surface_membership_id
surface_id
surface_build_id
input_geometry_build_id
convergence_region_id
geometry_feature_id_summary
structural_motif_id_summary
source_topology_relationship_id_summary
source_assertion_id_summary
eligibility_status
disclosure_status
eligibility_basis_summary
disclosure_basis_summary
withholding_reason
lossiness_status
validation_status
```

Surface Membership records may be one-to-many relative to surfaces.

Surface Membership records must remain explicit and reconstructable.

---

# Expected Eligibility Basis Shape

An eligibility basis table may include:

```text
surface_membership_id
surface_id
eligibility_status
eligibility_basis_type
eligibility_basis_value
eligibility_basis_reference
eligibility_policy_id
eligibility_policy_version
source_geometry_reference
source_topology_reference
source_assertion_reference
source_corpus_generation_id
source_registration_unit_reference
validation_status
```

Eligibility basis records may be one-to-many relative to Surface Membership records.

Eligibility basis records must explain why a membership was eligible, ineligible, deferred, not applicable, or not evaluated.

---

# Expected Disclosure Basis Shape

A disclosure basis table may include:

```text
surface_membership_id
surface_id
disclosure_status
disclosure_basis_type
disclosure_basis_value
disclosure_basis_reference
disclosure_policy_id
disclosure_policy_version
withholding_reason
source_geometry_reference
source_topology_reference
source_assertion_reference
source_corpus_generation_id
source_registration_unit_reference
validation_status
```

Disclosure basis records may be one-to-many relative to Surface Membership records.

Disclosure basis records must explain why a membership was exposed, withheld, deferred, deprecated, superseded, not applicable, or not evaluated.

---

# Expected Surface Lineage Shape

A surface lineage table may include:

```text
surface_id
surface_build_id
surface_membership_id
input_geometry_build_id
convergence_region_id
geometry_feature_id
structural_motif_id
input_topology_build_id
source_topology_relationship_id
source_assertion_id
input_corpus_generation_id
source_registration_unit_id
producer_family
evidence_domain
modality_when_available
namespace_status
uncertainty_state
null_state_when_available
validation_status
```

Lineage records must support reconstruction from surface records back through geometry, topology, Assertion Records, Corpus Generation, and Registration Units.

---

# Expected Generation And Currency Shape

A generation and currency table may include:

```text
surface_id
surface_build_id
surface_generation_id
input_geometry_build_id
input_topology_build_id
input_corpus_generation_id
input_assertion_record_index_id
build_timestamp
surface_policy_version
eligibility_policy_version
disclosure_policy_version
refresh_status
staleness_status
supersession_status
supersedes_surface_id
superseded_by_surface_id
validation_status
```

Generation and currency records must prevent stale or superseded surfaces from masquerading as current.

---

# Expected Downstream Projection Input Manifest Shape

A downstream projection input manifest may include:

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

This manifest exists to make Projection View construction deterministic.

It must not specify Projection View format.

It must not render, package, query, or export the surface.

It must not perform biological reasoning.

---

# Exit Criteria

The Evidence Convergence Surface implementation plan is complete when:

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
evidence strata are preserved
uncertainty states are preserved
null semantics are preserved when available
namespace states are preserved
generation context is preserved
currency context is preserved when applicable
lossiness status is explicit when applicable
machine-readable surface artifacts are emitted
human-readable surface build report is emitted
surface validation report is emitted
downstream projection input manifest is emitted
outputs are deterministic under fixed inputs
surface can serve as input to Projection Views
surface does not become source evidence
surface does not become a projection
surface does not become a query interface
surface does not perform biological reasoning
surface remains representation-neutral
anti-collapse safeguards pass
```

This implementation is not complete merely because a table, manifest, export, dashboard, query response, report, or package exists.

It is complete only when those records satisfy the Evidence Convergence Surface contract and can safely serve as governed exposure substrate for Projection Views.

---

# Summary

The Evidence Convergence Surface implementation plan establishes the governed exposure layer in VDB Phase 4.

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

The guiding rule is:

```text
Consume geometry.

Evaluate eligibility.

Declare disclosure.

Preserve withholding.

Preserve evidence strata.

Preserve lineage.

Preserve generation.

Preserve currency.

Remain projection-neutral.

Do not package.

Do not query.

Do not reason.

Never convert exposure into interpretation.
```

Evidence Convergence Surfaces expose governed structure without interpreting meaning.

They make structurally eligible convergence substrate available for projections and downstream reasoning.

They do not identify biological truth.

They do not confer biological confidence.

# Evidence Topology and Projection Geometry Formalism

> Status: SAGE-VDB mathematical foundation draft.
> This document defines the formal mathematical substrate by which VDB derives
> Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, and
> method-specific projection surfaces from preserved producer Assertion Records.
> It is intended for mathematical review and downstream implementation
> governance. It is not an implementation schema, storage design, or RDGP
> reasoning model.

---

# 1. Purpose

VDB exists to preserve heterogeneous producer evidence and transform it into
traceable, statistically reason-ready substrates for downstream systems such as
RDGP.

The purpose of this document is to formalize the mathematical model behind that
transformation.

It defines how VDB moves from:

```text
preserved producer assertions
    → typed evidence topology
        → opportunity-aware projection geometry
            → evidence convergence surfaces
                → method-specific projection surfaces
                    → TEP-VDB reason-ready transport
```

The central claim is:

```text
VDB transforms preserved producer assertions into statistically reason-ready
projection surfaces by constructing a typed, traceable evidence incidence
topology; applying declared projection policies and opportunity structures;
measuring convergence geometry over bounded substructures; and emitting
non-authoritative, reconstructable surfaces for downstream reasoning.
```

This document is intended to be reviewed by mathematically trained
collaborators. Its role is to make the mathematical spine of VDB explicit before
implementation schemas, validators, builders, and TEP-VDB emission contracts are
derived.

---

# 2. Position in the VDB Design Stack

This document formalizes the mathematical substrate underlying the existing
VDB design models:

```text
docs/design/assertion_record_and_projection_model.md
docs/design/evidence_topology_model.md
docs/design/convergence_geometry_model.md
docs/design/evidence_convergence_surface_model.md
docs/design/opportunity_space_and_projection_policy_model.md
docs/design/assertion_projection_taxonomy.md
        ↓
docs/design/mathematical_foundations/evidence_topology_projection_geometry_formalism.md
        ↓
docs/architecture/tep_vdb_architecture.md
        ↓
docs/design/projection_surfaces/oacs_opportunity_absence_callability_surface.md
docs/design/projection_surfaces/cues_conflict_uncertainty_evidence_state_surface.md
docs/design/projection_surfaces/rmcs_reasoning_method_currency_surface.md

docs/design/projection_surfaces/kvps_known_variant_pathogenicity_surface.md
docs/design/projection_surfaces/girs_genotype_inheritance_readiness_surface.md
docs/design/projection_surfaces/paps_phenotype_alignment_prior_surface.md
docs/design/projection_surfaces/pgers_patient_gene_evidence_rollup_surface.md

docs/design/projection_surfaces/cfbs_coordinate_first_burden_scan.md
docs/design/projection_surfaces/mplc_matched_prior_locus_contrast.md
docs/design/projection_surfaces/evrs_exact_variant_recurrence_surface.md
docs/design/projection_surfaces/rfps_regulatory_feature_projection_surface.md
        ↓
implementation specifications, schemas, validators, builders, and TEP-VDB exports
```

The upstream documents are architecture-facing and CS-friendly. They establish
responsibilities, authority boundaries, reconstruction duties, projection
taxonomy, and anti-collapse doctrine.

This document is mathematical. It defines the formal objects, maps, invariants,
and invalid transformations that future VDB topology, geometry, surface, and
projection builders must obey.

---

# 3. Terminology Note for Mathematical Reviewers

VDB uses several terms that overlap with formal mathematical language. This
section fixes their intended meaning for this document.

## Topology

In this document, **topology** means a typed evidence-incidence organization
model.

It does not necessarily mean point-set topology.

The preferred abstract representation is a typed directed incidence hypergraph.
The preferred implementation-compatible representation is a set of typed
relational incidence tables.

## Geometry

In this document, **geometry** means quantitative or structured measurement over
Evidence Topology and opportunity-aware projection substrates.

It does not necessarily mean metric geometry unless a projection policy defines
a metric.

## Surface

A **surface** is a bounded, traceable, governed mathematical exposure object.

A surface may be represented as a table, matrix, tensor, graph projection,
manifest, JSON structure, or transport package.

A surface is not biological truth.

## Projection

A **projection** is a purpose-bound, reconstructable view over preserved evidence
or governed derived structure.

Projection is view generation.

It is not evidence generation.

---

# 4. Foundational Doctrine

VDB preserves assertions.

VDB derives topology.

VDB characterizes geometry.

VDB exposes surfaces.

VDB emits projections.

RDGP reasons.

Scientists and clinicians interpret.

The governing epistemic invariant is:

```text
observation ≠ annotation ≠ projection ≠ interpretation ≠ reasoning
```

Where:

```text
observation
    evidence anchored to source, context, and identity

annotation
    overlay or label attached to evidence under a declared source or policy

projection
    governed mapping from one substrate to another

interpretation
    biological, clinical, mechanistic, or causal meaning assignment

reasoning
    downstream statistical, probabilistic, prioritization, or inference process
```

VDB may preserve, organize, project, expose, and transport evidence.

VDB must not silently interpret, rank, prioritize, diagnose, or assert causality.

---

# 5. Primitive Preserved Object: Corpus-Indexed Assertion Records

Let:

```text
C = a declared Corpus Generation
```

Define:

```text
A_C = {a_1, a_2, ..., a_n}
```

where `A_C` is the corpus-indexed set of preserved Assertion Records selected by
Corpus Generation `C`.

Each assertion `a_i` is a provenance-bound, context-bounded producer claim. It
may contain or reference:

```text
assertion_id
source_assertion_key
producer family
producer package identity
registration_unit_id
corpus_generation_id
assertion_record_index_id
participants
relationship or relationship class
evidence basis
source identity references
context
authority state
uncertainty state
confidence/support context when available
independence context when available
temporal/generation context when available
lineage and reconstruction handles
```

`A_C` is the primitive mathematical input substrate for VDB topology and
projection geometry.

Graphs, hypergraphs, relational tables, matrices, tensors, surfaces, and
TEP-VDB exports are downstream derived structures.

They are not primitive truth objects.

---

# 6. Identity and Provenance Non-Collapse

VDB distinguishes multiple identity layers.

The identity ladder includes:

```text
producer package identity
registration unit identity
corpus generation identity
assertion record index identity
source identity
source_assertion_key
corpus-indexed assertion_id
brokered identity attachment
topology identity
geometry identity
surface identity
projection identity
TEP-VDB export identity
consumer-side identity
```

The governing rule is:

```text
No downstream identity may replace an upstream preserved identity.
```

A topology relationship is not an Assertion Record.

A geometry feature is not a topology relationship.

A surface row is not a source assertion.

A projection record is not source truth.

A TEP-VDB package is not the evidence corpus itself.

For any derived object `x`, VDB must preserve a lineage map:

```text
lin(x) → source identity basis
```

where the source identity basis may include Assertion Records, Registration
Units, Corpus Generation, source artifacts, source rows, source identities,
namespace-resolution events, and policy identifiers.

If `lin(x)` is empty or non-reconstructable, `x` is not VDB-compliant.

---

# 7. Additive Namespace Brokerage as Identity Relation Structure

Namespace brokerage is modeled as an additive identity relation structure.

Let:

```text
I_source = set of source-native identities
I_brokered = set of brokered, canonical, coordinate, feature, gene,
             phenotype, sample, producer, or transport identities
```

Define the brokerage relation:

```text
B_C ⊆ I_source × I_brokered × Status × Provenance × Policy
```

A brokerage tuple records that a source identity has a governed relationship to
a brokered or canonical identity under a declared mapping status, provenance,
and policy.

Example mapping statuses include:

```text
resolved
unresolved
ambiguous
conflicted
deprecated
not_applicable
not_evaluated
source_identity_preserved
bridge_available
bridge_required
bridge_missing
deferred_by_policy
```

Core invariant:

```text
Brokered identity relationships may add paths in Evidence Topology,
but they must not overwrite source identity nodes.
```

This is essential for VDB because coordinate/reference-context identity is the
default substrate for variant-derived evidence. Gene identity is a routed
specialization, not the root identity model for all genomic evidence.

A noncoding or intergenic coordinate observation without a gene label remains a
valid source evidence object.

---

# 8. Evidence Topology Formalism

Evidence Topology is a typed evidence incidence system derived from `A_C`,
source identity structures, and declared construction policies.

The preferred abstract object is:

```text
T_C = (V_C, E_C, H_C, τ, ρ, σ, κ)
```

where:

```text
V_C
    set of typed evidence nodes

E_C
    set of typed directed pairwise relationships

H_C
    set of typed higher-order incidence relationships or hyperedges

τ
    type map over nodes, pairwise edges, and hyperedges

ρ
    role map assigning participant roles within relationships and hyperedges

σ
    provenance map from topology elements back to Assertion Records,
    source identities, Registration Units, source artifacts, and Corpus Generation

κ
    construction policy and build-context map
```

Evidence nodes may include:

```text
AssertionRecord
SourceTEP
RegistrationUnit
CorpusGeneration
SourceArtifact
SourceRecord
SourceIdentity
BrokeredIdentity
Sample
CoordinateVariantIdentity
VariantEntity
SampleVariantObservation
GenotypeObservation
Gene
FeatureInterval
CoordinateWindow
LocusWindow
PhenotypeScope
SemanticPrior
OpportunityRegion
ProjectionPolicy
NullDraw
Surface
```

Relationship or hyperedge types may include:

```text
emitted_by
registered_in
selected_by_corpus
has_source_identity
brokered_to
observed_in_sample
has_coordinate_identity
has_genotype_observation
overlaps_feature
maps_to_gene
near_locus
has_phenotype_scope
has_gsc_prior
belongs_to_window
belongs_to_locus
contributes_to_burden_cell
selected_as_background
member_of_projection
traceable_to
```

The inclusion of `H_C` is necessary because VDB evidence is frequently
higher-order. A producer assertion may simultaneously involve sample, variant,
gene, phenotype, source artifact, evidence basis, producer context, uncertainty,
and provenance.

A binary graph may be a useful projection of `T_C`, but it is not the complete
formal substrate.

---

# 9. Topological Traceability Invariant

Every topology element must be reconstructable.

For every topology element:

```text
x ∈ V_C ∪ E_C ∪ H_C
```

VDB requires:

```text
σ(x) ≠ ∅
```

Plain-language rule:

```text
Every topology node, edge, or hyperedge must trace back to preserved Assertion
Records or governed identity/provenance structures.
```

A topology element that cannot be reconstructed from preserved evidence and a
declared construction policy is invalid.

Evidence Topology may describe organization.

It may not create evidence.

---

# 10. Projection Policy Formalism

A projection policy is a versioned mathematical rule for mapping one evidence
substrate to another.

Let:

```text
θ = projection policy
```

A projection policy should declare:

```text
source substrate
target substrate
eligibility rule
filter rule
membership rule
counting rule
opportunity rule
lossiness rule
ambiguity rule
null-model rule when applicable
emission rule
validation rule
```

A projection policy induces a membership operator:

```text
M_θ : O_C → P(Y_θ)
```

where:

```text
O_C
    eligible source observations or evidence objects from T_C

Y_θ
    target objects such as coordinate windows, locus windows, genes,
    features, phenotype priors, candidate intervals, background sets,
    annotation targets, or export records

P(Y_θ)
    power set of Y_θ

M_θ(o)
    set of target memberships assigned to source object o under policy θ
```

Examples:

```text
sample-specific variant observation → coordinate window
sample-specific variant observation → locus window
coordinate variant → feature interval
feature interval → gene
gene → phenotype-scoped GSC prior
locus → matched background locus set
window → candidate interval
```

Projection policies are not biological truth.

They are declared mapping rules.

---

# 11. Membership Anti-Duplication Invariant

A source observation may have multiple memberships.

Multiple memberships do not imply multiple source observations.

Formal rule:

```text
For o ∈ O_C, |M_θ(o)| may be greater than 1.
```

However, aggregation must declare the unit being counted:

```text
count over source observations
count over sample-specific observations
count over coordinate identities
count over memberships
count over unique samples
count over patients
count over loci
count over windows
count over source assertions
```

The default burden-counting unit for variant-derived VDB projection surfaces is:

```text
sample-specific coordinate observation
```

unless a projection policy explicitly declares another unit.

This prevents the following failure mode:

```text
one variant maps to three transcripts
        ↓
three transcript memberships are counted as three observed variants
```

Correct behavior:

```text
one source observation
        ↓
three memberships
        ↓
one observed variant count unless policy explicitly counts memberships
```

In current VDB implementation terminology, the default countable sample-specific coordinate observation corresponds to `sample_variant_observation_id` or its genotype-aware successor.

---

# 12. Opportunity Space Formalism

Opportunity space defines what could have been observed under a declared assay,
callability, quality, and model-eligibility context.

For a projection policy `θ`, define:

```text
Ω_θ = (U_θ, μ_θ, q_θ)
```

where:

```text
U_θ
    eligible coordinate, feature, window, locus, sample-target, or target universe

μ_θ
    opportunity measure over U_θ

q_θ
    opportunity-state function over U_θ
```

Example opportunity measures:

```text
callable bases per coordinate window
callable bases per sample-window
callable bases per locus
callable bases per sample-locus
assayed bases per feature
eligible variants under a variant-class model
```

Example opportunity states:

```text
callable
absent_with_opportunity
not_callable
not_assayed
low_confidence
filtered
unknown
not_applicable
```

`absent_with_opportunity` is a derived analysis condition, not a replacement for raw opportunity states such as callable, not_callable, not_assayed, filtered, unknown, or opportunity_unmodeled.

Core doctrine:

```text
Observed evidence is numerator substrate.
Opportunity space is denominator substrate.
```

A burden surface without declared opportunity context is descriptive only.

It is not opportunity-normalized convergence evidence.

---

# 13. Burden and Recurrence as Measured Topology

Given projection policy `θ`, membership operator `M_θ`, and opportunity object
`Ω_θ`, define a target set:

```text
Y_θ = {y_1, y_2, ..., y_m}
```

For target `y ∈ Y_θ`, define burden:

```text
B_θ(y) = count or weighted count of qualifying source observations o
         such that y ∈ M_θ(o)
```

The counting unit must be declared by `θ`.

Define opportunity-normalized rate when the denominator is valid:

```text
R_θ(y) = B_θ(y) / μ_θ(y)
```

provided:

```text
μ_θ(y) > 0
q_θ(y) supports denominator interpretation
```

Define recurrence:

```text
K_θ(y) = number of distinct samples or patients with at least one qualifying
         observation assigned to y
```

`B_θ`, `R_θ`, and `K_θ` are geometry features.

They are not biological conclusions.

---

# 14. Convergence Region Formalism

A Convergence Region is a bounded typed substructure of Evidence Topology under
a declared region policy.

Let:

```text
ψ = region policy
```

Then:

```text
R_ψ ⊆ T_C
```

or more precisely:

```text
R_ψ = induced typed substructure of T_C under region policy ψ
```

Region policies may be based on:

```text
shared participant
coordinate window
locus window
phenotype scope
producer-crossing evidence
multi-modal evidence intersection
source provenance neighborhood
epistemic contrast
reasoning re-entry lineage
```

A Convergence Region is an internal mathematical object.

It is not a biological hypothesis.

---

# 15. Convergence Geometry Feature Functions

Convergence Geometry characterizes bounded topology substructures.

Let:

```text
Sub(T_C) = set of bounded typed substructures of T_C
```

A geometry feature is a function:

```text
φ_j : Sub(T_C) → X_j
```

where `X_j` may be numeric, categorical, Boolean, vector-valued, or structured.

Examples:

```text
density
intersection complexity
breadth
depth
producer diversity
modality diversity
provenance diversity
epistemic diversity
independence
temporal persistence
burden count
opportunity-normalized burden rate
patient recurrence
compactness
matched-background percentile
empirical tail probability
```

A Convergence Profile for region `R` is:

```text
Φ(R) = (φ_1(R), φ_2(R), ..., φ_k(R))
```

A Convergence Profile characterizes evidence organization.

It does not rank, prioritize, or interpret biology.

---

# 16. Convergence Geometry Object

For projection policy `θ`, define:

```text
G_θ = Γ(T_C, M_θ, Ω_θ, θ)
```

where:

```text
G_θ
    opportunity-aware convergence geometry induced by Evidence Topology,
    projection memberships, opportunity structure, and policy θ

Γ
    governed geometry construction function
```

`G_θ` may contain:

```text
burden matrices
recurrence matrices
membership incidence matrices
opportunity denominator arrays
convergence profiles
bounded region features
structural motifs
candidate interval structures
matched-background summaries
null-model summaries
```

Geometry characterizes structure.

Geometry does not interpret structure.

---

# 17. Evidence Convergence Surface Formalism

An Evidence Convergence Surface is a governed exposure object derived from
Evidence Topology, projection policy, opportunity space, and Convergence
Geometry.

Define:

```text
S_θ = F_θ(T_C, M_θ, Ω_θ, G_θ, θ)
```

where:

```text
S_θ
    emitted evidence convergence or projection surface

F_θ
    governed surface construction function
```

A surface may be represented as:

```text
table
matrix
tensor
hypergraph projection
JSON package
manifest
TEP-VDB export
validation report
```

Representation does not confer authority.

A matrix is not more truthful than a table.

A graph is not more authoritative than a manifest.

A TEP-VDB package is not source truth.

---

# 18. Surface-Cell Traceability Map

For every emitted surface `S_θ`, VDB requires a traceability map:

```text
tr_θ : cells(S_θ) → finite typed substructures of T_C
```

For every emitted cell, row, count, score, membership, or summary:

```text
c ∈ cells(S_θ)
```

VDB requires:

```text
tr_θ(c) ≠ ∅
```

Plain-language rule:

```text
Every emitted surface element must trace back to a finite evidence substructure
and to the declared construction policy that produced it.
```

The traceability basis should allow a reviewer to answer:

```text
Which source assertions support this surface element?
Which observations were counted?
Which memberships were used?
Which opportunity denominator was used?
Which projection policy produced this element?
Which identity brokerage events were involved?
Which ambiguity, uncertainty, or lossiness states apply?
Which validation receipts cover this element?
```

This is the central anti-hallucination invariant of VDB projection geometry.

---

# 19. Null-Model Formalism

Some projection surfaces require null models.

A null model is declared only where required by a projection policy.

Define:

```text
N_θ = declared null model associated with projection policy θ
```

A null model must declare:

```text
what is held fixed
what is randomized or exchanged
what opportunity space is respected
what matching features are used
what statistic is compared
whether the null is local or genome-wide / surface-wide
how many draws or permutations are used
which random seed or reproducibility mechanism is used
which interpretation labels are permitted
```

Possible null structures include:

```text
matched exchangeability model
matched opportunity randomization
permutation distribution
resampling distribution
genomewide max-statistic null
per-window exploratory null
matched background locus null
```

Null-model evidence emitted by VDB surfaces is exploratory unless a downstream
validated reasoning layer owns stronger inferential claims.

---

# 20. Projection Surfaces as Method-Specific Specializations

CFBS and MPLC are not separate mathematical systems.

They are method-specific projection policies over the shared VDB formalism.

## 20.1 CFBS Specialization

For Coordinate-First Burden Scan:

```text
θ_CFBS:
    source observations = sample-specific coordinate variant observations
    target objects = genomic coordinate windows
    membership = observation belongs to window by coordinate overlap
    opportunity = callable bases per window or sample-window
    geometry = burden, recurrence, and optional compactness
    null = matched genomic opportunity randomization
    surface = CFBS coordinate-first burden scan projection
```

Existing CFBS quantities include:

```text
w = genomic window
s = patient or sample
N[w] = number of qualifying variants observed in window w
C[w] = callable opportunity in window w
R[w] = N[w] / C[w]
E[w] = (T / C_total) × C[w]
burden_excess[w] = N[w] / E[w]
K[w] = number of patients with ≥1 qualifying variant in window w
```

CFBS follows the order:

```text
coordinates → burden scan → candidate intervals → post hoc biological annotation
```

GSC priors may annotate CFBS-nominated intervals after coordinate-first ranking.

They must not select the scan windows for a coordinate-first analysis.

## 20.2 MPLC Specialization

For Matched Prior-Locus Contrast:

```text
θ_MPLC:
    source observations = sample-specific coordinate variant observations
    target objects = GSC-prior target locus windows and matched background locus windows
    membership = observation belongs to locus window by declared policy
    opportunity = callable bases per sample-locus
    geometry = burden and recurrence
    null = matched non-prior background locus exchangeability
    surface = MPLC matched prior-locus contrast projection
```

Existing MPLC quantities include:

```text
s = patient or sample
g = gene or locus window
B[s,g] = qualifying variant count for sample s near locus g
C[s,g] = callable bases for sample s near locus g
R[s,g] = B[s,g] / C[s,g]
O_target = sum of B[s,g] across patients and GSC-prior loci
C_target = sum of C[s,g] across patients and GSC-prior loci
R_target = O_target / C_target
K[g] = number of patients with ≥1 qualifying variant near locus g
```

MPLC uses GSC priors at the front to define target loci.

Its claim is therefore prior-informed, not coordinate-first genome-wide
discovery.

---

# 21. TEP-VDB as Export Projection over Surfaces

TEP-VDB is an export projection over VDB-derived surfaces and their required
lineage.

Define:

```text
TEP_VDB_θ = Export_θ(S_θ, lineage, policy, disclosure)
```

A TEP-VDB package is:

```text
transport view
reason-ready substrate
policy-declared export
traceability-preserving package
```

It is not:

```text
source truth
independent evidence
RDGP conclusion
biological interpretation
clinical result
```

TEP-VDB should carry enough information for RDGP to reason without re-ingesting
VAP, GSC, or other producer packages independently.

At minimum, a method-specific TEP-VDB export should preserve:

```text
surface identity
projection policy identity
source corpus identity
topology build identity
geometry build identity
opportunity model identity
membership rules
counting rules
null model, when applicable
source traceability
validation receipts
anti-overclaim labels
validation_receipts
anti_overclaim_label_set
```

---

# 22. RDGP Boundary and Reasoning Re-Entry

VDB emits reason-ready surfaces.

RDGP reasons.

RDGP outputs may return to VDB as new producer assertions.

Formal boundary:

```text
RDGP_output ⊄ S_θ
```

unless the RDGP output is re-ingested as a future Assertion Record and included
in a later Corpus Generation.

RDGP must not mutate the input surface.

RDGP results must not overwrite Assertion Records, Evidence Topology,
Convergence Geometry, or prior Evidence Convergence Surfaces.

Reasoning re-entry is monotonic expansion:

```text
S_θ
    → RDGP reasoning
        → TEP-RDGP
            → new Assertion Records
                → future topology / geometry / surfaces
```

Earlier evidence states remain historically valid relative to their source
corpus.

---

# 23. Governing Invariants

The formalism is governed by the following invariants.

## 23.1 Assertion Primacy

```text
All topology, geometry, surfaces, and projections derive from preserved
Assertion Records or governed Registration Unit / Corpus Generation structures.
```

## 23.2 Identity Non-Collapse

```text
No downstream identity may replace an upstream preserved identity.
```

## 23.3 Additive Namespace Brokerage

```text
Identity brokerage adds relationships. It does not mutate source identities.
```

## 23.4 Topology Traceability

```text
For every topology element x:

σ(x) ≠ ∅
```

## 23.5 Membership Anti-Duplication

```text
Projection memberships may multiply relationships.
They must not multiply source observations unless explicitly declared by a
counting policy.
```

## 23.6 Opportunity-Aware Burden Interpretation

```text
A burden surface without declared opportunity context is descriptive only.
```

## 23.7 Geometry Non-Interpretation

```text
Geometry characterizes structure. It does not claim biological meaning.
```

## 23.8 Surface-Cell Traceability

```text
For every emitted surface element c:

tr_θ(c) ≠ ∅
```

## 23.9 Projection Non-Authority

```text
Projection changes representation and access.
It does not change authority.
```

## 23.10 Null-Model Declaration

```text
Every null-model surface must declare what is fixed, randomized, matched,
measured, and compared.
```

## 23.11 RDGP Boundary Preservation

```text
VDB exposes. RDGP evaluates. Returned reasoning re-enters only as new assertions.
```

## 23.12 Deterministic Reconstructability

```text
Under fixed inputs, fixed policies, and fixed software versions, VDB-derived
surfaces must be reconstructable.
```

---

# 24. Invalid Mathematical Patterns

The following patterns violate this formalism.

## 24.1 Untraceable Surface Element

A surface row, cell, score, count, or summary lacks traceability to finite
topology substructures and declared policy.

## 24.2 Burden without Opportunity

A burden surface reports counts or rates without declaring observable
opportunity and missingness/callability state.

## 24.3 Membership Counted as Observation

A source observation maps to multiple features, transcripts, genes, or windows,
and those memberships are counted as independent observations without an
explicit counting policy.

## 24.4 Gene Identity Replaces Coordinate Identity

Coordinate or variant-derived evidence is collapsed into gene identity such
that noncoding, intergenic, ambiguous, or feature-dependent evidence is lost.

## 24.5 Projection Row Replaces Assertion Record

A projection or export row becomes treated as the source evidence object.

## 24.6 Surface Score Treated as Biological Conclusion

A convergence score, burden excess, recurrence count, or empirical-tail value is
reported as causality, pathogenicity, disease association, diagnosis, or
clinical actionability.

## 24.7 RDGP Result Mutates Source Surface

A downstream reasoning output modifies the source surface instead of returning
as new preserved assertions.

## 24.8 Missingness Collapsed into Zero

`unknown`, `not_assayed`, `not_callable`, `filtered`, and
`absent_with_opportunity` are collapsed into a single zero or missing state.

## 24.9 GSC Prior Used as CFBS Window Selector

A coordinate-first scan uses GSC prior loci to choose scan windows and still
claims to be coordinate-first.

## 24.10 Unversioned Projection Policy

A surface emits projection results without declaring the policy, version,
lossiness, and source-target mapping rule that generated them.

---

# 25. Mathematical Review Questions

This section defines the intended review questions for mathematical
collaborators.

1. Is a typed directed incidence hypergraph, with relational incidence tables as
   the implementation-compatible representation, an appropriate substrate for
   VDB Evidence Topology?

2. Are projection policies correctly modeled as membership operators from source
   observations or evidence objects to target objects?

3. Does the traceability map `tr_θ` sufficiently prevent provenance loss and
   hallucinated surface cells?

4. Is opportunity space adequately modeled as a denominator measure and
   observability-state function?

5. Are burden, recurrence, compactness, density, diversity, and temporal
   persistence valid geometry features over bounded evidence substructures?

6. Does the membership anti-duplication invariant correctly prevent
   double-counting when one observation maps to multiple features, genes,
   transcripts, windows, or priors?

7. Are OACS, CUES, RMCS, KVPS, GIRS, PAPS, PGERS, CFBS, MPLC, EVRS, and RFPS
   coherent specializations of the same formal machinery, with surface-specific
   projection policies, opportunity models, traceability requirements, and
   anti-overclaim boundaries?

8. Are the null-model declaration requirements sufficient for exploratory
   empirical evidence surfaces?

9. Should future VDB versions use stronger mathematical structures for selected
   surfaces, such as simplicial complexes, sheaves, category-theoretic functors,
   measure-theoretic kernels, persistent homology, or another formalism?

10. What mathematical assumptions should be made explicit before implementation
    schemas and builders are derived from this model?

---

# 26. Non-Goals

This document does not define:

```text
SQLite DDL
physical file formats
implementation schemas
DEX builder code
complete opportunity-space file format
complete projection-surface implementations
complete CFBS implementation
complete MPLC implementation
complete EVRS implementation
complete RFPS implementation
complete OACS / CUES / RMCS implementation
complete KVPS / GIRS / PAPS / PGERS implementation
RDGP prioritization model
clinical interpretation
formal disease association testing
```

Those belong to downstream specifications, schemas, validators,
implementation plans, and reasoning-system designs.

---

# 27. Implementation Obligations Derived from the Formalism

Future DEX-VDB implementation documents should derive concrete schemas and
validators from this formalism.

At minimum, implementations should preserve:

```text
corpus_generation_id
assertion_record_index_id
assertion_id
source_assertion_key
registration_unit_id
source identity lineage
brokerage event lineage
topology build identity
projection_policy_id
projection_policy_version
membership identity
opportunity_model_id
geometry_build_id
surface_id
surface_generation_id
projection_id
traceability references
validation receipts
```

Builders must expose enough metadata to reconstruct:

```text
which assertions were selected
which topology was built
which projection policies were applied
which memberships were created
which opportunity denominators were used
which geometry features were computed
which surface elements were emitted
which validation checks passed or failed
```

No implementation is compliant merely because it emits tables.

It is compliant only if the emitted tables instantiate the formal objects and
invariants defined here.

---

# 28. Summary Doctrine

The mathematical spine of VDB is:

```text
A_C
    → T_C
    → (M_θ, Ω_θ)
    → G_θ
    → S_θ
    → TEP-VDB
    → RDGP
```

where:

```text
A_C
    corpus-indexed preserved Assertion Records

T_C
    typed evidence topology

M_θ
    projection-policy-induced membership operator

Ω_θ
    opportunity space and denominator structure

G_θ
    convergence geometry

S_θ
    traceable evidence convergence or projection surface

TEP-VDB
    export projection over VDB-derived surfaces

RDGP
    downstream reasoning system
```

The anti-hallucination condition is:

```text
For every emitted surface element c:

tr_θ(c) ≠ ∅
```

The anti-collapse condition is:

```text
No projection, surface, geometry feature, topology relationship, or brokered
identity may replace the preserved assertion and source identity basis from
which it was derived.
```

The opportunity condition is:

```text
Burden evidence requires declared opportunity context before it can be treated
as opportunity-normalized reasoning substrate.
```

The downstream boundary is:

```text
VDB exposes deterministic reasoning capacity.
RDGP evaluates that capacity.
Reasoning outputs return only as new assertions.
```

In this way, VDB can transform intersecting lines of evidence into advanced,
traceable, statistically reason-ready surfaces without losing provenance,
duplicating truth, or crossing into biological interpretation.

# Appendix: Relationship to Current VDB Developmental Phase Indices

```text
Phase 4.4 Evidence Topology      ≈ T_C
Phase 4.5 Convergence Geometry   ≈ G_θ
Phase 4.6 Convergence Surfaces   ≈ S_θ
Phase 4.7 Consumer Surfaces      ≈ TEP-VDB export / consumer-specific projection
```
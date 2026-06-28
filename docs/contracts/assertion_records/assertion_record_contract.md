# Assertion Record Contract

## Purpose

This document defines the VDB contract for Assertion Records.

An Assertion Record is the primary preserved scientific claim object in VDB.

Assertion Records preserve producer-emitted scientific claims in a corpus-indexable, provenance-bound, context-bounded form so that downstream VDB layers can derive Evidence Topology, characterize Convergence Geometry, construct Evidence Convergence Surfaces, and emit Projection Views without losing producer identity, source identity, evidence basis, uncertainty, authority context, or reconstruction paths.

This contract ensures that Assertion Records remain:

```text
producer-aware
claim-preserving
context-bounded
provenance-bound
participant-explicit
relationship-explicit
evidence-basis-preserving
authority-aware
uncertainty-aware
lineage-preserving
corpus-indexable
reconstructable
```

Assertion Records preserve what producers claimed.

They do not represent VDB belief.

They do not determine biological correctness.

---

# Scope

This contract applies to all VDB Assertion Records, including Assertion Records derived or resolved from:

```text
VAP registration units
GSC registration units
future RSP registration units
future RDGP-returned registration units
future TEP-VDB products
future TEP-RDGP products
future external evidence capsules
future producer evidence packages
future reasoning producer outputs
```

This contract governs the logical requirements of Assertion Records.

It does not prescribe a single physical storage representation.

Assertion Records may be represented by:

```text
relational rows
SQLite records
TSV records
JSON records
JSONL records
Parquet records
lakehouse partitions
object-store metadata records
future storage backends
```

The representation is not the architecture.

The preserved, traceable, producer-emitted scientific claim is the architecture.

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

This contract defines the obligations of the Assertion Record layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Assertion Record contract governs the transition from declared corpus scope into preserved scientific claim objects.

An Assertion Record answers:

```text
What did a producer claim,
about which participants,
under what relationship,
with what evidence basis,
in what context,
with what provenance,
authority,
and uncertainty?
```

An Assertion Record does not answer:

```text
What is connected across assertions?

What topology emerges from the corpus?

What convergence geometry exists?

Which convergence regions are surface-eligible?

What projections should consumers receive?

What biological meaning should downstream systems infer?

Whether the producer claim is biologically correct?
```

Those responsibilities belong to downstream contracts or downstream reasoning systems.

---

# Definition

An Assertion Record is a provenance-bound, context-bounded evidence statement made by a producer about one or more participants, with an explicit relationship, evidence basis, and epistemic status.

An Assertion Record is the primary preserved scientific object used by Phase 4 derived layers.

An Assertion Record must preserve enough information to support:

```text
producer claim reconstruction
participant reconstruction
relationship reconstruction
evidence basis reconstruction
context reconstruction
provenance reconstruction
authority reconstruction
uncertainty reconstruction
source identity reconstruction
source artifact reconstruction
registration unit reconstruction
corpus generation reconstruction
topology derivation
geometry derivation
surface lineage
projection lineage
downstream consumer reconstruction
```

An Assertion Record is preservation-authoritative for what VDB preserved as a producer-emitted claim.

It is not authoritative for biological truth.

It is not an observation itself.

It is not a raw artifact.

It is not a source identity.

It is not topology.

It is not geometry.

It is not a surface.

It is not a projection.

It is not downstream reasoning.

---

# Core Invariant

The architectural rule is:

```text
Assertion Records preserve producer scientific claims.

Derived layers organize, characterize, expose, or project those claims.

Derived layers do not replace those claims.
```

Assertion Records are the last preservation layer before derived organization begins.

The governing transition is:

```text
Registration Units
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
```

This means:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Topology derives organization.
```

---

# Producer Neutrality

Assertion Records must be producer-neutral.

The contract must support heterogeneous producer families without forcing all producers into the same biological shape.

Examples of producer-specific assertion patterns may include:

```text
VAP
    sample-variant-gene interpretation claims
    variant observation claims
    variant prioritization claims
    validation claims
    routing claims

GSC
    phenotype-gene semantic prior claims
    source-gene relationship claims
    gene provenance claims
    source contribution relationship claims
    producer contract validation claims

Future RSP
    condition-gene expression claims
    transcriptomic contrast claims
    enrichment claims
    pathway activity claims

Future RDGP
    sample-gene prioritization claims
    phenotype compatibility claims
    inheritance compatibility claims
    reasoning confidence claims

External Evidence Capsules
    externally sourced evidence claims
    ontology-derived claims
    literature-derived claims
    database snapshot claims
```

No producer family may require a hard-coded Assertion Record structure that prevents other producer families from being represented.

Participants must be role-bearing.

Relationships must be explicit.

Evidence basis and context must remain producer-aware.

---

# Relationship To Registration Units

Registration Units preserve assertion registrations.

Assertion Records are constructed, resolved, or indexed from assertion registrations within selected Registration Units.

The distinction is:

```text
Registration Unit
    preserves registered custody over an accepted producer evidence package

assertion registration
    registration-layer record that preserves assertion-bearing material
    within a Registration Unit

Assertion Record
    corpus-indexable preserved scientific claim object used by Phase 4
    derived layers
```

Assertion Records must preserve traceability to their source Registration Units.

Each Assertion Record must preserve:

```text
registration_unit_id
source_package_id
source_artifact_id or source artifact reference
assertion registration reference when applicable
source identity references when applicable
```

An Assertion Record must not erase the Registration Unit boundary from which it was constructed.

---

# Relationship To Corpus Generations

Corpus Generations declare the evidence scope from which Assertion Records are indexed.

Assertion Records must preserve Corpus Generation lineage.

Each corpus-indexed Assertion Record must preserve:

```text
corpus_generation_id
corpus_generation_label when available
corpus_generation_version when available
selection policy reference when available
```

The same underlying producer assertion may participate in more than one Corpus Generation.

When this occurs, each corpus-indexed Assertion Record or Assertion Record membership record must preserve which Corpus Generation selected it.

A Corpus Generation does not replace Assertion Records.

Assertion Records do not replace Corpus Generations.

---

# Required Assertion Record Identity

Every Assertion Record must have a stable identity.

An Assertion Record identity must preserve:

```text
assertion_id
assertion_label when available
assertion_type
producer_family
producer_id or producer reference
registration_unit_id
corpus_generation_id
source_package_id
source_artifact_id or source artifact reference
source_assertion_registration_id when available
created_at or indexed_at timestamp
indexing_process or builder name
indexing_process_version when available
validation_status
```

Assertion identity must be stable across topology derivation, geometry derivation, surface construction, projection generation, validation, and reconstruction.

Human-readable labels may support inspection.

Labels must not replace stable Assertion Record identity.

---

# Required Assertion Components

An Assertion Record must preserve or explicitly declare absence for the following components:

```text
producer identity
assertion type
relationship or relationship class
participants
evidence basis
context
provenance
authority context
uncertainty context
confidence or support context when available
independence context when available
temporal or generation context
source artifact references
source identity references
registration unit references
corpus generation references
payload references when applicable
validation status
```

Required components must not be collapsed into an opaque score, summary, or projection row.

If a component is unavailable, not applicable, not reported, unresolved, or intentionally absent, that state must be explicit when relevant.

---

# Participant Obligations

Assertion Records must preserve participants as role-bearing components.

A participant record should preserve:

```text
participant_id or participant reference
participant_role
participant_namespace when available
participant_value or resolvable reference
source_identity_reference when available
source_artifact_reference when available
producer_family
participant_context when available
```

Participant roles may include, but are not limited to:

```text
sample
variant
gene
transcript
phenotype
condition
contrast
source
semantic channel
pathway
regulatory_region
enhancer
promoter
chromatin_domain
noncoding_interval
regulatory_feature
cohort
publication
method
environment
reasoning output
external authority
```

Participant vocabulary may evolve as new producer families are added.

Participant identity must remain distinguishable from canonical identity.

Source participants must not be overwritten by namespace-resolved participants.

Canonical identifiers may be attached separately through namespace governance.

---

# Relationship Obligations

Assertion Records must preserve the relationship asserted by the producer.

A relationship record must preserve:

```text
relationship_id or relationship reference when available
relationship_type
relationship_label when available
relationship_directionality when applicable
relationship_arity
relationship_context when available
producer_family
assertion_type
```

Relationships may be unary, binary, or higher-order.

VDB must not force all assertions into a subject-predicate-object model when the producer claim requires a richer participant structure.

Examples of relationship classes may include:

```text
variant observed in sample
variant assigned interpretation label
variant associated with gene
gene associated with phenotype prior
source contributes evidence for gene
producer contract validation result
gene differentially expressed under condition
sample-gene prioritization output
inheritance compatibility assertion
external source supports participant relationship
```

Relationship preservation does not imply biological correctness.

A relationship inside an Assertion Record represents what the producer claimed.

It does not represent VDB endorsement.

---

# Evidence Basis Obligations

Assertion Records must preserve the evidence basis for the producer claim when available.

Evidence basis may include:

```text
source artifact
source row
source record
source table
source file
source database snapshot
source method
source score
source count
source threshold
source validation result
source provenance channel
source contribution channel
producer-specific payload reference
external evidence snapshot
```

Evidence basis must remain traceable to Registration Units and source artifacts.

Evidence basis may be represented directly or by reconstructable reference.

Large payloads do not need to be duplicated inside the Assertion Record if reconstruction is guaranteed.

Evidence basis must not be replaced by opaque summaries that prevent reconstruction of the producer claim.

---

# Context Obligations

Assertion Records must preserve context sufficient to interpret the producer claim as emitted.

Context may include:

```text
phenotype context
sample context
cohort context
condition context
contrast context
genome build context
transcript context
annotation context
regulatory context
regulatory domain context
chromatin context
noncoding burden context
regulatory feature annotation context
disease model context
method context
release context
run context
producer version context
schema version context
temporal context
evidence generation context
reasoning generation context when applicable
```

Context must remain distinct from biological interpretation.

Context explains the boundaries under which the producer emitted the claim.

Context does not determine whether the claim is biologically correct.

---

# Provenance Obligations

Assertion Records must preserve provenance sufficient to reconstruct:

```text
which producer emitted the claim
which producer family emitted the claim
which run or release generated the claim when available
which TEP transported the claim
which Registration Unit preserved the claim-bearing package
which Corpus Generation selected the Registration Unit
which artifact contained the claim-bearing material
which assertion registration carried the claim-bearing material when applicable
which source identities participated in the claim
which indexing process constructed or resolved the Assertion Record
which validation checks were applied
```

Assertion Record provenance must include:

```text
producer reference
source package reference
source artifact reference
registration unit reference
corpus generation reference
source identity references when applicable
indexing process reference
schema or contract version when available
validation report reference when available
```

An Assertion Record without reconstructable provenance is not VDB-compliant.

---

# Authority And Uncertainty Obligations

Assertion Records have preservation authority.

They do not have biological truth authority.

An Assertion Record is authoritative for:

```text
what producer claim was preserved
which producer emitted it
which evidence basis supported it
which context bounded it
which provenance produced it
which uncertainty or epistemic state accompanied it
```

An Assertion Record is not authoritative for:

```text
whether the claim is biologically correct
whether the claim is clinically actionable
whether the claim explains phenotype
whether the claim establishes causality
whether the claim should be prioritized
whether the claim is independently replicated
```

Assertion Records must preserve uncertainty and epistemic status when available.

Examples of uncertainty or epistemic states may include:

```text
positive
negative
null
uncertain
conflicting
unsupported
provisional
deprecated
withdrawn
not_applicable
not_reported
ambiguous
unresolved
```

VDB must not collapse:

```text
absence of evidence into negative evidence
uncertainty into falsehood
conflict into consensus
deprecated evidence into deleted evidence
provisional evidence into certified evidence
```

When uncertainty context is absent, unknown, or not applicable, that state should be explicit when relevant.

---

# Confidence And Support Obligations

Assertion Records may preserve confidence or support context when producer data provides it.

Confidence or support context may include:

```text
producer score
semantic score
support count
frequency count
validation status
quality flag
confidence label
evidence channel
threshold status
method-derived confidence
producer-specific confidence class
```

Confidence or support values must preserve producer context.

VDB must not convert heterogeneous producer confidence values into a single opaque cross-producer confidence score at the Assertion Record layer.

Cross-assertion aggregation, if performed, belongs downstream and must remain traceable to source Assertion Records.

---

# Independence And Temporal Obligations

Assertion Records should preserve independence context when available.

Independence context may include:

```text
producer run
producer release
source artifact
source table
source database
source publication
source cohort
source method
source evidence channel
source derivation group
replicate group
reasoning generation
evidence generation
```

Independence context helps downstream layers avoid false convergence.

The Assertion Record layer must preserve available independence metadata.

It must not infer independence beyond declared or reconstructable evidence.

Assertion Records must also preserve temporal or generation context when available, including:

```text
producer run timestamp
producer release version
TEP generation timestamp
Registration Unit creation timestamp
Corpus Generation build timestamp
Assertion Record indexing timestamp
evidence generation identifier
reasoning generation identifier when applicable
```

Temporal context must not be collapsed across generations.

---

# Payload And Reconstruction Obligations

Assertion Records must preserve enough structured information for indexing, derivation, validation, and reconstruction.

An Assertion Record may preserve large or producer-specific payloads by reference rather than duplication.

Payload references may include:

```text
source artifact reference
source row reference
source record reference
source table reference
source file reference
registration unit record reference
producer payload path
external snapshot reference
object-store reference
checksum reference when available
```

Payload references must be resolvable or explicitly marked as unavailable.

If a payload reference cannot be resolved, the Assertion Record must expose that reconstruction limitation.

Payload lossiness must be explicit.

An Assertion Record must not be considered complete if the preserved core fields and payload references are insufficient to reconstruct the producer claim.

---

# Relationship To Evidence Topology

Assertion Records are inputs to Evidence Topology.

Evidence Topology derives organization over Assertion Records.

Assertion Records may preserve internal producer relationships among their participants.

Assertion Records must not derive cross-assertion topology.

The distinction is:

```text
Assertion Record
    preserves what a producer claimed among participants

Evidence Topology
    derives how preserved claims are connected across a corpus
```

Evidence Topology must preserve traceability to source Assertion Records.

A topology relationship must not replace an Assertion Record.

---

# Relationship To Convergence Geometry

Assertion Records do not create Convergence Geometry.

Convergence Geometry is derived from Evidence Topology.

Geometry derivation must preserve Assertion Record lineage through topology relationships.

An Assertion Record must not characterize convergence, density, breadth, depth, producer diversity, modality diversity, epistemic diversity, temporal persistence, or biological meaning.

---

# Relationship To Evidence Convergence Surfaces

Assertion Records do not expose Evidence Convergence Surfaces.

Evidence Convergence Surfaces are governed exposure objects over Convergence Geometry.

Surface construction must preserve Assertion Record lineage.

A surface may expose Assertion Record-derived evidence structure.

A surface must not replace Assertion Records.

A surface must not acquire Assertion Record authority.

---

# Relationship To Projection Views

Assertion Records may be inspected, summarized, exported, or packaged through Projection Views.

A projection over Assertion Records must declare:

```text
projection purpose
projection source layer
source Assertion Record identities
source Registration Unit identities
source Corpus Generation identity
source records
materialization status
lossiness status when applicable
reconstruction path
```

A Projection View over Assertion Records does not replace Assertion Records.

A Projection View does not acquire Assertion Record authority.

If a projection omits Assertion Record fields, the omitted fields and projection lossiness must be explicit when relevant.

---

# Relationship To RDGP Consumer Projections

RDGP-facing consumer projections may include Assertion Record-derived evidence.

RDGP-facing projections must preserve sufficient Assertion Record lineage so that RDGP can evaluate:

```text
which producer emitted the claim
which Registration Unit preserved it
which Corpus Generation selected it
which evidence basis supported it
which participants were involved
which uncertainty state accompanied it
which evidence strata were present or absent
which reasoning generation or evidence generation was used
whether the reasoning substrate was current or stale
```

An Assertion Record does not perform RDGP reasoning.

An Assertion Record does not determine whether evidence explains phenotype.

An Assertion Record only preserves the producer claim available for downstream derivation and projection.

---

# Validation Obligations

Assertion Record validation must confirm:

```text
assertion_id exists
assertion_type exists
producer identity exists
registration_unit_id is traceable
corpus_generation_id is traceable
source package reference is traceable
source artifact reference is traceable when applicable
source assertion registration reference is traceable when applicable
relationship or relationship class is present
participants are declared when applicable
participant roles are explicit when participants are present
evidence basis is declared or explicitly absent
context is declared or explicitly absent
provenance is reconstructable
authority context is visible
uncertainty context is visible
source identity references resolve when applicable
payload references resolve or expose reconstruction limitations
indexing is deterministic
assertion counts reconcile to selected Registration Units when applicable
no assertion collapse occurs
no topology, geometry, surface, projection, or reasoning authority is embedded
```

Validation must confirm preservation and reconstructability.

Validation must not claim biological correctness.

---

# Anti-Collapse Rules

The following are prohibited:

```text
producer identity collapse
assertion type collapse
relationship collapse
participant collapse
participant role collapse
evidence basis collapse
context collapse
provenance collapse
authority collapse
uncertainty collapse
confidence context collapse
independence context collapse
temporal context collapse
registration unit lineage collapse
corpus generation lineage collapse
source artifact lineage collapse
source identity collapse
payload reference collapse
assertion registration collapse
Assertion Record replaced by source identity
Assertion Record replaced by artifact row
Assertion Record replaced by Evidence Object
Assertion Record replaced by Evidence State
Assertion Record replaced by topology relationship
Assertion Record replaced by geometry feature
Assertion Record replaced by surface membership
Assertion Record replaced by projection row
opaque score replacing assertion basis
cross-producer confidence score created at Assertion Record layer
biological truth asserted by VDB
clinical actionability asserted by VDB
causality asserted by VDB
RDGP reasoning embedded in Assertion Record unless returned as a producer assertion
```

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

An Assertion Record implementation is complete only when:

```text
Assertion Record identity is stable
producer identity is preserved
assertion type is preserved
relationship or relationship class is preserved
participants are preserved when applicable
participant roles are explicit when participants are present
evidence basis is preserved or explicitly absent
context is preserved or explicitly absent
provenance is reconstructable
authority context is visible
uncertainty context is visible
confidence or support context is preserved when available
independence context is preserved when available
temporal or generation context is preserved when available
registration unit lineage is preserved
corpus generation lineage is preserved
source artifact lineage is preserved
source identity lineage is preserved when applicable
payload references resolve or expose reconstruction limitations
Assertion Records can serve as input to Evidence Topology
Assertion Records do not derive topology
Assertion Records do not perform biological reasoning
anti-collapse validation passes
```

An Assertion Record implementation is not complete merely because rows, records, files, or indexes exist.

An Assertion Record implementation is complete only when those records satisfy this contract.

---

# Summary

An Assertion Record is the primary preserved scientific claim object in VDB.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Topology derives organization.
```

Assertion Records are the last preservation layer before derived organization begins.

They preserve what producers claimed, not what VDB believes.

The guiding rule is:

```text
Preserve the claim.

Preserve the producer.

Preserve the participants.

Preserve the evidence basis.

Preserve the context.

Preserve the uncertainty.

Preserve the lineage.

Never infer meaning at the preservation layer.
```

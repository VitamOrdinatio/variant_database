# Evidence Topology Over Time

## Epoch V: Rationale Layer

| Epoch | Epoch Identity      | Epoch Purpose                                                                                       |
| ----- | ------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer         | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | Evidence Geometry   | Once assertions exist, how do they organize into biological knowledge?                              |
| III   | Discovery Layer     | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer    | How does one truth generate many useful views without duplication?                                  |
| V     | **Rationale Layer** | **Why is this important?**                                                                          |

---

## Purpose

This document explains why VDB evidence topology must be generation-aware.

VDB does not merely preserve a static evidence state.

It preserves evidence in a form that allows later systems to reconstruct how evidence organization changed as producer assertions, TEPs, downstream reasoning outputs, methods, and scientific paradigms evolved.

The central claim is:

```text
Static topology describes the organization of preserved assertions within one VDB generation.

Longitudinal topology describes how that organization changes across VDB generations and longer scientific-methodological horizons.
```

Evidence topology over time is not a claim that biological truth changed.

It is a preserved record of how assertion-derived evidence organization changed.

---

# Central Rationale

VDB topology changes because the preserved assertion corpus changes across time.

A VDB generation represents a specific evidence state:

```text
assertion corpus
        ↓
topology build
        ↓
geometry build
        ↓
surface build
        ↓
projection state
```

When new producer assertions enter VDB, the assertion corpus changes.

When the assertion corpus changes, the derived topology may change.

When topology changes, convergence geometry may change.

When geometry changes, surfaces and projections may change.

This change is expected.

It is not a defect.

It is the mechanism by which VDB remains scientifically current while preserving historical evidence states.

The governing principle is:

```text
A new assertion does not rewrite the past.

It changes the topology of the present.
```

---

# Two Timescales of Topology Change

VDB evidence topology changes across at least two timescales.

## 1. Operational / Generational Time

This is the immediate information flow inside the VDB ecosystem.

Example:

```text
Producers
        ↓
TEPs
        ↓
VDB₁
        ↓
TEP-VDB
        ↓
RDGP
        ↓
TEP-RDGP
        ↓
VDB₂
```

In this cycle, VDB emits a governed evidence package to a downstream reasoning system.

The reasoning system emits a new TEP.

When that TEP is ingested, its outputs enter VDB as new Assertion Records.

The result is a later VDB generation.

```text
VDB₂ ≠ VDB₁
```

VDB₂ is not VDB₁ corrected.

VDB₂ is VDB₁ expanded by later preserved assertions.

## 2. Scientific / Methodological Time

This is the longer horizon over which scientific methods, producer capabilities, reasoning systems, and paradigms change.

Over this timescale:

* new producer methods appear
* old producer methods are deprecated
* TEP schemas evolve
* new assertion types become possible
* new evidence modalities enter VDB
* reasoning systems change version
* null models change
* validation criteria change
* disease models change
* scientific paradigms shift
* previously accepted hypotheses may be challenged
* previously marginal evidence may become central

This longer timescale is influenced by scientific refutation, methodological evolution, and paradigm change.

VDB does not decide which scientific views survive.

It preserves the evidence history through which hypotheses are proposed, challenged, falsified, replaced, or retained.

---

# Timescale 1: Operational Information Flow

The first topology-over-time pattern is the operational cycle:

```text
Producer systems
        ↓
Producer TEPs
        ↓
VDB₁
        ↓
TEP-VDB
        ↓
Downstream reasoning
        ↓
Reasoning TEP
        ↓
VDB₂
```

This is not a circular overwrite.

It is a generational expansion.

At VDB₁, VDB preserves an assertion corpus produced by upstream systems such as:

* VAP
* GSC
* RSP
* future proteomics producers
* validation producers
* other evidence producers

From that assertion corpus, VDB derives:

```text
topology₁
geometry₁
surfaces₁
projections₁
```

VDB may then emit a governed TEP-VDB package for RDGP or another downstream reasoning system.

RDGP evaluates the evidence package.

RDGP emits a TEP-RDGP.

When VDB ingests TEP-RDGP, the reasoning output is preserved as new Assertion Records.

Now VDB contains a later evidence corpus:

```text
assertion corpus₂
    =
assertion corpus₁
    +
RDGP reasoning assertions
```

From this later corpus, VDB derives:

```text
topology₂
geometry₂
surfaces₂
projections₂
```

This is the first and most concrete form of evidence topology over time.

---

# Why VDB₂ Is Not VDB₁

VDB₂ is temporally later than VDB₁.

It contains preserved assertions that VDB₁ did not contain.

Therefore, VDB₂ may have a different topology.

Differences may include:

* new topology relationships
* new participant neighborhoods
* new cross-producer intersections
* new cross-modality intersections
* new reasoning-output strata
* new convergence geometry
* new evidence convergence surfaces
* new projections
* new refresh or staleness states

This does not mean VDB₁ was wrong.

It means VDB₁ was an earlier preserved evidence state.

The correct relationship is:

```text
VDB₁ remains historically reconstructable.

VDB₂ becomes the current expanded evidence state.
```

Later generations must not overwrite earlier generations.

They must preserve the ability to reconstruct what VDB knew, organized, exposed, and projected at each point in time.

---

# Historical Validity

Historical validity is central to evidence topology over time.

A prior VDB generation remains valid as a historical state even when later evidence changes the current topology.

For example:

```text
VDB₁ may contain VAP and GSC assertions.

VDB₂ may contain VAP, GSC, and RDGP assertions.

VDB₃ may contain VAP, GSC, RDGP, and proteomic assertions.
```

VDB₃ does not erase VDB₂.

VDB₂ does not erase VDB₁.

Each generation records what evidence was preserved and how derived layers were built from that evidence at that time.

This is necessary for:

* audit
* reproducibility
* release comparison
* downstream reasoning refresh
* historical review
* scientific reinterpretation
* method comparison
* producer validation

A later generation may be richer.

It is not allowed to destroy the earlier record.

---

# Timescale 2: Scientific and Methodological Change

The second topology-over-time pattern occurs over longer scientific and methodological horizons.

Over time, the producers that emit TEPs may change.

The kinds of assertions VDB receives may change.

The reasoning systems that consume VDB evidence may change.

The scientific paradigms that define what counts as meaningful evidence may change.

Examples include:

```text
variant-centric evidence
        ↓
gene-level semantic priors
        ↓
transcriptomic context
        ↓
proteomic context
        ↓
multi-omic convergence
        ↓
developmental timing
        ↓
network perturbation
        ↓
future unknown evidence models
```

Each shift may alter what producers assert.

When assertion types change, VDB topology may gain new dimensions.

A topology that once connected evidence primarily through variants and genes may later connect evidence through regulatory regions, cell types, developmental stages, protein states, pathway dynamics, or reasoning outputs.

VDB must be capable of preserving those changes without rewriting earlier evidence.

---

# Popperian Pressure: Refutation Without Deletion

Scientific claims are tested, challenged, revised, and sometimes falsified.

VDB must preserve the evidence record through which that process occurs.

Refutation pressure may enter VDB as:

* counter-assertions
* negative evidence
* null evidence
* validation failures
* lower-confidence reanalyses
* contradictory producer outputs
* deprecated method outputs
* revised reasoning assertions
* method-version changes
* calibration changes

VDB does not delete the earlier claim because a later assertion challenges it.

Instead, VDB preserves both.

The topology may change because the challenged assertion now participates in a different evidence neighborhood.

It may become part of an epistemic contrast region.

It may contribute to a validation conflict surface.

It may cause a prior reasoning output to become stale.

But VDB does not adjudicate the biological outcome.

The Popperian consequence is:

```text
Refutation changes the evidence corpus by adding counter-assertions, validation failures, null evidence, or revised reasoning outputs.

It does not justify deleting the historical assertion record.
```

---

# Kuhnian Change: New Assertion Types and New Topology Dimensions

Scientific paradigms influence what researchers and producer systems are able to assert.

When paradigms shift, the shape of producer evidence may change.

A prior producer ecosystem may primarily emit:

* variant observations
* gene annotations
* phenotype associations
* clinical classifications

A later producer ecosystem may emit:

* regulatory burden assertions
* network perturbation assertions
* developmental timing assertions
* cell-type-specific assertions
* spatial transcriptomic assertions
* proteomic state assertions
* multi-omic convergence assertions
* uncertainty-aware reasoning assertions

These new assertion types do not merely add more rows to the corpus.

They may create new topology dimensions.

They may create new relationships among older assertions.

They may make previously isolated evidence neighborhoods newly connected.

They may expose convergence regions that earlier VDB generations could not represent.

The Kuhnian consequence is:

```text
Scientific paradigm change can alter the kinds of assertions producers emit.

New assertion kinds can reshape VDB topology without rewriting earlier assertions.
```

---

# Eliot-Like Reordering: Prior Assertions in a New Corpus

New evidence can change how prior evidence is situated.

A prior assertion retains its original identity, provenance, context, and epistemic status.

But after new assertions arrive, that prior assertion may belong to a different topology neighborhood.

It may participate in new convergence geometry.

It may appear in new evidence convergence surfaces.

It may be exposed through new projections.

It may become relevant to a reasoning workflow that did not previously exist.

The earlier assertion has not changed.

Its relationship to the expanded corpus has changed.

The Eliot-like consequence is:

```text
New assertions can change how prior assertions are situated without changing what prior assertions originally asserted.
```

This is essential for VDB.

It allows the system to preserve historical evidence while still allowing future evidence to alter the structure around it.

---

# Topology Delta

A topology delta is a structural difference between topology builds across VDB generations.

A topology delta may include:

* new topology relationships
* changed relationship scope
* newly connected participants
* expanded participant neighborhoods
* new producer intersections
* new modality intersections
* new evidence strata
* new epistemic contrast
* new temporal persistence
* new independence relationships
* changed topology derivation basis
* changed topology build rules
* changed topology source corpus

Topology deltas are structural records.

They are not biological conclusions.

A topology delta may say:

```text
A new cross-producer relationship involving POLG appeared between VDB₁ and VDB₂.
```

It must not say:

```text
POLG became more biologically important.
```

The latter is interpretation.

The former is evidence organization.

---

# What Can Change Over Time

The following VDB elements may change across generations:

## Assertion Corpus

New assertions may be added.

Assertions may be superseded by later assertions.

Assertions may gain later counter-assertions or validation assertions.

Historical assertions remain preserved.

## Evidence Topology

New relationships may emerge.

Existing topology neighborhoods may expand.

New topology dimensions may become available as assertion types evolve.

## Convergence Geometry

Structural features may change as topology changes.

Convergence regions may appear, expand, split, or become differently characterized.

## Evidence Convergence Surfaces

New surfaces may become structurally eligible.

Existing surfaces may become historical, superseded, or refresh candidates.

Reasoning-informed surfaces may become stale relative to current evidence.

## Projections

New views may be generated.

Older projections may become historical or stale.

Projection transforms, policies, or consumers may change.

## Reasoning Currency

Reasoning outputs may become stale when evidence, methods, models, or producer versions change.

Staleness is metadata-derived.

It is not a VDB judgment that the reasoning output is false.

---

# What Must Not Change

The following must not be destructively changed:

* historical Assertion Records
* producer identity
* source provenance
* original evidence basis
* original assertion context
* original epistemic status
* prior VDB generation identity
* prior topology build identity
* prior geometry build identity
* prior surface generation identity
* prior projection generation identity
* reconstruction paths for historical states

A later VDB generation may supersede, contextualize, challenge, or expand earlier evidence.

It must not erase or rewrite it.

---

# Reasoning Currency and Staleness

Reasoning currency is one of the clearest examples of topology over time.

A downstream reasoning system reasons over a specific evidence state.

For example:

```text
VDB₁
        ↓
TEP-VDB₁
        ↓
RDGP reasoning run
        ↓
TEP-RDGP₁
        ↓
VDB₂
```

The RDGP output is current relative to the evidence package it consumed.

But later:

```text
VDB₂
        ↓
new producer TEP
        ↓
VDB₃
```

VDB₃ now contains relevant assertions that were not present when RDGP reasoned.

The earlier RDGP assertion may now be stale relative to VDB₃.

This does not mean RDGP was wrong.

It means RDGP reasoned over an earlier evidence corpus.

The correct VDB statement is:

```text
This reasoning assertion was generated from VDB₁-derived evidence.

The current relevant evidence corpus is VDB₃.

A refresh may be warranted.
```

Staleness means a reasoning output belongs to an earlier evidence or method context.

It does not mean VDB has judged the output false.

---

# Method-Driven Staleness

Reasoning may also become stale because the reasoning method changes.

For example:

```text
RDGP v1 reasons over VDB₁.

RDGP v2 introduces a new inheritance model, null model, calibration method, or evidence weighting scheme.

Prior RDGP v1 outputs may be stale relative to the current declared RDGP method.
```

This is method-driven staleness.

It is not evidence-driven staleness.

Both are metadata-derived.

VDB may record:

* reasoning producer version
* reasoning method version
* input VDB generation
* input assertion corpus
* current relevant assertion corpus
* current declared method version
* refresh trigger

VDB must not claim:

```text
RDGP v2 is biologically more correct.
```

unless that claim itself is preserved as a producer assertion.

---

# What VDB May Say

VDB may safely make structural and metadata-derived statements such as:

* a new assertion entered the corpus
* a new producer TEP was ingested
* a new topology relationship was derived
* a topology neighborhood expanded
* a convergence region became structurally eligible
* a surface became active
* a surface became historical
* a reasoning-informed surface became stale due to new evidence
* a reasoning-informed surface became stale due to method update
* a projection became stale due to source generation change
* a VDB generation differs from an earlier VDB generation

These are evidence-organization statements.

They are within VDB's responsibility.

---

# What VDB Must Not Say

VDB must not claim:

* biological truth changed
* a hypothesis was falsified by VDB
* a paradigm shift was detected by VDB
* a gene became more important
* a variant became causal
* a mechanism was established
* a disease model was proven
* a reasoning method became biologically superior
* a clinical conclusion changed
* a surface became biologically meaningful

Those are downstream reasoning or scientific interpretation claims.

VDB may preserve such claims if producers assert them.

VDB must not generate them as its own conclusions.

---

# Example: VDB₁ to VDB₂ Through RDGP Re-Entry

Consider an initial VDB generation:

```text
VDB₁
    preserved assertions:
        VAP variant assertions
        GSC semantic prior assertions

    derived layers:
        topology₁
        geometry₁
        surfaces₁
        projections₁
```

VDB emits a governed export:

```text
TEP-VDB₁
```

RDGP consumes this package and emits:

```text
TEP-RDGP₁
```

VDB ingests the RDGP output as new Assertion Records.

The next generation is:

```text
VDB₂
    preserved assertions:
        VAP variant assertions
        GSC semantic prior assertions
        RDGP reasoning assertions

    derived layers:
        topology₂
        geometry₂
        surfaces₂
        projections₂
```

VDB₂ is not VDB₁ with overwritten truth.

VDB₂ is VDB₁ plus later preserved reasoning assertions.

This may create new topology relationships between raw evidence, semantic priors, and reasoning outputs.

It may create reasoning-informed surfaces.

It may create new export projections.

It may also create future refresh obligations.

---

# Example: Longer-Horizon Producer Evolution

Consider a longer scientific horizon.

An early VDB ecosystem may contain:

```text
VAP variant assertions
GSC semantic prior assertions
```

A later ecosystem may add:

```text
RSP transcriptomic assertions
PTN proteomic assertions
spatial context assertions
validation assertions
RDGP reasoning assertions
future multi-omic producer assertions
```

These new producer TEPs may introduce new participants, relationships, evidence strata, modalities, contexts, and epistemic states.

As a result, topology may change in ways that earlier generations could not express.

For example:

```text
A gene that previously appeared only in semantic prior evidence may later participate in transcriptomic, proteomic, validation, and reasoning-output neighborhoods.
```

VDB may expose that the evidence neighborhood expanded.

It must not conclude that the gene is now causal or clinically actionable.

---

# Relationship to Epoch I: Truth Layer

Evidence topology over time depends on Truth Layer preservation.

If VDB overwrote assertions, longitudinal topology would be impossible.

Historical comparison requires stable preserved assertions and generation-aware evidence state.

The Truth Layer makes temporal reconstruction possible.

---

# Relationship to Epoch II: Evidence Geometry

Topology and geometry are derived from Assertion Records.

Because they are derived, they can be rebuilt for each VDB generation.

This allows VDB to compare topology and geometry across generations without modifying historical assertions.

The Evidence Geometry layer makes structural change visible.

---

# Relationship to Epoch III: Discovery Layer

Evidence Convergence Surfaces are generation-aware exposure objects.

A surface may be active in one generation, historical in another, or stale relative to later evidence or method changes.

The Discovery Layer makes generation-specific convergence inspectable.

---

# Relationship to Epoch IV: Projection Layer

Projection makes topology over time usable.

VDB may generate projections such as:

* generation comparison tables
* topology delta reports
* surface emergence reports
* reasoning staleness dashboards
* release-to-release summaries
* producer contribution change views
* longitudinal audit packages
* refresh candidate reports

These projections provide access to temporal topology.

They do not become source truth.

---

# What This Enables

Evidence topology over time enables:

* reconstruction of historical evidence states
* comparison between VDB generations
* audit of when assertions entered VDB
* audit of when convergence became visible
* reasoning refresh detection
* release comparison
* producer method comparison
* longitudinal validation
* scientific-history preservation
* downstream reanalysis
* method evolution tracking
* evidence maturation review

These are infrastructure capabilities.

They support science without replacing scientific interpretation.

---

# What This Prevents

Generation-aware topology helps prevent:

## Historical Amnesia

Earlier evidence states are not overwritten by later interpretations.

## Hidden Staleness

Reasoning outputs are not silently treated as current after evidence or methods change.

## Consensus Overwrite

New consensus does not erase prior evidence states.

## Method Drift Invisibility

Reasoning or producer method changes can be tracked.

## Projection Confusion

A current projection is not confused with a historical projection.

## Destructive Reinterpretation

Later scientific understanding does not rewrite what was originally asserted.

---

# Summary

Evidence topology over time describes how VDB's assertion-derived organization changes across evidence generations and longer scientific-methodological horizons.

The operational cycle is:

```text
Producers
        ↓
TEPs
        ↓
VDB₁
        ↓
TEP-VDB
        ↓
RDGP
        ↓
TEP-RDGP
        ↓
VDB₂
```

VDB₂ is not VDB₁ corrected.

VDB₂ is VDB₁ expanded by later preserved assertions.

At longer timescales, scientific methods, producer capabilities, reasoning systems, and paradigms may change the kinds of assertions VDB receives and the topology dimensions those assertions make possible.

VDB does not evolve biological truth.

It preserves the evolving corpus of scientific truth-claims.

The final doctrine is:

```text
Static topology shows how preserved assertions are organized within one generation.

Longitudinal topology shows how assertion-derived organization changes across generations.

Neither determines biological truth.
```

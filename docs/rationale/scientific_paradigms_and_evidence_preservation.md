# Scientific Paradigms and Evidence Preservation

> We shall not cease from exploration
> And the end of all our exploring
> Will be to arrive where we started
> And know the place for the first time.

- "Little Gidding" of T.S. Eliot's *Four Quartets*

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

This document explains why VDB is designed as an evidence preservation substrate rather than a conclusion store, consensus database, graph database, hypothesis engine, or biological truth adjudicator.

The central claim is:

```text
Scientific interpretation changes over time.

Therefore, scientific infrastructure must preserve evidence in a form that remains usable across paradigm shifts, refutations, reinterpretations, new methods, and future reasoning systems.
```

VDB does not preserve today's interpretation of evidence as final truth.

It preserves evidence so that changing scientific interpretations remain auditable.

---

# Central Rationale

Scientific evidence does not exist in a vacuum.

The same observation may be interpreted differently under different paradigms, methods, ontologies, statistical frameworks, disease models, or biological theories.

A variant may be treated as noise under one framework, regulatory burden under another, network perturbation under another, and developmental timing evidence under another.

A gene may be interpreted as a disease candidate, pathway member, semantic prior, transcriptomic signal, dosage-sensitive locus, modifier, or irrelevant participant depending on the evidence context and scientific question.

If VDB stored only current conclusions, current rankings, current consensus labels, or current graph relationships, it would preserve a historically contingent interpretation rather than the evidence needed for future scientific work.

VDB therefore preserves assertions.

An assertion records who made a scientific statement, about which participants, under what context, using what evidence, with what provenance, and with what epistemic status.

That is the unit most likely to survive scientific change.

---

# Why Scientific Paradigms Matter

Scientific communities do not merely accumulate facts.

They organize observations through conceptual frameworks that influence what counts as signal, anomaly, explanation, mechanism, evidence, or legitimate question.

These frameworks change.

When they do, older evidence may become newly important, newly ambiguous, newly contradicted, or newly interpretable.

A preservation system that stores only the current dominant interpretation risks losing the very context needed to understand how evidence should be reconsidered later.

VDB is designed to survive this instability.

It does so by preserving:

* producer identity
* assertion identity
* participant identity
* evidence basis
* provenance
* context
* epistemic status
* temporal scope
* independence metadata
* lineage
* derived-layer traceability

The goal is not to prevent scientific interpretation.

The goal is to ensure that interpretation remains reconstructable, attributable, and revisable.

---

# Kuhn: Evidence Within Paradigms

Thomas Kuhn's account of scientific paradigms is useful for VDB because it emphasizes that scientific meaning is shaped by the frameworks within which communities work.

A scientific community's paradigm influences which observations appear ordinary, which appear anomalous, which explanations are acceptable, and which questions seem worth asking.

For VDB, the architectural consequence is direct:

```text
VDB must preserve evidence before forcing it into a single paradigm-specific interpretation.
```

This matters because VDB is intended to persist across changes in:

* disease models
* variant interpretation frameworks
* pathway models
* regulatory biology
* population genetics assumptions
* transcriptomic interpretation
* proteomic interpretation
* multi-omic reasoning
* rare disease prioritization
* future biological abstractions not yet defined

A noncoding variant, a semantic prior, a transcriptomic signal, or a proteomic observation may become meaningful only after the scientific framework around it changes.

VDB must therefore preserve evidence in a form that does not depend on today's preferred explanatory model.

---

# VDB Consequence of Kuhn

The Kuhnian consequence for VDB is:

```text
Preserve assertions before interpretation.
Preserve context before consensus.
Preserve disagreement before adjudication.
```

VDB does not collapse producer assertions into a single paradigm.

It allows multiple scientific frameworks to coexist as preserved evidence.

For example:

```text
VAP may assert variant observations.

GSC may assert phenotype-scoped semantic priors.

RSP may assert transcriptomic evidence.

A future proteomics pipeline may assert protein-level evidence.

RDGP may assert downstream reasoning outputs.
```

These assertions may intersect around the same gene, phenotype, variant, pathway, or sample.

VDB preserves them as distinct evidence states.

It does not force them into one interpretation.

Their relationships may later be organized, characterized, exposed, projected, or evaluated by downstream systems.

But the underlying assertions remain preserved.

---

# Popper: Refutation and the Preservation of Counterevidence

Karl Popper's account of scientific inquiry is useful for VDB because it emphasizes that scientific claims must remain exposed to testing, counterevidence, and possible refutation.

A scientific infrastructure that preserves only confirming evidence is not a scientific preservation system.

It is a confirmation archive.

VDB must preserve evidence that complicates, weakens, contradicts, or fails to support current interpretations.

This includes:

* positive evidence
* negative evidence
* null evidence
* conflicting evidence
* uncertain evidence
* deprecated evidence
* low-confidence evidence
* failed validation evidence
* reasoning outputs later challenged by new evidence
* evidence that is meaningful only under future methods

Preserving such evidence is not indecision.

It is scientific discipline.

---

# VDB Consequence of Popper

The Popperian consequence for VDB is:

```text
VDB must preserve evidence states even when they weaken, complicate, or contradict favored interpretations.
```

This supports several VDB architectural commitments:

* assertions are append-only
* historical evidence is not destructively rewritten
* epistemic status is preserved
* uncertainty is preserved
* null and negative states are preservable
* downstream reasoning outputs return as new assertions
* prior evidence is not overwritten by later conclusions
* projection and visualization do not become authority
* evidence conflict is not treated as database failure

A claim may later be challenged.

A reasoning output may later become stale.

A producer method may later be superseded.

A variant interpretation may later change.

VDB must preserve the evidence trail that makes such changes auditable.

---

# T. S. Eliot: New Evidence and the Reordering of Prior Evidence

> We shall not cease from exploration
> And the end of all our exploring
> Will be to arrive where we started
> And know the place for the first time.

- "Little Gidding" of T.S. Eliot's *Four Quartets*

T. S. Eliot's account of tradition and historical relation is useful here by analogy.

A new work does not merely enter a static archive. It can change the perceived relationships among earlier works.

The earlier works are not rewritten, but their arrangement, relevance, and relation to the whole may change.

This maps naturally onto VDB.

A new assertion does not rewrite old assertions, but it may change the topology around them.

For example:

```text
A new proteomic assertion involving POLG does not modify earlier VAP or GSC assertions.

However, it may create a new evidence intersection.

That intersection may alter topology.

The altered topology may produce new geometry.

The new geometry may support new convergence surfaces.

Those surfaces may support new projections or downstream reasoning.
```

The old assertions retain their original identity while the corpus around them has changed.

---

# VDB Consequence of Eliot

The Eliot-like consequence for VDB is:

```text
New evidence may reorder relationships among prior evidence without rewriting prior evidence.
```

This supports VDB's monotonic knowledge model:

```text
new assertion
        ↓
preservation
        ↓
updated topology
        ↓
updated geometry
        ↓
updated surfaces
        ↓
updated projections
        ↓
downstream reasoning
        ↓
new assertions
```

Knowledge expands.

It does not loop backward destructively.

Historical evidence remains historically valid.

Later evidence may change how prior evidence is connected, exposed, projected, or interpreted.

But it does not change what prior evidence originally asserted.

---

# Why Assertions Are Preserved Instead of Conclusions

Conclusions are important.

But conclusions are downstream products of evidence, method, context, and interpretation.

They are historically contingent.

An assertion preserves more fundamental scientific structure:

```text
who
said what
about which participants
under what context
using what evidence
with what provenance
and what epistemic status
```

This is why Assertion Records are the primitive truth objects in VDB.

A conclusion may be preserved if a producer asserts it.

But VDB preserves that conclusion as an assertion made by a producer, not as VDB's own final truth.

For example:

```text
RDGP may assert that a gene is prioritized for a sample.

VDB preserves that prioritization assertion.

VDB does not itself become the prioritizer.
```

This distinction allows reasoning systems to contribute evidence without allowing their outputs to overwrite the substrate.

---

# Why Competing Evidence Must Coexist

Scientific disagreement is not an error condition.

It is often the normal state of active inquiry.

Different producers may disagree because they use different:

* datasets
* methods
* thresholds
* ontologies
* biological assumptions
* statistical models
* phenotype scopes
* temporal scopes
* evidence hierarchies
* validation criteria

VDB must preserve these differences.

If VDB collapses competing evidence into a single label, score, edge, or conclusion, it loses the scientific structure needed to explain why disagreement exists.

The correct VDB behavior is:

```text
preserve competing assertions
preserve their provenance
preserve their context
preserve their epistemic status
allow derived layers to organize relationships
allow downstream systems to reason over them
```

VDB is not less scientific because it avoids adjudication.

It is more scientifically conservative because it preserves the evidence needed for future adjudication.

---

# Why VDB Does Not Adjudicate Scientific Truth

VDB does not determine:

* biological truth
* clinical truth
* pathogenicity
* causality
* mechanism
* therapeutic relevance
* diagnostic relevance
* final gene priority
* final disease model
* final interpretation

Those responsibilities belong to:

* statistical models
* reasoning systems
* expert review
* validation workflows
* clinical interpretation
* scientific communities
* future methods not yet defined

VDB's responsibility is different.

VDB preserves, organizes, exposes, and projects evidence without claiming final meaning.

The boundary can be stated simply:

```text
VDB preserves evidence conditions.
Reasoning systems evaluate evidence conditions.
Scientific communities interpret evidence conditions.
```

---

# Relationship to Epoch I: Truth Layer

Epoch I established that VDB truth means faithful preservation, not biological correctness.

This rationale explains why.

Scientific correctness changes as methods, paradigms, and evidence change.

Faithful preservation is the more stable substrate.

Therefore:

```text
VDB truth is preservation truth.
It is not final biological truth.
```

The Truth Layer exists because scientific infrastructure must preserve what was asserted before deciding what later frameworks will make of it.

---

# Relationship to Epoch II: Evidence Geometry

Epoch II established that preserved assertions can be organized into topology and characterized as geometry.

This rationale explains why those derived layers must remain non-interpretive.

A topology may reveal that evidence is connected.

A geometry may reveal that evidence has structural convergence.

But neither determines what that convergence means.

This matters because future paradigms may interpret the same structure differently.

Therefore:

```text
Topology and geometry organize preserved evidence.
They do not adjudicate its meaning.
```

---

# Relationship to Epoch III: Discovery Layer

Epoch III established Evidence Convergence Surfaces.

Surfaces expose structurally eligible evidence geometry.

They do not reason.

This rationale explains why exposure must remain separate from interpretation.

A convergence surface may identify where evidence currently intersects.

That intersection may be useful for downstream reasoning.

But usefulness is not correctness.

A surface is an opportunity for reasoning, not a reasoning result.

Therefore:

```text
Discovery exposes evidence opportunity.
It does not determine biological meaning.
```

---

# Relationship to Epoch IV: Projection Layer

Epoch IV established that projections create useful views without duplicating truth.

This rationale explains why projections must remain non-authoritative.

Different consumers may need different views of the same evidence:

* audit tables
* dashboards
* export packages
* graph views
* validation reports
* release summaries
* reasoning input packages
* visualization panels

These views are necessary.

But they are historically and operationally contingent.

They must not become truth.

Therefore:

```text
Projection changes representation.
Projection does not change authority.
```

---

# Design Implications

This rationale supports the following VDB design commitments.

## Append-Only Evidence History

Historical evidence should not be destructively rewritten.

New evidence enters as new assertions.

## Assertion Primacy

Assertions are the preserved scientific units from which topology, geometry, surfaces, and projections derive.

## Provenance Preservation

Evidence without producer identity and source lineage cannot support future reinterpretation.

## Context Preservation

Assertions must preserve the context in which they were made.

## Epistemic Status Preservation

Observed, inferred, semantic-prior, validation, null, negative, uncertain, and reasoning-derived evidence states must remain distinguishable.

## Evidence Strata

Raw observations, semantic priors, transcriptomic evidence, proteomic evidence, validation assertions, and reasoning outputs must not collapse into a single support bucket.

## Non-Destructive Derived Layers

Topology, geometry, surfaces, and projections may be recomputed as evidence grows.

They must not overwrite historical assertions.

## Reasoning Re-Entry

Downstream reasoning outputs may re-enter VDB only as new assertions.

They must not modify prior evidence.

## Metadata-Derived Currency

A surface or projection may become stale because evidence, method, transform, generation, or policy changed.

Currency is metadata-derived.

It is not a VDB judgment about biological truth.

## Future Optionality

VDB must remain useful to future scientific paradigms, methods, and mathematical representations.

Preserving assertions makes this possible.

---

# What This Prevents

This rationale explains why VDB avoids several common failure modes.

## Consensus Collapse

A system may preserve only the current best label.

VDB preserves the evidence and context behind competing labels.

## Graph Lock-In

A system may treat a graph representation as the truth.

VDB treats graphs as projections or implementations, not as the evidence substrate.

## Dashboard Authority Drift

A system may treat a dashboard as authoritative because it is easy to access.

VDB treats dashboards as projections.

## Export Authority Drift

A system may treat export packages as source truth.

VDB treats TEP-VDB outputs as transport artifacts generated from governed projections.

## Reasoning Overwrite

A system may allow downstream reasoning to overwrite upstream evidence.

VDB allows reasoning outputs to re-enter only as new assertions.

## Historical Amnesia

A system may update away older evidence states.

VDB preserves historical evidence state so scientific change remains auditable.

---

# Why This Matters for Scientific Infrastructure

Scientific infrastructure should not merely answer today's questions.

It should preserve the conditions under which future questions can be asked.

A rare disease gene prioritization system may need evidence that today appears weak.

A future regulatory model may need variants that today appear uninterpretable.

A future pathway model may reinterpret semantic priors.

A future multi-omic method may connect evidence strata that are currently separate.

A future clinical framework may reinterpret previously uncertain assertions.

If the evidence substrate has already collapsed these states into current conclusions, the future system cannot recover what was lost.

VDB is designed to avoid that loss.

---

# Summary

VDB is built for scientific change.

Kuhn clarifies why evidence must survive paradigm change.

Popper clarifies why evidence must remain available for refutation, contradiction, and uncertainty.

T. S. Eliot clarifies by analogy why new evidence can reorder prior evidence without rewriting it.

Together, these perspectives support a single VDB doctrine:

```text
Preserve evidence before interpretation.
Preserve context before consensus.
Preserve history before replacement.
```

VDB does not preserve today's interpretation as final truth.

It preserves assertions so that future interpretations remain auditable.

That is why VDB is an evidence preservation substrate rather than a conclusion store.

And that is why every later VDB layer must remain derived, traceable, reconstructable, and non-authoritative over the preserved assertion substrate.

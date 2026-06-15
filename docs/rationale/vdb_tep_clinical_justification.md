# VDB Transitional Evidence Product (TEP) Clinical Justification

## Purpose

This document explains why Transitional Evidence Products (TEPs) exist from a clinical discovery perspective and why they may become valuable components of future evidence ecosystems.

The goal is not to justify a particular implementation.

Rather, the goal is to justify the existence of a semantically governed evidence transport architecture capable of preserving biological reasoning while evidence moves between acquisition systems, persistence systems, prioritization systems, and discovery systems.

This document serves as the ecosystem-level clinical justification for TEPs.

Repository-specific TEP clinical justifications may exist as specializations of this broader framework.

---

# Core Motivation

Modern clinical genomics workflows generate large volumes of biological evidence.

Examples include:

* genomic variants
* variant annotations
* phenotype-gene associations
* inheritance observations
* transcriptomic findings
* pathway evidence
* network evidence
* prioritization outputs
* cohort observations

These evidence streams frequently originate from different software systems.

Within the repository ecosystem, examples include:

* VAP-derived variant evidence
* GSC-derived semantic prior evidence
* RSP-derived transcriptomic evidence
* RDGP-derived prioritization evidence

Unfortunately, these evidence streams often remain fragmented across files, databases, software systems, and analytical workflows.

As a result:

* evidence context becomes lost
* provenance becomes difficult to reconstruct
* uncertainty becomes compressed
* explainability degrades
* future re-analysis becomes difficult
* cross-system discovery becomes challenging

TEPs exist to preserve evidence state before these losses occur.

---

# What a TEP Represents

A TEP is not a diagnosis.

A TEP is not a prioritization score.

A TEP is not a machine-learning prediction.

A TEP is not a clinical report.

Instead, a TEP represents:

```text
A semantically rich evidence state
```

preserved in a transportable form.

Different repositories may produce different TEP families.

Examples include:

```text
VAP-TEP
    Variant evidence state

GSC-TEP
    Semantic prior evidence state

RSP-TEP
    Transcriptomic evidence state

RDGP-TEP
    Prioritization evidence state
```

Together these evidence states form a transportable ecosystem of biological reasoning.

Different TEP families are not required to contain identical evidence structures.

Rather, TEPs provide a common transport architecture that permits biologically distinct evidence states to coexist, persist, and participate in discovery workflows while preserving repository-specific semantics.

This allows genomic, transcriptomic, semantic-prior, and prioritization evidence to contribute to shared discovery surfaces without requiring semantic homogenization.

Importantly, TEPs do not merely preserve evidence.

TEPs preserve the reasoning context associated with evidence, including provenance, uncertainty, semantic decomposition, supporting rationale, and evidence topology.

This distinction enables future discovery systems to operate on preserved biological reasoning rather than isolated biological observations.

---

# Clinical Use Case 1 — Cross-Repository Similar Case Discovery

Traditional systems frequently support queries such as:

```text
Find patients with variant X.
```

or:

```text
Find patients with gene Y.
```

A TEP-enabled discovery ecosystem supports richer questions:

```text
Find patients whose evidence state resembles this patient.
```

Evidence similarity may include:

* variant architecture
* phenotype structure
* inheritance patterns
* uncertainty patterns
* transcriptomic evidence
* prioritization context

This enables discovery based upon evidence composition rather than isolated identifiers.

---

# Clinical Use Case 2 — Variant and Semantic-Prior Convergence

Many clinical questions require combining evidence from multiple systems.

Examples include:

```text
Which rare variants occur near genes
that are strongly associated with this phenotype?
```

This requires integration between:

* VAP-derived evidence
* GSC-derived evidence

TEPs preserve these evidence states independently while allowing later convergence within VDB.

This supports biologically meaningful discovery without requiring repeated manual integration.

---

# Clinical Use Case 3 — Variant and Transcriptomic Convergence

Future workflows may combine:

* genomic evidence
* transcriptomic evidence

Clinicians may ask:

```text
Do variants observed in this patient
align with expression abnormalities?
```

or:

```text
Which candidate genes exhibit both
genomic and transcriptomic support?
```

TEPs provide a mechanism for preserving these evidence streams while maintaining provenance and explainability.

---

# Clinical Use Case 4 — Discovery of Oligogenic and Pathway-Centered Disease Architectures

Many diseases may arise from combinations of:

* coding variants
* regulatory variants
* pathway perturbations
* modifier loci
* network-level disruptions

TEPs preserve evidence decomposition in a manner that supports discovery of:

```text
recurrent evidence architectures
```

rather than merely recurrent variants.

This may facilitate future investigation of:

* oligogenic disease models
* pathway-centered disease models
* network-centered disease models
* burden-based disease architectures

across patient populations.

---

# Clinical Use Case 5 — Longitudinal Re-analysis

Biological interpretation evolves continuously.

New disease genes emerge.

New transcriptomic evidence emerges.

New semantic priors emerge.

Because TEPs preserve:

* provenance
* uncertainty
* evidence composition
* supporting rationale

historical cases can be revisited without reconstructing entire analytical workflows.

This supports:

* unresolved case review
* retrospective analysis
* evolving disease-gene discovery
* institutional memory preservation

---

# Clinical Use Case 6 — Explainable Prioritization

Clinical interpretation requires transparency.

A clinician should be able to determine:

* why evidence was considered important
* which systems contributed evidence
* which uncertainties remained unresolved
* which assumptions were made

TEPs preserve reasoning components explicitly.

This supports:

* explainability
* auditability
* reproducibility
* clinical review

while avoiding opaque evidence aggregation.

---

# Clinical Use Case 7 — Hospital-Scale Discovery Systems

Large clinical institutions accumulate evidence over many years.

A mature TEP ecosystem enables questions such as:

```text
Have we observed similar evidence states before?
```

```text
Which unresolved patients resemble this solved patient?
```

```text
Do recurring evidence architectures exist
across disease cohorts?
```

```text
Which transcriptomic patterns repeatedly
co-occur with specific variant architectures?
```

These capabilities become increasingly valuable as institutional evidence repositories grow.

---

# Clinical Use Case 8 — Knowledge Preservation

One of the greatest risks in clinical genomics is loss of reasoning context.

Files remain.

Reports remain.

Variants remain.

However, the rationale underlying interpretation frequently disappears.

TEPs preserve:

* why evidence mattered
* what uncertainty existed
* which evidence systems contributed support
* what assumptions were considered
* what questions remained unresolved

This transforms evidence from a transient analytical artifact into a durable knowledge object.

---

# Clinical Use Case 9 — Reviewability and Candidate Architecture Discovery

Clinical variant interpretation frequently generates reviewable candidate sets whose composition varies across patients.

Examples include:

* clinically supported coding candidates
* clinically supported noncoding candidates
* candidate escalation structures
* reviewability architectures
* validation-ready evidence states

A TEP-enabled discovery ecosystem allows clinicians to ask:

```text
Have we observed similar reviewability structures before?

Which candidate architectures repeatedly
appear among patients with similar manifestations?
```

This enables discovery based upon evidence architecture rather than isolated variants and may facilitate future cohort-scale investigation of reviewability patterns, candidate density patterns, and validation trajectories.

---

# Clinical Use Case 10 — Semantic Prior Reinterpretation

Clinical interpretation often evolves as new disease-gene associations emerge.

A TEP-enabled ecosystem preserves semantic-prior evidence independently of variant evidence.

Clinicians may ask:

```text
Which historical cases would become more interesting
if current semantic-prior knowledge were applied?

Which patients harbor variants near genes that
were not considered clinically relevant at the time
of original analysis?
```

This supports longitudinal reinterpretation without requiring reconstruction of historical acquisition workflows.

---

# Strategic Value

The long-term value of TEPs extends beyond any individual repository.

Unlike producer repositories, VDB is uniquely positioned to observe all TEP families simultaneously.

As a result, VDB can expose discovery surfaces that no individual repository can provide independently.

Cross-repository evidence convergence, longitudinal reinterpretation, similarity discovery, and multi-modal evidence retrieval become possible because VDB operates as the persistence and brokerage layer across all producer-specific TEP families.

A mature evidence ecosystem may eventually transport evidence between:

* acquisition systems
* annotation systems
* transcriptomic systems
* prioritization systems
* persistence systems
* discovery systems

while preserving:

* provenance continuity
* semantic integrity
* uncertainty visibility
* explainability
* future re-analysis value

across repository boundaries.

---

# Core Principle

```text
The purpose of a Transitional Evidence Product
is not merely to move evidence.
```

> The purpose of a Transitional Evidence Product is to preserve biological reasoning while evidence moves between systems.

---

# Ecosystem Principle

```text
VAP preserves variant evidence.

GSC preserves semantic prior evidence.

RSP preserves transcriptomic evidence.

RDGP preserves prioritization evidence.

TEPs preserve transportable evidence states.

VDB preserves and discovers them.
```

---

# Appendix A: TEP Analogs

Examples of related concepts include:

1. GA4GH Phenopackets
2. Matchmaker Exchange
3. Rare-disease phenotype similarity systems

These systems demonstrate the value of structured biological evidence exchange and comparison.

TEPs are not intended to replace these approaches.

Rather, TEPs are positioned as semantically governed evidence-state objects capable of preserving provenance, uncertainty, explainability, and future re-analysis value across heterogeneous evidence systems.

---

# Appendix B: Relationship to Repository-Specific TEP Families

This document defines ecosystem-level clinical justification.

Repository-specific TEP families may define specialized clinical justifications.

Examples include:

```text
RDGP-TEP
    Rare-disease prioritization

VAP-TEP
    Variant evidence transport

GSC-TEP
    Semantic prior transport

RSP-TEP
    Transcriptomic evidence transport
```

These specializations inherit from the broader ecosystem-level rationale defined in this document.

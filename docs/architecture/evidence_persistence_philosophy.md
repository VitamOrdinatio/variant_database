# Evidence Persistence Philosophy

## Purpose

The purpose of VDB is not storage.

The purpose of VDB is preservation.

While storage systems focus on retaining data, VDB focuses on retaining meaning.

The distinction is critical.

A stored artifact may remain accessible while losing the semantic context necessary for future interpretation.

VDB therefore exists to preserve biological evidence in a form that remains traceable, explainable, interoperable, and useful for future discovery.

This document defines the philosophical foundation governing evidence persistence within VDB.

---

## The Central Question

Every persistence system must answer a fundamental question:

```text
What is worth preserving?
```

VDB answers this question differently than conventional data warehouses.

Rather than preserving only final conclusions, summaries, or convenience-oriented views, VDB seeks to preserve evidence structures that enable future biological reasoning.

The goal is not simply to remember what was concluded.

The goal is to preserve why those conclusions were possible.

---

## Preservation Over Compression

VDB adopts preservation as its primary architectural principle.

Compression is useful.

Summarization is useful.

Derived views are useful.

However, these products should emerge from preserved evidence rather than replace preserved evidence.

The ecosystem therefore rejects irreversible semantic reduction when that reduction would prevent future reinterpretation.

Persistence should preserve optionality.

---

## Future Biological Questions

Biological interpretation evolves.

Scientific knowledge evolves.

Clinical knowledge evolves.

Ontology systems evolve.

Evidence sources evolve.

Questions that cannot be asked today may become important tomorrow.

Persistence decisions should therefore optimize for future inquiry rather than present convenience.

A persistence strategy succeeds when future investigators can ask new questions without requiring reconstruction of lost evidence.

---

## Evidence as a Renewable Resource

Evidence should be viewed as a renewable scientific resource.

The same evidence may support multiple interpretations over time.

Examples include:

```text
Variant reinterpretation

Gene-disease reassociation

Ontology refinement

Phenotype expansion

Functional reclassification

Clinical guideline revision
```

Evidence persistence should preserve the possibility of reinterpretation.

The goal is not to preserve a single interpretation.

The goal is to preserve interpretability.

---

## Semantic Preservation

Biological meaning is not limited to individual values.

Meaning also exists within relationships.

Examples include:

```text
Variant ↔ Transcript

Variant ↔ Gene

Gene ↔ Phenotype

Sample ↔ Variant

Release ↔ Semantic Prior
```

VDB therefore preserves semantic structures rather than isolated facts.

Relationships are first-class evidence.

---

## Provenance Preservation

Evidence without provenance becomes difficult to trust.

Every persisted entity should remain traceable to its origin.

This includes:

* source repository
* source package identity
* source artifact identity
* release identity
* execution identity
* transport identity
* namespace-resolution history

The objective is reconstructability.

Future investigators should be able to understand how evidence arrived in its persisted state.

---

## Multiplicity Preservation

Biological evidence frequently exhibits multiplicity.

Examples include:

```text
Multiple transcripts

Multiple annotations

Multiple releases

Multiple evidence sources

Multiple ontology mappings

Multiple interpretations
```

Multiplicity should remain visible.

Persistence should not force biological complexity into artificial singularity.

When multiple valid representations exist, those representations should remain detectable.

---

## Identity Preservation

Identity carries biological meaning.

Source identities therefore possess enduring value.

Examples include:

```text
Variant identifiers

Gene identifiers

Transcript identifiers

Phenotype identifiers

Release identifiers
```

Identity normalization should not erase source identities.

Canonical identities support interoperability, but source identities remain part of the evidence record.

Preservation requires both.

---

## Overlay Preservation

Not all evidence originates from observations.

Some evidence originates from curated biological knowledge.

Examples include:

```text
GSC semantic priors

Phenotype-scoped knowledge

Release-scoped consensus products
```

These artifacts should not be reduced to binary annotations or membership flags.

Their provenance, release history, semantic channels, and scoring context remain meaningful.

VDB therefore treats overlays as first-class evidence.

---

## Noncoding Preservation

Historically, many systems prioritized coding variation while reducing noncoding observations to secondary status.

VDB rejects this distinction.

Noncoding evidence is evidence.

Persistence decisions should preserve:

* regulatory observations
* intronic observations
* intergenic observations
* untranslated-region observations
* future functional annotations

The architecture intentionally avoids assumptions that future biological relevance will be restricted to currently favored evidence classes.

---

## Repository Independence

Evidence persistence should remain independent of repository structure.

Repository ownership should not determine persistence organization.

Likewise:

```text
Repository Ownership
        ≠
Persistence Domain
```

and

```text
Identity Space
        ≠
Persistence Domain
```

Evidence should be organized according to semantic meaning rather than implementation history.

This principle enables long-term interoperability.

---

## Persistence as Stewardship

VDB acts as a steward rather than an owner.

Producer repositories remain authoritative for evidence generation.

Examples include:

```text
VAP
    Observations

GSC
    Semantic Priors

Future RSP
    Functional Evidence
```

VDB preserves, organizes, and exposes evidence.

It does not replace producer authority.

Stewardship therefore becomes the appropriate persistence model.

---

## Persistence and Discovery

Persistence is not an archival activity.

Persistence exists to support discovery.

The value of preserved evidence emerges when future users can:

* query it
* reinterpret it
* compare it
* aggregate it
* enrich it
* reason over it

Persistence should therefore maximize future discoverability.

---

## Historical Reproducibility

Scientific conclusions should remain reproducible.

This requires preservation of historical context.

Examples include:

```text
Historical releases

Historical overlays

Historical provenance

Historical ontology mappings

Historical namespace resolutions
```

A persistence system that preserves only the latest state cannot fully support historical reproducibility.

VDB therefore values historical continuity.

---

## Persistence and Future-Proofing

Future-proofing is not prediction.

Future-proofing is preservation.

VDB does not attempt to predict future scientific discoveries.

Instead, it seeks to preserve sufficient evidence richness that future discoveries can be supported when they occur.

Preservation therefore becomes the primary mechanism of future-proofing.

---

## The Persistence Mission

The mission of VDB can be summarized as follows:

```text
Preserve meaning.

Preserve provenance.

Preserve multiplicity.

Preserve identity.

Preserve interpretability.

Preserve discoverability.

Preserve future utility.
```

These principles collectively define the philosophy of evidence persistence within VDB.

---

## Summary

VDB is not designed to function as a conventional warehouse.

It is designed to function as a semantic persistence system.

Its purpose is not merely to store information, but to preserve biological evidence in a form that remains interpretable, reproducible, interoperable, and useful for future discovery.

Persistence succeeds when future biological questions remain answerable.

That objective governs every architectural persistence decision within VDB.

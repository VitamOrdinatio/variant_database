# vdb_discovery_justification.md

## Purpose

This document explains why the Variant Database (VDB) includes a Discovery Engine.

The Discovery Engine exists because evidence preservation alone is insufficient to support long-term biological reuse, reinterpretation, and integration.

This document describes the architectural rationale for discovery within VDB.

---

# The Fundamental Problem

VDB receives evidence from producer systems.

Examples include:

```text
VAP

GSC

future RSP

future RDGP

future producer systems
```

Producer systems are authoritative for the evidence they generate.

However, producer systems cannot anticipate every future context, interpretation, integration opportunity, or discovery need.

As a result:

```text
preserved evidence
```

and

```text
available evidence
```

are not always identical.

---

# Evidence Preservation Is Necessary But Not Sufficient

Preservation ensures that evidence survives.

Preservation does not automatically ensure that evidence remains maximally useful.

Examples:

```text
missing metadata

missing ontology context

missing registry context

missing cross-domain relationships

future reinterpretation opportunities
```

may remain undiscovered.

The Discovery Engine exists to identify such opportunities.

---

# The Stewardship Principle

VDB is not merely an evidence warehouse.

VDB is an evidence steward.

A warehouse stores what arrives.

A steward evaluates:

```text
what exists

what is missing

what is attachable

what is reusable

what may become useful later
```

The Discovery Engine operationalizes that stewardship role.

---

# Discovery Expands The Evidence Horizon

The central purpose of discovery is to expand the evidence horizon of preserved evidence.

Discovery attempts to identify:

```text
additional context

additional relationships

additional metadata

additional authority sources

future reinterpretation opportunities
```

without altering authoritative producer evidence.

---

# Core Principle

```text
Discovery expands evidence context.

Discovery does not replace evidence authority.
```

Discovery may add information.

Discovery must not rewrite history.

---

# Why Producer TEPs Are Not Enough

Producer TEPs are authoritative transport objects.

They preserve what producers know.

However, producers cannot know every future requirement.

Examples:

```text
VAP knows variants

GSC knows phenotype-gene priors

RSP may know expression signals

RDGP may know reasoning outputs
```

None of these systems necessarily know:

```text
future metadata needs

future ontology needs

future cross-domain relationships

future reinterpretation requirements
```

VDB therefore requires a mechanism for identifying additional evidence context.

---

# Discovery Is Not A Critique Of Producers

The Discovery Engine does not exist because producers are incomplete.

The Discovery Engine exists because future questions evolve.

The architecture assumes:

```text
future biological questions
```

will differ from:

```text
current biological questions
```

Discovery provides a mechanism for adapting preserved evidence to future contexts.

---

# Discovery Classes

VDB discovery activities fall into multiple categories.

---

## Internal Discovery

Internal discovery evaluates evidence already present within VDB.

Examples:

```text
TEPs

artifacts

entities

evidence objects

evidence states
```

Questions include:

```text
What exists?

What relationships exist?

What overlays exist?
```

---

## Cross-Domain Discovery

Cross-domain discovery identifies relationships between evidence domains.

Examples:

```text
VAP ↔ GSC

VAP ↔ RSP

GSC ↔ RDGP

future domain relationships
```

Questions include:

```text
What evidence can be related?

What overlays can be attached?
```

---

## External Evidence Discovery

External discovery identifies contextual evidence outside producer repositories.

Examples:

```text
BioSample metadata

BioProject metadata

registry metadata

ontology metadata
```

Questions include:

```text
What authoritative context is available?

What evidence can be retrieved?
```

---

## Future Reinterpretation Discovery

Future reinterpretation discovery identifies evidence that may gain value as biological knowledge evolves.

Examples:

```text
noncoding variants

regulatory regions

network relationships

future annotations
```

Questions include:

```text
What evidence may become useful later?

What evidence should remain visible?
```

---

# The BioSample Example

Consider a patient processed by VAP.

Conceptually:

```text
FASTQ
        ↓

VAP
        ↓

TEP-VAP
        ↓

VDB
```

VDB may determine that useful contextual metadata is not present.

Examples:

```text
BioSample metadata

BioProject metadata

registry context
```

The Discovery Engine may retrieve that information from an authoritative source.

Conceptually:

```text
TEP-VAP
        ↓

Discovery Event
        ↓

External Evidence Capsule
        ↓

Overlay Attachment
```

The original TEP remains unchanged.

The newly discovered evidence remains independently attributable.

---

# Discovery And Authority

Discovery must never obscure authority.

Every discovered artifact must preserve:

```text
authority source

retrieval timestamp

retrieval method

record identity

snapshot identity
```

Discovery must remain auditable.

---

# Discovery And Preservation

Discovery must not overwrite preserved evidence.

Examples of prohibited behavior include:

```text
rewriting producer metadata

overwriting producer identities

silently replacing values

silently promoting inferred values
```

Discovery augments preserved evidence.

Discovery does not replace preserved evidence.

---

# Discovery And External Evidence Capsules

Discovered evidence should enter VDB through governed structures.

Examples:

```text
BioSample capsule

BioProject capsule

ontology capsule

registry capsule
```

External evidence must remain distinguishable from producer evidence.

---

# Discovery Lifecycle

Discovery should remain a governed process.

Conceptually:

```text
discover
        ↓

profile
        ↓

classify
        ↓

validate
        ↓

attach
        ↓

ingest
        ↓

index
```

These steps remain distinct.

Discovery must not bypass validation.

---

# Discovery And Future Biology

Many future biological questions cannot be anticipated today.

Examples include:

```text
poly-noncoding burden

future regulatory models

AlphaGenome-style reinterpretation

cross-modal convergence

network convergence

future disease models
```

Discovery enables VDB to revisit preserved evidence as biological understanding evolves.

---

# Discovery And Reinterpretation

Future scientific progress may transform previously uninformative evidence into informative evidence.

Examples:

```text
unknown noncoding variants

weak pathway relationships

incomplete ontology mappings

partial metadata
```

may become biologically meaningful.

Discovery provides a mechanism for identifying such opportunities.

---

# Discovery And Query Surfaces

Discovery alone is insufficient.

Discovered evidence must also become retrievable.

Query Surfaces provide the mechanism through which discovered evidence becomes visible to consumers.

Conceptually:

```text
Discovery
        ↓

Persistence
        ↓

Query Surface
        ↓

Consumer
```

---

# Anti-Pattern: Silent Enrichment

One of the primary architectural risks is silent enrichment.

Example:

```text
external metadata discovered

metadata attached

metadata appears as if producer supplied it
```

This is prohibited.

Discovery provenance must remain visible.

Discovery authority must remain visible.

Discovery lineage must remain visible.

---

# Architectural Benefits

The Discovery Engine enables:

```text
context expansion

future reinterpretation

cross-domain integration

metadata enrichment

authority-aware augmentation

query-surface expansion

evidence reuse
```

while preserving evidence integrity.

---

# Design Principle

The central design principle of discovery is:

```text
Preserved evidence should remain useful
even as biological knowledge evolves.
```

---

# Conclusion

The Discovery Engine exists because future biological questions cannot be fully anticipated by current producer systems.

Preservation ensures evidence survives.

Discovery ensures evidence remains reusable.

The purpose of discovery is not to modify producer evidence.

The purpose of discovery is to identify additional context, relationships, and opportunities while preserving authority, provenance, identity, and reconstructability.

The guiding principle is:

```text
Discover broadly.

Preserve authority.

Never rewrite the evidence.
```

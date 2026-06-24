# data_schema.md

## Purpose

The VDB Data Schema defines the biological evidence domains preserved within the Variant Database (VDB).

The Data Schema specifies:

```text
what evidence classes exist
what biological substrates are preserved
what evidence domains are recognized
what semantic obligations apply
```

The Data Schema does not define:

```text
database tables
storage engines
indexes
query execution
lineage relationships
```

Those concerns belong to later schema layers.

The purpose of the Data Schema is to ensure that biological evidence remains available for future interpretation, discovery, reanalysis, and integration.

---

# Scope

The Data Schema governs:

```text
variant evidence
gene evidence
phenotype evidence
semantic-prior evidence
interpretation evidence
validation evidence
reasoning evidence
future biological evidence
```

The Data Schema applies to:

```text
VAP
GSC
RSP
RDGP
future producer repositories
```

---

# Relationship To Metadata And Provenance

## Metadata

Metadata answers:

```text
What evidence object exists?
```

Defined in:

```text
metadata_schema.md
```

---

## Provenance

Provenance answers:

```text
How did evidence come into existence?
```

Defined in:

```text
provenance_schema.md
```

---

## Data

Data answers:

```text
What biological evidence is being preserved?
```

Defined here.

---

# Design Principles

## Preservation Before Utility

The VDB Data Schema prioritizes preservation.

Evidence should not be discarded solely because:

```text
it lacks annotation
it lacks immediate utility
it lacks current biological interpretation
```

Future tools may extract meaning from currently uninterpretable evidence.

---

## Biological Substrate Preservation

The primary preservation target is the biological substrate.

Examples:

```text
observed variants
observed transcripts
observed expression changes
semantic priors
source contributions
reasoning outputs
```

Interpretation layers are important.

Underlying biological substrates are more important.

---

## Interpretation Is Not Preservation

Interpretations may change.

Observed evidence remains valuable.

VDB therefore preserves:

```text
evidence
and
interpretation
```

as distinct concepts.

---

## Future Reanalysis Enablement

Evidence should remain usable by:

```text
future annotation systems
future regulatory models
future ontology systems
future prioritization systems
future reasoning systems
```

including systems not yet known at the time of ingestion.

---

## Producer Diversity

The Data Schema must support:

```text
sample-centric evidence
phenotype-centric evidence
gene-centric evidence
transcript-centric evidence
reasoning-centric evidence
```

without forcing them into a common biological model.

---

# Evidence Family Model

The Data Schema organizes biological evidence into Evidence Families.

An Evidence Family represents a coherent biological domain.

Examples:

```text
Variant Observation
Semantic Prior
Transcriptomic Observation
Reasoning Output
```

Evidence Families are preservation units.

They are not database tables.

---

# VAP Evidence Domains

## Variant Observation Domain

Represents observed variants.

Examples:

```text
SNVs
indels
structural variants
future variant classes
```

Preservation obligations:

```text
coordinates
alleles
genotypes
quality state
sample identity
```

Variant observations must remain reconstructable.

---

## Variant Normalization Domain

Represents normalized variant representations.

Examples:

```text
transcript mappings
canonical consequences
normalized coordinates
```

Normalization must not replace observations.

Observation and normalization remain distinct domains.

---

## Routing Domain

Represents classification and routing state.

Examples:

```text
coding
noncoding
clinical routing
exploratory routing
```

Routing remains evidence context.

Routing does not replace observations.

---

## Coding Interpretation Domain

Represents coding-region interpretation outputs.

Examples:

```text
functional consequence
protein impact
coding annotation
```

Coding interpretation remains separate from observations.

---

## Noncoding Interpretation Domain

Represents noncoding interpretation outputs.

Examples:

```text
regulatory annotations
promoter annotations
enhancer annotations
future AlphaGenome outputs
```

Noncoding interpretation must remain extensible.

Lack of annotation is not evidence of lack of importance.

---

## Prioritization Domain

Represents prioritization overlays.

Examples:

```text
candidate ranking
priority tier
selection status
```

Prioritization does not replace evidence.

Prioritization is an overlay.

---

## Validation Domain

Represents validation-oriented evidence.

Examples:

```text
candidate validation sets
quality-control evidence
benchmark evidence
```

Validation remains separate from prioritization.

---

## Context Domain

Represents contextual summaries.

Examples:

```text
run summaries
execution context
interpretive context
```

Context supports understanding.

Context does not replace evidence.

---

# GSC Evidence Domains

## Phenotype Domain

Represents phenotype-scoped context.

Examples:

```text
epilepsy
mitochondrial disease
future phenotypes
```

Phenotype context must remain visible.

---

## Semantic Prior Domain

Represents phenotype-gene semantic priors.

Examples:

```text
SCN1A epilepsy prior
POLG mitochondrial prior
```

Semantic priors are first-class evidence objects.

---

## Gene Identity Domain

Represents gene identity structures.

Examples:

```text
gene_id
gene_symbol
gene_namespace
mapping state
```

Gene identity must remain preserved independently from scores.

---

## Scoring Domain

Represents scoring outputs.

Examples:

```text
consensus score
semantic score
weighted contribution score
```

Scores are preserved.

Scores are not sufficient preservation units.

---

## Semantic Channel Domain

Represents evidence decomposition.

Examples:

```text
direct disease evidence
clinical interpretation
contextual biology
utilization
exploratory support
```

Channel structure must remain reconstructable.

---

## Source Contribution Domain

Represents evidence contribution topology.

Examples:

```text
GTR contribution
MitoCarta contribution
EPI25 contribution
```

Contribution topology must remain preserved.

Gene-plus-score collapse is prohibited.

---

## Uncertainty Domain

Represents uncertainty state.

Examples:

```text
mapping uncertainty
source uncertainty
null states
```

Uncertainty must remain explicit.

---

# Future Evidence Domains

The Data Schema anticipates future producer repositories.

Examples:

```text
transcriptomic evidence
proteomic evidence
metabolomic evidence
network evidence
clinical evidence
reasoning evidence
```

New evidence domains may be added.

Existing evidence domains must remain valid.

---

# Identity Brokerage Concepts

Cross-domain evidence integration requires identity brokerage.

Identity brokerage does not alter biological evidence.

Identity brokerage enables relationships between evidence domains while preserving source identities.

Examples:

```text
gene identity brokerage

variant identity brokerage

phenotype identity brokerage

locus identity brokerage
```

Identity brokerage is implemented by the Namespace Brokerage Layer defined within the Relational Schema.

---

# Cross-Domain Biological Concepts

The Data Schema recognizes several cross-domain concepts.

These are conceptual bridges.

They are not relational joins.

---

## Variant-Gene Relationship

Represents relationships between:

```text
variant evidence
gene evidence
```

May originate from:

```text
coding overlap
regulatory association
future biological models
```

---

## Sample-Gene Relationship

Represents relationships between:

```text
sample evidence
gene evidence
```

Used by downstream systems such as RDGP.

---

## Phenotype-Gene Relationship

Represents relationships between:

```text
phenotype evidence
gene evidence
```

Primary preservation target of GSC.

---

## Variant-Locus Relationship

Represents relationships between:

```text
variant evidence
genomic intervals
```

Supports future regulatory interpretation.

---

## Noncoding Proximity Relationship

Represents relationships between:

```text
noncoding variants
candidate genes
candidate loci
regulatory intervals
```

This relationship is intentionally future-facing.

Preservation of noncoding evidence exists partly to support future discovery workflows.

---

# Null And Absence Semantics

The absence of annotation is not equivalent to biological irrelevance.

Examples:

```text
unknown consequence
unknown regulatory role
unknown phenotype association
```

must remain distinguishable from:

```text
negative evidence
excluded evidence
failed evidence
```

Null states must remain explicit.

---

# Anti-Collapse Rules

## Observation Collapse Prohibited

Observed evidence may not be replaced solely by interpreted evidence.

---

## Interpretation Collapse Prohibited

Interpretation layers may not overwrite observations.

---

## Prioritization Collapse Prohibited

Candidate ranking may not replace underlying evidence.

---

## Semantic Prior Collapse Prohibited

Phenotype-gene semantic priors may not be reduced to:

```text
gene
score
```

alone.

---

## Noncoding Collapse Prohibited

Noncoding evidence may not be discarded solely because:

```text
annotation is absent
current utility is unknown
```

---

## Future Utility Collapse Prohibited

Evidence may not be removed solely because a present-day consumer does not use it.

---

# Required Data Invariants

## Invariant 1

Observed biological evidence remains preservable.

---

## Invariant 2

Interpretations remain distinguishable from observations.

---

## Invariant 3

Scores remain distinguishable from evidence.

---

## Invariant 4

Source contribution topology remains preservable.

---

## Invariant 5

Uncertainty remains preservable.

---

## Invariant 6

Noncoding evidence remains preservable.

---

## Invariant 7

Future biological reinterpretation remains possible.

---

# Relationship To Relational Schema

The Data Schema defines:

```text
what biological evidence domains exist
```

The Relational Schema defines:

```text
how those domains are represented in persistence structures
```

The Relational Schema must be derived from the Data Schema.

The Data Schema must not be constrained by a specific relational implementation.

---

# Relationship To Discovery Schema

The Discovery Schema determines how evidence domains are located and explored.

The Discovery Schema must preserve the distinctions established by the Data Schema.

Discovery convenience must never justify biological information loss.

---

# Relationship To RDGP Query Surfaces

RDGP consumes evidence domains exposed by VDB.

The Data Schema therefore serves as the biological substrate layer upon which future query surfaces are constructed.

Preservation remains primary.

Queryability remains secondary.

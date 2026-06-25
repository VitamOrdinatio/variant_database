# evidence_assertion_registration_model.md

## Purpose

This document defines the Evidence Assertion Registration Model for VDB.

The purpose of this model is to clarify the relationship between producer-emitted evidence, VDB custody, and Discovery Engine operation.

This model identifies Assertion Registration as a core VDB architectural primitive.

---

# Core Principle

```text
Producer owns assertions.

VDB owns registrations.

Discovery Engine owns relationships among registrations.
```

This principle separates producer authority from VDB stewardship.

VDB does not rewrite producer assertions.

VDB registers assertions into a preserved, traceable, discoverable knowledge topology.

---

# Evidence Assertion

An Evidence Assertion is a provenance-bound statement emitted by a producer regarding one or more biological identities.

An Evidence Assertion is not simply a file, row, artifact, or score.

An Evidence Assertion expresses that a producer has made a statement about evidence under a specific context.

Examples:

```text
VAP asserts that sample HG002 contains variant evidence affecting POLG.

GSC asserts that POLG has phenotype-scoped semantic support for mitochondrial disease.

Future RSP may assert that POLG shows expression evidence in a sample or condition.
```

The assertion belongs to the producer.

VDB preserves the assertion but does not become its originator.

---

# Assertion Registration

An Assertion Registration is VDB's custody record for a producer-emitted Evidence Assertion.

Assertion Registration is the act by which VDB admits a producer assertion into its knowledge topology while preserving:

```text
producer identity
source artifact identity
source evidence surface
biological participants
assertion relationship
supporting context
provenance
authority
uncertainty
reconstruction handles
```

Assertion Registration is not biological interpretation.

Assertion Registration is not truth adjudication.

Assertion Registration is not namespace resolution.

Assertion Registration is the durable VDB record that a producer assertion exists and can participate in downstream discovery.

---

# Assertion Versus Registration

The distinction between assertion and registration is mandatory.

```text
Evidence Assertion
    producer-emitted statement

Assertion Registration
    VDB custody record for that statement
```

The assertion remains producer-owned.

The registration becomes VDB-owned.

This distinction prevents VDB from silently converting producer evidence into VDB-authored biological conclusions.

---

# What An Assertion Is Not

An Evidence Assertion is not an observation alone.

For example:

```text
chr15
89333596
T
TTGC
```

is an observation.

It becomes part of an assertion only when a producer states something about it within a context.

---

An Evidence Assertion is not a biological truth.

For example:

```text
POLG is causal.
```

is not treated as truth by VDB.

VDB may preserve that a producer made such a claim, if a producer did so, but VDB does not convert it into truth.

---

An Evidence Assertion is not merely an interpretation.

Interpretations may be contained within assertions, but an assertion is broader because it includes:

```text
who asserted it
what was asserted
which identities participated
which artifact supported it
which run produced it
which context governed it
```

---

# Conceptual Tuple

An Evidence Assertion can be modeled conceptually as:

```text
Producer
    asserts
Relationship
    among
Biological Identities
    supported by
Evidence Surface / Artifact
    under
Provenance and Context
```

This tuple is conceptual.

It does not require a specific physical database layout.

---

# Producer Examples

## VAP

A VAP assertion may involve:

```text
sample
variant
gene
interpretation context
run provenance
```

Example:

```text
VAP asserts that HG002 contains coding variant evidence involving POLG,
supported by stage_09_coding_interpreted.tsv, under run_2026_06_03_010030.
```

---

## GSC

A GSC assertion may involve:

```text
phenotype
gene
semantic support
source contribution context
run provenance
```

Example:

```text
GSC asserts that POLG has phenotype-scoped semantic support for mitochondrial disease,
supported by a GSC semantic consensus TEP.
```

---

## Future RSP

An RSP assertion may involve:

```text
sample or condition
gene
expression state
analysis context
run provenance
```

Example:

```text
RSP asserts that POLG has expression evidence under a sample or condition,
supported by an RNA-seq evidence surface.
```

---

# Producer-Native Identity Spaces

VDB must preserve producer-native identity spaces.

No single biological identity axis is universal across the ecosystem.

Examples:

```text
VAP
    primary identity space:
        sample_id × variant_id

GSC
    primary identity space:
        phenotype × gene_id

RDGP
    primary identity space:
        sample_id × gene_id

VDB
    primary identity space:
        multi-identity evidence brokerage
```

VDB must not force all producer assertions into a gene-centered, variant-centered, sample-centered, or phenotype-centered model.

Instead, VDB registers the identities that each producer emits and preserves the relationships among those identity spaces.

---

# VAP Identity Preservation

VAP assertions are variant-centered.

For VAP, the core participant identity is:

```text
sample_id × variant_id
```

Gene identity may be present.

Gene identity may be absent.

Gene identity may describe coding context, transcript context, annotation context, nearest-gene context, regulatory context, or candidate association context.

VDB must not require gene identity for VAP assertion registration.

A VAP noncoding variant without gene annotation must remain fully discoverable.

This is required because future biological interpretation may reveal noncoding mechanisms that are invisible to current annotation systems, including:

```text
distal regulatory effects
noncoding RNA disruption
enhancer or promoter effects
transcriptional assembly effects
chromatin or topology effects
patient-enriched noncoding burden
```

Absence of gene annotation must not reduce evidence preservation or discoverability.

---

# Participant Discovery Doctrine

Assertion Participant Discovery must preserve producer-native participants.

For VAP row-level assertions, participant discovery should prioritize:

```text
sample identity
variant identity
```

and attach optional identities only when present, including:

```text
gene
transcript
feature
phenotype
regulatory element
external annotation
```

For GSC assertions, participant discovery may prioritize:

```text
phenotype
gene
```

For RDGP assertions, participant discovery may prioritize:

```text
sample
gene
reasoning output context
```

The participant model must support all of these without redesign.

---

# No Gene-Gating Rule

No VAP assertion registration may require a gene participant.

No VAP variant may be discarded, downgraded, hidden, or made less discoverable because gene identity is absent.

Gene identity is an optional participant for VAP.

Variant identity is primary.

Sample identity is required when available from package or row context.

---

# Surface Exposure Principle

VDB exposes evidence surfaces.

RDGP and other downstream analytical systems reason over those exposed surfaces.

VDB must preserve and expose producer-emitted substrates without requiring VDB to perform the analytical reasoning itself.

TEP-RDGP outputs must re-enter VDB as producer-emitted assertion streams.

Once ingested, TEP-RDGP assertions should participate in the same registration, identity attachment, discovery, overlay, and query-surface processes as TEP-VAP, TEP-GSC, and future TEP-RSP.

Some evidence surfaces may emerge only after downstream reasoning has occurred and returned to VDB as new TEPs.

VDB must therefore preserve identity spaces broadly enough to support future emergent surfaces that are not visible at initial VAP, GSC, or RSP ingestion time.

---

# Assertion Participants

An Assertion Registration may reference one or more biological participants.

Examples include:

```text
sample
gene
variant
phenotype
transcript
condition
pathway
external authority record
```

Participants must preserve source identity.

Canonical identity may be attached later through namespace governance.

Source identity must not be replaced by canonical identity.

---

# Assertion Relationship

An Assertion Registration must preserve the producer-emitted relationship type.

Examples include:

```text
variant observed in sample
variant interpreted against gene
gene prioritized for sample
gene semantically supported for phenotype
gene expression altered in condition
external metadata attached to sample
```

Relationship type describes what the producer assertion says.

It does not determine whether the assertion is biologically true.

---

# Assertion Support

An Assertion Registration must preserve support references.

Support may include:

```text
source artifact
source evidence surface
source row or record reference
source TEP package
source run
source producer
source manifest
```

Support references are required for reconstruction.

---

# Assertion Authority

An Assertion Registration must preserve authority context.

Examples include:

```text
producer-emitted
adapter-resolved
externally sourced
derived by VDB
returned by downstream consumer
```

Authority must remain visible.

Authority collapse is prohibited.

---

# Assertion Uncertainty

An Assertion Registration must preserve uncertainty context.

Examples include:

```text
unknown
missing
not evaluated
ambiguous
conflicted
source asserted
derived
validated
development fixture
```

Uncertainty must not be hidden or converted into absence.

---

# Assertion Registration And Evidence Objects

Evidence Objects may be derived from Assertion Registrations or may participate in their implementation.

However, Assertion Registration is the more fundamental architectural primitive.

Evidence Objects represent preserved evidence units.

Assertion Registrations represent producer statements admitted into VDB custody.

Implementation may evolve, but the distinction must remain visible.

---

# Source Identity And Canonical Identity

Assertion Registrations preserve source identities first.

A source identity is a producer-emitted or producer-derived identity string attached to an Assertion Registration.

Examples include:

```text
HG002
POLG
ENSG00000140521
mitochondrial disease
```

Source identities remain producer-owned.

VDB must not overwrite source identities during canonical identity attachment.

---

# Canonical Identity Attachment

A Canonical Identity Attachment is a VDB-governed record that connects a preserved source identity to a candidate or accepted canonical identity.

Canonical attachment is additive.

Canonical attachment must not replace source identity.

Conceptually:

```text
Source Identity
    remains unchanged

Canonical Identity Attachment
    points from source identity to canonical identity

Namespace Event
    records how the attachment was made

Identity Bridge
    may later connect multiple source identities through shared canonical attachment
```

---

# Identity Ownership Principle

```text
Producer owns source identity.

VDB owns canonical attachment.

Namespace governance owns bridge status.
```

This mirrors the assertion registration principle:

```text
Producer owns assertions.

VDB owns registrations.

Discovery Engine owns relationships among registrations.
```

---

# No-Collapse Identity Ladder

Namespace brokerage must preserve the following identity ladder:

```text
Source Identity
    producer-emitted identity string or identifier

Canonical Identity Attachment
    VDB-governed attachment to a candidate or accepted canonical identity

Namespace Event
    provenance record explaining how and why attachment occurred

Identity Bridge
    relationship connecting source identities through canonical identity
```

Each layer adds one claim.

No layer replaces the layer below it.

---

# Resolution Status

Canonical identity attachment must preserve resolution status.

Examples include:

```text
not_evaluated
source_asserted
exact
alias_resolved
deprecated_resolved
ambiguous
conflicted
unresolved
```

Initial implementation may use a narrow subset such as:

```text
source_asserted
not_evaluated
```

until external authority lookup or richer namespace governance is implemented.

---

# Example: VAP Gene Identity

A VAP Assertion Registration may contain source identities such as:

```text
source_value: POLG
source_namespace: vap_gene_symbol
identity_kind: gene
```

and:

```text
source_value: ENSG00000140521
source_namespace: vap_ensembl_gene_id
identity_kind: gene
```

VDB may attach:

```text
canonical_value: ENSG00000140521
canonical_namespace: ensembl_gene_id
resolution_status: source_asserted
resolution_method: producer_supplied_identifier
```

The source identities remain unchanged.

---

# Example: GSC Gene Identity

A GSC Assertion Registration may contain source identities such as:

```text
source_value: POLG
source_namespace: gsc_gene_symbol
identity_kind: gene
```

and:

```text
source_value: ENSG00000140521
source_namespace: gsc_ensembl_gene_id
identity_kind: gene
```

VDB may attach the same canonical identity:

```text
canonical_value: ENSG00000140521
canonical_namespace: ensembl_gene_id
resolution_status: source_asserted
resolution_method: producer_supplied_identifier
```

A future Identity Bridge may connect the VAP and GSC source identities through the shared canonical identity.

The bridge emerges from preserved attachments.

It is not created by replacing either source identity.

---

# Operational Requirements

Canonical identity attachment must preserve:

```text
source_identity_id
source_value
source_namespace
identity_kind
participant_role
producer context
canonical_value
canonical_namespace
resolution_status
resolution_method
resolution_provenance
namespace_event_id when available
```

Canonical attachment must allow:

```text
multiple canonical candidates
ambiguous mappings
conflicted mappings
unresolved mappings
source-asserted mappings
future authority-verified mappings
```

---

# Anti-Collapse Identity Rules

The following are prohibited:

```text
replacing source identity with canonical identity
treating source assertion as authority-verified resolution
collapsing producer-specific namespaces
collapsing POLG into POLG2 by text similarity
hiding ambiguous mappings
hiding conflicted mappings
removing source identity after bridge creation
```

Identity preservation takes precedence over convenience.

---

# Discovery Implication

The Discovery Engine should operate over preserved source identities and canonical attachments.

It should ask:

```text
Which source identities exist?

Which canonical identities are attached?

Under what authority?

With what status?

Which source identities can be bridged through shared canonical attachments?
```

It should not ask:

```text
What did this identity become?
```

Source identity never becomes canonical identity.

Canonical identity is attached, governed, and reconstructable.

---

# Relationship To Discovery Engine

The Discovery Engine operates on Assertion Registrations.

It does not discover relationships among files.

It discovers relationships among registered assertions.

Discovery examples:

```text
VAP assertion references POLG.

GSC assertion references POLG.

RSP assertion references POLG.

Discovery Engine identifies a cross-producer convergence point.
```

The Discovery Engine creates discoverable knowledge topology by connecting registrations through identity, provenance, evidence surface, and context.

---

# Knowledge Topology

VDB knowledge topology emerges from registered assertions and their relationships.

The topology is not equivalent to the producer file tree.

Producer TEPs provide transport topology.

VDB registration creates knowledge topology.

Discovery connects knowledge topology.

Query surfaces expose selected portions of knowledge topology.

---

# Conceptual Flow

```text
Producer
    ↓
Evidence Assertion
    ↓
Assertion Registration
    ↓
Knowledge Topology
    ↓
Discovery Engine
    ↓
Query Surfaces
```

Each layer adds one responsibility.

The producer emits.

VDB registers.

The Discovery Engine relates.

Query surfaces expose.

---

# Anti-Collapse Rules

The assertion registration model prohibits:

```text
collapsing assertion into truth
collapsing source identity into canonical identity
collapsing producer assertion into VDB interpretation
collapsing artifact inventory into knowledge topology
collapsing observation into assertion
collapsing registration into query output
collapsing uncertainty into absence
```

Preservation takes precedence over convenience.

---

# Development Implications

Phase 3 implementation should focus on Assertion Registration, not biological interpretation.

Initial implementation should:

```text
classify evidence surfaces
identify candidate assertion-bearing artifacts
create registration records
preserve source identity
preserve source support
preserve provenance handles
avoid row-level biological interpretation unless explicitly scoped
```

The implementation should remain producer-agnostic.

The initial benchmark may use HG002 TEP-VAP, but abstractions must remain compatible with GSC TEPs and future producers.

---

# Summary

Evidence Assertion Registration is the inner core of VDB.

It defines the point where producer-emitted evidence enters VDB-managed knowledge topology.

The guiding principle is:

```text
Do not claim truth.

Do not rewrite producers.

Register assertions.

Preserve context.

Let discovery emerge from relationships.
```

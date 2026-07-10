# Scientific Evidence Preservation Principles

This document is part of the architectural epoch: **Truth Layer**

| Epoch | Epoch Identity    | Epoch Purpose |
| ----- | ----------------- | ------------- |
| I     | **Truth Layer**       | **What is truth? What must be preserved? What are the limits of knowledge? How does information flow?** |
| II    | Evidence Geometry | Once assertions exist, how do they organize into biological knowledge? |
| III   | Discovery Layer   | How do preserved evidence topologies become discoverable? |
| IV    | Projection Layer  | How does one truth generate many useful views without duplication? |
| V     | Rationale Layer   | Why do we do this? |

---

## Epoch I: Truth Layer

```text
Truth Layer Philosophy
        ↓
Scientific Evidence Preservation Principles <-THIS DOC
        ↓
Evidence Persistence Philosophy
        ↓
Epistemic Boundaries
        ↓
Knowledge Flow Philosophy
```

See also:
- [Truth Layer Philosophy](./truth_layer_philosophy.md)
- [Scientific Evidence Preservation Principles](./scientific_evidence_preservation_principles.md)
- [Evidence Persistence Philosophy](./evidence_persistence_philosophy.md)
- [Epistemic Boundaries](./epistemic_boundaries.md)
- [Knowledge Flow Philosophy](./knowledge_flow_philosophy.md)

---

## Purpose

This document defines the architectural preservation principles that govern the Variant Database (VDB).

The Truth Layer Philosophy establishes what truth means within VDB. This document establishes what scientific information must remain preserved so that truth can remain reconstructable, interpretable, and useful for future discovery.

These principles apply to every design, specification, schema, interface, query surface, projection, and implementation within VDB.

---

# Governing Principle

Every transformation performed by VDB must preserve the scientific information necessary for future investigators to faithfully reconstruct the original evidence statement.

Storage may change.

Representations may change.

Projection methods may change.

Reasoning systems may change.

The preserved scientific meaning must remain recoverable.

---

# Principle 1: Preserve Meaning

VDB must preserve what the producer asserted.

An evidence record is not preserved if its values remain stored but its scientific meaning becomes ambiguous, altered, or unrecoverable.

Preserving meaning requires that VDB retain enough structure to distinguish:

* what was asserted
* who asserted it
* what entities participated
* what evidence supported it
* under what context it was valid
* what epistemic status it carried

VDB must not preserve data in a way that silently changes the scientific statement.

---

# Principle 2: Preserve Identity

Scientific participants must remain identifiable.

Participants may include:

* samples
* variants
* genes
* transcripts
* phenotypes
* conditions
* publications
* sources
* cohorts
* environmental factors
* viruses
* pathways
* future evidence entities

VDB may later attach canonical identities, broker namespaces, or construct cross-producer mappings.

These operations must not erase producer-native identities.

Identity normalization supports interoperability.

Identity preservation protects evidence.

Both are required.

---

# Principle 3: Preserve Provenance

Evidence without provenance cannot be fully trusted, reconstructed, or reinterpreted.

VDB must preserve chain-of-custody information for every registered assertion and derived product where available.

Provenance includes origin, transport, artifact, version, execution, and source-record context.

Future investigators must be able to ask:

* where did this evidence come from?
* which producer emitted it?
* which artifact contained it?
* which run generated it?
* which release or version governed it?
* which source record supported it?
* how did it enter VDB?

If those questions cannot be answered, preservation is incomplete.

---

# Principle 4: Preserve Context

Scientific evidence is bounded by context.

A statement observed in one sample, phenotype, tissue, contrast, cohort, pipeline run, or resource release must not silently become a general biological claim.

VDB must preserve the biological, technical, phenotypic, experimental, temporal, and computational context necessary to interpret an assertion.

Context prevents evidence from being overgeneralized.

Context also allows future investigators to determine whether an assertion applies to a new question.

---

# Principle 5: Preserve Epistemic Status

Not all scientific statements represent the same kind of knowledge.

An observed variant call, an annotation, a semantic prior, a derived projection, a statistical inference, and a hypothesis are different epistemic objects.

VDB must preserve epistemic status so that downstream systems can distinguish:

* observed evidence
* annotated evidence
* asserted evidence
* derived evidence
* inferred evidence
* brokered evidence
* projected evidence
* hypothesized evidence

VDB must not silently promote weak evidence into strong evidence or transform an inference into an observation.

---

# Principle 6: Preserve Evidence Independence

Multiple records do not necessarily represent multiple independent observations.

Several assertions may derive from:

* the same publication
* the same database release
* the same pipeline run
* the same source adapter
* the same cohort
* the same sample
* the same upstream annotation resource

VDB must preserve evidence-independence information where available.

This principle is essential for downstream statistical reasoning, evidence weighting, Bayesian integration, and assessment of convergence.

Ten records from one evidence origin are not equivalent to ten independent witnesses.

---

# Principle 7: Preserve Time and Version Context

Scientific evidence exists within time.

A statement made under one resource release, ontology version, genome build, software version, or clinical knowledge state may be interpreted differently later.

VDB must preserve time and version context where available.

Historical context enables:

* reproducibility
* reinterpretation
* comparison across releases
* longitudinal evidence topology
* recognition of changing scientific understanding

Preserving only the latest state is insufficient.

---

# Principle 8: Preserve Producer Authority

Producer repositories remain authoritative for the evidence they generate.

VDB is a steward, not the author, of producer evidence.

VDB must preserve producer authority by retaining the identity of the producer and the original form of the assertion as emitted or represented through its transport artifacts.

VDB may organize producer evidence.

VDB may project producer evidence.

VDB may expose convergence among producer evidence.

VDB may not replace producer authority with VDB authority.

---

# Principle 9: Preserve Multiplicity

Biological evidence frequently admits multiple valid representations.

Examples include:

* multiple transcripts
* multiple annotations
* multiple source identifiers
* multiple phenotype mappings
* multiple evidence channels
* multiple releases
* multiple interpretations
* multiple relationships to future questions

VDB must preserve multiplicity rather than forcing artificial singularity.

Where biological or evidentiary multiplicity exists, it must remain detectable.

---

# Principle 10: Preserve Recoverability

Every derived structure should remain traceable back to the evidence from which it was produced.

This includes:

* projections
* topology records
* convergence geometry
* evidence convergence surfaces
* query surfaces
* downstream reasoning outputs

A user or downstream system should be able to move from a derived object back to the preserved assertions, participants, artifacts, provenance, and evidence basis that gave rise to it.

If recoverability is lost, the derived structure becomes scientifically unsafe.

---

# Principle 11: Preserve Uncertainty

Uncertainty is part of scientific evidence.

VDB must preserve uncertainty where it is present, including:

* ambiguous mappings
* incomplete context
* missing values
* low-confidence evidence
* conflicting annotations
* competing interpretations
* uncertain provenance
* unresolved namespace mappings

Absence, ambiguity, and uncertainty must not be silently converted into certainty.

Preserving uncertainty enables future reasoning systems to distinguish unknown from negative, incomplete from false, and ambiguous from resolved.

---

# Principle 12: Preserve Future Optionality

VDB must preserve evidence for questions that cannot yet be asked.

Future scientific methods may rely on relationships, contexts, provenance, or metadata that appear secondary today.

Therefore, VDB should not discard evidence richness merely because it is not immediately useful.

Future-proofing is not prediction.

Future-proofing is preservation.

VDB succeeds when future investigators can ask new questions without needing to reconstruct lost scientific meaning.

---

# Principle 13: Preserve Non-Equivalence of Representations

No representation is the evidence itself.

A table, graph, hypergraph, RDF triple, simplicial complex, topology summary, or query surface is a representation of preserved evidence.

VDB must not confuse representation with scientific substrate.

The preserved assertion remains primary.

Representations are derived and replaceable.

---

# Principle 14: Preserve the Boundary Between Evidence and Interpretation

VDB may expose evidence convergence.

VDB may reveal topology.

VDB may identify regions of interest.

VDB must not convert those observations into biological conclusions.

Interpretation belongs downstream.

The boundary between preserved evidence and interpreted knowledge must remain explicit.

---

# Principle 15: Preserve Append-Only Scientific History

New evidence should augment the scientific record.

It should not rewrite preserved evidence.

If later evidence contradicts earlier evidence, both must remain available with their respective context, provenance, and epistemic status.

A contradiction is not a persistence failure.

It is part of the scientific record.

---

# Architectural Use

These principles provide the evaluation standard for future VDB architecture.

Any proposed feature, optimization, storage strategy, projection, or reasoning interface should be evaluated against the preservation principles.

A change that improves performance but loses provenance is not acceptable.

A projection that improves query convenience but collapses epistemic status is not acceptable.

A schema that simplifies identity but erases source identity is not acceptable.

A convergence surface that hides evidence independence is not acceptable.

---

# Relationship to Persistence

Persistence is one implementation domain governed by these principles.

Evidence persistence must preserve meaning, identity, provenance, context, epistemic status, independence, time, multiplicity, uncertainty, recoverability, and future optionality.

The persistence layer may change over time, but these preservation obligations remain.

---

# Relationship to Downstream Reasoning

Downstream reasoning systems such as RDGP may assign confidence, evaluate statistical support, rank hypotheses, or propose biological interpretations.

Those downstream products must remain traceable to preserved evidence.

Reasoning may add derived knowledge.

Reasoning may not rewrite preserved evidence.

---

# Summary

The scientific evidence preservation mission of VDB is:

```text
Preserve meaning.
Preserve identity.
Preserve provenance.
Preserve context.
Preserve epistemic status.
Preserve independence.
Preserve time.
Preserve multiplicity.
Preserve uncertainty.
Preserve recoverability.
Preserve future optionality.
```

These principles ensure that VDB remains faithful to its Truth Layer philosophy.

Scientific understanding may change.

The preserved evidentiary record must remain reconstructable.

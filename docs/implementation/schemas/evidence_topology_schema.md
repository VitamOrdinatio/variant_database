# Evidence Topology Schema

## Epoch II: Evidence Geometry

| Epoch | Epoch Identity        | Epoch Purpose                                                                                       |
| ----- | --------------------- | --------------------------------------------------------------------------------------------------- |
| I     | Truth Layer           | What is truth? What must be preserved? What are the limits of knowledge? How does information flow? |
| II    | **Evidence Geometry** | **Once assertions exist, how do they organize into biological knowledge?**                          |
| III   | Discovery Layer       | How do preserved evidence topologies become discoverable?                                           |
| IV    | Projection Layer      | How does one truth generate many useful views without duplication?                                  |
| V     | Rationale Layer       | Why do we do this?                                                                                  |

---

## Relationship to Design and Specification

This schema implements:

```text
docs/design/evidence_topology_model.md
```

and

```text
docs/implementation/specifications/evidence_topology_spec.md
```

The design document defines the conceptual model.

The specification defines implementation requirements.

This schema defines the structural representation of Evidence Topology objects.

---

# Purpose

Evidence Topology objects represent deterministic organizational relationships derived from preserved Assertion Records.

Topology records are:

* derived
* reconstructable
* traceable
* non-authoritative

They organize preserved scientific evidence.

They are not themselves scientific evidence.

---

# Schema Overview

The Evidence Topology schema consists of two primary objects.

```text
EvidenceTopologyBuild
        │
        └── EvidenceTopologyRelationship
                ├── RelationshipMember[]
                └── BasisComponent[]
```

---

# Object: EvidenceTopologyBuild

Represents a single deterministic topology construction event.

## Fields

| Field                     | Type     | Required | Description                                           |
| ------------------------- | -------- | -------- | ----------------------------------------------------- |
| topology_build_id         | string   | Yes      | Unique topology construction identifier               |
| input_assertion_corpus_id | string   | Yes      | Identifier of assertion corpus used to build topology |
| topology_builder_name     | string   | Yes      | Builder implementation name                           |
| topology_builder_version  | string   | Yes      | Builder implementation version                        |
| build_scope               | string   | Yes      | Scope of topology construction                        |
| build_parameters          | object   | Optional | Builder configuration                                 |
| built_at                  | datetime | Yes      | UTC construction timestamp                            |

---

# Object: EvidenceTopologyRelationship

Represents one deterministic organizational relationship derived from preserved Assertion Records.

## Fields

| Field                    | Type                      | Required | Description                               |
| ------------------------ | ------------------------- | -------- | ----------------------------------------- |
| topology_relationship_id | string                    | Yes      | Unique relationship identifier            |
| topology_build_id        | string                    | Yes      | Parent topology build                     |
| topology_dimension       | enum                      | Yes      | Organizational dimension                  |
| derivation_basis         | enum                      | Yes      | Reason relationship exists                |
| relationship_scope       | string                    | Optional | Scope of organizational relationship      |
| source_assertion_ids     | array[string]             | Yes      | Assertions contributing to relationship   |
| relationship_members     | array[RelationshipMember] | Yes      | Members participating in relationship     |
| basis_components         | array[BasisComponent]     | Yes      | Components responsible for derivation     |
| epistemic_summary        | object                    | Optional | Summary of contributing epistemic classes |
| provenance_summary       | object                    | Optional | Summary of contributing provenance        |
| independence_summary     | object                    | Optional | Summary of evidence independence          |
| temporal_summary         | object                    | Optional | Summary of temporal context               |

---

# Object: RelationshipMember

Represents one participant in a derived topological relationship.

## Fields

| Field            | Type   | Required | Description                             |
| ---------------- | ------ | -------- | --------------------------------------- |
| member_role      | string | Yes      | Role within organizational relationship |
| member_kind      | string | Yes      | Kind of participating object            |
| member_namespace | string | Optional | Namespace identifier                    |
| member_value     | string | Yes      | Canonical member identifier             |
| member_label     | string | Optional | Human-readable label                    |

---

# Object: BasisComponent

Represents one preserved assertion component responsible for creating the relationship.

## Fields

| Field           | Type   | Required | Description                       |
| --------------- | ------ | -------- | --------------------------------- |
| basis_kind      | string | Yes      | Kind of assertion component       |
| basis_role      | string | Yes      | Biological or organizational role |
| basis_namespace | string | Optional | Namespace of component            |
| basis_value     | string | Yes      | Canonical preserved value         |
| basis_label     | string | Optional | Human-readable label              |

---

# Controlled Vocabulary

## topology_dimension

Initial controlled values:

```text
participant
relationship
context
provenance
epistemic
temporal
independence
producer
```

Future dimensions may be introduced without modifying existing topology records.

---

## derivation_basis

Initial controlled values:

```text
shared_participant
shared_relationship
shared_context
shared_provenance
shared_producer
shared_temporal_scope
shared_independence_group
shared_evidence_basis
epistemic_contrast
cross_producer_intersection
multi_component_intersection
```

Every topology relationship must declare exactly one primary derivation basis.

---

# Example

## Participant Topology Relationship

```yaml
topology_relationship_id: topology_rel_000014

topology_dimension: participant

derivation_basis: shared_participant

source_assertion_ids:
  - assertion_vap_000317
  - assertion_gsc_000041

relationship_members:

  - member_role: assertion
    member_kind: assertion_record
    member_value: assertion_vap_000317

  - member_role: assertion
    member_kind: assertion_record
    member_value: assertion_gsc_000041

  - member_role: shared_participant
    member_kind: gene
    member_namespace: ensembl_gene_id
    member_value: ENSG00000140521
    member_label: POLG

basis_components:

  - basis_kind: participant
    basis_role: gene
    basis_namespace: ensembl_gene_id
    basis_value: ENSG00000140521
    basis_label: POLG
```

---

# Cardinality

```text
EvidenceTopologyBuild

    1

    ↓

EvidenceTopologyRelationship

    1..N

    ↓

RelationshipMember

    2..N

    ↓

BasisComponent

    1..N
```

This permits pairwise relationships while naturally supporting higher-order organizational structures.

---

# Schema Invariants

Every EvidenceTopologyRelationship shall satisfy the following:

* derived from one or more Assertion Records
* declares exactly one topology dimension
* declares exactly one primary derivation basis
* identifies all contributing Assertion Records
* identifies all participating relationship members
* identifies one or more basis components
* remains traceable to preserved assertions
* remains reconstructable
* introduces no biological interpretation

Relationships violating these invariants are invalid.

---

# Representation Independence

This schema intentionally avoids defining graph nodes or graph edges.

Evidence Topology is represented as organizational relationships rather than graph primitives.

Consequently, the same topology may later be projected into:

* relational databases
* property graphs
* hypergraphs
* simplicial complexes
* tensor representations
* future mathematical frameworks

without changing the preserved scientific meaning.

---

# Summary

The Evidence Topology Schema provides the structural representation of deterministic organizational relationships derived from preserved Assertion Records.

It captures:

* topology construction
* organizational relationships
* relationship members
* derivation basis
* traceability
* reconstruction metadata

while preserving the fundamental architectural invariant established throughout Epoch II:

**Evidence Topology is derived organization over preserved scientific assertions. It is never itself the preserved scientific evidence.**

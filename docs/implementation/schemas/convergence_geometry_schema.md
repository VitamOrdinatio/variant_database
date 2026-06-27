# Convergence Geometry Schema

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
docs/design/convergence_geometry_model.md
```

and

```text
docs/implementation/specifications/convergence_geometry_spec.md
```

The design document defines the conceptual model.

The specification defines implementation obligations.

This schema defines the structural representation of Convergence Geometry objects.

---

# Purpose

Convergence Geometry objects represent deterministic structural characterizations derived from Evidence Topology.

Geometry records are:

* topology-derived
* deterministic
* reconstructable
* traceable
* non-authoritative

They characterize preserved evidence organization.

They are not themselves scientific evidence.

---

# Schema Overview

The Convergence Geometry schema consists of six primary objects.

```text
ConvergenceGeometryBuild
        │
        └── ConvergenceRegion
                ├── RegionBoundary[]
                ├── GeometryFeature[]
                ├── StructuralMotif[]
                └── ConvergenceProfile
```

---

# Object: ConvergenceGeometryBuild

Represents a single deterministic geometry construction event.

## Fields

| Field                    | Type     | Required | Description                             |
| ------------------------ | -------- | -------- | --------------------------------------- |
| geometry_build_id        | string   | Yes      | Unique geometry construction identifier |
| input_topology_build_id  | string   | Yes      | Source Evidence Topology build          |
| geometry_builder_name    | string   | Yes      | Builder implementation                  |
| geometry_builder_version | string   | Yes      | Builder version                         |
| geometry_method          | string   | Yes      | Geometry characterization method        |
| build_scope              | string   | Yes      | Scope of geometry construction          |
| build_parameters         | object   | Optional | Builder configuration                   |
| built_at                 | datetime | Yes      | UTC construction timestamp              |

---

# Object: ConvergenceRegion

Represents one deterministic structural region derived from Evidence Topology.

## Fields

| Field                            | Type                | Required | Description                                            |
| -------------------------------- | ------------------- | -------- | ------------------------------------------------------ |
| convergence_region_id            | string              | Yes      | Unique region identifier                               |
| geometry_build_id                | string              | Yes      | Parent geometry build                                  |
| region_label                     | string              | Optional | Human-readable label                                   |
| region_kind                      | enum                | Yes      | Organizational region type                             |
| region_bounding_basis            | enum                | Yes      | Rule defining the region boundary                      |
| region_anchor                    | array[RegionAnchor] | Yes      | Primary structural anchor(s)                           |
| source_topology_relationship_ids | array[string]       | Yes      | Contributing topology relationships                    |
| source_assertion_ids             | array[string]       | Optional | Contributing Assertion Records (traceability shortcut) |

---

# Object: RegionAnchor

Represents one structural anchor defining a Convergence Region.

## Fields

| Field            | Type   | Required | Description                              |
| ---------------- | ------ | -------- | ---------------------------------------- |
| anchor_kind      | string | Yes      | Biological or organizational object type |
| anchor_namespace | string | Optional | Namespace identifier                     |
| anchor_value     | string | Yes      | Canonical identifier                     |
| anchor_label     | string | Optional | Human-readable label                     |

---

# Object: RegionBoundary

Represents the deterministic rule defining a Convergence Region.

## Fields

| Field                        | Type          | Required | Description                             |
| ---------------------------- | ------------- | -------- | --------------------------------------- |
| boundary_kind                | string        | Yes      | Boundary classification                 |
| boundary_rule                | string        | Yes      | Deterministic inclusion rule            |
| boundary_value               | string        | Yes      | Canonical boundary value                |
| included_topology_dimensions | array[string] | Yes      | Participating topology dimensions       |
| included_derivation_bases    | array[string] | Yes      | Participating topology derivation bases |

---

# Object: GeometryFeature

Represents one structural characteristic of a Convergence Region.

## Fields

| Field                            | Type          | Required | Description                       |
| -------------------------------- | ------------- | -------- | --------------------------------- |
| geometry_feature_id              | string        | Yes      | Unique feature identifier         |
| convergence_region_id            | string        | Yes      | Parent Convergence Region         |
| feature_kind                     | enum          | Yes      | Structural feature type           |
| feature_value                    | string        | Yes      | Measured or characterized value   |
| feature_unit                     | string        | Optional | Unit or representation            |
| feature_derivation_basis         | string        | Yes      | Topological basis of the feature  |
| source_topology_relationship_ids | array[string] | Yes      | Supporting topology relationships |
| description                      | string        | Optional | Human-readable summary            |

---

# Object: StructuralMotif

Represents a recurring deterministic organizational pattern.

## Fields

| Field                            | Type          | Required | Description                       |
| -------------------------------- | ------------- | -------- | --------------------------------- |
| structural_motif_id              | string        | Yes      | Unique motif identifier           |
| convergence_region_id            | string        | Yes      | Parent region                     |
| motif_kind                       | enum          | Yes      | Motif classification              |
| motif_pattern                    | string        | Yes      | Structural pattern description    |
| motif_derivation_basis           | string        | Yes      | Topological basis                 |
| source_topology_relationship_ids | array[string] | Yes      | Supporting topology relationships |

---

# Object: ConvergenceProfile

Represents a structural summary of a Convergence Region.

## Fields

| Field                  | Type          | Required | Description                       |
| ---------------------- | ------------- | -------- | --------------------------------- |
| convergence_profile_id | string        | Yes      | Unique profile identifier         |
| convergence_region_id  | string        | Yes      | Parent region                     |
| profile_label          | string        | Optional | Human-readable profile name       |
| profile_summary        | string        | Optional | Narrative structural summary      |
| profile_components     | array[string] | Yes      | Structural components represented |

---

# Controlled Vocabulary

## region_kind

Initial values:

```text
participant_centered
phenotype_centered
variant_centered
producer_crossing
multi_component
temporal
provenance
```

---

## region_bounding_basis

Initial values:

```text
participant_centered_neighborhood
phenotype_centered_neighborhood
producer_crossing_intersection
multi_component_intersection
temporal_persistence_region
provenance_centered_region
```

---

## feature_kind

Initial values:

```text
density
breadth
depth
intersection_complexity
producer_diversity
modality_diversity
provenance_diversity
epistemic_diversity
independence_breadth
temporal_persistence
temporal_accumulation
```

---

## motif_kind

Initial values:

```text
participant_intersection
cross_producer_pattern
cross_modality_pattern
multi_participant_pattern
shared_provenance_pattern
shared_epistemic_pattern
```

---

# Example

## POLG-Centered Convergence Region

```yaml
convergence_region_id: conv_region_000014

region_kind: participant_centered

region_bounding_basis: participant_centered_neighborhood

region_anchor:

  - anchor_kind: gene
    anchor_namespace: ensembl_gene_id
    anchor_value: ENSG00000140521
    anchor_label: POLG

source_topology_relationship_ids:

  - topology_rel_00124
  - topology_rel_00491
  - topology_rel_00672
```

---

# Cardinality

```text
ConvergenceGeometryBuild

        1

        ↓

ConvergenceRegion

        1..N

        ↓

RegionBoundary
GeometryFeature
StructuralMotif
ConvergenceProfile
```

Each region may contain multiple boundaries, features, and motifs, while producing a single structural profile.

---

# Schema Invariants

Every Convergence Region shall satisfy the following:

* derived from Evidence Topology
* declares exactly one primary region-bounding basis
* identifies one or more structural anchors
* identifies contributing topology relationships
* remains traceable to preserved assertions
* remains reconstructable
* introduces no biological interpretation

Every Geometry Feature shall:

* declare its derivation basis
* identify contributing topology relationships
* characterize structure only

Every Structural Motif shall:

* represent recurring organizational structure
* remain deterministic
* remain topology-derived

---

# Representation Independence

This schema intentionally avoids commitment to any particular mathematical representation.

Convergence Geometry may later be represented using:

* relational structures
* graphs
* hypergraphs
* simplicial complexes
* topological representations
* tensor methods
* future mathematical frameworks

without altering the preserved structural meaning.

---

# Summary

The Convergence Geometry Schema defines the structural representation of deterministic characterizations over Evidence Topology.

It captures:

* geometry construction
* convergence regions
* structural boundaries
* geometry features
* structural motifs
* convergence profiles

while preserving the governing architectural invariant of Epoch II:

**Convergence Geometry is a deterministic, topology-derived characterization of preserved evidence organization. It exposes structure without introducing interpretation, ensuring that every geometric object remains traceable to the topology—and ultimately to the original producer assertions—from which it was derived.**

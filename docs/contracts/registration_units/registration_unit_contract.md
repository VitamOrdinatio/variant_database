# Registration Unit Contract

## Purpose

This document defines the VDB contract for Registration Units.

A Registration Unit is the durable custody boundary between producer TEP ingestion and Phase 4 derived evidence architecture.

Registration Units preserve the registered representation of accepted producer evidence packages so that downstream VDB layers can construct corpus generations, Assertion Record indexes, Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, and Projection Views without re-reading or mutating raw producer artifacts.

This contract ensures that Registration Units remain:

```text
traceable
readable
non-destructive
storage-neutral
producer-aware
namespace-preserving
assertion-preserving
source-identity-preserving
certification-aware
reconstructable
```

---

# Scope

This contract applies to all VDB Registration Units, including:

```text
SQLite-backed registration units
future relational registration units
future producer-run registration units
future corpus-materialized registration units
future lakehouse-backed registration units
future object-store-backed registration units
future storage backends
```

This contract governs the logical requirements of a Registration Unit.

It does not prescribe a single physical storage representation.

In the current MARK implementation, a Registration Unit may be represented as:

```text
results/registration/mark_phase3_canonical/<registration_unit_label>/vdb.sqlite
```

That representation is an implementation choice.

The Registration Unit is the architectural object.

---

# Parent System Contract Obligations

This contract is subordinate to:

```text
docs/contracts/system_contract.md
```

The System Contract establishes the governing VDB authority chain:

```text
Producer TEP
        ↓
registration unit
        ↓
corpus generation
        ↓
Assertion Records
        ↓
Evidence Topology
        ↓
Convergence Geometry
        ↓
Evidence Convergence Surfaces
        ↓
Projection Views
        ↓
Downstream Reasoning
```

This contract defines the obligations of the Registration Unit layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Registration Unit contract governs the transition from producer package custody into reusable VDB substrate custody.

A Registration Unit answers:

```text
Has this accepted producer evidence package been registered in a traceable,
readable, non-destructive, and validation-aware form?
```

A Registration Unit does not answer:

```text
Which Registration Units belong in a corpus generation?

What topology emerges from the corpus?

What convergence geometry exists?

Which surfaces should be exposed?

What projections should consumers receive?

What biological meaning should downstream systems infer?
```

Those responsibilities belong to downstream contracts.

---

# Definition

A Registration Unit is the canonical registered custody representation of one accepted producer evidence package.

A Registration Unit must preserve enough information to support:

```text
package reconstruction
artifact reconstruction
assertion registration reconstruction
source identity reconstruction
namespace reconstruction
producer-family reconstruction
provenance reconstruction
validation reconstruction
certification reconstruction
Phase 4 corpus selection
Phase 4 Assertion Record indexing
```

A Registration Unit is canonical only in the VDB custody sense.

It is not canonical biological truth.

It is not an integrated corpus.

It is not topology.

It is not geometry.

It is not a surface.

It is not a projection.

It is not downstream reasoning.

---

# Core Invariant

The operational rule for current MARK development is:

```text
1 accepted TEP → 1 certified SQLite Registration Unit
```

The architectural rule is:

```text
1 accepted TEP → 1 traceable Registration Unit
```

The architectural rule is the invariant.

The SQLite representation is the current implementation.

---

# Storage Neutrality

A Registration Unit may be represented by multiple physical storage strategies if all contract obligations are satisfied.

Valid future representations may include:

```text
one database per TEP
one database per producer run
logical Registration Unit partitions within one database per corpus generation
logical Registration Unit partitions within one central relational database
lakehouse-style partitioned files
object store plus indexed metadata
future storage backends
```

Any representation is compliant only if it preserves:

```text
Registration Unit identity
source package identity
producer identity
artifact identity
assertion registrations
source identities
source namespaces
provenance
validation status
certification status when available
reconstruction paths
```

The storage backend must not define the architecture.

The Registration Unit boundary defines the architecture.

---

# Current Implementation Representation

In the current MARK implementation, certified Registration Units are represented as SQLite databases.

The Phase 3 certified MARK corpus includes Registration Units such as:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

These Registration Units are checkpointed Phase 4 inputs.

Phase 4 builders may inspect them.

Phase 4 builders must not destructively modify them.

---

# Required Registration Unit Identity

Every Registration Unit must have a stable identity.

A Registration Unit identity must preserve:

```text
registration_unit_id
registration_unit_label
producer_family
source_package_id
source_package_path or resolvable reference
registration_backend
registration_backend_version when available
registration_created_at
registration_created_by process or tool
validation_status
certification_status when available
```

The Registration Unit identity must remain stable across validation, corpus selection, and derived-layer construction.

A Registration Unit may have aliases or labels for human readability.

Aliases must not replace stable Registration Unit identity.

---

# Required Preserved Domains

A Registration Unit must preserve or expose registered records for the following domains:

```text
TEP package
producer
repository
run or release when available
artifact
assertion registration
source identity
source namespace
evidence domain
assertion type
authority context
uncertainty context
surface-relevant roles when declared
provenance
validation status
certification status when available
```

A Registration Unit may also preserve implementation-supporting records such as:

```text
metadata records
entity records
Evidence Object records
Evidence State records
Evidence State Transition records
registration reports
schema metadata
backend metadata
```

These support custody and lifecycle tracking.

They must not supersede Assertion Record primacy.

---

# Package Obligations

A Registration Unit must preserve the identity of the accepted producer package from which it was constructed.

Package preservation must include:

```text
package identifier
producer family
producer repository when available
producer run identifier when available
producer release identifier when available
package path or resolvable reference
package manifest reference when available
package checksum when available
package validation status
```

The package record must be reconstructable from the Registration Unit.

If the package cannot be reconstructed or identified, the Registration Unit is not VDB-compliant.

---

# Artifact Obligations

A Registration Unit must preserve artifact identity and artifact lineage.

Artifact preservation must include:

```text
artifact identifier
artifact name or label
artifact path or resolvable reference
artifact role
artifact evidence domain
artifact producer family
artifact package reference
artifact checksum when available
artifact validation status
```

Artifact records must remain distinct.

A Registration Unit must not collapse multiple artifacts into a single opaque evidence object unless each original artifact remains reconstructable.

---

# Assertion Registration Obligations

A Registration Unit must preserve assertion registrations sufficient to construct or resolve Assertion Records during Phase 4 indexing.

Assertion registration preservation must include:

```text
assertion registration identity
source package reference
source artifact reference
producer family
assertion type
evidence domain
relationship or registered relationship class when available
participant references when available
evidence basis references when available
authority context
uncertainty context
source row or source record reference when available
payload reference when applicable
validation status
```

A Registration Unit does not need to be the final corpus-level Assertion Record index.

However, it must preserve enough assertion-registration structure for Phase 4 to build that index deterministically.

A Registration Unit must not collapse distinct assertion registrations into an opaque score, count, or summary that prevents reconstruction of the registered assertion basis.

---

# Source Identity Obligations

A Registration Unit must preserve source identities before any canonical identity attachment.

Source identity preservation must include:

```text
source_identity_id
source identifier value
source namespace
source artifact reference
source assertion registration reference when applicable
source extraction method
source extraction context
producer family
validation status
```

Source identities must remain visible even when canonical identifiers are later attached.

Canonical identifiers may be added by namespace governance.

Canonical identifiers must not replace source identities.

A Registration Unit must preserve unresolved, ambiguous, conflicted, or missing source identity states when applicable.

---

# Namespace Obligations

A Registration Unit must preserve source namespace information sufficient for later namespace governance.

Namespace preservation must include:

```text
namespace label
namespace type when available
source identifier values
source artifact references
producer family
extraction method
resolution status when available
resolution provenance when available
ambiguity status when available
conflict status when available
```

Namespace resolution is optional at the Registration Unit layer.

Namespace preservation is mandatory.

If namespace resolution has already occurred, the Registration Unit must preserve source identity and canonical identity separately.

---

# Provenance Obligations

A Registration Unit must preserve provenance sufficient to reconstruct:

```text
which producer emitted the package
which run or release generated the package when available
which TEP transported the package
which artifact contained each registered assertion
which source identities were extracted
which methods performed registration
which validation checks were applied
which certification checks were applied when available
```

Registration provenance must include:

```text
registration process or tool
registration process version when available
registration timestamp
input package reference
input artifact references
schema or contract version when available
validation report reference when available
certification report reference when available
```

A Registration Unit without reconstructable provenance is not VDB-compliant.

---

# Certification Status Obligations

A Registration Unit must expose validation and certification status.

Supported status classes include:

```text
certified
validated
provisional
uncertified
rejected
```

Status semantics:

```text
certified
    The Registration Unit passed declared certification checks and may serve as
    a canonical Phase 4 checkpoint input.

validated
    The Registration Unit passed validation checks but has not been formally certified.

provisional
    The Registration Unit is usable for development or fixture testing but is not
    authoritative for heavy Phase 4 certification.

uncertified
    The Registration Unit exists but lacks sufficient validation or certification
    status for authoritative Phase 4 use.

rejected
    The Registration Unit failed required validation or certification checks and
    must not be used as a Phase 4 input unless explicitly testing failure behavior.
```

Current MARK heavy Phase 4 smoketests should use Registration Units with status:

```text
certified
```

Local synthetic tests may use provisional Registration Units if their status is explicit.

No Registration Unit may silently masquerade as certified.

---

# Read-Only Consumption Obligations

Phase 4 builders may read certified Registration Units.

Phase 4 builders must not destructively modify certified Registration Units.

Allowed Phase 4 actions include:

```text
read Registration Unit metadata
read package registrations
read artifact registrations
read assertion registrations
read source identities
read validation status
read certification status
emit sidecar indexes
emit validation reports
emit corpus generation manifests
emit derived artifacts outside the certified Registration Unit
```

Prohibited Phase 4 actions include:

```text
rewriting certified Registration Units
deleting registered records
mutating producer package references
mutating artifact references
mutating assertion registrations
mutating source identities
replacing source identities with canonical identities
marking uncertified units as certified without certification evidence
```

If a Registration Unit must be repaired, regenerated, migrated, or recertified, that operation must produce a new Registration Unit version or a documented migration artifact.

---

# Relationship To Corpus Generation

Registration Units are inputs to Corpus Generations.

A Registration Unit contract asks:

```text
Is this individual registered evidence package valid, traceable, readable, and non-mutated?
```

A Corpus Generation contract asks:

```text
Which Registration Units are selected together as a declared evidence corpus?
```

Registration Units must not define corpus scope.

Corpus Generations must not erase Registration Unit boundaries.

A Corpus Generation may include multiple Registration Units.

A Registration Unit may participate in multiple Corpus Generations.

Each Corpus Generation must preserve the Registration Unit identities it selected.

---

# Relationship To Assertion Records

Registration Units preserve assertion registrations.

Assertion Records are the primary preserved scientific objects used by Phase 4 derived layers.

Phase 4 Assertion Record indexing must be able to construct or resolve Assertion Records from Registration Unit contents.

The distinction is:

```text
Registration Unit
    preserves registered custody over an accepted producer evidence package

Assertion Record
    preserves a producer scientific claim in a corpus-indexable form
```

Registration Units support Assertion Record construction.

Registration Units do not replace Assertion Records.

Assertion Record indexes must preserve traceability back to Registration Units.

---

# Relationship To Evidence Topology

Registration Units do not create Evidence Topology.

Registration Units provide registered assertion and source identity material from which Evidence Topology may later be derived.

Evidence Topology must be derived from Assertion Records or assertion-equivalent indexed records.

Topology derivation must preserve Registration Unit lineage.

A Registration Unit must not infer cross-producer convergence, cross-modality convergence, or topology relationships by itself.

---

# Relationship To Convergence Geometry

Registration Units do not create Convergence Geometry.

Registration Units may provide the upstream registered evidence material that later participates in geometry derivation.

Convergence Geometry must be derived from Evidence Topology.

Geometry derivation must preserve Registration Unit lineage through topology and Assertion Records.

A Registration Unit must not characterize convergence, density, breadth, depth, modality diversity, temporal persistence, or biological meaning.

---

# Relationship To Evidence Convergence Surfaces

Registration Units do not expose Evidence Convergence Surfaces.

Registration Units may preserve surface-relevant roles when those roles are declared by producer artifacts, registration policy, or upstream metadata.

Surface relevance must not be confused with surface membership.

Evidence Convergence Surface construction must occur downstream of Convergence Geometry.

Surface construction must preserve Registration Unit lineage.

---

# Relationship To Projection Views

Registration Units may be inspected or summarized by Projection Views.

A projection over a Registration Unit must declare:

```text
projection purpose
projection source layer
source Registration Unit identity
source records
materialization status
lossiness status when applicable
reconstruction path
```

A Projection View over a Registration Unit does not replace the Registration Unit.

A Projection View does not acquire Registration Unit authority.

---

# Validation Obligations

Registration Unit validation must confirm:

```text
Registration Unit exists
Registration Unit is readable
Registration Unit representation is declared
Registration Unit identity is stable
producer family is declared
source package identity is preserved
artifact registrations exist
assertion registrations exist
source identities exist where expected
source namespaces are preserved
artifact references resolve
assertion references resolve
source identity references resolve
validation status is visible
certification status is visible when available
inspection does not mutate the Registration Unit
```

For SQLite-backed Registration Units, validation may additionally confirm:

```text
required tables exist
required indexes exist when applicable
referential integrity holds
package references resolve
artifact references resolve
assertion registration references resolve
source identity references resolve
row counts are internally consistent
```

SQLite-specific checks are implementation validation checks.

They do not redefine the Registration Unit contract.

---

# Anti-Collapse Rules

The following are prohibited:

```text
producer identity collapse
package identity collapse
artifact identity collapse
assertion registration collapse
source identity collapse
source namespace collapse
authority collapse
uncertainty collapse
validation status collapse
certification status collapse
Registration Unit boundary collapse
canonical identity replacing source identity
multiple TEPs merged without preserved Registration Unit boundaries
cross-producer convergence inferred inside a Registration Unit
topology created inside a Registration Unit
geometry created inside a Registration Unit
surface membership created inside a Registration Unit
projection output replacing a Registration Unit
biological reasoning performed inside a Registration Unit
destructive modification of certified Registration Units
```

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

A Registration Unit implementation is complete only when:

```text
Registration Unit identity is stable
producer package identity is preserved
artifact identity is preserved
assertion registrations are preserved
source identities are preserved
source namespaces are preserved
provenance is reconstructable
validation status is visible
certification status is visible when available
Registration Unit inspection is read-only
Registration Unit representation is declared
storage backend does not define the architecture
Registration Unit can be selected by a Corpus Generation
Assertion Record indexing can trace back to the Registration Unit
anti-collapse validation passes
```

A Registration Unit implementation is not complete merely because a database or file exists.

A Registration Unit implementation is complete only when that representation satisfies this contract.

---

# Summary

A Registration Unit is the durable custody boundary between producer TEP ingestion and Phase 4 derived evidence architecture.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Topology derives organization.
```

Registration Units make Phase 4 possible by providing validated, traceable, non-destructive, checkpointed inputs.

They do not perform Phase 4 derivation themselves.

The guiding rule is:

```text
Preserve the registered package.

Protect source identity.

Expose certification status.

Remain storage-neutral.

Never derive authority.
```

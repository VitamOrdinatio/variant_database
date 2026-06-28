# Corpus Generation Contract

## Purpose

This document defines the VDB contract for Corpus Generations.

A Corpus Generation is the declared evidence scope from which Phase 4 derived evidence structures are built.

Corpus Generations select Registration Units with explicit validation or certification status and declare the exact evidence universe used for Assertion Record indexing, Evidence Topology derivation, Convergence Geometry derivation, Evidence Convergence Surface construction, Projection View generation, and downstream consumer projections.

This contract ensures that Corpus Generations remain:

```text
declared
traceable
deterministic
registration-unit-preserving
producer-aware
scope-explicit
policy-explicit
validation-aware
certification-aware
reconstructable
```

A Corpus Generation declares evidence scope.

It does not interpret evidence.

---

# Scope

This contract applies to all VDB Corpus Generations, including:

```text
local synthetic corpus generations
small integration-test corpus generations
certified MARK corpus generations
future multi-producer corpus generations
future multi-cohort corpus generations
future release corpus generations
future reasoning-informed corpus generations
future external-capsule corpus generations
```

This contract governs the logical requirements of a Corpus Generation.

It does not prescribe a single physical materialization strategy.

A Corpus Generation may be represented by:

```text
manifest files
TSV files
JSON files
SQLite indexes
directory structures
central relational records
lakehouse-style partitions
object-store metadata indexes
future storage backends
```

The representation is not the architecture.

The declared, reconstructable, validated evidence scope is the architecture.

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

This contract defines the obligations of the Corpus Generation layer.

If this contract conflicts with the System Contract, the System Contract takes precedence.

---

# Contract Role

The Corpus Generation contract governs the transition from individually registered producer evidence packages into a declared multi-unit evidence scope.

A Corpus Generation answers:

```text
Which Registration Units are selected together
as the evidence basis for this derived VDB build?
```

A Corpus Generation does not answer:

```text
What scientific claims are represented as Assertion Records?

What relationships exist among assertions?

What topology emerges from the selected corpus?

What convergence geometry exists?

Which convergence regions are surface-eligible?

What projections should consumers receive?

What biological meaning should downstream systems infer?
```

Those responsibilities belong to downstream contracts.

---

# Definition

A Corpus Generation is a declared collection of Registration Units selected under an explicit policy for a specific VDB derivation context.

A Corpus Generation must preserve enough information to support:

```text
corpus scope reconstruction
Registration Unit selection reconstruction
Registration Unit exclusion reconstruction when applicable
producer-family reconstruction
package reconstruction
artifact-count reconstruction
assertion-registration-count reconstruction
source-identity-count reconstruction
validation reconstruction
certification reconstruction
downstream Assertion Record indexing
downstream topology derivation
downstream geometry derivation
downstream surface construction
downstream projection lineage
```

A Corpus Generation is not the total VDB universe.

A Corpus Generation is not source truth.

A Corpus Generation is not a merged replacement for its Registration Units.

A Corpus Generation is not topology.

A Corpus Generation is not geometry.

A Corpus Generation is not a surface.

A Corpus Generation is not a projection.

A Corpus Generation is not downstream reasoning.

---

# Core Invariant

The architectural rule is:

```text
many traceable Registration Units → one declared Corpus Generation
```

A Corpus Generation declares selected Registration Units.

It does not imply that all known Registration Units are selected.

It does not erase Registration Unit boundaries.

It does not convert selected Registration Units into a new source of evidence authority.

---

# Materialization Neutrality

A Corpus Generation may be physically represented in multiple ways if all contract obligations are satisfied.

Valid representations may include:

```text
corpus_generation_manifest.tsv
corpus_generation_manifest.json
corpus_generation_report.md
corpus_generation_validation_report.md
SQLite-backed corpus index
central relational corpus record
lakehouse-style corpus partition
object-store metadata index
future storage backends
```

Any representation is compliant only if it preserves:

```text
Corpus Generation identity
selected Registration Unit identities
Registration Unit references
selection policy
inclusion rationale
exclusion rationale when applicable
producer-family context
package identity
artifact counts
assertion registration counts
source identity counts
validation status
certification status when available
reconstruction paths
```

The materialization format must not define the architecture.

The declared corpus scope defines the architecture.

If a Corpus Generation is materialized as an integrated database, index, partition, or object-store layout, the materialization must preserve Registration Unit boundaries and must not convert the materialized corpus into source truth.


---

# Current Benchmark Corpus

The initial Phase 4 heavy smoketest corpus should be constructed from the certified Phase 3 MARK Registration Units.

The current benchmark corpus may be identified as:

```text
mark_phase4_corpus_6tep_v1
```

or another explicitly declared Corpus Generation identifier.

The initial benchmark corpus is expected to include:

```text
results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite
results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite
results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite
results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite
results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

This benchmark corpus is useful because it includes:

```text
multiple producer families
heterogeneous evidence domains
small GSC semantic evidence packages
large VAP source-identity-heavy evidence packages
certified Phase 3 registration outputs
realistic MARK-scale storage behavior
```

This benchmark corpus is not the only valid Corpus Generation pattern.

Future Corpus Generations may include different Registration Units, producer families, cohorts, evidence modalities, or reasoning-returned assertion packages.

---

# Required Corpus Generation Identity

Every Corpus Generation must have a stable identity.

A Corpus Generation identity must preserve:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
corpus_generation_version when applicable
selection_policy_id
selection_policy_version when applicable
builder_name
builder_version when available
build_timestamp
validation_status
certification_status when available
```

The Corpus Generation identity must remain stable across downstream Assertion Record indexing, topology derivation, geometry derivation, surface construction, projection generation, validation, and certification.

A Corpus Generation may have aliases or labels for human readability.

Aliases must not replace stable Corpus Generation identity.

---

# Registration Unit Selection Obligations

A Corpus Generation must explicitly declare every Registration Unit it includes.

For each included Registration Unit, the Corpus Generation must preserve:

```text
registration_unit_id
registration_unit_label
registration_unit_path or resolvable reference
producer_family
source_package_id
registration_backend
validation_status
certification_status when available
inclusion_status
inclusion_rationale
```

Included Registration Units must remain individually identifiable.

A Corpus Generation must not merge selected Registration Units into a single opaque evidence source.

A Corpus Generation must not silently include Registration Units.

A Corpus Generation must not silently exclude Registration Units when the exclusion affects interpretation of corpus scope.

---

# Inclusion And Exclusion Obligations

A Corpus Generation must declare its selection policy.

The selection policy must state:

```text
which Registration Units are eligible
which Registration Units are selected
which Registration Units are excluded when exclusion is relevant
why each selected unit is included
why each relevant excluded unit is excluded
what certification or validation status is required
what producer families are in scope
what evidence domains are in scope
what temporal or generation constraints apply when applicable
```

Inclusion rationale may include:

```text
certified Phase 3 benchmark input
producer-family representation
evidence-domain representation
cohort representation
heavy smoketest coverage
consumer projection readiness testing
release-corpus inclusion
failure-mode testing
synthetic fixture inclusion
```

Exclusion rationale may include:

```text
uncertified Registration Unit
failed validation
out-of-scope producer family
out-of-scope cohort
out-of-scope evidence domain
duplicate or superseded Registration Unit
missing path
unreadable backend
explicitly deferred input
```

A Corpus Generation with undocumented inclusion or exclusion behavior is not VDB-compliant.

---

# Corpus Manifest Obligations

A Corpus Generation must emit or resolve to a corpus manifest.

The corpus manifest must preserve:

```text
corpus_generation_id
corpus_generation_label
corpus_generation_purpose
selection_policy_id
selection_policy_version when applicable
included_registration_units
excluded_registration_units when applicable
producer_family_summary
package_summary
artifact_count_summary
assertion_registration_count_summary
source_identity_count_summary
validation_status_summary
certification_status_summary
build_timestamp
builder_name
builder_version when available
manifest_schema_version when available
```

The corpus manifest must be deterministic under fixed inputs.

The corpus manifest must be sufficient to reconstruct the exact selected Registration Unit set.

The corpus manifest must not replace the selected Registration Units.

---

# Count And Inventory Obligations

A Corpus Generation may summarize selected Registration Units.

Allowed summaries include:

```text
number of Registration Units
producer-family distribution
package count
artifact count
assertion registration count
source identity count
namespace distribution
validation status distribution
certification status distribution
storage footprint summary when available
```

Count and inventory summaries must remain traceable to selected Registration Units.

Summaries must not replace Registration Unit records.

Summaries must not collapse source identity, producer identity, artifact identity, assertion registration identity, validation status, or certification status.

If counts are unavailable, incomplete, or approximate, that status must be explicit.

---

# Certification Status Obligations

A Corpus Generation must expose its own validation and certification status.

Supported status classes include:

```text
planned
provisional
validated
certified
rejected
deprecated
```

Status semantics:

```text
planned
    The Corpus Generation has been declared but not yet constructed.

provisional
    The Corpus Generation is usable for development or fixture testing but is not
    authoritative for certification.

validated
    The Corpus Generation passed declared validation checks but has not been
    formally certified.

certified
    The Corpus Generation passed declared certification checks and may serve as
    a canonical Phase 4 derivation input.

rejected
    The Corpus Generation failed required validation or certification checks and
    must not be used as a Phase 4 input unless explicitly testing failure behavior.

deprecated
    The Corpus Generation remains historically reconstructable but should not be
    used for new derivation work unless explicitly requested.
```

A Corpus Generation built entirely from certified Registration Units is not automatically certified.

Certified Registration Units support Corpus Generation certification.

They do not replace Corpus Generation validation.

A Corpus Generation must not silently masquerade as certified.

---

# Read-Only Input Obligations

Corpus Generation construction may inspect Registration Units.

Corpus Generation construction must not destructively modify Registration Units.

Allowed Corpus Generation actions include:

```text
read Registration Unit metadata
read Registration Unit validation status
read Registration Unit certification status
read package registrations
read artifact registrations
read assertion registration counts
read source identity counts
read producer-family metadata
emit corpus manifests
emit corpus inventories
emit corpus validation reports
emit sidecar indexes
emit downstream input manifests
```

Prohibited Corpus Generation actions include:

```text
rewriting certified Registration Units
deleting Registration Unit records
mutating producer package references
mutating artifact references
mutating assertion registrations
mutating source identities
replacing source identities with canonical identities
changing Registration Unit certification status without evidence
copying all source identities into a materialized corpus without explicit need
treating materialized corpus output as source truth
```

If Corpus Generation construction requires Registration Unit repair, migration, regeneration, or recertification, that work must occur outside the Corpus Generation operation and must produce new or explicitly versioned Registration Unit artifacts.

---

# Relationship To Registration Units

Registration Units are inputs to Corpus Generations.

A Registration Unit contract asks:

```text
Is this individual registered evidence package valid, traceable, readable, and non-mutated?
```

A Corpus Generation contract asks:

```text
Which Registration Units are selected together as a declared evidence corpus?
```

A Corpus Generation may include multiple Registration Units.

A Registration Unit may participate in multiple Corpus Generations.

Corpus Generations must preserve Registration Unit identities.

Corpus Generations must not erase Registration Unit boundaries.

---

# Relationship To Assertion Records

Corpus Generations provide the evidence scope for Assertion Record indexing.

Assertion Record indexing must preserve both:

```text
corpus_generation_id
registration_unit_id
```

The distinction is:

```text
Corpus Generation
    declares the evidence scope selected for a build

Assertion Record
    preserves a producer scientific claim in corpus-indexable form
```

A Corpus Generation does not replace Assertion Records.

A Corpus Generation does not decide scientific meaning.

A Corpus Generation must preserve sufficient Registration Unit lineage for Assertion Records to trace back to their source Registration Units.

---

# Relationship To Evidence Topology

Corpus Generations provide the declared input scope for Evidence Topology derivation.

Evidence Topology must declare:

```text
input_corpus_generation_id
input_assertion_record_index_id when available
topology_build_id
topology_derivation_policy
```

A Corpus Generation may define the evidence universe for topology derivation.

A Corpus Generation must not define topology relationships.

Topology answers:

```text
What is connected?
```

Corpus Generation answers:

```text
What evidence is in scope?
```

Those responsibilities must remain distinct.

---

# Relationship To Convergence Geometry

Corpus Generations may provide upstream scope for Convergence Geometry indirectly through Evidence Topology.

Convergence Geometry must be derived from Evidence Topology.

Geometry derivation must preserve Corpus Generation lineage through topology and Assertion Records.

A Corpus Generation must not characterize convergence, density, breadth, depth, producer diversity, modality diversity, epistemic diversity, temporal persistence, or biological meaning.

---

# Relationship To Evidence Convergence Surfaces

Corpus Generations may provide upstream scope for Evidence Convergence Surface construction indirectly through Evidence Topology and Convergence Geometry.

Evidence Convergence Surfaces must be constructed over Convergence Geometry.

Surface construction must preserve Corpus Generation lineage.

A Corpus Generation must not declare surface eligibility.

A Corpus Generation must not determine surface disclosure.

A Corpus Generation must not expose reasoning capacity by itself.

---

# Relationship To Projection Views

Corpus Generations may be inspected, summarized, or exported through Projection Views.

A projection over a Corpus Generation must declare:

```text
projection purpose
projection source layer
source Corpus Generation identity
source Registration Unit identities
source records
materialization status
lossiness status when applicable
reconstruction path
```

A Projection View over a Corpus Generation does not replace the Corpus Generation.

A Projection View does not acquire Corpus Generation authority.

---

# Relationship To RDGP Consumer Projections

RDGP-facing consumer projections may be generated from downstream surfaces or other governed VDB layers whose lineage includes a Corpus Generation.

RDGP-facing projections must preserve Corpus Generation lineage so that RDGP reasoning can later identify:

```text
which evidence generation was used
which Registration Units were selected
which producer families were represented
which evidence strata were available
which evidence strata were absent
whether the reasoning substrate was current or stale
```

A Corpus Generation does not perform RDGP reasoning.

A Corpus Generation does not decide whether evidence explains phenotype.

A Corpus Generation only declares the evidence scope available for downstream derivation and projection.

---

# Validation Obligations

Corpus Generation validation must confirm:

```text
Corpus Generation identity exists
Corpus Generation purpose is declared
selection policy is declared
included Registration Units are explicit
included Registration Units are resolvable
included Registration Units are readable
included Registration Units expose validation status
included Registration Units expose certification status when available
included Registration Unit boundaries remain intact
producer-family metadata is preserved
package identifiers are preserved
artifact counts are recorded when available
assertion registration counts are recorded when available
source identity counts are recorded when available
inclusion rationale is documented
exclusion rationale is documented when applicable
corpus manifest is deterministic
corpus scope is reconstructable
corpus generation does not mutate Registration Units
corpus generation does not become source truth
```

For the initial MARK Phase 4 benchmark corpus, validation should additionally confirm:

```text
expected six Registration Units are present
expected VAP Registration Units are present
expected GSC Registration Units are present
all expected Registration Units are readable
all expected Registration Units are certified
corpus identity is stable
corpus manifest is deterministic
```

---

# Anti-Collapse Rules

The following are prohibited:

```text
corpus scope collapse
Registration Unit boundary collapse
producer-family collapse
package identity collapse
artifact identity collapse
assertion registration collapse
source identity collapse
namespace collapse
validation status collapse
certification status collapse
inclusion rationale collapse
exclusion rationale collapse
Corpus Generation treated as source truth
materialized corpus treated as source truth
uncertified Registration Units silently included in a certified corpus
Registration Units merged without preserved boundaries
topology derived before corpus scope is declared
topology relationships created inside a Corpus Generation
geometry created inside a Corpus Generation
surface eligibility declared inside a Corpus Generation
projection output replacing a Corpus Generation
biological reasoning performed inside a Corpus Generation
destructive modification of Registration Units during Corpus Generation construction
```

Any implementation that performs one of these actions violates this contract.

---

# Exit Criteria

A Corpus Generation implementation is complete only when:

```text
Corpus Generation identity is stable
Corpus Generation purpose is declared
selection policy is declared
included Registration Units are explicit
included Registration Units are resolvable
Registration Unit boundaries are preserved
producer-family context is preserved
package identity is preserved
artifact counts are recorded when available
assertion registration counts are recorded when available
source identity counts are recorded when available
validation status is visible
certification status is visible when available
inclusion rationale is documented
exclusion rationale is documented when applicable
corpus manifest is deterministic
corpus scope is reconstructable
Corpus Generation does not mutate Registration Units
Corpus Generation can serve as input to Assertion Record indexing
anti-collapse validation passes
```

A Corpus Generation implementation is not complete merely because a file list exists.

A Corpus Generation implementation is complete only when that file list, manifest, database, index, or other representation satisfies this contract.

---

# Summary

A Corpus Generation is the declared evidence scope from which Phase 4 derived evidence structures are built.

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Topology derives organization.
```

Corpus Generations make Phase 4 derivation reproducible by declaring exactly which Registration Units are in scope.

They do not perform derivation themselves.

The guiding rule is:

```text
Declare the corpus.

Preserve Registration Unit boundaries.

Document inclusion and exclusion.

Remain materialization-neutral.

Never interpret the evidence.
```

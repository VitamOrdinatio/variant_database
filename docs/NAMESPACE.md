# NAMESPACE.md for `docs/`

**Documentation Namespace Topology = VDB documentation governance map**

> What does each documentation namespace govern, and how do we prevent semantic collapse as VDB matures?

VDB uses explicit documentation namespaces to preserve architectural clarity before implementation begins.

This matters because VDB is intended to become the ecosystem evidence nexus for:

* VAP-derived variant and telemetry substrates
* GSC-derived gene and phenotype overlays
* future RSP-derived expression or functional evidence
* RDGP-facing evidence query surfaces

The documentation topology exists to keep these responsibilities separated, reviewable, and implementable.

---

# Top-Level Documentation Namespaces

| Namespace         | Core identity                    |
| ----------------- | -------------------------------- |
| `architecture/`   | conceptual worldview             |
| `design/`         | subsystem operational strategy   |
| `interfaces/`     | cross-system communication       |
| `contracts/`      | guarantees and invariants        |
| `implementation/` | realized operational behavior    |
| `maps/`           | strategic milestone direction    |
| `plans/`          | future execution sequencing      |
| `validation/`     | proof and verification           |
| `examples/`       | illustrative concrete artifacts  |
| `status/`         | current maturity and checkpoints |
| `releases/`       | historical release states        |

---

# Nested Implementation Namespaces

| Namespace                        | Core identity                                |
| -------------------------------- | -------------------------------------------- |
| `implementation/schemas/`        | exact structural definitions                 |
| `implementation/specifications/` | formal implementation definitions            |
| `implementation/workflow/`       | realized orchestration flow                  |
| `implementation/queries/`        | stable query surfaces and retrieval patterns |

These namespaces live under `implementation/` because they describe concrete structures and behaviors that implementation must realize.

---

# Boundary Rules

`Architecture` defines what VDB is.

`Design` defines how major subsystems should behave.

`Interfaces` define how VDB communicates with other repositories.

`Contracts` define what VDB guarantees.

`Implementation` defines how those guarantees become operational.

`Validation` proves the guarantees are satisfied.

`Examples` make the abstractions concrete.

`Status` records current maturity.

`Releases` preserve historical milestones.

---

# Anti-Collapse Principle

VDB must not become:

* a pile of unrelated adapters
* a warehouse of unexplained tables
* a silent namespace-normalization black box
* an undocumented interoperability layer
* a collection of brittle one-off ingestion scripts

VDB should remain:

* governed
* auditable
* queryable
* provenance-preserving
* namespace-aware
* interoperable
* deterministic

---

# Reviewer Principle

Each namespace should help a reviewer answer one question quickly:

| Question                             | Namespace         |
| ------------------------------------ | ----------------- |
| What is VDB trying to be?            | `architecture/`   |
| How should each subsystem work?      | `design/`         |
| How do repos exchange evidence?      | `interfaces/`     |
| What must VDB guarantee?             | `contracts/`      |
| What structures and workflows exist? | `implementation/` |
| What was planned?                    | `plans/`          |
| What has been proven?                | `validation/`     |
| What can I inspect concretely?       | `examples/`       |
| What is the current state?           | `status/`         |
| What changed at release time?        | `releases/`       |

---

# Operator Principle

`README.md` files are for reviewer-facing orientation.

`NAMESPACE.md` files are for taxonomy, boundaries, and semantic governance.

Together they act as guardrails to prevent both:

* semantic collapse during implementation
* reviewer cognitive collapse during inspection

---

# Namespace Topology Reference

The appendices below collectively serve as the canonical namespace topology reference for VDB documentation governance.

Together they define:

* namespace identities
* namespace boundaries
* dependency relationships
* taxonomy groupings
* document placement authority
* namespace principles and anti-patterns
* constitutional authority relationships

These appendices should be consulted before introducing new documentation namespaces or placing new documents within existing namespaces.

---

# Appendix A: Namespace Fencepost Map

| Namespace                        | Core identity                 | Must answer                                                                  |
| -------------------------------- | ----------------------------- | ---------------------------------------------------------------------------- |
| `docs/`                          | documentation topology        | How is VDB documentation organized to prevent semantic collapse?             |
| `architecture/`                  | system worldview              | What is VDB philosophically and structurally?                                |
| `design/`                        | subsystem strategy            | How should major VDB subsystems behave?                                      |
| `interfaces/`                    | cross-repo communication      | How do VAP/GSC/RSP/RDGP exchange evidence with VDB?                          |
| `contracts/`                     | guarantees/invariants         | What does VDB promise to preserve or enforce?                                |
| `implementation/`                | realized operational behavior | How are architecture/design/contracts made concrete?                         |
| `implementation/schemas/`        | exact structures              | What fields, tables, records, and datatypes exist?                           |
| `implementation/specifications/` | formal definitions            | What rules govern valid artifacts, events, manifests, and transport objects? |
| `implementation/workflow/`       | operational sequence          | What steps occur from discovery through ingestion/query?                     |
| `implementation/queries/`        | stable retrieval surfaces     | What query outputs does VDB expose to downstream systems?                    |
| `maps/`                          | strategic direction           | What milestones define VDB’s intended maturation?                            |
| `plans/`                         | execution sequencing          | What work should be performed to implement VDB?                              |
| `validation/`                    | proof                         | How do we prove VDB behavior is correct and reproducible?                    |
| `examples/`                      | concrete artifacts            | What small examples make VDB behavior inspectable?                           |
| `status/`                        | current state                 | What is currently true about VDB maturity?                                   |
| `releases/`                      | historical milestones         | What changed at release checkpoints?                                         |

## Key boundary decisions:

1. To reduce reviewer burden:

   - `schemas/` and `specifications/` stay nested under `implementation/`, not top-level. 
   - `queries/` and `workflow/` also stay nested under `implementation/`, not top-level. 
 
2. `workflow/` is realized operational flow, not abstract architecture.

3. `interfaces/` and `contracts/` remain top-level because they are constitutional. 
   - Interfaces define cross-repo communication.
   - Maps define big-picture repo directionality / features.
   - Contracts define guarantees.
   - Plans define codebase implementation plans.

---

# Appendix B: Brief Namespace Identity Map

| Namespace | Identity |
|---|---|
| Architecture | System worldview |
| Design | Subsystem operational strategy |
| Interfaces | Cross-repository communication |
| Contracts | Guarantees and invariants |
| Implementation | Realized operational behavior |
| Schemas | Exact structures |
| Specifications | Formal implementation definitions |
| Workflow | Operational sequence |
| Queries | Stable retrieval surfaces |
| Validation | Proof |
| Plans | Execution sequencing |
| Maps | Strategic directionality |
| Status | Current repository state |
| Releases | Historical milestones |
| Examples | Concrete artifacts |

---

# Appendix C: Dependency Hierarchy


```text
Architecture
    ↓
Design
    ↓
Interfaces + Contracts
    ↓
Namespace Authority
    ↓
Implementation
    ↓
Validation
    ↓
Status
    ↓
Releases
```

```text
Implementation
    ├── Schemas
    ├── Specifications
    ├── Workflow
    └── Queries
```

```text
Maps
    ↓
Plans
    ↓
Implementation
```

```text
Examples
    ↓
Reviewer Understanding
```

---

# Appendix D: Namespace Group Taxonomy

Tiny classification shortcut:

```text
Taxon 1 = Constitution
Taxon 2 = Implementation realization
Taxon 3 = Governance lifecycle
Taxon 4 = Orientation
```

---

## Taxon 1 — Constitutional Namespace Layer

Taxon 1 defines the top-level governance perimeter for VDB documentation.

```text
docs/
docs/architecture/
docs/design/
docs/interfaces/
docs/contracts/
docs/implementation/
```

These namespaces establish:

- what VDB is
- how subsystems should behave
- how repositories communicate
- what guarantees VDB must preserve
- how those guarantees become operational

Taxon 1 is constitutional because mistakes here propagate into every downstream document and implementation decision.

---

## Taxon 2 — Implementation Subdomain Layer

Taxon 2 defines the nested implementation territories beneath implementation/.

```text
docs/implementation/schemas/
docs/implementation/specifications/
docs/implementation/workflow/
docs/implementation/queries/
```

These namespaces establish:

- structures
- rules
- sequences
- retrieval surfaces

Taxon 2 is implementation-facing because it governs how VDB’s architecture, design, interfaces, and contracts become concrete without collapsing into one undifferentiated implementation blob.

---

## Taxon 3 — Governance Lifecycle Layer

Taxon 3 governs how VDB is planned, verified, tracked, and released.

```text
docs/plans/
docs/validation/
docs/status/
docs/releases/
```

These namespaces establish:

* execution sequencing
* proof and verification
* repository maturity
* historical release state

Taxon 3 is governance-facing because it governs the lifecycle of VDB rather than the structure of VDB itself.

---

## Taxon 4 — Orientation Layer

Taxon 4 improves repository understanding, navigation, and adoption.

```text
docs/maps/
docs/examples/
```

These namespaces establish:

* strategic direction
* illustrative examples

Taxon 4 is reviewer-facing because it helps readers understand where VDB is going and what VDB looks like in practice.

---

# Appendix E: Detailed Namespace Principles & Anti-patterns

## Taxon 1 — Detailed Constitutional Namespace Layer

### Architecture

Principle: 

```text
Architecture defines enduring system truths.
```

Anti-pattern:

```text
Architecture documents should not contain implementation details,
schemas, query definitions, or validation procedures.
```

---

### Design

Principle:

```text
Design translates architectural intent into subsystem strategy.
```

Anti-pattern:

```text
Design documents should not become implementation plans,
task lists, or coding instructions.
```

---

### Interfaces

Principle:

```text
Interfaces preserve interoperability between repositories.
```

Anti-pattern:

```text
Interface documents should not define storage architecture,
persistence logic, or database internals.
```

---

### Contracts

Principle:

```text
Contracts define guarantees independent of implementation.
```

Anti-pattern:

```text
Contracts should not prescribe how guarantees are implemented.
```

---

### Implementation

Principle:

```text
Implementation realizes architecture, design, interfaces, and contracts.
```

Anti-pattern:

```text
Implementation documents should not redefine architecture,
change interface responsibilities, or alter contractual guarantees.
```

---

## Taxon 2 — Detailed Implementation Subdomain Layer

### Schemas

Principle:

```text
Schemas define exact structures that implementation must produce, store, or expose.
```

Anti-pattern:

```text
Schema documents should not explain system philosophy,
subsystem strategy, or cross-repository responsibilities.
```

---

### Specifications

Principle:

```text
Specifications define formal rules for valid implementation artifacts, events, manifests, and transport objects.
```

Anti-pattern:

```text
Specification documents should not become broad architecture documents
or informal design discussions.
```

---

### Workflow

Principle:

```text
Workflow documents define realized operational sequences.
```

Anti-pattern:

```text
Workflow documents should not redefine architecture,
invent new subsystem responsibilities, or replace implementation plans.
```

---

### Queries

Principle:

```text
Query documents define stable retrieval surfaces and downstream access patterns.
```

Anti-pattern:

```text
Query documents should not become persistence schemas,
storage policy documents, or downstream reasoning logic.
```

---

## Taxon 3 — Detailed Governance Lifecycle Layer

### Plans

Principle:

```text
Plans define future implementation sequencing.
```

Anti-pattern:

```text
Plans should not redefine architecture,
replace contracts, or document completed work.
```

---

### Validation

Principle:

```text
Validation proves that implementation satisfies contractual expectations.
```

Anti-pattern:

```text
Validation documents should not become implementation specifications
or future implementation plans.
```

---

### Status

Principle:

```text
Status documents communicate current repository maturity and progress.
```

Anti-pattern:

```text
Status documents should not become release histories
or implementation plans.
```

---

### Releases

Principle:

```text
Release documents preserve historical repository milestones.
```

Anti-pattern:

```text
Release documents should not describe future work
or current repository status.
```

---

## Taxon 4 — Detailed Orientation Layer

### Maps

Principle:

```text
Maps define strategic repository direction and long-term evolution.
```

Anti-pattern:

```text
Maps should not become implementation plans,
contracts, or subsystem designs.
```

---

### Examples

Principle:

```text
Examples make abstract VDB concepts concrete and inspectable.
```

Anti-pattern:

```text
Examples should not become canonical specifications,
contracts, or architectural authorities.
```

---

# Appendix F: Document Placement Examples

| Document | Correct Namespace | Why |
|---|---|---|
| vap_vdb_interface.md | interfaces/ | dominant function = cross-repo communication |
| artifact_manifest_spec.md | implementation/specifications/ | dominant function = formal artifact definition |
| relational_schema.md | implementation/schemas/ | dominant function = exact structure |
| query_surface_design.md | design/ | dominant function = subsystem strategy |
| rdgp_query_surface_schema.md | implementation/schemas/ | dominant function = output structure |
| rdgp_query_surface.md | implementation/queries/ | dominant function = retrieval behavior |

---

# Appendix G: Cross-cutting Architectural Taxonomy

```text
Variant Persistence      = VAP → VDB
Overlay Persistence      = GSC → VDB
Functional Persistence   = future RSP → VDB
Aggregation              = VDB → RDGP
Overlay Attachment       = GSC → RDGP / VDB-derived views
Identity Brokerage       = identity governance + preservation + routing
Identity-Space Bridging  = cross-space joins + map + reconcile
```

> Note the subtle difference that identity brokerage is governance while identity-space bridging is execution.

Examples:

| Operation class | Architecture                    | Design                         | Interface         | Schema/spec/query                       |
| --------------- | ------------------------------- | ------------------------------ | ----------------- | --------------------------------------- |
| Persistence     | evidence persistence philosophy | ingestion orchestration        | VAP→VDB           | provenance schema, ingestion event spec |
| Aggregation     | interoperability topology       | query surface design           | VDB→RDGP          | sample-gene evidence query              |
| Overlay         | ecosystem layer model           | query surface / overlay design | GSC↔VDB, GSC→RDGP | overlay attachment query/spec           |

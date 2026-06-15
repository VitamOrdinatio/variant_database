# README.md for `docs/`

![Figure 1. VDB — Semantic Persistence and Interoperability Nexus](architecture/figures/vdb_semantic_persistence_and_interoperability_nexus.png)


**Figure 1. VDB — Semantic Persistence and Interoperability Nexus.**
VDB functions as the ecosystem's persistence authority, identity brokerage layer, and system of record. Specialized repositories generate biological knowledge and evidence within their own identity spaces, while VDB preserves that evidence as durable, provenance-aware infrastructure. Persistent flows route through VDB for long-term retention, reproducibility, and discovery, whereas selected transient exchanges enable live interoperability between repositories without requiring persistence. This architecture enables downstream systems to consume preserved knowledge while maintaining source-scoped provenance, semantic integrity, and historical reproducibility.

# `NAMESPACE.md` Acts as Functional Taxonomy

Each `docs/` folder contains a dedicated `NAMESPACE.md` document which defines that folder's role and the underlying namespace governed by that folder's constituents.

# Folder Hierarchy For `docs/`

VDB utilizes an extensive collection of namespace identity to architecturally prevent semantic collapse.

| Namespace      | Core identity                    |
| -------------- | -------------------------------- |
| architecture   | conceptual worldview             |
| contracts      | guarantees/invariants            |
| design         | subsystem operational strategy   |
| examples       | illustrative concrete artifacts  |
| implementation | realized operational behavior    |
| interfaces     | cross-system communication       |
| maps           | maps for long-term repo strategy |
| plans          | implementation sequencing        |
| rationale      | justification of subsystems      |
| releases       | historical milestone states      |
| status         | current maturity/checkpoints     |
| validation     | proof and verification           |


Additionally, `docs/implementation` cleanly separates:

- `docs/implementation/queries`
- `docs/implementation/schemas`
- `docs/implementation/specifications`
- `docs/implementation/workflow`

| Namespace      | Core identity                    |
| -------------- | -------------------------------- |
| queries        | sql query framework / slices     |
| schemas        | exact structural definitions     |
| specifications | authoritative formal definitions |
| workflow       | orchestration/lifecycle flow     |


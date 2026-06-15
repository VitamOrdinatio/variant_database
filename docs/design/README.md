# README.md for `docs/design/`

# Scope

Design documents specifically address how major VDB subsystems behave.

Design should discuss:

- subsystem behavior
- responsibilities
- operational strategy

---

# Directory Inventory

```text
ingestion_orchestration_design.md
    How evidence moves through VDB intake as a coordinated subsystem.

namespace_resolution_engine_design.md
    How additive identity brokerage should operate.

vdb_discovery_engine_design.md
    describes the control plane

vdb_semantic_persistence_domains.md
    describes the destination plane

query_surface_design.md
    How persisted evidence becomes stable downstream-facing views.
```

| Design File                             | Purpose                              |
| --------------------------------------- | ------------------------------------ |
| `ingestion_orchestration_design.md`     | How do we handle arriving evidence?  |
| `namespace_resolution_engine_design.md` | How do identities relate?            |
| `vdb_discovery_engine_design.md`        | What is the VDB control plane?       |
| `vdb_semantic_persistence_domains.md`   | What is the VDB destination plane?   |
| `query_surface_design.md`               | How does evidence become consumable? |


Note that:

```text
Persistence Domain
        ≠
Query Surface
```

---

# Core Subsystem Behavior

```text
Discovery:
    discover → profile → map → validate → ingest

Persistence:
    organize evidence by semantic domain, not repo ownership
```

# Orchestration Design

```text
TEP Transport
    ↓
Discovery
    ↓
Validation
    ↓
Namespace Brokerage
    ↓
Persistence Routing
    ↓
Semantic Persistence Domains
    ↓
Query Surface Exposure
```

## Document-Level Orchestration

```text
vdb_discovery_engine_design (observe evidence)
        ↓
ingestion_orchestration_design (coordinate intake)
        ↓
namespace_resolution_engine_design (broker identities)
        ↓
vdb_semantic_persistence_domains (persist semantically)
        ↓
query_surface_design (expose consumable surfaces)
```


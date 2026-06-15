# Interfaces Namespace

Namespace: `docs/interfaces/`

**Interfaces = Cross-repository communication**

> Core question:
> How do external systems exchange evidence with VDB?

Examples:

- gsc_vdb_interface.md
- rsp_vdb_interface.md
- vap_vdb_interface.md
- vdb_rdgp_interface.md

Interface documents answer:

1. What information crosses system boundaries?
2. How is evidence exchanged?
3. What interoperability assumptions exist?
4. What responsibilities belong to each participating system?

Interfaces are:

- interoperability-focused
- boundary-oriented
- ecosystem-facing
- repository-independent

> Principle:
> Interfaces preserve interoperability between repositories.

> Anti-pattern:
> Interface documents should not define storage architecture,
> persistence logic, or database internals.

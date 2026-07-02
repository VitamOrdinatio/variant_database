# Phase 4.3C Assertion Record Layer 1 Tests

These tests define the local Layer 1 validation architecture for Phase 4.3 Assertion Records.

Layer 1 is intentionally synthetic and pytest-centered. It uses controlled mini-fixtures only. It does not use the compressed MARK-derived Layer 2 golden fixture and does not run against the full MARK corpus.

Layer boundaries:

```text
Layer 1:
    synthetic controlled mini-fixtures
    mostly sys76
    pytest-centered

Layer 2:
    compressed real-world data
    sys76 scripts/tests against committed golden fixture

Layer 3:
    non-compressed, non-synthetic, real-world data
    MARK full-corpus validation
```

Layer 1 proves that the Assertion Record builder preserves identity, lineage, role-bearing participants, relationship semantics, evidence basis, context, uncertainty/authority context, and explicit unsupported/deferred accounting without deriving topology or interpreting evidence.

These are implementation-driving tests. They may fail until the Phase 4.3 Assertion Record implementation modules are introduced.

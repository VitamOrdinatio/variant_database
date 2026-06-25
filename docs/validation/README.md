# README.md for `docs/validation/`

# Scope

Validation documentation describes how we can prove compliance.

# Validation Philosophy

```text
validation_strategy.md
    Why validate?

schema_validation.md
    Is the architecture coherent?

ingestion_validation.md
    Can evidence enter VDB safely?

namespace_resolution_validation.md
    Can identities be brokered safely?

vdb_end_to_end_lifecycle_walkthrough.md
    Can evidence survive the complete ecosystem lifecycle?
```

# Validation Execution

```text
validation_strategy.md
    master doctrine

schema_validation.md
    schema validation doctrine, defines concreate schema-coherence procedures

ingestion_validation.md
    ingestion validation doctrine

namespace_resolution_validation.md
    namespace validation doctrine

vdb_end_to_end_lifecycle_walkthrough.md
    lifecycle validation execution
```

# Test Taxonomy

```text
                MARK Canonical HG002
                     (13 GB)
                         ▲
                         │
              Lightweight HG002 Emulator
               (real structure, tiny data)
                         ▲
                         │
          Integration / Developer Scripts
                         ▲
                         │
               Synthetic Unit Tests
```

Each layer serves a different purpose.

```text
Synthetic Unit Tests
    Does this one function work?

Lightweight Emulator
    Does the VDB architecture work against a realistic TEP?

Canonical HG002 on MARK
    Does everything still work on production-scale evidence?
```
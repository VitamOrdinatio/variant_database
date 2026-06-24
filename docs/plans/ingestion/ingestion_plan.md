# ingestion_plan.md

## Purpose

This document defines the implementation plan for the VDB ingestion subsystem.

The ingestion subsystem is responsible for transferring producer evidence into VDB custody while preserving identity, provenance, authority, uncertainty, and reconstructability.

This plan translates:

```text
docs/contracts/ingestion/ingestion_contract.md
```

into a concrete implementation sequence.

---

# Relationship To Master Plan

This plan services:

```text
docs/plans/implementation_plan.md
```

and implements:

```text
docs/contracts/ingestion/ingestion_contract.md
```

The ingestion subsystem represents the first executable phase of VDB implementation.

No downstream subsystem may become authoritative until ingestion succeeds.

---

# Implementation Goal

The goal of the ingestion subsystem is:

```text
Prove that certified producer TEPs can enter VDB
custody without mutation while preserving
identity, provenance, authority, and evidence topology.
```

The purpose of ingestion is preservation.

The purpose of ingestion is not interpretation.

---

# Success Criteria

The ingestion subsystem is considered successful when VDB can:

```text
read certified producer TEPs

inventory TEP contents

inventory artifacts

inventory entities

inventory metadata

inventory provenance

emit deterministic ingestion reports

preserve producer immutability
```

without mutating producer artifacts.

---

# Initial Benchmark Artifacts

Initial implementation shall target the certified producer artifacts used during VDB architectural development.

## Certified TEP-VAP

```text
HG002

run_2026_06_03_010030
```

---

## Certified TEP-GSC

```text
Epilepsy

run_2026_06_22_184534
```

---

## Certified TEP-GSC

```text
Mitochondrial

run_2026_06_23_015533
```

These artifacts constitute the initial ingestion acceptance corpus.

---

# Phase 1 — Read-Only TEP Inspection

## Purpose

Verify that VDB can safely inspect certified producer artifacts.

## Expected Work

Implement:

```text
TEP path discovery

manifest discovery

artifact discovery

entity discovery

metadata discovery

provenance discovery
```

No persistence is required during this phase.

---

## Expected Outputs

```text
TEP inventory report

artifact inventory report

entity inventory report

metadata inventory report

provenance inventory report
```

---

## Exit Criteria

```text
all benchmark TEPs readable

all benchmark TEPs inventoryable

no producer artifacts modified

inspection reports deterministic
```

---

# Phase 2 — Package Registration

## Purpose

Register TEP packages within VDB custody.

## Expected Work

Implement:

```text
TEP Package Record creation

package identifier assignment

package metadata registration

schema version registration

producer registration
```

---

## Required Logical Output

```text
TEP Package Record
```

---

## Exit Criteria

```text
every benchmark TEP produces
a deterministic Package Record
```

---

# Phase 3 — Artifact Registration

## Purpose

Register artifacts transported by producer TEPs.

## Expected Work

Implement:

```text
artifact discovery

artifact classification

artifact registration

artifact lineage references

artifact checksum registration
```

when available.

---

## Required Logical Output

```text
Artifact Records
```

---

## Exit Criteria

```text
artifacts are inventoryable

artifacts remain reconstructable

artifact identity preserved
```

---

# Phase 4 — Entity Registration

## Purpose

Register entities represented within artifacts.

## Expected Work

Implement:

```text
entity discovery

entity classification

entity registration

entity source references
```

Examples include:

```text
genes

variants

samples

phenotypes

future entities
```

---

## Required Logical Output

```text
Entity Records
```

---

## Exit Criteria

```text
entities remain traceable
to source artifacts
```

---

# Phase 5 — Metadata Registration

## Purpose

Register metadata associated with ingested evidence.

## Expected Work

Implement registration of:

```text
producer metadata

repository metadata

release metadata

run metadata

package metadata

artifact metadata
```

---

## Required Logical Output

```text
Metadata Records
```

---

## Exit Criteria

```text
metadata remains reconstructable

metadata remains associated
with originating artifacts
```

---

# Phase 6 — Provenance Registration

## Purpose

Preserve provenance prior to evidence construction.

## Expected Work

Implement registration of:

```text
producer provenance

artifact provenance

package provenance

lineage references

generation context
```

---

## Required Logical Output

```text
Provenance Records
```

---

## Exit Criteria

```text
evidence origin reconstructable

artifact origin reconstructable

producer origin reconstructable
```

---

# Phase 7 — Ingestion Event Creation

## Purpose

Record custody transfer events.

## Expected Work

Implement:

```text
Ingestion Event creation

event timestamps

validation status

package references

operator context when appropriate
```

---

## Required Logical Output

```text
Ingestion Event
```

---

## Exit Criteria

```text
every successful ingestion
produces an Ingestion Event
```

---

# Phase 8 — Ingestion Reporting

## Purpose

Provide deterministic visibility into ingestion outcomes.

## Expected Work

Implement:

```text
human-readable reports

machine-readable reports

validation summaries

inventory summaries
```

---

## Required Logical Output

```text
ingestion_report.json

ingestion_report.md
```

or equivalent formats.

---

## Exit Criteria

```text
reports deterministic

reports reconstructable

reports traceable
```

---

# Proposed Module Structure

Initial implementation may utilize:

```text
src/variant_database/ingestion/

    package_scanner.py

    manifest_reader.py

    artifact_registry.py

    entity_registry.py

    metadata_registry.py

    provenance_registry.py

    ingestion_registry.py

    ingestion_reporter.py
```

Module names may evolve.

Responsibilities must remain intact.

---

# Test Strategy

Every ingestion component must include tests for:

```text
successful registration

missing artifacts

missing metadata

missing provenance

determinism

immutability

reconstructability
```

---

# Fixture Strategy

Use three fixture tiers.

## Tier 1

```text
synthetic minimal fixtures
```

Purpose:

```text
unit testing
```

---

## Tier 2

```text
small producer-derived fixtures
```

Purpose:

```text
integration testing
```

---

## Tier 3

```text
MARK-hosted certified TEPs
```

Purpose:

```text
acceptance testing
```

---

# Validation Gates

The ingestion subsystem must satisfy:

```text
docs/validation/ingestion_validation.md
```

Required gates include:

```text
TEP readability

artifact completeness

metadata completeness

provenance completeness

traceability

determinism

immutability
```

---

# Anti-Collapse Checks

The ingestion subsystem must verify that implementation does not:

```text
flatten TEPs into convenience tables

discard evidence

discard artifacts

discard provenance

discard metadata

replace source identity

collapse namespace information
```

These checks are mandatory.

---

# Future Benchmark Scenario

The ingestion subsystem must support eventual execution of:

```text
docs/examples/vdb_evidence_lifecycle_example.md
```

Specifically:

```text
HG002 POLG VAP evidence

+

Mitochondrial POLG GSC evidence
```

must remain preservable through ingestion.

No ingestion behavior may prevent later execution of the benchmark lifecycle.

---

# Definition Of Done

The ingestion subsystem is complete when:

```text
certified producer TEPs are readable

Package Records exist

Artifact Records exist

Entity Records exist

Metadata Records exist

Provenance Records exist

Ingestion Events exist

deterministic reports exist

validation passes

producer artifacts remain immutable
```

The ingestion subsystem is not complete merely because files can be parsed.

---

# Summary

The ingestion subsystem establishes the custody boundary of VDB.

Its purpose is to safely transfer producer evidence into VDB while preserving everything necessary for future discovery, interoperability, reasoning, and reconstruction.

The guiding implementation rule is:

```text
Read carefully.

Register faithfully.

Preserve completely.
```

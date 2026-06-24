# discovery_overlay_plan.md

## Purpose

This document defines the implementation plan for the VDB discovery and overlay attachment subsystem.

The discovery and overlay subsystem is responsible for identifying candidate evidence relationships and preserving overlay attachments while maintaining identity, provenance, authority, uncertainty, phenotype context, and reconstructability.

This plan translates:

`docs/contracts/discovery_overlay/discovery_overlay_contract.md`

into a concrete implementation sequence.

---

# Relationship To Master Plan

This plan services:

`docs/plans/implementation_plan.md`

and implements:

`docs/contracts/discovery_overlay/discovery_overlay_contract.md`

Discovery and overlay attachment correspond to Phase 5 of the master implementation plan.

---

# Implementation Goal

The goal of the discovery and overlay subsystem is:

```text
Create explicit, reconstructable evidence relationships
without fusing evidence across producers or domains.
```

The purpose of discovery is relationship detection.

The purpose of overlay attachment is relationship preservation.

---

# Initial Scope

Version 1 implementation focuses on:

```text
VAP-to-GSC gene-centered overlay attachment
```

The initial benchmark is:

```text
HG002 POLG VAP evidence

+

Mitochondrial POLG GSC semantic evidence
```

Future overlay domains may include:

```text
epilepsy GSC overlays

RSP transcriptomic overlays

external metadata overlays

RDGP-returned reasoning overlays
```

---

# Required Inputs

Version 1 depends upon:

```text
persisted Evidence Objects

persisted Evidence States

Namespace Events

Identity Bridges

GSC semantic evidence

VAP sample-gene evidence
```

Discovery and overlay attachment must not execute before persistence and namespace resolution prerequisites are satisfied.

---

# Proposed Module Structure

Initial implementation may utilize:

```text
src/variant_database/discovery_overlay/

    discovery_models.py

    overlay_models.py

    overlay_candidate_finder.py

    overlay_attachment_builder.py

    discovery_event_writer.py

    overlay_validator.py
```

Module names may evolve.

Responsibilities must remain intact.

---

# Phase 1 — Overlay Candidate Discovery

## Purpose

Identify candidate overlay relationships.

## Expected Work

Implement:

```text
read persisted VAP evidence

read persisted GSC evidence

read Identity Bridges

identify matching gene-centered overlay candidates

preserve discovery rationale

preserve namespace bridge references
```

## Expected Outputs

```text
overlay candidate records

Discovery Event records

candidate discovery report
```

## Exit Criteria

```text
HG002 POLG VAP evidence identified

mitochondrial POLG GSC evidence identified

candidate relationship detected through identity bridge

POLG2 does not participate in POLG overlay
```

---

# Phase 2 — Discovery Event Persistence

## Purpose

Persist discovery history.

## Expected Work

Implement:

```text
Discovery Event creation

Discovery Event persistence

discovery policy version recording

candidate evidence references

discovery rationale recording
```

## Expected Outputs

```text
Discovery Event records

discovery event retrieval API

discovery validation tests
```

## Exit Criteria

```text
discovery event reconstructable

candidate evidence reconstructable

discovery rationale visible
```

---

# Phase 3 — Overlay Attachment Construction

## Purpose

Create explicit overlay relationships.

## Expected Work

Implement:

```text
Overlay Attachment creation

primary evidence reference preservation

overlay evidence reference preservation

attachment basis preservation

phenotype context preservation

attachment uncertainty preservation

attachment provenance preservation
```

## Expected Outputs

```text
Overlay Attachment records

overlay attachment retrieval API

overlay attachment validation tests
```

## Exit Criteria

```text
primary evidence remains distinct

overlay evidence remains distinct

attachment rationale visible

phenotype context visible

attachment provenance visible
```

---

# Phase 4 — Overlay-Attached Evidence State

## Purpose

Represent overlay attachment as a new evidence state when required.

## Expected Work

Implement:

```text
derived overlay-attached Evidence State creation

Evidence State Transition creation

transition rationale preservation

source state preservation

destination state preservation
```

## Expected Outputs

```text
overlay-attached Evidence State records

Evidence State Transition records

state transition validation tests
```

## Exit Criteria

```text
prior states remain unchanged

overlay-attached state is additive

state transition reconstructable
```

---

# Phase 5 — Validation

## Purpose

Validate discovery and overlay preservation behavior.

## Validation Targets

```text
primary evidence preservation

overlay evidence preservation

attachment provenance

attachment rationale

phenotype context

namespace bridge provenance

uncertainty preservation

determinism

anti-collapse behavior
```

## Exit Criteria

```text
validation passes

anti-collapse checks pass

benchmark lifecycle remains executable
```

---

# Anti-Collapse Checks

The discovery and overlay subsystem must verify that implementation does not:

```text
merge VAP evidence with GSC evidence

replace VAP evidence with GSC evidence

replace GSC evidence with VAP evidence

hide phenotype context

hide namespace bridge uncertainty

hide attachment provenance

hide discovery provenance

collapse overlay attachment into primary evidence

collapse POLG into POLG2
```

These checks are mandatory.

---

# Future Benchmark Scenario

Discovery and overlay attachment must support eventual execution of:

`docs/examples/vdb_evidence_lifecycle_example.md`

Specifically:

```text
HG002 POLG VAP evidence

↓

Namespace bridge through ENSG00000140521

↓

Mitochondrial POLG GSC overlay attachment
```

must remain achievable.

No discovery or overlay behavior may prevent this benchmark lifecycle.

---

# Definition Of Done

The discovery and overlay subsystem is complete when:

```text
overlay candidates can be discovered

Discovery Events exist

Overlay Attachments exist

overlay-attached Evidence States exist when required

Evidence State Transitions exist when required

attachment rationale remains visible

phenotype context remains visible

namespace bridge provenance remains visible

validation passes

anti-collapse checks pass
```

The discovery and overlay subsystem is not complete merely because two records can be matched.

---

# Summary

The discovery and overlay subsystem exists to preserve evidence relationships.

Its purpose is to connect evidence without merging evidence.

The guiding implementation rule is:

```text
Find the relationship.

Record the attachment.

Preserve both sides.
```
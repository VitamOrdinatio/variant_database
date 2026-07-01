# Phase 4.3 Assertion Registration Reconnaissance Plan

**Status:** ACTIVE PHASE 4.3 RECONNAISSANCE PLAN

**Phase:** IV.3B — Registration Unit Reconnaissance

**Primary Validation Governance:** `docs/validation/assertion_record_validation.md`

**Primary Schema:** `docs/implementation/schemas/assertion_record_schema.md`

**Resolver Policy Model:** `docs/design/assertion_record_resolver_policy_model.md`

**Identity Preservation Model:** `docs/design/assertion_record_identity_preservation_model.md`

**MARK Reconnaissance Script:** `scripts/mark/run_phase4_3_assertion_registration_reconnaissance.py`

**Primary Reconnaissance Receipt Family:** `results/validation/phase4_assertion_records/`

**MARK Export Root:** `/root/Desktop/`

---

## Purpose

This document defines the Phase 4.3B reconnaissance plan for inspecting the assertion-registration substrate exposed by the six canonical MARK Registration Units.

The purpose of reconnaissance is to determine what producer assertion registrations are actually available before implementing the Phase 4.3 Assertion Record builder.

Reconnaissance answers:

```text
Which tables contain assertion registrations?
What columns exist?
How are VAP assertion registrations represented?
How are GSC assertion registrations represented?
Which source artifact references are available?
Which source identity references are available?
Are producer assertion IDs stable?
Do we need fallback source_assertion_key construction?
Which assertion registration types should be indexed in v1?
Which should be deferred but counted?
```

Reconnaissance is exploratory.

It does not create Assertion Records.

It does not derive Evidence Topology.

It does not characterize Convergence Geometry.

It does not construct Evidence Convergence Surfaces.

It does not emit Projection Views.

It does not perform RDGP reasoning.

---

# Governance Role

The governing Phase 4.3 transition is:

```text
Registration Units
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
```

The governing distinction is:

```text
Registration Units preserve custody.

Corpus Generations declare scope.

Assertion Records preserve scientific claims.

Evidence Topology derives organization.
```

Phase 4.3B reconnaissance sits between Corpus Generation closure and Assertion Record implementation.

It inspects the declared six-unit Corpus Generation to ground resolver policy, Layer 2 fixture construction, and Layer 3 MARK validation expectations in observed Registration Unit structure.

---

# Scope

The reconnaissance scope is the canonical six-unit MARK Corpus Generation:

```text
mark_phase4_corpus_6tep_v1
```

Canonical Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Required upstream handoff artifact:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

The reconnaissance script must consume this handoff artifact.

The reconnaissance script must not crawl Registration Unit folders opportunistically to define scope.

---

# MARK-First Scouting Rule

Production-grade reconnaissance should be performed on MARK.

MARK is the source compute environment for the heavy benchmark Registration Units and full corpus state.

The workflow is:

```text
1. Commit reconnaissance plan and script on sys76.
2. Push to git.
3. Pull the updated VDB repo on MARK.
4. Run the reconnaissance script on MARK from the VDB repo root.
5. Write receipts and archive to /root/Desktop/.
6. Download the TGZ and checksum from MARK.
7. Inspect the reconnaissance receipt before coding the Assertion Record builder.
```

MARK must not push changes.

MARK only runs reconnaissance and exports receipts.

---

# Required Inputs

Required script input:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

The downstream Assertion Record input manifest should provide or permit resolution of:

```text
corpus_generation_id
registration_unit_id
registration_unit_label
registration_unit_path
registration_unit_sqlite_path
producer_family
source_package_id
registration_backend
assertion_registration_count
source_identity_count
registration_unit_validation_status
registration_unit_certification_status
registration_unit_readiness_status
```

The script should tolerate missing recommended columns by reporting explicit unresolved state rather than failing prematurely when safe to continue.

The script should fail if no selected Registration Units can be resolved.

---

# Required Reconnaissance Questions

Reconnaissance must produce evidence addressing:

```text
Which SQLite tables exist per Registration Unit?
Which columns exist per table?
Which tables are likely assertion-registration tables?
Which columns are present in likely assertion-registration tables?
Which assertion registration types are observable?
Which source artifact references are present?
Which source identity references are present?
Which source row or source record references are present?
Which stable assertion registration identifiers are present?
Which producer families expose assertion registrations in compatible forms?
Which source_assertion_key strategy appears feasible?
Where fallback source_assertion_key construction is likely needed?
Which VAP assertion registration types appear indexable in v1?
Which GSC assertion registration types appear indexable in v1?
Which assertion registration types should be deferred, unsupported, or reviewed?
```

---

# Required Output Receipt Family

The MARK reconnaissance script should write a timestamped receipt directory under `/root/Desktop/` and produce a portable TGZ archive.

Recommended output directory pattern:

```text
/root/Desktop/assertion_registration_reconnaissance_<timestamp>/
```

Recommended archive pattern:

```text
/root/Desktop/assertion_registration_reconnaissance_<timestamp>.tgz
/root/Desktop/assertion_registration_reconnaissance_<timestamp>.tgz.sha256
```

Expected receipt files:

```text
README.md
reconnaissance_run_summary.json
reconnaissance_run_summary.tsv
registration_unit_table_inventory.tsv
registration_unit_column_inventory.tsv
assertion_registration_table_candidates.tsv
assertion_registration_column_inventory.tsv
assertion_registration_type_inventory.tsv
assertion_registration_sample_values.tsv
source_artifact_reference_inventory.tsv
source_identity_reference_inventory.tsv
producer_family_reconnaissance_summary.tsv
source_assertion_key_feasibility.tsv
resolver_scope_recommendations.tsv
non_mutation_summary.json
sidecar_check_summary.json
unresolved_questions.md
```

These receipts are exploratory.

They are not Assertion Record build artifacts.

They are not Phase 4.3 certification evidence by themselves.

They are inputs to Phase 4.3 architecture closure and implementation planning.

---

# Read-Only Requirements

Reconnaissance must be read-only with respect to selected Registration Units.

The script must:

```text
open SQLite databases using read-only mode
avoid writing inside Registration Unit directories
snapshot sidecar files before inspection
snapshot sidecar files after inspection
report whether sidecars appeared during inspection
write all reconnaissance outputs outside Registration Units
write MARK export artifacts to /root/Desktop/
```

The script must not:

```text
mutate Registration Unit SQLite files
create SQLite journal, WAL, or SHM sidecars in Registration Unit directories
rewrite Registration Unit metadata
rewrite Registration Unit manifests
write Assertion Record artifacts
write Evidence Topology artifacts
```

---

# Candidate Table Detection

Reconnaissance should not assume a single hard-coded table name.

It should prioritize likely tables including:

```text
assertion_registrations
assertion_registration
assertions
registered_assertions
source_identities
source_identity
artifacts
packages
metadata
```

It should also flag tables with names or columns containing terms such as:

```text
assertion
claim
relationship
participant
source_identity
source_artifact
artifact_id
package_id
producer_family
assertion_type
source_record
source_row
```

Candidate detection is heuristic.

Candidate detection does not determine final resolver behavior.

Observed structures must be reviewed before builder implementation.

---

# Source Assertion Key Feasibility

The reconnaissance receipt must evaluate source assertion key feasibility for candidate assertion-registration tables.

The feasibility summary should report:

```text
registration_unit_id
producer_family
candidate_table
has_source_assertion_registration_id
has_assertion_type
has_source_artifact_id
has_source_record_reference
has_source_row_reference
has_participant_fields
has_relationship_fields
preferred_key_strategy
fallback_key_strategy
fallback_required
key_risk_level
notes
```

Preferred source assertion key strategy:

```text
source_assertion_registration_id
```

Fallback source assertion key strategy may use a deterministic source-record fingerprint from:

```text
registration_unit_id
source_package_id
source_artifact_id
source_record_reference
relationship_or_relationship_class
participant_reference_fingerprint
assertion_type
producer_family
```

Fallback use must remain visible.

Fallback keys must not masquerade as native producer assertion identifiers.

---

# Resolver Scope Recommendations

The reconnaissance receipt should include a resolver-scope recommendation table.

Recommended fields:

```text
producer_family
registration_unit_id
observed_table
observed_assertion_registration_type
observed_row_count
recommended_v1_action
recommended_assertion_type
recommended_relationship_class
source_assertion_key_strategy
fallback_required
reason
notes
```

Allowed recommendation actions:

```text
index
index_with_note
defer
unsupported
not_applicable
needs_review
```

The reconnaissance script may generate conservative recommendations.

Final resolver policy remains a DEX-reviewed architecture decision.

---

# Relationship To Layer 2 Fixture

The reconnaissance receipt should inform construction of the Phase 4.3 Layer 2 compressed real-row golden fixture.

Layer 2 should include enough observed VAP and GSC assertion-bearing material to validate:

```text
VAP resolver behavior
GSC resolver behavior
source_assertion_key generation
fallback key reporting
participant mapping
relationship mapping
evidence basis mapping
context mapping
lineage mapping
unsupported/deferred accounting
deterministic output
anti-collapse behavior
```

Reconnaissance should identify which real rows should be candidates for fixture extraction.

Reconnaissance itself does not create the Layer 2 fixture.

---

# Relationship To Phase 4.3 Implementation

Reconnaissance must complete before Assertion Record builder implementation begins.

After reconnaissance, VDB should:

```text
inspect the reconnaissance receipt
patch resolver policy model if observed structures differ from assumptions
finalize VAP resolver v1 scope
finalize GSC resolver v1 scope
define Phase 4.3 Layer 2 fixture contents
then begin Assertion Record builder implementation
```

Coding the builder before reconnaissance risks hard-coding unobserved assumptions.

---

# Completion Criteria

Phase 4.3B reconnaissance is complete when:

```text
MARK reconnaissance script runs from the VDB repo root
script consumes the Phase 4.2 downstream Assertion Record input manifest
all six canonical Registration Units are inspected read-only
all SQLite tables are inventoried
all SQLite columns are inventoried
likely assertion-registration tables are identified
assertion registration types are summarized when observable
source artifact reference availability is summarized
source identity reference availability is summarized
source assertion key feasibility is summarized
resolver scope recommendations are emitted
non-mutation and sidecar checks are emitted
portable TGZ archive is written to /root/Desktop/
archive checksum is written to /root/Desktop/
no Assertion Records are emitted
no topology, geometry, surface, projection, or reasoning artifacts are emitted
```

---

# Summary

Phase 4.3B reconnaissance is the microscope pass before Assertion Record builder implementation.

The guiding rule is:

```text
Scout the declared corpus.

Inspect Registration Units read-only.

Inventory assertion-bearing material.

Ground resolver policy in observed reality.

Do not index yet.

Do not derive.

Do not interpret.
```

# Phase 4.3 Assertion Record Golden Fixture Contract

**Status:** ACTIVE PHASE 4.3 GOLDEN FIXTURE CONTRACT

**Phase:** IV.3 — Assertion Records

**Contract Family:** Golden Fixtures

**Contract ID:** `phase4_3_assertion_record_golden_fixture_contract`

**Fixture ID:** `phase4_3_assertion_record_golden_fixture_v1`

**Source Corpus Generation:** `mark_phase4_corpus_6tep_v1`

**Primary Assertion Record Schema:** `docs/implementation/schemas/assertion_record_schema.md`

**Primary Resolver Policy:** `docs/design/assertion_record_resolver_policy_model.md`

**Primary Validation Governance:** `docs/validation/assertion_record_validation.md`

**Sister Plan:** `docs/plans/golden_fixtures/phase4_3_assertion_record_golden_fixture_plan.md`

---

## Purpose

This contract defines the required obligations for the Phase 4.3 Assertion Record golden fixture.

The fixture exists to provide a committed, compressed, real-world-derived Layer 2 validation substrate for Assertion Record builder implementation.

This contract governs the Layer 2 golden fixture only.

Layer 1 uses synthetic or tightly controlled local fixtures and runs mostly on sys76 through pytest.

Layer 2 uses compressed real-world data derived from MARK, is committed under `tests/fixtures/`, and runs on sys76 through explicit validation scripts. Useful Layer 2 run artifacts may be stored when they clarify implementation behavior or preserve validation provenance.

Layer 3 uses non-compressed, non-synthetic, real-world data, runs on MARK against the full canonical corpus, and produces generated artifacts that are retrieved to sys76, staged, and committed strategically for git-tracked provenance.

The fixture must be small enough to commit.

The fixture must be rich enough to fail compact-but-flattened implementations.

The fixture must validate both:

```text
compact producer claim preservation
lossless source identity recoverability
```

This contract defines what the fixture must preserve, include, exclude, prove, and make invalid.

It does not define the operational extraction procedure.

The operational extraction and curation procedure belongs in:

```text
docs/plans/golden_fixtures/phase4_3_assertion_record_golden_fixture_plan.md
```

---

# Contract Role

The Phase 4.3 Assertion Record golden fixture is a governed validation fixture.

It is not a production Assertion Record Index.

It is not a Phase 4.3 certification receipt.

It is not Evidence Topology.

It is not Convergence Geometry.

It is not an Evidence Convergence Surface.

It is not a Projection View.

It is not RDGP reasoning.

It is a real-row fixture used to validate that the Assertion Record builder preserves producer claims while keeping the source identity universe reconstructable.

It is the Layer 2 fixture substrate in the Phase 4.3 validation ladder.

It is not the Layer 1 synthetic pytest fixture family.

It is not the Layer 3 MARK full-corpus smoketest.

---

# Relationship To Three-Layer Phase 4.3 Validation

Phase 4.3 validation uses a three-layer sequence.

```text
Layer 1:
    Synthetic or tightly controlled local tests.
    Runs mostly on sys76 through pytest.
    Proves builder mechanics, deterministic identity construction,
    validation vocabulary handling, failure-mode behavior, and anti-collapse
    safeguards under controlled inputs.

Layer 2:
    Compressed real-world golden fixture.
    Derived from MARK production-grade Registration Unit material.
    Curated and committed on sys76 under tests/fixtures/.
    Runs on sys76 through explicit scripts against the committed fixture.
    Proves real producer shape, source identity set recoverability,
    anti-flattening behavior, and resolver behavior without requiring full
    MARK-scale data.

Layer 3:
    Non-compressed, non-synthetic, real-world full-corpus smoketest.
    Runs on MARK against mark_phase4_corpus_6tep_v1.
    Uses full canonical Registration Unit data without fixture compression.
    Generated artifacts and validation receipts are retrieved to sys76,
    staged, and committed strategically for git-tracked provenance.
```

This contract governs Layer 2 only.

MARK may be used to extract a compressed candidate fixture package for Layer 2 because MARK holds the production-grade source material.

That extraction step is source acquisition for the fixture.

It is not Layer 2 validation execution.

It is not Layer 3 full-corpus validation.

Layer 2 validation execution must remain sys76-runnable against the committed compressed fixture.

---

# Governing Invariant

The governing invariant is:

```text
The Phase 4.3 Assertion Record golden fixture must validate both compact
claim preservation and lossless source identity recoverability.
```

The fixture is invalid if it validates compact Assertion Record creation while losing reconstructable access to the source identity universe attached to those records.

The fixture must prevent the following failure mode:

```text
assertion_registrations become compact Assertion Records
source_identities are ignored
participants are reduced to example rows
non-annotated variant identities are lost
noncoding variant identities are lost
downstream topology receives an impoverished substrate
```

The fixture must preserve the distinction between:

```text
Assertion Records:
    compact producer claim containers

Source Identity Sets:
    reconstructable participant/evidence universes attached to those claims
```

---

# Relationship To Phase 4.3

The governing Phase 4.3 chain is:

```text
Registration Units
        ↓
Corpus Generation
        ↓
Assertion Records
        ↓
Evidence Topology
```

The golden fixture validates the transition from selected Registration Unit substrate into Assertion Record builder inputs and expected outputs.

It must validate that the Assertion Record layer:

```text
consumes declared Corpus Generation scope
preserves producer assertion registrations
preserves source assertion identity
preserves source artifact lineage
preserves source identity recoverability
preserves role-bearing participant semantics
preserves relationship semantics
preserves evidence basis
preserves context
preserves authority and uncertainty context
emits deterministic expected outputs
does not derive topology
does not interpret biology
```

---

# Relationship To Existing Golden Fixture Governance

This contract extends the existing VDB golden fixture governance pattern.

The existing Phase 4 Registration Unit golden fixture contract and plan govern earlier Registration Unit and Corpus Generation fixture substrate.

This contract governs the next Layer 2 fixture family:

```text
Phase 4.1 / 4.2:
    Registration Unit golden fixture contract and plan

Phase 4.3:
    Assertion Record golden fixture contract and plan
```

The Assertion Record golden fixture must remain consistent with earlier golden fixture governance while addressing Phase 4.3-specific preservation obligations.

---

# Source Authority

The authoritative source corpus is:

```text
mark_phase4_corpus_6tep_v1
```

The authoritative upstream handoff is:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

The authoritative production source machine for fixture extraction is:

```text
MARK
```

MARK provides the production-grade Registration Unit material from which the compressed Layer 2 fixture is extracted.

MARK is not the Layer 2 validation execution authority.

After extraction, the candidate fixture package must be retrieved to sys76, reviewed, curated, and committed before Layer 2 validation is run.

The fixture must not be fabricated from synthetic-only local data.

The fixture may contain compressed slices of production-derived records.

The fixture must preserve enough source lineage to prove how each slice traces back to the selected Corpus Generation and Registration Units.

---

# Required Registration Unit Scope

The fixture must represent the six canonical Registration Units selected by the initial Phase 4.3 corpus:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

If one of these Registration Units is omitted from a fixture version, the omission must be explicit, justified, and validation-visible.

Silent omission is prohibited.

The preferred fixture includes representative substrate from all six Registration Units.

---

# Required Input Substrate

The fixture must include or reconstructably represent the following Registration Unit substrate families:

```text
assertion_registrations
source_identities
artifacts
tep_packages
schema_metadata
```

The fixture must also include or reconstructably represent:

```text
downstream Assertion Record input manifest slice
Registration Unit lineage metadata
Corpus Generation lineage metadata
source package references
source artifact references
source assertion registration references
source identity set references
```

The fixture must not rely on opportunistic filesystem discovery.

Fixture scope must be declared explicitly.

---

# Assertion Registration Obligations

The fixture should include all assertion registration rows from the six selected Registration Units when feasible.

At minimum, the fixture must include enough assertion registrations to cover all producer families and assertion type classes needed by the Phase 4.3 builder.

The fixture must preserve:

```text
assertion_registration_id
package_id
artifact_id
surface_role
evidence_domain
producer_family
source_record_ref
assertion_type
participant_summary_json
support_ref_json
authority_context
uncertainty_context
registration_status
payload_json
```

When a field is absent, unavailable, or unresolved in source material, that state must be explicit in fixture metadata or expected validation output.

Assertion registration rows are the primary claim-container substrate for Phase 4.3.

They must not be replaced by artifact rows.

They must not be replaced by source identity rows.

---

# Source Identity Recoverability Obligations

Source identity recoverability is a first-class obligation of this contract.

The fixture must preserve source identity recoverability for the source identity universe attached to selected assertion registrations.

The fixture may use compressed source identity slices.

The fixture may use source identity set references.

The fixture does not need to duplicate full production-scale source identity tables.

However, the fixture must prove that source identity collections can remain losslessly reconstructable by reference when full duplication is impractical.

The fixture must include or enable expected outputs for:

```text
assertion_record_source_identity_sets.tsv
assertion_record_source_identity_summary.tsv
```

The fixture is invalid if source identities are represented only by one or more example participants while the larger attached source identity universe is discarded.

The fixture must preserve:

```text
source_identity_id when included
assertion_registration_id
identity_kind
participant_role
source_value
source_namespace
source_label
extraction_method
source_record_ref
payload_json when needed
```

The fixture must preserve enough source identity diversity to detect implementations that silently:

```text
drop non-annotated variants
drop noncoding variants
drop unprioritized variants
drop source-native identities
drop participant roles
drop source namespaces
collapse many source identities into one example participant
```

When noncoding status is explicitly available in source material, the fixture must include noncoding examples.

When noncoding status is not explicitly available, the fixture must preserve variant identities broadly enough that downstream layers can recover, classify, or annotate noncoding status later.

Phase 4.3 must preserve evidence.

It must not over-interpret evidence.

---

# VAP Coverage Requirements

The fixture must include VAP-derived substrate from the four canonical VAP Registration Units:

```text
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

The fixture should exercise VAP assertion registration types observed or expected for the canonical corpus, including:

```text
variant_observation
variant_normalization
variant_interpretation
variant_prioritization
validation
candidate_routing
```

The fixture must preserve VAP source identity recoverability across relevant source identity classes when present:

```text
sample identities
variant identities
gene identities
transcript identities
annotation source identities
clinical label identities
consequence identities
priority tier identities
pipeline stage identities
validation method identities
source namespaces
source labels
source record references
```

The fixture must guard against annotated-only, prioritized-only, clinically labeled-only, and coding-only flattening.

The fixture must not require Phase 4.3 to biologically interpret noncoding variant consequence.

It must require that non-annotated and noncoding variant identities remain reconstructable when present in selected Registration Units.

---

# GSC Coverage Requirements

The fixture must include GSC-derived substrate from the two canonical GSC Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
```

The fixture should exercise GSC assertion registration types observed or expected for the canonical corpus, including:

```text
phenotype_gene_semantic_prior
phenotype_gene_provenance
source_gene_relationship
aggregation_support
source_contribution_topology
producer_contract_validation
```

The fixture must preserve GSC source identity recoverability across relevant source identity classes when present:

```text
phenotype identities
gene identities
source identities
semantic channel identities
evidence source identities
method identities
release identities
source namespaces
source labels
source record references
```

The fixture may preserve `source_contribution_topology` as a GSC producer-emitted assertion type.

The fixture must not treat `source_contribution_topology` as VDB-derived Evidence Topology.

The fixture must not collapse phenotype-scoped semantic priors into general gene truth claims.

---

# Required Fixture Artifact Family

A complete committed fixture should contain an inspectable fixture family under a stable test fixture directory.

The expected committed location is:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
```

The fixture family should include:

```text
README.md
fixture_manifest.json
fixture_manifest.tsv
input/
registration_units/
expected/
```

The exact operational layout is defined by the sister plan.

This contract requires that the layout preserve:

```text
fixture identity
contract identity
source corpus identity
Registration Unit scope
source table slices
expected output snapshots
validation expectations
lineage and reconstruction notes
known limitations
```

---

# Required Source Table Slice Obligations

The fixture must include source table slices sufficient to exercise the Assertion Record builder.

Required source table slice families:

```text
assertion_registrations.slice.tsv
source_identities.slice.tsv
artifacts.slice.tsv
tep_packages.slice.tsv
schema_metadata.slice.tsv
```

For each slice, fixture metadata must preserve:

```text
source Registration Unit
source table name
source row count in slice
selection policy
known omissions
checksum or integrity metadata when available
```

The fixture may use one file per Registration Unit or a combined file with `registration_unit_id`.

The plan may decide the operational layout.

---

# Expected Output Snapshot Obligations

A complete fixture must define expected output snapshots for the Assertion Record builder.

Expected output snapshots should include:

```text
expected_assertion_record_index.tsv
expected_assertion_record_index.jsonl
expected_assertion_record_source_identity_sets.tsv
expected_assertion_record_source_identity_summary.tsv
expected_assertion_record_participants.tsv
expected_assertion_record_relationships.tsv
expected_assertion_record_evidence_basis.tsv
expected_assertion_record_context.tsv
expected_assertion_record_lineage.tsv
expected_assertion_record_payload_references.tsv
expected_downstream_topology_input_manifest.tsv
expected_validation_summary.json
```

Expected outputs must prove preservation behavior.

They must not embed topology, geometry, surface, projection, RDGP, biological truth, clinical actionability, or causality authority.

Expected outputs may include `indexed_with_note`, `deferred`, or `unsupported_assertion_type` states where appropriate.

Silent exclusion is prohibited.

---

# Compression And Sampling Rules

The fixture may be compressed relative to full MARK production data.

Compression must be deterministic.

Compression must be documented.

Compression must be validation-visible.

Allowed compression approaches include:

```text
all assertion registrations with stratified source identity slices
all referenced artifact rows
all referenced package rows
minimal schema metadata required for context
source identity summary rows grouped by assertion registration, role, kind, and namespace
small example source identity rows for inspection
```

Disallowed compression approaches include:

```text
random-only sampling without deterministic seed and policy
annotated-only VAP variant sampling
prioritized-only VAP variant sampling
coding-only VAP variant sampling when broader variant identities are available
single-example participant replacement for large source identity sets
dropping source namespaces
dropping participant roles
dropping source record references
dropping Registration Unit lineage
dropping Corpus Generation lineage
```

The fixture should be compact.

It must not be biologically impoverished.

---

# Non-Goals

The Phase 4.3 Assertion Record golden fixture does not:

```text
certify Phase 4.3
replace Layer 1 synthetic pytest validation
replace Layer 3 MARK full-corpus validation
replace MARK full-corpus validation
replace Registration Units
replace Corpus Generation artifacts
create production Assertion Records
derive Evidence Topology
characterize Convergence Geometry
construct Evidence Convergence Surfaces
emit Projection Views
perform RDGP reasoning
rank genes
rank variants
assign biological truth
assign clinical actionability
establish causality
```

The fixture is a Layer 2 validation substrate.

It must remain sys76-runnable after curation and commit.

It must not be treated as the Layer 3 uncompressed MARK benchmark.

---

# Invalid Fixture Conditions

A fixture is invalid if it:

```text
omits canonical Registration Unit families without explicit justification
omits assertion_registrations
omits source identity coverage
represents source identities only as one or more example participants
cannot reconstruct source identity set membership
drops non-annotated VAP variant identities when present
drops noncoding VAP variant identities when present or recoverable
restricts VAP evidence to annotated variants without explicit downstream projection status
restricts VAP evidence to prioritized variants without explicit downstream projection status
collapses source-native identifiers into canonical identifiers
collapses participant roles
collapses source namespaces
collapses assertion registrations into artifacts
collapses source identities into Assertion Records
derives VDB Evidence Topology during fixture construction
emits Convergence Geometry during fixture construction
constructs Evidence Convergence Surfaces during fixture construction
emits Projection Views during fixture construction
performs RDGP reasoning
removes Registration Unit lineage
removes Corpus Generation lineage
removes source artifact lineage
removes payload reconstruction paths
silently skips unsupported assertion registrations
silently skips deferred assertion registrations
uses manual expected outputs without declared generation or review status
```

A fixture that passes tests while allowing these failures is not contract-compliant.

---

# Validation Obligations

The fixture must support Layer 2 validation of:

```text
input scope preservation
Registration Unit lineage preservation
Corpus Generation lineage preservation
assertion registration preservation
source assertion key behavior
source identity set recoverability
source identity summary behavior
VAP resolver behavior
GSC resolver behavior
participant mapping behavior
relationship mapping behavior
evidence basis mapping behavior
context mapping behavior
lineage mapping behavior
payload reference behavior
unsupported assertion accounting
deferred assertion accounting
deterministic output generation
anti-collapse safeguards
```

The fixture must support negative or failure-mode checks for anti-flattening behavior.

At minimum, a builder should fail Layer 2 validation if it emits compact Assertion Records while losing reconstructable source identity set access.

---

# Anti-Flattening Requirements

The fixture must protect the discovery mission of VDB.

A compliant fixture must detect and reject implementations that flatten evidence into annotated or prioritized summaries only.

The fixture must preserve enough source identity diversity to support future downstream questions such as:

```text
Which non-annotated variant identities remain attached to this VAP assertion?

Can downstream topology recover the variant identity universe attached to this assertion?

Can downstream layers later classify noncoding burden without rerunning VAP?

Can phenotype-gene semantic prior evidence remain separable from variant evidence?

Can producer-native identities be reconstructed after Assertion Record indexing?
```

The fixture must therefore validate evidence preservation, not merely row creation.

---

# Acceptance Criteria

The fixture contract is satisfied when a committed fixture can demonstrate that:

```text
fixture identity is declared
contract identity is declared
source corpus identity is declared
all six canonical Registration Units are represented or omissions are explicit
assertion_registrations are included
source_identities are included or represented by lossless set references
artifacts are included or represented by reconstructable references
tep_packages are included or represented by reconstructable references
schema metadata needed for context is included
VAP assertion registration types are represented
GSC assertion registration types are represented
VAP source identity recoverability is represented
GSC source identity recoverability is represented
non-annotated VAP variant identities remain reconstructable when present
noncoding VAP variant identities remain reconstructable when present or later classifiable
expected Assertion Record outputs are declared
expected source identity set outputs are declared
expected validation summary is declared
fixture compression policy is visible
fixture limitations are visible
anti-flattening checks are possible
Layer 2 remains compressed, sys76-runnable, and distinct from Layer 3 MARK full-corpus validation
topology is not derived
geometry is not characterized
surfaces are not constructed
projections are not emitted
RDGP reasoning is not performed
biological truth is not assigned
clinical actionability is not assigned
```

The fixture is not contract-compliant merely because it is small, convenient, or easy to test.

It is contract-compliant only if it preserves the discovery-critical substrate required by Phase 4.3.

---

# Summary

The Phase 4.3 Assertion Record golden fixture contract governs the Layer 2 real-row fixture for Assertion Record implementation.

The guiding rule is:

```text
Preserve compact producer claim containers.

Preserve source identity recoverability.

Keep the fixture small enough to commit.

Keep the fixture rich enough to fail flattened implementations.

Do not derive.

Do not interpret.

Do not discard discovery substrate.
```

A compliant fixture must prove that Assertion Record indexing can preserve producer scientific claims without severing access to the large participant, variant, gene, phenotype, source, and evidence identity universe attached to those claims.

It must do this as Layer 2: compressed, real-world-derived, committed, sys76-runnable, and clearly distinct from both Layer 1 synthetic pytest validation and Layer 3 uncompressed MARK full-corpus validation.

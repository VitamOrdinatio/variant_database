# Phase 4.3 Assertion Record Golden Fixture Plan

**Status:** ACTIVE PHASE 4.3 GOLDEN FIXTURE PLAN

**Phase:** IV.3 — Assertion Records

**Plan Family:** Golden Fixtures

**Plan ID:** `phase4_3_assertion_record_golden_fixture_plan`

**Fixture ID:** `phase4_3_assertion_record_golden_fixture_v1`

**Governing Contract:** `docs/contracts/golden_fixtures/phase4_3_assertion_record_golden_fixture_contract.md`

**Source Corpus Generation:** `mark_phase4_corpus_6tep_v1`

**Primary MARK Extraction Script:** `scripts/mark/build_phase4_3_assertion_record_golden_fixture.py`

**Candidate MARK Output Family:** `/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>/`

**Committed Fixture Target:** `tests/fixtures/phase4/assertion_records/golden_fixture/`

---

## Purpose

This plan defines the operational workflow for constructing, exporting, reviewing, curating, and committing the Phase 4.3 Assertion Record golden fixture.

The governing contract defines what the fixture must preserve, include, exclude, prove, and make invalid.

This plan defines how the fixture should be produced and curated.

The fixture exists to provide a committed, compressed, real-world-derived Layer 2 validation substrate for Assertion Record builder implementation.

This plan governs Layer 2 fixture construction and curation.

It does not govern Layer 1 synthetic pytest validation except where Layer 1 depends on builder mechanics shared with later layers.

It does not govern Layer 3 MARK full-corpus validation except by preserving a clear boundary between compressed sys76-runnable fixture validation and uncompressed MARK production-scale validation.

The fixture must validate both:

```text
compact producer claim preservation
lossless source identity recoverability
```

The fixture must be small enough to commit.

The fixture must be rich enough to fail compact-but-flattened implementations.

---

# Plan Role

This plan governs the fixture construction workflow.

It does not replace the governing contract.

It does not define Assertion Record production behavior.

It does not certify Phase 4.3.

It defines the path from production-grade MARK source material to a curated sys76-committed golden fixture.

The MARK step in this plan is fixture extraction, not Layer 2 validation execution.

Layer 2 validation execution occurs on sys76 against the committed compressed fixture.

Layer 3 validation execution occurs separately on MARK against non-compressed real-world data.

The governing machine doctrine is:

```text
MARK scouts and exports.

sys76 curates, commits, and pushes.
```

MARK must not be used as the git push authority for this fixture.

---

# Governing Contract

This plan is subordinate to:

```text
docs/contracts/golden_fixtures/phase4_3_assertion_record_golden_fixture_contract.md
```

If this plan conflicts with the contract, the contract governs.

The central contract invariant is:

```text
The Phase 4.3 Assertion Record golden fixture must validate both compact
claim preservation and lossless source identity recoverability.
```

The plan must therefore produce a fixture that can detect and reject an implementation that indexes compact Assertion Records while losing reconstructable source identity set access.

---

# Relationship To Three-Layer Phase 4.3 Validation

Phase 4.3 validation uses a three-layer sequence.

```text
Layer 1:
    Synthetic or tightly controlled tests.
    Runs mostly on sys76 through pytest.
    Uses synthetic/local fixture material only.
    Proves local mechanics, deterministic behavior, failure-mode handling,
    and anti-collapse safeguards under controlled inputs.

Layer 2:
    Compressed real-world golden fixture.
    Extracted from MARK production-grade source material.
    Curated and committed on sys76 under tests/fixtures/.
    Runs on sys76 using explicit scripts against the committed fixture.
    May optionally store useful script-generated artifacts when they aid
    review, debugging, or provenance.
    Proves real producer shape, source identity set recoverability,
    anti-flattening behavior, and resolver behavior at commit-friendly scale.

Layer 3:
    Non-compressed, non-synthetic, real-world full-corpus smoketest.
    Runs on MARK against mark_phase4_corpus_6tep_v1.
    Uses actual canonical Registration Unit data without compression.
    Generated artifacts and validation receipts are retrieved to sys76,
    staged, and committed strategically for git-tracked provenance.
```

This plan is specifically a Layer 2 fixture plan.

The plan may use MARK to extract the compressed Layer 2 fixture candidate because MARK holds production-grade data.

That extraction is not a Layer 2 validation run.

Layer 2 validation must remain sys76-runnable after the fixture is curated and committed.

Layer 3 must remain a separate MARK-only, uncompressed, full-corpus validation event.

---

# Fixture Maturity States

The fixture may pass through two maturity states.

## Candidate Extraction Package

A candidate extraction package is produced on MARK.

It contains compressed real-world source slices, manifests, summaries, contract-alignment reports, checksums, and placeholder expected-output metadata.

A candidate extraction package is not automatically a committed fixture.

It is not a Layer 2 validation run.

It is not a Layer 3 full-corpus smoketest.

It must be reviewed on sys76 before curation.

## Committed Executable Fixture

A committed executable fixture lives under:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
```

It contains curated compressed real-world source slices, manifests, summaries, contract-alignment notes, and expected output snapshots when available.

This is the substrate used by Layer 2 sys76 scripts.

It is intentionally smaller than the Layer 3 MARK full-corpus substrate.

Expected outputs may be introduced in a second fixture curation pass after the Assertion Record builder emits draft outputs and DEX review accepts them as contract-compliant snapshots.

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

The source machine for fixture extraction is:

```text
MARK
```

The fixture must be derived from production-grade Registration Unit material available on MARK.

MARK extraction produces a compressed candidate fixture package for later sys76 curation.

MARK extraction does not replace Layer 2 sys76 execution and does not replace Layer 3 full-corpus validation.

The MARK extraction script must consume the governed downstream Assertion Record input manifest.

The extraction script must not discover scope by opportunistic filesystem traversal.

---

# Registration Unit Scope

The fixture should represent all six canonical Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

If a Registration Unit is omitted from a candidate fixture, the omission must be explicit in:

```text
extraction_summary.tsv
contract_alignment_summary.tsv
fixture_limitations.md
```

Silent omission is prohibited.

---

# Workflow Overview

The operational workflow is:

```text
1. Draft and commit this plan.
2. Draft and commit the MARK extraction script.
3. Pull latest VDB on MARK.
4. Run the extraction script on MARK from the VDB repo root.
5. Write compressed candidate fixture output to /root/Desktop/.
6. Download candidate fixture TGZ and checksum to sys76.
7. Verify checksum on sys76.
8. Inspect extraction and contract-alignment summaries.
9. Curate acceptable fixture material into tests/fixtures/.
10. Commit curated fixture from sys76.
11. Run Layer 2 Assertion Record builder scripts on sys76 against the committed fixture.
12. Optionally preserve useful Layer 2 generated artifacts when they aid review or provenance.
13. Add or refresh expected output snapshots after builder behavior is reviewed.
14. Later, run Layer 3 full-corpus validation separately on MARK against uncompressed real-world data.
15. Retrieve Layer 3 generated artifacts and receipts to sys76, stage, and commit strategically for provenance.
```

---

# Phase A — MARK Extraction Of Compressed Layer 2 Candidate

This phase extracts a compressed Layer 2 candidate fixture from production-grade MARK material.

It is not Layer 2 validation execution.

It is not Layer 3 full-corpus validation.

The MARK extraction script should be:

```text
scripts/mark/build_phase4_3_assertion_record_golden_fixture.py
```

The script should be run from the VDB repo root on MARK:

```bash
python3 scripts/mark/build_phase4_3_assertion_record_golden_fixture.py
```

Default input:

```text
results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/downstream_assertion_record_input_manifest.tsv
```

Default output:

```text
/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>/
/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>.tgz
/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>.tgz.sha256
```

The script must open selected Registration Unit SQLite databases read-only.

The script must not mutate Registration Units.

The script must not create Assertion Record production artifacts.

The script must not derive topology.

The script must not produce Projection Views.

---

# Phase B — Candidate Fixture Package Layout

A MARK candidate package should use this layout:

```text
phase4_3_assertion_record_golden_fixture_<timestamp>/
    README.md
    extraction_manifest.json
    extraction_manifest.tsv
    extraction_summary.json
    extraction_summary.tsv
    fixture_limitations.md
    input/
        downstream_assertion_record_input_manifest.slice.tsv
        selected_registration_units.tsv
    registration_units/
        gsc_epilepsy/
        gsc_mitochondrial_disease/
        vap_hg002/
        vap_median_ERR10619300/
        vap_q1_ERR10619212/
        vap_q3_ERR10619225/
    expected/
        expected_output_placeholder_manifest.tsv
    validation/
        contract_alignment_summary.json
        contract_alignment_summary.tsv
        source_identity_recoverability_summary.tsv
        anti_flattening_coverage_summary.tsv
    checksums/
        file_manifest.sha256
```

Each Registration Unit directory should contain:

```text
registration_units/<registration_unit_id>/
    assertion_registrations.slice.tsv
    source_identities.slice.tsv
    source_identity_summary.tsv
    source_identity_set_candidates.tsv
    artifacts.slice.tsv
    tep_packages.slice.tsv
    schema_metadata.slice.tsv
```

If a table is unavailable or empty, the file may be empty, but the state must be explicit in extraction summaries.

---

# Phase C — Source Table Slice Policy

The extractor should emit source table slices sufficient to exercise the Assertion Record builder.

Required source table families:

```text
assertion_registrations
source_identities
artifacts
tep_packages
schema_metadata
```

For `assertion_registrations`, the preferred policy is:

```text
include all assertion_registration rows from all six selected Registration Units
```

For `artifacts`, the preferred policy is:

```text
include all artifact rows referenced by selected assertion_registrations
include additional manifest or package-supporting artifact rows when needed for reconstruction
```

For `tep_packages`, the preferred policy is:

```text
include all package rows referenced by selected assertion_registrations
```

For `schema_metadata`, the preferred policy is:

```text
include minimal complete schema metadata needed to preserve context and verify Registration Unit shape
```

The extractor must preserve `registration_unit_id` in all emitted slice files.

---

# Phase D — Source Identity Slice Policy

The extractor must preserve source identity recoverability without duplicating the full MARK-scale source identity universe.

For every selected `assertion_registration_id`, the extractor should emit source identity summaries grouped by:

```text
registration_unit_id
assertion_registration_id
identity_kind
participant_role
source_namespace
```

For every selected `assertion_registration_id`, the extractor should emit source identity set candidate rows containing:

```text
registration_unit_id
source_assertion_registration_id
source_identity_table_reference
source_identity_filter
identity_kind
participant_role
source_namespace
source_identity_count
lossiness_status
resolution_status
validation_status
```

The canonical reconstructable filter should be:

```text
assertion_registration_id=<source_assertion_registration_id>
```

when that filter is sufficient.

The bounded source identity row slice should be deterministic.

Recommended deterministic selection policy:

```text
group source_identities by registration_unit_id, assertion_registration_id,
identity_kind, participant_role, and source_namespace

within each group, sort by source_identity_id, source_record_ref, source_value

select the first K rows per group
select the last K rows per group when the group is large
include rows with non-null source_record_ref when available
include rows with null or unresolved source_record_ref when available
include variant identity rows when present
include sample, gene, transcript, phenotype, source, and semantic-channel rows when present
```

The initial recommended `K` is:

```text
K = 3
```

The MARK extractor may expose `K` as a command-line parameter.

Random sampling is not preferred.

If random sampling is used for supplemental inspection, it must use a declared deterministic seed and must not replace deterministic stratified slicing.

---

# Phase E — VAP Coverage Procedure

For VAP Registration Units, the extractor should preserve assertion registrations for:

```text
variant_observation
variant_normalization
variant_interpretation
variant_prioritization
validation
candidate_routing
```

If these assertion types are absent from a selected VAP Registration Unit, the absence must be reported.

The VAP source identity slice should attempt to include source identity coverage for:

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
```

The extractor must not intentionally restrict VAP source identity slices to:

```text
annotated variants only
prioritized variants only
clinically labeled variants only
coding variants only
```

When noncoding status is explicitly present in source fields, the extractor should include noncoding examples.

When noncoding status is not explicitly present, the extractor should preserve broad variant identity recoverability so downstream layers can classify or annotate noncoding status later.

The extractor must report whether noncoding detection was:

```text
explicitly_detected
not_detectable_from_source_identity_table
not_evaluated
```

The extractor must not infer noncoding biology beyond available source evidence.

---

# Phase F — GSC Coverage Procedure

For GSC Registration Units, the extractor should preserve assertion registrations for:

```text
phenotype_gene_semantic_prior
phenotype_gene_provenance
source_gene_relationship
aggregation_support
source_contribution_topology
producer_contract_validation
```

If these assertion types are absent from a selected GSC Registration Unit, the absence must be reported.

The GSC source identity slice should attempt to include source identity coverage for:

```text
phenotype identities
gene identities
source identities
semantic channel identities
evidence source identities
method identities
release identities
```

The extractor may preserve `source_contribution_topology` as a GSC producer-emitted assertion type.

The extractor must not treat `source_contribution_topology` as VDB-derived Evidence Topology.

The extractor must not collapse phenotype-scoped semantic priors into general gene truth claims.

---

# Phase G — Contract Alignment Checks

The MARK candidate package should include contract-alignment summaries.

Required checks:

```text
all six canonical Registration Units represented or omission explicit
assertion_registrations present
source_identities slice present or explicit unavailable state
source identity set candidates present
source identity summaries present
artifacts slice present
tep_packages slice present
schema_metadata slice present
VAP producer family represented
GSC producer family represented
VAP assertion registration types summarized
GSC assertion registration types summarized
source identity recoverability summarized
anti-flattening coverage summarized
non-annotated variant preservation status reported when detectable
noncoding variant preservation status reported when detectable
topology not derived
geometry not characterized
surfaces not constructed
projections not emitted
RDGP reasoning not performed
Registration Units opened read-only
Registration Units not mutated
```

Recommended summary artifacts:

```text
validation/contract_alignment_summary.tsv
validation/source_identity_recoverability_summary.tsv
validation/anti_flattening_coverage_summary.tsv
```

These summaries are reconnaissance/fixture-alignment outputs.

They are not Layer 2 validation execution receipts.

They are not Layer 3 full-corpus validation receipts.

They are not Phase 4.3 certification receipts.

---

# Phase H — Sys76 Curation

After MARK extraction, the operator should download:

```text
/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>.tgz
/root/Desktop/phase4_3_assertion_record_golden_fixture_<timestamp>.tgz.sha256
```

On sys76, the operator should:

```bash
sha256sum -c phase4_3_assertion_record_golden_fixture_<timestamp>.tgz.sha256
mkdir -p /tmp/phase4_3_assertion_record_golden_fixture_review
tar -xzf phase4_3_assertion_record_golden_fixture_<timestamp>.tgz \
  -C /tmp/phase4_3_assertion_record_golden_fixture_review
```

Then inspect:

```text
extraction_summary.tsv
validation/contract_alignment_summary.tsv
validation/source_identity_recoverability_summary.tsv
validation/anti_flattening_coverage_summary.tsv
fixture_limitations.md
```

The operator should reject or revise the candidate package if it violates the contract.

The operator should curate acceptable material into:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
```

sys76 is the git commit and push authority.

---

# Phase I — Committed Fixture Layout

The curated committed fixture should use this layout:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
    README.md
    fixture_manifest.json
    fixture_manifest.tsv
    fixture_limitations.md
    input/
        downstream_assertion_record_input_manifest.slice.tsv
        selected_registration_units.tsv
    registration_units/
        gsc_epilepsy/
        gsc_mitochondrial_disease/
        vap_hg002/
        vap_median_ERR10619300/
        vap_q1_ERR10619212/
        vap_q3_ERR10619225/
    expected/
        expected_output_placeholder_manifest.tsv
    validation/
        contract_alignment_summary.json
        contract_alignment_summary.tsv
        source_identity_recoverability_summary.tsv
        anti_flattening_coverage_summary.tsv
    checksums/
        file_manifest.sha256
```

Expected output snapshots may be added under `expected/` after the Assertion Record builder emits draft outputs and those outputs are reviewed.

Layer 2 script outputs generated during sys76 runs may be stored outside the fixture or under a governed review/output directory when useful.

Such artifacts must not be confused with Layer 3 MARK full-corpus receipts.

---

# Phase J — Expected Output Snapshot Procedure

A complete executable fixture should eventually include expected output snapshots:

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

Expected outputs should not be handwritten as final truth without review.

Recommended procedure:

```text
1. Run the Assertion Record builder against the curated source fixture.
2. Emit draft expected outputs to a temporary review directory.
3. Review output against the fixture contract, schema, resolver policy, and validation governance.
4. Patch builder or fixture if anti-flattening or preservation obligations fail.
5. Promote reviewed outputs into tests/fixtures/phase4/assertion_records/golden_fixture/expected/.
6. Commit expected outputs with a clear message.
```

Expected outputs must not contain:

```text
Evidence Topology
Convergence Geometry
Evidence Convergence Surfaces
Projection Views
RDGP reasoning
biological truth authority
clinical actionability authority
causality authority
```

---

# Phase K — Layer 2 Sys76 Script Integration Plan

Layer 2 validation should run on sys76 using explicit scripts against the committed compressed real-world fixture.

Layer 2 is not the synthetic pytest-only layer.

Layer 2 is not the MARK full-corpus layer.

Layer 2 tests should consume the committed fixture from:

```text
tests/fixtures/phase4/assertion_records/golden_fixture/
```

Layer 2 scripts should verify:

```text
fixture manifest is readable
contract identity is declared
fixture identity is declared
all required Registration Unit slices are present or omissions are explicit
assertion registration rows are loaded
source identity set candidates are loaded
source identity summaries are loaded
artifact and package slices are loaded
builder emits deterministic Assertion Record outputs
builder emits deterministic source identity set outputs
builder emits deterministic validation summary
builder preserves source identity recoverability
builder does not flatten to annotated/prioritized/coding-only evidence
builder does not derive topology
builder does not mutate fixture inputs
```

Layer 2 scripts should include negative or failure-mode checks when feasible.

At minimum, scripts should fail if source identity set outputs are missing when source identity slices are present.

Useful Layer 2 generated artifacts may be preserved when they support review, debugging, or provenance, but they remain Layer 2 sys76 artifacts and must not be labeled as MARK full-corpus receipts.

---

# Phase L — Commit Policy

The plan and contract should be committed before the MARK extraction script.

Recommended commit grouping:

```text
Commit 1:
    Add Phase 4.3 Assertion Record golden fixture contract and plan

Commit 2:
    Add MARK extraction script for Phase 4.3 Assertion Record golden fixture

Commit 3:
    Add curated Phase 4.3 Assertion Record golden fixture source slices

Commit 4:
    Add reviewed expected output snapshots after builder behavior stabilizes
```

Generated MARK candidate packages should not be committed directly without sys76 curation.

Large or inappropriate extracted files should be excluded before commit.

---

# Non-Goals

This plan does not define:

```text
Layer 1 synthetic pytest validation
Layer 3 MARK full-corpus validation
production Assertion Record Index construction
Phase 4.3 certification
Evidence Topology construction
Convergence Geometry construction
Evidence Convergence Surface construction
Projection View construction
RDGP reasoning
biological interpretation
clinical interpretation
causal interpretation
```

This plan does not authorize MARK to push to git.

---

# Acceptance Criteria

This plan is satisfied when:

```text
the governing contract exists
the plan exists under docs/plans/golden_fixtures/
the MARK extraction script is implemented under scripts/mark/
the extraction script consumes the governed downstream Assertion Record input manifest
the extraction script writes candidate packages to /root/Desktop/
the candidate package includes source slices and summaries required by contract
the candidate package includes source identity set candidates
the candidate package includes anti-flattening coverage summaries
the candidate package is packaged as TGZ with checksum
sys76 curation workflow is documented
the committed fixture target layout is documented
expected output snapshot procedure is documented
Layer 2 sys76 script integration expectations are documented
Layer 2 remains compressed and distinct from Layer 3
Layer 3 remains MARK-based, uncompressed, and separately receipt-tracked
MARK remains export-only and does not push
```

The plan is not satisfied merely because a fixture directory exists.

The plan is satisfied when the fixture workflow can produce a contract-compliant committed Layer 2 substrate.

---

# Summary

The Phase 4.3 Assertion Record golden fixture plan operationalizes the sister contract.

The guiding workflow is:

```text
Extract compressed production-derived slices on MARK.

Export candidate fixture package to /root/Desktop/.

Review and curate on sys76.

Commit only contract-compliant fixture material.

Run Layer 2 scripts on sys76 against the committed compressed fixture.

Reserve Layer 3 for uncompressed MARK full-corpus validation.

Retrieve Layer 3 artifacts to sys76 and commit strategically for provenance.

Use the fixture to fail compact-but-flattened Assertion Record implementations.
```

The plan exists to make the Layer 2 fixture practical without weakening the contract's preservation requirement.

The fixture must stay compact.

It must not become biologically impoverished.

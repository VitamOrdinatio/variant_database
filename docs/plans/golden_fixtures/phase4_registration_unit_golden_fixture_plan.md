# Phase 4 Registration Unit Golden Fixture Plan

## Purpose

This document defines the implementation plan for creating the Phase 4 Registration Unit golden fixture used by the Variant Database (VDB).

The Phase 4 golden fixture is a lightweight, retrievable, MARK-derived compression of the six certified Phase 3 VDB Registration Unit SQLite databases.

The fixture is created on MARK by read-only extraction and written only to `/root/Desktop/`.

After extraction, the user manually retrieves the artifact from MARK and places it into the sys76 VDB repository under:

```text
tests/fixtures/phase4/
```

The fixture supports rapid local Phase 4 development without requiring sys76 to store or operate on the full MARK SQLite corpus.

---

# Governing Contract

This plan is governed by:

```text
docs/contracts/golden_fixtures/phase4_registration_unit_golden_fixture_contract.md
```

The contract defines what must remain true.

This plan defines how to create, retrieve, place, inspect, and validate the fixture.

The governing invariant is:

```text
Real source rows, compressed volume, deterministic selection, traceable lineage,
read-only MARK execution, no authority inflation.
```

---

# Planning Verdict

```text
APPROVED FOR MARK-DERIVED PHASE 4 GOLDEN FIXTURE IMPLEMENTATION
```

The Phase 4 Registration Unit golden fixture should be created from the six certified Phase 3 VDB Registration Unit SQLite files on MARK.

The fixture must not be synthetic.

The fixture must not be generated from hand-authored local declarations.

The fixture must be derived from real source SQLite rows.

The fixture must preserve the certified Registration Unit inspection surface and selected real `source_identities` rows while compressing MARK-scale row volume.

---

# Fixture Development Doctrine

The fixture development doctrine is:

```text
compress real certified Phase 3 VDB registration outputs,
do not emulate them synthetically.
```

The fixture should preserve:

```text
six Registration Unit labels
directory structure
SQLite table surface
table columns
small structural tables
real assertion registration records
real artifact records
real package records
selected real source identity records
source identity categorical coverage
priority biological seed rows where present
null and non-null source_record_ref behavior where present
lineage from selected rows to source rows
auditability of source and output databases
```

The fixture may compress:

```text
source_identities row volume
full VAP biological breadth
full GSC biological breadth
MARK-scale storage mass
complete variant/gene/phenotype/sample breadth
```

The fixture must not synthesize:

```text
biological rows
source identity rows
assertion registration rows
source namespaces
participant roles
evidence domains
priority seed matches
```

---

# Validation Layer Role

The Phase 4 golden fixture serves as Validation Layer 2.

The intended Phase 4 validation ladder is:

```text
Validation Layer 1:
    local unit tests and deterministic logic tests

Validation Layer 2:
    compressed real-world Phase 4 golden fixture

Validation Layer 3:
    MARK smoketest against all six full certified Phase 3 Registration Unit
    SQLite databases
```

The fixture is intended to catch substrate mismatches that a synthetic fixture might miss.

Passing fixture tests does not certify Phase 4.

Passing fixture tests authorizes progression toward MARK full-corpus smoketesting.

---

# Source Corpus

The source corpus is located on MARK.

Expected MARK VDB repository root:

```text
/root/dev/portfolio_projects/variant_database
```

Expected source corpus root:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

Required source SQLite databases:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite

/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite

/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite

/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite

/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite

/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

All six source databases are required.

If any source database is absent, unreadable, or missing required registration-facing tables, the extraction script must fail or emit an explicit anomaly report.

---

# Prime Directive

The Prime Directive is active for all stages of fixture creation.

The MARK-side extraction script may read:

```text
/root/dev/portfolio_projects/variant_database/
```

The MARK-side extraction script may read VAP repository paths only if explicitly required for supplemental provenance inspection.

The MARK-side extraction script must write only to:

```text
/root/Desktop/
```

The script must not write into:

```text
/root/dev/portfolio_projects/variant_database/
/root/dev/portfolio_projects/variant_annotation_pipeline/
any producer repository
```

The script must not mutate source SQLite files.

The script must not create indexes, tables, triggers, views, WAL files, SHM files, checkpoints, migrations, sidecars, or generated fixture artifacts inside MARK repository directories.

---

# Canonical Script

The fixture extraction script should live at:

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

This name is intentionally aligned with the existing Phase 3 lightweight emulation pattern.

The script creates a lightweight Phase 4 development fixture from Phase 3 certified VDB registration outputs.

The script is MARK-specific.

The script may hardcode MARK absolute source paths.

The script must document all hardcoded source paths near the top of the file.

The script must fail loudly if the expected source corpus is absent.

The script must not search broadly for substitute SQLite files.

---

# Stage 0 — Prepare Repository State

## Objective

Prepare VDB repository state for the MARK-derived fixture workflow.

## Actions

Remove obsolete synthetic fixture materials if present:

```text
tests/fixtures/phase4/source/phase4_registration_unit_golden_fixture.yaml
scripts/dev/golden_fixtures/build_phase4_registration_unit_golden_fixture.py
```

Ensure the following governance files exist:

```text
docs/contracts/golden_fixtures/phase4_registration_unit_golden_fixture_contract.md
docs/plans/golden_fixtures/phase4_registration_unit_golden_fixture_plan.md
```

Create or confirm the MARK script location:

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

## Stage 0 Exit Criteria

Stage 0 is complete when the synthetic local-builder path has been removed and the MARK-derived contract/plan pair governs the fixture workflow.

---

# Stage 1 — Implement MARK Source Declaration In Script

## Objective

Hardcode the certified MARK source corpus in the MARK extraction script.

## Required Constants

The script should declare:

```text
SOURCE_VDB_REPO_ROOT
SOURCE_CORPUS_ROOT
OUTPUT_PARENT
OUTPUT_ROOT
ARCHIVE_PATH
REGISTRATION_UNITS
FULL_COPY_TABLES
COMPRESSED_TABLE
PRIORITY_SEEDS
```

Recommended source root:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

Recommended output parent:

```text
/root/Desktop/
```

Recommended output directory pattern:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>/
```

Recommended archive pattern:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>.tgz
```

Required Registration Unit map:

```text
gsc_epilepsy:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite

gsc_mitochondrial_disease:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite

vap_hg002:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite

vap_median_ERR10619300:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite

vap_q1_ERR10619212:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite

vap_q3_ERR10619225:
    /root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite
```

## Stage 1 Exit Criteria

Stage 1 is complete when the script contains the explicit six-database source declaration and refuses to proceed if the declared source corpus is incomplete.

---

# Stage 2 — Open Source SQLite Files Read-Only

## Objective

Open source SQLite files without mutating MARK-resident databases.

## Required Access Pattern

The script should open source databases using a read-only SQLite URI where practical:

```text
file:<source_path>?mode=ro&immutable=1
```

The script should set query-only behavior where practical:

```text
PRAGMA query_only=ON;
```

The script should avoid operations that can create source-side sidecars.

## Required Audits

Before extraction, the script should record source state:

```text
source_database_path
source_database_exists
source_database_size_bytes
source_database_mtime_ns
source_database_sha256_or_skip_reason
open_status
required_table_status
row counts for required tables
source_identities categorical summaries
null source_record_ref count
non-null source_record_ref count
```

After extraction, the script should record source state again where practical:

```text
source_database_size_bytes_after
source_database_mtime_ns_after
post_extraction_state_status
```

## Stage 2 Exit Criteria

Stage 2 is complete when all six source databases open read-only, required tables are visible, and pre-extraction audit data is captured.

---

# Stage 3 — Create Portable Output Directory

## Objective

Create a complete portable output fixture directory under `/root/Desktop/`.

## Output Root

Recommended output path:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>/
```

## Archive Internal Root

The output directory should contain this portable internal structure:

```text
phase4_registration_unit_golden_fixture/
├── registration_units/
│   └── mark_phase3_canonical_6sqlite_lightweight/
├── manifests/
├── reports/
├── lineage/
└── expected/
```

## Required Output Registration Unit Shape

The script should create:

```text
phase4_registration_unit_golden_fixture/
└── registration_units/
    └── mark_phase3_canonical_6sqlite_lightweight/
        ├── gsc_epilepsy/
        │   └── vdb.sqlite
        ├── gsc_mitochondrial_disease/
        │   └── vdb.sqlite
        ├── vap_hg002/
        │   └── vdb.sqlite
        ├── vap_median_ERR10619300/
        │   └── vdb.sqlite
        ├── vap_q1_ERR10619212/
        │   └── vdb.sqlite
        └── vap_q3_ERR10619225/
            └── vdb.sqlite
```

## Stage 3 Exit Criteria

Stage 3 is complete when the output directory exists under `/root/Desktop/` and contains the expected portable folder structure.

---

# Stage 4 — Recreate SQLite Table Surface In Compressed Outputs

## Objective

Create compressed output SQLite files that preserve the registration-facing SQLite table surface.

## Required Tables

Each compressed output `vdb.sqlite` must include:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
source_identities
```

## Schema Strategy

The script should inspect each source table schema using SQLite metadata.

Recommended approach:

```text
PRAGMA table_info(<table>);
```

The script should recreate output tables using source-compatible column names and types.

The script may preserve primary key declarations if practical.

The script may omit indexes unless necessary for local fixture use.

The script should not add fixture-only biological rows.

The script should avoid adding fixture-only metadata rows inside copied tables unless explicitly documented.

## Stage 4 Exit Criteria

Stage 4 is complete when each compressed output SQLite database contains the expected table surface and compatible columns.

---

# Stage 5 — Copy Full-Copy Tables

## Objective

Copy structurally central small tables completely.

## Full-Copy Tables

The following tables should be copied completely from source to compressed output:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
```

## Copy Requirements

The script must preserve:

```text
row values
row counts
column names
primary identifiers
package identifiers
artifact identifiers
assertion registration identifiers
producer-family values
surface-role values
evidence-domain values
assertion-type values
authority-context values
uncertainty-context values
registration-status values
```

## Lineage

The script must emit copied-table lineage to:

```text
phase4_registration_unit_golden_fixture/lineage/copied_table_lineage.tsv
```

Recommended fields:

```text
registration_unit_label
source_database_path
source_table
output_database_relative_path
output_table
source_row_count
output_row_count
copy_mode
copy_status
```

## Stage 5 Exit Criteria

Stage 5 is complete when all full-copy tables have matching source/output row counts, or documented anomalies cause the script to fail.

---

# Stage 6 — Select Real `source_identities` Rows Deterministically

## Objective

Compress the large `source_identities` table by selecting deterministic real rows from each source database.

## Compression Target

```text
source_identities
```

## Selection Requirements

For each Registration Unit, the script should attempt to select rows covering:

```text
each assertion_registration_id where available
each observed identity_kind
each observed source_namespace
each observed participant_role
each observed extraction_method
null source_record_ref examples where available
non-null source_record_ref examples where available
priority biological seed rows where present
fallback early rows for baseline context
```

## Deterministic Strategy

Use stable ordering such as:

```text
ORDER BY rowid
```

or:

```text
ORDER BY source_identity_id
```

Selection must not use randomness.

Selection must not depend on nondeterministic database traversal.

Selection must not synthesize missing categories.

Selection must not invent biological rows.

## Suggested Per-Unit Limits

Initial limits should keep the fixture lightweight while preserving coverage.

Recommended initial targets:

```text
MAX_ROWS_PER_ASSERTION_REGISTRATION = 10
MAX_ROWS_PER_IDENTITY_KIND = 20
MAX_ROWS_PER_SOURCE_NAMESPACE = 20
MAX_ROWS_PER_PARTICIPANT_ROLE = 20
MAX_ROWS_PER_EXTRACTION_METHOD = 20
MAX_NULL_SOURCE_RECORD_REF_ROWS = 20
MAX_NON_NULL_SOURCE_RECORD_REF_ROWS = 20
MAX_PRIORITY_SEED_ROWS = 100
MAX_FALLBACK_ROWS = 100
```

The script should deduplicate selected rows by source row identity.

If these values produce an unexpectedly large fixture, revise limits downward.

If they fail to preserve critical categories, revise limits upward.

## Stage 6 Exit Criteria

Stage 6 is complete when each output `source_identities` table contains a deterministic, deduplicated, real-row subset with selection lineage.

---

# Stage 7 — Apply Biological Priority Seed Capture

## Objective

Capture real source identity rows involving priority biological seeds useful for downstream Phase 4 development.

## Priority Genes

Recommended priority gene symbols:

```text
POLG
TWNK
SCN1A
DEPDC5
```

## Priority Ensembl Gene Identifiers

Recommended priority identifiers:

```text
ENSG00000140521
ENSG00000107815
ENSG00000144285
ENSG00000100150
```

## Priority Variant Fragments

The script may include known VAP-relevant variant fragments where available.

Recommended initial fragments:

```text
15:89333596:T:TTGC
89333596
```

## Matching Scope

Priority matching should search real source identity values and labels.

Recommended fields:

```text
source_value
source_label
payload_json
source_record_ref
```

## No-Synthesis Rule

If priority seed rows are absent, the script records absence.

The script must not create synthetic priority rows.

The script must not edit source values to create matches.

## Stage 7 Exit Criteria

Stage 7 is complete when priority seed capture has either selected real matching rows or recorded that no matching rows were found for a given unit/seed.

---

# Stage 8 — Emit Lineage Artifacts

## Objective

Provide row-level traceability from compressed fixture rows back to source rows.

## Required Lineage Files

```text
phase4_registration_unit_golden_fixture/lineage/selected_source_identity_lineage.tsv
phase4_registration_unit_golden_fixture/lineage/copied_table_lineage.tsv
```

## Selected Source Identity Lineage Fields

Recommended fields:

```text
registration_unit_label
source_database_path
source_database_size_bytes
source_table
source_rowid
source_primary_key
output_database_relative_path
output_table
output_primary_key
selection_reason
selection_rank
identity_kind
source_namespace
participant_role
extraction_method
source_record_ref_state
```

## Selection Reasons

Allowed selection reason values should include:

```text
assertion_registration_coverage
identity_kind_coverage
source_namespace_coverage
participant_role_coverage
extraction_method_coverage
null_source_record_ref_coverage
non_null_source_record_ref_coverage
priority_seed_match
fallback_context
```

If a row is selected for multiple reasons, the script may either:

```text
emit one lineage row per reason
```

or:

```text
emit one lineage row with semicolon-delimited selection reasons
```

The chosen policy should be documented in the report.

## Stage 8 Exit Criteria

Stage 8 is complete when selected source identity rows and full-copy tables are traceable through lineage artifacts.

---

# Stage 9 — Emit Audits, Manifests, Reports, And Expected Outputs

## Objective

Emit reviewable metadata describing the source corpus, compression policy, output fixture, and known limitations.

## Required Artifacts

```text
phase4_registration_unit_golden_fixture/manifests/phase4_registration_unit_golden_fixture_manifest.json
phase4_registration_unit_golden_fixture/reports/phase4_registration_unit_golden_fixture_report.md
phase4_registration_unit_golden_fixture/reports/source_database_audit.tsv
phase4_registration_unit_golden_fixture/reports/fixture_database_audit.tsv
phase4_registration_unit_golden_fixture/reports/fixture_checksums.tsv
```

## Optional Expected Outputs

The script may also emit initial expected-output skeletons under:

```text
phase4_registration_unit_golden_fixture/expected/
```

Recommended expected outputs:

```text
registration_unit_table_counts_expected.tsv
registration_unit_category_summary_expected.tsv
registration_unit_fixture_inventory_expected.tsv
```

These may be preliminary.

Final Phase 4.1 expected outputs may be regenerated later by the canonical Phase 4.1 inspector.

## Manifest Requirements

The manifest JSON should include:

```text
fixture_id
fixture_version
created_at_utc
script_path
source_vdb_repo_root
output_root
archive_path
prime_directive
source_registration_units
source_database_paths
source_database_sizes
output_registration_units
output_database_paths
output_database_sizes
output_database_sha256
full_copy_tables
compressed_tables
source_identity_selection_policy
priority_seed_policy
lineage_artifact_paths
authority_statement
```

## Report Requirements

The report Markdown should include:

```text
purpose
source corpus
Prime Directive
extraction policy
compression policy
per-unit row counts
per-unit selected source identity counts
priority seed capture summary
null/non-null source_record_ref summary
lineage artifact summary
output archive path
sys76 placement recommendation
authority boundary
known limitations
```

## Stage 9 Exit Criteria

Stage 9 is complete when the output fixture includes machine-readable and human-readable metadata sufficient to review how the fixture was created.

---

# Stage 10 — Create Retrievable Archive

## Objective

Package the output fixture into a portable archive on MARK.

## Archive Path

Recommended archive path:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>.tgz
```

## Archive Requirements

The archive must contain the portable internal root:

```text
phase4_registration_unit_golden_fixture/
```

The archive must include:

```text
registration_units/
manifests/
reports/
lineage/
expected/
```

The script should print the archive path at completion.

The script should print the output directory path at completion.

## Stage 10 Exit Criteria

Stage 10 is complete when the `.tgz` exists on `/root/Desktop/` and contains the complete portable fixture root.

---

# Stage 11 — Manual Retrieval To sys76

## Objective

Move the fixture artifact from MARK to sys76 under operator control.

## Manual Transfer

The user manually downloads the archive from MARK’s `/root/Desktop/`.

The script must not automate transfer.

The script must not write to sys76.

## sys76 Destination

Recommended destination after extraction:

```text
~/dev/portfolio_projects/variant_database/tests/fixtures/phase4/
```

Expected resulting local path:

```text
~/dev/portfolio_projects/variant_database/tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

## Stage 11 Exit Criteria

Stage 11 is complete when the fixture has been manually placed into the sys76 VDB repository under `tests/fixtures/phase4/`.

---

# Stage 12 — Validate Local Fixture On sys76

## Objective

Confirm that the retrieved fixture is usable for local Phase 4 development.

## Recommended Local Checks

From sys76 VDB repo root:

```bash
find tests/fixtures/phase4 -type f | sort
du -sh tests/fixtures/phase4
```

For SQLite surface checks:

```bash
sqlite3 tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_hg002/vdb.sqlite ".tables"
```

Expected table surface:

```text
artifacts
assertion_registrations
schema_metadata
source_identities
tep_packages
```

## Recommended Fixture Validation Test

A later fixture validation test should live at:

```text
tests/phase4/test_phase4_registration_unit_golden_fixture.py
```

This test should verify:

```text
six Registration Unit directories exist
each Registration Unit contains vdb.sqlite
each SQLite opens read-only
required tables exist
required columns exist
full-copy tables have expected row counts
source_identities has selected real rows
lineage artifacts exist
manifest artifacts exist
audit artifacts exist
checksums exist
fixture size is reasonable
```

## Stage 12 Exit Criteria

Stage 12 is complete when the fixture can be inspected locally and passes initial fixture validation checks.

---

# Stage 13 — Use Fixture For Phase 4.1 Development

## Objective

Use the golden fixture as the primary local substrate for Phase 4.1 Registration Unit inspection.

## Phase 4.1 Development Uses

The fixture should support:

```text
Registration Unit input declaration
Registration Unit path resolution
read-only SQLite opening
required table inspection
required column inspection
package inspection
artifact inspection
assertion registration inspection
source identity inspection
producer-family extraction
surface-role extraction
evidence-domain extraction
identity-kind extraction
namespace extraction
inventory emission
readiness emission
non-mutation checks
deterministic expected-output comparison
```

## Runtime Code Path Requirement

The Phase 4.1 inspector must not contain fixture-only logic.

The same inspector should run against:

```text
tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

and later against:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

Only the input root, manifest, execution profile, and output directory should differ.

## Stage 13 Exit Criteria

Stage 13 is complete when Phase 4.1 development can proceed locally against the compressed real-row fixture.

---

# Stage 14 — Preserve MARK Smoketest Separation

## Objective

Maintain the distinction between fixture validation and full MARK validation.

## Fixture Role

The lightweight fixture is Validation Layer 2.

It supports fast local development and real-row substrate testing.

## MARK Full-Corpus Role

The full MARK source corpus remains Validation Layer 3.

It supports real-scale smoketesting and certification readiness.

## Required Separation

The fixture must not replace MARK full-corpus testing.

The MARK smoketest should later run against the full source corpus:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

The MARK smoketest should write outputs only to an approved MARK output location, not source Registration Unit directories.

## Stage 14 Exit Criteria

Stage 14 is complete when the fixture and full-corpus validation roles are explicitly preserved in implementation and documentation.

---

# Git Tracking Policy

The following should be git-tracked immediately:

```text
docs/contracts/golden_fixtures/phase4_registration_unit_golden_fixture_contract.md
docs/plans/golden_fixtures/phase4_registration_unit_golden_fixture_plan.md
scripts/mark/create_phase3_lightweight_emulation.py
```

After manual retrieval to sys76, the following should be considered for git tracking if the fixture remains reasonably small:

```text
tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
tests/fixtures/phase4/manifests/
tests/fixtures/phase4/reports/
tests/fixtures/phase4/lineage/
tests/fixtures/phase4/expected/
```

If the compressed fixture is too large for routine git tracking, the repository should still track:

```text
manifest
report
lineage summaries
checksum summaries
restoration instructions
```

The preferred outcome is a compressed fixture small enough to commit.

---

# Size Policy

The fixture should remain lightweight enough for rapid local development.

Initial target:

```text
full extracted fixture under 100 MB
```

Preferred target:

```text
full extracted fixture under 25 MB if practical
```

If the fixture exceeds the initial target, inspect:

```text
source_identities selected row volume
payload_json size
priority seed row counts
fallback row counts
SQLite page overhead
unneeded indexes
duplicate selected rows
```

The fixture should preserve real-row coverage, not MARK-scale row volume.

---

# Non-Mutation Policy

The extraction script must not mutate source databases.

The extraction script must not write into MARK repository paths.

The Phase 4 local inspector must not mutate fixture SQLite files.

Forbidden mutation behaviors include:

```text
CREATE TABLE against source databases
CREATE INDEX against source databases
CREATE VIEW against source databases
CREATE TRIGGER against source databases
INSERT into source databases
UPDATE source databases
DELETE from source databases
DROP source database objects
ALTER source database objects
VACUUM source databases
REINDEX source databases
ANALYZE source databases
PRAGMA wal_checkpoint against source databases
PRAGMA optimize against source databases
```

The script may create new compressed SQLite files under `/root/Desktop/`.

The script may write manifests, reports, lineage, audits, checksums, and archives under `/root/Desktop/`.

---

# Failure Policy

The extraction script should fail loudly if:

```text
a required source SQLite file is missing
a required source SQLite file cannot be opened read-only
a required table is missing
a full-copy table cannot be copied completely
a compressed output SQLite cannot be created
source_identities cannot be queried
lineage artifacts cannot be written
source or fixture audits cannot be emitted
the output archive cannot be created
```

The script may complete with warnings if:

```text
a priority seed is absent from a given source database
a null source_record_ref example is absent from a given source database
a non-null source_record_ref example is absent from a given source database
a category has fewer rows than the requested selection limit
```

Warnings must be recorded in the report.

---

# Acceptance Gates

The fixture workflow is acceptable when all gates pass.

## Gate 1 — Contract Present

```text
docs/contracts/golden_fixtures/phase4_registration_unit_golden_fixture_contract.md
```

## Gate 2 — Plan Present

```text
docs/plans/golden_fixtures/phase4_registration_unit_golden_fixture_plan.md
```

## Gate 3 — MARK Extraction Script Present

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

## Gate 4 — MARK Script Runs

The script runs on MARK and writes only to `/root/Desktop/`.

## Gate 5 — Six Source Databases Read

The script reads all six declared source SQLite files.

## Gate 6 — Six Output Databases Created

The archive contains six compressed Registration Unit SQLite files.

## Gate 7 — Full-Copy Tables Preserved

For each unit, these tables are copied completely:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
```

## Gate 8 — Source Identities Compressed

For each unit, `source_identities` is compressed by deterministic real-row selection.

## Gate 9 — No Synthetic Rows

No synthetic biological rows or source identity rows are created.

## Gate 10 — Lineage Emitted

Selected source identities and copied tables are traceable through lineage artifacts.

## Gate 11 — Audits Emitted

Source and fixture database audits are emitted.

## Gate 12 — Manifest And Report Emitted

Machine-readable and human-readable summaries are emitted.

## Gate 13 — Archive Created

A `.tgz` archive is created on `/root/Desktop/`.

## Gate 14 — Manual sys76 Placement

The user manually places the fixture under:

```text
tests/fixtures/phase4/
```

## Gate 15 — Local Fixture Inspectable

The retrieved fixture can be inspected locally on sys76.

---

# Deferred Work

The following work is deferred:

```text
Phase 4.1 fixture validation test implementation
Phase 4.1 Registration Unit inspector implementation
Phase 4.2 Corpus Generation test expansion
Phase 4.3 Assertion Record indexing validation
negative fixture family
stress fixture family
topology-specific fixture extension
geometry-specific fixture extension
surface-specific fixture extension
projection-specific fixture extension
MARK full-corpus Phase 4 smoketest
```

Deferred work must preserve the authority boundary between:

```text
lightweight fixture development
```

and:

```text
MARK full-corpus certification testing
```

---

# Recommended Implementation Sequence

Recommended execution order:

```text
1. Commit the de novo MARK-derived golden fixture contract.

2. Commit this MARK-derived golden fixture plan.

3. Implement scripts/mark/create_phase3_lightweight_emulation.py.

4. Run the script on MARK.

5. Retrieve the generated .tgz from /root/Desktop/.

6. Extract the archive on sys76.

7. Place the fixture under tests/fixtures/phase4/.

8. Inspect the local fixture manually.

9. Add fixture validation tests.

10. Begin Phase 4.1 Registration Unit inspector development against the
    compressed real-row fixture.

11. Later run the same inspector against the full six-database MARK source corpus.
```

---

# Summary

This plan implements the Phase 4 Registration Unit golden fixture as a MARK-derived compressed real-row fixture.

The fixture is created from the six certified Phase 3 VDB Registration Unit SQLite databases.

The extraction script runs on MARK.

The script reads source databases read-only.

The script writes only to `/root/Desktop/`.

The fixture is manually retrieved to sys76.

The fixture is placed under `tests/fixtures/phase4/`.

The fixture becomes Validation Layer 2 for Phase 4 development.

The full MARK corpus remains Validation Layer 3.

The plan’s operating rule is:

```text
Build one primary golden fixture from compressed real certified data,
then use it for as much Phase 4 development as it can honestly support.
```

# Phase 4 Registration Unit Golden Fixture Contract

## Purpose

This document defines the contract for the Phase 4 Registration Unit golden fixture used by the Variant Database (VDB).

The Phase 4 golden fixture is a lightweight, retrievable, MARK-derived compression of the six certified Phase 3 VDB Registration Unit SQLite databases.

The fixture is created by read-only extraction on MARK and is used for rapid Phase 4 development on sys76.

The fixture exists to provide a real-row-derived development substrate for Phase 4.1 Registration Unit inspection, Phase 4.2 Corpus Generation development, and as much downstream Phase 4 development as its compressed biological and structural contents can support.

The fixture is not synthetic.

The fixture is not a hand-authored emulator.

The fixture is not a biological benchmark.

The fixture is not a certification substitute.

The fixture is not release certification evidence.

The fixture is a compressed real-world development fixture derived from certified Phase 3 VDB registration outputs.

---

# Core Invariant

The governing invariant for the Phase 4 Registration Unit golden fixture is:

```text
Real source rows, compressed volume, deterministic selection, traceable lineage,
read-only MARK execution, no authority inflation.
```

Expanded:

```text
The Phase 4 Registration Unit golden fixture must preserve the certified
Registration Unit inspection surface and selected real source rows from the
MARK Phase 3 certified corpus, while intentionally compressing MARK-scale row
volume into a lightweight fixture that can be retrieved to sys76 for rapid
Phase 4 development.
```

---

# Contract Status

```text
CONTRACTUAL FOR PHASE 4 LIGHTWEIGHT GOLDEN FIXTURE CREATION
```

This contract governs the creation of the Phase 4 Registration Unit golden fixture from MARK-resident Phase 3 certified VDB Registration Unit SQLite files.

This contract governs:

```text
MARK-side source access
MARK-side extraction boundaries
real-row compression policy
lineage and traceability requirements
output archive requirements
sys76 placement expectations
authority boundaries
acceptance criteria
```

This contract does not govern canonical VDB runtime portability.

This contract does not authorize mutation of MARK-resident repositories.

This contract does not authorize generation of synthetic biological fixture rows.

---

# Source Corpus

The source corpus consists of six MARK-resident VDB Registration Unit SQLite databases produced by Phase 3 registration certification.

Expected MARK VDB repository root:

```text
/root/dev/portfolio_projects/variant_database
```

Expected source corpus root:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

Required source Registration Units:

```text
results/registration/mark_phase3_canonical/
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

The fixture must derive from all six source SQLite files.

A fixture derived from only one Registration Unit is not sufficient for Phase 4.

A fixture derived from only VAP Registration Units is not sufficient for Phase 4.

A fixture derived from only GSC Registration Units is not sufficient for Phase 4.

---

# Prime Directive

The Prime Directive is always active.

The extraction script may read MARK-resident VDB repository paths.

The extraction script may read MARK-resident VAP repository paths only if a later declared extraction requirement requires supplemental provenance inspection.

The extraction script must write only to:

```text
/root/Desktop/
```

The extraction script must not write to:

```text
/root/dev/portfolio_projects/variant_database/
```

The extraction script must not write to:

```text
/root/dev/portfolio_projects/variant_annotation_pipeline/
```

The extraction script must not write to any producer repository.

The extraction script must not alter MARK repository structures.

The extraction script must not create fixture outputs inside the MARK VDB repository.

The extraction script must not mutate source SQLite files.

The extraction script must not create indexes, tables, triggers, views, checkpoints, WAL files, SHM files, migrations, or sidecar state in source repository directories.

The user manually retrieves the completed artifact from `/root/Desktop/` and places it into the sys76 VDB repository.

---

# MARK-Only Execution Boundary

The fixture extraction script is intended to run on MARK.

Canonical script path:

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

The script may hardcode MARK absolute paths because it is a controlled MARK extraction utility.

Hardcoded MARK paths in this script are allowed for provenance, operator clarity, and controlled artifact generation.

Hardcoded MARK paths in this script must not be interpreted as a design pattern for canonical VDB implementation code.

Canonical VDB implementation code must remain portable, configurable, and path-abstracted.

The distinction is:

```text
MARK extraction utility:
    may hardcode MARK absolute source paths
    may write only to /root/Desktop/
    exists to create a lightweight fixture artifact

canonical VDB runtime code:
    must not hardcode MARK-specific paths
    must operate through declared inputs and configurable paths
    exists to implement portable VDB functionality
```

---

# Relationship To Phase 3 Certification

The fixture is downstream of Phase 3 certification.

The source SQLite files are certified Phase 3 VDB Registration Unit outputs.

The fixture does not create new certification.

The fixture does not replace the certified source corpus.

The fixture does not modify the certified source corpus.

The correct relationship is:

```text
Phase 3 certified MARK VDB Registration Units
        ↓
read-only MARK compression script
        ↓
lightweight real-row-derived fixture archive on /root/Desktop/
        ↓
manual retrieval to sys76
        ↓
Phase 4 local development fixture
        ↓
later MARK full-corpus smoketest
```

The fixture inherits its structural relevance from the certified Phase 3 source corpus.

The fixture does not inherit certification authority.

---

# Relationship To Phase 4 Development

The fixture supports Phase 4 development by providing a compressed but real-row-derived substrate.

Expected uses include:

```text
Phase 4.1 Registration Unit inspection
Phase 4.1 inventory emission
Phase 4.1 readiness validation
Phase 4.2 Corpus Generation development
Phase 4.2 corpus manifest development
early Phase 4.3 Assertion Record indexing development
early evidence-domain and identity-kind grouping checks
early namespace-aware grouping checks
early convergence seed inspection where real selected rows support it
```

The fixture should support as much downstream Phase 4 development as possible.

If later Phase 4 layers require additional real-row patterns, the fixture may be extended by rerunning or revising the MARK-side compression script.

Additional fixtures may be created later for negative cases, stress cases, topology-specific cases, geometry-specific cases, or projection-specific cases.

Those future fixtures must not redefine this primary golden fixture unless this contract is revised.

---

# Validation Layer Role

The Phase 4 golden fixture serves as Validation Layer 2.

The intended validation ladder is:

```text
Validation Layer 1:
    unit tests and small deterministic logic tests

Validation Layer 2:
    compressed real-world lightweight Phase 4 golden fixture

Validation Layer 3:
    MARK smoketest against all six full certified Phase 3 Registration Unit SQLite files
```

The Phase 4 golden fixture must be strong enough to detect real substrate mismatches that a synthetic fixture could miss.

The fixture does not eliminate the need for MARK full-corpus smoketesting.

The fixture improves local development fidelity before MARK full-corpus execution.

---

# Fixture Output And Transfer Model

The MARK-side extraction script must write a complete output directory to `/root/Desktop/`.

Recommended output directory pattern:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>/
```

Recommended archive pattern:

```text
/root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>.tgz
```

The output directory should contain a portable fixture root suitable for placement into the sys76 VDB repository.

Recommended archive internal structure:

```text
phase4_registration_unit_golden_fixture/
├── registration_units/
│   └── mark_phase3_canonical_6sqlite_lightweight/
│       ├── gsc_epilepsy/
│       │   └── vdb.sqlite
│       ├── gsc_mitochondrial_disease/
│       │   └── vdb.sqlite
│       ├── vap_hg002/
│       │   └── vdb.sqlite
│       ├── vap_median_ERR10619300/
│       │   └── vdb.sqlite
│       ├── vap_q1_ERR10619212/
│       │   └── vdb.sqlite
│       └── vap_q3_ERR10619225/
│           └── vdb.sqlite
├── manifests/
├── reports/
├── lineage/
└── expected/
```

Expected sys76 placement after manual retrieval:

```text
tests/fixtures/phase4/
```

The MARK script must not perform this sys76 placement.

The user performs transfer and placement manually.

---

# Required Source Registration Units

The fixture must include lightweight compressed outputs for all six source Registration Units.

Required GSC units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
```

Required VAP units:

```text
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

Each output Registration Unit must preserve the source Registration Unit label.

Each output Registration Unit must contain one SQLite file named:

```text
vdb.sqlite
```

Each output Registration Unit must preserve enough structure that Phase 4 code can switch between the lightweight fixture and the full MARK source corpus by changing only the input root, manifest, or execution profile.

---

# Required SQLite Surface

Each compressed output `vdb.sqlite` must preserve the same registration-facing table surface as the source SQLite file.

Expected required tables:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
source_identities
```

The extraction script must inspect the source SQLite surface before extraction.

If an expected table is absent from a source database, the script must record this as a failure or explicit anomaly in the report.

The script must not silently synthesize missing tables.

The script must not silently invent replacement rows.

---

# Full-Copy Tables

The following tables should be copied completely from each source SQLite database into the compressed fixture SQLite database:

```text
schema_metadata
tep_packages
artifacts
assertion_registrations
```

These tables are expected to be small and structurally central.

The extraction script must preserve:

```text
table names
column names
row values
row counts
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

If any full-copy table is unexpectedly too large or impractical to copy, the script must fail or emit an explicit anomaly report.

It must not silently downsample these tables without a contract revision.

---

# Deterministic Compression Table

The `source_identities` table is the primary compression target.

The full MARK corpus may contain very large `source_identities` row volume.

The compressed fixture must select a deterministic subset of real `source_identities` rows from each source database.

The extractor must not synthesize `source_identities` rows.

The extractor must not fabricate biological identifiers.

The extractor must not fabricate source namespaces.

The extractor must not fabricate participant roles.

The extractor must not fabricate source record references.

Selected `source_identities` rows must be copied from source databases.

---

# Source Identity Selection Policy

The `source_identities` selection policy must preserve real-row coverage across important structural categories.

At minimum, for each source Registration Unit, the selection policy should attempt to include:

```text
rows linked to each assertion_registration_id where available
rows representing each observed identity_kind
rows representing each observed source_namespace
rows representing each observed participant_role
rows representing each observed extraction_method
rows with null source_record_ref where available
rows with non-null source_record_ref where available
priority biological seed rows where present
fallback early rows for baseline context
```

The selection policy must be deterministic.

Deterministic strategies may include:

```text
ORDER BY rowid
ORDER BY source_identity_id
stable grouped selection by categorical field
stable priority matching followed by stable fallback selection
```

The selection policy must not depend on random sampling.

The selection policy must not depend on wall-clock time except for naming output directories or reports.

The selection policy must record why each selected row was selected.

---

# Biological Priority Seed Policy

The extraction script should attempt to preserve real rows involving a small set of biological priority seeds useful for downstream Phase 4 development.

Recommended priority genes:

```text
POLG
TWNK
SCN1A
DEPDC5
```

Recommended Ensembl gene identifiers:

```text
ENSG00000140521
ENSG00000107815
ENSG00000144285
ENSG00000100150
```

Recommended variant fragments may include known VAP fixture-relevant fragments where present.

The priority seed policy must be real-row-only.

If a priority gene, identifier, or variant fragment is absent from a source database, the extractor must record the absence.

The extractor must not create synthetic priority rows.

The extractor must not edit real rows to make them match priority seeds.

Priority rows support development structure.

Priority rows do not create biological conclusions.

---

# No-Synthesis Rule

The Phase 4 golden fixture must be real-row-derived.

The extractor must not synthesize biological rows.

The extractor must not synthesize source identity rows.

The extractor must not synthesize assertion registrations.

The extractor must not synthesize source namespaces.

The extractor must not synthesize participant roles.

The extractor must not synthesize evidence-domain rows.

The extractor may create metadata files describing the extraction process.

The extractor may create reports, manifests, checksums, and lineage files.

The extractor may create new compressed SQLite files under `/root/Desktop/`.

The content copied into compressed SQLite tables must be derived from source SQLite rows, except for explicitly documented fixture-level metadata stored outside the copied SQLite databases.

If the extractor adds fixture metadata to the output SQLite files, this must be documented and must not alter or obscure copied source rows.

The preferred approach is to keep copied SQLite database contents limited to source-derived rows and place fixture metadata in external manifests.

---

# Lineage And Traceability Requirements

The fixture must include traceability from compressed output rows back to source databases.

Required lineage artifacts include:

```text
lineage/selected_source_identity_lineage.tsv
lineage/copied_table_lineage.tsv
```

`selected_source_identity_lineage.tsv` should include one row per selected `source_identities` row.

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

`copied_table_lineage.tsv` should include one row per full-copy table per Registration Unit.

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

The fixture must include enough lineage to let reviewers distinguish:

```text
rows copied completely
rows selected by category preservation
rows selected by priority seed matching
rows selected as fallback context
rows selected for null/non-null edge coverage
```

---

# Output Manifest Requirements

The fixture archive must include machine-readable and human-readable manifests.

Required manifest/report artifacts:

```text
manifests/phase4_registration_unit_golden_fixture_manifest.json
reports/phase4_registration_unit_golden_fixture_report.md
reports/source_database_audit.tsv
reports/fixture_database_audit.tsv
reports/fixture_checksums.tsv
```

The manifest JSON should include:

```text
fixture_id
fixture_version
created_at_utc
script_path
script_version_or_sha_context_if_available
source_vdb_repo_root
output_root
archive_path
prime_directive
source_registration_units
source_database_paths
source_database_sizes
source_database_sha256_or_declared_skip_reason
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

The human-readable report should include:

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

---

# Source Database Audit Requirements

The extraction script must emit a source database audit.

The source audit should include, for each source SQLite database:

```text
registration_unit_label
source_database_path
source_database_exists
source_database_size_bytes
open_status
query_only_status
table_count
required_table_status
schema_metadata_row_count
tep_packages_row_count
artifacts_row_count
assertion_registrations_row_count
source_identities_row_count
source_identity_identity_kind_count
source_identity_namespace_count
source_identity_participant_role_count
source_identity_extraction_method_count
null_source_record_ref_count
non_null_source_record_ref_count
audit_status
```

The source audit helps confirm that the compressed fixture was derived from the intended MARK source corpus.

---

# Fixture Database Audit Requirements

The extraction script must emit a fixture database audit.

The fixture audit should include, for each compressed output SQLite database:

```text
registration_unit_label
output_database_relative_path
output_database_exists
output_database_size_bytes
open_status
required_table_status
schema_metadata_row_count
tep_packages_row_count
artifacts_row_count
assertion_registrations_row_count
source_identities_row_count
foreign_key_check_status_if_applicable
integrity_check_status
audit_status
```

The fixture audit helps confirm that the compressed SQLite files are readable and internally coherent.

---

# Non-Mutation Requirements

Source SQLite files must be opened read-only.

Preferred SQLite access mode:

```text
file:<source_path>?mode=ro&immutable=1
```

The script should set query-only behavior where practical:

```text
PRAGMA query_only=ON;
```

The script must not execute write statements against source databases.

Forbidden source operations include:

```text
CREATE TABLE
CREATE INDEX
CREATE VIEW
CREATE TRIGGER
INSERT
UPDATE
DELETE
DROP
ALTER
VACUUM
REINDEX
ANALYZE
PRAGMA wal_checkpoint
PRAGMA optimize
ATTACH with write intent
```

The script must not write output files into the source database directories.

The script must not modify source database timestamps or sidecars as part of extraction.

The script should record pre/post source file state where practical.

---

# sys76 Placement Policy

The MARK script creates a retrievable artifact on `/root/Desktop/`.

The user manually downloads the archive from MARK.

The user manually places the extracted fixture into the sys76 VDB repository.

Recommended sys76 destination:

```text
~/dev/portfolio_projects/variant_database/tests/fixtures/phase4/
```

The fixture should be placed so that the local VDB test suite can reference:

```text
tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

The contract does not require the MARK script to know the sys76 filesystem.

The contract does not require the MARK script to write directly to sys76.

---

# Git Tracking Policy

The script used to create the fixture should be git-tracked:

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

The contract should be git-tracked:

```text
docs/contracts/golden_fixtures/phase4_registration_unit_golden_fixture_contract.md
```

The sister plan should be git-tracked:

```text
docs/plans/golden_fixtures/phase4_registration_unit_golden_fixture_plan.md
```

After the archive is manually retrieved and placed into sys76 VDB, the lightweight fixture files may be git-tracked if their size is reasonable.

At minimum, the following fixture artifacts should be considered for git tracking:

```text
tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/
tests/fixtures/phase4/manifests/
tests/fixtures/phase4/reports/
tests/fixtures/phase4/lineage/
tests/fixtures/phase4/expected/
```

If the compressed fixture is too large for normal git tracking, the repository must track at least:

```text
the extraction script
the contract
the plan
the manifest
the report
the lineage summaries
the checksum summaries
instructions for restoring the fixture artifact
```

The preferred outcome is a lightweight fixture small enough to git-track.

---

# Hardcoded Path Policy

Hardcoded MARK source paths are allowed in:

```text
scripts/mark/create_phase3_lightweight_emulation.py
```

because this script is a controlled MARK execution utility.

Hardcoded MARK source paths are not allowed as a general pattern in canonical VDB implementation code.

The script should document all hardcoded source paths near the top of the file.

The script should fail loudly if expected source paths are absent.

The script should not search broadly across the filesystem for replacement source databases.

This protects provenance by ensuring the fixture is derived from the declared certified source corpus.

---

# Authority Boundary

The fixture has development authority only.

The fixture may support:

```text
local test development
local fixture validation
Phase 4.1 inspector implementation
Phase 4.2 corpus generation development
early Phase 4 downstream development
review of compressed real-row behavior
```

The fixture must not be treated as:

```text
source evidence
producer evidence
biological truth
clinical truth
RDGP reasoning output
Phase 3 certification
Phase 4 certification
MARK full-corpus validation
release certification
```

Passing tests against the fixture does not certify Phase 4.

Passing tests against the fixture authorizes moving toward MARK smoketesting, not skipping it.

---

# Acceptance Criteria

The Phase 4 Registration Unit golden fixture satisfies this contract when all of the following are true:

```text
The extraction script is git-tracked at scripts/mark/create_phase3_lightweight_emulation.py.

The extraction script runs on MARK.

The extraction script reads the six declared Phase 3 certified VDB Registration
Unit SQLite files.

The extraction script writes only to /root/Desktop/.

The extraction script does not mutate MARK VDB, VAP, or producer repository
structures.

The extraction script creates a retrievable output directory and .tgz archive.

The output archive contains six compressed Registration Unit directories.

Each compressed Registration Unit directory contains one vdb.sqlite file.

Each compressed vdb.sqlite preserves the required registration-facing table
surface.

schema_metadata, tep_packages, artifacts, and assertion_registrations are copied
completely unless a documented failure occurs.

source_identities is compressed by deterministic real-row selection.

No synthetic source identity rows are created.

No synthetic biological rows are created.

Selection lineage is emitted for selected source_identities rows.

Copied-table lineage is emitted for full-copy tables.

Source database audit artifacts are emitted.

Fixture database audit artifacts are emitted.

Checksum artifacts are emitted.

The human-readable report explains source corpus, compression policy, priority
seed capture, known limitations, and authority boundary.

The resulting archive can be manually retrieved to sys76.

The extracted fixture can be placed under tests/fixtures/phase4/ in the sys76 VDB
repository.

The fixture supports rapid local Phase 4 development without requiring local
copies of the full MARK SQLite corpus.
```

---

# Out Of Scope

This contract does not require the fixture to preserve all source rows.

This contract does not require the fixture to preserve MARK-scale row volume.

This contract does not require the fixture to preserve full VAP biological breadth.

This contract does not require the fixture to preserve full GSC biological breadth.

This contract does not require the fixture to prove Phase 4 correctness.

This contract does not require the fixture to replace MARK smoketesting.

This contract does not require the fixture to test malformed SQLite inputs.

This contract does not require negative fixture cases.

This contract does not require stress testing.

This contract does not require topology, geometry, surface, or projection correctness.

Those concerns belong to later validation layers, additional fixtures, or MARK full-corpus tests.

---

# Required Sister Plan

This contract must be accompanied by a sister implementation plan:

```text
docs/plans/golden_fixtures/phase4_registration_unit_golden_fixture_plan.md
```

The plan should define how to:

```text
implement the MARK-side extraction script
declare hardcoded source paths
open source SQLite files read-only
copy full-copy tables
select source_identities rows deterministically
emit compressed output SQLite files
emit lineage artifacts
emit source and fixture audits
emit manifests and reports
create the retrievable archive
transfer and place the fixture on sys76
validate the local fixture before Phase 4.1 development relies on it
preserve the distinction between lightweight fixture testing and MARK smoketesting
```

The contract defines what must remain true.

The plan defines how to build, retrieve, place, and validate the fixture.

---

# Summary

The Phase 4 Registration Unit golden fixture is a compressed, real-row-derived development substrate created from the six certified Phase 3 VDB Registration Unit SQLite databases on MARK.

It is created by read-only extraction.

It writes only to `/root/Desktop/`.

It is manually retrieved to sys76.

It supports rapid local Phase 4 development without requiring local copies of the full MARK SQLite corpus.

It preserves source-derived structure and selected real rows.

It compresses MARK-scale volume.

It emits lineage and audit artifacts.

It does not synthesize biological rows.

It does not mutate MARK repositories.

It does not replace MARK certification.

Its operating doctrine is:

```text
Real source rows, compressed volume, deterministic selection, traceable lineage,
read-only MARK execution, no authority inflation.
```

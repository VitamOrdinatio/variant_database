# Registration Unit Input Manifest Specification

## Purpose

This document specifies the Phase 4 Registration Unit input manifest used by VDB.

The manifest declares Registration Units that Phase 4 code is allowed to inspect.

The manifest is the entry point for Phase 4.1 Registration Unit handling.

It supports both:

```text
Validation Layer 2:
    lightweight local golden fixture on sys76

Validation Layer 3:
    full certified MARK Registration Unit corpus for heavy smoketesting
```

The manifest provides declared inputs.

It does not inspect SQLite contents.

It does not certify Registration Units.

It does not mutate Registration Units.

---

# Core Invariant

```text
The manifest declares Registration Units.
It does not inspect them.
It does not certify them.
It does not mutate them.
```

Expanded:

```text
A Registration Unit input manifest is a declarative list of Registration Unit
locations and expected execution context. Runtime code may load and resolve the
manifest before opening any SQLite database, but manifest loading itself must
not perform SQLite inspection or alter source artifacts.
```

---

# Specification Status

```text
IMPLEMENTATION SPECIFICATION FOR PHASE 4.1
```

This specification governs:

```text
manifest file format
required manifest columns
allowed field values
path resolution behavior
pre-inspection validation
relationship to lightweight fixture testing
relationship to MARK full-corpus smoketesting
non-mutation boundaries
```

---

# Manifest Format

The manifest must be a TSV file.

Required delimiter:

```text
tab
```

Required encoding:

```text
UTF-8
```

Required header:

```text
manifest_schema_version
registration_unit_id
registration_unit_label
producer_family
validation_layer
source_role
registration_backend
registration_unit_path
sqlite_path
expected_read_mode
notes
```

The manifest must contain one row per declared Registration Unit.

The manifest must not contain duplicate `registration_unit_id` values.

The manifest should not contain duplicate `registration_unit_label` values within a single execution manifest.

---

# Required Columns

## `manifest_schema_version`

Version of the input manifest schema.

Allowed initial value:

```text
v1
```

## `registration_unit_id`

Stable manifest-local identifier for the Registration Unit.

This value is used by Phase 4 runtime code and emitted artifacts.

Recommended pattern:

```text
ru_<producer_or_source>_<label>
```

Examples:

```text
ru_gsc_epilepsy
ru_gsc_mitochondrial_disease
ru_vap_hg002
ru_vap_median_ERR10619300
ru_vap_q1_ERR10619212
ru_vap_q3_ERR10619225
```

## `registration_unit_label`

Human-readable and filesystem-aligned Registration Unit label.

Examples:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

## `producer_family`

Producer family represented by the Registration Unit.

Allowed initial values:

```text
GSC
VAP
```

Future producer families may be added by specification revision.

## `validation_layer`

Validation layer represented by the manifest row.

Allowed initial values:

```text
validation_layer_2_lightweight_fixture
validation_layer_3_mark_full_corpus
```

## `source_role`

Role of the declared source corpus.

Allowed initial values:

```text
phase4_golden_fixture
mark_phase3_canonical_full_corpus
```

## `registration_backend`

Backend used by the Registration Unit.

Allowed initial value:

```text
sqlite
```

Future backends require specification revision.

## `registration_unit_path`

Path to the Registration Unit directory.

For the local lightweight fixture, this should usually be repo-relative.

For MARK full-corpus smoketesting, this may be an absolute MARK path.

Examples:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_hg002
```

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/vap_hg002
```

## `sqlite_path`

Path to the SQLite file.

Recommended value when `registration_unit_path` points to the Registration Unit directory:

```text
vdb.sqlite
```

If `sqlite_path` is relative, it is resolved relative to `registration_unit_path`.

If `sqlite_path` is absolute, it is used as declared.

## `expected_read_mode`

Expected runtime access mode.

Allowed initial value:

```text
read_only
```

The manifest must not request writable access.

## `notes`

Free-text operator notes.

This field may be empty.

---

# Path Resolution Rules

Manifest path resolution must be deterministic.

## Rule 1 — Registration Unit Path

If `registration_unit_path` is absolute, it must be used as declared.

If `registration_unit_path` is relative, it must be resolved against the VDB repository root or an explicitly supplied manifest base directory.

## Rule 2 — SQLite Path

If `sqlite_path` is absolute, it must be used as declared.

If `sqlite_path` is relative, it must be resolved relative to the resolved `registration_unit_path`.

## Rule 3 — No Filesystem Search

The loader must not search broadly for replacement SQLite files.

If a declared path is absent, the loader must emit a deterministic failure.

## Rule 4 — No Mutation

Path resolution must not create directories.

Path resolution must not create files.

Path resolution must not open SQLite databases.

Path resolution must not alter source artifacts.

---

# Manifest Loading Responsibilities

The manifest loader is responsible for:

```text
reading the TSV
validating required columns
validating required values
checking duplicate registration_unit_id values
checking duplicate registration_unit_label values
resolving registration_unit_path
resolving sqlite_path
confirming path syntax
optionally confirming declared sqlite_path exists
returning normalized Registration Unit declarations
```

The manifest loader is not responsible for:

```text
opening SQLite files
inspecting SQLite table surfaces
counting rows
checking source identities
emitting Registration Unit inventory
emitting readiness artifacts
certifying Registration Units
```

Those responsibilities belong to later Phase 4.1 inspection and validation steps.

---

# Normalized Manifest Record

Runtime code should normalize each manifest row into a structured record.

Recommended normalized fields:

```text
manifest_schema_version
registration_unit_id
registration_unit_label
producer_family
validation_layer
source_role
registration_backend
registration_unit_path_declared
sqlite_path_declared
registration_unit_path_resolved
sqlite_path_resolved
expected_read_mode
notes
```

The normalized record may also include loader metadata:

```text
manifest_path
manifest_row_number
path_resolution_status
declaration_status
```

---

# Local Golden Fixture Manifest

The local lightweight fixture manifest should declare all six compressed Registration Units.

Recommended path:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/manifests/registration_unit_input_manifest.tsv
```

Expected Registration Unit root:

```text
tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/
```

Example rows:

```tsv
manifest_schema_version	registration_unit_id	registration_unit_label	producer_family	validation_layer	source_role	registration_backend	registration_unit_path	sqlite_path	expected_read_mode	notes
v1	ru_gsc_epilepsy	gsc_epilepsy	GSC	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/gsc_epilepsy	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
v1	ru_gsc_mitochondrial_disease	gsc_mitochondrial_disease	GSC	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/gsc_mitochondrial_disease	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
v1	ru_vap_hg002	vap_hg002	VAP	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_hg002	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
v1	ru_vap_median_ERR10619300	vap_median_ERR10619300	VAP	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_median_ERR10619300	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
v1	ru_vap_q1_ERR10619212	vap_q1_ERR10619212	VAP	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_q1_ERR10619212	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
v1	ru_vap_q3_ERR10619225	vap_q3_ERR10619225	VAP	validation_layer_2_lightweight_fixture	phase4_golden_fixture	sqlite	tests/fixtures/phase4/phase4_registration_unit_golden_fixture_2026_06_29_155520/phase4_registration_unit_golden_fixture/registration_units/mark_phase3_canonical_6sqlite_lightweight/vap_q3_ERR10619225	vdb.sqlite	read_only	MARK-derived compressed real-row fixture
```

---

# MARK Full-Corpus Smoketest Manifest

The MARK full-corpus smoketest manifest should declare the six full certified Registration Unit SQLite files.

Recommended path:

```text
configs/mark/phase4_registration_unit_heavy_smoketest_manifest.tsv
```

Expected MARK Registration Unit root:

```text
/root/dev/portfolio_projects/variant_database/results/registration/mark_phase3_canonical/
```

The MARK full-corpus manifest should use:

```text
validation_layer_3_mark_full_corpus
```

and:

```text
mark_phase3_canonical_full_corpus
```

The same Phase 4.1 manifest loader must support both the local lightweight manifest and the MARK full-corpus smoketest manifest.

Only the manifest path and output directory should differ between local fixture execution and MARK full-corpus smoketest execution.

---

# Pre-Inspection Validation

Manifest validation must occur before SQLite inspection.

A manifest row is valid when:

```text
all required fields are present
manifest_schema_version is v1
registration_unit_id is non-empty
registration_unit_label is non-empty
producer_family is allowed
validation_layer is allowed
source_role is allowed
registration_backend is sqlite
registration_unit_path resolves deterministically
sqlite_path resolves deterministically
expected_read_mode is read_only
```

Optional filesystem validation may confirm:

```text
resolved registration_unit_path exists
resolved sqlite_path exists
resolved sqlite_path is a file
```

Filesystem validation must not open SQLite files.

---

# Failure Policy

Manifest loading must fail deterministically when:

```text
the manifest file is missing
the manifest file cannot be parsed as TSV
required columns are missing
required fields are blank
manifest_schema_version is unsupported
producer_family is unsupported
validation_layer is unsupported
source_role is unsupported
registration_backend is unsupported
expected_read_mode is not read_only
registration_unit_id is duplicated
registration_unit_path cannot be resolved
sqlite_path cannot be resolved
filesystem validation is requested and declared paths are absent
```

Manifest loading should emit warnings, not failures, when:

```text
notes is blank
registration_unit_label contains implementation-specific sample identifiers
a path is absolute but allowed by the execution profile
```

---

# Non-Mutation Requirements

Manifest loading must not mutate the filesystem.

Manifest loading must not open SQLite databases.

Manifest loading must not create output directories.

Manifest loading must not create cache files.

Manifest loading must not rewrite the manifest.

Manifest loading must not normalize paths by modifying the source manifest file.

Runtime SQLite inspection must occur in a later phase using read-only access.

---

# Runtime Boundary

The manifest layer ends after producing normalized Registration Unit declarations.

The next layer, Registration Unit inspection, may:

```text
open SQLite files read-only
inspect required table surface
inspect required columns
count rows
emit inventory artifacts
emit readiness artifacts
perform non-mutation checks
```

The manifest layer must not perform those tasks.

---

# Acceptance Criteria

This specification is satisfied when:

```text
a TSV manifest format is defined
required columns are declared
allowed values are declared
path resolution behavior is declared
manifest loading is separated from SQLite inspection
local lightweight fixture manifest can be represented
MARK full-corpus smoketest manifest can be represented
manifest loading does not mutate source artifacts
manifest loading emits normalized Registration Unit declarations
```

---

# Summary

The Registration Unit input manifest is the declarative entry point for Phase 4.1.

It tells VDB which Registration Units are in scope, where their SQLite files are located, what producer family they represent, and which validation layer they support.

It does not inspect, certify, or mutate Registration Units.

Its operating rule is:

```text
Declare first.
Inspect later.
Never mutate.
```

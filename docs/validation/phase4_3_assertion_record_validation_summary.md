# Phase 4.3 Assertion Record Validation Summary

This document records the validation status of the Phase 4.3 Assertion Record layer for the canonical MARK Phase 4 corpus generation `mark_phase4_corpus_6tep_v1`.

The official validation receipt is stored at:

```text
results/validation/phase4_assertion_records/mark_phase4_corpus_6tep_v1_validation_2026_07_02_202002/
```

## Validation Conclusion

Phase 4.3 is closure-candidate complete for `mark_phase4_corpus_6tep_v1`.

The canonical six-unit corpus produced 52 preserved Assertion Records, 204 Source Identity Set groups, and 147,941,196 represented source identities with zero input mutations. The resulting Assertion Record surface is suitable as the governed downstream substrate for Phase 4.4+ Evidence Topology work.

This summary supports Phase 4.3 closure. A separate closure note or milestone update may formally declare Phase 4.3 closed and authorize Phase 4.4 execution.

## Validation Scope

| Field | Value |
|---|---|
| Phase | 4.3 |
| Layer | Assertion Records |
| Corpus Generation | `mark_phase4_corpus_6tep_v1` |
| Validation Layer | Layer 3 MARK full-corpus smoketest |
| Official Receipt | `results/validation/phase4_assertion_records/mark_phase4_corpus_6tep_v1_validation_2026_07_02_202002/` |
| Result | Passed |
| Runtime | 398.422 seconds / 6.64 minutes |
| Prime Directive Input Mutations | 0 |

The validated corpus contains six Registration Units:

```text
gsc_epilepsy
gsc_mitochondrial_disease
vap_hg002
vap_median_ERR10619300
vap_q1_ERR10619212
vap_q3_ERR10619225
```

## Official Receipt Structure

The official receipt folder contains the MARK retrieval archive, the external checksum sidecar, and a readable extracted summary subset for auditability.

```text
results/validation/phase4_assertion_records/mark_phase4_corpus_6tep_v1_validation_2026_07_02_202002/
├── README.md
├── receipt_audit.json
├── receipt_audit.tsv
├── receipt_summary_manifest.tsv
├── build_output_audit.tsv
├── retrieval/
│   ├── phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz
│   └── phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz.sha256
└── extracted_receipt_summary/
    ├── validation_summary.json
    ├── validation_summary.tsv
    ├── runtime_metadata.json
    ├── runtime_metadata.tsv
    ├── run_manifest.json
    ├── bundle_report.json
    ├── bundle_report.tsv
    ├── count_reconciliation.tsv
    ├── preservation_hardening_report.tsv
    ├── source_identity_reconciliation.tsv
    ├── input_mutation_report.tsv
    └── output_file_manifest.tsv
```

The `.tgz` archive is the canonical MARK retrieval artifact. The extracted summary files are staged to make the validation state reviewable without unpacking the full archive.

## Validation Result

The MARK full-corpus smoketest passed with all required checks successful.

| Metric | Result |
|---|---:|
| Overall Status | passed |
| Validation Checks Passed | 18 |
| Validation Checks Failed | 0 |
| Runtime Seconds | 398.422 |
| Runtime Minutes | 6.64 |
| Input Mutations | 0 |

The Prime Directive was preserved: Phase 4.2 Corpus Generation inputs and Registration Unit SQLite inputs were treated as read-only substrate, and no input file mutations were detected.

## Core Count Reconciliation

| Count | Expected | Observed | Status |
|---|---:|---:|---|
| Registration Units | 6 | 6 | passed |
| Input Assertions | 52 | 52 | passed |
| Output Assertion Records | 52 | 52 | passed |
| VAP Assertion Records | 40 | 40 | passed |
| GSC Assertion Records | 12 | 12 | passed |
| Downstream Topology Manifest Rows | 52 | 52 | passed |
| Source Identity Set Groups | 204 | 204 | passed |
| Source Identity Summary Groups | 204 | 204 | passed |
| Source Identities Represented | 147,941,196 | 147,941,196 | passed |

This count reconciliation establishes that the Phase 4.3 builder preserved all assertion registrations from the canonical six-unit corpus and produced the expected source identity set accounting without flattening the source identity universe.

## Preservation and Resolver Semantics

Phase 4.3 separates preservation status from resolver status.

```text
preservation_status != resolver_status
```

Preservation status answers whether the Assertion Record was preserved as an Assertion Record. Resolver status answers how mature the downstream resolver interpretation is for that record.

| Status Plane | Status | Count |
|---|---|---:|
| preservation_status | preserved | 52 |
| resolver_status | supported | 26 |
| resolver_status | indexed_with_note | 14 |
| resolver_status | deferred | 12 |

All 52 Assertion Records are preserved. The 12 deferred records are preserved records whose downstream resolver interpretation is deferred; they are not dropped, missing, or unpreserved.

This distinction is required for downstream Phase 4.4+ work. Evidence Topology may derive organization from preserved Assertion Records, but it must not confuse resolver immaturity with substrate loss.

## Participant and Source Identity Preservation

The MARK corpus contains 147,941,196 source identities. Phase 4.3 intentionally does not flatten those identities into enumerated participant rows.

Instead, `assertion_record_participants.tsv` acts as a compact participant bridge to Source Identity Sets.

| Output | Rows | Role |
|---|---:|---|
| `assertion_record_participants.tsv` | 204 | Compact participant bridge rows |
| `assertion_record_source_identity_sets.tsv` | 204 | Source Identity Set definitions |
| `assertion_record_source_identity_summary.tsv` | 204 | Source Identity Set counts and summaries |

All participant rows use:

```text
participant_source = source_identity_set_reference
```

All participant `source_identity_set_id` values join to `assertion_record_source_identity_sets.tsv`. All summary `source_identity_set_id` values also join to `assertion_record_source_identity_sets.tsv`.

The participant table therefore preserves role-bearing participant substrate by reference. It does not enumerate the full source identity universe and does not collapse Source Identity Sets into flat records.

Two Assertion Records do not have Source Identity Set obligations. These are the expected GSC `producer_contract_validation` records and are represented with:

```text
source_identity_set_status = not_applicable
```

This is legitimate not-applicable status, not participant loss.

## Lineage and Governed Missingness

Row-level `source_record_ref` is absent for all 52 Assertion Records in the canonical MARK corpus. This absence is explicitly represented.

| Field | Status | Count |
|---|---|---:|
| `source_record_ref` | empty | 52 |
| `source_record_ref_status` | explicit_absence | 52 |
| `lineage_completeness_status` | artifact_level_lineage_present_row_ref_absent | 52 |

This is governed source-level absence of row-level `source_record_ref`, not code-injected missingness.

Artifact-level lineage is preserved through:

```text
source_artifact_relative_path
source_artifact_sha256
source_artifact_size_bytes
```

Phase 4.3 must preserve true missingness when the incoming TEP substrate lacks a row-level source reference. It must not introduce missingness through inadequate builder logic. This validation receipt demonstrates that row-level absence is explicitly status-encoded while artifact-level provenance remains present.

## Validation Report Alignment

The Assertion Record validation report is assertion-aligned.

| Output | Rows |
|---|---:|
| `assertion_record_index.tsv` | 52 |
| `assertion_record_validation_report.tsv` | 52 |

The validation report no longer contains duplicate rows for source-identity-not-applicable assertions. GSC `producer_contract_validation` records are represented as:

```text
preservation_status = preserved
resolver_status = indexed_with_note
validation_status = indexed_with_note
source_identity_set_status = not_applicable
message = Artifact-level validation assertion without source identity set obligation.
```

This keeps the validation plane assertion-aligned and avoids conflating resolver status with source identity obligation status.

## Checksum and Retrieval Governance

The authoritative archive checksum is the external `.tgz.sha256` sidecar stored next to the retrieval archive.

```text
retrieval/phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz
retrieval/phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz.sha256
```

The internal bundle report declares:

```text
bundle_checksum_authority = external_sidecar
internal_archive_sha256_claim = false
```

The internal bundle report does not make a self-referential `bundle_sha256` claim for the archive containing itself. This prevents checksum incoherence and preserves clear retrieval authority.

## Downstream Readiness

Phase 4.4+ may consume the Phase 4.3 Assertion Record surface as the governed substrate for Evidence Topology derivation.

The primary downstream files are:

```text
assertion_record_index.tsv
assertion_record_participants.tsv
assertion_record_source_identity_sets.tsv
assertion_record_source_identity_summary.tsv
assertion_record_lineage.tsv
assertion_record_payload_references.tsv
downstream_topology_input_manifest.tsv
```

Phase 4.4 may derive Evidence Topology from Assertion Records. It must not reinterpret Registration Units as topology, and it must not flatten Source Identity Sets into enumerated participant rows unless a governed downstream projection explicitly requires such expansion.

## Validation Boundary

This validation summary establishes Phase 4.3 Assertion Record readiness for the canonical MARK corpus generation `mark_phase4_corpus_6tep_v1`.

It does not certify downstream Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces, Projection Views, or RDGP reasoning outputs. Those are downstream phases and must be derived from the preserved Assertion Record substrate under their own validation rules.

## Closure Support Statement

The Phase 4.3 Assertion Record layer has met its validation obligations for `mark_phase4_corpus_6tep_v1`:

```text
Registration Units preserve custody.
Corpus Generations declare scope.
Assertion Records preserve scientific claims.
Source Identity Sets preserve the participant/evidence universe attached to claims.
Evidence Topology derives organization.
```

The official receipt demonstrates preserved assertion cardinality, source identity set accounting, explicit missingness semantics, artifact-level lineage preservation, validation-report alignment, external-sidecar checksum governance, runtime observability, and Prime Directive compliance.

This document supports formal Phase 4.3 closure and authorizes Phase 4.4 Evidence Topology work to proceed from the preserved Assertion Record surface.

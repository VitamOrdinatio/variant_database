# Phase 4.3E MARK Full-Corpus Validation Receipt

This folder stages the official VDB Phase 4.3E MARK full-corpus Assertion Record smoketest receipt for `mark_phase4_corpus_6tep_v1`.

## Canonical retrieval artifacts

```text
retrieval/phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz
retrieval/phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz.sha256
```

The `.tgz.sha256` sidecar is the sole authoritative checksum for the archive.

## Validation result

```text
overall_status: passed
archive_sha256: ae909025d0c581262bdd25fce0c56630d4595395b945b43114c74139480cf6ff
started_at_utc: 2026-07-03T00:20:02Z
completed_at_utc: 2026-07-03T00:26:41Z
duration_seconds: 398.422
duration_minutes: 6.64
```

## Core substrate counts

```text
registration_units: 6
assertion_records: 52
vap_assertions: 40
gsc_assertions: 12
source_identity_set_groups: 204
source_identity_summary_groups: 204
source_identity_total: 147,941,196
participant_bridge_rows: 204
validation_report_rows: 52
```

## Staged contents

```text
retrieval/                  canonical MARK archive and external checksum sidecar
extracted_receipt_summary/  diffable receipt metadata extracted from the archive
receipt_audit.json          local audit proving the staged receipt is coherent
receipt_audit.tsv           TSV form of the local audit
build_output_audit.tsv      row counts and hashes for key Assertion Record outputs inside the archive
receipt_summary_manifest.tsv copied receipt-summary files and hashes
```

## Verify manually

From this directory:

```bash
cd retrieval
sha256sum -c phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz.sha256
tar -tzf phase4_3_mark_full_corpus_assertion_record_smoketest_2026_07_02_202002.tgz | head
```

The full Assertion Record build output is preserved inside the archive under:

```text
results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/
```

# HG002 WGS Stress-Test Retirement Policy

> Status: VDB architecture policy.
> This document defines when HG002 may be retired from active VDB working
> storage after serving as the WGS stress-test member of the 6TEP proof corpus.
> It is a data-stewardship and reproducibility policy, not a deletion script.

## 1. Purpose

VDB uses heterogeneous Transportable Evidence Products (TEPs) to validate a
preservation-first genomic evidence architecture. The current stress-test proof
corpus includes:

```text
4 TEP-VAPs:
    HG002 WGS
    epilepsy WES q1
    epilepsy WES median
    epilepsy WES q3

2 TEP-GSCs:
    epilepsy semantic priors
    mitochondrial disease semantic priors
```

HG002 is scientifically valuable because it exercises VDB against a
WGS-scale VAP evidence product. It is also storage-expensive and is not a
biological control for epilepsy-oriented reasoning.

This policy defines how VDB can preserve the scientific proof provided by HG002
without requiring bulky HG002-derived working artifacts to remain in active
storage indefinitely.

## 2. Decision Summary

HG002 should remain active until VDB captures receipts showing that the WGS-scale
TEP-VAP successfully survived the preservation chain:

```text
TEP-VAP
    -> Registration Unit
        -> Corpus Generation
            -> Assertion Records
                -> Evidence Topology v2
                    -> validation, identity, checksum, and storage receipts
```

After those receipts are preserved, bulky HG002-derived VDB working artifacts
may be retired from active storage. Source identity, manifests, checksums,
validation summaries, topology summaries, command/run context, and cold-storage
references must remain auditable.

## 3. HG002 Role in VDB

HG002 should be treated as:

```text
WGS stress-test specimen
benchmark-derived VAP TEP
coordinate-scale validation member
large-artifact preservation challenge
```

HG002 should not be treated as:

```text
normal control
healthy comparator
disease-control specimen
case-control reference
epilepsy cohort member
```

HG002 was critical for VAP benchmarking. In VDB, its role is different: it tests
whether a WGS-scale producer package can be registered, preserved, summarized,
and propagated into topology-ready evidence handles without collapsing coordinate
evidence, source identity, provenance, metadata, or feature declarations.

## 4. Retirement Invariant

The governing invariant is:

```text
Do not delete HG002 from VDB history.
Retire only bulky, regenerable HG002-derived working artifacts after receipt capture.
```

Retirement means:

```text
remove heavy active working copies
preserve compact scientific receipts
preserve source package identity
preserve manifests and checksums
preserve validation outcomes
preserve enough context to regenerate or audit the stress test
```

Retirement does not mean:

```text
erase evidence that HG002 was used
erase corpus membership history
erase source package identity
erase validation receipts
erase scientific rationale
silently relabel the corpus after membership changes
```

This policy treats storage retirement as part of reproducible scientific data
stewardship: heavy derived artifacts may leave active storage only after the
proof they provided remains auditable.

## 5. Safe Retirement Gate

HG002 may be retired from active VDB working storage only after the following
gate has passed:

```text
HG002 WGS Stress-Test Gate

Required pass:
    6TEP WGS stress corpus registration
    Corpus Generation
    Assertion Record generation
    Evidence Topology v2
    identity and namespace-preservation audit
    validation receipt capture
    checksum / manifest receipt capture
    storage and scale summary capture
```

The identity and namespace-preservation audit confirms that source identifiers,
namespace labels, source package identity, declaration-set handles, and lineage
references survived the preservation chain. It does not require full downstream
namespace mediation unless a later VDB policy explicitly declares that mediation
as part of the retirement gate.

The safe removal point is not registration success alone. HG002 completes its
VDB role only after VDB demonstrates that the WGS-scale substrate survives
registration, corpus generation, Assertion Records, Evidence Topology, and
receipt capture.

## 6. Required Receipt Package

Before retirement, capture a compact receipt package sufficient for future
inspection, regeneration, or audit.

Recommended permanent documentation and receipt paths:

```text
docs/architecture/hg002_wgs_stress_test_retirement_policy.md
docs/status/hg002_wgs_stress_test_receipt.md
docs/validation/hg002_wgs_retirement_validation_receipt.md

results/phase4/stress_receipts/hg002_wgs_6tep_stress_test/

docs/manifests/vdb_6tep_wgs_stress_corpus_manifest.md
```

Recommended receipt contents:

```text
README.md
run_manifest.yaml or command_log.txt
git_commit.txt
environment_snapshot.txt
hg002_source_package_manifest.tsv
hg002_artifact_checksums.tsv
hg002_registration_summary.tsv
hg002_corpus_generation_summary.tsv
hg002_assertion_record_summary.tsv
hg002_topology_v2_summary.tsv
hg002_identity_namespace_preservation_summary.tsv
hg002_storage_footprint_summary.tsv
hg002_retirement_receipt.md
```

The receipt package should make clear:

```text
what HG002 was
why HG002 was included
which corpus included it
which VDB phases consumed it
which validations passed
how large the active storage footprint was
why active-storage retirement was appropriate
which artifacts remain retained
which active working artifacts were removed
how the stress test could be regenerated or audited
```

## 7. Corpus Identity After Retirement

Do not silently reuse a corpus name after HG002 is removed from active routine
use. Corpus membership is part of corpus identity.

Recommended names:

```text
mark_phase4_corpus_6tep_wgs_stress_v1
mark_phase4_corpus_5tep_core_v1
```

Meaning:

```text
6TEP WGS stress corpus:
    proves VDB can handle one WGS-scale VAP TEP plus WES and GSC heterogeneity.

5TEP core corpus:
    supports storage-efficient routine VDB development after WGS stress proof.
```

The 5TEP core corpus should not be compared to the 6TEP WGS stress corpus unless
the membership difference is explicitly declared.

## 8. Retain vs Remove

Only VDB-derived working artifacts may be retired from active storage under this
policy. Producer-owned source artifacts must either remain retained or have a
documented cold-storage location and checksum.

After the retirement gate passes, the following may be removed from active VDB
working storage:

```text
heavy materialized HG002 registration copies
large scratch extraction products
large HG002-derived intermediate VDB tables
temporary topology expansion artifacts that can be regenerated
intermediate files duplicated elsewhere with checksums
bulky working outputs that are summarized in receipt artifacts
```

The following must remain available locally, in cold storage, or through
manifest/checksum receipts:

```text
original HG002 TEP-VAP or cold-storage location
source VCF path/checksum receipt where applicable
HG002 VAP run manifest
TEP-VAP package manifest
artifact checksum manifest
VDB stress-test receipt package
validation summaries
topology summaries
identity/namespace preservation summaries
storage-footprint summaries
retirement decision note
```

If local storage cannot retain the original HG002 TEP-VAP, the retirement
receipt must state:

```text
where the cold artifact resides
which checksum verifies it
which command or path can recover it
which VDB receipts remain locally available
which limitations are introduced by cold-only storage
```

## 9. Minimum Retirement Checklist

HG002 should not be retired from active VDB working storage until all applicable
items below are complete:

```text
[ ] HG002 is represented in the 6TEP WGS stress corpus manifest.
[ ] HG002 Registration Unit completes successfully.
[ ] HG002 source package ID is preserved.
[ ] HG002 TEP ID is preserved.
[ ] HG002 run ID is preserved.
[ ] HG002 sample ID is preserved.
[ ] HG002 artifact paths and checksums are captured.
[ ] HG002 contributes expected Assertion Records.
[ ] HG002 coordinate declaration handles survive into topology.
[ ] HG002 feature declaration handles survive into topology where applicable.
[ ] Evidence Topology v2 passes with HG002 included.
[ ] Identity and namespace-preservation audit passes with HG002 included.
[ ] Validation receipts are captured.
[ ] Storage footprint and scale metrics are recorded.
[ ] A retirement receipt is written.
[ ] Documentation states that HG002 was a WGS stress-test member, not a disease control.
[ ] A smaller non-HG002 routine corpus can still run after HG002 active-storage retirement.
```

## 10. Conditional Genotype-Preservation Supplement

If a genotype-preservation supplement lands before HG002 retirement, then the
retirement receipt should also capture genotype-observation status:

```text
[ ] HG002 genotype observations are generated or referenced.
[ ] Genotype observations trace to source VCF FORMAT/sample fields.
[ ] TEP-VAP manifest includes genotype observations or a genotype supplement.
[ ] VDB can ingest, register, or preserve references to genotype-observation evidence.
```

Genotype-observation receipts are required only if the genotype-preservation
supplement has already landed before retirement. HG002 retirement should not be
blocked by an unimplemented future genotype backfill if source VCF identity,
checksum, and recovery path are preserved.

If genotype preservation has not landed, include:

```text
hg002_genotype_preservation_pending.md
```

That document should state whether source VCFs are retained and whether genotype
recovery is expected to be possible without rerunning HG002.

## 11. Relationship to RDGP-Oriented Disease Corpora

HG002 retirement does not weaken future disease-oriented RDGP work.

HG002 serves a WGS-scale VDB preservation stress-test role. RDGP-facing corpora
should be defined separately around disease-relevant VAP and GSC evidence.

A future RDGP-oriented corpus may use:

```text
12 epilepsy TEP-VAPs
2 TEP-GSCs:
    epilepsy semantic priors
    mitochondrial disease semantic priors
```

That disease/prior corpus has a different purpose from the HG002 WGS stress
corpus. HG002 should not be interpreted as an epilepsy control or background
comparator unless a separate study design explicitly justifies that role.

## 12. Risks and Guardrails

DEX-VDB and future maintainers should guard against:

```text
1. Retiring HG002 before topology validation completes.
2. Retiring HG002 before artifact checksums are captured.
3. Recording cold-storage paths without checksums.
4. Removing producer-owned source artifacts without a recoverable cold-storage record.
5. Continuing to call a post-HG002 routine corpus "6TEP".
6. Treating HG002 as disease-cohort evidence in downstream reasoning.
7. Letting HG002 dominate scale summaries without labeling it as a stress-test member.
8. Preserving validation receipts that cannot be linked back to the HG002 source package.
9. Comparing 5TEP core results to 6TEP stress results without declaring corpus membership changes.
10. Allowing storage cleanup to erase the ability to audit or regenerate the stress test.
```

## 13. Retirement Decision Record

The final retirement receipt should include:

```text
decision_id
decision_date
operator
corpus_id
hg002_source_package_id
hg002_tep_id
hg002_run_id
stress_test_verdict
validation_summary
artifact_receipt_location
cold_storage_location_if_applicable
deleted_active_paths
retained_receipt_paths
known limitations
approval_status
```

Suggested verdict labels:

```text
retired_after_successful_stress_test
retirement_deferred_pending_receipts
retirement_deferred_pending_genotype_patch
retirement_deferred_missing_source_artifacts
retirement_rejected
```

## 14. Recommended Final Statement

The final retirement receipt should be able to state:

```text
HG002 successfully passed VDB 6TEP WGS stress-test registration,
Assertion Record preservation, Evidence Topology propagation,
identity/namespace preservation audit, and validation receipt capture.
HG002 is now retired from active routine VDB working storage and retained as a
cold/reference stress-test artifact.
```

If genotype preservation is completed before retirement, include:

```text
HG002 genotype observations were recovered from retained VCF FORMAT/sample fields
and incorporated into the genotype-preservation receipt before active-storage
retirement.
```

## 15. Summary

HG002 is scientifically important to VDB as a WGS-scale stress-test specimen.
It is not scientifically required as a routine disease-corpus member or epilepsy
control.

The correct strategy is:

```text
keep HG002 through the 6TEP WGS stress-test milestone
capture compact scientific receipts
rename post-retirement routine work as a distinct 5TEP core corpus
remove bulky HG002-derived working artifacts from active storage
retain manifests, checksums, validation summaries, topology summaries, and cold-source references
```

This preserves the scientific proof while protecting VDB development from
unnecessary long-term storage burden.

# Corpus Generation Report

## Identity

```text
corpus_generation_id: mark_phase4_corpus_6tep_v1
corpus_generation_label: MARK Phase 4 6-TEP Benchmark Corpus v1
corpus_generation_purpose: Layer 3 MARK full-corpus validation for Phase 4.2 Corpus Generation artifact flow
corpus_generation_version: v1
corpus_generation_validation_status: not_evaluated
corpus_generation_certification_status: not_available
```

## Selection Policy

```text
selection_policy_id: mark_phase4_6tep_certified_input_policy
selection_policy_version: v1
selection_policy_description: Select the six certified MARK Phase 3 canonical Registration Units for Phase 4.2 Corpus Generation Layer 3 full-corpus validation.
```

## Input Selection Manifest

```text
copied_path: results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/scratch_corpus_generation/mark_phase4_corpus_6tep_v1/inputs/corpus_generation_selection_manifest.tsv
sha256: d769d334e032f6f52ec2a2459158b413f3aa97bd501b1f9ae31a5e056a487ca2
record_count: 6
```

## Phase 4.1 Receipt Inputs

```text
registration_unit_inventory_path: results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/phase4_1_receipts/registration_unit_inventory.tsv
registration_unit_readiness_path: results/validation/phase4_corpus_generation/mark_full_corpus_smoketest_2026_06_30_123500/phase4_1_receipts/registration_unit_readiness.tsv
```

## Summary

```text
included_registration_unit_count: 6
excluded_registration_unit_count: 0
downstream_assertion_record_input_count: 6
artifact_count_total: 82
assertion_registration_count_total: 52
source_identity_count_total: 147941196
```

## Included Registration Units

| registration_unit_label | producer_family | readiness | assertions | source_identities |
| --- | --- | --- | --- | --- |
| gsc_epilepsy | GSC | ready | 6 | 89138 |
| gsc_mitochondrial_disease | GSC | ready | 6 | 85434 |
| vap_hg002 | VAP | ready | 10 | 97369849 |
| vap_median_ERR10619300 | VAP | ready | 10 | 15467317 |
| vap_q1_ERR10619212 | VAP | ready | 10 | 19017490 |
| vap_q3_ERR10619225 | VAP | ready | 10 | 15911968 |

## Excluded Or Deferred Registration Units

_None._

## Boundary

This report is a Corpus Generation build artifact.

It is not source truth.

It is not a validation receipt.

It does not certify the Corpus Generation.

It does not create Assertion Records, topology, geometry, surfaces, projections, or biological interpretation.

## Downstream Handoff

```text
downstream_assertion_record_input_manifest_rows: 6
```

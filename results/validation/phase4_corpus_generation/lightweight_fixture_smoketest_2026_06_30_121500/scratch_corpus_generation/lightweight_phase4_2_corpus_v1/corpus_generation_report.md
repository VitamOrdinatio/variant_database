# Corpus Generation Report

## Identity

```text
corpus_generation_id: lightweight_phase4_2_corpus_v1
corpus_generation_label: Lightweight Phase 4.2 Corpus Generation Fixture v1
corpus_generation_purpose: local golden fixture smoketest for Phase 4.2 Corpus Generation
corpus_generation_version: v1
corpus_generation_validation_status: not_evaluated
corpus_generation_certification_status: not_available
```

## Selection Policy

```text
selection_policy_id: lightweight_phase4_2_golden_fixture_policy
selection_policy_version: v1
selection_policy_description: Select a two-unit lightweight golden Corpus Generation fixture with one deferred control row for Phase 4.2 smoketesting.
```

## Input Selection Manifest

```text
copied_path: results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/scratch_corpus_generation/lightweight_phase4_2_corpus_v1/inputs/corpus_generation_selection_manifest.tsv
sha256: 8dcd7335b058dd6697cdfe7bafd5d79a0a92971ca9284e634226dfe84f271b81
record_count: 3
```

## Phase 4.1 Receipt Inputs

```text
registration_unit_inventory_path: results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/phase4_1_receipts/registration_unit_inventory.tsv
registration_unit_readiness_path: results/validation/phase4_corpus_generation/lightweight_fixture_smoketest_2026_06_30_121500/phase4_1_receipts/registration_unit_readiness.tsv
```

## Summary

```text
included_registration_unit_count: 2
excluded_registration_unit_count: 1
downstream_assertion_record_input_count: 2
artifact_count_total: 25
assertion_registration_count_total: 16
source_identity_count_total: 300
```

## Included Registration Units

| registration_unit_label | producer_family | readiness | assertions | source_identities |
| --- | --- | --- | --- | --- |
| gsc_lightweight_fixture | GSC | ready | 6 | 100 |
| vap_lightweight_fixture | VAP | ready | 10 | 200 |

## Excluded Or Deferred Registration Units

| registration_unit_label | exclusion_status | exclusion_rationale |
| --- | --- | --- |
| vap_deferred_lightweight_fixture | deferred | lightweight golden fixture deferred control |

## Boundary

This report is a Corpus Generation build artifact.

It is not source truth.

It is not a validation receipt.

It does not certify the Corpus Generation.

It does not create Assertion Records, topology, geometry, surfaces, projections, or biological interpretation.

## Downstream Handoff

```text
downstream_assertion_record_input_manifest_rows: 2
```

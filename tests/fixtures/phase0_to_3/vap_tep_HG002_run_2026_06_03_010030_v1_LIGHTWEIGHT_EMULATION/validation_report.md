# VAP-TEP Validation Report

Validation status: `pass`

| Criterion | Status | Description | Details |
|---|---|---|---|
| STRUCTURE-001 | PASS | Required top-level manifest keys present |  |
| STRUCTURE-002 | PASS | Manifest type is valid |  |
| STRUCTURE-003 | PASS | Entities field is a list |  |
| STRUCTURE-004 | PASS | Lineage edges field is a list |  |
| AC-010 | PASS | tep_id present | vap_tep_HG002_run_2026_06_03_010030_v1 |
| AC-013A | PASS | tep_schema_version present | vap_tep_v1 |
| AC-011 | PASS | sample_id present | HG002 |
| AC-012 | PASS | run_id present | run_2026_06_03_010030 |
| AC-001 | PASS | observation_entity present |  |
| AC-002 | PASS | normalization_entity present |  |
| AC-003 | PASS | routing_entity present |  |
| AC-004 | PASS | coding_interpretation_overlay present |  |
| AC-005 | PASS | noncoding_interpretation_overlay present |  |
| AC-006 | PASS | prioritization_overlay present |  |
| AC-007 | PASS | validation_overlay present |  |
| AC-009 | PASS | context_sidecar present |  |
| AC-008 | PASS | lineage_manifest present |  |
| AC-017A | PASS | Exactly one instance of each required entity role exists |  |
| AC-017 | PASS | Every entity declares entity_role |  |
| AC-014 | PASS | Every entity preserves source artifact provenance |  |
| AC-026 | PASS | Transport paths exist within package |  |
| AC-024 | PASS | Transported artifact SHA256 values match manifest |  |
| AC-015/AC-016 | PASS | Required parent/child lineage edges present |  |
| AC-027 | PASS | Lineage manifest indexes all required entities |  |
| AC-018 | PASS | Stage07 observation lineage remains traceable into Stage08 normalization lineage | VAP v1 row_count and variant_id_count parity confirmed |
| AC-040 | PASS | Stage08 normalization semantic surface preserved |  |
| AC-041 | PASS | Stage09 coding interpretation semantic surface preserved |  |
| AC-042 | PASS | Stage10 noncoding interpretation semantic surface preserved |  |
| AC-043 | PASS | Stage11 prioritization semantic surface preserved |  |
| AC-044 | PASS | Stage12 validation semantic surface preserved |  |
| AC-029 | PASS | observation_entity preserved |  |
| AC-030 | PASS | normalization_entity preserved |  |
| AC-031A | PASS | coding_interpretation_overlay preserved |  |
| AC-032 | PASS | prioritization_overlay preserved |  |
| AC-033 | PASS | validation_overlay preserved |  |
| AC-031B | PASS | Coding and noncoding interpretation overlays remain present |  |
| AC-028 | PASS | Candidate-only preservation prohibited |  |

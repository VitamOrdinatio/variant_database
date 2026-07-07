# Tier 1 Namespace Provenance Audit — Compact VDB Artifacts

audit_id: `mark_phase4_corpus_6tep_v1_compact_vdb_audit_v1`
corpus_id: `mark_phase4_corpus_6tep_v1`
topology_build_id: `mark_phase4_corpus_6tep_v1_topology_build_v1`
generated_utc: `2026-07-07T07:02:12Z`

## Scope

This Tier 1 audit inspects compact VDB Phase 4 artifacts available on sys76.
It validates handle-level namespace substrate preservation from Phase 4.3 Assertion Records through Phase 4.4 Evidence Topology Step 7.
It does not inspect MARK-only TEP payloads or registration SQLite value-level substrates.

## Interpretation

Passed Tier 1 checks mean compact handles survived.
They do not prove value-level coordinate, feature, or gene bridge provenance; MARK deep traces are required for those questions.

## Artifact Inventory

- `corpus_selection_manifest`: present (6 rows) — `docs/manifests/corpus_generation/mark_phase4_corpus_6tep_v1_selection_manifest.tsv`
- `assertion_record_index`: present (52 rows) — `results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_index.tsv`
- `assertion_record_participants`: present (204 rows) — `results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_participants.tsv`
- `assertion_record_source_identity_sets`: present (204 rows) — `results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_source_identity_sets.tsv`
- `assertion_record_source_identity_summary`: present (204 rows) — `results/phase4/assertion_records/mark_phase4_corpus_6tep_v1/assertion_record_source_identity_summary.tsv`
- `topology_relationships`: present (54 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_relationships.tsv`
- `topology_relationship_members`: present (1232 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_relationship_members.tsv`
- `topology_basis_components`: present (892 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_basis_components.tsv`
- `topology_source_identity_expansion_index`: present (816 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_source_identity_expansion_index.tsv`
- `topology_namespace_mediation`: present (11 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/topology_namespace_mediation.tsv`
- `downstream_geometry_input_manifest`: present (54 rows) — `results/phase4/evidence_topology/mark_phase4_corpus_6tep_v1_topology_build_v1/downstream_geometry_input_manifest.tsv`

## Join / Preservation Check Summary

- passed: 19

No error or critical join/preservation findings were detected in Tier 1 compact artifacts.

## Route Inventory Summary

- GSC / gene_brokerage: 22 Source Identity Sets; represented_source_identity_count=86846; namespaces=`gsc_ensembl_gene_id;gsc_gene_symbol;gsc_source_gene_id`; status=passed_tier1_compact_handles
- GSC / phenotype_or_overlay_brokerage: 10 Source Identity Sets; represented_source_identity_count=38852; namespaces=`gsc_phenotype`; status=passed_tier1_compact_handles
- GSC / producer_or_observation_brokerage: 12 Source Identity Sets; represented_source_identity_count=48874; namespaces=`gsc_provenance_id;gsc_semantic_channel;gsc_source_id`; status=passed_tier1_compact_handles
- VAP / default_coordinate_or_variant_brokerage: 40 Source Identity Sets; represented_source_identity_count=49255528; namespaces=`vap_variant_id`; status=passed_tier1_compact_handles
- VAP / gene_brokerage: 80 Source Identity Sets; represented_source_identity_count=98511056; namespaces=`vap_ensembl_gene_id;vap_gene_symbol`; status=passed_tier1_compact_handles
- VAP / producer_or_observation_brokerage: 40 Source Identity Sets; represented_source_identity_count=40; namespaces=`vap_sample_id`; status=passed_tier1_compact_handles

## Sentinel Candidates For Tier 2 MARK Trace

The candidates below are handle-level representatives selected from compact artifacts. They are intended to guide MARK-side TEP/SQLite deep provenance tracing.

- `vap_variant_id` / `sis_7293b3134b3e588860e2ff60` (VAP, default_coordinate_or_variant_brokerage, count=2891): On MARK, trace vap_variant_id through TEP/SQLite to confirm reference build, contig, start/end or pos, ref, alt, variant type, and observation context.
- `vap_variant_id` / `sis_cec33e159ed11a16e1253fba` (VAP, default_coordinate_or_variant_brokerage, count=4636584): On MARK, trace vap_variant_id through TEP/SQLite to confirm reference build, contig, start/end or pos, ref, alt, variant type, and observation context.
- `vap_ensembl_gene_id` / `sis_bd4a92849d6fb595f360a838` (VAP, gene_brokerage, count=2891): On MARK, trace vap_ensembl_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `vap_ensembl_gene_id` / `sis_a3c34177d611a11c344e0c42` (VAP, gene_brokerage, count=4636584): On MARK, trace vap_ensembl_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `vap_gene_symbol` / `sis_082fa77a30bd1439bda84bd7` (VAP, gene_brokerage, count=2891): On MARK, trace vap_gene_symbol through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `vap_gene_symbol` / `sis_da107139bffb9a615b1f6410` (VAP, gene_brokerage, count=4636584): On MARK, trace vap_gene_symbol through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `vap_sample_id` / `sis_038ba5dc7eac7d9b1c79f884` (VAP, producer_or_observation_brokerage, count=1): On MARK if needed, trace vap_sample_id to confirm producer/run/sample/source/provenance scope remains attached.
- `vap_sample_id` / `sis_ff111d79193606338460a8f3` (VAP, producer_or_observation_brokerage, count=1): On MARK if needed, trace vap_sample_id to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_ensembl_gene_id` / `sis_00058d7dda724ab41a793ce3` (GSC, gene_brokerage, count=3543): On MARK, trace gsc_ensembl_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_ensembl_gene_id` / `sis_e129e1a4a60af61497d36d1a` (GSC, gene_brokerage, count=4405): On MARK, trace gsc_ensembl_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_source_gene_id` / `sis_17ffd89fe7ae37af6b3fdff0` (GSC, gene_brokerage, count=3885): On MARK, trace gsc_source_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_source_gene_id` / `sis_e2d3c4d851d818edeae29454` (GSC, gene_brokerage, count=4398): On MARK, trace gsc_source_gene_id through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_gene_symbol` / `sis_2164cb8fc78d1da857441408` (GSC, gene_brokerage, count=3543): On MARK, trace gsc_gene_symbol through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_gene_symbol` / `sis_4e8a1a45c27177b27a3724a1` (GSC, gene_brokerage, count=4405): On MARK, trace gsc_gene_symbol through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable.
- `gsc_phenotype` / `sis_259bb5ce60af87dbbcad3083` (GSC, phenotype_or_overlay_brokerage, count=3543): On MARK if needed, trace gsc_phenotype to confirm phenotype/release/source scope remains attached to gene or overlay evidence.
- `gsc_phenotype` / `sis_c22c7cb51109959a4b4e283f` (GSC, phenotype_or_overlay_brokerage, count=4405): On MARK if needed, trace gsc_phenotype to confirm phenotype/release/source scope remains attached to gene or overlay evidence.
- `gsc_source_id` / `sis_4e1669630dcf09ba61306c30` (GSC, producer_or_observation_brokerage, count=3885): On MARK if needed, trace gsc_source_id to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_source_id` / `sis_a7aab1a3a976503d7d292c83` (GSC, producer_or_observation_brokerage, count=4405): On MARK if needed, trace gsc_source_id to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_provenance_id` / `sis_3e4e7be8494c9a9d8388f9bc` (GSC, producer_or_observation_brokerage, count=3543): On MARK if needed, trace gsc_provenance_id to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_provenance_id` / `sis_a81a34dfa1291e854f5aa725` (GSC, producer_or_observation_brokerage, count=4405): On MARK if needed, trace gsc_provenance_id to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_semantic_channel` / `sis_a6be0cb39e19fd7a877f5789` (GSC, producer_or_observation_brokerage, count=3885): On MARK if needed, trace gsc_semantic_channel to confirm producer/run/sample/source/provenance scope remains attached.
- `gsc_semantic_channel` / `sis_37236d0d4a5a7551bbb08fa0` (GSC, producer_or_observation_brokerage, count=4405): On MARK if needed, trace gsc_semantic_channel to confirm producer/run/sample/source/provenance scope remains attached.

## Tier 1 Verdict

Tier 1 compact artifacts preserve the tested namespace handles and joins. Proceed to Tier 2 MARK deep trace for value-level TEP and SQLite provenance.

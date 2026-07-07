# VAP Coordinate and Feature Registration Specification

## Status

Draft implementation specification for VDB Phase 3 hardening.

This specification defines how VDB registration should preserve VAP package metadata, genomic coordinate declarations, and feature declarations so that later Assertion Record, Evidence Topology, and namespace brokerage workflows can operate on explicit topology-ready substrate.

## 1. Purpose

VAP TEPs contain coordinate-bearing variant evidence and feature/annotation context. VDB Phase 3 registration already preserves conservative source identities such as VAP variant IDs, VAP gene identifiers, and VAP sample identifiers. However, Evidence Topology and future Convergence Geometry require more than compact participant identities.

This specification defines the additional registration substrate required for VAP evidence:

1. package metadata registration,
2. coordinate declaration registration,
3. feature declaration registration.

The goal is preservation and topology readiness, not reinterpretation.

## 2. Governing Workflow

The intended hardening sequence is:

0. Incorporate TEP metadata into Phase 3 registration.
1. Harden Phase 3 registration to emit coordinate identity payloads and feature declaration substrate.
2. Harden Phase 4.3 Assertion Records to preserve coordinate and feature declaration sets by lossless reference.
3. Harden Phase 4.4 Evidence Topology to consume coordinate and feature declaration handles as topology-eligible inputs.
4. Resume Step 8 namespace mediation only after coordinate and feature substrate is explicit and preserved.

This ordering is mandatory. Namespace mediation must not silently compensate for missing coordinate or feature substrate.

## 3. Scope

This specification applies to VAP TEP ingestion and VDB Phase 3 registration.

In scope:

- VAP TEP package metadata at `entities/metadata/config_snapshot.yaml`.
- VAP coordinate-bearing evidence TSV rows.
- VAP feature, consequence, annotation, and gene-mapping fields.
- Phase 3 registration SQLite persistence.
- Phase 4.3 lossless-by-reference preservation requirements.
- Phase 4.4 topology consumption requirements.

Out of scope:

- Canonical variant identity assignment.
- Cross-build coordinate liftover.
- Left-normalization policy beyond preserving VAP-declared state.
- Transcript namespace mediation.
- Regulatory interval canonicalization.
- Gene namespace mediation.
- MyGene.info or other external lookup.
- Clinical reinterpretation.
- RDGP prioritization.
- Convergence Geometry computation.

## 4. Producer-Side Prerequisites

VAP TEPs are expected to include:

```text
entities/metadata/config_snapshot.yaml
```

This artifact is package metadata. It is not a scientific evidence entity and must not be interpreted as a Stage07-Stage13 evidence record.

Expected VAP TEP metadata behavior:

- `entity_inventory.json` indexes `entities/metadata/config_snapshot.yaml` with role `package_metadata` or equivalent metadata classification.
- `lineage_manifest.json` includes the metadata artifact as part of the package topology.
- `validation_report.md` validates metadata artifact presence and transport integrity.
- Existing scientific evidence artifacts remain unchanged.

VDB must treat the config snapshot as authoritative producer execution context for the TEP package.

## 5. Run Identifier Rule

VAP `config_snapshot.yaml` may not explicitly contain the VAP run ID.

For VAP TEP v1 hardening, VDB must derive `run_id` from the TEP directory path when the config does not declare it.

Examples:

```text
vap_tep_HG002_run_2026_06_03_010030_v1
    -> run_2026_06_03_010030

vap_tep_ERR10619330_run_2026_06_01_203130_v1
    -> run_2026_06_01_203130
```

The registration record must preserve the derivation method.

Recommended field:

```text
run_id_derivation_method = tep_directory_name
```

If no run ID can be parsed, VDB must preserve the metadata artifact but mark `run_id_derivation_status = failed`.

## 6. Phase 3 Registration Responsibilities

Phase 3 registration must preserve four substrate classes for VAP TEPs:

1. existing source identities,
2. package metadata context,
3. coordinate declarations,
4. feature declarations.

These products are additive to existing registration artifacts such as:

- `tep_packages`,
- `artifacts`,
- `assertion_registrations`,
- `source_identities`,
- `schema_metadata`.

Registration must remain producer-preserving. It must not collapse coordinates into genes, features into genes, or source identifiers into canonical identifiers.

## 7. Package Metadata Registration

VDB registration must parse and register `entities/metadata/config_snapshot.yaml` when present.

Recommended registration product:

```text
package_metadata
```

An implementation may alternatively store these fields in an existing package metadata payload if the same fields remain queryable and auditable.

### Required Package Metadata Fields

```text
package_metadata_id
registration_unit_id
tep_id
producer_repo
producer_package_type
metadata_role
metadata_artifact_path
metadata_artifact_sha256
metadata_format
run_id
run_id_derivation_method
run_id_derivation_status
sample_id
sample_alias
sra_accession
assay_type
project_name
pipeline_name
pipeline_version
execution_profile_name
hardware_class
reference_genome_build
reference_fasta_path
reference_fasta_index_path
reference_sequence_dictionary_path
annotation_engine
annotation_assembly
annotation_cache_dir
deterministic_mode
record_tool_versions
metadata_parse_status
payload_json
```

### Expected VAP Config Paths

VDB should attempt to extract the following YAML paths when present:

```text
project.name
project.pipeline_name
project.version
input.sample_id
input.sample_alias
input.sra_accession
input.assay_type
execution_profile.name
execution_profile.hardware_class
reference.genome_build
reference.fasta_path
reference.fasta_index
reference.sequence_dictionary
annotation.engine
tools.vep.assembly
tools.vep.cache_dir
runtime.deterministic_mode
runtime.record_tool_versions
```

`reference.fasta_path`, `reference.fasta_index`, and `reference.sequence_dictionary` are producer-environment provenance. They must be preserved but must not be treated as globally portable reference identifiers unless checksums or controlled reference identifiers are later added.

## 8. Coordinate Declaration Registration

VAP variant evidence must be registered as coordinate identity substrate, not only as an opaque participant string.

Recommended registration product:

```text
source_coordinate_declarations
```

A coordinate declaration represents a genomic coordinate-bearing variant identity in producer context.

### Required Coordinate Declaration Fields

```text
coordinate_declaration_id
registration_unit_id
assertion_registration_id
source_identity_id
source_record_ref
source_artifact_path
source_artifact_role
variant_source_namespace
variant_source_value
reference_genome_build
reference_context_source
chromosome
position
start
end
reference_allele
alternate_allele
variant_type
variant_class
coordinate_system
coordinate_system_status
normalization_status
normalization_status_source
sample_id
run_id
producer_pipeline
extraction_method
payload_json
```

### Coordinate Field Sources

VDB should extract row-level coordinate fields from VAP TSV columns when present.

Candidate chromosome columns:

```text
chromosome
chrom
#chromosome
#chrom
contig
```

Candidate position/start columns:

```text
position
pos
start
```

Candidate end columns:

```text
end
stop
```

Candidate reference allele columns:

```text
reference_allele
reference
ref
```

Candidate alternate allele columns:

```text
alternate_allele
alternate
alternative
alt
```

Candidate variant identifier columns:

```text
variant_id
variant_key
variant
```

### Reference Context

For VAP coordinate declarations, `reference_genome_build` must be extracted from package metadata when available, usually from:

```text
reference.genome_build
```

`annotation_assembly` should be extracted from:

```text
tools.vep.assembly
```

The coordinate declaration must preserve:

```text
reference_context_source = entities/metadata/config_snapshot.yaml
```

If row-level coordinates are present but reference context cannot be extracted, VDB must emit a validation finding rather than silently creating an apparently complete coordinate declaration.

### Coordinate System Status

VAP config snapshots may not explicitly declare coordinate convention.

Allowed `coordinate_system_status` values:

```text
declared
inferred
not_observed
```

For VAP TSV evidence, VDB may use `inferred` only when the inference rule is documented in `payload_json`.

Example:

```json
{
  "coordinate_system_status": "inferred",
  "coordinate_system_inference": "VAP TSV fields derived from VCF-style variant representation"
}
```

## 9. Feature Declaration Registration

VAP feature and annotation context must be preserved as declaration substrate. Feature declarations are topology-eligible relationships from coordinate-bearing evidence to annotation values, transcript context, gene context, variant context, or consequence classes.

Feature declarations are not all source identities. Some feature values are entity-like identifiers, while others are relationship labels, annotations, flags, or classification values.

Recommended registration product:

```text
source_feature_declarations
```

### Required Feature Declaration Fields

```text
feature_declaration_id
registration_unit_id
assertion_registration_id
coordinate_declaration_id
source_identity_id
source_record_ref
source_artifact_path
source_artifact_role
variant_source_namespace
variant_source_value
feature_kind
feature_namespace
feature_value
feature_label
relationship_type
relationship_status
gene_id
gene_symbol
gene_mapping_status
transcript_id
consequence
impact
impact_class
functional_impact
variant_context
is_regulatory_candidate
is_splice_region_candidate
annotation_source
annotation_version
annotation_assembly
reference_genome_build
extraction_method
payload_json
```

### Initial Feature Kinds

VDB should initially support the following conservative feature kinds:

```text
gene_overlap
transcript_annotation
sequence_consequence
impact
impact_class
functional_impact
variant_context
regulatory_candidate
splice_region_candidate
gene_mapping_status
annotation_source
annotation_version
```

### Initial Relationship Types

Allowed initial `relationship_type` values:

```text
overlaps_gene
assigned_to_transcript
has_consequence
has_impact
has_impact_class
has_functional_impact
has_variant_context
flagged_as_regulatory_candidate
flagged_as_splice_region_candidate
has_gene_mapping_status
has_annotation_source
has_annotation_version
```

### Candidate Feature Columns

VDB should inspect VAP TSV rows for these columns when present:

```text
gene_id
gene_symbol
gene_mapping_status
transcript_id
consequence
impact
impact_class
functional_impact
variant_context
is_regulatory_candidate
is_splice_region_candidate
annotation_source
annotation_version
```

Missing feature columns must not cause coordinate declaration failure. They should result in absent feature declarations for that row or a scoped validation warning if the artifact role is expected to contain feature annotations.

## 10. Existing Source Identity Compatibility

This specification does not replace existing `source_identities` behavior.

VAP registration should continue to emit source identities such as:

```text
vap_variant_id
vap_constructed_variant_key
vap_ensembl_gene_id
vap_gene_symbol
vap_sample_id
```

Coordinate declarations should link to variant source identities when possible.

Feature declarations should link to coordinate declarations and/or variant source identities when possible.

The intended relationship is:

```text
source_identity
    identifies a participant-like source value

source_coordinate_declaration
    gives coordinate/reference substrate for a variant participant

source_feature_declaration
    gives annotation/feature relationship substrate for a coordinate-bearing variant
```

## 11. Deterministic Identifier Rules

All new registration identifiers must be deterministic and stable across repeated registration of identical TEP packages.

Recommended ID formulas:

```text
package_metadata_id =
    sha256(registration_unit_id | metadata_artifact_path | metadata_artifact_sha256)

coordinate_declaration_id =
    sha256(registration_unit_id | assertion_registration_id | source_record_ref |
           variant_source_namespace | variant_source_value | reference_genome_build |
           chromosome | position | reference_allele | alternate_allele)

feature_declaration_id =
    sha256(registration_unit_id | assertion_registration_id | source_record_ref |
           variant_source_namespace | variant_source_value | feature_kind |
           feature_namespace | feature_value | relationship_type |
           annotation_source | annotation_version)
```

Identifier inputs must not include ingestion timestamp, local machine hostname, nondeterministic row iteration order, or transient runtime state.

If `source_record_ref` is used, it must itself be deterministic for the source artifact.

## 12. Source Artifact and Record References

Coordinate and feature declarations must remain traceable to producer artifacts and source records.

Required trace fields:

```text
registration_unit_id
tep_id
run_id
sample_id
assertion_registration_id
source_artifact_path
source_record_ref
variant_source_namespace
variant_source_value
```

Coordinate declarations must point to the row from which coordinate fields were extracted.

Feature declarations must point to the row from which feature or annotation values were extracted.

When feature declarations are derived from the same row as a coordinate declaration, the feature declaration should reference the coordinate declaration ID when available.

## 13. Assertion Record Preservation Requirements

Phase 4.3 Assertion Records must preserve coordinate and feature declaration substrate by lossless reference. They must not duplicate millions of declarations inline when a compact reference is sufficient.

Recommended future Assertion Record artifacts:

```text
assertion_record_coordinate_declaration_sets.tsv
assertion_record_feature_declaration_sets.tsv
```

A generalized declaration-set artifact is also acceptable if it preserves the same fields.

Required declaration-set fields:

```text
assertion_record_id
assertion_registration_id
declaration_set_id
declaration_table_reference
declaration_filter
declaration_kind
declaration_namespace
declaration_count
declaration_set_status
lossiness_status
```

Required rule:

```text
lossiness_status = lossless_by_reference
```

unless an explicit validation finding explains otherwise.

Assertion Records may summarize declaration counts and routes, but they must preserve enough table reference and filter information for full reconstruction from Phase 3 registration artifacts.

## 14. Evidence Topology Consumption Requirements

Phase 4.4 Evidence Topology must consume coordinate and feature declaration handles as topology-eligible inputs after Phase 4.3 preserves them.

Topology input classes should distinguish:

```text
source_identity_set
coordinate_declaration_set
feature_declaration_set
metadata_context
```

Coordinate and feature declaration handles may contribute to relationship families such as:

```text
same_coordinate_identity
same_reference_build
coordinate_to_gene_context
coordinate_to_transcript_context
coordinate_to_feature_context
shared_consequence_class
shared_impact_class
shared_variant_context
shared_regulatory_candidate_status
shared_splice_region_status
```

Evidence Topology must not claim canonical convergence geometry merely because feature declarations are topology-visible. Geometry remains downstream.

## 15. Namespace Brokerage Implications

Namespace mediation should resume only after coordinate and feature substrate has been registered and preserved through Assertion Records and Evidence Topology.

Coordinate brokerage requires:

```text
reference_genome_build
chromosome
position or interval
reference_allele
alternate_allele
normalization_status
coordinate_system_status
```

Feature brokerage requires:

```text
feature_kind
feature_namespace
feature_value
relationship_type
annotation_source
annotation_version
annotation_assembly
reference_genome_build
```

Gene brokerage remains separate from coordinate and feature brokerage.

Required anti-collapse rules:

1. Coordinates must not be collapsed into genes.
2. Features must not replace coordinates.
3. Gene identity must not become the default identity substrate for variant-derived evidence.
4. Intergenic and no-gene variants must remain coordinate-bearing evidence.
5. Feature declarations must preserve annotation provenance.

## 16. Validation Requirements

Registration validation must include checks for package metadata, coordinate declarations, and feature declarations.

Required checks:

```text
metadata_artifact_present_for_vap_tep
metadata_artifact_parseable
run_id_derivable_from_tep_path_or_metadata
sample_id_extractable
reference_genome_build_extractable_for_coordinate_bearing_vap_tep
annotation_assembly_extractable_or_warned
coordinate_declarations_emitted_for_vap_variant_identities
coordinate_declarations_include_reference_genome_build
coordinate_declarations_are_source_record_traceable
feature_declarations_emitted_for_configured_feature_columns
feature_declarations_are_source_record_traceable
coordinate_declaration_ids_are_deterministic
feature_declaration_ids_are_deterministic
assertion_record_coordinate_declaration_sets_are_lossless_by_reference
assertion_record_feature_declaration_sets_are_lossless_by_reference
evidence_topology_preserves_declaration_set_handles
```

Allowed validation statuses:

```text
passed
passed_with_deferred_resolution
warning_metadata_missing_for_legacy_tep
warning_coordinate_system_inferred
warning_annotation_version_not_observed
warning_feature_column_absent_for_artifact_role
error_reference_build_missing_for_coordinate_declaration
error_coordinate_declaration_untraceable
error_feature_declaration_untraceable
critical_coordinate_identity_collapsed
critical_feature_context_lost
```

## 17. Implementation Notes

Likely implementation areas:

```text
src/variant_database/registration/metadata_extractor.py
src/variant_database/registration/coordinate_extractor.py
src/variant_database/registration/feature_declaration_extractor.py
src/variant_database/registration/registration_orchestrator.py
src/variant_database/persistence/schema_manager.py
```

The existing participant extraction pathway should not be overloaded with all coordinate and feature declaration logic.

Recommended separation:

```text
participant_extractor.py
    participant-like source identities

metadata_extractor.py
    package execution metadata

coordinate_extractor.py
    coordinate identity/reference declarations

feature_declaration_extractor.py
    feature, consequence, annotation, and relationship declarations
```

## 18. Deferred Extensions

The following extensions are intentionally deferred:

```text
reference FASTA checksum support
reference dictionary checksum support
explicit coordinate-system declaration from VAP
VEP version extraction
VEP cache version extraction
transcript namespace mediation
regulatory interval canonicalization
left-normalization policy
multi-allelic decomposition policy
cross-build liftover
full interval overlap
canonical_variant_id generation
canonical_feature_id generation
cross-producer coordinate brokerage
convergence geometry computation
```

Deferred status does not mean these concerns are unnecessary. It means they must not be silently implemented inside Phase 3 registration hardening without explicit governance.

## 19. Summary Rule

VAP-derived evidence must enter VDB with separable coordinate, feature, and gene substrate.

```text
coordinates
    first-class identity substrate tied to reference context

features
    first-class declaration and relationship substrate tied to coordinates

genes
    independently brokered identity substrate, not the default root identity for variants
```

This separation is required so Evidence Topology can organize preserved evidence without premature mediation, and so future Convergence Geometry can emerge from explicit coordinate and feature relationships rather than from gene-centric collapse.

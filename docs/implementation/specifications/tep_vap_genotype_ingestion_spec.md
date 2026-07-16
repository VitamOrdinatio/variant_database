# TEP-VAP Genotype Ingestion Specification

**Status:** implementation specification draft  
**Intended path:** `docs/implementation/specifications/tep_vap_genotype_ingestion_spec.md`  
**Repository:** `variant_database`  
**Audience:** DEX-VDB, SAGE-VDB, future VDB maintainers  
**Scope:** VDB ingestion behavior for genotype-capable TEP-VAP packages  
**Architecture parent:** `docs/architecture/genotype_first_class_vdb_evidence_model.md`  
**Design parent:** `docs/design/genotype_evidence_ingestion_and_brokerage_design.md`  
**Primary brokerage policy:** `docs/design/multiallelic_relationships_vdb_brokerage_policy.md`  
**Primary producer input:** modern genotype-capable TEP-VAP  

---

## 1. Purpose

This specification defines required VDB behavior for ingesting genotype-capable
TEP-VAP packages.

The architecture document defines what must remain true.

The design document defines how genotype evidence should move through VDB.

This specification defines what VDB MUST, SHOULD, MAY, and MUST NOT do during
trusted genotype ingestion.

The central specification doctrine is:

```text
A genotype-capable TEP-VAP package is trusted for VDB genotype ingestion only
when the genotype artifact set is complete, version-supported,
checksum-reconciled, lineage-indexed, validation-passing,
row-count-reconciled, and preservable without producer identity or
relationship-state mutation.
```

---

## 2. Scope

This specification governs:

```text
TEP-VAP genotype capability classification
required genotype artifact discovery
supported genotype artifact versions
execution provenance context registration
genotype observation preservation
identity preservation
relationship partitioning
direct relationship registration
complex relationship preservation
brokerage input requirements
brokerage output requirements
spanning-deletion handling
legacy compatibility behavior
failure and quarantine conditions
required validation receipts
```

This specification does not define:

```text
physical database schemas
SQL DDL
implementation module names
CLI behavior
test function names
RDGP reasoning rules
projection-surface schemas
TEP-VDB package schemas
```

Those belong to downstream schema, validation, contract, implementation-plan,
and code documents.

---

## 3. Normative Language

The terms below are used with the following meanings.

```text
MUST:
    required for trusted genotype ingestion

MUST NOT:
    prohibited for trusted genotype ingestion

SHOULD:
    strongly recommended; deviations require explicit justification

MAY:
    permitted but not required

Trusted ingestion:
    ingestion eligible for normal VDB persistence and downstream use

Quarantine ingestion:
    preservation for diagnostic inspection only; not eligible for normal
    discovery, topology, geometry, or downstream consumer surfaces
```

---

## 3A. Genotype Maturity States

Trusted genotype handling is tiered.

VDB MUST NOT claim a higher genotype maturity state than its validation receipts
support.

Recommended maturity states are:

```text
genotype_discovered

genotype_preservation_validated

genotype_direct_relationships_registered

genotype_complex_relationships_preserved

genotype_brokerage_evaluated

genotype_assertion_ready

genotype_topology_ready

genotype_projection_ready
```

Maturity states are cumulative only when their prerequisite validation receipts
have passed.

A VDB build may be genotype-preserving before it is genotype-brokered.

A VDB build may be genotype-brokered before it is genotype-projection-ready.

The contract document MUST distinguish these states rather than using
`genotype-aware` as an undifferentiated claim.

---

## 4. Authority Sources

This specification derives from the following VDB-side authority stack:

```text
docs/architecture/genotype_first_class_vdb_evidence_model.md

docs/design/genotype_evidence_ingestion_and_brokerage_design.md

docs/design/multiallelic_relationships_vdb_brokerage_policy.md

shared/handoffs/vdb/genotype_first_class/sage_to_dex_genotype_first_class_vdb_handoff.md
```

Producer-side VAP documents define what VAP emits.

They do not define VDB implementation behavior.

RDGP documents define downstream reasoning constraints.

They do not define VDB implementation behavior.

The VDB-specific brokerage policy is the primary relationship-governance
authority for VDB.

---

## 5. Package Classification

VDB MUST classify every TEP-VAP package with respect to genotype capability
before trusted ingestion.

Allowed package-level genotype capability states are:

```text
genotype_capability_available

genotype_capability_unavailable_legacy

genotype_capability_incomplete

genotype_capability_invalid

genotype_capability_unsupported_version
```

### 5.1 `genotype_capability_available`

A package is `genotype_capability_available` only when:

```text
all required genotype artifacts are present

all required genotype artifacts are registered in package governance metadata

required checksums are present

required lineage is discoverable

required schema versions are supported

genotype summary counts reconcile

TEP validation state is discoverable and acceptable
```

### 5.2 `genotype_capability_unavailable_legacy`

A package is `genotype_capability_unavailable_legacy` when:

```text
no genotype artifact set is present

the package predates modern genotype-capable TEP-VAP emission

the package is otherwise valid for variant-only ingestion
```

Legacy unavailability MUST NOT be used when a partial genotype artifact set is
present.

### 5.3 `genotype_capability_incomplete`

A package is `genotype_capability_incomplete` when:

```text
one or more genotype artifacts are present

and

one or more required genotype artifacts are missing
```

Incomplete genotype packages MUST NOT enter trusted genotype ingestion.

They MAY be rejected or quarantined.

### 5.4 `genotype_capability_invalid`

A package is `genotype_capability_invalid` when required genotype artifacts are
present but fail any required integrity, lineage, checksum, count, or validation
condition.

Invalid genotype packages MUST NOT enter trusted genotype ingestion.

They MAY be rejected or quarantined.

### 5.5 `genotype_capability_unsupported_version`

A package is `genotype_capability_unsupported_version` when genotype artifacts
declare schema versions not supported by this specification or by a governed VDB
migration policy.

Unsupported-version genotype artifacts MAY be preserved for audit.

They MUST NOT be registered into active trusted genotype structures without an
explicit governed migration.

---

## 6. Required Input Artifacts

Trusted genotype ingestion requires the canonical genotype artifact set:

```text
entities/genotype/genotype_observations.tsv

entities/genotype/genotype_projection_summary.json

entities/genotype/genotype_source_header_context.json
```

These three artifacts form one atomic genotype producer artifact set.

VDB MUST NOT classify a package as genotype-enabled if only a partial set
exists.

Trusted genotype ingestion also requires the core package governance artifacts:

```text
entity_inventory.json

lineage_manifest.json

validation_report.md
```

Trusted modern genotype-capable TEP-VAP ingestion also requires execution
provenance at:

```text
entities/context/execution_provenance.json
```

For trusted modern genotype ingestion, VDB MUST discover and register execution
provenance as context.

If execution provenance is absent, malformed, or misclassified in a modern
genotype-capable package, VDB MUST fail or quarantine trusted genotype ingestion.

For legacy, compatibility, quarantine, or unsupported-version paths, VDB MAY
represent execution provenance absence explicitly.

VDB MUST NOT fabricate execution provenance.

---

## 7. Supported Versions

Initial supported producer versions are:

```text
genotype_observation_v1

genotype_projection_summary_v1

genotype_source_header_context_v1

genotype_observation_id_v1
```

VDB MUST reject or quarantine unsupported versions unless a governed migration
policy exists.

VDB MUST NOT silently coerce unsupported genotype artifacts into supported
schemas.

VDB MAY preserve unsupported artifacts for audit under an inactive or quarantine
state.

---

## 8. Required Discovery Order

For trusted genotype ingestion, VDB MUST inspect small governance and context
artifacts before streaming or bulk-ingesting `genotype_observations.tsv`.

Required discovery order:

```text
1. validation_report.md

2. entity_inventory.json

3. lineage_manifest.json

4. entities/genotype/genotype_projection_summary.json

5. entities/genotype/genotype_source_header_context.json

6. entities/context/execution_provenance.json

7. entities/genotype/genotype_observations.tsv
```

For legacy, compatibility, quarantine, or unsupported-version paths,
execution_provenance.json absence may be represented explicitly.

This order prevents VDB from deriving package truth directly from a large table
before establishing the package contract.

---

## 9. Genotype Artifact-Set Validation

Before trusted genotype ingestion, VDB MUST verify:

```text
all three genotype artifacts are present

all three genotype artifacts have discoverable transport paths

all three genotype artifacts have discoverable checksums

all three genotype artifacts are represented in entity inventory or equivalent
package governance metadata

the genotype lineage branch is represented in lineage manifest

the genotype projection summary is parseable

the source-header context is parseable

the genotype observation table header is readable

the genotype observation table row count reconciles with genotype summary

canonical genotype artifact checksums reconcile for trusted modern genotype
ingestion

declared checksums reconcile for all package-governance artifacts where package
metadata provides checksums

checksum absence is represented explicitly only for legacy, compatibility,
quarantine, or unsupported-version paths
```

Failure of any required genotype artifact-set condition MUST prevent trusted
genotype ingestion.

---

## 10. Execution Provenance Registration Requirements

When present, VDB MUST register:

```text
entities/context/execution_provenance.json
```

as execution context.

Execution provenance registration MUST preserve:

```text
source artifact path

source artifact checksum

toolchain context

annotation environment context

resource environment context

reference-resource identity

contract status

provenance completeness status
```

Execution provenance MUST NOT be registered as:

```text
variant evidence

genotype evidence

pathogenicity evidence

phenotype evidence

reasoning evidence
```

Execution provenance MAY support later method-currency and comparability
surfaces.

---

## 11. Genotype Observation Preservation Requirements

VDB MUST preserve every emitted genotype observation row without mutating
producer values.

VDB MUST preserve all columns emitted in `genotype_observations.tsv`, including
columns not used by the first-pass ingestion implementation.

VDB MUST preserve all producer-emitted genotype columns either as typed/indexed
columns or as a raw source-row extension representation sufficient to
reconstruct the producer-emitted row.

Raw producer value preservation and VDB-normalized convenience values are
distinct.

VDB MUST NOT replace raw producer values with normalized convenience values.

Required preservation classes include:

```text
schema fields

producer identity fields

sample and run fields

source VCF identity fields

source VCF header identity fields

source record ordinal / line / hash fields

reference build fields

coordinate and allele fields

normalization state fields

relationship status / reason / target fields

variant_id and variant_observation_id fields when emitted

raw FORMAT and sample FORMAT fields

GT / AD / DP / GQ / PL / FT fields where emitted

unknown FORMAT fields where emitted

GT parsing fields

called allele index fields

missingness and no-call fields

genotype call-state fields

depth and quality convenience fields

site and sample filter fields

record parse status fields

record preservation status fields

projection advisory and warning fields
```

VDB MAY create internal persistence identifiers.

VDB MAY create canonical identities.

VDB MAY create derived relationship identifiers.

VDB MUST NOT replace or rewrite `genotype_observation_id`.

---

## 12. Identity Preservation Requirements

Trusted genotype ingestion MUST preserve the following producer identities when
emitted:

```text
genotype_observation_id

genotype_observation_id_version

sample_id

sample_alias

sra_accession

run_id

vcf_sample_column_name

sample_selection_policy

sample_identity_mapping_status

source_pipeline

assay_type

source_vcf_path

source_vcf_sha256

source_vcf_header_hash

source_record_ordinal

source_line_number

source_record_hash

reference_build
```

VDB MUST preserve the ability to reconstruct:

```text
which source package transported the observation

which source VCF record produced the observation

which selected sample column supplied the genotype

which VAP sample and run identities were assigned

which reference-build context applied
```

If any required producer identity is absent for a modern genotype-enabled
package, trusted genotype ingestion MUST fail or quarantine unless a documented
compatibility policy permits the absence.

---

## 13. Count Reconciliation Requirements

VDB MUST reconcile genotype summary counts against the observed genotype table.

Required reconciliations include:

```text
genotype_observation_row_count
    == observed data row count in genotype_observations.tsv
```

When the projection summary provides source-record count:

```text
source_record_count
    == genotype_observation_row_count
```

Relationship partition counts MUST reconcile:

```text
direct_relationship_count
+ complex_relationship_count
+ unresolved_relationship_count
+ not_applicable_relationship_count
    == genotype_observation_row_count
```

If a summary omits one of the relationship partition counts, VDB MUST compute
the observed count from the genotype table and record that the count was
computed rather than producer-summarized.

Count mismatch MUST prevent trusted genotype ingestion unless an explicit,
documented compatibility policy exists.

---

## 14. Relationship Partitioning Requirements

VDB MUST partition genotype observations using producer relationship fields.

Primary fields:

```text
variant_relationship_status

relationship_reason

relationship_resolution_target

variant_id

variant_observation_id

alternate_alleles_raw

alternate_allele_count

called_allele_indices

source_record_hash
```

Recognized primary relationship status values are:

```text
direct

complex

unresolved

not_applicable
```

VDB MUST preserve unrecognized values as source-emitted values.

For unrecognized values, VDB MUST NOT perform trusted direct or derived
relationship registration unless a governed compatibility policy exists.

Relationship partitioning MUST NOT mutate the registered genotype observation.

---

## 15. Direct Relationship Registration Requirements

A row is eligible for direct relationship registration when all of the following
conditions hold:

```text
variant_relationship_status = direct

relationship_resolution_target = none

variant_id is populated

genotype_observation_id is populated

source_record_hash is populated
```

For direct rows, VDB MUST:

```text
preserve the source genotype observation

register a direct producer-declared genotype-to-variant relationship

record relationship state as direct_source_biallelic or equivalent

preserve producer relationship status

preserve producer relationship reason

preserve producer relationship resolution target

preserve source traceability
```

VDB MUST keep direct producer relationships distinguishable from VDB-derived
relationships.

Direct relationship registration MUST NOT imply:

```text
inheritance mode

carrier status

compound heterozygosity

de novo status

disease causality

diagnosis
```

---

## 16. Complex Relationship Preservation Requirements

A row requires complex relationship preservation when:

```text
variant_relationship_status = complex
```

or when producer fields otherwise indicate that VDB brokerage is required.

For complex rows, VDB MUST:

```text
preserve the source genotype observation

preserve producer relationship status

preserve relationship reason

preserve relationship resolution target

preserve source record identity

preserve source ALT order

preserve called allele indices

preserve raw GT / AD / DP / GQ / PL / FORMAT fields where emitted

preserve advisory and warning codes

route the row to brokerage input or explicit not-evaluated state
```

VDB MUST NOT treat a blank, missing, or sentinel `variant_id` on a complex row
as a genotype preservation failure when the row is explicitly delegated to VDB
brokerage.

VDB MUST NOT silently promote complex rows to direct source relationships.

VDB MUST NOT represent complex rows as missing genotype evidence.

---

## 17. Brokerage Input Requirements

A genotype observation is eligible for brokerage evaluation only if VDB can
recover enough source context to evaluate the relationship under a declared VDB
brokerage policy.

Minimum brokerage input fields SHOULD include:

```text
genotype_observation_id

sample_id

run_id

source package identity

reference_build

chromosome

position

reference_allele

alternate_alleles_raw

alternate_allele_count

called_allele_indices

variant_relationship_status

relationship_reason

relationship_resolution_target

source_vcf_sha256

source_vcf_header_hash

source_record_ordinal

source_record_hash

gt_raw

ad_raw

dp_raw

gq_raw

pl_raw

format_raw

sample_format_raw

record_parse_status

record_preservation_status
```

If required brokerage input is unavailable, VDB MUST preserve the genotype
observation and emit an explicit unresolved or not-evaluated relationship state.

Missing brokerage prerequisites MUST NOT cause deletion of the source genotype
observation.

---

## 18. Brokerage Output Requirements

For each brokerage-required genotype observation, VDB MUST record an explicit
brokerage outcome.

Allowed high-level brokerage outcomes include:

```text
brokerage_not_evaluated

brokerage_resolved

brokerage_ambiguous

brokerage_unresolved

brokerage_policy_unavailable
```

When constructing derived genotype-to-variant relationships, VDB MUST preserve:

```text
genotype_observation_id

source_record_hash

allele_index when applicable

source_alt_allele when applicable

variant identity or sample-specific variant observation identity when resolved

relationship derivation policy

normalization policy when used

relationship state

ambiguity state

lossiness state

identity registration state

traceability references
```

VDB-derived relationships MUST remain distinguishable from direct
producer-declared relationships.

A single `genotype_observation_id` MAY map to zero, one, or multiple
VDB-derived relationship identifiers.

Multiple VDB-derived relationship identifiers MUST NOT imply multiple producer
genotype observations.

---

## 19. Required Relationship States

VDB SHOULD use relationship states that distinguish direct, derived,
normalized, ambiguous, unresolved, and not-evaluated cases.

Recommended relationship states include:

```text
direct_source_biallelic

resolved_from_multiallelic_record

brokered_with_normalization

resolved_from_split_normalized_record

ambiguous_requires_review

unresolved_missing_variant_identity

unresolved_symbolic_alt

unresolved_spanning_deletion

spanning_deletion_context_required

unresolved_malformed_gt

unresolved_allele_index_out_of_range

unresolved_normalization_ambiguous

unresolved_policy_not_available

not_evaluated
```

VDB MUST NOT collapse:

```text
resolved_from_multiallelic_record
```

into:

```text
direct_source_biallelic
```

even when the derived relationship is unambiguous and usable.

---

## 20. Spanning-Deletion Requirements

When a genotype observation involves a spanning-deletion allele such as:

```text
ALT = *
```

VDB MUST preserve the source genotype observation and source relationship state.

Unless a declared spanning-deletion resolution policy exists, VDB MUST NOT treat
the `*` allele as an ordinary SNV or small-indel alternate allele.

Allowed conservative states include:

```text
spanning_deletion_context_required

unresolved_spanning_deletion
```

Spanning-deletion unresolved state MUST NOT be treated as:

```text
missing genotype evidence

variant absence

evidence loss

direct biallelic linkage
```

---

## 21. FORMAT and Depth Preservation Requirements

VDB MUST preserve raw FORMAT and sample FORMAT values.

VDB MUST preserve record-level vector fields as record-level evidence.

For allele-index-derived annotations, VDB MUST cite:

```text
source genotype observation

source record hash

source vector field

source vector index

allele index

source ALT allele
```

VDB MUST NOT represent allele-specific depth annotations as independent
producer AD vectors.

Example prohibited claim:

```text
A>C has independent producer AD = 2,4
```

Safe relationship annotation:

```text
allele index 1 maps to source ALT C and AD[1] = 4 under allele-index mapping
policy
```

---

## 22. Legacy Compatibility Requirements

For packages classified as:

```text
genotype_capability_unavailable_legacy
```

VDB MAY proceed with variant-only trusted ingestion if all non-genotype
package requirements pass.

VDB MUST explicitly label legacy mode using states such as:

```text
variant_only_legacy_compatibility_mode

genotype_context_unavailable

genotype_not_emitted_by_source

genotype_projection_not_evaluated
```

VDB MUST NOT infer genotype from legacy variant-only packages.

Legacy absence of genotype artifacts MUST NOT be interpreted as:

```text
homozygous reference

variant absence

no-call

callability

opportunity evidence

negative disease evidence

inheritance-readiness support
```

---

## 23. Failure and Quarantine Conditions

Trusted genotype ingestion MUST fail or quarantine when any of the following
conditions occur:

```text
partial genotype artifact set

missing required genotype artifact

malformed genotype projection summary

malformed genotype source-header context

malformed entity inventory required for genotype discovery

malformed lineage manifest required for genotype discovery

missing genotype lineage branch

checksum mismatch

row-count mismatch

unsupported genotype artifact version

missing required genotype_observation_id

duplicate genotype_observation_id with conflicting producer content

source VCF identity unrecoverable

source VCF header identity unrecoverable

source record identity unrecoverable

required producer validation state unavailable or failing

inability to preserve full genotype observation row

attempted mutation of producer genotype observation

attempted complex-to-direct silent promotion

attempted synthetic producer genotype row creation

attempted inheritance interpretation during ingestion
```

Quarantined genotype packages or rows MUST NOT enter:

```text
normal discovery surfaces

trusted Assertion Records

trusted Evidence Topology

geometry surfaces

TEP-VDB consumer surfaces

RDGP-facing exports
```

unless and until the quarantine condition is resolved under governed policy.

---

## 24. Required Validation Receipts

A trusted genotype ingestion run MUST emit or record validation receipts
covering at minimum:

```text
package genotype capability classification

genotype artifact-set completeness

supported schema-version status

entity inventory reconciliation

lineage manifest reconciliation

TEP validation status capture

genotype projection summary reconciliation

source-header context registration

execution provenance registration status when present

genotype row-count reconciliation

genotype column preservation

genotype_observation_id uniqueness

source VCF identity preservation

source VCF header identity preservation

source record identity preservation

sample / run / reference-build coherence

relationship partition counts

direct relationship registration count

complex relationship preservation count

brokerage input count

brokerage attempted count

brokerage resolved count

brokerage ambiguous count

brokerage unresolved count

brokerage not-evaluated count

spanning-deletion conservative state count

producer observation split count

inheritance assertion count emitted by VDB ingestion
```

The expected value for producer observation split count is:

```text
0
```

The expected value for inheritance assertion count emitted by VDB ingestion is:

```text
0
```

Any nonzero value MUST fail trusted genotype ingestion.

---

## 25. Non-Goals

This specification does not define:

```text
physical table names

SQL column definitions

SQLite / SQLAlchemy implementation details

streaming parser implementation

command-line interfaces

test file names

projection surface schemas

RDGP reasoning behavior

clinical interpretation behavior

full symbolic ALT resolution

final spanning-deletion resolution
```

This specification also does not replace:

```text
docs/design/multiallelic_relationships_vdb_brokerage_policy.md
```

That policy remains authoritative for VDB relationship brokerage doctrine.

---

## 26. Success Criteria

This specification is satisfied when VDB can demonstrate that a modern
genotype-capable TEP-VAP package is ingested only if:

```text
1. The genotype artifact set is complete.

2. Required versions are supported.

3. Required package governance artifacts are readable.

4. TEP validation state is discoverable and acceptable.

5. Genotype artifacts are registered in package governance metadata.

6. Genotype lineage is discoverable.

7. Genotype summary counts reconcile with observed rows.

8. All genotype observation columns are preserved.

9. genotype_observation_id values are preserved and unique.

10. Source VCF, source header, source record, sample, run, and reference-build
    identities remain recoverable.

11. Direct producer relationships are registered as direct and remain distinct
    from VDB-derived relationships.

12. Complex relationships remain explicit and are routed to brokerage or
    not-evaluated states.

13. Multiallelic-derived relationships do not create producer genotype rows.

14. Spanning-deletion relationships are preserved conservatively unless a
    declared resolution policy exists.

15. Execution provenance is registered as context, not biological evidence.

16. Legacy variant-only packages remain usable without inferred genotype.

17. No inheritance interpretation is emitted during genotype ingestion.
```

---

## 27. Relationship to Schema, Validation, Contract, and Plan

This specification governs required behavior.

The downstream schema document should define:

```text
how genotype observations, relationship inputs, relationship outputs, receipts,
and topology substrates are represented.
```

The downstream validation document should define:

```text
how VDB proves the requirements in this specification were satisfied.
```

The downstream contract should define:

```text
what VDB guarantees to downstream consumers after successful genotype ingestion.
```

The downstream implementation plan should define:

```text
the code and test sequence for implementing this specification.
```

---

## 28. Final Doctrine

Trusted genotype ingestion is valid only when VDB preserves the complete
producer genotype observation substrate and records relationship state without
collapsing producer evidence into derived topology or downstream reasoning.

VDB may register direct producer relationships.

VDB may construct additive derived relationships under declared brokerage
policy.

VDB must preserve complex, ambiguous, unresolved, not-evaluated, and legacy
states explicitly.

VDB must not infer inheritance.

The boundary remains:

```text
VAP preserves.

VDB brokers.

RDGP reasons.
```

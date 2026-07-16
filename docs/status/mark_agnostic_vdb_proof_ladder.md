# MARK-Agnostic VDB Proof Ladder

**Status:** strategic execution plan  
**Intended path:** `docs/status/mark_agnostic_vdb_proof_ladder.md`  
**Scope:** VAP → TEP-VAP → VDB → TEP-VDB → RDGP stepping-stone strategy  
**Primary execution substrate:** local sys76 node  
**Secondary / optional substrate:** MARK, if access returns  
**Last updated:** 2026-07-15  

---

## 1. Purpose

This document defines a MARK-agnostic execution strategy for proving VDB using
local sys76 resources.

The immediate goal is to avoid dependency on MARK access while continuing to
advance:

```text
FASTQ
    → VAP
        → genotype-aware TEP-VAP
            → VDB
                → TEP-VDB
                    → RDGP
                        → TEP-RDGP
                            → VDB re-ingestion
```

The strategy uses progressively larger corpora to prove functionality,
scalability, telemetry, statistical resolution, and future publication
readiness.

The near-term portfolio goal is to prove the system through small and moderate
corpora that are scientifically honest, computationally tractable, and useful
for job-facing demonstrations.

The long-term research goal is to build toward a complete BioProject-scale
analysis using all available WES epilepsy SRAs from PRJEB57558.

---

## 2. Strategic Premise

MARK access is currently unreliable.

Therefore:

```text
sys76 becomes the primary development, execution, and proof substrate.

MARK becomes an optional accelerator or later reproduction environment,
not a dependency.
```

This requires the VDB proof ladder to be:

```text
local-first
telemetry-gated
corpus-scaled
storage-aware
resumable
certification-driven
```

The guiding principle is:

```text
Do not wait for infrastructure that cannot be controlled.
```

---

## 3. Current Technical Direction

DEX-VAP is elevating genotype into TEP-VAP.

The current local genotype-aware calibration run is:

```text
ERR10619300
```

This run is being executed locally on sys76 from FASTQ through VAP and is
expected to produce a genotype-aware TEP-VAP.

Once SAGE-VAP certifies the genotype-elevated TEP-VAP implementation,
DEX-VDB will inspect the new TEP-VAP structure and adjust VDB ingestion so that
genotype becomes a first-class VDB substrate beside:

```text
metadata
genomic coordinates
features
source identity
assertion records
evidence topology
```

For the current genotype integration wave:

```text
metadata:
    preserve existing TEP-VAP behavior

coordinates:
    preserve existing VDB-compatible extraction / declaration behavior

features:
    preserve existing VDB-compatible extraction / declaration behavior

genotype:
    add explicit first-class TEP-VAP transport and VDB ingestion
```

---

## 4. Proof Ladder Overview

The proposed proof ladder is:

```text
Gate 1:
    1 WES TEP-VAP + 2 TEP-GSC
    interface / genotype / TEP-VDB proof

Gate 2:
    5 TEP corpus
    3 WES TEP-VAP + 2 TEP-GSC
    small disease-substrate proof

Gate 3:
    14 TEP corpus
    12 WES TEP-VAP + 2 TEP-GSC
    full planned epilepsy WES disease-corpus proof

Gate 4:
    3 TEP WGS stress corpus
    HG002 WGS TEP-VAP + 2 TEP-GSC
    WGS stress / continuity proof

Gate 5:
    146 TEP corpus
    144 WES TEP-VAP + 2 TEP-GSC
    long-term BioProject-scale research / publication target
```

The first four gates are portfolio-relevant stepping stones.

The fifth gate is a future research target.

---

## 5. Corpus Definitions

### 5.1 Gate 1 — 1-WES + 2-GSC Interface Proof

```text
1 WES TEP-VAP:
    ERR10619300

2 TEP-GSC:
    epilepsy semantic prior
    mitochondrial disease semantic prior
```

Purpose:

```text
prove genotype-aware TEP-VAP ingestion

prove VAP + GSC mixed-producer registration

prove genotype as first-class VDB substrate

prove VDB can proceed from ingestion through TEP-VDB emission

prove all planned projection surfaces on a minimal mixed-producer corpus

This gate is not intended to make disease-cohort statistical claims.
```

---

### 5.2 Gate 2 — 5-TEP Local Disease-Substrate Proof

```text
3 WES TEP-VAP:
    ERR10619212    q1
    ERR10619300    median
    ERR10619225    q3

2 TEP-GSC:
    epilepsy semantic prior
    mitochondrial disease semantic prior
```

Purpose:

```text
prove small disease-corpus execution locally

test q1 / median / q3 WES diversity

exercise genotype-aware VDB ingestion across multiple VAP TEPs

exercise VAP + GSC integration

exercise projection-surface emission on a small but nontrivial corpus

generate early RDGP-ready TEP-VDB substrate
```

Scientific interpretation boundary:

```text
5-TEP may prove architecture and execution.

5-TEP must not be treated as a strong burden, recurrence, or disease-association
result.
```

---

### 5.3 Gate 3 — 14-TEP Full Planned WES Disease Corpus

```text
12 WES TEP-VAP:
    complete planned epilepsy WES subset

2 TEP-GSC:
    epilepsy semantic prior
    mitochondrial disease semantic prior
```

Purpose:

```text
prove the planned full WES disease-corpus strategy

evaluate VDB scaling over all 12 local or regenerated epilepsy WES TEP-VAPs

produce stronger CFBS / MPLC / EVRS / RFPS substrates

produce the primary portfolio-ready disease-corpus TEP-VDB

provide a stronger RDGP input substrate than 5-TEP
```

This corpus is likely beyond the minimum portfolio requirement, but it is highly
valuable if sys76 telemetry shows that local execution is tractable.

---

### 5.4 Gate 4 — 3-TEP HG002 WGS Stress / Continuity Corpus

```text
1 WGS TEP-VAP:
    HG002

2 TEP-GSC:
    epilepsy semantic prior
    mitochondrial disease semantic prior
```

Purpose:

```text
stress-test VDB with a WGS-scale VAP TEP

preserve continuity from earlier HG002 work

demonstrate FASTQ → VAP → VDB → TEP-VDB behavior on a reference specimen

optionally provide RDGP with an HG002 continuity substrate
```

Interpretation boundary:

```text
HG002 is a stress and continuity specimen.

HG002 is not the epilepsy disease-corpus proof.
```

This gate should occur after 14-TEP WES proof, not before, because WGS may
distort runtime, storage, and implementation priorities.

---

### 5.5 Gate 5 — 146-TEP BioProject-Scale Research Corpus

```text
144 WES TEP-VAP:
    complete PRJEB57558 WES SRA corpus

2 TEP-GSC:
    epilepsy semantic prior
    mitochondrial disease semantic prior
```

Purpose:

```text
future research-scale analysis

publication-oriented cohort-scale VDB proof

larger statistical-resolution substrate for CFBS, MPLC, EVRS, RFPS, and RDGP

long-term demonstration that the VAP → VDB → RDGP architecture can scale beyond
portfolio proof
```

This corpus is not required for near-term portfolio completion.

It is a long-term research target.

---

## 6. Explicit Execution Workflow

The planned workflow is:

```text
1. DEX-VAP completes genotype-elevated VAP implementation.

2. SAGE-VAP certifies genotype-elevated TEP-VAP output.

3. DEX-VDB inspects the new ERR10619300 genotype-aware TEP-VAP state.

4. DEX-VDB adjusts VDB ingestion so genotype becomes a first-class substrate.

5. DEX-VDB smoke-tests VDB against:
       1 WES TEP-VAP: ERR10619300
       2 TEP-GSCs: epilepsy + mitochondrial disease

6. If the smoke test clears through VDB Developmental Phase 4.4 step 8,
   DEX-VDB resumes VDB code development.

7. DEX-VDB continues implementation through:
       projection surfaces
       TEP-VDB emission
       three-layer validation methodology

8. SAGE-VDB certifies the emitted TEP-VDB.

9. DEX-VDB executes the 5-TEP corpus:
       3 WES + 2 GSC

10. SAGE-VDB certifies 5-TEP receipts.

11. DEX-VDB executes the 14-TEP corpus:
       12 WES + 2 GSC

12. SAGE-VDB certifies 14-TEP receipts.

13. DEX-VDB executes the HG002 WGS 3-TEP stress corpus:
       1 WGS + 2 GSC

14. SAGE-VDB certifies WGS 3-TEP stress receipts.

15. VDB case studies are wrapped.

16. RDGP begins from certified TEP-VDBs, especially:
       5-TEP TEP-VDB
       14-TEP TEP-VDB
       optional HG002 3-TEP TEP-VDB

17. RDGP eventually emits TEP-RDGP back to VDB.

18. DEX-VDB ingests TEP-RDGP as a new reasoning-assertion producer corpus.
```

---

## 7. Developmental Phase Position

The immediate VDB target after genotype ingestion is to restore and extend VDB
through the existing developmental ladder:

```text
Phase 4.1:
    source identity / package substrate

Phase 4.2:
    coordinate / feature / metadata declaration substrate

Phase 4.3:
    assertion records

Phase 4.4:
    evidence topology

Phase 4.5:
    convergence geometry

Phase 4.6:
    evidence convergence surfaces

Phase 4.7:
    projection / consumer surfaces

TEP-VDB:
    reason-ready transport package
```

Genotype must be caught up to metadata, coordinates, and features through this
pipeline.

At minimum, genotype-aware VDB should support:

```text
source_genotype_observations

assertion_record_genotype_declaration_sets

topology genotype declaration members

CUES genotype uncertainty events

OACS genotype / no-call / opportunity context where applicable

RMCS genotype dependency / parser / policy currency

GIRS projection surface
```

---

## 8. Telemetry as a Formal Gate

Telemetry is required because sys76 is now the primary execution substrate.

Each corpus scale should produce telemetry sufficient to answer:

```text
How long did this corpus take?

How much storage did it require?

How much did the database grow?

Which tables dominated row counts?

Which phase was the bottleneck?

Did runtime scale linearly, sublinearly, or pathologically?

Can we extrapolate from 1-TEP to 5-TEP, 14-TEP, and 146-TEP?
```

Telemetry makes the 146-TEP target thinkable even if it is not immediately
executed.

---

## 9. Recommended Telemetry Fields

Each VDB execution should record at least:

```text
execution_id
corpus_id
corpus_label
tep_count
vap_tep_count
gsc_tep_count
wes_tep_count
wgs_tep_count
start_time
end_time
elapsed_seconds
host
execution_mode
git_commit
python_version
sqlite_version
free_disk_before
free_disk_after
database_size_before
database_size_after
peak_temp_dir_size when available
phase_name
phase_start_time
phase_end_time
phase_elapsed_seconds
row_counts_by_table
insert_rate_by_table when available
index_build_time when available
validation_elapsed_seconds
warning_count
error_count
largest_artifact_paths
validation_status
certification_status
```

For VAP regeneration telemetry, each WES/WGS run should record:

```text
sra_id
run_id
assay_type
fastq_size_r1
fastq_size_r2
alignment_start_time
alignment_end_time
vap_total_elapsed_seconds
tep_size
processed_vcf_size
run_directory_size
genotype_observation_count
genotype_relationship_state_counts
validation_status
certification_status
```

---

## 10. Critical VDB Row Counts

VDB should report row counts for key substrates at each scale:

```text
registration_units
source_identities
package_metadata
source_coordinate_declarations
source_feature_declarations
source_genotype_observations
assertion_records
assertion_record_source_identity_sets
assertion_record_coordinate_declaration_sets
assertion_record_feature_declaration_sets
assertion_record_genotype_declaration_sets
topology_relationships
topology_members
topology_basis
projection_surface_rows_by_surface
tep_vdb_manifest_rows
```

These counts should be recorded for:

```text
1-WES + 2-GSC
5-TEP
14-TEP
HG002 3-TEP
eventual 146-TEP
```

---

## 11. Comparative Scaling Questions

The telemetry should answer practical scaling questions:

```text
Does VDB runtime scale roughly linearly with WES TEP count?

Does feature declaration expansion dominate storage?

Does genotype observation volume materially change runtime?

Does topology expansion grow linearly or superlinearly?

Do projection surfaces introduce new bottlenecks?

Does the 5-TEP corpus predict 14-TEP behavior?

Can 14-TEP behavior support a credible extrapolation to 146-TEP?

Which artifacts must be archived or pruned between runs?

Which tables require indexing or batching improvements?
```

---

## 12. Comparative Statistical Resolution Across Corpora

Different corpora offer different statistical and reasoning resolution.

### 1-WES + 2-GSC

```text
Resolution:
    interface and integration only

Useful for:
    genotype ingestion
    mixed-producer substrate proof
    TEP-VDB emission proof

Not useful for:
    burden inference
    recurrence inference
    disease-corpus claims
```

### 5-TEP

```text
Resolution:
    small corpus behavior

Useful for:
    q1 / median / q3 WES diversity
    early projection-surface validation
    RDGP interface demonstration

Limited for:
    CFBS statistical claims
    MPLC burden contrast
    EVRS recurrence
```

### 14-TEP

```text
Resolution:
    planned full WES disease-corpus behavior

Useful for:
    stronger recurrence substrate
    stronger burden substrate
    stronger prior-locus contrast substrate
    primary portfolio-grade disease-corpus demonstration

Still limited for:
    publication-scale statistical power
    robust rare-variant association claims
```

### 3-TEP HG002 WGS

```text
Resolution:
    WGS stress and continuity

Useful for:
    WGS-scale stress testing
    reference specimen continuity
    FASTQ → VAP → VDB → RDGP demonstration

Not useful for:
    epilepsy disease-corpus inference
```

### 146-TEP

```text
Resolution:
    future BioProject-scale research substrate

Useful for:
    improved recurrence resolution
    improved burden contrast
    more credible CFBS / MPLC empirical-null behavior
    stronger RDGP reasoning substrate
    publication-oriented cohort-scale analysis

Still requires:
    careful opportunity modeling
    statistical caution
    SAGE review
    independent validation
```

---

## 13. Portfolio Versus Research Targets

The near-term portfolio target is not to execute every possible corpus.

The near-term portfolio target is to demonstrate:

```text
genotype-aware VAP output

VDB genotype-aware ingestion

VDB mixed-producer integration

TEP-VDB projection-surface architecture

RDGP-ready transport

traceability, validation, and anti-overclaim governance
```

The minimum portfolio-useful stepping stones are:

```text
1-WES + 2-GSC

5-TEP

HG002 WGS 3-TEP stress / continuity
```

The stronger portfolio target is:

```text
14-TEP
```

The long-term research target is:

```text
146-TEP
```

The strategic value of the ladder is that every near-term portfolio step also
builds toward the future research path.

---

## 14. Storage and Run-Folder Policy

For local sys76 execution, VAP run folders should be managed carefully.

Before pruning any VAP run:

```text
1. certify the TEP-VAP
2. back up the complete run folder to external storage
3. verify backup integrity
4. retain active local files needed for VDB ingestion and debugging
```

The ideal VDB handoff unit is:

```text
results/run_<id>/tep/
```

Before VDB genotype ingestion is fully proven, active local storage should also
retain:

```text
processed/*.vcf
metadata/
validation/
reports/
logs/
```

After VDB genotype ingestion is proven and the TEP-VAP is certified, the active
local minimum can eventually shrink toward:

```text
tep/
```

while complete run backups remain on external storage.

---

## 15. Gate Criteria

### Gate 1 Exit Criteria

```text
ERR10619300 genotype-aware TEP-VAP certified

VDB consumes genotype-aware TEP-VAP

VDB consumes 2 TEP-GSCs

VDB clears through Phase 4.4 step 8

metadata / coordinate / feature behavior remains stable

genotype declaration path is validated
```

### Gate 2 Exit Criteria

```text
3 WES + 2 GSC corpus executes locally

5-TEP receipts are complete

TEP-VDB is emitted

SAGE-VDB certifies 5-TEP receipts

telemetry supports or refines 14-TEP feasibility
```

### Gate 3 Exit Criteria

```text
12 WES + 2 GSC corpus executes locally

14-TEP receipts are complete

TEP-VDB is emitted

SAGE-VDB certifies 14-TEP receipts

telemetry supports or refines 146-TEP extrapolation
```

### Gate 4 Exit Criteria

```text
HG002 WGS + 2 GSC stress corpus executes

WGS-scale receipts are complete

SAGE-VDB certifies WGS stress receipts

HG002 continuity case study is ready
```

### Gate 5 Entry Criteria

```text
14-TEP telemetry suggests 146-TEP may be tractable

storage strategy is defined

batch execution strategy is defined

long-running process resilience is validated

statistical analysis plan is reviewed by SAGE

146-TEP is explicitly treated as research/publication scope, not portfolio
minimum scope
```

---

## 16. Risk Register

### Risk: sys76 storage exhaustion

Mitigation:

```text
external-drive backups
post-certification pruning
phase-level disk telemetry
avoid parallel VAP WES runs unless proven safe
```

### Risk: VDB SQLite/database expansion

Mitigation:

```text
batched writes
index timing telemetry
row-count telemetry
intermediate 5-TEP and 14-TEP dry runs
```

### Risk: feature declaration explosion

Mitigation:

```text
monitor source_feature_declarations
monitor topology member growth
preserve declaration-set references rather than duplicating rows
```

### Risk: genotype representation drift

Mitigation:

```text
inspect genotype-aware TEP-VAP before VDB code changes
derive VDB genotype ingestion from emitted TEP-VAP substrate
preserve multiallelic and genotype-to-variant relationship states
```

### Risk: premature statistical overclaim

Mitigation:

```text
use anti-overclaim labels
separate execution proof from scientific inference
require SAGE certification
treat 5-TEP as architecture proof, not association proof
```

### Risk: MARK dependency returns implicitly

Mitigation:

```text
treat MARK as optional
keep sys76 as primary proof substrate
maintain local execution receipts
```

---

## 17. Strategic Summary

This plan turns local sys76 execution into a controlled proof ladder:

```text
1-WES + 2-GSC
    → prove interface and genotype-aware ingestion

5-TEP
    → prove small local disease-substrate execution

14-TEP
    → prove planned WES disease corpus

HG002 WGS 3-TEP
    → prove WGS stress and continuity

146-TEP
    → future BioProject-scale research target
```

The plan supports near-term portfolio outcomes while preserving a future path
toward publication-scale research.

The guiding doctrine is:

```text
Build the portfolio stepping stones now.

Collect telemetry that makes the research-scale path calculable later.
```

The long-term value of the strategy is not only that VDB may run locally.

The value is that every corpus scale becomes both:

```text
a validation artifact

and

a scaling measurement
```

That lets VDB grow from a portfolio-grade architecture proof into a future
research-grade cohort analysis platform without depending on unreliable MARK
access.

MARK independence converts fixture generation from an external scheduling
problem into a local storage, telemetry, and validation-management problem.

The architectural consequence:

```text
Golden fixtures are no longer rare artifacts.

They can become a managed fixture ladder:
    tiny synthetic fixtures
    1-WES real fixtures
    5-TEP corpus fixtures
    14-TEP corpus fixtures
    WGS stress fixtures
```
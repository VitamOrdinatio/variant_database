#!/usr/bin/env python3
"""
Deep read-only Tier 2 namespace provenance recon for MARK.

Run from the MARK VDB repo root:
    ~/dev/portfolio_projects/variant_database

The script inspects MARK-side VAP TEP artifacts and VDB registration SQLite
files, then writes audit receipts under:
    results/phase4/namespace_audit/mark_phase4_corpus_6tep_v1_tep2vdb_audit_v1/deep_recon/

Safety boundaries:
- No mutation of VAP TEP directories.
- No mutation of VDB registration SQLite files.
- SQLite databases are opened read-only with mode=ro and PRAGMA query_only=ON.
- No external network calls.
- No identifier mediation or canonical identity creation.
- Outputs are written only under the configured audit output directory.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    csv.field_size_limit(sys.maxsize)
except OverflowError:
    csv.field_size_limit(2**31 - 1)

CORPUS_ID = "mark_phase4_corpus_6tep_v1"
AUDIT_ID = f"{CORPUS_ID}_tep2vdb_audit_v1"
DEFAULT_OUT_DIR = Path("results/phase4/namespace_audit") / AUDIT_ID / "deep_recon"
DEFAULT_VAP_ROOT = Path.home() / "dev/portfolio_projects/variant_annotation_pipeline"

OFFICIAL_VAP_RUNS = [
    {"sra_id": "ERR10619203", "run_id": "run_2026_05_30_071639", "depth_category": "q3", "subject_label": "ERR10619203", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619207", "run_id": "run_2026_06_01_124134", "depth_category": "q3", "subject_label": "ERR10619207", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619208", "run_id": "run_2026_05_30_151355", "depth_category": "median", "subject_label": "ERR10619208", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619212", "run_id": "run_2026_05_30_214724", "depth_category": "q1", "subject_label": "ERR10619212", "in_current_6tep_corpus": True, "registration_dir": "vap_q1_ERR10619212"},
    {"sra_id": "ERR10619225", "run_id": "run_2026_05_31_091242", "depth_category": "q3", "subject_label": "ERR10619225", "in_current_6tep_corpus": True, "registration_dir": "vap_q3_ERR10619225"},
    {"sra_id": "ERR10619230", "run_id": "run_2026_06_01_004903", "depth_category": "q3", "subject_label": "ERR10619230", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619241", "run_id": "run_2026_06_02_052302", "depth_category": "q1", "subject_label": "ERR10619241", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619281", "run_id": "run_2026_05_27_233524", "depth_category": "median", "subject_label": "ERR10619281", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619285", "run_id": "run_2026_06_02_124300", "depth_category": "median", "subject_label": "ERR10619285", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619300", "run_id": "run_2026_05_27_172531", "depth_category": "median", "subject_label": "ERR10619300", "in_current_6tep_corpus": True, "registration_dir": "vap_median_ERR10619300"},
    {"sra_id": "ERR10619309", "run_id": "run_2026_06_02_181024", "depth_category": "q1", "subject_label": "ERR10619309", "in_current_6tep_corpus": False},
    {"sra_id": "ERR10619330", "run_id": "run_2026_06_01_203130", "depth_category": "q1", "subject_label": "ERR10619330", "in_current_6tep_corpus": False},
    {"sra_id": "SRR12898354", "run_id": "run_2026_06_03_010030", "depth_category": "hg002", "subject_label": "HG002", "in_current_6tep_corpus": True, "registration_dir": "vap_hg002"},
]

CANONICAL_SQLITE_REGISTRATIONS = [
    {"db_key": "mark_phase3_canonical_vap_hg002", "producer": "VAP", "registration_dir": "vap_hg002", "sqlite_path": "results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite", "in_current_6tep_corpus": True},
    {"db_key": "mark_phase3_canonical_vap_median_ERR10619300", "producer": "VAP", "registration_dir": "vap_median_ERR10619300", "sqlite_path": "results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite", "in_current_6tep_corpus": True},
    {"db_key": "mark_phase3_canonical_vap_q1_ERR10619212", "producer": "VAP", "registration_dir": "vap_q1_ERR10619212", "sqlite_path": "results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite", "in_current_6tep_corpus": True},
    {"db_key": "mark_phase3_canonical_vap_q3_ERR10619225", "producer": "VAP", "registration_dir": "vap_q3_ERR10619225", "sqlite_path": "results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite", "in_current_6tep_corpus": True},
    {"db_key": "mark_phase3_canonical_gsc_epilepsy", "producer": "GSC", "registration_dir": "gsc_epilepsy", "sqlite_path": "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite", "in_current_6tep_corpus": True},
    {"db_key": "mark_phase3_canonical_gsc_mitochondrial_disease", "producer": "GSC", "registration_dir": "gsc_mitochondrial_disease", "sqlite_path": "results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite", "in_current_6tep_corpus": True},
]

LEGACY_CONTEXT_SQLITE_REGISTRATIONS = [
    {"db_key": "legacy_gsc_epilepsy", "producer": "GSC", "registration_dir": "gsc/epilepsy", "sqlite_path": "results/registration/gsc/epilepsy/vdb.sqlite", "in_current_6tep_corpus": False},
    {"db_key": "legacy_gsc_mitochondrial_disease", "producer": "GSC", "registration_dir": "gsc/mitochondrial_disease", "sqlite_path": "results/registration/gsc/mitochondrial_disease/vdb.sqlite", "in_current_6tep_corpus": False},
]

VAP_TEP_TSV_RELATIVE_PATHS = [
    ("observation", "entities/observation/*.annotated_variants.tsv"),
    ("normalization_vdb_ready", "entities/normalization/stage_08_vdb_ready_variants.tsv"),
    ("normalization_selected_transcript_consequences", "entities/normalization/stage_08_selected_transcript_consequences.tsv"),
    ("coding_interpretation", "entities/coding_interpretation/stage_09_coding_interpreted.tsv"),
    ("noncoding_interpretation", "entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv"),
    ("routing_coding", "entities/routing/coding_candidates.tsv"),
    ("routing_noncoding", "entities/routing/noncoding_candidates.tsv"),
    ("routing_splice_region", "entities/routing/splice_region_candidates.tsv"),
    ("prioritization", "entities/prioritization/stage_11_prioritized_variants.tsv"),
    ("validation", "entities/validation/stage_12_validation_candidates.tsv"),
]

METADATA_RELATIVE_PATHS = [
    "entity_inventory.json",
    "lineage_manifest.json",
    "validation_report.md",
    "entities/context/stage_13_artifact_manifest.json",
    "entities/context/stage_13_final_summary.json",
    "entities/context/stage_13_run_report.md",
]

REFERENCE_TERMS = [
    "reference_build", "genome_build", "assembly", "GRCh38", "GRCh37", "hg38", "hg19",
    "fasta_path", "fasta_index", "sequence_dictionary", "bwa_index_prefix", "primary_assembly",
    "vep", "VEP", "annotation_source", "annotation_version", "cache_version", "reference",
]

COORDINATE_COLS = [
    "variant_id", "chromosome", "chrom", "contig", "position", "pos", "start", "end",
    "reference_allele", "ref", "alternate_allele", "alt", "variant_type", "variant_class",
    "variant_context", "variant_effect_severity", "normalization_status",
]
GENE_COLS = [
    "gene_id", "ensembl_gene_id", "gene_symbol", "gene", "symbol", "gene_mapping_status",
    "hgnc_id", "entrezgene", "source_gene_id",
]
FEATURE_COLS = [
    "transcript_id", "feature", "feature_type", "consequence", "impact", "impact_class",
    "functional_impact", "is_regulatory_candidate", "biotype", "exon", "intron", "hgvsc",
    "hgvsp", "coding_change", "protein_change", "distance_to_gene",
]
PRODUCER_COLS = [
    "sample_id", "run_id", "source_pipeline", "annotation_source", "annotation_version",
    "source_interpretation_label", "source_file", "producer", "sra_id",
]

ESSENTIAL_COORD_SYNONYMS = {
    "chromosome": ["chromosome", "chrom", "contig"],
    "position": ["position", "pos", "start"],
    "reference_allele": ["reference_allele", "ref"],
    "alternate_allele": ["alternate_allele", "alt"],
}

STANDARD_SENTINEL_COLUMNS = [
    "variant_id", "chromosome", "chrom", "contig", "position", "pos", "start", "end",
    "reference_allele", "ref", "alternate_allele", "alt", "variant_type", "variant_class",
    "variant_context", "gene_id", "ensembl_gene_id", "gene_symbol", "gene_mapping_status",
    "transcript_id", "consequence", "impact", "impact_class", "functional_impact",
    "is_regulatory_candidate", "annotation_source", "annotation_version", "sample_id", "run_id", "source_pipeline",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def s(value: Any) -> str:
    return "" if value is None else str(value)


def nonempty(value: Any) -> bool:
    return bool(s(value).strip())


def intish(value: Any) -> int:
    try:
        return int(str(value or "").strip())
    except (TypeError, ValueError):
        return 0


def truncate(value: Any, limit: int = 600) -> str:
    text = s(value).replace("\n", " ").replace("\r", " ")
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames or []), rows


def read_header(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            first = handle.readline().rstrip("\n\r")
        if not first:
            return []
        return first.split("\t")
    except OSError:
        return []


def lower_field_map(fields: Iterable[str]) -> dict[str, str]:
    return {field.lower(): field for field in fields}


def matching_columns(fields: Iterable[str], wanted: Iterable[str]) -> list[str]:
    fmap = lower_field_map(fields)
    hits = []
    for wanted_col in wanted:
        if wanted_col.lower() in fmap:
            hits.append(fmap[wanted_col.lower()])
    return hits


def get_any(row: dict[str, str], names: Iterable[str]) -> str:
    fmap = {k.lower(): k for k in row.keys()}
    for name in names:
        key = fmap.get(name.lower())
        if key is not None and nonempty(row.get(key)):
            return s(row.get(key))
    return ""


def has_any(row: dict[str, str], names: Iterable[str]) -> bool:
    return nonempty(get_any(row, names))


def coordinate_complete(row: dict[str, str]) -> bool:
    return all(nonempty(get_any(row, candidates)) for candidates in ESSENTIAL_COORD_SYNONYMS.values())


def find_tep_dir(vap_root: Path, run: dict[str, Any]) -> Path:
    return vap_root / "results" / run["run_id"] / "tep" / f"vap_tep_{run['subject_label']}_{run['run_id']}_v1"


def find_tsv_artifacts(tep_dir: Path) -> list[tuple[str, Path]]:
    artifacts: list[tuple[str, Path]] = []
    for role, pattern in VAP_TEP_TSV_RELATIVE_PATHS:
        for path in sorted(tep_dir.glob(pattern)):
            artifacts.append((role, path))
    return artifacts


def text_hits(path: Path, terms: list[str], max_bytes: int = 5_000_000) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    try:
        text = path.read_bytes()[:max_bytes].decode("utf-8", errors="replace")
    except OSError:
        return hits
    for idx, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()
        for term in terms:
            if term.lower() in lower:
                hits.append({"file_path": str(path), "line_number": idx, "term": term, "line_excerpt": truncate(line, 500)})
                break
    return hits


def discover_config_files(vap_root: Path, run: dict[str, Any], max_files: int = 200) -> list[Path]:
    candidates: list[Path] = []
    seen: set[Path] = set()
    search_roots = [vap_root, vap_root / "config", vap_root / "configs", vap_root / "results" / run["run_id"]]
    patterns = ["*.yaml", "*.yml", "config*.yaml", "config*.yml", "**/config*.yaml", "**/config*.yml"]
    for root in search_roots:
        if not root.exists():
            continue
        for pattern in patterns:
            try:
                for path in root.glob(pattern):
                    if not path.is_file():
                        continue
                    resolved = path.resolve()
                    if resolved in seen:
                        continue
                    name_text = str(path).lower()
                    if (
                        run["run_id"].lower() in name_text
                        or run["sra_id"].lower() in name_text
                        or run["subject_label"].lower() in name_text
                        or path.parent in {vap_root, vap_root / "config", vap_root / "configs"}
                    ):
                        seen.add(resolved)
                        candidates.append(path)
                        if len(candidates) >= max_files:
                            return candidates
            except OSError:
                continue
    return candidates


def inventory_vap_teps(vap_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run in OFFICIAL_VAP_RUNS:
        tep_dir = find_tep_dir(vap_root, run)
        metadata_present = [rel for rel in METADATA_RELATIVE_PATHS if (tep_dir / rel).exists()]
        tsv_artifacts = find_tsv_artifacts(tep_dir) if tep_dir.exists() else []
        rows.append({
            "sra_id": run["sra_id"], "run_id": run["run_id"], "subject_label": run["subject_label"],
            "depth_category": run["depth_category"], "in_current_6tep_corpus": str(bool(run.get("in_current_6tep_corpus"))).lower(),
            "registration_dir": run.get("registration_dir", ""), "expected_tep_dir": str(tep_dir),
            "tep_dir_exists": str(tep_dir.exists()).lower(), "metadata_artifact_count": len(metadata_present),
            "metadata_artifacts_present": ";".join(metadata_present), "tsv_artifact_count": len(tsv_artifacts),
            "audit_status": "present" if tep_dir.exists() else "missing",
        })
    return rows


def scan_vap_reference_context(vap_root: Path, current_only: bool = True) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    metadata_hits: list[dict[str, Any]] = []
    config_hits: list[dict[str, Any]] = []
    for run in OFFICIAL_VAP_RUNS:
        if current_only and not run.get("in_current_6tep_corpus"):
            continue
        tep_dir = find_tep_dir(vap_root, run)
        for rel in METADATA_RELATIVE_PATHS:
            path = tep_dir / rel
            if path.exists():
                for hit in text_hits(path, REFERENCE_TERMS):
                    metadata_hits.append({"sra_id": run["sra_id"], "run_id": run["run_id"], "subject_label": run["subject_label"], "depth_category": run["depth_category"], "metadata_role": rel, **hit})
        for cfg in discover_config_files(vap_root, run):
            for hit in text_hits(cfg, REFERENCE_TERMS):
                config_hits.append({"sra_id": run["sra_id"], "run_id": run["run_id"], "subject_label": run["subject_label"], "depth_category": run["depth_category"], "config_path": str(cfg), "line_number": hit["line_number"], "term": hit["term"], "line_excerpt": hit["line_excerpt"]})
    return metadata_hits, config_hits


def classify_sentinel(row: dict[str, str], artifact_role: str) -> list[str]:
    classes: list[str] = []
    role = artifact_role.lower()
    consequence = get_any(row, ["consequence"]).lower()
    impact = get_any(row, ["impact", "impact_class", "functional_impact"]).lower()
    gene_status = get_any(row, ["gene_mapping_status"]).lower()
    gene_present = has_any(row, ["gene_id", "ensembl_gene_id", "gene_symbol", "gene"])
    regulatory = get_any(row, ["is_regulatory_candidate"]).lower()
    if "splice" in role or "splice" in consequence:
        classes.append("splice_region_candidate")
    if "coding" in role or any(tok in consequence for tok in ["coding", "missense", "frameshift", "stop_gained", "stop_lost", "synonymous", "protein", "exon"]) or any(tok in impact for tok in ["high", "moderate"]):
        if gene_present or consequence:
            classes.append("coding_or_gene_overlap")
    if "noncoding" in role or any(tok in consequence for tok in ["intron", "utr", "upstream", "downstream", "regulatory", "non_coding", "noncoding"]) or regulatory in {"true", "1", "yes"}:
        if gene_present or consequence or regulatory:
            classes.append("noncoding_gene_or_feature_associated")
    if any(tok in consequence for tok in ["intergenic", "no_gene", "unmapped", "none", "not_mapped"]) or any(tok in gene_status for tok in ["intergenic", "no_gene", "unmapped", "none", "not_mapped"]) or not gene_present:
        classes.append("intergenic_or_no_gene_assigned")
    if coordinate_complete(row):
        classes.append("coordinate_complete")
    if not classes:
        classes.append("unclassified_but_observed")
    return list(dict.fromkeys(classes))


def scan_vap_tsv_artifact(run: dict[str, Any], artifact_role: str, path: Path, sentinel_limit: int, max_rows: int, progress_every: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fields = read_header(path)
    coord_cols = matching_columns(fields, COORDINATE_COLS)
    gene_cols = matching_columns(fields, GENE_COLS)
    feature_cols = matching_columns(fields, FEATURE_COLS)
    producer_cols = matching_columns(fields, PRODUCER_COLS)
    summary: dict[str, Any] = {
        "sra_id": run["sra_id"], "run_id": run["run_id"], "subject_label": run["subject_label"], "depth_category": run["depth_category"],
        "artifact_role": artifact_role, "artifact_path": str(path), "exists": str(path.exists()).lower(), "size_bytes": path.stat().st_size if path.exists() else 0,
        "column_count": len(fields), "coordinate_columns": ";".join(coord_cols), "gene_columns": ";".join(gene_cols), "feature_columns": ";".join(feature_cols), "producer_columns": ";".join(producer_cols),
        "row_count_scanned": 0, "coordinate_complete_rows": 0, "gene_annotated_rows": 0, "feature_context_rows": 0, "intergenic_or_no_gene_rows": 0,
        "scan_status": "not_started", "gene_mapping_status_counts": "{}", "consequence_counts": "{}", "variant_class_counts": "{}", "impact_counts": "{}",
    }
    sentinels: list[dict[str, Any]] = []
    sentinel_counts: Counter[str] = Counter()
    gene_mapping_status_counts: Counter[str] = Counter()
    consequence_counts: Counter[str] = Counter()
    variant_class_counts: Counter[str] = Counter()
    impact_counts: Counter[str] = Counter()
    if not path.exists():
        summary["scan_status"] = "missing"
        return summary, sentinels
    if not fields:
        summary["scan_status"] = "missing_or_unreadable_header"
        return summary, sentinels
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for idx, row in enumerate(reader, start=1):
                if max_rows and idx > max_rows:
                    break
                if progress_every and idx % progress_every == 0:
                    print(f"  scanned {idx:,} rows: {path}", flush=True)
                if coordinate_complete(row):
                    summary["coordinate_complete_rows"] += 1
                if has_any(row, ["gene_id", "ensembl_gene_id", "gene_symbol", "gene"]):
                    summary["gene_annotated_rows"] += 1
                if has_any(row, FEATURE_COLS):
                    summary["feature_context_rows"] += 1
                classes = classify_sentinel(row, artifact_role)
                if "intergenic_or_no_gene_assigned" in classes:
                    summary["intergenic_or_no_gene_rows"] += 1
                for key, names, counter in [
                    ("gm", ["gene_mapping_status"], gene_mapping_status_counts),
                    ("cons", ["consequence"], consequence_counts),
                    ("vc", ["variant_class", "variant_type", "variant_context"], variant_class_counts),
                    ("imp", ["impact", "impact_class", "functional_impact"], impact_counts),
                ]:
                    val = get_any(row, names)
                    if val:
                        counter[val] += 1
                for cls in classes:
                    if sentinel_counts[cls] < sentinel_limit:
                        sentinel_counts[cls] += 1
                        sentinel_row: dict[str, Any] = {"sra_id": run["sra_id"], "run_id": run["run_id"], "subject_label": run["subject_label"], "depth_category": run["depth_category"], "artifact_role": artifact_role, "artifact_path": str(path), "row_number": idx, "sentinel_class": cls, "coordinate_complete": str(coordinate_complete(row)).lower()}
                        for col in STANDARD_SENTINEL_COLUMNS:
                            sentinel_row[col] = get_any(row, [col])
                        sentinels.append(sentinel_row)
                summary["row_count_scanned"] = idx
        summary["scan_status"] = "completed_full_scan" if not max_rows or summary["row_count_scanned"] < max_rows else f"completed_limited_scan_{max_rows}"
    except Exception as exc:
        summary["scan_status"] = f"error:{type(exc).__name__}:{exc}"
    summary["gene_mapping_status_counts"] = json.dumps(dict(gene_mapping_status_counts.most_common(30)), sort_keys=True)
    summary["consequence_counts"] = json.dumps(dict(consequence_counts.most_common(30)), sort_keys=True)
    summary["variant_class_counts"] = json.dumps(dict(variant_class_counts.most_common(30)), sort_keys=True)
    summary["impact_counts"] = json.dumps(dict(impact_counts.most_common(30)), sort_keys=True)
    return summary, sentinels


def scan_current_vap_tsvs(vap_root: Path, sentinel_limit: int, max_rows: int, progress_every: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summaries: list[dict[str, Any]] = []
    sentinels: list[dict[str, Any]] = []
    for run in OFFICIAL_VAP_RUNS:
        if not run.get("in_current_6tep_corpus"):
            continue
        tep_dir = find_tep_dir(vap_root, run)
        if not tep_dir.exists():
            continue
        for artifact_role, path in find_tsv_artifacts(tep_dir):
            print(f"Scanning VAP TEP TSV: {run['sra_id']} {artifact_role} {path}", flush=True)
            summary, rows = scan_vap_tsv_artifact(run, artifact_role, path, sentinel_limit, max_rows, progress_every)
            summaries.append(summary)
            sentinels.extend(rows)
    return summaries, sentinels


def sqlite_connect_readonly(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=ON")
    return conn


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def sqlite_table_names(conn: sqlite3.Connection) -> list[str]:
    return [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]


def sqlite_columns(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(f"PRAGMA table_info({qident(table)})")]


def inspect_sqlite_databases(vdb_root: Path, include_legacy: bool, sample_limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    database_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    group_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    assertion_sample_rows: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    registrations = list(CANONICAL_SQLITE_REGISTRATIONS)
    if include_legacy:
        registrations.extend(LEGACY_CONTEXT_SQLITE_REGISTRATIONS)
    for reg in registrations:
        sqlite_path = vdb_root / reg["sqlite_path"]
        db_row = {"db_key": reg["db_key"], "producer": reg["producer"], "registration_dir": reg["registration_dir"], "sqlite_path": str(sqlite_path), "in_current_6tep_corpus": str(bool(reg["in_current_6tep_corpus"])).lower(), "exists": str(sqlite_path.exists()).lower(), "size_bytes": sqlite_path.stat().st_size if sqlite_path.exists() else 0, "read_status": "not_started", "table_count": 0, "tables": ""}
        if not sqlite_path.exists():
            db_row["read_status"] = "missing"
            database_rows.append(db_row)
            findings.append(finding("sqlite_database_missing", "error", f"SQLite database missing: {sqlite_path}", reg["db_key"], "phase3_registration", "registration_output"))
            continue
        try:
            print(f"Inspecting SQLite read-only: {sqlite_path}", flush=True)
            conn = sqlite_connect_readonly(sqlite_path)
            try:
                tables = sqlite_table_names(conn)
                db_row["read_status"] = "opened_readonly"
                db_row["table_count"] = len(tables)
                db_row["tables"] = ";".join(tables)
                for table in tables:
                    cols = sqlite_columns(conn, table)
                    col_names = [c["name"] for c in cols]
                    schema_rows.append({"db_key": reg["db_key"], "producer": reg["producer"], "table_name": table, "column_count": len(col_names), "columns": ";".join(col_names), "coordinate_columns": ";".join(matching_columns(col_names, COORDINATE_COLS)), "gene_columns": ";".join(matching_columns(col_names, GENE_COLS)), "feature_columns": ";".join(matching_columns(col_names, FEATURE_COLS)), "producer_columns": ";".join(matching_columns(col_names, PRODUCER_COLS))})
                if "source_identities" in tables:
                    group_rows.extend(sqlite_source_identity_groups(conn, reg))
                    sample_rows.extend(sqlite_source_identity_samples(conn, reg, sample_limit))
                else:
                    findings.append(finding("source_identities_table_missing", "critical", "source_identities table missing from canonical registration DB.", reg["db_key"], "phase3_registration", "registration_schema"))
                if "assertion_registrations" in tables:
                    assertion_sample_rows.extend(sqlite_assertion_registration_samples(conn, reg, sample_limit))
                else:
                    findings.append(finding("assertion_registrations_table_missing", "error", "assertion_registrations table missing from registration DB.", reg["db_key"], "phase3_registration", "registration_schema"))
            finally:
                conn.close()
        except Exception as exc:
            db_row["read_status"] = f"error:{type(exc).__name__}:{exc}"
            findings.append(finding("sqlite_open_or_inspect_error", "error", db_row["read_status"], reg["db_key"], "phase3_registration", "sqlite_probe"))
        database_rows.append(db_row)
    return database_rows, schema_rows, group_rows, sample_rows, assertion_sample_rows, findings


def sqlite_source_identity_groups(conn: sqlite3.Connection, reg: dict[str, Any]) -> list[dict[str, Any]]:
    cols = [row["name"] for row in sqlite_columns(conn, "source_identities")]
    required = ["assertion_registration_id", "identity_kind", "participant_role", "source_namespace"]
    if not all(col in cols for col in required):
        return [{"db_key": reg["db_key"], "producer": reg["producer"], "assertion_registration_id": "", "identity_kind": "", "participant_role": "", "source_namespace": "", "sqlite_source_identity_count": "", "query_status": "missing_required_group_columns:" + ";".join(c for c in required if c not in cols)}]
    sql = "SELECT assertion_registration_id, identity_kind, participant_role, source_namespace, COUNT(*) AS n FROM source_identities GROUP BY assertion_registration_id, identity_kind, participant_role, source_namespace ORDER BY assertion_registration_id, identity_kind, participant_role, source_namespace"
    rows: list[dict[str, Any]] = []
    print(f"  Aggregating source_identities groups for {reg['db_key']}", flush=True)
    for row in conn.execute(sql):
        rows.append({"db_key": reg["db_key"], "producer": reg["producer"], "assertion_registration_id": row["assertion_registration_id"], "identity_kind": row["identity_kind"], "participant_role": row["participant_role"], "source_namespace": row["source_namespace"], "sqlite_source_identity_count": row["n"], "query_status": "completed"})
    return rows


def sqlite_source_identity_samples(conn: sqlite3.Connection, reg: dict[str, Any], sample_limit: int) -> list[dict[str, Any]]:
    cols = [row["name"] for row in sqlite_columns(conn, "source_identities")]
    if "source_namespace" not in cols:
        return []
    namespaces = [row[0] for row in conn.execute("SELECT DISTINCT source_namespace FROM source_identities ORDER BY source_namespace")]
    wanted_cols = [c for c in ["source_identity_id", "assertion_registration_id", "identity_kind", "participant_role", "source_namespace", "source_value", "source_label", "extraction_method", "source_record_ref", "payload_json"] if c in cols]
    rows: list[dict[str, Any]] = []
    for ns in namespaces:
        sql = f"SELECT {', '.join(qident(c) for c in wanted_cols)} FROM source_identities WHERE source_namespace = ? LIMIT ?"
        for idx, row in enumerate(conn.execute(sql, (ns, sample_limit)), start=1):
            out = {"db_key": reg["db_key"], "producer": reg["producer"], "sample_rank": idx}
            for c in wanted_cols:
                out[c] = truncate(row[c], 700)
            rows.append(out)
    return rows


def sqlite_assertion_registration_samples(conn: sqlite3.Connection, reg: dict[str, Any], sample_limit: int) -> list[dict[str, Any]]:
    cols = [row["name"] for row in sqlite_columns(conn, "assertion_registrations")]
    wanted_cols = [c for c in ["assertion_registration_id", "assertion_type", "subject_id", "subject_namespace", "predicate", "object_id", "object_namespace", "participant_summary_json", "support_ref_json", "source_record_ref", "payload_json"] if c in cols]
    if not wanted_cols:
        return []
    sql = f"SELECT {', '.join(qident(c) for c in wanted_cols)} FROM assertion_registrations LIMIT ?"
    rows: list[dict[str, Any]] = []
    for idx, row in enumerate(conn.execute(sql, (sample_limit,)), start=1):
        out = {"db_key": reg["db_key"], "producer": reg["producer"], "sample_rank": idx}
        for c in wanted_cols:
            out[c] = truncate(row[c], 900)
        out["reference_term_hits"] = ";".join(term for term in REFERENCE_TERMS if any(term.lower() in s(row[c]).lower() for c in wanted_cols))
        rows.append(out)
    return rows


def parse_source_identity_filter(text: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    if not text:
        return parts
    for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*'?([^;'\s]+)'?", text):
        parts[match.group(1)] = match.group(2)
    return parts


def db_key_from_source_identity_table_reference(ref: str) -> tuple[str, str]:
    if ":" in ref:
        db_key, table = ref.split(":", 1)
        return db_key, table
    return ref, ""


def trace_compact_sis_to_sqlite(vdb_root: Path, sqlite_group_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ar_path = vdb_root / "results/phase4/assertion_records" / CORPUS_ID / "assertion_record_source_identity_sets.tsv"
    _fields, sis_rows = read_tsv(ar_path)
    group_counts: dict[tuple[str, str, str, str, str], int] = {}
    for row in sqlite_group_rows:
        if row.get("query_status") != "completed":
            continue
        key = (row.get("db_key", ""), row.get("assertion_registration_id", ""), row.get("identity_kind", ""), row.get("participant_role", ""), row.get("source_namespace", ""))
        group_counts[key] = intish(row.get("sqlite_source_identity_count"))
    traces: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    if not sis_rows:
        findings.append(finding("compact_source_identity_sets_missing", "critical", f"Missing compact Source Identity Sets: {ar_path}", "compact_vdb", "phase4_3_assertion_records", "assertion_record_source_identity_sets"))
        return traces, findings
    for sis in sis_rows:
        db_key, table = db_key_from_source_identity_table_reference(sis.get("source_identity_table_reference", ""))
        parsed_filter = parse_source_identity_filter(sis.get("source_identity_filter", ""))
        assertion_registration_id = sis.get("source_assertion_registration_id") or parsed_filter.get("assertion_registration_id", "")
        identity_kind = sis.get("identity_kind") or parsed_filter.get("identity_kind", "")
        participant_role = sis.get("participant_role") or parsed_filter.get("participant_role", "")
        source_namespace = sis.get("source_namespace") or parsed_filter.get("source_namespace", "")
        key = (db_key, assertion_registration_id, identity_kind, participant_role, source_namespace)
        expected = intish(sis.get("source_identity_count"))
        observed = group_counts.get(key)
        if observed is None:
            status = "critical_source_identity_untraceable"
            findings.append(finding("compact_sis_not_found_in_sqlite_groups", "critical", f"Compact Source Identity Set did not match SQLite source_identities group: {sis.get('source_identity_set_id')}", sis.get("source_identity_set_id", ""), "phase3_registration", "source_identities_group_trace"))
        elif observed == expected:
            status = "passed_value_substrate_group_count_matches"
        else:
            status = "error_sqlite_count_mismatch"
            findings.append(finding("compact_sis_sqlite_count_mismatch", "error", f"Expected {expected} source identities but SQLite group count was {observed}: {sis.get('source_identity_set_id')}", sis.get("source_identity_set_id", ""), "phase3_registration", "source_identities_group_trace"))
        traces.append({"source_identity_set_id": sis.get("source_identity_set_id", ""), "db_key": db_key, "table_name": table, "assertion_id": sis.get("assertion_id", ""), "source_assertion_registration_id": assertion_registration_id, "identity_kind": identity_kind, "participant_role": participant_role, "source_namespace": source_namespace, "source_identity_count_expected": expected, "sqlite_source_identity_count_observed": "" if observed is None else observed, "source_identity_filter": sis.get("source_identity_filter", ""), "trace_status": status})
    return traces, findings


def finding(check_id: str, status: str, message: str, subject: str, earliest_gap_stage: str, recommended_fix_layer: str) -> dict[str, Any]:
    return {"check_id": check_id, "status": status, "message": message, "subject": subject, "earliest_gap_stage": earliest_gap_stage, "recommended_fix_layer": recommended_fix_layer}


def derive_findings(vap_inventory: list[dict[str, Any]], metadata_hits: list[dict[str, Any]], config_hits: list[dict[str, Any]], tsv_summaries: list[dict[str, Any]], sis_traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for row in [r for r in vap_inventory if r.get("in_current_6tep_corpus") == "true" and r.get("tep_dir_exists") != "true"]:
        findings.append(finding("current_vap_tep_missing", "critical", f"Current-corpus VAP TEP missing: {row['expected_tep_dir']}", row["sra_id"], "producer_tep_arrival", "tep_availability"))
    metadata_has_build = any("grch38" in s(r.get("line_excerpt")).lower() or "genome_build" in s(r.get("line_excerpt")).lower() or "assembly" in s(r.get("line_excerpt")).lower() for r in metadata_hits)
    config_has_build = any("grch38" in s(r.get("line_excerpt")).lower() or "genome_build" in s(r.get("line_excerpt")).lower() or "assembly" in s(r.get("line_excerpt")).lower() for r in config_hits)
    if metadata_has_build:
        findings.append(finding("reference_context_preserved_in_tep_metadata", "passed", "Reference/assembly context was observed in VAP TEP metadata artifacts.", "VAP", "producer_tep_arrival", "none"))
    elif config_has_build:
        findings.append(finding("reference_context_external_config_only", "warning", "Reference/assembly context was observed in VAP invocation config files but not in probed TEP metadata artifacts.", "VAP", "producer_tep_arrival", "tep_metadata_reference_context"))
    else:
        findings.append(finding("reference_context_unobserved", "error", "Reference/assembly context was not observed in VAP TEP metadata or discovered config files.", "VAP", "producer_tep_arrival", "tep_metadata_reference_context"))
    current_summaries = [r for r in tsv_summaries if r.get("exists") == "true"]
    coordinate_files = [r for r in current_summaries if nonempty(r.get("coordinate_columns"))]
    if coordinate_files and sum(intish(r.get("coordinate_complete_rows")) for r in coordinate_files) > 0:
        findings.append(finding("vap_coordinate_substrate_present", "passed", "VAP TEP TSVs expose coordinate-bearing rows.", "VAP", "producer_tep_arrival", "none"))
    else:
        findings.append(finding("vap_coordinate_substrate_missing", "critical", "No coordinate-complete rows were observed in current VAP TEP TSV scans.", "VAP", "producer_tep_arrival", "vap_tep_coordinate_substrate"))
    feature_files = [r for r in current_summaries if nonempty(r.get("feature_columns"))]
    if feature_files and sum(intish(r.get("feature_context_rows")) for r in feature_files) > 0:
        findings.append(finding("vap_feature_substrate_present", "passed", "VAP TEP TSVs expose feature/consequence/annotation context.", "VAP", "producer_tep_arrival", "none"))
    else:
        findings.append(finding("vap_feature_substrate_unobserved", "warning", "Feature/consequence substrate was not observed in current VAP TEP TSV scans.", "VAP", "producer_tep_arrival", "vap_tep_feature_substrate"))
    if sum(intish(r.get("intergenic_or_no_gene_rows")) for r in current_summaries) > 0:
        findings.append(finding("vap_intergenic_or_no_gene_coordinate_evidence_observed", "passed", "VAP TEP scans observed intergenic/no-gene-assigned coordinate evidence.", "VAP", "producer_tep_arrival", "none"))
    else:
        findings.append(finding("vap_intergenic_or_no_gene_not_observed", "warning", "No intergenic/no-gene-assigned evidence was observed by the scan heuristics.", "VAP", "producer_tep_arrival", "sentinel_classification"))
    bad_traces = [r for r in sis_traces if not s(r.get("trace_status", "")).startswith("passed")]
    if bad_traces:
        findings.append(finding("compact_to_sqlite_trace_incomplete", "critical", f"{len(bad_traces)} compact Source Identity Sets did not trace cleanly to SQLite group counts.", "compact_sis", "phase3_registration", "source_identities_group_trace"))
    elif sis_traces:
        findings.append(finding("compact_to_sqlite_trace_complete", "passed", "All compact Source Identity Sets trace to matching SQLite source_identities group counts.", "compact_sis", "none", "none"))
    else:
        findings.append(finding("compact_to_sqlite_trace_not_run", "error", "No compact Source Identity Set traces were produced.", "compact_sis", "phase4_3_assertion_records", "source_identity_set_trace"))
    return findings


def write_report(path: Path, summary: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    status_counts = Counter(row["status"] for row in findings)
    lines: list[str] = ["# Tier 2 TEP-to-VDB Namespace Deep Provenance Recon", ""]
    for key in ["audit_id", "generated_utc", "vdb_root", "vap_root", "output_dir"]:
        lines.append(f"{key}: `{summary.get(key, '')}`")
    lines.extend(["", "## Scope", "", "This Tier 2 recon inspects MARK-side VAP TEP artifacts and VDB Phase 3 registration SQLite files.", "It tests whether compact namespace handles can be traced toward producer TEP and registration substrates without performing namespace mediation.", "", "## Safety Boundary", "", "- Read-only VAP TEP inspection.", "- Read-only SQLite connections using `mode=ro` and `PRAGMA query_only=ON`.", "- No MyGene.info or external network calls.", "- No canonical identity creation.", "- No source artifact or SQLite mutation.", "", "## Finding Summary", ""])
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Findings", ""])
    for row in findings:
        lines.append(f"- `{row['check_id']}` — **{row['status']}** — {row['message']} [subject={row['subject']}; earliest_gap_stage={row['earliest_gap_stage']}; recommended_fix_layer={row['recommended_fix_layer']}]")
    lines.extend(["", "## Output Files", ""])
    for output in summary.get("output_files", []):
        lines.append(f"- `{output}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only MARK Tier 2 TEP-to-VDB namespace deep provenance recon.")
    parser.add_argument("--vdb-root", default=".", help="VDB repo root. Default: current directory.")
    parser.add_argument("--vap-root", default=str(DEFAULT_VAP_ROOT), help=f"VAP repo root. Default: {DEFAULT_VAP_ROOT}")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help=f"Output directory. Default: {DEFAULT_OUT_DIR}")
    parser.add_argument("--max-tsv-rows", type=int, default=0, help="Maximum TSV rows to scan per file. Default 0 means full streaming scan.")
    parser.add_argument("--sentinel-limit", type=int, default=5, help="Sentinel rows per class per artifact. Default: 5.")
    parser.add_argument("--sqlite-sample-limit", type=int, default=5, help="Sample rows per SQLite source namespace and assertion registration table. Default: 5.")
    parser.add_argument("--progress-every", type=int, default=1_000_000, help="Print TSV scan progress every N rows. Default: 1,000,000. Use 0 to disable.")
    parser.add_argument("--include-legacy-sqlite", action="store_true", help="Also inspect legacy noncanonical GSC SQLite files as context.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vdb_root = Path(args.vdb_root).expanduser().resolve()
    vap_root = Path(args.vap_root).expanduser().resolve()
    out_dir = (vdb_root / args.out_dir).resolve() if not Path(args.out_dir).is_absolute() else Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Tier 2 TEP-to-VDB namespace deep provenance recon")
    print(f"  vdb_root: {vdb_root}")
    print(f"  vap_root: {vap_root}")
    print(f"  output_dir: {out_dir}")
    print(f"  max_tsv_rows: {'full scan' if args.max_tsv_rows == 0 else args.max_tsv_rows}")
    print("  safety: read-only TEP/SQLite inputs; outputs only under output_dir")
    output_files: list[str] = []
    vap_inventory = inventory_vap_teps(vap_root)
    write_tsv(out_dir / "tier2_vap_tep_inventory.tsv", vap_inventory, ["sra_id", "run_id", "subject_label", "depth_category", "in_current_6tep_corpus", "registration_dir", "expected_tep_dir", "tep_dir_exists", "metadata_artifact_count", "metadata_artifacts_present", "tsv_artifact_count", "audit_status"])
    output_files.append("tier2_vap_tep_inventory.tsv")
    metadata_hits, config_hits = scan_vap_reference_context(vap_root, current_only=True)
    write_tsv(out_dir / "tier2_vap_tep_metadata_reference_hits.tsv", metadata_hits, ["sra_id", "run_id", "subject_label", "depth_category", "metadata_role", "file_path", "line_number", "term", "line_excerpt"])
    output_files.append("tier2_vap_tep_metadata_reference_hits.tsv")
    write_tsv(out_dir / "tier2_vap_config_reference_hits.tsv", config_hits, ["sra_id", "run_id", "subject_label", "depth_category", "config_path", "line_number", "term", "line_excerpt"])
    output_files.append("tier2_vap_config_reference_hits.tsv")
    tsv_summaries, sentinel_rows = scan_current_vap_tsvs(vap_root, args.sentinel_limit, args.max_tsv_rows, args.progress_every)
    write_tsv(out_dir / "tier2_vap_tsv_substrate_summary.tsv", tsv_summaries, ["sra_id", "run_id", "subject_label", "depth_category", "artifact_role", "artifact_path", "exists", "size_bytes", "column_count", "coordinate_columns", "gene_columns", "feature_columns", "producer_columns", "row_count_scanned", "coordinate_complete_rows", "gene_annotated_rows", "feature_context_rows", "intergenic_or_no_gene_rows", "scan_status", "gene_mapping_status_counts", "consequence_counts", "variant_class_counts", "impact_counts"])
    output_files.append("tier2_vap_tsv_substrate_summary.tsv")
    write_tsv(out_dir / "tier2_vap_sentinel_rows.tsv", sentinel_rows, ["sra_id", "run_id", "subject_label", "depth_category", "artifact_role", "artifact_path", "row_number", "sentinel_class", "coordinate_complete", *STANDARD_SENTINEL_COLUMNS])
    output_files.append("tier2_vap_sentinel_rows.tsv")
    database_rows, schema_rows, group_rows, source_samples, assertion_samples, sqlite_findings = inspect_sqlite_databases(vdb_root, args.include_legacy_sqlite, args.sqlite_sample_limit)
    write_tsv(out_dir / "tier2_sqlite_database_inventory.tsv", database_rows, ["db_key", "producer", "registration_dir", "sqlite_path", "in_current_6tep_corpus", "exists", "size_bytes", "read_status", "table_count", "tables"])
    output_files.append("tier2_sqlite_database_inventory.tsv")
    write_tsv(out_dir / "tier2_sqlite_schema_inventory.tsv", schema_rows, ["db_key", "producer", "table_name", "column_count", "columns", "coordinate_columns", "gene_columns", "feature_columns", "producer_columns"])
    output_files.append("tier2_sqlite_schema_inventory.tsv")
    write_tsv(out_dir / "tier2_sqlite_source_identity_group_counts.tsv", group_rows, ["db_key", "producer", "assertion_registration_id", "identity_kind", "participant_role", "source_namespace", "sqlite_source_identity_count", "query_status"])
    output_files.append("tier2_sqlite_source_identity_group_counts.tsv")
    write_tsv(out_dir / "tier2_sqlite_source_identity_samples.tsv", source_samples, ["db_key", "producer", "sample_rank", "source_identity_id", "assertion_registration_id", "identity_kind", "participant_role", "source_namespace", "source_value", "source_label", "extraction_method", "source_record_ref", "payload_json"])
    output_files.append("tier2_sqlite_source_identity_samples.tsv")
    write_tsv(out_dir / "tier2_sqlite_assertion_registration_samples.tsv", assertion_samples, ["db_key", "producer", "sample_rank", "assertion_registration_id", "assertion_type", "subject_id", "subject_namespace", "predicate", "object_id", "object_namespace", "participant_summary_json", "support_ref_json", "source_record_ref", "payload_json", "reference_term_hits"])
    output_files.append("tier2_sqlite_assertion_registration_samples.tsv")
    sis_traces, trace_findings = trace_compact_sis_to_sqlite(vdb_root, group_rows)
    write_tsv(out_dir / "tier2_compact_sis_to_sqlite_trace.tsv", sis_traces, ["source_identity_set_id", "db_key", "table_name", "assertion_id", "source_assertion_registration_id", "identity_kind", "participant_role", "source_namespace", "source_identity_count_expected", "sqlite_source_identity_count_observed", "source_identity_filter", "trace_status"])
    output_files.append("tier2_compact_sis_to_sqlite_trace.tsv")
    findings = []
    findings.extend(sqlite_findings)
    findings.extend(trace_findings)
    findings.extend(derive_findings(vap_inventory, metadata_hits, config_hits, tsv_summaries, sis_traces))
    deduped: list[dict[str, Any]] = []
    seen = set()
    for row in findings:
        key = tuple(row.get(k, "") for k in ["check_id", "status", "message", "subject"])
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    findings = deduped
    write_tsv(out_dir / "tier2_audit_findings.tsv", findings, ["check_id", "status", "message", "subject", "earliest_gap_stage", "recommended_fix_layer"])
    output_files.append("tier2_audit_findings.tsv")
    status_counts = dict(Counter(row["status"] for row in findings))
    trace_status_counts = dict(Counter(row.get("trace_status", "") for row in sis_traces))
    summary = {"audit_id": AUDIT_ID, "generated_utc": utc_now(), "vdb_root": str(vdb_root), "vap_root": str(vap_root), "output_dir": str(out_dir), "max_tsv_rows": args.max_tsv_rows, "vap_tep_count": len(vap_inventory), "current_vap_tep_present_count": sum(1 for r in vap_inventory if r.get("in_current_6tep_corpus") == "true" and r.get("tep_dir_exists") == "true"), "metadata_reference_hit_count": len(metadata_hits), "config_reference_hit_count": len(config_hits), "vap_tsv_artifacts_scanned": len(tsv_summaries), "vap_sentinel_rows": len(sentinel_rows), "sqlite_database_count": len(database_rows), "sqlite_group_count_rows": len(group_rows), "compact_sis_trace_rows": len(sis_traces), "finding_status_counts": status_counts, "compact_sis_trace_status_counts": trace_status_counts, "output_files": output_files}
    (out_dir / "tier2_tep2vdb_deep_recon_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_files.append("tier2_tep2vdb_deep_recon_summary.json")
    write_report(out_dir / "tier2_tep2vdb_deep_recon_report.md", summary, findings)
    output_files.append("tier2_tep2vdb_deep_recon_report.md")
    print("Tier 2 TEP-to-VDB namespace deep provenance recon complete")
    print(f"  output_dir: {out_dir}")
    print(f"  finding_status_counts: {status_counts}")
    print(f"  compact_sis_trace_status_counts: {trace_status_counts}")
    print(f"  report: {out_dir / 'tier2_tep2vdb_deep_recon_report.md'}")


if __name__ == "__main__":
    main()

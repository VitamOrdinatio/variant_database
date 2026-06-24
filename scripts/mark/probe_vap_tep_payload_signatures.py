#!/usr/bin/env python3
"""
probe_vap_tep_payload_signatures.py

Read-only MARK probe for focused inspection of VAP TEP payload signatures.

Purpose:
    Inspect representative certified VAP TEPs deeply enough to inform VDB schema
    documentation without reading entire multi-GB artifacts or mutating anything.

Prime Directive:
    - Read-only against VAP.
    - No mutation of canonical VAP run folders.
    - Write outputs only under /root/Desktop/<probe_name>_<timestamp>/.

Recommended execution on MARK from VDB repo root:

    cd /root/dev/portfolio_projects/variant_database
    source .venv/bin/activate
    python scripts/mark/probe_vap_tep_payload_signatures.py

Default representative runs:
    q1      ERR10619212  run_2026_05_30_214724
    median  ERR10619300  run_2026_05_27_172531
    q3      ERR10619225  run_2026_05_31_091242
    hg002    SRR12898354  run_2026_06_03_010030

Probe outputs:
    /root/Desktop/probe_vap_tep_payload_signatures_<timestamp>/
        probe_manifest.tsv
        selected_run_summary.tsv
        json_signature.tsv
        entity_artifact_signature.tsv
        lineage_edge_signature.tsv
        tabular_signature.tsv
        tabular_column_union.tsv
        tabular_preview_samples.tsv
        preservation_target_matrix.tsv
        warnings.txt
        probe.log

This probe intentionally inspects the full VAP TEP package topology:
    entity_inventory.json
    lineage_manifest.json
    validation_report.md
    entities/observation/
    entities/normalization/
    entities/coding_interpretation/
    entities/noncoding_interpretation/
    entities/prioritization/
    entities/routing/
    entities/validation/
    entities/context/

It does NOT treat stage_08_vdb_ready_variants.tsv as sufficient for VDB preservation.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPRESENTATIVE_RUNS = [
    {"sra": "ERR10619212", "run_id": "run_2026_05_30_214724", "depth_category": "q1"},
    {"sra": "ERR10619300", "run_id": "run_2026_05_27_172531", "depth_category": "median"},
    {"sra": "ERR10619225", "run_id": "run_2026_05_31_091242", "depth_category": "q3"},
    {"sra": "SRR12898354", "run_id": "run_2026_06_03_010030", "depth_category": "hg002"},
]

ENTITY_DIRS = [
    "observation",
    "normalization",
    "coding_interpretation",
    "noncoding_interpretation",
    "prioritization",
    "routing",
    "validation",
    "context",
]

TARGET_BASENAMES = {
    "entity_inventory.json",
    "lineage_manifest.json",
    "validation_report.md",
    "annotated_variants.tsv",
    "stage_08_vdb_ready_variants.tsv",
    "stage_08_selected_transcript_consequences.tsv",
    "stage_09_coding_interpreted.tsv",
    "stage_10_noncoding_interpreted.tsv",
    "stage_11_prioritized_variants.tsv",
    "stage_12_validation_candidates.tsv",
}

# Column classes are deliberately broad. They help DEX-VDB reason about schema domains
# without interpreting biological values or making clinical assertions.
COLUMN_CLASS_PATTERNS = {
    "sample_identity": ["sample", "sra"],
    "run_identity": ["run_id", "run"],
    "variant_identity": ["variant", "chrom", "pos", "ref", "alt", "allele", "genotype", "zygosity"],
    "gene_identity": ["gene", "hgnc", "ensembl", "symbol"],
    "transcript_identity": ["transcript", "mane", "canonical"],
    "annotation": ["annotation", "consequence", "impact", "effect", "biotype"],
    "clinical": ["clinvar", "clinical", "pathogenic", "benign", "significance"],
    "population_frequency": ["gnomad", "af", "frequency", "maf"],
    "prioritization": ["priority", "tier", "rank", "score", "candidate"],
    "validation": ["validation", "qc", "quality", "flag", "status"],
    "provenance": ["source", "provenance", "lineage", "artifact", "stage", "timestamp"],
    "noncoding": ["noncoding", "regulatory", "promoter", "enhancer", "utr", "splice"],
    "routing": ["route", "routing"],
    "context": ["summary", "context"],
}


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_tsv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def log_line(log_path: Path, message: str) -> None:
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text_head(path: Path, max_bytes: int) -> str:
    with path.open("rb") as handle:
        data = handle.read(max_bytes)
    return data.decode("utf-8", errors="replace")


def read_gzip_text_head(path: Path, max_bytes: int) -> str:
    chunks: List[bytes] = []
    total = 0
    with gzip.open(path, "rb") as handle:
        while total < max_bytes:
            chunk = handle.read(min(65536, max_bytes - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


def flatten_json_keys(obj: Any, prefix: str = "", max_keys: int = 500) -> List[str]:
    keys: List[str] = []

    def visit(value: Any, pfx: str) -> None:
        if len(keys) >= max_keys:
            return
        if isinstance(value, dict):
            for k, v in value.items():
                key = f"{pfx}.{k}" if pfx else str(k)
                keys.append(key)
                visit(v, key)
                if len(keys) >= max_keys:
                    return
        elif isinstance(value, list):
            key = f"{pfx}[]" if pfx else "[]"
            keys.append(key)
            if value:
                visit(value[0], key)

    visit(obj, prefix)
    return keys


def load_json_if_safe(path: Path, max_bytes: int) -> Tuple[Optional[Any], str]:
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return None, f"SKIPPED_SIZE_GT_{max_bytes}"
        return json.loads(read_text_head(path, max_bytes=max_bytes)), "OK"
    except Exception as exc:
        return None, f"ERROR: {type(exc).__name__}: {exc}"


def classify_column(column: str) -> str:
    c = column.lower()
    hits: List[str] = []
    for class_name, patterns in COLUMN_CLASS_PATTERNS.items():
        if any(p in c for p in patterns):
            hits.append(class_name)
    return "|".join(hits) if hits else "unclassified"


def infer_entity_domain(path: Path) -> str:
    parts = path.parts
    if "entities" in parts:
        idx = parts.index("entities")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    name = path.name.lower()
    if name == "entity_inventory.json":
        return "tep_inventory"
    if name == "lineage_manifest.json":
        return "tep_lineage"
    if name == "validation_report.md":
        return "tep_validation_report"
    return "unknown"


def is_tabular(path: Path) -> bool:
    suffixes = "".join(path.suffixes).lower()
    return (
        path.suffix.lower() in {".tsv", ".csv"}
        or suffixes.endswith(".tsv.gz")
        or suffixes.endswith(".csv.gz")
    )


def is_json(path: Path) -> bool:
    return path.suffix.lower() == ".json"


def collect_tep_files(tep_dir: Path) -> List[Path]:
    if not tep_dir.exists() or not tep_dir.is_dir():
        return []
    files: List[Path] = []
    for root, dirs, filenames in os.walk(tep_dir):
        dirs.sort()
        filenames.sort()
        for fn in filenames:
            files.append(Path(root) / fn)
    return files


def count_rows_safe(path: Path, max_lines: int) -> Tuple[int, bool, str]:
    """
    Count rows by streaming text. This reads line-by-line and does not load the file.
    Returns data row count estimate excluding header when possible.
    """
    try:
        suffixes = "".join(path.suffixes).lower()
        opener = gzip.open if suffixes.endswith(".gz") else open
        line_count = 0
        truncated = False
        with opener(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
            for line_count, _ in enumerate(handle, start=1):
                if line_count >= max_lines:
                    truncated = True
                    break
        if line_count == 0:
            return 0, truncated, "OK_EMPTY"
        return max(0, line_count - 1), truncated, "OK"
    except Exception as exc:
        return -1, False, f"ERROR: {type(exc).__name__}: {exc}"


def read_tabular_preview(path: Path, max_bytes: int, max_rows: int) -> Tuple[List[str], List[List[str]], str, str]:
    try:
        suffixes = "".join(path.suffixes).lower()
        if suffixes.endswith(".gz"):
            text = read_gzip_text_head(path, max_bytes=max_bytes)
        else:
            text = read_text_head(path, max_bytes=max_bytes)

        lines = text.splitlines()
        if not lines:
            return [], [], "", "OK_EMPTY"
        delimiter = "\t" if "\t" in lines[0] else ","
        header = lines[0].split(delimiter)
        data_rows = [line.split(delimiter) for line in lines[1 : 1 + max_rows]]
        return header, data_rows, "TAB" if delimiter == "\t" else "COMMA", "OK"
    except Exception as exc:
        return [], [], "", f"ERROR: {type(exc).__name__}: {exc}"


def summarize_json(
    path: Path,
    tep_dir: Path,
    sra: str,
    run_id: str,
    depth: str,
    max_json_bytes: int,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    obj, status = load_json_if_safe(path, max_json_bytes)
    rel = safe_rel(path, tep_dir)
    size = path.stat().st_size if path.exists() else ""

    top_type = ""
    top_keys = ""
    flattened = ""

    artifact_rows: List[Dict[str, Any]] = []
    lineage_rows: List[Dict[str, Any]] = []

    if obj is not None:
        if isinstance(obj, dict):
            top_type = "object"
            top_keys = "|".join(map(str, list(obj.keys())[:100]))
        elif isinstance(obj, list):
            top_type = "array"
            top_keys = "[]"
        else:
            top_type = type(obj).__name__
        flattened = "|".join(flatten_json_keys(obj, max_keys=500))

        # Entity inventory usually contains artifacts/entities. Preserve broad signatures.
        if path.name == "entity_inventory.json" and isinstance(obj, dict):
            for candidate_key in ["artifacts", "entities"]:
                value = obj.get(candidate_key)
                if isinstance(value, list):
                    for idx, item in enumerate(value[:10000]):
                        if isinstance(item, dict):
                            artifact_rows.append({
                                "sra": sra,
                                "run_id": run_id,
                                "depth_category": depth,
                                "source_json": rel,
                                "record_group": candidate_key,
                                "record_index": idx,
                                "record_keys": "|".join(map(str, item.keys())),
                                "artifact_id": item.get("artifact_id", item.get("id", "")),
                                "entity_id": item.get("entity_id", ""),
                                "entity_type": item.get("entity_type", item.get("type", "")),
                                "semantic_role": item.get("semantic_role", item.get("role", "")),
                                "path": item.get("path", item.get("artifact_path", "")),
                                "producer_ownership": item.get("producer_ownership", ""),
                                "status": "OK",
                            })
                elif isinstance(value, dict):
                    for idx, (key, item) in enumerate(value.items()):
                        if isinstance(item, dict):
                            artifact_rows.append({
                                "sra": sra,
                                "run_id": run_id,
                                "depth_category": depth,
                                "source_json": rel,
                                "record_group": candidate_key,
                                "record_index": idx,
                                "record_keys": "|".join(map(str, item.keys())),
                                "artifact_id": item.get("artifact_id", key),
                                "entity_id": item.get("entity_id", ""),
                                "entity_type": item.get("entity_type", item.get("type", "")),
                                "semantic_role": item.get("semantic_role", item.get("role", "")),
                                "path": item.get("path", item.get("artifact_path", "")),
                                "producer_ownership": item.get("producer_ownership", ""),
                                "status": "OK",
                            })

        # Lineage manifest usually contains lineage_edges/entities. Preserve edge signatures.
        if path.name == "lineage_manifest.json" and isinstance(obj, dict):
            for edge_key in ["lineage_edges", "edges"]:
                edges = obj.get(edge_key)
                if isinstance(edges, list):
                    for idx, edge in enumerate(edges[:10000]):
                        if isinstance(edge, dict):
                            lineage_rows.append({
                                "sra": sra,
                                "run_id": run_id,
                                "depth_category": depth,
                                "source_json": rel,
                                "edge_group": edge_key,
                                "edge_index": idx,
                                "edge_keys": "|".join(map(str, edge.keys())),
                                "source": edge.get("source", edge.get("from", edge.get("source_entity", ""))),
                                "target": edge.get("target", edge.get("to", edge.get("target_entity", ""))),
                                "relationship": edge.get("relationship", edge.get("relation", edge.get("edge_type", ""))),
                                "status": "OK",
                            })

    json_row = {
        "sra": sra,
        "run_id": run_id,
        "depth_category": depth,
        "relative_path": rel,
        "entity_domain": infer_entity_domain(path),
        "size_bytes": size,
        "status": status,
        "top_level_type": top_type,
        "top_level_keys": top_keys,
        "flattened_keys_sample": flattened,
    }

    return json_row, artifact_rows, lineage_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Focused read-only VAP TEP payload signature probe.")
    parser.add_argument("--vap-root", default="/root/dev/portfolio_projects/variant_annotation_pipeline")
    parser.add_argument("--output-root", default="/root/Desktop")
    parser.add_argument("--json-max-bytes", type=int, default=75_000_000)
    parser.add_argument("--preview-max-bytes", type=int, default=2_000_000)
    parser.add_argument("--preview-rows", type=int, default=3)
    parser.add_argument("--row-count-max-lines", type=int, default=25_000_000)
    args = parser.parse_args()

    vap_root = Path(args.vap_root).expanduser().resolve()
    outdir = Path(args.output_root).expanduser().resolve() / f"probe_vap_tep_payload_signatures_{now_stamp()}"
    outdir.mkdir(parents=True, exist_ok=False)

    log_path = outdir / "probe.log"
    warnings: List[str] = []

    log_line(log_path, "Starting probe_vap_tep_payload_signatures.py")
    log_line(log_path, f"VAP root: {vap_root}")
    log_line(log_path, f"Output directory: {outdir}")
    log_line(log_path, "Prime Directive: read-only against VAP; writes only to output directory.")

    probe_manifest_rows = [{
        "probe_name": "probe_vap_tep_payload_signatures",
        "probe_version": "1.0.0",
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "vap_root": str(vap_root),
        "output_directory": str(outdir),
        "selected_run_count": len(REPRESENTATIVE_RUNS),
        "prime_directive": "READ_ONLY_AGAINST_VAP_WRITE_ONLY_TO_ROOT_DESKTOP_OUTPUT_FOLDER",
        "schema_note": "Stage08 is inspected as one entity surface, not treated as sufficient preservation substrate.",
    }]

    selected_run_rows: List[Dict[str, Any]] = []
    json_rows: List[Dict[str, Any]] = []
    entity_artifact_rows: List[Dict[str, Any]] = []
    lineage_edge_rows: List[Dict[str, Any]] = []
    tabular_rows: List[Dict[str, Any]] = []
    column_union_rows: List[Dict[str, Any]] = []
    preview_rows: List[Dict[str, Any]] = []
    preservation_matrix_rows: List[Dict[str, Any]] = []

    for item in REPRESENTATIVE_RUNS:
        sra = item["sra"]
        run_id = item["run_id"]
        depth = item["depth_category"]
        run_root = vap_root / "results" / run_id
        tep_dir = run_root / "tep"

        log_line(log_path, f"Inspecting representative run: {sra} {run_id} {depth}")

        files = collect_tep_files(tep_dir)
        selected_run_rows.append({
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "run_root": str(run_root),
            "tep_dir": str(tep_dir),
            "run_root_exists": run_root.exists(),
            "tep_dir_exists": tep_dir.exists(),
            "tep_file_count": len(files),
            "tep_total_size_bytes": sum(p.stat().st_size for p in files if p.exists()),
            "status": "OK" if tep_dir.exists() else "TEP_DIR_MISSING",
        })

        if not tep_dir.exists():
            warnings.append(f"TEP_DIR_MISSING: {tep_dir}")
            continue

        present_entity_dirs = set()
        target_presence = {name: False for name in TARGET_BASENAMES}

        for entity_dir in ENTITY_DIRS:
            if (tep_dir / "entities" / entity_dir).exists():
                present_entity_dirs.add(entity_dir)

        for path in files:
            if path.name in target_presence:
                target_presence[path.name] = True

            if is_json(path):
                json_row, artifact_rows, edge_rows = summarize_json(
                    path, tep_dir, sra, run_id, depth, max_json_bytes=args.json_max_bytes
                )
                json_rows.append(json_row)
                entity_artifact_rows.extend(artifact_rows)
                lineage_edge_rows.extend(edge_rows)

            if is_tabular(path):
                header, data_rows, delim, status = read_tabular_preview(
                    path, max_bytes=args.preview_max_bytes, max_rows=args.preview_rows
                )
                data_row_estimate, truncated, row_status = count_rows_safe(path, max_lines=args.row_count_max_lines)

                rel = safe_rel(path, tep_dir)
                entity_domain = infer_entity_domain(path)
                col_classes = [classify_column(col) for col in header]
                tabular_rows.append({
                    "sra": sra,
                    "run_id": run_id,
                    "depth_category": depth,
                    "relative_path": rel,
                    "entity_domain": entity_domain,
                    "size_bytes": path.stat().st_size,
                    "status": status,
                    "row_count_status": row_status,
                    "data_row_count_estimate": data_row_estimate,
                    "row_count_truncated": truncated,
                    "delimiter_guess": delim,
                    "column_count": len(header),
                    "columns": "|".join(header),
                    "column_classes": "|".join(col_classes),
                })

                for idx, col in enumerate(header):
                    column_union_rows.append({
                        "sra": sra,
                        "run_id": run_id,
                        "depth_category": depth,
                        "relative_path": rel,
                        "entity_domain": entity_domain,
                        "column_index": idx,
                        "column_name": col,
                        "column_class": classify_column(col),
                    })

                for ridx, row in enumerate(data_rows):
                    # Store short structural previews only. This is not for biological interpretation.
                    values = []
                    for value in row[: min(len(row), 40)]:
                        if len(value) > 120:
                            values.append(value[:120] + "...TRUNCATED")
                        else:
                            values.append(value)
                    preview_rows.append({
                        "sra": sra,
                        "run_id": run_id,
                        "depth_category": depth,
                        "relative_path": rel,
                        "entity_domain": entity_domain,
                        "preview_row_index": ridx,
                        "preview_values_first_40_columns": "|".join(values),
                    })

        for entity_dir in ENTITY_DIRS:
            preservation_matrix_rows.append({
                "sra": sra,
                "run_id": run_id,
                "depth_category": depth,
                "preservation_unit": f"entities/{entity_dir}/",
                "present": entity_dir in present_entity_dirs,
                "unit_type": "entity_directory",
            })

        for basename, present in sorted(target_presence.items()):
            preservation_matrix_rows.append({
                "sra": sra,
                "run_id": run_id,
                "depth_category": depth,
                "preservation_unit": basename,
                "present": present,
                "unit_type": "target_artifact_basename",
            })

    write_tsv(outdir / "probe_manifest.tsv", probe_manifest_rows, [
        "probe_name", "probe_version", "timestamp", "vap_root", "output_directory",
        "selected_run_count", "prime_directive", "schema_note"
    ])
    write_tsv(outdir / "selected_run_summary.tsv", selected_run_rows, [
        "sra", "run_id", "depth_category", "run_root", "tep_dir", "run_root_exists",
        "tep_dir_exists", "tep_file_count", "tep_total_size_bytes", "status"
    ])
    write_tsv(outdir / "json_signature.tsv", json_rows, [
        "sra", "run_id", "depth_category", "relative_path", "entity_domain", "size_bytes",
        "status", "top_level_type", "top_level_keys", "flattened_keys_sample"
    ])
    write_tsv(outdir / "entity_artifact_signature.tsv", entity_artifact_rows, [
        "sra", "run_id", "depth_category", "source_json", "record_group", "record_index",
        "record_keys", "artifact_id", "entity_id", "entity_type", "semantic_role",
        "path", "producer_ownership", "status"
    ])
    write_tsv(outdir / "lineage_edge_signature.tsv", lineage_edge_rows, [
        "sra", "run_id", "depth_category", "source_json", "edge_group", "edge_index",
        "edge_keys", "source", "target", "relationship", "status"
    ])
    write_tsv(outdir / "tabular_signature.tsv", tabular_rows, [
        "sra", "run_id", "depth_category", "relative_path", "entity_domain", "size_bytes",
        "status", "row_count_status", "data_row_count_estimate", "row_count_truncated",
        "delimiter_guess", "column_count", "columns", "column_classes"
    ])
    write_tsv(outdir / "tabular_column_union.tsv", column_union_rows, [
        "sra", "run_id", "depth_category", "relative_path", "entity_domain",
        "column_index", "column_name", "column_class"
    ])
    write_tsv(outdir / "tabular_preview_samples.tsv", preview_rows, [
        "sra", "run_id", "depth_category", "relative_path", "entity_domain",
        "preview_row_index", "preview_values_first_40_columns"
    ])
    write_tsv(outdir / "preservation_target_matrix.tsv", preservation_matrix_rows, [
        "sra", "run_id", "depth_category", "preservation_unit", "present", "unit_type"
    ])

    (outdir / "warnings.txt").write_text("\n".join(warnings) + ("\n" if warnings else ""), encoding="utf-8")
    log_line(log_path, f"Completed probe. Output directory: {outdir}")

    print(f"Probe completed: {outdir}")
    print("Primary outputs:")
    for name in [
        "selected_run_summary.tsv",
        "json_signature.tsv",
        "entity_artifact_signature.tsv",
        "lineage_edge_signature.tsv",
        "tabular_signature.tsv",
        "tabular_column_union.tsv",
        "preservation_target_matrix.tsv",
    ]:
        print(f"  {outdir / name}")
    if warnings:
        print(f"Warnings: {outdir / 'warnings.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

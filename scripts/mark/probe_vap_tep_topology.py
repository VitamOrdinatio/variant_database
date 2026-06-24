#!/usr/bin/env python3
"""
probe_vap_tep_topology.py

Read-only MARK probe for inspecting certified VAP TEP topology from the VDB repo.

Prime Directive:
    - Do not mutate VAP artifacts.
    - Do not delete, move, rename, chmod, touch, or rewrite canonical VAP files.
    - Only write probe outputs under /root/Desktop/<probe_name>_<timestamp>/.

Intended execution on MARK from VDB repo root:

    cd /root/dev/portfolio_projects/variant_database
    source .venv/bin/activate
    python scripts/mark/probe_vap_tep_topology.py

Primary target:
    /root/dev/portfolio_projects/variant_annotation_pipeline/results/run_<id>/tep/

Secondary context target:
    /root/dev/portfolio_projects/variant_annotation_pipeline/results/run_<id>/processed/
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CANONICAL_RUNS = [
    {"sra": "ERR10619203", "run_id": "run_2026_05_30_071639", "depth_category": "q3"},
    {"sra": "ERR10619207", "run_id": "run_2026_06_01_124134", "depth_category": "q3"},
    {"sra": "ERR10619208", "run_id": "run_2026_05_30_151355", "depth_category": "median"},
    {"sra": "ERR10619212", "run_id": "run_2026_05_30_214724", "depth_category": "q1"},
    {"sra": "ERR10619225", "run_id": "run_2026_05_31_091242", "depth_category": "q3"},
    {"sra": "ERR10619230", "run_id": "run_2026_06_01_004903", "depth_category": "q3"},
    {"sra": "ERR10619241", "run_id": "run_2026_06_02_052302", "depth_category": "q1"},
    {"sra": "ERR10619281", "run_id": "run_2026_05_27_233524", "depth_category": "median"},
    {"sra": "ERR10619285", "run_id": "run_2026_06_02_124300", "depth_category": "median"},
    {"sra": "ERR10619300", "run_id": "run_2026_05_27_172531", "depth_category": "median"},
    {"sra": "ERR10619309", "run_id": "run_2026_06_02_181024", "depth_category": "q1"},
    {"sra": "ERR10619330", "run_id": "run_2026_06_01_203130", "depth_category": "q1"},
    {"sra": "SRR12898354", "run_id": "run_2026_06_03_010030", "depth_category": "hg002"},
]


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


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


def file_record(path: Path, run_root: Path, target_label: str, sra: str, run_id: str, depth: str) -> Dict[str, Any]:
    try:
        st = path.stat()
        size = st.st_size
        mtime = dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")
        status = "OK"
    except OSError as exc:
        size = ""
        mtime = ""
        status = f"STAT_ERROR: {exc}"

    return {
        "sra": sra,
        "run_id": run_id,
        "depth_category": depth,
        "target": target_label,
        "relative_path": safe_rel(path, run_root),
        "suffix": path.suffix.lower(),
        "size_bytes": size,
        "mtime": mtime,
        "status": status,
    }


def inventory_files(
    base: Path,
    run_root: Path,
    target_label: str,
    sra: str,
    run_id: str,
    depth: str,
    max_files: int,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    rows: List[Dict[str, Any]] = []
    if not base.exists():
        return rows, "MISSING"
    if not base.is_dir():
        return rows, "NOT_DIRECTORY"

    count = 0
    for root, dirs, files in os.walk(base):
        dirs.sort()
        files.sort()
        for filename in files:
            count += 1
            if count > max_files:
                return rows, f"MAX_FILES_REACHED for {base}: {max_files}"
            rows.append(file_record(Path(root) / filename, run_root, target_label, sra, run_id, depth))

    return rows, None


def read_text_head(path: Path, max_bytes: int = 1_000_000) -> str:
    data = path.open("rb").read(max_bytes)
    return data.decode("utf-8", errors="replace")


def read_gzip_text_head(path: Path, max_bytes: int = 1_000_000) -> str:
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


def flatten_json_keys(obj: Any, prefix: str = "", max_keys: int = 300) -> List[str]:
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


def inspect_json(path: Path, run_root: Path, sra: str, run_id: str, depth: str, max_size: int) -> Dict[str, Any]:
    rel = safe_rel(path, run_root)
    try:
        size = path.stat().st_size
        if size > max_size:
            return {
                "sra": sra,
                "run_id": run_id,
                "depth_category": depth,
                "relative_path": rel,
                "size_bytes": size,
                "status": f"SKIPPED_SIZE_GT_{max_size}",
                "top_level_type": "",
                "top_level_keys": "",
                "flattened_keys_sample": "",
            }
        obj = json.loads(read_text_head(path, max_bytes=max_size))
        if isinstance(obj, dict):
            top_keys = list(obj.keys())
            top_type = "object"
        elif isinstance(obj, list):
            top_keys = ["[]"]
            top_type = "array"
        else:
            top_keys = []
            top_type = type(obj).__name__
        flat = flatten_json_keys(obj)
        return {
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "relative_path": rel,
            "size_bytes": size,
            "status": "OK",
            "top_level_type": top_type,
            "top_level_keys": "|".join(map(str, top_keys[:100])),
            "flattened_keys_sample": "|".join(flat[:300]),
        }
    except Exception as exc:
        return {
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "relative_path": rel,
            "size_bytes": path.stat().st_size if path.exists() else "",
            "status": f"ERROR: {type(exc).__name__}: {exc}",
            "top_level_type": "",
            "top_level_keys": "",
            "flattened_keys_sample": "",
        }


def inspect_tabular_header(path: Path, run_root: Path, sra: str, run_id: str, depth: str, max_head_bytes: int) -> Dict[str, Any]:
    rel = safe_rel(path, run_root)
    try:
        suffixes = "".join(path.suffixes).lower()
        if suffixes.endswith(".gz"):
            text = read_gzip_text_head(path, max_bytes=max_head_bytes)
        else:
            text = read_text_head(path, max_bytes=max_head_bytes)
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        delimiter = "\t" if "\t" in first_line else ","
        columns = first_line.split(delimiter) if first_line else []
        return {
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "relative_path": rel,
            "size_bytes": path.stat().st_size,
            "status": "OK",
            "delimiter_guess": "TAB" if delimiter == "\t" else "COMMA",
            "column_count": len(columns),
            "columns": "|".join(columns),
        }
    except Exception as exc:
        return {
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "relative_path": rel,
            "size_bytes": path.stat().st_size if path.exists() else "",
            "status": f"ERROR: {type(exc).__name__}: {exc}",
            "delimiter_guess": "",
            "column_count": "",
            "columns": "",
        }


def make_tree_text(base: Path, label: str, max_depth: int = 8, max_entries: int = 5000) -> List[str]:
    lines: List[str] = [f"# {label}: {base}"]
    if not base.exists():
        lines.append("MISSING")
        return lines
    if not base.is_dir():
        lines.append("NOT_DIRECTORY")
        return lines

    base_depth = len(base.parts)
    emitted = 0
    for root, dirs, files in os.walk(base):
        dirs.sort()
        files.sort()
        root_path = Path(root)
        depth = len(root_path.parts) - base_depth
        if depth > max_depth:
            dirs[:] = []
            continue

        indent = "  " * depth
        lines.append(f"{indent}{root_path.name}/" if root_path != base else f"{base.name}/")

        child_indent = "  " * (depth + 1)
        for filename in files:
            emitted += 1
            if emitted > max_entries:
                lines.append(f"{child_indent}... MAX_ENTRIES_REACHED {max_entries}")
                return lines
            path = root_path / filename
            try:
                size = path.stat().st_size
            except OSError:
                size = "NA"
            lines.append(f"{child_indent}{filename}\t{size}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only VAP TEP topology probe for MARK.")
    parser.add_argument("--vap-root", default="/root/dev/portfolio_projects/variant_annotation_pipeline")
    parser.add_argument("--output-root", default="/root/Desktop")
    parser.add_argument("--processed-max-files", type=int, default=150)
    parser.add_argument("--tep-max-files", type=int, default=5000)
    parser.add_argument("--json-max-size", type=int, default=50_000_000)
    parser.add_argument("--header-max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()

    vap_root = Path(args.vap_root).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()
    outdir = output_root / f"probe_vap_tep_topology_{now_stamp()}"
    outdir.mkdir(parents=True, exist_ok=False)

    log_path = outdir / "probe.log"
    warnings: List[str] = []

    log_line(log_path, "Starting probe_vap_tep_topology.py")
    log_line(log_path, f"VAP root: {vap_root}")
    log_line(log_path, f"Output directory: {outdir}")
    log_line(log_path, "Prime Directive: read-only against VAP; writes only to output directory.")

    probe_manifest = [{
        "probe_name": "probe_vap_tep_topology",
        "probe_version": "1.0.0",
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "vap_root": str(vap_root),
        "output_directory": str(outdir),
        "run_count": len(CANONICAL_RUNS),
        "prime_directive": "READ_ONLY_AGAINST_VAP_WRITE_ONLY_TO_ROOT_DESKTOP_OUTPUT_FOLDER",
    }]

    run_summary_rows: List[Dict[str, Any]] = []
    tep_file_rows: List[Dict[str, Any]] = []
    processed_file_rows: List[Dict[str, Any]] = []
    json_rows: List[Dict[str, Any]] = []
    tabular_rows: List[Dict[str, Any]] = []
    tree_lines: List[str] = []

    if not vap_root.exists():
        warnings.append(f"VAP_ROOT_MISSING: {vap_root}")

    for item in CANONICAL_RUNS:
        sra = item["sra"]
        run_id = item["run_id"]
        depth = item["depth_category"]
        run_root = vap_root / "results" / run_id
        tep_dir = run_root / "tep"
        processed_dir = run_root / "processed"

        log_line(log_path, f"Inspecting {sra} {run_id} {depth}")

        run_summary = {
            "sra": sra,
            "run_id": run_id,
            "depth_category": depth,
            "run_root": str(run_root),
            "run_root_exists": run_root.exists(),
            "tep_dir_exists": tep_dir.exists(),
            "processed_dir_exists": processed_dir.exists(),
            "tep_file_count": "",
            "tep_total_size_bytes": "",
            "processed_limited_file_count": "",
            "status": "OK",
        }

        if not run_root.exists():
            run_summary["status"] = "RUN_ROOT_MISSING"
            warnings.append(f"RUN_ROOT_MISSING: {run_root}")
            run_summary_rows.append(run_summary)
            continue

        rows, warning = inventory_files(tep_dir, run_root, "tep", sra, run_id, depth, max_files=args.tep_max_files)
        if warning:
            warnings.append(f"{sra} {run_id} tep: {warning}")
        tep_file_rows.extend(rows)
        run_summary["tep_file_count"] = len(rows)
        run_summary["tep_total_size_bytes"] = sum(int(r["size_bytes"]) for r in rows if str(r["size_bytes"]).isdigit())

        proc_rows, proc_warning = inventory_files(
            processed_dir, run_root, "processed_limited", sra, run_id, depth, max_files=args.processed_max_files
        )
        if proc_warning:
            warnings.append(f"{sra} {run_id} processed: {proc_warning}")
        processed_file_rows.extend(proc_rows)
        run_summary["processed_limited_file_count"] = len(proc_rows)

        tree_lines.extend(make_tree_text(tep_dir, f"{sra} {run_id} {depth}", max_depth=8))
        tree_lines.append("")

        for r in rows:
            rel_path = r["relative_path"]
            path = run_root / rel_path
            suffixes = "".join(path.suffixes).lower()
            suffix = path.suffix.lower()

            if suffix == ".json":
                json_rows.append(inspect_json(path, run_root, sra, run_id, depth, max_size=args.json_max_size))

            if suffix in {".tsv", ".csv"} or suffixes.endswith(".tsv.gz") or suffixes.endswith(".csv.gz"):
                tabular_rows.append(inspect_tabular_header(path, run_root, sra, run_id, depth, max_head_bytes=args.header_max_bytes))

        run_summary_rows.append(run_summary)

    write_tsv(outdir / "probe_manifest.tsv", probe_manifest, [
        "probe_name", "probe_version", "timestamp", "vap_root", "output_directory", "run_count", "prime_directive"
    ])
    write_tsv(outdir / "run_summary.tsv", run_summary_rows, [
        "sra", "run_id", "depth_category", "run_root", "run_root_exists", "tep_dir_exists",
        "processed_dir_exists", "tep_file_count", "tep_total_size_bytes", "processed_limited_file_count", "status"
    ])
    write_tsv(outdir / "tep_file_inventory.tsv", tep_file_rows, [
        "sra", "run_id", "depth_category", "target", "relative_path", "suffix", "size_bytes", "mtime", "status"
    ])
    write_tsv(outdir / "processed_file_inventory_limited.tsv", processed_file_rows, [
        "sra", "run_id", "depth_category", "target", "relative_path", "suffix", "size_bytes", "mtime", "status"
    ])
    write_tsv(outdir / "json_key_inventory.tsv", json_rows, [
        "sra", "run_id", "depth_category", "relative_path", "size_bytes", "status",
        "top_level_type", "top_level_keys", "flattened_keys_sample"
    ])
    write_tsv(outdir / "tabular_header_inventory.tsv", tabular_rows, [
        "sra", "run_id", "depth_category", "relative_path", "size_bytes", "status",
        "delimiter_guess", "column_count", "columns"
    ])

    (outdir / "tree_tep.txt").write_text("\n".join(tree_lines) + "\n", encoding="utf-8")
    (outdir / "warnings.txt").write_text("\n".join(warnings) + ("\n" if warnings else ""), encoding="utf-8")

    log_line(log_path, f"Completed probe. Output directory: {outdir}")

    print(f"Probe completed: {outdir}")
    print("Primary outputs:")
    print(f"  {outdir / 'run_summary.tsv'}")
    print(f"  {outdir / 'tep_file_inventory.tsv'}")
    print(f"  {outdir / 'json_key_inventory.tsv'}")
    print(f"  {outdir / 'tabular_header_inventory.tsv'}")
    print(f"  {outdir / 'tree_tep.txt'}")
    if warnings:
        print(f"Warnings: {outdir / 'warnings.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

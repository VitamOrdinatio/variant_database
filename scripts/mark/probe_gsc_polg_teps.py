#!/usr/bin/env python3
"""
Read-only MARK probe for POLG signals in certified TEP-GSCs.

Purpose:
    Collect topology, manifest/entity-like summaries, lightweight artifact
    metadata, and POLG-specific rows from the two certified GSC TEPs used
    for VDB lifecycle exemplar development.

Prime Directive:
    This probe is strictly read-only with respect to GSC/VDB repositories.
    It writes output only to /root/Desktop/vdb_gsc_polg_tep_probe/.

Canonical targets:
    GSC repo:
        /root/dev/portfolio_projects/gene_set_consensus

    Certified TEP-GSC paths expected from MARK:
        results/teps/gsc/epilepsy_semantic_gtr_experimental/run_2026_06_22_184534/
        results/teps/gsc/mitochondrial_semantic_gtr_experimental/run_2026_06_23_015533/

Notes:
    This probe intentionally avoids mutation, copying producer artifacts, or
    rewriting TEP contents. It reads small TSV/JSON/YAML/MD/TXT files in place,
    computes summaries, searches for POLG rows, and writes a compact report.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GSC_ROOT = Path("/root/dev/portfolio_projects/gene_set_consensus")
RESULTS_ROOT = GSC_ROOT / "results"

TARGET_GENE_SYMBOLS = {"POLG"}

TEP_TARGETS = [
    {
        "phenotype_surface": "epilepsy_semantic_gtr_experimental",
        "run_id": "run_2026_06_22_184534",
        "tep_dir": RESULTS_ROOT
        / "teps"
        / "gsc"
        / "epilepsy_semantic_gtr_experimental"
        / "run_2026_06_22_184534",
        "table_dir": RESULTS_ROOT / "tables" / "epilepsy_semantic_gtr_experimental",
        "report_dir": RESULTS_ROOT / "reports" / "epilepsy_semantic_gtr_experimental",
    },
    {
        "phenotype_surface": "mitochondrial_semantic_gtr_experimental",
        "run_id": "run_2026_06_23_015533",
        "tep_dir": RESULTS_ROOT
        / "teps"
        / "gsc"
        / "mitochondrial_semantic_gtr_experimental"
        / "run_2026_06_23_015533",
        "table_dir": RESULTS_ROOT / "tables" / "mitochondrial_semantic_gtr_experimental",
        "report_dir": RESULTS_ROOT / "reports" / "mitochondrial_semantic_gtr_experimental",
    },
]

OUT_DIR = Path("/root/Desktop/vdb_gsc_polg_tep_probe")
OUT_JSON = OUT_DIR / "gsc_polg_tep_probe.json"
OUT_MD = OUT_DIR / "gsc_polg_tep_probe.md"

MAX_TEXT_PREVIEW_LINES = 40
MAX_JSON_TOP_KEYS = 100
MAX_MATCHES_PER_FILE = 25
MAX_TREE_FILES_PER_TARGET = 500
MAX_FILE_BYTES_TO_SCAN = 128 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".tsv":
        return "tsv"
    if suffix == ".csv":
        return "csv"
    if suffix in {".md", ".txt", ".log"}:
        return "text"
    return suffix.lstrip(".") or "unknown"


def safe_read_text(path: Path, max_bytes: int = 64 * 1024) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(max_bytes)
        return data.decode("utf-8", errors="replace")
    except Exception as exc:
        return f"[READ_ERROR] {type(exc).__name__}: {exc}"


def try_load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        return {"_load_error": f"{type(exc).__name__}: {exc}"}


def row_has_target_gene(row: dict[str, str]) -> tuple[bool, dict[str, str]]:
    """Return whether row appears to match target gene(s), plus hit columns."""
    hit_cols: dict[str, str] = {}

    for col, value in row.items():
        value_str = str(value).strip()
        col_l = col.lower()

        # Prefer precise gene-symbol-ish columns.
        if col_l in {
            "gene_symbol",
            "symbol",
            "gene",
            "hgnc_symbol",
            "approved_symbol",
            "gene_name",
        } and value_str.upper() in TARGET_GENE_SYMBOLS:
            hit_cols[col] = value_str

    # Fallback text scan only if no precise hit was found.
    if not hit_cols:
        joined = "\t".join(str(v) for v in row.values())
        for target in TARGET_GENE_SYMBOLS:
            if target in joined.split("\t") or target in joined:
                hit_cols["_text_hit"] = target
                break

    return bool(hit_cols), hit_cols


def scan_delimited_for_gene(path: Path, delimiter: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "header": None,
        "row_count_excluding_header": None,
        "gene_like_columns": [],
        "polg_match_count": 0,
        "matches_truncated": False,
        "matches": [],
        "error": None,
    }

    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            result["header"] = reader.fieldnames or []
            result["gene_like_columns"] = [
                c
                for c in (reader.fieldnames or [])
                if any(token in c.lower() for token in ["gene", "symbol", "hgnc", "ensembl", "source"])
            ]

            count = 0
            match_count = 0
            matches: list[dict[str, Any]] = []

            for row in reader:
                count += 1
                is_hit, hit_cols = row_has_target_gene(row)
                if not is_hit:
                    continue

                match_count += 1
                if len(matches) < MAX_MATCHES_PER_FILE:
                    matches.append(
                        {
                            "row_number": count,
                            "match_info": {
                                "gene_column_hits": hit_cols,
                            },
                            "row": row,
                        }
                    )

            result["row_count_excluding_header"] = count
            result["polg_match_count"] = match_count
            result["matches_truncated"] = match_count > len(matches)
            result["matches"] = matches

    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def summarize_artifact(path: Path, root_for_relative: Path) -> dict[str, Any]:
    stat = path.stat()
    kind = file_kind(path)
    rel = path.relative_to(root_for_relative).as_posix()

    item: dict[str, Any] = {
        "relative_path": rel,
        "absolute_path": str(path),
        "kind": kind,
        "size_bytes": stat.st_size,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "sha256": None,
        "content_summary": None,
        "polg_match_count": None,
        "matches_truncated": False,
        "matches": [],
        "error": None,
    }

    if stat.st_size <= MAX_FILE_BYTES_TO_SCAN:
        try:
            item["sha256"] = sha256_file(path)
        except Exception as exc:
            item["sha256"] = f"[HASH_ERROR] {type(exc).__name__}: {exc}"
    else:
        item["sha256"] = "[SKIPPED_HASH_OVER_SCAN_LIMIT]"

    if stat.st_size > MAX_FILE_BYTES_TO_SCAN:
        item["content_summary"] = {
            "skipped": True,
            "skip_reason": f"file larger than {MAX_FILE_BYTES_TO_SCAN} bytes",
        }
        return item

    if kind == "tsv":
        scan = scan_delimited_for_gene(path, "\t")
        item["content_summary"] = {
            "header": scan.get("header"),
            "row_count_excluding_header": scan.get("row_count_excluding_header"),
            "gene_like_columns": scan.get("gene_like_columns"),
        }
        item["polg_match_count"] = scan.get("polg_match_count")
        item["matches_truncated"] = scan.get("matches_truncated")
        item["matches"] = scan.get("matches")
        item["error"] = scan.get("error")

    elif kind == "csv":
        scan = scan_delimited_for_gene(path, ",")
        item["content_summary"] = {
            "header": scan.get("header"),
            "row_count_excluding_header": scan.get("row_count_excluding_header"),
            "gene_like_columns": scan.get("gene_like_columns"),
        }
        item["polg_match_count"] = scan.get("polg_match_count")
        item["matches_truncated"] = scan.get("matches_truncated")
        item["matches"] = scan.get("matches")
        item["error"] = scan.get("error")

    elif kind == "json":
        loaded = try_load_json(path)
        if isinstance(loaded, dict):
            item["content_summary"] = {
                "json_top_level_type": "dict",
                "json_top_level_keys": list(loaded.keys())[:MAX_JSON_TOP_KEYS],
                "json_top_level_key_count": len(loaded.keys()),
            }
        elif isinstance(loaded, list):
            item["content_summary"] = {
                "json_top_level_type": "list",
                "length": len(loaded),
                "first_item_type": type(loaded[0]).__name__ if loaded else None,
            }
        else:
            item["content_summary"] = {
                "json_top_level_type": type(loaded).__name__,
            }

        raw = json.dumps(loaded, ensure_ascii=False)
        matches = []
        for target in TARGET_GENE_SYMBOLS:
            if target in raw:
                matches.append({"target": target, "match_type": "raw_json_text"})
        item["polg_match_count"] = len(matches)
        item["matches"] = matches

    elif kind in {"yaml", "text"}:
        text = safe_read_text(path)
        preview_lines = text.splitlines()[:MAX_TEXT_PREVIEW_LINES]
        matches = []
        for idx, line in enumerate(text.splitlines(), start=1):
            if any(target in line for target in TARGET_GENE_SYMBOLS):
                if len(matches) < MAX_MATCHES_PER_FILE:
                    matches.append({"line_number": idx, "line": line})
        item["content_summary"] = {
            "preview_lines": preview_lines,
        }
        item["polg_match_count"] = len(matches)
        item["matches_truncated"] = len(matches) >= MAX_MATCHES_PER_FILE
        item["matches"] = matches

    return item


def collect_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()

    for root in paths:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path not in seen:
                seen.add(path)
                files.append(path)

    return files


def probe_target(target: dict[str, Any]) -> dict[str, Any]:
    target_paths = [
        target["tep_dir"],
        target["table_dir"],
        target["report_dir"],
    ]

    files = collect_files(target_paths)

    # Use GSC repo root for stable relative paths across TEP/table/report areas.
    reports = [
        summarize_artifact(path, GSC_ROOT)
        for path in files[:MAX_TREE_FILES_PER_TARGET]
    ]

    if len(files) > MAX_TREE_FILES_PER_TARGET:
        reports.append(
            {
                "relative_path": "[TRUNCATED]",
                "absolute_path": str(GSC_ROOT),
                "kind": "truncation_notice",
                "size_bytes": None,
                "mtime_utc": None,
                "sha256": None,
                "content_summary": {
                    "total_files": len(files),
                    "reported_files": MAX_TREE_FILES_PER_TARGET,
                },
                "polg_match_count": None,
                "matches_truncated": True,
                "matches": [],
                "error": None,
            }
        )

    hit_files = [
        {
            "relative_path": item["relative_path"],
            "kind": item["kind"],
            "size_bytes": item["size_bytes"],
            "polg_match_count": item.get("polg_match_count"),
            "matches_truncated": item.get("matches_truncated"),
            "content_summary": item.get("content_summary"),
        }
        for item in reports
        if isinstance(item.get("polg_match_count"), int) and item.get("polg_match_count", 0) > 0
    ]

    total_hits = sum(
        item.get("polg_match_count", 0)
        for item in reports
        if isinstance(item.get("polg_match_count"), int)
    )

    return {
        "phenotype_surface": target["phenotype_surface"],
        "run_id": target["run_id"],
        "paths": {
            "tep_dir": str(target["tep_dir"]),
            "tep_dir_exists": target["tep_dir"].exists(),
            "table_dir": str(target["table_dir"]),
            "table_dir_exists": target["table_dir"].exists(),
            "report_dir": str(target["report_dir"]),
            "report_dir_exists": target["report_dir"].exists(),
        },
        "summary": {
            "files_seen": len(files),
            "files_reported": min(len(files), MAX_TREE_FILES_PER_TARGET),
            "files_with_polg_hits": len(hit_files),
            "total_reported_polg_hits": total_hits,
            "hit_files": hit_files,
        },
        "file_reports": reports,
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# GSC POLG TEP Probe",
        "",
        "## Purpose",
        "",
        "Read-only MARK probe for POLG signals in certified GSC TEP/table/report artifacts.",
        "",
        "## Probe Metadata",
        "",
        f"- Generated at: `{report['probe_metadata']['generated_at_utc']}`",
        f"- GSC root: `{report['paths']['gsc_root']}`",
        f"- GSC root exists: `{report['paths']['gsc_root_exists']}`",
        f"- Output dir: `{report['paths']['output_dir']}`",
        "",
        "## Target Gene Symbols",
        "",
    ]

    for target_gene in sorted(TARGET_GENE_SYMBOLS):
        lines.append(f"- `{target_gene}`")

    lines.append("")

    for target_report in report["target_reports"]:
        lines.extend(
            [
                "---",
                "",
                f"## {target_report['phenotype_surface']}",
                "",
                f"- Run ID: `{target_report['run_id']}`",
                f"- TEP dir: `{target_report['paths']['tep_dir']}`",
                f"- TEP dir exists: `{target_report['paths']['tep_dir_exists']}`",
                f"- Table dir: `{target_report['paths']['table_dir']}`",
                f"- Table dir exists: `{target_report['paths']['table_dir_exists']}`",
                f"- Report dir: `{target_report['paths']['report_dir']}`",
                f"- Report dir exists: `{target_report['paths']['report_dir_exists']}`",
                "",
                "### Summary",
                "",
                f"- Files seen: `{target_report['summary']['files_seen']}`",
                f"- Files reported: `{target_report['summary']['files_reported']}`",
                f"- Files with POLG hits: `{target_report['summary']['files_with_polg_hits']}`",
                f"- Total reported POLG hits: `{target_report['summary']['total_reported_polg_hits']}`",
                "",
                "### Hit Files",
                "",
            ]
        )

        hit_files = target_report["summary"]["hit_files"]
        if not hit_files:
            lines.append("- None detected")
            lines.append("")
        else:
            for hit in hit_files:
                lines.extend(
                    [
                        f"#### `{hit['relative_path']}`",
                        "",
                        f"- Kind: `{hit['kind']}`",
                        f"- Size bytes: `{hit['size_bytes']}`",
                        f"- POLG match count: `{hit['polg_match_count']}`",
                        f"- Matches truncated: `{hit['matches_truncated']}`",
                        "",
                    ]
                )
                content = hit.get("content_summary")
                if isinstance(content, dict):
                    if content.get("row_count_excluding_header") is not None:
                        lines.append(f"- Rows excluding header: `{content.get('row_count_excluding_header')}`")
                    if content.get("gene_like_columns"):
                        lines.append(f"- Gene-like columns: `{content.get('gene_like_columns')}`")
                    lines.append("")

        lines.append("### Match Details")
        lines.append("")

        any_details = False
        for item in target_report["file_reports"]:
            matches = item.get("matches") or []
            if not matches:
                continue

            any_details = True
            lines.extend(
                [
                    f"#### `{item['relative_path']}`",
                    "",
                    f"- SHA256: `{item.get('sha256')}`",
                    "",
                ]
            )

            for match in matches[:MAX_MATCHES_PER_FILE]:
                if "row" in match:
                    lines.append(f"##### Row `{match.get('row_number')}`")
                    lines.append("")
                    lines.append("```json")
                    lines.append(json.dumps(match, indent=2))
                    lines.append("```")
                    lines.append("")
                elif "line" in match:
                    lines.append(f"- Line `{match.get('line_number')}`: `{match.get('line')}`")
                else:
                    lines.append("```json")
                    lines.append(json.dumps(match, indent=2))
                    lines.append("```")
                    lines.append("")

        if not any_details:
            lines.append("- No POLG match details detected.")
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Prime Directive Confirmation",
            "",
            "This probe did not mutate GSC or VDB repository files. It wrote only to:",
            "",
            f"`{OUT_DIR}`",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    target_reports = [probe_target(target) for target in TEP_TARGETS]

    report: dict[str, Any] = {
        "probe_metadata": {
            "probe_name": "probe_gsc_polg_teps",
            "generated_at_utc": utc_now(),
            "prime_directive": "read-only probe; writes only to /root/Desktop/vdb_gsc_polg_tep_probe/",
            "target_gene_symbols": sorted(TARGET_GENE_SYMBOLS),
        },
        "paths": {
            "gsc_root": str(GSC_ROOT),
            "gsc_root_exists": GSC_ROOT.exists(),
            "results_root": str(RESULTS_ROOT),
            "results_root_exists": RESULTS_ROOT.exists(),
            "output_dir": str(OUT_DIR),
        },
        "target_reports": target_reports,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_markdown(report), encoding="utf-8")

    print(f"Wrote JSON report: {OUT_JSON}")
    print(f"Wrote Markdown report: {OUT_MD}")


if __name__ == "__main__":
    main()

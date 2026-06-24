#!/usr/bin/env python3
"""
Read-only MARK probe for POLG signals inside the canonical HG002 TEP-VAP.

Purpose:
    Search lightweight, line-oriented TEP artifacts from the certified HG002
    VAP run for POLG-related records so VDB can author a concrete lifecycle
    exemplar grounded in the actual TEP-VAP payload.

Prime Directive:
    This probe is strictly read-only with respect to VAP/VDB repositories.
    It writes output only to /root/Desktop/vdb_hg002_polg_tep_probe/.

Canonical target:
    VAP repo:
        /root/dev/portfolio_projects/variant_annotation_pipeline

    HG002 run:
        run_2026_06_03_010030

    TEP directory:
        /root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_06_03_010030/tep/
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VAP_ROOT = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
RUN_ID = "run_2026_06_03_010030"
RUN_DIR = VAP_ROOT / "results" / RUN_ID
TEP_DIR = RUN_DIR / "tep"

OUT_DIR = Path("/root/Desktop/vdb_hg002_polg_tep_probe")
OUT_JSON = OUT_DIR / "hg002_polg_tep_probe.json"
OUT_MD = OUT_DIR / "hg002_polg_tep_probe.md"

TARGET_GENE_SYMBOLS = {"POLG"}
TARGET_PATTERN = re.compile(r"\bPOLG\b", re.IGNORECASE)

# Keep this probe lightweight and safe for MARK.
MAX_FILE_SIZE_TO_SCAN_BYTES = 512 * 1024 * 1024
MAX_MATCHES_PER_FILE = 25
MAX_TEXT_PREVIEW_CHARS = 1_000
MAX_JSON_TEXT_CHARS = 25_000
MAX_TOTAL_FILES = 5_000

GENE_LIKE_COLUMN_TOKENS = (
    "gene",
    "symbol",
    "hgnc",
    "ensembl",
    "transcript",
    "canonical",
    "annotation",
    "consequence",
)


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
    if suffix in {".tsv", ".tab"}:
        return "tsv"
    if suffix == ".csv":
        return "csv"
    if suffix in {".md", ".txt", ".log", ".yaml", ".yml"}:
        return "text"
    return suffix.lstrip(".") or "unknown"


def safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def is_probably_text_artifact(path: Path) -> bool:
    return file_kind(path) in {"json", "tsv", "csv", "text"}


def candidate_gene_columns(header: list[str] | None) -> list[str]:
    if not header:
        return []
    cols = []
    for col in header:
        lowered = col.lower()
        if any(token in lowered for token in GENE_LIKE_COLUMN_TOKENS):
            cols.append(col)
    return cols


def row_matches_target(row: list[str], header: list[str] | None) -> tuple[bool, dict[str, Any]]:
    joined = "\t".join(row)
    text_hit = bool(TARGET_PATTERN.search(joined))

    gene_column_hits: dict[str, str] = {}
    if header:
        for idx, col in enumerate(header):
            if idx >= len(row):
                continue
            lowered = col.lower()
            if any(token in lowered for token in GENE_LIKE_COLUMN_TOKENS):
                value = row[idx]
                if TARGET_PATTERN.search(value):
                    gene_column_hits[col] = value

    return text_hit or bool(gene_column_hits), {
        "text_hit": text_hit,
        "gene_column_hits": gene_column_hits,
    }


def scan_delimited_file(path: Path, delimiter: str, root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "relative_path": safe_rel(path, root),
        "absolute_path": str(path),
        "kind": file_kind(path),
        "size_bytes": path.stat().st_size,
        "sha256": None,
        "header": None,
        "gene_like_columns": [],
        "row_count_excluding_header": 0,
        "polg_match_count": 0,
        "matches_truncated": False,
        "matches": [],
        "error": None,
    }

    try:
        result["sha256"] = sha256_file(path)
    except Exception as exc:
        result["sha256"] = f"[HASH_ERROR] {type(exc).__name__}: {exc}"

    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader, None)
            result["header"] = header
            result["gene_like_columns"] = candidate_gene_columns(header)

            for row_number, row in enumerate(reader, start=2):
                result["row_count_excluding_header"] += 1
                matched, match_info = row_matches_target(row, header)
                if not matched:
                    continue

                result["polg_match_count"] += 1
                if len(result["matches"]) < MAX_MATCHES_PER_FILE:
                    record: dict[str, Any] = {
                        "row_number": row_number,
                        "match_info": match_info,
                    }
                    if header and len(header) == len(row):
                        record["row"] = dict(zip(header, row))
                    else:
                        record["row"] = row
                    result["matches"].append(record)
                else:
                    result["matches_truncated"] = True

    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def scan_text_file(path: Path, root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "relative_path": safe_rel(path, root),
        "absolute_path": str(path),
        "kind": file_kind(path),
        "size_bytes": path.stat().st_size,
        "sha256": None,
        "polg_match_count": 0,
        "matches_truncated": False,
        "matches": [],
        "error": None,
    }

    try:
        result["sha256"] = sha256_file(path)
    except Exception as exc:
        result["sha256"] = f"[HASH_ERROR] {type(exc).__name__}: {exc}"

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_number, line in enumerate(f, start=1):
                if not TARGET_PATTERN.search(line):
                    continue

                result["polg_match_count"] += 1
                if len(result["matches"]) < MAX_MATCHES_PER_FILE:
                    result["matches"].append(
                        {
                            "line_number": line_number,
                            "preview": line.strip()[:MAX_TEXT_PREVIEW_CHARS],
                        }
                    )
                else:
                    result["matches_truncated"] = True
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def scan_json_file(path: Path, root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "relative_path": safe_rel(path, root),
        "absolute_path": str(path),
        "kind": "json",
        "size_bytes": path.stat().st_size,
        "sha256": None,
        "json_top_level_type": None,
        "json_top_level_keys": None,
        "polg_match_count": 0,
        "matches_truncated": False,
        "matches": [],
        "error": None,
    }

    try:
        result["sha256"] = sha256_file(path)
    except Exception as exc:
        result["sha256"] = f"[HASH_ERROR] {type(exc).__name__}: {exc}"

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            loaded = json.load(f)

        result["json_top_level_type"] = type(loaded).__name__
        if isinstance(loaded, dict):
            result["json_top_level_keys"] = list(loaded.keys())[:100]

        # Lightweight JSON search. This is intentionally not a full JSONPath
        # crawler because lifecycle needs signals, not complete payload extraction.
        text = json.dumps(loaded, ensure_ascii=False)
        if len(text) > MAX_JSON_TEXT_CHARS:
            searchable = text[:MAX_JSON_TEXT_CHARS]
            truncated_json_text = True
        else:
            searchable = text
            truncated_json_text = False

        matches = list(TARGET_PATTERN.finditer(searchable))
        result["polg_match_count"] = len(matches)
        result["matches_truncated"] = truncated_json_text or len(matches) > MAX_MATCHES_PER_FILE
        for match in matches[:MAX_MATCHES_PER_FILE]:
            start = max(match.start() - 200, 0)
            end = min(match.end() + 200, len(searchable))
            result["matches"].append(
                {
                    "char_start": match.start(),
                    "preview": searchable[start:end],
                }
            )

    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def scan_file(path: Path, root: Path) -> dict[str, Any]:
    kind = file_kind(path)
    if path.stat().st_size > MAX_FILE_SIZE_TO_SCAN_BYTES:
        return {
            "relative_path": safe_rel(path, root),
            "absolute_path": str(path),
            "kind": kind,
            "size_bytes": path.stat().st_size,
            "skipped": True,
            "skip_reason": f"file larger than {MAX_FILE_SIZE_TO_SCAN_BYTES} bytes",
            "polg_match_count": None,
        }

    if kind == "tsv":
        return scan_delimited_file(path, "\t", root)
    if kind == "csv":
        return scan_delimited_file(path, ",", root)
    if kind == "json":
        return scan_json_file(path, root)
    if kind == "text":
        return scan_text_file(path, root)

    return {
        "relative_path": safe_rel(path, root),
        "absolute_path": str(path),
        "kind": kind,
        "size_bytes": path.stat().st_size,
        "skipped": True,
        "skip_reason": "unsupported file kind for POLG text scan",
        "polg_match_count": None,
    }


def discover_candidate_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files = sorted([p for p in root.rglob("*") if p.is_file()])
    return [p for p in files[:MAX_TOTAL_FILES] if is_probably_text_artifact(p)]


def summarize_matches(file_reports: list[dict[str, Any]]) -> dict[str, Any]:
    reports_with_hits = [
        report for report in file_reports
        if isinstance(report.get("polg_match_count"), int) and report["polg_match_count"] > 0
    ]
    return {
        "files_scanned": len(file_reports),
        "files_with_polg_hits": len(reports_with_hits),
        "total_reported_polg_hits": sum(report["polg_match_count"] for report in reports_with_hits),
        "hit_files": [
            {
                "relative_path": report["relative_path"],
                "kind": report.get("kind"),
                "size_bytes": report.get("size_bytes"),
                "polg_match_count": report.get("polg_match_count"),
                "matches_truncated": report.get("matches_truncated"),
                "gene_like_columns": report.get("gene_like_columns"),
                "row_count_excluding_header": report.get("row_count_excluding_header"),
            }
            for report in reports_with_hits
        ],
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# HG002 POLG TEP-VAP Probe",
        "",
        "## Purpose",
        "",
        "Read-only MARK probe for POLG signals in the canonical certified HG002 TEP-VAP.",
        "",
        "## Probe Metadata",
        "",
        f"- Generated at: `{report['probe_metadata']['generated_at_utc']}`",
        f"- VAP root: `{report['paths']['vap_root']}`",
        f"- Run ID: `{report['run']['run_id']}`",
        f"- TEP dir: `{report['paths']['tep_dir']}`",
        f"- TEP dir exists: `{report['paths']['tep_dir_exists']}`",
        "",
        "## Summary",
        "",
        f"- Files scanned: `{report['summary']['files_scanned']}`",
        f"- Files with POLG hits: `{report['summary']['files_with_polg_hits']}`",
        f"- Total reported POLG hits: `{report['summary']['total_reported_polg_hits']}`",
        "",
        "## Hit Files",
        "",
    ]

    if not report["summary"]["hit_files"]:
        lines.append("- No POLG hits detected in scanned text-like TEP artifacts.")
        lines.append("")
    else:
        for hit_file in report["summary"]["hit_files"]:
            lines.append(f"### `{hit_file['relative_path']}`")
            lines.append("")
            lines.append(f"- Kind: `{hit_file.get('kind')}`")
            lines.append(f"- Size bytes: `{hit_file.get('size_bytes')}`")
            lines.append(f"- POLG match count: `{hit_file.get('polg_match_count')}`")
            lines.append(f"- Matches truncated: `{hit_file.get('matches_truncated')}`")
            if hit_file.get("row_count_excluding_header") is not None:
                lines.append(f"- Rows excluding header: `{hit_file.get('row_count_excluding_header')}`")
            if hit_file.get("gene_like_columns"):
                lines.append(f"- Gene-like columns: `{hit_file.get('gene_like_columns')}`")
            lines.append("")

    lines.append("## Match Details")
    lines.append("")

    for file_report in report["file_reports"]:
        if not (isinstance(file_report.get("polg_match_count"), int) and file_report["polg_match_count"] > 0):
            continue

        lines.append(f"### `{file_report['relative_path']}`")
        lines.append("")
        lines.append(f"- SHA256: `{file_report.get('sha256')}`")
        lines.append("")

        for match in file_report.get("matches", []):
            if "row_number" in match:
                lines.append(f"#### Row `{match['row_number']}`")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(match, indent=2)[:8_000])
                lines.append("```")
                lines.append("")
            elif "line_number" in match:
                lines.append(f"- Line `{match['line_number']}`: `{match.get('preview', '')}`")
            else:
                lines.append("```json")
                lines.append(json.dumps(match, indent=2)[:4_000])
                lines.append("```")
                lines.append("")

    lines.extend(
        [
            "## Prime Directive Confirmation",
            "",
            "This probe did not mutate VAP or VDB repository files. It wrote only to:",
            "",
            f"`{OUT_DIR}`",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    candidate_files = discover_candidate_files(TEP_DIR)
    file_reports = [scan_file(path, TEP_DIR) for path in candidate_files]

    report: dict[str, Any] = {
        "probe_metadata": {
            "probe_name": "probe_hg002_polg_tep_vap",
            "generated_at_utc": utc_now(),
            "prime_directive": "read-only probe; writes only to /root/Desktop/vdb_hg002_polg_tep_probe/",
            "target_gene_symbols": sorted(TARGET_GENE_SYMBOLS),
        },
        "paths": {
            "vap_root": str(VAP_ROOT),
            "vap_root_exists": VAP_ROOT.exists(),
            "run_dir": str(RUN_DIR),
            "run_dir_exists": RUN_DIR.exists(),
            "tep_dir": str(TEP_DIR),
            "tep_dir_exists": TEP_DIR.exists(),
            "output_dir": str(OUT_DIR),
        },
        "run": {
            "sample": "HG002",
            "run_id": RUN_ID,
            "depth_category": "hg002",
            "expected_canonical_status": "certified",
        },
        "summary": summarize_matches(file_reports),
        "file_reports": file_reports,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_markdown(report), encoding="utf-8")

    print(f"Wrote JSON report: {OUT_JSON}")
    print(f"Wrote Markdown report: {OUT_MD}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""
Read-only MARK probe for HG002 TEP-VAP lifecycle exemplar inputs.

Purpose:
Collect topology, manifest, entity, lineage, validation, and lightweight
artifact metadata from the canonical certified HG002 VAP TEP.

Prime Directive:
This probe is strictly read-only with respect to VAP/VDB repositories.
It writes output only to /root/Desktop/vdb_hg002_tep_lifecycle_probe/.

Canonical target:
VAP repo:
/root/dev/portfolio_projects/variant_annotation_pipeline

```
HG002 run:
    run_2026_06_03_010030

TEP directory:
    /root/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_06_03_010030/tep/
```

"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VAP_ROOT = Path("/root/dev/portfolio_projects/variant_annotation_pipeline")
RUN_ID = "run_2026_06_03_010030"
RUN_DIR = VAP_ROOT / "results" / RUN_ID
TEP_DIR = RUN_DIR / "tep"

OUT_DIR = Path("/root/Desktop/vdb_hg002_tep_lifecycle_probe")
OUT_JSON = OUT_DIR / "hg002_tep_lifecycle_probe.json"
OUT_MD = OUT_DIR / "hg002_tep_lifecycle_probe.md"

MAX_PREVIEW_BYTES = 16_384
MAX_TREE_FILES = 2_000
MAX_TEXT_PREVIEW_LINES = 40


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read_text(path: Path, max_bytes: int = MAX_PREVIEW_BYTES) -> str:
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


def file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".json"}:
        return "json"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix in {".tsv"}:
        return "tsv"
    if suffix in {".csv"}:
        return "csv"
    if suffix in {".md", ".txt", ".log"}:
        return "text"
    return suffix.lstrip(".") or "unknown"


def count_delimited_rows_and_header(path: Path, delimiter: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "header": None,
        "row_count_excluding_header": None,
        "preview_rows": [],
        "error": None,
    }
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader, None)
            result["header"] = header

            preview = []
            count = 0
            for row in reader:
                count += 1
                if len(preview) < 5:
                    preview.append(row)

            result["row_count_excluding_header"] = count
            result["preview_rows"] = preview
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def summarize_file(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    rel = path.relative_to(root).as_posix()
    kind = file_kind(path)
    summary: dict[str, Any] = {
        "relative_path": rel,
        "absolute_path": str(path),
        "kind": kind,
        "size_bytes": stat.st_size,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "sha256": None,
        "content_summary": None,
    }

    # Hashing very large files can be expensive. For lifecycle topology,
    # record hashes for files <= 512 MB and mark larger files as skipped.
    if stat.st_size <= 512 * 1024 * 1024:
        try:
            summary["sha256"] = sha256_file(path)
        except Exception as exc:
            summary["sha256"] = f"[HASH_ERROR] {type(exc).__name__}: {exc}"
    else:
        summary["sha256"] = "[SKIPPED_LARGE_FILE_OVER_512MB]"

    if kind == "json":
        loaded = try_load_json(path)
        if isinstance(loaded, dict):
            summary["content_summary"] = {
                "json_type": "object",
                "top_level_keys": list(loaded.keys())[:100],
                "top_level_key_count": len(loaded.keys()),
            }
        elif isinstance(loaded, list):
            summary["content_summary"] = {
                "json_type": "array",
                "length": len(loaded),
                "first_item_type": type(loaded[0]).__name__ if loaded else None,
            }
        else:
            summary["content_summary"] = {
                "json_type": type(loaded).__name__,
            }
    elif kind == "tsv":
        summary["content_summary"] = count_delimited_rows_and_header(path, "\t")
    elif kind == "csv":
        summary["content_summary"] = count_delimited_rows_and_header(path, ",")
    elif kind in {"text", "yaml"}:
        text = safe_read_text(path)
        summary["content_summary"] = {
            "preview_lines": text.splitlines()[:MAX_TEXT_PREVIEW_LINES],
        }

    return summary


def collect_tree(root: Path) -> list[dict[str, Any]]:
    files = []
    if not root.exists():
        return files

    all_files = sorted([p for p in root.rglob("*") if p.is_file()])
    for path in all_files[:MAX_TREE_FILES]:
        files.append(summarize_file(path, root))

    if len(all_files) > MAX_TREE_FILES:
        files.append(
            {
                "relative_path": "[TRUNCATED]",
                "absolute_path": str(root),
                "kind": "truncation_notice",
                "size_bytes": None,
                "mtime_utc": None,
                "sha256": None,
                "content_summary": {
                    "total_files": len(all_files),
                    "reported_files": MAX_TREE_FILES,
                },
            }
        )
    return files


def find_named_artifacts(root: Path) -> dict[str, list[str]]:
    patterns = {
    "entity_inventory": ["*entity*inventory*.json", "*entity*inventory*.md"],
    "lineage_manifest": ["*lineage*manifest*.json", "*lineage*manifest*.md"],
    "validation_report": ["*validation*report*.json", "*validation*report*.md", "*validation*.md"],
    "manifest": ["*manifest*.json", "*manifest*.yaml", "*manifest*.yml", "*manifest*.md"],
    "stage_artifacts": ["*stage*"],
    "tsv_artifacts": ["*.tsv"],
    "json_artifacts": ["*.json"],
    }

    found: dict[str, list[str]] = {}
    if not root.exists():
        return found

    for label, globs in patterns.items():
        hits: list[str] = []
        for pattern in globs:
            hits.extend([p.relative_to(root).as_posix() for p in root.rglob(pattern) if p.is_file()])
        found[label] = sorted(set(hits))
    return found


def summarize_run_sidecars(run_dir: Path) -> dict[str, Any]:
    candidates = [
                    run_dir / "metadata",
                    run_dir / "reports",
                    run_dir / "validation",
                    run_dir / "final",
                    run_dir / "processed",
    ]
    output: dict[str, Any] = {}
    for candidate in candidates:
        if candidate.exists():
            files = sorted([p for p in candidate.rglob("*") if p.is_file()])
            output[candidate.name] = {
                "path": str(candidate),
                "file_count": len(files),
                "sample_files": [p.relative_to(candidate).as_posix() for p in files[:50]],
            }
        else:
            output[candidate.name] = {
                "path": str(candidate),
                "exists": False,
            }
    return output


def build_markdown(report: dict[str, Any]) -> str:
    tep_exists = report["paths"]["tep_dir_exists"]
    files = report.get("tep_tree", [])
    named = report.get("named_artifacts", {})

    lines = [
        "# HG002 TEP-VAP Lifecycle Probe",
        "",
        "## Purpose",
        "",
        "Read-only MARK probe for authoring `docs/examples/vdb_evidence_lifecycle_example.md`.",
        "",
        "## Probe Metadata",
        "",
        f"- Generated at: `{report['probe_metadata']['generated_at_utc']}`",
        f"- VAP root: `{report['paths']['vap_root']}`",
        f"- Run ID: `{report['run']['run_id']}`",
        f"- TEP dir: `{report['paths']['tep_dir']}`",
        f"- TEP dir exists: `{tep_exists}`",
        "",
        "## TEP Artifact Summary",
        "",
        f"- File count reported: `{len(files)}`",
        "",
        "## Named Artifact Groups",
        "",
    ]

    for label, hits in named.items():
        lines.append(f"### {label}")
        lines.append("")
        if hits:
            for hit in hits[:100]:
                lines.append(f"- `{hit}`")
            if len(hits) > 100:
                lines.append(f"- `[TRUNCATED: {len(hits) - 100} additional]`")
        else:
            lines.append("- None detected")
        lines.append("")

    lines.extend(
        [
            "## TEP Tree File Summaries",
            "",
        ]
    )

    for item in files:
        lines.append(f"### `{item['relative_path']}`")
        lines.append("")
        lines.append(f"- Kind: `{item.get('kind')}`")
        lines.append(f"- Size bytes: `{item.get('size_bytes')}`")
        lines.append(f"- SHA256: `{item.get('sha256')}`")
        content = item.get("content_summary")
        if isinstance(content, dict):
            if "top_level_keys" in content:
                lines.append(f"- JSON top-level keys: `{content.get('top_level_keys')}`")
            if "header" in content:
                lines.append(f"- Header: `{content.get('header')}`")
                lines.append(f"- Rows excluding header: `{content.get('row_count_excluding_header')}`")
            if "preview_lines" in content:
                lines.append("- Preview:")
                lines.append("")
                lines.append("```text")
                lines.extend(content.get("preview_lines", [])[:20])
                lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Run Sidecar Summary",
            "",
            "```json",
            json.dumps(report.get("run_sidecars", {}), indent=2),
            "```",
            "",
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

    report: dict[str, Any] = {
        "probe_metadata": {
            "probe_name": "probe_hg002_tep_vap_lifecycle_inputs",
            "generated_at_utc": utc_now(),
            "prime_directive": "read-only probe; writes only to /root/Desktop/vdb_hg002_tep_lifecycle_probe/",
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
        "named_artifacts": find_named_artifacts(TEP_DIR),
        "tep_tree": collect_tree(TEP_DIR),
        "run_sidecars": summarize_run_sidecars(RUN_DIR),
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_markdown(report), encoding="utf-8")

    print(f"Wrote JSON report: {OUT_JSON}")
    print(f"Wrote Markdown report: {OUT_MD}")


if __name__ == "__main__":
    main()

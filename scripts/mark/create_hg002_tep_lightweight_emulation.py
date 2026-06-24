#!/usr/bin/env python3
"""
Create a lightweight emulation copy of the certified HG002 TEP-VAP.

This script is read-only with respect to the canonical VAP run.
It writes only to /root/Desktop/.

Canonical source:
    /root/dev/portfolio_projects/variant_annotation_pipeline/
    results/run_2026_06_03_010030/tep/
    vap_tep_HG002_run_2026_06_03_010030_v1

Output:
    /root/Desktop/vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_TEP_ROOT = Path(
    "/root/dev/portfolio_projects/variant_annotation_pipeline/"
    "results/run_2026_06_03_010030/tep/"
    "vap_tep_HG002_run_2026_06_03_010030_v1"
)

OUTPUT_ROOT = Path(
    "/root/Desktop/"
    "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
)

REPORT_JSON = OUTPUT_ROOT / "_emulation_manifest.json"
REPORT_MD = OUTPUT_ROOT / "_emulation_report.md"

TARGET_GENE_SYMBOLS = {"POLG"}
TARGET_GENE_IDS = {"ENSG00000140521"}
TARGET_VARIANT_FRAGMENTS = {"15:89333596:T:TTGC", "89333596"}

MAX_PRIORITY_ROWS_PER_TSV = 25
MAX_FALLBACK_ROWS_PER_TSV = 20
MAX_CONTEXT_COPY_BYTES = 10 * 1024 * 1024

EXPECTED_FILES = [
    "entity_inventory.json",
    "lineage_manifest.json",
    "validation_report.md",
    "entities/context/stage_13_artifact_manifest.json",
    "entities/context/stage_13_final_summary.json",
    "entities/context/stage_13_run_report.md",
    "entities/coding_interpretation/stage_09_coding_interpreted.tsv",
    "entities/noncoding_interpretation/stage_10_noncoding_interpreted.tsv",
    "entities/normalization/stage_08_selected_transcript_consequences.tsv",
    "entities/normalization/stage_08_vdb_ready_variants.tsv",
    "entities/observation/HG002_run_2026_06_03_010030.annotated_variants.tsv",
    "entities/prioritization/stage_11_prioritized_variants.tsv",
    "entities/routing/coding_candidates.tsv",
    "entities/routing/noncoding_candidates.tsv",
    "entities/routing/splice_region_candidates.tsv",
    "entities/validation/stage_12_validation_candidates.tsv",
]


@dataclass(frozen=True)
class FileEmulationRecord:
    relative_path: str
    source_exists: bool
    source_size_bytes: int | None
    output_exists: bool
    output_size_bytes: int | None
    mode: str
    header_columns: list[str]
    source_rows_scanned: int | None
    output_rows_written: int | None
    priority_rows_written: int | None
    fallback_rows_written: int | None
    source_sha256: str | None
    output_sha256: str | None
    notes: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_unlink_or_rmtree(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def row_text(row: dict[str, str]) -> str:
    return "\t".join(str(v) for v in row.values())


def row_is_priority(row: dict[str, str]) -> bool:
    for key, value in row.items():
        key_l = key.lower()
        value_s = str(value).strip()

        if key_l in {"gene_symbol", "symbol", "gene", "hgnc_symbol", "approved_symbol"}:
            if value_s.upper() in TARGET_GENE_SYMBOLS:
                return True

        if key_l in {"gene_id", "ensembl_gene_id", "ensembl_id"}:
            if value_s in TARGET_GENE_IDS:
                return True

    joined = row_text(row)

    if any(gene_id in joined for gene_id in TARGET_GENE_IDS):
        return True

    if any(fragment in joined for fragment in TARGET_VARIANT_FRAGMENTS):
        return True

    fields = [str(v).strip().upper() for v in row.values()]
    if "POLG" in fields:
        return True

    return False


def copy_small_file(source: Path, output: Path, rel: str) -> FileEmulationRecord:
    notes: list[str] = []
    ensure_parent(output)

    source_size = source.stat().st_size
    if source_size > MAX_CONTEXT_COPY_BYTES:
        notes.append(f"small-copy skipped: source larger than {MAX_CONTEXT_COPY_BYTES} bytes")
        output.write_text(
            f"[EMULATION PLACEHOLDER]\nSource file too large for intact copy: {rel}\n",
            encoding="utf-8",
        )
        mode = "placeholder_large_non_tsv"
    else:
        shutil.copy2(source, output)
        mode = "copy_intact"

    return FileEmulationRecord(
        relative_path=rel,
        source_exists=True,
        source_size_bytes=source_size,
        output_exists=output.exists(),
        output_size_bytes=output.stat().st_size if output.exists() else None,
        mode=mode,
        header_columns=[],
        source_rows_scanned=None,
        output_rows_written=None,
        priority_rows_written=None,
        fallback_rows_written=None,
        source_sha256=sha256_file(source),
        output_sha256=sha256_file(output) if output.exists() else None,
        notes=notes,
    )


def slice_tsv(source: Path, output: Path, rel: str) -> FileEmulationRecord:
    notes: list[str] = []
    ensure_parent(output)

    source_size = source.stat().st_size
    priority_rows: list[dict[str, str]] = []
    fallback_rows: list[dict[str, str]] = []
    source_rows_scanned = 0
    header_columns: list[str] = []

    with source.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        header_columns = list(reader.fieldnames or [])

        if not header_columns:
            notes.append("no header detected")
            output.write_text("", encoding="utf-8")
            return FileEmulationRecord(
                relative_path=rel,
                source_exists=True,
                source_size_bytes=source_size,
                output_exists=output.exists(),
                output_size_bytes=output.stat().st_size if output.exists() else None,
                mode="tsv_empty_or_no_header",
                header_columns=[],
                source_rows_scanned=0,
                output_rows_written=0,
                priority_rows_written=0,
                fallback_rows_written=0,
                source_sha256=sha256_file(source),
                output_sha256=sha256_file(output) if output.exists() else None,
                notes=notes,
            )

        for row in reader:
            source_rows_scanned += 1

            if row_is_priority(row):
                if len(priority_rows) < MAX_PRIORITY_ROWS_PER_TSV:
                    priority_rows.append(row)
                continue

            if len(fallback_rows) < MAX_FALLBACK_ROWS_PER_TSV:
                fallback_rows.append(row)

    output_rows = priority_rows + fallback_rows

    with output.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.DictWriter(
            out_handle,
            fieldnames=header_columns,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)

    if not priority_rows:
        notes.append("no POLG / ENSG00000140521 priority rows detected")
    else:
        notes.append(f"priority rows captured: {len(priority_rows)}")

    notes.append(f"fallback rows captured: {len(fallback_rows)}")

    return FileEmulationRecord(
        relative_path=rel,
        source_exists=True,
        source_size_bytes=source_size,
        output_exists=output.exists(),
        output_size_bytes=output.stat().st_size if output.exists() else None,
        mode="tsv_header_priority_and_fallback_slice",
        header_columns=header_columns,
        source_rows_scanned=source_rows_scanned,
        output_rows_written=len(output_rows),
        priority_rows_written=len(priority_rows),
        fallback_rows_written=len(fallback_rows),
        source_sha256=sha256_file(source),
        output_sha256=sha256_file(output),
        notes=notes,
    )


def make_missing_placeholder(output: Path, rel: str) -> FileEmulationRecord:
    ensure_parent(output)
    output.write_text(
        f"[EMULATION PLACEHOLDER]\nSource file missing in canonical TEP: {rel}\n",
        encoding="utf-8",
    )

    return FileEmulationRecord(
        relative_path=rel,
        source_exists=False,
        source_size_bytes=None,
        output_exists=output.exists(),
        output_size_bytes=output.stat().st_size,
        mode="missing_source_placeholder",
        header_columns=[],
        source_rows_scanned=None,
        output_rows_written=None,
        priority_rows_written=None,
        fallback_rows_written=None,
        source_sha256=None,
        output_sha256=sha256_file(output),
        notes=["source missing"],
    )


def emulate_file(rel: str) -> FileEmulationRecord:
    source = SOURCE_TEP_ROOT / rel
    output = OUTPUT_ROOT / rel

    if not source.exists():
        return make_missing_placeholder(output, rel)

    if source.suffix.lower() == ".tsv":
        return slice_tsv(source, output, rel)

    return copy_small_file(source, output, rel)


def write_report(records: list[FileEmulationRecord]) -> None:
    manifest: dict[str, Any] = {
        "emulation_manifest_version": "1.0",
        "created_at_utc": utc_now(),
        "source_tep_root": str(SOURCE_TEP_ROOT),
        "output_root": str(OUTPUT_ROOT),
        "prime_directive": (
            "Read-only with respect to canonical HG002 TEP; writes only to /root/Desktop."
        ),
        "target_gene_symbols": sorted(TARGET_GENE_SYMBOLS),
        "target_gene_ids": sorted(TARGET_GENE_IDS),
        "target_variant_fragments": sorted(TARGET_VARIANT_FRAGMENTS),
        "file_count": len(records),
        "records": [asdict(record) for record in records],
    }

    REPORT_JSON.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines: list[str] = [
        "# HG002 TEP-VAP Lightweight Emulation Report",
        "",
        "## Purpose",
        "",
        "Create a lightweight, structure-faithful emulation copy of the certified HG002 TEP-VAP.",
        "",
        "## Source",
        "",
        f"`{SOURCE_TEP_ROOT}`",
        "",
        "## Output",
        "",
        f"`{OUTPUT_ROOT}`",
        "",
        "## Prime Directive",
        "",
        "The canonical source TEP was treated as read-only. This script writes only to `/root/Desktop/`.",
        "",
        "## Priority Targets",
        "",
        "- Gene symbol: `POLG`",
        "- Gene ID: `ENSG00000140521`",
        "- Variant fragments: `15:89333596:T:TTGC`, `89333596`",
        "",
        "## File Summary",
        "",
        "| Relative path | Mode | Source rows scanned | Output rows | Priority rows | Notes |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record.relative_path}`",
                    record.mode,
                    "" if record.source_rows_scanned is None else str(record.source_rows_scanned),
                    "" if record.output_rows_written is None else str(record.output_rows_written),
                    "" if record.priority_rows_written is None else str(record.priority_rows_written),
                    "; ".join(record.notes),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Recommended sys76 Destination",
            "",
            "Copy this output folder into VDB as a local-only fixture or developer fixture, for example:",
            "",
            "```text",
            "tests/fixtures/tep_vap_hg002_lightweight/",
            "```",
            "",
            "Do not treat this emulator as biological evidence. It is a topology-preserving development fixture.",
            "",
        ]
    )

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not SOURCE_TEP_ROOT.exists():
        print(f"ERROR: source TEP root does not exist: {SOURCE_TEP_ROOT}")
        return 1

    if not SOURCE_TEP_ROOT.is_dir():
        print(f"ERROR: source TEP root is not a directory: {SOURCE_TEP_ROOT}")
        return 1

    safe_unlink_or_rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    records = [emulate_file(rel) for rel in EXPECTED_FILES]
    write_report(records)

    total_output_bytes = sum(record.output_size_bytes or 0 for record in records)
    priority_total = sum(record.priority_rows_written or 0 for record in records)

    print("HG002 TEP-VAP lightweight emulation complete")
    print(f"Source: {SOURCE_TEP_ROOT}")
    print(f"Output: {OUTPUT_ROOT}")
    print(f"Files emulated: {len(records)}")
    print(f"Total output bytes across emulated files: {total_output_bytes}")
    print(f"Priority POLG/ENSG rows captured across TSVs: {priority_total}")
    print(f"Manifest: {REPORT_JSON}")
    print(f"Report: {REPORT_MD}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

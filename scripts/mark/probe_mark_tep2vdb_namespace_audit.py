#!/usr/bin/env python3
"""Read-only MARK probe for Tier 2 TEP-to-VDB namespace provenance audit.

This probe is intentionally conservative:

* It writes only to the configured probe output directory.
* It reads VAP TEP directories and VDB registration SQLite databases.
* SQLite databases are opened in read-only URI mode with PRAGMA query_only=ON.
* It inventories schemas, TSV headers, and compact VDB handle references.
* It does not query external services, perform identifier mediation, mutate inputs,
  scan complete multi-GB TSVs, or expand source identity sets.

Run from MARK's VDB repository root, for example:

    PYTHONPATH=src:. python scripts/mark/probe_mark_tep2vdb_namespace_audit.py

Default output:

    results/phase4/namespace_audit/mark_phase4_corpus_6tep_v1_tep2vdb_audit_v1/probe/
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CORPUS_ID = "mark_phase4_corpus_6tep_v1"
AUDIT_ID = "mark_phase4_corpus_6tep_v1_tep2vdb_audit_v1"
DEFAULT_OUT_DIR = Path("results/phase4/namespace_audit") / AUDIT_ID / "probe"
DEFAULT_VAP_REPO = Path("~/dev/portfolio_projects/variant_annotation_pipeline").expanduser()

REGISTERED_CANONICAL_SQLITES = [
    ("vap_hg002", "VAP", "HG002 / SRR12898354", Path("results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite")),
    ("vap_median_ERR10619300", "VAP", "ERR10619300", Path("results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite")),
    ("vap_q1_ERR10619212", "VAP", "ERR10619212", Path("results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite")),
    ("vap_q3_ERR10619225", "VAP", "ERR10619225", Path("results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite")),
    ("gsc_epilepsy", "GSC", "epilepsy", Path("results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite")),
    ("gsc_mitochondrial_disease", "GSC", "mitochondrial_disease", Path("results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite")),
]

VAP_RUNS = [
    {"sra_id": "ERR10619203", "tep_label": "ERR10619203", "run_id": "run_2026_05_30_071639", "depth_category": "q3", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619207", "tep_label": "ERR10619207", "run_id": "run_2026_06_01_124134", "depth_category": "q3", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619208", "tep_label": "ERR10619208", "run_id": "run_2026_05_30_151355", "depth_category": "median", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619212", "tep_label": "ERR10619212", "run_id": "run_2026_05_30_214724", "depth_category": "q1", "in_current_6tep_corpus": "true"},
    {"sra_id": "ERR10619225", "tep_label": "ERR10619225", "run_id": "run_2026_05_31_091242", "depth_category": "q3", "in_current_6tep_corpus": "true"},
    {"sra_id": "ERR10619230", "tep_label": "ERR10619230", "run_id": "run_2026_06_01_004903", "depth_category": "q3", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619241", "tep_label": "ERR10619241", "run_id": "run_2026_06_02_052302", "depth_category": "q1", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619281", "tep_label": "ERR10619281", "run_id": "run_2026_05_27_233524", "depth_category": "median", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619285", "tep_label": "ERR10619285", "run_id": "run_2026_06_02_124300", "depth_category": "median", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619300", "tep_label": "ERR10619300", "run_id": "run_2026_05_27_172531", "depth_category": "median", "in_current_6tep_corpus": "true"},
    {"sra_id": "ERR10619309", "tep_label": "ERR10619309", "run_id": "run_2026_06_02_181024", "depth_category": "q1", "in_current_6tep_corpus": "false"},
    {"sra_id": "ERR10619330", "tep_label": "ERR10619330", "run_id": "run_2026_06_01_203130", "depth_category": "q1", "in_current_6tep_corpus": "false"},
    {"sra_id": "SRR12898354", "tep_label": "HG002", "run_id": "run_2026_06_03_010030", "depth_category": "hg002", "in_current_6tep_corpus": "true"},
]

ROUTE_KEYWORDS = {
    "coordinate_or_variant": [
        "chrom", "chromosome", "contig", "chr", "pos", "position", "start", "end", "stop",
        "ref", "alt", "allele", "variant", "vcf", "locus", "coordinate", "genomic",
        "reference_build", "assembly", "build", "normalization", "variant_type",
    ],
    "feature_or_interval": [
        "transcript", "feature", "feature_type", "consequence", "impact", "exon", "intron",
        "utr", "splice", "regulatory", "enhancer", "promoter", "biotype", "hgvsc", "hgvsp",
    ],
    "gene": [
        "gene", "symbol", "ensembl", "ensg", "entrez", "ncbi", "hgnc", "alias",
    ],
    "phenotype_or_overlay": [
        "phenotype", "disease", "hpo", "mondo", "omim", "trait", "channel", "semantic",
    ],
    "producer_or_observation": [
        "sample", "run", "release", "artifact", "manifest", "source", "producer", "provenance",
        "registration", "corpus", "tep", "package", "sra", "study", "execution",
    ],
}

@dataclass(frozen=True)
class Args:
    vdb_repo: Path
    vap_repo: Path
    out_dir: Path
    include_all_vap_headers: bool
    count_sqlite_rows: bool


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel_or_abs(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field) for field in fieldnames})


def read_tsv_header(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            first = handle.readline()
    except Exception:
        return []
    if not first:
        return []
    return first.rstrip("\n\r").split("\t")


def classify_column(name: str) -> str:
    lower = name.lower()
    matched: list[str] = []
    for route, keywords in ROUTE_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            matched.append(route)
    if not matched:
        return "unclassified"
    # Preserve deterministic route ordering by ROUTE_KEYWORDS insertion order.
    return ";".join(matched)


def classify_columns(columns: Iterable[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for column in columns:
        route = classify_column(column)
        if route == "unclassified":
            continue
        for part in route.split(";"):
            out[part].append(column)
    return dict(out)


def pipe(values: Iterable[str]) -> str:
    return "|".join(str(v) for v in values if str(v) != "")


def expected_vap_tep_dir(vap_repo: Path, run: dict[str, str]) -> Path:
    return vap_repo / "results" / run["run_id"] / "tep" / f"vap_tep_{run['tep_label']}_{run['run_id']}_v1"


def collect_vap_tep_inventory(args: Args) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    inventory: list[dict[str, Any]] = []
    artifact_rows: list[dict[str, Any]] = []
    header_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []

    for run in VAP_RUNS:
        tep_dir = expected_vap_tep_dir(args.vap_repo, run)
        exists = tep_dir.exists()
        files = sorted([p for p in tep_dir.rglob("*") if p.is_file()]) if exists else []
        tsv_files = [p for p in files if p.suffix.lower() == ".tsv"]
        key_files = {
            "entity_inventory": tep_dir / "entity_inventory.json",
            "lineage_manifest": tep_dir / "lineage_manifest.json",
            "validation_report": tep_dir / "validation_report.md",
            "stage_13_artifact_manifest": tep_dir / "entities" / "context" / "stage_13_artifact_manifest.json",
            "stage_13_final_summary": tep_dir / "entities" / "context" / "stage_13_final_summary.json",
        }

        inventory.append({
            **run,
            "expected_tep_dir": str(tep_dir),
            "tep_dir_exists": str(exists).lower(),
            "file_count": len(files),
            "tsv_count": len(tsv_files),
            "total_size_bytes": sum(p.stat().st_size for p in files) if files else 0,
            "entity_inventory_exists": str(key_files["entity_inventory"].exists()).lower(),
            "lineage_manifest_exists": str(key_files["lineage_manifest"].exists()).lower(),
            "validation_report_exists": str(key_files["validation_report"].exists()).lower(),
            "stage_13_artifact_manifest_exists": str(key_files["stage_13_artifact_manifest"].exists()).lower(),
            "stage_13_final_summary_exists": str(key_files["stage_13_final_summary"].exists()).lower(),
            "audit_status": "present" if exists else "missing_tep_dir",
        })

        for p in files:
            rel = rel_or_abs(p, tep_dir)
            artifact_rows.append({
                **run,
                "tep_dir": str(tep_dir),
                "relative_path": rel,
                "absolute_path": str(p),
                "suffix": p.suffix.lower(),
                "size_bytes": p.stat().st_size,
                "artifact_lane": classify_artifact_lane(rel),
            })

        # Headers for all current corpus TEPs by default; optional all-13 headers.
        if args.include_all_vap_headers or run["in_current_6tep_corpus"] == "true":
            for p in tsv_files:
                columns = read_tsv_header(p)
                classes = classify_columns(columns)
                rel = rel_or_abs(p, tep_dir)
                header_rows.append({
                    **run,
                    "tep_dir": str(tep_dir),
                    "relative_path": rel,
                    "absolute_path": str(p),
                    "size_bytes": p.stat().st_size,
                    "column_count": len(columns),
                    "columns": pipe(columns),
                    "coordinate_or_variant_columns": pipe(classes.get("coordinate_or_variant", [])),
                    "feature_or_interval_columns": pipe(classes.get("feature_or_interval", [])),
                    "gene_columns": pipe(classes.get("gene", [])),
                    "phenotype_or_overlay_columns": pipe(classes.get("phenotype_or_overlay", [])),
                    "producer_or_observation_columns": pipe(classes.get("producer_or_observation", [])),
                    "audit_status": "header_read" if columns else "header_missing_or_unreadable",
                })
                for column in columns:
                    route = classify_column(column)
                    if route == "unclassified":
                        continue
                    candidate_rows.append({
                        **run,
                        "tep_relative_path": rel,
                        "column_name": column,
                        "candidate_routes": route,
                    })

    return inventory, artifact_rows, header_rows, candidate_rows


def classify_artifact_lane(relative_path: str) -> str:
    lower = relative_path.lower()
    if "/observation/" in f"/{lower}":
        return "observation"
    if "/normalization/" in f"/{lower}":
        return "normalization"
    if "/coding_interpretation/" in f"/{lower}":
        return "coding_interpretation"
    if "/noncoding_interpretation/" in f"/{lower}":
        return "noncoding_interpretation"
    if "/routing/" in f"/{lower}":
        return "routing"
    if "/prioritization/" in f"/{lower}":
        return "prioritization"
    if "/validation/" in f"/{lower}":
        return "validation"
    if "/context/" in f"/{lower}":
        return "context"
    if lower.endswith("entity_inventory.json"):
        return "entity_inventory"
    if lower.endswith("lineage_manifest.json"):
        return "lineage_manifest"
    return "other"


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def open_sqlite_readonly(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only=ON")
    return conn


def collect_sqlite_probe(args: Args) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    db_rows: list[dict[str, Any]] = []
    table_rows: list[dict[str, Any]] = []
    column_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []

    # Include known canonical DBs plus any other vdb.sqlite found under results/registration.
    known_by_path: dict[Path, tuple[str, str, str]] = {}
    for db_key, producer, corpus_member, rel_path in REGISTERED_CANONICAL_SQLITES:
        known_by_path[(args.vdb_repo / rel_path).resolve()] = (db_key, producer, corpus_member)

    registration_root = args.vdb_repo / "results" / "registration"
    discovered_paths = sorted(registration_root.rglob("vdb.sqlite")) if registration_root.exists() else []
    for p in discovered_paths:
        rp = p.resolve()
        if rp not in known_by_path:
            db_key = rel_or_abs(p.parent, registration_root).replace("/", "_").replace("\\", "_") or p.parent.name
            producer = "GSC" if "gsc" in str(p).lower() else "VAP" if "vap" in str(p).lower() else "unknown"
            known_by_path[rp] = (db_key, producer, "discovered_noncanonical_or_legacy")

    for abs_path in sorted(known_by_path):
        db_key, producer, corpus_member = known_by_path[abs_path]
        exists = abs_path.exists()
        row = {
            "db_key": db_key,
            "producer": producer,
            "corpus_member": corpus_member,
            "sqlite_path": str(abs_path),
            "exists": str(exists).lower(),
            "size_bytes": abs_path.stat().st_size if exists else 0,
            "connection_status": "not_attempted",
            "sqlite_page_count": "",
            "sqlite_page_size": "",
            "table_count": 0,
            "view_count": 0,
            "audit_status": "missing" if not exists else "pending",
        }
        if not exists:
            db_rows.append(row)
            continue

        try:
            with open_sqlite_readonly(abs_path) as conn:
                row["connection_status"] = "connected_readonly"
                row["sqlite_page_count"] = pragma_scalar(conn, "page_count")
                row["sqlite_page_size"] = pragma_scalar(conn, "page_size")
                objects = conn.execute(
                    "SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' ORDER BY type, name"
                ).fetchall()
                row["table_count"] = sum(1 for _, typ in objects if typ == "table")
                row["view_count"] = sum(1 for _, typ in objects if typ == "view")
                row["audit_status"] = "schema_read"

                for table_name, object_type in objects:
                    columns = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})").fetchall()
                    column_names = [c[1] for c in columns]
                    classes = classify_columns(column_names)
                    count_status = "not_requested"
                    row_count = ""
                    if args.count_sqlite_rows and object_type == "table":
                        try:
                            row_count = conn.execute(f"SELECT COUNT(*) FROM {quote_identifier(table_name)}").fetchone()[0]
                            count_status = "counted"
                        except Exception as exc:  # noqa: BLE001
                            count_status = f"count_failed:{type(exc).__name__}"
                    table_rows.append({
                        "db_key": db_key,
                        "producer": producer,
                        "corpus_member": corpus_member,
                        "object_type": object_type,
                        "table_name": table_name,
                        "column_count": len(columns),
                        "row_count": row_count,
                        "row_count_status": count_status,
                        "coordinate_or_variant_columns": pipe(classes.get("coordinate_or_variant", [])),
                        "feature_or_interval_columns": pipe(classes.get("feature_or_interval", [])),
                        "gene_columns": pipe(classes.get("gene", [])),
                        "phenotype_or_overlay_columns": pipe(classes.get("phenotype_or_overlay", [])),
                        "producer_or_observation_columns": pipe(classes.get("producer_or_observation", [])),
                        "all_columns": pipe(column_names),
                    })
                    for cid, name, col_type, notnull, default, pk in columns:
                        route = classify_column(name)
                        col_row = {
                            "db_key": db_key,
                            "producer": producer,
                            "corpus_member": corpus_member,
                            "table_name": table_name,
                            "object_type": object_type,
                            "column_ordinal": cid,
                            "column_name": name,
                            "column_type": col_type,
                            "notnull": notnull,
                            "pk": pk,
                            "candidate_routes": route,
                        }
                        column_rows.append(col_row)
                        if route != "unclassified":
                            candidate_rows.append(col_row)
        except Exception as exc:  # noqa: BLE001
            row["connection_status"] = f"connection_failed:{type(exc).__name__}:{exc}"
            row["audit_status"] = "connection_failed"
        db_rows.append(row)

    return db_rows, table_rows, column_rows, candidate_rows


def pragma_scalar(conn: sqlite3.Connection, name: str) -> str:
    try:
        return str(conn.execute(f"PRAGMA {name}").fetchone()[0])
    except Exception:  # noqa: BLE001
        return ""


def collect_compact_handle_probe(args: Args) -> list[dict[str, Any]]:
    path = args.vdb_repo / "results" / "phase4" / "assertion_records" / CORPUS_ID / "assertion_record_source_identity_sets.tsv"
    if not path.exists():
        return [{
            "source_identity_set_id": "",
            "producer": "",
            "identity_route": "",
            "source_namespace": "",
            "source_identity_table_reference": "",
            "source_identity_filter": "",
            "source_identity_count": "",
            "audit_status": "missing_assertion_record_source_identity_sets",
        }]
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            source_namespace = row.get("source_namespace", "")
            text = " ".join([source_namespace, row.get("identity_kind", ""), row.get("participant_role", "")]).lower()
            if "vap" in text:
                producer = "VAP"
            elif "gsc" in text:
                producer = "GSC"
            else:
                producer = "unknown"
            rows.append({
                "source_identity_set_id": row.get("source_identity_set_id", ""),
                "assertion_id": row.get("assertion_id", ""),
                "source_assertion_registration_id": row.get("source_assertion_registration_id", ""),
                "producer": producer,
                "identity_route": route_from_namespace_row(row),
                "identity_kind": row.get("identity_kind", ""),
                "participant_role": row.get("participant_role", ""),
                "source_namespace": source_namespace,
                "source_identity_table_reference": row.get("source_identity_table_reference", ""),
                "source_identity_filter": row.get("source_identity_filter", ""),
                "source_identity_count": row.get("source_identity_count", ""),
                "lossiness_status": row.get("lossiness_status", ""),
                "resolution_status": row.get("resolution_status", ""),
                "source_identity_set_status": row.get("source_identity_set_status", ""),
                "audit_status": "compact_handle_loaded",
            })
    return rows


def route_from_namespace_row(row: dict[str, str]) -> str:
    text = " ".join([row.get("source_namespace", ""), row.get("identity_kind", ""), row.get("participant_role", "")]).lower()
    if any(token in text for token in ["variant", "coordinate", "allele", "locus"]):
        return "coordinate_or_variant"
    if any(token in text for token in ["transcript", "feature", "interval", "exon", "intron", "utr", "regulatory"]):
        return "feature_or_interval"
    if "gene" in text or "ensembl" in text or "hgnc" in text or "ncbi" in text:
        return "gene"
    if "phenotype" in text or "disease" in text:
        return "phenotype_or_overlay"
    if any(token in text for token in ["sample", "source", "provenance", "channel", "run", "release"]):
        return "producer_or_observation"
    return "unknown_or_deferred"


def write_report(args: Args, outputs: dict[str, list[dict[str, Any]]]) -> None:
    lines: list[str] = []
    lines.append("# MARK Probe — Tier 2 TEP-to-VDB Namespace Audit")
    lines.append("")
    lines.append(f"audit_id: `{AUDIT_ID}`")
    lines.append(f"corpus_id: `{CORPUS_ID}`")
    lines.append(f"generated_utc: `{utc_now()}`")
    lines.append(f"vdb_repo: `{args.vdb_repo}`")
    lines.append(f"vap_repo: `{args.vap_repo}`")
    lines.append(f"probe_output_dir: `{args.out_dir}`")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This probe performs read-only reconnaissance for the Tier 2 namespace provenance audit.")
    lines.append("It inventories VAP TEP paths, VAP TEP TSV headers, VDB registration SQLite schemas, and compact Source Identity Set references.")
    lines.append("It does not perform namespace mediation, value-level expansion, external service lookup, coordinate normalization, or interval overlap.")
    lines.append("")
    lines.append("## Safety")
    lines.append("")
    lines.append("SQLite databases are opened using `mode=ro` and `PRAGMA query_only=ON`.")
    lines.append("The probe writes only to its configured probe output directory.")
    lines.append("")
    lines.append("## VAP TEP Inventory")
    lines.append("")
    inv = outputs["vap_inventory"]
    inv_counts = Counter(row["audit_status"] for row in inv)
    for status, count in sorted(inv_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    for row in inv:
        if row["in_current_6tep_corpus"] == "true":
            lines.append(f"- current corpus VAP TEP `{row['sra_id']}` / `{row['run_id']}`: {row['audit_status']} — `{row['expected_tep_dir']}`")
    lines.append("")
    lines.append("## SQLite Inventory")
    lines.append("")
    db_counts = Counter(row["audit_status"] for row in outputs["sqlite_db_inventory"])
    for status, count in sorted(db_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    for row in outputs["sqlite_db_inventory"]:
        lines.append(f"- `{row['db_key']}` ({row['producer']}, {row['corpus_member']}): {row['audit_status']}; tables={row['table_count']}; path=`{row['sqlite_path']}`")
    lines.append("")
    lines.append("## Candidate Column Summary")
    lines.append("")
    route_counts = Counter()
    for row in outputs["sqlite_candidate_columns"] + outputs["vap_candidate_columns"]:
        for route in str(row.get("candidate_routes", "")).split(";"):
            if route and route != "unclassified":
                route_counts[route] += 1
    for route, count in sorted(route_counts.items()):
        lines.append(f"- {route}: {count}")
    lines.append("")
    lines.append("## Next Step")
    lines.append("")
    lines.append("Inspect these probe outputs, then build the full Tier 2 audit against observed table names, column names, and TEP artifact headers rather than assumed schemas.")
    lines.append("")
    (args.out_dir / "probe_report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Read-only MARK probe for Tier 2 TEP-to-VDB namespace provenance audit.")
    parser.add_argument("--vdb-repo", default=".", help="Path to MARK VDB repo root. Default: current directory.")
    parser.add_argument("--vap-repo", default=str(DEFAULT_VAP_REPO), help="Path to MARK VAP repo root.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Probe output directory, relative to VDB repo unless absolute.")
    parser.add_argument("--include-all-vap-headers", action="store_true", help="Read TSV headers for all 13 official VAP TEPs instead of only current 6-TEP corpus members.")
    parser.add_argument("--count-sqlite-rows", action="store_true", help="Optionally run SELECT COUNT(*) on SQLite tables. Off by default to avoid expensive scans.")
    ns = parser.parse_args()
    vdb_repo = Path(ns.vdb_repo).expanduser().resolve()
    vap_repo = Path(ns.vap_repo).expanduser().resolve()
    out_dir = Path(ns.out_dir).expanduser()
    if not out_dir.is_absolute():
        out_dir = vdb_repo / out_dir
    return Args(
        vdb_repo=vdb_repo,
        vap_repo=vap_repo,
        out_dir=out_dir.resolve(),
        include_all_vap_headers=bool(ns.include_all_vap_headers),
        count_sqlite_rows=bool(ns.count_sqlite_rows),
    )


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    vap_inventory, vap_artifacts, vap_headers, vap_candidates = collect_vap_tep_inventory(args)
    sqlite_db_inventory, sqlite_tables, sqlite_columns, sqlite_candidates = collect_sqlite_probe(args)
    compact_handles = collect_compact_handle_probe(args)

    write_tsv(args.out_dir / "probe_vap_tep_inventory.tsv", vap_inventory, [
        "sra_id", "tep_label", "run_id", "depth_category", "in_current_6tep_corpus", "expected_tep_dir",
        "tep_dir_exists", "file_count", "tsv_count", "total_size_bytes", "entity_inventory_exists",
        "lineage_manifest_exists", "validation_report_exists", "stage_13_artifact_manifest_exists",
        "stage_13_final_summary_exists", "audit_status",
    ])
    write_tsv(args.out_dir / "probe_vap_tep_artifact_inventory.tsv", vap_artifacts, [
        "sra_id", "tep_label", "run_id", "depth_category", "in_current_6tep_corpus", "tep_dir",
        "relative_path", "absolute_path", "suffix", "size_bytes", "artifact_lane",
    ])
    write_tsv(args.out_dir / "probe_vap_tep_headers.tsv", vap_headers, [
        "sra_id", "tep_label", "run_id", "depth_category", "in_current_6tep_corpus", "tep_dir",
        "relative_path", "absolute_path", "size_bytes", "column_count", "columns", "coordinate_or_variant_columns",
        "feature_or_interval_columns", "gene_columns", "phenotype_or_overlay_columns",
        "producer_or_observation_columns", "audit_status",
    ])
    write_tsv(args.out_dir / "probe_vap_tep_candidate_namespace_columns.tsv", vap_candidates, [
        "sra_id", "tep_label", "run_id", "depth_category", "in_current_6tep_corpus", "tep_relative_path",
        "column_name", "candidate_routes",
    ])
    write_tsv(args.out_dir / "probe_sqlite_database_inventory.tsv", sqlite_db_inventory, [
        "db_key", "producer", "corpus_member", "sqlite_path", "exists", "size_bytes", "connection_status",
        "sqlite_page_count", "sqlite_page_size", "table_count", "view_count", "audit_status",
    ])
    write_tsv(args.out_dir / "probe_sqlite_table_inventory.tsv", sqlite_tables, [
        "db_key", "producer", "corpus_member", "object_type", "table_name", "column_count", "row_count",
        "row_count_status", "coordinate_or_variant_columns", "feature_or_interval_columns", "gene_columns",
        "phenotype_or_overlay_columns", "producer_or_observation_columns", "all_columns",
    ])
    write_tsv(args.out_dir / "probe_sqlite_column_inventory.tsv", sqlite_columns, [
        "db_key", "producer", "corpus_member", "table_name", "object_type", "column_ordinal", "column_name",
        "column_type", "notnull", "pk", "candidate_routes",
    ])
    write_tsv(args.out_dir / "probe_sqlite_candidate_namespace_columns.tsv", sqlite_candidates, [
        "db_key", "producer", "corpus_member", "table_name", "object_type", "column_ordinal", "column_name",
        "column_type", "notnull", "pk", "candidate_routes",
    ])
    write_tsv(args.out_dir / "probe_compact_source_identity_set_references.tsv", compact_handles, [
        "source_identity_set_id", "assertion_id", "source_assertion_registration_id", "producer", "identity_route",
        "identity_kind", "participant_role", "source_namespace", "source_identity_table_reference", "source_identity_filter",
        "source_identity_count", "lossiness_status", "resolution_status", "source_identity_set_status", "audit_status",
    ])

    outputs = {
        "vap_inventory": vap_inventory,
        "sqlite_db_inventory": sqlite_db_inventory,
        "sqlite_candidate_columns": sqlite_candidates,
        "vap_candidate_columns": vap_candidates,
    }
    write_report(args, outputs)

    summary = {
        "audit_id": AUDIT_ID,
        "corpus_id": CORPUS_ID,
        "generated_utc": utc_now(),
        "vdb_repo": str(args.vdb_repo),
        "vap_repo": str(args.vap_repo),
        "probe_output_dir": str(args.out_dir),
        "vap_tep_count": len(vap_inventory),
        "vap_tep_present_count": sum(1 for r in vap_inventory if r["audit_status"] == "present"),
        "current_corpus_vap_tep_present_count": sum(1 for r in vap_inventory if r["in_current_6tep_corpus"] == "true" and r["audit_status"] == "present"),
        "sqlite_database_count": len(sqlite_db_inventory),
        "sqlite_schema_read_count": sum(1 for r in sqlite_db_inventory if r["audit_status"] == "schema_read"),
        "sqlite_table_rows_emitted": len(sqlite_tables),
        "sqlite_column_rows_emitted": len(sqlite_columns),
        "sqlite_candidate_namespace_column_rows_emitted": len(sqlite_candidates),
        "vap_header_rows_emitted": len(vap_headers),
        "vap_candidate_namespace_column_rows_emitted": len(vap_candidates),
        "compact_source_identity_set_reference_rows": len(compact_handles),
    }
    (args.out_dir / "probe_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("MARK Tier 2 TEP-to-VDB namespace probe complete")
    print(f"  audit_id: {AUDIT_ID}")
    print(f"  output_dir: {args.out_dir}")
    print(f"  report: {args.out_dir / 'probe_report.md'}")
    print(f"  summary: {args.out_dir / 'probe_summary.json'}")
    print("  retrieve this folder for review:")
    print(f"    {args.out_dir}")


if __name__ == "__main__":
    main()

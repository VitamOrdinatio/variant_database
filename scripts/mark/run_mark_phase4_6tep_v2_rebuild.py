#!/usr/bin/env python3
"""Run the MARK Phase 4 six-TEP v2 production substrate rebuild.

This operator script rebuilds VDB-side substrate from existing hardened producer
TEPs. It does not regenerate producer TEPs and it does not overwrite historical
6-TEP v1 outputs.

The v2 rebuild performs:

1. Phase 3 registration into results/registration/mark_phase3_canonical_v2/
2. Phase 4.3 Assertion Record construction into
   results/phase4/assertion_records/mark_phase4_corpus_6tep_v2/
3. Phase 4.4 Evidence Topology construction into
   results/phase4/evidence_topology/mark_phase4_corpus_6tep_v2_topology_build_v1/

The script writes lightweight timing/storage telemetry and creates a receipts-only
Desktop bundle. Large SQLite databases and row-scale payloads remain on MARK.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tarfile
import time
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path.cwd().resolve()
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from variant_database.ingestion.tep_package_resolver import resolve_gsc_tep_package  # noqa: E402
from variant_database.registration.registration_orchestrator import run_registration_pipeline  # noqa: E402
from variant_database.phase4.assertion_records.builder import build_assertion_records  # noqa: E402
from variant_database.phase4.evidence_topology.builder import write_topology_outputs_for_build  # noqa: E402

RUN_ID = "mark_phase4_corpus_6tep_v2_rebuild_001"
CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v2"
TOPOLOGY_BUILD_ID = "mark_phase4_corpus_6tep_v2_topology_build_v1"

DEFAULT_RUN_ROOT = Path("results/phase4/production_runs") / RUN_ID
DEFAULT_REGISTRATION_ROOT = Path("results/registration/mark_phase3_canonical_v2")
DEFAULT_ASSERTION_RECORD_ROOT = Path("results/phase4/assertion_records") / CORPUS_GENERATION_ID
DEFAULT_TOPOLOGY_OUTPUT_ROOT = Path("results/phase4/evidence_topology") / TOPOLOGY_BUILD_ID
DEFAULT_VAP_REPO_ROOT = Path.home() / "dev/portfolio_projects/variant_annotation_pipeline"
DEFAULT_GSC_REPO_ROOT = Path.home() / "dev/portfolio_projects/gene_set_consensus"
DEFAULT_TOPOLOGY_POLICY_TEMPLATE = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v2.json"
)

VAP_TARGETS = [
    {
        "label": "vap_hg002",
        "registration_unit_id": "mark_phase3_canonical_v2_vap_hg002",
        "sample_id": "HG002",
        "run_id": "run_2026_06_03_010030",
        "depth_category": "hg002",
    },
    {
        "label": "vap_median_ERR10619300",
        "registration_unit_id": "mark_phase3_canonical_v2_vap_median_ERR10619300",
        "sample_id": "ERR10619300",
        "run_id": "run_2026_05_27_172531",
        "depth_category": "median",
    },
    {
        "label": "vap_q1_ERR10619212",
        "registration_unit_id": "mark_phase3_canonical_v2_vap_q1_ERR10619212",
        "sample_id": "ERR10619212",
        "run_id": "run_2026_05_30_214724",
        "depth_category": "q1",
    },
    {
        "label": "vap_q3_ERR10619225",
        "registration_unit_id": "mark_phase3_canonical_v2_vap_q3_ERR10619225",
        "sample_id": "ERR10619225",
        "run_id": "run_2026_05_31_091242",
        "depth_category": "q3",
    },
]

GSC_TARGETS = [
    {
        "label": "gsc_epilepsy",
        "registration_unit_id": "mark_phase3_canonical_v2_gsc_epilepsy",
        "topic": "epilepsy",
        "run_id": "run_2026_06_22_184534",
        "tep_json_candidates": [
            Path("results/teps/gsc/epilepsy_semantic_gtr_experimental/run_2026_06_22_184534/gsc_tep.json"),
            Path("results/runs/run_2026_06_22_184534/gsc_tep.json"),
        ],
    },
    {
        "label": "gsc_mitochondrial_disease",
        "registration_unit_id": "mark_phase3_canonical_v2_gsc_mitochondrial_disease",
        "topic": "mitochondrial_disease",
        "run_id": "run_2026_06_23_015533",
        "tep_json_candidates": [
            Path("results/teps/gsc/mitochondrial_semantic_gtr_experimental/run_2026_06_23_015533/gsc_tep.json"),
            Path("results/teps/gsc/mitochondrial_disease_semantic_gtr_experimental/run_2026_06_23_015533/gsc_tep.json"),
            Path("results/runs/run_2026_06_23_015533/gsc_tep.json"),
        ],
    },
]

MANIFEST_COLUMNS = [
    "corpus_generation_id",
    "registration_unit_id",
    "registration_unit_label",
    "registration_unit_reference",
    "registration_unit_path",
    "registration_unit_sqlite_path",
    "registration_unit_inventory_record_reference",
    "registration_unit_readiness_record_reference",
    "phase4_1_validation_receipt_reference",
    "producer_family",
    "source_package_id",
    "registration_backend",
    "assertion_registration_count",
    "source_identity_count",
    "registration_unit_validation_status",
    "registration_unit_certification_status",
    "registration_unit_readiness_status",
    "inclusion_status",
    "inclusion_rationale",
]

REPORT_LINES: list[str] = []
TELEMETRY_ROWS: list[dict[str, Any]] = []


@dataclass(frozen=True)
class RegistrationTarget:
    label: str
    registration_unit_id: str
    producer_family: str
    package_path: Path
    db_path: Path
    source_package_id: str
    sample_id: str = ""
    run_id: str = ""
    depth_category: str = ""
    topic: str = ""


def log(message: str = "") -> None:
    print(message, flush=True)
    REPORT_LINES.append(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_tsv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: to_cell(row.get(key, "")) for key in fieldnames})


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tsv_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("rb") as handle:
        lines = sum(1 for _ in handle)
    return max(0, lines - 1)


def path_size_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            total += child.stat().st_size
    return total


def bytes_to_gib(value: int) -> str:
    return f"{value / 1024 / 1024 / 1024:.3f}"


def disk_usage_row(path: Path, label: str) -> dict[str, Any]:
    usage = shutil.disk_usage(path if path.exists() else REPO_ROOT)
    return {
        "label": label,
        "path": str(path),
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "total_gib": bytes_to_gib(usage.total),
        "used_gib": bytes_to_gib(usage.used),
        "free_gib": bytes_to_gib(usage.free),
        "path_size_bytes": path_size_bytes(path),
        "path_size_gib": bytes_to_gib(path_size_bytes(path)),
        "captured_utc": utc_now(),
    }


def capture_storage_snapshot(path: Path, *, run_root: Path, label: str, extra_paths: Sequence[tuple[str, Path]]) -> list[dict[str, Any]]:
    rows = [disk_usage_row(REPO_ROOT, "repo_root")]
    for item_label, item_path in extra_paths:
        rows.append(disk_usage_row(item_path, item_label))
    write_tsv(
        run_root / f"{label}_storage_snapshot.tsv",
        rows,
        [
            "label",
            "path",
            "total_bytes",
            "used_bytes",
            "free_bytes",
            "total_gib",
            "used_gib",
            "free_gib",
            "path_size_bytes",
            "path_size_gib",
            "captured_utc",
        ],
    )
    return rows


def require_repo_root() -> None:
    expected = REPO_ROOT / "src" / "variant_database"
    if not expected.exists():
        raise SystemExit(
            "This script must be run from the VDB repo root. "
            f"Expected to find {expected}."
        )


def fail_if_source_root_inside_output(source_path: Path, output_root: Path) -> None:
    try:
        source_path.resolve().relative_to(output_root.resolve())
    except ValueError:
        return
    raise RuntimeError(f"Refusing to treat output root as input source: {source_path}")


def clean_selected_roots(
    *,
    run_root: Path,
    registration_root: Path,
    assertion_record_root: Path,
    topology_output_root: Path,
    mode: str,
    overwrite: bool,
) -> None:
    selected: list[Path] = [run_root]
    if mode in {"all", "registration-only"}:
        selected.append(registration_root)
    if mode in {"all", "assertion-records-only", "assertion-and-topology"}:
        selected.append(assertion_record_root)
    if mode in {"all", "assertion-and-topology", "topology-only"}:
        selected.append(topology_output_root)

    for root in selected:
        if root.exists():
            if not overwrite:
                raise FileExistsError(
                    f"Output root already exists: {root}. Use --overwrite to remove selected output roots."
                )
            shutil.rmtree(root)
    run_root.mkdir(parents=True, exist_ok=True)


def find_vap_tep_directory(vap_repo_root: Path, *, sample_id: str, run_id: str) -> Path:
    run_dir = vap_repo_root / "results" / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"VAP run directory not found: {run_dir}")

    candidates = [
        path
        for path in run_dir.rglob(f"*{sample_id}*{run_id}*")
        if path.is_dir() and path.name.startswith("vap_tep_")
    ]
    non_emulation = [path for path in candidates if "emulation" not in str(path).lower()]
    selected = non_emulation or candidates

    if len(selected) != 1:
        raise RuntimeError(
            "Expected exactly one VAP TEP directory for "
            f"sample_id={sample_id!r}, run_id={run_id!r}; found {len(selected)}: "
            f"{[str(path) for path in selected]}"
        )
    return selected[0]


def find_gsc_tep_json(gsc_repo_root: Path, *, target: Mapping[str, Any]) -> Path:
    for relative in target["tep_json_candidates"]:
        candidate = gsc_repo_root / relative
        if candidate.is_file():
            return candidate

    run_id = str(target["run_id"])
    topic = str(target["topic"])
    matches = [
        path
        for path in gsc_repo_root.rglob("gsc_tep.json")
        if run_id in str(path) and topic.split("_")[0] in str(path).lower()
    ]
    if not matches:
        matches = [path for path in gsc_repo_root.rglob("gsc_tep.json") if run_id in str(path)]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one GSC TEP JSON for {target['label']} / {run_id}; "
            f"found {len(matches)}: {[str(path) for path in matches]}"
        )
    return matches[0]


def build_targets(*, registration_root: Path, vap_repo_root: Path, gsc_repo_root: Path) -> list[RegistrationTarget]:
    targets: list[RegistrationTarget] = []

    for target in VAP_TARGETS:
        tep_dir = find_vap_tep_directory(
            vap_repo_root,
            sample_id=str(target["sample_id"]),
            run_id=str(target["run_id"]),
        )
        config_snapshot = tep_dir / "entities" / "metadata" / "config_snapshot.yaml"
        if not config_snapshot.is_file():
            raise FileNotFoundError(
                "Hardened VAP TEP metadata artifact is missing: "
                f"{config_snapshot}. Pull/deploy the DEX-VAP hardening first."
            )
        targets.append(
            RegistrationTarget(
                label=str(target["label"]),
                registration_unit_id=str(target["registration_unit_id"]),
                producer_family="VAP",
                package_path=tep_dir,
                db_path=registration_root / str(target["label"]) / "vdb.sqlite",
                source_package_id=tep_dir.name,
                sample_id=str(target["sample_id"]),
                run_id=str(target["run_id"]),
                depth_category=str(target["depth_category"]),
            )
        )

    for target in GSC_TARGETS:
        tep_json = find_gsc_tep_json(gsc_repo_root, target=target)
        resolved_gsc = resolve_gsc_tep_package(
            tep_json_path=tep_json,
            producer_repo_root=gsc_repo_root,
        )
        if resolved_gsc.missing_required_artifact_ids:
            raise RuntimeError(
                f"{target['label']} TEP missing required artifacts: {resolved_gsc.missing_required_artifact_ids}"
            )
        targets.append(
            RegistrationTarget(
                label=str(target["label"]),
                registration_unit_id=str(target["registration_unit_id"]),
                producer_family="GSC",
                package_path=Path(resolved_gsc.registration_root),
                db_path=registration_root / str(target["label"]) / "vdb.sqlite",
                source_package_id=str(resolved_gsc.tep_id),
                run_id=str(target["run_id"]),
                topic=str(target["topic"]),
            )
        )

    return targets


def connect_read_only(sqlite_path: Path) -> sqlite3.Connection:
    if not sqlite_path.is_file():
        raise FileNotFoundError(f"SQLite database not found: {sqlite_path}")
    conn = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def table_count(conn: sqlite3.Connection, table_name: str) -> int:
    if not table_exists(conn, table_name):
        return 0
    row = conn.execute(f"SELECT COUNT(*) AS n FROM {table_name}").fetchone()
    return int(row["n"] if row is not None else 0)


def first_metadata_row(conn: sqlite3.Connection) -> dict[str, Any]:
    if not table_exists(conn, "package_metadata"):
        return {}
    row = conn.execute(
        "SELECT run_id, sample_id, sra_accession, reference_genome_build, "
        "annotation_assembly, metadata_artifact_path, metadata_parse_status "
        "FROM package_metadata ORDER BY package_metadata_id LIMIT 1"
    ).fetchone()
    return dict(row) if row is not None else {}


def summarize_registration_db(target: RegistrationTarget) -> dict[str, Any]:
    with connect_read_only(target.db_path) as conn:
        metadata = first_metadata_row(conn)
        return {
            "label": target.label,
            "registration_unit_id": target.registration_unit_id,
            "producer_family": target.producer_family,
            "sample_id": target.sample_id,
            "run_id": target.run_id,
            "depth_category": target.depth_category,
            "topic": target.topic,
            "sqlite_path": str(target.db_path),
            "sqlite_size_bytes": target.db_path.stat().st_size if target.db_path.exists() else 0,
            "sqlite_size_gib": bytes_to_gib(target.db_path.stat().st_size if target.db_path.exists() else 0),
            "assertion_registration_count": table_count(conn, "assertion_registrations"),
            "artifact_count": table_count(conn, "artifacts"),
            "source_identity_count": table_count(conn, "source_identities"),
            "package_metadata_count": table_count(conn, "package_metadata"),
            "coordinate_declaration_count": table_count(conn, "source_coordinate_declarations"),
            "feature_declaration_count": table_count(conn, "source_feature_declarations"),
            "metadata_reference_genome_build": metadata.get("reference_genome_build", ""),
            "metadata_annotation_assembly": metadata.get("annotation_assembly", ""),
            "metadata_sample_id": metadata.get("sample_id", ""),
            "metadata_sra_accession": metadata.get("sra_accession", ""),
            "metadata_run_id": metadata.get("run_id", ""),
            "metadata_artifact_path": metadata.get("metadata_artifact_path", ""),
            "metadata_parse_status": metadata.get("metadata_parse_status", ""),
        }


def telemetry_fieldnames() -> list[str]:
    return [
        "event_id",
        "phase",
        "target_label",
        "producer_family",
        "status",
        "start_utc",
        "end_utc",
        "elapsed_seconds",
        "input_path",
        "output_path",
        "sqlite_size_bytes",
        "sqlite_size_gib",
        "assertion_registration_count",
        "source_identity_count",
        "package_metadata_count",
        "coordinate_declaration_count",
        "feature_declaration_count",
        "source_identity_set_count",
        "coordinate_declaration_set_count",
        "feature_declaration_set_count",
        "relationship_count",
        "member_count",
        "basis_component_count",
        "declaration_set_expansion_index_count",
        "notes",
    ]


def record_telemetry(run_root: Path, row: Mapping[str, Any]) -> None:
    TELEMETRY_ROWS.append(dict(row))
    write_tsv(run_root / "phase_timing_telemetry.tsv", TELEMETRY_ROWS, telemetry_fieldnames())


def run_timed_event(
    *,
    run_root: Path,
    event_id: str,
    phase: str,
    target_label: str = "",
    producer_family: str = "",
    input_path: Path | None = None,
    output_path: Path | None = None,
    func,
) -> Any:
    start_utc = utc_now()
    start_perf = time.perf_counter()
    status = "passed"
    notes = ""
    result: Any = None
    try:
        result = func()
        return result
    except Exception as exc:
        status = "failed"
        notes = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        end_utc = utc_now()
        elapsed = time.perf_counter() - start_perf
        base_row: dict[str, Any] = {
            "event_id": event_id,
            "phase": phase,
            "target_label": target_label,
            "producer_family": producer_family,
            "status": status,
            "start_utc": start_utc,
            "end_utc": end_utc,
            "elapsed_seconds": f"{elapsed:.3f}",
            "input_path": str(input_path or ""),
            "output_path": str(output_path or ""),
            "notes": notes,
        }
        if isinstance(result, Mapping):
            for key in telemetry_fieldnames():
                if key in result and key not in base_row:
                    base_row[key] = result[key]
        record_telemetry(run_root, base_row)


def run_phase3_registration(*, targets: list[RegistrationTarget], run_root: Path) -> list[dict[str, Any]]:
    log("\nStage A: Phase 3 registration")
    log("=" * 80)
    rows: list[dict[str, Any]] = []
    for target in targets:
        log(f"Registering {target.label} ({target.producer_family})")
        log(f"  package: {target.package_path}")
        log(f"  sqlite:  {target.db_path}")
        target.db_path.parent.mkdir(parents=True, exist_ok=True)

        def _register() -> dict[str, Any]:
            summary = run_registration_pipeline(
                package_path=target.package_path,
                db_path=target.db_path,
                producer_family=target.producer_family,
            )
            db_summary = summarize_registration_db(target)
            db_summary.update(
                {
                    "pipeline_elapsed_seconds": getattr(summary, "elapsed_seconds", ""),
                    "rows_per_second": getattr(summary, "rows_per_second", ""),
                    "participants_per_second": getattr(summary, "participants_per_second", ""),
                }
            )
            return db_summary

        db_summary = run_timed_event(
            run_root=run_root,
            event_id=f"phase3_register_{target.label}",
            phase="phase3_registration",
            target_label=target.label,
            producer_family=target.producer_family,
            input_path=target.package_path,
            output_path=target.db_path,
            func=_register,
        )
        rows.append(db_summary)
        log(
            "  counts: "
            f"assertions={db_summary['assertion_registration_count']} "
            f"source_identities={db_summary['source_identity_count']} "
            f"package_metadata={db_summary['package_metadata_count']} "
            f"coordinates={db_summary['coordinate_declaration_count']} "
            f"features={db_summary['feature_declaration_count']} "
            f"sqlite_gib={db_summary['sqlite_size_gib']}"
        )
    return rows


def summarize_existing_registrations(targets: list[RegistrationTarget]) -> list[dict[str, Any]]:
    return [summarize_registration_db(target) for target in targets]


def write_assertion_manifest(
    *,
    targets: list[RegistrationTarget],
    phase3_rows: list[dict[str, Any]],
    manifest_path: Path,
) -> None:
    by_label = {row["label"]: row for row in phase3_rows}
    rows: list[dict[str, Any]] = []
    for target in targets:
        phase3 = by_label[target.label]
        rows.append(
            {
                "corpus_generation_id": CORPUS_GENERATION_ID,
                "registration_unit_id": target.registration_unit_id,
                "registration_unit_label": target.label,
                "registration_unit_reference": target.registration_unit_id,
                "registration_unit_path": str(target.db_path.parent.relative_to(REPO_ROOT)),
                "registration_unit_sqlite_path": str(target.db_path.relative_to(REPO_ROOT)),
                "registration_unit_inventory_record_reference": "mark_v2_rebuild_generated",
                "registration_unit_readiness_record_reference": "mark_v2_rebuild_generated",
                "phase4_1_validation_receipt_reference": "mark_v2_rebuild_generated",
                "producer_family": target.producer_family,
                "source_package_id": target.source_package_id,
                "registration_backend": "sqlite",
                "assertion_registration_count": phase3["assertion_registration_count"],
                "source_identity_count": phase3["source_identity_count"],
                "registration_unit_validation_status": "passed_mark_v2_rebuild_generated",
                "registration_unit_certification_status": "mark_v2_rebuild_not_producer_certification",
                "registration_unit_readiness_status": "ready_for_assertion_record_build",
                "inclusion_status": "included",
                "inclusion_rationale": "6-TEP v2 modern substrate rebuild",
            }
        )
    write_tsv(manifest_path, rows, MANIFEST_COLUMNS)


def run_phase4_3(*, manifest_path: Path, output_dir: Path, run_root: Path) -> dict[str, Any]:
    log("\nStage B: Phase 4.3 Assertion Records")
    log("=" * 80)
    log(f"manifest: {manifest_path}")
    log(f"output:   {output_dir}")

    def _build() -> dict[str, Any]:
        result = build_assertion_records(
            manifest_path=manifest_path,
            output_dir=output_dir,
            corpus_generation_id=CORPUS_GENERATION_ID,
        )
        return {
            "assertion_record_output_dir": str(output_dir),
            "assertion_count": getattr(result, "assertion_count", 0),
            "validation_count": getattr(result, "validation_count", 0),
            "registration_unit_count": getattr(result, "registration_unit_count", 0),
            "source_identity_set_count": tsv_row_count(output_dir / "assertion_record_source_identity_sets.tsv"),
            "coordinate_declaration_set_count": tsv_row_count(output_dir / "assertion_record_coordinate_declaration_sets.tsv"),
            "feature_declaration_set_count": tsv_row_count(output_dir / "assertion_record_feature_declaration_sets.tsv"),
        }

    summary = run_timed_event(
        run_root=run_root,
        event_id="phase4_3_assertion_records",
        phase="phase4_3_assertion_records",
        input_path=manifest_path,
        output_path=output_dir,
        func=_build,
    )
    log(
        "  counts: "
        f"assertions={summary['assertion_count']} "
        f"source_identity_sets={summary['source_identity_set_count']} "
        f"coordinate_sets={summary['coordinate_declaration_set_count']} "
        f"feature_sets={summary['feature_declaration_set_count']}"
    )
    return summary


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def patch_topology_policy(template: dict[str, Any], *, ar_dir: Path, topology_output_dir: Path) -> dict[str, Any]:
    policy = json.loads(json.dumps(template))
    policy.setdefault("policy_identity", {}).update(
        {
            "policy_id": "mark_phase4_vap_gsc_topology_derivation_policy_v2",
            "policy_version": "v2",
            "policy_label": "MARK Phase 4 6-TEP v2 Evidence Topology Policy",
            "input_corpus_generation_id": CORPUS_GENERATION_ID,
            "topology_build_id": TOPOLOGY_BUILD_ID,
            "policy_status": "production_rebuild",
        }
    )
    policy.setdefault("governing_references", {})[
        "upstream_assertion_record_output"
    ] = str(ar_dir.relative_to(REPO_ROOT))
    policy.setdefault("topology_build_defaults", {}).update(
        {
            "topology_build_id": TOPOLOGY_BUILD_ID,
            "topology_build_label": "MARK Phase 4 6-TEP v2 Evidence Topology Build v1",
            "input_corpus_generation_id": CORPUS_GENERATION_ID,
            "topology_derivation_policy_id": "mark_phase4_vap_gsc_topology_derivation_policy_v2",
            "topology_derivation_policy_version": "v2",
            "output_dir": str(topology_output_dir.relative_to(REPO_ROOT)),
        }
    )

    input_filenames = {
        "assertion_record_index": "assertion_record_index.tsv",
        "assertion_record_participants": "assertion_record_participants.tsv",
        "assertion_record_source_identity_sets": "assertion_record_source_identity_sets.tsv",
        "assertion_record_source_identity_summary": "assertion_record_source_identity_summary.tsv",
        "assertion_record_coordinate_declaration_sets": "assertion_record_coordinate_declaration_sets.tsv",
        "assertion_record_feature_declaration_sets": "assertion_record_feature_declaration_sets.tsv",
        "assertion_record_lineage": "assertion_record_lineage.tsv",
        "downstream_topology_input_manifest": "downstream_topology_input_manifest.tsv",
    }
    required_inputs = policy.setdefault("required_inputs", {})
    for key, filename in input_filenames.items():
        if key in required_inputs:
            required_inputs[key]["path"] = str((ar_dir / filename).relative_to(REPO_ROOT))
    return policy


def count_by_column(path: Path, column: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in read_tsv(path):
        value = row.get(column, "")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def run_phase4_4(*, policy_path: Path, output_dir: Path, run_root: Path) -> dict[str, Any]:
    log("\nStage C: Phase 4.4 Evidence Topology")
    log("=" * 80)
    log(f"policy: {policy_path}")
    log(f"output: {output_dir}")

    def _build() -> dict[str, Any]:
        result = write_topology_outputs_for_build(
            policy_path=policy_path,
            output_dir=output_dir,
            repo_root=REPO_ROOT,
            build_timestamp_utc=utc_now(),
        )
        member_path = output_dir / "topology_relationship_members.tsv"
        declaration_index_path = output_dir / "topology_declaration_set_expansion_index.tsv"
        return {
            "topology_output_dir": str(output_dir),
            "topology_build_id": getattr(result, "topology_build_id", TOPOLOGY_BUILD_ID),
            "validation_status": getattr(result, "validation_status", ""),
            "relationship_count": tsv_row_count(output_dir / "topology_relationships.tsv"),
            "member_count": tsv_row_count(member_path),
            "basis_component_count": tsv_row_count(output_dir / "topology_basis_components.tsv"),
            "source_identity_expansion_index_count": tsv_row_count(output_dir / "topology_source_identity_expansion_index.tsv"),
            "declaration_set_expansion_index_count": tsv_row_count(declaration_index_path),
            "member_type_counts": count_by_column(member_path, "member_type"),
            "declaration_set_type_counts": count_by_column(declaration_index_path, "declaration_set_type"),
        }

    summary = run_timed_event(
        run_root=run_root,
        event_id="phase4_4_evidence_topology",
        phase="phase4_4_evidence_topology",
        input_path=policy_path,
        output_path=output_dir,
        func=_build,
    )
    log(
        "  counts: "
        f"relationships={summary['relationship_count']} "
        f"members={summary['member_count']} "
        f"basis={summary['basis_component_count']} "
        f"declaration_index={summary['declaration_set_expansion_index_count']}"
    )
    return summary


def evaluate_rebuild(
    *,
    phase3_rows: list[dict[str, Any]],
    phase4_3: dict[str, Any] | None,
    phase4_4: dict[str, Any] | None,
    mode: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: str, message: str, expected: Any, observed: Any) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": status,
                "message": message,
                "expected": expected,
                "observed": observed,
            }
        )

    if mode in {"all", "registration-only", "assertion-records-only", "assertion-and-topology"}:
        for row in phase3_rows:
            label = row.get("label", "")
            producer = row.get("producer_family", "")
            add(
                f"{label}_source_identities_present",
                "passed" if int(row.get("source_identity_count") or 0) > 0 else "failed",
                f"{label} should preserve source identities.",
                ">0",
                row.get("source_identity_count", ""),
            )
            if producer == "VAP":
                add(
                    f"{label}_package_metadata_present",
                    "passed" if int(row.get("package_metadata_count") or 0) > 0 else "failed",
                    f"{label} should include package_metadata from config_snapshot.yaml.",
                    ">0",
                    row.get("package_metadata_count", ""),
                )
                add(
                    f"{label}_reference_build_grch38",
                    "passed" if row.get("metadata_reference_genome_build") == "GRCh38" else "failed",
                    f"{label} should expose GRCh38 reference context.",
                    "GRCh38",
                    row.get("metadata_reference_genome_build", ""),
                )
                add(
                    f"{label}_coordinates_present",
                    "passed" if int(row.get("coordinate_declaration_count") or 0) > 0 else "failed",
                    f"{label} should emit source_coordinate_declarations.",
                    ">0",
                    row.get("coordinate_declaration_count", ""),
                )
                add(
                    f"{label}_features_present",
                    "passed" if int(row.get("feature_declaration_count") or 0) > 0 else "failed",
                    f"{label} should emit source_feature_declarations.",
                    ">0",
                    row.get("feature_declaration_count", ""),
                )
            elif producer == "GSC":
                add(
                    f"{label}_coordinate_noop",
                    "passed" if int(row.get("coordinate_declaration_count") or 0) == 0 else "failed",
                    f"{label} should not emit VAP coordinate declarations.",
                    "0",
                    row.get("coordinate_declaration_count", ""),
                )
                add(
                    f"{label}_feature_noop",
                    "passed" if int(row.get("feature_declaration_count") or 0) == 0 else "failed",
                    f"{label} should not emit VAP feature declarations.",
                    "0",
                    row.get("feature_declaration_count", ""),
                )

    if phase4_3 is not None:
        add(
            "phase4_3_source_identity_sets_present",
            "passed" if int(phase4_3.get("source_identity_set_count") or 0) > 0 else "failed",
            "Assertion Records should preserve source identity sets by reference.",
            ">0",
            phase4_3.get("source_identity_set_count", ""),
        )
        add(
            "phase4_3_coordinate_declaration_sets_present",
            "passed" if int(phase4_3.get("coordinate_declaration_set_count") or 0) > 0 else "failed",
            "Assertion Records should preserve coordinate declaration sets by reference.",
            ">0",
            phase4_3.get("coordinate_declaration_set_count", ""),
        )
        add(
            "phase4_3_feature_declaration_sets_present",
            "passed" if int(phase4_3.get("feature_declaration_set_count") or 0) > 0 else "failed",
            "Assertion Records should preserve feature declaration sets by reference.",
            ">0",
            phase4_3.get("feature_declaration_set_count", ""),
        )

    if phase4_4 is not None:
        add(
            "phase4_4_validation_passed",
            "passed" if phase4_4.get("validation_status") == "passed" else "failed",
            "Evidence Topology build-local validation should pass.",
            "passed",
            phase4_4.get("validation_status", ""),
        )
        add(
            "phase4_4_declaration_expansion_index_present",
            "passed" if int(phase4_4.get("declaration_set_expansion_index_count") or 0) > 0 else "failed",
            "Evidence Topology should emit declaration-set handle expansion index.",
            ">0",
            phase4_4.get("declaration_set_expansion_index_count", ""),
        )
        member_counts = phase4_4.get("member_type_counts", {}) or {}
        add(
            "phase4_4_coordinate_members_present",
            "passed" if int(member_counts.get("coordinate_declaration_set") or 0) > 0 else "failed",
            "Evidence Topology should consume coordinate declaration set handles.",
            ">0",
            member_counts.get("coordinate_declaration_set", ""),
        )
        add(
            "phase4_4_feature_members_present",
            "passed" if int(member_counts.get("feature_declaration_set") or 0) > 0 else "failed",
            "Evidence Topology should consume feature declaration set handles.",
            ">0",
            member_counts.get("feature_declaration_set", ""),
        )

    return rows


def write_markdown_report(path: Path, *, summary: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    status_counts: dict[str, int] = {}
    for row in checks:
        status = str(row.get("status", ""))
        status_counts[status] = status_counts.get(status, 0) + 1
    lines = [
        "# MARK Phase 4 6-TEP v2 Production Rebuild Report",
        "",
        f"- run_id: `{RUN_ID}`",
        f"- corpus_generation_id: `{CORPUS_GENERATION_ID}`",
        f"- topology_build_id: `{TOPOLOGY_BUILD_ID}`",
        f"- rebuild_status: `{summary['rebuild_status']}`",
        f"- mode: `{summary['mode']}`",
        f"- generated_utc: `{summary['generated_utc']}`",
        f"- run_root: `{summary['run_root']}`",
        "",
        "## Scope",
        "",
        "This production rebuild consumes existing hardened VAP/GSC TEPs and creates VDB-side v2 registration, Assertion Record, and Evidence Topology substrate. It does not regenerate producer TEPs and does not overwrite historical v1 outputs.",
        "",
        "## Check status counts",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Checks", ""])
    for row in checks:
        lines.append(
            f"- `{row['check_id']}`: **{row['status']}** — {row['message']} "
            f"(expected: `{row['expected']}`, observed: `{row['observed']}`)"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def make_retrieval_bundle(
    *,
    run_root: Path,
    registration_root: Path,
    assertion_record_root: Path,
    topology_output_root: Path,
    desktop_root: Path,
) -> Path:
    """Create a lightweight receipts-only retrieval bundle.

    Full MARK outputs, especially Phase 3 SQLite files, remain on MARK. The
    bundle includes compact reports, summaries, validation receipts, manifest
    files, Assertion Record handle files, Evidence Topology handle files, and a
    file-size inventory for capacity planning.
    """

    desktop_root.mkdir(parents=True, exist_ok=True)
    receipt_root = desktop_root / f"{RUN_ID}_receipts"
    bundle_path = desktop_root / f"{RUN_ID}_receipts.tgz"

    if receipt_root.exists():
        shutil.rmtree(receipt_root)
    if bundle_path.exists():
        bundle_path.unlink()
    receipt_root.mkdir(parents=True, exist_ok=True)

    exact_receipt_names = {
        "rebuild_summary.json",
        "rebuild_report.md",
        "rebuild_validation_checks.tsv",
        "phase3_registration_summary.tsv",
        "phase4_3_assertion_record_summary.tsv",
        "phase4_4_topology_summary.json",
        "phase_timing_telemetry.tsv",
        "preflight_storage_snapshot.tsv",
        "postflight_storage_snapshot.tsv",
        "rebuild_console_log.txt",
        "generated_topology_policy.json",
        "downstream_assertion_record_input_manifest.tsv",
        "assertion_record_index.tsv",
        "assertion_record_source_identity_sets.tsv",
        "assertion_record_source_identity_summary.tsv",
        "assertion_record_coordinate_declaration_sets.tsv",
        "assertion_record_feature_declaration_sets.tsv",
        "assertion_record_validation_report.tsv",
        "assertion_record_validation_report.json",
        "topology_relationships.tsv",
        "topology_relationship_members.tsv",
        "topology_basis_components.tsv",
        "topology_source_identity_expansion_index.tsv",
        "topology_declaration_set_expansion_index.tsv",
        "topology_namespace_mediation.tsv",
        "topology_validation_report.tsv",
        "topology_validation_report.json",
        "topology_build_report.md",
        "topology_summary.tsv",
    }
    text_suffixes = {".md", ".json", ".txt"}
    excluded_suffixes = {".sqlite", ".sqlite3", ".db", ".db-shm", ".db-wal", ".sqlite-shm", ".sqlite-wal"}
    max_receipt_file_bytes = 50 * 1024 * 1024

    roots = [run_root, assertion_record_root, topology_output_root, registration_root]
    file_inventory_rows: list[dict[str, object]] = []
    copied_rows: list[dict[str, object]] = []
    skipped_rows: list[dict[str, object]] = []

    def should_include(source: Path) -> tuple[bool, str]:
        name = source.name
        suffix = source.suffix.lower()
        if suffix in excluded_suffixes:
            return False, "excluded_database_or_sqlite_sidecar"
        if name in exact_receipt_names:
            return True, "exact_receipt_name"
        if suffix in text_suffixes:
            return True, "text_receipt_suffix"
        if suffix == ".tsv" and any(token in name for token in ("summary", "report", "inventory", "validation", "manifest", "telemetry")):
            return True, "compact_receipt_pattern"
        return False, "not_receipt_pattern"

    for root in roots:
        if not root.exists():
            continue
        for source in sorted(p for p in root.rglob("*") if p.is_file()):
            relative_to_repo = source.relative_to(REPO_ROOT)
            size = source.stat().st_size
            file_inventory_rows.append(
                {
                    "size_bytes": size,
                    "size_mib": f"{size / 1024 / 1024:.3f}",
                    "relative_path": str(relative_to_repo),
                }
            )

            include, reason = should_include(source)
            if not include:
                skipped_rows.append(
                    {
                        "relative_path": str(relative_to_repo),
                        "size_bytes": size,
                        "skip_reason": reason,
                    }
                )
                continue
            if size > max_receipt_file_bytes:
                skipped_rows.append(
                    {
                        "relative_path": str(relative_to_repo),
                        "size_bytes": size,
                        "skip_reason": "receipt_file_size_guard",
                    }
                )
                continue

            destination = receipt_root / relative_to_repo
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied_rows.append(
                {
                    "relative_path": str(relative_to_repo),
                    "size_bytes": size,
                    "include_reason": reason,
                }
            )

    write_tsv(
        receipt_root / "full_rebuild_file_size_inventory.tsv",
        sorted(file_inventory_rows, key=lambda row: int(row["size_bytes"]), reverse=True),
        ["size_bytes", "size_mib", "relative_path"],
    )
    write_tsv(
        receipt_root / "receipt_copied_files.tsv",
        copied_rows,
        ["relative_path", "size_bytes", "include_reason"],
    )
    write_tsv(
        receipt_root / "receipt_skipped_files.tsv",
        skipped_rows,
        ["relative_path", "size_bytes", "skip_reason"],
    )
    (receipt_root / "full_rebuild_file_list.txt").write_text(
        "\n".join(row["relative_path"] for row in file_inventory_rows) + "\n",
        encoding="utf-8",
    )
    write_json(
        receipt_root / "receipt_bundle_manifest.json",
        {
            "run_id": RUN_ID,
            "source_run_root": str(run_root),
            "registration_root": str(registration_root),
            "assertion_record_root": str(assertion_record_root),
            "topology_output_root": str(topology_output_root),
            "receipt_root": str(receipt_root),
            "bundle_path": str(bundle_path),
            "copied_file_count": len(copied_rows),
            "skipped_file_count": len(skipped_rows),
            "max_receipt_file_bytes": max_receipt_file_bytes,
            "database_files_bundled": False,
            "row_scale_payload_files_bundled": False,
        },
    )

    with tarfile.open(bundle_path, "w:gz") as tar:
        tar.add(receipt_root, arcname=receipt_root.name)
    return bundle_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the MARK Phase 4 6-TEP v2 production substrate rebuild."
    )
    parser.add_argument(
        "--mode",
        choices=["all", "registration-only", "assertion-records-only", "assertion-and-topology", "topology-only"],
        default="all",
        help="Execution mode. Default runs Phase 3, Phase 4.3, and Phase 4.4.",
    )
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--registration-root", type=Path, default=DEFAULT_REGISTRATION_ROOT)
    parser.add_argument("--assertion-record-root", type=Path, default=DEFAULT_ASSERTION_RECORD_ROOT)
    parser.add_argument("--topology-output-root", type=Path, default=DEFAULT_TOPOLOGY_OUTPUT_ROOT)
    parser.add_argument("--vap-repo-root", type=Path, default=DEFAULT_VAP_REPO_ROOT)
    parser.add_argument("--gsc-repo-root", type=Path, default=DEFAULT_GSC_REPO_ROOT)
    parser.add_argument("--topology-policy-template", type=Path, default=DEFAULT_TOPOLOGY_POLICY_TEMPLATE)
    parser.add_argument("--desktop-root", type=Path, default=Path.home() / "Desktop")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove only selected v2 output roots for the requested mode before running.",
    )
    parser.add_argument(
        "--no-bundle",
        action="store_true",
        help="Do not write a lightweight receipts-only retrieval TGZ to the desktop root.",
    )
    return parser.parse_args(argv)


def resolve_repo_path(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    require_repo_root()

    run_root = resolve_repo_path(args.run_root)
    registration_root = resolve_repo_path(args.registration_root)
    assertion_record_root = resolve_repo_path(args.assertion_record_root)
    topology_output_root = resolve_repo_path(args.topology_output_root)
    vap_repo_root = args.vap_repo_root.expanduser().resolve()
    gsc_repo_root = args.gsc_repo_root.expanduser().resolve()
    policy_template_path = resolve_repo_path(args.topology_policy_template)
    desktop_root = args.desktop_root.expanduser().resolve()

    if not policy_template_path.is_file():
        raise FileNotFoundError(f"Topology v2 policy template not found: {policy_template_path}")
    if not vap_repo_root.exists():
        raise FileNotFoundError(f"VAP repo root not found: {vap_repo_root}")
    if not gsc_repo_root.exists():
        raise FileNotFoundError(f"GSC repo root not found: {gsc_repo_root}")

    for output_root in (run_root, registration_root, assertion_record_root, topology_output_root):
        fail_if_source_root_inside_output(vap_repo_root, output_root)
        fail_if_source_root_inside_output(gsc_repo_root, output_root)

    clean_selected_roots(
        run_root=run_root,
        registration_root=registration_root,
        assertion_record_root=assertion_record_root,
        topology_output_root=topology_output_root,
        mode=args.mode,
        overwrite=args.overwrite,
    )

    log("MARK Phase 4 6-TEP v2 production substrate rebuild")
    log("=" * 80)
    log(f"repo_root:              {REPO_ROOT}")
    log(f"mode:                   {args.mode}")
    log(f"run_root:               {run_root}")
    log(f"registration_root:      {registration_root}")
    log(f"assertion_record_root:  {assertion_record_root}")
    log(f"topology_output_root:   {topology_output_root}")
    log(f"vap_repo_root:          {vap_repo_root}")
    log(f"gsc_repo_root:          {gsc_repo_root}")
    log(f"policy_template:        {policy_template_path}")

    targets = build_targets(
        registration_root=registration_root,
        vap_repo_root=vap_repo_root,
        gsc_repo_root=gsc_repo_root,
    )

    log("\nTargets")
    log("=" * 80)
    for target in targets:
        log(f"{target.label}: {target.package_path}")

    capture_storage_snapshot(
        REPO_ROOT,
        run_root=run_root,
        label="preflight",
        extra_paths=[
            ("results_registration", REPO_ROOT / "results" / "registration"),
            ("results_phase4", REPO_ROOT / "results" / "phase4"),
            ("registration_root_v2", registration_root),
            ("assertion_record_root_v2", assertion_record_root),
            ("topology_output_root_v2", topology_output_root),
        ],
    )

    phase3_rows: list[dict[str, Any]] = []
    phase4_3: dict[str, Any] | None = None
    phase4_4: dict[str, Any] | None = None
    manifest_path = run_root / "corpus_generation" / "downstream_assertion_record_input_manifest.tsv"

    if args.mode in {"all", "registration-only"}:
        phase3_rows = run_phase3_registration(targets=targets, run_root=run_root)
        write_tsv(
            run_root / "phase3_registration_summary.tsv",
            phase3_rows,
            [
                "label",
                "registration_unit_id",
                "producer_family",
                "sample_id",
                "run_id",
                "depth_category",
                "topic",
                "sqlite_path",
                "sqlite_size_bytes",
                "sqlite_size_gib",
                "assertion_registration_count",
                "artifact_count",
                "source_identity_count",
                "package_metadata_count",
                "coordinate_declaration_count",
                "feature_declaration_count",
                "metadata_reference_genome_build",
                "metadata_annotation_assembly",
                "metadata_sample_id",
                "metadata_sra_accession",
                "metadata_run_id",
                "metadata_artifact_path",
                "metadata_parse_status",
                "pipeline_elapsed_seconds",
                "rows_per_second",
                "participants_per_second",
            ],
        )
    else:
        phase3_rows = summarize_existing_registrations(targets)
        write_tsv(
            run_root / "phase3_registration_summary.tsv",
            phase3_rows,
            list(phase3_rows[0].keys()) if phase3_rows else ["label"],
        )

    if args.mode in {"all", "assertion-records-only", "assertion-and-topology"}:
        write_assertion_manifest(targets=targets, phase3_rows=phase3_rows, manifest_path=manifest_path)
        phase4_3 = run_phase4_3(manifest_path=manifest_path, output_dir=assertion_record_root, run_root=run_root)
        write_tsv(run_root / "phase4_3_assertion_record_summary.tsv", [phase4_3], list(phase4_3.keys()))

    if args.mode in {"all", "assertion-and-topology", "topology-only"}:
        if args.mode == "topology-only":
            # Recreate a manifest pointer for receipts if possible, but do not rebuild Assertion Records.
            if not assertion_record_root.exists():
                raise FileNotFoundError(f"Assertion Record root not found for topology-only mode: {assertion_record_root}")
        policy = patch_topology_policy(
            load_json(policy_template_path),
            ar_dir=assertion_record_root,
            topology_output_dir=topology_output_root,
        )
        generated_policy_path = run_root / "generated_topology_policy.json"
        write_json(generated_policy_path, policy)
        phase4_4 = run_phase4_4(policy_path=generated_policy_path, output_dir=topology_output_root, run_root=run_root)
        write_json(run_root / "phase4_4_topology_summary.json", phase4_4)

    checks = evaluate_rebuild(phase3_rows=phase3_rows, phase4_3=phase4_3, phase4_4=phase4_4, mode=args.mode)
    write_tsv(
        run_root / "rebuild_validation_checks.tsv",
        checks,
        ["check_id", "status", "message", "expected", "observed"],
    )

    capture_storage_snapshot(
        REPO_ROOT,
        run_root=run_root,
        label="postflight",
        extra_paths=[
            ("results_registration", REPO_ROOT / "results" / "registration"),
            ("results_phase4", REPO_ROOT / "results" / "phase4"),
            ("registration_root_v2", registration_root),
            ("assertion_record_root_v2", assertion_record_root),
            ("topology_output_root_v2", topology_output_root),
        ],
    )

    failed = [row for row in checks if row["status"] != "passed"]
    rebuild_status = "passed" if not failed else "failed"
    summary = {
        "run_id": RUN_ID,
        "corpus_generation_id": CORPUS_GENERATION_ID,
        "topology_build_id": TOPOLOGY_BUILD_ID,
        "generated_utc": utc_now(),
        "mode": args.mode,
        "rebuild_status": rebuild_status,
        "run_root": str(run_root),
        "registration_root": str(registration_root),
        "assertion_record_root": str(assertion_record_root),
        "topology_output_root": str(topology_output_root),
        "manifest_path": str(manifest_path),
        "phase3": phase3_rows,
        "phase4_3": phase4_3,
        "phase4_4": phase4_4,
        "failed_checks": failed,
    }
    write_json(run_root / "rebuild_summary.json", summary)
    write_markdown_report(run_root / "rebuild_report.md", summary=summary, checks=checks)
    (run_root / "rebuild_console_log.txt").write_text("\n".join(REPORT_LINES) + "\n", encoding="utf-8")

    bundle_path = ""
    if not args.no_bundle:
        bundle = make_retrieval_bundle(
            run_root=run_root,
            registration_root=registration_root,
            assertion_record_root=assertion_record_root,
            topology_output_root=topology_output_root,
            desktop_root=desktop_root,
        )
        bundle_path = str(bundle)

    log("\nProduction rebuild complete")
    log("=" * 80)
    log(f"rebuild_status: {rebuild_status}")
    log(f"run_root:       {run_root}")
    log(f"summary_json:   {run_root / 'rebuild_summary.json'}")
    log(f"report_md:      {run_root / 'rebuild_report.md'}")
    if bundle_path:
        log(f"receipt_tgz:    {bundle_path}")

    if rebuild_status != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

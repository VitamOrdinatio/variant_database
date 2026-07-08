#!/usr/bin/env python3
"""Run the MARK Phase 4 two-TEP v2 substrate smoke test.

This operator script exercises the modern VDB substrate chain on MARK using a
small real corpus:

- VAP ERR10619300 / run_2026_05_27_172531
- GSC epilepsy semantic GTR experimental TEP

It writes only to a smoke-test output root and does not overwrite historical
canonical v1 artifacts. By default it fails if the smoke output root already
exists. Use ``--overwrite`` to remove only the configured smoke output root.

The smoke verifies that the hardened VAP TEP metadata, Phase 3 package metadata,
coordinate declarations, feature declarations, Phase 4.3 declaration-set handles,
and Phase 4.4 declaration-set topology handles are present end-to-end.
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
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path.cwd().resolve()
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from variant_database.ingestion.tep_package_resolver import resolve_gsc_tep_package  # noqa: E402
from variant_database.registration.registration_orchestrator import run_registration_pipeline  # noqa: E402
from variant_database.phase4.assertion_records.builder import build_assertion_records  # noqa: E402
from variant_database.phase4.evidence_topology.builder import write_topology_outputs_for_build  # noqa: E402

SMOKE_ID = "mark_phase4_corpus_2tep_v2_smoke_001"
CORPUS_GENERATION_ID = "mark_phase4_corpus_2tep_v2"
TOPOLOGY_BUILD_ID = "mark_phase4_corpus_2tep_v2_topology_smoke_001"

DEFAULT_SMOKE_ROOT = Path("results/phase4/smoke_tests") / SMOKE_ID
DEFAULT_VAP_REPO_ROOT = Path.home() / "dev/portfolio_projects/variant_annotation_pipeline"
DEFAULT_GSC_REPO_ROOT = Path.home() / "dev/portfolio_projects/gene_set_consensus"
DEFAULT_TOPOLOGY_POLICY_TEMPLATE = Path(
    "docs/implementation/policies/evidence_topology/"
    "mark_phase4_vap_gsc_topology_derivation_policy_v2.json"
)

VAP_TARGET = {
    "label": "vap_median_ERR10619300",
    "registration_unit_id": "mark_phase3_2tep_v2_vap_median_ERR10619300",
    "producer_family": "VAP",
    "sample_id": "ERR10619300",
    "run_id": "run_2026_05_27_172531",
}

GSC_TARGET = {
    "label": "gsc_epilepsy",
    "registration_unit_id": "mark_phase3_2tep_v2_gsc_epilepsy",
    "producer_family": "GSC",
    "tep_json_relative_path": Path(
        "results/teps/gsc/epilepsy_semantic_gtr_experimental/"
        "run_2026_06_22_184534/gsc_tep.json"
    ),
}

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


@dataclass(frozen=True)
class RegistrationTarget:
    label: str
    registration_unit_id: str
    producer_family: str
    package_path: Path
    db_path: Path
    source_package_id: str


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


def require_repo_root() -> None:
    expected = REPO_ROOT / "src" / "variant_database"
    if not expected.exists():
        raise SystemExit(
            "This script must be run from the VDB repo root. "
            f"Expected to find {expected}."
        )


def fail_if_source_root_inside_smoke(source_path: Path, smoke_root: Path) -> None:
    try:
        source_path.resolve().relative_to(smoke_root.resolve())
    except ValueError:
        return
    raise RuntimeError(f"Refusing to treat smoke output as input source: {source_path}")


def clean_smoke_root(smoke_root: Path, *, overwrite: bool) -> None:
    if smoke_root.exists():
        if not overwrite:
            raise FileExistsError(
                f"Smoke output root already exists: {smoke_root}. "
                "Use --overwrite to remove only this smoke output root."
            )
        shutil.rmtree(smoke_root)
    smoke_root.mkdir(parents=True, exist_ok=True)


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


def build_targets(*, smoke_root: Path, vap_repo_root: Path, gsc_repo_root: Path) -> list[RegistrationTarget]:
    vap_tep_dir = find_vap_tep_directory(
        vap_repo_root,
        sample_id=VAP_TARGET["sample_id"],
        run_id=VAP_TARGET["run_id"],
    )
    vap_config = vap_tep_dir / "entities" / "metadata" / "config_snapshot.yaml"
    if not vap_config.is_file():
        raise FileNotFoundError(
            "Hardened VAP TEP metadata artifact is missing: "
            f"{vap_config}. Pull/deploy the DEX-VAP hardening first."
        )

    gsc_tep_json = gsc_repo_root / GSC_TARGET["tep_json_relative_path"]
    resolved_gsc = resolve_gsc_tep_package(
        tep_json_path=gsc_tep_json,
        producer_repo_root=gsc_repo_root,
    )
    if resolved_gsc.missing_required_artifact_ids:
        raise RuntimeError(
            f"GSC epilepsy TEP missing required artifacts: {resolved_gsc.missing_required_artifact_ids}"
        )

    return [
        RegistrationTarget(
            label=str(VAP_TARGET["label"]),
            registration_unit_id=str(VAP_TARGET["registration_unit_id"]),
            producer_family="VAP",
            package_path=vap_tep_dir,
            db_path=smoke_root / "registration" / str(VAP_TARGET["label"]) / "vdb.sqlite",
            source_package_id=vap_tep_dir.name,
        ),
        RegistrationTarget(
            label=str(GSC_TARGET["label"]),
            registration_unit_id=str(GSC_TARGET["registration_unit_id"]),
            producer_family="GSC",
            package_path=Path(resolved_gsc.registration_root),
            db_path=smoke_root / "registration" / str(GSC_TARGET["label"]) / "vdb.sqlite",
            source_package_id=str(resolved_gsc.tep_id),
        ),
    ]


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
            "sqlite_path": str(target.db_path),
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


def run_phase3_registration(targets: list[RegistrationTarget]) -> list[dict[str, Any]]:
    log("\nStage A: Phase 3 registration")
    log("=" * 80)
    rows: list[dict[str, Any]] = []
    for target in targets:
        log(f"Registering {target.label} ({target.producer_family})")
        log(f"  package: {target.package_path}")
        log(f"  sqlite:  {target.db_path}")
        target.db_path.parent.mkdir(parents=True, exist_ok=True)
        summary = run_registration_pipeline(
            package_path=target.package_path,
            db_path=target.db_path,
            producer_family=target.producer_family,
        )
        db_summary = summarize_registration_db(target)
        db_summary.update(
            {
                "elapsed_seconds": getattr(summary, "elapsed_seconds", ""),
                "rows_per_second": getattr(summary, "rows_per_second", ""),
                "participants_per_second": getattr(summary, "participants_per_second", ""),
            }
        )
        rows.append(db_summary)
        log(
            "  counts: "
            f"assertions={db_summary['assertion_registration_count']} "
            f"source_identities={db_summary['source_identity_count']} "
            f"package_metadata={db_summary['package_metadata_count']} "
            f"coordinates={db_summary['coordinate_declaration_count']} "
            f"features={db_summary['feature_declaration_count']}"
        )
    return rows


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
                "registration_unit_reference": target.label,
                "registration_unit_path": str(target.db_path.parent.relative_to(REPO_ROOT)),
                "registration_unit_sqlite_path": str(target.db_path.relative_to(REPO_ROOT)),
                "registration_unit_inventory_record_reference": "smoke_generated",
                "registration_unit_readiness_record_reference": "smoke_generated",
                "phase4_1_validation_receipt_reference": "smoke_generated",
                "producer_family": target.producer_family,
                "source_package_id": target.source_package_id,
                "registration_backend": "sqlite",
                "assertion_registration_count": phase3["assertion_registration_count"],
                "source_identity_count": phase3["source_identity_count"],
                "registration_unit_validation_status": "passed_smoke_generated",
                "registration_unit_certification_status": "smoke_only_not_certified",
                "registration_unit_readiness_status": "ready_for_smoke",
                "inclusion_status": "included",
                "inclusion_rationale": "2-TEP v2 smoke test substrate",
            }
        )
    write_tsv(manifest_path, rows, MANIFEST_COLUMNS)


def run_phase4_3(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    log("\nStage B: Phase 4.3 Assertion Records")
    log("=" * 80)
    log(f"manifest: {manifest_path}")
    log(f"output:   {output_dir}")
    result = build_assertion_records(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id=CORPUS_GENERATION_ID,
    )
    summary = {
        "assertion_record_output_dir": str(output_dir),
        "assertion_count": getattr(result, "assertion_count", 0),
        "validation_count": getattr(result, "validation_count", 0),
        "registration_unit_count": getattr(result, "registration_unit_count", 0),
        "source_identity_set_count": tsv_row_count(output_dir / "assertion_record_source_identity_sets.tsv"),
        "coordinate_declaration_set_count": tsv_row_count(output_dir / "assertion_record_coordinate_declaration_sets.tsv"),
        "feature_declaration_set_count": tsv_row_count(output_dir / "assertion_record_feature_declaration_sets.tsv"),
    }
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
    policy["policy_identity"].update(
        {
            "policy_id": "mark_phase4_2tep_v2_smoke_topology_policy_v1",
            "policy_version": "v1",
            "policy_label": "MARK Phase 4 2-TEP v2 Smoke Evidence Topology Policy v1",
            "input_corpus_generation_id": CORPUS_GENERATION_ID,
            "topology_build_id": TOPOLOGY_BUILD_ID,
            "policy_status": "smoke_test",
        }
    )
    policy.setdefault("governing_references", {})[
        "upstream_assertion_record_output"
    ] = str(ar_dir.relative_to(REPO_ROOT))
    policy.setdefault("topology_build_defaults", {}).update(
        {
            "topology_build_id": TOPOLOGY_BUILD_ID,
            "topology_build_label": "MARK Phase 4 2-TEP v2 Evidence Topology Smoke Build 001",
            "input_corpus_generation_id": CORPUS_GENERATION_ID,
            "topology_derivation_policy_id": "mark_phase4_2tep_v2_smoke_topology_policy_v1",
            "topology_derivation_policy_version": "v1",
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


def run_phase4_4(policy_path: Path, output_dir: Path) -> dict[str, Any]:
    log("\nStage C: Phase 4.4 Evidence Topology")
    log("=" * 80)
    log(f"policy: {policy_path}")
    log(f"output: {output_dir}")
    result = write_topology_outputs_for_build(
        policy_path=policy_path,
        output_dir=output_dir,
        repo_root=REPO_ROOT,
        build_timestamp_utc=utc_now(),
    )
    member_path = output_dir / "topology_relationship_members.tsv"
    declaration_index_path = output_dir / "topology_declaration_set_expansion_index.tsv"
    summary = {
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
    log(
        "  counts: "
        f"relationships={summary['relationship_count']} "
        f"members={summary['member_count']} "
        f"basis={summary['basis_component_count']} "
        f"declaration_index={summary['declaration_set_expansion_index_count']}"
    )
    return summary


def evaluate_smoke(
    *,
    phase3_rows: list[dict[str, Any]],
    phase4_3: dict[str, Any],
    phase4_4: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    by_label = {row["label"]: row for row in phase3_rows}
    vap = by_label.get(str(VAP_TARGET["label"]), {})
    gsc = by_label.get(str(GSC_TARGET["label"]), {})

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

    add(
        "vap_package_metadata_present",
        "passed" if int(vap.get("package_metadata_count") or 0) > 0 else "failed",
        "VAP registration should include package_metadata from config_snapshot.yaml.",
        ">0",
        vap.get("package_metadata_count", ""),
    )
    add(
        "vap_reference_build_grch38",
        "passed" if vap.get("metadata_reference_genome_build") == "GRCh38" else "failed",
        "VAP package metadata should expose GRCh38 reference context.",
        "GRCh38",
        vap.get("metadata_reference_genome_build", ""),
    )
    add(
        "vap_coordinate_declarations_present",
        "passed" if int(vap.get("coordinate_declaration_count") or 0) > 0 else "failed",
        "VAP registration should emit source_coordinate_declarations.",
        ">0",
        vap.get("coordinate_declaration_count", ""),
    )
    add(
        "vap_feature_declarations_present",
        "passed" if int(vap.get("feature_declaration_count") or 0) > 0 else "failed",
        "VAP registration should emit source_feature_declarations.",
        ">0",
        vap.get("feature_declaration_count", ""),
    )
    add(
        "gsc_registration_safe_noop_for_coordinates",
        "passed" if int(gsc.get("coordinate_declaration_count") or 0) == 0 else "failed",
        "GSC registration should not emit VAP coordinate declarations.",
        "0",
        gsc.get("coordinate_declaration_count", ""),
    )
    add(
        "gsc_registration_safe_noop_for_features",
        "passed" if int(gsc.get("feature_declaration_count") or 0) == 0 else "failed",
        "GSC registration should not emit VAP feature declarations.",
        "0",
        gsc.get("feature_declaration_count", ""),
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

    return rows


def write_markdown_report(path: Path, *, summary: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    status_counts: dict[str, int] = {}
    for row in checks:
        status = str(row.get("status", ""))
        status_counts[status] = status_counts.get(status, 0) + 1
    lines = [
        f"# MARK Phase 4 2-TEP v2 Smoke Test Report",
        "",
        f"- smoke_id: `{SMOKE_ID}`",
        f"- corpus_generation_id: `{CORPUS_GENERATION_ID}`",
        f"- topology_build_id: `{TOPOLOGY_BUILD_ID}`",
        f"- smoke_status: `{summary['smoke_status']}`",
        f"- generated_utc: `{summary['generated_utc']}`",
        f"- output_root: `{summary['smoke_root']}`",
        "",
        "## Scope",
        "",
        "This smoke test uses VAP ERR10619300 and GSC epilepsy only. It does not overwrite the historical 6-TEP v1 outputs.",
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


def make_retrieval_bundle(smoke_root: Path, *, desktop_root: Path) -> Path:
    desktop_root.mkdir(parents=True, exist_ok=True)
    bundle_path = desktop_root / f"{SMOKE_ID}.tgz"
    if bundle_path.exists():
        bundle_path.unlink()
    with tarfile.open(bundle_path, "w:gz") as tar:
        tar.add(smoke_root, arcname=smoke_root.name)
    return bundle_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the MARK Phase 4 2-TEP v2 smoke test."
    )
    parser.add_argument(
        "--smoke-root",
        type=Path,
        default=DEFAULT_SMOKE_ROOT,
        help="Smoke output root relative to the VDB repo unless absolute.",
    )
    parser.add_argument(
        "--vap-repo-root",
        type=Path,
        default=DEFAULT_VAP_REPO_ROOT,
        help="MARK VAP repo root.",
    )
    parser.add_argument(
        "--gsc-repo-root",
        type=Path,
        default=DEFAULT_GSC_REPO_ROOT,
        help="MARK GSC repo root.",
    )
    parser.add_argument(
        "--topology-policy-template",
        type=Path,
        default=DEFAULT_TOPOLOGY_POLICY_TEMPLATE,
        help="V2 Evidence Topology policy template path.",
    )
    parser.add_argument(
        "--desktop-root",
        type=Path,
        default=Path.home() / "Desktop",
        help="Directory where the retrieval TGZ should be written.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove only the configured smoke output root before running.",
    )
    parser.add_argument(
        "--no-bundle",
        action="store_true",
        help="Do not write a retrieval TGZ to the desktop root.",
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

    smoke_root = resolve_repo_path(args.smoke_root)
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

    fail_if_source_root_inside_smoke(vap_repo_root, smoke_root)
    fail_if_source_root_inside_smoke(gsc_repo_root, smoke_root)
    clean_smoke_root(smoke_root, overwrite=args.overwrite)

    log("MARK Phase 4 2-TEP v2 smoke test")
    log("=" * 80)
    log(f"repo_root:      {REPO_ROOT}")
    log(f"smoke_root:     {smoke_root}")
    log(f"vap_repo_root:  {vap_repo_root}")
    log(f"gsc_repo_root:  {gsc_repo_root}")
    log(f"policy_template:{policy_template_path}")

    targets = build_targets(
        smoke_root=smoke_root,
        vap_repo_root=vap_repo_root,
        gsc_repo_root=gsc_repo_root,
    )

    log("\nTargets")
    log("=" * 80)
    for target in targets:
        log(f"{target.label}: {target.package_path}")

    phase3_rows = run_phase3_registration(targets)
    write_tsv(
        smoke_root / "smoke_phase3_registration_summary.tsv",
        phase3_rows,
        [
            "label",
            "registration_unit_id",
            "producer_family",
            "sqlite_path",
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
            "elapsed_seconds",
            "rows_per_second",
            "participants_per_second",
        ],
    )

    manifest_path = smoke_root / "corpus_generation" / "downstream_assertion_record_input_manifest.tsv"
    write_assertion_manifest(targets=targets, phase3_rows=phase3_rows, manifest_path=manifest_path)

    ar_output_dir = smoke_root / "assertion_records" / CORPUS_GENERATION_ID
    phase4_3 = run_phase4_3(manifest_path, ar_output_dir)
    write_tsv(smoke_root / "smoke_phase4_3_assertion_record_summary.tsv", [phase4_3], list(phase4_3.keys()))

    topology_output_dir = smoke_root / "evidence_topology" / TOPOLOGY_BUILD_ID
    policy = patch_topology_policy(load_json(policy_template_path), ar_dir=ar_output_dir, topology_output_dir=topology_output_dir)
    generated_policy_path = smoke_root / "generated_topology_policy.json"
    write_json(generated_policy_path, policy)

    phase4_4 = run_phase4_4(generated_policy_path, topology_output_dir)
    write_json(smoke_root / "smoke_phase4_4_topology_summary.json", phase4_4)

    checks = evaluate_smoke(phase3_rows=phase3_rows, phase4_3=phase4_3, phase4_4=phase4_4)
    write_tsv(
        smoke_root / "smoke_validation_checks.tsv",
        checks,
        ["check_id", "status", "message", "expected", "observed"],
    )

    failed = [row for row in checks if row["status"] != "passed"]
    smoke_status = "passed" if not failed else "failed"
    summary = {
        "smoke_id": SMOKE_ID,
        "corpus_generation_id": CORPUS_GENERATION_ID,
        "topology_build_id": TOPOLOGY_BUILD_ID,
        "generated_utc": utc_now(),
        "smoke_status": smoke_status,
        "smoke_root": str(smoke_root),
        "manifest_path": str(manifest_path),
        "assertion_record_output_dir": str(ar_output_dir),
        "topology_output_dir": str(topology_output_dir),
        "generated_topology_policy": str(generated_policy_path),
        "phase3": phase3_rows,
        "phase4_3": phase4_3,
        "phase4_4": phase4_4,
        "failed_checks": failed,
    }
    write_json(smoke_root / "smoke_summary.json", summary)
    write_markdown_report(smoke_root / "smoke_report.md", summary=summary, checks=checks)
    (smoke_root / "smoke_console_log.txt").write_text("\n".join(REPORT_LINES) + "\n", encoding="utf-8")

    bundle_path = ""
    if not args.no_bundle:
        bundle = make_retrieval_bundle(smoke_root, desktop_root=desktop_root)
        bundle_path = str(bundle)

    log("\nSmoke test complete")
    log("=" * 80)
    log(f"smoke_status: {smoke_status}")
    log(f"output_root:   {smoke_root}")
    log(f"summary_json:  {smoke_root / 'smoke_summary.json'}")
    log(f"report_md:     {smoke_root / 'smoke_report.md'}")
    if bundle_path:
        log(f"retrieval_tgz: {bundle_path}")

    if smoke_status != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

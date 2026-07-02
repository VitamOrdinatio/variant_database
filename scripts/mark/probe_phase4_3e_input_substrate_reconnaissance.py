#!/usr/bin/env python3
"""Phase 4.3E input substrate reconnaissance probe for MARK.

This probe inspects the full-corpus Phase 4.3E input substrate before any
Assertion Record hardening or closure claim. It is intentionally read-only with
respect to the VDB repository and all governed input folders.

The probe writes only to /root/Desktop by default. MARK remains export-only and
must not stage, commit, or push generated artifacts.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tarfile
from typing import Any, Iterable

DEFAULT_MANIFEST = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1/"
    "downstream_assertion_record_input_manifest.tsv"
)
DEFAULT_OUTPUT_ROOT = Path("/root/Desktop")
DEFAULT_CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"
PROBE_PREFIX = "phase4_3e_input_substrate_recon"

CANONICAL_LOGICAL_UNITS = [
    "gsc_epilepsy",
    "gsc_mitochondrial_disease",
    "vap_hg002",
    "vap_median_ERR10619300",
    "vap_q1_ERR10619212",
    "vap_q3_ERR10619225",
]

MANIFEST_PATH_COLUMNS = (
    "registration_unit_sqlite_path",
    "sqlite_path",
    "sqlite_db_path",
    "registration_unit_db_path",
    "registration_unit_path",
    "vdb_sqlite_path",
    "registration_unit_reference",
)

REQUIRED_TABLES = [
    "assertion_registrations",
    "source_identities",
    "artifacts",
    "tep_packages",
    "schema_metadata",
]

ASSERTION_FIELDS = [
    "assertion_registration_id",
    "package_id",
    "artifact_id",
    "surface_role",
    "evidence_domain",
    "producer_family",
    "source_record_ref",
    "assertion_type",
    "participant_summary_json",
    "support_ref_json",
    "authority_context",
    "uncertainty_context",
    "registration_status",
    "payload_json",
]

JSON_FIELDS = [
    "participant_summary_json",
    "support_ref_json",
    "payload_json",
]

SOURCE_IDENTITY_GROUP_FIELDS = [
    "assertion_registration_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
]

SIDE_EFFECT_SUFFIXES = (
    "-wal",
    "-shm",
    "-journal",
    ".sqlite-journal",
    ".db-journal",
)


@dataclass(frozen=True)
class RegistrationUnit:
    manifest_row_index: int
    registration_unit_id: str
    producer_family: str
    sqlite_path: Path
    manifest_row: dict[str, str]


@dataclass(frozen=True)
class SnapshotEntry:
    path: str
    exists: bool
    is_file: bool
    size: int | None
    mtime_ns: int | None


class ProbeFailure(Exception):
    """Operator/configuration failure that prevents the probe from running."""


def log(message: str) -> None:
    print(message, flush=True)


def now_timestamp() -> str:
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: to_cell(row.get(field, "")) for field in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def is_absent(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    if not text:
        return True
    return text.lower() in {"none", "null", "not_reported", "na", "n/a"}


def parse_json_status(value: Any) -> dict[str, Any]:
    if is_absent(value):
        return {
            "json_status": "blank",
            "json_top_level_type": "",
            "json_key_count": 0,
            "json_keys": "",
            "json_error": "",
        }
    text = str(value)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return {
            "json_status": "invalid_json",
            "json_top_level_type": "",
            "json_key_count": 0,
            "json_keys": "",
            "json_error": str(exc),
        }
    if isinstance(parsed, dict):
        keys = sorted(str(key) for key in parsed.keys())
        return {
            "json_status": "empty_object" if not parsed else "nonempty_object",
            "json_top_level_type": "object",
            "json_key_count": len(keys),
            "json_keys": ";".join(keys),
            "json_error": "",
        }
    if isinstance(parsed, list):
        return {
            "json_status": "empty_array" if not parsed else "nonempty_array",
            "json_top_level_type": "array",
            "json_key_count": len(parsed),
            "json_keys": "",
            "json_error": "",
        }
    return {
        "json_status": "scalar",
        "json_top_level_type": type(parsed).__name__,
        "json_key_count": 0,
        "json_keys": "",
        "json_error": "",
    }


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_path(path: Path) -> SnapshotEntry:
    if not path.exists():
        return SnapshotEntry(str(path), False, False, None, None)
    stat = path.stat()
    return SnapshotEntry(str(path), True, path.is_file(), stat.st_size if path.is_file() else None, stat.st_mtime_ns)


def input_sidecar_paths(sqlite_path: Path) -> list[Path]:
    parent = sqlite_path.parent
    base = sqlite_path.name
    candidates = [
        parent / f"{base}-wal",
        parent / f"{base}-shm",
        parent / f"{base}-journal",
        parent / f"{base}.sqlite-journal",
        parent / f"{base}.db-journal",
    ]
    try:
        for child in parent.iterdir():
            if child.name.startswith(base) and child.name.endswith(SIDE_EFFECT_SUFFIXES):
                candidates.append(child)
    except FileNotFoundError:
        pass
    return sorted(set(candidates))


def take_input_snapshot(manifest: Path, units: list[RegistrationUnit]) -> dict[str, dict[str, Any]]:
    paths: set[Path] = {manifest}
    for unit in units:
        paths.add(unit.sqlite_path)
        paths.update(input_sidecar_paths(unit.sqlite_path))
    snapshot: dict[str, dict[str, Any]] = {}
    for path in sorted(paths, key=lambda p: str(p)):
        entry = snapshot_path(path)
        snapshot[entry.path] = {
            "exists": entry.exists,
            "is_file": entry.is_file,
            "size": entry.size,
            "mtime_ns": entry.mtime_ns,
        }
    return snapshot


def compare_snapshots(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    keys = sorted(set(before) | set(after))
    for key in keys:
        b = before.get(key)
        a = after.get(key)
        if b != a:
            changes.append({
                "path": key,
                "status": "changed",
                "before": json.dumps(b, sort_keys=True),
                "after": json.dumps(a, sort_keys=True),
            })
    return changes


def resolve_path_candidate(value: str, repo_root: Path) -> Path | None:
    if is_absent(value):
        return None
    raw = Path(value)
    candidates = []
    candidates.append(raw if raw.is_absolute() else repo_root / raw)
    if not raw.is_absolute():
        candidates.append(Path.cwd() / raw)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
        if candidate.is_dir():
            for name in ("vdb.sqlite", "registration_unit.sqlite", "vdb.db"):
                child = candidate / name
                if child.is_file():
                    return child.resolve()
            sqlite_children = sorted(list(candidate.glob("*.sqlite")) + list(candidate.glob("*.db")))
            if sqlite_children:
                return sqlite_children[0].resolve()
    return None


def resolve_registration_unit_sqlite(row: dict[str, str], repo_root: Path) -> tuple[Path | None, str]:
    for column in MANIFEST_PATH_COLUMNS:
        value = row.get(column, "")
        resolved = resolve_path_candidate(value, repo_root)
        if resolved is not None:
            return resolved, column
    for column, value in row.items():
        text = (value or "").strip()
        if not text:
            continue
        if text.endswith((".sqlite", ".db")) or "/" in text:
            resolved = resolve_path_candidate(text, repo_root)
            if resolved is not None:
                return resolved, f"scanned:{column}"
    return None, "unresolved"


def infer_registration_unit_id(row: dict[str, str], index: int) -> str:
    for column in ("registration_unit_id", "registration_unit_label", "registration_unit_reference", "unit_id"):
        value = (row.get(column) or "").strip()
        if value:
            return value
    return f"manifest_row_{index:06d}"


def infer_producer_family(row: dict[str, str], registration_unit_id: str) -> str:
    for column in ("producer_family", "producer", "source_family"):
        value = (row.get(column) or "").strip()
        if value:
            return value.upper()
    rid = registration_unit_id.lower()
    if "gsc" in rid:
        return "GSC"
    if "vap" in rid:
        return "VAP"
    return "unknown"


def load_manifest_units(manifest_path: Path, repo_root: Path) -> tuple[list[RegistrationUnit], list[dict[str, Any]]]:
    rows = read_tsv(manifest_path)
    units: list[RegistrationUnit] = []
    audit_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        registration_unit_id = infer_registration_unit_id(row, idx)
        producer_family = infer_producer_family(row, registration_unit_id)
        sqlite_path, source_column = resolve_registration_unit_sqlite(row, repo_root)
        status = "resolved" if sqlite_path is not None else "unresolved"
        audit_rows.append({
            "manifest_row_index": idx,
            "registration_unit_id": registration_unit_id,
            "producer_family": producer_family,
            "sqlite_path_resolution_status": status,
            "sqlite_path_source_column": source_column,
            "sqlite_path": str(sqlite_path or ""),
            "manifest_columns": ";".join(row.keys()),
        })
        if sqlite_path is not None:
            units.append(RegistrationUnit(idx, registration_unit_id, producer_family, sqlite_path, row))
    return units, audit_rows


def connect_read_only(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    if not table_exists(conn, table_name):
        return []
    return [str(row[1]) for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]


def table_count(conn: sqlite3.Connection, table_name: str) -> int | None:
    if not table_exists(conn, table_name):
        return None
    row = conn.execute(f"SELECT COUNT(*) AS n FROM {table_name}").fetchone()
    return int(row["n"])


def select_all(conn: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    if not table_exists(conn, table_name):
        return []
    return [dict(row) for row in conn.execute(f"SELECT * FROM {table_name}").fetchall()]


def rows_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row.get(key, "")): row for row in rows if not is_absent(row.get(key))}


def group_source_identities(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    if not table_exists(conn, "source_identities"):
        return []
    columns = set(table_columns(conn, "source_identities"))
    missing = [column for column in SOURCE_IDENTITY_GROUP_FIELDS if column not in columns]
    if missing:
        return []
    query = """
        SELECT
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace,
            COUNT(*) AS source_identity_count
        FROM source_identities
        GROUP BY
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace
        ORDER BY
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace
    """
    return [dict(row) for row in conn.execute(query).fetchall()]


def audit_registration_unit(
    unit: RegistrationUnit,
    conn: sqlite3.Connection,
    output_accumulators: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    log(f"Inspecting {unit.registration_unit_id} ({unit.producer_family})")

    table_audit = output_accumulators["registration_unit_table_audit"]
    assertion_field_rows = output_accumulators["assertion_registration_field_completeness"]
    json_summary_rows = output_accumulators["assertion_registration_json_field_summary"]
    artifact_resolution_rows = output_accumulators["assertion_to_artifact_resolution"]
    package_resolution_rows = output_accumulators["assertion_to_package_resolution"]
    attachment_summary_rows = output_accumulators["source_identity_attachment_summary"]
    role_kind_rows = output_accumulators["source_identity_role_kind_namespace_summary"]
    participant_audit_rows = output_accumulators["participant_substrate_audit"]
    lineage_audit_rows = output_accumulators["lineage_substrate_audit"]
    findings = output_accumulators["phase_localization_findings"]

    for table in REQUIRED_TABLES:
        columns = table_columns(conn, table)
        row_count = table_count(conn, table) if columns else ""
        table_audit.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": unit.producer_family,
            "sqlite_path": str(unit.sqlite_path),
            "table_name": table,
            "table_exists": bool(columns),
            "row_count": row_count,
            "column_count": len(columns),
            "columns": ";".join(columns),
        })
        if not columns:
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": unit.producer_family,
                "source_assertion_registration_id": "",
                "assertion_type": "",
                "finding_key": f"missing_required_table:{table}",
                "phase_localization": "upstream_4_1_registration_unit_gap",
                "severity": "error",
                "message": f"Required Registration Unit table is missing: {table}",
            })

    assertion_rows = select_all(conn, "assertion_registrations")
    artifact_rows = select_all(conn, "artifacts")
    package_rows = select_all(conn, "tep_packages")
    artifacts = rows_by_key(artifact_rows, "artifact_id")
    packages = rows_by_key(package_rows, "package_id")
    source_groups = group_source_identities(conn)

    group_by_assertion: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for group in source_groups:
        group_by_assertion[str(group.get("assertion_registration_id", ""))].append(group)
        role_kind_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": unit.producer_family,
            "source_assertion_registration_id": group.get("assertion_registration_id", ""),
            "identity_kind": group.get("identity_kind", ""),
            "participant_role": group.get("participant_role", ""),
            "source_namespace": group.get("source_namespace", ""),
            "source_identity_count": group.get("source_identity_count", 0),
        })

    assertion_type_counts: Counter[str] = Counter()
    participant_status_counts: Counter[str] = Counter()
    lineage_status_counts: Counter[str] = Counter()
    source_identity_total = 0

    for assertion in assertion_rows:
        assertion_id = str(assertion.get("assertion_registration_id", ""))
        assertion_type = str(assertion.get("assertion_type", ""))
        assertion_producer = str(assertion.get("producer_family") or unit.producer_family).upper()
        assertion_type_counts[assertion_type] += 1

        completeness: dict[str, str] = {}
        for field in ASSERTION_FIELDS:
            completeness[field] = "absent" if is_absent(assertion.get(field)) else "present"
        assertion_field_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            **{f"{field}_status": completeness[field] for field in ASSERTION_FIELDS},
        })

        for field in JSON_FIELDS:
            parsed = parse_json_status(assertion.get(field))
            json_summary_rows.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "json_field": field,
                **parsed,
            })

        artifact_id = str(assertion.get("artifact_id", ""))
        package_id = str(assertion.get("package_id", ""))
        artifact = artifacts.get(artifact_id)
        package = packages.get(package_id)
        artifact_status = "resolved" if artifact else ("missing_artifact_id" if is_absent(artifact_id) else "unresolved_artifact_id")
        package_status = "resolved" if package else ("missing_package_id" if is_absent(package_id) else "unresolved_package_id")

        artifact_resolution_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            "artifact_id": artifact_id,
            "artifact_resolution_status": artifact_status,
            "artifact_relative_path": artifact.get("relative_path", "") if artifact else "",
            "artifact_sha256": artifact.get("sha256", "") if artifact else "",
            "artifact_size_bytes": artifact.get("size_bytes", "") if artifact else "",
            "artifact_is_manifest": artifact.get("is_manifest", "") if artifact else "",
        })
        package_resolution_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            "package_id": package_id,
            "package_resolution_status": package_status,
            "package_columns_present": ";".join(package.keys()) if package else "",
        })

        if artifact_status != "resolved":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "artifact_reference_unresolved",
                "phase_localization": "upstream_4_1_registration_unit_gap",
                "severity": "error",
                "message": f"assertion artifact_id does not resolve: {artifact_id}",
            })
        if package_status != "resolved":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "package_reference_unresolved",
                "phase_localization": "upstream_4_1_registration_unit_gap",
                "severity": "error",
                "message": f"assertion package_id does not resolve: {package_id}",
            })

        groups = group_by_assertion.get(assertion_id, [])
        identity_count = sum(int(group.get("source_identity_count") or 0) for group in groups)
        source_identity_total += identity_count
        role_values = sorted({str(group.get("participant_role", "")) for group in groups if not is_absent(group.get("participant_role"))})
        kind_values = sorted({str(group.get("identity_kind", "")) for group in groups if not is_absent(group.get("identity_kind"))})
        namespace_values = sorted({str(group.get("source_namespace", "")) for group in groups if not is_absent(group.get("source_namespace"))})
        attachment_status = "attached" if identity_count else "no_source_identities_attached"
        attachment_summary_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            "source_identity_attachment_status": attachment_status,
            "source_identity_group_count": len(groups),
            "source_identity_total_count": identity_count,
            "participant_roles": ";".join(role_values),
            "identity_kinds": ";".join(kind_values),
            "source_namespaces": ";".join(namespace_values),
        })

        participant_json_status = parse_json_status(assertion.get("participant_summary_json"))
        participant_summary_has_content = participant_json_status["json_status"] == "nonempty_object"
        if participant_summary_has_content and identity_count:
            participant_substrate_status = "participant_summary_and_source_identities_present"
        elif participant_summary_has_content:
            participant_substrate_status = "participant_summary_only"
        elif identity_count:
            participant_substrate_status = "source_identities_only"
        else:
            participant_substrate_status = "no_participant_substrate_detected"
        participant_status_counts[participant_substrate_status] += 1
        participant_audit_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            "participant_summary_json_status": participant_json_status["json_status"],
            "participant_summary_json_keys": participant_json_status["json_keys"],
            "source_identity_group_count": len(groups),
            "source_identity_total_count": identity_count,
            "source_identity_participant_roles": ";".join(role_values),
            "participant_substrate_status": participant_substrate_status,
        })
        if participant_substrate_status == "source_identities_only":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "participants_exist_in_source_identities_not_participant_summary_json",
                "phase_localization": "phase_4_3_builder_mapping_gap",
                "severity": "warning",
                "message": "participant_summary_json is blank/empty, but source_identities contain role-bearing participant substrate",
            })
        elif participant_substrate_status == "no_participant_substrate_detected":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "no_participant_substrate_detected",
                "phase_localization": "needs_manual_review",
                "severity": "warning",
                "message": "neither participant_summary_json nor source_identities provide participant substrate",
            })

        row_ref_status = "present" if not is_absent(assertion.get("source_record_ref")) else "explicit_absence"
        artifact_lineage_status = "present" if artifact_status == "resolved" else "missing"
        package_lineage_status = "present" if package_status == "resolved" else "missing"
        if row_ref_status == "present" and artifact_lineage_status == "present" and package_lineage_status == "present":
            lineage_completeness_status = "row_and_artifact_lineage_present"
        elif artifact_lineage_status == "present" and package_lineage_status == "present":
            lineage_completeness_status = "artifact_level_lineage_present_row_ref_absent"
        else:
            lineage_completeness_status = "lineage_incomplete"
        lineage_status_counts[lineage_completeness_status] += 1
        lineage_audit_rows.append({
            "registration_unit_id": unit.registration_unit_id,
            "producer_family": assertion_producer,
            "source_assertion_registration_id": assertion_id,
            "assertion_type": assertion_type,
            "source_record_ref": assertion.get("source_record_ref", ""),
            "source_record_ref_status": row_ref_status,
            "package_id": package_id,
            "package_resolution_status": package_status,
            "artifact_id": artifact_id,
            "artifact_resolution_status": artifact_status,
            "artifact_relative_path": artifact.get("relative_path", "") if artifact else "",
            "artifact_sha256": artifact.get("sha256", "") if artifact else "",
            "artifact_size_bytes": artifact.get("size_bytes", "") if artifact else "",
            "lineage_completeness_status": lineage_completeness_status,
        })
        if lineage_completeness_status == "artifact_level_lineage_present_row_ref_absent":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "row_level_source_record_ref_absent_artifact_lineage_present",
                "phase_localization": "legitimate_explicit_absence_requires_phase_4_3_status_encoding",
                "severity": "info",
                "message": "source_record_ref is absent in assertion_registrations, but artifact/package lineage resolves",
            })
        elif lineage_completeness_status == "lineage_incomplete":
            findings.append({
                "registration_unit_id": unit.registration_unit_id,
                "producer_family": assertion_producer,
                "source_assertion_registration_id": assertion_id,
                "assertion_type": assertion_type,
                "finding_key": "lineage_incomplete",
                "phase_localization": "upstream_4_1_registration_unit_gap",
                "severity": "error",
                "message": "artifact/package lineage is incomplete for assertion registration",
            })

    return {
        "registration_unit_id": unit.registration_unit_id,
        "producer_family": unit.producer_family,
        "assertion_count": len(assertion_rows),
        "assertion_type_counts": dict(assertion_type_counts),
        "source_identity_group_count": len(source_groups),
        "source_identity_total_count": source_identity_total,
        "participant_substrate_status_counts": dict(participant_status_counts),
        "lineage_completeness_status_counts": dict(lineage_status_counts),
    }


def write_manifest_for_output(root: Path) -> None:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.relative_to(root).as_posix() != "checksums/file_manifest.sha256":
            rows.append({
                "relative_path": path.relative_to(root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })
    write_tsv(root / "checksums" / "file_manifest.sha256", rows, ["sha256", "size_bytes", "relative_path"])
    write_json(root / "file_manifest.json", rows)


def make_archive(output_dir: Path) -> tuple[Path, Path, str]:
    archive_path = output_dir.with_suffix(".tgz")
    checksum_path = Path(str(archive_path) + ".sha256")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(output_dir, arcname=output_dir.name)
    digest = sha256_file(archive_path)
    checksum_path.write_text(f"{digest}  {archive_path.name}\n", encoding="utf-8")
    return archive_path, checksum_path, digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Probe Phase 4.3E full-corpus input substrate on MARK without mutating repo inputs.",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--corpus-generation-id", default=DEFAULT_CORPUS_GENERATION_ID)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing /root/Desktop probe directory with the same timestamp.")
    args = parser.parse_args(argv)

    repo_root = Path.cwd().resolve()
    manifest = args.manifest if args.manifest.is_absolute() else repo_root / args.manifest
    output_root = args.output_root
    timestamp = args.timestamp or now_timestamp()
    output_dir = output_root / f"{PROBE_PREFIX}_{timestamp}"

    if not manifest.exists():
        raise ProbeFailure(f"Manifest not found: {manifest}")
    if output_dir.exists():
        if not args.overwrite:
            raise ProbeFailure(f"Output directory already exists: {output_dir}; use --overwrite to replace it")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "input_manifest_audit": [],
        "registration_unit_table_audit": [],
        "assertion_registration_field_completeness": [],
        "assertion_registration_json_field_summary": [],
        "assertion_to_artifact_resolution": [],
        "assertion_to_package_resolution": [],
        "source_identity_attachment_summary": [],
        "source_identity_role_kind_namespace_summary": [],
        "participant_substrate_audit": [],
        "lineage_substrate_audit": [],
        "phase_localization_findings": [],
    }

    log("Phase 4.3E input substrate reconnaissance probe")
    log(f"Manifest: {manifest}")
    log(f"Output:   {output_dir}")

    units, manifest_audit = load_manifest_units(manifest, repo_root)
    all_outputs["input_manifest_audit"].extend(manifest_audit)
    if not units:
        raise ProbeFailure("No Registration Unit SQLite paths resolved from manifest")

    before_snapshot = take_input_snapshot(manifest, units)
    unit_summaries: list[dict[str, Any]] = []

    for unit in units:
        with connect_read_only(unit.sqlite_path) as conn:
            summary = audit_registration_unit(unit, conn, all_outputs)
            unit_summaries.append(summary)

    after_snapshot = take_input_snapshot(manifest, units)
    prime_directive_changes = compare_snapshots(before_snapshot, after_snapshot)

    represented_ids = {unit.registration_unit_id for unit in units}
    alias_hits = []
    for logical in CANONICAL_LOGICAL_UNITS:
        matching = sorted([rid for rid in represented_ids if logical in rid or rid.endswith(logical)])
        alias_hits.append({
            "logical_registration_unit": logical,
            "resolution_status": "resolved" if matching else "unresolved",
            "resolved_registration_unit_ids": ";".join(matching),
        })
        if not matching:
            all_outputs["phase_localization_findings"].append({
                "registration_unit_id": "",
                "producer_family": "",
                "source_assertion_registration_id": "",
                "assertion_type": "",
                "finding_key": f"canonical_logical_registration_unit_unresolved:{logical}",
                "phase_localization": "upstream_4_2_handoff_gap",
                "severity": "error",
                "message": f"Canonical logical Registration Unit not resolved in downstream manifest: {logical}",
            })

    totals = {
        "registration_unit_count": len(units),
        "assertion_count": sum(int(row["assertion_count"]) for row in unit_summaries),
        "source_identity_group_count": sum(int(row["source_identity_group_count"]) for row in unit_summaries),
        "source_identity_total_count": sum(int(row["source_identity_total_count"]) for row in unit_summaries),
        "finding_counts_by_severity": dict(Counter(row["severity"] for row in all_outputs["phase_localization_findings"])),
        "prime_directive_change_count": len(prime_directive_changes),
    }

    report_specs = {
        "input_manifest_audit": ["manifest_row_index", "registration_unit_id", "producer_family", "sqlite_path_resolution_status", "sqlite_path_source_column", "sqlite_path", "manifest_columns"],
        "registration_unit_table_audit": ["registration_unit_id", "producer_family", "sqlite_path", "table_name", "table_exists", "row_count", "column_count", "columns"],
        "assertion_registration_field_completeness": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type"] + [f"{field}_status" for field in ASSERTION_FIELDS],
        "assertion_registration_json_field_summary": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "json_field", "json_status", "json_top_level_type", "json_key_count", "json_keys", "json_error"],
        "assertion_to_artifact_resolution": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "artifact_id", "artifact_resolution_status", "artifact_relative_path", "artifact_sha256", "artifact_size_bytes", "artifact_is_manifest"],
        "assertion_to_package_resolution": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "package_id", "package_resolution_status", "package_columns_present"],
        "source_identity_attachment_summary": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "source_identity_attachment_status", "source_identity_group_count", "source_identity_total_count", "participant_roles", "identity_kinds", "source_namespaces"],
        "source_identity_role_kind_namespace_summary": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "identity_kind", "participant_role", "source_namespace", "source_identity_count"],
        "participant_substrate_audit": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "participant_summary_json_status", "participant_summary_json_keys", "source_identity_group_count", "source_identity_total_count", "source_identity_participant_roles", "participant_substrate_status"],
        "lineage_substrate_audit": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "source_record_ref", "source_record_ref_status", "package_id", "package_resolution_status", "artifact_id", "artifact_resolution_status", "artifact_relative_path", "artifact_sha256", "artifact_size_bytes", "lineage_completeness_status"],
        "phase_localization_findings": ["registration_unit_id", "producer_family", "source_assertion_registration_id", "assertion_type", "finding_key", "phase_localization", "severity", "message"],
    }
    for name, fields in report_specs.items():
        write_tsv(output_dir / f"{name}.tsv", all_outputs[name], fields)

    write_tsv(output_dir / "canonical_registration_unit_alias_audit.tsv", alias_hits, ["logical_registration_unit", "resolution_status", "resolved_registration_unit_ids"])
    write_tsv(output_dir / "prime_directive_input_mutation_report.tsv", prime_directive_changes, ["path", "status", "before", "after"])
    write_json(output_dir / "input_snapshot_before.json", before_snapshot)
    write_json(output_dir / "input_snapshot_after.json", after_snapshot)
    write_json(output_dir / "unit_summaries.json", unit_summaries)
    write_json(output_dir / "recon_summary.json", {
        "probe_id": f"{PROBE_PREFIX}_{timestamp}",
        "corpus_generation_id": args.corpus_generation_id,
        "manifest": str(manifest),
        "output_dir": str(output_dir),
        "totals": totals,
        "canonical_registration_unit_alias_audit": alias_hits,
        "prime_directive_preserved": len(prime_directive_changes) == 0,
        "writes_repo_outputs": False,
        "writes_only_output_root": str(output_root),
        "derives_topology": False,
        "emits_projection_views": False,
        "performs_rdgp_reasoning": False,
    })
    readme = f"""# Phase 4.3E Input Substrate Reconnaissance Probe

Probe ID: `{PROBE_PREFIX}_{timestamp}`

This MARK-side probe inspects the governed Phase 4.3E input substrate before
downstream Assertion Record hardening. It writes only to `/root/Desktop` by default.

It does not build Assertion Records, does not mutate input folders, does not derive
topology, does not emit projections, and does not perform RDGP reasoning.

Key reports:

- `participant_substrate_audit.tsv`
- `lineage_substrate_audit.tsv`
- `phase_localization_findings.tsv`
- `source_identity_attachment_summary.tsv`
- `canonical_registration_unit_alias_audit.tsv`
- `prime_directive_input_mutation_report.tsv`
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    write_manifest_for_output(output_dir)
    archive_path, checksum_path, digest = make_archive(output_dir)

    log("Phase 4.3E input substrate reconnaissance probe completed")
    log(f"Output:   {output_dir}")
    log(f"Archive:  {archive_path}")
    log(f"Checksum: {checksum_path}")
    log(f"Archive SHA256: {digest}")
    log(f"Findings by severity: {totals['finding_counts_by_severity']}")
    log(f"Prime Directive preserved: {len(prime_directive_changes) == 0}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeFailure as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

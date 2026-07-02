"""Phase 4.3 Assertion Record builder.

This module implements the Assertion Record layer only. It consumes governed
Registration Unit substrate and emits Assertion Record artifacts. It deliberately
does not derive Evidence Topology, characterize Convergence Geometry, construct
Evidence Convergence Surfaces, emit Projection Views, or perform RDGP reasoning.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import hashlib
import json
import sqlite3
from typing import Any, Iterable

from .identity import make_assertion_id, make_source_assertion_key
from .resolver_policy import (
    resolve_assertion,
    source_identity_set_status as policy_source_identity_set_status,
)

ASSERTION_INDEX_COLUMNS = [
    "assertion_id",
    "source_assertion_key",
    "corpus_generation_id",
    "registration_unit_id",
    "producer_family",
    "source_package_id",
    "source_artifact_id",
    "source_assertion_registration_id",
    "assertion_type",
    "relationship_class",
    "preservation_status",
    "resolver_status",
    "validation_status",
    "source_identity_set_status",
    "authority_context",
    "uncertainty_context",
]

PARTICIPANT_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "participant_role",
    "participant_value",
    "participant_source",
    "source_identity_set_id",
    "participant_identity_kind",
    "participant_source_namespace",
    "participant_count",
    "participant_resolution_status",
]

RELATIONSHIP_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "relationship_class",
    "assertion_type",
    "producer_family",
]

EVIDENCE_BASIS_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "evidence_basis_status",
    "support_ref_json",
]

CONTEXT_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "context_status",
    "surface_role",
    "evidence_domain",
    "authority_context",
    "uncertainty_context",
]

LINEAGE_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "corpus_generation_id",
    "registration_unit_id",
    "source_package_id",
    "source_artifact_id",
    "source_artifact_relative_path",
    "source_artifact_sha256",
    "source_artifact_size_bytes",
    "source_record_ref",
    "source_record_ref_status",
    "lineage_completeness_status",
]

PAYLOAD_REFERENCE_COLUMNS = [
    "assertion_id",
    "source_assertion_registration_id",
    "source_artifact_id",
    "relative_path",
    "payload_json",
]

SOURCE_IDENTITY_SET_COLUMNS = [
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "source_identity_table_reference",
    "source_identity_filter",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
    "lossiness_status",
    "resolution_status",
    "validation_status",
    "source_identity_set_status",
]

SOURCE_IDENTITY_SUMMARY_COLUMNS = [
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "registration_unit_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
]

VALIDATION_COLUMNS = [
    "registration_unit_id",
    "producer_family",
    "source_assertion_registration_id",
    "assertion_type",
    "preservation_status",
    "resolver_status",
    "validation_status",
    "source_identity_set_status",
    "message",
]

DOWNSTREAM_TOPOLOGY_COLUMNS = [
    "assertion_id",
    "corpus_generation_id",
    "registration_unit_id",
    "producer_family",
    "source_assertion_registration_id",
    "assertion_type",
    "relationship_class",
    "preservation_status",
    "resolver_status",
    "validation_status",
]

MANIFEST_PATH_COLUMNS = (
    "registration_unit_sqlite_path",
    "sqlite_path",
    "sqlite_db_path",
    "registration_unit_db_path",
    "registration_unit_path",
)


@dataclass(frozen=True)
class BuildResult:
    output_dir: Path
    assertion_count: int
    validation_count: int
    registration_unit_count: int


def _stable_id(prefix: str, parts: Iterable[Any]) -> str:
    payload = "\x1f".join("" if part is None else str(part) for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}_{digest[:24]}"


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _write_tsv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _to_cell(row.get(key, "")) for key in fieldnames})


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _parse_json_cell(value: str, *, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def _resolve_registration_unit_path(row: dict[str, str], *, manifest_path: Path) -> Path:
    for column in MANIFEST_PATH_COLUMNS:
        value = (row.get(column) or "").strip()
        if value:
            path = Path(value)
            if not path.is_absolute():
                candidate = (manifest_path.parent / path).resolve()
                if candidate.exists():
                    return candidate
                return path
            return path
    raise ValueError(
        "Downstream Assertion Record input manifest row lacks a Registration Unit SQLite path. "
        f"Checked columns: {', '.join(MANIFEST_PATH_COLUMNS)}"
    )


def _connect_read_only(path: Path) -> sqlite3.Connection:
    if not path.exists():
        raise FileNotFoundError(f"Registration Unit SQLite database not found: {path}")
    uri = f"file:{path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    if not _table_exists(conn, table_name):
        return []
    return [str(row[1]) for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]


def _select_all(conn: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    if not _table_exists(conn, table_name):
        return []
    rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    return [dict(row) for row in rows]


def _artifact_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("artifact_id", "")): row for row in rows if row.get("artifact_id")}


def _participant_rows_from_summary(
    assertion_id: str,
    source_assertion_registration_id: str,
    participant_json: str,
) -> list[dict[str, Any]]:
    participant_summary = _parse_json_cell(participant_json, default={})
    rows: list[dict[str, Any]] = []
    if not isinstance(participant_summary, dict):
        return rows
    for role, value in sorted(participant_summary.items(), key=lambda item: str(item[0])):
        if isinstance(value, (dict, list, tuple)):
            value_cell = json.dumps(value, sort_keys=True, separators=(",", ":"))
        else:
            value_cell = "" if value is None else str(value)
        rows.append(
            {
                "assertion_id": assertion_id,
                "source_assertion_registration_id": source_assertion_registration_id,
                "participant_role": str(role),
                "participant_value": value_cell,
                "participant_source": "participant_summary_json",
                "source_identity_set_id": "",
                "participant_identity_kind": "",
                "participant_source_namespace": "",
                "participant_count": "",
                "participant_resolution_status": "resolved_from_participant_summary_json",
            }
        )
    return rows


def _participant_row_from_source_identity_set(source_identity_set_row: dict[str, Any]) -> dict[str, Any]:
    source_identity_set_id = str(source_identity_set_row["source_identity_set_id"])
    return {
        "assertion_id": source_identity_set_row["assertion_id"],
        "source_assertion_registration_id": source_identity_set_row["source_assertion_registration_id"],
        "participant_role": source_identity_set_row["participant_role"],
        "participant_value": f"source_identity_set:{source_identity_set_id}",
        "participant_source": "source_identity_set_reference",
        "source_identity_set_id": source_identity_set_id,
        "participant_identity_kind": source_identity_set_row["identity_kind"],
        "participant_source_namespace": source_identity_set_row["source_namespace"],
        "participant_count": source_identity_set_row["source_identity_count"],
        "participant_resolution_status": "resolved_from_source_identity_set",
    }


def _source_identity_groups(conn: sqlite3.Connection) -> dict[tuple[str, str, str, str], int]:
    """Aggregate source identity groups in SQLite, not Python.

    Layer 2 compressed fixture materialization may provide one row per source
    identity set candidate with source_identity_count representing the real set
    cardinality. Full MARK Registration Units do not have that column, so they
    use COUNT(*). This prevents loading full source_identities tables into Python
    while preserving compressed and full-corpus behavior.
    """
    if not _table_exists(conn, "source_identities"):
        return {}

    columns = set(_table_columns(conn, "source_identities"))
    if "source_identity_count" in columns:
        count_expr = """
            SUM(
                CASE
                    WHEN source_identity_count IS NULL THEN 1
                    WHEN TRIM(CAST(source_identity_count AS TEXT)) = '' THEN 1
                    ELSE CAST(source_identity_count AS INTEGER)
                END
            )
        """
    else:
        count_expr = "COUNT(*)"

    sql = f"""
        SELECT
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace,
            {count_expr} AS source_identity_count
        FROM source_identities
        GROUP BY
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace
    """
    rows = conn.execute(sql).fetchall()
    grouped: dict[tuple[str, str, str, str], int] = {}
    for row in rows:
        key = (
            str(row["assertion_registration_id"] or ""),
            str(row["identity_kind"] or ""),
            str(row["participant_role"] or ""),
            str(row["source_namespace"] or ""),
        )
        grouped[key] = int(row["source_identity_count"] or 0)
    return grouped


def _source_identity_filter(
    *,
    source_assertion_registration_id: str,
    identity_kind: str,
    participant_role: str,
    source_namespace: str,
) -> str:
    return (
        f"assertion_registration_id={source_assertion_registration_id};"
        f"identity_kind={identity_kind};"
        f"participant_role={participant_role};"
        f"source_namespace={source_namespace}"
    )


def _source_identity_set_id(
    *,
    assertion_id: str,
    source_assertion_registration_id: str,
    identity_kind: str,
    participant_role: str,
    source_namespace: str,
    source_identity_filter: str,
) -> str:
    return _stable_id(
        "sis",
        (
            assertion_id,
            source_assertion_registration_id,
            identity_kind,
            participant_role,
            source_namespace,
            source_identity_filter,
        ),
    )


def _source_record_ref_status(value: str) -> str:
    return "present" if value else "explicit_absence"


def _lineage_completeness_status(*, source_record_ref: str, artifact: dict[str, Any]) -> str:
    if source_record_ref:
        return "row_level_source_record_ref_present"
    if artifact:
        return "artifact_level_lineage_present_row_ref_absent"
    return "lineage_unresolved_row_ref_absent"


def build_assertion_records_from_manifest(
    *,
    manifest_path: str | Path,
    output_dir: str | Path,
    corpus_generation_id: str,
) -> BuildResult:
    """Build Assertion Record outputs from a governed manifest."""
    manifest = Path(manifest_path)
    output = Path(output_dir)
    corpus_generation_id = (corpus_generation_id or "").strip()

    if not corpus_generation_id:
        raise ValueError("corpus_generation_id is required")
    if not manifest.exists():
        raise FileNotFoundError(f"Downstream Assertion Record input manifest not found: {manifest}")

    manifest_rows = _read_tsv(manifest)
    if not manifest_rows:
        raise ValueError(f"Downstream Assertion Record input manifest is empty: {manifest}")

    output.mkdir(parents=True, exist_ok=True)

    index_rows: list[dict[str, Any]] = []
    participant_rows: list[dict[str, Any]] = []
    relationship_rows: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []
    payload_rows: list[dict[str, Any]] = []
    source_identity_set_rows: list[dict[str, Any]] = []
    source_identity_summary_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []
    downstream_rows: list[dict[str, Any]] = []

    for manifest_row in manifest_rows:
        registration_unit_id = (manifest_row.get("registration_unit_id") or "").strip()
        producer_family = (manifest_row.get("producer_family") or "").strip().upper()
        if not registration_unit_id:
            raise ValueError("manifest row missing registration_unit_id")
        if not producer_family:
            raise ValueError(f"manifest row for {registration_unit_id} missing producer_family")

        ru_path = _resolve_registration_unit_path(manifest_row, manifest_path=manifest)
        with _connect_read_only(ru_path) as conn:
            assertion_rows = _select_all(conn, "assertion_registrations")
            artifact_rows = _select_all(conn, "artifacts")
            source_groups = _source_identity_groups(conn)

        if not assertion_rows:
            raise ValueError(f"Registration Unit lacks assertion_registrations rows: {registration_unit_id}")

        artifacts = _artifact_map(artifact_rows)
        assertion_id_by_source: dict[str, str] = {}

        for assertion in assertion_rows:
            source_assertion_registration_id = str(assertion.get("assertion_registration_id", ""))
            assertion_type = str(assertion.get("assertion_type", ""))
            source_package_id = str(assertion.get("package_id", ""))
            source_artifact_id = str(assertion.get("artifact_id", ""))
            assertion_producer = str(assertion.get("producer_family", producer_family) or producer_family).upper()

            if not source_assertion_registration_id:
                raise ValueError(f"assertion_registrations row in {registration_unit_id} lacks assertion_registration_id")
            if not assertion_producer:
                raise ValueError(f"assertion {source_assertion_registration_id} lacks producer_family")

            policy = resolve_assertion(assertion_producer, assertion_type)
            resolver_status = policy["resolution_status"]
            validation_status = resolver_status  # Backward-compatible alias until downstream schemas are fully migrated.
            preservation_status = "preserved"
            relationship_class = policy["relationship_class"]
            source_identity_status = policy["source_identity_set_status"]

            source_key = make_source_assertion_key(
                registration_unit_id=registration_unit_id,
                source_package_id=source_package_id,
                source_artifact_id=source_artifact_id,
                source_assertion_registration_id=source_assertion_registration_id,
                assertion_type=assertion_type,
                producer_family=assertion_producer,
            )
            assertion_id = make_assertion_id(
                corpus_generation_id=corpus_generation_id,
                registration_unit_id=registration_unit_id,
                source_assertion_key=source_key,
                assertion_type=assertion_type,
                producer_family=assertion_producer,
            )
            assertion_id_by_source[source_assertion_registration_id] = assertion_id

            index_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_key": source_key,
                    "corpus_generation_id": corpus_generation_id,
                    "registration_unit_id": registration_unit_id,
                    "producer_family": assertion_producer,
                    "source_package_id": source_package_id,
                    "source_artifact_id": source_artifact_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "assertion_type": assertion_type,
                    "relationship_class": relationship_class,
                    "preservation_status": preservation_status,
                    "resolver_status": resolver_status,
                    "validation_status": validation_status,
                    "source_identity_set_status": source_identity_status,
                    "authority_context": str(assertion.get("authority_context", "")),
                    "uncertainty_context": str(assertion.get("uncertainty_context", "")),
                }
            )

            participant_rows.extend(
                _participant_rows_from_summary(
                    assertion_id,
                    source_assertion_registration_id,
                    str(assertion.get("participant_summary_json", "")),
                )
            )
            relationship_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "relationship_class": relationship_class,
                    "assertion_type": assertion_type,
                    "producer_family": assertion_producer,
                }
            )
            support_ref_json = str(assertion.get("support_ref_json", ""))
            evidence_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "evidence_basis_status": "present" if support_ref_json and support_ref_json != "{}" else "explicit_absence",
                    "support_ref_json": support_ref_json,
                }
            )
            context_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "context_status": "present",
                    "surface_role": str(assertion.get("surface_role", "")),
                    "evidence_domain": str(assertion.get("evidence_domain", "")),
                    "authority_context": str(assertion.get("authority_context", "")),
                    "uncertainty_context": str(assertion.get("uncertainty_context", "")),
                }
            )
            artifact = artifacts.get(source_artifact_id, {})
            source_record_ref = str(assertion.get("source_record_ref", "") or "")
            lineage_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "corpus_generation_id": corpus_generation_id,
                    "registration_unit_id": registration_unit_id,
                    "source_package_id": source_package_id,
                    "source_artifact_id": source_artifact_id,
                    "source_artifact_relative_path": str(artifact.get("relative_path", "")),
                    "source_artifact_sha256": str(artifact.get("sha256", "")),
                    "source_artifact_size_bytes": str(artifact.get("size_bytes", "")),
                    "source_record_ref": source_record_ref,
                    "source_record_ref_status": _source_record_ref_status(source_record_ref),
                    "lineage_completeness_status": _lineage_completeness_status(
                        source_record_ref=source_record_ref,
                        artifact=artifact,
                    ),
                }
            )
            payload_rows.append(
                {
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "source_artifact_id": source_artifact_id,
                    "relative_path": str(artifact.get("relative_path", "")),
                    "payload_json": str(assertion.get("payload_json", "")),
                }
            )
            validation_rows.append(
                {
                    "registration_unit_id": registration_unit_id,
                    "producer_family": assertion_producer,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "assertion_type": assertion_type,
                    "preservation_status": preservation_status,
                    "resolver_status": resolver_status,
                    "validation_status": validation_status,
                    "source_identity_set_status": source_identity_status,
                    "message": policy.get("note", ""),
                }
            )
            downstream_rows.append(
                {
                    "assertion_id": assertion_id,
                    "corpus_generation_id": corpus_generation_id,
                    "registration_unit_id": registration_unit_id,
                    "producer_family": assertion_producer,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "assertion_type": assertion_type,
                    "relationship_class": relationship_class,
                    "preservation_status": preservation_status,
                    "resolver_status": resolver_status,
                    "validation_status": validation_status,
                }
            )

        for (source_assertion_registration_id, identity_kind, participant_role, source_namespace), count in sorted(source_groups.items()):
            assertion_id = assertion_id_by_source.get(source_assertion_registration_id)
            if not assertion_id:
                validation_rows.append(
                    {
                        "registration_unit_id": registration_unit_id,
                        "producer_family": producer_family,
                        "source_assertion_registration_id": source_assertion_registration_id,
                        "assertion_type": "unknown",
                        "preservation_status": "not_applicable",
                        "resolver_status": "orphan_source_identity_group",
                        "validation_status": "orphan_source_identity_group",
                        "source_identity_set_status": "unresolved",
                        "message": "source_identity group did not resolve to an assertion registration",
                    }
                )
                continue
            filter_value = _source_identity_filter(
                source_assertion_registration_id=source_assertion_registration_id,
                identity_kind=identity_kind,
                participant_role=participant_role,
                source_namespace=source_namespace,
            )
            source_identity_set_id = _source_identity_set_id(
                assertion_id=assertion_id,
                source_assertion_registration_id=source_assertion_registration_id,
                identity_kind=identity_kind,
                participant_role=participant_role,
                source_namespace=source_namespace,
                source_identity_filter=filter_value,
            )
            set_row = {
                "source_identity_set_id": source_identity_set_id,
                "assertion_id": assertion_id,
                "source_assertion_registration_id": source_assertion_registration_id,
                "source_identity_table_reference": f"{registration_unit_id}:source_identities",
                "source_identity_filter": filter_value,
                "identity_kind": identity_kind,
                "participant_role": participant_role,
                "source_namespace": source_namespace,
                "source_identity_count": count,
                "lossiness_status": "lossless_by_reference",
                "resolution_status": "resolved",
                "validation_status": "not_evaluated",
                "source_identity_set_status": "resolved",
            }
            source_identity_set_rows.append(set_row)
            source_identity_summary_rows.append(
                {
                    "source_identity_set_id": source_identity_set_id,
                    "assertion_id": assertion_id,
                    "source_assertion_registration_id": source_assertion_registration_id,
                    "registration_unit_id": registration_unit_id,
                    "identity_kind": identity_kind,
                    "participant_role": participant_role,
                    "source_namespace": source_namespace,
                    "source_identity_count": count,
                }
            )
            participant_rows.append(_participant_row_from_source_identity_set(set_row))

        # Explicitly account for source-identity-not-applicable assertion types that have no groups.
        grouped_assertions = {group[0] for group in source_groups}
        for assertion in assertion_rows:
            source_assertion_registration_id = str(assertion.get("assertion_registration_id", ""))
            assertion_type = str(assertion.get("assertion_type", ""))
            assertion_producer = str(assertion.get("producer_family", producer_family) or producer_family).upper()
            if source_assertion_registration_id in grouped_assertions:
                continue
            status = policy_source_identity_set_status(assertion_producer, assertion_type)
            if status == "not_applicable":
                validation_rows.append(
                    {
                        "registration_unit_id": registration_unit_id,
                        "producer_family": assertion_producer,
                        "source_assertion_registration_id": source_assertion_registration_id,
                        "assertion_type": assertion_type,
                        "preservation_status": "preserved",
                        "resolver_status": "not_applicable_for_source_identity_sets",
                        "validation_status": "not_applicable_for_source_identity_sets",
                        "source_identity_set_status": "not_applicable",
                        "message": "artifact-level assertion without source identity set obligation",
                    }
                )

    # Deterministic output ordering.
    index_rows.sort(key=lambda row: row["assertion_id"])
    participant_rows.sort(
        key=lambda row: (
            row["assertion_id"],
            row["participant_role"],
            row.get("participant_identity_kind", ""),
            row.get("participant_source_namespace", ""),
            row["participant_value"],
        )
    )
    relationship_rows.sort(key=lambda row: row["assertion_id"])
    evidence_rows.sort(key=lambda row: row["assertion_id"])
    context_rows.sort(key=lambda row: row["assertion_id"])
    lineage_rows.sort(key=lambda row: row["assertion_id"])
    payload_rows.sort(key=lambda row: row["assertion_id"])
    source_identity_set_rows.sort(
        key=lambda row: (
            row["assertion_id"],
            row["identity_kind"],
            row["participant_role"],
            row["source_namespace"],
        )
    )
    source_identity_summary_rows.sort(
        key=lambda row: (
            row["assertion_id"],
            row["identity_kind"],
            row["participant_role"],
            row["source_namespace"],
        )
    )
    validation_rows.sort(
        key=lambda row: (
            row["registration_unit_id"],
            row["source_assertion_registration_id"],
            row["validation_status"],
        )
    )
    downstream_rows.sort(key=lambda row: row["assertion_id"])

    _write_tsv(output / "assertion_record_index.tsv", index_rows, ASSERTION_INDEX_COLUMNS)
    _write_jsonl(output / "assertion_record_index.jsonl", index_rows)
    _write_tsv(output / "assertion_record_participants.tsv", participant_rows, PARTICIPANT_COLUMNS)
    _write_tsv(output / "assertion_record_relationships.tsv", relationship_rows, RELATIONSHIP_COLUMNS)
    _write_tsv(output / "assertion_record_evidence_basis.tsv", evidence_rows, EVIDENCE_BASIS_COLUMNS)
    _write_tsv(output / "assertion_record_context.tsv", context_rows, CONTEXT_COLUMNS)
    _write_tsv(output / "assertion_record_lineage.tsv", lineage_rows, LINEAGE_COLUMNS)
    _write_tsv(output / "assertion_record_payload_references.tsv", payload_rows, PAYLOAD_REFERENCE_COLUMNS)
    _write_tsv(output / "assertion_record_source_identity_sets.tsv", source_identity_set_rows, SOURCE_IDENTITY_SET_COLUMNS)
    _write_tsv(output / "assertion_record_source_identity_summary.tsv", source_identity_summary_rows, SOURCE_IDENTITY_SUMMARY_COLUMNS)
    _write_tsv(output / "assertion_record_validation_report.tsv", validation_rows, VALIDATION_COLUMNS)
    _write_json(
        output / "assertion_record_validation_report.json",
        {
            "corpus_generation_id": corpus_generation_id,
            "registration_unit_count": len(manifest_rows),
            "assertion_record_count": len(index_rows),
            "participant_count": len(participant_rows),
            "source_identity_set_count": len(source_identity_set_rows),
            "validation_row_count": len(validation_rows),
            "preservation_status_counts": _count_values(index_rows, "preservation_status"),
            "resolver_status_counts": _count_values(index_rows, "resolver_status"),
            "validation_status_counts": _count_values(index_rows, "validation_status"),
            "lineage_completeness_status_counts": _count_values(lineage_rows, "lineage_completeness_status"),
            "non_goals": {
                "derives_topology": False,
                "characterizes_geometry": False,
                "constructs_surfaces": False,
                "emits_projection_views": False,
                "performs_rdgp_reasoning": False,
            },
        },
    )
    _write_tsv(output / "downstream_topology_input_manifest.tsv", downstream_rows, DOWNSTREAM_TOPOLOGY_COLUMNS)

    return BuildResult(
        output_dir=output,
        assertion_count=len(index_rows),
        validation_count=len(validation_rows),
        registration_unit_count=len(manifest_rows),
    )


def _count_values(rows: list[dict[str, Any]], column: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(column, ""))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def build_assertion_records(
    *,
    manifest_path: str | Path,
    output_dir: str | Path,
    corpus_generation_id: str,
) -> BuildResult:
    """Alias for compatibility with tests and future scripts."""
    return build_assertion_records_from_manifest(
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id=corpus_generation_id,
    )

#!/usr/bin/env python3
"""
Probe MARK Phase 4 golden fixture categorical counts.

Prime Directive
---------------
This script must not alter or mutate the VAP repo, VDB repo, GSC repo,
or any MARK-resident registration database.

Allowed reads:
    - VDB repo files needed to locate certified Registration Unit SQLite files
    - read-only SQLite categorical/count queries against VDB registration DBs

Allowed writes:
    - /root/Desktop only

This probe is the second-pass follow-up to:
    probe_mark_phase4_golden_fixture_feasibility.py

The first probe established that the six MARK-certified Phase 3 Registration
Unit SQLite databases expose a compact registration-facing schema:

    schema_metadata
    tep_packages
    artifacts
    assertion_registrations
    source_identities

This second probe collects exact row counts, categorical distributions,
cross-tab summaries, payload-size summaries, and fixture-design signals.

Run from MARK's VDB repository root:

    python3 scripts/mark/probe_mark_phase4_golden_fixture_categorical_counts.py

Optional:

    python3 scripts/mark/probe_mark_phase4_golden_fixture_categorical_counts.py \
        --db-root results/registration/mark_phase3_canonical \
        --query-timeout-seconds 600 \
        --max-groups-per-column 500
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import platform
import sqlite3
import sys
import tarfile
import time
import traceback
from pathlib import Path
from typing import Any
from urllib.parse import quote


PROBE_NAME = "probe_mark_phase4_golden_fixture_categorical_counts"
DEFAULT_DB_ROOT = Path("results/registration/mark_phase3_canonical")
DESKTOP_ROOT = Path("/root/Desktop")

EXPECTED_UNITS = {
    "gsc_epilepsy": {
        "producer_family": "GSC",
        "expected_relative_path": "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite",
        "fixture_role": "semantic phenotype-gene evidence",
    },
    "gsc_mitochondrial_disease": {
        "producer_family": "GSC",
        "expected_relative_path": "results/registration/mark_phase3_canonical/gsc_mitochondrial_disease/vdb.sqlite",
        "fixture_role": "semantic phenotype-gene evidence",
    },
    "vap_hg002": {
        "producer_family": "VAP",
        "expected_relative_path": "results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite",
        "fixture_role": "reference WGS variant evidence",
    },
    "vap_median_ERR10619300": {
        "producer_family": "VAP",
        "expected_relative_path": "results/registration/mark_phase3_canonical/vap_median_ERR10619300/vdb.sqlite",
        "fixture_role": "median-depth WES variant evidence",
    },
    "vap_q1_ERR10619212": {
        "producer_family": "VAP",
        "expected_relative_path": "results/registration/mark_phase3_canonical/vap_q1_ERR10619212/vdb.sqlite",
        "fixture_role": "q1-depth WES variant evidence",
    },
    "vap_q3_ERR10619225": {
        "producer_family": "VAP",
        "expected_relative_path": "results/registration/mark_phase3_canonical/vap_q3_ERR10619225/vdb.sqlite",
        "fixture_role": "q3-depth WES variant evidence",
    },
}

EXPECTED_TABLES = [
    "schema_metadata",
    "tep_packages",
    "artifacts",
    "assertion_registrations",
    "source_identities",
]

DISTRIBUTION_FIELDS = {
    "schema_metadata": [
        "key",
    ],
    "tep_packages": [
        "package_exists",
        "artifact_count",
        "manifest_count",
    ],
    "artifacts": [
        "package_id",
        "is_manifest",
    ],
    "assertion_registrations": [
        "package_id",
        "surface_role",
        "evidence_domain",
        "producer_family",
        "assertion_type",
        "authority_context",
        "uncertainty_context",
        "registration_status",
    ],
    "source_identities": [
        "identity_kind",
        "participant_role",
        "source_namespace",
        "source_label",
        "extraction_method",
    ],
}

CROSS_TABS = {
    "assertion_registrations": [
        ("producer_family", "evidence_domain"),
        ("surface_role", "evidence_domain"),
        ("evidence_domain", "assertion_type"),
        ("producer_family", "assertion_type"),
        ("registration_status", "evidence_domain"),
    ],
    "source_identities": [
        ("identity_kind", "participant_role"),
        ("identity_kind", "source_namespace"),
        ("participant_role", "source_namespace"),
        ("extraction_method", "identity_kind"),
    ],
}

PAYLOAD_FIELDS = {
    "assertion_registrations": [
        "payload_json",
        "participant_summary_json",
        "support_ref_json",
    ],
    "source_identities": [
        "payload_json",
    ],
}

FIXTURE_SIGNAL_FIELDS = {
    "tep_packages": [
        "package_id",
        "package_path",
        "package_exists",
        "artifact_count",
        "manifest_count",
    ],
    "artifacts": [
        "artifact_id",
        "package_id",
        "relative_path",
        "size_bytes",
        "sha256",
        "is_manifest",
    ],
    "assertion_registrations": [
        "assertion_registration_id",
        "package_id",
        "artifact_id",
        "surface_role",
        "evidence_domain",
        "producer_family",
        "source_record_ref",
        "assertion_type",
        "authority_context",
        "uncertainty_context",
        "registration_status",
    ],
    "source_identities": [
        "source_identity_id",
        "assertion_registration_id",
        "identity_kind",
        "participant_role",
        "source_value",
        "source_namespace",
        "source_label",
        "extraction_method",
        "source_record_ref",
    ],
}


def utc_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def safe_filename(value: str, max_len: int = 120) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in value)
    cleaned = cleaned.strip("_")
    if not cleaned:
        cleaned = "unnamed"
    return cleaned[:max_len]


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def sqlite_readonly_uri(path: Path) -> str:
    resolved = str(path.resolve())
    return f"file:{quote(resolved)}?mode=ro&immutable=1"


def ensure_desktop_output(path: Path) -> Path:
    resolved = path.resolve()
    desktop = DESKTOP_ROOT.resolve()

    if not str(resolved).startswith(str(desktop) + os.sep):
        fail(f"Refusing to write outside {desktop}: {resolved}")

    resolved.mkdir(parents=True, exist_ok=False)
    return resolved


def path_stat(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
        }

    st = path.stat()
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "mtime_iso_utc": dt.datetime.fromtimestamp(
            st.st_mtime,
            tz=dt.timezone.utc,
        ).isoformat(),
        "mode_octal": oct(st.st_mode),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }


def sqlite_sidecar_paths(db_path: Path) -> dict[str, Path]:
    raw = str(db_path)
    return {
        "db": db_path,
        "wal": Path(raw + "-wal"),
        "shm": Path(raw + "-shm"),
        "journal": Path(raw + "-journal"),
    }


def snapshot_sidecars(db_path: Path) -> dict[str, dict[str, Any]]:
    return {
        name: path_stat(path)
        for name, path in sqlite_sidecar_paths(db_path).items()
    }


def sidecar_mutation_summary(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    changed = []
    created = []
    removed = []

    for name in sorted(set(before) | set(after)):
        b = before.get(name, {"exists": False})
        a = after.get(name, {"exists": False})

        if not b.get("exists") and a.get("exists"):
            created.append(name)
            continue

        if b.get("exists") and not a.get("exists"):
            removed.append(name)
            continue

        if b.get("exists") and a.get("exists"):
            for field in ["size_bytes", "mtime_ns"]:
                if b.get(field) != a.get(field):
                    changed.append({
                        "sidecar": name,
                        "field": field,
                        "before": b.get(field),
                        "after": a.get(field),
                    })

    return {
        "created_sidecars": created,
        "removed_sidecars": removed,
        "changed_sidecars": changed,
        "non_mutation_check_status": (
            "passed" if not created and not removed and not changed else "failed"
        ),
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.write_text(text)


def write_tsv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    if fieldnames is None:
        fieldnames = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: "" if row.get(key) is None else row.get(key)
                for key in fieldnames
            })


def connect_readonly(db_path: Path) -> sqlite3.Connection:
    uri = sqlite_readonly_uri(db_path)
    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    conn.row_factory = sqlite3.Row

    # Connection/session-level settings only. These do not mutate the DB file.
    conn.execute("PRAGMA query_only = ON;")
    conn.execute("PRAGMA temp_store = MEMORY;")

    return conn


def run_query(
    conn: sqlite3.Connection,
    sql: str,
    timeout_seconds: float,
) -> list[dict[str, Any]]:
    start = time.monotonic()

    def progress_handler() -> int:
        if timeout_seconds > 0 and (time.monotonic() - start) > timeout_seconds:
            return 1
        return 0

    conn.set_progress_handler(progress_handler, 100_000)
    try:
        cur = conn.execute(sql)
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.set_progress_handler(None, 0)


def table_exists(
    conn: sqlite3.Connection,
    table_name: str,
    timeout_seconds: float,
) -> bool:
    rows = run_query(
        conn,
        f"""
        SELECT name
        FROM sqlite_master
        WHERE type IN ('table', 'view')
          AND name = '{table_name.replace("'", "''")}'
        LIMIT 1;
        """,
        timeout_seconds,
    )
    return bool(rows)


def column_names(
    conn: sqlite3.Connection,
    table_name: str,
    timeout_seconds: float,
) -> list[str]:
    rows = run_query(
        conn,
        f"PRAGMA table_info({quote_ident(table_name)});",
        timeout_seconds,
    )
    return [str(row["name"]) for row in rows]


def normalize_expr(column: str, max_value_chars: int) -> str:
    q = quote_ident(column)
    return (
        "CASE "
        f"WHEN {q} IS NULL THEN '[NULL]' "
        f"WHEN TRIM(CAST({q} AS TEXT)) = '' THEN '[BLANK]' "
        f"WHEN typeof({q}) = 'blob' THEN '[BLOB ' || length({q}) || ' bytes]' "
        f"ELSE substr(CAST({q} AS TEXT), 1, {int(max_value_chars)}) "
        "END"
    )


def collect_row_counts(
    conn: sqlite3.Connection,
    timeout_seconds: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []

    for table in EXPECTED_TABLES:
        try:
            if not table_exists(conn, table, timeout_seconds):
                rows.append({
                    "table_name": table,
                    "table_exists": False,
                    "row_count": "not_available",
                })
                continue

            count_rows = run_query(
                conn,
                f"SELECT COUNT(*) AS row_count FROM {quote_ident(table)};",
                timeout_seconds,
            )
            rows.append({
                "table_name": table,
                "table_exists": True,
                "row_count": count_rows[0]["row_count"],
            })
        except Exception as exc:
            rows.append({
                "table_name": table,
                "table_exists": "unknown",
                "row_count": "query_failed",
            })
            errors.append({
                "query_family": "row_count",
                "table_name": table,
                "field_name": "",
                "error": str(exc),
            })

    return rows, errors


def collect_distributions(
    conn: sqlite3.Connection,
    timeout_seconds: float,
    max_groups_per_column: int,
    max_value_chars: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []

    for table, fields in DISTRIBUTION_FIELDS.items():
        try:
            if not table_exists(conn, table, timeout_seconds):
                continue

            available_columns = set(column_names(conn, table, timeout_seconds))

            for field in fields:
                if field not in available_columns:
                    rows.append({
                        "table_name": table,
                        "field_name": field,
                        "field_value": "not_available",
                        "row_count": "not_available",
                        "query_status": "missing_column",
                    })
                    continue

                value_expr = normalize_expr(field, max_value_chars)

                sql = f"""
                SELECT
                    {value_expr} AS field_value,
                    COUNT(*) AS row_count
                FROM {quote_ident(table)}
                GROUP BY field_value
                ORDER BY row_count DESC, field_value ASC
                LIMIT {int(max_groups_per_column)};
                """

                dist_rows = run_query(conn, sql, timeout_seconds)

                for dist_row in dist_rows:
                    rows.append({
                        "table_name": table,
                        "field_name": field,
                        "field_value": dist_row.get("field_value"),
                        "row_count": dist_row.get("row_count"),
                        "query_status": "passed",
                    })

        except Exception as exc:
            errors.append({
                "query_family": "distribution",
                "table_name": table,
                "field_name": "",
                "error": str(exc),
            })

    return rows, errors


def collect_cross_tabs(
    conn: sqlite3.Connection,
    timeout_seconds: float,
    max_groups_per_pair: int,
    max_value_chars: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []

    for table, pairs in CROSS_TABS.items():
        try:
            if not table_exists(conn, table, timeout_seconds):
                continue

            available_columns = set(column_names(conn, table, timeout_seconds))

            for field_a, field_b in pairs:
                if field_a not in available_columns or field_b not in available_columns:
                    rows.append({
                        "table_name": table,
                        "field_a": field_a,
                        "field_b": field_b,
                        "value_a": "not_available",
                        "value_b": "not_available",
                        "row_count": "not_available",
                        "query_status": "missing_column",
                    })
                    continue

                expr_a = normalize_expr(field_a, max_value_chars)
                expr_b = normalize_expr(field_b, max_value_chars)

                sql = f"""
                SELECT
                    {expr_a} AS value_a,
                    {expr_b} AS value_b,
                    COUNT(*) AS row_count
                FROM {quote_ident(table)}
                GROUP BY value_a, value_b
                ORDER BY row_count DESC, value_a ASC, value_b ASC
                LIMIT {int(max_groups_per_pair)};
                """

                tab_rows = run_query(conn, sql, timeout_seconds)

                for tab_row in tab_rows:
                    rows.append({
                        "table_name": table,
                        "field_a": field_a,
                        "field_b": field_b,
                        "value_a": tab_row.get("value_a"),
                        "value_b": tab_row.get("value_b"),
                        "row_count": tab_row.get("row_count"),
                        "query_status": "passed",
                    })

        except Exception as exc:
            errors.append({
                "query_family": "cross_tab",
                "table_name": table,
                "field_name": "",
                "error": str(exc),
            })

    return rows, errors


def collect_payload_size_summaries(
    conn: sqlite3.Connection,
    timeout_seconds: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []

    for table, fields in PAYLOAD_FIELDS.items():
        try:
            if not table_exists(conn, table, timeout_seconds):
                continue

            available_columns = set(column_names(conn, table, timeout_seconds))

            for field in fields:
                if field not in available_columns:
                    rows.append({
                        "table_name": table,
                        "field_name": field,
                        "non_null_count": "not_available",
                        "null_count": "not_available",
                        "min_length": "not_available",
                        "max_length": "not_available",
                        "avg_length": "not_available",
                        "total_length": "not_available",
                        "query_status": "missing_column",
                    })
                    continue

                q = quote_ident(field)
                sql = f"""
                SELECT
                    SUM(CASE WHEN {q} IS NOT NULL THEN 1 ELSE 0 END) AS non_null_count,
                    SUM(CASE WHEN {q} IS NULL THEN 1 ELSE 0 END) AS null_count,
                    MIN(length({q})) AS min_length,
                    MAX(length({q})) AS max_length,
                    AVG(length({q})) AS avg_length,
                    SUM(length({q})) AS total_length
                FROM {quote_ident(table)};
                """

                size_rows = run_query(conn, sql, timeout_seconds)
                size_row = size_rows[0] if size_rows else {}

                rows.append({
                    "table_name": table,
                    "field_name": field,
                    "non_null_count": size_row.get("non_null_count"),
                    "null_count": size_row.get("null_count"),
                    "min_length": size_row.get("min_length"),
                    "max_length": size_row.get("max_length"),
                    "avg_length": size_row.get("avg_length"),
                    "total_length": size_row.get("total_length"),
                    "query_status": "passed",
                })

        except Exception as exc:
            errors.append({
                "query_family": "payload_size",
                "table_name": table,
                "field_name": "",
                "error": str(exc),
            })

    return rows, errors


def collect_fixture_signal_completeness(
    conn: sqlite3.Connection,
    timeout_seconds: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []

    for table, fields in FIXTURE_SIGNAL_FIELDS.items():
        try:
            if not table_exists(conn, table, timeout_seconds):
                continue

            available_columns = set(column_names(conn, table, timeout_seconds))

            for field in fields:
                if field not in available_columns:
                    rows.append({
                        "table_name": table,
                        "field_name": field,
                        "total_rows": "not_available",
                        "non_null_count": "not_available",
                        "null_count": "not_available",
                        "blank_count": "not_available",
                        "query_status": "missing_column",
                    })
                    continue

                q = quote_ident(field)
                sql = f"""
                SELECT
                    COUNT(*) AS total_rows,
                    SUM(CASE WHEN {q} IS NOT NULL THEN 1 ELSE 0 END) AS non_null_count,
                    SUM(CASE WHEN {q} IS NULL THEN 1 ELSE 0 END) AS null_count,
                    SUM(CASE
                        WHEN {q} IS NOT NULL AND TRIM(CAST({q} AS TEXT)) = ''
                        THEN 1 ELSE 0 END
                    ) AS blank_count
                FROM {quote_ident(table)};
                """

                comp_rows = run_query(conn, sql, timeout_seconds)
                comp_row = comp_rows[0] if comp_rows else {}

                rows.append({
                    "table_name": table,
                    "field_name": field,
                    "total_rows": comp_row.get("total_rows"),
                    "non_null_count": comp_row.get("non_null_count"),
                    "null_count": comp_row.get("null_count"),
                    "blank_count": comp_row.get("blank_count"),
                    "query_status": "passed",
                })

        except Exception as exc:
            errors.append({
                "query_family": "fixture_signal_completeness",
                "table_name": table,
                "field_name": "",
                "error": str(exc),
            })

    return rows, errors


def probe_one_unit(
    db_root: Path,
    unit_label: str,
    expected: dict[str, Any],
    output_root: Path,
    timeout_seconds: float,
    max_groups_per_column: int,
    max_groups_per_pair: int,
    max_value_chars: int,
) -> dict[str, Any]:
    unit_outdir = output_root / unit_label
    unit_outdir.mkdir(parents=True, exist_ok=True)

    db_path = db_root / unit_label / "vdb.sqlite"
    db_abs = db_path.resolve()

    result: dict[str, Any] = {
        "unit_label": unit_label,
        "expected": expected,
        "db_relative_path": str(db_path),
        "db_absolute_path": str(db_abs),
        "probe_started_at": now_iso(),
        "probe_status": "not_started",
        "errors": [],
    }

    before_sidecars = snapshot_sidecars(db_abs)
    write_json(unit_outdir / "00_pre_probe_file_state.json", before_sidecars)

    if not db_abs.exists():
        result["probe_status"] = "missing_db"
        result["errors"].append(f"Database not found: {db_abs}")
        after_sidecars = snapshot_sidecars(db_abs)
        write_json(unit_outdir / "99_post_probe_file_state.json", after_sidecars)
        result["non_mutation_audit"] = sidecar_mutation_summary(before_sidecars, after_sidecars)
        write_json(unit_outdir / "unit_probe_summary.json", result)
        return result

    all_errors: list[dict[str, Any]] = []

    try:
        conn = connect_readonly(db_abs)

        try:
            row_counts, errors = collect_row_counts(conn, timeout_seconds)
            all_errors.extend(errors)

            distributions, errors = collect_distributions(
                conn=conn,
                timeout_seconds=timeout_seconds,
                max_groups_per_column=max_groups_per_column,
                max_value_chars=max_value_chars,
            )
            all_errors.extend(errors)

            cross_tabs, errors = collect_cross_tabs(
                conn=conn,
                timeout_seconds=timeout_seconds,
                max_groups_per_pair=max_groups_per_pair,
                max_value_chars=max_value_chars,
            )
            all_errors.extend(errors)

            payload_sizes, errors = collect_payload_size_summaries(
                conn=conn,
                timeout_seconds=timeout_seconds,
            )
            all_errors.extend(errors)

            completeness, errors = collect_fixture_signal_completeness(
                conn=conn,
                timeout_seconds=timeout_seconds,
            )
            all_errors.extend(errors)

            write_tsv(unit_outdir / "01_row_counts.tsv", row_counts)
            write_tsv(unit_outdir / "02_categorical_distributions.tsv", distributions)
            write_tsv(unit_outdir / "03_cross_tab_distributions.tsv", cross_tabs)
            write_tsv(unit_outdir / "04_payload_size_summary.tsv", payload_sizes)
            write_tsv(unit_outdir / "05_fixture_signal_completeness.tsv", completeness)
            write_tsv(unit_outdir / "06_query_errors.tsv", all_errors)

            result.update({
                "probe_status": "passed" if not all_errors else "passed_with_query_notes",
                "row_counts": row_counts,
                "distribution_row_count": len(distributions),
                "cross_tab_row_count": len(cross_tabs),
                "payload_size_summary_count": len(payload_sizes),
                "fixture_signal_completeness_count": len(completeness),
                "query_error_count": len(all_errors),
            })

        finally:
            conn.close()

    except Exception as exc:
        result["probe_status"] = "failed"
        result["errors"].append(str(exc))
        write_text(
            unit_outdir / "probe_exception_traceback.txt",
            traceback.format_exc(),
        )

    after_sidecars = snapshot_sidecars(db_abs)
    write_json(unit_outdir / "99_post_probe_file_state.json", after_sidecars)

    result["non_mutation_audit"] = sidecar_mutation_summary(
        before_sidecars,
        after_sidecars,
    )
    result["probe_finished_at"] = now_iso()

    write_json(unit_outdir / "unit_probe_summary.json", result)
    write_text(unit_outdir / "unit_probe_summary.md", render_unit_report(result))

    return result


def render_unit_report(result: dict[str, Any]) -> str:
    audit = result.get("non_mutation_audit", {})
    row_counts = result.get("row_counts", [])

    lines = [
        f"# Phase 4 Golden Fixture Categorical Count Probe: {result.get('unit_label')}",
        "",
        "## Database",
        "",
        f"- Relative path: `{result.get('db_relative_path')}`",
        f"- Absolute path: `{result.get('db_absolute_path')}`",
        f"- Probe status: `{result.get('probe_status')}`",
        f"- Non-mutation check: `{audit.get('non_mutation_check_status', 'not_available')}`",
        "",
        "## Row Counts",
        "",
        "| Table | Exists | Row Count |",
        "|---|---|---:|",
    ]

    for row in row_counts:
        lines.append(
            "| `{}` | `{}` | `{}` |".format(
                row.get("table_name", ""),
                row.get("table_exists", ""),
                row.get("row_count", ""),
            )
        )

    lines.extend([
        "",
        "## Probe Outputs",
        "",
        "- `01_row_counts.tsv`",
        "- `02_categorical_distributions.tsv`",
        "- `03_cross_tab_distributions.tsv`",
        "- `04_payload_size_summary.tsv`",
        "- `05_fixture_signal_completeness.tsv`",
        "- `06_query_errors.tsv`",
        "",
        "## Prime Directive Check",
        "",
        "This probe opened the SQLite database through a read-only immutable URI and wrote outputs only under `/root/Desktop`.",
        "",
    ])

    if result.get("errors"):
        lines.extend([
            "## Errors",
            "",
        ])
        for error in result["errors"]:
            lines.append(f"- `{error}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_global_report(
    repo_root: Path,
    db_root: Path,
    output_root: Path,
    unit_results: list[dict[str, Any]],
) -> str:
    passed = sum(1 for row in unit_results if row.get("probe_status") == "passed")
    noted = sum(1 for row in unit_results if row.get("probe_status") == "passed_with_query_notes")
    failed = sum(1 for row in unit_results if row.get("probe_status") == "failed")
    missing = sum(1 for row in unit_results if row.get("probe_status") == "missing_db")
    mutation_failed = sum(
        1 for row in unit_results
        if row.get("non_mutation_audit", {}).get("non_mutation_check_status") == "failed"
    )

    lines = [
        "# MARK Phase 4 Golden Fixture Categorical Count Probe",
        "",
        "## Purpose",
        "",
        "This report summarizes categorical counts from the certified Phase 3 VDB Registration Unit SQLite files on MARK.",
        "",
        "The goal is to identify the minimal categorical and count coverage needed for a lightweight local Phase 4 golden fixture.",
        "",
        "The probe is read-only with respect to the VDB repository and all SQLite inputs.",
        "",
        "## Execution Context",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Registration Unit root: `{db_root}`",
        f"- Output root: `{output_root}`",
        f"- Probe timestamp: `{now_iso()}`",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.platform()}`",
        "",
        "## Summary",
        "",
        f"- Units expected: `{len(EXPECTED_UNITS)}`",
        f"- Units passed: `{passed}`",
        f"- Units passed with query notes: `{noted}`",
        f"- Units failed: `{failed}`",
        f"- Units missing: `{missing}`",
        f"- Non-mutation failures: `{mutation_failed}`",
        "",
        "## Unit Results",
        "",
        "| Unit | Producer | Status | Non-mutation | Query errors |",
        "|---|---|---|---|---:|",
    ]

    for row in unit_results:
        audit = row.get("non_mutation_audit", {})
        expected = row.get("expected", {})
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | {} |".format(
                row.get("unit_label", ""),
                expected.get("producer_family", ""),
                row.get("probe_status", ""),
                audit.get("non_mutation_check_status", "not_available"),
                row.get("query_error_count", 0),
            )
        )

    lines.extend([
        "",
        "## Fixture Design Interpretation",
        "",
        "Use this probe to decide which categorical values must be represented in the local Phase 4 golden fixture.",
        "",
        "The local fixture should not reproduce full MARK payload volume.",
        "",
        "It should reproduce the registration-facing categorical surface needed to exercise:",
        "",
        "```text",
        "Registration Unit inventory",
        "Corpus Generation selection",
        "Assertion Record indexing readiness",
        "source identity visibility",
        "namespace visibility",
        "producer-family representation",
        "evidence-domain representation",
        "status vocabulary handling",
        "payload-size/null handling without large payloads",
        "```",
        "",
        "## Prime Directive",
        "",
        "This probe writes only to `/root/Desktop`.",
        "",
        "It must not write to, modify, migrate, vacuum, index, checkpoint, or otherwise mutate any VDB, VAP, or GSC repository file.",
        "",
    ])

    if mutation_failed:
        lines.extend([
            "## Warning",
            "",
            "At least one non-mutation sidecar audit reported a change. Inspect per-unit `00_pre_probe_file_state.json` and `99_post_probe_file_state.json` before trusting the run.",
            "",
        ])

    return "\n".join(lines) + "\n"


def merge_unit_tsvs(
    output_root: Path,
    unit_labels: list[str],
    filename: str,
    merged_filename: str,
) -> None:
    merged_rows: list[dict[str, Any]] = []

    for unit_label in unit_labels:
        path = output_root / unit_label / filename
        if not path.exists():
            continue

        with path.open("r", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                merged = {"unit_label": unit_label}
                merged.update(row)
                merged_rows.append(merged)

    write_tsv(output_root / merged_filename, merged_rows)


def make_tarball(output_root: Path) -> Path:
    tar_path = output_root.with_suffix(".tgz")
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(output_root, arcname=output_root.name)
    return tar_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect categorical/count signals for Phase 4 golden fixture design from MARK Phase 3 certified Registration Units."
    )
    parser.add_argument(
        "--db-root",
        default=str(DEFAULT_DB_ROOT),
        help="Registration Unit root relative to the current VDB repo root.",
    )
    parser.add_argument(
        "--output-root",
        default="",
        help="Optional explicit output directory under /root/Desktop. Default creates timestamped directory.",
    )
    parser.add_argument(
        "--query-timeout-seconds",
        type=float,
        default=600.0,
        help="Per-query timeout in seconds. Use 0 to disable timeout.",
    )
    parser.add_argument(
        "--max-groups-per-column",
        type=int,
        default=500,
        help="Maximum grouped values to retain per categorical field.",
    )
    parser.add_argument(
        "--max-groups-per-pair",
        type=int,
        default=500,
        help="Maximum grouped values to retain per cross-tab field pair.",
    )
    parser.add_argument(
        "--max-value-chars",
        type=int,
        default=240,
        help="Maximum characters retained for grouped categorical values.",
    )
    parser.add_argument(
        "--units",
        nargs="*",
        default=list(EXPECTED_UNITS.keys()),
        help="Optional subset of unit labels to probe.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    repo_root = Path.cwd().resolve()
    db_root = (repo_root / args.db_root).resolve()

    if not db_root.exists():
        fail(f"Registration Unit root does not exist: {db_root}")

    if args.output_root:
        output_root = Path(args.output_root)
    else:
        output_root = DESKTOP_ROOT / f"{PROBE_NAME}_{utc_timestamp()}"

    output_root = ensure_desktop_output(output_root)

    manifest = {
        "probe_name": PROBE_NAME,
        "probe_started_at": now_iso(),
        "repo_root": str(repo_root),
        "db_root": str(db_root),
        "output_root": str(output_root),
        "prime_directive": {
            "allowed_reads": [
                "VDB repo SQLite registration databases",
                "registration-facing categorical/count queries",
            ],
            "allowed_writes": [
                "/root/Desktop only",
            ],
            "forbidden_actions": [
                "write to VDB repo",
                "write to VAP repo",
                "write to GSC repo",
                "mutate SQLite inputs",
                "migrate SQLite inputs",
                "vacuum SQLite inputs",
                "checkpoint SQLite inputs",
                "create indexes in SQLite inputs",
                "dump full biological payloads",
            ],
        },
        "args": vars(args),
        "expected_units": EXPECTED_UNITS,
        "expected_tables": EXPECTED_TABLES,
        "distribution_fields": DISTRIBUTION_FIELDS,
        "cross_tabs": CROSS_TABS,
        "payload_fields": PAYLOAD_FIELDS,
        "fixture_signal_fields": FIXTURE_SIGNAL_FIELDS,
    }
    write_json(output_root / "00_probe_manifest.json", manifest)

    unit_results = []
    unit_labels = list(args.units)

    for unit_label in unit_labels:
        if unit_label not in EXPECTED_UNITS:
            print(f"WARNING: Unknown unit label requested: {unit_label}", file=sys.stderr)
            expected = {
                "producer_family": "unknown",
                "expected_relative_path": str(DEFAULT_DB_ROOT / unit_label / "vdb.sqlite"),
                "fixture_role": "unknown",
            }
        else:
            expected = EXPECTED_UNITS[unit_label]

        print(f"[probe-counts] {unit_label}")
        result = probe_one_unit(
            db_root=db_root,
            unit_label=unit_label,
            expected=expected,
            output_root=output_root,
            timeout_seconds=args.query_timeout_seconds,
            max_groups_per_column=args.max_groups_per_column,
            max_groups_per_pair=args.max_groups_per_pair,
            max_value_chars=args.max_value_chars,
        )
        unit_results.append(result)

    global_summary = {
        "probe_name": PROBE_NAME,
        "probe_finished_at": now_iso(),
        "repo_root": str(repo_root),
        "db_root": str(db_root),
        "output_root": str(output_root),
        "unit_results": unit_results,
    }

    write_json(output_root / "99_global_probe_summary.json", global_summary)

    summary_rows = []
    non_mutation_rows = []

    for row in unit_results:
        audit = row.get("non_mutation_audit", {})
        expected = row.get("expected", {})

        summary_rows.append({
            "unit_label": row.get("unit_label"),
            "producer_family": expected.get("producer_family"),
            "db_absolute_path": row.get("db_absolute_path"),
            "probe_status": row.get("probe_status"),
            "query_error_count": row.get("query_error_count", 0),
            "non_mutation_check_status": audit.get("non_mutation_check_status"),
        })

        non_mutation_rows.append({
            "unit_label": row.get("unit_label"),
            "db_absolute_path": row.get("db_absolute_path"),
            "non_mutation_check_status": audit.get("non_mutation_check_status"),
            "created_sidecars": ",".join(audit.get("created_sidecars", [])),
            "removed_sidecars": ",".join(audit.get("removed_sidecars", [])),
            "changed_sidecars": json.dumps(audit.get("changed_sidecars", []), sort_keys=True),
        })

    write_tsv(output_root / "98_global_unit_summary.tsv", summary_rows)
    write_tsv(output_root / "97_global_non_mutation_audit.tsv", non_mutation_rows)

    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="01_row_counts.tsv",
        merged_filename="90_merged_row_counts.tsv",
    )
    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="02_categorical_distributions.tsv",
        merged_filename="91_merged_categorical_distributions.tsv",
    )
    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="03_cross_tab_distributions.tsv",
        merged_filename="92_merged_cross_tab_distributions.tsv",
    )
    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="04_payload_size_summary.tsv",
        merged_filename="93_merged_payload_size_summary.tsv",
    )
    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="05_fixture_signal_completeness.tsv",
        merged_filename="94_merged_fixture_signal_completeness.tsv",
    )
    merge_unit_tsvs(
        output_root=output_root,
        unit_labels=unit_labels,
        filename="06_query_errors.tsv",
        merged_filename="95_merged_query_errors.tsv",
    )

    write_text(
        output_root / "README.md",
        render_global_report(
            repo_root=repo_root,
            db_root=db_root,
            output_root=output_root,
            unit_results=unit_results,
        ),
    )

    tar_path = make_tarball(output_root)

    print()
    print("Categorical count probe complete.")
    print(f"Output directory: {output_root}")
    print(f"Tarball: {tar_path}")
    print()
    print("Prime Directive: no repo writes were performed by this script.")
    print("Inspect 97_global_non_mutation_audit.tsv for sidecar/stat changes.")
    print("Inspect 91_merged_categorical_distributions.tsv for fixture category coverage.")
    print("Inspect 92_merged_cross_tab_distributions.tsv for fixture pair coverage.")

    failed = any(row.get("probe_status") == "failed" for row in unit_results)
    mutation_failed = any(
        row.get("non_mutation_audit", {}).get("non_mutation_check_status") == "failed"
        for row in unit_results
    )

    if failed or mutation_failed:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

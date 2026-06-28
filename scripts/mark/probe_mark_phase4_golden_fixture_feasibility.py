#!/usr/bin/env python3
"""
Probe MARK Phase 4 golden fixture feasibility.

Prime Directive
---------------
This script must not alter or mutate the VAP repo, VDB repo, GSC repo,
or any MARK-resident registration database.

Allowed reads:
    - VDB repo files needed to locate certified Registration Unit SQLite files
    - read-only SQLite metadata and capped table previews from VDB registration DBs

Allowed writes:
    - /root/Desktop only

The probe is designed to run from MARK's VDB repository root.

Example:
    python3 scripts/mark/probe_mark_phase4_golden_fixture_feasibility.py

Optional:
    python3 scripts/mark/probe_mark_phase4_golden_fixture_feasibility.py \
        --db-root results/registration/mark_phase3_canonical \
        --head-rows 5 \
        --max-cell-chars 240
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import platform
import re
import sqlite3
import sys
import tarfile
import traceback
from pathlib import Path
from typing import Any
from urllib.parse import quote


PROBE_NAME = "probe_mark_phase4_golden_fixture_feasibility"
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

CANDIDATE_SURFACE_KEYWORDS = {
    "registration": [
        "registration",
        "registered",
        "registry",
        "package",
        "unit",
    ],
    "artifact": [
        "artifact",
        "file",
        "path",
        "checksum",
        "role",
    ],
    "assertion": [
        "assertion",
        "claim",
        "relationship",
        "predicate",
        "participant",
        "evidence_basis",
    ],
    "source_identity": [
        "source_identity",
        "identity",
        "entity",
        "identifier",
        "namespace",
        "canonical",
        "resolution",
    ],
    "provenance": [
        "provenance",
        "lineage",
        "run",
        "producer",
        "tep",
        "manifest",
        "created",
        "timestamp",
    ],
    "validation_certification": [
        "validation",
        "validated",
        "certification",
        "certified",
        "status",
        "readiness",
    ],
    "metadata": [
        "metadata",
        "meta",
        "summary",
        "inventory",
        "config",
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
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
    if not cleaned:
        cleaned = "unnamed"
    return cleaned[:max_len]


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def sqlite_readonly_uri(path: Path) -> str:
    # immutable=1 avoids lock/shm behavior and reinforces the no-mutation rule.
    # These Phase 3 certified registration DBs are expected to be closed,
    # checkpointed SQLite files.
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
            comparable_fields = ["size_bytes", "mtime_ns"]
            for field in comparable_fields:
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


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        field_set: list[str] = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    field_set.append(key)
        fieldnames = field_set

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
    conn.execute("PRAGMA query_only = ON;")
    return conn


def fetch_all_dicts(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    cur = conn.execute(sql)
    return [dict(row) for row in cur.fetchall()]


def fetch_pragmas(conn: sqlite3.Connection) -> dict[str, Any]:
    pragmas: dict[str, Any] = {}
    for pragma_name in [
        "database_list",
        "schema_version",
        "user_version",
        "application_id",
        "page_size",
        "page_count",
        "freelist_count",
        "encoding",
        "journal_mode",
    ]:
        try:
            rows = fetch_all_dicts(conn, f"PRAGMA {pragma_name};")
            pragmas[pragma_name] = rows
        except Exception as exc:
            pragmas[pragma_name] = {
                "error": str(exc),
            }
    return pragmas


def fetch_sqlite_master(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return fetch_all_dicts(
        conn,
        """
        SELECT
            type,
            name,
            tbl_name,
            rootpage,
            sql
        FROM sqlite_master
        WHERE type IN ('table', 'view', 'index', 'trigger')
        ORDER BY type, name;
        """,
    )


def fetch_table_columns(conn: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    rows = fetch_all_dicts(conn, f"PRAGMA table_info({quote_ident(table_name)});")
    for row in rows:
        row["table_name"] = table_name
    return rows


def build_table_inventory(
    master_rows: list[dict[str, Any]],
    column_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    columns_by_table: dict[str, list[dict[str, Any]]] = {}
    for row in column_rows:
        columns_by_table.setdefault(str(row["table_name"]), []).append(row)

    inventory = []
    for row in master_rows:
        if row.get("type") not in {"table", "view"}:
            continue

        name = str(row.get("name"))
        sql = str(row.get("sql") or "")
        cols = columns_by_table.get(name, [])
        inventory.append({
            "object_type": row.get("type"),
            "object_name": name,
            "column_count": len(cols),
            "column_names": ",".join(str(col.get("name")) for col in cols),
            "without_rowid_detected": "WITHOUT ROWID" in sql.upper(),
            "sql_preview": sql[:500],
        })

    return inventory


def candidate_surface_matches(
    table_name: str,
    columns: list[dict[str, Any]],
) -> dict[str, Any]:
    column_names = [str(col.get("name", "")) for col in columns]
    searchable = " ".join([table_name] + column_names).lower()

    matched_categories = []
    matched_terms = []

    for category, terms in CANDIDATE_SURFACE_KEYWORDS.items():
        category_hits = [term for term in terms if term.lower() in searchable]
        if category_hits:
            matched_categories.append(category)
            matched_terms.extend(category_hits)

    return {
        "matched_categories": ",".join(matched_categories),
        "matched_terms": ",".join(sorted(set(matched_terms))),
        "candidate_score": len(set(matched_categories)),
    }


def safe_preview_expr(column_name: str, max_cell_chars: int) -> str:
    q = quote_ident(column_name)
    return (
        "CASE "
        f"WHEN {q} IS NULL THEN 'NULL' "
        f"WHEN typeof({q}) = 'blob' THEN '[BLOB ' || length({q}) || ' bytes]' "
        f"ELSE substr(CAST({q} AS TEXT), 1, {int(max_cell_chars)}) "
        f"END AS {q}"
    )


def preview_table(
    conn: sqlite3.Connection,
    table_name: str,
    columns: list[dict[str, Any]],
    head_rows: int,
    max_cell_chars: int,
) -> list[dict[str, Any]]:
    if head_rows <= 0:
        return []

    column_names = [str(col.get("name")) for col in columns if col.get("name")]
    if not column_names:
        return []

    exprs = [safe_preview_expr(name, max_cell_chars) for name in column_names]
    sql = (
        "SELECT "
        + ", ".join(exprs)
        + f" FROM {quote_ident(table_name)}"
        + f" LIMIT {int(head_rows)};"
    )

    return fetch_all_dicts(conn, sql)


def write_preview_outputs(
    conn: sqlite3.Connection,
    unit_outdir: Path,
    table_inventory: list[dict[str, Any]],
    columns_by_table: dict[str, list[dict[str, Any]]],
    head_rows: int,
    max_cell_chars: int,
    max_preview_tables: int,
) -> list[dict[str, Any]]:
    preview_dir = unit_outdir / "table_head_previews"
    preview_dir.mkdir(parents=True, exist_ok=True)

    preview_summary = []
    previewed = 0

    for table in table_inventory:
        if table.get("object_type") != "table":
            continue

        table_name = str(table["object_name"])

        # Internal SQLite tables are usually not useful for fixture strategy.
        if table_name.startswith("sqlite_"):
            continue

        if previewed >= max_preview_tables:
            preview_summary.append({
                "table_name": table_name,
                "preview_status": "skipped_max_preview_tables_reached",
                "preview_rows": 0,
                "error": "",
            })
            continue

        try:
            rows = preview_table(
                conn=conn,
                table_name=table_name,
                columns=columns_by_table.get(table_name, []),
                head_rows=head_rows,
                max_cell_chars=max_cell_chars,
            )

            outpath = preview_dir / f"{safe_filename(table_name)}.tsv"
            write_tsv(outpath, rows)

            preview_summary.append({
                "table_name": table_name,
                "preview_status": "previewed",
                "preview_rows": len(rows),
                "preview_path": str(outpath),
                "error": "",
            })
            previewed += 1

        except Exception as exc:
            preview_summary.append({
                "table_name": table_name,
                "preview_status": "failed",
                "preview_rows": 0,
                "preview_path": "",
                "error": str(exc),
            })

    return preview_summary


def probe_one_unit(
    repo_root: Path,
    db_root: Path,
    unit_label: str,
    expected: dict[str, Any],
    output_root: Path,
    head_rows: int,
    max_cell_chars: int,
    max_preview_tables: int,
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

    try:
        conn = connect_readonly(db_abs)

        try:
            pragmas = fetch_pragmas(conn)
            master_rows = fetch_sqlite_master(conn)

            table_names = [
                str(row["name"])
                for row in master_rows
                if row.get("type") in {"table", "view"}
            ]

            column_rows: list[dict[str, Any]] = []
            columns_by_table: dict[str, list[dict[str, Any]]] = {}

            for table_name in table_names:
                try:
                    cols = fetch_table_columns(conn, table_name)
                    columns_by_table[table_name] = cols
                    column_rows.extend(cols)
                except Exception as exc:
                    result["errors"].append(
                        f"Failed column inspection for {table_name}: {exc}"
                    )

            table_inventory = build_table_inventory(master_rows, column_rows)

            candidate_rows = []
            for table in table_inventory:
                table_name = str(table["object_name"])
                cols = columns_by_table.get(table_name, [])
                matches = candidate_surface_matches(table_name, cols)
                candidate_rows.append({
                    "object_type": table.get("object_type"),
                    "table_name": table_name,
                    "column_count": table.get("column_count"),
                    "column_names": table.get("column_names"),
                    **matches,
                })

            candidate_rows = sorted(
                candidate_rows,
                key=lambda row: (
                    -int(row.get("candidate_score") or 0),
                    str(row.get("table_name")),
                ),
            )

            preview_summary = write_preview_outputs(
                conn=conn,
                unit_outdir=unit_outdir,
                table_inventory=table_inventory,
                columns_by_table=columns_by_table,
                head_rows=head_rows,
                max_cell_chars=max_cell_chars,
                max_preview_tables=max_preview_tables,
            )

            write_json(unit_outdir / "01_sqlite_pragmas.json", pragmas)
            write_tsv(unit_outdir / "02_sqlite_master.tsv", master_rows)
            write_tsv(unit_outdir / "03_table_inventory.tsv", table_inventory)
            write_tsv(unit_outdir / "04_column_inventory.tsv", column_rows)
            write_tsv(unit_outdir / "05_candidate_registration_surface_tables.tsv", candidate_rows)
            write_tsv(unit_outdir / "06_table_head_preview_summary.tsv", preview_summary)

            schema_lines = []
            for row in master_rows:
                if row.get("sql"):
                    schema_lines.append(f"-- {row.get('type')} {row.get('name')}")
                    schema_lines.append(str(row.get("sql")) + ";")
                    schema_lines.append("")
            write_text(unit_outdir / "07_schema_dump.sql", "\n".join(schema_lines))

            result.update({
                "probe_status": "passed",
                "sqlite_object_count": len(master_rows),
                "table_or_view_count": len(table_inventory),
                "column_count": len(column_rows),
                "previewed_table_count": sum(
                    1 for row in preview_summary
                    if row.get("preview_status") == "previewed"
                ),
                "candidate_surface_table_count": sum(
                    1 for row in candidate_rows
                    if int(row.get("candidate_score") or 0) > 0
                ),
                "highest_candidate_tables": candidate_rows[:20],
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
    highest = result.get("highest_candidate_tables", [])

    lines = [
        f"# Phase 4 Golden Fixture Feasibility Probe: {result.get('unit_label')}",
        "",
        "## Database",
        "",
        f"- Relative path: `{result.get('db_relative_path')}`",
        f"- Absolute path: `{result.get('db_absolute_path')}`",
        f"- Probe status: `{result.get('probe_status')}`",
        f"- Non-mutation check: `{audit.get('non_mutation_check_status', 'not_available')}`",
        "",
        "## Object Summary",
        "",
        f"- SQLite objects: `{result.get('sqlite_object_count', 'not_available')}`",
        f"- Tables/views: `{result.get('table_or_view_count', 'not_available')}`",
        f"- Columns: `{result.get('column_count', 'not_available')}`",
        f"- Previewed tables: `{result.get('previewed_table_count', 'not_available')}`",
        f"- Candidate registration-surface tables: `{result.get('candidate_surface_table_count', 'not_available')}`",
        "",
        "## Highest Candidate Registration Surface Tables",
        "",
        "| Table | Candidate Score | Matched Categories | Matched Terms |",
        "|---|---:|---|---|",
    ]

    for row in highest[:15]:
        lines.append(
            "| `{}` | {} | `{}` | `{}` |".format(
                row.get("table_name", ""),
                row.get("candidate_score", ""),
                row.get("matched_categories", ""),
                row.get("matched_terms", ""),
            )
        )

    if result.get("errors"):
        lines.extend([
            "",
            "## Errors",
            "",
        ])
        for error in result["errors"]:
            lines.append(f"- `{error}`")

    lines.extend([
        "",
        "## Prime Directive Check",
        "",
        "This probe opened the SQLite database through a read-only immutable URI and wrote outputs only under `/root/Desktop`.",
        "",
    ])

    return "\n".join(lines) + "\n"


def render_global_report(
    repo_root: Path,
    db_root: Path,
    output_root: Path,
    unit_results: list[dict[str, Any]],
) -> str:
    passed = sum(1 for row in unit_results if row.get("probe_status") == "passed")
    failed = sum(1 for row in unit_results if row.get("probe_status") == "failed")
    missing = sum(1 for row in unit_results if row.get("probe_status") == "missing_db")
    mutation_failed = sum(
        1 for row in unit_results
        if row.get("non_mutation_audit", {}).get("non_mutation_check_status") == "failed"
    )

    lines = [
        "# MARK Phase 4 Golden Fixture Feasibility Probe",
        "",
        "## Purpose",
        "",
        "This report scouts the certified Phase 3 VDB Registration Unit SQLite files on MARK to determine the minimal registration-surface shape needed for a lightweight local Phase 4 golden fixture.",
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
        f"- Units failed: `{failed}`",
        f"- Units missing: `{missing}`",
        f"- Non-mutation failures: `{mutation_failed}`",
        "",
        "## Unit Results",
        "",
        "| Unit | Producer | Status | Non-mutation | Tables/views | Columns | Candidate tables |",
        "|---|---|---|---|---:|---:|---:|",
    ]

    for row in unit_results:
        audit = row.get("non_mutation_audit", {})
        expected = row.get("expected", {})
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | {} | {} | {} |".format(
                row.get("unit_label", ""),
                expected.get("producer_family", ""),
                row.get("probe_status", ""),
                audit.get("non_mutation_check_status", "not_available"),
                row.get("table_or_view_count", "not_available"),
                row.get("column_count", "not_available"),
                row.get("candidate_surface_table_count", "not_available"),
            )
        )

    lines.extend([
        "",
        "## Fixture Feasibility Interpretation",
        "",
        "A local Phase 4 golden fixture should emulate the minimal inspection-facing Registration Unit surface discovered here, not the full biological payload volume of the MARK databases.",
        "",
        "The fixture should preserve:",
        "",
        "```text",
        "Registration Unit identity",
        "producer family",
        "source package identity",
        "artifact registration visibility",
        "assertion registration visibility",
        "source identity visibility",
        "namespace visibility",
        "validation status visibility",
        "certification status visibility",
        "read-only inspection behavior",
        "non-mutation evidence",
        "```",
        "",
        "The intended development path is:",
        "",
        "```text",
        "1. Use this probe output to identify the minimal Phase 3 registration-surface tables.",
        "2. Build tiny deterministic local SQLite Registration Units with the same inspection-facing shape.",
        "3. Implement Phase 4.1 Registration Unit inventory against the local golden fixture.",
        "4. Re-run the same inspector against the MARK-certified heavy Registration Units.",
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


def make_tarball(output_root: Path) -> Path:
    tar_path = output_root.with_suffix(".tgz")
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(output_root, arcname=output_root.name)
    return tar_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe MARK Phase 4 golden fixture feasibility from VDB Phase 3 certified Registration Units."
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
        "--head-rows",
        type=int,
        default=5,
        help="Number of preview rows per table. Use 0 to disable previews.",
    )
    parser.add_argument(
        "--max-cell-chars",
        type=int,
        default=240,
        help="Maximum characters per previewed cell.",
    )
    parser.add_argument(
        "--max-preview-tables",
        type=int,
        default=250,
        help="Maximum number of tables to preview per database.",
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
                "SQLite metadata",
                "capped SQLite table previews",
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
            ],
        },
        "args": vars(args),
        "expected_units": EXPECTED_UNITS,
    }
    write_json(output_root / "00_probe_manifest.json", manifest)

    unit_results = []

    for unit_label in args.units:
        if unit_label not in EXPECTED_UNITS:
            print(f"WARNING: Unknown unit label requested: {unit_label}", file=sys.stderr)
            expected = {
                "producer_family": "unknown",
                "expected_relative_path": str(DEFAULT_DB_ROOT / unit_label / "vdb.sqlite"),
                "fixture_role": "unknown",
            }
        else:
            expected = EXPECTED_UNITS[unit_label]

        print(f"[probe] {unit_label}")
        result = probe_one_unit(
            repo_root=repo_root,
            db_root=db_root,
            unit_label=unit_label,
            expected=expected,
            output_root=output_root,
            head_rows=args.head_rows,
            max_cell_chars=args.max_cell_chars,
            max_preview_tables=args.max_preview_tables,
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
            "non_mutation_check_status": audit.get("non_mutation_check_status"),
            "sqlite_object_count": row.get("sqlite_object_count"),
            "table_or_view_count": row.get("table_or_view_count"),
            "column_count": row.get("column_count"),
            "candidate_surface_table_count": row.get("candidate_surface_table_count"),
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
    print("Probe complete.")
    print(f"Output directory: {output_root}")
    print(f"Tarball: {tar_path}")
    print()
    print("Prime Directive: no repo writes were performed by this script.")
    print("Inspect 97_global_non_mutation_audit.tsv for sidecar/stat changes.")

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
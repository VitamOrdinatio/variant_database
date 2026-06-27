#!/usr/bin/env python3
"""
MARK Phase 3 registration efficacy probe.

Run from variant_database repo root:

    python scripts/mark/probe_mark_phase3_registration_efficacy.py

Outputs:
    /root/Desktop/vdb_phase3_registration_efficacy_<timestamp>.md
    /root/Desktop/vdb_phase3_registration_efficacy_<timestamp>.json
    /root/Desktop/vdb_phase3_registration_efficacy_<timestamp>_db_summary.tsv
    /root/Desktop/vdb_phase3_registration_efficacy_<timestamp>_identity_summary.tsv
"""

from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path.cwd()
REG_ROOT = REPO_ROOT / "results" / "registration" / "mark_phase3_canonical"
OUT_DIR = Path("/root/Desktop")


REQUIRED_TABLES = {
    "tep_packages",
    "artifacts",
    "assertion_registrations",
    "source_identities",
    "schema_metadata",
}


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def fetchall_dict(cur: sqlite3.Cursor, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    cur.execute(query, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def scalar(cur: sqlite3.Cursor, query: str, params: tuple[Any, ...] = ()) -> Any:
    cur.execute(query, params)
    return cur.fetchone()[0]


def table_exists(cur: sqlite3.Cursor, table: str) -> bool:
    return scalar(
        cur,
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ) == 1


def inspect_db(db_path: Path) -> dict[str, Any]:
    label = db_path.parent.name
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    tables = {
        row["name"]
        for row in fetchall_dict(
            cur,
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
        )
    }

    missing_tables = sorted(REQUIRED_TABLES - tables)

    counts: dict[str, int] = {}
    for table in sorted(tables):
        counts[table] = int(scalar(cur, f'SELECT COUNT(*) FROM "{table}"'))

    assertion_breakdown = []
    identity_breakdown = []
    artifact_breakdown = []
    package_rows = []
    sample_assertions = []
    sample_identities = []

    if not missing_tables:
        assertion_breakdown = fetchall_dict(
            cur,
            """
            SELECT
                producer_family,
                surface_role,
                evidence_domain,
                assertion_type,
                authority_context,
                uncertainty_context,
                registration_status,
                COUNT(*) AS n
            FROM assertion_registrations
            GROUP BY
                producer_family,
                surface_role,
                evidence_domain,
                assertion_type,
                authority_context,
                uncertainty_context,
                registration_status
            ORDER BY producer_family, surface_role, evidence_domain, assertion_type
            """,
        )

        identity_breakdown = fetchall_dict(
            cur,
            """
            SELECT
                identity_kind,
                participant_role,
                source_namespace,
                extraction_method,
                COUNT(*) AS n
            FROM source_identities
            GROUP BY
                identity_kind,
                participant_role,
                source_namespace,
                extraction_method
            ORDER BY identity_kind, participant_role, source_namespace, extraction_method
            """,
        )

        artifact_breakdown = fetchall_dict(
            cur,
            """
            SELECT
                is_manifest,
                COUNT(*) AS n,
                SUM(size_bytes) AS total_size_bytes
            FROM artifacts
            GROUP BY is_manifest
            ORDER BY is_manifest
            """,
        )

        package_rows = fetchall_dict(
            cur,
            """
            SELECT
                package_id,
                package_path,
                package_exists,
                artifact_count,
                manifest_count
            FROM tep_packages
            ORDER BY package_id
            """,
        )

        sample_assertions = fetchall_dict(
            cur,
            """
            SELECT
                assertion_registration_id,
                package_id,
                artifact_id,
                surface_role,
                evidence_domain,
                producer_family,
                assertion_type,
                source_record_ref,
                authority_context,
                uncertainty_context,
                registration_status,
                substr(participant_summary_json, 1, 220) AS participant_summary_preview,
                substr(support_ref_json, 1, 220) AS support_ref_preview,
                substr(payload_json, 1, 220) AS payload_preview
            FROM assertion_registrations
            ORDER BY assertion_registration_id
            LIMIT 12
            """,
        )

        sample_identities = fetchall_dict(
            cur,
            """
            SELECT
                source_identity_id,
                assertion_registration_id,
                identity_kind,
                participant_role,
                source_value,
                source_namespace,
                source_label,
                extraction_method,
                source_record_ref,
                substr(payload_json, 1, 220) AS payload_preview
            FROM source_identities
            ORDER BY source_identity_id
            LIMIT 20
            """,
        )

    con.close()

    invariants: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: str) -> None:
        invariants.append({"name": name, "passed": bool(passed), "detail": detail})

    add_check(
        "required_tables_present",
        not missing_tables,
        "missing=" + ",".join(missing_tables) if missing_tables else "all required tables present",
    )

    if not missing_tables:
        add_check(
            "single_tep_package",
            counts.get("tep_packages", 0) == 1,
            f"tep_packages={counts.get('tep_packages', 0)}",
        )
        add_check(
            "artifacts_registered",
            counts.get("artifacts", 0) > 0,
            f"artifacts={counts.get('artifacts', 0)}",
        )
        add_check(
            "assertions_registered",
            counts.get("assertion_registrations", 0) > 0,
            f"assertion_registrations={counts.get('assertion_registrations', 0)}",
        )
        add_check(
            "source_identities_registered",
            counts.get("source_identities", 0) > 0,
            f"source_identities={counts.get('source_identities', 0)}",
        )

        null_source_refs = scalar(
            cur := sqlite3.connect(db_path).cursor(),
            "SELECT COUNT(*) FROM assertion_registrations WHERE package_id IS NULL OR artifact_id IS NULL",
        )
        cur.connection.close()
        add_check(
            "assertion_package_artifact_refs_present",
            null_source_refs == 0,
            f"assertion rows missing package/artifact refs={null_source_refs}",
        )

        con2 = sqlite3.connect(db_path)
        cur2 = con2.cursor()
        non_registered = scalar(
            cur2,
            "SELECT COUNT(*) FROM assertion_registrations WHERE registration_status != 'registered'",
        )
        add_check(
            "all_assertions_registered_status",
            non_registered == 0,
            f"non-registered assertion rows={non_registered}",
        )

        missing_identity_refs = scalar(
            cur2,
            """
            SELECT COUNT(*)
            FROM source_identities si
            LEFT JOIN assertion_registrations ar
              ON si.assertion_registration_id = ar.assertion_registration_id
            WHERE ar.assertion_registration_id IS NULL
            """,
        )
        add_check(
            "source_identity_assertion_refs_resolve",
            missing_identity_refs == 0,
            f"source identities with missing assertion refs={missing_identity_refs}",
        )

        producer_count = scalar(
            cur2,
            "SELECT COUNT(DISTINCT producer_family) FROM assertion_registrations",
        )
        add_check(
            "producer_family_present",
            producer_count >= 1,
            f"distinct producer_family count={producer_count}",
        )

        namespace_count = scalar(
            cur2,
            "SELECT COUNT(DISTINCT source_namespace) FROM source_identities",
        )
        add_check(
            "source_namespaces_present",
            namespace_count >= 1,
            f"distinct source_namespace count={namespace_count}",
        )

        con2.close()

    passed_all = all(x["passed"] for x in invariants)

    return {
        "label": label,
        "db_path": str(db_path),
        "tables": sorted(tables),
        "missing_tables": missing_tables,
        "counts": counts,
        "package_rows": package_rows,
        "artifact_breakdown": artifact_breakdown,
        "assertion_breakdown": assertion_breakdown,
        "identity_breakdown": identity_breakdown,
        "sample_assertions": sample_assertions,
        "sample_identities": sample_identities,
        "invariants": invariants,
        "passed_all_invariants": passed_all,
    }


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = now_tag()

    db_paths = sorted(REG_ROOT.glob("*/vdb.sqlite"))

    report: dict[str, Any] = {
        "probe": "vdb_phase3_registration_efficacy",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(REPO_ROOT),
        "registration_root": str(REG_ROOT),
        "db_count": len(db_paths),
        "databases": [],
    }

    for db in db_paths:
        report["databases"].append(inspect_db(db))

    db_summary_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []

    for item in report["databases"]:
        counts = item["counts"]
        db_summary_rows.append(
            {
                "label": item["label"],
                "db_path": item["db_path"],
                "passed_all_invariants": item["passed_all_invariants"],
                "tep_packages": counts.get("tep_packages", 0),
                "artifacts": counts.get("artifacts", 0),
                "assertion_registrations": counts.get("assertion_registrations", 0),
                "source_identities": counts.get("source_identities", 0),
                "schema_metadata": counts.get("schema_metadata", 0),
                "missing_tables": ",".join(item["missing_tables"]),
            }
        )

        for row in item["identity_breakdown"]:
            out = {"label": item["label"]}
            out.update(row)
            identity_rows.append(out)

    md_path = OUT_DIR / f"vdb_phase3_registration_efficacy_{tag}.md"
    json_path = OUT_DIR / f"vdb_phase3_registration_efficacy_{tag}.json"
    db_tsv_path = OUT_DIR / f"vdb_phase3_registration_efficacy_{tag}_db_summary.tsv"
    identity_tsv_path = OUT_DIR / f"vdb_phase3_registration_efficacy_{tag}_identity_summary.tsv"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    write_tsv(
        db_tsv_path,
        db_summary_rows,
        [
            "label",
            "db_path",
            "passed_all_invariants",
            "tep_packages",
            "artifacts",
            "assertion_registrations",
            "source_identities",
            "schema_metadata",
            "missing_tables",
        ],
    )

    write_tsv(
        identity_tsv_path,
        identity_rows,
        [
            "label",
            "identity_kind",
            "participant_role",
            "source_namespace",
            "extraction_method",
            "n",
        ],
    )

    lines: list[str] = []
    lines.append("# VDB Phase 3 Registration Efficacy Probe")
    lines.append("")
    lines.append(f"- Generated UTC: `{report['generated_at_utc']}`")
    lines.append(f"- Repository root: `{REPO_ROOT}`")
    lines.append(f"- Registration root: `{REG_ROOT}`")
    lines.append(f"- Database count: `{len(db_paths)}`")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("")
    for row in db_summary_rows:
        status = "PASS" if row["passed_all_invariants"] else "REVIEW"
        lines.append(
            f"- **{row['label']}**: {status}; "
            f"artifacts={row['artifacts']}, "
            f"assertions={row['assertion_registrations']}, "
            f"source_identities={row['source_identities']}"
        )
    lines.append("")

    lines.append("## Database Summary")
    lines.append("")
    lines.append("| label | pass | artifacts | assertions | source identities |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in db_summary_rows:
        lines.append(
            f"| {row['label']} | {row['passed_all_invariants']} | "
            f"{row['artifacts']} | {row['assertion_registrations']} | {row['source_identities']} |"
        )
    lines.append("")

    for item in report["databases"]:
        lines.append(f"## {item['label']}")
        lines.append("")
        lines.append(f"- DB: `{item['db_path']}`")
        lines.append(f"- Passed all invariants: `{item['passed_all_invariants']}`")
        lines.append("")

        lines.append("### Invariant Checks")
        lines.append("")
        lines.append("| check | pass | detail |")
        lines.append("|---|---:|---|")
        for inv in item["invariants"]:
            lines.append(f"| {inv['name']} | {inv['passed']} | {inv['detail']} |")
        lines.append("")

        lines.append("### Table Counts")
        lines.append("")
        lines.append("| table | rows |")
        lines.append("|---|---:|")
        for table, count in sorted(item["counts"].items()):
            lines.append(f"| {table} | {count} |")
        lines.append("")

        lines.append("### Assertion Registration Breakdown")
        lines.append("")
        if item["assertion_breakdown"]:
            lines.append("| producer | surface_role | evidence_domain | assertion_type | authority | uncertainty | status | n |")
            lines.append("|---|---|---|---|---|---|---|---:|")
            for row in item["assertion_breakdown"]:
                lines.append(
                    "| "
                    + " | ".join(
                        str(row.get(k, ""))
                        for k in [
                            "producer_family",
                            "surface_role",
                            "evidence_domain",
                            "assertion_type",
                            "authority_context",
                            "uncertainty_context",
                            "registration_status",
                            "n",
                        ]
                    )
                    + " |"
                )
        else:
            lines.append("_No assertion breakdown available._")
        lines.append("")

        lines.append("### Source Identity Breakdown")
        lines.append("")
        if item["identity_breakdown"]:
            lines.append("| identity_kind | participant_role | source_namespace | extraction_method | n |")
            lines.append("|---|---|---|---|---:|")
            for row in item["identity_breakdown"]:
                lines.append(
                    "| "
                    + " | ".join(
                        str(row.get(k, ""))
                        for k in [
                            "identity_kind",
                            "participant_role",
                            "source_namespace",
                            "extraction_method",
                            "n",
                        ]
                    )
                    + " |"
                )
        else:
            lines.append("_No source identity breakdown available._")
        lines.append("")

        lines.append("### Sample Assertion Registrations")
        lines.append("")
        lines.append("```text")
        for row in item["sample_assertions"]:
            lines.append(json.dumps(row, ensure_ascii=False))
        lines.append("```")
        lines.append("")

        lines.append("### Sample Source Identities")
        lines.append("")
        lines.append("```text")
        for row in item["sample_identities"]:
            lines.append(json.dumps(row, ensure_ascii=False))
        lines.append("```")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    print("MARK Phase 3 registration efficacy probe complete")
    print(f"Markdown report: {md_path}")
    print(f"JSON report:     {json_path}")
    print(f"DB summary TSV:  {db_tsv_path}")
    print(f"Identity TSV:    {identity_tsv_path}")


if __name__ == "__main__":
    main()
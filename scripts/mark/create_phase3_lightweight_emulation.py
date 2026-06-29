#!/usr/bin/env python3
"""
Create a MARK-derived lightweight Phase 4 Registration Unit golden fixture.

This script compresses the six certified Phase 3 VDB Registration Unit SQLite
files on MARK into a retrievable, real-row-derived lightweight fixture for
Phase 4 development on sys76.

Prime Directive:
    - Read MARK-resident source SQLite files only.
    - Write only to /root/Desktop/.
    - Do not write into MARK VDB, VAP, GSC, or other producer repositories.
    - Do not mutate source SQLite files.

Canonical MARK source corpus:
    /root/dev/portfolio_projects/variant_database/
    results/registration/mark_phase3_canonical/

Output:
    /root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>/
    /root/Desktop/phase4_registration_unit_golden_fixture_<timestamp>.tgz
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sqlite3
import sys
import tarfile
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, NoReturn


SCRIPT_PATH = "scripts/mark/create_phase3_lightweight_emulation.py"
SCRIPT_VERSION = "1.0.0"
FIXTURE_ID = "phase4_registration_unit_golden_fixture"
FIXTURE_VERSION = "v1"

SOURCE_VDB_REPO_ROOT = Path("/root/dev/portfolio_projects/variant_database")
SOURCE_CORPUS_ROOT = SOURCE_VDB_REPO_ROOT / "results/registration/mark_phase3_canonical"
OUTPUT_PARENT = Path("/root/Desktop")

PORTABLE_ROOT_NAME = "phase4_registration_unit_golden_fixture"
REGISTRATION_UNIT_FIXTURE_NAME = "mark_phase3_canonical_6sqlite_lightweight"

REGISTRATION_UNITS: dict[str, Path] = {
    "gsc_epilepsy": SOURCE_CORPUS_ROOT / "gsc_epilepsy/vdb.sqlite",
    "gsc_mitochondrial_disease": SOURCE_CORPUS_ROOT / "gsc_mitochondrial_disease/vdb.sqlite",
    "vap_hg002": SOURCE_CORPUS_ROOT / "vap_hg002/vdb.sqlite",
    "vap_median_ERR10619300": SOURCE_CORPUS_ROOT / "vap_median_ERR10619300/vdb.sqlite",
    "vap_q1_ERR10619212": SOURCE_CORPUS_ROOT / "vap_q1_ERR10619212/vdb.sqlite",
    "vap_q3_ERR10619225": SOURCE_CORPUS_ROOT / "vap_q3_ERR10619225/vdb.sqlite",
}

REQUIRED_TABLES = [
    "schema_metadata",
    "tep_packages",
    "artifacts",
    "assertion_registrations",
    "source_identities",
]

FULL_COPY_TABLES = [
    "schema_metadata",
    "tep_packages",
    "artifacts",
    "assertion_registrations",
]

COMPRESSED_TABLE = "source_identities"

# Initial deterministic compression limits. These are intentionally conservative
# so the fixture remains lightweight while preserving real-row category coverage.
MAX_ROWS_PER_ASSERTION_REGISTRATION = 10
MAX_ROWS_PER_IDENTITY_KIND = 20
MAX_ROWS_PER_SOURCE_NAMESPACE = 20
MAX_ROWS_PER_PARTICIPANT_ROLE = 20
MAX_ROWS_PER_EXTRACTION_METHOD = 20
MAX_NULL_SOURCE_RECORD_REF_ROWS = 20
MAX_NON_NULL_SOURCE_RECORD_REF_ROWS = 20
MAX_PRIORITY_SEED_ROWS = 100
MAX_FALLBACK_ROWS = 100

PROGRESS_EVERY_ROWS = 1_000_000
OUTPUT_DB_SUFFIX = "vdb.sqlite"

PRIORITY_GENE_SYMBOLS = ["POLG", "TWNK", "SCN1A", "DEPDC5"]
PRIORITY_ENSEMBL_IDS = [
    "ENSG00000140521",  # POLG
    "ENSG00000107815",  # TWNK
    "ENSG00000144285",  # SCN1A
    "ENSG00000100150",  # DEPDC5
]
PRIORITY_VARIANT_FRAGMENTS = [
    "15:89333596:T:TTGC",
    "89333596",
]
PRIORITY_TERMS = PRIORITY_GENE_SYMBOLS + PRIORITY_ENSEMBL_IDS + PRIORITY_VARIANT_FRAGMENTS
PRIORITY_TERMS_UPPER = [term.upper() for term in PRIORITY_TERMS]

CATEGORY_SUMMARY_FIELDS = {
    "artifacts": ["is_manifest"],
    "assertion_registrations": [
        "producer_family",
        "surface_role",
        "evidence_domain",
        "assertion_type",
        "registration_status",
    ],
    "source_identities": [
        "identity_kind",
        "participant_role",
        "source_namespace",
        "extraction_method",
    ],
    "tep_packages": ["package_exists"],
}

AUTHORITY_STATEMENT = (
    "This fixture is a compressed, real-row-derived development substrate. "
    "It is not biological truth, clinical truth, Phase 4 certification, "
    "or a substitute for MARK full-corpus smoketesting."
)


@dataclass(frozen=True)
class FileState:
    path: str
    exists: bool
    size_bytes: int | None
    mtime_ns: int | None


@dataclass
class SourceAudit:
    registration_unit_label: str
    source_database_path: str
    source_database_exists: bool
    source_database_size_bytes: int | None
    source_database_mtime_ns_before: int | None
    source_database_mtime_ns_after: int | None
    source_sha256_or_skip_reason: str
    open_status: str
    query_only_status: str
    table_count: int | None
    required_table_status: str
    schema_metadata_row_count: int | None
    tep_packages_row_count: int | None
    artifacts_row_count: int | None
    assertion_registrations_row_count: int | None
    source_identities_row_count: int | None
    source_identity_identity_kind_count: int | None
    source_identity_namespace_count: int | None
    source_identity_participant_role_count: int | None
    source_identity_extraction_method_count: int | None
    null_source_record_ref_count: int | None
    non_null_source_record_ref_count: int | None
    post_extraction_state_status: str
    audit_status: str
    notes: str


@dataclass
class FixtureAudit:
    registration_unit_label: str
    output_database_relative_path: str
    output_database_exists: bool
    output_database_size_bytes: int | None
    open_status: str
    required_table_status: str
    schema_metadata_row_count: int | None
    tep_packages_row_count: int | None
    artifacts_row_count: int | None
    assertion_registrations_row_count: int | None
    source_identities_row_count: int | None
    foreign_key_check_status_if_applicable: str
    integrity_check_status: str
    audit_status: str


@dataclass
class CopiedTableLineage:
    registration_unit_label: str
    source_database_path: str
    source_table: str
    output_database_relative_path: str
    output_table: str
    source_row_count: int
    output_row_count: int
    copy_mode: str
    copy_status: str


@dataclass
class SelectedSourceIdentityLineage:
    registration_unit_label: str
    source_database_path: str
    source_database_size_bytes: int
    source_table: str
    source_rowid: int
    source_primary_key: str
    output_database_relative_path: str
    output_table: str
    output_primary_key: str
    selection_reason: str
    selection_rank: int
    identity_kind: str
    source_namespace: str
    participant_role: str
    extraction_method: str
    source_record_ref_state: str


@dataclass
class SelectedSourceIdentity:
    source_rowid: int
    row: dict[str, Any]
    reasons: set[str] = field(default_factory=set)
    rank: int = 0


@dataclass
class UnitResult:
    registration_unit_label: str
    source_database_path: str
    output_database_relative_path: str
    source_database_size_bytes: int
    output_database_size_bytes: int
    output_database_sha256: str
    source_identity_rows_scanned: int
    source_identity_rows_selected: int
    priority_seed_rows_selected: int
    null_source_record_ref_selected: int
    non_null_source_record_ref_selected: int
    warnings: list[str]


def fail(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def timestamp_for_path() -> str:
    return datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_stat(path: Path) -> FileState:
    if not path.exists():
        return FileState(str(path), False, None, None)
    stat = path.stat()
    return FileState(str(path), True, stat.st_size, stat.st_mtime_ns)


def ensure_under(path: Path, allowed_root: Path, label: str) -> None:
    resolved = path.resolve()
    allowed = allowed_root.resolve()
    if resolved != allowed and not str(resolved).startswith(str(allowed) + "/"):
        fail(f"Refusing {label} outside allowed root: {resolved} not under {allowed}")


def reset_output_dir(path: Path) -> None:
    ensure_under(path, OUTPUT_PARENT, "output directory")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_tsv(path: Path, rows: Iterable[Any], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            if hasattr(row, "__dataclass_fields__"):
                value = asdict(row)
            else:
                value = dict(row)
            writer.writerow(
                {key: "" if value.get(key) is None else value.get(key) for key in fieldnames}
            )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def repo_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def sqlite_readonly_uri(path: Path) -> str:
    # Paths used on MARK are simple absolute POSIX paths. Keeping the URI readable
    # improves operator inspection and matches prior MARK scripts.
    return f"file:{path.as_posix()}?mode=ro&immutable=1"


def open_source_connection(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(sqlite_readonly_uri(path), uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=ON;")
    return conn


def open_output_connection(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (table,)
    ).fetchone()
    return row is not None


def table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return [str(row["name"]) for row in rows]


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({quote_identifier(table)})").fetchall()
    return [str(row["name"]) for row in rows]


def table_create_sql(conn: sqlite3.Connection, table: str) -> str:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    if row is None or not row["sql"]:
        fail(f"Could not retrieve CREATE TABLE SQL for {table}")
    return str(row["sql"])


def count_rows(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) AS row_count FROM {quote_identifier(table)}").fetchone()
    return int(row["row_count"])


def required_table_status(conn: sqlite3.Connection) -> str:
    existing = set(table_names(conn))
    missing = [table for table in REQUIRED_TABLES if table not in existing]
    if missing:
        return "missing:" + ",".join(missing)
    return "passed"


def validate_source_paths() -> None:
    if not SOURCE_VDB_REPO_ROOT.exists():
        fail(f"SOURCE_VDB_REPO_ROOT does not exist: {SOURCE_VDB_REPO_ROOT}")
    if not SOURCE_CORPUS_ROOT.exists():
        fail(f"SOURCE_CORPUS_ROOT does not exist: {SOURCE_CORPUS_ROOT}")
    for label, path in REGISTRATION_UNITS.items():
        if not path.exists():
            fail(f"Required source SQLite missing for {label}: {path}")
        if not path.is_file():
            fail(f"Required source path is not a file for {label}: {path}")


def create_required_tables_from_source(
    source_conn: sqlite3.Connection,
    output_conn: sqlite3.Connection,
) -> None:
    for table in REQUIRED_TABLES:
        create_sql = table_create_sql(source_conn, table)
        output_conn.execute(create_sql)
    output_conn.commit()


def insert_rows(
    conn: sqlite3.Connection,
    table: str,
    columns: list[str],
    rows: list[dict[str, Any]],
) -> None:
    if not rows:
        return
    quoted_columns = ", ".join(quote_identifier(col) for col in columns)
    placeholders = ", ".join("?" for _ in columns)
    sql = f"INSERT INTO {quote_identifier(table)} ({quoted_columns}) VALUES ({placeholders})"
    values = [[row.get(col) for col in columns] for row in rows]
    conn.executemany(sql, values)


def select_rows_ordered(
    conn: sqlite3.Connection,
    table: str,
    columns: list[str],
    chunk_size: int = 1000,
) -> Iterable[list[dict[str, Any]]]:
    quoted_columns = ", ".join(quote_identifier(col) for col in columns)
    sql = f"SELECT {quoted_columns} FROM {quote_identifier(table)} ORDER BY rowid"
    cursor = conn.execute(sql)
    while True:
        batch = cursor.fetchmany(chunk_size)
        if not batch:
            break
        yield [dict(row) for row in batch]


def copy_full_table(
    unit_label: str,
    source_path: Path,
    source_conn: sqlite3.Connection,
    output_conn: sqlite3.Connection,
    output_db_rel: str,
    table: str,
) -> CopiedTableLineage:
    columns = table_columns(source_conn, table)
    source_count = count_rows(source_conn, table)
    copied = 0

    for batch in select_rows_ordered(source_conn, table, columns):
        insert_rows(output_conn, table, columns, batch)
        copied += len(batch)

    output_conn.commit()
    output_count = count_rows(output_conn, table)
    status = "passed" if source_count == output_count == copied else "failed"
    if status != "passed":
        fail(
            f"Full-copy row count mismatch for {unit_label}.{table}: "
            f"source={source_count}, copied={copied}, output={output_count}"
        )

    return CopiedTableLineage(
        registration_unit_label=unit_label,
        source_database_path=str(source_path),
        source_table=table,
        output_database_relative_path=output_db_rel,
        output_table=table,
        source_row_count=source_count,
        output_row_count=output_count,
        copy_mode="copy_all_rows",
        copy_status=status,
    )


def get_assertion_registration_ids(conn: sqlite3.Connection) -> list[str]:
    if not table_exists(conn, "assertion_registrations"):
        return []
    columns = set(table_columns(conn, "assertion_registrations"))
    if "assertion_registration_id" not in columns:
        return []
    rows = conn.execute(
        """
        SELECT assertion_registration_id
        FROM assertion_registrations
        ORDER BY assertion_registration_id
        """
    ).fetchall()
    return [str(row["assertion_registration_id"]) for row in rows]


def source_record_ref_state(value: Any) -> str:
    if value is None:
        return "null"
    if str(value).strip() == "":
        return "blank"
    return "non_null"


def priority_terms_found(row: dict[str, Any]) -> list[str]:
    search_parts = [
        row.get("source_value"),
        row.get("source_label"),
        row.get("payload_json"),
        row.get("source_record_ref"),
    ]
    haystack = "\n".join("" if part is None else str(part) for part in search_parts).upper()
    return [term for term in PRIORITY_TERMS_UPPER if term in haystack]


def add_selection(
    selected: dict[int, SelectedSourceIdentity],
    source_rowid: int,
    row: dict[str, Any],
    reason: str,
) -> None:
    if source_rowid not in selected:
        selected[source_rowid] = SelectedSourceIdentity(
            source_rowid=source_rowid,
            row=row,
            rank=len(selected) + 1,
        )
    selected[source_rowid].reasons.add(reason)


def increment_if_under(
    counter: dict[str, int],
    key: Any,
    limit: int,
) -> bool:
    key_s = "" if key is None else str(key)
    if counter[key_s] < limit:
        counter[key_s] += 1
        return True
    return False


def stream_select_source_identities(
    unit_label: str,
    source_path: Path,
    source_conn: sqlite3.Connection,
    output_db_rel: str,
    warnings: list[str],
) -> tuple[
    list[dict[str, Any]],
    list[SelectedSourceIdentityLineage],
    dict[str, Any],
]:
    columns = table_columns(source_conn, COMPRESSED_TABLE)
    required_cols = {
        "source_identity_id",
        "assertion_registration_id",
        "identity_kind",
        "participant_role",
        "source_namespace",
        "extraction_method",
        "source_record_ref",
    }
    missing_cols = sorted(required_cols - set(columns))
    if missing_cols:
        fail(f"{unit_label}: source_identities missing required columns: {missing_cols}")

    assertion_ids = set(get_assertion_registration_ids(source_conn))

    assertion_counter: dict[str, int] = defaultdict(int)
    identity_kind_counter: dict[str, int] = defaultdict(int)
    namespace_counter: dict[str, int] = defaultdict(int)
    participant_role_counter: dict[str, int] = defaultdict(int)
    extraction_method_counter: dict[str, int] = defaultdict(int)
    category_seen = {
        "identity_kind": defaultdict(int),
        "source_namespace": defaultdict(int),
        "participant_role": defaultdict(int),
        "extraction_method": defaultdict(int),
    }

    selected: dict[int, SelectedSourceIdentity] = {}
    null_selected = 0
    non_null_selected = 0
    fallback_selected = 0
    priority_selected = 0
    priority_matches_by_term: dict[str, int] = defaultdict(int)
    null_seen = 0
    non_null_seen = 0
    rows_scanned = 0

    quoted_columns = ", ".join(quote_identifier(col) for col in columns)
    sql = (
        f"SELECT rowid AS __source_rowid, {quoted_columns} "
        f"FROM {quote_identifier(COMPRESSED_TABLE)} ORDER BY rowid"
    )
    cursor = source_conn.execute(sql)

    while True:
        batch = cursor.fetchmany(10_000)
        if not batch:
            break

        for sqlite_row in batch:
            raw = dict(sqlite_row)
            source_rowid = int(raw.pop("__source_rowid"))
            row = raw
            rows_scanned += 1

            if PROGRESS_EVERY_ROWS and rows_scanned % PROGRESS_EVERY_ROWS == 0:
                print(f"[{unit_label}] scanned {rows_scanned:,} source_identities rows")

            assertion_id = str(row.get("assertion_registration_id", ""))
            identity_kind = str(row.get("identity_kind", ""))
            source_namespace = str(row.get("source_namespace", ""))
            participant_role = str(row.get("participant_role", ""))
            extraction_method = str(row.get("extraction_method", ""))
            ref_state = source_record_ref_state(row.get("source_record_ref"))

            category_seen["identity_kind"][identity_kind] += 1
            category_seen["source_namespace"][source_namespace] += 1
            category_seen["participant_role"][participant_role] += 1
            category_seen["extraction_method"][extraction_method] += 1

            if ref_state == "null":
                null_seen += 1
            else:
                non_null_seen += 1

            if assertion_id in assertion_ids and increment_if_under(
                assertion_counter,
                assertion_id,
                MAX_ROWS_PER_ASSERTION_REGISTRATION,
            ):
                add_selection(selected, source_rowid, row, "assertion_registration_coverage")

            if increment_if_under(identity_kind_counter, identity_kind, MAX_ROWS_PER_IDENTITY_KIND):
                add_selection(selected, source_rowid, row, "identity_kind_coverage")

            if increment_if_under(namespace_counter, source_namespace, MAX_ROWS_PER_SOURCE_NAMESPACE):
                add_selection(selected, source_rowid, row, "source_namespace_coverage")

            if increment_if_under(participant_role_counter, participant_role, MAX_ROWS_PER_PARTICIPANT_ROLE):
                add_selection(selected, source_rowid, row, "participant_role_coverage")

            if increment_if_under(extraction_method_counter, extraction_method, MAX_ROWS_PER_EXTRACTION_METHOD):
                add_selection(selected, source_rowid, row, "extraction_method_coverage")

            if ref_state == "null" and null_selected < MAX_NULL_SOURCE_RECORD_REF_ROWS:
                null_selected += 1
                add_selection(selected, source_rowid, row, "null_source_record_ref_coverage")

            if ref_state != "null" and non_null_selected < MAX_NON_NULL_SOURCE_RECORD_REF_ROWS:
                non_null_selected += 1
                add_selection(selected, source_rowid, row, "non_null_source_record_ref_coverage")

            matched_terms = priority_terms_found(row)
            if matched_terms:
                for term in matched_terms:
                    priority_matches_by_term[term] += 1
                if priority_selected < MAX_PRIORITY_SEED_ROWS:
                    priority_selected += 1
                    add_selection(selected, source_rowid, row, "priority_seed_match")

            if fallback_selected < MAX_FALLBACK_ROWS:
                fallback_selected += 1
                add_selection(selected, source_rowid, row, "fallback_context")

    selected_rows = [entry.row for entry in sorted(selected.values(), key=lambda item: item.source_rowid)]
    lineage_rows: list[SelectedSourceIdentityLineage] = []
    source_size = source_path.stat().st_size

    for entry in sorted(selected.values(), key=lambda item: item.rank):
        row = entry.row
        primary_key = str(row.get("source_identity_id", entry.source_rowid))
        lineage_rows.append(
            SelectedSourceIdentityLineage(
                registration_unit_label=unit_label,
                source_database_path=str(source_path),
                source_database_size_bytes=source_size,
                source_table=COMPRESSED_TABLE,
                source_rowid=entry.source_rowid,
                source_primary_key=primary_key,
                output_database_relative_path=output_db_rel,
                output_table=COMPRESSED_TABLE,
                output_primary_key=primary_key,
                selection_reason=";".join(sorted(entry.reasons)),
                selection_rank=entry.rank,
                identity_kind=str(row.get("identity_kind", "")),
                source_namespace=str(row.get("source_namespace", "")),
                participant_role=str(row.get("participant_role", "")),
                extraction_method=str(row.get("extraction_method", "")),
                source_record_ref_state=source_record_ref_state(row.get("source_record_ref")),
            )
        )

    for term in PRIORITY_TERMS_UPPER:
        if priority_matches_by_term.get(term, 0) == 0:
            warnings.append(f"priority seed absent in {unit_label}: {term}")

    if null_seen == 0:
        warnings.append(f"no null source_record_ref rows observed in {unit_label}")
    if non_null_seen == 0:
        warnings.append(f"no non-null source_record_ref rows observed in {unit_label}")

    summary = {
        "rows_scanned": rows_scanned,
        "rows_selected": len(selected_rows),
        "identity_kind_count": len(category_seen["identity_kind"]),
        "source_namespace_count": len(category_seen["source_namespace"]),
        "participant_role_count": len(category_seen["participant_role"]),
        "extraction_method_count": len(category_seen["extraction_method"]),
        "null_source_record_ref_count": null_seen,
        "non_null_source_record_ref_count": non_null_seen,
        "priority_rows_selected": priority_selected,
        "priority_matches_by_term": dict(sorted(priority_matches_by_term.items())),
        "selected_null_source_record_ref_rows": sum(
            1 for item in selected.values() if source_record_ref_state(item.row.get("source_record_ref")) == "null"
        ),
        "selected_non_null_source_record_ref_rows": sum(
            1 for item in selected.values() if source_record_ref_state(item.row.get("source_record_ref")) != "null"
        ),
    }

    return selected_rows, lineage_rows, summary


def source_audit_base(
    unit_label: str,
    source_path: Path,
    before_state: FileState,
) -> SourceAudit:
    return SourceAudit(
        registration_unit_label=unit_label,
        source_database_path=str(source_path),
        source_database_exists=before_state.exists,
        source_database_size_bytes=before_state.size_bytes,
        source_database_mtime_ns_before=before_state.mtime_ns,
        source_database_mtime_ns_after=None,
        source_sha256_or_skip_reason="source_sha256_skipped_large_mark_database",
        open_status="not_attempted",
        query_only_status="not_attempted",
        table_count=None,
        required_table_status="not_attempted",
        schema_metadata_row_count=None,
        tep_packages_row_count=None,
        artifacts_row_count=None,
        assertion_registrations_row_count=None,
        source_identities_row_count=None,
        source_identity_identity_kind_count=None,
        source_identity_namespace_count=None,
        source_identity_participant_role_count=None,
        source_identity_extraction_method_count=None,
        null_source_record_ref_count=None,
        non_null_source_record_ref_count=None,
        post_extraction_state_status="not_attempted",
        audit_status="not_attempted",
        notes="",
    )


def audit_fixture_db(
    unit_label: str,
    output_path: Path,
    portable_root: Path,
) -> FixtureAudit:
    rel = repo_relative(output_path, portable_root)
    if not output_path.exists():
        return FixtureAudit(
            unit_label,
            rel,
            False,
            None,
            "missing",
            "not_attempted",
            None,
            None,
            None,
            None,
            None,
            "not_attempted",
            "not_attempted",
            "failed",
        )

    conn = sqlite3.connect(f"file:{output_path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        table_status = required_table_status(conn)
        counts = {
            table: count_rows(conn, table) if table_exists(conn, table) else None
            for table in REQUIRED_TABLES
        }
        integrity = str(conn.execute("PRAGMA integrity_check;").fetchone()[0])
        try:
            fk_rows = conn.execute("PRAGMA foreign_key_check;").fetchall()
            fk_status = "passed" if not fk_rows else f"failed:{len(fk_rows)}"
        except sqlite3.DatabaseError as exc:
            fk_status = f"not_applicable_or_failed:{exc}"

        audit_status = "passed" if table_status == "passed" and integrity == "ok" else "failed"
        return FixtureAudit(
            registration_unit_label=unit_label,
            output_database_relative_path=rel,
            output_database_exists=True,
            output_database_size_bytes=output_path.stat().st_size,
            open_status="passed",
            required_table_status=table_status,
            schema_metadata_row_count=counts["schema_metadata"],
            tep_packages_row_count=counts["tep_packages"],
            artifacts_row_count=counts["artifacts"],
            assertion_registrations_row_count=counts["assertion_registrations"],
            source_identities_row_count=counts["source_identities"],
            foreign_key_check_status_if_applicable=fk_status,
            integrity_check_status=integrity,
            audit_status=audit_status,
        )
    finally:
        conn.close()


def category_counts(db_path: Path, table: str, field_name: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        if field_name not in table_columns(conn, table):
            return []
        rows = conn.execute(
            f"""
            SELECT {quote_identifier(field_name)} AS field_value,
                   COUNT(*) AS row_count
            FROM {quote_identifier(table)}
            GROUP BY {quote_identifier(field_name)}
            ORDER BY field_value
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def build_expected_outputs(
    unit_results: list[UnitResult],
    fixture_audits: list[FixtureAudit],
    portable_root: Path,
    expected_dir: Path,
) -> None:
    inventory_rows = []
    table_count_rows = []
    category_rows = []

    audit_by_label = {audit.registration_unit_label: audit for audit in fixture_audits}

    for result in unit_results:
        audit = audit_by_label[result.registration_unit_label]
        inventory_rows.append(
            {
                "registration_unit_label": result.registration_unit_label,
                "registration_unit_path": str(Path(result.output_database_relative_path).parent),
                "sqlite_filename": OUTPUT_DB_SUFFIX,
                "schema_metadata_row_count": audit.schema_metadata_row_count,
                "tep_packages_row_count": audit.tep_packages_row_count,
                "artifacts_row_count": audit.artifacts_row_count,
                "assertion_registrations_row_count": audit.assertion_registrations_row_count,
                "source_identities_row_count": audit.source_identities_row_count,
                "fixture_database_size_bytes": audit.output_database_size_bytes,
                "fixture_audit_status": audit.audit_status,
            }
        )

        db_path = portable_root / result.output_database_relative_path
        for table in REQUIRED_TABLES:
            row_count = getattr(audit, f"{table}_row_count", None)
            table_count_rows.append(
                {
                    "registration_unit_label": result.registration_unit_label,
                    "table_name": table,
                    "row_count": row_count,
                    "expected_status": "expected",
                }
            )

        for table, fields in CATEGORY_SUMMARY_FIELDS.items():
            for field_name in fields:
                for category in category_counts(db_path, table, field_name):
                    category_rows.append(
                        {
                            "registration_unit_label": result.registration_unit_label,
                            "table_name": table,
                            "field_name": field_name,
                            "field_value": category["field_value"],
                            "row_count": category["row_count"],
                        }
                    )

    write_tsv(
        expected_dir / "registration_unit_fixture_inventory_expected.tsv",
        inventory_rows,
        [
            "registration_unit_label",
            "registration_unit_path",
            "sqlite_filename",
            "schema_metadata_row_count",
            "tep_packages_row_count",
            "artifacts_row_count",
            "assertion_registrations_row_count",
            "source_identities_row_count",
            "fixture_database_size_bytes",
            "fixture_audit_status",
        ],
    )
    write_tsv(
        expected_dir / "registration_unit_table_counts_expected.tsv",
        table_count_rows,
        [
            "registration_unit_label",
            "table_name",
            "row_count",
            "expected_status",
        ],
    )
    write_tsv(
        expected_dir / "registration_unit_category_summary_expected.tsv",
        category_rows,
        [
            "registration_unit_label",
            "table_name",
            "field_name",
            "field_value",
            "row_count",
        ],
    )


def process_unit(
    unit_label: str,
    source_path: Path,
    portable_root: Path,
    output_db_path: Path,
) -> tuple[
    UnitResult,
    SourceAudit,
    FixtureAudit,
    list[CopiedTableLineage],
    list[SelectedSourceIdentityLineage],
]:
    print(f"\n=== Processing {unit_label} ===")
    before_state = safe_stat(source_path)
    source_audit = source_audit_base(unit_label, source_path, before_state)
    warnings: list[str] = []
    copied_lineage: list[CopiedTableLineage] = []
    selected_lineage: list[SelectedSourceIdentityLineage] = []
    output_db_rel = repo_relative(output_db_path, portable_root)

    source_conn = open_source_connection(source_path)
    output_conn = open_output_connection(output_db_path)

    try:
        source_audit.open_status = "passed"
        source_audit.query_only_status = "passed"
        source_audit.table_count = len(table_names(source_conn))
        source_audit.required_table_status = required_table_status(source_conn)
        if source_audit.required_table_status != "passed":
            fail(f"{unit_label}: required table status failed: {source_audit.required_table_status}")

        create_required_tables_from_source(source_conn, output_conn)

        for table in FULL_COPY_TABLES:
            print(f"[{unit_label}] copying full table: {table}")
            lineage = copy_full_table(
                unit_label=unit_label,
                source_path=source_path,
                source_conn=source_conn,
                output_conn=output_conn,
                output_db_rel=output_db_rel,
                table=table,
            )
            copied_lineage.append(lineage)

        print(f"[{unit_label}] selecting compressed source_identities rows")
        selected_rows, selected_lineage, selection_summary = stream_select_source_identities(
            unit_label=unit_label,
            source_path=source_path,
            source_conn=source_conn,
            output_db_rel=output_db_rel,
            warnings=warnings,
        )

        source_identity_columns = table_columns(source_conn, COMPRESSED_TABLE)
        insert_rows(output_conn, COMPRESSED_TABLE, source_identity_columns, selected_rows)
        output_conn.commit()

        source_audit.schema_metadata_row_count = count_rows(source_conn, "schema_metadata")
        source_audit.tep_packages_row_count = count_rows(source_conn, "tep_packages")
        source_audit.artifacts_row_count = count_rows(source_conn, "artifacts")
        source_audit.assertion_registrations_row_count = count_rows(source_conn, "assertion_registrations")
        source_audit.source_identities_row_count = int(selection_summary["rows_scanned"])
        source_audit.source_identity_identity_kind_count = int(selection_summary["identity_kind_count"])
        source_audit.source_identity_namespace_count = int(selection_summary["source_namespace_count"])
        source_audit.source_identity_participant_role_count = int(selection_summary["participant_role_count"])
        source_audit.source_identity_extraction_method_count = int(selection_summary["extraction_method_count"])
        source_audit.null_source_record_ref_count = int(selection_summary["null_source_record_ref_count"])
        source_audit.non_null_source_record_ref_count = int(selection_summary["non_null_source_record_ref_count"])

    finally:
        output_conn.close()
        source_conn.close()

    after_state = safe_stat(source_path)
    source_audit.source_database_mtime_ns_after = after_state.mtime_ns
    if before_state.size_bytes == after_state.size_bytes and before_state.mtime_ns == after_state.mtime_ns:
        source_audit.post_extraction_state_status = "unchanged"
    else:
        source_audit.post_extraction_state_status = "changed_warning"
        warnings.append("source file stat changed during extraction")

    source_audit.audit_status = "passed" if source_audit.post_extraction_state_status == "unchanged" else "warning"
    source_audit.notes = "; ".join(warnings)

    fixture_audit = audit_fixture_db(unit_label, output_db_path, portable_root)
    selected_source_identity_count = fixture_audit.source_identities_row_count or 0

    result = UnitResult(
        registration_unit_label=unit_label,
        source_database_path=str(source_path),
        output_database_relative_path=output_db_rel,
        source_database_size_bytes=source_path.stat().st_size,
        output_database_size_bytes=output_db_path.stat().st_size,
        output_database_sha256=sha256_file(output_db_path),
        source_identity_rows_scanned=source_audit.source_identities_row_count or 0,
        source_identity_rows_selected=selected_source_identity_count,
        priority_seed_rows_selected=sum(
            1 for row in selected_lineage if "priority_seed_match" in row.selection_reason
        ),
        null_source_record_ref_selected=sum(
            1 for row in selected_lineage if row.source_record_ref_state == "null"
        ),
        non_null_source_record_ref_selected=sum(
            1 for row in selected_lineage if row.source_record_ref_state != "null"
        ),
        warnings=warnings,
    )

    print(
        f"[{unit_label}] selected {result.source_identity_rows_selected} "
        f"source_identities rows from {result.source_identity_rows_scanned:,} scanned rows"
    )

    return result, source_audit, fixture_audit, copied_lineage, selected_lineage


def render_report(
    created_at_utc: str,
    output_root: Path,
    archive_path: Path,
    unit_results: list[UnitResult],
    source_audits: list[SourceAudit],
) -> str:
    total_source_bytes = sum(result.source_database_size_bytes for result in unit_results)
    total_output_bytes = sum(result.output_database_size_bytes for result in unit_results)
    total_scanned = sum(result.source_identity_rows_scanned for result in unit_results)
    total_selected = sum(result.source_identity_rows_selected for result in unit_results)
    total_priority = sum(result.priority_seed_rows_selected for result in unit_results)
    total_warnings = sum(len(result.warnings) for result in unit_results)

    lines = [
        "# Phase 4 Registration Unit Golden Fixture Report",
        "",
        "## Purpose",
        "",
        "Create a lightweight, real-row-derived Phase 4 development fixture from the six certified Phase 3 VDB Registration Unit SQLite databases on MARK.",
        "",
        "## Created",
        "",
        f"`{created_at_utc}`",
        "",
        "## Source Corpus",
        "",
        f"`{SOURCE_CORPUS_ROOT}`",
        "",
        "## Output",
        "",
        f"Output directory: `{output_root}`",
        "",
        f"Archive: `{archive_path}`",
        "",
        "## Prime Directive",
        "",
        "The script reads MARK-resident source SQLite files and writes only to `/root/Desktop/`. It must not mutate source repositories or source SQLite files.",
        "",
        "## Extraction Policy",
        "",
        "The fixture copies `schema_metadata`, `tep_packages`, `artifacts`, and `assertion_registrations` completely. It compresses `source_identities` by deterministic real-row selection with lineage.",
        "",
        "## Authority Boundary",
        "",
        AUTHORITY_STATEMENT,
        "",
        "## Summary",
        "",
        f"- Registration Units: `{len(unit_results)}`",
        f"- Total source SQLite bytes: `{total_source_bytes}`",
        f"- Total output SQLite bytes: `{total_output_bytes}`",
        f"- Total source_identities rows scanned: `{total_scanned}`",
        f"- Total source_identities rows selected: `{total_selected}`",
        f"- Total selected priority-seed rows: `{total_priority}`",
        f"- Total warnings: `{total_warnings}`",
        "",
        "## Per-Unit Summary",
        "",
        "| Unit | Source identity rows scanned | Selected source identities | Priority selected | Null selected | Non-null selected | Output bytes | Warnings |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for result in unit_results:
        warning_text = "; ".join(result.warnings)
        lines.append(
            "| `{}` | {} | {} | {} | {} | {} | {} | {} |".format(
                result.registration_unit_label,
                result.source_identity_rows_scanned,
                result.source_identity_rows_selected,
                result.priority_seed_rows_selected,
                result.null_source_record_ref_selected,
                result.non_null_source_record_ref_selected,
                result.output_database_size_bytes,
                warning_text,
            )
        )

    lines.extend(
        [
            "",
            "## Source Non-Mutation Audit",
            "",
            "| Unit | Pre/post state | Audit status | Notes |",
            "|---|---|---|---|",
        ]
    )

    for audit in source_audits:
        lines.append(
            f"| `{audit.registration_unit_label}` | `{audit.post_extraction_state_status}` | `{audit.audit_status}` | {audit.notes} |"
        )

    lines.extend(
        [
            "",
            "## sys76 Placement Recommendation",
            "",
            "After manual retrieval, place the extracted fixture contents under:",
            "",
            "```text",
            "tests/fixtures/phase4/",
            "```",
            "",
            "The local fixture Registration Unit root should then be:",
            "",
            "```text",
            "tests/fixtures/phase4/registration_units/mark_phase3_canonical_6sqlite_lightweight/",
            "```",
            "",
            "## Known Limitations",
            "",
            "This fixture does not preserve all source rows or MARK-scale row volume. It is intended for rapid local Phase 4 development and must not replace MARK full-corpus smoketesting.",
            "",
        ]
    )

    return "\n".join(lines)


def build_manifest(
    created_at_utc: str,
    output_root: Path,
    archive_path: Path,
    unit_results: list[UnitResult],
) -> dict[str, Any]:
    return {
        "fixture_id": FIXTURE_ID,
        "fixture_version": FIXTURE_VERSION,
        "created_at_utc": created_at_utc,
        "script_path": SCRIPT_PATH,
        "script_version": SCRIPT_VERSION,
        "source_vdb_repo_root": str(SOURCE_VDB_REPO_ROOT),
        "source_corpus_root": str(SOURCE_CORPUS_ROOT),
        "output_root": str(output_root),
        "archive_path": str(archive_path),
        "prime_directive": (
            "Read MARK-resident VDB SQLite sources; write only to /root/Desktop; "
            "do not mutate MARK repositories or source SQLite files."
        ),
        "source_registration_units": list(REGISTRATION_UNITS.keys()),
        "source_database_paths": {label: str(path) for label, path in REGISTRATION_UNITS.items()},
        "source_database_sizes": {
            result.registration_unit_label: result.source_database_size_bytes
            for result in unit_results
        },
        "output_registration_units": [result.registration_unit_label for result in unit_results],
        "output_database_paths": {
            result.registration_unit_label: result.output_database_relative_path
            for result in unit_results
        },
        "output_database_sizes": {
            result.registration_unit_label: result.output_database_size_bytes
            for result in unit_results
        },
        "output_database_sha256": {
            result.registration_unit_label: result.output_database_sha256
            for result in unit_results
        },
        "full_copy_tables": FULL_COPY_TABLES,
        "compressed_tables": [COMPRESSED_TABLE],
        "source_identity_selection_policy": {
            "deterministic": True,
            "row_order": "ORDER BY rowid",
            "max_rows_per_assertion_registration": MAX_ROWS_PER_ASSERTION_REGISTRATION,
            "max_rows_per_identity_kind": MAX_ROWS_PER_IDENTITY_KIND,
            "max_rows_per_source_namespace": MAX_ROWS_PER_SOURCE_NAMESPACE,
            "max_rows_per_participant_role": MAX_ROWS_PER_PARTICIPANT_ROLE,
            "max_rows_per_extraction_method": MAX_ROWS_PER_EXTRACTION_METHOD,
            "max_null_source_record_ref_rows": MAX_NULL_SOURCE_RECORD_REF_ROWS,
            "max_non_null_source_record_ref_rows": MAX_NON_NULL_SOURCE_RECORD_REF_ROWS,
            "max_priority_seed_rows": MAX_PRIORITY_SEED_ROWS,
            "max_fallback_rows": MAX_FALLBACK_ROWS,
        },
        "priority_seed_policy": {
            "gene_symbols": PRIORITY_GENE_SYMBOLS,
            "ensembl_gene_ids": PRIORITY_ENSEMBL_IDS,
            "variant_fragments": PRIORITY_VARIANT_FRAGMENTS,
            "no_synthesis": True,
        },
        "lineage_artifact_paths": {
            "selected_source_identity_lineage": "lineage/selected_source_identity_lineage.tsv",
            "copied_table_lineage": "lineage/copied_table_lineage.tsv",
        },
        "authority_statement": AUTHORITY_STATEMENT,
    }


def create_archive(run_root: Path, archive_path: Path) -> None:
    ensure_under(run_root, OUTPUT_PARENT, "archive source directory")
    ensure_under(archive_path, OUTPUT_PARENT, "archive output")
    if archive_path.exists():
        archive_path.unlink()
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(run_root / PORTABLE_ROOT_NAME, arcname=PORTABLE_ROOT_NAME)


def main() -> int:
    validate_source_paths()

    created_at_utc = utc_now()
    stamp = timestamp_for_path()
    run_root = OUTPUT_PARENT / f"phase4_registration_unit_golden_fixture_{stamp}"
    archive_path = OUTPUT_PARENT / f"phase4_registration_unit_golden_fixture_{stamp}.tgz"
    portable_root = run_root / PORTABLE_ROOT_NAME

    registration_root = portable_root / "registration_units" / REGISTRATION_UNIT_FIXTURE_NAME
    manifests_dir = portable_root / "manifests"
    reports_dir = portable_root / "reports"
    lineage_dir = portable_root / "lineage"
    expected_dir = portable_root / "expected"

    reset_output_dir(run_root)
    for directory in [registration_root, manifests_dir, reports_dir, lineage_dir, expected_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    unit_results: list[UnitResult] = []
    source_audits: list[SourceAudit] = []
    fixture_audits: list[FixtureAudit] = []
    copied_table_lineage: list[CopiedTableLineage] = []
    selected_source_identity_lineage: list[SelectedSourceIdentityLineage] = []

    for unit_label, source_path in REGISTRATION_UNITS.items():
        output_db_path = registration_root / unit_label / OUTPUT_DB_SUFFIX
        (
            result,
            source_audit,
            fixture_audit,
            copied_lineage,
            selected_lineage,
        ) = process_unit(
            unit_label=unit_label,
            source_path=source_path,
            portable_root=portable_root,
            output_db_path=output_db_path,
        )
        unit_results.append(result)
        source_audits.append(source_audit)
        fixture_audits.append(fixture_audit)
        copied_table_lineage.extend(copied_lineage)
        selected_source_identity_lineage.extend(selected_lineage)

    write_tsv(
        lineage_dir / "copied_table_lineage.tsv",
        copied_table_lineage,
        [
            "registration_unit_label",
            "source_database_path",
            "source_table",
            "output_database_relative_path",
            "output_table",
            "source_row_count",
            "output_row_count",
            "copy_mode",
            "copy_status",
        ],
    )

    write_tsv(
        lineage_dir / "selected_source_identity_lineage.tsv",
        selected_source_identity_lineage,
        [
            "registration_unit_label",
            "source_database_path",
            "source_database_size_bytes",
            "source_table",
            "source_rowid",
            "source_primary_key",
            "output_database_relative_path",
            "output_table",
            "output_primary_key",
            "selection_reason",
            "selection_rank",
            "identity_kind",
            "source_namespace",
            "participant_role",
            "extraction_method",
            "source_record_ref_state",
        ],
    )

    write_tsv(
        reports_dir / "source_database_audit.tsv",
        source_audits,
        [
            "registration_unit_label",
            "source_database_path",
            "source_database_exists",
            "source_database_size_bytes",
            "source_database_mtime_ns_before",
            "source_database_mtime_ns_after",
            "source_sha256_or_skip_reason",
            "open_status",
            "query_only_status",
            "table_count",
            "required_table_status",
            "schema_metadata_row_count",
            "tep_packages_row_count",
            "artifacts_row_count",
            "assertion_registrations_row_count",
            "source_identities_row_count",
            "source_identity_identity_kind_count",
            "source_identity_namespace_count",
            "source_identity_participant_role_count",
            "source_identity_extraction_method_count",
            "null_source_record_ref_count",
            "non_null_source_record_ref_count",
            "post_extraction_state_status",
            "audit_status",
            "notes",
        ],
    )

    write_tsv(
        reports_dir / "fixture_database_audit.tsv",
        fixture_audits,
        [
            "registration_unit_label",
            "output_database_relative_path",
            "output_database_exists",
            "output_database_size_bytes",
            "open_status",
            "required_table_status",
            "schema_metadata_row_count",
            "tep_packages_row_count",
            "artifacts_row_count",
            "assertion_registrations_row_count",
            "source_identities_row_count",
            "foreign_key_check_status_if_applicable",
            "integrity_check_status",
            "audit_status",
        ],
    )

    checksum_rows = [
        {
            "registration_unit_label": result.registration_unit_label,
            "output_database_relative_path": result.output_database_relative_path,
            "output_database_size_bytes": result.output_database_size_bytes,
            "output_database_sha256": result.output_database_sha256,
        }
        for result in unit_results
    ]
    write_tsv(
        reports_dir / "fixture_checksums.tsv",
        checksum_rows,
        [
            "registration_unit_label",
            "output_database_relative_path",
            "output_database_size_bytes",
            "output_database_sha256",
        ],
    )

    build_expected_outputs(unit_results, fixture_audits, portable_root, expected_dir)

    manifest = build_manifest(created_at_utc, portable_root, archive_path, unit_results)
    write_json(manifests_dir / "phase4_registration_unit_golden_fixture_manifest.json", manifest)

    report = render_report(created_at_utc, portable_root, archive_path, unit_results, source_audits)
    write_text(reports_dir / "phase4_registration_unit_golden_fixture_report.md", report)

    create_archive(run_root, archive_path)
    archive_sha256 = sha256_file(archive_path)

    print("\nPhase 4 Registration Unit golden fixture complete")
    print(f"Output directory: {portable_root}")
    print(f"Archive: {archive_path}")
    print(f"Archive SHA256: {archive_sha256}")
    print("\nManual sys76 placement target after retrieval:")
    print("  tests/fixtures/phase4/")
    print("\nRegistration Unit fixture root after placement:")
    print(f"  tests/fixtures/phase4/registration_units/{REGISTRATION_UNIT_FIXTURE_NAME}/")

    total_warnings = sum(len(result.warnings) for result in unit_results)
    if total_warnings:
        print(f"\nCompleted with {total_warnings} warning(s). See report for details.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

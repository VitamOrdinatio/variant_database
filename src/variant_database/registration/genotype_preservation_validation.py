"""Read-only validation receipts for source genotype observation preservation."""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from variant_database.registration.genotype_preservation import (
    PRESERVATION_SCOPE_KIND_BOUNDED,
    PRESERVATION_STATUS_COMPLETE_PENDING_VALIDATION,
    ROW_SELECTION_POLICY_FIRST_N,
    raw_source_row_hash,
)

VALIDATOR_NAME = "variant_database.registration.genotype_preservation_validation"
VALIDATOR_VERSION = "0.1.0"
VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"
VALIDATED_MATURITY_STATE = "genotype_preservation_validated"

REPORT_JSON_FILENAME = "genotype_preservation_validation_report.json"
REPORT_TSV_FILENAME = "genotype_preservation_validation_report.tsv"
SUMMARY_JSON_FILENAME = "genotype_preservation_validation_summary.json"
SUMMARY_TSV_FILENAME = "genotype_preservation_validation_summary.tsv"
REPORT_SCHEMA_VERSION = "genotype_preservation_validation_report_v1"
SUMMARY_SCHEMA_VERSION = "genotype_preservation_validation_summary_v1"

REQUIRED_TABLES = {
    "source_genotype_artifact_index",
    "source_genotype_context_index",
    "source_genotype_observations",
    "source_genotype_package_classifications",
    "source_genotype_preservation_scopes",
    "tep_packages",
}


@dataclass(frozen=True)
class GenotypePreservationValidationCheck:
    check_id: str
    receipt_family: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class GenotypePreservationValidationResult:
    database_path: Path
    validation_output_dir: Path
    package_id: str
    preservation_scope_id: str
    scope_label: str
    validation_status: str
    validated_maturity_state: str
    report_json_path: Path
    report_tsv_path: Path
    summary_json_path: Path
    summary_tsv_path: Path
    checks: tuple[GenotypePreservationValidationCheck, ...]
    summary: dict[str, object]


@dataclass(frozen=True)
class SQLiteFingerprint:
    exists: bool
    size_bytes: int | None
    mtime_ns: int | None
    sidecars: tuple[str, ...]


def validate_genotype_preservation_database(
    database_path: str | Path,
    validation_output_dir: str | Path,
    *,
    validation_timestamp: str,
    expected_scope_label: str,
    expected_row_limit: int,
    expected_source_tep_id: str,
) -> GenotypePreservationValidationResult:
    """Validate one bounded first-N preservation scope without mutation."""
    if not validation_timestamp:
        raise ValueError("validation_timestamp is required")
    if not expected_scope_label:
        raise ValueError("expected_scope_label is required")
    if expected_row_limit < 1:
        raise ValueError("expected_row_limit must be positive")
    if not expected_source_tep_id:
        raise ValueError("expected_source_tep_id is required")

    db_path = Path(database_path)
    output_dir = Path(validation_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    checks: list[GenotypePreservationValidationCheck] = []

    def add_check(
        check_id: str,
        receipt_family: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
    ) -> None:
        checks.append(
            GenotypePreservationValidationCheck(
                check_id=check_id,
                receipt_family=receipt_family,
                status=(
                    VALIDATION_STATUS_PASSED
                    if passed
                    else VALIDATION_STATUS_FAILED
                ),
                message=message,
                expected=_stringify(expected),
                observed=_stringify(observed),
            )
        )

    before = _fingerprint(db_path)
    add_check(
        "database_exists",
        "source_genotype_observation_preservation_receipt",
        db_path.is_file(),
        "Genotype preservation SQLite database exists.",
        "file exists",
        db_path,
    )

    package_id = ""
    scope_id = ""
    scope_label = ""
    observed_row_count = 0
    unique_observation_count = 0
    source_column_count = 0
    malformed_raw_row_count = 0
    raw_hash_mismatch_count = 0
    typed_value_mismatch_count = 0
    producer_observation_split_count = 0
    inheritance_assertion_count = 0

    if db_path.is_file():
        connection = _connect_read_only(db_path)
        try:
            tables = _table_names(connection)
            for table in sorted(REQUIRED_TABLES):
                add_check(
                    f"required_table__{table}",
                    "source_genotype_observation_preservation_receipt",
                    table in tables,
                    f"Required genotype preservation table exists: {table}.",
                    "table exists",
                    table if table in tables else "missing",
                )

            if REQUIRED_TABLES <= tables:
                classifications = _query(
                    connection,
                    """
                    SELECT *
                    FROM source_genotype_package_classifications
                    ORDER BY package_id
                    """,
                )
                add_check(
                    "package_classification_cardinality",
                    "source_genotype_observation_preservation_receipt",
                    len(classifications) == 1,
                    "Preservation database contains exactly one package classification.",
                    1,
                    len(classifications),
                )
                if len(classifications) == 1:
                    classification = classifications[0]
                    package_id = str(classification["package_id"])
                    _validate_classification(classification, add_check)

                    scopes = _query(
                        connection,
                        """
                        SELECT *
                        FROM source_genotype_preservation_scopes
                        WHERE package_id = ?
                        ORDER BY scope_label
                        """,
                        (package_id,),
                    )
                    matching = [
                        row
                        for row in scopes
                        if str(row["scope_label"]) == expected_scope_label
                    ]
                    add_check(
                        "declared_scope_cardinality",
                        "source_genotype_observation_preservation_receipt",
                        len(matching) == 1,
                        "Exactly one declared preservation scope matches the expected label.",
                        1,
                        len(matching),
                    )
                    if len(matching) == 1:
                        scope = matching[0]
                        scope_id = str(scope["preservation_scope_id"])
                        scope_label = str(scope["scope_label"])
                        source_columns = _json_string_list(
                            scope["source_column_order_json"]
                        )
                        source_column_count = len(source_columns)
                        _validate_scope(
                            scope=scope,
                            expected_scope_label=expected_scope_label,
                            expected_row_limit=expected_row_limit,
                            expected_source_tep_id=expected_source_tep_id,
                            source_columns=source_columns,
                            add_check=add_check,
                        )
                        _validate_artifact_traceability(
                            connection=connection,
                            package_id=package_id,
                            scope=scope,
                            add_check=add_check,
                        )

                        observation_rows = _query(
                            connection,
                            """
                            SELECT *
                            FROM source_genotype_observations
                            WHERE preservation_scope_id = ?
                            ORDER BY source_row_number
                            """,
                            (scope_id,),
                        )
                        observed_row_count = len(observation_rows)
                        unique_observation_count = len(
                            {
                                str(row["genotype_observation_id"])
                                for row in observation_rows
                            }
                        )
                        producer_observation_split_count = (
                            observed_row_count - unique_observation_count
                        )

                        add_check(
                            "persisted_row_count",
                            "genotype_count_reconciliation_receipt",
                            observed_row_count == expected_row_limit,
                            "Persisted bounded genotype row count equals the requested 1K scope.",
                            expected_row_limit,
                            observed_row_count,
                        )
                        add_check(
                            "genotype_observation_id_uniqueness",
                            "genotype_identity_preservation_receipt",
                            unique_observation_count == observed_row_count,
                            "Producer genotype_observation_id remains unique within the scope.",
                            observed_row_count,
                            unique_observation_count,
                        )
                        row_numbers = [
                            int(row["source_row_number"])
                            for row in observation_rows
                        ]
                        add_check(
                            "source_row_number_sequence",
                            "source_genotype_observation_preservation_receipt",
                            row_numbers == list(range(1, expected_row_limit + 1)),
                            "Bounded preservation keeps deterministic first-N source row order.",
                            f"1..{expected_row_limit}",
                            _range_summary(row_numbers),
                        )

                        (
                            malformed_raw_row_count,
                            raw_hash_mismatch_count,
                            typed_value_mismatch_count,
                        ) = _validate_rows(
                            observation_rows=observation_rows,
                            source_columns=source_columns,
                        )
                        add_check(
                            "raw_source_rows_reconstructable",
                            "source_genotype_observation_preservation_receipt",
                            malformed_raw_row_count == 0,
                            (
                                "Every producer row has a reconstructable ordered "
                                "raw-value representation."
                            ),
                            0,
                            malformed_raw_row_count,
                        )
                        add_check(
                            "raw_source_row_hash_reconciliation",
                            "source_genotype_observation_preservation_receipt",
                            raw_hash_mismatch_count == 0,
                            "Every raw source-row hash reconciles to its preserved ordered values.",
                            0,
                            raw_hash_mismatch_count,
                        )
                        add_check(
                            "typed_fields_match_raw_source_values",
                            "genotype_identity_preservation_receipt",
                            typed_value_mismatch_count == 0,
                            "Typed/indexed identity fields equal their raw producer values.",
                            0,
                            typed_value_mismatch_count,
                        )
                        add_check(
                            "producer_observation_split_count",
                            "anti_collapse_validation_receipt",
                            producer_observation_split_count == 0,
                            "No producer genotype observation is split into multiple source rows.",
                            0,
                            producer_observation_split_count,
                        )

                        distinct_identity = _query_one(
                            connection,
                            """
                            SELECT
                                COUNT(DISTINCT sample_id) AS sample_count,
                                COUNT(DISTINCT run_id) AS run_count,
                                COUNT(DISTINCT reference_build) AS reference_count,
                                COUNT(DISTINCT source_vcf_sha256) AS vcf_sha_count,
                                COUNT(DISTINCT source_vcf_header_hash) AS header_hash_count
                            FROM source_genotype_observations
                            WHERE preservation_scope_id = ?
                            """,
                            (scope_id,),
                        )
                        for key, label in (
                            ("sample_count", "sample"),
                            ("run_count", "run"),
                            ("reference_count", "reference build"),
                            ("vcf_sha_count", "source VCF checksum"),
                            ("header_hash_count", "source VCF header hash"),
                        ):
                            value = int(distinct_identity[key])
                            add_check(
                                f"identity_coherence__{key}",
                                "genotype_identity_preservation_receipt",
                                value == 1,
                                f"The preserved 1K scope has one coherent {label} identity.",
                                1,
                                value,
                            )

                        inheritance_assertion_count = _inheritance_assertion_count(
                            connection,
                            tables,
                        )
                        add_check(
                            "inheritance_assertion_count",
                            "anti_overclaim_validation_receipt",
                            inheritance_assertion_count == 0,
                            "Source genotype preservation emits no inheritance assertions.",
                            0,
                            inheritance_assertion_count,
                        )
        finally:
            connection.close()

    after = _fingerprint(db_path)
    add_check(
        "database_fingerprint_unchanged",
        "source_genotype_observation_preservation_receipt",
        before.size_bytes == after.size_bytes and before.mtime_ns == after.mtime_ns,
        "Read-only preservation validation does not mutate the SQLite database.",
        before,
        after,
    )
    add_check(
        "database_sidecars_unchanged",
        "source_genotype_observation_preservation_receipt",
        before.sidecars == after.sidecars,
        "Read-only preservation validation does not create or remove SQLite sidecars.",
        before.sidecars,
        after.sidecars,
    )

    validation_status = (
        VALIDATION_STATUS_PASSED
        if checks and all(check.status == VALIDATION_STATUS_PASSED for check in checks)
        else VALIDATION_STATUS_FAILED
    )
    validated_maturity_state = (
        VALIDATED_MATURITY_STATE
        if validation_status == VALIDATION_STATUS_PASSED
        else "not_claimed"
    )
    receipt_statuses = _receipt_statuses(checks)
    status_counts = dict(sorted(Counter(check.status for check in checks).items()))

    report_json_path = output_dir / REPORT_JSON_FILENAME
    report_tsv_path = output_dir / REPORT_TSV_FILENAME
    summary_json_path = output_dir / SUMMARY_JSON_FILENAME
    summary_tsv_path = output_dir / SUMMARY_TSV_FILENAME

    summary: dict[str, object] = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "generated_utc": validation_timestamp,
        "database_path": str(db_path),
        "package_id": package_id,
        "preservation_scope_id": scope_id,
        "scope_label": scope_label,
        "validation_scope": "single_registration_database_bounded_first_n",
        "validation_status": validation_status,
        "validated_maturity_state": validated_maturity_state,
        "expected_row_limit": expected_row_limit,
        "observed_row_count": observed_row_count,
        "unique_genotype_observation_id_count": unique_observation_count,
        "source_column_count": source_column_count,
        "malformed_raw_row_count": malformed_raw_row_count,
        "raw_hash_mismatch_count": raw_hash_mismatch_count,
        "typed_value_mismatch_count": typed_value_mismatch_count,
        "producer_observation_split_count": producer_observation_split_count,
        "inheritance_assertion_count": inheritance_assertion_count,
        "receipt_statuses": receipt_statuses,
        "check_status_counts": status_counts,
        "check_count": len(checks),
        "failed_check_count": status_counts.get(VALIDATION_STATUS_FAILED, 0),
        "report_json_path": str(report_json_path),
        "report_tsv_path": str(report_tsv_path),
    }
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "validator": {"name": VALIDATOR_NAME, "version": VALIDATOR_VERSION},
        "generated_utc": validation_timestamp,
        "database_path": str(db_path),
        "validation_scope": "single_registration_database_bounded_first_n",
        "package_id": package_id,
        "preservation_scope_id": scope_id,
        "scope_label": scope_label,
        "validation_status": validation_status,
        "validated_maturity_state": validated_maturity_state,
        "receipt_statuses": receipt_statuses,
        "check_status_counts": status_counts,
        "checks": [asdict(check) for check in checks],
    }

    _write_json(report_json_path, report)
    _write_tsv(
        report_tsv_path,
        [asdict(check) for check in checks],
        ["check_id", "receipt_family", "status", "message", "expected", "observed"],
    )
    _write_json(summary_json_path, summary)
    _write_tsv(summary_tsv_path, [summary], list(summary))

    return GenotypePreservationValidationResult(
        database_path=db_path,
        validation_output_dir=output_dir,
        package_id=package_id,
        preservation_scope_id=scope_id,
        scope_label=scope_label,
        validation_status=validation_status,
        validated_maturity_state=validated_maturity_state,
        report_json_path=report_json_path,
        report_tsv_path=report_tsv_path,
        summary_json_path=summary_json_path,
        summary_tsv_path=summary_tsv_path,
        checks=tuple(checks),
        summary=summary,
    )


def _validate_classification(classification: dict[str, object], add_check: Any) -> None:
    expected = {
        "producer_family": "VAP",
        "producer_genotype_applicability_state": "genotype_applicable_to_producer_type",
        "genotype_capability_state": "genotype_capability_available",
        "genotype_maturity_state": "genotype_discovered",
        "classification_status": "classified",
        "trusted_modern_ingestion_ready": 1,
    }
    for field, expected_value in expected.items():
        observed = classification[field]
        add_check(
            f"classification__{field}",
            "source_genotype_observation_preservation_receipt",
            observed == expected_value,
            f"Preservation starts from the required discovery classification: {field}.",
            expected_value,
            observed,
        )


def _validate_scope(
    *,
    scope: dict[str, object],
    expected_scope_label: str,
    expected_row_limit: int,
    expected_source_tep_id: str,
    source_columns: list[str],
    add_check: Any,
) -> None:
    expected = {
        "scope_label": expected_scope_label,
        "source_tep_id": expected_source_tep_id,
        "preservation_scope_kind": PRESERVATION_SCOPE_KIND_BOUNDED,
        "row_selection_policy": ROW_SELECTION_POLICY_FIRST_N,
        "requested_row_limit": expected_row_limit,
        "selected_row_count": expected_row_limit,
        "first_selected_source_row": 1,
        "last_selected_source_row": expected_row_limit,
        "preservation_status": PRESERVATION_STATUS_COMPLETE_PENDING_VALIDATION,
    }
    for field, expected_value in expected.items():
        observed = scope[field]
        add_check(
            f"scope__{field}",
            "source_genotype_observation_preservation_receipt",
            observed == expected_value,
            f"The persisted preservation scope records the expected {field}.",
            expected_value,
            observed,
        )
    add_check(
        "scope_source_column_order",
        "source_genotype_observation_preservation_receipt",
        bool(source_columns) and len(source_columns) == len(set(source_columns)),
        "Preservation scope records one ordered, duplicate-free source header.",
        "nonempty unique ordered columns",
        len(source_columns),
    )
    source_declared_row_count = scope["source_declared_row_count"]
    add_check(
        "scope_source_declared_row_count_supports_selection",
        "genotype_count_reconciliation_receipt",
        source_declared_row_count is not None
        and int(source_declared_row_count) >= expected_row_limit,
        "Producer-declared genotype row count is sufficient for the bounded selection.",
        f">={expected_row_limit}",
        source_declared_row_count,
    )


def _validate_artifact_traceability(
    *,
    connection: sqlite3.Connection,
    package_id: str,
    scope: dict[str, object],
    add_check: Any,
) -> None:
    artifact = _query_one(
        connection,
        """
        SELECT artifact_id, artifact_path, artifact_sha256
        FROM source_genotype_artifact_index
        WHERE package_id = ? AND artifact_role = 'genotype_observations'
        """,
        (package_id,),
    )
    for field, scope_field in (
        ("artifact_id", "source_artifact_id"),
        ("artifact_path", "source_artifact_path"),
        ("artifact_sha256", "source_artifact_sha256"),
    ):
        add_check(
            f"scope_artifact_traceability__{field}",
            "genotype_identity_preservation_receipt",
            artifact[field] == scope[scope_field],
            f"Preservation scope {scope_field} reconciles to genotype artifact index.",
            artifact[field],
            scope[scope_field],
        )


def _validate_rows(
    *,
    observation_rows: list[dict[str, object]],
    source_columns: list[str],
) -> tuple[int, int, int]:
    malformed = 0
    hash_mismatches = 0
    typed_mismatches = 0
    typed_fields = (
        "genotype_observation_id",
        "schema_version",
        "sample_id",
        "run_id",
        "source_vcf_sha256",
        "source_vcf_header_hash",
        "source_record_hash",
        "reference_build",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_alleles_raw",
        "variant_relationship_status",
        "relationship_reason",
        "relationship_resolution_target",
        "variant_id",
        "variant_observation_id",
        "format_raw",
        "sample_format_raw",
        "gt_raw",
        "ad_raw",
        "dp_raw",
        "gq_raw",
        "pl_raw",
        "ft_raw",
    )
    for row in observation_rows:
        try:
            values = json.loads(str(row["raw_source_values_json"]))
            if not isinstance(values, list) or len(values) != len(source_columns):
                raise TypeError
            raw = {
                field: "" if value is None else str(value)
                for field, value in zip(source_columns, values, strict=True)
            }
        except (json.JSONDecodeError, TypeError, ValueError, IndexError):
            malformed += 1
            continue
        serialized = str(row["raw_source_values_json"])
        if raw_source_row_hash(serialized) != str(row["raw_source_row_hash"]):
            hash_mismatches += 1
        for field in typed_fields:
            if field not in raw:
                continue
            typed_value = "" if row[field] is None else str(row[field])
            if typed_value != raw[field]:
                typed_mismatches += 1
    return malformed, hash_mismatches, typed_mismatches


def _inheritance_assertion_count(
    connection: sqlite3.Connection,
    tables: set[str],
) -> int:
    candidate_tables = [name for name in tables if "inheritance" in name.lower()]
    total = 0
    for table in candidate_tables:
        if not table.replace("_", "").isalnum():
            continue
        total += int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
    return total


def _connect_read_only(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        str(row[0])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }


def _query(
    connection: sqlite3.Connection,
    sql: str,
    parameters: tuple[object, ...] = (),
) -> list[dict[str, object]]:
    return [dict(row) for row in connection.execute(sql, parameters).fetchall()]


def _query_one(
    connection: sqlite3.Connection,
    sql: str,
    parameters: tuple[object, ...] = (),
) -> dict[str, object]:
    row = connection.execute(sql, parameters).fetchone()
    if row is None:
        raise ValueError("Expected validation query to return one row")
    return dict(row)


def _json_string_list(value: object) -> list[str]:
    try:
        data = json.loads(str(value))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        return []
    return data


def _fingerprint(path: Path) -> SQLiteFingerprint:
    if not path.exists():
        return SQLiteFingerprint(False, None, None, ())
    stat = path.stat()
    sidecars = tuple(
        sorted(
            str(candidate)
            for suffix in ("-journal", "-shm", "-wal")
            if (candidate := Path(str(path) + suffix)).exists()
        )
    )
    return SQLiteFingerprint(True, stat.st_size, stat.st_mtime_ns, sidecars)


def _receipt_statuses(
    checks: list[GenotypePreservationValidationCheck],
) -> dict[str, str]:
    families: dict[str, list[str]] = {}
    for check in checks:
        families.setdefault(check.receipt_family, []).append(check.status)
    return {
        family: (
            VALIDATION_STATUS_PASSED
            if all(status == VALIDATION_STATUS_PASSED for status in statuses)
            else VALIDATION_STATUS_FAILED
        )
        for family, statuses in sorted(families.items())
    }


def _range_summary(values: list[int]) -> str:
    if not values:
        return "empty"
    return f"{values[0]}..{values[-1]} ({len(values)} rows)"


def _stringify(value: object) -> str:
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, sort_keys=True, default=str)
    return str(value)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_tsv(
    path: Path,
    rows: list[dict[str, object]],
    fieldnames: list[str],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _stringify(row.get(key, "")) for key in fieldnames})

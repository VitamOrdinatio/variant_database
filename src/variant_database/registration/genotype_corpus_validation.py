"""Corpus-level validation for producer-aware genotype package classifications.

This validator consumes declared package classifications from existing VDB
registration databases. It emits external JSON and TSV receipts and never
mutates registration persistence.

It does not:
- register or copy producer packages
- derive package classifications from producer artifacts
- persist genotype observations or relationships
- compare genotype-not-applicable states on the ordered maturity ladder
- perform assertion, topology, projection, or biological reasoning
"""

from __future__ import annotations

import csv
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


VALIDATOR_NAME = "variant_database.registration.genotype_corpus_validation"
VALIDATOR_VERSION = "0.2.0"

VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"

REPORT_JSON_FILENAME = "mixed_corpus_genotype_scope_validation_report.json"
REPORT_TSV_FILENAME = "mixed_corpus_genotype_scope_validation_report.tsv"
SUMMARY_JSON_FILENAME = "mixed_corpus_genotype_scope_validation_summary.json"
SUMMARY_TSV_FILENAME = "mixed_corpus_genotype_scope_validation_summary.tsv"
MATRIX_TSV_FILENAME = "mixed_corpus_package_classification_matrix.tsv"

REPORT_SCHEMA_VERSION = "mixed_corpus_genotype_scope_validation_report_v1"
SUMMARY_SCHEMA_VERSION = "mixed_corpus_genotype_scope_validation_summary_v1"
MATRIX_SCHEMA_VERSION = "mixed_corpus_package_classification_matrix_v1"

GENOTYPE_APPLICABLE = "genotype_applicable_to_producer_type"
GENOTYPE_NOT_APPLICABLE = "genotype_not_applicable_to_producer_type"
GENOTYPE_CAPABILITY_NOT_APPLICABLE = "genotype_capability_not_applicable"
GENOTYPE_CAPABILITY_UNAVAILABLE_LEGACY = (
    "genotype_capability_unavailable_legacy"
)
GENOTYPE_MATURITY_NOT_APPLICABLE = "genotype_maturity_not_applicable"

BLOCKED_CAPABILITY_STATES = {
    "genotype_capability_incomplete",
    "genotype_capability_invalid",
    "genotype_capability_unsupported_version",
}
INVALID_OR_INCOMPLETE_CAPABILITY_STATES = {
    "genotype_capability_incomplete",
    "genotype_capability_invalid",
}

GENOTYPE_APPLICABLE_MATURITY_ORDER = (
    "genotype_discovered",
    "genotype_preservation_validated",
    "genotype_direct_relationships_registered",
    "genotype_complex_relationships_preserved",
    "genotype_brokerage_evaluated",
    "genotype_assertion_ready",
    "genotype_topology_ready",
    "genotype_projection_ready",
)
MATURITY_RANK = {
    state: rank for rank, state in enumerate(GENOTYPE_APPLICABLE_MATURITY_ORDER)
}

CLASSIFICATION_COLUMNS = (
    "package_id",
    "producer_family",
    "producer_genotype_applicability_state",
    "genotype_capability_state",
    "genotype_maturity_state",
    "genotype_artifact_set_status",
    "execution_provenance_status",
    "trusted_modern_ingestion_ready",
    "classification_status",
    "classification_reason",
)

MATRIX_COLUMNS = (
    "schema_version",
    "label",
    "database_path",
    "package_path",
    "package_id",
    "tep_id",
    "producer_family",
    "producer_genotype_applicability_state",
    "genotype_capability_state",
    "genotype_maturity_state",
    "genotype_artifact_set_status",
    "execution_provenance_status",
    "classification_status",
    "classification_reason",
    "trusted_modern_ingestion_ready",
    "individual_validation_status",
    "individual_validated_maturity_state",
    "corpus_pairing_status",
    "database_read_status",
)

SUMMARY_COLUMNS = (
    "schema_version",
    "validator_name",
    "validator_version",
    "validation_timestamp",
    "validation_scope",
    "validation_status",
    "mixed_corpus_exercised",
    "package_count",
    "expected_package_count",
    "unique_package_id_count",
    "producer_family_count",
    "vap_package_count",
    "gsc_package_count",
    "genotype_applicable_count",
    "genotype_not_applicable_count",
    "legacy_genotype_unavailable_count",
    "invalid_or_incomplete_count",
    "unsupported_version_count",
    "blocked_capability_count",
    "classification_failure_count",
    "individual_validation_failure_count",
    "capability_applicability_pairing_failure_count",
    "maturity_applicability_pairing_failure_count",
    "expected_pairing_failure_count",
    "genotype_applicable_package_maturity_floor",
    "check_count",
    "failed_check_count",
)


@dataclass(frozen=True)
class MixedCorpusPackageInput:
    """One explicitly declared package participating in corpus validation."""

    label: str
    database_path: Path
    tep_id: str
    expected_producer_family: str
    expected_applicability_state: str
    expected_capability_state: str
    expected_maturity_state: str
    expected_artifact_set_status: str
    expected_execution_provenance_status: str
    expected_trusted_modern_ingestion_ready: int
    individual_validation_status: str
    individual_validated_maturity_state: str


@dataclass(frozen=True)
class MixedCorpusValidationCheck:
    """One corpus-level genotype scope validation check."""

    check_id: str
    receipt_family: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class MixedCorpusValidationResult:
    """Aggregate validation result and emitted receipt paths."""

    validation_status: str
    mixed_corpus_exercised: bool
    validation_output_dir: Path
    report_json_path: Path
    report_tsv_path: Path
    summary_json_path: Path
    summary_tsv_path: Path
    matrix_tsv_path: Path
    summary: dict[str, object]
    package_rows: tuple[dict[str, object], ...]
    checks: tuple[MixedCorpusValidationCheck, ...]


@dataclass(frozen=True)
class SQLiteFingerprint:
    """Filesystem state used to prove read-only aggregate validation."""

    exists: bool
    size_bytes: int | None
    mtime_ns: int | None
    sidecars: tuple[str, ...]


def validate_mixed_corpus_genotype_scope(
    package_inputs: Sequence[MixedCorpusPackageInput],
    validation_output_dir: str | Path,
    *,
    validation_timestamp: str,
    expected_package_count: int,
    expected_family_counts: Mapping[str, int],
    expected_genotype_applicable_count: int,
    expected_genotype_not_applicable_count: int,
    expected_maturity_floor: str,
) -> MixedCorpusValidationResult:
    """Validate one declared mixed-producer package set and emit receipts."""

    if not validation_timestamp:
        raise ValueError("validation_timestamp is required.")
    if expected_package_count < 1:
        raise ValueError("expected_package_count must be positive.")

    output_dir = Path(validation_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    checks: list[MixedCorpusValidationCheck] = []

    def add_check(
        check_id: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
        receipt_family: str = "mixed_corpus_genotype_scope_receipt",
    ) -> None:
        checks.append(
            MixedCorpusValidationCheck(
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

    labels = [item.label for item in package_inputs]
    database_paths = [str(Path(item.database_path)) for item in package_inputs]

    add_check(
        "declared_package_count",
        len(package_inputs) == expected_package_count,
        "The aggregate evaluation consumes exactly the declared package count.",
        expected_package_count,
        len(package_inputs),
    )
    add_check(
        "declared_labels_unique",
        len(set(labels)) == len(labels),
        "Declared package labels are unique.",
        len(labels),
        len(set(labels)),
    )
    add_check(
        "declared_database_paths_unique",
        len(set(database_paths)) == len(database_paths),
        "Declared registration database paths are unique.",
        len(database_paths),
        len(set(database_paths)),
    )

    package_rows: list[dict[str, object]] = []

    for item in package_inputs:
        row, read_checks = _read_declared_package(item)
        package_rows.append(row)
        checks.extend(read_checks)

        prefix = f"package__{_safe_id(item.label)}"
        add_check(
            f"{prefix}__individual_validation_passed",
            item.individual_validation_status == VALIDATION_STATUS_PASSED,
            "The package passed individual genotype discovery validation in this run.",
            VALIDATION_STATUS_PASSED,
            item.individual_validation_status,
        )
        add_check(
            f"{prefix}__individual_maturity_matches_database",
            (
                bool(row["genotype_maturity_state"])
                and item.individual_validated_maturity_state
                == row["genotype_maturity_state"]
            ),
            "Individual validated maturity matches the persisted package classification.",
            row["genotype_maturity_state"],
            item.individual_validated_maturity_state,
        )

        expected_pairs = (
            (
                "producer_family",
                item.expected_producer_family.strip().upper(),
                str(row["producer_family"]).strip().upper(),
            ),
            (
                "producer_genotype_applicability_state",
                item.expected_applicability_state,
                row["producer_genotype_applicability_state"],
            ),
            (
                "genotype_capability_state",
                item.expected_capability_state,
                row["genotype_capability_state"],
            ),
            (
                "genotype_maturity_state",
                item.expected_maturity_state,
                row["genotype_maturity_state"],
            ),
            (
                "genotype_artifact_set_status",
                item.expected_artifact_set_status,
                row["genotype_artifact_set_status"],
            ),
            (
                "execution_provenance_status",
                item.expected_execution_provenance_status,
                row["execution_provenance_status"],
            ),
            (
                "trusted_modern_ingestion_ready",
                item.expected_trusted_modern_ingestion_ready,
                _coerce_int(row["trusted_modern_ingestion_ready"]),
            ),
        )
        expected_pairing_passed = True
        for field_name, expected, observed in expected_pairs:
            passed = expected == observed
            expected_pairing_passed = expected_pairing_passed and passed
            add_check(
                f"{prefix}__expected__{field_name}",
                passed,
                f"Declared package expectation matches persisted {field_name}.",
                expected,
                observed,
            )

        classification_status_passed = row["classification_status"] == "classified"
        add_check(
            f"{prefix}__classification_status",
            classification_status_passed,
            "Package classification status records completed classification.",
            "classified",
            row["classification_status"],
        )

        capability_pairing_passed = _capability_applicability_pairing_passes(row)
        maturity_pairing_passed = _maturity_applicability_pairing_passes(row)
        producer_pairing_passed = _producer_pairing_passes(row)

        add_check(
            f"{prefix}__capability_applicability_pairing",
            capability_pairing_passed,
            "Capability and applicability form a governed pairing.",
            "pass",
            "pass" if capability_pairing_passed else "fail",
        )
        add_check(
            f"{prefix}__maturity_applicability_pairing",
            maturity_pairing_passed,
            "Maturity and applicability form a governed pairing.",
            "pass",
            "pass" if maturity_pairing_passed else "fail",
        )
        add_check(
            f"{prefix}__producer_family_pairing",
            producer_pairing_passed,
            "Producer family uses its governed genotype scope grammar.",
            "pass",
            "pass" if producer_pairing_passed else "fail",
        )

        row["corpus_pairing_status"] = (
            VALIDATION_STATUS_PASSED
            if (
                expected_pairing_passed
                and classification_status_passed
                and capability_pairing_passed
                and maturity_pairing_passed
                and producer_pairing_passed
            )
            else VALIDATION_STATUS_FAILED
        )

    package_ids = [str(row["package_id"]) for row in package_rows if row["package_id"]]
    producer_families = [
        str(row["producer_family"]).strip().upper()
        for row in package_rows
        if row["producer_family"]
    ]
    applicability_states = [
        str(row["producer_genotype_applicability_state"])
        for row in package_rows
    ]
    capability_states = [str(row["genotype_capability_state"]) for row in package_rows]

    family_counts = {
        family: producer_families.count(family)
        for family in sorted(set(producer_families) | {key.upper() for key in expected_family_counts})
    }
    package_count = len(package_rows)
    unique_package_id_count = len(set(package_ids))
    genotype_applicable_count = applicability_states.count(GENOTYPE_APPLICABLE)
    genotype_not_applicable_count = applicability_states.count(GENOTYPE_NOT_APPLICABLE)
    legacy_count = capability_states.count(GENOTYPE_CAPABILITY_UNAVAILABLE_LEGACY)
    invalid_or_incomplete_count = sum(
        state in INVALID_OR_INCOMPLETE_CAPABILITY_STATES for state in capability_states
    )
    unsupported_version_count = capability_states.count(
        "genotype_capability_unsupported_version"
    )
    blocked_capability_count = sum(
        state in BLOCKED_CAPABILITY_STATES for state in capability_states
    )
    classification_failure_count = sum(
        row["classification_status"] != "classified" for row in package_rows
    )
    individual_validation_failure_count = sum(
        row["individual_validation_status"] != VALIDATION_STATUS_PASSED
        for row in package_rows
    )
    capability_pairing_failure_count = sum(
        not _capability_applicability_pairing_passes(row) for row in package_rows
    )
    maturity_pairing_failure_count = sum(
        not _maturity_applicability_pairing_passes(row) for row in package_rows
    )
    expected_pairing_failure_count = sum(
        row["corpus_pairing_status"] != VALIDATION_STATUS_PASSED
        for row in package_rows
    )

    maturity_floor, maturity_floor_error = _applicable_maturity_floor(package_rows)

    add_check(
        "aggregate_package_count",
        package_count == expected_package_count,
        "The evaluated package matrix has the expected cardinality.",
        expected_package_count,
        package_count,
    )
    add_check(
        "aggregate_package_ids_complete_and_unique",
        (
            len(package_ids) == expected_package_count
            and unique_package_id_count == expected_package_count
        ),
        "Every package has one nonempty unique package_id.",
        expected_package_count,
        unique_package_id_count,
    )
    add_check(
        "aggregate_producer_family_diversity",
        len(set(producer_families)) >= 2,
        "The corpus exercises more than one producer family.",
        ">=2",
        len(set(producer_families)),
    )

    for expected_family, expected_count in sorted(expected_family_counts.items()):
        family = expected_family.upper()
        observed_count = family_counts.get(family, 0)
        add_check(
            f"aggregate_family_count__{_safe_id(family)}",
            observed_count == expected_count,
            f"The corpus contains the expected number of {family} packages.",
            expected_count,
            observed_count,
        )

    add_check(
        "aggregate_genotype_applicable_count",
        genotype_applicable_count == expected_genotype_applicable_count,
        "The corpus has the expected genotype-applicable package count.",
        expected_genotype_applicable_count,
        genotype_applicable_count,
    )
    add_check(
        "aggregate_genotype_not_applicable_count",
        genotype_not_applicable_count == expected_genotype_not_applicable_count,
        "The corpus has the expected genotype-not-applicable package count.",
        expected_genotype_not_applicable_count,
        genotype_not_applicable_count,
    )
    add_check(
        "aggregate_legacy_genotype_unavailable_count",
        legacy_count == 0,
        "The proof corpus contains no legacy genotype-unavailable package.",
        0,
        legacy_count,
    )
    add_check(
        "aggregate_invalid_or_incomplete_count",
        invalid_or_incomplete_count == 0,
        "The proof corpus contains no invalid or incomplete genotype-applicable package.",
        0,
        invalid_or_incomplete_count,
    )
    add_check(
        "aggregate_unsupported_version_count",
        unsupported_version_count == 0,
        "The proof corpus contains no unsupported-version genotype package.",
        0,
        unsupported_version_count,
    )
    add_check(
        "aggregate_classification_failure_count",
        classification_failure_count == 0,
        "All package classifications completed successfully.",
        0,
        classification_failure_count,
    )
    add_check(
        "aggregate_individual_validation_failure_count",
        individual_validation_failure_count == 0,
        "All packages passed individual validation in the same run.",
        0,
        individual_validation_failure_count,
    )
    add_check(
        "aggregate_capability_applicability_pairing_failure_count",
        capability_pairing_failure_count == 0,
        "All packages have valid capability/applicability pairings.",
        0,
        capability_pairing_failure_count,
    )
    add_check(
        "aggregate_maturity_applicability_pairing_failure_count",
        maturity_pairing_failure_count == 0,
        "All packages have valid maturity/applicability pairings.",
        0,
        maturity_pairing_failure_count,
    )
    add_check(
        "aggregate_expected_pairing_failure_count",
        expected_pairing_failure_count == 0,
        "All persisted classifications match the explicitly declared corpus expectations.",
        0,
        expected_pairing_failure_count,
    )
    add_check(
        "aggregate_applicable_maturity_values_orderable",
        not maturity_floor_error,
        "Only governed genotype-applicable maturity states enter the ordered comparison.",
        "all applicable maturity states governed",
        maturity_floor_error or "all governed",
    )
    add_check(
        "aggregate_genotype_applicable_maturity_floor",
        maturity_floor == expected_maturity_floor,
        "The ordered maturity floor is computed only across genotype-applicable packages.",
        expected_maturity_floor,
        maturity_floor,
    )
    add_check(
        "aggregate_not_applicable_maturity_excluded_from_ordering",
        all(
            row["genotype_maturity_state"] == GENOTYPE_MATURITY_NOT_APPLICABLE
            for row in package_rows
            if row["producer_genotype_applicability_state"]
            == GENOTYPE_NOT_APPLICABLE
        ),
        "Genotype-not-applicable packages retain the terminal state outside the ordered ladder.",
        GENOTYPE_MATURITY_NOT_APPLICABLE,
        sorted(
            {
                str(row["genotype_maturity_state"])
                for row in package_rows
                if row["producer_genotype_applicability_state"]
                == GENOTYPE_NOT_APPLICABLE
            }
        ),
    )

    prefinal_passed = all(check.status == VALIDATION_STATUS_PASSED for check in checks)
    mixed_corpus_exercised = prefinal_passed and package_count == expected_package_count
    add_check(
        "mixed_corpus_exercised",
        mixed_corpus_exercised,
        "One corpus-level evaluation consumed all declared package classifications together.",
        True,
        mixed_corpus_exercised,
    )

    validation_status = (
        VALIDATION_STATUS_PASSED
        if all(check.status == VALIDATION_STATUS_PASSED for check in checks)
        else VALIDATION_STATUS_FAILED
    )
    failed_check_count = sum(
        check.status == VALIDATION_STATUS_FAILED for check in checks
    )

    summary: dict[str, object] = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "validation_timestamp": validation_timestamp,
        "validation_scope": "declared_three_package_mixed_producer_corpus",
        "validation_status": validation_status,
        "mixed_corpus_exercised": mixed_corpus_exercised,
        "package_count": package_count,
        "expected_package_count": expected_package_count,
        "unique_package_id_count": unique_package_id_count,
        "producer_family_count": len(set(producer_families)),
        "vap_package_count": family_counts.get("VAP", 0),
        "gsc_package_count": family_counts.get("GSC", 0),
        "genotype_applicable_count": genotype_applicable_count,
        "genotype_not_applicable_count": genotype_not_applicable_count,
        "legacy_genotype_unavailable_count": legacy_count,
        "invalid_or_incomplete_count": invalid_or_incomplete_count,
        "unsupported_version_count": unsupported_version_count,
        "blocked_capability_count": blocked_capability_count,
        "classification_failure_count": classification_failure_count,
        "individual_validation_failure_count": individual_validation_failure_count,
        "capability_applicability_pairing_failure_count": capability_pairing_failure_count,
        "maturity_applicability_pairing_failure_count": maturity_pairing_failure_count,
        "expected_pairing_failure_count": expected_pairing_failure_count,
        "genotype_applicable_package_maturity_floor": maturity_floor,
        "check_count": len(checks),
        "failed_check_count": failed_check_count,
    }

    report_json_path = output_dir / REPORT_JSON_FILENAME
    report_tsv_path = output_dir / REPORT_TSV_FILENAME
    summary_json_path = output_dir / SUMMARY_JSON_FILENAME
    summary_tsv_path = output_dir / SUMMARY_TSV_FILENAME
    matrix_tsv_path = output_dir / MATRIX_TSV_FILENAME

    report_payload = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "validation_timestamp": validation_timestamp,
        "validation_scope": summary["validation_scope"],
        "validation_status": validation_status,
        "mixed_corpus_exercised": mixed_corpus_exercised,
        "summary": summary,
        "packages": package_rows,
        "checks": [asdict(check) for check in checks],
    }

    _write_json(report_json_path, report_payload)
    _write_check_tsv(report_tsv_path, checks)
    _write_json(summary_json_path, summary)
    _write_summary_tsv(summary_tsv_path, summary)
    _write_matrix_tsv(matrix_tsv_path, package_rows)

    return MixedCorpusValidationResult(
        validation_status=validation_status,
        mixed_corpus_exercised=mixed_corpus_exercised,
        validation_output_dir=output_dir,
        report_json_path=report_json_path,
        report_tsv_path=report_tsv_path,
        summary_json_path=summary_json_path,
        summary_tsv_path=summary_tsv_path,
        matrix_tsv_path=matrix_tsv_path,
        summary=summary,
        package_rows=tuple(package_rows),
        checks=tuple(checks),
    )


def _read_declared_package(
    item: MixedCorpusPackageInput,
) -> tuple[dict[str, object], list[MixedCorpusValidationCheck]]:
    """Read one persisted package classification without mutating SQLite."""

    checks: list[MixedCorpusValidationCheck] = []

    def add_check(
        check_id: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
    ) -> None:
        checks.append(
            MixedCorpusValidationCheck(
                check_id=check_id,
                receipt_family="mixed_corpus_genotype_scope_receipt",
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

    database_path = Path(item.database_path)
    prefix = f"package__{_safe_id(item.label)}"
    before = _fingerprint(database_path)

    row: dict[str, object] = {
        "schema_version": MATRIX_SCHEMA_VERSION,
        "label": item.label,
        "database_path": str(database_path),
        "package_path": "",
        "package_id": "",
        "tep_id": item.tep_id,
        "producer_family": "",
        "producer_genotype_applicability_state": "",
        "genotype_capability_state": "",
        "genotype_maturity_state": "",
        "genotype_artifact_set_status": "",
        "execution_provenance_status": "",
        "classification_status": "",
        "classification_reason": "",
        "trusted_modern_ingestion_ready": "",
        "individual_validation_status": item.individual_validation_status,
        "individual_validated_maturity_state": item.individual_validated_maturity_state,
        "corpus_pairing_status": VALIDATION_STATUS_FAILED,
        "database_read_status": VALIDATION_STATUS_FAILED,
    }

    add_check(
        f"{prefix}__database_exists",
        database_path.is_file(),
        "Declared registration SQLite database exists.",
        "file exists",
        database_path,
    )
    add_check(
        f"{prefix}__declared_tep_id_present",
        bool(item.tep_id.strip()),
        "The corpus declaration includes a transport package identity.",
        "nonempty tep_id",
        item.tep_id,
    )

    if database_path.is_file():
        try:
            connection = _connect_read_only(database_path)
            try:
                tables = _table_names(connection)
                classification_table_present = (
                    "source_genotype_package_classifications" in tables
                )
                package_table_present = "tep_packages" in tables
                add_check(
                    f"{prefix}__classification_table_present",
                    classification_table_present,
                    "Package classification table exists.",
                    "table exists",
                    (
                        "table exists"
                        if classification_table_present
                        else "missing"
                    ),
                )
                add_check(
                    f"{prefix}__package_table_present",
                    package_table_present,
                    "Package inventory table exists.",
                    "table exists",
                    "table exists" if package_table_present else "missing",
                )

                if classification_table_present:
                    classification_rows = _query(
                        connection,
                        f"""
                        SELECT {', '.join(CLASSIFICATION_COLUMNS)}
                        FROM source_genotype_package_classifications
                        ORDER BY package_id
                        """,
                    )
                    add_check(
                        f"{prefix}__classification_cardinality",
                        len(classification_rows) == 1,
                        "Each declared single-package database contributes exactly one classification.",
                        1,
                        len(classification_rows),
                    )
                    if len(classification_rows) == 1:
                        classification = classification_rows[0]
                        for column in CLASSIFICATION_COLUMNS:
                            row[column] = classification[column]

                        if package_table_present:
                            package_rows = _query(
                                connection,
                                """
                                SELECT package_path
                                FROM tep_packages
                                WHERE package_id = ?
                                """,
                                (classification["package_id"],),
                            )
                            add_check(
                                f"{prefix}__package_inventory_cardinality",
                                len(package_rows) == 1,
                                "The classification resolves to exactly one package inventory row.",
                                1,
                                len(package_rows),
                            )
                            if len(package_rows) == 1:
                                row["package_path"] = package_rows[0]["package_path"]

                        row["database_read_status"] = VALIDATION_STATUS_PASSED
            finally:
                connection.close()
        except (sqlite3.Error, OSError, ValueError) as exc:
            add_check(
                f"{prefix}__database_readable",
                False,
                "Declared database is readable in SQLite read-only mode.",
                "readable",
                f"{type(exc).__name__}: {exc}",
            )
        else:
            add_check(
                f"{prefix}__database_readable",
                row["database_read_status"] == VALIDATION_STATUS_PASSED,
                "Declared database is readable in SQLite read-only mode.",
                "readable",
                row["database_read_status"],
            )

    after = _fingerprint(database_path)
    add_check(
        f"{prefix}__database_non_mutation",
        before == after,
        "Aggregate validation does not mutate the registration database.",
        before,
        after,
    )
    add_check(
        f"{prefix}__database_sidecar_stability",
        before.sidecars == after.sidecars,
        "Aggregate validation does not create or remove SQLite sidecars.",
        before.sidecars,
        after.sidecars,
    )

    return row, checks


def _capability_applicability_pairing_passes(row: Mapping[str, object]) -> bool:
    applicability = str(row["producer_genotype_applicability_state"])
    capability = str(row["genotype_capability_state"])
    if applicability == GENOTYPE_APPLICABLE:
        return capability != GENOTYPE_CAPABILITY_NOT_APPLICABLE
    if applicability == GENOTYPE_NOT_APPLICABLE:
        return capability == GENOTYPE_CAPABILITY_NOT_APPLICABLE
    return False


def _maturity_applicability_pairing_passes(row: Mapping[str, object]) -> bool:
    applicability = str(row["producer_genotype_applicability_state"])
    maturity = str(row["genotype_maturity_state"])
    if applicability == GENOTYPE_APPLICABLE:
        return maturity in MATURITY_RANK
    if applicability == GENOTYPE_NOT_APPLICABLE:
        return maturity == GENOTYPE_MATURITY_NOT_APPLICABLE
    return False


def _producer_pairing_passes(row: Mapping[str, object]) -> bool:
    producer = str(row["producer_family"]).strip().upper()
    applicability = str(row["producer_genotype_applicability_state"])
    capability = str(row["genotype_capability_state"])
    maturity = str(row["genotype_maturity_state"])
    artifact_set = str(row["genotype_artifact_set_status"])
    provenance = str(row["execution_provenance_status"])
    trusted_ready = _coerce_int(row["trusted_modern_ingestion_ready"])

    if producer == "VAP":
        return (
            applicability == GENOTYPE_APPLICABLE
            and capability != GENOTYPE_CAPABILITY_NOT_APPLICABLE
            and maturity in MATURITY_RANK
        )
    if producer == "GSC":
        return (
            applicability == GENOTYPE_NOT_APPLICABLE
            and capability == GENOTYPE_CAPABILITY_NOT_APPLICABLE
            and maturity == GENOTYPE_MATURITY_NOT_APPLICABLE
            and artifact_set == "genotype_artifact_set_not_applicable"
            and provenance == "execution_provenance_not_applicable"
            and trusted_ready == 0
        )
    return False


def _applicable_maturity_floor(
    package_rows: Iterable[Mapping[str, object]],
) -> tuple[str, str]:
    maturity_states = [
        str(row["genotype_maturity_state"])
        for row in package_rows
        if row["producer_genotype_applicability_state"] == GENOTYPE_APPLICABLE
    ]
    if not maturity_states:
        return "", "no genotype-applicable package"

    unknown = sorted(state for state in maturity_states if state not in MATURITY_RANK)
    if unknown:
        return "", "unknown applicable maturity states: " + ",".join(unknown)

    return min(maturity_states, key=MATURITY_RANK.__getitem__), ""


def _connect_read_only(database_path: Path) -> sqlite3.Connection:
    uri = f"{database_path.resolve().as_uri()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    return {str(row[0]) for row in rows}


def _query(
    connection: sqlite3.Connection,
    sql: str,
    parameters: tuple[object, ...] = (),
) -> list[dict[str, object]]:
    return [dict(row) for row in connection.execute(sql, parameters).fetchall()]


def _fingerprint(database_path: Path) -> SQLiteFingerprint:
    if not database_path.exists():
        return SQLiteFingerprint(False, None, None, ())
    stat = database_path.stat()
    sidecars = tuple(
        sorted(
            str(path)
            for suffix in ("-journal", "-shm", "-wal")
            if (path := Path(f"{database_path}{suffix}")).exists()
        )
    )
    return SQLiteFingerprint(True, stat.st_size, stat.st_mtime_ns, sidecars)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=_json_default) + "\n",
        encoding="utf-8",
    )


def _write_check_tsv(
    path: Path,
    checks: Sequence[MixedCorpusValidationCheck],
) -> None:
    check_fields = tuple(MixedCorpusValidationCheck.__dataclass_fields__)
    fieldnames = ("schema_version", *check_fields)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for check in checks:
            writer.writerow(
                {
                    "schema_version": REPORT_SCHEMA_VERSION,
                    **asdict(check),
                }
            )


def _write_summary_tsv(path: Path, summary: Mapping[str, object]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerow({key: _stringify(summary.get(key, "")) for key in SUMMARY_COLUMNS})


def _write_matrix_tsv(
    path: Path,
    package_rows: Sequence[Mapping[str, object]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MATRIX_COLUMNS, delimiter="\t")
        writer.writeheader()
        for row in package_rows:
            writer.writerow({key: _stringify(row.get(key, "")) for key in MATRIX_COLUMNS})


def _stringify(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, sort_keys=True, default=_json_default)
    return str(value)


def _json_default(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)  # type: ignore[arg-type]
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _coerce_int(value: object) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _safe_id(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)

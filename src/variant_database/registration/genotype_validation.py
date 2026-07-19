"""Validation receipts for genotype-aware VDB package discovery.

This validator evaluates package-level genotype discovery and context indexing.
It reads an existing registration SQLite database in read-only mode and emits
external JSON and TSV validation receipts.

It does not:
- mutate registration persistence
- persist genotype observation rows
- register genotype-to-variant relationships
- perform genotype brokerage
- infer inheritance or biological interpretation
"""

from __future__ import annotations

import csv
import json
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


VALIDATOR_NAME = "variant_database.registration.genotype_validation"
VALIDATOR_VERSION = "0.1.0"

VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"

VALIDATED_MATURITY_STATE = "genotype_discovered"

REPORT_JSON_FILENAME = "genotype_discovery_validation_report.json"
REPORT_TSV_FILENAME = "genotype_discovery_validation_report.tsv"
SUMMARY_JSON_FILENAME = "genotype_discovery_validation_summary.json"
SUMMARY_TSV_FILENAME = "genotype_discovery_validation_summary.tsv"

REQUIRED_TABLES = {
    "artifacts",
    "source_genotype_package_classifications",
    "source_genotype_artifact_index",
    "source_genotype_context_index",
    "tep_packages",
}

CANONICAL_ARTIFACT_SCHEMA_VERSIONS = {
    "genotype_observations": "genotype_observation_v1",
    "genotype_projection_summary": "genotype_projection_summary_v1",
    "genotype_source_header_context": "genotype_source_header_context_v1",
}

CANONICAL_ARTIFACT_PARSE_STATUSES = {
    "genotype_observations": "header_parsed",
    "genotype_projection_summary": "parsed",
    "genotype_source_header_context": "parsed",
}

ALLOWED_CAPABILITY_STATES = {
    "genotype_capability_available",
    "genotype_capability_unavailable_legacy",
    "genotype_capability_not_applicable",
    "genotype_capability_incomplete",
    "genotype_capability_invalid",
    "genotype_capability_unsupported_version",
}


GENOTYPE_MATURITY_NOT_APPLICABLE = (
    "genotype_maturity_not_applicable"
)

ALLOWED_MATURITY_STATES = {
    VALIDATED_MATURITY_STATE,
    GENOTYPE_MATURITY_NOT_APPLICABLE,
}


@dataclass(frozen=True)
class GenotypeDiscoveryValidationCheck:
    """One genotype discovery validation check."""

    check_id: str
    receipt_family: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class GenotypeDiscoveryValidationResult:
    """Result and emitted artifact paths for one validation run."""

    database_path: Path
    validation_output_dir: Path
    package_id: str
    producer_family: str
    validation_status: str
    validated_maturity_state: str
    report_json_path: Path
    report_tsv_path: Path
    summary_json_path: Path
    summary_tsv_path: Path
    checks: tuple[GenotypeDiscoveryValidationCheck, ...]


@dataclass(frozen=True)
class SQLiteFingerprint:
    """Filesystem state used to prove read-only validation."""

    exists: bool
    size_bytes: int | None
    mtime_ns: int | None
    sidecars: tuple[str, ...]


def validate_genotype_discovery_database(
    database_path: str | Path,
    validation_output_dir: str | Path,
    *,
    validation_timestamp: str,
) -> GenotypeDiscoveryValidationResult:
    """Validate genotype discovery records and emit external receipts."""
    if not validation_timestamp:
        raise ValueError("validation_timestamp is required.")

    db_path = Path(database_path)
    output_dir = Path(validation_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    checks: list[GenotypeDiscoveryValidationCheck] = []

    def add_check(
        check_id: str,
        receipt_family: str,
        passed: bool,
        message: str,
        expected: object = "",
        observed: object = "",
    ) -> None:
        checks.append(
            GenotypeDiscoveryValidationCheck(
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
        "genotype_package_classification_receipt",
        db_path.is_file(),
        "Registration SQLite database exists.",
        "file exists",
        db_path,
    )

    package_id = ""
    producer_family = ""

    if db_path.is_file():
        connection = _connect_read_only(db_path)
        try:
            table_names = _table_names(connection)

            for table_name in sorted(REQUIRED_TABLES):
                add_check(
                    f"required_table__{table_name}",
                    "genotype_package_classification_receipt",
                    table_name in table_names,
                    f"Required genotype discovery table exists: {table_name}.",
                    "table exists",
                    table_name if table_name in table_names else "missing",
                )

            if REQUIRED_TABLES <= table_names:
                classification_rows = _query(
                    connection,
                    """
                    SELECT *
                    FROM source_genotype_package_classifications
                    ORDER BY package_id
                    """,
                )

                add_check(
                    "package_classification_cardinality",
                    "genotype_package_classification_receipt",
                    len(classification_rows) == 1,
                    "Single-package discovery database has exactly one genotype classification.",
                    1,
                    len(classification_rows),
                )

                if len(classification_rows) == 1:
                    classification = classification_rows[0]
                    package_id = str(classification["package_id"])
                    producer_family = str(classification["producer_family"])

                    _validate_classification(
                        classification=classification,
                        add_check=add_check,
                    )

                    artifact_rows = _query(
                        connection,
                        """
                        SELECT
                            genotype_index.*,
                            inventory.relative_path AS inventory_relative_path,
                            inventory.sha256 AS inventory_sha256,
                            inventory.size_bytes AS inventory_size_bytes
                        FROM source_genotype_artifact_index AS genotype_index
                        LEFT JOIN artifacts AS inventory
                          ON inventory.artifact_id = genotype_index.artifact_id
                        WHERE genotype_index.package_id = ?
                        ORDER BY genotype_index.artifact_role
                        """,
                        (package_id,),
                    )

                    context_rows = _query(
                        connection,
                        """
                        SELECT *
                        FROM source_genotype_context_index
                        WHERE package_id = ?
                        ORDER BY context_kind
                        """,
                        (package_id,),
                    )

                    _validate_artifacts(
                        classification=classification,
                        artifact_rows=artifact_rows,
                        add_check=add_check,
                    )
                    _validate_execution_provenance(
                        classification=classification,
                        context_rows=context_rows,
                        add_check=add_check,
                    )
                    _validate_summary_reconciliation(
                        classification=classification,
                        context_rows=context_rows,
                        add_check=add_check,
                    )
                    _validate_mixed_corpus_role(
                        classification=classification,
                        add_check=add_check,
                    )
        finally:
            connection.close()

    after = _fingerprint(db_path)

    add_check(
        "registration_database_non_mutation",
        "genotype_discovery_read_only_validation_receipt",
        before == after,
        "Read-only validation does not mutate the registration database.",
        before,
        after,
    )
    add_check(
        "registration_database_sidecar_stability",
        "genotype_discovery_read_only_validation_receipt",
        before.sidecars == after.sidecars,
        "Read-only validation does not create or remove SQLite sidecars.",
        before.sidecars,
        after.sidecars,
    )

    return _emit_validation_result(
        database_path=db_path,
        validation_output_dir=output_dir,
        validation_timestamp=validation_timestamp,
        package_id=package_id,
        producer_family=producer_family,
        checks=checks,
    )


def _validate_classification(
    *,
    classification: dict[str, object],
    add_check: Any,
) -> None:
    capability = str(
        classification["genotype_capability_state"]
    )
    maturity = str(
        classification["genotype_maturity_state"]
    )
    classification_status = str(
        classification["classification_status"]
    )
    applicability = str(
        classification["producer_genotype_applicability_state"]
    )
    producer = str(
        classification["producer_family"]
    ).upper()

    add_check(
        "capability_state_allowed",
        "genotype_package_classification_receipt",
        capability in ALLOWED_CAPABILITY_STATES,
        "Package capability state uses the governed vocabulary.",
        sorted(ALLOWED_CAPABILITY_STATES),
        capability,
    )
    add_check(
        "maturity_state_allowed",
        "genotype_package_classification_receipt",
        maturity in ALLOWED_MATURITY_STATES,
        "Package genotype maturity uses the governed vocabulary.",
        sorted(ALLOWED_MATURITY_STATES),
        maturity,
    )
    add_check(
        "classification_status_classified",
        "genotype_package_classification_receipt",
        classification_status == "classified",
        "Package genotype capability evaluation completed.",
        "classified",
        classification_status,
    )

    if producer == "VAP":
        expected_applicability = (
            "genotype_applicable_to_producer_type"
        )
        expected_maturity = VALIDATED_MATURITY_STATE
        valid_capabilities = {
            "genotype_capability_available",
            "genotype_capability_unavailable_legacy",
            "genotype_capability_incomplete",
            "genotype_capability_invalid",
            "genotype_capability_unsupported_version",
        }
        capability_pairing_valid = (
            applicability == expected_applicability
            and capability in valid_capabilities
        )
        expected_capability_pairing = (
            "genotype_applicable_to_producer_type + "
            "a TEP-VAP genotype capability state"
        )
    elif producer == "GSC":
        expected_applicability = (
            "genotype_not_applicable_to_producer_type"
        )
        expected_maturity = (
            GENOTYPE_MATURITY_NOT_APPLICABLE
        )
        capability_pairing_valid = (
            applicability == expected_applicability
            and capability
            == "genotype_capability_not_applicable"
        )
        expected_capability_pairing = (
            "genotype_not_applicable_to_producer_type + "
            "genotype_capability_not_applicable"
        )
    else:
        expected_applicability = (
            "recognized producer family: VAP or GSC"
        )
        expected_maturity = (
            "declared producer-specific maturity"
        )
        capability_pairing_valid = False
        expected_capability_pairing = (
            "declared producer-specific pairing"
        )

    add_check(
        "producer_genotype_applicability",
        "genotype_package_classification_receipt",
        (
            producer in {"VAP", "GSC"}
            and applicability == expected_applicability
        ),
        (
            "Producer family receives the correct genotype "
            "applicability state."
        ),
        expected_applicability,
        applicability,
    )
    add_check(
        "producer_capability_applicability_pairing",
        "genotype_package_classification_receipt",
        capability_pairing_valid,
        (
            "Producer genotype applicability and capability "
            "form a coherent pair."
        ),
        expected_capability_pairing,
        f"{applicability} + {capability}",
    )
    add_check(
        "producer_maturity_applicability_pairing",
        "genotype_package_classification_receipt",
        (
            producer in {"VAP", "GSC"}
            and maturity == expected_maturity
        ),
        (
            "Producer genotype applicability and maturity "
            "form a coherent pair."
        ),
        f"{expected_applicability} + {expected_maturity}",
        f"{applicability} + {maturity}",
    )

def _validate_artifacts(
    *,
    classification: dict[str, object],
    artifact_rows: list[dict[str, object]],
    add_check: Any,
) -> None:
    capability = str(classification["genotype_capability_state"])
    applicability = str(
        classification["producer_genotype_applicability_state"]
    )
    artifact_set_status = str(
        classification["genotype_artifact_set_status"]
    )

    rows_by_role = {
        str(row["artifact_role"]): row
        for row in artifact_rows
    }

    add_check(
        "canonical_artifact_index_cardinality",
        "genotype_artifact_set_validation_receipt",
        set(rows_by_role) == set(CANONICAL_ARTIFACT_SCHEMA_VERSIONS),
        "Artifact index represents each canonical genotype artifact role exactly once.",
        sorted(CANONICAL_ARTIFACT_SCHEMA_VERSIONS),
        sorted(rows_by_role),
    )

    trusted_available = capability == "genotype_capability_available"
    legacy = capability == "genotype_capability_unavailable_legacy"
    not_applicable = (
        applicability == "genotype_not_applicable_to_producer_type"
    )

    if trusted_available:
        add_check(
            "artifact_set_status_complete",
            "genotype_artifact_set_validation_receipt",
            artifact_set_status == "genotype_artifact_set_complete",
            "Trusted modern genotype package has a complete artifact set.",
            "genotype_artifact_set_complete",
            artifact_set_status,
        )

        for role, expected_version in (
            CANONICAL_ARTIFACT_SCHEMA_VERSIONS.items()
        ):
            row = rows_by_role.get(role)
            add_check(
                f"artifact_present__{role}",
                "genotype_artifact_set_validation_receipt",
                row is not None and _optional_int(row["artifact_present"]) == 1,
                f"Canonical genotype artifact is present: {role}.",
                1,
                row["artifact_present"] if row else "missing",
            )

            if row is None:
                continue

            add_check(
                f"artifact_schema_version__{role}",
                "genotype_artifact_set_validation_receipt",
                str(row["schema_version"]) == expected_version,
                f"Canonical genotype artifact uses the supported schema: {role}.",
                expected_version,
                row["schema_version"],
            )
            add_check(
                f"artifact_parse_status__{role}",
                "genotype_artifact_set_validation_receipt",
                str(row["parse_status"])
                == CANONICAL_ARTIFACT_PARSE_STATUSES[role],
                f"Canonical genotype artifact parsed successfully: {role}.",
                CANONICAL_ARTIFACT_PARSE_STATUSES[role],
                row["parse_status"],
            )
            add_check(
                f"artifact_inventory_path_match__{role}",
                "genotype_artifact_set_validation_receipt",
                str(row["artifact_path"])
                == str(row["inventory_relative_path"]),
                f"Genotype artifact index path matches package inventory: {role}.",
                row["artifact_path"],
                row["inventory_relative_path"],
            )
            add_check(
                f"artifact_inventory_sha_match__{role}",
                "genotype_artifact_set_validation_receipt",
                str(row["artifact_sha256"])
                == str(row["inventory_sha256"]),
                f"Genotype artifact index checksum matches package inventory: {role}.",
                row["artifact_sha256"],
                row["inventory_sha256"],
            )
            add_check(
                f"artifact_inventory_size_match__{role}",
                "genotype_artifact_set_validation_receipt",
                _optional_int(row["size_bytes"])
                == _optional_int(row["inventory_size_bytes"]),
                f"Genotype artifact index size matches package inventory: {role}.",
                row["size_bytes"],
                row["inventory_size_bytes"],
            )

    elif legacy or not_applicable:
        expected_status = (
            "genotype_artifact_set_not_applicable"
            if not_applicable
            else "genotype_artifact_set_absent"
        )
        add_check(
            "artifact_set_absence_classified",
            "genotype_artifact_set_validation_receipt",
            artifact_set_status == expected_status,
            "Non-modern or non-applicable genotype absence is explicit.",
            expected_status,
            artifact_set_status,
        )
        add_check(
            "artifact_rows_absent",
            "genotype_artifact_set_validation_receipt",
            all(
                _optional_int(row["artifact_present"]) == 0
                for row in artifact_rows
            ),
            "Legacy or non-applicable package does not claim genotype artifacts.",
            "all artifact_present = 0",
            [
                _optional_int(row["artifact_present"])
                for row in artifact_rows
            ],
        )

    else:
        add_check(
            "artifact_set_trusted_state",
            "genotype_artifact_set_validation_receipt",
            False,
            "Incomplete, invalid, or unsupported genotype artifact sets cannot pass trusted discovery validation.",
            (
                "genotype_capability_available, "
                "genotype_capability_unavailable_legacy, or "
                "genotype-not-applicable producer"
            ),
            capability,
        )


def _validate_execution_provenance(
    *,
    classification: dict[str, object],
    context_rows: list[dict[str, object]],
    add_check: Any,
) -> None:
    capability = str(classification["genotype_capability_state"])
    applicability = str(
        classification["producer_genotype_applicability_state"]
    )
    provenance_status = str(
        classification["execution_provenance_status"]
    )

    rows_by_kind = {
        str(row["context_kind"]): row
        for row in context_rows
    }
    provenance = rows_by_kind.get("execution_provenance")

    if capability == "genotype_capability_available":
        add_check(
            "execution_provenance_context_present",
            "execution_provenance_context_validation_receipt",
            provenance is not None,
            "Trusted modern genotype package has execution provenance context.",
            "context row exists",
            "present" if provenance else "missing",
        )

        if provenance is None:
            return

        add_check(
            "execution_provenance_status_registered",
            "execution_provenance_context_validation_receipt",
            provenance_status
            == "execution_provenance_registered_as_context",
            "Package classification records execution provenance as context.",
            "execution_provenance_registered_as_context",
            provenance_status,
        )
        add_check(
            "execution_provenance_parsed",
            "execution_provenance_context_validation_receipt",
            str(provenance["parse_status"]) == "parsed",
            "Execution provenance JSON parsed successfully.",
            "parsed",
            provenance["parse_status"],
        )
        add_check(
            "execution_provenance_registered_as_context",
            "execution_provenance_context_validation_receipt",
            _optional_int(provenance["registered_as_context"]) == 1,
            "Execution provenance is registered as context.",
            1,
            provenance["registered_as_context"],
        )
        add_check(
            "execution_provenance_not_biological_evidence",
            "execution_provenance_context_validation_receipt",
            _optional_int(
                provenance["registered_as_biological_evidence"]
            )
            == 0,
            "Execution provenance is not registered as biological evidence.",
            0,
            provenance["registered_as_biological_evidence"],
        )
        add_check(
            "execution_provenance_contract_status",
            "execution_provenance_context_validation_receipt",
            str(provenance["contract_status"]) == "pass",
            "Execution provenance producer contract passed.",
            "pass",
            provenance["contract_status"],
        )
        add_check(
            "execution_provenance_completeness",
            "execution_provenance_context_validation_receipt",
            str(provenance["provenance_completeness"]) == "complete",
            "Execution provenance is complete.",
            "complete",
            provenance["provenance_completeness"],
        )

    elif (
        capability == "genotype_capability_unavailable_legacy"
        or applicability == "genotype_not_applicable_to_producer_type"
    ):
        add_check(
            "execution_provenance_not_required",
            "execution_provenance_context_validation_receipt",
            provenance_status
            in {
                "execution_provenance_missing",
                "execution_provenance_not_applicable",
            },
            "Execution provenance is not falsely required for legacy or genotype-not-applicable discovery.",
            (
                "execution_provenance_missing or "
                "execution_provenance_not_applicable"
            ),
            provenance_status,
        )
    else:
        add_check(
            "execution_provenance_trusted_state",
            "execution_provenance_context_validation_receipt",
            False,
            "Invalid or incomplete modern execution provenance cannot pass trusted discovery validation.",
            "trusted modern provenance or explicit legacy/not-applicable state",
            provenance_status,
        )


def _validate_summary_reconciliation(
    *,
    classification: dict[str, object],
    context_rows: list[dict[str, object]],
    add_check: Any,
) -> None:
    capability = str(classification["genotype_capability_state"])
    applicability = str(
        classification["producer_genotype_applicability_state"]
    )

    rows_by_kind = {
        str(row["context_kind"]): row
        for row in context_rows
    }
    summary = rows_by_kind.get("genotype_projection_summary")

    if capability == "genotype_capability_available":
        add_check(
            "projection_summary_context_present",
            "genotype_count_reconciliation_receipt",
            summary is not None,
            "Trusted modern genotype package has an indexed projection summary.",
            "context row exists",
            "present" if summary else "missing",
        )

        if summary is None:
            return

        total = _optional_int(
            summary["genotype_observation_row_count"]
        )
        source_records = _optional_int(summary["source_record_count"])
        direct = _optional_int(summary["direct_relationship_count"])
        complex_count = _optional_int(
            summary["complex_relationship_count"]
        )
        unresolved = _optional_int(
            summary["unresolved_relationship_count"]
        )

        raw_payload = _json_object(summary["payload_json"])
        producer_payload = raw_payload.get("payload", {})
        counts = (
            producer_payload.get("counts", {})
            if isinstance(producer_payload, dict)
            else {}
        )
        not_applicable = _optional_int(
            counts.get("not_applicable_relationship_count")
            if isinstance(counts, dict)
            else None
        )
        if not_applicable is None:
            not_applicable = 0

        add_check(
            "producer_summary_source_record_reconciliation",
            "genotype_count_reconciliation_receipt",
            total is not None
            and source_records is not None
            and total == source_records,
            "Producer genotype observation count equals producer source-record count.",
            total,
            source_records,
        )

        partition_values = [
            direct,
            complex_count,
            unresolved,
            not_applicable,
        ]
        partition_total = (
            sum(value for value in partition_values if value is not None)
            if all(value is not None for value in partition_values)
            else None
        )

        add_check(
            "producer_summary_relationship_partition_reconciliation",
            "genotype_count_reconciliation_receipt",
            total is not None
            and partition_total is not None
            and total == partition_total,
            "Producer relationship partitions reconcile to genotype observation count.",
            total,
            partition_total,
        )
        add_check(
            "producer_summary_projection_status",
            "genotype_count_reconciliation_receipt",
            str(summary["projection_status"])
            in {"pass", "pass_with_advisory"},
            "Producer genotype projection completed without failure.",
            ["pass", "pass_with_advisory"],
            summary["projection_status"],
        )
        add_check(
            "producer_summary_projection_error_count",
            "genotype_count_reconciliation_receipt",
            _optional_int(summary["projection_error_count"]) == 0,
            "Producer genotype projection reports no errors.",
            0,
            summary["projection_error_count"],
        )

    elif (
        capability == "genotype_capability_unavailable_legacy"
        or applicability == "genotype_not_applicable_to_producer_type"
    ):
        add_check(
            "producer_summary_reconciliation_not_applicable",
            "genotype_count_reconciliation_receipt",
            True,
            "Producer summary reconciliation is explicitly not applicable.",
            "not applicable",
            "not applicable",
        )
    else:
        add_check(
            "producer_summary_trusted_state",
            "genotype_count_reconciliation_receipt",
            False,
            "Invalid, incomplete, or unsupported genotype summaries cannot pass reconciliation.",
            "trusted modern summary or explicit legacy/not-applicable state",
            capability,
        )


def _validate_mixed_corpus_role(
    *,
    classification: dict[str, object],
    add_check: Any,
) -> None:
    producer = str(classification["producer_family"]).upper()
    applicability = str(
        classification["producer_genotype_applicability_state"]
    )

    expected = {
        "VAP": "genotype_applicable_to_producer_type",
        "GSC": "genotype_not_applicable_to_producer_type",
    }.get(producer)

    add_check(
        "package_mixed_corpus_role",
        "genotype_package_classification_receipt",
        expected is not None and applicability == expected,
        "Package has an explicit producer-aware role for later mixed-corpus validation.",
        expected if expected is not None else "recognized producer family",
        applicability,
    )


def _emit_validation_result(
    *,
    database_path: Path,
    validation_output_dir: Path,
    validation_timestamp: str,
    package_id: str,
    producer_family: str,
    checks: list[GenotypeDiscoveryValidationCheck],
) -> GenotypeDiscoveryValidationResult:
    report_json_path = validation_output_dir / REPORT_JSON_FILENAME
    report_tsv_path = validation_output_dir / REPORT_TSV_FILENAME
    summary_json_path = validation_output_dir / SUMMARY_JSON_FILENAME
    summary_tsv_path = validation_output_dir / SUMMARY_TSV_FILENAME

    expected_validated_maturity_state = (
        GENOTYPE_MATURITY_NOT_APPLICABLE
        if producer_family.strip().upper() == "GSC"
        else VALIDATED_MATURITY_STATE
    )

    validation_status = (
        VALIDATION_STATUS_PASSED
        if all(check.status == VALIDATION_STATUS_PASSED for check in checks)
        else VALIDATION_STATUS_FAILED
    )
    validated_maturity_state = (
        expected_validated_maturity_state
        if validation_status == VALIDATION_STATUS_PASSED
        else "not_claimed"
    )

    receipt_statuses = _receipt_statuses(checks)
    status_counts = dict(
        sorted(Counter(check.status for check in checks).items())
    )

    report_payload = {
        "schema_version": "genotype_discovery_validation_report_v1",
        "validator": {
            "name": VALIDATOR_NAME,
            "version": VALIDATOR_VERSION,
        },
        "generated_utc": validation_timestamp,
        "database_path": str(database_path),
        "validation_scope": "single_registration_database",
        "mixed_corpus_exercised": False,
        "package_id": package_id,
        "producer_family": producer_family,
        "validation_status": validation_status,
        "validated_maturity_state": validated_maturity_state,
        "receipt_statuses": receipt_statuses,
        "check_status_counts": status_counts,
        "checks": [asdict(check) for check in checks],
    }

    summary_payload = {
        "schema_version": "genotype_discovery_validation_summary_v1",
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "generated_utc": validation_timestamp,
        "database_path": str(database_path),
        "package_id": package_id,
        "producer_family": producer_family,
        "validation_status": validation_status,
        "validated_maturity_state": validated_maturity_state,
        "validation_scope": "single_registration_database",
        "mixed_corpus_exercised": False,
        "receipt_statuses": receipt_statuses,
        "check_status_counts": status_counts,
        "report_json_path": str(report_json_path),
        "report_tsv_path": str(report_tsv_path),
    }

    _write_json(report_json_path, report_payload)
    _write_tsv(
        report_tsv_path,
        [asdict(check) for check in checks],
        [
            "check_id",
            "receipt_family",
            "status",
            "message",
            "expected",
            "observed",
        ],
    )
    _write_json(summary_json_path, summary_payload)
    _write_tsv(
        summary_tsv_path,
        [
            {
                "package_id": package_id,
                "producer_family": producer_family,
                "validation_status": validation_status,
                "validated_maturity_state": validated_maturity_state,
                "validation_scope": "single_registration_database",
                "mixed_corpus_exercised": "false",
                "passed_check_count": status_counts.get("passed", 0),
                "failed_check_count": status_counts.get("failed", 0),
            }
        ],
        [
            "package_id",
            "producer_family",
            "validation_status",
            "validated_maturity_state",
            "validation_scope",
            "mixed_corpus_exercised",
            "passed_check_count",
            "failed_check_count",
        ],
    )

    return GenotypeDiscoveryValidationResult(
        database_path=database_path,
        validation_output_dir=validation_output_dir,
        package_id=package_id,
        producer_family=producer_family,
        validation_status=validation_status,
        validated_maturity_state=validated_maturity_state,
        report_json_path=report_json_path,
        report_tsv_path=report_tsv_path,
        summary_json_path=summary_json_path,
        summary_tsv_path=summary_tsv_path,
        checks=tuple(checks),
    )


def _connect_read_only(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(
        f"file:{path.resolve()}?mode=ro",
        uri=True,
    )
    connection.row_factory = sqlite3.Row
    return connection


def _table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {str(row["name"]) for row in rows}


def _query(
    connection: sqlite3.Connection,
    sql: str,
    parameters: tuple[object, ...] = (),
) -> list[dict[str, object]]:
    rows = connection.execute(sql, parameters).fetchall()
    return [dict(row) for row in rows]


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise TypeError("Boolean values are not valid integer receipt values.")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f"Receipt value is not an integer string: {value!r}"
            ) from exc
    raise TypeError(
        "Receipt value must be an integer, integer string, or None; "
        f"received {type(value).__name__}"
    )


def _json_object(value: object) -> dict[str, Any]:
    if not isinstance(value, str):
        return {}
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _receipt_statuses(
    checks: list[GenotypeDiscoveryValidationCheck],
) -> dict[str, str]:
    families = sorted({check.receipt_family for check in checks})
    return {
        family: (
            VALIDATION_STATUS_PASSED
            if all(
                check.status == VALIDATION_STATUS_PASSED
                for check in checks
                if check.receipt_family == family
            )
            else VALIDATION_STATUS_FAILED
        )
        for family in families
    }


def _fingerprint(path: Path) -> SQLiteFingerprint:
    if not path.exists():
        return SQLiteFingerprint(
            exists=False,
            size_bytes=None,
            mtime_ns=None,
            sidecars=(),
        )

    stat = path.stat()
    return SQLiteFingerprint(
        exists=True,
        size_bytes=stat.st_size,
        mtime_ns=stat.st_mtime_ns,
        sidecars=_sqlite_sidecars(path),
    )


def _sqlite_sidecars(path: Path) -> tuple[str, ...]:
    candidates = (
        path.parent / f"{path.name}-wal",
        path.parent / f"{path.name}-shm",
        path.parent / f"{path.name}-journal",
    )
    return tuple(
        sorted(str(candidate) for candidate in candidates if candidate.exists())
    )


def _stringify(value: object) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
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
    columns: list[str],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=columns,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {column: _stringify(row.get(column)) for column in columns}
            )

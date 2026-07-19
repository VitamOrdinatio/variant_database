#!/usr/bin/env python3
"""Validate the sys76 three-TEP genotype discovery proof corpus.

One invocation performs two layers:
1. independent read-only validation of each declared registration database
2. one aggregate producer-aware corpus evaluation over all three classifications

The aggregate phase does not copy packages into a unified database and does not
advance any package beyond its persisted discovery maturity.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from variant_database.registration.genotype_corpus_validation import (
    VALIDATION_STATUS_PASSED as CORPUS_VALIDATION_PASSED,
    MixedCorpusPackageInput,
    MixedCorpusValidationResult,
    validate_mixed_corpus_genotype_scope,
)
from variant_database.registration.genotype_validation import (
    VALIDATION_STATUS_PASSED as INDIVIDUAL_VALIDATION_PASSED,
    GenotypeDiscoveryValidationResult,
    validate_genotype_discovery_database,
)


OUTPUT_ROOT = Path("results/validation/genotype_discovery_3tep")


@dataclass(frozen=True)
class ValidationTarget:
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


TARGETS = (
    ValidationTarget(
        label="vap_ERR10619300",
        database_path=Path(
            "results/registration/"
            "sys76_single_ERR10619300_genotype_discovery_1k/vdb.sqlite"
        ),
        tep_id="vap_tep_ERR10619300_run_2026_07_14_114546_v1",
        expected_producer_family="VAP",
        expected_applicability_state="genotype_applicable_to_producer_type",
        expected_capability_state="genotype_capability_available",
        expected_maturity_state="genotype_discovered",
        expected_artifact_set_status="genotype_artifact_set_complete",
        expected_execution_provenance_status=(
            "execution_provenance_registered_as_context"
        ),
        expected_trusted_modern_ingestion_ready=1,
    ),
    ValidationTarget(
        label="gsc_epilepsy",
        database_path=Path(
            "results/registration/genotype_discovery_3tep/"
            "gsc_epilepsy/vdb.sqlite"
        ),
        tep_id="gsc_tep_epilepsy_semantic_gtr_experimental_v0_1",
        expected_producer_family="GSC",
        expected_applicability_state=(
            "genotype_not_applicable_to_producer_type"
        ),
        expected_capability_state="genotype_capability_not_applicable",
        expected_maturity_state="genotype_maturity_not_applicable",
        expected_artifact_set_status="genotype_artifact_set_not_applicable",
        expected_execution_provenance_status=(
            "execution_provenance_not_applicable"
        ),
        expected_trusted_modern_ingestion_ready=0,
    ),
    ValidationTarget(
        label="gsc_mitochondrial_disease",
        database_path=Path(
            "results/registration/genotype_discovery_3tep/"
            "gsc_mitochondrial_disease/vdb.sqlite"
        ),
        tep_id="gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1",
        expected_producer_family="GSC",
        expected_applicability_state=(
            "genotype_not_applicable_to_producer_type"
        ),
        expected_capability_state="genotype_capability_not_applicable",
        expected_maturity_state="genotype_maturity_not_applicable",
        expected_artifact_set_status="genotype_artifact_set_not_applicable",
        expected_execution_provenance_status=(
            "execution_provenance_not_applicable"
        ),
        expected_trusted_modern_ingestion_ready=0,
    ),
)


@dataclass(frozen=True)
class IndividualOutcome:
    target: ValidationTarget
    validation_status: str
    validated_maturity_state: str
    result: GenotypeDiscoveryValidationResult | None
    error: str


def _utc_run_identity() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    validation_timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    run_name = now.strftime("run_%Y-%m-%dT%H_%M_%SZ")
    return validation_timestamp, run_name


def _failed_check_count(result: GenotypeDiscoveryValidationResult) -> int:
    return sum(check.status != INDIVIDUAL_VALIDATION_PASSED for check in result.checks)


def _print_individual_result(
    target: ValidationTarget,
    result: GenotypeDiscoveryValidationResult,
) -> None:
    print("=" * 80)
    print(f"Label: {target.label}")
    print(f"Database: {result.database_path}")
    print(f"Package ID: {result.package_id}")
    print(f"Producer family: {result.producer_family}")
    print(f"Validation status: {result.validation_status}")
    print(f"Validated maturity state: {result.validated_maturity_state}")
    print(f"Check count: {len(result.checks)}")
    print(f"Failed check count: {_failed_check_count(result)}")
    print(f"Report JSON: {result.report_json_path}")
    print(f"Report TSV: {result.report_tsv_path}")
    print(f"Summary JSON: {result.summary_json_path}")
    print(f"Summary TSV: {result.summary_tsv_path}")


def _print_table(rows: tuple[dict[str, object], ...]) -> None:
    columns = (
        ("label", "label"),
        ("producer_family", "producer"),
        ("producer_genotype_applicability_state", "applicability"),
        ("genotype_capability_state", "capability"),
        ("genotype_maturity_state", "maturity"),
        ("genotype_artifact_set_status", "artifact_set"),
        ("execution_provenance_status", "provenance"),
        ("trusted_modern_ingestion_ready", "trusted_ready"),
        ("corpus_pairing_status", "pairing"),
    )
    widths = {
        key: max(
            len(header),
            *(len(str(row.get(key, ""))) for row in rows),
        )
        for key, header in columns
    }
    header = "  ".join(
        label.ljust(widths[key]) for key, label in columns
    )
    separator = "  ".join("-" * widths[key] for key, _ in columns)
    print(header)
    print(separator)
    for row in rows:
        print(
            "  ".join(
                str(row.get(key, "")).ljust(widths[key])
                for key, _ in columns
            )
        )


def _print_corpus_result(result: MixedCorpusValidationResult) -> None:
    print("=" * 80)
    print("Three-package mixed-corpus genotype scope matrix")
    _print_table(result.package_rows)
    print("=" * 80)
    print(f"Corpus validation status: {result.validation_status}")
    print(f"Mixed corpus exercised: {result.mixed_corpus_exercised}")
    print(f"Package count: {result.summary['package_count']}")
    print(
        "Genotype-applicable count: "
        f"{result.summary['genotype_applicable_count']}"
    )
    print(
        "Genotype-not-applicable count: "
        f"{result.summary['genotype_not_applicable_count']}"
    )
    print(
        "Legacy genotype-unavailable count: "
        f"{result.summary['legacy_genotype_unavailable_count']}"
    )
    print(
        "Invalid or incomplete count: "
        f"{result.summary['invalid_or_incomplete_count']}"
    )
    print(
        "Genotype-applicable package maturity floor: "
        f"{result.summary['genotype_applicable_package_maturity_floor']}"
    )
    print(f"Check count: {result.summary['check_count']}")
    print(f"Failed check count: {result.summary['failed_check_count']}")
    print(f"Report JSON: {result.report_json_path}")
    print(f"Report TSV: {result.report_tsv_path}")
    print(f"Summary JSON: {result.summary_json_path}")
    print(f"Summary TSV: {result.summary_tsv_path}")
    print(f"Classification matrix: {result.matrix_tsv_path}")


def main() -> int:
    validation_timestamp, run_name = _utc_run_identity()
    run_root = OUTPUT_ROOT / run_name
    run_root.mkdir(parents=True, exist_ok=False)

    outcomes: list[IndividualOutcome] = []

    for target in TARGETS:
        try:
            result = validate_genotype_discovery_database(
                database_path=target.database_path,
                validation_output_dir=run_root / target.label,
                validation_timestamp=validation_timestamp,
            )
        except Exception as exc:  # noqa: BLE001 - operator runner must report all targets
            error = f"{type(exc).__name__}: {exc}"
            print("=" * 80)
            print(f"Label: {target.label}")
            print(f"Database: {target.database_path}")
            print("Validation status: error")
            print(f"Error: {error}")
            outcomes.append(
                IndividualOutcome(
                    target=target,
                    validation_status="error",
                    validated_maturity_state="",
                    result=None,
                    error=error,
                )
            )
            continue

        _print_individual_result(target, result)
        outcomes.append(
            IndividualOutcome(
                target=target,
                validation_status=result.validation_status,
                validated_maturity_state=result.validated_maturity_state,
                result=result,
                error="",
            )
        )

    corpus_inputs = [
        MixedCorpusPackageInput(
            label=outcome.target.label,
            database_path=outcome.target.database_path,
            tep_id=outcome.target.tep_id,
            expected_producer_family=outcome.target.expected_producer_family,
            expected_applicability_state=outcome.target.expected_applicability_state,
            expected_capability_state=outcome.target.expected_capability_state,
            expected_maturity_state=outcome.target.expected_maturity_state,
            expected_artifact_set_status=outcome.target.expected_artifact_set_status,
            expected_execution_provenance_status=(
                outcome.target.expected_execution_provenance_status
            ),
            expected_trusted_modern_ingestion_ready=(
                outcome.target.expected_trusted_modern_ingestion_ready
            ),
            individual_validation_status=outcome.validation_status,
            individual_validated_maturity_state=outcome.validated_maturity_state,
        )
        for outcome in outcomes
    ]

    corpus_result = validate_mixed_corpus_genotype_scope(
        corpus_inputs,
        run_root,
        validation_timestamp=validation_timestamp,
        expected_package_count=3,
        expected_family_counts={"VAP": 1, "GSC": 2},
        expected_genotype_applicable_count=1,
        expected_genotype_not_applicable_count=2,
        expected_maturity_floor="genotype_discovered",
    )
    _print_corpus_result(corpus_result)

    all_individual_passed = (
        len(outcomes) == len(TARGETS)
        and all(
            outcome.validation_status == INDIVIDUAL_VALIDATION_PASSED
            for outcome in outcomes
        )
    )
    aggregate_passed = (
        corpus_result.validation_status == CORPUS_VALIDATION_PASSED
        and corpus_result.mixed_corpus_exercised
    )

    print("=" * 80)
    print(f"Validation timestamp: {validation_timestamp}")
    print(f"Validation output root: {run_root}")
    print(
        "Three-package individual validation: "
        f"{'passed' if all_individual_passed else 'failed'}"
    )
    print("Validation scope: declared_three_package_mixed_producer_corpus")
    print(f"Mixed corpus exercised: {corpus_result.mixed_corpus_exercised}")
    print(
        "Mixed-corpus genotype scope validation: "
        f"{'passed' if aggregate_passed else 'failed'}"
    )

    return 0 if all_individual_passed and aggregate_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

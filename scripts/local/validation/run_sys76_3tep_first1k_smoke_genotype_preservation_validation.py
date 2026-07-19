#!/usr/bin/env python3
"""Validate the bounded ERR10619300 first-1K preservation smoke substrate.

This receipt proves source-order bounded preservation mechanics only. It is not
the representative 3TEP_1K golden-fixture candidate and does not exercise
mixed-corpus preservation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from variant_database.registration.genotype_preservation_validation import (
    VALIDATION_STATUS_PASSED,
    validate_genotype_preservation_database,
)

DATABASE = Path(
    "results/registration/genotype_preservation_3tep_first1k_smoke/"
    "vap_ERR10619300_first1k_smoke/vdb.sqlite"
)
OUTPUT_ROOT = Path(
    "results/validation/genotype_preservation_3tep_first1k_smoke"
)
SOURCE_TEP_ID = "vap_tep_ERR10619300_run_2026_07_14_114546_v1"
SCOPE_LABEL = "genotype_3tep_first1k_smoke_v1"
ROW_LIMIT = 1000


def main() -> int:
    now = datetime.now(timezone.utc)
    validation_timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    run_name = now.strftime("run_%Y-%m-%dT%H_%M_%SZ")
    run_root = OUTPUT_ROOT / run_name
    run_root.mkdir(parents=True, exist_ok=False)

    result = validate_genotype_preservation_database(
        DATABASE,
        run_root / "vap_ERR10619300_first1k_smoke",
        validation_timestamp=validation_timestamp,
        expected_scope_label=SCOPE_LABEL,
        expected_row_limit=ROW_LIMIT,
        expected_source_tep_id=SOURCE_TEP_ID,
    )
    failed_count = sum(
        check.status != VALIDATION_STATUS_PASSED for check in result.checks
    )

    print("=" * 80)
    print("3TEP first-1K smoke VAP genotype preservation validation")
    print(f"Database: {result.database_path}")
    print(f"Package ID: {result.package_id}")
    print(f"Preservation scope ID: {result.preservation_scope_id}")
    print(f"Scope label: {result.scope_label}")
    print(f"Validation status: {result.validation_status}")
    print(f"Validated maturity state: {result.validated_maturity_state}")
    print(f"Observed preserved rows: {result.summary['observed_row_count']}")
    print(
        "Unique genotype observation IDs: "
        f"{result.summary['unique_genotype_observation_id_count']}"
    )
    print(f"Source column count: {result.summary['source_column_count']}")
    print(f"Check count: {len(result.checks)}")
    print(f"Failed check count: {failed_count}")
    print(f"Report JSON: {result.report_json_path}")
    print(f"Report TSV: {result.report_tsv_path}")
    print(f"Summary JSON: {result.summary_json_path}")
    print(f"Summary TSV: {result.summary_tsv_path}")
    print("=" * 80)
    print(f"Validation timestamp: {validation_timestamp}")
    print(f"Validation output root: {run_root}")
    print("Validation scope: single_vap_first1k_source_order_smoke")
    print("Mixed corpus preservation exercised: False")
    print(
        "3TEP first-1K smoke VAP preservation validation: "
        f"{'passed' if result.validation_status == VALIDATION_STATUS_PASSED else 'failed'}"
    )

    return 0 if result.validation_status == VALIDATION_STATUS_PASSED else 1


if __name__ == "__main__":
    raise SystemExit(main())

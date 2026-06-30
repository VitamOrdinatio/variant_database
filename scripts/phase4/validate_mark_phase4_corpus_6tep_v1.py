#!/usr/bin/env python3
"""Validate the canonical MARK Phase 4.2 six-unit Corpus Generation artifacts.

This script emits Phase 4.2 validation receipts for the already-emitted MARK
six-unit Corpus Generation build artifact set.

It validates artifact-set coherence only.

It does not certify the Corpus Generation, open SQLite, mutate Registration
Units, create Assertion Records, derive topology, or interpret evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from variant_database.phase4.corpus_generation.validation import (
    validate_corpus_generation_artifact_set,
)


CORPUS_GENERATION_ID = "mark_phase4_corpus_6tep_v1"

DEFAULT_CORPUS_GENERATION_DIR = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1"
)

DEFAULT_SELECTION_MANIFEST = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_corpus_6tep_v1_selection_manifest.tsv"
)

DEFAULT_POLICY = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_6tep_certified_input_policy.json"
)

DEFAULT_VALIDATION_ROOT = Path("results/validation/phase4_corpus_generation")


def main() -> int:
    args = _parse_args()
    repo_root = args.repo_root.resolve()

    corpus_generation_dir = _resolve(repo_root, args.corpus_generation_dir)
    selection_manifest = _resolve(repo_root, args.selection_manifest)
    policy = _resolve(repo_root, args.policy)
    validation_root = _resolve(repo_root, args.validation_root)

    policy_payload = json.loads(policy.read_text(encoding="utf-8"))

    inventory = _resolve(
        repo_root,
        Path(args.registration_unit_inventory)
        if args.registration_unit_inventory
        else Path(policy_payload["registration_unit_inventory_reference"]),
    )
    readiness = _resolve(
        repo_root,
        Path(args.registration_unit_readiness)
        if args.registration_unit_readiness
        else Path(policy_payload["registration_unit_readiness_reference"]),
    )

    validation_timestamp = args.validation_timestamp or _utc_timestamp()
    receipt_suffix = _timestamp_suffix(validation_timestamp)
    receipt_dir = validation_root / f"{CORPUS_GENERATION_ID}_validation_{receipt_suffix}"

    result = validate_corpus_generation_artifact_set(
        corpus_generation_dir,
        selection_manifest,
        policy,
        inventory,
        readiness,
        receipt_dir,
        validation_timestamp=validation_timestamp,
    )

    _copy_latest_receipts(result.validation_output_dir, validation_root)
    archive_path = _archive_receipt(result.validation_output_dir, validation_root)

    _print_summary(
        result=result,
        validation_timestamp=validation_timestamp,
        archive_path=archive_path,
    )

    return 0 if result.validation_status == "passed" else 1


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the MARK Phase 4.2 six-unit Corpus Generation artifact set."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--corpus-generation-dir",
        type=Path,
        default=DEFAULT_CORPUS_GENERATION_DIR,
        help="Corpus Generation artifact directory to validate.",
    )
    parser.add_argument(
        "--selection-manifest",
        type=Path,
        default=DEFAULT_SELECTION_MANIFEST,
        help="Governed Corpus Generation selection manifest.",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY,
        help="Governed Corpus Generation selection policy JSON.",
    )
    parser.add_argument(
        "--registration-unit-inventory",
        type=Path,
        default=None,
        help=(
            "Optional Phase 4.1 Registration Unit inventory TSV override. "
            "Defaults to the path declared in the policy JSON."
        ),
    )
    parser.add_argument(
        "--registration-unit-readiness",
        type=Path,
        default=None,
        help=(
            "Optional Phase 4.1 Registration Unit readiness TSV override. "
            "Defaults to the path declared in the policy JSON."
        ),
    )
    parser.add_argument(
        "--validation-root",
        type=Path,
        default=DEFAULT_VALIDATION_ROOT,
        help="Validation receipt root directory.",
    )
    parser.add_argument(
        "--validation-timestamp",
        default=None,
        help=(
            "Validation timestamp to preserve in receipts. "
            "If omitted, the current UTC timestamp is used."
        ),
    )
    return parser.parse_args()


def _resolve(repo_root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root / path


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _timestamp_suffix(timestamp: str) -> str:
    return (
        timestamp.replace("-", "_")
        .replace(":", "")
        .replace("T", "_")
        .replace("Z", "")
    )


def _copy_latest_receipts(receipt_dir: Path, validation_root: Path) -> None:
    validation_root.mkdir(parents=True, exist_ok=True)
    for filename in (
        "corpus_generation_validation_report.json",
        "corpus_generation_validation_report.tsv",
        "corpus_generation_validation_summary.json",
        "corpus_generation_validation_summary.tsv",
    ):
        shutil.copyfile(receipt_dir / filename, validation_root / filename)


def _archive_receipt(receipt_dir: Path, validation_root: Path) -> Path:
    archive_root = validation_root / "receipt_archives"
    archive_root.mkdir(parents=True, exist_ok=True)

    archive_path = archive_root / f"{receipt_dir.name}.tgz"
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(receipt_dir, arcname=receipt_dir.name)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(
        f"{digest}  {archive_path.name}\n",
        encoding="utf-8",
    )

    return archive_path


def _print_summary(*, result, validation_timestamp: str, archive_path: Path) -> None:
    summary = json.loads(
        result.validation_summary_json_path.read_text(encoding="utf-8")
    )

    print("Corpus Generation validation receipts emitted.")
    print()
    print(f"corpus_generation_id: {result.corpus_generation_id}")
    print(f"validation_status: {result.validation_status}")
    print(f"validation_timestamp: {validation_timestamp}")
    print()
    print(f"validation_output_dir: {result.validation_output_dir}")
    print(f"validation_report_json: {result.validation_report_json_path}")
    print(f"validation_report_tsv: {result.validation_report_tsv_path}")
    print(f"validation_summary_json: {result.validation_summary_json_path}")
    print(f"validation_summary_tsv: {result.validation_summary_tsv_path}")
    print(f"receipt_archive: {archive_path}")
    print()
    print("summary:")
    print(f"  total_check_count: {summary['total_check_count']}")
    print(f"  passed_check_count: {summary['passed_check_count']}")
    print(f"  failed_check_count: {summary['failed_check_count']}")


if __name__ == "__main__":
    raise SystemExit(main())

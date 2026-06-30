#!/usr/bin/env python3
"""Build the canonical MARK Phase 4.2 six-unit Corpus Generation artifact set.

This script emits Corpus Generation build artifacts from the governed MARK
six-unit selection manifest and machine-readable selection policy fixture.

It does not validate or certify the Corpus Generation.

It does not open SQLite, mutate Registration Units, create Assertion Records,
derive topology, derive geometry, construct surfaces, emit projections, or
interpret evidence.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from variant_database.phase4.corpus_generation.artifacts import (
    emit_corpus_generation_artifacts,
)


DEFAULT_SELECTION_MANIFEST = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_corpus_6tep_v1_selection_manifest.tsv"
)

DEFAULT_POLICY = Path(
    "docs/manifests/corpus_generation/"
    "mark_phase4_6tep_certified_input_policy.json"
)

DEFAULT_OUTPUT_DIR = Path(
    "results/phase4/corpus_generations/mark_phase4_corpus_6tep_v1"
)


def main() -> int:
    args = _parse_args()
    repo_root = args.repo_root.resolve()

    policy_path = _resolve(repo_root, args.policy)
    selection_manifest_path = _resolve(repo_root, args.selection_manifest)
    output_dir = _resolve(repo_root, args.output_dir)

    policy = _load_policy(policy_path)

    inventory_path = _resolve(
        repo_root,
        Path(args.registration_unit_inventory)
        if args.registration_unit_inventory
        else Path(policy["registration_unit_inventory_reference"]),
    )
    readiness_path = _resolve(
        repo_root,
        Path(args.registration_unit_readiness)
        if args.registration_unit_readiness
        else Path(policy["registration_unit_readiness_reference"]),
    )

    build_timestamp = args.build_timestamp or _utc_timestamp()

    artifacts = emit_corpus_generation_artifacts(
        selection_manifest_path,
        output_dir,
        corpus_generation_label=policy["corpus_generation_label"],
        corpus_generation_purpose=policy["corpus_generation_purpose"],
        corpus_generation_version=policy["corpus_generation_version"],
        selection_policy_id=policy["selection_policy_id"],
        selection_policy_version=policy["selection_policy_version"],
        selection_policy_description=policy["selection_policy_description"],
        registration_unit_inventory_path=inventory_path,
        registration_unit_readiness_path=readiness_path,
        repo_root=repo_root,
        build_timestamp=build_timestamp,
        validate_selection_manifest_filesystem=args.validate_selection_manifest_filesystem,
    )

    _print_summary(
        artifacts=artifacts,
        policy=policy,
        build_timestamp=build_timestamp,
    )

    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Emit the MARK Phase 4.2 six-unit Corpus Generation build artifact set."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--selection-manifest",
        type=Path,
        default=DEFAULT_SELECTION_MANIFEST,
        help=(
            "Corpus Generation selection manifest. Defaults to the canonical "
            "MARK six-unit fixture."
        ),
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY,
        help="Corpus Generation selection policy JSON.",
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
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for Corpus Generation build artifacts.",
    )
    parser.add_argument(
        "--build-timestamp",
        default=None,
        help=(
            "Build timestamp to preserve in emitted artifacts. "
            "If omitted, the current UTC timestamp is used."
        ),
    )
    parser.add_argument(
        "--validate-selection-manifest-filesystem",
        action="store_true",
        help=(
            "Require included Registration Unit directories and SQLite files "
            "declared in the selection manifest to exist. This does not open SQLite."
        ),
    )
    return parser.parse_args()


def _resolve(repo_root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root / path


def _load_policy(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Policy fixture does not exist: {path}")

    policy = json.loads(path.read_text(encoding="utf-8"))

    required = {
        "selection_policy_id",
        "selection_policy_version",
        "selection_policy_description",
        "corpus_generation_id",
        "corpus_generation_label",
        "corpus_generation_purpose",
        "corpus_generation_version",
        "registration_unit_inventory_reference",
        "registration_unit_readiness_reference",
    }

    missing = sorted(required - set(policy))
    if missing:
        raise ValueError(
            "Policy fixture is missing required keys: " + ", ".join(missing)
        )

    return policy


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _print_summary(
    *,
    artifacts,
    policy: dict[str, Any],
    build_timestamp: str,
) -> None:
    payload = json.loads(
        artifacts.corpus_generation_manifest_json_path.read_text(encoding="utf-8")
    )
    summaries = payload["summaries"]

    print("Corpus Generation build artifacts emitted.")
    print()
    print(f"corpus_generation_id: {policy['corpus_generation_id']}")
    print(f"selection_policy_id: {policy['selection_policy_id']}")
    print(f"build_timestamp: {build_timestamp}")
    print()
    print(f"output_dir: {artifacts.output_dir}")
    print(f"copied_selection_manifest: {artifacts.copied_selection_manifest_path}")
    print(f"corpus_generation_manifest_tsv: {artifacts.corpus_generation_manifest_tsv_path}")
    print(f"corpus_generation_manifest_json: {artifacts.corpus_generation_manifest_json_path}")
    print(f"corpus_generation_report: {artifacts.corpus_generation_report_path}")
    print(
        "downstream_assertion_record_input_manifest: "
        f"{artifacts.downstream_assertion_record_input_manifest_path}"
    )
    print()
    print("summary:")
    print(
        "  included_registration_unit_count: "
        f"{summaries['included_registration_unit_count']}"
    )
    print(
        "  excluded_registration_unit_count: "
        f"{summaries['excluded_registration_unit_count']}"
    )
    print(
        "  downstream_assertion_record_input_count: "
        f"{summaries['downstream_assertion_record_input_count']}"
    )
    print(f"  artifact_count_total: {summaries['artifact_count_total']}")
    print(
        "  assertion_registration_count_total: "
        f"{summaries['assertion_registration_count_total']}"
    )
    print(f"  source_identity_count_total: {summaries['source_identity_count_total']}")
    print()
    print("boundary:")
    print("  corpus_generation_validation_status: not_evaluated")
    print("  corpus_generation_certification_status: not_available")
    print("  creates_assertion_records: false")
    print("  derives_topology: false")
    print("  interprets_evidence: false")


if __name__ == "__main__":
    raise SystemExit(main())

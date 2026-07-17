#!/usr/bin/env python3
"""Run current VDB registration on one sys76 VAP TEP.

Local operator script only.

This intentionally runs the current registration pipeline as-is. It does not
implement genotype-aware ingestion. It measures the current materialized SQLite
registration behavior against a modern TEP-VAP substrate.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from variant_database.registration.registration_orchestrator import (
    run_registration_pipeline,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run current VDB registration on one VAP TEP."
    )
    parser.add_argument(
        "--tep",
        type=Path,
        required=True,
        help="Path to the TEP-VAP package directory.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        required=True,
        help="Output SQLite path.",
    )
    parser.add_argument(
        "--producer-family",
        default="VAP",
        choices=["VAP", "GSC"],
        help="Producer family label.",
    )
    parser.add_argument(
        "--max-rows-per-artifact",
        type=int,
        default=None,
        help="Optional canary limit. Omit for full as-is registration.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Delete existing SQLite output and sidecars before running.",
    )
    return parser.parse_args()


def delete_existing_sqlite_family(db_path: Path) -> None:
    if not db_path.parent.exists():
        return
    for path in db_path.parent.glob(f"{db_path.name}*"):
        path.unlink()


def main() -> int:
    args = parse_args()

    tep = args.tep.expanduser().resolve()
    db = args.db

    if not tep.is_dir():
        raise FileNotFoundError(f"TEP directory not found: {tep}")

    db.parent.mkdir(parents=True, exist_ok=True)

    if args.overwrite:
        delete_existing_sqlite_family(db)

    summary = run_registration_pipeline(
        package_path=tep,
        db_path=db,
        producer_family=args.producer_family,
        max_rows_per_artifact=args.max_rows_per_artifact,
    )

    print("VDB single-TEP registration complete")
    print(f"TEP path: {summary.package_path}")
    print(f"Database: {summary.db_path}")
    print(f"Producer family: {summary.producer_family}")
    print(f"Package exists: {summary.package_exists}")
    print(f"Package ID: {summary.package_id}")
    print(f"Artifacts: {summary.artifact_count}")
    print(f"Assertion registrations: {summary.assertion_registration_count}")
    print(f"Package metadata records: {summary.package_metadata_count}")
    print(f"Coordinate declarations: {summary.coordinate_declaration_count}")
    print(f"Feature declarations: {summary.feature_declaration_count}")
    print(f"Rows scanned: {summary.row_count_scanned}")
    print(f"Participants discovered: {summary.participant_count_discovered}")
    print(f"Source identities: {summary.source_identity_count}")
    print(f"Elapsed seconds: {summary.elapsed_seconds:.2f}")
    print(f"Rows/sec: {summary.rows_per_second:.2f}")
    print(f"Participants/sec: {summary.participants_per_second:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

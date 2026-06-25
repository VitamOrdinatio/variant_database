"""Run the VDB registration pipeline against the HG002 lightweight TEP emulator.

Development script only.

This script exercises the Phase 3 registration vertical slice:

TEP package
    -> package inventory
    -> persistence
    -> assertion registration
    -> assertion participant discovery
    -> source identity attachment

It does not mutate the source TEP fixture.
It writes only to the VDB results/ directory.
"""

from __future__ import annotations

from pathlib import Path

from variant_database.registration.registration_orchestrator import (
    run_registration_pipeline,
)


TEP_PATH = Path(
    "/home/steelsparrow/dev/portfolio_projects/"
    "variant_annotation_pipeline/results/"
    "run_2026_06_03_010030/tep_emulation/"
    "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
)

DB_PATH = Path("results/registration/hg002/vdb.sqlite")


def main() -> int:
    summary = run_registration_pipeline(
        package_path=TEP_PATH,
        db_path=DB_PATH,
        producer_family="VAP",
    )

    print("VDB registration pipeline run complete")
    print(f"TEP path: {summary.package_path}")
    print(f"Database: {summary.db_path}")
    print(f"Producer family: {summary.producer_family}")
    print(f"Package exists: {summary.package_exists}")
    print(f"Package ID: {summary.package_id}")
    print(f"Artifacts: {summary.artifact_count}")
    print(f"Assertion registrations: {summary.assertion_registration_count}")
    print(f"Rows scanned: {summary.row_count_scanned}")
    print(f"Participants discovered: {summary.participant_count_discovered}")
    print(f"Source identities: {summary.source_identity_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

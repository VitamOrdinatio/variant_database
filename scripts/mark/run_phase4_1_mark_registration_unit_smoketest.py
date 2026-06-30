#!/usr/bin/env python3
"""
Run the Phase 4.1 MARK full-corpus Registration Unit smoketest.

This script validates the real canonical Phase 3 Registration Units on MARK,
not the lightweight fixture.

It creates a timestamped receipt directory under:

```
results/validation/phase4_registration_units/
    mark_full_corpus_smoketest_YYYY_MM_DD_HHMMSS/
```

The smoketest performs:

```
manifest creation
read-only Registration Unit inspection
deterministic inventory artifact emission
readiness artifact emission
validation run summary emission
SQLite non-mutation checks
SQLite sidecar checks
optional tgz packaging with SHA256
```

Run from the VDB repository root on MARK inside tmux:

```
python3 scripts/mark/run_phase4_1_mark_registration_unit_smoketest.py
```

"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tarfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANIFEST_COLUMNS = [
    "manifest_schema_version",
    "registration_unit_id",
    "registration_unit_label",
    "producer_family",
    "validation_layer",
    "source_role",
    "registration_backend",
    "registration_unit_path",
    "sqlite_path",
    "expected_read_mode",
    "notes",
]

VALIDATION_LAYER = "validation_layer_3_mark_full_corpus"
SOURCE_ROLE = "mark_phase3_canonical_full_corpus"
REGISTRATION_BACKEND = "sqlite"
EXPECTED_READ_MODE = "read_only"
SQLITE_FILENAME = "vdb.sqlite"
SIDECAR_SUFFIXES = ("-wal", "-shm", "-journal")


@dataclass(frozen=True)
class ExpectedRegistrationUnit:
    """Expected real MARK Phase 3 canonical Registration Unit."""

    registration_unit_id: str
    registration_unit_label: str
    producer_family: str
    registration_unit_path: str
    notes: str

    @property
    def sqlite_path(self) -> str:
        """sqlite_path is intentionally relative to registration_unit_path."""
        return SQLITE_FILENAME

    def as_manifest_row(self) -> dict[str, str]:
        return {
            "manifest_schema_version": "v1",
            "registration_unit_id": self.registration_unit_id,
            "registration_unit_label": self.registration_unit_label,
            "producer_family": self.producer_family,
            "validation_layer": VALIDATION_LAYER,
            "source_role": SOURCE_ROLE,
            "registration_backend": REGISTRATION_BACKEND,
            "registration_unit_path": self.registration_unit_path,
            "sqlite_path": self.sqlite_path,
            "expected_read_mode": EXPECTED_READ_MODE,
            "notes": self.notes,
        }


EXPECTED_REGISTRATION_UNITS = [
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_gsc_epilepsy",
        registration_unit_label="gsc_epilepsy",
        producer_family="GSC",
        registration_unit_path="results/registration/mark_phase3_canonical/gsc_epilepsy",
        notes="Real MARK Phase 3 canonical GSC epilepsy Registration Unit.",
    ),
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_gsc_mitochondrial_disease",
        registration_unit_label="gsc_mitochondrial_disease",
        producer_family="GSC",
        registration_unit_path=(
            "results/registration/mark_phase3_canonical/"
            "gsc_mitochondrial_disease"
        ),
        notes=(
            "Real MARK Phase 3 canonical GSC mitochondrial disease "
            "Registration Unit."
        ),
    ),
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_vap_hg002",
        registration_unit_label="vap_hg002",
        producer_family="VAP",
        registration_unit_path="results/registration/mark_phase3_canonical/vap_hg002",
        notes="Real MARK Phase 3 canonical VAP HG002 Registration Unit.",
    ),
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_vap_median_ERR10619300",
        registration_unit_label="vap_median_ERR10619300",
        producer_family="VAP",
        registration_unit_path=(
            "results/registration/mark_phase3_canonical/"
            "vap_median_ERR10619300"
        ),
        notes=(
            "Real MARK Phase 3 canonical VAP median-depth ERR10619300 "
            "Registration Unit."
        ),
    ),
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_vap_q1_ERR10619212",
        registration_unit_label="vap_q1_ERR10619212",
        producer_family="VAP",
        registration_unit_path=(
            "results/registration/mark_phase3_canonical/vap_q1_ERR10619212"
        ),
        notes=(
            "Real MARK Phase 3 canonical VAP q1-depth ERR10619212 "
            "Registration Unit."
        ),
    ),
    ExpectedRegistrationUnit(
        registration_unit_id="mark_phase3_canonical_vap_q3_ERR10619225",
        registration_unit_label="vap_q3_ERR10619225",
        producer_family="VAP",
        registration_unit_path=(
            "results/registration/mark_phase3_canonical/vap_q3_ERR10619225"
        ),
        notes=(
            "Real MARK Phase 3 canonical VAP q3-depth ERR10619225 "
            "Registration Unit."
        ),
    ),
]


class TeeLogger:
    """Write each message to stdout and to a log file."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text("", encoding="utf-8")

    def log(self, message: str = "") -> None:
        print(message, flush=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{message}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 4.1 Registration Unit smoketest against the real MARK "
            "canonical Phase 3 Registration Units."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="VDB repository root. Default: current directory.",
    )
    parser.add_argument(
        "--real-root",
        default="results/registration/mark_phase3_canonical",
        help="Relative path to the real MARK canonical Registration Unit root.",
    )
    parser.add_argument(
        "--output-parent",
        default="results/validation/phase4_registration_units",
        help="Relative path where timestamped smoketest receipts should be written.",
    )
    parser.add_argument(
        "--run-ts",
        default=None,
        help=(
            "Optional timestamp override in YYYY_MM_DD_HHMMSS format. "
            "Default: current UTC time."
        ),
    )
    parser.add_argument(
        "--no-package",
        action="store_true",
        help="Do not create a .tgz archive and .sha256 file after the run.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Allow writing into an existing run directory. Default behavior is "
            "to fail if the timestamped run directory already exists."
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    repo_root = Path(args.repo_root).resolve()
    real_root = (repo_root / args.real_root).resolve()
    output_parent = (repo_root / args.output_parent).resolve()

    run_ts = args.run_ts or datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")
    run_dir = output_parent / f"mark_full_corpus_smoketest_{run_ts}"

    if run_dir.exists() and not args.overwrite:
        print(f"ERROR: run directory already exists: {run_dir}", flush=True)
        print("Use --overwrite only if you intentionally want to reuse it.", flush=True)
        return 2

    input_dir = run_dir / "inputs"
    log_dir = run_dir / "logs"
    manifest_path = input_dir / "registration_unit_input_manifest.tsv"
    log_path = log_dir / "mark_phase4_1_smoketest.log"

    input_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = TeeLogger(log_path)

    start_time = time.perf_counter()

    logger.log("# Phase 4.1 MARK Registration Unit Smoketest")
    logger.log()
    logger.log(f"repo_root: {repo_root}")
    logger.log(f"real_root: {real_root}")
    logger.log(f"run_dir: {run_dir}")
    logger.log(f"run_ts_utc: {run_ts}")
    logger.log(f"log_path: {log_path}")
    logger.log()

    if not (repo_root / "pyproject.toml").exists():
        logger.log("ERROR: repo_root does not look like the VDB repository root.")
        logger.log(f"Missing: {repo_root / 'pyproject.toml'}")
        return 2

    sys.path.insert(0, str(repo_root / "src"))

    try:
        from variant_database.phase4.registration_units.validation import (
            validate_registration_units_from_manifest,
        )
    except Exception as exc:
        logger.log("ERROR: could not import VDB Registration Unit validator.")
        logger.log(repr(exc))
        return 2

    logger.log("## Preflight: expected SQLite files")
    missing_paths = preflight_expected_sqlite_files(repo_root, logger)

    if missing_paths:
        logger.log()
        logger.log("ERROR: missing expected MARK Registration Unit paths.")
        for path in missing_paths:
            logger.log(f"missing: {path}")
        return 2

    logger.log()
    logger.log("## Preflight: existing SQLite sidecars")
    sidecars_before = find_sqlite_sidecars(real_root)
    if sidecars_before:
        for path in sidecars_before:
            logger.log(f"preexisting_sidecar: {path}")
    else:
        logger.log("preexisting_sidecars: none")

    logger.log()
    logger.log("## Writing MARK full-corpus Registration Unit manifest")
    write_manifest(manifest_path)
    logger.log(f"manifest_path: {manifest_path}")

    logger.log()
    logger.log("## Running validator")
    logger.log(
        "NOTE: this may be read-heavy because the real VAP SQLite files are large."
    )

    try:
        result = validate_registration_units_from_manifest(
            manifest_path=manifest_path,
            output_dir=run_dir,
            repo_root=repo_root,
        )
    except Exception as exc:
        logger.log()
        logger.log("ERROR: validator raised an exception.")
        logger.log(repr(exc))
        return 1

    logger.log()
    logger.log("## Validation result")
    logger.log(f"validation_status: {result.validation_status}")
    logger.log(f"record_count: {result.record_count}")
    logger.log(f"inspection_count: {result.inspection_count}")
    logger.log(f"inventory_row_count: {result.inventory_row_count}")
    logger.log(f"readiness_row_count: {result.readiness_row_count}")
    logger.log(f"ready_count: {result.ready_count}")
    logger.log(f"not_ready_count: {result.not_ready_count}")
    logger.log(f"inspection_status: {result.inspection_status}")
    logger.log(f"inventory_artifact_status: {result.inventory_artifact_status}")
    logger.log(f"readiness_artifact_status: {result.readiness_artifact_status}")
    logger.log(f"non_mutation_status: {result.non_mutation_status}")
    logger.log(f"sidecar_status: {result.sidecar_status}")
    logger.log(f"summary: {result.validation_run_summary_json_path}")

    logger.log()
    logger.log("## Summary JSON extract")
    log_summary_json(run_dir, logger)

    logger.log()
    logger.log("## Postflight: SQLite sidecars")
    sidecars_after = find_sqlite_sidecars(real_root)
    if sidecars_after:
        for path in sidecars_after:
            logger.log(f"postflight_sidecar: {path}")
    else:
        logger.log("postflight_sidecars: none")

    created_sidecars = sorted(set(sidecars_after) - set(sidecars_before))
    if created_sidecars:
        logger.log()
        logger.log("ERROR: new SQLite sidecars detected.")
        for path in created_sidecars:
            logger.log(f"created_sidecar: {path}")

    logger.log()
    logger.log("## Emitted files")
    log_file_listing(run_dir, logger)

    elapsed_seconds = time.perf_counter() - start_time
    logger.log()
    logger.log(f"elapsed_seconds: {elapsed_seconds:.2f}")

    if result.validation_status != "passed":
        logger.log()
        logger.log("ERROR: validation_status was not passed.")
        return 1

    if created_sidecars:
        logger.log()
        logger.log("ERROR: sidecars were created during smoketest.")
        return 1

    if not args.no_package:
        logger.log()
        logger.log("## Packaging receipt directory")
        archive_path = create_tgz_archive(run_dir)
        sha256_path = write_sha256_file(archive_path)
        logger.log(f"archive: {archive_path}")
        logger.log(f"sha256: {sha256_path}")

    logger.log()
    logger.log("MARK Phase 4.1 Registration Unit smoketest completed successfully.")
    return 0


def preflight_expected_sqlite_files(
    repo_root: Path,
    logger: TeeLogger,
) -> list[Path]:
    missing_paths: list[Path] = []

    for unit in EXPECTED_REGISTRATION_UNITS:
        registration_unit_path = repo_root / unit.registration_unit_path
        sqlite_path = registration_unit_path / unit.sqlite_path

        if not registration_unit_path.is_dir():
            missing_paths.append(registration_unit_path)

        if not sqlite_path.is_file():
            missing_paths.append(sqlite_path)
            continue

        size_bytes = sqlite_path.stat().st_size
        logger.log(f"{sqlite_path}\t{size_bytes} bytes")

    return missing_paths


def write_manifest(manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=MANIFEST_COLUMNS,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        for unit in EXPECTED_REGISTRATION_UNITS:
            writer.writerow(unit.as_manifest_row())


def find_sqlite_sidecars(real_root: Path) -> list[Path]:
    sidecars: list[Path] = []

    for suffix in SIDECAR_SUFFIXES:
        sidecars.extend(real_root.glob(f"**/{SQLITE_FILENAME}{suffix}"))

    return sorted(path.resolve() for path in sidecars)


def log_summary_json(run_dir: Path, logger: TeeLogger) -> None:
    summary_path = run_dir / "registration_unit_validation_run_summary.json"

    if not summary_path.is_file():
        logger.log(f"summary_json_missing: {summary_path}")
        return

    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    summary: dict[str, Any] = {
        "validation_status": payload["validation_status"],
        "record_count": payload["record_count"],
        "inspection": payload["inspection"],
        "inventory": {
            "artifact_status": payload["inventory"]["artifact_status"],
            "row_count": payload["inventory"]["row_count"],
        },
        "readiness": {
            "artifact_status": payload["readiness"]["artifact_status"],
            "row_count": payload["readiness"]["row_count"],
            "ready_count": payload["readiness"]["ready_count"],
            "not_ready_count": payload["readiness"]["not_ready_count"],
        },
        "non_mutation": {
            "non_mutation_status": payload["non_mutation"]["non_mutation_status"],
            "sidecar_status": payload["non_mutation"]["sidecar_status"],
            "mutation_details": payload["non_mutation"]["mutation_details"],
            "sidecar_details": payload["non_mutation"]["sidecar_details"],
        },
    }

    logger.log(json.dumps(summary, indent=2, sort_keys=True))


def log_file_listing(run_dir: Path, logger: TeeLogger) -> None:
    for path in sorted(run_dir.rglob("*")):
        if path.is_file():
            relative = path.relative_to(run_dir)
            size_bytes = path.stat().st_size
            logger.log(f"{relative}\t{size_bytes} bytes")


def create_tgz_archive(run_dir: Path) -> Path:
    archive_path = run_dir.with_suffix(".tgz")

    if archive_path.exists():
        archive_path.unlink()

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(run_dir, arcname=run_dir.name)

    return archive_path


def write_sha256_file(path: Path) -> Path:
    digest = sha256sum(path)
    sha256_path = Path(f"{path}.sha256")
    sha256_path.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    return sha256_path


def sha256sum(path: Path) -> str:
    hasher = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

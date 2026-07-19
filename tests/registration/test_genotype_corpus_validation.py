from __future__ import annotations

import csv
import inspect
import json
import sqlite3
from pathlib import Path

from variant_database.registration import genotype_validation
from variant_database.registration.genotype_corpus_validation import (
    MATRIX_SCHEMA_VERSION,
    MATRIX_TSV_FILENAME,
    REPORT_SCHEMA_VERSION,
    REPORT_JSON_FILENAME,
    REPORT_TSV_FILENAME,
    SUMMARY_JSON_FILENAME,
    SUMMARY_SCHEMA_VERSION,
    SUMMARY_TSV_FILENAME,
    MixedCorpusPackageInput,
    validate_mixed_corpus_genotype_scope,
)


def _make_db(
    path: Path,
    *,
    package_id: str,
    package_path: str,
    producer_family: str,
    applicability: str,
    capability: str,
    maturity: str,
    artifact_set_status: str,
    provenance_status: str,
    trusted_ready: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE tep_packages (
            package_id TEXT PRIMARY KEY,
            package_path TEXT NOT NULL,
            package_exists INTEGER NOT NULL,
            artifact_count INTEGER NOT NULL,
            manifest_count INTEGER NOT NULL
        );

        CREATE TABLE source_genotype_package_classifications (
            package_id TEXT PRIMARY KEY,
            producer_family TEXT NOT NULL,
            producer_genotype_applicability_state TEXT NOT NULL,
            genotype_capability_state TEXT NOT NULL,
            genotype_maturity_state TEXT NOT NULL,
            genotype_artifact_set_status TEXT NOT NULL,
            execution_provenance_status TEXT NOT NULL,
            trusted_modern_ingestion_ready INTEGER NOT NULL,
            classification_status TEXT NOT NULL,
            classification_reason TEXT NOT NULL
        );
        """
    )
    connection.execute(
        "INSERT INTO tep_packages VALUES (?, ?, 1, 1, 1)",
        (package_id, package_path),
    )
    connection.execute(
        """
        INSERT INTO source_genotype_package_classifications VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, 'classified', ?
        )
        """,
        (
            package_id,
            producer_family,
            applicability,
            capability,
            maturity,
            artifact_set_status,
            provenance_status,
            trusted_ready,
            "test_reason",
        ),
    )
    connection.commit()
    connection.close()


def _inputs(tmp_path: Path) -> list[MixedCorpusPackageInput]:
    vap_db = tmp_path / "vap.sqlite"
    epi_db = tmp_path / "epi.sqlite"
    mito_db = tmp_path / "mito.sqlite"

    _make_db(
        vap_db,
        package_id="vap-package",
        package_path="/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1",
        producer_family="VAP",
        applicability="genotype_applicable_to_producer_type",
        capability="genotype_capability_available",
        maturity="genotype_discovered",
        artifact_set_status="genotype_artifact_set_complete",
        provenance_status="execution_provenance_registered_as_context",
        trusted_ready=1,
    )
    for path, package_id in ((epi_db, "epi-package"), (mito_db, "mito-package")):
        _make_db(
            path,
            package_id=package_id,
            package_path=f"/gsc/{package_id}",
            producer_family="GSC",
            applicability="genotype_not_applicable_to_producer_type",
            capability="genotype_capability_not_applicable",
            maturity="genotype_maturity_not_applicable",
            artifact_set_status="genotype_artifact_set_not_applicable",
            provenance_status="execution_provenance_not_applicable",
            trusted_ready=0,
        )

    return [
        MixedCorpusPackageInput(
            label="vap_ERR10619300",
            database_path=vap_db,
            tep_id="vap_tep_ERR10619300_run_2026_07_14_114546_v1",
            expected_producer_family="VAP",
            expected_applicability_state="genotype_applicable_to_producer_type",
            expected_capability_state="genotype_capability_available",
            expected_maturity_state="genotype_discovered",
            expected_artifact_set_status="genotype_artifact_set_complete",
            expected_execution_provenance_status="execution_provenance_registered_as_context",
            expected_trusted_modern_ingestion_ready=1,
            individual_validation_status="passed",
            individual_validated_maturity_state="genotype_discovered",
        ),
        MixedCorpusPackageInput(
            label="gsc_epilepsy",
            database_path=epi_db,
            tep_id="gsc_tep_epilepsy_semantic_gtr_experimental_v0_1",
            expected_producer_family="GSC",
            expected_applicability_state="genotype_not_applicable_to_producer_type",
            expected_capability_state="genotype_capability_not_applicable",
            expected_maturity_state="genotype_maturity_not_applicable",
            expected_artifact_set_status="genotype_artifact_set_not_applicable",
            expected_execution_provenance_status="execution_provenance_not_applicable",
            expected_trusted_modern_ingestion_ready=0,
            individual_validation_status="passed",
            individual_validated_maturity_state="genotype_maturity_not_applicable",
        ),
        MixedCorpusPackageInput(
            label="gsc_mitochondrial_disease",
            database_path=mito_db,
            tep_id="gsc_tep_mitochondrial_semantic_gtr_experimental_v0_1",
            expected_producer_family="GSC",
            expected_applicability_state="genotype_not_applicable_to_producer_type",
            expected_capability_state="genotype_capability_not_applicable",
            expected_maturity_state="genotype_maturity_not_applicable",
            expected_artifact_set_status="genotype_artifact_set_not_applicable",
            expected_execution_provenance_status="execution_provenance_not_applicable",
            expected_trusted_modern_ingestion_ready=0,
            individual_validation_status="passed",
            individual_validated_maturity_state="genotype_maturity_not_applicable",
        ),
    ]


def _validate(inputs: list[MixedCorpusPackageInput], output: Path):
    return validate_mixed_corpus_genotype_scope(
        inputs,
        output,
        validation_timestamp="2026-07-18T20:00:00Z",
        expected_package_count=3,
        expected_family_counts={"VAP": 1, "GSC": 2},
        expected_genotype_applicable_count=1,
        expected_genotype_not_applicable_count=2,
        expected_maturity_floor="genotype_discovered",
    )


def test_valid_declared_three_package_corpus_passes(tmp_path: Path) -> None:
    output = tmp_path / "validation"
    result = _validate(_inputs(tmp_path), output)

    assert result.validation_status == "passed"
    assert result.mixed_corpus_exercised is True
    assert result.summary["package_count"] == 3
    assert result.summary["genotype_applicable_count"] == 1
    assert result.summary["genotype_not_applicable_count"] == 2
    assert result.summary["genotype_applicable_package_maturity_floor"] == "genotype_discovered"
    assert result.summary["failed_check_count"] == 0

    for filename in (
        REPORT_JSON_FILENAME,
        REPORT_TSV_FILENAME,
        SUMMARY_JSON_FILENAME,
        SUMMARY_TSV_FILENAME,
        MATRIX_TSV_FILENAME,
    ):
        assert (output / filename).is_file()

    report = json.loads((output / REPORT_JSON_FILENAME).read_text())
    assert report["schema_version"] == REPORT_SCHEMA_VERSION

    summary = json.loads((output / SUMMARY_JSON_FILENAME).read_text())
    assert summary["schema_version"] == SUMMARY_SCHEMA_VERSION
    assert summary["mixed_corpus_exercised"] is True

    with (output / REPORT_TSV_FILENAME).open(newline="") as handle:
        report_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert report_rows
    assert {row["schema_version"] for row in report_rows} == {
        REPORT_SCHEMA_VERSION
    }

    with (output / SUMMARY_TSV_FILENAME).open(newline="") as handle:
        summary_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(summary_rows) == 1
    assert summary_rows[0]["schema_version"] == SUMMARY_SCHEMA_VERSION

    with (output / MATRIX_TSV_FILENAME).open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 3
    assert {row["schema_version"] for row in rows} == {MATRIX_SCHEMA_VERSION}
    assert {row["corpus_pairing_status"] for row in rows} == {"passed"}


def test_gsc_genotype_discovered_fails_maturity_pairing(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    connection = sqlite3.connect(inputs[1].database_path)
    connection.execute(
        """
        UPDATE source_genotype_package_classifications
        SET genotype_maturity_state = 'genotype_discovered'
        """
    )
    connection.commit()
    connection.close()

    result = _validate(inputs, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.mixed_corpus_exercised is False
    assert result.summary["maturity_applicability_pairing_failure_count"] == 1
    assert result.summary["expected_pairing_failure_count"] == 1


def test_duplicate_package_ids_fail_uniqueness(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    connection = sqlite3.connect(inputs[2].database_path)
    connection.execute(
        "UPDATE tep_packages SET package_id = 'epi-package'"
    )
    connection.execute(
        "UPDATE source_genotype_package_classifications SET package_id = 'epi-package'"
    )
    connection.commit()
    connection.close()

    result = _validate(inputs, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.mixed_corpus_exercised is False
    assert result.summary["unique_package_id_count"] == 2


def test_single_package_validator_does_not_claim_mixed_corpus_receipt() -> None:
    source = inspect.getsource(genotype_validation)
    assert '"mixed_corpus_genotype_scope_receipt"' not in source

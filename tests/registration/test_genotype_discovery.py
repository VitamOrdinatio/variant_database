from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from variant_database.ingestion.package_scanner import scan_package
from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.genotype_repositories import (
    persist_genotype_artifact_index_records,
    persist_genotype_context_index_records,
    persist_genotype_package_classification,
)
from variant_database.persistence.repositories import (
    list_artifact_records,
    persist_package_inventory,
)
from variant_database.persistence.schema_manager import initialize_schema
from variant_database.registration.genotype_extractor import (
    build_genotype_discovery_records,
)
from variant_database.registration.genotype_validation import (
    validate_genotype_discovery_database,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    _write(path, json.dumps(payload, sort_keys=True))


def _make_modern_vap_tep(root: Path, *, omit: set[str] | None = None) -> Path:
    omit = omit or set()

    if "entity_inventory.json" not in omit:
        _write_json(root / "entity_inventory.json", {"schema_version": "test"})
    if "lineage_manifest.json" not in omit:
        _write_json(root / "lineage_manifest.json", {"schema_version": "test"})
    if "validation_report.md" not in omit:
        _write(root / "validation_report.md", "# validation\n")

    if "genotype_observations.tsv" not in omit:
        _write(
            root / "entities/genotype/genotype_observations.tsv",
            (
                "schema_version\tgenotype_observation_id\tsample_id\trun_id\t"
                "source_record_hash\treference_build\tchromosome\tposition\t"
                "reference_allele\talternate_alleles_raw\tcalled_allele_indices\t"
                "gt_raw\tad_raw\tdp_raw\tgq_raw\tpl_raw\t"
                "variant_relationship_status\trelationship_reason\t"
                "relationship_resolution_target\tvariant_id\n"
                "genotype_observation_v1\tg1\tS1\tR1\thash1\tGRCh38\t1\t100\t"
                "A\tG\t0,1\t0/1\t10,5\t15\t99\t1,2,3\t"
                "direct\tbiallelic_direct\tnone\t1:100:A:G\n"
            ),
        )

    if "genotype_projection_summary.json" not in omit:
        _write_json(
            root / "entities/genotype/genotype_projection_summary.json",
            {
                "schema_version": "genotype_projection_summary_v1",
                "counts": {
                    "genotype_observation_row_count": 1,
                    "direct_relationship_count": 1,
                    "complex_relationship_count": 0,
                    "unresolved_relationship_count": 0,
                    "projection_error_count": 0,
                    "projection_warning_count": 0,
                },
                "projection": {
                    "projection_status": "pass",
                    "reference_build": "GRCh38",
                },
                "sample_resolution": {
                    "sample_id": "S1",
                    "run_id": "R1",
                },
                "source_vcf": {
                    "source_record_count": 1,
                    "sha256": "vcf-sha",
                    "header_hash": "header-hash",
                },
            },
        )

    if "genotype_source_header_context.json" not in omit:
        _write_json(
            root / "entities/genotype/genotype_source_header_context.json",
            {
                "schema_version": "genotype_source_header_context_v1",
                "reference_context": {
                    "reference_build": "GRCh38",
                },
                "sample_columns": ["S1"],
                "format_definitions": [],
                "contig_declarations": [],
                "source_vcf": {
                    "sha256": "vcf-sha",
                    "header_hash": "header-hash",
                },
            },
        )

    if "execution_provenance.json" not in omit:
        _write_json(
            root / "entities/context/execution_provenance.json",
            {
                "schema_version": "1.0.0",
                "contract_status": "pass",
                "provenance_completeness": "complete",
                "toolchain_environment": {},
                "annotation_environment": {},
                "resource_environment": {},
            },
        )

    return root


def _discover_and_persist(
    tep: Path,
    db: Path,
    producer_family: str = "VAP",
) -> sqlite3.Connection:
    connection = connect_sqlite(db)
    initialize_schema(connection)

    inventory = scan_package(tep)
    package_id = persist_package_inventory(connection, inventory)
    artifact_records = list_artifact_records(connection, package_id)

    records = build_genotype_discovery_records(
        package_id=package_id,
        package_path=inventory.package_path,
        artifact_records=artifact_records,
        producer_family=producer_family,
    )

    persist_genotype_package_classification(
        connection=connection,
        classification=records["classification"],
    )
    persist_genotype_artifact_index_records(
        connection=connection,
        records=records["artifact_index_records"],
    )
    persist_genotype_context_index_records(
        connection=connection,
        records=records["context_index_records"],
    )

    return connection


def test_schema_creates_genotype_discovery_tables(tmp_path: Path) -> None:
    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }

    assert "source_genotype_package_classifications" in tables
    assert "source_genotype_artifact_index" in tables
    assert "source_genotype_context_index" in tables


def test_complete_modern_vap_classifies_available_and_indexes_context(tmp_path: Path) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    connection = _discover_and_persist(tep, tmp_path / "vdb.sqlite")

    classification = dict(
        connection.execute(
            """
            SELECT
                producer_genotype_applicability_state,
                genotype_capability_state,
                genotype_maturity_state,
                genotype_artifact_set_status,
                execution_provenance_status,
                trusted_modern_ingestion_ready,
                classification_reason
            FROM source_genotype_package_classifications
            """
        ).fetchone()
    )

    assert classification["producer_genotype_applicability_state"] == "genotype_applicable_to_producer_type"
    assert (
        classification["genotype_capability_state"]
        == "genotype_capability_available"
    ), classification["classification_reason"]
    assert classification["genotype_maturity_state"] == "genotype_discovered"
    assert classification["genotype_artifact_set_status"] == "genotype_artifact_set_complete"
    assert classification["execution_provenance_status"] == "execution_provenance_registered_as_context"
    assert classification["trusted_modern_ingestion_ready"] == 1

    artifact_count = connection.execute(
        "SELECT COUNT(*) FROM source_genotype_artifact_index"
    ).fetchone()[0]
    context_count = connection.execute(
        "SELECT COUNT(*) FROM source_genotype_context_index"
    ).fetchone()[0]

    assert artifact_count == 3
    assert context_count == 3

    execution_context = dict(
        connection.execute(
            """
            SELECT
                registered_as_context,
                registered_as_biological_evidence,
                contract_status,
                provenance_completeness
            FROM source_genotype_context_index
            WHERE context_kind = 'execution_provenance'
            """
        ).fetchone()
    )

    assert execution_context["registered_as_context"] == 1
    assert execution_context["registered_as_biological_evidence"] == 0
    assert execution_context["contract_status"] == "pass"
    assert execution_context["provenance_completeness"] == "complete"


def test_partial_genotype_artifact_set_is_incomplete_not_legacy(tmp_path: Path) -> None:
    tep = _make_modern_vap_tep(
        tmp_path / "tep",
        omit={"genotype_source_header_context.json"},
    )
    connection = _discover_and_persist(tep, tmp_path / "vdb.sqlite")

    classification = dict(
        connection.execute(
            """
            SELECT genotype_capability_state, genotype_artifact_set_status, classification_reason
            FROM source_genotype_package_classifications
            """
        ).fetchone()
    )

    assert classification["genotype_capability_state"] == "genotype_capability_incomplete"
    assert classification["genotype_artifact_set_status"] == "genotype_artifact_set_incomplete"
    assert "missing_genotype_artifacts" in classification["classification_reason"]


def test_gsc_is_genotype_not_applicable_not_failed(tmp_path: Path) -> None:
    tep = tmp_path / "gsc_tep"
    _write_json(tep / "entity_inventory.json", {"schema_version": "test"})

    connection = _discover_and_persist(
        tep,
        tmp_path / "vdb.sqlite",
        producer_family="GSC",
    )

    classification = dict(
        connection.execute(
            """
            SELECT
                producer_genotype_applicability_state,
                genotype_capability_state,
                genotype_maturity_state,
                genotype_artifact_set_status,
                classification_reason
            FROM source_genotype_package_classifications
            """
        ).fetchone()
    )

    assert classification["producer_genotype_applicability_state"] == "genotype_not_applicable_to_producer_type"
    assert (
        classification["genotype_capability_state"]
        == "genotype_capability_not_applicable"
    )
    assert (
        classification["genotype_maturity_state"]
        == "genotype_maturity_not_applicable"
    )
    assert classification["genotype_artifact_set_status"] == "genotype_artifact_set_not_applicable"
    assert classification["classification_reason"] == "genotype_not_applicable_to_producer_type"


def _validate_database(
    db: Path,
    output_dir: Path,
):
    return validate_genotype_discovery_database(
        database_path=db,
        validation_output_dir=output_dir,
        validation_timestamp="2026-07-18T05:00:00Z",
    )


def test_genotype_discovery_validation_emits_passing_receipts(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "passed"
    assert result.validated_maturity_state == "genotype_discovered"
    assert result.report_json_path.is_file()
    assert result.report_tsv_path.is_file()
    assert result.summary_json_path.is_file()
    assert result.summary_tsv_path.is_file()

    payload = json.loads(result.summary_json_path.read_text())
    assert payload["validation_status"] == "passed"
    assert payload["validated_maturity_state"] == "genotype_discovered"
    assert payload["mixed_corpus_exercised"] is False
    assert all(
        status == "passed"
        for status in payload["receipt_statuses"].values()
    )


def test_genotype_discovery_validation_fails_count_mismatch(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)

    connection.execute(
        """
        UPDATE source_genotype_context_index
        SET direct_relationship_count = 0
        WHERE context_kind = 'genotype_projection_summary'
        """
    )
    connection.commit()
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"

    failed_ids = {
        check.check_id
        for check in result.checks
        if check.status == "failed"
    }
    assert (
        "producer_summary_relationship_partition_reconciliation"
        in failed_ids
    )


def test_genotype_discovery_validation_rejects_provenance_as_biological_evidence(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)

    connection.execute(
        """
        UPDATE source_genotype_context_index
        SET registered_as_biological_evidence = 1
        WHERE context_kind = 'execution_provenance'
        """
    )
    connection.commit()
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"

    failed_ids = {
        check.check_id
        for check in result.checks
        if check.status == "failed"
    }
    assert "execution_provenance_not_biological_evidence" in failed_ids


def test_legacy_vap_passes_discovery_with_explicit_unavailable_state(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(
        tmp_path / "tep",
        omit={
            "genotype_observations.tsv",
            "genotype_projection_summary.json",
            "genotype_source_header_context.json",
            "execution_provenance.json",
        },
    )
    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "passed"
    assert result.validated_maturity_state == "genotype_discovered"

    summary = json.loads(result.summary_json_path.read_text())
    assert summary["validation_status"] == "passed"


def test_unsupported_genotype_schema_fails_trusted_discovery(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    observations = (
        tep / "entities/genotype/genotype_observations.tsv"
    )
    observations.write_text(
        observations.read_text().replace(
            "genotype_observation_v1",
            "genotype_observation_v999",
        ),
        encoding="utf-8",
    )

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"


def test_missing_execution_provenance_fails_modern_trusted_discovery(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(
        tmp_path / "tep",
        omit={"execution_provenance.json"},
    )
    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"


def test_failed_execution_provenance_contract_fails_discovery(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    provenance_path = (
        tep / "entities/context/execution_provenance.json"
    )
    payload = json.loads(provenance_path.read_text())
    payload["contract_status"] = "fail"
    _write_json(provenance_path, payload)

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"


def test_malformed_projection_summary_fails_discovery(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")
    _write(
        tep / "entities/genotype/genotype_projection_summary.json",
        "{not-json",
    )

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(tep, db)
    connection.close()

    result = _validate_database(db, tmp_path / "validation")

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"


def test_gsc_discovery_validation_passes_with_not_applicable_capability(
    tmp_path: Path,
) -> None:
    tep = tmp_path / "gsc_tep"
    _write_json(
        tep / "entity_inventory.json",
        {"schema_version": "test"},
    )

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(
        tep,
        db,
        producer_family="GSC",
    )
    connection.close()

    result = _validate_database(
        db,
        tmp_path / "validation",
    )

    assert result.validation_status == "passed"
    assert result.validated_maturity_state == "genotype_maturity_not_applicable"

    checks = {
        check.check_id: check
        for check in result.checks
    }
    pairing = checks[
        "producer_capability_applicability_pairing"
    ]

    assert pairing.status == "passed"
    assert (
        "genotype_capability_not_applicable"
        in pairing.observed
    )


def test_undeclared_producer_family_is_rejected(
    tmp_path: Path,
) -> None:
    tep = tmp_path / "rsp_tep"
    _write_json(
        tep / "entity_inventory.json",
        {"schema_version": "test"},
    )

    with pytest.raises(
        ValueError,
        match="Unsupported producer family for genotype classification",
    ):
        _discover_and_persist(
            tep,
            tmp_path / "vdb.sqlite",
            producer_family="RSP",
        )


def test_gsc_legacy_capability_pairing_fails_validation(
    tmp_path: Path,
) -> None:
    tep = tmp_path / "gsc_tep"
    _write_json(
        tep / "entity_inventory.json",
        {"schema_version": "test"},
    )

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(
        tep,
        db,
        producer_family="GSC",
    )

    connection.execute(
        """
        UPDATE source_genotype_package_classifications
        SET genotype_capability_state =
            'genotype_capability_unavailable_legacy'
        """
    )
    connection.commit()
    connection.close()

    result = _validate_database(
        db,
        tmp_path / "validation",
    )

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"

    failed_ids = {
        check.check_id
        for check in result.checks
        if check.status == "failed"
    }

    assert (
        "producer_capability_applicability_pairing"
        in failed_ids
    )


def test_gsc_discovered_maturity_pairing_fails_validation(
    tmp_path: Path,
) -> None:
    tep = tmp_path / "gsc_tep"
    _write_json(
        tep / "entity_inventory.json",
        {"schema_version": "test"},
    )

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(
        tep,
        db,
        producer_family="GSC",
    )

    connection.execute(
        """
        UPDATE source_genotype_package_classifications
        SET genotype_maturity_state = 'genotype_discovered'
        """
    )
    connection.commit()
    connection.close()

    result = _validate_database(
        db,
        tmp_path / "validation",
    )

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"

    failed_ids = {
        check.check_id
        for check in result.checks
        if check.status == "failed"
    }

    assert (
        "producer_maturity_applicability_pairing"
        in failed_ids
    )


def test_vap_not_applicable_maturity_pairing_fails_validation(
    tmp_path: Path,
) -> None:
    tep = _make_modern_vap_tep(tmp_path / "tep")

    db = tmp_path / "vdb.sqlite"
    connection = _discover_and_persist(
        tep,
        db,
        producer_family="VAP",
    )

    connection.execute(
        """
        UPDATE source_genotype_package_classifications
        SET genotype_maturity_state =
            'genotype_maturity_not_applicable'
        """
    )
    connection.commit()
    connection.close()

    result = _validate_database(
        db,
        tmp_path / "validation",
    )

    assert result.validation_status == "failed"
    assert result.validated_maturity_state == "not_claimed"

    failed_ids = {
        check.check_id
        for check in result.checks
        if check.status == "failed"
    }

    assert (
        "producer_maturity_applicability_pairing"
        in failed_ids
    )

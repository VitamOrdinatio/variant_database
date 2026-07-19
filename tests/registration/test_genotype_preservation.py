from __future__ import annotations

import csv
import json
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
from variant_database.registration.genotype_preservation import (
    GenotypePreservationRequest,
    preserve_genotype_observations,
)
from variant_database.registration.genotype_preservation_validation import (
    validate_genotype_preservation_database,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    _write(path, json.dumps(payload, sort_keys=True))


def _make_tep(root: Path, row_count: int = 3) -> Path:
    _write_json(root / "entity_inventory.json", {"schema_version": "test"})
    _write_json(root / "lineage_manifest.json", {"schema_version": "test"})
    _write(root / "validation_report.md", "# validation\n")

    columns = [
        "schema_version",
        "genotype_observation_id",
        "genotype_observation_id_version",
        "sample_id",
        "run_id",
        "source_vcf_path",
        "source_vcf_sha256",
        "source_vcf_header_hash",
        "source_record_ordinal",
        "source_line_number",
        "source_record_hash",
        "reference_build",
        "chromosome",
        "position",
        "reference_allele",
        "alternate_alleles_raw",
        "called_allele_indices",
        "format_raw",
        "sample_format_raw",
        "gt_raw",
        "ad_raw",
        "dp_raw",
        "gq_raw",
        "pl_raw",
        "variant_relationship_status",
        "relationship_reason",
        "relationship_resolution_target",
        "variant_id",
    ]
    path = root / "entities/genotype/genotype_observations.tsv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        for index in range(1, row_count + 1):
            writer.writerow(
                {
                    "schema_version": "genotype_observation_v1",
                    "genotype_observation_id": f"g{index}",
                    "genotype_observation_id_version": "genotype_observation_id_v1",
                    "sample_id": "S1",
                    "run_id": "R1",
                    "source_vcf_path": "/source.vcf.gz",
                    "source_vcf_sha256": "vcf-sha",
                    "source_vcf_header_hash": "header-hash",
                    "source_record_ordinal": str(index),
                    "source_line_number": str(index + 100),
                    "source_record_hash": f"record-hash-{index}",
                    "reference_build": "GRCh38",
                    "chromosome": "1",
                    "position": str(100 + index),
                    "reference_allele": "A",
                    "alternate_alleles_raw": "G",
                    "called_allele_indices": "0,1",
                    "format_raw": "GT:AD:DP:GQ:PL",
                    "sample_format_raw": "0/1:10,5:15:99:1,2,3",
                    "gt_raw": "0/1",
                    "ad_raw": "10,5",
                    "dp_raw": "15",
                    "gq_raw": "99",
                    "pl_raw": "1,2,3",
                    "variant_relationship_status": "direct",
                    "relationship_reason": "biallelic_direct",
                    "relationship_resolution_target": "none",
                    "variant_id": f"1:{100 + index}:A:G",
                }
            )

    _write_json(
        root / "entities/genotype/genotype_projection_summary.json",
        {
            "schema_version": "genotype_projection_summary_v1",
            "counts": {
                "genotype_observation_row_count": row_count,
                "direct_relationship_count": row_count,
                "complex_relationship_count": 0,
                "unresolved_relationship_count": 0,
                "not_applicable_relationship_count": 0,
                "projection_error_count": 0,
                "projection_warning_count": 0,
            },
            "projection": {
                "projection_status": "pass",
                "reference_build": "GRCh38",
            },
            "sample_resolution": {"sample_id": "S1", "run_id": "R1"},
            "source_vcf": {
                "source_record_count": row_count,
                "sha256": "vcf-sha",
                "header_hash": "header-hash",
            },
        },
    )
    _write_json(
        root / "entities/genotype/genotype_source_header_context.json",
        {
            "schema_version": "genotype_source_header_context_v1",
            "reference_context": {"reference_build": "GRCh38"},
            "sample_columns": ["S1"],
            "source_vcf": {
                "sha256": "vcf-sha",
                "header_hash": "header-hash",
            },
        },
    )
    _write_json(
        root / "entities/context/execution_provenance.json",
        {
            "schema_version": "1.0.0",
            "contract_status": "pass",
            "provenance_completeness": "complete",
        },
    )
    return root


def _discovery_db(tep: Path, db: Path):
    connection = connect_sqlite(db)
    initialize_schema(connection)
    inventory = scan_package(tep)
    package_id = persist_package_inventory(connection, inventory)
    artifacts = list_artifact_records(connection, package_id)
    records = build_genotype_discovery_records(
        package_id=package_id,
        package_path=inventory.package_path,
        artifact_records=artifacts,
        producer_family="VAP",
    )
    persist_genotype_package_classification(connection, records["classification"])
    persist_genotype_artifact_index_records(connection, records["artifact_index_records"])
    persist_genotype_context_index_records(connection, records["context_index_records"])
    return connection, package_id


def test_schema_creates_genotype_preservation_tables(tmp_path: Path) -> None:
    connection = connect_sqlite(tmp_path / "vdb.sqlite")
    initialize_schema(connection)
    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    assert "source_genotype_preservation_scopes" in tables
    assert "source_genotype_observations" in tables


def test_bounded_preservation_is_lossless_and_does_not_advance_maturity(
    tmp_path: Path,
) -> None:
    tep = _make_tep(tmp_path / "tep", row_count=3)
    connection, package_id = _discovery_db(tep, tmp_path / "vdb.sqlite")

    summary = preserve_genotype_observations(
        connection,
        GenotypePreservationRequest(
            package_id=package_id,
            scope_label="genotype_first1k_smoke_test",
            source_tep_id="vap_test",
            row_limit=2,
            batch_size=1,
        ),
    )

    assert summary.selected_row_count == 2
    assert summary.first_selected_source_row == 1
    assert summary.last_selected_source_row == 2
    assert summary.source_column_count == 28

    rows = connection.execute(
        """
        SELECT source_row_number, genotype_observation_id,
               raw_source_values_json, gt_raw, ad_raw
        FROM source_genotype_observations
        ORDER BY source_row_number
        """
    ).fetchall()
    assert [row["genotype_observation_id"] for row in rows] == ["g1", "g2"]
    assert [row["source_row_number"] for row in rows] == [1, 2]
    source_columns = json.loads(
        connection.execute(
            "SELECT source_column_order_json FROM source_genotype_preservation_scopes"
        ).fetchone()[0]
    )
    first_raw = dict(
        zip(source_columns, json.loads(rows[0]["raw_source_values_json"]), strict=True)
    )
    assert first_raw["gt_raw"] == rows[0]["gt_raw"] == "0/1"
    assert first_raw["ad_raw"] == rows[0]["ad_raw"] == "10,5"

    maturity = connection.execute(
        "SELECT genotype_maturity_state FROM source_genotype_package_classifications"
    ).fetchone()[0]
    assert maturity == "genotype_discovered"


def test_bounded_preservation_validation_claims_preservation_maturity(
    tmp_path: Path,
) -> None:
    tep = _make_tep(tmp_path / "tep", row_count=3)
    db = tmp_path / "vdb.sqlite"
    connection, package_id = _discovery_db(tep, db)
    preserve_genotype_observations(
        connection,
        GenotypePreservationRequest(
            package_id=package_id,
            scope_label="genotype_first1k_smoke_test",
            source_tep_id="vap_test",
            row_limit=2,
        ),
    )
    connection.close()

    result = validate_genotype_preservation_database(
        db,
        tmp_path / "validation",
        validation_timestamp="2026-07-19T01:00:00Z",
        expected_scope_label="genotype_first1k_smoke_test",
        expected_row_limit=2,
        expected_source_tep_id="vap_test",
    )

    assert result.validation_status == "passed"
    assert result.validated_maturity_state == "genotype_preservation_validated"
    assert result.summary["observed_row_count"] == 2
    assert result.summary["producer_observation_split_count"] == 0
    assert result.summary["inheritance_assertion_count"] == 0
    assert result.summary["failed_check_count"] == 0


def test_short_source_rolls_back_preservation_scope_and_rows(tmp_path: Path) -> None:
    tep = _make_tep(tmp_path / "tep", row_count=2)
    connection, package_id = _discovery_db(tep, tmp_path / "vdb.sqlite")

    with pytest.raises(ValueError, match="Requested bounded preservation"):
        preserve_genotype_observations(
            connection,
            GenotypePreservationRequest(
                package_id=package_id,
                scope_label="genotype_first1k_smoke_test",
                source_tep_id="vap_test",
                row_limit=3,
            ),
        )

    assert connection.execute(
        "SELECT COUNT(*) FROM source_genotype_preservation_scopes"
    ).fetchone()[0] == 0
    assert connection.execute(
        "SELECT COUNT(*) FROM source_genotype_observations"
    ).fetchone()[0] == 0


def test_preservation_rejects_duplicate_scope(tmp_path: Path) -> None:
    tep = _make_tep(tmp_path / "tep", row_count=2)
    connection, package_id = _discovery_db(tep, tmp_path / "vdb.sqlite")
    request = GenotypePreservationRequest(
        package_id=package_id,
        scope_label="genotype_first1k_smoke_test",
        source_tep_id="vap_test",
        row_limit=2,
    )
    preserve_genotype_observations(connection, request)

    with pytest.raises(ValueError, match="scope already exists"):
        preserve_genotype_observations(connection, request)

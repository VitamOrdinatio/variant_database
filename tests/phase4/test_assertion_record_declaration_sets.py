from __future__ import annotations

import csv
import json
from pathlib import Path
import sqlite3

from variant_database.persistence.backend import connect_sqlite
from variant_database.persistence.schema_manager import initialize_schema
from variant_database.phase4.assertion_records.builder import build_assertion_records


def _write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _seed_base_registration_unit(db_path: Path, *, producer_family: str = "VAP") -> sqlite3.Connection:
    conn = connect_sqlite(db_path)
    initialize_schema(conn)
    conn.execute(
        """
        INSERT INTO tep_packages (
            package_id, package_path, package_exists, artifact_count, manifest_count
        ) VALUES (?, ?, ?, ?, ?)
        """,
        ("pkg_vap", "/tmp/vap_tep_HG002_run_2026_06_03_010030_v1", 1, 1, 0),
    )
    conn.execute(
        """
        INSERT INTO artifacts (
            artifact_id, package_id, relative_path, size_bytes, sha256, is_manifest
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "artifact_variants",
            "pkg_vap",
            "entities/normalization/stage_08_vdb_ready_variants.tsv",
            123,
            "a" * 64,
            0,
        ),
    )
    conn.execute(
        """
        INSERT INTO assertion_registrations (
            assertion_registration_id,
            package_id,
            artifact_id,
            surface_role,
            evidence_domain,
            producer_family,
            source_record_ref,
            assertion_type,
            participant_summary_json,
            support_ref_json,
            authority_context,
            uncertainty_context,
            registration_status,
            payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "ar_src_001",
            "pkg_vap",
            "artifact_variants",
            "normalization",
            "variant",
            producer_family,
            "",
            "variant_normalization" if producer_family == "VAP" else "producer_contract_validation",
            "{}",
            "{}",
            "producer_asserted",
            "not_evaluated",
            "registered",
            "{}",
        ),
    )
    conn.commit()
    return conn


def _insert_source_identity(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        INSERT INTO source_identities (
            source_identity_id,
            assertion_registration_id,
            identity_kind,
            participant_role,
            source_value,
            source_namespace,
            source_label,
            extraction_method,
            source_record_ref,
            payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "sid_variant_001",
            "ar_src_001",
            "variant",
            "variant",
            "1:895427:G:C",
            "vap_variant_id",
            "1:895427:G:C",
            "test_fixture",
            "row:1",
            "{}",
        ),
    )


def _insert_coordinate_declaration(conn: sqlite3.Connection, declaration_id: str, *, row_ref: str, variant: str) -> None:
    conn.execute(
        """
        INSERT INTO source_coordinate_declarations (
            coordinate_declaration_id,
            assertion_registration_id,
            source_identity_id,
            source_record_ref,
            source_artifact_path,
            variant_source_namespace,
            variant_source_value,
            variant_source_label,
            reference_genome_build,
            reference_context_source,
            chromosome,
            position,
            start,
            end,
            reference_allele,
            alternate_allele,
            variant_type,
            variant_class,
            coordinate_system,
            coordinate_system_status,
            normalization_status,
            normalization_status_source,
            sample_id,
            run_id,
            producer_pipeline,
            extraction_method,
            payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            declaration_id,
            "ar_src_001",
            "sid_variant_001",
            row_ref,
            "entities/normalization/stage_08_vdb_ready_variants.tsv",
            "vap_variant_id",
            variant,
            variant,
            "GRCh38",
            "entities/metadata/config_snapshot.yaml",
            "1",
            "895427",
            "895427",
            "895427",
            "G",
            "C",
            "SNV",
            "single_nucleotide_variant",
            "vcf_style",
            "inferred",
            "vdb_ready",
            "artifact_path",
            "HG002",
            "run_2026_06_03_010030",
            "variant_annotation_pipeline",
            "test_fixture",
            "{}",
        ),
    )


def _insert_feature_declaration(
    conn: sqlite3.Connection,
    declaration_id: str,
    *,
    feature_kind: str,
    feature_namespace: str,
    feature_value: str,
    relationship_type: str,
) -> None:
    conn.execute(
        """
        INSERT INTO source_feature_declarations (
            feature_declaration_id,
            assertion_registration_id,
            coordinate_declaration_id,
            source_identity_id,
            source_record_ref,
            source_artifact_path,
            variant_source_namespace,
            variant_source_value,
            feature_kind,
            feature_namespace,
            feature_value,
            feature_label,
            relationship_type,
            relationship_status,
            gene_id,
            gene_symbol,
            gene_mapping_status,
            transcript_id,
            consequence,
            impact,
            impact_class,
            functional_impact,
            variant_context,
            is_regulatory_candidate,
            is_splice_region_candidate,
            annotation_source,
            annotation_version,
            annotation_assembly,
            reference_genome_build,
            sample_id,
            run_id,
            producer_pipeline,
            extraction_method,
            payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            declaration_id,
            "ar_src_001",
            "coord_decl_001",
            "sid_variant_001",
            "row:1",
            "entities/normalization/stage_08_vdb_ready_variants.tsv",
            "vap_variant_id",
            "1:895427:G:C",
            feature_kind,
            feature_namespace,
            feature_value,
            feature_value,
            relationship_type,
            "declared",
            "",
            "",
            "",
            "",
            feature_value if feature_kind == "sequence_consequence" else "",
            "",
            "",
            "",
            feature_value if feature_kind == "variant_context" else "",
            "",
            "",
            "VEP",
            "source_configured",
            "GRCh38",
            "GRCh38",
            "HG002",
            "run_2026_06_03_010030",
            "variant_annotation_pipeline",
            "test_fixture",
            "{}",
        ),
    )


def test_assertion_records_preserve_coordinate_and_feature_declaration_sets_by_reference(tmp_path: Path) -> None:
    db_path = tmp_path / "vdb.sqlite"
    conn = _seed_base_registration_unit(db_path)
    _insert_source_identity(conn)
    _insert_coordinate_declaration(conn, "coord_decl_001", row_ref="row:1", variant="1:895427:G:C")
    _insert_coordinate_declaration(conn, "coord_decl_002", row_ref="row:2", variant="1:895428:A:T")
    _insert_feature_declaration(
        conn,
        "feature_decl_001",
        feature_kind="sequence_consequence",
        feature_namespace="vap_consequence",
        feature_value="intergenic_variant",
        relationship_type="has_consequence",
    )
    _insert_feature_declaration(
        conn,
        "feature_decl_002",
        feature_kind="sequence_consequence",
        feature_namespace="vap_consequence",
        feature_value="intron_variant",
        relationship_type="has_consequence",
    )
    _insert_feature_declaration(
        conn,
        "feature_decl_003",
        feature_kind="annotation_status",
        feature_namespace="vap_annotation_status",
        feature_value="intergenic_coordinate_surveillance",
        relationship_type="has_annotation_status",
    )
    conn.commit()
    conn.close()

    manifest = tmp_path / "manifest.tsv"
    _write_tsv(
        manifest,
        [
            {
                "registration_unit_id": "ru_vap_hg002",
                "producer_family": "VAP",
                "registration_unit_sqlite_path": str(db_path),
            }
        ],
        ["registration_unit_id", "producer_family", "registration_unit_sqlite_path"],
    )

    build_assertion_records(
        manifest_path=manifest,
        output_dir=tmp_path / "assertion_records",
        corpus_generation_id="test_corpus",
    )

    output_dir = tmp_path / "assertion_records"
    coordinate_rows = _read_tsv(output_dir / "assertion_record_coordinate_declaration_sets.tsv")
    feature_rows = _read_tsv(output_dir / "assertion_record_feature_declaration_sets.tsv")
    summary = json.loads((output_dir / "assertion_record_validation_report.json").read_text(encoding="utf-8"))

    assert len(coordinate_rows) == 1
    coordinate_row = coordinate_rows[0]
    assert coordinate_row["coordinate_declaration_set_id"].startswith("cds_")
    assert coordinate_row["coordinate_declaration_table_reference"] == "ru_vap_hg002:source_coordinate_declarations"
    assert coordinate_row["coordinate_declaration_count"] == "2"
    assert coordinate_row["lossiness_status"] == "lossless_by_reference"
    assert coordinate_row["coordinate_declaration_set_status"] == "resolved"
    assert "reference_genome_build=GRCh38" in coordinate_row["coordinate_declaration_filter"]
    assert "normalization_status=vdb_ready" in coordinate_row["coordinate_declaration_filter"]

    assert len(feature_rows) == 2
    counts_by_kind = {row["feature_kind"]: row["feature_declaration_count"] for row in feature_rows}
    assert counts_by_kind == {
        "annotation_status": "1",
        "sequence_consequence": "2",
    }
    assert {row["feature_declaration_table_reference"] for row in feature_rows} == {
        "ru_vap_hg002:source_feature_declarations"
    }
    assert {row["lossiness_status"] for row in feature_rows} == {"lossless_by_reference"}
    assert {row["feature_declaration_set_status"] for row in feature_rows} == {"resolved"}
    assert all("annotation_assembly=GRCh38" in row["feature_declaration_filter"] for row in feature_rows)

    assert summary["coordinate_declaration_set_count"] == 1
    assert summary["feature_declaration_set_count"] == 2


def test_assertion_records_emit_header_only_declaration_sets_when_not_applicable(tmp_path: Path) -> None:
    db_path = tmp_path / "gsc.sqlite"
    conn = _seed_base_registration_unit(db_path, producer_family="GSC")
    conn.commit()
    conn.close()

    manifest = tmp_path / "manifest.tsv"
    _write_tsv(
        manifest,
        [
            {
                "registration_unit_id": "ru_gsc_tay_sachs",
                "producer_family": "GSC",
                "registration_unit_sqlite_path": str(db_path),
            }
        ],
        ["registration_unit_id", "producer_family", "registration_unit_sqlite_path"],
    )

    build_assertion_records(
        manifest_path=manifest,
        output_dir=tmp_path / "assertion_records",
        corpus_generation_id="test_corpus",
    )

    output_dir = tmp_path / "assertion_records"
    coordinate_rows = _read_tsv(output_dir / "assertion_record_coordinate_declaration_sets.tsv")
    feature_rows = _read_tsv(output_dir / "assertion_record_feature_declaration_sets.tsv")
    summary = json.loads((output_dir / "assertion_record_validation_report.json").read_text(encoding="utf-8"))

    assert coordinate_rows == []
    assert feature_rows == []
    assert summary["coordinate_declaration_set_count"] == 0
    assert summary["feature_declaration_set_count"] == 0

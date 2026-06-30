import csv
import json
from pathlib import Path

from variant_database.phase4.corpus_generation.artifacts import (
    CORPUS_GENERATION_MANIFEST_COLUMNS,
    emit_corpus_generation_artifacts,
)
from variant_database.phase4.corpus_generation.manifest import (
    CANONICAL_SELECTION_MANIFEST_COLUMNS,
)
from variant_database.phase4.corpus_generation.validation import (
    validate_corpus_generation_artifact_set,
)


BUILD_TIMESTAMP = "2026-06-30T12:00:00Z"
VALIDATION_TIMESTAMP = "2026-06-30T12:05:00Z"


def _write_tsv(path: Path, columns: tuple[str, ...], rows: list[dict[str, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(columns),
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def _selection_row(
    *,
    label: str,
    producer: str,
    included: bool,
) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": "test_corpus_v1",
            "registration_unit_label": label,
            "registration_unit_reference": label,
            "registration_unit_path": f"results/registration/{label}",
            "registration_unit_sqlite_path": f"results/registration/{label}/vdb.sqlite",
            "expected_producer_family": producer,
            "expected_registration_unit_validation_status": "passed",
            "expected_registration_unit_certification_status": "certified",
            "expected_registration_unit_readiness_status": "ready",
            "expected_backend": "sqlite",
            "registration_unit_inventory_record_reference": "inventory.tsv",
            "registration_unit_readiness_record_reference": "readiness.tsv",
            "phase4_1_validation_receipt_reference": "phase4_1_receipt/",
            "notes": f"{label} fixture",
        }
    )
    if included:
        row["inclusion_status"] = "included"
        row["inclusion_rationale"] = "included fixture input"
    else:
        row["inclusion_status"] = ""
        row["inclusion_rationale"] = ""
        row["exclusion_status"] = "deferred"
        row["exclusion_rationale"] = "excluded from fixture corpus"
    return row


def _write_selection_manifest(tmp_path: Path) -> Path:
    rows = [
        _selection_row(label="gsc_fixture", producer="GSC", included=True),
        _selection_row(label="vap_fixture", producer="VAP", included=True),
        _selection_row(label="deferred_fixture", producer="VAP", included=False),
    ]
    return _write_tsv(
        tmp_path / "selection_manifest.tsv",
        CANONICAL_SELECTION_MANIFEST_COLUMNS,
        rows,
    )


def _write_policy(tmp_path: Path) -> Path:
    policy = {
        "selection_policy_id": "test_policy",
        "selection_policy_version": "v1",
        "selection_policy_description": "Fixture policy for Corpus Generation validation tests.",
        "corpus_generation_id": "test_corpus_v1",
        "corpus_generation_label": "Test Corpus v1",
        "corpus_generation_purpose": "fixture corpus generation validation",
        "corpus_generation_version": "v1",
        "required_registration_unit_validation_status": "passed",
        "required_registration_unit_certification_status": "certified",
        "required_registration_unit_readiness_status": "ready",
        "required_backend": "sqlite",
        "producer_families_in_scope": ["GSC", "VAP"],
        "expected_registration_unit_count": 2,
        "expected_producer_family_counts": {"GSC": 1, "VAP": 1},
        "expected_registration_unit_labels": ["gsc_fixture", "vap_fixture"],
        "phase4_1_validation_receipt_reference": "phase4_1_receipt/",
        "registration_unit_inventory_reference": "inventory.tsv",
        "registration_unit_readiness_reference": "readiness.tsv",
        "authority_boundary": {
            "declares_scope": True,
            "interprets_evidence": False,
            "creates_assertion_records": False,
            "derives_topology": False,
            "certifies_corpus_generation": False,
        },
    }
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_inventory(tmp_path: Path) -> Path:
    columns = (
        "inventory_schema_version",
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "validation_layer",
        "source_role",
        "registration_backend",
        "registration_unit_path_resolved",
        "sqlite_path_resolved",
        "expected_read_mode",
        "open_status",
        "query_only_status",
        "required_table_status",
        "integrity_check_status",
        "inspection_status",
        "schema_metadata_row_count",
        "tep_packages_row_count",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
    )
    rows = [
        {
            "inventory_schema_version": "phase4_registration_unit_inventory_v1",
            "registration_unit_id": "ru_gsc_fixture",
            "registration_unit_label": "gsc_fixture",
            "producer_family": "GSC",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": "results/registration/gsc_fixture",
            "sqlite_path_resolved": "results/registration/gsc_fixture/vdb.sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "9",
            "assertion_registrations_row_count": "6",
            "source_identities_row_count": "100",
        },
        {
            "inventory_schema_version": "phase4_registration_unit_inventory_v1",
            "registration_unit_id": "ru_vap_fixture",
            "registration_unit_label": "vap_fixture",
            "producer_family": "VAP",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": "results/registration/vap_fixture",
            "sqlite_path_resolved": "results/registration/vap_fixture/vdb.sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "16",
            "assertion_registrations_row_count": "10",
            "source_identities_row_count": "200",
        },
    ]
    return _write_tsv(tmp_path / "inventory.tsv", columns, rows)


def _write_readiness(tmp_path: Path) -> Path:
    columns = (
        "readiness_schema_version",
        "registration_unit_id",
        "registration_unit_label",
        "producer_family",
        "validation_layer",
        "source_role",
        "registration_backend",
        "expected_read_mode",
        "open_status",
        "query_only_status",
        "required_table_status",
        "integrity_check_status",
        "inspection_status",
        "schema_metadata_row_count",
        "tep_packages_row_count",
        "artifacts_row_count",
        "assertion_registrations_row_count",
        "source_identities_row_count",
        "readiness_status",
        "readiness_reasons",
    )
    rows = [
        {
            "readiness_schema_version": "phase4_registration_unit_readiness_v1",
            "registration_unit_id": "ru_gsc_fixture",
            "registration_unit_label": "gsc_fixture",
            "producer_family": "GSC",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "9",
            "assertion_registrations_row_count": "6",
            "source_identities_row_count": "100",
            "readiness_status": "ready",
            "readiness_reasons": "ready fixture",
        },
        {
            "readiness_schema_version": "phase4_registration_unit_readiness_v1",
            "registration_unit_id": "ru_vap_fixture",
            "registration_unit_label": "vap_fixture",
            "producer_family": "VAP",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "expected_read_mode": "read_only",
            "open_status": "passed",
            "query_only_status": "passed",
            "required_table_status": "passed",
            "integrity_check_status": "passed",
            "inspection_status": "passed",
            "schema_metadata_row_count": "1",
            "tep_packages_row_count": "1",
            "artifacts_row_count": "16",
            "assertion_registrations_row_count": "10",
            "source_identities_row_count": "200",
            "readiness_status": "ready",
            "readiness_reasons": "ready fixture",
        },
    ]
    return _write_tsv(tmp_path / "readiness.tsv", columns, rows)


def _build_fixture(tmp_path: Path) -> dict[str, Path]:
    selection_manifest = _write_selection_manifest(tmp_path)
    policy = _write_policy(tmp_path)
    inventory = _write_inventory(tmp_path)
    readiness = _write_readiness(tmp_path)

    output_dir = tmp_path / "test_corpus_v1"
    emit_corpus_generation_artifacts(
        selection_manifest,
        output_dir,
        corpus_generation_label="Test Corpus v1",
        corpus_generation_purpose="fixture corpus generation validation",
        corpus_generation_version="v1",
        selection_policy_id="test_policy",
        selection_policy_version="v1",
        selection_policy_description="Fixture policy for Corpus Generation validation tests.",
        registration_unit_inventory_path=inventory,
        registration_unit_readiness_path=readiness,
        repo_root=tmp_path,
        build_timestamp=BUILD_TIMESTAMP,
    )

    return {
        "selection_manifest": selection_manifest,
        "policy": policy,
        "inventory": inventory,
        "readiness": readiness,
        "output_dir": output_dir,
    }


def _validate_fixture(paths: dict[str, Path], tmp_path: Path):
    return validate_corpus_generation_artifact_set(
        paths["output_dir"],
        paths["selection_manifest"],
        paths["policy"],
        paths["inventory"],
        paths["readiness"],
        tmp_path / "validation",
        validation_timestamp=VALIDATION_TIMESTAMP,
    )


def test_validate_corpus_generation_artifact_set_passes_for_fixture(tmp_path: Path) -> None:
    paths = _build_fixture(tmp_path)

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_status == "passed"
    assert all(check.status == "passed" for check in result.checks)


def test_validate_corpus_generation_artifact_set_emits_receipts(tmp_path: Path) -> None:
    paths = _build_fixture(tmp_path)

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_report_json_path.is_file()
    assert result.validation_report_tsv_path.is_file()
    assert result.validation_summary_json_path.is_file()
    assert result.validation_summary_tsv_path.is_file()


def test_validate_corpus_generation_artifact_set_detects_missing_required_artifact(
    tmp_path: Path,
) -> None:
    paths = _build_fixture(tmp_path)
    (
        paths["output_dir"] / "downstream_assertion_record_input_manifest.tsv"
    ).unlink()

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_status == "failed"
    assert any(
        check.check_id == "artifact_presence__downstream_assertion_record_input_manifest_tsv"
        and check.status == "failed"
        for check in result.checks
    )


def test_validate_corpus_generation_artifact_set_detects_downstream_excluded_leakage(
    tmp_path: Path,
) -> None:
    paths = _build_fixture(tmp_path)
    corpus_manifest = paths["output_dir"] / "corpus_generation_manifest.tsv"
    downstream_manifest = (
        paths["output_dir"] / "downstream_assertion_record_input_manifest.tsv"
    )

    with corpus_manifest.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    excluded = next(row for row in rows if row["registration_unit_label"] == "deferred_fixture")

    with downstream_manifest.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "corpus_generation_id",
                "registration_unit_id",
                "registration_unit_label",
                "registration_unit_reference",
                "registration_unit_path",
                "registration_unit_sqlite_path",
                "registration_unit_inventory_record_reference",
                "registration_unit_readiness_record_reference",
                "phase4_1_validation_receipt_reference",
                "producer_family",
                "source_package_id",
                "registration_backend",
                "assertion_registration_count",
                "source_identity_count",
                "registration_unit_validation_status",
                "registration_unit_certification_status",
                "registration_unit_readiness_status",
                "inclusion_status",
                "inclusion_rationale",
            ],
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writerow(excluded)

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_status == "failed"
    assert any(
        check.check_id == "downstream_included_only" and check.status == "failed"
        for check in result.checks
    )


def test_validate_corpus_generation_artifact_set_detects_self_certification(
    tmp_path: Path,
) -> None:
    paths = _build_fixture(tmp_path)
    corpus_manifest = paths["output_dir"] / "corpus_generation_manifest.tsv"

    with corpus_manifest.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    for row in rows:
        row["corpus_generation_certification_status"] = "certified"

    _write_tsv(corpus_manifest, CORPUS_GENERATION_MANIFEST_COLUMNS, rows)

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_status == "failed"
    assert any(
        check.check_id == "anti_self_certification_tsv" and check.status == "failed"
        for check in result.checks
    )


def test_validate_corpus_generation_artifact_set_detects_receipt_enrichment_mismatch(
    tmp_path: Path,
) -> None:
    paths = _build_fixture(tmp_path)
    corpus_manifest = paths["output_dir"] / "corpus_generation_manifest.tsv"

    with corpus_manifest.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    rows[0]["artifact_count"] = "999"
    _write_tsv(corpus_manifest, CORPUS_GENERATION_MANIFEST_COLUMNS, rows)

    result = _validate_fixture(paths, tmp_path)

    assert result.validation_status == "failed"
    assert any(
        check.check_id == "receipt_enrichment__gsc_fixture__artifact_count"
        and check.status == "failed"
        for check in result.checks
    )

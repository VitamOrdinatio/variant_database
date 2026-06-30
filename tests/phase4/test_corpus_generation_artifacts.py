import csv
import hashlib
import json
from pathlib import Path

import pytest

from variant_database.phase4.corpus_generation.artifacts import (
    CORPUS_GENERATION_MANIFEST_COLUMNS,
    DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS,
    CorpusGenerationArtifactError,
    emit_corpus_generation_artifacts,
)
from variant_database.phase4.corpus_generation.manifest import (
    CANONICAL_SELECTION_MANIFEST_COLUMNS,
)


FIXED_TIMESTAMP = "2026-06-30T12:00:00Z"


def _included_row(
    *,
    label: str = "gsc_epilepsy",
    producer_family: str = "GSC",
    registration_unit_path: str = "results/registration/mark_phase3_canonical/gsc_epilepsy",
    sqlite_path: str = "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite",
) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": "mark_phase4_corpus_6tep_v1",
            "registration_unit_label": label,
            "registration_unit_reference": label,
            "registration_unit_path": registration_unit_path,
            "registration_unit_sqlite_path": sqlite_path,
            "expected_producer_family": producer_family,
            "expected_registration_unit_validation_status": "passed",
            "expected_registration_unit_certification_status": "certified",
            "expected_registration_unit_readiness_status": "ready",
            "expected_backend": "sqlite",
            "registration_unit_inventory_record_reference": (
                "results/validation/phase4_registration_units/"
                "registration_unit_inventory.tsv"
            ),
            "registration_unit_readiness_record_reference": (
                "results/validation/phase4_registration_units/"
                "registration_unit_readiness.tsv"
            ),
            "phase4_1_validation_receipt_reference": (
                "results/validation/phase4_registration_units/"
                "mark_full_corpus_smoketest_2026_06_30_052739/"
            ),
            "inclusion_status": "included",
            "inclusion_rationale": "certified Phase 3 benchmark input",
            "notes": "included fixture row",
        }
    )
    return row


def _excluded_row() -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": "mark_phase4_corpus_6tep_v1",
            "registration_unit_label": "vap_deferred_ERR00000000",
            "registration_unit_reference": "vap_deferred_ERR00000000",
            "expected_backend": "sqlite",
            "exclusion_status": "deferred",
            "exclusion_rationale": "reserved for expanded corpus",
            "notes": "excluded fixture row",
        }
    )
    return row


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


def _write_selection_manifest(tmp_path: Path) -> Path:
    rows = [
        _included_row(label="gsc_epilepsy", producer_family="GSC"),
        _included_row(
            label="vap_hg002",
            producer_family="VAP",
            registration_unit_path="results/registration/mark_phase3_canonical/vap_hg002",
            sqlite_path="results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite",
        ),
        _excluded_row(),
    ]
    return _write_tsv(
        tmp_path / "corpus_generation_selection_manifest.tsv",
        CANONICAL_SELECTION_MANIFEST_COLUMNS,
        rows,
    )


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
            "registration_unit_id": "ru_gsc_epilepsy",
            "registration_unit_label": "gsc_epilepsy",
            "producer_family": "GSC",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": str(
                tmp_path / "results/registration/mark_phase3_canonical/gsc_epilepsy"
            ),
            "sqlite_path_resolved": str(
                tmp_path
                / "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite"
            ),
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
            "source_identities_row_count": "89138",
        },
        {
            "inventory_schema_version": "phase4_registration_unit_inventory_v1",
            "registration_unit_id": "ru_vap_hg002",
            "registration_unit_label": "vap_hg002",
            "producer_family": "VAP",
            "validation_layer": "phase4_1",
            "source_role": "registration_unit",
            "registration_backend": "sqlite",
            "registration_unit_path_resolved": str(
                tmp_path / "results/registration/mark_phase3_canonical/vap_hg002"
            ),
            "sqlite_path_resolved": str(
                tmp_path
                / "results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite"
            ),
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
            "source_identities_row_count": "97369849",
        },
    ]
    return _write_tsv(
        tmp_path / "registration_unit_inventory.tsv",
        columns,
        rows,
    )


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
            "registration_unit_id": "ru_gsc_epilepsy",
            "registration_unit_label": "gsc_epilepsy",
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
            "source_identities_row_count": "89138",
            "readiness_status": "ready",
            "readiness_reasons": "ready for corpus generation",
        },
        {
            "readiness_schema_version": "phase4_registration_unit_readiness_v1",
            "registration_unit_id": "ru_vap_hg002",
            "registration_unit_label": "vap_hg002",
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
            "source_identities_row_count": "97369849",
            "readiness_status": "ready",
            "readiness_reasons": "ready for corpus generation",
        },
    ]
    return _write_tsv(
        tmp_path / "registration_unit_readiness.tsv",
        columns,
        rows,
    )


def _emit(tmp_path: Path, output_dir: Path | None = None):
    selection_manifest = _write_selection_manifest(tmp_path)
    inventory = _write_inventory(tmp_path)
    readiness = _write_readiness(tmp_path)

    return emit_corpus_generation_artifacts(
        selection_manifest,
        output_dir or (tmp_path / "corpus_generation_output"),
        corpus_generation_label="MARK Phase 4 6-TEP Benchmark Corpus v1",
        corpus_generation_purpose="initial certified multi-producer Phase 4 benchmark corpus",
        selection_policy_id="mark_phase4_6tep_certified_input_policy",
        selection_policy_version="v1",
        selection_policy_description=(
            "Select certified Phase 3 Registration Units for initial "
            "Phase 4 benchmark derivation."
        ),
        registration_unit_inventory_path=inventory,
        registration_unit_readiness_path=readiness,
        repo_root=tmp_path,
        build_timestamp=FIXED_TIMESTAMP,
    )


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_emit_corpus_generation_artifacts_writes_expected_files(tmp_path: Path) -> None:
    artifacts = _emit(tmp_path)

    assert artifacts.copied_selection_manifest_path.is_file()
    assert artifacts.corpus_generation_manifest_tsv_path.is_file()
    assert artifacts.corpus_generation_manifest_json_path.is_file()
    assert artifacts.corpus_generation_report_path.is_file()
    assert artifacts.downstream_assertion_record_input_manifest_path.is_file()


def test_emit_corpus_generation_artifacts_copies_selection_manifest(
    tmp_path: Path,
) -> None:
    selection_manifest = _write_selection_manifest(tmp_path)
    inventory = _write_inventory(tmp_path)
    readiness = _write_readiness(tmp_path)

    artifacts = emit_corpus_generation_artifacts(
        selection_manifest,
        tmp_path / "output",
        corpus_generation_label="MARK Phase 4 6-TEP Benchmark Corpus v1",
        corpus_generation_purpose="initial certified multi-producer Phase 4 benchmark corpus",
        selection_policy_id="mark_phase4_6tep_certified_input_policy",
        selection_policy_version="v1",
        selection_policy_description="Select certified Phase 3 Registration Units.",
        registration_unit_inventory_path=inventory,
        registration_unit_readiness_path=readiness,
        repo_root=tmp_path,
        build_timestamp=FIXED_TIMESTAMP,
    )

    assert artifacts.copied_selection_manifest_path.read_text(
        encoding="utf-8"
    ) == selection_manifest.read_text(encoding="utf-8")


def test_emit_corpus_generation_artifacts_records_selection_manifest_sha256(
    tmp_path: Path,
) -> None:
    selection_manifest = _write_selection_manifest(tmp_path)
    inventory = _write_inventory(tmp_path)
    readiness = _write_readiness(tmp_path)

    artifacts = emit_corpus_generation_artifacts(
        selection_manifest,
        tmp_path / "output",
        corpus_generation_label="MARK Phase 4 6-TEP Benchmark Corpus v1",
        corpus_generation_purpose="initial certified multi-producer Phase 4 benchmark corpus",
        selection_policy_id="mark_phase4_6tep_certified_input_policy",
        selection_policy_version="v1",
        selection_policy_description="Select certified Phase 3 Registration Units.",
        registration_unit_inventory_path=inventory,
        registration_unit_readiness_path=readiness,
        repo_root=tmp_path,
        build_timestamp=FIXED_TIMESTAMP,
    )
    payload = json.loads(
        artifacts.corpus_generation_manifest_json_path.read_text(encoding="utf-8")
    )
    expected_sha = hashlib.sha256(selection_manifest.read_bytes()).hexdigest()

    assert payload["selection_manifest"]["sha256"] == expected_sha


def test_corpus_generation_manifest_contains_included_and_excluded_rows(
    tmp_path: Path,
) -> None:
    artifacts = _emit(tmp_path)

    rows = _read_tsv(artifacts.corpus_generation_manifest_tsv_path)

    assert [row["registration_unit_label"] for row in rows] == [
        "gsc_epilepsy",
        "vap_hg002",
        "vap_deferred_ERR00000000",
    ]
    assert [row["membership_record_type"] for row in rows] == [
        "included_registration_unit",
        "included_registration_unit",
        "excluded_registration_unit",
    ]


def test_downstream_manifest_contains_only_included_rows(tmp_path: Path) -> None:
    artifacts = _emit(tmp_path)

    rows = _read_tsv(artifacts.downstream_assertion_record_input_manifest_path)

    assert [row["registration_unit_label"] for row in rows] == [
        "gsc_epilepsy",
        "vap_hg002",
    ]


def test_emit_corpus_generation_artifacts_enriches_from_phase4_1_receipts(
    tmp_path: Path,
) -> None:
    artifacts = _emit(tmp_path)

    rows = _read_tsv(artifacts.corpus_generation_manifest_tsv_path)
    by_label = {row["registration_unit_label"]: row for row in rows}

    assert by_label["gsc_epilepsy"]["registration_unit_id"] == "ru_gsc_epilepsy"
    assert by_label["gsc_epilepsy"]["producer_family"] == "GSC"
    assert by_label["gsc_epilepsy"]["artifact_count"] == "9"
    assert by_label["gsc_epilepsy"]["assertion_registration_count"] == "6"
    assert by_label["gsc_epilepsy"]["source_identity_count"] == "89138"
    assert by_label["gsc_epilepsy"]["registration_unit_readiness_status"] == "ready"


def test_emit_corpus_generation_artifacts_does_not_self_certify(
    tmp_path: Path,
) -> None:
    artifacts = _emit(tmp_path)

    rows = _read_tsv(artifacts.corpus_generation_manifest_tsv_path)

    assert {row["corpus_generation_validation_status"] for row in rows} == {
        "not_evaluated"
    }
    assert {row["corpus_generation_certification_status"] for row in rows} == {
        "not_available"
    }


def test_emit_corpus_generation_artifacts_records_selection_policy(
    tmp_path: Path,
) -> None:
    artifacts = _emit(tmp_path)

    payload = json.loads(
        artifacts.corpus_generation_manifest_json_path.read_text(encoding="utf-8")
    )

    assert (
        payload["selection_policy"]["selection_policy_id"]
        == "mark_phase4_6tep_certified_input_policy"
    )
    assert payload["selection_policy"]["selection_policy_version"] == "v1"


def test_emit_corpus_generation_artifacts_is_deterministic_with_fixed_timestamp(
    tmp_path: Path,
) -> None:
    first = _emit(tmp_path, tmp_path / "first")
    second = _emit(tmp_path, tmp_path / "second")

    assert first.corpus_generation_manifest_tsv_path.read_text(
        encoding="utf-8"
    ) == second.corpus_generation_manifest_tsv_path.read_text(encoding="utf-8")

    first_payload = json.loads(
        first.corpus_generation_manifest_json_path.read_text(encoding="utf-8")
    )
    second_payload = json.loads(
        second.corpus_generation_manifest_json_path.read_text(encoding="utf-8")
    )

    # Output paths are expected to differ; compare deterministic semantic payload.
    first_payload["artifacts"] = {}
    second_payload["artifacts"] = {}
    first_payload["selection_manifest"]["copied_path"] = ""
    second_payload["selection_manifest"]["copied_path"] = ""

    assert first_payload == second_payload


def test_emit_corpus_generation_artifacts_requires_inventory_rows_when_supplied(
    tmp_path: Path,
) -> None:
    selection_manifest = _write_selection_manifest(tmp_path)
    readiness = _write_readiness(tmp_path)
    inventory = _write_tsv(
        tmp_path / "registration_unit_inventory.tsv",
        (
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
        ),
        [],
    )

    with pytest.raises(CorpusGenerationArtifactError, match="not found"):
        emit_corpus_generation_artifacts(
            selection_manifest,
            tmp_path / "output",
            corpus_generation_label="MARK Phase 4 6-TEP Benchmark Corpus v1",
            corpus_generation_purpose="initial certified multi-producer Phase 4 benchmark corpus",
            selection_policy_id="mark_phase4_6tep_certified_input_policy",
            selection_policy_version="v1",
            selection_policy_description="Select certified Phase 3 Registration Units.",
            registration_unit_inventory_path=inventory,
            registration_unit_readiness_path=readiness,
            repo_root=tmp_path,
            build_timestamp=FIXED_TIMESTAMP,
        )


def test_emit_corpus_generation_artifacts_rejects_mismatched_expected_producer_family(
    tmp_path: Path,
) -> None:
    selection_manifest = _write_selection_manifest(tmp_path)
    inventory = _write_inventory(tmp_path)
    readiness = _write_readiness(tmp_path)

    text = selection_manifest.read_text(encoding="utf-8")
    text = text.replace("\tgsc_epilepsy\t", "\tgsc_epilepsy\t", 1)
    text = text.replace("\tGSC\tpassed\tcertified\tready\t", "\tVAP\tpassed\tcertified\tready\t", 1)
    selection_manifest.write_text(text, encoding="utf-8")

    with pytest.raises(CorpusGenerationArtifactError, match="expected producer"):
        emit_corpus_generation_artifacts(
            selection_manifest,
            tmp_path / "output",
            corpus_generation_label="MARK Phase 4 6-TEP Benchmark Corpus v1",
            corpus_generation_purpose="initial certified multi-producer Phase 4 benchmark corpus",
            selection_policy_id="mark_phase4_6tep_certified_input_policy",
            selection_policy_version="v1",
            selection_policy_description="Select certified Phase 3 Registration Units.",
            registration_unit_inventory_path=inventory,
            registration_unit_readiness_path=readiness,
            repo_root=tmp_path,
            build_timestamp=FIXED_TIMESTAMP,
        )


def test_corpus_generation_manifest_uses_canonical_columns(tmp_path: Path) -> None:
    artifacts = _emit(tmp_path)

    with artifacts.corpus_generation_manifest_tsv_path.open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)

    assert tuple(header) == CORPUS_GENERATION_MANIFEST_COLUMNS


def test_downstream_manifest_uses_canonical_columns(tmp_path: Path) -> None:
    artifacts = _emit(tmp_path)

    with artifacts.downstream_assertion_record_input_manifest_path.open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)

    assert tuple(header) == DOWNSTREAM_ASSERTION_RECORD_INPUT_COLUMNS


def test_emit_corpus_generation_artifacts_report_preserves_boundary(
    tmp_path: Path,
) -> None:
    artifacts = _emit(tmp_path)

    report = artifacts.corpus_generation_report_path.read_text(encoding="utf-8")

    assert "It is not source truth." in report
    assert "It is not a validation receipt." in report
    assert "It does not certify the Corpus Generation." in report
    assert "It does not create Assertion Records" in report

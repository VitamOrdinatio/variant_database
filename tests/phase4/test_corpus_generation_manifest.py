import csv
from pathlib import Path

import pytest

from variant_database.phase4.corpus_generation.manifest import (
    CANONICAL_SELECTION_MANIFEST_COLUMNS,
    CorpusGenerationManifestError,
    load_corpus_generation_selection_manifest,
)


def _included_row(
    *,
    corpus_generation_id: str = "mark_phase4_corpus_6tep_v1",
    label: str = "gsc_epilepsy",
    registration_unit_path: str = "results/registration/mark_phase3_canonical/gsc_epilepsy",
    sqlite_path: str = "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite",
) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": corpus_generation_id,
            "registration_unit_label": label,
            "registration_unit_reference": label,
            "registration_unit_path": registration_unit_path,
            "registration_unit_sqlite_path": sqlite_path,
            "expected_producer_family": "GSC" if label.startswith("gsc_") else "VAP",
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
            "notes": "test row",
        }
    )
    return row


def _excluded_row(
    *,
    corpus_generation_id: str = "mark_phase4_corpus_6tep_v1",
    label: str = "vap_deferred_ERR00000000",
) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_SELECTION_MANIFEST_COLUMNS}
    row.update(
        {
            "corpus_generation_id": corpus_generation_id,
            "registration_unit_label": label,
            "registration_unit_reference": label,
            "expected_backend": "sqlite",
            "exclusion_status": "deferred",
            "exclusion_rationale": "reserved for expanded corpus",
            "notes": "deferred candidate",
        }
    )
    return row


def _write_manifest(
    tmp_path: Path,
    rows: list[dict[str, str]],
    *,
    columns: tuple[str, ...] | list[str] = CANONICAL_SELECTION_MANIFEST_COLUMNS,
    filename: str = "corpus_generation_selection_manifest.tsv",
) -> Path:
    path = tmp_path / filename
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(columns),
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def test_load_selection_manifest_requires_existing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.tsv"

    with pytest.raises(CorpusGenerationManifestError, match="does not exist"):
        load_corpus_generation_selection_manifest(missing)


def test_load_selection_manifest_requires_tsv_suffix(tmp_path: Path) -> None:
    path = tmp_path / "manifest.csv"
    path.write_text("corpus_generation_id\n", encoding="utf-8")

    with pytest.raises(CorpusGenerationManifestError, match="must be a .tsv"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_requires_required_columns(tmp_path: Path) -> None:
    columns = tuple(
        column
        for column in CANONICAL_SELECTION_MANIFEST_COLUMNS
        if column != "corpus_generation_id"
    )
    path = _write_manifest(tmp_path, [_included_row()], columns=columns)

    with pytest.raises(CorpusGenerationManifestError, match="missing required columns"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_rejects_unknown_columns(tmp_path: Path) -> None:
    columns = tuple(CANONICAL_SELECTION_MANIFEST_COLUMNS) + ("ambient_scope",)
    row = _included_row()
    row["ambient_scope"] = "not_allowed"
    path = _write_manifest(tmp_path, [row], columns=columns)

    with pytest.raises(CorpusGenerationManifestError, match="unknown columns"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_rejects_empty_manifest(tmp_path: Path) -> None:
    path = _write_manifest(tmp_path, [])

    with pytest.raises(CorpusGenerationManifestError, match="contains no records"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_requires_single_corpus_generation_id(
    tmp_path: Path,
) -> None:
    first = _included_row(corpus_generation_id="corpus_a", label="gsc_epilepsy")
    second = _included_row(
        corpus_generation_id="corpus_b",
        label="vap_hg002",
        registration_unit_path="results/registration/mark_phase3_canonical/vap_hg002",
        sqlite_path="results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite",
    )
    path = _write_manifest(tmp_path, [first, second])

    with pytest.raises(CorpusGenerationManifestError, match="exactly one"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_preserves_row_order(tmp_path: Path) -> None:
    rows = [
        _included_row(label="gsc_epilepsy"),
        _included_row(
            label="gsc_mitochondrial_disease",
            registration_unit_path=(
                "results/registration/mark_phase3_canonical/"
                "gsc_mitochondrial_disease"
            ),
            sqlite_path=(
                "results/registration/mark_phase3_canonical/"
                "gsc_mitochondrial_disease/vdb.sqlite"
            ),
        ),
        _included_row(
            label="vap_hg002",
            registration_unit_path="results/registration/mark_phase3_canonical/vap_hg002",
            sqlite_path="results/registration/mark_phase3_canonical/vap_hg002/vdb.sqlite",
        ),
    ]
    path = _write_manifest(tmp_path, rows)

    manifest = load_corpus_generation_selection_manifest(path, repo_root=tmp_path)

    assert [record.registration_unit_label for record in manifest.records] == [
        "gsc_epilepsy",
        "gsc_mitochondrial_disease",
        "vap_hg002",
    ]


def test_load_selection_manifest_resolves_paths_relative_to_repo_root(
    tmp_path: Path,
) -> None:
    row = _included_row(
        registration_unit_path="results/registration/mark_phase3_canonical/gsc_epilepsy",
        sqlite_path="results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite",
    )
    path = _write_manifest(tmp_path, [row])

    manifest = load_corpus_generation_selection_manifest(path, repo_root=tmp_path)

    record = manifest.records[0]
    assert record.registration_unit_path_resolved == (
        tmp_path / "results/registration/mark_phase3_canonical/gsc_epilepsy"
    ).resolve(strict=False)
    assert record.registration_unit_sqlite_path_resolved == (
        tmp_path / "results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite"
    ).resolve(strict=False)


def test_validate_filesystem_false_does_not_require_paths_to_exist(
    tmp_path: Path,
) -> None:
    row = _included_row(
        registration_unit_path="does/not/exist",
        sqlite_path="does/not/exist/vdb.sqlite",
    )
    path = _write_manifest(tmp_path, [row])

    manifest = load_corpus_generation_selection_manifest(
        path,
        repo_root=tmp_path,
        validate_filesystem=False,
    )

    assert manifest.corpus_generation_id == "mark_phase4_corpus_6tep_v1"


def test_validate_filesystem_true_requires_directory_and_sqlite_file(
    tmp_path: Path,
) -> None:
    row = _included_row(
        registration_unit_path="results/registration/mark_phase3_canonical/gsc_epilepsy",
        sqlite_path="results/registration/mark_phase3_canonical/gsc_epilepsy/vdb.sqlite",
    )
    path = _write_manifest(tmp_path, [row])

    with pytest.raises(CorpusGenerationManifestError, match="not a directory"):
        load_corpus_generation_selection_manifest(
            path,
            repo_root=tmp_path,
            validate_filesystem=True,
        )

    unit_dir = tmp_path / "results/registration/mark_phase3_canonical/gsc_epilepsy"
    unit_dir.mkdir(parents=True)

    with pytest.raises(CorpusGenerationManifestError, match="not a file"):
        load_corpus_generation_selection_manifest(
            path,
            repo_root=tmp_path,
            validate_filesystem=True,
        )

    sqlite_path = unit_dir / "vdb.sqlite"
    sqlite_path.write_text("", encoding="utf-8")

    manifest = load_corpus_generation_selection_manifest(
        path,
        repo_root=tmp_path,
        validate_filesystem=True,
    )

    assert len(manifest.included_records) == 1


def test_load_selection_manifest_rejects_duplicate_included_labels(
    tmp_path: Path,
) -> None:
    first = _included_row(label="gsc_epilepsy")
    second = _included_row(
        label="gsc_epilepsy",
        registration_unit_path="results/registration/mark_phase3_canonical/other",
        sqlite_path="results/registration/mark_phase3_canonical/other/vdb.sqlite",
    )
    path = _write_manifest(tmp_path, [first, second])

    with pytest.raises(CorpusGenerationManifestError, match="Duplicate included"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_rejects_duplicate_included_sqlite_paths(
    tmp_path: Path,
) -> None:
    first = _included_row(label="gsc_epilepsy")
    second = _included_row(label="gsc_mitochondrial_disease")
    second["registration_unit_sqlite_path"] = first["registration_unit_sqlite_path"]
    path = _write_manifest(tmp_path, [first, second])

    with pytest.raises(CorpusGenerationManifestError, match="Duplicate included"):
        load_corpus_generation_selection_manifest(path, repo_root=tmp_path)


def test_load_selection_manifest_requires_inclusion_rationale_for_included_rows(
    tmp_path: Path,
) -> None:
    row = _included_row()
    row["inclusion_rationale"] = ""
    path = _write_manifest(tmp_path, [row])

    with pytest.raises(CorpusGenerationManifestError, match="inclusion_rationale"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_supports_excluded_candidate_rows(
    tmp_path: Path,
) -> None:
    path = _write_manifest(tmp_path, [_included_row(), _excluded_row()])

    manifest = load_corpus_generation_selection_manifest(path)

    assert len(manifest.records) == 2
    assert len(manifest.included_records) == 1
    assert len(manifest.excluded_records) == 1
    assert manifest.excluded_records[0].exclusion_status == "deferred"


def test_load_selection_manifest_rejects_rows_with_both_inclusion_and_exclusion_status(
    tmp_path: Path,
) -> None:
    row = _included_row()
    row["exclusion_status"] = "deferred"
    row["exclusion_rationale"] = "reserved for expanded corpus"
    path = _write_manifest(tmp_path, [row])

    with pytest.raises(CorpusGenerationManifestError, match="exactly one"):
        load_corpus_generation_selection_manifest(path)


def test_load_selection_manifest_rejects_rows_with_no_disposition(
    tmp_path: Path,
) -> None:
    row = _included_row()
    row["inclusion_status"] = ""
    row["inclusion_rationale"] = ""
    path = _write_manifest(tmp_path, [row])

    with pytest.raises(CorpusGenerationManifestError, match="exactly one"):
        load_corpus_generation_selection_manifest(path)

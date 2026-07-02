from __future__ import annotations

import csv
import importlib.util
import json
import tarfile
from pathlib import Path
from types import ModuleType


SCRIPT = Path("scripts/mark/run_phase4_3_mark_full_corpus_assertion_record_smoketest.py")


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("phase4_3e_mark_script", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _valid_tables() -> dict[str, list[dict[str, str]]]:
    resolver_statuses = ["supported"] * 26 + ["indexed_with_note"] * 14 + ["deferred"] * 12
    source_obligations = ["required"] * 34 + ["optional"] * 16 + ["not_applicable"] * 2
    index_rows = []
    for i in range(52):
        producer_family = "GSC" if i >= 50 else "VAP"
        assertion_type = "producer_contract_validation" if i >= 50 else f"assertion_type_{i}"
        index_rows.append(
            {
                "assertion_id": f"assertion_{i:03d}",
                "producer_family": producer_family,
                "assertion_type": assertion_type,
                "preservation_status": "preserved",
                "resolver_status": resolver_statuses[i],
                "validation_status": resolver_statuses[i],
                "source_identity_set_status": source_obligations[i],
            }
        )

    set_rows = []
    summary_rows = []
    participant_rows = []
    for i in range(204):
        sid = f"source_identity_set_{i:03d}"
        assertion_id = f"assertion_{i % 50:03d}"
        set_row = {
            "source_identity_set_id": sid,
            "assertion_id": assertion_id,
            "source_assertion_registration_id": f"source_assertion_{i % 50:03d}",
            "identity_kind": "gene",
            "participant_role": "gene",
            "source_namespace": "test_namespace",
            "source_identity_count": "7",
            "source_identity_filter": "assertion_registration_id=x;identity_kind=gene;participant_role=gene;source_namespace=test_namespace",
            "source_identity_set_status": "resolved",
        }
        set_rows.append(set_row)
        summary_rows.append(
            {
                "source_identity_set_id": sid,
                "assertion_id": assertion_id,
                "source_assertion_registration_id": f"source_assertion_{i % 50:03d}",
                "registration_unit_id": "test_ru",
                "identity_kind": "gene",
                "participant_role": "gene",
                "source_namespace": "test_namespace",
                "source_identity_count": "7",
            }
        )
        participant_rows.append(
            {
                "assertion_id": assertion_id,
                "source_assertion_registration_id": f"source_assertion_{i % 50:03d}",
                "participant_role": "gene",
                "participant_value": f"source_identity_set:{sid}",
                "participant_source": "source_identity_set_reference",
                "source_identity_set_id": sid,
                "participant_identity_kind": "gene",
                "participant_source_namespace": "test_namespace",
                "participant_count": "7",
                "participant_resolution_status": "role_bearing_source_identity_set",
            }
        )

    lineage_rows = [
        {
            "assertion_id": f"assertion_{i:03d}",
            "source_artifact_relative_path": f"artifact_{i}.tsv",
            "source_artifact_sha256": "a" * 64,
            "source_artifact_size_bytes": "123",
            "source_record_ref": "",
            "source_record_ref_status": "explicit_absence",
            "lineage_completeness_status": "artifact_level_lineage_present_row_ref_absent",
        }
        for i in range(52)
    ]

    return {
        "assertion_record_index.tsv": index_rows,
        "assertion_record_participants.tsv": participant_rows,
        "assertion_record_source_identity_sets.tsv": set_rows,
        "assertion_record_source_identity_summary.tsv": summary_rows,
        "assertion_record_validation_report.tsv": [],
        "assertion_record_lineage.tsv": lineage_rows,
        "downstream_topology_input_manifest.tsv": [],
    }


def test_load_output_tables_includes_participants_and_lineage(tmp_path: Path) -> None:
    module = _load_script()
    _write_tsv(tmp_path / "assertion_record_index.tsv", [{"assertion_id": "a"}], ["assertion_id"])
    _write_tsv(tmp_path / "assertion_record_participants.tsv", [{"assertion_id": "a"}], ["assertion_id"])
    _write_tsv(tmp_path / "assertion_record_source_identity_sets.tsv", [{"source_identity_set_id": "s"}], ["source_identity_set_id"])
    _write_tsv(tmp_path / "assertion_record_source_identity_summary.tsv", [{"source_identity_set_id": "s"}], ["source_identity_set_id"])
    _write_tsv(tmp_path / "assertion_record_validation_report.tsv", [{"status": "passed"}], ["status"])
    _write_tsv(tmp_path / "assertion_record_lineage.tsv", [{"assertion_id": "a"}], ["assertion_id"])
    _write_tsv(tmp_path / "downstream_topology_input_manifest.tsv", [{"assertion_id": "a"}], ["assertion_id"])

    tables = module.load_output_tables(tmp_path)

    assert "assertion_record_participants.tsv" in tables
    assert "assertion_record_lineage.tsv" in tables
    assert tables["assertion_record_participants.tsv"] == [{"assertion_id": "a"}]
    assert tables["assertion_record_lineage.tsv"] == [{"assertion_id": "a"}]


def test_preservation_hardening_accepts_post_hardened_mark_tables() -> None:
    module = _load_script()
    rows = module.validate_preservation_hardening(_valid_tables())

    assert {row["status"] for row in rows} == {"passed"}
    assert {row["check_name"] for row in rows} == {
        "participant_bridge_populated_from_source_identity_sets",
        "source_identity_set_id_join_integrity",
        "preservation_and_resolver_status_are_explicit",
        "artifact_level_lineage_is_explicit",
        "source_identity_obligation_status_is_explicit",
    }


def test_preservation_hardening_fails_header_only_participants_when_source_identity_sets_exist() -> None:
    module = _load_script()
    tables = _valid_tables()
    tables["assertion_record_participants.tsv"] = []

    rows = module.validate_preservation_hardening(tables)
    statuses = {row["check_name"]: row["status"] for row in rows}

    assert statuses["participant_bridge_populated_from_source_identity_sets"] == "failed"
    assert statuses["source_identity_set_id_join_integrity"] == "failed"


def test_preservation_hardening_fails_orphan_participant_source_identity_set_ids() -> None:
    module = _load_script()
    tables = _valid_tables()
    tables["assertion_record_participants.tsv"][0] = {
        **tables["assertion_record_participants.tsv"][0],
        "source_identity_set_id": "orphan_source_identity_set",
    }

    rows = module.validate_preservation_hardening(tables)
    statuses = {row["check_name"]: row["status"] for row in rows}

    assert statuses["source_identity_set_id_join_integrity"] == "failed"


def test_preservation_hardening_fails_missing_lineage_status_fields() -> None:
    module = _load_script()
    tables = _valid_tables()
    tables["assertion_record_lineage.tsv"][0] = {
        key: value
        for key, value in tables["assertion_record_lineage.tsv"][0].items()
        if key != "lineage_completeness_status"
    }

    rows = module.validate_preservation_hardening(tables)
    statuses = {row["check_name"]: row["status"] for row in rows}

    assert statuses["artifact_level_lineage_is_explicit"] == "failed"


def test_preservation_hardening_fails_ambiguous_preservation_status() -> None:
    module = _load_script()
    tables = _valid_tables()
    tables["assertion_record_index.tsv"][0] = {
        **tables["assertion_record_index.tsv"][0],
        "preservation_status": "deferred",
    }

    rows = module.validate_preservation_hardening(tables)
    statuses = {row["check_name"]: row["status"] for row in rows}

    assert statuses["preservation_and_resolver_status_are_explicit"] == "failed"


def test_preservation_hardening_requires_explicit_source_identity_obligation_status() -> None:
    module = _load_script()
    tables = _valid_tables()
    tables["assertion_record_index.tsv"][51] = {
        **tables["assertion_record_index.tsv"][51],
        "source_identity_set_status": "optional",
    }

    rows = module.validate_preservation_hardening(tables)
    statuses = {row["check_name"]: row["status"] for row in rows}

    assert statuses["source_identity_obligation_status_is_explicit"] == "failed"


def test_bundle_report_declares_external_sidecar_checksum_authority(tmp_path: Path) -> None:
    module = _load_script()
    payload = module.bundle_report_payload(
        bundle_path=tmp_path / "receipt.tgz",
        sha_path=tmp_path / "receipt.tgz.sha256",
        retrieval_mode="plan_a_full_output_bundle",
        include_build_output=True,
    )

    assert payload["bundle_checksum_authority"] == "external_sidecar"
    assert payload["bundle_sha256_sidecar_name"] == "receipt.tgz.sha256"
    assert payload["internal_archive_sha256_claim"] is False
    assert "bundle_sha256" not in payload

    rows = module.bundle_report_rows(payload)
    keys = {row["key"] for row in rows}
    assert "bundle_checksum_authority" in keys
    assert "bundle_sha256" not in keys


def test_make_bundle_writes_external_sha256_sidecar_without_internal_archive_sha_claim(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_script()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)

    receipt_dir = tmp_path / "results" / "validation" / "phase4_assertion_records" / "receipt"
    build_output = tmp_path / "results" / "phase4" / "assertion_records" / "mark_phase4_corpus_6tep_v1"
    desktop_root = tmp_path / "Desktop"
    receipt_dir.mkdir(parents=True)
    build_output.mkdir(parents=True)
    (receipt_dir / "validation_summary.json").write_text('{"overall_status":"passed"}\n', encoding="utf-8")
    (build_output / "assertion_record_index.tsv").write_text("assertion_id\na1\n", encoding="utf-8")

    anticipated_bundle = desktop_root / "phase4_3_mark_full_corpus_assertion_record_smoketest_2099_01_01_000000.tgz"
    anticipated_sha = desktop_root / f"{anticipated_bundle.name}.sha256"
    payload = module.bundle_report_payload(
        bundle_path=anticipated_bundle,
        sha_path=anticipated_sha,
        retrieval_mode="plan_a_full_output_bundle",
        include_build_output=True,
    )
    (receipt_dir / "bundle_report.json").write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    bundle_path, sha_path, digest = module.make_bundle(
        timestamp="2099_01_01_000000",
        desktop_root=desktop_root,
        receipt_dir=receipt_dir,
        build_output=build_output,
        retrieval_mode="plan_a_full_output_bundle",
        include_build_output=True,
    )

    assert bundle_path.exists()
    assert sha_path.exists()
    assert digest in sha_path.read_text(encoding="utf-8")

    with tarfile.open(bundle_path, "r:gz") as tar:
        names = set(tar.getnames())
        report_name = "results/validation/phase4_assertion_records/receipt/bundle_report.json"
        assert report_name in names
        extracted_file = tar.extractfile(report_name)
        assert extracted_file is not None
        extracted = json.loads(extracted_file.read().decode("utf-8"))

    assert extracted["bundle_checksum_authority"] == "external_sidecar"
    assert extracted["internal_archive_sha256_claim"] is False
    assert "bundle_sha256" not in extracted

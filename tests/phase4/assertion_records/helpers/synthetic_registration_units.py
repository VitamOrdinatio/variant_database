"""Synthetic Registration Unit factory for Phase 4.3C Layer 1 tests.

The fixture produced here is intentionally tiny and synthetic. It mimics the
contract-critical relational shape of Registration Units without using real VAP/GSC
payloads. Layer 2 is responsible for compressed real-world fixture validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import hashlib
import json
import sqlite3
from typing import Iterable

CORPUS_GENERATION_ID = "synthetic_phase4_3_layer1_corpus_v1"
SYNTHETIC_VAP_RU = "synthetic_vap_registration_unit"
SYNTHETIC_GSC_RU = "synthetic_gsc_registration_unit"

ASSERTION_COLUMNS = [
    "assertion_registration_id",
    "package_id",
    "artifact_id",
    "surface_role",
    "evidence_domain",
    "producer_family",
    "source_record_ref",
    "assertion_type",
    "participant_summary_json",
    "support_ref_json",
    "authority_context",
    "uncertainty_context",
    "registration_status",
    "payload_json",
]

SOURCE_IDENTITY_COLUMNS = [
    "source_identity_id",
    "assertion_registration_id",
    "identity_kind",
    "participant_role",
    "source_value",
    "source_namespace",
    "source_label",
    "extraction_method",
    "source_record_ref",
    "payload_json",
]

ARTIFACT_COLUMNS = [
    "artifact_id",
    "package_id",
    "relative_path",
    "size_bytes",
    "sha256",
    "is_manifest",
]

PACKAGE_COLUMNS = [
    "package_id",
    "producer_family",
    "package_label",
    "source_package_id",
]

SCHEMA_METADATA_COLUMNS = [
    "schema_metadata_id",
    "schema_name",
    "schema_version",
    "created_by",
]

MANIFEST_COLUMNS = [
    "corpus_generation_id",
    "registration_unit_id",
    "registration_unit_label",
    "producer_family",
    "registration_unit_sqlite_path",
    "registration_unit_path",
    "validation_status",
]


@dataclass(frozen=True)
class SyntheticCorpus:
    root_dir: Path
    manifest_path: Path
    output_dir: Path
    corpus_generation_id: str
    registration_unit_paths: dict[str, Path]
    assertion_registration_ids: list[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def _stable_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _assertion(
    *,
    assertion_registration_id: str,
    package_id: str,
    artifact_id: str,
    surface_role: str,
    evidence_domain: str,
    producer_family: str,
    source_record_ref: str | None,
    assertion_type: str,
    participant_summary: object,
    support_ref: object,
    authority_context: str = "producer_emitted",
    uncertainty_context: str = "source_asserted",
    payload: object | None = None,
) -> dict[str, str]:
    return {
        "assertion_registration_id": assertion_registration_id,
        "package_id": package_id,
        "artifact_id": artifact_id,
        "surface_role": surface_role,
        "evidence_domain": evidence_domain,
        "producer_family": producer_family,
        "source_record_ref": source_record_ref or "",
        "assertion_type": assertion_type,
        "participant_summary_json": _json(participant_summary),
        "support_ref_json": _json(support_ref),
        "authority_context": authority_context,
        "uncertainty_context": uncertainty_context,
        "registration_status": "registered",
        "payload_json": _json(payload or {"synthetic": True, "assertion_type": assertion_type}),
    }


def _source_identity(
    *,
    source_identity_id: str,
    assertion_registration_id: str,
    identity_kind: str,
    participant_role: str,
    source_value: str,
    source_namespace: str,
    source_label: str,
    extraction_method: str = "synthetic_layer1_fixture",
    source_record_ref: str | None = None,
    payload: object | None = None,
) -> dict[str, str]:
    return {
        "source_identity_id": source_identity_id,
        "assertion_registration_id": assertion_registration_id,
        "identity_kind": identity_kind,
        "participant_role": participant_role,
        "source_value": source_value,
        "source_namespace": source_namespace,
        "source_label": source_label,
        "extraction_method": extraction_method,
        "source_record_ref": source_record_ref or "",
        "payload_json": _json(payload or {"synthetic": True}),
    }


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE assertion_registrations ("
        + ", ".join(f"{column} TEXT" for column in ASSERTION_COLUMNS)
        + ")"
    )
    conn.execute(
        "CREATE TABLE source_identities ("
        + ", ".join(f"{column} TEXT" for column in SOURCE_IDENTITY_COLUMNS)
        + ")"
    )
    conn.execute(
        "CREATE TABLE artifacts ("
        "artifact_id TEXT, package_id TEXT, relative_path TEXT, "
        "size_bytes INTEGER, sha256 TEXT, is_manifest INTEGER)"
    )
    conn.execute(
        "CREATE TABLE tep_packages ("
        "package_id TEXT, producer_family TEXT, package_label TEXT, source_package_id TEXT)"
    )
    conn.execute(
        "CREATE TABLE schema_metadata ("
        "schema_metadata_id TEXT, schema_name TEXT, schema_version TEXT, created_by TEXT)"
    )


def _insert_rows(conn: sqlite3.Connection, table: str, rows: list[dict[str, object]], columns: list[str]) -> None:
    placeholders = ", ".join("?" for _ in columns)
    column_sql = ", ".join(columns)
    conn.executemany(
        f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
        [[row.get(column, "") for column in columns] for row in rows],
    )


def _write_registration_unit(
    path: Path,
    *,
    package_id: str,
    producer_family: str,
    package_label: str,
    assertion_rows: list[dict[str, str]],
    source_identity_rows: list[dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        _create_schema(conn)
        artifact_rows = []
        seen_artifacts: set[str] = set()
        for row in assertion_rows:
            artifact_id = row["artifact_id"]
            if artifact_id in seen_artifacts:
                continue
            seen_artifacts.add(artifact_id)
            artifact_rows.append(
                {
                    "artifact_id": artifact_id,
                    "package_id": row["package_id"],
                    "relative_path": f"synthetic/{producer_family.lower()}/{artifact_id}.tsv",
                    "size_bytes": 128,
                    "sha256": _stable_sha(artifact_id),
                    "is_manifest": 0,
                }
            )

        _insert_rows(conn, "assertion_registrations", assertion_rows, ASSERTION_COLUMNS)
        _insert_rows(conn, "source_identities", source_identity_rows, SOURCE_IDENTITY_COLUMNS)
        _insert_rows(conn, "artifacts", artifact_rows, ARTIFACT_COLUMNS)
        _insert_rows(
            conn,
            "tep_packages",
            [
                {
                    "package_id": package_id,
                    "producer_family": producer_family,
                    "package_label": package_label,
                    "source_package_id": package_id,
                }
            ],
            PACKAGE_COLUMNS,
        )
        _insert_rows(
            conn,
            "schema_metadata",
            [
                {
                    "schema_metadata_id": f"{package_id}:schema",
                    "schema_name": "synthetic_registration_unit_v1",
                    "schema_version": "phase4_3_layer1",
                    "created_by": "pytest_synthetic_registration_units",
                }
            ],
            SCHEMA_METADATA_COLUMNS,
        )
        conn.commit()
    finally:
        conn.close()


def build_layer1_synthetic_corpus(tmp_path: Path) -> SyntheticCorpus:
    """Create two tiny synthetic Registration Unit SQLite files and a manifest."""
    root = tmp_path / "phase4_3_layer1_synthetic_corpus"
    ru_dir = root / "registration_units"
    output_dir = root / "assertion_records_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    vap_package = "synthetic_vap_package_001"
    gsc_package = "synthetic_gsc_package_001"

    vap_assertions = [
        _assertion(
            assertion_registration_id="vap_variant_observation_001",
            package_id=vap_package,
            artifact_id="vap_artifact_observation_001",
            surface_role="variant_observation",
            evidence_domain="variant",
            producer_family="VAP",
            source_record_ref="vap:row:1",
            assertion_type="variant_observation",
            participant_summary={"sample": "SYNTHETIC_SAMPLE", "variant": "chr1:101:A:T"},
            support_ref={"artifact_id": "vap_artifact_observation_001"},
        ),
        _assertion(
            assertion_registration_id="vap_variant_interpretation_001",
            package_id=vap_package,
            artifact_id="vap_artifact_interpretation_001",
            surface_role="noncoding_interpretation",
            evidence_domain="variant_annotation",
            producer_family="VAP",
            source_record_ref="vap:row:2",
            assertion_type="variant_interpretation",
            participant_summary={"variant": "chr1:202:G:C", "gene": "GENE1"},
            support_ref={"annotation_source": "synthetic_annotation"},
            payload={"interpretation_label": "synthetic_label", "biological_truth": "not_assigned"},
        ),
        _assertion(
            assertion_registration_id="vap_validation_001",
            package_id=vap_package,
            artifact_id="vap_artifact_validation_001",
            surface_role="validation",
            evidence_domain="producer_validation",
            producer_family="VAP",
            source_record_ref="vap:validation:1",
            assertion_type="validation",
            participant_summary={"sample": "SYNTHETIC_SAMPLE", "method": "synthetic_validation"},
            support_ref={"artifact_id": "vap_artifact_validation_001"},
        ),
        _assertion(
            assertion_registration_id="vap_candidate_routing_001",
            package_id=vap_package,
            artifact_id="vap_artifact_routing_001",
            surface_role="candidate_routing",
            evidence_domain="routing",
            producer_family="VAP",
            source_record_ref="vap:routing:1",
            assertion_type="candidate_routing",
            participant_summary={"variant": "chr1:303:T:G", "priority_tier": "synthetic_tier"},
            support_ref={"artifact_id": "vap_artifact_routing_001"},
        ),
        _assertion(
            assertion_registration_id="vap_unsupported_experimental_signal_001",
            package_id=vap_package,
            artifact_id="vap_artifact_unsupported_001",
            surface_role="experimental_signal",
            evidence_domain="unsupported_experimental",
            producer_family="VAP",
            source_record_ref="vap:unsupported:1",
            assertion_type="unsupported_experimental_signal",
            participant_summary={"variant": "chr1:404:C:A"},
            support_ref={"artifact_id": "vap_artifact_unsupported_001"},
        ),
    ]

    vap_source_identities = [
        _source_identity(
            source_identity_id="vap_si_sample_001",
            assertion_registration_id="vap_variant_observation_001",
            identity_kind="sample",
            participant_role="sample",
            source_value="SYNTHETIC_SAMPLE",
            source_namespace="synthetic_sample_id",
            source_label="Synthetic Sample",
            source_record_ref="vap:row:1",
        ),
        _source_identity(
            source_identity_id="vap_si_variant_001",
            assertion_registration_id="vap_variant_observation_001",
            identity_kind="variant",
            participant_role="variant",
            source_value="chr1:101:A:T",
            source_namespace="synthetic_variant_id",
            source_label="Synthetic observed variant",
            source_record_ref="vap:row:1",
        ),
        _source_identity(
            source_identity_id="vap_si_variant_002",
            assertion_registration_id="vap_variant_interpretation_001",
            identity_kind="variant",
            participant_role="variant",
            source_value="chr1:202:G:C",
            source_namespace="synthetic_variant_id",
            source_label="Synthetic interpreted variant",
            source_record_ref="vap:row:2",
            payload={"explicit_noncoding_status": "noncoding"},
        ),
        _source_identity(
            source_identity_id="vap_si_gene_001",
            assertion_registration_id="vap_variant_interpretation_001",
            identity_kind="gene",
            participant_role="gene",
            source_value="GENE1",
            source_namespace="synthetic_gene_symbol",
            source_label="GENE1",
            source_record_ref="vap:row:2",
        ),
        _source_identity(
            source_identity_id="vap_si_method_001",
            assertion_registration_id="vap_validation_001",
            identity_kind="validation_method",
            participant_role="validation_method",
            source_value="synthetic_validation",
            source_namespace="synthetic_validation_method",
            source_label="Synthetic validation method",
            source_record_ref="vap:validation:1",
        ),
        _source_identity(
            source_identity_id="vap_si_tier_001",
            assertion_registration_id="vap_candidate_routing_001",
            identity_kind="priority_tier",
            participant_role="priority_tier",
            source_value="synthetic_tier",
            source_namespace="synthetic_priority_tier",
            source_label="Synthetic priority tier",
            source_record_ref="vap:routing:1",
        ),
    ]

    gsc_assertions = [
        _assertion(
            assertion_registration_id="gsc_phenotype_gene_semantic_prior_001",
            package_id=gsc_package,
            artifact_id="gsc_artifact_semantic_prior_001",
            surface_role="semantic_prior",
            evidence_domain="phenotype_gene",
            producer_family="GSC",
            source_record_ref="gsc:row:1",
            assertion_type="phenotype_gene_semantic_prior",
            participant_summary={"phenotype": "synthetic epilepsy", "gene": "GENE2"},
            support_ref={"semantic_channel": "synthetic_channel"},
        ),
        _assertion(
            assertion_registration_id="gsc_source_gene_relationship_001",
            package_id=gsc_package,
            artifact_id="gsc_artifact_source_gene_001",
            surface_role="source_gene_relationship",
            evidence_domain="phenotype_gene_source",
            producer_family="GSC",
            source_record_ref="gsc:row:2",
            assertion_type="source_gene_relationship",
            participant_summary={"source": "synthetic_source", "gene": "GENE2"},
            support_ref={"artifact_id": "gsc_artifact_source_gene_001"},
        ),
        _assertion(
            assertion_registration_id="gsc_producer_contract_validation_001",
            package_id=gsc_package,
            artifact_id="gsc_artifact_contract_validation_001",
            surface_role="output_contract_validation",
            evidence_domain="producer_contract_validation",
            producer_family="GSC",
            source_record_ref=None,
            assertion_type="producer_contract_validation",
            participant_summary={},
            support_ref={"artifact_id": "gsc_artifact_contract_validation_001"},
            payload={"registration_level": "artifact", "source_identity_set_status": "not_applicable"},
        ),
    ]

    gsc_source_identities = [
        _source_identity(
            source_identity_id="gsc_si_phenotype_001",
            assertion_registration_id="gsc_phenotype_gene_semantic_prior_001",
            identity_kind="phenotype",
            participant_role="phenotype",
            source_value="synthetic epilepsy",
            source_namespace="synthetic_phenotype_label",
            source_label="Synthetic epilepsy",
            source_record_ref="gsc:row:1",
        ),
        _source_identity(
            source_identity_id="gsc_si_gene_001",
            assertion_registration_id="gsc_phenotype_gene_semantic_prior_001",
            identity_kind="gene",
            participant_role="gene",
            source_value="GENE2",
            source_namespace="synthetic_gene_symbol",
            source_label="GENE2",
            source_record_ref="gsc:row:1",
        ),
        _source_identity(
            source_identity_id="gsc_si_channel_001",
            assertion_registration_id="gsc_phenotype_gene_semantic_prior_001",
            identity_kind="semantic_channel",
            participant_role="semantic_channel",
            source_value="synthetic_channel",
            source_namespace="synthetic_semantic_channel",
            source_label="Synthetic semantic channel",
            source_record_ref="gsc:row:1",
        ),
        _source_identity(
            source_identity_id="gsc_si_source_001",
            assertion_registration_id="gsc_source_gene_relationship_001",
            identity_kind="evidence_source",
            participant_role="evidence_source",
            source_value="synthetic_source",
            source_namespace="synthetic_source_id",
            source_label="Synthetic source",
            source_record_ref="gsc:row:2",
        ),
        _source_identity(
            source_identity_id="gsc_si_gene_002",
            assertion_registration_id="gsc_source_gene_relationship_001",
            identity_kind="gene",
            participant_role="gene",
            source_value="GENE2",
            source_namespace="synthetic_gene_symbol",
            source_label="GENE2",
            source_record_ref="gsc:row:2",
        ),
    ]

    vap_db = ru_dir / f"{SYNTHETIC_VAP_RU}.sqlite"
    gsc_db = ru_dir / f"{SYNTHETIC_GSC_RU}.sqlite"

    _write_registration_unit(
        vap_db,
        package_id=vap_package,
        producer_family="VAP",
        package_label="Synthetic VAP package",
        assertion_rows=vap_assertions,
        source_identity_rows=vap_source_identities,
    )
    _write_registration_unit(
        gsc_db,
        package_id=gsc_package,
        producer_family="GSC",
        package_label="Synthetic GSC package",
        assertion_rows=gsc_assertions,
        source_identity_rows=gsc_source_identities,
    )

    manifest_path = root / "synthetic_downstream_assertion_record_input_manifest.tsv"
    write_tsv(
        manifest_path,
        [
            {
                "corpus_generation_id": CORPUS_GENERATION_ID,
                "registration_unit_id": SYNTHETIC_VAP_RU,
                "registration_unit_label": "synthetic_vap",
                "producer_family": "VAP",
                "registration_unit_sqlite_path": str(vap_db),
                "registration_unit_path": str(vap_db),
                "validation_status": "synthetic_layer1_valid",
            },
            {
                "corpus_generation_id": CORPUS_GENERATION_ID,
                "registration_unit_id": SYNTHETIC_GSC_RU,
                "registration_unit_label": "synthetic_gsc",
                "producer_family": "GSC",
                "registration_unit_sqlite_path": str(gsc_db),
                "registration_unit_path": str(gsc_db),
                "validation_status": "synthetic_layer1_valid",
            },
        ],
        MANIFEST_COLUMNS,
    )

    assertion_ids = [row["assertion_registration_id"] for row in vap_assertions + gsc_assertions]
    return SyntheticCorpus(
        root_dir=root,
        manifest_path=manifest_path,
        output_dir=output_dir,
        corpus_generation_id=CORPUS_GENERATION_ID,
        registration_unit_paths={SYNTHETIC_VAP_RU: vap_db, SYNTHETIC_GSC_RU: gsc_db},
        assertion_registration_ids=assertion_ids,
    )

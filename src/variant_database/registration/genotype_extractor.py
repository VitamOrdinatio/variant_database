"""Genotype package discovery and context indexing.

This module implements the first VDB genotype maturity tier:
`genotype_discovered`.

It intentionally does not preserve row-level genotype observations, register
direct genotype-to-variant relationships, broker complex relationships, or emit
inheritance reasoning.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, TypedDict

from variant_database.persistence.genotype_repositories import (
    genotype_artifact_index_id_for_role,
    genotype_classification_id_for_package,
    genotype_context_index_id_for_kind,
)

CANONICAL_GENOTYPE_ARTIFACTS = {
    "genotype_observations": "entities/genotype/genotype_observations.tsv",
    "genotype_projection_summary": "entities/genotype/genotype_projection_summary.json",
    "genotype_source_header_context": "entities/genotype/genotype_source_header_context.json",
}

REQUIRED_GOVERNANCE_ARTIFACTS = (
    "entity_inventory.json",
    "lineage_manifest.json",
    "validation_report.md",
)

EXECUTION_PROVENANCE_PATH = "entities/context/execution_provenance.json"

SUPPORTED_SCHEMA_VERSIONS = {
    "genotype_observations": "genotype_observation_v1",
    "genotype_projection_summary": "genotype_projection_summary_v1",
    "genotype_source_header_context": "genotype_source_header_context_v1",
    "execution_provenance": "1.0.0",
}


class GenotypeDiscoveryRecords(TypedDict):
    """Typed collection of package-level genotype discovery records."""

    classification: dict[str, object]
    artifact_index_records: list[dict[str, object]]
    context_index_records: list[dict[str, object]]


def _artifact_by_path(
    artifact_records: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    return {
        str(record["relative_path"]): record
        for record in artifact_records
    }


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - preserve parse failure as status.
        return None, "parse_error", str(exc)

    if not isinstance(data, dict):
        return None, "parse_error", "JSON root is not an object"

    return data, "parsed", None


def _read_genotype_observation_schema_version(path: Path) -> tuple[str | None, str, str | None, int | None]:
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            fieldnames = reader.fieldnames or []
            first_row = next(reader, None)
    except Exception as exc:  # noqa: BLE001 - preserve parse failure as status.
        return None, "parse_error", str(exc), None

    if not fieldnames:
        return None, "parse_error", "Missing genotype observation header", 0

    schema_version = first_row.get("schema_version") if first_row else None
    return schema_version, "header_parsed", None, len(fieldnames)


def _payload_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True)


def _artifact_record_for_path(
    artifact_map: dict[str, dict[str, object]],
    relative_path: str,
) -> dict[str, object] | None:
    return artifact_map.get(relative_path)


def _artifact_id(record: dict[str, object] | None) -> str | None:
    return str(record["artifact_id"]) if record is not None else None


def _artifact_sha(record: dict[str, object] | None) -> str:
    return str(record["sha256"]) if record is not None else ""


def _artifact_size(record: dict[str, object] | None) -> int:
    """Return a validated artifact size from a persisted artifact record."""
    if record is None:
        return 0

    value = record.get("size_bytes")

    if isinstance(value, bool):
        raise TypeError("Artifact size_bytes must not be boolean")

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f"Artifact size_bytes is not an integer string: {value!r}"
            ) from exc

    raise TypeError(
        "Artifact size_bytes must be an integer or integer string; "
        f"received {type(value).__name__}"
    )


def build_genotype_artifact_index_records(
    package_id: str,
    package_path: str,
    artifact_records: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Build canonical genotype artifact index records."""
    package = Path(package_path)
    artifact_map = _artifact_by_path(artifact_records)
    records: list[dict[str, object]] = []

    for role, relative_path in CANONICAL_GENOTYPE_ARTIFACTS.items():
        artifact = _artifact_record_for_path(artifact_map, relative_path)
        artifact_present = artifact is not None
        schema_version: str | None = None
        parse_status = "missing"
        parse_error: str | None = None
        column_count: int | None = None

        if artifact_present:
            path = package / relative_path
            if role == "genotype_observations":
                schema_version, parse_status, parse_error, column_count = (
                    _read_genotype_observation_schema_version(path)
                )
            else:
                data, parse_status, parse_error = _read_json(path)
                schema_version = str(data.get("schema_version")) if data else None

        payload = {
            "artifact_present": artifact_present,
            "artifact_role": role,
            "artifact_path": relative_path,
            "column_count": column_count,
            "parse_error": parse_error,
            "schema_version": schema_version,
        }

        records.append(
            {
                "genotype_artifact_index_id": genotype_artifact_index_id_for_role(
                    package_id=package_id,
                    artifact_role=role,
                    artifact_path=relative_path,
                ),
                "package_id": package_id,
                "artifact_id": _artifact_id(artifact),
                "artifact_role": role,
                "artifact_path": relative_path,
                "artifact_sha256": _artifact_sha(artifact),
                "size_bytes": _artifact_size(artifact),
                "artifact_present": int(artifact_present),
                "required_for_trusted_modern_ingestion": 1,
                "schema_version": schema_version,
                "parse_status": parse_status,
                "payload_json": _payload_json(payload),
            }
        )

    return records


def build_genotype_context_index_records(
    package_id: str,
    package_path: str,
    artifact_records: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Build genotype context index records for summary/header/provenance."""
    package = Path(package_path)
    artifact_map = _artifact_by_path(artifact_records)
    context_specs = [
        (
            "genotype_projection_summary",
            CANONICAL_GENOTYPE_ARTIFACTS["genotype_projection_summary"],
        ),
        (
            "genotype_source_header_context",
            CANONICAL_GENOTYPE_ARTIFACTS["genotype_source_header_context"],
        ),
        ("execution_provenance", EXECUTION_PROVENANCE_PATH),
    ]

    records: list[dict[str, object]] = []

    for context_kind, relative_path in context_specs:
        artifact = _artifact_record_for_path(artifact_map, relative_path)
        artifact_present = artifact is not None
        data: dict[str, Any] | None = None
        parse_status = "missing"
        parse_error: str | None = None

        if artifact_present:
            data, parse_status, parse_error = _read_json(package / relative_path)

        counts = data.get("counts", {}) if data else {}
        projection = data.get("projection", {}) if data else {}
        sample_resolution = data.get("sample_resolution", {}) if data else {}
        source_vcf = data.get("source_vcf", {}) if data else {}
        reference_context = data.get("reference_context", {}) if data else {}

        if context_kind == "execution_provenance":
            contract_status = data.get("contract_status") if data else None
            provenance_completeness = data.get("provenance_completeness") if data else None
            projection_status = None
            reference_build = None
            sample_id = None
            run_id = None
        elif context_kind == "genotype_projection_summary":
            contract_status = None
            provenance_completeness = None
            projection_status = projection.get("projection_status")
            reference_build = projection.get("reference_build")
            sample_id = sample_resolution.get("sample_id")
            run_id = sample_resolution.get("run_id")
        else:
            contract_status = None
            provenance_completeness = None
            projection_status = None
            reference_build = (
                reference_context.get("reference_build")
                or reference_context.get("assembly")
                or reference_context.get("reference_genome_build")
            )
            sample_columns = data.get("sample_columns", []) if data else []
            sample_id = sample_columns[0] if isinstance(sample_columns, list) and sample_columns else None
            run_id = None

        payload = {
            "context_kind": context_kind,
            "artifact_present": artifact_present,
            "parse_error": parse_error,
            "payload": data or {},
        }

        records.append(
            {
                "genotype_context_index_id": genotype_context_index_id_for_kind(
                    package_id=package_id,
                    context_kind=context_kind,
                    context_artifact_path=relative_path,
                ),
                "package_id": package_id,
                "artifact_id": _artifact_id(artifact),
                "context_kind": context_kind,
                "context_artifact_path": relative_path,
                "context_artifact_sha256": _artifact_sha(artifact),
                "schema_version": str(data.get("schema_version")) if data else None,
                "parse_status": parse_status,
                "registered_as_context": int(parse_status == "parsed"),
                "registered_as_biological_evidence": 0,
                "contract_status": contract_status,
                "provenance_completeness": provenance_completeness,
                "projection_status": projection_status,
                "genotype_observation_row_count": counts.get("genotype_observation_row_count"),
                "source_record_count": source_vcf.get("source_record_count"),
                "direct_relationship_count": counts.get("direct_relationship_count"),
                "complex_relationship_count": counts.get("complex_relationship_count"),
                "unresolved_relationship_count": counts.get("unresolved_relationship_count"),
                "projection_error_count": counts.get("projection_error_count"),
                "projection_warning_count": counts.get("projection_warning_count"),
                "reference_build": reference_build,
                "sample_id": sample_id,
                "run_id": run_id,
                "payload_json": _payload_json(payload),
            }
        )

    return records


def _schema_status(
    artifact_index_records: list[dict[str, object]],
    context_index_records: list[dict[str, object]],
) -> tuple[str, str]:
    parse_errors = [
        str(record["artifact_role"])
        for record in artifact_index_records
        if record["artifact_present"] and record["parse_status"] == "parse_error"
    ]
    parse_errors.extend(
        str(record["context_kind"])
        for record in context_index_records
        if record["artifact_id"] is not None and record["parse_status"] == "parse_error"
    )

    if parse_errors:
        return "genotype_capability_invalid", "parse_error:" + ",".join(parse_errors)

    unsupported: list[str] = []
    for record in artifact_index_records:
        role = str(record["artifact_role"])
        schema_version = record["schema_version"]
        expected = SUPPORTED_SCHEMA_VERSIONS.get(role)

        # For genotype_observations.tsv, a missing schema_version in an empty
        # fixture is invalid only for trusted modern ingestion. Real VAP rows
        # are expected to emit schema_version.
        if record["artifact_present"] and expected and schema_version != expected:
            unsupported.append(f"{role}:{schema_version}")

    for record in context_index_records:
        context_kind = str(record["context_kind"])
        schema_version = record["schema_version"]
        expected = SUPPORTED_SCHEMA_VERSIONS.get(context_kind)
        if record["artifact_id"] is not None and expected and schema_version != expected:
            unsupported.append(f"{context_kind}:{schema_version}")

    if unsupported:
        return "genotype_capability_unsupported_version", "unsupported_schema:" + ",".join(unsupported)

    return "ok", "schema_supported"


def build_genotype_package_classification(
    package_id: str,
    package_path: str,
    artifact_records: list[dict[str, object]],
    producer_family: str,
    artifact_index_records: list[dict[str, object]],
    context_index_records: list[dict[str, object]],
) -> dict[str, object]:
    """Build one package-level genotype classification."""
    producer = producer_family.strip().upper()
    artifact_map = _artifact_by_path(artifact_records)

    if producer == "GSC":
        payload = {
            "producer_family": producer_family,
            "reason": "genotype_not_applicable_to_producer_type",
        }
        return {
            "genotype_classification_id": genotype_classification_id_for_package(
                package_id
            ),
            "package_id": package_id,
            "producer_family": producer_family,
            "producer_genotype_applicability_state": (
                "genotype_not_applicable_to_producer_type"
            ),
            "genotype_capability_state": (
                "genotype_capability_not_applicable"
            ),
            "genotype_maturity_state": "genotype_maturity_not_applicable",
            "genotype_artifact_set_status": (
                "genotype_artifact_set_not_applicable"
            ),
            "governance_artifact_set_status": (
                "governance_artifact_set_not_applicable"
            ),
            "execution_provenance_status": (
                "execution_provenance_not_applicable"
            ),
            "trusted_modern_ingestion_ready": 0,
            "classification_status": "classified",
            "classification_reason": (
                "genotype_not_applicable_to_producer_type"
            ),
            "payload_json": _payload_json(payload),
        }

    if producer != "VAP":
        raise ValueError(
            "Unsupported producer family for genotype classification: "
            f"{producer_family!r}"
        )

    genotype_missing = [
        path
        for path in CANONICAL_GENOTYPE_ARTIFACTS.values()
        if path not in artifact_map
    ]
    genotype_present_count = len(CANONICAL_GENOTYPE_ARTIFACTS) - len(genotype_missing)

    governance_missing = [
        path for path in REQUIRED_GOVERNANCE_ARTIFACTS if path not in artifact_map
    ]

    execution_record = _artifact_record_for_path(artifact_map, EXECUTION_PROVENANCE_PATH)
    execution_context = next(
        (
            record
            for record in context_index_records
            if record["context_kind"] == "execution_provenance"
        ),
        None,
    )

    if genotype_present_count == 0:
        capability_state = "genotype_capability_unavailable_legacy"
        artifact_set_status = "genotype_artifact_set_absent"
        classification_reason = "genotype_artifacts_not_emitted_by_source"
        trusted_ready = 0
    elif genotype_missing:
        capability_state = "genotype_capability_incomplete"
        artifact_set_status = "genotype_artifact_set_incomplete"
        classification_reason = "missing_genotype_artifacts:" + ",".join(genotype_missing)
        trusted_ready = 0
    elif governance_missing:
        capability_state = "genotype_capability_incomplete"
        artifact_set_status = "genotype_artifact_set_complete"
        classification_reason = "missing_governance_artifacts:" + ",".join(governance_missing)
        trusted_ready = 0
    elif execution_record is None:
        capability_state = "genotype_capability_incomplete"
        artifact_set_status = "genotype_artifact_set_complete"
        classification_reason = "missing_execution_provenance"
        trusted_ready = 0
    else:
        schema_state, schema_reason = _schema_status(
            artifact_index_records=artifact_index_records,
            context_index_records=context_index_records,
        )
        if schema_state != "ok":
            capability_state = schema_state
            artifact_set_status = "genotype_artifact_set_complete"
            classification_reason = schema_reason
            trusted_ready = 0
        elif (
            execution_context is None
            or execution_context["parse_status"] != "parsed"
            or execution_context["contract_status"] != "pass"
            or execution_context["provenance_completeness"] != "complete"
        ):
            capability_state = "genotype_capability_invalid"
            artifact_set_status = "genotype_artifact_set_complete"
            classification_reason = "execution_provenance_context_invalid"
            trusted_ready = 0
        else:
            capability_state = "genotype_capability_available"
            artifact_set_status = "genotype_artifact_set_complete"
            classification_reason = "complete_modern_genotype_capable_package"
            trusted_ready = 1

    if governance_missing:
        governance_status = "governance_artifact_set_incomplete"
    else:
        governance_status = "governance_artifact_set_complete"

    if execution_record is None:
        execution_status = "execution_provenance_missing"
    elif execution_context and execution_context["parse_status"] == "parsed":
        execution_status = "execution_provenance_registered_as_context"
    else:
        execution_status = "execution_provenance_invalid"

    payload = {
        "canonical_genotype_artifacts": CANONICAL_GENOTYPE_ARTIFACTS,
        "missing_genotype_artifacts": genotype_missing,
        "missing_governance_artifacts": governance_missing,
        "execution_provenance_path": EXECUTION_PROVENANCE_PATH,
        "package_path": package_path,
    }

    return {
        "genotype_classification_id": genotype_classification_id_for_package(package_id),
        "package_id": package_id,
        "producer_family": producer_family,
        "producer_genotype_applicability_state": "genotype_applicable_to_producer_type",
        "genotype_capability_state": capability_state,
        "genotype_maturity_state": "genotype_discovered",
        "genotype_artifact_set_status": artifact_set_status,
        "governance_artifact_set_status": governance_status,
        "execution_provenance_status": execution_status,
        "trusted_modern_ingestion_ready": trusted_ready,
        "classification_status": "classified",
        "classification_reason": classification_reason,
        "payload_json": _payload_json(payload),
    }


def build_genotype_discovery_records(
    package_id: str,
    package_path: str,
    artifact_records: list[dict[str, object]],
    producer_family: str,
) -> GenotypeDiscoveryRecords:
    """Build all genotype discovery records for one package."""
    artifact_index_records = build_genotype_artifact_index_records(
        package_id=package_id,
        package_path=package_path,
        artifact_records=artifact_records,
    )
    context_index_records = build_genotype_context_index_records(
        package_id=package_id,
        package_path=package_path,
        artifact_records=artifact_records,
    )
    classification = build_genotype_package_classification(
        package_id=package_id,
        package_path=package_path,
        artifact_records=artifact_records,
        producer_family=producer_family,
        artifact_index_records=artifact_index_records,
        context_index_records=context_index_records,
    )

    return {
        "classification": classification,
        "artifact_index_records": artifact_index_records,
        "context_index_records": context_index_records,
    }

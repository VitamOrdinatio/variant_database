"""Deterministic Evidence Topology artifact writers.

This module serializes the in-memory Phase 4.4 Evidence Topology row build
without changing topology semantics. It does not derive new topology, compute
Convergence Geometry, construct Evidence Convergence Surfaces, emit Projection
Views, perform statistical testing, or perform RDGP reasoning.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence


OUTPUT_WRITER_NAME = "variant_database.phase4.evidence_topology.outputs"
OUTPUT_WRITER_VERSION = "0.1.0"

VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"
VALIDATION_STATUS_NOT_APPLICABLE = "not_applicable"

REQUIRED_OUTPUTS = [
    "topology_build_manifest.tsv",
    "topology_build_manifest.json",
    "topology_relationships.tsv",
    "topology_relationships.jsonl",
    "topology_relationship_members.tsv",
    "topology_basis_components.tsv",
    "topology_source_identity_expansion_index.tsv",
    "topology_declaration_set_expansion_index.tsv",
    "topology_namespace_mediation.tsv",
    "topology_metadata_relationships.tsv",
    "topology_summary.tsv",
    "topology_validation_report.json",
    "topology_validation_report.tsv",
    "topology_build_report.md",
    "downstream_geometry_input_manifest.tsv",
]

RELATIONSHIP_COLUMNS = [
    "topology_relationship_id",
    "topology_build_id",
    "relationship_family_id",
    "topology_dimension",
    "relationship_kind",
    "derivation_basis",
    "relationship_scope",
    "relationship_classification",
    "grouping_key",
    "grouping_value",
    "source_table",
    "source_assertion_id_summary",
    "source_identity_set_id_summary",
    "member_count",
    "basis_component_count",
    "input_corpus_generation_id",
    "source_identity_expansion_status",
    "statistical_testing_status",
    "namespace_mediation_status",
    "validation_status",
]

MEMBER_COLUMNS = [
    "topology_relationship_id",
    "member_id",
    "member_type",
    "member_role",
    "member_reference",
    "source_assertion_id",
    "source_identity_set_id",
    "source_registration_unit_id",
    "source_corpus_generation_id",
    "validation_status",
]

BASIS_COMPONENT_COLUMNS = [
    "topology_relationship_id",
    "basis_component_id",
    "basis_component_type",
    "basis_component_role",
    "basis_component_value",
    "basis_component_reference",
    "basis_component_namespace",
    "source_assertion_id",
    "source_identity_set_id",
    "source_registration_unit_id",
    "source_corpus_generation_id",
    "resolution_status",
    "ambiguity_status",
    "conflict_status",
    "lossiness_status",
    "validation_status",
]

SOURCE_IDENTITY_EXPANSION_COLUMNS = [
    "topology_build_id",
    "topology_relationship_id",
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "registration_unit_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
    "lossiness_status",
    "resolution_status",
    "source_identity_set_status",
    "source_identity_expansion_status",
    "statistical_testing_status",
    "validation_status",
]

DECLARATION_SET_EXPANSION_COLUMNS = [
    "topology_build_id",
    "topology_relationship_id",
    "declaration_set_type",
    "declaration_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "registration_unit_id",
    "declaration_table_reference",
    "declaration_filter",
    "declaration_count",
    "declaration_kind",
    "declaration_namespace",
    "relationship_type",
    "reference_genome_build",
    "source_artifact_path",
    "lossiness_status",
    "resolution_status",
    "declaration_set_status",
    "declaration_expansion_status",
    "statistical_testing_status",
    "validation_status",
]

NAMESPACE_MEDIATION_COLUMNS = [
    "topology_build_id",
    "topology_relationship_id",
    "relationship_family_id",
    "namespace_mediation_status",
    "match_type",
    "source_namespace_summary",
    "canonical_identity_id",
    "namespace_bridge_id",
    "namespace_policy_status",
    "validation_status",
]

SUMMARY_COLUMNS = [
    "topology_build_id",
    "summary_group",
    "summary_key",
    "summary_value",
]

VALIDATION_REPORT_COLUMNS = [
    "check_id",
    "validation_group",
    "status",
    "message",
    "expected",
    "observed",
]

BUILD_MANIFEST_COLUMNS = [
    "topology_build_id",
    "input_corpus_generation_id",
    "topology_derivation_policy_id",
    "topology_derivation_policy_version",
    "builder_name",
    "builder_version",
    "build_timestamp_utc",
    "output_dir",
    "artifact_name",
    "artifact_path",
    "artifact_role",
    "row_count",
    "sha256",
    "size_bytes",
    "validation_status",
]

DOWNSTREAM_GEOMETRY_COLUMNS = [
    "topology_build_id",
    "topology_relationship_id",
    "relationship_family_id",
    "topology_dimension",
    "relationship_kind",
    "derivation_basis",
    "relationship_scope",
    "relationship_classification",
    "member_count",
    "basis_component_count",
    "source_identity_expansion_status",
    "statistical_testing_status",
    "namespace_mediation_status",
    "input_corpus_generation_id",
    "geometry_input_status",
    "geometry_boundary_note",
]

FORBIDDEN_DOWNSTREAM_GEOMETRY_COLUMNS = {
    "convergence_density",
    "convergence_breadth",
    "convergence_depth",
    "producer_diversity_metric",
    "modality_diversity_metric",
    "evidence_domain_diversity_metric",
    "structural_motif",
    "convergence_region",
    "surface_eligibility",
    "surface_disclosure",
    "surface_withholding",
    "projection_readiness",
    "rdgp_readiness",
    "biological_significance",
    "statistical_significance",
    "burden_score",
}


@dataclass(frozen=True)
class TopologyOutputCheck:
    """Single build-local output validation check."""

    check_id: str
    validation_group: str
    status: str
    message: str
    expected: str
    observed: str


@dataclass(frozen=True)
class TopologyOutputResult:
    """Result returned after deterministic topology artifact emission."""

    output_dir: Path
    topology_build_id: str
    validation_status: str
    artifact_paths: dict[str, Path]
    checks: tuple[TopologyOutputCheck, ...]



def write_topology_outputs(
    build_result: Any,
    policy: str | Path | Mapping[str, Any],
    output_dir: str | Path | None = None,
    *,
    repo_root: str | Path = ".",
    build_timestamp_utc: str | None = None,
) -> TopologyOutputResult:
    """Serialize an in-memory Evidence Topology row build.

    The writer is intentionally deterministic and non-interpretive. It writes
    the full Phase 4.4 topology artifact family to ``output_dir`` and performs
    build-local integrity checks, but it does not derive new relationships.
    """

    repo = Path(repo_root)
    policy_payload = _load_policy(policy)
    defaults = policy_payload.get("topology_build_defaults", {})
    identity = policy_payload.get("policy_identity", {})

    topology_build_id = str(
        defaults.get("topology_build_id")
        or identity.get("topology_build_id")
        or _getattr_or_key(build_result, "topology_build_id", "")
    )
    if not topology_build_id:
        raise ValueError("topology_build_id is required to write topology outputs.")

    if output_dir is None:
        output_dir = defaults.get("output_dir")
    if output_dir is None:
        raise ValueError("output_dir is required when the policy does not define one.")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    timestamp = build_timestamp_utc or _utc_now()

    relationships = _extract_rows(
        build_result,
        "relationships",
        "relationship_rows",
        "topology_relationships",
    )
    members = _extract_rows(
        build_result,
        "members",
        "member_rows",
        "relationship_members",
    )
    basis_components = _extract_rows(
        build_result,
        "basis_components",
        "basis_component_rows",
        "topology_basis_components",
    )
    family_execution_rows = _extract_rows(
        build_result,
        "family_execution_records",
        "family_execution_rows",
        "relationship_family_execution_records",
    )

    relationships = _normalize_relationship_rows(relationships, topology_build_id, policy_payload)
    members = _normalize_member_rows(members)
    basis_components = _normalize_basis_component_rows(basis_components)
    family_execution_rows = _normalize_generic_rows(family_execution_rows)

    expansion_rows = _build_source_identity_expansion_rows(relationships, members, basis_components)
    declaration_expansion_rows = _build_declaration_set_expansion_rows(relationships, members, basis_components)
    namespace_rows = _build_namespace_mediation_rows(relationships, members, basis_components)
    metadata_rows = _build_metadata_relationship_rows(relationships)
    downstream_rows = _build_downstream_geometry_rows(relationships)
    summary_rows = _build_summary_rows(
        topology_build_id=topology_build_id,
        policy=policy_payload,
        relationships=relationships,
        members=members,
        basis_components=basis_components,
        family_execution_rows=family_execution_rows,
        expansion_rows=expansion_rows,
        declaration_expansion_rows=declaration_expansion_rows,
        namespace_rows=namespace_rows,
        metadata_rows=metadata_rows,
        downstream_rows=downstream_rows,
    )

    artifact_paths = {name: out / name for name in REQUIRED_OUTPUTS}

    _write_tsv(artifact_paths["topology_relationships.tsv"], relationships, RELATIONSHIP_COLUMNS)
    _write_jsonl(artifact_paths["topology_relationships.jsonl"], relationships)
    _write_tsv(artifact_paths["topology_relationship_members.tsv"], members, MEMBER_COLUMNS)
    _write_tsv(artifact_paths["topology_basis_components.tsv"], basis_components, BASIS_COMPONENT_COLUMNS)
    _write_tsv(
        artifact_paths["topology_source_identity_expansion_index.tsv"],
        expansion_rows,
        SOURCE_IDENTITY_EXPANSION_COLUMNS,
    )
    _write_tsv(
        artifact_paths["topology_declaration_set_expansion_index.tsv"],
        declaration_expansion_rows,
        DECLARATION_SET_EXPANSION_COLUMNS,
    )
    _write_tsv(
        artifact_paths["topology_namespace_mediation.tsv"],
        namespace_rows,
        NAMESPACE_MEDIATION_COLUMNS,
    )
    _write_tsv(
        artifact_paths["topology_metadata_relationships.tsv"],
        metadata_rows,
        RELATIONSHIP_COLUMNS,
    )
    _write_tsv(artifact_paths["topology_summary.tsv"], summary_rows, SUMMARY_COLUMNS)
    _write_tsv(
        artifact_paths["downstream_geometry_input_manifest.tsv"],
        downstream_rows,
        DOWNSTREAM_GEOMETRY_COLUMNS,
    )

    # Emit stubs so existence checks can reason over the complete required family.
    _write_tsv(artifact_paths["topology_validation_report.tsv"], [], VALIDATION_REPORT_COLUMNS)
    _write_json(artifact_paths["topology_validation_report.json"], {"checks": []})
    artifact_paths["topology_build_report.md"].write_text("# Evidence Topology Build Report\n", encoding="utf-8")
    _write_tsv(artifact_paths["topology_build_manifest.tsv"], [], BUILD_MANIFEST_COLUMNS)
    _write_json(artifact_paths["topology_build_manifest.json"], {"artifacts": []})

    checks = _build_validation_checks(
        artifact_paths=artifact_paths,
        relationships=relationships,
        members=members,
        basis_components=basis_components,
        expansion_rows=expansion_rows,
        declaration_expansion_rows=declaration_expansion_rows,
        namespace_rows=namespace_rows,
        metadata_rows=metadata_rows,
        downstream_rows=downstream_rows,
        family_execution_rows=family_execution_rows,
        policy=policy_payload,
    )
    validation_status = (
        VALIDATION_STATUS_PASSED
        if all(check.status == VALIDATION_STATUS_PASSED for check in checks)
        else VALIDATION_STATUS_FAILED
    )

    validation_rows = [asdict(check) for check in checks]
    _write_tsv(artifact_paths["topology_validation_report.tsv"], validation_rows, VALIDATION_REPORT_COLUMNS)
    _write_json(
        artifact_paths["topology_validation_report.json"],
        {
            "topology_build_id": topology_build_id,
            "validation_status": validation_status,
            "validator_name": OUTPUT_WRITER_NAME,
            "validator_version": OUTPUT_WRITER_VERSION,
            "check_count": len(checks),
            "failed_check_count": sum(1 for check in checks if check.status != VALIDATION_STATUS_PASSED),
            "checks": validation_rows,
        },
    )

    report_text = _build_report_markdown(
        topology_build_id=topology_build_id,
        policy=policy_payload,
        output_dir=out,
        validation_status=validation_status,
        checks=checks,
        summary_rows=summary_rows,
        family_execution_rows=family_execution_rows,
        timestamp=timestamp,
    )
    artifact_paths["topology_build_report.md"].write_text(report_text, encoding="utf-8")

    manifest_rows = _build_manifest_rows(
        topology_build_id=topology_build_id,
        policy=policy_payload,
        output_dir=out,
        artifact_paths=artifact_paths,
        validation_status=validation_status,
        build_timestamp_utc=timestamp,
    )
    _write_tsv(artifact_paths["topology_build_manifest.tsv"], manifest_rows, BUILD_MANIFEST_COLUMNS)
    _write_json(
        artifact_paths["topology_build_manifest.json"],
        {
            "topology_build_id": topology_build_id,
            "input_corpus_generation_id": _input_corpus_generation_id(policy_payload),
            "topology_derivation_policy_id": _policy_id(policy_payload),
            "topology_derivation_policy_version": _policy_version(policy_payload),
            "builder_name": defaults.get("builder_name", ""),
            "builder_version": defaults.get("builder_version", ""),
            "output_writer_name": OUTPUT_WRITER_NAME,
            "output_writer_version": OUTPUT_WRITER_VERSION,
            "build_timestamp_utc": timestamp,
            "validation_status": validation_status,
            "artifact_count": len(manifest_rows),
            "required_output_count": len(REQUIRED_OUTPUTS),
            "artifacts": manifest_rows,
        },
    )

    return TopologyOutputResult(
        output_dir=out,
        topology_build_id=topology_build_id,
        validation_status=validation_status,
        artifact_paths=artifact_paths,
        checks=tuple(checks),
    )



def _load_policy(policy: str | Path | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(policy, Mapping):
        return dict(policy)
    path = Path(policy)
    return json.loads(path.read_text(encoding="utf-8"))



def _extract_rows(build_result: Any, *names: str) -> list[dict[str, Any]]:
    if isinstance(build_result, Mapping):
        for name in names:
            if name in build_result:
                return _normalize_generic_rows(build_result[name])
    for name in names:
        if hasattr(build_result, name):
            return _normalize_generic_rows(getattr(build_result, name))
    return []



def _normalize_generic_rows(rows: Any) -> list[dict[str, Any]]:
    if rows is None:
        return []
    normalized: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, Mapping):
            normalized.append(dict(row))
        elif is_dataclass(row):
            normalized.append(asdict(row))
        elif hasattr(row, "__dict__"):
            normalized.append(dict(vars(row)))
        else:
            raise TypeError(f"Unsupported row object: {type(row)!r}")
    return normalized



def _normalize_relationship_rows(
    rows: list[dict[str, Any]],
    topology_build_id: str,
    policy: Mapping[str, Any],
) -> list[dict[str, Any]]:
    normalized = []
    input_corpus_generation_id = _input_corpus_generation_id(policy)
    for row in rows:
        out = dict(row)
        out.setdefault("topology_build_id", topology_build_id)
        out.setdefault("input_corpus_generation_id", input_corpus_generation_id)
        out.setdefault("validation_status", VALIDATION_STATUS_PASSED)
        normalized.append(out)
    return sorted(normalized, key=lambda row: _sort_key(row, "topology_relationship_id"))



def _normalize_member_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        out = dict(row)
        out.setdefault("validation_status", VALIDATION_STATUS_PASSED)
        normalized.append(out)
    return sorted(normalized, key=lambda row: (_cell(row.get("topology_relationship_id")), _cell(row.get("member_id"))))



def _normalize_basis_component_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        out = dict(row)
        out.setdefault("validation_status", VALIDATION_STATUS_PASSED)
        normalized.append(out)
    return sorted(normalized, key=lambda row: (_cell(row.get("topology_relationship_id")), _cell(row.get("basis_component_id"))))



def _build_source_identity_expansion_rows(
    relationships: list[dict[str, Any]],
    members: list[dict[str, Any]],
    basis_components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    relationship_by_id = {str(row.get("topology_relationship_id", "")): row for row in relationships}
    basis_by_rel_and_sis: dict[tuple[str, str], dict[str, Any]] = {}
    for basis in basis_components:
        rel_id = _cell(basis.get("topology_relationship_id"))
        sis_id = _cell(basis.get("source_identity_set_id")) or _cell(basis.get("basis_component_reference"))
        if rel_id and sis_id and (rel_id, sis_id) not in basis_by_rel_and_sis:
            basis_by_rel_and_sis[(rel_id, sis_id)] = basis

    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for member in members:
        sis_id = _cell(member.get("source_identity_set_id"))
        if not sis_id:
            continue
        rel_id = _cell(member.get("topology_relationship_id"))
        rel = relationship_by_id.get(rel_id, {})
        basis = basis_by_rel_and_sis.get((rel_id, sis_id), {})
        key = (rel_id, sis_id)
        rows[key] = {
            "topology_build_id": _cell(rel.get("topology_build_id")),
            "topology_relationship_id": rel_id,
            "source_identity_set_id": sis_id,
            "assertion_id": _cell(member.get("source_assertion_id")) or _cell(basis.get("source_assertion_id")),
            "source_assertion_registration_id": _cell(member.get("source_assertion_registration_id")) or _cell(basis.get("source_assertion_registration_id")),
            "registration_unit_id": _cell(member.get("source_registration_unit_id")) or _cell(basis.get("source_registration_unit_id")),
            "identity_kind": _cell(member.get("identity_kind")) or _cell(basis.get("identity_kind")),
            "participant_role": _cell(member.get("participant_role")) or _cell(basis.get("participant_role")),
            "source_namespace": _cell(member.get("source_namespace")) or _cell(basis.get("source_namespace")) or _cell(basis.get("basis_component_namespace")) or _namespace_from_relationship(rel),
            "source_identity_count": _cell(member.get("source_identity_count")) or _cell(basis.get("source_identity_count")),
            "lossiness_status": _cell(member.get("lossiness_status")) or _cell(basis.get("lossiness_status")) or "lossless_by_reference",
            "resolution_status": _cell(member.get("resolution_status")) or _cell(basis.get("resolution_status")),
            "source_identity_set_status": _cell(member.get("source_identity_set_status")) or _cell(basis.get("source_identity_set_status")),
            "source_identity_expansion_status": _cell(rel.get("source_identity_expansion_status")) or "available_by_source_identity_set_reference",
            "statistical_testing_status": _cell(rel.get("statistical_testing_status")) or "requires_source_identity_expansion",
            "validation_status": _cell(member.get("validation_status")) or _cell(rel.get("validation_status")) or VALIDATION_STATUS_PASSED,
        }
    return sorted(rows.values(), key=lambda row: (_cell(row.get("topology_relationship_id")), _cell(row.get("source_identity_set_id"))))




def _build_declaration_set_expansion_rows(
    relationships: list[dict[str, Any]],
    members: list[dict[str, Any]],
    basis_components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    relationship_by_id = {str(row.get("topology_relationship_id", "")): row for row in relationships}
    basis_by_rel_and_set: dict[tuple[str, str], dict[str, Any]] = {}
    for basis in basis_components:
        rel_id = _cell(basis.get("topology_relationship_id"))
        component_type = _cell(basis.get("basis_component_type"))
        if component_type not in {"coordinate_declaration_set_reference", "feature_declaration_set_reference"}:
            continue
        declaration_set_id = _cell(basis.get("basis_component_reference"))
        if rel_id and declaration_set_id and (rel_id, declaration_set_id) not in basis_by_rel_and_set:
            basis_by_rel_and_set[(rel_id, declaration_set_id)] = basis

    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for member in members:
        declaration_set_id = _cell(member.get("declaration_set_id"))
        if not declaration_set_id:
            continue
        rel_id = _cell(member.get("topology_relationship_id"))
        rel = relationship_by_id.get(rel_id, {})
        basis = basis_by_rel_and_set.get((rel_id, declaration_set_id), {})
        key = (rel_id, declaration_set_id)
        rows[key] = {
            "topology_build_id": _cell(rel.get("topology_build_id")),
            "topology_relationship_id": rel_id,
            "declaration_set_type": _cell(member.get("declaration_set_type")),
            "declaration_set_id": declaration_set_id,
            "assertion_id": _cell(member.get("source_assertion_id")) or _cell(basis.get("source_assertion_id")),
            "source_assertion_registration_id": _cell(member.get("source_assertion_registration_id")),
            "registration_unit_id": _cell(member.get("source_registration_unit_id")) or _cell(basis.get("source_registration_unit_id")),
            "declaration_table_reference": _cell(member.get("declaration_table_reference")),
            "declaration_filter": _cell(member.get("declaration_filter")),
            "declaration_count": _cell(member.get("declaration_count")) or _cell(basis.get("basis_component_value")),
            "declaration_kind": _cell(member.get("declaration_kind")),
            "declaration_namespace": _cell(member.get("declaration_namespace")) or _cell(basis.get("basis_component_namespace")),
            "relationship_type": _cell(member.get("declaration_relationship_type")),
            "reference_genome_build": _cell(member.get("declaration_reference_genome_build")),
            "source_artifact_path": _cell(member.get("declaration_source_artifact_path")),
            "lossiness_status": _cell(member.get("declaration_lossiness_status")) or _cell(basis.get("lossiness_status")) or "lossless_by_reference",
            "resolution_status": _cell(member.get("declaration_resolution_status")) or _cell(basis.get("resolution_status")),
            "declaration_set_status": _cell(member.get("declaration_set_status")),
            "declaration_expansion_status": _cell(member.get("declaration_expansion_status")) or "available_by_declaration_set_reference",
            "statistical_testing_status": _cell(rel.get("statistical_testing_status")) or "requires_declaration_expansion",
            "validation_status": _cell(member.get("validation_status")) or _cell(rel.get("validation_status")) or VALIDATION_STATUS_PASSED,
        }
    return sorted(rows.values(), key=lambda row: (_cell(row.get("topology_relationship_id")), _cell(row.get("declaration_set_id"))))


def _build_namespace_mediation_rows(
    relationships: list[dict[str, Any]],
    members: list[dict[str, Any]],
    basis_components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_namespace_by_rel: dict[str, set[str]] = defaultdict(set)
    for row in members + basis_components:
        rel_id = _cell(row.get("topology_relationship_id"))
        namespace = _cell(row.get("source_namespace")) or _cell(row.get("basis_component_namespace"))
        if rel_id and namespace:
            source_namespace_by_rel[rel_id].add(namespace)

    rows = []
    for rel in relationships:
        status = _cell(rel.get("namespace_mediation_status")) or "not_applicable"
        if status == "not_applicable" and _cell(rel.get("relationship_kind")) != "source_identity_set_role_namespace_membership":
            continue
        rel_id = _cell(rel.get("topology_relationship_id"))
        namespaces = sorted(source_namespace_by_rel.get(rel_id, set()))
        namespace_summary = ";".join(namespaces) or _namespace_from_relationship(rel)
        match_type = "source_namespace_match" if status == "source_namespace_only" else "not_applicable"
        rows.append(
            {
                "topology_build_id": _cell(rel.get("topology_build_id")),
                "topology_relationship_id": rel_id,
                "relationship_family_id": _cell(rel.get("relationship_family_id")),
                "namespace_mediation_status": status,
                "match_type": match_type,
                "source_namespace_summary": namespace_summary,
                "canonical_identity_id": "",
                "namespace_bridge_id": "",
                "namespace_policy_status": "canonical_identity_matching_disabled_v1" if status == "source_namespace_only" else "not_applicable",
                "validation_status": _cell(rel.get("validation_status")) or VALIDATION_STATUS_PASSED,
            }
        )
    return sorted(rows, key=lambda row: (_cell(row.get("topology_relationship_id")), _cell(row.get("namespace_mediation_status"))))



def _build_metadata_relationship_rows(relationships: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metadata_dimensions = {
        "metadata",
        "corpus_generation",
        "registration_unit",
        "producer",
        "relationship",
    }
    metadata_rows = []
    for row in relationships:
        dimension = _cell(row.get("topology_dimension"))
        scope = _cell(row.get("relationship_scope"))
        kind = _cell(row.get("relationship_kind"))
        if dimension in metadata_dimensions or scope in {"metadata", "metadata_membership"} or kind.endswith("_membership"):
            metadata_rows.append(dict(row))
    return sorted(metadata_rows, key=lambda row: _sort_key(row, "topology_relationship_id"))



def _build_downstream_geometry_rows(relationships: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for rel in relationships:
        expansion_status = _cell(rel.get("source_identity_expansion_status"))
        statistical_status = _cell(rel.get("statistical_testing_status"))
        scope = _cell(rel.get("relationship_scope"))
        dimension = _cell(rel.get("topology_dimension"))

        if statistical_status == "requires_source_identity_expansion" or expansion_status == "requires_controlled_expansion":
            geometry_status = "requires_controlled_expansion_before_exact_geometry"
            note = "Topology relationship preserves expansion handles; exact geometry requiring source identity values is deferred."
        elif scope in {"metadata", "metadata_membership"} or dimension in {"metadata", "corpus_generation", "registration_unit"}:
            geometry_status = "metadata_context_only"
            note = "Metadata topology is available as context for downstream geometry characterization."
        else:
            geometry_status = "available_for_geometry_characterization"
            note = "Topology relationship may be characterized by downstream Convergence Geometry without implying surface eligibility."

        rows.append(
            {
                "topology_build_id": _cell(rel.get("topology_build_id")),
                "topology_relationship_id": _cell(rel.get("topology_relationship_id")),
                "relationship_family_id": _cell(rel.get("relationship_family_id")),
                "topology_dimension": _cell(rel.get("topology_dimension")),
                "relationship_kind": _cell(rel.get("relationship_kind")),
                "derivation_basis": _cell(rel.get("derivation_basis")),
                "relationship_scope": _cell(rel.get("relationship_scope")),
                "relationship_classification": _cell(rel.get("relationship_classification")),
                "member_count": _cell(rel.get("member_count")),
                "basis_component_count": _cell(rel.get("basis_component_count")),
                "source_identity_expansion_status": expansion_status,
                "statistical_testing_status": statistical_status,
                "namespace_mediation_status": _cell(rel.get("namespace_mediation_status")),
                "input_corpus_generation_id": _cell(rel.get("input_corpus_generation_id")),
                "geometry_input_status": geometry_status,
                "geometry_boundary_note": note,
            }
        )
    return sorted(rows, key=lambda row: _sort_key(row, "topology_relationship_id"))



def _build_summary_rows(
    *,
    topology_build_id: str,
    policy: Mapping[str, Any],
    relationships: list[dict[str, Any]],
    members: list[dict[str, Any]],
    basis_components: list[dict[str, Any]],
    family_execution_rows: list[dict[str, Any]],
    expansion_rows: list[dict[str, Any]],
    declaration_expansion_rows: list[dict[str, Any]],
    namespace_rows: list[dict[str, Any]],
    metadata_rows: list[dict[str, Any]],
    downstream_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(group: str, key: str, value: Any) -> None:
        rows.append(
            {
                "topology_build_id": topology_build_id,
                "summary_group": group,
                "summary_key": key,
                "summary_value": str(value),
            }
        )

    add("artifact_counts", "relationship_count", len(relationships))
    add("artifact_counts", "member_count", len(members))
    add("artifact_counts", "basis_component_count", len(basis_components))
    add("artifact_counts", "family_execution_count", len(family_execution_rows))
    add("artifact_counts", "source_identity_expansion_index_count", len(expansion_rows))
    add("artifact_counts", "declaration_set_expansion_index_count", len(declaration_expansion_rows))
    add("artifact_counts", "namespace_mediation_row_count", len(namespace_rows))
    add("artifact_counts", "metadata_relationship_count", len(metadata_rows))
    add("artifact_counts", "downstream_geometry_input_count", len(downstream_rows))
    add("policy_counts", "enabled_relationship_family_count", len(policy.get("enabled_relationship_families", [])))
    add("policy_counts", "deferred_relationship_family_count", len(policy.get("deferred_relationship_families", [])))
    add("policy_counts", "prohibited_relationship_family_count", len(policy.get("prohibited_relationship_families", [])))

    for field, group in [
        ("relationship_family_id", "relationships_by_family"),
        ("topology_dimension", "relationships_by_dimension"),
        ("relationship_kind", "relationships_by_kind"),
        ("source_identity_expansion_status", "relationships_by_expansion_status"),
        ("statistical_testing_status", "relationships_by_statistical_testing_status"),
        ("namespace_mediation_status", "relationships_by_namespace_mediation_status"),
    ]:
        for key, count in sorted(Counter(_cell(row.get(field)) or "__EMPTY__" for row in relationships).items()):
            add(group, key, count)

    return rows



def _build_validation_checks(
    *,
    artifact_paths: Mapping[str, Path],
    relationships: list[dict[str, Any]],
    members: list[dict[str, Any]],
    basis_components: list[dict[str, Any]],
    expansion_rows: list[dict[str, Any]],
    declaration_expansion_rows: list[dict[str, Any]],
    namespace_rows: list[dict[str, Any]],
    metadata_rows: list[dict[str, Any]],
    downstream_rows: list[dict[str, Any]],
    family_execution_rows: list[dict[str, Any]],
    policy: Mapping[str, Any],
) -> list[TopologyOutputCheck]:
    checks: list[TopologyOutputCheck] = []

    def add(check_id: str, group: str, passed: bool, message: str, expected: Any = "", observed: Any = "") -> None:
        checks.append(
            TopologyOutputCheck(
                check_id=check_id,
                validation_group=group,
                status=VALIDATION_STATUS_PASSED if passed else VALIDATION_STATUS_FAILED,
                message=message,
                expected=_cell(expected),
                observed=_cell(observed),
            )
        )

    for name in REQUIRED_OUTPUTS:
        path = artifact_paths[name]
        add(
            f"required_output_exists__{name}",
            "artifact_family",
            path.is_file(),
            f"Required topology output exists: {name}",
            "file exists",
            str(path),
        )
        add(
            f"required_output_nonempty__{name}",
            "artifact_family",
            path.is_file() and path.stat().st_size > 0,
            f"Required topology output is non-empty: {name}",
            "non-empty file",
            path.stat().st_size if path.is_file() else "missing",
        )

    relationship_ids = [_cell(row.get("topology_relationship_id")) for row in relationships]
    member_ids = [_cell(row.get("member_id")) for row in members]
    basis_ids = [_cell(row.get("basis_component_id")) for row in basis_components]
    rel_id_set = set(relationship_ids)

    add("relationships_nonempty", "relationship_integrity", bool(relationships), "At least one topology relationship is emitted.", ">0", len(relationships))
    add("relationship_ids_unique", "relationship_integrity", len(relationship_ids) == len(rel_id_set), "Topology relationship IDs are unique.", len(relationship_ids), len(rel_id_set))
    add("member_ids_unique", "relationship_integrity", len(member_ids) == len(set(member_ids)), "Topology member IDs are unique.", len(member_ids), len(set(member_ids)))
    add("basis_component_ids_unique", "relationship_integrity", len(basis_ids) == len(set(basis_ids)), "Topology basis component IDs are unique.", len(basis_ids), len(set(basis_ids)))

    member_rel_ids = {_cell(row.get("topology_relationship_id")) for row in members}
    basis_rel_ids = {_cell(row.get("topology_relationship_id")) for row in basis_components}
    add("all_member_relationship_refs_valid", "relationship_integrity", member_rel_ids <= rel_id_set, "All member rows reference valid topology relationships.", sorted(member_rel_ids - rel_id_set), [])
    add("all_basis_relationship_refs_valid", "relationship_integrity", basis_rel_ids <= rel_id_set, "All basis component rows reference valid topology relationships.", sorted(basis_rel_ids - rel_id_set), [])
    add("every_relationship_has_member", "relationship_integrity", rel_id_set <= member_rel_ids, "Every topology relationship has at least one explicit member.", sorted(rel_id_set - member_rel_ids), [])
    add("every_relationship_has_basis", "relationship_integrity", rel_id_set <= basis_rel_ids, "Every topology relationship has at least one explicit basis component.", sorted(rel_id_set - basis_rel_ids), [])

    enabled_families = {
        _cell(row.get("relationship_family_id"))
        for row in policy.get("enabled_relationship_families", [])
    }
    executed_families = {_cell(row.get("relationship_family_id")) for row in family_execution_rows if _cell(row.get("relationship_family_id"))}
    emitted_families = {_cell(row.get("relationship_family_id")) for row in relationships if _cell(row.get("relationship_family_id"))}
    observed_families = executed_families or emitted_families
    add("enabled_families_accounted", "policy_execution", enabled_families <= observed_families, "Every enabled relationship family is executed or represented in emitted relationships.", sorted(enabled_families), sorted(observed_families))

    source_identity_set_members_present = any(_cell(row.get("source_identity_set_id")) for row in members)
    add("source_identity_expansion_index_emitted", "source_identity_expansion", (not source_identity_set_members_present) or bool(expansion_rows), "Source Identity Set expansion index rows are emitted when source identity set members are present.", ">0 when source identity set members present", len(expansion_rows))
    expanded_values_present = any(_cell(row.get("expanded_source_identity_value")) for row in expansion_rows)
    add("source_identity_values_not_flattened", "source_identity_expansion", not expanded_values_present, "Expansion index does not flatten individual source identity values.", "no expanded_source_identity_value", "present" if expanded_values_present else "absent")

    declaration_set_members_present = any(_cell(row.get("declaration_set_id")) for row in members)
    add("declaration_set_expansion_index_emitted", "declaration_set_expansion", (not declaration_set_members_present) or bool(declaration_expansion_rows), "Declaration Set expansion index rows are emitted when declaration set members are present.", ">0 when declaration sets present", len(declaration_expansion_rows))
    expanded_declaration_values_present = any(_cell(row.get("expanded_declaration_value")) for row in declaration_expansion_rows)
    add("declaration_values_not_flattened", "declaration_set_expansion", not expanded_declaration_values_present, "Declaration expansion index does not flatten individual coordinate or feature declaration values.", "no expanded_declaration_value", "present" if expanded_declaration_values_present else "absent")

    canonical_matches = [row for row in namespace_rows if _cell(row.get("match_type")) == "canonical_identity_match"]
    mediated_matches = [row for row in namespace_rows if _cell(row.get("match_type")) == "namespace_mediated_match"]
    namespace_relevant_relationships = [
        row
        for row in relationships
        if _cell(row.get("namespace_mediation_status")) not in {"", "not_applicable"}
        or _cell(row.get("relationship_kind")) == "source_identity_set_role_namespace_membership"
    ]
    add("namespace_rows_emitted", "namespace_mediation", (not namespace_relevant_relationships) or bool(namespace_rows), "Namespace mediation/status artifact rows are emitted when namespace-relevant relationships exist.", ">0 when namespace-relevant relationships exist", len(namespace_rows))
    add("canonical_namespace_matching_not_emitted_v1", "namespace_mediation", not canonical_matches and not mediated_matches, "v1 namespace output does not emit canonical or namespace-mediated identity matches.", "0 canonical/mediated matches", len(canonical_matches) + len(mediated_matches))

    forbidden_columns = sorted(FORBIDDEN_DOWNSTREAM_GEOMETRY_COLUMNS & set(DOWNSTREAM_GEOMETRY_COLUMNS))
    add("downstream_geometry_manifest_has_no_geometry_features", "downstream_geometry_boundary", not forbidden_columns, "Downstream geometry input manifest contains no geometry feature columns.", "no forbidden columns", forbidden_columns)
    add("downstream_geometry_rows_reference_relationships", "downstream_geometry_boundary", {_cell(row.get("topology_relationship_id")) for row in downstream_rows} <= rel_id_set, "Downstream geometry rows reference valid topology relationships.", "valid relationship refs", sorted({_cell(row.get("topology_relationship_id")) for row in downstream_rows} - rel_id_set))

    return checks



def _build_manifest_rows(
    *,
    topology_build_id: str,
    policy: Mapping[str, Any],
    output_dir: Path,
    artifact_paths: Mapping[str, Path],
    validation_status: str,
    build_timestamp_utc: str,
) -> list[dict[str, Any]]:
    defaults = policy.get("topology_build_defaults", {})
    rows = []
    for name in REQUIRED_OUTPUTS:
        path = artifact_paths[name]
        is_manifest = name in {"topology_build_manifest.tsv", "topology_build_manifest.json"}
        rows.append(
            {
                "topology_build_id": topology_build_id,
                "input_corpus_generation_id": _input_corpus_generation_id(policy),
                "topology_derivation_policy_id": _policy_id(policy),
                "topology_derivation_policy_version": _policy_version(policy),
                "builder_name": defaults.get("builder_name", ""),
                "builder_version": defaults.get("builder_version", ""),
                "build_timestamp_utc": build_timestamp_utc,
                "output_dir": str(output_dir),
                "artifact_name": name,
                "artifact_path": str(path),
                "artifact_role": _artifact_role(name),
                "row_count": _row_count(path),
                "sha256": "self_reference_not_applicable" if is_manifest else _sha256(path),
                "size_bytes": path.stat().st_size if path.is_file() else 0,
                "validation_status": validation_status,
            }
        )
    return rows



def _build_report_markdown(
    *,
    topology_build_id: str,
    policy: Mapping[str, Any],
    output_dir: Path,
    validation_status: str,
    checks: Sequence[TopologyOutputCheck],
    summary_rows: Sequence[Mapping[str, Any]],
    family_execution_rows: Sequence[Mapping[str, Any]],
    timestamp: str,
) -> str:
    failed = [check for check in checks if check.status != VALIDATION_STATUS_PASSED]
    summary_lookup = {
        (_cell(row.get("summary_group")), _cell(row.get("summary_key"))): _cell(row.get("summary_value"))
        for row in summary_rows
    }
    lines = [
        "# Evidence Topology Build Report",
        "",
        "## Build Identity",
        "",
        f"- `topology_build_id`: `{topology_build_id}`",
        f"- `input_corpus_generation_id`: `{_input_corpus_generation_id(policy)}`",
        f"- `topology_derivation_policy_id`: `{_policy_id(policy)}`",
        f"- `topology_derivation_policy_version`: `{_policy_version(policy)}`",
        f"- `build_timestamp_utc`: `{timestamp}`",
        f"- `output_dir`: `{output_dir}`",
        f"- `validation_status`: `{validation_status}`",
        "",
        "## Artifact Counts",
        "",
        f"- relationships: {summary_lookup.get(('artifact_counts', 'relationship_count'), '0')}",
        f"- members: {summary_lookup.get(('artifact_counts', 'member_count'), '0')}",
        f"- basis components: {summary_lookup.get(('artifact_counts', 'basis_component_count'), '0')}",
        f"- source identity expansion index rows: {summary_lookup.get(('artifact_counts', 'source_identity_expansion_index_count'), '0')}",
        f"- declaration set expansion index rows: {summary_lookup.get(('artifact_counts', 'declaration_set_expansion_index_count'), '0')}",
        f"- namespace mediation rows: {summary_lookup.get(('artifact_counts', 'namespace_mediation_row_count'), '0')}",
        f"- downstream geometry input rows: {summary_lookup.get(('artifact_counts', 'downstream_geometry_input_count'), '0')}",
        "",
        "## Relationship Family Execution",
        "",
    ]
    if family_execution_rows:
        for row in family_execution_rows:
            lines.append(
                f"- `{_cell(row.get('relationship_family_id'))}`: "
                f"{_cell(row.get('execution_status')) or 'executed'} "
                f"({ _cell(row.get('relationship_count')) or '0'} relationships)"
            )
    else:
        lines.append("- Family execution rows were not provided; emitted relationships were still serialized and validated.")

    lines.extend(
        [
            "",
            "## Boundary Statements",
            "",
            "- Source Identity Sets are preserved by reference; individual source identity values are not flattened.",
            "- Coordinate and feature declaration sets are preserved by reference; individual declaration values are not flattened.",
            "- Namespace output preserves source namespace state only for v1; canonical namespace mediation is not performed.",
            "- The downstream geometry manifest identifies topology relationships available to Phase 4.5 but emits no Convergence Geometry features.",
            "- This build report is not biological interpretation, statistical testing, Projection View output, or RDGP reasoning.",
            "",
            "## Validation Summary",
            "",
            f"- total checks: {len(checks)}",
            f"- failed checks: {len(failed)}",
        ]
    )
    if failed:
        lines.append("")
        lines.append("### Failed Checks")
        lines.append("")
        for check in failed:
            lines.append(f"- `{check.check_id}`: {check.message} observed={check.observed}")
    return "\n".join(lines) + "\n"



def _write_tsv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _cell(row.get(field, "")) for field in fieldnames})



def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(_json_safe(row), sort_keys=True, separators=(",", ":")) + "\n")



def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")



def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return _json_safe(asdict(value))
    return value



def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if isinstance(value, Mapping):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)



def _sort_key(row: Mapping[str, Any], key: str) -> str:
    return _cell(row.get(key))



def _getattr_or_key(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(key, default)
    return getattr(value, key, default)



def _input_corpus_generation_id(policy: Mapping[str, Any]) -> str:
    return _cell(
        policy.get("topology_build_defaults", {}).get("input_corpus_generation_id")
        or policy.get("policy_identity", {}).get("input_corpus_generation_id")
    )



def _policy_id(policy: Mapping[str, Any]) -> str:
    return _cell(
        policy.get("topology_build_defaults", {}).get("topology_derivation_policy_id")
        or policy.get("policy_identity", {}).get("policy_id")
    )



def _policy_version(policy: Mapping[str, Any]) -> str:
    return _cell(
        policy.get("topology_build_defaults", {}).get("topology_derivation_policy_version")
        or policy.get("policy_identity", {}).get("policy_version")
    )



def _artifact_role(name: str) -> str:
    if name.startswith("topology_build_manifest"):
        return "build_manifest"
    if name.startswith("topology_relationships"):
        return "relationship_index"
    if name == "topology_relationship_members.tsv":
        return "relationship_members"
    if name == "topology_basis_components.tsv":
        return "basis_components"
    if name == "topology_source_identity_expansion_index.tsv":
        return "source_identity_expansion_index"
    if name == "topology_declaration_set_expansion_index.tsv":
        return "declaration_set_expansion_index"
    if name == "topology_namespace_mediation.tsv":
        return "namespace_mediation"
    if name == "topology_metadata_relationships.tsv":
        return "metadata_relationships"
    if name == "topology_summary.tsv":
        return "summary"
    if name.startswith("topology_validation_report"):
        return "build_local_validation_report"
    if name == "topology_build_report.md":
        return "human_readable_build_report"
    if name == "downstream_geometry_input_manifest.tsv":
        return "downstream_geometry_input_manifest"
    return "artifact"



def _row_count(path: Path) -> int:
    if not path.is_file():
        return 0
    if path.suffix == ".jsonl":
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    if path.suffix == ".tsv":
        line_count = sum(1 for _ in path.open("r", encoding="utf-8"))
        return max(0, line_count - 1)
    if path.suffix == ".json":
        return 1
    if path.suffix == ".md":
        return 1
    return 0



def _sha256(path: Path) -> str:
    if not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()



def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def _namespace_from_relationship(rel: Mapping[str, Any]) -> str:
    grouping_key = _cell(rel.get("grouping_key"))
    grouping_value = _cell(rel.get("grouping_value"))
    combined = f"{grouping_key}|{grouping_value}"
    for part in combined.split("|"):
        if part.startswith("source_namespace="):
            return part.split("=", 1)[1]
    return ""

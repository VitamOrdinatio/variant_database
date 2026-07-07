from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CORPUS_ID = os.environ.get("CORPUS_ID", "mark_phase4_corpus_6tep_v1")
TOPOLOGY_BUILD_ID = os.environ.get("TOPOLOGY_BUILD_ID", "mark_phase4_corpus_6tep_v1_topology_build_v1")
AUDIT_ID = os.environ.get("AUDIT_ID", f"{CORPUS_ID}_compact_vdb_audit_v1")
OUT_DIR = Path(os.environ.get("OUT_DIR", f"results/phase4/namespace_audit/{AUDIT_ID}"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

AR_DIR = Path("results/phase4/assertion_records") / CORPUS_ID
TOPO_DIR = Path("results/phase4/evidence_topology") / TOPOLOGY_BUILD_ID
MANIFEST_DIR = Path("docs/manifests/corpus_generation")
PHASE4_DIR = Path("results/phase4")

REQUIRED_EXPANSION_HANDLE_FIELDS = [
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

REQUIRED_SOURCE_IDENTITY_SET_FIELDS = [
    "source_identity_set_id",
    "assertion_id",
    "source_assertion_registration_id",
    "identity_kind",
    "participant_role",
    "source_namespace",
    "source_identity_count",
    "lossiness_status",
    "resolution_status",
    "source_identity_set_status",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames or []), rows


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def nonempty(value: Any) -> bool:
    return bool(str(value or "").strip())


def intish(value: Any) -> int:
    text = str(value or "").strip()
    try:
        return int(text)
    except ValueError:
        return 0


def classify_producer(row: dict[str, str]) -> str:
    values = " ".join(str(row.get(k, "")) for k in ("source_namespace", "source_corpus_generation_id", "source_assertion_registration_id", "registration_unit_id", "assertion_id"))
    lower = values.lower()
    if "vap" in lower:
        return "VAP"
    if "gsc" in lower:
        return "GSC"
    if "rsp" in lower:
        return "RSP"
    return "unknown"


def classify_route(row: dict[str, str]) -> tuple[str, str]:
    namespace = str(row.get("source_namespace", "")).lower()
    identity_kind = str(row.get("identity_kind", "")).lower()
    role = str(row.get("participant_role", "")).lower()

    text = " ".join([namespace, identity_kind, role])
    if any(token in text for token in ["variant", "coordinate", "locus", "allele"]):
        return (
            "default_coordinate_or_variant_brokerage",
            "Variant/coordinate-like identity must remain first-class; value-level coordinate trace requires MARK if compact output only preserves handles.",
        )
    if any(token in text for token in ["transcript", "exon", "intron", "utr", "regulatory", "feature", "interval"]):
        return (
            "feature_brokerage",
            "Feature-like identity should remain distinct from gene identity and coordinate identity.",
        )
    if any(token in text for token in ["ensembl_gene", "gene_symbol", "source_gene", "gene_id", "gene"]):
        return (
            "gene_brokerage",
            "Gene identity is a routed specialization; source namespace and producer context must remain visible.",
        )
    if any(token in text for token in ["phenotype", "disease"]):
        return (
            "phenotype_or_overlay_brokerage",
            "Phenotype/overlay context must remain scoped and should not collapse into gene identity.",
        )
    if any(token in text for token in ["sample", "run", "release", "source", "provenance", "semantic_channel", "corpus", "registration"]):
        return (
            "producer_or_observation_brokerage",
            "Producer/observation identity supplies scope and provenance for evidence interpretation.",
        )
    return ("unknown_or_deferred", "Route could not be classified from compact namespace fields alone.")


def table_profile(stage: str, role: str, path: Path) -> dict[str, Any]:
    fields, rows = read_tsv(path)
    return {
        "stage": stage,
        "artifact_role": role,
        "artifact_path": str(path),
        "exists": str(path.exists()).lower(),
        "row_count": len(rows),
        "column_count": len(fields),
        "columns": ",".join(fields),
        "sha256": sha256(path) if path.exists() and path.is_file() else "",
        "audit_status": "present" if path.exists() else "missing",
    }


def check_nonempty(rows: list[dict[str, str]], fields: list[str], row_filter=lambda r: True) -> tuple[bool, dict[str, int]]:
    considered = [r for r in rows if row_filter(r)]
    missing_by_field = {}
    ok = True
    for field in fields:
        missing = sum(1 for r in considered if not nonempty(r.get(field)))
        missing_by_field[field] = missing
        if considered and missing:
            ok = False
    return ok, missing_by_field


def status_from_bool(ok: bool, warning: bool = False) -> str:
    if ok and not warning:
        return "passed"
    if ok and warning:
        return "warning"
    return "error"


def emit_file_inventory() -> list[dict[str, Any]]:
    known_files = [
        ("phase4_2_corpus_generation", "corpus_selection_manifest", MANIFEST_DIR / f"{CORPUS_ID}_selection_manifest.tsv"),
        ("phase4_3_assertion_records", "assertion_record_index", AR_DIR / "assertion_record_index.tsv"),
        ("phase4_3_assertion_records", "assertion_record_participants", AR_DIR / "assertion_record_participants.tsv"),
        ("phase4_3_assertion_records", "assertion_record_source_identity_sets", AR_DIR / "assertion_record_source_identity_sets.tsv"),
        ("phase4_3_assertion_records", "assertion_record_source_identity_summary", AR_DIR / "assertion_record_source_identity_summary.tsv"),
        ("phase4_4_evidence_topology", "topology_relationships", TOPO_DIR / "topology_relationships.tsv"),
        ("phase4_4_evidence_topology", "topology_relationship_members", TOPO_DIR / "topology_relationship_members.tsv"),
        ("phase4_4_evidence_topology", "topology_basis_components", TOPO_DIR / "topology_basis_components.tsv"),
        ("phase4_4_evidence_topology", "topology_source_identity_expansion_index", TOPO_DIR / "topology_source_identity_expansion_index.tsv"),
        ("phase4_4_evidence_topology", "topology_namespace_mediation", TOPO_DIR / "topology_namespace_mediation.tsv"),
        ("phase4_4_evidence_topology", "downstream_geometry_input_manifest", TOPO_DIR / "downstream_geometry_input_manifest.tsv"),
    ]
    return [table_profile(stage, role, path) for stage, role, path in known_files]


def emit_namespace_inventory(tables: list[tuple[str, str, Path]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for stage, role, path in tables:
        fields, rows = read_tsv(path)
        if not rows:
            continue
        namespace_like = [f for f in fields if "namespace" in f]
        for namespace_col in namespace_like:
            groups: dict[tuple[str, str, str, str], dict[str, Any]] = {}
            for row in rows:
                namespace = row.get(namespace_col, "")
                identity_kind = row.get("identity_kind", "")
                participant_role = row.get("participant_role", "")
                route, note = classify_route({**row, "source_namespace": namespace})
                key = (namespace, identity_kind, participant_role, route)
                if key not in groups:
                    groups[key] = {
                        "stage": stage,
                        "artifact_role": role,
                        "artifact_path": str(path),
                        "namespace_column": namespace_col,
                        "source_namespace": namespace,
                        "identity_kind": identity_kind,
                        "participant_role": participant_role,
                        "identity_route": route,
                        "row_count": 0,
                        "source_identity_count_total": 0,
                        "empty_namespace_rows": 0,
                        "audit_note": note,
                    }
                groups[key]["row_count"] += 1
                groups[key]["source_identity_count_total"] += intish(row.get("source_identity_count"))
                if not nonempty(namespace):
                    groups[key]["empty_namespace_rows"] += 1
            out.extend(groups.values())
    return sorted(out, key=lambda r: (r["stage"], r["artifact_role"], r["namespace_column"], r["source_namespace"], r["identity_kind"], r["participant_role"]))


def emit_source_identity_set_lifecycle(
    source_sets: list[dict[str, str]],
    source_summary: list[dict[str, str]],
    expansion: list[dict[str, str]],
) -> list[dict[str, Any]]:
    summary_by_sis = defaultdict(list)
    for row in source_summary:
        summary_by_sis[row.get("source_identity_set_id", "")].append(row)

    expansion_by_sis = defaultdict(list)
    for row in expansion:
        expansion_by_sis[row.get("source_identity_set_id", "")].append(row)

    rows_out: list[dict[str, Any]] = []
    for sis in source_sets:
        sid = sis.get("source_identity_set_id", "")
        route, route_note = classify_route(sis)
        producer = classify_producer(sis)
        exp_rows = expansion_by_sis.get(sid, [])
        required_ok, missing_required = check_nonempty(exp_rows, REQUIRED_EXPANSION_HANDLE_FIELDS)
        sis_ok, sis_missing = check_nonempty([sis], REQUIRED_SOURCE_IDENTITY_SET_FIELDS)
        summary_count = len(summary_by_sis.get(sid, []))
        status = "passed_compact_handle_preserved"
        notes = []
        if not sis_ok:
            status = "error_source_identity_set_incomplete"
            notes.append("Source Identity Set required fields incomplete: " + json.dumps(sis_missing, sort_keys=True))
        if not exp_rows:
            status = "error_missing_topology_expansion_handle"
            notes.append("Source Identity Set is absent from topology expansion index.")
        elif not required_ok:
            status = "error_topology_expansion_handle_incomplete"
            notes.append("Expansion required fields incomplete: " + json.dumps(missing_required, sort_keys=True))
        if route == "default_coordinate_or_variant_brokerage":
            notes.append("Tier 1 proves compact handle survival only; coordinate value provenance must be deep-traced on MARK.")
        if route == "gene_brokerage":
            notes.append("Tier 1 proves compact gene handle survival only; gene value/bridge provenance may require MARK/producer artifact trace.")
        if summary_count == 0:
            notes.append("No source identity summary row found for this Source Identity Set.")

        rows_out.append({
            "source_identity_set_id": sid,
            "producer": producer,
            "identity_route": route,
            "participant_role": sis.get("participant_role", ""),
            "identity_kind": sis.get("identity_kind", ""),
            "source_namespace": sis.get("source_namespace", ""),
            "assertion_id": sis.get("assertion_id", ""),
            "source_assertion_registration_id": sis.get("source_assertion_registration_id", ""),
            "source_identity_table_reference": sis.get("source_identity_table_reference", ""),
            "source_identity_filter": sis.get("source_identity_filter", ""),
            "source_identity_count": sis.get("source_identity_count", ""),
            "lossiness_status": sis.get("lossiness_status", ""),
            "resolution_status": sis.get("resolution_status", ""),
            "source_identity_set_status": sis.get("source_identity_set_status", ""),
            "summary_row_count": summary_count,
            "topology_expansion_row_count": len(exp_rows),
            "expansion_required_fields_complete": str(required_ok).lower() if exp_rows else "false",
            "source_identity_set_required_fields_complete": str(sis_ok).lower(),
            "audit_status": status,
            "audit_note": " ".join(notes) if notes else route_note,
        })
    return sorted(rows_out, key=lambda r: (r["producer"], r["identity_route"], r["source_namespace"], r["source_identity_set_id"]))


def emit_route_inventory(lifecycle_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in lifecycle_rows:
        key = (row["producer"], row["identity_route"])
        if key not in groups:
            groups[key] = {
                "producer": row["producer"],
                "identity_route": row["identity_route"],
                "source_identity_set_rows": 0,
                "represented_source_identity_count": 0,
                "topology_expansion_rows": 0,
                "source_namespaces": set(),
                "audit_statuses": Counter(),
                "requires_mark_deep_trace": "false",
                "audit_note": "",
            }
        g = groups[key]
        g["source_identity_set_rows"] += 1
        g["represented_source_identity_count"] += intish(row.get("source_identity_count"))
        g["topology_expansion_rows"] += intish(row.get("topology_expansion_row_count"))
        g["source_namespaces"].add(row.get("source_namespace", ""))
        g["audit_statuses"][row.get("audit_status", "")] += 1
        if row["identity_route"] in {"default_coordinate_or_variant_brokerage", "gene_brokerage", "feature_brokerage"}:
            g["requires_mark_deep_trace"] = "true"

    out = []
    for g in groups.values():
        statuses = dict(g.pop("audit_statuses"))
        g["source_namespaces"] = ";".join(sorted(ns for ns in g["source_namespaces"] if ns))
        g["audit_status_summary"] = json.dumps(statuses, sort_keys=True)
        if any(k.startswith("error") for k in statuses):
            g["audit_status"] = "error"
        else:
            g["audit_status"] = "passed_tier1_compact_handles"
        notes = []
        if g["requires_mark_deep_trace"] == "true":
            notes.append("Tier 1 validates compact handle survival; MARK is required for value-level TEP/SQLite provenance.")
        if g["identity_route"] == "default_coordinate_or_variant_brokerage":
            notes.append("Coordinate/variant route must be deep-traced to confirm reference-build/contig/start/end/ref/alt substrate.")
        if g["identity_route"] == "gene_brokerage":
            notes.append("Gene route must be deep-traced to confirm gene_id/gene_namespace/bridge provenance where available.")
        g["audit_note"] = " ".join(notes)
        out.append(g)
    return sorted(out, key=lambda r: (r["producer"], r["identity_route"]))


def emit_join_audit(
    assertion_index: list[dict[str, str]],
    participants: list[dict[str, str]],
    source_sets: list[dict[str, str]],
    source_summary: list[dict[str, str]],
    relationships: list[dict[str, str]],
    members: list[dict[str, str]],
    basis: list[dict[str, str]],
    expansion: list[dict[str, str]],
    namespace_mediation: list[dict[str, str]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, group: str, status: str, message: str, expected: Any = "", observed: Any = "", earliest_gap_stage: str = "", recommended_fix_layer: str = ""):
        checks.append({
            "check_id": check_id,
            "validation_group": group,
            "status": status,
            "message": message,
            "expected": expected,
            "observed": observed,
            "earliest_gap_stage": earliest_gap_stage,
            "recommended_fix_layer": recommended_fix_layer,
        })

    assertion_ids = {r.get("assertion_id", "") for r in assertion_index if nonempty(r.get("assertion_id"))}
    source_set_ids = {r.get("source_identity_set_id", "") for r in source_sets if nonempty(r.get("source_identity_set_id"))}
    relationship_ids = {r.get("topology_relationship_id", "") for r in relationships if nonempty(r.get("topology_relationship_id"))}

    add("artifact_assertion_index_present", "artifact_presence", "passed" if assertion_index else "error", "Assertion Record index is present and nonempty.", ">0", len(assertion_index), "phase4_3_assertion_records", "assertion_record_emission")
    add("artifact_source_identity_sets_present", "artifact_presence", "passed" if source_sets else "error", "Assertion Record Source Identity Sets are present and nonempty.", ">0", len(source_sets), "phase4_3_assertion_records", "assertion_record_source_identity_set_emission")
    add("artifact_topology_expansion_present", "artifact_presence", "passed" if expansion else "error", "Topology Source Identity expansion index is present and nonempty.", ">0", len(expansion), "phase4_4_evidence_topology", "evidence_topology_output_emission")

    invalid_participant_assertions = sum(1 for r in participants if nonempty(r.get("assertion_id")) and r.get("assertion_id") not in assertion_ids)
    add("participant_assertion_refs_valid", "join_integrity", "passed" if invalid_participant_assertions == 0 else "error", "Participant assertion_id references resolve to assertion_record_index.", 0, invalid_participant_assertions, "phase4_3_assertion_records", "assertion_record_participant_projection")

    invalid_sis_assertions = sum(1 for r in source_sets if nonempty(r.get("assertion_id")) and r.get("assertion_id") not in assertion_ids)
    add("source_identity_set_assertion_refs_valid", "join_integrity", "passed" if invalid_sis_assertions == 0 else "error", "Source Identity Set assertion_id references resolve to assertion_record_index.", 0, invalid_sis_assertions, "phase4_3_assertion_records", "assertion_record_source_identity_set_projection")

    invalid_summary_sis = sum(1 for r in source_summary if nonempty(r.get("source_identity_set_id")) and r.get("source_identity_set_id") not in source_set_ids)
    add("source_identity_summary_refs_valid", "join_integrity", "passed" if invalid_summary_sis == 0 else "error", "Source identity summary source_identity_set_id references resolve to Source Identity Sets.", 0, invalid_summary_sis, "phase4_3_assertion_records", "assertion_record_source_identity_summary")

    invalid_member_relationships = sum(1 for r in members if nonempty(r.get("topology_relationship_id")) and r.get("topology_relationship_id") not in relationship_ids)
    add("topology_member_relationship_refs_valid", "join_integrity", "passed" if invalid_member_relationships == 0 else "error", "Topology member relationship references resolve to topology_relationships.", 0, invalid_member_relationships, "phase4_4_evidence_topology", "evidence_topology_member_emission")

    invalid_basis_relationships = sum(1 for r in basis if nonempty(r.get("topology_relationship_id")) and r.get("topology_relationship_id") not in relationship_ids)
    add("topology_basis_relationship_refs_valid", "join_integrity", "passed" if invalid_basis_relationships == 0 else "error", "Topology basis relationship references resolve to topology_relationships.", 0, invalid_basis_relationships, "phase4_4_evidence_topology", "evidence_topology_basis_emission")

    invalid_expansion_relationships = sum(1 for r in expansion if nonempty(r.get("topology_relationship_id")) and r.get("topology_relationship_id") not in relationship_ids)
    add("expansion_relationship_refs_valid", "join_integrity", "passed" if invalid_expansion_relationships == 0 else "error", "Expansion index relationship references resolve to topology_relationships.", 0, invalid_expansion_relationships, "phase4_4_evidence_topology", "evidence_topology_expansion_index_emission")

    invalid_expansion_sis = sum(1 for r in expansion if nonempty(r.get("source_identity_set_id")) and r.get("source_identity_set_id") not in source_set_ids)
    add("expansion_source_identity_set_refs_valid", "join_integrity", "passed" if invalid_expansion_sis == 0 else "error", "Expansion index source_identity_set_id references resolve to Assertion Record Source Identity Sets.", 0, invalid_expansion_sis, "phase4_4_evidence_topology", "evidence_topology_expansion_index_emission")

    sis_required_ok, sis_missing = check_nonempty(source_sets, REQUIRED_SOURCE_IDENTITY_SET_FIELDS)
    add("source_identity_set_required_fields_nonempty", "handle_preservation", "passed" if sis_required_ok else "error", "Required Source Identity Set handle fields are nonempty.", "all required fields nonempty", json.dumps(sis_missing, sort_keys=True), "phase4_3_assertion_records", "assertion_record_source_identity_set_emission")

    expansion_required_ok, expansion_missing = check_nonempty(expansion, REQUIRED_EXPANSION_HANDLE_FIELDS)
    add("expansion_required_fields_nonempty", "handle_preservation", "passed" if expansion_required_ok else "error", "Required topology expansion handle fields are nonempty.", "all required fields nonempty", json.dumps(expansion_missing, sort_keys=True), "phase4_4_evidence_topology", "evidence_topology_expansion_index_emission")

    unique_expansion_sis = {r.get("source_identity_set_id", "") for r in expansion if nonempty(r.get("source_identity_set_id"))}
    source_count_by_sis = {r.get("source_identity_set_id", ""): intish(r.get("source_identity_count")) for r in source_sets}
    represented_total = sum(source_count_by_sis.get(sid, 0) for sid in unique_expansion_sis)
    all_sis_represented = unique_expansion_sis == source_set_ids
    add("expansion_unique_source_identity_sets_preserved", "handle_preservation", "passed" if all_sis_represented else "error", "Expansion index represents the same unique Source Identity Sets as Assertion Records.", len(source_set_ids), len(unique_expansion_sis), "phase4_4_evidence_topology", "evidence_topology_expansion_index_emission")
    add("expansion_unique_represented_source_identity_count", "handle_preservation", "passed" if represented_total > 0 else "error", "Expansion index preserves represented source identity count by unique Source Identity Set handle.", ">0", represented_total, "phase4_4_evidence_topology", "evidence_topology_expansion_index_emission")

    route_counts = Counter(classify_route(r)[0] for r in source_sets)
    add("coordinate_or_variant_route_observed", "route_inventory", "passed" if route_counts.get("default_coordinate_or_variant_brokerage", 0) else "warning", "At least one coordinate/variant route Source Identity Set is observed in compact Assertion Records.", ">0", route_counts.get("default_coordinate_or_variant_brokerage", 0), "phase4_3_assertion_records", "namespace_route_classification_or_upstream_ingestion")
    add("gene_route_observed", "route_inventory", "passed" if route_counts.get("gene_brokerage", 0) else "warning", "At least one gene route Source Identity Set is observed in compact Assertion Records.", ">0", route_counts.get("gene_brokerage", 0), "phase4_3_assertion_records", "namespace_route_classification_or_upstream_ingestion")
    add("producer_or_context_route_observed", "route_inventory", "passed" if (route_counts.get("producer_or_observation_brokerage", 0) or route_counts.get("phenotype_or_overlay_brokerage", 0)) else "warning", "At least one producer/context route Source Identity Set is observed in compact Assertion Records.", ">0", route_counts.get("producer_or_observation_brokerage", 0) + route_counts.get("phenotype_or_overlay_brokerage", 0), "phase4_3_assertion_records", "namespace_route_classification_or_upstream_ingestion")

    canonical_nonempty = sum(1 for r in namespace_mediation if nonempty(r.get("canonical_identity_id")))
    bridge_nonempty = sum(1 for r in namespace_mediation if nonempty(r.get("namespace_bridge_id")))
    add("namespace_mediation_no_unsupported_canonical_ids", "namespace_mediation_boundary", "passed" if canonical_nonempty == 0 else "warning", "Tier 1 expects no unsupported canonical_identity_id in conservative topology outputs.", 0, canonical_nonempty, "phase4_4_evidence_topology", "namespace_mediation_policy_or_topology_output")
    add("namespace_mediation_no_unsupported_bridge_ids", "namespace_mediation_boundary", "passed" if bridge_nonempty == 0 else "warning", "Tier 1 expects no unsupported namespace_bridge_id in conservative topology outputs.", 0, bridge_nonempty, "phase4_4_evidence_topology", "namespace_mediation_policy_or_topology_output")

    return checks


def choose_sentinel_candidates(lifecycle_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Select a compact, deterministic set of handle-level sentinels per producer/route/namespace.
    grouped = defaultdict(list)
    for row in lifecycle_rows:
        key = (row.get("producer", ""), row.get("identity_route", ""), row.get("source_namespace", ""))
        grouped[key].append(row)

    candidates = []
    priority_namespaces = {
        "vap_variant_id": 1,
        "vap_ensembl_gene_id": 2,
        "vap_gene_symbol": 3,
        "vap_sample_id": 4,
        "gsc_ensembl_gene_id": 5,
        "gsc_source_gene_id": 6,
        "gsc_gene_symbol": 7,
        "gsc_phenotype": 8,
        "gsc_source_id": 9,
        "gsc_provenance_id": 10,
        "gsc_semantic_channel": 11,
    }

    for key in sorted(grouped, key=lambda k: (priority_namespaces.get(k[2], 999), k)):
        rows = sorted(grouped[key], key=lambda r: (intish(r.get("source_identity_count")), r.get("source_identity_set_id", "")))
        # Choose one smallest and one largest per group when distinct.
        selected = []
        if rows:
            selected.append(rows[0])
        if len(rows) > 1 and rows[-1].get("source_identity_set_id") != rows[0].get("source_identity_set_id"):
            selected.append(rows[-1])
        for idx, row in enumerate(selected, start=1):
            requires_mark = row.get("identity_route") in {"default_coordinate_or_variant_brokerage", "gene_brokerage", "feature_brokerage"}
            candidates.append({
                "sentinel_rank_within_group": idx,
                "producer": row.get("producer", ""),
                "identity_route": row.get("identity_route", ""),
                "source_namespace": row.get("source_namespace", ""),
                "source_identity_set_id": row.get("source_identity_set_id", ""),
                "assertion_id": row.get("assertion_id", ""),
                "source_assertion_registration_id": row.get("source_assertion_registration_id", ""),
                "source_identity_table_reference": row.get("source_identity_table_reference", ""),
                "source_identity_filter": row.get("source_identity_filter", ""),
                "source_identity_count": row.get("source_identity_count", ""),
                "topology_expansion_row_count": row.get("topology_expansion_row_count", ""),
                "tier1_status": row.get("audit_status", ""),
                "requires_mark_deep_trace": str(requires_mark).lower(),
                "mark_trace_question": mark_trace_question(row),
            })
    return candidates


def mark_trace_question(row: dict[str, Any]) -> str:
    route = row.get("identity_route", "")
    ns = row.get("source_namespace", "")
    if route == "default_coordinate_or_variant_brokerage":
        return f"On MARK, trace {ns} through TEP/SQLite to confirm reference build, contig, start/end or pos, ref, alt, variant type, and observation context."
    if route == "gene_brokerage":
        return f"On MARK, trace {ns} through TEP/SQLite to confirm source gene value, declared namespace, identifier-map or adapter-resolution provenance, and release/phenotype scope when applicable."
    if route == "feature_brokerage":
        return f"On MARK, trace {ns} through TEP/SQLite to confirm feature interval/source annotation provenance."
    if route == "phenotype_or_overlay_brokerage":
        return f"On MARK if needed, trace {ns} to confirm phenotype/release/source scope remains attached to gene or overlay evidence."
    if route == "producer_or_observation_brokerage":
        return f"On MARK if needed, trace {ns} to confirm producer/run/sample/source/provenance scope remains attached."
    return f"On MARK, inspect {ns} source rows to classify route and preservation state."


def write_report(
    path: Path,
    manifest: list[dict[str, Any]],
    route_inventory: list[dict[str, Any]],
    join_audit: list[dict[str, Any]],
    sentinel_candidates: list[dict[str, Any]],
) -> None:
    status_counts = Counter(row["status"] for row in join_audit)
    route_status_counts = Counter(row["audit_status"] for row in route_inventory)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = []
    lines.append("# Tier 1 Namespace Provenance Audit — Compact VDB Artifacts")
    lines.append("")
    lines.append(f"audit_id: `{AUDIT_ID}`")
    lines.append(f"corpus_id: `{CORPUS_ID}`")
    lines.append(f"topology_build_id: `{TOPOLOGY_BUILD_ID}`")
    lines.append(f"generated_utc: `{now}`")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This Tier 1 audit inspects compact VDB Phase 4 artifacts available on sys76.")
    lines.append("It validates handle-level namespace substrate preservation from Phase 4.3 Assertion Records through Phase 4.4 Evidence Topology Step 7.")
    lines.append("It does not inspect MARK-only TEP payloads or registration SQLite value-level substrates.")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("Passed Tier 1 checks mean compact handles survived.")
    lines.append("They do not prove value-level coordinate, feature, or gene bridge provenance; MARK deep traces are required for those questions.")
    lines.append("")
    lines.append("## Artifact Inventory")
    lines.append("")
    for row in manifest:
        lines.append(f"- `{row['artifact_role']}`: {row['audit_status']} ({row['row_count']} rows) — `{row['artifact_path']}`")
    lines.append("")
    lines.append("## Join / Preservation Check Summary")
    lines.append("")
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    failing = [row for row in join_audit if row["status"] in {"error", "critical"}]
    if failing:
        lines.append("### Errors / Critical Findings")
        lines.append("")
        for row in failing:
            lines.append(f"- `{row['check_id']}`: {row['status']} — {row['message']} observed={row['observed']}")
        lines.append("")
    else:
        lines.append("No error or critical join/preservation findings were detected in Tier 1 compact artifacts.")
        lines.append("")
    lines.append("## Route Inventory Summary")
    lines.append("")
    for row in route_inventory:
        lines.append(
            f"- {row['producer']} / {row['identity_route']}: "
            f"{row['source_identity_set_rows']} Source Identity Sets; "
            f"represented_source_identity_count={row['represented_source_identity_count']}; "
            f"namespaces=`{row['source_namespaces']}`; "
            f"status={row['audit_status']}"
        )
    lines.append("")
    lines.append("## Sentinel Candidates For Tier 2 MARK Trace")
    lines.append("")
    lines.append("The candidates below are handle-level representatives selected from compact artifacts. They are intended to guide MARK-side TEP/SQLite deep provenance tracing.")
    lines.append("")
    for row in sentinel_candidates[:40]:
        lines.append(
            f"- `{row['source_namespace']}` / `{row['source_identity_set_id']}` "
            f"({row['producer']}, {row['identity_route']}, count={row['source_identity_count']}): "
            f"{row['mark_trace_question']}"
        )
    lines.append("")
    lines.append("## Tier 1 Verdict")
    lines.append("")
    if failing:
        lines.append("Tier 1 detected compact-artifact errors. Apply the provenance principle: locate and patch the earliest broken layer before fixing downstream symptoms.")
    else:
        lines.append("Tier 1 compact artifacts preserve the tested namespace handles and joins. Proceed to Tier 2 MARK deep trace for value-level TEP and SQLite provenance.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    assertion_index_fields, assertion_index = read_tsv(AR_DIR / "assertion_record_index.tsv")
    participant_fields, participants = read_tsv(AR_DIR / "assertion_record_participants.tsv")
    sis_fields, source_sets = read_tsv(AR_DIR / "assertion_record_source_identity_sets.tsv")
    summary_fields, source_summary = read_tsv(AR_DIR / "assertion_record_source_identity_summary.tsv")
    relationship_fields, relationships = read_tsv(TOPO_DIR / "topology_relationships.tsv")
    member_fields, members = read_tsv(TOPO_DIR / "topology_relationship_members.tsv")
    basis_fields, basis = read_tsv(TOPO_DIR / "topology_basis_components.tsv")
    expansion_fields, expansion = read_tsv(TOPO_DIR / "topology_source_identity_expansion_index.tsv")
    namespace_fields, namespace_mediation = read_tsv(TOPO_DIR / "topology_namespace_mediation.tsv")

    manifest = emit_file_inventory()
    namespace_inventory = emit_namespace_inventory([
        ("phase4_3_assertion_records", "assertion_record_participants", AR_DIR / "assertion_record_participants.tsv"),
        ("phase4_3_assertion_records", "assertion_record_source_identity_sets", AR_DIR / "assertion_record_source_identity_sets.tsv"),
        ("phase4_3_assertion_records", "assertion_record_source_identity_summary", AR_DIR / "assertion_record_source_identity_summary.tsv"),
        ("phase4_4_evidence_topology", "topology_source_identity_expansion_index", TOPO_DIR / "topology_source_identity_expansion_index.tsv"),
        ("phase4_4_evidence_topology", "topology_namespace_mediation", TOPO_DIR / "topology_namespace_mediation.tsv"),
    ])
    lifecycle_rows = emit_source_identity_set_lifecycle(source_sets, source_summary, expansion)
    route_inventory = emit_route_inventory(lifecycle_rows)
    join_audit = emit_join_audit(assertion_index, participants, source_sets, source_summary, relationships, members, basis, expansion, namespace_mediation)
    sentinel_candidates = choose_sentinel_candidates(lifecycle_rows)

    write_tsv(OUT_DIR / "compact_artifact_inventory.tsv", manifest, [
        "stage", "artifact_role", "artifact_path", "exists", "row_count", "column_count", "columns", "sha256", "audit_status"
    ])
    write_tsv(OUT_DIR / "compact_namespace_inventory.tsv", namespace_inventory, [
        "stage", "artifact_role", "artifact_path", "namespace_column", "source_namespace", "identity_kind", "participant_role", "identity_route", "row_count", "source_identity_count_total", "empty_namespace_rows", "audit_note"
    ])
    write_tsv(OUT_DIR / "source_identity_set_lifecycle.tsv", lifecycle_rows, [
        "source_identity_set_id", "producer", "identity_route", "participant_role", "identity_kind", "source_namespace", "assertion_id", "source_assertion_registration_id", "source_identity_table_reference", "source_identity_filter", "source_identity_count", "lossiness_status", "resolution_status", "source_identity_set_status", "summary_row_count", "topology_expansion_row_count", "expansion_required_fields_complete", "source_identity_set_required_fields_complete", "audit_status", "audit_note"
    ])
    write_tsv(OUT_DIR / "identity_route_inventory.tsv", route_inventory, [
        "producer", "identity_route", "source_identity_set_rows", "represented_source_identity_count", "topology_expansion_rows", "source_namespaces", "audit_status_summary", "requires_mark_deep_trace", "audit_status", "audit_note"
    ])
    write_tsv(OUT_DIR / "compact_lifecycle_join_audit.tsv", join_audit, [
        "check_id", "validation_group", "status", "message", "expected", "observed", "earliest_gap_stage", "recommended_fix_layer"
    ])
    write_tsv(OUT_DIR / "sentinel_candidates_for_mark_trace.tsv", sentinel_candidates, [
        "sentinel_rank_within_group", "producer", "identity_route", "source_namespace", "source_identity_set_id", "assertion_id", "source_assertion_registration_id", "source_identity_table_reference", "source_identity_filter", "source_identity_count", "topology_expansion_row_count", "tier1_status", "requires_mark_deep_trace", "mark_trace_question"
    ])
    write_report(OUT_DIR / "compact_namespace_audit_report.md", manifest, route_inventory, join_audit, sentinel_candidates)

    # Machine-readable summary for quick downstream parsing.
    summary = {
        "audit_id": AUDIT_ID,
        "corpus_id": CORPUS_ID,
        "topology_build_id": TOPOLOGY_BUILD_ID,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "output_dir": str(OUT_DIR),
        "artifact_count": 6,
        "join_audit_status_counts": dict(Counter(row["status"] for row in join_audit)),
        "route_inventory_status_counts": dict(Counter(row["audit_status"] for row in route_inventory)),
        "source_identity_set_count": len(source_sets),
        "topology_expansion_row_count": len(expansion),
        "unique_expansion_source_identity_sets": len({r.get("source_identity_set_id", "") for r in expansion if nonempty(r.get("source_identity_set_id"))}),
        "unique_represented_source_identity_count": sum(intish(row.get("source_identity_count")) for row in source_sets),
        "tier1_verdict": "passed_compact_handle_audit" if not any(row["status"] in {"error", "critical"} for row in join_audit) else "failed_compact_handle_audit",
    }
    (OUT_DIR / "compact_namespace_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Tier 1 compact VDB namespace audit complete")
    print(f"  audit_id: {AUDIT_ID}")
    print(f"  output_dir: {OUT_DIR}")
    print(f"  tier1_verdict: {summary['tier1_verdict']}")
    print(f"  join_audit_status_counts: {summary['join_audit_status_counts']}")
    print(f"  source_identity_set_count: {summary['source_identity_set_count']}")
    print(f"  unique_represented_source_identity_count: {summary['unique_represented_source_identity_count']}")
    print("  report:", OUT_DIR / "compact_namespace_audit_report.md")


if __name__ == "__main__":
    main()

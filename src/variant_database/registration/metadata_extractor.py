"""Package metadata extraction for VDB registration.

This module extracts producer execution metadata that is transported inside a
TEP package. It preserves package context only.

It does not register scientific evidence.
It does not perform namespace resolution.
It does not interpret biology.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from variant_database.persistence.repositories import stable_hash


VAP_CONFIG_SNAPSHOT_RELATIVE_PATH = "entities/metadata/config_snapshot.yaml"


RUN_ID_PATTERN = re.compile(r"(run_\d{4}_\d{2}_\d{2}_\d{6})")


def derive_run_id_from_tep_path(package_path: str) -> tuple[str | None, str]:
    """Derive a VAP run_id from a TEP package path when the config omits it."""
    match = RUN_ID_PATTERN.search(Path(package_path).name)
    if match:
        return match.group(1), "tep_package_path_regex"

    match = RUN_ID_PATTERN.search(package_path)
    if match:
        return match.group(1), "tep_package_path_regex"

    return None, "not_observed"


def package_metadata_id_for_record(
    package_id: str,
    metadata_artifact_path: str,
    metadata_artifact_sha256: str,
) -> str:
    """Derive a deterministic package metadata ID."""
    return stable_hash(
        [
            "package_metadata",
            package_id,
            metadata_artifact_path,
            metadata_artifact_sha256,
        ]
    )


def _nested(config: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = config
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _bool_or_none(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "on"}:
            return 1
        if normalized in {"false", "no", "0", "off"}:
            return 0
    return None


def _load_yaml_config(path: Path) -> tuple[dict[str, Any], str, str | None]:
    """Load config YAML and return config, parse status, and optional error."""
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - exact parser errors are YAML-specific
        return {}, "parse_error", str(exc)

    if loaded is None:
        return {}, "parsed_empty"

    if not isinstance(loaded, dict):
        return {"_raw_config_value": loaded}, "parsed_non_mapping", None

    return loaded, "parsed", None


def build_vap_package_metadata_record(
    package_id: str,
    package_path: str,
    artifact_records: list[dict[str, object]],
) -> dict[str, object] | None:
    """Build a VAP package metadata record from entities/metadata/config_snapshot.yaml.

    The config snapshot is package metadata, not scientific evidence. If the
    package does not contain the snapshot, no record is emitted.
    """
    metadata_artifact = None
    for artifact_record in artifact_records:
        if str(artifact_record["relative_path"]) == VAP_CONFIG_SNAPSHOT_RELATIVE_PATH:
            metadata_artifact = artifact_record
            break

    if metadata_artifact is None:
        return None

    metadata_artifact_path = str(metadata_artifact["relative_path"])
    metadata_artifact_sha256 = str(metadata_artifact["sha256"])
    metadata_artifact_id = str(metadata_artifact["artifact_id"])

    config_path = Path(package_path) / metadata_artifact_path
    config, metadata_parse_status, parse_error = _load_yaml_config(config_path)

    run_id, run_id_derivation_method = derive_run_id_from_tep_path(package_path)

    vep_config = _nested(config, ("tools", "vep"))
    if not isinstance(vep_config, dict):
        vep_config = {}

    annotation_engine = _string_or_none(_nested(config, ("annotation", "engine")))
    if annotation_engine is None and vep_config:
        annotation_engine = "vep"

    annotation_assembly = _string_or_none(_nested(config, ("annotation", "assembly")))
    if annotation_assembly is None:
        annotation_assembly = _string_or_none(vep_config.get("assembly"))

    payload = {
        "metadata_source": metadata_artifact_path,
        "metadata_role": "package_metadata",
        "metadata_parse_status": metadata_parse_status,
        "parse_error": parse_error,
        "config_snapshot": config,
    }

    package_metadata_id = package_metadata_id_for_record(
        package_id=package_id,
        metadata_artifact_path=metadata_artifact_path,
        metadata_artifact_sha256=metadata_artifact_sha256,
    )

    return {
        "package_metadata_id": package_metadata_id,
        "package_id": package_id,
        "metadata_artifact_id": metadata_artifact_id,
        "metadata_role": "package_metadata",
        "metadata_artifact_path": metadata_artifact_path,
        "metadata_artifact_sha256": metadata_artifact_sha256,
        "metadata_format": "yaml",
        "run_id": run_id,
        "run_id_derivation_method": run_id_derivation_method,
        "sample_id": _string_or_none(_nested(config, ("input", "sample_id"))),
        "sample_alias": _string_or_none(_nested(config, ("input", "sample_alias"))),
        "sra_accession": _string_or_none(_nested(config, ("input", "sra_accession"))),
        "assay_type": _string_or_none(_nested(config, ("input", "assay_type"))),
        "project_name": _string_or_none(_nested(config, ("project", "name"))),
        "pipeline_name": _string_or_none(_nested(config, ("project", "pipeline_name"))),
        "pipeline_version": _string_or_none(_nested(config, ("project", "version"))),
        "execution_profile_name": _string_or_none(_nested(config, ("execution_profile", "name"))),
        "hardware_class": _string_or_none(_nested(config, ("execution_profile", "hardware_class"))),
        "reference_genome_build": _string_or_none(_nested(config, ("reference", "genome_build"))),
        "reference_fasta_path": _string_or_none(_nested(config, ("reference", "fasta_path"))),
        "reference_fasta_index_path": _string_or_none(_nested(config, ("reference", "fasta_index"))),
        "reference_sequence_dictionary_path": _string_or_none(_nested(config, ("reference", "sequence_dictionary"))),
        "annotation_engine": annotation_engine,
        "annotation_assembly": annotation_assembly,
        "annotation_cache_dir": _string_or_none(vep_config.get("cache_dir")),
        "deterministic_mode": _bool_or_none(_nested(config, ("runtime", "deterministic_mode"))),
        "record_tool_versions": _bool_or_none(_nested(config, ("runtime", "record_tool_versions"))),
        "metadata_parse_status": metadata_parse_status,
        "payload_json": json.dumps(payload, sort_keys=True),
    }

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re


ROOT = Path(".")
INVENTORY_DIR = ROOT / "_notes/AI_assistance/inventory"
OUT = INVENTORY_DIR / "step5_authoring_input_manifest.md"

GLOBAL_INPUTS = [
    "_notes/AI_assistance/inventory/vdb_architectural_synthesis.md",
    "_notes/AI_assistance/inventory/source_doctrine_inventory.md",
    "_notes/AI_assistance/inventory/INVENTORY_governance.md",
    "_notes/AI_assistance/inventory/INVENTORY_template.md",
    "docs/NAMESPACE.md",
    "docs/README.md",
]

STEP5_TARGETS = [
    "docs/architecture/architecture.md",
    "docs/architecture/ecosystem_layer_model.md",
    "docs/architecture/interoperability_topology.md",
    "docs/architecture/namespace_authority_model.md",
    "docs/architecture/evidence_persistence_philosophy.md",

    "docs/design/ingestion_orchestration_design.md",
    "docs/design/namespace_resolution_engine_design.md",
    "docs/design/query_surface_design.md",

    "docs/interfaces/vap_vdb_interface.md",
    "docs/interfaces/gsc_vdb_interface.md",
    "docs/interfaces/vdb_rdgp_interface.md",
    "docs/interfaces/rsp_vdb_interface.md",

    "docs/implementation/workflow/workflow.md",

    "docs/implementation/specifications/artifact_manifest_spec.md",
    "docs/implementation/specifications/ingestion_event_spec.md",
    "docs/implementation/specifications/provenance_spec.md",
    "docs/implementation/specifications/namespace_resolution_spec.md",
    "docs/implementation/specifications/discovery_report_spec.md",
    "docs/implementation/specifications/tep_spec.md",

    "docs/implementation/schemas/data_schema.md",
    "docs/implementation/schemas/metadata_schema.md",
    "docs/implementation/schemas/provenance_schema.md",
    "docs/implementation/schemas/relational_schema.md",
    "docs/implementation/schemas/discovery_schema.md",
    "docs/implementation/schemas/rdgp_query_surface_schema.md",

    "docs/validation/validation_strategy.md",
    "docs/validation/schema_validation.md",
    "docs/validation/ingestion_validation.md",
    "docs/validation/namespace_resolution_validation.md",
]


@dataclass(frozen=True)
class Hit:
    file_path: Path
    line_no: int
    line_text: str
    match_type: str


def exists(path: str | Path) -> str:
    return "OK" if (ROOT / path).exists() else "MISSING"


def inventory_files() -> list[Path]:
    return sorted(INVENTORY_DIR.glob("inventory_*.md"))


def target_patterns(target: str) -> list[tuple[str, re.Pattern[str]]]:
    """
    Match explicit references to a target path.

    We include variants because inventory records sometimes omit the leading docs/.
    Example:
        docs/architecture/architecture.md
        architecture/architecture.md
    """
    no_docs = target.removeprefix("docs/")
    basename = Path(target).name

    variants = [
        target,
        no_docs,
    ]

    # For root-ish targets this can duplicate, so dedupe while preserving order.
    variants = list(dict.fromkeys(variants))

    return [
        (
            variant,
            re.compile(rf"(?<![\w./-]){re.escape(variant)}(?![\w./-])"),
        )
        for variant in variants
    ]


def find_hits_for_target(target: str) -> list[Hit]:
    patterns = target_patterns(target)
    hits: list[Hit] = []

    for file_path in inventory_files():
        text = file_path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            for label, pattern in patterns:
                if pattern.search(line):
                    hits.append(
                        Hit(
                            file_path=file_path,
                            line_no=idx,
                            line_text=line.strip(),
                            match_type=f"explicit:{label}",
                        )
                    )
                    break

    return hits


def unique_hit_files(hits: list[Hit]) -> list[Path]:
    return sorted({hit.file_path for hit in hits})


def format_path(path: Path | str) -> str:
    p = Path(path)
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def main() -> None:
    lines: list[str] = []
    missing_any = False
    no_hits: list[str] = []

    lines.append("# Step 5 Authoring Input Manifest")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This manifest derives target-specific authoring inputs by scanning "
        "inventory records for explicit references to each Step 5 target document."
    )
    lines.append("")
    lines.append("The script does not hardcode inventory-to-target mappings.")
    lines.append("")
    lines.append("Input classes:")
    lines.append("")
    lines.append("- `global`: governance/context files applied to every target")
    lines.append("- `derived`: inventory files that explicitly name the target document")
    lines.append("")
    lines.append("## Global Inputs")
    lines.append("")

    for path in GLOBAL_INPUTS:
        status = exists(path)
        if status == "MISSING":
            missing_any = True
        lines.append(f"- [{status}] `{path}`")
    lines.append("")

    lines.append("## Target-Specific Inputs")
    lines.append("")

    for target in STEP5_TARGETS:
        hits = find_hits_for_target(target)
        hit_files = unique_hit_files(hits)

        if not hits:
            no_hits.append(target)

        lines.append(f"### `{target}`")
        lines.append("")
        lines.append("Global inputs:")
        for path in GLOBAL_INPUTS:
            status = exists(path)
            if status == "MISSING":
                missing_any = True
            lines.append(f"- [{status}] `{path}`")
        lines.append("")

        lines.append("Derived inventory inputs:")
        if hit_files:
            for path in hit_files:
                status = exists(path)
                if status == "MISSING":
                    missing_any = True
                lines.append(f"- [{status}] `{format_path(path)}`")
        else:
            lines.append("- [NO_EXPLICIT_HIT] No inventory record explicitly names this target.")
        lines.append("")

        lines.append("Evidence lines:")
        if hits:
            for hit in hits:
                rel = format_path(hit.file_path)
                lines.append(
                    f"- `{rel}:{hit.line_no}` "
                    f"({hit.match_type}) — {hit.line_text}"
                )
        else:
            lines.append("- None")
        lines.append("")

    lines.append("## Audit Summary")
    lines.append("")
    lines.append(f"- Targets: {len(STEP5_TARGETS)}")
    lines.append(f"- Inventory records scanned: {len(inventory_files())}")
    lines.append(f"- Missing files detected: {'YES' if missing_any else 'NO'}")
    lines.append(f"- Targets with no explicit inventory hit: {len(no_hits)}")
    lines.append("")

    if no_hits:
        lines.append("### Targets with No Explicit Inventory Hit")
        lines.append("")
        for target in no_hits:
            lines.append(f"- `{target}`")
        lines.append("")
        lines.append(
            "These targets require either updated inventory records, "
            "manual justification, or intentional deferral."
        )
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Targets: {len(STEP5_TARGETS)}")
    print(f"Inventory records scanned: {len(inventory_files())}")
    print(f"Missing files detected: {'YES' if missing_any else 'NO'}")
    print(f"Targets with no explicit inventory hit: {len(no_hits)}")


if __name__ == "__main__":
    main()
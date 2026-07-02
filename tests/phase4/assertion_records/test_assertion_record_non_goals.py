"""Layer 1 tests for Phase 4.3 non-goals and mutation safeguards."""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.phase4.assertion_records.helpers.builder_imports import import_required
from tests.phase4.assertion_records.helpers.synthetic_registration_units import (
    build_layer1_synthetic_corpus,
    sha256_file,
)

pytestmark = pytest.mark.phase4_3_layer1

PROHIBITED_OUTPUT_NAME_FRAGMENTS = {
    "evidence_topology",
    "convergence_geometry",
    "evidence_convergence_surface",
    "projection_view",
    "rdgp",
}


def _run_builder(builder_module, *, manifest_path: Path, output_dir: Path, corpus_generation_id: str):
    if hasattr(builder_module, "build_assertion_records_from_manifest"):
        return builder_module.build_assertion_records_from_manifest(
            manifest_path=manifest_path,
            output_dir=output_dir,
            corpus_generation_id=corpus_generation_id,
        )
    if hasattr(builder_module, "build_assertion_records"):
        return builder_module.build_assertion_records(
            manifest_path=manifest_path,
            output_dir=output_dir,
            corpus_generation_id=corpus_generation_id,
        )
    pytest.fail(
        "builder module must expose build_assertion_records_from_manifest(...) "
        "or build_assertion_records(...)"
    )


def test_builder_does_not_mutate_synthetic_registration_units(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    before = {ru_id: sha256_file(path) for ru_id, path in corpus.registration_unit_paths.items()}

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    after = {ru_id: sha256_file(path) for ru_id, path in corpus.registration_unit_paths.items()}
    assert before == after


def test_builder_does_not_emit_topology_geometry_surface_projection_or_rdgp_outputs(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    _run_builder(
        builder,
        manifest_path=corpus.manifest_path,
        output_dir=corpus.output_dir,
        corpus_generation_id=corpus.corpus_generation_id,
    )

    emitted_names = [path.name for path in corpus.output_dir.rglob("*") if path.is_file()]
    prohibited = [
        name
        for name in emitted_names
        for fragment in PROHIBITED_OUTPUT_NAME_FRAGMENTS
        if fragment in name
    ]
    assert not prohibited, "builder emitted prohibited downstream authority outputs: " + ", ".join(prohibited)


def test_builder_requires_manifest_and_corpus_generation_identity(tmp_path: Path) -> None:
    builder = import_required("builder")
    corpus = build_layer1_synthetic_corpus(tmp_path)

    with pytest.raises((ValueError, FileNotFoundError, TypeError)):
        _run_builder(
            builder,
            manifest_path=tmp_path / "missing_manifest.tsv",
            output_dir=corpus.output_dir,
            corpus_generation_id=corpus.corpus_generation_id,
        )

    with pytest.raises((ValueError, TypeError)):
        _run_builder(
            builder,
            manifest_path=corpus.manifest_path,
            output_dir=corpus.output_dir,
            corpus_generation_id="",
        )

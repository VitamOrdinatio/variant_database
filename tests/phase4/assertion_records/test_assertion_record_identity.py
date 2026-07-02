"""Layer 1 tests for Phase 4.3 Assertion Record identity invariants."""
from __future__ import annotations

import pytest

from tests.phase4.assertion_records.helpers.builder_imports import import_required

pytestmark = pytest.mark.phase4_3_layer1


def test_source_assertion_key_is_stable_and_source_scoped() -> None:
    identity = import_required("identity")

    make_source_assertion_key = getattr(identity, "make_source_assertion_key")

    key_1 = make_source_assertion_key(
        registration_unit_id="synthetic_vap_registration_unit",
        source_package_id="synthetic_vap_package_001",
        source_artifact_id="vap_artifact_observation_001",
        source_assertion_registration_id="vap_variant_observation_001",
        assertion_type="variant_observation",
        producer_family="VAP",
    )
    key_2 = make_source_assertion_key(
        registration_unit_id="synthetic_vap_registration_unit",
        source_package_id="synthetic_vap_package_001",
        source_artifact_id="vap_artifact_observation_001",
        source_assertion_registration_id="vap_variant_observation_001",
        assertion_type="variant_observation",
        producer_family="VAP",
    )
    key_3 = make_source_assertion_key(
        registration_unit_id="synthetic_vap_registration_unit",
        source_package_id="synthetic_vap_package_001",
        source_artifact_id="vap_artifact_observation_001",
        source_assertion_registration_id="vap_variant_observation_002",
        assertion_type="variant_observation",
        producer_family="VAP",
    )

    assert key_1
    assert key_1 == key_2
    assert key_1 != key_3


def test_assertion_id_is_stable_and_corpus_indexed() -> None:
    identity = import_required("identity")

    make_source_assertion_key = getattr(identity, "make_source_assertion_key")
    make_assertion_id = getattr(identity, "make_assertion_id")

    source_key = make_source_assertion_key(
        registration_unit_id="synthetic_gsc_registration_unit",
        source_package_id="synthetic_gsc_package_001",
        source_artifact_id="gsc_artifact_semantic_prior_001",
        source_assertion_registration_id="gsc_phenotype_gene_semantic_prior_001",
        assertion_type="phenotype_gene_semantic_prior",
        producer_family="GSC",
    )

    assertion_id_1 = make_assertion_id(
        corpus_generation_id="synthetic_phase4_3_layer1_corpus_v1",
        registration_unit_id="synthetic_gsc_registration_unit",
        source_assertion_key=source_key,
        assertion_type="phenotype_gene_semantic_prior",
        producer_family="GSC",
    )
    assertion_id_2 = make_assertion_id(
        corpus_generation_id="synthetic_phase4_3_layer1_corpus_v1",
        registration_unit_id="synthetic_gsc_registration_unit",
        source_assertion_key=source_key,
        assertion_type="phenotype_gene_semantic_prior",
        producer_family="GSC",
    )
    assertion_id_other_corpus = make_assertion_id(
        corpus_generation_id="synthetic_phase4_3_layer1_corpus_v2",
        registration_unit_id="synthetic_gsc_registration_unit",
        source_assertion_key=source_key,
        assertion_type="phenotype_gene_semantic_prior",
        producer_family="GSC",
    )

    assert assertion_id_1
    assert assertion_id_1 == assertion_id_2
    assert assertion_id_1 != assertion_id_other_corpus


def test_assertion_id_changes_when_registration_unit_changes() -> None:
    identity = import_required("identity")

    make_assertion_id = getattr(identity, "make_assertion_id")

    assertion_id_1 = make_assertion_id(
        corpus_generation_id="synthetic_phase4_3_layer1_corpus_v1",
        registration_unit_id="synthetic_vap_registration_unit",
        source_assertion_key="source-key-constant",
        assertion_type="variant_observation",
        producer_family="VAP",
    )
    assertion_id_2 = make_assertion_id(
        corpus_generation_id="synthetic_phase4_3_layer1_corpus_v1",
        registration_unit_id="other_synthetic_vap_registration_unit",
        source_assertion_key="source-key-constant",
        assertion_type="variant_observation",
        producer_family="VAP",
    )

    assert assertion_id_1 != assertion_id_2

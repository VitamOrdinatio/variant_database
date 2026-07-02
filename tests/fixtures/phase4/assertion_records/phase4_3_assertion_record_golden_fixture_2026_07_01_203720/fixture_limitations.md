# Fixture Limitations

This is a MARK-derived candidate package for a compressed Layer 2 golden fixture.
It does not contain full production-scale source_identity tables.
It preserves source identity recoverability through deterministic slices, summaries, and set candidate filters.
Expected Assertion Record output snapshots are placeholders until the builder emits draft outputs and DEX review accepts them.
The package does not create production Assertion Records, derive topology, emit projections, or perform RDGP reasoning.

---

# Sys76 Curation Patch Notes

**Curation timestamp:** 2026-07-02T03:59:54Z

This fixture candidate was curated on sys76 after MARK acquisition.

Applied curation corrections:

```text
source_identity_filter values were strengthened to include partition predicates:
    assertion_registration_id
    identity_kind
    participant_role
    source_namespace

required Registration Unit presence warnings caused by logical-name / canonical-id aliasing were resolved when selected Registration Units mapped to the expected logical units.

GSC producer_contract_validation assertion registrations without attached source_identity rows were accounted as not_applicable source identity set cases.

checksums/file_manifest.sha256 was regenerated after curation.
```

Curation summary:

```json
{
  "curation_timestamp_utc": "2026-07-02T03:59:54Z",
  "extracted_root": "/tmp/phase4_3_fixture_curation_cy48092r/phase4_3_assertion_record_golden_fixture_2026_07_01_203720",
  "required_registration_unit_alias_warnings_patched": 6,
  "source_identity_filter_files_patched": 7,
  "source_identity_filter_rows_patched": 408,
  "source_identity_not_applicable_assertions_added": 2,
  "source_tgz": "/home/steelsparrow/Downloads/phase4_3_assertion_record_golden_fixture_2026_07_01_203720.tgz",
  "source_tgz_sha256_expected": "48175792ec2120dc57172aad57efb8e0804c3e6b5ad5f1d9670a715a03ddacc0",
  "source_tgz_sha256_observed": "48175792ec2120dc57172aad57efb8e0804c3e6b5ad5f1d9670a715a03ddacc0"
}
```


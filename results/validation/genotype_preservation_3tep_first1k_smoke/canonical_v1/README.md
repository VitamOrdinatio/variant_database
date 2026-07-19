# Genotype First-1K Source-Order Preservation Smoke — Canonical Evidence

This directory preserves the canonical compact validation receipts for the
ERR10619300 first-1K source-order genotype-preservation smoke.

The smoke selects the first 1,000 producer rows deterministically in source
order. It validates bounded streaming, lossless raw-value preservation,
producer-identity retention, scope persistence, and validation receipt
generation.

This substrate is not the representative 3TEP 1K candidate or golden fixture.
It does not establish representative biological or structural coverage.

The SQLite validation database is intentionally not committed. Its identity,
the complete local evidence archive identity, and the identities of these
canonical receipts are recorded in `SHA256SUMS`.

Validated result:

- selected rows: 1,000
- preserved rows: 1,000
- unique genotype observation identifiers: 1,000
- preserved producer columns: 68
- validation checks: 44
- failed checks: 0
- mixed-corpus preservation exercised: false
- externally validated maturity: genotype_preservation_validated
- persisted package maturity before receipt binding: genotype_discovered

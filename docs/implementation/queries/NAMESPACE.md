# Queries Namespace

Namespace: `docs/implementation/queries/`

**Queries = Stable retrieval surfaces**

> Core question:
> What query outputs does VDB expose to downstream systems?

Examples:

- rdgp_surface_query.md
- sample_gene_evidence_query.md
- overlay_attachment_query.md
- provenance_audit_query.md

Query documents answer:

1. What information can be retrieved?
2. How is information exposed?
3. What retrieval surfaces exist?
4. How do downstream systems access evidence?

Queries are:

- retrieval-oriented
- consumer-facing
- stable
- interoperability-aware

> Principle:
> Query documents define stable retrieval surfaces and downstream
> access patterns.

> Anti-pattern:
> Query documents should not become persistence schemas,
> storage policy documents, or downstream reasoning logic.

# VDB Namespace Brokerage Justification

## Purpose

This document explains why the Variant Database (VDB) implements namespace brokerage rather than namespace replacement.

The purpose of this document is to justify the identity management philosophy of the repository and explain why identity preservation is treated as a first-class architectural requirement.

This document does not define namespace resolution algorithms.

This document explains why namespace brokerage exists.

---

# Executive Summary

Modern biological evidence originates from many independent systems.

Each system introduces its own identifiers, naming conventions, authority structures, and identity assumptions.

Examples include:

```text
Ensembl

HGNC

NCBI

ClinVar

dbSNP

VAP

GSC

RSP

RDGP
```

These systems are not incorrect.

They are simply optimized for different purposes.

The purpose of VDB is therefore not to eliminate those identities.

The purpose of VDB is to preserve and relate them.

---

# The Traditional Approach

Many systems attempt to solve identity complexity through normalization.

Conceptually:

```text
Source Identity
        ↓
Normalization
        ↓
Canonical Identity
        ↓
Discard Original Identity
```

This approach simplifies implementation.

However, it introduces important risks.

Examples include:

```text
loss of provenance

loss of historical context

loss of authority information

loss of ambiguity

loss of future reinterpretation capability
```

VDB intentionally rejects this approach.

---

# Identity Is Evidence

One of the central assumptions of VDB is:

```text
Identity is evidence.
```

Identifiers are not merely implementation details.

Identifiers encode:

```text
authority

historical context

producer intent

biological context

semantic meaning
```

Discarding identities therefore discards information.

---

# Producer Repositories Are Authorities

Each producer repository owns identities within its own domain.

Examples:

```text
VAP
    run identifiers

VAP
    sample-level evidence identities

GSC
    semantic prior identities

GSC
    release identities

RDGP
    reasoning identities

RSP
    transcriptomic evidence identities
```

Producer-generated identities are authoritative within producer-defined contexts.

VDB should not overwrite those identities.

---

# Authority Is Distributed

The ecosystem intentionally embraces distributed authority.

Examples:

```text
HGNC
    symbol authority

Ensembl
    gene identifier authority

ClinVar
    clinical interpretation authority

VAP
    observational evidence authority

GSC
    semantic prior authority
```

No single system owns all biological identities.

VDB therefore acts as a broker among authorities rather than attempting to become the authority itself.

---

# Why Brokerage Exists

Namespace brokerage exists because interoperability requires relationships.

Interoperability does not require identity replacement.

Consider:

```text
SCN1A

ENSG00000144285

NCBIGene:6323
```

These identifiers are related.

They are not identical.

The goal is therefore:

```text
connect identities

without erasing identities
```

Namespace brokerage achieves this objective.

---

# The VDB Brokerage Model

Conceptually:

```text
Source Identity
        ↓
Namespace Brokerage
        ↓
Relationship Layer
        ↓
Canonical Reference Layer
        ↓
Discovery
```

The brokerage layer creates relationships.

The brokerage layer does not destroy source identity.

---

# Why Canonical Identity Still Exists

VDB may assign canonical identities.

Canonical identities provide:

```text
stable references

cross-repository linkage

query simplification

persistence stability
```

However:

```text
canonical identity
    ≠
source identity
```

Canonical identities exist to facilitate interoperability.

They do not invalidate original identities.

---

# Unresolved Identities Are Valuable

Many systems treat unresolved identifiers as failures.

VDB intentionally rejects this assumption.

Examples include:

```text
novel variants

novel genes

future evidence classes

emerging ontologies

repository-specific identifiers
```

An unresolved identity may still represent valid evidence.

Therefore:

```text
unresolved
    ≠
invalid
```

Preservation of unresolved identities is essential for future-proofing.

---

# Ambiguity Is Information

Ambiguous mappings are often treated as implementation problems.

VDB treats ambiguity as evidence.

Examples include:

```text
historical aliases

deprecated identifiers

multiple plausible mappings

ontology transitions
```

These conditions communicate uncertainty.

Removing ambiguity destroys information.

Therefore:

```text
ambiguity should be preserved

not hidden
```

whenever possible.

---

# Future Discovery Depends Upon Identity Preservation

Many future discoveries will emerge from relationships that are not obvious today.

Examples may include:

```text
new phenotype relationships

new gene relationships

new regulatory relationships

new evidence classes
```

If identities are discarded during ingestion, those future relationships may become impossible to reconstruct.

Identity preservation therefore protects future discovery opportunities.

---

# Future Reinterpretation Depends Upon Identity Preservation

Scientific understanding evolves continuously.

New resources may eventually resolve identities that are currently:

```text
unknown

ambiguous

partially resolved

deferred
```

Preserving original identities allows future systems to revisit those questions.

Replacing identities prematurely may prevent reinterpretation.

---

# Clinical Motivation

Clinical interpretation often occurs over long time horizons.

A future clinician may need to understand:

```text
what identifier was originally observed

what authority assigned it

what mappings existed at the time

what mappings exist now
```

Namespace brokerage preserves this history.

Identity replacement destroys it.

---

# Relationship To TEPs

Transitional Evidence Products (TEPs) preserve source identities during transport.

Examples include:

```text
sample identifiers

gene identifiers

variant identifiers

run identifiers

release identifiers

package identifiers
```

Namespace brokerage continues that preservation philosophy after ingestion.

TEPs preserve identities during transport.

VDB preserves identities during persistence.

These are complementary responsibilities.

---

# Relationship To Persistence

Persistence without identity preservation is incomplete.

Evidence that cannot be related back to its source identity loses context.

Namespace brokerage therefore serves as a critical component of the persistence mission.

Persistence preserves evidence.

Brokerage preserves relationships among evidence identities.

---

# Tradeoffs

Namespace brokerage introduces complexity.

Examples include:

```text
identity lineage tracking

authority tracking

mapping maintenance

ambiguity management

resolution provenance
```

These costs are accepted intentionally.

The repository prioritizes long-term interpretability over short-term simplification.

---

# Why VDB Is Not A Namespace Authority

VDB stores and relates evidence.

VDB does not define biological nomenclature.

VDB does not define external authority systems.

Instead:

```text
VDB preserves

VDB relates

VDB brokers
```

Authority remains with authoritative sources.

---

# Success Criteria

The namespace brokerage mission succeeds when future users can:

```text
recover original identifiers

recover authority context

understand identity lineage

trace mappings through time

preserve unresolved identities

preserve ambiguous identities

perform cross-repository discovery
```

without losing source meaning.

---

# Conclusion

Namespace brokerage exists because biological evidence emerges from many independent identity systems.

Rather than replacing those systems, VDB preserves and relates them.

This approach protects provenance, authority, ambiguity, future reinterpretation, and future discovery.

VDB therefore treats identities as evidence-bearing objects rather than disposable implementation details.

The mission of namespace brokerage is simple:

```text
Preserve identities.

Relate identities.

Never erase identities.
```

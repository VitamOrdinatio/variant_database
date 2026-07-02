"""Phase 4.3 Assertion Record implementation surface.

This package intentionally implements only the Assertion Record layer. It does not
construct Evidence Topology, Convergence Geometry, Evidence Convergence Surfaces,
Projection Views, or RDGP reasoning outputs.
"""

from .identity import make_assertion_id, make_source_assertion_key, stable_hash
from .resolver_policy import RESOLVER_POLICY, RESOLVER_STATUS, resolve_assertion, source_identity_set_status

__all__ = [
    "make_assertion_id",
    "make_source_assertion_key",
    "stable_hash",
    "RESOLVER_POLICY",
    "RESOLVER_STATUS",
    "resolve_assertion",
    "source_identity_set_status",
]

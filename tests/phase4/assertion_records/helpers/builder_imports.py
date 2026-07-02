"""Import helpers for Phase 4.3 Assertion Record implementation modules.

The exact VDB package namespace may settle during implementation. These helpers keep
Layer 1 tests explicit about the expected submodules while giving DEX a small set of
reasonable import candidates.
"""
from __future__ import annotations

from importlib import import_module
from types import ModuleType

import pytest

CANDIDATE_BASES = (
    "variant_database.phase4.assertion_records",
    "variant_database.phase4.assertion_records",
    "phase4.assertion_records",
)


def import_required(submodule: str) -> ModuleType:
    """Import a required Phase 4.3 implementation submodule or fail clearly."""
    attempts: list[str] = []
    for base in CANDIDATE_BASES:
        module_name = f"{base}.{submodule}"
        try:
            return import_module(module_name)
        except ModuleNotFoundError as exc:
            attempts.append(f"{module_name}: {exc}")

    pytest.fail(
        "Missing Phase 4.3 Assertion Record implementation module. "
        f"Tried submodule '{submodule}' using candidate bases:\n"
        + "\n".join(f"  - {attempt}" for attempt in attempts)
    )

from __future__ import annotations

from variant_database.cli import main


def test_cli_importable() -> None:
    assert callable(main)


def test_package_importable() -> None:
    import variant_database

    assert variant_database is not None

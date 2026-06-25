"""SQLite backend helpers for VDB persistence."""

from __future__ import annotations

from pathlib import Path
import sqlite3


def connect_sqlite(db_path: Path | str) -> sqlite3.Connection:
    """Open a SQLite connection with VDB-safe defaults."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

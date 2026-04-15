"""Database migration utilities."""

import sqlite3
from typing import Optional

from budgetcli.database.connection import DatabaseConnection, DatabaseMigration


def init_db(db_path: Optional[str] = None) -> None:
    """
    Initialize database with schema.

    Args:
        db_path: Optional path to database file.
    """
    DatabaseMigration.init_database(db_path)


def reset_db(db_path: Optional[str] = None) -> None:
    """
    Reset database (drop all tables and reinitialize).

    Warning: This deletes all data!

    Args:
        db_path: Optional path to database file.

    Raises:
        RuntimeError: If reset fails.
    """
    try:
        db = DatabaseConnection(db_path)
        conn = db.connect()
        cursor = conn.cursor()

        # Drop all tables
        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute("DROP TABLE IF EXISTS budgets")
        conn.commit()

        db.disconnect()

        # Reinitialize
        init_db(db_path)
    except sqlite3.Error as e:
        raise RuntimeError(f"Database reset failed: {e}") from e


__all__ = ["init_db", "reset_db"]

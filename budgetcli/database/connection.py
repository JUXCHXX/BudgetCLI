"""Database connection and initialization."""

import os
import sqlite3
from pathlib import Path
from typing import Optional


class DatabaseConnection:
    """Manages SQLite database connection."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file. Uses env var or default.
        """
        if db_path is None:
            db_path = os.getenv("BUDGETCLI_DB_PATH", str(Path.home() / ".budgetcli" / "budget.db"))

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """
        Establish database connection.

        Returns:
            SQLite connection object.
        """
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> sqlite3.Connection:
        """Context manager entry."""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.disconnect()


class DatabaseMigration:
    """Database schema initialization and migrations."""

    SCHEMA_SQL = """
    -- Transactions table
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
        category TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0),
        date TEXT NOT NULL,
        note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create index on date for faster queries
    CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
    CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
    CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);

    -- Budgets table
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL UNIQUE,
        monthly_limit REAL NOT NULL CHECK(monthly_limit > 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_budgets_category ON budgets(category);
    """

    @staticmethod
    def init_database(db_path: Optional[str] = None) -> None:
        """
        Initialize database tables and indices.

        Args:
            db_path: Path to database file.

        Raises:
            RuntimeError: If database initialization fails.
        """
        try:
            db = DatabaseConnection(db_path)
            conn = db.connect()
            cursor = conn.cursor()

            # Execute schema
            cursor.executescript(DatabaseMigration.SCHEMA_SQL)
            conn.commit()

            db.disconnect()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database initialization failed: {e}") from e

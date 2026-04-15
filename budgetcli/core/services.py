"""Core business logic services."""

import sqlite3
from datetime import datetime
from typing import Optional

from budgetcli.core.calculations import CalculationService
from budgetcli.core.validators import BudgetValidator, TransactionValidator, ValidationError
from budgetcli.database.connection import DatabaseConnection
from budgetcli.database.models import Budget, MonthlySummary, Transaction, TransactionType


class RepositoryException(Exception):
    """Custom repository exception."""
    pass


class TransactionService:
    """Service for managing transactions."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize transaction service.

        Args:
            db_path: Optional path to database.
        """
        self.db_path = db_path

    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        date: str,
        note: str = "",
    ) -> Transaction:
        """
        Add a new transaction.

        Args:
            transaction_type: Type of transaction (income/expense).
            category: Category name.
            amount: Transaction amount.
            date: Date in ISO format.
            note: Optional note.

        Returns:
            Created transaction object.

        Raises:
            ValidationError: If validation fails.
            RepositoryException: If database operation fails.
        """
        # Validate input
        TransactionValidator.validate_all_transaction_fields(
            transaction_type, category, amount, date
        )

        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO transactions (type, category, amount, date, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (transaction_type, category, amount, date, note),
            )

            conn.commit()
            transaction_id = cursor.lastrowid
            db.disconnect()

            return Transaction(
                id=transaction_id,
                type=TransactionType(transaction_type),
                category=category,
                amount=amount,
                date=date,
                note=note,
                created_at=datetime.now(),
            )
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to add transaction: {e}") from e

    def get_all_transactions(self) -> list[Transaction]:
        """
        Get all transactions.

        Returns:
            List of all transactions.

        Raises:
            RepositoryException: If database operation fails.
        """
        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, type, category, amount, date, note, created_at FROM transactions
                ORDER BY date DESC
                """
            )

            rows = cursor.fetchall()
            db.disconnect()

            transactions = []
            for row in rows:
                transactions.append(
                    Transaction(
                        id=row["id"],
                        type=TransactionType(row["type"]),
                        category=row["category"],
                        amount=row["amount"],
                        date=row["date"],
                        note=row["note"],
                        created_at=row["created_at"],
                    )
                )

            return transactions
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to fetch transactions: {e}") from e

    def get_transactions_by_month(self, year: int, month: int) -> list[Transaction]:
        """
        Get transactions for a specific month.

        Args:
            year: Year filter.
            month: Month filter.

        Returns:
            List of transactions for the month.

        Raises:
            RepositoryException: If database operation fails.
        """
        all_transactions = self.get_all_transactions()
        filtered = [
            t for t in all_transactions
            if t.date.startswith(f"{year:04d}-{month:02d}")
        ]
        return filtered

    def delete_transaction(self, transaction_id: int) -> None:
        """
        Delete a transaction.

        Args:
            transaction_id: Transaction ID to delete.

        Raises:
            RepositoryException: If database operation fails.
        """
        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            db.disconnect()
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to delete transaction: {e}") from e


class BudgetService:
    """Service for managing budgets."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize budget service.

        Args:
            db_path: Optional path to database.
        """
        self.db_path = db_path

    def set_budget(self, category: str, monthly_limit: float) -> Budget:
        """
        Set or update a budget.

        Args:
            category: Category name.
            monthly_limit: Monthly spending limit.

        Returns:
            Created or updated budget object.

        Raises:
            ValidationError: If validation fails.
            RepositoryException: If database operation fails.
        """
        # Validate input
        BudgetValidator.validate_all_budget_fields(category, monthly_limit)

        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            # Check if budget exists
            cursor.execute("SELECT id FROM budgets WHERE category = ?", (category,))
            existing = cursor.fetchone()

            if existing:
                # Update
                cursor.execute(
                    "UPDATE budgets SET monthly_limit = ? WHERE category = ?",
                    (monthly_limit, category),
                )
                budget_id = existing["id"]
            else:
                # Insert
                cursor.execute(
                    """
                    INSERT INTO budgets (category, monthly_limit)
                    VALUES (?, ?)
                    """,
                    (category, monthly_limit),
                )
                budget_id = cursor.lastrowid

            conn.commit()
            db.disconnect()

            return Budget(
                id=budget_id,
                category=category,
                monthly_limit=monthly_limit,
                created_at=datetime.now(),
            )
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to set budget: {e}") from e

    def get_all_budgets(self) -> list[Budget]:
        """
        Get all budgets.

        Returns:
            List of all budgets.

        Raises:
            RepositoryException: If database operation fails.
        """
        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, category, monthly_limit, created_at FROM budgets
                ORDER BY category
                """
            )

            rows = cursor.fetchall()
            db.disconnect()

            budgets = []
            for row in rows:
                budgets.append(
                    Budget(
                        id=row["id"],
                        category=row["category"],
                        monthly_limit=row["monthly_limit"],
                        created_at=row["created_at"],
                    )
                )

            return budgets
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to fetch budgets: {e}") from e

    def get_budget_by_category(self, category: str) -> Optional[Budget]:
        """
        Get budget for a specific category.

        Args:
            category: Category name.

        Returns:
            Budget object or None if not found.

        Raises:
            RepositoryException: If database operation fails.
        """
        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, category, monthly_limit, created_at FROM budgets
                WHERE category = ?
                """,
                (category,),
            )

            row = cursor.fetchone()
            db.disconnect()

            if not row:
                return None

            return Budget(
                id=row["id"],
                category=row["category"],
                monthly_limit=row["monthly_limit"],
                created_at=row["created_at"],
            )
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to fetch budget: {e}") from e

    def delete_budget(self, category: str) -> None:
        """
        Delete a budget.

        Args:
            category: Category name.

        Raises:
            RepositoryException: If database operation fails.
        """
        try:
            db = DatabaseConnection(self.db_path)
            conn = db.connect()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM budgets WHERE category = ?", (category,))
            conn.commit()
            db.disconnect()
        except sqlite3.Error as e:
            raise RepositoryException(f"Failed to delete budget: {e}") from e


class ReportService:
    """Service for generating reports."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize report service.

        Args:
            db_path: Optional path to database.
        """
        self.transaction_service = TransactionService(db_path)
        self.budget_service = BudgetService(db_path)

    def get_monthly_summary(self, year: int, month: int) -> list[MonthlySummary]:
        """
        Get monthly summary for all categories.

        Args:
            year: Year filter.
            month: Month filter.

        Returns:
            List of monthly summaries by category.

        Raises:
            RepositoryException: If database operation fails.
        """
        # Get transactions for month
        transactions = self.transaction_service.get_transactions_by_month(year, month)

        # Calculate totals by category
        totals = CalculationService.calculate_monthly_totals(transactions, year, month)

        # Get all budgets
        budgets = self.budget_service.get_all_budgets()
        budget_map = {b.category: b.monthly_limit for b in budgets}

        # Create summaries
        summaries = []
        seen_categories = set()

        # Add categories with transactions
        for category, total_spent in totals.items():
            budget_limit = budget_map.get(category)
            is_exceeded, difference = CalculationService.check_budget_exceeded(
                total_spent, budget_limit
            )

            status = "EXCEDIDO" if is_exceeded else "OK"

            summaries.append(
                MonthlySummary(
                    category=category,
                    total_spent=total_spent,
                    budget_limit=budget_limit,
                    difference=difference,
                    status=status,
                )
            )
            seen_categories.add(category)

        # Add budgeted categories with no transactions
        for budget in budgets:
            if budget.category not in seen_categories:
                summaries.append(
                    MonthlySummary(
                        category=budget.category,
                        total_spent=0.0,
                        budget_limit=budget.monthly_limit,
                        difference=budget.monthly_limit,
                        status="OK",
                    )
                )

        # Sort by category
        summaries.sort(key=lambda x: x.category)
        return summaries

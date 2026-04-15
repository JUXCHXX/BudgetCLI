"""Tests for services module."""

import pytest
import tempfile
from pathlib import Path

from budgetcli.core.services import (
    BudgetService,
    RepositoryException,
    TransactionService,
)
from budgetcli.core.validators import ValidationError
from budgetcli.database import init_db


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "test.db")
        init_db(db_path)
        yield db_path


class TestTransactionService:
    """Test transaction service."""

    def test_add_transaction_success(self, temp_db):
        """Test adding a valid transaction."""
        service = TransactionService(temp_db)
        transaction = service.add_transaction(
            "expense", "Food", 25.0, "2026-04-15", "Lunch"
        )

        assert transaction.id is not None
        assert transaction.type.value == "expense"
        assert transaction.category == "Food"
        assert transaction.amount == 25.0

    def test_add_transaction_invalid_type(self, temp_db):
        """Test adding transaction with invalid type."""
        service = TransactionService(temp_db)

        with pytest.raises(ValidationError):
            service.add_transaction("invalid", "Food", 25.0, "2026-04-15")

    def test_add_transaction_invalid_amount(self, temp_db):
        """Test adding transaction with invalid amount."""
        service = TransactionService(temp_db)

        with pytest.raises(ValidationError):
            service.add_transaction("expense", "Food", -25.0, "2026-04-15")

    def test_get_all_transactions(self, temp_db):
        """Test retrieving all transactions."""
        service = TransactionService(temp_db)

        # Add transactions
        service.add_transaction("expense", "Food", 25.0, "2026-04-15")
        service.add_transaction("income", "Salary", 5000.0, "2026-04-01")

        transactions = service.get_all_transactions()
        assert len(transactions) == 2

    def test_get_transactions_by_month(self, temp_db):
        """Test filtering transactions by month."""
        service = TransactionService(temp_db)

        # Add transactions
        service.add_transaction("expense", "Food", 25.0, "2026-04-15")
        service.add_transaction("expense", "Food", 30.0, "2026-05-10")

        apr_transactions = service.get_transactions_by_month(2026, 4)
        assert len(apr_transactions) == 1

        may_transactions = service.get_transactions_by_month(2026, 5)
        assert len(may_transactions) == 1

    def test_delete_transaction(self, temp_db):
        """Test deleting a transaction."""
        service = TransactionService(temp_db)

        transaction = service.add_transaction("expense", "Food", 25.0, "2026-04-15")
        assert transaction.id is not None

        service.delete_transaction(transaction.id)

        all_transactions = service.get_all_transactions()
        assert len(all_transactions) == 0


class TestBudgetService:
    """Test budget service."""

    def test_set_budget_new(self, temp_db):
        """Test setting a new budget."""
        service = BudgetService(temp_db)
        budget = service.set_budget("Food", 500.0)

        assert budget.id is not None
        assert budget.category == "Food"
        assert budget.monthly_limit == 500.0

    def test_set_budget_update(self, temp_db):
        """Test updating an existing budget."""
        service = BudgetService(temp_db)

        # Create budget
        budget1 = service.set_budget("Food", 500.0)
        id1 = budget1.id

        # Update budget
        budget2 = service.set_budget("Food", 600.0)

        # Should have same ID but updated limit
        assert budget2.id == id1
        assert budget2.monthly_limit == 600.0

    def test_set_budget_invalid_limit(self, temp_db):
        """Test setting budget with invalid limit."""
        service = BudgetService(temp_db)

        with pytest.raises(ValidationError):
            service.set_budget("Food", -100.0)

    def test_get_all_budgets(self, temp_db):
        """Test retrieving all budgets."""
        service = BudgetService(temp_db)

        # Add budgets
        service.set_budget("Food", 500.0)
        service.set_budget("Transport", 200.0)

        budgets = service.get_all_budgets()
        assert len(budgets) == 2

    def test_get_budget_by_category(self, temp_db):
        """Test retrieving budget by category."""
        service = BudgetService(temp_db)

        service.set_budget("Food", 500.0)

        budget = service.get_budget_by_category("Food")
        assert budget is not None
        assert budget.monthly_limit == 500.0

        budget = service.get_budget_by_category("NonExistent")
        assert budget is None

    def test_delete_budget(self, temp_db):
        """Test deleting a budget."""
        service = BudgetService(temp_db)

        service.set_budget("Food", 500.0)
        service.delete_budget("Food")

        budget = service.get_budget_by_category("Food")
        assert budget is None

"""Tests for calculations module."""

import pytest

from budgetcli.core.calculations import CalculationService
from budgetcli.database.models import Transaction, TransactionType


class TestCalculationService:
    """Test calculation service."""

    @pytest.fixture
    def sample_transactions(self):
        """Create sample transactions for testing."""
        return [
            Transaction(
                id=1,
                type=TransactionType.INCOME,
                category="Salary",
                amount=5000.0,
                date="2026-04-01",
            ),
            Transaction(
                id=2,
                type=TransactionType.EXPENSE,
                category="Food",
                amount=250.0,
                date="2026-04-05",
            ),
            Transaction(
                id=3,
                type=TransactionType.EXPENSE,
                category="Food",
                amount=150.0,
                date="2026-04-10",
            ),
            Transaction(
                id=4,
                type=TransactionType.EXPENSE,
                category="Transport",
                amount=100.0,
                date="2026-04-15",
            ),
            Transaction(
                id=5,
                type=TransactionType.EXPENSE,
                category="Food",
                amount=80.0,
                date="2026-05-05",
            ),
        ]

    def test_calculate_monthly_income(self, sample_transactions):
        """Test monthly income calculation."""
        income = CalculationService.calculate_monthly_income(sample_transactions, 2026, 4)
        assert income == 5000.0

    def test_calculate_monthly_expenses(self, sample_transactions):
        """Test monthly expenses calculation."""
        expenses = CalculationService.calculate_monthly_expenses(sample_transactions, 2026, 4)
        assert expenses == 500.0  # 250 + 150 + 100

    def test_calculate_balance(self, sample_transactions):
        """Test balance calculation."""
        balance = CalculationService.calculate_balance(sample_transactions, 2026, 4)
        assert balance == 4500.0  # 5000 - 500

    def test_calculate_monthly_totals(self, sample_transactions):
        """Test monthly totals by category."""
        totals = CalculationService.calculate_monthly_totals(sample_transactions, 2026, 4)
        assert totals["Food"] == 400.0  # 250 + 150
        assert totals["Transport"] == 100.0

    def test_check_budget_exceeded_not_exceeded(self):
        """Test budget not exceeded."""
        is_exceeded, difference = CalculationService.check_budget_exceeded(300.0, 500.0)
        assert is_exceeded is False
        assert difference == 200.0

    def test_check_budget_exceeded_exceeded(self):
        """Test budget exceeded."""
        is_exceeded, difference = CalculationService.check_budget_exceeded(600.0, 500.0)
        assert is_exceeded is True
        assert difference == -100.0

    def test_check_budget_no_limit(self):
        """Test without budget limit."""
        is_exceeded, difference = CalculationService.check_budget_exceeded(300.0, None)
        assert is_exceeded is False
        assert difference is None

    def test_format_currency(self):
        """Test currency formatting."""
        formatted = CalculationService.format_currency(1234.56)
        assert formatted == "$1,234.56"

    def test_format_currency_custom_symbol(self):
        """Test currency formatting with custom symbol."""
        formatted = CalculationService.format_currency(1234.56, currency_symbol="£")
        assert formatted == "£1,234.56"

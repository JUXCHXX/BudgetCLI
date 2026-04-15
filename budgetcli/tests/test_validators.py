"""Tests for validators module."""

import pytest

from budgetcli.core.validators import (
    BudgetValidator,
    TransactionValidator,
    ValidationError,
)


class TestTransactionValidator:
    """Test transaction validator."""

    def test_validate_type_valid(self):
        """Test valid transaction types."""
        TransactionValidator.validate_type("income")
        TransactionValidator.validate_type("expense")

    def test_validate_type_invalid(self):
        """Test invalid transaction types."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_type("invalid")

    def test_validate_category_valid(self):
        """Test valid category."""
        TransactionValidator.validate_category("Food")
        TransactionValidator.validate_category("Groceries")
        TransactionValidator.validate_category("Food-Delivery")

    def test_validate_category_empty(self):
        """Test empty category."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_category("")

    def test_validate_category_too_long(self):
        """Test category too long."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_category("a" * 101)

    def test_validate_amount_valid(self):
        """Test valid amounts."""
        TransactionValidator.validate_amount(100.0)
        TransactionValidator.validate_amount(0.01)

    def test_validate_amount_negative(self):
        """Test negative amount."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_amount(-10)

    def test_validate_amount_zero(self):
        """Test zero amount."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_amount(0)

    def test_validate_date_valid(self):
        """Test valid date."""
        TransactionValidator.validate_date("2026-04-15")
        TransactionValidator.validate_date("2026-01-01")

    def test_validate_date_invalid(self):
        """Test invalid date format."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_date("15-04-2026")

    def test_validate_month_string_valid(self):
        """Test valid month string."""
        year, month = TransactionValidator.validate_month_string("2026-04")
        assert year == 2026
        assert month == 4

    def test_validate_month_string_invalid(self):
        """Test invalid month string."""
        with pytest.raises(ValidationError):
            TransactionValidator.validate_month_string("2026-13")


class TestBudgetValidator:
    """Test budget validator."""

    def test_validate_limit_valid(self):
        """Test valid budget limit."""
        BudgetValidator.validate_limit(1000.0)
        BudgetValidator.validate_limit(0.01)

    def test_validate_limit_negative(self):
        """Test negative budget limit."""
        with pytest.raises(ValidationError):
            BudgetValidator.validate_limit(-100)

    def test_validate_limit_zero(self):
        """Test zero budget limit."""
        with pytest.raises(ValidationError):
            BudgetValidator.validate_limit(0)

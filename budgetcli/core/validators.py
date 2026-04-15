"""Validation logic for BudgetCLI."""

from datetime import datetime
from typing import Tuple

from budgetcli.database.models import TransactionType


class ValidationError(Exception):
    """Custom validation exception."""
    pass


class TransactionValidator:
    """Validates transaction data."""

    @staticmethod
    def validate_type(transaction_type: str) -> None:
        """
        Validate transaction type.

        Args:
            transaction_type: Type to validate (income/expense).

        Raises:
            ValidationError: If type is invalid.
        """
        valid_types = {t.value for t in TransactionType}
        if transaction_type not in valid_types:
            raise ValidationError(
                f"Invalid transaction type: {transaction_type}. "
                f"Must be one of {valid_types}"
            )

    @staticmethod
    def validate_category(category: str) -> None:
        """
        Validate category name.

        Args:
            category: Category to validate.

        Raises:
            ValidationError: If category is invalid.
        """
        if not category or len(category) > 100:
            raise ValidationError("Category must be 1-100 characters")
        if not category.replace(" ", "").replace("-", "").isalnum():
            raise ValidationError("Category can only contain alphanumeric, spaces, and hyphens")

    @staticmethod
    def validate_amount(amount: float) -> None:
        """
        Validate amount.

        Args:
            amount: Amount to validate.

        Raises:
            ValidationError: If amount is invalid.
        """
        if not isinstance(amount, (int, float)):
            raise ValidationError("Amount must be a number")
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero")

    @staticmethod
    def validate_date(date_str: str) -> None:
        """
        Validate date format (ISO YYYY-MM-DD).

        Args:
            date_str: Date string to validate.

        Raises:
            ValidationError: If date format is invalid.
        """
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            raise ValidationError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")

    @staticmethod
    def validate_month_string(month_str: str) -> Tuple[int, int]:
        """
        Validate and parse month string (YYYY-MM).

        Args:
            month_str: Month string to validate.

        Returns:
            Tuple of (year, month).

        Raises:
            ValidationError: If format is invalid.
        """
        try:
            parts = month_str.split("-")
            if len(parts) != 2:
                raise ValueError("Must be YYYY-MM format")
            year, month = int(parts[0]), int(parts[1])
            if not (1 <= month <= 12):
                raise ValueError("Month must be 01-12")
            return year, month
        except (ValueError, AttributeError) as e:
            raise ValidationError(f"Invalid month format: {month_str}. Use YYYY-MM. Error: {e}")

    @staticmethod
    def validate_all_transaction_fields(
        transaction_type: str, category: str, amount: float, date_str: str
    ) -> None:
        """
        Validate all transaction fields.

        Args:
            transaction_type: Type of transaction.
            category: Transaction category.
            amount: Transaction amount.
            date_str: Date string.

        Raises:
            ValidationError: If any field is invalid.
        """
        TransactionValidator.validate_type(transaction_type)
        TransactionValidator.validate_category(category)
        TransactionValidator.validate_amount(amount)
        TransactionValidator.validate_date(date_str)


class BudgetValidator:
    """Validates budget data."""

    @staticmethod
    def validate_limit(limit: float) -> None:
        """
        Validate budget limit.

        Args:
            limit: Budget limit to validate.

        Raises:
            ValidationError: If limit is invalid.
        """
        if not isinstance(limit, (int, float)):
            raise ValidationError("Monthly limit must be a number")
        if limit <= 0:
            raise ValidationError("Monthly limit must be greater than zero")

    @staticmethod
    def validate_all_budget_fields(category: str, monthly_limit: float) -> None:
        """
        Validate all budget fields.

        Args:
            category: Budget category.
            monthly_limit: Monthly limit.

        Raises:
            ValidationError: If any field is invalid.
        """
        TransactionValidator.validate_category(category)
        BudgetValidator.validate_limit(monthly_limit)

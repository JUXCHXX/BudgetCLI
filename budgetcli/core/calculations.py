"""Calculation logic for BudgetCLI."""

from typing import Dict, Optional

from budgetcli.database.models import MonthlySummary, Transaction, TransactionType


class CalculationService:
    """Service for financial calculations."""

    @staticmethod
    def calculate_monthly_totals(transactions: list[Transaction], year: int, month: int) -> Dict[str, float]:
        """
        Calculate total expenses by category for a month.

        Args:
            transactions: List of transactions.
            year: Year to filter.
            month: Month to filter.

        Returns:
            Dictionary mapping category to total spent.
        """
        totals: Dict[str, float] = {}

        for transaction in transactions:
            if transaction.type != TransactionType.EXPENSE:
                continue

            try:
                trans_year, trans_month, trans_day = map(int, transaction.date.split("-"))
            except (ValueError, AttributeError):
                continue

            if trans_year == year and trans_month == month:
                totals[transaction.category] = totals.get(transaction.category, 0) + transaction.amount

        return totals

    @staticmethod
    def calculate_monthly_income(transactions: list[Transaction], year: int, month: int) -> float:
        """
        Calculate total income for a month.

        Args:
            transactions: List of transactions.
            year: Year to filter.
            month: Month to filter.

        Returns:
            Total income.
        """
        total = 0.0

        for transaction in transactions:
            if transaction.type != TransactionType.INCOME:
                continue

            try:
                trans_year, trans_month, trans_day = map(int, transaction.date.split("-"))
            except (ValueError, AttributeError):
                continue

            if trans_year == year and trans_month == month:
                total += transaction.amount

        return total

    @staticmethod
    def calculate_monthly_expenses(transactions: list[Transaction], year: int, month: int) -> float:
        """
        Calculate total expenses for a month.

        Args:
            transactions: List of transactions.
            year: Year to filter.
            month: Month to filter.

        Returns:
            Total expenses.
        """
        total = 0.0

        for transaction in transactions:
            if transaction.type != TransactionType.EXPENSE:
                continue

            try:
                trans_year, trans_month, trans_day = map(int, transaction.date.split("-"))
            except (ValueError, AttributeError):
                continue

            if trans_year == year and trans_month == month:
                total += transaction.amount

        return total

    @staticmethod
    def calculate_balance(transactions: list[Transaction], year: int, month: int) -> float:
        """
        Calculate balance (income - expenses) for a month.

        Args:
            transactions: List of transactions.
            year: Year to filter.
            month: Month to filter.

        Returns:
            Balance amount.
        """
        income = CalculationService.calculate_monthly_income(transactions, year, month)
        expenses = CalculationService.calculate_monthly_expenses(transactions, year, month)
        return income - expenses

    @staticmethod
    def check_budget_exceeded(
        total_spent: float, budget_limit: Optional[float]
    ) -> tuple[bool, Optional[float]]:
        """
        Check if budget is exceeded.

        Args:
            total_spent: Total amount spent.
            budget_limit: Budget limit (None if no budget).

        Returns:
            Tuple of (is_exceeded, difference). Difference is negative if exceeded.
        """
        if budget_limit is None:
            return False, None

        is_exceeded = total_spent > budget_limit
        difference = budget_limit - total_spent

        return is_exceeded, difference

    @staticmethod
    def format_currency(amount: float, currency_symbol: str = "$") -> str:
        """
        Format amount as currency.

        Args:
            amount: Amount to format.
            currency_symbol: Currency symbol.

        Returns:
            Formatted currency string.
        """
        return f"{currency_symbol}{amount:,.2f}"

"""Database models and schema definition using SQLite."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(BaseModel):
    """Transaction domain model."""
    id: Optional[int] = None
    type: TransactionType
    category: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    date: str = Field(...)  # ISO format: YYYY-MM-DD
    note: Optional[str] = Field(default="", max_length=500)
    created_at: Optional[datetime] = None

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate ISO date format."""
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("Date must be in ISO format (YYYY-MM-DD)")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate amount is positive."""
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Transaction(id={self.id}, type={self.type}, category={self.category}, "
            f"amount={self.amount}, date={self.date})"
        )


class Budget(BaseModel):
    """Budget domain model."""
    id: Optional[int] = None
    category: str = Field(..., min_length=1, max_length=100)
    monthly_limit: float = Field(..., gt=0)
    created_at: Optional[datetime] = None

    @field_validator("monthly_limit")
    @classmethod
    def validate_limit(cls, v: float) -> float:
        """Validate limit is positive."""
        if v <= 0:
            raise ValueError("Monthly limit must be positive")
        return v

    def __repr__(self) -> str:
        """String representation."""
        return f"Budget(id={self.id}, category={self.category}, limit={self.monthly_limit})"


class MonthlySummary(BaseModel):
    """Monthly budget summary for reporting."""
    category: str
    total_spent: float
    budget_limit: Optional[float] = None
    difference: Optional[float] = None
    status: str  # "OK" or "EXCEDIDO"

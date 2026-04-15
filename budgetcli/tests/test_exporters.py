"""Tests for exporters module."""

import json
import csv
import tempfile
from pathlib import Path

import pytest

from budgetcli.database.models import Transaction, TransactionType
from budgetcli.utils.exporters import CSVExporter, JSONExporter


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    return [
        Transaction(
            id=1,
            type=TransactionType.EXPENSE,
            category="Food",
            amount=250.0,
            date="2026-04-05",
            note="Lunch",
        ),
        Transaction(
            id=2,
            type=TransactionType.INCOME,
            category="Salary",
            amount=5000.0,
            date="2026-04-01",
            note="Monthly salary",
        ),
    ]


@pytest.fixture
def temp_export_dir():
    """Create temporary export directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestCSVExporter:
    """Test CSV exporter."""

    def test_export_transactions_success(self, sample_transactions, temp_export_dir):
        """Test exporting transactions to CSV."""
        exporter = CSVExporter(temp_export_dir)
        filepath = exporter.export_transactions(sample_transactions)

        assert filepath.exists()
        assert filepath.suffix == ".csv"

        # Verify content
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 3  # Header + 2 transactions
        assert rows[0][0] == "ID"  # Header
        assert rows[1][2] == "Food"  # First transaction category

    def test_export_with_custom_filename(self, sample_transactions, temp_export_dir):
        """Test export with custom filename."""
        exporter = CSVExporter(temp_export_dir)
        filepath = exporter.export_transactions(sample_transactions, "custom.csv")

        assert filepath.name == "custom.csv"
        assert filepath.exists()


class TestJSONExporter:
    """Test JSON exporter."""

    def test_export_transactions_success(self, sample_transactions, temp_export_dir):
        """Test exporting transactions to JSON."""
        exporter = JSONExporter(temp_export_dir)
        filepath = exporter.export_transactions(sample_transactions)

        assert filepath.exists()
        assert filepath.suffix == ".json"

        # Verify content
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["category"] == "Food"
        assert data[1]["category"] == "Salary"

    def test_export_summary(self, temp_export_dir):
        """Test exporting summary to JSON."""
        exporter = JSONExporter(temp_export_dir)

        summary = {
            "month": "2026-04",
            "income": 5000.0,
            "expenses": 250.0,
            "balance": 4750.0,
        }

        filepath = exporter.export_summary(summary)

        assert filepath.exists()

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["month"] == "2026-04"
        assert data["balance"] == 4750.0

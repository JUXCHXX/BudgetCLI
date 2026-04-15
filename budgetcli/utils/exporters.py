"""Export utilities for financial data."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from budgetcli.database.models import Transaction


class ExportException(Exception):
    """Custom export exception."""
    pass


class BaseExporter:
    """Base class for exporters."""

    def __init__(self, output_dir: str = "exports") -> None:
        """
        Initialize exporter.

        Args:
            output_dir: Directory to save exports.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _generate_filename(self, base_name: str, extension: str) -> Path:
        """
        Generate unique filename with timestamp.

        Args:
            base_name: Base name for file.
            extension: File extension.

        Returns:
            Path to file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"{base_name}_{timestamp}{extension}"


class CSVExporter(BaseExporter):
    """Export data to CSV format."""

    def export_transactions(
        self, transactions: list[Transaction], filename: Optional[str] = None
    ) -> Path:
        """
        Export transactions to CSV.

        Args:
            transactions: List of transactions to export.
            filename: Optional custom filename.

        Returns:
            Path to exported file.

        Raises:
            ExportException: If export fails.
        """
        try:
            if filename is None:
                filepath = self._generate_filename("transactions", ".csv")
            else:
                filepath = self.output_dir / filename

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Type", "Category", "Amount", "Date", "Note", "Created At"])

                for trans in transactions:
                    writer.writerow(
                        [
                            trans.id,
                            trans.type.value,
                            trans.category,
                            f"{trans.amount:.2f}",
                            trans.date,
                            trans.note,
                            trans.created_at or "",
                        ]
                    )

            return filepath
        except IOError as e:
            raise ExportException(f"Failed to export to CSV: {e}") from e


class JSONExporter(BaseExporter):
    """Export data to JSON format."""

    def export_transactions(
        self, transactions: list[Transaction], filename: Optional[str] = None
    ) -> Path:
        """
        Export transactions to JSON.

        Args:
            transactions: List of transactions to export.
            filename: Optional custom filename.

        Returns:
            Path to exported file.

        Raises:
            ExportException: If export fails.
        """
        try:
            if filename is None:
                filepath = self._generate_filename("transactions", ".json")
            else:
                filepath = self.output_dir / filename

            data = []
            for trans in transactions:
                data.append(
                    {
                        "id": trans.id,
                        "type": trans.type.value,
                        "category": trans.category,
                        "amount": trans.amount,
                        "date": trans.date,
                        "note": trans.note,
                        "created_at": str(trans.created_at) if trans.created_at else None,
                    }
                )

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return filepath
        except IOError as e:
            raise ExportException(f"Failed to export to JSON: {e}") from e

    def export_summary(self, summary_data: dict, filename: Optional[str] = None) -> Path:
        """
        Export summary data to JSON.

        Args:
            summary_data: Summary data dictionary.
            filename: Optional custom filename.

        Returns:
            Path to exported file.

        Raises:
            ExportException: If export fails.
        """
        try:
            if filename is None:
                filepath = self._generate_filename("summary", ".json")
            else:
                filepath = self.output_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)

            return filepath
        except IOError as e:
            raise ExportException(f"Failed to export summary to JSON: {e}") from e


class PNGExporter(BaseExporter):
    """Export charts to PNG format using matplotlib."""

    def export_bar_chart(
        self,
        data: dict,
        title: str = "Monthly Expenses",
        filename: Optional[str] = None,
        ylabel: str = "Amount",
    ) -> Path:
        """
        Export data as bar chart PNG.

        Args:
            data: Dictionary mapping labels to values.
            title: Chart title.
            filename: Optional custom filename.
            ylabel: Y-axis label.

        Returns:
            Path to exported file.

        Raises:
            ExportException: If export fails.
        """
        try:
            import matplotlib.pyplot as plt

            if filename is None:
                filepath = self._generate_filename("chart", ".png")
            else:
                filepath = self.output_dir / filename

            # Create figure
            fig, ax = plt.subplots(figsize=(12, 6))

            # Create bar chart
            categories = list(data.keys())
            values = list(data.values())

            ax.bar(categories, values, color="steelblue", edgecolor="navy", alpha=0.7)

            # Formatting
            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.set_ylabel(ylabel, fontsize=11)
            ax.set_xlabel("Category", fontsize=11)
            ax.grid(axis="y", alpha=0.3, linestyle="--")

            # Rotate x-axis labels if needed
            if len(categories) > 5:
                plt.xticks(rotation=45, ha="right")

            # Format y-axis as currency
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            plt.close()

            return filepath
        except ImportError as e:
            raise ExportException("matplotlib is required for PNG export") from e
        except Exception as e:
            raise ExportException(f"Failed to export PNG chart: {e}") from e

    def export_pie_chart(
        self, data: dict, title: str = "Expense Distribution", filename: Optional[str] = None
    ) -> Path:
        """
        Export data as pie chart PNG.

        Args:
            data: Dictionary mapping labels to values.
            title: Chart title.
            filename: Optional custom filename.

        Returns:
            Path to exported file.

        Raises:
            ExportException: If export fails.
        """
        try:
            import matplotlib.pyplot as plt

            if filename is None:
                filepath = self._generate_filename("pie_chart", ".png")
            else:
                filepath = self.output_dir / filename

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 8))

            # Create pie chart
            categories = list(data.keys())
            values = list(data.values())

            colors = plt.cm.Set3(range(len(categories)))
            wedges, texts, autotexts = ax.pie(
                values,
                labels=categories,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
            )

            # Formatting
            ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

            # Make percentage text visible
            for autotext in autotexts:
                autotext.set_color("black")
                autotext.set_fontweight("bold")

            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            plt.close()

            return filepath
        except ImportError as e:
            raise ExportException("matplotlib is required for PNG export") from e
        except Exception as e:
            raise ExportException(f"Failed to export pie chart: {e}") from e

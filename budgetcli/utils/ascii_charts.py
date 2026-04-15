"""ASCII chart utilities for visualizing financial data."""

from typing import Dict, Optional


class ASCIIChart:
    """Generates ASCII bar charts for financial data."""

    @staticmethod
    def create_bar_chart(
        data: Dict[str, float],
        max_width: int = 50,
        show_values: bool = True,
    ) -> str:
        """
        Create an ASCII bar chart.

        Args:
            data: Dictionary mapping labels to values.
            max_width: Maximum width of the chart in characters.
            show_values: Whether to show values next to bars.

        Returns:
            String containing ASCII chart.
        """
        if not data:
            return "No data to display"

        # Find max value for scaling
        max_value = max(data.values()) if data else 1
        max_label_width = max(len(label) for label in data.keys())

        lines = []

        for label, value in sorted(data.items(), key=lambda x: -x[1]):
            # Calculate bar width
            if max_value > 0:
                bar_width = int((value / max_value) * max_width)
            else:
                bar_width = 0

            # Create bar
            bar = "█" * bar_width

            # Format line
            if show_values:
                line = f"{label:<{max_label_width}} {bar} {value:,.0f}"
            else:
                line = f"{label:<{max_label_width}} {bar}"

            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def create_horizontal_bar_chart(
        data: Dict[str, float],
        max_width: int = 40,
        show_values: bool = True,
    ) -> str:
        """
        Create horizontal ASCII bar chart (alias for create_bar_chart).

        Args:
            data: Dictionary mapping labels to values.
            max_width: Maximum width of the chart.
            show_values: Whether to show values.

        Returns:
            String containing ASCII chart.
        """
        return ASCIIChart.create_bar_chart(data, max_width, show_values)

    @staticmethod
    def create_comparison_chart(
        data: Dict[str, tuple[float, float]],
        max_width: int = 40,
        label1: str = "Actual",
        label2: str = "Budget",
    ) -> str:
        """
        Create comparison chart (Actual vs Budget).

        Args:
            data: Dict mapping category to (spent, budget) tuples.
            max_width: Maximum width of chart.
            label1: Label for first bar.
            label2: Label for second bar.

        Returns:
            String containing comparison chart.
        """
        if not data:
            return "No data to display"

        max_value = max(max(spent, budget) for spent, budget in data.values())
        if max_value == 0:
            max_value = 1

        max_label_width = max(len(label) for label in data.keys())

        lines = []
        lines.append(f"{'Category':<{max_label_width}} {label1:<15} {label2:<15}")
        lines.append("-" * (max_label_width + 35))

        for category in sorted(data.keys()):
            spent, budget = data[category]

            bar1_width = int((spent / max_value) * max_width) if max_value > 0 else 0
            bar2_width = int((budget / max_value) * max_width) if max_value > 0 else 0

            bar1 = "█" * bar1_width
            bar2 = "█" * bar2_width

            line = (
                f"{category:<{max_label_width}} "
                f"{bar1:<{max_width}} {spent:>8,.0f}  "
                f"{bar2:<{max_width}} {budget:>8,.0f}"
            )
            lines.append(line)

        return "\n".join(lines)

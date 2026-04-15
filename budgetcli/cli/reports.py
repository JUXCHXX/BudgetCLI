"""Report and visualization commands."""

from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from budgetcli.core import CalculationService, ReportService, RepositoryException, ValidationError
from budgetcli.core.validators import TransactionValidator
from budgetcli.utils import ASCIIChart, CSVExporter, ExportException, JSONExporter, PNGExporter

# Create sub-app with no_args_is_help for better UX
app = typer.Typer(
    help="View reports and summaries",
    no_args_is_help=True,
)
console = Console()


@app.command("monthly")
def monthly_report(
    month: Optional[str] = typer.Option(
        None,
        "--month",
        "-m",
        help="Month in YYYY-MM format (YYYY-MM). Default: current month",
    ),
) -> None:
    """Generate monthly expense report."""
    try:
        # Use current month if not specified
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        # Validate and parse month
        year, m = TransactionValidator.validate_month_string(month)

        # Get report
        report_service = ReportService()
        summaries = report_service.get_monthly_summary(year, m)

        if not summaries:
            console.print("[yellow]No data for this month[/yellow]")
            return

        # Create table
        table = Table(
            title=f"Monthly Report - {month}",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Category", style="green")
        table.add_column("Spent", justify="right", style="yellow")
        table.add_column("Budget", justify="right", style="blue")
        table.add_column("Difference", justify="right", style="magenta")
        table.add_column("Status", style="cyan")

        for summary in summaries:
            status_color = "red" if summary.status == "EXCEDIDO" else "green"
            status_text = f"[{status_color}]{summary.status}[/{status_color}]"

            budget_text = (
                f"{summary.budget_limit:,.2f}"
                if summary.budget_limit is not None
                else "-"
            )
            diff_text = (
                f"{summary.difference:,.2f}" if summary.difference is not None else "-"
            )

            table.add_row(
                summary.category,
                f"{summary.total_spent:,.2f}",
                budget_text,
                diff_text,
                status_text,
            )

        console.print(table)

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("summary")
def monthly_summary(
    month: Optional[str] = typer.Option(
        None,
        "--month",
        "-m",
        help="Month in YYYY-MM format (YYYY-MM). Default: current month",
    ),
) -> None:
    """Show monthly financial summary."""
    try:
        # Use current month if not specified
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        # Validate and parse month
        year, m = TransactionValidator.validate_month_string(month)

        # Get data
        report_service = ReportService()
        transactions = report_service.transaction_service.get_transactions_by_month(year, m)

        # Calculate totals
        income = CalculationService.calculate_monthly_income(transactions, year, m)
        expenses = CalculationService.calculate_monthly_expenses(transactions, year, m)
        balance = income - expenses

        # Create summary panels
        income_panel = Panel(
            f"[green]{CalculationService.format_currency(income)}[/green]",
            title="[bold cyan]Income[/bold cyan]",
            border_style="green",
        )

        expense_panel = Panel(
            f"[red]{CalculationService.format_currency(expenses)}[/red]",
            title="[bold cyan]Expenses[/bold cyan]",
            border_style="red",
        )

        balance_color = "green" if balance >= 0 else "red"
        balance_panel = Panel(
            f"[{balance_color}]{CalculationService.format_currency(balance)}[/{balance_color}]",
            title="[bold cyan]Balance[/bold cyan]",
            border_style=balance_color,
        )

        console.print(
            Panel(
                f"[bold]{month}[/bold]",
                title="[cyan]Monthly Summary[/cyan]",
                expand=False,
            )
        )
        console.print(income_panel)
        console.print(expense_panel)
        console.print(balance_panel)

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("chart")
def ascii_chart(
    month: Optional[str] = typer.Option(
        None,
        "--month",
        "-m",
        help="Month in YYYY-MM format (YYYY-MM). Default: current month",
    ),
) -> None:
    """Display ASCII bar chart of expenses."""
    try:
        # Use current month if not specified
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        # Validate and parse month
        year, m = TransactionValidator.validate_month_string(month)

        # Get report
        report_service = ReportService()
        transactions = report_service.transaction_service.get_transactions_by_month(year, m)

        # Calculate totals
        totals = CalculationService.calculate_monthly_totals(transactions, year, m)

        if not totals:
            console.print("[yellow]No expenses for this month[/yellow]")
            return

        # Create chart
        chart = ASCIIChart.create_bar_chart(totals, max_width=50, show_values=True)
        console.print(Panel(chart, title=f"[bold cyan]Expenses - {month}[/bold cyan]"))

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("export")
def export_data(
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Export format (json/csv)",
    ),
    month: Optional[str] = typer.Option(
        None,
        "--month",
        "-m",
        help="Month filter (YYYY-MM)",
    ),
    output_dir: str = typer.Option("exports", "--output-dir", "-o", help="Output directory"),
) -> None:
    """Export transactions to file."""
    try:
        report_service = ReportService()
        transactions = report_service.transaction_service.get_all_transactions()

        # Filter by month if specified
        if month:
            year, m = TransactionValidator.validate_month_string(month)
            transactions = [t for t in transactions if t.date.startswith(f"{year:04d}-{m:02d}")]

        if not transactions:
            console.print("[yellow]No transactions to export[/yellow]")
            return

        # Export
        if format.lower() == "csv":
            exporter = CSVExporter(output_dir)
            filepath = exporter.export_transactions(transactions)
        elif format.lower() == "json":
            exporter = JSONExporter(output_dir)
            filepath = exporter.export_transactions(transactions)
        else:
            console.print(f"[red]✗ Unsupported format: {format}[/red]")
            raise typer.Exit(code=1)

        console.print(f"[green]✓[/green] Exported to [cyan]{filepath}[/cyan]")

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except ExportException as e:
        console.print(f"[red]✗ Export error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("plot")
def plot_chart(
    month: Optional[str] = typer.Option(
        None,
        "--month",
        "-m",
        help="Month in YYYY-MM format (YYYY-MM). Default: current month",
    ),
    chart_type: str = typer.Option("bar", "--type", "-t", help="Chart type (bar/pie)"),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output filename (if provided, generates PNG)"
    ),
    output_dir: str = typer.Option("exports", "--output-dir", "-d", help="Output directory"),
) -> None:
    """Generate matplotlib charts (PNG)."""
    try:
        # Use current month if not specified
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        # Validate and parse month
        year, m = TransactionValidator.validate_month_string(month)

        # Get data
        report_service = ReportService()
        transactions = report_service.transaction_service.get_transactions_by_month(year, m)

        # Calculate totals
        totals = CalculationService.calculate_monthly_totals(transactions, year, m)

        if not totals:
            console.print("[yellow]No expenses for this month[/yellow]")
            return

        # Export PNG
        exporter = PNGExporter(output_dir)

        if chart_type.lower() == "pie":
            filepath = exporter.export_pie_chart(
                totals, title=f"Expense Distribution - {month}", filename=output
            )
        elif chart_type.lower() == "bar":
            filepath = exporter.export_bar_chart(
                totals, title=f"Monthly Expenses - {month}", filename=output
            )
        else:
            console.print(f"[red]✗ Unsupported chart type: {chart_type}[/red]")
            raise typer.Exit(code=1)

        console.print(f"[green]✓[/green] Chart exported to [cyan]{filepath}[/cyan]")

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except ExportException as e:
        console.print(f"[red]✗ Chart error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)

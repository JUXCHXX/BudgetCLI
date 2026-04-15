"""Main CLI application entry point."""

import typer
from rich.console import Console

from budgetcli import __version__
from budgetcli.cli import budgets, reports, transactions
from budgetcli.database import init_db

# Initialize CLI app
app = typer.Typer(
    help="BudgetCLI - Professional personal finance management tool",
    no_args_is_help=True,
)
console = Console()

# Add command groups (sub-applications)
app.add_typer(transactions.app, name="transaction", help="Manage transactions")
app.add_typer(budgets.app, name="budget", help="Manage budgets")
app.add_typer(reports.app, name="report", help="View reports and summaries")


@app.command()
def init() -> None:
    """Initialize database with schema."""
    try:
        init_db()
        console.print("[green]✓[/green] Database initialized successfully")
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize database: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[cyan]BudgetCLI[/cyan] version [yellow]{__version__}[/yellow]")


if __name__ == "__main__":
    app()

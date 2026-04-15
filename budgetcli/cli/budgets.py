"""Budget management commands."""

import typer
from rich.console import Console
from rich.table import Table

from budgetcli.core import BudgetService, RepositoryException, ValidationError

# Create sub-app with no_args_is_help for better UX
app = typer.Typer(
    help="Manage budgets",
    no_args_is_help=True,
)
console = Console()


@app.command("set-budget")
def set_budget(
    category: str = typer.Option(..., "--category", "-c", help="Category name"),
    limit: float = typer.Option(..., "--limit", "-l", help="Monthly spending limit"),
) -> None:
    """Set or update a budget for a category."""
    try:
        budget_service = BudgetService()
        budget = budget_service.set_budget(category, limit)

        console.print(
            f"[green]✓[/green] Budget for [cyan]{category}[/cyan] "
            f"set to [yellow]{limit:,.2f}[/yellow]"
        )

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("list")
def list_budgets() -> None:
    """List all budgets."""
    try:
        budget_service = BudgetService()
        budgets = budget_service.get_all_budgets()

        if not budgets:
            console.print("[yellow]No budgets configured[/yellow]")
            return

        # Create table
        table = Table(title="Budgets", show_header=True, header_style="bold cyan")
        table.add_column("Category", style="green")
        table.add_column("Monthly Limit", justify="right", style="yellow")
        table.add_column("Created", style="blue")

        for budget in budgets:
            table.add_row(
                budget.category,
                f"{budget.monthly_limit:,.2f}",
                str(budget.created_at)[:10] if budget.created_at else "-",
            )

        console.print(table)

    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("delete")
def delete_budget(
    category: str = typer.Option(..., "--category", "-c", help="Category name"),
) -> None:
    """Delete a budget."""
    try:
        budget_service = BudgetService()
        budget_service.delete_budget(category)
        console.print(f"[green]✓[/green] Budget for [cyan]{category}[/cyan] deleted")

    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)

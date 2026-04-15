"""Transaction management commands."""

from datetime import date
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from budgetcli.core import (
    BudgetService,
    CalculationService,
    RepositoryException,
    TransactionService,
    ValidationError,
)
from budgetcli.database import TransactionType

# Create sub-app with no_args_is_help for better UX
app = typer.Typer(
    help="Manage transactions",
    no_args_is_help=True,
)
console = Console()


@app.command("add")
def add_transaction(
    type: str = typer.Option(..., "--type", "-t", help="Transaction type (income/expense)"),
    category: str = typer.Option(..., "--category", "-c", help="Category name"),
    amount: float = typer.Option(..., "--amount", "-a", help="Amount"),
    date_str: str = typer.Option(
        str(date.today()), "--date", "-d", help="Date in YYYY-MM-DD format"
    ),
    note: str = typer.Option("", "--note", "-n", help="Optional note"),
) -> None:
    """Add a new transaction."""
    try:
        transaction_service = TransactionService()

        # Add transaction
        transaction = transaction_service.add_transaction(type, category, amount, date_str, note)

        # Check budget
        budget_service = BudgetService()
        budget = budget_service.get_budget_by_category(category)

        # Parse date
        parts = transaction.date.split("-")
        year, month = int(parts[0]), int(parts[1])

        if budget and type == TransactionType.EXPENSE.value:
            transactions = transaction_service.get_transactions_by_month(year, month)
            totals = CalculationService.calculate_monthly_totals(transactions, year, month)
            total = totals.get(category, 0)

            is_exceeded, difference = CalculationService.check_budget_exceeded(
                total, budget.monthly_limit
            )

            console.print(f"[green]✓[/green] Transaction added: {transaction}")

            if is_exceeded and difference is not None:
                console.print(
                    f"[red]⚠ Budget exceeded by {-difference:.2f} "
                    f"(spent: {total:.2f} / budget: {budget.monthly_limit:.2f})[/red]"
                )
            else:
                if difference is not None:
                    console.print(
                        f"[yellow]Remaining budget: {difference:.2f}[/yellow]"
                    )
        else:
            console.print(f"[green]✓[/green] Transaction added: {transaction}")

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("list")
def list_transactions(
    month: Optional[str] = typer.Option(
        None, "--month", "-m", help="Filter by month (YYYY-MM)"
    ),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum transactions to show"),
) -> None:
    """List transactions."""
    try:
        transaction_service = TransactionService()
        transactions = transaction_service.get_all_transactions()

        if month:
            from budgetcli.core.validators import TransactionValidator
            year, m = TransactionValidator.validate_month_string(month)
            transactions = [t for t in transactions if t.date.startswith(f"{year:04d}-{m:02d}")]

        # Limit results
        transactions = transactions[:limit]

        if not transactions:
            console.print("[yellow]No transactions found[/yellow]")
            return

        # Create table
        table = Table(title="Transactions", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Category", style="green")
        table.add_column("Amount", justify="right", style="yellow")
        table.add_column("Date", style="blue")
        table.add_column("Note", style="white")

        for trans in transactions:
            type_color = "green" if trans.type == TransactionType.INCOME else "red"
            table.add_row(
                str(trans.id),
                f"[{type_color}]{trans.type.value}[/{type_color}]",
                trans.category,
                f"{trans.amount:,.2f}",
                trans.date,
                trans.note,
            )

        console.print(table)

    except ValidationError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(code=1)
    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("delete")
def delete_transaction(
    transaction_id: int = typer.Argument(..., help="Transaction ID to delete"),
) -> None:
    """Delete a transaction."""
    try:
        transaction_service = TransactionService()
        transaction_service.delete_transaction(transaction_id)
        console.print(f"[green]✓[/green] Transaction {transaction_id} deleted")

    except RepositoryException as e:
        console.print(f"[red]✗ Database error: {e}[/red]")
        raise typer.Exit(code=1)

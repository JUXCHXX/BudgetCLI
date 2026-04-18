"""Utilities for the TUI (Text User Interface)."""

import os
from datetime import datetime
from typing import Callable, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str = "BudgetCLI v0.0.2") -> None:
    """Print the application header."""
    header = Panel(
        title,
        style="bold cyan",
        expand=False,
        border_style="cyan",
    )
    console.print(header)


def print_error(message: str) -> None:
    """Print an error message."""
    error_panel = Panel(
        f"[red]✗ Error[/red]\n{message}",
        style="red",
        border_style="red",
    )
    console.print(error_panel)


def print_success(message: str) -> None:
    """Print a success message."""
    success_panel = Panel(
        f"[green]✓ Éxito[/green]\n{message}",
        style="green",
        border_style="green",
    )
    console.print(success_panel)


def print_info(message: str) -> None:
    """Print an info message."""
    info_panel = Panel(
        message,
        style="blue",
        border_style="blue",
    )
    console.print(info_panel)


def wait_for_continue() -> None:
    """Wait for user to press Enter to continue."""
    input("\n[cyan]Presiona Enter para continuar...[/cyan]")


def validate_number(value: str, allow_negative: bool = False) -> Optional[float]:
    """
    Validate if a string is a valid number.

    Args:
        value: String to validate.
        allow_negative: If True, allow negative numbers.

    Returns:
        Float value if valid, None otherwise.
    """
    try:
        num = float(value)
        if not allow_negative and num < 0:
            return None
        return num
    except ValueError:
        return None


def validate_date(date_str: str) -> bool:
    """
    Validate date string in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate.

    Returns:
        True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_today_str() -> str:
    """Get today's date as YYYY-MM-DD string."""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_month_str() -> str:
    """Get current month as YYYY-MM string."""
    return datetime.now().strftime("%Y-%m")


def paginate_list(items: list, page_size: int = 20) -> list[list]:
    """
    Paginate a list into chunks.

    Args:
        items: List to paginate.
        page_size: Size of each page.

    Returns:
        List of pages (each page is a list of items).
    """
    pages = []
    for i in range(0, len(items), page_size):
        pages.append(items[i : i + page_size])
    return pages


def create_table(
    title: str, columns: list[str], rows: list[tuple], width: Optional[int] = None
) -> Table:
    """
    Create a Rich table.

    Args:
        title: Table title.
        columns: List of column names.
        rows: List of row tuples.
        width: Optional fixed width.

    Returns:
        Configured Rich Table.
    """
    table = Table(title=title, width=width)
    for col in columns:
        table.add_column(col, style="cyan")
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    return table


class NavigationStack:
    """Simple navigation stack for menu system."""

    def __init__(self) -> None:
        """Initialize navigation stack."""
        self._stack: list[Callable] = []

    def push(self, menu_fn: Callable) -> None:
        """
        Push a menu function onto the stack and execute it.

        Args:
            menu_fn: Menu function to push and execute.
        """
        self._stack.append(menu_fn)
        menu_fn()

    def go_back(self) -> None:
        """Go back to the previous menu."""
        if len(self._stack) > 1:
            self._stack.pop()
            clear_screen()
            self._stack[-1]()
        else:
            clear_screen()

    def is_at_root(self) -> bool:
        """Check if at root menu."""
        return len(self._stack) == 0

    def reset(self) -> None:
        """Reset navigation stack."""
        self._stack = []


# Global navigation stack
nav_stack = NavigationStack()

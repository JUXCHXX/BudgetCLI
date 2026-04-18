"""Main TUI application with opening animation and menu system."""

import time

import questionary
from rich.align import Align
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from budgetcli.cli.tui_menus import (
    configuration_menu,
    main_menu,
    reports_menu,
    budgets_menu,
    transactions_menu,
)
from budgetcli.cli.tui_utils import (
    clear_screen,
    nav_stack,
    print_header,
    wait_for_continue,
)

console = Console()


def animate_opening() -> None:
    """Play opening animation with ASCII art and progress bar."""
    clear_screen()

    # ASCII art frames for BudgetCLI logo
    frames = [
        """
╔═══════════════════════════════════╗
║                                   ║
║   ████████  ██    ██ ██████████   ║
║   ██        ██ ██ ██       ██     ║
║   ████████  ██ ██ ██       ██     ║
║   ██        ██    ██       ██     ║
║   ██        ██    ██       ██     ║
║                                   ║
║        BudgetCLI v0.0.2          ║
║                                   ║
╚═══════════════════════════════════╝
        """,
        """
╔═══════════════════════════════════╗
║ ▓▓▓▓▓▓▓▓  ▓▓    ▓▓ ▓▓▓▓▓▓▓▓▓▓   ║
║ ▓▓        ▓▓ ▓▓ ▓▓       ▓▓     ║
║ ▓▓▓▓▓▓▓▓  ▓▓ ▓▓ ▓▓       ▓▓     ║
║ ▓▓        ▓▓    ▓▓       ▓▓     ║
║ ▓▓        ▓▓    ▓▓       ▓▓     ║
║ ▒▒▒▒▒▒▒▒  ▒▒    ▒▒ ▒▒▒▒▒▒▒▒▒▒   ║
║ ░░░░░░░░  ░░    ░░ ░░░░░░░░░░   ║
║                                   ║
║        BudgetCLI v0.0.2          ║
║                                   ║
╚═══════════════════════════════════╝
        """,
    ]

    # Animate logo frames
    for frame in frames:
        console.print(Align.center(frame), style="cyan")
        time.sleep(0.4)
        clear_screen()

    # Progress bar animation
    messages = [
        "Verificando integridad...",
        "Cargando categorías...",
        "Inicializando base de datos...",
        "Listo.",
    ]

    progress_steps = [0, 33, 66, 100]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Inicializando...", total=100)

        for step, message in zip(progress_steps, messages):
            progress.update(task, description=message)
            time.sleep(0.4)
            if step < 100:
                progress.update(task, completed=step)

    time.sleep(0.5)
    clear_screen()


def show_main_menu() -> None:
    """Display the main interactive menu."""
    print_header()
    console.print()

    choices = [
        questionary.Choice("Transacciones", value="transactions"),
        questionary.Choice("Presupuestos", value="budgets"),
        questionary.Choice("Reportes", value="reports"),
        questionary.Choice("Configuración", value="config"),
        questionary.Choice("Salir", value="exit"),
    ]

    selected = questionary.select(
        "Selecciona una opción:",
        choices=choices,
        pointer="➤ ",
        use_shortcuts=False,
        use_pointer=True,
    ).ask()

    if selected is None:
        selected = "exit"

    if selected == "transactions":
        nav_stack.push(transactions_menu)
    elif selected == "budgets":
        nav_stack.push(budgets_menu)
    elif selected == "reports":
        nav_stack.push(reports_menu)
    elif selected == "config":
        nav_stack.push(configuration_menu)
    elif selected == "exit":
        handle_exit()


def handle_exit() -> None:
    """Handle application exit with confirmation."""
    confirm = questionary.confirm(
        "¿Seguro que deseas salir de BudgetCLI?",
        auto_enter=False,
        default=False,
    ).ask()

    if confirm:
        clear_screen()
        console.print(
            Align.center(
                "[green]✓[/green] Gracias por usar [cyan]BudgetCLI[/cyan]. ¡Hasta pronto!"
            )
        )
        raise SystemExit(0)
    else:
        show_main_menu()


def start_tui() -> None:
    """Start the TUI application."""
    try:
        # Play opening animation
        animate_opening()

        # Reset navigation stack and show main menu
        nav_stack.reset()
        nav_stack.push(show_main_menu)

    except KeyboardInterrupt:
        clear_screen()
        handle_exit()
    except SystemExit:
        raise
    except Exception as e:
        clear_screen()
        console.print(f"[red]✗ Error inesperado: {e}[/red]")
        raise SystemExit(1)


if __name__ == "__main__":
    start_tui()

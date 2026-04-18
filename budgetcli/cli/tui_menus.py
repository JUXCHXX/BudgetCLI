"""Interactive menus for the TUI."""

import os
from datetime import datetime
from typing import Optional

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from budgetcli.cli.tui_utils import (
    clear_screen,
    create_table,
    get_current_month_str,
    get_today_str,
    nav_stack,
    paginate_list,
    print_error,
    print_header,
    print_info,
    print_success,
    validate_date,
    validate_number,
    wait_for_continue,
)
from budgetcli.core import (
    BudgetService,
    CalculationService,
    RepositoryException,
    TransactionService,
    ValidationError,
)
from budgetcli.database import TransactionType
from budgetcli.utils.exporters import CSVExporter, JSONExporter

console = Console()


# ============================================================================
# TRANSACTIONS MENU
# ============================================================================


def transactions_menu() -> None:
    """Display transactions submenu."""
    clear_screen()
    print_header()
    console.print()

    choices = [
        questionary.Choice("Agregar ingreso", value="add_income"),
        questionary.Choice("Agregar gasto", value="add_expense"),
        questionary.Choice("Ver historial", value="view_history"),
        questionary.Choice("Eliminar transacción", value="delete"),
        questionary.Choice("← Volver", value="back"),
    ]

    selected = questionary.select(
        "Transacciones:",
        choices=choices,
        pointer="➤ ",
        use_shortcuts=False,
    ).ask()

    if selected is None or selected == "back":
        nav_stack.go_back()
    elif selected == "add_income":
        nav_stack.push(lambda: add_transaction_flow(TransactionType.INCOME.value))
    elif selected == "add_expense":
        nav_stack.push(lambda: add_transaction_flow(TransactionType.EXPENSE.value))
    elif selected == "view_history":
        nav_stack.push(view_transaction_history)
    elif selected == "delete":
        nav_stack.push(delete_transaction)


def add_transaction_flow(transaction_type: str) -> None:
    """
    Flow for adding a new transaction.

    Args:
        transaction_type: Type of transaction (income/expense).
    """
    clear_screen()
    print_header()
    console.print()

    type_label = "ingreso" if transaction_type == "income" else "gasto"
    console.print(f"[bold cyan]Agregar {type_label}[/bold cyan]\n")

    try:
        # Get service
        service = TransactionService()

        # Get categories from existing transactions
        all_transactions = service.get_all_transactions()
        existing_categories = sorted(
            set(t.category for t in all_transactions if t.type.value == transaction_type)
        )

        # Category selection
        category_choices = [questionary.Choice(cat, value=cat) for cat in existing_categories]
        category_choices.append(questionary.Choice("+ Nueva categoría", value="new"))

        category = questionary.select(
            "Categoría:",
            choices=category_choices if category_choices else [questionary.Choice("Nueva categoría", value="new")],
            pointer="➤ ",
            use_shortcuts=False,
        ).ask()

        if category == "new":
            category = questionary.text("Nombre de la nueva categoría:").ask()
            if not category:
                print_error("Categoría no puede estar vacía.")
                wait_for_continue()
                nav_stack.go_back()
                return

        # Amount
        while True:
            amount_str = questionary.text("Monto:").ask()
            amount = validate_number(amount_str, allow_negative=False)
            if amount is not None and amount > 0:
                break
            print_error("Por favor ingresa un número positivo válido.")

        # Date
        while True:
            date_str = questionary.text(
                "Fecha (YYYY-MM-DD):", default=get_today_str()
            ).ask()
            if validate_date(date_str):
                break
            print_error("Formato de fecha inválido. Usa YYYY-MM-DD")

        # Note
        note = questionary.text("Nota (opcional):").ask() or ""

        # Summary
        clear_screen()
        print_header()
        console.print()

        summary = Panel(
            f"[cyan]Tipo:[/cyan] {type_label.capitalize()}\n"
            f"[cyan]Categoría:[/cyan] {category}\n"
            f"[cyan]Monto:[/cyan] ${amount:.2f}\n"
            f"[cyan]Fecha:[/cyan] {date_str}\n"
            f"[cyan]Nota:[/cyan] {note or '(sin nota)'}",
            title="Resumen",
            border_style="cyan",
        )
        console.print(summary)

        # Confirm
        confirm = questionary.confirm(
            "¿Confirmar registro?", auto_enter=False, default=True
        ).ask()

        if confirm:
            # Add transaction
            transaction = service.add_transaction(
                transaction_type, category, amount, date_str, note
            )

            # Check budget if it's an expense
            if transaction_type == TransactionType.EXPENSE.value:
                budget_service = BudgetService()
                budget = budget_service.get_budget_by_category(category)

                if budget:
                    year, month = int(date_str[:4]), int(date_str[5:7])
                    transactions = service.get_transactions_by_month(year, month)
                    totals = CalculationService.calculate_monthly_totals(
                        transactions, year, month
                    )
                    total = totals.get(category, 0)

                    is_exceeded, difference = CalculationService.check_budget_exceeded(
                        total, budget.monthly_limit
                    )

                    print_success(f"Transacción registrada correctamente.")

                    if is_exceeded and difference is not None:
                        console.print(
                            f"[red]⚠ Presupuesto excedido por ${-difference:.2f}[/red]"
                        )
                    else:
                        if difference is not None:
                            console.print(
                                f"[yellow]Presupuesto restante: ${difference:.2f}[/yellow]"
                            )
                else:
                    print_success(f"Transacción registrada correctamente.")
            else:
                print_success(f"Transacción registrada correctamente.")

            wait_for_continue()
            nav_stack.go_back()
        else:
            nav_stack.go_back()

    except ValidationError as e:
        print_error(f"Error de validación: {e}")
        wait_for_continue()
        nav_stack.go_back()
    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def view_transaction_history() -> None:
    """View transaction history with optional filters."""
    clear_screen()
    print_header()
    console.print()

    try:
        service = TransactionService()
        transactions = service.get_all_transactions()

        # Ask for month filter
        filter_month = questionary.confirm(
            "¿Filtrar por mes?", auto_enter=False, default=False
        ).ask()

        if filter_month:
            month_str = questionary.text(
                "Mes (YYYY-MM):", default=get_current_month_str()
            ).ask()
            try:
                year, month = map(int, month_str.split("-"))
                transactions = [
                    t
                    for t in transactions
                    if t.date.startswith(f"{year:04d}-{month:02d}")
                ]
            except ValueError:
                print_error("Formato de mes inválido.")
                wait_for_continue()
                return

        if not transactions:
            print_info("No hay transacciones.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Paginate
        pages = paginate_list(transactions, page_size=10)

        for page_num, page in enumerate(pages):
            clear_screen()
            print_header()
            console.print()

            rows = [
                (t.id, t.type.value, t.category, f"${t.amount:.2f}", t.date, t.note)
                for t in page
            ]

            table = create_table(
                "Historial de Transacciones",
                ["ID", "Tipo", "Categoría", "Monto", "Fecha", "Nota"],
                rows,
            )
            console.print(table)

            if page_num < len(pages) - 1:
                if questionary.confirm(
                    "¿Ver más?", auto_enter=False, default=True
                ).ask():
                    continue
                else:
                    break

        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def delete_transaction() -> None:
    """Delete a transaction."""
    clear_screen()
    print_header()
    console.print()

    try:
        service = TransactionService()
        transactions = service.get_all_transactions()

        if not transactions:
            print_info("No hay transacciones.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Show compact list
        for t in transactions[:10]:
            console.print(f"[cyan]{t.id}[/cyan] - {t.category} (${t.amount:.2f}) - {t.date}")

        transaction_id_str = questionary.text("ID de la transacción a eliminar:").ask()

        try:
            transaction_id = int(transaction_id_str)
        except ValueError:
            print_error("ID inválido.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Confirm
        if questionary.confirm("¿Confirmar eliminación?", auto_enter=False, default=False).ask():
            service.delete_transaction(transaction_id)
            print_success("Transacción eliminada correctamente.")
            wait_for_continue()

        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


# ============================================================================
# BUDGETS MENU
# ============================================================================


def budgets_menu() -> None:
    """Display budgets submenu."""
    clear_screen()
    print_header()
    console.print()

    choices = [
        questionary.Choice("Definir presupuesto mensual", value="set"),
        questionary.Choice("Ver presupuestos activos", value="view"),
        questionary.Choice("Eliminar presupuesto", value="delete"),
        questionary.Choice("← Volver", value="back"),
    ]

    selected = questionary.select(
        "Presupuestos:",
        choices=choices,
        pointer="➤ ",
        use_shortcuts=False,
    ).ask()

    if selected is None or selected == "back":
        nav_stack.go_back()
    elif selected == "set":
        nav_stack.push(set_budget)
    elif selected == "view":
        nav_stack.push(view_budgets)
    elif selected == "delete":
        nav_stack.push(delete_budget)


def set_budget() -> None:
    """Set a new budget."""
    clear_screen()
    print_header()
    console.print()
    console.print("[bold cyan]Definir Presupuesto Mensual[/bold cyan]\n")

    try:
        # Category
        category = questionary.text("Categoría:").ask()
        if not category:
            print_error("Categoría no puede estar vacía.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Limit
        while True:
            limit_str = questionary.text("Límite mensual ($):").ask()
            limit = validate_number(limit_str, allow_negative=False)
            if limit is not None and limit > 0:
                break
            print_error("Por favor ingresa un número positivo válido.")

        # Confirmation
        clear_screen()
        print_header()
        console.print()

        summary = Panel(
            f"[cyan]Categoría:[/cyan] {category}\n" f"[cyan]Límite:[/cyan] ${limit:.2f}",
            title="Resumen",
            border_style="cyan",
        )
        console.print(summary)

        if questionary.confirm(
            "¿Confirmar presupuesto?", auto_enter=False, default=True
        ).ask():
            service = BudgetService()
            service.set_budget(category, limit)
            print_success("Presupuesto definido correctamente.")
            wait_for_continue()

        nav_stack.go_back()

    except ValidationError as e:
        print_error(f"Error de validación: {e}")
        wait_for_continue()
        nav_stack.go_back()
    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def view_budgets() -> None:
    """View active budgets with percentage used."""
    clear_screen()
    print_header()
    console.print()

    try:
        budget_service = BudgetService()
        transaction_service = TransactionService()

        budgets = budget_service.get_all_budgets()

        if not budgets:
            print_info("No hay presupuestos definidos.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Get current month
        year = datetime.now().year
        month = datetime.now().month
        transactions = transaction_service.get_transactions_by_month(year, month)
        totals = CalculationService.calculate_monthly_totals(transactions, year, month)

        # Build table rows
        rows = []
        for budget in budgets:
            spent = totals.get(budget.category, 0)
            percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
            status = "✓" if spent <= budget.monthly_limit else "✗"

            rows.append(
                (
                    budget.category,
                    f"${budget.monthly_limit:.2f}",
                    f"${spent:.2f}",
                    f"{percentage:.1f}%",
                    status,
                )
            )

        table = create_table(
            "Presupuestos Activos",
            ["Categoría", "Límite", "Gastado", "% Usado", "Estado"],
            rows,
        )
        console.print(table)

        wait_for_continue()
        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def delete_budget() -> None:
    """Delete a budget."""
    clear_screen()
    print_header()
    console.print()

    try:
        service = BudgetService()
        budgets = service.get_all_budgets()

        if not budgets:
            print_info("No hay presupuestos para eliminar.")
            wait_for_continue()
            nav_stack.go_back()
            return

        choices = [
            questionary.Choice(b.category, value=b.category) for b in budgets
        ]

        category = questionary.select(
            "Selecciona presupuesto a eliminar:",
            choices=choices,
            pointer="➤ ",
            use_shortcuts=False,
        ).ask()

        if category and questionary.confirm(
            "¿Confirmar eliminación?", auto_enter=False, default=False
        ).ask():
            service.delete_budget(category)
            print_success("Presupuesto eliminado correctamente.")
            wait_for_continue()

        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


# ============================================================================
# REPORTS MENU
# ============================================================================


def reports_menu() -> None:
    """Display reports submenu."""
    clear_screen()
    print_header()
    console.print()

    choices = [
        questionary.Choice("Reporte mensual", value="monthly"),
        questionary.Choice("Resumen financiero", value="summary"),
        questionary.Choice("Exportar gráfico (PNG)", value="png"),
        questionary.Choice("Exportar datos (CSV)", value="csv"),
        questionary.Choice("Exportar datos (JSON)", value="json"),
        questionary.Choice("← Volver", value="back"),
    ]

    selected = questionary.select(
        "Reportes:",
        choices=choices,
        pointer="➤ ",
        use_shortcuts=False,
    ).ask()

    if selected is None or selected == "back":
        nav_stack.go_back()
    elif selected == "monthly":
        nav_stack.push(monthly_report)
    elif selected == "summary":
        nav_stack.push(financial_summary)
    elif selected == "png":
        nav_stack.push(export_chart_png)
    elif selected == "csv":
        nav_stack.push(lambda: export_data("csv"))
    elif selected == "json":
        nav_stack.push(lambda: export_data("json"))


def monthly_report() -> None:
    """Generate monthly report."""
    clear_screen()
    print_header()
    console.print()

    try:
        from budgetcli.core.services import ReportService

        month_str = questionary.text(
            "Mes (YYYY-MM):", default=get_current_month_str()
        ).ask()

        try:
            year, month = map(int, month_str.split("-"))
        except ValueError:
            print_error("Formato de mes inválido.")
            wait_for_continue()
            nav_stack.go_back()
            return

        report_service = ReportService()
        summaries = report_service.get_monthly_summary(year, month)

        clear_screen()
        print_header()
        console.print()

        rows = [
            (
                s.category,
                f"${s.total_spent:.2f}",
                f"${s.budget_limit:.2f}" if s.budget_limit else "Sin límite",
                f"${s.difference:.2f}" if s.difference is not None else "N/A",
                s.status,
            )
            for s in summaries
        ]

        table = create_table(
            f"Reporte Mensual {month_str}",
            ["Categoría", "Gastado", "Presupuesto", "Diferencia", "Estado"],
            rows,
        )
        console.print(table)

        wait_for_continue()
        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def financial_summary() -> None:
    """Show financial summary."""
    clear_screen()
    print_header()
    console.print()

    try:
        service = TransactionService()
        all_transactions = service.get_all_transactions()

        total_income = sum(
            t.amount for t in all_transactions if t.type.value == "income"
        )
        total_expense = sum(
            t.amount for t in all_transactions if t.type.value == "expense"
        )
        balance = total_income - total_expense

        balance_color = "green" if balance >= 0 else "red"

        summary_text = f"""
[cyan]Ingresos totales:[/cyan]     [green]${total_income:.2f}[/green]
[cyan]Gastos totales:[/cyan]       [red]${total_expense:.2f}[/red]
[cyan]Balance:[/cyan]              [{balance_color}]${balance:.2f}[/{balance_color}]
        """

        print_info(summary_text)
        wait_for_continue()
        nav_stack.go_back()

    except RepositoryException as e:
        print_error(f"Error de base de datos: {e}")
        wait_for_continue()
        nav_stack.go_back()


def export_chart_png() -> None:
    """Export monthly expenses chart as PNG."""
    clear_screen()
    print_header()
    console.print()

    try:
        from budgetcli.utils.exporters import PNGExporter

        # Get current month
        year = datetime.now().year
        month = datetime.now().month

        # Get transactions
        service = TransactionService()
        transactions = service.get_transactions_by_month(year, month)

        if not transactions:
            print_info("No hay transacciones en este mes para generar gráfico.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Calculate totals by category for expenses only
        expenses_by_category = {}
        for t in transactions:
            if t.type.value == "expense":
                if t.category not in expenses_by_category:
                    expenses_by_category[t.category] = 0
                expenses_by_category[t.category] += t.amount

        if not expenses_by_category:
            print_info("No hay gastos en este mes para generar gráfico.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Export chart
        exporter = PNGExporter()
        filepath = exporter.export_bar_chart(
            expenses_by_category,
            title=f"Gastos por Categoría - {year}-{month:02d}",
            ylabel="Monto ($)"
        )

        print_success(f"Gráfico exportado a:\n[cyan]{filepath}[/cyan]")
        wait_for_continue()
        nav_stack.go_back()

    except Exception as e:
        print_error(f"Error durante exportación de gráfico: {e}")
        wait_for_continue()
        nav_stack.go_back()


def export_data(format_type: str) -> None:
    """
    Export data to file.

    Args:
        format_type: Export format (csv or json).
    """
    clear_screen()
    print_header()
    console.print()

    try:
        from budgetcli.database.models import Transaction

        service = TransactionService()
        transactions = service.get_all_transactions()

        if not transactions:
            print_info("No hay datos para exportar.")
            wait_for_continue()
            nav_stack.go_back()
            return

        # Export
        if format_type == "csv":
            exporter = CSVExporter()
            filepath = exporter.export_transactions(transactions)
        else:
            exporter = JSONExporter()
            filepath = exporter.export_transactions(transactions)

        # Show result
        clear_screen()
        print_header()
        console.print()
        print_success(f"Datos exportados a:\n{filepath}")

        wait_for_continue()
        nav_stack.go_back()

    except Exception as e:
        print_error(f"Error durante exportación: {e}")
        wait_for_continue()
        nav_stack.go_back()


# ============================================================================
# CONFIGURATION MENU
# ============================================================================


def configuration_menu() -> None:
    """Display configuration submenu."""
    clear_screen()
    print_header()
    console.print()

    choices = [
        questionary.Choice("Ver ruta de base de datos", value="db_path"),
        questionary.Choice("Hacer backup de datos", value="backup"),
        questionary.Choice("Acerca de BudgetCLI", value="about"),
        questionary.Choice("← Volver", value="back"),
    ]

    selected = questionary.select(
        "Configuración:",
        choices=choices,
        pointer="➤ ",
        use_shortcuts=False,
    ).ask()

    if selected is None or selected == "back":
        nav_stack.go_back()
    elif selected == "db_path":
        nav_stack.push(show_db_path)
    elif selected == "backup":
        nav_stack.push(make_backup)
    elif selected == "about":
        nav_stack.push(show_about)


def show_db_path() -> None:
    """Show database path."""
    clear_screen()
    print_header()
    console.print()

    from budgetcli.database.connection import DatabaseConnection

    db = DatabaseConnection()
    db_path = db.db_path

    print_info(f"Ruta de base de datos:\n[cyan]{db_path}[/cyan]")
    wait_for_continue()
    nav_stack.go_back()


def make_backup() -> None:
    """Make database backup."""
    clear_screen()
    print_header()
    console.print()

    try:
        import shutil
        from pathlib import Path

        from budgetcli.database.connection import DatabaseConnection

        db = DatabaseConnection()
        db_path = Path(db.db_path)

        # Create backups directory
        backups_dir = db_path.parent / "backups"
        backups_dir.mkdir(exist_ok=True)

        # Create backup filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = backups_dir / f"budget_{timestamp}.db"

        # Copy database
        shutil.copy2(db_path, backup_path)

        print_success(f"Backup creado en:\n[cyan]{backup_path}[/cyan]")
        wait_for_continue()
        nav_stack.go_back()

    except Exception as e:
        print_error(f"Error durante backup: {e}")
        wait_for_continue()
        nav_stack.go_back()


def show_about() -> None:
    """Show about information."""
    clear_screen()
    print_header()
    console.print()

    about_text = """
[cyan]BudgetCLI[/cyan] v0.0.2

[bold]Descripción:[/bold]
Gestor de finanzas personales 100% en terminal.
Organiza tus ingresos, gastos y presupuestos desde la línea de comandos.

[bold]Características:[/bold]
• Registro de transacciones (ingresos/gastos)
• Gestión de presupuestos mensuales
• Reportes y análisis financiero
• Exportación de datos (CSV/JSON)
• Interfaz interactiva en terminal

[bold]Licencia:[/bold]
MIT

[bold]GitHub:[/bold]
https://github.com/JUXCHXX/Budget-CLI
    """

    print_info(about_text)
    wait_for_continue()
    nav_stack.go_back()


def main_menu() -> None:
    """Main menu function for import."""
    from budgetcli.cli.tui import show_main_menu

    show_main_menu()

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-15

### Added

- Initial release of BudgetCLI
- Transaction management (income/expense tracking)
- Budget management with monthly limits
- Monthly expense reports with Rich tables
- ASCII bar charts for data visualization
- Financial summaries (income, expenses, balance)
- CSV and JSON export functionality
- PNG chart generation with matplotlib
- SQLite persistent storage
- Comprehensive validation system
- Full test suite with >80% coverage
- Professional CLI interface with Typer
- Rich terminal formatting with colors and panels

### Features

#### CLI Commands

- `budget init` - Initialize database
- `budget transaction add` - Add transactions
- `budget transaction list` - View transactions
- `budget transaction delete` - Delete transactions
- `budget budget set-budget` - Set category budgets
- `budget budget list` - View budgets
- `budget budget delete` - Delete budgets
- `budget report monthly` - View monthly report
- `budget report summary` - View financial summary
- `budget report chart` - Display ASCII chart
- `budget report export` - Export to CSV/JSON
- `budget report plot` - Generate PNG charts

#### Database

- Normalized SQLite schema
- Indexed queries for performance
- Transaction and Budget models
- Automatic schema initialization

#### Services

- `TransactionService` - Transaction management
- `BudgetService` - Budget management
- `ReportService` - Report generation
- `CalculationService` - Financial calculations

#### Utilities

- `ASCIIChart` - ASCII chart generation
- `CSVExporter` - CSV export
- `JSONExporter` - JSON export
- `PNGExporter` - PNG chart generation

#### Validation

- Input validation for all data
- Month format validation
- Amount and budget validation
- Type checking and error handling

#### Testing

- `test_validators.py` - Validator tests
- `test_calculations.py` - Calculation tests
- `test_services.py` - Service tests
- `test_exporters.py` - Exporter tests
- Pytest configuration and fixtures

### Documentation

- Comprehensive README.md
- Contributing guidelines
- Architecture documentation
- API docstrings
- Usage examples

---

## Planned Releases

### [1.1.0] - TBD

- Recurring transactions
- Budget alerts
- Multi-currency support
- Data import functionality
- Advanced filtering options

### [1.2.0] - TBD

- Investment tracking
- Tax report generation
- Financial goals
- Spending predictions

### [2.0.0] - TBD

- Web dashboard
- Mobile app
- Cloud sync
- Bank integration

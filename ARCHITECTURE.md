# BudgetCLI Architecture

## Overview

BudgetCLI follows **Clean Architecture** principles to ensure maintainability, testability, and scalability. The application is organized into distinct layers with clear responsibilities.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer (Typer)                     │
│              (User Input/Output Handling)                │
│  ┌──────────────┬──────────────┬──────────────┐          │
│  │transactions  │    budgets   │    reports   │          │
│  └──────────────┴──────────────┴──────────────┘          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           Business Logic Layer (Core)                    │
│     (No External Dependencies, Pure Logic)              │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │  Services    │Calculations  │  Validators  │         │
│  └──────────────┴──────────────┴──────────────┘         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           Data Access Layer (Database)                   │
│            (SQLite, Models, Migrations)                 │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ Connection   │    Models    │ Migrations   │         │
│  └──────────────┴──────────────┴──────────────┘         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   SQLite Database                        │
│      (Persistent Data Storage on File System)           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                Utilities Layer (Utils)                    │
│           (Charts, Exporters, Helpers)                  │
│  ┌──────────────┬──────────────┐                        │
│  │ASCIIChart    │  Exporters   │                        │
│  │(CSV, JSON)   │  (PNG)       │                        │
│  └──────────────┴──────────────┘                        │
└──────────────────────────────────────────────────────────┘
```

## Layers in Detail

### 1. CLI Layer (Presentation)

**Location:** `budgetcli/cli/`

**Responsibility:** Handle user input and output

**Contains:**
- `main.py` - Application entry point and setup
- `transactions.py` - Transaction commands
- `budgets.py` - Budget commands
- `reports.py` - Report and export commands

**Key Principles:**
- No business logic or calculations
- Only orchestrates services
- Uses Rich for terminal formatting
- Uses Typer for CLI framework
- All input validation delegated to services

**Example:**

```python
# CLI only orchestrates - no logic
@app.command("add")
def add_transaction(
    type: str = typer.Option(...),
    category: str = typer.Option(...),
    amount: float = typer.Option(...),
    date_str: str = typer.Option(...),
):
    """Add transaction (just orchestrate the service)"""
    try:
        transaction_service = TransactionService()
        transaction = transaction_service.add_transaction(
            type, category, amount, date_str
        )
        console.print(f"[green]✓[/green] Added: {transaction}")
    except ValidationError as e:
        console.print(f"[red]✗[/red] {e}")
```

### 2. Core Business Logic Layer

**Location:** `budgetcli/core/`

**Responsibility:** All business logic and domain operations

#### 2.1 Services (`services.py`)

**Entities:**
- `TransactionService` - Manage transactions (add, get, delete)
- `BudgetService` - Manage budgets (set, get, delete)
- `ReportService` - Generate reports

**Characteristics:**
- Independent of framework or infrastructure
- Pure Python business logic
- Testable without external dependencies
- Handle database orchestration

**Example:**

```python
class TransactionService:
    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        date: str,
    ) -> Transaction:
        # Validate input
        TransactionValidator.validate_all_transaction_fields(...)

        # Persist data
        db = DatabaseConnection()
        cursor.execute("INSERT INTO transactions...")

        # Return domain object
        return Transaction(...)
```

#### 2.2 Calculations (`calculations.py`)

**Responsibility:** Financial calculations

**Contains:**
- Monthly totals calculation
- Income/expense summaries
- Budget overflow detection
- Currency formatting

**Characteristics:**
- Pure functions (no side effects)
- Operates on in-memory data
- High test coverage

**Example:**

```python
class CalculationService:
    @staticmethod
    def calculate_balance(transactions, year, month) -> float:
        income = CalculationService.calculate_monthly_income(...)
        expenses = CalculationService.calculate_monthly_expenses(...)
        return income - expenses
```

#### 2.3 Validators (`validators.py`)

**Responsibility:** Input validation and error handling

**Contains:**
- `TransactionValidator` - Validate transaction data
- `BudgetValidator` - Validate budget data
- Custom `ValidationError` exception

**Characteristics:**
- Centralized validation logic
- Clear error messages
- Type-safe validation

**Example:**

```python
class TransactionValidator:
    @staticmethod
    def validate_type(transaction_type: str) -> None:
        valid_types = {"income", "expense"}
        if transaction_type not in valid_types:
            raise ValidationError(f"Invalid type: {transaction_type}")
```

### 3. Data Access Layer (Database)

**Location:** `budgetcli/database/`

**Responsibility:** Database operations and schema management

#### 3.1 Models (`models.py`)

**Contains:**
- Domain models using Pydantic
- `Transaction` model
- `Budget` model
- `MonthlySummary` model

**Characteristics:**
- Type-safe data models
- Built-in validation
- Serializable to JSON

**Example:**

```python
class Transaction(BaseModel):
    id: Optional[int] = None
    type: TransactionType
    category: str
    amount: float = Field(..., gt=0)
    date: str
    note: Optional[str] = ""
```

#### 3.2 Connection (`connection.py`)

**Contains:**
- `DatabaseConnection` - SQLite connection management
- `DatabaseMigration` - Schema initialization

**Characteristics:**
- Context manager support
- Thread-safe connections
- Schema versioning ready

#### 3.3 Migrations (`migrations.py`)

**Contains:**
- `init_db()` - Initialize database
- `reset_db()` - Reset database

**Characteristics:**
- Idempotent operations
- Schema versioning support

### 4. Utilities Layer

**Location:** `budgetcli/utils/`

**Responsibility:** Helper functions, exporters, and utilities

#### 4.1 ASCII Charts (`ascii_charts.py`)

**Contains:**
- `ASCIIChart` - Generate ASCII bar/pie charts

#### 4.2 Exporters (`exporters.py`)

**Contains:**
- `CSVExporter` - Export to CSV
- `JSONExporter` - Export to JSON
- `PNGExporter` - Export to PNG (matplotlib)
- Base `BaseExporter` - Common functionality

**Characteristics:**
- Plugin-like architecture
- Extensible for new formats
- Error handling

## Data Flow

### Add Transaction Flow

```
1. User Input (CLI)
   └─> budget transaction add --type expense --amount 100

2. CLI Command Handler
   └─> TransactionService.add_transaction()

3. Validation Layer
   └─> TransactionValidator.validate_all_transaction_fields()

4. Business Logic
   └─> CalculationService.calculate_monthly_totals()

5. Data Access
   └─> DatabaseConnection.execute()

6. SQLite Database
   └─> INSERT INTO transactions

7. Response
   └─> Display success/error message
```

### Get Report Flow

```
1. User Input
   └─> budget report monthly --month 2026-04

2. CLI Handler
   └─> ReportService.get_monthly_summary()

3. Data Retrieval
   └─> TransactionService.get_transactions_by_month()
   └─> BudgetService.get_all_budgets()

4. Calculations
   └─> CalculationService.calculate_monthly_totals()
   └─> CalculationService.check_budget_exceeded()

5. Report Generation
   └─> Create MonthlySummary objects

6. Presentation
   └─> Format with Rich tables
   └─> Display to user
```

## Design Patterns Used

### 1. Service Pattern
- `TransactionService`, `BudgetService`, `ReportService`
- Encapsulates business logic
- Dependency injection ready

### 2. Repository Pattern
- Services act as repositories
- Abstract data access operations
- Easy to mock for testing

### 3. Dependency Injection
- Services accept `db_path` parameter
- Makes testing easy
- Testable database path

### 4. Factory Pattern
- Model creation (Transaction, Budget)
- Database connection creation

### 5. Context Manager Pattern
- Database connection cleanup
- Ensures resources are released

### 6. Validator Pattern
- Centralized validation
- Reusable validators
- Clear error messages

## Testing Strategy

### Unit Tests

```
budgetcli/tests/
├── test_validators.py      # Validation logic
├── test_calculations.py    # Financial calculations
├── test_services.py        # Service operations
└── test_exporters.py       # Export functionality
```

**Coverage:** >80%

**Key Testing Principles:**
- Test in isolation (no external dependencies)
- Use temporary databases for DB tests
- Mock external services
- Test happy path and error cases

### Integration Tests

- Done through service tests
- Use temporary database
- Test full workflows

## Extension Points

### Adding New Export Format

```python
class XMLExporter(BaseExporter):
    def export_transactions(self, transactions):
        # Implement XML export
        pass
```

### Adding New Command

```python
# In cli/budgets.py or new file
@app.command("list-by-spent")
def list_budgets_by_spent():
    # Implement new command
    pass
```

### Adding New Calculation

```python
# In core/calculations.py
@staticmethod
def calculate_annual_summary(transactions, year):
    # Implement new calculation
    pass
```

## Dependency Management

### Internal Dependencies

```
CLI Layer
  ↓↓↓
Core Services ↔ Core Validators ↔ Core Calculations
  ↓↓↓
Database Connection ↔ Database Models
```

**Rule:** No circular dependencies allowed

### External Dependencies

| Layer | Dependencies |
|-------|--------------|
| CLI | Typer, Rich |
| Core | Pydantic |
| Database | sqlite3 |
| Utils | matplotlib (optional) |

## Performance Considerations

### Database Optimization

- Indices on frequently filtered columns (date, category, type)
- Normalized schema
- Connection pooling ready

### Caching Opportunities

- Monthly calculations (can cache)
- Budget lookups (small dataset)
- Category list (static during session)

### Query Optimization

- Filter at database level when possible
- Limit results when appropriate
- Use indices effectively

## Security Considerations

- SQL injection prevention (parameterized queries)
- Input validation (centralized)
- No hardcoded credentials
- Environment variable support for database path

## Future Architecture Changes

### Planned Improvements

1. **Database Abstraction Layer**
   - Support multiple database backends
   - Migration tools

2. **Event System**
   - Business events (TransactionAdded, BudgetExceeded)
   - Event listeners/subscribers

3. **Plugin System**
   - Custom exporters
   - Custom calculators

4. **Caching Layer**
   - Redis support (optional)
   - In-memory cache

5. **API Layer**
   - REST API (optional)
   - GraphQL support (future)

## Conclusion

BudgetCLI's architecture prioritizes:
- **Maintainability** through clear separation of concerns
- **Testability** through dependency injection
- **Scalability** through modular design
- **Extensibility** through well-defined interfaces
- **Clarity** through comprehensive documentation

This ensures the codebase can grow while remaining manageable and understandable.

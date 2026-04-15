# Arquitectura de BudgetCLI

## Resumen General

BudgetCLI sigue los principios de **Arquitectura Limpia** para garantizar mantenibilidad, testeabilidad y escalabilidad. La aplicación está organizada en capas distintas con responsabilidades claras.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                  Capa CLI (Typer)                        │
│        (Manejo de Entrada/Salida del Usuario)           │
│  ┌──────────────┬──────────────┬──────────────┐          │
│  │transacciones │  presupuestos│   reportes   │          │
│  └──────────────┴──────────────┴──────────────┘          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│        Capa de Lógica de Negocio (Core)                 │
│   (Sin Dependencias Externas, Lógica Pura)             │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │   Servicios  │ Cálculos     │  Validadores │         │
│  └──────────────┴──────────────┴──────────────┘         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│        Capa de Acceso a Datos (Base de Datos)           │
│      (SQLite, Modelos, Migraciones)                     │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │  Conexión    │    Modelos   │  Migraciones │         │
│  └──────────────┴──────────────┴──────────────┘         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│               Base de Datos SQLite                       │
│    (Almacenamiento Persistente en Sistema de Archivos) │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│            Capa de Utilidades (Utils)                    │
│       (Gráficos, Exportadores, Ayudantes)              │
│  ┌──────────────┬──────────────┐                        │
│  │ Gráficos ASCII│ Exportadores │                        │
│  │(CSV, JSON)   │  (PNG)       │                        │
│  └──────────────┴──────────────┘                        │
└──────────────────────────────────────────────────────────┘
```

## Capas en Detalle

### 1. Capa CLI (Presentación)

**Ubicación:** `budgetcli/cli/`

**Responsabilidad:** Manejar entrada y salida del usuario

**Contiene:**
- `main.py` - Punto de entrada de la aplicación
- `transactions.py` - Comandos de transacciones
- `budgets.py` - Comandos de presupuestos
- `reports.py` - Comandos de reportes y exportación

**Principios Clave:**
- Sin lógica de negocio o cálculos
- Solo orquesta servicios
- Usa Rich para formato de terminal
- Usa Typer como framework CLI
- Toda validación delegada a servicios

**Ejemplo:**

```python
# CLI solo orquesta - sin lógica
@app.command("add")
def add_transaction(
    type: str = typer.Option(...),
    category: str = typer.Option(...),
    amount: float = typer.Option(...),
    date_str: str = typer.Option(...),
):
    """Añadir transacción (solo orquestar el servicio)"""
    try:
        transaction_service = TransactionService()
        transaction = transaction_service.add_transaction(
            type, category, amount, date_str
        )
        console.print(f"[green]✓[/green] Añadido: {transaction}")
    except ValidationError as e:
        console.print(f"[red]✗[/red] {e}")
```

### 2. Capa de Lógica de Negocio (Core)

**Ubicación:** `budgetcli/core/`

**Responsabilidad:** Toda lógica de negocio y operaciones de dominio

#### 2.1 Servicios (`services.py`)

**Entidades:**
- `TransactionService` - Gestionar transacciones (añadir, obtener, eliminar)
- `BudgetService` - Gestionar presupuestos (establecer, obtener, eliminar)
- `ReportService` - Generar reportes

**Características:**
- Independiente del framework o infraestructura
- Lógica Python pura de negocio
- Testeable sin dependencias externas
- Manejan orquestación de base de datos

**Ejemplo:**

```python
class TransactionService:
    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        date: str,
    ) -> Transaction:
        # Validar entrada
        TransactionValidator.validate_all_transaction_fields(...)

        # Persistir datos
        db = DatabaseConnection()
        cursor.execute("INSERT INTO transactions...")

        # Retornar objeto de dominio
        return Transaction(...)
```

#### 2.2 Cálculos (`calculations.py`)

**Responsabilidad:** Cálculos financieros

**Contiene:**
- Cálculo de totales mensuales
- Resúmenes de ingresos/gastos
- Detección de exceso de presupuesto
- Formato de moneda

**Características:**
- Funciones puras (sin efectos secundarios)
- Opera con datos en memoria
- Cobertura de pruebas alta

**Ejemplo:**

```python
class CalculationService:
    @staticmethod
    def calculate_balance(transactions, year, month) -> float:
        income = CalculationService.calculate_monthly_income(...)
        expenses = CalculationService.calculate_monthly_expenses(...)
        return income - expenses
```

#### 2.3 Validadores (`validators.py`)

**Responsabilidad:** Validación de entrada y manejo de errores

**Contiene:**
- `TransactionValidator` - Validar datos de transacciones
- `BudgetValidator` - Validar datos de presupuestos
- Excepción personalizada `ValidationError`

**Características:**
- Lógica de validación centralizada
- Mensajes de error claros
- Validación type-safe

**Ejemplo:**

```python
class TransactionValidator:
    @staticmethod
    def validate_type(transaction_type: str) -> None:
        valid_types = {"income", "expense"}
        if transaction_type not in valid_types:
            raise ValidationError(f"Tipo inválido: {transaction_type}")
```

### 3. Capa de Acceso a Datos (Base de Datos)

**Ubicación:** `budgetcli/database/`

**Responsabilidad:** Operaciones de base de datos y gestión de esquema

#### 3.1 Modelos (`models.py`)

**Contiene:**
- Modelos de dominio usando Pydantic
- Modelo `Transaction`
- Modelo `Budget`
- Modelo `MonthlySummary`

**Características:**
- Modelos de datos type-safe
- Validación integrada
- Serializables a JSON

**Ejemplo:**

```python
class Transaction(BaseModel):
    id: Optional[int] = None
    type: TransactionType
    category: str
    amount: float = Field(..., gt=0)
    date: str
    note: Optional[str] = ""
```

#### 3.2 Conexión (`connection.py`)

**Contiene:**
- `DatabaseConnection` - Gestión de conexiones SQLite
- `DatabaseMigration` - Inicialización de esquema

**Características:**
- Soporte para context manager
- Conexiones thread-safe
- Versionado de esquema listo

#### 3.3 Migraciones (`migrations.py`)

**Contiene:**
- `init_db()` - Inicializar base de datos
- `reset_db()` - Resetear base de datos

**Características:**
- Operaciones idempotentes
- Soporte versionado de esquema

### 4. Capa de Utilidades

**Ubicación:** `budgetcli/utils/`

**Responsabilidad:** Funciones auxiliares, exportadores y utilidades

#### 4.1 Gráficos ASCII (`ascii_charts.py`)

**Contiene:**
- `ASCIIChart` - Generar gráficos ASCII de barras/pastel

#### 4.2 Exportadores (`exporters.py`)

**Contiene:**
- `CSVExporter` - Exportar a CSV
- `JSONExporter` - Exportar a JSON
- `PNGExporter` - Exportar a PNG (matplotlib)
- Base `BaseExporter` - Funcionalidad común

**Características:**
- Arquitectura tipo plugin
- Extensible para nuevos formatos
- Manejo de errores

## Flujo de Datos

### Flujo de Añadir Transacción

```
1. Entrada del Usuario (CLI)
   └─> budget transaction add --type expense --amount 100

2. Manejador de Comandos CLI
   └─> TransactionService.add_transaction()

3. Capa de Validación
   └─> TransactionValidator.validate_all_transaction_fields()

4. Lógica de Negocio
   └─> CalculationService.calculate_monthly_totals()

5. Acceso a Datos
   └─> DatabaseConnection.execute()

6. Base de Datos SQLite
   └─> INSERT INTO transactions

7. Respuesta
   └─> Mostrar mensaje de éxito/error
```

### Flujo de Obtener Reporte

```
1. Entrada del Usuario
   └─> budget report monthly --month 2026-04

2. Manejador CLI
   └─> ReportService.get_monthly_summary()

3. Obtención de Datos
   └─> TransactionService.get_transactions_by_month()
   └─> BudgetService.get_all_budgets()

4. Cálculos
   └─> CalculationService.calculate_monthly_totals()
   └─> CalculationService.check_budget_exceeded()

5. Generación de Reporte
   └─> Crear objetos MonthlySummary

6. Presentación
   └─> Formato con tablas Rich
   └─> Mostrar al usuario
```

## Patrones de Diseño Utilizados

### 1. Patrón Service
- `TransactionService`, `BudgetService`, `ReportService`
- Encapsula lógica de negocio
- Inyección de dependencias lista

### 2. Patrón Repository
- Los servicios actúan como repositorios
- Abstraen operaciones de acceso a datos
- Fácil de mockear para testing

### 3. Inyección de Dependencias
- Servicios aceptan parámetro `db_path`
- Facilita testing
- Ruta de base de datos testeable

### 4. Patrón Factory
- Creación de modelos (Transaction, Budget)
- Creación de conexión de base de datos

### 5. Patrón Context Manager
- Limpieza de conexión de base de datos
- Garantiza liberación de recursos

### 6. Patrón Validator
- Validación centralizada
- Validadores reutilizables
- Mensajes de error claros

## Estrategia de Testing

### Pruebas Unitarias

```
budgetcli/tests/
├── test_validators.py      # Lógica de validación
├── test_calculations.py    # Cálculos financieros
├── test_services.py        # Operaciones de servicio
└── test_exporters.py       # Funcionalidad de exportación
```

**Cobertura:** >80%

**Principios Clave de Testing:**
- Testear en aislamiento (sin dependencias externas)
- Usar bases de datos temporales para pruebas DB
- Mockear servicios externos
- Testear casos feliz y de error

### Pruebas de Integración

- Hechas a través de pruebas de servicio
- Usar base de datos temporal
- Testear workflows completos

## Puntos de Extensión

### Añadir Nuevo Formato de Exportación

```python
class XMLExporter(BaseExporter):
    def export_transactions(self, transactions):
        # Implementar exportación XML
        pass
```

### Añadir Nuevo Comando

```python
# En cli/budgets.py o archivo nuevo
@app.command("list-by-spent")
def list_budgets_by_spent():
    # Implementar nuevo comando
    pass
```

### Añadir Nuevo Cálculo

```python
# En core/calculations.py
@staticmethod
def calculate_annual_summary(transactions, year):
    # Implementar nuevo cálculo
    pass
```

## Gestión de Dependencias

### Dependencias Internas

```
Capa CLI
  ↓↓↓
Servicios Core ↔ Validadores Core ↔ Cálculos Core
  ↓↓↓
Conexión de BD ↔ Modelos de BD
```

**Regla:** No se permiten dependencias circulares

### Dependencias Externas

| Capa | Dependencias |
|------|--------------|
| CLI | Typer, Rich |
| Core | Pydantic |
| Base de Datos | sqlite3 |
| Utils | matplotlib (opcional) |

## Consideraciones de Rendimiento

### Optimización de Base de Datos

- Índices en columnas frecuentemente filtradas (date, category, type)
- Esquema normalizado
- Connection pooling listo

### Oportunidades de Caché

- Cálculos mensuales (se pueden cachear)
- Búsquedas de presupuesto (conjunto pequeño)
- Lista de categorías (estática durante sesión)

### Optimización de Consultas

- Filtrar a nivel de base de datos cuando sea posible
- Limitar resultados cuando sea apropiado
- Usar índices efectivamente

## Consideraciones de Seguridad

- Prevención de inyección SQL (consultas parametrizadas)
- Validación de entrada (centralizada)
- Sin credenciales hardcodeadas
- Soporte para variables de entorno para ruta de BD

## Cambios de Arquitectura Futuros

### Mejoras Planeadas

1. **Capa de Abstracción de Base de Datos**
   - Soportar múltiples backends de BD
   - Herramientas de migración

2. **Sistema de Eventos**
   - Eventos de negocio (TransactionAdded, BudgetExceeded)
   - Escuchadores/suscriptores de eventos

3. **Sistema de Plugins**
   - Exportadores personalizados
   - Calculadores personalizados

4. **Capa de Caché**
   - Soporte Redis (opcional)
   - Caché en memoria

5. **Capa API**
   - API REST (opcional)
   - Soporte GraphQL (futuro)

## Conclusión

La arquitectura de BudgetCLI prioriza:
- **Mantenibilidad** mediante separación clara de responsabilidades
- **Testeabilidad** mediante inyección de dependencias
- **Escalabilidad** mediante diseño modular
- **Extensibilidad** mediante interfaces bien definidas
- **Claridad** mediante documentación comprensiva

Esto garantiza que la base de código pueda crecer mientras permanece manejable y comprensible.

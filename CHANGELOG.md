# Registro de Cambios

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato se basa en [Mantener un Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionamiento Semántico](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-15

### Agregado

- Lanzamiento inicial de BudgetCLI
- Gestión de transacciones (seguimiento de ingresos/gastos)
- Gestión de presupuestos con límites mensuales
- Reportes de gastos mensuales con tablas Rich
- Gráficos ASCII de barras para visualización de datos
- Resúmenes financieros (ingresos, gastos, balance)
- Funcionalidad de exportación CSV y JSON
- Generación de gráficos PNG con matplotlib
- Almacenamiento persistente SQLite
- Sistema de validación completo
- Suite de pruebas completa con cobertura >80%
- Interfaz CLI profesional con Typer
- Formato de terminal Rich con colores y paneles

### Características

#### Comandos CLI

- `budget init` - Inicializar base de datos
- `budget transaction add` - Añadir transacciones
- `budget transaction list` - Ver transacciones
- `budget transaction delete` - Eliminar transacciones
- `budget budget set-budget` - Establecer presupuestos por categoría
- `budget budget list` - Ver presupuestos
- `budget budget delete` - Eliminar presupuestos
- `budget report monthly` - Ver reporte mensual
- `budget report summary` - Ver resumen financiero
- `budget report chart` - Mostrar gráfico ASCII
- `budget report export` - Exportar a CSV/JSON
- `budget report plot` - Generar gráficos PNG

#### Base de Datos

- Esquema SQLite normalizado
- Consultas indexadas para rendimiento
- Modelos Transaction y Budget
- Inicialización automática de esquema

#### Servicios

- `TransactionService` - Gestión de transacciones
- `BudgetService` - Gestión de presupuestos
- `ReportService` - Generación de reportes
- `CalculationService` - Cálculos financieros

#### Utilidades

- `ASCIIChart` - Generación de gráficos ASCII
- `CSVExporter` - Exportación a CSV
- `JSONExporter` - Exportación a JSON
- `PNGExporter` - Generación de gráficos PNG

#### Validación

- Validación de entrada para todos los datos
- Validación de formato de mes
- Validación de cantidad y presupuesto
- Verificación de tipos y manejo de errores

#### Testing

- `test_validators.py` - Pruebas de validadores
- `test_calculations.py` - Pruebas de cálculos
- `test_services.py` - Pruebas de servicios
- `test_exporters.py` - Pruebas de exportadores
- Configuración de pytest y fixtures

### Documentación

- README.md completo
- Directrices de contribución
- Documentación de arquitectura
- Docstrings de API
- Ejemplos de uso

---

## Lanzamientos Planeados

### [1.1.0] - Por Determinar

- Transacciones recurrentes
- Alertas de presupuesto
- Soporte de múltiples monedas
- Funcionalidad de importación de datos
- Opciones de filtrado avanzado

### [1.2.0] - Por Determinar

- Seguimiento de inversiones
- Generación de reportes fiscales
- Objetivos financieros
- Predicción de gastos

### [2.0.0] - Por Determinar

- Dashboard web
- Aplicación móvil
- Sincronización en la nube
- Integración bancaria

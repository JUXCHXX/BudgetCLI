# Registro de Cambios

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato se basa en [Mantener un Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionamiento Semántico](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-04-17

### Agregado

- **Interfaz TUI Interactiva**: Nueva experiencia de usuario completamente interactiva desde la terminal
- **Comando `budget start`**: Nuevo comando para lanzar la interfaz interactiva
- **Animación de Apertura**: Animación ASCII con barra de progreso al iniciar la TUI
- **Menú Principal Interactivo**: Navegación con flechas y Enter para todas las opciones
- **Submenú Transacciones**: Agregar ingresos/gastos, ver historial, eliminar con interfaz visual
- **Submenú Presupuestos**: Definir, ver y eliminar presupuestos con indicador de % usado
- **Submenú Reportes**: Reportes mensuales, resumen financiero, exportación CSV/JSON
- **Submenú Configuración**: Ver ruta de BD, hacer backups, información de la app
- **Sistema de Navegación Global**: Stack de navegación para "Volver" entre menús

### Cambios

- Versión actualizada a 0.0.2
- Dependencia `questionary>=2.0.0` agregada para menús interactivos

### Archivos

- `budgetcli/cli/tui.py` - Módulo principal de TUI con animación y menú
- `budgetcli/cli/tui_menus.py` - Implementación de todos los submenús
- `budgetcli/cli/tui_utils.py` - Utilidades y helpers para la TUI
- `budgetcli/tests/test_tui.py` - Suite de pruebas para TUI

### Compatibilidad

- Todos los comandos CLI existentes siguen funcionando normalmente
- La TUI es una capa adicional que no afecta la interfaz de línea de comandos tradicional
- Tests existentes permanecen en 40/40 passing con cobertura >80%

---

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

```
██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗         ██████╗██╗     ██╗
██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝        ██╔════╝██║     ██║
██████╔╝██║   ██║██║  ██║██║  ███╗█████╗     ██║    ████   ██║     ██║     ██║
██╔══██╗██║   ██║██║  ██║██║   ██║██╔══╝     ██║           ██║     ██║     ██║
██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗   ██║           ╚██████╗███████╗██║
╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝            ╚═════╝╚══════╝╚═╝
```

<div align="center">

**Tu gestor de finanzas personales desde la terminal.**
Ahora con interfaz interactiva. Navega con flechas. Sin memorizar comandos.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/version-0.0.2-0D9E75?style=flat-square)](https://github.com/JUXCHXX/BudgetCLI/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-085041?style=flat-square)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000?style=flat-square)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6366f1?style=flat-square)](https://github.com/JUXCHXX/BudgetCLI/blob/main/CONTRIBUTING.md)
[![Tests](https://img.shields.io/badge/Tests-40%2F40%20passing-0D9E75?style=flat-square&logo=pytest&logoColor=white)](https://github.com/JUXCHXX/BudgetCLI)

[Instalación](#-instalación) · [Modo interactivo](#-modo-interactivo--budget-start) · [Comandos clásicos](#-comandos-clásicos) · [Stack](#-stack-tecnológico) · [Historia](#-historia-del-proyecto) · [Contribuir](#-contribuir)

</div>

---

## ¿Qué hay de nuevo en v0.0.2?

La v0.0.1 era poderosa pero exigía recordar subcomandos y flags. La v0.0.2 introduce una **interfaz interactiva completa** navegable con el teclado, manteniendo el 100% de retrocompatibilidad con todo lo anterior.

| | v0.0.1 | v0.0.2 |
|---|---|---|
| Forma de uso | `budget transaction add --type expense ...` | `budget start` → menú |
| Navegación | Memorizar flags y argumentos | Flechas `↑` `↓` + `Enter` |
| Pantalla de inicio | Ninguna | Animación ASCII + barra de carga |
| Volver atrás | No disponible | `← Volver` en cada submenú |
| Formularios | Una línea larga con flags | Paso a paso con validación |
| Retrocompatibilidad | — | ✅ 100%, nada cambia |

---

## ✨ Características

```
🚀 budget start      →  Interfaz interactiva completa — navega con flechas
📝 Transacciones     →  Registra ingresos y gastos con formulario paso a paso
💵 Presupuestos      →  Define límites y ve el % usado en tiempo real
📊 Reportes          →  Resúmenes comparativos presupuesto vs. realidad
📈 Gráficos ASCII    →  Visualiza gastos directamente en la terminal
📤 Exportación       →  CSV y JSON para análisis en Excel u otras tools
🖼️  Gráficos PNG      →  Pie charts y bar charts con matplotlib
🚨 Alertas           →  Notificación automática al exceder presupuesto
💾 SQLite local      →  Base de datos en tu máquina, cero dependencias cloud
🔁 Volver atrás      →  Navegación con pila — nunca te quedas atascado
```

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.11+** — verifica con `python --version`
- **pip** — incluido con Python

### 1. Clona el repositorio

```bash
git clone https://github.com/JUXCHXX/BudgetCLI.git
cd BudgetCLI
```

### 2. Instala el paquete

```bash
# Instalación estándar
pip install -e .

# Para contribuidores (incluye herramientas de desarrollo)
pip install -e ".[dev]"
```

### 3. Inicializa la base de datos

```bash
budget init
```

La base de datos se crea automáticamente en `~/.budgetcli/budget.db`.

### 4. Lanza la interfaz interactiva

```bash
budget start
```

---

## 🎮 Modo interactivo — `budget start`

Al ejecutar `budget start`, la terminal muestra una animación ASCII de apertura con barra de progreso y luego el menú principal:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗║
║  ...                                                 ║
║                                                      ║
║       Tu dinero. Tu terminal. Tu control.            ║
╚══════════════════════════════════════════════════════╝

  Inicializando...  [████████████████████] 100%  Listo.
```

```
╭─ BudgetCLI v0.0.2 ────────────────────────────────────╮
│                                                        │
│   ¿Qué deseas hacer?                                   │
│                                                        │
│   > Transacciones                                      │
│     Presupuestos                                       │
│     Reportes                                           │
│     Configuración                                      │
│     Salir                                              │
│                                                        │
╰────────────────────────────────────────────────────────╯

  Navega con  ↑ ↓  y confirma con  Enter
```

### 📋 Submenú — Transacciones

```
> Agregar ingreso
  Agregar gasto
  Ver historial
  Eliminar transacción
  ← Volver
```

**Agregar ingreso / gasto** — formulario paso a paso:
1. Selecciona categoría de una lista o escribe una nueva
2. Ingresa el monto (con validación numérica automática)
3. Elige la fecha — por defecto es el día de hoy
4. Añade una nota opcional
5. Se muestra un resumen y se pide confirmación antes de guardar

**Ver historial** — tabla completa con opción de filtrar por mes. Paginación automática cada 20 registros.

**Eliminar transacción** — selecciona por ID, confirmación obligatoria antes de borrar.

---

### 💰 Submenú — Presupuestos

```
> Definir presupuesto mensual
  Ver presupuestos activos
  Eliminar presupuesto
  ← Volver
```

**Ver presupuestos activos** incluye una columna de **% usado en tiempo real** con indicadores visuales:

```
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Categoría       ┃ Gastado   ┃ Límite    ┃ Restante   ┃ Estado            ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Comida          │   250,000 │   500,000 │    250,000 │ ✓ Bien (50%)      │
│ Transporte      │   190,000 │   200,000 │     10,000 │ ⚠️  Casi al límite │
│ Entretenimiento │   120,000 │   100,000 │    -20,000 │ ❌ EXCEDIDO       │
└─────────────────┴───────────┴───────────┴────────────┴───────────────────┘
```

---

### 📊 Submenú — Reportes

```
> Reporte mensual
  Resumen financiero
  Gráfico ASCII
  Exportar gráfico PNG
  Exportar datos (CSV / JSON)
  ← Volver
```

Todos los reportes piden el mes en formato `YYYY-MM` (por defecto el mes actual). Los archivos exportados se guardan en `./exports/`.

---

### ⚙️ Submenú — Configuración

```
> Ver ruta de base de datos
  Hacer backup de datos
  Resetear base de datos
  Acerca de BudgetCLI
  ← Volver
```

**Hacer backup** — copia la base de datos a `~/.budgetcli/backups/budget_YYYY-MM-DD_HHmmss.db` con timestamp automático.

**Resetear base de datos** — requiere escribir `CONFIRMAR` manualmente. No hay marcha atrás.

---

### 🔁 Navegación y función "Volver atrás"

Cada submenú tiene la opción **← Volver** al final. La navegación funciona sobre una pila interna: puedes entrar y salir de cualquier nivel sin perder el contexto. Presiona `Ctrl+C` en cualquier momento y la app preguntará si deseas salir antes de cerrar.

---

## 🖥️ Comandos clásicos

Los comandos de v0.0.1 siguen disponibles sin ningún cambio. Si prefieres la línea de comandos directa, todo funciona exactamente igual.

### `budget transaction`

| Comando | Descripción |
|---|---|
| `transaction add --type expense --category "X" --amount N --date YYYY-MM-DD [--note "..."]` | Registra un gasto |
| `transaction add --type income --category "X" --amount N --date YYYY-MM-DD [--note "..."]` | Registra un ingreso |
| `transaction list` | Lista todas las transacciones |
| `transaction delete --id <ID>` | Elimina una transacción por ID |

### `budget budget`

| Comando | Descripción |
|---|---|
| `budget set-budget --category "X" --limit N` | Crea o actualiza un presupuesto |
| `budget list` | Muestra todos los presupuestos activos |
| `budget delete --category "X"` | Elimina el presupuesto de una categoría |

### `budget report`

| Comando | Descripción |
|---|---|
| `report monthly --month YYYY-MM` | Reporte mensual con comparativa vs. presupuesto |
| `report summary --month YYYY-MM` | Resumen de ingresos, gastos y balance |
| `report chart --month YYYY-MM` | Gráfico ASCII de gastos por categoría |
| `report plot --month YYYY-MM --type pie\|bar [--output nombre]` | Gráfico PNG exportable |
| `report export --format csv\|json [--month YYYY-MM]` | Exportación de datos |

> **Formato de fecha:** siempre `YYYY-MM-DD` (ej: `2026-04-15`). Para `--month`, usa `YYYY-MM`.

---

## 🛠️ Stack tecnológico

| Paquete | Versión | Uso |
|---|---|---|
| `click` | `>=8.0` | Framework CLI — comandos, argumentos y flags |
| `rich` | `>=13.0` | Tablas, colores, paneles, animaciones y Live display |
| `questionary` | `>=2.0` | Menús interactivos navegables con flechas ← **nuevo** |
| `pydantic` | `>=2.0` | Modelos de datos con validación type-safe |
| `sqlite3` | stdlib | Base de datos local — sin instalación adicional |
| `matplotlib` | `>=3.7` | Generación de gráficos PNG exportables |

---

## 🗂️ Estructura del proyecto

```
BudgetCLI/
├── budgetcli/
│   ├── cli/
│   │   ├── main.py           ← Punto de entrada (budget + budget start)
│   │   ├── transaction.py    ← Comandos clásicos de transacciones
│   │   ├── budget.py         ← Comandos clásicos de presupuestos
│   │   ├── report.py         ← Comandos clásicos de reportes
│   │   ├── tui.py            ← NUEVO: animación + menú principal
│   │   ├── tui_menus.py      ← NUEVO: submenús interactivos
│   │   └── tui_utils.py      ← NUEVO: helpers de navegación y go_back()
│   ├── core/
│   │   ├── models.py
│   │   ├── database.py
│   │   └── engine.py
│   └── utils/
│       ├── ascii_charts.py
│       └── exporters.py
├── tests/
│   └── test_tui.py           ← NUEVO
├── exports/                   ← Gráficos y datos exportados (generado)
├── pyproject.toml            ← version = "0.0.2"
└── requirements.txt          ← + questionary>=2.0
```

**Datos generados en uso:**

```
~/.budgetcli/
├── budget.db                          ← Tu base de datos SQLite (privada)
└── backups/
    └── budget_2026-04-18_143000.db   ← Backups con timestamp

./exports/
├── transactions_2026-04.csv
├── transactions_2026-04.json
├── chart_2026-04_pie.png
└── chart_2026-04_bar.png
```

---

## 🏗️ Arquitectura

BudgetCLI sigue los principios de **Arquitectura Limpia** con cuatro capas independientes:

```
┌─────────────────────────────────────────────────────────┐
│                  Capa CLI (Click + TUI)                 │
│     Entrada/salida del usuario — sin lógica de negocio  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Capa Core (Servicios + Validadores)        │
│         Lógica de negocio pura — sin dependencias UI    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           Capa Database (SQLite + Pydantic)             │
│          Modelos, conexión y migraciones locales        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 Capa Utils (Extras)                     │
│         Gráficos ASCII, exportadores PNG/CSV/JSON       │
└─────────────────────────────────────────────────────────┘
```

---

## ⚖️ ¿Por qué BudgetCLI?

| | BudgetCLI | Apps tradicionales |
|---|---|---|
| **Privacidad** | 100% local, datos en tu PC | Datos en servidores externos |
| **Velocidad** | Comando en < 1 segundo | Login, carga, navegación... |
| **Control** | Tu base de datos, tus reglas | Exportación limitada |
| **Sin internet** | Funciona 100% offline | Requiere conexión |
| **Costo** | Gratis, open source | Freemium / suscripción |

---

## 🧪 Desarrollo y tests

```bash
# Instalar con dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar la suite completa de tests
pytest -v

# Ver cobertura de código
pytest --cov=budgetcli --cov-report=term-missing

# Formatear código
black budgetcli/ tests/
```

---

## 📝 Historia del proyecto

Este proyecto nació como una iniciativa personal de **Juan Florián (JUXCHXX)**, desarrollador que prefiere la terminal sobre cualquier interfaz gráfica. Frustrado con las apps de finanzas que exigen registro, envían datos a la nube y tienen interfaces sobrecargadas, decidió construir su propia solución desde cero.

La **v0.0.1** fue construida sobre una arquitectura limpia en capas con SQLite como motor de persistencia, Click para los comandos, Rich para el formato visual y Pydantic para validación. Desde el inicio se priorizó la calidad: tests unitarios, cobertura superior al 80%, pre-commit hooks con Black y documentación técnica completa en `ARCHITECTURE.md`.

La **v0.0.2** surge de un problema práctico: registrar ingresos, gastos y categorías escribiendo flags y argumentos largos era tedioso en el día a día. La solución fue añadir una capa TUI con menús interactivos navegables usando `questionary` y `rich.live`, manteniendo el 100% de retrocompatibilidad con los comandos anteriores. Nada se rompió — solo se añadió.

---

## 🗓️ Changelog

### v0.0.2 — Abril 2026
- **Nuevo:** comando `budget start` con interfaz TUI interactiva completa
- **Nuevo:** animación ASCII de apertura con barra de progreso animada
- **Nuevo:** menú principal y submenús navegables con flechas (`questionary`)
- **Nuevo:** función `← Volver` con pila de navegación global (`go_back()`)
- **Nuevo:** formularios paso a paso con validación en tiempo real
- **Nuevo:** paginación automática en historial de transacciones
- **Nuevo:** columna `% usado` en tiempo real en vista de presupuestos
- **Nuevo:** backup automático con timestamp desde el menú de Configuración
- **Nuevo:** captura global de `Ctrl+C` con confirmación antes de salir
- **Mejorado:** manejo de errores en TUI con paneles de error en rojo
- Todos los comandos anteriores permanecen sin cambios

### v0.0.1 — Marzo 2026
- Lanzamiento inicial — transacciones, presupuestos, reportes, exportación CSV/JSON/PNG

---

## 📄 Documentación técnica

| Documento | Contenido |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Estructura interna, capas, flujos de datos y patrones |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Guía completa para contribuidores |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial detallado de versiones |
| [`ROADMAP.md`](ROADMAP.md) | Features planeadas para versiones futuras |

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz **fork** del repositorio
2. Crea una rama descriptiva: `git checkout -b feature/nueva-funcionalidad`
3. Haz tus cambios con tests incluidos
4. Asegúrate de que `pytest -v` pase al 100%
5. Abre un **Pull Request** con descripción clara

Lee [`CONTRIBUTING.md`](CONTRIBUTING.md) para la guía completa de contribución.

---

## 📬 Soporte

- **Bugs:** [Abre un issue](https://github.com/JUXCHXX/BudgetCLI/issues)
- **Ideas o preguntas:** [Inicia una discusión](https://github.com/JUXCHXX/BudgetCLI/discussions)
- **Contribuciones:** [Pull Requests](https://github.com/JUXCHXX/BudgetCLI/pulls)

---

## 📝 Licencia

Distribuido bajo la licencia [MIT](LICENSE). Úsalo libremente, incluso en proyectos comerciales.

---

<div align="center">

**Hecho con ❤️ para quienes prefieren la terminal sobre cualquier app.**

```bash
pip install -e . && budget init && budget start
```

</div>

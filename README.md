<<<<<<< HEAD
<div align="center">

```
██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗ ██████╗██╗     ██╗
██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝██╔════╝██║     ██║
██████╔╝██║   ██║██║  ██║██║  ███╗█████╗     ██║   ██║     ██║     ██║
██╔══██╗██║   ██║██║  ██║██║   ██║██╔══╝     ██║   ██║     ██║     ██║
██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗   ██║   ╚██████╗███████╗██║
╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝╚══════╝╚═╝
```

**Tu gestor de finanzas personales desde la terminal.**
Rápido. Privado. Sin complicaciones.

<br/>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-40%2F40%20passing-22c55e?style=flat-square&logo=pytest&logoColor=white)]()
[![Code style: black](https://img.shields.io/badge/Code%20style-black-000000?style=flat-square)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6366f1?style=flat-square)](CONTRIBUTING.md)

<br/>

[Instalación](#-instalación) · [Tutorial rápido](#-tutorial-rápido) · [Comandos](#-referencia-de-comandos) · [Arquitectura](#-arquitectura) · [Contribuir](#-contribuir)

</div>

---

## ¿Por qué BudgetCLI?

La mayoría de apps de finanzas personales requieren cuenta, envían tus datos a la nube y tienen interfaces sobrecargadas. BudgetCLI es diferente:

| | BudgetCLI | Apps tradicionales |
|---|---|---|
| **Privacidad** | 100% local, datos en tu PC | Datos en servidores externos |
| **Velocidad** | Comando en < 1 segundo | Login, carga, navegación... |
| **Control** | Tu base de datos, tus reglas | Exportación limitada |
| **Sin internet** | Funciona offline | Requiere conexión |
| **Costo** | Gratis, open source | Freemium / suscripción |

---

## ✨ Características

```
📝 Transacciones    →  Registra ingresos y gastos con categorías y notas
💵 Presupuestos     →  Define límites mensuales por categoría
📊 Reportes         →  Resúmenes comparativos presupuesto vs. realidad
📈 Gráficos ASCII   →  Visualiza gastos directamente en la terminal
📤 Exportación      →  CSV y JSON para análisis en Excel u otras tools
🖼️  Gráficos PNG     →  Pie charts y bar charts profesionales con matplotlib
🚨 Alertas          →  Notificación automática al exceder presupuesto
💾 SQLite local     →  Base de datos en tu máquina, cero dependencias cloud
```

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.11+** — verifica con `python --version`
- **pip** — incluido con Python

### 1. Clona el repositorio

```bash
git clone https://github.com/JUXCHXX/Budget-CLI.git
cd Budget-CLI
```

> **Sin Git?** Descarga el ZIP desde GitHub, descomprímelo y entra a la carpeta.

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

### 4. Verifica la instalación

```bash
budget --help
```

Deberías ver el menú de ayuda con todos los subcomandos disponibles. ✓

---

## 📚 Tutorial rápido

Un flujo completo de ejemplo para el mes de abril:

### Paso 1 — Define tu presupuesto mensual

```bash
budget budget set-budget --category "Comida"           --limit 500000
budget budget set-budget --category "Transporte"       --limit 200000
budget budget set-budget --category "Entretenimiento"  --limit 100000
budget budget set-budget --category "Servicios"        --limit 300000
```

Verifica que todo quedó bien:

```bash
budget budget list
```

### Paso 2 — Registra tus ingresos

```bash
budget transaction add \
  --type income \
  --category "Salario" \
  --amount 5000000 \
  --date 2026-04-01 \
  --note "Salario mensual"
```

### Paso 3 — Registra tus gastos del mes

```bash
# Comida
budget transaction add --type expense --category "Comida" \
  --amount 25000 --date 2026-04-15 --note "Almuerzo en restaurante"

# Transporte
budget transaction add --type expense --category "Transporte" \
  --amount 80000 --date 2026-04-10 --note "Gasolina"

# Entretenimiento
budget transaction add --type expense --category "Entretenimiento" \
  --amount 35000 --date 2026-04-08 --note "Cine"
```

### Paso 4 — Revisa tu historial

```bash
budget transaction list
```

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Date         ┃ Type     ┃ Category        ┃ Amount     ┃ Note                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ 2026-04-01   │ income   │ Salario         │  5,000,000 │ Salario mensual       │
│ 2026-04-08   │ expense  │ Entretenimiento │     35,000 │ Cine                  │
│ 2026-04-10   │ expense  │ Transporte      │     80,000 │ Gasolina              │
│ 2026-04-15   │ expense  │ Comida          │     25,000 │ Almuerzo              │
└──────────────┴──────────┴─────────────────┴────────────┴───────────────────────┘
```

### Paso 5 — Genera el reporte mensual

```bash
budget report monthly --month 2026-04
```

```
┌──────────────────────── Monthly Report — 2026-04 ─────────────────────────┐
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Category        ┃ Spent     ┃ Budget    ┃ Remaining  ┃ Status            ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Comida          │   250,000 │   500,000 │    250,000 │ ✓ Bien            │
│ Transporte      │   150,000 │   200,000 │     50,000 │ ✓ Bien            │
│ Entretenimiento │   120,000 │   100,000 │    -20,000 │ ❌ EXCEDIDO       │
│ Servicios       │   298,000 │   300,000 │      2,000 │ ⚠️  Casi al límite │
└─────────────────┴───────────┴───────────┴────────────┴───────────────────┘
```

### Paso 6 — Resumen financiero del mes

```bash
budget report summary --month 2026-04
```

```
┌─────────────────────────────────────┐
│      Monthly Summary — 2026-04      │
├─────────────────────────────────────┤
│  Income    │           5,000,000    │
│  Expenses  │             818,000    │
│  Balance   │           4,182,000    │
└────────────┴────────────────────────┘
```

### Paso 7 — Visualiza tus datos

```bash
# Gráfico ASCII en la terminal (sin dependencias extras)
budget report chart --month 2026-04

# Pie chart PNG para presentaciones
budget report plot --month 2026-04 --type pie

# Bar chart con nombre personalizado
budget report plot --month 2026-04 --type bar --output gastos_abril
```

Los gráficos se guardan automáticamente en `./exports/`.

### Paso 8 — Exporta para análisis externo

```bash
# Para Excel u otras herramientas
budget report export --format csv --month 2026-04

# Para APIs, scripts o procesamiento programático
budget report export --format json --month 2026-04
```

---

## 📖 Referencia de comandos

### `budget transaction`

| Comando | Descripción |
|---|---|
| `transaction add --type expense --category "X" --amount N --date YYYY-MM-DD [--note "..."]` | Registra un gasto |
| `transaction add --type income  --category "X" --amount N --date YYYY-MM-DD [--note "..."]` | Registra un ingreso |
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

## 🗂️ Archivos del proyecto

```
Budget-CLI/
├── budgetcli/
│   ├── cli/            # Comandos CLI (Click)
│   │   ├── main.py     # Punto de entrada
│   │   ├── transaction.py
│   │   ├── budget.py
│   │   └── report.py
│   ├── core/           # Lógica de negocio
│   │   ├── models.py
│   │   ├── database.py
│   │   └── engine.py
│   └── utils/          # Helpers (formateo, gráficos, exportación)
├── tests/              # Suite de tests (40/40 passing)
├── exports/            # Gráficos y archivos exportados (generado)
├── pyproject.toml
└── README.md
```

**Datos generados en uso:**

```
~/.budgetcli/
└── budget.db          ← Tu base de datos SQLite (privada, solo tuya)

./exports/
├── transactions_2026-04.csv
├── transactions_2026-04.json
├── chart_2026-04_pie.png
└── chart_2026-04_bar.png
```

---

## ⚙️ Configuración avanzada

### Ruta personalizada de base de datos

```bash
export BUDGETCLI_DB_PATH=/ruta/a/tu/budget.db
budget init
```

### Hacer backup de tus datos

```bash
cp ~/.budgetcli/budget.db ~/.budgetcli/budget_backup_$(date +%Y-%m-%d).db
```

### Resetear todo y comenzar desde cero

> ⚠️ **Advertencia:** Esta acción elimina todos los datos permanentemente.

```bash
rm ~/.budgetcli/budget.db
budget init
```

---

## 🛠️ Solución de problemas

<details>
<summary><strong>❌ "Comando no encontrado" al ejecutar <code>budget</code></strong></summary>

Reinstala el paquete asegurándote de estar en la carpeta del proyecto:

```bash
pip install -e .
```

O ejecuta directamente con Python:

```bash
python -m budgetcli.cli.main --help
```

</details>

<details>
<summary><strong>❌ "Database permission error"</strong></summary>

Verifica los permisos del directorio de datos:

```bash
ls -la ~/.budgetcli/
```

Si el problema persiste, recrea la base de datos:

```bash
rm ~/.budgetcli/budget.db
budget init
```

</details>

<details>
<summary><strong>❌ Errores de importación (ImportError)</strong></summary>

Instala con todas las dependencias de desarrollo:

```bash
pip install -e ".[dev]"
```

</details>

<details>
<summary><strong>❌ "Fecha inválida"</strong></summary>

El formato requerido es `YYYY-MM-DD`:

```bash
--date 2026-04-15   ✓ Correcto
--date 15-04-2026   ✗ Incorrecto
--date 15/04/2026   ✗ Incorrecto
```

</details>

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

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz **fork** del repositorio
2. Crea una rama descriptiva: `git checkout -b feature/nueva-funcionalidad`
3. Haz tus cambios con tests incluidos
4. Asegúrate de que `pytest -v` pase al 100%
5. Abre un **Pull Request** con descripción clara

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para la guía completa de contribución.

---

## 📄 Documentación técnica

| Documento | Contenido |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Estructura interna del código |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guía para contribuidores |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones |
| [ROADMAP.md](ROADMAP.md) | Features planeadas |

---

## 📬 Soporte

- **Bugs:** [Abre un issue](https://github.com/JUXCHXX/Budget-CLI/issues)
- **Ideas o preguntas:** [Inicia una discusión](https://github.com/JUXCHXX/Budget-CLI/discussions)
- **Contribuciones:** [Pull Requests](https://github.com/JUXCHXX/Budget-CLI/pulls)

---

## 📝 Licencia

Distribuido bajo la licencia [MIT](LICENSE). Úsalo libremente, incluso en proyectos comerciales.

---

<div align="center">

**Hecho con ❤️ para quienes prefieren la terminal sobre cualquier app.**

```bash
# Empieza ahora mismo
pip install -e . && budget init && budget --help
```

</div>
=======
# BudgetCLI
💰 Gestor de finanzas personales desde la terminal — registra ingresos y gastos, define presupuestos mensuales, visualiza tus gastos con gráficos ASCII y PNG, exporta a CSV/JSON. Basado en SQLite, 100% local y sin internet. Sin nube. Sin suscripciones. Tu dinero, tu máquina. 🖥️
>>>>>>> 48dab826e6b980251586dc4ad1fd6b9fdd11cda0

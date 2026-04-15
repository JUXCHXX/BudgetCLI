# Contribuyendo a BudgetCLI

¡Gracias por tu interés en contribuir a BudgetCLI! Este documento proporciona directrices e instrucciones para contribuir.

## Código de Conducta

Por favor sé respetuoso y constructivo en todas las interacciones.

## Comenzar

### Requisitos Previos

- Python 3.11+
- Git
- Familiaridad con aplicaciones CLI y Python

### Configurar Entorno de Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/Budget-CLI.git
cd Budget-CLI

# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar en modo desarrollo con todas las dependencias
pip install -e ".[dev]"
```

## Flujo de Desarrollo

### 1. Crear una Rama de Característica

```bash
git checkout -b feature/nombre-de-tu-caracteristica
# o
git checkout -b fix/tu-corrección-de-bug
```

### 2. Realizar Cambios

- Seguir la guía de estilo PEP 8
- Mantener commits enfocados y descriptivos
- Añadir pruebas para nueva funcionalidad
- Actualizar documentación según sea necesario

### 3. Verificaciones de Calidad de Código

```bash
# Formatear con black
black budgetcli

# Linting con ruff
ruff check budgetcli --fix

# Verificación de tipos con mypy
mypy budgetcli

# Ejecutar pruebas
pytest

# Ejecutar pruebas con cobertura
pytest --cov=budgetcli
```

### 4. Hacer Commit de Cambios

```bash
git commit -m "feat: agregar nueva característica" -m "Descripción detallada de cambios"
```

Usa formato de commit convencional:
- `feat:` para nuevas características
- `fix:` para correcciones de bugs
- `docs:` para documentación
- `test:` para pruebas
- `refactor:` para refactorización

### 5. Push y Crear Pull Request

```bash
git push origin feature/nombre-de-tu-caracteristica
```

Luego crea un pull request en GitHub.

## Directrices de Arquitectura

### Principios de Arquitectura Limpia

1. **Capa CLI** (`budgetcli/cli/`):
   - Solo orquestar servicios
   - Sin lógica de negocio
   - Manejar entrada/salida del usuario con Rich

2. **Lógica de Negocio** (`budgetcli/core/`):
   - Todos los cálculos y lógica
   - Servicios para operaciones de dominio
   - Validación centralizada

3. **Acceso a Datos** (`budgetcli/database/`):
   - Gestión de conexiones SQLite
   - Esquema y modelos
   - Operaciones de base de datos solamente

4. **Utilidades** (`budgetcli/utils/`):
   - Funcionalidad de exportación
   - Generación de gráficos
   - Funciones auxiliares

### Organización de Archivos

- Una clase de servicio por archivo
- Nombres de módulo claros y descriptivos
- Docstrings completos
- Type hints en todas las funciones

## Requisitos de Testing

- Mínimo 80% de cobertura de código
- Pruebas unitarias para todos los métodos de servicio
- Pruebas de validación para todos los validadores
- Testear casos extremos y condiciones de error

### Escribir Pruebas

```python
# budgetcli/tests/test_feature.py
import pytest
from budgetcli.core.services import SomeService

@pytest.fixture
def temp_db():
    """Configurar base de datos temporal."""
    with tempfile.TemporaryDirectory() as tmpdir:
        init_db(str(Path(tmpdir) / "test.db"))
        yield str(Path(tmpdir) / "test.db")

def test_feature_success(temp_db):
    """Testear operación exitosa."""
    service = SomeService(temp_db)
    result = service.do_something()
    assert result is not None

def test_feature_error():
    """Testear manejo de errores."""
    with pytest.raises(ValidationError):
        service.do_something_invalid()
```

## Documentación

### Formato de Docstring

Usar docstrings estilo Google:

```python
def add_transaction(
    transaction_type: str,
    category: str,
    amount: float,
    date: str,
    note: str = "",
) -> Transaction:
    """
    Añadir una nueva transacción.

    Args:
        transaction_type: Tipo de transacción (income/expense).
        category: Nombre de la categoría.
        amount: Monto de la transacción.
        date: Fecha en formato ISO (YYYY-MM-DD).
        note: Nota opcional de la transacción.

    Returns:
        Objeto de transacción creado.

    Raises:
        ValidationError: Si la validación falla.
        RepositoryException: Si la operación de base de datos falla.
    """
```

### Actualizar README

Si añades características, actualiza:
- Lista de características
- Ejemplos de uso
- Diagrama de arquitectura (si aplica)

## Problemas Comunes

### Errores de Base de Datos

```bash
# Resetear base de datos durante desarrollo
python -c "from budgetcli.database import reset_db; reset_db()"
```

### Errores de Importación

```bash
# Reinstalar en modo desarrollo
pip install -e "."
```

### Fallos en Pruebas

```bash
# Limpiar caché de Python
find . -type d -name __pycache__ -exec rm -r {} +
pytest --cache-clear
```

## Consideraciones de Rendimiento

- Minimizar consultas de base de datos
- Usar índices para columnas frecuentemente filtradas
- Cachear cálculos cuando sea apropiado
- Perfilar operaciones lentas

## Seguridad

- Validar todas las entradas del usuario
- Usar consultas parametrizadas (hecho a través de adaptadores SQLite)
- No almacenar datos sensibles en texto plano
- Mantener dependencias actualizadas

## Lista de Verificación para Lanzamiento

- [ ] Todas las pruebas pasando
- [ ] Cobertura de código ≥ 80%
- [ ] Documentación actualizada
- [ ] CHANGELOG actualizado
- [ ] Versión bumped (versionamiento semántico)
- [ ] Tag creado: `git tag v1.0.0`

## ¿Preguntas?

- Revisa issues y discusiones existentes
- Crea una nueva discusión para preguntas
- Revisa código existente para patrones

## Reconocimiento

Los contribuidores serán reconocidos en:
- CONTRIBUTORS.md
- Página de contribuidores de GitHub
- Notas de lanzamiento

¡Gracias por contribuir! 🎉

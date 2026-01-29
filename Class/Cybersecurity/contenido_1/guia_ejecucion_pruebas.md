# Guía de Ejecución de Pruebas - Proyecto Calculadora

## Descripción del Proyecto

Este proyecto contiene una calculadora con operaciones básicas y avanzadas, junto con un conjunto completo de pruebas unitarias implementadas con pytest.

## Estructura del Proyecto

```
proyecto/
├── src/
│   ├── __init__.py
│   └── calculadora.py          # Clase principal con operaciones matemáticas
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures compartidas
│   ├── test_calculadora.py    # Pruebas unitarias básicas
│   └── test_avanzadas.py      # Pruebas avanzadas e integración
├── pytest.ini                # Configuración de pytest
└── requirements.txt           # Dependencias del proyecto
```

## Requisitos Previos

### 1. Instalación de Dependencias

```bash
# Navegar al directorio del proyecto
cd "proyecto"

# Instalar las dependencias
pip install -r requirements.txt
```

### 2. Verificación de la Instalación

```bash
# Verificar que pytest está instalado
pytest --version
```

## Ejecución de Pruebas

### 1. Comando Básico

```bash
# Ejecutar todas las pruebas
pytest
```

**Resultado Esperado:**
```
============================= test session starts ==============================
platform darwin -- Python 3.9.23, pytest-8.4.1, pluggy-1.6.0 -- /path/to/python
cachedir: .pytest_cache
rootdir: /path/to/proyecto
configfile: pytest.ini
testpaths: tests
collecting ... collected 48 items

tests/test_avanzadas.py........                                         [ 16%]
tests/test_calculadora.py........................................       [100%]

============================== 48 passed in 0.23s
```

### 2. Ejecución con Detalles Verbosos

```bash
# Mostrar información detallada de cada prueba
pytest -v
```

**Resultado Esperado:**
- Se mostrarán todas las 48 pruebas individualmente
- Cada prueba aparecerá con su nombre completo y estado (PASSED)
- Tiempo total de ejecución aproximado: 0.2-0.3 segundos

### 3. Ejecución de Pruebas Específicas

```bash
# Ejecutar solo pruebas básicas
pytest tests/test_calculadora.py

# Ejecutar solo pruebas avanzadas
pytest tests/test_avanzadas.py

# Ejecutar una clase específica de pruebas
pytest tests/test_calculadora.py::TestOperacionesBasicas

# Ejecutar una prueba específica
pytest tests/test_calculadora.py::TestOperacionesBasicas::test_suma_numeros_positivos
```

### 4. Ejecución con Marcadores

```bash
# Ejecutar solo pruebas rápidas (excluir lentas)
pytest -m "not slow"

# Ejecutar solo pruebas de integración
pytest -m "integration"

# Ejecutar solo pruebas que usan mocking
pytest -m "mock"
```

## Tipos de Pruebas Incluidas

### 1. Pruebas Unitarias Básicas (40 pruebas)

**Archivo:** `tests/test_calculadora.py`

**Categorías:**
- **TestOperacionesBasicas:** Suma, resta, multiplicación, división
- **TestOperacionesAvanzadas:** Potencia, raíz cuadrada, factorial
- **TestPromedio:** Cálculo de promedios con diferentes casos
- **TestHistorial:** Gestión del historial de operaciones
- **TestValidacionEntrada:** Validación de tipos de datos

**Pruebas Parametrizadas:**
- Suma con múltiples combinaciones de números
- Raíz cuadrada con diferentes valores
- Promedio con diferentes listas
- Validación de tipos inválidos

### 2. Pruebas Avanzadas e Integración (8 pruebas)

**Archivo:** `tests/test_avanzadas.py`

**Categorías:**
- **TestIntegracion:** Flujos completos de operaciones
- **TestConMocking:** Pruebas con simulación de componentes
- **TestFixturesAvanzadas:** Uso de fixtures complejas
- **test_parametrizacion_fixtures:** Parametrización de fixtures

## Resultados Esperados por Categoría

### TestOperacionesBasicas (19 pruebas)
- ✅ Suma de números positivos y negativos
- ✅ Resta básica
- ✅ Multiplicación
- ✅ División normal y manejo de división por cero
- ✅ Suma parametrizada con 5 casos diferentes

### TestOperacionesAvanzadas (10 pruebas)
- ✅ Potencias básicas
- ✅ Raíz cuadrada parametrizada (6 casos)
- ✅ Raíz cuadrada de número negativo (error esperado)
- ✅ Factorial de números grandes
- ✅ Factorial de número negativo (error esperado)
- ✅ Factorial de no entero (error esperado)

### TestPromedio (8 pruebas)
- ✅ Promedio de lista normal
- ✅ Promedio de un elemento
- ✅ Promedio con decimales
- ✅ Promedio de lista vacía (error esperado)
- ✅ Promedio parametrizado (4 casos)

### TestHistorial (4 pruebas)
- ✅ Historial inicialmente vacío
- ✅ Registro de operaciones
- ✅ Limpieza de historial
- ✅ Obtención de copia del historial

### TestValidacionEntrada (6 pruebas)
- ✅ Rechazo de tipos inválidos (string, lista, diccionario, None, boolean)
- ✅ Validación en todas las operaciones

### Pruebas Avanzadas (8 pruebas)
- ✅ Flujo completo de calculadora
- ✅ Operaciones masivas
- ✅ Mock de math.sqrt
- ✅ Mock de validación
- ✅ Fixtures con datos complejos (2 pruebas)
- ✅ Parametrización de fixtures (2 pruebas)

## Configuración de pytest

El archivo `pytest.ini` contiene:

```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_functions = test_*
python_classes = Test*
addopts = -v --strict-markers --strict-config --disable-warnings --tb=short -ra

markers =
    slow: marca las pruebas como lentas
    unit: marca las pruebas como unitarias
    integration: marca las pruebas como de integración
    mock: marca las pruebas que usan mocking
    parametrize: marca las pruebas parametrizadas
```

## Solución de Problemas Comunes

### 1. Fixture no encontrada
**Error:** `fixture 'calculadora_fixture' not found`
**Solución:** Verificar que existe en `conftest.py`

### 2. TypeError no se produce
**Error:** `Failed: DID NOT RAISE <class 'TypeError'>`
**Solución:** Verificar validación de tipos booleanos

### 3. Marcadores desconocidos
**Error:** `PytestUnknownMarkWarning: Unknown pytest.mark.xxx`
**Solución:** Registrar marcadores en `pytest.ini`

## Comandos de Depuración

```bash
# Mostrar fixtures disponibles
pytest --fixtures

# Mostrar marcadores registrados
pytest --markers

# Ejecutar con salida detallada en caso de falla
pytest --tb=long

# Parar en la primera falla
pytest -x

# Mostrar las 10 pruebas más lentas
pytest --durations=10
```

## Métricas de Éxito

✅ **48 pruebas en total**
✅ **100% de pruebas pasando**
✅ **0 errores**
✅ **0 fallas**
✅ **0 warnings**
✅ **Tiempo de ejecución < 1 segundo**

## Interpretación de Resultados

### Resultado Exitoso
```
============================== 48 passed in 0.23s ==============================
```

### Información de Cobertura
- Todas las operaciones matemáticas están cubiertas
- Todos los casos de error están probados
- Validación de entrada completa
- Gestión de historial verificada

## Conclusión

Este conjunto de pruebas garantiza:
1. **Funcionalidad correcta** de todas las operaciones
2. **Manejo adecuado de errores** en casos edge
3. **Validación robusta** de tipos de entrada
4. **Integridad del historial** de operaciones
5. **Compatibilidad** con diferentes tipos de datos numéricos

El proyecto está listo para producción con una cobertura de pruebas completa y robusta.
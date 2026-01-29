# ============================================================================
# ARCHIVO 2: tests/conftest.py (Fixtures compartidas)
# ============================================================================

"""
Configuración de fixtures compartidas para todas las pruebas
Define datos de prueba reutilizables con diferentes scopes
"""

import pytest
from typing import List, Dict, Any
from src.calculadora import Calculadora

# Fixtures de instancias
@pytest.fixture
def calculadora_limpia():
    """
    Fixture que proporciona una calculadora nueva para cada prueba
    Scope: function (por defecto)
    """
    return Calculadora()

@pytest.fixture
def calculadora_con_historial(calculadora_limpia):
    """
    Fixture que proporciona una calculadora con historial previo
    Útil para probar funcionalidades de historial
    """
    calc = calculadora_limpia
    # Agregar algunas operaciones al historial
    calc.sumar(5, 3)
    calc.multiplicar(2, 4)
    calc.dividir(10, 2)
    return calc

# Fixtures de datos de prueba
@pytest.fixture
def numeros_enteros_positivos():
    """Números enteros positivos para pruebas"""
    return [1, 2, 3, 4, 5, 10, 100, 1000]

@pytest.fixture
def numeros_decimales():
    """Números decimales para pruebas de precisión"""
    return [1.5, 2.7, 3.14159, 0.1, 0.333333]

@pytest.fixture
def numeros_negativos():
    """Números negativos para casos edge"""
    return [-1, -5, -10, -100, -0.5]

@pytest.fixture
def casos_division_cero():
    """Casos que deberían generar ZeroDivisionError"""
    return [
        (10, 0),
        (0, 0),
        (-5, 0),
        (3.14, 0.0)
    ]

@pytest.fixture
def datos_complejos():
    """
    Fixture con estructura de datos compleja para pruebas avanzadas
    Scope: session (se crea una vez por sesión)
    """
    return {
        'operaciones_basicas': [
            {'a': 2, 'b': 3, 'suma': 5, 'resta': -1, 'mult': 6, 'div': 0.666667},
            {'a': 10, 'b': 5, 'suma': 15, 'resta': 5, 'mult': 50, 'div': 2.0},
            {'a': -4, 'b': 2, 'suma': -2, 'resta': -6, 'mult': -8, 'div': -2.0}
        ],
        'potencias': [
            {'base': 2, 'exp': 3, 'resultado': 8},
            {'base': 5, 'exp': 2, 'resultado': 25},
            {'base': 10, 'exp': 0, 'resultado': 1}
        ],
        'factoriales': [
            {'n': 0, 'factorial': 1},
            {'n': 1, 'factorial': 1},
            {'n': 5, 'factorial': 120},
            {'n': 10, 'factorial': 3628800}
        ]
    }

# Fixtures con diferentes scopes para demostración
@pytest.fixture(scope="class")
def calculadora_clase():
    """Fixture con scope de clase - se crea una vez por clase de pruebas"""
    return Calculadora()

@pytest.fixture(scope="module")
def datos_modulo():
    """Fixture con scope de módulo - se crea una vez por archivo"""
    return {"configuracion": "datos_compartidos_modulo"}

@pytest.fixture(scope="session")
def configuracion_global():
    """Fixture con scope de sesión - se crea una vez por sesión completa"""
    return {
        "precision_decimales": 10,
        "timeout_operaciones": 5.0,
        "max_operaciones_historial": 1000
    }

# Fixtures con cleanup (teardown)
@pytest.fixture
def calculadora_con_cleanup():
    """
    Ejemplo de fixture con cleanup automático usando yield
    Todo después del yield se ejecuta como teardown
    """
    calc = Calculadora()
    
    # Setup: configuración inicial si fuera necesaria
    print("\\nSetup: Inicializando calculadora")
    
    yield calc  # Aquí se ejecuta la prueba
    
    # Teardown: limpieza después de la prueba
    print("\\nTeardown: Limpiando calculadora")
    calc.limpiar_historial()

# Fixture parametrizable para test_parametrizacion_fixtures
@pytest.fixture
def calculadora_fixture(request):
    """
    Fixture que permite parametrización indirecta de otras fixtures
    """
    if request.param == "calculadora_limpia":
        return Calculadora()
    elif request.param == "calculadora_con_historial":
        calc = Calculadora()
        calc.sumar(5, 3)
        calc.multiplicar(2, 4)
        calc.dividir(10, 2)
        return calc
    else:
        raise ValueError(f"Parámetro desconocido: {request.param}")
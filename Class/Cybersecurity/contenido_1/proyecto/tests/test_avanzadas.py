# ============================================================================
# ARCHIVO 4: tests/test_avanzadas.py (Pruebas avanzadas)
# ============================================================================

"""
Pruebas avanzadas que demuestran técnicas específicas de Pytest
Incluye mocking, fixtures complejas, y pruebas de integración
"""

import pytest
from unittest.mock import patch, MagicMock
from src.calculadora import Calculadora

class TestIntegracion:
    """
    Pruebas de integración que prueban workflows completos
    Marcadas con marker 'integration'
    """
    
    @pytest.mark.integration
    def test_flujo_completo_calculadora(self, calculadora_limpia):
        """
        Prueba un flujo completo de uso de la calculadora
        Simula uso real con múltiples operaciones
        """
        calc = calculadora_limpia
        
        # Flujo: (5 + 3) * 2 = 16, luego √16 = 4
        suma = calc.sumar(5, 3)          # 8
        producto = calc.multiplicar(suma, 2)  # 16
        raiz = calc.raiz_cuadrada(producto)   # 4.0
        
        assert suma == 8
        assert producto == 16
        assert raiz == 4.0
        
        # Verificar que todas las operaciones están en el historial
        historial = calc.obtener_historial()
        assert len(historial) == 3
        assert any("5 + 3 = 8" in op for op in historial)
        assert any("8 × 2 = 16" in op for op in historial)
        assert any("√16 = 4.0" in op for op in historial)
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_operaciones_masivas(self, calculadora_limpia):
        """
        Prueba rendimiento con muchas operaciones
        Verificar que no hay memory leaks en el historial
        """
        calc = calculadora_limpia
        
        # Realizar 1000 operaciones
        for i in range(1000):
            calc.sumar(i, 1)
        
        assert len(calc.obtener_historial()) == 1000
        
        # Verificar que la última operación es correcta
        ultimo_resultado = calc.sumar(1000, 1)
        assert ultimo_resultado == 1001

@pytest.mark.mock
class TestConMocking:
    """
    Pruebas que demuestran el uso de mocking
    Útil para aislar componentes y simular comportamientos
    """
    
    def test_mock_math_sqrt(self, calculadora_limpia):
        """
        Ejemplo de mock de función externa (math.sqrt)
        Demuestra cómo aislar dependencias externas
        """
        with patch('src.calculadora.math.sqrt') as mock_sqrt:
            # Configurar el mock para retornar un valor específico
            mock_sqrt.return_value = 42.0
            
            resultado = calculadora_limpia.raiz_cuadrada(16)
            
            # Verificar que se usó el mock
            mock_sqrt.assert_called_once_with(16)
            assert resultado == 42.0
    
    def test_mock_validacion(self, calculadora_limpia):
        """
        Ejemplo de mock de método interno
        Útil para probar comportamientos específicos
        """
        with patch.object(calculadora_limpia, '_validar_numeros') as mock_validar:
            # El mock permite que la validación "pase" siempre
            mock_validar.return_value = None
            
            # Esta operación normalmente fallaría por tipo de dato
            # Pero el mock permite que continúe
            resultado = calculadora_limpia.sumar("5", "3")  # Normalmente TypeError
            
            # Verificar que se llamó la validación
            mock_validar.assert_called_once_with("5", "3")

class TestFixturesAvanzadas:
    """
    Pruebas que demuestran el uso de fixtures avanzadas
    Incluye fixtures con parámetros y scopes diferentes
    """
    
    def test_datos_complejos_operaciones_basicas(self, datos_complejos, calculadora_limpia):
        """
        Prueba usando fixture con datos complejos
        Demuestra cómo reutilizar datos de prueba estructurados
        """
        for caso in datos_complejos['operaciones_basicas']:
            a, b = caso['a'], caso['b']
            
            assert calculadora_limpia.sumar(a, b) == caso['suma']
            calculadora_limpia.limpiar_historial()  # Limpiar entre pruebas
            
            assert calculadora_limpia.restar(a, b) == caso['resta']
            calculadora_limpia.limpiar_historial()
            
            assert calculadora_limpia.multiplicar(a, b) == caso['mult']
            calculadora_limpia.limpiar_historial()
            
            assert calculadora_limpia.dividir(a, b) == pytest.approx(caso['div'], abs=1e-5)
            calculadora_limpia.limpiar_historial()
    
    def test_datos_complejos_factoriales(self, datos_complejos, calculadora_limpia):
        """Prueba factoriales usando datos de fixture compleja"""
        for caso in datos_complejos['factoriales']:
            resultado = calculadora_limpia.factorial(caso['n'])
            assert resultado == caso['factorial']

@pytest.mark.parametrize("calculadora_fixture", [
    "calculadora_limpia",
    "calculadora_con_historial"
], indirect=True)
def test_parametrizacion_fixtures(calculadora_fixture):
    """
    Ejemplo avanzado: parametrización de fixtures
    Permite probar el mismo comportamiento con diferentes configuraciones
    """
    # Esta prueba se ejecutará una vez con cada fixture
    assert hasattr(calculadora_fixture, 'sumar')
    assert hasattr(calculadora_fixture, 'historial')
    
    # La prueba se adapta al tipo de fixture
    resultado = calculadora_fixture.sumar(1, 1)
    assert resultado == 2
# ============================================================================
# ARCHIVO 3: tests/test_calculadora.py (Pruebas principales)
# ============================================================================

"""
Suite completa de pruebas para la clase Calculadora
Demuestra diferentes tipos de pruebas y técnicas con Pytest
"""

import pytest
import math
from src.calculadora import Calculadora

class TestOperacionesBasicas:
    """
    Clase para agrupar pruebas de operaciones básicas
    Demuestra organización de pruebas en clases
    """
    
    def test_suma_numeros_positivos(self, calculadora_limpia):
        """Prueba suma de números positivos"""
        # Arrange
        a, b = 5, 3
        
        # Act
        resultado = calculadora_limpia.sumar(a, b)
        
        # Assert
        assert resultado == 8
        assert len(calculadora_limpia.historial) == 1
        assert "5 + 3 = 8" in calculadora_limpia.historial[0]
    
    def test_suma_con_negativos(self, calculadora_limpia):
        """Prueba suma con números negativos"""
        assert calculadora_limpia.sumar(-5, 3) == -2
        assert calculadora_limpia.sumar(-5, -3) == -8
    
    def test_resta_basica(self, calculadora_limpia):
        """Prueba resta básica"""
        assert calculadora_limpia.restar(10, 4) == 6
        assert calculadora_limpia.restar(3, 7) == -4
    
    def test_multiplicacion(self, calculadora_limpia):
        """Prueba multiplicación"""
        assert calculadora_limpia.multiplicar(4, 5) == 20
        assert calculadora_limpia.multiplicar(-3, 4) == -12
        assert calculadora_limpia.multiplicar(0, 100) == 0
    
    def test_division_normal(self, calculadora_limpia):
        """Prueba división normal"""
        assert calculadora_limpia.dividir(10, 2) == 5.0
        assert calculadora_limpia.dividir(7, 3) == pytest.approx(2.333333, abs=1e-5)
    
    def test_division_por_cero(self, calculadora_limpia):
        """Prueba que división por cero lance excepción"""
        with pytest.raises(ZeroDivisionError, match="No se puede dividir entre cero"):
            calculadora_limpia.dividir(10, 0)
    
    @pytest.mark.parametrize("a,b,esperado", [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (1.5, 2.5, 4.0),
        (100, -50, 50),
    ])
    def test_suma_parametrizada(self, calculadora_limpia, a, b, esperado):
        """
        Prueba parametrizada para suma
        Demuestra cómo probar múltiples casos con una sola función
        """
        assert calculadora_limpia.sumar(a, b) == esperado

class TestOperacionesAvanzadas:
    """Pruebas para operaciones matemáticas avanzadas"""
    
    def test_potencia_basica(self, calculadora_limpia):
        """Prueba operación de potencia"""
        assert calculadora_limpia.potencia(2, 3) == 8
        assert calculadora_limpia.potencia(5, 2) == 25
        assert calculadora_limpia.potencia(10, 0) == 1
    
    @pytest.mark.parametrize("numero,esperado", [
        (4, 2.0),
        (9, 3.0),
        (16, 4.0),
        (0, 0.0),
        (1, 1.0),
        (2, pytest.approx(1.414213, abs=1e-5))
    ])
    def test_raiz_cuadrada_parametrizada(self, calculadora_limpia, numero, esperado):
        """Prueba parametrizada para raíz cuadrada"""
        assert calculadora_limpia.raiz_cuadrada(numero) == esperado
    
    def test_raiz_cuadrada_numero_negativo(self, calculadora_limpia):
        """Prueba que raíz cuadrada de número negativo lance excepción"""
        with pytest.raises(ValueError, match="número negativo"):
            calculadora_limpia.raiz_cuadrada(-4)
    
    @pytest.mark.slow  # Marcador personalizado
    def test_factorial_numeros_grandes(self, calculadora_limpia):
        """
        Prueba factorial de números grandes
        Marcado como 'slow' para ejecución opcional
        """
        assert calculadora_limpia.factorial(10) == 3628800
        assert calculadora_limpia.factorial(0) == 1
        assert calculadora_limpia.factorial(1) == 1
    
    def test_factorial_numero_negativo(self, calculadora_limpia):
        """Prueba que factorial de número negativo lance excepción"""
        with pytest.raises(ValueError, match="números negativos"):
            calculadora_limpia.factorial(-1)
    
    def test_factorial_no_entero(self, calculadora_limpia):
        """Prueba que factorial de no-entero lance excepción"""
        with pytest.raises(TypeError, match="números enteros"):
            calculadora_limpia.factorial(3.5)

class TestPromedio:
    """Pruebas para cálculo de promedio"""
    
    def test_promedio_lista_normal(self, calculadora_limpia):
        """Prueba promedio de lista normal"""
        numeros = [2, 4, 6, 8]
        assert calculadora_limpia.promedio(numeros) == 5.0
    
    def test_promedio_un_elemento(self, calculadora_limpia):
        """Prueba promedio de lista con un elemento"""
        assert calculadora_limpia.promedio([42]) == 42.0
    
    def test_promedio_con_decimales(self, calculadora_limpia):
        """Prueba promedio con números decimales"""
        numeros = [1.5, 2.5, 3.0]
        esperado = 2.333333
        assert calculadora_limpia.promedio(numeros) == pytest.approx(esperado, abs=1e-5)
    
    def test_promedio_lista_vacia(self, calculadora_limpia):
        """Prueba que promedio de lista vacía lance excepción"""
        with pytest.raises(ValueError, match="lista vacía"):
            calculadora_limpia.promedio([])
    
    @pytest.mark.parametrize("lista_numeros,esperado", [
        ([1, 2, 3, 4, 5], 3.0),
        ([10, 20, 30], 20.0),
        ([-1, 0, 1], 0.0),
        ([100], 100.0),
    ])
    def test_promedio_casos_multiples(self, calculadora_limpia, lista_numeros, esperado):
        """Prueba parametrizada para diferentes casos de promedio"""
        assert calculadora_limpia.promedio(lista_numeros) == esperado

class TestHistorial:
    """Pruebas para funcionalidad de historial"""
    
    def test_historial_inicialmente_vacio(self, calculadora_limpia):
        """Prueba que el historial inicie vacío"""
        assert len(calculadora_limpia.historial) == 0
        assert calculadora_limpia.obtener_historial() == []
    
    def test_historial_registra_operaciones(self, calculadora_limpia):
        """Prueba que las operaciones se registren en el historial"""
        calculadora_limpia.sumar(2, 3)
        calculadora_limpia.multiplicar(4, 5)
        
        historial = calculadora_limpia.obtener_historial()
        assert len(historial) == 2
        assert "2 + 3 = 5" in historial[0]
        assert "4 × 5 = 20" in historial[1]
    
    def test_limpiar_historial(self, calculadora_con_historial):
        """
        Prueba funcionalidad de limpieza de historial
        Usa fixture con historial pre-existente
        """
        # Verificar que hay historial previo
        assert len(calculadora_con_historial.obtener_historial()) > 0
        
        # Limpiar historial
        calculadora_con_historial.limpiar_historial()
        
        # Verificar que esté vacío
        assert len(calculadora_con_historial.obtener_historial()) == 0
    
    def test_obtener_historial_es_copia(self, calculadora_con_historial):
        """
        Prueba que obtener_historial retorna una copia, no la referencia original
        Esto previene modificaciones accidentales del historial
        """
        historial_original = calculadora_con_historial.obtener_historial()
        
        # Modificar la copia retornada
        historial_original.append("Operación falsa")
        
        # Verificar que el historial interno no cambió
        historial_actual = calculadora_con_historial.obtener_historial()
        assert "Operación falsa" not in historial_actual

class TestValidacionEntrada:
    """Pruebas para validación de tipos de entrada"""
    
    @pytest.mark.parametrize("entrada_invalida", [
        "5",        # String
        [],         # Lista
        {},         # Diccionario
        None,       # None
        True,       # Boolean
    ])
    def test_suma_rechaza_tipos_invalidos(self, calculadora_limpia, entrada_invalida):
        """Prueba que suma rechace tipos de datos inválidos"""
        with pytest.raises(TypeError):
            calculadora_limpia.sumar(entrada_invalida, 5)
        
        with pytest.raises(TypeError):
            calculadora_limpia.sumar(5, entrada_invalida)
    
    def test_todas_operaciones_validan_entrada(self, calculadora_limpia):
        """Prueba que todas las operaciones validen tipos de entrada"""
        entrada_invalida = "no_es_numero"
        
        with pytest.raises(TypeError):
            calculadora_limpia.restar(entrada_invalida, 5)
        
        with pytest.raises(TypeError):
            calculadora_limpia.multiplicar(entrada_invalida, 5)
        
        with pytest.raises(TypeError):
            calculadora_limpia.dividir(entrada_invalida, 5)
        
        with pytest.raises(TypeError):
            calculadora_limpia.potencia(entrada_invalida, 2)
        
        with pytest.raises(TypeError):
            calculadora_limpia.raiz_cuadrada(entrada_invalida)
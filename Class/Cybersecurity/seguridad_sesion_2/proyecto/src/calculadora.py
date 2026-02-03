# ============================================================================
# ARCHIVO 1: src/calculadora.py (Código a probar)
# ============================================================================

"""
Clase Calculadora para demostrar pruebas con Pytest
Incluye operaciones básicas y avanzadas, manejo de errores
"""

import math
from typing import List, Union

class Calculadora:
    """
    Calculadora con operaciones matemáticas básicas y avanzadas
    Incluye historial de operaciones y validación de entrada
    """
    
    def __init__(self):
        """Inicializa la calculadora con historial vacío"""
        self.historial: List[str] = []
        self._precision = 10  # Precisión para operaciones decimales
    
    def sumar(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Suma dos números y registra la operación
        
        Args:
            a: Primer número
            b: Segundo número
            
        Returns:
            Resultado de la suma
            
        Raises:
            TypeError: Si los argumentos no son números
        """
        self._validar_numeros(a, b)
        resultado = a + b
        self.historial.append(f"{a} + {b} = {resultado}")
        return resultado
    
    def restar(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Resta dos números"""
        self._validar_numeros(a, b)
        resultado = a - b
        self.historial.append(f"{a} - {b} = {resultado}")
        return resultado
    
    def multiplicar(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiplica dos números"""
        self._validar_numeros(a, b)
        resultado = a * b
        self.historial.append(f"{a} × {b} = {resultado}")
        return resultado
    
    def dividir(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide dos números
        
        Raises:
            ZeroDivisionError: Si el divisor es cero
        """
        self._validar_numeros(a, b)
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        
        resultado = a / b
        self.historial.append(f"{a} ÷ {b} = {resultado}")
        return resultado
    
    def potencia(self, base: Union[int, float], exponente: Union[int, float]) -> Union[int, float]:
        """Calcula base elevado a exponente"""
        self._validar_numeros(base, exponente)
        resultado = base ** exponente
        self.historial.append(f"{base}^{exponente} = {resultado}")
        return resultado
    
    def raiz_cuadrada(self, numero: Union[int, float]) -> float:
        """
        Calcula la raíz cuadrada de un número
        
        Raises:
            ValueError: Si el número es negativo
        """
        self._validar_numero(numero)
        if numero < 0:
            raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
        
        resultado = math.sqrt(numero)
        self.historial.append(f"√{numero} = {resultado}")
        return resultado
    
    def factorial(self, n: int) -> int:
        """
        Calcula el factorial de un número entero
        
        Raises:
            ValueError: Si n es negativo o no es entero
        """
        if not isinstance(n, int):
            raise TypeError("El factorial solo se calcula para números enteros")
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos")
        
        if n <= 1:
            resultado = 1
        else:
            resultado = math.factorial(n)
        
        self.historial.append(f"{n}! = {resultado}")
        return resultado
    
    def promedio(self, numeros: List[Union[int, float]]) -> float:
        """
        Calcula el promedio de una lista de números
        
        Raises:
            ValueError: Si la lista está vacía
        """
        if not numeros:
            raise ValueError("No se puede calcular el promedio de una lista vacía")
        
        for num in numeros:
            self._validar_numero(num)
        
        resultado = sum(numeros) / len(numeros)
        self.historial.append(f"Promedio de {numeros} = {resultado}")
        return resultado
    
    def limpiar_historial(self) -> None:
        """Limpia el historial de operaciones"""
        self.historial.clear()
    
    def obtener_historial(self) -> List[str]:
        """Retorna una copia del historial"""
        return self.historial.copy()
    
    def _validar_numero(self, numero: Union[int, float]) -> None:
        """Valida que el input sea un número"""
        if isinstance(numero, bool) or not isinstance(numero, (int, float)):
            raise TypeError(f"Se esperaba un número, se recibió {type(numero).__name__}")
    
    def _validar_numeros(self, *numeros) -> None:
        """Valida que todos los inputs sean números"""
        for numero in numeros:
            self._validar_numero(numero)
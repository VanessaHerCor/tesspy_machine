"""
Sesión 5: Depuración y análisis de código
Ejemplo práctico de debugging, logging estructurado y profiling
"""

import logging
import time
import cProfile
import pstats
import tracemalloc
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Any
# from memory_profiler import profile
# Funcionalidad de profiling simulada para evitar dependencias externas
def profile(func):
    """Decorator simulado para memory profiling"""
    def wrapper(*args, **kwargs):
        import tracemalloc
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Memory usage - Current: {current / 1024 / 1024:.2f} MB, Peak: {peak / 1024 / 1024:.2f} MB")
        return result
    return wrapper
import json


# Configuración de logging estructurado
class StructuredLogger:
    """Logger estructurado con contexto automático"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Formato estructurado
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        self._context = {}
    
    @contextmanager
    def log_context(self, **kwargs):
        """Context manager para agregar contexto a logs"""
        old_context = self._context.copy()
        self._context.update(kwargs)
        try:
            yield
        finally:
            self._context = old_context
    
    def _format_message(self, message: str, extra: Dict = None) -> str:
        """Formatea mensaje con contexto estructurado"""
        log_data = {
            'message': message,
            'context': self._context,
            'timestamp': datetime.utcnow().isoformat()
        }
        if extra:
            log_data.update(extra)
        return json.dumps(log_data, indent=2)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(self._format_message(message, kwargs))
    
    def info(self, message: str, **kwargs):
        self.logger.info(self._format_message(message, kwargs))
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(self._format_message(message, kwargs))
    
    def error(self, message: str, **kwargs):
        self.logger.error(self._format_message(message, kwargs))


# Inicializar logger
logger = StructuredLogger("debug_example")


class BuggyCalculator:
    """Calculadora con bugs intencionales para debugging"""
    
    def __init__(self):
        self.history = []
        self.cache = {}
    
    def divide(self, a: float, b: float) -> float:
        """División con bug intencional"""
        logger.debug("Starting division operation", 
                    operation="divide", a=a, b=b)
        
        # BUG: No maneja división por cero correctamente
        try:
            result = a / b
            self.history.append(f"{a} / {b} = {result}")
            logger.info("Division completed successfully", result=result)
            return result
        except ZeroDivisionError:
            # BUG: Este mensaje no es estructurado
            print(f"Error: Cannot divide {a} by zero!")
            logger.error("Division by zero attempted", a=a, b=b)
            return None
    
    def factorial(self, n: int) -> int:
        """Factorial con implementación ineficiente"""
        logger.debug("Calculating factorial", n=n)
        
        if n in self.cache:
            logger.debug("Using cached result", n=n)
            return self.cache[n]
        
        # BUG: Implementación O(n!) muy ineficiente
        if n == 0 or n == 1:
            result = 1
        else:
            result = n * self.factorial(n - 1)
        
        self.cache[n] = result
        logger.info("Factorial calculated", n=n, result=result)
        return result
    
    @profile  # Memory profiling decorator
    def memory_intensive_operation(self, size: int) -> List[int]:
        """Operación que consume mucha memoria"""
        logger.debug("Starting memory intensive operation", size=size)
        
        # Crear listas grandes para consumir memoria
        data = [i for i in range(size)]
        processed = [x * 2 for x in data]
        squares = [x ** 2 for x in processed]
        
        # BUG: No liberamos memoria intermedia
        logger.info("Memory operation completed", 
                   final_size=len(squares))
        return squares


def demonstrate_debugging():
    """Demuestra técnicas de debugging"""
    print("=== DEBUGGING DEMONSTRATION ===")
    
    calc = BuggyCalculator()
    
    with logger.log_context(user_id=123, session_id="abc-def"):
        logger.info("Starting debugging demonstration")
        
        # Operación normal
        result1 = calc.divide(10, 2)
        print(f"10 / 2 = {result1}")
        
        # Operación con error
        result2 = calc.divide(10, 0)
        print(f"10 / 0 = {result2}")
        
        # Operación lenta
        # import pdb; pdb.set_trace()  # Breakpoint para debugging interactivo (comentado para demo)
        result3 = calc.factorial(10)
        print(f"10! = {result3}")


def demonstrate_profiling():
    """Demuestra técnicas de profiling"""
    print("\n=== PROFILING DEMONSTRATION ===")
    
    calc = BuggyCalculator()
    
    # Time profiling con cProfile
    pr = cProfile.Profile()
    pr.enable()
    
    # Operaciones a perfilar
    for i in range(5):
        calc.factorial(i + 5)
    
    pr.disable()
    
    # Análisis de resultados
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    print("\nTop 10 funciones por tiempo:")
    stats.print_stats(10)
    
    # Memory profiling
    print("\nMemory profiling en acción...")
    calc.memory_intensive_operation(1000)


def demonstrate_static_analysis():
    """Demuestra conceptos de análisis estático"""
    print("\n=== STATIC ANALYSIS CONCEPTS ===")
    
    # Ejemplo de código que herramientas estáticas detectarían
    
    # pylint detectaría: unused variable
    unused_variable = "This will be flagged"
    
    # mypy detectaría: type inconsistency
    def bad_typing(x: int) -> str:
        return x + 1  # Retorna int, no str
    
    # bandit detectaría: potential security issue
    import subprocess
    # subprocess.call(user_input, shell=True)  # Comentado por seguridad
    
    # flake8 detectaría: style issues
    def   poorly_formatted_function(  ):
        pass
    
    print("Este código tendría múltiples warnings en análisis estático")
    print("- Unused variables")
    print("- Type inconsistencies") 
    print("- Security vulnerabilities")
    print("- Style violations")


def demonstrate_memory_debugging():
    """Demuestra debugging de memoria"""
    print("\n=== MEMORY DEBUGGING ===")
    
    # Iniciar tracking de memoria
    tracemalloc.start()
    
    calc = BuggyCalculator()
    
    # Operaciones que consumen memoria
    data = []
    for i in range(1000):
        data.append(calc.memory_intensive_operation(100))
    
    # Tomar snapshot de memoria
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("Top 5 líneas que más memoria consumen:")
    for stat in top_stats[:5]:
        print(f"{stat.traceback.format()[0]} - {stat.size / 1024:.1f} KB")


def run_comprehensive_example():
    """Ejecuta ejemplo completo con todas las técnicas"""
    print("🔍 SESIÓN 5: DEPURACIÓN Y ANÁLISIS DE CÓDIGO")
    print("=" * 50)
    
    try:
        # 1. Debugging básico
        demonstrate_debugging()
        
        # 2. Profiling
        demonstrate_profiling()
        
        # 3. Análisis estático (conceptual)
        demonstrate_static_analysis()
        
        # 4. Memory debugging
        demonstrate_memory_debugging()
        
        print("\n✅ Demostración completada exitosamente")
        
    except Exception as e:
        logger.error("Error during demonstration", 
                    error=str(e), 
                    error_type=type(e).__name__)
        raise


if __name__ == "__main__":
    # Ejecutar ejemplo completo
    run_comprehensive_example()
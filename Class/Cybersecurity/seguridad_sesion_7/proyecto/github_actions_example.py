"""
Sesión 7: Automatización de pruebas con GitHub Actions
Script de ejemplo con código Python y configuración para CI/CD
"""

import json
import time
import pytest
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Representa el resultado de un test"""
    name: str
    passed: bool
    duration: float
    message: str = ""


class Calculator:
    """Calculadora simple para demostrar testing automatizado"""
    
    def add(self, a: float, b: float) -> float:
        """Suma dos números"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Resta dos números"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplica dos números"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide dos números"""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Eleva un número a una potencia"""
        return base ** exponent


class DataProcessor:
    """Procesador de datos para demostrar testing de integración"""
    
    def __init__(self):
        self.data: List[Dict[str, Any]] = []
    
    def add_record(self, record: Dict[str, Any]) -> None:
        """Añade un registro al procesador"""
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")
        
        # Validar campos requeridos
        required_fields = ['id', 'timestamp', 'value']
        for field in required_fields:
            if field not in record:
                raise ValueError(f"Missing required field: {field}")
        
        record['processed_at'] = datetime.utcnow().isoformat()
        self.data.append(record)
        logger.info(f"Record added: {record['id']}")
    
    def get_records(self) -> List[Dict[str, Any]]:
        """Obtiene todos los registros"""
        return self.data.copy()
    
    def filter_by_value(self, min_value: float) -> List[Dict[str, Any]]:
        """Filtra registros por valor mínimo"""
        return [record for record in self.data if record['value'] >= min_value]
    
    def calculate_stats(self) -> Dict[str, float]:
        """Calcula estadísticas de los datos"""
        if not self.data:
            return {'count': 0, 'sum': 0, 'avg': 0, 'min': 0, 'max': 0}
        
        values = [record['value'] for record in self.data]
        return {
            'count': len(values),
            'sum': sum(values),
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }


class ApiSimulator:
    """Simulador de API para testing de servicios externos"""
    
    def __init__(self, latency: float = 0.1):
        self.latency = latency
        self.failure_rate = 0.0
        self.call_count = 0
    
    def set_failure_rate(self, rate: float) -> None:
        """Establece la tasa de fallos simulados"""
        if not 0 <= rate <= 1:
            raise ValueError("Failure rate must be between 0 and 1")
        self.failure_rate = rate
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Simula obtener datos de usuario"""
        self.call_count += 1
        time.sleep(self.latency)
        
        # Simular fallos
        import random
        if random.random() < self.failure_rate:
            raise ConnectionError("API connection failed")
        
        return {
            'id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com',
            'active': True,
            'created_at': datetime.utcnow().isoformat()
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simula crear un usuario"""
        self.call_count += 1
        time.sleep(self.latency)
        
        # Validar datos requeridos
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Simular respuesta de creación
        user_id = hash(user_data['email']) % 10000
        return {
            'id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'active': True,
            'created_at': datetime.utcnow().isoformat()
        }


class TestRunner:
    """Runner personalizado para demostrar reporting de tests"""
    
    def __init__(self):
        self.results: List[TestResult] = []
    
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> TestResult:
        """Ejecuta un test individual"""
        start_time = time.time()
        try:
            test_func(*args, **kwargs)
            duration = time.time() - start_time
            result = TestResult(test_name, True, duration)
            logger.info(f"✅ {test_name} passed in {duration:.3f}s")
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(test_name, False, duration, str(e))
            logger.error(f"❌ {test_name} failed in {duration:.3f}s: {e}")
        
        self.results.append(result)
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de resultados"""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        total_duration = sum(r.duration for r in self.results)
        
        return {
            'total': len(self.results),
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / len(self.results)) * 100 if self.results else 0,
            'total_duration': total_duration
        }
    
    def export_results(self, filename: str = 'test_results.json') -> None:
        """Exporta resultados a JSON para CI/CD"""
        results_data = {
            'summary': self.get_summary(),
            'results': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'duration': r.duration,
                    'message': r.message
                }
                for r in self.results
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        logger.info(f"Results exported to {filename}")


def test_calculator_operations():
    """Tests para la calculadora"""
    calc = Calculator()
    
    # Test suma
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)
    
    # Test división
    assert calc.divide(10, 2) == 5
    with pytest.raises(ValueError):
        calc.divide(10, 0)
    
    # Test potencia
    assert calc.power(2, 3) == 8
    assert calc.power(5, 0) == 1


def test_data_processor():
    """Tests para el procesador de datos"""
    processor = DataProcessor()
    
    # Test añadir registro válido
    record = {
        'id': 1,
        'timestamp': '2023-01-01T00:00:00Z',
        'value': 100.0
    }
    processor.add_record(record)
    
    # Verificar que se añadió
    records = processor.get_records()
    assert len(records) == 1
    assert records[0]['id'] == 1
    assert 'processed_at' in records[0]
    
    # Test filtrado
    processor.add_record({'id': 2, 'timestamp': '2023-01-01T01:00:00Z', 'value': 50.0})
    filtered = processor.filter_by_value(75.0)
    assert len(filtered) == 1
    
    # Test estadísticas
    stats = processor.calculate_stats()
    assert stats['count'] == 2
    assert stats['avg'] == 75.0


def test_api_simulator():
    """Tests para el simulador de API"""
    api = ApiSimulator(latency=0.01)  # Latencia baja para tests
    
    # Test obtener usuario
    user = api.get_user(123)
    assert user['id'] == 123
    assert 'name' in user
    assert 'email' in user
    
    # Test crear usuario
    user_data = {'name': 'Test User', 'email': 'test@example.com'}
    created_user = api.create_user(user_data)
    assert created_user['name'] == 'Test User'
    assert created_user['email'] == 'test@example.com'
    
    # Test validación
    with pytest.raises(ValueError):
        api.create_user({'name': 'Incomplete'})  # Falta email


def run_comprehensive_demo():
    """Ejecuta demostración completa para CI/CD"""
    print("🚀 SESIÓN 7: AUTOMATIZACIÓN CON GITHUB ACTIONS")
    print("=" * 55)
    
    # Inicializar runner personalizado
    runner = TestRunner()
    
    # Ejecutar tests con el runner personalizado
    runner.run_test("Calculator Basic", test_calculator_operations)
    runner.run_test("Data Processor", test_data_processor)
    runner.run_test("API Simulator", test_api_simulator)
    
    # Test de integración simulado
    def integration_test():
        processor = DataProcessor()
        api = ApiSimulator(latency=0.01)
        
        # Simular workflow de procesamiento
        user = api.get_user(1)
        record = {
            'id': user['id'],
            'timestamp': user['created_at'],
            'value': 150.0
        }
        processor.add_record(record)
        
        stats = processor.calculate_stats()
        assert stats['count'] == 1
        assert stats['avg'] == 150.0
    
    runner.run_test("Integration Test", integration_test)
    
    # Test de rendimiento simulado
    def performance_test():
        api = ApiSimulator(latency=0.001)
        start_time = time.time()
        
        for i in range(10):
            api.get_user(i)
        
        duration = time.time() - start_time
        assert duration < 1.0, f"Performance test failed: {duration:.3f}s > 1.0s"
    
    runner.run_test("Performance Test", performance_test)
    
    # Mostrar resumen
    summary = runner.get_summary()
    print(f"\n📊 RESULTADOS DE TESTING:")
    print(f"   Total tests: {summary['total']}")
    print(f"   Passed: {summary['passed']}")
    print(f"   Failed: {summary['failed']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    print(f"   Total duration: {summary['total_duration']:.3f}s")
    
    # Exportar resultados para CI/CD
    runner.export_results()
    
    # Simular diferentes exit codes para CI/CD
    if summary['failed'] > 0:
        print("\n❌ Tests failed - Exit code 1")
        return 1
    else:
        print("\n✅ All tests passed - Exit code 0")
        return 0


if __name__ == "__main__":
    # Ejecutar demostración
    exit_code = run_comprehensive_demo()
    
    print(f"\n🎯 Este script demuestra:")
    print("   • Testing automatizado con pytest")
    print("   • Generación de reportes JSON")
    print("   • Simulación de APIs y servicios")
    print("   • Exit codes para GitHub Actions")
    print("   • Integración con workflows de CI/CD")
    
    exit(exit_code)
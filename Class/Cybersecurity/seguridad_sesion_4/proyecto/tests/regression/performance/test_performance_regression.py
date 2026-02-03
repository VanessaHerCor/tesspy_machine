"""
Performance regression tests: Detectan degradación de rendimiento
Usan pytest-benchmark para medir y comparar tiempos de ejecución
"""

import pytest
from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator
import random

@pytest.mark.regression
@pytest.mark.performance
class TestPerformanceRegression:
    """Tests de regresión de rendimiento"""
    
    @pytest.fixture
    def large_user_dataset(self):
        """Dataset grande para testing de performance"""
        users = []
        for i in range(1000):
            user = {
                'id': i,
                'username': f'user{i}',
                'email': f'user{i}@example{i%10}.com',
                'is_active': random.choice([True, False])
            }
            users.append(user)
        return users
    
    @pytest.fixture
    def processor(self):
        return DataProcessor()
    
    @pytest.fixture
    def generator(self):
        return ReportGenerator()
    
    def test_user_processing_performance(self, benchmark, processor, large_user_dataset):
        """
        Benchmark: Procesamiento de usuarios debe mantenerse rápido
        Establece baseline de rendimiento para detectar regresiones
        """
        # Ejecutar benchmark
        result = benchmark(processor.process_user_list, large_user_dataset)
        
        # Verificar que el resultado es correcto
        assert len(result) == 1000
        assert all('processed_at' in user for user in result)
    
    def test_search_performance(self, benchmark, processor, large_user_dataset):
        """
        Benchmark: Búsqueda debe ser O(n) y mantenerse eficiente
        """
        # Benchmark de búsqueda con query común
        result = benchmark(processor.search_users, large_user_dataset, 'user1')
        
        # Verificar resultados
        assert len(result) >= 1  # Al menos user1, user10, user100, etc.
        assert all('user1' in user['username'] for user in result)
    
    def test_statistics_calculation_performance(self, benchmark, processor):
        """
        Benchmark: Cálculo de estadísticas debe ser rápido
        """
        # Dataset numérico grande
        large_numbers = [random.uniform(0, 1000) for _ in range(10000)]
        
        result = benchmark(processor.calculate_statistics, large_numbers)
        
        # Verificar cálculos
        assert result['count'] == 10000
        assert 0 <= result['mean'] <= 1000
    
    def test_report_generation_performance(self, benchmark, generator, large_user_dataset):
        """
        Benchmark: Generación de reportes debe escalar bien
        """
        result = benchmark(generator.generate_user_summary, large_user_dataset)
        
        # Verificar reporte
        assert result['total_users'] == 1000
        assert 'top_email_domains' in result
    
    @pytest.mark.slow
    def test_algorithm_comparison_benchmark(self, benchmark, processor):
        """
        Benchmark: Comparar algoritmo lento vs optimizado
        Demuestra la importancia de optimización
        """
        # Dataset pequeño para que slow_algorithm sea tolerable
        small_dataset = list(range(50))
        
        # Benchmark del algoritmo lento
        slow_result = benchmark.pedantic(
            processor.slow_algorithm, 
            args=[small_dataset], 
            iterations=1, 
            rounds=3
        )
        
        # También medir el optimizado para comparación
        fast_result = processor.optimized_algorithm(small_dataset)
        
        # Verificar que ambos dan el mismo resultado
        assert slow_result == fast_result
        
        # El benchmark detectará si slow_algorithm se hace más lento
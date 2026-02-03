"""
Golden/Snapshot tests: Verifican que outputs específicos no cambien
Si estos tests fallan, es señal de cambio no intencional en el comportamiento
"""

import pytest
import json
from src.report_generator import ReportGenerator

@pytest.mark.regression
@pytest.mark.golden
class TestReportGoldenOutputs:
    """Golden tests para outputs de reportes"""
    
    @pytest.fixture
    def generator(self):
        """Generator con timestamp fijo para reproducibilidad"""
        return ReportGenerator(fixed_timestamp="2024-01-01T00:00:00Z")
    
    def test_user_summary_golden_output(self, generator, file_regression):
        """
        Golden test: Output de resumen de usuarios debe ser estable
        Usa pytest-regressions para comparación automática
        """
        # Datos de entrada fijos
        users_data = [
            {'id': 1, 'username': 'alice', 'email': 'alice@gmail.com', 'is_active': True},
            {'id': 2, 'username': 'bob', 'email': 'bob@company.com', 'is_active': True},
            {'id': 3, 'username': 'charlie', 'email': 'charlie@gmail.com', 'is_active': False},
            {'id': 4, 'username': 'diana', 'email': 'diana@university.edu', 'is_active': True},
        ]
        
        # Generar reporte
        report = generator.generate_user_summary(users_data)
        
        # Comparar con golden file (se crea automáticamente la primera vez)
        file_regression.check(json.dumps(report, indent=2, sort_keys=True))
    
    def test_performance_report_golden_output(self, generator, file_regression):
        """Golden test: Reporte de rendimiento con métricas fijas"""
        # Métricas de entrada fijas para reproducibilidad
        metrics = [0.123, 0.156, 0.089, 0.234, 0.167, 0.145, 0.198, 0.134, 0.176, 0.112]
        
        report = generator.generate_performance_report(metrics)
        
        file_regression.check(json.dumps(report, indent=2, sort_keys=True))
    
    def test_trend_analysis_golden_output(self, generator, file_regression):
        """Golden test: Análisis de tendencias con datos fijos"""
        # Datos de tendencia fijos
        daily_data = {
            '2024-01-01': 100,
            '2024-01-02': 120,
            '2024-01-03': 115,
            '2024-01-04': 130,
            '2024-01-05': 140,
            '2024-01-06': 135,
            '2024-01-07': 150
        }
        
        report = generator.generate_trend_analysis(daily_data)
        
        file_regression.check(json.dumps(report, indent=2, sort_keys=True))
    
    def test_empty_data_golden_outputs(self, generator, file_regression):
        """Golden test: Comportamiento con datos vacíos debe ser estable"""
        reports = {
            'empty_users': generator.generate_user_summary([]),
            'empty_metrics': generator.generate_performance_report([]),
            'empty_trends': generator.generate_trend_analysis({})
        }
        
        file_regression.check(json.dumps(reports, indent=2, sort_keys=True))
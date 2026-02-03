"""
Smoke tests: Verifican funcionalidad crítica básica
Deben ejecutarse rápido (<5 min) y fallar rápido si algo está muy roto
"""

import pytest
import requests
import time
from src.report_generator import ReportGenerator
from src.data_processor import DataProcessor

@pytest.mark.smoke
class TestCoreAPI:
    """Smoke tests para API crítica"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """URL base de la API para testing"""
        return "http://localhost:5001"
    
    def test_health_endpoint_responds(self, api_base_url):
        """
        TEST CRÍTICO: Health check debe responder siempre
        Si falla, algo está muy mal
        """
        try:
            response = requests.get(f"{api_base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - start with 'python src/app.py'")
    
    def test_users_endpoint_basic(self, api_base_url):
        """TEST CRÍTICO: Endpoint principal de usuarios"""
        try:
            response = requests.get(f"{api_base_url}/api/users", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert 'users' in data
            assert 'total' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running")
    
    def test_user_creation_basic(self, api_base_url):
        """TEST CRÍTICO: Crear usuario básico"""
        try:
            user_data = {
                'username': f'smoketest_{int(time.time())}',
                'email': 'smoke@test.com'
            }
            response = requests.post(f"{api_base_url}/api/users", json=user_data, timeout=10)
            assert response.status_code == 201
            data = response.json()
            assert data['username'] == user_data['username']
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running")

@pytest.mark.smoke
class TestCoreComponents:
    """Smoke tests para componentes básicos del sistema"""
    
    def test_report_generator_basic(self):
        """TEST CRÍTICO: Generador de reportes básico"""
        generator = ReportGenerator()
        
        # Test con datos mínimos
        users = [{'id': 1, 'username': 'test', 'email': 'test@example.com'}]
        report = generator.generate_user_summary(users)
        
        assert report['total_users'] == 1
        assert 'timestamp' in report
    
    def test_data_processor_basic(self):
        """TEST CRÍTICO: Procesador de datos básico"""
        processor = DataProcessor()
        
        # Test con datos mínimos
        users = [{'id': 1, 'username': 'test', 'email': 'test@example.com'}]
        processed = processor.process_user_list(users)
        
        assert len(processed) == 1
        assert processed[0]['username'] == 'TEST'  # Debe convertir a mayúsculas
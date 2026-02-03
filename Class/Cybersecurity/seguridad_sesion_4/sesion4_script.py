"""
SESIÓN 4: PRUEBAS DE REGRESIÓN Y PRUEBAS DE CARGA
Script de ejemplo: Sistema completo con regresión automática y load testing

DEPENDENCIAS NECESARIAS:
pip install pytest pytest-benchmark locust requests flask faker pytest-regressions

ESTRUCTURA DE ARCHIVOS:
proyecto/
├── src/
│   ├── __init__.py
│   ├── app.py              # API Flask para load testing
│   ├── report_generator.py # Generador de reportes (golden tests)
│   └── data_processor.py   # Procesador de datos
├── tests/
│   ├── smoke/             # Smoke tests críticos
│   ├── regression/        # Suite de regresión completa
│   │   ├── historical/    # Tests de bugs pasados
│   │   ├── golden/        # Golden/snapshot tests
│   │   └── performance/   # Regression de rendimiento
│   └── load/              # Scripts de Locust
├── data/
│   ├── golden_outputs/    # Archivos de referencia
│   ├── test_datasets/     # Datos de prueba
│   └── benchmarks/        # Resultados de benchmark
├── locustfile.py          # Script principal de Locust
├── pytest.ini
└── requirements.txt

INSTRUCCIONES DE EJECUCIÓN:

1. SMOKE TESTS (críticos, rápidos):
   pytest tests/smoke/ -v --maxfail=1

2. REGRESSION SUITE (completa):
   pytest tests/regression/ -v

3. PERFORMANCE REGRESSION:
   pytest tests/regression/performance/ --benchmark-only

4. LOAD TESTING:
   # Terminal 1: Iniciar servidor
   python src/app.py
   
   # Terminal 2: Ejecutar load test
   locust -f locustfile.py --host=http://localhost:5000

5. GOLDEN TESTS (actualizar referencias):
   pytest tests/regression/golden/ --force-regen

CONCEPTOS DEMOSTRADOS:
- Smoke testing automatizado
- Golden tests / Snapshot testing
- Regression suite organizada
- Performance regression testing
- Load testing con Locust
- Realistic user scenarios
- Métricas y análisis de rendimiento
"""

# ============================================================================
# ARCHIVO 1: src/app.py (API Flask para load testing)
# ============================================================================

"""
API Flask simple para demostrar load testing
Incluye endpoints con diferentes características de rendimiento
"""

from flask import Flask, jsonify, request, abort
import time
import random
import threading
from datetime import datetime
from typing import Dict, List
import json

app = Flask(__name__)

# Simulación de base de datos en memoria
users_db = {}
posts_db = {}
sessions = {}
request_count = 0
request_lock = threading.Lock()

def get_request_stats():
    """Obtiene estadísticas de requests para monitoring"""
    with request_lock:
        return request_count

@app.before_request
def track_requests():
    """Middleware para contar requests"""
    global request_count
    with request_lock:
        request_count += 1

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check - crítico para smoke tests
    Debe responder siempre en <100ms
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Endpoint rápido para listar usuarios
    Simula consulta simple a BD
    """
    # Simular latencia de BD (50-100ms)
    time.sleep(random.uniform(0.05, 0.1))
    
    return jsonify({
        'users': list(users_db.values()),
        'total': len(users_db),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Endpoint para crear usuario
    Simula operación de escritura más lenta
    """
    data = request.get_json()
    if not data or 'username' not in data:
        abort(400, 'Username is required')
    
    username = data['username']
    if username in users_db:
        abort(409, 'User already exists')
    
    # Simular validación y escritura a BD (100-200ms)
    time.sleep(random.uniform(0.1, 0.2))
    
    user_id = len(users_db) + 1
    user = {
        'id': user_id,
        'username': username,
        'email': data.get('email', f'{username}@example.com'),
        'created_at': datetime.utcnow().isoformat()
    }
    users_db[user_id] = user
    
    return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Endpoint para obtener usuario específico
    Incluye posibilidad de error 404
    """
    # Simular latencia de consulta
    time.sleep(random.uniform(0.03, 0.08))
    
    if user_id not in users_db:
        abort(404, 'User not found')
    
    return jsonify(users_db[user_id]), 200

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Endpoint con paginación - útil para load testing
    Simula consulta más compleja
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Simular consulta compleja (100-300ms)
    time.sleep(random.uniform(0.1, 0.3))
    
    # Simular paginación
    total_posts = len(posts_db)
    start = (page - 1) * per_page
    end = start + per_page
    posts_slice = list(posts_db.values())[start:end]
    
    return jsonify({
        'posts': posts_slice,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total_posts,
            'pages': (total_posts + per_page - 1) // per_page
        }
    }), 200

@app.route('/api/search', methods=['GET'])
def search():
    """
    Endpoint de búsqueda - operación costosa
    Ideal para stress testing
    """
    query = request.args.get('q', '')
    if not query:
        abort(400, 'Query parameter q is required')
    
    # Simular búsqueda compleja (200-500ms)
    time.sleep(random.uniform(0.2, 0.5))
    
    # Simular resultados basados en query
    results = []
    for user in users_db.values():
        if query.lower() in user['username'].lower():
            results.append(user)
    
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results),
        'execution_time_ms': random.randint(200, 500)
    }), 200

@app.route('/api/heavy-operation', methods=['POST'])
def heavy_operation():
    """
    Endpoint que simula operación pesada
    Para testing de límites y timeouts
    """
    # Simular operación muy lenta (1-3 segundos)
    time.sleep(random.uniform(1.0, 3.0))
    
    # 10% de probabilidad de error para simular condiciones reales
    if random.random() < 0.1:
        abort(500, 'Internal server error during heavy operation')
    
    return jsonify({
        'status': 'completed',
        'processing_time': random.uniform(1.0, 3.0),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Endpoint para obtener estadísticas del servidor
    Útil para monitoreo durante load testing
    """
    return jsonify({
        'total_requests': get_request_stats(),
        'total_users': len(users_db),
        'total_posts': len(posts_db),
        'active_sessions': len(sessions),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/slow', methods=['GET'])
def slow_endpoint():
    """
    Endpoint intencionalmente lento
    Para demonstrar degradación de rendimiento
    """
    # Simular degradación progresiva bajo carga
    current_load = get_request_stats()
    sleep_time = min(0.1 + (current_load * 0.001), 2.0)  # Máximo 2 segundos
    time.sleep(sleep_time)
    
    return jsonify({
        'message': 'This endpoint gets slower under load',
        'current_load': current_load,
        'sleep_time': sleep_time
    }), 200

# Inicializar algunos datos de prueba
def init_test_data():
    """Inicializa datos de prueba para la aplicación"""
    global users_db, posts_db
    
    # Crear usuarios de prueba
    for i in range(1, 11):
        user = {
            'id': i,
            'username': f'user{i}',
            'email': f'user{i}@example.com',
            'created_at': datetime.utcnow().isoformat()
        }
        users_db[i] = user
    
    # Crear posts de prueba
    for i in range(1, 21):
        post = {
            'id': i,
            'title': f'Post {i}',
            'content': f'Content for post {i}',
            'author_id': random.randint(1, 10),
            'created_at': datetime.utcnow().isoformat()
        }
        posts_db[i] = post

if __name__ == '__main__':
    init_test_data()
    print("🚀 Starting Flask server for load testing...")
    print("📊 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/users - List users")
    print("  POST /api/users - Create user")
    print("  GET  /api/users/<id> - Get user")
    print("  GET  /api/posts - List posts (paginated)")
    print("  GET  /api/search?q=<query> - Search")
    print("  POST /api/heavy-operation - Heavy operation")
    print("  GET  /api/stats - Server stats")
    print("  GET  /api/slow - Intentionally slow endpoint")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

# ============================================================================
# ARCHIVO 2: src/report_generator.py (Para golden tests)
# ============================================================================

"""
Generador de reportes que será usado para golden/snapshot testing
Los outputs de estas funciones deben permanecer estables
"""

import json
from datetime import datetime
from typing import Dict, List, Any
import statistics

class ReportGenerator:
    """
    Generador de reportes con salidas determinísticas
    Perfecto para golden testing
    """
    
    def __init__(self, fixed_timestamp: str = None):
        """
        Inicializa generador con timestamp fijo para tests reproducibles
        """
        self.fixed_timestamp = fixed_timestamp or "2024-01-01T00:00:00Z"
    
    def generate_user_summary(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Genera resumen de usuarios
        Output debe ser estable para golden testing
        """
        if not users:
            return {
                'total_users': 0,
                'summary': 'No users found',
                'timestamp': self.fixed_timestamp
            }
        
        # Estadísticas básicas
        total_users = len(users)
        active_users = len([u for u in users if u.get('is_active', True)])
        
        # Dominios de email más comunes
        domains = {}
        for user in users:
            email = user.get('email', '')
            if '@' in email:
                domain = email.split('@')[1]
                domains[domain] = domains.get(domain, 0) + 1
        
        # Top 3 dominios
        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'activity_rate': round(active_users / total_users * 100, 2) if total_users > 0 else 0,
            'top_email_domains': [
                {'domain': domain, 'count': count} 
                for domain, count in top_domains
            ],
            'timestamp': self.fixed_timestamp,
            'report_version': '1.0'
        }
    
    def generate_performance_report(self, metrics: List[float]) -> Dict[str, Any]:
        """
        Genera reporte de rendimiento
        Usado para detectar regresiones de performance
        """
        if not metrics:
            return {
                'error': 'No metrics provided',
                'timestamp': self.fixed_timestamp
            }
        
        return {
            'metrics_count': len(metrics),
            'min_value': round(min(metrics), 3),
            'max_value': round(max(metrics), 3),
            'mean': round(statistics.mean(metrics), 3),
            'median': round(statistics.median(metrics), 3),
            'std_dev': round(statistics.stdev(metrics) if len(metrics) > 1 else 0, 3),
            'percentiles': {
                'p90': round(self._percentile(metrics, 90), 3),
                'p95': round(self._percentile(metrics, 95), 3),
                'p99': round(self._percentile(metrics, 99), 3)
            },
            'timestamp': self.fixed_timestamp,
            'report_version': '1.0'
        }
    
    def generate_trend_analysis(self, daily_data: Dict[str, int]) -> Dict[str, Any]:
        """
        Analiza tendencias en datos temporales
        Para detectar cambios en patrones
        """
        if not daily_data:
            return {
                'error': 'No data provided',
                'timestamp': self.fixed_timestamp
            }
        
        # Ordenar por fecha
        sorted_dates = sorted(daily_data.keys())
        values = [daily_data[date] for date in sorted_dates]
        
        # Calcular tendencia simple
        if len(values) >= 2:
            trend = 'increasing' if values[-1] > values[0] else 'decreasing' if values[-1] < values[0] else 'stable'
            change_percent = round(((values[-1] - values[0]) / values[0]) * 100, 2) if values[0] != 0 else 0
        else:
            trend = 'insufficient_data'
            change_percent = 0
        
        return {
            'date_range': {
                'start': sorted_dates[0],
                'end': sorted_dates[-1],
                'days': len(sorted_dates)
            },
            'trend': trend,
            'change_percent': change_percent,
            'total_sum': sum(values),
            'daily_average': round(sum(values) / len(values), 2),
            'peak_day': {
                'date': sorted_dates[values.index(max(values))],
                'value': max(values)
            },
            'lowest_day': {
                'date': sorted_dates[values.index(min(values))],
                'value': min(values)
            },
            'timestamp': self.fixed_timestamp,
            'report_version': '1.0'
        }
    
    def _percentile(self, data: List[float], p: float) -> float:
        """Calcula percentil específico"""
        sorted_data = sorted(data)
        index = (p / 100.0) * (len(sorted_data) - 1)
        lower = int(index)
        upper = lower + 1
        
        if upper >= len(sorted_data):
            return sorted_data[-1]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

# ============================================================================
# ARCHIVO 3: src/data_processor.py (Para performance regression)
# ============================================================================

"""
Procesador de datos con funciones que pueden degradarse
Usado para detectar regresiones de rendimiento
"""

import time
import random
from typing import List, Dict, Any

class DataProcessor:
    """
    Procesador de datos con diferentes algoritmos
    Algunos pueden degradarse accidentalmente
    """
    
    def process_user_list(self, users: List[Dict]) -> List[Dict]:
        """
        Procesa lista de usuarios - función que debe mantener rendimiento
        """
        # Simular tiempo de procesamiento predecible
        time.sleep(0.001 * len(users))  # 1ms por usuario
        
        processed = []
        for user in users:
            processed_user = {
                'id': user.get('id'),
                'username': user.get('username', '').upper(),
                'email_domain': user.get('email', '').split('@')[-1] if '@' in user.get('email', '') else 'unknown',
                'processed_at': time.time()
            }
            processed.append(processed_user)
        
        return processed
    
    def search_users(self, users: List[Dict], query: str) -> List[Dict]:
        """
        Búsqueda de usuarios - algoritmo O(n) que debe mantenerse eficiente
        """
        start_time = time.time()
        
        results = []
        query_lower = query.lower()
        
        for user in users:
            # Búsqueda en username y email
            username = user.get('username', '').lower()
            email = user.get('email', '').lower()
            
            if query_lower in username or query_lower in email:
                results.append(user)
        
        # Simular que no debe tomar más de cierto tiempo
        elapsed = time.time() - start_time
        if elapsed > 0.1:  # Warning si toma más de 100ms
            print(f"WARNING: search_users took {elapsed:.3f}s for {len(users)} users")
        
        return results
    
    def calculate_statistics(self, numbers: List[float]) -> Dict[str, float]:
        """
        Calcula estadísticas - función matemática que debe ser rápida
        """
        if not numbers:
            return {}
        
        # Implementación eficiente
        sorted_nums = sorted(numbers)
        n = len(numbers)
        
        return {
            'count': n,
            'sum': sum(numbers),
            'mean': sum(numbers) / n,
            'median': sorted_nums[n // 2] if n % 2 == 1 else (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2,
            'min': min(numbers),
            'max': max(numbers),
            'range': max(numbers) - min(numbers)
        }
    
    def slow_algorithm(self, data: List[Any]) -> int:
        """
        Algoritmo intencionalmente lento para demostrar regression testing
        Esta función DEBERÍA ser optimizada en el futuro
        """
        # Algoritmo O(n²) ineficiente a propósito
        count = 0
        for i in range(len(data)):
            for j in range(len(data)):
                if i != j:
                    count += 1
        return count
    
    def optimized_algorithm(self, data: List[Any]) -> int:
        """
        Versión optimizada del algoritmo anterior
        Debería usarse en lugar de slow_algorithm
        """
        # Algoritmo O(1) - matemáticas simples
        n = len(data)
        return n * (n - 1) if n > 1 else 0

# ============================================================================
# ARCHIVO 4: tests/smoke/test_core_functionality.py (Smoke tests)
# ============================================================================

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
        return "http://localhost:5000"
    
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

# ============================================================================
# ARCHIVO 5: tests/regression/historical/test_fixed_bugs.py (Regression histórica)
# ============================================================================

"""
Tests de regresión para bugs que se arreglaron en el pasado
Estos tests aseguran que los bugs no vuelvan a aparecer
"""

import pytest
from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator

@pytest.mark.regression
class TestHistoricalBugFixes:
    """Tests para bugs específicos que se arreglaron antes"""
    
    def test_bug_001_empty_username_handling(self):
        """
        BUG #001 (Fixed 2024-01-15): Crash cuando username está vacío
        Antes: KeyError cuando username era None o ''
        Ahora: Debe manejar gracefully
        """
        processor = DataProcessor()
        
        # Casos que antes causaban crash
        problematic_users = [
            {'id': 1, 'username': None, 'email': 'test1@example.com'},
            {'id': 2, 'username': '', 'email': 'test2@example.com'},
            {'id': 3, 'email': 'test3@example.com'},  # Sin username
        ]
        
        # No debe lanzar excepción
        processed = processor.process_user_list(problematic_users)
        
        assert len(processed) == 3
        # Debe manejar usernames problemáticos
        assert processed[0]['username'] == ''  # None -> ''
        assert processed[1]['username'] == ''  # '' -> ''
        assert processed[2]['username'] == ''  # Missing -> ''
    
    def test_bug_002_division_by_zero_in_stats(self):
        """
        BUG #002 (Fixed 2024-01-20): División por cero en estadísticas
        Antes: ZeroDivisionError con listas vacías
        Ahora: Debe retornar dict vacío
        """
        processor = DataProcessor()
        
        # Caso que antes causaba ZeroDivisionError
        empty_list = []
        stats = processor.calculate_statistics(empty_list)
        
        # Debe retornar dict vacío, no crash
        assert stats == {}
    
    def test_bug_003_email_domain_extraction_crash(self):
        """
        BUG #003 (Fixed 2024-01-25): Crash extrayendo dominio de email inválido
        Antes: IndexError cuando email no tenía '@'
        Ahora: Debe retornar 'unknown'
        """
        processor = DataProcessor()
        
        # Emails problemáticos que antes causaban crash
        users_with_bad_emails = [
            {'id': 1, 'username': 'user1', 'email': 'notanemail'},
            {'id': 2, 'username': 'user2', 'email': ''},
            {'id': 3, 'username': 'user3'},  # Sin email
        ]
        
        processed = processor.process_user_list(users_with_bad_emails)
        
        # Todos deben tener email_domain = 'unknown'
        for user in processed:
            assert user['email_domain'] == 'unknown'
    
    def test_bug_004_report_percentage_calculation(self):
        """
        BUG #004 (Fixed 2024-02-01): Cálculo erróneo de porcentajes
        Antes: activity_rate mostraba valores incorrectos
        Ahora: Debe calcular correctamente
        """
        generator = ReportGenerator()
        
        # Caso específico que daba resultado incorrecto
        users = [
            {'id': 1, 'username': 'user1', 'email': 'user1@test.com', 'is_active': True},
            {'id': 2, 'username': 'user2', 'email': 'user2@test.com', 'is_active': True},
            {'id': 3, 'username': 'user3', 'email': 'user3@test.com', 'is_active': False},
            {'id': 4, 'username': 'user4', 'email': 'user4@test.com', 'is_active': False},
        ]
        
        report = generator.generate_user_summary(users)
        
        # 2 activos de 4 total = 50%
        assert report['activity_rate'] == 50.0
        assert report['active_users'] == 2
        assert report['inactive_users'] == 2

# ============================================================================
# ARCHIVO 6: tests/regression/golden/test_report_outputs.py (Golden tests)
# ============================================================================

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

# ============================================================================
# ARCHIVO 7: tests/regression/performance/test_performance_regression.py
# ============================================================================

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

# ============================================================================
# ARCHIVO 8: locustfile.py (Load testing con Locust)
# ============================================================================

"""
Script principal de Locust para load testing
Define comportamientos realistas de usuarios
"""

from locust import HttpUser, task, between, events
import random
import json
import time
from typing import Dict, Any

class WebsiteUser(HttpUser):
    """
    Usuario típico del sitio web
    Simula comportamiento realista con diferentes patrones
    """
    
    # Tiempo de espera entre requests (simula tiempo de lectura/navegación)
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Setup inicial para cada usuario simulado
        Se ejecuta una vez al inicio de cada usuario
        """
        self.username = f"loadtest_user_{random.randint(1000, 9999)}"
        self.email = f"{self.username}@loadtest.com"
        self.user_id = None
        
        # Crear usuario de prueba
        self.create_test_user()
    
    def create_test_user(self):
        """Crea usuario de prueba para este usuario simulado"""
        user_data = {
            'username': self.username,
            'email': self.email
        }
        
        with self.client.post("/api/users", json=user_data, catch_response=True) as response:
            if response.status_code == 201:
                data = response.json()
                self.user_id = data.get('id')
            elif response.status_code == 409:
                # Usuario ya existe, está bien
                pass
            else:
                response.failure(f"Failed to create user: {response.status_code}")
    
    @task(10)  # Peso 10: más frecuente
    def view_homepage(self):
        """
        Simula visita a página principal
        Operación más común y rápida
        """
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Health check failed: {response.status_code}")
    
    @task(8)  # Peso 8: frecuente
    def list_users(self):
        """
        Simula listado de usuarios
        Operación de lectura común
        """
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if 'users' not in data:
                    response.failure("Invalid response format")
            else:
                response.failure(f"Failed to list users: {response.status_code}")
    
    @task(6)  # Peso 6: moderadamente frecuente
    def view_posts(self):
        """
        Simula navegación por posts con paginación
        """
        page = random.randint(1, 3)
        per_page = random.choice([5, 10, 20])
        
        with self.client.get(f"/api/posts?page={page}&per_page={per_page}", 
                           catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if 'posts' not in data or 'pagination' not in data:
                    response.failure("Invalid posts response")
            else:
                response.failure(f"Failed to get posts: {response.status_code}")
    
    @task(4)  # Peso 4: menos frecuente
    def search_users(self):
        """
        Simula búsqueda de usuarios
        Operación más costosa
        """
        queries = ['user', 'test', 'admin', 'demo', 'sample']
        query = random.choice(queries)
        
        with self.client.get(f"/api/search?q={query}", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if 'results' not in data:
                    response.failure("Invalid search response")
            else:
                response.failure(f"Search failed: {response.status_code}")
    
    @task(2)  # Peso 2: poco frecuente
    def view_specific_user(self):
        """
        Simula ver usuario específico
        """
        if self.user_id:
            user_id = self.user_id
        else:
            user_id = random.randint(1, 10)  # IDs de usuarios de prueba
        
        with self.client.get(f"/api/users/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if 'id' not in data:
                    response.failure("Invalid user response")
            elif response.status_code == 404:
                # Usuario no encontrado es válido
                pass
            else:
                response.failure(f"Failed to get user: {response.status_code}")
    
    @task(1)  # Peso 1: raro
    def create_new_user(self):
        """
        Simula creación de nuevo usuario
        Operación de escritura menos frecuente
        """
        timestamp = int(time.time())
        new_user_data = {
            'username': f'newuser_{timestamp}_{random.randint(100, 999)}',
            'email': f'newuser_{timestamp}@example.com'
        }
        
        with self.client.post("/api/users", json=new_user_data, catch_response=True) as response:
            if response.status_code == 201:
                data = response.json()
                if 'id' not in data:
                    response.failure("Invalid create user response")
            elif response.status_code == 409:
                # Conflicto de usuario existente es válido
                pass
            else:
                response.failure(f"Failed to create user: {response.status_code}")

class HeavyUser(HttpUser):
    """
    Usuario que realiza operaciones pesadas
    Para stress testing y encontrar límites
    """
    
    wait_time = between(0.5, 1.5)  # Más agresivo
    weight = 1  # Menos instancias de este tipo
    
    @task(5)
    def heavy_operation(self):
        """Ejecuta operación pesada"""
        with self.client.post("/api/heavy-operation", catch_response=True) as response:
            if response.status_code == 200:
                # Verificar que no tome demasiado tiempo
                if response.elapsed.total_seconds() > 5:
                    response.failure(f"Heavy operation too slow: {response.elapsed.total_seconds()}s")
            elif response.status_code == 500:
                # Algunos errores son esperados en operaciones pesadas
                pass
            else:
                response.failure(f"Heavy operation failed: {response.status_code}")
    
    @task(3)
    def slow_endpoint(self):
        """Accede al endpoint intencionalmente lento"""
        with self.client.get("/api/slow", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Slow endpoint failed: {response.status_code}")

class MonitoringUser(HttpUser):
    """
    Usuario que monitorea estadísticas del sistema
    Simula dashboards y monitoring
    """
    
    wait_time = between(5, 10)  # Consultas menos frecuentes
    weight = 1  # Pocas instancias
    
    @task
    def check_stats(self):
        """Consulta estadísticas del sistema"""
        with self.client.get("/api/stats", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if 'total_requests' not in data:
                    response.failure("Invalid stats response")
            else:
                response.failure(f"Stats check failed: {response.status_code}")

# Event listeners para métricas personalizadas
@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response, 
                      context, exception, start_time, url, **kwargs):
    """
    Handler personalizado para requests
    Permite logging y métricas personalizadas
    """
    if exception:
        print(f"Request failed: {name} - {exception}")
    elif response_time > 1000:  # Log requests lentas (>1s)
        print(f"Slow request detected: {name} took {response_time}ms")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Se ejecuta al inicio del test"""
    print("🚀 Load test starting...")
    print(f"Target host: {environment.host}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Se ejecuta al final del test"""
    print("🏁 Load test completed!")
    
    # Log estadísticas finales
    stats = environment.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.num_failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"Max response time: {stats.total.max_response_time}ms")

# ============================================================================
# ARCHIVO 9: pytest.ini (Configuración actualizada)
# ============================================================================

"""
# Contenido actualizado del archivo pytest.ini

[tool:pytest]
testpaths = tests

python_files = test_*.py *_test.py
python_functions = test_*
python_classes = Test*

addopts = 
    -v
    --strict-markers
    --strict-config
    --tb=short
    -ra

# Marcadores para diferentes tipos de pruebas
markers =
    smoke: smoke tests críticos (deben ejecutarse primero)
    regression: tests de regresión (previenen retrocesos)
    golden: golden/snapshot tests (outputs estables)
    performance: tests de rendimiento (benchmarking)
    slow: tests que tardan >1 segundo
    integration: tests de integración
    unit: tests unitarios

# Configuración para pytest-benchmark
addopts = --benchmark-skip

# Para ejecutar benchmarks solamente:
# pytest --benchmark-only

# Configuración de pytest-regressions para golden tests
regressions_data_dir = tests/regression/golden/test_data
"""

# ============================================================================
# ARCHIVO 10: requirements.txt (Dependencias completas)
# ============================================================================

"""
# Dependencias para el proyecto completo

# Framework de testing básico
pytest>=7.0.0
pytest-mock>=3.10.0
pytest-cov>=4.0.0
pytest-xdist>=3.0.0

# Regression testing específico
pytest-regressions>=2.4.0     # Golden/snapshot testing
pytest-benchmark>=4.0.0       # Performance benchmarking
pytest-html>=3.1.0           # Reportes HTML

# Load testing
locust>=2.14.0                # Framework de load testing

# API y servidor
flask>=2.2.0                  # API server para testing
requests>=2.28.0              # Cliente HTTP

# Utilidades
faker>=15.0.0                 # Datos sintéticos
"""

# ============================================================================
# ARCHIVO 11: scripts/run_regression_suite.py (Script de automatización)
# ============================================================================

"""
Script para ejecutar suite completa de regresión
Automatiza diferentes tipos de pruebas en orden apropiado
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Ejecuta comando y retorna True si es exitoso"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    duration = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} - OK ({duration:.2f}s)")
        return True
    else:
        print(f"❌ {description} - FAILED ({duration:.2f}s)")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

def main():
    """Ejecuta suite completa de regresión"""
    print("🚀 Starting comprehensive regression testing suite")
    
    # 1. Smoke Tests (críticos, deben pasar primero)
    print("\n" + "="*60)
    print("PHASE 1: SMOKE TESTS (Critical)")
    print("="*60)
    
    if not run_command(
        "pytest tests/smoke/ -v --maxfail=1 --tb=short",
        "Smoke tests (critical functionality)"
    ):
        print("\n💥 CRITICAL: Smoke tests failed! Stopping execution.")
        print("Fix critical issues before continuing with regression suite.")
        sys.exit(1)
    
    # 2. Golden Tests (detectar cambios no intencionales)
    print("\n" + "="*60)
    print("PHASE 2: GOLDEN TESTS (Behavior verification)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/golden/ -v",
        "Golden tests (output verification)"
    )
    
    # 3. Historical Regression (bugs del pasado)
    print("\n" + "="*60)
    print("PHASE 3: HISTORICAL REGRESSION (Bug prevention)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/historical/ -v",
        "Historical bug regression tests"
    )
    
    # 4. Performance Regression (detectar degradación)
    print("\n" + "="*60)
    print("PHASE 4: PERFORMANCE REGRESSION (Speed verification)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/performance/ --benchmark-only --benchmark-sort=mean",
        "Performance regression benchmarks"
    )
    
    # 5. Generar reportes
    print("\n" + "="*60)
    print("PHASE 5: REPORTING")
    print("="*60)
    
    run_command(
        "pytest tests/regression/ --html=reports/regression_report.html --self-contained-html",
        "Generate HTML regression report"
    )
    
    run_command(
        "pytest tests/regression/ --cov=src --cov-report=html:reports/coverage",
        "Generate coverage report"
    )
    
    print("\n" + "="*60)
    print("🎉 REGRESSION SUITE COMPLETED")
    print("="*60)
    print("📊 Reports generated:")
    print("  - HTML Report: reports/regression_report.html")
    print("  - Coverage: reports/coverage/index.html")
    print("  - Benchmark results in terminal output")
    
    print("\n📋 Next steps:")
    print("  1. Review any failed tests")
    print("  2. Update golden files if intentional changes: pytest --force-regen")
    print("  3. Run load tests: locust -f locustfile.py --host=http://localhost:5000")

if __name__ == "__main__":
    main()

# ============================================================================
# ARCHIVO 12: scripts/run_load_test.py (Automatización de load testing)
# ============================================================================

"""
Script para automatizar load testing con diferentes escenarios
"""

import subprocess
import time
import requests
import signal
import os
import sys
from pathlib import Path

class LoadTestRunner:
    """Automatiza ejecución de load tests con diferentes configuraciones"""
    
    def __init__(self, host="http://localhost:5000"):
        self.host = host
        self.server_process = None
    
    def check_server_health(self) -> bool:
        """Verifica que el servidor esté respondiendo"""
        try:
            response = requests.get(f"{self.host}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_server_if_needed(self):
        """Inicia servidor si no está corriendo"""
        if self.check_server_health():
            print(f"✅ Server already running at {self.host}")
            return
        
        print(f"🚀 Starting server at {self.host}...")
        self.server_process = subprocess.Popen([
            sys.executable, "src/app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que el servidor inicie
        for i in range(30):  # Máximo 30 segundos
            if self.check_server_health():
                print(f"✅ Server started successfully")
                return
            time.sleep(1)
        
        raise Exception("Failed to start server")
    
    def stop_server(self):
        """Detiene servidor si fue iniciado por este script"""
        if self.server_process:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
    
    def run_load_test(self, users: int, duration: str, description: str):
        """Ejecuta load test con configuración específica"""
        print(f"\n🔄 {description}")
        print(f"Users: {users}, Duration: {duration}")
        
        cmd = [
            "locust",
            "-f", "locustfile.py",
            "--host", self.host,
            "--users", str(users),
            "--spawn-rate", str(min(users // 10, 10)),  # Spawn rate razonable
            "--run-time", duration,
            "--headless",  # Sin interfaz web
            "--html", f"reports/load_test_{users}users_{duration.replace('m', 'min')}.html"
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration_actual = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - Completed ({duration_actual:.1f}s)")
            
            # Extraer métricas básicas del output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'Aggregated' in line or 'Total' in line:
                    print(f"📊 {line.strip()}")
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
    
    def run_test_suite(self):
        """Ejecuta suite completa de load tests"""
        try:
            self.start_server_if_needed()
            
            print("\n" + "="*60)
            print("LOAD TESTING SUITE")
            print("="*60)
            
            # 1. Smoke load test
            self.run_load_test(
                users=5,
                duration="1m",
                description="Smoke load test (light load verification)"
            )
            
            # 2. Normal load test
            self.run_load_test(
                users=20,
                duration="3m",
                description="Normal load test (typical usage)"
            )
            
            # 3. Stress test
            self.run_load_test(
                users=50,
                duration="2m",
                description="Stress test (high load)"
            )
            
            # 4. Spike test (rápido pero intenso)
            self.run_load_test(
                users=100,
                duration="30s",
                description="Spike test (sudden load increase)"
            )
            
            print("\n" + "="*60)
            print("🎉 LOAD TESTING COMPLETED")
            print("="*60)
            print("📊 Reports generated in reports/ directory")
            print("📋 Review HTML reports for detailed metrics")
            
        finally:
            self.stop_server()

def main():
    """Función principal"""
    # Crear directorio de reportes
    Path("reports").mkdir(exist_ok=True)
    
    runner = LoadTestRunner()
    
    # Manejar Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Load testing interrupted")
        runner.stop_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        runner.run_test_suite()
    except Exception as e:
        print(f"❌ Load testing failed: {e}")
        runner.stop_server()
        sys.exit(1)

if __name__ == "__main__":
    main()

# ============================================================================
# COMANDOS DE EJECUCIÓN Y EJEMPLOS
# ============================================================================

"""
COMANDOS PRINCIPALES PARA TESTING DE REGRESIÓN Y CARGA:

=== SMOKE TESTS (Críticos) ===
pytest tests/smoke/ -v --maxfail=1
pytest -m smoke --tb=short

=== REGRESSION SUITE COMPLETA ===
python scripts/run_regression_suite.py

=== GOLDEN TESTS (Snapshot testing) ===
# Ejecutar y comparar con referencias
pytest tests/regression/golden/ -v

# Actualizar referencias (después de cambios intencionales)
pytest tests/regression/golden/ --force-regen

=== PERFORMANCE REGRESSION ===
# Solo benchmarks
pytest tests/regression/performance/ --benchmark-only

# Comparar con baseline anterior
pytest tests/regression/performance/ --benchmark-compare=baseline.json

# Guardar nuevo baseline
pytest tests/regression/performance/ --benchmark-save=baseline

=== LOAD TESTING ===
# Suite automatizada completa
python scripts/run_load_test.py

# Manual con interfaz web
locust -f locustfile.py --host=http://localhost:5000

# Headless con configuración específica
locust -f locustfile.py --host=http://localhost:5000 \
       --users 50 --spawn-rate 5 --run-time 5m --headless

# Distribuido (master)
locust -f locustfile.py --master --host=http://production.com

# Distribuido (workers)
locust -f locustfile.py --worker --master-host=master-ip

=== COMBINACIONES ÚTILES ===
# CI/CD Pipeline básico
pytest tests/smoke/ --maxfail=1 && \
pytest tests/regression/ --html=reports/regression.html

# Performance tracking
pytest tests/regression/performance/ --benchmark-only \
       --benchmark-json=reports/benchmark.json

# Full regression con coverage
pytest tests/regression/ --cov=src --cov-report=html:reports/coverage \
       --html=reports/full_regression.html

EJEMPLOS DE SALIDA:

=== Smoke Tests ===
$ pytest tests/smoke/ -v
========================= test session starts =========================
collected 6 items

tests/smoke/test_core_functionality.py::TestCoreAPI::test_health_endpoint_responds PASSED
tests/smoke/test_core_functionality.py::TestCoreAPI::test_users_endpoint_basic PASSED
tests/smoke/test_core_functionality.py::TestCoreAPI::test_user_creation_basic PASSED
tests/smoke/test_core_functionality.py::TestCoreComponents::test_report_generator_basic PASSED
tests/smoke/test_core_functionality.py::TestCoreComponents::test_data_processor_basic PASSED

==================== 6 passed, 0 failed in 2.34s ====================

=== Performance Benchmark ===
$ pytest tests/regression/performance/ --benchmark-only
========================= test session starts =========================

tests/regression/performance/test_performance_regression.py::TestPerformanceRegression::test_user_processing_performance

Name (time in ms)                Min       Max      Mean    StdDev    Median     IQR
------------------------------------------------------------------------------------------
test_user_processing_performance  45.23    52.87    48.45     2.34     47.82    3.21

tests/regression/performance/test_performance_regression.py::TestPerformanceRegression::test_search_performance

Name (time in ms)                Min       Max      Mean    StdDev    Median     IQR
------------------------------------------------------------------------------------------
test_search_performance          12.45    18.76    15.23     1.89     14.87    2.34

=== Load Testing Output ===
$ locust -f locustfile.py --headless --users 20 --spawn-rate 2 --run-time 1m
[2024-01-01 10:00:00,000] INFO/locust.main: Starting Locust 2.14.0
[2024-01-01 10:00:00,001] INFO/locust.runners: Spawning 20 users at the rate 2 users/s...
[2024-01-01 10:01:00,123] INFO/locust.main: Running performance tests...

Type     Name                    # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|-----------------------|-----------|---------|-------|-------|-------|-------|-------|-----------
GET      /api/users              156          0(0.00%) |    125      89     234    120 |    2.60        0.00
GET      /api/posts               98          0(0.00%) |    187     134     312    178 |    1.63        0.00
GET      /api/search              67          1(1.49%) |    245     156     567    234 |    1.12        0.02
POST     /api/users               23          0(0.00%) |    167     123     289    156 |    0.38        0.00
--------|-----------------------|-----------|---------|-------|-------|-------|-------|-------|-----------
         Aggregated             344          1(0.29%) |    156      89     567    145 |    5.73        0.02

Response time percentiles (approximated):
Type     Name                     50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-----------------------|------|------|------|------|------|------|------|------|------|------|------|------
GET      /api/users               120    135    145    156    178    201    223    234    234    234    234    156
GET      /api/posts               178    198    234    245    278    289    312    312    312    312    312     98
--------|-----------------------|------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated              145    167    189    201    234    278    312    567    567    567    567    344
"""

if __name__ == "__main__":
    print("Sistema completo de pruebas de regresión y carga")
    print("\n🔍 Componentes incluidos:")
    print("  - Smoke tests críticos")
    print("  - Golden/snapshot testing")
    print("  - Regression de bugs históricos")
    print("  - Performance regression con benchmarks")
    print("  - Load testing completo con Locust")
    print("  - Scripts de automatización")
    print("\n🚀 Comandos principales:")
    print("  python scripts/run_regression_suite.py  # Suite completa")
    print("  python scripts/run_load_test.py         # Load testing")
    print("  pytest tests/smoke/ -v                  # Solo smoke tests")
    print("  locust -f locustfile.py                 # Load test manual")
    print("\n📊 Los reportes se generan en reports/")
    print("\nPara más detalles, ver comentarios en el código.")
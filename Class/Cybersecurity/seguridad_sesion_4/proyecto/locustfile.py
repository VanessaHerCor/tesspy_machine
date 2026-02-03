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
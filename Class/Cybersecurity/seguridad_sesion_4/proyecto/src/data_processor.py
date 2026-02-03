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
                'username': (user.get('username') or '').upper(),
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
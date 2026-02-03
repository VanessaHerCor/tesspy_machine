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
# ============================================================================
# ARCHIVO 4: src/api_client.py
# ============================================================================

"""Cliente para servicios externos - perfecto para unit testing con mocks"""

import requests
from typing import Dict, Any, Optional
from .exceptions import ExternalServiceError

class ExternalUserValidationClient:
    """
    Cliente que valida usuarios contra un servicio externo
    Ejemplo perfecto de dependencia externa que necesita mocking
    """
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """Inicializa cliente con configuración"""
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """
        Valida email contra servicio externo
        Esta función será mockeada en unit tests
        """
        try:
            response = self.session.get(
                f"{self.base_url}/validate/email",
                params={'email': email},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                'valid': data.get('valid', False),
                'deliverable': data.get('deliverable', False),
                'risk_score': data.get('risk_score', 1.0),
                'provider': data.get('provider', 'unknown')
            }
        
        except requests.exceptions.Timeout:
            raise ExternalServiceError("Timeout validando email")
        except requests.exceptions.ConnectionError:
            raise ExternalServiceError("Error de conexión con servicio de validación")
        except requests.exceptions.HTTPError as e:
            raise ExternalServiceError(f"Error HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado validando email: {str(e)}")
    
    def check_user_reputation(self, username: str, email: str) -> Dict[str, Any]:
        """
        Verifica reputación del usuario en servicios externos
        Otra función ideal para mocking
        """
        try:
            payload = {
                'username': username,
                'email': email
            }
            
            response = self.session.post(
                f"{self.base_url}/reputation/check",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                'reputation_score': data.get('reputation_score', 0.5),
                'blocked': data.get('blocked', False),
                'risk_factors': data.get('risk_factors', []),
                'recommendation': data.get('recommendation', 'review')
            }
        
        except requests.exceptions.RequestException as e:
            raise ExternalServiceError(f"Error verificando reputación: {str(e)}")
    
    def notify_user_created(self, user_data: Dict[str, Any]) -> bool:
        """
        Notifica a servicio externo sobre nuevo usuario
        Función que puede fallar y necesita manejo de errores
        """
        try:
            response = self.session.post(
                f"{self.base_url}/notifications/user_created",
                json=user_data,
                timeout=self.timeout
            )
            
            # 2xx = éxito, otros códigos no son críticos
            return response.status_code < 300
        
        except requests.exceptions.RequestException:
            # Notificación no crítica, no fallar el proceso principal
            return False
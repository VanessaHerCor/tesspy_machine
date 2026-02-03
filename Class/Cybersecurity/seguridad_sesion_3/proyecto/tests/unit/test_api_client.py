# ============================================================================
# ARCHIVO 9: tests/unit/test_api_client.py (Unit tests para API client)
# ============================================================================

"""
Unit tests para ExternalUserValidationClient
Enfoque: Mocking de requests HTTP
"""

import pytest
from unittest.mock import Mock, patch
import requests
from src.api_client import ExternalUserValidationClient
from src.exceptions import ExternalServiceError

class TestExternalUserValidationClient:
    """Unit tests para cliente de API externa"""
    
    @pytest.fixture
    def api_client(self):
        """Fixture que proporciona cliente configurado"""
        return ExternalUserValidationClient(
            base_url="https://api.example.com",
            api_key="test_key_123",
            timeout=5
        )
    
    @patch('src.api_client.requests.Session.get')
    def test_validate_email_success(self, mock_get, api_client):
        """Prueba validación exitosa de email"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            'valid': True,
            'deliverable': True,
            'risk_score': 0.1,
            'provider': 'gmail'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = api_client.validate_email("test@gmail.com")
        
        # Assert
        assert result['valid'] is True
        assert result['deliverable'] is True
        assert result['risk_score'] == 0.1
        assert result['provider'] == 'gmail'
        
        mock_get.assert_called_once_with(
            "https://api.example.com/validate/email",
            params={'email': 'test@gmail.com'},
            timeout=5
        )
    
    @patch('src.api_client.requests.Session.get')
    def test_validate_email_timeout(self, mock_get, api_client):
        """Prueba manejo de timeout"""
        # Arrange
        mock_get.side_effect = requests.exceptions.Timeout()
        
        # Act & Assert
        with pytest.raises(ExternalServiceError, match="Timeout validando email"):
            api_client.validate_email("test@example.com")
    
    @patch('src.api_client.requests.Session.get')
    def test_validate_email_http_error(self, mock_get, api_client):
        """Prueba manejo de errores HTTP"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        # Act & Assert
        with pytest.raises(ExternalServiceError, match="Error HTTP 400"):
            api_client.validate_email("invalid@email")
    
    @patch('src.api_client.requests.Session.post')
    def test_check_user_reputation_success(self, mock_post, api_client):
        """Prueba verificación exitosa de reputación"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            'reputation_score': 0.8,
            'blocked': False,
            'risk_factors': [],
            'recommendation': 'approve'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Act
        result = api_client.check_user_reputation("testuser", "test@example.com")
        
        # Assert
        assert result['reputation_score'] == 0.8
        assert result['blocked'] is False
        assert result['recommendation'] == 'approve'
        
        expected_payload = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        mock_post.assert_called_once_with(
            "https://api.example.com/reputation/check",
            json=expected_payload,
            timeout=5
        )
    
    @patch('src.api_client.requests.Session.post')
    def test_notify_user_created_success(self, mock_post, api_client):
        """Prueba notificación exitosa"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        user_data = {'id': 1, 'username': 'testuser'}
        
        # Act
        result = api_client.notify_user_created(user_data)
        
        # Assert
        assert result is True
        mock_post.assert_called_once_with(
            "https://api.example.com/notifications/user_created",
            json=user_data,
            timeout=5
        )
    
    @patch('src.api_client.requests.Session.post')
    def test_notify_user_created_failure_graceful(self, mock_post, api_client):
        """Prueba que notificación falle gracefully"""
        # Arrange
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        # Act
        result = api_client.notify_user_created({'id': 1})
        
        # Assert - no debe lanzar excepción, retorna False
        assert result is False
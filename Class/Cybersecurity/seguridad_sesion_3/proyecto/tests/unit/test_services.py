# ============================================================================
# ARCHIVO 8: tests/unit/test_services.py (Unit tests para servicios)
# ============================================================================

"""
Unit tests para UserService
Enfoque: Lógica de negocio aislada usando mocks
"""

import pytest
from unittest.mock import Mock, patch
from src.services import UserService
from src.models import User
from src.exceptions import InvalidUserDataError, UserAlreadyExistsError, ExternalServiceError

class TestUserServiceCreateUser:
    """Unit tests para creación de usuarios usando mocks"""
    
    def test_create_user_success_without_external_validation(self, user_service_with_mocks, mock_repository):
        """Prueba creación exitosa sin validación externa"""
        # Arrange
        mock_repository.exists_username.return_value = False
        mock_repository.exists_email.return_value = False
        mock_repository.create.return_value = User("testuser", "test@example.com", "Test User")
        
        service = user_service_with_mocks
        
        # Act
        result = service.create_user("testuser", "test@example.com", "Test User", validate_externally=False)
        
        # Assert
        assert result.username == "testuser"
        mock_repository.exists_username.assert_called_once_with("testuser")
        mock_repository.exists_email.assert_called_once_with("test@example.com")
        mock_repository.create.assert_called_once()
    
    def test_create_user_duplicate_username(self, user_service_with_mocks, mock_repository):
        """Prueba fallo por username duplicado"""
        # Arrange
        mock_repository.exists_username.return_value = True  # Username ya existe
        service = user_service_with_mocks
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="Username 'testuser' ya existe"):
            service.create_user("testuser", "test@example.com", "Test User")
        
        # Verificar que no se intentó crear
        mock_repository.create.assert_not_called()
    
    def test_create_user_duplicate_email(self, user_service_with_mocks, mock_repository):
        """Prueba fallo por email duplicado"""
        # Arrange
        mock_repository.exists_username.return_value = False
        mock_repository.exists_email.return_value = True  # Email ya existe
        service = user_service_with_mocks
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError, match="Email 'test@example.com' ya existe"):
            service.create_user("testuser", "test@example.com", "Test User")
    
    def test_create_user_invalid_data(self, user_service_with_mocks):
        """Prueba fallo por datos inválidos (usando lógica del modelo)"""
        service = user_service_with_mocks
        
        # Act & Assert - username inválido
        with pytest.raises(InvalidUserDataError, match="Datos inválidos"):
            service.create_user("ab", "test@example.com", "Test User")  # Username muy corto
    
    def test_create_user_with_external_validation_success(self, user_service_with_mocks, 
                                                         mock_repository, mock_api_client):
        """Prueba creación con validación externa exitosa"""
        # Arrange
        mock_repository.exists_username.return_value = False
        mock_repository.exists_email.return_value = False
        mock_repository.create.return_value = User("testuser", "test@example.com", "Test User")
        
        # Mock respuestas del API client
        mock_api_client.validate_email.return_value = {'valid': True, 'deliverable': True}
        mock_api_client.check_user_reputation.return_value = {'blocked': False, 'reputation_score': 0.8}
        mock_api_client.notify_user_created.return_value = True
        
        service = user_service_with_mocks
        
        # Act
        result = service.create_user("testuser", "test@example.com", "Test User", validate_externally=True)
        
        # Assert
        assert result.username == "testuser"
        mock_api_client.validate_email.assert_called_once_with("test@example.com")
        mock_api_client.check_user_reputation.assert_called_once_with("testuser", "test@example.com")
        mock_api_client.notify_user_created.assert_called_once()
    
    def test_create_user_blocked_by_reputation(self, user_service_with_mocks, 
                                             mock_repository, mock_api_client):
        """Prueba fallo por usuario bloqueado en validación externa"""
        # Arrange
        mock_repository.exists_username.return_value = False
        mock_repository.exists_email.return_value = False
        
        mock_api_client.validate_email.return_value = {'valid': True}
        mock_api_client.check_user_reputation.return_value = {'blocked': True}  # Usuario bloqueado
        
        service = user_service_with_mocks
        
        # Act & Assert
        with pytest.raises(InvalidUserDataError, match="Usuario bloqueado"):
            service.create_user("testuser", "test@example.com", "Test User", validate_externally=True)
    
    def test_create_user_external_service_failure_continues(self, user_service_with_mocks, 
                                                          mock_repository, mock_api_client):
        """Prueba que fallo de servicio externo no impide creación"""
        # Arrange
        mock_repository.exists_username.return_value = False
        mock_repository.exists_email.return_value = False
        mock_repository.create.return_value = User("testuser", "test@example.com", "Test User")
        
        # Simular fallo del servicio externo
        mock_api_client.validate_email.side_effect = ExternalServiceError("Servicio no disponible")
        
        service = user_service_with_mocks
        
        # Act - no debería fallar
        result = service.create_user("testuser", "test@example.com", "Test User", validate_externally=True)
        
        # Assert
        assert result.username == "testuser"
        mock_repository.create.assert_called_once()

class TestUserServiceOtherMethods:
    """Unit tests para otros métodos del servicio"""
    
    def test_get_user_success(self, user_service_with_mocks, mock_repository):
        """Prueba obtención exitosa de usuario"""
        # Arrange
        expected_user = User("testuser", "test@example.com", "Test User")
        mock_repository.get_by_id.return_value = expected_user
        service = user_service_with_mocks
        
        # Act
        result = service.get_user(1)
        
        # Assert
        assert result == expected_user
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_get_user_statistics(self, user_service_with_mocks, mock_repository):
        """Prueba obtención de estadísticas usando mocks"""
        # Arrange
        mock_users = [
            User("user1", "user1@example.com", "User 1"),
            User("user2", "user2@test.com", "User 2"),
            User("user3", "user3@example.com", "User 3")
        ]
        mock_repository.count_active_users.return_value = 3
        mock_repository.get_all_active.return_value = mock_users
        
        service = user_service_with_mocks
        
        # Act
        stats = service.get_user_statistics()
        
        # Assert
        assert stats['total_active_users'] == 3
        assert stats['total_users'] == 3
        assert 'users_by_domain' in stats
        assert stats['users_by_domain']['example.com'] == 2
        assert stats['users_by_domain']['test.com'] == 1
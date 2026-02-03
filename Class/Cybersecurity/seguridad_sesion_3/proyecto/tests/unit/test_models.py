# ============================================================================
# ARCHIVO 7: tests/unit/test_models.py (Unit tests para modelos)
# ============================================================================

"""
Unit tests para la clase User
Enfoque: Lógica de validación y métodos del modelo (sin BD)
"""

import pytest
from datetime import datetime
from src.models import User

class TestUserCreation:
    """Pruebas unitarias para creación de usuarios"""
    
    def test_create_valid_user(self):
        """Prueba creación de usuario válido"""
        # Arrange & Act
        user = User("testuser", "test@example.com", "Test User")
        
        # Assert
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
    
    @pytest.mark.parametrize("invalid_username,expected_error", [
        ("ab", "al menos 3 caracteres"),           # Muy corto
        ("a" * 51, "no puede exceder 50"),         # Muy largo
        ("user@123", "solo puede contener"),       # Caracteres especiales
        ("", "al menos 3 caracteres"),             # Vacío
    ])
    def test_invalid_username_validation(self, invalid_username, expected_error):
        """Prueba parametrizada para validación de username"""
        with pytest.raises(ValueError, match=expected_error):
            User(invalid_username, "test@example.com", "Test User")
    
    @pytest.mark.parametrize("invalid_email,expected_error", [
        ("notanemail", "formato válido"),          # Sin @
        ("", "formato válido"),                    # Vacío
        ("a" * 95 + "@test.com", "no puede exceder"), # Muy largo
    ])
    def test_invalid_email_validation(self, invalid_email, expected_error):
        """Prueba parametrizada para validación de email"""
        with pytest.raises(ValueError, match=expected_error):
            User("testuser", invalid_email, "Test User")
    
    @pytest.mark.parametrize("invalid_name,expected_error", [
        ("", "al menos 2 caracteres"),            # Vacío
        ("a", "al menos 2 caracteres"),           # Muy corto
        ("a" * 101, "no puede exceder 100"),      # Muy largo
        ("   ", "al menos 2 caracteres"),         # Solo espacios
    ])
    def test_invalid_full_name_validation(self, invalid_name, expected_error):
        """Prueba parametrizada para validación de nombre"""
        with pytest.raises(ValueError, match=expected_error):
            User("testuser", "test@example.com", invalid_name)

class TestUserMethods:
    """Pruebas unitarias para métodos de User"""
    
    def test_update_profile_valid_data(self, sample_user_model):
        """Prueba actualización válida de perfil"""
        # Arrange
        user = sample_user_model
        original_updated_at = user.updated_at
        
        # Act
        user.update_profile(email="new@example.com", full_name="New Name")
        
        # Assert
        assert user.email == "new@example.com"
        assert user.full_name == "New Name"
        assert user.updated_at > original_updated_at
    
    def test_update_profile_partial(self, sample_user_model):
        """Prueba actualización parcial de perfil"""
        user = sample_user_model
        original_email = user.email
        
        user.update_profile(full_name="Only Name Changed")
        
        assert user.email == original_email  # No cambió
        assert user.full_name == "Only Name Changed"
    
    def test_deactivate_user(self, sample_user_model):
        """Prueba desactivación de usuario"""
        user = sample_user_model
        assert user.is_active is True
        
        user.deactivate()
        
        assert user.is_active is False
        assert isinstance(user.updated_at, datetime)
    
    def test_activate_user(self, sample_user_model):
        """Prueba activación de usuario"""
        user = sample_user_model
        user.deactivate()  # Primero desactivar
        
        user.activate()
        
        assert user.is_active is True
    
    def test_to_dict_conversion(self, sample_user_model):
        """Prueba conversión a diccionario"""
        user = sample_user_model
        user_dict = user.to_dict()
        
        expected_keys = {'id', 'username', 'email', 'full_name', 'is_active', 'created_at', 'updated_at'}
        assert set(user_dict.keys()) == expected_keys
        assert user_dict['username'] == user.username
        assert user_dict['email'] == user.email
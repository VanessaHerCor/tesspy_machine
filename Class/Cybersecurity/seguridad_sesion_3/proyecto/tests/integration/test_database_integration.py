# ============================================================================
# ARCHIVO 10: tests/integration/test_database_integration.py (Integration tests)
# ============================================================================

"""
Integration tests para Repository y base de datos
Enfoque: Probar que componentes trabajen juntos con BD real
"""

import pytest
from sqlalchemy.exc import IntegrityError
from src.models import User
from src.exceptions import UserNotFoundError, UserAlreadyExistsError

@pytest.mark.integration
class TestUserRepositoryIntegration:
    """Integration tests para UserRepository con base de datos real"""
    
    def test_create_and_retrieve_user(self, real_repository, test_session):
        """Prueba flujo completo: crear y recuperar usuario"""
        # Arrange
        user = User("testuser", "test@example.com", "Test User")
        
        # Act - crear
        created_user = real_repository.create(user)
        test_session.commit()
        
        # Act - recuperar
        retrieved_user = real_repository.get_by_id(created_user.id)
        
        # Assert
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "test@example.com"
        assert retrieved_user.full_name == "Test User"
    
    def test_unique_constraints_enforcement(self, real_repository, test_session):
        """Prueba que constraints únicos se respeten en BD"""
        # Arrange
        user1 = User("testuser", "test@example.com", "Test User 1")
        user2 = User("testuser", "different@example.com", "Test User 2")  # Mismo username
        
        # Act - crear primer usuario
        real_repository.create(user1)
        test_session.commit()
        
        # Act & Assert - segundo usuario debe fallar
        with pytest.raises(UserAlreadyExistsError, match="Username 'testuser' ya existe"):
            real_repository.create(user2)
    
    def test_user_not_found_scenarios(self, real_repository):
        """Prueba escenarios donde usuario no existe"""
        # ID no existente
        with pytest.raises(UserNotFoundError, match="Usuario con ID 999"):
            real_repository.get_by_id(999)
        
        # Username no existente
        with pytest.raises(UserNotFoundError, match="Usuario 'nonexistent'"):
            real_repository.get_by_username("nonexistent")
        
        # Email no existente
        with pytest.raises(UserNotFoundError, match="Usuario con email"):
            real_repository.get_by_email("nonexistent@example.com")
    
    def test_update_user_flow(self, real_repository, test_session):
        """Prueba flujo de actualización de usuario"""
        # Arrange - crear usuario inicial
        user = User("testuser", "test@example.com", "Test User")
        created_user = real_repository.create(user)
        test_session.commit()
        
        # Act - modificar y actualizar
        created_user.update_profile(email="newemail@example.com", full_name="Updated Name")
        updated_user = real_repository.update(created_user)
        test_session.commit()
        
        # Assert - verificar cambios persistidos
        retrieved_user = real_repository.get_by_id(updated_user.id)
        assert retrieved_user.email == "newemail@example.com"
        assert retrieved_user.full_name == "Updated Name"
        assert retrieved_user.updated_at is not None
    
    def test_delete_user_flow(self, real_repository, test_session):
        """Prueba eliminación de usuario"""
        # Arrange
        user = User("testuser", "test@example.com", "Test User")
        created_user = real_repository.create(user)
        test_session.commit()
        user_id = created_user.id
        
        # Act
        deleted = real_repository.delete(user_id)
        test_session.commit()
        
        # Assert
        assert deleted is True
        with pytest.raises(UserNotFoundError):
            real_repository.get_by_id(user_id)
    
    def test_get_all_active_users(self, real_repository, test_session):
        """Prueba obtención de usuarios activos"""
        # Arrange - crear usuarios, algunos inactivos
        users_data = [
            ("user1", "user1@example.com", "User 1", True),
            ("user2", "user2@example.com", "User 2", False),
            ("user3", "user3@example.com", "User 3", True)
        ]
        
        for username, email, full_name, is_active in users_data:
            user = User(username, email, full_name)
            if not is_active:
                user.deactivate()
            real_repository.create(user)
        
        test_session.commit()
        
        # Act
        active_users = real_repository.get_all_active()
        
        # Assert
        assert len(active_users) == 2  # Solo los activos
        active_usernames = [u.username for u in active_users]
        assert "user1" in active_usernames
        assert "user3" in active_usernames
        assert "user2" not in active_usernames
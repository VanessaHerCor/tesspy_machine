# ============================================================================
# ARCHIVO 11: tests/integration/test_user_workflow.py (Integration tests completos)
# ============================================================================

"""
Integration tests para workflows completos de usuario
Enfoque: Probar UserService con Repository real (sin mocks)
"""

import pytest
from src.exceptions import UserAlreadyExistsError, InvalidUserDataError

@pytest.mark.integration
class TestUserWorkflowIntegration:
    """Integration tests para workflows completos de usuario"""
    
    def test_complete_user_lifecycle(self, real_user_service, test_session):
        """Prueba ciclo de vida completo: crear, actualizar, desactivar"""
        # 1. Crear usuario
        created_user = real_user_service.create_user(
            username="lifecycle", 
            email="lifecycle@example.com", 
            full_name="Lifecycle User",
            validate_externally=False
        )
        test_session.commit()
        
        assert created_user.username == "lifecycle"
        assert created_user.is_active is True
        user_id = created_user.id
        
        # 2. Actualizar perfil
        updated_user = real_user_service.update_user_profile(
            user_id=user_id,
            email="updated@example.com",
            full_name="Updated User"
        )
        test_session.commit()
        
        assert updated_user.email == "updated@example.com"
        assert updated_user.full_name == "Updated User"
        
        # 3. Desactivar usuario
        deactivated_user = real_user_service.deactivate_user(user_id)
        test_session.commit()
        
        assert deactivated_user.is_active is False
        
        # 4. Reactivar usuario
        reactivated_user = real_user_service.activate_user(user_id)
        test_session.commit()
        
        assert reactivated_user.is_active is True
    
    def test_user_creation_with_business_rules(self, real_user_service, test_session):
        """Prueba creación con reglas de negocio aplicadas"""
        # Crear primer usuario
        user1 = real_user_service.create_user(
            username="user1",
            email="user1@example.com",
            full_name="User One",
            validate_externally=False
        )
        test_session.commit()
        
        # Intentar crear usuario con username duplicado
        with pytest.raises(UserAlreadyExistsError, match="Username 'user1' ya existe"):
            real_user_service.create_user(
                username="user1",  # Duplicado
                email="different@example.com",
                full_name="Different User",
                validate_externally=False
            )
        
        # Intentar crear usuario con email duplicado
        with pytest.raises(UserAlreadyExistsError, match="Email 'user1@example.com' ya existe"):
            real_user_service.create_user(
                username="differentuser",
                email="user1@example.com",  # Duplicado
                full_name="Different User",
                validate_externally=False
            )
    
    def test_user_statistics_integration(self, real_user_service, test_session):
        """Prueba estadísticas con datos reales en BD"""
        # Crear varios usuarios
        users_data = [
            ("alice", "alice@gmail.com", "Alice Smith"),
            ("bob", "bob@company.com", "Bob Johnson"),
            ("charlie", "charlie@gmail.com", "Charlie Brown"),
        ]
        
        for username, email, full_name in users_data:
            real_user_service.create_user(username, email, full_name, validate_externally=False)
        
        test_session.commit()
        
        # Obtener estadísticas
        stats = real_user_service.get_user_statistics()
        
        # Verificar estadísticas
        assert stats['total_active_users'] == 3
        assert stats['total_users'] == 3
        assert stats['users_by_domain']['gmail.com'] == 2
        assert stats['users_by_domain']['company.com'] == 1
    
    def test_update_profile_with_constraints(self, real_user_service, test_session):
        """Prueba actualización de perfil respetando constraints"""
        # Crear dos usuarios
        user1 = real_user_service.create_user("user1", "user1@example.com", "User 1", validate_externally=False)
        user2 = real_user_service.create_user("user2", "user2@example.com", "User 2", validate_externally=False)
        test_session.commit()
        
        # Intentar actualizar user2 con email de user1 (debe fallar)
        with pytest.raises(UserAlreadyExistsError, match="Email 'user1@example.com' ya existe"):
            real_user_service.update_user_profile(
                user_id=user2.id,
                email="user1@example.com"  # Email ya usado por user1
            )
        
        # Actualización válida debe funcionar
        updated_user = real_user_service.update_user_profile(
            user_id=user2.id,
            email="user2_updated@example.com",
            full_name="User 2 Updated"
        )
        test_session.commit()
        
        assert updated_user.email == "user2_updated@example.com"
        assert updated_user.full_name == "User 2 Updated"

@pytest.mark.integration
@pytest.mark.slow
class TestLargeDatasetIntegration:
    """Integration tests con datasets grandes para probar rendimiento"""
    
    def test_bulk_user_creation_performance(self, real_user_service, test_session):
        """Prueba creación masiva de usuarios"""
        # Crear 100 usuarios
        created_users = []
        for i in range(100):
            user = real_user_service.create_user(
                username=f"bulkuser{i}",
                email=f"bulk{i}@example.com",
                full_name=f"Bulk User {i}",
                validate_externally=False
            )
            created_users.append(user)
        
        test_session.commit()
        
        # Verificar que todos se crearon
        assert len(created_users) == 100
        
        # Verificar estadísticas
        stats = real_user_service.get_user_statistics()
        assert stats['total_active_users'] == 100
# ============================================================================
# ARCHIVO 5: src/services.py
# ============================================================================

"""Capa de lógica de negocio - combina repositories y servicios externos"""

from typing import Dict, Any, List, Optional
from .models import User
from .repositories import UserRepository
from .api_client import ExternalUserValidationClient
from .exceptions import InvalidUserDataError, UserAlreadyExistsError, ExternalServiceError

class UserService:
    """
    Servicio de usuarios que combina múltiples componentes
    Perfecto para demostrar la diferencia entre unit e integration testing
    """
    
    def __init__(self, 
                 repository: UserRepository, 
                 validation_client: Optional[ExternalUserValidationClient] = None):
        """Inyección de dependencias"""
        self.repository = repository
        self.validation_client = validation_client
    
    def create_user(self, username: str, email: str, full_name: str, 
                   validate_externally: bool = True) -> User:
        """
        Crea un usuario con validaciones completas
        Esta función coordina múltiples componentes
        """
        # 1. Validación básica usando el modelo (lógica interna)
        try:
            user = User(username=username, email=email, full_name=full_name)
        except ValueError as e:
            raise InvalidUserDataError(f"Datos inválidos: {str(e)}")
        
        # 2. Verificar que no existe (usando repository)
        if self.repository.exists_username(username):
            raise UserAlreadyExistsError(f"Username '{username}' ya existe")
        
        if self.repository.exists_email(email):
            raise UserAlreadyExistsError(f"Email '{email}' ya existe")
        
        # 3. Validación externa opcional (usando API client)
        if validate_externally and self.validation_client:
            try:
                email_validation = self.validation_client.validate_email(email)
                if not email_validation.get('valid', False):
                    raise InvalidUserDataError("Email no válido según servicio externo")
                
                reputation = self.validation_client.check_user_reputation(username, email)
                if reputation.get('blocked', False):
                    raise InvalidUserDataError("Usuario bloqueado por política de seguridad")
                
            except ExternalServiceError:
                # En production, decidir si continuar o fallar
                # Para este ejemplo, continuamos con warning
                pass
        
        # 4. Crear usuario en base de datos
        created_user = self.repository.create(user)
        
        # 5. Notificación externa (no crítica)
        if self.validation_client:
            try:
                self.validation_client.notify_user_created(created_user.to_dict())
            except ExternalServiceError:
                # Notificación no crítica, no fallar
                pass
        
        return created_user
    
    def get_user(self, user_id: int) -> User:
        """Obtiene usuario por ID - simple delegación"""
        return self.repository.get_by_id(user_id)
    
    def update_user_profile(self, user_id: int, email: Optional[str] = None, 
                          full_name: Optional[str] = None) -> User:
        """
        Actualiza perfil de usuario
        Combina lógica de negocio con persistencia
        """
        # Obtener usuario existente
        user = self.repository.get_by_id(user_id)
        
        # Verificar conflictos si se cambia email
        if email and email.lower() != user.email:
            if self.repository.exists_email(email):
                raise UserAlreadyExistsError(f"Email '{email}' ya existe")
        
        # Aplicar cambios usando lógica del modelo
        try:
            user.update_profile(email=email, full_name=full_name)
        except ValueError as e:
            raise InvalidUserDataError(f"Datos inválidos: {str(e)}")
        
        # Persistir cambios
        return self.repository.update(user)
    
    def deactivate_user(self, user_id: int) -> User:
        """Desactiva un usuario"""
        user = self.repository.get_by_id(user_id)
        user.deactivate()
        return self.repository.update(user)
    
    def activate_user(self, user_id: int) -> User:
        """Activa un usuario"""
        user = self.repository.get_by_id(user_id)
        user.activate()
        return self.repository.update(user)
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de usuarios
        Función que coordina múltiples consultas
        """
        active_count = self.repository.count_active_users()
        all_users = self.repository.get_all_active()
        
        return {
            'total_active_users': active_count,
            'total_users': len(all_users) if all_users else 0,
            'users_by_domain': self._group_users_by_email_domain(all_users),
            'recent_registrations': len([u for u in all_users if self._is_recent_user(u)])
        }
    
    def _group_users_by_email_domain(self, users: List[User]) -> Dict[str, int]:
        """Agrupa usuarios por dominio de email - lógica interna"""
        domains = {}
        for user in users:
            domain = user.email.split('@')[1] if '@' in user.email else 'unknown'
            domains[domain] = domains.get(domain, 0) + 1
        return domains
    
    def _is_recent_user(self, user: User) -> bool:
        """Determina si es un usuario reciente - lógica interna"""
        from datetime import datetime, timedelta
        if not user.created_at:
            return False
        return user.created_at > datetime.utcnow() - timedelta(days=30)
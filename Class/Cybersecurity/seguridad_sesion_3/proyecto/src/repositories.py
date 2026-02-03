# ============================================================================
# ARCHIVO 3: src/repositories.py
# ============================================================================

"""Capa de acceso a datos - Repository Pattern"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from .models import User
from .exceptions import UserNotFoundError, UserAlreadyExistsError

class UserRepository:
    """
    Repository para operaciones de base de datos de usuarios
    Esta capa es ideal para integration testing
    """
    
    def __init__(self, session: Session):
        """Inyección de dependencia de sesión de BD"""
        self.session = session
    
    def create(self, user: User) -> User:
        """
        Crea un usuario en la base de datos
        Maneja violaciones de constraints únicos
        """
        try:
            self.session.add(user)
            self.session.flush()  # Flush para obtener ID sin commit
            return user
        except IntegrityError as e:
            self.session.rollback()
            if 'username' in str(e.orig):
                raise UserAlreadyExistsError(f"Username '{user.username}' ya existe")
            elif 'email' in str(e.orig):
                raise UserAlreadyExistsError(f"Email '{user.email}' ya existe")
            else:
                raise UserAlreadyExistsError("Usuario ya existe")
    
    def get_by_id(self, user_id: int) -> User:
        """Obtiene usuario por ID"""
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")
        return user
    
    def get_by_username(self, username: str) -> User:
        """Obtiene usuario por username"""
        user = self.session.query(User).filter(User.username == username.lower()).first()
        if not user:
            raise UserNotFoundError(f"Usuario '{username}' no encontrado")
        return user
    
    def get_by_email(self, email: str) -> User:
        """Obtiene usuario por email"""
        user = self.session.query(User).filter(User.email == email.lower()).first()
        if not user:
            raise UserNotFoundError(f"Usuario con email '{email}' no encontrado")
        return user
    
    def get_all_active(self) -> List[User]:
        """Obtiene todos los usuarios activos"""
        return self.session.query(User).filter(User.is_active == True).all()
    
    def update(self, user: User) -> User:
        """
        Actualiza usuario existente
        Asume que el usuario ya está en la sesión
        """
        try:
            self.session.flush()
            return user
        except IntegrityError as e:
            self.session.rollback()
            raise UserAlreadyExistsError("Conflicto al actualizar usuario")
    
    def delete(self, user_id: int) -> bool:
        """
        Elimina usuario por ID
        Retorna True si se eliminó, False si no existía
        """
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.flush()
            return True
        return False
    
    def exists_username(self, username: str) -> bool:
        """Verifica si existe un username"""
        return self.session.query(User).filter(User.username == username.lower()).count() > 0
    
    def exists_email(self, email: str) -> bool:
        """Verifica si existe un email"""
        return self.session.query(User).filter(User.email == email.lower()).count() > 0
    
    def count_active_users(self) -> int:
        """Cuenta usuarios activos"""
        return self.session.query(User).filter(User.is_active == True).count()
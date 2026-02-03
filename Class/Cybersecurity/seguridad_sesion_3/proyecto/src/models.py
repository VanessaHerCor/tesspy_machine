# ============================================================================
# ARCHIVO 2: src/models.py
# ============================================================================

"""Modelos de datos usando SQLAlchemy"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional

Base = declarative_base()

class User(Base):
    """
    Modelo de usuario con validaciones básicas
    Representa la entidad principal del dominio
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, username: str, email: str, full_name: str):
        """
        Inicializa usuario con validaciones básicas
        Esta lógica es perfecta para unit testing
        """
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.full_name = self._validate_full_name(full_name)
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def _validate_username(self, username: str) -> str:
        """Valida formato de username"""
        if not username or len(username) < 3:
            raise ValueError("Username debe tener al menos 3 caracteres")
        if len(username) > 50:
            raise ValueError("Username no puede exceder 50 caracteres")
        if not username.isalnum():
            raise ValueError("Username solo puede contener letras y números")
        return username.lower()
    
    def _validate_email(self, email: str) -> str:
        """Valida formato básico de email"""
        if not email or '@' not in email:
            raise ValueError("Email debe tener formato válido")
        if len(email) > 100:
            raise ValueError("Email no puede exceder 100 caracteres")
        return email.lower()
    
    def _validate_full_name(self, full_name: str) -> str:
        """Valida nombre completo"""
        if not full_name or len(full_name.strip()) < 2:
            raise ValueError("Nombre completo debe tener al menos 2 caracteres")
        if len(full_name) > 100:
            raise ValueError("Nombre completo no puede exceder 100 caracteres")
        return full_name.strip()
    
    def update_profile(self, email: Optional[str] = None, full_name: Optional[str] = None):
        """
        Actualiza perfil del usuario
        Lógica de negocio que necesita unit testing
        """
        if email is not None:
            self.email = self._validate_email(email)
        if full_name is not None:
            self.full_name = self._validate_full_name(full_name)
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Desactiva el usuario"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self):
        """Activa el usuario"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convierte usuario a diccionario (para APIs)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
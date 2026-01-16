from mongoengine import Document, StringField, DateTimeField, IntField
from datetime import datetime
from hashlib import sha256
import os
import base64


class User(Document):
    """Modelo de Usuario para autenticación JWT - MongoDB"""
    user_id = StringField(required=True, unique=True)  # ID único: user-1, user-2, etc
    username = StringField(unique=True, required=True, max_length=100)
    password_hash = StringField(required=True)  # Hash SHA256 de la contraseña
    role = StringField(choices=['admin', 'manager', 'user'], default='user')
    created_at = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    is_active = StringField(default='true')  # 'true' o 'false' (MongoDB no tiene bool nativo en algunos casos)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'user_id']
    }
    
    def set_password(self, raw_password):
        """Hashear contraseña con SHA256 + salt"""
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')
        password_hash = sha256((salt + raw_password).encode()).hexdigest()
        self.password_hash = f"{salt}${password_hash}"
    
    def check_password(self, raw_password):
        """Verificar contraseña contra hash almacenado"""
        try:
            salt, password_hash = self.password_hash.split('$')
            computed_hash = sha256((salt + raw_password).encode()).hexdigest()
            return computed_hash == password_hash
        except Exception:
            return False
    
    def to_dict(self):
        """Convertir usuario a diccionario (para JSON)"""
        return {
            'id': str(self.user_id),
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_next_user_id(cls):
        """Generar el siguiente user_id automático (user-1, user-2, etc)"""
        count = cls.objects.count()
        return f"user-{count + 1}"
    
    @classmethod
    def initialize_users(cls):
        """Inicializa usuarios por defecto si no existen"""
        if cls.objects.count() == 0:
            # Usuario admin
            admin = cls(user_id='user-1', username='admin1', role='admin')
            admin.set_password('admin123')
            admin.save()
            
            # Usuario manager
            manager = cls(user_id='user-2', username='manager', role='manager')
            manager.set_password('manager123')
            manager.save()
            
            print("✅ Usuarios iniciales creados en MongoDB")
    
    def __str__(self):
        return f"{self.username} ({self.role})"

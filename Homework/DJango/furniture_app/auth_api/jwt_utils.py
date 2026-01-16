"""Utilidades para manejar JWT con PyJWT"""
import jwt
import json
from datetime import datetime, timedelta
from django.conf import settings

# Clave secreta para firmar tokens (usa SECRET_KEY de Django)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

# Tiempos de expiración
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id, username, role, expires_delta=None):
    """Crear JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': expire,
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(user_id, expires_delta=None):
    """Crear JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        'user_id': user_id,
        'exp': expire,
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    """Verificar y decodificar JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expirado'}
    except jwt.InvalidTokenError:
        return {'error': 'Token inválido'}
    except Exception as e:
        return {'error': str(e)}


def decode_token(token):
    """Decodificar token sin verificar firma (para debugging)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        return payload
    except Exception as e:
        return {'error': str(e)}

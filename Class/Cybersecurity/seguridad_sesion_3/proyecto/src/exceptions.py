# ============================================================================
# ARCHIVO 1: src/exceptions.py
# ============================================================================

"""Excepciones personalizadas del dominio"""

class UserServiceError(Exception):
    """Excepción base para errores del servicio de usuarios"""
    pass

class UserNotFoundError(UserServiceError):
    """Usuario no encontrado"""
    pass

class UserAlreadyExistsError(UserServiceError):
    """Usuario ya existe"""
    pass

class InvalidUserDataError(UserServiceError):
    """Datos de usuario inválidos"""
    pass

class ExternalServiceError(UserServiceError):
    """Error en servicio externo"""
    pass
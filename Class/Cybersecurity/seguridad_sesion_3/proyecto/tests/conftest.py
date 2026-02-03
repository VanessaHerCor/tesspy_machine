# ============================================================================
# ARCHIVO 6: tests/conftest.py (Fixtures compartidas)
# ============================================================================

"""Fixtures compartidas para todos los tipos de pruebas"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import Mock

from src.models import Base, User
from src.repositories import UserRepository
from src.services import UserService
from src.api_client import ExternalUserValidationClient

# ===== FIXTURES PARA UNIT TESTS (Mocks) =====

@pytest.fixture
def mock_repository():
    """Mock de UserRepository para unit tests"""
    return Mock(spec=UserRepository)

@pytest.fixture
def mock_api_client():
    """Mock de ExternalUserValidationClient para unit tests"""
    return Mock(spec=ExternalUserValidationClient)

@pytest.fixture
def user_service_with_mocks(mock_repository, mock_api_client):
    """UserService con dependencias mockeadas para unit tests"""
    return UserService(repository=mock_repository, validation_client=mock_api_client)

# ===== FIXTURES PARA INTEGRATION TESTS (Base de datos real) =====

@pytest.fixture(scope="function")
def test_engine():
    """
    Engine de SQLite en memoria para cada test
    Scope function = nueva BD para cada prueba
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def test_session(test_engine):
    """
    Sesión de BD con rollback automático
    Garantiza aislamiento entre pruebas
    """
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    
    yield session
    
    session.rollback()
    session.close()

@pytest.fixture
def real_repository(test_session):
    """Repository real para integration tests"""
    return UserRepository(test_session)

@pytest.fixture
def real_user_service(real_repository):
    """UserService con repository real pero sin API client"""
    return UserService(repository=real_repository, validation_client=None)

# ===== FIXTURES DE DATOS DE PRUEBA =====

@pytest.fixture
def sample_user_data():
    """Datos válidos para crear usuario"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'full_name': 'Test User'
    }

@pytest.fixture
def sample_user_model(sample_user_data):
    """Instancia de User para pruebas"""
    return User(**sample_user_data)

@pytest.fixture
def users_in_db(real_repository, test_session):
    """
    Fixture que crea varios usuarios en la BD de prueba
    Útil para integration tests que necesitan datos existentes
    """
    users_data = [
        {'username': 'alice', 'email': 'alice@example.com', 'full_name': 'Alice Smith'},
        {'username': 'bob', 'email': 'bob@test.com', 'full_name': 'Bob Johnson'},
        {'username': 'charlie', 'email': 'charlie@demo.org', 'full_name': 'Charlie Brown'}
    ]
    
    created_users = []
    for data in users_data:
        user = User(**data)
        created_user = real_repository.create(user)
        test_session.commit()  # Commit cada usuario
        created_users.append(created_user)
    
    return created_users
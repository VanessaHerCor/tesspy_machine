from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .jwt_utils import create_access_token, create_refresh_token, verify_token


@api_view(['POST'])
def login(request):
    """
    🔐 Endpoint de Login - Obtener JWT Tokens
    POST /api/auth/login/
    
    Body:
    {
        "username": "admin1",
        "password": "admin123"
    }
    
    Respuesta:
    {
        "message": "Login exitoso",
        "access_token": "eyJ...",
        "refresh_token": "eyJ...",
        "user": {
            "id": "user-1",
            "username": "admin1",
            "role": "admin"
        }
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Crear tokens
        access_token = create_access_token(
            user_id=str(user.user_id),
            username=user.username,
            role=user.role
        )
        refresh_token = create_refresh_token(user_id=str(user.user_id))
        
        # Actualizar último login
        user.last_login = __import__('datetime').datetime.now()
        user.save()
        
        return Response({
            'message': 'Login exitoso',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Credenciales inválidas',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    """
    📝 Endpoint de Registro - Crear Nuevo Usuario
    POST /api/auth/register/
    
    Body:
    {
        "username": "nuevo_usuario",
        "password": "password123",
        "role": "user"  // opcional: admin, manager, user
    }
    
    Respuesta:
    {
        "message": "Usuario creado exitosamente",
        "user": {
            "id": "user-3",
            "username": "nuevo_usuario",
            "role": "user",
            "created_at": "2026-01-12T..."
        }
    }
    """
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Usuario creado exitosamente',
            'user': user.to_dict()
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Error al crear usuario',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_access_token(request):
    """
    🔄 Endpoint para Refrescar Access Token
    POST /api/auth/refresh/
    
    Body:
    {
        "refresh_token": "eyJ..."
    }
    
    Respuesta:
    {
        "access_token": "eyJ...",
        "message": "Token refrescado"
    }
    """
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({
            'error': 'Token de refresco requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    payload = verify_token(refresh_token)
    
    if 'error' in payload:
        return Response({
            'error': payload['error']
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if payload.get('type') != 'refresh':
        return Response({
            'error': 'Token inválido (debe ser refresh token)'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Obtener usuario y crear nuevo access token
    user_id = payload.get('user_id')
    user = User.objects(user_id=user_id).first()
    
    if not user:
        return Response({
            'error': 'Usuario no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    new_access_token = create_access_token(
        user_id=str(user.user_id),
        username=user.username,
        role=user.role
    )
    
    return Response({
        'access_token': new_access_token,
        'message': 'Token refrescado'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_jwt_token(request):
    """
    ✅ Endpoint para Verificar Token
    POST /api/auth/verify/
    
    Body:
    {
        "token": "eyJ..."
    }
    
    Respuesta:
    {
        "valid": true,
        "user_id": "user-1",
        "username": "admin1",
        "role": "admin"
    }
    """
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Token requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    payload = verify_token(token)
    
    if 'error' in payload:
        return Response({
            'valid': False,
            'error': payload['error']
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'valid': True,
        'user_id': payload.get('user_id'),
        'username': payload.get('username'),
        'role': payload.get('role'),
        'type': payload.get('type')
    }, status=status.HTTP_200_OK)

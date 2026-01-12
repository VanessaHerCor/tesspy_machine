from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    """Serializador para conversión User ↔ JSON"""
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=['admin', 'manager', 'user'],
        default='user',
        required=False
    )
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Crear nuevo usuario"""
        username = validated_data.get('username')
        password = validated_data.get('password')
        role = validated_data.get('role', 'user')
        
        # Verificar que el usuario no exista
        if User.objects(username=username).first():
            raise serializers.ValidationError({'username': 'Este usuario ya existe'})
        
        # Crear usuario con ID automático
        user = User(
            user_id=User.get_next_user_id(),
            username=username,
            role=role
        )
        user.set_password(password)
        user.save()
        return user
    
    def to_representation(self, instance):
        """Representación en JSON (sin contraseña)"""
        return {
            'id': str(instance.user_id),
            'username': instance.username,
            'role': instance.role,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }


class LoginSerializer(serializers.Serializer):
    """Serializador para login"""
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validar credenciales"""
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects(username=username).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Usuario o contraseña incorrectos')
        
        data['user'] = user
        return data

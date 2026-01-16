from rest_framework import serializers
from .models import Videogame

class VideogameSerializer(serializers.Serializer):
    """Serializador para convertir documentos Videogame a JSON"""
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    genre = serializers.CharField()
    score = serializers.IntegerField()
    main_platform = serializers.CharField(max_length=100)
    coop = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    description = serializers.CharField(required=False, allow_blank=True)
    developer = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    def create(self, validated_data):
        """Crear un nuevo videojuego"""
        return Videogame.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Actualizar un videojuego existente"""
        instance.title = validated_data.get('title', instance.title)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.score = validated_data.get('score', instance.score)
        instance.main_platform = validated_data.get('main_platform', instance.main_platform)
        instance.coop = validated_data.get('coop', instance.coop)
        instance.description = validated_data.get('description', instance.description)
        instance.developer = validated_data.get('developer', instance.developer)
        instance.save()
        return instance

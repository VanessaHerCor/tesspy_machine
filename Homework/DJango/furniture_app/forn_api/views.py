from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dynamicpages.models import Videogame
from dynamicpages.serializers import VideogameSerializer


@api_view(['GET'])
def lista_videojuegos(request):
    """
    🎮 API REST - Lista todos los videojuegos
    GET /api/videogames/ → Lista todos en JSON
    """
    videojuegos = Videogame.objects.all().order_by('-score')
    serializer = VideogameSerializer(videojuegos, many=True)
    
    return Response({
        'count': videojuegos.count(),
        'results': serializer.data
    })


@api_view(['POST'])
def crear_videojuego(request):
    """
    🎮 API REST - Crear nuevo videojuego
    POST /api/videogames/create/ → Crear desde JSON
    """
    serializer = VideogameSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_videojuego(request, pk):
    """
    🎮 API REST - Operaciones sobre un videojuego específico
    GET /api/videogames/{id}/ → Obtener detalles
    PUT /api/videogames/{id}/ → Actualizar
    DELETE /api/videogames/{id}/ → Eliminar
    """
    try:
        videojuego = Videogame.objects.get(pk=pk)
    except Videogame.DoesNotExist:
        return Response(
            {'error': 'Videojuego no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = VideogameSerializer(videojuego)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = VideogameSerializer(videojuego, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        videojuego.delete()
        return Response(
            {'message': 'Videojuego eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
def estadisticas_videojuegos(request):
    """
    📊 Endpoint personalizado - Estadísticas del catálogo
    GET /api/videogames/stats/ → Retorna estadísticas
    """
    total = Videogame.objects.count()
    
    # Obtener el videojuego con mayor puntuación
    mejor_juego = Videogame.objects.order_by('-score').first()
    
    # Obtener el más reciente
    mas_reciente = Videogame.objects.order_by('-created_at').first()
    
    # Contar juegos con coop
    con_coop = Videogame.objects.filter(coop=True).count()
    
    stats = {
        'total_videojuegos': total,
        'juegos_con_coop': con_coop,
        'mejor_juego': {
            'titulo': mejor_juego.title,
            'puntuacion': mejor_juego.score,
            'plataforma': mejor_juego.main_platform
        } if mejor_juego else None,
        'mas_reciente': {
            'titulo': mas_reciente.title,
            'fecha': mas_reciente.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'genero': mas_reciente.genre
        } if mas_reciente else None,
    }
    
    return Response(stats)

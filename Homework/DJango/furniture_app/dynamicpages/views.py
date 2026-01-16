from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Videogame
from .serializers import VideogameSerializer
from bson import ObjectId

# ==================== VISTAS CON TEMPLATES ====================

def videogames_list(request):
    """Vista que consulta MongoDB y pasa datos al template"""
    # MongoEngine usa la misma sintaxis de consulta que Django ORM
    videogames = Videogame.objects.all().order_by('-score')
    
    # El contexto son los datos que se pasan al template
    context = {
        'videogames': videogames,
        'page_title': 'Catálogo de Videojuegos'
    }

    # render() combina el template con el contexto
    return render(request, 'dynamicpages/videogames_list.html', context)


def videogame_detail(request, id):
    """Vista que muestra un videojuego específico desde MongoDB"""
    try:
        videogame = Videogame.objects.get(id=ObjectId(id))
        context = {
            'videogame': videogame
        }
        return render(request, 'dynamicpages/videogame_detail.html', context)
    except Videogame.DoesNotExist:
        return HttpResponse("<h1>❌ Videojuego no encontrado</h1>", status=404)
    except Exception as e:
        return HttpResponse(f"<h1>Error</h1><p>{str(e)}</p>", status=500)


def create_videogame(request):
    """View to handle videogame creation via form submission"""
    if request.method == 'POST':
        try:
            # Create and save the videogame to MongoDB
            videogame = Videogame(
                title=request.POST.get('title'),
                genre=request.POST.get('genre'),
                score=int(request.POST.get('score')),
                main_platform=request.POST.get('main_platform'),
                coop=request.POST.get('coop') == 'on',
                developer=request.POST.get('developer', ''),
                description=request.POST.get('description', '')
            )
            videogame.save()
            messages.success(request, f'✅ "{videogame.title}" created successfully in MongoDB!')
            return redirect('videogames_list')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
            return render(request, 'dynamicpages/create_videogame.html')
    
    return render(request, 'dynamicpages/create_videogame.html')


# ==================== REST API JSON ====================

@api_view(['GET', 'POST'])
def api_videogames_list(request):
    """API REST - Lista todos los videojuegos en JSON"""
    if request.method == 'GET':
        videogames = Videogame.objects.all()
        serializer = VideogameSerializer(videogames, many=True)
        return Response({
            'status': 'success',
            'total': len(videogames),
            'data': serializer.data
        })
    
    elif request.method == 'POST':
        serializer = VideogameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Videojuego creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_videogame_detail(request, id):
    """API REST - Obtener, actualizar o eliminar un videojuego específico"""
    try:
        game = Videogame.objects.get(id=ObjectId(id))
    except Videogame.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Videojuego no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VideogameSerializer(game)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        serializer = VideogameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Videojuego actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        game.delete()
        return Response({
            'status': 'success',
            'message': 'Videojuego eliminado exitosamente'
        })

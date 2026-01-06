from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def get_videogame(request,id):
    videogames = [
        {"id": 1, "title": "The Legend of Zelda: Breath of the Wild", "platform": "Nintendo Switch"},
        {"id": 2, "title": "God of War", "platform": "PlayStation 4"},
        {"id": 3, "title": "Halo Infinite", "platform": "Xbox Series X"},
    ]
    print(f"Requested videogame ID: {id}")
    return JsonResponse(videogames, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_videogame(request):
    body=request
    return JsonResponse(body, safe=False, status=status.HTTP_201_CREATED)
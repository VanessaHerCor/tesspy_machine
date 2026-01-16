from django.urls import path
from . import views

urlpatterns = [
    # Vistas HTML con Templates
    path('', views.videogames_list, name='videogames_list'),
    path('create/', views.create_videogame, name='create_videogame'),
    path('videogame/<str:id>/', views.videogame_detail, name='videogame_detail'),
    
    # API REST JSON
    path('api/videogames/', views.api_videogames_list, name='api_videogames_list'),
    path('api/videogames/<str:id>/', views.api_videogame_detail, name='api_videogame_detail'),
]

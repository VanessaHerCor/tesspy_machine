"""
URL configuration for furniture_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    # 📊 Endpoint de estadísticas
    path('stats/', views.estadisticas_videojuegos, name='api_estadisticas'),  # GET /api/videogames/stats/
    
    # 🎮 Crear nuevo
    path('create/', views.crear_videojuego, name='api_crear_videojuego'),  # POST /api/videogames/create/
    
    # 🎮 Operaciones sobre lista de videojuegos
    path('', views.lista_videojuegos, name='api_lista_videojuegos'),  # GET /api/videogames/
    
    # 🎮 Operaciones sobre un videojuego específico
    path('<str:pk>/', views.detalle_videojuego, name='api_detalle_videojuego'),  # GET/PUT/DELETE
]

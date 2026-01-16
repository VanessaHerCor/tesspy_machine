from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Autenticación
    path('login/', views.login, name='auth_login'),           # POST /api/auth/login/
    path('register/', views.register, name='auth_register'),   # POST /api/auth/register/
    path('refresh/', views.refresh_access_token, name='auth_refresh'),  # POST /api/auth/refresh/
    path('verify/', views.verify_jwt_token, name='auth_verify'),  # POST /api/auth/verify/
]

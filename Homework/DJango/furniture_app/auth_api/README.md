# 🔐 AUTH_API - Autenticación con JWT

Módulo de autenticación y autorización basado en **JWT (JSON Web Tokens)** con MongoDB. Gestiona login, registro, renovación de tokens y verificación de identidad.

---

## 📋 Tabla de Contenidos

- [Estructura](#estructura)
- [Instalación y Configuración](#instalación-y-configuración)
- [Modelos](#modelos)
- [Endpoints](#endpoints)
- [JWT Tokens](#jwt-tokens)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 📁 Estructura

```
auth_api/
├── __init__.py          # Configuración del app
├── apps.py              # Definición de la app
├── admin.py             # Admin de Django (no usado con MongoDB)
├── models.py            # Modelo User (MongoEngine)
├── serializers.py       # Validación de datos (DRF)
├── views.py             # Endpoints de la API
├── urls.py              # Rutas de la API
├── jwt_utils.py         # Utilidades para JWT
├── management/          # Commands personalizados
├── __pycache__/         # Cache de Python
└── README.md            # Este archivo
```

---

## ⚙️ Instalación y Configuración

### 1. Verificar que esté instalado en `INSTALLED_APPS`

En [furniture_app/settings.py](../furniture_app/settings.py):

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'auth_api',
]
```

### 2. Inicializar usuarios predeterminados

```bash
python manage.py shell

>>> from auth_api.models import User
>>> User.initialize_users()
✅ Usuarios iniciales creados en MongoDB
```

Esto crea:
- **admin1** / **admin123** (rol: admin)
- **manager** / **manager123** (rol: manager)

---

## 👤 Modelos

### User

```python
class User(Document):
    user_id          # StringField - ID único (user-1, user-2, etc)
    username         # StringField - Nombre de usuario único
    password_hash    # StringField - Hash SHA256 + salt
    role             # StringField - admin, manager, o user
    created_at       # DateTimeField - Fecha de creación
    last_login       # DateTimeField - Último login
    is_active        # StringField - 'true' o 'false'
```

#### Métodos Principales

```python
user.set_password(raw_password)      # Hashear contraseña
user.check_password(raw_password)    # Verificar contraseña
user.to_dict()                       # Convertir a diccionario JSON
User.get_next_user_id()              # Generar ID automático
User.initialize_users()              # Crear usuarios por defecto
```

---

## 🔌 Endpoints

### 1. **LOGIN** - Obtener JWT Tokens
```
POST /api/auth/login/
```

**Body:**
```json
{
    "username": "admin1",
    "password": "admin123"
}
```

**Respuesta (200 OK):**
```json
{
    "message": "Login exitoso",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": "user-1",
        "username": "admin1",
        "role": "admin",
        "created_at": "2026-01-12T10:30:00"
    }
}
```

**Errores:**
- `400 BAD REQUEST` - Credenciales inválidas
- `400 BAD REQUEST` - Datos incompletos

---

### 2. **REGISTER** - Crear Nuevo Usuario
```
POST /api/auth/register/
```

**Body:**
```json
{
    "username": "nuevo_usuario",
    "password": "password123",
    "role": "user"
}
```

**Respuesta (201 CREATED):**
```json
{
    "message": "Usuario creado exitosamente",
    "user": {
        "id": "user-3",
        "username": "nuevo_usuario",
        "role": "user",
        "created_at": "2026-01-12T11:45:00"
    }
}
```

**Errores:**
- `400 BAD REQUEST` - Usuario ya existe
- `400 BAD REQUEST` - Datos incompletos

---

### 3. **REFRESH TOKEN** - Renovar Access Token
```
POST /api/auth/refresh/
```

**Body:**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200 OK):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Token refrescado"
}
```

**Errores:**
- `400 BAD REQUEST` - Refresh token no proporcionado
- `401 UNAUTHORIZED` - Token expirado o inválido
- `404 NOT FOUND` - Usuario no encontrado

---

### 4. **VERIFY TOKEN** - Verificar Validez del Token
```
POST /api/auth/verify/
```

**Body:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200 OK):**
```json
{
    "valid": true,
    "user_id": "user-1",
    "username": "admin1",
    "role": "admin",
    "type": "access"
}
```

**Errores:**
- `400 BAD REQUEST` - Token no proporcionado
- `401 UNAUTHORIZED` - Token expirado o inválido

---

## 🎫 JWT Tokens

### Access Token
- **Duración:** 30 minutos
- **Tipo:** `access`
- **Contenido:**
  ```python
  {
      'user_id': 'user-1',
      'username': 'admin1',
      'role': 'admin',
      'exp': <timestamp>,
      'iat': <timestamp>,
      'type': 'access'
  }
  ```

### Refresh Token
- **Duración:** 7 días
- **Tipo:** `refresh`
- **Contenido:**
  ```python
  {
      'user_id': 'user-1',
      'exp': <timestamp>,
      'iat': <timestamp>,
      'type': 'refresh'
  }
  ```

### Configuración
En [jwt_utils.py](jwt_utils.py):
```python
SECRET_KEY = settings.SECRET_KEY              # De Django settings
ALGORITHM = 'HS256'                           # Algoritmo de firma
ACCESS_TOKEN_EXPIRE_MINUTES = 30              # Duración access token
REFRESH_TOKEN_EXPIRE_DAYS = 7                 # Duración refresh token
```

---

## 💡 Ejemplos de Uso

### Usando cURL

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin1", "password": "admin123"}'

# 2. Refrescar token
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'

# 3. Verificar token
curl -X POST http://localhost:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_ACCESS_TOKEN"}'

# 4. Registrar usuario
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "nuevo_user", "password": "pass123", "role": "user"}'
```

### Usando Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/auth"

# 1. Login
response = requests.post(f"{BASE_URL}/login/", json={
    "username": "admin1",
    "password": "admin123"
})
tokens = response.json()
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

# 2. Usar access token en headers
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 3. Refrescar token cuando expire
new_tokens = requests.post(f"{BASE_URL}/refresh/", json={
    "refresh_token": refresh_token
})
```

### Usando Postman

1. **Crear colección** "Auth_API"
2. **Login request:**
   - Método: POST
   - URL: `http://localhost:8000/api/auth/login/`
   - Body (JSON):
     ```json
     {"username": "admin1", "password": "admin123"}
     ```
3. **Guardar tokens** en variables de entorno:
   - `{{access_token}}` - Usar en headers Authorization
   - `{{refresh_token}}` - Usar para refrescar

---

## 🔒 Seguridad

### Prácticas Implementadas

✅ **Hash SHA256 + Salt** - Contraseñas hasheadas con salt aleatorio
✅ **JWT Firmado** - Tokens firmados con SECRET_KEY de Django
✅ **Expiración de Tokens** - Access token: 30 min, Refresh token: 7 días
✅ **Tipos de Token** - Distintos tipos para access y refresh
✅ **Verificación de Credenciales** - Validación estricta en login

### Mejoras Futuras

- [ ] Rate limiting en endpoints de login
- [ ] Blacklist de tokens revocados
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 / Social login
- [ ] CORS configuration

---

## 📝 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| [models.py](models.py) | Definición del modelo User (MongoDB) |
| [serializers.py](serializers.py) | Validación y conversión JSON ↔ Python |
| [views.py](views.py) | Lógica de endpoints |
| [urls.py](urls.py) | Rutas de la API |
| [jwt_utils.py](jwt_utils.py) | Funciones para crear y verificar JWT |

---

## 🚀 Próximos Pasos

Este módulo es utilizado por:
- [dynamicpages](../dynamicpages/) - Para páginas dinámicas con autenticación
- [forn_api](../forn_api/) - Para formularios protegidos
- [staticpages](../staticpages/) - Para renderizar con usuario autenticado

---

**Última actualización:** 12 enero 2026

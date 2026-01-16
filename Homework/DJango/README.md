# 🎮 Furniture App - Videogames Database Platform

**Plataforma completa de base de datos de videojuegos** construida con **Django 6.0**, **MongoDB**, y **Django REST Framework**. Sistema educativo que demuestra autenticación JWT, vistas dinámicas, API REST, y páginas estáticas en un proyecto Django integrado.

---

## 🎯 Visión General

Este proyecto está organizado en **4 módulos independientes pero interconectados**, cada uno con una responsabilidad específica:

```
┌────────────────────────────────────────────────────┐
│         FURNITURE APP - Video Games Platform       │
├────────────────────────────────────────────────────┤
│                                                    │
│  1️⃣ STATICPAGES          2️⃣ DYNAMICPAGES         │
│     (Páginas HTML)       (Catálogo Dinámico)     │
│     Landing Pages        + Templates             │
│     + Info Estática      + MongoDB Integration   │
│                                                    │
│  3️⃣ FORN_API            4️⃣ AUTH_API             │
│     (REST API Pura)      (Autenticación)         │
│     CRUD + Estadísticas  JWT Tokens              │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
DJango/
├── README.md                           # 📄 Este archivo - Guía general
│
├── img_sesions/                        # 🖼️ Imágenes de ejemplos
│   ├── sesion_staticpages/             # Imágenes de STATICPAGES
│   ├── sesion_dynamicpages/            # Imágenes de DYNAMICPAGES
│   ├── sesion_forn_api/                # Imágenes de FORN_API
│   └── sesion_auth_login/              # Imágenes de AUTH_API
│
└── furniture_app/                      # 🏠 Proyecto Django principal
    ├── README.md                       # Guía detallada de módulos
    ├── manage.py                       # 🛠️ Script de gestión de Django
    ├── create_games.py                 # 📝 Script para inicializar datos
    ├── db.sqlite3                      # 🗄️ BD SQLite
    │
    ├── furniture_app/                  # 🏠 Configuración principal
    │   ├── settings.py                 # ⚙️ Configuración
    │   ├── urls.py                     # 🔗 URLs routing principal
    │   ├── wsgi.py                     # 🌐 WSGI
    │   ├── asgi.py                     # ⚡ ASGI
    │   └── __init__.py
    │
    ├── staticpages/                    # 📄 MÓDULO 1: Páginas Estáticas
    │   ├── README.md                   # 📖 Documentación
    │   ├── views.py                    # home, about, contact
    │   ├── urls.py                     # Rutas: /static-pages/*
    │   ├── models.py
    │   ├── admin.py
    │   ├── apps.py
    │   └── __init__.py
    │
    ├── dynamicpages/                   # 🎮 MÓDULO 2: Catálogo Dinámico
    │   ├── README.md                   # 📖 Documentación
    │   ├── views.py                    # HTML + API REST
    │   ├── urls.py                     # Rutas: /dynamic/*
    │   ├── models.py                   # Videogame (MongoDB)
    │   ├── serializers.py              # VideogameSerializer
    │   ├── templates/dynamicpages/
    │   ├── admin.py
    │   ├── apps.py
    │   └── __init__.py
    │
    ├── forn_api/                       # 📝 MÓDULO 3: REST API Avanzada
    │   ├── README.md                   # 📖 Documentación
    │   ├── views.py                    # 5 endpoints + estadísticas
    │   ├── urls.py                     # Rutas: /api/videogames/*
    │   ├── models.py
    │   ├── admin.py
    │   ├── apps.py
    │   └── __init__.py
    │
    └── auth_api/                       # 🔐 MÓDULO 4: Autenticación JWT
        ├── README.md                   # 📖 Documentación
        ├── views.py                    # login, register, refresh, verify
        ├── urls.py                     # Rutas: /api/auth/*
        ├── models.py                   # User (MongoDB)
        ├── serializers.py              # UserSerializer
        ├── jwt_utils.py                # Funciones JWT
        ├── management/
        ├── admin.py
        ├── apps.py
        └── __init__.py
```

---

## 🚀 Módulos en Detalle

### 📄 **STATICPAGES** - Páginas Estáticas (Módulo 1)

**Propósito:** Proporcionar landing pages e información general sin lógica compleja.

| Característica | Detalles |
|---|---|
| **Rutas** | `/static-pages/`, `/static-pages/about/`, `/static-pages/contact/` |
| **Vistas** | `home()`, `about()`, `contact()` |
| **Base de Datos** | ❌ No usa |
| **Salida** | HTML estático |
| **Templates** | ❌ HTML en vistas |

[📖 Documentación Completa](furniture_app/staticpages/README.md)

---

### 🎮 **DYNAMICPAGES** - Catálogo Dinámico (Módulo 2)

**Propósito:** Mostrar catálogo de videojuegos con datos en tiempo real de MongoDB + API JSON.

| Característica | Detalles |
|---|---|
| **Rutas** | `/dynamic/*` |
| **Vistas** | 3 HTML + 2 API |
| **Base de Datos** | ✅ MongoDB (Videogame) |
| **Salida** | HTML + JSON |
| **Templates** | ✅ Django Templates |

[📖 Documentación Completa](furniture_app/dynamicpages/README.md)

---

### 📝 **FORN_API** - API REST Avanzada (Módulo 3)

**Propósito:** Proporcionar API REST pura para aplicaciones móviles y SPAs + estadísticas.

| Característica | Detalles |
|---|---|
| **Rutas** | `/api/videogames/*` |
| **Endpoints** | 5 CRUD + estadísticas |
| **Base de Datos** | ✅ MongoDB (Videogame) |
| **Salida** | JSON únicamente |
| **Templates** | ❌ No usa |

[📖 Documentación Completa](furniture_app/forn_api/README.md)

---

### 🔐 **AUTH_API** - Autenticación JWT (Módulo 4)

**Propósito:** Gestionar autenticación con JWT tokens y roles de usuario.

| Característica | Detalles |
|---|---|
| **Rutas** | `/api/auth/*` |
| **Endpoints** | 4 (login, register, refresh, verify) |
| **Base de Datos** | ✅ MongoDB (User) |
| **Salida** | JSON |
| **Seguridad** | ✅ JWT + SHA256 Hash |

[📖 Documentación Completa](furniture_app/auth_api/README.md)

---

## 🔗 Flujo de Datos y Navegación

```
USUARIO ACCEDE A LA APP
│
├─→ /static-pages/                    [STATICPAGES]
│   └─→ Landing page con navegación
│
├─→ /dynamic/                          [DYNAMICPAGES]
│   └─→ Catálogo de videojuegos
│
├─→ /api/videogames/*                  [FORN_API]
│   └─→ API REST con estadísticas
│
└─→ /api/auth/*                        [AUTH_API]
    └─→ Autenticación JWT
```

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

```
Frontend
├── HTML5 + CSS3
└── JavaScript

Backend
├── Django 6.0
├── Django REST Framework
├── MongoEngine (ODM)
└── PyJWT

Base de Datos
├── MongoDB (Videogame, User)
└── SQLite (Django interno)
```

---

## 📊 Comparativa de Módulos

| Aspecto | STATIC | DYNAMIC | FORN_API | AUTH_API |
|--------|--------|---------|----------|----------|
| **BD** | ❌ | ✅ MongoDB | ✅ MongoDB | ✅ MongoDB |
| **HTML** | ✅ | ✅ Templates | ❌ | ❌ |
| **JSON** | ❌ | ✅ API | ✅ Pura | ✅ Pura |
| **CRUD** | ❌ | ✅ Parcial | ✅ Completo | ✅ User |
| **Casos de Uso** | Landing | Web | Apps/SPA | Seguridad |

---

## 🛠️ Instalación y Configuración

### 1. Entorno Virtual

```bash
# Crear entorno virtual
python -m venv django_env

# Activar
django_env\Scripts\activate  # Windows
source django_env/bin/activate  # Linux/Mac
```

### 2. Dependencias

```bash
pip install django djangorestframework mongoengine pyjwt
```

### 3. MongoDB

Asegurate que MongoDB esté ejecutándose en `localhost:27017`

### 4. Inicializar Usuarios (Auth_api)

```bash
cd furniture_app
python manage.py shell
>>> from auth_api.models import User
>>> User.initialize_users()
```

### 5. Ejecutar Servidor

```bash
cd furniture_app
python manage.py runserver
# Servidor en http://localhost:8000
```

---

## 🎯 Ejemplos de Uso

### Via Navegador

```
http://localhost:8000/static-pages/
http://localhost:8000/dynamic/
http://localhost:8000/api/videogames/
http://localhost:8000/api/auth/login/
```

### Via cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin1", "password": "admin123"}'

# Listar videojuegos
curl -X GET http://localhost:8000/api/videogames/
```

### Via Python

```python
import requests

response = requests.get('http://localhost:8000/api/videogames/')
games = response.json()
```

---

## 📚 Documentación Detallada

| Módulo | README |
|--------|--------|
| **STATICPAGES** | [staticpages/README.md](furniture_app/staticpages/README.md) |
| **DYNAMICPAGES** | [dynamicpages/README.md](furniture_app/dynamicpages/README.md) |
| **FORN_API** | [forn_api/README.md](furniture_app/forn_api/README.md) |
| **AUTH_API** | [auth_api/README.md](furniture_app/auth_api/README.md) |

---

## 🖼️ Imágenes y Ejemplos

La carpeta `img_sesions/` contiene imágenes de ejemplos para cada módulo:

- `sesion_staticpages/` - Ejemplos visuales de STATICPAGES
- `sesion_dynamicpages/` - Ejemplos visuales de DYNAMICPAGES
- `sesion_forn_api/` - Ejemplos visuales de FORN_API
- `sesion_auth_login/` - Ejemplos visuales de AUTH_API

---

## 🔐 Seguridad

✅ Hashing SHA256 + Salt
✅ JWT Firmado
✅ Validación de Datos
✅ Expiración de Tokens
✅ Roles de Usuario

---

## 🚀 Mejoras Futuras

- [ ] Búsqueda y filtros avanzados
- [ ] Paginación
- [ ] Caché con Redis
- [ ] Sistema de comentarios
- [ ] Wishlist de usuarios
- [ ] OAuth social
- [ ] Tests automatizados
- [ ] Documentación Swagger/OpenAPI
- [ ] Despliegue en Heroku/AWS

---

**Última actualización:** 12 enero 2026
**Versión:** 1.0
**Estado:** Producción-ready

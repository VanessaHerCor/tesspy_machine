# 🎮 DYNAMICPAGES - Páginas Dinámicas con Templates y REST API

Módulo que implementa **vistas HTML dinámicas con templates Django** y **REST API JSON** para gestionar una base de datos de videojuegos en MongoDB. Demuestra la integración entre templates, MongoEngine y Django REST Framework.

---

## 📋 Tabla de Contenidos

- [Estructura](#estructura)
- [Modelos](#modelos)
- [Vistas HTML (Templates)](#vistas-html-templates)
- [REST API JSON](#rest-api-json)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Templates](#templates)

---

## 📁 Estructura

```
dynamicpages/
├── __init__.py              # Configuración del app
├── apps.py                  # Definición de la app
├── admin.py                 # Admin de Django
├── models.py                # Modelo Videogame (MongoEngine)
├── serializers.py           # Validación de datos (DRF)
├── views.py                 # Vistas HTML y API
├── urls.py                  # Rutas de la app
├── tests.py                 # Tests unitarios
├── templates/
│   └── dynamicpages/
│       ├── base.html                # Template base (herencia)
│       ├── videogames_list.html     # Listado de videojuegos
│       ├── videogame_detail.html    # Detalle de videojuego
│       └── create_videogame.html    # Formulario de creación
├── __pycache__/
└── README.md                # Este archivo
```

---

## 👾 Modelos

### Videogame

```python
class Videogame(Document):
    title               # StringField - Título del juego
    genre               # StringField - Género (RPG, FPS, etc)
    score               # IntField - Puntuación (0-100)
    main_platform       # StringField - Plataforma principal
    coop                # BooleanField - Soporte cooperativo
    created_at          # DateTimeField - Fecha de creación
    description         # StringField - Descripción detallada
    developer           # StringField - Desarrollador del juego
```

#### Métodos

```python
videogame.get_rating_stars()    # Convierte score a estrellas (0-5)
```

#### Ejemplo de Documento en MongoDB

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "title": "The Legend of Zelda: Breath of the Wild",
    "genre": "Action-Adventure",
    "score": 97,
    "main_platform": "Nintendo Switch",
    "coop": false,
    "created_at": ISODate("2026-01-12T10:00:00Z"),
    "description": "An open-world masterpiece...",
    "developer": "Nintendo"
}
```

---

## 🌐 Vistas HTML (Templates)

### 1. **Lista de Videojuegos**
```
GET /dynamicpages/
```

**Función:** [videogames_list()](views.py)

**Características:**
- ✅ Consulta MongoDB en tiempo real
- ✅ Muestra todos los videojuegos ordenados por puntuación
- ✅ Sistema de estrellas dinámico
- ✅ Botón para crear nuevo videojuego
- ✅ Links a detalles de cada juego

**Template:** [videogames_list.html](templates/dynamicpages/videogames_list.html)

**Contexto:**
```python
{
    'videogames': [Videogame objects],
    'page_title': 'Catálogo de Videojuegos'
}
```

---

### 2. **Detalle de Videojuego**
```
GET /dynamicpages/videogame/<id>/
```

**Función:** [videogame_detail()](views.py)

**Características:**
- ✅ Busca por ID de MongoDB
- ✅ Muestra información completa del juego
- ✅ Validación de existencia
- ✅ Manejo de errores (404, 500)

**Template:** [videogame_detail.html](templates/dynamicpages/videogame_detail.html)

**URL de ejemplo:**
```
http://localhost:8000/dynamicpages/videogame/507f1f77bcf86cd799439011/
```

---

### 3. **Crear Videojuego**
```
GET  /dynamicpages/create/
POST /dynamicpages/create/
```

**Función:** [create_videogame()](views.py)

**Características:**
- ✅ Formulario HTML (`GET`) para crear juego
- ✅ Procesamiento del formulario (`POST`)
- ✅ Mensajes de éxito/error
- ✅ Redirección a lista tras crear

**Template:** [create_videogame.html](templates/dynamicpages/create_videogame.html)

**Campos del Formulario:**
- `title` (required)
- `genre` (required)
- `score` (required, 0-100)
- `main_platform` (required)
- `developer` (optional)
- `description` (optional)
- `coop` (checkbox)

---

## 🔌 REST API JSON

### 1. **Listar Videojuegos**
```
GET /dynamicpages/api/videogames/
POST /dynamicpages/api/videogames/
```

**Función:** [api_videogames_list()](views.py)

#### GET - Obtener todos los videojuegos

**Respuesta (200 OK):**
```json
{
    "status": "success",
    "total": 15,
    "data": [
        {
            "id": "507f1f77bcf86cd799439011",
            "title": "The Legend of Zelda: Breath of the Wild",
            "genre": "Action-Adventure",
            "score": 97,
            "main_platform": "Nintendo Switch",
            "coop": false,
            "created_at": "2026-01-12T10:00:00Z",
            "description": "An open-world masterpiece...",
            "developer": "Nintendo"
        },
        ...
    ]
}
```

#### POST - Crear nuevo videojuego

**Body:**
```json
{
    "title": "Final Fantasy VII Rebirth",
    "genre": "RPG",
    "score": 95,
    "main_platform": "PlayStation 5",
    "coop": false,
    "developer": "Square Enix",
    "description": "Epic RPG continuation"
}
```

**Respuesta (201 CREATED):**
```json
{
    "status": "success",
    "message": "Videojuego creado exitosamente",
    "data": {
        "id": "507f1f77bcf86cd799439012",
        "title": "Final Fantasy VII Rebirth",
        "genre": "RPG",
        "score": 95,
        "main_platform": "PlayStation 5",
        "coop": false,
        "created_at": "2026-01-12T11:30:00Z",
        "developer": "Square Enix",
        "description": "Epic RPG continuation"
    }
}
```

---

### 2. **Detalle, Actualizar, Eliminar**
```
GET    /dynamicpages/api/videogames/<id>/
PUT    /dynamicpages/api/videogames/<id>/
DELETE /dynamicpages/api/videogames/<id>/
```

**Función:** [api_videogame_detail()](views.py)

#### GET - Obtener videojuego específico

**Respuesta (200 OK):**
```json
{
    "status": "success",
    "data": {
        "id": "507f1f77bcf86cd799439011",
        "title": "The Legend of Zelda: Breath of the Wild",
        "genre": "Action-Adventure",
        "score": 97,
        "main_platform": "Nintendo Switch",
        "coop": false,
        "created_at": "2026-01-12T10:00:00Z",
        "description": "An open-world masterpiece...",
        "developer": "Nintendo"
    }
}
```

#### PUT - Actualizar videojuego (actualización parcial)

**Body (parcial - solo campos a modificar):**
```json
{
    "score": 98,
    "description": "Updated description"
}
```

**Respuesta (200 OK):**
```json
{
    "status": "success",
    "message": "Videojuego actualizado exitosamente",
    "data": {
        "id": "507f1f77bcf86cd799439011",
        "title": "The Legend of Zelda: Breath of the Wild",
        "genre": "Action-Adventure",
        "score": 98,
        "main_platform": "Nintendo Switch",
        "coop": false,
        "created_at": "2026-01-12T10:00:00Z",
        "description": "Updated description",
        "developer": "Nintendo"
    }
}
```

#### DELETE - Eliminar videojuego

**Respuesta (200 OK):**
```json
{
    "status": "success",
    "message": "Videojuego eliminado exitosamente"
}
```

---

## 📝 Templates

### base.html
Template base con estructura HTML, estilos y navegación. Todos los otros templates heredan de este.

```html
{% extends 'dynamicpages/base.html' %}
{% block title %}Mi Página{% endblock %}
{% block content %}
    <!-- Contenido aquí -->
{% endblock %}
```

### videogames_list.html
Listado con tabla/cards de videojuegos, sistema de estrellas dinámico.

### videogame_detail.html
Página individual de un videojuego con información completa.

### create_videogame.html
Formulario para crear nuevo videojuego.

---

## 💡 Ejemplos de Uso

### Usando cURL (API REST)

```bash
# 1. Listar todos los videojuegos
curl -X GET http://localhost:8000/dynamicpages/api/videogames/ \
  -H "Content-Type: application/json"

# 2. Crear nuevo videojuego
curl -X POST http://localhost:8000/dynamicpages/api/videogames/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hollow Knight: Silksong",
    "genre": "Metroidvania",
    "score": 92,
    "main_platform": "Nintendo Switch",
    "coop": false,
    "developer": "Team Cherry",
    "description": "Challenging 2D platformer"
  }'

# 3. Obtener videojuego específico
curl -X GET http://localhost:8000/dynamicpages/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json"

# 4. Actualizar videojuego
curl -X PUT http://localhost:8000/dynamicpages/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "score": 99,
    "description": "Absolutely masterpiece!"
  }'

# 5. Eliminar videojuego
curl -X DELETE http://localhost:8000/dynamicpages/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json"
```

### Usando Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/dynamicpages/api"

# Listar todos
response = requests.get(f"{BASE_URL}/videogames/")
games = response.json()['data']
print(f"Total de juegos: {len(games)}")

# Crear
new_game = {
    "title": "Elden Ring",
    "genre": "Action RPG",
    "score": 96,
    "main_platform": "PC",
    "coop": True,
    "developer": "FromSoftware"
}
response = requests.post(f"{BASE_URL}/videogames/", json=new_game)
created_game = response.json()['data']
game_id = created_game['id']

# Actualizar
update_data = {"score": 97}
response = requests.put(f"{BASE_URL}/videogames/{game_id}/", json=update_data)

# Obtener
response = requests.get(f"{BASE_URL}/videogames/{game_id}/")
game = response.json()['data']

# Eliminar
requests.delete(f"{BASE_URL}/videogames/{game_id}/")
```

### Navegación Web

1. **Listar videojuegos:**
   - URL: http://localhost:8000/dynamicpages/
   - Método: GET (automático)
   - Ver lista con estrellas de puntuación

2. **Ver detalle:**
   - Hacer clic en un videojuego de la lista
   - URL: http://localhost:8000/dynamicpages/videogame/{id}/

3. **Crear nuevo:**
   - Hacer clic en "➕ Agregar Videojuego"
   - URL: http://localhost:8000/dynamicpages/create/
   - Llenar formulario y enviar

---

## 🔄 Flujo de Datos

```
Usuario accede a /dynamicpages/
         ↓
    views.videogames_list()
         ↓
  Consulta a MongoDB (Videogame.objects.all())
         ↓
   VideogameSerializer (conversión)
         ↓
 Render template con contexto
         ↓
   HTML renderizado al navegador
```

---

## 🎨 Estilo y Diseño

- **Tema:** Dark mode con colores neón (cyan, magenta, dorado)
- **Framework CSS:** Estilos inline en base.html
- **Responsive:** Media queries para dispositivos móviles
- **Iconos:** Emojis para navegación intuitiva

---

## 📊 Integración con Otros Módulos

Este módulo se integra con:

- **[auth_api](../auth_api/)** - Autenticación JWT
- **[forn_api](../forn_api/)** - Formularios avanzados
- **[staticpages](../staticpages/)** - Páginas estáticas complementarias

---

## 🚀 Características Clave

✅ **Templates con herencia** - Código DRY con base.html
✅ **Consultas dinámicas** - Datos en tiempo real de MongoDB
✅ **API REST completa** - CRUD con JSON
✅ **Validación serializada** - Datos limpios y seguros
✅ **Manejo de errores** - Respuestas apropiadas (404, 400, 500)
✅ **Sistema de mensajes** - Feedback de usuario (success/error)
✅ **Estrellas dinámicas** - Visualización gráfica de puntuaciones

---

## 📖 Referencia Rápida de URLs

| Ruta | Método | Descripción |
|------|--------|------------|
| `/dynamicpages/` | GET | Listado HTML |
| `/dynamicpages/create/` | GET, POST | Formulario de creación |
| `/dynamicpages/videogame/<id>/` | GET | Detalle HTML |
| `/dynamicpages/api/videogames/` | GET, POST | API lista (JSON) |
| `/dynamicpages/api/videogames/<id>/` | GET, PUT, DELETE | API detalle (JSON) |

---

**Última actualización:** 12 enero 2026

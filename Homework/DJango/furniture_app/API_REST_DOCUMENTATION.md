# 🎮 API REST - Video Games Database

## 📚 ¿Qué es una API REST?

Una **API REST** (Representational State Transfer) es un servicio web que permite que **aplicaciones externas** se comuniquen con tu servidor usando el protocolo HTTP.

### Diferencia: Navegador vs API

```
🌐 Navegador                          🔌 API REST
├─ Solicita HTML                      ├─ Solicita JSON
├─ Devuelve página renderizada        ├─ Devuelve datos puros
└─ Para humanos                        └─ Para máquinas/aplicaciones
```

## 📋 Serializers - ¿Por qué los necesitamos?

### ❌ El Problema

```python
videojuego = Videogame.objects.get(id=1)
return JsonResponse(videojuego)  # ❌ Error! No puede convertir objeto a JSON
```

Los modelos MongoDB son objetos Python complejos. JSON solo entiende:
- strings
- números
- booleanos
- listas y diccionarios

### ✅ La Solución: Serializers

```python
Modelo Videogame (MongoDB)  ←→  VideogameSerializer  ←→  JSON
    {
        id: ObjectId(...),          {
        title: "Portal",            "id": "507f1f77bcf86cd799439011",
        score: 90,          →→→     "title": "Portal",
        created_at: DateTime(...)    "score": 90,
    }                               "created_at": "2025-01-11T10:30:00Z"
                                }
```

### Qué hace el Serializer

| Operación | Código | Resultado |
|-----------|--------|-----------|
| Modelo → JSON | `serializer.data` | `{"id": "...", "title": "Portal"}` |
| JSON → Modelo | `serializer.save()` | Objeto `Videogame` guardado en BD |
| Validación | `serializer.is_valid()` | `True/False` + errores |

## 🔌 Endpoints de la API

Base URL: `http://localhost:8000/api/`

### 1️⃣ Listar todos los videojuegos

```http
GET /api/videogames/
```

**Respuesta:**
```json
{
    "count": 5,
    "results": [
        {
            "id": "507f1f77bcf86cd799439011",
            "title": "Portal",
            "genre": "Puzzle",
            "score": 90,
            "main_platform": "PC",
            "coop": true,
            "created_at": "2025-01-10T15:30:00Z",
            "description": "...",
            "developer": "Valve"
        },
        ...
    ]
}
```

### 2️⃣ Obtener un videojuego específico

```http
GET /api/videogames/{id}/
```

**Ejemplo:**
```http
GET /api/videogames/507f1f77bcf86cd799439011/
```

**Respuesta:**
```json
{
    "id": "507f1f77bcf86cd799439011",
    "title": "Portal",
    "genre": "Puzzle",
    "score": 90,
    "main_platform": "PC",
    "coop": true,
    "created_at": "2025-01-10T15:30:00Z",
    "description": "...",
    "developer": "Valve"
}
```

### 3️⃣ Crear un nuevo videojuego

```http
POST /api/videogames/create/
Content-Type: application/json

{
    "title": "Super Mario Bros",
    "genre": "Platformer",
    "score": 95,
    "main_platform": "Nintendo Switch",
    "coop": true,
    "description": "Un clásico de los videojuegos",
    "developer": "Nintendo"
}
```

**Respuesta (201 Created):**
```json
{
    "id": "507f1f77bcf86cd799439012",
    "title": "Super Mario Bros",
    "genre": "Platformer",
    "score": 95,
    "main_platform": "Nintendo Switch",
    "coop": true,
    "created_at": "2025-01-11T10:30:00Z",
    "description": "Un clásico de los videojuegos",
    "developer": "Nintendo"
}
```

### 4️⃣ Actualizar un videojuego

```http
PUT /api/videogames/{id}/
Content-Type: application/json

{
    "title": "Portal 2",
    "score": 95,
    "description": "La secuela mejorada"
}
```

**Respuesta:**
```json
{
    "id": "507f1f77bcf86cd799439011",
    "title": "Portal 2",
    "genre": "Puzzle",
    "score": 95,
    "main_platform": "PC",
    "coop": true,
    "created_at": "2025-01-10T15:30:00Z",
    "description": "La secuela mejorada",
    "developer": "Valve"
}
```

### 5️⃣ Eliminar un videojuego

```http
DELETE /api/videogames/{id}/
```

**Respuesta (204 No Content):**
```json
{
    "message": "Videojuego eliminado correctamente"
}
```

### 6️⃣ Obtener estadísticas

```http
GET /api/videogames/stats/
```

**Respuesta:**
```json
{
    "total_videojuegos": 5,
    "juegos_con_coop": 3,
    "mejor_juego": {
        "titulo": "Elden Ring",
        "puntuacion": 97,
        "plataforma": "PlayStation 5"
    },
    "mas_reciente": {
        "titulo": "Hades",
        "fecha": "2025-01-11 10:30:00",
        "genero": "Roguelike"
    }
}
```

## 🧪 Cómo probar la API

### Opción 1: cURL (Terminal)

```bash
# Listar todos
curl http://localhost:8000/api/videogames/

# Crear nuevo
curl -X POST http://localhost:8000/api/videogames/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","genre":"Action","score":80,"main_platform":"PC","coop":false}'

# Obtener uno
curl http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/

# Actualizar
curl -X PUT http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{"score":85}'

# Eliminar
curl -X DELETE http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/

# Estadísticas
curl http://localhost:8000/api/videogames/stats/
```

### Opción 2: Postman

1. Descarga [Postman](https://www.postman.com/)
2. Crea un nuevo request
3. Selecciona el método (GET, POST, PUT, DELETE)
4. Ingresa la URL
5. En la pestaña "Body" → selecciona "raw" → "JSON"
6. Pega el JSON y envía

### Opción 3: Python + requests

```python
import requests

# Listar todos
response = requests.get('http://localhost:8000/api/videogames/')
print(response.json())

# Crear nuevo
new_game = {
    "title": "Cyberpunk 2077",
    "genre": "RPG",
    "score": 82,
    "main_platform": "PC",
    "coop": False,
    "description": "Juego futurista",
    "developer": "CD Projekt Red"
}
response = requests.post('http://localhost:8000/api/videogames/create/', json=new_game)
print(response.json())

# Obtener uno
game_id = "507f1f77bcf86cd799439011"
response = requests.get(f'http://localhost:8000/api/videogames/{game_id}/')
print(response.json())
```

## 📊 Códigos HTTP Esperados

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK - Solicitud exitosa | GET /api/videogames/ |
| 201 | Created - Recurso creado | POST /api/videogames/create/ |
| 204 | No Content - Eliminado correctamente | DELETE /api/videogames/{id}/ |
| 400 | Bad Request - Datos inválidos | POST con JSON mal formado |
| 404 | Not Found - Recurso no existe | GET /api/videogames/999/ |
| 500 | Server Error - Error en el servidor | Fallo de BD |

## 🔒 Estructura del Videogame (MongoDB)

```python
class Videogame(Document):
    # Campos disponibles en la API
    _id              → id              # ID de MongoDB (automático)
    title            → title           # Título del juego
    genre            → genre           # Género (Puzzle, Action, RPG, etc)
    score            → score           # Puntuación (0-100)
    main_platform    → main_platform   # Plataforma principal
    coop             → coop            # ¿Tiene modo coop? (True/False)
    created_at       → created_at      # Fecha de creación (automática)
    description      → description     # Descripción (opcional)
    developer        → developer       # Desarrollador (opcional)
```

## 📝 Flujo de una Solicitud API

```
1. Cliente (cURL/Postman/App)
       ↓
2. Request HTTP (GET/POST/PUT/DELETE)
       ↓
3. Django routing: /api/videogames/{id}/ → forn_api/views.py
       ↓
4. Vista API (ej: detalle_videojuego)
       ↓
5. Consulta MongoDB (ej: Videogame.objects.get(pk=id))
       ↓
6. Serializer convierte Modelo → JSON
       ↓
7. Response HTTP + JSON
       ↓
8. Cliente recibe datos
```

## 🎯 Resumen: REST vs tradicional

| Aspecto | REST API | Tradicional |
|---------|----------|-------------|
| Respuesta | JSON | HTML |
| Cliente | Apps, scripts, navegadores | Solo navegador |
| Uso | Datos puros | Página renderizada |
| Escalabilidad | Mayor | Menor |
| Rendimiento | Más rápido | Más lento |

## ✅ Conclusión

Con esta API REST puedes:
- ✅ Crear aplicaciones móviles que consuman los datos
- ✅ Hacer gráficos interactivos con los datos
- ✅ Automatizar tareas con scripts Python
- ✅ Integrar con otros servicios
- ✅ Crear SPAs (Single Page Applications) con React, Vue, etc.

---

**Endpoints disponibles:**

```
GET    /api/videogames/              # Listar todos
POST   /api/videogames/crear/       # Crear nuevo
GET    /api/videogames/{id}/         # Obtener uno
PUT    /api/videogames/{id}/         # Actualizar
DELETE /api/videogames/{id}/         # Eliminar
GET    /api/videogames/stats/        # Estadísticas
```

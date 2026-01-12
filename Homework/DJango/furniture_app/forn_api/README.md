# 📝 FORN_API - API REST Avanzada y Estadísticas

Módulo de **REST API avanzada** que proporciona endpoints adicionales para operaciones CRUD completas, búsquedas personalizadas y **estadísticas de la base de datos**. Complementa a [dynamicpages](../dynamicpages/) con funcionalidades de API pura (sin templates HTML).

---

## 📋 Tabla de Contenidos

- [Estructura](#estructura)
- [Endpoints API](#endpoints-api)
- [Estadísticas](#estadísticas)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Diferencias con dynamicpages](#diferencias-con-dynamicpages)

---

## 📁 Estructura

```
forn_api/
├── __init__.py              # Configuración del app
├── apps.py                  # Definición de la app
├── admin.py                 # Admin de Django (no usado)
├── models.py                # Modelos locales (vacío)
├── views.py                 # Endpoints de la API
├── urls.py                  # Rutas de la API
├── tests.py                 # Tests unitarios
├── migrations/              # Migraciones de BD
├── __pycache__/
└── README.md                # Este archivo
```

---

## 🔌 Endpoints API

### 1. **Listar Videojuegos**
```
GET /api/videogames/
```

**Función:** [lista_videojuegos()](views.py)

**Respuesta (200 OK):**
```json
{
    "count": 15,
    "results": [
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
        {
            "id": "507f1f77bcf86cd799439012",
            "title": "Elden Ring",
            "genre": "Action RPG",
            "score": 96,
            "main_platform": "PC",
            "coop": true,
            "created_at": "2026-01-12T11:00:00Z",
            "description": "Collaborative adventure...",
            "developer": "FromSoftware"
        },
        ...
    ]
}
```

**Características:**
- ✅ Retorna lista ordenada por puntuación (descendente)
- ✅ Incluye contador total
- ✅ Datos serializados en JSON

---

### 2. **Crear Videojuego**
```
POST /api/videogames/create/
```

**Función:** [crear_videojuego()](views.py)

**Body (JSON):**
```json
{
    "title": "Final Fantasy VII Rebirth",
    "genre": "RPG",
    "score": 95,
    "main_platform": "PlayStation 5",
    "coop": false,
    "developer": "Square Enix",
    "description": "Epic RPG continuation of the remake saga"
}
```

**Respuesta (201 CREATED):**
```json
{
    "id": "507f1f77bcf86cd799439015",
    "title": "Final Fantasy VII Rebirth",
    "genre": "RPG",
    "score": 95,
    "main_platform": "PlayStation 5",
    "coop": false,
    "created_at": "2026-01-12T14:30:00Z",
    "description": "Epic RPG continuation of the remake saga",
    "developer": "Square Enix"
}
```

**Errores:**
- `400 BAD REQUEST` - Datos inválidos o incompletos

---

### 3. **Obtener Detalle**
```
GET /api/videogames/<id>/
```

**Función:** [detalle_videojuego()](views.py)

**URL de ejemplo:**
```
GET /api/videogames/507f1f77bcf86cd799439011/
```

**Respuesta (200 OK):**
```json
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
}
```

**Errores:**
- `404 NOT FOUND` - Videojuego no existe

---

### 4. **Actualizar Videojuego**
```
PUT /api/videogames/<id>/
```

**Función:** [detalle_videojuego()](views.py)

**Body (JSON - actualización parcial):**
```json
{
    "score": 98,
    "description": "Updated review after replay"
}
```

**Respuesta (200 OK):**
```json
{
    "id": "507f1f77bcf86cd799439011",
    "title": "The Legend of Zelda: Breath of the Wild",
    "genre": "Action-Adventure",
    "score": 98,
    "main_platform": "Nintendo Switch",
    "coop": false,
    "created_at": "2026-01-12T10:00:00Z",
    "description": "Updated review after replay",
    "developer": "Nintendo"
}
```

**Errores:**
- `404 NOT FOUND` - Videojuego no existe
- `400 BAD REQUEST` - Datos inválidos

---

### 5. **Eliminar Videojuego**
```
DELETE /api/videogames/<id>/
```

**Función:** [detalle_videojuego()](views.py)

**Respuesta (204 NO CONTENT):**
```json
{
    "message": "Videojuego eliminado correctamente"
}
```

**Errores:**
- `404 NOT FOUND` - Videojuego no existe

---

## 📊 Estadísticas

### Endpoint de Estadísticas
```
GET /api/videogames/stats/
```

**Función:** [estadisticas_videojuegos()](views.py)

**Respuesta (200 OK):**
```json
{
    "total_videojuegos": 15,
    "juegos_con_coop": 7,
    "mejor_juego": {
        "titulo": "The Legend of Zelda: Breath of the Wild",
        "puntuacion": 97,
        "plataforma": "Nintendo Switch"
    },
    "mas_reciente": {
        "titulo": "Final Fantasy VII Rebirth",
        "fecha": "2026-01-12 14:30:00",
        "genero": "RPG"
    }
}
```

**Información que proporciona:**
- 📊 **Total de videojuegos** - Cantidad total en la BD
- 🤝 **Juegos con cooperativo** - Cuenta de juegos multijugador
- 🏆 **Mejor juego** - El de mayor puntuación con detalles
- 📅 **Más reciente** - El creado recientemente con detalles

---

## 💡 Ejemplos de Uso

### Usando cURL

```bash
# 1. Listar todos los videojuegos
curl -X GET http://localhost:8000/api/videogames/ \
  -H "Content-Type: application/json"

# 2. Crear nuevo videojuego
curl -X POST http://localhost:8000/api/videogames/create/ \
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
curl -X GET http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json"

# 4. Actualizar videojuego
curl -X PUT http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "score": 99,
    "description": "Absolutely masterpiece!"
  }'

# 5. Eliminar videojuego
curl -X DELETE http://localhost:8000/api/videogames/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json"

# 6. Ver estadísticas
curl -X GET http://localhost:8000/api/videogames/stats/ \
  -H "Content-Type: application/json"
```

### Usando Python (requests)

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/videogames"

# 1. Listar
response = requests.get(f"{BASE_URL}/")
data = response.json()
print(f"Total de juegos: {data['count']}")
for game in data['results']:
    print(f"- {game['title']} ({game['score']}/100)")

# 2. Crear
new_game = {
    "title": "Cyberpunk 2077",
    "genre": "Action RPG",
    "score": 88,
    "main_platform": "PC",
    "coop": False,
    "developer": "CD Projekt Red",
    "description": "Open-world dystopian RPG"
}
response = requests.post(f"{BASE_URL}/create/", json=new_game)
created = response.json()
game_id = created['id']
print(f"✅ Creado: {created['title']} (ID: {game_id})")

# 3. Obtener
response = requests.get(f"{BASE_URL}/{game_id}/")
game = response.json()
print(f"Título: {game['title']}")
print(f"Puntuación: {game['score']}/100")

# 4. Actualizar
update = {"score": 90}
response = requests.put(f"{BASE_URL}/{game_id}/", json=update)
updated = response.json()
print(f"✏️ Actualizado a {updated['score']}/100")

# 5. Eliminar
response = requests.delete(f"{BASE_URL}/{game_id}/")
print("🗑️ Eliminado")

# 6. Estadísticas
response = requests.get(f"{BASE_URL}/stats/")
stats = response.json()
print(f"📊 Total: {stats['total_videojuegos']} juegos")
print(f"🤝 Con coop: {stats['juegos_con_coop']}")
print(f"🏆 Mejor: {stats['mejor_juego']['titulo']} ({stats['mejor_juego']['puntuacion']}/100)")
```

### Usando JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000/api/videogames";

// Listar
async function listar() {
    const response = await fetch(`${BASE_URL}/`);
    const data = await response.json();
    console.log(`Total: ${data.count} videojuegos`);
    data.results.forEach(game => {
        console.log(`- ${game.title}: ${game.score}/100`);
    });
}

// Crear
async function crear() {
    const newGame = {
        title: "Star Wars Outlaws",
        genre: "Action-Adventure",
        score: 91,
        main_platform: "PC",
        coop: false,
        developer: "Massive Entertainment",
        description: "Open-world Star Wars adventure"
    };
    
    const response = await fetch(`${BASE_URL}/create/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newGame)
    });
    const created = await response.json();
    console.log(`✅ Creado: ${created.title}`);
    return created.id;
}

// Actualizar
async function actualizar(id) {
    const update = { score: 92 };
    const response = await fetch(`${BASE_URL}/${id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(update)
    });
    const updated = await response.json();
    console.log(`✏️ Actualizado a ${updated.score}/100`);
}

// Estadísticas
async function estadisticas() {
    const response = await fetch(`${BASE_URL}/stats/`);
    const stats = await response.json();
    console.log("📊 Estadísticas:");
    console.log(`- Total: ${stats.total_videojuegos}`);
    console.log(`- Con coop: ${stats.juegos_con_coop}`);
    console.log(`- Mejor: ${stats.mejor_juego.titulo}`);
}
```

---

## 🔄 Diferencias con dynamicpages

| Aspecto | forn_api | dynamicpages |
|--------|---------|--------------|
| **Propósito** | API REST pura | Vistas HTML + API |
| **Salida** | JSON | HTML + JSON |
| **Templates** | No | Sí |
| **Endpoints** | 5 (CRUD + stats) | 3 HTML + 2 API |
| **Estadísticas** | ✅ Sí | ❌ No |
| **Navegación Web** | ❌ No (API pura) | ✅ Sí |
| **Casos de uso** | Apps móviles, SPA | Sitios web tradicionales |

---

## 🎯 Casos de Uso

### 1. **Aplicación Móvil**
```javascript
// Frontend React Native/Flutter
const response = await fetch('http://api.example.com/api/videogames/');
const games = await response.json();
// Renderizar lista en app móvil
```

### 2. **Single Page Application (SPA)**
```javascript
// Frontend React/Vue/Angular
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/videogames'
});

// Usar en componentes
const [games, setGames] = useState([]);
useEffect(() => {
    api.get('/').then(res => setGames(res.data.results));
}, []);
```

### 3. **Dashboard Administrativo**
```python
# Backend Python
import requests

api = requests.Session()
api.headers.update({'Content-Type': 'application/json'})

# Obtener estadísticas para dashboard
stats = api.get('http://localhost:8000/api/videogames/stats/').json()
print(f"Dashboard - Total de juegos: {stats['total_videojuegos']}")
```

### 4. **Integración con Otras APIs**
```bash
# Sincronizar con servicio externo
curl -X GET http://localhost:8000/api/videogames/ \
  | jq '.results | length'  # Procesar con jq
```

---

## 📝 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| [views.py](views.py) | 5 funciones de API (lista, crear, detalle, actualizar, eliminar, stats) |
| [urls.py](urls.py) | Rutas de los 5 endpoints |
| [apps.py](apps.py) | Configuración de la app |
| [models.py](models.py) | Vacío (usa modelos de dynamicpages) |
| [admin.py](admin.py) | Vacío (no necesario) |

---

## 🔐 Seguridad

### Recomendaciones para Producción

```python
# Agregar en settings.py

# 1. Rate limiting
# pip install djangorestframework-throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# 2. Autenticación
# Usar JWT de auth_api
from auth_api.jwt_utils import verify_token

@api_view(['GET'])
def lista_videojuegos(request):
    # Verificar token
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return Response({'error': 'No autorizado'}, status=401)
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    if 'error' in payload:
        return Response({'error': 'Token inválido'}, status=401)
    
    # Continuar con la lógica...
```

---

## 🚀 Integración con Otros Módulos

Este módulo se integra con:

- **[dynamicpages](../dynamicpages/)** - Comparten el modelo Videogame y serializer
- **[auth_api](../auth_api/)** - Puede protegerse con JWT (recomendado en producción)
- **[staticpages](../staticpages/)** - Pueden consumir esta API

---

## 📖 Referencia Rápida de URLs

| Ruta | Método | Descripción |
|------|--------|------------|
| `/api/videogames/` | GET | Listar todos (JSON) |
| `/api/videogames/create/` | POST | Crear nuevo |
| `/api/videogames/<id>/` | GET | Obtener detalle |
| `/api/videogames/<id>/` | PUT | Actualizar |
| `/api/videogames/<id>/` | DELETE | Eliminar |
| `/api/videogames/stats/` | GET | Ver estadísticas |

---

**Última actualización:** 12 enero 2026

# **🎮 API RESTful de Videojuegos (Flask) - 🕹️ Video Games API – Flask Project**
    Proyecto de Backend desarrollado con Python y el microframework Flask para exponer una colección "quemada" de videojuegos a través de una API RESTful.

# **📌 Descripción del Proyecto**

Esta aplicación es una REST API construida con Flask, enfocada en gestionar una colección de videojuegos.
Los datos se almacenan en un diccionario “quemado” (hardcoded) dentro del código, cumpliendo el requisito de la tarea.

### La API permite:
    -Obtener todos los videojuegos
    -Obtener un videojuego por ID
    -Filtrar videojuegos por género y por si tienen modo cooperativo
    -Buscar por título
    -Buscar por plataforma
    -Agregar nuevos videojuegos (POST)
    -Modificar videojuegos existentes (PUT)
    -Eliminar videojuegos por ID (DELETE)


### Estructura del proyecto
     📁 /Flask
         📁 /img
             📁 /error
                    ├── error_get_id.png
                    ├── error_get_options.png
                    ├── error_get_platform.png
                    ├── error_get_title.png
                    ├── error_put_games.png
             📁 /success
                    ├── delete_games.png
                    ├── get_all.png
                    ├── get_id.png
                    ├── get_options.png
                    ├── get_options1.png
                    ├── get_platform.png
                    ├── get_platform1.png
                    ├── get_title.png
                    ├── post_games.png
                    ├── put_games.png
    ├──app.py
    ├──README.md
    ├──.gitignore

<!-- _______________________________________________________________________________________________________________ -->
## **🎮 Tema elegido: Videojuegos**

    La API trabaja con un “diccionario quemado” (lista en memoria) llamado games, que contiene múltiples videojuegos.
    Cada videojuego incluye al menos 5 campos, por ejemplo:
            {
                "id": 1,
                "title": "Portal",
                "genre": "First-person puzzle",
                "score": 90,
                "main_platform": "PC",
                "coop": false
            }

<!-- _______________________________________________________________________________________________________________ -->

## 🧠 **Tecnologías Utilizadas**

    * Python 3
    * Flask
    * JSON

---

<!-- _______________________________________________________________________________________________________________ -->

# 🚀 **Cómo Ejecutar el Proyecto**

    1. Instalar dependencias:

```bash
    pip install flask
```

2. Ejecutar la aplicación:

```bash
    python app.py
```

3. Abrir en el navegador o Postman:

```
    http://localhost:8001/
```

<!-- _______________________________________________________________________________________________________________ -->

# 🎮 **Endpoints Disponibles:**

## 📌 **1. Home**

**GET /**
Pantalla de bienvenida.

---

## 📌 **2. Obtener todos los videojuegos**

**GET /api/games/**

### 🔍 Query params opcionales:

    | Parámetro | Tipo    | Ejemplo         | Descripción                      |
    | --------- | ------- | --------------- | -------------------------------- |
    | `genre`   | string  | `?genre=Puzzle` | Filtra por género                |
    | `coop`    | boolean | `?coop=true`    | Filtra si tiene modo cooperativo |

    Ejemplo:

    ```
    /api/games/?genre=Platformer&coop=true
    ```

---

## 📌 **3. Obtener un videojuego por ID**

**GET /api/games/"id"/**

    Ejemplo:

    ```
    /api/games/5/
    ```

    ---

## 📌 **4. Buscar videojuegos por título**

**GET /api/games/title/"title"/**

    Ejemplo:

    ```
    /api/games/title/portal/
    ```

    ---

## 📌 **5. Buscar videojuegos por plataforma**

**GET /api/games/platform/"platform"/**

    Ejemplo:

    ```
    /api/games/platform/pc/
    ```

---

## 📌 **6. Agregar un videojuego (POST)**

**POST /api/games/**

### 📝 Body JSON requerido:


    {
        "title": "Nombre del juego",
        "genre": "Género",
        "score": 90,
        "main_platform": "PC",
        "coop": true
    }

Por ejemplo:
```json
    {
        "title": "Celeste",
        "genre": "Platformer / Precision",
        "score": 96,
        "main_platform": "Switch / PC",
        "coop": false
    }
```
_**Retorna el nuevo elemento con ID autoincremental.**_

---

## 📌 **7. Actualizar un videojuego (PUT)**

**PUT /api/games/"id"/**

Puedes enviar un JSON parcial, solo actualizando los campos deseados (esto se pasa por el body):

```json
{
  "score": 95,
  "coop": false
}
```

---

## 📌 **8. Eliminar un videojuego (DELETE)**

**DELETE /api/games/"id"/**

Ejemplo:

```
/api/games/10/
```

<!-- _______________________________________________________________________________________________________________ -->

# ✔️ **Cumplimiento de Requisitos**

| Requisito                            | Estado            |
| ------------------------------------ | ----------------- |
| Flask app con un tema                | ✔️                |
| Diccionario quemado con 5+ elementos | ✔️ (16 juegos)    |
| Mínimo 5 campos por elemento         | ✔️                |
| GET ONE                              | ✔️                |
| GET ALL                              | ✔️                |
| Filtros con query params             | ✔️ (genre, coop)  |
| POST                                 | ✔️                |
| DELETE                               | ✔️                |
| Imágenes de endpoints funcionando    | ✔️ (carpeta /img) |
| .gitignore                           | ✔️                |

---

# 🔐 **Autenticación y Manejo de Usuarios (JWT + Roles)**

Además de gestionar videojuegos, esta API implementa **registro de usuarios, login con JWT y control de acceso por roles**.

Los usuarios están almacenados en una lista “quemada” en memoria, al igual que los videojuegos.

La API soporta:

* Registro de nuevos usuarios (`POST /api/register/`)
* Inicio de sesión con JWT (`POST /api/login/`)
* Tokens con expiración (15 minutos)
* Claims personalizados (como el rol del usuario)
* Rutas protegidas con `@jwt_required()`
* Rutas protegidas por rol usando el decorador `@role_required("admin")`

---

# 👤 **1. Registro de Usuario**

**POST /api/register/**

Permite crear un nuevo usuario con rol **user** por defecto.

### 📝 Body JSON requerido:

```json
{
  "username": "nuevo_usuario",
  "password": "123456",
  "age": 25
}
```

### ✔️ Validaciones:

* No permite usernames repetidos.
* Encripta la contraseña usando `generate_password_hash()`.
* Genera un `id` único con `uuid4`.

### 📌 Respuesta exitosa:

```json
{
  "status": "success",
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": "uuid-generado",
    "username": "nuevo_usuario"
  }
}
```

---

# 🔑 **2. Inicio de Sesión (Login)**

**POST /api/login/**

Permite a un usuario obtener un **token JWT**, necesario para acceder a las rutas protegidas.

### 📝 Body JSON requerido:

```json
{
  "username": "vanessa",
  "password": "shadow_love"
}
```

### ✔️ Validaciones:

* Verifica si el usuario existe.
* Verifica la contraseña con `check_password_hash()`.

### 📌 Respuesta exitosa:

```json
{
  "status": "success",
  "message": "Login exitoso.",
  "access_token": "TOKEN_JWT"
}
```

Puedes usar este token en Postman o navegador:

```
Authorization: Bearer TOKEN_AQUÍ
```

---

# 🛡️ **3. Rutas Protegidas (JWT Required)**

Cualquier endpoint que tenga:

```python
@jwt_required()
```

requiere un token válido para ser accedido.

Ejemplos protegidos:

* GET /api/games/
* GET /api/games/<id>/
* GET /api/games/title/<title>/
* GET /api/games/platform/<platform>/

Si el token expiró (15 min), debes volver a hacer login.

---

# 👑 **4. Control de Roles (admin / user)**

La API incluye un decorador especial:

```python
@role_required("admin")
```

Esto restringe el acceso a ciertos endpoints sensibles.

### 🛑 Solo **admin** puede:

| Acción           | Endpoint                |
| ---------------- | ----------------------- |
| Agregar juego    | POST /api/games/        |
| Actualizar juego | PUT /api/games/<id>/    |
| Eliminar juego   | DELETE /api/games/<id>/ |

### ✔️ Los usuarios normales solo pueden hacer:

* Leer juegos (GET)
* Filtrar juegos
* Buscar juegos por título o plataforma

---

# 🧠 **5. Estructura interna del usuario**

Cada usuario se almacena así:

```json
{
    "id": "uuid",
    "username": "vanessa",
    "password": "hash",
    "age": 26,
    "role": "admin",
    "created_at": "2025-02-02T08:30:00"
}
```

Las contraseñas NO se guardan en texto plano.

---

# 🔐 **6. Ejemplo de Token JWT**

Los tokens incluyen:

* `identity`: el ID del usuario
* `role`: incluido como claim adicional

Ejemplo claim:

```json
{
  "sub": "uuid-del-usuario",
  "role": "admin",
  "exp": 1734022134
}
```

---

# 📌 **7. Cómo probar Login + Acceso Protegido**

### 1️⃣ Haces login:

POST → `/api/login/`

Copia el token.

### 2️⃣ En Postman:

En **Authorization → Bearer Token**:

```
eyJ0eXAiOiJKV1QiLCJh...
```

### 3️⃣ Ya puedes consumir endpoints como:

```
GET /api/games/
```

Si no envías el token → 401
Si no eres admin e intentas un POST/PUT/DELETE → 403

---

# 👩‍💻 Autora
Vanessa Hernández
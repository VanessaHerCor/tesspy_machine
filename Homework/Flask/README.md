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

# 👩‍💻 Autora
Vanessa Hernández
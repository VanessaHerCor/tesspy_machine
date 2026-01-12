from flask import Flask, request, jsonify
# Flask: la clase principal para crear la aplicación web
# request: un objeto que te permite leer datos enviados por el cliente (JSON, query params, headers, formularios, etc)
# jsonify: una función que convierte listas/diccionarios de Python en una respuesta JSON válida para enviar al navegador
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#import uuid ya no necesito esto
from flask_jwt_extended import create_access_token, JWTManager, jwt_required,get_jwt
import os
from pymongo import MongoClient
# Crear un decorador para proteger rutas segun el rol
from functools import wraps

from bson import ObjectId
from bson.errors import InvalidId

# Convierte documentos Mongo en JSON amigable
def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def role_required(required_role): 
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", None)

            if user_role != required_role:
                return jsonify({
                    "status": "error",
                    "message": "No tienes permisos para realizar esta acción."
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

app = Flask(__name__)

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret") #Deberia ser una clave secreta mas segura en produccion
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)  #Deberia ser una clave secreta mas segura en produccion
jwt = JWTManager(app)

# MongoDB config
host = "mongodb://localhost"
port = 27017
db_name = "games_database"

games_collection = None
users_collection = None

def connect_db():
    global games_collection, users_collection

    try:
        client = MongoClient(f"{host}:{port}/")
        db = client[db_name]

        games_collection = db.games
        users_collection = db.users

        # Probar conexión real
        client.admin.command("ping")

        print("✅ Conexión a MongoDB exitosa")
        print(f"✅ Games collection OK: {games_collection is not None}")
        print(f"✅ Users collection OK: {users_collection is not None}")

    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        print("⚠️ La aplicación requiere MongoDB para funcionar correctamente.")


games = [
    {"id": 1,"title": "Portal","genre": "First-person puzzle","score": 90,"main_platform": "PC","coop": False},
    {"id": 2,"title": "Portal 2","genre": "First-person puzzle","score": 95,"main_platform": "PC","coop": True},
    {"id": 3,"title": "Super Mario Bros 3","genre": "Platformer","score": 97,"main_platform": "Nintendo","coop": False},
    {"id": 4,"title": "Red Dead Redemption","genre": "Action / Open world","score": 95,"main_platform": "Consoles","coop": False},
    {"id": 5,"title": "Superliminal","genre": "Puzzle","score": 75,"main_platform": "PC","coop": False},
    {"id": 6,"title": "Cult of the Lamb","genre": "Action / Management","score": 85,"main_platform": "PC / Switch","coop": True},
    {"id": 7,"title": "Baldur's Gate 3","genre": "Tactical RPG","score": 98,"main_platform": "PC","coop": True},
    {"id": 8,"title": "Titanfall 2","genre": "Shooter","score": 90,"main_platform": "PC / Consoles","coop": False},
    {"id": 9,"title": "The Stanley Parable","genre": "Narrative exploration","score": 89,"main_platform": "PC","coop": False},
    {"id": 10,"title": "Killer Frequency","genre": "Narrative horror","score": 80,"main_platform": "PC","coop": False},
    {"id": 11,"title": "Metal: Hellsinger","genre": "Rhythm shooter","score": 90,"main_platform": "PC","coop": False},
    {"id": 12,"title": "Cuphead","genre": "Platformer / Boss rush","score": 88,"main_platform": "PC / Xbox / Switch","coop": True},
    {"id": 13,"title": "Sonic Mania","genre": "Platformer","score": 90,"main_platform": "Switch / PC / PS4","coop": True},
    {"id": 14,"title": "Detroit: Become Human","genre": "Narrative adventure","score": 95,"main_platform": "PlayStation / PC","coop": False},
    {"id": 15,"title": "Coffee Talk","genre": "Visual novel","score": 80,"main_platform": "PC / Switch","coop": False},
    {"id": 16,"title": "Dispatch","genre": "Horror / Thriller","score": 80,"main_platform": "PC","coop": False}
]

#ID autoincremental para nuevos juegos
next_id = 17

@app.route('/')
def home():
    return "<h1 style='color:cyan;'> Bienvenido! </h1>" \
           "<h2> Buscador de Videojuegos </h2>"

# --- ENDPOINTS REST ---

# Obtenert Uno GET ONE (Por ID)
#Ruta de ejemplo: /api/games/3/
@app.route('/api/games/<string:game_id>/', methods=['GET'])
@jwt_required() #Protege la ruta con JWT, requiere token valido
def get_game(game_id):

    try:
        game = games_collection.find_one(
            {"_id": ObjectId(game_id)}
        )
    except InvalidId:
        return jsonify({
            "status": "error",
            "message": "ID invalido"
        }), 400
    
    if not game:
        return jsonify({
            "status": "error",
            "message": f"Juego con ID {game_id} no encontrado"
        }), 404

    # Llama a serialize para devolver el documento con _id en formato string
    return jsonify(serialize(game)), 200

#Obtener todo con parametros Opcionales)
#Mas o menos Ruta: /api/games/?genre=Puzzle&coop=true
@app.route('/api/games/', methods=['GET'])
@jwt_required() #Protege la ruta con JWT, requiere token valido
def get_games():

    
    #Obtener los Query Parameters (Los Opcionales)
    genre = request.args.get('genre') #Obtiene el valor de genre por ejemplo Puzzle
    coop = request.args.get('coop')   #Obtiene el valor del coop ejemplo true o false
    query = {}

    # Filtro por género
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}

    # Filtro por coop
    if coop is not None:
        query["coop"] = coop.lower() == "true" #.lower(): convierte todo a minusculas

    games = list(games_collection.find(query))

    if not games:
        return jsonify({
            "status": "error",
            "message": "No se encontraron juegos con ese filtro"
        }), 404

    return jsonify([serialize(g) for g in games]), 200


# FILTRAR LOS JUEGOS POR TITULO
@app.route('/api/games/title/<string:title>/')
@jwt_required() #Protege la ruta con JWT, requiere token valido
def get_title(title):
    
    games = list(games_collection.find({
        "title": {"$regex": title, "$options": "i"}
    }))
    
    # Si la lista esta vacia - title invalido o sin juegos
    if not games:
        return jsonify({
            "status": "error",
            "message": f"No se encontraron juegos con el nombre de: {title}"
        }), 404
    
    return jsonify([serialize(g) for g in games]), 200

# FILTRAR LOS JUEGOS POR PLATFORMA
@app.route('/api/games/platform/<string:main_platform>/')
@jwt_required() #Protege la ruta con JWT, requiere token valido
def get_platform(main_platform):
    
    games = list(games_collection.find({
        "main_platform": {"$regex": main_platform, "$options": "i"}
    }))

    # Si la lista esta vacia - plataforma invalida o sin juegos
    if not games:
        return jsonify({
            "status": "error",
            "message": f"No se encontraron juegos con el nombre de: {main_platform}"
        }), 404
    
    return jsonify([serialize(g) for g in games]), 200

#POST agregar un Elemento
@app.route('/api/games/', methods=['POST'])
@jwt_required() #Protege la ruta con JWT, requiere token valido
@role_required("admin") #Protege la ruta segun el rol
def add_game():
    
    #obtiene el JSON enviado en el cuerpo de la peticion
    new_game_data = request.get_json()

    required = [
                    "title", 
                    "genre", 
                    "score", 
                    "main_platform", 
                    "coop"
                ]

    #Verifica que new_game_data no sea None y que CADA elemento de la lista 'required' exista como clave en new_game_data
    if not new_game_data or not all(field in new_game_data for field in required):
        return jsonify({
            "status": "error",
            "message": f"Datos de juego invalidos. Se requieren todos estos campos: {', '.join(required)}."
        }), 400
    
    # Insertar en Mongo crear el nuevo objeto juego
    new_game = games_collection.insert_one({
        "title": new_game_data["title"],
        "genre": new_game_data["genre"],
        "score": new_game_data["score"],
        "main_platform": new_game_data["main_platform"],
        "coop": new_game_data["coop"],
        "created_at": datetime.now()
    })

    return jsonify({
        "status": "created",# 201 Created
        "message": "Juego agregado exitosamente",
        "id": str(new_game.inserted_id)
    }), 201

#UPDATE (Modificar un elemento existente)
#Metodo PUT en la misma ruta del GET individual, ejemplo /api/games/12/
@app.route('/api/games/<string:game_id>/', methods=['PUT'])
@jwt_required() #Protege la ruta con JWT, requiere token valido
@role_required("admin") #Protege la ruta segun el rol
def update_game(game_id):

    try:
        game = games_collection.find_one(
            {"_id": ObjectId(game_id)}
        )
    except InvalidId:
        return jsonify({
            "status": "error",
            "message": "ID invalido"
        }), 400
    
    # Obtener campos enviados en el body (JSON)
    update_data = request.get_json()

    if not update_data:
        return jsonify({
            "status": "error",
            "message": "Debes enviar al menos un campo para actualizar."
        }), 400

    #Actualizar solo los campos enviados
    result = games_collection.update_one(
        {"_id": ObjectId(game_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        return jsonify({
            "status": "error",
            "message": f"Juego con ID {game_id} no encontrado"
        }), 404

    return jsonify({
                "status": "success",
                "message": f"Juego con ID {game_id} actualizado correctamente",
    }), 200

#DELETE (Eliminar un Elemento)
# Ruta: /api/games/3/
@app.route('/api/games/<string:game_id>/', methods=['DELETE'])
@jwt_required() #Protege la ruta con JWT, requiere token valido
@role_required("admin") #Protege la ruta segun el rol
def delete_game(game_id):
  
    try:
        game = games_collection.find_one(
            {"_id": ObjectId(game_id)}
        )
    except InvalidId:
        return jsonify({
            "status": "error",
            "message": "ID invalido"
        }), 400

    result = games_collection.delete_one({"_id": ObjectId(game_id)})

    if result.deleted_count == 0:
        return jsonify({
                "status": "error",
                "message": f"Juego con ID {game_id} no encontrado"
        }), 404

    return jsonify({
                "status": "success",
                "message": "Juego con eliminado correctamente",
    }), 200

# ______________________________________________________________________________________________________________________________________
# Parte del usuario y autenticacion JWT con MONGODB

@app.route('/api/register/', methods=['POST'])
def register_user():
    user_data = request.get_json()

    required = ["username", "password", "age"]

    # Validar campos
    if not user_data or not all(field in user_data for field in required):
        return jsonify({
            "status": "error",
            "message": f"Datos inválidos. Se requieren: {', '.join(required)}."
        }), 400

    username = user_data["username"]

    # --- CAMBIO 1: Validar usuario duplicado en MongoDB ---
    if users_collection.find_one({"username": username}):
        return jsonify({
            "status": "error",
            "message": "El usuario ya existe. Elige otro nombre."
        }), 409  # 409: conflicto

    # Crear usuario nuevo
    new_user = {
        # MongoDB generará automáticamente el _id. Ya no necesitamos uuid.uuid4()
        "username": username,
        "password": generate_password_hash(user_data["password"]),
        "age": user_data["age"],
        "role": "user",
        "created_at": datetime.now()
    }

    # --- CAMBIO 2: Insertar en MongoDB ---
    result = users_collection.insert_one(new_user)
    
    # El ID insertado es result.inserted_id (es un ObjectId, lo convertimos a str)

    return jsonify({
        "status": "success",
        "message": "Usuario registrado exitosamente",
        "user": {
            "id": str(result.inserted_id),
            "username": new_user["username"]
        }
    }), 201


@app.route('/api/login/', methods=['POST'])
def login():
    login_data = request.get_json()

    if not login_data or "username" not in login_data or "password" not in login_data:
        return jsonify({
            "status": "error",
            "message": "Debes enviar username y password."
        }), 400

    username = login_data["username"]
    password = login_data["password"]

    #Buscar usuario en MongoDB
    user = users_collection.find_one({"username": username})

    # Validar existencia y contraseña
    if not user or not check_password_hash(user["password"], password):
        return jsonify({
            "status": "error",
            "message": "Usuario y/o contraseña incorrectos."
        }), 401
    
    #Usar el _id de MongoDB para el token
    # Usamos str(user["_id"]) porque ObjectId no es JSON serializable
    token = create_access_token(
        identity=str(user["_id"]), 
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "status": "success",
        "message": "Login exitoso.",
        "access_token": token
    }), 200


# _______________________________________________________________________________________________________________________________________
# Lo que levanta el servidor
if __name__ == '__main__':
    connect_db()
    app.run(debug=True, port=8001)
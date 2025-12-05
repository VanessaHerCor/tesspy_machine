from flask import Flask, request, jsonify
# Flask: la clase principal para crear la aplicación web
# request: un objeto que te permite leer datos enviados por el cliente (JSON, query params, headers, formularios, etc)
# jsonify: una función que convierte listas/diccionarios de Python en una respuesta JSON válida para enviar al navegador
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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
@app.route('/api/games/<int:game_id>/', methods=['GET'])
def get_game(game_id):

    #Otra forma °° Revisa cada g dentro de la lista games y se queda solo con los que tengan g["id"] == game_id
    game = next((g for g in games if g["id"] == game_id), None)
    
    if game:
        return jsonify(game), 200
    else:
        return jsonify({"message": f"El Juego con el ID {game_id} no se encuentra"}), 404


#Obtener todo con parametros Opcionales)
#Mas o menos Ruta: /api/games/?genre=Puzzle&coop=true
@app.route('/api/games/', methods=['GET'])
def get_games():
    global games
    
    #Obtener los Query Parameters (Los Opcionales)
    genre_filter = request.args.get('genre') #Obtiene el valor de genre por ejemplo Puzzle
    coop_filter = request.args.get('coop')   #Obtiene el valor del coop ejemplo true o false
    
    #variable pa ir filtrando
    filtered_games = games

    #aplicar el filtro de genre
    if genre_filter:
        filtered_games = [
            game for game in filtered_games #ELEMENTO_A_GUARDAR for VARIABLE in LISTA
            if genre_filter.lower() in game["genre"].lower() #.lower(): convierte todo a minusculas
        ]

    # 3. Aplicar el filtro de COOP (booleano)
    if coop_filter is not None:
        # Convertir el string del query param ('true'/'false') a booleano
        is_coop = coop_filter.lower() == 'true'
        filtered_games = [
            game for game in filtered_games
            if game["coop"] == is_coop
        ]
        
    if not filtered_games:
        return jsonify({"message": "No se encontraron juegos con esos filtros"}), 404
        
    return jsonify(filtered_games), 200

@app.route('/api/games/title/<string:title>/')
def get_title(title):
    # FILTRAR LOS JUEGOS POR TITULO
    filtered = [
        game for game in games #ELEMENTO_A_GUARDAR for VARIABLE in LISTA
        if title.lower() in game["title"].lower() #.lower(): convierte todo a minusculas
    ]

    # Si la lista esta vacia - title invalido o sin juegos
    if not filtered:
        response = {
            "status": "error",
            "message": f"No se encontraron juegos con el nombre de: {title}"
        },404
    else:
        response = jsonify(filtered),200
    
    return response

@app.route('/api/games/platform/<string:main_platform>/')
def get_platform(main_platform):
    # FILTRAR LOS JUEGOS POR PLATFORMA
    filtered = [
        game for game in games
        if main_platform.lower() in game["main_platform"].lower()
    ]

    # Si la lista esta vacia - plataforma invalida o sin juegos
    if not filtered:
        response = {
            "status": "error",
            "message": f"No se encontraron juegos para la plataforma: {main_platform}"
        },404
    else:
        response = jsonify(filtered),200
    
    return response

#POST agregar un Elemento
@app.route('/api/games/', methods=['POST'])
def add_game():
    global next_id
    
    #obtiene el JSON enviado en el cuerpo de la peticion
    new_game_data = request.get_json()
    
    required = ["title", "genre", "score", "main_platform", "coop"]

    #Verifica que new_game_data no sea None y que CADA elemento de la lista 'required' exista como clave en new_game_data
    if not new_game_data or not all(field in new_game_data for field in required):
        return jsonify({
            "status": "error",
            "message": f"Datos de juego invalidos. Se requieren todos estos campos: {', '.join(required)}."
        }), 400
    
    #crear el nuevo objeto juego
    new_game = {
        "id": next_id,
        "title": new_game_data.get("title"),
        "genre": new_game_data.get("genre"),
        "score": new_game_data.get("score"),
        "main_platform": new_game_data.get("main_platform"),
        "coop": new_game_data.get("coop")
    }
    
    #Agregar el juego a la lista
    games.append(new_game)
    # Incrementar el ID para el proximo
    next_id += 1
    
    return jsonify({
        "message": "Juego agregado exitosamente",
        "game": new_game
    }), 201 # 201 Created

#UPDATE (Modificar un elemento existente)
#Metodo PUT en la misma ruta del GET individual, ejemplo /api/games/12/
@app.route('/api/games/<int:game_id>/', methods=['PUT'])
def update_game(game_id):
    global games

    # Buscar el juego por ID
    game = next((g for g in games if g["id"] == game_id), None)

    if not game:
        return jsonify({"message": f"Juego con ID {game_id} no encontrado"}), 404

    # Obtener campos enviados en el body (JSON)
    update_data = request.get_json()

    if not update_data:
        return jsonify({
            "status": "error",
            "message": "Debes enviar al menos un campo para actualizar."
        }), 400

    # Actualizar solo los campos enviados
    for key, value in update_data.items():
        if key in game:   # Solo si el campo existe en el juego
            game[key] = value

    return jsonify({
        "message": f"Juego con ID {game_id} actualizado correctamente",
        "updated_game": game
    }), 200

#DELETE (Eliminar un Elemento)
# Ruta: /api/games/3/
@app.route('/api/games/<int:game_id>/', methods=['DELETE'])
def delete_game(game_id):
    global games
    global next_id
    
    # Encontrar el índice del juego
    game_index = next((i for i, g in enumerate(games) if g["id"] == game_id), -1)

    if game_index != -1:
        # Eliminar el juego de la lista
        deleted_game = games.pop(game_index)
        
        return jsonify({
            "message": f"Juego con ID {game_id} eliminado exitosamente",
            "deleted": deleted_game
        }), 200
    else:
        return jsonify({"message": f"No se pudo eliminar. Juego con ID {game_id} no encontrado"}), 404

# Parte del usuario
users = [
            {
                'user_id': 'user-1',
                'username': 'user-admin',
                'role': 'admin',
                'password_hash': generate_password_hash('user-admin-123'),
                'created_at': datetime.now()
            },
               {
                'user_id': 'user-1',
                'username': 'user-manager',
                'role': 'manager',
                'password_hash': generate_password_hash('user-mager-123'),
                'created_at': datetime.now()
            },
        ]

def get_users_by_username(username):
    return list(filter(lambda u: u["username"]== username, users))

def authenticate_user(username, password):
    users  = get_users_by_username(username)
    print(f"users found: {users}, with username : {username}" )
    if len(users)<= 0 or not check_password_hash(users[0]['password_hash'], password):
        return None, False
    else:
        return users[0], True
   
@app.route('/api/signIn', methods= ['POST'])
def sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({
            'error': 'Datos inválidos',
            'message': 'Se requieren username y password'
        }), 400
    username = request.json['username']
    password = request.json['password']
    if len(get_users_by_username(username) ) >0:
        return  jsonify({
            'error': 'Nombre de usuario ya existe'
        }), 400
    user_id = 'user-'+str(uuid.uuid4())
    users.append({
                'user_id': user_id,
                'username': username,
                'role': 'client',
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now()
            })
    return {
        'username': username,
        'user_id': user_id
    }, 201

    
@app.route('/api/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({
            'error': 'Datos inválidos',
            'message': 'Se requieren username y password'
        }), 400
        
    username = request.json['username']
    password = request.json['password']
    user, auth_result = authenticate_user(username,password)
    if auth_result:
        user_id = user.get('user_id') 
        token = create_access_token(identity=username,additional_claims={
            'user_id': user_id,
            'role': user["role"]
        })
        return {"message": "login success", "access_token": token}, 200
    else:
        return {"message": "Not authorized"}, 401
    

    
# Lo que levanta el servidor
if __name__ == '__main__':
    # Asegúrate de usar un puerto que no esté en uso, 8001 está bien
    app.run(debug=True, port=8001)
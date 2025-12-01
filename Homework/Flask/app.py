from flask import Flask, request, jsonify
# Flask: la clase principal para crear la aplicación web
# request: un objeto que te permite leer datos enviados por el cliente (JSON, query params, headers, formularios, etc)
# jsonify: una función que convierte listas/diccionarios de Python en una respuesta JSON válida para enviar al navegador

app = Flask(__name__)

@app.route('/')
def home():
    return  "<h1 style='color:cyan;'> Bienvenido! </h1>" \
            "<h2> Buscador de Videojuegos </h2>" 

@app.route('/api/')
def get_api():
    return "<h2> Recomendaciones por plataforma de videojuegos </h2>" 

# REST ENDPOINTS
games = [
    {"title": "Portal","genre": "First-person puzzle","score": 90,"main_platform": "PC","coop": False},
    {"title": "Portal 2","genre": "First-person puzzle","score": 95,"main_platform": "PC","coop": True},
    {"title": "Super Mario Bros 3","genre": "Platformer","score": 97,"main_platform": "Nintendo","coop": False},
    {"title": "Red Dead Redemption","genre": "Action / Open world","score": 95,"main_platform": "Consoles","coop": False},
    {"title": "Superliminal","genre": "Puzzle","score": 75,"main_platform": "PC","coop": False},
    {"title": "Cult of the Lamb","genre": "Action / Management","score": 85,"main_platform": "PC / Switch","coop": True},
    {"title": "Baldur's Gate 3","genre": "Tactical RPG","score": 98,"main_platform": "PC","coop": True},
    {"title": "Titanfall 2","genre": "Shooter","score": 90,"main_platform": "PC / Consoles","coop": False},
    {"title": "The Stanley Parable","genre": "Narrative exploration","score": 89,"main_platform": "PC","coop": False},
    {"title": "Killer Frequency","genre": "Narrative horror","score": 80,"main_platform": "PC","coop": False},
    {"title": "Metal: Hellsinger","genre": "Rhythm shooter","score": 90,"main_platform": "PC","coop": False},
    {"title": "Cuphead","genre": "Platformer / Boss rush","score": 88,"main_platform": "PC / Xbox / Switch","coop": True},
    {"title": "Sonic Mania","genre": "Platformer","score": 90,"main_platform": "Switch / PC / PS4","coop": True},
    {"title": "Detroit: Become Human","genre": "Narrative adventure","score": 95,"main_platform": "PlayStation / PC","coop": False},
    {"title": "Coffee Talk","genre": "Visual novel","score": 80,"main_platform": "PC / Switch","coop": False},
    {"title": "Dispatch","genre": "Horror / Thriller","score": 80,"main_platform": "PC","coop": False}
]


@app.route('/api/games/')
def get_games():
    return jsonify(games)

@app.route('/api/games/<string:main_platform>/')
def get_platform(main_platform):

    # FILTRAMOS LOS JUEGOS POR PLATFORMA
    filtered = [
        game for game in games #ELEMENTO_A_GUARDAR for VARIABLE in LISTA
        if main_platform.lower() in game["main_platform"].lower() #.lower(): convierte todo a minusculas
    ]

    # Si la lista está vacía - plataforma invalida o sin juegos
    if not filtered:
        response = {
            "status": "error",
            "message": f"No se encontraron juegos para la plataforma: {main_platform}"
        },404
    else:
        response = jsonify(filtered),200
    
    return response

if __name__ == '__main__':
    app.run(debug=True,port=8001)
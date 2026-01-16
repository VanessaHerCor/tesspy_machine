import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_app.settings')
import django
django.setup()

from dynamicpages.models import Videogame
from datetime import datetime

# Crear videojuegos de ejemplo
games_data = [
    {
        'title': 'Portal',
        'genre': 'First-person puzzle',
        'score': 90,
        'main_platform': 'PC',
        'coop': False,
        'developer': 'Valve',
        'description': 'Un juego de acertijos de primer grado donde usas un arma de portal para resolver puzzles complejos.'
    },
    {
        'title': 'The Legend of Zelda: Breath of the Wild',
        'genre': 'Action-Adventure',
        'score': 97,
        'main_platform': 'Nintendo Switch',
        'coop': False,
        'developer': 'Nintendo',
        'description': 'Una aventura épica en el reino de Hyrule con total libertad de exploración.'
    },
    {
        'title': 'Elden Ring',
        'genre': 'Action RPG',
        'score': 96,
        'main_platform': 'PC/PlayStation/Xbox',
        'coop': True,
        'developer': 'FromSoftware',
        'description': 'Un desafiante RPG de acción con un mundo vasto y secretos por descubrir.'
    },
    {
        'title': 'Hades',
        'genre': 'Roguelike',
        'score': 93,
        'main_platform': 'PC/Nintendo Switch',
        'coop': False,
        'developer': 'Supergiant Games',
        'description': 'Un roguelike viciado con narrativa excepcional y mecánicas pulidas.'
    },
    {
        'title': 'Among Us',
        'genre': 'Social Deduction',
        'score': 75,
        'main_platform': 'PC/Mobile',
        'coop': True,
        'developer': 'Innersloth',
        'description': 'Un juego multijugador donde encuentras al impostor entre tripulantes.'
    },
]

# Eliminar juegos existentes y crear nuevos
Videogame.objects.delete()

for game_data in games_data:
    game = Videogame(**game_data)
    game.save()
    print(f'✅ Creado: {game.title} - Puntuación: {game.score}')

print(f'\n📊 Total de videojuegos: {Videogame.objects.count()}')

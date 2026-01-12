from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField
from datetime import datetime

class Videogame(Document):
    """Modelo de videojuego - se guarda en MongoDB"""
    title = StringField(max_length=200, required=True)
    genre = StringField(required=True)
    score = IntField(required=True)  # Puntuación de 0 a 100
    main_platform = StringField(max_length=100, required=True)
    coop = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    description = StringField()  # Descripción adicional del juego
    developer = StringField(max_length=200)  # Desarrollador del juego
    
    meta = {
        'collection': 'videogames',  # Nombre de la colección en MongoDB
        'ordering': ['-score']  # Ordenar por puntuación descendente
    }
    
    def __str__(self):
        return f"{self.title} - {self.genre}"
    
    def get_rating_stars(self):
        """Convierte la puntuación a estrellas (0-5)"""
        return round(self.score / 20)

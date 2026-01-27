"""
Módulo de configuración del juego

Facilita la importación de colores y características

Uso:
    from configuracion.config import colores
    from configuracion.config import caracteristicas
    
    # O más simple:
    from configuracion.config.colores import *
    from configuracion.config.caracteristicas import *
"""

# Importar todos los colores
from .colores import *

# Importar todas las características
from .caracteristicas import *

# Esto permite hacer:
# from configuracion.config import NEGRO, BLANCO, ANCHO_DEFAULT

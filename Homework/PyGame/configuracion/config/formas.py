"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        FORMAS Y FIGURAS DEL JUEGO                         ║
║                                                                            ║
║  Aquí se definen todas las funciones para dibujar diferentes formas       ║
║  de los objetos del juego (enemigo, jugador, moneda, etc.)                ║
║                                                                            ║
║  VENTAJAS de dibujar formas vs sprites:                                   ║
║  ✓ Sin peso de archivos (más rápido de cargar)                            ║
║  ✓ Escalan perfectamente a cualquier tamaño                               ║
║  ✓ Animaciones suaves con transformaciones                                ║
║  ✗ Menos detalles visuales                                                ║
║                                                                            ║
║  VENTAJAS de sprites (imágenes):                                          ║
║  ✓ Mucho más detalle visual                                               ║
║  ✓ Artistas pueden crear gráficos hermosos                                ║
║  ✗ Más pesado en memoria                                                  ║
║  ✗ Menos flexible al escalar                                              ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame
import math

# ════════════════════════════════════════════════════════════════════════════
# FORMAS SIMPLES - ENEMIGOS
# ════════════════════════════════════════════════════════════════════════════

def dibujar_enemigo_circulo(pantalla, rect, color):
    """Dibuja el enemigo como un círculo con borde"""
    centro_x = rect.centerx
    centro_y = rect.centery
    radio = rect.width // 2
    pygame.draw.circle(pantalla, color, (centro_x, centro_y), radio)
    pygame.draw.circle(pantalla, (255, 255, 255), (centro_x, centro_y), radio, 2)

def dibujar_enemigo_triangulo(pantalla, rect, color):
    """Dibuja el enemigo como un triángulo apuntando hacia arriba"""
    puntos = [
        (rect.centerx, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ]
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)

def dibujar_enemigo_estrella(pantalla, rect, color):
    """Dibuja el enemigo como una estrella de 5 puntas"""
    centro_x = rect.centerx
    centro_y = rect.centery
    radio_externo = rect.width // 2
    radio_interno = radio_externo // 2.5
    
    puntos = []
    for i in range(10):
        angulo = (i * math.pi) / 5 - math.pi / 2
        if i % 2 == 0:
            radio = radio_externo
        else:
            radio = radio_interno
        
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        puntos.append((x, y))
    
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)

def dibujar_enemigo_diamante(pantalla, rect, color):
    """Dibuja el enemigo como un diamante/rombo"""
    puntos = [
        (rect.centerx, rect.top),
        (rect.right, rect.centery),
        (rect.centerx, rect.bottom),
        (rect.left, rect.centery)
    ]
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)

def dibujar_enemigo_hexagono(pantalla, rect, color):
    """Dibuja el enemigo como un hexágono"""
    centro_x = rect.centerx
    centro_y = rect.centery
    radio = rect.width // 2
    
    puntos = []
    for i in range(6):
        angulo = (i * math.pi) / 3
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        puntos.append((x, y))
    
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)

# ════════════════════════════════════════════════════════════════════════════
# FORMAS COMPLEJAS - DISEÑOS DETALLADOS
# ════════════════════════════════════════════════════════════════════════════

def dibujar_enemigo_nave(pantalla, rect, color):
    """
    Dibuja el enemigo como una nave espacial (más detallado)
    Esto demuestra cómo hacer diseños complejos sin sprites
    """
    cx = rect.centerx
    cy = rect.centery
    w = rect.width
    h = rect.height
    
    # Cuerpo principal (triángulo grande)
    puntos_cuerpo = [
        (cx, cy - h//3),      # Punta delantera
        (cx - w//3, cy + h//3),   # Abajo izquierda
        (cx + w//3, cy + h//3)    # Abajo derecha
    ]
    pygame.draw.polygon(pantalla, color, puntos_cuerpo)
    
    # Ventana (pequeño círculo en la punta)
    pygame.draw.circle(pantalla, (255, 255, 100), (cx, cy - h//6), w//8)
    
    # Alas/aletas (dos líneas laterales)
    pygame.draw.line(pantalla, color, (cx - w//3, cy), (cx - w//2, cy + h//4), 2)
    pygame.draw.line(pantalla, color, (cx + w//3, cy), (cx + w//2, cy + h//4), 2)
    
    # Borde del cuerpo
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos_cuerpo, 2)

def dibujar_enemigo_robot(pantalla, rect, color):
    """
    Dibuja el enemigo como un robot (cuadrado con detalles)
    Ejemplo de cómo agregar expresión a un cuadrado
    """
    # Cuerpo
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
    
    # Ojos (dos círculos)
    ojo_size = rect.width // 8
    ojo_y = rect.top + rect.height // 3
    pygame.draw.circle(pantalla, (255, 255, 0), (rect.left + rect.width // 3, ojo_y), ojo_size)
    pygame.draw.circle(pantalla, (255, 255, 0), (rect.right - rect.width // 3, ojo_y), ojo_size)
    
    # Pupila (negro dentro del ojo)
    pygame.draw.circle(pantalla, (0, 0, 0), (rect.left + rect.width // 3, ojo_y), ojo_size // 2)
    pygame.draw.circle(pantalla, (0, 0, 0), (rect.right - rect.width // 3, ojo_y), ojo_size // 2)
    
    # Boca (línea)
    boca_y = rect.bottom - rect.height // 4
    pygame.draw.line(pantalla, (255, 255, 255), 
                     (rect.left + rect.width // 4, boca_y),
                     (rect.right - rect.width // 4, boca_y), 3)

def dibujar_enemigo_dragon(pantalla, rect, color):
    """
    Dibuja el enemigo como un dragón (cuerpo + cabeza + cola)
    Ejemplo avanzado de formas múltiples combinadas
    """
    cx = rect.centerx
    cy = rect.centery
    w = rect.width
    h = rect.height
    
    # Cuerpo (rectángulo redondeado)
    cuerpo_rect = pygame.Rect(cx - w//3, cy - h//4, w*0.6, h//2)
    pygame.draw.rect(pantalla, color, cuerpo_rect)
    
    # Cabeza (círculo)
    pygame.draw.circle(pantalla, color, (cx + w//2, cy - h//4), w//5)
    
    # Ojos (dos pequeños círculos blancos)
    pygame.draw.circle(pantalla, (255, 255, 255), (cx + w//2 + w//8, cy - h//4 - w//10), w//15)
    pygame.draw.circle(pantalla, (255, 255, 255), (cx + w//2 + w//8, cy - h//4 + w//10), w//15)
    
    # Cola (línea larga y curva)
    cola_start = (cx - w//3, cy)
    cola_end = (cx - w//2 - 10, cy + h//3)
    pygame.draw.line(pantalla, color, cola_start, cola_end, 3)
    
    # Aletas (líneas diagonales en el cuerpo)
    pygame.draw.line(pantalla, color, (cx - w//6, cy + h//8), (cx - w//6, cy + h//4), 2)
    pygame.draw.line(pantalla, color, (cx + w//6, cy + h//8), (cx + w//6, cy + h//4), 2)
    
    # Borde general
    pygame.draw.rect(pantalla, (255, 255, 255), cuerpo_rect, 2)
    pygame.draw.circle(pantalla, (255, 255, 255), (cx + w//2, cy - h//4), w//5, 2)

# ════════════════════════════════════════════════════════════════════════════
# FORMAS PARA JUGADOR
# ════════════════════════════════════════════════════════════════════════════

def dibujar_jugador_nave(pantalla, rect, color):
    """Dibuja el jugador como una nave (simplificada)"""
    puntos = [
        (rect.centerx, rect.top),
        (rect.right, rect.bottom),
        (rect.centerx + rect.width//4, rect.centery),
        (rect.centerx, rect.bottom - rect.height//3),
        (rect.centerx - rect.width//4, rect.centery),
        (rect.left, rect.bottom)
    ]
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 1)

# ════════════════════════════════════════════════════════════════════════════
# FORMAS PARA MONEDA
# ════════════════════════════════════════════════════════════════════════════

def dibujar_moneda_estrella(pantalla, rect, color):
    """Dibuja la moneda como una estrella pequeña"""
    centro_x = rect.centerx
    centro_y = rect.centery
    radio_externo = rect.width // 2
    radio_interno = radio_externo // 2.5
    
    puntos = []
    for i in range(10):
        angulo = (i * math.pi) / 5 - math.pi / 2
        if i % 2 == 0:
            radio = radio_externo
        else:
            radio = radio_interno
        
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        puntos.append((x, y))
    
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 1)

def dibujar_moneda_corazon(pantalla, rect, color):
    """Dibuja la moneda como un corazón ❤️"""
    cx = rect.centerx
    cy = rect.centery
    s = rect.width // 2
    
    # Dos semicírculos en la parte superior
    pygame.draw.circle(pantalla, color, (cx - s//2, cy - s//3), s//2)
    pygame.draw.circle(pantalla, color, (cx + s//2, cy - s//3), s//2)
    
    # Triángulo en la parte inferior
    puntos = [
        (cx - s, cy + s//2),
        (cx + s, cy + s//2),
        (cx, cy + s)
    ]
    pygame.draw.polygon(pantalla, color, puntos)

def dibujar_moneda_gema(pantalla, rect, color):
    """Dibuja la moneda como una gema/cristal"""
    cx = rect.centerx
    cy = rect.centery
    
    puntos = [
        (cx, rect.top),           # Punta arriba
        (rect.right, cy - rect.height//4),
        (rect.right, cy + rect.height//4),
        (cx, rect.bottom),        # Punta abajo
        (rect.left, cy + rect.height//4),
        (rect.left, cy - rect.height//4)
    ]
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)

# ════════════════════════════════════════════════════════════════════════════
# DICCIONARIO DE FORMAS (fácil de usar)
# ════════════════════════════════════════════════════════════════════════════

FORMAS_ENEMIGO = {
    'cuadrado': lambda p, r, c: pygame.draw.rect(p, c, r),
    'circulo': dibujar_enemigo_circulo,
    'triangulo': dibujar_enemigo_triangulo,
    'estrella': dibujar_enemigo_estrella,
    'diamante': dibujar_enemigo_diamante,
    'hexagono': dibujar_enemigo_hexagono,
    'nave': dibujar_enemigo_nave,
    'robot': dibujar_enemigo_robot,
    'dragon': dibujar_enemigo_dragon,
}

FORMAS_JUGADOR = {
    'cuadrado': lambda p, r, c: pygame.draw.rect(p, c, r),
    'circulo': lambda p, r, c: (
        pygame.draw.circle(p, c, (r.centerx, r.centery), r.width // 2),
        pygame.draw.circle(p, (255, 255, 255), (r.centerx, r.centery), r.width // 2, 2)
    ),
    'nave': dibujar_jugador_nave,
}

FORMAS_MONEDA = {
    'cuadrado': lambda p, r, c: pygame.draw.rect(p, c, r),
    'circulo': lambda p, r, c: (
        pygame.draw.circle(p, c, (r.centerx, r.centery), r.width // 2),
        pygame.draw.circle(p, (255, 255, 255), (r.centerx, r.centery), r.width // 2, 2)
    ),
    'estrella': dibujar_moneda_estrella,
    'corazon': dibujar_moneda_corazon,
    'gema': dibujar_moneda_gema,
}

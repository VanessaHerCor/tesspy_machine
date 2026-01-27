"""
╔════════════════════════════════════════════════════════════════════════════╗
║          JUEGO PYGAME PROFESIONAL - RECOGEDOR DE MONEDAS                  ║
║                                                                            ║
║  ESTRUCTURA MODULAR - CÓDIGO ORGANIZADO                                   ║
║                                                                            ║
║  Este archivo demuestra cómo usar la estructura de carpetas               ║
║  profesional que creaste                                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame
import random

# ════════════════════════════════════════════════════════════════════════════
# IMPORTAR CONFIGURACIÓN DESDE TUS MÓDULOS
# ════════════════════════════════════════════════════════════════════════════

# Importar TODOS los colores desde tu módulo de colores
from configuracion.config.colores import *

# Importar características desde tu módulo de características
from configuracion.config.caracteristicas import (
    RESOLUCION_DEFAULT,
    ANCHO_DEFAULT,
    ALTO_DEFAULT,
    FPS,
    TAMAÑO_FUENTE_TITULO,
    TAMAÑO_FUENTE_SUBTITULO,
    TAMAÑO_FUENTE_NORMAL,
    crear_ventana,
    crear_objetos_adaptativos,
    RUTA_SONIDO_MONEDA,
    calcular_escala,
    actualizar_fuentes_dinamicas,
    actualizar_objetos_dinamicos,
)

# Importar formas desde tu módulo de formas
from configuracion.config.formas import FORMAS_ENEMIGO, FORMAS_JUGADOR, FORMAS_MONEDA

# ════════════════════════════════════════════════════════════════════════════
# INICIALIZAR PYGAME
# ════════════════════════════════════════════════════════════════════════════

pygame.init()
pygame.mixer.init()

# ════════════════════════════════════════════════════════════════════════════
# CREAR VENTANA USANDO TU FUNCIÓN
# ════════════════════════════════════════════════════════════════════════════

pantalla = crear_ventana(RESOLUCION_DEFAULT, pantalla_completa=False)
pygame.display.set_caption("🎮 Juego Modular Profesional")
clock = pygame.time.Clock()

# ════════════════════════════════════════════════════════════════════════════
# CARGAR SONIDO
# ════════════════════════════════════════════════════════════════════════════

try:
    sonido_moneda = pygame.mixer.Sound(RUTA_SONIDO_MONEDA)
except:
    sonido_moneda = None
    print("⚠️ Sonido no encontrado, continuando sin audio")

# ════════════════════════════════════════════════════════════════════════════
# CREAR OBJETOS USANDO TU FUNCIÓN
# ════════════════════════════════════════════════════════════════════════════

objetos = crear_objetos_adaptativos(pantalla)
jugador = objetos['jugador']
moneda = objetos['moneda']
enemigo = objetos['enemigo']
velocidad_jugador = objetos['velocidad_jugador']
velocidad_enemigo = objetos['velocidad_enemigo']

# Velocidades del enemigo (para rebote)
velocidad_enemigo_x = velocidad_enemigo
velocidad_enemigo_y = velocidad_enemigo

# ════════════════════════════════════════════════════════════════════════════
# VARIABLES DE JUEGO
# ════════════════════════════════════════════════════════════════════════════

score = 0
sonido_activado = True
escala_actual = 1.0

# ← NUEVO: Guardar tamaño de ventana para detectar cambios
ancho_anterior = ANCHO_DEFAULT
alto_anterior = ALTO_DEFAULT

# ════════════════════════════════════════════════════════════════════════════
# CREAR FUENTES (usando tus tamaños definidos)
# ════════════════════════════════════════════════════════════════════════════

fuente_grande = pygame.font.Font(None, TAMAÑO_FUENTE_TITULO)
fuente_mediana = pygame.font.Font(None, TAMAÑO_FUENTE_SUBTITULO)
fuente_pequeña = pygame.font.Font(None, TAMAÑO_FUENTE_NORMAL)

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE FORMAS
# ════════════════════════════════════════════════════════════════════════════

# Elige la forma de cada objeto (ver opciones en configuracion/config/formas.py)
FORMA_ENEMIGO = "dragon"      # Opciones: cuadrado, circulo, triangulo, estrella, diamante, hexagono, nave, robot, dragon
FORMA_JUGADOR = "nave"        # Opciones: cuadrado, circulo, nave
FORMA_MONEDA = "gema"         # Opciones: cuadrado, circulo, estrella, corazon, gema

def respawn_moneda():
    """Coloca la moneda en una posición aleatoria"""
    rect = pantalla.get_rect()
    moneda.x = random.randint(0, max(rect.width - moneda.width, 0))
    moneda.y = random.randint(0, max(rect.height - moneda.height, 0))

def reproducir_sonido():
    """Reproduce sonido de moneda si está activado"""
    if sonido_activado and sonido_moneda:
        sonido_moneda.play()

# ════════════════════════════════════════════════════════════════════════════
# CICLO PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

running = True

while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ← NUEVO: Detectar cambio de tamaño de ventana
        elif event.type == pygame.VIDEORESIZE:
            # Actualizar la pantalla con el nuevo tamaño
            pantalla = pygame.display.set_mode(
                (event.w, event.h), 
                pygame.RESIZABLE
            )
            
            # Usar función desde config para mantener posiciones exactas
            resultado = actualizar_objetos_dinamicos(
                pantalla, 
                ancho_anterior, 
                alto_anterior,
                {
                    'jugador': jugador,
                    'moneda': moneda,
                    'enemigo': enemigo
                },
                {
                    'velocidad_enemigo_x': velocidad_enemigo_x,
                    'velocidad_enemigo_y': velocidad_enemigo_y
                }
            )
            
            # Actualizar objetos y velocidades
            jugador.update(resultado['jugador'])
            moneda.update(resultado['moneda'])
            enemigo.update(resultado['enemigo'])
            velocidad_jugador = resultado['velocidad_jugador']
            velocidad_enemigo = resultado['velocidad_enemigo']
            velocidad_enemigo_x = resultado['velocidad_enemigo_x']
            velocidad_enemigo_y = resultado['velocidad_enemigo_y']
            escala_actual = resultado['escala_actual']
            
            # Actualizar fuentes también
            fuentes = actualizar_fuentes_dinamicas(
                escala_actual,
                TAMAÑO_FUENTE_TITULO,
                TAMAÑO_FUENTE_SUBTITULO,
                TAMAÑO_FUENTE_NORMAL
            )
            fuente_grande = fuentes['fuente_grande']
            fuente_mediana = fuentes['fuente_mediana']
            fuente_pequeña = fuentes['fuente_pequeña']
            
            # Guardar nuevo tamaño como anterior para el próximo resize
            ancho_anterior = event.w
            alto_anterior = event.h
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Obtener dimensiones actuales
    rect = pantalla.get_rect()
    ancho_actual = rect.width
    alto_actual = rect.height
    
    # MOVIMIENTO DEL JUGADOR
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        jugador.x -= velocidad_jugador
    if keys[pygame.K_RIGHT]:
        jugador.x += velocidad_jugador
    if keys[pygame.K_UP]:
        jugador.y -= velocidad_jugador
    if keys[pygame.K_DOWN]:
        jugador.y += velocidad_jugador
    
    # Mantener jugador dentro de la pantalla
    if jugador.x < 0:
        jugador.x = 0
    if jugador.x > ancho_actual - jugador.width:
        jugador.x = ancho_actual - jugador.width
    if jugador.y < 0:
        jugador.y = 0
    if jugador.y > alto_actual - jugador.height:
        jugador.y = alto_actual - jugador.height
    
    # MOVIMIENTO DEL ENEMIGO
    enemigo.x += velocidad_enemigo_x
    enemigo.y += velocidad_enemigo_y
    
    # REBOTE DEL ENEMIGO
    if enemigo.x <= 0 or enemigo.x >= ancho_actual - enemigo.width:
        velocidad_enemigo_x *= -1
    if enemigo.y <= 0 or enemigo.y >= alto_actual - enemigo.height:
        velocidad_enemigo_y *= -1
    
    # Mantener enemigo dentro de la pantalla
    if enemigo.x < 0:
        enemigo.x = 0
    if enemigo.x > ancho_actual - enemigo.width:
        enemigo.x = ancho_actual - enemigo.width
    if enemigo.y < 0:
        enemigo.y = 0
    if enemigo.y > alto_actual - enemigo.height:
        enemigo.y = alto_actual - enemigo.height
    
    # COLISIONES
    if jugador.colliderect(moneda):
        score += 1
        reproducir_sonido()
        respawn_moneda()
    
    if jugador.colliderect(enemigo):
        print(f"💥 Game Over! Puntuación: {score}")
        running = False
    
    # ────────────────────────────────────────────────────────────────────────
    # DIBUJAR TODO
    # ────────────────────────────────────────────────────────────────────────
    
    # Fondo negro (usando tu color importado)
    pantalla.fill(NEGRO)
    
    # Dibujar objetos usando formas desde config
    if FORMA_JUGADOR in FORMAS_JUGADOR:
        FORMAS_JUGADOR[FORMA_JUGADOR](pantalla, jugador, VERDE)
    else:
        pygame.draw.rect(pantalla, VERDE, jugador)
    
    if FORMA_MONEDA in FORMAS_MONEDA:
        FORMAS_MONEDA[FORMA_MONEDA](pantalla, moneda, AMARILLO)
    else:
        pygame.draw.rect(pantalla, AMARILLO, moneda)
    
    if FORMA_ENEMIGO in FORMAS_ENEMIGO:
        FORMAS_ENEMIGO[FORMA_ENEMIGO](pantalla, enemigo, ROJO)
    else:
        pygame.draw.rect(pantalla, ROJO, enemigo)
    
    # Dibujar puntuación (usando tu color importado)
    texto_score = fuente_pequeña.render(f"Score: {score}", True, BLANCO)
    pantalla.blit(texto_score, (10, 10))
    
    # Instrucciones
    texto_ayuda = fuente_pequeña.render("ESC: Salir", True, LIGHT_GRAY)
    pantalla.blit(texto_ayuda, (10, 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS (usando tu configuración)
    clock.tick(FPS)

# ════════════════════════════════════════════════════════════════════════════
# CERRAR JUEGO
# ════════════════════════════════════════════════════════════════════════════

pygame.quit()
print(f"🎮 Juego terminado. Puntuación final: {score}")
print("✨ Gracias por jugar!")

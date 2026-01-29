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
    RESOLUCIONES_LISTA,
    ANCHO_DEFAULT,
    ALTO_DEFAULT,
    FPS,
    TAMAÑO_FUENTE_TITULO,
    TAMAÑO_FUENTE_SUBTITULO,
    TAMAÑO_FUENTE_NORMAL,
    crear_ventana,
    crear_objetos_adaptativos,
    calcular_escala
)

# Importar enemigo y jugador animados desde sprites
from configuracion.config.sprites_animados import EnemigoDinamico, JugadorDinamico, MonedaDinamica

# Importar pantallas y menús
from configuracion.config.pantallas import (
    pantalla_titulo, 
    pantalla_instrucciones,
    pantalla_game_over, 
    pantalla_respawn,
    crear_fuentes_escaladas,
    inicializar_resolucion_global,
    get_pantalla_actual
)

# Importar sistema de sonidos
from configuracion.config.sonidos import (
    inicializar_audio,
    cargar_sonidos,
    cargar_musica_fondo,
    iniciar_musica_fondo,
    detener_musica_fondo,
    pausar_musica_fondo,
    reanudar_musica_fondo,
    reproducir_sonido_moneda,
    reproducir_sonido_failed,
    reproducir_sonido_game_over,
    detener_todos_sonidos
)

# Importar sistema de Inteligencia Artificial
from configuracion.config.inteligencia_artificial import crear_enemigo_inteligente

# ════════════════════════════════════════════════════════════════════════════
# INICIALIZAR PYGAME Y AUDIO
# ════════════════════════════════════════════════════════════════════════════════

pygame.init()
inicializar_audio()

# Cargar todos los sonidos
sonidos = cargar_sonidos()
musica_cargada = cargar_musica_fondo()

# ════════════════════════════════════════════════════════════════════════════
# CREAR FUENTES PARA MENÚS (importada desde pantallas.py)
# ════════════════════════════════════════════════════════════════════════════

fuentes = crear_fuentes_escaladas(RESOLUCION_DEFAULT[0])
fuente_grande = fuentes['grande']
fuente_mediana = fuentes['mediana']
fuente_pequeña = fuentes['pequeña']

# ════════════════════════════════════════════════════════════════════════════
# CREAR VENTANA INICIAL CENTRADA
# ════════════════════════════════════════════════════════════════════════════

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # ← Centrar ventana en la pantalla

pantalla = crear_ventana(RESOLUCION_DEFAULT, pantalla_completa=False)
pygame.display.set_caption("🔮 Ladron de Magia")
clock = pygame.time.Clock()

# INICIALIZAR SISTEMA CENTRALIZADO DE RESOLUCIÓN
inicializar_resolucion_global(pantalla)

# Resolución inicial fija
resolucion_actual = RESOLUCION_DEFAULT

# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE TÍTULO CON OPCIONES
# ════════════════════════════════════════════════════════════════════════════

# Usar la pantalla del sistema centralizado
pantalla = get_pantalla_actual()
resultado = pantalla_titulo(pantalla, fuente_grande, fuente_mediana)
if resultado[0] == 'salir':
    pygame.quit()
    print("¡Gracias por jugar!")
    exit()

# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE INSTRUCCIONES
# ════════════════════════════════════════════════════════════════════════════

ruta_sprites_aux = os.path.join(os.path.dirname(__file__), 'configuracion', 'sprites')
pantalla = get_pantalla_actual()  # Usar pantalla centralizada
if not pantalla_instrucciones(pantalla, fuente_mediana, ruta_sprites_aux):
    pygame.quit()
    print("¡Gracias por jugar!")
    exit()

# ════════════════════════════════════════════════════════════════════════════
# INICIAR MÚSICA DE FONDO
# ════════════════════════════════════════════════════════════════════════════

if musica_cargada:
    iniciar_musica_fondo()

# ════════════════════════════════════════════════════════════════════════════
# CREAR OBJETOS DEL JUEGO
# ════════════════════════════════════════════════════════════════════════════

pantalla = get_pantalla_actual()  # Asegurar pantalla actualizada
objetos = crear_objetos_adaptativos(pantalla)
jugador_rect = objetos['jugador']
moneda = objetos['moneda']
enemigo_rect = objetos['enemigo']
velocidad_jugador = objetos['velocidad_jugador']
velocidad_enemigo = objetos['velocidad_enemigo']

# Crear objetos animados con sprites
import os
ruta_sprites = os.path.join(os.path.dirname(__file__), 'configuracion', 'sprites')
jugador = JugadorDinamico(jugador_rect, ruta_sprites)
enemigo = EnemigoDinamico(enemigo_rect, ruta_sprites)

# Crear moneda animada
moneda = MonedaDinamica(moneda, ruta_sprites)

# Función para actualizar sprites cuando cambie la resolución
def actualizar_sprites_resolucion():
    """Actualiza todos los sprites cuando cambia la resolución"""
    print("🔄 Actualizando sprites para nueva resolución")
    jugador.forzar_actualizacion_resolucion()
    enemigo.forzar_actualizacion_resolucion()
    moneda.forzar_actualizacion_resolucion()

print("✅ Sprites configurados con sistema centralizado de resolución")

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURAR INTELIGENCIA ARTIFICIAL DEL ENEMIGO
# ════════════════════════════════════════════════════════════════════════════

# Opción 1: Red Neuronal
# enemigo_ia = crear_enemigo_inteligente("neuronal", velocidad_enemigo)

# Opción 2: Persecución Inteligente
# enemigo_ia = crear_enemigo_inteligente("basica", velocidad_enemigo)

# Opción 3: Patrones Aleatorios
enemigo_ia = crear_enemigo_inteligente("patrones", velocidad_enemigo)

# Opción 4: Híbrida
# enemigo_ia = crear_enemigo_inteligente("hibrida", velocidad_enemigo)

# Crear IA para el enemigo (Red Neuronal - Aprende durante el juego)
# enemigo_ia = crear_enemigo_inteligente("neuronal", velocidad_enemigo)
print("🧠 Red Neuronal cargada - El enemigo APRENDERÁ durante el juego")

# Variables para tracking de posición del jugador
posicion_anterior_jugador = (jugador.rect.x, jugador.rect.y)
tiempo_juego = 0

# Velocidades del enemigo (ya no usamos rebote simple)
velocidad_enemigo_x = 0  # Ahora controlado por IA
velocidad_enemigo_y = 0  # Ahora controlado por IA

# ════════════════════════════════════════════════════════════════════════════
# VARIABLES DE JUEGO
# ════════════════════════════════════════════════════════════════════════════

score = 0
vidas = 5  # Sistema de vidas
posicion_respawn_jugador = (jugador.rect.x, jugador.rect.y)  # Posición inicial para respawn
resolucion_actual = RESOLUCION_DEFAULT

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN PARA RESPAWN DE MONEDA
# ════════════════════════════════════════════════════════════════════════════

def respawn_moneda():
    """Coloca la moneda en una posición aleatoria"""
    rect = pantalla.get_rect()
    moneda.x = random.randint(0, max(rect.width - moneda.width, 0))
    moneda.y = random.randint(0, max(rect.height - moneda.height, 0))

# ════════════════════════════════════════════════════════════════════════════
# CICLO PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

running = True

while running:
    # Obtener pantalla actualizada del sistema centralizado
    pantalla = get_pantalla_actual()
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener dimensiones actuales (fijas)
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
    
    # ← NUEVO: Detectar movimiento horizontal para actualizar animación
    movimiento_jugador_x = 0
    if keys[pygame.K_LEFT]:
        movimiento_jugador_x = -1
    elif keys[pygame.K_RIGHT]:
        movimiento_jugador_x = 1
    
    jugador.actualizar_animacion(movimiento_jugador_x, 0)
    
    # ← NUEVO: Actualizar animación de moneda
    moneda.actualizar_animacion()
    
    # Mantener jugador dentro de la pantalla
    if jugador.x < 0:
        jugador.x = 0
    if jugador.x > ancho_actual - jugador.width:
        jugador.x = ancho_actual - jugador.width
    if jugador.y < 0:
        jugador.y = 0
    if jugador.y > alto_actual - jugador.height:
        jugador.y = alto_actual - jugador.height
    
    # ════════════════════════════════════════════════════════════════════════════
    # 🧠 MOVIMIENTO INTELIGENTE DEL ENEMIGO (CON IA)
    # ════════════════════════════════════════════════════════════════════════════
    
    # Incrementar tiempo de juego
    tiempo_juego += 1
    
    # Obtener posiciones actuales
    pos_enemigo = (enemigo.x, enemigo.y)
    pos_jugador = (jugador.x, jugador.y)
    
    # IA calcula el movimiento óptimo
    # ⚠️ IMPORTANTE: Cada IA tiene una firma diferente de calcular_movimiento()
    
    # Detectar qué tipo de IA se está usando y llamar con los argumentos correctos
    tipo_ia = type(enemigo_ia).__name__
    
    if tipo_ia == "RedNeuronalSimple":
        # Red Neuronal: solo necesita posiciones
        movimiento_ia = enemigo_ia.calcular_movimiento(pos_enemigo, pos_jugador)
        
    elif tipo_ia == "PerseguirInteligente":
        # Básica: necesita posición anterior para predicción
        movimiento_ia = enemigo_ia.calcular_movimiento(
            pos_enemigo, 
            pos_jugador, 
            posicion_anterior_jugador
        )
        
    elif tipo_ia == "IAPatronesAleatorios":
        # Patrones: necesita tiempo para cambiar estrategias
        movimiento_ia = enemigo_ia.calcular_movimiento(
            pos_enemigo, 
            pos_jugador, 
            tiempo_juego
        )
        
    elif tipo_ia == "IAHibrida":
        # Híbrida: necesita todo
        movimiento_ia = enemigo_ia.calcular_movimiento(
            pos_enemigo, 
            pos_jugador, 
            tiempo_juego,
            posicion_anterior_jugador
        )
    else:
        # Fallback por si acaso
        movimiento_ia = enemigo_ia.calcular_movimiento(pos_enemigo, pos_jugador)
    
    # Aplicar movimiento calculado por la IA
    velocidad_enemigo_x = movimiento_ia[0]
    velocidad_enemigo_y = movimiento_ia[1]
    
    enemigo.x += velocidad_enemigo_x
    enemigo.y += velocidad_enemigo_y
    
    # ← NUEVO: Actualizar animación del enemigo según dirección de IA
    enemigo.actualizar_animacion(velocidad_enemigo_x, velocidad_enemigo_y)
    
    # Mantener enemigo dentro de la pantalla (pero con IA puede tocar bordes)
    if enemigo.x < 0:
        enemigo.x = 0
    if enemigo.x > ancho_actual - enemigo.width:
        enemigo.x = ancho_actual - enemigo.width
    if enemigo.y < 0:
        enemigo.y = 0
    if enemigo.y > alto_actual - enemigo.height:
        enemigo.y = alto_actual - enemigo.height
        
    # Guardar posición anterior del jugador para próxima iteración
    posicion_anterior_jugador = pos_jugador
    
    # COLISIONES
    if jugador.colliderect(moneda):
        score += 1
        reproducir_sonido_moneda(sonidos)  # ← Reproducir sonido de moneda
        respawn_moneda()
    
    if jugador.colliderect(enemigo):
        # 🧠 IA: Registrar captura exitosa para evolución
        enemigo_ia.captura_exitosa()
        
        # ← Sistema de vidas corregido
        vidas -= 1        
        # Separar jugador y enemigo inmediatamente
        jugador.rect.x = posicion_respawn_jugador[0]
        jugador.rect.y = posicion_respawn_jugador[1]
        
        # Mover enemigo lejos
        rect = pantalla.get_rect()
        enemigo.rect.x = rect.width - 100
        enemigo.rect.y = rect.height - 100
        
        if vidas > 0:
            # Pausar música para que se escuche el sonido de failed
            pausar_musica_fondo()
            
            # Dibujar estado actual antes de pausar
            pantalla.fill(NEGRO)
            jugador.dibujar(pantalla)
            moneda.dibujar(pantalla)
            enemigo.dibujar(pantalla)
            
            # Mostrar pantalla de respawn (esto pausa el juego)
            pantalla = get_pantalla_actual()  # Usar pantalla centralizada
            if not pantalla_respawn(pantalla, fuente_grande, fuente_mediana, vidas, score, sonidos):
                running = False
                continue
            
            # Reanudar música cuando continúa jugando
            reanudar_musica_fondo()
        else:
            # Game Over - mostrar pantalla final
            detener_musica_fondo()  # ← Detener música
            reproducir_sonido_game_over(sonidos)  # ← Reproducir sonido de game over
            pygame.time.wait(500)  # ← Esperar a que suene el game over
            pantalla = get_pantalla_actual()  # Usar pantalla centralizada
            opcion = pantalla_game_over(pantalla, fuente_grande, fuente_mediana, score, vidas)
            
            if opcion == 'reintentar':
                # Reiniciar el juego completamente
                detener_musica_fondo()  # ← Asegurar que todo se detiene
                detener_todos_sonidos(sonidos)  # ← Detener todos los efectos de sonido
                score = 0
                vidas = 5
                respawn_moneda()
                jugador.rect.x = posicion_respawn_jugador[0]
                jugador.rect.y = posicion_respawn_jugador[1]
                # Resetear velocidades del enemigo
                velocidad_enemigo_x = velocidad_enemigo
                velocidad_enemigo_y = velocidad_enemigo
                # Reiniciar música de fondo
                if musica_cargada:
                    iniciar_musica_fondo()
            else:
                running = False
                continue
    
    # ────────────────────────────────────────────────────────────────────────
    # DIBUJAR TODO
    # ────────────────────────────────────────────────────────────────────────
    
    # Fondo negro
    pantalla.fill(NEGRO)
    
    # Dibujar objetos animados (sprites)
    jugador.dibujar(pantalla)
    
    # ← NUEVO: Dibujar moneda animada
    moneda.dibujar(pantalla)
    
    enemigo.dibujar(pantalla)
    
    # Dibujar puntuación (usando tu color importado)
    texto_score = fuente_pequeña.render(f"Score: {score}", True, BLANCO)
    pantalla.blit(texto_score, (10, 10))
    
    # ← NUEVO: Mostrar vidas
    texto_vidas = fuente_pequeña.render(f"Vidas: {vidas}", True, ROJO_CLARO)
    pantalla.blit(texto_vidas, (10, 35))
    
    # # Instrucciones
    # texto_ayuda = fuente_pequeña.render("Solo puedes salir en Game Over", True, LIGHT_GRAY)
    # rect_ayuda = texto_ayuda.get_rect()
    # pantalla.blit(texto_ayuda, (pantalla.get_width() - rect_ayuda.width - 10, 10))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS (usando tu configuración)
    clock.tick(FPS)

# ════════════════════════════════════════════════════════════════════════════
# CERRAR JUEGO Y DETENER AUDIO
# ════════════════════════════════════════════════════════════════════════════

detener_musica_fondo()
pygame.quit()
print(f"🎮 Juego terminado. Puntuación final: {score}")
print("✨ Gracias por jugar!")

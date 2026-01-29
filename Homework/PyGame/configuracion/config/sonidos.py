"""
════════════════════════════════════════════════════════════════════════════════
🔊 MÓDULO DE SONIDOS - Sistema de Audio del Juego
════════════════════════════════════════════════════════════════════════════════
Este módulo gestiona todos los efectos de sonido y música del juego.
Incluye:
  - Música de fondo (loop continuo durante el juego)
  - Sonido de moneda recolectada
  - Sonido de pérdida de vida
  - Sonido de game over

Autor: Vanessa
Fecha: 28 de enero de 2026
════════════════════════════════════════════════════════════════════════════════
"""

import pygame
import os

# ════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL MIXER
# ════════════════════════════════════════════════════════════════════════════════

def inicializar_audio():
    """
    Inicializa el sistema de audio de pygame
    """
    pygame.mixer.init()
    print("✓ Sistema de audio inicializado")


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS DE LOS ARCHIVOS DE SONIDO
# ════════════════════════════════════════════════════════════════════════════════

# Obtener la ruta base del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_SOUNDS = os.path.join(RUTA_BASE, "sounds")

# Rutas específicas de cada archivo
RUTA_MONEDA = os.path.join(RUTA_SOUNDS, "soundtrack-coin.wav")
RUTA_GAME_OVER = os.path.join(RUTA_SOUNDS, "soundtrack-game-over.wav")
RUTA_FAILED = os.path.join(RUTA_SOUNDS, "soundtrack-failed.wav")
RUTA_MUSICA = os.path.join(RUTA_SOUNDS, "soundtrack-level.mp3")


# ════════════════════════════════════════════════════════════════════════════════
# CARGAR SONIDOS
# ════════════════════════════════════════════════════════════════════════════════

def cargar_sonidos():
    """
    Carga todos los efectos de sonido del juego
    
    Returns:
        dict: Diccionario con todos los sonidos cargados
    """
    sonidos = {}
    
    # Cargar efecto de moneda
    if os.path.exists(RUTA_MONEDA):
        try:
            sonidos['moneda'] = pygame.mixer.Sound(RUTA_MONEDA)
            sonidos['moneda'].set_volume(0.5)  # 50% volumen
            print(f"✓ Sonido de moneda cargado: {RUTA_MONEDA}")
        except Exception as e:
            print(f"❌ Error al cargar moneda: {e}")
            sonidos['moneda'] = None
    else:
        print(f"⚠ Archivo no encontrado: {RUTA_MONEDA}")
        sonidos['moneda'] = None
    
    # Cargar efecto de pérdida de vida
    if os.path.exists(RUTA_FAILED):
        try:
            sonidos['failed'] = pygame.mixer.Sound(RUTA_FAILED)
            sonidos['failed'].set_volume(0.6)  # 60% volumen
            print(f"✓ Sonido de vida perdida cargado: {RUTA_FAILED}")
        except Exception as e:
            print(f"❌ Error al cargar failed: {e}")
            sonidos['failed'] = None
    else:
        print(f"⚠ Archivo no encontrado: {RUTA_FAILED}")
        sonidos['failed'] = None
    
    # Cargar efecto de game over
    if os.path.exists(RUTA_GAME_OVER):
        try:
            sonidos['game_over'] = pygame.mixer.Sound(RUTA_GAME_OVER)
            sonidos['game_over'].set_volume(0.7)  # 70% volumen
            print(f"✓ Sonido de game over cargado: {RUTA_GAME_OVER}")
        except Exception as e:
            print(f"❌ Error al cargar game over: {e}")
            sonidos['game_over'] = None
    else:
        print(f"⚠ Archivo no encontrado: {RUTA_GAME_OVER}")
        sonidos['game_over'] = None
    
    return sonidos


# ════════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE MÚSICA DE FONDO
# ════════════════════════════════════════════════════════════════════════════════

def cargar_musica_fondo():
    """
    Carga y prepara la música de fondo del juego
    """
    try:
        if os.path.exists(RUTA_MUSICA):
            pygame.mixer.music.load(RUTA_MUSICA)
            pygame.mixer.music.set_volume(0.3)  # 30% volumen para música de fondo
            print(f"✓ Música de fondo cargada")
            return True
        else:
            print(f"⚠ Archivo no encontrado: {RUTA_MUSICA}")
            return False
    except Exception as e:
        print(f"❌ Error al cargar música de fondo: {e}")
        return False


def iniciar_musica_fondo():
    """
    Inicia la reproducción de la música de fondo en loop
    """
    try:
        pygame.mixer.music.play(-1)  # -1 = loop infinito
        print("♪ Música de fondo iniciada")
    except Exception as e:
        print(f"❌ Error al iniciar música: {e}")


def detener_musica_fondo():
    """
    Detiene la música de fondo
    """
    pygame.mixer.music.stop()
    print("⏹ Música de fondo detenida")


def pausar_musica_fondo():
    """
    Pausa la música de fondo (puede reanudarse)
    """
    pygame.mixer.music.pause()


def reanudar_musica_fondo():
    """
    Reanuda la música de fondo pausada
    """
    pygame.mixer.music.unpause()


# ════════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE REPRODUCCIÓN DE EFECTOS
# ════════════════════════════════════════════════════════════════════════════════

def reproducir_sonido_moneda(sonidos):
    """
    Reproduce el sonido de recolectar moneda
    
    Args:
        sonidos (dict): Diccionario con los sonidos cargados
    """
    if sonidos.get('moneda'):
        sonidos['moneda'].play()


def reproducir_sonido_failed(sonidos):
    """
    Reproduce el sonido de perder una vida
    
    Args:
        sonidos (dict): Diccionario con los sonidos cargados
    """
    if sonidos.get('failed'):
        sonidos['failed'].play()


def reproducir_sonido_game_over(sonidos):
    """
    Reproduce el sonido de game over
    
    Args:
        sonidos (dict): Diccionario con los sonidos cargados
    """
    if sonidos.get('game_over'):
        sonidos['game_over'].play()


def detener_todos_sonidos(sonidos):
    """
    Detiene todos los efectos de sonido que se estén reproduciendo
    
    Args:
        sonidos (dict): Diccionario con los sonidos cargados
    """
    for sonido in sonidos.values():
        if sonido and hasattr(sonido, 'stop'):
            sonido.stop()


# ════════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ════════════════════════════════════════════════════════════════════════════════

def ajustar_volumen_musica(volumen):
    """
    Ajusta el volumen de la música de fondo
    
    Args:
        volumen (float): Nivel de volumen (0.0 a 1.0)
    """
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volumen)))


def ajustar_volumen_efectos(sonidos, volumen):
    """
    Ajusta el volumen de todos los efectos de sonido
    
    Args:
        sonidos (dict): Diccionario con los sonidos cargados
        volumen (float): Nivel de volumen (0.0 a 1.0)
    """
    volumen = max(0.0, min(1.0, volumen))
    for sonido in sonidos.values():
        if sonido:
            sonido.set_volume(volumen)

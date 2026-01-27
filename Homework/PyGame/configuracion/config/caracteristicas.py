"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    CARACTERÍSTICAS Y CONFIGURACIÓN DEL JUEGO               ║
║                                                                            ║
║  Aquí se definen:                                                          ║
║  - Resoluciones disponibles                                                ║
║  - Tamaños de objetos                                                      ║
║  - Tamaños de fuentes                                                      ║
║  - Velocidades                                                             ║
║  - Configuración de ventana                                                ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE VENTANA
# ════════════════════════════════════════════════════════════════════════════

# Resoluciones disponibles para el jugador
RESOLUCIONES = [
    (800, 600),      # HD pequeño
    (1024, 768),     # HD medio
    (1280, 720),     # HD 720p
    (1920, 1080),    # Full HD 1080p
]

# Resolución por defecto al iniciar el juego
RESOLUCION_DEFAULT = (400, 400)
ANCHO_DEFAULT, ALTO_DEFAULT = RESOLUCION_DEFAULT

# FPS (Fotogramas por segundo)
# 60 FPS = movimiento muy suave (estándar para juegos)
# 30 FPS = más ligero pero menos suave
FPS = 60

# Modos de ventana
MODO_VENTANA = pygame.RESIZABLE      # Ventana redimensionable
MODO_PANTALLA_COMPLETA = pygame.FULLSCREEN  # Pantalla completa

# ════════════════════════════════════════════════════════════════════════════
# TAMAÑOS DE OBJETOS DEL JUEGO
# ════════════════════════════════════════════════════════════════════════════

# Tamaños base (en píxeles) - Se ajustan según la resolución
TAMAÑO_JUGADOR_BASE = 50        # Tamaño del cuadrado del jugador
TAMAÑO_MONEDA_BASE = 25         # Tamaño de la moneda
TAMAÑO_ENEMIGO_BASE = 35        # Tamaño del enemigo

# Tamaños mínimos (para que no desaparezcan en pantallas pequeñas)
TAMAÑO_JUGADOR_MIN = 20
TAMAÑO_MONEDA_MIN = 10
TAMAÑO_ENEMIGO_MIN = 15

# ════════════════════════════════════════════════════════════════════════════
# VELOCIDADES DE MOVIMIENTO
# ════════════════════════════════════════════════════════════════════════════

# Velocidad base del jugador (píxeles por fotograma)
VELOCIDAD_JUGADOR_BASE = 5

# Velocidad base del enemigo
VELOCIDAD_ENEMIGO_BASE = 4

# Velocidades mínimas (para pantallas pequeñas)
VELOCIDAD_JUGADOR_MIN = 2
VELOCIDAD_ENEMIGO_MIN = 1

# Factor de escalado de velocidad (qué tan rápido se escala con la resolución)
FACTOR_ESCALA = 0.8  # 80% de la escala completa

# ════════════════════════════════════════════════════════════════════════════
# TAMAÑOS DE FUENTES
# ════════════════════════════════════════════════════════════════════════════

# Tamaños de fuente para diferentes usos
TAMAÑO_FUENTE_TITULO = 72       # Título del juego en el menú
TAMAÑO_FUENTE_SUBTITULO = 48    # Subtítulos e instrucciones
TAMAÑO_FUENTE_NORMAL = 36       # Texto normal (score, etc.)
TAMAÑO_FUENTE_BOTONES = 32      # Texto en botones
TAMAÑO_FUENTE_PEQUEÑA = 24      # Texto pequeño (ayuda, créditos)

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE BOTONES
# ════════════════════════════════════════════════════════════════════════════

# Tamaños de botones
ANCHO_BOTON_GRANDE = 400        # Botones grandes (Jugar, Opciones)
ALTO_BOTON_GRANDE = 60

ANCHO_BOTON_MEDIANO = 300       # Botones medianos
ALTO_BOTON_MEDIANO = 50

ANCHO_BOTON_PEQUEÑO = 150       # Botones pequeños (resoluciones)
ALTO_BOTON_PEQUEÑO = 40

# Espaciado entre botones
ESPACIADO_BOTONES = 20          # Píxeles entre botones

# Grosor del borde de botones
GROSOR_BORDE_BOTON = 3

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE AUDIO
# ════════════════════════════════════════════════════════════════════════════

# Volumen por defecto (0.0 a 1.0)
VOLUMEN_EFECTOS = 0.5           # 50% de volumen para efectos
VOLUMEN_MUSICA = 0.3            # 30% de volumen para música de fondo

# Rutas de archivos de sonido
RUTA_SONIDO_MONEDA = "configuracion/sounds/moneda.wav"
RUTA_SONIDO_COLISION = "configuracion/sounds/colision.wav"
RUTA_MUSICA_FONDO = "configuracion/sounds/musica_fondo.mp3"

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: CREAR VENTANA
# ════════════════════════════════════════════════════════════════════════════

def crear_ventana(resolucion=RESOLUCION_DEFAULT, pantalla_completa=False):
    """
    Crea la ventana del juego con la configuración especificada
    
    Args:
        resolucion (tuple): (ancho, alto) de la ventana
        pantalla_completa (bool): True para pantalla completa
    
    Returns:
        pygame.Surface: Superficie de la pantalla
    """
    modo = MODO_PANTALLA_COMPLETA if pantalla_completa else MODO_VENTANA
    return pygame.display.set_mode(resolucion, modo)

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: CALCULAR ESCALA
# ════════════════════════════════════════════════════════════════════════════

def calcular_escala(ancho_actual):
    """
    Calcula el factor de escala basado en el ancho de la ventana
    
    Esto permite que los objetos se adapten al tamaño de la ventana
    
    Args:
        ancho_actual (int): Ancho actual de la ventana
    
    Returns:
        float: Factor de escala (ej: 1.0 para 800px, 2.0 para 1600px)
    """
    return (ancho_actual / ANCHO_DEFAULT) * FACTOR_ESCALA

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: CALCULAR TAMAÑO ADAPTATIVO
# ════════════════════════════════════════════════════════════════════════════

def calcular_tamaño(tamaño_base, tamaño_minimo, escala):
    """
    Calcula el tamaño de un objeto basado en la escala
    
    Args:
        tamaño_base (int): Tamaño original del objeto
        tamaño_minimo (int): Tamaño mínimo permitido
        escala (float): Factor de escala
    
    Returns:
        int: Tamaño escalado (pero no menor al mínimo)
    """
    return max(int(tamaño_base * escala), tamaño_minimo)

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: CALCULAR VELOCIDAD ADAPTATIVA
# ════════════════════════════════════════════════════════════════════════════

def calcular_velocidad(velocidad_base, velocidad_minima, escala):
    """
    Calcula la velocidad de un objeto basada en la escala
    
    Args:
        velocidad_base (int): Velocidad original
        velocidad_minima (int): Velocidad mínima permitida
        escala (float): Factor de escala
    
    Returns:
        int: Velocidad escalada
    """
    return max(int(velocidad_base * escala), velocidad_minima)

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: CREAR OBJETOS ADAPTATIVOS
# ════════════════════════════════════════════════════════════════════════════

def crear_objetos_adaptativos(pantalla):
    """
    Crea todos los objetos del juego adaptados al tamaño de la ventana
    
    Args:
        pantalla (pygame.Surface): Superficie de la pantalla
    
    Returns:
        dict: Diccionario con todos los objetos y sus propiedades
    """
    # Obtener dimensiones actuales
    rect = pantalla.get_rect()
    ancho = rect.width
    alto = rect.height
    
    # Calcular escala
    escala = calcular_escala(ancho)
    
    # Calcular tamaños
    tamaño_jugador = calcular_tamaño(TAMAÑO_JUGADOR_BASE, TAMAÑO_JUGADOR_MIN, escala)
    tamaño_moneda = calcular_tamaño(TAMAÑO_MONEDA_BASE, TAMAÑO_MONEDA_MIN, escala)
    tamaño_enemigo = calcular_tamaño(TAMAÑO_ENEMIGO_BASE, TAMAÑO_ENEMIGO_MIN, escala)
    
    # Calcular velocidades
    velocidad_jugador = calcular_velocidad(VELOCIDAD_JUGADOR_BASE, VELOCIDAD_JUGADOR_MIN, escala)
    velocidad_enemigo = calcular_velocidad(VELOCIDAD_ENEMIGO_BASE, VELOCIDAD_ENEMIGO_MIN, escala)
    
    # Crear objetos
    jugador = pygame.Rect(
        int(ancho * 0.1),          # 10% desde la izquierda
        int(alto * 0.3),           # 30% desde arriba
        tamaño_jugador,
        tamaño_jugador
    )
    
    moneda = pygame.Rect(
        int(ancho // 2),           # Centro horizontal
        int(alto // 2),            # Centro vertical
        tamaño_moneda,
        tamaño_moneda
    )
    
    enemigo = pygame.Rect(
        int(ancho - 100 * escala), # Cerca del borde derecho
        int(alto * 0.2),           # 20% desde arriba
        tamaño_enemigo,
        tamaño_enemigo
    )
    
    return {
        'jugador': jugador,
        'moneda': moneda,
        'enemigo': enemigo,
        'velocidad_jugador': velocidad_jugador,
        'velocidad_enemigo': velocidad_enemigo,
        'escala': escala,
        'tamaños': {
            'jugador': tamaño_jugador,
            'moneda': tamaño_moneda,
            'enemigo': tamaño_enemigo,
        }
    }

# ════════════════════════════════════════════════════════════════════════════
# FUNCIONES PARA ACTUALIZACIÓN DINÁMICA DE VENTANA
# ════════════════════════════════════════════════════════════════════════════

def actualizar_fuentes_dinamicas(escala_actual, tamaño_titulo, tamaño_subtitulo, tamaño_normal):
    """
    Actualiza los tamaños de fuente según la escala actual
    Esto hace que el texto también se adapte al tamaño de ventana
    
    Args:
        escala_actual: Factor de escala basado en ancho de ventana
        tamaño_titulo: Tamaño base de fuente para títulos
        tamaño_subtitulo: Tamaño base de fuente para subtítulos  
        tamaño_normal: Tamaño base de fuente normal
    
    Returns:
        dict con las tres fuentes recreadas
    """
    # Calcular nuevos tamaños basados en la escala
    tamaño_grande = max(int(tamaño_titulo * escala_actual), 24)
    tamaño_mediana = max(int(tamaño_subtitulo * escala_actual), 18)
    tamaño_pequeña = max(int(tamaño_normal * escala_actual), 14)
    
    # Recrear las fuentes con los nuevos tamaños
    return {
        'fuente_grande': pygame.font.Font(None, tamaño_grande),
        'fuente_mediana': pygame.font.Font(None, tamaño_mediana),
        'fuente_pequeña': pygame.font.Font(None, tamaño_pequeña)
    }

def actualizar_objetos_dinamicos(pantalla, ancho_anterior, alto_anterior, 
                                  objetos_actuales, velocidades_actuales):
    """
    Actualiza objetos del juego manteniendo sus posiciones EXACTAS escaladas.
    Si el enemigo estaba en la esquina superior derecha, seguirá ahí.
    
    Args:
        pantalla: Surface de pygame con el nuevo tamaño
        ancho_anterior: Ancho de ventana antes del resize
        alto_anterior: Alto de ventana antes del resize
        objetos_actuales: dict con 'jugador', 'moneda', 'enemigo' actuales
        velocidades_actuales: dict con 'velocidad_enemigo_x' y 'velocidad_enemigo_y'
    
    Returns:
        dict con objetos actualizados y nuevas velocidades
    """
    rect = pantalla.get_rect()
    ancho_nuevo = rect.width
    alto_nuevo = rect.height
    
    # Calcular factor de escala entre ventana anterior y nueva
    escala_x = ancho_nuevo / max(ancho_anterior, 1)
    escala_y = alto_nuevo / max(alto_anterior, 1)
    
    # Calcular nueva escala para tamaños
    escala_actual = calcular_escala(ancho_nuevo)
    
    # Crear nuevos objetos con tamaños escalados
    objetos_nuevos = crear_objetos_adaptativos(pantalla)
    
    jugador = objetos_actuales['jugador']
    enemigo = objetos_actuales['enemigo']
    moneda = objetos_actuales['moneda']
    
    # ═══════════════════════════════════════════════════════════════════
    # MANTENER POSICIONES EXACTAS ESCALADAS (no mover a random)
    # ═══════════════════════════════════════════════════════════════════
    
    # Calcular el centro de cada objeto (más preciso que esquinas)
    jugador_centro_x = jugador.x + jugador.width / 2
    jugador_centro_y = jugador.y + jugador.height / 2
    
    enemigo_centro_x = enemigo.x + enemigo.width / 2
    enemigo_centro_y = enemigo.y + enemigo.height / 2
    
    moneda_centro_x = moneda.x + moneda.width / 2
    moneda_centro_y = moneda.y + moneda.height / 2
    
    # Escalar las posiciones de los centros
    jugador_nuevo_centro_x = jugador_centro_x * escala_x
    jugador_nuevo_centro_y = jugador_centro_y * escala_y
    
    enemigo_nuevo_centro_x = enemigo_centro_x * escala_x
    enemigo_nuevo_centro_y = enemigo_centro_y * escala_y
    
    moneda_nuevo_centro_x = moneda_centro_x * escala_x
    moneda_nuevo_centro_y = moneda_centro_y * escala_y
    
    # Aplicar centros escalados a los nuevos objetos
    objetos_nuevos['jugador'].centerx = int(jugador_nuevo_centro_x)
    objetos_nuevos['jugador'].centery = int(jugador_nuevo_centro_y)
    
    objetos_nuevos['enemigo'].centerx = int(enemigo_nuevo_centro_x)
    objetos_nuevos['enemigo'].centery = int(enemigo_nuevo_centro_y)
    
    objetos_nuevos['moneda'].centerx = int(moneda_nuevo_centro_x)
    objetos_nuevos['moneda'].centery = int(moneda_nuevo_centro_y)
    
    # Asegurar que los objetos estén dentro de la pantalla
    objetos_nuevos['jugador'].clamp_ip(rect)
    objetos_nuevos['enemigo'].clamp_ip(rect)
    objetos_nuevos['moneda'].clamp_ip(rect)
    
    # Escalar velocidades del enemigo también (para mantener su trayectoria)
    vel_enemigo_x = velocidades_actuales['velocidad_enemigo_x']
    vel_enemigo_y = velocidades_actuales['velocidad_enemigo_y']
    
    # Mantener la dirección pero escalar la magnitud
    signo_x = 1 if vel_enemigo_x >= 0 else -1
    signo_y = 1 if vel_enemigo_y >= 0 else -1
    
    velocidad_enemigo_nueva = objetos_nuevos['velocidad_enemigo']
    
    return {
        'jugador': objetos_nuevos['jugador'],
        'moneda': objetos_nuevos['moneda'],
        'enemigo': objetos_nuevos['enemigo'],
        'velocidad_jugador': objetos_nuevos['velocidad_jugador'],
        'velocidad_enemigo': velocidad_enemigo_nueva,
        'velocidad_enemigo_x': signo_x * velocidad_enemigo_nueva,
        'velocidad_enemigo_y': signo_y * velocidad_enemigo_nueva,
        'escala_actual': escala_actual
    }

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE POSICIONES EN MENÚ
# ════════════════════════════════════════════════════════════════════════════

# Posiciones relativas para elementos del menú (en porcentaje)
POS_TITULO_Y = 0.15           # 15% desde arriba
POS_PRIMER_BOTON_Y = 0.40     # 40% desde arriba
POS_SEGUNDO_BOTON_Y = 0.55    # 55% desde arriba
POS_TERCER_BOTON_Y = 0.70     # 70% desde arriba

# ════════════════════════════════════════════════════════════════════════════
# EJEMPLOS DE USO
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎮 Configuración del juego cargada:")
    print(f"\n📐 Resoluciones disponibles:")
    for res in RESOLUCIONES:
        print(f"  - {res[0]}x{res[1]}")
    
    print(f"\n🎯 Tamaños base:")
    print(f"  Jugador: {TAMAÑO_JUGADOR_BASE}px")
    print(f"  Moneda: {TAMAÑO_MONEDA_BASE}px")
    print(f"  Enemigo: {TAMAÑO_ENEMIGO_BASE}px")
    
    print(f"\n⚡ Velocidades base:")
    print(f"  Jugador: {VELOCIDAD_JUGADOR_BASE} px/frame")
    print(f"  Enemigo: {VELOCIDAD_ENEMIGO_BASE} px/frame")
    
    print(f"\n🔊 Audio:")
    print(f"  Volumen efectos: {int(VOLUMEN_EFECTOS * 100)}%")
    print(f"  Volumen música: {int(VOLUMEN_MUSICA * 100)}%")

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    SISTEMA DE MENÚS Y PANTALLAS                           ║
║                                                                            ║
║  Gestiona:                                                                 ║
║  - Pantalla de título                                                      ║
║  - Menú de opciones (resolución)                                           ║
║  - Pantalla de game over                                                   ║
║  - Botones interactivos                                                    ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame

# Importar TODOS los colores desde tu módulo de colores
from configuracion.config.colores import *

# Importar tamaños base de fuentes para escalar en menús
from configuracion.config.caracteristicas import (
    TAMAÑO_FUENTE_TITULO,
    TAMAÑO_FUENTE_SUBTITULO,
    TAMAÑO_FUENTE_NORMAL,
    RESOLUCIONES_LISTA,
    crear_ventana
)

# Importar sistema de sonidos
from configuracion.config.sonidos import reproducir_sonido_failed

# ════════════════════════════════════════════════════════════════════════════
# SISTEMA CENTRALIZADO DE RESOLUCIÓN
# ════════════════════════════════════════════════════════════════════════════

# Variable global para manejar la resolución actual
_resolucion_global = None
_pantalla_global = None

def inicializar_resolucion_global(pantalla):
    """Inicializa la resolución global al iniciar el juego"""
    global _resolucion_global, _pantalla_global
    _pantalla_global = pantalla
    _resolucion_global = (pantalla.get_width(), pantalla.get_height())

def get_resolucion_actual():
    """Obtiene la resolución actual"""
    return _resolucion_global

def get_pantalla_actual():
    """Obtiene la pantalla actual"""
    return _pantalla_global

def actualizar_resolucion_global(nueva_pantalla):
    """Actualiza la resolución global y la pantalla"""
    global _resolucion_global, _pantalla_global
    _pantalla_global = nueva_pantalla
    _resolucion_global = (nueva_pantalla.get_width(), nueva_pantalla.get_height())
    return _pantalla_global

# ════════════════════════════════════════════════════════════════════════════
# CLASE BOTÓN
# ════════════════════════════════════════════════════════════════════════════

class Boton:
    """Botón interactivo para menús"""
    
    def __init__(self, x, y, ancho, alto, texto, fuente, color_fondo=None, color_texto=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.color_fondo = color_fondo if color_fondo else GRIS_OSCURO
        self.color_texto = color_texto if color_texto else BLANCO
        self.color_hover = GRIS_MEDIO
        self.is_hover = False
    
    def update(self, mouse_pos):
        """Actualiza si el mouse está sobre el botón"""
        self.is_hover = self.rect.collidepoint(mouse_pos)
    
    def draw(self, pantalla):
        """Dibuja el botón"""
        color = self.color_hover if self.is_hover else self.color_fondo
        pygame.draw.rect(pantalla, color, self.rect)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 2)
        
        texto_renderizado = self.fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        pantalla.blit(texto_renderizado, texto_rect)
    
    def clicked(self, mouse_pos, mouse_click):
        """Retorna True si el botón fue clickeado"""
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]


def crear_fuentes_escaladas(ancho_ventana):
    """Crea fuentes escaladas según el tamaño de la ventana"""
    escala = ancho_ventana / 800
    return {
        'grande': pygame.font.Font(None, max(int(TAMAÑO_FUENTE_TITULO * escala), 24)),
        'mediana': pygame.font.Font(None, max(int(TAMAÑO_FUENTE_SUBTITULO * escala), 18)),
        'pequeña': pygame.font.Font(None, max(int(TAMAÑO_FUENTE_NORMAL * escala), 14))
    }


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE TÍTULO (menú de configuración)
# ════════════════════════════════════════════════════════════════════════════

def pantalla_titulo(pantalla, fuente_grande, fuente_mediana):
    """
    Pantalla principal del juego con opciones - SISTEMA CENTRALIZADO
    Retorna: ('iniciar', None) o ('salir', None)
    """
    global _pantalla_global, _resolucion_global
    
    # Inicializar sistema global si no existe
    if _pantalla_global is None:
        inicializar_resolucion_global(pantalla)
    
    def crear_elementos_titulo():
        """Crea elementos escalados para la resolución actual"""
        pantalla_actual = _pantalla_global
        ancho = pantalla_actual.get_width()
        alto = pantalla_actual.get_height()
        
        # Escalar fuentes
        escala_x = ancho / 800
        escala_y = alto / 600
        fuentes = crear_fuentes_escaladas(ancho)
        
        # Crear botones escalados
        ancho_boton = max(int(300 * escala_x), 200)
        alto_boton = max(int(60 * escala_y), 40)
        centro_y = alto // 2
        offset_1 = int(-80 * escala_y)
        offset_2 = int(20 * escala_y)
        offset_3 = int(120 * escala_y)
        
        boton_iniciar = Boton(ancho // 2 - ancho_boton // 2, centro_y + offset_1, ancho_boton, alto_boton, "INICIAR JUEGO", fuentes['mediana'])
        boton_opciones = Boton(ancho // 2 - ancho_boton // 2, centro_y + offset_2, ancho_boton, alto_boton, "OPCIONES", fuentes['mediana'])
        boton_salir = Boton(ancho // 2 - ancho_boton // 2, centro_y + offset_3, ancho_boton, alto_boton, "SALIR", fuentes['mediana'])
        
        return boton_iniciar, boton_opciones, boton_salir, fuentes
    
    # Crear elementos iniciales
    boton_iniciar, boton_opciones, boton_salir, fuentes = crear_elementos_titulo()
    
    running = True
    while running:
        pantalla_actual = _pantalla_global
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ('salir', None)
        
        # Actualizar botones
        boton_iniciar.update(mouse_pos)
        boton_opciones.update(mouse_pos)
        boton_salir.update(mouse_pos)
        
        # Detectar clicks
        if boton_iniciar.clicked(mouse_pos, mouse_click):
            return ('iniciar', None)
        
        if boton_opciones.clicked(mouse_pos, mouse_click):
            # Llamar a pantalla de opciones
            cambio_resolucion = pantalla_opciones_completa(pantalla_actual, fuentes['mediana'])
            if cambio_resolucion:
                # Si cambió la resolución, recrear TODOS los elementos
                boton_iniciar, boton_opciones, boton_salir, fuentes = crear_elementos_titulo()
                # Pequeña pausa para estabilizar
                pygame.time.wait(100)
        
        if boton_salir.clicked(mouse_pos, mouse_click):
            return ('salir', None)
        
        # DIBUJAR TODO ESCALADO
        pantalla_actual = _pantalla_global
        ancho_pantalla = pantalla_actual.get_width()
        alto_pantalla = pantalla_actual.get_height()
        
        pantalla_actual.fill(FONDO_OSCURO)
        
        # Título escalado
        titulo = fuentes['grande'].render("🔮 LADRÓN DE MAGIA 🔮", True, AZUL_CLARO)
        titulo_rect = titulo.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 4))
        pantalla_actual.blit(titulo, titulo_rect)
        
        # Botones
        boton_iniciar.draw(pantalla_actual)
        boton_opciones.draw(pantalla_actual)
        boton_salir.draw(pantalla_actual)
        
        # Info sobre ESC escalada
        escala_info = max(int(20 * ancho_pantalla / 800), 14)
        fuente_info = pygame.font.Font(None, escala_info)
        info_esc = fuente_info.render("ESC solo disponible en Game Over", True, GRIS_MEDIO)
        pantalla_actual.blit(info_esc, (20, alto_pantalla - 30))
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return ('salir', None)


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE INSTRUCCIONES
# ════════════════════════════════════════════════════════════════════════════

def pantalla_instrucciones(pantalla, fuente_mediana, ruta_sprites):
    """
    Pantalla de instrucciones con sprites de moneda y enemigo - SISTEMA CENTRALIZADO
    """
    import os
    global _pantalla_global
    
    def crear_elementos_instrucciones():
        """Crea elementos escalados para la resolución actual"""
        pantalla_actual = _pantalla_global
        ancho = pantalla_actual.get_width()
        alto = pantalla_actual.get_height()
        
        # Escalar fuentes
        fuentes = crear_fuentes_escaladas(ancho)
        
        # Cargar sprites escalados
        escala = ancho / 800
        try:
            coin = pygame.image.load(os.path.join(ruta_sprites, "coin-1.jpg"))
            coin = pygame.transform.scale(coin, (max(int(50 * escala), 20), max(int(50 * escala), 20)))
        except:
            coin = None
        
        try:
            enemy = pygame.image.load(os.path.join(ruta_sprites, "enemy-right-1.jpg"))
            enemy = pygame.transform.scale(enemy, (max(int(60 * escala), 24), max(int(60 * escala), 24)))
        except:
            enemy = None
        
        return fuentes, coin, enemy
    
    # Crear elementos escalados
    fuentes, img_coin, img_enemy = crear_elementos_instrucciones()
    
    running = True
    while running:
        pantalla_actual = _pantalla_global
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        
        ancho_pantalla = pantalla_actual.get_width()
        alto_pantalla = pantalla_actual.get_height()
        
        # Fondo
        pantalla_actual.fill(FONDO_OSCURO)
        
        # Título escalado
        titulo = fuentes['grande'].render("CÓMO JUGAR", True, AZUL_CLARO)
        titulo_rect = titulo.get_rect(center=(ancho_pantalla // 2, max(int(80 * alto_pantalla / 600), 60)))
        pantalla_actual.blit(titulo, titulo_rect)
        
        # Instrucción 1: Recolectar monedas
        y_pos = max(int(200 * alto_pantalla / 600), 120)
        texto1 = fuentes['mediana'].render("Recolecta puntos de magia", True, VERDE_CLARO)
        pantalla_actual.blit(texto1, (ancho_pantalla // 4, y_pos))
        if img_coin:
            pantalla_actual.blit(img_coin, (ancho_pantalla // 2 + max(int(100 * ancho_pantalla / 800), 60), y_pos - 10))
        
        # Instrucción 2: Evitar enemigos
        y_pos = max(int(280 * alto_pantalla / 600), 180)
        texto2 = fuentes['mediana'].render("Evita los monstruos", True, ROJO_CLARO)
        pantalla_actual.blit(texto2, (ancho_pantalla // 4, y_pos))
        if img_enemy:
            pantalla_actual.blit(img_enemy, (ancho_pantalla // 2 + max(int(100 * ancho_pantalla / 800), 60), y_pos - 15))
        
        # Instrucción 3: Ganar
        y_pos = max(int(360 * alto_pantalla / 600), 240)
        texto3 = fuentes['mediana'].render("¡Y gana!", True, AMARILLO_CLARO)
        pantalla_actual.blit(texto3, (ancho_pantalla // 4, y_pos))
        
        # Instrucción final escalada
        instruccion = fuentes['mediana'].render("Pulsa ESPACIO para iniciar", True, AZUL_SUAVE)
        instruccion_rect = instruccion.get_rect(center=(ancho_pantalla // 2, alto_pantalla - max(int(100 * alto_pantalla / 600), 80)))
        pantalla_actual.blit(instruccion, instruccion_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return False



# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE OPCIONES COMPLETA (CON MANEJO CORRECTO DE RESOLUCIÓN)
# ════════════════════════════════════════════════════════════════════════════

def pantalla_opciones_completa(pantalla_actual, fuente_mediana):
    """
    Pantalla de opciones SIMPLE y FUNCIONAL
    RETORNA: True si cambió la resolución, False si no
    """
    global _pantalla_global, _resolucion_global
    
    resolucion_inicial = (pantalla_actual.get_width(), pantalla_actual.get_height())
    
    def crear_elementos_opciones():
        """Crea botones para la resolución actual"""
        pantalla = _pantalla_global
        ancho = pantalla.get_width()
        alto = pantalla.get_height()
        
        # Escalar elementos
        escala_x = ancho / 800
        escala_y = alto / 600
        ancho_boton = max(int(300 * escala_x), 200)
        alto_boton = max(int(60 * escala_y), 40)
        espaciado = max(int(80 * escala_y), 60)
        
        # Fuentes escaladas
        fuente_titulo = pygame.font.Font(None, max(int(50 * escala_x), 24))
        fuente_botones = pygame.font.Font(None, max(int(32 * escala_x), 18))
        
        botones = []
        y_inicio = alto // 2 - (len(RESOLUCIONES_LISTA) * espaciado) // 2
        
        for i, (nombre, resolucion) in enumerate(RESOLUCIONES_LISTA):
            texto_boton = f"{nombre.upper()} ({resolucion[0]}x{resolucion[1]})"
            es_actual = (resolucion == _resolucion_global)
            
            if es_actual:
                texto_boton += " ✓"
            
            boton = Boton(
                ancho // 2 - ancho_boton // 2,
                y_inicio + i * espaciado,
                ancho_boton, alto_boton,
                texto_boton,
                fuente_botones,
                color_fondo=VERDE_CLARO if es_actual else GRIS_OSCURO
            )
            botones.append((resolucion, boton, nombre))
        
        # Botón ATRÁS
        boton_atras = Boton(
            ancho // 2 - ancho_boton // 2, 
            alto - max(int(100 * escala_y), 80),
            ancho_boton, alto_boton, 
            "ATRÁS", 
            fuente_botones,
            color_fondo=AZUL_OSCURO
        )
        
        return botones, boton_atras, fuente_titulo, fuente_botones
    
    # Crear elementos iniciales
    botones_res, boton_atras, fuente_titulo, fuente_botones = crear_elementos_opciones()
    
    running = True
    cambio_resolucion = False
    
    # Protección contra clicks fantasma
    tiempo_entrada = pygame.time.get_ticks()
    DELAY_INICIAL = 200
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
        
        # Verificar si ya pasó el tiempo de protección
        tiempo_actual = pygame.time.get_ticks()
        puede_clickear = (tiempo_actual - tiempo_entrada) >= DELAY_INICIAL
        
        if puede_clickear:
            # Verificar clicks en botones de resolución
            for resolucion, boton, nombre in botones_res:
                boton.update(mouse_pos)
                if boton.clicked(mouse_pos, mouse_click):
                    if resolucion != _resolucion_global:
                        # CAMBIAR RESOLUCIÓN
                        nueva_pantalla = crear_ventana(resolucion, pantalla_completa=False)
                        pygame.display.set_caption("🔮 Ladrón de Magia")
                        actualizar_resolucion_global(nueva_pantalla)
                        cambio_resolucion = True
                        
                        # Recrear elementos para nueva resolución
                        botones_res, boton_atras, fuente_titulo, fuente_botones = crear_elementos_opciones()
                        
                        # Pequeña pausa para evitar clicks múltiples
                        pygame.time.wait(150)
                        tiempo_entrada = pygame.time.get_ticks()
            
            # Verificar click en ATRÁS
            boton_atras.update(mouse_pos)
            if boton_atras.clicked(mouse_pos, mouse_click):
                running = False
        else:
            # Durante la protección, solo actualizar visualmente
            for resolucion, boton, nombre in botones_res:
                boton.update(mouse_pos)
            boton_atras.update(mouse_pos)
        
        # DIBUJAR TODO
        pantalla = _pantalla_global
        pantalla.fill(FONDO_OSCURO)
        
        # Título
        titulo = fuente_titulo.render("RESOLUCIONES FIJAS", True, AMARILLO_CLARO)
        titulo_rect = titulo.get_rect(center=(pantalla.get_width() // 2, 80))
        pantalla.blit(titulo, titulo_rect)
        
        # Info
        info = fuente_botones.render("(Elige tu tamaño de ventana ideal)", True, GRIS_CLARO)
        info_rect = info.get_rect(center=(pantalla.get_width() // 2, 130))
        pantalla.blit(info, info_rect)
        
        # Botones de resolución
        for resolucion, boton, nombre in botones_res:
            boton.draw(pantalla)
        
        # Botón ATRÁS
        boton_atras.draw(pantalla)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return cambio_resolucion

# ════════════════════════════════════════════════════════════════════════════
# PANTALLA GAME OVER
# ════════════════════════════════════════════════════════════════════════════

def pantalla_game_over(pantalla, fuente_grande, fuente_mediana, score_final, vidas):
    """
    Pantalla de fin de juego - SISTEMA CENTRALIZADO
    Retorna: 'reintentar' o 'salir'
    """
    global _pantalla_global
    
    def crear_elementos_game_over():
        """Crea elementos escalados para la resolución actual"""
        pantalla_actual = _pantalla_global
        ancho = pantalla_actual.get_width()
        alto = pantalla_actual.get_height()
        
        # Escalar fuentes
        fuentes = crear_fuentes_escaladas(ancho)
        
        # Escalar botones
        escala_x = ancho / 800
        escala_y = alto / 600
        ancho_boton = max(int(300 * escala_x), 200)
        alto_boton = max(int(60 * escala_y), 40)
        
        btn_reintentar = Boton(
            ancho // 2 - ancho_boton // 2, alto // 2,
            ancho_boton, alto_boton, "REINTENTAR", fuentes['mediana'],
            color_fondo=ROJO_OSCURO
        )
        
        btn_salir = Boton(
            ancho // 2 - ancho_boton // 2, alto // 2 + max(int(100 * escala_y), 80),
            ancho_boton, alto_boton, "SALIR", fuentes['mediana'],
            color_fondo=AZUL_OSCURO
        )
        
        return btn_reintentar, btn_salir, fuentes
    
    boton_reintentar, boton_salir, fuentes = crear_elementos_game_over()
    
    running = True
    while running:
        pantalla_actual = _pantalla_global
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'salir'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'salir'  # ESC solo funciona aquí (Game Over)
        
        boton_reintentar.update(mouse_pos)
        boton_salir.update(mouse_pos)
        
        if boton_reintentar.clicked(mouse_pos, mouse_click):
            return 'reintentar'
        
        if boton_salir.clicked(mouse_pos, mouse_click):
            return 'salir'
        
        # Dibujar escalado
        ancho_pantalla = pantalla_actual.get_width()
        alto_pantalla = pantalla_actual.get_height()
        
        pantalla_actual.fill(NEGRO)
        
        # Título GAME OVER escalado
        game_over = fuentes['grande'].render("GAME OVER", True, ROJO_CLARO)
        game_over_rect = game_over.get_rect(center=(ancho_pantalla // 2, max(int(100 * alto_pantalla / 600), 80)))
        pantalla_actual.blit(game_over, game_over_rect)
        
        # Score escalado
        score_text = fuentes['mediana'].render(f"Puntuación: {score_final}", True, BLANCO)
        score_rect = score_text.get_rect(center=(ancho_pantalla // 2, max(int(200 * alto_pantalla / 600), 150)))
        pantalla_actual.blit(score_text, score_rect)
        
        # Botones
        boton_reintentar.draw(pantalla_actual)
        boton_salir.draw(pantalla_actual)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE PAUSA (respawn)
# ════════════════════════════════════════════════════════════════════════════

def pantalla_respawn(pantalla, fuente_grande, fuente_mediana, vidas_restantes, score, sonidos):
    """
    Pantalla cuando el jugador pierde una vida - SISTEMA CENTRALIZADO
    Espera a que presione una tecla para continuar
    """
    global _pantalla_global
    
    # Reproducir sonido UNA SOLA VEZ antes del bucle
    reproducir_sonido_failed(sonidos)
    
    def crear_elementos_respawn():
        """Crea elementos escalados para la resolución actual"""
        pantalla_actual = _pantalla_global
        ancho = pantalla_actual.get_width()
        alto = pantalla_actual.get_height()
        
        # Escalar fuentes
        fuentes = crear_fuentes_escaladas(ancho)
        
        return fuentes
    
    fuentes = crear_elementos_respawn()
    
    running = True
    while running:
        pantalla_actual = _pantalla_global
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                return True
        
        ancho_pantalla = pantalla_actual.get_width()
        alto_pantalla = pantalla_actual.get_height()
        
        # Dibujar con semi-transparencia
        overlay = pygame.Surface((ancho_pantalla, alto_pantalla))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        pantalla_actual.blit(overlay, (0, 0))

        # Textos escalados usando fuentes del sistema centralizado
        perdiste = fuentes['grande'].render("¡PERDISTE UNA VIDA!", True, ROJO_CLARO)
        vidas_text = fuentes['mediana'].render(f"Vidas restantes: {vidas_restantes}", True, BLANCO)
        score_text = fuentes['mediana'].render(f"Score: {score}", True, AMARILLO_CLARO)
        continuar = fuentes['mediana'].render("Presiona cualquier tecla...", True, GRIS_CLARO)
        
        # Posiciones escaladas
        perdiste_rect = perdiste.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 - max(int(100 * alto_pantalla / 600), 80)))
        vidas_rect = vidas_text.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2))
        score_rect = score_text.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + max(int(60 * alto_pantalla / 600), 50)))
        continuar_rect = continuar.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + max(int(140 * alto_pantalla / 600), 120)))
        
        pantalla_actual.blit(perdiste, perdiste_rect)
        pantalla_actual.blit(vidas_text, vidas_rect)
        pantalla_actual.blit(score_text, score_rect)
        pantalla_actual.blit(continuar, continuar_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)



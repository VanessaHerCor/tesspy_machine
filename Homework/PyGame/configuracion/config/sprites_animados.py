"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    SPRITES ANIMADOS DEL JUEGO                             ║
║                                                                            ║
║  Manejo de sprites con animación según dirección y movimiento            ║
║  INTEGRADO CON SISTEMA CENTRALIZADO DE RESOLUCIÓN                        ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame
import os

from configuracion.config.colores import ROJO_CLARO, AMARILLO_CLARO

# Importar sistema centralizado de resolución
try:
    from configuracion.config.pantallas import get_pantalla_actual, get_resolucion_actual
    SISTEMA_CENTRALIZADO_DISPONIBLE = True
except ImportError:
    SISTEMA_CENTRALIZADO_DISPONIBLE = False
    print("⚠ Sistema centralizado no disponible para sprites")

# ════════════════════════════════════════════════════════════════════════════
# CLASE BASE PARA SPRITES ANIMADOS
# ════════════════════════════════════════════════════════════════════════════

class SpriteAnimado:
    """Clase base para manejar sprites animados con dirección - SISTEMA CENTRALIZADO"""
    
    def __init__(self, rect, ruta_sprites, prefijo, num_frames_por_direccion):
        """
        Args:
            rect: pygame.Rect con posición y tamaño
            ruta_sprites: ruta a la carpeta con sprites
            prefijo: prefijo del archivo (ej: "enemy", "player")
            num_frames_por_direccion: cuántos frames tiene cada dirección
        """
        self.rect = rect
        self.ruta_sprites = ruta_sprites
        self.prefijo = prefijo
        self.num_frames = num_frames_por_direccion
        
        # Variables de animación
        self.frame_actual = 0
        self.contador_frame = 0
        self.velocidad_animacion = 5  # Cambiar frame cada X fotogramas
        
        # Dirección actual
        self.direccion = "derecha"
        
        # Sistema centralizado - resolver resolución actual
        self.resolucion_anterior = None
        self._actualizar_resolucion_cache()
        
        # Cargar sprites con tamaño escalado
        self.sprites_izquierda = self._cargar_sprites("left")
        self.sprites_derecha = self._cargar_sprites("right")
        
        # Imagen actual
        if self.sprites_derecha:
            self.image = self.sprites_derecha[0]
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(ROJO_CLARO)
    
    def _actualizar_resolucion_cache(self):
        """Actualiza la caché de resolución desde el sistema centralizado"""
        if SISTEMA_CENTRALIZADO_DISPONIBLE:
            try:
                self.resolucion_actual = get_resolucion_actual()
            except:
                self.resolucion_actual = (800, 600)  # Fallback
        else:
            self.resolucion_actual = (800, 600)  # Fallback
    
    def _calcular_tamaño_escalado(self, tamaño_base):
        """Calcula el tamaño escalado según la resolución actual"""
        if not self.resolucion_actual:
            return tamaño_base
        
        escala_x = self.resolucion_actual[0] / 800  # Resolución base: 800x600
        escala_y = self.resolucion_actual[1] / 600
        
        # Usar la escala menor para mantener proporciones
        escala = min(escala_x, escala_y)
        
        nuevo_ancho = max(int(tamaño_base[0] * escala), 16)  # Mínimo 16 pixels
        nuevo_alto = max(int(tamaño_base[1] * escala), 16)
        
        return (nuevo_ancho, nuevo_alto)
    
    def _cargar_sprites(self, direccion):
        """Carga sprites de una dirección con escalado automático"""
        sprites = []
        
        # Obtener tamaño escalado
        tamaño_escalado = self._calcular_tamaño_escalado((self.rect.width, self.rect.height))
        
        for i in range(1, self.num_frames + 1):
            nombre_archivo = f"{self.prefijo}-{direccion}-{i}.jpg"
            ruta_completa = os.path.join(self.ruta_sprites, nombre_archivo)
            
            try:
                imagen = pygame.image.load(ruta_completa)
                imagen = pygame.transform.scale(imagen, tamaño_escalado)
                sprites.append(imagen)
                print(f"✓ Sprite cargado y escalado ({tamaño_escalado}): {nombre_archivo}")
            except FileNotFoundError:
                print(f"✗ Archivo no encontrado: {nombre_archivo}")
        
        return sprites if sprites else None
    
    def actualizar_animacion(self, velocidad_x, velocidad_y=None):
        """Actualiza frame según dirección y verifica cambios de resolución"""
        
        # Verificar si cambió la resolución
        self._verificar_cambio_resolucion()
        
        # Detectar dirección
        if velocidad_x < 0:
            self.direccion = "izquierda"
            sprites_actuales = self.sprites_izquierda
        elif velocidad_x > 0:
            self.direccion = "derecha"
            sprites_actuales = self.sprites_derecha
        else:
            sprites_actuales = (
                self.sprites_izquierda if self.direccion == "izquierda"
                else self.sprites_derecha
            )
        
        # Animar
        if sprites_actuales:
            self.contador_frame += 1
            if self.contador_frame >= self.velocidad_animacion:
                self.contador_frame = 0
                self.frame_actual = (self.frame_actual + 1) % len(sprites_actuales)
                self.image = sprites_actuales[self.frame_actual]
    
    def _verificar_cambio_resolucion(self):
        """Verifica si cambió la resolución y recarga sprites si es necesario"""
        resolucion_anterior = self.resolucion_actual
        self._actualizar_resolucion_cache()
        
        if self.resolucion_actual != resolucion_anterior:
            print(f"🔄 Resolución cambió para sprite {self.prefijo}: {resolucion_anterior} → {self.resolucion_actual}")
            self._recargar_sprites()

    def _recargar_sprites(self):
        """Recarga sprites al cambiar de tamaño o resolución"""
        print(f"🔄 Recargando sprites para {self.prefijo} con resolución {self.resolucion_actual}")
        self.sprites_izquierda = self._cargar_sprites("left")
        self.sprites_derecha = self._cargar_sprites("right")
        self.frame_actual = 0
        if self.direccion == "izquierda" and self.sprites_izquierda:
            self.image = self.sprites_izquierda[0]
        elif self.sprites_derecha:
            self.image = self.sprites_derecha[0]
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(ROJO_CLARO)
    
    def dibujar(self, pantalla):
        """Dibuja el sprite en la pantalla"""
        pantalla.blit(self.image, self.rect)
    
    def forzar_actualizacion_resolucion(self):
        """Fuerza la actualización de sprites para nueva resolución"""
        print(f"🔄 Forzando actualización de resolución para sprite {self.prefijo}")
        self._actualizar_resolucion_cache()
        self._recargar_sprites()
    
    # ════════════════════════════════════════════════════════════════════════
    # PROPIEDADES PARA COMPATIBILIDAD
    # ════════════════════════════════════════════════════════════════════════
    
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, valor):
        self.rect.x = valor
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, valor):
        self.rect.y = valor
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height
    
    def colliderect(self, otro_rect):
        """Detecta colisión"""
        return self.rect.colliderect(otro_rect)
    
    def clamp_ip(self, rect):
        """Mantiene dentro de los límites"""
        self.rect.clamp_ip(rect)
    
    @property
    def centerx(self):
        return self.rect.centerx
    
    @centerx.setter
    def centerx(self, valor):
        self.rect.centerx = valor
    
    @property
    def centery(self):
        return self.rect.centery
    
    @centery.setter
    def centery(self, valor):
        self.rect.centery = valor
    
    @property
    def left(self):
        return self.rect.left
    
    @left.setter
    def left(self, valor):
        self.rect.left = valor
    
    @property
    def right(self):
        return self.rect.right
    
    @right.setter
    def right(self, valor):
        self.rect.right = valor
    
    @property
    def top(self):
        return self.rect.top
    
    @top.setter
    def top(self, valor):
        self.rect.top = valor
    
    @property
    def bottom(self):
        return self.rect.bottom
    
    @bottom.setter
    def bottom(self, valor):
        self.rect.bottom = valor
    
    def update(self, otro_rect):
        """Actualiza desde otro rectángulo"""
        cambio_tamaño = (otro_rect.width != self.rect.width) or (otro_rect.height != self.rect.height)
        self.rect.topleft = otro_rect.topleft
        self.rect.size = otro_rect.size
        if cambio_tamaño:
            self._recargar_sprites()

# ════════════════════════════════════════════════════════════════════════════
# CLASE ENEMIGO ANIMADO (3 frames por dirección)
# ════════════════════════════════════════════════════════════════════════════

class EnemigoDinamico(SpriteAnimado):
    """Enemigo con 3 frames de animación por dirección"""
    
    def __init__(self, rect, ruta_sprites):
        super().__init__(rect, ruta_sprites, "enemy", 3)
        self.velocidad_animacion = 5

# ════════════════════════════════════════════════════════════════════════════
# CLASE JUGADOR ANIMADO (4 frames por dirección)
# ════════════════════════════════════════════════════════════════════════════

class JugadorDinamico(SpriteAnimado):
    """Jugador con 4 frames de animación por dirección"""
    
    def __init__(self, rect, ruta_sprites):
        super().__init__(rect, ruta_sprites, "player", 4)
        self.velocidad_animacion = 5


# ════════════════════════════════════════════════════════════════════════════
# CLASE PARA MONEDA ANIMADA
# ════════════════════════════════════════════════════════════════════════════

class MonedaDinamica:
    """Moneda animada con rotación de sprites - SISTEMA CENTRALIZADO"""
    
    def __init__(self, rect, ruta_sprites):
        """
        Args:
            rect: pygame.Rect con posición y tamaño
            ruta_sprites: ruta a la carpeta con sprites
        """
        self.rect = rect
        self.ruta_sprites = ruta_sprites
        
        # Variables de animación
        self.frame_actual = 0
        self.contador_frame = 0
        self.velocidad_animacion = 8  # Cambiar frame cada X fotogramas (más alto = más lento)
        
        # Sistema centralizado - resolver resolución actual
        self.resolucion_actual = None
        self._actualizar_resolucion_cache()
        
        # Cargar sprites de coin (coin-1.jpg, coin-2.jpg, etc.)
        self.sprites = self._cargar_sprites()
        
        # Imagen actual
        if self.sprites:
            self.image = self.sprites[0]
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(AMARILLO_CLARO)
    
    def _actualizar_resolucion_cache(self):
        """Actualiza la caché de resolución desde el sistema centralizado"""
        if SISTEMA_CENTRALIZADO_DISPONIBLE:
            try:
                self.resolucion_actual = get_resolucion_actual()
            except:
                self.resolucion_actual = (800, 600)  # Fallback
        else:
            self.resolucion_actual = (800, 600)  # Fallback
    
    def _calcular_tamaño_escalado(self, tamaño_base):
        """Calcula el tamaño escalado según la resolución actual"""
        if not self.resolucion_actual:
            return tamaño_base
        
        escala_x = self.resolucion_actual[0] / 800  # Resolución base: 800x600
        escala_y = self.resolucion_actual[1] / 600
        
        # Usar la escala menor para mantener proporciones
        escala = min(escala_x, escala_y)
        
        nuevo_ancho = max(int(tamaño_base[0] * escala), 12)  # Mínimo 12 pixels para moneda
        nuevo_alto = max(int(tamaño_base[1] * escala), 12)
        
        return (nuevo_ancho, nuevo_alto)
    
    def _cargar_sprites(self):
        """Carga los sprites de moneda numerados con escalado automático"""
        sprites = []
        
        # Obtener tamaño escalado
        tamaño_escalado = self._calcular_tamaño_escalado((self.rect.width, self.rect.height))
        
        for i in range(1, 5):  # coin-1 a coin-4
            ruta = os.path.join(self.ruta_sprites, f"coin-{i}.jpg")
            try:
                img = pygame.image.load(ruta)
                img = pygame.transform.scale(img, tamaño_escalado)
                sprites.append(img)
                print(f"✓ Sprite moneda cargado y escalado ({tamaño_escalado}): coin-{i}.jpg")
            except FileNotFoundError:
                print(f"⚠ No se encontró: {ruta}")
        return sprites

    def _verificar_cambio_resolucion(self):
        """Verifica si cambió la resolución y recarga sprites si es necesario"""
        resolucion_anterior = self.resolucion_actual
        self._actualizar_resolucion_cache()
        
        if self.resolucion_actual != resolucion_anterior:
            print(f"🔄 Resolución cambió para moneda: {resolucion_anterior} → {self.resolucion_actual}")
            self._recargar_sprites()

    def _recargar_sprites(self):
        """Recarga sprites al cambiar de tamaño o resolución"""
        print(f"🔄 Recargando sprites de moneda con resolución {self.resolucion_actual}")
        self.sprites = self._cargar_sprites()
        self.frame_actual = 0
        if self.sprites:
            self.image = self.sprites[0]
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(AMARILLO_CLARO)
    
    def actualizar_animacion(self):
        """Actualiza la animación de la moneda y verifica cambios de resolución"""
        
        # Verificar si cambió la resolución
        self._verificar_cambio_resolucion()
        
        if not self.sprites:
            return
        
        self.contador_frame += 1
        if self.contador_frame >= self.velocidad_animacion:
            self.contador_frame = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.sprites)
            self.image = self.sprites[self.frame_actual]
    
    def dibujar(self, pantalla):
        """Dibuja la moneda en la pantalla"""
        pantalla.blit(self.image, self.rect)
    
    def forzar_actualizacion_resolucion(self):
        """Fuerza la actualización de sprites para nueva resolución"""
        print(f"🔄 Forzando actualización de resolución para moneda")
        self._actualizar_resolucion_cache()
        self._recargar_sprites()
    
    def colliderect(self, otro_rect):
        """Detecta colisión con otro rectángulo"""
        return self.rect.colliderect(otro_rect)
    
    def update(self, otro_rect):
        """Actualiza posición desde otro rectángulo"""
        cambio_tamaño = (otro_rect.width != self.rect.width) or (otro_rect.height != self.rect.height)
        self.rect.topleft = otro_rect.topleft
        self.rect.size = otro_rect.size
        if cambio_tamaño:
            self._recargar_sprites()
    
    # Propiedades para compatibilidad
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, valor):
        self.rect.x = valor
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, valor):
        self.rect.y = valor
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height

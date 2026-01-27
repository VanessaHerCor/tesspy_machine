"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     CÓMO USAR SPRITES EN PYGAME                           ║
║                                                                            ║
║  SPRITES = Imágenes/animaciones que usas en vez de dibujar formas        ║
║                                                                            ║
║  VENTAJAS DE SPRITES:                                                     ║
║  ✓ Gráficos mucho más bonitos y detallados                                ║
║  ✓ Animaciones fluidas (cambiar imagen por fotograma)                     ║
║  ✓ Facilita agregar efectos visuales                                      ║
║                                                                            ║
║  DESVENTAJAS:                                                             ║
║  ✗ Requiere archivos de imagen (.png, .jpg, etc.)                         ║
║  ✗ Usa más memoria                                                        ║
║  ✗ Menos flexible que dibujar (no escala tan bien)                        ║
║                                                                            ║
║  CÓMO OBTENER SPRITES GRATIS:                                             ║
║  1. OpenGameArt.org (sprites 2D gratuitos y CC)                           ║
║  2. Itch.io (búsca "free sprite packs")                                   ║
║  3. Kenney.nl (sprites gratuitos ultra profesionales)                      ║
║  4. FreePik (imágenes vectoriales)                                         ║
║  5. Pixabay/Pexels (fotos gratis para fondo)                              ║
║                                                                            ║
║  ESTRUCTURA MÍNIMA PARA USAR SPRITES:                                     ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame
import os

# ════════════════════════════════════════════════════════════════════════════
# CLASE PARA MANEJAR SPRITES
# ════════════════════════════════════════════════════════════════════════════

class Sprite(pygame.sprite.Sprite):
    """
    Clase para crear un sprite (imagen con comportamiento)
    
    Ejemplo de uso:
        jugador = Sprite('ruta/imagen.png', (100, 100), (200, 200))
        # Ahora puedes mover jugador.rect y dibujarlo
    """
    
    def __init__(self, ruta_imagen, tamaño, posicion=(0, 0)):
        """
        Args:
            ruta_imagen: string con la ruta a la imagen
            tamaño: tupla (ancho, alto)
            posicion: tupla (x, y)
        """
        super().__init__()
        
        self.ruta_original = ruta_imagen
        
        # Intentar cargar la imagen
        if os.path.exists(ruta_imagen):
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
            print(f"✓ Sprite cargado: {ruta_imagen}")
        else:
            print(f"✗ Archivo no encontrado: {ruta_imagen}")
            print(f"  Crea una imagen PNG en esa ubicación")
            # Crear un rectángulo de color como fallback
            self.image = pygame.Surface(tamaño)
            self.image.fill((255, 0, 0))  # Rojo como placeholder
        
        # Redimensionar a el tamaño deseado
        self.image = pygame.transform.scale(self.image, tamaño)
        
        # Crear rectángulo para colisiones y posición
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
    
    def dibujar(self, pantalla):
        """Dibuja el sprite en la pantalla"""
        pantalla.blit(self.image, self.rect)


# ════════════════════════════════════════════════════════════════════════════
# EJEMPLO BÁSICO: CARGAR UN SPRITE
# ════════════════════════════════════════════════════════════════════════════

def ejemplo_basico():
    """
    Ejemplo 1: Cargar y mostrar un sprite simple
    """
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # OPCIÓN 1: Crear sprite desde imagen
    # (necesitas una imagen en 'assets/jugador.png')
    # jugador = Sprite('assets/jugador.png', (50, 50), (100, 100))
    
    # OPCIÓN 2: Por ahora, usar formas (más adelante agregas imágenes)
    jugador_rect = pygame.Rect(100, 100, 50, 50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Mover con teclas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            jugador_rect.x += 5
        
        # Dibujar
        pantalla.fill((0, 0, 0))
        pygame.draw.rect(pantalla, (255, 0, 0), jugador_rect)
        
        # Mostrar instrucción
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render("Crea carpeta 'assets' y agrega imágenes PNG", True, (255, 255, 255))
        pantalla.blit(texto, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


# ════════════════════════════════════════════════════════════════════════════
# EJEMPLO INTERMEDIO: ANIMACIÓN CON SPRITE SHEET
# ════════════════════════════════════════════════════════════════════════════

class SpriteAnimado(pygame.sprite.Sprite):
    """
    Sprite que puede cambiar entre múltiples imágenes para simular animación
    
    Un "sprite sheet" es una sola imagen con varias frames (fotogramas)
    Por ejemplo: un personaje corriendo tiene 6 frames de animación
    """
    
    def __init__(self, ruta_spritesheet, filas, columnas, tamaño_final, posicion=(0, 0)):
        """
        Args:
            ruta_spritesheet: imagen con todos los frames
            filas: cuántas filas tiene la hoja
            columnas: cuántas columnas tiene la hoja
            tamaño_final: tupla (ancho, alto) para redimensionar
            posicion: (x, y)
        """
        super().__init__()
        
        self.frames = []
        self.frame_actual = 0
        self.contador = 0
        self.velocidad_animacion = 5  # Cambiar frame cada X fotogramas
        
        try:
            spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
            ancho_sheet = spritesheet.get_width()
            alto_sheet = spritesheet.get_height()
            
            # Calcular tamaño de cada frame
            ancho_frame = ancho_sheet // columnas
            alto_frame = alto_sheet // filas
            
            # Extraer cada frame
            for fila in range(filas):
                for col in range(columnas):
                    x = col * ancho_frame
                    y = fila * alto_frame
                    frame = spritesheet.subsurface(
                        pygame.Rect(x, y, ancho_frame, alto_frame)
                    )
                    frame = pygame.transform.scale(frame, tamaño_final)
                    self.frames.append(frame)
            
            print(f"✓ AnimaciÃ³n cargada: {len(self.frames)} frames")
        
        except Exception as e:
            print(f"✗ Error cargando sprite sheet: {e}")
            # Crear frame placeholder
            placeholder = pygame.Surface(tamaño_final)
            placeholder.fill((255, 0, 255))
            self.frames = [placeholder]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
    
    def actualizar(self):
        """Actualiza la animación (llamar cada fotograma del juego)"""
        self.contador += 1
        if self.contador >= self.velocidad_animacion:
            self.contador = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.image = self.frames[self.frame_actual]
    
    def dibujar(self, pantalla):
        """Dibuja el sprite en la pantalla"""
        pantalla.blit(self.image, self.rect)


# ════════════════════════════════════════════════════════════════════════════
# EJEMPLO AVANZADO: JUEGO CON SPRITES
# ════════════════════════════════════════════════════════════════════════════

def crear_carpeta_assets():
    """Crea la carpeta 'assets' si no existe y explica qué meter ahí"""
    if not os.path.exists('assets'):
        os.makedirs('assets')
        
        print("\n" + "="*70)
        print("📁 Carpeta 'assets' creada!")
        print("="*70)
        print("\nAhora necesitas agregar imágenes PNG:")
        print("\n  assets/")
        print("  ├── jugador.png          (tamaño sugerido: 50x50 px)")
        print("  ├── enemigo.png          (tamaño sugerido: 40x40 px)")
        print("  ├── moneda.png           (tamaño sugerido: 25x25 px)")
        print("  ├── fondo.png            (tamaño: 800x600 px)")
        print("  └── animacion.png        (sprite sheet con múltiples frames)")
        print("\n📌 DÓNDE DESCARGAR SPRITES GRATIS:")
        print("  - OpenGameArt.org")
        print("  - Itch.io (busca: 'free sprite packs')")
        print("  - Kenney.nl (sprites profesionales)")
        print("  - Pixabay.com (fotos gratis)")
        print("="*70 + "\n")


# ════════════════════════════════════════════════════════════════════════════
# COMPARATIVA: FORMAS vs SPRITES
# ════════════════════════════════════════════════════════════════════════════

COMPARATIVA = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    FORMAS vs SPRITES vs HÍBRIDO                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  DIBUJAR CON FUNCIONES (círculos, rectángulos, polígonos):             │
│  ✓ No necesitas archivos                                                │
│  ✓ Escala perfecta en cualquier resolución                              │
│  ✓ Mucho más rápido de codificar                                        │
│  ✓ Perfecto para prototipado                                            │
│  ✗ Menos visual                                                          │
│  ✗ No puedes animar fácilmente                                          │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  SPRITES (Imágenes PNG/JPG):                                            │
│  ✓ Gráficos hermosos y detallados                                       │
│  ✓ Fácil de animar                                                      │
│  ✓ Puedes contratar artistas                                            │
│  ✗ Necesitas archivos                                                   │
│  ✗ Más lento de cargar                                                  │
│  ✗ Usa más memoria                                                      │
│  ✗ Escalado puede verse pixelado                                        │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  RECOMENDACIÓN (MEJOR DE AMBOS):                                        │
│  ✓ Usa FORMAS para prototipado y juegos simples                         │
│  ✓ Usa SPRITES solo cuando tengas arte listo                            │
│  ✓ O... usa AMBOS: sprites para personajes, formas para UI              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
"""

if __name__ == "__main__":
    print(COMPARATIVA)
    crear_carpeta_assets()

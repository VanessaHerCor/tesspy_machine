# 🎮 Ladrón de Magia - PyGame AI

Un juego tipo **"Avoid & Collect"** desarrollado en PyGame con **4 sistemas diferentes de Inteligencia Artificial** para controlar enemigos inteligentes.

---

## 📋 Tabla de Contenidos

1. [Características](#características)
2. [Instalación](#instalación)
3. [Cómo Jugar](#cómo-jugar)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Sistemas de IA](#sistemas-de-ia)
6. [Cómo Funciona el Código](#cómo-funciona-el-código)
7. [Cambiar Entre IAs](#cambiar-entre-ias)

---

## ✨ Características

✅ **4 Sistemas de IA Diferentes:**
- Persecución Inteligente (Básica)
- Patrones Aleatorios (Impredecible)
- Red Neuronal Simple (Aprende)
- IA Híbrida (Combina todas)

✅ **Sistema de Sprites Animados:**
- Jugador con animaciones personalizadas
- Enemigo dinámico
- Moneda animada

✅ **Sistema de Audio:**
- Música de fondo
- Efectos de sonido para monedas, fallos y game over

✅ **Menús y Pantallas:**
- Pantalla de título
- Instrucciones del juego
- Respawn cuando pierdes vidas
- Game Over con opción de reintentar

✅ **Sistema de Puntuación y Vidas:**
- Seguimiento de score en tiempo real
- Sistema de 5 vidas
- Pantalla de respawn entre vidas

---

## 🚀 Instalación

### Requisitos Previos
- **Python 3.8+**
- **pip** (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto:**
```bash
cd Homework/PyGame
```

2. **Crear un ambiente virtual (recomendado):**
```bash
python -m venv .venv
```

3. **Activar el ambiente virtual:**

   **En Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **En Windows (CMD):**
   ```cmd
   .venv\Scripts\activate.bat
   ```

   **En macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Instalar dependencias:**
```bash
pip install pygame numpy
```

5. **Ejecutar el juego:**
```bash
python app_modular.py
```

---

## 🎮 Cómo Jugar

### Controles

| Tecla | Acción |
|-------|--------|
| **Flechas ⬅️⬆️➡️⬇️** | Mover al jugador |
| **Enter** | Seleccionar opciones en menús |
| **ESC** | Salir del juego |

### Objetivo

1. **Recoge las monedas** 💰 para aumentar tu puntuación
2. **Evita al enemigo** 👹 que te persigue
3. **Tienes 5 vidas** - perderás una si el enemigo te toca
4. **Game Over** cuando pierdes todas las vidas

### Gameplay Loop

```
┌─────────────────────────┐
│   RECOGER MONEDA        │
│   +1 Score              │
│   Nueva moneda spawn    │
└────────────┬────────────┘
             │
             ▼
    ¿Enemigo te toca?
    │                │
   SÍ               NO
    │                │
    ▼                ▼
 -1 Vida       Siguiente frame
    │
    ▼
 ¿Vidas > 0?
 │       │
SÍ      NO
 │       │
 │       ▼
 │    GAME OVER
 │
 └─► Continuar
```

---

## 📁 Estructura del Proyecto

```
Homework/PyGame/
│
├── 📄 app_modular.py                    ← ARCHIVO PRINCIPAL DEL JUEGO
├── 📄 README.md                         ← Este archivo
├── 📄 README_IA.md                      ← Guía detallada de IAs
│
└── 📁 configuracion/
    └── 📁 config/
        ├── 🤖 inteligencia_artificial.py ← TODA LA IA DEL JUEGO
        │   ├── PerseguirInteligente (IA Básica)
        │   ├── IAPatronesAleatorios (IA Impredecible)
        │   ├── RedNeuronalSimple (IA que Aprende)
        │   ├── IAHibrida (Combinación de todas)
        │   └── crear_enemigo_inteligente()
        │
        ├── 🎨 sprites_animados.py        ← Clases de animación
        │   ├── JugadorDinamico
        │   ├── EnemigoDinamico
        │   └── MonedaDinamica
        │
        ├── 🌈 colores.py                 ← Paleta de colores
        │
        ├── ⚙️ caracteristicas.py         ← Configuración del juego
        │   ├── Resoluciones
        │   ├── FPS
        │   ├── Tamaños de fuentes
        │   └── Funciones auxiliares
        │
        ├── 🎬 pantallas.py               ← Menús y pantallas
        │   ├── pantalla_titulo()
        │   ├── pantalla_instrucciones()
        │   ├── pantalla_game_over()
        │   └── pantalla_respawn()
        │
        └── 🔊 sonidos.py                 ← Sistema de audio
            ├── cargar_sonidos()
            ├── reproducir_sonido_moneda()
            ├── reproducir_sonido_game_over()
            └── reproducir_sonido_failed()
│
├── 📁 configuracion/sprites/            ← Assets de sprites
│   ├── jugador/
│   ├── enemigo/
│   └── moneda/
│
└── 📁 configuracion/sonidos/            ← Assets de audio
    ├── moneda.wav
    ├── game_over.wav
    ├── failed.wav
    └── musica_fondo.wav
```

---

## 🧠 Sistemas de IA

### 1️⃣ Persecución Inteligente (Básica) - `PerseguirInteligente`

**Clase:** `configuracion.config.inteligencia_artificial.PerseguirInteligente`

**Cómo funciona:**
- Predice hacia dónde se mueve el jugador
- Mantiene un historial de las últimas 10 posiciones
- Calcula la velocidad del jugador y se adelanta
- ¡Persigue el destino, no la posición actual!

**Parámetros:**
```python
enemigo_ia = PerseguirInteligente(velocidad_base=5)
movimiento = enemigo_ia.calcular_movimiento(
    pos_enemigo=(x, y),
    pos_jugador=(jx, jy),
    pos_jugador_anterior=(jx_ant, jy_ant)
)
```

**Características:**
- ⚡ Velocidad: Rápido
- ⭐⭐ Inteligencia: Media
- ❌ Aprendizaje: No aprende
- ✅ Predicción: Sí predice movimientos

---

### 2️⃣ Patrones Aleatorios - `IAPatronesAleatorios` ⭐ RECOMENDADA

**Clase:** `configuracion.config.inteligencia_artificial.IAPatronesAleatorios`

**Cómo funciona:**
- Cambia de estrategia cada 2 segundos (120 frames)
- Elige aleatoriamente entre 4 patrones:
  - **Perseguir** (60% de probabilidad)
  - **Flanquear** (15%) - ataca desde los lados
  - **Circundar** (15%) - orbita alrededor
  - **Aleatorio** (10%) - movimiento caótico

**Parámetros:**
```python
enemigo_ia = IAPatronesAleatorios(velocidad_base=5)
movimiento = enemigo_ia.calcular_movimiento(
    pos_enemigo=(x, y),
    pos_jugador=(jx, jy),
    tiempo_actual=tiempo_juego
)
```

**Características:**
- ⚡⚡ Velocidad: Muy rápido
- ⭐⭐⭐ Inteligencia: Alta
- ❌ Aprendizaje: No aprende
- ❌ Predictibilidad: Muy impredecible (¡es lo bueno!)

---

### 3️⃣ Red Neuronal Simple - `RedNeuronalSimple`

**Clase:** `configuracion.config.inteligencia_artificial.RedNeuronalSimple`

**Cómo funciona:**
- Red neuronal artificial con 3 capas:
  - Entrada: 5 neuronas
  - Oculta: 8 neuronas
  - Salida: 2 neuronas
- Funciones de activación: Sigmoide → TanH
- **EVOLUCIONA** después de cada captura
- Usa algoritmo genético simple

**Estructura:**
```
Input (5) → Hidden (8) → Output (2)
  │           │           │
  ├─ dx      ├─ Sigmoide ├─ dx (velocidad)
  ├─ dy      │           └─ dy (velocidad)
  ├─ dist    └─ TanH
  ├─ vel_x
  └─ vel_y
```

**Parámetros:**
```python
enemigo_ia = RedNeuronalSimple(velocidad_base=5)
movimiento = enemigo_ia.calcular_movimiento(
    pos_enemigo=(x, y),
    pos_jugador=(jx, jy)
)
enemigo_ia.captura_exitosa()  # Evoluciona después de capturar
```

**Características:**
- ⚡ Velocidad: Rápido
- ⭐⭐⭐⭐ Inteligencia: Muy alta
- ✅ Aprendizaje: Sí, evoluciona
- 🔴 Complejidad: Muy compleja

---

### 4️⃣ IA Híbrida - `IAHibrida`

**Clase:** `configuracion.config.inteligencia_artificial.IAHibrida`

**Cómo funciona:**
- Combina las 3 IAs anteriores según la distancia al jugador
- Elige estrategia dinámicamente:

| Distancia | Estrategia | Uso |
|-----------|-----------|-----|
| < 150px | Red Neuronal | Maniobras precisas |
| 150-300px | Patrones | Impredecible |
| > 300px | Persecución | Ataque directo |

**Parámetros:**
```python
enemigo_ia = IAHibrida(velocidad_base=5)
movimiento = enemigo_ia.calcular_movimiento(
    pos_enemigo=(x, y),
    pos_jugador=(jx, jy),
    tiempo_actual=tiempo_juego,
    pos_jugador_anterior=(jx_ant, jy_ant)
)
```

**Características:**
- ⚡⚡ Velocidad: Rápido
- ⭐⭐⭐⭐⭐ Inteligencia: Máxima
- ✅ Aprendizaje: Sí, red neuronal evoluciona
- ✅ Adaptabilidad: Cambia según situación

---

## 💻 Cómo Funciona el Código

### `app_modular.py` - El Archivo Principal

#### 1️⃣ **Imports y Configuración (Líneas 1-80)**
```python
# Importar módulos de IA
from configuracion.config.inteligencia_artificial import crear_enemigo_inteligente

# Importar sistemas de sprites, sonidos, pantallas, etc.
from configuracion.config.sprites_animados import JugadorDinamico, EnemigoDinamico
from configuracion.config.sonidos import *
```

#### 2️⃣ **Inicializar Pygame (Líneas 85-150)**
```python
pygame.init()
inicializar_audio()
sonidos = cargar_sonidos()
pantalla = crear_ventana(RESOLUCION_DEFAULT)
```

#### 3️⃣ **Crear Enemigo con IA (Líneas 165-170)**
```python
enemigo_ia = crear_enemigo_inteligente("patrones", velocidad_enemigo)
print("🧠 IA cargada")
```

Aquí es donde **eliges qué IA usar**. Opciones:
- `"basica"` → Persecución Inteligente
- `"patrones"` → Patrones Aleatorios ⭐
- `"neuronal"` → Red Neuronal
- `"hibrida"` → IA Híbrida

#### 4️⃣ **Loop Principal (Líneas 230-390)**

**A) Movimiento del Jugador (Líneas 240-260):**
```python
keys = pygame.key.get_pressed()

if keys[pygame.K_LEFT]:
    jugador.x -= velocidad_jugador
if keys[pygame.K_RIGHT]:
    jugador.x += velocidad_jugador
# ... etc con UP y DOWN
```

**B) Cálculo de IA (Líneas 280-320):**
```python
# El código detecta automáticamente qué IA estás usando
tipo_ia = type(enemigo_ia).__name__

if tipo_ia == "IAPatronesAleatorios":
    movimiento_ia = enemigo_ia.calcular_movimiento(
        pos_enemigo, pos_jugador, tiempo_juego
    )
```

**C) Aplicar Movimiento del Enemigo (Líneas 325-335):**
```python
velocidad_enemigo_x = movimiento_ia[0]
velocidad_enemigo_y = movimiento_ia[1]

enemigo.x += velocidad_enemigo_x
enemigo.y += velocidad_enemigo_y
```

**D) Detectar Colisiones (Líneas 350-385):**
```python
# Recoger moneda
if jugador.colliderect(moneda):
    score += 1
    reproducir_sonido_moneda(sonidos)
    respawn_moneda()

# Enemigo toca jugador
if jugador.colliderect(enemigo):
    enemigo_ia.captura_exitosa()  # IA evoluciona
    vidas -= 1
```

**E) Renderizado (Líneas 390-410):**
```python
pantalla.fill(NEGRO)
jugador.dibujar(pantalla)
moneda.dibujar(pantalla)
enemigo.dibujar(pantalla)
texto_score = fuente.render(f"Score: {score}", True, BLANCO)
pantalla.blit(texto_score, (10, 10))
pygame.display.flip()
```

---

### `inteligencia_artificial.py` - El Corazón de la IA

#### **Flujo General:**
```
Entrada:
  pos_enemigo = (x, y)
  pos_jugador = (x, y)
  tiempo_actual (opcional)
  
        ↓
        
Procesamiento (según IA):
  - Calcular dirección
  - Aplicar estrategia
  - Normalizar velocidad
  
        ↓
        
Salida:
  (dx, dy) = movimiento a aplicar
```

#### **Clase `PerseguirInteligente`:**
```python
class PerseguirInteligente:
    def calcular_movimiento(self, pos_enemigo, pos_jugador, pos_anterior):
        # 1. Guardar historial del jugador
        self.historyal.append(pos_jugador)
        
        # 2. Calcular velocidad del jugador
        vel_x = pos_actual[0] - pos_anterior[0]
        vel_y = pos_actual[1] - pos_anterior[1]
        
        # 3. Predecir posición futura
        pos_predicha = (
            pos_jugador[0] + vel_x * 3,
            pos_jugador[1] + vel_y * 3
        )
        
        # 4. Calcular dirección hacia predicción
        dx = pos_predicha[0] - pos_enemigo[0]
        dy = pos_predicha[1] - pos_enemigo[1]
        
        # 5. Normalizar y aplicar velocidad
        distancia = sqrt(dx² + dy²)
        return (
            (dx/distancia) * velocidad_base,
            (dy/distancia) * velocidad_base
        )
```

#### **Clase `RedNeuronalSimple`:**
```python
class RedNeuronalSimple:
    def __init__(self):
        # Inicializar pesos aleatoriamente
        self.pesos_entrada_oculta = random(5, 8)
        self.pesos_oculta_salida = random(8, 2)
        
    def calcular_movimiento(self, pos_enemigo, pos_jugador):
        # 1. Preparar entrada (5 valores normalizados)
        entrada = [dx_norm, dy_norm, dist_norm, vel_x, vel_y]
        
        # 2. Propagar por capa oculta (con sigmoide)
        z1 = entrada · pesos_entrada + sesgo_oculta
        a1 = sigmoide(z1)
        
        # 3. Propagar por capa salida (con tanh)
        z2 = a1 · pesos_oculta + sesgo_salida
        salida = tanh(z2)  # Rango: [-1, 1]
        
        # 4. Combinar con persecución base (50-50)
        nuevo_dx = (dx_norm * 0.5 + salida[0] * 0.5) * velocidad
        nuevo_dy = (dy_norm * 0.5 + salida[1] * 0.5) * velocidad
        
        return (nuevo_dx, nuevo_dy)
    
    def captura_exitosa(self):
        # Calcular fitness basado en tiempo de captura
        fitness = 1 - (tiempo_captura / tiempo_maximo)
        
        # Evolucionar con mutación
        if fitness > 0.7:
            mutacion = 0.05  # Cambios pequeños
        else:
            mutacion = 0.2   # Cambios grandes
        
        # Aplicar mutación a pesos
        pesos += random_normal() * mutacion
```

---

## 🎛️ Cambiar Entre IAs

### Opción 1: Cambiar en `app_modular.py`

Busca la línea ~165:

```python
# ❌ Esto:
# enemigo_ia = crear_enemigo_inteligente("patrones", velocidad_enemigo)

# ✅ Cambia a esto:
enemigo_ia = crear_enemigo_inteligente("basica", velocidad_enemigo)
# O "neuronal", o "hibrida"
```

### Opción 2: Crear Selector de IA

```python
# Después de crear la ventana, pide al usuario que elija:
print("Elige una IA:")
print("1. Básica (persecución inteligente)")
print("2. Patrones (aleatorio)")
print("3. Neuronal (aprende)")
print("4. Híbrida (combina todas)")

opcion = input("Tu opción (1-4): ")

ia_types = {"1": "basica", "2": "patrones", "3": "neuronal", "4": "hibrida"}
enemigo_ia = crear_enemigo_inteligente(ia_types[opcion], velocidad_enemigo)
```

---

## 🔧 Personalización

### Cambiar Velocidad del Enemigo

En `app_modular.py`, línea ~165:

```python
enemigo_ia = crear_enemigo_inteligente("patrones", velocidad=8)  # ← Cambiar aquí
```

### Cambiar Vidas Iniciales

En `app_modular.py`, línea ~180:

```python
vidas = 5  # ← Cambiar a lo que quieras
```

### Cambiar Dificultad de Red Neuronal

En `inteligencia_artificial.py`, línea ~280:

```python
# Balance actual: 50-50
nuevo_dx = (dx_norm * 0.5 + salida[0] * 0.5) * velocidad

# Para MÁS FÁCIL: 70-30
nuevo_dx = (dx_norm * 0.7 + salida[0] * 0.3) * velocidad

# Para MÁS DIFÍCIL: 30-70
nuevo_dx = (dx_norm * 0.3 + salida[0] * 0.7) * velocidad
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pygame'"

```bash
pip install pygame
```

### Error: "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy
```

### El juego va muy lento

- Reduce la resolución en `caracteristicas.py`
- Desactiva algunos efectos de sonido en `sonidos.py`
- Reduce FPS a 30 en lugar de 60

### El enemigo no persigue

Verifica que estés usando la IA correcta en `app_modular.py`:
```python
enemigo_ia = crear_enemigo_inteligente("patrones", velocidad_enemigo)
```

---

## 📚 Documentación Adicional

Para información más detallada sobre el sistema de IA, consulta **`README_IA.md`**

Contiene:
- Explicaciones detalladas de cada algoritmo
- Diagramas de flujo
- Matemáticas de la red neuronal
- Ejemplos de código avanzado

---

## 👨‍💻 Autor

Desarrollado como proyecto educativo para aprender PyGame e Inteligencia Artificial.

---

## 📄 Licencia

Uso libre para propósitos educativos.

---

**¡Diviértete jugando y experimenta con las diferentes IAs!** 🎮🤖

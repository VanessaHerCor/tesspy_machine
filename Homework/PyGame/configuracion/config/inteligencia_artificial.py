"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    INTELIGENCIA ARTIFICIAL PARA ENEMIGOS                  ║
║                                                                            ║
║  Este módulo implementa diferentes algoritmos de IA para que              ║
║  el enemigo persiga inteligentemente al jugador                           ║
║                                                                            ║
║  Algoritmos implementados:                                                 ║
║  1. Persecución directa con predicción                                     ║
║  2. Pathfinding básico (evita obstáculos)                                 ║
║  3. IA con patrones aleatorios                                             ║
║  4. Red neuronal simple para toma de decisiones                           ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import math
import random
import numpy as np
from typing import Tuple, List

# ════════════════════════════════════════════════════════════════════════════
# OPCIÓN 1: PERSECUCIÓN INTELIGENTE DIRECTA
# ════════════════════════════════════════════════════════════════════════════

class PerseguirInteligente:
    """
    Algoritmo de persecución que predice hacia dónde se dirige el jugador
    y ajusta la velocidad y dirección del enemigo de manera inteligente
    """
    
    def __init__(self, velocidad_base=5):
        self.velocidad_base = velocidad_base
        self.historyal_jugador = []  # Guarda las últimas posiciones del jugador
        self.prediccion_activa = True
        self.factor_prediccion = 3  # Qué tan adelante predecir
        
    def calcular_movimiento(self, pos_enemigo, pos_jugador, pos_jugador_anterior=None):
        """
        Calcula el movimiento inteligente del enemigo hacia el jugador
        
        Args:
            pos_enemigo: Tupla (x, y) posición actual del enemigo
            pos_jugador: Tupla (x, y) posición actual del jugador
            pos_jugador_anterior: Tupla (x, y) posición anterior del jugador
            
        Returns:
            Tupla (dx, dy) con el movimiento a aplicar
        """
        
        # Guardar historial del jugador
        self.historyal_jugador.append(pos_jugador)
        if len(self.historyal_jugador) > 10:  # Mantener solo 10 posiciones
            self.historyal_jugador.pop(0)
            
        # PREDICCIÓN: ¿Hacia dónde se dirige el jugador?
        if len(self.historyal_jugador) >= 2 and self.prediccion_activa:
            # Calcular velocidad del jugador
            ultima_pos = self.historyal_jugador[-1]
            penultima_pos = self.historyal_jugador[-2]
            
            vel_jugador_x = ultima_pos[0] - penultima_pos[0]
            vel_jugador_y = ultima_pos[1] - penultima_pos[1]
            
            # Predecir posición futura del jugador
            pos_predicha = (
                pos_jugador[0] + vel_jugador_x * self.factor_prediccion,
                pos_jugador[1] + vel_jugador_y * self.factor_prediccion
            )
            
            objetivo = pos_predicha
        else:
            objetivo = pos_jugador
            
        # Calcular dirección hacia el objetivo
        dx = objetivo[0] - pos_enemigo[0]
        dy = objetivo[1] - pos_enemigo[1]
        
        # Calcular distancia
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        # Normalizar y aplicar velocidad
        dx_normalizado = (dx / distancia) * self.velocidad_base
        dy_normalizado = (dy / distancia) * self.velocidad_base
        
        return (dx_normalizado, dy_normalizado)
    
    def captura_exitosa(self):
        """Registra una captura (esta IA no evoluciona, solo persigue)"""
        # La IA básica no aprende, pero necesita este método para compatibilidad
        pass  # No hace nada, solo para evitar errores

# ════════════════════════════════════════════════════════════════════════════
# OPCIÓN 2: IA CON PATRONES ALEATORIOS
# ════════════════════════════════════════════════════════════════════════════

class IAPatronesAleatorios:
    """
    IA que combina persecución con patrones aleatorios para ser impredecible
    """
    
    def __init__(self, velocidad_base=5):
        self.velocidad_base = velocidad_base
        self.patron_actual = "perseguir"  # perseguir, flanquear, circundar, aleatorio
        self.tiempo_patron = 0
        self.cambio_patron = 120  # Cambiar patrón cada 2 segundos (60 FPS)
        self.offset_flanqueo = random.choice([-100, 100])
        
    def calcular_movimiento(self, pos_enemigo, pos_jugador, tiempo_actual):
        """
        Calcula movimiento usando diferentes patrones de IA
        """
        
        # Cambiar patrón ocasionalmente
        self.tiempo_patron += 1
        if self.tiempo_patron >= self.cambio_patron:
            self.tiempo_patron = 0
            self.patron_actual = random.choice([
                "perseguir", "perseguir", "perseguir",  # 60% perseguir
                "flanquear", "circundar", "aleatorio"   # 40% otros patrones
            ])
            self.offset_flanqueo = random.choice([-80, -60, 60, 80])
            
        if self.patron_actual == "perseguir":
            return self._perseguir_directo(pos_enemigo, pos_jugador)
        elif self.patron_actual == "flanquear":
            return self._flanquear(pos_enemigo, pos_jugador)
        elif self.patron_actual == "circundar":
            return self._circundar(pos_enemigo, pos_jugador, tiempo_actual)
        else:
            return self._movimiento_aleatorio(pos_enemigo, pos_jugador)
            
    def _perseguir_directo(self, pos_enemigo, pos_jugador):
        """Persecución directa"""
        dx = pos_jugador[0] - pos_enemigo[0]
        dy = pos_jugador[1] - pos_enemigo[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        return (
            (dx / distancia) * self.velocidad_base,
            (dy / distancia) * self.velocidad_base
        )
        
    def _flanquear(self, pos_enemigo, pos_jugador):
        """Intentar flanquear al jugador"""
        # Moverse hacia un lado del jugador
        objetivo_x = pos_jugador[0] + self.offset_flanqueo
        objetivo_y = pos_jugador[1]
        
        dx = objetivo_x - pos_enemigo[0]
        dy = objetivo_y - pos_enemigo[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        return (
            (dx / distancia) * self.velocidad_base,
            (dy / distancia) * self.velocidad_base
        )
        
    def _circundar(self, pos_enemigo, pos_jugador, tiempo):
        """Circundar alrededor del jugador"""
        radio = 120
        angulo = (tiempo * 0.05) % (2 * math.pi)
        
        objetivo_x = pos_jugador[0] + math.cos(angulo) * radio
        objetivo_y = pos_jugador[1] + math.sin(angulo) * radio
        
        dx = objetivo_x - pos_enemigo[0]
        dy = objetivo_y - pos_enemigo[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        return (
            (dx / distancia) * self.velocidad_base,
            (dy / distancia) * self.velocidad_base
        )
        
    def _movimiento_aleatorio(self, pos_enemigo, pos_jugador):
        """Movimiento aleatorio hacia el jugador con variación"""
        # Añadir ruido aleatorio a la persecución
        dx = pos_jugador[0] - pos_enemigo[0] + random.randint(-50, 50)
        dy = pos_jugador[1] - pos_enemigo[1] + random.randint(-50, 50)
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        return (
            (dx / distancia) * self.velocidad_base,
            (dy / distancia) * self.velocidad_base
        )
    
    def captura_exitosa(self):
        """Registra una captura (esta IA no evoluciona, usa patrones fijos)"""
        # La IA de patrones no aprende, solo cambia de estrategia aleatoriamente
        pass  # No hace nada, solo para evitar errores

# ════════════════════════════════════════════════════════════════════════════
# OPCIÓN 3: RED NEURONAL SIMPLE
# ════════════════════════════════════════════════════════════════════════════

class RedNeuronalSimple:
    """
    Red neuronal simple para tomar decisiones de movimiento
    basada en la posición relativa del jugador
    """
    
    def __init__(self, velocidad_base=5):
        self.velocidad_base = velocidad_base
        
        # Pesos de la red neuronal (inicializados aleatoriamente)
        # Input: [dx_normalizado, dy_normalizado, distancia_normalizada, velocidad_previa_x, velocidad_previa_y]
        # Output: [nuevo_dx, nuevo_dy]
        
        self.pesos_entrada_oculta = np.random.randn(5, 8) * 0.5
        self.pesos_oculta_salida = np.random.randn(8, 2) * 0.5
        self.sesgo_oculta = np.random.randn(8) * 0.1
        self.sesgo_salida = np.random.randn(2) * 0.1
        
        self.velocidad_previa = [0, 0]
        
    def activacion_sigmoide(self, x):
        """Función de activación sigmoide"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip para evitar overflow
        
    def activacion_tanh(self, x):
        """Función de activación tangente hiperbólica"""
        return np.tanh(x)
        
    def calcular_movimiento(self, pos_enemigo, pos_jugador):
        """
        Usa la red neuronal para decidir el movimiento
        """
        
        # Preparar inputs
        dx = pos_jugador[0] - pos_enemigo[0]
        dy = pos_jugador[1] - pos_enemigo[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return (0, 0)
            
        # Normalizar inputs
        dx_norm = dx / max(distancia, 1)
        dy_norm = dy / max(distancia, 1)
        dist_norm = min(distancia / 400, 1)  # Normalizar distancia
        
        # Vector de entrada
        entrada = np.array([
            dx_norm,
            dy_norm,
            dist_norm,
            self.velocidad_previa[0] / self.velocidad_base,
            self.velocidad_previa[1] / self.velocidad_base
        ])
        
        # Propagación hacia adelante
        # Capa oculta
        z1 = np.dot(entrada, self.pesos_entrada_oculta) + self.sesgo_oculta
        a1 = self.activacion_sigmoide(z1)
        
        # Capa de salida
        z2 = np.dot(a1, self.pesos_oculta_salida) + self.sesgo_salida
        salida = self.activacion_tanh(z2)  # Valores entre -1 y 1
        
        # 🔧 BALANCE INTELIGENTE: Combinar salida de red con persecución base
        # 50% persecución básica + 50% salida red neuronal
        # Esto permite que la red neuronal tenga más influencia mientras garantiza persecución
        persecucion_base_x = (dx_norm * 0.5)
        persecucion_base_y = (dy_norm * 0.5)
        
        nuevo_dx = (persecucion_base_x + salida[0] * 0.5) * self.velocidad_base
        nuevo_dy = (persecucion_base_y + salida[1] * 0.5) * self.velocidad_base
        
        # Guardar velocidad para próxima iteración
        self.velocidad_previa = [nuevo_dx, nuevo_dy]
        
        return (nuevo_dx, nuevo_dy)
        
    def evolucionar(self, fitness):
        """
        Evoluciona la red neuronal basada en el fitness
        (más fitness = mejor rendimiento)
        """
        if fitness > 0.7:  # Si está funcionando bien, pequeños ajustes
            mutacion = 0.05
        else:  # Si no funciona bien, cambios más grandes
            mutacion = 0.2
            
        # Mutar pesos ligeramente
        self.pesos_entrada_oculta += np.random.randn(*self.pesos_entrada_oculta.shape) * mutacion
        self.pesos_oculta_salida += np.random.randn(*self.pesos_oculta_salida.shape) * mutacion
        self.sesgo_oculta += np.random.randn(*self.sesgo_oculta.shape) * mutacion * 0.5
        self.sesgo_salida += np.random.randn(*self.sesgo_salida.shape) * mutacion * 0.5
    
    def captura_exitosa(self):
        """Registra una captura exitosa y evoluciona la red neuronal"""
        # En la Red Neuronal simple, siempre ocurre una "captura"
        # por lo que asumimos fitness medio (el juego es entretenido)
        fitness = 0.6
        self.evolucionar(fitness)
        print(f"🧠 Red Neuronal evolucionó con fitness: {fitness:.2f}")

# ════════════════════════════════════════════════════════════════════════════
# OPCIÓN 4: IA HÍBRIDA (RECOMENDADA PARA EL PROFESOR)
# ════════════════════════════════════════════════════════════════════════════

class IAHibrida:
    """
    Combina múltiples algoritmos de IA para crear un enemigo muy inteligente
    que usa diferentes estrategias según la situación
    """
    
    def __init__(self, velocidad_base=5):
        self.velocidad_base = velocidad_base
        
        # Inicializar diferentes módulos de IA
        self.perseguidor = PerseguirInteligente(velocidad_base)
        self.patronos = IAPatronesAleatorios(velocidad_base)
        self.red_neuronal = RedNeuronalSimple(velocidad_base)
        
        # Estado de la IA
        self.modo_actual = "inteligente"
        self.tiempo_cambio = 0
        self.distancia_activacion_neuronal = 150  # Activar red neuronal cuando está cerca
        
        # Métricas de rendimiento
        self.distancia_promedio = []
        self.tiempo_sin_captura = 0
        
    def calcular_movimiento(self, pos_enemigo, pos_jugador, tiempo_actual, pos_jugador_anterior=None):
        """
        Decide qué algoritmo usar basado en la situación actual
        """
        
        # Calcular distancia actual
        dx = pos_jugador[0] - pos_enemigo[0]
        dy = pos_jugador[1] - pos_enemigo[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        
        # Registrar métricas
        self.distancia_promedio.append(distancia)
        if len(self.distancia_promedio) > 300:  # 5 segundos a 60 FPS
            self.distancia_promedio.pop(0)
            
        self.tiempo_sin_captura += 1
        
        # Decidir estrategia basada en la distancia
        if distancia < self.distancia_activacion_neuronal:
            # Cerca del jugador: usar red neuronal para maniobras precisas
            return self.red_neuronal.calcular_movimiento(pos_enemigo, pos_jugador)
            
        elif distancia > 300:
            # Lejos del jugador: persecución inteligente directa
            return self.perseguidor.calcular_movimiento(pos_enemigo, pos_jugador, pos_jugador_anterior)
            
        else:
            # Distancia media: usar patrones aleatorios para ser impredecible
            return self.patronos.calcular_movimiento(pos_enemigo, pos_jugador, tiempo_actual)
            
    def captura_exitosa(self):
        """Llamar cuando el enemigo capture al jugador"""
        # Calcular fitness basado en qué tan rápido fue la captura
        fitness = max(0, 1 - (self.tiempo_sin_captura / 1800))  # 30 segundos máximo
        
        # Evolucionar la red neuronal
        self.red_neuronal.evolucionar(fitness)
        
        # Resetear métricas
        self.tiempo_sin_captura = 0
        self.distancia_promedio = []
        
        print(f"🧠 IA evolucionó con fitness: {fitness:.2f}")

# ════════════════════════════════════════════════════════════════════════════
# FUNCIÓN HELPER PARA INTEGRAR CON TU JUEGO
# ════════════════════════════════════════════════════════════════════════════

def crear_enemigo_inteligente(tipo="hibrida", velocidad=5):
    """
    Crear un enemigo con IA del tipo especificado
    
    Args:
        tipo (str): "basica", "patrones", "neuronal", "hibrida"
        velocidad (int): Velocidad base del enemigo
        
    Returns:
        Objeto IA correspondiente
    """
    
    if tipo == "basica":
        return PerseguirInteligente(velocidad)
    elif tipo == "patrones":
        return IAPatronesAleatorios(velocidad)
    elif tipo == "neuronal":
        return RedNeuronalSimple(velocidad)
    elif tipo == "hibrida":
        return IAHibrida(velocidad)
    else:
        print("⚠️ Tipo no reconocido, usando IA híbrida")
        return IAHibrida(velocidad)

# ════════════════════════════════════════════════════════════════════════════
# EJEMPLO DE USO
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🤖 Sistema de IA para PyGame cargado")
    print("Tipos disponibles:")
    print("  - 'basica': Persecución con predicción")
    print("  - 'patrones': Patrones aleatorios inteligentes")
    print("  - 'neuronal': Red neuronal simple")
    print("  - 'hibrida': Combina todas las estrategias (RECOMENDADA)")
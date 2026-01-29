"""
📹 DETECCIÓN EN TIEMPO REAL CON CÁMARA WEB
Este script simula detección de objetos en tiempo real
similar a lo que harías con YOLO real
"""

import cv2
import numpy as np
import random
import time

class DetectorTiempoReal:
    def __init__(self):
        self.objetos_detectables = ['persona', 'cara', 'mano', 'celular', 'libro']
        self.colores = {
            'persona': (0, 255, 0),
            'cara': (255, 0, 0), 
            'mano': (0, 0, 255),
            'celular': (255, 255, 0),
            'libro': (255, 0, 255)
        }
        self.fps_contador = 0
        self.tiempo_inicio = time.time()
        
    def simular_deteccion(self, frame):
        """Simula detección de objetos en el frame actual"""
        h, w = frame.shape[:2]
        detecciones = []
        
        # Simular 0-3 detecciones aleatorias
        num_detecciones = random.randint(0, 3)
        
        for _ in range(num_detecciones):
            # Generar posición aleatoria
            x = random.randint(50, w - 150)
            y = random.randint(50, h - 150)
            w_obj = random.randint(80, 120)
            h_obj = random.randint(80, 120)
            
            # Generar objeto y confianza aleatoria
            objeto = random.choice(self.objetos_detectables)
            confianza = random.uniform(0.3, 0.95)
            
            detecciones.append({
                'tipo': objeto,
                'bbox': (x, y, w_obj, h_obj),
                'confianza': confianza
            })
        
        return detecciones
    
    def dibujar_detecciones(self, frame, detecciones):
        """Dibuja las detecciones en el frame"""
        frame_resultado = frame.copy()
        
        for det in detecciones:
            if det['confianza'] > 0.5:  # Filtrar por confianza
                x, y, w, h = det['bbox']
                tipo = det['tipo']
                confianza = det['confianza']
                
                color = self.colores.get(tipo, (128, 128, 128))
                
                # Dibujar bounding box
                cv2.rectangle(frame_resultado, (x, y), (x + w, y + h), color, 2)
                
                # Etiqueta
                etiqueta = f"{tipo}: {confianza:.2f}"
                tam_texto = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Fondo de etiqueta
                cv2.rectangle(frame_resultado, (x, y - tam_texto[1] - 10), 
                             (x + tam_texto[0], y), color, -1)
                
                # Texto
                cv2.putText(frame_resultado, etiqueta, (x, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return frame_resultado
    
    def dibujar_fps(self, frame):
        """Dibuja el FPS en el frame"""
        self.fps_contador += 1
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        
        if tiempo_transcurrido >= 1.0:
            fps = self.fps_contador / tiempo_transcurrido
            self.fps_contador = 0
            self.tiempo_inicio = tiempo_actual
        else:
            fps = self.fps_contador / max(tiempo_transcurrido, 0.001)
        
        # Dibujar FPS
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame

def main():
    print("📹 DETECCIÓN EN TIEMPO REAL CON CÁMARA")
    print("=" * 45)
    print()
    print("🎮 Controles:")
    print("   ESPACIO = Pausar/Reanudar")
    print("   ESC     = Salir")
    print("   'r'     = Reiniciar")
    print("   's'     = Capturar pantalla")
    print()
    
    # Intentar abrir la cámara
    print("📷 Intentando abrir la cámara...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        print("💡 Simulando con imagen estática...")
        usar_camara = False
        # Crear una imagen de prueba
        frame_estatico = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)
    else:
        print("✅ Cámara abierta correctamente")
        usar_camara = True
    
    detector = DetectorTiempoReal()
    pausado = False
    captura_numero = 1
    
    print("\n🚀 Iniciando detección en tiempo real...")
    print("   (Las detecciones son simuladas para fines educativos)")
    
    try:
        while True:
            if usar_camara and not pausado:
                ret, frame = cap.read()
                if not ret:
                    print("❌ No se pudo leer de la cámara")
                    break
            elif not usar_camara:
                frame = frame_estatico.copy()
                # Agregar un poco de "movimiento" para simular video
                overlay = np.random.randint(0, 30, frame.shape, dtype=np.uint8)
                frame = cv2.add(frame, overlay)
            else:
                # Pausado - mantener el último frame
                pass
            
            # Simular detección
            if not pausado:
                detecciones = detector.simular_deteccion(frame)
                frame_con_detecciones = detector.dibujar_detecciones(frame, detecciones)
            else:
                frame_con_detecciones = frame.copy()
                cv2.putText(frame_con_detecciones, "PAUSADO", 
                           (frame.shape[1]//2 - 50, frame.shape[0]//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Dibujar FPS y estado
            frame_con_detecciones = detector.dibujar_fps(frame_con_detecciones)
            
            # Dibujar instrucciones
            cv2.putText(frame_con_detecciones, "ESC=Salir, ESPACIO=Pausa, R=Reset, S=Capture", 
                       (10, frame_con_detecciones.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # Mostrar frame
            cv2.imshow('🎯 Detección en Tiempo Real (Simulada)', frame_con_detecciones)
            
            # Manejar teclas
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                print("\n👋 Saliendo...")
                break
            elif key == 32:  # ESPACIO
                pausado = not pausado
                print(f"{'⏸️  Pausado' if pausado else '▶️  Reanudando'}")
            elif key == ord('r'):  # R
                print("🔄 Reiniciando...")
                detector = DetectorTiempoReal()
            elif key == ord('s'):  # S
                filename = f"captura_{captura_numero:03d}.jpg"
                cv2.imwrite(filename, frame_con_detecciones)
                print(f"📸 Captura guardada: {filename}")
                captura_numero += 1
    
    except KeyboardInterrupt:
        print("\n⏹️  Interrumpido por el usuario")
    
    finally:
        # Limpiar
        if usar_camara:
            cap.release()
        cv2.destroyAllWindows()
        print("✅ Recursos liberados correctamente")

if __name__ == "__main__":
    main()
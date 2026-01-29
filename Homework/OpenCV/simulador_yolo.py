"""
🎯 SIMULADOR BÁSICO DE DETECCIÓN DE OBJETOS
Este script simula el funcionamiento básico de YOLO
mostrando cómo se detectan y clasifican objetos
"""

import cv2
import numpy as np
import random

class DetectorBasico:
    def __init__(self):
        self.colores = {
            'persona': (0, 255, 0),      # Verde
            'carro': (255, 0, 0),        # Azul  
            'bicicleta': (0, 0, 255),    # Rojo
            'perro': (255, 255, 0),      # Cyan
            'gato': (255, 0, 255),       # Magenta
            'desconocido': (128, 128, 128)  # Gris
        }
        
        self.confianza_minima = 0.5
    
    def crear_escena_ejemplo(self):
        """Crear una escena simulada con múltiples 'objetos'"""
        img = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # Fondo con gradiente (simular cielo)
        for y in range(200):
            color = int(135 + (120 * y / 200))  # Gradiente azul
            img[y, :] = (color, color // 2, 50)
        
        # Fondo inferior (simular suelo)
        img[200:, :] = (50, 80, 50)  # Verde oscuro
        
        # Objetos simulados (rectángulos con diferentes colores y tamaños)
        objetos = [
            {'tipo': 'persona', 'bbox': (100, 250, 80, 200), 'confianza': 0.87},
            {'tipo': 'carro', 'bbox': (300, 320, 150, 100), 'confianza': 0.92},
            {'tipo': 'bicicleta', 'bbox': (500, 280, 100, 120), 'confianza': 0.76},
            {'tipo': 'perro', 'bbox': (200, 380, 60, 80), 'confianza': 0.65},
            {'tipo': 'gato', 'bbox': (650, 350, 50, 60), 'confianza': 0.58},
            {'tipo': 'desconocido', 'bbox': (50, 150, 70, 70), 'confianza': 0.45}
        ]
        
        # Dibujar los objetos como rectángulos de colores
        for obj in objetos:
            x, y, w, h = obj['bbox']
            tipo = obj['tipo']
            
            # Color base del objeto
            if tipo == 'persona':
                color_obj = (150, 100, 50)  # Color piel
            elif tipo == 'carro':
                color_obj = (200, 200, 200)  # Gris metálico
            elif tipo == 'bicicleta':
                color_obj = (100, 150, 200)  # Azul claro
            elif tipo == 'perro':
                color_obj = (50, 50, 100)   # Marrón
            elif tipo == 'gato':
                color_obj = (80, 80, 80)    # Gris
            else:
                color_obj = (100, 100, 100) # Gris
            
            # Dibujar el objeto
            cv2.rectangle(img, (x, y), (x + w, y + h), color_obj, -1)
            
            # Agregar algunos detalles
            if tipo == 'persona':
                # Cabeza
                cv2.circle(img, (x + w//2, y + 20), 15, (200, 150, 100), -1)
            elif tipo == 'carro':
                # Ventanas
                cv2.rectangle(img, (x + 10, y + 10), (x + w - 10, y + 40), (100, 150, 200), -1)
                # Ruedas
                cv2.circle(img, (x + 20, y + h - 10), 15, (0, 0, 0), -1)
                cv2.circle(img, (x + w - 20, y + h - 10), 15, (0, 0, 0), -1)
        
        return img, objetos
    
    def procesar_detecciones(self, img, objetos):
        """Simular el proceso de detección y clasificación"""
        resultado = img.copy()
        detecciones_validas = []
        
        print(f"🔍 Procesando {len(objetos)} posibles objetos...")
        
        for i, obj in enumerate(objetos):
            tipo = obj['tipo']
            bbox = obj['bbox']
            confianza = obj['confianza']
            
            print(f"   Objeto {i+1}: {tipo} (confianza: {confianza:.2f})")
            
            # Filtrar por confianza mínima
            if confianza >= self.confianza_minima:
                detecciones_validas.append(obj)
                
                # Dibujar bounding box
                x, y, w, h = bbox
                color = self.colores.get(tipo, self.colores['desconocido'])
                
                # Rectángulo principal
                cv2.rectangle(resultado, (x, y), (x + w, y + h), color, 3)
                
                # Etiqueta con fondo
                etiqueta = f"{tipo}: {confianza:.2f}"
                tam_texto = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Fondo de la etiqueta
                cv2.rectangle(resultado, (x, y - tam_texto[1] - 10), 
                             (x + tam_texto[0], y), color, -1)
                
                # Texto de la etiqueta
                cv2.putText(resultado, etiqueta, (x, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            else:
                print(f"      ❌ Descartado (confianza {confianza:.2f} < {self.confianza_minima})")
        
        return resultado, detecciones_validas
    
    def mostrar_estadisticas(self, detecciones):
        """Mostrar estadísticas de las detecciones"""
        print(f"\n📊 ESTADÍSTICAS DE DETECCIÓN:")
        print(f"   Total detectado: {len(detecciones)} objetos")
        
        # Contar por tipo
        conteo = {}
        for det in detecciones:
            tipo = det['tipo']
            conteo[tipo] = conteo.get(tipo, 0) + 1
        
        print("   Por tipo:")
        for tipo, cantidad in conteo.items():
            print(f"     - {tipo}: {cantidad}")
        
        # Confianza promedio
        if detecciones:
            confianza_prom = np.mean([det['confianza'] for det in detecciones])
            print(f"   Confianza promedio: {confianza_prom:.2f}")

def main():
    print("🎯 SIMULADOR DE DETECCIÓN DE OBJETOS (YOLO-like)")
    print("=" * 55)
    
    # Crear detector
    detector = DetectorBasico()
    
    # Crear escena
    print("\n🎨 Generando escena con objetos...")
    img_original, objetos = detector.crear_escena_ejemplo()
    
    print(f"✅ Escena creada con {len(objetos)} objetos potenciales")
    
    # Mostrar imagen original
    cv2.imshow('🖼️  Escena Original', img_original)
    cv2.waitKey(0)
    
    # Procesar detecciones
    print(f"\n🔍 Iniciando detección (confianza mínima: {detector.confianza_minima})...")
    img_resultado, detecciones = detector.procesar_detecciones(img_original, objetos)
    
    # Mostrar estadísticas
    detector.mostrar_estadisticas(detecciones)
    
    # Mostrar resultado final
    print(f"\n👁️  Mostrando resultado final...")
    cv2.imshow('🎯 Detecciones Finales', img_resultado)
    
    # Crear comparación lado a lado
    comparacion = np.hstack((img_original, img_resultado))
    cv2.putText(comparacion, 'ORIGINAL', (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(comparacion, 'CON DETECCIONES', (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow('📊 COMPARACIÓN: Antes vs Después', comparacion)
    
    print("\n✅ ¡Simulación completada!")
    print("💡 Esto es básicamente lo que hace YOLO, pero con miles de objetos reales")
    print("   Presiona cualquier tecla para salir...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
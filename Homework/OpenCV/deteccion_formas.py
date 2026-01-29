"""
🔵 DETECCIÓN DE FORMAS CON OPENCV
Este script te enseña a detectar formas geométricas, 
un paso previo importante para entender YOLO
"""

import cv2
import numpy as np

def detectar_formas(img):
    """Detecta formas geométricas en una imagen"""
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque para reducir ruido
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detectar bordes
    edges = cv2.Canny(blur, 50, 150)
    
    # Encontrar contornos
    contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Imagen para dibujar resultados
    resultado = img.copy()
    
    print(f"🔍 Encontradas {len(contornos)} formas")
    
    for i, contorno in enumerate(contornos):
        # Calcular área
        area = cv2.contourArea(contorno)
        
        # Filtrar contornos muy pequeños
        if area < 500:
            continue
            
        # Aproximar el contorno a una forma poligonal
        epsilon = 0.02 * cv2.arcLength(contorno, True)
        approx = cv2.approxPolyDP(contorno, epsilon, True)
        
        # Determinar qué forma es basándose en el número de vértices
        vertices = len(approx)
        
        # Obtener el rectángulo que encierra la forma
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Clasificar la forma
        if vertices == 3:
            forma = "Triangulo"
            color = (0, 255, 0)  # Verde
        elif vertices == 4:
            # Verificar si es cuadrado o rectángulo
            aspecto = w / float(h)
            if 0.95 <= aspecto <= 1.05:
                forma = "Cuadrado"
            else:
                forma = "Rectangulo"
            color = (255, 0, 0)  # Azul
        elif vertices > 4:
            forma = "Circulo"
            color = (0, 0, 255)  # Rojo
        else:
            forma = "Desconocido"
            color = (128, 128, 128)  # Gris
        
        # Dibujar el contorno y la etiqueta
        cv2.drawContours(resultado, [contorno], -1, color, 2)
        cv2.rectangle(resultado, (x, y), (x + w, y + h), color, 2)
        
        # Agregar texto con la clasificación
        cv2.putText(resultado, f"{forma} ({vertices} vertices)", 
                   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        print(f"   Forma {i+1}: {forma} - Área: {int(area)} - Vértices: {vertices}")
    
    return resultado, edges

def crear_imagen_formas_complejas():
    """Crear una imagen más compleja con múltiples formas"""
    img = np.zeros((500, 600, 3), dtype=np.uint8)
    
    # Fondo oscuro
    img[:, :] = (30, 30, 30)
    
    # Círculo rojo
    cv2.circle(img, (150, 150), 60, (0, 0, 255), -1)
    
    # Rectángulo azul
    cv2.rectangle(img, (300, 80), (450, 180), (255, 0, 0), -1)
    
    # Cuadrado verde
    cv2.rectangle(img, (100, 300), (200, 400), (0, 255, 0), -1)
    
    # Triángulo amarillo
    puntos = np.array([[400, 300], [350, 400], [450, 400]], np.int32)
    cv2.fillPoly(img, [puntos], (0, 255, 255))
    
    # Pentágono violeta
    centro = (500, 350)
    radio = 50
    puntos_pent = []
    for i in range(5):
        angulo = i * 2 * np.pi / 5 - np.pi / 2
        x = int(centro[0] + radio * np.cos(angulo))
        y = int(centro[1] + radio * np.sin(angulo))
        puntos_pent.append([x, y])
    
    cv2.fillPoly(img, [np.array(puntos_pent, np.int32)], (255, 0, 255))
    
    return img

def main():
    print("🔵 DETECCIÓN DE FORMAS GEOMÉTRICAS")
    print("=" * 40)
    
    # Crear imagen con formas
    img = crear_imagen_formas_complejas()
    
    print("\n🎨 Imagen creada con múltiples formas")
    cv2.imshow('Imagen Original', img)
    cv2.waitKey(0)
    
    # Detectar formas
    print("\n🔍 Analizando formas...")
    resultado, edges = detectar_formas(img)
    
    # Mostrar resultados
    print("\n📊 Resultados:")
    cv2.imshow('Bordes Detectados', edges)
    cv2.waitKey(0)
    
    cv2.imshow('🎯 Formas Detectadas y Clasificadas', resultado)
    print("\n✅ ¡Detección completada! Presiona cualquier tecla para salir...")
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
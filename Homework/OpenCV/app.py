import cv2
import numpy as np
import os

def crear_imagen_ejemplo():
    """Crear una imagen de ejemplo si no tenemos ninguna"""
    # Crear una imagen simple con formas geométricas
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Fondo azul
    img[:, :] = (100, 50, 0)
    
    # Rectángulo rojo
    cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 255), -1)
    
    # Círculo verde
    cv2.circle(img, (300, 100), 50, (0, 255, 0), -1)
    
    # Triángulo azul
    points = np.array([[200, 200], [250, 280], [150, 280]], np.int32)
    cv2.fillPoly(img, [points], (255, 0, 0))
    
    return img

def procesar_con_camara():
    """Opción para usar la cámara web"""
    print("🎥 Intentando abrir la cámara...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return None
    
    print("📸 Presiona ESPACIO para capturar una imagen")
    print("❌ Presiona ESC para salir")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow('Camara - Presiona ESPACIO para capturar', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # ESPACIO
            cap.release()
            cv2.destroyAllWindows()
            return frame
    
    cap.release()
    cv2.destroyAllWindows()
    return None

def main():
    print("🖼️  OPENCV - TUTORIAL DE VISIÓN COMPUTACIONAL")
    print("=" * 50)
    
    # Opciones para obtener imagen
    print("\n¿Cómo quieres obtener la imagen?")
    print("1. Usar imagen de ejemplo (formas geométricas)")
    print("2. Usar cámara web")
    print("3. Cargar imagen desde archivo")
    
    opcion = input("\nElige una opción (1-3): ").strip()
    
    img = None
    
    if opcion == "1":
        print("\n🎨 Creando imagen de ejemplo...")
        img = crear_imagen_ejemplo()
        
    elif opcion == "2":
        img = procesar_con_camara()
        
    elif opcion == "3":
        ruta = input("Ingresa la ruta de tu imagen: ").strip()
        if os.path.exists(ruta):
            img = cv2.imread(ruta)
            if img is None:
                print("❌ No se pudo cargar la imagen")
        else:
            print("❌ El archivo no existe")
    
    if img is None:
        print("❌ No se pudo obtener ninguna imagen. Usando imagen de ejemplo...")
        img = crear_imagen_ejemplo()
    
    print(f"\n📏 Tamaño de la imagen: {img.shape}")
    print(f"   - Alto: {img.shape[0]} píxeles")
    print(f"   - Ancho: {img.shape[1]} píxeles") 
    print(f"   - Canales: {img.shape[2]} (BGR)")
    
    # Procesar imagen step by step
    print("\n🔄 Procesando imagen...")
    
    # 1. Redimensionar
    print("1. Redimensionando...")
    img_small = cv2.resize(img, (400, 300))
    
    # 2. Escala de grises
    print("2. Convirtiendo a escala de grises...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3. Desenfoque
    print("3. Aplicando desenfoque...")
    blur = cv2.GaussianBlur(img, (15, 15), 0)
    
    # 4. Detectar bordes
    print("4. Detectando bordes...")
    edges = cv2.Canny(gray, 50, 150)
    
    # Mostrar resultados
    print("\n👁️  Mostrando resultados...")
    print("   - Presiona cualquier tecla para pasar al siguiente")
    print("   - Presiona ESC para salir\n")
    
    cv2.imshow('1. Original', img)
    cv2.waitKey(0)
    
    cv2.imshow('2. Redimensionada', img_small)  
    cv2.waitKey(0)
    
    cv2.imshow('3. Escala de Grises', gray)
    cv2.waitKey(0)
    
    cv2.imshow('4. Desenfocada', blur)
    cv2.waitKey(0)
    
    cv2.imshow('5. Bordes Detectados', edges)
    cv2.waitKey(0)
    
    # Mostrar todo junto
    print("📊 Comparación final de todas las transformaciones...")
    
    # Crear un montage
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Redimensionar todas al mismo tamaño
    h, w = 200, 200
    img_resized = cv2.resize(img, (w, h))
    gray_resized = cv2.resize(gray_3ch, (w, h))
    blur_resized = cv2.resize(blur, (w, h))
    edges_resized = cv2.resize(edges_3ch, (w, h))
    
    # Crear montage 2x2
    top_row = np.hstack((img_resized, gray_resized))
    bottom_row = np.hstack((blur_resized, edges_resized))
    montage = np.vstack((top_row, bottom_row))
    
    # Agregar texto
    cv2.putText(montage, 'Original', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(montage, 'Grises', (w+10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(montage, 'Desenfoque', (10, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(montage, 'Bordes', (w+10, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    cv2.imshow('🎯 RESUMEN - Todas las transformaciones', montage)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    print("\n✅ ¡Tutorial completado!")

if __name__ == "__main__":
    main()
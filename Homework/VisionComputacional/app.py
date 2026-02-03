# ============================================================
# APLICACIÓN PRINCIPAL: DETECCIÓN CON CÁMARA EN TIEMPO REAL
# ============================================================
# Este script permite usar tu modelo entrenado para detectar
# objetos en vivo desde tu cámara web
# ============================================================

from ultralytics import YOLO
import cv2
import os
import time

def main():
    """
    Ejecuta detección en tiempo real desde la cámara web
    """
    print("\n" + "=" * 60)
    print("📹 DETECCIÓN EN VIVO - CÁMARA WEB")
    print("=" * 60)
    
    # =====================================================
    # PASO 1: CARGAR EL MODELO ENTRENADO
    # =====================================================
    model_path = 'runs/detect/train/weights/best.pt'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Error: Modelo no encontrado en {model_path}")
        print("   Solución: Ejecuta primero: python train_custom_model.py")
        return
    
    print(f"\n✅ Cargando modelo: {model_path}")
    try:
        model = YOLO(model_path)
        print("✅ Modelo cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        return
    
    # =====================================================
    # PASO 2: ABRIR LA CÁMARA WEB
    # =====================================================
    print("\n📷 Abriendo cámara web...")
    cap = cv2.VideoCapture(0)  # 0 = cámara predeterminada
    
    if not cap.isOpened():
        print("❌ No se pudo acceder a la cámara web")
        print("   Verifica que tengas una cámara conectada")
        return
    
    print("✅ Cámara abierta")
    print("\n" + "=" * 60)
    print("CONTROLES:")
    print("  SPACE → Capturar imagen")
    print("  Q     → Salir")
    print("=" * 60 + "\n")
    
    # =====================================================
    # PASO 3: PROCESAR FRAMES EN VIVO
    # =====================================================
    frame_count = 0
    fps_start_time = time.time()
    fps_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error leyendo cámara")
            break
        
        # Hacer predicción
        results = model.predict(frame, conf=0.5, verbose=False)
        
        # Obtener frame anotado
        annotated_frame = results[0].plot()
        
        # Calcular FPS (frames por segundo)
        fps_count += 1
        elapsed = time.time() - fps_start_time
        if elapsed >= 1.0:
            fps = fps_count / elapsed
            fps_start_time = time.time()
            fps_count = 0
        else:
            fps = fps_count / elapsed if elapsed > 0 else 0
        
        # Mostrar FPS en pantalla
        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Contar detecciones
        num_detections = 0
        if results[0].boxes is not None:
            num_detections = len(results[0].boxes)
        
        cv2.putText(
            annotated_frame,
            f"Objetos: {num_detections}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Mostrar frame
        cv2.imshow("Detección en Vivo", annotated_frame)
        
        # Esperar input del usuario
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):  # Presionar 'Q' para salir
            print("\n👋 Saliendo...")
            break
        
        elif key == ord(' '):  # Presionar SPACE para capturar
            # Crear carpeta de capturas si no existe
            os.makedirs('cam_capture', exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"cam_capture/capture_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"✅ Imagen capturada: {filename}")
        
        frame_count += 1
    
    # =====================================================
    # PASO 4: CERRAR CÁMARA
    # =====================================================
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✅ Procesados {frame_count} frames")
    print("¡Listo!")

if __name__ == "__main__":
    main()

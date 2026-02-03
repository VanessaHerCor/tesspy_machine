# ============================================================
# PREDICCIÓN CON MODELO YOLO ENTRENADO
# ============================================================
# Este script usa el modelo entrenado para detectar objetos
# en imágenes nuevas (que el modelo nunca vio)
# ============================================================

from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import numpy as np

def load_trained_model():
    """
    Carga el modelo entrenado
    
    Returns:
        YOLO: Modelo listo para hacer predicciones, o None si falló
    """
    # Ruta del modelo entrenado
    model_path = 'runs/detect/train/weights/best.pt'
    
    if not os.path.exists(model_path):
        print(f"❌ Error: No encontré el modelo en {model_path}")
        print("   Primero ejecuta: python train_custom_model.py")
        return None
    
    print(f"✅ Cargando modelo: {model_path}")
    model = YOLO(model_path)
    return model

def predict_image(model, image_path, confidence=0.5):
    """
    Hace predicción en una imagen individual
    
    Args:
        model (YOLO): Modelo entrenado
        image_path (str): Ruta de la imagen
        confidence (float): Confianza mínima (0-1)
    
    Returns:
        tuple: (imagen con detecciones, lista de detecciones)
    """
    if not os.path.exists(image_path):
        print(f"⚠️  Imagen no encontrada: {image_path}")
        return None, []
    
    # Leer imagen
    image = cv2.imread(image_path)
    if image is None:
        print(f"⚠️  No se pudo leer: {image_path}")
        return None, []
    
    # Hacer predicción
    results = model.predict(image, conf=confidence, verbose=False)
    
    # Procesar resultados
    detections = []
    
    if results[0].boxes is not None:
        for box in results[0].boxes:
            # Coordenadas de la caja
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence_score = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Dibujar caja en la imagen
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Escribir etiqueta
            label = f"{class_name} {confidence_score:.2f}"
            cv2.putText(
                image, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )
            
            # Guardar información de detección
            detections.append({
                'class': class_name,
                'confidence': confidence_score,
                'bbox': (x1, y1, x2, y2)
            })
    
    return image, detections

def main_interactive():
    """
    Modo interactivo: elige qué imagen predecir
    """
    print("\n" + "=" * 60)
    print("🔍 DETECTOR DE OBJETOS - MODO INTERACTIVO")
    print("=" * 60)
    
    # Cargar modelo
    model = load_trained_model()
    if model is None:
        return
    
    print(f"\n✅ Modelo cargado. Clases detectables: {list(model.names.values())}\n")
    
    # Menú interactivo
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Predecir en una imagen")
        print("2. Predecir en carpeta de imágenes")
        print("3. Salir")
        
        choice = input("\nElige (1-3): ").strip()
        
        if choice == "1":
            image_path = input("Ruta de imagen: ").strip()
            result_image, detections = predict_image(model, image_path)
            
            if result_image is not None:
                print(f"\n✅ Detecciones encontradas: {len(detections)}")
                for i, det in enumerate(detections, 1):
                    print(f"   {i}. {det['class']} (confianza: {det['confidence']:.2f})")
                
                # Mostrar imagen
                cv2.imshow("Detecciones", result_image)
                print("\nPresiona cualquier tecla para cerrar la ventana...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                # Opción de guardar
                save = input("\n¿Guardar imagen con detecciones? (s/n): ").lower()
                if save == 's':
                    output_path = image_path.replace('.', '_detected.')
                    cv2.imwrite(output_path, result_image)
                    print(f"✅ Guardado en: {output_path}")
        
        elif choice == "2":
            folder_path = input("Ruta de carpeta con imágenes: ").strip()
            if not os.path.isdir(folder_path):
                print("❌ La carpeta no existe")
                continue
            
            # Buscar imágenes
            image_files = []
            for ext in ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG']:
                image_files.extend(Path(folder_path).glob(ext))
            
            if not image_files:
                print("❌ No encontré imágenes en esa carpeta")
                continue
            
            print(f"\n🔍 Procesando {len(image_files)} imágenes...\n")
            
            total_detections = 0
            for img_path in image_files:
                result_image, detections = predict_image(model, str(img_path))
                
                if result_image is not None:
                    total_detections += len(detections)
                    print(f"✅ {img_path.name}: {len(detections)} objeto(s)")
                    
                    # Guardar resultado
                    output_path = str(img_path).replace('.', '_detected.')
                    cv2.imwrite(output_path, result_image)
            
            print(f"\n✅ Total de objetos detectados: {total_detections}")
        
        elif choice == "3":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")

def main_quick_test():
    """
    Modo rápido: predecir en una sola imagen de prueba
    Útil para verificar que todo funciona
    """
    print("\n" + "=" * 60)
    print("⚡ PRUEBA RÁPIDA")
    print("=" * 60)
    
    # Cargar modelo
    model = load_trained_model()
    if model is None:
        return
    
    # Buscar una imagen en valid/images (ruta relativa funciona desde la raíz)
    valid_images_dir = 'dataset/valid/images'
    if os.path.isdir(valid_images_dir):
        images = list(Path(valid_images_dir).glob('*.jpg')) + \
                 list(Path(valid_images_dir).glob('*.png'))
        
        if images:
            test_image = str(images[0])
            print(f"\n🧪 Usando imagen de prueba: {Path(test_image).name}")
            
            result_image, detections = predict_image(model, test_image)
            
            if result_image is not None:
                print(f"\n✅ Detecciones: {len(detections)}")
                for det in detections:
                    print(f"   - {det['class']}: {det['confidence']:.2f}")
                
                # Mostrar
                cv2.imshow("Prueba", result_image)
                print("\nPresiona cualquier tecla para cerrar...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Modo de prueba rápido
        main_quick_test()
    else:
        # Modo interactivo
        main_interactive()

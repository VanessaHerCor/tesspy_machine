# ============================================================
# ETIQUETADOR AUTOMÁTICO DE IMÁGENES
# ============================================================
# Este script etiqueta automáticamente las imágenes que
# descargaste, creando archivos .txt con las coordenadas
# de los objetos detectados para entrenar el modelo
# ============================================================

# IMPORTAR LIBRERÍAS
from ultralytics import YOLO  # Modelo de visión: detecta objetos en imágenes
import os  # Para manejar carpetas y rutas de archivos
import glob  # Para buscar archivos que coincidan con un patrón
import re  # Expresiones regulares: buscar patrones en texto

def auto_label_images():
    """
    Etiqueta automáticamente las imágenes descargadas.
    Crea archivos .txt con las coordenadas de los objetos detectados.
    """
    print("\n" + "=" * 60)
    print("AUTO-ETIQUETADO INTELIGENTE DE IMÁGENES")
    print("=" * 60)
    print("Esto creará etiquetas automáticas para entrenar el modelo...\n")
    
    # PASO 1: CARGAR EL MODELO YOLO-WORLD
    # YOLO-World puede detectar cualquier objeto si le dices su nombre
    try:
        model = YOLO('yolov8s-worldv2.pt')  # Modelo pequeño y eficiente
        print("✅ Modelo YOLO cargado exitosamente\n")
    except Exception as e:
        print(f"❌ Error cargando YOLO-World: {e}")
        print("   Intenta instalar: pip install ultralytics")
        return

    # PASO 2: CONFIGURAR RUTAS DE CARPETAS
    # Obtener la carpeta donde está este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # La carpeta principal donde están las imágenes
    dataset_dir = os.path.join(base_dir, 'dataset')
    # Procesar carpetas de entrenamiento y validación
    subsets = ['train', 'valid']
    
    # Contador de imágenes etiquetadas
    total_labeled = 0
    
    # PASO 3: PROCESAR CARPETAS DE ENTRENAMIENTO Y VALIDACIÓN
    for subset in subsets:
        # Rutas para imágenes y donde guardar etiquetas
        images_dir = os.path.join(dataset_dir, subset, 'images')  # Imágenes
        labels_dir = os.path.join(dataset_dir, subset, 'labels')  # Etiquetas
        
        # Verificar si existe la carpeta de imágenes
        if not os.path.exists(images_dir):
            print(f"⚠️  Carpeta no encontrada: {images_dir}")
            print(f"   Primero ejecuta: python download_custom_images.py")
            continue
            
        # Crear carpeta de etiquetas si no existe
        os.makedirs(labels_dir, exist_ok=True)
        
        # PASO 4: BUSCAR IMÁGENES
        image_files = []  # Lista para guardar las imágenes encontradas
        # Buscar archivos con extensión jpg, png o jpeg
        for ext in ['*.jpg', '*.png', '*.jpeg']:
            image_files.extend(glob.glob(os.path.join(images_dir, ext)))
            
        print(f"📁 Procesando {len(image_files)} imágenes en carpeta '{subset}'...\n")
        
        # PASO 5: ETIQUETAR CADA IMAGEN
        for img_path in image_files:
            filename = os.path.basename(img_path)  # Obtener nombre sin la ruta
            
            # EXTRAER EL NOMBRE DEL OBJETO
            # El descargador crea nombres como: "cat_train_0.jpg"
            # Necesitamos extraer "cat" usando expresiones regulares
            match = re.match(r"(.+)_(train|valid)_\d+\.", filename)
            
            if match:
                # Si coincide: extraer "cat" de "cat_train_0.jpg"
                # replace('_', ' ') convierte "cat_toy" a "cat toy"
                object_name = match.group(1).replace('_', ' ')
            else:
                # Si no coincide, usar el nombre del archivo limpio
                object_name = os.path.splitext(filename)[0].replace('_', ' ')
            
            # PASO 6: DETECTAR EL OBJETO EN LA IMAGEN
            # Decirle al modelo: "Busca ESTO en esta foto"
            model.set_classes([object_name])
            
            # Ejecutar predicción
            # conf=0.05 = detectar incluso con poca confianza
            # verbose=False = no mostrar detalles
            results = model.predict(img_path, conf=0.05, verbose=False)
            
            # PASO 7: GUARDAR ETIQUETA EN ARCHIVO .txt
            # Crear nombre: "cat_train_0.jpg" → "cat_train_0.txt"
            txt_name = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(labels_dir, txt_name)
            
            # Escribir coordenadas del objeto en el archivo
            with open(txt_path, 'w') as f:
                has_detection = False  # ¿Encontró el objeto?
                
                for result in results:
                    for box in result.boxes:
                        # Obtener coordenadas normalizadas (0-1)
                        # x, y = centro del objeto
                        # w, h = ancho y alto
                        x, y, w, h = box.xywhn[0].tolist()
                        # Guardar formato YOLO: clase x y w h
                        # Clase 0 = primer objeto (solo hay uno)
                        f.write(f"0 {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
                        has_detection = True
                
                # Mostrar resultado
                if has_detection:
                    total_labeled += 1  # Incrementar contador
                    print(f"  ✅ [OK] '{object_name}' detectado en {filename}")
                else:
                    print(f"  ❌ [FAIL] No se encontró '{object_name}' en {filename}")

    # PASO 8: MOSTRAR RESULTADO FINAL
    print(f"\n{'='*60}")
    print(f"✅ ¡Listo! Se generaron etiquetas para {total_labeled} imágenes.")
    print(f"{'='*60}")
    print("\nTu dataset está listo para entrenar el modelo.")
    print("\nProximos pasos:")
    print("1. Verifica que los labels se guardaron en: dataset/train/labels y dataset/valid/labels")
    print("2. Crea un archivo 'data.yaml' con la configuración")
    print("3. Ejecuta: python train_custom_model.py")

# =====================================================
# EJECUTAR LA FUNCIÓN
# =====================================================
if __name__ == '__main__':
    # Solo ejecutar si corres este archivo directamente
    auto_label_images()

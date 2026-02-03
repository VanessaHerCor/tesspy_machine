# ============================================================
# RE-ETIQUETAR IMÁGENES SIN LABELS (Versión ARREGLADA)
# ============================================================
# Este script detecta guitarras en imágenes que NO tienen
# labels, sin eliminar nada. Solo LLENA los vacíos.
# ============================================================

from ultralytics import YOLO
import os
import glob
from pathlib import Path

def relabel_empty_fixed():
    """
    Encuentra imágenes sin labels y las etiqueta automáticamente
    VERSIÓN ARREGLADA Y MÁS ROBUSTA
    """
    print("\n" + "=" * 70)
    print("🔍 RE-ETIQUETANDO IMÁGENES SIN LABELS (VERSIÓN ARREGLADA)")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Cargar modelo
    print("\n📦 Cargando modelo YOLO-World...")
    try:
        model = YOLO(os.path.join(base_dir, 'yolov8s-worldv2.pt'))
        print("✅ Modelo cargado\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    total_processed = 0
    total_relabeled = 0
    
    for subset in ['train', 'valid']:
        images_dir = os.path.join(base_dir, 'dataset', subset, 'images')
        labels_dir = os.path.join(base_dir, 'dataset', subset, 'labels')
        
        if not os.path.exists(images_dir):
            print(f"⚠️  No encontré: {images_dir}")
            continue
        
        print(f"📁 Procesando '{subset}'...\n")
        
        # Buscar TODAS las imágenes
        image_files = []
        for ext in ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG']:
            image_files.extend(glob.glob(os.path.join(images_dir, ext)))
        
        image_files.sort()
        print(f"   Total de imágenes: {len(image_files)}")
        
        relabeled_count = 0
        
        for img_path in image_files:
            filename = os.path.basename(img_path)
            label_name = os.path.splitext(filename)[0] + '.txt'
            label_path = os.path.join(labels_dir, label_name)
            
            # Revisar si el label está vacío
            is_empty = True
            if os.path.exists(label_path):
                try:
                    with open(label_path, 'r') as f:
                        content = f.read().strip()
                        if len(content) > 0:
                            is_empty = False
                except:
                    pass
            
            # Si está vacío, detectar
            if is_empty:
                total_processed += 1
                try:
                    # Detectar con confianza baja (0.05 es muy tolerante)
                    model.set_classes(['guitar'])
                    results = model.predict(img_path, conf=0.05, verbose=False)
                    
                    # Obtener detecciones
                    detections = []
                    
                    # Revisar si hay boxes detectadas
                    if results[0].boxes is not None:
                        num_boxes = len(results[0].boxes)
                        if num_boxes > 0:
                            for box in results[0].boxes:
                                # Normalizar coordenadas
                                h, w = results[0].orig_img.shape[:2]
                                x1, y1, x2, y2 = box.xyxy[0]
                                
                                x_center = ((x1 + x2) / 2) / w
                                y_center = ((y1 + y2) / 2) / h
                                width = (x2 - x1) / w
                                height = (y2 - y1) / h
                                
                                detections.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                    
                    # Guardar resultado
                    with open(label_path, 'w') as f:
                        if detections:
                            f.write('\n'.join(detections))
                            print(f"   [{total_processed:2d}] ✅ {filename:<25s} → {len(detections)} guitarra(s)")
                            relabeled_count += 1
                            total_relabeled += 1
                        else:
                            f.write('')
                            print(f"   [{total_processed:2d}] ⚠️  {filename:<25s} → sin detecciones")
                
                except Exception as e:
                    print(f"   [{total_processed:2d}] ❌ {filename:<25s} → ERROR: {e}")
        
        print(f"\n   Resultado '{subset}': {relabeled_count} imágenes re-etiquetadas")
        print()
    
    print("=" * 70)
    print(f"✅ ¡LISTO!")
    print(f"   Total procesadas: {total_processed}")
    print(f"   Total con detecciones: {total_relabeled}")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    relabel_empty_fixed()

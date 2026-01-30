# ============================================================
# LIMPIAR LABELS VACÍOS
# ============================================================
# Elimina imágenes que no tienen guitarra detectada
# (labels vacíos)
# ============================================================

import os
from pathlib import Path

def clean_empty_labels():
    """
    Elimina imágenes y labels vacíos
    """
    print("\n" + "=" * 60)
    print("🧹 LIMPIANDO LABELS VACÍOS")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Procesar train y valid
    for subset in ['train', 'valid']:
        images_dir = os.path.join(base_dir, 'dataset', subset, 'images')
        labels_dir = os.path.join(base_dir, 'dataset', subset, 'labels')
        
        if not os.path.exists(images_dir):
            print(f"\n⚠️  No encontré: {images_dir}")
            continue
        
        print(f"\n📁 Procesando carpeta '{subset}'...\n")
        
        deleted_count = 0
        kept_count = 0
        
        # Buscar labels vacíos
        label_files = list(Path(labels_dir).glob('*.txt'))
        
        for label_path in label_files:
            # Leer el contenido del label
            with open(label_path, 'r') as f:
                content = f.read().strip()
            
            # Si está vacío
            if len(content) == 0:
                # Obtener nombre del archivo de imagen correspondiente
                label_name = label_path.stem  # Nombre sin extensión
                
                # Buscar la imagen
                for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
                    image_path = os.path.join(images_dir, label_name + ext)
                    
                    if os.path.exists(image_path):
                        # Eliminar imagen
                        os.remove(image_path)
                        print(f"   ❌ Eliminado: {label_name}{ext}")
                        deleted_count += 1
                        break
                
                # Eliminar label
                os.remove(label_path)
            else:
                kept_count += 1
        
        print(f"\n   📊 Resultado en '{subset}':")
        print(f"      ✅ Guardadas: {kept_count} imágenes")
        print(f"      ❌ Eliminadas: {deleted_count} imágenes")
    
    print("\n" + "=" * 60)
    print("✅ ¡Limpieza completada!")
    print("=" * 60)

if __name__ == "__main__":
    clean_empty_labels()

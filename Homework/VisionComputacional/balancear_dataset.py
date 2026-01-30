# ============================================================
# BALANCEADOR DE DATASET - 80/20 Train/Valid
# ============================================================
# Este script detecta el número de imágenes y balancea
# automáticamente el dataset en ratio 80% train / 20% valid
# ============================================================

import os
import glob
import shutil
import random
from pathlib import Path

def balancear_dataset():
    """
    Balancea el dataset en ratio 80/20 (train/valid)
    Mueve imágenes automáticamente para mantener el balance
    """
    
    print("\n" + "=" * 60)
    print("BALANCEADOR DE DATASET - 80/20 Train/Valid")
    print("=" * 60)
    
    # Obtener rutas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, 'dataset')
    
    train_images_dir = os.path.join(dataset_dir, 'train', 'images')
    train_labels_dir = os.path.join(dataset_dir, 'train', 'labels')
    valid_images_dir = os.path.join(dataset_dir, 'valid', 'images')
    valid_labels_dir = os.path.join(dataset_dir, 'valid', 'labels')
    
    # Crear carpetas si no existen
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(valid_images_dir, exist_ok=True)
    os.makedirs(valid_labels_dir, exist_ok=True)
    
    # PASO 1: Contar imágenes actuales
    train_images = glob.glob(os.path.join(train_images_dir, '*.jpg')) + \
                   glob.glob(os.path.join(train_images_dir, '*.png'))
    valid_images = glob.glob(os.path.join(valid_images_dir, '*.jpg')) + \
                   glob.glob(os.path.join(valid_images_dir, '*.png'))
    
    num_train = len(train_images)
    num_valid = len(valid_images)
    total = num_train + num_valid
    
    print(f"\n📊 ESTADO ACTUAL:")
    print(f"   Train: {num_train} imágenes ({num_train/total*100:.1f}%)")
    print(f"   Valid: {num_valid} imágenes ({num_valid/total*100:.1f}%)")
    print(f"   Total: {total} imágenes")
    
    if total == 0:
        print("\n❌ No hay imágenes en el dataset. Saliendo...")
        return
    
    # PASO 2: Calcular el balance ideal (80/20)
    ideal_train = int(total * 0.8)
    ideal_valid = total - ideal_train
    
    print(f"\n🎯 BALANCE IDEAL (80/20):")
    print(f"   Train: {ideal_train} imágenes ({ideal_train/total*100:.1f}%)")
    print(f"   Valid: {ideal_valid} imágenes ({ideal_valid/total*100:.1f}%)")
    
    # PASO 3: Detectar desbalance
    diferencia_train = num_train - ideal_train
    
    if abs(diferencia_train) < 2:
        print(f"\n✅ Dataset ya está balanceado!")
        return
    
    print(f"\n⚠️  DESBALANCE DETECTADO:")
    
    if diferencia_train > 0:
        # Hay demasiadas en train, mover a valid
        a_mover = diferencia_train
        print(f"   Train tiene {a_mover} imágenes de más")
        print(f"   → Moviendo {a_mover} imágenes de train a valid")
        
        confirmacion = input("\n¿Continuar? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Cancelado.")
            return
        
        # Seleccionar imágenes random de train
        random.shuffle(train_images)
        imagenes_a_mover = train_images[:a_mover]
        
        for img_path in imagenes_a_mover:
            filename = os.path.basename(img_path)
            
            # Rutas destino
            img_dest = os.path.join(valid_images_dir, filename)
            label_src = img_path.replace('.jpg', '.txt').replace('.png', '.txt').replace('images', 'labels')
            label_dest = os.path.join(valid_labels_dir, os.path.basename(label_src))
            
            # Mover imagen
            shutil.move(img_path, img_dest)
            
            # Mover etiqueta si existe
            if os.path.exists(label_src):
                shutil.move(label_src, label_dest)
            
            print(f"   ✅ {filename}")
    
    else:
        # Hay demasiadas en valid, mover a train
        a_mover = abs(diferencia_train)
        print(f"   Valid tiene {a_mover} imágenes de más")
        print(f"   → Moviendo {a_mover} imágenes de valid a train")
        
        confirmacion = input("\n¿Continuar? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Cancelado.")
            return
        
        # Seleccionar imágenes random de valid
        random.shuffle(valid_images)
        imagenes_a_mover = valid_images[:a_mover]
        
        for img_path in imagenes_a_mover:
            filename = os.path.basename(img_path)
            
            # Rutas destino
            img_dest = os.path.join(train_images_dir, filename)
            label_src = img_path.replace('.jpg', '.txt').replace('.png', '.txt').replace('images', 'labels')
            label_dest = os.path.join(train_labels_dir, os.path.basename(label_src))
            
            # Mover imagen
            shutil.move(img_path, img_dest)
            
            # Mover etiqueta si existe
            if os.path.exists(label_src):
                shutil.move(label_src, label_dest)
            
            print(f"   ✅ {filename}")
    
    # PASO 4: Verificar balance final
    train_images_final = glob.glob(os.path.join(train_images_dir, '*.jpg')) + \
                         glob.glob(os.path.join(train_images_dir, '*.png'))
    valid_images_final = glob.glob(os.path.join(valid_images_dir, '*.jpg')) + \
                         glob.glob(os.path.join(valid_images_dir, '*.png'))
    
    num_train_final = len(train_images_final)
    num_valid_final = len(valid_images_final)
    total_final = num_train_final + num_valid_final
    
    print(f"\n" + "=" * 60)
    print(f"✅ BALANCE FINAL:")
    print(f"   Train: {num_train_final} imágenes ({num_train_final/total_final*100:.1f}%)")
    print(f"   Valid: {num_valid_final} imágenes ({num_valid_final/total_final*100:.1f}%)")
    print(f"   Total: {total_final} imágenes")
    print("=" * 60)
    
    print(f"\n📋 Próximos pasos:")
    print(f"   1. Ejecuta: python auto_label.py")
    print(f"   2. Ejecuta: python clean_empty_labels.py")
    print(f"   3. Ejecuta: python train_custom_model.py")
    print(f"\n")

if __name__ == "__main__":
    balancear_dataset()

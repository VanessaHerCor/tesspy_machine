# ============================================================
# UNIFICADOR DE NOMBRES - FLEXIBLE
# ============================================================
# Este script renombra INTELIGENTEMENTE imágenes con
# CUALQUIER nombre a un nombre unificado, evitando conflictos
# ============================================================

import os
import glob
import shutil
from pathlib import Path
import re

def encontrar_prefijo_comun(images_dir):
    """
    Encuentra el prefijo común en todos los archivos de imágenes
    Ejemplo: acoustic_guitar_train_0.jpg → acoustic_guitar
    """
    archivos = glob.glob(os.path.join(images_dir, '*.jpg')) + \
               glob.glob(os.path.join(images_dir, '*.png'))
    
    if not archivos:
        return None
    
    prefijos = []
    for archivo in archivos:
        filename = os.path.basename(archivo)
        # Extraer todo antes de _train o _valid
        # Ejemplo: acoustic_guitar_train_0.jpg → acoustic_guitar
        match = re.match(r"(.+)_(train|valid)_\d+\.", filename)
        if match:
            prefijos.append(match.group(1))
    
    if prefijos:
        return prefijos[0]  # Usar el primero como referencia
    return None

def unificar_nombres():
    """
    Renombra imágenes con cualquier nombre a un nombre unificado
    Evita conflictos encontrando el número máximo disponible
    """
    
    print("\n" + "=" * 60)
    print("UNIFICADOR DE NOMBRES - FLEXIBLE")
    print("=" * 60)
    
    # Carpetas a procesar (subir un nivel para llegar a la raíz)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, 'dataset')
    
    # PASO 1: Detectar automáticamente el prefijo actual
    images_dir_train = os.path.join(dataset_dir, 'train', 'images')
    prefijo_detectado = encontrar_prefijo_comun(images_dir_train)
    
    print(f"\n🔍 Prefijo detectado: {prefijo_detectado if prefijo_detectado else 'No encontrado'}\n")
    
    # PASO 2: Preguntar al usuario
    print("¿Qué nombre actual tienen tus imágenes?")
    if prefijo_detectado:
        print(f"(Detectado: {prefijo_detectado})")
    print("(Ejemplo: acoustic_guitar, cat, perro, etc.)")
    nombre_actual = input("> ").strip()
    
    if not nombre_actual:
        nombre_actual = prefijo_detectado
        if not nombre_actual:
            print("❌ No se encontraron imágenes. Saliendo...")
            return
    
    print(f"\n¿A qué nombre quieres unificar?")
    print("(Por defecto: guitar)")
    nombre_nuevo = input("> ").strip()
    
    if not nombre_nuevo:
        nombre_nuevo = "guitar"
    
    # Confirmación
    print(f"\n" + "=" * 60)
    print(f"Renombrando: {nombre_actual} → {nombre_nuevo}")
    print("=" * 60)
    
    confirmacion = input("\n¿Continuar? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("Cancelado.")
        return
    
    # PASO 3: Procesar train y valid
    subsets = ['train', 'valid']
    total_renombradas = 0
    
    for subset in subsets:
        print(f"\n📁 Procesando: {subset}/")
        
        images_dir = os.path.join(dataset_dir, subset, 'images')
        labels_dir = os.path.join(dataset_dir, subset, 'labels')
        
        # Encontrar el número máximo de {nombre_nuevo}_* existentes
        patron_nuevo = os.path.join(images_dir, f'{nombre_nuevo}_*.jpg')
        archivos_nuevos = glob.glob(patron_nuevo)
        numeros_nuevos = []
        
        for file in archivos_nuevos:
            filename = os.path.basename(file)
            try:
                num = int(filename.split('_')[2].split('.')[0])
                numeros_nuevos.append(num)
            except:
                pass
        
        max_number = max(numeros_nuevos) if numeros_nuevos else 0
        print(f"   Máximo número encontrado: {max_number}")
        
        # Encontrar todas las imágenes con el nombre actual
        patron_actual = os.path.join(images_dir, f'{nombre_actual}_*.jpg')
        archivos_actuales = glob.glob(patron_actual)
        print(f"   Imágenes {nombre_actual}_* encontradas: {len(archivos_actuales)}")
        
        if len(archivos_actuales) == 0:
            print(f"   ✅ No hay imágenes {nombre_actual}_* en {subset}")
            continue
        
        # Renombrar cada imagen
        for archivo_actual in archivos_actuales:
            max_number += 1
            
            # Rutas actuales
            img_actual_path = archivo_actual
            label_actual_path = img_actual_path.replace('.jpg', '.txt').replace('images', 'labels')
            
            # Extraer tipo (train o valid)
            filename = os.path.basename(img_actual_path)
            match = re.match(r".+_(train|valid)_\d+\.", filename)
            subset_type = match.group(1) if match else subset
            
            # Rutas nuevas
            img_nueva_path = os.path.join(images_dir, f'{nombre_nuevo}_{subset_type}_{max_number}.jpg')
            label_nueva_path = os.path.join(labels_dir, f'{nombre_nuevo}_{subset_type}_{max_number}.txt')
            
            # Renombrar imagen
            if os.path.exists(img_actual_path):
                shutil.move(img_actual_path, img_nueva_path)
                print(f"   ✅ {os.path.basename(img_actual_path)} → {os.path.basename(img_nueva_path)}")
            
            # Renombrar etiqueta
            if os.path.exists(label_actual_path):
                shutil.move(label_actual_path, label_nueva_path)
            
            total_renombradas += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ PROCESO COMPLETADO")
    print(f"   Total de imágenes renombradas: {total_renombradas}")
    print(f"=" * 60)
    print(f"\n📋 Próximos pasos:")
    print(f"   1. Ejecuta: python py_scripts/auto_label.py")
    print(f"   2. Ejecuta: python py_scripts/clean_empty_labels.py")
    print(f"   3. Ejecuta: python py_scripts/train_custom_model.py")
    print(f"\n")

if __name__ == "__main__":
    unificar_nombres()

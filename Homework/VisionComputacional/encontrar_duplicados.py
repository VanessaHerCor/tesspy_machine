# ============================================================
# DETECTOR DE IMÁGENES DUPLICADAS
# ============================================================
# Encuentra imágenes idénticas o muy parecidas en el dataset
# ============================================================

import os
import cv2
import numpy as np
import hashlib
import glob
from collections import defaultdict
from pathlib import Path

def calcular_hash_imagen(ruta_imagen):
    """Calcula hash MD5 de la imagen (detecta duplicados exactos)"""
    try:
        with open(ruta_imagen, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def calcular_histograma(ruta_imagen):
    """Calcula histograma de la imagen (detecta similares)"""
    try:
        img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return cv2.normalize(hist, hist).flatten()
    except:
        return None

def comparar_histogramas(hist1, hist2):
    """Compara dos histogramas (0 = idénticos, 1 = diferentes)"""
    if hist1 is None or hist2 is None:
        return 1.0
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

def encontrar_duplicados():
    """
    Encuentra imágenes duplicadas en el dataset
    """
    
    print("\n" + "=" * 60)
    print("DETECTOR DE IMÁGENES DUPLICADAS")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, 'dataset')
    
    # Opciones de detección
    print("\n⚙️ OPCIONES DE BÚSQUEDA:\n")
    print("1. Encontrar DUPLICADOS EXACTOS (MD5 hash)")
    print("2. Encontrar IMÁGENES PARECIDAS (histograma > 95% similar)")
    print("3. AMBAS búsquedas")
    print("4. Salir")
    
    opcion = input("\n¿Qué buscas? (1-4): ").strip()
    
    if opcion == "4":
        print("Cancelado.")
        return
    
    # =====================================================
    # BÚSQUEDA 1: DUPLICADOS EXACTOS
    # =====================================================
    if opcion in ["1", "3"]:
        print("\n🔍 Buscando DUPLICADOS EXACTOS...")
        print("-" * 60)
        
        hashes = defaultdict(list)
        duplicados_exactos = []
        
        for subset in ['train', 'valid']:
            images_dir = os.path.join(dataset_dir, subset, 'images')
            
            for img_file in glob.glob(os.path.join(images_dir, '*.jpg')):
                hash_img = calcular_hash_imagen(img_file)
                if hash_img:
                    hashes[hash_img].append(img_file)
        
        # Encontrar grupos con más de 1 imagen (duplicados)
        for hash_val, archivos in hashes.items():
            if len(archivos) > 1:
                duplicados_exactos.append(archivos)
        
        if duplicados_exactos:
            print(f"\n⚠️  ENCONTRADOS {len(duplicados_exactos)} GRUPOS DE DUPLICADOS EXACTOS:\n")
            
            total_a_eliminar = 0
            for idx, grupo in enumerate(duplicados_exactos, 1):
                print(f"📋 GRUPO {idx} ({len(grupo)} imágenes idénticas):")
                for archivo in grupo:
                    print(f"   • {os.path.relpath(archivo, dataset_dir)}")
                total_a_eliminar += len(grupo) - 1  # Guardar 1, eliminar el resto
            
            print(f"\n💡 Se pueden eliminar: {total_a_eliminar} imágenes")
            
            eliminar = input("\n¿Eliminar duplicados exactos? (s/n): ").strip().lower()
            if eliminar == 's':
                eliminadas = 0
                for grupo in duplicados_exactos:
                    # Guardar el primero, eliminar los demás
                    for archivo in grupo[1:]:
                        try:
                            # Eliminar imagen
                            os.remove(archivo)
                            # Eliminar etiqueta
                            label_file = archivo.replace('.jpg', '.txt').replace('images', 'labels')
                            if os.path.exists(label_file):
                                os.remove(label_file)
                            print(f"   ✅ Eliminado: {os.path.basename(archivo)}")
                            eliminadas += 1
                        except Exception as e:
                            print(f"   ❌ Error al eliminar {archivo}: {e}")
                
                print(f"\n✅ {eliminadas} imágenes duplicadas eliminadas")
        else:
            print("✅ NO se encontraron duplicados exactos")
    
    # =====================================================
    # BÚSQUEDA 2: IMÁGENES PARECIDAS
    # =====================================================
    if opcion in ["2", "3"]:
        print("\n🔍 Buscando IMÁGENES PARECIDAS (95%+ similares)...")
        print("-" * 60)
        
        imagenes = []
        histogramas = []
        
        for subset in ['train', 'valid']:
            images_dir = os.path.join(dataset_dir, subset, 'images')
            
            for img_file in sorted(glob.glob(os.path.join(images_dir, '*.jpg'))):
                hist = calcular_histograma(img_file)
                if hist is not None:
                    imagenes.append(img_file)
                    histogramas.append(hist)
        
        similares_grupos = []
        procesadas = set()
        
        for i, (img1, hist1) in enumerate(zip(imagenes, histogramas)):
            if i in procesadas:
                continue
            
            grupo_similar = [img1]
            
            for j, (img2, hist2) in enumerate(zip(imagenes[i+1:], histogramas[i+1:]), start=i+1):
                if j in procesadas:
                    continue
                
                similitud = 1 - comparar_histogramas(hist1, hist2)
                
                if similitud >= 0.95:  # 95% o más similar
                    grupo_similar.append(img2)
                    procesadas.add(j)
            
            if len(grupo_similar) > 1:
                similares_grupos.append(grupo_similar)
                procesadas.add(i)
        
        if similares_grupos:
            print(f"\n⚠️  ENCONTRADOS {len(similares_grupos)} GRUPOS DE IMÁGENES PARECIDAS:\n")
            
            for idx, grupo in enumerate(similares_grupos, 1):
                print(f"📋 GRUPO {idx} ({len(grupo)} imágenes 95%+ similares):")
                for archivo in grupo:
                    print(f"   • {os.path.relpath(archivo, dataset_dir)}")
            
            eliminar = input("\n¿Eliminar imágenes parecidas? (s/n): ").strip().lower()
            if eliminar == 's':
                eliminadas = 0
                for grupo in similares_grupos:
                    # Guardar la primera, eliminar las demás
                    for archivo in grupo[1:]:
                        try:
                            os.remove(archivo)
                            label_file = archivo.replace('.jpg', '.txt').replace('images', 'labels')
                            if os.path.exists(label_file):
                                os.remove(label_file)
                            print(f"   ✅ Eliminado: {os.path.basename(archivo)}")
                            eliminadas += 1
                        except Exception as e:
                            print(f"   ❌ Error al eliminar {archivo}: {e}")
                
                print(f"\n✅ {eliminadas} imágenes parecidas eliminadas")
        else:
            print("✅ NO se encontraron imágenes parecidas (95%+ similares)")
    
    print("\n" + "=" * 60)
    print("📋 Próximos pasos:")
    print("   1. Ejecuta: python auto_label.py")
    print("   2. Ejecuta: python clean_empty_labels.py")
    print("   3. Ejecuta: python train_custom_model.py")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    encontrar_duplicados()

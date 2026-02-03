# ============================================================
# DESCARGADOR AUTOMÁTICO DE IMÁGENES PARA ENTRENAMIENTO
# ============================================================
# Este script busca imágenes en internet y las descarga
# automáticamente, dividiéndolas en entrenamiento (80%)
# y validación (20%)
# ============================================================

# IMPORTAR LIBRERÍAS
import os  # Para manejar rutas y carpetas
import requests  # Para descargar archivos de internet
from ddgs import DDGS  # Motor de búsqueda DuckDuckGo (versión nueva - mejor)
import time  # Para hacer pausas entre descargas

# Función para descargar una imagen desde una URL
def download_image(url, folder, name):
    """
    Descarga una imagen desde una URL y la guarda en una carpeta
    
    Args:
        url (str): La dirección web de la imagen
        folder (str): La carpeta donde guardar la imagen
        name (str): El nombre con el que guardar el archivo
    
    Returns:
        bool: True si descargó correctamente, False si falló
    """
    try:
        # Intentar descargar con un máximo de 10 segundos
        response = requests.get(url, timeout=10)
        
        # Si la descarga fue exitosa (código HTTP 200)
        if response.status_code == 200:
            # Guardar el contenido (la imagen) en un archivo
            with open(os.path.join(folder, name), 'wb') as f:
                f.write(response.content)
            return True  # Retornar True = éxito
    except Exception as e:
        # Si hay cualquier error, simplemente ignorarlo
        pass
    
    return False  # Retornar False = fallo

def search_and_download(term, max_images=30):
    """
    Busca imágenes en DuckDuckGo y las descarga automáticamente
    
    Args:
        term (str): Qué objeto buscar (ejemplo: "cat", "dog", "electrical outlet")
        max_images (int): Cuántas imágenes descargar (por defecto 30)
    """
    print(f"\n🔍 Buscando imágenes de: '{term}'...")
    
    # =====================================================
    # PASO 1: CONFIGURAR LAS CARPETAS
    # =====================================================
    # Obtener la carpeta donde está este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear ruta para el dataset
    dataset_dir = os.path.join(base_dir, 'dataset')  # Carpeta principal
    train_dir = os.path.join(dataset_dir, 'train/images')  # Para entrenamiento (80%)
    valid_dir = os.path.join(dataset_dir, 'valid/images')  # Para validación (20%)
    
    # Crear las carpetas si no existen (exist_ok=True = no fallar si ya existen)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)
    
    count = 0  # Contador: cuántas imágenes descargamos exitosamente
    
    # =====================================================
    # PASO 2: BUSCAR IMÁGENES EN DUCKDUCKGO
    # =====================================================
    with DDGS() as ddgs:
        # Realizar la búsqueda de imágenes
        results = ddgs.images(
            query=term,  # Qué buscar (cambió de 'keywords' a 'query')
            max_results=max_images + 10  # Pedir más por si fallan algunas
        )
        
        # Convertir resultados a lista
        results_list = list(results)
        print(f"✅ Se encontraron {len(results_list)} enlaces. Iniciando descarga...\n")
        
        # =====================================================
        # PASO 3: DESCARGAR CADA IMAGEN UNA POR UNA
        # =====================================================
        for i, r in enumerate(results_list):
            # Si ya descargamos suficientes, salir del loop
            if count >= max_images:
                break
                
            url = r['image']  # Obtener la URL de la imagen
            
            # DECIDIR SI ESTA IMAGEN VA PARA ENTRENAMIENTO O VALIDACIÓN
            # 80% de las imágenes para entrenamiento, 20% para validación
            if count < int(max_images * 0.8):
                dest_folder = train_dir  # Primera 80%: guardar en entrenamiento
                prefix = "train"
            else:
                dest_folder = valid_dir  # Última 20%: guardar en validación
                prefix = "valid"
                
            # Crear el nombre del archivo
            # Ejemplo: "cat_train_0.jpg" o "dog_valid_5.jpg"
            filename = f"{term.replace(' ', '_')}_{prefix}_{i}.jpg"
            
            print(f"  Descargando {count+1}/{max_images}: {url[:50]}...")
            
            # Intentar descargar la imagen
            if download_image(url, dest_folder, filename):
                count += 1  # Si fue exitosa, incrementar contador
            else:
                print(f"     ❌ Falló, continuando...")
            
            # Esperar 0.5 segundos entre descargas (ser respetuoso con los servidores)
            time.sleep(0.5)

    # =====================================================
    # PASO 4: MOSTRAR RESULTADO FINAL
    # =====================================================
    print(f"\n🎉 ¡Listo! Se descargaron {count} imágenes.")
    print(f"📁 Guardadas en: {dataset_dir}")
    print(f"   - Entrenamiento: {train_dir}")
    print(f"   - Validación: {valid_dir}")
    print("\n⚠️  IMPORTANTE: Revisa las imágenes y borra las que no sirvan.")
    print("   Después ejecuta: python auto_label.py")

if __name__ == "__main__":  # Solo ejecutar si corres este archivo directamente
    print("=" * 60)
    print("DESCARGADOR DE IMÁGENES PARA ENTRENAMIENTO CON YOLO")
    print("=" * 60)
    
    # Preguntar al usuario qué quiere buscar
    # Recomendación: buscar en inglés da mejores resultados
    search_term = input("\n¿Qué objeto quieres buscar? (Ej. 'cat', 'dog', 'car'): ")
    if not search_term:
        # Si deja en blanco, usar un término por defecto
        search_term = "electrical outlet"
        print(f"   Usando término por defecto: {search_term}")
    
    # Preguntar cuántas imágenes descargar
    num_images = input("¿Cuántas imágenes quieres? (Recomendado 50): ")
    if not num_images:
        # Si deja en blanco, usar 50 por defecto
        num_images = 50
        print(f"   Descargando 50 imágenes por defecto")
    else:
        # Convertir el texto que escribió a un número entero
        num_images = int(num_images)
        
    # Llamar a la función para buscar y descargar
    search_and_download(search_term, num_images)

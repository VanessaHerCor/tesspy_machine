# ====================================================================
# ANÁLISIS EXPLORATORIO DE DATOS (EDA) - Música y Salud Mental
# Dataset: Music & Mental Health Survey Results
# ====================================================================

# ====================================================================
# PASO 1: Importar las librerías necesarias para EDA
# ====================================================================
# Pandas: Para manejar datos en tablas (dataframes)
# Numpy: Para operaciones matemáticas y arrays
# Seaborn y Matplotlib: Para hacer gráficas bonitas
# ====================================================================

import pandas as pd
import numpy as np
import seaborn as sns                       # Para visualizaciones
import matplotlib.pyplot as plt             # Para gráficas

# Configuración para que las gráficas se vean bonitas
sns.set(color_codes=True)

print("✅ Paso 1 completado: Librerías importadas correctamente")


# ====================================================================
# PASO 2: Cargar los datos en un DataFrame
# ====================================================================
# Dataset: Music & Mental Health Survey Results (MXMH)
# Este dataset relaciona los hábitos musicales con la salud mental
# ====================================================================

try:
    df = pd.read_csv("data/music_mental_health.csv")
    print("✅ Paso 2 completado: Datos cargados correctamente")
    print(f"📊 El dataset tiene {len(df)} filas y {len(df.columns)} columnas")
    
    # Mostrar las primeras 5 filas (para ver cómo se ven los datos)
    print("\n🔝 Primeras 5 filas del dataset:")
    print(df.head(5))
    
    # Mostrar las últimas 5 filas
    print("\n🔽 Últimas 5 filas del dataset:")
    print(df.tail(5))
    
    # Mostrar nombres de las columnas
    print("\n📋 Columnas disponibles:")
    print(df.columns.tolist())
    
except FileNotFoundError:
    print("❌ ERROR: No se encontró el archivo 'music_mental_health.csv'")
    print("💡 Asegúrate de que el archivo esté en la carpeta 'data/'")


# ====================================================================
# PASO 3: Verificar los tipos de datos de cada columna
# ====================================================================
# Esto es importante porque a veces los precios vienen como texto (string)
# y necesitamos que sean números (int o float) para hacer cálculos
# ====================================================================

print("\n" + "="*60)
print("PASO 3: Tipos de datos de cada columna")
print("="*60)
try:
    print(df.dtypes)
    print("✅ Paso 3 completado: Tipos de datos verificados")
except:
    print("⚠️ Primero necesitas cargar el dataset correctamente")


# ====================================================================
# PASO 4: Eliminar columnas irrelevantes
# ====================================================================
# Algunas columnas no son útiles para el análisis o modelo
# En este caso, las columnas de "Timestamp" y "Permissions" no aportan
# al análisis de salud mental y música
# ====================================================================

print("\n" + "="*60)
print("PASO 4: Eliminando columnas innecesarias")
print("="*60)

try:
    # Ver las columnas antes de eliminar
    print(f"Columnas antes: {len(df.columns)}")
    print(f"Total de filas: {len(df)}")
    
    # Columnas que vamos a eliminar
    columnas_a_eliminar = [
        'Timestamp',      # Marca de tiempo (no es relevante para el análisis)
        'Permissions'     # Solo dice "I understand" en todas las filas
    ]
    
    # Eliminar las columnas (axis=1 significa columnas, axis=0 sería filas)
    df = df.drop(columnas_a_eliminar, axis=1)
    
    print("✅ Paso 4 completado: Columnas eliminadas")
    print(f"📊 Ahora el dataset tiene {len(df.columns)} columnas")
    print("\n🔝 Primeras 5 filas después de eliminar columnas:")
    print(df.head(5))
    
    # Mostrar información básica del dataset
    print("\n📊 Información del dataset:")
    print(df.info())
    
except KeyError as e:
    print(f"⚠️ Error: No se encontró alguna columna. Verifica los nombres: {e}")
except:
    print("⚠️ Primero necesitas cargar el dataset correctamente")


# ====================================================================
# 📝 RESUMEN DE LO QUE HICIMOS:
# ====================================================================
# ✅ Paso 1: Importamos pandas, numpy, seaborn y matplotlib
# ✅ Paso 2: Cargamos el archivo CSV en un DataFrame
# ✅ Paso 3: Revisamos qué tipo de datos tiene cada columna
# ✅ Paso 4: Eliminamos columnas que no necesitamos
#
# 🎯 SIGUIENTE PASO: Continuar con la parte 2 de la tarea
# ====================================================================
print("Dataset: Music & Mental Health Survey")
print("🎵 Analiza la relación entre música y salud mental")
print("📊 Variables: Géneros musicales, Ansiedad, Depresión, Insomnio, OCD")
print("🎉 ¡PRIMERA PARTE COMPLETADA!")
print("="*60)
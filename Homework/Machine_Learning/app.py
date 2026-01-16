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
# PASO 5: Renombrar columnas para mejor legibilidad
# ====================================================================
# Algunos nombres de columnas son largos o confusos
# Los acortamos para que sean más fáciles de usar
# ====================================================================

print("\n" + "="*60)
print("PASO 5: Renombrando columnas")
print("="*60)

try:
    print("Columnas ANTES de renombrar:")
    print(df.columns.tolist())
    
    # Renombrar columnas largas o confusas
    df = df.rename(columns={
        "Primary streaming service": "Streaming",      # Más corto
        "Hours per day": "Hours",                      # Más corto
        "While working": "Work",                       # Más corto
        "Fav genre": "Fav_Genre",                      # Sin espacio
        "Foreign languages": "Languages",              # Más corto
        "Music effects": "Effects"                     # Más corto
    })
    
    print("\n✅ Paso 5 completado: Columnas renombradas")
    print("\nColumnas DESPUÉS de renombrar:")
    print(df.columns.tolist())
    
except Exception as e:
    print(f"⚠️ Error: {e}")


# ====================================================================
# PASO 6: Detectar y eliminar filas duplicadas
# ====================================================================
# A veces hay datos repetidos (duplicados) que pueden distorsionar
# el análisis. Los detectamos y eliminamos
# ====================================================================

print("\n" + "="*60)
print("PASO 6: Detectando y eliminando duplicados")
print("="*60)

try:
    print(f"🔢 Número de filas ANTES de eliminar duplicados: {len(df)}")
    
    # Detectar filas duplicadas
    duplicate_rows = df[df.duplicated()]
    print(f"⚠️  Número de filas duplicadas encontradas: {len(duplicate_rows)}")
    
    if len(duplicate_rows) > 0:
        print("\nEjemplo de filas duplicadas:")
        print(duplicate_rows.head())
    
    # Eliminar duplicados
    df = df.drop_duplicates()
    
    print(f"\n✅ Paso 6 completado: Duplicados eliminados")
    print(f"🔢 Número de filas DESPUÉS de eliminar duplicados: {len(df)}")
    print(f"📉 Filas eliminadas: {len(duplicate_rows)}")
    
except Exception as e:
    print(f"⚠️ Error: {e}")


# ====================================================================
# PASO 7: Detectar y manejar valores faltantes (NaN/null)
# ====================================================================
# Algunos datos pueden estar vacíos (NaN = Not a Number)
# Tenemos 2 opciones:
# 1. Eliminar las filas con datos faltantes (si son pocos)
# 2. Rellenar con promedio/moda (si son muchos)
# ====================================================================

print("\n" + "="*60)
print("PASO 7: Detectando valores faltantes (NaN)")
print("="*60)

try:
    print("🔍 Valores faltantes por columna:")
    print(df.isnull().sum())
    
    # Calcular porcentaje de valores faltantes
    print("\n📊 Porcentaje de valores faltantes:")
    missing_percent = (df.isnull().sum() / len(df)) * 100
    print(missing_percent[missing_percent > 0])
    
    # Opción 1: Eliminar filas con valores faltantes
    # (Solo si son pocas filas, menos del 5-10%)
    print(f"\n🔢 Filas ANTES de eliminar valores faltantes: {len(df)}")
    
    df_cleaned = df.dropna()  # Elimina todas las filas con algún NaN
    
    print(f"🔢 Filas DESPUÉS de eliminar valores faltantes: {len(df_cleaned)}")
    print(f"📉 Filas eliminadas: {len(df) - len(df_cleaned)}")
    
    # Actualizar el dataframe
    df = df_cleaned
    
    print("\n✅ Paso 7 completado: Valores faltantes eliminados")
    print("\n🔍 Verificando que NO queden valores faltantes:")
    print(df.isnull().sum())
    
except Exception as e:
    print(f"⚠️ Error: {e}")


# ====================================================================
# 📝 RESUMEN DE LO QUE HICIMOS (PARTE 1 y 2):
# ====================================================================
print("\n" + "="*60)
print("🎉 ¡PARTE 1 Y 2 COMPLETADAS!")
print("="*60)
print("✅ Paso 1: Importamos librerías (pandas, numpy, seaborn, matplotlib)")
print("✅ Paso 2: Cargamos el dataset de música y salud mental")
print("✅ Paso 3: Verificamos tipos de datos")
print("✅ Paso 4: Eliminamos columnas innecesarias")
print("✅ Paso 5: Renombramos columnas para mejor legibilidad")
print("✅ Paso 6: Eliminamos filas duplicadas")
print("✅ Paso 7: Eliminamos valores faltantes")
print("\n📊 Dataset final:")
print(f"   - Filas: {len(df)}")
print(f"   - Columnas: {len(df.columns)}")
print("\n🎵 Dataset: Music & Mental Health Survey")
print("🧠 Variables: Géneros musicales, Ansiedad, Depresión, Insomnio, OCD")
print("="*60)
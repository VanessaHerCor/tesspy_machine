"""
=============================================================================
TÉCNICA 1: BAG OF WORDS (BOW) - LA BOLSA DE PALABRAS
=============================================================================

¿QUÉ ES?
--------
Bag of Words es la técnica más simple para convertir texto en números.
Imagina que metes todas las palabras de un texto en una "bolsa" y luego
las cuentas. El orden no importa, solo la FRECUENCIA (cuántas veces aparece
cada palabra).

¿CÓMO FUNCIONA?
---------------
1. Recopilas todos los textos (corpus)
2. Crearas un VOCABULARIO: todas las palabras únicas
3. Para cada texto, creas un VECTOR donde:
   - Cada posición = una palabra del vocabulario
   - El valor = cuántas veces aparece esa palabra en el texto

EJEMPLO:
--------
Vocabulario: ['el', 'perro', 'gato', 'come', 'juega']

Texto 1: "el perro come"
Vector: [1,     1,      0,   1,    0]  -> el=1, perro=1, gato=0, come=1, juega=0

Texto 2: "el gato juega"
Vector: [1,     0,     1,   0,    1]  -> el=1, perro=0, gato=1, come=0, juega=1

VENTAJAS:
- Muy simple y rápido
- Fácil de entender

DESVENTAJAS:
- Le da la misma importancia a TODAS las palabras
- En "el perro come", la palabra "el" es la más frecuente pero menos importante
- Pierde el orden de las palabras
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def explicar_bow():
    """
    Función que EXPLICA y DEMUESTRA cómo funciona Bag of Words
    """
    print("\n" + "="*80)
    print("BAG OF WORDS (BOW) - LA BOLSA DE PALABRAS")
    print("="*80)
    
    # PASO 1: Preparar el corpus (colección de documentos/textos)
    # Estos son nuestros textos de ejemplo
    corpus = [
        'el perro come la comida',
        'el gato come pescado, el gato orina, el gato mira a la ventana',
        'el perro juega con el gato'
    ]
    
    print("\n📚 CORPUS (textos que vamos a analizar):")
    for i, texto in enumerate(corpus, 1):
        print(f"   Texto {i}: '{texto}'")
    
    # PASO 2: Crear el vectorizador (herramienta que hace el trabajo)
    print("\n🔨 CREANDO EL VECTORIZADOR...")
    vectorizer = CountVectorizer()
    
    # PASO 3: Ajustar y transformar (fit_transform)
    # - fit_transform crea el vocabulario y convierte los textos en números
    print("✅ Analizando textos y creando vocabulario...")
    X = vectorizer.fit_transform(corpus)
    
    # PASO 4: Ver el vocabulario (todas las palabras únicas)
    print("\n📖 VOCABULARIO CREADO (todas las palabras únicas):")
    vocabulario = vectorizer.get_feature_names_out()
    for i, palabra in enumerate(vocabulario):
        print(f"   {i}: '{palabra}'")
    
    # PASO 5: Convertir a un DataFrame para ver mejor
    # DataFrame = tabla con filas y columnas (como en Excel)
    bow_df = pd.DataFrame(
        X.toarray(),  # Convertir a array (tabla)
        columns=vocabulario,  # Las columnas son las palabras
        index=[f'Texto {i+1}' for i in range(len(corpus))]  # Las filas son los textos
    )
    
    print("\n📊 MATRIZ DE BAG OF WORDS:")
    print(bow_df)
    print("\n💡 EXPLICACIÓN:")
    print("   - Cada FILA = un texto")
    print("   - Cada COLUMNA = una palabra del vocabulario")
    print("   - Cada VALOR = cuántas veces aparece esa palabra en ese texto")
    
    # PASO 6: Análisis de resultados
    print("\n🔍 ANÁLISIS:")
    print(f"\n   📈 Frecuencia total de cada palabra (en todo el corpus):")
    frecuencias = bow_df.sum()
    for palabra, freq in frecuencias.items():
        print(f"      '{palabra}': {int(freq)} veces")
    
    print("\n   ⚠️  PROBLEMA IDENTIFICADO:")
    print("      La palabra 'el' aparece {} veces (LA MÁS FRECUENTE)".format(int(frecuencias['el'])))
    print("      Pero 'el' es una palabra común (artículo) con poco significado")
    print("      Mientras que 'pescado' aparece solo 1 vez pero es muy significativo")
    
    return vectorizer, X, bow_df, corpus


def practicar_bow_nuevo_texto():
    """
    Función para practicar con nuevos textos usando BoW entrenado
    """
    print("\n" + "="*80)
    print("PRACTICANDO BOW CON NUEVOS TEXTOS")
    print("="*80)
    
    # Usamos el vectorizador entrenado anteriormente
    vectorizer = CountVectorizer()
    
    # Textos de entrenamiento (los que usamos para crear el vocabulario)
    corpus_entrenamiento = [
        'el perro come la comida',
        'el gato come pescado, el gato orina, el gato mira a la ventana',
        'el perro juega con el gato'
    ]
    
    # Entrenar el vectorizador
    vectorizer.fit(corpus_entrenamiento)
    
    # Nuevos textos para analizar
    nuevo_texto = ['el gato come comida']
    
    print(f"\n📝 Nuevo texto a analizar: '{nuevo_texto[0]}'")
    
    # Transformar el nuevo texto (SIN fit, solo transform)
    # Solo transform = usamos el vocabulario que ya tenemos
    X_nuevo = vectorizer.transform(nuevo_texto)
    
    # Ver el resultado
    nuevo_df = pd.DataFrame(
        X_nuevo.toarray(),
        columns=vectorizer.get_feature_names_out(),
        index=['Nuevo Texto']
    )
    
    print("\n📊 Vector del nuevo texto:")
    print(nuevo_df)
    print("\n💡 Interpretación:")
    print(f"   - El gato aparece 1 vez")
    print(f"   - Comida aparece 1 vez")
    print(f"   - Las demás palabras no aparecen (valor 0)")


if __name__ == "__main__":
    # Ejecutar la explicación
    vectorizer, X, bow_df, corpus = explicar_bow()
    
    # Practicar con nuevos textos
    practicar_bow_nuevo_texto()
    
    print("\n" + "="*80)
    print("✅ BOW FINALIZADO")
    print("="*80)

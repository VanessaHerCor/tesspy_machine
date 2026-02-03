"""
=============================================================================
TÉCNICA 2: TF-IDF (TERM FREQUENCY - INVERSE DOCUMENT FREQUENCY)
=============================================================================

¿QUÉ ES?
--------
TF-IDF es una MEJORA de Bag of Words. Intenta resolver el problema:
"Las palabras comunes como 'el', 'es', 'y' son muy frecuentes pero poco útiles"

TF-IDF da una PUNTUACIÓN a cada palabra basada en:
- TF (Term Frequency): ¿Qué tan frecuente es la palabra en UN documento?
- IDF (Inverse Document Frequency): ¿Qué tan rara es la palabra en TODOS los documentos?

FÓRMULA (simplificada):
-----------------------
TF-IDF = TF × IDF

Donde:
  TF = frecuencia de la palabra en el documento
  IDF = log(total de documentos / documentos que contienen la palabra)

INTUICIÓN:
---------
- Palabras COMUNES en muchos documentos → IDF BAJO → TF-IDF BAJO
  Ejemplo: "el", "es", "y" aparecen en casi todo
  
- Palabras RARAS en pocos documentos → IDF ALTO → TF-IDF ALTO
  Ejemplo: "pescado", "juega" aparecen en pocos textos, son MÁS IMPORTANTES
  
RESULTADO:
---------
TF-IDF es ALTO cuando:
✓ La palabra aparece MUCHAS VECES en el documento (TF alto)
✓ La palabra aparece en POCOS documentos (IDF alto)

EJEMPLO:
--------
Corpus:
  Doc1: "el perro come carne"
  Doc2: "el gato come pescado, el perro comida"
  Doc3: "el perro juega con el gato"

Analizar "pescado":
  - Aparece 1 vez en Doc2 → TF es bajo
  - Aparece en SOLO 1 documento → IDF es ALTO
  - Resultado: TF-IDF es ALTO (palabra importante/distintiva)

Analizar "el":
  - Aparece muchas veces en los documentos → TF alto
  - Aparece en los 3 documentos → IDF es BAJO
  - Resultado: TF-IDF es BAJO (palabra común, poco útil)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def explicar_tfidf():
    """
    Función que EXPLICA y DEMUESTRA cómo funciona TF-IDF
    """
    print("\n" + "="*80)
    print("TF-IDF (TERM FREQUENCY - INVERSE DOCUMENT FREQUENCY)")
    print("="*80)
    
    # PASO 1: Preparar el corpus
    corpus = [
        'el perro come carne',
        'el gato come pescado, el perro comida',
        'el perro juega con el gato'
    ]
    
    print("\n📚 CORPUS (textos que vamos a analizar):")
    for i, texto in enumerate(corpus, 1):
        print(f"   Texto {i}: '{texto}'")
    
    # PASO 2: Crear el vectorizador TF-IDF
    print("\n🔨 CREANDO EL VECTORIZADOR TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer()
    
    # PASO 3: Ajustar y transformar
    print("✅ Calculando TF-IDF para cada palabra en cada documento...")
    X_tfidf = tfidf_vectorizer.fit_transform(corpus)
    
    # PASO 4: Ver el vocabulario
    print("\n📖 VOCABULARIO:")
    vocabulario = tfidf_vectorizer.get_feature_names_out()
    for i, palabra in enumerate(vocabulario):
        print(f"   {i}: '{palabra}'")
    
    # PASO 5: Crear DataFrame para visualizar
    tfidf_df = pd.DataFrame(
        X_tfidf.toarray(),
        columns=vocabulario,
        index=[f'Texto {i+1}' for i in range(len(corpus))]
    )
    
    print("\n📊 MATRIZ TF-IDF (valores de importancia):")
    print(tfidf_df)
    print("\n💡 EXPLICACIÓN:")
    print("   - Cada FILA = un texto")
    print("   - Cada COLUMNA = una palabra")
    print("   - Cada VALOR = IMPORTANCIA de esa palabra en ese texto (0 a 1)")
    print("   - VALOR MÁS ALTO = palabra más distintiva/importante")
    
    # PASO 6: Análisis detallado
    print("\n🔍 ANÁLISIS DETALLADO:")
    print("\n   Comparación de palabras:")
    print(f"\n   • 'el' en Texto 1: {tfidf_df.loc['Texto 1', 'el']:.4f}")
    print(f"     → Aparece en muchos textos → IDF BAJO → TF-IDF BAJO")
    print(f"     → Palabra COMÚN, poco distintiva")
    
    print(f"\n   • 'pescado' en Texto 2: {tfidf_df.loc['Texto 2', 'pescado']:.4f}")
    print(f"     → Aparece en solo 1 texto → IDF ALTO → TF-IDF ALTO")
    print(f"     → Palabra RARA, muy distintiva")
    
    print(f"\n   • 'juega' en Texto 3: {tfidf_df.loc['Texto 3', 'juega']:.4f}")
    print(f"     → Aparece en solo 1 texto → IDF ALTO → TF-IDF ALTO")
    print(f"     → Palabra RARA, muy distintiva")
    
    # PASO 7: Comparación con BoW
    print("\n⚡ COMPARACIÓN: BoW vs TF-IDF")
    print("   BoW: cuenta frecuencias sin importancia")
    print("   TF-IDF: pondera las palabras por su importancia")
    
    from sklearn.feature_extraction.text import CountVectorizer
    bow_vectorizer = CountVectorizer()
    X_bow = bow_vectorizer.fit_transform(corpus)
    
    bow_df = pd.DataFrame(
        X_bow.toarray(),
        columns=bow_vectorizer.get_feature_names_out(),
        index=[f'Texto {i+1}' for i in range(len(corpus))]
    )
    
    print("\n   MATRIZ BOW (frecuencias):")
    print(bow_df)
    
    print("\n   ✅ VENTAJA de TF-IDF:")
    print("      - Reduce la importancia de palabras muy comunes")
    print("      - Destaca palabras distintivas/importantes")
    
    return tfidf_vectorizer, X_tfidf, tfidf_df, corpus


def practicar_tfidf_similitud():
    """
    Función para practicar TF-IDF y calcular similitud entre documentos
    """
    print("\n" + "="*80)
    print("PRACTICANDO TF-IDF CON SIMILITUD")
    print("="*80)
    
    corpus = [
        'el perro come carne',
        'el gato come pescado',
        'el gato juega con la pelota'
    ]
    
    # Crear y entrenar TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    X_tfidf = tfidf_vectorizer.fit_transform(corpus)
    
    # Calcular similitud usando cosine_similarity
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Matriz de similitud
    similitud = cosine_similarity(X_tfidf)
    
    similitud_df = pd.DataFrame(
        similitud,
        index=[f'Texto {i+1}' for i in range(len(corpus))],
        columns=[f'Texto {i+1}' for i in range(len(corpus))]
    )
    
    print("\n📊 MATRIZ DE SIMILITUD (cosine similarity):")
    print(similitud_df)
    print("\n💡 EXPLICACIÓN:")
    print("   - Valores entre 0 y 1")
    print("   - 1 = textos idénticos")
    print("   - 0 = textos completamente diferentes")
    print("   - Basada en la similitud del COSENO (ángulo entre vectores)")
    
    print("\n🔍 INTERPRETACIÓN:")
    print(f"\n   Texto 1 vs Texto 2: {similitud_df.loc['Texto 1', 'Texto 2']:.4f}")
    print("   → Ambos hablan de animales comiendo (similitud media)")
    
    print(f"\n   Texto 2 vs Texto 3: {similitud_df.loc['Texto 2', 'Texto 3']:.4f}")
    print("   → Ambos hablan de GATOS (similitud alta)")


if __name__ == "__main__":
    # Ejecutar la explicación
    tfidf_vectorizer, X_tfidf, tfidf_df, corpus = explicar_tfidf()
    
    # Practicar con similitud
    practicar_tfidf_similitud()
    
    print("\n" + "="*80)
    print("✅ TF-IDF FINALIZADO")
    print("="*80)

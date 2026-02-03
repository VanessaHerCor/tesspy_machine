"""
=============================================================================
TÉCNICA 3: WORD2VEC - EMBEDDINGS ESTÁTICOS (CONTEXTO SIMPLE)
=============================================================================

¿QUÉ ES?
--------
Word2Vec crea EMBEDDINGS: vectores que capturan el SIGNIFICADO de las palabras.
No solo cuenta frecuencias, sino que APRENDE relaciones entre palabras.

DIFERENCIA CON BoW Y TF-IDF:
----------------------------
  BoW/TF-IDF: "¿Cuántas veces aparece cada palabra?"
              → Resultado: matriz de números sin mucho significado

  Word2Vec: "¿Cuál es el CONTEXTO en el que aparece la palabra?"
            "¿Qué palabras aparecen cerca de ella?"
            → Resultado: vectores que capturan el SIGNIFICADO
            
IDEA PRINCIPAL:
---------------
"Las palabras que aparecen en contextos similares tienen significados similares"

Ejemplos:
  • "rey" y "reina" aparecen cerca de: hombre, mujer, corona, poder
    → Sus vectores serán SIMILARES
  
  • "perro" y "gato" aparecen con: animal, mascotas, juegan, comen
    → Sus vectores serán SIMILARES
  
  • "perro" y "contenedor" no aparecen en contextos similares
    → Sus vectores serán DIFERENTES

VENTAJA IMPORTANTE:
-------------------
Word2Vec es ESTÁTICO: cada palabra tiene UN SOLO vector (no cambia con contexto)
Esto es simple pero limitado (lo veremos más tarde con BERT)

CÓMO FUNCIONA (muy simplificado):
---------------------------------
1. Toma un corpus de textos
2. Para cada palabra, mira las palabras VECINAS (dentro de una ventana)
3. Aprende: "¿Si veo esta palabra, qué otras palabras probablemente vea cerca?"
4. Codifica eso en un vector de números
5. Palabras que co-aparecen frecuentemente tienen vectores SIMILARES

VECTOR RESULTANTE:
------------------
En lugar de:
  "perro" → [0, 1, 0, 0, 0, 1, 0, 0, 0, ...]  (BoW, solo 0s y 1s)

Word2Vec crea:
  "perro" → [0.23, -0.54, 0.81, 0.12, -0.33, ...]  (valores continuos con significado)

CARACTERÍSTICAS MÁGICAS:
-----------------------
• Analogías: rey - hombre + mujer ≈ reina
  (La matemática de los vectores captura las relaciones!)
  
• Similitud: cosine_similarity(vector_perro, vector_gato) ≈ 0.85
  (Vectores similares = palabras relacionadas)
"""

import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity


def explicar_word2vec():
    """
    Función que EXPLICA y DEMUESTRA cómo funciona Word2Vec
    """
    print("\n" + "="*80)
    print("WORD2VEC - EMBEDDINGS DE PALABRAS")
    print("="*80)
    
    # PASO 1: Preparar corpus
    # Nota: Word2Vec necesita el corpus como LISTA DE LISTAS de palabras
    print("\n📚 PREPARANDO CORPUS...")
    corpus = [
        ['rey', 'es', 'un', 'hombre', 'poderoso'],
        ['reina', 'es', 'una', 'mujer', 'poderosa'],
        ['mujer', 'es', 'inteligente'],
        ['el', 'rey', 'gobierna', 'el', 'reino'],
        ['la', 'reina', 'gobierna', 'el', 'reino']
    ]
    
    print("Oraciones del corpus:")
    for i, sent in enumerate(corpus, 1):
        print(f"   {i}. {' '.join(sent)}")
    
    # PASO 2: Entrenar Word2Vec
    print("\n🤖 ENTRENANDO WORD2VEC...")
    print("   (Analizando relaciones entre palabras en el corpus...)")
    
    # Parámetros:
    # vector_size: cuántos números en cada vector (10 = 10 dimensiones)
    # window: cuántas palabras a cada lado mirar (5 = mira 5 palabras antes y después)
    # min_count: ignorar palabras que aparecen menos de 1 vez
    model = Word2Vec(
        sentences=corpus,
        vector_size=10,  # Vectores de 10 dimensiones
        window=5,        # Ventana de contexto de 5 palabras
        min_count=1,     # Incluir todas las palabras
        workers=4,       # Usar 4 procesadores
        epochs=100       # Entrenar 100 veces (más entrenamiento = mejor)
    )
    
    print("✅ Entrenamiento completado!")
    
    # PASO 3: Explorar los vectores
    print("\n📊 VECTORES APRENDIDOS:")
    print("\n   Vector para 'rey' (10 números):")
    vector_rey = model.wv['rey']
    print(f"   {vector_rey}")
    print("   (Estos números capturan el 'significado' de 'rey' según el corpus)")
    
    print("\n   Vector para 'reina':")
    vector_reina = model.wv['reina']
    print(f"   {vector_reina}")
    
    print("\n   Vector para 'contenedor' (palabra no en el corpus):")
    try:
        vector_contenedor = model.wv['contenedor']
        print(f"   {vector_contenedor}")
    except KeyError:
        print("   ❌ Error: 'contenedor' no está en el vocabulario")
        print("      (solo puede representar palabras que vio durante el entrenamiento)")
    
    # PASO 4: Similitud entre palabras
    print("\n🔍 SIMILITUD ENTRE PALABRAS (cosine similarity):")
    print("   (1.0 = idénticas, 0.0 = completamente diferentes)")
    
    # Calcular similitudes
    sim_rey_reina = model.wv.similarity('rey', 'reina')
    sim_rey_hombre = model.wv.similarity('rey', 'hombre')
    sim_rey_mujer = model.wv.similarity('rey', 'mujer')
    sim_rey_gato = model.wv.similarity('rey', 'inteligente')
    
    print(f"\n   'rey' vs 'reina': {sim_rey_reina:.4f}")
    print("   ✓ MUY SIMILAR (ambos son monarcas)")
    
    print(f"\n   'rey' vs 'hombre': {sim_rey_hombre:.4f}")
    print("   ✓ SIMILAR (rey es hombre)")
    
    print(f"\n   'rey' vs 'mujer': {sim_rey_mujer:.4f}")
    print("   ✗ MENOS SIMILAR (rey es típicamente hombre, no mujer)")
    
    print(f"\n   'rey' vs 'inteligente': {sim_rey_gato:.4f}")
    print("   ✗ POCO SIMILAR (características diferentes)")
    
    # PASO 5: Palabras más similares
    print("\n🎯 PALABRAS MÁS SIMILARES A 'rey':")
    similares_rey = model.wv.most_similar('rey', topn=3)
    for palabra, similitud in similares_rey:
        print(f"   • {palabra}: {similitud:.4f}")
    
    print("\n🎯 PALABRAS MÁS SIMILARES A 'mujer':")
    similares_mujer = model.wv.most_similar('mujer', topn=3)
    for palabra, similitud in similares_mujer:
        print(f"   • {palabra}: {similitud:.4f}")
    
    return model


def demostrar_analogias(model):
    """
    Función que DEMUESTRA la propiedad más mágica de Word2Vec: las ANALOGÍAS
    
    Ejemplo: rey - hombre + mujer ≈ reina
    
    Explicación:
    - Tomamos el vector de 'rey'
    - Le restamos el vector de 'hombre' (quitamos la característica "masculino")
    - Le sumamos el vector de 'mujer' (añadimos la característica "femenino")
    - ¡El resultado es el vector más cercano a 'reina'!
    """
    print("\n" + "="*80)
    print("ANALOGÍAS EN WORD2VEC (¡LA PARTE MÁGICA!)")
    print("="*80)
    
    print("\n✨ EJEMPLO: Rey - Hombre + Mujer = ?")
    print("   Pregunta: ¿Si rey es a hombre como X es a mujer?")
    print("   Respuesta esperada: REINA")
    
    print("\n   Explicación matemática:")
    print("   vector('rey') - vector('hombre') + vector('mujer') ≈ vector('reina')")
    print("   Porque:")
    print("      • vector('rey') - vector('hombre') = característica 'royal'")
    print("      • + vector('mujer') = aplicar 'royal' a una mujer")
    print("      • = vector('reina')")
    
    try:
        resultado = model.wv.most_similar(
            positive=['rey', 'mujer'],  # Sumar estos vectores
            negative=['hombre'],         # Restar este vector
            topn=3
        )
        
        print("\n🎯 RESULTADO DE LA ANALOGÍA:")
        print("   Palabras más cercanas a (rey - hombre + mujer):")
        for palabra, similitud in resultado:
            print(f"   • {palabra}: {similitud:.4f}")
            if palabra == 'reina':
                print("     ✨ ¡CORRECTO! Es la respuesta que esperábamos!")
    
    except Exception as e:
        print(f"\n⚠️  No se pudo completar la analogía: {e}")
        print("    (Esto puede ocurrir si el corpus es muy pequeño)")


def comparar_con_bow():
    """
    Función que COMPARA Word2Vec con BoW para mostrar las diferencias
    """
    print("\n" + "="*80)
    print("COMPARACIÓN: BoW vs TF-IDF vs Word2Vec")
    print("="*80)
    
    print("\nPara la palabra 'rey':")
    
    print("\n1️⃣  BOW (Bag of Words):")
    print("    Resultado: [0, 1, 0, 0, 0, 1, 0, 0, 0, ...]")
    print("    → Solo cuenta: ¿aparece o no? (0 o 1)")
    print("    → No hay información sobre significado")
    
    print("\n2️⃣  TF-IDF:")
    print("    Resultado: [0, 0.34, 0, 0, 0, 0.67, 0, 0, 0, ...]")
    print("    → Cuenta frecuencia y rareza")
    print("    → Pondera palabras más importantes")
    print("    → Pero sigue siendo un conteo, no significado real")
    
    print("\n3️⃣  WORD2VEC:")
    print("    Resultado: [0.23, -0.54, 0.81, 0.12, -0.33, 0.19, ...]")
    print("    → Números que representan SIGNIFICADO")
    print("    → Captura relaciones con otras palabras")
    print("    → Permite calcular similitud y analogías")
    print("    → Mucho más poderoso para tareas de IA")
    
    print("\n✅ VENTAJAS DE WORD2VEC:")
    print("    • Captura significado semántico")
    print("    • Permite similitud entre palabras")
    print("    • Permite analogías")
    print("    • Input ideal para redes neuronales")
    
    print("\n⚠️  DESVENTAJAS DE WORD2VEC:")
    print("    • Cada palabra tiene UN SOLO vector (no contextual)")
    print("    • 'banco' = institución financiera o asiento")
    print("      → Ambos significados tienen el MISMO vector")
    print("    • No distingue por contexto")
    print("    • Necesita entrenamiento previo")


if __name__ == "__main__":
    # Entrenar y explicar Word2Vec
    model = explicar_word2vec()
    
    # Demostrar analogías
    demostrar_analogias(model)
    
    # Comparar con otras técnicas
    comparar_con_bow()
    
    print("\n" + "="*80)
    print("✅ WORD2VEC FINALIZADO")
    print("="*80)
    print("\n💡 PRÓXIMO PASO: BERT (embeddings CONTEXTUALES)")
    print("   BERT usa el mismo principio pero con inteligencia adicional:")
    print("   ¡Cada palabra obtiene vectores DIFERENTES según el contexto!")

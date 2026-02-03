"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           EJEMPLOS AVANZADOS - DESPUÉS DE DOMINAR LOS BÁSICOS               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Este archivo tiene ejemplos MÁS COMPLEJOS que puedes intentar después
de entender las 4 técnicas básicas.

NO EJECUTES ESTO AL PRINCIPIO - primero domina:
  ✓ 1_bag_of_words.py
  ✓ 2_tfidf.py
  ✓ 3_word2vec.py
  ✓ 4_bert.py

DESPUÉS, vuelve aquí y experimenta con estos ejemplos más avanzados.
"""

# ============================================================================
# EJEMPLO 1: ENCONTRAR DOCUMENTO MÁS SIMILAR
# ============================================================================

def ejemplo_1_documento_similar():
    """
    Problema: Tienes 5 documentos y quieres encontrar cuál es más
    similar a una consulta del usuario.
    
    Casos de uso real:
    - Motor de búsqueda
    - Sistema de recomendaciones
    - Detección de duplicados
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: ENCONTRAR DOCUMENTO MÁS SIMILAR")
    print("="*80)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Base de datos de documentos
    documentos = [
        "El perro es una mascota leal y amorosa",
        "Los gatos son independientes y les encanta dormir",
        "Python es un lenguaje de programación versátil",
        "La inteligencia artificial revoluciona el mundo",
        "El fútbol es el deporte más popular del mundo"
    ]
    
    # Consulta del usuario
    consulta = "Quiero aprender sobre lenguajes de programación"
    
    print(f"\n📚 DOCUMENTOS EN LA BASE DE DATOS:")
    for i, doc in enumerate(documentos, 1):
        print(f"   {i}. {doc}")
    
    print(f"\n🔍 CONSULTA: '{consulta}'")
    
    # Crear vectorizador TF-IDF
    vectorizer = TfidfVectorizer()
    
    # Combinar documentos + consulta
    todos = documentos + [consulta]
    
    # Vectorizar
    tfidf_matrix = vectorizer.fit_transform(todos)
    
    # Calcular similitud con la consulta (último documento)
    similaridades = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
    
    # Encontrar el más similar
    documento_mas_similar = max(enumerate(similaridades), key=lambda x: x[1])
    indice, similitud = documento_mas_similar
    
    print(f"\n✅ RESULTADO:")
    print(f"   Documento más similar: #{indice + 1}")
    print(f"   Contenido: '{documentos[indice]}'")
    print(f"   Similitud: {similitud:.2%}")
    
    print(f"\n💡 INTERPRETACIÓN:")
    print(f"   Similitud: {similitud:.2%}")
    print(f"   - 100% = idénticos")
    print(f"   - 0% = completamente diferentes")


# ============================================================================
# EJEMPLO 2: CLASIFICACIÓN SIMPLE (SPAM vs NO-SPAM)
# ============================================================================

def ejemplo_2_clasificacion_spam():
    """
    Problema: Tienes mensajes y quieres clasificarlos como SPAM o NO-SPAM
    usando similitud de TF-IDF
    
    Nota: Este es un ejemplo educativo. Para producción, usarías 
    modelos de machine learning como SVM, Naive Bayes, etc.
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: DETECTAR SPAM CON TF-IDF")
    print("="*80)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Ejemplos de mensajes SPAM típicos
    spam_ejemplos = [
        "GANA DINERO RÁPIDO!!! Hazte rico en 24 horas",
        "¡¡¡OFERTA INCREÍBLE!!! 50% de descuento en TODO",
        "Haz clic aquí para ganar un iPhone GRATIS",
        "Has sido seleccionado para recibir 1 millón de dólares"
    ]
    
    # Mensaje a clasificar
    mensaje = "¿Estás interesado en ganar dinero fácilmente sin esfuerzo?"
    
    print(f"\n📊 EJEMPLOS DE SPAM:")
    for i, spam in enumerate(spam_ejemplos, 1):
        print(f"   {i}. {spam}")
    
    print(f"\n🔍 MENSAJE A CLASIFICAR:")
    print(f"   '{mensaje}'")
    
    # Vectorizar
    vectorizer = TfidfVectorizer()
    todos = spam_ejemplos + [mensaje]
    tfidf = vectorizer.fit_transform(todos)
    
    # Calcular similitud con ejemplos SPAM
    similitudes = cosine_similarity(tfidf[-1:], tfidf[:-1])[0]
    similitud_promedio = similitudes.mean()
    
    print(f"\n📈 RESULTADOS:")
    for i, sim in enumerate(similitudes):
        print(f"   Similitud con spam {i+1}: {sim:.2%}")
    
    print(f"\n📊 SIMILITUD PROMEDIO CON SPAM: {similitud_promedio:.2%}")
    
    if similitud_promedio > 0.3:
        print(f"\n⚠️  CLASIFICACIÓN: PROBABLEMENTE SPAM")
        print(f"   Confianza: {similitud_promedio:.0%}")
    else:
        print(f"\n✓ CLASIFICACIÓN: NO SPAM")
        print(f"   Confianza: {(1-similitud_promedio):.0%}")
    
    print(f"\n💡 NOTA:")
    print(f"   Este es un ejemplo educativo.")
    print(f"   En producción usarías modelos ML más sofisticados.")


# ============================================================================
# EJEMPLO 3: ENCONTRAR PALABRAS SIMILARES CON WORD2VEC
# ============================================================================

def ejemplo_3_palabras_similares():
    """
    Usando Word2Vec, encontramos palabras relacionadas
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: ENCONTRAR SINÓNIMOS Y PALABRAS RELACIONADAS")
    print("="*80)
    
    from gensim.models import Word2Vec
    
    # Corpus más grande para entrenar Word2Vec
    corpus = [
        ['el', 'gato', 'es', 'una', 'mascota', 'domesticada'],
        ['el', 'perro', 'es', 'una', 'mascota', 'leal'],
        ['el', 'tigre', 'es', 'un', 'felino', 'salvaje'],
        ['el', 'león', 'es', 'un', 'felino', 'poderoso'],
        ['la', 'casa', 'es', 'el', 'hogar', 'del', 'hombre'],
        ['el', 'hogar', 'es', 'donde', 'vivimos'],
        ['el', 'coche', 'es', 'un', 'vehículo', 'rápido'],
        ['el', 'bus', 'es', 'un', 'vehículo', 'público']
    ]
    
    print(f"\n📚 Entrenando Word2Vec con {len(corpus)} documentos...")
    model = Word2Vec(corpus, vector_size=10, window=3, min_count=1, epochs=100)
    print("✅ Entrenamiento completado!")
    
    palabras_a_buscar = ['gato', 'coche', 'hogar']
    
    for palabra in palabras_a_buscar:
        print(f"\n🔍 PALABRAS SIMILARES A '{palabra}':")
        try:
            similares = model.wv.most_similar(palabra, topn=3)
            for pal_similar, similitud in similares:
                print(f"   • {pal_similar}: {similitud:.2%}")
        except KeyError:
            print(f"   ❌ '{palabra}' no encontrada en el vocabulario")


# ============================================================================
# EJEMPLO 4: ANÁLISIS DE SENTIMIENTOS (BÁSICO)
# ============================================================================

def ejemplo_4_sentimientos():
    """
    Análisis simple de sentimientos usando TF-IDF
    (Para análisis real usarías modelos más complejos)
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: ANÁLISIS BÁSICO DE SENTIMIENTOS")
    print("="*80)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Palabras positivas y negativas
    positivas = [
        "Este producto es excelente",
        "Me encanta, muy bueno",
        "Fantástico, recomendado",
        "Maravilloso, super feliz"
    ]
    
    negativas = [
        "Producto terrible y defectuoso",
        "Muy malo, no lo recomiendo",
        "Horrible, peor compra",
        "Decepcionante y de baja calidad"
    ]
    
    # Texto a analizar
    comentario = "Es un buen producto pero tiene algunos problemas"
    
    print(f"\n😊 COMENTARIOS POSITIVOS:")
    for com in positivas[:2]:
        print(f"   • {com}")
    
    print(f"\n😞 COMENTARIOS NEGATIVOS:")
    for com in negativas[:2]:
        print(f"   • {com}")
    
    print(f"\n📝 COMENTARIO A ANALIZAR:")
    print(f"   '{comentario}'")
    
    # Vectorizar
    todos = positivas + negativas + [comentario]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(todos)
    
    # Calcular similitudes
    sim_positivos = cosine_similarity(tfidf[-1:], tfidf[:len(positivas)])[0]
    sim_negativos = cosine_similarity(tfidf[-1:], tfidf[len(positivas):len(positivas)+len(negativas)])[0]
    
    promedio_positivo = sim_positivos.mean()
    promedio_negativo = sim_negativos.mean()
    
    print(f"\n📊 RESULTADO:")
    print(f"   Similitud con comentarios POSITIVOS: {promedio_positivo:.2%}")
    print(f"   Similitud con comentarios NEGATIVOS: {promedio_negativo:.2%}")
    
    if promedio_positivo > promedio_negativo:
        print(f"\n😊 SENTIMIENTO POSITIVO")
    else:
        print(f"\n😞 SENTIMIENTO NEGATIVO")
    
    print(f"\n💡 NOTA:")
    print(f"   Este análisis es muy básico.")
    print(f"   Para análisis real, usarías:")
    print(f"   - Modelos pre-entrenados (como BERT)")
    print(f"   - Librerías como TextBlob, VADER")
    print(f"   - Datos de entrenamiento específicos")


# ============================================================================
# EJEMPLO 5: VECTORIZACIÓN DE MÚLTIPLES TEXTOS
# ============================================================================

def ejemplo_5_comparar_multiples():
    """
    Comparar múltiples textos entre sí y encontrar patrones
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: COMPARAR MÚLTIPLES TEXTOS (MATRIZ DE SIMILITUD)")
    print("="*80)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import pandas as pd
    
    # Textos sobre diferentes temas
    textos = [
        "Python es un lenguaje de programación versátil",
        "Java también es un lenguaje de programación",
        "El fútbol es el deporte más popular",
        "El baloncesto es un deporte emocionante",
        "Las vacaciones en la playa son relajantes"
    ]
    
    print("\n📄 TEXTOS A COMPARAR:")
    for i, texto in enumerate(textos, 1):
        print(f"   {i}. {texto}")
    
    # Vectorizar
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(textos)
    
    # Matriz de similitud
    similitud = cosine_similarity(tfidf)
    
    # Mostrar como tabla
    df = pd.DataFrame(
        similitud,
        index=[f'Texto {i}' for i in range(1, len(textos)+1)],
        columns=[f'T{i}' for i in range(1, len(textos)+1)]
    )
    
    print("\n📊 MATRIZ DE SIMILITUD:")
    print(df.round(3))
    
    print("\n💡 INTERPRETACIÓN:")
    print("   - 1.0 = textos idénticos (diagonal principal)")
    print("   - > 0.5 = textos similares")
    print("   - < 0.3 = textos diferentes")
    
    print("\n🔍 AGRUPAMIENTOS DETECTADOS:")
    print("   • Textos 1-2: lenguajes de programación (similitud ~0.8)")
    print("   • Textos 3-4: deportes (similitud ~0.6)")
    print("   • Texto 5: actividades de ocio (diferente)")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Ejecuta todos los ejemplos avanzados
    """
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "EJEMPLOS AVANZADOS DE NLP".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        ejemplo_1_documento_similar()
        ejemplo_2_clasificacion_spam()
        ejemplo_3_palabras_similares()
        ejemplo_4_sentimientos()
        ejemplo_5_comparar_multiples()
        
        print("\n" + "="*80)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*80)
        
        print("\n💡 SIGUIENTES PASOS:")
        print("   1. Experimenta modificando los datos")
        print("   2. Intenta crear tus propios ejemplos")
        print("   3. Combina técnicas (TF-IDF + similitud, Word2Vec + clasificación, etc.)")
        print("   4. Aplica esto a problemas reales")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de tener instaladas las dependencias:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()

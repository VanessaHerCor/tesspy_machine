"""
=============================================================================
TÉCNICA 4: BERT - EMBEDDINGS CONTEXTUALES (¡LA REVOLUCIÓN!)
=============================================================================

¿QUÉ ES?
--------
BERT (Bidirectional Encoder Representations from Transformers) es la revolución
en Procesamiento del Lenguaje Natural.

A diferencia de Word2Vec:
  Word2Vec: Una palabra = UN SOLO vector (siempre igual)
  BERT: Una palabra = VECTORES DIFERENTES según el contexto

PROBLEMA QUE RESUELVE:
---------------------
La palabra "banco" tiene múltiples significados:
  1. "Voy al banco a sacar dinero" (institución financiera)
  2. "Me siento en el banco del parque" (asiento)

Word2Vec: Ambos "banco" usan el MISMO vector ❌
BERT: Cada contexto usa VECTORES DIFERENTES ✓

OTRO EJEMPLO: "PLANTA"
---------------------
Frase 1: "La planta de tomates necesita agua"
         → "planta" = ser vivo que crece (VECTOR A)

Frase 2: "La planta de fabricación cerrará mañana"
         → "planta" = fábrica/instalación (VECTOR B)

Frase 3: "El atleta sintió dolor en la planta del pie"
         → "planta" = parte del cuerpo (VECTOR C)

VECTOR A ≠ VECTOR B ≠ VECTOR C

¡Cada uno es diferente porque el CONTEXTO es diferente!

¿CÓMO FUNCIONA?
---------------
1. BERT analiza la ORACIÓN COMPLETA (antes y después de la palabra)
2. Usa REDES NEURONALES para entender el contexto
3. Genera un vector ÚNICO para esa palabra EN ESE CONTEXTO
4. Resultado: Mejor comprensión del significado real

¿POR QUÉ ES TAN POTENTE?
------------------------
✓ Entiende múltiples significados (polisemia)
✓ Entiende matices y contexto
✓ Usa información bidireccional (mira antes Y después)
✓ Pre-entrenado en MILLONES de textos
✓ Base de muchos modelos modernos (ChatGPT, etc.)

VENTAJAS SOBRE WORD2VEC:
------------------------
Word2Vec:
  - Rápido
  - Simple
  - Pero: no contextual

BERT:
  - Lento (necesita procesamiento complejo)
  - Complejo
  - Pero: contextual, más preciso, más inteligente ✨

DESVENTAJAS:
----------
- Más lento que Word2Vec
- Requiere más poder computacional
- Necesita librerías especiales (transformers)
- Requiere descargar un modelo pre-entrenado

NOTA: En este archivo usamos BERT en español (dccuchile/bert-base-spanish-wwm-cased)
"""

import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity


def cargar_bert_modelo():
    """
    Carga el modelo BERT pre-entrenado en español
    
    Este modelo fue entrenado con millones de textos en español,
    por lo que ya "entiende" el idioma español
    """
    print("\n" + "="*80)
    print("CARGANDO BERT (Puede tardar unos segundos en la primera ejecución)...")
    print("="*80)
    
    print("\n📦 Descargando modelo pre-entrenado...")
    print("   (dccuchile/bert-base-spanish-wwm-cased)")
    
    try:
        # Cargar tokenizador
        # El tokenizador convierte palabras en tokens que BERT entiende
        tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-cased')
        
        # Cargar modelo
        # El modelo genera los vectores
        model = BertModel.from_pretrained('dccuchile/bert-base-spanish-wwm-cased')
        
        print("✅ Modelo cargado exitosamente!")
        return tokenizer, model
    
    except Exception as e:
        print(f"\n❌ Error al cargar BERT: {e}")
        print("   Solución: Instala las dependencias con:")
        print("   pip install transformers torch")
        return None, None


def obtener_embedding_contextual(text, target_word, tokenizer, model):
    """
    Función para obtener el embedding (vector) de una palabra en un contexto específico
    
    Parámetros:
        text: la oración completa (contexto)
        target_word: la palabra cuyo vector queremos
        tokenizer: tokenizador BERT
        model: modelo BERT
    
    Retorna:
        vector numpy que representa la palabra en ese contexto
    """
    
    # PASO 1: Tokenizar la oración
    # Esto convierte la oración en tokens que BERT entiende
    print(f"\n📝 Analizando: '{text}'")
    print(f"   Palabra objetivo: '{target_word}'")
    
    inputs = tokenizer(text, return_tensors="pt")
    
    # PASO 2: Procesar con BERT (sin guardar gradientes = faster)
    # torch.no_grad() dice: "No necesito calcular derivadas, solo predicciones"
    print("   🤖 Procesando con BERT...")
    
    with torch.no_grad():
        # output_hidden_states=True: queremos ver todos los estados internos
        outputs = model(**inputs, output_hidden_states=True)
    
    # PASO 3: Extraer los estados ocultos (las capas internas de BERT)
    # BERT tiene 12 capas, cada una representa diferentes niveles de información
    hidden_states = outputs.hidden_states
    
    # PASO 4: Convertir tokens a palabras para entender qué pasó
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    print(f"   Tokens generados por BERT: {tokens}")
    
    # PASO 5: Encontrar dónde está la palabra que buscamos
    try:
        target_word_index = tokens.index(target_word)
        print(f"   ✓ Palabra '{target_word}' encontrada en posición {target_word_index}")
    except ValueError:
        print(f"   ❌ Palabra '{target_word}' no encontrada como token único")
        print(f"      Nota: BERT puede dividir palabras en sub-tokens")
        return None
    
    # PASO 6: Obtener los embeddings de las ÚLTIMAS 4 CAPAS de BERT
    # Las últimas capas contienen información más contextual y semántica
    # (las primeras capas son más básicas, como reconocer caracteres)
    last_four_layers = [hidden_states[i] for i in (-1, -2, -3, -4)]
    
    # Sumar los embeddings de las 4 últimas capas
    # Esto combina información de diferentes niveles de comprensión
    token_embeddings = torch.stack(last_four_layers).sum(0)
    
    # Extraer el embedding de nuestra palabra específica
    word_embedding = token_embeddings[0][target_word_index]
    
    # Convertir a numpy (formato que podemos usar fácilmente)
    return word_embedding.numpy()


def demostrar_contextualidad(tokenizer, model):
    """
    Demuestra cómo BERT genera VECTORES DIFERENTES para la misma palabra
    en contextos diferentes (¡esto es lo mágico!)
    """
    print("\n" + "="*80)
    print("DEMOSTRANDO LA CONTEXTUALIDAD DE BERT")
    print("="*80)
    
    print("\n✨ EXPERIMENTO: La palabra 'planta' en 3 contextos diferentes")
    print("="*80)
    
    # Tres oraciones con la palabra "planta" pero con significados diferentes
    oraciones = {
        'ser_vivo': "La planta de tomates que sembramos en el jardín necesita mucho sol y agua para crecer",
        'fabrica': "La planta de ensamblaje de coches en la zona industrial tuvo que cerrar por falta de suministros",
        'cuerpo': "El atleta sintió un dolor agudo en toda la planta del pie después de correr la maratón"
    }
    
    # Obtener los vectores para "planta" en cada contexto
    embeddings = {}
    
    for contexto, oracion in oraciones.items():
        print(f"\n{'='*80}")
        print(f"CONTEXTO: {contexto.upper()}")
        print(f"{'='*80}")
        
        embedding = obtener_embedding_contextual(oracion, 'planta', tokenizer, model)
        embeddings[contexto] = embedding
        
        if embedding is not None:
            print(f"   Vector generado: {embedding[:5]}... (primeros 5 valores de 768)")
            print(f"   Tamaño del vector: {len(embedding)} dimensiones")
    
    # PASO 2: Comparar los vectores con similitud del coseno
    print("\n" + "="*80)
    print("COMPARANDO LOS VECTORES (similitud del coseno)")
    print("="*80)
    
    if all(v is not None for v in embeddings.values()):
        # Calcular similitudes
        sim_vivo_fabrica = cosine_similarity(
            [embeddings['ser_vivo']], 
            [embeddings['fabrica']]
        )[0][0]
        
        sim_vivo_cuerpo = cosine_similarity(
            [embeddings['ser_vivo']], 
            [embeddings['cuerpo']]
        )[0][0]
        
        sim_fabrica_cuerpo = cosine_similarity(
            [embeddings['fabrica']], 
            [embeddings['cuerpo']]
        )[0][0]
        
        print(f"\n📊 RESULTADOS:")
        print(f"\n   Ser Vivo vs. Fábrica:  {sim_vivo_fabrica:.4f}")
        print("   ↓ Interpretación:")
        print("      Valores bajos (< 0.5) = contextos completamente diferentes")
        print("      BERT entiende que 'planta' significa cosas distintas")
        
        print(f"\n   Ser Vivo vs. Cuerpo:   {sim_vivo_cuerpo:.4f}")
        print("   ↓ Interpretación:")
        print("      Ambas son 'seres vivos' pero diferentes")
        
        print(f"\n   Fábrica vs. Cuerpo:    {sim_fabrica_cuerpo:.4f}")
        print("   ↓ Interpretación:")
        print("      Contextos muy diferentes")
        
        print("\n✅ CONCLUSIÓN:")
        print("   Los vectores para 'planta' son DIFERENTES en cada contexto")
        print("   ¡Esto demuestra que BERT es CONTEXTUAL!")
        print("   No usa el mismo vector siempre, sino que adapta según el contexto")


def comparacion_final():
    """
    Comparación final de todas las técnicas
    """
    print("\n" + "="*80)
    print("COMPARACIÓN FINAL: BoW vs TF-IDF vs Word2Vec vs BERT")
    print("="*80)
    
    tecnicas = {
        'Bag of Words': {
            'Qué hace': 'Cuenta frecuencia de palabras',
            'Output': '[0, 1, 0, 1, 0, 1, ...]  (0s y 1s)',
            'Contextual': '❌ No',
            'Rapidez': '⚡⚡⚡ Muy rápido',
            'Complejidad': '🟢 Muy simple',
            'Mejor para': 'Tareas simples, análisis rápido'
        },
        'TF-IDF': {
            'Qué hace': 'Pondera palabras por importancia',
            'Output': '[0.1, 0.34, 0.05, ...]  (números decimales)',
            'Contextual': '❌ No',
            'Rapidez': '⚡⚡⚡ Muy rápido',
            'Complejidad': '🟢 Simple',
            'Mejor para': 'Búsqueda de documentos, clasificación'
        },
        'Word2Vec': {
            'Qué hace': 'Aprende relaciones entre palabras',
            'Output': '[0.23, -0.54, 0.81, ...]  (valores significativos)',
            'Contextual': '❌ No (mismo vector siempre)',
            'Rapidez': '⚡⚡ Rápido',
            'Complejidad': '🟡 Media',
            'Mejor para': 'Similitud, analogías, entrada para redes'
        },
        'BERT': {
            'Qué hace': 'Entiende contexto y significado profundo',
            'Output': '[0.12, 0.89, -0.45, ...]  (768 valores contextuales)',
            'Contextual': '✅ Sí (vectores diferentes por contexto)',
            'Rapidez': '🐢 Lento',
            'Complejidad': '🔴 Muy complejo',
            'Mejor para': 'Tareas avanzadas, clasificación, análisis profundo'
        }
    }
    
    for tecnica, info in tecnicas.items():
        print(f"\n{'='*80}")
        print(f"🔹 {tecnica}")
        print(f"{'='*80}")
        for clave, valor in info.items():
            print(f"   {clave:20}: {valor}")
    
    print("\n" + "="*80)
    print("📈 EVOLUCIÓN DEL PODER")
    print("="*80)
    print("\nBoW → TF-IDF → Word2Vec → BERT")
    print("     ↓         ↓           ↓")
    print("   Mejora   Mejora     🚀 REVOLUCIÓN")
    print("\nCada técnica es más poderosa pero también más lenta/compleja")


if __name__ == "__main__":
    # Cargar modelo BERT
    tokenizer, model = cargar_bert_modelo()
    
    if tokenizer and model:
        # Demostrar contextualidad
        demostrar_contextualidad(tokenizer, model)
        
        # Comparación final
        comparacion_final()
        
        print("\n" + "="*80)
        print("✅ BERT FINALIZADO")
        print("="*80)
    else:
        print("\n❌ No se pudo completar el ejercicio de BERT")

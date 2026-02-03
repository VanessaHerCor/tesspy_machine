"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                 APRENDE PROCESAMIENTO DEL LENGUAJE NATURAL (NLP)             ║
║                                                                              ║
║              🎓 Guía Práctica y Educativa de Técnicas NLP                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

¿QUÉ ES ESTE PROYECTO?
======================

Este proyecto contiene práctica educativa sobre las técnicas MÁS IMPORTANTES 
del Procesamiento del Lenguaje Natural (NLP), basadas en las clases que viste:

  • Tutoría PYTHON IV 17: Tokenización
  • Tutoría PYTHON IV 18: Lenguaje Natural e Introducción a Embeddings
  • Tutoría PYTHON IV 19: Lenguaje Natural

CONTENIDO DEL PROYECTO
======================

Este archivo (main.py) es el PUNTO DE ENTRADA. Desde aquí puedes:

1. Elegir qué técnica quieres practicar
2. Cada técnica está en su propio archivo en la carpeta 'tecnicas/'

ARCHIVO                    TÉCNICA
─────────────────────────────────────────────────────────────────────────────
tecnicas/1_bag_of_words.py → Bag of Words (BoW) - LO MÁS BÁSICO
                             • Cuenta frecuencia de palabras
                             • Muy simple y rápido
                             • Base de todo lo demás

tecnicas/2_tfidf.py        → TF-IDF - MEJORA DE BOW
                             • Pondera palabras por importancia
                             • Elimina palabras comunes innecesarias
                             • Estándar en búsqueda de documentos

tecnicas/3_word2vec.py     → Word2Vec - EMBEDDINGS ESTÁTICOS
                             • Aprende significado de palabras
                             • Captura relaciones (análogas, similitud)
                             • Entrada ideal para redes neuronales

tecnicas/4_bert.py         → BERT - EMBEDDINGS CONTEXTUALES ⭐
                             • Lo más avanzado aquí
                             • Entiende contexto
                             • Base de ChatGPT, Google, etc.

CÓMO USAR ESTE PROYECTO
=======================

1️⃣  OPCIÓN 1: Ejecutar CADA TÉCNICA POR SEPARADO
    ├── python tecnicas/1_bag_of_words.py
    ├── python tecnicas/2_tfidf.py
    ├── python tecnicas/3_word2vec.py
    └── python tecnicas/4_bert.py

2️⃣  OPCIÓN 2: Ejecutar ESTE ARCHIVO (main.py) para un MENÚ INTERACTIVO
    └── python main.py
    (Elige qué técnica quieres practicar)

RECOMENDACIÓN PARA APRENDER
===========================

ORDEN RECOMENDADO (de fácil a difícil):

  1. BoW        → Entiende lo básico (frecuencias)
  2. TF-IDF     → Mejora sobre BoW (ponderación)
  3. Word2Vec   → Salto conceptual: VECTORES con significado
  4. BERT       → La culminación: contexto + profundidad

Después de ejecutar cada uno:
  ✓ Lee el código comentado
  ✓ Entiende qué hace cada sección
  ✓ Experimenta con nuevos ejemplos
  ✓ Luego pasa al siguiente

NOTAS IMPORTANTES
=================

⚠️  Primera ejecución:
    - La primera vez descargará modelos (~500MB)
    - Puede tardar unos minutos
    - Después será más rápido

📦 Dependencias necesarias:
    pip install scikit-learn pandas gensim transformers torch

🎯 Objetivo:
    Entender PROFUNDAMENTE cómo se convierte TEXTO en NÚMEROS
    para que las máquinas puedan procesarlo

💡 Consejo:
    No solo ejecutes el código, LÉELO y ENTIÉNDELO
    Cada parte está comentada para tu comprensión

================================================================================
"""

import os
import sys
from pathlib import Path


def mostrar_menu():
    """
    Muestra el menú interactivo para elegir qué técnica practicar
    """
    print("\n" + "="*80)
    print("🎓 MENÚ DE TÉCNICAS NLP")
    print("="*80)
    
    opciones = {
        '1': ('Bag of Words (BoW)', 'tecnicas/1_bag_of_words.py'),
        '2': ('TF-IDF', 'tecnicas/2_tfidf.py'),
        '3': ('Word2Vec', 'tecnicas/3_word2vec.py'),
        '4': ('BERT (Embeddings Contextuales)', 'tecnicas/4_bert.py'),
        '5': ('Ver explicación de todas las técnicas', None),
        '0': ('Salir', None)
    }
    
    for clave, (nombre, archivo) in opciones.items():
        print(f"\n   {clave}. {nombre}")
        if archivo:
            print(f"      📂 {archivo}")
    
    print("\n" + "="*80)
    return opciones


def ejecutar_tecnica(ruta_archivo):
    """
    Ejecuta el archivo Python de una técnica
    """
    # Convertir a ruta absoluta
    ruta_completa = Path(__file__).parent / ruta_archivo
    
    if not ruta_completa.exists():
        print(f"\n❌ Error: El archivo {ruta_completa} no existe")
        return
    
    print(f"\n▶️  Ejecutando: {ruta_archivo}")
    print("="*80)
    
    # Ejecutar el archivo
    import subprocess
    resultado = subprocess.run([sys.executable, str(ruta_completa)])
    
    if resultado.returncode != 0:
        print(f"\n⚠️  Hubo un error ejecutando {ruta_archivo}")
        print("   Asegúrate de tener instaladas todas las dependencias:")
        print("   pip install scikit-learn pandas gensim transformers torch")


def mostrar_explicacion_general():
    """
    Muestra una explicación general del flujo NLP
    """
    print("\n" + "="*80)
    print("📚 EXPLICACIÓN GENERAL: CONVERSIÓN DE TEXTO A NÚMEROS")
    print("="*80)
    
    print("""
¿POR QUÉ CONVERTIR TEXTO A NÚMEROS?
====================================

Las máquinas NO entienden texto como nosotros. Los modelos de IA solo entienden
NÚMEROS. Entonces, el primer paso SIEMPRE es:

    TEXTO → (proceso mágico) → NÚMEROS
    
    Ejemplo:
    --------
    "El perro come"  → [0.23, -0.54, 0.81, 0.12, -0.33, ...]
    
    Estos números representan el SIGNIFICADO y CONTEXTO de la frase.


EL FLUJO COMPLETO (de simple a complejo)
==========================================

1. TOKENIZACIÓN
   ──────────────
   "El perro come" → ["El", "perro", "come"]
   
   ¿QUÉ HACE?
   • Divide el texto en unidades básicas (palabras, caracteres, etc.)
   • Primer paso obligatorio
   • Los tokens se convierten a números


2. BAG OF WORDS (BoW)
   ──────────────────
   Vocabulario: [el, perro, come]
   Vector: [1, 1, 1]  (aparece 1 vez cada palabra)
   
   ¿QUÉ HACE?
   • Cuenta cuántas veces aparece cada palabra
   • Muy simple, muy rápido
   • Pero pierde el orden y el significado


3. TF-IDF
   ──────
   Vector: [0.1, 0.7, 0.6]  (números ponderados)
   
   ¿QUÉ HACE?
   • Mejora BoW: da menos peso a palabras comunes ("el")
   • Da más peso a palabras significativas ("perro")
   • Mejor para búsqueda de documentos


4. WORD2VEC
   ─────────
   "perro" → [0.23, -0.54, 0.81, 0.12, -0.33, ...]  (10 números)
   
   ¿QUÉ HACE?
   • Cada palabra → vector con SIGNIFICADO
   • Palabras similares → vectores similares
   • Permite analogías: "rey - hombre + mujer ≈ reina"
   • Pero: mismo vector siempre (no contextual)


5. BERT (¡LA REVOLUCIÓN!)
   ──────────────────────
   Contexto 1: "banco" (institución) → [0.12, 0.89, -0.45, ...]
   Contexto 2: "banco" (asiento)     → [0.34, 0.12, 0.67, ...]
   
   ¿QUÉ HACE?
   • Cada palabra → vectores DIFERENTES por CONTEXTO
   • Entiende múltiples significados
   • Entiende el contexto de toda la oración
   • Es la base de ChatGPT y modelos modernos
   • Pero: es lento y complejo


RESUMEN VISUAL
==============

Precisión:     BoW < TF-IDF < Word2Vec < BERT
               🟢  →  🟡    →   🟠    →  🔴

Complejidad:   BoW < TF-IDF < Word2Vec < BERT
               💤  →  😴    →   😐    →  🤔

Velocidad:     BERT < Word2Vec < TF-IDF < BoW
               🐢  →   🦌    →   🐇   →  ⚡⚡⚡

¿CUÁNDO USAR CADA UNA?
======================

BoW:
  • Cuando tienes pocos datos
  • Cuando necesitas VELOCIDAD
  • Análisis rápido de textos
  • No necesitas precisión extrema

TF-IDF:
  • Búsqueda de documentos (Google)
  • Clasificación de textos simple
  • Recomendaciones
  • Standard en muchas empresas

Word2Vec:
  • Análisis de similitud
  • Detección de analogías
  • Input para redes neuronales
  • Cuando necesitas significado pero rapidez

BERT:
  • Clasificación de textos avanzada
  • Análisis de sentimientos precisos
  • Respuestas a preguntas (Q&A)
  • Traducción automática
  • Cualquier tarea NLP moderna


CONEXIÓN CON TUS CLASES
=======================

En la clase 17 (Tokenización):
  ✓ Aprendiste CÓMO dividir texto en tokens
  ✓ Aprendiste QUE cada token = número
  ✓ IMPORTANTE para entender BoW

En la clase 18 (Lenguaje Natural e Introducción a Embeddings):
  ✓ Viste vectores y cómo se relacionan
  ✓ Aprendiste Bag of Words, TF-IDF, Word2Vec, BERT
  ✓ Entendiste POR QUÉ se usan embeddings

En la clase 19 (Lenguaje Natural):
  ✓ Viste más sobre embeddings contextuales
  ✓ Entendiste las limitaciones de diccionarios
  ✓ Viste por qué BERT es superior


PRÓXIMOS PASOS EN TU CURSO
==========================

1. Domina estas 4 técnicas (estás aquí 📍)
2. Aprenderás sobre Transformers (arquitectura de BERT)
3. Aprenderás Fine-tuning (adaptar BERT a tus problemas)
4. Aplicarás esto al PROYECTO FINAL


¡EMPECEMOS!
===========
""")


def main():
    """
    Función principal que muestra el menú y ejecuta las opciones
    """
    
    # Mostrar introducción al iniciar
    print(__doc__)
    
    while True:
        opciones = mostrar_menu()
        
        seleccion = input("\n🎯 Elige una opción (0-5): ").strip()
        
        if seleccion not in opciones:
            print("\n❌ Opción no válida. Intenta de nuevo.")
            continue
        
        nombre, archivo = opciones[seleccion]
        
        if seleccion == '0':
            print("\n👋 ¡Gracias por practicar NLP! Sigue estudiando 📚")
            break
        
        elif seleccion == '5':
            mostrar_explicacion_general()
            input("\n📌 Presiona Enter para volver al menú...")
        
        else:
            ejecutar_tecnica(archivo)
            input("\n📌 Presiona Enter para volver al menú...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("\nAsegúrate de tener instaladas las dependencias:")
        print("pip install scikit-learn pandas gensim transformers torch")

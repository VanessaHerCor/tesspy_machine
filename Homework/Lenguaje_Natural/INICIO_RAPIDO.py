"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    GUÍA RÁPIDA DE INICIO (QUICK START)                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

SI QUIERES EMPEZAR RÁPIDAMENTE, SIGUE ESTOS PASOS:
==================================================

1. INSTALAR DEPENDENCIAS
─────────────────────────
Abre una terminal (PowerShell en Windows) y ejecuta:

    pip install -r requirements.txt

⏱️  Tiempo: 2-5 minutos (depende de tu internet)
✓ Esto instalará: pandas, scikit-learn, gensim, transformers, torch

Una sola vez. Después no lo necesitas hacer más.


2. EJECUTAR EL PROGRAMA
───────────────────────
En la misma carpeta (Lenguaje_Natural), escribe:

    python main.py

✓ Te mostrará un menú interactivo
✓ Elige qué técnica quieres practicar
✓ El código se ejecutará y te mostrará ejemplos


3. ENTENDER LO QUE VES
──────────────────────
Cada ejecución te mostrará:

    📚 CORPUS: Los textos que se analizan
    🔨 PROCESAMIENTO: Lo que está ocurriendo
    📊 RESULTADOS: La salida en forma de tabla o números
    💡 EXPLICACIÓN: Qué significa cada resultado


¿CUÁL ES EL MEJOR ORDEN?
========================

1️⃣  Bag of Words       (1_bag_of_words.py)
   └─ Empieza aquí. Es lo más simple.
   └─ Duración: ~5 minutos

2️⃣  TF-IDF             (2_tfidf.py)
   └─ Segunda técnica. Mejora de BoW.
   └─ Duración: ~5 minutos

3️⃣  Word2Vec           (3_word2vec.py)
   └─ Salto conceptual importante.
   └─ Duración: ~10 minutos
   └─ Aquí ves analogías mágicas

4️⃣  BERT              (4_bert.py)
   └─ Lo más avanzado. Prepárate para esperar.
   └─ Duración: ~20 minutos (primera vez descarga modelo)
   └─ Después de lo más rápido


EJECUTAR CADA UNA POR SEPARADO
==============================

Si quieres saltar el menú:

# Bag of Words
python tecnicas/1_bag_of_words.py

# TF-IDF
python tecnicas/2_tfidf.py

# Word2Vec
python tecnicas/3_word2vec.py

# BERT
python tecnicas/4_bert.py


PROBLEMAS COMUNES
=================

❌ "No se encuentra python"
✓ Asegúrate de tener Python instalado
✓ En terminal: python --version

❌ "No se encuentra el módulo scikit-learn"
✓ No instalaste las dependencias
✓ Ejecuta: pip install -r requirements.txt

❌ "BERT se queda pegado/lento"
✓ Es NORMAL en la primera ejecución
✓ Está descargando un modelo (~500MB)
✓ Ten paciencia ☕
✓ Después será más rápido

❌ "Error al descargar modelo de BERT"
✓ Problema de conexión a internet
✓ Intenta de nuevo
✓ O usa otro ejecutor de código (Colab)


CONSEJOS MIENTRAS PRACTICAS
===========================

✓ LEE EL CÓDIGO: Está súper comentado para ti
✓ MODIFICA EJEMPLOS: Cambia los textos y ve qué pasa
✓ EXPERIMENTA: Agrega nuevas frases
✓ ENTIENDE: No solo copies/pegues, aprende
✓ PACIENCIA: BERT es complejo pero vale la pena


PRÓXIMOS PASOS DESPUÉS DE DOMINAR ESTO
======================================

1. Aprenderás sobre Transformers (arquitectura)
2. Aprenderás Fine-tuning (adaptar modelos a tus datos)
3. Crearás chatbots con librerías como LangChain
4. Harás tu PROYECTO FINAL usando todo esto


REFERENCIA RÁPIDA DE TÉCNICAS
=============================

BoW:       Cuenta palabras
TF-IDF:    Pondera palabras por importancia
Word2Vec:  Aprende significado de palabras
BERT:      Entiende contexto (¡la estrella!)


DOCUMENTACIÓN
=============

📖 README.md         ← Guía completa (lee esto después)
📄 requirements.txt  ← Lista de dependencias
🐍 main.py          ← Menú principal
📁 tecnicas/        ← Carpeta con cada técnica


¿LISTA PARA EMPEZAR?
====================

¡Sí! Entonces:

1. Abre una terminal
2. Ve a esta carpeta (cd Lenguaje_Natural)
3. Ejecuta: pip install -r requirements.txt
4. Ejecuta: python main.py
5. ¡Aprende! 📚


TIEMPO ESTIMADO TOTAL
====================

Instalación:        5 minutos
BoW:               5 minutos
TF-IDF:            5 minutos
Word2Vec:          10 minutos
BERT:              20 minutos (+ descargas)
                  ──────────────
TOTAL:            ~45 minutos

¡Menos de una hora para dominar 4 técnicas NLP fundamentales! 🚀


RECURSOS ADICIONALES
====================

Si quieres aprender más:
- Documentación de scikit-learn: https://scikit-learn.org/
- Word2Vec en Gensim: https://radimrehurek.com/gensim/
- BERT explicado: https://huggingface.co/

Pero primero, ¡domina lo que tienes aquí! 😊


¿PREGUNTAS?
===========

Revisa el README.md (tiene una sección de Q&A)

---

¡BIENVENIDO AL MUNDO DEL NLP! 🎓✨

Haz que cuente,
tu profesor de Python IV
"""

print(__doc__)

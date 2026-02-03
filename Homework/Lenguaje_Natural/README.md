# 📚 Lenguaje Natural - Práctica Educativa

Proyecto educativo para aprender **Procesamiento del Lenguaje Natural (NLP)** basado en las clases de Python IV.

## 📁 Estructura del Proyecto

```
Lenguaje_Natural/
├── main.py                          ← EMPIEZA AQUÍ (menú principal)
├── README.md                        ← Este archivo
│
└── tecnicas/
    ├── 1_bag_of_words.py           ← Bag of Words (lo más simple)
    ├── 2_tfidf.py                  ← TF-IDF (mejora de BoW)
    ├── 3_word2vec.py               ← Word2Vec (embeddings)
    └── 4_bert.py                   ← BERT (lo más avanzado) ⭐
```

## 🚀 Cómo Empezar

### Opción 1: Ejecutar el Menú Interactivo (Recomendado)

```bash
python main.py
```

Te permitirá elegir qué técnica practicar.

### Opción 2: Ejecutar Técnicas Individuales

```bash
# Bag of Words
python tecnicas/1_bag_of_words.py

# TF-IDF
python tecnicas/2_tfidf.py

# Word2Vec
python tecnicas/3_word2vec.py

# BERT
python tecnicas/4_bert.py
```

## 📦 Instalación de Dependencias

Necesitas instalar las librerías requeridas:

```bash
pip install scikit-learn pandas gensim transformers torch
```

Si tienes problemas, instala cada una por separado:

```bash
pip install scikit-learn
pip install pandas
pip install gensim
pip install transformers
pip install torch
```

## 🎓 ¿Qué vas a Aprender?

| Técnica | Concepto | Dificultad | Velocidad |
|---------|----------|-----------|-----------|
| **Bag of Words** | Conteo de palabras | 🟢 Fácil | ⚡⚡⚡ |
| **TF-IDF** | Ponderación inteligente | 🟡 Medio | ⚡⚡ |
| **Word2Vec** | Embeddings con significado | 🟠 Difícil | ⚡ |
| **BERT** | Contexto y profundidad | 🔴 Muy Difícil | 🐢 |

## 📖 Orden Recomendado de Estudio

**1️⃣ Bag of Words** (Comienza aquí)
   - Entiende lo más básico
   - Cómo contar palabras y crear vectores simples
   - ⏱️ 10 minutos

**2️⃣ TF-IDF** (Después)
   - Aprende a ponderar palabras
   - Entiende por qué "el" es menos importante que "pescado"
   - ⏱️ 15 minutos

**3️⃣ Word2Vec** (Nivel intermedio)
   - Descubre embeddings reales
   - Ve cómo "rey" y "reina" son vectores similares
   - Aprende sobre análogas matemáticas
   - ⏱️ 20 minutos

**4️⃣ BERT** (Nivel avanzado)
   - La culminación: contexto verdadero
   - Entiende cómo la misma palabra tiene significados diferentes
   - ⏱️ 25 minutos (+ descarga de modelo primera vez)

**Total: ~1 hora** de aprendizaje interactivo

## 💡 Consejos para Aprender

### ✅ HAZ ESTO

- 📖 **Lee el código comentado** - Cada sección tiene explicaciones
- ▶️ **Ejecuta el código** - Ver los resultados es importante
- 🧪 **Experimenta** - Modifica los textos de ejemplo y ve qué pasa
- 📝 **Toma notas** - Apunta lo que no entiendes
- 🔄 **Repite** - Vuelve a cada técnica cuando lo necesites

### ❌ NO HAGAS ESTO

- ⏭️ No saltes directamente a BERT (necesitas los fundamentos)
- 🚀 No intentes ir rápido - Aprende paso a paso
- 📱 No intentes hacer cosas complejas al inicio
- 🤔 No te desanimes si BERT es lento (es normal)

## 🔗 Conexión con Tus Clases

**Clase 17: Tokenización**
- Aprendiste CÓMO se dividen los textos en tokens
- Aprendiste QUE cada token se convierte a un número
- Aquí practicas CÓMO esos números se usan en técnicas

**Clase 18: Lenguaje Natural e Introducción a Embeddings**
- Viste vectores y cómo se relacionan
- Aprendiste sobre BoW, TF-IDF, Word2Vec, BERT
- Aquí VES EN ACCIÓN todas esas técnicas

**Clase 19: Lenguaje Natural**
- Aprendiste sobre los problemas de los diccionarios
- Viste por qué BERT es superior
- Aquí COMPRENDES por qué funcionan los embeddings

## ⚠️ Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'sklearn'"

**Solución:**
```bash
pip install scikit-learn
```

### Error: "ModuleNotFoundError: No module named 'gensim'"

**Solución:**
```bash
pip install gensim
```

### Error: "ModuleNotFoundError: No module named 'transformers'"

**Solución:**
```bash
pip install transformers torch
```

### BERT es muy lento / se queda "pegado"

**Esto es NORMAL en la primera ejecución:**
- Está descargando un modelo (~500MB)
- Depende de tu velocidad de internet
- Después será más rápido
- Ten paciencia ☕

## 🎯 Checklist de Aprendizaje

- [ ] Ejecuté main.py y vi el menú
- [ ] Entendí BoW (frecuencias de palabras)
- [ ] Entendí TF-IDF (ponderación)
- [ ] Entendí Word2Vec (embeddings y analogías)
- [ ] Entendí BERT (contexto y múltiples significados)
- [ ] Ejecuté cada técnica y leí su código
- [ ] Modifiqué los ejemplos y ví diferentes resultados
- [ ] Entendí POR QUÉ cada técnica es mejor que la anterior

## 📚 Material Adicional

Estos códigos están basados en:
- Tutoría PYTHON IV 17: Tokenización
- Tutoría PYTHON IV 18: Lenguaje Natural e Introducción a Embeddings
- Tutoría PYTHON IV 19: Lenguaje Natural

## 🚀 Próximos Pasos

Una vez hayas dominado esto:
1. Aprenderás sobre **Transformers** (arquitectura de BERT)
2. Aprenderás **Fine-tuning** (adaptar modelos)
3. Aprenderás **Arquitecturas modernas** (GPT, etc.)
4. Aplicarás todo al **PROYECTO FINAL**

## 💬 Dudas Frecuentes

**P: ¿Por qué cada técnica es un archivo separado?**
R: Para que puedas enfocarte en UNA técnica a la vez sin distracciones.

**P: ¿Puedo modificar los ejemplos?**
R: ¡SÍ! Recomendado. Cambia los textos y ve qué pasa.

**P: ¿Necesito instalar CUDA para BERT?**
R: No, funcionará en CPU (lento pero funciona). CUDA (GPU) es opcional para más velocidad.

**P: ¿Qué es "contextual" en BERT?**
R: La misma palabra tiene vectores DIFERENTES según el contexto. "banco" (dinero) ≠ "banco" (asiento).

## ✅ Validación

Sabrás que entendiste cuando puedas:
- ✓ Explicar qué hace cada técnica
- ✓ Saber cuándo usar cada una
- ✓ Entender por qué BERT es mejor (pero lento)
- ✓ Modificar ejemplos y predecir resultados

## 📞 Soporte

Si algo no funciona:
1. Verifica que instalaste todas las dependencias
2. Lee los comentarios en el código (están muy detallados)
3. Revisa el error exacto (ayuda mucho)
4. Pregunta a tu profesor

---

**Versión:** 1.0
**Creado para:** Estudiante de Python IV  
**Fecha:** Febrero 2026

¡**¡Bienvenido al maravilloso mundo del NLP!** 🎓✨

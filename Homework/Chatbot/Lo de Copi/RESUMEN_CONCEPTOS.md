# 📚 GUÍA RÁPIDA - CONCEPTOS CLAVE RESUMIDOS

## 🎯 EN UNA SOLA PÁGINA

### Clases 18-19: De Palabras a Números

#### Problema Base:
```
Las máquinas NO entienden palabras.
Solo entienden NÚMEROS (vectores).
```

#### Solución Paso a Paso:

**1. Bag of Words (BoW) - SIMPLE pero MALO**
```
"el perro come"  → [el: 1, perro: 1, come: 1]
"el gato come"   → [el: 1, gato: 1, come: 1]

Problema: "el" aparece en ambos = son iguales?
NO! Pero BoW dice que sí.
```

**2. TF-IDF - MEJOR**
```
TF-IDF = Term Frequency × Inverse Document Frequency
       = Qué tan frecuente × Qué tan RARA

Si una palabra está EN TODOS LOS DOCUMENTOS → IDF baja = menos importante
Si está en POCOS documentos → IDF alta = MÁS importante

Resultado: "el" recibe peso bajo ✓
          "perro" recibe peso alto ✓
```

#### 3. Embeddings - LA REVOLUCIÓN

```
ANTES (Word2Vec):
- "banco" (dinero) → vector [0.2, -0.5, 0.8]
- "banco" (parque) → vector [0.2, -0.5, 0.8]  (MISMO!)
Problema: No diferencia contexto

AHORA (BERT):
- "Voy al banco a sacar dinero"      → [0.2, -0.5, 0.8, ...]
- "Me senté en el banco del parque" → [0.1, 0.3, -0.2, ...]  (DIFERENTE!)
Ventaja: Entiende contexto
```

#### Cómo Aprende:

```
Corpus (datos de entrenamiento):
"Rey es un guerrero honesto"
"Reina era hermosa y fundamental"
"Mujeres son como flores hermosas"

El modelo:
1. Ve "reina" y "hermosa" juntos
2. Ve "mujeres" y "hermosa" juntos
3. Conclusión: "reina" ≈ "mujer"

SIN DICCIONARIO, solo por CONTEXTO
```

#### Analogía Famosa:

```
Rey - Hombre + Mujer ≈ ?

Vector(Rey)           (0.5,  0.3, -0.2, ...)
- Vector(Hombre)    - (0.4,  0.2, -0.1, ...)
+ Vector(Mujer)     + (0.1,  0.4,  0.5, ...)
_________________________________
= Vector Resultante  (0.2,  0.5,  0.4, ...)

Busca el vector MÁS CERCANO → Reina ✓
```

---

### Clase 22: El Chatbot Explicado

#### ¿QUÉ HACE?

```
Tu PDFs + Mi Pregunta + IA = RESPUESTA INTELIGENTE
```

#### Paso a Paso:

**1. INGESTA (Setup inicial - 1 sesión)**
```python
# Cargar PDFs
documentos = cargar_pdfs()
# Resultado: ["La planta tiene...", "El agua es...", ...]
```

**2. VECTORIZACIÓN (Convertir a números - 1 sesión)**
```python
# Convertir cada párrafo a vector
embedding = modelo_embedding("La planta tiene raíces")
# Resultado: [0.2, -0.5, 0.8, ..., 0.1]  (768 números)
```

**3. ALMACENAMIENTO (BD vectorial - 1 sesión)**
```python
# Guardar todos los vectores
vector_db.guardar(embeddings)
# Resultado: BD lista para búsquedas rápidas
```

**4. CUANDO EL USUARIO PREGUNTA (Durante uso)**
```python
pregunta = "¿Cómo cuido una planta?"
# a) Convertir pregunta a vector
pregunta_vector = embedding(pregunta)  # [0.1, -0.4, 0.7, ...]

# b) Buscar párrafos SIMILARES en BD
similares = vector_db.buscar(pregunta_vector, top_k=3)
# Resultado: Los 3 párrafos más relevantes

# c) Mandar a GPT con contexto
respuesta = gpt(pregunta, contexto=similares)
# Resultado: "Para cuidar una planta debes..."
```

#### Arquitectura Visual:

```
┌──────────────────────────────────┐
│        TUS 3+ PDFs               │
├──────────────────────────────────┤
│  Documento 1: "Las plantas..."   │
│  Documento 2: "El jardín..."     │
│  Documento 3: "Técnicas de..."   │
└──────────┬───────────────────────┘
           │ CARGAR & DIVIDIR
           ↓
┌──────────────────────────────────┐
│      CHUNKS (párrafos)           │
├──────────────────────────────────┤
│ ["La planta tiene...", "El agua...", ...]
└──────────┬───────────────────────┘
           │ VECTORIZAR
           ↓
┌──────────────────────────────────┐
│    VECTOR DATABASE (FAISS)       │
├──────────────────────────────────┤
│ Almacena todos los embeddings    │
│ Búsqueda ultrrápida (similitud)  │
└──────────┬───────────────────────┘
           │
           ← USUARIO PREGUNTA →
           │
           ↓ VECTORIZAR PREGUNTA
           │
           ↓ BUSCAR TOP 3 SIMILARES
           │
┌──────────┴───────────────────────┐
│     PIPELINE GENERACIÓN          │
├──────────────────────────────────┤
│ GPT + Contexto Relevante → RESPUESTA
└──────────────────────────────────┘
```

---

## 🔧 TECHNOLOGIES

| Componente | Librería | Función |
|-----------|----------|---------|
| **Carga PDFs** | langchain-community | Lee y extrae texto |
| **Embeddings** | sentence-transformers | Convierte texto a vectores |
| **Vector DB** | FAISS | Almacena y busca vectores |
| **LLM** | OpenAI / Hugging Face | Genera respuestas |
| **Framework** | LangChain | Orquesta todo |
| **Interfaz** | Streamlit | Interfaz web |

---

## 📊 COMPARATIVA: SIMPLE vs AVANZADO

| Aspecto | Bag of Words | TF-IDF | Embeddings | BERT |
|--------|-------------|--------|-----------|------|
| **Contexto** | ❌ No | ❌ No | ⚠️ Parcial | ✅ Sí |
| **Precision** | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⚡⚡⚡ | ⚡⚡ | ⚡ | ⚡ |
| **Complejidad** | Simple | Media | Alta | Muy Alta |
| **Usado en** | Spam filter | Google (pasado) | Similitud | GPT, Chatbot |

---

## 💻 CÓDIGO MÍNIMO VIABLE

```python
# 1. CARGAR PDFs
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("archivo.pdf")
docs = loader.load()  # Listo, tienes el texto!

# 2. CREAR EMBEDDINGS
from langchain.embeddings import HuggingFaceEmbeddings
embed = HuggingFaceEmbeddings()
vectores = [embed.embed_query(doc.page_content) for doc in docs]

# 3. GUARDAR EN BD VECTORIAL
from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs, embed)

# 4. BUSCAR
resultados = db.similarity_search("¿Cómo cuido plantas?", k=3)

# 5. GENERAR RESPUESTA
from langchain.llms import OpenAI
llm = OpenAI(api_key="...")
respuesta = llm("Dado este contexto: " + resultados + "Responde: ¿Cómo cuido plantas?")
print(respuesta)
```

**¡ESO ES! Con 15 líneas tienes un chatbot funcional.**

---

## ✅ CHECKLIST RÁPIDA

Antes de comenzar:
- [ ] Tengo 3+ PDFs del mismo tema
- [ ] Todos en MISMO IDIOMA
- [ ] Entiendo qué es un embedding
- [ ] Sé por qué BERT > Word2Vec
- [ ] Conozco LangChain básico

Listo? ¡A PROGRAMAR! 🚀

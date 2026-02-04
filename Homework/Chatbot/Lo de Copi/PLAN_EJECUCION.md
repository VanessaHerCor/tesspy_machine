# 🎯 PLAN DE EJECUCIÓN - PROYECTO CHATBOT

## RESUMEN EJECUTIVO DE LAS CLASES

### Clases 18-19: Lenguaje Natural (Viernes 30 enero)
**Concepto clave:** Cómo convertir PALABRAS en NÚMEROS que las máquinas entienden

#### 1️⃣ **Representación de Texto:**
- **Problema:** Las máquinas NO entienden palabras, solo números
- **Solución 1 - Bag of Words (BoW):** Contar frecuencia de palabras
  - ❌ No funciona bien: trata todas las palabras igual
  - Ejemplo: "el" aparece 10 veces = importante? NO
  
- **Solución 2 - TF-IDF:** 
  - ✅ Mejor: da peso a palabras RARAS y IMPORTANTES
  - TF = Qué tan frecuente en UN documento
  - IDF = Qué tan RARA es en TODOS los documentos
  - Fórmula: TF-IDF = TF × IDF

#### 2️⃣ **Embeddings - La Revolución:**
Los vectores (listas de números) que representan palabras

| Modelo | Características | Problema |
|--------|-----------------|----------|
| **Word2Vec** | UN vector por palabra | No entiende contexto |
| **FastText** | Resiste palabras desconocidas | Menos preciso |
| **BERT** ⭐ | Vectores DIFERENTES por contexto | Antes no existía |

**Ejemplo BERT:**
```
Texto 1: "Voy al banco a sacar dinero"      → banco = vector A
Texto 2: "Me senté en el banco del parque"  → banco = vector B (DIFERENTE!)
```

#### 3️⃣ **Cómo Aprende el Modelo:**
- NO memoriza un diccionario
- Aprende viendo CONTEXTO:
  - Si "reina" aparece con "hermosa"
  - Y "mujer" también aparece con "hermosa"
  - → El modelo aprende que "reina" y "mujer" están relacionadas

**Analogía famosa:**
```
Rey - Hombre + Mujer ≈ Reina
(resta vectores, suma, busca el más cercano)
```

---

### Clase 22: Chatbot con LangChain (Lunes 2 febrero)

#### 🎓 LO QUE NECESITAS SABER:

**1. Qué es un Chatbot con IA:**
- Lee TUS DOCUMENTOS (PDFs)
- Entiende lo que preguntas (embeddings)
- Busca respuestas EN TUS DOCUMENTOS (RAG)
- Genera respuestas con GPT

**2. Arquitectura:**
```
TUS PDFs → [DIVIDIDOS EN CHUNKS] 
         → [CONVERTIDOS A EMBEDDINGS]
         → [GUARDADOS EN BD VECTORIAL]
         ↓
PREGUNTA DEL USUARIO
         ↓
[BUSCAR CHUNKS SIMILARES]
         ↓
[MANDARLE A GPT CON CONTEXTO]
         ↓
RESPUESTA COHERENTE
```

**3. Proyecto Final - Opciones:**
- ✅ **Opción A:** Chatbot entrenado con 3+ PDFs (RECOMENDADO)
- ✅ **Opción B:** Otro proyecto (visión, ML, etc.)

**4. Requisitos técnicos:**
- 3 PDFs mínimo, ~20 páginas cada uno
- **MISMO IDIOMA EN TODOS** (no mezcles español con inglés)
- Cualquier tema: libros, documentos, manuales

**5. Framework: LangChain**
- Maneja embeddings automáticamente
- Conecta con APIs de OpenAI, Hugging Face, etc.
- Gestiona memoria y contexto
- MUY fácil de usar (2-3 líneas de código para cada cosa)

**6. Despliegue:**
- NO Discord (eso fue otra clase)
- Será WEB con **Streamlit** (interfaz visual simple)

---

## ⚙️ PASOS ESPECÍFICOS PARA COMENZAR

### PASO 1: Preparar los datos
```
📁 Homework/Chatbot/
├── pdfs/                 ← AQUÍ VAN TUS PDFs
│   ├── documento1.pdf
│   ├── documento2.pdf
│   └── documento3.pdf
├── app.py               ← Código principal
├── requirements.txt     ← Librerías necesarias
└── .env                 ← Variables (API keys)
```

**📝 TODO:**
- [ ] Recopila 3+ PDFs de un tema que te interese
- [ ] Ponlos en `pdfs/`
- [ ] Asegúrate que estén en MISMO IDIOMA

### PASO 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

**Librerías necesarias:**
```
langchain==0.2.16
langchain-community==0.2.17
langchain-text-splitters==0.2.4
sentence-transformers
faiss-cpu
streamlit
python-dotenv
```

### PASO 3: Estructura básica del código

**Fase 1 - Cargar PDFs:** (1 sesión)
```python
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("pdfs/documento.pdf")
documents = loader.load()
```

**Fase 2 - Crear embeddings:** (1 sesión)
```python
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="...")
```

**Fase 3 - Vector database:** (1 sesión)
```python
from langchain.vectorstores import FAISS
vector_store = FAISS.from_documents(documents, embeddings)
```

**Fase 4 - Conectar con LLM:** (1 sesión)
```python
from langchain.llms import OpenAI
llm = OpenAI(api_key="tu_key")
```

**Fase 5 - Interfaz Streamlit:** (2-3 sesiones)
```python
import streamlit as st
st.title("Mi Chatbot Inteligente")
# ... tu código aquí
```

---

## 📋 CHECKLIST - QUÉ HACER AHORA MISMO

### Hoy mismo:
- [ ] Decide qué tema para tu chatbot
- [ ] Busca 3-5 PDFs de ese tema
- [ ] Crea carpeta `pdfs/` en `Homework/Chatbot/`
- [ ] Coloca los PDFs ahí

### Esta semana (Sesión 1):
- [ ] Instala LangChain
- [ ] Aprende a cargar PDFs
- [ ] Extrae el texto de los PDFs

### Próximas 2 sesiones:
- [ ] Crea embeddings
- [ ] Configura vector database (FAISS)
- [ ] Prueba búsqueda de documentos similares

### Sesión 4:
- [ ] Integra OpenAI API (o modelo local)
- [ ] Crea el pipeline completo

### Sesiones 5-7:
- [ ] Mejoras: historial de chat, parámetros, interfaz
- [ ] Despliegue con Streamlit
- [ ] Pruebas exhaustivas

---

## 💡 CONSEJOS DEL PROFE

1. **Tiempo:** Tienes SUFICIENTE. El chatbot básico se hace en 3-4 sesiones
2. **Complejidad:** El profe maneja la mayoría automáticamente con LangChain
3. **Errores:** Esperados. Son la mejor forma de aprender
4. **Documentos:** Entre más datos, mejor. Calidad > cantidad
5. **No temas:** Esto es 90% automático con LangChain, 10% código

---

## 📚 REFERENCIAS

- **Paper revolucionario:** "Attention Is All You Need" (Google, 2017)
- **Arquitectura:** Transformers (base de GPT)
- **Técnicas vistas:**
  - Vectorización
  - Word2Vec, FastText, BERT
  - Attention mechanisms
  - RAG (Retrieval-Augmented Generation)

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Necesito API key de OpenAI?**
R: Para GPT sí. Para pruebas, puedes usar modelos locales gratis.

**P: ¿Los PDFs pueden ser en inglés?**
R: Sí, pero que TODOS estén en el mismo idioma. No mezcles.

**P: ¿Qué pasa si uso PDFs de baja calidad?**
R: El chatbot será mediocre. GIGO (Garbage In, Garbage Out).

**P: ¿Puedo usar Word, Excel, etc?**
R: El profe enfatizó PDFs. Para otros formatos, necesitas convertirlos.

**P: ¿Cuánto tarda entrenar?**
R: Con LangChain, NO "entrenas". Solo creas embeddings (segundos-minutos).

---

## 🎬 PRÓXIMOS PASOS

1. Abre esta carpeta en VS Code
2. Crea el archivo `requirements.txt`
3. Crea el archivo `app.py` (vacío por ahora)
4. Empieza a reunir PDFs
5. ¡Avísale al profe si tienes dudas!

¡Adelante! Este proyecto va a quedar BACANO 🚀

# 🎯 PRIMEROS PASOS - GUÍA PASO A PASO

## AHORA MISMO - Los próximos 10 minutos

### Paso 1: Verifica la estructura
Tu carpeta `Homework/Chatbot/` debe tener:
```
✅ app.py                  (código principal)
✅ requirements.txt        (librerías necesarias)
✅ README.md               (descripción del proyecto)
✅ .env.example            (template de configuración)
✅ PLAN_EJECUCION.md       (plan detallado)
✅ RESUMEN_CONCEPTOS.md    (guía rápida de teoría)
✅ PRIMEROS_PASOS.md       (este archivo)
```

### Paso 2: Crea la carpeta de PDFs
```bash
# En tu terminal, dentro de Homework/Chatbot/
mkdir pdfs
```

### Paso 3: Copia el archivo de configuración
```bash
# En la carpeta Homework/Chatbot/
cp .env.example .env
```

### Paso 4: Abre VS Code aquí
```bash
# Desde la carpeta Homework/Chatbot/
code .
```

---

## SESIÓN 1: CARGAR PDFs (Esta semana)

### Objetivo
Que el código pueda leer tus PDFs correctamente

### Tareas

1. **Busca 3-5 PDFs** de un tema que te interese
   - Ejemplos: Un libro sobre Python, documentación, manual técnico
   - Pueden ser en español o inglés (pero todos IGUAL)
   - Deben ser legibles por máquina (no escaneados)

2. **Coloca los PDFs en `pdfs/`**
   ```
   Homework/Chatbot/
   └── pdfs/
       ├── documento1.pdf
       ├── documento2.pdf
       └── documento3.pdf
   ```

3. **Instala las librerías básicas**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prueba cargar los PDFs**
   - Abre `app.py`
   - Ejecuta solo la función `cargar_pdfs()`
   - Debería imprimir cuántas páginas cargó

   ```python
   # En la terminal de VS Code
   python -c "from app import cargar_pdfs; docs = cargar_pdfs()"
   ```

5. **Resultado esperado:**
   ```
   ========================================================================
   CHATBOT CON LANGCHAIN - ESTRUCTURA INICIAL
   ========================================================================
   
   📄 Cargando: pdfs/documento1.pdf
      ✅ 45 páginas cargadas
   📄 Cargando: pdfs/documento2.pdf
      ✅ 67 páginas cargadas
   📄 Cargando: pdfs/documento3.pdf
      ✅ 78 páginas cargadas
   ```

### ✅ Checklist Sesión 1
- [ ] Tengo 3+ PDFs en `pdfs/`
- [ ] PDFs están en el mismo idioma
- [ ] Instalé requirements.txt
- [ ] Ejecuté cargar_pdfs() exitosamente
- [ ] Aparece el mensaje "✅ X páginas cargadas"

---

## SESIÓN 2: CREAR EMBEDDINGS (Próxima semana)

### Objetivo
Convertir el texto en vectores (números) que la máquina entienda

### Tareas

1. **Modifica app.py para ejecutar Fase 2:**
   ```python
   if __name__ == "__main__":
       # Fase 1
       documentos = cargar_pdfs()
       
       # Fase 2 - NUEVA
       chunks = preparar_documentos(documentos)
       
       print(f"✅ Listo! Tienes {len(chunks)} chunks")
   ```

2. **Ejecuta:**
   ```bash
   python app.py
   ```

3. **Resultado esperado:**
   ```
   📄 Cargando: pdfs/documento1.pdf
      ✅ 45 páginas cargadas
   📚 Total de chunks creados: 234
   ✅ Listo! Tienes 234 chunks
   ```

### ¿Qué son los chunks?
Dividimos documentos grandes en párrafos pequeños para que el modelo pueda procesarlos mejor.

```
Documento (50 páginas)
    ↓ Dividir en chunks
Chunk 1: "La inteligencia artificial..."
Chunk 2: "Los modelos de IA usan..."
Chunk 3: "Los embeddings son..."
...
Chunk 234: "En conclusión, la IA..."
```

### ✅ Checklist Sesión 2
- [ ] Modifiqué app.py para incluir Fase 2
- [ ] Ejecuté `python app.py`
- [ ] Aparece "Total de chunks creados: X"
- [ ] El número X es > 100 (sino tus PDFs son muy pequeños)

---

## SESIÓN 3: VECTOR DATABASE (Semana 3)

### Objetivo
Crear una base de datos que permite búsquedas rápidas

### Tareas

1. **Actualiza app.py:**
   ```python
   if __name__ == "__main__":
       documentos = cargar_pdfs()
       chunks = preparar_documentos(documentos)
       
       # Fase 3 - NUEVA
       vector_db = crear_vector_database(chunks)
       
       # Prueba una búsqueda
       resultados = vector_db.similarity_search("tu pregunta", k=3)
       for r in resultados:
           print(r.page_content[:100])  # Primeros 100 caracteres
   ```

2. **Ejecuta:**
   ```bash
   python app.py
   ```

3. **Prueba preguntas diferentes:**
   - Cambia "tu pregunta" por cosas como:
     - "¿Qué es Python?"
     - "¿Cómo usar funciones?"
     - "Explica conceptos básicos"

### ¿Qué está pasando?
```
Tu pregunta: "¿Qué es Python?"
    ↓ Convertir a vector
Vector: [0.12, -0.45, 0.89, ..., 0.34]
    ↓ Buscar vectores similares en FAISS
Top 3 documentos más parecidos:
1. "Python es un lenguaje..." (similitud: 0.95)
2. "Características de Python..." (similitud: 0.88)
3. "Python se usa en..." (similitud: 0.82)
```

### ✅ Checklist Sesión 3
- [ ] Ejecuté Fase 3 sin errores
- [ ] Probé 3+ búsquedas diferentes
- [ ] Los resultados tienen sentido (relevancia)
- [ ] FAISS está respondiendo rápido

---

## SESIÓN 4: CONECTAR CON GPT (Semana 4)

### Objetivo
Usar OpenAI para generar respuestas inteligentes

### IMPORTANTE: Configura API Key

1. **Obtén tu API Key:**
   - Ve a https://platform.openai.com/api-keys
   - Crea una nueva key
   - Cópiala

2. **Configura en .env:**
   ```bash
   # En VS Code, abre el archivo .env
   # Cambia esto:
   OPENAI_API_KEY=tu_clave_aqui
   
   # A esto (pega tu clave):
   OPENAI_API_KEY=sk-abc123...
   ```

3. **Actualiza app.py:**
   ```python
   if __name__ == "__main__":
       documentos = cargar_pdfs()
       chunks = preparar_documentos(documentos)
       vector_db = crear_vector_database(chunks)
       
       # Fase 4 - NUEVA
       chatbot = crear_chatbot(vector_db)
       
       # Prueba
       if chatbot:
           respuesta = chatbot("¿Qué es Python?")
           print(respuesta)
   ```

4. **Ejecuta:**
   ```bash
   python app.py
   ```

### Resultado esperado:
```
🤖 Respuesta: "Python es un lenguaje de programación 
de alto nivel, interpretado y de propósito general. 
Se caracteriza por su sintaxis simple y legible, lo que 
lo hace ideal para principiantes..."

📚 Basado en:
  - pdfs/documento1.pdf
  - pdfs/documento2.pdf
```

### ✅ Checklist Sesión 4
- [ ] Obtuve API Key de OpenAI
- [ ] Configuré .env con mi key
- [ ] Ejecuté Fase 4 sin errores
- [ ] GPT generó respuestas coherentes
- [ ] Las respuestas están basadas en MIS PDFs

---

## SESIÓN 5+: INTERFAZ STREAMLIT (Semana 5+)

### Objetivo
Crear una interfaz bonita y profesional

### Tareas

1. **Instala Streamlit:**
   ```bash
   pip install streamlit streamlit-chat
   ```

2. **Crea un nuevo archivo `streamlit_app.py`:**
   ```python
   import streamlit as st
   from app import *
   
   st.set_page_config(page_title="Mi Chatbot", layout="wide")
   st.title("🤖 Mi Chatbot Inteligente")
   
   # Cargar datos
   docs = cargar_pdfs()
   chunks = preparar_documentos(docs)
   vector_db = crear_vector_database(chunks)
   chatbot = crear_chatbot(vector_db)
   
   # Interfaz
   if "messages" not in st.session_state:
       st.session_state.messages = []
   
   with st.form("chat_form"):
       user_input = st.text_input("Tu pregunta:")
       submitted = st.form_submit_button("Enviar")
   
   if submitted and user_input:
       resultado = chatbot(user_input)
       st.session_state.messages.append({
           "role": "user",
           "content": user_input
       })
       st.session_state.messages.append({
           "role": "bot",
           "content": resultado["result"]
       })
   
   for msg in st.session_state.messages:
       if msg["role"] == "user":
           st.write(f"**Tú:** {msg['content']}")
       else:
           st.write(f"**Bot:** {msg['content']}")
   ```

3. **Ejecuta:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Se abrirá en tu navegador:**
   - URL: `http://localhost:8501`
   - Interfaz hermosa y funcional
   - Chatbot completamente operativo

### ✅ Checklist Sesión 5+
- [ ] Instalé Streamlit
- [ ] Creé streamlit_app.py
- [ ] Ejecuté `streamlit run streamlit_app.py`
- [ ] Se abrió en navegador
- [ ] Puedo hacer preguntas y recibir respuestas
- [ ] El historial se mantiene

---

## 🎁 CÓDIGO MÍNIMO FUNCIONAL (Si quieres ir rápido)

Si no quieres hacer todo paso a paso, aquí está el mínimo:

```python
# minimal_chatbot.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
import glob

# 1. Cargar PDFs
pdfs = glob.glob("pdfs/*.pdf")
docs = []
for pdf in pdfs:
    docs.extend(PyPDFLoader(pdf).load())

# 2. Dividir
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

# 3. Embeddings
embed = HuggingFaceEmbeddings()
vector_db = FAISS.from_documents(chunks, embed)

# 4. LLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 5. Chatbot
chatbot = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(search_kwargs={"k": 3})
)

# 6. Usar
while True:
    pregunta = input("Pregunta: ")
    print(chatbot(pregunta)["result"])
```

**15 líneas = chatbot funcional**

---

## 📞 PROBLEMAS COMUNES

### "No se encontraron PDFs"
```
❌ pdf_files está vacío
✅ Solución: Crea carpeta pdfs/ y coloca archivos .pdf
```

### "ModuleNotFoundError: No module named 'langchain'"
```
❌ Librerías no instaladas
✅ Solución: pip install -r requirements.txt
```

### "API Key no válida"
```
❌ OPENAI_API_KEY incorrecta en .env
✅ Solución: Verifica que copiaste completa, sin espacios
```

### "Los PDFs son muy pequeños"
```
❌ Menos de 100 chunks
✅ Solución: Agrega más PDFs o más largos
```

---

## 🚀 ¡VAMOS!

Empieza por **Sesión 1** hoy mismo:
1. Busca 3 PDFs
2. Colócalos en `pdfs/`
3. Ejecuta `python app.py`

Si todo funciona → ¡Ya tienes el 25% del proyecto! 🎉

Cualquier duda pregunta al profe. ¡Adelante! 💪

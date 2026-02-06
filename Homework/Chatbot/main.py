# INSTALAR ANTES
# pip install -U "numpy>=2" "tenacity>=9,<10"
# pip install torch langchain langchain-community langchain-text-splitters transformers sentence-transformers faiss-cpu langchain-huggingface
# pip install pypdf


# ============================================
# CHATBOT CON IA USANDO LANGCHAIN Y HUGGINGFACE
# ============================================
# Este script implementa un chatbot que responde preguntas
# basado en documentos PDF locales usando un modelo de IA

import os
import glob
import torch
from pathlib import Path

# ============= IMPORTACIONES NECESARIAS =============

# Herramientas para cargar y procesar PDFs
from langchain_community.document_loaders import PyPDFLoader

# Herramientas para dividir documentos en fragmentos pequeños
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Herramientas para crear representaciones vectoriales (embeddings) del texto
from langchain_community.embeddings import HuggingFaceEmbeddings

# FAISS es una librería para búsqueda rápida de vectores similares
from langchain_community.vectorstores import FAISS

# Pipeline para usar modelos de IA localmente
from langchain_huggingface import HuggingFacePipeline

# Modelos y tokenizadores de Hugging Face
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


# ============= PASO 0: CONFIGURAR RUTAS Y CARPETAS =============

# Definir la carpeta donde están los PDFs (LOCAL, no en Colab)
pdf_folder_path = Path(__file__).parent / "PDF_PSY"

# Carpeta donde se guardarán los embeddings (para reutilizarlos)
embedding_folder_path = Path(__file__).parent / "embedding_storage"

print("=" * 60)
print("PASO 0: VERIFICANDO CARPETAS")
print("=" * 60)
print(f"📂 Carpeta de PDFs: {pdf_folder_path}")
print(f"📂 Carpeta de embeddings: {embedding_folder_path}")

# Crear la carpeta de embeddings si no existe
if not os.path.exists(embedding_folder_path):
    os.makedirs(embedding_folder_path)
    print(f"✅ Carpeta de embeddings creada")


# ============= PASO 1: VERIFICAR CARPETA DE PDFS =============

print("\n" + "=" * 60)
print("PASO 1: VERIFICANDO CARPETA DE PDFS")
print("=" * 60)
print(f"Buscando PDFs en: {pdf_folder_path}")

# Verificar si la carpeta existe
if not os.path.exists(pdf_folder_path):
    print(f"❌ Error: La carpeta {pdf_folder_path} no existe")
    print("Por favor, asegúrate de que tus PDFs estén en: Homework/Chatbot/PDF_PSY")
    exit()

# Buscar todos los archivos PDF en la carpeta
pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")

if not pdf_files:
    print(f"⚠️  No se encontraron PDFs en {pdf_folder_path}")
else:
    print(f"✅ Se encontraron {len(pdf_files)} PDF(s):")
    for pdf in pdf_files:
        print(f"   - {os.path.basename(pdf)}")


# ============= PASO 2 Y 3: CARGAR Y PROCESAR PDFS O CARGAR EMBEDDINGS =============

print("\n" + "=" * 60)
print("PASO 2-3: PROCESANDO DOCUMENTOS")
print("=" * 60)

# Verificar si ya existen embeddings guardados
if os.path.exists(embedding_folder_path / "index.faiss"):
    print("⚡ Se detectaron embeddings guardados previamente")
    print("🔄 Cargando embeddings desde caché (MUCHO MÁS RÁPIDO)...")
    
    # Cargar el modelo de embeddings
    embeddings_local = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    
    # Cargar la base de datos de vectores guardada
    vectorstore = FAISS.load_local(
        str(embedding_folder_path),
        embeddings_local,
        allow_dangerous_deserialization=True
    )
    print("✅ Embeddings cargados desde caché (¡sin regenerar!)")
    
else:
    # Si no existen embeddings, generarlos
    print("📝 Generando embeddings por primera vez (esto toma tiempo)...")
    print("   Las próximas ejecuciones serán MUCHO más rápidas 🚀\n")
    
    # ---- CARGAR PDFS ----
    print("📄 Cargando PDFs...")
    all_pages = []
    
    for pdf_file in pdf_files:
        print(f"   - {os.path.basename(pdf_file)}", end=" ")
        
        try:
            loader = PyPDFLoader(pdf_file)
            pages = loader.load()
            all_pages.extend(pages)
            print(f"✅ ({len(pages)} páginas)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Total de páginas cargadas: {len(all_pages)}")
    
    # ---- DIVIDIR EN FRAGMENTOS ----
    print("\n📊 Dividiendo documentos en fragmentos...")
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )
    docs = text_split.split_documents(all_pages)
    print(f"✅ {len(docs)} fragmentos creados")
    
    # ---- CREAR EMBEDDINGS ----
    print("\n🔢 Generando vectores (embeddings)...")
    print("   Modelo: sentence-transformers/all-MiniLM-L6-v2")
    
    embeddings_local = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    
    vectorstore = FAISS.from_documents(docs, embeddings_local)
    
    # ---- GUARDAR EMBEDDINGS PARA LA PRÓXIMA VEZ ----
    print("\n💾 Guardando embeddings en caché...")
    vectorstore.save_local(str(embedding_folder_path))
    print(f"✅ Embeddings guardados en: {embedding_folder_path}")
    print("   ⚡ La próxima ejecución será INSTANTÁNEA")


# ============= PASO 4: CREAR EL RETRIEVER =============

print("\n" + "=" * 60)
print("PASO 4: CONFIGURANDO RETRIEVER")
print("=" * 60)
print("""
¿Qué es el retriever?
- Busca los documentos más relevantes para cada pregunta
- Usa los vectores para encontrar información relacionada
""")

# Configurar el recuperador
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
print("✅ Retriever listo")

# Probar el retriever
print("\n🧪 Prueba del retriever:")
pregunta_prueba = "¿Qué es la depresión?"
docs_relevantes = retriever.invoke(pregunta_prueba)
print(f"   Pregunta: '{pregunta_prueba}'")
print(f"   ✅ Se encontraron {len(docs_relevantes)} documentos relevantes")


# ============= PASO 5: CARGAR EL MODELO DE LENGUAJE =============

print("\n" + "=" * 60)
print("PASO 5: CARGANDO MODELO DE LENGUAJE (LLM)")
print("=" * 60)
print("""
Modelo: Qwen/Qwen3-0.6B
- Ligero: Solo 0.6 mil millones de parámetros
- Rápido: Funciona bien en CPU
- Eficiente: Bajo consumo de memoria
""")

model_id = 'Qwen/Qwen3-0.6B'
print(f"⏳ Cargando {model_id}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print("✅ Tokenizador cargado")
    
    # Cargar el modelo sin device_map (funciona mejor en CPU)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        dtype=torch.float16
    )
    print("✅ Modelo cargado")
    
    # Configurar el pipeline con parámetros para evitar repeticiones
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,          # Limitar a 256 tokens para respuestas concisas
        do_sample=True,              # Usar sampling para respuestas variadas
        temperature=0.7,             # Temperatura (0.7 = balance entre creatividad y coherencia)
        top_p=0.9,                   # Nucleus sampling
        repetition_penalty=1.2,      # Penalizar repeticiones (IMPORTANTE)
        eos_token_id=tokenizer.eos_token_id
    )
    
    llm_local = HuggingFacePipeline(pipeline=pipe)
    
    print("✅ Pipeline de generación listo")
    print("\n" + "=" * 60)
    print("🎉 ¡CHATBOT COMPLETAMENTE CONFIGURADO!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit()


# ============= PASO 6: FUNCIÓN PARA HACER PREGUNTAS =============

def hacer_pregunta(pregunta):
    """
    Función para hacer preguntas al chatbot.
    
    Pasos:
    1. El retriever busca documentos relevantes
    2. Se construye un prompt con contexto
    3. El LLM genera una respuesta
    
    Args:
        pregunta (str): La pregunta del usuario
    
    Returns:
        str: La respuesta generada por la IA
    """
    print(f"\n💭 Buscando información relevante...")
    
    # Obtener documentos relevantes
    docs_contexto = retriever.invoke(pregunta)
    
    # Preparar el contexto
    contexto = "\n".join([
        f"[Documento {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs_contexto)
    ])
    
    # Crear un prompt mejor estructurado
    prompt = f"""You are a helpful psychology expert assistant. Based on the provided documents, answer the user's question clearly and accurately.

Context information:
{contexto}

User question: {pregunta}

Answer based only on the context provided above. Be concise and direct:"""
    
    print("⏳ Generando respuesta...")
    
    # Generar respuesta
    try:
        respuesta = llm_local.invoke(prompt)
        # Limpiar la respuesta de repeticiones obvias
        return respuesta[:800]  # Limitar longitud
    except Exception as e:
        return f"Error al generar respuesta: {e}"


# ============= PASO 7: MENÚ INTERACTIVO =============

def menu_principal():
    """
    Menú interactivo para hacer preguntas al chatbot
    """
    print("\n\n" + "=" * 60)
    print("CHATBOT PSICOLOGÍA - MENÚ INTERACTIVO")
    print("=" * 60)
    print("""
INSTRUCCIONES:
- Escribe tu pregunta sobre psicología
- El chatbot buscará en los PDFs y responderá
- Escribe 'salir' para terminar
""")
    
    while True:
        try:
            # Obtener pregunta del usuario
            pregunta = input("\n📝 Tu pregunta: ").strip()
            
            # Verificar si el usuario quiere salir
            if pregunta.lower() in ['salir', 'exit', 'quit', 'no']:
                print("\n👋 ¡Hasta luego! Gracias por usar el chatbot.")
                break
            
            # Validar que no esté vacío
            if not pregunta:
                print("⚠️  Por favor escribe una pregunta válida")
                continue
            
            # Hacer la pregunta
            respuesta = hacer_pregunta(pregunta)
            
            print("\n" + "-" * 60)
            print("🤖 RESPUESTA DEL CHATBOT:")
            print("-" * 60)
            print(respuesta)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chatbot terminado.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


# ============= PROGRAMA PRINCIPAL =============

if __name__ == "__main__":
    # Ejemplo de uso automático (comentado)
    print("\n\n" + "=" * 60)
    print("EJEMPLO DE USO")
    print("=" * 60)
    
    pregunta_ejemplo = "¿Qué es la depresión?"
    print(f"\n💬 Pregunta: {pregunta_ejemplo}")
    respuesta = hacer_pregunta(pregunta_ejemplo)
    print(f"\n🤖 Respuesta:\n{respuesta}\n")
    
    # Menú interactivo
    print("\nAhora puedes hacer tus propias preguntas:")
    menu_principal()
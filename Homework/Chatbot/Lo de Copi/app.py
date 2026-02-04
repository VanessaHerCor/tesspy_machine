"""
CHATBOT CON LANGCHAIN - ESTRUCTURA BÁSICA

Este es el punto de partida para tu proyecto final.
Está dividido en fases que corresponden a cada sesión.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
load_dotenv()

# Rutas
PDF_FOLDER = Path("pdfs")
PDF_FOLDER.mkdir(exist_ok=True)

# Variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_EMBEDDING = "sentence-transformers/paraphrase-MiniLM-L6-v2"  # Gratuito y rápido

print("=" * 70)
print("CHATBOT CON LANGCHAIN - ESTRUCTURA INICIAL")
print("=" * 70)

# ============================================================================
# FASE 1: CARGAR PDFs
# ============================================================================

def cargar_pdfs():
    """
    Sesión 1: Cargar todos los PDFs de la carpeta 'pdfs/'
    
    Retorna:
        list: Lista de documentos (con metadata de página, etc.)
    """
    from langchain_community.document_loaders import PyPDFLoader
    import glob
    
    pdf_files = glob.glob(str(PDF_FOLDER / "*.pdf"))
    
    if not pdf_files:
        print(f"❌ No se encontraron PDFs en {PDF_FOLDER}")
        print("   Crea la carpeta 'pdfs/' y coloca tus archivos .pdf ahí")
        return []
    
    documentos = []
    for pdf_file in pdf_files:
        print(f"📄 Cargando: {pdf_file}")
        try:
            loader = PyPDFLoader(pdf_file)
            docs = loader.load()
            documentos.extend(docs)
            print(f"   ✅ {len(docs)} páginas cargadas")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return documentos


# ============================================================================
# FASE 2: PREPARAR DOCUMENTOS (Chunking)
# ============================================================================

def preparar_documentos(documentos, chunk_size=1000, overlap=200):
    """
    Sesión 2: Dividir documentos grandes en chunks más pequeños
    
    Args:
        documentos: Lista de documentos cargados
        chunk_size: Tamaño de cada chunk (caracteres)
        overlap: Sobreposición entre chunks (para contexto)
    
    Retorna:
        list: Documentos divididos en chunks
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    if not documentos:
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    
    chunks = splitter.split_documents(documentos)
    print(f"\n📚 Total de chunks creados: {len(chunks)}")
    return chunks


# ============================================================================
# FASE 3: CREAR EMBEDDINGS Y VECTOR DATABASE
# ============================================================================

def crear_vector_database(chunks):
    """
    Sesión 3: Crear embeddings y almacenarlos en FAISS
    
    Args:
        chunks: Documentos divididos en chunks
    
    Retorna:
        FAISS: Vector database lista para búsquedas
    """
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    
    if not chunks:
        print("❌ No hay chunks para procesar")
        return None
    
    print("\n🧠 Creando embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_EMBEDDING)
    
    print("💾 Almacenando en FAISS...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    
    print(f"✅ Vector database creada con {len(chunks)} documentos")
    return vector_db


# ============================================================================
# FASE 4: CREAR CADENA DE PREGUNTA-RESPUESTA
# ============================================================================

def crear_chatbot(vector_db):
    """
    Sesión 4: Conectar vector DB con LLM
    
    Args:
        vector_db: Vector database con embeddings
    
    Retorna:
        function: Función para hacer preguntas
    """
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    
    if vector_db is None:
        print("❌ Vector database no disponible")
        return None
    
    if not OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY no configurada")
        print("   Opción 1: Configura en .env")
        print("   Opción 2: Usa modelo local con HuggingFacePipeline")
        return None
    
    print("\n🤖 Configurando LLM...")
    
    llm = OpenAI(
        api_key=OPENAI_API_KEY,
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500
    )
    
    # Crear cadena QA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    print("✅ Chatbot listo para usar")
    return qa_chain


# ============================================================================
# PHASE 5: INTERFAZ STREAMLIT
# ============================================================================

def crear_interfaz_streamlit(qa_chain):
    """
    Sesión 5+: Interfaz web con Streamlit
    
    Esta función se ejecuta con: streamlit run app.py
    """
    try:
        import streamlit as st
        from streamlit_chat import message
    except ImportError:
        print("⚠️  Streamlit no instalado. Instala con: pip install streamlit streamlit-chat")
        return
    
    st.set_page_config(page_title="Mi Chatbot Inteligente", layout="wide")
    st.title("🤖 Chatbot Inteligente con LangChain")
    
    # Inicializar estado
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensajes previos
    with st.container():
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=str(i))
            else:
                message(msg["content"], is_user=False, key=str(i))
    
    # Input del usuario
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("Tu pregunta:", key="input")
        with col2:
            enviar = st.button("Enviar")
    
    # Procesar pregunta
    if enviar and user_input:
        # Agregar pregunta al historial
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Obtener respuesta
        with st.spinner("Buscando respuesta..."):
            try:
                resultado = qa_chain(user_input)
                respuesta = resultado["result"]
                fuentes = resultado.get("source_documents", [])
                
                # Agregar respuesta al historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": respuesta
                })
                
                # Mostrar fuentes
                if fuentes:
                    st.info("**Fuentes consultadas:**")
                    for doc in fuentes:
                        st.write(f"- {doc.metadata.get('source', 'PDF')}")
                
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


# ============================================================================
# MAIN - ORQUESTACIÓN
# ============================================================================

def main():
    """Función principal que orquesta todo el flujo"""
    
    print("\n1️⃣  CARGANDO PDFs...")
    documentos = cargar_pdfs()
    
    if not documentos:
        print("Abortando. Coloca PDFs en la carpeta 'pdfs/'")
        return
    
    print("\n2️⃣  PREPARANDO DOCUMENTOS...")
    chunks = preparar_documentos(documentos)
    
    print("\n3️⃣  CREANDO VECTOR DATABASE...")
    vector_db = crear_vector_database(chunks)
    
    if vector_db is None:
        print("No se pudo crear la base de datos vectorial")
        return
    
    print("\n4️⃣  CREANDO CHATBOT...")
    chatbot = crear_chatbot(vector_db)
    
    if chatbot is None:
        print("⚠️  Chatbot no disponible (falta API key)")
        print("Pero la vector database está lista para búsquedas")
        return
    
    # Ejemplo de uso interactivo
    print("\n" + "=" * 70)
    print("CHATBOT LISTO PARA USAR")
    print("=" * 70)
    print("\nEscribe 'exit' para salir\n")
    
    while True:
        pregunta = input("Tu pregunta: ").strip()
        
        if pregunta.lower() in ["exit", "salir", "quit"]:
            print("👋 ¡Hasta luego!")
            break
        
        if not pregunta:
            continue
        
        try:
            resultado = chatbot(pregunta)
            print(f"\n🤖 Respuesta: {resultado['result']}\n")
            
            if resultado.get("source_documents"):
                print("📚 Basado en:")
                for doc in resultado["source_documents"]:
                    print(f"  - {doc.metadata.get('source', 'PDF')}")
            print()
        except Exception as e:
            print(f"❌ Error: {e}\n")


# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    main()

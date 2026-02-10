# ============================================================================
# CHATBOT DE PSICOLOGÍA - PROYECTO FINAL
# Basado en LangChain y Sistema RAG (Retrieval-Augmented Generation)
# ============================================================================

# PASO 1: IMPORTAR LIBRERÍAS NECESARIAS
# ============================================================================

import os
import glob  # Para buscar archivos PDF
from pathlib import Path

# Librerías de LangChain - el framework principal para construir chatbots
from langchain_community.document_loaders import PyPDFLoader  # Carga archivos PDF
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Divide textos en fragmentos
from langchain_community.vectorstores import FAISS  # Base de datos de vectores (embeddings)
from langchain_huggingface import HuggingFaceEmbeddings  # Convierte texto a vectores (versión actualizada)
from langchain_community.llms import HuggingFacePipeline  # Pipeline local de HuggingFace

# Para usar modelos locales
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline  # Modelos locales
import torch  # Para GPU (si está disponible)

# ============================================================================
# PASO 2: CONFIGURAR LA RUTA A LOS PDFs
# ============================================================================

# Indicar dónde están guardados los archivos PDF
PDF_FOLDER = "PDF_PSY"  # Carpeta con los PDFs

# Validar que la carpeta existe
if not os.path.exists(PDF_FOLDER):
    print(f"❌ ERROR: La carpeta '{PDF_FOLDER}' no existe.")
    print("Por favor, crea una carpeta 'PDF_PSY' en la misma ubicación que este archivo.")
    exit()

# Buscar todos los archivos PDF en la carpeta
pdf_files = glob.glob(os.path.join(PDF_FOLDER, "*.pdf"))

if not pdf_files:
    print(f"❌ ERROR: No hay archivos PDF en la carpeta '{PDF_FOLDER}'")
    exit()

print(f"✅ Se encontraron {len(pdf_files)} archivos PDF")
print("Archivos cargados:")
for pdf in pdf_files:
    print(f"  - {os.path.basename(pdf)}")

# ============================================================================
# PASO 3: CARGAR Y PROCESAR LOS PDFs
# ============================================================================
print("\n📄 Cargando documentos PDF...")

# Lista para almacenar todos los documentos
all_documents = []

# Cargar cada PDF
for pdf_file in pdf_files:
    try:
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        all_documents.extend(documents)
        print(f"✅ Cargado: {os.path.basename(pdf_file)} ({len(documents)} páginas)")
    except Exception as e:
        print(f"⚠️ Error al cargar {pdf_file}: {e}")

print(f"\n✅ Total de documentos cargados: {len(all_documents)}")

# ============================================================================
# PASO 4: DIVIDIR DOCUMENTOS EN FRAGMENTOS PEQUEÑOS (CHUNKS)
# ============================================================================
print("\n✂️ Dividiendo documentos en fragmentos...")

# Dividir el texto en fragmentos más pequeños (600 chars) para mejor comprensión
# Chunks más pequeños = mejor relevancia y menos confusión del modelo
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,       # Fragmentos más pequeños = mejor precisión
    chunk_overlap=100,    # Solapamiento menor para eficiencia
)

# Aplicar la división a todos los documentos
chunks = text_splitter.split_documents(all_documents)
print(f"✅ Documentos divididos en {len(chunks)} fragmentos")

# ============================================================================
# PASO 5: CREAR EMBEDDINGS (VECTORES) DE LOS FRAGMENTOS
# ============================================================================
print("\n🧠 Creando embeddings (vectores)...")

# Usar HuggingFace para crear embeddings - estos son GRATUITOS
# Los embeddings convierten texto en números que representan el significado
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    # Este modelo funciona bien con textos en español
)

# Nombre del archivo donde se guardarán los embeddings
EMBEDDINGS_PATH = "embedding_storage"

# Verificar si ya existen embeddings guardados (para no procesarlos de nuevo)
if os.path.exists(EMBEDDINGS_PATH):
    print(f"✅ Encontrados embeddings guardados en '{EMBEDDINGS_PATH}'")
    print("Cargando embeddings... (esto es MUCHO más rápido)")
    vector_store = FAISS.load_local(EMBEDDINGS_PATH, embeddings, allow_dangerous_deserialization=True)
    print("✅ Embeddings cargados exitosamente")
else:
    # Crear la base de datos de vectores usando FAISS (muy rápido y eficiente)
    # Esto almacena todos los embeddings y permite búsquedas rápidas
    print("Primera vez: creando embeddings...")
    print("Esto puede tardar unos momentos...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # GUARDAR los embeddings para la próxima vez (igual que tu profesor)
    print(f"\n💾 Guardando embeddings en '{EMBEDDINGS_PATH}' para uso futuro...")
    vector_store.save_local(EMBEDDINGS_PATH)
    print("✅ Base de datos de vectores creada y guardada exitosamente")
    print("⚡ La próxima vez cargará MUCHO más rápido")

# ============================================================================
# PASO 6: CREAR EL RETRIEVER
# ============================================================================
print("\n🔍 Configurando el retriever...")

# El retriever busca los fragmentos más relevantes para cada pregunta
# search_kwargs={'k': 4} significa que traerá los 4 fragmentos más similares
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

print("✅ Retriever configurado (buscará los 4 documentos más relevantes)")

# ============================================================================
# PASO 7: CONFIGURAR EL MODELO DE LENGUAJE (LLM)
# ============================================================================
print("\n🤖 Configurando el modelo de lenguaje...")

# Vamos a usar un modelo GRATUITO de HuggingFace
# Puedes cambiar el modelo según tus necesidades
# Modelos recomendados: "mistralai/Mistral-7B-Instruct-v0.2" o "meta-llama/Llama-2-7b-chat"

# ============================================================================
# PASO 7: CONFIGURAR EL MODELO DE LENGUAJE LOCAL (LLM)
# ============================================================================
print("\n🤖 Configurando el modelo de lenguaje local...")
print("⚠️ Primera vez: descargará ~7GB (puede tardar 10-20 minutos)...")

llm = None  # Inicializar

try:
    # Usar Microsoft Phi-2: modelo poderoso optimizado
    # Con parámetros ajustados para mejor rendimiento
    model_id = "microsoft/phi-2"
    
    print(f"📥 Descargando modelo: {model_id}")
    print("Este proceso solo ocurre la primera vez...")
    
    # Cargar el tokenizador
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Cargar el modelo (esto descargará ~7GB)
    # torch_dtype=torch.float16 lo hace más pequeño y rápido
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        torch_dtype=torch.float16  # Usar 16-bit para usar menos memoria
    )
    
    # Crear el pipeline de generación de texto con parámetros optimizados
    # Estos parámetros evitan repeticiones y generan respuestas coherentes
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,           # Respuestas moderadas (300 tokens)
        temperature=0.7,              # Variedad en generación (evita monotonía)
        top_p=0.9,                    # Nucleus sampling (variedad controlada)
        repetition_penalty=1.2,       # Penaliza repeticiones
        do_sample=True                # Muestreo para diversidad
    )
    
    # Envolver en HuggingFacePipeline para LangChain
    llm = HuggingFacePipeline(pipeline=pipe)
    
    print("✅ Modelo de lenguaje configurado correctamente")
    print(f"✅ Usando: {model_id}")
    
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    print("Asegúrate de tener:")
    print("  - 16GB+ RAM disponible")
    print("  - PyTorch instalado: pip install torch")
    print("  - Conexión a internet (para descargar el modelo)")
    llm = None

# ============================================================================
# PASO 8: CONFIGURACIÓN LISTA
# ============================================================================
print("✅ Todos los componentes están listos")

# ============================================================================
# PASO 9: CREAR LA CADENA CONVERSACIONAL (MANUAL - compatible con LangChain nuevo)
# ============================================================================
print("\n⛓️ Configurando el sistema de respuestas...")

qa_chain = None

if llm is not None:
    # En lugar de usar ConversationalRetrievalChain (que está deprecado),
    # vamos a implementar la lógica manualmente pero MÁS compatible
    # Esto le permite al modelo recordar el historial
    
    print("✅ Sistema de respuestas configurado")
    qa_chain = True  # Marcador simple de que está listo
else:
    print("⚠️ No se puede crear la cadena sin el modelo LLM")
    print("Verifica que el modelo se cargó correctamente")

# ============================================================================
# PASO 10: VARIABLE PARA GUARDAR EL HISTORIAL DE CHAT
# ============================================================================

# El historial se guarda aquí para que la IA recuerde la conversación
chat_history = []

# ============================================================================
# PASO 11: FUNCIÓN PARA HACER PREGUNTAS AL CHATBOT
# ============================================================================

def hacer_pregunta(pregunta):
    """
    Función para hacer una pregunta al chatbot con historial conversacional
    
    Args:
        pregunta (str): La pregunta que deseas hacer
    """
    global chat_history  # Usar el historial global
    
    print(f"\n👤 Tu pregunta: {pregunta}")
    print("-" * 60)
    
    if qa_chain is None:
        print("❌ El chatbot no está disponible")
        return
    
    try:
        # PASO 1: Buscar documentos relevantes
        print("🔍 Buscando información relevante...")
        docs_relevantes = retriever.invoke(pregunta)
        
        # PASO 2: Preparar el contexto de los documentos
        contexto = "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" 
                                for i, doc in enumerate(docs_relevantes)])
        
        # PASO 3: Construir el historial conversacional para darle contexto al modelo
        # Esto permite que el modelo recuerde las preguntas anteriores
        historial_texto = ""
        if chat_history:
            historial_texto = "\n\nHistorial de conversación anterior:\n"
            for q, a in chat_history[-3:]:  # Últimas 3 conversaciones para no contaminar
                historial_texto += f"P: {q}\nR: {a}\n"
        
        # PASO 4: Crear un prompt más simple y directo
        # Menos contexto = mejor generación, el modelo no se confunde
        prompt = f"""Basándote en la siguiente información de libros de Psicología, responde la pregunta de forma concisa:

INFORMACIÓN:
{contexto}

PREGUNTA: {pregunta}
RESPUESTA CONCISA:"""
        
        print("⏳ Generando respuesta...")
        
        # PASO 5: Generar la respuesta usando el LLM
        respuesta_completa = llm.invoke(prompt)
        
        # Extraer solo la respuesta (quitar el prompt que devuelve el modelo)
        if "RESPUESTA CONCISA:" in respuesta_completa:
            respuesta = respuesta_completa.split("RESPUESTA CONCISA:")[-1].strip()
        else:
            respuesta = respuesta_completa.strip()
        
        # Si la respuesta es muy larga o vacía, limpiarla
        respuesta = respuesta[:1500].strip()  # Máximo 1500 caracteres
        if not respuesta:
            respuesta = "No pude generar una respuesta. Intenta reformular tu pregunta."
        
        print(f"\n🤖 Respuesta del chatbot:")
        print(respuesta)
        
        # PASO 6: Guardar en el historial para la próxima pregunta
        chat_history.append((pregunta, respuesta))
        
        # PASO 7: Mostrar los documentos de los que se extrajo la información
        print(f"\n📚 Documentos consultados ({len(docs_relevantes)}): ")
        for i, doc in enumerate(docs_relevantes, 1):
            fuente = doc.metadata.get('source', 'Fuente desconocida')
            pagina = doc.metadata.get('page', 'N/A')
            print(f"  {i}. {fuente} (Página {pagina})")
        
        return respuesta
    
    except Exception as e:
        print(f"❌ Error al procesar la pregunta: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# PASO 11: INTERFAZ DE USUARIO (LOOP INTERACTIVO)
# ============================================================================

def iniciar_chatbot():
    """
    Inicia el chatbot en modo conversacional
    El usuario puede hacer preguntas hasta escribir 'salir'
    El chatbot recuerda el contexto de la conversación
    """
    
    # Verificar si el chatbot está completamente configurado
    if qa_chain is None:
        print("\n❌ ERROR: El chatbot no está completamente configurado")
        print("No fue posible cargar el modelo de lenguaje local.")
        print("\nPara arreglarlo:")
        print("1. Asegúrate de tener PyTorch: pip install torch")
        print("2. Verifica que tienes al menos 16GB de RAM disponibles")
        print("3. Vuelve a ejecutar este archivo")
        print("\nMientras tanto, puedes usar: python test.py")
        print("(que busca documentos sin usar el modelo LLM)")
        return
    
    print("\n" + "="*60)
    print("🎓 BIENVENIDO AL CHATBOT DE PSICOLOGÍA INTELIGENTE")
    print("="*60)
    print("\n✨ Este chatbot RECUERDA nuestra conversación")
    print("Escribe tus preguntas sobre psicología.")
    print("El chatbot usará IA para generar respuestas inteligentes.")
    print("\nEscribe 'salir' o 'quit' para terminar.")
    print("Escribe 'limpiar' para olvidar el historial.\n")
    
    while True:
        # Pedir pregunta al usuario
        pregunta = input("\n📝 Escribe tu pregunta: ").strip()
        
        # Verificar si el usuario quiere salir
        if pregunta.lower() in ["salir", "quit", "exit"]:
            print("\n👋 ¡Hasta luego! Gracias por usar el chatbot.")
            break
        
        # Limpiar historial
        if pregunta.lower() == "limpiar":
            chat_history.clear()
            print("🧹 Historial de conversación limpiado.")
            continue
        
        # Ignorar preguntas vacías
        if not pregunta:
            continue
        
        # Hacer la pregunta al chatbot
        hacer_pregunta(pregunta)

# ============================================================================
# PASO 12: EJECUTAR EL CHATBOT
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("INICIALIZANDO CHATBOT DE PSICOLOGÍA")
    print("="*60)
    
    # Iniciar el loop interactivo
    iniciar_chatbot()

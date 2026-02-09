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
from langchain_community.embeddings import HuggingFaceEmbeddings  # Convierte texto a vectores
from langchain.chains import ConversationalRetrievalChain  # Cadena conversacional (como el profesor)
from langchain.prompts import PromptTemplate  # Template para dar instrucciones al modelo

# Para usar modelos locales (como el profesor)
from langchain_community.llms import HuggingFacePipeline  # Pipeline local de HuggingFace
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

# Dividir el texto en fragmentos de 1000 caracteres con 200 caracteres de solapamiento
# Esto es importante para que el modelo entienda mejor el contexto
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamaño de cada fragmento
    chunk_overlap=200,    # Solapamiento para no perder contexto
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
EMBEDDINGS_PATH = "embeddings_psy"

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
    # Usar Microsoft Phi-2: más pequeño que Mistral pero muy poderoso
    # Es lo que recomendó tu profesor
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
    
    # Crear el pipeline de generación de texto
    # max_new_tokens controla cuán larga será la respuesta
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512  # Respuestas moderadas
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
# PASO 8: CREAR EL TEMPLATE DE PREGUNTA (PROMPT)
# ============================================================================

# Este template define cómo se le formula la pregunta al modelo
# Incluye el contexto (documentos relevantes) y la pregunta del usuario
prompt_template = """Eres un asistente experto en Psicología. 
Usa la siguiente información para responder la pregunta de manera clara y completa.
Si no sabes la respuesta, di que no tienes la información disponible.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:"""

# Crear el prompt usando el template
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# ============================================================================
# PASO 9: CREAR LA CADENA CONVERSACIONAL (COMO EL PROFESOR)
# ============================================================================
print("\n⛓️ Creando la cadena conversacional...")

qa_chain = None

if llm is not None:
    # Usar ConversationalRetrievalChain (igual que el profesor)
    # Esta cadena:
    # 1. Recuerda el historial de conversación
    # 2. Busca documentos relevantes
    # 3. Genera respuestas basadas en los documentos
    
    try:
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,                              # Modelo de lenguaje local
            retriever=retriever,                  # El retriever que configuramos
            return_source_documents=True         # Mostrar de dónde sacó la información
        )
        print("✅ Cadena conversacional lista para usar")
    except Exception as e:
        print(f"⚠️ Error al crear la cadena: {e}")
        qa_chain = None
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
        # Hacer la pregunta a la cadena
        # El historial le permite al modelo recordar conversaciones previas
        result = qa_chain.invoke({
            "question": pregunta,
            "chat_history": chat_history
        })
        
        # Extraer la respuesta
        respuesta = result.get("answer", "No se pudo obtener respuesta")
        
        print(f"\n🤖 Respuesta del chatbot:")
        print(respuesta)
        
        # Guardar en el historial para la próxima pregunta
        # Esto le permite al chatbot recordar
        chat_history.append((pregunta, respuesta))
        
        # Mostrar los documentos de los que se extrajo la información
        if "source_documents" in result:
            print(f"\n📚 Documentos consultados ({len(result['source_documents'])}): ")
            for i, doc in enumerate(result['source_documents'], 1):
                fuente = doc.metadata.get('source', 'Fuente desconocida')
                pagina = doc.metadata.get('page', 'N/A')
                print(f"  {i}. {fuente} (Página {pagina})")
        
        return result
    
    except Exception as e:
        print(f"❌ Error al procesar la pregunta: {e}")
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

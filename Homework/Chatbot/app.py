# ╔════════════════════════════════════════════════════════════════════════════╗
# ║           CHATBOT INTELIGENTE CON LANGCHAIN - CARGA DE PDFs                ║
# ║                                                                              ║
# ║  Este código carga tus PDFs de psicología y prepara la información para     ║
# ║  entrenar un chatbot inteligente que pueda responder preguntas basadas      ║
# ║  en el contenido de tus documentos.                                         ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# ============================================================================
# PASO 1: IMPORTAR LIBRERÍAS NECESARIAS
# ============================================================================

import os                                      # Para manejo de rutas de archivos
import glob                                    # Para buscar archivos (*. pdf)
from pathlib import Path                       # Para manejo profesional de rutas

# Importar el cargador de PDFs de LangChain
from langchain_community.document_loaders import PyPDFLoader

# ⭐ IMPORTAR PARA GUARDAR/CARGAR FAISS (BASE DE DATOS)
from langchain_community.vectorstores import FAISS

# ============================================================================
# PASO 2: CONFIGURAR LA RUTA DE TUS PDFs
# ============================================================================

# Define la carpeta donde están tus PDFs
# En tu caso es: Homework/Chatbot/PDF_PSY
pdf_folder_path = r'PDF_PSY'  # La 'r' significa "raw string" (ruta sin procesar)

# Alternativa más profesional con Path:
pdf_folder_path = Path('PDF_PSY')  # Esto funciona en Windows, Mac y Linux

# ⭐ RUTA DONDE GUARDAREMOS LA BASE DE DATOS FAISS
# Si la carpeta existe, no la recrea. Si no existe, la crea automáticamente
faiss_db_path = Path('FAISS_DB')  # Se guardará en una carpeta llamada FAISS_DB

# ============================================================================
# PASO 3: VERIFICAR QUE LA CARPETA EXISTE
# ============================================================================

# Verificar si la carpeta de PDFs existe
if not os.path.exists(pdf_folder_path):
    # Si NO existe, crear la carpeta
    os.makedirs(pdf_folder_path)
    print(f'❌ La carpeta {pdf_folder_path} no existe.')
    print(f'✅ Se creó automáticamente. Coloca tus PDFs ahí.')
else:
    # Si existe, mostrar confirmación
    print(f'✅ Carpeta encontrada: {pdf_folder_path}')

# ============================================================================
# PASO 4: BUSCAR TODOS LOS ARCHIVOS .PDF EN LA CARPETA
# ============================================================================

# glob.glob() busca todos los archivos que coincidan con el patrón
# En este caso: cualquier archivo .pdf en la carpeta PDF_PSY
pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")

# Mostrar cuántos PDFs encontró
print(f"\n📚 PDFs encontrados: {len(pdf_files)}")
for i, pdf in enumerate(pdf_files, 1):
    print(f"   {i}. {os.path.basename(pdf)}")  # Mostrar solo el nombre del archivo

# ============================================================================
# PASO 5: CARGAR TODOS LOS PDFs Y EXTRAER SU CONTENIDO
# ============================================================================

# Esta lista almacenará TODAS las páginas de TODOS los PDFs
all_pages = []

# Recorrer cada archivo PDF encontrado
for pdf_file in pdf_files:
    print(f"\n📖 Procesando: {os.path.basename(pdf_file)}...")
    
    try:
        # PASO 5a: Crear un cargador para este PDF específico
        loader = PyPDFLoader(pdf_file)
        
        # PASO 5b: Cargar todas las páginas del PDF
        # Cada página contiene: contenido de texto + metadatos (nombre, número de página)
        pages = loader.load()
        
        # PASO 5c: Agregar todas las páginas a nuestra lista general
        all_pages.extend(pages)
        
        # Mostrar cuántas páginas se extrajeron de este PDF
        print(f"   ✅ {len(pages)} páginas cargadas exitosamente")
        
    except Exception as e:
        # Si hay error, mostrarlo pero continuar con el siguiente PDF
        print(f"   ❌ Error al cargar: {e}")

# ============================================================================
# PASO 6: RESUMEN FINAL
# ============================================================================

print(f"\n" + "="*70)
print(f"✅ PROCESO COMPLETADO")
print(f"="*70)
print(f"Total de páginas cargadas: {len(all_pages)}")
print(f"\nAhora tienes {len(all_pages)} páginas de contenido listas para:")
print(f"  1. Dividir en chunks (párrafos pequeños)")
print(f"  2. Crear embeddings (vectores)")
print(f"  3. Entrenar el chatbot")
print(f"="*70)

# ============================================================================
# PASO 7: DIVIDIR EL CONTENIDO EN CHUNKS (PÁRRAFOS PEQUEÑOS)
# ============================================================================
# 
# ¿POR QUÉ dividir?
#   - Los modelos de IA no pueden procesar texto muy largo de una sola vez
#   - Es mejor tener párrafos pequeños y manejables
#   - Facilita buscar información relevante más rápido
#
# ¿QUÉ es un chunk?
#   - Un trozo de texto de ~1000 caracteres (aproximadamente 200 palabras)
#   - Los chunks se pueden traslapar (overlap) para no perder contexto
#

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Crear un divisor de texto con parámetros específicos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Cada chunk tendrá máximo 1000 caracteres
    chunk_overlap=200,      # Los chunks se superponen 200 caracteres (para contexto)
    separators=["\n\n", "\n", ".", " "]  # Separadores por orden de preferencia
)

# Dividir TODOS los documentos en chunks
chunks = text_splitter.split_documents(all_pages)

print(f"\n" + "="*70)
print(f"📦 CHUNKS CREADOS")
print(f"="*70)
print(f"Total de chunks: {len(chunks)}")
print(f"\nEjemplo del primer chunk:")
print(f"-" * 70)
# ============================================================================
# PASO 8: CREAR EMBEDDINGS O CARGAR LA BASE DE DATOS GUARDADA
# ============================================================================
#
# ⭐ OPTIMIZACIÓN: Aquí es donde ocurre la "magia"
#    - PRIMERA VEZ: Crea embeddings (tarda ~5 minutos)
#    - SIGUIENTES VECES: Carga la base de datos guardada (tarda <1 segundo)
#

from langchain_community.embeddings import HuggingFaceEmbeddings

# Crear el modelo de embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)

# ⭐ VERIFICAR SI LA BASE DE DATOS YA EXISTE
if faiss_db_path.exists():
    # SI EXISTE: Cargar la base de datos guardada (¡RÁPIDO!)
    print(f"\n" + "="*70)
    print(f"⚡ CARGANDO BASE DE DATOS GUARDADA (RÁPIDO)")
    print(f"="*70)
    print(f"📂 Encontrada base de datos en: {faiss_db_path}")
    print(f"⏱️ Cargando... (esto tarda <1 segundo)")
    
    # Cargar FAISS desde disco
    vector_store = FAISS.load_local(
        folder_path=str(faiss_db_path),
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    
    print(f"✅ Base de datos cargada exitosamente")
    print(f"   📊 Documentos en la BD: {len(chunks)} chunks")
    
else:
    # SI NO EXISTE: Crear la base de datos (proceso completo)
    print(f"\n" + "="*70)
    print(f"🧠 MODELO DE EMBEDDINGS CARGADO")
    print(f"="*70)
    print(f"Modelo: sentence-transformers/paraphrase-MiniLM-L6-v2")
    print(f"Tipo de vector: 384 dimensiones (números por vector)")

    # Crear un embedding de prueba para mostrar cómo funciona
    print(f"\n📝 Creando embedding de prueba...")
    test_text = "La psicología es el estudio del comportamiento humano"
    test_embedding = embeddings.embed_query(test_text)
    print(f"✅ Embedding creado: {len(test_embedding)} números")
    print(f"   Primeros 5 números: {test_embedding[:5]}")


# ============================================================================
# PASO 9: CREAR BASE DE DATOS VECTORIAL (FAISS) O REUTILIZAR LA EXISTENTE
# ============================================================================
#
# ¿QUÉ es FAISS?
#   - Base de datos especializada en almacenar vectores
#   - Permite búsquedas rápidas por SIMILITUD
#   - Usada por Google, Meta, OpenAI
#
# ⭐ OPTIMIZACIÓN: Si la base de datos existe, solo la cargamos
#

# Si NO teníamos la base de datos guardada, crearla ahora
if not faiss_db_path.exists():
    print(f"\n" + "="*70)
    print(f"💾 CREANDO BASE DE DATOS VECTORIAL (FAISS)")
    print(f"="*70)
    print(f"⏱️ Esto puede tardar 1-2 minutos (solo la primera vez)...")
    print(f"   (Las siguientes veces será instantáneo)")

    # Crear la base de datos vectorial a partir de los chunks
    # Cada chunk se convierte en un vector y se almacena en FAISS
    vector_store = FAISS.from_documents(
        documents=chunks,           # Los chunks a procesar
        embedding=embeddings        # El modelo de embeddings a usar
    )

    print(f"✅ Base de datos vectorial creada")
    print(f"   Documentos indexados: {len(chunks)}")
    
    # ⭐ GUARDAR LA BASE DE DATOS EN DISCO
    print(f"\n💾 Guardando base de datos para próximas ejecuciones...")
    vector_store.save_local(folder_path=str(faiss_db_path))
    print(f"✅ Guardado en: {faiss_db_path}")
    print(f"   Próximas ejecuciones serán mucho más rápidas ⚡")

# ============================================================================
# PASO 10: BUSCAR INFORMACIÓN SIMILAR
# ============================================================================
#
# Ahora que tenemos todo preparado, podemos hacer búsquedas inteligentes
#

print(f"\n" + "="*70)
print(f"🔍 BÚSQUEDA INTERACTIVA EN PDFs")
print(f"="*70)
print(f"\n¡Tu chatbot está listo para responder preguntas!")
print(f"Escribe 'salir' para terminar\n")

# Loop interactivo para hacer búsquedas
while True:
    # Solicitar pregunta al usuario
    query = input("❓ ¿Qué quieres preguntar?: ").strip()
    
    # Si dice salir, terminar
    if query.lower() in ['salir', 'exit', 'quit']:
        print("\n👋 ¡Hasta luego!")
        break
    
    # Si está vacío, pedir que escriba algo
    if not query:
        print("⚠️ Por favor, escribe una pregunta\n")
        continue
    
    # Buscar documentos similares
    print(f"\n🔍 Buscando información sobre: '{query}'")
    print("   (esto tarda un segundo...)\n")
    
    try:
        results = vector_store.similarity_search(query, k=3)
        
        print(f"✅ Encontrados {len(results)} resultados similares:\n")
        
        for i, result in enumerate(results, 1):
            page_num = result.metadata.get('page', 'N/A')
            content = result.page_content[:200]
            
            print(f"Resultado {i}: (Página {page_num})")
            print(f"  {content}...")
            print()
        
    except Exception as e:
        print(f"❌ Error en la búsqueda: {e}\n")

# ============================================================================
# PASO 11: FIN DEL CHATBOT INTERACTIVO
# ============================================================================

print(f"\n" + "="*70)
print(f"📋 RESUMEN DEL PROGRESO")
print(f"="*70)
print(f"✅ Paso 1:  PDFs cargados ({len(all_pages)} páginas)")
print(f"✅ Paso 2:  Chunks creados ({len(chunks)} chunks)")
print(f"✅ Paso 3:  Embeddings generados")
print(f"✅ Paso 4:  Base de datos vectorial (FAISS) lista")
print(f"✅ Paso 5:  Chat interactivo completado ✓")
print(f"\n🚀 PRÓXIMAS MEJORAS:")
print(f"  1. Conectar con OpenAI GPT (para respuestas inteligentes)")
print(f"  2. Crear interfaz Streamlit (chat web bonito)")
print(f"  3. Agregar historial de conversaciones")
print(f"="*70)
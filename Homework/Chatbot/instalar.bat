@echo off
REM ============================================================================
REM SCRIPT DE INSTALACIÓN AUTOMÁTICA - CHATBOT DE PSICOLOGÍA
REM ============================================================================
REM Este script configura automáticamente todo lo necesario para ejecutar
REM el chatbot de Psicología en Windows

echo.
echo ============================================================
echo INSTALADOR AUTOMÁTICO - CHATBOT DE PSICOLOGÍA
echo ============================================================
echo.

REM Verificar si existe .venv
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error: No se pudo crear el entorno virtual
        echo Asegúrate de tener Python 3.10+ instalado
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

echo.
echo 🔄 Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado

echo.
echo 📥 Actualizando pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ⚠️ Advertencia: Pip ya está actualizado
)

echo.
echo 📦 Instalando dependencias exactas...
echo (Esta operación puede tomar 5-10 minutos)
echo.

REM Instalar requirements exactos
pip install langchain==1.2.9 langchain-community==0.4.1 langchain-text-splitters==1.1.0 langchain-huggingface==1.2.0 transformers==5.1.0 torch==2.10.0 sentence-transformers==5.2.2 huggingface_hub==1.4.1 faiss-cpu==1.13.2 pypdf==6.6.2

if errorlevel 1 (
    echo ❌ Error durante la instalación de dependencias
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo 📁 Estructura de carpetas:
echo    Chatbot/
echo    ├── app.py (versión avanzada - RECOMENDADA)
echo    ├── main.py (versión ligera)
echo    ├── PDF_PSY/ (tu carpeta de PDFs)
echo    └── .venv/ (entorno virtual) ✅ CREADO
echo.
echo 🚀 PRÓXIMOS PASOS:
echo    1. Copia tus archivos PDF a la carpeta "PDF_PSY"
echo    2. Ejecuta: python app.py
echo    3. Responde a las preguntas interactivamente
echo.
echo 📚 Documentación:
echo    - README.md: Guía general del proyecto
echo    - COMPARACION.md: Diferencias entre app.py y main.py
echo    - TROUBLESHOOTING.md: Solución de problemas
echo.
echo ⚠️  IMPORTANTE:
echo    - Primera ejecución descargará ~7GB (10-20 minutos)
echo    - Las siguientes ejecuciones serán más rápidas (todo en caché)
echo.
pause

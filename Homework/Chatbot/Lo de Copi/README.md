# CHATBOT INTELIGENTE CON LANGCHAIN

## 📁 Estructura del Proyecto

```
Chatbot/
├── pdfs/                      ← Coloca tus PDFs aquí
│   ├── documento1.pdf
│   ├── documento2.pdf
│   └── documento3.pdf
├── app.py                     ← Código principal (Streamlit)
├── requirements.txt           ← Dependencias
├── .env                       ← Variables de entorno (API keys)
├── README.md                  ← Este archivo
├── PLAN_EJECUCION.md         ← Plan detallado
└── RESUMEN_CONCEPTOS.md      ← Guía rápida
```

## 🚀 QUICK START

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables (Opcional)
Crea `.env` con:
```
OPENAI_API_KEY=tu_clave_aqui
HUGGINGFACEHUB_API_TOKEN=tu_token_aqui
```

### 3. Agregar PDFs
- Crea carpeta `pdfs/` si no existe
- Coloca 3+ PDFs ahí
- Asegúrate que estén en el MISMO idioma

### 4. Ejecutar
```bash
streamlit run app.py
```

---

## 📚 CONCEPTOS CLAVE

### Embeddings
Cada palabra/texto se convierte en un vector (lista de números) que captura su significado.

```
"Hola" → [0.12, -0.45, 0.89, ..., 0.34]  (768 números)
```

### RAG (Retrieval-Augmented Generation)
El chatbot busca información relevante en TUS PDFs y la usa para generar respuestas mejor contextualizadas.

```
Pregunta → Buscar en PDFs → Pasar a GPT → Respuesta
```

### Vector Database (FAISS)
Almacena todos los vectores de tus documentos para búsquedas rápidas por similitud.

---

## 🔧 ROADMAP DE DESARROLLO

### Fase 1: Cargar Documentos (Sesión 1)
- [ ] Cargar PDFs con PyPDFLoader
- [ ] Dividir en chunks (párrafos)
- [ ] Verificar que se carga correctamente

### Fase 2: Crear Embeddings (Sesión 2)
- [ ] Usar HuggingFaceEmbeddings
- [ ] Guardar en FAISS
- [ ] Probar búsqueda de similitud

### Fase 3: Conectar LLM (Sesión 3)
- [ ] Integrar OpenAI o modelo local
- [ ] Crear cadena de preguntas-respuestas
- [ ] Probar E2E

### Fase 4: Interfaz Streamlit (Sesión 4+)
- [ ] Crear UI para chatear
- [ ] Historial de conversación
- [ ] Mostrar fuentes de respuestas
- [ ] Parámetros ajustables

---

## 📝 NOTAS IMPORTANTES

1. **PDFs:** Deben ser de BUENA calidad (legibles por máquina, no escaneados)
2. **Idioma:** Todos en el MISMO idioma (español, inglés, etc.)
3. **Cantidad:** 3-5 PDFs de 20+ páginas es ideal
4. **API Keys:** Necesarias para OpenAI o Hugging Face (algunos servicios son gratis)
5. **Tiempo:** El setup básico toma ~4 sesiones, personalizaciones +3 sesiones

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Puedo usar PDFs escaneados?**
R: Sí, pero la calidad será peor. Idealmente PDFs nativos.

**P: ¿Necesito GPU?**
R: No, funciona en CPU. GPU es MUCHO más rápido pero no es obligatorio.

**P: ¿Cuántos PDFs necesito?**
R: Mínimo 3 de buena calidad. Entre más, mejor (pero espacio en BD).

**P: ¿Puedo usar modelos locales?**
R: Sí. OpenAI cuesta dinero, pero ollama/llama2 son gratis.

---

## 🎯 OBJETIVO FINAL

Un chatbot inteligente que:
1. ✅ Lee tus PDFs
2. ✅ Entiende preguntas
3. ✅ Busca respuestas relevantes en los docs
4. ✅ Genera respuestas coherentes
5. ✅ Tiene interfaz amigable
6. ✅ Mantiene historial de chat

---

## 📞 CONTACTO/DUDAS

Si tienes dudas:
- Revisa `PLAN_EJECUCION.md` para detalles
- Revisa `RESUMEN_CONCEPTOS.md` para teoría
- Pregunta al profe en clase o por email

¡A PROGRAMAR! 🚀

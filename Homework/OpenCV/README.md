# 🖼️ OpenCV y Visión Computacional - Tutorial Completo

## 📚 ¿Qué vas a aprender?

Este proyecto te enseña **visión computacional** paso a paso, desde conceptos básicos con OpenCV hasta entender cómo funciona YOLO para detección de objetos.

## 🗂️ Archivos en este proyecto:

### 1. `app.py` - Tutorial Básico de OpenCV
**Lo que hace:**
- ✅ Carga imágenes (archivo, cámara, o ejemplo generado)
- ✅ Redimensiona imágenes
- ✅ Convierte a escala de grises  
- ✅ Aplica desenfoque
- ✅ Detecta bordes
- ✅ Muestra comparación visual de todas las transformaciones

**Conceptos que aprenderás:**
- Matrices de píxeles (2D para B&N, 3D para color)
- Operaciones básicas de OpenCV
- Preprocesamiento de imágenes para ML

### 2. `deteccion_formas.py` - Detección de Formas Geométricas  
**Lo que hace:**
- 🔍 Detecta automáticamente formas geométricas
- 🏷️ Las clasifica (triángulo, cuadrado, círculo, etc.)
- 📊 Calcula áreas y cuenta vértices
- 🎨 Dibuja bounding boxes y etiquetas

**Conceptos que aprenderás:**
- Detección de contornos
- Clasificación automática de objetos
- Aproximación poligonal
- Base para entender detección de objetos

### 3. `simulador_yolo.py` - Simulador de YOLO
**Lo que hace:**
- 🎯 Simula cómo funciona YOLO internamente
- 🚗 Detecta múltiples objetos (persona, carro, bicicleta, etc.)
- 📈 Filtra por confianza mínima
- 📊 Genera estadísticas de detección
- 🎨 Dibuja bounding boxes con etiquetas profesionales

**Conceptos que aprenderás:**
- Cómo YOLO procesa múltiples objetos
- Sistema de confianza/score
- Filtrado de detecciones
- Visualización profesional de resultados

## 🚀 Cómo ejecutar:

```bash
# Activar entorno virtual (ya está configurado)
.venv/Scripts/Activate.ps1

# Ejecutar tutorial básico
python Homework/OpenCV/app.py

# Ejecutar detección de formas
python Homework/OpenCV/deteccion_formas.py

# Ejecutar simulador YOLO
python Homework/OpenCV/simulador_yolo.py

# O usar el menú principal
python Homework/OpenCV/menu_principal.py
```

## 📋 Orden recomendado de estudio:

1. **`app.py`** → Fundamentos básicos
2. **`deteccion_formas.py`** → Detección de objetos simples  
3. **`simulador_yolo.py`** → Entender cómo funciona YOLO

## 🎯 Conectando con las clases:

### De la Tutoría 10:
- ✅ Operaciones básicas con OpenCV
- ✅ Matrices de píxeles y canales de color
- ✅ Transformaciones geométricas
- ✅ Detección de bordes

### De la Tutoría 11:
- ✅ Concepto de YOLO y detección de objetos
- ✅ Scraping de imágenes (proyecto compartido por el profesor)
- ✅ Preparación para proyecto final

## 🔗 Próximos pasos:

1. **Practicar estos ejemplos** hasta dominarlos
2. **Descargar el proyecto YOLO** que compartió el profesor
3. **Decidir si tu proyecto final** será de visión computacional
4. **Experimentar con tus propias imágenes**

## 💡 Consejos del profesor:

> *"No se enfoquen en memorizar el código. Lo importante es entender los conceptos y saber contar una historia con los datos. La IA puede generar código, pero la capacidad de análisis es lo que los hará buenos científicos de datos."*

## 🆘 ¿Problemas?

- **No se abre la cámara**: Usa la opción 1 (imagen de ejemplo)
- **Error al cargar imagen**: Verifica que la ruta sea correcta  
- **Ventanas no aparecen**: Presiona cualquier tecla para continuar
- **OpenCV no instalado**: Ya está instalado en tu entorno virtual

---

**¡Ahora estás listo para dominar la visión computacional! 🚀**
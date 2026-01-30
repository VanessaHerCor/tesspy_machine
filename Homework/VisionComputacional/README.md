# 📚 GUÍA RÁPIDA - VISIÓN COMPUTACIONAL CON YOLO

## ✅ ARCHIVOS CREADOS EN TU CARPETA

Tu carpeta `VisionComputacional` ahora tiene:

```
VisionComputacional/
├── download_custom_images.py    ← Descarga imágenes automáticamente
├── unificar_nombres.py          ← Unifica nombres (guitar/guitarra → guitar)
├── encontrar_duplicados.py      ← Detecta y elimina duplicados
├── balancear_dataset.py         ← Balancea train/valid (80/20)
├── auto_label.py                ← Etiqueta imágenes automáticamente
├── clean_empty_labels.py        ← Limpia imágenes sin detecciones
├── train_custom_model.py        ← Entrena el modelo YOLO
├── main.py                      ← Usa el modelo en imágenes
├── app.py                       ← Detección en tiempo real (cámara)
├── requirements.txt             ← Librerías necesarias
└── dataset/                     ← Se crea automáticamente
    ├── train/
    │   ├── images/  (80% de las imágenes)
    │   └── labels/  (etiquetas)
    └── valid/
        ├── images/  (20% de las imágenes)
        └── labels/  (etiquetas)
```

---

## 🚀 CÓMO EJECUTAR - PASO A PASO

### **PASO 1: Instalar dependencias (una sola vez)**
```powershell
cd C:\Users\Vanessa-Prevrenal\Desktop\tesspy_machine\Homework\VisionComputacional
pip install -r requirements.txt
```

### **PASO 2: Descargar imágenes**
```powershell
python download_custom_images.py
```

Te preguntará:
```
¿Qué objeto quieres buscar? guitar
¿Cuántas imágenes quieres? 100
```

**Resultado:** Las imágenes se guardan automáticamente en `dataset/train/images` y `dataset/valid/images`

### **PASO 3: Unificar nombres (OPCIONAL - solo si descargaste con diferente idioma)**
```powershell
python unificar_nombres.py
```

**Resultado:** Convierte guitarra_* → guitar_* sin conflictos

### **PASO 4: Eliminar duplicados (OPCIONAL pero recomendado)**
```powershell
python encontrar_duplicados.py
```

Te preguntará qué tipo de duplicados buscar (exactos o similares)

**Resultado:** Dataset limpio sin imágenes repetidas

### **PASO 5: Balancear dataset (RECOMENDADO)**
```powershell
python balancear_dataset.py
```

**Resultado:** Ajusta automáticamente a 80% train y 20% valid

### **PASO 6: Etiquetar imágenes automáticamente**
```powershell
python auto_label.py
```

**Resultado:** Crea carpetas `dataset/train/labels` y `dataset/valid/labels` con archivos `.txt`

### **PASO 7: Limpiar etiquetas vacías**
```powershell
python clean_empty_labels.py
```

**Resultado:** Elimina imágenes que YOLO no pudo detectar (calidad baja, borrosas, etc.)

---

## 📝 ¿QUÉ HACE CADA ARCHIVO?

### **download_custom_images.py**
- 🔍 Busca imágenes en DuckDuckGo
- ⬇️ Las descarga automáticamente
- 📁 Las organiza en entrenamiento (80%) y validación (20%)
- ✅ No necesita API key

### **unificar_nombres.py**
- 🔄 Renombra inteligentemente guitarra_* → guitar_*
- 🚫 Evita conflictos de nombres automáticamente
- 📊 Útil cuando descargas con diferente idioma

### **encontrar_duplicados.py**
- 🔍 Detecta imágenes duplicadas (exactas y similares)
- 🗑️ Elimina automáticamente con confirmación
- 🎯 Mejora calidad del dataset (evita overfitting)

### **balancear_dataset.py**
- ⚖️ Balancea automáticamente train/valid (80/20)
- 🔁 Mueve imágenes y etiquetas con confirmación
- ✅ Evita sesgo por validación muy pequeña

### **auto_label.py**
- 🤖 Usa modelo YOLO para detectar objetos
- 📝 Crea archivos `.txt` con coordenadas del objeto
- 🏷️ Etiqueta automáticamente sin dibujar cajas manualmente
- ⚡ Rápido y eficiente

### **clean_empty_labels.py**
- 🧹 Elimina imágenes que YOLO no pudo etiquetar
- 🎯 Mejora la calidad del dataset
- ✅ Evita que el modelo se entrene con basura
- 📊 Muestra cuántas guardó/eliminó
---

## 🎓 CONCEPTOS CLAVE QUE NECESITAS SABER

### **¿Qué es un Dataset?**
Un conjunto de datos (imágenes) organizados para entrenar el modelo.
- **Entrenamiento (80%):** El modelo aprende de estas
- **Validación (20%):** El modelo se prueba con estas

### **¿Qué es una Etiqueta?**
Un archivo `.txt` que dice: "En esta imagen está X objeto en estas coordenadas"

**Formato:**
```
0 0.5 0.5 0.3 0.4
```
- `0` = clase (1er objeto)
- `0.5` = posición X del centro (normalizado 0-1)
- `0.5` = posición Y del centro
- `0.3` = ancho del objeto
- `0.4` = alto del objeto

### **¿Qué es Fine-tuning?**
Reutilizar un modelo ya entrenado (YOLO) para aprender nuevos objetos.
- ✅ Mucho más rápido que entrenar desde cero
- ✅ Necesita menos datos
- ✅ Mejor precisión

---

## 🔧 TROUBLESHOOTING (Problemas comunes)

### ❌ "No se encontró módulo X"
**Solución:** Instalar las dependencias
```powershell
pip install -r requirements.txt
```

### ❌ "Se descargaron imágenes malas"
**Solución:** Elimina manualmente las que no sirvan de la carpeta `dataset/train/images`

### ❌ "No detectó el objeto"
**Posibles causas:**
1. Las imágenes no tienen el objeto
2. El nombre del objeto es muy genérico
3. Probar con otro objeto diferente

---

## 📚 PRÓXIMOS PASOS (Para después de hoy)

1. ✅ Descargar imágenes (`download_custom_images.py`)
2. ✅ Unificar nombres (`unificar_nombres.py`) *(opcional)*
3. ✅ Eliminar duplicados (`encontrar_duplicados.py`) *(recomendado)*
4. ✅ Balancear dataset (`balancear_dataset.py`) *(80/20)*
5. ✅ Etiquetar imágenes (`auto_label.py`)
6. ✅ Limpiar vacíos (`clean_empty_labels.py`)
7. 🔜 Entrenar modelo (`train_custom_model.py`)
8. 🔜 Probar con cámara (`main.py`)

---

## 💡 TIPS PARA BUENOS RESULTADOS

✅ **Descargar entre 50-100 imágenes por objeto**
- 30-50 para ver resultados rápido hoy
- 70+ para mejor precisión

✅ **Usar nombres en inglés**
- "cat" es mejor que "gato"
- "electrical outlet" es mejor que "enchufe"

✅ **Revisar las imágenes descargadas**
- Elimina las que no sean lo que buscas
- Imagina mal = modelo mal

✅ **Ser específico**
- "red car" es mejor que "car"
- "standing dog" es mejor que "dog"

---

## 🎯 RESUMEN FINAL

| Archivo | Qué hace | Cuándo ejecutar |
|---------|----------|-----------------|
| `download_custom_images.py` | Descarga imágenes | 1️⃣ Primero |
| `unificar_nombres.py` | Unifica nombres | 2️⃣ Opcional |
| `encontrar_duplicados.py` | Elimina duplicados | 3️⃣ Recomendado |
| `balancear_dataset.py` | Balancea 80/20 | 4️⃣ Antes de etiquetar |
| `auto_label.py` | Etiqueta imágenes | 5️⃣ Después |
| `clean_empty_labels.py` | Limpia vacíos | 6️⃣ Después |
| `train_custom_model.py` | Entrena el modelo | 7️⃣ Al final |
| `main.py` | Prueba con cámara | 8️⃣ Después |

---

**¡Todos tus archivos tienen comentarios detallados en español!**
Abre los `.py` y verás explicaciones paso a paso de qué hace cada parte.

¿Preguntas? Pregunta sin miedo 😊

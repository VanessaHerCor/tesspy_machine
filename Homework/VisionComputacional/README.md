# 📚 GUÍA RÁPIDA - VISIÓN COMPUTACIONAL CON YOLO

## ✅ ARCHIVOS CREADOS EN TU CARPETA

Tu carpeta `VisionComputacional` ahora tiene:

```
VisionComputacional/
├── download_custom_images.py    ← Descarga imágenes automáticamente
├── auto_label.py                ← Etiqueta imágenes automáticamente
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
¿Qué objeto quieres buscar? cat
¿Cuántas imágenes quieres? 50
```

**Resultado:** Las imágenes se guardan automáticamente en `dataset/train/images` y `dataset/valid/images`

### **PASO 3: Etiquetar imágenes automáticamente**
```powershell
python auto_label.py
```

**Resultado:** Crea carpetas `dataset/train/labels` y `dataset/valid/labels` con archivos `.txt`

---

## 📝 ¿QUÉ HACE CADA ARCHIVO?

### **download_custom_images.py**
- 🔍 Busca imágenes en DuckDuckGo
- ⬇️ Las descarga automáticamente
- 📁 Las organiza en entrenamiento (80%) y validación (20%)
- ✅ No necesita API key

### **auto_label.py**
- 🤖 Usa modelo YOLO para detectar objetos
- 📝 Crea archivos `.txt` con coordenadas del objeto
- 🏷️ Etiqueta automáticamente sin dibujar cajas manualmente
- ⚡ Rápido y eficiente

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
2. ✅ Etiquetar imágenes (`auto_label.py`)
3. 🔜 Crear archivo `data.yaml`
4. 🔜 Entrenar modelo (`train_custom_model.py`)
5. 🔜 Probar con cámara (`main.py`)

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
| `auto_label.py` | Etiqueta imágenes | 2️⃣ Segundo |
| `train_custom_model.py` | Entrena el modelo | 3️⃣ Después (próxima clase) |
| `main.py` | Prueba con cámara | 4️⃣ Al final (próxima clase) |

---

**¡Todos tus archivos tienen comentarios detallados en español!**
Abre los `.py` y verás explicaciones paso a paso de qué hace cada parte.

¿Preguntas? Pregunta sin miedo 😊

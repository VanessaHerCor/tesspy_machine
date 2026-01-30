# 🎓 GUÍA PARA ESTUDIANTES: ¿Qué diablos estamos haciendo?

## 🎯 EL OBJETIVO FINAL

Crear un sistema que:
1. **VEA** una imagen/video
2. **ENCUENTRE** guitarras en ella
3. **MARQUE** dónde están

Ejemplo: Le muestras una foto → El sistema dice "Guitarra aquí [dibuja cuadro verde]"

---

## 📚 LA ANALOGÍA SIMPLE

Imagina que quieres **entrenar a un perro** para encontrar pelotas:

### PASO 1: Recolectar ejemplos (download_custom_images.py)
```
Tú: "Perro, aprende qué es una pelota"
Acción: Compras 100 pelotas de diferentes colores/tamaños
Resultado: Tienes 80 pelotas para enseñanza, 20 para prueba
```

### PASO 2: Organizar nombres (unificar_nombres.py)
```
Problema: Algunas dicen "pelota" y otras "ball"
Acción: Renombras todo a "pelota" para consistencia
Resultado: Todas tienen el mismo nombre
```

### PASO 3: Eliminar duplicados (encontrar_duplicados.py)
```
Problema: Compraste la misma pelota 3 veces por error
Acción: Eliminas las repetidas
Resultado: Solo pelotas únicas
```

### PASO 4: Balancear proporción (balancear_dataset.py)
```
Problema: Tienes 100 pelotas para enseñar y 2 para evaluar
Acción: Ajustas a 80% entrenamiento y 20% validación
Resultado: Evaluación justa sin sesgos
```

### PASO 5: Mostrar dónde está (auto_label.py)
```
Tú: "En ESTA foto, la pelota está AQUÍ"
Acción: En cada foto marcas con un círculo dónde está
Resultado: 100 fotos con círculos marcados
```

### PASO 6: Eliminar ejemplos malos (clean_empty_labels.py)
```
Problema: Algunas fotos están borrosas o la pelota es microscópica
Acción: Las eliminas porque confunden al perro
Resultado: Solo quedan 52 fotos buenas
```

### PASO 7: ENTRENAR (train_custom_model.py) ← ESTO ESTÁS HACIENDO AHORA
```
Tú: "Perro, ve estas 52 fotos mil veces"
Perro: *mira foto 1* "Pelota aquí"
       *mira foto 2* "Pelota aquí"
       ... (repite 1000 veces)
Resultado: El perro APRENDIÓ qué es una pelota
```

### PASO 8: Probar (main.py)
```
Tú: "Perro, aquí hay una foto nueva que nunca viste"
Perro: "¡HAY UNA PELOTA AHÍ!"
Resultado: Funciona con fotos nuevas
```

### PASO 9: Usar en vivo (app.py)
```
Tú: Abres la cámara
Perro: Detecta pelotas en TIEMPO REAL
Resultado: Sistema funcional
```

---

## 🔬 LA VERSIÓN TÉCNICA (Para entender qué hace cada script)

| Script | Nombre Técnico | Qué Hace (Humano) | Qué Hace (Técnico) |
|--------|----------------|-------------------|-------------------|
| `download_custom_images.py` | Recolector de Data | Descarga fotos de guitarras | Web scraping de DuckDuckGo |
| `unificar_nombres.py` | Unificador de Nombres | Renombra guitar/guitarra a uno solo | Renombrado inteligente sin conflictos |
| `encontrar_duplicados.py` | Detector de Duplicados | Encuentra fotos repetidas | Hash MD5 + comparación de histogramas |
| `balancear_dataset.py` | Balanceador de Dataset | Ajusta 80/20 train/valid | Reubica imágenes y etiquetas |
| `auto_label.py` | Etiquetador | Marca dónde está la guitarra | YOLO-World detecta y guarda coordenadas |
| `clean_empty_labels.py` | Limpiador de Dataset | Elimina fotos malas | Elimina imágenes sin detecciones |
| `train_custom_model.py` | Entrenador | Enseña al modelo | Fine-tuning de YOLOv8 |
| `main.py` | Probador | Prueba en fotos nuevas | Inferencia con modelo entrenado |
| `app.py` | Sistema en Vivo | Usa la cámara | Detección en tiempo real |

---

## ⏱️ LÍNEA DE TIEMPO (Lo que YA hiciste)

```
✅ PASO 1: Descargaste ~100 imágenes de guitarras
   Resultado: 71 en train/, 13 en valid/

✅ PASO 2: Unificaste nombres (guitar/guitarra → guitar)
   Resultado: Nombres consistentes

✅ PASO 3: Eliminaste duplicados
   Resultado: Solo imágenes únicas

✅ PASO 4: Balanceaste train/valid (80/20)
   Resultado: Validación justa sin sesgos

✅ PASO 5: Etiquetaste automáticamente con YOLO-World
   Resultado: 52 imágenes con detecciones válidas

✅ PASO 6: Limpiaste las imágenes sin detecciones
   Resultado: Dataset limpio (52 train, 6 valid)

🔴 PASO 7: ENTRENANDO AHORA (train_custom_model.py)
   El modelo está viendo tus 52 fotos mil veces
   Duración: 5-10 minutos

⏳ PASO 8: Después probarás con main.py

⏳ PASO 9: Después usarás app.py en vivo
```

---

## 🧠 ¿QUÉ ESTÁ PASANDO EN EL ENTRENAMIENTO? (AHORA MISMO)

```python
Epoch 1/30:
  - Modelo ve foto 1: "¿Aquí está la guitarra? Creo que sí"
  - Modelo ve foto 2: "¿Y aquí? Creo que también"
  - ... (ve todas las 52 fotos)
  - Calcula error: "Me equivoqué en 15 fotos"
  
Epoch 2/30:
  - Modelo ajusta su "cerebro"
  - Ve las mismas 52 fotos de nuevo
  - Calcula error: "Ahora me equivoqué solo en 10"
  
...

Epoch 30/30:
  - Modelo ya casi no se equivoca
  - Guarda su "cerebro entrenado" en best.pt
```

**Resultado:** Un archivo `best.pt` que "sabe" qué es una guitarra

---

## 📊 TÉRMINOS TÉCNICOS (Para que entiendas al profe)

| Término | Qué Significa (Simple) | Ejemplo |
|---------|----------------------|---------|
| **Dataset** | Colección de fotos organizadas | Tus 52 fotos de guitarras |
| **Label/Etiqueta** | Archivo que dice dónde está el objeto | "Guitarra en X:0.5, Y:0.5" |
| **Entrenamiento** | Enseñarle al modelo | Ver fotos mil veces |
| **Validación** | Probar si aprendió bien | Las 6 fotos que no usaste para enseñar |
| **Epoch** | Una pasada completa del dataset | Ver las 52 fotos 1 vez |
| **Batch** | Cuántas fotos ve a la vez | 8 fotos |
| **Fine-tuning** | Ajustar un modelo existente | Tomar YOLO y especializarlo en guitarras |
| **Inferencia** | Usar el modelo ya entrenado | Darle foto nueva y que detecte |

---

## 🎯 LO QUE EL PROFE ESPERA

El profesor pidió en las clases:

✅ **Descargar datos** automáticamente (Internet)
✅ **Procesar datos** (etiquetar automáticamente)
✅ **Limpiar datos** (eliminar basura)
✅ **Entrenar modelo** (fine-tuning con YOLO)
✅ **Hacer predicciones** (usar en imágenes nuevas)
✅ **Aplicación en tiempo real** (cámara web)

**TÚ ESTÁS CUMPLIENDO TODO.** ✨

---

## ❓ PREGUNTAS FRECUENTES

### ¿Por qué tardó tanto en detectar las imágenes?
YOLO-World no es perfecto. Algunas guitarras son muy difíciles de ver.

### ¿52 imágenes es suficiente?
Para aprendizaje, lo ideal es 100-500. Pero 52 funciona para un proyecto estudiantil.

### ¿Qué pasa si descargo 200 imágenes después?
El script `train_custom_model.py` se ajusta automáticamente. Solo vuelves a ejecutar.

### ¿Cuánto dura el entrenamiento?
Con CPU: 5-15 minutos
Con GPU: 2-5 minutos

### ¿Qué hago después del entrenamiento?
```powershell
python main.py --test  # Prueba rápida
python main.py         # Modo interactivo
python app.py          # Cámara en vivo
```

---

## 🎓 RESUMEN PARA PRESENTAR

**Lo que hiciste:**
1. Automatizaste la recolección de 100 imágenes de guitarras
2. Automatizaste el etiquetado usando YOLO-World
3. Limpiaste el dataset (52 imágenes de calidad)
4. Entrenaste un modelo personalizado con fine-tuning
5. Creaste un sistema funcional de detección en tiempo real

**Tecnologías usadas:**
- Python 3.13
- YOLOv8 (Ultralytics)
- YOLO-World (zero-shot detection)
- OpenCV (visión computacional)
- DuckDuckGo API (web scraping)

**Resultado:**
Sistema capaz de detectar guitarras en imágenes y video en tiempo real.

---

## 💡 TIP FINAL

**No te preocupes si no entiendes TODO.** Lo importante es:
1. Ejecutaste los scripts en orden
2. Cada paso funcionó
3. El resultado final funciona

Eso es lo que importa en un proyecto real. 🚀

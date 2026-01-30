# 🚀 GUÍA COMPLETA: CÓMO EJECUTAR TU PROYECTO

## Resumen de lo que tienes ahora

```
✅ download_custom_images.py    → Descargar imágenes
✅ unificar_nombres.py          → Unificar nombres (guitar/guitarra)
✅ encontrar_duplicados.py      → Eliminar duplicados
✅ balancear_dataset.py         → Balancear 80/20 (train/valid)
✅ auto_label.py                → Etiquetar automáticamente
✅ clean_empty_labels.py        → Limpiar etiquetas vacías
✅ train_custom_model.py        → Entrenar modelo
✅ main.py                      → Usar en imágenes individuales
✅ app.py                       → Detección en vivo (cámara)
✅ dataset/data.yaml            → Configuración (CORRECTO)
```

---

## ⚡ EJECUCIÓN PASO A PASO

### PASO 1: Descargar Imágenes (Si aún no lo hiciste)

```powershell
python download_custom_images.py
```

Responde a las preguntas:
```
¿Qué objeto quieres buscar? guitar
¿Cuántas imágenes quieres? 100
```

**Resultado:** Las imágenes en `dataset/train/images` y `dataset/valid/images`

---

### PASO 2: Unificar Nombres (OPCIONAL - solo si descargaste con diferente idioma)

```powershell
python unificar_nombres.py
```

**¿Qué hace?**
- Renombra inteligentemente guitarra_* → guitar_*
- Evita conflictos de nombres incrementando números

**Resultado:** Todas las imágenes con nombres consistentes

---

### PASO 3: Eliminar Duplicados (OPCIONAL pero RECOMENDADO)

```powershell
python encontrar_duplicados.py
```

**¿Qué hace?**
- Detecta imágenes EXACTAMENTE iguales (hash MD5)
- Detecta imágenes MUY parecidas (95%+ similares)
- Elimina duplicados con confirmación
- Mejora dataset (evita overfitting)

**Resultado:** Dataset sin imágenes repetidas

---

### PASO 4: Balancear Dataset (RECOMENDADO)

```powershell
python balancear_dataset.py
```

**¿Qué hace?**
- Ajusta automáticamente train/valid a 80/20
- Mueve imágenes y etiquetas con confirmación
- Evita sesgo por validación demasiado pequeña

**Resultado:** Dataset balanceado

---

### PASO 5: Etiquetar Automáticamente

```powershell
python auto_label.py
```

**Resultado:** Archivos `.txt` en `dataset/train/labels` y `dataset/valid/labels`

---

### PASO 6: Limpiar Etiquetas Vacías ⭐ IMPORTANTE

```powershell
python clean_empty_labels.py
```

**¿Qué hace?**
- Elimina imágenes que YOLO no detectó correctamente
- Son imágenes borrosas, muy pequeñas, o de mala calidad
- Mejora la calidad del dataset para entrenamiento

**Resultado:** Solo quedan imágenes con detecciones válidas

---

### PASO 7: ENTRENAR EL MODELO ⭐

```powershell
python train_custom_model.py
```

**¿Qué hace?**
- Detecta automáticamente cuántas imágenes tienes
- Ajusta parámetros (épocas, batch, patience) según cantidad
- Entrena YOLO con TUS imágenes
- Guarda el modelo entrenado

**Duración:** 5-15 minutos

**Resultado:** Modelo guardado en `runs/detect/train/weights/best.pt`

---

### PASO 8: USAR EL MODELO (Opción A - Interactivo)

```powershell
python main.py
```

**Menú interactivo:**
```
¿Qué deseas hacer?
1. Predecir en una imagen
2. Predecir en carpeta de imágenes
3. Salir

Elige (1-3): 1
Ruta de imagen: ruta/a/imagen.jpg
```

**Resultado:** Muestra dónde detectó el objeto

---

### PASO 8B: USAR EL MODELO (Opción B - Prueba Rápida)

```powershell
python main.py --test
```

**¿Qué hace?**
- Coge una imagen de validación automáticamente
- Muestra las detecciones

---

### PASO 9: DETECCIÓN EN VIVO (CÁMARA WEB)

```powershell
python app.py
```

**¿Qué ves?**
- Tu cámara en tiempo real
- Cajas alrededor de los objetos detectados
- FPS (velocidad de detección)

**Controles:**
```
SPACE → Capturar imagen (guarda como capture_YYYYMMDD_HHMMSS.jpg)
Q     → Salir
```

---

## 📊 ESTRUCTURA FINAL (Después de ejecutar TODO)

```
VisionComputacional/
├── download_custom_images.py      ✅
├── auto_label.py                  ✅
├── clean_empty_labels.py          ✅ NUEVO - Limpia dataset
├── train_custom_model.py          ✅ NUEVO
├── main.py                        ✅ NUEVO
├── app.py                         ✅ NUEVO
├── requirements.txt               ✅
├── README.md                      ✅
├── yolov8s-worldv2.pt            (modelo para etiquetar)
├── dataset/
│   ├── data.yaml                 ← CONFIGURACIÓN IMPORTANTE
│   ├── train/
│   │   ├── images/               (imágenes limpias)
│   │   └── labels/               (coordenadas del objeto)
│   └── valid/
│       ├── images/               (imágenes limpias)
│       └── labels/               (coordenadas del objeto)
│
├── runs/                          ← SE CREA AL ENTRENAR
│   └── detect/
│       └── train/
│           └── weights/
│               └── best.pt        ← TU MODELO ENTRENADO ⭐
│
└── capture_*.jpg                 ← IMÁGENES CAPTURADAS
```

---

## 🎓 Explicación Educativa: ¿Qué hace cada script?

### `download_custom_images.py` - EL RECOLECTOR
```
Tú:  "Necesito 100 fotos de guitarras"
↓
Script: "Voy a DuckDuckGo, busco 'guitar', descargo 100"
↓
Resultado: Imágenes en dataset/train/images y dataset/valid/images
```

### `auto_label.py` - EL ANOTADOR
```
Script: "Tengo 100 fotos. Ahora marcaré dónde está la guitarra"
↓
YOLO-World: "En esta foto, la guitarra está AQUÍ [dibuja caja]"
↓
Resultado: Archivos .txt con coordenadas en dataset/*/labels/
```
clean_empty_labels.py` - EL LIMPIADOR
```
Script: "Algunas imágenes no tienen detecciones"
↓
Script: "Elimino 19 imágenes borrosas/malas de train"
↓
Resultado: Solo imágenes de calidad en el dataset
```

### `
### `train_custom_model.py` - EL MAESTRO
```
Script: "Tengo 80 fotos etiquetadas para enseñanza"
↓
YOLO: "Voy a ver mil veces estas fotos... 
        Foto 1: guitarra está aquí
        Foto 2: guitarra está acá
        ..."
↓
YOLO aprende: "Reconozco patrones. Ahora SÉ dónde está una guitarra"
↓
Resultado: Modelo guardado (best.pt)
```

### `main.py` - EL VERIFICADOR
```
Script: "Tengo el modelo entrenado. Déjame probarlo en imágenes nuevas"
↓
Usuario: "Aquí hay una imagen que el modelo NUNCA vio"
↓
Modelo: "Basándome en lo que aprendí... aquí hay una guitarra"
↓
Resultado: Imagen con cuadro verde alrededor del objeto
```

### `app.py` - EL DETECTOR EN VIVO
```
Script: "Abre la cámara"
↓
Tu cámara: "Tengo 30 frames por segundo (vídeo en vivo)"
↓
Modelo: "En CADA frame... aquí, aquí, aquí está la guitarra"
↓
Resultado: Ves tu cámara con detecciones en TIEMPO REAL
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### "ModuleNotFoundError: No module named 'ultralytics'"
```powershell
pip install --upgrade ultralytics torch
```

### "No encontré el modelo en runs/detect/train/weights/best.pt"
Solución: Primero ejecuta `python train_custom_model.py`

### "No se pudo acceder a la cámara web"
- Verifica que tienes cámara conectada
- Cierra otras aplicaciones que usen cámara (Zoom, Teams, etc.)
- Reinicia el script

### El entrenamiento se demora MUCHO
- Es normal con +200 imágenes
- Puedes reducir `epochs=50` a `epochs=25` en train_custom_model.py
- O aumentar `batch=16` a `batch=32` si tienes mucha RAM

---

## ✅ CHECKLIST FINAL

Cuando hayas hecho TODO, checkea esto:

- [ ] Ejecuté `python download_custom_images.py`
- [ ] Ejecuté `python auto_label.py`
- [ ] Ejecuté `python train_custom_model.py` (esperé a que termine)
- [ ] Ejecuté `python main.py --test` (prueba rápida)
- [ ] Ejecuté `python main.py` y probé predicción en imagen
- [ ] Ejecuté `python app.py` y detecté en vivo
- [ ] Mi modelo detecta correctamente el objeto

✅ Si todo esto funciona, **¡TU PROYECTO ESTÁ COMPLETO!**

---

## 🎯 RESUMEN PARA EL PROFE

Tu proyecto cumple con:

✅ **Descargar datos** (imágenes de internet automáticamente)
✅ **Procesar datos** (etiquetar automáticamente)
✅ **Entrenar modelo** (fine-tuning con YOLO)
✅ **Hacer predicciones** (usar en imágenes nuevas)
✅ **Aplicación en tiempo real** (cámara web en vivo)

Eso es exactamente lo que pidió el Profesor en clase. 🎉

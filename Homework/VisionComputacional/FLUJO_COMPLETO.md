# 📋 FLUJO COMPLETO DEL PROYECTO

## ✅ ORDEN CORRECTO DE EJECUCIÓN

```
1️⃣ python py_scripts/download_custom_images.py
   └─ Descarga imágenes de Internet (guitar, cat, etc.)
   
2️⃣ python py_scripts/unificar_nombres.py (OPCIONAL)
   └─ Solo si descargaste con diferente idioma (guitar/guitarra)
   
3️⃣ python py_scripts/encontrar_duplicados.py (RECOMENDADO)
   └─ Elimina imágenes repetidas (evita overfitting)
   
4️⃣ python py_scripts/balancear_dataset.py (RECOMENDADO)
   └─ Ajusta train/valid a 80/20 automáticamente
   
5️⃣ python py_scripts/auto_label.py
   └─ Etiqueta automáticamente usando YOLO-World
   
6️⃣ python py_scripts/relabel_empty.py (OPCIONAL)
   └─ Re-etiqueta imágenes que quedaron sin labels (sin eliminar)
   
7️⃣ python py_scripts/clean_empty_labels.py
   └─ Elimina imágenes que YOLO no pudo detectar
   
8️⃣ python py_scripts/train_custom_model.py
   └─ Entrena el modelo con tu dataset limpio
   └─ ✨ REUTILIZA modelo anterior si existe (Transfer Learning automático)
   
9️⃣ python main.py --test
   └─ Prueba el modelo en imágenes de validación
   
🔟 python app.py
   └─ Usa el modelo en tiempo real con tu cámara
```

---

## 🚀 **IMPORTANTE: Transfer Learning Automático**

Ahora el script detecta automáticamente:

- **Si es tu PRIMER entrenamiento:** Carga `yolov8s.pt` (modelo base)
- **Si ya entrenaste antes:** Carga `runs/detect/train/weights/best.pt` (reutiliza aprendizaje anterior) ✨

**Esto significa:**
- ✅ Si descargas imágenes nuevas y ejecutas el script de nuevo, será MEJOR
- ✅ La precisión mejora con más datos
- ✅ No pierdes el trabajo anterior

---

## ⚠️ ERRORES COMUNES

### ❌ ERROR 1: Olvidar auto_label.py
```
python py_scripts/download_custom_images.py
python py_scripts/clean_empty_labels.py  ← ¡FALTAN LAS ETIQUETAS!
python py_scripts/train_custom_model.py  ← FALLA
```

**✅ CORRECTO:**
```
python py_scripts/download_custom_images.py
python py_scripts/auto_label.py           ← PRIMERO ETIQUETAR
python py_scripts/relabel_empty.py        ← RELLENAR VACÍOS (opcional)
python py_scripts/clean_empty_labels.py
python py_scripts/train_custom_model.py
```

### ❌ ERROR 2: Mezclar idiomas sin unificar
```
dataset/train/images/
├── guitar_train_0.jpg      ← detecta "guitar"
├── guitar_train_1.jpg
├── guitarra_train_0.jpg    ← detecta "guitarra"
└── guitarra_train_1.jpg
```

**Resultado:** Modelo confundido (2 clases en lugar de 1)

**✅ SOLUCIÓN:**
```powershell
python py_scripts/unificar_nombres.py  # Convierte todo a "guitar"
python py_scripts/auto_label.py        # Re-etiqueta con clase consistente
```

### ❌ ERROR 3: No eliminar duplicados
```
dataset/train/images/
├── guitar_train_0.jpg
├── guitar_train_1.jpg  ← IGUAL a train_0
├── guitar_train_2.jpg  ← IGUAL a train_0
```

**Resultado:** Overfitting (memoriza esas 3 imágenes)

**✅ SOLUCIÓN:**
```powershell
python py_scripts/encontrar_duplicados.py  # Elimina automáticamente
```

### ❌ ERROR 4: No balancear train/valid
```
Train: 105 imágenes
Valid: 2 imágenes
```

**Resultado:** Validación sesgada y métricas falsas

**✅ SOLUCIÓN:**
```powershell
python py_scripts/balancear_dataset.py  # Ajusta a 80/20
```

Antes de ejecutar `python train_custom_model.py`, verifica:

- [ ] ✅ Tienes al menos 30-50 imágenes únicas
- [ ] ✅ Todas las imágenes tienen el MISMO prefijo (guitar_, cat_, etc.)
- [ ] ✅ NO hay duplicados (usa `encontrar_duplicados.py`)
- [ ] ✅ Train/Valid está balanceado (usa `balancear_dataset.py`)
- [ ] ✅ Todas las imágenes tienen etiquetas `.txt`
- [ ] ✅ Las etiquetas NO están vacías
- [ ] ✅ El archivo `dataset/data.yaml` existe

---

## 📊 MÉTRICAS ESPERADAS

| Imágenes | Precisión Esperada | Tiempo Entrenamiento |
|----------|-------------------|---------------------|
| 30-50    | 70-80%            | 3-5 minutos         |
| 50-100   | 80-90%            | 5-10 minutos        |
| 100-300  | 90-95%            | 10-20 minutos       |
| 300+     | 95%+              | 20-40 minutos       |

**Tu resultado:** 95.6% con ~50 imágenes → ¡EXCELENTE! 🎉

---

## 🚀 PRÓXIMOS PASOS

Una vez entrenado:

1. **Probar en validación:**
   ```powershell
   python main.py --test
   ```

2. **Probar imagen específica:**
   ```powershell
   python main.py
   # Luego selecciona opción 1 y elige una imagen
   ```

3. **Usar en tiempo real:**
   ```powershell
   python app.py
   # Presiona ESPACIO para capturar
   # Presiona Q para salir
   ```

---

## 📚 ARCHIVOS DEL PROYECTO

```
VisionComputacional/
├── 🔧 Scripts de procesamiento
│   ├── download_custom_images.py    (Descarga)
│   ├── unificar_nombres.py          (Unifica)
│   ├── encontrar_duplicados.py      (Limpia duplicados)
│   ├── balancear_dataset.py         (Balancea 80/20)
│   ├── auto_label.py                (Etiqueta)
│   └── clean_empty_labels.py        (Limpia vacíos)
│
├── 🤖 Scripts de modelo
│   ├── train_custom_model.py        (Entrena)
│   ├── main.py                      (Predice)
│   └── app.py                       (Tiempo real)
│
├── 📖 Documentación
│   ├── README.md                    (Guía rápida)
│   ├── INSTRUCCIONES_COMPLETAS.md   (Paso a paso)
│   ├── GUIA_ESTUDIANTE.md           (Para entender conceptos)
│   └── FLUJO_COMPLETO.md            (Este archivo)
│
└── 📁 Dataset
    └── dataset/
        ├── data.yaml                (Configuración YOLO)
        ├── train/
        │   ├── images/              (80% imágenes)
        │   └── labels/              (Etiquetas .txt)
        └── valid/
            ├── images/              (20% imágenes)
            └── labels/              (Etiquetas .txt)
```

---

## 💡 TIPS PROFESIONALES

1. **Más imágenes = Mejor modelo**
   - Mínimo: 30 imágenes
   - Recomendado: 100-300 imágenes
   - Profesional: 1000+ imágenes

2. **Calidad > Cantidad**
   - Mejor 50 imágenes buenas que 200 malas
   - Usa `encontrar_duplicados.py` regularmente

3. **Diversidad es clave**
   - Diferentes ángulos
   - Diferentes iluminaciones
   - Diferentes fondos
   - Diferentes tamaños

4. **Re-entrenar cuando:**
   - Agregas más imágenes
   - El modelo falla en casos específicos
   - Quieres detectar nuevos objetos

---

## 🎓 RESUMEN PARA PRESENTAR AL PROFE

**Proyecto:** Detector de guitarras con YOLO

**Proceso:**
1. ✅ Automatización de descarga de dataset (DuckDuckGo API)
2. ✅ Limpieza de datos (unificación y deduplicación)
3. ✅ Etiquetado automático (YOLO-World zero-shot)
4. ✅ Validación de calidad (eliminación de etiquetas vacías)
5. ✅ Entrenamiento con fine-tuning (YOLOv8s)
6. ✅ Ajuste dinámico de hiperparámetros según tamaño del dataset
7. ✅ Sistema funcional de predicción e inferencia en tiempo real

**Tecnologías:**
- Python 3.13
- YOLOv8 (Ultralytics)
- YOLO-World (zero-shot detection)
- OpenCV (procesamiento de video)
- DuckDuckGo Search (web scraping sin API key)

**Métricas:**
- Precisión: 95.6%
- Dataset: 58 imágenes (52 train, 6 valid)
- Tiempo entrenamiento: ~5 minutos

**Resultado:**
Sistema capaz de detectar guitarras en imágenes y video en tiempo real con alta precisión. 🚀

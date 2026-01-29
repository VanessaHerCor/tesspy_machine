# 📋 GUÍA COMPLETA: Proyecto Integrador YOLO - Tutoría 14 & 15

## 🎯 **¿QUÉ TIENES QUE HACER HOY?**

El profe dejó este proyecto integrador para que apliques **fine-tuning** (personalización) de YOLO con tus propios objetos. Esto significa:
1. Elegir un objeto para detectar (enchufes, cajas de fusibles, banderas, etc.)
2. Conseguir imágenes (~30-50 fotos)
3. Etiquetarlas automáticamente
4. Entrenar el modelo YOLO
5. Probar el modelo personalizado

---

## 📚 **RESUMEN TUTORÍAS 14 & 15**

### **Tutoría 14: PyTest - Testing en Python** (Profesor Néstor Cardona)

**🎯 Objetivo:** Aprender a hacer pruebas unitarias con PyTest para validar que tu código funcione correctamente.

**Conceptos Clave:**

1. **¿Qué es PyTest?**
   - Framework de testing para Python
   - Sirve para validar que tus funciones/clases funcionen como esperabas
   - No interfiere con tu aplicación (es independiente)

2. **Estructura de pruebas:**
   ```python
   # Archivo: test_calculadora.py
   import pytest
   from calculadora import Calculadora
   
   class TestOperacionesBasicas:
       def test_suma_positivos(self, calculadora_limpia):
           # Arrange: Preparar datos
           a, b = 5, 3
           
           # Act: Ejecutar función
           resultado = calculadora_limpia.sumar(a, b)
           
           # Assert: Validar resultado
           assert resultado == 8
           assert len(calculadora_limpia.historial) == 1
   ```

3. **Fixtures:**
   - Son instancias reutilizables para tus tests
   - Ejemplo: `calculadora_limpia` es una fixture que crea una calculadora nueva para cada test

4. **Parametrización:**
   ```python
   @pytest.mark.parametrize("a, b, esperado", [
       (1, 2, 3),
       (5, 5, 10),
       (-1, 1, 0),
   ])
   def test_suma_parametrizada(self, calculadora, a, b, esperado):
       assert calculadora.sumar(a, b) == esperado
   ```
   - Ejecuta el mismo test con diferentes conjuntos de datos

5. **Marcadores (Markers):**
   - `@pytest.mark.slow` - Para pruebas que tardan mucho
   - `@pytest.mark.unit` - Pruebas unitarias
   - `@pytest.mark.integration` - Pruebas de integración
   - Sirven para filtrar qué pruebas ejecutar

6. **Ejecución:**
   ```bash
   # Correr todos los tests
   pytest
   
   # Correr solo tests unitarios
   pytest -m unit
   
   # Excluir tests lentos
   pytest -m "not slow"
   ```

7. **Cobertura:**
   - Objetivo: ~80% de cobertura
   - Indica qué porcentaje de tu código está siendo testeado

**📝 Consejos del profe:**
- Los tests NO dependen de tu aplicación principal
- Valida: resultados esperados, excepciones, tipos de datos
- Agrupa tests relacionados en clases
- Usa nombres descriptivos: `test_suma_con_numeros_positivos`

---

### **Tutoría 15: YOLO - Fine-Tuning Modelos** (Profesor Yolo)

**🎯 Objetivo:** Entrenar YOLO para detectar objetos personalizados usando modelos pre-entrenados.

**Conceptos Clave:**

1. **¿Qué es Fine-Tuning?**
   - **NO** entrenar un modelo desde cero (carísimo, lento)
   - **SÍ** tomar un modelo ya entrenado (YOLOv8) y personalizarlo
   - El profe dijo: *"coger un modelo que ya previamente alguien ha hecho"*
   - Ventajas:
     - Barato (computacionalmente)
     - Rápido (minutos vs días)
     - Preciso (aprovecha el conocimiento del modelo base)

2. **YOLO sigue detectando 80 objetos por defecto:**
   - Cuando entrenas con "fusibles", YOLO aprende a detectar fusibles
   - PERO también sigue detectando personas, celulares, laptops, etc.
   - Es mixto: tu objeto nuevo + los 80 objetos originales

3. **Biblioteca Ultralytics:**
   - Framework para usar YOLO en Python
   - Muy simple de usar:
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8s.pt')  # Cargar pre-entrenado
   model.train(data='dataset/data.yaml', epochs=10)  # Entrenar
   results = model.predict('imagen.jpg')  # Detectar
   ```

4. **Estructura de Entrenamiento:**
   - **Épocas:** Cantidad de veces que el modelo revisa todas las imágenes
     - Más épocas = mejor precisión (hasta cierto punto)
     - Profe usó 10 épocas (demo rápida)
     - Recomendado: 50-100 para producción
   
   - **Batch Size:** Cuántas imágenes procesa a la vez
     - batch=16: Procesa 16 imágenes por iteración
     - Si tienes poca RAM, usa batch=8 o batch=4
   
   - **Imagen Size (imgsz):** Resolución de entrenamiento
     - 640x640 (estándar)
     - Si tus objetos son pequeños, usa 1280

5. **Device (CPU vs GPU):**
   - `device='cpu'` - Usa procesador (más lento pero funciona en cualquier PC)
   - `device='gpu'` - Usa tarjeta gráfica (mucho más rápido)
   - `device='auto'` - YOLO decide automáticamente

6. **Exist_ok=True:**
   - Si el modelo ya existe, no lo re-entrena (ahorra tiempo)
   - Útil para no perder progreso si algo falla

**⚠️ Problemas Comunes (discutidos en clase):**

| Problema | Solución del Profe |
|----------|-------------------|
| María no pudo instalar ultralytics | Usar entorno virtual, ejecutar desde terminal |
| Imágenes de Google no relevantes | Descargar manualmente o buscar en inglés |
| Figuras geométricas no funcionan | YOLO-World no entiende conceptos abstractos sin datos específicos |
| Kernel/IDE no ejecuta bien | **SIEMPRE ejecutar desde terminal:** `python src/main.py` |

7. **Auto-Label con YOLO-World:**
   - Usa un modelo avanzado (yolov8s-worldv2.pt)
   - Lee el nombre del archivo para saber qué buscar
   - Ejemplo: `electrical_outlet_train_5.jpg` → busca "electrical outlet"
   - Genera archivos .txt con coordenadas de las cajas

8. **Security.py (Opcional - Bonus):**
   - Define una zona restringida
   - Detecta objetos prohibidos (celular, billetera)
   - Captura screenshots del "intruso"
   - Muy bacano para proyectos avanzados

**📝 Consejos del profe:**
- *"Siempre ejecuten desde terminal con `python archivo.py`, NO con el play de VSCode"*
- *"Si el scraper da imágenes malas, descarguen 30-40 manualmente, es válido"*
- *"Fine-tuning es lo que usan TODAS las empresas, nadie entrena desde cero"*
- *"El modelo NO olvida los 80 objetos, solo aprende uno nuevo"*

---

## 🔗 **CONEXIÓN: CLASES ↔ PROYECTO**

### **Del Profe → Al Código:**

| Concepto de Clase | Archivo del Proyecto | Explicación |
|-------------------|----------------------|-------------|
| "Buscar imágenes en Google" | `download_custom_images.py` | Usa DuckDuckGo para descargar imágenes automáticamente (80% train, 20% valid) |
| "Auto-etiquetar con YOLO-World" | `auto_label.py` | Lee el nombre del archivo, usa yolov8s-worldv2.pt para generar labels .txt |
| "Entrenar con fine-tuning" | `train_custom_model.py` | Carga yolov8s.pt, entrena 10 épocas, guarda en `custom_models/` |
| "Probar el modelo entrenado" | `test_custom_model.py` | Abre webcam, usa tu modelo personalizado, muestra detecciones |
| "Detección en tiempo real" | `main.py` | Procesa imágenes/webcam/video con yolov8n.pt (modelo base) |
| "Zona restringida bonus" | `security.py` | Define área prohibida, alerta objetos, captura screenshots |
| "Wrapper para YOLO" | `detector.py` | Clase simplificada para cargar modelo y hacer predicciones |

### **Flujo de Trabajo Completo:**

```
1. download_custom_images.py  →  Descarga ~50 imágenes
                ↓
2. auto_label.py              →  Genera etiquetas .txt automáticamente
                ↓
3. train_custom_model.py      →  Entrena modelo personalizado
                ↓
4. test_custom_model.py       →  Prueba modelo con webcam
                ↓
5. (Opcional) security.py     →  Aplicación de seguridad avanzada
```

---

## 🚀 **PLAN DE ACCIÓN PARA HOY**

### **Paso 1: Preparar Entorno (5 min)**

```bash
# 1. Activar entorno virtual
cd C:\Users\Vanessa-Prevrenal\Desktop\tesspy_machine
.venv\Scripts\activate

# 2. Ir a carpeta YOLO
cd Homework\YOLO\yolo-opencv-integration

# 3. Instalar dependencias (si no lo has hecho)
pip install ultralytics opencv-python numpy pillow matplotlib tqdm duckduckgo-search
```

### **Paso 2: Elegir Objeto a Detectar (2 min)**

**Ideas del profe:**
- ✅ Enchufes/tomacorrientes (electrical outlet)
- ✅ Cajas de fusibles (fuse box)
- ✅ Banderas de países (ej: "flags latin america")
- ✅ Objetos del hogar (remote control, coffee mug, etc.)

**❌ NO recomendado:**
- Figuras geométricas abstractas (YOLO-World no las entiende)
- Objetos demasiado genéricos

**Mi recomendación:** Empieza con algo concreto como "laptop", "phone charger" o "coffee mug".

### **Paso 3: Descargar Imágenes (10 min)**

```bash
python src/download_custom_images.py
```

**Te preguntará:**
- Objeto: `laptop` (ejemplo, búscalo en inglés)
- Cantidad: `50` (recomendado)

**⚠️ Si falla el scraper:**
- Descarga 30-40 imágenes manualmente de Google
- Guárdalas en `dataset/train/images/` y `dataset/valid/images/`
- Usa nombres descriptivos: `laptop_1.jpg`, `laptop_2.jpg`, etc.

### **Paso 4: Etiquetar Automáticamente (3 min)**

```bash
python src/auto_label.py
```

**¿Qué hace?**
- Lee las imágenes de `dataset/train/images/` y `dataset/valid/images/`
- Extrae el nombre del objeto del archivo (ej: `laptop_train_5.jpg` → "laptop")
- Usa YOLO-World para detectar el objeto
- Genera archivos .txt en `dataset/train/labels/` y `dataset/valid/labels/`

**Formato del .txt:**
```
0 0.512345 0.678901 0.234567 0.345678
│    │        │        │        │
│    └─────x──┴────y───┴───w────┴──h (coordenadas normalizadas 0-1)
└─ Clase (0 = tu objeto)
```

### **Paso 5: Entrenar Modelo (30-60 min)**

```bash
python src/train_custom_model.py
```

**⏱️ Tiempo estimado:**
- CPU: 30-60 minutos (10 épocas)
- GPU: 5-10 minutos

**¿Qué verás?**
```
Epoch | Loss/Box | Loss/Cls | Loss/DFL | Precision | Recall | mAP50
------|----------|----------|----------|-----------|--------|-------
  1/10 | 1.234   | 0.567   | 0.890   | 0.45     | 0.38  | 0.42
  2/10 | 0.987   | 0.432   | 0.765   | 0.62     | 0.55  | 0.59
  ...
 10/10 | 0.345   | 0.123   | 0.234   | 0.87     | 0.82  | 0.85
```

**Métricas importantes:**
- **Loss:** Debe bajar progresivamente
- **Precision:** Qué tan correcto es cuando detecta
- **Recall:** Qué tan bueno es encontrando objetos
- **mAP50:** Precisión promedio (> 0.7 es bueno)

**✅ Resultado:**
- Modelo guardado en: `custom_models/mi_entrenamiento/weights/best.pt`

### **Paso 6: Editar data.yaml (2 min)**

Abre `dataset/data.yaml` y cambia:

```yaml
# Cambiar ESTA línea:
path: C:/Users/LENOVO/OneDrive/Escritorio/Work/SoftTI/yolo-opencv-integration/dataset

# Por TU ruta absoluta:
path: C:/Users/Vanessa-Prevrenal/Desktop/tesspy_machine/Homework/YOLO/yolo-opencv-integration/dataset

# Y cambiar el nombre del objeto:
names:
  0: laptop  # Pon el nombre de TU objeto
```

### **Paso 7: Probar Modelo con Webcam (5 min)**

**ANTES de ejecutar, edita `src/test_custom_model.py`:**

Busca esta línea:
```python
model_path = os.path.join(base_dir, 'C:\\Users\\LENOVO\\OneDrive\\Escritorio\\Work\\custom_models\\mi_entrenamiento\\weights\\best.pt')
```

Cámbiala por:
```python
model_path = os.path.join(base_dir, '../custom_models/mi_entrenamiento/weights/best.pt')
```

Luego ejecuta:
```bash
python src/test_custom_model.py
```

**¿Qué verás?**
- Se abre tu webcam
- El modelo detecta TU objeto personalizado
- Presiona `q` para salir

### **Paso 8 (Opcional): Probar Security.py (5 min)**

```bash
python src/security.py
```

**¿Qué hace?**
- Define una zona roja (zona restringida)
- Detecta objetos prohibidos (celular, laptop, etc.)
- Captura screenshots en carpeta `adens/`
- Cuenta violaciones

---

## 🐛 **TROUBLESHOOTING**

### ❌ Error: "No module named 'ultralytics'"
```bash
pip install ultralytics
```

### ❌ Error: "No se encontró el modelo en..."
- Verifica que train_custom_model.py terminó correctamente
- Revisa la ruta en test_custom_model.py

### ❌ Error: "Failed to load image..."
- Borra imágenes corruptas del dataset
- Ejecuta de nuevo auto_label.py

### ❌ Auto-label no detecta nada
- Revisa que el nombre del archivo sea descriptivo
- Usa nombres en inglés (mejor precisión)
- Ejemplo: `laptop_train_1.jpg` en vez de `img001.jpg`

### ❌ "Camera could not be opened"
- Revisa permisos de cámara en Windows
- Cambia `cv2.VideoCapture(0)` por `cv2.VideoCapture(1)`

### ❌ Entrenamiento muy lento
- Usa menos épocas: `epochs=5`
- Reduce batch: `batch=8`
- Usa menos imágenes (~30 en vez de 50)

---

## 📊 **ENTREGABLES ESPERADOS**

**Lo que debes tener al final:**

1. ✅ Dataset organizado:
   ```
   dataset/
   ├── train/
   │   ├── images/ (imágenes de entrenamiento)
   │   └── labels/ (etiquetas .txt)
   ├── valid/
   │   ├── images/ (imágenes de validación)
   │   └── labels/ (etiquetas .txt)
   └── data.yaml
   ```

2. ✅ Modelo entrenado:
   ```
   custom_models/
   └── mi_entrenamiento/
       └── weights/
           └── best.pt  ← Este es tu modelo
   ```

3. ✅ Evidencia de funcionamiento:
   - Screenshots del entrenamiento (métricas finales)
   - Video/captura probando con webcam
   - (Opcional) Screenshots de security.py

4. ✅ Código ejecutable:
   - Los scripts del profe funcionando
   - data.yaml con tu ruta
   - test_custom_model.py con tu ruta

---

## 🎓 **CONCLUSIONES CLAVE**

### De la Tutoría 14 (PyTest):
- Testing es ESENCIAL para código en producción
- Objetivo: ~80% de cobertura
- Separa lógica (src/) de tests (test/)
- Usa fixtures para instancias reutilizables
- Parametriza tests para probar múltiples casos

### De la Tutoría 15 (YOLO):
- **Fine-tuning >> Entrenar desde cero**
- YOLO mixto: detecta tus objetos + 80 clases originales
- Ultralytics hace todo super simple
- Auto-etiquetado funciona si nombras bien los archivos
- **SIEMPRE ejecutar desde terminal**

### Del Proyecto Integrador:
- Workflow: Descargar → Etiquetar → Entrenar → Probar
- 30-50 imágenes son suficientes
- 10 épocas para demo, 50+ para producción
- Security.py es opcional pero muy bacano
- El scraper puede fallar, manual es válido

---

## 📞 **SI TIENES DUDAS**

1. **Repasa las grabaciones** de las tutorías 14 y 15
2. **Revisa los comentarios** en cada archivo .py del proyecto
3. **Pregunta al profe mañana** (él dijo que revisa dudas)
4. **Experimenta:** El profe dijo *"los invito a que experimenten con eso"*

---

## ⏱️ **TIEMPO TOTAL ESTIMADO: 2-3 horas**

- Preparación: 10 min
- Descarga imágenes: 10 min
- Auto-label: 3 min
- Entrenamiento: 30-60 min
- Pruebas: 10 min
- Ajustes/fixes: 30 min
- (Opcional) Security: 10 min

---

**🚀 ¡ÉXITO EN TU PROYECTO! Recuerda ejecutar SIEMPRE desde terminal con `python src/archivo.py`**

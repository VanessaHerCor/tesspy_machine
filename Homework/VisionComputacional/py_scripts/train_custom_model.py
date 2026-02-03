# ============================================================
# ENTRENAMIENTO DE MODELO YOLO PERSONALIZADO
# ============================================================
# Este script entrena YOLO con tus imágenes descargadas
# ============================================================

from ultralytics import YOLO
import os
from pathlib import Path
import glob

def train_model():
    """
    Entrena un modelo YOLO con tus datos personalizados
    Con control interactivo sobre EarlyStopping
    """
    print("\n" + "=" * 60)
    print("🤖 ENTRENAMIENTO DE MODELO YOLO PERSONALIZADO")
    print("=" * 60)
    print("\n⚙️  MODO INTERACTIVO - Tú controlas cuándo parar")
    print("   Si EarlyStopping se activa, te preguntaré si continuar\n")
    
    # =====================================================
    # PASO 1: CONFIGURAR RUTAS
    # =====================================================
    # Obtener la carpeta raíz (subir un nivel desde py_scripts)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Ruta del archivo de configuración del dataset
    data_yaml = os.path.join(base_dir, 'dataset', 'data.yaml')
    
    # Verificar que el archivo data.yaml existe
    if not os.path.exists(data_yaml):
        print(f"❌ Error: No encontré {data_yaml}")
        print("   Primero ejecuta: python py_scripts/auto_label.py")
        return False
    
    print(f"✅ Archivo de configuración encontrado: {data_yaml}\n")
    
    # =====================================================
    # PASO 1.5: DETECTAR CANTIDAD DE IMÁGENES Y AJUSTAR PARÁMETROS
    # =====================================================
    train_images_dir = os.path.join(base_dir, 'dataset', 'train', 'images')
    train_images = glob.glob(os.path.join(train_images_dir, '*.jpg')) + \
                   glob.glob(os.path.join(train_images_dir, '*.png'))
    num_images = len(train_images)
    
    print(f"📊 Dataset detectado:")
    print(f"   Imágenes de entrenamiento: {num_images}")
    
    # Ajustar parámetros según cantidad de imágenes
    if num_images < 50:
        epochs = 50
        batch = 4
        patience_default = 20
        print(f"   ⚠️  Dataset pequeño (<50) - Parámetros conservadores")
    elif num_images < 100:
        epochs = 30
        batch = 8
        patience_default = 15
        print(f"   ✅ Dataset mediano (50-100) - Parámetros balanceados")
    elif num_images < 300:
        epochs = 50
        batch = 16
        patience_default = 10
        print(f"   ✅ Dataset bueno (100-300) - Parámetros óptimos")
    else:
        epochs = 100
        batch = 32
        patience_default = 10
        print(f"   🌟 Dataset grande (300+) - Parámetros agresivos")
    
    # PREGUNTARLE AL USUARIO POR PATIENCE
    print(f"\n⏸️  CONFIGURACIÓN DE EARLYSTOPPING")
    print(f"   Valor sugerido: {patience_default}")
    print(f"   (Más alto = más épocas antes de parar)")
    print(f"   (0 = desactivar EarlyStopping)")
    
    patience_input = input(f"\n   ¿Patience? (Enter para {patience_default}): ").strip()
    
    if patience_input == "":
        patience = patience_default
    else:
        try:
            patience = int(patience_input)
        except:
            patience = patience_default
    
    print(f"\n   ✅ Configuración final:")
    print(f"   - Épocas máximas: {epochs}")
    print(f"   - Batch size: {batch}")
    print(f"   - Patience: {patience}\n")
    
    # =====================================================
    # PASO 2: CARGAR EL MODELO BASE
    # =====================================================
    # PASO 2: CARGAR EL MODELO (TRANSFER LEARNING)
    # =====================================================
    # INTENTA CARGAR EL MODELO ENTRENADO ANTERIOR
    # Si existe, reutiliza el aprendizaje anterior (Transfer Learning)
    # Si no existe, carga el modelo base (primer entrenamiento)
    
    print("📦 Cargando modelo...")
    
    best_model_path = os.path.join(base_dir, 'runs', 'detect', 'train', 'weights', 'best.pt')
    base_model_path = os.path.join(base_dir, 'yolov8s.pt')
    
    try:
        if os.path.exists(best_model_path):
            # ✅ TRANSFER LEARNING: Reutilizar modelo anterior
            print(f"✅ Encontré modelo anterior: {best_model_path}")
            print("   Cargando modelo entrenado (Transfer Learning)...")
            model = YOLO(best_model_path)
            print("✅ Modelo cargado exitosamente")
            print("   💡 Esto reutilizará el aprendizaje anterior\n")
            resume_mode = True  # Para continuar desde donde quedó
        else:
            # 🟡 PRIMER ENTRENAMIENTO: Usar modelo base
            # YOLO pequeño (recomendado para inicio)
            # Otras opciones: 'yolov8m.pt' (mediano), 'yolov8l.pt' (grande)
            print(f"   Primer entrenamiento detectado")
            print("   Cargando modelo base YOLO8s...")
            model = YOLO(base_model_path)
            print("✅ Modelo cargado exitosamente\n")
            resume_mode = False
            
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        print("   Intenta: pip install --upgrade ultralytics torch")
        return False
    
    # =====================================================
    # PASO 3: ENTRENAR EL MODELO (CON LOOP INTERACTIVO)
    # =====================================================
    print("🚀 Iniciando entrenamiento...")
    print("   Esto puede tomar 5-15 minutos dependiendo de:")
    print("   - Número de imágenes")
    print("   - Velocidad de tu computadora")
    print("   - GPU disponible")
    print()
    
    continuar = True
    
    while continuar:
        try:
            # Entrenar el modelo
            results = model.train(
                data=data_yaml,        # Dónde están tus datos
                epochs=epochs,         # Épocas totales
                imgsz=640,             # Tamaño de imagen
                device='cpu',          # CPU (0 para GPU NVIDIA)
                patience=patience,     # EarlyStopping
                batch=batch,           # Tamaño de lote
                save=True,             # Guardar el modelo
                verbose=True,          # Mostrar detalles
                resume=resume_mode,    # Continuar entreno anterior
                project=base_dir       # Guardar resultados en la raíz
            )
            
            # Detectar si EarlyStopping se activó
            # (Si epochs completadas < epochs solicitadas = EarlyStopping)
            epochs_completadas = results.epoch + 1 if hasattr(results, 'epoch') else epochs
            
            print(f"\n📊 Epochs completadas: {epochs_completadas}/{epochs}")
            
            # EarlyStopping se activó si paró antes
            if epochs_completadas < epochs:
                print("\n⏸️  EarlyStopping activado!")
                print("   El modelo no mejoró en los últimos épocas.")
                print("\n   ¿Qué deseas hacer?")
                print("   1. Terminar (usar el mejor modelo)")
                print("   2. Continuar (más patience = más épocas)")
                print("   3. Salir sin preguntar más")
                
                opcion = input("\n   Elige (1-3): ").strip()
                
                if opcion == "1" or opcion == "":
                    print("\n✅ Entrenamiento finalizado.")
                    continuar = False
                    
                elif opcion == "2":
                    nueva_patience = input("\n   Nuevo patience (Enter para +5): ").strip()
                    if nueva_patience == "":
                        patience += 5
                    else:
                        try:
                            patience = int(nueva_patience)
                        except:
                            patience += 5
                    
                    epochs += 20  # Agregar más épocas
                    print(f"\n🔄 Continuando con patience={patience}, epochs={epochs}...")
                    print("   Esto puede tomar más tiempo...\n")
                    resume_mode = True
                    
                elif opcion == "3":
                    print("\n✅ Terminando sin preguntar más.")
                    continuar = False
                else:
                    print("\n❌ Opción inválida. Terminando...")
                    continuar = False
            else:
                # Entrenamiento completo sin EarlyStopping
                print("\n✅ ¡ENTRENAMIENTO COMPLETADO NATURALMENTE!")
                continuar = False
            
        except KeyboardInterrupt:
            # Usuario presionó Ctrl+C
            print("\n\n⚠️  Entrenamiento interrumpido por el usuario (Ctrl+C)")
            print("   ¿Qué deseas hacer?")
            print("   1. Terminar (guardar modelo actual)")
            print("   2. Continuar desde donde paró")
            print("   3. Salir")
            
            opcion = input("\n   Elige (1-3): ").strip()
            
            if opcion == "1" or opcion == "":
                print("\n✅ Entrenamiento finalizado.")
                continuar = False
            elif opcion == "2":
                print("\n🔄 Continuando entrenamiento...")
                epochs += 10  # Agregar 10 épocas más
                resume_mode = True
            else:
                print("\n❌ Saliendo...")
                continuar = False
        
        except Exception as e:
            # Error distinto a EarlyStopping o Ctrl+C
            print(f"\n❌ Error durante entrenamiento: {e}")
            print(f"   Verifica que:")
            print(f"   1. data.yaml existe en dataset/")
            print(f"   2. Tienes imágenes en dataset/train/images/")
            print(f"   3. Tienes etiquetas en dataset/train/labels/")
            continuar = False
            return False
    
    # =====================================================
    # PASO 4: INFORMACIÓN DEL MODELO ENTRENADO
    # =====================================================
    print("\n📊 Resultados del entrenamiento:")
    print(f"   - Modelo guardado en: runs/detect/train/")
    print(f"   - Archivo del modelo: runs/detect/train/weights/best.pt")
    print(f"   - Métricas guardadas en: runs/detect/train/results.csv")
    print(f"\n   Ahora puedes usar el modelo con: python main.py")
    
    return True

if __name__ == "__main__":
    success = train_model()
    
    if not success:
        print("\n⚠️  El entrenamiento falló. Revisa los errores arriba.")
        exit(1)
    else:
        print("\n🎉 ¡Todo listo para hacer predicciones!")

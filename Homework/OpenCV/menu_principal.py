"""
🎮 MENÚ PRINCIPAL - TUTORIALES DE VISIÓN COMPUTACIONAL
Selecciona qué tutorial quieres ejecutar
"""

import os
import sys

def mostrar_menu():
    print("🖼️  TUTORIALES DE VISIÓN COMPUTACIONAL")
    print("=" * 50)
    print()
    print("📚 Selecciona el tutorial que quieres ejecutar:")
    print()
    print("1. 🔰 Tutorial Básico OpenCV")
    print("   └── Operaciones básicas, filtros, transformaciones")
    print()
    print("2. 🔍 Detección de Formas Geométricas") 
    print("   └── Detecta triángulos, círculos, cuadrados automáticamente")
    print()
    print("3. 🎯 Simulador YOLO")
    print("   └── Entiende cómo funciona la detección de objetos")
    print()
    print("4. � Detección en Tiempo Real")
    print("   └── Simula detección con cámara web (como YOLO real)")
    print()
    print("5. �📖 Ver README completo")
    print()
    print("0. ❌ Salir")
    print()

def ejecutar_tutorial(opcion):
    """Ejecuta el tutorial seleccionado"""
    
    base_path = os.path.dirname(__file__)
    
    if opcion == "1":
        print("\n🚀 Iniciando Tutorial Básico OpenCV...")
        archivo = os.path.join(base_path, "app.py")
        
    elif opcion == "2":
        print("\n🚀 Iniciando Detección de Formas...")
        archivo = os.path.join(base_path, "deteccion_formas.py")
        
    elif opcion == "3":
        print("\n🚀 Iniciando Simulador YOLO...")
        archivo = os.path.join(base_path, "simulador_yolo.py")
        
    elif opcion == "4":
        print("\n� Iniciando Detección en Tiempo Real...")
        archivo = os.path.join(base_path, "deteccion_tiempo_real.py")
        
    elif opcion == "5":
        print("\n📖 README COMPLETO:")
        print("=" * 30)
        readme_path = os.path.join(base_path, "README.md")
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ README.md no encontrado")
        return True
        
    elif opcion == "0":
        print("\n👋 ¡Hasta luego! Sigue practicando visión computacional.")
        return False
        
    else:
        print("\n❌ Opción no válida. Intenta de nuevo.")
        return True
    
    # Ejecutar el archivo seleccionado
    if opcion in ["1", "2", "3", "4"]:
        try:
            print(f"📁 Ejecutando: {archivo}")
            print("🔄 Cargando...")
            print("-" * 50)
            
            # Ejecutar el archivo
            exec(open(archivo).read())
            
        except FileNotFoundError:
            print(f"❌ No se encontró el archivo: {archivo}")
        except Exception as e:
            print(f"❌ Error al ejecutar: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Tutorial completado. ¿Quieres ejecutar otro?")
    
    return True

def main():
    """Función principal del menú"""
    
    print("🎉 ¡Bienvenido a los tutoriales de Visión Computacional!")
    print("💡 Estos tutoriales están basados en tus clases de Python IV")
    print()
    
    while True:
        mostrar_menu()
        
        opcion = input("👆 Elige una opción (0-5): ").strip()
        
        # Limpiar pantalla en Windows
        os.system('cls' if os.name == 'nt' else 'clear')
        
        continuar = ejecutar_tutorial(opcion)
        
        if not continuar:
            break
            
        # Pausa antes de mostrar el menú de nuevo
        input("\n⏸️  Presiona ENTER para volver al menú principal...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
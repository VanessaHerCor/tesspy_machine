"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  ⚡ PRUEBA RÁPIDA - VERIFICA QUE TODO FUNCIONA              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Este script verifica que:
  ✓ Todas las librerías están instaladas
  ✓ Todos los archivos existen
  ✓ El proyecto está listo para usar

Ejecuta esto DESPUÉS de: pip install -r requirements.txt
"""

import sys
import os
from pathlib import Path


def verificar_instalacion():
    """Verifica que todas las librerías estén instaladas"""
    print("\n" + "="*80)
    print("🔍 VERIFICANDO INSTALACIÓN DE LIBRERÍAS")
    print("="*80)
    
    librerias = {
        'pandas': '📦 pandas',
        'numpy': '📦 numpy',
        'sklearn': '📦 scikit-learn',
        'gensim': '📦 gensim',
        'transformers': '📦 transformers',
        'torch': '📦 torch'
    }
    
    todas_ok = True
    
    for libreria, nombre in librerias.items():
        try:
            __import__(libreria)
            print(f"✅ {nombre} - Instalado")
        except ImportError:
            print(f"❌ {nombre} - NO instalado")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  FALTAN LIBRERÍAS!")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    print("\n✅ ¡Todas las librerías instaladas correctamente!")
    return True


def verificar_archivos():
    """Verifica que todos los archivos existan"""
    print("\n" + "="*80)
    print("📁 VERIFICANDO ARCHIVOS DEL PROYECTO")
    print("="*80)
    
    directorio_actual = Path(__file__).parent
    
    archivos_esperados = {
        'main.py': '📄 Menú principal',
        'INICIO_RAPIDO.py': '📄 Guía rápida',
        'ESTRUCTURA.py': '📄 Resumen de estructura',
        'README.md': '📖 Documentación',
        'requirements.txt': '📋 Dependencias',
        'EJEMPLOS_AVANZADOS.py': '🚀 Ejemplos avanzados',
        'tecnicas/1_bag_of_words.py': '🔹 Bag of Words',
        'tecnicas/2_tfidf.py': '🔹 TF-IDF',
        'tecnicas/3_word2vec.py': '🔹 Word2Vec',
        'tecnicas/4_bert.py': '🔹 BERT'
    }
    
    todos_ok = True
    
    for archivo, descripcion in archivos_esperados.items():
        ruta = directorio_actual / archivo
        if ruta.exists():
            print(f"✅ {descripcion} - Encontrado")
        else:
            print(f"❌ {descripcion} - NO encontrado")
            todos_ok = False
    
    if not todos_ok:
        print("\n⚠️  FALTAN ARCHIVOS!")
        print("Asegúrate de estar en la carpeta 'Lenguaje_Natural'")
        return False
    
    print("\n✅ ¡Todos los archivos están presentes!")
    return True


def prueba_basica():
    """Prueba básica de funcionalidad"""
    print("\n" + "="*80)
    print("⚡ PRUEBA BÁSICA DE FUNCIONALIDAD")
    print("="*80)
    
    try:
        print("\n📝 Probando pandas...")
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print("✅ Pandas funciona correctamente")
        
        print("\n📊 Probando scikit-learn...")
        from sklearn.feature_extraction.text import CountVectorizer
        corpus = ['hello world', 'how are you']
        cv = CountVectorizer()
        cv.fit(corpus)
        print("✅ Scikit-learn funciona correctamente")
        
        print("\n🔤 Probando gensim...")
        from gensim.models import Word2Vec
        sentences = [['hello', 'world'], ['how', 'are', 'you']]
        model = Word2Vec(sentences, vector_size=5, window=2, min_count=1, epochs=10)
        print("✅ Gensim funciona correctamente")
        
        print("\n🤖 Probando torch...")
        import torch
        tensor = torch.tensor([1, 2, 3])
        print(f"✅ Torch funciona correctamente")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        return False


def mostrar_proximos_pasos():
    """Muestra los próximos pasos"""
    print("\n" + "="*80)
    print("🚀 PRÓXIMOS PASOS")
    print("="*80)
    
    print("""
✅ TODO ESTÁ LISTO

Ahora puedes:

1️⃣  OPCIÓN 1: Ejecutar el menú interactivo
    python main.py
    
2️⃣  OPCIÓN 2: Ejecutar guía rápida
    python INICIO_RAPIDO.py
    
3️⃣  OPCIÓN 3: Ver estructura del proyecto
    python ESTRUCTURA.py
    
4️⃣  OPCIÓN 4: Ejecutar una técnica específica
    python tecnicas/1_bag_of_words.py
    python tecnicas/2_tfidf.py
    python tecnicas/3_word2vec.py
    python tecnicas/4_bert.py
    
5️⃣  OPCIÓN 5: Ver ejemplos avanzados
    python EJEMPLOS_AVANZADOS.py


RECOMENDACIÓN:
==============
Comienza con: python main.py

¡Que disfrutes aprendiendo NLP! 📚✨
""")


def main():
    """Función principal"""
    print("\n╔" + "="*78 + "╗")
    print("║" + "VERIFICACIÓN DEL PROYECTO LENGUAJE_NATURAL".center(78) + "║")
    print("╚" + "="*78 + "╝")
    
    # Ejecutar verificaciones
    libs_ok = verificar_instalacion()
    archivos_ok = verificar_archivos()
    funcionalidad_ok = prueba_basica()
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    
    if libs_ok and archivos_ok and funcionalidad_ok:
        print("\n✅ ¡PERFECTO! Todo está funcionando correctamente")
        print("\n🎉 El proyecto está LISTO para usarse")
        mostrar_proximos_pasos()
        return 0
    else:
        print("\n⚠️  HAY PROBLEMAS")
        
        if not libs_ok:
            print("\n❌ Librerías faltantes:")
            print("   Ejecuta: pip install -r requirements.txt")
        
        if not archivos_ok:
            print("\n❌ Archivos faltantes:")
            print("   Asegúrate de estar en la carpeta 'Lenguaje_Natural'")
            print("   Verifica que no borraste ningún archivo")
        
        if not funcionalidad_ok:
            print("\n❌ Error de funcionalidad:")
            print("   Hay un problema al usar las librerías")
            print("   Intenta reinstalar: pip install --upgrade -r requirements.txt")
        
        return 1


if __name__ == "__main__":
    try:
        codigo_salida = main()
        sys.exit(codigo_salida)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

# SESIÓN 5: Depuración y análisis de código

Sistema completo de debugging, logging estructurado, profiling y análisis estático de código.

## 🎯 Objetivos

- Usar herramientas avanzadas de debugging en Python
- Implementar logging estratégico para debugging
- Realizar análisis estático de código con herramientas profesionales
- Identificar y resolver memory leaks y problemas de rendimiento
- Configurar profiling para optimización de código

## 📁 Estructura del Proyecto

```
proyecto/
├── debug_example.py      # Script principal con ejemplos
├── static_analysis/      # Configuraciones de análisis estático
├── requirements.txt      # Dependencias
└── README.md            # Esta documentación
```

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 💻 Cómo Ejecutar

### Ejemplo Principal
```bash
python debug_example.py
```

### Debugging Interactivo con pdb
```bash
python debug_example.py
# Cuando aparezca (Pdb), usa estos comandos:
# l    - mostrar código
# n    - siguiente línea
# c    - continuar
# p variable_name - mostrar valor
# q    - salir
```

### Debugging Visual con pudb
```bash
python -m pudb debug_example.py
```

### Memory Profiling
```bash
python -m memory_profiler debug_example.py
```

### Profiling de Rendimiento
```bash
python -m cProfile -o profile.stats debug_example.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Análisis Estático

#### Linting con flake8
```bash
flake8 debug_example.py
```

#### Type checking con mypy
```bash
mypy debug_example.py
```

#### Security analysis con bandit
```bash
bandit -r .
```

#### Code formatting con black
```bash
black debug_example.py
```

### Profiling en Producción
```bash
# Instalar py-spy
pip install py-spy

# Terminal 1: Ejecutar aplicación
python debug_example.py

# Terminal 2: Profiling en vivo
py-spy record -o profile.svg -- python debug_example.py
```

## 🔧 Características Implementadas

### 1. **Logging Estructurado**
- Logger con contexto automático
- Formato JSON para fácil análisis
- Niveles de logging apropiados
- Context managers para trazabilidad

### 2. **Debugging Interactivo**
- Breakpoints estratégicos con pdb
- Ejemplos de debugging paso a paso
- Inspección de variables y estado

### 3. **Profiling de Rendimiento**
- Time profiling con cProfile
- Memory profiling línea por línea
- Identificación de bottlenecks

### 4. **Memory Debugging**
- Tracking de uso de memoria con tracemalloc
- Detección de memory leaks
- Análisis de consumo por línea

### 5. **Análisis Estático**
- Ejemplos de problemas que detectan herramientas
- Configuración de pre-commit hooks
- Integración con workflow de desarrollo

## 📊 Técnicas Demostradas

### Debugging Sistemático
```python
# 1. Reproducir el problema
# 2. Aislar variables
# 3. Formular hipótesis
# 4. Validar con tests
# 5. Implementar fix
```

### Logging Estratégico
```python
# Entrada/salida de funciones
# Estados de variables críticas
# Timing de operaciones
# Correlation IDs
```

### Profiling Efectivo
```python
# Time profiling para bottlenecks
# Memory profiling para leaks
# Call profiling para optimización
```

## 🛠️ Herramientas Incluidas

- **pdb/pdbpp**: Debugging interactivo
- **pudb**: Debugging visual
- **memory_profiler**: Análisis de memoria
- **cProfile**: Profiling de tiempo
- **flake8**: Linting básico
- **mypy**: Type checking
- **bandit**: Security analysis
- **black**: Code formatting

## 🎓 Conceptos Clave

1. **Debugging científico**: Hipótesis → Test → Validación
2. **Logging estructurado**: Contexto + JSON + Trazabilidad
3. **Profiling orientado a datos**: Medir antes de optimizar
4. **Análisis estático preventivo**: Detectar problemas temprano
5. **Automatización**: Pre-commit hooks + CI integration

## 🔍 Comandos Útiles

```bash
# Debugging interactivo
python -m pdb debug_example.py

# Memory profiling detallado
mprof run debug_example.py
mprof plot

# Profiling estadístico
python -m pyinstrument debug_example.py

# Análisis completo
flake8 . && mypy . && bandit -r . && python debug_example.py
```

## 📝 Notas Importantes

- El script incluye bugs intencionales para demostrar debugging
- Los breakpoints con `pdb.set_trace()` están comentados por defecto
- El memory profiling puede consumir recursos adicionales
- Las herramientas de análisis estático requieren configuración específica

¡Experimenta con diferentes técnicas de debugging y profiling para mejorar la calidad de tu código!
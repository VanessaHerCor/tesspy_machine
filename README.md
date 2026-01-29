<<<<<<< HEAD
# tesspy_machine
Repositorio para clases
=======
# 🐍 Sesión Django - Los 3 Enfoques Web - 2 Horas

## 📋 Agenda de la Sesión

**Duración Total:** 120 minutos  
**Enfoque:** Entender los **3 enfoques diferentes** para servir contenido web con Django  
**Objetivo:** Comparar **páginas estáticas**, **templates dinámicos** y **APIs JSON**

---

## 🎯 Los 3 Enfoques que Aprenderás

| **Enfoque** | **Cuándo usar** | **Tecnología** | **Ejemplo** |
|-------------|-----------------|----------------|-------------|
| **📄 Estático** | Landing pages, documentación | HTML fijo | Página "Acerca de" |
| **🎨 Dinámico** | Apps web tradicionales | Django Templates + BD | Blog, dashboard |
| **🔌 API** | Apps móviles, SPAs, microservicios | JSON + REST | React app, app móvil |

---

## 🗓️ Cronograma

### ⏰ **Ejercicio 1: Django Básico** (30 minutos)
- **🏗️ Estructura de Django** (10 min) - Proyectos, apps, configuración
- **📄 Páginas Estáticas** (15 min) - HTML fijo, URLs, vistas simples  
- **📊 Migraciones** (5 min) - Base de datos, showmigrations, migrate

### ☕ **Descanso** (10 minutos)

### ⏰ **Ejercicio 2: Templates Dinámicos + API** (45 minutos)
- **🗄️ Modelos y BD** (15 min) - BlogEntry, migraciones, datos de prueba
- **🎨 Templates Dinámicos** (20 min) - Sintaxis {% %}, herencia, filtros
- **🔌 API REST** (10 min) - Serializers (modelo ↔ JSON), endpoints manuales

### ☕ **Descanso** (5 minutos)

### ⏰ **Ejercicio 3: Formularios y Autenticación** (30 minutos)
- **📝 Formularios** (15 min) - ModelForm, validación, POST
- **🔐 Autenticación** (15 min) - Login, logout, usuarios

---

## 📚 Estructura Final del Proyecto

```
mi_blog/
├── README.md                # Este archivo - Guía de la sesión  
├── ejercicios/              # Ejercicios paso a paso
│   ├── ejercicio_1.md       # 📄 Django básico + páginas estáticas
│   ├── ejercicio_2.md       # 🎨 Templates dinámicos + API JSON
│   └── ejercicio_3.md       # 📝 Formularios + autenticación
└── solucion/mi_blog/        # Proyecto Django completo
    ├── staticpages/         # 📄 App para contenido estático
    ├── dynamicpages/        # 🎨 App para templates dinámicos  
    ├── api/                 # 🔌 App para API REST
    └── mi_blog/             # Configuración principal
```

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta sesión, los estudiantes **dominarán los 3 enfoques de Django**:

### 📄 Páginas Estáticas
- ✅ **HTML fijo** definido en views.py
- ✅ **Sin base de datos** - contenido que no cambia
- ✅ **Respuesta rápida** - ideal para landing pages
- ✅ **URLs y vistas** básicas

### 🎨 Templates Dinámicos  
- ✅ **Sintaxis Django**: `{{ variable }}`, `{% tag %}`, `|filtros`
- ✅ **Herencia de templates**: `{% extends %}`, `{% block %}`
- ✅ **Contexto**: Pasar datos de vista a template
- ✅ **Consultas de BD**: Modelos → Template

### 🔌 API REST
- ✅ **Serializers**: Conversión automática modelo Django ↔ JSON
- ✅ **@api_view**: Decoradores para endpoints manuales
- ✅ **REST endpoints**: GET, POST, PUT, DELETE explícitos
- ✅ **Validación**: Datos JSON → modelo Django con validación
- ✅ **Django REST Framework**

### 🔄 Reutilización
- ✅ **Mismo modelo** (`BlogEntry`) usado de 3 formas diferentes
- ✅ **Comparar enfoques** en tiempo real
- ✅ **Elegir el enfoque correcto** según necesidades

---

## 🛠️ Requisitos Previos

- Python 3.8+ instalado
- Conocimientos básicos de Python
- Editor de código (VS Code, PyCharm, etc.)
- Terminal/Línea de comandos

## 📦 Instalación

```bash
# Crear entorno virtual
python -m venv django_env

# Activar entorno virtual
# En Windows:
django_env\Scripts\activate
# En Mac/Linux:
source django_env/bin/activate

# Instalar dependencias
pip install django djangorestframework

# Verificar instalación
django-admin --version
```

---

## 🚀 Comenzar la Sesión

### 📋 Orden de los Ejercicios:

#### 1. **Ejercicio 1** (`ejercicios/ejercicio_1.md`) - 30 min
   - ✅ Crear proyecto Django desde cero
   - ✅ Entender estructura: proyecto vs app
   - ✅ Páginas estáticas con HTML fijo
   - ✅ Sistema de URLs y vistas básicas
   - ✅ Migraciones y base de datos
   - **Resultado:** Páginas estáticas funcionando

#### 2. **Ejercicio 2** (`ejercicios/ejercicio_2.md`) - 45 min  
   - ✅ Crear modelos y base de datos
   - ✅ Templates dinámicos con sintaxis Django
   - ✅ Herencia de templates (base.html)
   - ✅ API REST con Django REST Framework
   - ✅ Comparar los 3 enfoques funcionando
   - **Resultado:** Sistema completo con 3 enfoques

#### 3. **Ejercicio 3** (`ejercicios/ejercicio_3.md`) - 30 min
   - ✅ Formularios para crear contenido
   - ✅ Autenticación de usuarios
   - ✅ Templates con Bootstrap
   - ✅ Rutas protegidas
   - **Resultado:** Blog completo e interactivo

---

## 🎯 URLs Finales del Proyecto

### 📄 **Contenido Estático**
- `http://127.0.0.1:8000/static-pages/` → Home estática
- `http://127.0.0.1:8000/static-pages/about/` → About estática
- `http://127.0.0.1:8000/static-pages/contact/` → Formulario estático

### 🎨 **Templates Dinámicos**  
- `http://127.0.0.1:8000/dynamic-pages/` → Lista de blog desde BD
- `http://127.0.0.1:8000/dynamic-pages/blogentry/1/` → Detalle desde BD

### 🔌 **API JSON**
- `http://127.0.0.1:8000/api/v1/blogentries/` → Lista en JSON
- `http://127.0.0.1:8000/api/v1/blogentries/1/` → Detalle en JSON

---

## 🎓 Valor Pedagógico

### **¿Por qué 3 enfoques?**

Los estudiantes verán **el mismo dato** (`BlogEntry`) servido de **3 formas diferentes**:

1. **📄 Estático**: Para contenido que no cambia
2. **🎨 Dinámico**: Para apps web tradicionales  
3. **🔌 API**: Para apps móviles y SPAs

### **Conceptos Clave**
- **URLs**: Enrutamiento y organización
- **Vistas**: Lógica de negocio
- **Templates**: Presentación de datos
- **Modelos**: Estructura de datos
- **Migraciones**: Evolución de BD
- **REST**: Arquitectura moderna

---

## 🏆 Al Final Tendrás

Un proyecto Django **completo y pedagógico** que demuestra:

- ✅ **3 enfoques web** funcionando simultáneamente
- ✅ **Estructura profesional** con múltiples apps
- ✅ **Reutilización de código** (mismo modelo, 3 usos)
- ✅ **Comparación práctica** entre enfoques
- ✅ **Base sólida** para proyectos reales

**¡Una sesión que cubre desde lo básico hasta conceptos avanzados!** 🚀

---

## 🔧 Comandos Útiles de Django

```bash
# Gestión de migraciones
python manage.py showmigrations       # Ver estado
python manage.py makemigrations       # Crear migraciones
python manage.py migrate              # Aplicar migraciones

# Servidor de desarrollo
python manage.py runserver            # Solo localhost (127.0.0.1:8000)
python manage.py runserver 8080       # Puerto personalizado
python manage.py runserver 0.0.0.0:8000  # Accesible desde otros dispositivos

# Crear datos de prueba
python manage.py crear_posts          # Comando personalizado

# Shell interactivo
python manage.py shell                # Django shell
```

### 📱 **Acceso desde Otros Dispositivos**

Para que **móviles u otros dispositivos** en la misma red accedan al servidor:

```bash
# 1. Ejecutar servidor en todas las interfaces
python manage.py runserver 0.0.0.0:8000

# 2. Configurar ALLOWED_HOSTS en settings.py
ALLOWED_HOSTS = ['*']  # Permite todas las IPs (solo desarrollo)

# 3. Acceder desde otro dispositivo usando IP del servidor
# Ejemplo: http://192.168.1.100:8000/static-pages/
```

**⚠️ Nota de Seguridad:** `ALLOWED_HOSTS = ['*']` **solo para desarrollo**. En producción, especifica IPs/dominios específicos.

**¡Sin admin panel! Solo Django core y conceptos fundamentales!** 🎯
>>>>>>> e2c17bf652615bb793ab9a1469d744ec789020a8

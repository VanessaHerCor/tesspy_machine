# 📄 STATICPAGES - Páginas Estáticas y Landing Pages

Módulo que proporciona **páginas estáticas HTML renderizadas directamente** desde vistas de Django. Ideal para landing pages, páginas de información general (About, Contact) que no requieren datos dinámicos de la base de datos ni templates complejos.

---

## 📋 Tabla de Contenidos

- [Estructura](#estructura)
- [Vistas Estáticas](#vistas-estáticas)
- [Características](#características)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Diferencias con Otros Módulos](#diferencias-con-otros-módulos)

---

## 📁 Estructura

```
staticpages/
├── __init__.py              # Configuración del app
├── apps.py                  # Definición de la app
├── admin.py                 # Admin de Django (no usado)
├── models.py                # Modelos locales (vacío)
├── views.py                 # Vistas que retornan HTML estático
├── urls.py                  # Rutas de las páginas estáticas
├── tests.py                 # Tests unitarios
├── __pycache__/
└── README.md                # Este archivo
```

---

## 🌐 Vistas Estáticas

### 1. **Home (Landing Page)**
```
GET /static-pages/
```

**Función:** [home()](views.py)

**Descripción:**
Página principal de bienvenida con:
- ✅ Título y descripción del proyecto
- ✅ Lista de características principales
- ✅ Botones de llamada a la acción (CTA)
- ✅ Navegación central a todas las secciones

**HTML Generado:**
- Encabezado con navegación
- Sección hero con descripción
- Lista de características
- Botones para acceder a catálogo y más información
- Estilos inline (dark mode neón)

**Contenido Mostrado:**

```
🎮 Videojuegos - Landing Page

¡Bienvenido a Video Games Database!

La mejor plataforma para descubrir videojuegos

✅ Catálogo completo de videojuegos
✅ Información actualizada de títulos populares
✅ Búsqueda rápida y eficiente
✅ Reseñas y puntuaciones de usuarios

[🎮 Ver Catálogo Dinámico] [ℹ️ Conocer Más]
```

---

### 2. **About (Información General)**
```
GET /static-pages/about/
```

**Función:** [about()](views.py)

**Descripción:**
Página informativa sobre el proyecto:
- ✅ Misión y visión del proyecto
- ✅ Características técnicas principales
- ✅ Stack tecnológico utilizado
- ✅ Links a otras secciones

**Contenido Mostrado:**

```
ℹ️ Acerca de Video Games Database

Nuestra Misión:
Proporcionar la base de datos más completa y actualizada 
de videojuegos del mundo.

Características principales:
🎯 Base de datos MongoDB para escalabilidad
🔍 API REST para acceder a información de videojuegos
⭐ Sistema de calificaciones y reseñas
🏆 Clasificación por géneros, plataformas y años
📊 Estadísticas actualizadas en tiempo real

Tecnología:
Django + MongoDB + REST Framework
```

---

### 3. **Contact (Formulario de Contacto)**
```
GET /static-pages/contact/
```

**Función:** [contact()](views.py)

**Descripción:**
Página con formulario de contacto:
- ✅ Formulario con campos estándar
- ✅ Validación básica en cliente
- ✅ Mensaje de confirmación al enviar
- ✅ Links de navegación

**Formulario:**
```
📧 Contacto

Campos:
- Nombre (text, required)
- Email (email, required)
- Asunto (text, required)
- Mensaje (textarea, required)

[📤 Enviar Mensaje]
```

**Interactividad:**
- Click en botón → `alert('¡Gracias por tu mensaje! Te contactaremos pronto.')`
- Nota: Es un formulario de demostración sin procesamiento backend

---

## 🎨 Características

### Diseño y Estilo

✅ **Dark Mode Neón:**
- Fondo: Gradiente azul oscuro (#1a1a2e → #16213e)
- Colores principales: Cyan (#00d4ff), Magenta (#ff006e)
- Texto: Blanco/Gris claro

✅ **Responsive:**
- Navbar flexible con secciones
- Botones y formularios adaptables
- Media queries integrados

✅ **Interactividad:**
- Hover effects en navegación
- Efectos de transición suave
- Formulario con validación HTML5

✅ **Navegación Consistente:**
- Header en todas las páginas
- Dos secciones de nav: Estáticas y Dinámicas
- Links entre todas las secciones

### Navegación

```
Header:
├── 📄 ESTÁTICAS
│   ├── 🏠 Home (/static-pages/)
│   ├── ℹ️ About (/static-pages/about/)
│   └── 📧 Contact (/static-pages/contact/)
└── 🎮 DINÁMICAS
    ├── 📋 Catálogo (/dynamic/)
    └── 🔌 API JSON (/dynamic/api/videogames/)
```

---

## 💡 Ejemplos de Uso

### Acceso desde Navegador

```
1. Home (Landing Page):
   URL: http://localhost:8000/static-pages/
   
2. About (Información):
   URL: http://localhost:8000/static-pages/about/
   
3. Contact (Formulario):
   URL: http://localhost:8000/static-pages/contact/
```

### Desde cURL (verificar que retorna HTML)

```bash
# 1. Obtener HTML de Home
curl -X GET http://localhost:8000/static-pages/ \
  -H "Content-Type: text/html"

# 2. Obtener HTML de About
curl -X GET http://localhost:8000/static-pages/about/ \
  -H "Content-Type: text/html"

# 3. Obtener HTML de Contact
curl -X GET http://localhost:8000/static-pages/contact/ \
  -H "Content-Type: text/html"
```

### Desde Python

```python
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000/static-pages"

# Obtener y parsear HTML
response = requests.get(f"{BASE_URL}/")
soup = BeautifulSoup(response.content, 'html.parser')

# Extraer título
title = soup.find('title').text
print(f"Título: {title}")

# Extraer todas las características
features = soup.find_all('li')
for feature in features:
    print(f"- {feature.text}")
```

### Desde JavaScript

```javascript
// Obtener contenido HTML
fetch('http://localhost:8000/static-pages/')
    .then(response => response.text())
    .then(html => {
        // Procesar HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const heading = doc.querySelector('h2').textContent;
        console.log(heading); // "¡Bienvenido a Video Games Database!"
    });
```

---

## 🔄 Diferencias con Otros Módulos

| Aspecto | staticpages | dynamicpages | forn_api | auth_api |
|--------|----------|----------|----------|---------|
| **Propósito** | Landing pages estáticas | Catálogo dinámico + API | API REST avanzada | Autenticación JWT |
| **Base de Datos** | ❌ No | ✅ MongoDB | ✅ MongoDB | ✅ MongoDB |
| **Templates** | ❌ HTML en vistas | ✅ Templates Django | ❌ API pura | ❌ API pura |
| **Datos Dinámicos** | ❌ No | ✅ Sí (MongoDB) | ✅ Sí (MongoDB) | ✅ Sí (MongoDB) |
| **Respuesta** | HTML estático | HTML + JSON | JSON | JSON |
| **Casos de uso** | Landing, About, Info | Catálogo web completo | Apps, SPA, dashboards | Seguridad, autenticación |

---

## 🎯 Casos de Uso

### 1. **Landing Page de Presentación**
```
http://localhost:8000/static-pages/
→ Presentar el proyecto y atraer usuarios
→ Botones de llamada a la acción (CTA)
```

### 2. **Página de Información (About)**
```
http://localhost:8000/static-pages/about/
→ Explicar características del proyecto
→ Mostrar tecnología utilizada
→ Información de la misión
```

### 3. **Formulario de Contacto**
```
http://localhost:8000/static-pages/contact/
→ Permitir que usuarios se pongan en contacto
→ Validación básica de formulario
→ Confirmación de envío
```

### 4. **Hub de Navegación Central**
```
Todas las páginas incluyen navegación consistente:
→ Enlaces a otras áreas estáticas
→ Acceso rápido a secciones dinámicas
→ Experiencia de usuario coherente
```

---

## 📊 Flujo de Navegación

```
┌─────────────────────────────────────┐
│   STATIC PAGES (Páginas Estáticas)  │
├─────────────────────────────────────┤
│                                     │
│  Home (/static-pages/)              │
│  ├── ℹ️ About                       │
│  ├── 📧 Contact                     │
│  └── 🎮 Catálogo (→ dynamicpages)  │
│                                     │
│  About (/static-pages/about/)       │
│  ├── 🏠 Home                        │
│  ├── 📧 Contact                     │
│  └── 🎮 Catálogo                    │
│                                     │
│  Contact (/static-pages/contact/)   │
│  ├── 🏠 Home                        │
│  ├── ℹ️ About                       │
│  └── 🎮 Catálogo                    │
│                                     │
└─────────────────────────────────────┘
         ↓ (Links a secciones)
┌─────────────────────────────────────┐
│  DYNAMIC PAGES & API                │
│  (/dynamic/ y /api/videogames/)     │
└─────────────────────────────────────┘
```

---

## 🛠️ Implementación Técnica

### Estructura de Vistas

```python
def home(request):
    """Retorna HTML estático como HttpResponse"""
    html_content = """..."""  # HTML completo aquí
    return HttpResponse(html_content)
```

### Ventajas de Este Enfoque

✅ **Simple y directo** - No requiere templates
✅ **Rápido** - Sin procesamiento de BD
✅ **Controlado** - HTML completamente personalizado
✅ **Independiente** - No depende de otros módulos

### Desventajas

❌ **Código repetido** - El HTML de header/nav se repite
❌ **Difícil de mantener** - Cambios requieren editar múltiples vistas
❌ **No escalable** - Agregar nuevas páginas requiere código adicional

### Mejora Recomendada (Futuro)

```python
# Convertir a templates Django para reutilización
# staticpages/templates/
# ├── base.html          (Header y nav reutilizable)
# ├── home.html          (extends base.html)
# ├── about.html         (extends base.html)
# └── contact.html       (extends base.html)

def home(request):
    return render(request, 'staticpages/home.html')
```

---

## 📝 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| [views.py](views.py) | 3 vistas que generan HTML estático |
| [urls.py](urls.py) | Rutas de las 3 páginas estáticas |
| [apps.py](apps.py) | Configuración de la app |
| [models.py](models.py) | Vacío (no usa BD) |
| [admin.py](admin.py) | Vacío (no necesario) |

---

## 🔐 Consideraciones de Seguridad

### HTML Injection

```python
# ❌ PELIGROSO - No hacer esto con entrada de usuario:
user_input = request.GET.get('message')  # "'; DROP TABLE users; --"
html = f"<p>{user_input}</p>"  # Vulnerable a inyección

# ✅ SEGURO - Escapar siempre:
from django.utils.html import escape
html = f"<p>{escape(user_input)}</p>"  # Seguro
```

### Para Formularios Reales

En producción, usar Django Forms:

```python
from django import forms
from django.views.decorators.http import require_http_methods

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=200)
    mensaje = forms.CharField(widget=forms.Textarea)

@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesar formulario
            send_email(form.cleaned_data)
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

---

## 🚀 Mejoras Futuras

- [ ] Convertir a templates Django para reutilización
- [ ] Agregar validación backend de formulario contact
- [ ] Implementar envío de emails
- [ ] Agregar SEO (meta tags, sitemap)
- [ ] Agregar formulario de suscripción a newsletter
- [ ] Integrar con auth_api para login/registro
- [ ] Agregar página 404 personalizada

---

## 🔗 Integración con Otros Módulos

Este módulo se integra con:

- **[dynamicpages](../dynamicpages/)** - Links en navegación
- **[forn_api](../forn_api/)** - Links a API JSON
- **[auth_api](../auth_api/)** - Potencial para login en futuro

---

## 📖 Referencia Rápida de URLs

| Ruta | Método | Descripción |
|------|--------|------------|
| `/static-pages/` | GET | Home (landing page) |
| `/static-pages/about/` | GET | Información del proyecto |
| `/static-pages/contact/` | GET | Formulario de contacto |

---

## 🎨 CSS y Diseño

### Colores Principales

```css
/* Fondos */
background: #1a1a2e;      /* Azul oscuro principal */
background: #16213e;      /* Azul más oscuro */

/* Textos y acentos */
color: #00d4ff;           /* Cyan (primario) */
color: #ff006e;           /* Magenta (énfasis) */
color: #eee;              /* Gris claro */

/* Bordes */
border: 2px solid #00d4ff;
```

### Tipografía

```css
font-family: Arial, sans-serif;
font-size: 2.5em;         /* Títulos principales */
font-weight: bold;        /* Énfasis */
```

### Efectos

```css
/* Transiciones suaves */
transition: all 0.3s;

/* Sombras */
box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);

/* Gradientes */
background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
```

---

**Última actualización:** 12 enero 2026

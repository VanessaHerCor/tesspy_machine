# Proyecto 2 - Ejemplo de Selenium con Google

Este proyecto demuestra el uso básico de Selenium para automatizar la búsqueda en Google.

## Requisitos

- Python 3.x
- Firefox instalado
- geckodriver (ya incluido en el proyecto)

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el script:
```bash
python google_search.py
```

## Descripción

El script realiza las siguientes acciones:
1. Abre el navegador Firefox
2. Accede a google.com
3. Escribe "Selenium Python tutorial" en la barra de búsqueda
4. Presiona Enter para buscar
5. Espera 3 segundos para ver los resultados
6. Cierra el navegador

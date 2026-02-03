"""
Configuración global de pytest para el proyecto.
Agrega el directorio raíz al PYTHONPATH automáticamente.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
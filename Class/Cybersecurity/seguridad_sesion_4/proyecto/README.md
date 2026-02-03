# SESIÓN 4: PRUEBAS DE REGRESIÓN Y PRUEBAS DE CARGA

Sistema completo con regresión automática y load testing

## Estructura del Proyecto

```
proyecto/
├── src/
│   ├── __init__.py
│   ├── app.py              # API Flask para load testing
│   ├── report_generator.py # Generador de reportes (golden tests)
│   └── data_processor.py   # Procesador de datos
├── tests/
│   ├── smoke/             # Smoke tests críticos
│   ├── regression/        # Suite de regresión completa
│   │   ├── historical/    # Tests de bugs pasados
│   │   ├── golden/        # Golden/snapshot tests
│   │   └── performance/   # Regression de rendimiento
│   └── load/              # Scripts de Locust
├── data/
│   ├── golden_outputs/    # Archivos de referencia
│   ├── test_datasets/     # Datos de prueba
│   └── benchmarks/        # Resultados de benchmark
├── scripts/               # Scripts de automatización
├── reports/               # Reportes generados
├── locustfile.py          # Script principal de Locust
├── pytest.ini
└── requirements.txt
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Comandos de Ejecución

### 1. TODOS LOS TESTS (suite completa):
```bash
pytest tests/ -v
```

### 2. SMOKE TESTS (críticos, rápidos):
```bash
pytest tests/smoke/ -v --maxfail=1
```

### 3. REGRESSION SUITE (completa):
```bash
pytest tests/regression/ -v
```

### 4. PERFORMANCE REGRESSION:
```bash
pytest tests/regression/performance/ --benchmark-only
```

### 5. LOAD TESTING:
Terminal 1: Iniciar servidor
```bash
python src/app.py
```

Terminal 2: Ejecutar load test
```bash
locust -f locustfile.py --host=http://localhost:5001
```

### 6. GOLDEN TESTS (actualizar referencias):
```bash
pytest tests/regression/golden/ --force-regen
```

## Scripts de Automatización

### Suite completa de regresión:
```bash
python scripts/run_regression_suite.py
```

### Load testing automatizado:
```bash
python scripts/run_load_test.py
```

## Conceptos Demostrados

- Smoke testing automatizado
- Golden tests / Snapshot testing
- Regression suite organizada
- Performance regression testing
- Load testing con Locust
- Realistic user scenarios
- Métricas y análisis de rendimiento

## Endpoints de la API

- `GET /health` - Health check
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/<id>` - Get user
- `GET /api/posts` - List posts (paginated)
- `GET /api/search?q=<query>` - Search
- `POST /api/heavy-operation` - Heavy operation
- `GET /api/stats` - Server stats
- `GET /api/slow` - Intentionally slow endpoint
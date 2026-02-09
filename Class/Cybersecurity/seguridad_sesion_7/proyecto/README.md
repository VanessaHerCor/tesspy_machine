# SESIÓN 7: Automatización de pruebas con GitHub Actions

Sistema completo de CI/CD con GitHub Actions para testing automatizado

## 🎯 Objetivos

- Configurar pipelines de CI/CD con GitHub Actions para testing
- Implementar estrategias de testing automatizado por tipo y entorno
- Configurar matrix testing para múltiples versiones de Python
- Integrar code coverage, security scanning y quality gates
- Crear workflows eficientes con caching y paralelización
- Implementar deployment condicional basado en testing

## 📁 Estructura del Proyecto

```
proyecto/
├── github_actions_example.py    # Script principal con ejemplos de testing
├── .github/
│   └── workflows/
│       └── ci.yml              # Workflow completo de GitHub Actions
├── requirements.txt            # Dependencias del proyecto
└── README.md                  # Esta documentación
```

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 💻 Cómo Ejecutar Localmente

### Ejemplo Principal
```bash
python github_actions_example.py
```

### Testing Individual con pytest
```bash
# Todos los tests
pytest github_actions_example.py -v

# Tests específicos
pytest github_actions_example.py::test_calculator_operations -v
pytest github_actions_example.py::test_data_processor -v
pytest github_actions_example.py::test_api_simulator -v
```

### Coverage Report
```bash
pytest --cov=. --cov-report=html github_actions_example.py
open htmlcov/index.html
```

### Code Quality Checks
```bash
# Linting
flake8 github_actions_example.py

# Code formatting
black github_actions_example.py

# Type checking
mypy github_actions_example.py --ignore-missing-imports

# Import sorting
isort github_actions_example.py
```

### Security Scanning
```bash
# Vulnerability scanning
bandit -r . -v

# Dependency checking
safety check
```

## 🔧 GitHub Actions Workflow

El workflow `.github/workflows/ci.yml` implementa un pipeline completo con:

### 1. **Code Quality (lint)**
- Linting con flake8
- Formatting check con black
- Import sorting con isort
- Type checking con mypy

### 2. **Security Scanning (security)**
- Vulnerability scanning con bandit
- Dependency checking con safety
- Artifact upload de reportes

### 3. **Unit Tests (unit-tests)**
- Matrix testing: Python 3.8-3.12
- Multi-OS: Ubuntu, Windows
- Coverage reporting
- Parallel execution

### 4. **Integration Tests (integration-tests)**
- Tests con servicios (Redis)
- API simulation testing
- End-to-end scenarios

### 5. **Performance Tests (performance-tests)**
- Benchmarking con pytest-benchmark
- Solo en branch main
- Performance regression detection

### 6. **Build Artifacts (build)**
- Package building
- Artifact creation y upload
- Distribution preparation

### 7. **Deployment (deploy)**
- Conditional deployment
- Environment-specific configs
- Smoke testing
- Rollback en fallos

### 8. **Quality Gates (quality-gate)**
- Status consolidation
- Final reporting
- Pipeline success validation

## ⚡ Características del Workflow

### Triggers Configurados
```yaml
on:
  push:
    branches: [main, develop]
    paths: ['src/**', 'tests/**', '*.py']
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily
  workflow_dispatch:     # Manual trigger
```

### Matrix Testing
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.8', '3.9', '3.10', '3.11']
    include:
      - python-version: '3.12'
        os: ubuntu-latest
        experimental: true
```

### Caching Optimizado
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Services Integration
```yaml
services:
  redis:
    image: redis:6
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
```

## 📊 Componentes del Script Principal

### 1. **Calculator Class**
- Operaciones matemáticas básicas
- Manejo de errores (división por cero)
- Testing de funciones puras

### 2. **DataProcessor Class**
- Procesamiento de datos con validación
- Estadísticas y filtrado
- Testing de estado y transformaciones

### 3. **ApiSimulator Class**
- Simulación de APIs externas
- Control de latencia y fallos
- Testing de servicios remotos

### 4. **TestRunner Class**
- Runner personalizado para CI/CD
- Generación de reportes JSON
- Métricas de performance

## 🎯 Best Practices Implementadas

### Performance
- ✅ Caching de dependencias y resultados
- ✅ Ejecución de tests en paralelo
- ✅ Fail fast en errores de lint/syntax
- ✅ Matrix testing para compatibilidad

### Reliability
- ✅ Pin de versiones de actions (v3, no @main)
- ✅ Timeouts para evitar workflows colgados
- ✅ Conditional steps para diferentes branches
- ✅ Proper error handling y rollbacks

### Security
- ✅ Secrets para información sensible
- ✅ Restricted permissions (GITHUB_TOKEN)
- ✅ Validation de external inputs
- ✅ Trusted actions únicamente

### Maintainability
- ✅ Workflows organizados por propósito
- ✅ Documentación de logic compleja
- ✅ Monitoring de workflow performance
- ✅ Artifacts para debugging

## 🔍 Comandos de CI/CD

### Simular Workflow Localmente
```bash
# Install act (GitHub Actions local runner)
# brew install act  # en macOS
# choco install act  # en Windows

# Run workflow locally
act push
```

### Debugging de Workflows
```bash
# Enable debug logging
# Set repository secret: ACTIONS_STEP_DEBUG = true
# Set repository secret: ACTIONS_RUNNER_DEBUG = true
```

### Manual Workflow Trigger
```bash
# Via GitHub CLI
gh workflow run ci.yml

# Con inputs
gh workflow run ci.yml -f environment=production
```

## 📈 Métricas y Monitoring

### Coverage Thresholds
- Unit tests: >80% coverage
- Integration tests: >70% coverage
- Combined: >85% coverage

### Performance Benchmarks
- API response time: <100ms
- Test execution: <15 min total
- Build time: <5 min

### Quality Gates
- Zero security vulnerabilities (high/critical)
- All linting checks pass
- All type checks pass
- No performance regressions

## 🚨 Troubleshooting

### Workflow Failures
1. Check logs en GitHub Actions tab
2. Verify dependencies en requirements.txt
3. Ensure secrets están configurados
4. Check branch protection rules

### Local Testing Issues
```bash
# Clear pytest cache
pytest --cache-clear

# Verbose output
pytest -v -s github_actions_example.py

# Debug específico
pytest --pdb github_actions_example.py::test_name
```

### Performance Issues
```bash
# Profile test execution
pytest --durations=10 github_actions_example.py

# Memory profiling
pytest --memray github_actions_example.py
```

## 🎓 Conceptos Demostrados

1. **Fail Fast Principle**: Errores tempranos para feedback rápido
2. **Matrix Testing**: Compatibilidad across versions y OS
3. **Conditional Execution**: Logic específica por branch/evento
4. **Artifact Management**: Preservación de builds y reportes
5. **Quality Gates**: Prevención de deployments defectuosos
6. **Parallel Execution**: Optimización de tiempo total
7. **Environment Management**: Staging → Production flow

## 📝 Próximos Pasos

1. Configurar branch protection rules
2. Añadir integration con Slack/Teams
3. Implementar blue-green deployments
4. Añadir monitoring con Prometheus
5. Configurar alerting automático

¡Experimenta con diferentes configuraciones de workflow para optimizar tu pipeline de CI/CD!
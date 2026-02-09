# SESIÓN 8: Pruebas con Selenium

Sistema completo de testing E2E con Selenium WebDriver y Page Object Model

## 🎯 Objetivos

- Configurar Selenium WebDriver para testing automatizado de UI
- Implementar el patrón Page Object Model para tests mantenibles
- Crear tests end-to-end robustos y confiables
- Manejar elementos dinámicos, waits y sincronización
- Integrar Selenium tests en pipelines de CI/CD
- Implementar testing cross-browser y responsive
- Configurar reporting y debugging avanzado

## 📁 Estructura del Proyecto

```
proyecto/
├── selenium_tests_example.py   # Script principal con Page Object Model
├── requirements.txt           # Dependencias de Selenium y testing
├── pytest.ini               # Configuración de pytest
├── conftest.py              # Fixtures compartidos
├── screenshots/             # Screenshots automáticos en fallos
├── reports/                 # Reportes HTML de tests
└── README.md               # Esta documentación
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.8+
- Google Chrome o Firefox instalado
- (Opcional) Docker para Selenium Grid

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

**Nota**: Los drivers de navegador se descargan automáticamente usando `webdriver-manager`.

## 💻 Cómo Ejecutar

### Ejemplo Principal
```bash
python selenium_tests_example.py
```

### Tests con pytest
```bash
# Ejecutar todos los tests
pytest selenium_tests_example.py -v

# Ejecutar con reporte HTML
pytest selenium_tests_example.py --html=reports/report.html --self-contained-html

# Ejecutar en paralelo
pytest selenium_tests_example.py -n 2

# Ejecutar tests específicos
pytest selenium_tests_example.py::SeleniumTestSuite::test_successful_login -v
```

### Modo Headless (para CI/CD)
```bash
# Editar configuración en el script
config = TestConfig(
    headless=True,
    screenshot_on_failure=True
)
```

### Cross-Browser Testing
```bash
# El script incluye función para múltiples navegadores
# Editar la lista de browsers en run_cross_browser_tests()
```

## 🏗️ Arquitectura del Código

### 1. **Page Object Model (POM)**
El código implementa el patrón Page Object Model para separar la lógica de testing de los detalles de la UI:

```python
class LoginPage(BasePage):
    # Locators centralizados
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    
    # Métodos de acción
    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
```

### 2. **Gestión de Drivers**
```python
class DriverManager:
    @staticmethod
    def get_chrome_driver(headless: bool = False):
        # Configuración automática con webdriver-manager
        # Optimizaciones para CI/CD
        # Performance tuning
```

### 3. **Base Page Class**
Funcionalidad común para todas las páginas:
- Explicit waits
- Manejo de elementos
- Screenshots automáticos
- Utilidades de navegación

## 🔧 Características Implementadas

### 1. **Tests E2E Completos**
- ✅ Login exitoso y fallido
- ✅ Contenido dinámico
- ✅ Upload de archivos
- ✅ Múltiples ventanas
- ✅ Drag and drop
- ✅ Elementos interactivos

### 2. **Waits y Sincronización**
```python
# Explicit waits
self.wait.until(EC.element_to_be_clickable(locator))

# Custom waits
def wait_for_content_change(self, original_content):
    self.wait.until(lambda driver: 
        self.get_page_content() != original_content
    )
```

### 3. **Debugging y Reporting**
- Screenshots automáticos en fallos
- Logging estructurado
- Reportes HTML detallados
- Console logs capture

### 4. **Configuración para CI/CD**
```python
# Headless mode
options.add_argument('--headless')

# CI optimizations
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
```

## 🌐 Cross-Browser Testing

### Navegadores Soportados
- ✅ Chrome (por defecto)
- ✅ Firefox
- ✅ Edge (con configuración adicional)
- ✅ Safari (solo macOS)

### Configuración de Browsers
```python
BROWSERS = {
    'chrome': DriverManager.get_chrome_driver,
    'firefox': DriverManager.get_firefox_driver,
    # Añadir más según necesidad
}
```

## 🐳 Docker Integration

### Selenium Grid con Docker
```bash
# Levantar Selenium Hub + Nodos
docker run -d -p 4444:4444 --name selenium-hub selenium/hub:4.15.0

# Nodo Chrome
docker run -d --link selenium-hub:hub selenium/node-chrome:4.15.0

# Nodo Firefox
docker run -d --link selenium-hub:hub selenium/node-firefox:4.15.0
```

### Conectar a Selenium Grid
```python
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)
```

## 📊 Configuraciones Avanzadas

### pytest.ini
```ini
[tool:pytest]
testpaths = .
python_files = *test*.py
python_classes = Test* *TestSuite
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --html=reports/report.html
    --self-contained-html
markers =
    smoke: Smoke tests
    regression: Regression tests
    slow: Slow tests
```

### conftest.py
```python
@pytest.fixture(scope="session")
def driver():
    driver = DriverManager.get_chrome_driver(headless=True)
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    if request.node.rep_call.failed:
        # Tomar screenshot automáticamente
        pass
```

## 🔍 Debugging y Troubleshooting

### Screenshots Automáticos
Los tests toman screenshots automáticamente cuando fallan:
```
screenshots/
├── failure_Login_Exitoso_20231101_143022.png
├── failure_Dynamic_Content_20231101_143055.png
└── ...
```

### Logs de Navegador
```python
# Capturar console logs
logs = driver.get_log('browser')
for log in logs:
    if log['level'] == 'SEVERE':
        print(f"JavaScript error: {log['message']}")
```

### Debugging Interactivo
```python
# Pausar ejecución para debugging
import pdb; pdb.set_trace()

# O usar time.sleep() para observar
time.sleep(5)
```

## ⚡ Best Practices Implementadas

### Reliability
- ✅ Always use explicit waits
- ✅ Implement retry mechanisms for flaky elements
- ✅ Use stable locators (ID > CSS > XPath)
- ✅ Avoid testing implementation details

### Performance
- ✅ Run tests in parallel where possible
- ✅ Use headless mode in CI
- ✅ Disable images/extensions for speed
- ✅ Implement smart test selection

### Maintainability
- ✅ Use Page Object Model consistently
- ✅ Keep tests focused and atomic
- ✅ Extract common functionality to base classes
- ✅ Use data-test attributes for stable selection

### Debugging
- ✅ Take screenshots on failures
- ✅ Capture browser logs
- ✅ Use explicit test names
- ✅ Implement proper error messages

## 🚫 Antipatterns Evitados

### ❌ Hard-coded sleeps
```python
# MAL
time.sleep(5)  # Siempre espera, lento e impredecible

# BIEN
self.wait.until(EC.element_to_be_clickable(locator))
```

### ❌ Brittle locators
```python
# MAL
driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/span[1]/button")

# BIEN
driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-button']")
```

### ❌ Tests demasiado largos
```python
# MAL
def test_entire_user_journey():  # 50+ pasos
    login()
    create_account()
    # ... 30 más pasos

# BIEN
def test_login(): pass
def test_create_account(): pass
def test_purchase_flow(): pass
```

## 🎯 Casos de Uso del Script

### 1. **Testing de Login**
- Credenciales válidas e inválidas
- Mensajes de error
- Redirección post-login

### 2. **Contenido Dinámico**
- AJAX loading
- Content refresh
- State changes

### 3. **Interacciones Complejas**
- File uploads
- Drag and drop
- Multiple windows
- Form submissions

### 4. **Validaciones de UI**
- Element visibility
- Text verification
- URL changes
- Page loading states

## 🔗 Integración con CI/CD

### GitHub Actions Example
```yaml
- name: Run Selenium Tests
  run: |
    # Setup display for headless
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    
    # Install Chrome
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install google-chrome-stable
    
    # Run tests
    pytest selenium_tests_example.py --html=report.html
```

### Docker Pipeline
```dockerfile
FROM python:3.9-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy tests
COPY . .

# Run tests
CMD ["pytest", "selenium_tests_example.py", "--html=report.html"]
```

## 📈 Métricas y Reporting

### Success Metrics
- Test execution time
- Success/failure rates
- Cross-browser compatibility
- Screenshot evidence

### Reporting Features
- HTML reports con screenshots
- Test duration tracking
- Error categorization
- Browser compatibility matrix

## 🛠️ Comandos Útiles

```bash
# Ejecutar tests con diferentes configuraciones
pytest --browser=chrome --headless=true
pytest --browser=firefox --resolution=1920x1080

# Ejecutar solo smoke tests
pytest -m smoke

# Ejecutar con retry en fallos
pytest --reruns 2 --reruns-delay 1

# Generar reporte con coverage
pytest --cov=. --cov-report=html

# Debug mode
pytest -s --pdb --tb=long
```

## 🔜 Próximos Pasos

1. **Integrar con Selenium Grid**
2. **Añadir tests de performance**
3. **Implementar visual regression testing**
4. **Configurar parallel execution avanzado**
5. **Añadir mobile testing con Appium**

¡Experimenta con diferentes escenarios de testing para dominar Selenium y automatización de UI!
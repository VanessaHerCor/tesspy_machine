"""
Configuración compartida para tests de Selenium
Fixtures y hooks para pytest
"""

import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def test_config():
    """Configuración global para tests"""
    return {
        'base_url': 'https://the-internet.herokuapp.com',
        'implicit_wait': 10,
        'explicit_wait': 15,
        'headless': os.getenv('SELENIUM_HEADLESS', 'false').lower() == 'true',
        'browser': os.getenv('SELENIUM_BROWSER', 'chrome'),
        'timeout': int(os.getenv('SELENIUM_TIMEOUT', '10')),
        'screenshot_on_failure': True
    }


@pytest.fixture(scope="function")
def driver(test_config):
    """Fixture para WebDriver con configuración automática"""
    
    # Configurar opciones de Chrome
    options = Options()
    
    if test_config['headless']:
        options.add_argument('--headless')
    
    # Configuraciones para estabilidad
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    
    # Configurar servicio
    service = Service(ChromeDriverManager().install())
    
    # Crear driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(test_config['implicit_wait'])
    driver.maximize_window()
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver, test_config):
    """Toma screenshot automáticamente cuando un test falla"""
    yield
    
    if request.node.rep_call.failed and test_config['screenshot_on_failure']:
        # Crear directorio de screenshots si no existe
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("::", "_").replace(" ", "_")
        filename = f"failure_{test_name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        try:
            driver.save_screenshot(filepath)
            print(f"\n📸 Screenshot guardado: {filepath}")
        except Exception as e:
            print(f"\n⚠️ Error tomando screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar el resultado de cada test"""
    outcome = yield
    rep = outcome.get_result()
    
    # Agregar resultado al item para uso en otros fixtures
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuración inicial del entorno de testing"""
    # Crear directorios necesarios
    directories = ["screenshots", "reports", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("\n🚀 Configurando entorno de testing...")
    print(f"   📁 Directorios creados: {', '.join(directories)}")
    
    yield
    
    print("\n🏁 Finalizando entorno de testing...")


@pytest.fixture(scope="function")
def page_factory(driver, test_config):
    """Factory para crear Page Objects"""
    from selenium_tests_example import LoginPage, SecurePage, DynamicContentPage, FileUploadPage
    
    return {
        'login': lambda: LoginPage(driver, test_config),
        'secure': lambda: SecurePage(driver, test_config),
        'dynamic': lambda: DynamicContentPage(driver, test_config),
        'upload': lambda: FileUploadPage(driver, test_config)
    }


@pytest.fixture(scope="function")
def test_data():
    """Datos de prueba para tests"""
    return {
        'valid_credentials': {
            'username': 'tomsmith',
            'password': 'SuperSecretPassword!'
        },
        'invalid_credentials': {
            'username': 'invaliduser',
            'password': 'invalidpass'
        },
        'test_files': {
            'text_file': 'test_upload.txt',
            'image_file': 'test_image.png'
        }
    }


@pytest.fixture(scope="function")
def wait_helper(driver, test_config):
    """Helper para waits personalizados"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    class WaitHelper:
        def __init__(self, driver, timeout):
            self.driver = driver
            self.wait = WebDriverWait(driver, timeout)
        
        def until_clickable(self, locator):
            return self.wait.until(EC.element_to_be_clickable(locator))
        
        def until_visible(self, locator):
            return self.wait.until(EC.visibility_of_element_located(locator))
        
        def until_present(self, locator):
            return self.wait.until(EC.presence_of_element_located(locator))
        
        def until_url_contains(self, text):
            return self.wait.until(EC.url_contains(text))
        
        def until_text_present(self, locator, text):
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
    
    return WaitHelper(driver, test_config['explicit_wait'])


# Configuración de marcadores para ejecución selectiva
def pytest_configure(config):
    """Configuración adicional de pytest"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modificar tests recolectados"""
    # Agregar marcador 'slow' a tests que toman mucho tiempo
    slow_tests = ["test_file_upload", "test_drag_and_drop"]
    
    for item in items:
        if any(slow_test in item.name for slow_test in slow_tests):
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="session")
def browser_capabilities():
    """Capacidades de navegador para testing avanzado"""
    return {
        'chrome': {
            'browserName': 'chrome',
            'version': 'latest',
            'platform': 'ANY'
        },
        'firefox': {
            'browserName': 'firefox',
            'version': 'latest',
            'platform': 'ANY'
        }
    }


# Fixture para parallel testing
@pytest.fixture(scope="session")
def worker_id(request):
    """ID del worker para testing paralelo"""
    return getattr(request.config, 'workerinput', {}).get('workerid', 'master')


@pytest.fixture(scope="function")
def unique_test_data(worker_id):
    """Datos únicos por worker para evitar conflictos"""
    timestamp = datetime.now().strftime("%H%M%S")
    return {
        'unique_id': f"{worker_id}_{timestamp}",
        'test_file': f"test_file_{worker_id}_{timestamp}.txt"
    }
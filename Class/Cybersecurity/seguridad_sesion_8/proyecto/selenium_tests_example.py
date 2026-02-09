"""
Sesión 8: Pruebas con Selenium
Script de ejemplo con Page Object Model y testing E2E automatizado
"""

import time
import os
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

# Importaciones condicionales para manejo de dependencias
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    print("⚠️ pytest no disponible - algunos features limitados")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("❌ Selenium no disponible - ejecutando en modo simulado")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("⚠️ webdriver-manager no disponible - usando driver del sistema")


@dataclass
class TestConfig:
    """Configuración para tests de Selenium"""
    base_url: str = "https://the-internet.herokuapp.com"
    implicit_wait: int = 10
    explicit_wait: int = 15
    headless: bool = False
    screenshot_on_failure: bool = True
    browser: str = "chrome"


class DriverManager:
    """Gestor de WebDriver con configuración optimizada"""
    
    @staticmethod
    def get_chrome_driver(headless: bool = False):
        """Obtiene driver de Chrome configurado"""
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # Configuraciones para CI/CD
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Optimizaciones de rendimiento
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Para tests más rápidos
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    @staticmethod
    def get_firefox_driver(headless: bool = False) -> webdriver.Firefox:
        """Obtiene driver de Firefox configurado"""
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from webdriver_manager.firefox import GeckoDriverManager
        
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)


class BasePage:
    """Clase base para todas las Page Objects"""
    
    def __init__(self, driver: webdriver.Chrome, config: TestConfig):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.explicit_wait)
    
    def find_element(self, locator: tuple) -> webdriver.remote.webelement.WebElement:
        """Encuentra elemento con wait explícito"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: tuple) -> List[webdriver.remote.webelement.WebElement]:
        """Encuentra múltiples elementos"""
        return self.driver.find_elements(*locator)
    
    def click(self, locator: tuple) -> None:
        """Click en elemento con wait para que sea clickeable"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator: tuple, text: str) -> None:
        """Envía texto a elemento"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: tuple) -> str:
        """Obtiene texto de elemento"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Verifica si elemento es visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_change(self, expected_url: str, timeout: int = 10) -> bool:
        """Espera cambio de URL"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(expected_url)
            )
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator: tuple) -> None:
        """Scroll hacia elemento"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, name: str) -> str:
        """Toma screenshot y retorna el path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{name}_{timestamp}.png"
        
        # Crear directorio si no existe
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath


class LoginPage(BasePage):
    """Page Object para página de login"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.ID, "flash")
    
    def navigate_to(self) -> None:
        """Navega a la página de login"""
        self.driver.get(f"{self.config.base_url}/login")
    
    def enter_username(self, username: str) -> None:
        """Ingresa nombre de usuario"""
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Ingresa contraseña"""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login(self) -> None:
        """Click en botón de login"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """Proceso completo de login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        """Obtiene mensaje de error"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_login_successful(self) -> bool:
        """Verifica si login fue exitoso"""
        return self.wait_for_url_change("/secure", timeout=5)


class SecurePage(BasePage):
    """Page Object para página segura (después del login)"""
    
    # Locators
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href='/logout']")
    SUCCESS_MESSAGE = (By.ID, "flash")
    SECURE_AREA_TEXT = (By.CSS_SELECTOR, "h2")
    
    def is_loaded(self) -> bool:
        """Verifica si la página está cargada"""
        try:
            self.wait.until(EC.presence_of_element_located(self.SECURE_AREA_TEXT))
            return "Secure Area" in self.get_text(self.SECURE_AREA_TEXT)
        except TimeoutException:
            return False
    
    def logout(self) -> None:
        """Hace logout"""
        self.click(self.LOGOUT_BUTTON)
    
    def get_success_message(self) -> str:
        """Obtiene mensaje de éxito"""
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=3):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""


class DynamicContentPage(BasePage):
    """Page Object para contenido dinámico"""
    
    # Locators
    CONTENT_DIVS = (By.CSS_SELECTOR, "#content .row")
    REFRESH_BUTTON = (By.CSS_SELECTOR, "a[href='/dynamic_content']")
    
    def navigate_to(self) -> None:
        """Navega a página de contenido dinámico"""
        self.driver.get(f"{self.config.base_url}/dynamic_content")
    
    def click_refresh(self) -> None:
        """Click en refresh"""
        self.click(self.REFRESH_BUTTON)
    
    def wait_for_content_change(self, original_content: str) -> bool:
        """Espera a que el contenido cambie"""
        try:
            self.wait.until(lambda driver: 
                self.get_page_content() != original_content
            )
            return True
        except TimeoutException:
            return False
    
    def get_page_content(self) -> str:
        """Obtiene contenido de la página"""
        elements = self.find_elements(self.CONTENT_DIVS)
        return "".join([elem.text for elem in elements])


class FileUploadPage(BasePage):
    """Page Object para upload de archivos"""
    
    # Locators
    FILE_INPUT = (By.ID, "file-upload")
    UPLOAD_BUTTON = (By.ID, "file-submit")
    UPLOADED_FILES = (By.ID, "uploaded-files")
    
    def navigate_to(self) -> None:
        """Navega a página de upload"""
        self.driver.get(f"{self.config.base_url}/upload")
    
    def upload_file(self, file_path: str) -> None:
        """Sube archivo"""
        # Crear archivo temporal para el test
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("Test file content")
        
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(os.path.abspath(file_path))
        self.click(self.UPLOAD_BUTTON)
    
    def is_file_uploaded(self, filename: str) -> bool:
        """Verifica si archivo fue subido"""
        try:
            self.wait.until(EC.presence_of_element_located(self.UPLOADED_FILES))
            uploaded_text = self.get_text(self.UPLOADED_FILES)
            return filename in uploaded_text
        except TimeoutException:
            return False


class SeleniumTestSuite:
    """Suite de tests de Selenium"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.driver = None
        self.results = []
    
    def setup_driver(self) -> None:
        """Configura el driver"""
        if self.config.browser.lower() == "chrome":
            self.driver = DriverManager.get_chrome_driver(self.config.headless)
        elif self.config.browser.lower() == "firefox":
            self.driver = DriverManager.get_firefox_driver(self.config.headless)
        else:
            raise ValueError(f"Browser {self.config.browser} not supported")
        
        self.driver.implicitly_wait(self.config.implicit_wait)
        self.driver.maximize_window()
    
    def teardown_driver(self) -> None:
        """Cierra el driver"""
        if self.driver:
            self.driver.quit()
    
    def run_test(self, test_name: str, test_func) -> Dict[str, Any]:
        """Ejecuta un test individual"""
        print(f"\n🧪 Ejecutando: {test_name}")
        start_time = time.time()
        
        try:
            test_func()
            duration = time.time() - start_time
            result = {
                'name': test_name,
                'status': 'PASSED',
                'duration': duration,
                'error': None
            }
            print(f"✅ {test_name} - PASSED ({duration:.2f}s)")
        except Exception as e:
            duration = time.time() - start_time
            result = {
                'name': test_name,
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
            print(f"❌ {test_name} - FAILED ({duration:.2f}s): {e}")
            
            # Screenshot en fallo
            if self.config.screenshot_on_failure and self.driver:
                try:
                    base_page = BasePage(self.driver, self.config)
                    screenshot_path = base_page.take_screenshot(f"failure_{test_name}")
                    result['screenshot'] = screenshot_path
                    print(f"📸 Screenshot guardado: {screenshot_path}")
                except Exception as screenshot_error:
                    print(f"⚠️ Error tomando screenshot: {screenshot_error}")
        
        self.results.append(result)
        return result
    
    def test_successful_login(self) -> None:
        """Test de login exitoso"""
        login_page = LoginPage(self.driver, self.config)
        secure_page = SecurePage(self.driver, self.config)
        
        login_page.navigate_to()
        login_page.login("tomsmith", "SuperSecretPassword!")
        
        assert login_page.is_login_successful(), "Login debería ser exitoso"
        assert secure_page.is_loaded(), "Página segura debería cargar"
        assert "You logged into a secure area!" in secure_page.get_success_message()
    
    def test_failed_login(self) -> None:
        """Test de login fallido"""
        login_page = LoginPage(self.driver, self.config)
        
        login_page.navigate_to()
        login_page.login("invaliduser", "invalidpass")
        
        assert not login_page.is_login_successful(), "Login debería fallar"
        error_message = login_page.get_error_message()
        assert "Your username is invalid!" in error_message, f"Mensaje de error incorrecto: {error_message}"
    
    def test_dynamic_content(self) -> None:
        """Test de contenido dinámico"""
        dynamic_page = DynamicContentPage(self.driver, self.config)
        
        dynamic_page.navigate_to()
        original_content = dynamic_page.get_page_content()
        
        dynamic_page.click_refresh()
        
        # Verificar que el contenido cambió
        content_changed = dynamic_page.wait_for_content_change(original_content)
        assert content_changed, "El contenido dinámico debería cambiar después del refresh"
    
    def test_file_upload(self) -> None:
        """Test de subida de archivo"""
        upload_page = FileUploadPage(self.driver, self.config)
        
        # Crear archivo temporal
        test_file = "test_upload.txt"
        upload_page.navigate_to()
        upload_page.upload_file(test_file)
        
        # Verificar que el archivo se subió
        assert upload_page.is_file_uploaded(test_file), "El archivo debería subirse exitosamente"
        
        # Limpiar archivo temporal
        if os.path.exists(test_file):
            os.remove(test_file)
    
    def test_multiple_windows(self) -> None:
        """Test de manejo de múltiples ventanas"""
        self.driver.get(f"{self.config.base_url}/windows")
        
        # Click en link que abre nueva ventana
        new_window_link = self.driver.find_element(By.LINK_TEXT, "Click Here")
        new_window_link.click()
        
        # Cambiar a nueva ventana
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        # Verificar contenido de nueva ventana
        wait = WebDriverWait(self.driver, self.config.explicit_wait)
        new_window_text = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h3"))
        ).text
        
        assert "New Window" in new_window_text, "Debería estar en la nueva ventana"
        
        # Volver a ventana original
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        # Verificar que estamos de vuelta
        original_text = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Opening a new window" in original_text, "Debería estar de vuelta en la ventana original"
    
    def test_drag_and_drop(self) -> None:
        """Test de drag and drop"""
        self.driver.get(f"{self.config.base_url}/drag_and_drop")
        
        source = self.driver.find_element(By.ID, "column-a")
        target = self.driver.find_element(By.ID, "column-b")
        
        # Verificar estado inicial
        assert source.text == "A", "Columna A debería contener 'A' inicialmente"
        assert target.text == "B", "Columna B debería contener 'B' inicialmente"
        
        # Realizar drag and drop
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        
        # Verificar que se intercambiaron
        time.sleep(1)  # Pequeña pausa para que se complete la animación
        assert source.text == "B", "Columna A debería contener 'B' después del drag"
        assert target.text == "A", "Columna B debería contener 'A' después del drop"
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Ejecuta todos los tests"""
        print("🚀 SESIÓN 8: PRUEBAS CON SELENIUM")
        print("=" * 40)
        
        try:
            self.setup_driver()
            
            # Ejecutar tests
            self.run_test("Login Exitoso", self.test_successful_login)
            self.run_test("Login Fallido", self.test_failed_login)
            self.run_test("Contenido Dinámico", self.test_dynamic_content)
            self.run_test("Subida de Archivo", self.test_file_upload)
            self.run_test("Múltiples Ventanas", self.test_multiple_windows)
            self.run_test("Drag and Drop", self.test_drag_and_drop)
            
        finally:
            self.teardown_driver()
        
        # Generar resumen
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        failed = len([r for r in self.results if r['status'] == 'FAILED'])
        total_duration = sum([r['duration'] for r in self.results])
        
        summary = {
            'total': len(self.results),
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / len(self.results)) * 100 if self.results else 0,
            'total_duration': total_duration,
            'results': self.results
        }
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DE RESULTADOS:")
        print(f"   Total: {summary['total']}")
        print(f"   Passed: {summary['passed']}")
        print(f"   Failed: {summary['failed']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Duration: {summary['total_duration']:.2f}s")
        
        if failed > 0:
            print(f"\n❌ {failed} tests fallaron")
            for result in self.results:
                if result['status'] == 'FAILED':
                    print(f"   • {result['name']}: {result['error']}")
        else:
            print(f"\n✅ Todos los tests pasaron exitosamente")
        
        return summary


def run_cross_browser_tests() -> None:
    """Ejecuta tests en múltiples navegadores"""
    browsers = ["chrome"]  # Podemos añadir "firefox" si está instalado
    
    for browser in browsers:
        print(f"\n🌐 Testing en {browser.upper()}")
        print("-" * 30)
        
        config = TestConfig(
            browser=browser,
            headless=True,  # Para CI/CD
            screenshot_on_failure=True
        )
        
        suite = SeleniumTestSuite(config)
        summary = suite.run_all_tests()
        
        print(f"\n{browser.upper()} - Success Rate: {summary['success_rate']:.1f}%")


if __name__ == "__main__":
    # Configuración por defecto
    config = TestConfig(
        headless=False,  # Cambiar a True para headless
        screenshot_on_failure=True
    )
    
    # Ejecutar suite de tests
    suite = SeleniumTestSuite(config)
    results = suite.run_all_tests()
    
    print(f"\n🎯 Este script demuestra:")
    print("   • Page Object Model para tests mantenibles")
    print("   • Explicit waits para tests estables")
    print("   • Manejo de elementos dinámicos")
    print("   • Testing de funcionalidades complejas")
    print("   • Screenshots automáticos en fallos")
    print("   • Cross-browser testing capabilities")
    print("   • Configuración para CI/CD")
    
    # Exit code basado en resultados
    exit_code = 0 if results['failed'] == 0 else 1
    exit(exit_code)
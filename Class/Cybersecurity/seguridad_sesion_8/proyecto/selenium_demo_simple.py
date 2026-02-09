"""
Sesión 8: Pruebas con Selenium - Demo Simplificado
Script de demostración que funciona con o sin dependencias de Selenium
"""

import time
import os
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

# Verificar disponibilidad de Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
    print("✅ Selenium está disponible")
except ImportError:
    SELENIUM_AVAILABLE = False
    print("❌ Selenium no está disponible - ejecutando en modo simulado")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    WEBDRIVER_MANAGER_AVAILABLE = True
    print("✅ WebDriver Manager está disponible")
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("⚠️ WebDriver Manager no disponible")


@dataclass
class TestConfig:
    """Configuración para tests de Selenium"""
    base_url: str = "https://the-internet.herokuapp.com"
    timeout: int = 10
    headless: bool = True  # Por defecto headless para CI
    simulate_mode: bool = not SELENIUM_AVAILABLE


class SeleniumSimulator:
    """Simulador para demostrar conceptos cuando Selenium no está disponible"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.current_url = ""
        self.page_title = ""
        self.elements = {}
    
    def get(self, url: str) -> None:
        """Simula navegación a URL"""
        self.current_url = url
        print(f"🌐 Navegando a: {url}")
        time.sleep(0.5)  # Simular tiempo de carga
        
        # Simular contenido según la URL
        if "/login" in url:
            self.page_title = "Login Page"
            self.elements = {
                "username": "",
                "password": "",
                "login_button": "enabled"
            }
        elif "/secure" in url:
            self.page_title = "Secure Area"
            self.elements = {
                "success_message": "You logged into a secure area!",
                "logout_button": "enabled"
            }
    
    def find_element(self, by: str, value: str) -> Dict[str, str]:
        """Simula búsqueda de elemento"""
        print(f"🔍 Buscando elemento: {by}='{value}'")
        return {"type": "element", "selector": value, "found": True}
    
    def send_keys(self, element: Dict, text: str) -> None:
        """Simula envío de texto"""
        print(f"⌨️ Escribiendo: '{text}' en {element['selector']}")
        time.sleep(0.2)
    
    def click(self, element: Dict) -> None:
        """Simula click"""
        print(f"🖱️ Haciendo click en: {element['selector']}")
        time.sleep(0.3)
    
    def get_text(self, element: Dict) -> str:
        """Simula obtener texto"""
        if "success" in element['selector']:
            return "You logged into a secure area!"
        return "Sample text"
    
    def take_screenshot(self, filename: str) -> None:
        """Simula screenshot"""
        print(f"📸 Screenshot simulado: {filename}")
    
    def quit(self) -> None:
        """Simula cerrar navegador"""
        print("🚪 Cerrando navegador simulado")


class RealSeleniumDriver:
    """Wrapper para Selenium real"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.driver = self._create_driver()
    
    def _create_driver(self):
        """Crea driver real de Selenium"""
        options = Options()
        
        if self.config.headless:
            options.add_argument('--headless')
        
        # Configuraciones para estabilidad
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            else:
                # Usar driver del sistema
                driver = webdriver.Chrome(options=options)
            
            driver.implicitly_wait(self.config.timeout)
            return driver
        except Exception as e:
            print(f"❌ Error creando driver: {e}")
            return None
    
    def get(self, url: str) -> None:
        """Navegar a URL"""
        if self.driver:
            self.driver.get(url)
            print(f"🌐 Navegando a: {url}")
    
    def find_element(self, by: str, value: str):
        """Buscar elemento"""
        if self.driver:
            return self.driver.find_element(by, value)
        return None
    
    def take_screenshot(self, filename: str) -> None:
        """Tomar screenshot"""
        if self.driver:
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot guardado: {filepath}")
    
    def quit(self) -> None:
        """Cerrar navegador"""
        if self.driver:
            self.driver.quit()
            print("🚪 Cerrando navegador")


class LoginPageTest:
    """Page Object para testing de login"""
    
    def __init__(self, driver, config: TestConfig):
        self.driver = driver
        self.config = config
    
    def navigate_to_login(self) -> None:
        """Navegar a página de login"""
        login_url = f"{self.config.base_url}/login"
        self.driver.get(login_url)
    
    def login(self, username: str, password: str) -> bool:
        """Realizar login"""
        try:
            if SELENIUM_AVAILABLE and not self.config.simulate_mode:
                # Selenium real
                username_field = self.driver.find_element(By.ID, "username")
                password_field = self.driver.find_element(By.ID, "password")
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                
                username_field.clear()
                username_field.send_keys(username)
                password_field.clear()
                password_field.send_keys(password)
                login_button.click()
                
                # Verificar login exitoso
                wait = WebDriverWait(self.driver.driver, self.config.timeout)
                wait.until(EC.url_contains("/secure"))
                print("✅ Login exitoso")
                return True
            else:
                # Simulación
                username_elem = self.driver.find_element("id", "username")
                password_elem = self.driver.find_element("id", "password")
                login_button = self.driver.find_element("css", "button[type='submit']")
                
                self.driver.send_keys(username_elem, username)
                self.driver.send_keys(password_elem, password)
                self.driver.click(login_button)
                
                # Simular navegación exitosa
                self.driver.get(f"{self.config.base_url}/secure")
                print("✅ Login simulado exitoso")
                return True
                
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return False
    
    def verify_secure_area(self) -> bool:
        """Verificar que estamos en área segura"""
        try:
            if SELENIUM_AVAILABLE and not self.config.simulate_mode:
                success_element = self.driver.find_element(By.ID, "flash")
                message = success_element.text
                return "You logged into a secure area" in message
            else:
                # Simulación
                success_element = self.driver.find_element("id", "flash")
                message = self.driver.get_text(success_element)
                return "You logged into a secure area" in message
        except Exception as e:
            print(f"⚠️ Error verificando área segura: {e}")
            return False


class SeleniumTestSuite:
    """Suite de tests de Selenium"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.results = []
        
        if config.simulate_mode or not SELENIUM_AVAILABLE:
            self.driver = SeleniumSimulator(config)
        else:
            self.driver = RealSeleniumDriver(config)
    
    def run_test(self, test_name: str, test_func) -> Dict[str, Any]:
        """Ejecutar un test individual"""
        print(f"\n🧪 Ejecutando: {test_name}")
        start_time = time.time()
        
        try:
            success = test_func()
            duration = time.time() - start_time
            result = {
                'name': test_name,
                'status': 'PASSED' if success else 'FAILED',
                'duration': duration,
                'error': None if success else 'Test returned False'
            }
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {test_name} - {result['status']} ({duration:.2f}s)")
            
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
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"failure_{test_name}_{timestamp}.png"
                self.driver.take_screenshot(screenshot_name)
            except:
                pass
        
        self.results.append(result)
        return result
    
    def test_successful_login(self) -> bool:
        """Test de login exitoso"""
        login_page = LoginPageTest(self.driver, self.config)
        
        # Navegar a login
        login_page.navigate_to_login()
        
        # Realizar login con credenciales válidas
        login_success = login_page.login("tomsmith", "SuperSecretPassword!")
        
        if not login_success:
            return False
        
        # Verificar que estamos en área segura
        return login_page.verify_secure_area()
    
    def test_failed_login(self) -> bool:
        """Test de login fallido"""
        login_page = LoginPageTest(self.driver, self.config)
        
        # Navegar a login
        login_page.navigate_to_login()
        
        # Intentar login con credenciales inválidas
        try:
            login_page.login("invalid_user", "invalid_password")
            # Si llegamos aquí sin error, el test debe fallar
            # porque las credenciales inválidas no deberían funcionar
            return False
        except:
            # Se espera que falle con credenciales inválidas
            print("✅ Login falló como se esperaba con credenciales inválidas")
            return True
    
    def test_page_navigation(self) -> bool:
        """Test de navegación entre páginas"""
        try:
            # Navegar a diferentes páginas
            test_urls = [
                f"{self.config.base_url}/",
                f"{self.config.base_url}/login",
                f"{self.config.base_url}/dynamic_content"
            ]
            
            for url in test_urls:
                self.driver.get(url)
                time.sleep(1)  # Pausa entre navegaciones
            
            print("✅ Navegación entre páginas exitosa")
            return True
        except Exception as e:
            print(f"❌ Error en navegación: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Ejecutar todos los tests"""
        print("🚀 SESIÓN 8: PRUEBAS CON SELENIUM")
        print("=" * 50)
        
        if self.config.simulate_mode:
            print("🎭 Ejecutando en MODO SIMULADO")
        else:
            print("🌐 Ejecutando con Selenium REAL")
        
        print(f"📍 URL base: {self.config.base_url}")
        print(f"⏱️ Timeout: {self.config.timeout}s")
        print(f"👁️ Headless: {self.config.headless}")
        
        try:
            # Ejecutar tests
            self.run_test("Login Exitoso", self.test_successful_login)
            self.run_test("Login Fallido", self.test_failed_login)
            self.run_test("Navegación de Páginas", self.test_page_navigation)
            
        finally:
            # Cleanup
            self.driver.quit()
        
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
            'results': self.results,
            'simulated': self.config.simulate_mode
        }
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DE RESULTADOS:")
        print(f"   Total: {summary['total']}")
        print(f"   Passed: {summary['passed']}")
        print(f"   Failed: {summary['failed']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Duration: {summary['total_duration']:.2f}s")
        print(f"   Mode: {'Simulado' if summary['simulated'] else 'Real'}")
        
        if failed > 0:
            print(f"\n❌ {failed} tests fallaron:")
            for result in self.results:
                if result['status'] == 'FAILED':
                    print(f"   • {result['name']}: {result['error']}")
        else:
            print(f"\n✅ Todos los tests pasaron exitosamente!")
        
        return summary


def main():
    """Función principal"""
    print("🎯 SELENIUM TESTING DEMO")
    print("=" * 30)
    
    # Configuración
    config = TestConfig(
        headless=True,  # Para evitar abrir ventanas
        simulate_mode=not SELENIUM_AVAILABLE
    )
    
    if not SELENIUM_AVAILABLE:
        print("\n💡 MODO EDUCATIVO:")
        print("   Este demo muestra los conceptos de Selenium")
        print("   Para ejecutar tests reales, instala:")
        print("   pip install selenium webdriver-manager")
    
    # Ejecutar tests
    suite = SeleniumTestSuite(config)
    results = suite.run_all_tests()
    
    print(f"\n🎓 CONCEPTOS DEMOSTRADOS:")
    print("   • Page Object Model para organización")
    print("   • Manejo de errores y excepciones")
    print("   • Screenshots automáticos en fallos")
    print("   • Configuración headless para CI/CD")
    print("   • Testing de flujos de usuario E2E")
    print("   • Waits y sincronización")
    print("   • Cross-browser compatibility")
    
    # Exit code basado en resultados
    exit_code = 0 if results['failed'] == 0 else 1
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
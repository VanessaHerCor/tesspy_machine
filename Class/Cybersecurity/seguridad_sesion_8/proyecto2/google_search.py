from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
import time

# Configurar el servicio de geckodriver
service = Service('./geckodriver')

# Inicializar el navegador Firefox
driver = webdriver.Firefox(service=service)

try:
    # Abrir Google
    driver.get("https://www.google.com")

    # Esperar un momento para que cargue la página
    time.sleep(2)

    # Buscar el campo de búsqueda (puede ser por nombre o por otro selector)
    search_box = driver.find_element(By.NAME, "q")

    # Escribir texto en la barra de búsqueda
    search_box.send_keys("Selenium Python tutorial")

    # Hacer clic en el botón de búsqueda o presionar Enter
    search_box.send_keys(Keys.RETURN)

    # Esperar para ver los resultados
    time.sleep(10)

    print("Búsqueda completada exitosamente!")

finally:
    # Cerrar el navegador
    driver.quit()

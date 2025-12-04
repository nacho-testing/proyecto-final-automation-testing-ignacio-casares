import pytest
import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.login_page import LoginPage

USERNAME = 'standard_user'
PASSWORD = 'secret_sauce'

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--guest")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    yield driver

    time.sleep(1)
    driver.quit()

@pytest.fixture
def usuario_logueado(driver):
    """
    Fixture que realiza login
    """
    print("Iniciando fixture usuario_logueado")
    login_page = LoginPage(driver)
    print("Abriendo la página de login")
    login_page.abrir()
    print("Realizando login con usuario estándar")
    pagina = login_page.login(USERNAME, PASSWORD)
    print("Login exitoso, devolviendo sesión de usuario")
    return pagina

def captura_de_pantalla(driver, caso):
    # Guarda una captura de pantalla con tiempo y nombre de test.
    os.makedirs("reports", exist_ok=True)
    tiempo = datetime.now().strftime("%d-%m-%Y %S-%M-%H")
    archivo = f"reports/{caso}_{tiempo}.png"
    driver.save_screenshot(archivo)
    print(f"Screenshot guardado en: {archivo}")
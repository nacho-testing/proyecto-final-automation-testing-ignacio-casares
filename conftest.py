import pytest
import time
import os
import pathlib
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.login_page import LoginPage

_USERNAME = 'standard_user'
_PASSWORD = 'secret_sauce'

target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True)

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
    pagina = login_page.login(_USERNAME, _PASSWORD)
    print("Login exitoso, devolviendo sesión de usuario")
    return pagina

def _crear_logger():
    path_dir = pathlib.Path("logs")
    path_dir.mkdir(exist_ok=True)

    log_file = path_dir / "suite.log"

    logger = logging.getLogger("talentolab")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = _crear_logger()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            tiempo = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            file_name = target / f"TEST {item.name}_{tiempo}.png"
            
            try:
                driver.save_screenshot(str(file_name))
                
                if hasattr(rep, 'extra'):
                    rep.extra = getattr(rep, 'extra', [])
                    rep.extra.append({
                        'name': 'screenshot',
                        'format': 'image', 
                        'content': str(file_name)
                    })

            except Exception as e:
                print(f"Error al capturar pantalla: {e}")

def pytest_html_report_title(report):
    report.title = "TalentoLab - Resumen de ejecución"

def pytest_html_results_summary(prefix, summary, postfix):
    summary.extend(["<p>Suite UI + API completa</p>"])

def pytest_html_results_table_header(cells):
    cells.insert(4, 'URL')

def pytest_html_results_table_row(report, cells):
    cells.insert(4, getattr(report, 'page_url', '-'))
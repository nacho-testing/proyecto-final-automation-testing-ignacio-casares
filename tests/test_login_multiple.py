import os
import sys
import pytest
from pages.login_page import LoginPage
from conftest import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.datos import leer_json

_CASOS_LOGIN = leer_json('datos/login.json')

@pytest.mark.regresion
@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe_funcionar", _CASOS_LOGIN)
def test_login(driver, request, usuario, clave, debe_funcionar):
    """
    Verifica distintos casos de login según usuario, clave y resultado esperado.
    """

    request.node.page_url = driver.current_url

    logger.info("Iniciando test de login con usuario: '%s'", usuario)
    login_page = LoginPage(driver)

    logger.info("Abriendo la página de login")
    login_page.abrir()
        
    logger.info("Intentando login con usuario='%s' y clave='%s'", usuario, clave)
    resultado = login_page.login(usuario, clave)

    if debe_funcionar == "True":
        logger.info("Se espera que el login funcione")
        assert resultado is not None, "El login debía funcionar pero falló."
        logger.info("Login exitoso")

        assert "inventory.html" in driver.current_url, f"URL inesperada: {driver.current_url}"
        logger.info("Redirigido correctamente a la página de inventario")

    else:
        logger.info("Se espera que el login falle")
        assert resultado is None, "El login no debía funcionar, pero sí funcionó."
        
        assert login_page.hay_error(), "Se esperaba un mensaje de error y no apareció."
        logger.info("Mensaje de error mostrado correctamente")

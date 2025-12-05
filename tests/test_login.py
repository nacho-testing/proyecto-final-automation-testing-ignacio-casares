import pytest
from conftest import logger

@pytest.mark.smoke
@pytest.mark.ui
def test_login(driver, request, usuario_logueado):
    """
    Verifica que un usuario logueado acceda correctamente a la página de inventario.
    Comprueba el título del logo y el título de la sección de productos.
    """

    request.node.page_url = driver.current_url
     
    logger.info("Iniciando verificación de login y página de inventario")
    inventory_page = usuario_logueado

    logger.info("Verificando el título del logo de la página")
    titulo = inventory_page.titulo()
    assert titulo, "No se encontró el titulo"
    logger.info("Título encontrado: '%s'", titulo.text)
    assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

    logger.info("Verificando título de la sección de productos")
    seccion = inventory_page.titulo_de_seccion()
    assert seccion, "No se encontró el elemento de título de sección"
        
    logger.info("Título de sección encontrado: '%s'", seccion.text)
    assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

    logger.info("Login completado correctamente y se ingresó a la página de inventario.")
    
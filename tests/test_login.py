from conftest import captura_de_pantalla
import pytest


@pytest.mark.smoke
def test_login(driver, usuario_logueado):
    """
    Verifica que un usuario logueado acceda correctamente a la página de inventario.
    Comprueba el título del logo y el título de la sección de productos.
    """
        
    try:
        print("Iniciando verificación de login y página de inventario")
        inventory_page = usuario_logueado

        print("Verificando el título del logo de la página")
        titulo = inventory_page.titulo()
        assert titulo, "No se encontró el titulo"
        print("Título encontrado: '%s'", titulo.text)
        assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

        print("Verificando título de la sección de productos")
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        
        print("Título de sección encontrado: '%s'", seccion.text)
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        print("Login completado correctamente y se ingresó a la página de inventario.")
    
    except Exception as e:
        captura_de_pantalla(driver, 'test_login')
        raise e
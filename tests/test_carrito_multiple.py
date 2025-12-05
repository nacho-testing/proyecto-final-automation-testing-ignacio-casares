import os
import sys
import pytest
from conftest import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.datos import leer_csv

_PRODUCTOS = leer_csv('datos/productos.csv')

@pytest.mark.regresion
@pytest.mark.ui
@pytest.mark.parametrize("producto", _PRODUCTOS)
def test_carrito(driver, request, usuario_logueado, producto):
    """
    Verifica que un producto específico se pueda agregar correctamente al carrito.
    Comprueba el precio del producto y la actualización del contador del carrito.
    """

    request.node.page_url = driver.current_url

    nombre, precio, descripcion = producto

    inventory_page = usuario_logueado
    logger.info("Iniciando test del carrito para el producto: %s", nombre)

    logger.info("Obteniendo título de la sección del inventario")
    seccion = inventory_page.titulo_de_seccion()
    assert seccion, "No se encontró el elemento de título de sección"

    logger.info("Título de sección encontrado: '%s'", seccion.text)
    assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

    cantidad_productos = inventory_page.obtener_cantidad_productos()
    logger.info("Cantidad de productos encontrados en el catálogo: %d", cantidad_productos)
    assert cantidad_productos > 0, "No se encontraron productos en el catálogo"

    precio_del_producto = inventory_page.obtener_precio_del_producto(nombre)
    logger.info("Precio obtenido para '%s': %s", nombre, precio_del_producto)

    assert precio_del_producto, "Producto sin precio"
    assert precio_del_producto == float(precio), (
        f"El precio mostrado ({precio_del_producto}) no coincide con el esperado ({precio}) para el producto {nombre}"
    )

    logger.info("Agregando producto al carrito: %s", nombre)
    inventory_page.agregar_producto_por_nombre(nombre)

    logger.info("Verificando que el contador del carrito se actualizó")
    contador_carrito = inventory_page.carrito_contador()
    logger.info("Valor del contador del carrito: %d", contador_carrito)
    assert contador_carrito > 0, "No se encontró el contador del carrito después de agregar el producto"

    logger.info("Navegando a la página del carrito")
    cart_page = inventory_page.ir_al_carrito()

    logger.info("Verificando la lista de productos en el carrito")
    lista_productos = cart_page.lista_de_los_productos()
    assert lista_productos, "No se encontró la lista de productos en el carrito"

    productos_del_carrito = cart_page.productos_del_carrito()
    logger.info("Cantidad de productos en el carrito: %d", len(productos_del_carrito))
    assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"

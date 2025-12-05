import pytest


@pytest.mark.smoke
@pytest.mark.ui
def test_catalogo(driver, request, usuario_logueado):
    """
    Verifica que el catálogo cargue correctamente para un usuario logueado.
    Comprueba menú lateral, opciones de ordenamiento y productos visibles.
    Asegura que el carrito esté vacío y que todos los ítems del catálogo sean válidos.
    """

    request.node.page_url = driver.current_url

    inventory_page = usuario_logueado

    print("Obteniendo título de la sección del inventario")
    seccion = inventory_page.titulo_de_seccion()
    assert seccion, "No se encontró el elemento de título de sección"

    print("Título de sección encontrado: '%s'", seccion.text)
    assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

    print("Verificando existencia del botón de menú lateral")
    assert inventory_page.menu_boton(), "No se encontró el botón del menú"
    print("Botón de menú encontrado.")

    print("Haciendo clic en el botón de menú lateral")
    inventory_page.abrir_menu()
    print("El menú lateral está abierto.")

    menu_items_esperados = ["All Items", "About", "Logout", "Reset App State"]
    menu_items = inventory_page.menu_items()

    print("Verificando cantidad de ítems en el menú: esperados %d, encontrados %d", len(menu_items_esperados), len(menu_items))
    assert len(menu_items) == len(menu_items_esperados), (
        f"Cantidad de ítems inesperada: se esperaban {len(menu_items_esperados)}, "
        f"pero se encontraron {len(menu_items)}."
    )

    for index, esperado in enumerate(menu_items_esperados):
        obtenido = menu_items[index]
        print("Verificando menú ítem: esperado '%s', obtenido '%s'", esperado, obtenido.text)
        assert esperado == obtenido.text, f"Texto inesperado: se esperaba '{esperado}' pero se obtuvo '{obtenido.text}'"

    print("Todos los ítems del menú fueron verificados correctamente.")

    print("Verificando que la opción del ordenamiento activo sea 'Name (A to Z)'")
    active_option = inventory_page.filtro_activo()
    assert active_option, "No se encontró el elemento con el ordenamiento activo."

    print("Opción activa encontrada: '%s'", active_option.text)
    assert active_option.text == "Name (A to Z)", f"El ordenamiento activo no es el esperado: se esperaba 'Name (A to Z)', pero se encontró '{active_option.text}'."

    print("Verificando existencia del select de ordenamiento")
    select = inventory_page.select_de_ordenamiento()
    assert select, "No se encontró el select de ordenamiento"

    opciones = inventory_page.opciones_de_ordenamiento()
    print("Cantidad de opciones en el select: %d", len(opciones))
    assert len(opciones) > 0, "El select no contiene opciones"

    opciones_esperadas = [
        "Name (A to Z)",
        "Name (Z to A)",
        "Price (low to high)",
        "Price (high to low)"
    ]
    print("Verificando orden y texto de cada opción del select")
    for index, texto_esperado in enumerate(opciones_esperadas):
        option_text = opciones[index].text
        print("Opción %d: esperado '%s', obtenido '%s'", index, texto_esperado, option_text)
        assert option_text == texto_esperado, f"Texto inesperado en opción {index}: se esperaba {texto_esperado} pero se obtuvo {option_text}"

    print("Verificando existencia del carrito de compras")
    assert inventory_page.carrito(), "No se encontró el elemento con id shopping_cart_container"

    print("Verificando que el carrito esté vacío")
    contador = inventory_page.carrito_contador()
    print("Valor del contador del carrito: %d", contador)
    assert contador == 0, f"El carrito no está vacío: se encontró un contador de cantidad: {contador}"

    cantidad_productos = inventory_page.obtener_cantidad_productos()
    print("Cantidad de productos en el catálogo: %d", cantidad_productos)
    assert cantidad_productos > 0, "No se encontraron productos en el catálogo"

    productos = inventory_page.obtener_productos()
    print("Verificando que cada producto tenga nombre y precio visibles")
    for index, producto in enumerate(productos):
        nombre_del_producto = inventory_page.nombre_del_producto(producto)
        precio_del_producto = inventory_page.obtener_precio_del_producto(nombre_del_producto)

        print("Producto %d: Nombre='%s', Precio='%s'", index, nombre_del_producto, precio_del_producto)
        assert nombre_del_producto, f"Producto {index} sin nombre"
        assert precio_del_producto, f"Producto {index} sin precio"

    primer_producto = productos[0]
    nombre_del_producto = inventory_page.nombre_del_producto(primer_producto)
    precio_del_producto = inventory_page.obtener_precio_del_producto(nombre_del_producto)
    print("Primer producto: Nombre='%s', Precio='%s'", nombre_del_producto, precio_del_producto)

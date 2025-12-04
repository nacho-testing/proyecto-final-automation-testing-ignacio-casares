from conftest import captura_de_pantalla


def test_carrito(driver, usuario_logueado):
    """
    Verifica que un usuario logueado pueda agregar un producto al carrito.
    Comprueba nombre, precio y la presencia del contador del carrito.
    Asegura que el producto añadido coincida con el mostrado en el carrito.
    """

    try:
        inventory_page = usuario_logueado

        print("Verificando el título de la sección")
        seccion = inventory_page.titulo_de_seccion()
        assert seccion, "No se encontró el elemento de título de sección"
        print("Título de sección encontrado: '%s'", seccion.text)
        assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

        cantidad_productos = inventory_page.obtener_cantidad_productos()
        print("Cantidad de productos en el catálogo: %d", cantidad_productos)
        assert cantidad_productos > 0, "No se encontraron productos en el catálogo"

        productos = inventory_page.obtener_productos()
        primer_producto = productos[0]
        print("Primer producto obtenido para pruebas")

        print("Verificando que el primer producto tenga nombre y precio")
        nombre_del_producto = inventory_page.nombre_del_producto(primer_producto)
        assert nombre_del_producto, "Producto sin nombre"
        print("Nombre del primer producto: %s", nombre_del_producto)

        precio_del_producto = inventory_page.obtener_precio_del_producto(nombre_del_producto)
        assert precio_del_producto, "Producto sin precio"
        print("Precio del primer producto: %s", precio_del_producto)

        print("Primer producto: Nombre='%s', Precio='%s'", nombre_del_producto, precio_del_producto)

        print("Verificando que exista el botón 'Add to cart' en el primer producto")
        assert inventory_page.boton_agregar(primer_producto), "No se encontró el botón 'Add to cart' en el primer producto"

        print("Agregando primer producto al carrito")
        inventory_page.agregar_producto(primer_producto)

        contador_carrito = inventory_page.carrito_contador()
        print("Valor del contador del carrito después de agregar el producto: %d", contador_carrito)
        assert contador_carrito > 0, "No se encontró el contador del carrito después de agregar el producto"

        print("Navegando a la página del carrito")
        cart_page = inventory_page.ir_al_carrito()

        print("Verificando que exista la lista de productos en el carrito")
        lista_productos_carrito = cart_page.lista_de_los_productos()
        assert lista_productos_carrito, "No se encontró la lista de productos en el carrito"

        productos_del_carrito = cart_page.productos_del_carrito()
        print("Cantidad de productos en el carrito: %d", len(productos_del_carrito))
        assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"

        print("Verificando que el producto añadido sea el correcto")
        primer_producto_del_carrito = productos_del_carrito[0]

        nombre_en_carrito = cart_page.nombre_del_producto_agregado(primer_producto_del_carrito)
        print("Nombre del producto en el carrito: %s", nombre_en_carrito.text if nombre_en_carrito else None)
        assert nombre_en_carrito, "No se encontró el nombre del producto en el carrito"
        assert nombre_en_carrito.text == nombre_del_producto, (
            f"Nombre inesperado en el carrito: se esperaba {nombre_del_producto} pero se obtuvo {nombre_en_carrito.text}"
        )

        precio_en_carrito = cart_page.precio_del_producto_agregado(primer_producto_del_carrito)
        print("Precio del producto en el carrito: %s", precio_en_carrito)
        assert precio_en_carrito, "No se encontró el precio del producto en el carrito"
        assert precio_en_carrito == precio_del_producto, (
            f"Precio inesperado en el carrito: se esperaba {precio_del_producto} pero se obtuvo {precio_en_carrito}"
        )

        print("Verificación completa: el producto en el carrito coincide con el producto añadido")
    except Exception as e:
        captura_de_pantalla(driver, 'test_carrito')
        raise e
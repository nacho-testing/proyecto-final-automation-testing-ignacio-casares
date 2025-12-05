import requests
import pytest

_URL_BASE = "https://jsonplaceholder.typicode.com"

@pytest.mark.api
def test_obtener_post_exitoso():
    """GET - Verifica que se puede obtener un post existente correctamente."""

    respuesta = requests.get(f"{_URL_BASE}/posts/1")

    verificar_status(respuesta, [200])

    datos = respuesta.json()
    assert "userId" in datos, f"Falta 'userId'. Respuesta: {datos}"
    assert "id" in datos, f"Falta 'id'. Respuesta: {datos}"
    assert "title" in datos, f"Falta 'title'. Respuesta: {datos}"
    assert "body" in datos, f"Falta 'body'. Respuesta: {datos}"
    assert datos["id"] == 1, f"ID incorrecto. Respuesta: {datos}"


@pytest.mark.api
def test_crear_post_exitoso():
    """POST - Verifica que se puede crear un post nuevo correctamente."""

    cuerpo = {"title": "Mi nuevo post", "body": "Contenido del post", "userId": 1}
    respuesta = requests.post(f"{_URL_BASE}/posts", json=cuerpo)

    verificar_status(respuesta, [201])

    datos = respuesta.json()
    assert datos["title"] == cuerpo["title"], f"Título incorrecto. Respuesta: {datos}"
    assert datos["body"] == cuerpo["body"], f"Body incorrecto. Respuesta: {datos}"
    assert datos["userId"] == cuerpo["userId"], f"UserId incorrecto. Respuesta: {datos}"
    assert "id" in datos, "No se recibió ID en la respuesta"


@pytest.mark.api
def test_eliminar_post_exitoso():
    """DELETE - Verifica que se puede eliminar un post correctamente."""

    respuesta = requests.delete(f"{_URL_BASE}/posts/1")

    verificar_status(respuesta, [200, 204])

    assert respuesta.text in ["{}", ""], f"Se esperaba cuerpo vacío. Recibido: {respuesta.text}"


@pytest.mark.api
def test_post_no_encontrado():
    """GET - Verifica el comportamiento al solicitar un post que no existe."""

    respuesta = requests.get(f"{_URL_BASE}/posts/999999")

    verificar_status(respuesta, [404])

    assert respuesta.text in ["{}", ""], f"Se esperaba cuerpo vacío. Recibido:\n{respuesta.text}"


def verificar_status(respuesta, codigos_esperados):
    assert respuesta.status_code in codigos_esperados, f"Código inesperado: {respuesta.status_code}. Respuesta: {respuesta.text}"

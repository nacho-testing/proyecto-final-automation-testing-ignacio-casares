
# Automation Testing - Proyecto de Automatización de Pruebas

**Autor**: Ignacio Casares

## Propósito del proyecto

Este proyecto automatiza pruebas funcionales para **SauceDemo** y la API **jsonplaceholder**, garantizando el correcto funcionamiento de sus funciones críticas.\
Incluye pruebas de interfaz web con Selenium y de API, con scripts reproducibles para validar comportamientos clave del sistema.

## Tecnologías utilizadas

-   **Python 3**
-   **pytest**
-   **pytest-html**
-   **Selenium WebDriver**
-   **Requests**

## Estructura del proyecto

    README.md              # Documentación general del proyecto
    requirements.txt       # Dependencias de Python necesarias
    conftest.py            # Configuración de Pytest
    pytest.ini             # Archivo de configuración adicional de Pytest
    tests/                 # Tests de UI
    tests_api/             # Tests de API
    pages/                 # Page Objects para pruebas de UI
    datos/                 # Datos de prueba (CSV o JSON)
    utils/                 # Funciones auxiliares y helpers
    reports/               # Reportes de ejecución, capturas de pantalla y HTML
    logs/                  # Logs generados durante la ejecución

## Instalación de dependencias

    pip install -r requirements.txt

## Ejecución de las pruebas

### a. Completo

    pytest -v

### b. Por carpetas - UI, API

    pytest -v tests/
    pytest -v tests_api/

### c. Con markers
Los markers se definen en `pytest.ini`.

    pytest -m MARKER

### d. Reporte HTML

    pytest --html=reports/reporte.html --self-contained-html -v -s

## Interpretación de los reportes

Los reportes se guardan en `reports/` e incluyen:
 - Información del entorno de ejecución.
 - Estado y duración de cada prueba.
 - Capturas de pantalla de los tests fallidos (`screens/`).

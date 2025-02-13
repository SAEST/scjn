import pandas as pd
import numpy as np
import re
import pytest
import allure
from utils.data_reader import data_reader
from utils.conteos_csv import cargar_y_filtrar_datos, calcular_data_values

@pytest.fixture
def df():
    return cargar_y_filtrar_datos()

@pytest.fixture
def data_values(df):
    return calcular_data_values(*df)

@pytest.mark.parametrize("allure_story, valor, valor2, encabezado", data_reader.leer_datos_csv2())
@allure.feature('Cálculo y Validación de datos CSV Ministro(a) SCJN')
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_calculo_validacion_datos(data_values, allure_story, valor, valor2, encabezado):
    """
    Prueba que realiza los conteos con la informacion del csv, para validar los encabezados coincidan con lo esperado.
    """
    # Aplicar la etiqueta @allure.story dinámicamente
    allure.dynamic.story(allure_story)  # Etiqueta dinámica basada en el CSV

    # Establecer un título dinámico para la prueba
    allure.dynamic.title(allure_story)

    valor = data_values[valor]
    valor2 = data_values[valor2]

    with allure.step(f"Comparando los valores de {encabezado} con los esperados"):
        if np.array_equal(valor, valor2):
            allure.attach(
                f"Los valores de {encabezado} coinciden. Conteo CSV: {valor} Encabezado CSV: {valor2}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
            #print(f'Los valores de {encabezado} coinciden. Conteo CSV: {valor} Encabezado CSV: {valor2}')
        else:
            allure.attach(
                f"Los valores de {encabezado} no coinciden. Conteo CSV: {valor} Encabezado CSV: {valor2}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
            #print(f'Los valores de {encabezado} no coinciden. Conteo CSV: {valor} Encabezado CSV: {valor2}')
        try:
            assert np.array_equal(valor, valor2)
        except AssertionError:
            pytest.fail(f"Los valores de {encabezado} no coinciden. Conteo CSV: {valor} Encabezado CSV: {valor2}")
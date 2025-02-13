import pandas as pd
import os

class data_reader():
    # Función para leer datos desde el CSV y eliminar el BOM si está presente
    @staticmethod
    def leer_datos_csv():
        filepath = './data/elementos.csv'
        df = pd.read_csv(filepath, encoding='utf-8-sig')

        for index, row in df.iterrows():
            yield row['allure_story'], row['valor'], row['tipo_dato'], row['selector'], row['ruta']

    def leer_datos_csv2():
        filepath = './data/conteoscsv.csv'
        df = pd.read_csv(filepath, encoding='utf-8-sig')

        for index, row in df.iterrows():
            yield row['allure_story'], row['valor'], row['valor2'], row['encabezado']

    @staticmethod
    def df():
        # Leer el archivo CSV en un DataFrame
        csv_path = './data/bd/csv/MIN_2025.csv'
        df = pd.read_csv(csv_path, skiprows=3, nrows=1, sep='|', header=None, names=[
            "ACTAS_ESPERADAS", "ACTAS_COMPUTADAS", "PORCENTAJE_ACTAS_COMPUTADAS", "LISTA_NOMINAL_ACTAS_COMPUTADAS", 
            "TOTAL_VOTOS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
        ])

        # Retornar solo las columnas necesarias en un nuevo DataFrame
        selected_columns = df[[
            "ACTAS_ESPERADAS", "ACTAS_COMPUTADAS", "PORCENTAJE_ACTAS_COMPUTADAS", "LISTA_NOMINAL_ACTAS_COMPUTADAS", "TOTAL_VOTOS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
        ]]

        return selected_columns
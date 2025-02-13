import pandas as pd

# Constantes de columnas
ACTAS_ESPERADAS = 'ACTAS_ESPERADAS'
ACTAS_COMPUTADAS = 'ACTAS_COMPUTADAS'
PORCENTAJE_ACTAS_COMPUTADAS = 'PORCENTAJE_ACTAS_COMPUTADAS'
LISTA_NOMINAL_ACTAS_COMPUTADAS = 'LISTA_NOMINAL_ACTAS_COMPUTADAS'
TOTAL_VOTOS = 'TOTAL_VOTOS'
PORCENTAJE_PARTICIPACION_CIUDADANA = 'PORCENTAJE_PARTICIPACION_CIUDADANA'

def cargar_y_filtrar_datos():
    file_path = './data/bd/csv/MIN_2025.csv'
    df = pd.read_csv(file_path, skiprows=5, sep='|', encoding='latin-1', low_memory=False)
    df1 = pd.read_csv(file_path, skiprows=4, sep='|', encoding='latin-1', nrows=1, header=None,
                      names=[ACTAS_ESPERADAS, ACTAS_COMPUTADAS, PORCENTAJE_ACTAS_COMPUTADAS, 
                             LISTA_NOMINAL_ACTAS_COMPUTADAS, TOTAL_VOTOS, PORCENTAJE_PARTICIPACION_CIUDADANA])
    return df, df1

def calcular_data_values(df, df1):

# Conversión y limpieza de datos (aplicar a todas las columnas necesarias)
    for col in [ACTAS_COMPUTADAS, ACTAS_ESPERADAS, LISTA_NOMINAL_ACTAS_COMPUTADAS, TOTAL_VOTOS]:
        if col in df1.columns: # Check if column exists to avoid errors
            df1[col] = pd.to_numeric(df1[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0) # Convert, replace commas, handle NaN

# Extracción de datos
    if not df1.empty:
        try:
            valores = df1.iloc[0][[ACTAS_COMPUTADAS, ACTAS_ESPERADAS, PORCENTAJE_ACTAS_COMPUTADAS, LISTA_NOMINAL_ACTAS_COMPUTADAS, TOTAL_VOTOS, PORCENTAJE_PARTICIPACION_CIUDADANA]]
            actas_esperadas = int(valores[ACTAS_ESPERADAS] or 0)
            actas_computadas = int(valores[ACTAS_COMPUTADAS] or 0) 
            porcentaje_actas_computadas = float(valores[PORCENTAJE_ACTAS_COMPUTADAS] or 0.0)
            ln_actas_computadas = int(valores[LISTA_NOMINAL_ACTAS_COMPUTADAS] or 0)
            total_votos = int(valores[TOTAL_VOTOS] or 0)
            participacionciu = float(valores[PORCENTAJE_PARTICIPACION_CIUDADANA] or 0.0)

        except (ValueError, TypeError, KeyError) as e: 
            print(f"Error al procesar datos: {e}")
    else:
        print("El DataFrame está vacío.")

    # Calculos
    calculo_actas_esperadas = len(df)
    calculo_actas_computadas = len(df)
    calculo_porcentaje_actas_computadas = (df1[ACTAS_COMPUTADAS].iloc[0] * 100) / df1[ACTAS_ESPERADAS].iloc[0]
    calculo_ln_actas_computadas = df['LISTA_NOMINAL_CASILLA'].astype(int).sum()
    calculo_total_votos = df['TOTAL_VOTOS_CALCULADOS'].astype(int).sum()
    calculo_participacionciu = ((calculo_total_votos * 100) / calculo_ln_actas_computadas, 4)
    calculo_participacionciu = pd.Series(calculo_participacionciu)
    calculo_participacionciu = calculo_participacionciu.apply(lambda x: int(x * 10000) / 10000)
    calculo_participacionciu = calculo_participacionciu.iloc[0]

    return {
        "calculo_actas_esperadas": calculo_actas_esperadas,
        "calculo_actas_computadas": calculo_actas_computadas,
        "calculo_porcentaje_actas_computadas": calculo_porcentaje_actas_computadas,
        "calculo_ln_actas_computadas": calculo_ln_actas_computadas,
        "calculo_total_votos": calculo_total_votos,
        "calculo_participacionciu": calculo_participacionciu,
        "actas_computadas": actas_computadas,
        "actas_esperadas": actas_esperadas,
        "porcentaje_actas_computadas": porcentaje_actas_computadas,
        "ln_actas_computadas": ln_actas_computadas,
        "total_votos": total_votos,
        "participacionciu": participacionciu
    }

import requests
import zipfile
import os
import pytest
import allure
from shutil import rmtree

url = 'https://computos2025.ine.mx/YYYYMMDD_HHMM_COMPUTOS.zip'
nombre_archivo = url.split('/')[-1]
csv = ["MIN_2025.csv", "MIN_CANDIDATURAS_2025.csv"]

directorio_destino = './data/bd'  # Carpeta en donde se descarga el zip principal
directorio_unzip = './data/bd/unzip' # Carpeta en donde se extraen los archivos del zip principal
directorio_csv = './data/bd/csv'  # Carpeta donde se van a extraer los archivos para presidente
ruta_completa = os.path.join(directorio_destino, nombre_archivo)

# Crear la carpeta de destino si no existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Realizar la petición GET al servidor
respuesta = requests.get(url)

# Verificar si la descarga fue exitosa (código 200)
if respuesta.status_code == 200:
    # Guardar el contenido descargado en un archivo local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)
    print(f'Descarga exitosa: {ruta_completa}')
else:
    print(f'Error al descargar: {respuesta.status_code}')

lista_archivos = os.listdir(directorio_destino)
for archivo in lista_archivos:
    if archivo.endswith(".zip"):
        nombre_archivo = os.path.basename(archivo)
        print(f"Nombre del archivo: {nombre_archivo}")

archivo_zip1 = os.path.join(directorio_destino, nombre_archivo) # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
    zip_ref.extractall(directorio_unzip)

print(f'Archivo ZIP "{archivo_zip1}" descomprimido exitosamente en "{directorio_unzip}"')

@pytest.fixture
def path_destino():
    return directorio_unzip #Jenkins

@pytest.mark.parametrize("archivos_esperados", [(csv),])
@allure.feature('Descarga de CSV Ministro(a) de SCJN')  
@allure.story('Descompresion de CSV')  
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_descomprimir_archivo(archivos_esperados):
    """
    Prueba la descompresión de un archivo ZIP y la existencia de archivos CSV.

    Args:
        archivos_esperados: Lista de nombres de archivos CSV esperados tras la descompresión.
        directorio_destino: Directorio donde se descomprimirá el archivo.
    """
    with allure.step("Descomprimiendo archivo ZIP"):
        for archivo in os.listdir(directorio_unzip):
            if "_SCJN.zip" in archivo:
                archivo_zip_path = os.path.join(directorio_unzip, archivo)
                break
        with zipfile.ZipFile(archivo_zip_path, 'r') as zip_ref:
            zip_ref.extractall(directorio_csv)  # Descomprimir directamente en la raíz
            print(f'Archivo ZIP "{archivo_zip_path}" descomprimido exitosamente en "{directorio_csv}"')

    # Verificar y adjuntar los archivos descomprimidos
    for archivo in archivos_esperados:
        ruta_completa = os.path.join(directorio_csv, archivo)
        if os.path.exists(ruta_completa):
            allure.attach.file(ruta_completa, name=f"Archivo CSV: {archivo}", attachment_type=allure.attachment_type.CSV)
            print(f'Archivo CSV: "{archivo}" guardado exitosamente en "{directorio_csv}"')
        else:
            pytest.fail(f"El archivo CSV {archivo} no se encontró en el directorio de destino.")
            print(f'Archivo ZIP "{archivo_zip_path}" no se encontró en el directorio "{ruta_completa}"')
    
    clean_path()
    
    # Adjuntar la información de éxito general
    allure.attach(f"El archivo ZIP {archivo_zip_path} se descomprimió exitosamente en {directorio_unzip}", 
                  name="Resultado de descompresión", attachment_type=allure.attachment_type.TEXT)

def clean_path():
    with allure.step("Limpiando archivos no usados"):
        #borrar zip que no se usan
        rmtree(directorio_unzip)

        #borrar archivo zip principal
        os.remove(ruta_completa)

        allure.attach(f"Los directorios {directorio_unzip} y archivos {nombre_archivo} creados se liberaron exitosamente ", 
                  name="Limpiando proyecto", attachment_type=allure.attachment_type.TEXT)
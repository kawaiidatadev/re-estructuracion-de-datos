import os
import pandas as pd
from utils import process_excel_file


def process_all_excels(directory_path, excel_files):
    """
    Procesa múltiples archivos Excel y retorna un dataframe combinado.

    Args:
    directory_path (str): Ruta al directorio que contiene los archivos Excel.
    excel_files (list): Lista de nombres de archivos Excel a procesar.

    Returns:
    pd.DataFrame: Dataframe combinado resultante.
    """
    # Inicializar una lista vacía para almacenar los dataframes
    dataframes = []


    # Procesar cada archivo Excel
    for file in excel_files:
        file_path = os.path.join(directory_path, file)
        df = process_excel_file(file_path)
        dataframes.append(df)


    # Concatenar todos los dataframes en uno solo
    result_df = pd.concat(dataframes, ignore_index=True)
    print("process_data.py ejecutado")
    return result_df
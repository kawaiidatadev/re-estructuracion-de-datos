import pandas as pd
import numpy as np

# Función para quitar acentos de los nombres de las columnas
def remove_accents(column_name):
    accents = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
    }
    for accented_char, unaccented_char in accents.items():
        column_name = column_name.replace(accented_char, unaccented_char)
    return column_name


# Función para procesar un archivo Excel
def process_excel_file(file_path):
    df = pd.read_excel(file_path)

    # Quitar filas vacías
    df.dropna(how='all', inplace=True)

    # Eliminar columnas especificadas
    df.drop(columns=['Unidad', 'Proveedor', 'Equipo', 'Ultimo Costo', 'Costo', 'Costo Extendido'], inplace=True)

    # Renombrar columnas
    df.rename(columns={'Cantidad por': 'Cantidad'}, inplace=True)

    # Quitar acentos de los nombres de las columnas y convertir a minúsculas con guiones bajos
    df.columns = [remove_accents(col).lower().replace(' ', '_') for col in df.columns]

    print(df.columns)
    # Verificar y eliminar registros con valores nulos en las columnas 'nivel', 'producto' o 'descripcion'
    columns_to_check = ['nivel', 'producto', 'descripcion', 'cantidad']
    df = df.dropna(subset=columns_to_check)

    # Mostrar las filas eliminadas
    for column in columns_to_check:
        missing_rows = df[df[column].isnull()]
        if not missing_rows.empty:
            for index, row in missing_rows.iterrows():
                print(f"Fila eliminada por datos faltantes en la columna '{column}' - Fila {index + 1}")

    print('Registros con null en columnas determinadas')

    # Verificar y convertir la columna "nivel" a enteros
    if 'nivel' in df.columns:
        for index, value in df['nivel'].items():
            if not float(value).is_integer():
                print(f"Valor decimal encontrado en 'nivel' en la fila {index}: {value}")
        df['nivel'] = df['nivel'].astype(int)

    print("utils.py ejecutado")

    return df
"""
Este codigo, mediante el uso de funciones, y try, except.
Debe de recorrer una a una las filas de la columna "nivel", de el excel.
Si el dato, en la fila es un numero negativo, elimina toda la fila, y continua comprovando la sigguiente fila
hasta acabar con todos los registros.
Guarda el excel en la misma ruta, sobreescribiendo al anterior.
Teniendo cuidado usando tiempos de espera para evitar errores
"""


import pandas as pd
import time
import os

def eliminar_filas_negativas(path, columna):
    try:
        # Verificar si el archivo existe
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo en la ruta {path} no existe.")

        # Cargar el archivo Excel en un DataFrame
        df = pd.read_excel(path)

        # Verificar si la columna existe en el DataFrame
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no se encuentra en el archivo Excel.")

        # Eliminar filas donde la columna tenga valores negativos (no eliminar los nivel = 0)
        df = df[df[columna] >= 0]

        # Guardar el archivo actualizado (sobrescribe el original)
        df.to_excel(path, index=False)

        # Tiempo de espera para evitar errores en sistemas que puedan necesitarlo
        time.sleep(2)

        print("El archivo ha sido procesado y guardado correctamente.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

# Ruta del archivo y nombre de la columna
path = r'C:\Users\lmacias\Downloads\Reforma SAP\jet_format_todo.xlsx'
columna = 'nivel'

# Llamar a la función
eliminar_filas_negativas(path, columna)

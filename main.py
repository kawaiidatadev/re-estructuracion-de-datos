import process_data
from crear_db import save_to_sqlite
from seleccionar_padre_uno import *

# Ruta que contiene los archivos Excel
directory_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\data'
excel_files = ['bom1.xlsx', 'bom2.xlsx', 'bom3.xlsx']
db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

# Llamar a la función para procesar los archivos Excel
# df = process_data.process_all_excels(directory_path, excel_files)

# Segundo Paso: Guardar el DataFrame en una base de datos SQLite
# save_to_sqlite(df)


# Funcion para obtener el primer padre con sus hijos
df = segment_first_product(db_path)

# Funcion que guarda en memoria el producto, su tipo, y la cantidad.
# save_product_details(df)

import pandas as pd

def obtener_rango_trabajo(df):
    # Encontrar el primer índice donde 'nivel' es 0
    primer_nivel_cero = df[df['nivel'] == 0].index[0]

    # Encontrar el siguiente índice donde 'nivel' es 0 después del primer nivel cero
    siguiente_nivel_cero = df[df['nivel'] == 0].index[1] if len(df[df['nivel'] == 0]) > 1 else len(df)

    # Filtrar el rango de trabajo
    rango_trabajo = df.iloc[primer_nivel_cero:siguiente_nivel_cero]
    return rango_trabajo

def transformar_a_formato_sap(df):
    # Obtener el rango de trabajo
    rango_trabajo = obtener_rango_trabajo(df)

    # Crear el DataFrame df_sap con las columnas especificadas
    df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])

    # Obtener el producto padre
    producto_padre = rango_trabajo[rango_trabajo['nivel'] == 0]['producto'].values[0]

    # Filtrar los productos hijos
    productos_hijos = rango_trabajo[rango_trabajo['nivel'] == 1]

    # Llenar el DataFrame df_sap
    for _, row in productos_hijos.iterrows():
        df_sap = pd.concat([df_sap, pd.DataFrame({
            'producto_padre': [producto_padre],
            'producto_hijo': [row['producto']],
            'cantidad_hijo': [row['cantidad']]
        })], ignore_index=True)

    return df_sap


df_sap = transformar_a_formato_sap(df)
print(df_sap)

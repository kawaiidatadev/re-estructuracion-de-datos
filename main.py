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

def obtener_rango_trabajo(df, nivel_inicial=0, inicio=0):
    # Encontrar el primer índice donde 'nivel' es igual a nivel_inicial a partir del índice 'inicio'
    primer_nivel = df[df['nivel'] == nivel_inicial].index[df[df['nivel'] == nivel_inicial].index >= inicio][0]

    # Encontrar el siguiente índice donde 'nivel' es igual a nivel_inicial después del primer nivel
    siguiente_nivel = df[df['nivel'] == nivel_inicial].index[df[df['nivel'] == nivel_inicial].index > primer_nivel][0] if len(df[df['nivel'] == nivel_inicial].index[df[df['nivel'] == nivel_inicial].index > primer_nivel]) > 0 else len(df)

    # Filtrar el rango de trabajo
    rango_trabajo = df.iloc[primer_nivel:siguiente_nivel]
    return rango_trabajo

def transformar_a_formato_sap(df):
    # Obtener el rango de trabajo inicial
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

    # Procesar cada hijo de nivel 1 como nuevo padre
    for i in range(len(productos_hijos)):
        hijo = productos_hijos.iloc[i]
        nuevo_rango_trabajo = obtener_rango_trabajo(df, nivel_inicial=1, inicio=hijo.name)

        # Filtrar los productos hijos del nuevo rango de trabajo
        productos_nivel_2 = nuevo_rango_trabajo[nuevo_rango_trabajo['nivel'] == 2]

        # Llenar el DataFrame df_sap con el nuevo rango de trabajo
        for _, row in productos_nivel_2.iterrows():
            df_sap = pd.concat([df_sap, pd.DataFrame({
                'producto_padre': [hijo['producto']],
                'producto_hijo': [row['producto']],
                'cantidad_hijo': [row['cantidad']]
            })], ignore_index=True)

    return df_sap


df_sap = transformar_a_formato_sap(df)
print(df_sap)
df_sap.to_excel("export_df_sap.xlsx", index=False)

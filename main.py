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
    siguiente_nivel = df[df['nivel'] == nivel_inicial].index[df[df['nivel'] == nivel_inicial].index > primer_nivel][0] \
        if len(df[df['nivel'] == nivel_inicial].index[df[df['nivel'] == nivel_inicial].index > primer_nivel]) > 0 else\
        len(df)

    # Filtrar el rango de trabajo
    rango_trabajo = df.iloc[primer_nivel:siguiente_nivel]
    return rango_trabajo

def transformar_a_formato_sap(df, nivel_actual=0, productos_procesados=None):
    if productos_procesados is None:
        productos_procesados = set()  # Usamos un set para evitar duplicados de productos procesados

    # Obtener el rango de trabajo inicial
    rango_trabajo = obtener_rango_trabajo(df, nivel_inicial=nivel_actual)

    # Crear el DataFrame df_sap con las columnas especificadas
    df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])

    # Obtener el producto padre
    producto_padre = rango_trabajo[rango_trabajo['nivel'] == nivel_actual]['producto'].values[0]

    # Filtrar los productos hijos
    productos_hijos = rango_trabajo[rango_trabajo['nivel'] == nivel_actual + 1]

    # Llenar el DataFrame df_sap
    for _, row in productos_hijos.iterrows():
        if row['producto'] not in productos_procesados:
            df_sap = pd.concat([df_sap, pd.DataFrame({
                'producto_padre': [producto_padre],
                'producto_hijo': [row['producto']],
                'cantidad_hijo': [row['cantidad']]
            })], ignore_index=True)
            productos_procesados.add(row['producto'])

    # Procesar cada hijo de nivel actual + 1 como nuevo padre
    for i in range(len(productos_hijos)):
        hijo = productos_hijos.iloc[i]
        nuevo_rango_trabajo = obtener_rango_trabajo(df, nivel_inicial=nivel_actual + 1, inicio=hijo.name)

        # Filtrar los productos hijos del nuevo rango de trabajo
        productos_nivel_siguiente = nuevo_rango_trabajo[nuevo_rango_trabajo['nivel'] == nivel_actual + 2]

        # Llenar el DataFrame df_sap con el nuevo rango de trabajo
        for _, row in productos_nivel_siguiente.iterrows():
            if row['producto'] not in productos_procesados:
                df_sap = pd.concat([df_sap, pd.DataFrame({
                    'producto_padre': [hijo['producto']],
                    'producto_hijo': [row['producto']],
                    'cantidad_hijo': [row['cantidad']]
                })], ignore_index=True)
                productos_procesados.add(row['producto'])

    return df_sap, productos_procesados

def transformar_a_formato_sap_recurrente(df):
    # Crear el DataFrame df_sap_final con las columnas especificadas
    df_sap_final = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])

    # Mantener un conjunto de productos procesados
    productos_procesados = set()

    # Recursively process all necessary levels
    nivel_maximo = df['nivel'].max()

    for nivel in range(nivel_maximo + 1):
        df_sap, productos_procesados = transformar_a_formato_sap(df, nivel_actual=nivel,
                                                                 productos_procesados=productos_procesados)
        if not df_sap.empty:
            df_sap_final = pd.concat([df_sap_final, df_sap], ignore_index=True)

    return df_sap_final




# Supongamos que ya tienes un DataFrame df
df_sap_final = transformar_a_formato_sap_recurrente(df)
print(df_sap_final)
df_sap_final.to_excel("export_df_sap.xlsx", index=False)

def verificar_y_completar_hijos(df_sap_final, df):
    # Crear una copia del DataFrame df_sap_final para agregar los hijos faltantes
    df_sap_completo = df_sap_final.copy()

    # Recorrer cada producto padre en df_sap_final
    for producto_padre in df_sap_final['producto_padre'].unique():
        # Obtener los hijos esperados del producto padre según df
        hijos_esperados = df[(df['producto'] == producto_padre) & (df['nivel'] < df['nivel'].max() - 1)]
        hijos_esperados = df[df['nivel'] == df[df['producto'] == producto_padre]['nivel'].values[0] + 1]

        for _, hijo in hijos_esperados.iterrows():
            # Comprobar si el hijo ya está en df_sap_final
            if not ((df_sap_completo['producto_padre'] == producto_padre) &
                    (df_sap_completo['producto_hijo'] == hijo['producto'])).any():
                # Si no está, agregarlo
                df_sap_completo = pd.concat([df_sap_completo, pd.DataFrame({
                    'producto_padre': [producto_padre],
                    'producto_hijo': [hijo['producto']],
                    'cantidad_hijo': [hijo['cantidad']]
                })], ignore_index=True)

    return df_sap_completo

# Llamar a la función para verificar y completar los hijos
df_sap_final_completo = verificar_y_completar_hijos(df_sap_final, df)

# Exportar el DataFrame completo a Excel
df_sap_final_completo.to_excel("export_df_sap_completo.xlsx", index=False)
print("Exportación completa. Archivo: export_df_sap_completo.xlsx")

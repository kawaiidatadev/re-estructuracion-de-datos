import sqlite3
import pandas as pd

def segment_first_product(db_path):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)

    # Consulta para seleccionar todos los registros de la tabla "jet_format"
    query = "SELECT * FROM jet_format"

    # Cargar los datos en un DataFrame
    df = pd.read_sql_query(query, conn)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Encontrar la primera ocurrencia de nivel 0
    first_level_0_index = df[df['nivel'] == 0].index[0]

    # Encontrar la siguiente ocurrencia de nivel 0 después de la primera
    next_level_0_index = df[df['nivel'] == 0].index[1]

    # Seleccionar el rango de registros desde el primer nivel 0 hasta el siguiente nivel 0
    selected_df = df.loc[first_level_0_index:next_level_0_index-1]

    # Imprimir el DataFrame seleccionado
    df = selected_df

    # Retornar el dataframe
    return df



def save_product_details(df):
    # Crear una lista para almacenar los detalles del producto
    product_details = []

    for index, row in df.iterrows():
        product = row['producto']
        tipo = row['tipo']
        cantidad = row['cantidad']

        product_details.append({'producto': product, 'tipo': tipo, 'cantidad': cantidad})

    # Convertir la lista en un DataFrame
    product_details_df = pd.DataFrame(product_details)
    print(product_details_df)
    return product_details_df

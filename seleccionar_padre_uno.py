import pandas as pd
import sqlite3


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


def segment_first_product(db_path, cantidad=1):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)

    # Consulta para seleccionar todos los registros de la tabla "jet_format"
    query = "SELECT * FROM jet_format"

    # Cargar los datos en un DataFrame
    df = pd.read_sql_query(query, conn)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Encontrar todos los índices donde 'nivel' es igual a 0
    indices_nivel_0 = df[df['nivel'] == 0].index

    # Verifica que hay suficientes productos de nivel 0
    if len(indices_nivel_0) == 0:
        raise ValueError("No se encontró un nivel 0 en el DataFrame.")

    max_productos = len(indices_nivel_0)
    print(f"Puede escoger hasta {max_productos} productos de nivel 0.")

    if cantidad > max_productos:
        raise ValueError(
            f"Cantidad solicitada ({cantidad}) excede el máximo de productos de nivel 0 disponibles ({max_productos}).")

    # Inicializa una lista para almacenar los rangos de trabajo
    rangos_trabajo = []

    for i in range(cantidad):
        indice_nivel_0 = indices_nivel_0[i]
        nivel_inicial = df.loc[indice_nivel_0, 'nivel']
        indice_siguiente_nivel = df[(df.index > indice_nivel_0) & (df['nivel'] == nivel_inicial)].index

        if not indice_siguiente_nivel.empty:
            indice_fin = indice_siguiente_nivel[0]
        else:
            indice_fin = df.index[-1] + 1

        rango_trabajo = df.loc[indice_nivel_0:indice_fin - 1]
        rangos_trabajo.append(rango_trabajo)

    # Combina todos los rangos de trabajo en un solo DataFrame
    resultado = pd.concat(rangos_trabajo)
    return resultado
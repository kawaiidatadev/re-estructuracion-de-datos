import pandas as pd


def obtener_rango_trabajo(df):
    """
    Encuentra un rango de trabajo en el DataFrame basado en los niveles.

    :param df: DataFrame que contiene una columna 'nivel' para determinar jerarquías.
    :return: DataFrame filtrado con el rango de trabajo.
    """
    # Verifica que la columna 'nivel' existe en el DataFrame
    if 'nivel' not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'nivel'.")

    # Encuentra el índice del primer registro donde 'nivel' es igual a 0
    try:
        indice_nivel_0 = df[df['nivel'] == 0].index[0]
    except IndexError:
        raise ValueError("No se encontró un nivel 0 en el DataFrame.")

    # Encuentra el nivel inicial después de 'nivel' == 0
    nivel_inicial = df.loc[indice_nivel_0, 'nivel']
    indice_siguiente_nivel = df[(df.index > indice_nivel_0) & (df['nivel'] == nivel_inicial)].index

    # Si no hay un siguiente nivel, utiliza hasta el final del DataFrame
    if not indice_siguiente_nivel.empty:
        indice_fin = indice_siguiente_nivel[0]
    else:
        indice_fin = df.index[-1] + 1

    # Filtra el rango de trabajo
    rango_trabajo = df.loc[indice_nivel_0:indice_fin - 1]
    return rango_trabajo

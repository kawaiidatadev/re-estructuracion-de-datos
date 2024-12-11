import sys
import sqlite3
import process_data
from crear_db import save_to_sqlite
from seleccionar_padre_uno import *
import pandas as pd

# Ruta que contiene los archivos Excel
directory_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\data'
excel_files = ['bom1.xlsx', 'bom2.xlsx', 'bom3.xlsx']
db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

# Llamar a la función para procesar los archivos Excel
# df = process_data.process_all_excels(directory_path, excel_files)

# Segundo Paso: Guardar el DataFrame en una base de datos SQLite
# save_to_sqlite(df)

# Funcion para obtener el primer padre con sus hijos
df = segment_first_product(db_path, cantidad=1512)  #genera el df a trabajar. (formato bom)
# print(df)  # Existen 1512 productos de nivel = 0 (se colocan 2 --> [cantidad=2])
# Nivel maximo en todos los bom --> 8

# Obtener el nivel máximo en el DataFrame df
nivel_maximo = df['nivel'].max()
# Imprimir el nivel máximo encontrado
print(f"El nivel máximo encontrado es: {nivel_maximo}")
import time
time.sleep(10)

# Crear un dataframe 'df_sap' nuevo, con las columnas ['producto_padre', 'producto_hijo', 'cantidad_hijo'
df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])


# Función para obtener productos de nivel 0
def obtener_productos_nivel_0(df):
    """
    Detecta y retorna una lista de todos los productos con nivel = 0.
    """
    productos = df[df['nivel'] == 0]['producto'].tolist()
    print(f"Productos nivel 0 detectados: {productos}")
    return productos

# Función para obtener el rango de filas entre dos productos de nivel 0
def obtener_rango_producto(df, producto_actual, siguiente_producto=None):
    """
    Obtiene el rango de filas desde un producto de nivel 0 hasta otro producto de nivel 0.
    """
    inicio = df[df['producto'] == producto_actual].index[0]
    if siguiente_producto:
        fin = df[df['producto'] == siguiente_producto].index[0]
    else:
        fin = len(df)
    rango = df.iloc[inicio:fin]
    print(f"Rango procesado para {producto_actual}: \n{rango}")
    return rango

# Función para obtener productos hijos de un nivel específico dentro de un rango
def obtener_hijos(df_rango, producto_padre, nivel_padre, nivel_hijo):
    """
    Filtra los productos hijos de un nivel específico que pertenecen a un producto padre.
    """
    hijos = []
    agregar = False
    for index, row in df_rango.iterrows():
        if row['producto'] == producto_padre and row['nivel'] == nivel_padre:
            agregar = True
            continue
        if agregar:
            if row['nivel'] <= nivel_padre and row['producto'] != producto_padre:
                break
            if row['nivel'] == nivel_hijo:
                hijos.append((producto_padre, row['producto'], row['cantidad']))
    print(f"Hijos detectados para {producto_padre} (nivel {nivel_hijo}): {hijos}")
    return hijos

# Función para agregar hijos a un DataFrame
def agregar_hijos_a_df(df_sap, hijos):
    """
    Añade las relaciones padre-hijo a un DataFrame de salida.
    """
    for padre, hijo, cantidad in hijos:
        nuevo_df = pd.DataFrame({'producto_padre': [padre], 'producto_hijo': [hijo], 'cantidad_hijo': [cantidad]})
        if not nuevo_df.empty and nuevo_df.notna().all().all():
            df_sap = pd.concat([df_sap, nuevo_df], ignore_index=True) if not df_sap.empty else nuevo_df
    print(f"DataFrame actualizado con hijos: \n{df_sap}")
    return df_sap

# Función recursiva para procesar niveles
def procesar_niveles_recursivo(df, df_sap, rango, producto_padre, nivel_padre, nivel_hijo, max_nivel):
    if nivel_hijo > max_nivel:
        return df_sap

    hijos = obtener_hijos(rango, producto_padre, nivel_padre, nivel_hijo)
    df_sap = agregar_hijos_a_df(df_sap, hijos)

    for _, hijo, _ in hijos:
        df_sap = procesar_niveles_recursivo(df, df_sap, rango, hijo, nivel_hijo, nivel_hijo + 1, max_nivel)

    return df_sap

# Función principal para procesar niveles
def procesar_niveles(df, max_nivel):
    """
    Procesa los niveles jerárquicos de los productos, detectando relaciones nivel por nivel.
    """
    df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])

    # Obtener todos los productos de nivel 0
    productos_padre_nivel_0 = obtener_productos_nivel_0(df)

    # Iterar sobre cada producto de nivel 0
    for i, producto_padre in enumerate(productos_padre_nivel_0):
        print(f"\nProcesando producto padre nivel 0: {producto_padre}")

        # Determinar el siguiente producto de nivel 0 para definir el rango
        siguiente_producto = (
            productos_padre_nivel_0[i + 1] if i + 1 < len(productos_padre_nivel_0) else None
        )

        # Obtener el rango de filas para este producto
        rango = obtener_rango_producto(df, producto_padre, siguiente_producto)

        # Procesar niveles jerárquicos hasta el máximo nivel especificado
        df_sap = procesar_niveles_recursivo(df, df_sap, rango, producto_padre, nivel_padre=0, nivel_hijo=1, max_nivel=max_nivel)

    return df_sap

# Procesar niveles y generar el DataFrame resultante
max_nivel = 8  # Nivel máximo a procesar
df_sap = procesar_niveles(df, max_nivel)

# Guardar resultados creando una tabla "sap_format" en mi db, que ya esta creada, en la ruta:
#db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

import sqlite3

# Función para guardar el DataFrame en la base de datos SQLite
def save_to_sqlite(df_sap, db_path, table_name="sap_format"):
    # Establecer la conexión a la base de datos
    conn = sqlite3.connect(db_path)

    # Guardar el DataFrame en la tabla especificada de la base de datos
    df_sap.to_sql(table_name, conn, if_exists='replace', index=False)

    # Confirmar que se guardó
    print(f"Datos guardados en la tabla '{table_name}' de la base de datos.")

    # Cerrar la conexión
    conn.close()


# Llamar a la función para guardar el DataFrame
save_to_sqlite(df_sap, db_path)
print("\nProceso finalizado. Resultados guardados")
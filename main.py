import process_data
from crear_db import save_to_sqlite
from seleccionar_padre_uno import *
from obtener_rango_de_trabajo import obtener_rango_trabajo

# Ruta que contiene los archivos Excel
directory_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\data'
excel_files = ['bom1.xlsx', 'bom2.xlsx', 'bom3.xlsx']
db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

# Llamar a la función para procesar los archivos Excel
# df = process_data.process_all_excels(directory_path, excel_files)

# Segundo Paso: Guardar el DataFrame en una base de datos SQLite
# save_to_sqlite(df)

# Funcion para obtener el primer padre con sus hijos
df = segment_first_product(db_path) #genera el df orifginal a trabajar. (formato bom)

# Funcion que guarda en memoria el producto, su tipo, y la cantidad.
# save_product_details(df)

# Funcion que obtiene en "df" el rango de trabajo (un solo producto de nivel 1 y sus hijos en formato bom)
df = obtener_rango_trabajo(df)


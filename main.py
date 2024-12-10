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
df = segment_first_product(db_path, cantidad=2)  #genera el df orifginal a trabajar. (formato bom)
print(df)  # 1512 productos nivel = 0

#


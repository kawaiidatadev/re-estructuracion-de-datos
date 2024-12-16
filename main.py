import sys
import sqlite3
import process_data
from crear_db import save_to_sqlite
from seleccionar_padre_uno import *
import pandas as pd
import time

# Ruta que contiene los archivos Excel
# directory_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\data'
# excel_files = ['bom1.xlsx', 'bom2.xlsx', 'bom3.xlsx']
db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

# Despues de la segunda actualizacion con todos los bom con ETL manual en su nivel (n-1)

directory_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\data_ETL'
excel_files = ['jet_format_todo.xlsx']

# Llamar a la función para procesar los archivos Excel
df = process_data.process_all_excels(directory_path, excel_files)

# Segundo Paso: Guardar el DataFrame en una base de datos SQLite
save_to_sqlite(df)

# Funcion para obtener el primer padre con sus hijos
df = segment_first_product(db_path, cantidad=1512)  #genera el df a trabajar. (formato bom)
print(df)  # Existen 1512 productos de nivel = 0, segunda ETL manual : 149200 productos

# Obtener el nivel máximo en el DataFrame df
nivel_maximo = df['nivel'].max()
# Nivel maximo en todos los bom --> 8
print(f"El nivel máximo encontrado es: {nivel_maximo}")
time.sleep(8)
sys.exit(0)

# Crear un dataframe 'df_sap' nuevo, con las columnas ['producto_padre', 'producto_hijo', 'cantidad_hijo'
df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])


# Procesar niveles y generar el DataFrame resultante
from recostructor import *
max_nivel = int(nivel_maximo)  # Nivel máximo a procesar
df_sap = procesar_niveles(df, max_nivel)




# Llamar a la función para guardar el DataFrame
# save_to_sqlite(df_sap, db_path)
print("\nProceso finalizado. Resultados guardados")
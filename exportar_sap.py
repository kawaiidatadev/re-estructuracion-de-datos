import sqlite3
import pandas as pd
import os

# Ruta de la base de datos y directorio de exportación
db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'
exceles_con_la_tabla = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite'

# Conectar a la base de datos SQLite
conn = sqlite3.connect(db_path)

# Definir el número máximo de filas por archivo Excel (Excel tiene un límite de 1,048,576 filas)
max_rows_per_excel = 1048576

# Leer todos los registros de la tabla sap_format
query = "SELECT * FROM sap_format"
df = pd.read_sql(query, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Contar cuántos archivos Excel necesitamos
num_files = len(df) // max_rows_per_excel + 1

# Exportar a múltiples archivos Excel
for i in range(num_files):
    # Determinar el rango de filas para el archivo actual
    start_row = i * max_rows_per_excel
    end_row = min((i + 1) * max_rows_per_excel, len(df))

    # Obtener el DataFrame para el archivo actual
    df_chunk = df.iloc[start_row:end_row]

    # Nombre del archivo Excel
    excel_file = os.path.join(exceles_con_la_tabla, f'sap_format_{i + 1}.xlsx')

    # Exportar el DataFrame a Excel
    df_chunk.to_excel(excel_file, index=False)

    print(f"Exportando {excel_file}...")

print("Exportación completada.")

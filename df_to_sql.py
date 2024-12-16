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

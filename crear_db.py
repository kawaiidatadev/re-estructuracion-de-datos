import sqlite3 as sq3

def save_to_sqlite(df):
    try:
        # Ensure the 'nivel' column is of integer type
        df['nivel'] = df['nivel'].astype(int)
        print(df['nivel'])

        # Define the path for the SQLite database
        db_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\Proyectos\En proceso\sap_data\db_sqlite\db.db'

        # Connect to the SQLite database
        conn = sq3.connect(db_path)

        # Save the DataFrame to SQLite
        df.to_sql('jet_format', conn, if_exists='replace', index=False)

        # Commit and close the connection
        conn.commit()
        conn.close()
        print(f"Datos guardados exitosamente en {db_path}")

    except Exception as e:
        print(f"Error al guardar en SQLite: {e}")
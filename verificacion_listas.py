import os
import pandas as pd

# Ruta donde se encuentran los archivos Excel
ruta = r"C:\\Users\\lmacias\\Downloads\\Reforma SAP\\data"

# Lista de nombres a buscar
nombres_a_buscar = [
    "200-ARN1AL12VRT6.5",
    "200-ARN2AL12VRT6.0",
    "200-ARN2AL12VRT6.1",
    "200-ARN2AL12VRT7.2",
    "200-ARN2AL12VRT9",
    "200-ARN2AL12VRT9.1",
    "200-ARN2ALVRT6.5"
]

# Lista para almacenar los resultados
encontrados = []

# Iterar sobre los archivos en la ruta
for archivo in os.listdir(ruta):
    if archivo.endswith('.xlsx'):
        archivo_path = os.path.join(ruta, archivo)
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo_path, sheet_name=None, engine='openpyxl')

            # Iterar sobre las hojas del archivo
            for nombre_hoja, datos in df.items():
                # Iterar sobre las filas y buscar coincidencias
                for index, row in datos.iterrows():
                    if any(nombre in str(row.values) for nombre in nombres_a_buscar):
                        encontrados.append(
                            {
                                'Archivo': archivo,
                                'Hoja': nombre_hoja,
                                'Fila': index + 1,
                                'Datos_Fila': row.to_dict()
                            }
                        )
        except Exception as e:
            print(f"Error al procesar el archivo {archivo}: {e}")

# Mostrar resultados
encontrados_df = pd.DataFrame(encontrados)
if not encontrados_df.empty:
    print(encontrados_df)
    # Guardar resultados en un archivo Excel
    encontrados_df.to_excel(r"C:\\Users\\lmacias\\Downloads\\resultados.xlsx", index=False)
    print("Resultados guardados en resultados.xlsx")
else:
    print("No se encontraron coincidencias.")
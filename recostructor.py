import pandas as pd
import #  time

# Función para obtener productos de nivel 0
def obtener_productos_nivel_0(df):
    """
    Detecta y retorna una lista de todos los productos con nivel = 0.
    """
    print("Inicio de la función 'obtener_productos_nivel_0'.")
    print("Objetivo: Identificar todos los productos en el DataFrame que tienen el nivel 0.")
    #  time.sleep(15)

    # Filtramos el DataFrame para encontrar filas donde la columna 'nivel' sea igual a 0
    print("Filtrando el DataFrame para detectar las filas donde 'nivel' sea igual a 0.")
    productos = df[df['nivel'] == 0]['producto'].tolist()

    print("Conversión del resultado a una lista con los productos de nivel 0.")
    print(f"Productos detectados con nivel 0: {productos}")
    #  time.sleep(15)

    # Retornamos la lista de productos de nivel 0
    print("Devolviendo la lista de productos de nivel 0 para su uso posterior.")
    return productos


# Función para obtener el rango de filas entre dos productos de nivel 0
def obtener_rango_producto(df, producto_actual, siguiente_producto=None):
    """
    Obtiene el rango de filas desde un producto de nivel 0 hasta otro producto de nivel 0.
    """
    print("\nInicio de la función 'obtener_rango_producto'.")
    print(
        "Objetivo: Extraer un subconjunto de filas del DataFrame que representan el rango entre dos productos de nivel 0.")
    print(f"Producto actual: {producto_actual}. Producto siguiente: {siguiente_producto}.")
    #  time.sleep(15)

    # Encontramos el índice de inicio del producto actual
    print("Buscando el índice del producto actual en el DataFrame.")
    inicio = df[df['producto'] == producto_actual].index[0]
    print(f"Índice de inicio encontrado: {inicio}.")
    #  time.sleep(15)

    # Determinamos el índice de fin con base en el producto siguiente, si existe
    if siguiente_producto:
        print("Buscando el índice del siguiente producto en el DataFrame.")
        fin = df[df['producto'] == siguiente_producto].index[0]
        print(f"Índice de fin encontrado: {fin}.")
    else:
        print("No se proporcionó un producto siguiente. Usaremos el tamaño total del DataFrame como índice de fin.")
        fin = len(df)
        print(f"Índice de fin establecido en: {fin}.")
    #  time.sleep(15)

    # Extraemos el rango de filas entre los índices de inicio y fin
    print("Extrayendo el rango de filas del DataFrame entre los índices de inicio y fin.")
    rango = df.iloc[inicio:fin]
    print(f"Rango extraído:\n{rango}")
    #  time.sleep(15)

    # Retornamos el rango extraído
    print("Devolviendo el rango procesado para su uso posterior.")
    return rango


# Función para obtener productos hijos de un nivel específico dentro de un rango
def obtener_hijos(df_rango, producto_padre, nivel_padre, nivel_hijo):
    """
    Filtra los productos hijos de un nivel específico que pertenecen a un producto padre.
    """
    print("\nInicio de la función 'obtener_hijos'.")
    print("Objetivo: Identificar productos hijos que se encuentren en un rango de filas del DataFrame.")
    print(f"Producto padre: {producto_padre}, Nivel del padre: {nivel_padre}, Nivel de los hijos: {nivel_hijo}.")
    #  time.sleep(15)

    # Lista para almacenar los hijos detectados
    print("Inicializando una lista vacía para almacenar los productos hijos detectados.")
    hijos = []

    # Variable para determinar cuándo empezar a agregar hijos
    print("Inicializando una bandera 'agregar' como False para controlar cuándo empezar a registrar hijos.")
    agregar = False

    # Iteramos sobre cada fila del rango de filas
    print("Iniciando iteración sobre las filas del rango proporcionado.")
    for index, row in df_rango.iterrows():
        print(f"Procesando fila en el índice {index}: {row.to_dict()}")

        # Si encontramos el producto padre en el nivel indicado, activamos la bandera
        if row['producto'] == producto_padre and row['nivel'] == nivel_padre:
            print(f"Producto padre detectado en el índice {index}. Activando bandera 'agregar'.")
            agregar = True
            continue

        # Si estamos agregando y encontramos un nivel igual o superior al padre, terminamos
        if agregar:
            if row['nivel'] <= nivel_padre and row['producto'] != producto_padre:
                print(f"Encontrado un producto de nivel menor o igual al nivel del padre. Terminando iteración.")
                break

            # Si el nivel coincide con el nivel de los hijos, añadimos el producto a la lista
            if row['nivel'] == nivel_hijo:
                print(
                    f"Hijo detectado: Producto padre: {producto_padre}, Producto hijo: {row['producto']}, Cantidad: {row['cantidad']}.")
                hijos.append((producto_padre, row['producto'], row['cantidad']))
        #  time.sleep(3)

    # Retornamos la lista de hijos detectados
    print(f"Hijos detectados para el producto {producto_padre} (nivel {nivel_hijo}): {hijos}")
    return hijos



# Función para agregar hijos a un DataFrame
def agregar_hijos_a_df(df_sap, hijos):
    """
    Añade las relaciones padre-hijo a un DataFrame de salida.
    """
    print("\nInicio de la función 'agregar_hijos_a_df'.")
    print("Objetivo: Tomar una lista de relaciones padre-hijo y añadirlas al DataFrame de salida llamado 'df_sap'.")
    #  time.sleep(20)

    for padre, hijo, cantidad in hijos:
        print(f"\nProcesando hijo: Padre: {padre}, Hijo: {hijo}, Cantidad: {cantidad}")
        # Crear un nuevo DataFrame con las relaciones padre-hijo detectadas
        nuevo_df = pd.DataFrame({'producto_padre': [padre], 'producto_hijo': [hijo], 'cantidad_hijo': [cantidad]})
        print(f"Nuevo DataFrame creado: \n{nuevo_df}")

        # Verificar si el nuevo DataFrame no está vacío y no contiene valores nulos
        if not nuevo_df.empty and nuevo_df.notna().all().all():
            print("El nuevo DataFrame no está vacío y no contiene valores nulos. Procediendo a concatenar.")
            df_sap = pd.concat([df_sap, nuevo_df], ignore_index=True) if not df_sap.empty else nuevo_df
        else:
            print("El nuevo DataFrame está vacío o contiene valores nulos. Se omite esta entrada.")
        #  time.sleep(3)

    print(f"\nDataFrame actualizado con las relaciones padre-hijo detectadas: \n{df_sap}")
    return df_sap


# Función recursiva para procesar niveles
def procesar_niveles_recursivo(df, df_sap, rango, producto_padre, nivel_padre, nivel_hijo, max_nivel):
    print("\nInicio de la función recursiva 'procesar_niveles_recursivo'.")
    print(
        f"Objetivo: Procesar de manera recursiva las relaciones jerárquicas de los productos desde el producto padre '{producto_padre}' ")
    print(
        f"Nivel actual del padre: {nivel_padre}, Nivel de los hijos: {nivel_hijo}, Máximo nivel permitido: {max_nivel}.")
    #  time.sleep(20)

    # Si el nivel hijo excede el máximo nivel permitido, se detiene la recursión
    if nivel_hijo > max_nivel:
        print(
            f"Nivel hijo {nivel_hijo} excede el máximo nivel permitido {max_nivel}. Finalizando recursión para este camino.")
        return df_sap

    # Obtener los hijos del producto padre actual dentro del rango
    print("Llamando a la función 'obtener_hijos' para identificar los productos hijos.")
    hijos = obtener_hijos(rango, producto_padre, nivel_padre, nivel_hijo)
    print(f"Hijos detectados: {hijos}")
    #  time.sleep(15)

    # Añadir las relaciones padre-hijo detectadas al DataFrame de salida
    print("Llamando a la función 'agregar_hijos_a_df' para añadir los hijos detectados al DataFrame de salida.")
    df_sap = agregar_hijos_a_df(df_sap, hijos)

    # Iterar sobre cada hijo detectado para procesar sus propios hijos de forma recursiva
    print("Iniciando iteración sobre los hijos detectados para procesar sus relaciones jerárquicas.")
    for _, hijo, _ in hijos:
        print(f"\nProcesando hijo '{hijo}' como nuevo producto padre en el siguiente nivel.")
        df_sap = procesar_niveles_recursivo(df, df_sap, rango, hijo, nivel_hijo, nivel_hijo + 1, max_nivel)
        #  time.sleep(15)

    print(f"\nFinalizando procesamiento recursivo para el producto padre '{producto_padre}' en el nivel {nivel_padre}.")
    return df_sap


# Función principal para procesar niveles
def procesar_niveles(df, max_nivel):
    """
    Procesa los niveles jerárquicos de los productos, detectando relaciones nivel por nivel.
    """
    print("\nInicio de la función principal 'procesar_niveles'.")
    print(f"Objetivo: Detectar todas las relaciones jerárquicas hasta un nivel máximo especificado: {max_nivel}.")
    #  time.sleep(20)

    # Inicializar el DataFrame de salida
    print(
        "Inicializando el DataFrame de salida vacío con columnas: ['producto_padre', 'producto_hijo', 'cantidad_hijo'].")
    df_sap = pd.DataFrame(columns=['producto_padre', 'producto_hijo', 'cantidad_hijo'])
    #  time.sleep(20)

    # Obtener todos los productos de nivel 0
    print("Llamando a la función 'obtener_productos_nivel_0' para identificar los productos raíz (nivel 0).")
    productos_padre_nivel_0 = obtener_productos_nivel_0(df)
    print(f"Productos detectados de nivel 0: {productos_padre_nivel_0}")
    #  time.sleep(20)

    # Iterar sobre cada producto de nivel 0
    for i, producto_padre in enumerate(productos_padre_nivel_0):
        print(f"\nProcesando producto raíz: '{producto_padre}' (nivel 0).")

        # Determinar el siguiente producto de nivel 0 para definir el rango
        siguiente_producto = (
            productos_padre_nivel_0[i + 1] if i + 1 < len(productos_padre_nivel_0) else None
        )
        print(f"Producto siguiente: {siguiente_producto if siguiente_producto else 'Ninguno (último producto raíz)'}.")
        #  time.sleep(20)

        # Obtener el rango de filas para este producto
        print(
            "Llamando a la función 'obtener_rango_producto' para determinar el rango de filas del DataFrame correspondiente a este producto raíz.")
        rango = obtener_rango_producto(df, producto_padre, siguiente_producto)
        print(f"Rango obtenido:\n{rango}")
        #  time.sleep(20)

        # Procesar niveles jerárquicos hasta el máximo nivel especificado
        print("Llamando a la función 'procesar_niveles_recursivo' para procesar jerarquías desde este producto raíz.")
        df_sap = procesar_niveles_recursivo(df, df_sap, rango, producto_padre, nivel_padre=0, nivel_hijo=1,
                                            max_nivel=max_nivel)

    print(
        "\nProcesamiento completo de todos los productos raíz. Devolviendo el DataFrame de salida con las jerarquías detectadas.")
    return df_sap

from django.db import connection

def consultar_inmuebles_para_arriendo():
    sql_query = """
    SELECT comuna.comuna, inmueble.nombre_inmueble, inmueble.descripcion
    FROM gestion_inmuebles_inmueble inmueble
    JOIN gestion_inmuebles_comuna comuna ON inmueble.comuna_id = comuna.id
    ORDER BY comuna.comuna, inmueble.nombre_inmueble;
    """
    
    # Execute SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        resultados = cursor.fetchall()

    # Debug: Print the query results length and raw data
    print(f"Resultados encontrados: {len(resultados)}")
    print(f"Datos brutos: {resultados}")

    if resultados:
        for row in resultados:
            print(f"Comuna: {row[0]}")
            print(f"Nombre Inmueble: {row[1]}")
            print(f"Descripción: {row[2]}")
            print("-" * 40)  # Separator between records
    else:
        print("No se encontraron inmuebles para arriendo.")

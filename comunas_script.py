from django.db import connection

def obtener_comunas_por_region(region_nombre):
    # Definir la consulta SQL
    sql_query = """
    SELECT comuna.comuna, region.region
    FROM gestion_inmuebles_comuna comuna
    JOIN gestion_inmuebles_region region ON comuna.region_id = region.id
    WHERE region.region = %s;
    """
    
    # Ejecutar la consulta SQL
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [region_nombre])
        resultados = cursor.fetchall()

    # Mostrar los resultados en consola
    if resultados:
        print(f"Comunas en la región {region_nombre}:")
        for row in resultados:
            print(f"- {row[0]} ({row[1]})")
    else:
        print(f"No se encontraron comunas en la región {region_nombre}.")

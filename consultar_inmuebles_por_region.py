import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Update with your project settings
django.setup()

from django.db import connection

# Function to query properties for rent, grouped by region
def consultar_inmuebles_por_region():
    # SQL Query to get inmuebles grouped by region
    sql_query = """
    SELECT region.region, comuna.comuna, inmueble.nombre_inmueble, inmueble.descripcion
    FROM gestion_inmuebles_inmueble inmueble
    JOIN gestion_inmuebles_comuna comuna ON inmueble.comuna_id = comuna.id
    JOIN gestion_inmuebles_region region ON comuna.region_id = region.id
    ORDER BY region.region, comuna.comuna, inmueble.nombre_inmueble;
    """

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        resultados = cursor.fetchall()

    # Group results by region
    inmuebles_por_region = {}
    for row in resultados:
        region, comuna, nombre_inmueble, descripcion = row
        if region not in inmuebles_por_region:
            inmuebles_por_region[region] = []
        inmuebles_por_region[region].append({
            'comuna': comuna,
            'nombre_inmueble': nombre_inmueble,
            'descripcion': descripcion
        })

    # Print the results directly in the terminal (Python shell)
    for region, inmuebles in inmuebles_por_region.items():
        print(f"Región: {region}")
        for inmueble in inmuebles:
            print(f"  Comuna: {inmueble['comuna']}")
            print(f"    Nombre Inmueble: {inmueble['nombre_inmueble']}")
            print(f"    Descripción: {inmueble['descripcion']}")
            print("-" * 40)  # Separator between properties
        print("\n" + "=" * 80)  # Separator between regions

# Run the function when the script is executed
consultar_inmuebles_por_region()

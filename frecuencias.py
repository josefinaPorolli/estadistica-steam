# Para generar el reporte, se hará, por cada variable tomada, un conteo de la cantidad de veces que cada valor se repite, haciendo un análisis por separado de aquellos juegos en early access y aquellos que fueron lanzados directamente.

import pandas as pd # para el manejo de dataframes
import matplotlib.pyplot as plt # para la generación de gráficos

# Traer los datos del json
data = pd.read_json('data.json')

####### PRECIO BASE ###########
# Intervalos tomados de 10 dólares hasta 60 dólares
intervalos_precio = [0, 10, 20, 30, 40, 50, 60]

# ===== Early access =====
early_access = data[data['early_access'] == True] # Filtrar los juegos en early access
precio_base_early_access = early_access['precio_base'] # Tomar la columna de precio base

# Contar la cantidad de juegos en cada intervalo de precio
conteo_precio_early_access = pd.cut(precio_base_early_access, bins=intervalos_precio).value_counts().sort_index()

# ===== Lanzados directamente =====
lanzados_directamente = data[data['early_access'] == False] # Filtrar los juegos lanzados directamente
precio_base_lanzados_directamente = lanzados_directamente['precio_base'] # Tomar la columna de precio base

# Contar la cantidad de juegos en cada intervalo de precio
conteo_precio_lanzados_directamente = pd.cut(precio_base_lanzados_directamente, bins=intervalos_precio).value_counts().sort_index()

# Imprimir los resultados
print("Conteo de juegos en early access por intervalo de precio:")
print(conteo_precio_early_access)
print("\nConteo de juegos lanzados directamente por intervalo de precio:")
print(conteo_precio_lanzados_directamente)



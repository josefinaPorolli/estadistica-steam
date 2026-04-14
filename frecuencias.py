# Para generar el reporte, se hará, por cada variable tomada, un conteo de la cantidad de veces que cada valor se repite, haciendo un análisis por separado de aquellos juegos en early access y aquellos que fueron lanzados directamente.

import pandas as pd # para el manejo de dataframes
import matplotlib.pyplot as plt # para la generación de gráficos
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Traer los datos del json
data = pd.read_json('data.json')

# Estilos para gráficos
plt.style.use("seaborn-v0_8-darkgrid")

####### PRECIO BASE ###########
# Intervalos tomados de 10 dólares hasta 60 dólares
intervalos_precio = [0, 10, 20, 30, 40, 50, 60]

# ===== Early access =====
early_access = data[data['estado_lanzamiento'] == 'Early Access'] # Filtrar los juegos en early access
precio_base_early_access = early_access['precio_base_usd'] # Tomar la columna de precio base

# ===== Lanzados directamente =====
lanzados_directamente = data[data['estado_lanzamiento'] == 'Completo Directo'] # Filtrar los juegos lanzados directamente
precio_base_lanzados_directamente = lanzados_directamente['precio_base_usd'] # Tomar la columna de precio base

# Función para generar tabla de frecuencias
def generar_tabla_frecuencias(valores, bins, label):
    counts, bin_edges = pd.cut(valores, bins=bins, retbins=True, right=False)
    freq_data = counts.value_counts().sort_index()
    
    tabla = []
    intervalos = [f"[{bin_edges[i]:.1f}, {bin_edges[i+1]:.1f})" for i in range(len(bin_edges)-1)]
    
    n = len(valores)
    fi_acum = 0
    hi_acum = 0.0
    
    for i, intervalo in enumerate(intervalos):
        fi = freq_data.get(pd.Interval(left=bin_edges[i], right=bin_edges[i+1], closed='left'), 0)
        hi = fi / n
        fi_acum += fi
        hi_acum += hi
        
        tabla.append({
            'intervalo': intervalo,
            'fi': fi,
            'hi': round(hi, 3),
            'Fi': fi_acum,
            'Hi': round(hi_acum, 3)
        })
    
    return tabla, freq_data, bin_edges, n

# Generar tablas
tabla_ea, freq_ea, edges_ea, n_ea = generar_tabla_frecuencias(precio_base_early_access, intervalos_precio, "Early Access")
tabla_cd, freq_cd, edges_cd, n_cd = generar_tabla_frecuencias(precio_base_lanzados_directamente, intervalos_precio, "Completo Directo")

# Crear gráficos
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico Early Access
axes[0].hist(precio_base_early_access, bins=intervalos_precio, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Precio base (USD$)')
axes[0].set_ylabel('Frecuencia Absoluta')
axes[0].set_title('Early Access - Distribución de Precios')
axes[0].yaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Gráfico Completo Directo
axes[1].hist(precio_base_lanzados_directamente, bins=intervalos_precio, color='coral', edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Precio base (USD$)')
axes[1].set_ylabel('Frecuencia Absoluta')
axes[1].set_title('Completo Directo - Distribución de Precios')
axes[1].yaxis.set_major_locator(plt.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig(IMAGES_DIR / "frecuencias.png", dpi=150, bbox_inches='tight')
plt.close()

# Crear archivo markdown
md_content = "# Frecuencias\n\n"
md_content += "## Organización y presentación de los datos: construcción de distribuciones de frecuencias\n\n"
md_content += "Se realizó un análisis de las distribuciones de frecuencias absolutas y relativas, simples y acumuladas de la variable **precio base (USD)** de los videojuegos de la muestra, diferenciando entre juegos en Early Access y juegos lanzados directamente.\n\n"

# Tabla Early Access
md_content += "### Juegos en Early Access\n\n"
md_content += "| Intervalo | fi | hi | Fi | Hi |\n"
md_content += "|---|---:|---:|---:|---:|\n"
for row in tabla_ea:
    md_content += f"| {row['intervalo']} | {row['fi']} | {row['hi']} | {row['Fi']} | {row['Hi']} |\n"
md_content += f"\n**Total de juegos en Early Access:** {n_ea}\n\n"

# Tabla Completo Directo
md_content += "### Juegos Lanzados Directamente\n\n"
md_content += "| Intervalo | fi | hi | Fi | Hi |\n"
md_content += "|---|---:|---:|---:|---:|\n"
for row in tabla_cd:
    md_content += f"| {row['intervalo']} | {row['fi']} | {row['hi']} | {row['Fi']} | {row['Hi']} |\n"
md_content += f"\n**Total de juegos lanzados directamente:** {n_cd}\n\n"

# Gráficos
md_content += "## Visualización\n\n"
md_content += "![Distribución de Frecuencias](images/frecuencias.png)\n\n"

md_content += "## Análisis e Interpretación\n\n"
md_content += "- Los juegos en **Early Access** se concentran en el rango de precios más bajo ($10-20)\n"
md_content += "- Los juegos **lanzados directamente** tienen una distribución más dispersa con presencia en rangos superiores\n"
md_content += "- La frecuencia relativa acumulada permite observar qué porcentaje de juegos está por debajo de cada límite de intervalo\n"

# Guardar markdown
with open(BASE_DIR / "frecuencias.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("✓ Archivo frecuencias.md generado correctamente")
print(f"✓ Gráficos guardados en: {IMAGES_DIR}")
print(f"\nResumen:")
print(f"- Early Access: {n_ea} juegos")
print(f"- Completo Directo: {n_cd} juegos")



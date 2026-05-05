import pandas as pd
from pathlib import Path

# 1. Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
REPORTES_DIR = BASE_DIR / "reportes"
REPORTES_DIR.mkdir(exist_ok=True)

# Archivo donde se guardarán tus tablas
archivo_salida = REPORTES_DIR / "asimetria_y_apuntamiento.md"

# 2. Cargar los datos
ruta_datos = BASE_DIR / "data.json"
df = pd.read_json(ruta_datos)

# Diccionario para buscar en el JSON y mostrar un nombre bonito en la tabla
variables = {
    'precio_base_usd': 'Precio', 
    'porcentaje_resenas_positivas': '% positivas', 
    'pico_historico_concurrentes': 'Pico histórico', 
    'jugadores_promedio': 'Jugadores promedio'
}

def calcular_forma(df_grupo, nombre_grupo, archivo):
    archivo.write(f"### {nombre_grupo}\n\n")
    archivo.write(f"| Variable | Asimetría (Sesgo) | Apuntamiento (Curtosis) |\n")
    archivo.write(f"|:--------------------------------|------------------:|------------------------:|\n")
    
    for var_json, nombre_tabla in variables.items():
        if var_json in df_grupo.columns:
            # Calculamos asimetría y curtosis
            asimetria = df_grupo[var_json].skew()
            curtosis = df_grupo[var_json].kurt()
            
            # Escribimos la fila usando el nombre bonito
            archivo.write(f"| {nombre_tabla:<31} | {asimetria:>17.2f} | {curtosis:>23.2f} |\n")
    
    archivo.write("\n<br>\n\n")

# 3. Separar los datos usando la llave exacta de tu JSON ('estado_lanzamiento')
df_completo = df[df['estado_lanzamiento'] == 'Completo Directo']
df_early = df[df['estado_lanzamiento'] == 'Early Access']

# 4. Generar el reporte
print("Generando reporte de Asimetría y Apuntamiento...")

with open(archivo_salida, 'w', encoding='utf-8') as f:
    f.write("# Reporte de Asimetría y Apuntamiento\n\n")
    
    calcular_forma(df_completo, "Completo Directo", f)
    calcular_forma(df_early, "Early Access", f)

print(f"¡Listo! El reporte se guardó en: {archivo_salida}")
import pandas as pd
import numpy as np
from scipy import stats
import io

# 1. Carga de datos (basado en muestra_etapa1.csv)
data = """AppID,Nombre,Precio base (USD),Porcentaje de reseñas positivas,Categoría de reseñas,Pico histórico / CCU,Jugadores Promedio,Estado de lanzamiento,Soporte Multiplataforma,Género principal
730,Counter-Strike 2,0.0,86.7%,Very Positive,1013936,33597,Completo Directo,"Windows, Linux",Action
271590,Grand Theft Auto V Legacy,N/A,87.4%,Very Positive,67851,14589,Completo Directo,Windows,Action
292030,The Witcher 3: Wild Hunt,39.99,96.1%,Overwhelmingly Positive,15893,3662,Completo Directo,Windows,RPG
1091500,Cyberpunk 2077,59.99,84.4%,Very Positive,22265,4922,Completo Directo,"Windows, Mac",RPG
367520,Hollow Knight,14.99,97.0%,Overwhelmingly Positive,4912,2235,Completo Directo,"Windows, Mac, Linux",Action
1623730,Palworld,29.99,94.1%,Very Positive,18028,3869,Early Access,Windows,Action
1145350,Hades II,29.99,94.9%,Overwhelmingly Positive,1838,2525,Completo Directo,"Windows, Mac",Action
892970,Valheim,19.99,94.3%,Very Positive,14439,4688,Early Access,"Windows, Mac, Linux",Action
739630,Phasmophobia,19.99,95.8%,Overwhelmingly Positive,9978,2439,Early Access,Windows,Action
108600,Project Zomboid,19.99,94.2%,Very Positive,22864,4215,Early Access,"Windows, Mac, Linux",Indie"""

df = pd.read_csv(io.StringIO(data))

# 2. Limpieza de datos
# Convertir porcentajes a flotantes [cite: 48]
df['Porcentaje de reseñas positivas'] = df['Porcentaje de reseñas positivas'].str.rstrip('%').astype('float')
# Manejar precios N/A o 0.0 [cite: 46]
df['Precio base (USD)'] = pd.to_numeric(df['Precio base (USD)'], errors='coerce').fillna(0)

print("--- ANÁLISIS DE VARIANZA (ANOVA) ---")
# Objetivo: Comparar si el 'Género principal' influye en los 'Jugadores Promedio' [cite: 6, 54]
# Hipótesis:
# H0: No hay diferencia en el promedio de jugadores entre géneros.
# H1: Al menos un género tiene un promedio de jugadores distinto.

grupos_genero = [group['Jugadores Promedio'].values for name, group in df.groupby('Género principal')]

f_stat, p_value_anova = stats.f_oneway(*grupos_genero)

print(f"Estadístico F: {f_stat:.4f}")
print(f"Valor p (ANOVA): {p_value_anova:.4f}")

if p_value_anova < 0.05:
    print("Resultado: Se rechaza H0. El género influye significativamente en la cantidad de jugadores.")
else:
    print("Resultado: No se rechaza H0. No hay evidencia de que el género afecte el promedio de jugadores.")

print("\n--- PRUEBA DE INDEPENDENCIA CHI-CUADRADO (Bondad de Ajuste) ---")
# Objetivo: Ver si el 'Estado de lanzamiento' está relacionado con la 'Categoría de reseñas' 
# H0: El estado de lanzamiento y la categoría de reseñas son independientes.
# H1: Existe una relación entre el estado de lanzamiento y la satisfacción del usuario.

contingency_table = pd.crosstab(df['Estado de lanzamiento'], df['Categoría de reseñas'])
print("Tabla de contingencia:")
print(contingency_table)

chi2, p_value_chi2, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\nEstadístico Chi-cuadrado: {chi2:.4f}")
print(f"Valor p: {p_value_chi2:.4f}")

if p_value_chi2 < 0.05:
    print("Resultado: Se rechaza H0. Existe una relación entre el modelo Early Access y la categoría de reseñas.")
else:
    print("Resultado: No se rechaza H0. El tipo de lanzamiento parece independiente de la categoría de reseña en esta muestra.")
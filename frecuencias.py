# Genera un reporte de frecuencias para variables continuas y categóricas
# separando juegos en Early Access y Completo Directo.

from math import ceil, floor, log10
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Configuracion de rutas
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
REPORTES_DIR = BASE_DIR / "reportes"

IMAGES_DIR.mkdir(exist_ok=True)
REPORTES_DIR.mkdir(exist_ok=True)

# Estilo para graficos
plt.style.use("seaborn-v0_8-darkgrid")


def construir_bins_paso(valores: pd.Series, paso: float, minimo: float | None = None, maximo: float | None = None):
    """Construye bordes de intervalos de ancho fijo y cubre todo el rango de datos."""
    valor_min = float(valores.min()) if minimo is None else float(minimo)
    valor_max = float(valores.max()) if maximo is None else float(maximo)

    inicio = floor(valor_min / paso) * paso
    fin = ceil(valor_max / paso) * paso

    if fin <= inicio:
        fin = inicio + paso
    fin += paso

    bins = []
    actual = inicio
    while actual <= fin:
        bins.append(round(actual, 10))
        actual += paso

    return bins


def construir_bins_optimos_sturges(valores: pd.Series):
    """Calcula intervalos para variables continuas usando la regla de Sturges."""
    serie = valores.dropna()
    n = len(serie)

    if n <= 1:
        v = float(serie.iloc[0]) if n == 1 else 0.0
        return [v, v + 1]

    k = max(4, round(1 + 3.322 * log10(n)))
    rango = float(serie.max() - serie.min())
    amplitud = max(1.0, ceil(rango / k))

    inicio = floor(float(serie.min()) / amplitud) * amplitud
    fin = ceil(float(serie.max()) / amplitud) * amplitud
    if fin <= inicio:
        fin = inicio + amplitud
    fin += amplitud

    bins = []
    actual = inicio
    while actual <= fin:
        bins.append(round(actual, 10))
        actual += amplitud

    return bins


def generar_tabla_frecuencias_intervalos(valores: pd.Series, bins: list[float]):
    """Calcula frecuencias absolutas y relativas (simples y acumuladas) por intervalo."""
    categorias, bin_edges = pd.cut(valores, bins=bins, retbins=True, right=False)
    freq_data = categorias.value_counts().sort_index()

    intervalos = [f"[{bin_edges[i]:.1f}, {bin_edges[i + 1]:.1f})" for i in range(len(bin_edges) - 1)]

    n = len(valores)
    fi_acum = 0
    hi_acum = 0.0
    tabla = []

    for i, intervalo in enumerate(intervalos):
        fi = freq_data.get(pd.Interval(left=bin_edges[i], right=bin_edges[i + 1], closed="left"), 0)
        hi = fi / n if n else 0
        fi_acum += fi
        hi_acum += hi

        tabla.append(
            {
                "categoria": intervalo,
                "fi": int(fi),
                "hi": round(hi, 3),
                "Fi": int(fi_acum),
                "Hi": round(hi_acum, 3),
            }
        )

    return tabla, n


def generar_tabla_frecuencias_categorias(valores: pd.Series, orden: list[str] | None = None):
    """Calcula frecuencias absolutas y relativas (simples y acumuladas) para categorías."""
    serie = valores.dropna().astype(str)
    conteos = serie.value_counts()

    categorias = orden if orden is not None else sorted(conteos.index.tolist())

    n = len(serie)
    fi_acum = 0
    hi_acum = 0.0
    tabla = []

    for categoria in categorias:
        fi = int(conteos.get(categoria, 0))
        hi = fi / n if n else 0
        fi_acum += fi
        hi_acum += hi
        tabla.append(
            {
                "categoria": categoria,
                "fi": fi,
                "hi": round(hi, 3),
                "Fi": fi_acum,
                "Hi": round(hi_acum, 3),
            }
        )

    return tabla, n


def agregar_tabla_markdown(md_content: list[str], titulo: str, tabla: list[dict], total: int):
    md_content.append(f"### {titulo}\n")
    md_content.append("| Categoría / Intervalo | fi | hi | Fi | Hi |\n")
    md_content.append("|---|---:|---:|---:|---:|\n")
    for row in tabla:
        md_content.append(
            f"| {row['categoria']} | {row['fi']} | {row['hi']} | {row['Fi']} | {row['Hi']} |\n"
        )
    md_content.append(f"\n**Total de juegos:** {total}\n\n")


def generar_histograma_doble(
    valores_ea: pd.Series,
    valores_cd: pd.Series,
    bins: list[float],
    x_label: str,
    titulo_ea: str,
    titulo_cd: str,
    nombre_archivo: str,
):
    """Genera histogramas lado a lado para Early Access y Completo Directo."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].hist(valores_ea, bins=bins, color="skyblue", edgecolor="black", alpha=0.75)
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel("Frecuencia Absoluta")
    axes[0].set_title(titulo_ea)
    axes[0].yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    axes[1].hist(valores_cd, bins=bins, color="coral", edgecolor="black", alpha=0.75)
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel("Frecuencia Absoluta")
    axes[1].set_title(titulo_cd)
    axes[1].yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_barras_dobles_desde_tablas(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    titulo: str,
    nombre_archivo: str,
):
    """Genera gráfico de barras comparativo EA vs CD usando mismas categorías/intervalos."""
    etiquetas = [row["categoria"] for row in tabla_ea]
    fi_ea = [row["fi"] for row in tabla_ea]
    fi_cd = [row["fi"] for row in tabla_cd]

    pos = list(range(len(etiquetas)))
    ancho = 0.4

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar([p - ancho / 2 for p in pos], fi_ea, width=ancho, color="skyblue", edgecolor="black", label="Early Access")
    ax.bar([p + ancho / 2 for p in pos], fi_cd, width=ancho, color="coral", edgecolor="black", label="Completo Directo")

    ax.set_xticks(pos)
    ax.set_xticklabels(etiquetas, rotation=35, ha="right")
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frecuencia Absoluta")
    ax.set_title(titulo)
    ax.legend()
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_dot_plot_doble_desde_tablas(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    titulo_ea: str,
    titulo_cd: str,
    nombre_archivo: str,
):
    """Genera dos dot plots (EA y CD) en la misma imagen."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 5), sharey=True)

    for ax, tabla, titulo in [
        (axes[0], tabla_ea, titulo_ea),
        (axes[1], tabla_cd, titulo_cd),
    ]:
        categorias = [row["categoria"] for row in tabla]
        frecuencias = [row["fi"] for row in tabla]

        xs = []
        ys = []
        for idx, fi in enumerate(frecuencias):
            for nivel in range(1, fi + 1):
                xs.append(idx)
                ys.append(nivel)

        if xs:
            ax.scatter(xs, ys, s=90, color="#1F77B4")

        ax.set_xticks(list(range(len(categorias))))
        ax.set_xticklabels(categorias, rotation=30, ha="right")
        ax.set_xlabel(x_label)
        ax.set_ylabel("")
        ax.set_title(titulo)
        ax.set_yticks([])
        ax.set_ylim(bottom=0)
        ax.grid(False)
        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_linewidth(1.2)

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def main():
    data = pd.read_json(BASE_DIR / "data.json")

    early_access = data[data["estado_lanzamiento"] == "Early Access"]
    completo_directo = data[data["estado_lanzamiento"] == "Completo Directo"]

    md_content = []
    md_content.append("# Frecuencias\n\n")
    md_content.append(
        "## Organización y presentación de los datos: construcción de distribuciones de frecuencias\n\n"
    )

    # ---------- Precio base ----------
    md_content.append("## Precio Base (USD)\n\n")
    bins_precio = [0, 10, 20, 30, 40, 50, 60]

    precio_ea = early_access["precio_base_usd"]
    precio_cd = completo_directo["precio_base_usd"]

    tabla_precio_ea, n_precio_ea = generar_tabla_frecuencias_intervalos(precio_ea, bins_precio)
    tabla_precio_cd, n_precio_cd = generar_tabla_frecuencias_intervalos(precio_cd, bins_precio)

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_precio_ea, n_precio_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_precio_cd, n_precio_cd)

    generar_histograma_doble(
        valores_ea=precio_ea,
        valores_cd=precio_cd,
        bins=bins_precio,
        x_label="Precio base (USD$)",
        titulo_ea="Early Access - Distribución de Precios",
        titulo_cd="Completo Directo - Distribución de Precios",
        nombre_archivo="frecuencias_precio.png",
    )
    md_content.append("## Visualización - Precio Base\n\n")
    md_content.append("![Histograma de precio base](../images/frecuencias_precio.png)\n\n")

    # ---------- Porcentaje de reseñas positivas ----------
    md_content.append("## Porcentaje de Reseñas Positivas\n\n")
    resenas_ea = early_access["porcentaje_resenas_positivas"]
    resenas_cd = completo_directo["porcentaje_resenas_positivas"]
    resenas_total = pd.concat([resenas_ea, resenas_cd], ignore_index=True)
    bins_resenas = construir_bins_paso(resenas_total, paso=5, minimo=0, maximo=100)

    tabla_resenas_ea, n_resenas_ea = generar_tabla_frecuencias_intervalos(resenas_ea, bins_resenas)
    tabla_resenas_cd, n_resenas_cd = generar_tabla_frecuencias_intervalos(resenas_cd, bins_resenas)

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_resenas_ea, n_resenas_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_resenas_cd, n_resenas_cd)

    generar_histograma_doble(
        valores_ea=resenas_ea,
        valores_cd=resenas_cd,
        bins=bins_resenas,
        x_label="Porcentaje de reseñas positivas (%)",
        titulo_ea="Early Access - Reseñas Positivas",
        titulo_cd="Completo Directo - Reseñas Positivas",
        nombre_archivo="frecuencias_resenas.png",
    )
    md_content.append("## Visualización - Reseñas Positivas\n\n")
    md_content.append("![Histograma de porcentaje de reseñas positivas](../images/frecuencias_resenas.png)\n\n")

    # ---------- Categorías de reseñas ----------
    md_content.append("## Categorías de Reseñas\n\n")
    orden_resenas = [
        "No User Reviews",
        "Overwhelmingly Negative",
        "Very Negative",
        "Negative",
        "Mostly Negative",
        "Mixed",
        "Mostly Positive",
        "Positive",
        "Very Positive",
        "Overwhelmingly Positive",
    ]

    tabla_cat_resenas_ea, n_cat_resenas_ea = generar_tabla_frecuencias_categorias(
        early_access["categoria_resenas"], orden=orden_resenas
    )
    tabla_cat_resenas_cd, n_cat_resenas_cd = generar_tabla_frecuencias_categorias(
        completo_directo["categoria_resenas"], orden=orden_resenas
    )

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_cat_resenas_ea, n_cat_resenas_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_cat_resenas_cd, n_cat_resenas_cd)

    generar_dot_plot_doble_desde_tablas(
        tabla_ea=tabla_cat_resenas_ea,
        tabla_cd=tabla_cat_resenas_cd,
        x_label="Categoría de reseñas",
        titulo_ea="Early Access - Dot Plot categorías de reseñas",
        titulo_cd="Completo Directo - Dot Plot categorías de reseñas",
        nombre_archivo="frecuencias_categoria_resenas_dotplot.png",
    )
    md_content.append("## Visualización - Categorías de Reseñas\n\n")
    md_content.append("![Dot plot de categorías de reseñas](../images/frecuencias_categoria_resenas_dotplot.png)\n\n")

    # ---------- Pico histórico de concurrentes ----------
    md_content.append("## Pico Histórico de Jugadores Concurrentes\n\n")
    pico_total = pd.concat(
        [
            early_access["pico_historico_concurrentes"],
            completo_directo["pico_historico_concurrentes"],
        ],
        ignore_index=True,
    )
    bins_pico = construir_bins_optimos_sturges(pico_total)

    tabla_pico_ea, n_pico_ea = generar_tabla_frecuencias_intervalos(
        early_access["pico_historico_concurrentes"], bins_pico
    )
    tabla_pico_cd, n_pico_cd = generar_tabla_frecuencias_intervalos(
        completo_directo["pico_historico_concurrentes"], bins_pico
    )

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_pico_ea, n_pico_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_pico_cd, n_pico_cd)

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_pico_ea,
        tabla_cd=tabla_pico_cd,
        x_label="Intervalos de jugadores concurrentes",
        titulo="Frecuencias - Pico histórico de concurrentes",
        nombre_archivo="frecuencias_pico_historico_barras.png",
    )
    md_content.append("## Visualización - Pico Histórico de Concurrentes\n\n")
    md_content.append("![Barras de pico histórico de concurrentes](../images/frecuencias_pico_historico_barras.png)\n\n")

    # ---------- Jugadores promedio ----------
    md_content.append("## Jugadores Promedio\n\n")
    jug_total = pd.concat(
        [
            early_access["jugadores_promedio"],
            completo_directo["jugadores_promedio"],
        ],
        ignore_index=True,
    )
    bins_jug = construir_bins_optimos_sturges(jug_total)

    tabla_jug_ea, n_jug_ea = generar_tabla_frecuencias_intervalos(
        early_access["jugadores_promedio"], bins_jug
    )
    tabla_jug_cd, n_jug_cd = generar_tabla_frecuencias_intervalos(
        completo_directo["jugadores_promedio"], bins_jug
    )

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_jug_ea, n_jug_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_jug_cd, n_jug_cd)

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        titulo="Frecuencias - Jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_barras.png",
    )
    md_content.append("## Visualización - Jugadores Promedio\n\n")
    md_content.append("![Barras de jugadores promedio](../images/frecuencias_jugadores_promedio_barras.png)\n\n")

    # ---------- Soporte multiplataforma ----------
    md_content.append("## Soporte Multiplataforma\n\n")
    soporte_ea = early_access["soporte_multiplataforma"].explode()
    soporte_cd = completo_directo["soporte_multiplataforma"].explode()
    orden_plataformas = sorted(pd.concat([soporte_ea, soporte_cd]).dropna().astype(str).unique().tolist())

    tabla_plat_ea, n_plat_ea = generar_tabla_frecuencias_categorias(soporte_ea, orden=orden_plataformas)
    tabla_plat_cd, n_plat_cd = generar_tabla_frecuencias_categorias(soporte_cd, orden=orden_plataformas)

    agregar_tabla_markdown(md_content, "Juegos en Early Access (ocurrencias)", tabla_plat_ea, n_plat_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo (ocurrencias)", tabla_plat_cd, n_plat_cd)

    generar_dot_plot_doble_desde_tablas(
        tabla_ea=tabla_plat_ea,
        tabla_cd=tabla_plat_cd,
        x_label="Plataforma",
        titulo_ea="Early Access - Dot Plot soporte multiplataforma",
        titulo_cd="Completo Directo - Dot Plot soporte multiplataforma",
        nombre_archivo="frecuencias_soporte_plataforma_dotplot.png",
    )
    md_content.append("## Visualización - Soporte Multiplataforma\n\n")
    md_content.append("![Dot plot de soporte multiplataforma](../images/frecuencias_soporte_plataforma_dotplot.png)\n\n")

    # ---------- Género principal ----------
    md_content.append("## Género Principal\n\n")
    orden_generos = sorted(data["genero_principal"].dropna().astype(str).unique().tolist())

    tabla_genero_ea, n_genero_ea = generar_tabla_frecuencias_categorias(
        early_access["genero_principal"], orden=orden_generos
    )
    tabla_genero_cd, n_genero_cd = generar_tabla_frecuencias_categorias(
        completo_directo["genero_principal"], orden=orden_generos
    )

    agregar_tabla_markdown(md_content, "Juegos en Early Access", tabla_genero_ea, n_genero_ea)
    agregar_tabla_markdown(md_content, "Juegos en Completo Directo", tabla_genero_cd, n_genero_cd)

    generar_dot_plot_doble_desde_tablas(
        tabla_ea=tabla_genero_ea,
        tabla_cd=tabla_genero_cd,
        x_label="Género",
        titulo_ea="Early Access - Dot Plot género principal",
        titulo_cd="Completo Directo - Dot Plot género principal",
        nombre_archivo="frecuencias_genero_principal_dotplot.png",
    )
    md_content.append("## Visualización - Género Principal\n\n")
    md_content.append("![Dot plot de género principal](../images/frecuencias_genero_principal_dotplot.png)\n\n")

    reporte_path = REPORTES_DIR / "frecuencias.md"
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("".join(md_content))

    print("Archivo frecuencias.md generado correctamente")
    print(f"Reporte guardado en: {reporte_path}")


if __name__ == "__main__":
    main()

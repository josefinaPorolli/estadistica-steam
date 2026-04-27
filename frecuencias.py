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
REPORTES_VARIABLES_DIR = REPORTES_DIR / "variables"

IMAGES_DIR.mkdir(exist_ok=True)
REPORTES_DIR.mkdir(exist_ok=True)
REPORTES_VARIABLES_DIR.mkdir(exist_ok=True)

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
    # La regla de Sturges sugiere k = 1 + 3.322 * log10(n) intervalos, donde n es el número de datos.
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


def guardar_reporte_variable(nombre_archivo: str, titulo_variable: str, contenido_frecuencias: list[str]):
    """Guarda un reporte Markdown por variable con la sección del ítem frecuencias."""
    md = []
    md.append(f"# {titulo_variable}\n\n")
    md.append("## Frecuencias\n\n")
    md.extend(contenido_frecuencias)

    reporte_path = REPORTES_VARIABLES_DIR / f"{nombre_archivo}.md"
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    return reporte_path


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


def generar_barras_separadas_desde_tablas(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    nombre_archivo: str,
):
    """Genera dos gráficos de barras separados (EA y CD) en la misma imagen."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    for ax, tabla, titulo, color in [
        (axes[0], tabla_ea, "Early Access", "skyblue"),
        (axes[1], tabla_cd, "Completo Directo", "coral"),
    ]:
        categorias = [row["categoria"] for row in tabla]
        frecuencias = [row["fi"] for row in tabla]
        
        x_pos = list(range(len(categorias)))
        ax.bar(x_pos, frecuencias, width=0.7, color=color, edgecolor="black", alpha=0.8)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categorias, rotation=45, ha="right")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Frecuencia Absoluta")
        ax.set_title(f"{titulo} - Gráfico de Barras")
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_ojivas_separadas_desde_tablas(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    nombre_archivo: str,
):
    """Genera dos gráficos de ojiva separados (EA y CD) en la misma imagen."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    for ax, tabla, titulo, color in [
        (axes[0], tabla_ea, "Early Access", "skyblue"),
        (axes[1], tabla_cd, "Completo Directo", "coral"),
    ]:
        categorias = [row["categoria"] for row in tabla]
        frecuencias_acum = [row["Fi"] for row in tabla]
        
        x_pos = list(range(len(categorias)))
        ax.plot(x_pos, frecuencias_acum, color=color, marker="o", linewidth=2.5, markersize=8, label="Ojiva")
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categorias, rotation=45, ha="right")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Frecuencia Acumulada")
        ax.set_title(f"{titulo} - Gráfico de Ojiva")
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_ojivas_comparativas(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    nombre_archivo: str,
):
    """Genera gráfico de ojivas comparativas (EA vs CD) lado a lado."""
    fig, ax = plt.subplots(figsize=(13, 5))

    etiquetas = [row["categoria"] for row in tabla_ea]
    Fi_ea = [row["Fi"] for row in tabla_ea]
    Fi_cd = [row["Fi"] for row in tabla_cd]
    
    x_pos = list(range(len(etiquetas)))
    ancho = 0.35

    # Ojivas lado a lado
    ax.plot([p - ancho / 2 for p in x_pos], Fi_ea, color="skyblue", marker="o", linewidth=2.5, 
            markersize=7, label="Early Access", alpha=0.9)
    ax.plot([p + ancho / 2 for p in x_pos], Fi_cd, color="coral", marker="^", linewidth=2.5, 
            markersize=7, label="Completo Directo", alpha=0.9)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(etiquetas, rotation=45, ha="right")
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frecuencia Acumulada")
    ax.set_title("Gráfico de Ojivas Comparativas")
    ax.legend()
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_poligono_frecuencias_separado(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    nombre_archivo: str,
):
    """Genera dos polígonos de frecuencia separados (EA y CD) en la misma imagen."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    for ax, tabla, titulo, color in [
        (axes[0], tabla_ea, "Early Access", "skyblue"),
        (axes[1], tabla_cd, "Completo Directo", "coral"),
    ]:
        categorias = [row["categoria"] for row in tabla]
        frecuencias = [row["fi"] for row in tabla]
        
        x_pos = list(range(len(categorias)))
        ax.plot(x_pos, frecuencias, color=color, marker="o", linewidth=2.5, markersize=8)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categorias, rotation=45, ha="right")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Frecuencia Absoluta")
        ax.set_title(f"{titulo} - Polígono de Frecuencias")
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_poligono_frecuencias_comparativo(
    tabla_ea: list[dict],
    tabla_cd: list[dict],
    x_label: str,
    nombre_archivo: str,
):
    """Genera polígono de frecuencias comparativo (EA vs CD) en el mismo gráfico."""
    fig, ax = plt.subplots(figsize=(13, 5))

    etiquetas = [row["categoria"] for row in tabla_ea]
    fi_ea = [row["fi"] for row in tabla_ea]
    fi_cd = [row["fi"] for row in tabla_cd]
    
    x_pos = list(range(len(etiquetas)))
    
    ax.plot(x_pos, fi_ea, color="skyblue", marker="o", linewidth=2.5, markersize=8, label="Early Access")
    ax.plot(x_pos, fi_cd, color="coral", marker="^", linewidth=2.5, markersize=8, label="Completo Directo")
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(etiquetas, rotation=45, ha="right")
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frecuencia Absoluta")
    ax.set_title("Polígono de Frecuencias Comparativo")
    ax.legend()
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def agregar_referencias_iqr(
    ax,
    q1: float,
    q3: float,
    color: str,
):
    """Dibuja las cuatro referencias de IQR en un boxplot horizontal."""
    iqr = q3 - q1
    posiciones = [q1 - 3 * iqr, q1 - 1.5 * iqr, q3 + 1.5 * iqr, q3 + 3 * iqr]
    estilos = ["dashdot", "dashed", "dashed", "dashdot"]
    for index, (pos, estilo) in enumerate(zip(posiciones, estilos), start=1):
        ax.axvline(pos, color=color, linestyle=estilo, linewidth=1.3, alpha=0.7)
        ax.text(
            pos,
            0.91,
            f"Ref {index}",
            transform=ax.get_xaxis_transform(),
            color=color,
            fontsize=9,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.75, edgecolor=color, linewidth=0.8),
            clip_on=False,
        )


def generar_boxplot_horizontal(
    valores_ea: pd.Series,
    valores_cd: pd.Series,
    datos_ea: pd.DataFrame,
    datos_cd: pd.DataFrame,
    x_label: str,
    nombre_archivo: str,
):
    """Genera boxplot horizontal (uno arriba del otro) para EA y CD con estadísticas."""
    def calcular_estadisticas(valores, datos):
        """Calcula estadísticas para los valores."""
        q1 = valores.quantile(0.25)
        q3 = valores.quantile(0.75)
        mediana = valores.quantile(0.50)
        media = valores.mean()
        iqr = q3 - q1
        
        # Límites de whiskers
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        # Outliers y anómalos
        outliers = valores[(valores < limite_inferior) | (valores > limite_superior)]
        
        # Mapear outliers a nombres de juegos
        outlier_info = []
        for val in outliers:
            idx = valores[valores == val].index
            if len(idx) > 0:
                nombre_juego = datos.loc[idx[0], "nombre"]
                outlier_info.append((val, nombre_juego))
        
        return {
            "Q1": q1,
            "Q3": q3,
            "Mediana": mediana,
            "Media": media,
            "IQR": iqr,
            "Ref1": q1 - 3 * iqr,
            "Ref2": q1 - 1.5 * iqr,
            "Ref3": q3 + 1.5 * iqr,
            "Ref4": q3 + 3 * iqr,
            "Outliers": outlier_info,
        }

    def formatear_bloque_estadisticas(titulo: str, stats: dict) -> str:
        lineas = [
            f"{titulo}",
            f"- Cuartil 1 (Q1): {stats['Q1']:.2f}",
            f"- Mediana: {stats['Mediana']:.2f}",
            f"- Cuartil 3 (Q3): {stats['Q3']:.2f}",
            f"- Media: {stats['Media']:.2f}",
            f"- Ref 1 (Q1 - 3·IQR): {stats['Ref1']:.2f}",
            f"- Ref 2 (Q1 - 1.5·IQR): {stats['Ref2']:.2f}",
            f"- Ref 3 (Q3 + 1.5·IQR): {stats['Ref3']:.2f}",
            f"- Ref 4 (Q3 + 3·IQR): {stats['Ref4']:.2f}",
        ]

        if stats["Outliers"]:
            lineas.append("- Valores atípicos / anómalos:")
            for valor, juego in stats["Outliers"]:
                lineas.append(f"  - {valor:.2f} - {juego}")
        else:
            lineas.append("- Valores atípicos / anómalos: Ninguno")

        return "\n".join(lineas)
    
    stats_ea = calcular_estadisticas(valores_ea, datos_ea)
    stats_cd = calcular_estadisticas(valores_cd, datos_cd)
    
    fig = plt.figure(figsize=(14, 10))
    
    # Crear grid para boxplots + estadísticas
    gs = fig.add_gridspec(4, 1, height_ratios=[1, 0.8, 1, 0.8])
    
    # Early Access boxplot
    ax0 = fig.add_subplot(gs[0])
    ax0.boxplot(valores_ea, vert=False, widths=0.5, patch_artist=True,
                boxprops=dict(facecolor="skyblue", alpha=0.7),
                medianprops=dict(color="darkblue", linewidth=2),
                whiskerprops=dict(color="skyblue", linewidth=1.5),
                capprops=dict(color="skyblue", linewidth=1.5),
                flierprops=dict(marker="o", markerfacecolor="skyblue", markersize=6, alpha=0.5))
    agregar_referencias_iqr(ax0, stats_ea["Q1"], stats_ea["Q3"], "darkblue")
    ax0.scatter(stats_ea["Media"], 1, marker="x", s=120, color="darkblue", linewidths=2.5, zorder=5)
    ax0.set_title("Early Access - Boxplot Horizontal", fontweight="bold")
    ax0.set_xlabel(x_label)
    ax0.grid(True, alpha=0.3, axis="x")
    
    # Early Access estadísticas
    ax1 = fig.add_subplot(gs[1])
    ax1.axis("off")
    
    stats_text_ea = formatear_bloque_estadisticas("Resumen estadístico", stats_ea)
    
    ax1.text(0.05, 0.95, stats_text_ea, transform=ax1.transAxes, 
             fontsize=10, verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.3))
    
    # Completo Directo boxplot
    ax2 = fig.add_subplot(gs[2])
    ax2.boxplot(valores_cd, vert=False, widths=0.5, patch_artist=True,
                boxprops=dict(facecolor="coral", alpha=0.7),
                medianprops=dict(color="darkred", linewidth=2),
                whiskerprops=dict(color="coral", linewidth=1.5),
                capprops=dict(color="coral", linewidth=1.5),
                flierprops=dict(marker="o", markerfacecolor="coral", markersize=6, alpha=0.5))
    agregar_referencias_iqr(ax2, stats_cd["Q1"], stats_cd["Q3"], "darkred")
    ax2.scatter(stats_cd["Media"], 1, marker="x", s=120, color="darkred", linewidths=2.5, zorder=5)
    ax2.set_title("Completo Directo - Boxplot Horizontal", fontweight="bold")
    ax2.set_xlabel(x_label)
    ax2.grid(True, alpha=0.3, axis="x")
    
    # Completo Directo estadísticas
    ax3 = fig.add_subplot(gs[3])
    ax3.axis("off")
    
    stats_text_cd = formatear_bloque_estadisticas("Resumen estadístico", stats_cd)
    
    ax3.text(0.05, 0.95, stats_text_cd, transform=ax3.transAxes, 
             fontsize=10, verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="lightsalmon", alpha=0.3))
    
    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def generar_boxplot_horizontal_comparativo(
    valores_ea: pd.Series,
    valores_cd: pd.Series,
    datos_ea: pd.DataFrame,
    datos_cd: pd.DataFrame,
    x_label: str,
    nombre_archivo: str,
):
    """Genera un boxplot horizontal comparativo en una única escala."""

    def calcular_media_y_outliers(valores, datos):
        q1 = valores.quantile(0.25)
        q3 = valores.quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        outliers = valores[(valores < limite_inferior) | (valores > limite_superior)]

        outlier_info = []
        for val in outliers:
            idx = valores[valores == val].index
            if len(idx) > 0:
                outlier_info.append((val, datos.loc[idx[0], "nombre"]))

        return float(valores.mean()), outlier_info

    media_ea, outliers_ea = calcular_media_y_outliers(valores_ea, datos_ea)
    media_cd, outliers_cd = calcular_media_y_outliers(valores_cd, datos_cd)

    fig, ax = plt.subplots(figsize=(14, 5))
    bp = ax.boxplot(
        [valores_ea, valores_cd],
        vert=False,
        positions=[2, 1],
        widths=0.5,
        patch_artist=True,
        tick_labels=["Early Access", "Completo Directo"],
        medianprops=dict(color="black", linewidth=2),
        whiskerprops=dict(linewidth=1.5),
        capprops=dict(linewidth=1.5),
        flierprops=dict(marker="o", markersize=6, alpha=0.5),
    )

    colores = [("skyblue", "darkblue"), ("coral", "darkred")]
    for box, (fill_color, _) in zip(bp["boxes"], colores):
        box.set_facecolor(fill_color)
        box.set_alpha(0.7)

    for median, (_, line_color) in zip(bp["medians"], colores):
        median.set_color(line_color)

    for whisker, (_, line_color) in zip(bp["whiskers"], colores * 2):
        whisker.set_color(line_color)

    for cap, (_, line_color) in zip(bp["caps"], colores * 2):
        cap.set_color(line_color)

    ax.scatter(media_ea, 2, marker="x", s=120, color="darkblue", linewidths=2.5, zorder=5)
    ax.scatter(media_cd, 1, marker="x", s=120, color="darkred", linewidths=2.5, zorder=5)

    min_val = min(float(valores_ea.min()), float(valores_cd.min()))
    max_val = max(float(valores_ea.max()), float(valores_cd.max()))
    margen = (max_val - min_val) * 0.08 if max_val > min_val else 1
    ax.set_xlim(min_val - margen, max_val + margen)

    ax.set_title("Boxplot Comparativo - Misma Escala", fontweight="bold")
    ax.set_xlabel(x_label)
    ax.set_yticks([1, 2])
    ax.set_yticklabels(["Completo Directo", "Early Access"])
    ax.grid(True, alpha=0.3, axis="x")

    if outliers_ea or outliers_cd:
        leyenda = []
        if outliers_ea:
            leyenda.append(f"EA atípicos: {len(outliers_ea)}")
        if outliers_cd:
            leyenda.append(f"CD atípicos: {len(outliers_cd)}")
        ax.text(
            0.02,
            1.03,
            " | ".join(leyenda),
            transform=ax.transAxes,
            fontsize=9,
            va="bottom",
            ha="left",
        )

    plt.tight_layout()
    output_path = IMAGES_DIR / nombre_archivo
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def main():
    data = pd.read_json(BASE_DIR / "data.json")

    early_access = data[data["estado_lanzamiento"] == "Early Access"]
    completo_directo = data[data["estado_lanzamiento"] == "Completo Directo"]

    reportes_generados = []

    # ---------- Precio base ----------
    contenido_precio = []
    bins_precio = [0, 10, 20, 30, 40, 50, 60]

    precio_ea = early_access["precio_base_usd"]
    precio_cd = completo_directo["precio_base_usd"]

    tabla_precio_ea, n_precio_ea = generar_tabla_frecuencias_intervalos(precio_ea, bins_precio)
    tabla_precio_cd, n_precio_cd = generar_tabla_frecuencias_intervalos(precio_cd, bins_precio)

    agregar_tabla_markdown(contenido_precio, "Juegos en Early Access", tabla_precio_ea, n_precio_ea)
    agregar_tabla_markdown(contenido_precio, "Juegos en Completo Directo", tabla_precio_cd, n_precio_cd)

    generar_histograma_doble(
        valores_ea=precio_ea,
        valores_cd=precio_cd,
        bins=bins_precio,
        x_label="Precio base (USD$)",
        titulo_ea="Early Access - Distribución de Precios",
        titulo_cd="Completo Directo - Distribución de Precios",
        nombre_archivo="frecuencias_precio_histograma.png",
    )
    contenido_precio.append("### Visualización - Histograma\n\n")
    contenido_precio.append("![Histograma de precio base](../../images/frecuencias_precio_histograma.png)\n\n")

    generar_poligono_frecuencias_separado(
        tabla_ea=tabla_precio_ea,
        tabla_cd=tabla_precio_cd,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_poligono.png",
    )
    contenido_precio.append("### Visualización - Polígono de Frecuencias\n\n")
    contenido_precio.append("![Polígono de precio base](../../images/frecuencias_precio_poligono.png)\n\n")

    generar_poligono_frecuencias_comparativo(
        tabla_ea=tabla_precio_ea,
        tabla_cd=tabla_precio_cd,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_poligono_comparativo.png",
    )
    contenido_precio.append("### Visualización - Polígono Junto\n\n")
    contenido_precio.append(
        "![Polígono comparativo de precio base](../../images/frecuencias_precio_poligono_comparativo.png)\n\n"
    )

    generar_ojivas_separadas_desde_tablas(
        tabla_ea=tabla_precio_ea,
        tabla_cd=tabla_precio_cd,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_ojiva.png",
    )
    contenido_precio.append("### Visualización - Ojiva\n\n")
    contenido_precio.append("![Ojiva de precio base](../../images/frecuencias_precio_ojiva.png)\n\n")

    generar_ojivas_comparativas(
        tabla_ea=tabla_precio_ea,
        tabla_cd=tabla_precio_cd,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_ojiva_comparativa.png",
    )
    contenido_precio.append("### Visualización - Ojiva Junto\n\n")
    contenido_precio.append(
        "![Ojiva comparativa de precio base](../../images/frecuencias_precio_ojiva_comparativa.png)\n\n"
    )

    generar_boxplot_horizontal(
        valores_ea=precio_ea,
        valores_cd=precio_cd,
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_boxplot_horizontal.png",
    )
    contenido_precio.append("### Visualización - Boxplot Horizontal\n\n")
    contenido_precio.append(
        "![Boxplot horizontal de precio base](../../images/frecuencias_precio_boxplot_horizontal.png)\n\n"
    )

    generar_boxplot_horizontal_comparativo(
        valores_ea=precio_ea,
        valores_cd=precio_cd,
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Precio base (USD$)",
        nombre_archivo="frecuencias_precio_boxplot_comparativo.png",
    )
    contenido_precio.append("### Visualización - Boxplot Comparativo\n\n")
    contenido_precio.append(
        "![Boxplot comparativo de precio base](../../images/frecuencias_precio_boxplot_comparativo.png)\n\n"
    )

    reportes_generados.append(
        guardar_reporte_variable("precio_base_usd", "Precio Base (USD)", contenido_precio)
    )

    # ---------- Porcentaje de reseñas positivas ----------
    contenido_resenas = []
    resenas_ea = early_access["porcentaje_resenas_positivas"]
    resenas_cd = completo_directo["porcentaje_resenas_positivas"]
    resenas_total = pd.concat([resenas_ea, resenas_cd], ignore_index=True)
    bins_resenas = construir_bins_paso(resenas_total, paso=5, minimo=0, maximo=100)

    tabla_resenas_ea, n_resenas_ea = generar_tabla_frecuencias_intervalos(resenas_ea, bins_resenas)
    tabla_resenas_cd, n_resenas_cd = generar_tabla_frecuencias_intervalos(resenas_cd, bins_resenas)

    agregar_tabla_markdown(contenido_resenas, "Juegos en Early Access", tabla_resenas_ea, n_resenas_ea)
    agregar_tabla_markdown(contenido_resenas, "Juegos en Completo Directo", tabla_resenas_cd, n_resenas_cd)

    generar_histograma_doble(
        valores_ea=resenas_ea,
        valores_cd=resenas_cd,
        bins=bins_resenas,
        x_label="Porcentaje de reseñas positivas (%)",
        titulo_ea="Early Access - Reseñas Positivas",
        titulo_cd="Completo Directo - Reseñas Positivas",
        nombre_archivo="frecuencias_resenas_histograma.png",
    )
    contenido_resenas.append("### Visualización - Histograma\n\n")
    contenido_resenas.append(
        "![Histograma de porcentaje de reseñas positivas](../../images/frecuencias_resenas_histograma.png)\n\n"
    )

    generar_poligono_frecuencias_separado(
        tabla_ea=tabla_resenas_ea,
        tabla_cd=tabla_resenas_cd,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_poligono.png",
    )
    contenido_resenas.append("### Visualización - Polígono de Frecuencias\n\n")
    contenido_resenas.append(
        "![Polígono de porcentaje de reseñas positivas](../../images/frecuencias_resenas_poligono.png)\n\n"
    )

    generar_poligono_frecuencias_comparativo(
        tabla_ea=tabla_resenas_ea,
        tabla_cd=tabla_resenas_cd,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_poligono_comparativo.png",
    )
    contenido_resenas.append("### Visualización - Polígono Junto\n\n")
    contenido_resenas.append(
        "![Polígono comparativo de porcentaje de reseñas positivas](../../images/frecuencias_resenas_poligono_comparativo.png)\n\n"
    )

    generar_ojivas_separadas_desde_tablas(
        tabla_ea=tabla_resenas_ea,
        tabla_cd=tabla_resenas_cd,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_ojiva.png",
    )
    contenido_resenas.append("### Visualización - Ojiva\n\n")
    contenido_resenas.append(
        "![Ojiva de porcentaje de reseñas positivas](../../images/frecuencias_resenas_ojiva.png)\n\n"
    )

    generar_ojivas_comparativas(
        tabla_ea=tabla_resenas_ea,
        tabla_cd=tabla_resenas_cd,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_ojiva_comparativa.png",
    )
    contenido_resenas.append("### Visualización - Ojiva Junto\n\n")
    contenido_resenas.append(
        "![Ojiva comparativa de porcentaje de reseñas positivas](../../images/frecuencias_resenas_ojiva_comparativa.png)\n\n"
    )

    generar_boxplot_horizontal(
        valores_ea=resenas_ea,
        valores_cd=resenas_cd,
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_boxplot_horizontal.png",
    )
    contenido_resenas.append("### Visualización - Boxplot Horizontal\n\n")
    contenido_resenas.append(
        "![Boxplot horizontal de porcentaje de reseñas positivas](../../images/frecuencias_resenas_boxplot_horizontal.png)\n\n"
    )

    generar_boxplot_horizontal_comparativo(
        valores_ea=resenas_ea,
        valores_cd=resenas_cd,
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Porcentaje de reseñas positivas (%)",
        nombre_archivo="frecuencias_resenas_boxplot_comparativo.png",
    )
    contenido_resenas.append("### Visualización - Boxplot Comparativo\n\n")
    contenido_resenas.append(
        "![Boxplot comparativo de porcentaje de reseñas positivas](../../images/frecuencias_resenas_boxplot_comparativo.png)\n\n"
    )

    reportes_generados.append(
        guardar_reporte_variable(
            "porcentaje_resenas_positivas",
            "Porcentaje de Reseñas Positivas",
            contenido_resenas,
        )
    )

    # ---------- Categorías de reseñas ----------
    contenido_cat_resenas = []
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

    agregar_tabla_markdown(contenido_cat_resenas, "Juegos en Early Access", tabla_cat_resenas_ea, n_cat_resenas_ea)
    agregar_tabla_markdown(contenido_cat_resenas, "Juegos en Completo Directo", tabla_cat_resenas_cd, n_cat_resenas_cd)

    # Barras
    generar_barras_separadas_desde_tablas(
        tabla_ea=tabla_cat_resenas_ea,
        tabla_cd=tabla_cat_resenas_cd,
        x_label="Categoría de reseñas",
        nombre_archivo="frecuencias_categoria_resenas_barras_separadas.png",
    )
    contenido_cat_resenas.append("### Visualización - Gráficos de Barras\n\n")
    contenido_cat_resenas.append(
        "![Barras separadas de categorías de reseñas](../../images/frecuencias_categoria_resenas_barras_separadas.png)\n\n"
    )

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_cat_resenas_ea,
        tabla_cd=tabla_cat_resenas_cd,
        x_label="Categoría de reseñas",
        titulo="Categorías de Reseñas - Gráfico de Barras Comparativo",
        nombre_archivo="frecuencias_categoria_resenas_barras_comparativas.png",
    )
    contenido_cat_resenas.append("![Barras comparativas de categorías de reseñas](../../images/frecuencias_categoria_resenas_barras_comparativas.png)\n\n")

    # Ojivas
    generar_ojivas_separadas_desde_tablas(
        tabla_ea=tabla_cat_resenas_ea,
        tabla_cd=tabla_cat_resenas_cd,
        x_label="Categoría de reseñas",
        nombre_archivo="frecuencias_categoria_resenas_ojivas_separadas.png",
    )
    contenido_cat_resenas.append("### Visualización - Gráficos de Ojiva\n\n")
    contenido_cat_resenas.append(
        "![Ojivas separadas de categorías de reseñas](../../images/frecuencias_categoria_resenas_ojivas_separadas.png)\n\n"
    )

    generar_ojivas_comparativas(
        tabla_ea=tabla_cat_resenas_ea,
        tabla_cd=tabla_cat_resenas_cd,
        x_label="Categoría de reseñas",
        nombre_archivo="frecuencias_categoria_resenas_ojivas_comparativas.png",
    )
    contenido_cat_resenas.append("![Ojivas comparativas de categorías de reseñas](../../images/frecuencias_categoria_resenas_ojivas_comparativas.png)\n\n")

    reportes_generados.append(
        guardar_reporte_variable("categoria_resenas", "Categorías de Reseñas", contenido_cat_resenas)
    )

    # ---------- Pico histórico de concurrentes ----------
    contenido_pico = []
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

    agregar_tabla_markdown(contenido_pico, "Juegos en Early Access", tabla_pico_ea, n_pico_ea)
    agregar_tabla_markdown(contenido_pico, "Juegos en Completo Directo", tabla_pico_cd, n_pico_cd)

    generar_histograma_doble(
        valores_ea=early_access["pico_historico_concurrentes"],
        valores_cd=completo_directo["pico_historico_concurrentes"],
        bins=bins_pico,
        x_label="Intervalos de jugadores concurrentes",
        titulo_ea="Early Access - Pico Histórico de Concurrentes",
        titulo_cd="Completo Directo - Pico Histórico de Concurrentes",
        nombre_archivo="frecuencias_pico_historico_histograma.png",
    )
    contenido_pico.append("### Visualización - Histograma\n\n")
    contenido_pico.append(
        "![Histograma de pico histórico de concurrentes](../../images/frecuencias_pico_historico_histograma.png)\n\n"
    )

    generar_poligono_frecuencias_separado(
        tabla_ea=tabla_pico_ea,
        tabla_cd=tabla_pico_cd,
        x_label="Intervalos de jugadores concurrentes",
        nombre_archivo="frecuencias_pico_historico_poligono.png",
    )
    contenido_pico.append("### Visualización - Polígono de Frecuencias\n\n")
    contenido_pico.append(
        "![Polígono de pico histórico de concurrentes](../../images/frecuencias_pico_historico_poligono.png)\n\n"
    )

    generar_poligono_frecuencias_comparativo(
        tabla_ea=tabla_pico_ea,
        tabla_cd=tabla_pico_cd,
        x_label="Intervalos de jugadores concurrentes",
        nombre_archivo="frecuencias_pico_historico_poligono_comparativo.png",
    )
    contenido_pico.append("### Visualización - Polígono Junto\n\n")
    contenido_pico.append(
        "![Polígono junto de pico histórico de concurrentes](../../images/frecuencias_pico_historico_poligono_comparativo.png)\n\n"
    )

    generar_ojivas_separadas_desde_tablas(
        tabla_ea=tabla_pico_ea,
        tabla_cd=tabla_pico_cd,
        x_label="Intervalos de jugadores concurrentes",
        nombre_archivo="frecuencias_pico_historico_ojiva.png",
    )
    contenido_pico.append("### Visualización - Ojiva\n\n")
    contenido_pico.append(
        "![Ojiva de pico histórico de concurrentes](../../images/frecuencias_pico_historico_ojiva.png)\n\n"
    )

    generar_ojivas_comparativas(
        tabla_ea=tabla_pico_ea,
        tabla_cd=tabla_pico_cd,
        x_label="Intervalos de jugadores concurrentes",
        nombre_archivo="frecuencias_pico_historico_ojiva_comparativa.png",
    )
    contenido_pico.append("### Visualización - Ojiva Junto\n\n")
    contenido_pico.append(
        "![Ojiva junto de pico histórico de concurrentes](../../images/frecuencias_pico_historico_ojiva_comparativa.png)\n\n"
    )

    generar_boxplot_horizontal(
        valores_ea=early_access["pico_historico_concurrentes"],
        valores_cd=completo_directo["pico_historico_concurrentes"],
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Pico Histórico de Concurrentes",
        nombre_archivo="frecuencias_pico_historico_boxplot_horizontal.png",
    )
    contenido_pico.append("### Visualización - Boxplot Horizontal\n\n")
    contenido_pico.append(
        "![Boxplot horizontal de pico histórico de concurrentes](../../images/frecuencias_pico_historico_boxplot_horizontal.png)\n\n"
    )

    generar_boxplot_horizontal_comparativo(
        valores_ea=early_access["pico_historico_concurrentes"],
        valores_cd=completo_directo["pico_historico_concurrentes"],
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Pico Histórico de Concurrentes",
        nombre_archivo="frecuencias_pico_historico_boxplot_comparativo.png",
    )
    contenido_pico.append("### Visualización - Boxplot Comparativo\n\n")
    contenido_pico.append(
        "![Boxplot comparativo de pico histórico de concurrentes](../../images/frecuencias_pico_historico_boxplot_comparativo.png)\n\n"
    )

    reportes_generados.append(
        guardar_reporte_variable(
            "pico_historico_concurrentes",
            "Pico Histórico de Jugadores Concurrentes",
            contenido_pico,
        )
    )

    # ---------- Jugadores promedio ----------
    contenido_jugadores = []
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

    agregar_tabla_markdown(contenido_jugadores, "Juegos en Early Access", tabla_jug_ea, n_jug_ea)
    agregar_tabla_markdown(contenido_jugadores, "Juegos en Completo Directo", tabla_jug_cd, n_jug_cd)

    # Barras
    generar_barras_separadas_desde_tablas(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_barras_separadas.png",
    )
    contenido_jugadores.append("### Visualización - Gráficos de Barras\n\n")
    contenido_jugadores.append("![Barras separadas de jugadores promedio](../../images/frecuencias_jugadores_promedio_barras_separadas.png)\n\n")

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        titulo="Jugadores Promedio - Gráfico de Barras Comparativo",
        nombre_archivo="frecuencias_jugadores_promedio_barras_comparativas.png",
    )
    contenido_jugadores.append("![Barras comparativas de jugadores promedio](../../images/frecuencias_jugadores_promedio_barras_comparativas.png)\n\n")

    # Polígono de Frecuencias
    generar_poligono_frecuencias_separado(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_poligono_separado.png",
    )
    contenido_jugadores.append("### Visualización - Polígono de Frecuencias\n\n")
    contenido_jugadores.append("![Polígono separado de jugadores promedio](../../images/frecuencias_jugadores_promedio_poligono_separado.png)\n\n")

    generar_poligono_frecuencias_comparativo(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_poligono_comparativo.png",
    )
    contenido_jugadores.append("![Polígono comparativo de jugadores promedio](../../images/frecuencias_jugadores_promedio_poligono_comparativo.png)\n\n")

    # Ojivas
    generar_ojivas_separadas_desde_tablas(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_ojivas_separadas.png",
    )
    contenido_jugadores.append("### Visualización - Gráficos de Ojiva\n\n")
    contenido_jugadores.append("![Ojivas separadas de jugadores promedio](../../images/frecuencias_jugadores_promedio_ojivas_separadas.png)\n\n")

    generar_ojivas_comparativas(
        tabla_ea=tabla_jug_ea,
        tabla_cd=tabla_jug_cd,
        x_label="Intervalos de jugadores promedio",
        nombre_archivo="frecuencias_jugadores_promedio_ojivas_comparativas.png",
    )
    contenido_jugadores.append("![Ojivas comparativas de jugadores promedio](../../images/frecuencias_jugadores_promedio_ojivas_comparativas.png)\n\n")

    # Boxplot Horizontal
    generar_boxplot_horizontal(
        valores_ea=early_access["jugadores_promedio"],
        valores_cd=completo_directo["jugadores_promedio"],
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Jugadores Promedio",
        nombre_archivo="frecuencias_jugadores_promedio_boxplot_horizontal.png",
    )
    contenido_jugadores.append("### Visualización - Boxplot Horizontal\n\n")
    contenido_jugadores.append("![Boxplot horizontal de jugadores promedio](../../images/frecuencias_jugadores_promedio_boxplot_horizontal.png)\n\n")

    generar_boxplot_horizontal_comparativo(
        valores_ea=early_access["jugadores_promedio"],
        valores_cd=completo_directo["jugadores_promedio"],
        datos_ea=early_access,
        datos_cd=completo_directo,
        x_label="Jugadores Promedio",
        nombre_archivo="frecuencias_jugadores_promedio_boxplot_comparativo.png",
    )
    contenido_jugadores.append("### Visualización - Boxplot Comparativo\n\n")
    contenido_jugadores.append("![Boxplot comparativo de jugadores promedio](../../images/frecuencias_jugadores_promedio_boxplot_comparativo.png)\n\n")

    reportes_generados.append(
        guardar_reporte_variable("jugadores_promedio", "Jugadores Promedio", contenido_jugadores)
    )

    # ---------- Soporte multiplataforma ----------
    contenido_soporte = []
    soporte_ea = early_access["soporte_multiplataforma"].explode()
    soporte_cd = completo_directo["soporte_multiplataforma"].explode()
    orden_plataformas = sorted(pd.concat([soporte_ea, soporte_cd]).dropna().astype(str).unique().tolist())

    tabla_plat_ea, n_plat_ea = generar_tabla_frecuencias_categorias(soporte_ea, orden=orden_plataformas)
    tabla_plat_cd, n_plat_cd = generar_tabla_frecuencias_categorias(soporte_cd, orden=orden_plataformas)

    agregar_tabla_markdown(contenido_soporte, "Juegos en Early Access (ocurrencias)", tabla_plat_ea, n_plat_ea)
    agregar_tabla_markdown(contenido_soporte, "Juegos en Completo Directo (ocurrencias)", tabla_plat_cd, n_plat_cd)

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_plat_ea,
        tabla_cd=tabla_plat_cd,
        x_label="Plataforma",
        titulo="Soporte Multiplataforma - Gráfico de Barras Comparativo",
        nombre_archivo="frecuencias_soporte_multiplataforma_barras_comparativas.png",
    )
    contenido_soporte.append("### Visualización\n\n")
    contenido_soporte.append(
        "![Barras comparativas de soporte multiplataforma](../../images/frecuencias_soporte_multiplataforma_barras_comparativas.png)\n\n"
    )
    reportes_generados.append(
        guardar_reporte_variable("soporte_multiplataforma", "Soporte Multiplataforma", contenido_soporte)
    )

    # ---------- Género principal ----------
    contenido_genero = []
    orden_generos = sorted(data["genero_principal"].dropna().astype(str).unique().tolist())

    tabla_genero_ea, n_genero_ea = generar_tabla_frecuencias_categorias(
        early_access["genero_principal"], orden=orden_generos
    )
    tabla_genero_cd, n_genero_cd = generar_tabla_frecuencias_categorias(
        completo_directo["genero_principal"], orden=orden_generos
    )

    agregar_tabla_markdown(contenido_genero, "Juegos en Early Access", tabla_genero_ea, n_genero_ea)
    agregar_tabla_markdown(contenido_genero, "Juegos en Completo Directo", tabla_genero_cd, n_genero_cd)

    generar_barras_dobles_desde_tablas(
        tabla_ea=tabla_genero_ea,
        tabla_cd=tabla_genero_cd,
        x_label="Género",
        titulo="Género Principal - Gráfico de Barras Comparativo",
        nombre_archivo="frecuencias_genero_principal_barras_comparativas.png",
    )
    contenido_genero.append("### Visualización\n\n")
    contenido_genero.append("![Barras comparativas de género principal](../../images/frecuencias_genero_principal_barras_comparativas.png)\n\n")
    reportes_generados.append(
        guardar_reporte_variable("genero_principal", "Género Principal", contenido_genero)
    )

    index_lines = ["# Reportes por Variable\n\n"]
    index_lines.append("Estos reportes contienen el ítem de frecuencias por variable.\n\n")
    for path in reportes_generados:
        index_lines.append(f"- [{path.stem}](variables/{path.name})\n")

    index_path = REPORTES_DIR / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("".join(index_lines))

    legacy_path = REPORTES_DIR / "frecuencias.md"
    if legacy_path.exists():
        legacy_path.unlink()

    print("Reportes de frecuencias por variable generados correctamente")
    print(f"Índice guardado en: {index_path}")


if __name__ == "__main__":
    main()

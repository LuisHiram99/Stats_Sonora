import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon

def plot_sonora_map(data: pd.DataFrame, title:str):
    """
    Plotea un mapa de Sonora con los datos proporcionados.

    Args:
        data (pd.DataFrame): DataFrame con dos columnas: la primera con los nombres de los municipios y la segunda con los valores a graficar.
        title (str): Título del gráfico.
    
    """
    data_copy = data.copy()
    municipio_col, valor_col = data_copy.columns[0], data_copy.columns[1]
    
    mun = gpd.read_file(
    "/Users/luishernandez/Desktop/StatsSonora/mapas/shapefile_sonora/inegi_refcenmuni_2010.shp",
    engine="fiona",       # 👈 forzamos Fiona en lugar de pyogrio
    encoding="latin-1"    # 👈 INEGI casi siempre está en latin-1
)
    mun_sonora = mun[mun['nom_ent'] == 'Sonora']

    pob_mun_mapa = mun_sonora.merge(data_copy, left_on="nom_mun", right_on=municipio_col, how="left")
    fig, ax = plt.subplots(figsize=(10, 10))

    pob_mun_mapa.plot(
        column=valor_col,       # Columna con datos
        cmap="OrRd",           # Escala de colores (rojo = más población)
        legend=True,           # Mostrar leyenda
        edgecolor="black",     # Bordes de los municipios
        linewidth=0.5,
        ax=ax
    )

    ax.set_title(title, fontsize=16)
    ax.axis("off")  # Quita ejes para que quede más limpio

    plt.show()
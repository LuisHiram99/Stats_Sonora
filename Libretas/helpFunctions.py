import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.patheffects as path_effects

def plot_sonora_map(data: pd.DataFrame, title: str, graph_value=False, height=10, weight=10):
    """
    Plotea un mapa de Sonora con los datos proporcionados.

    Args:
        data (pd.DataFrame): DataFrame con dos columnas: la primera con los nombres de los municipios y la segunda con los valores a graficar.
        title (str): Título del gráfico.
        graph_value (bool): Si es True, muestra el valor sobre cada municipio.
    """
    data_copy = data.copy()
    municipio_col, valor_col = data_copy.columns[0], data_copy.columns[1]
    
    # Leer shapefile
    mun = gpd.read_file(
        "/Users/luishernandez/Desktop/Stats_Sonora/mapas/shapefile_sonora/inegi_refcenmuni_2010.shp",
        engine="fiona",
        encoding="latin-1"
    )
    mun_sonora = mun[mun['nom_ent'] == 'Sonora']

    # Unir datos con shapefile
    pob_mun_mapa = mun_sonora.merge(data_copy, left_on="nom_mun", right_on=municipio_col, how="left")

    # Calcular centroides para ubicar texto
    pob_mun_mapa["centroid"] = pob_mun_mapa.geometry.centroid

    # Crear figura
    fig, ax = plt.subplots(figsize=(height, weight))

    # Graficar mapa
    pob_mun_mapa.plot(
        column=valor_col,
        cmap="OrRd",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        ax=ax
    )

    # Si se pide, mostrar valores
    if graph_value:
        for _, row in pob_mun_mapa.iterrows():
            if pd.notnull(row[valor_col]):
                x, y = row["centroid"].x, row["centroid"].y
                ax.text(
                    x, y,
                    f"{row[valor_col]:,.0f}",
                    ha="center", va="center",
                    fontsize=7,
                    color="black",
                    path_effects=[
                        path_effects.withStroke(linewidth=1, foreground="white")
                    ]
                )

    ax.set_title(title, fontsize=16)
    ax.axis("off")

    plt.show()
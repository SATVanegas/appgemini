import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


def cargar_datos():
    """Carga datos desde la URL fija del archivo de deforestación.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados e interpolados.
    """
    url = (
        "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/"
        "refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    )
    df = pd.read_csv(url)
    return df.interpolate(method="linear")


def mostrar_estadisticas(df):
    """Muestra estadísticas generales del dataset."""
    st.write("### Estadísticas Generales")
    st.write(df.describe())


def mostrar_mapa_deforestacion(df):
    """Genera un mapa con las zonas de deforestación usando imágenes satelitales.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'Latitud', 'Longitud', 'Superficie_Deforestada'.
    """
    st.write("### Mapa de Zonas Deforestadas")

    # Filtros en la barra lateral
    st.sidebar.write("### Filtros para el Mapa")
    latitud_range = st.sidebar.slider(
        "Rango de Latitud",
        min_value=float(df["Latitud"].min()),
        max_value=float(df["Latitud"].max()),
        value=(float(df["Latitud"].min()), float(df["Latitud"].max())),
    )
    longitud_range = st.sidebar.slider(
        "Rango de Longitud",
        min_value=float(df["Longitud"].min()),
        max_value=float(df["Longitud"].max()),
        value=(float(df["Longitud"].min()), float(df["Longitud"].max())),
    )
    superficie_range = st.sidebar.slider(
        "Rango de Superficie Deforestada",
        min_value=float(df["Superficie_Deforestada"].min()),
        max_value=float(df["Superficie_Deforestada"].max()),
        value=(float(df["Superficie_Deforestada"].min()), float(df["Superficie_Deforestada"].max())),
    )

    # Aplicar filtros
    filtered_df = df[
        (df["Latitud"] >= latitud_range[0])
        & (df["Latitud"] <= latitud_range[1])
        & (df["Longitud"] >= longitud_range[0])
        & (df["Longitud"] <= longitud_range[1])
        & (df["Superficie_Deforestada"] >= superficie_range[0])
        & (df["Superficie_Deforestada"] <= superficie_range[1])
    ]

    # Crear el mapa
    route = (
        "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    )
    world = gpd.read_file(route)
    filtered_df["geometry"] = filtered_df.apply(
        lambda row: Point(row["Longitud"], row["Latitud"]), axis=1
    )
    gdf = gpd.GeoDataFrame(filtered_df, geometry="geometry")
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgray")
    gdf.plot(
        ax=ax, column="Superficie_Deforestada", legend=True, cmap="Reds", markersize=5
    )
    st.pyplot(fig)


def clusterizar_deforestacion(df):
    """Realiza un análisis de clúster sobre las superficies deforestadas.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'Latitud', 'Longitud', 'Superficie_Deforestada'.
    """
    st.write("### Análisis de Clúster de Deforestación")
    bins = np.histogram_bin_edges(df["Superficie_Deforestada"], bins=3)
    df["cluster"] = np.digitize(df["Superficie_Deforestada"], bins=bins)
    fig, ax = plt.subplots()
    scatter = ax.scatter(df["Longitud"], df["Latitud"], c=df["cluster"], cmap="viridis")
    plt.colorbar(scatter, label="Cluster")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_title("Clúster de Deforestación")
    st.pyplot(fig)


def grafico_torta_vegetacion(df):
    """Genera un gráfico de torta según el tipo de vegetación.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Tipo_Vegetacion'.
    """
    st.write("### Distribución por Tipo de Vegetación")
    tipo_veg = df["Tipo_Vegetacion"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(tipo_veg, labels=tipo_veg.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribución por Tipo de Vegetación")
    st.pyplot(fig)


def main():
    """Función principal para ejecutar la aplicación de análisis de deforestación."""
    st.title("Análisis de Deforestación")
    st.sidebar.title("Opciones")

    # Cargar datos
    df = cargar_datos()

    if df is not None:
        # Menú de opciones en la barra lateral
        opcion = st.sidebar.radio(
            "Selecciona una opción:",
            [
                "Estadísticas Generales",
                "Mapa de Deforestación",
                "Análisis de Clúster",
                "Gráfico de Vegetación",
            ],
        )

        if opcion == "Estadísticas Generales":
            mostrar_estadisticas(df)
        elif opcion == "Mapa de Deforestación":
            mostrar_mapa_deforestacion(df)
        elif opcion == "Análisis de Clúster":
            clusterizar_deforestacion(df)
        elif opcion == "Gráfico de Vegetación":
            grafico_torta_vegetacion(df)


if __name__ == "__main__":
    main()

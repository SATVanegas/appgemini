import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


def cargar_datos():
    """Carga datos desde la URL fija del archivo de análisis de enfermedades.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    url = (
        "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/"
        "refs/heads/main/archivos-datos/aplicaciones/analisis_enfermedades.csv"
    )
    df = pd.read_csv(url)
    return df


def mostrar_estadisticas(df):
    """Muestra estadísticas generales de las variables numéricas."""
    st.write("### Estadísticas Generales de Variables Numéricas")
    st.write(df.describe())


def mostrar_estadisticas_filtradas(df):
    """Muestra estadísticas de variables numéricas filtradas por categorías seleccionadas."""
    st.write("### Estadísticas Filtradas por Categorías")

    # Selección de variables categóricas
    categoricas = df.select_dtypes(include=["object"]).columns
    categoria_seleccionada = st.selectbox("Selecciona una categoría para filtrar:", categoricas)

    # Selección de valores de la categoría
    valores_categoria = df[categoria_seleccionada].unique()
    valor_seleccionado = st.selectbox(f"Selecciona un valor de {categoria_seleccionada}:", valores_categoria)

    # Filtrar el DataFrame
    df_filtrado = df[df[categoria_seleccionada] == valor_seleccionado]
    st.write(f"Estadísticas para {categoria_seleccionada} = {valor_seleccionado}:")
    st.write(df_filtrado.describe())


def mostrar_mapa_calor(df):
    """Genera un mapa de calor de todas las enfermedades."""
    st.write("### Mapa de Calor de Todas las Enfermedades")

    # Convertir a GeoDataFrame
    df["geometry"] = df.apply(lambda row: Point(row["Longitud"], row["Latitud"]), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry="geometry")

    # Cargar mapa mundial
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Crear el mapa
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgray")
    gdf.plot(ax=ax, markersize=df["Incidencia"] * 0.1, color="red", alpha=0.5)
    plt.title("Mapa de Calor de Incidencia de Enfermedades")
    st.pyplot(fig)


def mostrar_mapa_calor_por_enfermedad(df):
    """Genera un mapa de calor para una enfermedad específica seleccionada por el usuario."""
    st.write("### Mapa de Calor por Enfermedad")

    # Selección de enfermedad
    enfermedades = df["Enfermedad"].unique()
    enfermedad_seleccionada = st.selectbox("Selecciona una enfermedad:", enfermedades)

    # Filtrar por enfermedad
    df_filtrado = df[df["Enfermedad"] == enfermedad_seleccionada]

    # Convertir a GeoDataFrame
    df_filtrado["geometry"] = df_filtrado.apply(lambda row: Point(row["Longitud"], row["Latitud"]), axis=1)
    gdf = gpd.GeoDataFrame(df_filtrado, geometry="geometry")

    # Cargar mapa mundial
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Crear el mapa
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgray")
    gdf.plot(ax=ax, markersize=df_filtrado["Incidencia"] * 0.1, color="red", alpha=0.5)
    plt.title(f"Mapa de Calor de {enfermedad_seleccionada}")
    st.pyplot(fig)


def mostrar_series_temporales(df):
    """Genera un gráfico de series temporales de todas las enfermedades."""
    st.write("### Series Temporales de Todas las Enfermedades")

    # Agrupar por fecha y enfermedad
    df_agrupado = df.groupby(["Fecha", "Enfermedad"]).sum().reset_index()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    for enfermedad in df_agrupado["Enfermedad"].unique():
        df_enfermedad = df_agrupado[df_agrupado["Enfermedad"] == enfermedad]
        ax.plot(df_enfermedad["Fecha"], df_enfermedad["Incidencia"], label=enfermedad)
    plt.legend()
    plt.title("Series Temporales de Incidencia de Enfermedades")
    plt.xlabel("Fecha")
    plt.ylabel("Incidencia")
    st.pyplot(fig)


def mostrar_serie_temporal_por_region(df):
    """Genera un gráfico de serie temporal para una enfermedad y región seleccionadas."""
    st.write("### Serie Temporal por Enfermedad y Región")

    # Selección de enfermedad
    enfermedades = df["Enfermedad"].unique()
    enfermedad_seleccionada = st.selectbox("Selecciona una enfermedad:", enfermedades, key="enfermedad_serie")

    # Selección de región
    regiones = df["Region"].unique()
    region_seleccionada = st.selectbox("Selecciona una región:", regiones, key="region_serie")

    # Filtrar por enfermedad y región
    df_filtrado = df[(df["Enfermedad"] == enfermedad_seleccionada) & (df["Region"] == region_seleccionada)]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_filtrado["Fecha"], df_filtrado["Incidencia"])
    plt.title(f"Serie Temporal de {enfermedad_seleccionada} en {region_seleccionada}")
    plt.xlabel("Fecha")
    plt.ylabel("Incidencia")
    st.pyplot(fig)


def mostrar_tasas_hospitalizacion(df):
    """Genera un gráfico de barras de tasas de hospitalización por enfermedad y región."""
    st.write("### Tasas de Hospitalización por Enfermedad y Región")

    # Agrupar por enfermedad y región
    df_agrupado = df.groupby(["Enfermedad", "Region"])["Tasa_Hospitalizacion"].mean().reset_index()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    for region in df_agrupado["Region"].unique():
        df_region = df_agrupado[df_agrupado["Region"] == region]
        ax.bar(df_region["Enfermedad"], df_region["Tasa_Hospitalizacion"], label=region)
    plt.legend()
    plt.title("Tasas de Hospitalización por Enfermedad y Región")
    plt.xlabel("Enfermedad")
    plt.ylabel("Tasa de Hospitalización")
    st.pyplot(fig)


def main():
    """Función principal para ejecutar la aplicación de análisis de enfermedades."""
    st.title("Análisis de Distribución de Enfermedades")
    st.sidebar.title("Opciones")

    # Cargar datos
    df = cargar_datos()

    if df is not None:
        # Menú de opciones en la barra lateral
        opcion = st.sidebar.radio(
            "Selecciona una opción:",
            [
                "Estadísticas Generales",
                "Estadísticas Filtradas",
                "Mapa de Calor (Todas las Enfermedades)",
                "Mapa de Calor (Por Enfermedad)",
                "Series Temporales (Todas las Enfermedades)",
                "Serie Temporal (Por Enfermedad y Región)",
                "Tasas de Hospitalización",
            ],
        )

        if opcion == "Estadísticas Generales":
            mostrar_estadisticas(df)
        elif opcion == "Estadísticas Filtradas":
            mostrar_estadisticas_filtradas(df)
        elif opcion == "Mapa de Calor (Todas las Enfermedades)":
            mostrar_mapa_calor(df)
        elif opcion == "Mapa de Calor (Por Enfermedad)":
            mostrar_mapa_calor_por_enfermedad(df)
        elif opcion == "Series Temporales (Todas las Enfermedades)":
            mostrar_series_temporales(df)
        elif opcion == "Serie Temporal (Por Enfermedad y Región)":
            mostrar_serie_temporal_por_region(df)
        elif opcion == "Tasas de Hospitalización":
            mostrar_tasas_hospitalizacion(df)


if __name__ == "__main__":
    main()

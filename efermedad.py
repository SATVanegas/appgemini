import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


def cargar_datos(archivo=None, url=None):
    """Carga datos desde un archivo o una URL.

    Args:
        archivo (str, optional): Ruta del archivo CSV. Defaults to None.
        url (str, optional): URL del archivo CSV. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados e interpolados.
    """
    if archivo is not None:
        df = pd.read_csv(archivo)
    elif url is not None:
        df = pd.read_csv(url)
    else:
        st.error("Debes proporcionar un archivo o una URL.")
        return None

    # Interpolación lineal para rellenar valores faltantes
    df = df.interpolate(method="linear")
    return df


def mostrar_estadisticas(df):
    """Muestra estadísticas generales de las variables numéricas.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
    """
    st.write("### Estadísticas Generales de Variables Numéricas")
    st.write(df.describe())


def mostrar_mapa_calor(df):
    """Genera un mapa de calor de todas las enfermedades.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'Latitud', 'Longitud', 'Casos_reportados'.
    """
    st.write("### Mapa de Calor de Todas las Enfermedades")

    # Convertir a GeoDataFrame
    df["geometry"] = df.apply(lambda row: Point(row["Longitud"], row["Latitud"]), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry="geometry")

    # Descargar el mapa mundial desde una URL
    world_url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(world_url)

    # Crear el mapa
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgray")
    gdf.plot(ax=ax, markersize=df["Casos_reportados"] * 0.1, color="red", alpha=0.5)
    plt.title("Mapa de Calor de Incidencia de Enfermedades")
    st.pyplot(fig)


def mostrar_series_temporales(df):
    """Genera un gráfico de series temporales de todas las enfermedades.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'Fecha' y 'Casos_reportados'.
    """
    st.write("### Series Temporales de Todas las Enfermedades")

    # Agrupar por fecha y enfermedad
    df_agrupado = df.groupby(["Fecha", "Enfermedad"]).sum(numeric_only=True).reset_index()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    for enfermedad in df_agrupado["Enfermedad"].unique():
        df_enfermedad = df_agrupado[df_agrupado["Enfermedad"] == enfermedad]
        ax.plot(df_enfermedad["Fecha"], df_enfermedad["Casos_reportados"], label=enfermedad)
    plt.legend()
    plt.title("Series Temporales de Incidencia de Enfermedades")
    plt.xlabel("Fecha")
    plt.ylabel("Casos Reportados")
    st.pyplot(fig)


def mostrar_tasas_hospitalizacion(df):
    """Genera un gráfico de barras de tasas de hospitalización por enfermedad y región.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'Enfermedad', 'Region', 'Hospitalizaciones'.
    """
    st.write("### Tasas de Hospitalización por Enfermedad y Región")

    # Agrupar por enfermedad y región
    df_agrupado = df.groupby(["Enfermedad", "Region"])["Hospitalizaciones"].mean().reset_index()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    for region in df_agrupado["Region"].unique():
        df_region = df_agrupado[df_agrupado["Region"] == region]
        ax.bar(df_region["Enfermedad"], df_region["Hospitalizaciones"], label=region)
    plt.legend()
    plt.title("Tasas de Hospitalización por Enfermedad y Región")
    plt.xlabel("Enfermedad")
    plt.ylabel("Hospitalizaciones")
    st.pyplot(fig)


def main():
    """Función principal para ejecutar la aplicación de análisis de enfermedades."""
    st.title("Análisis de Distribución de Enfermedades")
    st.sidebar.title("Opciones")

    # Cargar datos
    st.sidebar.write("### Cargar Datos")
    opcion_carga = st.sidebar.radio(
        "Selecciona una opción para cargar los datos:",
        ["Subir archivo CSV", "Ingresar URL"],
    )

    if opcion_carga == "Subir archivo CSV":
        archivo = st.sidebar.file_uploader("Sube un archivo CSV", type=["csv"])
        df = cargar_datos(archivo=archivo) if archivo is not None else None
    else:
        url = st.sidebar.text_input("Ingresa la URL del archivo CSV")
        df = cargar_datos(url=url) if url else None

    if df is not None:
        # Menú de opciones en la barra lateral
        opcion = st.sidebar.radio(
            "Selecciona una opción:",
            [
                "Estadísticas Generales",
                "Mapa de Calor",
                "Series Temporales",
                "Tasas de Hospitalización",
            ],
        )

        if opcion == "Estadísticas Generales":
            mostrar_estadisticas(df)
        elif opcion == "Mapa de Calor":
            mostrar_mapa_calor(df)
        elif opcion == "Series Temporales":
            mostrar_series_temporales(df)
        elif opcion == "Tasas de Hospitalización":
            mostrar_tasas_hospitalizacion(df)


if __name__ == "__main__":
    main()

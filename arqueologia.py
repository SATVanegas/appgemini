import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Configuración de la app
st.set_page_config(page_title="Mi primera app", layout="wide")

# Título y autor
st.title("Mi primera app")
st.write("Esta app fue elaborada por **SANTIAGO VANEGAS**.")

# Cargar los datos desde el enlace proporcionado
url = (
    "https://raw.githubusercontent.com/gabrielawad/"
    "programacion-para-ingenieria/refs/heads/main/"
    "archivos-datos/aplicaciones/datos_arqueologicos.csv"
)
df = pd.read_csv(url)

# Interpolación de columnas numéricas
df["Edad_Aprox_Anios"] = df["Edad_Aprox_Anios"].interpolate(
    method="linear", limit_direction="both"
)
df["Profundidad_Excavación_m"] = df["Profundidad_Excavación_m"].interpolate(
    method="linear", limit_direction="both"
)

# Interpolación de columnas categóricas (rellenar con la moda)
df["Nombre_Artefacto"] = df["Nombre_Artefacto"].fillna(
    df["Nombre_Artefacto"].mode().iloc[0]
)
df["Ubicación_Descubrimiento"] = df["Ubicación_Descubrimiento"].fillna(
    df["Ubicación_Descubrimiento"].mode().iloc[0]
)
df["Investigador_Principal"] = df["Investigador_Principal"].fillna(
    df["Investigador_Principal"].mode().iloc[0]
)

# Interpolación de fechas
df["Fecha_Descubrimiento"] = pd.to_datetime(
    df["Fecha_Descubrimiento"], errors="coerce"
)
df["Fecha_Descubrimiento"] = df["Fecha_Descubrimiento"].fillna(method="ffill")

# Mostrar valores nulos después de la interpolación
st.write("### Valores nulos después de la interpolación:")
st.dataframe(df.isnull().sum())

# Cargar el mapa mundial desde Natural Earth
naturalearth_lowres = (
    "https://naciscdn.org/naturalearth/110m/cultural/"
    "ne_110m_admin_0_countries.zip"
)
mapa_mundial = gpd.read_file(naturalearth_lowres)

# Filtrar artefactos tallados con coordenadas válidas
artefactos_tallados = df[df["Técnica_Fabricación"] == "tallado"].dropna(
    subset=["Latitud", "Longitud"]
)

# Crear un GeoDataFrame con coordenadas geográficas
gdf_tallados = gpd.GeoDataFrame(
    artefactos_tallados,
    geometry=gpd.points_from_xy(
        artefactos_tallados["Longitud"], artefactos_tallados["Latitud"]
    ),
    crs="EPSG:4326",
)

# Definir la cuadrícula para la interpolación
x, y = gdf_tallados.geometry.x, gdf_tallados.geometry.y

# Verificar que hay suficientes puntos
if len(x) >= 4:
    grid_x, grid_y = np.meshgrid(
        np.linspace(x.min(), x.max(), 100),
        np.linspace(y.min(), y.max(), 100),
    )

    # Interpolar la densidad de artefactos
    grid_z = griddata((x, y), np.ones_like(x), (grid_x, grid_y), method="cubic")
    grid_z = np.nan_to_num(grid_z)  # Reemplazar NaN con 0

    # Crear la figura
    fig, ax = plt.subplots(figsize=(12, 8))

    # Dibujar el mapa mundial
    mapa_mundial.boundary.plot(ax=ax, linewidth=0.8, color="black")

    # Dibujar el mapa de calor
    contour = ax.contourf(grid_x, grid_y, grid_z, cmap="YlGnBu", alpha=0.7)

    # Dibujar los puntos de los artefactos
    ax.scatter(x, y, color="red", s=10, label="Artefactos Tallados")

    # Agregar la barra de color
    cbar = plt.colorbar(contour, ax=ax, orientation="vertical")
    cbar.set_label("Densidad de Artefactos")

    # Etiquetas y título
    ax.set_title("Mapa de Calor: Densidad de Artefactos Tallados")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend()

    # Mostrar el mapa en Streamlit
    st.pyplot(fig)
else:
    st.warning("No hay suficientes puntos para la interpolación. Se requieren al menos 4.")

# Mostrar vista previa de los datos corregidos
st.write("### Vista previa de los datos corregidos:")
st.dataframe(df.head())

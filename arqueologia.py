import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
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

# 🔹 Gráfico de cantidad de artefactos por cultura
st.write("## Cantidad de Artefactos por Cultura")
conteo_culturas = df["Cultura_Asociada"].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
conteo_culturas.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)

ax.set_xlabel("Cultura")
ax.set_ylabel("Cantidad de Artefactos")
ax.set_title("Cantidad de Artefactos por Cultura")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

st.pyplot(fig)

# 🔹 Gráfico de dispersión: Relación entre Edad y Profundidad
st.write("## Relación entre Edad y Profundidad del Artefacto")

# Filtrar datos con valores válidos en "Edad_Aprox_Anios" y "Profundidad_Excavación_m"
datos_filtrados = df.dropna(subset=["Edad_Aprox_Anios", "Profundidad_Excavación_m"])

# Calcular la correlación de Pearson
if not datos_filtrados.empty:
    correlacion, p_valor = stats.pearsonr(
        datos_filtrados["Edad_Aprox_Anios"], datos_filtrados["Profundidad_Excavación_m"]
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        datos_filtrados["Edad_Aprox_Anios"],
        datos_filtrados["Profundidad_Excavación_m"],
        alpha=0.6,
        color="royalblue",
    )

    ax.set_xlabel("Edad Aproximada del Artefacto (años)")
    ax.set_ylabel("Profundidad del Hallazgo (metros)")
    ax.set_title(
        f"Relación entre Edad y Profundidad\nCorrelación de Pearson: {correlacion:.2f}"
    )

    st.pyplot(fig)

    # Mostrar valores de correlación
    st.write(f"**Correlación de Pearson:** {correlacion:.2f}")
    st.write(f"**P-valor:** {p_valor:.5f}")
else:
    st.warning("No hay suficientes datos válidos para calcular la correlación.")

# 🔹 Mapa de Calor de Artefactos Tallados
st.write("## Mapa de Calor: Densidad de Artefactos Tallados")

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

if len(x) >= 4:
    grid_x, grid_y = np.meshgrid(
        np.linspace(x.min(), x.max(), 100),
        np.linspace(y.min(), y.max(), 100),
    )

    # Interpolar la densidad de artefactos
    grid_z = griddata((x, y), np.ones_like(x), (grid_x, grid_y), method="cubic")
    grid_z = np.nan_to_num(grid_z)  # Reemplazar NaN con 0

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

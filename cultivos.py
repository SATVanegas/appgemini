import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

# URL del archivo CSV
url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/datos_cultivos_agricolas.csv"

# Cargar los datos en un DataFrame
df = pd.read_csv(url)

# Título de la aplicación
st.title("🌱 Análisis de Cultivos Agrícolas")

# Mostrar las primeras filas
st.subheader("📋 Datos originales")
st.dataframe(df.head())

# 🔹 Interpolar valores numéricos de manera lineal
df.interpolate(method="linear", inplace=True)

# 🔹 Rellenar valores categóricos con el valor más frecuente
for col in df.select_dtypes(include=["object"]).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# 🔹 Rellenar valores faltantes en fechas con el valor anterior
for col in df.select_dtypes(include=["datetime64"]).columns:
    df[col].fillna(method="ffill", inplace=True)

# 🔹 Verificar si quedan valores nulos
st.subheader("✅ Valores nulos restantes después de la limpieza:")
st.write(df.isnull().sum())

# 🔹 Filtrar cultivos de alta calidad
cultivos_alta_calidad = df[df["Calidad_Cosecha"] >= df["Calidad_Cosecha"].quantile(0.75)]

# 🔹 Extraer coordenadas
cultivos_alta_calidad[["Latitud", "Longitud"]] = cultivos_alta_calidad["Ubicación_Parcela"].str.split(", ", expand=True).astype(float)

# 🔹 Crear un GeoDataFrame
gdf_calidad = gpd.GeoDataFrame(
    cultivos_alta_calidad,
    geometry=gpd.points_from_xy(cultivos_alta_calidad["Longitud"], cultivos_alta_calidad["Latitud"]),
    crs="EPSG:4326"
)

# 🔹 Cargar el mapa mundial
naturalearth_lowres = (
    "https://naciscdn.org/naturalearth/110m/cultural/"
    "ne_110m_admin_0_countries.zip"
)
mapa_mundial = gpd.read_file(naturalearth_lowres)

# 🔹 Extraer coordenadas
x, y = gdf_calidad.geometry.x, gdf_calidad.geometry.y

# 🔹 Evitar errores si hay pocos puntos
if len(x) < 4:
    raise ValueError("No hay suficientes puntos de alta calidad para generar el mapa de calor.")

# 🔹 KDE para calcular densidad
xy = np.vstack([x, y])
kde = gaussian_kde(xy)
xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()
xi, yi = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
zi = kde(np.vstack([xi.flatten(), yi.flatten()]))

# 🔹 Crear la figura
fig, ax = plt.subplots(figsize=(12, 8))

# 🔹 Dibujar el mapa mundial
mapa_mundial.boundary.plot(ax=ax, linewidth=0.8, color="black")

# 🔹 Dibujar el mapa de calor con colores azul a rojo
ax.imshow(
    np.rot90(zi.reshape(xi.shape)),
    extent=[xmin, xmax, ymin, ymax],
    cmap="coolwarm",
    alpha=0.7
)

# 🔹 Dibujar los puntos de cultivos de alta calidad
ax.scatter(x, y, color="black", s=5, label="Cultivos Alta Calidad")

# 🔹 Agregar la barra de color
cbar = plt.colorbar(ax.collections[0], ax=ax, orientation="vertical")
cbar.set_label("Densidad de Cultivos de Alta Calidad")

# 🔹 Etiquetas y título
ax.set_title("🔥 Mapa de Calor de Cultivos de Alta Calidad")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.legend()

# Mostrar el gráfico con Streamlit
st.pyplot(fig)

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

# 🔹 Gráfico de barras apiladas: Distribución de Materiales según Cultura Asociada
st.write("## Distribución de Materiales según la Cultura Asociada")

# Filtrar datos sin valores nulos en "Cultura" y "Material"
datos_filtrados = df.dropna(subset=["Cultura_Asociada", "Material"])

# Contar la cantidad de artefactos por Cultura y Material
conteo_materiales = datos_filtrados.groupby(["Cultura_Asociada", "Material"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
conteo_materiales.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")

ax.set_xlabel("Cultura Asociada")
ax.set_ylabel("Cantidad de Artefactos")
ax.set_title("Distribución de Materiales según la Cultura Asociada")
ax.legend(title="Material", bbox_to_anchor=(1.05, 1), loc="upper left")

st.pyplot(fig)

# 🔹 Mapa de ubicación geográfica de los artefactos
st.write("## Ubicación Geográfica de los Artefactos")

# Cargar el mapa base del mundo
naturalearth_lowres = (
    "https://naciscdn.org/naturalearth/110m/"
    "cultural/ne_110m_admin_0_countries.zip"
)
gdf = gpd.read_file(naturalearth_lowres)

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(12, 8))

# Graficar el mapa base
gdf.plot(ax=ax, color="lightgray", edgecolor="black")

# Filtrar datos con coordenadas válidas
df_coordenadas = df.dropna(subset=["Latitud", "Longitud"])

if not df_coordenadas.empty:
    ax.scatter(
        df_coordenadas["Longitud"],
        df_coordenadas["Latitud"],
        c="red",
        marker="o",
        alpha=0.7,
        label="Artefactos",
    )

    ax.set_title("Ubicación Geográfica de los Artefactos")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
else:
    st.warning("No hay suficientes datos con coordenadas para graficar el mapa.")

# Mostrar vista previa de los datos corregidos
st.write("### Vista previa de los datos corregidos:")
st.dataframe(df.head())

import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("ruta/a/tu/archivo.csv")

# Asegurarse de que las columnas numéricas no contengan valores nulos
df["Calidad_Cosecha"] = pd.to_numeric(df["Calidad_Cosecha"], errors='coerce')
df = df.dropna(subset=["Calidad_Cosecha"])

# 🔹 Filtrar cultivos de alta calidad
cultivos_alta_calidad = df[df["Calidad_Cosecha"] >= df["Calidad_Cosecha"].quantile(0.75)]

# 🔹 Comprobar si hay suficientes cultivos de alta calidad
if len(cultivos_alta_calidad) < 4:
    st.error("No hay suficientes cultivos de alta calidad para generar el mapa de calor.")
else:
    # Extraer coordenadas
    cultivos_alta_calidad[["Latitud", "Longitud"]] = cultivos_alta_calidad["Ubicación_Parcela"].str.split(", ", expand=True).astype(float)

    # 🔹 Crear el GeoDataFrame
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

    # Evitar errores si hay pocos puntos
    if len(x) < 4:
        st.error("No hay suficientes puntos de alta calidad para generar el mapa de calor.")
    else:
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

        # 🔹 Mostrar el gráfico en Streamlit
        st.pyplot(fig)

# 🔹 Visualización de la correlación entre variables
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x='Humedad_Suelo', y='Rendimiento_Cosecha', scatter_kws={'alpha': 0.5})
plt.title("📊 Correlación entre Humedad del Suelo y Rendimiento de Cosecha")
plt.xlabel("Humedad del Suelo (%)")
plt.ylabel("Rendimiento de Cosecha (kg/ha)")
plt.grid(True)
st.pyplot()

plt.figure(figsize=(8, 5))
sns.histplot(df['Temperatura_Aire'], bins=20, kde=True, color="royalblue")
plt.title("🌡️ Distribución de la Temperatura del Aire")
plt.xlabel("Temperatura del Aire (°C)")
plt.ylabel("Frecuencia")
plt.grid(True)
st.pyplot()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Método_Cultivo', y='Rendimiento_Cosecha', palette="Set2")
plt.title("📈 Comparación del Rendimiento por Método de Cultivo")
plt.xlabel("Método de Cultivo")
plt.ylabel("Rendimiento de Cosecha (kg/ha)")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot()

# 🔹 Gráfico de Precipitación vs Rendimiento
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Precipitación_Total', y='Rendimiento_Cosecha', alpha=0.6)
sns.regplot(data=df, x='Precipitación_Total', y='Rendimiento_Cosecha', scatter=False, color="red")
plt.title("🌧️ Relación entre Precipitación y Rendimiento de Cosecha")
plt.xlabel("Precipitación Total (mm)")
plt.ylabel("Rendimiento de Cosecha (kg/ha)")
plt.grid(True)
st.pyplot()

# 🔹 Frecuencia de Enfermedades
plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='Enfermedades_Presentes', order=df['Enfermedades_Presentes'].value_counts().index, palette="Reds_r")
plt.title("🦠 Frecuencia de Enfermedades en los Cultivos")
plt.xlabel("Cantidad de Cultivos Afectados")
plt.ylabel("Tipo de Enfermedad")
plt.grid(axis="x", linestyle="--", alpha=0.6)
st.pyplot()

# 🔹 Comparación de Calidad de Cosecha por Variedad de Semilla
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Variedad_Semilla", y="Calidad_Cosecha", palette="muted")
plt.title("🌾 Comparación de Calidad de Cosecha por Variedad de Semilla")
plt.xlabel("Variedad de Semilla")
plt.ylabel("Calidad de la Cosecha")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot()

# 🔹 Distribución de los Días de Cultivo
df["Fecha_Siembra"] = pd.to_datetime(df["Fecha_Siembra"])
df["Fecha_Cosecha"] = pd.to_datetime(df["Fecha_Cosecha"])
df["Días_Cultivo"] = (df["Fecha_Cosecha"] - df["Fecha_Siembra"]).dt.days
plt.figure(figsize=(8, 5))
sns.histplot(df["Días_Cultivo"], bins=20, kde=True, color="darkgreen")
plt.title("📅 Distribución de los Días de Cultivo")
plt.xlabel("Días de Cultivo")
plt.ylabel("Frecuencia")
plt.grid(True)
st.pyplot()

# 🔹 Distribución de Horas de Sol
plt.figure(figsize=(8, 6))
sns.histplot(df["Horas_Sol"], bins=20, kde=True)
plt.title("☀️ Distribución de Horas de Sol Recibidas")
plt.xlabel("Horas de Sol")
plt.ylabel("Frecuencia")
plt.grid(True)
st.pyplot()

# 🔹 Comparación del Riego Aplicado por Tipo de Suelo
plt.figure(figsize=(10, 6))
sns.boxplot(x="Tipo_Suelo", y="Riego_Aplicado", data=df)
plt.xticks(rotation=45)
plt.title("💧 Comparación del Riego Aplicado por Tipo de Suelo")
plt.xlabel("Tipo de Suelo")
plt.ylabel("Riego Aplicado")
plt.grid(True)
st.pyplot()

# 🔹 Relación entre pH del Suelo y Humedad del Suelo
plt.figure(figsize=(8, 6))
sns.scatterplot(x="pH_Suelo", y="Humedad_Suelo", data=df, alpha=0.6)
sns.regplot(x="pH_Suelo", y="Humedad_Suelo", data=df, scatter=False, color="red")
plt.title("📈 Relación entre pH del Suelo y Humedad del Suelo")
plt.xlabel("pH del Suelo")
plt.ylabel("Humedad del Suelo")
st.pyplot()

# 🔹 Frecuencia de Plagas
plt.figure(figsize=(12, 6))
df["Plagas_Presentes"].str.split(", ").explode().value_counts().plot(kind="bar", color="coral")
plt.title("🐛 Frecuencia de Plagas Presentes en los Cultivos")
plt.xlabel("Plaga")
plt.ylabel("Cantidad de Cultivos Afectados")
plt.xticks(rotation=45)
plt.grid(axis="y")
st.pyplot()

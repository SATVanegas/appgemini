import streamlit as st
import pandas as pd
import geopandas as gpd

# Configuración de la app
st.set_page_config(page_title="Mi primera app", layout="centered")

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

# Guardar el archivo corregido
df.to_csv("artefactos_interpolados.csv", index=False)

# Mostrar vista previa de los datos corregidos
st.write("### Vista previa de los datos corregidos:")
st.dataframe(df.head())

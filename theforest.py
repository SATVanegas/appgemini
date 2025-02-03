import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq

# URL del archivo en GitHub
CSV_URL = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/main/archivos-datos/aplicaciones/deforestacion.csv"

@st.cache_data
def cargar_datos():
    return pd.read_csv(CSV_URL)

def main():
    st.title("Análisis de la Deforestación")
    datos = cargar_datos()
    
    # Mostrar datos iniciales
    st.subheader("Vista previa de los datos")
    st.dataframe(datos.head())
    
    # Análisis de superficie deforestada
    if "superficie_deforestada" in datos.columns:
        st.subheader("Análisis de Superficie Deforestada")
        st.write("Superficie total deforestada:", datos["superficie_deforestada"].sum())
        fig, ax = plt.subplots()
        datos["superficie_deforestada"].hist(bins=30, ax=ax)
        ax.set_title("Distribución de Superficie Deforestada")
        st.pyplot(fig)
    
    # Análisis de tasas de deforestación
    if "tasa_deforestacion" in datos.columns:
        st.subheader("Tasas de Deforestación")
        fig, ax = plt.subplots()
        datos["tasa_deforestacion"].hist(bins=30, ax=ax)
        ax.set_title("Distribución de Tasas de Deforestación")
        st.pyplot(fig)
    
    # Gráfico de torta según tipo de vegetación
    if "tipo_vegetacion" in datos.columns:
        st.subheader("Distribución por Tipo de Vegetación")
        fig, ax = plt.subplots()
        datos["tipo_vegetacion"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    
    # Mapas por variables seleccionadas
    st.subheader("Mapas personalizados")
    columnas_disponibles = ["latitud", "longitud", "superficie_deforestada", "altitud", "precipitacion"]
    opciones = st.multiselect("Selecciona hasta cuatro variables", columnas_disponibles, default=["latitud", "longitud", "superficie_deforestada"])
    
    if len(opciones) >= 2:
        fig, ax = plt.subplots()
        scatter = ax.scatter(datos[opciones[1]], datos[opciones[0]], c=datos[opciones[2]] if len(opciones) > 2 else 'red', alpha=0.5)
        ax.set_xlabel(opciones[1])
        ax.set_ylabel(opciones[0])
        ax.set_title("Mapa Personalizado")
        st.pyplot(fig)
    
    # Análisis de clústeres
    if all(col in datos.columns for col in ["latitud", "longitud", "superficie_deforestada"]):
        st.subheader("Clústeres de Deforestación")
        k = st.slider("Selecciona el número de clústeres", 2, 10, 3)
        X = datos[["latitud", "longitud", "superficie_deforestada"]].dropna().values
        centroids, _ = kmeans(X, k)
        idx, _ = vq(X, centroids)
        fig, ax = plt.subplots()
        scatter = ax.scatter(X[:, 1], X[:, 0], c=idx, cmap='viridis')
        ax.set_title("Clústeres de Deforestación")
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        st.pyplot(fig)
    
if __name__ == "__main__":
    main()
